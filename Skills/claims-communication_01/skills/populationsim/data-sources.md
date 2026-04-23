---
name: populationsim-data-sources
description: |
  Reference documentation for PopulationSim data sources including Census ACS, 
  CDC PLACES, SVI, ADI, and other public health data. Use this to understand 
  data provenance, vintage, and quality characteristics.
---

# PopulationSim Data Sources

## Overview

PopulationSim synthesizes data from multiple authoritative public health and demographic sources to generate realistic population profiles. This document describes each data source, its characteristics, and how it's used.

---

## Primary Data Sources

### 1. American Community Survey (ACS)

**Source**: U.S. Census Bureau  
**URL**: https://www.census.gov/programs-surveys/acs  
**Update Frequency**: Annual (5-year estimates released December)

#### Products Used

| Product | Geographic Coverage | Reliability |
|---------|---------------------|-------------|
| ACS 5-Year | All areas including tracts | Highest for small areas |
| ACS 1-Year | Areas ≥65,000 population | More current |

#### Variables Used

| Category | Key Variables | ACS Table |
|----------|---------------|-----------|
| Total Population | Total count | B01003 |
| Age | Age by sex | B01001 |
| Sex | Male/female | B01001 |
| Race | Race categories | B02001 |
| Ethnicity | Hispanic/Latino | B03003 |
| Income | Median household income | B19013 |
| Poverty | Below poverty level | B17001 |
| Employment | Labor force status | B23025 |
| Education | Educational attainment | B15003 |
| Insurance | Coverage by type | B27001-B27010 |
| Housing | Tenure, value, rent | B25003, B25077 |
| Transportation | Vehicles, commute | B25044, B08301 |

#### PopulationSim Usage

- Demographic distributions in PopulationProfile
- Household composition
- Economic factors in SDOHProfile
- Insurance coverage baseline

---

### 2. CDC PLACES

**Source**: Centers for Disease Control and Prevention  
**URL**: https://www.cdc.gov/places  
**Update Frequency**: Annual (data typically 2 years prior)

#### Coverage

| Geography | Availability |
|-----------|--------------|
| County | All US counties |
| Place/City | All incorporated places |
| Census Tract | All tracts |
| ZCTA | All ZCTAs |

#### Measures

| Category | Measures |
|----------|----------|
| Health Outcomes (13) | Arthritis, High BP, Cancer, Asthma, CHD, COPD, Depression, Diabetes, High Cholesterol, CKD, Obesity, Stroke, Tooth Loss |
| Prevention (9) | BP Meds, Cervical Screen, Checkup, Cholesterol Screen, Colon Screen, Core Preventive (M/F), Dental, Mammogram |
| Health Behaviors (4) | Binge Drinking, Smoking, Physical Inactivity, Sleep |
| Health Status (3) | Mental Health Days, Physical Health Days, General Health |

#### Methodology

- Model-based small area estimation
- Multilevel regression and poststratification (MRP)
- BRFSS survey data as input

#### PopulationSim Usage

- Health indicator prevalence in PopulationProfile
- Condition rates for cohort generation
- Health behavior baselines

---

### 3. CDC/ATSDR Social Vulnerability Index (SVI)

**Source**: CDC Agency for Toxic Substances and Disease Registry  
**URL**: https://www.atsdr.cdc.gov/placeandhealth/svi  
**Update Frequency**: Biennial

#### Structure

| Theme | Variables |
|-------|-----------|
| Theme 1: Socioeconomic | Below poverty, Unemployed, Per capita income, No HS diploma |
| Theme 2: Household Composition & Disability | Age 65+, Age 17-, Disability, Single parent |
| Theme 3: Minority Status & Language | Minority, Limited English |
| Theme 4: Housing Type & Transportation | Multi-unit, Mobile home, Crowding, No vehicle, Group quarters |

#### Calculation

1. Calculate percentile rank for each variable (tract vs. all US tracts)
2. Sum percentile ranks within each theme
3. Calculate percentile rank for each theme sum
4. Sum all variable percentiles for overall SVI
5. Calculate percentile rank for overall score

#### Output Scores

| Score Type | Range | Interpretation |
|------------|-------|----------------|
| RPL_THEME1-4 | 0-1 | Theme percentile |
| RPL_THEMES | 0-1 | Overall percentile |
| F_PLxx | 0 or 1 | Flag if ≥90th percentile |

#### PopulationSim Usage

- SVI scores in SDOHProfile
- Vulnerability-based cohort filtering
- Z-code prevalence estimation

---

### 4. Area Deprivation Index (ADI)

**Source**: University of Wisconsin School of Medicine and Public Health  
**URL**: https://www.neighborhoodatlas.medicine.wisc.edu  
**Update Frequency**: Annual

#### Structure

| Domain | Variables |
|--------|-----------|
| Income | Median family income, income disparity, home value, rent, mortgage |
| Poverty | Below 150% FPL, single-parent, public assistance |
| Education | No HS diploma, HS or higher |
| Employment | Unemployment, not in labor force |
| Housing Quality | Crowding, no vehicle, no telephone, no plumbing, no kitchen |

#### Scores

| Score | Range | Description |
|-------|-------|-------------|
| National Percentile | 1-100 | Rank vs. all US block groups |
| State Decile | 1-10 | Rank within state |

#### Geographic Level

- Block group (12-digit FIPS) - most granular available
- Can aggregate to tract or county

#### PopulationSim Usage

- ADI scores in SDOHProfile
- Fine-grained deprivation analysis
- Healthcare access modeling

---

### 5. USDA Food Access Research Atlas

**Source**: USDA Economic Research Service  
**URL**: https://www.ers.usda.gov/data-products/food-access-research-atlas  
**Update Frequency**: Periodic (every 3-5 years)

#### Key Variables

| Variable | Definition |
|----------|------------|
| Low Access | >1 mile (urban) or >10 miles (rural) to supermarket |
| Low Income + Low Access | Low access + poverty rate ≥20% |
| SNAP Retailers | SNAP-authorized stores per capita |

#### PopulationSim Usage

- Food insecurity indicators
- Food desert classification
- Z59.41 prevalence estimation

---

## Secondary Data Sources

### 6. HRSA Health Professional Shortage Areas (HPSA)

**Source**: Health Resources and Services Administration  
**URL**: https://data.hrsa.gov/topics/health-workforce/shortage-areas

#### Designation Types

| Type | Description |
|------|-------------|
| Primary Care HPSA | PCP shortage |
| Dental HPSA | Dentist shortage |
| Mental Health HPSA | Mental health provider shortage |

#### PopulationSim Usage

- Healthcare access indicators
- Provider availability metrics

---

### 7. Census TIGER/Line Shapefiles

**Source**: U.S. Census Bureau  
**URL**: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

#### Uses

- Geographic boundary definitions
- FIPS code reference
- Urban/rural classification
- CBSA/MSA definitions

---

### 8. OMB Metropolitan Delineations

**Source**: Office of Management and Budget  
**URL**: https://www.census.gov/programs-surveys/metro-micro.html

#### Definitions

| Type | Population | Example |
|------|------------|---------|
| Metropolitan (Metro) | ≥50,000 | Houston-The Woodlands-Sugar Land |
| Micropolitan (Micro) | 10,000-49,999 | College Station-Bryan |

---

## Data Vintage and Freshness

### Current Default Vintages

| Source | Data Year | Release Year |
|--------|-----------|--------------|
| ACS 5-Year | 2018-2022 | 2023 |
| CDC PLACES | 2022 | 2024 |
| SVI | 2022 | 2024 |
| ADI | 2021 | 2023 |
| Food Access | 2019 | 2021 |

### Lag Considerations

- ACS: 1-2 year lag from reference period end
- PLACES: ~2 year lag from BRFSS survey
- SVI: Based on ACS vintage
- ADI: Based on ACS vintage

---

## Data Quality Notes

### ACS Margin of Error

- All ACS estimates have associated MOE
- Small populations have larger MOE
- 5-year estimates more reliable than 1-year

### PLACES Modeled Estimates

- Not direct measurements
- Based on BRFSS survey + demographic modeling
- Most reliable at county level
- Tract estimates have higher uncertainty

### SVI/ADI Percentile Interpretation

- Relative rankings, not absolute measures
- Compare within same vintage
- National percentile vs. state rankings differ

---

## API Access

### Census API

```
Base URL: https://api.census.gov/data/
Example: https://api.census.gov/data/2022/acs/acs5?get=B01001_001E&for=county:201&in=state:48
```

### CDC PLACES API

```
Base URL: https://data.cdc.gov/resource/
Example: https://data.cdc.gov/resource/swc5-untb.json?locationabbr=TX
```

### SVI Data

- Available as downloadable CSV/shapefiles
- No public API

### ADI Data

- Available through Neighborhood Atlas download
- Registration required

---

## Related Documentation

- [Census Variables Reference](../../references/census-variables.md)
- [CDC PLACES Indicators](../../references/cdc-places-indicators.md)
- [SVI Methodology](../../references/svi-methodology.md)
- [ADI Methodology](../../references/adi-methodology.md)
- [Geography Codes](../../references/geography-codes.md)
