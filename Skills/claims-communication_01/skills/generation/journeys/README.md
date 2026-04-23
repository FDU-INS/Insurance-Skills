# Journey Patterns

Temporal event sequence patterns for healthcare data generation.

## Overview

Journey patterns define how events unfold over time. They range from simple linear sequences to complex branching protocols with conditional logic.

## Skills in This Category

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [journey-patterns.md](journey-patterns.md) | All pattern types and usage | Designing any temporal sequence |

## Pattern Types

| Pattern | Complexity | Use Case | Example |
|---------|------------|----------|---------|
| **Linear** | Simple | Fixed sequence of events | Annual wellness visits |
| **Branching** | Medium | Decision-based paths | ER → Admit OR Discharge |
| **Cyclic** | Medium | Repeating events | Monthly refills, quarterly visits |
| **Protocol** | High | Clinical trial schedules | Cycle 1 Day 1, Day 8, Day 15 |
| **Lifecycle** | High | Multi-year progressions | Disease progression over years |

## Quick Reference

### Linear Pattern
```
Day 0 ──► Week 2 ──► Week 6 ──► Week 12
 │          │          │          │
Visit 1   Visit 2   Visit 3   Visit 4
```

### Branching Pattern
```
          ┌─── Admit ───► Inpatient stay ───► Discharge
ER Visit ─┤
          └─── Discharge ───► Follow-up in 3 days
```

### Cyclic Pattern
```
          ┌────────────────────────────────┐
          │                                │
          ▼                                │
Day 0 ──► Day 30 ──► Day 60 ──► Day 90 ───┘
 │          │          │          │
Fill 1    Fill 2    Fill 3    Fill 4
```

### Protocol Pattern
```
Cycle 1                 Cycle 2                 Cycle 3
├─ Day 1: Treatment    ├─ Day 1: Treatment    ├─ Day 1: Treatment
├─ Day 8: Labs         ├─ Day 8: Labs         ├─ Day 8: Labs
└─ Day 15: Assessment  └─ Day 15: Assessment  └─ Day 15: Assessment
     └───────────────────────┘
            21-day cycle
```

## When to Use Each Pattern

| Cohort | Recommended Pattern |
|----------|---------------------|
| Simple follow-up care | Linear |
| ER or urgent care | Branching |
| Medication refills | Cyclic |
| Clinical trial visits | Protocol |
| Chronic disease progression | Lifecycle |
| New member onboarding | Linear + Branching |
| Surgical episode | Linear with phases |

## Related Categories

- [Builders](../builders/) - Journey Builder creates specifications
- [Executors](../executors/) - Journey Executor generates events
- [Templates](../templates/journeys/) - Pre-built journey templates

---

*Part of the HealthSim Generative Framework*
