# HealthSim Deploy Scripts

Scripts for deploying HealthSim as a Managed Agent on Anthropic's platform.

For the full operations guide, see [docs/MANAGED-AGENT-GUIDE.md](../docs/MANAGED-AGENT-GUIDE.md).

## Prerequisites

- `.env` file at project root with `ANTHROPIC_API_KEY`, `HEALTHSIM_MCP_TOKEN`, `MOTHERDUCK_TOKEN`
- Python venv activated with `anthropic` and `pyyaml` installed
- MCP server deployed to Railway (URL in `railway-url.txt`)
- MotherDuck database `healthsim_ref` populated via `scripts/migrate_to_motherduck.py`

## Quick Start — Deploy from Scratch

```bash
source .env

# 1. Upload all skills to Anthropic Skills API
.venv/bin/python deploy/push-skills.py --all

# 2. Create the agent definition
.venv/bin/python deploy/push-agent.py

# 3. Create the environment
.venv/bin/python deploy/push-environment.py

# 4. Test with a session
./deploy/run.sh
```

## Scripts

### push-skills.py

Uploads SKILL.md files to the Anthropic Skills API. Reads skill paths from `agent-config.yaml`.

```bash
.venv/bin/python deploy/push-skills.py --all              # Upload all skills
.venv/bin/python deploy/push-skills.py --path ./skills/patientsim/  # Upload one
.venv/bin/python deploy/push-skills.py --list              # List uploaded skills
.venv/bin/python deploy/push-skills.py --delete <skill_id> # Remove a skill
```

Output: `skill-ids.json` — mapping of skill names to Anthropic skill IDs.

### push-agent.py

Creates or updates the Managed Agent definition. Reads system prompt, skill IDs, and MCP server config.

```bash
.venv/bin/python deploy/push-agent.py           # Create new agent
.venv/bin/python deploy/push-agent.py --update   # Update existing (version increment)
```

Output: `agent-ids.json` — agent ID, version, and environment ID.

### push-environment.py

Creates or updates the container environment (pip packages, networking rules).

```bash
.venv/bin/python deploy/push-environment.py
```

Output: Updates `agent-ids.json` with environment ID.

### start-session.py

Interactive CLI for chatting with the deployed Managed Agent.

```bash
.venv/bin/python deploy/start-session.py                    # New session
.venv/bin/python deploy/start-session.py --session <id>     # Resume session
```

In-session commands: `session`, `history`, `export <file>`, `quit`

### run.sh

Convenience wrapper — loads `.env` and runs `start-session.py`.

```bash
./deploy/run.sh                    # New session
./deploy/run.sh --session <id>     # Resume session
```

## Updating After Changes

| What Changed | Run |
|-------------|-----|
| A skill file | `push-skills.py --path ./skills/<name>/` then `push-agent.py --update` |
| System prompt | Edit `system-prompt.md` then `push-agent.py --update` |
| MCP server code | `railway up` (rebuild and deploy container) |
| Python dependencies | Update `agent-config.yaml` then `push-environment.py` |
| Reference data | `scripts/migrate_to_motherduck.py --full` |
