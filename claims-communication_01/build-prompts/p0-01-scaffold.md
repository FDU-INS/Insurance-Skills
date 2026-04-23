# p0-01: Directory Scaffold + Environment Setup

## What to build

Set up the directory structure, environment file, and dependencies for the Managed Agent migration. This does NOT change any existing code — it only adds new infrastructure alongside what's already here.

## Tasks

1. Create the `deploy/` directory with placeholder files:
   ```
   deploy/
   ├── push-skills.py        # placeholder — built in Phase 2
   ├── push-agent.py         # placeholder — built in Phase 3
   ├── push-environment.py   # placeholder — built in Phase 3
   └── start-session.py      # placeholder — built in Phase 3
   ```

2. Create `.env` at project root (if it doesn't exist) with these keys. DO NOT fill in values — leave them as placeholders for the user to fill in:
   ```
   # Anthropic
   ANTHROPIC_API_KEY=your-key-here

   # Railway MCP Server
   HEALTHSIM_MCP_TOKEN=generate-a-random-token-here

   # MotherDuck
   MOTHERDUCK_TOKEN=your-motherduck-token-here

   # Supabase (Phase 4 — not needed yet)
   SUPABASE_URL=your-supabase-url-here
   SUPABASE_ANON_KEY=your-supabase-anon-key-here
   ```

3. Verify `.env` is in `.gitignore`. If not, add it.

4. Install the Anthropic Python SDK in the existing `.venv`:
   ```bash
   .venv/bin/pip install anthropic
   ```

5. Verify `agent-config.yaml` exists at project root (it should — it was created alongside these prompts). Read it and confirm it references the correct skill paths and MCP server path for this project.

6. Git add the new files (deploy/, agent-config.yaml, build-prompts/), commit with message: "chore: scaffold managed agent migration infrastructure"

## Deliverables

- `deploy/` directory with placeholder scripts
- `.env` with placeholder keys
- `.gitignore` updated if needed
- `anthropic` package installed in .venv
- `agent-config.yaml` verified
- Committed and pushed

## Do NOT

- Modify any existing code
- Fill in actual API keys (the user will do this)
- Start building the deploy scripts yet — those come in later phases
