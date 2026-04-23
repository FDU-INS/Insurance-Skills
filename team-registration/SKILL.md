---
name: team-registration
description: "Orchestrate the registration team to guide expats through Anmeldung, Steuer-ID, health insurance, business registration, and other German bureaucratic processes."
argument-hint: "[describe what you need to register or set up]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
---

Orchestrate the registration and bureaucracy team.

## Team Composition

- **intake-specialist** — identifies what the user needs to set up
- **registration-specialist** — provides step-by-step guidance
- **document-drafter** — drafts any cover letters or forms if needed

## Pipeline

### Phase 1: Intake

Identify:
- What stage is the user at? (just arrived / changing status / specific document needed)
- Have they done Anmeldung? (everything else depends on this)
- What specific thing do they need? (Steuer-ID, Gewerbeanmeldung, health insurance, etc.)

### Phase 2: Guidance

Delegate to **registration-specialist** for:
- Step-by-step process
- Documents to bring
- Where to go (specific office, website)
- Realistic timeline
- Common mistakes
- If citing specific fees or procedures, run a quick freshness check per `docs/law-freshness.md` (Registration section) and note the source inline.

### Phase 3: Final Output

```
## Registration Guidance

**What you need to do:** [ordered checklist]
**Where to go:** [specific offices/portals]
**Documents to bring:** [list]
**Timeline:** [realistic expectations]
**Cost:** [fees]
```
