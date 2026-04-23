---
name: disenrollment
description: Member disenrollment/termination journey template
triggers:
  - disenrollment
  - termination
  - cancel coverage
  - end enrollment
---

# Disenrollment Journey

Journey template for member disenrollment and coverage termination.

## Overview

Disenrollment occurs when members leave a health plan:
- Voluntary termination
- Loss of eligibility
- Death
- Move out of service area
- Non-payment

## Journey Specification

```json
{
  "journey_id": "disenrollment",
  "name": "Member Disenrollment Journey",
  "description": "Journey for member termination from health plan",
  "products": ["membersim"],
  "duration_days": 90,
  "events": [
    {
      "event_id": "term_request",
      "name": "Termination Request",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 0},
      "parameters": {"request_type": "voluntary"}
    },
    {
      "event_id": "term_confirmation",
      "name": "Termination Confirmation",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 3, "days_min": 1, "days_max": 7, "distribution": "uniform"},
      "depends_on": "term_request"
    },
    {
      "event_id": "final_claims_period",
      "name": "Final Claims Run-out Period",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 0},
      "depends_on": "term_confirmation"
    },
    {
      "event_id": "cobra_notice",
      "name": "COBRA Election Notice",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 14, "days_min": 7, "days_max": 30, "distribution": "uniform"},
      "depends_on": "termination",
      "probability": 0.8,
      "parameters": {"notice_type": "COBRA"}
    },
    {
      "event_id": "termination",
      "name": "Coverage Termination",
      "event_type": "termination",
      "product": "membersim",
      "delay": {"days": 30, "days_min": 15, "days_max": 45, "distribution": "uniform"},
      "depends_on": "term_confirmation",
      "parameters": {"reason": "voluntary"}
    },
    {
      "event_id": "cobra_election",
      "name": "COBRA Election",
      "event_type": "new_enrollment",
      "product": "membersim",
      "delay": {"days": 45, "days_min": 30, "days_max": 60, "distribution": "uniform"},
      "depends_on": "cobra_notice",
      "probability": 0.08,
      "parameters": {"enrollment_type": "COBRA"}
    },
    {
      "event_id": "runout_complete",
      "name": "Claims Run-out Complete",
      "event_type": "milestone",
      "product": "membersim",
      "delay": {"days": 90},
      "depends_on": "termination"
    }
  ]
}
```

## Termination Reasons

| Reason | Code | Description |
|--------|------|-------------|
| Voluntary | VOL | Member-initiated termination |
| Loss of Eligibility | LOE | No longer qualifies (age, employment) |
| Non-Payment | NPY | Premium non-payment |
| Death | DTH | Deceased |
| Move Out | MOV | Moved out of service area |
| Other Coverage | OTH | Obtained other coverage |

## COBRA Continuation

Qualifying events for COBRA:
- Voluntary termination
- Reduction in hours
- Divorce or legal separation
- Dependent aging out

**COBRA rates:** Typically elect at ~8% rate, mostly high utilizers.

## Related Journeys

- **[New Member Onboarding](new-member-onboarding.md)** - Initial enrollment
- **[Annual Enrollment](annual-enrollment.md)** - Plan changes
- **[MemberSim Enrollment Skills](../../../membersim/enrollment-eligibility.md)** - MemberSim enrollment patterns

---

*Part of the HealthSim Generative Framework*
