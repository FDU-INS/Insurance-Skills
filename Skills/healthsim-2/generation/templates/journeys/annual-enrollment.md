---
name: annual-enrollment
description: Annual enrollment/open enrollment journey template
triggers:
  - annual enrollment
  - open enrollment
  - AEP
  - OEP
---

# Annual Enrollment Journey

Journey template for annual/open enrollment periods.

## Overview

Annual enrollment periods when members can change plans:
- Medicare Annual Enrollment Period (AEP): Oct 15 - Dec 7
- Medicare Open Enrollment Period (OEP): Jan 1 - Mar 31
- Commercial Open Enrollment: Varies by employer (typically fall)
- ACA Marketplace: Nov 1 - Jan 15

## Journey Specification

```json
{
  "journey_id": "annual-enrollment",
  "name": "Annual Enrollment Journey",
  "description": "Member journey through annual enrollment period",
  "products": ["membersim"],
  "duration_days": 90,
  "events": [
    {
      "event_id": "enrollment_notice",
      "name": "Enrollment Period Notice",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 0},
      "parameters": {"notice_type": "annual_enrollment_start"}
    },
    {
      "event_id": "plan_comparison",
      "name": "Plan Comparison Review",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 7, "days_min": 3, "days_max": 30, "distribution": "uniform"},
      "depends_on": "enrollment_notice",
      "probability": 0.6
    },
    {
      "event_id": "plan_selection",
      "name": "Plan Selection Decision",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 21, "days_min": 7, "days_max": 45, "distribution": "uniform"},
      "depends_on": "enrollment_notice"
    },
    {
      "event_id": "plan_change",
      "name": "Plan Change Submission",
      "event_type": "plan_change",
      "product": "membersim",
      "delay": {"days": 0},
      "depends_on": "plan_selection",
      "probability": 0.15,
      "parameters": {"change_reason": "annual_enrollment"}
    },
    {
      "event_id": "no_change",
      "name": "Auto-Renewal (No Change)",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 0},
      "depends_on": "plan_selection",
      "probability": 0.85
    },
    {
      "event_id": "new_id_card",
      "name": "New ID Card Issued",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 45, "days_min": 30, "days_max": 60, "distribution": "uniform"},
      "depends_on": "plan_change"
    },
    {
      "event_id": "effective_date",
      "name": "New Plan Effective",
      "event_type": "new_enrollment",
      "product": "membersim",
      "delay": {"days": 60, "days_min": 45, "days_max": 75, "distribution": "uniform"},
      "depends_on": "plan_change",
      "parameters": {"enrollment_type": "renewal"}
    }
  ]
}
```

## Enrollment Periods by Market

| Market | Period | Effective Date |
|--------|--------|----------------|
| Medicare AEP | Oct 15 - Dec 7 | Jan 1 |
| Medicare OEP | Jan 1 - Mar 31 | 1st of next month |
| Commercial | Varies (typically Oct-Nov) | Jan 1 |
| ACA Individual | Nov 1 - Jan 15 | Jan 1 or 1st of next month |

## Plan Change Rates

Typical rates by market:
| Market | Switch Rate | Factors |
|--------|-------------|---------|
| Medicare Advantage | 12-18% | Star ratings, benefits, premiums |
| Commercial Large Group | 5-10% | Plan options, cost sharing |
| ACA Marketplace | 15-25% | Premium changes, CSR |

## Related Journeys

- **[New Member Onboarding](new-member-onboarding.md)** - Initial enrollment
- **[Disenrollment](disenrollment.md)** - Voluntary termination

---

*Part of the HealthSim Generative Framework*
