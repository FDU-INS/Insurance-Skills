---
name: health-outcome-disparities
description: >
  Analyze health disparities by race, ethnicity, age, income, and geography.
  Use for health equity assessment, disparity quantification, and diversity
  planning. Triggers: "disparities", "by race", "health equity", "inequities",
  "compare outcomes by [demographic]", "disparity analysis".
---

# Health Outcome Disparities Skill

## Overview

The health-outcome-disparities skill analyzes differences in health outcomes across demographic groups and geographic areas, quantifying disparities and identifying contributing factors. This supports health equity assessment, disparity-focused interventions, and diversity planning for clinical trials.

**Primary Use Cases**:
- Health equity assessment
- Disparity quantification by demographic group
- Identifying disparity hotspots
- Clinical trial diversity planning
- SDOH-health outcome linkage
- Targeted intervention planning

---

## Trigger Phrases

- "Show health disparities by race in [geography]"
- "Compare diabetes rates by ethnicity"
- "Health equity analysis for [area]"
- "Racial disparities in [condition]"
- "Income-based health disparities"
- "Which groups have worst outcomes for [condition]?"
- "Disparity gap for [condition] in [geography]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, tract, metro, or state |
| `condition` | string | No | "all" | Specific condition or "all" |
| `stratify_by` | string | No | "race_ethnicity" | "race_ethnicity", "income", "education", "age", "geography" |
| `compare_groups` | array | No | all groups | Specific groups to compare |
| `include_drivers` | boolean | No | true | Include disparity drivers |

---

## Data Sources (Embedded v2.0)

Disparity analysis uses embedded data with geographic stratification:

| Data Type | File | Key Columns |
|-----------|------|-------------|
| Health Outcomes | `data/county/places_county_2024.csv` | [CONDITION]_CrudePrev |
| Demographics | `data/tract/svi_tract_2022.csv` | EP_MINRTY, E_AFAM, E_HISP, E_ASIAN |
| SVI by Theme | `data/tract/svi_tract_2022.csv` | RPL_THEME3 (Minority/Language) |
| Socioeconomic | `data/tract/svi_tract_2022.csv` | EP_POV150, EP_NOHSDP |

### Disparity Analysis Pattern

```
1. Identify high-minority vs low-minority tracts using EP_MINRTY
2. Compare health outcomes between tract groups
3. Calculate disparity ratios and absolute differences
4. Correlate with SVI themes to identify drivers
5. Return with source citations
```

**Note**: Race-specific health data requires BRFSS microdata or stratified estimates not in embedded package. Use SVI demographic composition as proxy for geographic disparity analysis.

---

## Disparity Dimensions

### Race/Ethnicity Categories

| Group | Census Code | Typical Health Patterns |
|-------|-------------|------------------------|
| White Non-Hispanic | WNH | Baseline for many comparisons |
| Black/African American | BAA | Higher CHD, stroke, HTN, diabetes |
| Hispanic/Latino | HIS | Higher diabetes, lower cancer |
| Asian | ASN | Lower obesity, varied by subgroup |
| American Indian/Alaska Native | AIAN | Highest diabetes, substance use |
| Native Hawaiian/Pacific Islander | NHPI | High obesity, diabetes |
| Two or More Races | TMR | Varies |

### Key Disparity Patterns (National)

| Condition | Highest Rate Group | Lowest Rate Group | Gap |
|-----------|-------------------|-------------------|-----|
| Diabetes | AIAN (14.8%) | Asian (9.2%) | 5.6% |
| Heart Disease | Black (6.8%) | Hispanic (4.2%) | 2.6% |
| Stroke | Black (4.2%) | Asian (2.4%) | 1.8% |
| Hypertension | Black (42.2%) | Asian (28.4%) | 13.8% |
| Obesity | Black (38.4%) | Asian (12.8%) | 25.6% |

---

## Output Schema

```json
{
  "analysis_type": "health_disparities",
  "geography": {
    "type": "county",
    "fips": "13121",
    "name": "Fulton County",
    "state": "GA"
  },
  "stratification": "race_ethnicity",
  "condition_analyzed": "diabetes",
  "population_demographics": {
    "total": 1066710,
    "white_nh": 0.384,
    "black": 0.432,
    "hispanic": 0.088,
    "asian": 0.068
  },
  "disparities": {
    "by_group": [
      {
        "group": "Black",
        "prevalence": 0.142,
        "vs_white_nh": {
          "absolute_diff": 0.048,
          "relative_ratio": 1.51,
          "interpretation": "51% higher than White NH"
        },
        "population_affected": 65200
      },
      {
        "group": "Hispanic",
        "prevalence": 0.118,
        "vs_white_nh": {
          "absolute_diff": 0.024,
          "relative_ratio": 1.26,
          "interpretation": "26% higher than White NH"
        },
        "population_affected": 11100
      },
      {
        "group": "White NH",
        "prevalence": 0.094,
        "vs_white_nh": {
          "absolute_diff": 0,
          "relative_ratio": 1.0,
          "interpretation": "Reference group"
        },
        "population_affected": 38500
      },
      {
        "group": "Asian",
        "prevalence": 0.088,
        "vs_white_nh": {
          "absolute_diff": -0.006,
          "relative_ratio": 0.94,
          "interpretation": "6% lower than White NH"
        },
        "population_affected": 6400
      }
    ],
    "disparity_summary": {
      "highest_rate_group": "Black",
      "lowest_rate_group": "Asian",
      "max_gap_absolute": 0.054,
      "max_gap_relative": 1.61,
      "disparity_index": 0.42
    }
  },
  "disparity_drivers": {
    "socioeconomic": {
      "poverty_rate_by_group": {
        "Black": 0.182,
        "Hispanic": 0.168,
        "White NH": 0.078,
        "Asian": 0.092
      },
      "correlation_poverty_diabetes": 0.68
    },
    "access_factors": {
      "uninsured_by_group": {
        "Black": 0.108,
        "Hispanic": 0.188,
        "White NH": 0.052,
        "Asian": 0.068
      }
    },
    "behavioral_factors": {
      "obesity_by_group": {
        "Black": 0.382,
        "Hispanic": 0.324,
        "White NH": 0.278,
        "Asian": 0.142
      },
      "correlation_obesity_diabetes": 0.72
    },
    "geographic_concentration": {
      "black_high_svi_pct": 0.68,
      "white_high_svi_pct": 0.12
    }
  },
  "equity_implications": {
    "priority_groups": ["Black", "Hispanic"],
    "intervention_focus": [
      "Diabetes prevention in Black communities",
      "Insurance coverage for Hispanic population",
      "Target high-SVI census tracts"
    ],
    "trial_diversity_note": "Diabetes trials should over-sample Black (51% higher rate) and Hispanic populations"
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "data_sources": ["CDC_PLACES_2024", "ACS_2022", "CDC_SVI_2022"],
    "methodology": "Age-adjusted rates, CDC race/ethnicity categories"
  }
}
```

---

## Examples

### Example 1: Racial Disparities in Diabetes

**Request**: "Analyze diabetes disparities by race in Atlanta metro"

**Response**:

**Atlanta Metro Diabetes Disparities by Race/Ethnicity**

| Group | Diabetes Rate | vs White NH | Population |
|-------|---------------|-------------|------------|
| Black | 14.2% | +52% ⚠️ | 2,012,000 |
| Hispanic | 11.8% | +26% | 724,000 |
| White NH | 9.4% | Reference | 2,845,000 |
| Asian | 9.2% | -2% | 418,000 |

**Disparity Magnitude**:
- Black-White gap: 4.8 percentage points
- Relative risk: Black adults 1.52x more likely to have diabetes

**Contributing Factors**:

| Factor | Black | White NH | Gap |
|--------|-------|----------|-----|
| Obesity | 38.2% | 27.8% | +10.4% |
| Physical Inactivity | 28.4% | 18.2% | +10.2% |
| Poverty Rate | 18.2% | 7.8% | +10.4% |
| Food Insecurity | 22.4% | 8.2% | +14.2% |
| High-SVI Residence | 68% | 12% | +56% |

**Geographic Pattern**:
- Highest Black diabetes: South Fulton, Clayton, DeKalb
- Overlap with high-SVI areas: 94% correlation

**HealthSim Implications**:
- When generating Atlanta diabetics, use racial distribution weighted by prevalence
- Include SDOH Z-codes at higher rates for Black patients
- Expect higher comorbidity rates in Black diabetic cohorts

---

### Example 2: Income-Based Disparities

**Request**: "Health disparities by income in California"

**Response**:

**California Health Disparities by Income Level**

**Income Categories** (% of FPL):
- < 100% FPL: Poor
- 100-200% FPL: Near-poor
- 200-400% FPL: Middle income
- > 400% FPL: Higher income

**Chronic Condition Rates**:

| Condition | Poor | Near-Poor | Middle | Higher | Gap |
|-----------|------|-----------|--------|--------|-----|
| Diabetes | 14.2% | 11.8% | 9.4% | 6.8% | 7.4% |
| Obesity | 38.4% | 34.2% | 28.4% | 22.1% | 16.3% |
| Depression | 28.4% | 22.8% | 18.2% | 14.8% | 13.6% |
| Fair/Poor Health | 32.4% | 22.8% | 14.2% | 8.4% | 24.0% |

**Healthcare Access**:

| Measure | Poor | Near-Poor | Middle | Higher |
|---------|------|-----------|--------|--------|
| Uninsured | 18.4% | 12.8% | 6.4% | 3.2% |
| No PCP | 32.4% | 24.8% | 14.2% | 8.4% |
| No Checkup | 38.2% | 28.4% | 22.1% | 18.4% |

**Gradient Analysis**:
- Diabetes increases 2.1x from highest to lowest income
- Fair/poor health increases 3.9x
- Strong linear gradient across all conditions

---

### Example 3: Geographic Disparity Hotspots

**Request**: "Find diabetes disparity hotspots in Texas"

**Response**:

**Texas Diabetes Disparity Hotspots**

**Methodology**: Census tracts where Black or Hispanic diabetes rate exceeds White NH rate by > 5 percentage points

**Hotspot Summary**:
- Total hotspot tracts: 842 (12% of TX tracts)
- Population in hotspots: 3.2 million
- Geographic concentration: Border, South Texas, urban cores

**Regional Analysis**:

| Region | Hotspot Tracts | Gap Magnitude | Primary Group |
|--------|----------------|---------------|---------------|
| Rio Grande Valley | 312 | 6.8% | Hispanic |
| Houston Inner City | 186 | 5.8% | Black |
| Dallas South | 124 | 5.4% | Black |
| San Antonio South | 98 | 5.2% | Hispanic |
| El Paso | 72 | 4.8% | Hispanic |

**Hotspot Characteristics**:
| Metric | Hotspot Tracts | Non-Hotspot |
|--------|----------------|-------------|
| Mean SVI | 0.82 | 0.38 |
| Poverty Rate | 28.4% | 12.8% |
| Uninsured | 22.4% | 11.2% |
| Obesity | 38.2% | 28.4% |
| No PCP | 34.2% | 18.4% |

**Intervention Priority Rankings**:
1. Rio Grande Valley - Largest population, largest gap
2. Houston 5th Ward/3rd Ward - Extreme poverty overlay
3. Dallas Fair Park/South Dallas - High SDOH burden

---

## Validation Rules

### Input Validation
- Geography must be valid
- Stratification variable must be valid
- Groups must exist in data

### Output Validation
- [ ] All group rates between 0 and 1
- [ ] Reference group identified
- [ ] Relative ratios calculated correctly
- [ ] Population numbers sum correctly

### Statistical Notes
- Small populations may have unreliable subgroup estimates
- Some Asian subgroups have very different patterns
- Hispanic includes diverse subpopulations

---

## Related Skills

- [chronic-disease-prevalence.md](chronic-disease-prevalence.md) - Disease rates
- [svi-analysis.md](../sdoh/svi-analysis.md) - SDOH context
- [diversity-planning.md](../trial-support/diversity-planning.md) - Trial diversity
- [census-tract-analysis.md](../geographic/census-tract-analysis.md) - Tract hotspots
- [cohort-specification.md](../cohorts/cohort-specification.md) - Diverse cohorts
