---
name: reviewing-business-terminology
description: Use when reviewing pull requests or code changes that modify business wording, translations, rejection reasons, or eligibility terms in the auto insurance domain.
---

# Reviewing Business Terminology

## Overview

Review business-language changes for consistency, not just code correctness.

Core principle: a wording change is incomplete if the FR->EN lexicon is not updated in the same change set.

## When to Use

Use this skill when:
- Reviewing PRs that change domain messages or labels
- Reviewing translations between French and English business terms
- Reviewing eligibility/rejection wording in Application, Domain, tests, docs, or PR text

Do not use this for purely technical refactors with no business language change.

## Quick Reference

| Check | Pass criteria |
| --- | --- |
| Lexicon sync | `.github/instructions/business-lexicon.instructions.md` updated in same change when terms changed |
| Canonical translation | English term matches existing canonical entry in table |
| US terminology | Uses US wording consistently |
| Cross-file consistency | Same term used consistently across code/tests/docs |
| Regression risk | Assertions/messages updated where wording changed |

## Implementation

1. Detect whether business wording changed.
2. Compare changed terms against `.github/instructions/business-lexicon.instructions.md`.
3. If missing or inconsistent, raise a blocking finding.
4. Check for inconsistent synonyms across changed files.
5. Confirm tests and expected messages were updated when wording changed.
6. Report findings ordered by severity with file references.

## Blocking Findings Template

- `HIGH`: Lexicon not updated in same change after business-term modification.
- `MEDIUM`: Non-canonical translation conflicts with existing table entry.
- `MEDIUM`: Inconsistent wording across files can cause behavior/docs drift.
- `LOW`: US terminology style mismatch without functional impact.

## Common Mistakes

- Approving translation changes without lexicon-table updates.
- Treating wording changes as cosmetic even when tests/assertions depend on exact messages.
- Mixing near-synonyms for the same domain concept across layers.

## Red Flags

- "Text-only change, safe to skip"
- "We can align the lexicon later"
- "Translation is obvious, no need to check table"

If any red flag appears, produce at least one explicit terminology check before approving.
