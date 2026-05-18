---
name: populationsim-geographic
description: >
  Geographic intelligence skills for PopulationSim. Use for county profiles,
  census tract analysis, metro area profiles, and custom region building.
  Provides demographic, health, and SDOH data for geographic areas.
---

# Geographic Intelligence Skills

## Overview

Geographic intelligence skills profile geographic areas at multiple levels of granularity, from metro areas down to individual census tracts. These skills combine Census ACS demographics with CDC PLACES health indicators and SDOH indices to create comprehensive geographic profiles.

**Key Capability**: Transform geography identifiers (FIPS codes, county names, metro areas) into rich PopulationProfile objects that can drive cohort definition and synthetic data generation.

---

## Skills in This Category

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [county-profile.md](county-profile.md) | County-level comprehensive profiles | "county profile", "demographics for [county]" |
| [census-tract-analysis.md](census-tract-analysis.md) | Tract-level granular analysis | "tract level", "hotspots", "vulnerable tracts" |
| [metro-area-profile.md](metro-area-profile.md) | MSA/CBSA aggregate profiles | "metro", "MSA", "metropolitan area" |
| [custom-region-builder.md](custom-region-builder.md) | User-defined region profiles | "service area", "combine counties", "custom region" |

---

## Common Output: PopulationProfile

All geographic skills output PopulationProfile objects with consistent structure:

```json
{
  "geography": {
    "type": "county|tract|msa|custom",
    "fips": "06073",
    "name": "San Diego County",
    "state": "CA",
    "parent": { "type": "state", "fips": "06", "name": "California" }
  },
  "demographics": {
    "total_population": 3286069,
    "population_density": 775.2,
    "median_age": 37.1,
    "age_distribution": { "0-17": 0.21, "18-64": 0.62, "65+": 0.17 },
    "race_ethnicity": { "white_nh": 0.43, "hispanic": 0.34, "asian": 0.12 },
    "median_household_income": 102285,
    "poverty_rate": 0.103
  },
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "diabetes_prevalence": 0.095,
    "obesity_prevalence": 0.280,
    "hypertension_prevalence": 0.285
  },
  "sdoh_indices": {
    "svi_overall": 0.42,
    "svi_themes": { "socioeconomic": 0.38, "household_composition": 0.45 },
    "adi_national_rank": 35
  },
  "healthcare_access": {
    "uninsured_rate": 0.071,
    "pcp_per_100k": 82.4,
    "insurance_mix": { "employer": 0.52, "medicaid": 0.18, "medicare": 0.15 }
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "data_vintage": { "census": "ACS_2022_5yr", "health": "CDC_PLACES_2024" }
  }
}
```

---

## Geographic Hierarchy

```
Nation
  └── Region (4)
      └── Division (9)
          └── State (50 + DC)
              └── County (3,143)
                  └── Census Tract (~85,000)
                      └── Block Group (~240,000)
```

### FIPS Code Structure

| Level | Format | Example | Description |
|-------|--------|---------|-------------|
| State | 2 digits | `06` | California |
| County | 5 digits | `06073` | San Diego County, CA |
| Tract | 11 digits | `06073008346` | Tract within San Diego |
| Block Group | 12 digits | `060730083461` | Block group within tract |

### Metropolitan Statistical Areas

- **CBSA Code**: 5-digit Core Based Statistical Area identifier
- **MSA**: Metropolitan Statistical Area (urban core ≥50,000)
- **μSA**: Micropolitan Statistical Area (urban core 10,000-49,999)

---

## Data Sources by Geography Level

| Level | ACS | CDC PLACES | SVI | ADI |
|-------|-----|------------|-----|-----|
| Nation | ✓ 1-year | ✓ | - | - |
| State | ✓ 1-year | ✓ | - | - |
| County | ✓ 1-year (pop ≥65K) | ✓ | ✓ | - |
| Tract | ✓ 5-year only | ✓ | ✓ | - |
| Block Group | ✓ 5-year only | - | - | ✓ |

---

## Skill Selection Guide

### Use county-profile.md when:
- Need comprehensive county-level overview
- Comparing counties within or across states
- Regional health department planning
- Service area demographic analysis

### Use census-tract-analysis.md when:
- Need neighborhood-level granularity
- Identifying health hotspots or vulnerable areas
- Targeting community health interventions
- SDOH analysis at local level

### Use metro-area-profile.md when:
- Analyzing urban markets
- Multi-county metropolitan planning
- Comparing metro areas nationally
- Site selection across metro areas

### Use custom-region-builder.md when:
- Defining multi-county service areas
- Creating custom aggregations
- Hospital catchment area analysis
- Non-standard geographic units

---

## Quick Examples

### County Profile
```
"Profile San Diego County health indicators"
→ PopulationProfile for FIPS 06073 with full demographics, CDC PLACES measures, SVI
```

### Tract Hotspots
```
"Find high-SVI census tracts in Los Angeles County"
→ List of tracts with SVI ≥ 0.75 and their characteristics
```

### Metro Comparison
```
"Compare Houston and Dallas metro areas for diabetes prevalence"
→ Two PopulationProfiles with MSA-aggregated data and comparison
```

### Custom Region
```
"Create a profile for our service area: Harris, Fort Bend, and Montgomery counties TX"
→ Aggregated PopulationProfile for the 3-county region
```

---

## Integration with Other Skills

### → Cohort Definition
Geographic profiles provide the foundation for cohort specification:
```
Geographic Profile → Cohort Filter → CohortSpecification
```

### → Trial Support
Geographic analysis feeds site selection:
```
Metro Profiles → Disease Prevalence Ranking → Site Selection
```

### → PatientSim/MemberSim
Geographic characteristics drive synthetic data:
```
County Profile → Demographic Distribution → Patient Demographics
```

---

## Validation Notes

### Data Quality Indicators

| Indicator | Meaning |
|-----------|---------|
| ✓ High confidence | Large population, CV < 15% |
| ~ Moderate | Medium population, CV 15-30% |
| ⚠️ Use with caution | Small population, CV > 30% |

### Common Validation Checks

- [ ] FIPS code valid and exists
- [ ] Population ≥ threshold for reliable estimates
- [ ] Data vintage noted in metadata
- [ ] Age-adjusted rates used for comparisons

---

## Related Skills

- [Population Intelligence Domain](../population-intelligence-domain.md) - Core concepts
- [Health Patterns](../health-patterns/README.md) - Disease analysis
- [SDOH Analysis](../sdoh/README.md) - SVI, ADI deep dives
- [Cohort Definition](../cohorts/README.md) - Cohort specs from profiles
