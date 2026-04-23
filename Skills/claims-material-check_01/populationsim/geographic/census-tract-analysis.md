---
name: census-tract-analysis
description: >
  Analyze census tracts for granular neighborhood-level population intelligence.
  Use for identifying health hotspots, vulnerable areas, SDOH concentrations,
  and targeted intervention planning. Triggers: "tract level", "census tracts",
  "hotspots", "vulnerable tracts", "neighborhood analysis", "granular analysis".
---

# Census Tract Analysis Skill

## Overview

The census-tract-analysis skill provides granular neighborhood-level population intelligence by analyzing census tracts (~4,000 population each). This enables identification of health hotspots, vulnerable communities, and SDOH concentrations that county-level analysis would miss.

**Primary Use Cases**:
- Identify high-vulnerability neighborhoods
- Target community health interventions
- Find health disparity hotspots
- Support FQHC service area analysis
- Enable precise cohort targeting

**Key Advantage**: Census tracts reveal within-county variation that aggregate county data masks.

---

## Trigger Phrases

- "Find vulnerable tracts in [county/area]"
- "Analyze census tracts in [geography]"
- "Show me high-SVI tracts"
- "Identify diabetes hotspots in [county]"
- "Tract-level analysis for [area]"
- "Neighborhood health analysis"
- "Which tracts have the highest [condition/metric]?"
- "Granular SDOH analysis for [county]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, state, or list of tracts to analyze |
| `filter` | object | No | none | Criteria to filter tracts |
| `filter.svi_min` | float | No | - | Minimum SVI threshold (0-1) |
| `filter.condition` | string | No | - | Health condition to focus on |
| `filter.population_min` | int | No | 500 | Minimum tract population |
| `sort_by` | string | No | "svi_overall" | Metric to rank by |
| `limit` | int | No | 20 | Maximum tracts to return |
| `include_adjacent` | boolean | No | false | Include neighboring tracts |
| `output_format` | string | No | "summary" | "summary", "detailed", "map_ready" |

---

## Data Sources (Embedded v2.0)

This skill reads from PopulationSim's embedded tract-level data:

| Data Type | File | Records | Key Columns |
|-----------|------|---------|-------------|
| Health Indicators | `data/tract/places_tract_2024.csv` | 83,522 | LocationID, [MEASURE]_CrudePrev |
| SVI Full Dataset | `data/tract/svi_tract_2022.csv` | 84,120 | FIPS, RPL_THEMES, E_TOTPOP, EP_* |
| ADI Rankings | `data/block_group/adi_blockgroup_2023.csv` | 242,336 | FIPS (12-digit), ADI_NATRANK |

### Key Column Reference

**CDC PLACES Tract Columns:**
- LocationID: 11-digit tract FIPS
- StateAbbr, CountyName: Geography identifiers
- [MEASURE]_CrudePrev: Crude prevalence (e.g., DIABETES_CrudePrev)
- TotalPopulation: Tract population 18+

**SVI Tract Columns:**
- FIPS: 11-digit tract FIPS
- STCNTY: 5-digit county FIPS (for filtering)
- E_TOTPOP: Total population
- RPL_THEMES: Overall SVI (0-1, higher = more vulnerable)
- RPL_THEME1-4: Theme-specific rankings
- EP_POV150, EP_UNINSUR, EP_MINRTY: Key percentages

### Tract FIPS Structure
```
11 digits: [State-2][County-3][Tract-6]
Example: 48201311500
  48 = Texas
  201 = Harris County
  311500 = Tract 3115.00
```

---

## Generation Patterns

### Pattern 1: High-Vulnerability Tract Identification

**Input**: "Find high-SVI tracts in Harris County, TX"

**Process**:
1. **Read SVI tract data:**
   - Read `data/tract/svi_tract_2022.csv`
   - Filter: STCNTY = "48201" (Harris County)
2. **Apply SVI filter:**
   - Filter: RPL_THEMES >= 0.75
3. **Sort and limit:**
   - Sort by RPL_THEMES descending
   - Return top 20 tracts
4. **Format with provenance**

**Output**: 
```
Harris County High-Vulnerability Tracts (SVI ≥ 0.75)

| Tract FIPS | SVI | Population | Poverty | Minority |
|------------|-----|------------|---------|----------|
| 48201311500 | 0.98 | 4,521 | 52.3% | 94.2% |
| 48201311600 | 0.96 | 3,892 | 48.7% | 91.8% |
| ... | ... | ... | ... | ... |

Found 187 high-vulnerability tracts in Harris County (24% of 786 total tracts)

*Source: CDC/ATSDR SVI 2022*
```

### Pattern 2: Disease Hotspot Detection

**Input**: "Identify diabetes hotspots in Harris County"

**Process**:
1. **Read PLACES tract data:**
   - Read `data/tract/places_tract_2024.csv`
   - Filter: CountyFIPS = "48201"
2. **Calculate statistics:**
   - County mean diabetes prevalence
   - Standard deviation across tracts
3. **Identify hotspots:**
   - Tracts where DIABETES_CrudePrev > mean + 1.5*SD
4. **Cross-reference with SVI for context**

**Output**: Diabetes hotspot clusters with demographics

### Pattern 3: Disparity Analysis

**Input**: "Compare tract-level diabetes rates by SVI quartile in Cook County"

**Process**:
1. Load all Cook County tracts
2. Assign SVI quartile to each tract
3. Calculate mean diabetes prevalence by quartile
4. Calculate gradient and significance
5. Identify exemplar tracts

**Output**: Disparity gradient with tract examples

---

## Output Schema

### Tract Summary Output

```json
{
  "analysis_type": "vulnerability_identification",
  "geography_scope": {
    "type": "county",
    "fips": "06037",
    "name": "Los Angeles County",
    "state": "CA",
    "total_tracts": 2493
  },
  "filter_applied": {
    "svi_min": 0.75,
    "population_min": 500
  },
  "results_summary": {
    "tracts_matching": 623,
    "pct_of_total": 0.250,
    "total_population": 2834521,
    "aggregate_profile": {
      "mean_svi": 0.84,
      "median_income": 42850,
      "mean_diabetes": 0.142,
      "mean_uninsured": 0.182
    }
  },
  "top_tracts": [
    {
      "tract_fips": "06037534302",
      "tract_name": "Census Tract 5343.02",
      "population": 4521,
      "svi_overall": 0.98,
      "svi_themes": {
        "socioeconomic": 0.96,
        "household_composition": 0.92,
        "minority_language": 0.99,
        "housing_transportation": 0.94
      },
      "demographics": {
        "median_age": 28.4,
        "median_income": 32450,
        "poverty_rate": 0.342,
        "race_ethnicity": {
          "hispanic": 0.92,
          "white_nh": 0.03
        }
      },
      "health_indicators": {
        "diabetes": 0.168,
        "obesity": 0.382,
        "uninsured": 0.248
      },
      "notable_factors": [
        "Very high SVI (98th percentile)",
        "High poverty (34.2%)",
        "Limited English proficiency area",
        "Low vehicle access"
      ]
    }
  ],
  "geographic_clustering": {
    "clusters_identified": 8,
    "largest_cluster": {
      "tract_count": 42,
      "centroid_tract": "06037534302",
      "neighborhood_name": "South Los Angeles",
      "combined_population": 178432
    }
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "data_vintage": {
      "census": "ACS_2022_5yr",
      "health": "CDC_PLACES_2024",
      "svi": "CDC_SVI_2022"
    }
  }
}
```

### Hotspot Detection Output

```json
{
  "analysis_type": "disease_hotspot",
  "condition": "diabetes",
  "geography_scope": {
    "counties": ["48201", "48157", "48339"],
    "county_names": ["Harris", "Fort Bend", "Montgomery"],
    "total_tracts": 1124
  },
  "baseline": {
    "region_mean": 0.118,
    "region_std": 0.032,
    "hotspot_threshold": 0.166
  },
  "hotspots": {
    "tract_count": 87,
    "pct_of_total": 0.077,
    "total_population": 342156,
    "clusters": [
      {
        "cluster_id": 1,
        "tract_count": 23,
        "mean_prevalence": 0.182,
        "z_score": 2.0,
        "geography": "Northeast Houston",
        "population": 94521,
        "demographics": {
          "mean_age": 38.2,
          "pct_65_plus": 0.142,
          "hispanic": 0.68,
          "black": 0.24
        },
        "contributing_factors": [
          "High obesity (38.4%)",
          "Low physical activity (32.1%)",
          "Food desert overlap (78% of tracts)",
          "High SVI (mean 0.82)"
        ],
        "tracts": ["48201311400", "48201311500", "48201311600"]
      }
    ]
  }
}
```

---

## Examples

### Example 1: Vulnerability Analysis

**Request**: "Find the most vulnerable census tracts in Miami-Dade County"

**Response**:

**Miami-Dade County Vulnerability Analysis**

**Scope**: 519 census tracts analyzed

**High-Vulnerability Tracts (SVI ≥ 0.80)**: 127 tracts (24.5%)

| Rank | Tract | Population | SVI | Key Vulnerabilities |
|------|-------|------------|-----|---------------------|
| 1 | 12086000701 | 3,842 | 0.98 | Poverty 48%, No vehicle 42%, Limited English 61% |
| 2 | 12086001003 | 4,215 | 0.97 | Poverty 42%, Single parent 38%, No HS diploma 45% |
| 3 | 12086001102 | 3,521 | 0.96 | Poverty 39%, Disability 22%, Housing cost burden 68% |

**Geographic Clusters**:
1. **Little Haiti/Liberty City** (32 tracts): Mean SVI 0.89, population 128,450
2. **Overtown/Allapattah** (24 tracts): Mean SVI 0.87, population 96,200
3. **Homestead/Florida City** (18 tracts): Mean SVI 0.85, population 72,300

**Aggregate Health Profile** (high-SVI tracts):
| Metric | High-SVI Tracts | County Average | Gap |
|--------|-----------------|----------------|-----|
| Diabetes | 14.8% | 10.2% | +4.6% |
| Obesity | 35.2% | 28.4% | +6.8% |
| Uninsured | 22.4% | 14.8% | +7.6% |
| No Checkup | 28.1% | 21.2% | +6.9% |

---

### Example 2: Hotspot Detection

**Request**: "Identify heart disease hotspots in Philadelphia"

**Response**:

**Philadelphia Heart Disease Hotspot Analysis**

**Baseline**: City-wide CHD prevalence = 6.2%
**Hotspot Threshold**: > 8.5% (1.5 SD above mean)

**Hotspots Identified**: 34 tracts (8.9% of city tracts)

**Cluster 1: North Philadelphia** (18 tracts)
- Mean CHD: 9.8%
- Population: 68,240
- Demographics: 82% Black, median age 42.1
- Risk factors: Smoking 28%, HTN 42%, Diabetes 18%
- SVI: 0.91 (very high)

**Cluster 2: West Philadelphia** (11 tracts)
- Mean CHD: 9.2%
- Population: 44,850
- Demographics: 76% Black, median age 38.4
- Risk factors: Smoking 24%, HTN 38%, Obesity 42%
- SVI: 0.84 (high)

**Cluster 3: Southwest** (5 tracts)
- Mean CHD: 8.8%
- Population: 21,200
- Demographics: 68% Black, 22% White NH
- Risk factors: Smoking 22%, Physical inactivity 34%
- SVI: 0.78 (moderate-high)

**Common Characteristics Across Hotspots**:
- Age 65+ population > 18%
- Smoking prevalence > 20%
- Hypertension > 35%
- SVI > 0.75

---

### Example 3: Disparity Gradient

**Request**: "Show how diabetes varies by SVI quartile in Dallas County"

**Response**:

**Dallas County: Diabetes Prevalence by SVI Quartile**

| SVI Quartile | Tracts | Population | Mean Diabetes | vs Q1 |
|--------------|--------|------------|---------------|-------|
| Q1 (0.00-0.25) | 134 | 542,180 | 8.2% | - |
| Q2 (0.25-0.50) | 131 | 498,420 | 10.4% | +2.2% |
| Q3 (0.50-0.75) | 128 | 512,850 | 12.8% | +4.6% |
| Q4 (0.75-1.00) | 132 | 486,220 | 15.4% | **+7.2%** |

**Gradient**: +2.4% per quartile increase (p < 0.001)

**Q4 (High Vulnerability) Characteristics**:
- Mean household income: $38,450 (vs $112,800 in Q1)
- Uninsured rate: 24.8% (vs 6.2% in Q1)
- Obesity rate: 38.2% (vs 24.1% in Q1)
- No annual checkup: 31.4% (vs 18.2% in Q1)

**Exemplar Tracts**:

*Lowest Vulnerability, Lowest Diabetes (Q1)*:
- Tract 48113014814 (Highland Park): SVI 0.02, Diabetes 5.8%
- Income $248,500, 99% insured

*Highest Vulnerability, Highest Diabetes (Q4)*:
- Tract 48113003100 (South Dallas): SVI 0.98, Diabetes 18.2%
- Income $24,200, 68% insured

---

## Validation Rules

### Input Validation
- Geography must resolve to valid county or tract list
- SVI thresholds must be between 0 and 1
- Population minimums must be positive integers

### Output Validation
- [ ] Tract FIPS codes are valid 11-digit format
- [ ] SVI values between 0 and 1
- [ ] Percentages between 0 and 1
- [ ] Population values are positive integers
- [ ] Tracts sum to expected county totals

### Data Quality Notes
- Tracts with population < 500 have less reliable estimates
- ACS 5-year estimates required for tract-level data
- CDC PLACES tract data may have higher MOE for small tracts
- SVI not available for tracts with missing ACS data

---

## Related Skills

- [county-profile.md](county-profile.md) - County-level aggregate profiles
- [svi-analysis.md](../sdoh/svi-analysis.md) - Deep dive into SVI themes
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Disease analysis
- [health-outcome-disparities.md](../health-patterns/health-outcome-disparities.md) - Disparity analysis
- [cohort-specification.md](../cohorts/cohort-specification.md) - Define cohorts from tract analysis

---

## Data Sources

| Data Element | Source | Vintage | Notes |
|--------------|--------|---------|-------|
| Demographics | Census ACS 5-year | 2022 | Required for tract level |
| Health Indicators | CDC PLACES | 2024 | Available for most tracts |
| SVI | CDC/ATSDR | 2022 | All populated tracts |
| Tract Boundaries | TIGER/Line | 2022 | For mapping/adjacency |
