---
name: medicaid-pediatric-template
description: Pre-built profile for Medicaid pediatric population
type: profile_template
---

# Medicaid Pediatric Profile Template

Ready-to-use profile for generating Medicaid-enrolled children with age-appropriate conditions and preventive care patterns.

## Quick Start

```
User: "Use the Medicaid pediatric template for 200 kids"

Claude: "Using template 'medicaid-pediatric' with defaults:
- 200 children
- Medicaid/CHIP coverage
- Age 0-17 (distributed by age bands)
- Well-child visits, immunizations
- SDOH factors included

Generate now or customize?"
```

## Template Specification

```json
{
  "template": {
    "id": "medicaid-pediatric",
    "name": "Medicaid Pediatric Population",
    "version": "1.0",
    "category": "payer",
    "tags": ["medicaid", "chip", "pediatric", "children"]
  },
  
  "profile": {
    "generation": {
      "count": 200,
      "products": ["patientsim", "membersim"],
      "validation": "strict"
    },
    
    "demographics": {
      "age": {
        "type": "categorical",
        "weights": {
          "infant_0-1": 0.12,
          "toddler_1-3": 0.18,
          "preschool_3-5": 0.15,
          "school_age_6-11": 0.30,
          "adolescent_12-17": 0.25
        }
      },
      "gender": {
        "type": "categorical",
        "weights": {"M": 0.51, "F": 0.49}
      },
      "geography": {
        "source": "populationsim",
        "filter": {
          "poverty_rate": {"min": 0.15},
          "medicaid_eligibility": "high"
        }
      },
      "household": {
        "single_parent": 0.40,
        "two_parent": 0.35,
        "grandparent_guardian": 0.15,
        "foster_care": 0.10
      }
    },
    
    "clinical": {
      "conditions_by_age": {
        "infant_0-1": [
          {"code": "P07.39", "description": "Preterm birth", "prevalence": 0.12},
          {"code": "J06.9", "description": "Upper respiratory infection", "prevalence": 0.35},
          {"code": "R11.10", "description": "Vomiting", "prevalence": 0.20},
          {"code": "L22", "description": "Diaper dermatitis", "prevalence": 0.25}
        ],
        "toddler_1-3": [
          {"code": "J06.9", "description": "Upper respiratory infection", "prevalence": 0.45},
          {"code": "H66.90", "description": "Otitis media", "prevalence": 0.35},
          {"code": "J20.9", "description": "Acute bronchitis", "prevalence": 0.15},
          {"code": "B34.9", "description": "Viral infection", "prevalence": 0.30}
        ],
        "preschool_3-5": [
          {"code": "J06.9", "description": "Upper respiratory infection", "prevalence": 0.40},
          {"code": "J45.20", "description": "Mild persistent asthma", "prevalence": 0.12},
          {"code": "H66.90", "description": "Otitis media", "prevalence": 0.25},
          {"code": "L20.9", "description": "Atopic dermatitis", "prevalence": 0.15}
        ],
        "school_age_6-11": [
          {"code": "J45.20", "description": "Mild persistent asthma", "prevalence": 0.15},
          {"code": "F90.9", "description": "ADHD", "prevalence": 0.12},
          {"code": "J06.9", "description": "Upper respiratory infection", "prevalence": 0.30},
          {"code": "S52.509A", "description": "Fracture (injury)", "prevalence": 0.05},
          {"code": "E66.9", "description": "Obesity", "prevalence": 0.20}
        ],
        "adolescent_12-17": [
          {"code": "J45.30", "description": "Moderate persistent asthma", "prevalence": 0.12},
          {"code": "F90.9", "description": "ADHD", "prevalence": 0.10},
          {"code": "F32.9", "description": "Depression", "prevalence": 0.15},
          {"code": "F41.1", "description": "Anxiety", "prevalence": 0.18},
          {"code": "E66.9", "description": "Obesity", "prevalence": 0.22},
          {"code": "L70.0", "description": "Acne", "prevalence": 0.35}
        ]
      },
      "preventive_care": {
        "well_child_visits": {
          "infant": {"target": 6, "compliance": 0.75},
          "toddler": {"target": 2, "compliance": 0.70},
          "preschool": {"target": 1, "compliance": 0.65},
          "school_age": {"target": 1, "compliance": 0.60},
          "adolescent": {"target": 1, "compliance": 0.55}
        },
        "immunization_compliance": 0.72,
        "dental_visit": 0.45,
        "vision_screening": 0.55
      },
      "special_needs": {
        "developmental_delay": 0.08,
        "speech_language": 0.06,
        "autism_spectrum": 0.025,
        "learning_disability": 0.05
      }
    },
    
    "coverage": {
      "type": "Medicaid",
      "program_distribution": {
        "Traditional Medicaid": 0.55,
        "CHIP": 0.30,
        "Medicaid Managed Care": 0.15
      },
      "eligibility_category": {
        "poverty_level": 0.60,
        "ssi_disability": 0.10,
        "foster_care": 0.10,
        "medically_needy": 0.05,
        "chip_expansion": 0.15
      }
    },
    
    "sdoh": {
      "source": "populationsim",
      "factors": {
        "food_insecurity": 0.22,
        "housing_instability": 0.15,
        "transportation_barriers": 0.18,
        "limited_english": 0.12
      }
    },
    
    "utilization": {
      "er_visits_annual": {
        "type": "log_normal",
        "mean": 0.8,
        "std_dev": 1.2
      },
      "pcp_visits_annual": {
        "type": "conditional",
        "rules": [
          {"if": "age_band == 'infant'", "distribution": {"type": "normal", "mean": 8, "std_dev": 2}},
          {"if": "age_band == 'toddler'", "distribution": {"type": "normal", "mean": 4, "std_dev": 1.5}},
          {"else": true, "distribution": {"type": "normal", "mean": 2.5, "std_dev": 1}}
        ]
      }
    }
  },
  
  "customizable": {
    "count": "Number of children (1-10,000)",
    "age_band": "Focus on specific age group",
    "geography": "State, county, or high-need area",
    "special_needs_rate": "Adjust developmental/behavioral prevalence",
    "sdoh_intensity": "High/medium/low SDOH burden"
  }
}
```

## Customization Examples

### High-Need Urban Area
```
User: "Use Medicaid pediatric for South Bronx with high SDOH"

Adjustments:
- Geography: Bronx County, NY (FIPS 36005)
- SDOH: food_insecurity +15%, housing_instability +20%
- Asthma: +10% prevalence (urban environmental factors)
- ER utilization: +30%
```

### Rural Population
```
User: "Use Medicaid pediatric for rural Mississippi"

Adjustments:
- Geography: Rural MS counties
- Transportation barriers: +25%
- Dental access: -20% compliance
- Well-child compliance: -15%
```

## Expected Outputs

| Product | Entity Types | Formats |
|---------|--------------|---------|
| PatientSim | Patient, Conditions, Immunizations, Growth Charts | FHIR R4 |
| MemberSim | Member, Eligibility, Claims | X12 834, X12 837 |

## HEDIS/Quality Measures

| Measure | Description | Target |
|---------|-------------|--------|
| W34 | Well-Child Visits (3-6) | 65% |
| WCV | Well-Child Visits (12-21) | 55% |
| CIS | Childhood Immunization | 70% |
| ADD | ADHD Follow-Up | 50% |

## Related Templates

- [Medicaid Adult](medicaid-adult.md) - Adult Medicaid population
- [Commercial Pediatric](commercial-pediatric.md) - Commercial comparison
- [CHIP Only](chip-only.md) - CHIP-specific population

---

*Part of the HealthSim Generative Framework Template Library*
