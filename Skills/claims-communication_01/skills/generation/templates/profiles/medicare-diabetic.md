---
name: medicare-diabetic-template
description: Pre-built profile for Medicare Type 2 diabetes population
type: profile_template
---

# Medicare Diabetic Profile Template

Ready-to-use profile for generating Medicare beneficiaries with Type 2 diabetes.

## Quick Start

```
User: "Use the Medicare diabetic template for 100 patients"

Claude: "Using template 'medicare-diabetic' with defaults:
- 100 patients
- Medicare (55% MA, 45% Original)
- Age 65-95 (mean 72)
- Type 2 diabetes with standard comorbidities
- National geography

Generate now or customize?"
```

## Template Specification

```json
{
  "template": {
    "id": "medicare-diabetic",
    "name": "Medicare Type 2 Diabetic Population",
    "version": "1.0",
    "category": "payer",
    "tags": ["medicare", "diabetes", "chronic"]
  },
  
  "profile": {
    "generation": {
      "count": 100,
      "products": ["patientsim", "membersim"],
      "validation": "strict"
    },
    
    "demographics": {
      "age": {
        "type": "normal",
        "mean": 72,
        "std_dev": 8,
        "min": 65,
        "max": 95
      },
      "gender": {
        "type": "categorical",
        "weights": {"M": 0.48, "F": 0.52}
      },
      "geography": {
        "type": "national",
        "distribution": "population_weighted"
      }
    },
    
    "clinical": {
      "primary_condition": {
        "code": "E11",
        "description": "Type 2 diabetes mellitus",
        "prevalence": 1.0,
        "severity": {
          "type": "categorical",
          "weights": {
            "without_complications": 0.40,
            "with_complications": 0.45,
            "uncontrolled": 0.15
          }
        }
      },
      "comorbidities": [
        {"code": "I10", "description": "Essential hypertension", "prevalence": 0.78},
        {"code": "E78.5", "description": "Hyperlipidemia", "prevalence": 0.72},
        {"code": "E66.9", "description": "Obesity", "prevalence": 0.42},
        {"code": "N18.3", "description": "CKD Stage 3", "prevalence": 0.28},
        {"code": "I25.10", "description": "CAD", "prevalence": 0.25},
        {"code": "I50.9", "description": "Heart failure", "prevalence": 0.18},
        {"code": "G62.9", "description": "Peripheral neuropathy", "prevalence": 0.30},
        {"code": "H35.81", "description": "Diabetic retinopathy", "prevalence": 0.22}
      ],
      "labs": {
        "a1c": {
          "type": "conditional",
          "rules": [
            {"if": "severity == 'without_complications'", "distribution": {"type": "normal", "mean": 6.8, "std_dev": 0.4}},
            {"if": "severity == 'with_complications'", "distribution": {"type": "normal", "mean": 7.8, "std_dev": 0.8}},
            {"if": "severity == 'uncontrolled'", "distribution": {"type": "normal", "mean": 9.5, "std_dev": 1.0}}
          ]
        },
        "egfr": {
          "type": "conditional",
          "rules": [
            {"if": "has_condition('N18.3')", "distribution": {"type": "uniform", "min": 30, "max": 59}},
            {"else": true, "distribution": {"type": "normal", "mean": 75, "std_dev": 15, "min": 60}}
          ]
        }
      }
    },
    
    "coverage": {
      "type": "Medicare",
      "plan_distribution": {
        "Medicare Advantage": 0.55,
        "Original Medicare": 0.45
      },
      "part_d": {
        "enrolled": 0.92,
        "lis_eligible": 0.28
      }
    },
    
    "medications": {
      "antidiabetic": [
        {"class": "biguanide", "drug": "metformin", "prevalence": 0.75},
        {"class": "sulfonylurea", "drug": "glipizide", "prevalence": 0.25},
        {"class": "sglt2i", "drug": "empagliflozin", "prevalence": 0.20},
        {"class": "glp1ra", "drug": "semaglutide", "prevalence": 0.15},
        {"class": "insulin", "drug": "insulin glargine", "prevalence": 0.30}
      ],
      "cardiovascular": [
        {"class": "ace_inhibitor", "drug": "lisinopril", "prevalence": 0.55},
        {"class": "statin", "drug": "atorvastatin", "prevalence": 0.65},
        {"class": "beta_blocker", "drug": "metoprolol", "prevalence": 0.35},
        {"class": "aspirin", "drug": "aspirin 81mg", "prevalence": 0.60}
      ]
    }
  },
  
  "customizable": {
    "count": "Number of patients (1-10,000)",
    "geography": "National, state, MSA, or county",
    "severity_distribution": "Adjust complication rates",
    "plan_mix": "MA vs Original Medicare ratio",
    "add_journey": "Attach diabetic_first_year or diabetic_annual"
  }
}
```

## Customization Examples

### Smaller Cohort
```
User: "Use Medicare diabetic template with 25 patients"
→ Sets count to 25, all other defaults
```

### Specific State
```
User: "Use Medicare diabetic template for Florida"
→ Sets geography to {"state": "FL"}
```

### Higher Severity
```
User: "Use Medicare diabetic template with 50% having complications"
→ Adjusts severity weights
```

### With Journey
```
User: "Use Medicare diabetic template with first year journey"
→ Attaches diabetic_first_year journey template
```

## Expected Outputs

| Product | Entity Types | Formats |
|---------|--------------|---------|
| PatientSim | Patient, Conditions, Observations, Medications | FHIR R4, HL7v2 |
| MemberSim | Member, Eligibility, Claims | X12 834, X12 837 |

## Related Templates

- [Commercial Diabetic](commercial-diabetic.md) - Working-age diabetics
- [Medicaid Diabetic](medicaid-diabetic.md) - Medicaid population
- [Medicare CHF](medicare-chf.md) - Heart failure focus

---

*Part of the HealthSim Generative Framework Template Library*
