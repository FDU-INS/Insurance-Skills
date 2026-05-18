---
name: commercial-healthy-template
description: Pre-built profile for healthy commercial/employer population
type: profile_template
---

# Commercial Healthy Profile Template

Ready-to-use profile for generating working-age adults with employer-sponsored insurance and minimal chronic conditions.

## Quick Start

```
User: "Use the commercial healthy template for 500 members"

Claude: "Using template 'commercial-healthy' with defaults:
- 500 members
- Commercial PPO/HMO mix
- Age 25-55 (mean 38)
- Low chronic disease burden
- National geography

Generate now or customize?"
```

## Template Specification

```json
{
  "template": {
    "id": "commercial-healthy",
    "name": "Commercial Healthy Adult Population",
    "version": "1.0",
    "category": "payer",
    "tags": ["commercial", "employer", "healthy", "working-age"]
  },
  
  "profile": {
    "generation": {
      "count": 500,
      "products": ["patientsim", "membersim"],
      "validation": "strict"
    },
    
    "demographics": {
      "age": {
        "type": "normal",
        "mean": 38,
        "std_dev": 10,
        "min": 22,
        "max": 64
      },
      "gender": {
        "type": "categorical",
        "weights": {"M": 0.48, "F": 0.52}
      },
      "geography": {
        "type": "national",
        "distribution": "employment_weighted"
      },
      "employment": {
        "status": "employed",
        "employer_size": {
          "type": "categorical",
          "weights": {
            "large_employer_1000+": 0.45,
            "mid_employer_100-999": 0.35,
            "small_employer_50-99": 0.20
          }
        }
      }
    },
    
    "clinical": {
      "health_status": {
        "type": "categorical",
        "weights": {
          "healthy": 0.70,
          "minor_chronic": 0.25,
          "managed_chronic": 0.05
        }
      },
      "conditions_by_status": {
        "healthy": {
          "prevalence": 0.70,
          "conditions": []
        },
        "minor_chronic": {
          "prevalence": 0.25,
          "conditions": [
            {"code": "J30.9", "description": "Allergic rhinitis", "prevalence": 0.40},
            {"code": "K21.0", "description": "GERD", "prevalence": 0.25},
            {"code": "M54.5", "description": "Low back pain", "prevalence": 0.30},
            {"code": "F41.1", "description": "Generalized anxiety", "prevalence": 0.20},
            {"code": "G43.909", "description": "Migraine", "prevalence": 0.15}
          ]
        },
        "managed_chronic": {
          "prevalence": 0.05,
          "conditions": [
            {"code": "I10", "description": "Essential hypertension", "prevalence": 0.60},
            {"code": "E78.5", "description": "Hyperlipidemia", "prevalence": 0.40},
            {"code": "E11.9", "description": "Type 2 diabetes", "prevalence": 0.15}
          ]
        }
      },
      "preventive_care": {
        "annual_physical": 0.55,
        "flu_shot": 0.45,
        "dental_visit": 0.60
      }
    },
    
    "coverage": {
      "type": "Commercial",
      "plan_distribution": {
        "PPO": 0.50,
        "HMO": 0.30,
        "HDHP": 0.15,
        "POS": 0.05
      },
      "deductible_tier": {
        "type": "categorical",
        "weights": {
          "low_500": 0.25,
          "mid_1500": 0.50,
          "high_3000": 0.25
        }
      },
      "family_status": {
        "type": "categorical",
        "weights": {
          "employee_only": 0.45,
          "employee_spouse": 0.20,
          "employee_children": 0.15,
          "family": 0.20
        }
      }
    },
    
    "utilization": {
      "annual_visits": {
        "type": "log_normal",
        "mean": 3.2,
        "std_dev": 2.5,
        "min": 0
      },
      "er_visits": {
        "type": "categorical",
        "weights": {
          "0": 0.92,
          "1": 0.06,
          "2+": 0.02
        }
      },
      "rx_fills_monthly": {
        "type": "conditional",
        "rules": [
          {"if": "health_status == 'healthy'", "distribution": {"type": "categorical", "weights": {"0": 0.70, "1": 0.20, "2+": 0.10}}},
          {"if": "health_status == 'minor_chronic'", "distribution": {"type": "categorical", "weights": {"0": 0.30, "1": 0.40, "2+": 0.30}}},
          {"if": "health_status == 'managed_chronic'", "distribution": {"type": "categorical", "weights": {"0": 0.10, "1-2": 0.40, "3+": 0.50}}}
        ]
      }
    }
  },
  
  "customizable": {
    "count": "Number of members (1-10,000)",
    "geography": "National, state, MSA",
    "employer_industry": "Tech, healthcare, manufacturing, etc.",
    "plan_mix": "Adjust PPO/HMO/HDHP ratios",
    "chronic_rate": "Increase/decrease chronic disease prevalence"
  }
}
```

## Customization Examples

### Tech Company Workforce
```
User: "Use commercial healthy template for a Silicon Valley tech company"

Adjustments:
- Geography: San Francisco-San Jose MSA
- Age: mean 32 (younger workforce)
- Plan mix: 60% HDHP (tech companies favor HDHPs)
- Mental health: +10% anxiety/depression prevalence
```

### Manufacturing Workforce
```
User: "Use commercial healthy for a Midwest manufacturing plant"

Adjustments:
- Geography: Ohio, Michigan, Indiana
- Age: mean 45 (older workforce)
- Conditions: +15% musculoskeletal, +10% hypertension
- Plan mix: 60% PPO (union plans)
```

## Expected Outputs

| Product | Entity Types | Formats |
|---------|--------------|---------|
| PatientSim | Patient, Conditions, Encounters | FHIR R4 |
| MemberSim | Member, Eligibility, Claims | X12 834, X12 837 |

## Related Templates

- [Commercial Family](commercial-family.md) - Family coverage focus
- [Commercial High-Cost](commercial-high-cost.md) - High utilizers
- [Medicare Diabetic](medicare-diabetic.md) - Medicare comparison

---

*Part of the HealthSim Generative Framework Template Library*
