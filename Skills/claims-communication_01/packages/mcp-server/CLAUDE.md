# MCP Server - Claude Development Guide

## Overview

This is the HealthSim MCP (Model Context Protocol) server that provides Claude with direct access to the DuckDB database. It serves as the single connection holder, solving file locking issues.

## Key Files

```
packages/mcp-server/
├── healthsim_mcp.py      # Main MCP server implementation
├── pyproject.toml        # Package configuration
├── README.md             # Comprehensive usage documentation
└── tests/                # Server integration tests
```

## Development Patterns

### Adding New Tools

1. Define the tool in `healthsim_mcp.py`:
```python
@mcp.tool(description="Description for Claude")
async def healthsim_new_tool(param: str) -> str:
    """Implementation."""
    pass
```

2. Follow existing patterns for:
   - Error handling with clear messages
   - Connection management via `get_connection()`
   - JSON serialization for complex returns

### Testing

```bash
cd packages/mcp-server
pytest tests/ -v
```

Key test files:
- `test_canonical_e2e.py` - End-to-end cohort operations
- `test_search_providers.py` - NPPES provider search
- `test_entity_type_validation.py` - Reference vs cohort data

### Connection Management

The server maintains a single DuckDB connection:
```python
_connection: Optional[duckdb.DuckDBPyConnection] = None

def get_connection() -> duckdb.DuckDBPyConnection:
    global _connection
    if _connection is None:
        _connection = duckdb.connect(db_path, read_only=False)
    return _connection
```

## Tool Categories

### Cohort Management
- `healthsim_save_cohort` - Full cohort replacement (≤50 entities)
- `healthsim_add_entities` - Incremental upsert (recommended for large datasets)
- `healthsim_load_cohort` - Load cohort by name/ID
- `healthsim_list_cohorts` - List all cohorts
- `healthsim_delete_cohort` - Delete cohort (requires confirm=True)

### Query Tools
- `healthsim_query` - Execute read-only SQL
- `healthsim_query_reference` - Query PopulationSim reference data
- `healthsim_search_providers` - Search NPPES provider data

### Utility
- `healthsim_tables` - List database tables
- `healthsim_get_cohort_summary` - Token-efficient summaries

## Entity Type Validation

The server enforces real vs synthetic data separation:

**Cohort Data** (synthetic PHI): patients, members, claims, encounters
**Relationship Data** (links): pcp_assignments, network_contracts
**Reference Data** (query only): providers, facilities, pharmacies

See README.md for detailed validation rules.

## Integration with Core

The MCP server imports from healthsim.state:
```python
from healthsim.state import StateManager, EntityWithProvenance
```

Ensure PYTHONPATH includes the core package in Claude Desktop config.

## Debugging

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Common issues:
- Lock conflicts: Only one process can hold DuckDB connection
- Module not found: Check PYTHONPATH in MCP config
- Truncation: Use add_entities for large datasets

---

*Part of HealthSim Workspace*
