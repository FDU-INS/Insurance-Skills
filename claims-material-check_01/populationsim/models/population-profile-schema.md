---
name: population-profile-schema
description: >
  Complete schema definition for PopulationProfile - the core model representing
  geographic population characteristics in PopulationSim. Version 2.0 includes
  per-field data provenance for audit trail and transparency.
version: "2.0"
---

# PopulationProfile Schema v2.0

## Overview

PopulationProfile is the foundational model for PopulationSim, representing the complete demographic, health, and social characteristics of a geographic area. It combines data from Census ACS, CDC PLACES, CDC SVI, ADI, and other sources into a unified structure.

**Version 2.0 adds per-field provenance** - every data point tracks its source, vintage, and methodology for complete audit trail.

---

## Data Provenance Philosophy

PopulationSim v2.0 follows a "data-first" philosophy where generated values are grounded in real reference data. Per-field provenance ensures:

1. **Transparency** - Users know exactly where each value originated
2. **Reproducibility** - Same inputs produce same outputs
3. **Auditability** - Complete chain of custody for compliance
4. **Currency** - Clear vintage information for freshness assessment

---

## Complete Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://healthsim.io/schemas/population-profile-v2",
  "title": "PopulationProfile",
  "description": "Complete population characteristics with per-field provenance",
  "type": "object",
  "required": ["profile_id", "geography", "demographics", "metadata"],
  
  "properties": {
    "profile_id": {
      "type": "string",
      "description": "Unique identifier for this profile",
      "pattern": "^[a-z0-9_-]+$"
    },
    
    "geography": {
      "type": "object",
      "required": ["type", "name"],
      "properties": {
        "type": {
          "type": "string",
          "enum": ["nation", "region", "division", "state", "county", "tract", "block_group", "msa", "custom"]
        },
        "fips": { "type": "string" },
        "name": { "type": "string" },
        "state": { "type": "string" },
        "state_fips": { "type": "string", "pattern": "^[0-9]{2}$" },
        "county_fips": { "type": "string", "pattern": "^[0-9]{5}$" },
        "tract_fips": { "type": "string", "pattern": "^[0-9]{11}$" },
        "block_group_fips": { "type": "string", "pattern": "^[0-9]{12}$" },
        "cbsa_code": { "type": "string", "pattern": "^[0-9]{5}$" },
        "cbsa_name": { "type": "string" },
        "cbsa_type": { "type": "string", "enum": ["metro", "micro"] },
        "population": { "$ref": "#/$defs/provenancedInteger" },
        "households": { "$ref": "#/$defs/provenancedInteger" },
        "land_area_sq_mi": { "$ref": "#/$defs/provenancedNumber" },
        "population_density": { "$ref": "#/$defs/provenancedNumber" },
        "urban_rural": { "type": "string", "enum": ["urban", "suburban", "rural"] }
      }
    },
    
    "demographics": {
      "type": "object",
      "properties": {
        "total_population": { "$ref": "#/$defs/provenancedInteger" },
        "age": {
          "type": "object",
          "properties": {
            "median": { "$ref": "#/$defs/provenancedNumber" },
            "mean": { "$ref": "#/$defs/provenancedNumber" },
            "distribution": { "$ref": "#/$defs/provenancedDistribution" }
          }
        },
        "sex": {
          "type": "object",
          "properties": {
            "male": { "$ref": "#/$defs/provenancedRate" },
            "female": { "$ref": "#/$defs/provenancedRate" }
          }
        },
        "race_ethnicity": {
          "type": "object",
          "properties": {
            "white_nh": { "$ref": "#/$defs/provenancedRate" },
            "black": { "$ref": "#/$defs/provenancedRate" },
            "hispanic": { "$ref": "#/$defs/provenancedRate" },
            "asian": { "$ref": "#/$defs/provenancedRate" },
            "aian": { "$ref": "#/$defs/provenancedRate" },
            "nhpi": { "$ref": "#/$defs/provenancedRate" },
            "two_or_more": { "$ref": "#/$defs/provenancedRate" },
            "other": { "$ref": "#/$defs/provenancedRate" }
          }
        }
      }
    },
    
    "health_indicators": {
      "type": "object",
      "properties": {
        "outcomes": {
          "type": "object",
          "properties": {
            "diabetes": { "$ref": "#/$defs/healthMeasure" },
            "obesity": { "$ref": "#/$defs/healthMeasure" },
            "hypertension": { "$ref": "#/$defs/healthMeasure" },
            "chd": { "$ref": "#/$defs/healthMeasure" },
            "stroke": { "$ref": "#/$defs/healthMeasure" },
            "copd": { "$ref": "#/$defs/healthMeasure" },
            "asthma": { "$ref": "#/$defs/healthMeasure" },
            "cancer": { "$ref": "#/$defs/healthMeasure" },
            "kidney": { "$ref": "#/$defs/healthMeasure" },
            "depression": { "$ref": "#/$defs/healthMeasure" },
            "arthritis": { "$ref": "#/$defs/healthMeasure" },
            "disability": { "$ref": "#/$defs/healthMeasure" }
          }
        },
        "behaviors": {
          "type": "object",
          "properties": {
            "smoking": { "$ref": "#/$defs/healthMeasure" },
            "physical_inactivity": { "$ref": "#/$defs/healthMeasure" },
            "binge_drinking": { "$ref": "#/$defs/healthMeasure" },
            "short_sleep": { "$ref": "#/$defs/healthMeasure" }
          }
        },
        "prevention": {
          "type": "object",
          "properties": {
            "checkup": { "$ref": "#/$defs/healthMeasure" },
            "dental": { "$ref": "#/$defs/healthMeasure" },
            "cholesterol_screening": { "$ref": "#/$defs/healthMeasure" },
            "mammography": { "$ref": "#/$defs/healthMeasure" },
            "colorectal_screening": { "$ref": "#/$defs/healthMeasure" },
            "bp_medication": { "$ref": "#/$defs/healthMeasure" },
            "core_preventive_men": { "$ref": "#/$defs/healthMeasure" },
            "core_preventive_women": { "$ref": "#/$defs/healthMeasure" }
          }
        },
        "disabilities": {
          "type": "object",
          "properties": {
            "any_disability": { "$ref": "#/$defs/healthMeasure" },
            "hearing": { "$ref": "#/$defs/healthMeasure" },
            "vision": { "$ref": "#/$defs/healthMeasure" },
            "cognitive": { "$ref": "#/$defs/healthMeasure" },
            "mobility": { "$ref": "#/$defs/healthMeasure" },
            "self_care": { "$ref": "#/$defs/healthMeasure" },
            "independent_living": { "$ref": "#/$defs/healthMeasure" }
          }
        }
      }
    },
    
    "sdoh_indices": {
      "type": "object",
      "properties": {
        "svi": { "$ref": "#/$defs/sviMeasure" },
        "adi": { "$ref": "#/$defs/adiMeasure" },
        "economic": {
          "type": "object",
          "properties": {
            "median_household_income": { "$ref": "#/$defs/provenancedNumber" },
            "per_capita_income": { "$ref": "#/$defs/provenancedNumber" },
            "poverty_rate": { "$ref": "#/$defs/provenancedRate" },
            "unemployment_rate": { "$ref": "#/$defs/provenancedRate" },
            "gini_coefficient": { "$ref": "#/$defs/provenancedNumber" },
            "snap_recipients": { "$ref": "#/$defs/provenancedRate" }
          }
        },
        "education": {
          "type": "object",
          "properties": {
            "no_hs_diploma": { "$ref": "#/$defs/provenancedRate" },
            "hs_diploma": { "$ref": "#/$defs/provenancedRate" },
            "some_college": { "$ref": "#/$defs/provenancedRate" },
            "bachelors_or_higher": { "$ref": "#/$defs/provenancedRate" }
          }
        },
        "housing": {
          "type": "object",
          "properties": {
            "owner_occupied": { "$ref": "#/$defs/provenancedRate" },
            "median_home_value": { "$ref": "#/$defs/provenancedNumber" },
            "median_rent": { "$ref": "#/$defs/provenancedNumber" },
            "cost_burden": { "$ref": "#/$defs/provenancedRate" },
            "no_vehicle": { "$ref": "#/$defs/provenancedRate" },
            "crowding": { "$ref": "#/$defs/provenancedRate" },
            "mobile_homes": { "$ref": "#/$defs/provenancedRate" },
            "group_quarters": { "$ref": "#/$defs/provenancedRate" }
          }
        }
      }
    },
    
    "healthcare_access": {
      "type": "object",
      "properties": {
        "uninsured": { "$ref": "#/$defs/healthMeasure" },
        "insurance_coverage": {
          "type": "object",
          "properties": {
            "employer": { "$ref": "#/$defs/provenancedRate" },
            "medicaid": { "$ref": "#/$defs/provenancedRate" },
            "medicare": { "$ref": "#/$defs/provenancedRate" },
            "individual": { "$ref": "#/$defs/provenancedRate" },
            "uninsured": { "$ref": "#/$defs/provenancedRate" }
          }
        },
        "provider_availability": {
          "type": "object",
          "properties": {
            "pcp_per_100k": { "$ref": "#/$defs/provenancedNumber" },
            "specialist_per_100k": { "$ref": "#/$defs/provenancedNumber" },
            "hospital_beds_per_100k": { "$ref": "#/$defs/provenancedNumber" },
            "mental_health_per_100k": { "$ref": "#/$defs/provenancedNumber" }
          }
        },
        "hpsa_status": {
          "type": "object",
          "properties": {
            "primary_care": { "type": "boolean" },
            "mental_health": { "type": "boolean" },
            "dental": { "type": "boolean" }
          }
        }
      }
    },
    
    "comparison": {
      "type": "object",
      "description": "Comparison metrics against benchmark geographies",
      "properties": {
        "benchmark": { "type": "string" },
        "benchmark_type": { "type": "string", "enum": ["state", "national", "peer", "custom"] },
        "metrics": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "value": { "type": "number" },
              "benchmark_value": { "type": "number" },
              "difference": { "type": "number" },
              "percentile": { "type": "number", "minimum": 0, "maximum": 100 },
              "interpretation": { "type": "string", "enum": ["better", "similar", "worse"] }
            }
          }
        }
      }
    },
    
    "metadata": {
      "type": "object",
      "required": ["generated_at", "schema_version", "data_package_version"],
      "properties": {
        "generated_at": { "type": "string", "format": "date-time" },
        "schema_version": { "type": "string", "const": "2.0" },
        "data_package_version": { 
          "type": "string",
          "description": "PopulationSim embedded data package version"
        },
        "data_sources_summary": {
          "type": "array",
          "description": "Summary of all data sources used in this profile",
          "items": { "$ref": "#/$defs/dataSourceSummary" }
        },
        "geographic_level": {
          "type": "string",
          "enum": ["county", "tract", "block_group", "state", "national"]
        },
        "completeness": {
          "type": "object",
          "properties": {
            "fields_populated": { "type": "integer" },
            "fields_total": { "type": "integer" },
            "percentage": { "type": "number" }
          }
        },
        "reliability": { "type": "string", "enum": ["high", "moderate", "low"] },
        "notes": { "type": "string" }
      }
    }
  },

  "$defs": {
    "dataProvenance": {
      "type": "object",
      "description": "Source tracking for any data value",
      "required": ["source", "data_year"],
      "properties": {
        "source": {
          "type": "string",
          "description": "Data source identifier",
          "enum": [
            "CDC_PLACES_2024",
            "CDC_SVI_2022", 
            "ADI_2023",
            "CENSUS_ACS_2022",
            "CENSUS_DECENNIAL_2020",
            "CROSSWALK_2023",
            "DERIVED",
            "ESTIMATED"
          ]
        },
        "data_year": {
          "type": "integer",
          "description": "Reference year of the underlying data"
        },
        "release_version": {
          "type": "string",
          "description": "Specific release version (e.g., '2024 Release' for PLACES)"
        },
        "methodology": {
          "type": "string",
          "description": "How the value was obtained",
          "enum": [
            "direct_lookup",
            "model_based_estimate",
            "survey_weighted",
            "aggregated",
            "interpolated",
            "derived_calculation"
          ]
        },
        "file_reference": {
          "type": "string",
          "description": "Path to source file in data package"
        }
      }
    },
    
    "provenancedNumber": {
      "type": "object",
      "description": "Numeric value with provenance",
      "required": ["value", "provenance"],
      "properties": {
        "value": { "type": "number" },
        "provenance": { "$ref": "#/$defs/dataProvenance" }
      }
    },
    
    "provenancedInteger": {
      "type": "object",
      "description": "Integer value with provenance",
      "required": ["value", "provenance"],
      "properties": {
        "value": { "type": "integer", "minimum": 0 },
        "provenance": { "$ref": "#/$defs/dataProvenance" }
      }
    },
    
    "provenancedRate": {
      "type": "object",
      "description": "Rate/proportion (0-1) with provenance",
      "required": ["value", "provenance"],
      "properties": {
        "value": { "type": "number", "minimum": 0, "maximum": 1 },
        "provenance": { "$ref": "#/$defs/dataProvenance" }
      }
    },
    
    "provenancedDistribution": {
      "type": "object",
      "description": "Distribution object with provenance",
      "required": ["values", "provenance"],
      "properties": {
        "values": {
          "type": "object",
          "additionalProperties": { "type": "number", "minimum": 0, "maximum": 1 }
        },
        "provenance": { "$ref": "#/$defs/dataProvenance" }
      }
    },
    
    "healthMeasure": {
      "type": "object",
      "description": "Health measure with confidence interval and provenance",
      "required": ["crude_prevalence", "provenance"],
      "properties": {
        "crude_prevalence": { 
          "type": "number", 
          "minimum": 0, 
          "maximum": 100,
          "description": "Crude prevalence as percentage (0-100)"
        },
        "crude_95ci": {
          "type": "object",
          "properties": {
            "low": { "type": "number" },
            "high": { "type": "number" }
          }
        },
        "age_adjusted_prevalence": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "Age-adjusted prevalence as percentage (0-100)"
        },
        "age_adjusted_95ci": {
          "type": "object",
          "properties": {
            "low": { "type": "number" },
            "high": { "type": "number" }
          }
        },
        "reliable": { 
          "type": "boolean",
          "description": "Whether estimate meets reliability threshold"
        },
        "provenance": { "$ref": "#/$defs/dataProvenance" }
      }
    },
    
    "sviMeasure": {
      "type": "object",
      "description": "Social Vulnerability Index with all themes and provenance",
      "required": ["overall_percentile", "provenance"],
      "properties": {
        "overall_percentile": { 
          "type": "number", 
          "minimum": 0, 
          "maximum": 1,
          "description": "Overall SVI percentile (0-1, higher = more vulnerable)"
        },
        "theme1_socioeconomic": { "type": "number", "minimum": 0, "maximum": 1 },
        "theme2_household_disability": { "type": "number", "minimum": 0, "maximum": 1 },
        "theme3_minority_language": { "type": "number", "minimum": 0, "maximum": 1 },
        "theme4_housing_transport": { "type": "number", "minimum": 0, "maximum": 1 },
        "flag_count": {
          "type": "integer",
          "minimum": 0,
          "maximum": 4,
          "description": "Number of themes in 90th percentile or above"
        },
        "vulnerability_category": {
          "type": "string",
          "enum": ["low", "moderate", "high", "very_high"]
        },
        "provenance": { "$ref": "#/$defs/dataProvenance" }
      }
    },
    
    "adiMeasure": {
      "type": "object",
      "description": "Area Deprivation Index with provenance",
      "required": ["provenance"],
      "properties": {
        "national_percentile": { 
          "type": "integer", 
          "minimum": 1, 
          "maximum": 100,
          "description": "National ADI percentile (1-100, higher = more deprived)"
        },
        "state_decile": { 
          "type": "integer", 
          "minimum": 1, 
          "maximum": 10,
          "description": "State-level ADI decile (1-10)"
        },
        "deprivation_category": {
          "type": "string",
          "enum": ["low", "moderate", "high", "very_high"],
          "description": "Categorical interpretation of ADI"
        },
        "provenance": { "$ref": "#/$defs/dataProvenance" }
      }
    },
    
    "dataSourceSummary": {
      "type": "object",
      "description": "Summary entry for a data source used in the profile",
      "properties": {
        "source_id": { "type": "string" },
        "name": { "type": "string" },
        "release_version": { "type": "string" },
        "data_year": { "type": "integer" },
        "geographic_coverage": { "type": "string" },
        "file_path": { "type": "string" },
        "fields_used": { "type": "integer" }
      }
    }
  }
}
```

---

## Example Instance (with Provenance)

```json
{
  "profile_id": "harris_county_tx_2024",
  
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County",
    "state": "TX",
    "state_fips": "48",
    "county_fips": "48201",
    "cbsa_code": "26420",
    "cbsa_name": "Houston-The Woodlands-Sugar Land, TX",
    "cbsa_type": "metro",
    "population": {
      "value": 4731145,
      "provenance": {
        "source": "CDC_PLACES_2024",
        "data_year": 2022,
        "methodology": "direct_lookup",
        "file_reference": "data/county/places_county_2024.csv"
      }
    },
    "urban_rural": "urban"
  },
  
  "demographics": {
    "total_population": {
      "value": 4731145,
      "provenance": {
        "source": "CDC_PLACES_2024",
        "data_year": 2022,
        "methodology": "direct_lookup",
        "file_reference": "data/county/places_county_2024.csv"
      }
    },
    "race_ethnicity": {
      "hispanic": {
        "value": 0.44,
        "provenance": {
          "source": "CDC_SVI_2022",
          "data_year": 2022,
          "release_version": "2022",
          "methodology": "survey_weighted",
          "file_reference": "data/county/svi_county_2022.csv"
        }
      },
      "black": {
        "value": 0.20,
        "provenance": {
          "source": "CDC_SVI_2022",
          "data_year": 2022,
          "methodology": "survey_weighted",
          "file_reference": "data/county/svi_county_2022.csv"
        }
      }
    }
  },
  
  "health_indicators": {
    "outcomes": {
      "diabetes": {
        "crude_prevalence": 12.1,
        "crude_95ci": { "low": 11.8, "high": 12.4 },
        "age_adjusted_prevalence": 11.5,
        "age_adjusted_95ci": { "low": 11.2, "high": 11.8 },
        "reliable": true,
        "provenance": {
          "source": "CDC_PLACES_2024",
          "data_year": 2022,
          "release_version": "2024 Release",
          "methodology": "model_based_estimate",
          "file_reference": "data/county/places_county_2024.csv"
        }
      },
      "obesity": {
        "crude_prevalence": 32.8,
        "crude_95ci": { "low": 32.3, "high": 33.3 },
        "age_adjusted_prevalence": 32.1,
        "reliable": true,
        "provenance": {
          "source": "CDC_PLACES_2024",
          "data_year": 2022,
          "methodology": "model_based_estimate",
          "file_reference": "data/county/places_county_2024.csv"
        }
      }
    },
    "behaviors": {
      "physical_inactivity": {
        "crude_prevalence": 28.4,
        "reliable": true,
        "provenance": {
          "source": "CDC_PLACES_2024",
          "data_year": 2022,
          "methodology": "model_based_estimate",
          "file_reference": "data/county/places_county_2024.csv"
        }
      }
    }
  },
  
  "sdoh_indices": {
    "svi": {
      "overall_percentile": 0.68,
      "theme1_socioeconomic": 0.62,
      "theme2_household_disability": 0.55,
      "theme3_minority_language": 0.79,
      "theme4_housing_transport": 0.48,
      "flag_count": 1,
      "vulnerability_category": "high",
      "provenance": {
        "source": "CDC_SVI_2022",
        "data_year": 2022,
        "release_version": "2022",
        "methodology": "direct_lookup",
        "file_reference": "data/county/svi_county_2022.csv"
      }
    },
    "economic": {
      "median_household_income": {
        "value": 62320,
        "provenance": {
          "source": "CDC_SVI_2022",
          "data_year": 2022,
          "methodology": "survey_weighted",
          "file_reference": "data/county/svi_county_2022.csv"
        }
      },
      "poverty_rate": {
        "value": 0.158,
        "provenance": {
          "source": "CDC_SVI_2022",
          "data_year": 2022,
          "methodology": "survey_weighted",
          "file_reference": "data/county/svi_county_2022.csv"
        }
      }
    }
  },
  
  "healthcare_access": {
    "uninsured": {
      "crude_prevalence": 22.1,
      "crude_95ci": { "low": 21.6, "high": 22.6 },
      "reliable": true,
      "provenance": {
        "source": "CDC_PLACES_2024",
        "data_year": 2022,
        "methodology": "model_based_estimate",
        "file_reference": "data/county/places_county_2024.csv"
      }
    }
  },
  
  "metadata": {
    "generated_at": "2024-12-23T15:30:00Z",
    "schema_version": "2.0",
    "data_package_version": "2.0.0",
    "geographic_level": "county",
    "data_sources_summary": [
      {
        "source_id": "CDC_PLACES_2024",
        "name": "CDC PLACES",
        "release_version": "2024 Release",
        "data_year": 2022,
        "geographic_coverage": "county",
        "file_path": "data/county/places_county_2024.csv",
        "fields_used": 15
      },
      {
        "source_id": "CDC_SVI_2022",
        "name": "CDC Social Vulnerability Index",
        "release_version": "2022",
        "data_year": 2022,
        "geographic_coverage": "county",
        "file_path": "data/county/svi_county_2022.csv",
        "fields_used": 12
      }
    ],
    "completeness": {
      "fields_populated": 27,
      "fields_total": 45,
      "percentage": 60.0
    },
    "reliability": "high"
  }
}
```

---

## Provenance Source Reference

| Source ID | Full Name | Geographic Levels | Data Year | Methodology |
|-----------|-----------|-------------------|-----------|-------------|
| CDC_PLACES_2024 | CDC PLACES 2024 Release | County, Tract | 2022 BRFSS | Model-based small area estimates |
| CDC_SVI_2022 | CDC/ATSDR Social Vulnerability Index | County, Tract | 2018-2022 ACS | Percentile ranking |
| ADI_2023 | Area Deprivation Index v4.0.1 | Block Group | 2019-2023 ACS | Factor analysis composite |
| CENSUS_ACS_2022 | American Community Survey | All | 2022 | Survey estimates |
| CROSSWALK_2023 | Census Geographic Crosswalks | All | 2023 | Direct mapping |

---

## Simplified Output Mode

For applications that don't require full provenance, the schema supports a `simplified` output mode that returns only values:

```json
{
  "profile_id": "harris_county_tx_2024",
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County",
    "population": 4731145
  },
  "health_indicators": {
    "outcomes": {
      "diabetes": 12.1,
      "obesity": 32.8
    }
  },
  "sdoh_indices": {
    "svi": { "overall": 0.68 }
  },
  "metadata": {
    "generated_at": "2024-12-23T15:30:00Z",
    "schema_version": "2.0",
    "output_mode": "simplified"
  }
}
```

---

## Related Schemas

- [CohortSpecification](cohort-specification-schema.md) - Uses PopulationProfile as input
- [CrossProductIntegration](cross-product-integration.md) - Product mapping
- [Data Package README](../data/README.md) - Embedded data documentation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2024-12-23 | Added per-field provenance, ADI support, simplified output mode |
| 1.0 | 2024-11-15 | Initial schema with aggregate data_sources in metadata |
