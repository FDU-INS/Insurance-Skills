# Executors

Execution layer that transforms specifications into actual entities.

## Overview

Executors take approved specifications from Builders and generate the actual healthcare data. They handle distribution sampling, cross-product coordination, and validation.

## Skills in This Category

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [profile-executor.md](profile-executor.md) | Execute profile specifications | After profile approval |
| [journey-executor.md](journey-executor.md) | Execute journey timelines | After journey approval |
| [cross-domain-sync.md](cross-domain-sync.md) | Coordinate multi-product generation | When generating across products |

## Workflow

```
Approved Specification
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                     PROFILE EXECUTOR                        │
│                                                             │
│  1. Validate specification                                  │
│  2. Sample from distributions                               │
│  3. Generate demographic attributes                         │
│  4. Generate clinical attributes                            │
│  5. Generate coverage attributes                            │
│  6. Link to NetworkSim providers (if applicable)            │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                     JOURNEY EXECUTOR                        │
│                                                             │
│  For each entity generated:                                 │
│  1. Expand timeline to absolute dates                       │
│  2. Apply variance                                          │
│  3. Evaluate branching conditions                           │
│  4. Generate events (encounters, labs, Rx, claims)          │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                     CROSS-DOMAIN SYNC                       │
│                                                             │
│  1. Link Patient ↔ Member (identity correlation)            │
│  2. Generate Encounter → Claim                              │
│  3. Generate Prescription → Fill                            │
│  4. Validate referential integrity                          │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
Generated Entities + Validation Report
```

## Execution Modes

| Mode | Description | When to Use |
|------|-------------|-------------|
| **Immediate** | Generate and save | Default for approved specs |
| **Dry Run** | Preview without saving | Validate before committing |
| **Batch** | Generate in chunks | Large populations (>100) |

## Quick Start

### Execute Profile
```
Execute the approved Medicare diabetic profile
```

### Execute with Journey
```
Execute the profile with the diabetic first-year journey
```

### Dry Run
```
Dry run this profile (show what would be generated)
```

## Related Categories

- [Builders](../builders/) - Create specifications
- [Templates](../templates/) - Pre-built specifications
- [Common Skills](../../common/) - State management, DuckDB

---

*Part of the HealthSim Generative Framework*
