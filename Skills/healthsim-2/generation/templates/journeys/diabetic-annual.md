---
name: diabetic-annual
description: Annual diabetes management journey template
triggers:
  - diabetes
  - annual
  - A1C monitoring
  - diabetic care
---

# Diabetic Annual Care Journey

Annual routine care journey for established diabetic patients.

## Overview

Annual care cycle for patients with established diabetes diagnosis, covering:
- Quarterly A1C monitoring
- Annual comprehensive exam
- Preventive screenings
- Medication management

## Journey Specification

```json
{
  "journey_id": "diabetic-annual",
  "name": "Diabetic Annual Care",
  "description": "Standard annual care for established Type 2 diabetes",
  "products": ["patientsim", "membersim"],
  "duration_days": 365,
  "events": [
    {
      "event_id": "annual_visit",
      "name": "Annual Diabetes Visit",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 0},
      "parameters": {"encounter_type": "office", "reason": "Annual diabetes management"}
    },
    {
      "event_id": "q1_a1c",
      "name": "Q1 A1C Test",
      "event_type": "lab_order",
      "product": "patientsim",
      "delay": {"days": 0},
      "depends_on": "annual_visit",
      "parameters": {"loinc": "4548-4", "test_name": "Hemoglobin A1c"}
    },
    {
      "event_id": "annual_eye_exam",
      "name": "Diabetic Eye Exam",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 30, "days_min": 14, "days_max": 60, "distribution": "uniform"},
      "depends_on": "annual_visit",
      "parameters": {"encounter_type": "specialist", "specialty": "Ophthalmology"}
    },
    {
      "event_id": "q2_a1c",
      "name": "Q2 A1C Test",
      "event_type": "lab_order",
      "product": "patientsim",
      "delay": {"days": 90, "days_min": 80, "days_max": 100, "distribution": "uniform"},
      "depends_on": "annual_visit",
      "parameters": {"loinc": "4548-4", "test_name": "Hemoglobin A1c"}
    },
    {
      "event_id": "kidney_screening",
      "name": "Annual Kidney Screening",
      "event_type": "lab_order",
      "product": "patientsim",
      "delay": {"days": 90, "days_min": 60, "days_max": 180, "distribution": "uniform"},
      "depends_on": "annual_visit",
      "parameters": {"loinc": "14959-1", "test_name": "Urine Albumin/Creatinine Ratio"}
    },
    {
      "event_id": "q3_a1c",
      "name": "Q3 A1C Test",
      "event_type": "lab_order",
      "product": "patientsim",
      "delay": {"days": 180, "days_min": 170, "days_max": 190, "distribution": "uniform"},
      "depends_on": "annual_visit",
      "parameters": {"loinc": "4548-4", "test_name": "Hemoglobin A1c"}
    },
    {
      "event_id": "foot_exam",
      "name": "Annual Foot Exam",
      "event_type": "encounter",
      "product": "patientsim",
      "delay": {"days": 180, "days_min": 90, "days_max": 365, "distribution": "uniform"},
      "depends_on": "annual_visit",
      "parameters": {"encounter_type": "office", "reason": "Diabetic foot exam"}
    },
    {
      "event_id": "q4_a1c",
      "name": "Q4 A1C Test",
      "event_type": "lab_order",
      "product": "patientsim",
      "delay": {"days": 270, "days_min": 260, "days_max": 280, "distribution": "uniform"},
      "depends_on": "annual_visit",
      "parameters": {"loinc": "4548-4", "test_name": "Hemoglobin A1c"}
    }
  ]
}
```

## Quality Measures Addressed

| Measure | NQF | Description |
|---------|-----|-------------|
| CDC - A1C Testing | 0059 | A1C test at least annually |
| CDC - Eye Exam | 0055 | Dilated eye exam annually |
| CDC - Kidney Screening | 0062 | Nephropathy screening annually |
| CDC - Foot Exam | - | Annual foot examination |

## Related Journeys

- **[Diabetic First Year](diabetic-first-year.md)** - Newly diagnosed diabetes
- **[CHF First Year](chf-first-year.md)** - Heart failure with diabetes comorbidity

---

*Part of the HealthSim Generative Framework*
