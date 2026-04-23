---
name: context-transfer
description: "Generate a state document (context transfer) that allows any fresh AI instance to resume work without conversation history. Use this skill whenever the user asks to checkpoint, create a state transfer, save state, generate a handoff document, create compaction insurance, or says anything like 'snapshot this', 'create a context transfer', 'checkpoint', 'save state for handoff', 'write a recovery doc', or 'transfer context'. Also trigger when the user mentions compaction concerns, session handoff, multi-session continuity, or wants to preserve the current conversation's state. Works for any conversation type: projects, research, debugging, investigations, design sessions, or long-running chats. This skill produces a structured markdown document optimized for AI cold-start recovery, not human notes."
---

# Context Transfer

Generate structured state documents for AI cold-start recovery across any conversation type.

## When To Use

- User asks to checkpoint, snapshot, or save state
- Session is getting long and compaction insurance is needed
- Work will continue in a new session (handoff)
- Multi-session work needs persistent state
- User mentions compaction, context loss, or continuity concerns
- Any conversation where accumulated decisions, findings, or state would be costly to lose

## Before Starting

Read the full protocol:
```
Read references/protocol_v2.4s.md
```

This contains the complete section definitions, templates, rules, and quality checklist.

## Quick Reference

The context transfer has 11 sections. Scale to complexity — not every conversation needs all sections.

| Section | Purpose | Required? |
|---------|---------|-----------|
| **I. What This Is** | Identity + "It is NOT" correction | Always |
| **II. Domain Context** | Problem-space briefing | Multi-session+ |
| **III. Architecture** | System structure | Build/engineering work |
| **IV. Decisions** | Numbered with narrative WHY | When decisions exist |
| **V. Current State** | Step sequence or phase summary | Always |
| **VI. Artifacts** | File inventory with status | When files exist |
| **VII. Anti-Drift Warnings** | Observed/predicted failure modes | Multi-session+ |
| **VIII. What NOT To Do** | Catastrophic prohibitions | When applicable |
| **IX. Glossary** | Context-specific terms | Domain-specific |
| **X. Open Questions** | Unresolved issues | When they exist |
| **XI. Recovery Pointer** | Exact restart location + path | Always |

**Minimum viable:** Sections I, V, XI.

## Workflow

1. **Read the protocol** (`references/protocol_v2.4s.md`) — understand all section rules
2. **Assess scope** — use Scaling Guide to determine which sections are needed
3. **Gather state from conversation** — extract decisions, current step, artifacts, open questions
4. **Write each section** following the protocol templates exactly
5. **Apply critical rules:**
   - §I must include "It is NOT..." correction sentence
   - §IV decisions must have narrative WHY (mark `[inferred]` if rationale not explicitly stated)
   - §VII every warning tagged `[observed]` or `[predicted]`
   - §XI must include `Work lives in:` (write `UNKNOWN — ask user` if path not known)
6. **Run Quality Checklist** from protocol
7. **Save to** `/mnt/user-data/outputs/` and present to user

## Output

Save as: `[topic_or_project]_context_transfer.md` in `/mnt/user-data/outputs/`

The document header should include:
```markdown
# Context Transfer — [Topic or Project Name]

**Version:** [N]
**Updated:** [date]
**Purpose:** Compaction insurance. If you just got compacted, read this first.
```

## Key Rules (from protocol)

These are the rules most likely to be missed. Full rules are in the protocol reference.

- **Single source of truth:** One context transfer per conversation/project. Never maintain parallel state docs.
- **Correction sentence:** §I must state what it IS then what it is NOT.
- **Narrative WHY:** §IV uses prose, not tables. Tables compress reasoning too much for cold start.
- **Inferred rationale:** If WHY isn't explicitly stated, mark as `[inferred]` — never present inference as ground truth.
- **Tag all warnings:** §VII requires `[observed]` or `[predicted]` on every warning. No untagged.
- **Never fabricate paths:** §XI `Work lives in:` must be real or `UNKNOWN — ask user`.
- **Update immediately:** Write to file after each decision/state change. Don't batch.

## Notes

- This skill is validated across Claude, GPT, and Gemini cold instances (n=5 tests, zero operational failures)
- The protocol is model-agnostic — works without cognitive scaffolding
- Optimized for AI pattern recognition, not human readability
- The context transfer IS the conversation's memory — treat it as critical infrastructure
