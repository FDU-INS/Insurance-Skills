---
name: insurance-construction
description: >
  Analyze, draft, and review Insurance clauses for Construction contracts.
  Use when the user mentions insurance clause, coverage requirements, construction insurance, or asks to review, redline,
  or generate this clause type. Returns structured risk assessment,
  plain-language summary, and suggested alternative language.
---

# Insurance Clause -- Construction

This skill provides expert-level analysis and drafting assistance for
**Insurance** clauses in **Construction** contracts.

---

## When to Activate

Activate this skill when the user:

- Uploads or pastes a contract containing a Insurance clause
- Asks to **draft**, **redline**, or **improve** a Insurance clause
- Asks for a **risk assessment** of an existing Insurance provision
- Mentions keywords: *insurance clause, coverage requirements, construction insurance*

---

## Workflow

### Step 1 -- Intake

Ask the user (if not already provided):

1. **Which party** are you representing? *(e.g., vendor, client, buyer, seller)*
2. **Jurisdiction** governing the contract? *(e.g., New York, California, England & Wales)*
3. **Is this a draft for review or should I generate fresh language?**

### Step 2 -- Analysis

If reviewing existing language, output the following structure:

```
## Insurance Clause Analysis

### Plain-Language Summary
[2-3 sentence plain-English description of what the clause does]

### Key Provisions Identified
- [Provision 1]
- [Provision 2]

### Risk Assessment
| Item | Risk Level | Notes |
|------|-----------|-------|
| [item] | High / Medium / Low | [explanation] |

### Recommended Redlines
[Specific suggested changes with rationale]

### Market Standard Comparison
[How this clause compares to typical Construction market standard]
```

### Step 3 -- Drafting

If generating new language, produce:

1. **Balanced version** (neither party-favored)
2. **Favorable to client** version
3. **Negotiation notes** -- what the other side will likely push back on

---

## Insurance Playbook -- Construction

> See `scripts/playbook.md` for detailed clause-specific guidance,
> fallback positions, jurisdiction-specific notes, and precedent language.

---

## Important Notes

- Always caveat that output is not legal advice and should be reviewed by qualified counsel.
- Flag any provisions that may be unenforceable or jurisdiction-specific.
- When jurisdiction is unknown, apply general common-law principles and note assumptions.
