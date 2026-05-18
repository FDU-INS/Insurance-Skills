---
name: adi-analysis
description: >
  Analyze Area Deprivation Index (ADI) for neighborhood-level socioeconomic
  disadvantage assessment. ADI provides block group granularity and state/national
  rankings. Triggers: "ADI", "area deprivation", "neighborhood disadvantage",
  "deprivation index", "ADI ranking".
---

# ADI Analysis Skill

## Overview

The adi-analysis skill provides detailed analysis of the Area Deprivation Index (ADI), a measure of neighborhood socioeconomic disadvantage developed by the Health Resources and Services Administration (HRSA). ADI offers block group-level granularity and both national percentile and state decile rankings.

**Primary Use Cases**:
- Neighborhood disadvantage assessment
- Within-state targeting
- Healthcare resource allocation
- SDOH profile development
- Health outcome correlation

**Key Advantage**: Block group level provides finer granularity than SVI (which uses tracts).

---

## Trigger Phrases

- "What's the ADI for [geography]?"
- "Area deprivation in [neighborhood]"
- "ADI ranking for [area]"
- "Most deprived neighborhoods in [county]"
- "Compare ADI between [A] and [B]"
- "Neighborhood disadvantage analysis"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, tract, block group, or ZIP |
| `ranking_type` | string | No | "national" | "national" or "state" |
| `threshold` | int | No | - | Filter above this percentile/decile |
| `compare_to` | string | No | - | Geography for comparison |

---

## Data Sources (Embedded v2.0)

This skill reads from PopulationSim's embedded ADI data:

| Level | File | Records | Source |
|-------|------|---------|--------|
| Block Group | `data/block_group/adi_blockgroup_2023.csv` | 242,336 | UW-Madison Neighborhood Atlas |

### File Structure

| Column | Description | Values |
|--------|-------------|--------|
| FIPS | 12-digit block group FIPS | e.g., "482012104001" |
| ADI_NATRANK | National percentile ranking | 1-100 or suppression code |
| ADI_STATERNK | State decile ranking | 1-10 or suppression code |

### Suppression Codes

| Code | Meaning | Action |
|------|---------|--------|
| GQ | >33% group quarters population | Exclude from analysis |
| PH | Population <100 or <30 housing units | Exclude from analysis |
| GQ-PH | Both conditions | Exclude from analysis |
| QDI | Missing key demographic factor | Exclude from analysis |

### Data Lookup Pattern

```
1. Identify geography type:
   - Block group: direct lookup by 12-digit FIPS
   - Tract: aggregate block groups (first 11 digits match)
   - County: aggregate all block groups (first 5 digits match)
2. Read `data/block_group/adi_blockgroup_2023.csv`
3. Filter by FIPS prefix
4. Exclude suppressed values
5. Return rankings with Neighborhood Atlas source citation
```

### Data Vintage

- **Source**: UW-Madison Neighborhood Atlas
- **Version**: 2023 v4.0.1
- **Base Data**: 2019-2023 ACS 5-year estimates

---

## ADI Structure

### 17 Variables Across 4 Domains

**Income Domain (5 variables)**
| Variable | Definition |
|----------|------------|
| Median family income | Family income in past 12 months |
| Income disparity | Ratio of households earning <$10K to >$50K |
| Median home value | Value of owner-occupied units |
| Median gross rent | Gross rent for renter-occupied |
| Median monthly mortgage | Monthly mortgage costs |

**Education Domain (2 variables)**
| Variable | Definition |
|----------|------------|
| Less than 9 years education | Adults 25+ with < 9 years |
| High school diploma | Adults 25+ with HS diploma or higher |

**Employment Domain (1 variable)**
| Variable | Definition |
|----------|------------|
| Unemployment | Civilian labor force unemployed |

**Housing Quality Domain (9 variables)**
| Variable | Definition |
|----------|------------|
| Owner-occupied housing | % units owner-occupied |
| No complete plumbing | Units lacking complete plumbing |
| No telephone | Units without telephone service |
| Crowding | >1 person per room |
| And additional housing measures... |

### Scoring

| Ranking | Scale | Interpretation |
|---------|-------|----------------|
| **National Percentile** | 1-100 | 100 = most disadvantaged nationally |
| **State Decile** | 1-10 | 10 = most disadvantaged in state |

**Interpretation Guide**:
| National Percentile | State Decile | Disadvantage Level |
|---------------------|--------------|-------------------|
| 1-20 | 1-2 | Low |
| 21-40 | 3-4 | Low-Moderate |
| 41-60 | 5-6 | Moderate |
| 61-80 | 7-8 | Moderate-High |
| 81-100 | 9-10 | High |

---

## Output Schema

```json
{
  "analysis_type": "adi_analysis",
  "geography": {
    "type": "county",
    "fips": "39035",
    "name": "Cuyahoga County",
    "state": "OH",
    "block_group_count": 1248
  },
  "adi_summary": {
    "mean_national_percentile": 58,
    "median_national_percentile": 62,
    "mean_state_decile": 6.2,
    "interpretation": "moderate_high",
    "vs_state_mean": "+12 percentile points"
  },
  "distribution": {
    "by_national_percentile": {
      "1_20_low": { "block_groups": 186, "population": 148000 },
      "21_40_low_mod": { "block_groups": 224, "population": 179000 },
      "41_60_moderate": { "block_groups": 248, "population": 198000 },
      "61_80_mod_high": { "block_groups": 312, "population": 250000 },
      "81_100_high": { "block_groups": 278, "population": 222000 }
    },
    "by_state_decile": {
      "decile_1_2": { "block_groups": 162, "population": 130000 },
      "decile_3_4": { "block_groups": 198, "population": 158000 },
      "decile_5_6": { "block_groups": 286, "population": 229000 },
      "decile_7_8": { "block_groups": 324, "population": 259000 },
      "decile_9_10": { "block_groups": 278, "population": 222000 }
    }
  },
  "high_deprivation_areas": {
    "threshold": "national_percentile >= 80",
    "block_group_count": 278,
    "population": 222000,
    "pct_of_county": 0.223,
    "characteristics": {
      "mean_income": 28400,
      "poverty_rate": 0.342,
      "unemployment": 0.128,
      "no_hs_diploma": 0.224
    },
    "geographic_clusters": [
      { "area": "East Cleveland", "block_groups": 48, "mean_adi": 94 },
      { "area": "Central Cleveland", "block_groups": 62, "mean_adi": 91 },
      { "area": "Euclid", "block_groups": 34, "mean_adi": 88 }
    ]
  },
  "variable_detail": {
    "median_family_income": 62400,
    "income_disparity_ratio": 2.8,
    "pct_less_than_9_years_ed": 0.042,
    "pct_no_hs_diploma": 0.108,
    "unemployment_rate": 0.068,
    "pct_owner_occupied": 0.582,
    "pct_crowded": 0.024,
    "median_home_value": 142000,
    "median_rent": 892
  },
  "comparison": {
    "benchmark": "Ohio",
    "vs_state": {
      "mean_adi": { "county": 58, "state": 46, "diff": "+12" },
      "high_deprivation_pct": { "county": 0.223, "state": 0.142, "diff": "+8.1%" }
    }
  },
  "health_correlations": {
    "high_adi_health_outcomes": {
      "diabetes": 0.148,
      "hypertension": 0.382,
      "depression": 0.248,
      "fair_poor_health": 0.282
    },
    "low_adi_health_outcomes": {
      "diabetes": 0.082,
      "hypertension": 0.268,
      "depression": 0.162,
      "fair_poor_health": 0.118
    },
    "gradient": "Health outcomes worsen 28% from lowest to highest ADI quintile"
  },
  "cohort_implications": {
    "sdoh_profile_for_high_adi": {
      "income_barrier": 0.342,
      "education_barrier": 0.224,
      "housing_quality_issue": 0.086
    }
  },
  "metadata": {
    "adi_version": "ADI_2021",
    "data_source": "Neighborhood Atlas, UW Medicine",
    "generated_at": "2024-12-23T10:00:00Z"
  }
}
```

---

## Examples

### Example 1: County ADI Analysis

**Request**: "ADI analysis for Wayne County, Michigan"

**Response**:

**Wayne County, MI (Detroit Metro) ADI Analysis**

**Summary**:
- Mean National Percentile: 72 (Moderate-High)
- Median State Decile: 8 (High within Michigan)
- Block Groups: 1,842

**Distribution**:
| ADI Level | Block Groups | Population | % of County |
|-----------|--------------|------------|-------------|
| Low (1-20) | 142 | 114,000 | 7.7% |
| Low-Mod (21-40) | 186 | 149,000 | 10.1% |
| Moderate (41-60) | 312 | 250,000 | 16.9% |
| Mod-High (61-80) | 486 | 389,000 | 26.4% |
| High (81-100) | 716 | 573,000 | **38.9%** ⚠️ |

**Highly Deprived Areas** (ADI ≥ 80):
| Area | Block Groups | Mean ADI | Key Factors |
|------|--------------|----------|-------------|
| Detroit Downtown | 124 | 94 | Income $18K, Poverty 48% |
| East Detroit | 186 | 92 | Unemployment 18%, No HS 28% |
| Highland Park | 42 | 96 | Income $16K, Vacant housing 38% |
| Inkster | 38 | 89 | Poverty 38%, Owner-occupied 42% |

**Health Correlation**:
| Metric | High ADI | Low ADI | Gap |
|--------|----------|---------|-----|
| Diabetes | 16.8% | 7.2% | +9.6% |
| Heart Disease | 8.4% | 4.2% | +4.2% |
| Life Expectancy | 71.2 yrs | 82.4 yrs | -11.2 yrs |

---

### Example 2: State Comparison

**Request**: "Compare ADI profiles: Mississippi vs Minnesota"

**Response**:

**State ADI Comparison: MS vs MN**

| Metric | Mississippi | Minnesota | Gap |
|--------|-------------|-----------|-----|
| Mean National ADI | 74 | 38 | +36 ⚠️ |
| High-ADI Block Groups | 52% | 12% | +40% |
| Low-ADI Block Groups | 8% | 42% | -34% |

**ADI Distribution**:

*Mississippi*:
| Percentile | % of State |
|------------|------------|
| 1-20 | 8% |
| 21-40 | 12% |
| 41-60 | 18% |
| 61-80 | 28% |
| 81-100 | 34% ⚠️ |

*Minnesota*:
| Percentile | % of State |
|------------|------------|
| 1-20 | 42% |
| 21-40 | 28% |
| 41-60 | 18% |
| 61-80 | 8% |
| 81-100 | 4% |

**Underlying Factors**:
| Factor | Mississippi | Minnesota |
|--------|-------------|-----------|
| Median Income | $46,511 | $77,720 |
| Poverty Rate | 19.4% | 9.1% |
| No HS Diploma | 14.2% | 6.8% |
| Unemployment | 6.2% | 3.1% |

---

### Example 3: Block Group Detail

**Request**: "Most deprived block groups in Chicago"

**Response**:

**Chicago High-Deprivation Block Groups (ADI ≥ 90)**

**Summary**: 284 block groups with ADI ≥ 90

**Top 10 Most Deprived**:
| Block Group | ADI | Population | Median Income | Poverty |
|-------------|-----|------------|---------------|---------|
| 170318381001 | 100 | 1,842 | $12,400 | 62% |
| 170318382002 | 100 | 2,124 | $14,200 | 58% |
| 170316801001 | 99 | 1,568 | $15,800 | 54% |
| 170316802003 | 99 | 1,924 | $16,200 | 52% |
| 170318401002 | 98 | 2,248 | $17,400 | 48% |

**Geographic Concentration**:
| Community Area | Block Groups | Mean ADI |
|----------------|--------------|----------|
| Englewood | 42 | 96 |
| West Englewood | 38 | 95 |
| Austin | 52 | 92 |
| North Lawndale | 34 | 94 |
| Roseland | 28 | 91 |

**vs Low-ADI Areas** (Lincoln Park, Lake View):
| Metric | High-ADI Areas | Low-ADI Areas |
|--------|----------------|---------------|
| Life Expectancy | 68.2 years | 84.6 years |
| Infant Mortality | 14.2/1000 | 3.8/1000 |
| Diabetes | 18.4% | 6.2% |

---

## ADI vs SVI Comparison

| Aspect | ADI | SVI |
|--------|-----|-----|
| **Geography** | Block group | Census tract |
| **Granularity** | ~600-3,000 pop | ~1,200-8,000 pop |
| **Focus** | Socioeconomic deprivation | Social vulnerability (broader) |
| **Rankings** | National percentile + State decile | National percentile |
| **Variables** | 17 (income, education, housing) | 16 (4 themes) |
| **Best For** | Neighborhood targeting | Disaster preparedness, broad SDOH |

**When to Use ADI**:
- Need block group granularity
- Focus on socioeconomic deprivation specifically
- Within-state comparisons (state decile useful)
- Correlating with health outcomes

**When to Use SVI**:
- Broader social vulnerability assessment
- Disaster/emergency planning
- Need the 4-theme breakdown
- Tract-level analysis sufficient

---

## Validation Rules

### Input Validation
- Geography must be valid
- Ranking type must be "national" or "state"
- Threshold: 1-100 for national, 1-10 for state

### Output Validation
- [ ] National percentile 1-100
- [ ] State decile 1-10
- [ ] Block group counts match geography
- [ ] Income/poverty values reasonable

---

## Related Skills

- [svi-analysis.md](svi-analysis.md) - Social Vulnerability Index
- [economic-indicators.md](economic-indicators.md) - Income detail
- [census-tract-analysis.md](../geographic/census-tract-analysis.md) - Geographic analysis
- [health-outcome-disparities.md](../health-patterns/health-outcome-disparities.md) - Health correlations
