# Geography Codes Reference

## Overview

This reference documents the geographic coding systems used by PopulationSim for identifying and hierarchically organizing geographic entities. Understanding these codes is essential for querying population data and building cohort specifications.

---

## Geographic Hierarchy

```
Nation (USA)
  └── Region (4)
      └── Division (9)
          └── State (50 + DC + territories)
              └── County (3,143)
                  └── Census Tract (~85,000)
                      └── Block Group (~240,000)
                          └── Census Block (~11 million)
```

**PopulationSim Primary Levels**: State → County → Census Tract → Block Group

---

## FIPS Codes

### State FIPS Codes (2-digit)

| Code | State | Code | State | Code | State |
|------|-------|------|-------|------|-------|
| 01 | Alabama | 19 | Iowa | 37 | North Carolina |
| 02 | Alaska | 20 | Kansas | 38 | North Dakota |
| 04 | Arizona | 21 | Kentucky | 39 | Ohio |
| 05 | Arkansas | 22 | Louisiana | 40 | Oklahoma |
| 06 | California | 23 | Maine | 41 | Oregon |
| 08 | Colorado | 24 | Maryland | 42 | Pennsylvania |
| 09 | Connecticut | 25 | Massachusetts | 44 | Rhode Island |
| 10 | Delaware | 26 | Michigan | 45 | South Carolina |
| 11 | District of Columbia | 27 | Minnesota | 46 | South Dakota |
| 12 | Florida | 28 | Mississippi | 47 | Tennessee |
| 13 | Georgia | 29 | Missouri | 48 | Texas |
| 15 | Hawaii | 30 | Montana | 49 | Utah |
| 16 | Idaho | 31 | Nebraska | 50 | Vermont |
| 17 | Illinois | 32 | Nevada | 51 | Virginia |
| 18 | Indiana | 33 | New Hampshire | 53 | Washington |
| | | 34 | New Jersey | 54 | West Virginia |
| | | 35 | New Mexico | 55 | Wisconsin |
| | | 36 | New York | 56 | Wyoming |

### County FIPS Codes (5-digit)

Format: `{state_fips}{county_code}` (2 + 3 digits)

**Examples**:
| FIPS | County | State |
|------|--------|-------|
| 06037 | Los Angeles County | CA |
| 48201 | Harris County | TX |
| 17031 | Cook County | IL |
| 04013 | Maricopa County | AZ |
| 12086 | Miami-Dade County | FL |
| 36061 | New York County (Manhattan) | NY |
| 06073 | San Diego County | CA |
| 48113 | Dallas County | TX |

### Census Tract FIPS (11-digit)

Format: `{state_fips}{county_fips}{tract_code}` (2 + 3 + 6 digits)

**Examples**:
| FIPS | Description |
|------|-------------|
| 06037207100 | Tract 2071.00 in Los Angeles County, CA |
| 48201311500 | Tract 3115.00 in Harris County, TX |
| 17031839100 | Tract 8391.00 in Cook County, IL |

**Tract Code Format**: 
- 6 digits, usually displayed with decimal (e.g., 2071.00)
- Leading zeros preserved
- Range: 000100 to 999999

### Block Group FIPS (12-digit)

Format: `{tract_fips}{block_group}` (11 + 1 digit)

**Examples**:
| FIPS | Description |
|------|-------------|
| 060372071001 | Block Group 1 of Tract 2071.00, LA County |
| 060372071002 | Block Group 2 of Tract 2071.00, LA County |

**Block Group Codes**: 0-9 (typically 1-4 per tract)

---

## CBSA Codes (Metropolitan/Micropolitan Areas)

### Core Based Statistical Area (CBSA)

5-digit codes assigned by OMB for metropolitan and micropolitan statistical areas.

**Metropolitan Statistical Areas** (population ≥ 50,000):

| CBSA | Name | Principal City | Population |
|------|------|----------------|------------|
| 35620 | New York-Newark-Jersey City | New York | 19.8M |
| 31080 | Los Angeles-Long Beach-Anaheim | Los Angeles | 13.0M |
| 16980 | Chicago-Naperville-Elgin | Chicago | 9.5M |
| 19100 | Dallas-Fort Worth-Arlington | Dallas | 7.6M |
| 26420 | Houston-The Woodlands-Sugar Land | Houston | 7.1M |
| 47900 | Washington-Arlington-Alexandria | Washington | 6.3M |
| 33100 | Miami-Fort Lauderdale-Pompano Beach | Miami | 6.1M |
| 37980 | Philadelphia-Camden-Wilmington | Philadelphia | 6.1M |
| 12060 | Atlanta-Sandy Springs-Alpharetta | Atlanta | 6.0M |
| 38060 | Phoenix-Mesa-Chandler | Phoenix | 4.9M |
| 14460 | Boston-Cambridge-Newton | Boston | 4.9M |
| 41860 | San Francisco-Oakland-Berkeley | San Francisco | 4.7M |
| 40140 | Riverside-San Bernardino-Ontario | Riverside | 4.6M |
| 19820 | Detroit-Warren-Dearborn | Detroit | 4.3M |
| 42660 | Seattle-Tacoma-Bellevue | Seattle | 4.0M |

**Micropolitan Statistical Areas** (population 10,000-49,999):
- 5-digit codes in same format
- ~540 micropolitan areas nationally

### Combined Statistical Areas (CSA)

Larger groupings of adjacent CBSAs with economic ties.

| CSA | Name | Component CBSAs |
|-----|------|-----------------|
| 408 | New York-Newark | 35620, 35084, 35154, etc. |
| 348 | Los Angeles-Long Beach | 31080, 40140, 37100 |
| 176 | Chicago-Naperville | 16980, 16974, 28100 |

---

## Census Geographic Components

### Geographic Component Codes

Used in ACS data to identify summary levels.

| Code | Level | Description |
|------|-------|-------------|
| 010 | Nation | United States total |
| 020 | Region | Census regions (4) |
| 030 | Division | Census divisions (9) |
| 040 | State | States and DC |
| 050 | County | Counties and equivalents |
| 140 | Census Tract | Statistical subdivisions of counties |
| 150 | Block Group | Subdivisions of tracts |

### Census Regions and Divisions

| Region | Division | States |
|--------|----------|--------|
| **Northeast** | New England | CT, ME, MA, NH, RI, VT |
| | Middle Atlantic | NJ, NY, PA |
| **Midwest** | East North Central | IL, IN, MI, OH, WI |
| | West North Central | IA, KS, MN, MO, NE, ND, SD |
| **South** | South Atlantic | DE, DC, FL, GA, MD, NC, SC, VA, WV |
| | East South Central | AL, KY, MS, TN |
| | West South Central | AR, LA, OK, TX |
| **West** | Mountain | AZ, CO, ID, MT, NV, NM, UT, WY |
| | Pacific | AK, CA, HI, OR, WA |

---

## Urban/Rural Classification

### Urban Area Types

| Type | Definition | Example |
|------|------------|---------|
| Urbanized Area (UA) | Population ≥ 50,000 | Los Angeles UA |
| Urban Cluster (UC) | Population 2,500-49,999 | Sedona, AZ UC |
| Rural | Not in UA or UC | - |

### Rural-Urban Continuum Codes (RUCC)

| Code | Description |
|------|-------------|
| 1 | Metro - 1 million+ population |
| 2 | Metro - 250,000 to 1 million |
| 3 | Metro - fewer than 250,000 |
| 4 | Nonmetro - urban pop 20,000+, adjacent to metro |
| 5 | Nonmetro - urban pop 20,000+, not adjacent |
| 6 | Nonmetro - urban pop 2,500-19,999, adjacent |
| 7 | Nonmetro - urban pop 2,500-19,999, not adjacent |
| 8 | Nonmetro - completely rural, adjacent to metro |
| 9 | Nonmetro - completely rural, not adjacent |

---

## Usage in PopulationSim

### FIPS in CohortSpecification

```json
{
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County",
    "state": "TX",
    "state_fips": "48"
  }
}
```

### CBSA in MetroAreaProfile

```json
{
  "geography": {
    "type": "msa",
    "cbsa_code": "26420",
    "name": "Houston-The Woodlands-Sugar Land, TX",
    "component_counties": [
      {"fips": "48201", "name": "Harris"},
      {"fips": "48157", "name": "Fort Bend"},
      {"fips": "48339", "name": "Montgomery"}
    ]
  }
}
```

### Tract in CensusTractAnalysis

```json
{
  "geography": {
    "type": "tract",
    "geoid": "48201311500",
    "tract_code": "3115.00",
    "county_fips": "48201",
    "county_name": "Harris County",
    "state": "TX"
  }
}
```

---

## Data Sources

| Source | URL | Content |
|--------|-----|---------|
| Census Bureau | census.gov/geographies | Official FIPS codes |
| OMB Bulletins | whitehouse.gov/omb | CBSA definitions |
| Census TIGERweb | tigerweb.geo.census.gov | Geographic boundaries |
| American FactFinder | data.census.gov | Data by geography |

---

## Related References

- [Census Variables](census-variables.md) - ACS data dictionary
- [SVI Methodology](svi-methodology.md) - Uses tract-level geography
- [ADI Methodology](adi-methodology.md) - Uses block group geography
