---
name: care-transition
description: Journey template for care transitions between settings
triggers:
  - care transition
  - discharge
  - post-acute
  - hospital to home
  - SNF
---

# Care Transition Journey

Journey template for care transitions between healthcare settings.

## Overview

Care transitions occur when patients move between care settings:
- Hospital → Home
- Hospital → SNF/Rehab
- Hospital → Home Health
- SNF → Home
- ED → Observation → Home

These transitions are high-risk periods for adverse events and readmissions.

## Journey Specification

```json
{
  "journey_id": "care-transition",
  "name": "Care Transition Journey",
  "description": "Standard care transition from inpatient to post-acute settings",
  "products": ["patientsim", "membersim"],
  "duration_days": 90,
  "events": [
    {
      "event_id": "discharge",
      "name": "Hospital Discharge",
      "event_type": "discharge",
      "product": "patientsim",
      "delay": {"days": 0},
      "parameters": {
        "discharge_disposition": "home_with_services"
      }
    },
    {
      "event_id": "discharge_claim",
      "name": "Inpatient Claim",
      "event_type": "claim_institutional",
      "product": "membersim",
      "delay": {"days": 3, "days_min": 2, "days_max": 7, "distribution": "uniform"},
      "depends_on": "discharge"
    },
    {
      "event_id": "tcm_call",
      "name": "Transitional Care Call",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 2, "days_min": 1, "days_max": 3, "distribution": "uniform"},
      "depends_on": "discharge",
      "parameters": {
        "encounter_type": "phone",
        "reason": "Post-discharge follow-up"
      }
    },
    {
      "event_id": "home_health_start",
      "name": "Home Health Assessment",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 3, "days_min": 1, "days_max": 5, "distribution": "uniform"},
      "depends_on": "discharge",
      "probability": 0.6,
      "parameters": {
        "encounter_type": "home_health",
        "reason": "Initial home health visit"
      }
    },
    {
      "event_id": "followup_visit",
      "name": "Post-Discharge Visit",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 7, "days_min": 5, "days_max": 14, "distribution": "uniform"},
      "depends_on": "discharge",
      "parameters": {
        "encounter_type": "office",
        "reason": "Post-hospital follow-up"
      }
    },
    {
      "event_id": "med_reconciliation",
      "name": "Medication Reconciliation",
      "event_type": "medication_order",
      "product": "patientsim",
      "delay": {"days": 0},
      "depends_on": "followup_visit"
    },
    {
      "event_id": "tcm_claim",
      "name": "TCM Service Claim",
      "event_type": "claim_professional",
      "product": "membersim",
      "delay": {"days": 14, "days_min": 7, "days_max": 30, "distribution": "uniform"},
      "depends_on": "followup_visit",
      "parameters": {
        "procedure_codes": ["99495", "99496"]
      }
    },
    {
      "event_id": "readmission",
      "name": "30-Day Readmission",
      "event_type": "admission",
      "product": "patientsim",
      "delay": {"days": 20, "days_min": 3, "days_max": 30, "distribution": "uniform"},
      "depends_on": "discharge",
      "probability": 0.15,
      "parameters": {
        "admission_type": "readmission"
      }
    }
  ]
}
```

## Transition Types

### Hospital to Home

Standard discharge with outpatient follow-up:
- Discharge planning
- TCM call within 2 days
- Follow-up visit within 7-14 days
- Medication reconciliation

### Hospital to SNF

Post-acute skilled nursing:
- SNF admission within 24 hours
- Therapy assessments
- Weekly progress reviews
- Discharge planning at day 14-21
- Home transition

### Hospital to Home Health

Home-based services:
- Home health intake within 48 hours
- Nursing visits 2-3x weekly
- PT/OT if ordered
- 60-day certification period

## Key Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| 30-day readmission rate | <15% | Return to hospital within 30 days |
| TCM completion rate | >80% | Follow-up visit within 14 days |
| Med reconciliation rate | >95% | Medications reviewed post-discharge |
| Home health referral rate | 60% | Appropriate post-acute services |

## Related Journey Templates

- **[HF Exacerbation](hf-exacerbation.md)** - Heart failure episode with transition
- **[Surgical Episode](surgical-episode.md)** - Surgical care with recovery
- **[New Member Onboarding](new-member-onboarding.md)** - Initial member setup

## Related Skills

- **[PatientSim ADT](../../../patientsim/adt-workflow.md)** - Admit/discharge patterns
- **[MemberSim Claims](../../../membersim/SKILL.md)** - Claims generation
- **[Heart Failure](../../../patientsim/heart-failure.md)** - HF-specific patterns

---

*Part of the HealthSim Generative Framework*
