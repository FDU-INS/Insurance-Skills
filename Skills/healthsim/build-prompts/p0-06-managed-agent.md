# p0-06: Create Managed Agent + Test Session

## What to build

Wire everything together: create a Managed Agent definition that references the Railway MCP server and the uploaded skill, create an environment, start a test session, and validate end-to-end. This is the gate check for Phase 0.

## Context

You now have:
- A Railway-hosted MCP server URL (from p0-04, in `deploy/railway-url.txt`)
- A skill ID uploaded to the Skills API (from p0-05, in `deploy/skill-ids.json`)
- A MotherDuck database with sample reference data (from p0-03)

The Managed Agents API uses these endpoints (all require `managed-agents-2026-04-01` beta header):
- `POST /v1/agents` — create an agent definition
- `POST /v1/environments` — create a container environment
- `POST /v1/sessions` — start a session
- `POST /v1/sessions/{id}/events` — send a user message
- `GET /v1/sessions/{id}/events` — stream responses (SSE)

## Tasks

1. **Create `deploy/start-session.py`** — a CLI tool that creates an agent, environment, and session, then enters an interactive prompt loop. This is your primary testing tool and will also serve as the template for the Rewire SSE consumer later.

   The script should:

   a. Load config from `.env` and `deploy/skill-ids.json` and `deploy/railway-url.txt`

   b. Create an agent via `POST /v1/agents`:
   ```json
   {
     "name": "HealthSim Spike",
     "model": "claude-sonnet-4-6",
     "system": "You are HealthSim, a synthetic healthcare data generation platform. You can generate realistic patient cohorts, claims data, clinical trial data, and provider networks. Use the healthsim MCP tools to query reference data and manage cohorts. Be helpful and precise.",
     "tools": [{"type": "agent_toolset_20260401"}],
     "skills": ["<skill_id_from_skill-ids.json>"],
     "mcp_servers": [
       {
         "url": "<railway_url_from_railway-url.txt>",
         "authorization_token": "<HEALTHSIM_MCP_TOKEN from .env>"
       }
     ]
   }
   ```

   c. Create an environment via `POST /v1/environments`:
   ```json
   {
     "name": "healthsim-spike-env",
     "config": {
       "type": "cloud",
       "packages": {
         "pip": ["duckdb", "pandas"]
       },
       "networking": {"type": "unrestricted"}
     }
   }
   ```

   d. Create a session via `POST /v1/sessions`:
   ```json
   {
     "agent_id": "<agent_id>",
     "agent_version": <version>,
     "environment_id": "<environment_id>"
   }
   ```

   e. Send an initial user event and stream the response:
   ```json
   {
     "type": "user",
     "content": [{"type": "text", "text": "<user prompt>"}]
   }
   ```

   f. Print each streamed SSE event to the terminal as it arrives. For text content, print it inline. For tool calls, print a summary (tool name + args).

   g. After the agent finishes responding, prompt for the next user input. Loop until the user types `quit` or `exit`.

   **Important**: Check the Anthropic Python SDK for Managed Agents support first. The SDK may have helper methods that simplify this. If not, use raw HTTP with `requests` and SSE parsing with `sseclient-py` (install if needed).

2. **Run the gate check tests**. Start the session and try these prompts in order:

   **Test 1 — Skill loaded?**
   ```
   What capabilities do you have for generating healthcare data?
   ```
   Expected: The agent should reference HealthSim-specific capabilities from the common skill.

   **Test 2 — MCP server reachable?**
   ```
   List my saved cohorts using the healthsim tools.
   ```
   Expected: The agent should call `healthsim_list_cohorts` via the Railway MCP server. It may return an empty list (that's fine — proves connectivity).

   **Test 3 — MCP + reference data?**
   ```
   Search for cardiologists in California using the provider search tool.
   ```
   Expected: The agent should call `healthsim_search_providers` and return NPPES data from the DuckDB bundled in the Railway container.

3. **Document the results** in `deploy/spike-results.md`:
   - Agent ID and version
   - Environment ID
   - Session ID
   - Pass/fail for each of the three tests
   - Any issues encountered and how they were resolved
   - Railway URL confirmed working
   - Latency observations (how long did MCP calls take?)

4. **Git commit**: "feat: add start-session.py and Phase 0 spike results"

## Deliverables

- `deploy/start-session.py` — interactive Managed Agent CLI
- `deploy/spike-results.md` — documented test results
- All three gate check tests passing
- Committed

## Gate Check Summary

| Test | What It Proves | Pass Criteria |
|------|---------------|---------------|
| Skill loaded | Skills API upload + agent loading works | Agent references HealthSim capabilities |
| MCP reachable | Railway deployment + HTTP transport + auth works | Agent calls healthsim_list_cohorts successfully |
| Reference data | DuckDB in container + MCP query path works | Agent returns provider data from NPPES |

**If all three pass → proceed to Phase 1.**
**If any fail → debug here. Do not proceed.**

## After Phase 0

You can also test via the Anthropic Console UI at `platform.claude.com`. Create a test session manually using the Agent ID and Environment ID from the spike results. This gives you a browser-based interface while we build the Rewire UI in Phases 4-5.

## Notes on the Managed Agents API

- The API is in beta (`managed-agents-2026-04-01` header required on all requests)
- The SDK may or may not have full support yet — check docs and fall back to raw HTTP if needed
- SSE streaming from `GET /v1/sessions/{id}/events` follows standard Server-Sent Events format
- Sessions persist server-side — you can reconnect to an existing session by ID
- The MCP server configuration in the agent definition may use different field names than shown above — consult the docs at `platform.claude.com/docs/en/managed-agents/` for the exact schema
