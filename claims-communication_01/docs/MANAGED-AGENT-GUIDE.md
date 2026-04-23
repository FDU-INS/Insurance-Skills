# HealthSim Managed Agent Guide

> **Develop locally in Claude Code. Deploy to the cloud via Managed Agent. Use from Console, CLI, or Web.**

This guide covers the Managed Agent deployment of HealthSim — how it works, how to deploy it, how to access it, and how to keep it in sync with your local development environment.

---

## Solution Lifecycle

HealthSim supports two deployment modes that share the same codebase:

```
DEVELOP (Claude Code)           DEPLOY (Managed Agent)          USE
───────────────────────         ───────────────────────         ─────────────────────────
Edit skills locally       →    push-skills.py            →     Console UI (platform.claude.com)
Edit MCP server locally   →    Deploy to Railway         →     CLI (deploy/run.sh)
Edit Python modules       →    Redeploy Railway          →     Web App (Rewire — coming)
Test with local DuckDB    →    Data lives in MotherDuck
Run evals locally         →    push-agent.py
                               push-environment.py
```

**Claude Code is your development environment.** You edit skills, test MCP tools, run generation workflows, and iterate — all locally with stdio transport and a local DuckDB file.

**Managed Agent is your deployment target.** When your changes are tested and ready, you run the deploy scripts to push them to Anthropic's infrastructure. The Managed Agent uses the same skills, the same MCP server code, and the same Python modules — just with HTTP transport and MotherDuck instead of local files.

**Users access the deployed agent** through the Anthropic Console UI, a CLI tool, or (coming soon) the Rewire web application. They never touch Claude Code or your local environment.

---

## Architecture

Five platforms, each handling what it does best:

| Platform | Role | What It Stores/Runs |
|----------|------|---------------------|
| **Anthropic Managed Agents** | Agent runtime | Agent definition, skills, session management, context, compaction |
| **Railway** | MCP server hosting | HealthSim MCP server (HTTP transport, bearer auth, 11 tools) |
| **MotherDuck** | Analytical data | NPPES providers (8.9M), CDC PLACES, SVI, cohort data, reference codes |
| **Supabase** | Application state | User accounts, session history, saved analyses (used by Rewire web app) |
| **GitHub** | Source of truth | All code, skills, configuration — everything else is a deployment target |

### The Data Boundary Rule

- **If the agent queries it during analysis → MotherDuck.** Reference data, generated cohorts, provider lookups.
- **If the web app queries it to manage the user experience → Supabase.** Auth, session tracking, saved analyses.

No overlap between the two. The agent inside the Managed Agent container connects to MotherDuck via the MCP server. The Rewire web frontend connects to Supabase. They never cross.

### How a Request Flows

```
User (Console/CLI/Web)
  │
  ▼
Anthropic Managed Agent Session
  │
  ├── Agent reads skill instructions (loaded from Skills API)
  ├── Agent decides to call MCP tool
  │     │
  │     ▼
  │   Railway MCP Server (HTTPS)
  │     │
  │     ├── Queries MotherDuck (reference data, cohorts)
  │     ├── Runs generation engine (Python modules)
  │     └── Returns results to agent
  │
  └── Agent formulates response → streamed back to user
```

---

## The agent-config.yaml Manifest

The `agent-config.yaml` at the project root is the single manifest that drives all deployment. The deploy scripts read it; you rarely need to call the APIs directly.

```yaml
name: healthsim                          # Agent name
model: claude-sonnet-4-6                 # Model for the Managed Agent
description: Synthetic healthcare data generation platform

system_prompt_source: ./deploy/system-prompt.md   # Cloud-adapted system prompt

skills:                                  # Skills to upload to Skills API
  - path: ./skills/patientsim/SKILL.md   # Each path is read and uploaded
    skill_id: skill_healthsim_patientsim_v1
  - path: ./skills/membersim/SKILL.md
    skill_id: skill_healthsim_membersim_v1
  # ... (9 skills total)

mcp_servers:                             # MCP servers the agent can call
  - name: healthsim-mcp
    local: ./packages/mcp-server/healthsim_mcp.py   # For local dev reference
    remote: https://healthsim-mcp.up.railway.app     # Production URL
    auth_env: HEALTHSIM_MCP_TOKEN                    # Shared secret

environment:                             # Container configuration
  packages:
    pip: [duckdb, pandas, faker, scipy, pydantic]
  networking:
    type: limited
    allow_mcp_servers: true
    allow_package_managers: true

storage:                                 # Data layer configuration
  analytical:
    type: motherduck
    database: healthsim_ref
    token_env: MOTHERDUCK_TOKEN
  operational:
    type: supabase
    url_env: SUPABASE_URL
    key_env: SUPABASE_ANON_KEY
```

---

## Deploy Scripts Reference

All scripts live in `deploy/` and read from `agent-config.yaml` and `.env`.

| Script | What It Does | When to Run |
|--------|-------------|-------------|
| `push-skills.py` | Uploads SKILL.md files to the Anthropic Skills API | After editing any skill |
| `push-agent.py` | Creates/updates the agent definition (system prompt, skill IDs, MCP server URLs) | After changing agent config or system prompt |
| `push-environment.py` | Creates/updates the container environment (pip packages, networking rules) | After changing Python dependencies |
| `start-session.py` | Interactive CLI for chatting with the Managed Agent | Testing and ad-hoc use |
| `run.sh` | Convenience wrapper — loads `.env` and runs `start-session.py` | Quick access |

### Generated Artifacts

These files are created by the deploy scripts and gitignored (they contain environment-specific IDs):

| File | Contents | Created By |
|------|----------|-----------|
| `deploy/skill-ids.json` | Mapping of skill names → Anthropic skill IDs | `push-skills.py` |
| `deploy/agent-ids.json` | Agent ID, version, and environment ID | `push-agent.py` / `push-environment.py` |
| `deploy/railway-url.txt` | The Railway deployment URL for the MCP server | Manual (during Railway deploy) |
| `deploy/system-prompt.md` | Cloud-adapted system prompt (derived from CLAUDE.md) | Manual (Phase 3) |
| `deploy/spike-results.md` | Validation test results | Manual (during testing) |

### Deploy from Scratch

```bash
# 1. Fill in .env with your API keys and tokens
# 2. Deploy in order:

source .env

# Upload all skills
.venv/bin/python deploy/push-skills.py --all

# Create the agent definition
.venv/bin/python deploy/push-agent.py

# Create the environment
.venv/bin/python deploy/push-environment.py

# Verify with a test session
./deploy/run.sh
```

---

## How to Access the Managed Agent

### Console UI (platform.claude.com)

The Anthropic Console provides a browser-based interface for testing Managed Agents.

1. Go to [platform.claude.com](https://platform.claude.com)
2. Navigate to **Managed Agents**
3. Select the **HealthSim** agent
4. Click **Start Session** — select the `healthsim-production` environment
5. Chat with the agent in the browser

The Console is a developer tool — good for testing and debugging, but not intended for end users. You can inspect tool calls, see raw events, and debug issues that might be hidden by a polished UI.

### CLI (deploy/start-session.py)

A terminal-based chat interface for interacting with the Managed Agent from your local machine.

```bash
# Start a new session
./deploy/run.sh

# Resume an existing session
./deploy/run.sh --session <session_id>
```

**In-session commands:**
- Type your message and press Enter to send
- `session` — print the current session ID (for resuming later)
- `history` — print a summary of the conversation
- `export <filename>` — save the conversation to a file
- `quit` or `exit` — end the session

The CLI streams responses in real time and shows tool call indicators when the agent calls MCP tools.

### Web App (Rewire — coming)

The Rewire web application adds authentication, session history, visualization components, and a polished UI on top of the Managed Agent. It's currently in development (Phases 4-5). When complete, it will be the primary interface for end users.

- Auth via Supabase (email/password)
- Session history sidebar
- Rich visualizations (SDTM inspector, population config panel, CDISC validator)
- Template gallery for common generation tasks
- Deployed on Vercel

---

## Common Workflows

### "I updated a skill and want to deploy it"

```bash
# 1. Edit the skill locally
#    e.g., skills/patientsim/SKILL.md

# 2. Test locally in Claude Code — verify the skill works

# 3. Upload the updated skill
.venv/bin/python deploy/push-skills.py --path ./skills/patientsim/

# 4. Update the agent definition (picks up new skill version)
.venv/bin/python deploy/push-agent.py --update

# 5. New sessions will use the updated skill
```

### "I changed the MCP server code"

```bash
# 1. Edit packages/mcp-server/healthsim_mcp.py

# 2. Test locally in HTTP mode
export MCP_TRANSPORT=http && export MCP_PORT=8001
.venv/bin/python packages/mcp-server/healthsim_mcp.py
# In another terminal: run test_mcp_motherduck.py against localhost

# 3. Rebuild and deploy to Railway
railway up

# 4. Verify Railway deployment
curl https://healthsim-mcp.up.railway.app/
```

### "I added a new Python dependency"

```bash
# 1. Add to packages/core/pyproject.toml and install locally
.venv/bin/pip install <package>

# 2. Update agent-config.yaml → environment.packages.pip

# 3. Update the Managed Agent environment
.venv/bin/python deploy/push-environment.py

# 4. Also update the Dockerfile for Railway if the MCP server needs it
railway up
```

### "I want to add reference data to MotherDuck"

```bash
# 1. Load data into local DuckDB first, verify queries work

# 2. Add migration logic to scripts/migrate_to_motherduck.py

# 3. Run the migration
.venv/bin/python scripts/migrate_to_motherduck.py --full

# 4. Verify row counts match
.venv/bin/python scripts/migrate_to_motherduck.py --verify
```

---

## Environment Variables Reference

All variables are stored in `.env` at the project root (gitignored). Load with `source .env` or use `python-dotenv`.

| Variable | Where Used | How to Get It |
|----------|-----------|---------------|
| `ANTHROPIC_API_KEY` | Deploy scripts, Managed Agent | [platform.claude.com/settings/keys](https://platform.claude.com/settings/keys) |
| `HEALTHSIM_MCP_TOKEN` | Railway MCP server, agent definition | Generate: `openssl rand -hex 32` |
| `MOTHERDUCK_TOKEN` | MCP server, migration scripts | [app.motherduck.com](https://app.motherduck.com) → Settings → Access Tokens |
| `SUPABASE_URL` | Rewire web app (Phase 4+) | [supabase.com/dashboard](https://supabase.com/dashboard) → Project Settings → API |
| `SUPABASE_ANON_KEY` | Rewire web app (Phase 4+) | Same as above |
| `HEALTHSIM_AGENT_ID` | Rewire web app (Phase 4+) | Output of `push-agent.py` → `deploy/agent-ids.json` |
| `HEALTHSIM_ENVIRONMENT_ID` | Rewire web app (Phase 4+) | Output of `push-environment.py` → `deploy/agent-ids.json` |

---

## Troubleshooting

### MCP server not reachable from Managed Agent

- Check Railway logs: `railway logs`
- Verify the Railway URL in `deploy/railway-url.txt` matches the agent definition
- Verify the bearer token matches between Railway env vars and the agent definition
- Test the server directly: `curl -H "Authorization: Bearer <token>" https://<railway-url>/`

### Skills not loading

- Run `deploy/push-skills.py --list` to verify all skills are uploaded
- Check that skill IDs in `deploy/skill-ids.json` match what `push-agent.py` sends
- Re-run `push-agent.py` to refresh the agent definition

### MotherDuck connection fails

- Verify `MOTHERDUCK_TOKEN` is set in Railway env vars
- Test connection: `python -c "import duckdb; duckdb.connect('md:healthsim_ref').execute('SELECT 1')"`
- Check MotherDuck dashboard for the `healthsim_ref` database

### Agent doesn't use MCP tools

- Verify the MCP server URL in the agent definition
- Check that `allow_mcp_servers: true` is set in the environment networking config
- Test the MCP server independently with curl before testing through the agent

### Session won't resume

- Session IDs are specific to an agent version — if you updated the agent, old sessions may not be resumable
- Check `deploy/agent-ids.json` for the current agent version
- Start a new session if the old one is incompatible

### Local Claude Code workflow broken

- Unset cloud env vars: `unset MOTHERDUCK_TOKEN MCP_TRANSPORT MCP_PORT HEALTHSIM_MCP_TOKEN`
- Verify local DuckDB file exists: `ls -la healthsim_current.duckdb`
- Run the test suite: `.venv/bin/python -m pytest packages/ -x -q`
- The connection manager should fall back to local DuckDB when `MOTHERDUCK_TOKEN` is not set

---

*HealthSim Managed Agent Guide · April 2026*
