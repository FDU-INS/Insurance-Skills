# p2-03: Adapt Product Skills (patientsim, membersim, rxmembersim, trialsim)

## What to build

Adapt the four main product skills for the Skills API. These are simpler than populationsim — they have supporting scenario/domain files but less embedded data.

## Context

Each of these skills has a SKILL.md plus supporting markdown files that describe scenarios, domains, or configurations. The adaptation pattern is the same for all four:
1. Replace any embedded data or file references with MCP tool calls
2. Add an output format section
3. Bundle supporting files for Skills API upload

## Tasks

1. **For each of these four skills**, repeat this process:

   a. Read the skill directory:
   ```bash
   ls skills/patientsim/
   cat skills/patientsim/SKILL.md | head -50
   ```

   b. Search for embedded data references (file paths, inline data, local file instructions):
   ```bash
   grep -r "skills/" skills/patientsim/
   grep -r "\.csv\|\.json\|data/" skills/patientsim/
   ```

   c. Replace any embedded data references with MCP tool references. Most of these skills reference MCP tools already (they were designed for Claude Code's MCP integration). The main change is ensuring references use the tool names rather than file paths.

   d. Add an Output Formats section with appropriate artifact types:
   
   **patientsim**: `patient_cohort_result`, `encounter_timeline`, `clinical_summary`
   **membersim**: `claims_summary`, `enrollment_report`, `accumulator_snapshot`
   **rxmembersim**: `prescription_summary`, `formulary_coverage`, `dur_alert_report`
   **trialsim**: `trial_enrollment`, `sdtm_domain_result`, `protocol_summary`

2. **Test each adapted skill locally** in Claude Code. Quick smoke test for each:
   - patientsim: "Generate a 5-patient diabetic cohort"
   - membersim: "Generate claims for a small health plan"
   - rxmembersim: "Generate pharmacy claims for 5 members"
   - trialsim: "Generate a Phase 2 oncology trial with 10 subjects"

3. **Git commit after each skill** or batch all four:
   "refactor: adapt product skills for Skills API — patientsim, membersim, rxmembersim, trialsim"

## Deliverables

- All four skills adapted with MCP tool references and output format sections
- Each skill smoke-tested locally
- Committed
