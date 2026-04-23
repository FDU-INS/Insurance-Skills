---
name: demographic-distribution
description: >
  Build accurate demographic distributions for cohorts including age, sex,
  and race/ethnicity. Provides empirical distributions from Census data
  with optional condition-specific adjustments. Triggers: "age distribution",
  "demographics for cohort", "population distribution", "demographic profile".
---

# Demographic Distribution Skill

## Overview

The demographic-distribution skill creates accurate demographic profiles for cohorts by leveraging Census ACS data and condition-specific adjustments. It generates age, sex, and race/ethnicity distributions that can be used directly in CohortSpecification objects.

**Primary Use Cases**:
- Set realistic age distributions
- Match geographic demographics
- Adjust for condition-specific patterns
- Support diversity requirements

---

## Trigger Phrases

- "Age distribution for [geography/condition]"
- "Demographics for [population]"
- "What's the age breakdown for diabetics?"
- "Match demographics to [geography]"
- "Demographic profile for [cohort type]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | Geographic reference |
| `condition` | string | No | - | Condition for adjustment |
| `age_brackets` | array | No | standard | Custom age groupings |
| `match_source` | string | No | "acs" | "acs", "medicare", "medicaid" |

---

## Data Sources (Embedded v2.0)

Demographic data comes from embedded SVI files:

| Metric | File | Columns |
|--------|------|---------|
| Total Population | `data/tract/svi_tract_2022.csv` | E_TOTPOP |
| Age 65+ | `data/tract/svi_tract_2022.csv` | E_AGE65, EP_AGE65 |
| Age Under 18 | `data/tract/svi_tract_2022.csv` | E_AGE17, EP_AGE17 |
| Minority Status | `data/tract/svi_tract_2022.csv` | E_MINRTY, EP_MINRTY |
| African American | `data/tract/svi_tract_2022.csv` | E_AFAM, EP_AFAM |
| Hispanic | `data/tract/svi_tract_2022.csv` | E_HISP, EP_HISP |
| Asian | `data/tract/svi_tract_2022.csv` | E_ASIAN, EP_ASIAN |

### Data Lookup Pattern

```
1. Identify geography FIPS code
2. Read SVI tract file for demographic indicators
3. Calculate demographic proportions from E_* and EP_* columns
4. Aggregate across tracts if county/metro level
5. Apply condition-specific adjustments from domain knowledge
6. Return distributions with source citation
```

**Note**: Detailed age breakdowns (5-year groups) require ACS S0101 not in embedded package. SVI provides key demographic segments.

---

## Standard Age Brackets

### General Population
```json
{
  "0-17": "pediatric",
  "18-24": "young_adult",
  "25-34": "adult_1",
  "35-44": "adult_2",
  "45-54": "middle_age_1",
  "55-64": "middle_age_2",
  "65-74": "senior_1",
  "75-84": "senior_2",
  "85+": "elderly"
}
```

### Chronic Disease Cohorts
```json
{
  "18-44": "young_onset",
  "45-54": "early_middle",
  "55-64": "late_middle",
  "65-74": "early_senior",
  "75+": "late_senior"
}
```

### Pediatric
```json
{
  "0-1": "infant",
  "2-5": "early_childhood",
  "6-11": "childhood",
  "12-17": "adolescent"
}
```

---

## Condition-Specific Adjustments

### Diabetes (E11)
| Factor | Adjustment |
|--------|------------|
| Age shift | +8 years mean age |
| 65+ representation | +15% vs general |
| Male prevalence | 1.05x female |

### Heart Failure (I50)
| Factor | Adjustment |
|--------|------------|
| Age shift | +18 years mean age |
| 65+ representation | +35% vs general |
| Male prevalence | 1.15x female |

### Asthma (J45)
| Factor | Adjustment |
|--------|------------|
| Age distribution | Bimodal (child + adult) |
| Pediatric peak | Age 5-14 |
| Female prevalence | 1.25x male (adult) |

### Depression (F32)
| Factor | Adjustment |
|--------|------------|
| Age peak | 25-44 years |
| Female prevalence | 1.7x male |
| 65+ representation | -10% vs general |

---

## Output Schema

```json
{
  "demographics": {
    "source_geography": {
      "type": "county",
      "fips": "48201",
      "name": "Harris County, TX"
    },
    "source_data": "ACS_2022_5yr",
    "condition_adjustment": "E11",
    
    "age": {
      "min": 18,
      "max": 95,
      "mean": 58.4,
      "median": 59,
      "std": 14.2,
      "distribution": {
        "18-44": 0.18,
        "45-54": 0.22,
        "55-64": 0.28,
        "65-74": 0.22,
        "75+": 0.10
      },
      "cumulative": {
        "18-44": 0.18,
        "18-54": 0.40,
        "18-64": 0.68,
        "18-74": 0.90,
        "18+": 1.00
      }
    },
    
    "sex": {
      "male": 0.47,
      "female": 0.53,
      "ratio_m_to_f": 0.89,
      "notes": "Slight female predominance in diabetes"
    },
    
    "race_ethnicity": {
      "white_nh": 0.28,
      "black": 0.20,
      "hispanic": 0.42,
      "asian": 0.08,
      "aian": 0.004,
      "nhpi": 0.002,
      "two_or_more": 0.028,
      "other": 0.006
    },
    
    "age_by_sex": {
      "male": {
        "18-44": 0.20,
        "45-64": 0.52,
        "65+": 0.28
      },
      "female": {
        "18-44": 0.16,
        "45-64": 0.48,
        "65+": 0.36
      }
    },
    
    "age_by_race": {
      "white_nh": { "mean_age": 62.4, "65_plus": 0.38 },
      "black": { "mean_age": 56.8, "65_plus": 0.28 },
      "hispanic": { "mean_age": 54.2, "65_plus": 0.22 },
      "asian": { "mean_age": 58.4, "65_plus": 0.30 }
    }
  },
  
  "validation": {
    "source": "ACS_S0101_S1701_B03002",
    "adjustment_applied": "diabetes_age_shift",
    "confidence": "high"
  }
}
```

---

## Examples

### Example 1: Geographic Demographics

**Request**: "Demographics for Cook County, Illinois"

**Response**:

**Cook County Demographics (General Population)**

| Age Group | Percentage | Population |
|-----------|------------|------------|
| 0-17 | 21.4% | 1,089,000 |
| 18-24 | 9.2% | 468,000 |
| 25-34 | 14.8% | 753,000 |
| 35-44 | 13.2% | 672,000 |
| 45-54 | 12.4% | 631,000 |
| 55-64 | 12.8% | 651,000 |
| 65-74 | 9.8% | 499,000 |
| 75+ | 6.4% | 326,000 |

**Sex**: Male 48.2%, Female 51.8%

**Race/Ethnicity**:
| Group | Percentage |
|-------|------------|
| White NH | 42.8% |
| Black | 23.4% |
| Hispanic | 25.8% |
| Asian | 7.2% |
| Other | 0.8% |

---

### Example 2: Condition-Adjusted

**Request**: "Age distribution for diabetics in Texas"

**Response**:

**Texas Diabetic Population Age Distribution**

*Adjusted from general population for E11 prevalence patterns*

| Age Group | General Pop | Diabetic Pop | Adjustment |
|-----------|-------------|--------------|------------|
| 18-44 | 38.2% | 18.4% | -19.8% |
| 45-54 | 12.8% | 22.4% | +9.6% |
| 55-64 | 11.4% | 26.8% | +15.4% |
| 65-74 | 8.2% | 21.2% | +13.0% |
| 75+ | 5.8% | 11.2% | +5.4% |

**Summary Statistics**:
- Mean Age: 59.2 years (vs 38.4 general)
- Median Age: 60 years
- 65+ Representation: 32.4% (vs 14.0% general)

**Sex Distribution**:
- Male: 48.2% (slight under-representation)
- Female: 51.8%

---

### Example 3: Diversity Matching

**Request**: "Match demographics for clinical trial with 40% minority target"

**Response**:

**Clinical Trial Demographic Targets (40% Minority)**

**Baseline** (US National):
- White NH: 60%
- Minority: 40%

**Stratified Minority Target**:
| Group | Natural Rate | Target | Adjustment |
|-------|--------------|--------|------------|
| White NH | 60% | 60% | - |
| Black | 12% | 15% | +3% |
| Hispanic | 18% | 18% | - |
| Asian | 6% | 5% | -1% |
| Other | 4% | 2% | -2% |

**Age Distribution** (Adult Trial):
| Age | Target |
|-----|--------|
| 18-44 | 28% |
| 45-64 | 45% |
| 65+ | 27% |

**Sex**: 50% male, 50% female (balanced design)

**Sampling Recommendation**:
- Over-sample minority sites
- Target urban academic centers for Black enrollment
- Southwest sites for Hispanic enrollment

---

## Validation Rules

### Distribution Checks
- [ ] Age brackets sum to 1.0 (±0.01)
- [ ] Sex sums to 1.0
- [ ] Race/ethnicity sums to 1.0 (±0.02)

### Reasonability Checks
- [ ] Mean age within expected range for condition
- [ ] Sex ratio clinically plausible
- [ ] Geographic demographics match source

---

## Related Skills

- [cohort-specification.md](cohort-specification.md) - Full cohort
- [county-profile.md](../geographic/county-profile.md) - Geographic source
- [health-outcome-disparities.md](../health-patterns/health-outcome-disparities.md) - Race patterns
