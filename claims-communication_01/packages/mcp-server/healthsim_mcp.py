"""
HealthSim MCP Server.

Provides MCP tools for interacting with the HealthSim DuckDB database.
Uses close-before-write pattern for reliable database access:
- Persistent read-only connection for queries (shared lock, fast repeated reads)
- Write operations close read connection first, then open read-write connection
- Read connection reopens lazily after writes complete

This pattern is required because DuckDB does not allow simultaneous connections
with different read_only configurations to the same database file, even within
the same process.

See docs/mcp/duckdb-connection-architecture.md for design details.

Tools provided:
- healthsim_list_cohorts: List all saved cohorts
- healthsim_load_cohort: Load a cohort by name/ID
- healthsim_save_cohort: Save a new cohort (full replacement)
- healthsim_add_entities: Add entities incrementally (recommended for large datasets)
- healthsim_delete_cohort: Delete a cohort
- healthsim_query: Execute read-only SQL queries
- healthsim_get_cohort_summary: Get token-efficient cohort summary
- healthsim_query_reference: Query PopulationSim reference data
- healthsim_search_providers: Search real NPPES provider data
- healthsim_tables: List all tables in the database

DATA SOURCE DECISION GUIDE:
- Providers/Facilities: Use healthsim_search_providers to query REAL NPPES data (8.9M providers)
- PHI entities (patients, members, claims): Generate SYNTHETIC data
- Reference data (demographics, health indicators): Use healthsim_query_reference for real CDC/SVI data

Usage:
    python healthsim_mcp.py
    
Configuration in claude_desktop_config.json:
    "healthsim-mcp": {
        "command": "python",
        "args": ["/path/to/healthsim_mcp.py"]
    }

Environment Variables:
    HEALTHSIM_DB_PATH: Override default database path
"""

import atexit
import json
import os
import re
import signal
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

import duckdb
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict


# =============================================================================
# HTTP Transport Configuration
# =============================================================================

MCP_TRANSPORT = os.environ.get("MCP_TRANSPORT", "stdio")
# Railway sets PORT; MCP_PORT overrides; fallback 8000
MCP_PORT = int(os.environ.get("MCP_PORT", os.environ.get("PORT", "8000")))
MCP_TOKEN = os.environ.get("HEALTHSIM_MCP_TOKEN")

# Add healthsim to path
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))

from healthsim.db import DEFAULT_DB_PATH
from healthsim.state import StateManager
from healthsim.state.auto_persist import AutoPersistService
from healthsim.state.serializers import get_serializer, get_table_info


# =============================================================================
# Entity Type Taxonomy - Defines what can be stored in cohorts
# =============================================================================

# SCENARIO DATA: Synthetic PHI entities that are generated per-cohort
# These are the ONLY entity types that should be stored in cohort_entities
SCENARIO_ENTITY_TYPES = {
    "patients",      # Synthetic patient demographics
    "members",       # Synthetic insurance enrollment  
    "claims",        # Synthetic claims/utilization
    "claim_lines",   # Synthetic claim line items
    "encounters",    # Synthetic clinical encounters
    "prescriptions", # Synthetic medication records
    "subjects",      # Clinical trial subjects
}

# RELATIONSHIP ENTITIES: Link cohort data to reference data via IDs/NPIs
# These store relationships, not copies of reference data
RELATIONSHIP_ENTITY_TYPES = {
    "pcp_assignments",      # member_id → provider_npi
    "network_contracts",    # plan_id → provider_npi  
    "authorizations",       # member_id → service → provider_npi
    "referrals",            # member_id → from_npi → to_npi
    "facility_assignments", # member_id → facility_npi
}

# REFERENCE DATA: Real-world data that should NEVER be copied into cohorts
# These exist in shared reference tables (network.providers, population.*, etc.)
REFERENCE_ENTITY_TYPES = {
    "providers",    # → Query network.providers (8.9M NPPES records)
    "facilities",   # → Query network.providers with entity_type=2
    "pharmacies",   # → Query network.providers with taxonomy LIKE '333600%'
    "hospitals",    # → Query network.providers with taxonomy LIKE '282N%'
    "organizations",# → Query network.providers with entity_type=2
}

# Combined set of allowed types for validation
ALLOWED_ENTITY_TYPES = SCENARIO_ENTITY_TYPES | RELATIONSHIP_ENTITY_TYPES


# =============================================================================
# Configuration from Environment
# =============================================================================

# Allow override via environment variable
# Supports local file paths OR MotherDuck connection strings (md:database_name)
_db_env = os.environ.get("HEALTHSIM_DB_PATH", str(DEFAULT_DB_PATH))
IS_MOTHERDUCK = _db_env.startswith("md:")

if IS_MOTHERDUCK:
    DB_PATH = _db_env  # MotherDuck connection string, not a file path
else:
    DB_PATH = Path(_db_env)

# Log startup configuration (to stderr so it doesn't interfere with MCP protocol)
_display_path = re.sub(r'motherduck_token=[^&\s]+', 'motherduck_token=***', str(DB_PATH))
print(f"HealthSim MCP Server starting...", file=sys.stderr)
print(f"  Database: {_display_path}", file=sys.stderr)
if IS_MOTHERDUCK:
    print(f"  Connection mode: MotherDuck (cloud)", file=sys.stderr)
else:
    print(f"  Connection mode: dual (read-only persistent + on-demand write)", file=sys.stderr)
    print(f"  DB exists: {DB_PATH.exists()}", file=sys.stderr)


# =============================================================================
# Connection Manager - Close-Before-Write Pattern
# =============================================================================

class ConnectionManager:
    """
    Manages DuckDB connections using close-before-write pattern.

    For local files:
      DuckDB Constraint: Cannot have simultaneous connections with different
      read_only configurations to the same database file, even in the same process.
      Solution: read-only persistent + close-before-write for writes.

    For MotherDuck:
      Single persistent connection (MotherDuck handles concurrency server-side).
    """

    def __init__(self, db_path, is_motherduck: bool = False):
        self.db_path = db_path
        self.is_motherduck = is_motherduck
        self._read_conn: Optional[duckdb.DuckDBPyConnection] = None
        self._read_manager: Optional[StateManager] = None

    def get_read_connection(self) -> duckdb.DuckDBPyConnection:
        """
        Get persistent read connection.

        Local: read-only with shared lock and retry logic.
        MotherDuck: single persistent connection (no read_only flag).
        """
        import time

        if self._read_conn is None:
            if self.is_motherduck:
                self._read_conn = duckdb.connect(self.db_path)
                print(f"  Opened MotherDuck connection", file=sys.stderr)
            else:
                max_retries = 3
                retry_delay = 0.1
                for attempt in range(max_retries):
                    try:
                        self._read_conn = duckdb.connect(str(self.db_path), read_only=True)
                        print(f"  Opened read-only connection to {self.db_path}", file=sys.stderr)
                        break
                    except Exception as e:
                        if attempt < max_retries - 1 and "lock" in str(e).lower():
                            print(f"  Read connection attempt {attempt + 1} failed (lock), retrying...", file=sys.stderr)
                            time.sleep(retry_delay)
                            retry_delay *= 2
                        else:
                            raise
        return self._read_conn
    
    def get_read_manager(self) -> StateManager:
        """Get StateManager backed by read-only connection."""
        if self._read_manager is None:
            self._read_manager = StateManager(connection=self.get_read_connection())
        return self._read_manager
    
    def _close_read_connection(self):
        """
        Close the read connection.
        
        Called before write operations to avoid DuckDB configuration conflicts.
        The read connection will be lazily reopened on the next read operation.
        """
        if self._read_conn is not None:
            self._read_conn.close()
            self._read_conn = None
            self._read_manager = None
            print(f"  Closed read-only connection (preparing for write)", file=sys.stderr)
    
    @contextmanager
    def write_connection(self):
        """
        Context manager for write operations.

        Local: close-before-write pattern to avoid DuckDB lock conflicts.
        MotherDuck: reuses the persistent connection (server-side concurrency).
        """
        if self.is_motherduck:
            # MotherDuck: just yield the persistent connection
            yield self.get_read_connection()
        else:
            import time

            self._close_read_connection()
            time.sleep(0.05)

            conn = duckdb.connect(str(self.db_path))
            print(f"  Opened read-write connection for write operation", file=sys.stderr)
            try:
                yield conn
            finally:
                try:
                    conn.execute("CHECKPOINT")
                    print(f"  Checkpointed database", file=sys.stderr)
                except Exception as e:
                    print(f"  Checkpoint warning: {e}", file=sys.stderr)
                conn.close()
                print(f"  Closed read-write connection (write complete)", file=sys.stderr)
                time.sleep(0.05)
    
    @contextmanager
    def write_manager(self):
        """
        Context manager for StateManager with write capability.
        
        Usage:
            with manager.write_manager() as state_mgr:
                state_mgr.save_cohort(...)
        """
        with self.write_connection() as conn:
            yield StateManager(connection=conn)
    
    @contextmanager
    def write_auto_persist(self):
        """
        Context manager for AutoPersistService with write capability.
        
        Usage:
            with manager.write_auto_persist() as service:
                service.persist_entities(...)
        """
        with self.write_connection() as conn:
            yield AutoPersistService(connection=conn)
    
    def close(self):
        """Close all connections."""
        if self._read_conn:
            self._read_conn.close()
            self._read_conn = None
            self._read_manager = None
            print(f"  Closed read-only connection", file=sys.stderr)


# Global connection manager
_manager: Optional[ConnectionManager] = None


def _get_manager() -> ConnectionManager:
    """Get or create the connection manager."""
    global _manager
    if _manager is None:
        _manager = ConnectionManager(DB_PATH, is_motherduck=IS_MOTHERDUCK)
    return _manager


def _cleanup_connections():
    """Clean up database connections on shutdown."""
    global _manager
    if _manager is not None:
        print("  Cleaning up database connections...", file=sys.stderr)
        _manager.close()
        _manager = None
        print("  Database connections closed", file=sys.stderr)


def _signal_handler(signum, frame):
    """Handle termination signals gracefully."""
    print(f"  Received signal {signum}, shutting down...", file=sys.stderr)
    _cleanup_connections()
    sys.exit(0)


# Register cleanup handlers
atexit.register(_cleanup_connections)
signal.signal(signal.SIGTERM, _signal_handler)
signal.signal(signal.SIGINT, _signal_handler)


def _ensure_sequences():
    """Ensure required sequences exist (for databases created before sequences were added)."""
    try:
        if IS_MOTHERDUCK:
            conn = duckdb.connect(DB_PATH)
        else:
            conn = duckdb.connect(str(DB_PATH))
        conn.execute("CREATE SEQUENCE IF NOT EXISTS cohort_tags_seq START 1")
        conn.execute("CREATE SEQUENCE IF NOT EXISTS cohort_entities_seq START 1")
        conn.close()
    except Exception as e:
        print(f"  Warning: Could not ensure sequences: {e}", file=sys.stderr)


_ensure_sequences()


# Initialize the MCP server
mcp = FastMCP("healthsim_mcp", host="0.0.0.0", port=MCP_PORT)


# =============================================================================
# Pydantic Input Models
# =============================================================================

class ListCohortsInput(BaseModel):
    """Input for listing cohorts."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    tag: Optional[str] = Field(default=None, description="Filter by tag")
    search: Optional[str] = Field(default=None, description="Search in name/description")
    limit: int = Field(default=50, description="Maximum results", ge=1, le=200)


class LoadCohortInput(BaseModel):
    """Input for loading a cohort."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name_or_id: str = Field(..., description="Cohort name or UUID", min_length=1)
    include_entities: bool = Field(default=True, description="Include full entity data")


class SaveCohortInput(BaseModel):
    """Input for saving a cohort."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: str = Field(..., description="Unique cohort name", min_length=1, max_length=200)
    entities: Dict[str, List[Dict[str, Any]]] = Field(..., description="Entity dict: {type: [entities]}")
    description: Optional[str] = Field(default=None, description="Cohort description")
    tags: Optional[List[str]] = Field(default=None, description="Tags for filtering")
    overwrite: bool = Field(default=False, description="Overwrite if exists")
    allow_reference_entities: bool = Field(
        default=False, 
        description="Set True to intentionally store reference-type entities (providers, facilities). "
                    "Only use when synthetic data is explicitly needed for testing or demos."
    )


class AddEntitiesInput(BaseModel):
    """Input for adding entities incrementally to a cohort.
    
    This is the RECOMMENDED approach for large datasets. It:
    - Adds entities without deleting existing ones
    - Handles duplicates gracefully (upsert behavior)
    - Returns a summary instead of echoing all data (token-efficient)
    - Supports batched operations across multiple calls
    """
    model_config = ConfigDict(str_strip_whitespace=True)
    
    # Scenario identification - use ONE of these
    cohort_id: Optional[str] = Field(
        default=None, 
        description="Existing cohort UUID to add entities to. If provided, entities are added to this cohort."
    )
    cohort_name: Optional[str] = Field(
        default=None,
        description="Cohort name. If cohort_id not provided, creates new cohort with this name or auto-generates one."
    )
    
    # Entities to add
    entities: Dict[str, List[Dict[str, Any]]] = Field(
        ..., 
        description="Entity dict: {type: [entities]}. Example: {'patients': [...], 'members': [...]}"
    )
    
    # Optional metadata (only used when creating new cohort)
    description: Optional[str] = Field(default=None, description="Cohort description (for new cohorts)")
    tags: Optional[List[str]] = Field(default=None, description="Tags for filtering (for new cohorts)")
    
    # Batch tracking (optional, for progress reporting)
    batch_number: Optional[int] = Field(default=None, description="Current batch number (e.g., 1, 2, 3)")
    total_batches: Optional[int] = Field(default=None, description="Total number of batches expected")
    
    # Override for intentional reference data storage
    allow_reference_entities: bool = Field(
        default=False, 
        description="Set True to intentionally store reference-type entities (providers, facilities). "
                    "Only use when synthetic data is explicitly needed for testing or demos."
    )


class DeleteCohortInput(BaseModel):
    """Input for deleting a cohort."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name_or_id: str = Field(..., description="Cohort name or UUID", min_length=1)
    confirm: bool = Field(default=False, description="Must be True to delete")


class QueryInput(BaseModel):
    """Input for SQL queries."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    sql: str = Field(..., description="SQL query (SELECT only)", min_length=1)
    limit: int = Field(default=100, description="Max rows to return", ge=1, le=1000)


class GetSummaryInput(BaseModel):
    """Input for getting cohort summary."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    cohort_id_or_name: str = Field(..., description="Cohort name or UUID", min_length=1)
    include_samples: bool = Field(default=True, description="Include sample entities")
    samples_per_type: int = Field(default=3, description="Samples per entity type", ge=1, le=10)


class QueryReferenceInput(BaseModel):
    """Input for querying reference data."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    table: str = Field(..., description="Reference table: places_county, places_tract, svi_county, svi_tract, adi_blockgroup")
    state: Optional[str] = Field(default=None, description="Filter by state abbreviation (e.g., 'CA')")
    county: Optional[str] = Field(default=None, description="Filter by county name")
    limit: int = Field(default=20, description="Max rows", ge=1, le=100)


class SearchProvidersInput(BaseModel):
    """Input for searching real NPPES provider data.
    
    This searches REAL registered providers from the NPPES database (8.9M records).
    Use this BEFORE generating synthetic providers to check if real data is available.
    """
    model_config = ConfigDict(str_strip_whitespace=True)
    
    # Location filters
    state: str = Field(..., description="State abbreviation (e.g., 'CA', 'TX')")
    city: Optional[str] = Field(default=None, description="City name (optional)")
    county_fips: Optional[str] = Field(default=None, description="5-digit county FIPS code (optional)")
    zip_code: Optional[str] = Field(default=None, description="ZIP code (5 digits, optional)")
    
    # Specialty filters
    specialty: Optional[str] = Field(
        default=None, 
        description="Specialty keyword (e.g., 'Family Medicine', 'Cardiology', 'Internal Medicine')"
    )
    taxonomy_code: Optional[str] = Field(
        default=None, 
        description="NUCC taxonomy code (e.g., '207Q00000X' for Family Medicine)"
    )
    
    # Entity type
    entity_type: Optional[str] = Field(
        default=None,
        description="'individual' (NPI-1) or 'organization' (NPI-2). Default: both"
    )
    
    # Results
    limit: int = Field(default=50, description="Max results to return", ge=1, le=200)


# =============================================================================
# Canonical Table Helpers
# =============================================================================

def insert_into_canonical_table(
    conn,
    cohort_id: str,
    entity_type: str,
    entity: Dict[str, Any]
) -> tuple:
    """
    Insert entity into canonical table using serializer.
    
    This mirrors the behavior of StateManager._insert_canonical_entity to ensure
    that add_entities writes to both cohort_entities AND canonical tables.
    
    Args:
        conn: DuckDB connection
        cohort_id: Scenario UUID
        entity_type: Normalized entity type (e.g., 'patients', 'members')
        entity: Entity data dict
        
    Returns:
        Tuple of (success: bool, error_message: str or None)
    """
    serializer = get_serializer(entity_type)
    if not serializer:
        # No serializer for this entity type - skip canonical insert
        return (False, f"No serializer for entity type: {entity_type}")
    
    try:
        table_name, id_column = get_table_info(entity_type)
        
        # Get provenance from entity (supports both '_provenance' and 'provenance' keys)
        provenance = entity.get('_provenance', {})
        if 'provenance' in entity:
            prov_data = entity['provenance']
            if isinstance(prov_data, dict):
                provenance = prov_data
        
        # Serialize entity to canonical format
        data = serializer(entity, provenance)
        
        # Add cohort_id to data
        data['cohort_id'] = cohort_id
        
        # Filter to only columns that exist in the table
        schema_result = conn.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
        """).fetchall()
        valid_columns = {row[0] for row in schema_result}
        
        if not valid_columns:
            return (False, f"Table '{table_name}' not found or has no columns")
        
        # Filter data to only include valid columns
        filtered_data = {k: v for k, v in data.items() if k in valid_columns}
        removed_columns = set(data.keys()) - set(filtered_data.keys())
        
        if not filtered_data:
            return (False, f"No valid columns for {table_name}. Data keys: {list(data.keys())}, Table columns: {list(valid_columns)}")
        
        # Build INSERT statement with conflict handling
        columns = list(filtered_data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        
        # For conflict handling, update all columns except the primary key
        non_pk_columns = [c for c in columns if c != id_column]
        updates = ', '.join([f"{col} = excluded.{col}" for col in non_pk_columns])
        
        sql = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT ({id_column}) DO UPDATE SET {updates}
        """
        
        conn.execute(sql, list(filtered_data.values()))
        return (True, None)
        
    except Exception as e:
        # Return the actual error for diagnosis
        import traceback
        error_detail = f"{type(e).__name__}: {e}"
        print(f"[CANONICAL INSERT ERROR] {entity_type}: {error_detail}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return (False, error_detail)


# =============================================================================
# Validation Helpers
# =============================================================================

def validate_entity_types(
    entities: Dict[str, List[Dict[str, Any]]], 
    allow_reference_override: bool = False
) -> Optional[str]:
    """
    Validate that entity types are appropriate for cohort storage.
    
    Args:
        entities: Dict of entity_type -> list of entities
        allow_reference_override: If True, allows reference types with a warning
        
    Returns None if valid, or an error message string if invalid.
    """
    for entity_type in entities.keys():
        # Normalize to lowercase plural
        normalized = entity_type.lower()
        if not normalized.endswith('s'):
            normalized += 's'
        
        # Check if it's reference data (should NOT be stored in cohorts by default)
        if normalized in REFERENCE_ENTITY_TYPES:
            if allow_reference_override:
                # User explicitly requested synthetic reference data - allow with info
                return None  # Continue - will log info in the response
            else:
                # Default: suggest using real data instead
                return (
                    f"⚠️ '{entity_type}' is typically REFERENCE DATA that exists in shared tables.\n\n"
                    f"RECOMMENDED: Use real data from network.providers (8.9M+ records):\n"
                    f"  → healthsim_search_providers(state='CA', specialty='Family Medicine')\n"
                    f"  → Then store relationships via 'pcp_assignments' or 'network_contracts'\n\n"
                    f"TO OVERRIDE: If you intentionally need synthetic {entity_type} for testing/demos,\n"
                    f"set allow_reference_entities=True in your request.\n\n"
                    f"Example with override:\n"
                    f"  healthsim_add_entities(\n"
                    f"    cohort_id='...',\n"
                    f"    entities={{'{entity_type}': [...]}},\n"
                    f"    allow_reference_entities=True  # Explicit override\n"
                    f"  )"
                )
        
        # Check if it's an allowed type (cohort data, relationships, or overridden reference)
        if normalized not in ALLOWED_ENTITY_TYPES and normalized not in REFERENCE_ENTITY_TYPES:
            return (
                f"⚠️ Unknown entity type: '{entity_type}'\n\n"
                f"Allowed cohort entity types:\n"
                f"  Scenario data: {sorted(SCENARIO_ENTITY_TYPES)}\n"
                f"  Relationships: {sorted(RELATIONSHIP_ENTITY_TYPES)}\n"
                f"  Reference (with override): {sorted(REFERENCE_ENTITY_TYPES)}\n\n"
                f"If this is a new valid entity type, add it to the taxonomy in healthsim_mcp.py"
            )
    
    return None  # Valid


# =============================================================================
# Tool Implementations - READ Operations (use persistent read connection)
# =============================================================================

@mcp.tool(
    name="healthsim_list_cohorts",
    annotations={
        "title": "List HealthSim Cohorts",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def list_cohorts(params: ListCohortsInput) -> str:
    """List all saved cohorts in the HealthSim database.
    
    Returns cohort names, descriptions, entity counts, and tags.
    Use this to discover available cohorts before loading them.
    
    Returns:
        JSON list of cohort summaries with: cohort_id, name, description,
        created_at, updated_at, entity_count, tags
    """
    manager = _get_manager().get_read_manager()
    
    cohorts = manager.list_cohorts(
        tag=params.tag,
        search=params.search,
        limit=params.limit,
    )
    
    # Format for readability
    result = []
    for s in cohorts:
        result.append({
            "cohort_id": s["cohort_id"],
            "name": s["name"],
            "description": s.get("description"),
            "entity_count": s.get("entity_count", 0),
            "tags": s.get("tags", []),
            "created_at": str(s.get("created_at", "")),
            "updated_at": str(s.get("updated_at", "")),
        })
    
    return json.dumps(result, indent=2, default=str)


@mcp.tool(
    name="healthsim_load_cohort",
    annotations={
        "title": "Load HealthSim Cohort",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def load_cohort(params: LoadCohortInput) -> str:
    """Load a cohort by name or ID.
    
    Returns full cohort data including all entities. For large cohorts,
    consider using healthsim_get_cohort_summary instead for a token-efficient summary.
    
    Returns:
        JSON with cohort metadata and entities dict
    """
    manager = _get_manager().get_read_manager()
    
    try:
        cohort = manager.load_cohort(params.name_or_id)
        
        if not params.include_entities:
            # Return metadata only
            cohort.pop("entities", None)
        
        return json.dumps(cohort, indent=2, default=str)
    except ValueError as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_query",
    annotations={
        "title": "Query HealthSim Database",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def query(params: QueryInput) -> str:
    """Execute a SQL query against the HealthSim database.
    
    Only SELECT queries are allowed. Use this for:
    - Exploring reference data (population.places_county, population.svi_tract, etc.)
    - Querying entity tables (patients, members, encounters, claims)
    - Running analytics queries
    
    Available tables: SHOW TABLES for full list.
    
    Returns:
        JSON with columns and rows
    """
    conn = _get_manager().get_read_connection()
    
    # Basic SQL injection protection
    sql_lower = params.sql.lower().strip()
    if not sql_lower.startswith(("select", "show", "describe", "with")):
        return json.dumps({
            "error": "Only SELECT, SHOW, DESCRIBE, and WITH queries are allowed",
        })
    
    # Check for dangerous keywords
    dangerous = ["insert", "update", "delete", "drop", "alter", "create", "truncate"]
    for keyword in dangerous:
        if keyword in sql_lower.split():
            return json.dumps({
                "error": f"Query contains forbidden keyword: {keyword}",
            })
    
    try:
        # Add LIMIT if not present
        if "limit" not in sql_lower:
            sql = f"{params.sql.rstrip(';')} LIMIT {params.limit}"
        else:
            sql = params.sql
        
        result = conn.execute(sql).fetchall()
        columns = [desc[0] for desc in conn.description]
        
        # Convert to list of dicts
        rows = []
        for row in result:
            rows.append({col: val for col, val in zip(columns, row)})
        
        return json.dumps({
            "columns": columns,
            "row_count": len(rows),
            "rows": rows,
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_get_cohort_summary",
    annotations={
        "title": "Get Scenario Summary",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def get_summary(params: GetSummaryInput) -> str:
    """Get a token-efficient summary of a cohort.
    
    Use this instead of load_cohort when you need context about a cohort
    without loading all entities (~500 tokens vs potentially 10K+).
    
    Returns:
        JSON with entity counts, statistics, and optional samples
    """
    manager = _get_manager().get_read_manager()
    
    try:
        summary = manager.get_summary(
            params.cohort_id_or_name,
            include_samples=params.include_samples,
            samples_per_type=params.samples_per_type,
        )
        
        # Convert to dict for JSON serialization
        return json.dumps(summary.to_dict(), indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_query_reference",
    annotations={
        "title": "Query Reference Data",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def query_reference(params: QueryReferenceInput) -> str:
    """Query PopulationSim reference data tables.
    
    Available tables:
    - places_county: CDC PLACES county-level health indicators (3,143 rows)
    - places_tract: CDC PLACES tract-level health indicators (83,522 rows)
    - svi_county: Social Vulnerability Index by county (3,144 rows)
    - svi_tract: Social Vulnerability Index by tract (84,120 rows)
    - adi_blockgroup: Area Deprivation Index by block group (242,336 rows)
    
    Returns:
        JSON with columns and filtered rows
    """
    conn = _get_manager().get_read_connection()
    
    # Map short names to full schema-qualified table names
    table_map = {
        "places_county": "population.places_county",
        "places_tract": "population.places_tract",
        "svi_county": "population.svi_county",
        "svi_tract": "population.svi_tract",
        "adi_blockgroup": "population.adi_blockgroup",
    }
    
    # Map table names to their state column (different sources use different naming)
    state_column_map = {
        "places_county": "stateabbr",
        "places_tract": "stateabbr", 
        "svi_county": "st_abbr",
        "svi_tract": "st_abbr",
        "adi_blockgroup": "fips",  # ADI uses 12-digit FIPS in fips column
    }
    
    # Map table names to their county column
    county_column_map = {
        "places_county": "countyname",
        "places_tract": "countyname",
        "svi_county": "county",
        "svi_tract": "county",
        "adi_blockgroup": "fips",  # ADI uses FIPS codes, no county name
    }
    
    table = table_map.get(params.table)
    if not table:
        return json.dumps({
            "error": f"Unknown table: {params.table}",
            "available": list(table_map.keys()),
        })
    
    # Build query with filters
    conditions = []
    query_params = []
    
    state_col = state_column_map.get(params.table, "stateabbr")
    county_col = county_column_map.get(params.table, "countyname")
    
    # State abbreviation to FIPS mapping for ADI queries
    STATE_FIPS = {
        "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06",
        "CO": "08", "CT": "09", "DE": "10", "FL": "12", "GA": "13",
        "HI": "15", "ID": "16", "IL": "17", "IN": "18", "IA": "19",
        "KS": "20", "KY": "21", "LA": "22", "ME": "23", "MD": "24",
        "MA": "25", "MI": "26", "MN": "27", "MS": "28", "MO": "29",
        "MT": "30", "NE": "31", "NV": "32", "NH": "33", "NJ": "34",
        "NM": "35", "NY": "36", "NC": "37", "ND": "38", "OH": "39",
        "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45",
        "SD": "46", "TN": "47", "TX": "48", "UT": "49", "VT": "50",
        "VA": "51", "WA": "53", "WV": "54", "WI": "55", "WY": "56",
        "DC": "11", "PR": "72",
    }
    
    if params.state:
        # Handle ADI specially - it uses FIPS codes, not state abbreviations
        if params.table == "adi_blockgroup":
            # State FIPS is first 2 chars of gidbg
            state_fips = STATE_FIPS.get(params.state.upper(), params.state)
            conditions.append(f"SUBSTRING({state_col}, 1, 2) = ?")
            query_params.append(state_fips)
        else:
            conditions.append(f"{state_col} = ?")
            query_params.append(params.state.upper())
    
    if params.county:
        if params.table == "adi_blockgroup":
            # ADI doesn't have a county name column, skip this filter
            pass
        else:
            conditions.append(f"{county_col} ILIKE ?")
            query_params.append(f"%{params.county}%")
    
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    sql = f"SELECT * FROM {table}{where_clause} LIMIT {params.limit}"
    
    try:
        result = conn.execute(sql, query_params).fetchall()
        columns = [desc[0] for desc in conn.description]
        
        rows = []
        for row in result:
            rows.append({col: val for col, val in zip(columns, row)})
        
        return json.dumps({
            "table": table,
            "columns": columns,
            "row_count": len(rows),
            "rows": rows,
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_tables",
    annotations={
        "title": "List Database Tables",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def list_tables() -> str:
    """List all tables in the HealthSim database.
    
    Returns table names grouped by category:
    - Reference tables (ref_*): PopulationSim demographic/health data
    - Entity tables: patients, members, encounters, claims, etc.
    - System tables: cohorts, cohort_entities, schema_migrations
    
    Returns:
        JSON with categorized table names
    """
    conn = _get_manager().get_read_connection()
    
    result = conn.execute("SHOW TABLES").fetchall()
    tables = [row[0] for row in result]
    
    # Categorize
    reference = [t for t in tables if t.startswith("ref_")]
    system = ["cohorts", "cohort_entities", "cohort_tags", "schema_migrations"]
    entity = [t for t in tables if t not in reference and t not in system]
    
    return json.dumps({
        "reference_tables": reference,
        "entity_tables": entity,
        "system_tables": [t for t in system if t in tables],
        "total": len(tables),
    }, indent=2)


@mcp.tool(
    name="healthsim_search_providers",
    annotations={
        "title": "Search Real NPPES Providers",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def search_providers(params: SearchProvidersInput) -> str:
    """Search real healthcare providers from NPPES data (8.9M records).
    
    ⚠️ USE THIS TOOL FIRST when providers are needed for a cohort.
    Returns REAL, registered healthcare providers with valid NPIs.
    Only generate synthetic providers if real data is unavailable or explicitly requested.
    
    Common taxonomy codes for Primary Care:
    - 207Q00000X: Family Medicine
    - 207R00000X: Internal Medicine
    - 208D00000X: General Practice
    - 363L00000X: Nurse Practitioner
    - 363A00000X: Physician Assistant
    
    Common taxonomy codes for Specialists:
    - 207RC0000X: Cardiovascular Disease
    - 207RG0100X: Gastroenterology
    - 2084N0400X: Neurology
    - 207RX0202X: Medical Oncology
    - 2086S0122X: Orthopedic Surgery
    
    Returns:
        JSON with provider records including NPI, name, specialty, location
    """
    conn = _get_manager().get_read_connection()
    
    # Check if network.providers table exists
    try:
        table_check = conn.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'providers'"
        ).fetchone()
        if not table_check or table_check[0] == 0:
            return json.dumps({
                "error": "NPPES provider data not loaded. Run NetworkSim data import first.",
                "hint": "See skills/networksim/data/ for import instructions",
            })
    except Exception:
        return json.dumps({
            "error": "network.providers table not available",
            "hint": "NPPES provider data may not be loaded in this database",
        })
    
    # Build query with filters
    conditions = ["1=1"]  # Base condition for easier AND chaining
    query_params = []
    
    # State is required
    conditions.append("practice_state = ?")
    query_params.append(params.state.upper())
    
    # Optional filters
    if params.city:
        conditions.append("practice_city ILIKE ?")
        query_params.append(f"%{params.city}%")
    
    if params.county_fips:
        conditions.append("county_fips = ?")
        query_params.append(params.county_fips)
    
    if params.zip_code:
        conditions.append("practice_zip LIKE ?")
        query_params.append(f"{params.zip_code}%")
    
    if params.taxonomy_code:
        # Search across all 4 taxonomy columns
        conditions.append("(taxonomy_1 = ? OR taxonomy_2 = ? OR taxonomy_3 = ? OR taxonomy_4 = ?)")
        query_params.extend([params.taxonomy_code] * 4)
    elif params.specialty:
        # Search taxonomy descriptions (requires join or subquery)
        # For now, search in common taxonomy codes based on specialty keyword
        specialty_lower = params.specialty.lower()
        taxonomy_patterns = []
        
        if 'family' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '207Q%'")
        if 'internal' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '207R%'")
        if 'cardio' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '207RC%'")
        if 'neuro' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '2084N%'")
        if 'gastro' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '207RG%'")
        if 'oncol' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '207RX%'")
        if 'ortho' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '2086S%'")
        if 'nurse' in specialty_lower or 'np' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '363L%'")
        if 'physician assistant' in specialty_lower or 'pa-c' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '363A%'")
        if 'hospital' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '282N%'")
        if 'urgent' in specialty_lower:
            taxonomy_patterns.append("taxonomy_1 LIKE '261QU%'")
        
        if taxonomy_patterns:
            conditions.append(f"({' OR '.join(taxonomy_patterns)})")
    
    if params.entity_type:
        if params.entity_type.lower() == 'individual':
            conditions.append("entity_type_code = 1")
        elif params.entity_type.lower() == 'organization':
            conditions.append("entity_type_code = 2")
    
    where_clause = " AND ".join(conditions)
    
    sql = f"""
        SELECT 
            npi,
            entity_type_code,
            CASE WHEN entity_type_code = 1 THEN first_name || ' ' || last_name
                 ELSE organization_name END as name,
            credential,
            taxonomy_1 as primary_taxonomy,
            practice_address_1 as practice_address,
            practice_city,
            practice_state,
            practice_zip,
            county_fips,
            phone
        FROM network.providers
        WHERE {where_clause}
        LIMIT {params.limit}
    """
    
    try:
        result = conn.execute(sql, query_params).fetchall()
        columns = [desc[0] for desc in conn.description]
        
        rows = []
        for row in result:
            rows.append({col: val for col, val in zip(columns, row)})
        
        return json.dumps({
            "source": "NPPES (National Plan and Provider Enumeration System)",
            "data_type": "REAL registered providers",
            "filters_applied": {
                "state": params.state,
                "city": params.city,
                "specialty": params.specialty,
                "taxonomy_code": params.taxonomy_code,
                "entity_type": params.entity_type,
            },
            "result_count": len(rows),
            "providers": rows,
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


# =============================================================================
# Tool Implementations - WRITE Operations (use on-demand write connection)
# =============================================================================

@mcp.tool(
    name="healthsim_save_cohort",
    annotations={
        "title": "Save HealthSim Cohort",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
    }
)
def save_cohort(params: SaveCohortInput) -> str:
    """Save a cohort to the HealthSim database.
    
    ⚠️  USE healthsim_add_entities INSTEAD when:
    - Total entity count exceeds 50 (to avoid token limit truncation)
    - Building cohorts incrementally across multiple calls
    - Adding entities to an existing cohort
    
    This tool REPLACES ALL entities in one atomic operation.
    Only use for small, complete datasets (≤50 entities total).
    
    Entities should be a dict mapping entity type to list of entities:
    {
        "patients": [{...}, {...}],
        "encounters": [{...}],
        "claims": [{...}]
    }
    
    Supported entity types: patients, members, encounters, claims, 
    claim_lines, prescriptions, subjects, etc.
    
    Returns:
        JSON with cohort_id and status
    """
    try:
        # Validate entity types - suggest real data unless override is set
        validation_error = validate_entity_types(
            params.entities, 
            allow_reference_override=params.allow_reference_entities
        )
        if validation_error:
            return json.dumps({"error": validation_error})
        
        # Use write connection for the save operation
        with _get_manager().write_manager() as manager:
            cohort_id = manager.save_cohort(
                name=params.name,
                entities=params.entities,
                description=params.description,
                tags=params.tags,
                overwrite=params.overwrite,
            )
        
        # Get entity counts
        entity_counts = {k: len(v) for k, v in params.entities.items()}
        
        return json.dumps({
            "status": "saved",
            "cohort_id": cohort_id,
            "name": params.name,
            "entity_counts": entity_counts,
            "total_entities": sum(entity_counts.values()),
        }, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": f"Save failed: {str(e)}"})


@mcp.tool(
    name="healthsim_add_entities",
    annotations={
        "title": "Add Entities to Scenario (Incremental)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,  # Upsert behavior makes it idempotent
    }
)
def add_entities(params: AddEntitiesInput) -> str:
    """Add entities incrementally to a cohort (RECOMMENDED for most use cases).
    
    ⚠️ REAL vs SYNTHETIC DATA DECISION:
    - For PROVIDERS/FACILITIES: Use healthsim_search_providers FIRST to get real NPPES data
    - For PHI entities (patients, members, claims): Generate synthetic data here
    - Only generate synthetic providers if real data unavailable or explicitly requested
    
    ✅ USE THIS TOOL when:
    - Total entity count exceeds 50 (avoids token limit truncation)
    - Building cohorts in batches across multiple calls
    - Adding new entity types to existing cohorts
    - Updating specific entities without affecting others
    
    This tool uses UPSERT logic:
    - Adds new entities
    - Updates existing entities (matched by entity_id)
    - NEVER deletes entities not in the current payload
    
    Returns a summary (not full data) to stay within token limits.
    
    Usage patterns:
    
    1. CREATE NEW SCENARIO (first batch):
       {"cohort_name": "My Scenario", "entities": {"patients": [...]}}
       
    2. ADD TO EXISTING (subsequent batches):
       {"cohort_id": "uuid-from-first-call", "entities": {"patients": [...]}}
       
    3. ADD DIFFERENT ENTITY TYPES:
       {"cohort_id": "uuid", "entities": {"members": [...]}}
    
    Batch tracking (optional):
       {"cohort_id": "uuid", "entities": {...}, "batch_number": 2, "total_batches": 4}
    
    Returns:
        JSON with cohort_id, entity counts, and summary (NOT full entity data)
    """
    try:
        # Validate: need at least one of cohort_id or cohort_name for new cohorts
        if not params.cohort_id and not params.cohort_name and not params.entities:
            return json.dumps({
                "error": "Must provide cohort_id (to add to existing) or cohort_name (to create new), plus entities"
            })
        
        # Validate entity types - suggest real data unless override is set
        validation_error = validate_entity_types(
            params.entities,
            allow_reference_override=params.allow_reference_entities
        )
        if validation_error:
            return json.dumps({"error": validation_error})
        
        # Use write connection for the add operation
        with _get_manager().write_auto_persist() as service:
            # Determine cohort context
            cohort_id = params.cohort_id
            cohort_name = params.cohort_name
            is_new_cohort = False
            
            # If no cohort_id provided, we need to create or find the cohort
            if not cohort_id:
                if cohort_name:
                    # Check if cohort exists
                    existing = service.conn.execute(
                        "SELECT id FROM cohorts WHERE name = ?",
                        [cohort_name]
                    ).fetchone()
                    
                    if existing:
                        cohort_id = existing[0]
                    else:
                        # Create new cohort
                        is_new_cohort = True
                        cohort_id = str(uuid4())
                        now = datetime.utcnow()
                        
                        service.conn.execute("""
                            INSERT INTO cohorts (id, name, description, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?)
                        """, [cohort_id, cohort_name, params.description, now, now])
                        
                        # Add tags if provided
                        if params.tags:
                            for tag in params.tags:
                                service.conn.execute("""
                                    INSERT INTO cohort_tags (id, cohort_id, tag)
                                    VALUES (nextval('cohort_tags_seq'), ?, ?)
                                """, [cohort_id, tag.lower()])
                else:
                    # Auto-generate cohort name
                    is_new_cohort = True
                    cohort_id = str(uuid4())
                    cohort_name = f"cohort-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
                    now = datetime.utcnow()
                    
                    service.conn.execute("""
                        INSERT INTO cohorts (id, name, description, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, [cohort_id, cohort_name, params.description, now, now])
            else:
                # Verify cohort exists
                existing = service.conn.execute(
                    "SELECT name FROM cohorts WHERE id = ?",
                    [cohort_id]
                ).fetchone()
                
                if not existing:
                    return json.dumps({"error": f"Cohort not found: {cohort_id}"})
                
                cohort_name = existing[0]
            
            # Now add entities to cohort_entities table
            entity_counts = {}
            entity_ids_added = {}
            canonical_errors = {}  # Track canonical table insert failures
            
            for entity_type, entity_list in params.entities.items():
                if not entity_list:
                    continue
                
                # Normalize entity type to plural
                entity_type_normalized = entity_type.lower()
                if not entity_type_normalized.endswith('s'):
                    entity_type_normalized += 's'
                
                added_ids = []
                canonical_failures = []  # Track canonical insert failures
                for entity in entity_list:
                    # Determine entity ID
                    entity_id = (
                        entity.get('id') or 
                        entity.get(f'{entity_type_normalized[:-1]}_id') or
                        entity.get('patient_id') or
                        entity.get('member_id') or
                        str(uuid4())
                    )
                    
                    # Store as JSON in cohort_entities
                    entity_json = json.dumps(entity, default=str)
                    
                    # Upsert: check if exists, update or insert
                    existing_entity = service.conn.execute("""
                        SELECT id FROM cohort_entities 
                        WHERE cohort_id = ? AND entity_type = ? AND entity_id = ?
                    """, [cohort_id, entity_type_normalized, entity_id]).fetchone()
                    
                    if existing_entity:
                        # Update existing
                        service.conn.execute("""
                            UPDATE cohort_entities 
                            SET entity_data = ?, created_at = ?
                            WHERE cohort_id = ? AND entity_type = ? AND entity_id = ?
                        """, [entity_json, datetime.utcnow(), cohort_id, entity_type_normalized, entity_id])
                    else:
                        # Insert new (use sequence for id like core manager does)
                        service.conn.execute("""
                            INSERT INTO cohort_entities 
                            VALUES (nextval('cohort_entities_seq'), ?, ?, ?, ?, ?)
                        """, [cohort_id, entity_type_normalized, entity_id, entity_json, datetime.utcnow()])
                    
                    # Also insert into canonical table for query consistency
                    # This ensures get_summary and direct table queries work correctly
                    success, error = insert_into_canonical_table(
                        service.conn,
                        cohort_id,
                        entity_type_normalized,
                        entity
                    )
                    if not success and len(canonical_failures) < 3:  # Limit to first 3 errors
                        canonical_failures.append({"entity_id": entity_id, "error": error})
                    
                    added_ids.append(entity_id)
                
                entity_counts[entity_type_normalized] = len(added_ids)
                entity_ids_added[entity_type_normalized] = added_ids[:5]  # Only return first 5 IDs as sample
                if canonical_failures:
                    canonical_errors[entity_type_normalized] = canonical_failures
            
            # Update cohort timestamp
            service.conn.execute("""
                UPDATE cohorts SET updated_at = ? WHERE id = ?
            """, [datetime.utcnow(), cohort_id])
            
            # Get total entity count for cohort
            total_result = service.conn.execute("""
                SELECT entity_type, COUNT(*) as count 
                FROM cohort_entities 
                WHERE cohort_id = ? 
                GROUP BY entity_type
            """, [cohort_id]).fetchall()
            
            total_by_type = {row[0]: row[1] for row in total_result}
            total_entities = sum(total_by_type.values())
        
        # Build response
        response = {
            "status": "added",
            "cohort_id": cohort_id,
            "cohort_name": cohort_name,
            "is_new_cohort": is_new_cohort,
            "entities_added_this_batch": entity_counts,
            "sample_ids": entity_ids_added,
            "cohort_totals": {
                "by_type": total_by_type,
                "total_entities": total_entities,
            },
        }
        
        # Include canonical insert errors if any occurred
        if canonical_errors:
            response["canonical_insert_errors"] = canonical_errors
            response["warning"] = "Some entities failed to insert into canonical tables. They exist in cohort_entities (JSON) but not in queryable tables."
        
        # Add batch info if provided
        if params.batch_number is not None:
            response["batch_number"] = params.batch_number
        if params.total_batches is not None:
            response["total_batches"] = params.total_batches
            if params.batch_number is not None:
                response["batches_remaining"] = params.total_batches - params.batch_number
        
        return json.dumps(response, indent=2, default=str)
        
    except Exception as e:
        return json.dumps({"error": f"Add entities failed: {str(e)}"})


@mcp.tool(
    name="healthsim_delete_cohort",
    annotations={
        "title": "Delete HealthSim Cohort",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
    }
)
def delete_cohort(params: DeleteCohortInput) -> str:
    """Delete a cohort from the database.
    
    CAUTION: This permanently removes the cohort and all linked entities.
    You must set confirm=True to actually delete.
    
    Returns:
        JSON with deletion status
    """
    if not params.confirm:
        return json.dumps({
            "error": "Must set confirm=True to delete. This action is permanent.",
            "cohort": params.name_or_id,
        })
    
    try:
        # Use write connection for the delete operation
        with _get_manager().write_manager() as manager:
            deleted = manager.delete_cohort(params.name_or_id, confirm=True)
        
        return json.dumps({
            "status": "deleted" if deleted else "not_found",
            "cohort": params.name_or_id,
        })
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": f"Delete failed: {str(e)}"})


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    if MCP_TRANSPORT == "http":
        import uvicorn
        from starlette.requests import Request
        from starlette.responses import JSONResponse

        app = mcp.streamable_http_app()

        if MCP_TOKEN:
            from starlette.middleware.base import BaseHTTPMiddleware

            class BearerAuthMiddleware(BaseHTTPMiddleware):
                async def dispatch(self, request: Request, call_next):
                    auth = request.headers.get("authorization", "")
                    if not auth.startswith("Bearer ") or auth[7:] != MCP_TOKEN:
                        return JSONResponse(
                            {"error": "Unauthorized"}, status_code=401
                        )
                    return await call_next(request)

            app.add_middleware(BearerAuthMiddleware)

        config = uvicorn.Config(app, host="0.0.0.0", port=MCP_PORT, log_level="info")
        server = uvicorn.Server(config)
        import anyio
        anyio.run(server.serve)
    else:
        mcp.run(transport="stdio")
