---
name: populationsim-cohorts
description: >
  Cohort definition skills for PopulationSim. Use for creating CohortSpecification
  objects that drive synthetic data generation in PatientSim, MemberSim, and
  TrialSim. Combines demographics, clinical profiles, and SDOH characteristics.
---

# Cohort Definition Skills

## Overview

Cohort definition skills create CohortSpecification objects that capture the complete profile of a target population. These specifications drive synthetic data generation across the HealthSim ecosystem, ensuring realistic and consistent patient, member, and subject populations.

**Key Capability**: Transform population analysis into actionable generation parameters that produce statistically accurate synthetic cohorts.

---

## Skills in This Category

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [cohort-specification.md](cohort-specification.md) | Complete cohort definition | "define cohort", "create cohort spec", "population spec" |
| [demographic-distribution.md](demographic-distribution.md) | Age, sex, race distribution | "age distribution", "demographics for cohort" |
| [clinical-prevalence-profile.md](clinical-prevalence-profile.md) | Disease and comorbidity rates | "clinical profile", "comorbidity rates" |
| [sdoh-profile-builder.md](sdoh-profile-builder.md) | SDOH characteristics | "SDOH profile", "social factors for cohort" |

---

## CohortSpecification Object

The central output of cohort definition - drives all HealthSim products:

```json
{
  "cohort_id": "houston_diabetics_2024",
  "name": "Houston Metro Diabetic Adults",
  "description": "Adult diabetics in Houston MSA for chronic care management program",
  "target_size": 10000,
  
  "geography": {
    "type": "msa",
    "cbsa_code": "26420",
    "name": "Houston-The Woodlands-Sugar Land, TX"
  },
  
  "demographics": {
    "age": {
      "distribution_type": "empirical",
      "min": 18,
      "max": 85,
      "mean": 58.4,
      "brackets": {
        "18-44": 0.18,
        "45-64": 0.42,
        "65-74": 0.28,
        "75+": 0.12
      }
    },
    "sex": {
      "male": 0.48,
      "female": 0.52
    },
    "race_ethnicity": {
      "white_nh": 0.28,
      "black": 0.22,
      "hispanic": 0.38,
      "asian": 0.08,
      "other": 0.04
    }
  },
  
  "clinical_profile": {
    "primary_condition": {
      "icd10": "E11",
      "name": "Type 2 Diabetes",
      "prevalence": 1.0
    },
    "comorbidities": {
      "I10": { "name": "Hypertension", "rate": 0.71 },
      "E78": { "name": "Hyperlipidemia", "rate": 0.68 },
      "E66": { "name": "Obesity", "rate": 0.62 },
      "F32": { "name": "Depression", "rate": 0.28 },
      "N18": { "name": "CKD", "rate": 0.24 }
    },
    "severity_distribution": {
      "mild": 0.35,
      "moderate": 0.45,
      "severe": 0.20
    }
  },
  
  "sdoh_profile": {
    "poverty_rate": 0.18,
    "uninsured_rate": 0.16,
    "limited_english": 0.14,
    "transportation_barrier": 0.12,
    "food_insecurity": 0.15,
    "svi_mean": 0.58
  },
  
  "insurance_mix": {
    "medicare": 0.38,
    "medicaid": 0.22,
    "commercial": 0.32,
    "uninsured": 0.08
  },
  
  "z_code_rates": {
    "Z59.6": { "name": "Low income", "rate": 0.18 },
    "Z59.41": { "name": "Food insecurity", "rate": 0.15 },
    "Z60.3": { "name": "Limited English", "rate": 0.14 },
    "Z59.82": { "name": "Transportation", "rate": 0.12 }
  },
  
  "validation": {
    "sources": ["CDC_PLACES", "ACS_2022", "CDC_SVI_2022"],
    "confidence": "high",
    "notes": "Large MSA with reliable estimates"
  },
  
  "metadata": {
    "created_at": "2024-12-23T10:00:00Z",
    "created_by": "PopulationSim",
    "version": "1.0"
  }
}
```

---

## Workflow

### 1. Geographic Analysis → 2. Cohort Definition → 3. Data Generation

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  PopulationSim   │     │  PopulationSim   │     │  PatientSim/     │
│  Geographic      │────▶│  Cohort          │────▶│  MemberSim/      │
│  Analysis        │     │  Definition      │     │  TrialSim        │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                  │
                                  ▼
                         CohortSpecification
```

---

## Integration Points

### → PatientSim

CohortSpecification drives patient generation:
- Demographics → Patient demographics
- Clinical profile → Diagnoses, conditions
- SDOH profile → Z-codes
- Comorbidities → Multi-diagnosis patients

```
cohort.demographics.age → Patient.birthDate
cohort.clinical_profile.comorbidities → Patient.conditions[]
cohort.sdoh_profile → Patient.conditions[] (Z-codes)
```

### → MemberSim

CohortSpecification informs member profiles:
- Demographics → Member demographics
- Insurance mix → Coverage type
- SDOH → Utilization patterns

```
cohort.insurance_mix → Member.coverage
cohort.clinical_profile → Member.risk_score
cohort.sdoh_profile → Member.utilization_pattern
```

### → TrialSim

CohortSpecification guides subject selection:
- Demographics → Inclusion/exclusion
- Clinical profile → Eligibility
- Geographic constraints → Site assignment

```
cohort.demographics → Subject.eligibility
cohort.clinical_profile → Subject.screening_status
cohort.geography → Subject.site_assignment
```

---

## Skill Selection Guide

### Use cohort-specification.md when:
- Need complete cohort definition
- Starting a new generation project
- Defining target population for simulation

### Use demographic-distribution.md when:
- Focus on age, sex, race distribution
- Need to match specific population
- Adjusting demographic balance

### Use clinical-prevalence-profile.md when:
- Defining disease-specific cohorts
- Setting comorbidity patterns
- Severity distribution needed

### Use sdoh-profile-builder.md when:
- Adding social determinants
- Z-code rate setting
- Vulnerability profiling

---

## Common Cohort Types

### Chronic Disease Management
```json
{
  "primary_condition": "E11",
  "age_range": [45, 80],
  "comorbidities": ["I10", "E78", "E66"],
  "sdoh_focus": ["food_insecurity", "cost_barrier"]
}
```

### Health Plan Population
```json
{
  "insurance_type": "medicare_advantage",
  "geography": "county",
  "risk_stratification": ["low", "moderate", "high"],
  "demographics": "match_plan_enrollment"
}
```

### Clinical Trial Target
```json
{
  "condition": "E11.65",
  "age_range": [18, 75],
  "exclusions": ["N18.5", "N18.6"],
  "diversity_targets": { "minority": 0.40 }
}
```

### FQHC Population
```json
{
  "geography": "service_area_tracts",
  "insurance_mix": { "medicaid": 0.45, "uninsured": 0.35 },
  "svi_threshold": 0.70,
  "primary_care_focus": true
}
```

---

## Validation

### Required Fields
- [ ] cohort_id (unique identifier)
- [ ] geography (at least type)
- [ ] demographics.age (min, max, or distribution)
- [ ] demographics.sex (distribution)

### Recommended Fields
- [ ] clinical_profile (for disease cohorts)
- [ ] sdoh_profile (for realistic populations)
- [ ] insurance_mix (for member simulations)

### Consistency Checks
- [ ] Age distribution sums to ~1.0
- [ ] Sex distribution sums to 1.0
- [ ] Race/ethnicity sums to ~1.0
- [ ] Comorbidity rates clinically plausible
- [ ] SDOH rates match geography SVI

---

## Related Skills

- [Geographic Intelligence](../geographic/README.md) - Source for demographics
- [Health Patterns](../health-patterns/README.md) - Source for clinical profiles
- [SDOH Analysis](../sdoh/README.md) - Source for SDOH profiles
- [Trial Support](../trial-support/README.md) - Trial-specific cohorts
