---
name: claim-source-auditor
description: >
  Verify claims, quotes, timelines, and findings against supplied source files and return a source map
  with verified, conflicting, not found, and manual-review statuses. Use when the user asks to fact-check
  a memo, audit, timeline, executive summary, research packet, or project brief against PDFs, XML,
  HTML, notes, screenshots, exported chat logs, or other supplied files before sending, publishing,
  or relying on the result.
---

# Claim Source Auditor

## Objective

Turn a draft or claim set into a traceable evidence map. Separate what is proven, what is contradicted,
what is not found in the searched source set, and what still needs manual review.

## Directives

| Parameter | Requirement |
| --- | --- |
| Formatting | Table-first; each claim gets a discrete status row |
| Tone | Factual, restrained, audit-style |
| Scope | Verification only; do not rewrite the whole narrative unless the verification results require targeted remediation |
| Grounding | Every `verified` or `conflicting` result must trace to a named file, source location, or quoted passage |
| Defaults | Use the fixed status taxonomy and keep unsourced claims unresolved rather than downgraded into speculation |
| Fallback | If search or extraction is partial, return the searched scope, likely matches, and manual-review flags instead of overstating certainty |
| Triggering | Use for source mapping, quote verification, claim checking, contradiction audits, and pre-release fact review |
| Restrictions | Do not treat absence as falsity without naming the searched scope; do not paraphrase a quote as verified unless the exact wording or a faithful equivalent is present |

## Workflow

1. Define the audit scope: claims list, searched sources, and whether exact quotes are required.
2. Break compound paragraphs into individual claims.
3. Search the provided source set for exact wording first, then faithful supporting context.
4. Assign one status per claim: `verified`, `verified in broader bundle`, `conflicting`, `not found in searched sources`, or `manual review needed`.
5. Cite the exact source location when available.
6. Separate remediation notes from evidence status so unsupported claims are easy to fix or remove.

## Resources

| Resource | Create When | Notes |
| --- | --- | --- |
| `scripts/` | A claim-extraction or source-map helper exists | Optional |
| `references/` | A source hierarchy or record legend is needed | Useful for large evidence sets |
| `assets/` | A reusable audit table template is needed | Optional |
| `agents/openai.yaml` | The skill should appear cleanly in the UI | Keep the UI prompt focused on verification |

Preferred status meanings:

- `verified`: supported in the exact searched packet
- `verified in broader bundle`: supported locally, but outside the narrow packet under review
- `conflicting`: the source materially contradicts the draft claim
- `not found in searched sources`: not located in the named search scope
- `manual review needed`: likely present, but extraction, image content, or ambiguity blocks automatic confirmation

## Validation

1. Verify that every claim row names the searched source scope.
2. Verify that every `verified` or `conflicting` row includes a concrete citation or file reference.
3. Verify that every `not found` row distinguishes source absence from search limitation.
4. Remove blended statuses and duplicated claims.
5. Run `scripts/quick_validate.py <path/to/skill-folder>` before delivery.
