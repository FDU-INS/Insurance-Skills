---
name: data-sources
description: >
  Consolidated reference for all PopulationSim v2.0 embedded data sources
  including file locations, schemas, vintages, and citation requirements.
---

# PopulationSim Data Sources Reference

## Overview

PopulationSim v2.0 includes an embedded data package (148 MB) with real-world demographic, health, and SDOH data covering 100% of US geography. This reference documents all data sources, their structure, and proper citation.

---

## Data Package Summary

| Dataset | Level | File | Records | Size | Source |
|---------|-------|------|---------|------|--------|
| CDC PLACES 2024 | County | `data/county/places_county_2024.csv` | 3,143 | 4.8 MB | CDC |
| CDC PLACES 2024 | Tract | `data/tract/places_tract_2024.csv` | 83,522 | 67 MB | CDC |
| CDC SVI 2022 | County | `data/county/svi_county_2022.csv` | 3,144 | 0.4 MB | CDC/ATSDR |
| CDC SVI 2022 | Tract | `data/tract/svi_tract_2022.csv` | 84,120 | 61 MB | CDC/ATSDR |
| ADI 2023 | Block Group | `data/block_group/adi_blockgroup_2023.csv` | 242,336 | 12 MB | UW-Madison |
| State FIPS | Crosswalk | `data/crosswalks/fips_state.csv` | 51 | <1 KB | Census |
| County FIPS | Crosswalk | `data/crosswalks/fips_county.csv` | 3,144 | 0.2 MB | Census |
| Tract-to-County | Crosswalk | `data/crosswalks/tract_to_county.csv` | 84,120 | 4 MB | Census |
| CBSA Definitions | Crosswalk | `data/crosswalks/cbsa_definitions.csv` | 1,918 | 0.2 MB | OMB/Census |

**Total Size:** 148 MB

---

## CDC PLACES 2024

### Description
Model-based estimates for 40 health measures at county and census tract levels using multilevel regression and poststratification (MRP) on BRFSS data.

### Data Vintage
- **Release Year:** 2024
- **Base Data:** 2022 BRFSS
- **Geography Base:** 2020 Census boundaries

### Files
- County: `data/county/places_county_2024.csv`
- Tract: `data/tract/places_tract_2024.csv`

### Key Columns
| Column Pattern | Description | Example |
|----------------|-------------|---------|
| StateAbbr | State abbreviation | TX |
| CountyName | County name | Harris |
| CountyFIPS | 5-digit FIPS | 48201 |
| TotalPopulation | Population 18+ | 4835125 |
| [MEASURE]_CrudePrev | Crude prevalence (%) | DIABETES_CrudePrev |
| [MEASURE]_AdjPrev | Age-adjusted prevalence | DIABETES_AdjPrev |

### Available Measures (40)
**Health Outcomes:** DIABETES, OBESITY, BPHIGH, HIGHCHOL, CHD, STROKE, COPD, CASTHMA, CANCER, KIDNEY, ARTHRITIS, DEPRESSION

**Health Behaviors:** CSMOKING, BINGE, LPA, SLEEP

**Prevention:** CHECKUP, DENTAL, CHOLSCREEN, COLON_SCREEN, MAMMOUSE

**Disabilities:** HEARING, VISION, COGNITION, MOBILITY, SELFCARE, INDEPLIVE, DISABILITY

**Health Status:** GHLTH, MHLTH, PHLTH

**Social Needs:** FOODINSECU, HOUSINSECU, LACKTRPT, SHUTUTILITY

### Citation
```
Centers for Disease Control and Prevention. PLACES: Local Data for Better Health. 
County/Tract Data 2024 Release. https://www.cdc.gov/places
```

---

## CDC/ATSDR SVI 2022

### Description
Social Vulnerability Index ranking 16 Census variables across 4 themes to identify communities needing support during emergencies.

### Data Vintage
- **Release Year:** 2024
- **Base Data:** ACS 2018-2022 5-year estimates
- **Geography Base:** 2020 Census boundaries

### Files
- County: `data/county/svi_county_2022.csv`
- Tract: `data/tract/svi_tract_2022.csv`

### Key Columns
| Column Pattern | Description | Example |
|----------------|-------------|---------|
| ST_ABBR | State abbreviation | TX |
| STCNTY | 5-digit county FIPS | 48201 |
| FIPS | 11-digit tract FIPS | 48201311500 |
| E_TOTPOP | Total population | 4521 |
| E_* | Estimate (count) | E_POV150 |
| EP_* | Percentage | EP_POV150 |
| RPL_THEMES | Overall SVI (0-1) | 0.82 |
| RPL_THEME1-4 | Theme rankings | 0.75 |

### SVI Themes
1. **Socioeconomic Status:** POV150, UNEMP, HBURD, NOHSDP, UNINSUR
2. **Household Characteristics:** AGE65, AGE17, DISABL, SNGPNT, LIMENG
3. **Minority/Language:** MINRTY, LIMENG
4. **Housing/Transportation:** MUNIT, MOBILE, CROWD, NOVEH, GROUPQ

### Citation
```
Centers for Disease Control and Prevention/Agency for Toxic Substances and Disease Registry.
CDC/ATSDR Social Vulnerability Index 2022. https://www.atsdr.cdc.gov/placeandhealth/svi/
```

---

## Neighborhood Atlas ADI 2023

### Description
Area Deprivation Index measuring neighborhood socioeconomic disadvantage at block group level using 17 Census variables.

### Data Vintage
- **Version:** 2023 v4.0.1
- **Base Data:** ACS 2019-2023 5-year estimates
- **Geography Base:** 2020 Census boundaries

### File
- `data/block_group/adi_blockgroup_2023.csv`

### Columns
| Column | Description | Values |
|--------|-------------|--------|
| FIPS | 12-digit block group FIPS | 482012104001 |
| ADI_NATRANK | National percentile | 1-100 |
| ADI_STATERNK | State decile | 1-10 |

### Suppression Codes
| Code | Meaning |
|------|---------|
| GQ | >33% group quarters population |
| PH | Population <100 or <30 housing units |
| GQ-PH | Both conditions |
| QDI | Missing key demographic factor |

### Citation
```
University of Wisconsin School of Medicine and Public Health. 
Neighborhood Atlas - Area Deprivation Index v4.0.1 (2023).
https://www.neighborhoodatlas.medicine.wisc.edu/
```

---

## Geography Crosswalks

### State FIPS
- **File:** `data/crosswalks/fips_state.csv`
- **Columns:** state_fips, state_name, state_abbr
- **Records:** 51

### County FIPS
- **File:** `data/crosswalks/fips_county.csv`
- **Columns:** state_fips, state_abbr, county_fips, county_name
- **Records:** 3,144

### Tract to County
- **File:** `data/crosswalks/tract_to_county.csv`
- **Columns:** tract_fips, county_fips, state_abbr, county_name, tract_name
- **Records:** 84,120

### CBSA Definitions
- **File:** `data/crosswalks/cbsa_definitions.csv`
- **Columns:** county_fips, cbsa_code, cbsa_title, cbsa_type, central_outlying
- **Records:** 1,918 (county-CBSA mappings for 937 unique CBSAs)
- **Source:** OMB Bulletin No. 23-01 (July 2023)

---

## Data Provenance Requirements

**All responses using embedded data must include:**
1. Source name (CDC PLACES, CDC SVI, ADI)
2. Data vintage (year)
3. Geography identifier (FIPS code)

### Example Citation Format

**Prose:**
> Harris County, TX has a diabetes prevalence of 13.2%.
> *Source: CDC PLACES 2024 Release (2022 BRFSS data)*

**JSON:**
```json
{
  "value": 13.2,
  "source": "CDC PLACES 2024",
  "data_year": "2022 BRFSS",
  "geography_fips": "48201"
}
```

---

## Related References

- [cdc-places-measures.md](cdc-places-measures.md) - Complete PLACES measure definitions
- [svi-variables.md](svi-variables.md) - SVI variable details
- [fips-codes.md](fips-codes.md) - FIPS code structure
- [../data/README.md](../data/README.md) - Full data package documentation
