---
name: medicaid-adult-profile
description: Adult Medicaid beneficiary profile template
type: profile_template
---

# Medicaid Adult Profile

Profile template for adult Medicaid beneficiaries with typical eligibility and utilization patterns.

## Quick Start

```
User: "Generate an adult Medicaid member"

Claude: "Creating Medicaid adult profile:
- Age 19-64 (non-elderly adult)
- Income-based eligibility
- Managed care enrollment
- Higher chronic disease burden"
```

## Profile Specification

```json
{
  "template": {
    "id": "medicaid_adult",
    "name": "Medicaid Adult Beneficiary",
    "version": "1.0",
    "category": "medicaid",
    "tags": ["medicaid", "adult", "managed_care", "low_income"]
  },
  
  "demographics": {
    "age_range": {"min": 19, "max": 64},
    "gender_distribution": {"M": 0.40, "F": 0.60},
    "income_level": "below_138_fpl"
  },
  
  "eligibility": {
    "categories": [
      {"type": "expansion_adult", "probability": 0.45},
      {"type": "parent_caretaker", "probability": 0.25},
      {"type": "disability", "probability": 0.20},
      {"type": "pregnant", "probability": 0.10}
    ],
    "managed_care_enrollment": 0.85,
    "churn_rate_annual": 0.25
  },
  
  "clinical_profile": {
    "chronic_conditions": [
      {"condition": "depression", "probability": 0.35},
      {"condition": "anxiety", "probability": 0.30},
      {"condition": "diabetes_type2", "probability": 0.20},
      {"condition": "hypertension", "probability": 0.25},
      {"condition": "asthma", "probability": 0.15},
      {"condition": "substance_use", "probability": 0.18}
    ],
    "behavioral_health_need": 0.45
  },
  
  "utilization": {
    "annual_visits": {"min": 3, "max": 15},
    "er_visits": {"mean": 1.5, "std": 1.2},
    "inpatient_admissions": {"mean": 0.15, "std": 0.4},
    "behavioral_health_visits": {"mean": 4, "std": 6}
  },
  
  "social_determinants": {
    "housing_instability": 0.20,
    "food_insecurity": 0.25,
    "transportation_barrier": 0.30,
    "health_literacy_low": 0.35
  }
}
```

## Utilization Patterns

| Service Type | Annual Rate | Notes |
|--------------|-------------|-------|
| Primary care | 3-5 visits | Often via FQHC |
| ER visits | 1-3 | Higher than commercial |
| Behavioral health | 4-12 | If engaged |
| Pharmacy | 6-12 Rx | Generic preferred |

## Cost Profile

| Component | Annual Range |
|-----------|-------------|
| Total PMPM | $400 - $800 |
| Pharmacy | $80 - $200 PMPM |
| Behavioral Health | $50 - $150 PMPM |
| Inpatient | $100 - $300 PMPM |

## Related Profiles

- **[Medicaid Pediatric](medicaid-pediatric.md)** - Child Medicaid
- **[Medicaid Diabetic](medicaid-diabetic.md)** - Chronic condition focus

---

*Part of the HealthSim Generative Framework Template Library*
