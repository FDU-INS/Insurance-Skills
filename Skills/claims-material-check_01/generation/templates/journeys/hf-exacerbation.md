---
name: hf-exacerbation-journey
description: Heart failure hospitalization with readmission prevention and follow-up
type: journey_template
---

# Heart Failure Exacerbation Journey Template

Complete care journey for acute heart failure hospitalization through 30-day post-discharge period.

## Quick Start

```
User: "Use the HF exacerbation journey"

Claude: "Using journey template 'hf_exacerbation':

45-day timeline with:
- Acute hospitalization (3-5 days)
- Transitional care management
- High-intensity follow-up
- Medication optimization
- Readmission prevention focus

Attach to profile or customize?"
```

## Journey Specification

```json
{
  "template": {
    "id": "hf_exacerbation",
    "name": "Heart Failure Exacerbation Journey",
    "version": "1.0",
    "duration": "45 days",
    "category": "episode",
    "tags": ["heart_failure", "hospitalization", "readmission", "transitional_care"]
  },
  
  "journey": {
    "start_trigger": "admission_date",
    
    "phases": [
      {
        "name": "acute_presentation",
        "description": "ER presentation and admission decision",
        "duration": "0-8 hours",
        "events": [
          {
            "id": "er_arrival",
            "type": "encounter",
            "timing": {"hour": 0},
            "details": {
              "encounter_type": "emergency",
              "chief_complaint": "Shortness of breath, leg swelling",
              "acuity": "ESI-2",
              "diagnoses": ["I50.9", "J81.0"]
            }
          },
          {
            "id": "initial_workup",
            "type": "observation",
            "timing": {"hour": 0},
            "details": {
              "tests": [
                {"name": "BNP", "expected": {"min": 400, "max": 2000}},
                {"name": "Troponin", "expected": {"type": "normal_or_mild_elevation"}},
                {"name": "BMP", "expected": {"cr_elevated": 0.40}},
                {"name": "CBC"},
                {"name": "Chest X-Ray", "finding": "pulmonary_edema"}
              ]
            }
          },
          {
            "id": "er_treatment",
            "type": "procedure",
            "timing": {"hour": 1},
            "details": {
              "interventions": [
                {"type": "IV Furosemide", "dose": "40-80mg"},
                {"type": "Supplemental O2", "conditional": "spo2 < 92%"},
                {"type": "Nitroglycerin", "conditional": "sbp > 100"}
              ]
            }
          },
          {
            "id": "admission_decision",
            "type": "administrative",
            "timing": {"hour": 4, "variance": 2},
            "details": {
              "disposition": {
                "type": "categorical",
                "weights": {
                  "telemetry": 0.60,
                  "icu_ccu": 0.30,
                  "observation": 0.10
                }
              }
            }
          }
        ]
      },
      
      {
        "name": "inpatient_acute",
        "description": "Acute inpatient management",
        "duration": "3-5 days",
        "events": [
          {
            "id": "admission",
            "type": "admission",
            "timing": {"hour": 6},
            "details": {
              "admission_type": "urgent",
              "drg": "291",
              "expected_los": {"mean": 4, "range": [3, 7]}
            }
          },
          {
            "id": "diuresis",
            "type": "procedure",
            "timing": {"day": 1},
            "recurrence": "daily",
            "details": {
              "type": "IV diuretic therapy",
              "target": "negative 1-2L fluid balance daily",
              "monitoring": ["daily weights", "I&O", "BMP"]
            }
          },
          {
            "id": "daily_labs",
            "type": "observation",
            "timing": {"day": 1},
            "recurrence": "daily",
            "details": {
              "tests": ["BMP", "Magnesium"],
              "purpose": "Monitor electrolytes during diuresis"
            }
          },
          {
            "id": "echo",
            "type": "procedure",
            "timing": {"day": 1, "variance": 1},
            "details": {
              "type": "Transthoracic echocardiogram",
              "cpt": "93306",
              "findings": {
                "ef_range": {"reduced": 0.60, "borderline": 0.25, "preserved": 0.15}
              }
            }
          },
          {
            "id": "cardiology_consult",
            "type": "encounter",
            "timing": {"day": 1},
            "details": {
              "specialty": "Cardiology",
              "purpose": "HF management optimization"
            }
          },
          {
            "id": "medication_optimization",
            "type": "prescription",
            "timing": {"day": 2},
            "details": {
              "gdmt_initiation": [
                {"class": "ace_arb_arni", "if": "not_contraindicated"},
                {"class": "beta_blocker", "if": "hemodynamically_stable"},
                {"class": "mra", "if": "ef_reduced"},
                {"class": "sglt2i", "if": "not_already_on"}
              ]
            }
          },
          {
            "id": "patient_education",
            "type": "encounter",
            "timing": {"day": 2},
            "details": {
              "type": "education",
              "topics": ["daily_weights", "low_sodium_diet", "fluid_restriction", "medication_adherence", "symptom_recognition"]
            }
          },
          {
            "id": "social_work_consult",
            "type": "encounter",
            "timing": {"day": 2, "variance": 1},
            "details": {
              "purpose": "Discharge planning, assess support system",
              "referrals": ["home_health", "meal_delivery", "transportation"]
            }
          }
        ]
      },
      
      {
        "name": "discharge",
        "description": "Discharge planning and transition",
        "duration": "day 3-5",
        "events": [
          {
            "id": "discharge_readiness",
            "type": "observation",
            "timing": {"day": 3},
            "details": {
              "criteria": [
                "Stable on oral diuretics x24h",
                "Ambulating without significant dyspnea",
                "Weight stable",
                "Cr stable or improving",
                "O2 sat >90% on room air"
              ]
            }
          },
          {
            "id": "discharge",
            "type": "discharge",
            "timing": {"day": 4, "variance": 1},
            "details": {
              "disposition": {
                "type": "categorical",
                "weights": {
                  "home": 0.50,
                  "home_with_home_health": 0.35,
                  "snf": 0.12,
                  "ltach": 0.03
                }
              },
              "discharge_meds": [
                "oral_diuretic",
                "ace_arb_arni",
                "beta_blocker",
                "mra",
                "sglt2i"
              ]
            }
          },
          {
            "id": "discharge_labs",
            "type": "observation",
            "timing": {"day_of_discharge": true},
            "details": {
              "tests": ["BMP", "BNP"],
              "purpose": "Baseline for outpatient comparison"
            }
          },
          {
            "id": "tcm_call_scheduled",
            "type": "administrative",
            "timing": {"day_of_discharge": true},
            "details": {
              "tcm_call": {"within": "2 business days"},
              "pcp_followup": {"within": "7 days"},
              "cardiology_followup": {"within": "14 days"}
            }
          }
        ]
      },
      
      {
        "name": "transitional_care",
        "description": "High-intensity post-discharge period",
        "duration": "14 days",
        "events": [
          {
            "id": "tcm_phone_call",
            "type": "encounter",
            "timing": {"day": 2, "after": "discharge"},
            "details": {
              "type": "telephone",
              "cpt": "99495",
              "purpose": "Medication reconciliation, symptom check, appointment confirmation"
            }
          },
          {
            "id": "home_health_visit",
            "type": "encounter",
            "timing": {"day": 2, "after": "discharge"},
            "condition": "discharge_to_home_health",
            "recurrence": {"frequency": "3x_week", "duration": "2 weeks"},
            "details": {
              "services": ["vital_signs", "weight", "medication_review", "symptom_assessment"]
            }
          },
          {
            "id": "pcp_followup",
            "type": "encounter",
            "timing": {"day": 5, "after": "discharge", "variance": 2},
            "details": {
              "visit_type": "99215",
              "cpt_tcm": "99495",
              "purpose": "TCM visit, medication review, volume assessment",
              "orders": ["BMP", "BNP"]
            }
          },
          {
            "id": "post_discharge_labs",
            "type": "observation",
            "timing": {"day": 7, "after": "discharge"},
            "details": {
              "tests": ["BMP", "Magnesium"],
              "purpose": "Monitor renal function and electrolytes on diuretics"
            }
          },
          {
            "id": "cardiology_followup",
            "type": "encounter",
            "timing": {"day": 12, "after": "discharge", "variance": 3},
            "details": {
              "specialty": "Cardiology",
              "visit_type": "99214",
              "purpose": "GDMT optimization, assess for device therapy"
            }
          }
        ]
      },
      
      {
        "name": "ongoing_monitoring",
        "description": "Continued outpatient management",
        "duration": "30 days",
        "events": [
          {
            "id": "monthly_visit",
            "type": "encounter",
            "timing": {"day": 30, "after": "discharge"},
            "details": {
              "visit_type": "99214",
              "purpose": "Ongoing HF management",
              "orders": ["BMP", "BNP if symptomatic"]
            }
          },
          {
            "id": "medication_refills",
            "type": "prescription",
            "timing": {"day": 25, "after": "discharge"},
            "details": {
              "medications": ["loop_diuretic", "ace_arb", "beta_blocker", "mra"],
              "refill": true
            }
          },
          {
            "id": "cardiac_rehab_referral",
            "type": "referral",
            "timing": {"day": 14, "after": "discharge"},
            "condition": "stable_and_eligible",
            "details": {
              "program": "Cardiac rehabilitation",
              "sessions": 36,
              "duration": "12 weeks"
            }
          }
        ]
      }
    ],
    
    "branching_rules": [
      {
        "id": "icu_admission",
        "condition": "hemodynamic_instability OR respiratory_failure",
        "probability": 0.30,
        "action": "icu_pathway",
        "events": [
          {"type": "procedure", "details": {"inotropes": true}},
          {"type": "procedure", "details": {"bipap_or_intubation": true}}
        ]
      },
      {
        "id": "readmission",
        "condition": "random",
        "probability": 0.22,
        "timing": "within 30 days",
        "action": "readmission_event",
        "reasons": [
          {"reason": "volume_overload", "weight": 0.50},
          {"reason": "medication_nonadherence", "weight": 0.20},
          {"reason": "dietary_indiscretion", "weight": 0.15},
          {"reason": "infection", "weight": 0.10},
          {"reason": "arrhythmia", "weight": 0.05}
        ]
      },
      {
        "id": "device_evaluation",
        "condition": "ef <= 35 AND on_gdmt_3months",
        "action": "icd_crt_evaluation",
        "timing": "3 months post discharge"
      }
    ],
    
    "quality_measures": {
      "cms_hf_measures": [
        {"measure": "HF-1", "description": "Discharge instructions", "target": 0.95},
        {"measure": "HF-2", "description": "LV function assessment", "target": 0.98},
        {"measure": "HF-3", "description": "ACEi/ARB at discharge", "target": 0.90}
      ],
      "readmission_target": 0.20,
      "tcm_completion_target": 0.80,
      "7_day_followup_target": 0.75
    }
  },
  
  "cross_product": {
    "patientsim": {
      "entities": ["encounters", "observations", "procedures", "medications", "conditions"],
      "formats": ["fhir_r4"]
    },
    "membersim": {
      "entities": ["facility_claims", "professional_claims", "snf_claims"],
      "formats": ["x12_837i", "x12_837p"]
    },
    "rxmembersim": {
      "entities": ["prescriptions", "fills"],
      "formats": ["ncpdp_d0"]
    }
  },
  
  "customizable": {
    "severity": "Adjust ICU rate, LOS",
    "readmission_rate": "Set target readmission rate",
    "discharge_destination": "Adjust home vs SNF rates",
    "device_therapy": "Include ICD/CRT evaluation",
    "extend_duration": "Extend to 90 days for longer follow-up"
  }
}
```

## Expected Timeline

| Day | Key Events |
|-----|------------|
| 0 | ER presentation, admission |
| 1-2 | IV diuresis, echo, cardiology consult |
| 2-3 | GDMT optimization, patient education |
| 4 | Discharge (average) |
| D+2 | TCM phone call, home health starts |
| D+5-7 | PCP TCM visit, post-discharge labs |
| D+12-14 | Cardiology follow-up |
| D+14 | Cardiac rehab referral |
| D+30 | Monthly follow-up, readmission window closes |

## Cost Profile

| Component | Typical Range |
|-----------|--------------|
| Inpatient (DRG 291) | $12,000 - $25,000 |
| Physician (Hospital) | $1,500 - $3,000 |
| TCM Services | $200 - $400 |
| Follow-up Visits | $300 - $600 |
| Labs/Imaging | $500 - $1,500 |
| Home Health (2 weeks) | $1,500 - $3,000 |
| Medications (30 days) | $200 - $800 |
| **Total Episode** | **$16,200 - $34,300** |

## Related Templates

- [Medicare Advantage Complex](../profiles/medicare-advantage-complex.md) - High-risk population
- [Diabetic First Year](diabetic-first-year.md) - Chronic disease management
- [Care Transition](care-transition.md) - Hospital to home transitions

---

*Part of the HealthSim Generative Framework Template Library*
