# p0-05: Upload Test Skill to Skills API

## What to build

Upload one skill to the Anthropic Skills API to validate the upload flow and confirm the skill loads correctly in a Managed Agent. Use the `skills/common/` skill since it's the simplest.

## Context

The Anthropic Skills API allows uploading custom skills via `POST /v1/skills`. Skills require the `managed-agents-2026-04-01` beta header. The API returns a skill ID that you reference when creating an agent.

Read the Skills API documentation first. The Anthropic Python SDK should support skills — check via:
```bash
.venv/bin/python -c "import anthropic; help(anthropic.Anthropic().beta)"
```

If the SDK doesn't have direct skills support yet (it's beta), use raw HTTP requests via the `requests` library or `curl`.

## Tasks

1. **Read the current common skill** to understand what we're uploading:
   ```bash
   cat skills/common/SKILL.md
   ls skills/common/
   ```

2. **Create `deploy/push-skills.py`** — a minimal version that uploads a single skill. This will be expanded in Phase 2 to handle all skills from the manifest. For now, it should:

   a. Load `ANTHROPIC_API_KEY` from `.env`
   b. Read the skill file(s) from a given path
   c. Upload via `POST /v1/skills` with the beta header
   d. Print the returned skill ID
   e. Save the skill ID to `deploy/skill-ids.json`

   The script should accept a `--path` argument for the skill directory and a `--name` argument for the skill identifier.

   Usage:
   ```bash
   .venv/bin/python deploy/push-skills.py \
     --path ./skills/common/ \
     --name skill_healthsim_common_v1
   ```

3. **Run the upload**:
   ```bash
   source .env
   .venv/bin/python deploy/push-skills.py \
     --path ./skills/common/ \
     --name skill_healthsim_common_v1
   ```

4. **Verify the upload** by listing skills:
   ```bash
   curl -s https://api.anthropic.com/v1/skills \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "anthropic-beta: managed-agents-2026-04-01" | python -m json.tool
   ```

5. **Record the skill ID** in `deploy/skill-ids.json`:
   ```json
   {
     "skill_healthsim_common_v1": "skill_01abc..."
   }
   ```

6. **Git commit**: "feat: add push-skills.py and upload test skill"

## Deliverables

- `deploy/push-skills.py` (minimal, single-skill version)
- `deploy/skill-ids.json` with the uploaded skill ID
- Verified: skill appears in Skills API listing
- Committed

## Important

- The Skills API is in beta. If the endpoint structure or request format differs from what's documented here, adapt accordingly. The Anthropic docs at `platform.claude.com/docs/en/agents-and-tools/agent-skills/` are the authoritative source.
- If multi-file skills (SKILL.md + supporting .md files) need special handling for the API, document what you learn — we'll need this knowledge for Phase 2 when uploading all 9 skills.
- Do NOT modify the skill content yet. Upload it as-is. Adaptation (replacing embedded data refs, adding output format sections) happens in Phase 2.
