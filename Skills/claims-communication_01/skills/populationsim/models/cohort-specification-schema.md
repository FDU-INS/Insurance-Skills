---
name: cohort-specification-schema
description: >
  Complete schema definition for CohortSpecification - the model that defines
  target populations for synthetic data generation across HealthSim products.
---

# CohortSpecification Schema

## Overview

CohortSpecification defines a target population for synthetic data generation. It captures demographics, clinical profiles, SDOH characteristics, and generation parameters. This is the primary output of PopulationSim cohort skills and the primary input for PatientSim, MemberSim, and TrialSim.

---

## Complete Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://healthsim.io/schemas/cohort-specification-v1",
  "title": "CohortSpecification",
  "description": "Target population definition for synthetic data generation",
  "type": "object",
  "required": ["cohort_id", "name", "geography", "demographics", "metadata"],
  
  "properties": {
    "cohort_id": {
      "type": "string",
      "description": "Unique identifier",
      "pattern": "^[a-z0-9_-]+$"
    },
    "name": { "type": "string" },
    "description": { "type": "string" },
    "target_size": { "type": "integer", "minimum": 1 },
    "version": { "type": "string", "default": "1.0" },
    
    "geography": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": { "type": "string" },
        "fips": { "type": "string" },
        "cbsa_code": { "type": "string" },
        "name": { "type": "string" },
        "state": { "type": "string" },
        "population_source": { "type": "integer" }
      }
    },
    
    "selection_criteria": {
      "type": "object",
      "properties": {
        "age_range": {
          "type": "array",
          "items": { "type": "integer" },
          "minItems": 2,
          "maxItems": 2
        },
        "sex_filter": { "type": "string", "enum": ["all", "male", "female"] },
        "primary_condition": { "type": "string" },
        "required_conditions": {
          "type": "array",
          "items": { "type": "string" }
        },
        "exclusions": {
          "type": "array",
          "items": { "type": "string" }
        },
        "insurance_filter": { "type": "string" }
      }
    },
    
    "demographics": {
      "type": "object",
      "properties": {
        "age": {
          "type": "object",
          "properties": {
            "min": { "type": "integer" },
            "max": { "type": "integer" },
            "mean": { "type": "number" },
            "median": { "type": "number" },
            "std": { "type": "number" },
            "distribution": {
              "type": "object",
              "additionalProperties": { "type": "number" }
            }
          }
        },
        "sex": {
          "type": "object",
          "properties": {
            "male": { "type": "number" },
            "female": { "type": "number" }
          }
        },
        "race_ethnicity": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        }
      }
    },
    
    "clinical_profile": {
      "type": "object",
      "properties": {
        "primary_condition": {
          "type": "object",
          "properties": {
            "code": { "type": "string" },
            "name": { "type": "string" },
            "prevalence": { "type": "number", "default": 1.0 },
            "severity_distribution": {
              "type": "object",
              "additionalProperties": { "type": "number" }
            }
          }
        },
        "comorbidities": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "rate": { "type": "number" },
              "correlation": { "type": "string" }
            }
          }
        },
        "multimorbidity": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        },
        "medications": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        },
        "lab_patterns": {
          "type": "object",
          "additionalProperties": { "type": "object" }
        }
      }
    },
    
    "sdoh_profile": {
      "type": "object",
      "properties": {
        "source": { "type": "string" },
        "svi_overall": { "type": "number" },
        "svi_themes": {
          "type": "object",
          "properties": {
            "socioeconomic": { "type": "number" },
            "household_composition": { "type": "number" },
            "minority_language": { "type": "number" },
            "housing_transportation": { "type": "number" }
          }
        },
        "indicators": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        }
      }
    },
    
    "z_code_rates": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "rate": { "type": "number" }
        }
      }
    },
    
    "insurance_mix": {
      "type": "object",
      "additionalProperties": { "type": "number" }
    },
    
    "utilization_patterns": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "mean": { "type": "number" },
          "std": { "type": "number" }
        }
      }
    },
    
    "generation_parameters": {
      "type": "object",
      "properties": {
        "sampling_method": {
          "type": "string",
          "enum": ["random", "stratified", "weighted"]
        },
        "stratification_vars": {
          "type": "array",
          "items": { "type": "string" }
        },
        "seed": { "type": "integer" },
        "output_format": { "type": "string" }
      }
    },
    
    "validation": {
      "type": "object",
      "properties": {
        "demographic_source": { "type": "string" },
        "clinical_source": { "type": "string" },
        "sdoh_source": { "type": "string" },
        "confidence": { "type": "string" },
        "notes": { "type": "string" }
      }
    },
    
    "metadata": {
      "type": "object",
      "required": ["created_at"],
      "properties": {
        "created_at": { "type": "string", "format": "date-time" },
        "created_by": { "type": "string" },
        "use_case": { "type": "string" },
        "target_product": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  }
}
```

---

## Usage by Product

### PatientSim Mapping

```json
{
  "cohort.demographics.age" → "Patient.birthDate",
  "cohort.demographics.sex" → "Patient.gender",
  "cohort.demographics.race_ethnicity" → "Patient.extension[us-core-race]",
  "cohort.clinical_profile.primary_condition" → "Condition.code",
  "cohort.clinical_profile.comorbidities" → "Condition.code[]",
  "cohort.z_code_rates" → "Condition.code[] (Z-codes)",
  "cohort.clinical_profile.medications" → "MedicationRequest[]"
}
```

### MemberSim Mapping

```json
{
  "cohort.demographics" → "Member.demographics",
  "cohort.insurance_mix" → "Member.coverage.type",
  "cohort.clinical_profile" → "Member.riskScore",
  "cohort.sdoh_profile" → "Member.utilizationPattern",
  "cohort.utilization_patterns" → "Claim.frequency"
}
```

### TrialSim Mapping

```json
{
  "cohort.demographics" → "Subject.eligibility",
  "cohort.selection_criteria" → "Subject.inclusion/exclusion",
  "cohort.clinical_profile" → "Subject.screeningStatus",
  "cohort.geography" → "Subject.site"
}
```

---

## Validation Rules

### Demographics
- Age distribution must sum to ~1.0 (±0.02)
- Sex distribution must sum to 1.0
- Race/ethnicity must sum to ~1.0 (±0.02)

### Clinical
- Comorbidity rates must be ≤1.0
- Severity distribution must sum to ~1.0
- Medication rates must be ≤1.0

### SDOH
- SVI scores must be 0-1
- Z-code rates must be ≤1.0

---

## Related Schemas

- [PopulationProfile](population-profile-schema.md) - Source data
- [CrossProductIntegration](cross-product-integration.md) - Product mapping
