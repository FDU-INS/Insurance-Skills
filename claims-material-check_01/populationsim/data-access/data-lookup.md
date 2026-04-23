---
name: data-lookup
description: >
  Look up specific data values from PopulationSim's embedded data package.
  Use for direct queries like "what is the diabetes rate in X county",
  "show me SVI for tract Y", or "ADI for block group Z".
  Triggers: "what is the", "look up", "exact", "from CDC PLACES", "from SVI"
---

# Data Lookup Skill

## Overview

The data-lookup skill provides direct access to PopulationSim's embedded data package. Use this skill when you need exact values for specific geographies rather than synthesized estimates.

**Data-First Philosophy**: When data exists in the embedded files, return the exact value with source citation. Only synthesize when data is unavailable.

## Trigger Phrases

- "What is the [measure] in [geography]?"
- "Look up [measure] for [geography]"
- "What's the exact [measure] rate in [county/tract]?"
- "Show me CDC PLACES data for [geography]"
- "Get the SVI for [geography]"
- "Find the ADI for [block group]"
- "What does the data say about [geography]?"

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| geography_type | string | Yes | "county", "tract", or "block_group" |
| geography_id | string | Yes | FIPS code or name (e.g., "48201" or "Harris County, TX") |
| dataset | string | No | "places", "svi", or "adi" (auto-detected from measure) |
| measures | array | No | Specific measures to return (default: key measures) |

## Data File Reference

### CDC PLACES County Data
**File:** `data/county/places_county_2024.csv`
**Key Columns:**
| Column | Description |
|--------|-------------|
| StateAbbr | State abbreviation (TX, CA, etc.) |
| CountyName | County name |
| CountyFIPS | 5-digit county FIPS code |
| TotalPopulation | County population |
| [MEASURE]_CrudePrev | Crude prevalence (%) |
| [MEASURE]_AdjPrev | Age-adjusted prevalence (%) |

### CDC PLACES Measures (40 total)

**Health Outcomes:**
| MeasureId | Description | National Avg |
|-----------|-------------|--------------|
| DIABETES | Diagnosed diabetes | 10.1% |
| OBESITY | Obesity (BMI ≥30) | 32.1% |
| BPHIGH | High blood pressure | 32.4% |
| HIGHCHOL | High cholesterol | 29.8% |
| CHD | Coronary heart disease | 5.4% |
| STROKE | Stroke | 3.0% |
| COPD | COPD | 6.2% |
| CASTHMA | Current asthma | 9.8% |
| CANCER | Cancer (ever told) | 6.9% |
| KIDNEY | Chronic kidney disease | 3.0% |
| ARTHRITIS | Arthritis | 24.2% |
| DEPRESSION | Depression | 18.6% |

**Health Behaviors:**
| MeasureId | Description | National Avg |
|-----------|-------------|--------------|
| CSMOKING | Current smoking | 14.1% |
| BINGE | Binge drinking | 16.8% |
| LPA | Physical inactivity | 22.8% |
| SLEEP | Short sleep (<7 hrs) | 34.8% |

**Prevention:**
| MeasureId | Description | National Avg |
|-----------|-------------|--------------|
| CHECKUP | Annual checkup | 77.8% |
| DENTAL | Dental visit | 66.8% |
| CHOLSCREEN | Cholesterol screening | 88.4% |
| COLON_SCREEN | Colorectal screening | 72.8% |
| MAMMOUSE | Mammography | 78.2% |

**Disabilities:**
| MeasureId | Description |
|-----------|-------------|
| HEARING | Hearing difficulty |
| VISION | Vision difficulty |
| COGNITION | Cognitive difficulty |
| MOBILITY | Mobility difficulty |
| SELFCARE | Self-care difficulty |
| INDEPLIVE | Independent living difficulty |
| DISABILITY | Any disability |

**Health Status:**
| MeasureId | Description |
|-----------|-------------|
| GHLTH | Fair/poor general health |
| MHLTH | Frequent mental distress (14+ days) |
| PHLTH | Frequent physical distress (14+ days) |

**Social Needs:**
| MeasureId | Description |
|-----------|-------------|
| FOODINSECU | Food insecurity |
| HOUSINSECU | Housing insecurity |
| LACKTRPT | Lack of transportation |
| SHUTUTILITY | Utility shutoff threat |

### SVI County Data
**File:** `data/county/svi_county_2022.csv`
**Key Columns:**
| Column | Description |
|--------|-------------|
| ST_ABBR | State abbreviation |
| COUNTY | County name |
| STCNTY | 5-digit county FIPS |
| E_TOTPOP | Total population |
| RPL_THEMES | Overall SVI (0-1) |
| RPL_THEME1 | Socioeconomic Status (0-1) |
| RPL_THEME2 | Household Characteristics (0-1) |
| RPL_THEME3 | Minority/Language (0-1) |
| RPL_THEME4 | Housing/Transportation (0-1) |
| EP_POV150 | % below 150% poverty |
| EP_UNINSUR | % uninsured |
| EP_MINRTY | % minority |

### SVI Tract Data
**File:** `data/tract/svi_tract_2022.csv`
**Same structure as county file plus:**
- FIPS: 11-digit tract FIPS
- LOCATION: Tract description
- Full demographic variables (E_* counts, EP_* percentages)

### ADI Block Group Data
**File:** `data/block_group/adi_blockgroup_2023.csv`
**Columns:**
| Column | Description |
|--------|-------------|
| FIPS | 12-digit block group FIPS |
| ADI_NATRANK | National percentile (1-100) |
| ADI_STATERNK | State decile (1-10) |

**Suppression Codes:**
- GQ: >33% group quarters
- PH: Population <100 or <30 housing units
- QDI: Missing key demographic factor



## Generation Patterns

### Pattern 1: County Health Indicator Lookup

**Input:** "What is the diabetes prevalence in Harris County, TX?"

**Process:**
1. Identify geography: county = "Harris", state = "TX"
2. Resolve FIPS: Look up in `data/crosswalks/fips_county.csv` → 48201
3. Read `data/county/places_county_2024.csv`
4. Filter: CountyFIPS = "48201"
5. Extract: DIABETES_CrudePrev
6. Format response with provenance

**Response:**
Harris County, TX has a diabetes prevalence of **13.2%** among adults.

| Attribute | Value |
|-----------|-------|
| Crude Prevalence | 13.2% |
| Geography | Harris County, TX (FIPS 48201) |
| Population | 4,835,125 |
| Source | CDC PLACES 2024 Release |
| Data Year | 2022 BRFSS |

This is higher than the national average of 10.1%.

---

### Pattern 2: Multiple Health Measures

**Input:** "Show me the key health indicators for San Diego County"

**Process:**
1. Resolve: San Diego, CA → FIPS 06073
2. Read PLACES county file
3. Extract multiple measures
4. Compare to national averages

**Response:**
**San Diego County, CA (FIPS 06073) Health Profile**
Population: 3,269,973

| Measure | San Diego | National | Status |
|---------|-----------|----------|--------|
| Diabetes | 10.0% | 10.1% | ≈ Average |
| Obesity | 25.3% | 32.1% | ✓ Below |
| Hypertension | 28.7% | 32.4% | ✓ Below |
| Smoking | 10.0% | 14.1% | ✓ Below |
| Depression | 19.1% | 18.6% | ≈ Average |

*Source: CDC PLACES 2024 Release (2022 BRFSS data)*

---

### Pattern 3: County SVI Lookup

**Input:** "What's the SVI for Cook County, IL?"

**Process:**
1. Resolve: Cook County, IL → FIPS 17031
2. Read `data/county/svi_county_2022.csv`
3. Filter: STCNTY = "17031"
4. Extract all RPL_ columns

**Response:**
**Cook County, IL Social Vulnerability Index**

| Theme | Score | Interpretation |
|-------|-------|----------------|
| **Overall SVI** | 0.566 | Moderate vulnerability |
| Socioeconomic Status | 0.562 | Moderate |
| Household Characteristics | 0.513 | Moderate |
| Minority/Language | 0.683 | Moderate-High |
| Housing/Transportation | 0.525 | Moderate |

**Key Indicators:**
- Population: 5,087,072
- Below 150% Poverty: 22.8%
- Uninsured: 9.2%
- Minority: 62.4%

*Source: CDC/ATSDR Social Vulnerability Index 2022 (2018-2022 ACS)*

---

### Pattern 4: Tract-Level Lookup

**Input:** "Show SVI for census tract 48201311500"

**Process:**
1. Validate tract FIPS (11 digits)
2. Read `data/tract/svi_tract_2022.csv`
3. Filter: FIPS = "48201311500"
4. Extract SVI themes and demographics

**Response:**
**Census Tract 48201311500 (Harris County, TX)**

| Theme | Score | Interpretation |
|-------|-------|----------------|
| **Overall SVI** | 0.92 | Very High vulnerability |
| Socioeconomic Status | 0.89 | High |
| Household Characteristics | 0.78 | High |
| Minority/Language | 0.95 | Very High |
| Housing/Transportation | 0.82 | High |

*Source: CDC/ATSDR SVI 2022*

---

### Pattern 5: Block Group ADI Lookup

**Input:** "What's the ADI for block group 482012104001?"

**Process:**
1. Validate block group FIPS (12 digits)
2. Read `data/block_group/adi_blockgroup_2023.csv`
3. Filter: FIPS = "482012104001"
4. Extract ADI rankings

**Response:**
**Block Group 482012104001** (Harris County, TX)

| Ranking | Value | Interpretation |
|---------|-------|----------------|
| National Percentile | 46 | Lower-moderate deprivation |
| State Decile | 4 | Below Texas median |

A national percentile of 46 means this block group has less deprivation than 46% of all US block groups.

*Source: Neighborhood Atlas ADI 2023 v4.0.1 (UW-Madison)*

---

### Pattern 6: Comparison Query

**Input:** "Compare diabetes rates: Harris County TX vs Los Angeles County CA"

**Process:**
1. Resolve both counties
2. Read PLACES for both
3. Calculate difference

**Response:**
**Diabetes Prevalence Comparison**

| County | FIPS | Diabetes Rate | vs National (10.1%) |
|--------|------|---------------|---------------------|
| Harris County, TX | 48201 | 13.2% | +3.1% ⚠️ |
| Los Angeles County, CA | 06037 | 12.8% | +2.7% ⚠️ |

Both counties have diabetes rates significantly above the national average, with Harris County slightly higher.

*Source: CDC PLACES 2024 Release*

---

## Examples

### Example 1: Simple Health Query

**User:** "What's the obesity rate in Miami-Dade County, Florida?"

**Claude:** Miami-Dade County, FL has an obesity prevalence of **27.8%** among adults.

This is below the national average of 32.1%, though still represents a significant public health concern for the county's 2.7 million residents.

*Source: CDC PLACES 2024 Release (2022 BRFSS data)*

---

### Example 2: SVI Deep Dive

**User:** "Show me detailed SVI data for Maricopa County, Arizona"

**Claude:** **Maricopa County, AZ (FIPS 04013) Social Vulnerability Index**

| Component | Score | Percentile |
|-----------|-------|------------|
| **Overall SVI** | 0.528 | 53rd (Moderate) |
| Theme 1: Socioeconomic | 0.492 | 49th |
| Theme 2: Household Comp | 0.468 | 47th |
| Theme 3: Minority/Language | 0.624 | 62nd |
| Theme 4: Housing/Transport | 0.512 | 51st |

**Detailed Indicators:**
- Population: 4,420,568
- Below 150% Poverty: 20.2%
- Uninsured: 10.8%
- No High School Diploma: 11.4%
- Age 65+: 15.8%
- Single Parent Households: 8.2%

Maricopa County shows moderate vulnerability overall, with slightly elevated minority/language vulnerability reflecting its diverse population.

*Source: CDC/ATSDR SVI 2022 (2018-2022 ACS data)*

---

### Example 3: ADI for Neighborhood Analysis

**User:** "Look up ADI for these Harris County block groups: 482012104001, 482012104002, 482012105001"

**Claude:** **ADI Rankings for Harris County Block Groups**

| Block Group | National Rank | State Decile | Interpretation |
|-------------|---------------|--------------|----------------|
| 482012104001 | 46 | 4 | Lower-moderate deprivation |
| 482012104002 | 65 | 6 | Moderate deprivation |
| 482012105001 | 61 | 5 | Moderate deprivation |

**Average for these 3 block groups:**
- National Rank: 57
- Interpretation: Moderate neighborhood deprivation

*Source: Neighborhood Atlas ADI 2023 v4.0.1*

---

## Validation Rules

### Input Validation
- County FIPS must be exactly 5 digits
- Tract FIPS must be exactly 11 digits
- Block group FIPS must be exactly 12 digits
- State abbreviations must be valid 2-letter codes
- County names should match Census gazetteer

### Output Validation
- [ ] All values come from actual data files
- [ ] Source citation included
- [ ] Data vintage/year specified
- [ ] Percentages are in reasonable range (0-100)
- [ ] SVI scores are between 0 and 1
- [ ] ADI ranks are 1-100 (national) or 1-10 (state)

### Missing Data Handling
- If geography not found: "No data available for [geography]. Please verify the FIPS code or name."
- If measure suppressed: "Data suppressed for [measure] in [geography] due to small sample size."
- If ADI has suppression code: Explain the code (GQ, PH, QDI)

---

## Related Skills

- [geography-lookup.md](geography-lookup.md) - Resolve FIPS codes
- [data-aggregation.md](data-aggregation.md) - Aggregate across geographies
- [../geographic/county-profile.md](../geographic/county-profile.md) - Full county profiles
- [../sdoh/svi-analysis.md](../sdoh/svi-analysis.md) - SVI interpretation
- [../sdoh/adi-analysis.md](../sdoh/adi-analysis.md) - ADI interpretation
