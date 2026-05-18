---
name: populationsim-trial-support
description: >
  Trial support skills for clinical trial feasibility and planning. Provides
  population-level insights for site selection, enrollment projection, and
  diversity planning. Uses v2.0 embedded CDC PLACES and SVI data for evidence-based
  trial planning. Complements TrialSim's subject-level generation.
version: "2.0"
---

# Trial Support Skills

## Overview

Trial support skills provide population-level analytics to support clinical trial planning and feasibility assessment. These skills complement TrialSim by providing the demographic and epidemiologic foundation for realistic trial simulations.

**Key Capability**: Transform real-world population data into actionable trial planning parameters, enabling realistic enrollment projections and diversity-aware site selection.

---

## Skills in This Category

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [feasibility-estimation.md](feasibility-estimation.md) | Estimate eligible population for protocol | "feasibility", "eligible population", "how many patients" |
| [site-selection-support.md](site-selection-support.md) | Identify optimal trial site locations | "site selection", "where to conduct trial", "best locations" |
| [enrollment-projection.md](enrollment-projection.md) | Project enrollment rates and timelines | "enrollment projection", "recruitment timeline", "enrollment rate" |

---

## Integration with TrialSim

```
┌──────────────────────┐     ┌──────────────────────┐
│    PopulationSim     │     │      TrialSim        │
│    Trial Support     │────▶│   Subject Generation │
│                      │     │                      │
│ • Feasibility est.   │     │ • DM domain data     │
│ • Site selection     │     │ • Screening/Enroll   │
│ • Enrollment proj.   │     │ • Treatment assign   │
│ • Diversity targets  │     │ • Efficacy/Safety    │
└──────────────────────┘     └──────────────────────┘
         │                            │
         └────────────┬───────────────┘
                      ▼
              CohortSpecification
              (trial-qualified)
```

---

## Trial Feasibility Flow

### 1. Define Protocol Criteria
```
Inclusion:
- Age 18-75
- Confirmed T2DM (E11)
- HbA1c 7.5-10.5%
- On stable metformin

Exclusion:
- CKD Stage 4-5 (N18.4, N18.5, N18.6)
- Recent CV event
- Current insulin use
```

### 2. Estimate Eligible Population
```
National T2DM population: 34.2M
→ Age filter: 28.4M
→ HbA1c range: 12.8M
→ On metformin: 9.2M
→ After exclusions: 6.8M eligible
```

### 3. Apply Geographic Constraints
```
Target states: TX, FL, CA, NY
→ Regional eligible: 2.4M
→ Top 20 metros: 1.8M accessible
```

### 4. Project Enrollment
```
Sites: 40
Per-site eligible: ~3,000
Screen rate: 5%/year
Screen-to-enroll: 35%
→ Annual enrollment: 210/site
→ Time to 2,000 subjects: ~6 months
```

---

## Key Outputs

### Feasibility Report
```json
{
  "protocol": "DIABETES-001",
  "indication": "E11",
  "national_eligible": 6800000,
  "funnel": {
    "disease_prevalent": 34200000,
    "after_age_filter": 28400000,
    "after_clinical_criteria": 12800000,
    "after_exclusions": 6800000
  },
  "geographic_distribution": {
    "south": 0.38,
    "west": 0.24,
    "midwest": 0.20,
    "northeast": 0.18
  }
}
```

### Site Recommendation
```json
{
  "recommended_sites": [
    {
      "metro": "Houston",
      "eligible_population": 185000,
      "diversity_score": 0.82,
      "competition": "moderate"
    }
  ],
  "diversity_achievable": {
    "minority_enrollment": 0.42,
    "hispanic": 0.28,
    "black": 0.14
  }
}
```

### Enrollment Projection
```json
{
  "target_enrollment": 2000,
  "sites": 40,
  "projected_timeline_months": 8,
  "monthly_enrollment": [
    { "month": 1, "cumulative": 180, "sites_active": 25 },
    { "month": 2, "cumulative": 420, "sites_active": 38 }
  ]
}
```

---

## Data Sources (Embedded v2.0)

Trial support skills use PopulationSim's embedded data package with 100% US coverage:

| Source | Embedded File | Records | Application |
|--------|---------------|---------|-------------|
| CDC PLACES (County) | `data/county/places_county_2024.csv` | 3,143 | Disease prevalence |
| CDC PLACES (Tract) | `data/tract/places_tract_2024.csv` | 83,522 | Site catchment analysis |
| CDC SVI (County) | `data/county/svi_county_2022.csv` | 3,144 | Diversity, retention risk |
| CDC SVI (Tract) | `data/tract/svi_tract_2022.csv` | 84,120 | SDOH-based adjustments |
| ADI (Block Group) | `data/block_group/adi_blockgroup_2023.csv` | 242,336 | Deprivation-based modeling |

### v2.0 Benefits

- **Real Prevalence Rates**: Use actual CDC PLACES data instead of generic estimates
- **Evidence-Based Diversity**: SVI EP_MINRTY field for minority population %
- **SDOH-Adjusted Retention**: Model dropout risk using real vulnerability data
- **Provenance Tracking**: All outputs cite data source, year, and file reference

---

## Diversity Considerations

### FDA Diversity Guidelines
- Enrollment should reflect disease epidemiology
- Underrepresented groups: Black, Hispanic, AIAN
- Sex balance appropriate for condition
- Age range reflects real-world use

### PopulationSim Support
- Demographic distribution by geography
- Disease prevalence by race/ethnicity
- Site recommendations for diversity
- Enrollment projections by demographic

### Example Targets
| Condition | Black Target | Hispanic Target | Notes |
|-----------|--------------|-----------------|-------|
| Diabetes | 15-20% | 20-25% | Reflects prevalence |
| Heart Failure | 18-22% | 10-15% | Higher Black burden |
| Breast Cancer | 12-15% | 10-15% | Mortality disparity |
| Alzheimer's | 15-20% | 12-18% | Risk difference |

---

## Related Categories

- [Geographic Intelligence](../geographic/README.md) - Population data
- [Health Patterns](../health-patterns/README.md) - Prevalence data
- [Cohort Definition](../cohorts/README.md) - Trial cohort specs
- TrialSim Skills - Subject generation
