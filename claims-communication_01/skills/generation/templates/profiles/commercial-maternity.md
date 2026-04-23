---
name: commercial-maternity-template
description: Pre-built profile for commercial maternity population through pregnancy journey
type: profile_template
---

# Commercial Maternity Profile Template

Ready-to-use profile for generating commercially insured pregnant women from conception through postpartum.

## Quick Start

```
User: "Use the commercial maternity template for 100 members"

Claude: "Using template 'commercial-maternity' with defaults:
- 100 pregnant members
- Commercial PPO/HMO coverage
- Age 25-40 (mean 31)
- Mix of pregnancy stages
- Standard and high-risk pregnancies

Generate now or customize?"
```

## Template Specification

```json
{
  "template": {
    "id": "commercial-maternity",
    "name": "Commercial Maternity Population",
    "version": "1.0",
    "category": "payer",
    "tags": ["commercial", "maternity", "pregnancy", "women's-health"]
  },
  
  "profile": {
    "generation": {
      "count": 100,
      "products": ["patientsim", "membersim", "rxmembersim"],
      "validation": "strict"
    },
    
    "demographics": {
      "age": {
        "type": "normal",
        "mean": 31,
        "std_dev": 5,
        "min": 18,
        "max": 45
      },
      "gender": {
        "type": "fixed",
        "value": "F"
      },
      "geography": {
        "type": "national",
        "distribution": "employment_weighted"
      },
      "gravida_para": {
        "type": "categorical",
        "weights": {
          "G1P0": 0.40,
          "G2P1": 0.30,
          "G3P2": 0.18,
          "G4+": 0.12
        }
      }
    },
    
    "clinical": {
      "pregnancy_stage": {
        "type": "categorical",
        "weights": {
          "first_trimester": 0.25,
          "second_trimester": 0.35,
          "third_trimester": 0.30,
          "postpartum": 0.10
        }
      },
      "risk_category": {
        "type": "categorical",
        "weights": {
          "low_risk": 0.70,
          "moderate_risk": 0.20,
          "high_risk": 0.10
        }
      },
      "pregnancy_conditions": {
        "standard": {
          "prevalence": 0.70,
          "conditions": [
            {"code": "Z34.00", "description": "Normal first pregnancy", "conditional": "G1P0"},
            {"code": "Z34.80", "description": "Normal pregnancy", "conditional": "!G1P0"}
          ]
        },
        "moderate_risk": {
          "prevalence": 0.20,
          "conditions": [
            {"code": "O24.410", "description": "Gestational diabetes", "prevalence": 0.40},
            {"code": "O13.9", "description": "Gestational hypertension", "prevalence": 0.30},
            {"code": "O26.20", "description": "Pregnancy care for habitual aborter", "prevalence": 0.15},
            {"code": "O09.521", "description": "Advanced maternal age (>35)", "prevalence": 0.35}
          ]
        },
        "high_risk": {
          "prevalence": 0.10,
          "conditions": [
            {"code": "O14.00", "description": "Preeclampsia", "prevalence": 0.35},
            {"code": "O44.00", "description": "Placenta previa", "prevalence": 0.15},
            {"code": "O60.00", "description": "Preterm labor", "prevalence": 0.30},
            {"code": "O30.001", "description": "Twin pregnancy", "prevalence": 0.15},
            {"code": "O10.011", "description": "Pre-existing HTN with pregnancy", "prevalence": 0.20}
          ]
        }
      },
      "pre_existing_conditions": [
        {"code": "E66.9", "description": "Obesity", "prevalence": 0.28},
        {"code": "F41.1", "description": "Anxiety", "prevalence": 0.15},
        {"code": "F32.9", "description": "Depression", "prevalence": 0.12},
        {"code": "E03.9", "description": "Hypothyroidism", "prevalence": 0.08},
        {"code": "E11.9", "description": "Pre-gestational diabetes", "prevalence": 0.03}
      ],
      "delivery_type": {
        "type": "categorical",
        "weights": {
          "vaginal_spontaneous": 0.55,
          "vaginal_induced": 0.13,
          "cesarean_planned": 0.12,
          "cesarean_unplanned": 0.18,
          "vbac": 0.02
        }
      },
      "labs": {
        "first_trimester": [
          {"test": "CBC", "frequency": 1},
          {"test": "Blood Type/Rh", "frequency": 1},
          {"test": "Rubella titer", "frequency": 1},
          {"test": "HBsAg", "frequency": 1},
          {"test": "HIV", "frequency": 1},
          {"test": "Urine culture", "frequency": 1},
          {"test": "First trimester screen", "frequency": 1}
        ],
        "second_trimester": [
          {"test": "Quad screen", "frequency": 1},
          {"test": "Glucose challenge 1hr", "frequency": 1},
          {"test": "CBC", "frequency": 1}
        ],
        "third_trimester": [
          {"test": "GBS culture", "frequency": 1},
          {"test": "CBC", "frequency": 1},
          {"test": "NST", "condition": "high_risk", "frequency": "weekly"}
        ]
      }
    },
    
    "coverage": {
      "type": "Commercial",
      "plan_distribution": {
        "PPO": 0.55,
        "HMO": 0.30,
        "HDHP": 0.10,
        "POS": 0.05
      },
      "maternity_benefits": {
        "deductible_applies": true,
        "global_ob_fee": 0.85,
        "separate_hospital_bill": 0.15
      },
      "family_status": {
        "type": "categorical",
        "weights": {
          "employee_spouse": 0.45,
          "employee_only": 0.30,
          "family": 0.25
        }
      }
    },
    
    "utilization": {
      "prenatal_visits": {
        "low_risk": 12,
        "high_risk": 18
      },
      "ultrasounds": {
        "low_risk": 2,
        "high_risk": 6
      },
      "hospital_los": {
        "vaginal": {"mean": 2, "variance": 1},
        "cesarean": {"mean": 4, "variance": 1}
      }
    },
    
    "medications": {
      "prenatal_vitamins": {"prevalence": 0.95},
      "iron_supplement": {"prevalence": 0.25},
      "zofran": {"prevalence": 0.15, "condition": "hyperemesis"},
      "progesterone": {"prevalence": 0.10, "condition": "high_risk"},
      "antihypertensive": {"prevalence": 0.08, "condition": "preeclampsia"},
      "insulin": {"prevalence": 0.07, "condition": "gdm_or_dm"},
      "ssri_continuation": {"prevalence": 0.05, "condition": "depression"}
    }
  },
  
  "journey_integration": {
    "default_journey": "pregnancy-journey",
    "journey_parameters": {
      "conception_date": "auto_calculate",
      "due_date": "conception_date + 280 days",
      "delivery_date": "due_date ± 14 days"
    }
  },
  
  "quality_measures": {
    "hedis": {
      "prenatal_timeliness": {"description": "Prenatal care in first trimester", "target": 0.85},
      "postpartum_visit": {"description": "Postpartum visit 7-84 days", "target": 0.75},
      "prenatal_care": {"description": "≥80% expected visits", "target": 0.80}
    },
    "outcomes": {
      "preterm_birth_rate": {"target": 0.10},
      "low_birth_weight": {"target": 0.08},
      "cesarean_rate": {"target": 0.32},
      "nicu_admission": {"target": 0.10}
    }
  },
  
  "customizable": {
    "count": "Number of members (1-10,000)",
    "pregnancy_stage": "Focus on specific trimester or postpartum",
    "risk_level": "Adjust high-risk percentage",
    "delivery_type": "Adjust cesarean vs vaginal rates",
    "attach_journey": "Link to pregnancy journey template"
  }
}
```

## Use Cases

### Maternity Care Management
```
User: "Generate 50 high-risk pregnancies for care management"

Adjustments:
- risk_category: 100% high_risk
- care_management: enrolled = true
- Add weekly NST and biophysical profiles
```

### Bundled Payment Analysis
```
User: "Generate maternity episodes for bundled payment modeling"

Additions:
- Full journey from first prenatal to 60 days postpartum
- All claims with global OB fee structure
- Separate facility claims for delivery
```

## Expected Outputs

| Product | Entity Types | Formats |
|---------|--------------|---------|
| PatientSim | Patient, Conditions, Observations, Procedures | FHIR R4 |
| MemberSim | Member, Eligibility, Professional Claims, Facility Claims | X12 837 |
| RxMemberSim | Prescriptions, Fills | NCPDP D0 |

## Typical Cost Distribution

| Component | Vaginal Delivery | Cesarean Delivery |
|-----------|------------------|-------------------|
| Professional (Global) | $3,500-5,000 | $4,500-6,500 |
| Facility (Mother) | $8,000-15,000 | $15,000-25,000 |
| Facility (Newborn) | $2,000-4,000 | $3,000-8,000 |
| Labs & Imaging | $1,500-3,000 | $2,000-4,000 |
| Anesthesia | $1,000-2,000 | $1,500-3,000 |
| **Total Episode** | **$16,000-29,000** | **$26,000-46,500** |

## Related Templates

- [Pregnancy Journey](../journeys/pregnancy-journey.md) - Full pregnancy timeline
- [Commercial Healthy](commercial-healthy.md) - Non-pregnant commercial
- [Pediatric Newborn](pediatric-newborn.md) - Newborn care journey

---

*Part of the HealthSim Generative Framework Template Library*
