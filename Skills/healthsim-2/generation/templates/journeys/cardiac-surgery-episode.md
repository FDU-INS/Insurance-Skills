---
name: cardiac-surgery-episode-journey
description: Cardiac surgery episode journey template
type: journey_template
---

# Cardiac Surgery Episode Journey

Complete cardiac surgery episode from evaluation through recovery (CABG, valve replacement).

## Quick Start

```
User: "Create a CABG surgery episode journey"

Claude: "Creating cardiac surgery journey:
- Pre-operative evaluation
- Surgical procedure
- ICU/stepdown care
- Cardiac rehabilitation"
```

## Journey Specification

```json
{
  "template": {
    "id": "cardiac_surgery_episode",
    "name": "Cardiac Surgery Episode",
    "version": "1.0",
    "duration": "90-180 days",
    "category": "surgical",
    "tags": ["cardiac", "surgery", "cabg", "valve", "episode"]
  },
  
  "procedure_types": {
    "cabg": {"probability": 0.60, "los": 7},
    "valve_replacement": {"probability": 0.25, "los": 8},
    "combined_cabg_valve": {"probability": 0.15, "los": 10}
  },
  
  "phases": [
    {
      "name": "pre_operative",
      "duration": "2-4 weeks",
      "events": [
        {"type": "cardiology_consult", "timing": "day -21"},
        {"type": "cardiac_cath", "timing": "day -14"},
        {"type": "ct_surgery_consult", "timing": "day -10"},
        {"type": "pre_op_testing", "timing": "day -7", "details": "Labs, CXR, EKG, echo"},
        {"type": "pre_admit_visit", "timing": "day -1"}
      ]
    },
    {
      "name": "surgery_hospitalization",
      "duration": "5-14 days",
      "events": [
        {"type": "admission", "timing": "day 0"},
        {"type": "surgery", "timing": "day 0", "cpt": ["33533", "33534", "33405"]},
        {"type": "icu_stay", "duration": "1-3 days"},
        {"type": "stepdown_care", "duration": "3-5 days"},
        {"type": "discharge", "timing": "day 7-14"}
      ]
    },
    {
      "name": "post_operative",
      "duration": "6-12 weeks",
      "events": [
        {"type": "home_health", "timing": "day 8-21", "visits": 6},
        {"type": "ct_surgery_followup", "timing": "day 14"},
        {"type": "cardiac_rehab_start", "timing": "day 21"},
        {"type": "cardiology_followup", "timing": "day 30"},
        {"type": "cardiac_rehab_sessions", "count": 36},
        {"type": "final_followup", "timing": "day 90"}
      ]
    }
  ],
  
  "complications": {
    "atrial_fibrillation": {"probability": 0.30},
    "wound_infection": {"probability": 0.03},
    "readmission_30day": {"probability": 0.12},
    "stroke": {"probability": 0.02}
  }
}
```

## Expected Timeline

| Phase | Duration | Key Events |
|-------|----------|------------|
| Pre-op | 2-4 weeks | Cath, consults, clearance |
| Surgery | Day 0 | OR, bypass time 2-4 hours |
| ICU | 1-3 days | Ventilator, hemodynamic monitoring |
| Floor | 4-7 days | Mobilization, education |
| Recovery | 6-12 weeks | Rehab, return to activities |

## Cost Profile

| Component | Cost Range |
|-----------|-----------|
| Pre-operative | $3,000 - $8,000 |
| Surgery & hospitalization | $80,000 - $150,000 |
| Cardiac rehabilitation | $5,000 - $10,000 |
| Follow-up care | $2,000 - $5,000 |
| **Total episode** | **$90,000 - $173,000** |

## Related Templates

- **[Surgical Episode](surgical-episode.md)** - General surgical template
- **[Medicare CHF](../profiles/medicare-chf.md)** - Post-surgical profile

---

*Part of the HealthSim Generative Framework Template Library*
