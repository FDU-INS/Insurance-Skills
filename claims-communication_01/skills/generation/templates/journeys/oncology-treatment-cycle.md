---
name: oncology-treatment-cycle-journey
description: Chemotherapy or immunotherapy treatment cycle journey
type: journey_template
---

# Oncology Treatment Cycle Journey Template

Complete care journey for a single cycle of systemic cancer therapy (chemotherapy, immunotherapy, or targeted therapy).

## Quick Start

```
User: "Use the oncology treatment cycle journey for breast cancer"

Claude: "Using journey template 'oncology_treatment_cycle':

21-day treatment cycle with:
- Day 1 infusion
- Lab monitoring
- Supportive care
- Toxicity management
- Follow-up assessments

Regimen: AC-T (Adriamycin/Cyclophosphamide → Taxol)?
Or specify different regimen?"
```

## Journey Specification

```json
{
  "template": {
    "id": "oncology_treatment_cycle",
    "name": "Oncology Systemic Treatment Cycle",
    "version": "1.0",
    "duration": "21-28 days",
    "category": "treatment",
    "tags": ["oncology", "chemotherapy", "immunotherapy", "treatment_cycle"]
  },
  
  "journey": {
    "start_trigger": "cycle_day_1",
    "cycle_length": {
      "type": "variable",
      "options": {
        "q21d": 21,
        "q28d": 28,
        "q14d": 14,
        "weekly": 7
      }
    },
    
    "regimen_patterns": {
      "breast_ac": {
        "name": "AC (Doxorubicin/Cyclophosphamide)",
        "cycle_length": 21,
        "cycles": 4,
        "schedule": "Day 1"
      },
      "breast_taxol": {
        "name": "Paclitaxel (Weekly)",
        "cycle_length": 7,
        "cycles": 12,
        "schedule": "Day 1 weekly"
      },
      "lung_pembrolizumab": {
        "name": "Pembrolizumab",
        "cycle_length": 21,
        "cycles": "until_progression",
        "schedule": "Day 1"
      },
      "colon_folfox": {
        "name": "FOLFOX",
        "cycle_length": 14,
        "cycles": 12,
        "schedule": "Day 1-2"
      },
      "lymphoma_rchop": {
        "name": "R-CHOP",
        "cycle_length": 21,
        "cycles": 6,
        "schedule": "Day 1"
      }
    },
    
    "phases": [
      {
        "name": "pre_cycle",
        "description": "Pre-treatment assessment and clearance",
        "duration": "1-3 days before",
        "events": [
          {
            "id": "pre_treatment_labs",
            "type": "observation",
            "timing": {"day": -2, "variance": 1},
            "details": {
              "panels": [
                {"name": "CBC with diff", "required": true},
                {"name": "CMP", "required": true},
                {"name": "LFTs", "required": true},
                {"name": "Tumor markers", "conditional": "if_applicable"}
              ],
              "clearance_criteria": {
                "anc": {"min": 1500},
                "platelets": {"min": 100000},
                "cr_clearance": {"min": 30},
                "bilirubin": {"max": 1.5}
              }
            }
          },
          {
            "id": "pre_treatment_visit",
            "type": "encounter",
            "timing": {"day": -1, "variance": 1},
            "details": {
              "visit_type": "99214",
              "specialty": "Medical Oncology",
              "assessments": [
                "Symptom assessment",
                "ECOG performance status",
                "Prior cycle toxicity review",
                "Treatment clearance"
              ]
            }
          }
        ]
      },
      
      {
        "name": "treatment_day",
        "description": "Infusion and immediate supportive care",
        "duration": "day 1",
        "events": [
          {
            "id": "infusion_encounter",
            "type": "encounter",
            "timing": {"day": 1, "time": "08:00"},
            "details": {
              "encounter_type": "outpatient_infusion",
              "place_of_service": "22",
              "duration_hours": {
                "type": "variable",
                "by_regimen": {
                  "ac": 3,
                  "taxol": 4,
                  "pembrolizumab": 1,
                  "folfox": 8,
                  "rchop": 6
                }
              }
            }
          },
          {
            "id": "pre_medications",
            "type": "procedure",
            "timing": {"day": 1, "before": "infusion"},
            "details": {
              "medications": [
                {"name": "Ondansetron", "dose": "8mg IV"},
                {"name": "Dexamethasone", "dose": "12mg IV", "conditional": "taxane_or_io"},
                {"name": "Diphenhydramine", "dose": "25mg IV", "conditional": "taxane"},
                {"name": "Famotidine", "dose": "20mg IV", "conditional": "taxane"}
              ]
            }
          },
          {
            "id": "chemotherapy_infusion",
            "type": "procedure",
            "timing": {"day": 1},
            "details": {
              "type": "chemotherapy_administration",
              "j_codes": {
                "doxorubicin": "J9000",
                "cyclophosphamide": "J9070",
                "paclitaxel": "J9267",
                "pembrolizumab": "J9271",
                "oxaliplatin": "J9263",
                "rituximab": "J9312"
              },
              "administration_codes": ["96413", "96415", "96417"]
            }
          },
          {
            "id": "post_infusion_monitoring",
            "type": "observation",
            "timing": {"day": 1, "after": "infusion"},
            "details": {
              "vital_signs": true,
              "duration_minutes": 30,
              "reaction_monitoring": true
            }
          }
        ]
      },
      
      {
        "name": "supportive_care",
        "description": "Home medications and supportive care",
        "duration": "days 2-7",
        "events": [
          {
            "id": "antiemetic_rx",
            "type": "prescription",
            "timing": {"day": 1},
            "details": {
              "medications": [
                {"name": "Ondansetron 8mg", "frequency": "Q8H PRN", "days_supply": 5},
                {"name": "Prochlorperazine 10mg", "frequency": "Q6H PRN", "days_supply": 5},
                {"name": "Dexamethasone 4mg", "frequency": "BID x 3 days", "conditional": "high_emetogenic"}
              ]
            }
          },
          {
            "id": "growth_factor",
            "type": "prescription",
            "timing": {"day": 2},
            "condition": "high_risk_febrile_neutropenia",
            "details": {
              "options": [
                {"name": "Pegfilgrastim", "timing": "Day 2", "j_code": "J2505"},
                {"name": "Filgrastim", "timing": "Days 2-7", "j_code": "J1442"}
              ]
            }
          },
          {
            "id": "symptom_call",
            "type": "outreach",
            "timing": {"day": 3, "variance": 1},
            "details": {
              "type": "nursing_call",
              "purpose": "Symptom check, toxicity assessment",
              "escalation": "if_grade_3_toxicity"
            }
          }
        ]
      },
      
      {
        "name": "nadir_monitoring",
        "description": "Monitoring during nadir period",
        "duration": "days 7-14",
        "events": [
          {
            "id": "nadir_labs",
            "type": "observation",
            "timing": {"day": 10, "variance": 2},
            "condition": "first_cycle OR high_risk",
            "details": {
              "panels": ["CBC with diff"],
              "purpose": "Nadir assessment"
            }
          },
          {
            "id": "toxicity_visit",
            "type": "encounter",
            "timing": {"day": 10, "variance": 3},
            "condition": "grade_3_toxicity OR patient_concern",
            "details": {
              "visit_type": "99213",
              "purpose": "Toxicity management"
            }
          }
        ]
      },
      
      {
        "name": "recovery",
        "description": "Recovery before next cycle",
        "duration": "days 14-21",
        "events": [
          {
            "id": "restaging_imaging",
            "type": "procedure",
            "timing": {"day": 18},
            "condition": "every_2_cycles OR end_of_treatment",
            "details": {
              "type": "diagnostic_imaging",
              "modality": {
                "type": "conditional",
                "rules": [
                  {"if": "solid_tumor", "value": "CT_chest_abd_pelvis"},
                  {"if": "lymphoma", "value": "PET_CT"},
                  {"if": "breast", "value": "CT_or_bone_scan"}
                ]
              }
            }
          },
          {
            "id": "oncology_followup",
            "type": "encounter",
            "timing": {"day": 19, "variance": 2},
            "condition": "restaging_performed",
            "details": {
              "visit_type": "99215",
              "purpose": "Review imaging, assess response, plan next cycle"
            }
          }
        ]
      }
    ],
    
    "branching_rules": [
      {
        "id": "treatment_delay",
        "condition": "anc < 1500 OR platelets < 100000",
        "probability": 0.15,
        "action": "delay_1_week",
        "events": [
          {"type": "observation", "details": {"repeat_labs": true, "timing": 7}},
          {"type": "administrative", "details": {"reschedule_infusion": true}}
        ]
      },
      {
        "id": "dose_reduction",
        "condition": "grade_3_4_toxicity",
        "probability": 0.10,
        "action": "reduce_dose_25_percent",
        "documentation": "Dose modification per protocol"
      },
      {
        "id": "febrile_neutropenia",
        "condition": "fever AND anc < 500",
        "probability": 0.08,
        "action": "hospitalization",
        "events": [
          {"type": "encounter", "details": {"er_visit": true}},
          {"type": "admission", "details": {"indication": "febrile_neutropenia", "los": 3}}
        ]
      },
      {
        "id": "infusion_reaction",
        "condition": "random",
        "probability": 0.05,
        "action": "manage_reaction",
        "events": [
          {"type": "procedure", "details": {"stop_infusion": true}},
          {"type": "procedure", "details": {"treat_reaction": true}},
          {"type": "procedure", "details": {"rechallenge_slower": true}}
        ]
      },
      {
        "id": "disease_progression",
        "condition": "restaging_shows_progression",
        "probability": 0.15,
        "action": "change_regimen",
        "events": [
          {"type": "encounter", "details": {"tumor_board": true}},
          {"type": "administrative", "details": {"new_treatment_plan": true}}
        ]
      }
    ],
    
    "toxicity_monitoring": {
      "common_toxicities": [
        {"name": "Nausea", "grade_1_2": 0.60, "grade_3_4": 0.10},
        {"name": "Fatigue", "grade_1_2": 0.70, "grade_3_4": 0.15},
        {"name": "Neutropenia", "grade_1_2": 0.40, "grade_3_4": 0.25},
        {"name": "Neuropathy", "grade_1_2": 0.35, "grade_3_4": 0.05, "conditional": "taxane"},
        {"name": "Diarrhea", "grade_1_2": 0.30, "grade_3_4": 0.08},
        {"name": "Mucositis", "grade_1_2": 0.25, "grade_3_4": 0.05}
      ],
      "ctcae_version": "5.0"
    }
  },
  
  "cross_product": {
    "patientsim": {
      "entities": ["encounters", "procedures", "observations", "medications", "conditions"],
      "formats": ["fhir_r4"]
    },
    "membersim": {
      "entities": ["professional_claims", "drug_claims"],
      "formats": ["x12_837p"]
    },
    "rxmembersim": {
      "entities": ["prescriptions", "specialty_fills"],
      "formats": ["ncpdp_d0"]
    },
    "trialsim": {
      "entities": ["visits", "adverse_events", "response_assessment"],
      "conditional": "if_trial_subject"
    }
  },
  
  "customizable": {
    "regimen": "Select specific chemotherapy regimen",
    "cycle_number": "Which cycle in treatment course",
    "toxicity_rate": "Adjust toxicity probabilities",
    "trial_context": "Add clinical trial protocol elements",
    "io_specific": "Add immunotherapy-specific monitoring"
  }
}
```

## Expected Timeline (21-day cycle)

| Day | Key Events |
|-----|------------|
| -2 to -1 | Pre-treatment labs, oncology visit |
| 1 | Chemotherapy infusion |
| 1-3 | Antiemetics, supportive care |
| 2 | Growth factor (if indicated) |
| 3 | Nursing symptom call |
| 7-10 | Nadir period, labs if needed |
| 18-19 | Restaging (if applicable) |
| 21 | Next cycle begins |

## Cost Profile (Per Cycle)

| Component | Typical Range |
|-----------|--------------|
| Chemotherapy drugs | $1,000 - $15,000+ |
| Administration (J codes) | $500 - $2,000 |
| Physician visit | $200 - $400 |
| Labs | $200 - $500 |
| Growth factor | $3,000 - $8,000 |
| Imaging (every 2 cycles) | $1,500 - $3,000 |
| Supportive meds | $100 - $500 |
| **Total per cycle** | **$5,500 - $29,400+** |

## Related Templates

- [TrialSim Clinical Trials](../../../trialsim/SKILL.md) - Clinical trial context
- [TrialSim Phase 3](../../../trialsim/phase3-pivotal.md) - Pivotal trial protocols
- [Surgical Episode](surgical-episode.md) - Pre/post surgical care

---

*Part of the HealthSim Generative Framework Template Library*
