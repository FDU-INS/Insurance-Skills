---
name: populationsim-models
description: >
  Canonical data models and schemas for PopulationSim. These models define
  the structure of population intelligence data and enable integration
  across HealthSim products.
---

# PopulationSim Models & Schemas

## Overview

PopulationSim uses canonical data models to ensure consistent representation of population intelligence across all skills and integrations. These models define the structure for geographic profiles, cohort specifications, and cross-product data exchange.

---

## Core Models

| Model | Purpose | Primary Use |
|-------|---------|-------------|
| [PopulationProfile](population-profile-schema.md) | Geographic population characteristics | All geographic skills |
| [CohortSpecification](cohort-specification-schema.md) | Target population definition | Cohort skills, generation |
| [DataSourceMapping](data-source-mapping.md) | Source data to model mapping | Reference, validation |
| [CrossProductIntegration](cross-product-integration.md) | HealthSim product integration | Cross-product cohorts |

---

## Model Hierarchy

```
PopulationProfile
├── Geography (location context)
├── Demographics (age, sex, race)
├── HealthIndicators (CDC PLACES)
├── SDOHIndices (SVI, ADI)
└── HealthcareAccess (coverage, providers)

CohortSpecification
├── Geography (from PopulationProfile)
├── Demographics (distributions)
├── ClinicalProfile (conditions, meds)
├── SDOHProfile (Z-code rates)
├── InsuranceMix (coverage types)
└── GenerationParameters (output config)
```

---

## Model Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ Census  │  │  CDC    │  │  CDC    │  │  USDA   │            │
│  │   ACS   │  │ PLACES  │  │   SVI   │  │  Food   │            │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘            │
│       │            │            │            │                   │
│       └────────────┴─────┬──────┴────────────┘                  │
│                          ▼                                       │
│              ┌───────────────────────┐                          │
│              │   PopulationProfile   │                          │
│              │  (Geographic Entity)  │                          │
│              └───────────┬───────────┘                          │
│                          │                                       │
│              ┌───────────▼───────────┐                          │
│              │  CohortSpecification  │                          │
│              │  (Generation Target)  │                          │
│              └───────────┬───────────┘                          │
│                          │                                       │
│       ┌──────────────────┼──────────────────┐                   │
│       ▼                  ▼                  ▼                   │
│ ┌───────────┐    ┌───────────┐    ┌───────────┐                │
│ │PatientSim │    │ MemberSim │    │ TrialSim  │                │
│ │ (Patient) │    │ (Member)  │    │ (Subject) │                │
│ └───────────┘    └───────────┘    └───────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Common Model Elements

### Geography Object

Used across all models for location context:

```json
{
  "geography": {
    "type": "county|tract|msa|state|custom",
    "fips": "48201",
    "name": "Harris County",
    "state": "TX",
    "state_fips": "48",
    "cbsa_code": "26420",
    "cbsa_name": "Houston-The Woodlands-Sugar Land, TX",
    "population": 4731145,
    "land_area_sq_mi": 1729.2
  }
}
```

### Demographics Object

Standard demographic distribution:

```json
{
  "demographics": {
    "age": {
      "min": 0,
      "max": 100,
      "mean": 34.2,
      "median": 33.5,
      "distribution": {
        "0-17": 0.24,
        "18-44": 0.38,
        "45-64": 0.24,
        "65+": 0.14
      }
    },
    "sex": {
      "male": 0.49,
      "female": 0.51
    },
    "race_ethnicity": {
      "white_nh": 0.28,
      "black": 0.20,
      "hispanic": 0.44,
      "asian": 0.07,
      "other": 0.01
    }
  }
}
```

### Health Indicators Object

CDC PLACES measures:

```json
{
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "outcomes": {
      "diabetes": 0.108,
      "obesity": 0.328,
      "hypertension": 0.324,
      "chd": 0.052,
      "stroke": 0.032
    },
    "behaviors": {
      "smoking": 0.142,
      "physical_inactivity": 0.228,
      "binge_drinking": 0.162
    },
    "prevention": {
      "checkup": 0.768,
      "dental": 0.642,
      "mammography": 0.784
    }
  }
}
```

### SDOH Indices Object

Social vulnerability measures:

```json
{
  "sdoh_indices": {
    "svi": {
      "overall": 0.68,
      "socioeconomic": 0.62,
      "household": 0.58,
      "minority_language": 0.78,
      "housing_transport": 0.64
    },
    "adi": {
      "national_percentile": 72,
      "state_decile": 8
    },
    "indicators": {
      "poverty_rate": 0.158,
      "uninsured_rate": 0.168,
      "food_insecurity": 0.128
    }
  }
}
```

---

## Validation Standards

### Required Fields

Every model instance must include:
- `model_type` - Identifies the model
- `version` - Model version
- `created_at` - ISO 8601 timestamp
- `geography` - At minimum, type and identifier

### Data Quality

- Percentages must be 0.0-1.0
- FIPS codes must be valid format
- ICD-10 codes must be valid
- Distributions must sum to ~1.0

---

## Related Documentation

- [PopulationSim SKILL.md](../SKILL.md) - Master router
- [Cohort Skills](../cohorts/README.md) - Cohort generation
- [References](../references/README.md) - Data sources
