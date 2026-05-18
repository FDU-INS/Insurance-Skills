"""
Auto-persist service for HealthSim.

Implements the Structured RAG pattern:
- Summary in context (~500 tokens)
- Samples for consistency (~3000 tokens)
- Data stays in DuckDB
- Paginated queries for retrieval

This service is the primary interface for the auto-persist feature,
coordinating between auto-naming, summary generation, and database operations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import uuid4
from pathlib import Path
import re
import json

from ..db import get_connection
from .serializers import get_serializer, get_table_info, ENTITY_TABLE_MAP
from .auto_naming import generate_cohort_name, ensure_unique_name, sanitize_name
from .summary import CohortSummary, generate_summary, get_cohort_by_name


@dataclass
class PersistResult:
    """Result of a persist operation."""
    
    cohort_id: str
    cohort_name: str
    entity_type: str
    entities_persisted: int
    entity_ids: List[str]
    summary: CohortSummary
    is_new_cohort: bool
    batch_number: Optional[int] = None
    total_batches: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'cohort_id': self.cohort_id,
            'cohort_name': self.cohort_name,
            'entity_type': self.entity_type,
            'entities_persisted': self.entities_persisted,
            'entity_ids': self.entity_ids,
            'is_new_cohort': self.is_new_cohort,
            'batch_number': self.batch_number,
            'total_batches': self.total_batches,
            'summary': self.summary.to_dict(),
        }


@dataclass
class QueryResult:
    """Result of a paginated query."""
    
    results: List[Dict]
    total_count: int
    page: int
    page_size: int
    has_more: bool
    query_executed: str
    
    @property
    def offset(self) -> int:
        """Get current offset."""
        return self.page * self.page_size
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'results': self.results,
            'total_count': self.total_count,
            'page': self.page,
            'page_size': self.page_size,
            'has_more': self.has_more,
            'query_executed': self.query_executed,
        }


@dataclass
class CohortBrief:
    """Brief cohort info for listing."""
    
    cohort_id: str
    name: str
    description: Optional[str]
    entity_count: int
    created_at: datetime
    updated_at: datetime
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'cohort_id': self.cohort_id,
            'name': self.name,
            'description': self.description,
            'entity_count': self.entity_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tags': self.tags,
        }


@dataclass
class CloneResult:
    """Result of a clone operation."""
    
    source_cohort_id: str
    source_cohort_name: str
    new_cohort_id: str
    new_cohort_name: str
    entities_cloned: Dict[str, int]
    total_entities: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'source_cohort_id': self.source_cohort_id,
            'source_cohort_name': self.source_cohort_name,
            'new_cohort_id': self.new_cohort_id,
            'new_cohort_name': self.new_cohort_name,
            'entities_cloned': self.entities_cloned,
            'total_entities': self.total_entities,
        }


@dataclass
class MergeResult:
    """Result of a merge operation."""
    
    source_cohort_ids: List[str]
    source_cohort_names: List[str]
    target_cohort_id: str
    target_cohort_name: str
    entities_merged: Dict[str, int]
    total_entities: int
    conflicts_resolved: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'source_cohort_ids': self.source_cohort_ids,
            'source_cohort_names': self.source_cohort_names,
            'target_cohort_id': self.target_cohort_id,
            'target_cohort_name': self.target_cohort_name,
            'entities_merged': self.entities_merged,
            'total_entities': self.total_entities,
            'conflicts_resolved': self.conflicts_resolved,
        }


@dataclass
class ExportResult:
    """Result of an export operation."""
    
    cohort_id: str
    cohort_name: str
    format: str
    file_path: str
    entities_exported: Dict[str, int]
    total_entities: int
    file_size_bytes: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'cohort_id': self.cohort_id,
            'cohort_name': self.cohort_name,
            'format': self.format,
            'file_path': self.file_path,
            'entities_exported': self.entities_exported,
            'total_entities': self.total_entities,
            'file_size_bytes': self.file_size_bytes,
        }


# SQL patterns that are NOT allowed in queries
DISALLOWED_SQL_PATTERNS = [
    r'\bINSERT\b',
    r'\bUPDATE\b',
    r'\bDELETE\b',
    r'\bDROP\b',
    r'\bCREATE\b',
    r'\bALTER\b',
    r'\bTRUNCATE\b',
    r'\bGRANT\b',
    r'\bREVOKE\b',
    r'\bEXEC\b',
    r'\bEXECUTE\b',
    r'--',  # SQL comments
    r';.*\S',  # Multiple statements
]

# Tables that contain entity data (for cloning/merging/export)
CANONICAL_TABLES = [
    # Core
    ('persons', 'person_id'),
    ('providers', 'provider_id'),
    ('facilities', 'facility_id'),
    # PatientSim
    ('patients', 'id'),
    ('encounters', 'encounter_id'),
    ('diagnoses', 'id'),
    ('procedures', 'id'),
    ('lab_results', 'id'),
    ('medications', 'id'),
    ('allergies', 'id'),
    ('vitals', 'id'),
    # MemberSim
    ('members', 'member_id'),
    ('accumulators', 'id'),
    ('claims', 'claim_id'),
    ('claim_lines', 'id'),
    ('authorizations', 'id'),
    # RxMemberSim
    ('rx_members', 'rx_member_id'),
    ('prescriptions', 'prescription_id'),
    ('pharmacy_claims', 'pharmacy_claim_id'),
    ('dur_alerts', 'id'),
    ('pharmacies', 'pharmacy_id'),
    # TrialSim
    ('studies', 'study_id'),
    ('sites', 'site_id'),
    ('treatment_arms', 'arm_id'),
    ('subjects', 'subject_id'),
    ('adverse_events', 'ae_id'),
    ('visit_schedule', 'scheduled_visit_id'),
    ('actual_visits', 'actual_visit_id'),
    ('disposition_events', 'disposition_id'),
    # PopulationSim
    ('geographic_entities', 'geo_id'),
    ('population_profiles', 'profile_id'),
    ('health_indicators', 'indicator_id'),
    ('sdoh_indices', 'sdoh_id'),
    ('cohort_specifications', 'cohort_id'),
    # NetworkSim
    ('networks', 'network_id'),
    ('network_providers', 'network_provider_id'),
    ('network_facilities', 'network_facility_id'),
    ('provider_specialties', 'specialty_id'),
]


def _validate_query(query: str) -> bool:
    """
    Validate that a query is SELECT-only.
    
    Args:
        query: SQL query string
        
    Returns:
        True if query is safe, False otherwise
        
    Raises:
        ValueError: If query contains disallowed patterns
    """
    query_upper = query.upper().strip()
    
    # Must start with SELECT or WITH (for CTEs)
    if not (query_upper.startswith('SELECT') or query_upper.startswith('WITH')):
        raise ValueError("Query must be a SELECT statement")
    
    # Check for disallowed patterns
    for pattern in DISALLOWED_SQL_PATTERNS:
        if re.search(pattern, query, re.IGNORECASE):
            raise ValueError(f"Query contains disallowed pattern: {pattern}")
    
    return True


class AutoPersistService:
    """
    Service for auto-persisting generated entities.
    
    Implements the core Structured RAG pattern:
    1. Persist entities to DuckDB immediately after generation
    2. Return summary (not full data) to context
    3. Provide paginated queries for data retrieval
    
    Also provides:
    - Tag management for cohort organization
    - Scenario cloning for creating variations
    - Scenario merging for combining datasets
    - Export utilities for data portability
    
    Usage:
        service = get_auto_persist_service()
        
        # Persist entities
        result = service.persist_entities(
            entities=[...],
            entity_type='patient',
            context_keywords=['diabetes', 'elderly']
        )
        
        # Query data
        query_result = service.query_cohort(
            cohort_id=result.cohort_id,
            query="SELECT * FROM patients WHERE gender = 'F'"
        )
        
        # Tag management
        service.add_tag(cohort_id, 'training')
        service.remove_tag(cohort_id, 'draft')
        
        # Clone cohort
        clone = service.clone_cohort(cohort_id, 'new-name')
        
        # Export
        export = service.export_cohort(cohort_id, format='json')
    """
    
    def __init__(self, connection=None):
        """
        Initialize the service.
        
        Args:
            connection: Optional DuckDB connection (uses default if not provided)
        """
        self._conn = connection
    
    @property
    def conn(self):
        """Get database connection."""
        if self._conn is None:
            self._conn = get_connection()
        return self._conn
    
    # ========================================================================
    # Core Scenario Management
    # ========================================================================
    
    def _create_cohort(
        self,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        Create a new cohort.
        
        Args:
            name: Scenario name
            description: Optional description
            tags: Optional list of tags
            
        Returns:
            New cohort ID
        """
        cohort_id = str(uuid4())
        now = datetime.utcnow()
        
        self.conn.execute("""
            INSERT INTO cohorts (id, name, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, [cohort_id, name, description, now, now])
        
        # Add tags
        if tags:
            for tag in tags:
                self.conn.execute("""
                    INSERT INTO cohort_tags (id, cohort_id, tag)
                    VALUES (nextval('cohort_tags_seq'), ?, ?)
                """, [cohort_id, tag.lower()])
        
        return cohort_id
    
    def _update_cohort_timestamp(self, cohort_id: str):
        """Update cohort's updated_at timestamp."""
        self.conn.execute("""
            UPDATE cohorts SET updated_at = ? WHERE id = ?
        """, [datetime.utcnow(), cohort_id])
    
    def _get_cohort_info(self, cohort_id: str) -> Optional[Dict[str, Any]]:
        """Get cohort metadata."""
        result = self.conn.execute("""
            SELECT id, name, description, created_at, updated_at
            FROM cohorts WHERE id = ?
        """, [cohort_id]).fetchone()
        
        if not result:
            return None
        
        return {
            'cohort_id': result[0],
            'name': result[1],
            'description': result[2],
            'created_at': result[3],
            'updated_at': result[4],
        }
    
    def _table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        try:
            result = self.conn.execute("""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_name = ?
            """, [table_name]).fetchone()
            return result[0] > 0
        except Exception:
            return False
    
    def persist_entities(
        self,
        entities: List[Dict],
        entity_type: str,
        cohort_id: Optional[str] = None,
        cohort_name: Optional[str] = None,
        cohort_description: Optional[str] = None,
        context_keywords: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        batch_number: Optional[int] = None,
        total_batches: Optional[int] = None,
    ) -> PersistResult:
        """
        Persist entities to DuckDB and return summary.
        
        If no cohort_id provided:
        - Creates new cohort with auto-generated name
        - Uses context_keywords for naming if available
        
        Args:
            entities: List of entity dictionaries to persist
            entity_type: Type of entities (patient, claim, etc.)
            cohort_id: Existing cohort ID to add to (optional)
            cohort_name: Name for new cohort (optional, auto-generated if not provided)
            cohort_description: Description for cohort (optional)
            context_keywords: Keywords from generation context for auto-naming
            tags: Tags for the cohort
            batch_number: Current batch number (for progress tracking)
            total_batches: Total number of batches (for progress tracking)
            
        Returns:
            PersistResult with summary (NOT full entity data)
        """
        if not entities:
            raise ValueError("No entities to persist")
        
        # Normalize entity type
        entity_type = entity_type.lower().rstrip('s') + 's'  # Ensure plural
        
        # Get table info
        table_info = get_table_info(entity_type)
        if not table_info:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        table_name, id_column = table_info
        
        # Get serializer
        serializer = get_serializer(entity_type)
        
        # Create or use existing cohort
        is_new_cohort = False
        if not cohort_id:
            is_new_cohort = True
            
            # Generate name if not provided
            if not cohort_name:
                cohort_name = generate_cohort_name(
                    keywords=context_keywords,
                    entity_type=entity_type,
                    connection=self.conn,
                )
            else:
                cohort_name = ensure_unique_name(
                    sanitize_name(cohort_name),
                    connection=self.conn,
                )
            
            cohort_id = self._create_cohort(
                name=cohort_name,
                description=cohort_description,
                tags=tags,
            )
        else:
            # Get existing cohort name
            result = self.conn.execute("""
                SELECT name FROM cohorts WHERE id = ?
            """, [cohort_id]).fetchone()
            
            if not result:
                raise ValueError(f"Cohort not found: {cohort_id}")
            
            cohort_name = result[0]
        
        # Persist entities
        entity_ids = []
        
        for entity in entities:
            # Serialize entity
            if serializer:
                serialized = serializer(entity)
            else:
                serialized = entity.copy()
            
            # Add cohort_id (database column)
            serialized['cohort_id'] = cohort_id
            
            # Get or generate entity ID
            entity_id = serialized.get(id_column) or str(uuid4())
            serialized[id_column] = entity_id
            entity_ids.append(entity_id)
            
            # Build insert statement
            columns = list(serialized.keys())
            placeholders = ', '.join(['?' for _ in columns])
            column_str = ', '.join(columns)
            
            try:
                self.conn.execute(f"""
                    INSERT INTO {table_name} ({column_str})
                    VALUES ({placeholders})
                """, list(serialized.values()))
            except Exception as e:
                # Handle duplicate key by updating
                if 'duplicate' in str(e).lower() or 'unique' in str(e).lower():
                    # Update existing record
                    set_clause = ', '.join([f"{col} = ?" for col in columns if col != id_column])
                    values = [v for k, v in serialized.items() if k != id_column]
                    values.append(entity_id)
                    
                    self.conn.execute(f"""
                        UPDATE {table_name}
                        SET {set_clause}
                        WHERE {id_column} = ?
                    """, values)
                else:
                    raise
        
        # Update cohort timestamp
        self._update_cohort_timestamp(cohort_id)
        
        # Generate summary
        summary = generate_summary(
            cohort_id=cohort_id,
            include_samples=True,
            samples_per_type=3,
            connection=self.conn,
        )
        
        return PersistResult(
            cohort_id=cohort_id,
            cohort_name=cohort_name,
            entity_type=entity_type,
            entities_persisted=len(entities),
            entity_ids=entity_ids,
            summary=summary,
            is_new_cohort=is_new_cohort,
            batch_number=batch_number,
            total_batches=total_batches,
        )
    
    def get_cohort_summary(
        self,
        cohort_id: Optional[str] = None,
        cohort_name: Optional[str] = None,
        include_samples: bool = True,
        samples_per_type: int = 3,
    ) -> CohortSummary:
        """
        Get cohort summary for loading into context.
        
        IMPORTANT: Never loads full entity data!
        Returns summary (~500 tokens) + samples (~3000 tokens)
        
        Args:
            cohort_id: Scenario UUID (optional if name provided)
            cohort_name: Scenario name for fuzzy lookup (optional if ID provided)
            include_samples: Whether to include sample entities
            samples_per_type: Number of samples per entity type
            
        Returns:
            CohortSummary with counts, statistics, and samples
        """
        # Resolve cohort ID
        if not cohort_id:
            if not cohort_name:
                raise ValueError("Either cohort_id or cohort_name required")
            
            cohort_id = get_cohort_by_name(cohort_name, self.conn)
            if not cohort_id:
                raise ValueError(f"Cohort not found: {cohort_name}")
        
        return generate_summary(
            cohort_id=cohort_id,
            include_samples=include_samples,
            samples_per_type=samples_per_type,
            connection=self.conn,
        )
    
    def query_cohort(
        self,
        cohort_id: str,
        query: str,
        limit: int = 20,
        offset: int = 0,
    ) -> QueryResult:
        """
        Execute paginated query against cohort data.
        
        Args:
            cohort_id: Scenario to query
            query: SQL SELECT query
            limit: Results per page (default 20, max 100)
            offset: Starting offset
            
        Returns:
            QueryResult with paginated results
            
        Raises:
            ValueError: If query is not SELECT-only
        """
        # Validate query
        _validate_query(query)
        
        # Enforce limits
        limit = min(limit, 100)
        
        # Modify query to add pagination and cohort filter
        # This is a simplified approach - assumes query doesn't already have LIMIT
        query_lower = query.lower().strip()
        
        # Add cohort_id filter if not already present
        if 'cohort_id' not in query_lower:
            # Find WHERE clause or add one
            if ' where ' in query_lower:
                # Add to existing WHERE
                where_idx = query_lower.index(' where ') + 7
                query = query[:where_idx] + f"cohort_id = '{cohort_id}' AND " + query[where_idx:]
            else:
                # Find FROM clause and add WHERE after table name
                # This is simplified - proper SQL parsing would be more robust
                from_match = re.search(r'\bFROM\s+(\w+)', query, re.IGNORECASE)
                if from_match:
                    table_end = from_match.end()
                    query = query[:table_end] + f" WHERE cohort_id = '{cohort_id}'" + query[table_end:]
        
        # Remove any existing LIMIT/OFFSET
        query = re.sub(r'\bLIMIT\s+\d+', '', query, flags=re.IGNORECASE)
        query = re.sub(r'\bOFFSET\s+\d+', '', query, flags=re.IGNORECASE)
        
        # Get total count first
        count_query = f"SELECT COUNT(*) FROM ({query}) AS subquery"
        try:
            total_count = self.conn.execute(count_query).fetchone()[0]
        except Exception:
            total_count = 0
        
        # Add pagination
        paginated_query = f"{query} LIMIT {limit} OFFSET {offset}"
        
        # Execute query
        try:
            result = self.conn.execute(paginated_query)
            columns = [desc[0] for desc in result.description]
            rows = result.fetchall()
            
            results = []
            for row in rows:
                row_dict = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    # Convert special types
                    if isinstance(value, (datetime,)):
                        value = value.isoformat()
                    row_dict[col] = value
                results.append(row_dict)
        except Exception as e:
            raise ValueError(f"Query error: {str(e)}")
        
        page = offset // limit if limit > 0 else 0
        has_more = (offset + len(results)) < total_count
        
        return QueryResult(
            results=results,
            total_count=total_count,
            page=page,
            page_size=limit,
            has_more=has_more,
            query_executed=paginated_query,
        )
    
    def list_cohorts(
        self,
        filter_pattern: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 20,
        sort_by: str = "updated_at",
    ) -> List[CohortBrief]:
        """
        List available cohorts with brief stats.
        
        Args:
            filter_pattern: Filter by name pattern (case-insensitive)
            tag: Filter by tag
            limit: Maximum results
            sort_by: Sort field (updated_at, created_at, name)
            
        Returns:
            List of CohortBrief objects
        """
        # Build query
        query = """
            SELECT 
                s.id,
                s.name,
                s.description,
                s.created_at,
                s.updated_at
            FROM cohorts s
        """
        
        params = []
        conditions = []
        
        if filter_pattern:
            conditions.append("LOWER(s.name) LIKE LOWER(?)")
            params.append(f"%{filter_pattern}%")
        
        if tag:
            query += " JOIN cohort_tags t ON s.id = t.cohort_id"
            conditions.append("LOWER(t.tag) = LOWER(?)")
            params.append(tag)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Sort
        sort_map = {
            'updated_at': 's.updated_at DESC',
            'created_at': 's.created_at DESC',
            'name': 's.name ASC',
        }
        query += f" ORDER BY {sort_map.get(sort_by, 's.updated_at DESC')}"
        query += f" LIMIT {limit}"
        
        result = self.conn.execute(query, params).fetchall()
        
        cohorts = []
        for row in result:
            cohort_id = str(row[0])
            
            # Get entity count
            count = 0
            for table in ['patients', 'members', 'subjects', 'claims', 'prescriptions']:
                try:
                    cnt_result = self.conn.execute(f"""
                        SELECT COUNT(*) FROM {table} WHERE cohort_id = ?
                    """, [cohort_id]).fetchone()
                    count += cnt_result[0] if cnt_result else 0
                except Exception:
                    pass
            
            # Get tags
            tags_result = self.conn.execute("""
                SELECT tag FROM cohort_tags WHERE cohort_id = ?
            """, [cohort_id]).fetchall()
            tags = [t[0] for t in tags_result]
            
            cohorts.append(CohortBrief(
                cohort_id=cohort_id,
                name=row[1],
                description=row[2],
                entity_count=count,
                created_at=row[3],
                updated_at=row[4],
                tags=tags,
            ))
        
        return cohorts
    
    def rename_cohort(
        self,
        cohort_id: str,
        new_name: str,
    ) -> Tuple[str, str]:
        """
        Rename a cohort.
        
        Args:
            cohort_id: Cohort to rename
            new_name: New name for the cohort
            
        Returns:
            Tuple of (old_name, new_name)
            
        Raises:
            ValueError: If cohort not found or name already exists
        """
        # Get current name
        result = self.conn.execute("""
            SELECT name FROM cohorts WHERE id = ?
        """, [cohort_id]).fetchone()
        
        if not result:
            raise ValueError(f"Cohort not found: {cohort_id}")
        
        old_name = result[0]
        
        # Sanitize and ensure unique
        new_name = sanitize_name(new_name)
        new_name = ensure_unique_name(new_name, self.conn)
        
        # Update
        self.conn.execute("""
            UPDATE cohorts SET name = ?, updated_at = ?
            WHERE id = ?
        """, [new_name, datetime.utcnow(), cohort_id])
        
        return (old_name, new_name)
    
    def delete_cohort(
        self,
        cohort_id: str,
        confirm: bool = False,
    ) -> Dict[str, Any]:
        """
        Delete cohort and all linked entities.
        
        Args:
            cohort_id: Scenario to delete
            confirm: Must be True to proceed with deletion
            
        Returns:
            Dict with deleted cohort info
            
        Raises:
            ValueError: If confirm is not True or cohort not found
        """
        if not confirm:
            raise ValueError("Deletion requires confirm=True")
        
        # Get cohort info
        result = self.conn.execute("""
            SELECT name, description FROM cohorts WHERE id = ?
        """, [cohort_id]).fetchone()
        
        if not result:
            raise ValueError(f"Cohort not found: {cohort_id}")
        
        name = result[0]
        description = result[1]
        
        # Count entities before deletion
        entity_count = 0
        for table_name, _ in CANONICAL_TABLES:
            if self._table_exists(table_name):
                try:
                    cnt = self.conn.execute(f"""
                        SELECT COUNT(*) FROM {table_name} WHERE cohort_id = ?
                    """, [cohort_id]).fetchone()
                    entity_count += cnt[0] if cnt else 0
                except Exception:
                    pass
        
        # Delete entities from all tables
        for table_name, _ in CANONICAL_TABLES:
            if self._table_exists(table_name):
                try:
                    self.conn.execute(f"""
                        DELETE FROM {table_name} WHERE cohort_id = ?
                    """, [cohort_id])
                except Exception:
                    pass
        
        # Delete tags
        self.conn.execute("""
            DELETE FROM cohort_tags WHERE cohort_id = ?
        """, [cohort_id])
        
        # Delete cohort
        self.conn.execute("""
            DELETE FROM cohorts WHERE id = ?
        """, [cohort_id])
        
        return {
            'cohort_id': cohort_id,
            'name': name,
            'description': description,
            'entity_count': entity_count,
        }
    
    def get_entity_samples(
        self,
        cohort_id: str,
        entity_type: str,
        count: int = 3,
        strategy: str = "diverse",
    ) -> List[Dict]:
        """
        Get sample entities for pattern consistency.
        
        Args:
            cohort_id: Scenario to get samples from
            entity_type: Type of entities to sample
            count: Number of samples (default 3)
            strategy: Sampling strategy
                - "diverse": Maximize variety (default)
                - "random": Random selection
                - "recent": Most recently added
                
        Returns:
            List of sample entity dictionaries
        """
        # Normalize entity type
        entity_type = entity_type.lower()
        if not entity_type.endswith('s'):
            entity_type = entity_type + 's'
        
        # Get table info
        table_info = get_table_info(entity_type)
        if not table_info:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        table_name, id_column = table_info
        
        # Build query based on strategy
        if strategy == "random":
            order_clause = "ORDER BY RANDOM()"
        elif strategy == "recent":
            order_clause = "ORDER BY created_at DESC"
        else:  # diverse - sample evenly across the dataset
            order_clause = "ORDER BY created_at"
        
        # Get samples
        try:
            result = self.conn.execute(f"""
                SELECT * FROM {table_name}
                WHERE cohort_id = ?
                {order_clause}
            """, [cohort_id]).fetchall()
            
            columns = [desc[0] for desc in self.conn.execute(
                f"SELECT * FROM {table_name} LIMIT 1"
            ).description]
        except Exception as e:
            raise ValueError(f"Error fetching samples: {str(e)}")
        
        if not result:
            return []
        
        # For diverse sampling, take evenly spaced samples
        if strategy == "diverse" and len(result) > count:
            step = len(result) / count
            indices = [int(i * step) for i in range(count)]
            selected = [result[i] for i in indices]
        else:
            selected = result[:count]
        
        # Convert to dicts
        samples = []
        for row in selected:
            sample = {}
            for i, col in enumerate(columns):
                value = row[i]
                if isinstance(value, datetime):
                    value = value.isoformat()
                # Skip internal columns
                if col not in ('cohort_id', 'generation_seed'):
                    sample[col] = value
            samples.append(sample)
        
        return samples
    
    # ========================================================================
    # Tag Management (Phase 2)
    # ========================================================================
    
    def add_tag(self, cohort_id: str, tag: str) -> List[str]:
        """
        Add a tag to a cohort.
        
        Args:
            cohort_id: Scenario to tag
            tag: Tag to add (case-insensitive, stored lowercase)
            
        Returns:
            List of all tags on the cohort
            
        Raises:
            ValueError: If cohort not found
        """
        # Verify cohort exists
        if not self._get_cohort_info(cohort_id):
            raise ValueError(f"Cohort not found: {cohort_id}")
        
        tag = tag.lower().strip()
        if not tag:
            raise ValueError("Tag cannot be empty")
        
        # Check if tag already exists
        existing = self.conn.execute("""
            SELECT COUNT(*) FROM cohort_tags
            WHERE cohort_id = ? AND tag = ?
        """, [cohort_id, tag]).fetchone()[0]
        
        if existing == 0:
            self.conn.execute("""
                INSERT INTO cohort_tags (cohort_id, tag)
                VALUES (?, ?)
            """, [cohort_id, tag])
            self._update_cohort_timestamp(cohort_id)
        
        return self.get_tags(cohort_id)
    
    def remove_tag(self, cohort_id: str, tag: str) -> List[str]:
        """
        Remove a tag from a cohort.
        
        Args:
            cohort_id: Scenario to modify
            tag: Tag to remove (case-insensitive)
            
        Returns:
            List of remaining tags on the cohort
            
        Raises:
            ValueError: If cohort not found
        """
        # Verify cohort exists
        if not self._get_cohort_info(cohort_id):
            raise ValueError(f"Cohort not found: {cohort_id}")
        
        tag = tag.lower().strip()
        
        self.conn.execute("""
            DELETE FROM cohort_tags
            WHERE cohort_id = ? AND tag = ?
        """, [cohort_id, tag])
        
        self._update_cohort_timestamp(cohort_id)
        
        return self.get_tags(cohort_id)
    
    def get_tags(self, cohort_id: str) -> List[str]:
        """
        Get all tags for a cohort.
        
        Args:
            cohort_id: Scenario to get tags for
            
        Returns:
            List of tags (sorted alphabetically)
        """
        result = self.conn.execute("""
            SELECT tag FROM cohort_tags
            WHERE cohort_id = ?
            ORDER BY tag
        """, [cohort_id]).fetchall()
        
        return [row[0] for row in result]
    
    def list_all_tags(self) -> List[Dict[str, Any]]:
        """
        List all tags in use with counts.
        
        Returns:
            List of dicts with 'tag' and 'count' keys, sorted by count desc
        """
        result = self.conn.execute("""
            SELECT tag, COUNT(*) as count
            FROM cohort_tags
            GROUP BY tag
            ORDER BY count DESC, tag ASC
        """).fetchall()
        
        return [{'tag': row[0], 'count': row[1]} for row in result]
    
    def cohorts_by_tag(self, tag: str) -> List[CohortBrief]:
        """
        Get all cohorts with a specific tag.
        
        Args:
            tag: Tag to filter by (case-insensitive)
            
        Returns:
            List of CohortBrief objects
        """
        return self.list_cohorts(tag=tag, limit=100)
    
    # ========================================================================
    # Scenario Cloning (Phase 2)
    # ========================================================================
    
    def clone_cohort(
        self,
        source_cohort_id: str,
        new_name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        include_entity_types: Optional[List[str]] = None,
    ) -> CloneResult:
        """
        Clone a cohort with all its entities.
        
        Creates an exact copy of the cohort with a new ID and name.
        All entity IDs are regenerated to ensure uniqueness.
        
        Args:
            source_cohort_id: Scenario to clone
            new_name: Name for the new cohort (auto-generated if not provided)
            description: Description for cohort (copied from source if not provided)
            tags: Tags for new cohort (copied from source if not provided)
            include_entity_types: Optional list of entity types to include
                                  (all types if not specified)
            
        Returns:
            CloneResult with clone details
            
        Raises:
            ValueError: If source cohort not found
        """
        # Get source cohort info
        source_info = self._get_cohort_info(source_cohort_id)
        if not source_info:
            raise ValueError(f"Source cohort not found: {source_cohort_id}")
        
        source_name = source_info['name']
        
        # Generate new name if not provided
        if not new_name:
            new_name = f"{source_name}-copy"
        new_name = ensure_unique_name(sanitize_name(new_name), self.conn)
        
        # Use source description if not provided
        if description is None:
            description = source_info.get('description') or f"Clone of {source_name}"
        
        # Get source tags if not provided
        if tags is None:
            tags = self.get_tags(source_cohort_id)
        
        # Create new cohort
        new_cohort_id = self._create_cohort(
            name=new_name,
            description=description,
            tags=tags,
        )
        
        # Clone entities from each table
        entities_cloned = {}
        total_entities = 0
        
        for table_name, id_column in CANONICAL_TABLES:
            if not self._table_exists(table_name):
                continue
            
            # Check if we should include this entity type
            entity_type = table_name.rstrip('s')
            if include_entity_types and entity_type not in include_entity_types and table_name not in include_entity_types:
                continue
            
            try:
                # Get all columns
                sample = self.conn.execute(f"SELECT * FROM {table_name} LIMIT 1")
                columns = [desc[0] for desc in sample.description]
                
                # Get source entities
                source_entities = self.conn.execute(f"""
                    SELECT * FROM {table_name}
                    WHERE cohort_id = ?
                """, [source_cohort_id]).fetchall()
                
                if not source_entities:
                    continue
                
                # Clone each entity with new IDs
                cloned_count = 0
                for row in source_entities:
                    row_dict = dict(zip(columns, row))
                    
                    # Generate new IDs
                    row_dict['cohort_id'] = new_cohort_id
                    row_dict[id_column] = str(uuid4())
                    
                    # Reset timestamps
                    if 'created_at' in row_dict:
                        row_dict['created_at'] = datetime.utcnow()
                    
                    # Insert cloned entity
                    cols = list(row_dict.keys())
                    placeholders = ', '.join(['?' for _ in cols])
                    col_str = ', '.join(cols)
                    
                    self.conn.execute(f"""
                        INSERT INTO {table_name} ({col_str})
                        VALUES ({placeholders})
                    """, list(row_dict.values()))
                    
                    cloned_count += 1
                
                if cloned_count > 0:
                    entities_cloned[table_name] = cloned_count
                    total_entities += cloned_count
                    
            except Exception as e:
                # Log but continue with other tables
                continue
        
        self._update_cohort_timestamp(new_cohort_id)
        
        return CloneResult(
            source_cohort_id=source_cohort_id,
            source_cohort_name=source_name,
            new_cohort_id=new_cohort_id,
            new_cohort_name=new_name,
            entities_cloned=entities_cloned,
            total_entities=total_entities,
        )
    
    # ========================================================================
    # Scenario Merging (Phase 2)
    # ========================================================================
    
    def merge_cohorts(
        self,
        source_cohort_ids: List[str],
        target_name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        conflict_strategy: str = "skip",
    ) -> MergeResult:
        """
        Merge multiple cohorts into a new cohort.
        
        Creates a new cohort containing entities from all source cohorts.
        Entity IDs are regenerated to avoid conflicts.
        
        Args:
            source_cohort_ids: List of cohort IDs to merge
            target_name: Name for the merged cohort (auto-generated if not provided)
            description: Description for merged cohort
            tags: Tags for merged cohort (union of source tags if not provided)
            conflict_strategy: How to handle duplicate entities
                - "skip": Skip duplicates (default)
                - "overwrite": Later sources overwrite earlier
                - "rename": Rename conflicting entities
                
        Returns:
            MergeResult with merge details
            
        Raises:
            ValueError: If any source cohort not found or less than 2 sources
        """
        if len(source_cohort_ids) < 2:
            raise ValueError("At least 2 source cohorts required for merge")
        
        # Validate all source cohorts exist
        source_names = []
        all_tags = set()
        
        for sid in source_cohort_ids:
            info = self._get_cohort_info(sid)
            if not info:
                raise ValueError(f"Source cohort not found: {sid}")
            source_names.append(info['name'])
            all_tags.update(self.get_tags(sid))
        
        # Generate target name if not provided
        if not target_name:
            target_name = f"merged-{datetime.utcnow().strftime('%Y%m%d')}"
        target_name = ensure_unique_name(sanitize_name(target_name), self.conn)
        
        # Use union of tags if not provided
        if tags is None:
            tags = list(all_tags)
        
        # Set description
        if description is None:
            description = f"Merged from: {', '.join(source_names)}"
        
        # Create target cohort
        target_cohort_id = self._create_cohort(
            name=target_name,
            description=description,
            tags=tags,
        )
        
        # Merge entities from each source
        entities_merged = {}
        total_entities = 0
        conflicts_resolved = 0
        seen_ids = {}  # Track seen IDs per table for conflict detection
        
        for source_id in source_cohort_ids:
            for table_name, id_column in CANONICAL_TABLES:
                if not self._table_exists(table_name):
                    continue
                
                try:
                    # Get all columns
                    sample = self.conn.execute(f"SELECT * FROM {table_name} LIMIT 1")
                    columns = [desc[0] for desc in sample.description]
                    
                    # Get source entities
                    source_entities = self.conn.execute(f"""
                        SELECT * FROM {table_name}
                        WHERE cohort_id = ?
                    """, [source_id]).fetchall()
                    
                    if not source_entities:
                        continue
                    
                    if table_name not in seen_ids:
                        seen_ids[table_name] = set()
                    
                    for row in source_entities:
                        row_dict = dict(zip(columns, row))
                        original_id = row_dict[id_column]
                        
                        # Check for conflicts based on business key
                        # For simplicity, we use the original ID as the conflict key
                        if original_id in seen_ids[table_name]:
                            conflicts_resolved += 1
                            if conflict_strategy == "skip":
                                continue
                            # For "overwrite" and "rename", we proceed with new ID
                        
                        seen_ids[table_name].add(original_id)
                        
                        # Generate new IDs
                        row_dict['cohort_id'] = target_cohort_id
                        row_dict[id_column] = str(uuid4())
                        
                        # Reset timestamps
                        if 'created_at' in row_dict:
                            row_dict['created_at'] = datetime.utcnow()
                        
                        # Insert merged entity
                        cols = list(row_dict.keys())
                        placeholders = ', '.join(['?' for _ in cols])
                        col_str = ', '.join(cols)
                        
                        self.conn.execute(f"""
                            INSERT INTO {table_name} ({col_str})
                            VALUES ({placeholders})
                        """, list(row_dict.values()))
                        
                        if table_name not in entities_merged:
                            entities_merged[table_name] = 0
                        entities_merged[table_name] += 1
                        total_entities += 1
                        
                except Exception:
                    continue
        
        self._update_cohort_timestamp(target_cohort_id)
        
        return MergeResult(
            source_cohort_ids=source_cohort_ids,
            source_cohort_names=source_names,
            target_cohort_id=target_cohort_id,
            target_cohort_name=target_name,
            entities_merged=entities_merged,
            total_entities=total_entities,
            conflicts_resolved=conflicts_resolved,
        )
    
    # ========================================================================
    # Export Utilities (Phase 2)
    # ========================================================================
    
    def export_cohort(
        self,
        cohort_id: str,
        format: str = "json",
        output_path: Optional[str] = None,
        include_entity_types: Optional[List[str]] = None,
        include_provenance: bool = True,
    ) -> ExportResult:
        """
        Export a cohort to a file.
        
        Args:
            cohort_id: Scenario to export
            format: Export format ("json", "csv", "parquet")
            output_path: Path to save the export (defaults to ~/Downloads)
            include_entity_types: Optional list of entity types to include
            include_provenance: Whether to include provenance columns
            
        Returns:
            ExportResult with export details
            
        Raises:
            ValueError: If cohort not found or unsupported format
        """
        # Validate format
        format = format.lower()
        if format not in ('json', 'csv', 'parquet'):
            raise ValueError(f"Unsupported export format: {format}")
        
        # Get cohort info
        info = self._get_cohort_info(cohort_id)
        if not info:
            raise ValueError(f"Cohort not found: {cohort_id}")
        
        cohort_name = info['name']
        
        # Set output path
        if not output_path:
            downloads_dir = Path.home() / "Downloads"
            downloads_dir.mkdir(exist_ok=True)
            output_path = str(downloads_dir / f"{cohort_name}.{format}")
        else:
            # If output_path is a directory, create filename within it
            output_path_obj = Path(output_path)
            if output_path_obj.is_dir():
                output_path = str(output_path_obj / f"{cohort_name}.{format}")
        
        # Columns to exclude if not including provenance
        provenance_columns = {
            'source_type', 'source_system', 'skill_used',
            'generation_seed', 'cohort_id'
        }
        
        # Collect all entity data
        entities_exported = {}
        all_data = {}
        total_entities = 0
        
        for table_name, id_column in CANONICAL_TABLES:
            if not self._table_exists(table_name):
                continue
            
            # Check if we should include this entity type
            entity_type = table_name.rstrip('s')
            if include_entity_types and entity_type not in include_entity_types and table_name not in include_entity_types:
                continue
            
            try:
                result = self.conn.execute(f"""
                    SELECT * FROM {table_name}
                    WHERE cohort_id = ?
                """, [cohort_id])
                
                columns = [desc[0] for desc in result.description]
                rows = result.fetchall()
                
                if not rows:
                    continue
                
                # Filter columns if not including provenance
                if not include_provenance:
                    filtered_indices = [
                        i for i, col in enumerate(columns)
                        if col not in provenance_columns
                    ]
                    columns = [columns[i] for i in filtered_indices]
                    rows = [[row[i] for i in filtered_indices] for row in rows]
                
                # Convert rows to dicts
                data = []
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        value = row[i]
                        if isinstance(value, datetime):
                            value = value.isoformat()
                        row_dict[col] = value
                    data.append(row_dict)
                
                all_data[table_name] = data
                entities_exported[table_name] = len(data)
                total_entities += len(data)
                
            except Exception:
                continue
        
        # Write to file based on format
        if format == 'json':
            export_obj = {
                'cohort_id': cohort_id,
                'cohort_name': cohort_name,
                'description': info.get('description'),
                'tags': self.get_tags(cohort_id),
                'exported_at': datetime.utcnow().isoformat(),
                'entities': all_data,
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_obj, f, indent=2, default=str)
        
        elif format == 'csv':
            import csv
            
            # For CSV, create a directory with separate files per entity type
            output_dir = Path(output_path).with_suffix('')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for table_name, data in all_data.items():
                if not data:
                    continue
                
                csv_path = output_dir / f"{table_name}.csv"
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            
            # Update output_path to directory
            output_path = str(output_dir)
        
        elif format == 'parquet':
            try:
                import pyarrow as pa
                import pyarrow.parquet as pq
                
                # Create a directory with separate files per entity type
                output_dir = Path(output_path).with_suffix('')
                output_dir.mkdir(parents=True, exist_ok=True)
                
                for table_name, data in all_data.items():
                    if not data:
                        continue
                    
                    parquet_path = output_dir / f"{table_name}.parquet"
                    table = pa.Table.from_pylist(data)
                    pq.write_table(table, str(parquet_path))
                
                output_path = str(output_dir)
                
            except ImportError:
                raise ValueError("Parquet export requires pyarrow: pip install pyarrow")
        
        # Calculate file size
        output_path_obj = Path(output_path)
        if output_path_obj.is_dir():
            file_size = sum(f.stat().st_size for f in output_path_obj.rglob('*') if f.is_file())
        else:
            file_size = output_path_obj.stat().st_size
        
        return ExportResult(
            cohort_id=cohort_id,
            cohort_name=cohort_name,
            format=format,
            file_path=output_path,
            entities_exported=entities_exported,
            total_entities=total_entities,
            file_size_bytes=file_size,
        )
    
    def export_to_csv(
        self,
        cohort_id: str,
        output_path: Optional[str] = None,
    ) -> ExportResult:
        """Convenience method for CSV export."""
        return self.export_cohort(cohort_id, format='csv', output_path=output_path)
    
    def export_to_json(
        self,
        cohort_id: str,
        output_path: Optional[str] = None,
    ) -> ExportResult:
        """Convenience method for JSON export."""
        return self.export_cohort(cohort_id, format='json', output_path=output_path)
    
    def export_to_parquet(
        self,
        cohort_id: str,
        output_path: Optional[str] = None,
    ) -> ExportResult:
        """Convenience method for Parquet export."""
        return self.export_cohort(cohort_id, format='parquet', output_path=output_path)


# Module-level singleton
_service: Optional[AutoPersistService] = None


def get_auto_persist_service(connection=None) -> AutoPersistService:
    """
    Get singleton service instance.
    
    Args:
        connection: Optional DuckDB connection
        
    Returns:
        AutoPersistService instance
    """
    global _service
    if _service is None or connection is not None:
        _service = AutoPersistService(connection)
    return _service


def reset_service():
    """Reset the singleton service (for testing)."""
    global _service
    _service = None
