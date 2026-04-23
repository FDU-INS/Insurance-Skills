# SDOHProfile Model

## Overview

The SDOHProfile provides a comprehensive representation of Social Determinants of Health (SDOH) characteristics for a geographic area or population cohort. It integrates data from multiple sources (SVI, ADI, ACS) and maps to clinical coding systems (ICD-10 Z-codes).

---

## Model Structure

```
SDOHProfile
├── summary_indices               # SVI, ADI composite scores
├── economic_factors              # Income, poverty, employment
├── education_factors             # Educational attainment
├── housing_factors               # Housing stability, quality
├── transportation_factors        # Vehicle access, transit
├── food_access_factors           # Food security, desert status
├── healthcare_access_factors     # Insurance, provider availability
├── social_context_factors        # Social cohesion, isolation
├── environmental_factors         # Air quality, built environment
├── z_code_mapping                # ICD-10-CM Z-code prevalence
└── metadata                      # Sources and methodology
```

---

## Schema Definition

### Root Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `profile_id` | string | Yes | Unique identifier |
| `geography` | GeographicEntity | Yes | Associated geography |
| `summary_indices` | SummaryIndices | Yes | Composite vulnerability scores |
| `economic_factors` | EconomicFactors | Yes | Economic indicators |
| `education_factors` | EducationFactors | Yes | Education indicators |
| `housing_factors` | HousingFactors | Yes | Housing indicators |
| `transportation_factors` | TransportationFactors | No | Transportation access |
| `food_access_factors` | FoodAccessFactors | No | Food security |
| `healthcare_access_factors` | HealthcareAccessFactors | No | Healthcare access |
| `social_context_factors` | SocialContextFactors | No | Social environment |
| `environmental_factors` | EnvironmentalFactors | No | Environmental quality |
| `z_code_mapping` | ZCodeMapping | Yes | Z-code prevalence |
| `metadata` | SDOHMetadata | Yes | Data sources |

---

## SummaryIndices Object

### Structure

```json
{
  "summary_indices": {
    "svi": {
      "overall": 0.72,
      "percentile_rank": 72,
      "vulnerability_level": "high",
      
      "themes": {
        "socioeconomic": {
          "score": 0.68,
          "rank": 68,
          "flag": false
        },
        "household_disability": {
          "score": 0.52,
          "rank": 52,
          "flag": false
        },
        "minority_language": {
          "score": 0.88,
          "rank": 88,
          "flag": false
        },
        "housing_transportation": {
          "score": 0.78,
          "rank": 78,
          "flag": false
        }
      }
    },
    
    "adi": {
      "national_percentile": 72,
      "state_decile": 7,
      "deprivation_level": "high"
    },
    
    "composite_vulnerability": {
      "score": 0.74,
      "level": "high",
      "method": "weighted_svi_adi"
    }
  }
}
```

### Vulnerability Levels

| Level | SVI Range | ADI Percentile | Description |
|-------|-----------|----------------|-------------|
| `low` | 0.00-0.25 | 1-25 | Low vulnerability/deprivation |
| `moderate` | 0.25-0.50 | 26-50 | Moderate vulnerability |
| `high` | 0.50-0.75 | 51-75 | High vulnerability |
| `very_high` | 0.75-1.00 | 76-100 | Very high vulnerability |

---

## EconomicFactors Object

### Structure

```json
{
  "economic_factors": {
    "income": {
      "median_household_income": 52400,
      "median_family_income": 58200,
      "per_capita_income": 28400,
      "income_quintile": 2
    },
    
    "poverty": {
      "poverty_rate": 0.182,
      "deep_poverty_rate": 0.088,
      "child_poverty_rate": 0.248,
      "elderly_poverty_rate": 0.124,
      "poverty_level": "high"
    },
    
    "employment": {
      "unemployment_rate": 0.068,
      "labor_force_participation": 0.648,
      "employment_population_ratio": 0.604
    },
    
    "public_assistance": {
      "snap_rate": 0.148,
      "medicaid_rate": 0.198,
      "ssi_rate": 0.048,
      "tanf_rate": 0.022
    },
    
    "economic_stability_score": 0.42
  }
}
```

### Poverty Level Classification

| Level | Poverty Rate | Description |
|-------|--------------|-------------|
| `low` | <10% | Low poverty |
| `moderate` | 10-15% | Moderate poverty |
| `high` | 15-25% | High poverty |
| `very_high` | >25% | Concentrated poverty |

---

## EducationFactors Object

### Structure

```json
{
  "education_factors": {
    "attainment": {
      "no_hs_diploma": 0.218,
      "hs_diploma": 0.282,
      "some_college": 0.232,
      "bachelors_degree": 0.168,
      "graduate_degree": 0.100
    },
    
    "literacy": {
      "estimated_low_literacy": 0.142,
      "limited_english_proficiency": 0.168
    },
    
    "school_enrollment": {
      "preschool_enrollment": 0.482,
      "school_age_enrollment": 0.942
    },
    
    "education_access_score": 0.58
  }
}
```

---

## HousingFactors Object

### Structure

```json
{
  "housing_factors": {
    "tenure": {
      "owner_occupied": 0.548,
      "renter_occupied": 0.452
    },
    
    "affordability": {
      "housing_cost_burden_owner": 0.242,
      "housing_cost_burden_renter": 0.482,
      "severe_cost_burden": 0.182
    },
    
    "quality": {
      "overcrowding": 0.082,
      "no_complete_plumbing": 0.004,
      "no_complete_kitchen": 0.008,
      "built_before_1970": 0.342
    },
    
    "stability": {
      "moved_last_year": 0.168,
      "housing_instability_index": 0.38
    },
    
    "structure_type": {
      "single_family_detached": 0.548,
      "single_family_attached": 0.082,
      "small_multifamily": 0.148,
      "large_multifamily": 0.168,
      "mobile_home": 0.054
    },
    
    "housing_stability_score": 0.52
  }
}
```

### Housing Cost Burden

| Level | Cost as % of Income | Description |
|-------|---------------------|-------------|
| No burden | <30% | Affordable housing |
| Cost burden | 30-50% | Moderate burden |
| Severe burden | ≥50% | Severe burden |

---

## TransportationFactors Object

### Structure

```json
{
  "transportation_factors": {
    "vehicle_access": {
      "no_vehicle_households": 0.088,
      "one_vehicle_households": 0.342,
      "two_plus_vehicles": 0.570
    },
    
    "commute": {
      "mean_commute_time_minutes": 28.4,
      "public_transit_commuters": 0.048,
      "work_from_home": 0.082,
      "carpool": 0.098
    },
    
    "transit_access": {
      "within_half_mile_transit": 0.682,
      "transit_frequency_index": 0.58
    },
    
    "transportation_access_score": 0.62
  }
}
```

---

## FoodAccessFactors Object

### Structure

```json
{
  "food_access_factors": {
    "food_insecurity": {
      "food_insecurity_rate": 0.148,
      "child_food_insecurity_rate": 0.198,
      "severity": "moderate"
    },
    
    "food_desert": {
      "low_access_tract": true,
      "distance_to_supermarket_miles": 1.8,
      "snap_retailers_per_1000": 2.4
    },
    
    "food_assistance": {
      "snap_participation_rate": 0.148,
      "wic_participation_rate": 0.042,
      "free_reduced_lunch_rate": 0.682
    },
    
    "food_access_score": 0.48
  }
}
```

### Food Desert Definition

| Type | Urban Threshold | Rural Threshold |
|------|-----------------|-----------------|
| Low access | >1 mile to supermarket | >10 miles |
| Low access, low income | Low access + poverty ≥20% | Same |

---

## HealthcareAccessFactors Object

### Structure

```json
{
  "healthcare_access_factors": {
    "insurance_coverage": {
      "uninsured_rate": 0.148,
      "public_insurance_rate": 0.348,
      "private_insurance_rate": 0.504,
      "underinsured_estimate": 0.182
    },
    
    "provider_availability": {
      "pcp_per_100k": 62.4,
      "specialist_per_100k": 48.2,
      "mental_health_per_100k": 128.4,
      "dentist_per_100k": 52.8
    },
    
    "shortage_areas": {
      "primary_care_hpsa": "partial",
      "mental_health_hpsa": "full",
      "dental_hpsa": "partial",
      "medically_underserved": true
    },
    
    "facility_access": {
      "distance_to_hospital_miles": 4.2,
      "distance_to_fqhc_miles": 2.8,
      "distance_to_pharmacy_miles": 1.4
    },
    
    "healthcare_access_score": 0.54
  }
}
```

### HPSA Designations

| Designation | Description |
|-------------|-------------|
| `full` | Entire area is HPSA |
| `partial` | Part of area is HPSA |
| `none` | No HPSA designation |

---

## SocialContextFactors Object

### Structure

```json
{
  "social_context_factors": {
    "household_composition": {
      "single_person_households": 0.248,
      "single_parent_households": 0.142,
      "multigenerational_households": 0.068,
      "living_alone_65_plus": 0.098
    },
    
    "social_isolation_risk": {
      "score": 0.42,
      "elderly_living_alone": 0.098,
      "limited_english_household": 0.068,
      "disability_rate": 0.128
    },
    
    "community_factors": {
      "group_quarters_population": 0.022,
      "institutionalized_population": 0.012,
      "recent_immigrants": 0.048
    },
    
    "social_cohesion_score": 0.52
  }
}
```

---

## EnvironmentalFactors Object

### Structure

```json
{
  "environmental_factors": {
    "air_quality": {
      "pm25_annual_avg": 9.8,
      "ozone_days_exceeding_standard": 12,
      "air_quality_index": "moderate"
    },
    
    "built_environment": {
      "walk_score": 42,
      "bike_score": 38,
      "transit_score": 35,
      "park_access_pct": 0.682
    },
    
    "environmental_hazards": {
      "superfund_site_proximity": false,
      "flood_zone": "moderate",
      "heat_vulnerability_index": 0.68
    },
    
    "environmental_quality_score": 0.58
  }
}
```

---

## ZCodeMapping Object

### Structure

```json
{
  "z_code_mapping": {
    "prevalence_rates": {
      "Z55.0": {
        "code": "Z55.0",
        "description": "Illiteracy and low-level literacy",
        "rate": 0.044,
        "source_factor": "no_hs_diploma",
        "calculation": "no_hs_diploma * 0.2"
      },
      "Z56.0": {
        "code": "Z56.0",
        "description": "Unemployment, unspecified",
        "rate": 0.054,
        "source_factor": "unemployment_rate",
        "calculation": "unemployment_rate * 0.8"
      },
      "Z59.00": {
        "code": "Z59.00",
        "description": "Homelessness, unspecified",
        "rate": 0.008,
        "source_factor": "homelessness_estimate",
        "calculation": "pit_count / population"
      },
      "Z59.1": {
        "code": "Z59.1",
        "description": "Inadequate housing",
        "rate": 0.024,
        "source_factor": "housing_quality",
        "calculation": "overcrowding + no_plumbing"
      },
      "Z59.41": {
        "code": "Z59.41",
        "description": "Food insecurity",
        "rate": 0.118,
        "source_factor": "food_insecurity_rate",
        "calculation": "food_insecurity_rate * 0.8"
      },
      "Z59.6": {
        "code": "Z59.6",
        "description": "Low income",
        "rate": 0.146,
        "source_factor": "poverty_rate",
        "calculation": "poverty_rate * 0.8"
      },
      "Z59.7": {
        "code": "Z59.7",
        "description": "Insufficient social insurance",
        "rate": 0.118,
        "source_factor": "uninsured_rate",
        "calculation": "uninsured_rate * 0.8"
      },
      "Z59.82": {
        "code": "Z59.82",
        "description": "Transportation insecurity",
        "rate": 0.070,
        "source_factor": "no_vehicle",
        "calculation": "no_vehicle * 0.8"
      },
      "Z60.2": {
        "code": "Z60.2",
        "description": "Problems related to living alone",
        "rate": 0.078,
        "source_factor": "living_alone_65_plus",
        "calculation": "living_alone_65_plus * 0.8"
      },
      "Z60.3": {
        "code": "Z60.3",
        "description": "Acculturation difficulty",
        "rate": 0.068,
        "source_factor": "limited_english",
        "calculation": "limited_english * 0.4"
      },
      "Z63.5": {
        "code": "Z63.5",
        "description": "Disruption of family by separation",
        "rate": 0.048,
        "source_factor": "single_parent",
        "calculation": "single_parent * 0.3"
      }
    },
    
    "summary": {
      "total_sdoh_encounter_rate": 0.342,
      "average_z_codes_per_patient": 1.4,
      "top_z_codes": ["Z59.6", "Z59.41", "Z59.7"]
    }
  }
}
```

### Z-Code to SDOH Factor Mapping

| Z-Code | SDOH Factor | Multiplier | Rationale |
|--------|-------------|------------|-----------|
| Z55.0 | no_hs_diploma | 0.20 | Subset with functional literacy issues |
| Z56.0 | unemployment_rate | 0.80 | Most unemployed documented |
| Z59.41 | food_insecurity_rate | 0.80 | Clinical documentation rate |
| Z59.6 | poverty_rate | 0.80 | Documented in encounters |
| Z59.7 | uninsured_rate | 0.80 | Coverage-related encounters |
| Z59.82 | no_vehicle | 0.80 | Transport barriers noted |
| Z60.3 | limited_english | 0.40 | Subset with acculturation issues |

---

## SDOHMetadata Object

### Structure

```json
{
  "metadata": {
    "profile_id": "sdoh-48201-2024-001",
    "created_at": "2024-12-23T10:30:00Z",
    "version": "1.0",
    
    "data_sources": {
      "svi": {
        "source": "CDC_ATSDR_SVI",
        "version": "2022",
        "data_year": 2022
      },
      "adi": {
        "source": "UW_Neighborhood_Atlas",
        "version": "4.0",
        "data_year": 2021
      },
      "acs": {
        "source": "ACS_5YR",
        "vintage": "2018-2022"
      },
      "food_access": {
        "source": "USDA_Food_Access",
        "data_year": 2019
      }
    },
    
    "methodology": {
      "z_code_estimation": "factor_based",
      "composite_scoring": "weighted_average",
      "normalization": "percentile_rank"
    }
  }
}
```

---

## Complete Example

```json
{
  "profile_id": "sdoh-48201311500-2024-001",
  
  "geography": {
    "type": "tract",
    "identifiers": {
      "fips": "48201311500",
      "name": "Tract 3115.00",
      "county": "Harris County",
      "state": "TX"
    }
  },
  
  "summary_indices": {
    "svi": {
      "overall": 0.78,
      "themes": {
        "socioeconomic": {"score": 0.72},
        "household_disability": {"score": 0.58},
        "minority_language": {"score": 0.88},
        "housing_transportation": {"score": 0.82}
      }
    },
    "adi": {
      "national_percentile": 78,
      "state_decile": 8
    }
  },
  
  "economic_factors": {
    "income": {"median_household_income": 42500},
    "poverty": {"poverty_rate": 0.228},
    "employment": {"unemployment_rate": 0.078}
  },
  
  "z_code_mapping": {
    "prevalence_rates": {
      "Z59.6": {"rate": 0.182},
      "Z59.41": {"rate": 0.142},
      "Z56.0": {"rate": 0.062}
    },
    "summary": {
      "total_sdoh_encounter_rate": 0.42
    }
  },
  
  "metadata": {
    "created_at": "2024-12-23T10:30:00Z",
    "version": "1.0"
  }
}
```

---

## Usage in HealthSim

### PatientSim Integration

SDOHProfile drives Z-code assignment in patient encounters.

### MemberSim Integration

Informs plan selection, utilization patterns, and payment adjustments.

### TrialSim Integration

Supports diversity planning and social needs assessment.

---

## Related Models

- [PopulationProfile](population-profile.md) - Parent profile
- [CohortSpecification](cohort-specification.md) - SDOH requirements
- [SVI Methodology](../svi-methodology.md) - SVI details
- [ADI Methodology](../adi-methodology.md) - ADI details
