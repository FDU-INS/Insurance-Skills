---
name: geography-lookup
description: >
  Resolve FIPS codes, find geographies by name, and navigate geographic hierarchies.
  Use for queries like "what's the FIPS for Harris County", "which state is 48",
  "what county is tract X in", or "list counties in Houston MSA".
  Triggers: "FIPS code", "which county", "what state", "list counties in"
---

# Geography Lookup Skill

## Overview

The geography-lookup skill resolves geographic identifiers using PopulationSim's embedded crosswalk files. Use this when you need to:
- Convert county names to FIPS codes (and vice versa)
- Identify which county a tract belongs to
- List counties in a metropolitan area (CBSA)
- Validate geographic codes

## Trigger Phrases

- "What's the FIPS code for [county], [state]?"
- "Which state is FIPS [code]?"
- "What county is tract [FIPS] in?"
- "List counties in the [metro area] MSA"
- "What's the CBSA code for [metro]?"
- "Is [FIPS] a valid county code?"
- "Which counties are in CBSA [code]?"

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lookup_type | string | Yes | "state", "county", "tract", or "cbsa" |
| input | string | Yes | Name or FIPS code to look up |
| state | string | Conditional | Required for ambiguous county names |

## Crosswalk Files

### State FIPS Codes
**File:** `data/crosswalks/fips_state.csv`
**Columns:** state_fips, state_name, state_abbr
**Records:** 51 (50 states + DC)

### County FIPS Codes
**File:** `data/crosswalks/fips_county.csv`
**Columns:** state_fips, state_abbr, county_fips, county_name
**Records:** 3,144

### Tract to County Mapping
**File:** `data/crosswalks/tract_to_county.csv`
**Columns:** tract_fips, county_fips, state_abbr, county_name, tract_name
**Records:** 84,120

### CBSA Definitions
**File:** `data/crosswalks/cbsa_definitions.csv`
**Columns:** county_fips, cbsa_code, cbsa_title, cbsa_type, csa_code, csa_title, central_outlying
**Records:** 1,918 county-CBSA mappings (937 unique CBSAs)

## FIPS Code Structure

### State FIPS (2 digits)
```
06 = California
48 = Texas
17 = Illinois
```

### County FIPS (5 digits)
```
State (2) + County (3)
48201 = Harris County, TX (48 = TX, 201 = Harris)
06073 = San Diego County, CA (06 = CA, 073 = San Diego)
17031 = Cook County, IL (17 = IL, 031 = Cook)
```

### Tract FIPS (11 digits)
```
State (2) + County (3) + Tract (6)
48201311500 = Tract 3115 in Harris County, TX
06073008300 = Tract 83 in San Diego County, CA
```

### Block Group FIPS (12 digits)
```
State (2) + County (3) + Tract (6) + Block Group (1)
482012104001 = Block Group 1, Tract 2104, Harris County, TX
```

## Generation Patterns

### Pattern 1: County Name to FIPS

**Input:** "What's the FIPS for Harris County, Texas?"

**Process:**
1. Read `data/crosswalks/fips_county.csv`
2. Filter: county_name = "Harris" AND state_abbr = "TX"
3. Return county_fips

**Response:**
Harris County, Texas has FIPS code **48201**.

| Component | Value |
|-----------|-------|
| State FIPS | 48 |
| County Code | 201 |
| Full FIPS | 48201 |

---

### Pattern 2: FIPS to County Name

**Input:** "Which county is 06073?"

**Process:**
1. Read `data/crosswalks/fips_county.csv`
2. Filter: county_fips = "06073"
3. Return county_name, state_abbr

**Response:**
FIPS 06073 is **San Diego County, California**.

---

### Pattern 3: Tract to County

**Input:** "What county is census tract 48201311500 in?"

**Process:**
1. Extract county FIPS from tract (first 5 digits): 48201
2. Read `data/crosswalks/fips_county.csv`
3. Look up county name

**Response:**
Census tract 48201311500 is in **Harris County, Texas** (county FIPS 48201).

The tract portion is 311500, which is tract 3115.00.

---

### Pattern 4: CBSA Lookup

**Input:** "List the counties in the Houston MSA"

**Process:**
1. Read `data/crosswalks/cbsa_definitions.csv`
2. Filter: cbsa_title contains "Houston"
3. Return all matching counties

**Response:**
**Houston-The Woodlands-Sugar Land, TX MSA** (CBSA 26420)

| County | FIPS | Role |
|--------|------|------|
| Harris | 48201 | Central |
| Fort Bend | 48157 | Central |
| Montgomery | 48339 | Central |
| Brazoria | 48039 | Outlying |
| Galveston | 48167 | Outlying |
| Liberty | 48291 | Outlying |
| Waller | 48473 | Outlying |
| Chambers | 48071 | Outlying |
| Austin | 48015 | Outlying |

Total: 9 counties

---

### Pattern 5: Ambiguous County Resolution

**Input:** "What's the FIPS for Washington County?"

**Process:**
1. Read `data/crosswalks/fips_county.csv`
2. Filter: county_name = "Washington"
3. Find multiple matches → request clarification

**Response:**
"Washington County" exists in **30 states**. Please specify the state.

Common ones include:
- Washington County, PA (42125)
- Washington County, OR (41067)
- Washington County, MN (27163)
- Washington County, TX (48477)

Which state did you mean?

---

### Pattern 6: State FIPS Lookup

**Input:** "What state is FIPS 48?"

**Process:**
1. Read `data/crosswalks/fips_state.csv`
2. Filter: state_fips = "48"
3. Return state_name, state_abbr

**Response:**
State FIPS 48 is **Texas (TX)**.

---

## Examples

### Example 1: Simple County Lookup

**User:** "FIPS code for Cook County, Illinois"

**Claude:** Cook County, Illinois has FIPS code **17031**.
- State FIPS: 17 (Illinois)
- County Code: 031

---

### Example 2: Metro Area Counties

**User:** "What counties are in the San Diego metro area?"

**Claude:** **San Diego-Chula Vista-Carlsbad, CA MSA** (CBSA 41740)

This is a single-county MSA consisting only of:
- **San Diego County** (FIPS 06073) - Central

San Diego MSA has a population of approximately 3.3 million.

---

### Example 3: Block Group Context

**User:** "What's the geographic context for block group 170318414001?"

**Claude:** **Block Group 170318414001** Geographic Hierarchy:

| Level | Code | Name |
|-------|------|------|
| State | 17 | Illinois |
| County | 17031 | Cook County |
| Tract | 17031841400 | Census Tract 8414 |
| Block Group | 170318414001 | Block Group 1 |

This block group is located in Cook County, Illinois (Chicago area).

---

### Example 4: Multi-County Metro

**User:** "Show me the Dallas-Fort Worth metro composition"

**Claude:** **Dallas-Fort Worth-Arlington, TX MSA** (CBSA 19100)

| County | FIPS | Population | Role |
|--------|------|------------|------|
| Dallas | 48113 | 2,613,539 | Central |
| Tarrant | 48439 | 2,110,640 | Central |
| Collin | 48085 | 1,064,465 | Central |
| Denton | 48121 | 906,422 | Central |
| Ellis | 48139 | 192,455 | Outlying |
| Johnson | 48251 | 179,927 | Outlying |
| Kaufman | 48257 | 145,310 | Outlying |
| Parker | 48367 | 148,222 | Outlying |
| Rockwall | 48397 | 107,819 | Outlying |
| Wise | 48497 | 72,542 | Outlying |
| Hunt | 48231 | 99,514 | Outlying |
| Hood | 48221 | 65,454 | Outlying |
| Somervell | 48425 | 9,128 | Outlying |

Total: 13 counties, ~7.7 million population

---

## Validation Rules

### FIPS Validation
- State FIPS: 2 digits, 01-56 (with gaps)
- County FIPS: 5 digits, valid state prefix
- Tract FIPS: 11 digits, valid county prefix
- Block Group FIPS: 12 digits, valid tract prefix

### Name Matching
- Case-insensitive matching
- Handle common variations ("St." vs "Saint")
- Require state for ambiguous county names

### Error Handling
- Invalid FIPS: "FIPS code [X] is not valid. Check the format."
- Not found: "No geography found matching [X]."
- Ambiguous: List all matches, request clarification

---

## Related Skills

- [data-lookup.md](data-lookup.md) - Look up data values for resolved geographies
- [data-aggregation.md](data-aggregation.md) - Aggregate data across geographies
- [../geographic/county-profile.md](../geographic/county-profile.md) - Full county profiles
- [../geographic/metro-area-profile.md](../geographic/metro-area-profile.md) - MSA profiles
