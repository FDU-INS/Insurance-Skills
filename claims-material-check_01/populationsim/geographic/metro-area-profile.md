---
name: metro-area-profile
description: >
  Generate population profiles for Metropolitan Statistical Areas (MSAs) and
  Core Based Statistical Areas (CBSAs). Use for metro market analysis, multi-county
  urban area profiling, and cross-metro comparisons. Triggers: "metro area",
  "MSA profile", "metropolitan", "CBSA", "urban market".
---

# Metro Area Profile Skill

## Overview

The metro-area-profile skill generates PopulationProfile objects for Metropolitan Statistical Areas (MSAs) and Core Based Statistical Areas (CBSAs), aggregating data across all counties within the metro definition. This enables analysis of urban markets, labor market areas, and regional healthcare systems.

**Primary Use Cases**:
- Urban market assessment
- Multi-county health system planning
- Cross-metro comparisons for site selection
- Regional disease burden analysis
- Healthcare network service area profiling

**Key Value**: MSAs represent functional economic regions that cross county boundaries, better reflecting actual healthcare markets.

---

## Trigger Phrases

- "Profile the [city] metro area"
- "MSA profile for [metro name]"
- "Show me the [city] metropolitan area demographics"
- "Compare [metro A] to [metro B]"
- "Which metro areas have the highest [condition]?"
- "Top 10 metros by [metric]"
- "Profile the Dallas-Fort Worth CBSA"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `metro` | string | Yes | - | Metro name or CBSA code |
| `include_counties` | boolean | No | true | List constituent counties |
| `include_health` | boolean | No | true | Include health indicators |
| `include_sdoh` | boolean | No | true | Include SDOH indices |
| `compare_to` | string | No | - | Metro to compare against |
| `rank_by` | string | No | - | Metric to rank metros by |
| `top_n` | int | No | 10 | Number of metros in ranking |
| `benchmark` | string | No | "national" | Comparison: "national", "region", "none" |

---

## Data Sources (Embedded v2.0)

Metro area profiles aggregate data from embedded files:

| Data Type | File | Usage |
|-----------|------|-------|
| CBSA Definitions | `data/crosswalks/cbsa_definitions.csv` | Map metro to counties |
| Health Indicators | `data/county/places_county_2024.csv` | Per-county health data |
| SVI Scores | `data/county/svi_county_2022.csv` | Per-county vulnerability |
| County FIPS | `data/crosswalks/fips_county.csv` | County name lookups |

### Metro Aggregation Pattern

```
1. Look up CBSA code from metro name in cbsa_definitions.csv
2. Get all county FIPS codes for that CBSA
3. For each county, read PLACES and SVI data
4. Aggregate using population-weighted averages
5. Return with source citations
```

### Key CBSA Columns
- `cbsa_code`: 5-digit CBSA identifier
- `cbsa_title`: Full metro name (e.g., "Houston-The Woodlands-Sugar Land, TX")
- `cbsa_type`: "Metropolitan" or "Micropolitan"
- `county_fips`: 5-digit county FIPS
- `central_outlying`: County role in the metro

---

## Generation Patterns

### Pattern 1: Single Metro Profile

**Input**: "Profile the Houston metro area"

**Process**:
1. Resolve "Houston" → CBSA 26420 (Houston-The Woodlands-Sugar Land)
2. Identify constituent counties (Harris, Fort Bend, Montgomery, etc.)
3. Aggregate demographics across all counties
4. Calculate population-weighted health indicators
5. Compute metro-level SDOH indices
6. Assemble PopulationProfile

**Output**: Complete metro PopulationProfile

### Pattern 2: Metro Comparison

**Input**: "Compare Atlanta and Charlotte metros for diabetes prevalence"

**Process**:
1. Generate profiles for both metros
2. Focus on diabetes and related metrics
3. Calculate comparative statistics
4. Identify key differences

**Output**: Side-by-side comparison with analysis

### Pattern 3: Metro Ranking

**Input**: "Top 10 metros by uninsured rate"

**Process**:
1. Load all 384 MSAs
2. Calculate uninsured rate for each
3. Rank descending
4. Add context for top 10
5. Include demographic context

**Output**: Ranked list with profiles

---

## Output Schema

```json
{
  "geography": {
    "type": "msa",
    "cbsa_code": "26420",
    "cbsa_name": "Houston-The Woodlands-Sugar Land, TX",
    "cbsa_type": "Metropolitan Statistical Area",
    "principal_city": "Houston",
    "state": "TX",
    "states_included": ["TX"],
    "region": "South",
    "division": "West South Central",
    "constituent_counties": [
      {
        "fips": "48201",
        "name": "Harris County",
        "population": 4731145,
        "pct_of_metro": 0.653
      },
      {
        "fips": "48157",
        "name": "Fort Bend County",
        "population": 822779,
        "pct_of_metro": 0.114
      },
      {
        "fips": "48339",
        "name": "Montgomery County",
        "population": 620443,
        "pct_of_metro": 0.086
      }
    ],
    "county_count": 9
  },
  "demographics": {
    "total_population": 7245672,
    "population_rank": 5,
    "population_density": 728.4,
    "land_area_sq_mi": 9948.4,
    "median_age": 34.8,
    "age_distribution": {
      "0-17": 0.252,
      "18-64": 0.628,
      "65+": 0.120
    },
    "sex_distribution": {
      "male": 0.498,
      "female": 0.502
    },
    "race_ethnicity": {
      "white_nh": 0.304,
      "hispanic": 0.378,
      "black": 0.178,
      "asian": 0.082,
      "two_or_more": 0.042,
      "other": 0.016
    },
    "foreign_born": 0.228,
    "limited_english": 0.142,
    "median_household_income": 75506,
    "per_capita_income": 39842,
    "poverty_rate": 0.118,
    "education": {
      "less_than_hs": 0.148,
      "hs_graduate": 0.218,
      "some_college": 0.268,
      "bachelors_plus": 0.366
    }
  },
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "methodology": "population_weighted_average",
    "chronic_conditions": {
      "diabetes": 0.118,
      "obesity": 0.322,
      "hypertension": 0.318,
      "high_cholesterol": 0.328,
      "chd": 0.054,
      "stroke": 0.032,
      "copd": 0.052,
      "asthma": 0.088,
      "ckd": 0.032,
      "depression": 0.178,
      "cancer": 0.054
    },
    "health_behaviors": {
      "smoking": 0.138,
      "binge_drinking": 0.168,
      "physical_inactivity": 0.248,
      "short_sleep": 0.368
    },
    "prevention": {
      "annual_checkup": 0.762,
      "dental_visit": 0.608,
      "cholesterol_screening": 0.842
    },
    "health_status": {
      "fair_poor_health": 0.172
    }
  },
  "sdoh_indices": {
    "svi": {
      "source": "CDC_SVI_2022",
      "metro_aggregate": 0.58,
      "interpretation": "moderate",
      "themes": {
        "socioeconomic": 0.52,
        "household_composition": 0.48,
        "minority_language": 0.78,
        "housing_transportation": 0.54
      },
      "tract_distribution": {
        "low_0_25": 0.22,
        "low_mod_25_50": 0.24,
        "mod_high_50_75": 0.28,
        "high_75_100": 0.26
      }
    },
    "adi": {
      "source": "ADI_2021",
      "metro_mean_national_percentile": 48,
      "interpretation": "moderate"
    }
  },
  "healthcare_access": {
    "insurance_coverage": {
      "uninsured_rate": 0.162,
      "coverage_type": {
        "employer": 0.498,
        "medicare": 0.112,
        "medicaid": 0.142,
        "individual": 0.068,
        "military": 0.018
      }
    },
    "provider_availability": {
      "pcp_per_100k": 62.4,
      "specialist_per_100k": 148.2,
      "hospital_beds_per_1000": 2.8
    },
    "major_health_systems": [
      "Houston Methodist",
      "Memorial Hermann",
      "Texas Medical Center"
    ]
  },
  "comparison": {
    "benchmark": "national",
    "vs_national": {
      "population_rank": 5,
      "diabetes": { "metro": 0.118, "national": 0.101, "diff": 0.017, "status": "above" },
      "uninsured": { "metro": 0.162, "national": 0.088, "diff": 0.074, "status": "above" },
      "obesity": { "metro": 0.322, "national": 0.321, "diff": 0.001, "status": "similar" }
    }
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "cbsa_definition_year": 2023,
    "data_vintage": {
      "census": "ACS_2022_1yr",
      "health": "CDC_PLACES_2024",
      "svi": "CDC_SVI_2022"
    }
  }
}
```

---

## Examples

### Example 1: Metro Area Profile

**Request**: "Profile the Denver metro area"

**Response**:

**Denver-Aurora-Lakewood, CO Metro Area (CBSA 19740)**

| Metric | Value | vs National |
|--------|-------|-------------|
| **Population** | 2,963,821 | Rank #19 |
| **Median Age** | 37.2 | Similar (38.1) |
| **Median Income** | $92,682 | +36% above |
| **Poverty Rate** | 8.4% | -3.2% below |

**Constituent Counties** (10 total):
| County | Population | % of Metro |
|--------|------------|------------|
| Denver | 715,522 | 24.1% |
| Arapahoe | 656,590 | 22.2% |
| Jefferson | 582,910 | 19.7% |
| Adams | 519,572 | 17.5% |
| Douglas | 351,154 | 11.8% |
| Other (5) | 138,073 | 4.7% |

**Demographics**:
- White NH: 56.8%
- Hispanic: 23.4%
- Black: 5.8%
- Asian: 4.2%

**Health Profile** (CDC PLACES):
| Condition | Denver Metro | Colorado | National |
|-----------|--------------|----------|----------|
| Diabetes | 7.8% | 7.4% | 10.1% | ✓ Below |
| Obesity | 23.4% | 23.8% | 32.1% | ✓ Below |
| Smoking | 12.8% | 13.2% | 14.1% | ✓ Below |
| Binge Drinking | 21.2% | 20.8% | 16.8% | ⚠️ Above |

**SDOH Summary**:
- SVI Overall: 0.32 (low-moderate)
- High-vulnerability tracts: 12.4% of metro

**Healthcare Access**:
- Uninsured: 7.2% (below national 8.8%)
- PCPs per 100K: 94.2 (above national 76.4)

---

### Example 2: Metro Comparison

**Request**: "Compare Phoenix and Las Vegas metros for cardiovascular health"

**Response**:

**Metro Comparison: Phoenix vs Las Vegas**

| | Phoenix-Mesa-Chandler | Las Vegas-Henderson |
|---|----------------------|---------------------|
| **CBSA Code** | 38060 | 29820 |
| **Population** | 4,946,145 | 2,265,461 |
| **Median Age** | 38.1 | 38.4 |

**Cardiovascular Metrics**:
| Metric | Phoenix | Las Vegas | Diff |
|--------|---------|-----------|------|
| CHD | 5.2% | 6.1% | -0.9% ✓ |
| Stroke | 2.8% | 3.2% | -0.4% ✓ |
| Hypertension | 29.8% | 31.2% | -1.4% ✓ |
| High Cholesterol | 30.2% | 31.8% | -1.6% ✓ |

**CV Risk Factors**:
| Factor | Phoenix | Las Vegas | Diff |
|--------|---------|-----------|------|
| Diabetes | 10.2% | 11.8% | -1.6% ✓ |
| Obesity | 30.4% | 28.2% | +2.2% |
| Smoking | 13.8% | 16.2% | -2.4% ✓ |
| Physical Inactivity | 22.4% | 24.8% | -2.4% ✓ |

**Summary**: Phoenix has better cardiovascular health metrics across most measures, with lower CHD, stroke, hypertension, and most risk factors. Las Vegas has lower obesity but higher smoking and physical inactivity.

**SDOH Context**:
| Metric | Phoenix | Las Vegas |
|--------|---------|-----------|
| SVI Overall | 0.51 | 0.62 |
| Uninsured | 9.8% | 11.2% |
| Poverty | 10.8% | 12.1% |

---

### Example 3: Metro Ranking

**Request**: "Top 5 metros by diabetes prevalence"

**Response**:

**Top 5 Metropolitan Areas by Diabetes Prevalence**

| Rank | Metro Area | Diabetes | Population | Key Factors |
|------|------------|----------|------------|-------------|
| 1 | McAllen-Edinburg, TX | 17.2% | 868,707 | 92% Hispanic, poverty 28%, obesity 42% |
| 2 | Brownsville-Harlingen, TX | 16.8% | 423,163 | 91% Hispanic, poverty 31%, border region |
| 3 | Laredo, TX | 15.4% | 267,114 | 96% Hispanic, poverty 25% |
| 4 | Memphis, TN-MS-AR | 14.2% | 1,337,779 | 47% Black, obesity 38%, SVI 0.72 |
| 5 | Jackson, MS | 13.8% | 594,806 | 48% Black, poverty 21%, SVI 0.68 |

**Pattern Analysis**:
- Texas border metros dominate due to: Hispanic population with genetic predisposition, high poverty, limited healthcare access
- Southern metros (Memphis, Jackson): High Black population, high obesity, high SVI
- All top 5 have SVI > 0.65 (moderate-high vulnerability)

**For Comparison - Lowest 5**:
| Rank | Metro Area | Diabetes | Key Factors |
|------|------------|----------|-------------|
| 380 | Boulder, CO | 5.8% | High education, high income, active lifestyle |
| 381 | San Francisco-Oakland, CA | 6.2% | High income, diverse, health-conscious |
| 382 | San Jose-Sunnyvale, CA | 6.4% | High Asian pop, high income, tech hub |

---

## Validation Rules

### Input Validation
- Metro name must match CBSA definition or valid CBSA code
- CBSA code must be 5 digits
- Comparison metros must both be valid

### Output Validation
- [ ] All constituent counties identified
- [ ] Population sums correctly across counties
- [ ] Percentages between 0 and 1
- [ ] Health indicators are population-weighted averages
- [ ] CBSA definition year noted

### Aggregation Rules
- Demographics: Simple sum or population-weighted average
- Health indicators: Population-weighted average across counties
- SVI: Tract-level population-weighted aggregate
- Rates: Recalculated from numerators/denominators, not averaged

---

## Related Skills

- [county-profile.md](county-profile.md) - Individual county profiles
- [census-tract-analysis.md](census-tract-analysis.md) - Tract-level within metro
- [custom-region-builder.md](custom-region-builder.md) - Custom multi-county regions
- [site-selection-support.md](../trial-support/site-selection-support.md) - Rank metros for trial sites
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Disease focus

---

## Data Sources

| Data Element | Source | Vintage | Notes |
|--------------|--------|---------|-------|
| CBSA Definitions | OMB | 2023 | Revised periodically |
| Demographics | Census ACS | 2022 1-year | For metros > 65K pop |
| Health Indicators | CDC PLACES | 2024 | County-level aggregated |
| SVI | CDC/ATSDR | 2022 | Tract-level aggregated |

---

## MSA/CBSA Reference

### Largest US Metropolitan Areas (2022)

| Rank | CBSA | Metro Name | Population |
|------|------|------------|------------|
| 1 | 35620 | New York-Newark-Jersey City | 19,617,864 |
| 2 | 31080 | Los Angeles-Long Beach-Anaheim | 12,872,808 |
| 3 | 16980 | Chicago-Naperville-Elgin | 9,441,575 |
| 4 | 19100 | Dallas-Fort Worth-Arlington | 7,759,615 |
| 5 | 26420 | Houston-The Woodlands-Sugar Land | 7,245,672 |
| 6 | 47900 | Washington-Arlington-Alexandria | 6,361,882 |
| 7 | 37980 | Philadelphia-Camden-Wilmington | 6,228,601 |
| 8 | 33100 | Miami-Fort Lauderdale-Pompano Beach | 6,091,747 |
| 9 | 12060 | Atlanta-Sandy Springs-Alpharetta | 6,089,815 |
| 10 | 14460 | Boston-Cambridge-Newton | 4,899,932 |
