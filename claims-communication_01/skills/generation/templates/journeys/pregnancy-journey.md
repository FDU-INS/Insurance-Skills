---
name: pregnancy-journey-template
description: Complete pregnancy and maternity care journey
type: journey_template
---

# Pregnancy Journey Template

Complete prenatal, delivery, and postpartum care journey template.

## Quick Start

```
User: "Create a pregnancy journey for a commercial member"

Claude: "Creating pregnancy journey:
- 40-week prenatal care
- Delivery event
- 6-week postpartum follow-up
- Newborn linkage"
```

## Journey Specification

```json
{
  "template": {
    "id": "pregnancy_journey",
    "name": "Pregnancy and Maternity Journey",
    "version": "1.0",
    "duration": "280 days + 42 days postpartum",
    "category": "maternity",
    "tags": ["pregnancy", "maternity", "prenatal", "delivery", "postpartum"]
  },
  
  "phases": [
    {
      "name": "first_trimester",
      "duration": "weeks 1-13",
      "events": [
        {"type": "prenatal_visit", "week": 8, "details": "Initial OB visit, dating ultrasound"},
        {"type": "prenatal_visit", "week": 12, "details": "NT scan, genetic counseling"}
      ]
    },
    {
      "name": "second_trimester",
      "duration": "weeks 14-27",
      "events": [
        {"type": "prenatal_visit", "week": 16, "details": "Routine visit"},
        {"type": "prenatal_visit", "week": 20, "details": "Anatomy scan"},
        {"type": "prenatal_visit", "week": 24, "details": "Glucose screening"},
        {"type": "lab", "week": 24, "details": "1-hour glucose tolerance"}
      ]
    },
    {
      "name": "third_trimester",
      "duration": "weeks 28-40",
      "events": [
        {"type": "prenatal_visit", "week": 28, "details": "Rhogam if indicated"},
        {"type": "prenatal_visit", "week": 32},
        {"type": "prenatal_visit", "week": 36, "details": "GBS screening"},
        {"type": "prenatal_visit", "week": 38},
        {"type": "prenatal_visit", "week": 39},
        {"type": "prenatal_visit", "week": 40}
      ]
    },
    {
      "name": "delivery",
      "duration": "1-4 days",
      "events": [
        {"type": "admission", "details": "Labor and delivery admission"},
        {"type": "delivery", "outcome": {"vaginal": 0.68, "cesarean": 0.32}},
        {"type": "newborn", "details": "Newborn care, nursery"}
      ]
    },
    {
      "name": "postpartum",
      "duration": "6 weeks",
      "events": [
        {"type": "postpartum_visit", "week": 1, "conditional": "cesarean"},
        {"type": "postpartum_visit", "week": 6, "details": "Final postpartum check"}
      ]
    }
  ],
  
  "branching": {
    "gestational_diabetes": {"probability": 0.10, "adds": "diabetes_management"},
    "preeclampsia": {"probability": 0.05, "adds": "high_risk_monitoring"},
    "preterm_labor": {"probability": 0.08, "adds": "nicu_care"}
  }
}
```

## Expected Visit Schedule

| Weeks | Visit Frequency | Key Events |
|-------|-----------------|------------|
| 4-28 | Monthly | Initial labs, anatomy scan, glucose |
| 28-36 | Every 2 weeks | GBS, growth monitoring |
| 36-40 | Weekly | NST if indicated, cervical checks |
| Delivery | Admission | L&D, delivery, recovery |
| Postpartum | 1-2 visits | Recovery, contraception |

## Cost Profile

| Phase | Cost Range |
|-------|-----------|
| Prenatal care | $3,000 - $5,000 |
| Delivery (vaginal) | $8,000 - $15,000 |
| Delivery (cesarean) | $15,000 - $25,000 |
| Postpartum | $500 - $1,000 |
| Newborn (routine) | $2,000 - $4,000 |

## Related Templates

- **[Commercial Maternity](../profiles/commercial-maternity.md)** - Mother profile
- **[Pediatric Newborn](../profiles/pediatric-newborn.md)** - Newborn profile

---

*Part of the HealthSim Generative Framework Template Library*
