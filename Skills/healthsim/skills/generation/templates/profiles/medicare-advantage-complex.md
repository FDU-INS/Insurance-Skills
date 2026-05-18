---
name: medicare-advantage-complex-template
description: Pre-built profile for Medicare Advantage members with multiple chronic conditions
type: profile_template
---

# Medicare Advantage Complex Profile Template

Ready-to-use profile for generating Medicare Advantage members with high-acuity, multiple chronic conditions.

## Quick Start

```
User: "Use the Medicare Advantage complex template for 150 members"

Claude: "Using template 'ma-complex' with defaults:
- 150 members
- Medicare Advantage HMO/PPO mix
- Age 68-88 (mean 76)
- 3+ chronic conditions average
- High-risk HCC scores

Generate now or customize?"
```

## Template Specification

```json
{
  "template": {
    "id": "medicare-advantage-complex",
    "name": "Medicare Advantage Complex/High-Risk Population",
    "version": "1.0",
    "category": "payer",
    "tags": ["medicare", "ma", "complex", "high-risk", "chronic"]
  },
  
  "profile": {
    "generation": {
      "count": 150,
      "products": ["patientsim", "membersim", "rxmembersim"],
      "validation": "strict"
    },
    
    "demographics": {
      "age": {
        "type": "normal",
        "mean": 76,
        "std_dev": 7,
        "min": 65,
        "max": 95
      },
      "gender": {
        "type": "categorical",
        "weights": {"M": 0.45, "F": 0.55}
      },
      "geography": {
        "source": "populationsim",
        "filter": {
          "medicare_penetration": {"min": 0.30}
        }
      },
      "living_situation": {
        "type": "categorical",
        "weights": {
          "independent": 0.55,
          "with_family": 0.25,
          "assisted_living": 0.12,
          "snf": 0.08
        }
      }
    },
    
    "clinical": {
      "risk_stratification": {
        "type": "categorical",
        "weights": {
          "rising_risk": 0.25,
          "high_risk": 0.50,
          "very_high_risk": 0.25
        }
      },
      "hcc_profile": {
        "average_hcc_count": 4.5,
        "raf_score_range": {"min": 1.5, "max": 4.0}
      },
      "primary_conditions": {
        "selection": "weighted_combination",
        "conditions": [
          {"code": "I50.9", "description": "Heart failure", "prevalence": 0.45},
          {"code": "J44.9", "description": "COPD", "prevalence": 0.35},
          {"code": "E11.9", "description": "Type 2 diabetes", "prevalence": 0.55},
          {"code": "N18.3", "description": "CKD Stage 3", "prevalence": 0.40},
          {"code": "I25.10", "description": "CAD", "prevalence": 0.50},
          {"code": "F32.9", "description": "Depression", "prevalence": 0.30},
          {"code": "G20", "description": "Parkinson's disease", "prevalence": 0.08},
          {"code": "G30.9", "description": "Alzheimer's", "prevalence": 0.12}
        ]
      },
      "comorbidities": [
        {"code": "I10", "description": "Hypertension", "prevalence": 0.88},
        {"code": "E78.5", "description": "Hyperlipidemia", "prevalence": 0.82},
        {"code": "E66.9", "description": "Obesity", "prevalence": 0.38},
        {"code": "I48.91", "description": "Atrial fibrillation", "prevalence": 0.28},
        {"code": "M81.0", "description": "Osteoporosis", "prevalence": 0.25},
        {"code": "G47.33", "description": "Sleep apnea", "prevalence": 0.22},
        {"code": "K21.0", "description": "GERD", "prevalence": 0.35},
        {"code": "M17.11", "description": "Knee osteoarthritis", "prevalence": 0.40}
      ],
      "functional_status": {
        "adl_limitations": {
          "type": "categorical",
          "weights": {
            "none": 0.35,
            "mild_1-2": 0.35,
            "moderate_3-4": 0.20,
            "severe_5+": 0.10
          }
        },
        "fall_risk": {
          "type": "categorical",
          "weights": {"low": 0.40, "moderate": 0.40, "high": 0.20}
        }
      },
      "labs": {
        "a1c": {
          "type": "conditional",
          "rules": [
            {"if": "has_condition('E11')", "distribution": {"type": "normal", "mean": 7.8, "std_dev": 1.2}},
            {"else": true, "distribution": {"type": "normal", "mean": 5.6, "std_dev": 0.3}}
          ]
        },
        "egfr": {
          "type": "conditional",
          "rules": [
            {"if": "has_condition('N18.3')", "distribution": {"type": "uniform", "min": 30, "max": 59}},
            {"if": "has_condition('N18.4')", "distribution": {"type": "uniform", "min": 15, "max": 29}},
            {"else": true, "distribution": {"type": "normal", "mean": 68, "std_dev": 12}}
          ]
        },
        "bnp": {
          "type": "conditional",
          "rules": [
            {"if": "has_condition('I50')", "distribution": {"type": "log_normal", "mean": 450, "std_dev": 300}},
            {"else": true, "distribution": {"type": "normal", "mean": 50, "std_dev": 25}}
          ]
        }
      }
    },
    
    "coverage": {
      "type": "Medicare Advantage",
      "plan_distribution": {
        "MA HMO": 0.55,
        "MA PPO": 0.35,
        "MA PFFS": 0.05,
        "MA SNP": 0.05
      },
      "part_d": {
        "enrolled": 0.98,
        "lis_eligible": 0.42
      },
      "star_rating_target": 4.0
    },
    
    "care_management": {
      "enrolled": 0.65,
      "intensity": {
        "type": "categorical",
        "weights": {
          "telephonic": 0.40,
          "in_person": 0.35,
          "transitional_care": 0.25
        }
      }
    },
    
    "utilization": {
      "inpatient_admits_annual": {
        "type": "log_normal",
        "mean": 1.2,
        "std_dev": 1.0
      },
      "er_visits_annual": {
        "type": "log_normal",
        "mean": 1.5,
        "std_dev": 1.2
      },
      "pcp_visits_annual": {
        "type": "normal",
        "mean": 8,
        "std_dev": 3
      },
      "specialist_visits_annual": {
        "type": "normal",
        "mean": 12,
        "std_dev": 5
      },
      "rx_fills_monthly": {
        "type": "normal",
        "mean": 8,
        "std_dev": 3
      }
    },
    
    "medications": {
      "polypharmacy": {
        "average_medications": 12,
        "range": {"min": 6, "max": 20}
      },
      "common_classes": [
        {"class": "ace_arb", "prevalence": 0.65},
        {"class": "beta_blocker", "prevalence": 0.55},
        {"class": "statin", "prevalence": 0.70},
        {"class": "diuretic", "prevalence": 0.50},
        {"class": "anticoagulant", "prevalence": 0.30},
        {"class": "ppi", "prevalence": 0.45},
        {"class": "antidepressant", "prevalence": 0.35},
        {"class": "opioid", "prevalence": 0.15},
        {"class": "insulin", "prevalence": 0.25},
        {"class": "oral_hypoglycemic", "prevalence": 0.45}
      ]
    }
  },
  
  "quality_measures": {
    "hedis_gaps": {
      "a1c_testing": {"target": 0.90, "baseline": 0.82},
      "diabetic_eye_exam": {"target": 0.70, "baseline": 0.58},
      "med_adherence_dm": {"target": 0.80, "baseline": 0.72},
      "med_adherence_htn": {"target": 0.80, "baseline": 0.75},
      "med_adherence_chol": {"target": 0.80, "baseline": 0.78},
      "osteoporosis_screen": {"target": 0.60, "baseline": 0.45},
      "fall_risk_screen": {"target": 0.85, "baseline": 0.70}
    }
  },
  
  "customizable": {
    "count": "Number of members (1-10,000)",
    "geography": "National, state, or specific plan service area",
    "risk_level": "Adjust risk stratification mix",
    "condition_focus": "Emphasize specific conditions (CHF, COPD, etc.)",
    "snp_type": "C-SNP, D-SNP, or I-SNP focus"
  }
}
```

## Use Cases

### Care Management Programs
```
User: "Generate 200 high-risk MA members for care management pilot"

Adjustments:
- risk_stratification: 80% high_risk, 20% very_high_risk
- care_management.enrolled: 1.0
- recent_admit: true (stratify by recent hospitalization)
```

### Value-Based Contract Analysis
```
User: "Generate MA cohort for total cost of care analysis"

Additions:
- Include full claims history (12 months)
- Generate with realistic cost distributions
- Include PMPM cost calculations
```

## Expected Outputs

| Product | Entity Types | Formats |
|---------|--------------|---------|
| PatientSim | Patient, Conditions, Medications, Labs | FHIR R4, HL7v2 |
| MemberSim | Member, Eligibility, Claims, HCC Scores | X12 834, X12 837 |
| RxMemberSim | Prescriptions, Fills, MTM Eligibility | NCPDP D0 |

## Star Ratings Implications

| Measure Category | Simulated Baseline | 4-Star Target |
|-----------------|-------------------|---------------|
| Medication Adherence | 72-78% | 80%+ |
| Controlling Blood Pressure | 65% | 70%+ |
| Diabetes Care | 70% | 75%+ |
| Plan All-Cause Readmission | 16% | <15% |

## Related Templates

- [Medicare Diabetic](medicare-diabetic.md) - Simpler diabetic focus
- [CHF Journey](../journeys/hf-exacerbation.md) - Heart failure episode
- [Care Transitions](../journeys/care-transition.md) - Post-acute transitions

---

*Part of the HealthSim Generative Framework Template Library*
