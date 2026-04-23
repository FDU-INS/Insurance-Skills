# p3-02: Build push-agent.py and push-environment.py

## What to build

Create the two remaining deploy scripts that create/update the Managed Agent definition and environment via the Anthropic API.

## Tasks

1. **Create `deploy/push-agent.py`** that:

   a. Reads `agent-config.yaml` for: name, model, mcp_servers
   b. Reads `deploy/system-prompt.md` for the system prompt content
   c. Reads `deploy/skill-ids.json` for the uploaded skill IDs
   d. Reads `deploy/railway-url.txt` for the MCP server URL
   e. Reads `HEALTHSIM_MCP_TOKEN` and `ANTHROPIC_API_KEY` from `.env`
   
   f. Creates or updates the agent via `POST /v1/agents` (or `PUT` for update):
   ```json
   {
     "name": "HealthSim",
     "model": "claude-sonnet-4-6",
     "system": "<contents of system-prompt.md>",
     "tools": [{"type": "agent_toolset_20260401"}],
     "skills": ["<skill_id_1>", "<skill_id_2>", ...],
     "mcp_servers": [
       {
         "url": "<railway_url>",
         "authorization_token": "<mcp_token>"
       }
     ]
   }
   ```
   
   g. Saves agent ID and version to `deploy/agent-ids.json`:
   ```json
   {
     "agent_id": "agent_01...",
     "agent_version": 1,
     "environment_id": null
   }
   ```
   
   h. Supports `--update` flag that passes the current version for safe updates

2. **Create `deploy/push-environment.py`** that:

   a. Reads `agent-config.yaml` for environment config
   b. Creates the environment via `POST /v1/environments`:
   ```json
   {
     "name": "healthsim-production",
     "config": {
       "type": "cloud",
       "packages": {
         "pip": ["duckdb", "pandas", "faker", "scipy", "pydantic"]
       },
       "networking": {
         "type": "limited",
         "allow_mcp_servers": true,
         "allow_package_managers": true
       }
     }
   }
   ```
   
   c. Saves the environment ID to `deploy/agent-ids.json` (updates the existing file)

3. **Test both scripts** (dry run — just verify the API calls would be correct):
   ```bash
   .venv/bin/python deploy/push-agent.py
   .venv/bin/python deploy/push-environment.py
   ```

4. **Git commit**: "feat: add push-agent.py and push-environment.py deploy scripts"

## Deliverables

- `deploy/push-agent.py`
- `deploy/push-environment.py`
- Both tested
- `deploy/agent-ids.json` created with IDs
- Committed

## Note on MCP Server Config

The exact schema for `mcp_servers` in the agent definition may differ from what's shown above. Consult the Anthropic docs at `platform.claude.com/docs/en/managed-agents/agent-setup` for the correct field names. The MCP server may need to be specified as a remote URL with auth headers rather than inline config. Adapt accordingly.
