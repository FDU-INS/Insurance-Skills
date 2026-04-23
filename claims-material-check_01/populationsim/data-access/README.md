---
name: populationsim-data-access
description: >
  Skills for directly accessing PopulationSim's embedded data package.
  Use these skills when you need to look up specific values, resolve
  geography codes, or aggregate data across geographic levels.
  Triggers: "look up", "exact value", "FIPS code", "aggregate tracts"
---

# Data Access Skills

## Overview

PopulationSim v2.0 includes an **embedded data package** (148 MB) with real demographic, health, and SDOH data covering 100% of US geography. These skills provide direct access patterns for reading and aggregating this data.

**Key Principle**: Every response that includes data from these files must cite the source and vintage.

## Data Package Summary

| Level | Files | Records | Key Data |
|-------|-------|---------|----------|
| County | 2 | ~3,144 | CDC PLACES health measures, SVI rankings |
| Tract | 2 | ~84,000 | CDC PLACES health measures, SVI full dataset |
| Block Group | 1 | ~242,000 | ADI national/state rankings |
| Crosswalks | 4 | Various | FIPS codes, CBSA definitions |

## Skills in This Category

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [data-lookup.md](data-lookup.md) | Look up specific values by geography | "what is the diabetes rate", "look up SVI" |
| [geography-lookup.md](geography-lookup.md) | Resolve FIPS codes, find geographies | "FIPS for", "which county", "what state" |
| [data-aggregation.md](data-aggregation.md) | Aggregate across geographic levels | "aggregate tracts", "metro area totals" |

## Data File Locations

All data files are in `skills/populationsim/data/`:

```
data/
├── README.md                          # Complete data dictionary
├── county/
│   ├── places_county_2024.csv         # CDC PLACES (40 measures, 3,143 counties)
│   └── svi_county_2022.csv            # SVI aggregated (3,144 counties)
├── tract/
│   ├── places_tract_2024.csv          # CDC PLACES (40 measures, 83,522 tracts)
│   └── svi_tract_2022.csv             # SVI full dataset (84,120 tracts, 158 columns)
├── block_group/
│   ├── adi_blockgroup_2023.csv        # ADI rankings (242,336 block groups)
│   └── adi_readme.txt                 # ADI documentation
└── crosswalks/
    ├── fips_state.csv                 # State FIPS codes (51 entries)
    ├── fips_county.csv                # County FIPS codes (3,144 entries)
    ├── tract_to_county.csv            # Tract-to-county mapping (84,120 entries)
    └── cbsa_definitions.csv           # Metro/micro area definitions (937 CBSAs)
```

## Data Provenance Principle

**Every data value returned must include its source.** Standard format:

```
Harris County, TX has a diabetes prevalence of **13.2%** among adults.

*Source: CDC PLACES 2024 Release (2022 BRFSS data)*
```

For JSON output:
```json
{
  "value": 13.2,
  "unit": "percent",
  "source": "CDC PLACES 2024",
  "data_year": "2022 BRFSS",
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County, TX"
  },
  "measure": "DIABETES_CrudePrev"
}
```

## Quick Examples

### County Health Lookup
**Query:** "What is the obesity rate in Cook County, IL?"
**Answer:** Cook County, IL has an obesity prevalence of **31.0%** among adults.
*Source: CDC PLACES 2024 Release*

### County SVI Lookup
**Query:** "What's the SVI for Harris County, TX?"
**Answer:** Harris County, TX has an overall SVI of **0.633** (moderate-high vulnerability).
- Socioeconomic: 0.671
- Household Characteristics: 0.586
- Minority/Language: 0.794
- Housing/Transportation: 0.478
*Source: CDC/ATSDR SVI 2022*

### Block Group ADI
**Query:** "What's the ADI for block group 482012104001?"
**Answer:** Block group 482012104001 (Harris County, TX):
- National Percentile: **46** (lower-moderate deprivation)
- State Decile: **4**
*Source: Neighborhood Atlas ADI 2023 v4.0.1*

## Related Categories

- [geographic/](../geographic/) - County, tract, and metro area profiles
- [health-patterns/](../health-patterns/) - Disease prevalence and health behaviors
- [sdoh/](../sdoh/) - Social determinants analysis
- [cohorts/](../cohorts/) - Cohort specification with real data
