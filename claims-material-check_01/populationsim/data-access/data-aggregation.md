---
name: data-aggregation
description: >
  Aggregate data across geographic levels (tract→county, county→metro).
  Use for queries like "aggregate tract SVI to county", "metro area totals",
  or "average ADI across block groups".
  Triggers: "aggregate", "combine", "average across", "metro total"
---

# Data Aggregation Skill

## Overview

The data-aggregation skill provides patterns for combining data across geographic levels. Use when you need to:
- Aggregate tract-level data to county level
- Compute metro area statistics from component counties
- Average block group ADI to tract or county level
- Create custom regional summaries

## Trigger Phrases

- "Aggregate [measure] for [geography]"
- "What's the average [measure] across tracts in [county]?"
- "Combine counties for [metro area] statistics"
- "Total population for [region]"
- "Weighted average of [measure] in [geography]"

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| aggregation_type | string | Yes | "tract_to_county", "county_to_metro", "block_group_to_tract" |
| target_geography | string | Yes | Target geography identifier |
| measures | array | No | Specific measures to aggregate |
| method | string | No | "sum", "mean", "weighted_mean" (default varies by measure) |

## Aggregation Methods

### For Count Variables (E_* columns)
**Method:** SUM
- E_TOTPOP (total population): Sum across sub-geographies
- E_POV150 (persons below 150% poverty): Sum
- E_UNINSUR (uninsured persons): Sum

### For Percentage Variables (EP_* columns, prevalence rates)
**Method:** POPULATION-WEIGHTED AVERAGE
```
Aggregated Rate = Σ(Rate_i × Population_i) / Σ(Population_i)
```

### For Percentile Rankings (RPL_* columns, ADI)
**Method:** POPULATION-WEIGHTED AVERAGE
- Weight each tract/block group by its population
- Higher-population areas have more influence on aggregate

### For Missing Data
- SVI uses -999 for missing values → Exclude from calculations
- ADI uses suppression codes (GQ, PH, QDI) → Exclude from calculations

## Generation Patterns

### Pattern 1: Tract to County Aggregation (SVI)

**Input:** "Aggregate SVI scores for all tracts in Harris County, TX"

**Process:**
1. Read `data/tract/svi_tract_2022.csv`
2. Filter: FIPS starts with "48201" (Harris County)
3. For each RPL_ column:
   - Calculate population-weighted average
   - Weight = E_TOTPOP for each tract
4. Sum E_TOTPOP for total population

**Calculation Example:**
```
Tract 1: RPL_THEMES = 0.85, Population = 5,000
Tract 2: RPL_THEMES = 0.42, Population = 8,000
Tract 3: RPL_THEMES = 0.68, Population = 3,000

Weighted SVI = (0.85×5000 + 0.42×8000 + 0.68×3000) / (5000+8000+3000)
             = (4250 + 3360 + 2040) / 16000
             = 9650 / 16000
             = 0.603
```

**Response:**
**Harris County, TX - Aggregated SVI from 786 Census Tracts**

| Theme | Aggregated Score | Interpretation |
|-------|------------------|----------------|
| Overall SVI | 0.633 | Moderate-High |
| Socioeconomic | 0.671 | Moderate-High |
| Household Comp | 0.586 | Moderate |
| Minority/Language | 0.794 | High |
| Housing/Transport | 0.478 | Moderate |

Total Population: 4,726,177 (from 786 tracts)

*Method: Population-weighted average of tract values*
*Source: CDC/ATSDR SVI 2022*

---

### Pattern 2: County to Metro Aggregation

**Input:** "Calculate total population and average diabetes rate for Houston MSA"

**Process:**
1. Read `data/crosswalks/cbsa_definitions.csv`
2. Filter: cbsa_title contains "Houston" → Get 9 county FIPS
3. Read `data/county/places_county_2024.csv` for each county
4. Sum: TotalPopulation
5. Weighted average: DIABETES_CrudePrev (weighted by population)

**Response:**
**Houston-The Woodlands-Sugar Land, TX MSA**
CBSA 26420 | 9 Counties

| Metric | Value | Method |
|--------|-------|--------|
| Total Population | 7,340,586 | Sum |
| Diabetes Prevalence | 12.8% | Pop-weighted avg |
| Obesity Prevalence | 34.2% | Pop-weighted avg |
| Uninsured Rate | 18.1% | Pop-weighted avg |

**County Breakdown:**

| County | Population | Diabetes | Weight |
|--------|------------|----------|--------|
| Harris | 4,835,125 | 13.2% | 65.9% |
| Fort Bend | 842,123 | 11.8% | 11.5% |
| Montgomery | 644,672 | 12.4% | 8.8% |
| Brazoria | 379,582 | 13.5% | 5.2% |
| Galveston | 350,209 | 12.9% | 4.8% |
| Others | 288,875 | varies | 3.9% |

*Source: CDC PLACES 2024, Census Bureau*

---

### Pattern 3: Block Group to Tract ADI

**Input:** "What's the average ADI for tract 48201210400?"

**Process:**
1. Read `data/block_group/adi_blockgroup_2023.csv`
2. Filter: FIPS starts with "48201210400" (11 digits)
3. Exclude suppressed values (GQ, PH, QDI)
4. Average ADI_NATRANK across valid block groups

**Response:**
**Census Tract 48201210400 (Harris County, TX) - Estimated ADI**

| Block Group | ADI National Rank | State Decile |
|-------------|-------------------|--------------|
| 482012104001 | 46 | 4 |
| 482012104002 | 65 | 6 |
| 482012104003 | 52 | 4 |

**Tract Aggregate:**
- Average National Rank: **54** (moderate deprivation)
- Average State Decile: **4.7** (below state median)

*Method: Simple average of block group values*
*Source: Neighborhood Atlas ADI 2023*

---

### Pattern 4: Custom Region Aggregation

**Input:** "Aggregate health data for a 5-county service area: Harris, Fort Bend, Montgomery, Brazoria, Galveston TX"

**Process:**
1. Resolve county names to FIPS
2. Read PLACES and SVI data for each county
3. Sum populations
4. Calculate weighted averages for rates/percentiles

**Response:**
**Custom Service Area: 5-County Houston Region**

| County | FIPS | Population |
|--------|------|------------|
| Harris | 48201 | 4,835,125 |
| Fort Bend | 48157 | 842,123 |
| Montgomery | 48339 | 644,672 |
| Brazoria | 48039 | 379,582 |
| Galveston | 48167 | 350,209 |
| **Total** | - | **7,051,711** |

**Aggregated Health Indicators:**

| Measure | Service Area | Texas | Difference |
|---------|--------------|-------|------------|
| Diabetes | 12.9% | 11.8% | +1.1% |
| Obesity | 34.5% | 33.2% | +1.3% |
| Hypertension | 32.2% | 31.8% | +0.4% |
| Uninsured | 17.8% | 17.5% | +0.3% |

**Aggregated SVI:**
- Overall: 0.58 (moderate)

*Method: Population-weighted averages*
*Sources: CDC PLACES 2024, CDC SVI 2022*

---

## Special Cases

### Handling Missing Tract Data

Some tracts may have missing data (coded as -999 in SVI). Exclude from weighted calculations:

```python
# Pseudocode for weighted average with missing data
valid_tracts = [t for t in tracts if t.value != -999]
weighted_sum = sum(t.value * t.population for t in valid_tracts)
total_weight = sum(t.population for t in valid_tracts)
aggregated_value = weighted_sum / total_weight
```

### Handling ADI Suppression

Block groups with suppression codes should be excluded:
- GQ (Group Quarters): Skip - unusual population composition
- PH (Population/Housing): Skip - too small for reliable estimate
- QDI (Questionable Data): Skip - missing key factors

Report the number of suppressed block groups in the response.

### Metro Areas Crossing State Lines

Some CBSAs span multiple states (e.g., Philadelphia-Camden-Wilmington). Aggregate all counties regardless of state.

---

## Validation Rules

### Aggregation Quality Checks
- [ ] At least 80% of sub-geographies have valid data
- [ ] Population total matches expected range
- [ ] Aggregated rates are within 0-100% bounds
- [ ] Report count of excluded/missing values

### Output Requirements
- [ ] Specify aggregation method used
- [ ] List component geographies
- [ ] Include total population
- [ ] Cite data sources

---

## Examples

### Example 1: County SVI from Tracts

**User:** "Calculate the population-weighted SVI for San Diego County from tract data"

**Claude:** **San Diego County, CA - SVI Aggregated from 628 Census Tracts**

| SVI Theme | Aggregated Score |
|-----------|------------------|
| **Overall (RPL_THEMES)** | 0.545 |
| Socioeconomic (RPL_THEME1) | 0.503 |
| Household Comp (RPL_THEME2) | 0.479 |
| Minority/Language (RPL_THEME3) | 0.679 |
| Housing/Transport (RPL_THEME4) | 0.582 |

- Total Population: 3,269,973
- Tracts Included: 628
- Tracts Excluded (missing data): 3

*Method: Population-weighted average (E_TOTPOP as weight)*
*Source: CDC/ATSDR SVI 2022*

---

### Example 2: Service Area Analysis

**User:** "Aggregate diabetes and obesity rates for a hospital service area covering these ZIP codes: 77001-77099"

**Claude:** I'll need to convert ZIP codes to census tracts first. However, our embedded data doesn't include ZIP-to-tract crosswalks.

**Alternative approach:** If you can specify the counties or census tracts in your service area, I can aggregate from:
- County-level PLACES data (for county-based service areas)
- Tract-level PLACES data (for tract-based service areas)

Would you like to specify the geography using counties or tract FIPS codes instead?

---

## Related Skills

- [data-lookup.md](data-lookup.md) - Look up individual values
- [geography-lookup.md](geography-lookup.md) - Resolve FIPS codes
- [../geographic/custom-region-builder.md](../geographic/custom-region-builder.md) - Build custom regions
- [../geographic/metro-area-profile.md](../geographic/metro-area-profile.md) - Metro profiles
