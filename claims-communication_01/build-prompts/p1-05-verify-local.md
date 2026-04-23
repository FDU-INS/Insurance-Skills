# p1-05: Verify Local CLI Still Works

## What to build

Confirm that the local Claude Code development workflow is completely unaffected by the migration changes. This is the safety check before moving to Phase 2.

## Context

We've changed the connection manager and the MCP server transport logic. The local development path (stdio transport, local DuckDB file) must still work exactly as before.

## Tasks

1. **Unset all cloud environment variables**:
   ```bash
   unset MOTHERDUCK_TOKEN
   unset MCP_TRANSPORT
   unset MCP_PORT
   unset HEALTHSIM_MCP_TOKEN
   ```

2. **Run the existing test suite**:
   ```bash
   .venv/bin/python -m pytest packages/ -x -q
   ```
   All tests must pass.

3. **Run the smoke tests**:
   ```bash
   .venv/bin/python scripts/smoke_test.py
   .venv/bin/python scripts/smoke_test_generation.py
   ```

4. **Verify MCP server works in stdio mode** by checking that Claude Code can still use it:
   - Open a new Claude Code session in the healthsim-workspace
   - Ask: "List my saved cohorts"
   - Ask: "Search for pediatricians in San Diego"
   - Both should work via the local MCP server using stdio transport and local DuckDB

5. **Document the verification** in `deploy/spike-results.md` (append a "Phase 1 Verification" section):
   - Test suite: pass/fail
   - Smoke tests: pass/fail
   - Claude Code MCP: pass/fail
   - Any issues encountered

6. **Git commit**: "test: verify local development workflow after MotherDuck migration"

## Deliverables

- All existing tests passing
- Smoke tests passing
- Claude Code MCP workflow verified
- Results documented
- Committed

## Phase 1 Complete

At this point:
- ✅ All reference data is in MotherDuck
- ✅ MCP server runs on Railway connected to MotherDuck
- ✅ Local development still works unchanged
- Ready for Phase 2 (skills adaptation and upload)
