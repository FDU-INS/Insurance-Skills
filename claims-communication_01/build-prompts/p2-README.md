# Phase 2 — Skills Adaptation & Upload

## Context

Phase 1 delivered a working MCP server on Railway connected to MotherDuck. Phase 2 adapts all 9 skills for the Skills API and uploads them. Each skill needs three changes: replace embedded data refs with MCP tool calls, add output format sections, and bundle multi-file skills.

Run `/clear` between prompts. Run `/compact` mid-prompt only if context exceeds 50%.

## Prompts

| # | File | Title | Effort |
|---|------|-------|--------|
| p2-01 | p2-01-push-skills-full.md | Expand push-skills.py for all skills | 30 min |
| p2-02 | p2-02-adapt-populationsim.md | Adapt populationsim skill (hardest) | 45 min |
| p2-03 | p2-03-adapt-product-skills.md | Adapt patientsim, membersim, rxmembersim, trialsim | 45 min |
| p2-04 | p2-04-adapt-remaining.md | Adapt networksim, common, generation, formats | 30 min |
| p2-05 | p2-05-upload-all.md | Upload all skills and verify | 20 min |

## Prerequisites

- Phase 1 complete — MCP server on Railway, MotherDuck data migrated
- `deploy/push-skills.py` exists (minimal version from Phase 0)
