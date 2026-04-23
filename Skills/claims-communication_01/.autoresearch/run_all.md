# HealthSim Workspace — Full Autoresearch Sweep

## What This Does

Runs a single improvement pass across all 7 HealthSim skill domains.
95 total criteria across 7 skills.

**Key difference from BioScience/Vantage**: Most HealthSim skills are
ALREADY over 2000 words. The default mode is TIGHTEN and REFACTOR,
not add. Move detailed content into sub-skill .md files (which have
no word limit) and use freed space for higher-value routing logic.

## Priority Order

1. patientsim (20 criteria — most used, most complex)
2. membersim (15 criteria — claims generation)
3. rxmembersim (15 criteria — pharmacy claims)
4. populationsim (12 criteria — population generation)
5. networksim (12 criteria — provider networks)
6. trialsim (12 criteria — clinical trials)
7. generation (9 criteria — generation engine)

## Per-Skill Steps

For each skill:

**Step 1: Read the skill and eval**
```
Read skills/{skill}/SKILL.md
Read .autoresearch/{skill}/program.md
Read .autoresearch/{skill}/evaluate.py
```

**Step 2: Check word count**
```bash
wc -w skills/{skill}/SKILL.md
```
Most HealthSim skills are 2000-2500 words — OVER the recommended limit.
Use the saturated strategy below for any skill over 1900 words.

**Step 3: Identify the biggest gap**

Based on eval criteria, which category scores lowest? Common gaps:
- Missing safety guardrails (all data is synthetic, no clinical advice)
- Missing negative examples (invalid code formats, unrealistic data)
- Weak code system references (ICD-10, CPT, LOINC, RxNorm, NDC)
- Missing edge case handling (partial data, missing fields)
- Verbose content that could move to sub-skill files

**Step 4: Make ONE improvement**

CONSTRAINTS:
- Target 2000 words or fewer (most skills need trimming, not adding)
- Preserve frontmatter name and triggers
- One change per skill per pass
- Prefer tightening over adding

**Step 5: Test**
```bash
.venv/bin/python3 -m pytest packages/core/tests/ -q --tb=short -x
```
If ANY test fails → `git checkout skills/{skill}/SKILL.md` → skip.

**Step 6: Commit**
```bash
git add skills/{skill}/
git commit -m "feat({skill}): [brief description]"
```

**Step 7: Move to next skill**

## Strategy for Saturated Skills (1900+ words) — DEFAULT MODE

Most HealthSim skills are over 2000 words. For these:

**Tighten existing language (highest priority):**
Replace verbose phrases with precise ones. Remove redundant
explanations. HealthSim skills tend to have long prose sections
that can be shortened without losing information.

**Move detail to sub-skill files:**
Each HealthSim skill directory already has sub-skill .md files
(e.g., patientsim/diabetes-management.md, membersim/facility-claims.md).
Move detailed tables, worked examples, and protocol descriptions
there. Replace with concise pointers.

**Add high-value content in freed space:**
Once trimmed, use freed space for safety guardrails, negative
examples, or edge case handling — the gaps the eval tests.

When refactoring:
```bash
git add skills/{skill}/
git commit -m "refactor({skill}): [what was tightened/moved]"
```

## Stopping Rules

- Skip skills where no meaningful improvement is found
- If 3+ skills fail tests consecutively, stop and report
- When a full sweep produces zero improvements, evals are saturated

## After Sweep

Report summary with word counts before and after:
```
Skill                Action         Change              Words Before → After
──────────────────────────────────────────────────────────────────────────
patientsim           tightened      removed redundant examples    2364 → 1980
membersim            refactored     moved claim detail to subs    2403 → 1850
...
```
