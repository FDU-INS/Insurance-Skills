---
name: pediatric-newborn-profile
description: Newborn and infant profile template
type: profile_template
---

# Pediatric Newborn Profile

Profile template for newborns and infants (0-12 months) with well-child care patterns.

## Quick Start

```
User: "Generate a newborn for maternity follow-up"

Claude: "Creating newborn profile:
- Birth weight and APGAR scores
- Newborn screening results
- Well-child visit schedule
- Immunization timeline"
```

## Profile Specification

```json
{
  "template": {
    "id": "pediatric_newborn",
    "name": "Pediatric Newborn",
    "version": "1.0",
    "category": "pediatric",
    "tags": ["newborn", "infant", "well_child", "immunization"]
  },
  
  "demographics": {
    "age_range": {"min": 0, "max": 1},
    "birth_metrics": {
      "weight_grams": {"mean": 3400, "std": 450},
      "length_cm": {"mean": 50, "std": 2.5},
      "head_circumference_cm": {"mean": 34, "std": 1.5},
      "apgar_1min": {"min": 7, "max": 10},
      "apgar_5min": {"min": 8, "max": 10}
    }
  },
  
  "birth_events": {
    "delivery_type": {
      "vaginal": 0.68,
      "cesarean": 0.32
    },
    "birth_location": "hospital",
    "length_of_stay": {
      "vaginal": 2,
      "cesarean": 4
    }
  },
  
  "well_child_schedule": {
    "visits": [
      {"age_days": 3, "type": "newborn_followup"},
      {"age_weeks": 2, "type": "2_week_check"},
      {"age_months": 1, "type": "1_month_well"},
      {"age_months": 2, "type": "2_month_well"},
      {"age_months": 4, "type": "4_month_well"},
      {"age_months": 6, "type": "6_month_well"},
      {"age_months": 9, "type": "9_month_well"},
      {"age_months": 12, "type": "12_month_well"}
    ]
  },
  
  "immunizations": {
    "birth": ["HepB_dose1"],
    "2_months": ["DTaP_1", "IPV_1", "Hib_1", "PCV13_1", "RV_1"],
    "4_months": ["DTaP_2", "IPV_2", "Hib_2", "PCV13_2", "RV_2"],
    "6_months": ["DTaP_3", "IPV_3", "Hib_3", "PCV13_3", "RV_3", "Influenza"],
    "12_months": ["MMR_1", "Varicella_1", "HepA_1"]
  }
}
```

## Expected Encounters (First Year)

| Visit Type | Count | CPT Codes |
|------------|-------|-----------|
| Well-child | 8-10 | 99381, 99391 |
| Immunization | 8-10 | 90460, 90461 |
| Sick visits | 2-4 | 99213, 99214 |

## Cost Profile (First Year)

| Component | Cost Range |
|-----------|-----------|
| Delivery/birth | $10,000 - $25,000 |
| Well-child visits | $1,200 - $2,000 |
| Immunizations | $800 - $1,500 |
| Sick visits | $400 - $1,000 |

## Related Profiles

- **[Commercial Maternity](commercial-maternity.md)** - Mother profile
- **[Medicaid Pediatric](medicaid-pediatric.md)** - Medicaid equivalent
- **[Commercial Pediatric](commercial-pediatric.md)** - Older children

---

*Part of the HealthSim Generative Framework Template Library*
