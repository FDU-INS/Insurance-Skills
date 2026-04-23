---
name: medicare-chf-profile
description: Medicare beneficiary with heart failure profile template
type: profile_template
---

# Medicare CHF Profile

Profile template for Medicare beneficiaries with congestive heart failure (CHF/HFrEF/HFpEF).

## Quick Start

```
User: "Generate a Medicare CHF patient"

Claude: "Creating Medicare CHF profile:
- Heart failure diagnosis
- LVEF classification
- Guideline-directed therapy
- High readmission risk"
```

## Profile Specification

```json
{
  "template": {
    "id": "medicare_chf",
    "name": "Medicare Heart Failure Patient",
    "version": "1.0",
    "category": "medicare",
    "tags": ["heart_failure", "chronic", "medicare", "high_risk"]
  },
  
  "demographics": {
    "age_range": {"min": 65, "max": 90},
    "gender_distribution": {"M": 0.55, "F": 0.45}
  },
  
  "clinical_profile": {
    "hf_type": {
      "hfref": {"probability": 0.50, "lvef": "<40%"},
      "hfpef": {"probability": 0.45, "lvef": ">=50%"},
      "hfmref": {"probability": 0.05, "lvef": "40-49%"}
    },
    "nyha_class": {
      "I": 0.15,
      "II": 0.40,
      "III": 0.35,
      "IV": 0.10
    },
    "comorbidities": [
      {"condition": "atrial_fibrillation", "probability": 0.50},
      {"condition": "hypertension", "probability": 0.80},
      {"condition": "diabetes", "probability": 0.45},
      {"condition": "ckd_stage_3_4", "probability": 0.55},
      {"condition": "copd", "probability": 0.30}
    ]
  },
  
  "medications": {
    "gdmt": {
      "ace_arb_arni": 0.80,
      "beta_blocker": 0.85,
      "mra": 0.50,
      "sglt2i": 0.35,
      "diuretic": 0.90
    },
    "typical_count": {"mean": 8, "std": 3}
  },
  
  "utilization": {
    "cardiology_visits": 3,
    "pcp_visits": 4,
    "er_visits": {"mean": 1.5, "std": 1.2},
    "inpatient_admissions": {"mean": 0.8, "std": 0.7},
    "30_day_readmission_risk": 0.22
  },
  
  "monitoring": {
    "bnp_frequency": "quarterly",
    "echo_frequency": "annual",
    "weight_monitoring": "daily"
  }
}
```

## GDMT Optimization

| Medication Class | Target % | Typical % |
|------------------|----------|-----------|
| ACE/ARB/ARNI | 90% | 75-80% |
| Beta-blocker | 90% | 80-85% |
| MRA | 75% | 45-55% |
| SGLT2i | 75% | 30-40% |

## Cost Profile

| Component | Annual Range |
|-----------|-------------|
| Inpatient | $15,000 - $50,000 |
| Medications | $3,000 - $8,000 |
| Cardiology | $2,000 - $5,000 |
| DME (oxygen, etc) | $1,000 - $3,000 |
| Total | $21,000 - $66,000 |

## Related Profiles

- **[Medicare Diabetic](medicare-diabetic.md)** - Common comorbidity
- **[Commercial High-Cost](commercial-high-cost.md)** - High-cost patterns

## Related Journeys

- **[CHF First Year](../journeys/chf-first-year.md)** - First year of care

---

*Part of the HealthSim Generative Framework Template Library*
