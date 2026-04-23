---
name: new-member-onboarding-journey
description: First 90 days journey for newly enrolled health plan members
type: journey_template
---

# New Member Onboarding Journey Template

Complete journey from plan enrollment through first utilization and engagement.

## Quick Start

```
User: "Use the new member onboarding journey"

Claude: "Using journey template 'new_member_onboarding':

90-day timeline with:
- Enrollment and ID card issuance
- Welcome call and PCP assignment
- Initial health assessment
- First utilization events
- Engagement and gap closure

Attach to profile or customize?"
```

## Journey Specification

```json
{
  "template": {
    "id": "new_member_onboarding",
    "name": "New Member Onboarding Journey",
    "version": "1.0",
    "duration": "90 days",
    "category": "lifecycle",
    "tags": ["enrollment", "onboarding", "engagement", "new_member"]
  },
  
  "journey": {
    "start_trigger": "effective_date",
    "coverage_types": ["commercial", "medicare_advantage", "medicaid", "exchange"],
    
    "phases": [
      {
        "name": "enrollment",
        "description": "Plan enrollment and administrative setup",
        "duration": "1 week",
        "events": [
          {
            "id": "enrollment_transaction",
            "type": "administrative",
            "timing": {"day": -14, "before": "effective_date"},
            "details": {
              "transaction_type": "834_enrollment",
              "enrollment_type": {
                "type": "categorical",
                "weights": {
                  "open_enrollment": 0.60,
                  "new_hire": 0.25,
                  "special_enrollment": 0.10,
                  "aging_in": 0.05
                }
              }
            }
          },
          {
            "id": "id_card_mailed",
            "type": "administrative",
            "timing": {"day": -7, "before": "effective_date"},
            "details": {
              "type": "fulfillment",
              "item": "member_id_card"
            }
          },
          {
            "id": "welcome_packet",
            "type": "administrative",
            "timing": {"day": -5, "before": "effective_date"},
            "details": {
              "type": "fulfillment",
              "items": ["welcome_letter", "plan_documents", "provider_directory"]
            }
          },
          {
            "id": "effective_date",
            "type": "administrative",
            "timing": {"day": 0},
            "details": {
              "type": "coverage_effective",
              "eligibility_status": "active"
            }
          }
        ]
      },
      
      {
        "name": "welcome_outreach",
        "description": "Initial member engagement and PCP assignment",
        "duration": "2 weeks",
        "events": [
          {
            "id": "welcome_call",
            "type": "outreach",
            "timing": {"day": 3, "variance": 2},
            "details": {
              "channel": "phone",
              "purpose": "Welcome, verify information, answer questions",
              "completion_rate": 0.45
            }
          },
          {
            "id": "pcp_assignment",
            "type": "administrative",
            "timing": {"day": 5},
            "details": {
              "type": "provider_assignment",
              "assignment_method": {
                "type": "categorical",
                "weights": {
                  "member_selected": 0.35,
                  "auto_assigned_proximity": 0.40,
                  "auto_assigned_capacity": 0.20,
                  "previous_provider": 0.05
                }
              }
            }
          },
          {
            "id": "portal_registration",
            "type": "engagement",
            "timing": {"day": 7, "variance": 5},
            "details": {
              "type": "digital_activation",
              "channel": "member_portal",
              "completion_rate": 0.55
            }
          },
          {
            "id": "mobile_app_download",
            "type": "engagement",
            "timing": {"day": 10, "variance": 7},
            "details": {
              "type": "digital_activation",
              "channel": "mobile_app",
              "completion_rate": 0.35
            }
          }
        ]
      },
      
      {
        "name": "health_assessment",
        "description": "Initial health evaluation and risk identification",
        "duration": "4 weeks",
        "events": [
          {
            "id": "hra_invitation",
            "type": "outreach",
            "timing": {"day": 7},
            "details": {
              "type": "health_risk_assessment",
              "channel": "email",
              "incentive": true
            }
          },
          {
            "id": "hra_completion",
            "type": "engagement",
            "timing": {"day": 21, "variance": 14},
            "condition": "hra_invited",
            "details": {
              "type": "health_risk_assessment",
              "completion_rate": 0.40,
              "risk_stratification": {
                "low_risk": 0.55,
                "moderate_risk": 0.30,
                "high_risk": 0.15
              }
            }
          },
          {
            "id": "care_gap_identification",
            "type": "administrative",
            "timing": {"day": 14},
            "details": {
              "type": "gap_analysis",
              "sources": ["claims_history", "hra_responses", "age_gender_guidelines"]
            }
          },
          {
            "id": "care_gap_outreach",
            "type": "outreach",
            "timing": {"day": 21},
            "condition": "gaps_identified",
            "details": {
              "channels": ["mail", "email", "phone"],
              "gap_types": ["preventive_screenings", "chronic_care", "immunizations"]
            }
          }
        ]
      },
      
      {
        "name": "first_utilization",
        "description": "Initial healthcare utilization",
        "duration": "6 weeks",
        "events": [
          {
            "id": "first_pcp_visit",
            "type": "encounter",
            "timing": {"day": 30, "variance": 21},
            "details": {
              "encounter_type": "ambulatory",
              "visit_type": {
                "type": "conditional",
                "rules": [
                  {"if": "new_to_plan AND chronic_conditions", "value": "99215"},
                  {"if": "new_to_plan", "value": "99214"},
                  {"else": true, "value": "99213"}
                ]
              },
              "completion_rate": 0.35
            }
          },
          {
            "id": "first_rx_fill",
            "type": "prescription",
            "timing": {"day": 14, "variance": 14},
            "condition": "has_chronic_condition OR maintenance_meds",
            "details": {
              "fill_type": {
                "type": "categorical",
                "weights": {
                  "transfer_fill": 0.50,
                  "new_prescription": 0.30,
                  "refill": 0.20
                }
              },
              "completion_rate": 0.65
            }
          },
          {
            "id": "preventive_screening",
            "type": "encounter",
            "timing": {"day": 45, "variance": 30},
            "condition": "gap_identified",
            "details": {
              "visit_types": ["mammogram", "colonoscopy", "a1c_test", "annual_wellness"],
              "completion_rate": 0.25
            }
          },
          {
            "id": "specialist_visit",
            "type": "encounter",
            "timing": {"day": 60, "variance": 30},
            "condition": "chronic_condition OR referral_needed",
            "details": {
              "encounter_type": "specialist",
              "completion_rate": 0.20
            }
          }
        ]
      },
      
      {
        "name": "ongoing_engagement",
        "description": "Continued engagement and program enrollment",
        "duration": "4 weeks",
        "events": [
          {
            "id": "disease_management_outreach",
            "type": "outreach",
            "timing": {"day": 45},
            "condition": "high_risk OR chronic_conditions",
            "details": {
              "program": "disease_management",
              "conditions": ["diabetes", "heart_failure", "copd", "asthma"],
              "enrollment_rate": 0.30
            }
          },
          {
            "id": "care_management_enrollment",
            "type": "engagement",
            "timing": {"day": 60, "variance": 14},
            "condition": "high_risk AND dm_outreach_accepted",
            "details": {
              "program": "care_management",
              "intensity": {
                "type": "categorical",
                "weights": {
                  "telephonic": 0.60,
                  "in_person": 0.25,
                  "digital": 0.15
                }
              }
            }
          },
          {
            "id": "wellness_program_enrollment",
            "type": "engagement",
            "timing": {"day": 30, "variance": 30},
            "details": {
              "programs": ["fitness", "nutrition", "smoking_cessation", "stress_management"],
              "enrollment_rate": 0.15
            }
          },
          {
            "id": "90_day_survey",
            "type": "engagement",
            "timing": {"day": 85},
            "details": {
              "type": "member_satisfaction",
              "channel": "email",
              "completion_rate": 0.20
            }
          }
        ]
      }
    ],
    
    "branching_rules": [
      {
        "id": "high_utilizer_path",
        "condition": "claims_30_days >= 3 OR er_visit",
        "action": "accelerated_outreach",
        "events": [
          {"type": "outreach", "details": {"cm_call": true, "day": 7}},
          {"type": "engagement", "details": {"care_plan": true}}
        ]
      },
      {
        "id": "no_utilization_path",
        "condition": "claims_60_days == 0",
        "action": "engagement_outreach",
        "events": [
          {"type": "outreach", "details": {"reminder_call": true}},
          {"type": "outreach", "details": {"pcp_scheduling_assist": true}}
        ]
      },
      {
        "id": "disenrollment",
        "condition": "random",
        "probability": 0.02,
        "action": "early_disenrollment",
        "reasons": ["job_change", "moved", "dissatisfaction", "cost"]
      }
    ],
    
    "kpis": {
      "pcp_assignment_rate": {"target": 0.95, "by_day": 7},
      "portal_activation_rate": {"target": 0.50, "by_day": 30},
      "hra_completion_rate": {"target": 0.35, "by_day": 45},
      "first_pcp_visit_rate": {"target": 0.30, "by_day": 90},
      "rx_adherence_rate": {"target": 0.80, "by_day": 90},
      "member_satisfaction": {"target": 4.0, "scale": 5}
    }
  },
  
  "coverage_variants": {
    "medicare_advantage": {
      "annual_wellness_visit": {"required": true, "timing": "day_60"},
      "hra_required": true,
      "star_measures": ["diabetes_care", "medication_adherence", "fall_risk"]
    },
    "commercial": {
      "employer_reporting": true,
      "wellness_incentives": true
    },
    "medicaid": {
      "presumptive_eligibility": true,
      "redetermination_reminder": {"day": 75}
    },
    "exchange": {
      "premium_payment_reminder": true,
      "navigator_assistance": true
    }
  },
  
  "cross_product": {
    "membersim": {
      "entities": ["member", "eligibility", "enrollment_834"],
      "formats": ["x12_834", "x12_270"]
    },
    "patientsim": {
      "entities": ["encounters", "observations"],
      "formats": ["fhir_r4"]
    },
    "rxmembersim": {
      "entities": ["fills", "formulary_checks"],
      "formats": ["ncpdp_d0"]
    }
  },
  
  "customizable": {
    "coverage_type": "Commercial, MA, Medicaid, Exchange",
    "engagement_intensity": "High-touch vs. digital-first",
    "chronic_condition_rate": "Adjust population health profile",
    "utilization_patterns": "Heavy vs. light utilization"
  }
}
```

## Expected Timeline

| Day | Key Events |
|-----|------------|
| -14 | Enrollment transaction received |
| -7 | ID card mailed |
| 0 | Coverage effective |
| 3-5 | Welcome call |
| 5-7 | PCP assignment, portal registration |
| 7-14 | HRA invitation, first Rx fill (if applicable) |
| 14-21 | Care gap identification and outreach |
| 21-35 | HRA completion, preventive screening scheduled |
| 30-45 | First PCP visit |
| 45-60 | Disease management outreach (if applicable) |
| 60-75 | Care management enrollment, specialist visits |
| 85-90 | 90-day satisfaction survey |

## KPI Dashboard

| Metric | Target | Measurement Point |
|--------|--------|-------------------|
| PCP Assignment | 95% | Day 7 |
| Portal Activation | 50% | Day 30 |
| HRA Completion | 35% | Day 45 |
| First PCP Visit | 30% | Day 90 |
| Rx Adherence | 80% | Day 90 |
| Member Satisfaction | 4.0/5.0 | Day 90 |

## Related Templates

- [Annual Enrollment Period](annual-enrollment.md) - AEP-specific journey
- [Disenrollment Journey](disenrollment.md) - Member off-boarding
- [Care Transition](care-transition.md) - Plan-to-plan transfer

---

*Part of the HealthSim Generative Framework Template Library*
