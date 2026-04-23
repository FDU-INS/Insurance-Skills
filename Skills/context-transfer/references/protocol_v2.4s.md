# Context Transfer Protocol

**Version:** 2.4s
**Purpose:** State document enabling any fresh instance to resume work without conversation history. Optimized for cold start — compaction recovery, session handoff, new instance onboarding.

**Design principle:** K for the next instance, not notes for the human. Optimize for AI pattern recognition and fast orientation.

---

## When To Use

- **Compaction recovery:** Context window compressed mid-chat
- **Session handoff:** Work continues in new chat
- **Multi-session projects:** State persists across sessions
- **Single-session checkpoint:** Insurance against context loss

**Single source of truth:** One context transfer per project. Never maintain parallel state documents — sync drift between them is how compaction kills you. If a separate checkpoint exists, merge it in and retire it.

---

## Required Sections

### I. What This Is

2-4 sentences. What are we building? For whom? End state?

**Then immediately state what it is NOT** — targeting the specific misunderstanding drift or compaction would cause.

```markdown
## What This Is

Building [deliverable] for [who]. The [deliverable] is [what it actually is].
It is NOT [the most likely misunderstanding]. [One sentence on end-state.]
```

**Correction sentence examples:**
- "K is for Claude, not for attorneys. Attorneys never open this file."
- "This is a testable architecture, not a theoretical framework. Files exist. Next step is execution."

---

### II. Domain Context

Enough for a fresh instance to understand the problem space — a briefing, not a textbook.

**Include:** The domain, key operational concepts, non-obvious constraints, core method/approach with absolute rules.

**Scale to complexity:**
- Simple task: 2-3 sentences
- Code project: Problem the code solves, not the code itself. Technical environment → §III.
- Domain-specific: Full subsection with terminology
- R&D: Enough theoretical context to evaluate results against hypotheses
- Multi-phase: Strategic frame

**Test:** Could a fresh instance correctly classify what matters vs. noise in a new document from this domain?

---

### III. Architecture / Structure

How pieces fit together. What the system looks like.

**Include:** Component list/diagram, what each does (one line), data/work flow, what's built vs. planned.

**Adapt to project type:**
- Software: Component architecture, data flow, language/framework, dependencies, file structure, how to run/test
- Research: Investigation structure, evidence chain
- Writing: Document structure, section purposes
- Pipeline: Stages, inputs, outputs, handoffs

**Skip if:** "What This Is" already covers structure.

---

### IV. Decisions

Numbered. Each with explicit WHY — narrative format, not table columns. Tables compress reasoning too much for cold start.

The WHY is what compaction destroys. Conclusions survive summaries; rationale doesn't.

```markdown
### D[N]: [Decision statement]
**Why:** [What failed or was rejected. What alternative was considered.
What would go wrong if reversed.]
```

**Rules:**
- Every decision gets a Why
- Why includes what was rejected and/or what failure prompted it
- If brief doesn't state why, mark as `[inferred]` — do not present inferred rationale as ground truth
- Override notation: "Overrides D[N]"
- Append new decisions — don't edit old ones
- Group by domain if decisions span multiple areas

---

### V. Current State

Where are we? What's done, what's next, what's blocked?

**Multi-phase — execution sequence:**

```markdown
Step  1: [Task]                    ✅ DONE
Step  2: [Task]                    ✅ DONE
Step  3: [Task]                    ← CURRENT
Step  4: [Task]
```

**Simple — phase summary:**

```markdown
**Phase:** [Current phase]
**Done:** [What's complete]
**Next:** [What happens next]
**Blocked:** [If anything]
```

Include test/validation results if applicable — what worked, what failed, what needs fixing.

---

### VI. Artifacts

| File | Purpose | Status |
|------|---------|--------|
| [filename] | [what it does] | ✅ Complete / 🔧 Draft / ❌ Retired |

Mark retired artifacts explicitly — a fresh instance might find them and think they're current.

---

### VII. Anti-Drift Warnings

**Most important section for cold start.** Each warning targets a specific, observed failure.

```markdown
If you're reading this after compaction or cold start:

1. **[The specific mistake you'll make].** [What you'll think → what's actually true.]
   If you catch yourself [specific behavior] → stop, reread D[N].
```

**Tag every warning** as `[observed]` or `[predicted]`. No untagged warnings.

- **`[observed]`:** Actual failure from this project. Sharpen the behavioral tell from experience.
- **`[predicted]`:** No failure history yet — most likely drift for this project type. Convert to `[observed]` as failures occur.

Each warning names the decision it protects, includes a behavioral tell, ordered by likelihood/severity. Minimum 3.

---

### VIII. What NOT To Do

Explicit prohibitions — absolute rules, not behavioral tells.

```markdown
1. **Never** [prohibited action] — [why catastrophic]
```

**Distinct from §VII:** Warnings catch drift (gradual). Prohibitions prevent catastrophic errors (discrete). If unsure → put in warnings. Reserve prohibitions for catastrophic and irreversible.

**Skip if:** No catastrophic failure modes exist.

---

### IX. Glossary

| Term | Meaning |
|------|---------|
| [Term] | [Operational definition in THIS project] |

**Scale:** General project → skip or 3-5 terms. Domain-specific → 10-20. Custom vocabulary → as needed.

**Skip if:** All terms are common knowledge for the target AI.

---

### X. Open Questions

| Question | What Would Answer It | Priority |
|----------|---------------------|----------|
| [Issue] | [Evidence or action needed] | High/Med/Low |

**Skip if:** No open questions. Don't fabricate.

---

### XI. Recovery Pointer

```markdown
**You are HERE:** [Section] → [Step] → [Task].
**Work lives in:** [repo path, folder, or file location].
**Do THIS next:** [One sentence — immediate next action].
```

Not a summary. One location, one action, one path. If path unknown, write `**Work lives in:** UNKNOWN — ask user`. Never fabricate a path.

Instance reads full document for context, follows this pointer to begin.

---

## Formatting Rules

- Tables for reference data (artifacts, glossary, open questions)
- Execution sequences for multi-step work (numbered + completion markers)
- Correction sentences after identity statements ("It IS X. It is NOT Y.")
- Flag uncertainty explicitly
- Timestamp document header only

---

## Scaling Guide

| Project Type | Required Sections | Optional |
|---|---|---|
| **Quick task** | I, V, XI | IV if decisions made |
| **Single-session investigation** | I, II, IV, V, X, XI | III, VI, VII |
| **Research** (multi-session) | I, II, IV, V, VII, X, XI | III, VI, IX |
| **Multi-session build** | All | — |
| **Domain-specific** | All, especially II and IX | — |

**Minimum viable:** Sections I, V, XI.

---

## Maintenance

**Update when:**
- New decision → §IV
- Decision revised → new entry with "Overrides D[N]"
- State changes → §V
- New drift pattern → §VII
- Artifact created/retired → §VI

Write to file immediately. Don't batch — compaction doesn't wait.

Version the document header on each meaningful update.

---

## Quality Checklist

- [ ] Fresh instance with zero history can resume from this alone?
- [ ] §I includes correction sentence ("it is NOT...")?
- [ ] All decisions have narrative WHY?
- [ ] §VII: every warning tagged `[observed]` or `[predicted]`?
- [ ] §V reflects actual state?
- [ ] Retired artifacts marked in §VI?
- [ ] §XI points to one specific next action?
- [ ] Exactly ONE context transfer for this project?
