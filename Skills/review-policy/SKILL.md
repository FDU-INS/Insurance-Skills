---
name: review-policy
description: "Review policy drafts for clarity, completeness, cross-policy consistency, and regulatory accuracy before approval"
license: MIT
allowed-tools: Read
metadata:
  author: "redline-team"
  version: "1.0.0"
  category: "compliance"
  risk_tier: "high"
---

# Review Policy

## Purpose

Independently review a policy draft to verify quality, consistency with other organizational policies, and correctness of regulatory references. This skill is executed by the **reviewer** agent (checker role) and must never be performed by the same agent that drafted the policy.

## Inputs

- **Draft policy path**: path to the updated policy file
- **Original policy path**: path to the previous version (or same path if reviewing in-place changes)
- **Change summary**: the change summary produced by the draft-policy skill

## Instructions

1. **Read the draft policy** from the specified path.

2. **Read ALL other policies** in the `policies/` directory. This is essential for cross-policy consistency checking.

3. **Evaluate the draft on five dimensions:**

### Dimension 1: Clarity
- Is the language unambiguous? Could a non-expert employee follow the policy?
- Are responsibilities clearly assigned to specific roles (not "the team" or "management")?
- Are processes actionable with concrete steps, not just aspirational statements?
- Are terms defined where they might be ambiguous?

### Dimension 2: Completeness
- Do the changes address every gap identified in the change summary?
- Are there any REDLINE comments referencing requirements that aren't fully addressed?
- Are there placeholder decisions (`[DECISION REQUIRED]`) that need human input before the policy is complete?

### Dimension 3: Consistency with Other Policies
- Does any new language contradict existing policies in the `policies/` directory?
- Common contradiction areas:
  - BYOD rules in acceptable-use vs. device restrictions in access-control
  - Retention periods in data-privacy vs. deletion timelines in other policies
  - Incident reporting timelines across different policies
  - Access control requirements that conflict between policies
- If a contradiction is found, flag it with both policy references and the specific conflicting statements.

### Dimension 4: Regulatory Accuracy
- Are regulation citations correct? (e.g., does the text attributed to "GDPR Article 22" actually reflect what Article 22 says?)
- Read the relevant `knowledge/frameworks/` requirements to verify claims
- Are regulatory requirements accurately represented — not weakened or overstated?

### Dimension 5: Structural Integrity
- Does the new content follow the existing document's formatting and numbering?
- Are REDLINE comments properly placed on all new/changed sections?
- Is the table of contents / section numbering still consistent?

4. **Produce a review decision:**

## Output Format

```
## Policy Review: [Policy Name]

**Reviewed by**: reviewer (checker role)
**Date**: [date]
**Decision**: APPROVED / APPROVED WITH COMMENTS / REJECTED

### Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Clarity | PASS / NEEDS WORK | [brief note] |
| Completeness | PASS / NEEDS WORK | [brief note] |
| Cross-Policy Consistency | PASS / CONFLICT FOUND | [brief note] |
| Regulatory Accuracy | PASS / INACCURACY FOUND | [brief note] |
| Structural Integrity | PASS / NEEDS WORK | [brief note] |

### Findings

[List each finding with line/section reference]

### Contradictions Found

[If any, list the specific conflicting statements across policies]

### Decision Rationale

[Why approved or rejected — specific reasons]
```

## Decision Rules

- **APPROVED**: All dimensions PASS, no contradictions, no inaccuracies
- **APPROVED WITH COMMENTS**: Minor issues that don't affect compliance (formatting, clarity improvements). Comments should be addressed but are not blocking.
- **REJECTED**: Any regulatory inaccuracy, any cross-policy contradiction, any gap from the change summary not addressed, or any critical clarity issue that could lead to misinterpretation
