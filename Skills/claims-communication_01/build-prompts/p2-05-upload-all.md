# p2-05: Upload All Skills and Verify

## What to build

Upload all 9 adapted skills to the Anthropic Skills API using the expanded push-skills.py script.

## Tasks

1. **Upload all skills**:
   ```bash
   .venv/bin/python deploy/push-skills.py --all
   ```

   This reads `agent-config.yaml`, walks each skill path, and uploads them all. Monitor the output for errors.

2. **Verify all skills uploaded** by listing them:
   ```bash
   .venv/bin/python deploy/push-skills.py --list
   ```

   Confirm all 9 skills appear with correct names:
   - skill_healthsim_patientsim_v1
   - skill_healthsim_membersim_v1
   - skill_healthsim_rxmembersim_v1
   - skill_healthsim_trialsim_v1
   - skill_healthsim_populationsim_v1
   - skill_healthsim_networksim_v1
   - skill_healthsim_common_v1
   - skill_healthsim_generation_v1
   - skill_healthsim_formats_v1

3. **Check `deploy/skill-ids.json`** — all 9 entries should be present with valid skill IDs.

4. **If any uploads failed**, check:
   - File size limits on the Skills API (some skills with many supporting files may be large)
   - Multi-file bundling format — the API may expect a specific structure
   - Document any API limitations discovered in `deploy/spike-results.md`

5. **Git commit**: "feat: upload all 9 adapted skills to Skills API"

## Deliverables

- All 9 skills uploaded and verified
- `deploy/skill-ids.json` complete
- Any issues documented
- Committed

## Phase 2 Complete

At this point:
- ✅ All skills adapted for the Skills API
- ✅ All skills uploaded and accessible via API
- ✅ Local Claude Code development still works with adapted skills
- Ready for Phase 3 (agent assembly)
