# PopulationSim Data Package

This directory contains reference datasets for PopulationSim v2.0, providing real demographic, health, and social vulnerability data for 100% US coverage.

## Overview

| Category | Files | Records | Size |
|----------|-------|---------|------|
| County-level | 2 files | ~3,144 counties | ~5 MB |
| Tract-level | 2 files | ~84,000 tracts | ~122 MB |
| Block Group-level | 1 file | ~242,000 block groups | ~12 MB |
| Crosswalks | 4 files | Various | ~7 MB |
| **Total** | **9 files** | - | **~146 MB** |

## Data Sources & Vintages

| Dataset | Source | Vintage | Data Year | Geographic Level |
|---------|--------|---------|-----------|------------------|
| CDC PLACES | CDC Division of Population Health | 2024 Release | 2022 BRFSS | County, Tract |
| SVI | CDC/ATSDR GRASP | 2022 | 2018-2022 ACS | County, Tract |
| ADI | UW-Madison Neighborhood Atlas | 2023 v4.0.1 | 2019-2023 ACS | Block Group |
| Geography | US Census Bureau | 2023 | - | State, County, Tract, CBSA |

## Directory Structure

```
data/
├── README.md                    # This file
├── county/
│   ├── places_county_2024.csv   # CDC PLACES health measures (GIS-friendly format)
│   └── svi_county_2022.csv      # SVI aggregated from tract data
├── tract/
│   ├── places_tract_2024.csv    # CDC PLACES health measures (GIS-friendly format)
│   └── svi_tract_2022.csv       # CDC/ATSDR Social Vulnerability Index
├── block_group/
│   ├── adi_blockgroup_2023.csv  # Area Deprivation Index (Neighborhood Atlas)
│   └── adi_readme.txt           # ADI documentation from source
└── crosswalks/
    ├── fips_state.csv           # State FIPS codes
    ├── fips_county.csv          # County FIPS codes
    ├── tract_to_county.csv      # Tract to county mapping
    └── cbsa_definitions.csv     # Metropolitan/Micropolitan area definitions
```


## File Specifications

### County-Level Data

#### places_county_2024.csv
CDC PLACES 2024 Release - County-level health estimates in GIS-friendly format.

| Column | Description | Example |
|--------|-------------|---------|
| StateAbbr | State abbreviation | TX |
| StateDesc | State name | Texas |
| CountyName | County name | Harris County |
| CountyFIPS | 5-digit FIPS code | 48201 |
| TotalPopulation | Total population estimate | 4,731,145 |
| TotalPop18plus | Population 18+ | 3,622,890 |
| *_CrudePrev | Crude prevalence (%) | 12.1 |
| *_Crude95CI | 95% confidence interval | (11.8, 12.4) |
| *_AdjPrev | Age-adjusted prevalence (%) | 11.5 |
| *_Adj95CI | Age-adjusted 95% CI | (11.2, 11.8) |

**Health Measures (40 total):**

*Outcomes (12):*
- ARTHRITIS - Arthritis among adults
- BPHIGH - High blood pressure
- CANCER - Cancer (excluding skin)
- CASTHMA - Current asthma
- CHD - Coronary heart disease
- COPD - Chronic obstructive pulmonary disease
- DEPRESSION - Depression
- DIABETES - Diagnosed diabetes
- HIGHCHOL - High cholesterol
- KIDNEY - Chronic kidney disease
- OBESITY - Obesity
- STROKE - Stroke

*Prevention (7):*
- ACCESS2 - Lack of health insurance
- BPMED - Taking BP medication
- CHECKUP - Annual checkup
- CHOLSCREEN - Cholesterol screening
- COLON_SCREEN - Colorectal cancer screening
- COREM - Core preventive services (men)
- COREW - Core preventive services (women)

*Health Behaviors (4):*
- BINGE - Binge drinking
- CSMOKING - Current smoking
- LPA - No leisure-time physical activity
- SLEEP - Short sleep duration

*Disabilities (7):*
- DISABILITY - Any disability
- HEARING - Hearing disability
- VISION - Vision disability
- COGNITION - Cognitive disability
- MOBILITY - Mobility disability
- SELFCARE - Self-care disability
- INDEPLIVE - Independent living disability

*Health Status (3):*
- GHLTH - Fair or poor general health
- MHLTH - Mental health not good
- PHLTH - Physical health not good

*Social Needs (7):*
- FOODSTMP - Received SNAP
- HOUSING - Housing instability
- SOCIAL - Social isolation
- TRANSPORT - Lack of transportation
- UTILITIES - Utility bill difficulty
- FOOD - Food insecurity
- INTERNET - No internet access

#### svi_county_2022.csv
Social Vulnerability Index aggregated from tract-level data (population-weighted).

| Column | Description | Example |
|--------|-------------|---------|
| ST | State FIPS code | 48 |
| STATE | State name | Texas |
| ST_ABBR | State abbreviation | TX |
| STCNTY | 5-digit county FIPS | 48201 |
| COUNTY | County name | Harris County |
| AREA_SQMI | Area in square miles | 1,777.1 |
| E_TOTPOP | Total population | 4,731,145 |
| E_* | Estimate (count) | Various |
| EP_* | Percentage | Various |
| RPL_THEMES | Overall SVI (0-1) | 0.7823 |
| RPL_THEME1 | Socioeconomic Status (0-1) | 0.6542 |
| RPL_THEME2 | Household Characteristics (0-1) | 0.8134 |
| RPL_THEME3 | Racial/Ethnic Minority Status (0-1) | 0.8921 |
| RPL_THEME4 | Housing Type/Transportation (0-1) | 0.7012 |


### Tract-Level Data

#### places_tract_2024.csv
CDC PLACES 2024 Release - Census tract-level health estimates.

Same structure as county-level file with additional fields:
| Column | Description | Example |
|--------|-------------|---------|
| LocationID | Census tract FIPS (11-digit) | 48201211100 |
| LocationName | Tract description | Census Tract 2111, Harris County, Texas |

#### svi_tract_2022.csv
CDC/ATSDR Social Vulnerability Index - Full tract-level dataset (158 columns).

**Key Column Categories:**

| Prefix | Description | Example |
|--------|-------------|---------|
| ST, STATE, ST_ABBR | State identifiers | 48, Texas, TX |
| STCNTY, COUNTY | County identifiers | 48201, Harris County |
| FIPS | 11-digit tract FIPS | 48201211100 |
| E_* | Estimates (counts) | E_TOTPOP, E_POV150 |
| M_* | Margins of error | M_TOTPOP, M_POV150 |
| EP_* | Percentages | EP_POV150, EP_UNINSUR |
| MP_* | Percentage MOEs | MP_POV150, MP_UNINSUR |
| EPL_* | Percentile rankings (single variable) | EPL_POV150 |
| SPL_* | Sum of percentile rankings (theme) | SPL_THEME1 |
| RPL_* | Overall percentile ranking | RPL_THEMES |
| F_* | Flags (1=90th percentile) | F_POV150, F_THEME1 |

**SVI Themes:**
- **Theme 1 (Socioeconomic):** Below 150% poverty, Unemployed, Housing cost burden, No high school diploma, No health insurance
- **Theme 2 (Household Characteristics):** Aged 65+, Aged 17 and younger, Civilian with disability, Single-parent households, English language proficiency
- **Theme 3 (Racial/Ethnic Minority Status):** Racial/ethnic minority population
- **Theme 4 (Housing/Transportation):** Multi-unit structures, Mobile homes, Crowding, No vehicle, Group quarters


### Block Group-Level Data

#### adi_blockgroup_2023.csv
Area Deprivation Index from UW-Madison Neighborhood Atlas (v4.0.1) - Block group-level socioeconomic disadvantage rankings.

| Column | Description | Example |
|--------|-------------|---------|
| GISJOIN | NHGIS linkage key | G48020121110011 |
| FIPS | 12-digit block group FIPS | 482012111001 |
| ADI_NATRANK | National percentile (1-100) | 45 |
| ADI_STATERNK | State decile (1-10) | 3 |

**ADI Rankings:**
- **National Rank (1-100):** Percentile ranking compared to all US block groups. Higher = more disadvantaged.
- **State Rank (1-10):** Decile ranking within the state. Higher = more disadvantaged.

**Suppression Codes (instead of numeric values):**
| Code | Meaning |
|------|---------|
| GQ | >33.3% of housing units are group quarters |
| PH | Population <100 or <30 housing units |
| GQ-PH | Both GQ and PH conditions |
| QDI | Missing key demographic factor in ACS data |

**Coverage:** 242,336 block groups (all 50 states + DC + Puerto Rico)

**ADI Components (17 factors):**
- Income: Median family income, income disparity, % families below poverty, % population below 150% poverty
- Education: % population 25+ with <9 years education, % with <high school diploma
- Employment: % civilian labor force unemployed
- Housing Quality: Median home value, median gross rent, median monthly mortgage
- Housing Characteristics: % owner-occupied, % occupied units without complete plumbing, % occupied without telephone, % crowded (>1 person/room)
- Household: % single-parent households with children, % households without motor vehicle

### Crosswalk Files

#### fips_state.csv
State FIPS code reference (51 states/territories including DC).

| Column | Description | Example |
|--------|-------------|---------|
| state_fips | 2-digit FIPS code | 48 |
| state_name | Full state name | Texas |
| state_abbr | 2-letter abbreviation | TX |

#### fips_county.csv
County FIPS code reference (3,144 counties).

| Column | Description | Example |
|--------|-------------|---------|
| state_fips | 2-digit state FIPS | 48 |
| state_abbr | State abbreviation | TX |
| county_fips | 5-digit county FIPS | 48201 |
| county_name | County name | Harris County |

#### tract_to_county.csv
Tract to county mapping (84,120 tracts).

| Column | Description | Example |
|--------|-------------|---------|
| tract_fips | 11-digit tract FIPS | 48201211100 |
| county_fips | 5-digit county FIPS | 48201 |
| state_abbr | State abbreviation | TX |
| county_name | County name | Harris County |
| tract_name | Full tract description | Census Tract 2111; Harris County; Texas |

#### cbsa_definitions.csv
Metropolitan/Micropolitan Statistical Area definitions (1,918 county-CBSA mappings).

| Column | Description | Example |
|--------|-------------|---------|
| county_fips | 5-digit county FIPS | 48201 |
| state_fips | 2-digit state FIPS | 48 |
| state_name | State name | Texas |
| county_name | County name | Harris County |
| cbsa_code | 5-digit CBSA code | 26420 |
| cbsa_title | CBSA name | Houston-The Woodlands-Sugar Land, TX |
| cbsa_type | Metro or Micro | Metro |
| csa_code | Combined Statistical Area code | 288 |
| csa_title | CSA name | Houston-The Woodlands, TX |
| central_outlying | County role in CBSA | Central |


## Usage Examples

### Python - Load County Health Data
```python
import pandas as pd

# Load CDC PLACES county data
places = pd.read_csv('county/places_county_2024.csv')

# Find counties with highest diabetes prevalence
high_diabetes = places.nlargest(10, 'DIABETES_AdjPrev')[
    ['StateAbbr', 'CountyName', 'DIABETES_AdjPrev', 'OBESITY_AdjPrev']
]
```

### Python - Join SVI with PLACES
```python
# Load both datasets
svi = pd.read_csv('county/svi_county_2022.csv', dtype={'STCNTY': str})
places = pd.read_csv('county/places_county_2024.csv', dtype={'CountyFIPS': str})

# Join on county FIPS
merged = svi.merge(places, left_on='STCNTY', right_on='CountyFIPS')

# Analyze relationship between SVI and health outcomes
correlation = merged[['RPL_THEMES', 'DIABETES_AdjPrev', 'OBESITY_AdjPrev']].corr()
```

### SQL (DuckDB) - Query Tract Data
```sql
-- Load tract-level SVI
CREATE TABLE svi_tract AS 
SELECT * FROM read_csv_auto('tract/svi_tract_2022.csv');

-- Find high-vulnerability tracts in Texas
SELECT FIPS, LOCATION, RPL_THEMES, EP_POV150, EP_UNINSUR
FROM svi_tract
WHERE ST_ABBR = 'TX' AND RPL_THEMES > 0.9
ORDER BY RPL_THEMES DESC
LIMIT 20;
```

### SQL - Metropolitan Area Analysis
```sql
-- Join county data with CBSA definitions
SELECT 
    c.cbsa_title,
    c.cbsa_type,
    COUNT(*) as county_count,
    SUM(s.E_TOTPOP) as total_pop,
    AVG(s.RPL_THEMES) as avg_svi
FROM read_csv_auto('crosswalks/cbsa_definitions.csv') c
JOIN read_csv_auto('county/svi_county_2022.csv') s 
    ON c.county_fips = s.STCNTY
WHERE c.cbsa_type = 'Metro'
GROUP BY c.cbsa_code, c.cbsa_title, c.cbsa_type
ORDER BY total_pop DESC
LIMIT 20;
```


## Data Notes

### Missing Values
- **SVI:** Value of -999 indicates suppressed data (small population or unreliable estimate)
- **PLACES:** Empty cells or specific values indicate suppressed data per CDC rules

### Geographic Coverage
- **States:** All 50 states + DC (51 total)
- **Counties:** 3,144 counties (excludes some territories)
- **Tracts:** ~84,000 census tracts (2020 Census geography)
- **CBSA:** 937 Core-Based Statistical Areas (384 Metro + 553 Micro)

### Data Limitations
1. **Temporal alignment:** SVI uses 2018-2022 ACS; PLACES uses 2022 BRFSS. Minor temporal mismatches possible.
2. **Small area estimates:** Tract-level data has higher uncertainty than county-level.
3. **Model-based:** CDC PLACES uses small area estimation models, not direct survey data.
4. **SVI county aggregation:** County-level SVI was aggregated from tract data using population-weighted averages.

### FIPS Code Structure
```
State:  XX          (2 digits)
County: XXXXX       (5 digits = state + county)
Tract:  XXXXXXXXXXX (11 digits = state + county + tract)
```

## References

1. **CDC PLACES:** https://www.cdc.gov/places/
   - Methodology: https://www.cdc.gov/places/methodology/
   
2. **CDC/ATSDR SVI:** https://www.atsdr.cdc.gov/placeandhealth/svi/
   - Documentation: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/
   
3. **Census CBSA Delineations:** https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html

4. **Census FIPS Codes:** https://www.census.gov/library/reference/code-lists/ansi.html

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12 | Initial data package with PLACES 2024, SVI 2022 |

---
*Generated for PopulationSim v2.0 - Part of HealthSim Platform*
