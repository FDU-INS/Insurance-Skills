---
name: chip-only-profile
description: CHIP (Children's Health Insurance Program) member profile
type: profile_template
---

# CHIP-Only Profile

Profile template for children enrolled in CHIP (Children's Health Insurance Program) with distinct eligibility and benefit patterns.

## Quick Start

```
User: "Generate a CHIP member"

Claude: "Creating CHIP profile:
- Child age 0-18
- Family income 138-300% FPL
- State CHIP program enrollment
- Cost-sharing requirements"
```

## Profile Specification

```json
{
  "template": {
    "id": "chip_only",
    "name": "CHIP Program Member",
    "version": "1.0",
    "category": "chip",
    "tags": ["chip", "pediatric", "public_program", "cost_sharing"]
  },
  
  "demographics": {
    "age_range": {"min": 0, "max": 18},
    "gender_distribution": {"M": 0.51, "F": 0.49}
  },
  
  "eligibility": {
    "income_range": "138_to_300_fpl",
    "program_types": [
      {"type": "separate_chip", "probability": 0.60},
      {"type": "medicaid_expansion_chip", "probability": 0.40}
    ],
    "premium_required": 0.65,
    "monthly_premium": {"min": 0, "max": 50}
  },
  
  "benefits": {
    "coverage_type": "comprehensive",
    "cost_sharing": {
      "copay_pcp": {"min": 0, "max": 10},
      "copay_specialist": {"min": 5, "max": 25},
      "copay_er": {"min": 25, "max": 75}
    },
    "dental_included": true,
    "vision_included": true,
    "behavioral_health": true
  },
  
  "utilization": {
    "similar_to": "medicaid_pediatric",
    "well_child_compliance": 0.75,
    "dental_utilization": 0.60
  }
}
```

## CHIP vs Medicaid Differences

| Feature | CHIP | Medicaid |
|---------|------|----------|
| Income Level | 138-300% FPL | <138% FPL |
| Premiums | Often required | None |
| Cost-sharing | Limited | None/minimal |
| Enrollment cap | Some states | No cap |

## Related Profiles

- **[Medicaid Pediatric](medicaid-pediatric.md)** - Lower income children
- **[Commercial Pediatric](commercial-pediatric.md)** - Employer coverage

---

*Part of the HealthSim Generative Framework Template Library*
