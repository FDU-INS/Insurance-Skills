# p1-03: Switch MCP Server to MotherDuck

## What to build

Verify that the MCP server works correctly when connected to MotherDuck (via the updated connection manager from p1-02). Test all 11 tools against MotherDuck data.

## Context

After p1-02, the connection manager supports both local DuckDB and MotherDuck. The MCP server imports from this module, so it should automatically connect to MotherDuck when `MOTHERDUCK_TOKEN` is set. This prompt validates that all tools work correctly against the cloud data.

## Tasks

1. **Start the MCP server in HTTP mode pointed at MotherDuck**:
   ```bash
   export MCP_TRANSPORT=http
   export MCP_PORT=8001
   export MOTHERDUCK_TOKEN=<your-token>
   .venv/bin/python packages/mcp-server/healthsim_mcp.py
   ```

2. **Test each of the 11 MCP tools** by calling them via HTTP. For each tool, verify it returns correct data from MotherDuck. Create a test script `scripts/test_mcp_motherduck.py` that:
   - Connects to the local HTTP server
   - Calls each tool with a simple test input
   - Prints pass/fail for each

   Key tools to verify:
   - `healthsim_query_reference` — queries reference data from MotherDuck
   - `healthsim_search_providers` — searches NPPES in MotherDuck
   - `healthsim_list_cohorts` — reads from cohort schema (may be empty, that's fine)
   - `healthsim_tables` — lists available tables
   - `healthsim_add_entities` — writes to cohort schema in MotherDuck (tests write path)
   - `healthsim_get_cohort_summary` — reads cohort data

3. **Check for schema or table name mismatches** between what the MCP server expects and what exists in MotherDuck. The migration script may have created tables with slightly different names or schemas. Fix any mismatches.

4. **Test the write path**: Generate a small test cohort (5 patients) and verify it persists in MotherDuck. Then delete it. This validates the full CRUD cycle against MotherDuck.

5. **Git commit**: "test: verify all MCP tools work against MotherDuck"

## Deliverables

- `scripts/test_mcp_motherduck.py` — automated tool verification
- All 11 tools verified working against MotherDuck
- Any schema mismatches identified and fixed
- Write path (create + delete cohort) verified
- Committed
