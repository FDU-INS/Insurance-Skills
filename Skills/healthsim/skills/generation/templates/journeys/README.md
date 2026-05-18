# Journey Templates

Pre-built temporal event sequences for common healthcare cohorts.

## Available Templates

| Template | Duration | Pattern | Products |
|----------|----------|---------|----------|
| [diabetic-first-year.md](diabetic-first-year.md) | 12 months | Linear + Branching | PatientSim, MemberSim, RxMemberSim |
| [surgical-episode.md](surgical-episode.md) | 3 months | Linear with phases | PatientSim, MemberSim |
| [new-member-onboarding.md](new-member-onboarding.md) | 90 days | Linear + Branching | MemberSim, PatientSim |
| [hf-exacerbation.md](hf-exacerbation.md) | 30 days | Branching | PatientSim, MemberSim |
| [oncology-treatment-cycle.md](oncology-treatment-cycle.md) | 6 months | Protocol | PatientSim, MemberSim, TrialSim |

## Quick Start

### Use Standalone Journey
```
Create a diabetic first-year journey for a patient
```

### Attach to Profile
```
Use the Medicare diabetic template with the diabetic first-year journey
```

### Customize Timeline
```
Use the surgical episode journey but extend PT to 12 weeks
```

## Journey Categories

### Chronic Disease Management
- [diabetic-first-year.md](diabetic-first-year.md) - New T2DM diagnosis through stabilization
- [hf-exacerbation.md](hf-exacerbation.md) - Heart failure acute episode

### Episodic Care
- [surgical-episode.md](surgical-episode.md) - Elective surgery pre-op through recovery
- [oncology-treatment-cycle.md](oncology-treatment-cycle.md) - Cancer treatment cycles

### Administrative/Lifecycle
- [new-member-onboarding.md](new-member-onboarding.md) - New plan enrollment journey

## Template Customization

All journey templates support these customizations:

| Field | Description | Example |
|-------|-------------|---------|
| `duration` | Extend or shorten | "18 months", "6 weeks" |
| `visit_frequency` | Adjust encounter frequency | "monthly", "weekly" |
| `complication_rate` | Adjust branching probabilities | "10% hospitalization" |
| `medication_changes` | Modify Rx events | "Add SGLT2 at month 3" |

## Creating New Templates

1. Start with Journey Builder to design
2. Save specification to this directory
3. Follow naming convention: `condition-episode-type.md`
4. Update this README with the new template

---

*Part of the HealthSim Generative Framework Template Library*
