# CohortSpecification Model

## Overview

The CohortSpecification defines the criteria for generating a synthetic population cohort. It serves as the primary input to PopulationSim skills and drives downstream generation in PatientSim, MemberSim, and TrialSim.

---

## Model Structure

```
CohortSpecification
├── cohort_id                    # Unique identifier
├── name                         # Human-readable name
├── description                  # Purpose and context
├── geography                    # Geographic constraints
├── demographics                 # Age, sex, race/ethnicity targets
├── clinical_profile             # Condition prevalence targets
├── sdoh_requirements            # Social determinant constraints
├── size                         # Target population size
├── integration                  # Cross-product linkage
└── metadata                     # Creation context
```

---

## Schema Definition

### Root Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cohort_id` | string | Yes | Unique identifier (UUID or descriptive) |
| `name` | string | Yes | Human-readable cohort name |
| `description` | string | No | Purpose and context description |
| `geography` | GeographyConstraint | Yes | Geographic scope and filters |
| `demographics` | DemographicConstraint | No | Demographic targets |
| `clinical_profile` | ClinicalConstraint | No | Clinical condition requirements |
| `sdoh_requirements` | SDOHConstraint | No | SDOH characteristics |
| `size` | SizeSpec | Yes | Target cohort size |
| `integration` | IntegrationSpec | No | Cross-product settings |
| `metadata` | CohortMetadata | Yes | Creation metadata |

---

## GeographyConstraint Object

### Structure

```json
{
  "geography": {
    "type": "county",
    "identifiers": {
      "fips": "48201",
      "name": "Harris County",
      "state": "TX"
    },
    
    "filters": {
      "urban_rural": "urban",
      "svi_min": 0.5,
      "svi_max": 1.0,
      "include_tracts": ["48201311500", "48201312100"],
      "exclude_tracts": []
    },
    
    "aggregation": "weighted_average"
  }
}
```

### Geography Types

| Type | Identifier | Description |
|------|------------|-------------|
| `nation` | - | Entire United States |
| `state` | state_fips | Single state |
| `county` | county_fips | Single county |
| `msa` | cbsa_code | Metropolitan statistical area |
| `tract` | tract_fips | Census tract |
| `custom` | tract_list | Custom set of tracts |
| `multi_county` | county_list | Multiple counties |

### Filter Options

| Filter | Type | Description |
|--------|------|-------------|
| `urban_rural` | enum | `urban`, `suburban`, `rural`, `any` |
| `svi_min` | number | Minimum SVI threshold (0-1) |
| `svi_max` | number | Maximum SVI threshold (0-1) |
| `adi_min` | integer | Minimum ADI percentile (1-100) |
| `adi_max` | integer | Maximum ADI percentile (1-100) |
| `include_tracts` | array | Specific tracts to include |
| `exclude_tracts` | array | Specific tracts to exclude |

---

## DemographicConstraint Object

### Structure

```json
{
  "demographics": {
    "age": {
      "min": 18,
      "max": 75,
      "distribution": "population_based",
      "custom_distribution": null
    },
    
    "sex": {
      "distribution": "population_based",
      "custom_distribution": {
        "male": 0.50,
        "female": 0.50
      }
    },
    
    "race_ethnicity": {
      "distribution": "population_based",
      "minimum_diversity": {
        "minority_pct": 0.30,
        "hispanic_pct": 0.15,
        "black_pct": 0.10
      }
    }
  }
}
```

### Distribution Types

| Type | Description |
|------|-------------|
| `population_based` | Match geographic population profile |
| `uniform` | Equal distribution across categories |
| `custom` | User-specified proportions |
| `national` | Match national demographics |

### Age Constraint Options

| Field | Type | Description |
|-------|------|-------------|
| `min` | integer | Minimum age (0-120) |
| `max` | integer | Maximum age (0-120) |
| `distribution` | enum | Distribution strategy |
| `bands` | object | Custom age band weights |

---

## ClinicalConstraint Object

### Structure

```json
{
  "clinical_profile": {
    "conditions": {
      "diabetes": {
        "prevalence": 0.20,
        "required": true
      },
      "hypertension": {
        "prevalence": 0.40,
        "required": false
      },
      "chf": {
        "prevalence": 0.08,
        "required": false
      }
    },
    
    "comorbidity_rules": {
      "diabetes_hypertension": 0.65,
      "diabetes_chf": 0.25
    },
    
    "exclusions": [
      "pregnancy",
      "esrd_dialysis"
    ],
    
    "risk_stratification": {
      "method": "hcc",
      "target_distribution": {
        "low": 0.40,
        "medium": 0.35,
        "high": 0.25
      }
    }
  }
}
```

### Condition Specification

| Field | Type | Description |
|-------|------|-------------|
| `prevalence` | number | Target prevalence (0-1) |
| `required` | boolean | Must have condition for inclusion |
| `icd10_codes` | array | Specific ICD-10 codes |
| `value_set` | string | Reference to value set |

### Risk Stratification Methods

| Method | Description |
|--------|-------------|
| `hcc` | CMS-HCC risk adjustment |
| `charlson` | Charlson Comorbidity Index |
| `elixhauser` | Elixhauser Comorbidity |
| `custom` | Custom risk score |

---

## SDOHConstraint Object

### Structure

```json
{
  "sdoh_requirements": {
    "vulnerability_level": "high",
    
    "svi_thresholds": {
      "overall_min": 0.60,
      "theme_1_min": 0.50,
      "theme_3_min": 0.70
    },
    
    "adi_thresholds": {
      "national_percentile_min": 60,
      "state_decile_min": 6
    },
    
    "specific_factors": {
      "poverty_rate_min": 0.15,
      "uninsured_rate_min": 0.10,
      "food_insecurity_min": 0.12
    },
    
    "z_code_prevalence": {
      "Z59.6": 0.15,
      "Z59.41": 0.10,
      "Z56.0": 0.08
    }
  }
}
```

### Vulnerability Levels

| Level | SVI Range | ADI Range | Description |
|-------|-----------|-----------|-------------|
| `low` | 0.00-0.25 | 1-25 | Low vulnerability |
| `moderate` | 0.25-0.50 | 26-50 | Moderate vulnerability |
| `high` | 0.50-0.75 | 51-75 | High vulnerability |
| `very_high` | 0.75-1.00 | 76-100 | Very high vulnerability |

---

## SizeSpec Object

### Structure

```json
{
  "size": {
    "target": 10000,
    "type": "exact",
    "tolerance": 0.05,
    
    "stratification": {
      "by": "age_sex",
      "ensure_minimum": 50
    }
  }
}
```

### Size Types

| Type | Description |
|------|-------------|
| `exact` | Generate exactly target count |
| `approximate` | Allow tolerance variance |
| `proportional` | Based on population proportion |
| `minimum` | At least target count |

---

## IntegrationSpec Object

### Structure

```json
{
  "integration": {
    "patientsim": {
      "enabled": true,
      "generate_clinical_data": true,
      "encounter_density": "moderate"
    },
    
    "membersim": {
      "enabled": true,
      "plan_distribution": "population_based",
      "generate_claims": true
    },
    
    "trialsim": {
      "enabled": true,
      "protocol_id": "CARDIO-2024-001",
      "target_enrollment": 500
    },
    
    "identity_correlation": {
      "ssn_as_correlator": true,
      "generate_mrns": true,
      "generate_member_ids": true
    }
  }
}
```

### Integration Options

| Product | Key Settings |
|---------|--------------|
| PatientSim | Clinical data generation, encounter density |
| MemberSim | Plan distribution, claims generation |
| TrialSim | Protocol linkage, enrollment targets |

---

## CohortMetadata Object

### Structure

```json
{
  "metadata": {
    "created_at": "2024-12-23T10:30:00Z",
    "created_by": "user@example.com",
    "version": "1.0",
    "purpose": "clinical_trial_feasibility",
    "project": "CARDIO-2024",
    
    "tags": ["diabetes", "high_sdoh", "trial_recruitment"],
    
    "source_profile": "pop-48201-2024-001",
    
    "generation_settings": {
      "random_seed": 42,
      "deterministic": true
    }
  }
}
```

---

## Complete Example

```json
{
  "cohort_id": "cohort-diabetes-high-sdoh-001",
  "name": "High-SDOH Diabetes Cohort - Houston",
  "description": "Adults with diabetes in high-vulnerability areas of Harris County for trial recruitment feasibility",
  
  "geography": {
    "type": "county",
    "identifiers": {
      "fips": "48201",
      "name": "Harris County",
      "state": "TX"
    },
    "filters": {
      "svi_min": 0.60,
      "urban_rural": "urban"
    }
  },
  
  "demographics": {
    "age": {
      "min": 35,
      "max": 70,
      "distribution": "population_based"
    },
    "sex": {
      "distribution": "population_based"
    },
    "race_ethnicity": {
      "distribution": "population_based",
      "minimum_diversity": {
        "minority_pct": 0.40
      }
    }
  },
  
  "clinical_profile": {
    "conditions": {
      "diabetes": {
        "prevalence": 1.0,
        "required": true
      },
      "hypertension": {
        "prevalence": 0.55
      },
      "obesity": {
        "prevalence": 0.45
      }
    },
    "exclusions": ["esrd_dialysis", "pregnancy"]
  },
  
  "sdoh_requirements": {
    "vulnerability_level": "high",
    "svi_thresholds": {
      "overall_min": 0.60
    },
    "z_code_prevalence": {
      "Z59.6": 0.20,
      "Z59.41": 0.15
    }
  },
  
  "size": {
    "target": 5000,
    "type": "exact"
  },
  
  "integration": {
    "patientsim": {
      "enabled": true,
      "generate_clinical_data": true
    },
    "trialsim": {
      "enabled": true,
      "protocol_id": "DM-CARDIO-2024-001"
    },
    "identity_correlation": {
      "ssn_as_correlator": true
    }
  },
  
  "metadata": {
    "created_at": "2024-12-23T10:30:00Z",
    "version": "1.0",
    "purpose": "trial_feasibility",
    "tags": ["diabetes", "high_sdoh", "cardiovascular"]
  }
}
```

---

## Validation Rules

### Required Relationships

1. If `clinical_profile.conditions[x].required = true`, prevalence must be 1.0
2. Comorbidity rates cannot exceed individual condition rates
3. Age min must be less than age max
4. SVI/ADI thresholds must be in valid ranges

### Geographic Validation

1. FIPS codes must be valid and exist
2. Tract lists must be within specified county/state
3. Custom regions must have at least one tract

### Size Validation

1. Target size must be positive integer
2. Stratification minimum must be achievable given target

---

## Usage Patterns

### Trial Recruitment Cohort

Focus on clinical conditions, diversity requirements, and geographic constraints near trial sites.

### Health Equity Analysis Cohort

Emphasize SDOH requirements, vulnerability thresholds, and Z-code prevalence.

### Claims Simulation Cohort

Include MemberSim integration, plan distribution, and utilization patterns.

---

## Related Models

- [PopulationProfile](population-profile.md) - Source population data
- [GeographicEntity](geographic-entity.md) - Geography schema
- [SDOHProfile](sdoh-profile.md) - SDOH detail schema
