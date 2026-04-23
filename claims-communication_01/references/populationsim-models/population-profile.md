# PopulationProfile Model

## Overview

The PopulationProfile is the primary output model for PopulationSim, representing a comprehensive snapshot of a geographic area's population characteristics. It combines demographic, health, and social determinant data to enable downstream generation in PatientSim, MemberSim, and TrialSim.

---

## Model Structure

```
PopulationProfile
├── geography                    # Geographic identification
├── demographics                 # Age, sex, race/ethnicity distributions
├── health_indicators            # CDC PLACES health measures
├── sdoh_profile                 # Social determinants (SVI, ADI, economic)
├── healthcare_access            # Insurance, provider access
├── utilization_patterns         # Expected healthcare utilization
└── metadata                     # Source, timestamp, version
```

---

## Schema Definition

### Root Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `profile_id` | string | Yes | Unique identifier (UUID) |
| `geography` | GeographicEntity | Yes | Geographic area being profiled |
| `demographics` | Demographics | Yes | Population demographic distributions |
| `health_indicators` | HealthIndicators | Yes | Health outcome and behavior measures |
| `sdoh_profile` | SDOHProfile | Yes | Social determinants composite |
| `healthcare_access` | HealthcareAccess | Yes | Insurance and provider metrics |
| `utilization_patterns` | UtilizationPatterns | No | Expected utilization rates |
| `benchmarks` | Benchmarks | No | Comparison to national/state |
| `metadata` | ProfileMetadata | Yes | Data sources and timestamps |

---

## Demographics Object

### Structure

```json
{
  "demographics": {
    "total_population": 4700000,
    
    "age_distribution": {
      "0_4": 0.062,
      "5_17": 0.168,
      "18_24": 0.098,
      "25_34": 0.148,
      "35_44": 0.138,
      "45_54": 0.128,
      "55_64": 0.118,
      "65_74": 0.082,
      "75_plus": 0.058
    },
    
    "sex_distribution": {
      "male": 0.492,
      "female": 0.508
    },
    
    "race_ethnicity": {
      "white_nh": 0.298,
      "black_nh": 0.192,
      "hispanic": 0.432,
      "asian_nh": 0.072,
      "aian_nh": 0.004,
      "nhpi_nh": 0.001,
      "multiracial_nh": 0.022,
      "other_nh": 0.008
    },
    
    "median_age": 33.8,
    "dependency_ratio": 0.52,
    
    "household_composition": {
      "average_household_size": 2.78,
      "family_households": 0.682,
      "single_person": 0.248,
      "single_parent": 0.142
    }
  }
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `total_population` | integer | Total population count |
| `age_distribution` | object | Proportion in each age band (sum = 1.0) |
| `sex_distribution` | object | Male/female proportions |
| `race_ethnicity` | object | Race/ethnicity proportions (NH = Non-Hispanic) |
| `median_age` | number | Median age in years |
| `dependency_ratio` | number | (Age <18 + Age 65+) / (Age 18-64) |
| `household_composition` | object | Household structure metrics |

---

## HealthIndicators Object

### Structure

```json
{
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "data_year": 2022,
    
    "chronic_conditions": {
      "diabetes": 0.108,
      "obesity": 0.342,
      "hypertension": 0.348,
      "chd": 0.068,
      "copd": 0.078,
      "depression": 0.198,
      "asthma": 0.102,
      "ckd": 0.038,
      "stroke": 0.042,
      "cancer": 0.072,
      "arthritis": 0.268
    },
    
    "health_behaviors": {
      "current_smoking": 0.148,
      "physical_inactivity": 0.288,
      "binge_drinking": 0.162,
      "short_sleep": 0.368
    },
    
    "prevention": {
      "annual_checkup": 0.762,
      "cholesterol_screening": 0.868,
      "dental_visit": 0.628,
      "mammography": 0.758,
      "colorectal_screening": 0.702
    },
    
    "health_status": {
      "poor_mental_health_days": 0.168,
      "poor_physical_health_days": 0.142,
      "fair_poor_health": 0.188
    }
  }
}
```

### Measure Codes

| Field | CDC PLACES ID | Description |
|-------|---------------|-------------|
| `diabetes` | DIABETES | Adults with diagnosed diabetes |
| `obesity` | OBESITY | Adults with BMI ≥30 |
| `hypertension` | BPHIGH | Adults with high blood pressure |
| `chd` | CHD | Adults with coronary heart disease |
| `copd` | COPD | Adults with COPD |
| `depression` | DEPRESSION | Adults with depressive disorder |
| `current_smoking` | CSMOKING | Current cigarette smokers |
| `physical_inactivity` | LPA | No leisure-time physical activity |

---

## SDOHProfile Object

### Structure

```json
{
  "sdoh_profile": {
    "svi": {
      "overall": 0.72,
      "theme_1_socioeconomic": 0.68,
      "theme_2_household_disability": 0.52,
      "theme_3_minority_language": 0.88,
      "theme_4_housing_transportation": 0.78
    },
    
    "adi": {
      "national_percentile": 72,
      "state_decile": 7
    },
    
    "economic": {
      "median_household_income": 52400,
      "poverty_rate": 0.182,
      "unemployment_rate": 0.068,
      "uninsured_rate": 0.148
    },
    
    "education": {
      "no_hs_diploma": 0.218,
      "bachelors_or_higher": 0.248
    },
    
    "housing": {
      "owner_occupied": 0.548,
      "housing_cost_burden": 0.342,
      "no_vehicle": 0.088
    },
    
    "food_access": {
      "food_insecurity_rate": 0.148,
      "low_access_tract": true
    },
    
    "z_code_rates": {
      "Z59.6": 0.146,
      "Z59.41": 0.118,
      "Z56.0": 0.054,
      "Z59.82": 0.070,
      "Z60.3": 0.068,
      "Z55.0": 0.044
    }
  }
}
```

### Z-Code Mapping

| Z-Code | SDOH Factor | Rate Formula |
|--------|-------------|--------------|
| Z59.6 | Low income | poverty_rate × 0.8 |
| Z59.41 | Food insecurity | food_insecurity_rate × 0.8 |
| Z56.0 | Unemployment | unemployment_rate × 0.8 |
| Z59.82 | Transportation insecurity | no_vehicle × 0.8 |
| Z60.3 | Acculturation difficulty | limited_english × 0.5 |
| Z55.0 | Low literacy | no_hs_diploma × 0.2 |

---

## HealthcareAccess Object

### Structure

```json
{
  "healthcare_access": {
    "insurance_coverage": {
      "commercial": 0.482,
      "medicare": 0.148,
      "medicaid": 0.198,
      "dual_eligible": 0.032,
      "uninsured": 0.148
    },
    
    "provider_access": {
      "pcp_per_100k": 62.4,
      "specialist_per_100k": 48.2,
      "mental_health_per_100k": 128.4,
      "hpsa_designation": "partial"
    },
    
    "facility_access": {
      "hospital_beds_per_1k": 2.1,
      "fqhc_present": true,
      "rural_health_clinic": false,
      "distance_to_hospital_miles": 4.2
    }
  }
}
```

### Insurance Mix Interpretation

| Profile Type | Commercial | Medicare | Medicaid | Uninsured |
|--------------|------------|----------|----------|-----------|
| Affluent suburban | 65-75% | 12-18% | 5-10% | 3-6% |
| Urban mixed | 45-55% | 14-18% | 18-25% | 10-15% |
| High-vulnerability | 30-40% | 15-20% | 28-35% | 15-22% |
| Rural | 40-50% | 18-25% | 15-22% | 12-18% |

---

## UtilizationPatterns Object

### Structure

```json
{
  "utilization_patterns": {
    "ed_visits_per_1k": 428,
    "inpatient_admits_per_1k": 98,
    "avg_los_days": 4.2,
    "readmit_30_day_rate": 0.142,
    "ambulatory_visits_per_capita": 4.8,
    "preventive_visit_rate": 0.62,
    "no_show_rate": 0.182,
    
    "sdoh_adjustments": {
      "ed_multiplier": 1.18,
      "preventive_reduction": 0.88,
      "no_show_multiplier": 1.24
    }
  }
}
```

### SDOH Impact on Utilization

| SVI Quartile | ED Multiplier | Preventive Reduction | No-Show Multiplier |
|--------------|---------------|---------------------|-------------------|
| Q1 (0-0.25) | 0.85 | 1.10 | 0.85 |
| Q2 (0.25-0.50) | 0.95 | 1.02 | 0.95 |
| Q3 (0.50-0.75) | 1.08 | 0.92 | 1.12 |
| Q4 (0.75-1.0) | 1.22 | 0.82 | 1.28 |

---

## Benchmarks Object

### Structure

```json
{
  "benchmarks": {
    "comparison_level": "national",
    
    "health_comparisons": {
      "diabetes": {
        "local": 0.108,
        "benchmark": 0.101,
        "percentile": 62,
        "status": "above_average"
      },
      "obesity": {
        "local": 0.342,
        "benchmark": 0.321,
        "percentile": 68,
        "status": "above_average"
      }
    },
    
    "sdoh_comparisons": {
      "svi_overall": {
        "local": 0.72,
        "benchmark": 0.50,
        "percentile": 72,
        "status": "high_vulnerability"
      }
    }
  }
}
```

---

## ProfileMetadata Object

### Structure

```json
{
  "metadata": {
    "profile_id": "pop-48201-2024-001",
    "created_at": "2024-12-23T10:30:00Z",
    "version": "1.0",
    
    "data_sources": {
      "demographics": {
        "source": "ACS_5YR",
        "vintage": "2018-2022",
        "release_date": "2023-12-07"
      },
      "health": {
        "source": "CDC_PLACES",
        "data_year": 2022,
        "release_date": "2024-06-15"
      },
      "svi": {
        "source": "CDC_ATSDR_SVI",
        "data_year": 2022,
        "version": "2022"
      },
      "adi": {
        "source": "UW_Neighborhood_Atlas",
        "data_year": 2021,
        "version": "4.0"
      }
    },
    
    "generation_context": {
      "generated_by": "PopulationSim",
      "skill_version": "1.0.0",
      "purpose": "cohort_generation"
    }
  }
}
```

---

## Complete Example

```json
{
  "profile_id": "pop-48201-2024-001",
  
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County",
    "state": "TX",
    "state_fips": "48",
    "cbsa_code": "26420",
    "cbsa_name": "Houston-The Woodlands-Sugar Land, TX"
  },
  
  "demographics": {
    "total_population": 4731145,
    "age_distribution": {
      "0_4": 0.068,
      "5_17": 0.172,
      "18_24": 0.092,
      "25_34": 0.158,
      "35_44": 0.142,
      "45_54": 0.128,
      "55_64": 0.112,
      "65_74": 0.078,
      "75_plus": 0.050
    },
    "sex_distribution": {
      "male": 0.498,
      "female": 0.502
    },
    "race_ethnicity": {
      "white_nh": 0.288,
      "black_nh": 0.198,
      "hispanic": 0.438,
      "asian_nh": 0.078,
      "other_nh": 0.018
    },
    "median_age": 33.4
  },
  
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "chronic_conditions": {
      "diabetes": 0.112,
      "obesity": 0.328,
      "hypertension": 0.342
    },
    "health_behaviors": {
      "current_smoking": 0.142,
      "physical_inactivity": 0.268
    }
  },
  
  "sdoh_profile": {
    "svi": {
      "overall": 0.58,
      "theme_1_socioeconomic": 0.54,
      "theme_3_minority_language": 0.72
    },
    "economic": {
      "median_household_income": 58100,
      "poverty_rate": 0.158
    },
    "z_code_rates": {
      "Z59.6": 0.126,
      "Z59.41": 0.098
    }
  },
  
  "healthcare_access": {
    "insurance_coverage": {
      "commercial": 0.508,
      "medicare": 0.138,
      "medicaid": 0.188,
      "uninsured": 0.166
    }
  },
  
  "metadata": {
    "created_at": "2024-12-23T10:30:00Z",
    "version": "1.0",
    "data_sources": {
      "demographics": {"source": "ACS_5YR", "vintage": "2018-2022"}
    }
  }
}
```

---

## Usage in HealthSim

### Input to PatientSim

PopulationProfile drives patient generation demographics, SDOH Z-codes, and condition prevalence.

### Input to MemberSim

PopulationProfile determines insurance mix, service area characteristics, and utilization patterns.

### Input to TrialSim

PopulationProfile informs trial feasibility, diversity planning, and site selection.

---

## Related Models

- [GeographicEntity](geographic-entity.md) - Geography schema
- [SDOHProfile](sdoh-profile.md) - SDOH detail schema
- [CohortSpecification](cohort-specification.md) - Cohort definition schema
