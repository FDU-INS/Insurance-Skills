---
name: acs-tables
description: >
  Key American Community Survey table references for demographic and 
  socioeconomic data used in PopulationSim.
---

# ACS Table Reference

## Overview

The American Community Survey (ACS) is the primary source for demographic and socioeconomic data in PopulationSim. This reference covers the most commonly used tables.

**Source**: U.S. Census Bureau
**Estimates**: 1-year (larger areas), 5-year (all geographies)
**Update**: Annual
**Current**: ACS 2022 (1-year), ACS 2018-2022 (5-year)

---

## Table Naming Convention

| Prefix | Description | Example |
|--------|-------------|---------|
| B | Detailed tables | B01001 (Age/Sex) |
| C | Collapsed tables | C17002 (Poverty ratio) |
| S | Subject tables | S0101 (Age and Sex) |
| DP | Data profiles | DP02 (Social) |
| CP | Comparison profiles | CP02 (Social comparison) |

---

## Demographics

### Age and Sex

| Table | Title | Key Variables |
|-------|-------|---------------|
| **S0101** | Age and Sex | Total, by age group, median age |
| **B01001** | Sex by Age | Detailed 5-year age groups |
| **B01002** | Median Age by Sex | Median age M/F/Total |

**Key Variables from S0101**:
- `S0101_C01_001E` - Total population
- `S0101_C01_002E` - Under 5 years
- `S0101_C01_026E` - Median age (years)
- `S0101_C01_030E` - 65 years and over (percent)

### Race and Ethnicity

| Table | Title | Key Variables |
|-------|-------|---------------|
| **B03002** | Hispanic or Latino Origin by Race | Complete breakdown |
| **B02001** | Race | Single race categories |
| **DP05** | Demographics and Housing | Summary statistics |

**Key Variables from B03002**:
- `B03002_001E` - Total population
- `B03002_003E` - White alone, not Hispanic
- `B03002_004E` - Black or African American alone, not Hispanic
- `B03002_006E` - Asian alone, not Hispanic
- `B03002_012E` - Hispanic or Latino

---

## Economic Characteristics

### Income

| Table | Title | Key Variables |
|-------|-------|---------------|
| **S1901** | Income in Past 12 Months | Median, mean, distribution |
| **B19013** | Median Household Income | Single value |
| **B19001** | Household Income | Distribution buckets |

**Key Variables from S1901**:
- `S1901_C01_012E` - Median household income
- `S1901_C01_013E` - Mean household income

### Poverty

| Table | Title | Key Variables |
|-------|-------|---------------|
| **S1701** | Poverty Status | By age, sex, race |
| **C17002** | Ratio of Income to Poverty | Below 100%, 150%, 200% |
| **B17001** | Poverty by Sex by Age | Detailed breakdown |

**Key Variables from S1701**:
- `S1701_C03_001E` - Percent below poverty level
- `S1701_C03_002E` - Under 18 years, percent below poverty

### Employment

| Table | Title | Key Variables |
|-------|-------|---------------|
| **S2301** | Employment Status | Labor force, unemployment |
| **S2401** | Occupation by Sex | Occupation distribution |
| **S2403** | Industry by Sex | Industry distribution |

**Key Variables from S2301**:
- `S2301_C03_001E` - Unemployment rate (16+ years)
- `S2301_C02_001E` - Labor force participation rate

---

## Health Insurance

| Table | Title | Key Variables |
|-------|-------|---------------|
| **S2701** | Health Insurance Coverage | By type, age |
| **S2702** | Coverage by Work Experience | Work status detail |
| **S2704** | Coverage by Poverty | Income relationship |

**Key Variables from S2701**:
- `S2701_C03_001E` - Percent uninsured
- `S2701_C04_001E` - Percent with public coverage
- `S2701_C05_001E` - Percent with private coverage

---

## Education

| Table | Title | Key Variables |
|-------|-------|---------------|
| **S1501** | Educational Attainment | By age, sex |
| **B15003** | Educational Attainment | Detailed levels |
| **S1601** | Language Spoken at Home | English proficiency |

**Key Variables from S1501**:
- `S1501_C02_014E` - Percent bachelor's degree or higher
- `S1501_C02_009E` - Percent high school graduate or higher
- `S1501_C02_007E` - Percent less than 9th grade

---

## Housing

| Table | Title | Key Variables |
|-------|-------|---------------|
| **DP04** | Housing Characteristics | Comprehensive |
| **S2501** | Occupancy Characteristics | Tenure, vehicles |
| **B25003** | Tenure | Owner vs renter |

**Key Variables from DP04**:
- `DP04_0046PE` - Owner-occupied (percent)
- `DP04_0058PE` - No vehicle available (percent)
- `DP04_0134E` - Median gross rent
- `DP04_0089E` - Median home value

### Housing Cost Burden

| Table | Title | Key Variables |
|-------|-------|---------------|
| **B25070** | Gross Rent as % of Income | Renter burden |
| **B25091** | Mortgage as % of Income | Owner burden |

**Cost Burden Categories**:
- `< 20%` - Affordable
- `20-30%` - Cost pressured
- `30-50%` - Cost burdened
- `> 50%` - Severely burdened

---

## Disability

| Table | Title | Key Variables |
|-------|-------|---------------|
| **S1810** | Disability Characteristics | By type, age |
| **B18101** | Sex by Age by Disability | Detailed |

**Disability Types**:
- Hearing difficulty
- Vision difficulty
- Cognitive difficulty
- Ambulatory difficulty
- Self-care difficulty
- Independent living difficulty

---

## Geographic Coverage

| Geography | 1-Year ACS | 5-Year ACS |
|-----------|------------|------------|
| Nation | ✓ | ✓ |
| State | ✓ (pop ≥65K) | ✓ |
| County | ✓ (pop ≥65K) | ✓ |
| Place | ✓ (pop ≥65K) | ✓ |
| Tract | - | ✓ |
| Block Group | - | ✓ |
| ZCTA | - | ✓ |

---

## API Access

**Base URL**: `https://api.census.gov/data/`
**Example** (2022 5-year, median income by county):
```
https://api.census.gov/data/2022/acs/acs5?get=NAME,S1901_C01_012E&for=county:*&in=state:48
```

**API Key**: Register at https://api.census.gov/data/key_signup.html

---

## Related References

- [fips-codes.md](fips-codes.md) - Geographic identifiers
- [svi-variables.md](svi-variables.md) - SVI uses ACS data
- [cdc-places-measures.md](cdc-places-measures.md) - Health data comparison
