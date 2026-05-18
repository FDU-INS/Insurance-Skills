# Documentation Audit: Managed Agent Migration

## Context

HealthSim now supports two deployment modes:
1. **Local development** — Claude Code with stdio MCP, local DuckDB (existing, unchanged)
2. **Managed Agent** — Anthropic-hosted agent with Railway MCP server, MotherDuck, accessible via Console UI, CLI tool, and (soon) Rewire web app

The current documentation only covers mode 1. We need to document mode 2 across the project without breaking or confusing the existing mode 1 docs. The key is making the **solution lifecycle** clear: you develop locally in Claude Code, then deploy to the Managed Agent infrastructure.

Read these files first to understand the current state:
- `README.md`
- `INSTALL.md`
- `hello-healthsim/README.md`
- `.claude/CLAUDE.md`
- `deploy/` directory contents
- `agent-config.yaml`

## Task 1: Create `docs/MANAGED-AGENT-GUIDE.md`

This is the primary new document. It should cover the complete Managed Agent story in this order:

### 1. Solution Lifecycle Overview

Start with a clear diagram/table of the lifecycle:

```
DEVELOP (Claude Code)          DEPLOY (Managed Agent)         USE (Console / CLI / Web)
─────────────────────          ─────────────────────          ──────────────────────────
Edit skills locally     →      push-skills.py          →      Console UI at platform.claude.com
Edit MCP server locally →      Deploy to Railway       →      CLI via deploy/run.sh
Edit Python modules     →      Redeploy Railway        →      Web via Rewire (coming)
Run tests locally       →      push-agent.py           →
                               push-environment.py
```

Make it crystal clear: **Claude Code is for development. Managed Agent is for deployment. They use the same skills, same MCP server code, same Python modules — just different transports and data connections.**

### 2. Architecture

Explain the five-platform architecture:
- **Anthropic Managed Agents** — agent runtime (skills, sessions, context management)
- **Railway** — MCP server hosting (HTTP transport, bearer auth)
- **MotherDuck** — analytical data (reference data, cohort storage)
- **Supabase** — application state (users, sessions, saved analyses) — used by Rewire web app
- **GitHub repo** — source of truth for all code and configuration

Include the data boundary rule: agent queries → MotherDuck, web app queries → Supabase.

### 3. The agent-config.yaml Manifest

Explain what it is, what it controls, and how the deploy scripts read it. Include the full annotated manifest with comments explaining each section.

### 4. Deploy Scripts Reference

Document each script in `deploy/`:

| Script | What It Does | When to Run |
|--------|-------------|-------------|
| `push-skills.py` | Uploads SKILL.md files to Anthropic Skills API | After editing any skill |
| `push-agent.py` | Creates/updates the agent definition (system prompt, skills, MCP URLs) | After changing agent config |
| `push-environment.py` | Creates/updates the container environment (pip packages, networking) | After changing dependencies |
| `start-session.py` | Interactive CLI for chatting with the Managed Agent | Testing and ad-hoc use |
| `run.sh` | Convenience wrapper that loads .env and runs start-session.py | Quick access |

### 5. How to Access the Managed Agent

Three access methods, each explained:

**Console UI** (platform.claude.com):
- Where to find it
- How to select the agent and environment
- How to start a test session
- Limitations (developer-facing, not for end users)

**CLI** (deploy/start-session.py):
- How to start a new session
- How to resume an existing session
- Available commands (quit, session, history, export)
- How to find your session ID

**Web App** (Rewire — coming in Phase 4-5):
- What it adds (auth, session history, visualizations, templates)
- Current status
- Where the code lives (rewire monorepo)

### 6. Common Workflows

Document the workflows that will come up most often:

**"I updated a skill and want to deploy it"**
```
1. Edit the skill locally in skills/{product}/SKILL.md
2. Test locally in Claude Code
3. Run: .venv/bin/python deploy/push-skills.py --path ./skills/{product}/
4. The Managed Agent picks up the new skill on the next session
```

**"I changed the MCP server code"**
```
1. Edit packages/mcp-server/healthsim_mcp.py
2. Test locally with MCP_TRANSPORT=http
3. Rebuild and deploy: railway up
4. Verify: curl https://healthsim-mcp.up.railway.app/
```

**"I added a new Python dependency"**
```
1. Add to packages/core/pyproject.toml
2. Test locally
3. Update agent-config.yaml environment.packages.pip
4. Run: .venv/bin/python deploy/push-environment.py
```

**"I want to add reference data to MotherDuck"**
```
1. Load data into local DuckDB first, test queries
2. Add migration logic to scripts/migrate_to_motherduck.py
3. Run migration: .venv/bin/python scripts/migrate_to_motherduck.py --full
4. Verify: .venv/bin/python scripts/migrate_to_motherduck.py --verify
```

### 7. Environment Variables Reference

| Variable | Where Used | How to Get |
|----------|-----------|------------|
| `ANTHROPIC_API_KEY` | Deploy scripts, Managed Agent | platform.claude.com/settings/keys |
| `HEALTHSIM_MCP_TOKEN` | Railway MCP server, agent definition | Generated: `openssl rand -hex 32` |
| `MOTHERDUCK_TOKEN` | MCP server, migration scripts | app.motherduck.com → Settings → Access Tokens |
| `SUPABASE_URL` | Rewire web app (Phase 4+) | supabase.com/dashboard → Project Settings |
| `SUPABASE_ANON_KEY` | Rewire web app (Phase 4+) | supabase.com/dashboard → Project Settings |
| `HEALTHSIM_AGENT_ID` | Rewire web app (Phase 4+) | Output of push-agent.py → deploy/agent-ids.json |
| `HEALTHSIM_ENVIRONMENT_ID` | Rewire web app (Phase 4+) | Output of push-environment.py → deploy/agent-ids.json |

### 8. Troubleshooting

Common issues:
- MCP server not reachable → check Railway logs, verify URL, check bearer token
- Skills not loading → verify skill IDs in agent definition match skill-ids.json
- MotherDuck connection fails → check token, verify database name
- Agent doesn't use MCP tools → check MCP server URL in agent definition
- Session won't resume → check session ID format, session may have expired

## Task 2: Create `deploy/README.md`

A shorter, focused document for the deploy directory. Cover:
- What each script does (one paragraph each)
- Prerequisites (API keys, Railway CLI, MotherDuck account)
- Quick start: how to deploy from scratch in order
- How to update after changes
- File reference (skill-ids.json, agent-ids.json, railway-url.txt, system-prompt.md, spike-results.md)

## Task 3: Update `README.md`

Add a new top-level section between "Getting Started" and "Generative Framework" called **"Deployment Modes"**. This should briefly explain:

- **Local (Claude Code)** — for development and testing. Uses stdio MCP, local DuckDB. Start here.
- **Managed Agent (Cloud)** — for hosted access via Console, CLI, or web app. Uses Railway MCP, MotherDuck. See [Managed Agent Guide](docs/MANAGED-AGENT-GUIDE.md).

Update the **Repository Structure** section to include the new directories:
```
├── agent-config.yaml           # Managed Agent deployment manifest
├── build-prompts/              # Migration execution prompts (Phases 0-3)
├── deploy/                     # Deploy scripts and artifacts
│   ├── push-skills.py
│   ├── push-agent.py
│   ├── push-environment.py
│   ├── start-session.py
│   └── run.sh
```

Update the **Setup** section to mention: "For Managed Agent deployment, see [docs/MANAGED-AGENT-GUIDE.md](docs/MANAGED-AGENT-GUIDE.md)."

Update the **Documentation** table to include the new guide.

## Task 4: Update `INSTALL.md`

Add a new section **"Managed Agent Infrastructure"** after the existing Claude integration section. Cover:

1. **Railway** — install CLI (`brew install railway`), login, deploy MCP server
2. **MotherDuck** — create account, get token, run migration script
3. **Anthropic API** — get API key, verify Managed Agents beta access
4. **Deploy scripts** — run push-skills, push-agent, push-environment

Make it clear this is **in addition to** the local setup, not a replacement. The local setup remains the development environment.

## Task 5: Update `hello-healthsim/README.md`

Add a brief section near the top (after Prerequisites) called **"Access Methods"**:

| Method | Best For | Setup |
|--------|----------|-------|
| **Claude Code** (local) | Development, testing, skill editing | [Setup below](#prerequisites) |
| **Console UI** (cloud) | Quick testing, ad-hoc queries | [Managed Agent Guide](../docs/MANAGED-AGENT-GUIDE.md) |
| **CLI** (cloud) | Scripted access, automation | [Deploy README](../deploy/README.md) |
| **Web App** (cloud) | End users, team access | Coming soon via Rewire |

Keep the rest of the document focused on Claude Code (local) since that's the getting-started path for developers.

## Task 6: Update `CHANGELOG.md`

Add an entry for the Managed Agent migration:

```markdown
## [Unreleased] - Managed Agent Migration

### Added
- Managed Agent deployment via Anthropic Managed Agents API
- `agent-config.yaml` — deployment manifest for skills, MCP servers, and environment
- `deploy/` directory with push-skills.py, push-agent.py, push-environment.py, start-session.py
- `build-prompts/` — Phase 0-3 migration execution prompts
- MotherDuck integration for cloud-hosted reference data
- HTTP transport + bearer auth for MCP server (alongside existing stdio)
- Dual connection manager: local DuckDB (development) / MotherDuck (production)
- `docs/MANAGED-AGENT-GUIDE.md` — comprehensive operations guide

### Changed
- MCP server now supports both stdio and HTTP transports via MCP_TRANSPORT env var
- Connection manager auto-selects local DuckDB or MotherDuck based on MOTHERDUCK_TOKEN env var
- Skills adapted for Skills API upload (embedded data refs → MCP tool calls)

### Unchanged
- All local Claude Code workflows continue to work as before
- DuckDB file still used for local development
- All existing tests still pass
```

## Do NOT

- Modify `.claude/CLAUDE.md` — this stays as-is for local Claude Code development
- Remove or rewrite existing documentation — only add to it
- Make the Managed Agent path seem like the primary path — Claude Code is still the development environment, Managed Agent is the deployment target
- Include actual API keys, tokens, or URLs in documentation

## Commit Strategy

Single commit: "docs: comprehensive documentation update for Managed Agent migration"
