# PopulationSim v2.0 Phase 2: Skills Integration Super-Prompt

## Mission

Transform PopulationSim from a synthesis-first system to a **data-first platform** by updating all skills to read from the embedded data package (148 MB, 100% US coverage) and provide exact values with transparent provenance.

---

## Context & Prerequisites

### What Was Completed in Phase 1
- Downloaded CDC PLACES (county + tract)
- Downloaded SVI (county aggregated + tract)
- Downloaded ADI (block group level)
- Created geography crosswalks (state, county, tract, CBSA)
- Documented all datasets in `data/README.md`

### Embedded Data Package Location
```
skills/populationsim/data/
├── README.md                          # Complete data dictionary
├── county/
│   ├── places_county_2024.csv         # 3,143 counties, 40 health measures
│   └── svi_county_2022.csv            # 3,144 counties, aggregated SVI
├── tract/
│   ├── places_tract_2024.csv          # 83,522 tracts, 40 health measures  
│   └── svi_tract_2022.csv             # 84,120 tracts, 158 columns
├── block_group/
│   ├── adi_blockgroup_2023.csv        # 242,336 block groups, ADI rankings
│   └── adi_readme.txt                 # Source documentation
└── crosswalks/
    ├── fips_state.csv                 # 51 states/territories
    ├── fips_county.csv                # 3,144 counties
    ├── tract_to_county.csv            # 84,120 tract mappings
    └── cbsa_definitions.csv           # 937 CBSAs (metro/micro)
```

### Reference Documents to Read First
1. `skills/populationsim/data/README.md` - Complete data dictionary
2. `skills/populationsim/SKILL.md` - Current master skill
3. `skills/populationsim/geographic/county-profile.md` - Pattern example
4. `docs/POPULATIONSIM-DATA-PACKAGE-OVERVIEW.md` - Architecture vision

---

## Pre-Flight Checklist

Before starting implementation:

- [ ] Verify data files exist in `skills/populationsim/data/`
- [ ] Read `data/README.md` to understand column schemas
- [ ] Review current SKILL.md structure
- [ ] Understand the PopulationProfile and CohortSpecification schemas
- [ ] Note the pattern: read data → assemble response → cite source

---

## Phase 2 Deliverables

### Part A: New Skills to Create (4 files)

| File | Purpose | Priority |
|------|---------|----------|
| `skills/populationsim/data-access/README.md` | Category overview | High |
| `skills/populationsim/data-access/data-lookup.md` | Direct data file access patterns | High |
| `skills/populationsim/data-access/geography-lookup.md` | FIPS code resolution and crosswalks | High |
| `skills/populationsim/data-access/data-aggregation.md` | Aggregating tract→county, block group→tract | Medium |

### Part B: Existing Skills to Update (15+ files)

**Geographic Skills** (update to use real data):
| File | Key Updates |
|------|-------------|
| `geographic/county-profile.md` | Add data lookup instructions, real examples |
| `geographic/census-tract-analysis.md` | Enable tract-level queries with PLACES + SVI |
| `geographic/metro-area-profile.md` | CBSA crosswalk lookups |
| `geographic/custom-region-builder.md` | Multi-county aggregation patterns |

**Health Pattern Skills** (connect to CDC PLACES):
| File | Key Updates |
|------|-------------|
| `health-patterns/chronic-disease-prevalence.md` | Real PLACES measure lookups |
| `health-patterns/health-behavior-patterns.md` | Real behavior measure lookups |
| `health-patterns/healthcare-access-analysis.md` | Real access metrics |
| `health-patterns/health-outcome-disparities.md` | Quantitative disparity analysis |

**SDOH Skills** (connect to SVI + ADI):
| File | Key Updates |
|------|-------------|
| `sdoh/svi-analysis.md` | Real SVI data lookups |
| `sdoh/adi-analysis.md` | Real ADI block group lookups |
| `sdoh/economic-indicators.md` | SVI economic variables |
| `sdoh/community-factors.md` | SVI housing/transportation |

**Cohort Skills** (use real distributions):
| File | Key Updates |
|------|-------------|
| `cohorts/cohort-specification.md` | Real demographic distributions |
| `cohorts/demographic-distribution.md` | Real ACS demographics from SVI |
| `cohorts/clinical-prevalence-profile.md` | Real PLACES prevalence rates |
| `cohorts/sdoh-profile-builder.md` | Real SVI/ADI indices |

### Part C: Reference Files to Update (3 files)

| File | Updates |
|------|---------|
| `references/cdc-places-measures.md` | Add column name mappings |
| `references/svi-variables.md` | Add column name mappings |
| `data-sources.md` | Complete overhaul with data package |

### Part D: Master Skill Update (1 file)

| File | Updates |
|------|---------|
| `SKILL.md` | Add data-access category, update trigger phrases, add data-first examples |

---

## Implementation Instructions

### Step 1: Create Data Access Category (Session Start)

#### 1.1 Create `skills/populationsim/data-access/README.md`

```markdown
---
name: populationsim-data-access
description: >
  Skills for directly accessing PopulationSim's embedded data package.
  Use these skills when you need to look up specific values, resolve
  geography codes, or aggregate data across geographic levels.
---

# Data Access Skills

## Overview

PopulationSim v2.0 includes an embedded data package with real demographic,
health, and SDOH data covering 100% of US geography. These skills provide
direct access patterns for reading and aggregating this data.

## Data Package Summary

| Level | Files | Records | Key Data |
|-------|-------|---------|----------|
| County | 2 | ~3,144 | PLACES health, SVI aggregate |
| Tract | 2 | ~84,000 | PLACES health, SVI full |
| Block Group | 1 | ~242,000 | ADI rankings |
| Crosswalks | 4 | Various | FIPS, CBSA mappings |

## Skills in This Category

| Skill | Use When |
|-------|----------|
| [data-lookup.md](data-lookup.md) | Looking up specific values by geography |
| [geography-lookup.md](geography-lookup.md) | Resolving FIPS codes, finding geographies |
| [data-aggregation.md](data-aggregation.md) | Aggregating tract→county or computing means |

## Data Provenance Principle

**Every data value returned must include its source.** Pattern:

```json
{
  "value": 12.1,
  "source": "CDC PLACES 2024",
  "data_year": 2022,
  "geography": "48201",
  "measure": "DIABETES"
}
```

## File Locations

All data files are in `skills/populationsim/data/`:
- County data: `data/county/*.csv`
- Tract data: `data/tract/*.csv`  
- Block group data: `data/block_group/*.csv`
- Crosswalks: `data/crosswalks/*.csv`
```

#### 1.2 Create `skills/populationsim/data-access/data-lookup.md`

This is the **core skill** for reading embedded data. Include:

**Sections Required:**
1. Overview - explain data-first philosophy
2. Trigger Phrases - "look up", "what is the exact", "CDC PLACES for"
3. Parameters - geography_type, geography_id, dataset, measures
4. Data File Mapping - which file for which query
5. Column Reference - key columns in each file
6. Generation Patterns:
   - County health lookup (PLACES)
   - County SVI lookup
   - Tract health lookup
   - Tract SVI lookup
   - Block group ADI lookup
7. Examples with REAL data (pick 3 real counties, show actual values)
8. Validation Rules
9. Related Skills

**Critical Content - Data File Mapping:**

```markdown
## Data File Mapping

| Query Type | File | Key Columns |
|------------|------|-------------|
| County health indicators | `county/places_county_2024.csv` | StateAbbr, CountyName, CountyFIPS, MeasureId, Data_Value |
| County SVI | `county/svi_county_2022.csv` | ST_ABBR, COUNTY, FIPS, RPL_THEMES, RPL_THEME1-4 |
| Tract health indicators | `tract/places_tract_2024.csv` | StateAbbr, CountyName, LocationID, MeasureId, Data_Value |
| Tract SVI | `tract/svi_tract_2022.csv` | ST_ABBR, COUNTY, FIPS, RPL_THEMES, E_TOTPOP, EP_* |
| Block group ADI | `block_group/adi_blockgroup_2023.csv` | FIPS, ADI_NATRANK, ADI_STATERNK |
| State FIPS | `crosswalks/fips_state.csv` | state_fips, state_name, state_abbr |
| County FIPS | `crosswalks/fips_county.csv` | state_fips, county_fips, county_name, state_abbr |
| CBSA definitions | `crosswalks/cbsa_definitions.csv` | county_fips, cbsa_code, cbsa_title, cbsa_type |

## CDC PLACES Measure IDs

The PLACES files use MeasureId codes. Key mappings:

| MeasureId | Measure Name | Category |
|-----------|--------------|----------|
| DIABETES | Diabetes prevalence | Outcomes |
| OBESITY | Obesity prevalence | Outcomes |
| BPHIGH | High blood pressure | Outcomes |
| HIGHCHOL | High cholesterol | Outcomes |
| CHD | Coronary heart disease | Outcomes |
| STROKE | Stroke | Outcomes |
| COPD | COPD | Outcomes |
| CASTHMA | Current asthma | Outcomes |
| DEPRESSION | Depression | Outcomes |
| KIDNEY | Chronic kidney disease | Outcomes |
| CANCER | Cancer (ever) | Outcomes |
| CSMOKING | Current smoking | Behaviors |
| BINGE | Binge drinking | Behaviors |
| LPA | Physical inactivity | Behaviors |
| SLEEP | Short sleep | Behaviors |
| CHECKUP | Annual checkup | Prevention |
| DENTAL | Dental visit | Prevention |
| COLON_SCREEN | Colorectal screening | Prevention |
| MAMMOUSE | Mammography | Prevention |
```

**Critical Content - Lookup Pattern:**

```markdown
## Generation Pattern: County Health Lookup

**Input:** "What is the diabetes prevalence in Harris County, TX?"

**Process:**
1. Read `data/county/places_county_2024.csv`
2. Filter: StateAbbr = "TX" AND CountyName = "Harris" AND MeasureId = "DIABETES"
3. Extract Data_Value
4. Format response with provenance

**Response:**
Harris County, TX has a diabetes prevalence of **12.1%** among adults.

| Attribute | Value |
|-----------|-------|
| Data Value | 12.1% |
| Source | CDC PLACES 2024 |
| Data Year | 2022 BRFSS |
| Geography | Harris County, TX (FIPS 48201) |
| Measure | Crude prevalence of diagnosed diabetes |

This is higher than the Texas state average (11.8%) and national average (10.1%).
```

#### 1.3 Create `skills/populationsim/data-access/geography-lookup.md`

Focus on FIPS code resolution and crosswalk queries.

**Key Content:**
- State FIPS lookup (name → code, code → name)
- County FIPS lookup (resolve ambiguous county names)
- Tract FIPS structure (explain 11-digit format)
- CBSA lookup (county → metro area)
- Block group FIPS structure (explain 12-digit format)

#### 1.4 Create `skills/populationsim/data-access/data-aggregation.md`

Focus on aggregating data across geographic levels.

**Key Content:**
- Aggregating tracts to county (population-weighted averages)
- Computing metro area statistics from component counties
- Block group to tract aggregation for ADI
- Handling missing data (-999 in SVI, suppression codes in ADI)



### Step 2: Update Geographic Skills

#### 2.1 Update `geographic/county-profile.md`

**Changes Required:**

1. **Add Data Lookup Section** (after Overview, before Trigger Phrases):

```markdown
## Data Sources (Embedded)

This skill reads from PopulationSim's embedded data package:

| Data Type | File | Key Columns |
|-----------|------|-------------|
| Health Indicators | `data/county/places_county_2024.csv` | CountyFIPS, MeasureId, Data_Value |
| SVI Scores | `data/county/svi_county_2022.csv` | FIPS, RPL_THEMES, RPL_THEME1-4, E_TOTPOP |
| Demographics | `data/tract/svi_tract_2022.csv` | Aggregate from tracts - E_TOTPOP, EP_* columns |

**Data Access Pattern:**
1. Resolve county name to FIPS code using `data/crosswalks/fips_county.csv`
2. Look up health indicators in PLACES county file
3. Look up SVI scores in SVI county file
4. For demographics, aggregate from tract-level SVI file (has full ACS demographics)
```

2. **Update Generation Pattern 1** to include file reading:

```markdown
### Pattern 1: Single County Profile

**Input**: "Profile San Diego County"

**Process**:
1. Resolve county identifier:
   - Read `data/crosswalks/fips_county.csv`
   - Find: county_name = "San Diego" AND state_abbr = "CA"
   - Extract: county_fips = "06073"

2. Pull CDC PLACES health measures:
   - Read `data/county/places_county_2024.csv`
   - Filter: CountyFIPS = "06073"
   - Extract all MeasureId/Data_Value pairs

3. Pull SVI scores:
   - Read `data/county/svi_county_2022.csv`
   - Filter: FIPS = "06073"
   - Extract: RPL_THEMES, RPL_THEME1, RPL_THEME2, RPL_THEME3, RPL_THEME4

4. Pull demographics (from tract SVI file):
   - Read `data/tract/svi_tract_2022.csv`
   - Filter: FIPS starts with "06073" (county portion)
   - Sum: E_TOTPOP for total population
   - Average: EP_* columns weighted by E_TOTPOP

5. Assemble PopulationProfile with provenance metadata
```

3. **Update Examples** with REAL data values:

Read actual values from the data files and use those exact numbers in examples.

4. **Add Data Provenance to Output Schema**:

```json
"metadata": {
  "generated_at": "2024-12-23T10:00:00Z",
  "data_sources": {
    "health_indicators": {
      "file": "places_county_2024.csv",
      "source": "CDC PLACES",
      "vintage": "2024 Release",
      "data_year": "2022 BRFSS"
    },
    "svi": {
      "file": "svi_county_2022.csv", 
      "source": "CDC/ATSDR",
      "vintage": "2022",
      "data_year": "2018-2022 ACS"
    },
    "demographics": {
      "file": "svi_tract_2022.csv",
      "source": "Census ACS via SVI",
      "vintage": "2022",
      "data_year": "2018-2022 ACS"
    }
  }
}
```

#### 2.2 Update `geographic/census-tract-analysis.md`

**Key Changes:**
1. Add data lookup instructions for tract-level files
2. Update examples with real tract FIPS codes and values
3. Add pattern for finding high/low tracts within a county
4. Include aggregation pattern for summarizing tracts

#### 2.3 Update `geographic/metro-area-profile.md`

**Key Changes:**
1. Add CBSA crosswalk lookup pattern
2. Show how to aggregate county data to metro level
3. Example: Houston MSA (9 counties) with real aggregated values

#### 2.4 Update `geographic/custom-region-builder.md`

**Key Changes:**
1. Multi-county aggregation patterns
2. Weighted averaging for percentages
3. Sum patterns for counts

---

### Step 3: Update Health Pattern Skills

#### 3.1 Update `health-patterns/chronic-disease-prevalence.md`

**Critical Changes:**

1. **Add PLACES Measure Reference:**

```markdown
## Available Measures (CDC PLACES 2024)

### Health Outcomes (13 measures)
| MeasureId | Description | National Rate |
|-----------|-------------|---------------|
| ARTHRITIS | Arthritis | 24.2% |
| BPHIGH | High blood pressure | 32.4% |
| CANCER | Cancer (ever told) | 6.9% |
| CASTHMA | Current asthma | 9.8% |
| CHD | Coronary heart disease | 5.4% |
| COPD | COPD | 6.2% |
| DEPRESSION | Depression | 18.6% |
| DIABETES | Diabetes | 10.1% |
| HIGHCHOL | High cholesterol | 29.8% |
| KIDNEY | Chronic kidney disease | 3.0% |
| OBESITY | Obesity | 32.1% |
| STROKE | Stroke | 3.0% |
| TEETHLOST | All teeth lost (65+) | 12.8% |
```

2. **Add Data Lookup Pattern:**

```markdown
## Lookup Pattern

**Query:** "What are the chronic disease rates in Miami-Dade County?"

**Steps:**
1. Read `data/county/places_county_2024.csv`
2. Filter: CountyFIPS = "12086" (Miami-Dade)
3. Filter: Category = "Health Outcomes"
4. Return all measures with Data_Value

**Sample Output:**
| Condition | Miami-Dade | Florida | National |
|-----------|------------|---------|----------|
| Diabetes | 13.2% | 11.2% | 10.1% |
| Obesity | 29.8% | 30.4% | 32.1% |
| Hypertension | 32.1% | 31.8% | 32.4% |
```

#### 3.2 Update `health-patterns/health-behavior-patterns.md`

Add lookup patterns for:
- CSMOKING (smoking)
- BINGE (binge drinking)
- LPA (physical inactivity)
- SLEEP (short sleep)

#### 3.3 Update `health-patterns/healthcare-access-analysis.md`

Note: SVI tract file has E_UNINSUR and EP_UNINSUR columns.

#### 3.4 Update `health-patterns/health-outcome-disparities.md`

Add pattern for comparing tract-level data to identify disparities.

---

### Step 4: Update SDOH Skills

#### 4.1 Update `sdoh/svi-analysis.md`

**Major Update Required:**

1. **Add SVI Column Reference:**

```markdown
## SVI Data Structure

### Theme Rankings (0-1 scale, higher = more vulnerable)
| Column | Description |
|--------|-------------|
| RPL_THEMES | Overall SVI ranking |
| RPL_THEME1 | Socioeconomic Status |
| RPL_THEME2 | Household Characteristics |
| RPL_THEME3 | Racial/Ethnic Minority Status |
| RPL_THEME4 | Housing Type/Transportation |

### Theme 1: Socioeconomic Status Variables
| Column | Description |
|--------|-------------|
| E_POV150 | Persons below 150% poverty (count) |
| EP_POV150 | Persons below 150% poverty (%) |
| E_UNEMP | Unemployed civilians 16+ (count) |
| EP_UNEMP | Unemployment rate (%) |
| E_HBURD | Housing cost burdened (count) |
| EP_HBURD | Housing cost burdened (%) |
| E_NOHSDP | No high school diploma 25+ (count) |
| EP_NOHSDP | No high school diploma (%) |
| E_UNINSUR | Uninsured (count) |
| EP_UNINSUR | Uninsured (%) |

### Demographics (from SVI tract file)
The SVI tract file includes extensive ACS demographics:
| Prefix | Content |
|--------|---------|
| E_TOTPOP | Total population |
| EP_AGE65, EP_AGE17 | Age distributions |
| EP_MINRTY | Minority percentage |
| EP_LIMENG | Limited English |
```

2. **Add Data Lookup Pattern:**

```markdown
## Lookup Pattern: County SVI

**Query:** "What is the SVI for Cook County, IL?"

**Steps:**
1. Read `data/county/svi_county_2022.csv`
2. Filter: FIPS = "17031" (Cook County)
3. Extract theme rankings

**Response:**
Cook County, IL (FIPS 17031) Social Vulnerability Index:

| Theme | Ranking | Interpretation |
|-------|---------|----------------|
| **Overall SVI** | 0.78 | High vulnerability (78th percentile) |
| Socioeconomic | 0.72 | High |
| Household Characteristics | 0.68 | Moderate-High |
| Minority/Language | 0.89 | Very High |
| Housing/Transportation | 0.71 | High |

*Source: CDC/ATSDR SVI 2022 (2018-2022 ACS data)*
```

#### 4.2 Update `sdoh/adi-analysis.md`

**Major Update Required:**

1. **Add ADI Data Reference:**

```markdown
## ADI Data Structure

| Column | Description | Values |
|--------|-------------|--------|
| FIPS | 12-digit block group FIPS | e.g., "482012111001" |
| ADI_NATRANK | National percentile | 1-100 or suppression code |
| ADI_STATERNK | State decile | 1-10 or suppression code |

### Suppression Codes
| Code | Meaning |
|------|---------|
| GQ | >33% group quarters housing |
| PH | Population <100 or <30 housing units |
| GQ-PH | Both conditions |
| QDI | Missing key demographic factor |
```

2. **Add Lookup and Aggregation Patterns:**

```markdown
## Lookup Pattern: Block Group ADI

**Query:** "What is the ADI for block group 482012111001?"

**Steps:**
1. Read `data/block_group/adi_blockgroup_2023.csv`
2. Filter: FIPS = "482012111001"
3. Extract ADI_NATRANK and ADI_STATERNK

**Response:**
Block Group 482012111001 (Harris County, TX):
- **National Rank:** 71st percentile (higher deprivation than 71% of US block groups)
- **State Decile:** 4 (moderate deprivation within Texas)

*Source: Neighborhood Atlas ADI 2023 v4.0.1*

## Aggregation Pattern: Tract ADI

To get ADI for a census tract, aggregate its block groups:

**Steps:**
1. Read ADI file
2. Filter: FIPS starts with tract FIPS (first 11 digits)
3. Average ADI_NATRANK across block groups (exclude suppressed)
4. Report as "estimated tract ADI"

**Example:**
Tract 48201211100 has 4 block groups:
- 482012111001: ADI 71
- 482012111002: ADI 79
- 482012111003: ADI 65
- 482012111004: ADI 73

**Tract Estimated ADI:** 72 (average)
```

#### 4.3 Update `sdoh/economic-indicators.md`

Add lookup patterns for SVI economic variables (E_POV150, E_UNEMP, etc.)

#### 4.4 Update `sdoh/community-factors.md`

Add lookup patterns for housing/transportation variables from SVI Theme 4.

---

### Step 5: Update Cohort Skills

#### 5.1 Update `cohorts/cohort-specification.md`

Add section on using real data for cohort specifications:

```markdown
## Data-Driven Cohort Specifications

When creating cohorts for specific geographies, use embedded data:

### Demographic Distributions
Read from SVI tract file (aggregated to specified geography):
- EP_AGE65, EP_AGE17 for age brackets
- EP_MINRTY for minority percentage
- Compute sex distribution from tract data

### Clinical Prevalence Rates
Read from PLACES county/tract files:
- Use actual prevalence rates for the geography
- Comorbidity rates for the primary condition

### SDOH Profile
Read from SVI and ADI files:
- Actual SVI theme rankings
- ADI distribution within geography
```

#### 5.2 Update `cohorts/demographic-distribution.md`

Show how to pull real age/sex/race distributions from SVI data.

#### 5.3 Update `cohorts/clinical-prevalence-profile.md`

Show how to pull real condition prevalence from PLACES data.

#### 5.4 Update `cohorts/sdoh-profile-builder.md`

Show how to build real SDOH profiles from SVI + ADI data.

---

### Step 6: Update Master SKILL.md

Add new data-access category to Quick Reference table and directory structure:

```markdown
## Quick Reference (add row)

| I want to... | Use This Skill | Key Triggers |
|--------------|----------------|--------------|
| Look up real data values | `data-access/data-lookup.md` | "exact", "look up", "from PLACES" |
| Resolve FIPS codes | `data-access/geography-lookup.md` | "FIPS for", "what county is" |
| Aggregate geographic data | `data-access/data-aggregation.md` | "aggregate", "summarize tracts" |

## Directory Structure (add section)

├── data-access/                       # Data Package Access (v2.0)
│   ├── README.md                      # Data access overview
│   ├── data-lookup.md                 # Direct value lookups
│   ├── geography-lookup.md            # FIPS resolution
│   └── data-aggregation.md            # Geographic aggregation
```

Add new trigger phrases:
```markdown
### Data Access (NEW)
- "What is the exact [measure] in [geography]?"
- "Look up [measure] from CDC PLACES"
- "What's the SVI for [geography]?"
- "Find the ADI for [block group]"
- "Which tracts in [county] have highest [measure]?"
```

---

### Step 7: Update Reference Files

#### 7.1 Update `references/cdc-places-measures.md`

Add column name mappings from data files.

#### 7.2 Update `references/svi-variables.md`

Add column name mappings and E_/EP_ prefix explanations.

#### 7.3 Update `data-sources.md`

Complete overhaul to document embedded data package.

---

## Post-Flight Checklist

After completing all updates:

- [ ] All 4 new data-access skills created
- [ ] All geographic skills updated with data lookup patterns
- [ ] All health-patterns skills updated with PLACES references
- [ ] All SDOH skills updated with SVI/ADI lookups
- [ ] All cohort skills updated with real data patterns
- [ ] SKILL.md updated with new category and triggers
- [ ] Reference files updated with column mappings
- [ ] At least 2 examples per skill use REAL data values
- [ ] Every data value includes source citation
- [ ] Git commit with descriptive message
- [ ] Git push to origin

---

## Verification Tests

After implementation, test these queries:

### Test 1: County Health Lookup
**Query:** "What is the diabetes prevalence in Harris County, TX?"
**Expected:** Exact value from PLACES file with CDC source citation

### Test 2: Tract SVI Lookup  
**Query:** "Show the SVI for census tract 06037204920 in Los Angeles"
**Expected:** All four SVI theme rankings with CDC/ATSDR source

### Test 3: Block Group ADI
**Query:** "What's the ADI for block group 170312801001?"
**Expected:** National rank and state decile with Neighborhood Atlas source

### Test 4: County Comparison
**Query:** "Compare obesity rates in Miami-Dade FL vs Harris TX"
**Expected:** Both exact values from PLACES with comparison

### Test 5: Metro Aggregation
**Query:** "What's the average diabetes rate across the Houston MSA?"
**Expected:** Aggregated value from 9-county MSA with methodology note

### Test 6: High-Vulnerability Tracts
**Query:** "Which tracts in Cook County IL have SVI above 0.9?"
**Expected:** List of specific tract FIPS with their SVI scores

---

## Success Criteria

Phase 2 is complete when:

1. ✅ All skills can look up real values from embedded data files
2. ✅ Every data value includes source and vintage citation
3. ✅ Examples show actual data values (not synthesized)
4. ✅ Graceful handling when data is missing (clear message)
5. ✅ Aggregation patterns documented and demonstrated
6. ✅ Cross-references between skills are working
7. ✅ Master SKILL.md routes correctly to new data-access category

---

## Session Plan

This phase should take **2-3 sessions**:

| Session | Focus | Deliverables |
|---------|-------|--------------|
| 2A | Data Access Category | Create all 4 data-access skills |
| 2B | Geographic + Health Skills | Update 8 geographic/health-patterns skills |
| 2C | SDOH + Cohort + Master | Update SDOH/cohort skills, SKILL.md, references |

---

## Git Commit Message Template

```
[PopulationSim] Phase 2 - Skills Integration with Embedded Data

- Created data-access skill category (4 new skills)
- Updated geographic skills with data lookup patterns
- Updated health-patterns skills with PLACES references
- Updated SDOH skills with SVI/ADI lookups
- Updated cohort skills with real data patterns
- Updated SKILL.md with new category routing
- Updated reference files with column mappings

All skills now read from embedded data package (148 MB)
with full source provenance in responses.
```

---

*Document Version: 1.0*
*Created: December 2024*
*Purpose: Phase 2 Implementation Guide*
