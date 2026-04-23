# p3-04: Run Full Validation Checklist

## What to build

Systematically validate that the Managed Agent works correctly for all core HealthSim workflows. This is the acceptance test for Phases 0-3.

## Tasks

Run each test via the Console UI or start-session.py. Record pass/fail for each.

1. **MCP Server Connectivity**
   - Prompt: "List my saved cohorts"
   - Expected: Agent calls `healthsim_list_cohorts`. May return empty list — that's fine. Proves MCP connectivity.

2. **Reference Data Access**
   - Prompt: "What is the diabetes prevalence in San Diego County?"
   - Expected: Agent calls `healthsim_query_reference` and returns CDC PLACES data from MotherDuck.

3. **Provider Search**
   - Prompt: "Find cardiologists in San Diego, California"
   - Expected: Agent calls `healthsim_search_providers` and returns real NPPES provider data.

4. **Patient Generation**
   - Prompt: "Generate a small cohort of 5 diabetic patients in San Diego County"
   - Expected: Agent follows patientsim skill patterns, uses generation MCP tools, produces patient records.

5. **Claims Generation**
   - Prompt: "Generate professional claims for the patients you just created"
   - Expected: Agent follows membersim skill patterns, produces claims data linked to the cohort.

6. **Format Knowledge**
   - Prompt: "Show me what CDISC SDTM format looks like for the patient demographics"
   - Expected: Agent references formats skill, produces correctly structured SDTM output.

7. **Cohort Persistence**
   - Prompt: "Save this cohort as 'validation-test'"
   - Then in a NEW session: "Load the cohort called 'validation-test'"
   - Expected: Cohort persists in MotherDuck across sessions.

8. **Skills Loading**
   - Prompt: "Explain how HealthSim generates realistic clinical timelines for patients"
   - Expected: Agent draws on generation framework skill knowledge, not generic responses.

9. **Error Handling**
   - Prompt: "Generate a cohort of 1 million patients" (intentionally too large)
   - Expected: Agent handles gracefully — either sets reasonable limits or explains constraints.

## Document Results

Update `deploy/spike-results.md` with a Phase 3 Validation section:

```markdown
## Phase 3 Validation — [date]

| # | Test | Result | Notes |
|---|------|--------|-------|
| 1 | MCP connectivity | PASS/FAIL | |
| 2 | Reference data | PASS/FAIL | |
| 3 | Provider search | PASS/FAIL | |
| 4 | Patient generation | PASS/FAIL | |
| 5 | Claims generation | PASS/FAIL | |
| 6 | Format knowledge | PASS/FAIL | |
| 7 | Cohort persistence | PASS/FAIL | |
| 8 | Skills loading | PASS/FAIL | |
| 9 | Error handling | PASS/FAIL | |
```

## Git commit

"test: Phase 3 validation checklist results"

## If Tests Fail

- MCP failures → check Railway logs, verify MCP token matches between agent config and Railway env vars
- Data failures → verify MotherDuck tables have correct schemas and data
- Skill failures → check skill upload status, verify skill IDs in agent definition match skill-ids.json
- Generation failures → check if the generation engine modules are accessible to the MCP server on Railway
