# Generative Framework Initiative

**Status:** Ready for Implementation  
**Timeline:** 4-6 weeks (8-12 sessions)  
**Version:** 1.0

---

## Overview

The Generative Framework extends HealthSim with a two-phase architecture for data-driven generation of synthetic healthcare populations and their journeys over time.

**Phase 1 - Specification Building (Creative):** Conversational tools (Profile Builder, Journey Builder) that gather requirements and construct specifications through natural language.

**Phase 2 - Execution (Mechanical):** Deterministic executors that transform specifications into actual entities, coordinating across products.

---

## Documents

| Document | Purpose |
|----------|---------|
| [GENERATIVE-FRAMEWORK-MASTER-PLAN.md](GENERATIVE-FRAMEWORK-MASTER-PLAN.md) | **START HERE** - Complete implementation plan with phases, deliverables, testing |
| [CONCEPTS.md](CONCEPTS.md) | Core concepts: profiles, distributions, journeys, events, triggers |
| [DECISIONS.md](DECISIONS.md) | Design decisions and rationale |
| [PROFILE-BUILDER-SPEC.md](PROFILE-BUILDER-SPEC.md) | Profile Builder 4-phase conversation flow |
| [TAXONOMY.md](TAXONOMY.md) | Mental model and terminology reference |

> **Note:** Visual architecture diagrams will be added during Phase 1 implementation.

---

## Quick Reference

### What Gets Built

```
skills/generation/
├── builders/           # Profile & Journey specification tools
├── executors/          # Specification execution
├── distributions/      # Statistical distribution patterns
├── journeys/           # Journey pattern templates
└── templates/          # Pre-built profiles and journeys
    ├── profiles/
    └── journeys/
```

### Session Progress

| Phase | Sessions | Status |
|-------|----------|--------|
| Phase 0: Foundation | 1 | ⬜ Not Started |
| Phase 1: Profile Builder | 2-3 | ⬜ Not Started |
| Phase 2: Journey Builder | 4-5 | ⬜ Not Started |
| Phase 3: Executors | 6-7 | ⬜ Not Started |
| Phase 4: Integration | 8-10 | ⬜ Not Started |

### Session Logs

Session logs will be stored in [sessions/](sessions/) as work progresses.

---

## Key Principles

1. **Skills-First:** All knowledge in Skills, not Python code
2. **Conversation-Driven:** Configuration via natural language
3. **Consistent Architecture:** Uniform patterns across all products
4. **Test-Driven:** Automated validation at every stage
5. **Documentation Excellence:** Every file documented, linked, navigable

---

*Last Updated: January 3, 2026*
