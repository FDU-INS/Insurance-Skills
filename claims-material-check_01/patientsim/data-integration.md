---
name: patientsim-data-integration
description: |
  Foundation skill for data-driven patient generation using PopulationSim v2.0 
  embedded data. Provides lookup patterns, provenance tracking, and SDOH integration.
  Triggers: data-driven patient, geography-based, real demographics, population data
---

# PatientSim Data Integration

## For Claude

This is a **foundation skill** that enables data-driven patient generation. Load this skill when:

- User specifies a geography (county FIPS, tract FIPS, city/state)
- User requests "realistic demographics" or "population-based" patients
- User mentions SDOH factors, social vulnerability, or health disparities
- Any clinical cohort skill needs real population data

**This skill does NOT generate patients directly** - it provides the data lookup patterns that other PatientSim skills use.

---

## Overview

PopulationSim v2.0 embeds real population health data that PatientSim uses to generate clinically realistic patients. Instead of generic national averages, data-driven generation uses actual rates for specific geographies.

### Generation Modes

| Mode | Trigger | Data Source |
|------|---------|-------------|
| Generic | No geography specified | National averages |
| County-Level | 5-digit FIPS (e.g., "48201") | CDC PLACES + SVI county files |
| Tract-Level | 11-digit FIPS (e.g., "48201002300") | CDC PLACES + SVI tract files |
| Block Group | 12-digit FIPS | ADI block group file |

---

## Embedded Data Files

### County-Level Health Data

**File:** `skills/populationsim/data/county/places_county_2024.csv`

| Column Pattern | Example | Description |
|----------------|---------|-------------|
| `{MEASURE}_CrudePrev` | DIABETES_CrudePrev | Crude prevalence (%) |
| `{MEASURE}_Crude95CI` | DIABETES_Crude95CI | 95% confidence interval |
| `{MEASURE}_AdjPrev` | DIABETES_AdjPrev | Age-adjusted prevalence (%) |
| `StateAbbr` | TX | State abbreviation |
| `CountyName` | Harris County | County name |
| `CountyFIPS` | 48201 | 5-digit FIPS code |
| `TotalPopulation` | 4731145 | Population count |

**Available Health Measures (40 total):**

*Chronic Conditions:*
- DIABETES - Diabetes prevalence
- OBESITY - Obesity prevalence  
- BPHIGH - High blood pressure
- HIGHCHOL - High cholesterol
- CHD - Coronary heart disease
- STROKE - Stroke history
- COPD - Chronic obstructive pulmonary disease
- CASTHMA - Current asthma
- KIDNEY - Chronic kidney disease
- CANCER - Cancer (excluding skin)
- ARTHRITIS - Arthritis
- DEPRESSION - Depression

*Health Behaviors:*
- CSMOKING - Current smoking
- LPA - No leisure-time physical activity
- BINGE - Binge drinking
- SLEEP - Short sleep duration (<7 hours)

*Prevention & Access:*
- ACCESS2 - Lack of health insurance (18-64)
- CHECKUP - Annual checkup
- DENTAL - Dental visit
- CHOLSCREEN - Cholesterol screening
- MAMMOGRAPHY - Mammography (women 50-74)
- COLON_SCREEN - Colorectal cancer screening

*Disabilities:*
- DISABILITY - Any disability
- HEARING - Hearing disability
- VISION - Vision disability
- COGNITION - Cognitive disability
- MOBILITY - Mobility disability

### County-Level Social Vulnerability

**File:** `skills/populationsim/data/county/svi_county_2022.csv`

| Column | Range | Description |
|--------|-------|-------------|
| FIPS | 5-digit | County FIPS code |
| RPL_THEMES | 0-1 | Overall vulnerability percentile |
| RPL_THEME1 | 0-1 | Socioeconomic status |
| RPL_THEME2 | 0-1 | Household composition/disability |
| RPL_THEME3 | 0-1 | Minority status/language |
| RPL_THEME4 | 0-1 | Housing type/transportation |
| EP_POV150 | % | Below 150% poverty |
| EP_UNEMP | % | Unemployed |
| EP_NOHSDP | % | No high school diploma |
| EP_UNINSUR | % | Uninsured |
| EP_AGE65 | % | Age 65 and older |
| EP_DISABL | % | With disability |
| EP_MINRTY | % | Minority |
| EP_MUNIT | % | Multi-unit housing |
| EP_MOBILE | % | Mobile homes |
| EP_NOVEH | % | No vehicle |

### Tract-Level Data

Same structure as county files, with 11-digit tract FIPS:

- `skills/populationsim/data/tract/places_tract_2024.csv`
- `skills/populationsim/data/tract/svi_tract_2022.csv`

### Block Group ADI

**File:** `skills/populationsim/data/block_group/adi_blockgroup_2023.csv`

| Column | Range | Description |
|--------|-------|-------------|
| FIPS | 12-digit | Block group FIPS |
| ADI_NATRANK | 1-100 | National percentile (higher = more deprived) |
| ADI_STAESSION | 1-10 | State decile |

---

## Lookup Patterns

### Pattern 1: County Health Lookup

```
Given: County FIPS "48201" (Harris County, TX)
Action: Look up row in places_county_2024.csv where CountyFIPS = "48201"
Result: DIABETES_CrudePrev = 12.1, OBESITY_CrudePrev = 32.8, etc.
```

### Pattern 2: County Vulnerability Lookup

```
Given: County FIPS "48201"
Action: Look up row in svi_county_2022.csv where FIPS = "48201"
Result: RPL_THEMES = 0.68, EP_UNINSUR = 22.1, etc.
```

### Pattern 3: Tract-Level Lookup

```
Given: Tract FIPS "48201002300"
Action: Look up row in places_tract_2024.csv where TractFIPS = "48201002300"
Result: More granular neighborhood-level data
```

### Pattern 4: Block Group ADI Lookup

```
Given: Block Group FIPS "482010023001"
Action: Look up row in adi_blockgroup_2023.csv where FIPS = "482010023001"
Result: ADI_NATRANK = 78 (moderately high deprivation)
```

---

## SDOH-to-Outcome Correlations

SVI and ADI scores affect clinical outcomes in predictable ways:

### Medication Adherence

| Vulnerability | Adherence Modifier |
|---------------|-------------------|
| RPL_THEMES < 0.25 | +10% adherence |
| RPL_THEMES 0.25-0.50 | Baseline |
| RPL_THEMES 0.50-0.75 | -10% adherence |
| RPL_THEMES > 0.75 | -20% adherence |

### Disease Control

| ADI Percentile | A1C Control Impact |
|----------------|-------------------|
| 1-25 | Well-controlled more likely |
| 26-50 | Baseline |
| 51-75 | Moderate control more likely |
| 76-100 | Poor control more likely |

### Healthcare Access

| EP_UNINSUR | Access Pattern |
|------------|----------------|
| < 10% | Regular preventive care |
| 10-20% | Delayed care patterns |
| > 20% | ED-dominant care patterns |

---

## Provenance Output Format

When using data-driven generation, include provenance in output:

```json
{
  "metadata": {
    "generation_mode": "data_driven",
    "geography": {
      "fips": "48201",
      "name": "Harris County",
      "state": "TX",
      "level": "county",
      "population": 4731145
    },
    "data_provenance": [
      {
        "source": "CDC_PLACES_2024",
        "data_year": 2022,
        "release_version": "2024 Release",
        "methodology": "model_based_estimate",
        "file_reference": "populationsim/data/county/places_county_2024.csv",
        "fields_used": ["DIABETES_CrudePrev", "OBESITY_CrudePrev"]
      },
      {
        "source": "CDC_SVI_2022",
        "data_year": 2022,
        "methodology": "direct_lookup",
        "file_reference": "populationsim/data/county/svi_county_2022.csv",
        "fields_used": ["RPL_THEMES", "EP_UNINSUR"]
      }
    ],
    "rates_applied": {
      "diabetes_prevalence": 0.121,
      "obesity_prevalence": 0.328,
      "vulnerability_score": 0.68
    }
  }
}
```

---

## Example: Data-Driven Diabetic Patient

**Request:** "Generate a diabetic patient in Harris County, TX"

**Data Lookup:**
```
From places_county_2024.csv (FIPS 48201):
  DIABETES_CrudePrev: 12.1%
  OBESITY_CrudePrev: 32.8%
  BPHIGH_CrudePrev: 32.4%
  KIDNEY_CrudePrev: 3.2%

From svi_county_2022.csv (FIPS 48201):
  RPL_THEMES: 0.68 (high vulnerability)
  EP_UNINSUR: 22.1%
  EP_POV150: 28.4%
```

**Applied to Generation:**
- Base diabetes rate: 12.1% (vs national 10.1%)
- Comorbidity probability adjusted: 32.8% obesity, 32.4% hypertension
- Adherence modifier: -15% (RPL_THEMES = 0.68)
- A1C control: Moderate-to-poor more likely
- Insurance: 22.1% chance uninsured

**Output includes provenance tracking the data sources used.**

---

## Related Skills

- [PopulationSim → PatientSim Integration](../populationsim/integration/patientsim-integration.md) - Complete mapping specification
- [diabetes-management.md](diabetes-management.md) - Example of data-driven clinical cohort
- [PopulationSim SKILL.md](../populationsim/SKILL.md) - Data package overview
