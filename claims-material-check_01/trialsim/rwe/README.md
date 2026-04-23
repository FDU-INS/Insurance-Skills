# Real World Evidence (RWE) Skills

Generate synthetic real world data for external control arms, treatment pathway analysis, and hybrid study designs.

## Available RWE Skills

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [overview.md](overview.md) | RWE concepts and regulatory context | "RWE", "real world", "external data" |
| [synthetic-control.md](synthetic-control.md) | External control arm generation | "synthetic control", "external control" |

## What is RWE in TrialSim?

RWE in TrialSim is the **convergence point** for all HealthSim products:

```
PatientSim (EMR/clinical data)
        +
MemberSim (claims data)
        +
RxMemberSim (pharmacy data)
        =
External Control Population (matched to trial)
```

## Current Scope

**In Scope (v1):**
- Synthetic external control arms for single-arm trials
- Baseline characteristic matching
- Propensity score methodology
- Cross-product data integration

**Deferred:**
- Full observational study generation
- Comparative effectiveness research
- Post-marketing surveillance

## Cross-References

- [Clinical Trials Domain](../clinical-trials-domain.md) - Trial design concepts
- [PatientSim](../../patientsim/SKILL.md) - Source clinical data
- [MemberSim](../../membersim/SKILL.md) - Source claims data
