---
name: chronic-disease-prevalence
description: >
  Analyze chronic disease prevalence using CDC PLACES data. Use for disease
  burden assessment, comorbidity analysis, geographic comparisons, and clinical
  profile development. Triggers: "diabetes rate", "prevalence", "disease burden",
  "chronic disease", "how common is [condition]", "compare [disease] rates".
---

# Chronic Disease Prevalence Skill

## Overview

The chronic-disease-prevalence skill analyzes disease prevalence rates across geographic areas using CDC PLACES data. This enables disease burden assessment, comorbidity pattern analysis, and geographic comparisons for conditions including diabetes, heart disease, COPD, cancer, and more.

**Primary Use Cases**:
- Disease burden assessment for planning
- Geographic comparison of disease rates
- Comorbidity pattern analysis
- Clinical trial feasibility estimation
- Cohort clinical profile development

---

## Trigger Phrases

- "What's the diabetes prevalence in [geography]?"
- "Compare [disease] rates between [A] and [B]"
- "Which counties have the highest [condition]?"
- "Show chronic disease burden for [geography]"
- "Comorbidity patterns for diabetics in [area]"
- "Analyze heart disease in [region]"
- "Disease profile for [geography]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, tract, metro, or state |
| `condition` | string | No | "all" | Specific condition or "all" |
| `compare_to` | string | No | - | Geography for comparison |
| `include_comorbidities` | boolean | No | true | Show comorbidity patterns |
| `include_risk_factors` | boolean | No | true | Include related risk factors |
| `benchmark` | string | No | "national" | "national", "state", "none" |
| `rank_by` | string | No | - | Condition to rank geographies |

---

## Data Sources (Embedded v2.0)

This skill reads from PopulationSim's embedded CDC PLACES data:

| Level | File | Records | Data Year |
|-------|------|---------|-----------|
| County | `data/county/places_county_2024.csv` | 3,143 | 2022 BRFSS |
| Tract | `data/tract/places_tract_2024.csv` | 83,522 | 2022 BRFSS |

### Key Columns

The PLACES files use a **wide format** with columns for each measure:
- `[MEASURE]_CrudePrev`: Crude prevalence percentage
- `[MEASURE]_AdjPrev`: Age-adjusted prevalence percentage
- `[MEASURE]_Crude95CI`: 95% confidence interval for crude estimate

### Data Lookup Pattern

```
1. Identify geography level (county or tract)
2. Read appropriate PLACES file
3. Filter by CountyFIPS or LocationID
4. Extract [MEASURE]_CrudePrev columns
5. Return with source citation
```

---

## Available Conditions

### CDC PLACES Health Outcomes (from embedded data)

| Condition | Column Prefix | National Avg |
|-----------|---------------|--------------|
| Diabetes | DIABETES | 10.1% |
| Obesity | OBESITY | 32.1% |
| Hypertension | BPHIGH | 32.4% |
| High Cholesterol | HIGHCHOL | 29.8% |
| Coronary Heart Disease | CHD | I25 | 5.4% |
| Stroke | STROKE | I63 | 3.0% |
| COPD | COPD | J44 | 6.2% |
| Asthma | CASTHMA | J45 | 9.4% |
| Chronic Kidney Disease | KIDNEY | N18 | 3.0% |
| Arthritis | ARTHRITIS | M19 | 22.8% |
| Cancer (excl. skin) | CANCER | C00-C97 | 6.1% |
| Depression | DEPRESSION | F32 | 18.6% |

### Common Comorbidity Patterns

| Primary Condition | Common Comorbidities | Correlation |
|-------------------|---------------------|-------------|
| **Diabetes** | HTN (71%), HLD (68%), Obesity (62%), CKD (25%), Depression (28%) |
| **Heart Failure** | HTN (82%), CAD (65%), Diabetes (42%), CKD (38%), AFib (35%) |
| **COPD** | HTN (52%), CAD (28%), Depression (38%), Diabetes (24%) |
| **CKD** | HTN (85%), Diabetes (45%), CAD (38%), Anemia (32%) |

---

## Generation Patterns

### Pattern 1: Single Condition Analysis

**Input**: "What's the diabetes prevalence in Harris County, TX?"

**Process**:
1. Pull CDC PLACES diabetes data for Harris County
2. Compare to Texas and national benchmarks
3. Include related metrics (obesity, A1C testing)
4. Add comorbidity context
5. Note demographic context

**Output**: Diabetes profile with context

### Pattern 2: Comparative Analysis

**Input**: "Compare heart disease rates: Appalachian vs coastal counties"

**Process**:
1. Define geography groups
2. Pull CHD, stroke, HTN for each
3. Calculate group averages
4. Identify drivers of differences
5. Add SDOH context

**Output**: Comparative analysis with explanations

### Pattern 3: Disease Burden Profile

**Input**: "Complete chronic disease profile for Los Angeles County"

**Process**:
1. Pull all CDC PLACES chronic conditions
2. Rank conditions by prevalence
3. Identify comorbidity clusters
4. Compare to state/national
5. Flag concerning patterns

**Output**: Comprehensive disease burden assessment

---

## Output Schema

```json
{
  "analysis_type": "chronic_disease_prevalence",
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County",
    "state": "TX",
    "population": 4731145
  },
  "primary_condition": {
    "name": "Diabetes",
    "variable": "DIABETES",
    "icd10_category": "E11",
    "prevalence": 0.124,
    "methodology": "age_adjusted",
    "vs_benchmarks": {
      "texas": { "value": 0.118, "diff": 0.006, "status": "above" },
      "national": { "value": 0.101, "diff": 0.023, "status": "above" }
    },
    "affected_population_estimate": 586662,
    "trend": {
      "direction": "increasing",
      "five_year_change": 0.012
    }
  },
  "comorbidities": {
    "among_diabetics": {
      "hypertension": { "rate": 0.712, "description": "HTN in diabetics" },
      "obesity": { "rate": 0.624, "description": "Obesity in diabetics" },
      "hyperlipidemia": { "rate": 0.589, "description": "HLD in diabetics" },
      "depression": { "rate": 0.281, "description": "Depression in diabetics" },
      "ckd": { "rate": 0.243, "description": "CKD in diabetics" }
    },
    "multimorbidity_estimate": {
      "diabetes_only": 0.12,
      "diabetes_plus_1": 0.28,
      "diabetes_plus_2": 0.35,
      "diabetes_plus_3_or_more": 0.25
    }
  },
  "risk_factors": {
    "obesity": { "rate": 0.338, "correlation_with_diabetes": 0.72 },
    "physical_inactivity": { "rate": 0.248, "correlation_with_diabetes": 0.54 },
    "no_annual_checkup": { "rate": 0.238, "correlation_with_diabetes": 0.38 }
  },
  "demographic_context": {
    "age_impact": "Older population increases crude rate",
    "race_ethnicity_factors": {
      "hispanic": { "pct_population": 0.438, "diabetes_disparity": "+4.2%" },
      "black": { "pct_population": 0.194, "diabetes_disparity": "+3.8%" }
    }
  },
  "healthcare_implications": {
    "estimated_annual_dm_encounters": 2347000,
    "estimated_dm_related_ed_visits": 58000,
    "insulin_users_estimate": 175000,
    "complications_risk": {
      "retinopathy": "16% of diabetics",
      "neuropathy": "28% of diabetics",
      "nephropathy": "24% of diabetics"
    }
  },
  "cohort_clinical_profile": {
    "recommended_for_diabetic_cohort": {
      "comorbidities": {
        "hypertension": 0.71,
        "obesity": 0.62,
        "hyperlipidemia": 0.59,
        "depression": 0.28,
        "ckd": 0.24
      },
      "medications": {
        "metformin": 0.72,
        "sulfonylurea": 0.28,
        "insulin": 0.30,
        "ace_arb": 0.68,
        "statin": 0.62
      }
    }
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "data_vintage": "CDC_PLACES_2024",
    "methodology_notes": [
      "Age-adjusted to 2000 US standard population",
      "Comorbidity rates from MEPS and literature",
      "Population estimates from Census ACS 2022"
    ]
  }
}
```

---

## Examples

### Example 1: Diabetes Deep Dive

**Request**: "Analyze diabetes in San Antonio metro"

**Response**:

**Diabetes Analysis: San Antonio-New Braunfels, TX MSA**

**Prevalence**: 12.8% (vs 10.1% national) ⚠️

| Metric | San Antonio | Texas | National | Status |
|--------|-------------|-------|----------|--------|
| Diabetes | 12.8% | 11.8% | 10.1% | High |
| Obesity | 35.2% | 33.2% | 32.1% | High |
| Physical Inactivity | 26.8% | 25.4% | 22.8% | High |
| No Annual Checkup | 25.4% | 25.8% | 22.4% | High |

**Affected Population**: ~307,000 adults with diabetes

**Comorbidity Profile** (among diabetics):
- 72% Hypertension
- 64% Obesity
- 58% Hyperlipidemia
- 26% Depression
- 22% CKD

**Demographic Context**:
- 65% Hispanic population (higher diabetes risk)
- Border region health patterns
- Lower median income than state average

**Geographic Variation** (county-level):
| County | Diabetes | SVI |
|--------|----------|-----|
| Bexar | 12.4% | 0.62 |
| Comal | 9.8% | 0.24 |
| Guadalupe | 10.2% | 0.38 |

---

### Example 2: Multi-Disease Comparison

**Request**: "Compare chronic disease burden: Mississippi vs Colorado"

**Response**:

**Chronic Disease Comparison: MS vs CO**

| Condition | Mississippi | Colorado | Difference |
|-----------|-------------|----------|------------|
| Diabetes | 14.2% | 7.4% | +6.8% ⚠️ |
| Obesity | 39.8% | 23.8% | +16.0% ⚠️ |
| Hypertension | 40.2% | 26.8% | +13.4% ⚠️ |
| Heart Disease | 8.2% | 4.8% | +3.4% ⚠️ |
| Stroke | 4.8% | 2.4% | +2.4% ⚠️ |
| COPD | 9.2% | 5.8% | +3.4% ⚠️ |
| Depression | 22.4% | 19.8% | +2.6% |

**Key Drivers of Disparity**:

| Factor | Mississippi | Colorado |
|--------|-------------|----------|
| Poverty Rate | 19.4% | 9.4% |
| Uninsured | 11.8% | 7.2% |
| Smoking | 19.8% | 13.2% |
| Physical Inactivity | 32.4% | 16.8% |
| No HS Diploma | 14.2% | 8.4% |

**Analysis**: Mississippi's chronic disease burden is driven by:
1. Higher poverty and lower education
2. Higher rates of modifiable risk factors
3. Lower healthcare access
4. Rural healthcare challenges

---

### Example 3: Top Counties Analysis

**Request**: "Which US counties have the highest diabetes rates?"

**Response**:

**Top 10 Counties by Diabetes Prevalence**

| Rank | County | State | Diabetes | Population | Key Factors |
|------|--------|-------|----------|------------|-------------|
| 1 | Starr | TX | 18.4% | 67,141 | 96% Hispanic, poverty 38%, border |
| 2 | Hidalgo | TX | 17.2% | 870,781 | 92% Hispanic, poverty 27% |
| 3 | Cameron | TX | 16.8% | 423,725 | 91% Hispanic, poverty 28% |
| 4 | Zavala | TX | 16.4% | 11,840 | 94% Hispanic, poverty 35% |
| 5 | Pemiscot | MO | 16.2% | 15,820 | Rural, poverty 32%, SVI 0.94 |
| 6 | Holmes | MS | 15.8% | 16,955 | 82% Black, poverty 42%, rural |
| 7 | Humphreys | MS | 15.6% | 8,145 | 75% Black, poverty 38% |
| 8 | Webb | TX | 15.4% | 276,652 | 96% Hispanic, border region |
| 9 | Tunica | MS | 15.2% | 9,227 | 78% Black, poverty 35% |
| 10 | Coahoma | MS | 15.0% | 21,613 | 76% Black, poverty 32% |

**Pattern Analysis**:
- Texas border counties: Hispanic population, border region health patterns
- Mississippi Delta: Black population, extreme poverty, rural
- Common factors: High poverty, limited access, high obesity, high SVI

---

## Validation Rules

### Input Validation
- Geography must be valid (county, tract, metro, state)
- Condition must be in CDC PLACES measure set
- Comparison geographies must be same level

### Output Validation
- [ ] Prevalence rates between 0 and 1
- [ ] Age-adjusted rates used for comparisons
- [ ] Comorbidity rates sum appropriately
- [ ] Population estimates match Census data

### Clinical Reasonability
- Diabetes rarely > 20% even in high-risk areas
- CHD rates typically 3-10%
- Comorbidity rates should reflect clinical reality

---

## Related Skills

- [health-behavior-patterns.md](health-behavior-patterns.md) - Risk factor analysis
- [health-outcome-disparities.md](health-outcome-disparities.md) - Disparities by group
- [county-profile.md](../geographic/county-profile.md) - Full county profile
- [cohort-specification.md](../cohorts/cohort-specification.md) - Clinical profiles
- [feasibility-estimation.md](../trial-support/feasibility-estimation.md) - Trial planning

---

## Data Sources

| Source | Content | Geography | Update |
|--------|---------|-----------|--------|
| CDC PLACES | Disease prevalence | County, Tract | Annual |
| MEPS | Comorbidity rates | National | Annual |
| BRFSS | Survey data | State | Annual |
| CDC Wonder | Mortality | County | Annual |
