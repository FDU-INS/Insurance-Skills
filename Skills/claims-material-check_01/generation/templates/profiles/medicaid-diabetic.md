---
name: medicaid-diabetic-profile
description: Medicaid member with diabetes profile template
type: profile_template
---

# Medicaid Diabetic Profile

Profile template for Medicaid beneficiaries with Type 2 diabetes and associated social determinants.

## Quick Start

```
User: "Generate a Medicaid diabetic member"

Claude: "Creating Medicaid diabetic profile:
- Type 2 diabetes with SDOH challenges
- Care coordination needs
- FQHC-based care
- Quality measure targets"
```

## Profile Specification

```json
{
  "template": {
    "id": "medicaid_diabetic",
    "name": "Medicaid Diabetic Beneficiary",
    "version": "1.0",
    "category": "medicaid",
    "tags": ["diabetes", "chronic", "medicaid", "care_coordination"]
  },
  
  "demographics": {
    "age_range": {"min": 25, "max": 64},
    "gender_distribution": {"M": 0.45, "F": 0.55}
  },
  
  "clinical_profile": {
    "primary_condition": "type_2_diabetes",
    "a1c_range": {"mean": 8.5, "std": 2.0},
    "control_status": {
      "controlled": 0.40,
      "uncontrolled": 0.60
    },
    "comorbidities": [
      {"condition": "hypertension", "probability": 0.75},
      {"condition": "depression", "probability": 0.40},
      {"condition": "obesity", "probability": 0.65},
      {"condition": "ckd", "probability": 0.30}
    ]
  },
  
  "care_barriers": {
    "transportation": 0.35,
    "food_insecurity": 0.40,
    "medication_adherence": 0.55,
    "health_literacy": 0.45,
    "appointment_no_show": 0.25
  },
  
  "utilization": {
    "pcp_visits": {"mean": 3, "std": 2},
    "er_visits_diabetes": {"mean": 0.8, "std": 1},
    "dka_admissions": {"probability": 0.08}
  }
}
```

## Quality Challenges

| Measure | Target | Typical Rate |
|---------|--------|--------------|
| A1C <9% | 80% | 55-65% |
| Eye exam | 70% | 40-50% |
| Nephropathy screening | 85% | 60-70% |
| BP control | 75% | 50-60% |

## Care Coordination Needs

- Diabetes self-management education
- Nutritional counseling
- Community health worker support
- Transportation assistance
- Medication assistance programs

## Related Profiles

- **[Medicaid Adult](medicaid-adult.md)** - General Medicaid adult
- **[Commercial Diabetic](commercial-diabetic.md)** - Commercial comparison

---

*Part of the HealthSim Generative Framework Template Library*
