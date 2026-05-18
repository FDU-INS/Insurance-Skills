---
name: economic-indicators
description: >
  Analyze economic SDOH factors including income, poverty, employment, and
  economic security. Use for understanding financial barriers to healthcare
  and informing cost-related SDOH profiles. Triggers: "poverty rate", "income",
  "unemployment", "economic indicators", "financial barriers".
---

# Economic Indicators Skill

## Overview

The economic-indicators skill provides detailed analysis of economic factors that influence health outcomes, including income levels, poverty rates, employment status, and economic security. These factors are key drivers of healthcare access, medication adherence, and health outcomes.

**Primary Use Cases**:
- Financial barrier assessment
- Insurance type prediction
- Cost-related SDOH profiling
- Economic disparity analysis
- Member population characterization

---

## Trigger Phrases

- "What's the poverty rate in [geography]?"
- "Income levels in [area]"
- "Unemployment analysis for [geography]"
- "Economic indicators for [region]"
- "Financial barriers in [area]"
- "Compare income between [A] and [B]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, tract, metro, or state |
| `indicators` | array | No | all | Specific indicators to analyze |
| `compare_to` | string | No | - | Geography for comparison |
| `stratify_by` | string | No | - | "race", "age", "education" |

---

## Data Sources (Embedded v2.0)

Economic indicators are available in embedded SVI data:

| Indicator | File | Column |
|-----------|------|--------|
| Below 150% Poverty (%) | `data/county/svi_county_2022.csv` | EP_POV150 |
| Below 150% Poverty (count) | `data/tract/svi_tract_2022.csv` | E_POV150 |
| Unemployment (%) | `data/tract/svi_tract_2022.csv` | EP_UNEMP |
| Unemployment (count) | `data/tract/svi_tract_2022.csv` | E_UNEMP |
| Housing Cost Burden (%) | `data/tract/svi_tract_2022.csv` | EP_HBURD |
| No Health Insurance (%) | `data/tract/svi_tract_2022.csv` | EP_UNINSUR |

### ADI Economic Context
The Area Deprivation Index (`data/block_group/adi_blockgroup_2023.csv`) incorporates:
- Median family income
- Income disparity ratio
- Unemployment rate
- Poverty rate

### Data Lookup Pattern

```
1. Identify geography type and FIPS code
2. Read SVI file for economic indicators
3. Read ADI for neighborhood-level deprivation
4. Compare to national/state benchmarks
5. Return with source citations
```

**Note**: Detailed income distributions require ACS microdata not in embedded package. SVI provides key economic indicators for SDOH profiling.

---

## Key Economic Indicators

### Income Measures (ACS)

| Indicator | Definition | National Value |
|-----------|------------|----------------|
| Median Household Income | 50th percentile household income | $74,580 |
| Per Capita Income | Total income / population | $39,456 |
| Median Family Income | 50th percentile family income | $91,612 |
| Mean Household Income | Average household income | $102,316 |

### Poverty Measures (ACS)

| Indicator | Definition | National Value |
|-----------|------------|----------------|
| Poverty Rate | Below 100% FPL | 11.5% |
| Deep Poverty | Below 50% FPL | 5.2% |
| Near Poverty | 100-150% FPL | 8.4% |
| Low Income | Below 200% FPL | 28.2% |

### Federal Poverty Level (2024)

| Household Size | 100% FPL | 150% FPL | 200% FPL |
|----------------|----------|----------|----------|
| 1 | $15,060 | $22,590 | $30,120 |
| 2 | $20,440 | $30,660 | $40,880 |
| 3 | $25,820 | $38,730 | $51,640 |
| 4 | $31,200 | $46,800 | $62,400 |

### Employment Measures (ACS)

| Indicator | Definition | National Value |
|-----------|------------|----------------|
| Labor Force Participation | In labor force / population 16+ | 63.2% |
| Unemployment Rate | Unemployed / labor force | 3.6% |
| Employment Rate | Employed / population 16+ | 60.1% |

### Economic Security

| Indicator | Definition | Source |
|-----------|------------|--------|
| Food Insecurity | Lack reliable food access | USDA |
| Housing Cost Burden | Paying >30% income for housing | ACS |
| Severe Housing Burden | Paying >50% income for housing | ACS |
| Asset Poverty | Insufficient savings for 3 months | Survey |

---

## Output Schema

```json
{
  "analysis_type": "economic_indicators",
  "geography": {
    "type": "county",
    "fips": "06037",
    "name": "Los Angeles County",
    "state": "CA",
    "population": 9829544
  },
  "income": {
    "median_household": 76367,
    "per_capita": 36586,
    "median_family": 87212,
    "vs_state": -2842,
    "vs_national": 1787,
    "distribution": {
      "under_25k": 0.182,
      "25k_50k": 0.168,
      "50k_75k": 0.142,
      "75k_100k": 0.108,
      "100k_150k": 0.148,
      "150k_plus": 0.252
    },
    "gini_coefficient": 0.508
  },
  "poverty": {
    "poverty_rate": 0.134,
    "deep_poverty": 0.062,
    "near_poverty": 0.098,
    "low_income_200pct": 0.324,
    "vs_state": 0.011,
    "vs_national": 0.019,
    "population_in_poverty": 1317000,
    "by_age": {
      "under_18": 0.184,
      "18_64": 0.128,
      "65_plus": 0.118
    },
    "by_race": {
      "white_nh": 0.092,
      "black": 0.198,
      "hispanic": 0.168,
      "asian": 0.108
    }
  },
  "employment": {
    "labor_force_participation": 0.642,
    "unemployment_rate": 0.048,
    "employment_rate": 0.612,
    "by_industry": {
      "healthcare": 0.128,
      "retail": 0.108,
      "professional": 0.142,
      "manufacturing": 0.082
    }
  },
  "economic_security": {
    "food_insecurity": 0.108,
    "housing_cost_burden": 0.428,
    "severe_housing_burden": 0.218,
    "no_health_insurance": 0.082
  },
  "health_correlations": {
    "poverty_health_impact": {
      "diabetes_in_poverty": 0.148,
      "diabetes_non_poverty": 0.092,
      "gap": 0.056
    },
    "income_insurance_correlation": {
      "under_25k_uninsured": 0.142,
      "over_75k_uninsured": 0.038
    }
  },
  "cohort_implications": {
    "insurance_type_distribution": {
      "employer": 0.42,
      "medicaid": 0.28,
      "medicare": 0.14,
      "individual": 0.06,
      "uninsured": 0.08
    },
    "cost_barrier_rate": 0.182,
    "rx_cost_barrier_rate": 0.124
  },
  "metadata": {
    "data_source": "ACS_2022_5yr",
    "generated_at": "2024-12-23T10:00:00Z"
  }
}
```

---

## Examples

### Example 1: Poverty Analysis

**Request**: "Analyze poverty in Mississippi Delta counties"

**Response**:

**Mississippi Delta Poverty Analysis**

**Counties Analyzed**: Bolivar, Coahoma, Humphreys, Leflore, Quitman, Sunflower, Tallahatchie, Tunica, Washington

**Summary**:
| Metric | Delta Average | Mississippi | National | Gap |
|--------|---------------|-------------|----------|-----|
| Poverty Rate | 32.4% | 19.4% | 11.5% | +20.9% ⚠️ |
| Deep Poverty | 16.8% | 8.2% | 5.2% | +11.6% |
| Child Poverty | 48.2% | 27.4% | 16.8% | +31.4% ⚠️ |
| Median Income | $28,420 | $46,511 | $74,580 | -$46,160 |

**By County**:
| County | Poverty | Child Poverty | Median Income |
|--------|---------|---------------|---------------|
| Humphreys | 38.4% | 54.2% | $24,200 |
| Holmes | 36.8% | 52.4% | $25,800 |
| Quitman | 34.2% | 48.8% | $26,400 |
| Tunica | 32.8% | 46.2% | $27,200 |

**Health Impact**:
| Metric | Delta | Non-Delta MS | Gap |
|--------|-------|--------------|-----|
| Diabetes | 16.8% | 12.4% | +4.4% |
| Uninsured | 14.2% | 10.8% | +3.4% |
| No Checkup | 34.2% | 26.8% | +7.4% |

**SDOH Z-Code Implications**:
- Z59.6 (Low income): 32.4% of patients
- Z59.41 (Food insecurity): 24.8% of patients
- Z59.7 (Insufficient social insurance): 14.2%

---

### Example 2: Income Stratification

**Request**: "Income distribution and health correlation in Phoenix metro"

**Response**:

**Phoenix Metro Income-Health Analysis**

**Income Distribution**:
| Income Bracket | % of Households | Cumulative |
|----------------|-----------------|------------|
| Under $25,000 | 14.2% | 14.2% |
| $25,000-$50,000 | 18.4% | 32.6% |
| $50,000-$75,000 | 16.8% | 49.4% |
| $75,000-$100,000 | 14.2% | 63.6% |
| $100,000-$150,000 | 16.4% | 80.0% |
| Over $150,000 | 20.0% | 100% |

**Income-Health Correlation**:
| Metric | <$25K | $25-50K | $50-75K | $75-100K | >$100K |
|--------|-------|---------|---------|----------|--------|
| Uninsured | 18.4% | 12.2% | 7.8% | 5.2% | 3.4% |
| Diabetes | 14.8% | 12.4% | 10.2% | 8.4% | 6.8% |
| Obesity | 38.4% | 34.2% | 30.8% | 28.2% | 24.8% |
| Depression | 28.2% | 22.4% | 18.8% | 16.2% | 14.4% |
| No Checkup | 38.4% | 28.2% | 22.4% | 18.8% | 14.2% |

**Gradient Analysis**:
- Diabetes: 2.2x higher in lowest vs highest income
- Depression: 2.0x higher
- Uninsured: 5.4x higher

---

### Example 3: Employment Impact

**Request**: "Unemployment and health in Rust Belt metros"

**Response**:

**Rust Belt Metro Employment-Health Analysis**

**Metros**: Cleveland, Detroit, Pittsburgh, Buffalo, Youngstown

**Employment Metrics**:
| Metro | Unemployment | Labor Force Part. | vs National |
|-------|--------------|-------------------|-------------|
| Youngstown | 6.2% | 58.4% | +2.6% / -4.8% |
| Detroit | 5.4% | 60.2% | +1.8% / -3.0% |
| Cleveland | 4.8% | 62.4% | +1.2% / -0.8% |
| Buffalo | 4.4% | 61.8% | +0.8% / -1.4% |
| Pittsburgh | 4.2% | 63.8% | +0.6% / +0.6% |

**Unemployment-Health Link**:
| Health Metric | High Unemp Areas | Low Unemp Areas | Gap |
|---------------|------------------|-----------------|-----|
| Depression | 24.8% | 16.2% | +8.6% |
| Uninsured | 12.4% | 6.8% | +5.6% |
| Fair/Poor Health | 22.4% | 14.2% | +8.2% |
| Delayed Care | 18.4% | 10.2% | +8.2% |

**HealthSim Implications**:
- Higher Medicaid enrollment in high-unemployment areas
- Elevated mental health diagnoses (F32.x, F41.x)
- Z56.0 (Unemployment) Z-code assignment

---

## Validation Rules

### Input Validation
- Geography must be valid
- Stratification must be valid dimension

### Output Validation
- [ ] Percentages between 0 and 1
- [ ] Income values positive
- [ ] Poverty rate consistent with income distribution
- [ ] Employment rates sum correctly

---

## Related Skills

- [svi-analysis.md](svi-analysis.md) - Includes economic theme
- [adi-analysis.md](adi-analysis.md) - Economic deprivation
- [healthcare-access-analysis.md](../health-patterns/healthcare-access-analysis.md) - Insurance
- [cohort-specification.md](../cohorts/cohort-specification.md) - Coverage distribution
