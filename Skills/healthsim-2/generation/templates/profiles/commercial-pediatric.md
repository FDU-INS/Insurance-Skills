---
name: commercial-pediatric-profile
description: Commercial pediatric member profile template
type: profile_template
---

# Commercial Pediatric Profile

Profile template for commercially insured children ages 1-17 with standard well-child and illness patterns.

## Quick Start

```
User: "Generate a commercial pediatric member age 8"

Claude: "Creating pediatric profile:
- School-age child (8 years)
- Annual well-child visit
- Sports physical
- Typical illness patterns"
```

## Profile Specification

```json
{
  "template": {
    "id": "commercial_pediatric",
    "name": "Commercial Pediatric Member",
    "version": "1.0",
    "category": "commercial",
    "tags": ["pediatric", "commercial", "dependent", "well_child"]
  },
  
  "demographics": {
    "age_range": {"min": 1, "max": 17},
    "gender_distribution": {"M": 0.51, "F": 0.49}
  },
  
  "age_segments": {
    "toddler": {"age": "1-3", "visits_per_year": 4},
    "preschool": {"age": "4-5", "visits_per_year": 2},
    "school_age": {"age": "6-11", "visits_per_year": 1.5},
    "adolescent": {"age": "12-17", "visits_per_year": 1.5}
  },
  
  "clinical_profile": {
    "common_conditions": [
      {"condition": "upper_respiratory_infection", "annual_rate": 3},
      {"condition": "otitis_media", "annual_rate": 0.8},
      {"condition": "asthma", "prevalence": 0.12},
      {"condition": "adhd", "prevalence": 0.10},
      {"condition": "allergies", "prevalence": 0.20}
    ]
  },
  
  "preventive_care": {
    "well_child_visits": "annual",
    "immunizations": "age_appropriate",
    "dental_visits": 2,
    "vision_screening": "annual"
  },
  
  "utilization": {
    "well_child": 1,
    "sick_visits": {"mean": 3, "std": 2},
    "er_visits": {"mean": 0.3, "std": 0.5},
    "specialist": {"mean": 0.5, "std": 1}
  }
}
```

## Expected Annual Utilization

| Age Group | Well-Child | Sick Visits | Immunizations |
|-----------|------------|-------------|---------------|
| 1-3 years | 3-4 | 4-6 | 4-6 |
| 4-5 years | 1-2 | 3-5 | 2-3 |
| 6-11 years | 1 | 2-4 | 0-1 |
| 12-17 years | 1 | 2-3 | 1-2 |

## Cost Profile

| Component | Annual Range |
|-----------|-------------|
| Well-child | $200 - $400 |
| Sick visits | $300 - $600 |
| Immunizations | $200 - $500 |
| Dental | $200 - $400 |
| Total | $900 - $1,900 |

## Related Profiles

- **[Pediatric Newborn](pediatric-newborn.md)** - Infant care
- **[Medicaid Pediatric](medicaid-pediatric.md)** - Medicaid equivalent
- **[Commercial Family](commercial-family.md)** - Full family context

---

*Part of the HealthSim Generative Framework Template Library*
