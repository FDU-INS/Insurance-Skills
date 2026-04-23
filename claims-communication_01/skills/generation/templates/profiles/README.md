# Profile Templates

Pre-built population profiles for common healthcare cohorts.

## Available Templates

| Template | Population | Products | Key Features |
|----------|------------|----------|--------------|
| [medicare-diabetic.md](medicare-diabetic.md) | Medicare Type 2 DM | PatientSim, MemberSim | Age 65+, standard comorbidities |
| [commercial-healthy.md](commercial-healthy.md) | Commercial employer | PatientSim, MemberSim | Age 22-64, low chronic burden |
| [medicaid-pediatric.md](medicaid-pediatric.md) | Medicaid/CHIP children | PatientSim, MemberSim | Age 0-17, SDOH factors |
| [commercial-maternity.md](commercial-maternity.md) | Pregnancy | PatientSim, MemberSim | Prenatal through postpartum |
| [medicare-advantage-complex.md](medicare-advantage-complex.md) | MA high-risk | PatientSim, MemberSim, RxMemberSim | 3+ chronic conditions |

## Quick Start

### Use Default Template
```
Use the Medicare diabetic template for 100 patients
```

### Customize Count
```
Use the commercial healthy template for 500 members
```

### Customize Geography
```
Use the Medicaid pediatric template for South Bronx
```

### Combine with Journey
```
Use the Medicare diabetic template with the diabetic first-year journey for 200 patients
```

## Template Customization

All templates support these common customizations:

| Field | Description | Example |
|-------|-------------|---------|
| `count` | Number of entities | 100, 500, 1000 |
| `geography` | Location filter | State, MSA, County |
| `age_range` | Override age distribution | 70-85, 25-45 |
| `condition_prevalence` | Adjust comorbidity rates | HTN: 85%, HLD: 70% |
| `plan_mix` | Coverage distribution | 60% MA, 40% Original |

## Creating New Templates

1. Start with Profile Builder to design
2. Save specification to this directory
3. Follow naming convention: `population-condition.md`
4. Update this README with the new template

---

*Part of the HealthSim Generative Framework Template Library*
