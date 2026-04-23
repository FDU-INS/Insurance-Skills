# Census Variables Reference

## Overview

This reference documents American Community Survey (ACS) variables used by PopulationSim for demographic, economic, and housing analysis. Variables are organized by subject area with their codes, definitions, and typical use cases.

---

## ACS Data Products

| Product | Coverage | Sample Size | Use Case |
|---------|----------|-------------|----------|
| ACS 1-Year | Areas ≥65,000 pop | ~3.5M/year | Current estimates, large areas |
| ACS 5-Year | All areas | ~3.5M/year × 5 | Small area estimates, tracts |

**PopulationSim Default**: ACS 5-Year estimates for tract/block group analysis

---

## Variable Naming Convention

ACS variables follow a structured naming pattern:

```
{Table}_{Column}_{Estimate Type}
Example: B01001_001E

Where:
- B01001 = Table ID (Sex by Age)
- 001 = Column number
- E = Estimate (M = Margin of Error)
```

### Table Prefixes

| Prefix | Description |
|--------|-------------|
| B | Base/Detailed tables |
| C | Collapsed tables (fewer categories) |
| S | Subject tables (percentages) |
| DP | Data Profile tables |
| CP | Comparison Profile tables |

---

## Demographics

### Total Population (B01003)

| Variable | Description |
|----------|-------------|
| B01003_001E | Total population |

### Sex by Age (B01001)

| Variable | Description |
|----------|-------------|
| B01001_001E | Total |
| B01001_002E | Male |
| B01001_003E | Male: Under 5 years |
| B01001_004E | Male: 5 to 9 years |
| B01001_005E | Male: 10 to 14 years |
| B01001_006E | Male: 15 to 17 years |
| B01001_007E | Male: 18 and 19 years |
| B01001_008E | Male: 20 years |
| B01001_009E | Male: 21 years |
| B01001_010E | Male: 22 to 24 years |
| B01001_011E | Male: 25 to 29 years |
| B01001_012E | Male: 30 to 34 years |
| B01001_013E | Male: 35 to 39 years |
| B01001_014E | Male: 40 to 44 years |
| B01001_015E | Male: 45 to 49 years |
| B01001_016E | Male: 50 to 54 years |
| B01001_017E | Male: 55 to 59 years |
| B01001_018E | Male: 60 and 61 years |
| B01001_019E | Male: 62 to 64 years |
| B01001_020E | Male: 65 and 66 years |
| B01001_021E | Male: 67 to 69 years |
| B01001_022E | Male: 70 to 74 years |
| B01001_023E | Male: 75 to 79 years |
| B01001_024E | Male: 80 to 84 years |
| B01001_025E | Male: 85 years and over |
| B01001_026E | Female |
| B01001_027E-049E | Female age categories (same pattern) |

### Median Age (B01002)

| Variable | Description |
|----------|-------------|
| B01002_001E | Median age (total) |
| B01002_002E | Median age (male) |
| B01002_003E | Median age (female) |

### Race (B02001)

| Variable | Description |
|----------|-------------|
| B02001_001E | Total |
| B02001_002E | White alone |
| B02001_003E | Black or African American alone |
| B02001_004E | American Indian and Alaska Native alone |
| B02001_005E | Asian alone |
| B02001_006E | Native Hawaiian and Other Pacific Islander alone |
| B02001_007E | Some other race alone |
| B02001_008E | Two or more races |

### Hispanic or Latino Origin (B03003)

| Variable | Description |
|----------|-------------|
| B03003_001E | Total |
| B03003_002E | Not Hispanic or Latino |
| B03003_003E | Hispanic or Latino |

### Race/Ethnicity Combined (B03002)

| Variable | Description |
|----------|-------------|
| B03002_001E | Total |
| B03002_003E | White alone, not Hispanic |
| B03002_004E | Black alone, not Hispanic |
| B03002_005E | AIAN alone, not Hispanic |
| B03002_006E | Asian alone, not Hispanic |
| B03002_007E | NHPI alone, not Hispanic |
| B03002_008E | Some other race, not Hispanic |
| B03002_009E | Two or more races, not Hispanic |
| B03002_012E | Hispanic or Latino (any race) |

---

## Economic Characteristics

### Household Income (B19001)

| Variable | Description |
|----------|-------------|
| B19001_001E | Total households |
| B19001_002E | Less than $10,000 |
| B19001_003E | $10,000 to $14,999 |
| B19001_004E | $15,000 to $19,999 |
| B19001_005E | $20,000 to $24,999 |
| B19001_006E | $25,000 to $29,999 |
| B19001_007E | $30,000 to $34,999 |
| B19001_008E | $35,000 to $39,999 |
| B19001_009E | $40,000 to $44,999 |
| B19001_010E | $45,000 to $49,999 |
| B19001_011E | $50,000 to $59,999 |
| B19001_012E | $60,000 to $74,999 |
| B19001_013E | $75,000 to $99,999 |
| B19001_014E | $100,000 to $124,999 |
| B19001_015E | $125,000 to $149,999 |
| B19001_016E | $150,000 to $199,999 |
| B19001_017E | $200,000 or more |

### Median Household Income (B19013)

| Variable | Description |
|----------|-------------|
| B19013_001E | Median household income |

### Per Capita Income (B19301)

| Variable | Description |
|----------|-------------|
| B19301_001E | Per capita income |

### Poverty Status (B17001)

| Variable | Description |
|----------|-------------|
| B17001_001E | Total population for poverty determination |
| B17001_002E | Income below poverty level |

### Poverty Rate (S1701)

| Variable | Description |
|----------|-------------|
| S1701_C03_001E | Percent below poverty level |

### Employment Status (B23025)

| Variable | Description |
|----------|-------------|
| B23025_001E | Total population 16+ |
| B23025_002E | In labor force |
| B23025_003E | Civilian labor force |
| B23025_004E | Employed |
| B23025_005E | Unemployed |
| B23025_006E | Armed Forces |
| B23025_007E | Not in labor force |

### Unemployment Rate

Calculated: `B23025_005E / B23025_003E × 100`

---

## Education

### Educational Attainment (B15003)

| Variable | Description |
|----------|-------------|
| B15003_001E | Total population 25+ |
| B15003_002E | No schooling completed |
| B15003_003E-016E | Grades 1-12 (no diploma) |
| B15003_017E | Regular high school diploma |
| B15003_018E | GED or alternative credential |
| B15003_019E | Some college, less than 1 year |
| B15003_020E | Some college, 1 or more years, no degree |
| B15003_021E | Associate's degree |
| B15003_022E | Bachelor's degree |
| B15003_023E | Master's degree |
| B15003_024E | Professional school degree |
| B15003_025E | Doctorate degree |

### Key Education Aggregations

| Metric | Calculation |
|--------|-------------|
| No HS diploma | Sum(B15003_002E:B15003_016E) / B15003_001E |
| HS or higher | Sum(B15003_017E:B15003_025E) / B15003_001E |
| Bachelor's or higher | Sum(B15003_022E:B15003_025E) / B15003_001E |

---

## Health Insurance (B27001)

### Coverage by Age

| Variable | Description |
|----------|-------------|
| B27001_001E | Total civilian noninstitutionalized population |
| B27001_004E | Under 6: With health insurance |
| B27001_005E | Under 6: No health insurance |
| B27001_007E | 6-18: With health insurance |
| B27001_008E | 6-18: No health insurance |
| B27001_010E | 19-25: With health insurance |
| B27001_011E | 19-25: No health insurance |
| B27001_013E | 26-34: With health insurance |
| B27001_014E | 26-34: No health insurance |
| B27001_016E | 35-44: With health insurance |
| B27001_017E | 35-44: No health insurance |
| B27001_019E | 45-54: With health insurance |
| B27001_020E | 45-54: No health insurance |
| B27001_022E | 55-64: With health insurance |
| B27001_023E | 55-64: No health insurance |
| B27001_025E | 65-74: With health insurance |
| B27001_026E | 65-74: No health insurance |
| B27001_028E | 75+: With health insurance |
| B27001_029E | 75+: No health insurance |

### Insurance Type (B27010)

| Variable | Description |
|----------|-------------|
| B27010_001E | Total |
| B27010_003E | With employer-based coverage |
| B27010_010E | With direct-purchase coverage |
| B27010_017E | With Medicare |
| B27010_024E | With Medicaid/means-tested |
| B27010_031E | With TRICARE/VA |

---

## Housing

### Housing Tenure (B25003)

| Variable | Description |
|----------|-------------|
| B25003_001E | Total occupied housing units |
| B25003_002E | Owner occupied |
| B25003_003E | Renter occupied |

### Housing Units in Structure (B25024)

| Variable | Description |
|----------|-------------|
| B25024_001E | Total housing units |
| B25024_002E | 1, detached |
| B25024_003E | 1, attached |
| B25024_004E | 2 |
| B25024_005E | 3 or 4 |
| B25024_006E | 5 to 9 |
| B25024_007E | 10 to 19 |
| B25024_008E | 20 to 49 |
| B25024_009E | 50 or more |
| B25024_010E | Mobile home |
| B25024_011E | Boat, RV, van, etc. |

### Year Structure Built (B25034)

| Variable | Description |
|----------|-------------|
| B25034_001E | Total housing units |
| B25034_002E | Built 2020 or later |
| B25034_003E | Built 2010 to 2019 |
| B25034_004E | Built 2000 to 2009 |
| B25034_005E | Built 1990 to 1999 |
| B25034_006E | Built 1980 to 1989 |
| B25034_007E | Built 1970 to 1979 |
| B25034_008E | Built 1960 to 1969 |
| B25034_009E | Built 1950 to 1959 |
| B25034_010E | Built 1940 to 1949 |
| B25034_011E | Built 1939 or earlier |

### Gross Rent as % of Income (B25070)

| Variable | Description |
|----------|-------------|
| B25070_001E | Total renter-occupied units |
| B25070_007E | 30.0 to 34.9 percent |
| B25070_008E | 35.0 to 39.9 percent |
| B25070_009E | 40.0 to 49.9 percent |
| B25070_010E | 50.0 percent or more |

**Housing Cost Burden**: ≥30% of income on housing

---

## Transportation

### Vehicles Available (B25044)

| Variable | Description |
|----------|-------------|
| B25044_001E | Total occupied housing units |
| B25044_003E | Owner occupied: No vehicle |
| B25044_010E | Renter occupied: No vehicle |

### Means of Transportation to Work (B08301)

| Variable | Description |
|----------|-------------|
| B08301_001E | Total workers 16+ |
| B08301_002E | Car, truck, or van - drove alone |
| B08301_003E | Car, truck, or van - carpooled |
| B08301_010E | Public transportation |
| B08301_019E | Walked |
| B08301_021E | Worked from home |

---

## Language

### Language Spoken at Home (B16001)

| Variable | Description |
|----------|-------------|
| B16001_001E | Population 5+ years |
| B16001_002E | Speak only English |
| B16001_003E | Spanish: Speak English "very well" |
| B16001_004E | Spanish: Speak English less than "very well" |

### Limited English Speaking Households (C16002)

| Variable | Description |
|----------|-------------|
| C16002_001E | Total households |
| C16002_004E | Spanish: Limited English household |
| C16002_007E | Other Indo-European: Limited English |
| C16002_010E | Asian/Pacific Islander: Limited English |
| C16002_013E | Other: Limited English |

---

## Disability

### Disability Status (B18101)

| Variable | Description |
|----------|-------------|
| B18101_001E | Total civilian noninstitutionalized population |
| B18101_004E | Under 5: With a disability |
| B18101_007E | 5-17: With a disability |
| B18101_010E | 18-34: With a disability |
| B18101_013E | 35-64: With a disability |
| B18101_016E | 65-74: With a disability |
| B18101_019E | 75+: With a disability |

---

## SVI Component Variables

The CDC Social Vulnerability Index uses these ACS variables:

### Theme 1: Socioeconomic Status
- B17001_002E / B17001_001E → Below poverty
- B23025_005E / B23025_003E → Unemployed
- B19301_001E → Per capita income
- B15003_002E-016E → No high school diploma

### Theme 2: Household Composition & Disability
- Sum(B01001_020E:025E, B01001_044E:049E) → Age 65+
- Sum(B01001_003E:006E, B01001_027E:030E) → Age 17 and under
- B18101 → Civilian with disability
- B11001_006E → Single-parent households

### Theme 3: Minority Status & Language
- B03002 (non-White NH) → Minority
- C16002 → Limited English households

### Theme 4: Housing Type & Transportation
- B25024_007E-009E → Multi-unit housing (10+)
- B25024_010E → Mobile homes
- B25014_005E-007E, B25014_011E-013E → Crowding (>1 person/room)
- B25044_003E + B25044_010E → No vehicle
- B26001_001E → Group quarters

---

## Data Access

### Census API

```
Base URL: https://api.census.gov/data/

Example: 2022 ACS 5-Year, Harris County TX
GET /2022/acs/acs5?get=B01001_001E,B19013_001E&for=county:201&in=state:48
```

### Data.census.gov

Interactive data explorer: https://data.census.gov

---

## Related References

- [Geography Codes](geography-codes.md) - FIPS, CBSA codes
- [SVI Methodology](svi-methodology.md) - How SVI uses these variables
- [ADI Methodology](adi-methodology.md) - ADI variable requirements
