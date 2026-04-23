# p2-01: Expand push-skills.py for All Skills

## What to build

Expand `deploy/push-skills.py` from the single-skill Phase 0 version to a full deployment script that reads `agent-config.yaml` and uploads all skills.

## Tasks

1. **Read `agent-config.yaml`** to get the full list of skills and their paths.

2. **Expand `deploy/push-skills.py`** to:

   a. Parse `agent-config.yaml` for the skills list (use `pyyaml` — install if needed)
   
   b. For each skill entry:
      - Read the SKILL.md file
      - If the skill directory contains supporting files (subdirectories with .md files), bundle them appropriately for the Skills API
      - Upload via `POST /v1/skills`
      - Record the returned skill ID
   
   c. Support these modes:
      - `--all` — upload all skills from the manifest
      - `--path ./skills/patientsim/` — upload a single skill
      - `--list` — show current skills in the API
      - `--delete <skill_id>` — remove a skill (for cleanup)
   
   d. Write all skill IDs to `deploy/skill-ids.json`:
   ```json
   {
     "skill_healthsim_patientsim_v1": "skill_01abc...",
     "skill_healthsim_membersim_v1": "skill_01def...",
     ...
   }
   ```

   e. Support idempotent updates — if a skill already exists (by name), update it rather than creating a duplicate.

3. **Test with the existing common skill** (already uploaded in Phase 0):
   ```bash
   .venv/bin/python deploy/push-skills.py --path ./skills/common/
   ```
   Should update the existing skill, not create a duplicate.

4. **Git commit**: "feat: expand push-skills.py for full manifest-driven upload"

## Deliverables

- Updated `deploy/push-skills.py` with full manifest support
- Tested with existing skill (update, not duplicate)
- Committed

## Note

Don't upload all skills yet — the other skills need adaptation first (p2-02 through p2-04). This prompt only builds the tool.
