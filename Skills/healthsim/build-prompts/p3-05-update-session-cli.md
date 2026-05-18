# p3-05: Update start-session.py for Production Agent

## What to build

Update `deploy/start-session.py` to work as a polished CLI for the production HealthSim Managed Agent. This becomes your primary non-Console interaction tool until the Rewire UI is built.

## Tasks

1. **Update `deploy/start-session.py`** to:

   a. Read agent ID and environment ID from `deploy/agent-ids.json` (instead of creating new ones each time)
   
   b. Create a new session using the existing agent/environment
   
   c. Support resuming an existing session via `--session <session_id>` flag
   
   d. Pretty-print the streamed output:
      - Agent text: print normally with word wrapping
      - Tool calls: print as `[Tool: healthsim_search_providers] → searching...`
      - Tool results: print a brief summary, not the full JSON
      - Errors: print in red/highlighted
   
   e. Support these commands in the interactive prompt:
      - `quit` or `exit` — end the session
      - `session` — print the current session ID
      - `history` — print a summary of the conversation so far
      - `export <filename>` — save the conversation to a file
   
   f. Print session ID at startup so it can be resumed later

2. **Add a `deploy/run.sh`** convenience wrapper:
   ```bash
   #!/bin/bash
   source .env
   .venv/bin/python deploy/start-session.py "$@"
   ```

3. **Test the polished CLI**:
   ```bash
   chmod +x deploy/run.sh
   ./deploy/run.sh
   ```
   
   Run through a quick generation workflow:
   - "Generate 10 diabetic patients in Los Angeles"
   - "Export the demographics as CSV"
   - "Save this cohort as 'la-diabetes-10'"
   - `session` (print the session ID)
   - `exit`
   
   Then resume:
   ```bash
   ./deploy/run.sh --session <session_id>
   ```
   - "Load the cohort 'la-diabetes-10'"
   - Verify it remembers the context

4. **Git commit**: "feat: polished start-session.py CLI for production agent"

## Deliverables

- Updated `deploy/start-session.py` with session resume, pretty printing, commands
- `deploy/run.sh` convenience wrapper
- Tested end-to-end
- Committed

## Phase 3 Complete — Milestone

At this point:
- ✅ HealthSim runs as a Managed Agent on Anthropic's infrastructure
- ✅ MCP server on Railway connected to MotherDuck
- ✅ All 9 skills uploaded and loaded correctly
- ✅ Full validation checklist passing
- ✅ Accessible via Console UI and CLI tool
- ✅ Local Claude Code development workflow unchanged

**The infrastructure patterns (deploy scripts, manifest, Railway, MotherDuck, Skills API) are now proven and reusable for BioScience Agent and Vantage.**

Ready for Phase 4 (Rewire Core Framework) when you are.
