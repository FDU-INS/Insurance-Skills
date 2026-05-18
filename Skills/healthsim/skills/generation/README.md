# HealthSim Generative Framework

The Generative Framework provides conversation-driven specification and execution of healthcare data generation at scale. Instead of hardcoded rules, it uses **profile specifications** and **journey definitions** to create realistic, correlated data across all HealthSim products.

## Quick Reference

| Skill Category | Use When | Key Features |
|----------------|----------|--------------|
| [Builders](builders/) | Defining what to generate | Profile builder, journey builder, quick generate |
| [Executors](executors/) | Running specifications | Batch generation, cross-domain sync |
| [Distributions](distributions/) | Customizing statistical patterns | Age, cost, utilization distributions |
| [Journeys](journeys/) | Defining temporal patterns | Linear, branching, protocol, lifecycle |
| [Templates](templates/) | Starting from common patterns | Pre-built profiles and journeys |

## Getting Started

### Quick Generation (Single Entity)

```
Generate a 65-year-old diabetic Medicare member
```

### Profile-Driven Generation (Cohort)

```
Build a profile for 100 commercial members:
- Age 25-45
- Mix of healthy and chronic conditions
- Urban geography
```

### Journey-Driven Generation (Temporal)

```
Create a diabetic first-year journey for 50 patients:
- New diagnosis
- Initial treatment
- Quarterly follow-ups
- Lab monitoring
```

## Architecture

```
                     ┌─────────────────────────┐
                     │   User Conversation     │
                     │   "Generate 100..."     │
                     └───────────┬─────────────┘
                                 │
                     ┌───────────▼─────────────┐
                     │       BUILDERS          │
                     │  Profile / Journey      │
                     │  Specification          │
                     └───────────┬─────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
   ┌────────▼────────┐  ┌───────▼───────┐  ┌────────▼────────┐
   │  Distributions  │  │   Journeys    │  │    Templates    │
   │  (statistical)  │  │  (temporal)   │  │  (pre-built)    │
   └────────┬────────┘  └───────┬───────┘  └────────┬────────┘
            │                   │                    │
            └───────────────────┼────────────────────┘
                                │
                     ┌──────────▼──────────┐
                     │      EXECUTORS      │
                     │  Generate Entities  │
                     │  → DuckDB/MCP       │
                     └──────────┬──────────┘
                                │
     ┌──────────────────────────┼──────────────────────────┐
     │              │           │           │              │
┌────▼────┐  ┌──────▼────┐  ┌───▼───┐  ┌────▼────┐  ┌──────▼────┐
│PatientSim│ │ MemberSim │  │ TrialSim│ │RxMemberSim│ │NetworkSim│
└─────────┘  └───────────┘  └─────────┘ └──────────┘ └───────────┘
```

## Key Concepts

### Profile Specification

A **profile** defines the demographic, clinical, and coverage characteristics of a population:

```json
{
  "profile_name": "Medicare Diabetic Cohort",
  "count": 100,
  "demographics": {
    "age": { "distribution": "normal", "mean": 72, "std_dev": 8 },
    "gender": { "distribution": "categorical", "weights": {"M": 0.48, "F": 0.52} }
  },
  "conditions": [
    { "code": "E11.9", "prevalence": 1.0 },
    { "code": "I10", "prevalence": 0.72 }
  ],
  "coverage": { "type": "Medicare", "plan": "Medicare Advantage" }
}
```

### Journey Specification

A **journey** defines the temporal sequence of healthcare events:

```json
{
  "journey_name": "Diabetic First Year",
  "duration": "12 months",
  "phases": [
    {
      "name": "Diagnosis",
      "duration": "0-30 days",
      "events": ["initial_visit", "labs", "diagnosis", "rx_metformin"]
    },
    {
      "name": "Stabilization", 
      "duration": "30-180 days",
      "events": ["quarterly_visit", "a1c_check", "rx_refills"]
    }
  ]
}
```

## Folder Structure

```
skills/generation/
├── README.md                 # This file
├── SKILL.md                  # Trigger phrases and routing
├── builders/                 # Specification building skills
│   ├── profile-builder.md    # Population profile builder
│   ├── journey-builder.md    # Healthcare journey builder
│   └── quick-generate.md     # Simple entity generation
├── executors/                # Specification execution skills
│   ├── profile-executor.md   # Execute profile specs
│   ├── journey-executor.md   # Execute journey specs
│   └── cross-domain-sync.md  # Cross-product triggers
├── distributions/            # Statistical distribution patterns
│   ├── distribution-types.md # Core distribution types
│   ├── age-distributions.md  # Age patterns
│   └── cost-distributions.md # Cost/utilization patterns
├── journeys/                 # Journey pattern definitions
│   ├── linear-journey.md     # Simple A→B→C
│   ├── branching-journey.md  # Decision-based paths
│   ├── protocol-journey.md   # Trial protocols
│   └── lifecycle-journey.md  # Multi-year patterns
└── templates/                # Pre-built configurations
    ├── profiles/             # Ready-to-use profiles
    │   ├── medicare-diabetic.md
    │   ├── commercial-healthy.md
    │   └── medicaid-pediatric.md
    └── journeys/             # Ready-to-use journeys
        ├── diabetic-first-year.md
        ├── surgical-episode.md
        └── new-member-onboarding.md
```

## Related Skills

- **[PopulationSim](../populationsim/SKILL.md)** - Real-world demographics and SDOH data
- **[NetworkSim](../networksim/SKILL.md)** - Real provider and facility assignments
- **[Common: State Management](../common/state-management.md)** - Cohort persistence
- **[Common: Identity Correlation](../common/identity-correlation.md)** - Cross-product linking

## Design Documents

For detailed design rationale and specifications, see:

- [Generative Framework Concepts](../../docs/initiatives/generative-framework/CONCEPTS.md)
- [Design Decisions](../../docs/initiatives/generative-framework/DECISIONS.md)
- [Profile Builder Specification](../../docs/initiatives/generative-framework/PROFILE-BUILDER-SPEC.md)
- [Master Plan](../../docs/initiatives/generative-framework/GENERATIVE-FRAMEWORK-MASTER-PLAN.md)

---

*The Generative Framework is under active development. See [GENERATIVE-FRAMEWORK-PROGRESS.md](../../docs/GENERATIVE-FRAMEWORK-PROGRESS.md) for status.*
