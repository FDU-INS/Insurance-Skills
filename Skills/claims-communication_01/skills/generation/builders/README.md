# Builders

Specification building tools for defining what to generate.

## Overview

Builders guide users through creating **specifications** - structured definitions of the data they want. These specifications are then passed to Executors for actual generation.

## Skills in This Category

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [profile-builder.md](profile-builder.md) | Build population profiles | "Create a cohort of...", "Generate 100 members..." |
| [journey-builder.md](journey-builder.md) | Define event sequences | "Add a timeline...", "With monthly visits..." |
| [quick-generate.md](quick-generate.md) | Fast single-entity generation | "Give me a patient...", "Quick, generate..." |

## Workflow

```
User Request
    │
    ▼
┌─────────────────────┐
│   Quick Generate?   │──── Yes ───► Generate immediately (1-10 entities)
│   (simple request)  │
└─────────────────────┘
    │ No
    ▼
┌─────────────────────┐
│   Profile Builder   │──► 4-phase conversation ──► ProfileSpecification
│                     │    1. Intent recognition
│                     │    2. Profile selection
│                     │    3. Refinement loop
│                     │    4. Confirmation
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│   Journey Builder   │──► Timeline definition ──► JourneySpecification
│   (optional)        │    - Events by time
│                     │    - Branching rules
│                     │    - Cross-domain triggers
└─────────────────────┘
    │
    ▼
    ProfileSpecification + JourneySpecification ──► Executor
```

## Quick Start

### Simple Request → Quick Generate
```
"Generate a 65-year-old diabetic patient"
```

### Complex Request → Profile Builder
```
"I need 200 Medicare members with:
- Age 65-85
- Type 2 diabetes
- Hypertension comorbidity
- Texas geography"
```

### With Timeline → Add Journey Builder
```
"...and give them a first-year diabetes management journey"
```

## Related Categories

- [Executors](../executors/) - Execute specifications
- [Templates](../templates/) - Pre-built profiles and journeys
- [Distributions](../distributions/) - Customize statistical patterns

---

*Part of the HealthSim Generative Framework*
