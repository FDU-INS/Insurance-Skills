---
name: health-behavior-patterns
description: >
  Analyze health behaviors and risk factors using CDC PLACES data. Use for
  understanding modifiable risk factors like smoking, obesity, physical
  inactivity, and sleep patterns. Triggers: "smoking rate", "obesity",
  "physical activity", "health behaviors", "risk factors", "lifestyle factors".
---

# Health Behavior Patterns Skill

## Overview

The health-behavior-patterns skill analyzes modifiable health risk behaviors across geographic areas using CDC PLACES data. This enables understanding of lifestyle factors that drive chronic disease burden and informs prevention opportunities.

**Primary Use Cases**:
- Risk factor assessment for population health
- Prevention program targeting
- Understanding disease drivers
- Behavioral health intervention planning
- Cohort SDOH profile development

---

## Trigger Phrases

- "What's the smoking rate in [geography]?"
- "Compare obesity rates between [A] and [B]"
- "Physical activity patterns in [region]"
- "Health behaviors for [geography]"
- "Risk factor profile for [area]"
- "Which counties have highest [behavior]?"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, tract, metro, or state |
| `behavior` | string | No | "all" | Specific behavior or "all" |
| `compare_to` | string | No | - | Geography for comparison |
| `correlate_with` | string | No | - | Condition to correlate |
| `benchmark` | string | No | "national" | Comparison benchmark |

---

## Data Sources (Embedded v2.0)

Health behavior data comes from CDC PLACES in the embedded data package:

| Level | File | Key Columns |
|-------|------|-------------|
| County | `data/county/places_county_2024.csv` | CSMOKING_CrudePrev, OBESITY_CrudePrev, LPA_CrudePrev, BINGE_CrudePrev, SLEEP_CrudePrev |
| Tract | `data/tract/places_tract_2024.csv` | Same columns as county |

### Data Lookup Pattern

```
1. Identify geography (county FIPS or tract FIPS)
2. Read appropriate PLACES file
3. Filter by CountyFIPS or LocationID
4. Extract behavior columns ([BEHAVIOR]_CrudePrev)
5. Compare to national averages
6. Return with CDC PLACES 2024 source citation
```

---

## Available Behaviors

### CDC PLACES Health Behaviors

| Behavior | Variable | Definition | National Rate |
|----------|----------|------------|---------------|
| Current Smoking | CSMOKING | Adults who currently smoke | 14.1% |
| Obesity | OBESITY | BMI ≥ 30 | 32.1% |
| Physical Inactivity | LPA | No leisure physical activity | 22.8% |
| Binge Drinking | BINGE | Binge drinking past 30 days | 16.8% |
| Short Sleep | SLEEP | Sleep < 7 hours | 35.2% |

### Correlation with Chronic Conditions

| Behavior | Diabetes | CHD | COPD | Depression |
|----------|----------|-----|------|------------|
| Smoking | 0.32 | 0.58 | 0.72 | 0.48 |
| Obesity | 0.72 | 0.48 | 0.28 | 0.38 |
| Inactivity | 0.54 | 0.42 | 0.38 | 0.45 |
| Short Sleep | 0.42 | 0.38 | 0.32 | 0.52 |

---

## Output Schema

```json
{
  "analysis_type": "health_behavior_patterns",
  "geography": {
    "type": "county",
    "fips": "21111",
    "name": "Jefferson County",
    "state": "KY"
  },
  "behaviors": {
    "smoking": {
      "rate": 0.218,
      "vs_state": 0.224,
      "vs_national": 0.141,
      "status": "significantly_above",
      "population_affected": 124000,
      "trend": "decreasing"
    },
    "obesity": {
      "rate": 0.342,
      "vs_state": 0.348,
      "vs_national": 0.321,
      "status": "above",
      "population_affected": 195000
    },
    "physical_inactivity": {
      "rate": 0.268,
      "vs_state": 0.282,
      "vs_national": 0.228,
      "status": "above"
    },
    "binge_drinking": {
      "rate": 0.172,
      "vs_state": 0.168,
      "vs_national": 0.168,
      "status": "similar"
    },
    "short_sleep": {
      "rate": 0.382,
      "vs_state": 0.392,
      "vs_national": 0.352,
      "status": "above"
    }
  },
  "disease_correlations": {
    "smoking_related": {
      "copd_rate": 0.088,
      "lung_cancer_rate": 0.018,
      "chd_rate": 0.068
    },
    "obesity_related": {
      "diabetes_rate": 0.128,
      "hypertension_rate": 0.358
    }
  },
  "demographic_patterns": {
    "smoking_by_education": {
      "no_hs_diploma": 0.32,
      "hs_graduate": 0.24,
      "some_college": 0.18,
      "bachelors_plus": 0.08
    },
    "obesity_by_income": {
      "below_poverty": 0.42,
      "near_poverty": 0.38,
      "above_median": 0.28
    }
  },
  "prevention_opportunities": {
    "primary": "Smoking cessation programs - 7.7% excess vs national",
    "secondary": "Physical activity promotion - 4.0% excess",
    "target_populations": ["Low education", "Low income", "Rural areas"]
  }
}
```

---

## Examples

### Example 1: Smoking Analysis

**Request**: "Analyze smoking patterns in Kentucky"

**Response**:

**Kentucky Smoking Analysis**

**Current Smoking Rate**: 22.4% (vs 14.1% national) ⚠️ Highest in US

**Trend**: Decreasing (-4.2% since 2015, but still 58% above national)

**County Variation**:
| Category | Rate Range | Counties |
|----------|------------|----------|
| Highest | 28-32% | Owsley, McCreary, Clay |
| Moderate | 20-24% | Most rural counties |
| Lowest | 12-16% | Fayette, Oldham, Boone |

**Demographic Patterns**:
| Group | Smoking Rate |
|-------|--------------|
| No HS Diploma | 38.2% |
| HS Graduate | 28.4% |
| Some College | 22.1% |
| Bachelor's+ | 9.8% |

**Health Impact**:
| Condition | KY Rate | National | Excess |
|-----------|---------|----------|--------|
| COPD | 10.8% | 6.2% | +74% |
| Lung Cancer Mortality | 72/100K | 38/100K | +89% |
| CHD | 7.4% | 5.4% | +37% |

**Prevention Implications**:
- Priority target: Low-education populations
- Geographic focus: Eastern Kentucky
- Intervention: Tobacco cessation + economic support

---

### Example 2: Obesity Comparison

**Request**: "Compare obesity: Southern states vs Western states"

**Response**:

**Regional Obesity Comparison**

| Region | Mean Obesity | Range |
|--------|--------------|-------|
| South | 35.4% | 29.2-39.8% |
| West | 27.8% | 23.4-32.1% |
| **Difference** | **+7.6%** | |

**State Detail**:

*Southern States (highest to lowest)*:
| State | Obesity | Physical Inactivity |
|-------|---------|---------------------|
| Mississippi | 39.8% | 32.4% |
| West Virginia | 38.2% | 30.8% |
| Arkansas | 37.4% | 29.2% |
| Louisiana | 36.8% | 28.4% |
| Alabama | 36.2% | 28.8% |

*Western States (lowest to highest)*:
| State | Obesity | Physical Inactivity |
|-------|---------|---------------------|
| Colorado | 23.8% | 16.8% |
| Hawaii | 24.2% | 18.4% |
| California | 25.8% | 17.4% |
| Utah | 26.4% | 18.2% |
| Montana | 27.4% | 20.2% |

**Key Correlations**:
- Obesity ↔ Physical Inactivity: r = 0.82
- Obesity ↔ Poverty Rate: r = 0.64
- Obesity ↔ Education: r = -0.58

---

## Validation Rules

### Input Validation
- Geography must be valid identifier
- Behavior must be in CDC PLACES set

### Output Validation
- [ ] Rates between 0 and 1
- [ ] Correlations between -1 and 1
- [ ] Trends consistent with historical data

---

## Related Skills

- [chronic-disease-prevalence.md](chronic-disease-prevalence.md) - Disease outcomes
- [health-outcome-disparities.md](health-outcome-disparities.md) - Disparities
- [economic-indicators.md](../sdoh/economic-indicators.md) - Economic factors
- [cohort-specification.md](../cohorts/cohort-specification.md) - SDOH profiles
