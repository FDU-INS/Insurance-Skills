---
name: county-profile
description: >
  Generate comprehensive county-level population profiles including demographics,
  health indicators, and SDOH indices. Use for county profiling, regional planning,
  service area analysis, or county comparisons. Triggers: "county profile",
  "demographics for [county]", "health indicators for [county]", "profile [county]".
---

# County Profile Skill

## Overview

The county-profile skill generates comprehensive PopulationProfile objects for US counties, combining Census ACS demographics, CDC PLACES health indicators, and SDOH indices (SVI, ADI) into a unified profile.

**Primary Use Cases**:
- Regional health department planning
- Service area demographic analysis
- Health plan market assessment
- County-to-county comparisons
- Foundation for cohort definition

---

## Trigger Phrases

- "Profile [county name]"
- "County profile for [county]"
- "Demographics for [county name], [state]"
- "Health indicators for [county]"
- "Show me [county] population data"
- "Compare [county A] and [county B]"
- "What's the population of [county]?"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `county` | string | Yes | - | County name or FIPS code |
| `state` | string | Conditional | - | Required if county name is ambiguous |
| `include_health` | boolean | No | true | Include CDC PLACES health indicators |
| `include_sdoh` | boolean | No | true | Include SVI and ADI indices |
| `include_access` | boolean | No | true | Include healthcare access metrics |
| `compare_to` | string | No | - | County to compare against |
| `benchmark` | string | No | "state" | Comparison benchmark: "state", "national", "none" |

---

## Data Sources (Embedded v2.0)

This skill reads from PopulationSim's embedded data package for **exact values**:

| Data Type | File | Key Columns |
|-----------|------|-------------|
| Health Indicators | `data/county/places_county_2024.csv` | CountyFIPS, [MEASURE]_CrudePrev |
| SVI Scores | `data/county/svi_county_2022.csv` | STCNTY, RPL_THEMES, RPL_THEME1-4 |
| Demographics | `data/county/svi_county_2022.csv` | E_TOTPOP, EP_POV150, EP_UNINSUR, EP_MINRTY |

### Data Access Pattern

```
1. Resolve county name → FIPS code (via data/crosswalks/fips_county.csv)
2. Read health indicators from places_county_2024.csv
3. Read SVI scores and demographics from svi_county_2022.csv
4. Assemble PopulationProfile with source citations
```

### Key Column Mappings

**CDC PLACES Measures (Wide Format):**
- DIABETES_CrudePrev → Diabetes prevalence
- OBESITY_CrudePrev → Obesity prevalence
- BPHIGH_CrudePrev → Hypertension prevalence
- CSMOKING_CrudePrev → Smoking prevalence
- DEPRESSION_CrudePrev → Depression prevalence

**SVI Columns:**
- RPL_THEMES → Overall SVI (0-1)
- RPL_THEME1 → Socioeconomic Status
- RPL_THEME2 → Household Characteristics
- RPL_THEME3 → Minority/Language
- RPL_THEME4 → Housing/Transportation
- E_TOTPOP → Total population
- EP_POV150 → % below 150% poverty
- EP_UNINSUR → % uninsured
- EP_MINRTY → % minority

---

## Generation Patterns

### Pattern 1: Single County Profile

**Input**: "Profile San Diego County"

**Process**:
1. **Resolve county FIPS:**
   - Read `data/crosswalks/fips_county.csv`
   - Filter: county_name = "San Diego" AND state_abbr = "CA"
   - Result: county_fips = "06073"

2. **Pull CDC PLACES health measures:**
   - Read `data/county/places_county_2024.csv`
   - Filter: CountyFIPS = "06073"
   - Extract: TotalPopulation, DIABETES_CrudePrev, OBESITY_CrudePrev, BPHIGH_CrudePrev, etc.

3. **Pull SVI scores and demographics:**
   - Read `data/county/svi_county_2022.csv`
   - Filter: STCNTY = "06073"
   - Extract: RPL_THEMES, RPL_THEME1-4, E_TOTPOP, EP_POV150, EP_UNINSUR, EP_MINRTY

4. **Assemble PopulationProfile with provenance**

**Output**: Complete PopulationProfile with exact values from embedded data

### Pattern 2: County Comparison

**Input**: "Compare Harris County TX to Los Angeles County CA"

**Process**:
1. Resolve both county FIPS codes (48201, 06037)
2. Read PLACES and SVI data for both counties
3. Calculate absolute and relative differences
4. Identify statistically significant disparities
5. Format comparison table with both values

**Output**: Side-by-side comparison with source citations

### Pattern 3: County with Specific Focus

**Input**: "Show diabetes-related metrics for Cook County IL"

**Process**:
1. Resolve county FIPS: 17031
2. Read PLACES file, extract diabetes-related measures:
   - DIABETES_CrudePrev (primary)
   - OBESITY_CrudePrev (risk factor)
   - BPHIGH_CrudePrev (comorbidity)
   - LPA_CrudePrev (risk factor)
   - CHECKUP_CrudePrev (prevention)
3. Read SVI for socioeconomic context
4. Format focused profile

**Output**: Profile emphasizing diabetes ecosystem

---

## Output Schema

```json
{
  "geography": {
    "type": "county",
    "fips": "06073",
    "name": "San Diego County",
    "state": "CA",
    "state_fips": "06",
    "region": "West",
    "division": "Pacific",
    "urban_rural": "metro",
    "cbsa_code": "41740",
    "cbsa_name": "San Diego-Chula Vista-Carlsbad, CA"
  },
  "demographics": {
    "total_population": 3286069,
    "population_density": 775.2,
    "land_area_sq_mi": 4239.7,
    "median_age": 37.1,
    "age_distribution": {
      "0-4": 0.059,
      "5-17": 0.151,
      "18-24": 0.098,
      "25-34": 0.157,
      "35-44": 0.139,
      "45-54": 0.119,
      "55-64": 0.117,
      "65-74": 0.095,
      "75+": 0.066
    },
    "sex_distribution": {
      "male": 0.495,
      "female": 0.505
    },
    "race_ethnicity": {
      "white_nh": 0.434,
      "hispanic": 0.339,
      "asian": 0.124,
      "black": 0.052,
      "aian": 0.008,
      "nhpi": 0.005,
      "two_or_more": 0.038
    },
    "median_household_income": 102285,
    "per_capita_income": 49377,
    "poverty_rate": 0.103,
    "education": {
      "less_than_hs": 0.112,
      "hs_graduate": 0.178,
      "some_college": 0.281,
      "bachelors_plus": 0.429
    }
  },
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "methodology": "age_adjusted",
    "chronic_conditions": {
      "diabetes": 0.095,
      "obesity": 0.280,
      "hypertension": 0.285,
      "high_cholesterol": 0.318,
      "chd": 0.048,
      "stroke": 0.028,
      "copd": 0.043,
      "asthma": 0.095,
      "ckd": 0.028,
      "depression": 0.195,
      "arthritis": 0.215,
      "cancer": 0.058
    },
    "health_behaviors": {
      "smoking": 0.098,
      "binge_drinking": 0.178,
      "physical_inactivity": 0.182,
      "short_sleep": 0.352
    },
    "prevention": {
      "annual_checkup": 0.785,
      "dental_visit": 0.685,
      "cholesterol_screening": 0.872,
      "colorectal_screening": 0.682,
      "mammography": 0.798
    },
    "health_status": {
      "fair_poor_health": 0.148,
      "poor_mental_health_days": 0.128,
      "poor_physical_health_days": 0.102
    }
  },
  "sdoh_indices": {
    "svi": {
      "source": "CDC_SVI_2022",
      "overall": 0.42,
      "themes": {
        "socioeconomic": 0.38,
        "household_composition": 0.45,
        "minority_language": 0.52,
        "housing_transportation": 0.35
      },
      "interpretation": "moderate"
    },
    "adi": {
      "source": "ADI_2021",
      "national_percentile": 35,
      "state_decile": 4,
      "interpretation": "low_moderate"
    }
  },
  "healthcare_access": {
    "insurance_coverage": {
      "insured_rate": 0.929,
      "uninsured_rate": 0.071,
      "coverage_type": {
        "employer": 0.518,
        "medicare": 0.152,
        "medicaid": 0.181,
        "individual": 0.078,
        "military": 0.058,
        "uninsured": 0.071
      }
    },
    "provider_availability": {
      "pcp_per_100k": 82.4,
      "dentist_per_100k": 89.2,
      "mental_health_per_100k": 215.8
    },
    "facility_access": {
      "hospitals": 28,
      "fqhcs": 47,
      "urgent_care": 142
    }
  },
  "comparison": {
    "benchmark": "state",
    "benchmark_name": "California",
    "notable_differences": [
      {
        "metric": "diabetes_prevalence",
        "county_value": 0.095,
        "benchmark_value": 0.101,
        "difference": -0.006,
        "interpretation": "below_average"
      }
    ]
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "data_vintage": {
      "census": "ACS_2022_5yr",
      "health": "CDC_PLACES_2024",
      "svi": "CDC_SVI_2022",
      "adi": "ADI_2021"
    },
    "reliability": {
      "overall": "high",
      "notes": "Large population county with reliable estimates"
    }
  }
}
```

---

## Examples

### Example 1: Basic County Profile

**Request**: "Profile Harris County, Texas"

**Response**:

**Harris County, TX (FIPS 48201) Population Profile**

| Category | Value | Source |
|----------|-------|--------|
| **Population** | 4,835,125 | CDC PLACES 2024 |
| **Below 150% Poverty** | 25.4% | SVI 2022 |
| **Uninsured** | 21.1% | SVI 2022 |
| **Minority** | 72.4% | SVI 2022 |

**Health Indicators** (CDC PLACES 2024):
| Condition | Harris County | National Avg | Status |
|-----------|---------------|--------------|--------|
| Diabetes | 13.2% | 10.1% | ⚠️ Above |
| Obesity | 37.3% | 32.1% | ⚠️ Above |
| Hypertension | 32.8% | 32.4% | ≈ Average |
| Smoking | 12.7% | 14.1% | ✓ Below |
| Depression | 19.7% | 18.6% | ≈ Average |

**Social Vulnerability Index** (CDC SVI 2022):
| Theme | Score | Interpretation |
|-------|-------|----------------|
| **Overall SVI** | 0.633 | Moderate-High |
| Socioeconomic | 0.671 | Moderate-High |
| Household Comp | 0.586 | Moderate |
| Minority/Language | 0.794 | High |
| Housing/Transport | 0.478 | Moderate |

*Data Sources: CDC PLACES 2024 Release (2022 BRFSS), CDC/ATSDR SVI 2022 (2018-2022 ACS)*

---

### Example 2: County Comparison

**Request**: "Compare San Diego County CA to Cook County IL"

**Response**:

**County Comparison: San Diego vs Cook**

| Metric | San Diego, CA | Cook, IL | Difference |
|--------|---------------|----------|------------|
| Population | 3,269,973 | 5,087,072 | -1.8M |
| Diabetes | 10.0% | 11.8% | -1.8% ✓ |
| Obesity | 25.3% | 31.0% | -5.7% ✓ |
| Hypertension | 28.7% | 31.0% | -2.3% ✓ |
| Smoking | 10.0% | 11.1% | -1.1% ✓ |
| SVI Overall | 0.545 | 0.566 | -0.02 ✓ |

**Key Findings**:
- San Diego has lower chronic disease prevalence across all measures
- San Diego has 5.7% lower obesity rate (significant difference)
- Both counties have moderate social vulnerability
- Cook County has larger population but higher health burden

*Data Sources: CDC PLACES 2024, CDC SVI 2022*

---

### Example 3: Focused Profile

**Request**: "Show cardiovascular health metrics for Cuyahoga County, Ohio"

**Response**:

**Cuyahoga County, OH (FIPS 39035) - Cardiovascular Health Profile**

**Demographics Context** (from embedded data):
- Population: 1,233,088
- SVI Overall: 0.479 (Moderate vulnerability)

**Cardiovascular Conditions** (CDC PLACES 2024):
| Condition | Cuyahoga | National Avg | Status |
|-----------|----------|--------------|--------|
| Coronary Heart Disease | 6.9% | 5.4% | ⚠️ Above |
| Stroke | 4.0% | 3.0% | ⚠️ Above |
| Hypertension | 38.5% | 32.4% | ⚠️ Above |
| Diabetes | 13.4% | 10.1% | ⚠️ Above |

**CV Risk Factors** (CDC PLACES 2024):
| Factor | Cuyahoga | National Avg |
|--------|----------|--------------|
| Obesity | 35.3% | 32.1% |
| Smoking | 14.8% | 14.1% |

**Implications for HealthSim**:
When generating patients from Cuyahoga County, expect higher rates of CV conditions and risk factors, with multiple comorbidities common (HTN + DM + obesity).

*Data Source: CDC PLACES 2024 Release (2022 BRFSS)*

---

## Validation Rules

### Input Validation
- County name must match Census gazetteer or valid FIPS
- State required for ambiguous county names (e.g., "Washington County" exists in 30 states)
- FIPS code must be 5 digits and valid

### Output Validation
- [ ] Population > 0
- [ ] All percentages between 0 and 1
- [ ] Age distribution sums to ~1.0
- [ ] Race/ethnicity sums to ~1.0
- [ ] Health indicators within realistic ranges
- [ ] SVI between 0 and 1
- [ ] Data vintage noted in metadata

### Reliability Thresholds
| Population | Estimate Type | Reliability |
|------------|---------------|-------------|
| > 65,000 | ACS 1-year | High |
| 20,000-65,000 | ACS 5-year | Moderate |
| < 20,000 | ACS 5-year | Use with caution |

---

## Related Skills

- [census-tract-analysis.md](census-tract-analysis.md) - Granular tract-level analysis
- [metro-area-profile.md](metro-area-profile.md) - MSA aggregate profiles
- [custom-region-builder.md](custom-region-builder.md) - Multi-county regions
- [cohort-specification.md](../cohorts/cohort-specification.md) - Define cohorts from profiles
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Disease deep dives

---

## Data Sources

| Data Element | Source | Vintage | Geography |
|--------------|--------|---------|-----------|
| Demographics | Census ACS | 2022 5-year | County |
| Health Indicators | CDC PLACES | 2024 release | County |
| SVI | CDC/ATSDR | 2022 | County (from tracts) |
| ADI | HRSAdmin | 2021 | County (from block groups) |
| Provider Data | HRSA AHRF | 2023 | County |
