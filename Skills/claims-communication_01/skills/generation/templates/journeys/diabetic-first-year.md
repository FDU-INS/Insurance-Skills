---
name: diabetic-first-year-journey
description: First year care journey for newly diagnosed Type 2 diabetes
type: journey_template
---

# Diabetic First Year Journey Template

Timeline of care events for newly diagnosed Type 2 diabetes patients through their first year of management.

## Quick Start

```
User: "Use the diabetic first year journey"

Claude: "Using journey template 'diabetic_first_year':

12-month timeline with:
- Initial diagnosis and treatment start
- Medication titration period
- Quarterly monitoring
- Specialist referrals (eye, nutrition)
- Possible treatment intensification

Attach to profile or generate standalone?"
```

## Journey Specification

```json
{
  "template": {
    "id": "diabetic_first_year",
    "name": "Type 2 Diabetes First Year Journey",
    "version": "1.0",
    "duration": "12 months",
    "category": "chronic_disease",
    "tags": ["diabetes", "new_diagnosis", "longitudinal"]
  },
  
  "journey": {
    "start_trigger": "diagnosis_date",
    
    "phases": [
      {
        "name": "initial_diagnosis",
        "description": "Initial diagnosis, workup, and treatment initiation",
        "duration": "1 month",
        "events": [
          {
            "id": "initial_visit",
            "type": "encounter",
            "timing": {"day": 0},
            "details": {
              "encounter_type": "ambulatory",
              "visit_type": "99215",
              "diagnoses": ["E11.9"],
              "purpose": "New diabetes diagnosis and treatment planning"
            }
          },
          {
            "id": "initial_labs",
            "type": "observation",
            "timing": {"day": 0},
            "details": {
              "panels": ["HbA1c", "CMP", "Lipid Panel", "Urinalysis"],
              "purpose": "Baseline assessment"
            }
          },
          {
            "id": "metformin_start",
            "type": "prescription",
            "timing": {"day": 0},
            "details": {
              "medication": "metformin",
              "dose": "500mg",
              "frequency": "BID",
              "days_supply": 30,
              "refills": 5,
              "instructions": "Take with meals, start low and titrate"
            }
          },
          {
            "id": "diabetes_education",
            "type": "referral",
            "timing": {"day": 7, "variance": 7},
            "details": {
              "specialty": "Diabetes Self-Management Education (DSME)",
              "sessions": 10,
              "purpose": "Comprehensive diabetes education"
            }
          },
          {
            "id": "nutrition_referral",
            "type": "referral",
            "timing": {"day": 14, "variance": 7},
            "details": {
              "specialty": "Medical Nutrition Therapy",
              "sessions": 3,
              "purpose": "Dietary counseling for diabetes management"
            }
          }
        ]
      },
      
      {
        "name": "titration",
        "description": "Medication adjustment based on response",
        "duration": "2 months",
        "events": [
          {
            "id": "titration_visit",
            "type": "encounter",
            "timing": {"week": 4},
            "details": {
              "visit_type": "99214",
              "purpose": "Medication tolerance and titration"
            }
          },
          {
            "id": "metformin_increase",
            "type": "prescription",
            "timing": {"week": 4},
            "condition": "tolerating_well",
            "details": {
              "medication": "metformin",
              "dose": "1000mg",
              "frequency": "BID",
              "days_supply": 30
            }
          },
          {
            "id": "followup_labs",
            "type": "observation",
            "timing": {"week": 8},
            "details": {
              "panels": ["HbA1c", "BMP"],
              "purpose": "Check response to treatment"
            }
          }
        ]
      },
      
      {
        "name": "stabilization",
        "description": "Establishing routine care pattern",
        "duration": "3 months",
        "events": [
          {
            "id": "quarterly_visit_1",
            "type": "encounter",
            "timing": {"month": 3},
            "details": {
              "visit_type": "99214",
              "orders": ["HbA1c", "CMP"],
              "assessments": ["foot_exam", "weight", "blood_pressure"]
            }
          },
          {
            "id": "eye_exam_referral",
            "type": "referral",
            "timing": {"month": 4, "variance": 14},
            "details": {
              "specialty": "Ophthalmology",
              "exam_type": "Dilated fundoscopic exam",
              "purpose": "Baseline diabetic retinopathy screening"
            }
          },
          {
            "id": "eye_exam",
            "type": "encounter",
            "timing": {"month": 5, "variance": 14},
            "details": {
              "encounter_type": "specialist",
              "specialty": "Ophthalmology",
              "visit_type": "92004"
            }
          }
        ]
      },
      
      {
        "name": "ongoing_management",
        "description": "Established quarterly care with monitoring",
        "duration": "6 months",
        "events": [
          {
            "id": "quarterly_visits",
            "type": "encounter",
            "recurrence": "quarterly",
            "details": {
              "visit_type": "99214",
              "orders": ["HbA1c", "CMP", "Lipid Panel"],
              "assessments": ["foot_exam", "weight", "blood_pressure"]
            }
          },
          {
            "id": "medication_refills",
            "type": "prescription",
            "recurrence": "monthly",
            "details": {
              "medication": "metformin",
              "refill": true
            }
          },
          {
            "id": "annual_labs",
            "type": "observation",
            "timing": {"month": 12},
            "details": {
              "panels": ["HbA1c", "CMP", "Lipid Panel", "TSH", "Urinalysis with microalbumin", "Vitamin B12"],
              "purpose": "Comprehensive annual labs"
            }
          }
        ]
      }
    ],
    
    "branching_rules": [
      {
        "id": "intensify_treatment",
        "condition": "a1c > 8.0 at month 6",
        "description": "Add second agent if not at goal",
        "action": "add_second_agent",
        "options": [
          {"medication": "glipizide", "weight": 0.35},
          {"medication": "empagliflozin", "weight": 0.35},
          {"medication": "semaglutide", "weight": 0.30}
        ]
      },
      {
        "id": "start_insulin",
        "condition": "a1c > 10.0 at month 6",
        "description": "Consider basal insulin for very uncontrolled",
        "action": "add_basal_insulin",
        "probability": 0.6
      },
      {
        "id": "nephrology_referral",
        "condition": "egfr < 45 OR uacr > 300",
        "description": "Nephrology referral for CKD",
        "action": "specialist_referral",
        "specialty": "Nephrology"
      }
    ],
    
    "quality_measures": [
      {"measure": "A1c testing", "target": "Every 3 months", "hedis": "CDC - HbA1c Testing"},
      {"measure": "A1c control", "target": "< 8.0%", "hedis": "CDC - HbA1c Control (<8%)"},
      {"measure": "Eye exam", "target": "Annual", "hedis": "CDC - Eye Exam"},
      {"measure": "Nephropathy screening", "target": "Annual", "hedis": "CDC - Nephropathy"}
    ]
  },
  
  "cross_product": {
    "patientsim": {
      "entities": ["encounters", "observations", "medications", "conditions"],
      "formats": ["fhir_r4"]
    },
    "membersim": {
      "entities": ["professional_claims", "facility_claims"],
      "formats": ["x12_837"]
    },
    "rxmembersim": {
      "entities": ["prescriptions", "fills"],
      "formats": ["ncpdp_d0"]
    }
  },
  
  "customizable": {
    "duration": "Extend to 18 or 24 months",
    "visit_frequency": "Increase to monthly if needed",
    "specialist_referrals": "Add cardiology, podiatry",
    "second_agent_threshold": "Adjust A1c trigger",
    "medication_preferences": "Preferred formulary agents"
  }
}
```

## Expected Timeline

| Month | Key Events |
|-------|------------|
| 0 | Initial diagnosis, labs, metformin start |
| 0-1 | Diabetes education, nutrition counseling |
| 1 | Titration visit, metformin increase |
| 2 | Follow-up labs |
| 3 | Quarterly visit with A1c |
| 4-5 | Eye exam |
| 6 | Quarterly visit, treatment intensification if needed |
| 9 | Quarterly visit |
| 12 | Annual comprehensive visit and labs |

## Branching Cohorts

### Standard Pathway (78%)
- A1c < 8.0 at 6 months
- Continue metformin monotherapy
- Regular quarterly monitoring

### Treatment Intensification (22%)
- A1c ≥ 8.0 at 6 months
- Add second agent (sulfonylurea, SGLT2i, or GLP-1)
- More frequent monitoring

## Related Templates

- [Diabetic Annual](diabetic-annual.md) - Ongoing annual management
- [CHF First Year](chf-first-year.md) - Heart failure journey
- [New Member Onboarding](new-member-onboarding.md) - Plan enrollment journey

---

*Part of the HealthSim Generative Framework Template Library*
