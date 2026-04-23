---
name: fips-codes
description: >
  Federal Information Processing Standard (FIPS) geographic codes reference
  including structure, hierarchy, and lookup guidance.
---

# FIPS Geographic Codes Reference

## Overview

FIPS codes are standardized numeric codes that identify geographic entities. PopulationSim uses FIPS codes as the primary geographic identifier for all population intelligence operations.

**Authority**: U.S. Census Bureau (formerly NIST)
**Standard**: FIPS 5-2 (States), FIPS 6-4 (Counties)
**Note**: FIPS standards were officially withdrawn in 2008 but codes remain in widespread use

---

## Code Structure

### State Codes (2 digits)

| Code | State | Code | State |
|------|-------|------|-------|
| 01 | Alabama | 28 | Mississippi |
| 02 | Alaska | 29 | Missouri |
| 04 | Arizona | 30 | Montana |
| 05 | Arkansas | 31 | Nebraska |
| 06 | California | 32 | Nevada |
| 08 | Colorado | 33 | New Hampshire |
| 09 | Connecticut | 34 | New Jersey |
| 10 | Delaware | 35 | New Mexico |
| 11 | District of Columbia | 36 | New York |
| 12 | Florida | 37 | North Carolina |
| 13 | Georgia | 38 | North Dakota |
| 15 | Hawaii | 39 | Ohio |
| 16 | Idaho | 40 | Oklahoma |
| 17 | Illinois | 41 | Oregon |
| 18 | Indiana | 42 | Pennsylvania |
| 19 | Iowa | 44 | Rhode Island |
| 20 | Kansas | 45 | South Carolina |
| 21 | Kentucky | 46 | South Dakota |
| 22 | Louisiana | 47 | Tennessee |
| 23 | Maine | 48 | Texas |
| 24 | Maryland | 49 | Utah |
| 25 | Massachusetts | 50 | Vermont |
| 26 | Michigan | 51 | Virginia |
| 27 | Minnesota | 53 | Washington |
| | | 54 | West Virginia |
| | | 55 | Wisconsin |
| | | 56 | Wyoming |

*Note: Codes 03, 07, 14, 43, 52 are not used*

### Territories

| Code | Territory |
|------|-----------|
| 60 | American Samoa |
| 66 | Guam |
| 69 | Northern Mariana Islands |
| 72 | Puerto Rico |
| 78 | U.S. Virgin Islands |

---

## County Codes (5 digits)

Format: `SS-CCC` (State + County)

### Examples

| FIPS | County |
|------|--------|
| 06037 | Los Angeles County, CA |
| 48201 | Harris County, TX |
| 17031 | Cook County, IL |
| 04013 | Maricopa County, AZ |
| 36061 | New York County (Manhattan), NY |

### Special Cases

| Type | Example | Note |
|------|---------|------|
| Independent Cities | 51760 (Richmond, VA) | Virginia cities |
| Parishes | 22071 (Orleans Parish, LA) | Louisiana |
| Boroughs | 02020 (Anchorage, AK) | Alaska |
| Census Areas | 02090 (Fairbanks North Star, AK) | Alaska unorganized |

---

## Census Tract Codes (11 digits)

Format: `SSCCCTTTTTT` (State + County + Tract)

### Structure

```
06 037 2010.01
│  │    │    │
│  │    │    └── Suffix (2 digits, optional)
│  │    └─────── Base tract (4 digits)
│  └──────────── County (3 digits)
└─────────────── State (2 digits)
```

### Examples

| FIPS | Description |
|------|-------------|
| 06037201001 | Tract 2010.01 in Los Angeles County, CA |
| 48201311100 | Tract 3111.00 in Harris County, TX |
| 17031839100 | Tract 8391.00 in Cook County, IL |

---

## Block Group Codes (12 digits)

Format: `SSCCCTTTTTTB` (State + County + Tract + Block Group)

Block group is a single digit (1-9) appended to tract code.

### Example

```
06037201001 2
│           │
│           └── Block group 2
└───────────── Census tract
```

---

## CBSA Codes (5 digits)

Core Based Statistical Areas (Metropolitan and Micropolitan)

### Largest MSAs by CBSA Code

| CBSA | MSA Name | Population |
|------|----------|------------|
| 35620 | New York-Newark-Jersey City | 19.6M |
| 31080 | Los Angeles-Long Beach-Anaheim | 12.9M |
| 16980 | Chicago-Naperville-Elgin | 9.4M |
| 19100 | Dallas-Fort Worth-Arlington | 7.6M |
| 26420 | Houston-The Woodlands-Sugar Land | 7.2M |
| 47900 | Washington-Arlington-Alexandria | 6.3M |
| 37980 | Philadelphia-Camden-Wilmington | 6.2M |
| 12060 | Atlanta-Sandy Springs-Alpharetta | 6.1M |
| 33100 | Miami-Fort Lauderdale-Pompano Beach | 6.1M |
| 38060 | Phoenix-Mesa-Chandler | 5.0M |

---

## Geographic Hierarchy

```
Nation (00)
├── Region (1 digit)
│   └── Division (1 digit)
│       └── State (2 digits: 01-56)
│           ├── County (5 digits: SSCCC)
│           │   ├── Tract (11 digits: SSCCCTTTTTT)
│           │   │   └── Block Group (12 digits: SSCCCTTTTTB)
│           │   │       └── Block (15 digits)
│           │   └── Subdivision
│           └── Place (7 digits: SSPPPPP)
│
└── CBSA (5 digits, crosses state lines)
    └── Metropolitan Division
```

---

## Census Regions and Divisions

| Region | Division | States |
|--------|----------|--------|
| **Northeast (1)** | New England (1) | CT, ME, MA, NH, RI, VT |
| | Mid-Atlantic (2) | NJ, NY, PA |
| **Midwest (2)** | East North Central (3) | IL, IN, MI, OH, WI |
| | West North Central (4) | IA, KS, MN, MO, NE, ND, SD |
| **South (3)** | South Atlantic (5) | DE, DC, FL, GA, MD, NC, SC, VA, WV |
| | East South Central (6) | AL, KY, MS, TN |
| | West South Central (7) | AR, LA, OK, TX |
| **West (4)** | Mountain (8) | AZ, CO, ID, MT, NV, NM, UT, WY |
| | Pacific (9) | AK, CA, HI, OR, WA |

---

## Lookup Resources

### APIs

| Resource | URL |
|----------|-----|
| Census Geocoder | https://geocoding.geo.census.gov/ |
| TIGERweb | https://tigerweb.geo.census.gov/ |
| Census API | https://api.census.gov/ |

### Files

| Resource | Content |
|----------|---------|
| FIPS County Codes | Census gazetteer files |
| CBSA Delineations | OMB Bulletin files |
| ZIP-FIPS Crosswalk | HUD USPS Crosswalk |

---

## Related References

- [acs-tables.md](acs-tables.md) - ACS geography
- [county-profile.md](../geographic/county-profile.md) - County analysis
- [census-tract-analysis.md](../geographic/census-tract-analysis.md) - Tract analysis
