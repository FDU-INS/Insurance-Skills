---
name: commercial-family-profile
description: Commercial family coverage profile template
type: profile_template
---

# Commercial Family Profile

Profile template for a commercial family unit with dependent coverage.

## Quick Start

```
User: "Generate a commercial family with 2 kids"

Claude: "Creating commercial family profile:
- Primary subscriber (employed adult)
- Spouse (dependent)
- 2 children under 18

Coverage: Commercial PPO/HMO family plan"
```

## Profile Specification

```json
{
  "template": {
    "id": "commercial_family",
    "name": "Commercial Family Coverage",
    "version": "1.0",
    "category": "commercial",
    "tags": ["family", "commercial", "employer", "dependent"]
  },
  
  "family_structure": {
    "subscriber": {
      "role": "primary",
      "relationship_code": "18",
      "age_range": {"min": 25, "max": 60},
      "employment_status": "full_time"
    },
    "spouse": {
      "role": "dependent",
      "relationship_code": "01",
      "age_range": {"min": 25, "max": 60},
      "probability": 0.85
    },
    "children": {
      "role": "dependent",
      "relationship_code": "19",
      "age_range": {"min": 0, "max": 26},
      "count": {"min": 0, "max": 4, "mean": 1.8}
    }
  },
  
  "coverage": {
    "plan_types": ["PPO", "HMO", "POS", "HDHP"],
    "tier": "family",
    "effective_dates": {
      "pattern": "first_of_month",
      "waiting_period_days": 30
    },
    "benefits": {
      "deductible": {"individual": 500, "family": 1500},
      "oop_max": {"individual": 5000, "family": 10000},
      "coinsurance": 0.80
    }
  },
  
  "demographics": {
    "income_range": {"min": 50000, "max": 200000},
    "geography": "suburban_urban_mix",
    "employer_size": {"min": 50, "max": 10000}
  }
}
```

## Utilization Patterns

| Family Member | Annual Visits | Common Services |
|---------------|---------------|-----------------|
| Subscriber | 3-5 | Preventive, chronic care |
| Spouse | 4-6 | Preventive, specialist |
| Child (<5) | 8-12 | Well-child, immunizations |
| Child (5-18) | 3-5 | Preventive, sports physicals |

## Cost Profile

| Component | Family Annual Cost |
|-----------|-------------------|
| Premium | $18,000 - $24,000 |
| Member Share | $6,000 - $8,000 |
| Deductible Spend | $1,000 - $1,500 |
| Total Utilization | $8,000 - $15,000 |

## Related Profiles

- **[Commercial Healthy](commercial-healthy.md)** - Single healthy adult
- **[Commercial Maternity](commercial-maternity.md)** - Pregnancy coverage
- **[Commercial Pediatric](commercial-pediatric.md)** - Pediatric focus

---

*Part of the HealthSim Generative Framework Template Library*
