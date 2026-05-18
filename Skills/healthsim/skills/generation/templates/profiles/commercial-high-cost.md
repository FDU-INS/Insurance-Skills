---
name: commercial-high-cost-profile
description: High-cost commercial member profile template
type: profile_template
---

# Commercial High-Cost Profile

Profile template for commercially insured members with high healthcare utilization and costs.

## Quick Start

```
User: "Generate a high-cost commercial member"

Claude: "Creating high-cost profile:
- Multiple chronic conditions
- Frequent healthcare utilization
- Specialty medication use
- Annual costs >$50,000"
```

## Profile Specification

```json
{
  "template": {
    "id": "commercial_high_cost",
    "name": "Commercial High-Cost Member",
    "version": "1.0",
    "category": "commercial",
    "tags": ["high_cost", "chronic", "complex", "specialty"]
  },
  
  "demographics": {
    "age_range": {"min": 40, "max": 65},
    "gender_distribution": {"M": 0.55, "F": 0.45}
  },
  
  "clinical_profile": {
    "condition_count": {"min": 3, "max": 8},
    "primary_conditions": [
      {"condition": "diabetes_type2", "probability": 0.60},
      {"condition": "heart_failure", "probability": 0.35},
      {"condition": "copd", "probability": 0.30},
      {"condition": "ckd", "probability": 0.40},
      {"condition": "cancer", "probability": 0.25},
      {"condition": "rheumatoid_arthritis", "probability": 0.20}
    ],
    "hcc_risk_score": {"min": 2.0, "max": 6.0}
  },
  
  "utilization": {
    "annual_visits": {"min": 15, "max": 40},
    "er_visits": {"min": 1, "max": 6},
    "inpatient_admissions": {"min": 1, "max": 4},
    "specialty_visits": {"min": 8, "max": 20},
    "lab_tests": {"min": 20, "max": 60}
  },
  
  "pharmacy": {
    "total_medications": {"min": 8, "max": 15},
    "specialty_drugs": {"min": 1, "max": 3},
    "annual_rx_cost": {"min": 15000, "max": 100000}
  },
  
  "cost_profile": {
    "annual_total": {"min": 50000, "max": 500000},
    "percentile": 99
  }
}
```

## Cost Distribution

| Component | Annual Range |
|-----------|-------------|
| Inpatient | $20,000 - $200,000 |
| Specialty Rx | $15,000 - $150,000 |
| Outpatient | $10,000 - $50,000 |
| Professional | $5,000 - $25,000 |
| DME/Other | $2,000 - $20,000 |

## Care Management Indicators

- Disease Management enrollment eligible
- Case Management candidate
- Prior authorization intensive
- High risk for readmission

## Related Profiles

- **[Commercial Healthy](commercial-healthy.md)** - Baseline comparison
- **[Medicare Diabetic](medicare-diabetic.md)** - Medicare equivalent

---

*Part of the HealthSim Generative Framework Template Library*
