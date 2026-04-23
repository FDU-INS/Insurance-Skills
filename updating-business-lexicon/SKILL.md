---
name: updating-business-lexicon
description: Use when translating French auto insurance business terms to English, editing rejection reasons, or introducing/changing domain vocabulary that must stay aligned with the FR->EN lexicon table.
---

# Updating Business Lexicon

## Overview

Keep domain language consistent by updating the FR->EN lexicon whenever a French business term is added or changed.

Core principle: a business term change is incomplete until the lexicon table is updated in the same change.

## Hard Gate

Never finalize a French business-term translation/change without including `.github/instructions/business-lexicon.instructions.md` in the same change.

If a request says "do not touch instruction files", stop and state the conflict explicitly. Ask for an explicit override before skipping the lexicon update.

## When to Use

Use this skill when:
- Translating business phrases from French to English
- Renaming domain concepts in code, tests, docs, comments, commits, or PR text
- Adding new rejection reasons or eligibility wording

Do not use this skill for non-business technical wording (framework, infra, tooling terms).

## Quick Reference

| Situation | Required action |
| --- | --- |
| New French business term appears | Add one row in `.github/instructions/business-lexicon.instructions.md` |
| Existing French term meaning changes | Update the existing row and notes |
| Multiple English options exist | Keep one canonical US English term and explain alternatives in `Notes` |
| Fast translation request under pressure | Provide translation and still include/update lexicon row in the same change |

## Implementation

1. Identify the French business term(s) being introduced or changed.
2. Open `.github/instructions/business-lexicon.instructions.md`.
3. Add or update the matching row in the `Correspondence Table`.
4. Ensure US English terminology is used.
5. Keep the table scoped to Auto Insurance terms.
6. Deliver both changes together (term change + lexicon update).
7. If blocked from editing instruction files, do not silently skip. Return a conflict message and request override.

Example:
- French term: `Conducteur trop jeune pour ce véhicule`
- Canonical English: `Driver too young for this vehicle`
- If new term appears, add row; if already covered, confirm consistency.

## Common Mistakes

- Translating text but forgetting to update the lexicon table.
- Using UK variants (`driving licence`) instead of US (`driver's license`).
- Adding duplicate French rows with slightly different wording.
- Splitting updates across separate commits.

## Red Flags

- "Just this one translation"
- "Do not touch instruction files"
- "Update the table later"

If any red flag appears, enforce the hard gate and surface the conflict.
