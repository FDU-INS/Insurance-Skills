---
name: surgical-episode-journey
description: Pre-op through recovery journey for elective surgery
type: journey_template
---

# Surgical Episode Journey Template

Complete care journey from surgical consultation through post-operative recovery.

## Quick Start

```
User: "Use the surgical episode journey for knee replacement"

Claude: "Using journey template 'surgical_episode':

3-month timeline with:
- Pre-operative evaluation and clearance
- Surgery and hospital stay
- Acute post-op recovery
- Rehab and follow-up visits

Attach to profile or customize procedure?"
```

## Journey Specification

```json
{
  "template": {
    "id": "surgical_episode",
    "name": "Elective Surgical Episode",
    "version": "1.0",
    "duration": "3 months",
    "category": "episode",
    "tags": ["surgery", "elective", "episode", "bundled"]
  },
  
  "journey": {
    "start_trigger": "surgical_consult_date",
    "procedure_types": ["joint_replacement", "spine", "bariatric", "cardiac", "general"],
    
    "phases": [
      {
        "name": "pre_operative",
        "description": "Evaluation, clearance, and preparation",
        "duration": "4-6 weeks",
        "events": [
          {
            "id": "surgical_consult",
            "type": "encounter",
            "timing": {"day": 0},
            "details": {
              "encounter_type": "specialist",
              "specialty": "Orthopedic Surgery",
              "visit_type": "99244",
              "purpose": "Surgical consultation and decision"
            }
          },
          {
            "id": "pre_op_testing",
            "type": "encounter",
            "timing": {"week": -3, "variance": 7},
            "details": {
              "visit_type": "99213",
              "purpose": "Pre-operative testing and clearance"
            }
          },
          {
            "id": "pre_op_labs",
            "type": "observation",
            "timing": {"week": -3, "variance": 7},
            "details": {
              "panels": ["CBC", "CMP", "PT/INR", "Type and Screen"],
              "purpose": "Surgical clearance labs"
            }
          },
          {
            "id": "pre_op_imaging",
            "type": "procedure",
            "timing": {"week": -3, "variance": 7},
            "details": {
              "type": "diagnostic_imaging",
              "procedures": ["Chest X-Ray", "EKG"],
              "cpt_codes": ["71046", "93000"]
            }
          },
          {
            "id": "cardiology_clearance",
            "type": "encounter",
            "timing": {"week": -2, "variance": 7},
            "condition": "age > 50 OR cardiac_history",
            "details": {
              "specialty": "Cardiology",
              "visit_type": "99243",
              "purpose": "Cardiac risk assessment"
            }
          },
          {
            "id": "preadmission_class",
            "type": "encounter",
            "timing": {"week": -1},
            "details": {
              "type": "education",
              "purpose": "Joint replacement class / surgical preparation"
            }
          }
        ]
      },
      
      {
        "name": "surgical",
        "description": "Surgery and acute hospital stay",
        "duration": "2-4 days",
        "events": [
          {
            "id": "admission",
            "type": "admission",
            "timing": {"day": 0, "time": "06:00"},
            "details": {
              "admission_type": "elective",
              "admission_source": "physician_referral"
            }
          },
          {
            "id": "surgery",
            "type": "procedure",
            "timing": {"day": 0, "time": "08:00"},
            "details": {
              "procedure_type": "surgical",
              "cpt_joint_replacement": "27447",
              "description": "Total knee arthroplasty",
              "anesthesia": "general",
              "duration_hours": 2.5
            }
          },
          {
            "id": "inpatient_pt",
            "type": "procedure",
            "timing": {"day": 1},
            "recurrence": "daily",
            "details": {
              "type": "physical_therapy",
              "cpt": "97110",
              "purpose": "Acute post-op mobility"
            }
          },
          {
            "id": "discharge",
            "type": "discharge",
            "timing": {"day": 2, "variance": 1},
            "details": {
              "disposition": {
                "type": "conditional",
                "rules": [
                  {"if": "age < 65 AND support_at_home", "value": "home", "probability": 0.70},
                  {"if": "age >= 65 OR no_support", "value": "snf", "probability": 0.25},
                  {"else": true, "value": "home_health", "probability": 0.05}
                ]
              }
            }
          }
        ]
      },
      
      {
        "name": "acute_recovery",
        "description": "First 2 weeks post-discharge",
        "duration": "2 weeks",
        "events": [
          {
            "id": "home_health",
            "type": "encounter",
            "timing": {"day": 1, "after": "discharge"},
            "condition": "discharge_to_home",
            "recurrence": {"every": 2, "unit": "days", "count": 5},
            "details": {
              "type": "home_health_visit",
              "services": ["wound_care", "pt", "medication_management"]
            }
          },
          {
            "id": "snf_stay",
            "type": "encounter",
            "timing": {"day": 1, "after": "discharge"},
            "condition": "discharge_to_snf",
            "duration": "7-14 days",
            "details": {
              "type": "snf",
              "services": ["skilled_nursing", "pt", "ot"]
            }
          },
          {
            "id": "post_op_visit_1",
            "type": "encounter",
            "timing": {"week": 2, "after": "surgery"},
            "details": {
              "specialty": "Orthopedic Surgery",
              "visit_type": "99213",
              "purpose": "Wound check, staple removal"
            }
          }
        ]
      },
      
      {
        "name": "rehabilitation",
        "description": "Outpatient PT and recovery",
        "duration": "6-8 weeks",
        "events": [
          {
            "id": "outpatient_pt",
            "type": "encounter",
            "timing": {"week": 3, "after": "surgery"},
            "recurrence": {"frequency": "3x_weekly", "duration": "6 weeks"},
            "details": {
              "type": "physical_therapy",
              "cpt_codes": ["97110", "97140", "97530"],
              "purpose": "Strength and range of motion"
            }
          },
          {
            "id": "post_op_visit_2",
            "type": "encounter",
            "timing": {"week": 6, "after": "surgery"},
            "details": {
              "specialty": "Orthopedic Surgery",
              "visit_type": "99214",
              "purpose": "6-week follow-up, imaging"
            }
          },
          {
            "id": "post_op_xray",
            "type": "procedure",
            "timing": {"week": 6, "after": "surgery"},
            "details": {
              "type": "diagnostic_imaging",
              "cpt": "73560",
              "description": "Knee X-ray 2 views"
            }
          }
        ]
      },
      
      {
        "name": "final_recovery",
        "description": "Return to normal activity",
        "duration": "4 weeks",
        "events": [
          {
            "id": "post_op_visit_3",
            "type": "encounter",
            "timing": {"week": 12, "after": "surgery"},
            "details": {
              "specialty": "Orthopedic Surgery",
              "visit_type": "99213",
              "purpose": "Final follow-up, return to activity"
            }
          },
          {
            "id": "pt_discharge",
            "type": "encounter",
            "timing": {"week": 10, "after": "surgery", "variance": 14},
            "details": {
              "type": "physical_therapy",
              "purpose": "PT discharge, home exercise program"
            }
          }
        ]
      }
    ],
    
    "branching_rules": [
      {
        "id": "complication_infection",
        "condition": "random",
        "probability": 0.02,
        "action": "surgical_site_infection",
        "events": [
          {"type": "encounter", "details": {"er_visit": true, "diagnosis": "T84.54XA"}},
          {"type": "admission", "details": {"los": 5}},
          {"type": "procedure", "details": {"irrigation_debridement": true}}
        ]
      },
      {
        "id": "complication_dvt",
        "condition": "random",
        "probability": 0.01,
        "action": "deep_vein_thrombosis",
        "events": [
          {"type": "encounter", "details": {"diagnosis": "I82.409"}},
          {"type": "prescription", "details": {"anticoagulation": true}}
        ]
      },
      {
        "id": "readmission",
        "condition": "random",
        "probability": 0.05,
        "action": "30_day_readmission",
        "reasons": ["pain_management", "wound_issue", "fall", "medical_complication"]
      }
    ],
    
    "quality_measures": {
      "los_target": {"mean": 2.0, "max": 4},
      "readmission_target": 0.05,
      "infection_rate_target": 0.02,
      "pt_compliance_target": 0.85
    }
  },
  
  "procedure_variants": {
    "total_knee": {
      "cpt": "27447",
      "drg": "470",
      "los": 2,
      "pt_weeks": 8
    },
    "total_hip": {
      "cpt": "27130",
      "drg": "470",
      "los": 2,
      "pt_weeks": 6
    },
    "spine_fusion": {
      "cpt": "22612",
      "drg": "460",
      "los": 3,
      "pt_weeks": 12
    },
    "bariatric": {
      "cpt": "43644",
      "drg": "621",
      "los": 2,
      "pt_weeks": 0
    }
  },
  
  "cross_product": {
    "patientsim": {
      "entities": ["encounters", "procedures", "observations", "conditions"],
      "formats": ["fhir_r4"]
    },
    "membersim": {
      "entities": ["professional_claims", "facility_claims", "snf_claims"],
      "formats": ["x12_837i", "x12_837p"]
    }
  },
  
  "customizable": {
    "procedure_type": "Select from procedure_variants",
    "complication_rate": "Adjust complication probabilities",
    "snf_rate": "Adjust discharge to SNF rate",
    "pt_intensity": "Adjust PT frequency/duration"
  }
}
```

## Expected Timeline

| Week | Key Events |
|------|------------|
| -4 to -3 | Surgical consult, pre-op testing |
| -2 | Cardiac clearance (if needed) |
| -1 | Preadmission class |
| 0 | Surgery, hospital stay (2-3 days) |
| 1-2 | Home health or SNF, acute recovery |
| 2 | Post-op visit #1 (wound check) |
| 3-8 | Outpatient PT (3x/week) |
| 6 | Post-op visit #2 + X-ray |
| 10 | PT discharge |
| 12 | Final follow-up |

## Bundled Payment Compatibility

This journey aligns with CMS BPCI/CJR episode definitions:
- Episode trigger: Inpatient admission for joint replacement
- Episode duration: 90 days post-discharge
- Included services: All related care (hospital, SNF, PT, physician)

## Related Templates

- [Cardiac Surgery Episode](cardiac-surgery-episode.md) - CABG/valve journey
- [Bariatric Episode](bariatric-episode.md) - Weight loss surgery
- [Outpatient Procedure](outpatient-procedure.md) - Same-day surgery

---

*Part of the HealthSim Generative Framework Template Library*
