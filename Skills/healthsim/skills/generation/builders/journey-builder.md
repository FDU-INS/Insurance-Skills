---
name: journey-builder
description: Build temporal event sequence specifications for healthcare data generation
triggers:
  - build a journey
  - create a journey
  - event sequence
  - timeline
  - care pathway
  - episode of care
  - patient journey
---

# Journey Builder Skill

Build structured journey specifications that define temporal event sequences for healthcare data generation.

## Overview

A **Journey** defines the timeline of events a patient/member experiences. While a Profile defines *who* (demographics, conditions), a Journey defines *what happens over time* (visits, labs, prescriptions, claims).

## Journey Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Linear** | Simple sequence | Office visit → Lab → Follow-up |
| **Branching** | Decision points | ER → Admit OR Discharge |
| **Cyclic** | Repeating events | Monthly refills, quarterly visits |
| **Protocol** | Trial schedules | Cycle 1 Day 1, Day 8, Day 15 |
| **Lifecycle** | Long-term patterns | New member first year |

## Conversation Flow

### Phase 1: Understand the Journey Type

```
User: "Create a journey for diabetic patients"

Claude: "I'll help you build a diabetic patient journey.

What type of timeline are you looking for?

1. **First Year** - New diagnosis through stabilization
2. **Annual Cycle** - Ongoing annual management
3. **Episode** - Specific event (hospitalization, complication)
4. **Custom** - Define your own sequence

Or describe what you need and I'll structure it."
```

### Phase 2: Define Events

```
User: "First year journey for newly diagnosed Type 2 diabetes"

Claude: "Great choice. Here's a typical first-year diabetic journey:

**Month 1: Initial Diagnosis**
- PCP visit with diagnosis (E11.9)
- Initial labs (A1c, metabolic panel, lipids)
- Metformin prescription (500mg BID)
- Diabetes education referral

**Month 2-3: Titration**
- Follow-up visit
- A1c recheck
- Metformin increase to 1000mg BID (if needed)

**Month 4-6: Stabilization**
- Quarterly PCP visit
- A1c monitoring
- Eye exam referral
- Foot exam

**Month 7-12: Ongoing Management**
- Quarterly visits continue
- Possible second agent addition
- Annual comprehensive exam

Should I use this standard pattern, or would you like to customize?"
```

### Phase 3: Customize Parameters

```
User: "Use the standard pattern but add more lab detail"

Claude: "Adding detailed lab panels:

**Labs at Each Quarterly Visit:**
- HbA1c
- Comprehensive Metabolic Panel (CMP)
- Lipid Panel
- Urinalysis with microalbumin

**Annual Labs:**
- All quarterly labs plus:
- TSH
- Vitamin B12 (metformin patients)
- eGFR trending

**Trigger-Based Labs:**
- If A1c > 9%: Recheck in 6 weeks
- If new symptoms: Targeted panels

Ready to generate the specification?"
```

## Journey Specification Schema

```json
{
  "journey": {
    "id": "diabetic-first-year-001",
    "name": "Type 2 Diabetes First Year Journey",
    "version": "1.0",
    "duration": "12 months",
    "start_trigger": "diagnosis_date",
    
    "phases": [
      {
        "name": "initial_diagnosis",
        "duration": "1 month",
        "events": [
          {
            "type": "encounter",
            "encounter_type": "office_visit",
            "timing": {"day": 0},
            "details": {
              "visit_type": "99214",
              "diagnoses": ["E11.9"],
              "orders": ["a1c", "cmp", "lipid_panel"]
            }
          },
          {
            "type": "prescription",
            "timing": {"day": 0},
            "details": {
              "medication": "metformin",
              "dose": "500mg",
              "frequency": "BID",
              "days_supply": 30
            }
          },
          {
            "type": "referral",
            "timing": {"day": 7, "variance": 7},
            "details": {
              "type": "diabetes_education",
              "urgency": "routine"
            }
          }
        ]
      },
      {
        "name": "titration",
        "duration": "2 months",
        "events": [
          {
            "type": "encounter",
            "timing": {"week": 4},
            "details": {
              "visit_type": "99213",
              "purpose": "medication_followup"
            }
          },
          {
            "type": "prescription",
            "timing": {"week": 4},
            "condition": "a1c > 7.5",
            "details": {
              "medication": "metformin",
              "dose": "1000mg",
              "frequency": "BID"
            }
          }
        ]
      },
      {
        "name": "stabilization",
        "duration": "3 months",
        "events": [
          {
            "type": "encounter",
            "timing": {"month": 3},
            "recurrence": "quarterly",
            "details": {
              "visit_type": "99214",
              "orders": ["a1c", "cmp"]
            }
          },
          {
            "type": "referral",
            "timing": {"month": 4},
            "details": {
              "type": "ophthalmology",
              "purpose": "diabetic_eye_exam"
            }
          }
        ]
      },
      {
        "name": "ongoing_management",
        "duration": "6 months",
        "events": [
          {
            "type": "encounter",
            "recurrence": "quarterly",
            "details": {
              "visit_type": "99214",
              "orders": ["a1c", "cmp", "lipid_panel"]
            }
          },
          {
            "type": "prescription",
            "recurrence": "monthly",
            "details": {
              "medication": "metformin",
              "refill": true
            }
          }
        ]
      }
    ],
    
    "branching_rules": [
      {
        "condition": "a1c > 9.0 at month 6",
        "action": "add_second_agent",
        "options": ["sulfonylurea", "sglt2_inhibitor", "glp1_agonist"]
      },
      {
        "condition": "egfr < 45",
        "action": "nephrology_referral"
      }
    ],
    
    "cross_product": {
      "patientsim": ["encounters", "observations", "medications"],
      "membersim": ["professional_claims", "pharmacy_claims"],
      "rxmembersim": ["prescription_fills", "dur_alerts"]
    }
  }
}
```

## Event Types

| Event Type | Products | Description |
|------------|----------|-------------|
| `encounter` | PatientSim, MemberSim | Office visit, ER, inpatient |
| `observation` | PatientSim | Lab results, vitals |
| `prescription` | PatientSim, RxMemberSim | New Rx or refill |
| `procedure` | PatientSim, MemberSim | Surgical, diagnostic |
| `referral` | PatientSim | Specialist referral |
| `admission` | PatientSim, MemberSim | Hospital admission |
| `discharge` | PatientSim, MemberSim | Hospital discharge |

## Timing Options

### Absolute Timing
```json
{"day": 0}           // Day of journey start
{"week": 4}          // 4 weeks from start
{"month": 3}         // 3 months from start
```

### Relative Timing
```json
{"after": "initial_visit", "days": 14}  // 14 days after event
{"before": "discharge", "hours": 24}    // 24 hours before event
```

### Recurrence
```json
{"recurrence": "daily"}
{"recurrence": "weekly"}
{"recurrence": "monthly"}
{"recurrence": "quarterly"}
{"recurrence": {"every": 28, "unit": "days"}}
```

### Variance
```json
{"day": 30, "variance": 7}  // Day 30 ± 7 days
{"week": 4, "variance_pct": 0.2}  // Week 4 ± 20%
```

## Pre-Built Journey Templates

| Template | Duration | Use Case |
|----------|----------|----------|
| `diabetic_first_year` | 12 months | New T2DM diagnosis |
| `diabetic_annual` | 12 months | Ongoing annual management |
| `surgical_episode` | 3 months | Elective surgery |
| `new_member_onboarding` | 90 days | New enrollment |
| `pregnancy_journey` | 12 months | Prenatal through postpartum |
| `chf_management` | 12 months | Heart failure care |
| `oncology_treatment` | 6 months | Cancer treatment cycle |
| `trial_participation` | Variable | Clinical trial protocol |

## Examples

### Example 1: Simple Linear Journey

```
User: "Create a simple surgical episode journey"

Journey Output:
{
  "journey": {
    "id": "surgical-episode-001",
    "name": "Elective Joint Replacement",
    "duration": "3 months",
    "phases": [
      {
        "name": "pre_operative",
        "events": [
          {"type": "encounter", "timing": {"week": -4}, "details": {"visit_type": "surgical_consult"}},
          {"type": "encounter", "timing": {"week": -2}, "details": {"visit_type": "pre_op_testing"}},
          {"type": "observation", "timing": {"week": -2}, "details": {"tests": ["cbc", "cmp", "pt_inr", "ekg"]}}
        ]
      },
      {
        "name": "surgical",
        "events": [
          {"type": "admission", "timing": {"day": 0}},
          {"type": "procedure", "timing": {"day": 0}, "details": {"cpt": "27447", "description": "Total knee arthroplasty"}},
          {"type": "discharge", "timing": {"day": 2}}
        ]
      },
      {
        "name": "post_operative",
        "events": [
          {"type": "encounter", "timing": {"week": 2}, "details": {"visit_type": "post_op_followup"}},
          {"type": "encounter", "timing": {"week": 6}, "details": {"visit_type": "post_op_followup"}},
          {"type": "encounter", "timing": {"week": 12}, "details": {"visit_type": "final_followup"}}
        ]
      }
    ]
  }
}
```

### Example 2: Branching Journey

```
User: "Create an ER chest pain journey with admit/discharge branches"

Journey Output:
{
  "journey": {
    "id": "er-chest-pain-001",
    "name": "ER Chest Pain Workup",
    "phases": [
      {
        "name": "er_evaluation",
        "events": [
          {"type": "encounter", "timing": {"hour": 0}, "details": {"visit_type": "er_visit"}},
          {"type": "observation", "timing": {"hour": 0}, "details": {"tests": ["troponin", "ekg", "cxr"]}},
          {"type": "observation", "timing": {"hour": 3}, "details": {"tests": ["troponin_repeat"]}}
        ]
      }
    ],
    "branching_rules": [
      {
        "condition": "troponin_positive OR ekg_stemi",
        "branch": "cardiac_admit",
        "probability": 0.25
      },
      {
        "condition": "troponin_negative AND ekg_normal",
        "branch": "discharge",
        "probability": 0.75
      }
    ],
    "branches": {
      "cardiac_admit": {
        "events": [
          {"type": "admission", "details": {"unit": "CCU"}},
          {"type": "procedure", "details": {"type": "cardiac_cath"}}
        ]
      },
      "discharge": {
        "events": [
          {"type": "discharge", "details": {"disposition": "home"}},
          {"type": "encounter", "timing": {"day": 3}, "details": {"visit_type": "cardiology_followup"}}
        ]
      }
    }
  }
}
```

## Combining Profile + Journey

```
User: "200 Medicare diabetics with first year journey"

Combined Specification:
{
  "profile": {
    "id": "medicare-diabetic-001",
    "generation": {"count": 200, "products": ["patientsim", "membersim", "rxmembersim"]},
    "demographics": {"age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65}},
    "clinical": {"primary_condition": {"code": "E11", "prevalence": 1.0}}
  },
  "journey": {
    "template": "diabetic_first_year",
    "customizations": {
      "labs_detail": "comprehensive"
    }
  }
}
```

## Related Skills

- **[Profile Builder](profile-builder.md)** - Define population characteristics
- **[Journey Executor](../executors/journey-executor.md)** - Execute journey specs
- **[Journey Templates](../templates/journeys/)** - Pre-built journeys
- **[Cross-Domain Sync](../executors/cross-domain-sync.md)** - Multi-product coordination

---

*Part of the HealthSim Generative Framework*
