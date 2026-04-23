# PopulationSim Examples

Welcome to PopulationSim - the demographic and SDOH foundation for HealthSim. PopulationSim analyzes real population data from public sources to create specifications that drive realistic synthetic data generation.

## v2.0 Data-First Approach

PopulationSim v2.0 uses **embedded real-world data files**. When you request a profile, Claude looks up actual values:

| Dataset | Coverage | Records |
|---------|----------|---------|
| CDC PLACES 2024 | 40 health measures | 3,144 counties, 84,000 tracts |
| CDC SVI 2022 | 16 vulnerability indicators | 3,144 counties, 84,000 tracts |
| ADI 2023 | Area deprivation | 242,000 block groups |

**Key difference**: Values are **looked up from real data**, not estimated. When you request Harris County, Claude reads the actual diabetes rate (12.1%) from CDC PLACES data.

---

## Example 1: County Population Profile

**Request:**
```
Generate a population profile for Maricopa County, AZ
```

**Output:**
```json
{
  "profile_id": "pop-04013-2024-001",
  "geography": {
    "type": "county",
    "fips": "04013",
    "name": "Maricopa County",
    "state": "Arizona",
    "state_fips": "04"
  },
  "demographics": {
    "total_population": 4420568,
    "age_distribution": {
      "0_17": 0.228,
      "18_24": 0.092,
      "25_44": 0.278,
      "45_64": 0.238,
      "65_plus": 0.164
    },
    "sex_distribution": {
      "male": 0.498,
      "female": 0.502
    },
    "race_ethnicity": {
      "white_nh": 0.532,
      "black_nh": 0.058,
      "hispanic": 0.312,
      "asian_nh": 0.042,
      "other": 0.056
    }
  },
  "health_indicators": {
    "chronic_conditions": {
      "diabetes": 0.098,
      "hypertension": 0.312,
      "obesity": 0.298,
      "depression": 0.188
    },
    "health_behaviors": {
      "smoking": 0.142,
      "physical_inactivity": 0.224,
      "binge_drinking": 0.168
    }
  },
  "sdoh_profile": {
    "svi_overall": 0.42,
    "svi_themes": {
      "socioeconomic": 0.38,
      "household_disability": 0.44,
      "minority_language": 0.52,
      "housing_transportation": 0.36
    },
    "healthcare_access": {
      "uninsured_rate": 0.108,
      "primary_care_hpsa": false
    }
  },
  "data_sources": {
    "demographics": "ACS 5-Year 2018-2022",
    "health_indicators": "CDC PLACES 2023",
    "svi": "CDC/ATSDR SVI 2022"
  }
}
```

**Key Insights:**
- Large, diverse county with significant Hispanic population (31.2%)
- Moderate chronic disease burden, slightly below national average
- Relatively low social vulnerability overall (0.42)
- Higher vulnerability in minority/language theme (0.52)

---

## Example 2: SDOH Vulnerability Analysis

**Request:**
```
Analyze social vulnerability for rural Georgia counties with SVI above 0.70
```

**Output:**
```json
{
  "analysis_id": "svi-ga-rural-001",
  "parameters": {
    "state": "Georgia",
    "geography_type": "county",
    "urban_rural_filter": "rural",
    "svi_threshold": 0.70
  },
  "results": {
    "counties_matching": 42,
    "summary_statistics": {
      "mean_svi": 0.812,
      "median_svi": 0.798,
      "range": [0.702, 0.962]
    },
    "theme_analysis": {
      "socioeconomic": {
        "mean": 0.856,
        "high_vulnerability_count": 38
      },
      "household_disability": {
        "mean": 0.724,
        "high_vulnerability_count": 28
      },
      "minority_language": {
        "mean": 0.612,
        "high_vulnerability_count": 18
      },
      "housing_transportation": {
        "mean": 0.788,
        "high_vulnerability_count": 32
      }
    },
    "top_5_highest": [
      {"fips": "13141", "name": "Hancock County", "svi": 0.962},
      {"fips": "13269", "name": "Taylor County", "svi": 0.948},
      {"fips": "13037", "name": "Calhoun County", "svi": 0.936},
      {"fips": "13061", "name": "Clay County", "svi": 0.924},
      {"fips": "13307", "name": "Webster County", "svi": 0.918}
    ]
  },
  "z_code_prevalence_estimates": {
    "Z59.6_low_income": 0.312,
    "Z59.41_food_insecurity": 0.218,
    "Z59.82_transportation_insecurity": 0.186,
    "Z56.0_unemployment": 0.124
  }
}
```

**Key Insights:**
- 42 rural Georgia counties exceed SVI 0.70 threshold
- Socioeconomic factors are the primary driver (mean 0.856)
- High prevalence of food and transportation insecurity
- These counties ideal for SDOH-focused interventions

---

## Example 3: Cohort Specification

**Request:**
```
Define a cohort for a diabetes prevention study targeting underserved areas of Houston
```

**Output:**
```json
{
  "cohort_id": "cohort-dm-prev-houston-001",
  "purpose": "Diabetes Prevention Program Study",
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County",
    "tract_filter": {
      "svi_min": 0.60,
      "diabetes_prevalence_min": 0.10
    }
  },
  "demographics": {
    "age": {"min": 35, "max": 64},
    "sex": "any",
    "race_ethnicity": {
      "distribution_source": "population_match",
      "diversity_targets": {
        "minority_min": 0.50
      }
    }
  },
  "clinical_profile": {
    "conditions": {
      "prediabetes": {"required": true, "icd10": ["R73.03"]},
      "obesity": {"prevalence": 0.60, "icd10_prefix": "E66"}
    },
    "exclusions": {
      "diabetes": {"icd10_prefix": "E11"},
      "pregnancy": {"icd10_prefix": "O"}
    }
  },
  "sdoh_requirements": {
    "svi_min": 0.60,
    "z_codes": {
      "Z59.6_low_income": {"prevalence": 0.25},
      "Z59.41_food_insecurity": {"prevalence": 0.15}
    }
  },
  "size": {
    "target": 500,
    "tolerance": 0.05
  },
  "integration": {
    "patientsim_enabled": true,
    "output_format": "FHIR_R4"
  },
  "matching_tracts": {
    "count": 234,
    "estimated_eligible": 42800,
    "recruitment_rate_assumption": 0.012
  }
}
```

**Key Insights:**
- Targets high-risk census tracts (SVI ≥ 0.60, diabetes prevalence ≥ 10%)
- Focuses on prediabetic adults with obesity comorbidity
- Built-in diversity requirements (50% minority minimum)
- SDOH documentation requirements for Z-codes
- Ready for PatientSim integration

---

## Example 4: Trial Feasibility Analysis

**Request:**
```
Assess enrollment feasibility for a NASH trial at sites in Houston, Dallas, and Phoenix
```

**Output:**
```json
{
  "feasibility_id": "feas-nash-multi-001",
  "protocol": {
    "condition": "NASH",
    "age_range": {"min": 18, "max": 70},
    "bmi_requirement": {"min": 25},
    "exclusions": ["cirrhosis", "active_cancer", "pregnancy"]
  },
  "sites": [
    {
      "location": "Houston, TX",
      "county_fips": "48201",
      "catchment_analysis": {
        "total_population": 4731145,
        "age_eligible": 3218379,
        "estimated_nash_prevalence": 0.058,
        "estimated_eligible": 186666,
        "diversity_profile": {
          "hispanic": 0.432,
          "black_nh": 0.192,
          "white_nh": 0.298
        }
      },
      "sdoh_factors": {
        "mean_svi": 0.52,
        "pct_high_vulnerability": 0.34,
        "transportation_barrier_pct": 0.12
      },
      "enrollment_projection": {
        "monthly_rate": 8.5,
        "12_month_total": 102,
        "retention_risk": "moderate"
      }
    },
    {
      "location": "Dallas, TX",
      "county_fips": "48113",
      "catchment_analysis": {
        "total_population": 2613539,
        "age_eligible": 1777207,
        "estimated_nash_prevalence": 0.056,
        "estimated_eligible": 99524,
        "diversity_profile": {
          "hispanic": 0.402,
          "black_nh": 0.232,
          "white_nh": 0.288
        }
      },
      "sdoh_factors": {
        "mean_svi": 0.48,
        "pct_high_vulnerability": 0.28,
        "transportation_barrier_pct": 0.10
      },
      "enrollment_projection": {
        "monthly_rate": 6.2,
        "12_month_total": 74,
        "retention_risk": "low"
      }
    },
    {
      "location": "Phoenix, AZ",
      "county_fips": "04013",
      "catchment_analysis": {
        "total_population": 4420568,
        "age_eligible": 3006786,
        "estimated_nash_prevalence": 0.054,
        "estimated_eligible": 162366,
        "diversity_profile": {
          "hispanic": 0.312,
          "black_nh": 0.058,
          "white_nh": 0.532
        }
      },
      "sdoh_factors": {
        "mean_svi": 0.42,
        "pct_high_vulnerability": 0.24,
        "transportation_barrier_pct": 0.08
      },
      "enrollment_projection": {
        "monthly_rate": 7.8,
        "12_month_total": 94,
        "retention_risk": "low"
      }
    }
  ],
  "aggregate_projection": {
    "total_12_month": 270,
    "combined_diversity": {
      "hispanic": 0.382,
      "black_nh": 0.161,
      "white_nh": 0.373
    },
    "fda_diversity_guidance_met": true
  },
  "recommendations": [
    "Houston site offers highest enrollment potential and diversity",
    "Consider community health worker support at Houston site due to SDOH burden",
    "Phoenix site may need targeted Hispanic outreach",
    "All sites viable for 12-month enrollment window"
  ]
}
```

**Key Insights:**
- 3-site network can achieve 270 subjects in 12 months
- Houston offers highest diversity but needs SDOH accommodations
- Phoenix may need targeted Hispanic recruitment
- FDA diversity guidance achievable with current site mix

---

## Quick Reference

| Scenario | Trigger Phrase | Key Output |
|----------|----------------|------------|
| County Profile | "population profile for [County]" | PopulationProfile JSON |
| SDOH Analysis | "social vulnerability in [Area]" | SVI theme breakdown |
| Cohort Definition | "define a cohort for [Study]" | CohortSpecification JSON |
| Trial Feasibility | "assess feasibility for [Trial]" | Site-by-site projections |
| Cross-Product | "generate [N] patients from [Profile]" | PatientSim-ready spec |

---

## Related Documentation

- [PopulationSim SKILL.md](../../skills/populationsim/SKILL.md) - Main skill reference
- [Developer Guide](../../skills/populationsim/developer-guide.md) - Technical guide
- [Prompt Guide](../../skills/populationsim/prompt-guide.md) - More example prompts
- [Integration Guide](../../skills/populationsim/integration/README.md) - Cross-product integration
