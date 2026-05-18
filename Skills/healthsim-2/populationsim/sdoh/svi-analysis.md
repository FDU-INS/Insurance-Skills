---
name: svi-analysis
description: >
  Analyze CDC Social Vulnerability Index (SVI) including overall scores and
  4 theme breakdowns. Use for identifying vulnerable populations, disaster
  preparedness, and SDOH characterization. Triggers: "SVI", "social vulnerability",
  "vulnerable populations", "CDC SVI", "vulnerability index".
---

# SVI Analysis Skill

## Overview

The svi-analysis skill provides detailed analysis of CDC/ATSDR Social Vulnerability Index (SVI) scores across geographic areas. SVI ranks census tracts on 16 social factors across 4 themes, identifying communities that may need support before, during, and after disasters or health emergencies.

**Primary Use Cases**:
- Identify vulnerable populations
- Disaster/pandemic preparedness planning
- Health equity assessment
- SDOH profile development
- Community health needs assessment

---

## Trigger Phrases

- "What's the SVI for [geography]?"
- "Show vulnerable tracts in [county]"
- "SVI analysis for [area]"
- "Social vulnerability breakdown for [geography]"
- "Compare SVI between [A] and [B]"
- "Which tracts have highest vulnerability?"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, tract, metro, or state |
| `detail_level` | string | No | "themes" | "overall", "themes", "variables" |
| `threshold` | float | No | - | Filter tracts above this SVI |
| `compare_to` | string | No | - | Geography for comparison |
| `ranking` | string | No | "national" | "national" or "state" percentile |

---

## Data Sources (Embedded v2.0)

This skill reads from PopulationSim's embedded SVI data:

| Level | File | Records | Key Columns |
|-------|------|---------|-------------|
| County | `data/county/svi_county_2022.csv` | 3,144 | STCNTY, RPL_THEMES, RPL_THEME1-4 |
| Tract | `data/tract/svi_tract_2022.csv` | 84,120 | FIPS, RPL_THEMES, RPL_THEME1-4, EP_* |

### Key Column Reference

**SVI Ranking Columns (0-1, higher = more vulnerable):**
- `RPL_THEMES`: Overall SVI ranking
- `RPL_THEME1`: Socioeconomic Status
- `RPL_THEME2`: Household Characteristics
- `RPL_THEME3`: Minority/Language Status
- `RPL_THEME4`: Housing/Transportation

**Estimate Columns (E_*):** Raw counts (e.g., E_TOTPOP, E_POV150)
**Percentage Columns (EP_*):** Percentages (e.g., EP_POV150, EP_UNINSUR)
**Missing Values:** -999 indicates suppressed/unavailable data

### Data Lookup Pattern

```
1. Identify geography (county FIPS or tract FIPS)
2. Read appropriate SVI file
3. Filter by STCNTY (county) or FIPS (tract)
4. Extract RPL_* scores and EP_* variables
5. Return with CDC/ATSDR SVI 2022 source citation
```

---

## SVI Structure

### 4 Themes, 16 Variables

**Theme 1: Socioeconomic Status (5 variables)**
| Variable | Definition | Data Source |
|----------|------------|-------------|
| Below 150% poverty | Persons below 150% FPL | ACS S1701 |
| Unemployed | Civilian unemployed | ACS S2301 |
| Housing cost burden | Paying >30% income | ACS DP04 |
| No high school diploma | Adults 25+ without HS | ACS S1501 |
| No health insurance | Persons without insurance | ACS S2701 |

**Theme 2: Household Characteristics (5 variables)**
| Variable | Definition | Data Source |
|----------|------------|-------------|
| Aged 65+ | Persons age 65 or older | ACS S0101 |
| Aged 17 or younger | Persons under 18 | ACS S0101 |
| Civilian with disability | Persons with disability | ACS S1810 |
| Single-parent households | Single parent with children | ACS S1101 |
| Limited English | Speaks English "less than well" | ACS S1601 |

**Theme 3: Racial & Ethnic Minority Status (1 variable)**
| Variable | Definition | Data Source |
|----------|------------|-------------|
| Minority | All except White non-Hispanic | ACS B03002 |

**Theme 4: Housing Type & Transportation (5 variables)**
| Variable | Definition | Data Source |
|----------|------------|-------------|
| Multi-unit structures | In structures with 10+ units | ACS DP04 |
| Mobile homes | Living in mobile homes | ACS DP04 |
| Crowding | >1 person per room | ACS DP04 |
| No vehicle | Households without vehicle | ACS DP04 |
| Group quarters | In non-institutional group quarters | ACS S2601A |

### Scoring Methodology

1. Each variable ranked as percentile (0-1) within reference geography
2. Theme score = sum of variable percentiles / number of variables
3. Overall SVI = sum of all 4 theme scores (can normalize to 0-1)

---

## Output Schema

```json
{
  "analysis_type": "svi_analysis",
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County",
    "state": "TX",
    "tract_count": 1012
  },
  "svi_scores": {
    "overall": {
      "percentile": 0.68,
      "interpretation": "moderate_high",
      "rank_national": "68th percentile",
      "vs_state": 0.04
    },
    "themes": {
      "socioeconomic": {
        "percentile": 0.62,
        "interpretation": "moderate_high",
        "key_drivers": ["poverty", "no_insurance"]
      },
      "household_composition": {
        "percentile": 0.58,
        "interpretation": "moderate",
        "key_drivers": ["age_under_18", "disability"]
      },
      "minority_language": {
        "percentile": 0.82,
        "interpretation": "high",
        "key_drivers": ["minority_status", "limited_english"]
      },
      "housing_transportation": {
        "percentile": 0.64,
        "interpretation": "moderate_high",
        "key_drivers": ["multi_unit", "no_vehicle"]
      }
    }
  },
  "variable_detail": {
    "below_150_poverty": { "rate": 0.228, "percentile": 0.72 },
    "unemployed": { "rate": 0.058, "percentile": 0.52 },
    "no_hs_diploma": { "rate": 0.182, "percentile": 0.68 },
    "no_insurance": { "rate": 0.182, "percentile": 0.88 },
    "age_65_plus": { "rate": 0.112, "percentile": 0.32 },
    "age_under_18": { "rate": 0.264, "percentile": 0.72 },
    "disability": { "rate": 0.092, "percentile": 0.48 },
    "single_parent": { "rate": 0.084, "percentile": 0.62 },
    "limited_english": { "rate": 0.142, "percentile": 0.82 },
    "minority": { "rate": 0.696, "percentile": 0.82 },
    "multi_unit": { "rate": 0.282, "percentile": 0.72 },
    "mobile_home": { "rate": 0.022, "percentile": 0.18 },
    "crowding": { "rate": 0.048, "percentile": 0.78 },
    "no_vehicle": { "rate": 0.068, "percentile": 0.62 },
    "group_quarters": { "rate": 0.018, "percentile": 0.42 }
  },
  "tract_distribution": {
    "low_0_25": { "tract_count": 182, "population": 724000 },
    "low_mod_25_50": { "tract_count": 228, "population": 912000 },
    "mod_high_50_75": { "tract_count": 284, "population": 1136000 },
    "high_75_100": { "tract_count": 318, "population": 1272000 }
  },
  "high_vulnerability_areas": {
    "tract_count": 318,
    "population": 1272000,
    "pct_of_county": 0.314,
    "common_characteristics": [
      "High poverty (>25%)",
      "Limited English proficiency",
      "No health insurance",
      "Crowded housing"
    ],
    "geographic_clusters": [
      { "area": "East Houston", "tracts": 82, "mean_svi": 0.89 },
      { "area": "North Houston", "tracts": 68, "mean_svi": 0.86 },
      { "area": "Southwest Houston", "tracts": 54, "mean_svi": 0.84 }
    ]
  },
  "cohort_implications": {
    "sdoh_profile": {
      "poverty_barrier": 0.228,
      "insurance_barrier": 0.182,
      "language_barrier": 0.142,
      "transportation_barrier": 0.068
    },
    "z_code_rates": {
      "Z59.6_low_income": 0.228,
      "Z60.3_limited_english": 0.142,
      "Z59.82_transportation": 0.068
    }
  },
  "metadata": {
    "svi_version": "CDC_SVI_2022",
    "ranking_reference": "national",
    "generated_at": "2024-12-23T10:00:00Z"
  }
}
```

---

## Examples

### Example 1: County SVI Analysis

**Request**: "Analyze SVI for Bronx County, NY"

**Response**:

**Bronx County (FIPS 36005) SVI Analysis**

**Overall SVI**: 0.94 (94th percentile nationally) ⚠️ Very High

| Theme | Score | Key Drivers |
|-------|-------|-------------|
| Socioeconomic | 0.96 | Poverty 27%, No insurance 9%, Unemployment 9% |
| Household Composition | 0.88 | Single parent 18%, Disability 14% |
| Minority/Language | 0.98 | Minority 91%, Limited English 18% |
| Housing/Transportation | 0.92 | Multi-unit 89%, No vehicle 52%, Crowding 9% |

**Variable Detail**:
| Variable | Rate | Percentile |
|----------|------|------------|
| Below 150% poverty | 38.2% | 0.98 |
| Unemployed | 9.2% | 0.82 |
| No HS diploma | 21.4% | 0.88 |
| No insurance | 9.2% | 0.72 |
| Limited English | 18.4% | 0.92 |
| No vehicle | 52.4% | 0.98 |

**High-Vulnerability Tracts**: 312 of 348 (90%)

**HealthSim Implications**:
- Very high SDOH Z-code assignment rates
- Expect: Z59.6 (low income), Z60.3 (language), Z59.82 (transportation)
- High Medicaid enrollment, low employer coverage
- Higher ED utilization for primary care

---

### Example 2: Theme Comparison

**Request**: "Compare SVI themes across Texas metros"

**Response**:

**Texas Metro SVI Theme Comparison**

| Metro | Overall | Socioeconomic | Household | Minority | Housing |
|-------|---------|---------------|-----------|----------|---------|
| McAllen | 0.92 | 0.94 | 0.78 | 0.98 | 0.84 |
| Houston | 0.68 | 0.62 | 0.58 | 0.82 | 0.64 |
| San Antonio | 0.62 | 0.58 | 0.54 | 0.78 | 0.58 |
| Dallas | 0.58 | 0.52 | 0.48 | 0.74 | 0.56 |
| Austin | 0.42 | 0.38 | 0.44 | 0.62 | 0.48 |

**Pattern Analysis**:
- McAllen: Highest across all themes (border region)
- All metros: Minority/Language theme highest (diverse populations)
- Austin: Lowest overall, but rising housing theme

**Vulnerability Drivers by Metro**:
- McAllen: Poverty, limited English, no insurance
- Houston: No insurance, limited English, crowding
- Dallas: Similar to Houston, slightly lower
- Austin: Housing cost burden emerging issue

---

### Example 3: Tract-Level Hotspots

**Request**: "Find high-SVI tracts in Philadelphia"

**Response**:

**Philadelphia High-SVI Census Tracts (SVI ≥ 0.80)**

**Summary**: 186 of 384 tracts (48%) are high vulnerability

**Top 10 Highest SVI Tracts**:

| Tract | SVI | Population | Key Vulnerabilities |
|-------|-----|------------|---------------------|
| 42101003800 | 0.99 | 3,842 | Poverty 52%, No vehicle 68%, Disability 24% |
| 42101003900 | 0.98 | 4,215 | Poverty 48%, Crowding 12%, Limited English 22% |
| 42101011800 | 0.98 | 3,521 | Poverty 45%, Single parent 28%, No insurance 14% |

**Geographic Clusters**:
1. **North Philadelphia** (68 tracts): Mean SVI 0.91
   - Drivers: Poverty, unemployment, disability
2. **West Philadelphia** (42 tracts): Mean SVI 0.87
   - Drivers: Poverty, single parent, limited English
3. **Kensington** (38 tracts): Mean SVI 0.89
   - Drivers: Poverty, no insurance, crowding

**Health Outcome Correlation**:
| Health Metric | High-SVI | Low-SVI | Gap |
|---------------|----------|---------|-----|
| Diabetes | 14.8% | 8.2% | +6.6% |
| Depression | 24.2% | 16.4% | +7.8% |
| No Checkup | 32.4% | 18.2% | +14.2% |

---

## Validation Rules

### Input Validation
- Geography must be valid (county, tract, metro, state)
- Threshold must be between 0 and 1
- Ranking must be "national" or "state"

### Output Validation
- [ ] SVI values between 0 and 1
- [ ] Theme scores sum appropriately
- [ ] Variable rates match expected ranges
- [ ] Tract counts match geography

---

## Related Skills

- [adi-analysis.md](adi-analysis.md) - Area Deprivation Index
- [economic-indicators.md](economic-indicators.md) - Income detail
- [community-factors.md](community-factors.md) - Housing, transportation
- [census-tract-analysis.md](../geographic/census-tract-analysis.md) - Geographic analysis
- [health-outcome-disparities.md](../health-patterns/health-outcome-disparities.md) - SDOH-health links
