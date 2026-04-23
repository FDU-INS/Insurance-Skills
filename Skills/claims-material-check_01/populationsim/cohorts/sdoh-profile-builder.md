---
name: sdoh-profile-builder
description: >
  Build SDOH profiles for cohorts including social vulnerability factors,
  economic barriers, and Z-code assignment rates. Translates population-level
  SDOH data into individual patient/member characteristics. Triggers: "SDOH
  profile", "social factors for cohort", "Z-code rates", "vulnerability profile".
---

# SDOH Profile Builder Skill

## Overview

The sdoh-profile-builder skill creates comprehensive SDOH profiles for cohorts by translating population-level social determinant data into individual-level characteristics. It generates Z-code assignment rates, barrier indicators, and vulnerability scores that can be applied during synthetic patient/member generation.

**Primary Use Cases**:
- Add realistic SDOH to patient records
- Set Z-code assignment rates
- Model social barriers to care
- Support health equity analysis
- Inform utilization patterns

---

## Trigger Phrases

- "SDOH profile for [cohort/geography]"
- "Social factors for diabetic cohort"
- "Z-code rates for [population]"
- "Build vulnerability profile for [area]"
- "What social barriers affect [population]?"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | Geographic source for SDOH data |
| `vulnerability_level` | string | No | "match_geography" | "low", "moderate", "high", "very_high" |
| `focus_domains` | array | No | all | SDOH domains to emphasize |
| `z_code_detail` | bool | No | true | Include specific Z-codes |

---

## Data Sources (Embedded v2.0)

SDOH profiles are built from embedded data files:

| Data Type | File | Key Columns |
|-----------|------|-------------|
| SVI Themes | `data/county/svi_county_2022.csv` | RPL_THEMES, RPL_THEME1-4 |
| SVI Variables | `data/tract/svi_tract_2022.csv` | EP_POV150, EP_UNINSUR, EP_MINRTY |
| ADI Rankings | `data/block_group/adi_blockgroup_2023.csv` | ADI_NATRANK, ADI_STATERNK |
| Food Insecurity | `data/county/places_county_2024.csv` | FOODINSECU_CrudePrev |
| Housing Insecurity | `data/county/places_county_2024.csv` | HOUSINSECU_CrudePrev |
| Transportation | `data/county/places_county_2024.csv` | LACKTRPT_CrudePrev |

### Data Lookup Pattern

```
1. Look up SVI for geography (county or tract)
2. Look up CDC PLACES social needs measures (county)
3. Look up ADI for block groups (aggregate to tract/county if needed)
4. Apply Z-code assignment logic based on rates
5. Return SDOH profile with source citations
```

---

## SDOH to Z-Code Mapping

### Economic Stability (Z59)
| SDOH Factor | Z-Code | Assignment Logic |
|-------------|--------|------------------|
| Poverty (<100% FPL) | Z59.6 | poverty_rate × 0.8 |
| Low income (100-200% FPL) | Z59.6 | low_income_rate × 0.4 |
| Food insecurity | Z59.41 | food_insecurity_rate |
| Housing instability | Z59.81 | housing_burden × 0.6 |
| Homelessness | Z59.0 | homelessness_rate |
| Unemployment | Z56.0 | unemployment_rate × 0.5 |

### Education Access (Z55)
| SDOH Factor | Z-Code | Assignment Logic |
|-------------|--------|------------------|
| Less than HS diploma | Z55.0 | no_hs_diploma_rate × 0.6 |
| Illiteracy/low literacy | Z55.0 | estimate from education |

### Healthcare Access (Z75)
| SDOH Factor | Z-Code | Assignment Logic |
|-------------|--------|------------------|
| No health insurance | Z59.7 | uninsured_rate |
| Inadequate insurance | Z59.7 | underinsured estimate |
| No primary care | Z75.3 | pcp_shortage_indicator |

### Social/Community (Z60, Z62, Z63)
| SDOH Factor | Z-Code | Assignment Logic |
|-------------|--------|------------------|
| Limited English | Z60.3 | limited_english_rate |
| Social isolation | Z60.4 | from SVI household comp |
| Single parent | Z63.5 | single_parent_rate × 0.3 |

### Neighborhood (Z59)
| SDOH Factor | Z-Code | Assignment Logic |
|-------------|--------|------------------|
| Transportation barrier | Z59.82 | no_vehicle_rate |
| Inadequate housing | Z59.1 | substandard_housing_rate |
| Unsafe neighborhood | Z59.89 | from crime/SVI |

---

## Output Schema

```json
{
  "sdoh_profile": {
    "source": {
      "geography": "Harris County, TX",
      "fips": "48201",
      "svi_source": "CDC_SVI_2022",
      "acs_source": "ACS_2022_5yr"
    },
    
    "vulnerability_summary": {
      "svi_overall": 0.62,
      "svi_percentile_interpretation": "Moderate-High vulnerability",
      "adi_mean": 58,
      "vulnerability_level": "moderate_high"
    },
    
    "svi_themes": {
      "socioeconomic": {
        "score": 0.58,
        "poverty_rate": 0.168,
        "unemployment": 0.048,
        "no_hs_diploma": 0.142,
        "uninsured": 0.162
      },
      "household_composition": {
        "score": 0.52,
        "age_65_plus": 0.128,
        "age_17_under": 0.248,
        "disability": 0.108,
        "single_parent": 0.142
      },
      "minority_language": {
        "score": 0.78,
        "minority": 0.72,
        "limited_english": 0.142
      },
      "housing_transportation": {
        "score": 0.58,
        "multi_unit": 0.382,
        "mobile_home": 0.028,
        "crowding": 0.082,
        "no_vehicle": 0.078,
        "group_quarters": 0.018
      }
    },
    
    "domain_indicators": {
      "economic_stability": {
        "poverty_rate": 0.168,
        "deep_poverty": 0.072,
        "food_insecurity": 0.128,
        "housing_cost_burden": 0.382,
        "severe_housing_burden": 0.168
      },
      "education_access": {
        "no_hs_diploma": 0.142,
        "limited_literacy_est": 0.08,
        "no_internet": 0.082
      },
      "healthcare_access": {
        "uninsured": 0.162,
        "no_pcp": 0.124,
        "pcp_shortage_area": false,
        "no_dental_visit": 0.328
      },
      "social_community": {
        "limited_english": 0.142,
        "lives_alone_65plus": 0.082,
        "single_parent_household": 0.142
      },
      "neighborhood": {
        "no_vehicle": 0.078,
        "food_desert": 0.112,
        "substandard_housing": 0.028,
        "pre_1960_housing": 0.182
      }
    },
    
    "z_code_rates": {
      "economic": {
        "Z59.6": { "name": "Low income", "rate": 0.168, "assignment": 0.134 },
        "Z59.41": { "name": "Food insecurity", "rate": 0.128 },
        "Z59.81": { "name": "Housing instability", "rate": 0.101 },
        "Z59.0": { "name": "Homelessness", "rate": 0.008 }
      },
      "employment": {
        "Z56.0": { "name": "Unemployment", "rate": 0.024 },
        "Z56.9": { "name": "Work problem, unspecified", "rate": 0.015 }
      },
      "education": {
        "Z55.0": { "name": "Illiteracy/low-level literacy", "rate": 0.048 },
        "Z55.9": { "name": "Education problem, unspecified", "rate": 0.028 }
      },
      "social": {
        "Z60.3": { "name": "Acculturation difficulty", "rate": 0.142 },
        "Z60.4": { "name": "Social exclusion", "rate": 0.042 },
        "Z60.5": { "name": "Target of discrimination", "rate": 0.025 }
      },
      "housing_transportation": {
        "Z59.1": { "name": "Inadequate housing", "rate": 0.028 },
        "Z59.82": { "name": "Transportation insecurity", "rate": 0.078 }
      },
      "healthcare_access": {
        "Z59.7": { "name": "Insufficient social insurance", "rate": 0.162 },
        "Z75.3": { "name": "Unavailability of health care", "rate": 0.062 }
      }
    },
    
    "composite_z_code_summary": {
      "any_z_code": 0.342,
      "multiple_z_codes": 0.148,
      "mean_z_codes_if_any": 1.6
    },
    
    "health_impact_estimates": {
      "cost_barrier_to_care": 0.142,
      "medication_cost_barrier": 0.108,
      "missed_appointments_barrier": 0.128,
      "delayed_care_30_days": 0.168
    },
    
    "utilization_adjustments": {
      "ed_utilization_multiplier": 1.18,
      "preventive_care_reduction": 0.88,
      "medication_adherence_reduction": 0.92,
      "no_show_rate_multiplier": 1.24
    }
  },
  
  "cohort_application": {
    "target_cohort": "Houston Diabetics",
    "sdoh_prevalence_in_cohort": 0.38,
    "high_sdoh_segment": {
      "size": 0.22,
      "characteristics": {
        "svi_quartile": 4,
        "mean_z_codes": 2.4,
        "expected_utilization": "high_ed_low_preventive"
      }
    }
  },
  
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "methodology": "SVI_ACS_derived"
  }
}
```

---

## Examples

### Example 1: High-Vulnerability Cohort

**Request**: "SDOH profile for Medicaid population in Bronx County"

**Response**:

**Bronx County Medicaid SDOH Profile**

**Vulnerability Summary**:
- SVI Overall: 0.94 (Very High)
- Population: Medicaid beneficiaries
- Expected SDOH prevalence: 62%

**Domain Indicators**:
| Domain | Score | Key Factors |
|--------|-------|-------------|
| Economic | 0.92 | Poverty 28%, Food insecurity 22% |
| Education | 0.78 | No HS diploma 21% |
| Healthcare | 0.62 | N/A (Medicaid covered) |
| Social | 0.88 | Limited English 24%, Single parent 28% |
| Neighborhood | 0.82 | No vehicle 42%, Crowding 14% |

**Z-Code Assignment Rates**:
| Z-Code | Name | Rate |
|--------|------|------|
| Z59.6 | Low income | 42% |
| Z59.41 | Food insecurity | 22% |
| Z60.3 | Acculturation difficulty | 24% |
| Z59.82 | Transportation insecurity | 42% |
| Z59.1 | Inadequate housing | 14% |
| Z63.5 | Disrupted family | 18% |

**Expected Multiple Z-Codes**: 48% of cohort

**Health Impact**:
| Barrier | Prevalence | Effect |
|---------|------------|--------|
| Missed appointments | 28% | +1.4x |
| Medication non-adherence | 24% | +1.3x |
| ED utilization | +45% | vs low-SDOH |
| Preventive care gap | 32% | below target |

---

### Example 2: Clinical Trial SDOH

**Request**: "SDOH considerations for diabetes trial in Atlanta"

**Response**:

**Atlanta Diabetes Trial SDOH Profile**

**Site Context**: Atlanta Metro (CBSA 12060)
- Overall SVI: 0.58 (Moderate)
- High variation by neighborhood

**Trial Implications**:

**Recruitment Barriers**:
| SDOH Factor | Rate | Impact on Enrollment |
|-------------|------|---------------------|
| Transportation | 18% | May miss visits |
| Limited English | 8% | Need interpreters |
| Low income | 22% | Competing priorities |
| Food insecurity | 14% | Affects glycemic control |

**Stratification Consideration**:
| SDOH Level | % of Population | Enrollment Target |
|------------|-----------------|-------------------|
| Low SDOH | 42% | 35% |
| Moderate SDOH | 36% | 35% |
| High SDOH | 22% | 30% |

**Z-Codes to Capture**:
- Z59.6 (Low income) - affects adherence
- Z59.82 (Transportation) - affects visit completion
- Z59.41 (Food insecurity) - affects outcomes

**Retention Risk by SDOH**:
| SDOH Level | Expected Dropout |
|------------|-----------------|
| Low | 12% |
| Moderate | 18% |
| High | 28% ⚠️ |

---

### Example 3: Health Plan Population

**Request**: "SDOH profile for Medicare Advantage population in South Florida"

**Response**:

**South Florida Medicare Advantage SDOH**

**Geography**: Miami-Dade, Broward, Palm Beach counties
**Population**: 65+ Medicare Advantage members

**Age-Adjusted SDOH**:
| Factor | General Pop | Age 65+ Adjusted |
|--------|-------------|------------------|
| Limited English | 28% | 32% |
| Lives alone | 12% | 28% |
| Low income | 18% | 22% |
| No vehicle | 8% | 18% |
| Food insecurity | 12% | 14% |

**Social Isolation Risk**:
- Lives alone 65+: 28%
- No nearby family: 18%
- Limited mobility: 24%
- Z60.4 (Social exclusion): 12%

**Z-Code Profile for MA Population**:
| Z-Code | Prevalence |
|--------|------------|
| Z60.2 | Living alone - 28% |
| Z59.6 | Low income - 22% |
| Z59.82 | Transportation - 18% |
| Z60.3 | Language barrier - 32% |
| Z73.6 | Physical limitations - 24% |

**Care Management Implications**:
- Home visit candidates: 34%
- Transportation assistance need: 18%
- Language services: 32% (Spanish 28%, Creole 4%)
- Social work referral: 22%

---

## Validation Rules

### Distribution Checks
- [ ] Z-code rates ≤ 1.0
- [ ] Z-code rates sum plausibly (<1.5)
- [ ] SVI scores 0-1

### Source Validation
- [ ] Geography valid for SVI lookup
- [ ] ACS data available
- [ ] ADI coverage if used

### Clinical Plausibility
- [ ] Z-code rates match SVI level
- [ ] Health impacts directionally correct

---

## Related Skills

- [cohort-specification.md](cohort-specification.md) - Full cohort
- [svi-analysis.md](../sdoh/svi-analysis.md) - SVI source data
- [adi-analysis.md](../sdoh/adi-analysis.md) - ADI source data
- [economic-indicators.md](../sdoh/economic-indicators.md) - Economic detail
- [community-factors.md](../sdoh/community-factors.md) - Community factors
