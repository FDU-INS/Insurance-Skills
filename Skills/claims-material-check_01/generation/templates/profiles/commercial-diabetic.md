---
name: commercial-diabetic-profile
description: Commercial member with diabetes profile template
type: profile_template
---

# Commercial Diabetic Profile

Profile template for commercially insured members with Type 2 diabetes and associated care patterns.

## Quick Start

```
User: "Generate a commercial diabetic member"

Claude: "Creating diabetic profile:
- Type 2 diabetes diagnosis
- Quarterly A1C monitoring
- Diabetes medications
- Annual eye/foot exams"
```

## Profile Specification

```json
{
  "template": {
    "id": "commercial_diabetic",
    "name": "Commercial Diabetic Member",
    "version": "1.0",
    "category": "commercial",
    "tags": ["diabetes", "chronic", "commercial", "quality_measures"]
  },
  
  "demographics": {
    "age_range": {"min": 30, "max": 64},
    "gender_distribution": {"M": 0.52, "F": 0.48},
    "bmi_range": {"mean": 32, "std": 5}
  },
  
  "clinical_profile": {
    "primary_condition": "type_2_diabetes",
    "a1c_range": {"mean": 7.5, "std": 1.5},
    "comorbidities": [
      {"condition": "hypertension", "probability": 0.70},
      {"condition": "hyperlipidemia", "probability": 0.65},
      {"condition": "obesity", "probability": 0.55},
      {"condition": "ckd_stage_1_3", "probability": 0.25},
      {"condition": "neuropathy", "probability": 0.20}
    ]
  },
  
  "care_pattern": {
    "pcp_visits": 4,
    "endocrinology_visits": {"mean": 2, "probability": 0.40},
    "ophthalmology_annual": 1,
    "podiatry_annual": 1,
    "a1c_tests": 4,
    "lipid_panel": 1,
    "kidney_screening": 1
  },
  
  "medications": {
    "oral_agents": ["metformin", "sulfonylurea", "sglt2_inhibitor", "dpp4_inhibitor"],
    "injectable": ["glp1_agonist", "insulin"],
    "typical_count": {"mean": 3, "std": 1}
  },
  
  "quality_measures": ["a1c_control", "eye_exam", "kidney_screening", "bp_control"]
}
```

## Expected Annual Utilization

| Service | Frequency | Purpose |
|---------|-----------|---------|
| PCP visits | 4 | Quarterly monitoring |
| A1C tests | 4 | Glycemic control |
| Eye exam | 1 | Retinopathy screening |
| Foot exam | 1-2 | Neuropathy screening |
| Kidney labs | 1 | eGFR/UACR |

## Cost Profile

| Component | Annual Range |
|-----------|-------------|
| Medications | $3,000 - $15,000 |
| Office visits | $800 - $1,500 |
| Labs | $400 - $800 |
| Specialist | $500 - $1,200 |
| Total | $4,700 - $18,500 |

## Related Profiles

- **[Medicare Diabetic](medicare-diabetic.md)** - Medicare equivalent
- **[Medicaid Diabetic](medicaid-diabetic.md)** - Medicaid equivalent
- **[Commercial High-Cost](commercial-high-cost.md)** - Uncontrolled cases

---

*Part of the HealthSim Generative Framework Template Library*
