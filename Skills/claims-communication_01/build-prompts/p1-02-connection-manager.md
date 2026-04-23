# p1-02: Adapt Connection Manager for MotherDuck

## What to build

Modify `packages/core/src/healthsim/db/connection.py` to support both local DuckDB files and MotherDuck connections, switchable via environment variable. The local path remains the default for Claude Code development.

## Context

The current connection manager uses a close-before-write pattern with local DuckDB files. MotherDuck handles concurrency differently — it's a cloud service, so the single-writer constraint of local DuckDB may not apply in the same way. We need to understand and adapt for this.

Read these files first:
- `packages/core/src/healthsim/db/connection.py`
- `packages/core/src/healthsim/db/__init__.py`
- Any other files in `packages/core/src/healthsim/db/` that reference the connection

## Tasks

1. **Understand the current connection pattern**: Read `connection.py` and document how it manages connections. Note the close-before-write pattern and any singleton/pool behavior.

2. **Add MotherDuck connection support**:
   - If `MOTHERDUCK_TOKEN` is set in the environment, connect to MotherDuck: `duckdb.connect('md:healthsim_ref')`
   - If not set, fall back to the local DuckDB file path (existing behavior)
   - The connection string logic should be centralized in one place — don't scatter `md:` checks throughout the codebase

3. **Evaluate the close-before-write pattern for MotherDuck**:
   - MotherDuck supports concurrent reads and writes differently than local DuckDB
   - Test whether the existing pattern works as-is, or if it needs adaptation
   - If the pattern needs to change for MotherDuck, make the change conditional on connection type
   - Document your findings in a code comment

4. **Test both paths**:
   ```bash
   # Test MotherDuck path
   MOTHERDUCK_TOKEN=<token> .venv/bin/python -c "
   from healthsim.db.connection import get_connection
   conn = get_connection()
   result = conn.execute('SELECT COUNT(*) FROM reference.nppes_providers').fetchone()
   print(f'MotherDuck NPPES count: {result[0]}')
   "

   # Test local path (unset MOTHERDUCK_TOKEN)
   unset MOTHERDUCK_TOKEN
   .venv/bin/python -c "
   from healthsim.db.connection import get_connection
   conn = get_connection()
   # run equivalent local query
   "
   ```

5. **Run existing tests** to make sure nothing breaks:
   ```bash
   .venv/bin/python -m pytest packages/core/ -x -q
   ```

6. **Git commit**: "feat: dual connection support — local DuckDB and MotherDuck"

## Deliverables

- Updated `connection.py` with MotherDuck support
- Local DuckDB path still works as default
- Both paths tested
- Existing tests still pass
- Committed

## Important

- The MCP server imports from this connection module. Changing it here affects the server too — that's intentional. After this change, the MCP server can connect to either local or MotherDuck depending on environment.
- Do NOT change the connection module's public API (function signatures, class interfaces). Callers shouldn't need to know which backend they're talking to.
