---
name: svi-variables
description: >
  Complete reference for CDC/ATSDR Social Vulnerability Index 16 variables
  across 4 themes with definitions, data sources, and scoring methodology.
---

# CDC/ATSDR Social Vulnerability Index Variables

## Overview

The Social Vulnerability Index (SVI) uses 16 U.S. Census variables to identify communities that may need support before, during, or after disasters. Variables are grouped into 4 themes and combined into an overall vulnerability score.

**Source**: CDC/ATSDR Geospatial Research, Analysis & Services Program (GRASP)
**Geography**: County, Census Tract
**Update Frequency**: Biennial (based on ACS 5-year estimates)
**Current Version**: SVI 2022 (ACS 2018-2022)

---

## Embedded Data Files (v2.0)

| Level | File | Records |
|-------|------|---------|
| County | `data/county/svi_county_2022.csv` | 3,144 |
| Tract | `data/tract/svi_tract_2022.csv` | 84,120 |

### Column Naming Convention

**Estimate Columns (E_*):** Raw counts
- `E_TOTPOP`: Total population
- `E_POV150`: Persons below 150% poverty
- `E_UNINSUR`: Uninsured persons

**Percentage Columns (EP_*):** Percentages
- `EP_POV150`: % below 150% poverty
- `EP_UNINSUR`: % uninsured

**Ranking Columns (RPL_*):** Percentile rankings (0-1, higher = more vulnerable)
- `RPL_THEMES`: Overall SVI ranking
- `RPL_THEME1`: Socioeconomic Status ranking
- `RPL_THEME2`: Household Characteristics ranking
- `RPL_THEME3`: Minority/Language ranking
- `RPL_THEME4`: Housing/Transportation ranking

**Geography Columns:**
- `ST_ABBR`: State abbreviation
- `STCNTY`: 5-digit county FIPS
- `FIPS`: 11-digit tract FIPS (tract file only)
- `COUNTY`: County name

**Missing Values:** -999 indicates suppressed/unavailable data

---

## Theme 1: Socioeconomic Status

| Variable | Definition | ACS Table | National Mean |
|----------|------------|-----------|---------------|
| **E_POV150** | Persons below 150% poverty | S1701 | 20.8% |
| **E_UNEMP** | Civilian unemployed (16+) | S2301 | 5.4% |
| **E_HBURD** | Housing cost burden (>30% income) | DP04 | 28.2% |
| **E_NOHSDP** | No high school diploma (25+) | S1501 | 11.1% |
| **E_UNINSUR** | No health insurance | S2701 | 8.8% |

**Theme 1 Interpretation**:
- High scores indicate economic disadvantage
- Strongest predictor of health outcomes
- Correlates with healthcare access barriers

---

## Theme 2: Household Characteristics

| Variable | Definition | ACS Table | National Mean |
|----------|------------|-----------|---------------|
| **E_AGE65** | Persons aged 65 and older | S0101 | 16.8% |
| **E_AGE17** | Persons aged 17 and younger | S0101 | 21.4% |
| **E_DISABL** | Civilian noninstitutionalized with disability | S1810 | 12.8% |
| **E_SNGPNT** | Single-parent households with children | S1101 | 8.2% |
| **E_LIMENG** | Limited English proficiency (5+) | S1601 | 4.2% |

**Theme 2 Interpretation**:
- Captures household composition vulnerability
- Age extremes require special assistance
- Disability and language barriers affect evacuation

---

## Theme 3: Racial & Ethnic Minority Status

| Variable | Definition | ACS Table | National Mean |
|----------|------------|-----------|---------------|
| **E_MINRTY** | Minority (all except White non-Hispanic) | B03002 | 40.6% |
| **E_LIMENG** | Limited English proficiency | S1601 | 4.2% |

**Theme 3 Interpretation**:
- Historical discrimination and marginalization
- Language barriers to emergency communication
- Often overlaps with economic vulnerability

*Note: E_LIMENG appears in both Theme 2 and Theme 3*

---

## Theme 4: Housing Type & Transportation

| Variable | Definition | ACS Table | National Mean |
|----------|------------|-----------|---------------|
| **E_MUNIT** | Multi-unit structures (10+ units) | DP04 | 8.4% |
| **E_MOBILE** | Mobile homes | DP04 | 5.8% |
| **E_CROWD** | Crowded housing (>1 person/room) | DP04 | 2.8% |
| **E_NOVEH** | No vehicle available | DP04 | 8.2% |
| **E_GROUPQ** | Group quarters population | B26001 | 2.4% |

**Theme 4 Interpretation**:
- Housing type affects disaster vulnerability
- Mobile homes vulnerable to wind/tornado
- No vehicle impedes evacuation

---

## Scoring Methodology

### Percentile Ranking

Each variable is ranked as a percentile (0-1):
- 0.00 = lowest vulnerability (least vulnerable)
- 1.00 = highest vulnerability (most vulnerable)

### Theme Scores

Theme scores are the sum of percentile rankings for component variables, then ranked as percentiles:

```
Theme1_Percentile = Rank(E_POV150 + E_UNEMP + E_HBURD + E_NOHSDP + E_UNINSUR)
```

### Overall SVI

Overall SVI is the sum of all 16 variable percentiles, then ranked:

```
Overall_SVI = Rank(Σ all 16 variable percentiles)
```

---

## Interpretation Guide

| SVI Range | Vulnerability | Population % |
|-----------|---------------|--------------|
| 0.00-0.25 | Low | 25% |
| 0.25-0.50 | Low-Moderate | 25% |
| 0.50-0.75 | Moderate-High | 25% |
| 0.75-1.00 | High | 25% |

### Flag System

SVI also provides flags for extreme vulnerability:
- **0** = Below 90th percentile
- **1** = At or above 90th percentile (top 10%)

---

## Theme Correlations

| Theme | Theme 1 | Theme 2 | Theme 3 | Theme 4 |
|-------|---------|---------|---------|---------|
| Theme 1 (Socioeconomic) | 1.00 | 0.52 | 0.48 | 0.62 |
| Theme 2 (Household) | 0.52 | 1.00 | 0.42 | 0.38 |
| Theme 3 (Minority) | 0.48 | 0.42 | 1.00 | 0.56 |
| Theme 4 (Housing) | 0.62 | 0.38 | 0.56 | 1.00 |

---

## Data Quality Notes

### Suppression

Variables may be suppressed for small populations:
- Tracts with <50 population
- High margin of error estimates

### Margin of Error

ACS estimates include margins of error. For small tracts:
- CV (coefficient of variation) > 30% indicates unreliable
- Consider aggregating to county level

---

## Mapping to SDOH Z-Codes

| SVI Variable | Primary Z-Code | Secondary Z-Codes |
|--------------|----------------|-------------------|
| E_POV150 | Z59.6 (Low income) | Z59.41, Z59.7 |
| E_UNEMP | Z56.0 (Unemployment) | Z56.9 |
| E_NOHSDP | Z55.9 (Education problem) | Z55.0 |
| E_UNINSUR | Z59.7 (Insufficient insurance) | - |
| E_DISABL | Z73.6 (Limitation of activities) | - |
| E_LIMENG | Z60.3 (Acculturation difficulty) | - |
| E_NOVEH | Z59.82 (Transportation insecurity) | - |
| E_CROWD | Z59.1 (Inadequate housing) | - |
| E_MOBILE | Z59.1 (Inadequate housing) | - |

---

## Access

**Download**: https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html
**Interactive Map**: https://www.atsdr.cdc.gov/placeandhealth/svi/interactive_map.html
**API**: Available via CDC WONDER

---

## Related References

- [adi-analysis.md](../sdoh/adi-analysis.md) - Alternative deprivation measure
- [cdc-places-measures.md](cdc-places-measures.md) - Health outcomes
- [icd10-sdoh-codes.md](icd10-sdoh-codes.md) - Z-code mapping
