---
name: chf-first-year
description: First year journey for newly diagnosed heart failure patients
triggers:
  - heart failure
  - CHF
  - HF diagnosis
  - first year
---

# CHF First Year Journey

First year care journey for patients newly diagnosed with heart failure.

## Overview

Intensive management in the first year after heart failure diagnosis:
- Initial workup and staging
- Medication optimization (GDMT)
- Frequent monitoring
- Patient education
- Care transition management

## Journey Specification

```json
{
  "journey_id": "chf-first-year",
  "name": "First Year of Heart Failure Care",
  "description": "Intensive management for newly diagnosed heart failure",
  "products": ["patientsim", "membersim"],
  "duration_days": 365,
  "events": [
    {
      "event_id": "initial_dx",
      "name": "Heart Failure Diagnosis",
      "event_type": "diagnosis",
      "product": "patientsim",
      "delay": {"days": 0},
      "parameters": {"icd10": "I50.9", "description": "Heart failure, unspecified"}
    },
    {
      "event_id": "echo",
      "name": "Initial Echocardiogram",
      "event_type": "procedure",
      "product": "patientsim",
      "delay": {"days": 3, "days_min": 0, "days_max": 14, "distribution": "uniform"},
      "depends_on": "initial_dx",
      "parameters": {"cpt": "93306", "description": "Transthoracic echocardiography"}
    },
    {
      "event_id": "bnp_baseline",
      "name": "Baseline BNP",
      "event_type": "lab_order",
      "product": "patientsim",
      "delay": {"days": 0},
      "depends_on": "initial_dx",
      "parameters": {"loinc": "30934-4", "test_name": "BNP"}
    },
    {
      "event_id": "acei_start",
      "name": "Start ACE Inhibitor",
      "event_type": "medication_order",
      "product": "patientsim",
      "delay": {"days": 7, "days_min": 1, "days_max": 14, "distribution": "uniform"},
      "depends_on": "initial_dx",
      "parameters": {"rxnorm": "314077", "drug_name": "Lisinopril 5 MG"}
    },
    {
      "event_id": "beta_blocker_start",
      "name": "Start Beta Blocker",
      "event_type": "medication_order",
      "product": "patientsim",
      "delay": {"days": 14, "days_min": 7, "days_max": 28, "distribution": "uniform"},
      "depends_on": "acei_start",
      "parameters": {"rxnorm": "200033", "drug_name": "Carvedilol 6.25 MG"}
    },
    {
      "event_id": "followup_2wk",
      "name": "2-Week Follow-up",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 14, "days_min": 10, "days_max": 21, "distribution": "uniform"},
      "depends_on": "initial_dx",
      "parameters": {"encounter_type": "office"}
    },
    {
      "event_id": "cardiology_referral",
      "name": "Cardiology Consult",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 21, "days_min": 14, "days_max": 42, "distribution": "uniform"},
      "depends_on": "initial_dx",
      "parameters": {"encounter_type": "specialist", "specialty": "Cardiology"}
    },
    {
      "event_id": "followup_1mo",
      "name": "1-Month Follow-up",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 30, "days_min": 25, "days_max": 42, "distribution": "uniform"},
      "depends_on": "initial_dx"
    },
    {
      "event_id": "followup_3mo",
      "name": "3-Month Follow-up",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
      "depends_on": "initial_dx"
    },
    {
      "event_id": "bnp_3mo",
      "name": "3-Month BNP",
      "event_type": "lab_order",
      "product": "patientsim",
      "delay": {"days": 0},
      "depends_on": "followup_3mo",
      "parameters": {"loinc": "30934-4", "test_name": "BNP"}
    },
    {
      "event_id": "hf_exacerbation",
      "name": "HF Exacerbation",
      "event_type": "admission",
      "product": "patientsim",
      "delay": {"days": 120, "days_min": 30, "days_max": 300, "distribution": "uniform"},
      "depends_on": "initial_dx",
      "probability": 0.25,
      "parameters": {"admission_type": "urgent"}
    },
    {
      "event_id": "followup_6mo",
      "name": "6-Month Follow-up",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 180, "days_min": 160, "days_max": 200, "distribution": "uniform"},
      "depends_on": "initial_dx"
    },
    {
      "event_id": "echo_6mo",
      "name": "6-Month Echo",
      "event_type": "procedure",
      "product": "patientsim",
      "delay": {"days": 180, "days_min": 150, "days_max": 210, "distribution": "uniform"},
      "depends_on": "initial_dx",
      "parameters": {"cpt": "93306"}
    },
    {
      "event_id": "annual_visit",
      "name": "Annual HF Visit",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 365, "days_min": 330, "days_max": 395, "distribution": "uniform"},
      "depends_on": "initial_dx"
    }
  ]
}
```

## GDMT Optimization

Guideline-Directed Medical Therapy targets:
- ACE inhibitor/ARB/ARNI
- Beta blocker (carvedilol, metoprolol succinate, bisoprolol)
- Mineralocorticoid receptor antagonist (spironolactone)
- SGLT2 inhibitor (dapagliflozin, empagliflozin)

## Quality Measures

| Measure | Description |
|---------|-------------|
| HF-1 | Discharge instructions |
| HF-2 | Evaluation of LV function |
| HF-3 | ACE/ARB for LVSD |
| HF-6 | Beta blocker for LVSD |

## Related Journeys

- **[HF Exacerbation](hf-exacerbation.md)** - Acute decompensation
- **[Care Transition](care-transition.md)** - Post-discharge care
- **[Diabetic First Year](diabetic-first-year.md)** - Often comorbid

---

*Part of the HealthSim Generative Framework*
