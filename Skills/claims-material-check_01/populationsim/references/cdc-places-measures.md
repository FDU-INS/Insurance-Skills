---
name: cdc-places-measures
description: >
  Complete reference for CDC PLACES 27 health measures including definitions,
  data collection methods, and national benchmarks.
---

# CDC PLACES Health Measures Reference

## Overview

CDC PLACES (Population Level Analysis and Community Estimates) provides model-based estimates for 27 chronic disease measures at county and census tract levels. Data is produced using multilevel regression and poststratification (MRP) methodology.

**Source**: CDC Division of Population Health
**Geography**: County, Census Tract, ZCTA
**Update Frequency**: Annual
**Current Version**: PLACES 2024 (2022 BRFSS data)

---

## Embedded Data Files (v2.0)

| Level | File | Records |
|-------|------|---------|
| County | `data/county/places_county_2024.csv` | 3,143 |
| Tract | `data/tract/places_tract_2024.csv` | 83,522 |

### Column Naming Convention

The PLACES files use a **wide format** with multiple columns per measure:
- `[MEASURE]_CrudePrev`: Crude prevalence percentage (e.g., `DIABETES_CrudePrev`)
- `[MEASURE]_AdjPrev`: Age-adjusted prevalence percentage
- `[MEASURE]_Crude95CI`: 95% confidence interval for crude estimate
- `[MEASURE]_Adj95CI`: 95% confidence interval for adjusted estimate

### Key Geography Columns
- `StateAbbr`: State abbreviation (e.g., "TX")
- `CountyName`: County name
- `CountyFIPS`: 5-digit county FIPS code
- `LocationID`: 11-digit tract FIPS (tract file only)
- `TotalPopulation`: Population 18+

---

## Health Outcomes (13 measures)

### Chronic Diseases

| Measure | Definition | Age Group | National Rate |
|---------|------------|-----------|---------------|
| **ARTHRITIS** | Arthritis among adults | 18+ | 24.2% |
| **BPHIGH** | High blood pressure among adults | 18+ | 32.4% |
| **CANCER** | Cancer (excluding skin) among adults | 18+ | 6.9% |
| **CASTHMA** | Current asthma among adults | 18+ | 9.8% |
| **CHD** | Coronary heart disease among adults | 18+ | 5.4% |
| **COPD** | COPD among adults | 18+ | 6.4% |
| **DIABETES** | Diagnosed diabetes among adults | 18+ | 10.1% |
| **HIGHCHOL** | High cholesterol among adults screened | 18+ | 30.8% |
| **KIDNEY** | Chronic kidney disease among adults | 18+ | 3.1% |
| **OBESITY** | Obesity among adults | 18+ | 32.1% |
| **STROKE** | Stroke among adults | 18+ | 3.4% |

### Mental Health & Disability

| Measure | Definition | Age Group | National Rate |
|---------|------------|-----------|---------------|
| **DEPRESSION** | Depression among adults | 18+ | 20.4% |
| **DISABILITY** | Any disability among adults | 18+ | 27.5% |

---

## Health Behaviors (4 measures)

| Measure | Definition | Age Group | National Rate |
|---------|------------|-----------|---------------|
| **BINGE** | Binge drinking among adults | 18+ | 16.8% |
| **CSMOKING** | Current smoking among adults | 18+ | 14.1% |
| **LPA** | No leisure-time physical activity | 18+ | 22.8% |
| **SLEEP** | Short sleep duration (<7 hours) | 18+ | 35.2% |

---

## Prevention (9 measures)

### Screenings

| Measure | Definition | Age Group | National Rate |
|---------|------------|-----------|---------------|
| **CERVICAL** | Cervical cancer screening (Pap) | Women 21-65 | 83.2% |
| **COLON_SCREEN** | Colorectal cancer screening | 50-75 | 72.4% |
| **MAMMOUSE** | Mammography use | Women 50-74 | 78.8% |
| **CHOLSCREEN** | Cholesterol screening | 18+ | 88.2% |

### Preventive Care

| Measure | Definition | Age Group | National Rate |
|---------|------------|-----------|---------------|
| **CHECKUP** | Annual checkup among adults | 18+ | 77.2% |
| **DENTAL** | Dental visit among adults | 18+ | 67.4% |
| **COREM** | Core preventive services - men | 65+ | 31.2% |
| **COREW** | Core preventive services - women | 65+ | 28.8% |
| **BPMED** | Taking BP medication | Adults w/HBP | 78.4% |

---

## Health Status (1 measure)

| Measure | Definition | Age Group | National Rate |
|---------|------------|-----------|---------------|
| **GHLTH** | Fair or poor self-rated health | 18+ | 17.8% |

---

## Age Adjustment

All measures are age-adjusted to the 2000 U.S. standard population:

| Age Group | Weight |
|-----------|--------|
| 18-24 | 0.128 |
| 25-34 | 0.183 |
| 35-44 | 0.198 |
| 45-54 | 0.192 |
| 55-64 | 0.148 |
| 65-74 | 0.089 |
| 75-84 | 0.044 |
| 85+ | 0.018 |

---

## Data Quality Indicators

### Confidence Intervals

All estimates include 95% confidence intervals. Reliability flags:

| Flag | Meaning | Action |
|------|---------|--------|
| None | Stable estimate | Use directly |
| * | Wide CI (>10 points) | Use with caution |
| ** | Suppressed | Use county-level |

### Minimum Population

| Geography | Minimum | Note |
|-----------|---------|------|
| County | 50 | All counties included |
| Tract | 50 | Some suppression |
| ZCTA | 50 | Higher suppression rate |

---

## Correlation Matrix (Selected Measures)

| Measure | DIABETES | OBESITY | BPHIGH | CHD | DEPRESSION |
|---------|----------|---------|--------|-----|------------|
| DIABETES | 1.00 | 0.72 | 0.68 | 0.54 | 0.42 |
| OBESITY | 0.72 | 1.00 | 0.64 | 0.48 | 0.38 |
| BPHIGH | 0.68 | 0.64 | 1.00 | 0.62 | 0.36 |
| CHD | 0.54 | 0.48 | 0.62 | 1.00 | 0.44 |
| DEPRESSION | 0.42 | 0.38 | 0.36 | 0.44 | 1.00 |

---

## API Access

**Base URL**: `https://data.cdc.gov/resource/`
**County Dataset**: `swc5-untb`
**Tract Dataset**: `cwsq-ngmh`

Example query:
```
https://data.cdc.gov/resource/swc5-untb.json?stateabbr=TX&countyfips=48201
```

---

## Related References

- [svi-variables.md](svi-variables.md) - Social vulnerability
- [acs-tables.md](acs-tables.md) - Demographics source
