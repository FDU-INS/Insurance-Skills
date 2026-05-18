---
name: custom-region-builder
description: >
  Build population profiles for custom-defined regions by aggregating counties,
  tracts, or ZIP codes. Use for hospital service areas, health plan markets,
  ACO territories, or any non-standard geographic definitions. Triggers:
  "service area", "combine counties", "custom region", "catchment area",
  "market area", "aggregate [counties/tracts]".
---

# Custom Region Builder Skill

## Overview

The custom-region-builder skill creates PopulationProfile objects for user-defined geographic regions by aggregating data from component counties, census tracts, or ZIP codes. This enables analysis of healthcare service areas, health plan markets, and other non-standard geographic units.

**Primary Use Cases**:
- Hospital/health system service area profiling
- Health plan market area analysis
- ACO attributed population characterization
- FQHC service area assessment
- Clinical trial catchment area analysis
- Custom regional comparisons

**Key Capability**: Combine arbitrary geographic units into a unified profile with proper aggregation methodology.

---

## Trigger Phrases

- "Create a profile for our service area: [list of counties]"
- "Combine [counties/tracts] into a custom region"
- "Profile our market area covering [geographies]"
- "What's the population for these counties together: [list]"
- "Build a catchment area profile for [counties]"
- "Aggregate demographics for [list of geographies]"
- "Custom region including [geography list]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `region_name` | string | No | "Custom Region" | Name for the custom region |
| `components` | array | Yes | - | List of geographic units to combine |
| `component_type` | string | No | "county" | "county", "tract", "zip", "cbsa" |
| `include_health` | boolean | No | true | Include health indicators |
| `include_sdoh` | boolean | No | true | Include SDOH indices |
| `include_breakdown` | boolean | No | true | Show component-level detail |
| `weighting` | string | No | "population" | How to weight: "population", "equal" |
| `boundary_buffer` | string | No | "none" | Include adjacent areas: "none", "adjacent_tracts" |

---

## Data Sources (Embedded v2.0)

Custom regions aggregate from embedded data files:

| Component Type | Health Data | SVI Data | ADI Data |
|----------------|-------------|----------|----------|
| County | `data/county/places_county_2024.csv` | `data/county/svi_county_2022.csv` | Aggregate from tracts |
| Tract | `data/tract/places_tract_2024.csv` | `data/tract/svi_tract_2022.csv` | Aggregate from block groups |
| Block Group | N/A | N/A | `data/block_group/adi_blockgroup_2023.csv` |

### Aggregation Process

```
1. Resolve all component identifiers to FIPS codes
2. Read data for each component from appropriate files
3. Calculate population-weighted averages for rates/percentages
4. Sum absolute counts (population, uninsured persons, etc.)
5. Return aggregate with per-component breakdown
```

### Helper Files
- `data/crosswalks/fips_county.csv` - County name → FIPS
- `data/crosswalks/tract_to_county.csv` - Tract → County mapping
- `data/crosswalks/cbsa_definitions.csv` - CBSA → County list

---

## Generation Patterns

### Pattern 1: Multi-County Service Area

**Input**: "Create a profile for our service area: Harris, Fort Bend, and Montgomery counties in Texas"

**Process**:
1. Validate all county identifiers
2. Pull ACS demographics for each county
3. Sum populations, calculate weighted averages
4. Pull and aggregate CDC PLACES health indicators
5. Calculate region-level SDOH from tract data
6. Assemble unified PopulationProfile

**Output**: Combined region profile with component breakdown

### Pattern 2: Tract-Based Catchment

**Input**: "Build a catchment area from these census tracts: [list of 25 tracts]"

**Process**:
1. Validate all tract FIPS codes
2. Determine parent county/counties
3. Sum tract populations
4. Weight demographics by tract population
5. Aggregate health indicators and SDOH
6. Identify geographic extent

**Output**: Tract-aggregate profile

### Pattern 3: Multi-State Region

**Input**: "Profile the tri-state area: NY, NJ, and CT portions of the NYC metro"

**Process**:
1. Identify counties in NYC CBSA
2. Group by state
3. Create sub-region profiles
4. Aggregate to full region
5. Show state-by-state breakdown

**Output**: Multi-state region with sub-region detail

---

## Output Schema

```json
{
  "region": {
    "name": "Greater Houston Service Area",
    "type": "custom",
    "definition": {
      "component_type": "county",
      "component_count": 5,
      "components": [
        { "fips": "48201", "name": "Harris County, TX", "population": 4731145 },
        { "fips": "48157", "name": "Fort Bend County, TX", "population": 822779 },
        { "fips": "48339", "name": "Montgomery County, TX", "population": 620443 },
        { "fips": "48039", "name": "Brazoria County, TX", "population": 372031 },
        { "fips": "48167", "name": "Galveston County, TX", "population": 342139 }
      ],
      "states_included": ["TX"],
      "extent": {
        "north_county": "Montgomery",
        "south_county": "Galveston",
        "east_county": "Galveston",
        "west_county": "Fort Bend"
      }
    }
  },
  "demographics": {
    "total_population": 6888537,
    "land_area_sq_mi": 6789.4,
    "population_density": 1014.6,
    "median_age": 35.2,
    "age_distribution": {
      "0-17": 0.248,
      "18-64": 0.634,
      "65+": 0.118
    },
    "race_ethnicity": {
      "white_nh": 0.314,
      "hispanic": 0.368,
      "black": 0.172,
      "asian": 0.088,
      "other": 0.058
    },
    "median_household_income": 74850,
    "poverty_rate": 0.112
  },
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "aggregation_method": "population_weighted",
    "chronic_conditions": {
      "diabetes": 0.115,
      "obesity": 0.318,
      "hypertension": 0.312
    },
    "health_behaviors": {
      "smoking": 0.132,
      "physical_inactivity": 0.242
    }
  },
  "sdoh_indices": {
    "region_aggregate": {
      "svi_overall": 0.54,
      "svi_themes": {
        "socioeconomic": 0.48,
        "household_composition": 0.44,
        "minority_language": 0.72,
        "housing_transportation": 0.52
      }
    },
    "vulnerability_distribution": {
      "low_svi_tracts_pct": 0.28,
      "moderate_svi_tracts_pct": 0.38,
      "high_svi_tracts_pct": 0.34
    }
  },
  "healthcare_access": {
    "uninsured_rate": 0.154,
    "pcp_per_100k": 64.2,
    "hospital_count": 89,
    "fqhc_count": 124
  },
  "component_breakdown": {
    "by_county": [
      {
        "fips": "48201",
        "name": "Harris County",
        "population": 4731145,
        "pct_of_region": 0.687,
        "diabetes": 0.124,
        "svi": 0.68,
        "uninsured": 0.182
      },
      {
        "fips": "48157",
        "name": "Fort Bend County",
        "population": 822779,
        "pct_of_region": 0.119,
        "diabetes": 0.098,
        "svi": 0.32,
        "uninsured": 0.092
      }
    ],
    "variability": {
      "diabetes_range": [0.092, 0.124],
      "svi_range": [0.28, 0.68],
      "coefficient_of_variation": {
        "diabetes": 0.12,
        "svi": 0.34
      }
    }
  },
  "comparison_to_benchmarks": {
    "vs_texas": {
      "population_pct_of_state": 0.236,
      "diabetes_diff": 0.003,
      "svi_diff": -0.02
    },
    "vs_national": {
      "diabetes_diff": 0.014,
      "uninsured_diff": 0.066
    }
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "aggregation_notes": [
      "Demographics summed across components",
      "Health indicators population-weighted",
      "SVI aggregated from tract-level data"
    ],
    "data_vintage": {
      "census": "ACS_2022_5yr",
      "health": "CDC_PLACES_2024",
      "svi": "CDC_SVI_2022"
    }
  }
}
```

---

## Examples

### Example 1: Hospital Service Area

**Request**: "Create a profile for Memorial Hermann's primary service area: Harris, Fort Bend, Montgomery, and Galveston counties"

**Response**:

**Memorial Hermann Primary Service Area**

**Region Definition**:
- 4 counties in Southeast Texas
- Combined population: 6,546,506
- Land area: 5,892 sq mi

**Component Summary**:
| County | Population | % of Region | Median Income |
|--------|------------|-------------|---------------|
| Harris | 4,731,145 | 72.3% | $67,706 |
| Fort Bend | 822,779 | 12.6% | $108,432 |
| Montgomery | 620,443 | 9.5% | $94,287 |
| Galveston | 342,139 | 5.2% | $69,842 |

**Demographics**:
- Median Age: 35.1
- Race/Ethnicity: Hispanic 37%, White NH 31%, Black 17%, Asian 8%
- Median Household Income: $73,450
- Poverty Rate: 11.4%

**Health Profile**:
| Metric | Service Area | Texas | National |
|--------|--------------|-------|----------|
| Diabetes | 11.8% | 11.8% | 10.1% |
| Obesity | 32.4% | 33.2% | 32.1% |
| Uninsured | 15.8% | 17.5% | 8.8% ⚠️ |

**SDOH Analysis**:
- Overall SVI: 0.56 (moderate)
- High-SVI tracts: 28% of region
- Concentrated in: East Harris County, parts of Galveston

**Healthcare Infrastructure**:
- Hospitals: 72
- FQHCs: 98
- PCPs per 100K: 62.4

---

### Example 2: Multi-State Region

**Request**: "Profile the Cincinnati tri-state metro: Hamilton County OH, Boone/Kenton/Campbell counties KY, and Dearborn County IN"

**Response**:

**Cincinnati Tri-State Metro Region**

**Region Composition**:
| State | Counties | Population | % of Region |
|-------|----------|------------|-------------|
| Ohio | Hamilton | 830,639 | 40.2% |
| Kentucky | Boone, Kenton, Campbell | 445,912 | 21.6% |
| Indiana | Dearborn | 49,424 | 2.4% |
| **Total** | 5 counties | **2,066,251** | 100% |

**Cross-State Comparison**:
| Metric | Ohio Portion | Kentucky Portion | Indiana Portion |
|--------|--------------|------------------|-----------------|
| Median Income | $62,450 | $68,720 | $64,180 |
| Poverty Rate | 14.2% | 9.8% | 8.4% |
| Uninsured | 5.8% | 6.2% | 7.4% |
| Diabetes | 11.2% | 10.8% | 11.4% |

**Regional Aggregate**:
- Total Population: 2,066,251
- Median Household Income: $64,250
- Poverty Rate: 12.1%
- Diabetes Prevalence: 11.0%
- SVI Overall: 0.48

**Notable Observations**:
- Kentucky counties have higher income, lower poverty (suburban character)
- Ohio portion (Hamilton Co) has urban core with higher vulnerability
- Indiana portion is small, rural character

---

### Example 3: Tract-Based Catchment

**Request**: "Build a profile for these 12 tracts around our FQHC in South Phoenix"

**Response**:

**South Phoenix FQHC Catchment Area**

**Tract List**: 
04013112101, 04013112102, 04013112200, 04013112301, 04013112302, 04013112400, 04013112500, 04013112601, 04013112602, 04013112700, 04013112801, 04013112802

**Geography**:
- Parent County: Maricopa County, AZ
- Tract Count: 12
- Combined Population: 48,752
- Area: 8.4 sq mi

**Demographics**:
- Median Age: 28.4 (young population)
- Hispanic: 84.2%
- White NH: 8.4%
- Median Income: $38,420
- Poverty Rate: 28.4%

**Health Profile**:
| Metric | Catchment | Maricopa County | Difference |
|--------|-----------|-----------------|------------|
| Diabetes | 14.8% | 10.2% | +4.6% ⚠️ |
| Obesity | 38.2% | 30.4% | +7.8% ⚠️ |
| No Checkup | 34.2% | 24.8% | +9.4% ⚠️ |
| Uninsured | 22.4% | 9.8% | +12.6% ⚠️ |

**SDOH Profile**:
- Mean SVI: 0.92 (very high vulnerability)
- All 12 tracts in top SVI quartile
- Key vulnerabilities:
  - Poverty: 28.4%
  - No high school diploma: 42.1%
  - Limited English: 38.4%
  - No vehicle: 18.2%

**Service Implications**:
- High need for chronic disease management (diabetes, obesity)
- Language services essential (Spanish)
- Transportation assistance needed
- Sliding fee scale critical (high poverty)

---

## Validation Rules

### Input Validation
- All component geographies must be valid identifiers
- Component types must be consistent (all counties, all tracts, etc.)
- Overlapping components flagged (e.g., county + tracts within same county)

### Output Validation
- [ ] All components successfully resolved
- [ ] Population totals match sum of components
- [ ] Weighted averages correctly calculated
- [ ] No double-counting of population
- [ ] SVI aggregated from component tracts

### Aggregation Methods

| Metric Type | Method |
|-------------|--------|
| Population counts | Sum |
| Percentages/rates | Population-weighted average |
| Medians | Cannot aggregate; use weighted estimate |
| SVI | Recalculate from tract-level or weighted average |
| Counts (hospitals, etc.) | Sum |

---

## Related Skills

- [county-profile.md](county-profile.md) - Individual county profiles
- [census-tract-analysis.md](census-tract-analysis.md) - Tract-level analysis
- [metro-area-profile.md](metro-area-profile.md) - Standard MSA profiles
- [cohort-specification.md](../cohorts/cohort-specification.md) - Define cohorts for region
- [healthcare-access-analysis.md](../health-patterns/healthcare-access-analysis.md) - Access detail

---

## Data Sources

| Data Element | Source | Vintage | Notes |
|--------------|--------|---------|-------|
| Demographics | Census ACS | 2022 5-year | For tract-level aggregation |
| Health Indicators | CDC PLACES | 2024 | County and tract level |
| SVI | CDC/ATSDR | 2022 | Tract-level for aggregation |
| ZIP-County Crosswalk | HUD | 2023 | For ZIP-based regions |

---

## Common Region Types

### Hospital Service Area
- Typically 3-8 counties
- Based on patient origin data
- May cross state lines

### Health Plan Market
- State regulatory boundaries
- Rating areas
- May be county-based

### ACO Territory
- Attribution-based
- Often county or ZIP defined
- Medicare vs commercial may differ

### FQHC Service Area
- Often tract-based
- MUA/MUP designated areas
- Can include specific tracts

### Clinical Trial Catchment
- Distance-based from sites
- Population centers
- Often custom geographic definitions
