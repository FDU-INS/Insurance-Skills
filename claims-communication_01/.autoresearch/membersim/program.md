# MemberSim SKILL.md — Autoresearch Program

## Objective
Maximize pass rate on evaluate.py by optimizing skills/membersim/SKILL.md.

## Target File
`skills/membersim/SKILL.md`

## Eval Levels
- **Level 1 (keyword):** Does the SKILL.md mention the right terms?
- **Level 2 (structural):** Does the SKILL.md have required sections, valid links, word budget?
- **Level 3 (response):** Does Claude produce correct output when guided by this skill?

## Rules
1. One change per experiment.
2. Never modify evaluate.py.
3. Most HealthSim skills are ALREADY over 2000 words — default to tightening
   and refactoring to sub-skill files, not adding content.
4. Preserve frontmatter name and triggers.

## Mutation Strategies

### Level 1 (keyword matching)
1. Tighten verbose language — say the same thing in fewer words
2. Move detailed tables/examples into sub-skill .md files (no word limit)
3. Add safety guardrails if missing (all data is synthetic, no clinical advice)
4. Add negative examples (what NOT to generate)
5. Strengthen code system references (ICD-10, CPT, LOINC, RxNorm, NDC)
6. Add edge case handling (missing fields, invalid codes, partial data)

### Level 2 (structural quality)
7. Add YAML frontmatter with name and description fields
8. Add required sections: Safety Guardrails, Examples, Edge Cases
9. Fix broken markdown links to sub-skill files
10. Ensure word count stays ≤ 2000

### Level 3 (response quality)
11. Add worked JSON examples that demonstrate correct output structure
12. Add clinical coherence rules (medications match diagnoses)
13. Add code validation guidance (use real ICD-10/CPT/LOINC codes, not invented ones)
14. Add temporal ordering rules (diagnosis before treatment, labs after orders)
