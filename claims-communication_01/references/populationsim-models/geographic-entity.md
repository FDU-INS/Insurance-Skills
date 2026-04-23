# GeographicEntity Model

## Overview

The GeographicEntity model represents a geographic area at any level of the Census hierarchy. It provides consistent identification and metadata for geographic references across all PopulationSim outputs.

---

## Model Structure

```
GeographicEntity
├── type                         # Geography level
├── identifiers                  # FIPS, CBSA, names
├── hierarchy                    # Parent geographies
├── characteristics              # Urban/rural, land area
├── boundaries                   # Coordinate bounds (optional)
└── metadata                     # Source and version
```

---

## Schema Definition

### Root Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | enum | Yes | Geographic level type |
| `identifiers` | Identifiers | Yes | Codes and names |
| `hierarchy` | Hierarchy | Yes | Parent geographies |
| `characteristics` | Characteristics | No | Area characteristics |
| `boundaries` | Boundaries | No | Geographic bounds |
| `metadata` | GeoMetadata | No | Source information |

---

## Geographic Types

| Type | FIPS Digits | Description | Example |
|------|-------------|-------------|---------|
| `nation` | - | United States | USA |
| `region` | 1 | Census region | South |
| `division` | 1 | Census division | West South Central |
| `state` | 2 | State or territory | Texas (48) |
| `county` | 5 | County or equivalent | Harris County (48201) |
| `tract` | 11 | Census tract | 48201311500 |
| `block_group` | 12 | Block group | 482013115001 |
| `msa` | 5 (CBSA) | Metropolitan area | Houston MSA (26420) |
| `zcta` | 5 | ZIP Code Tabulation Area | 77001 |
| `custom` | - | User-defined region | - |

---

## Identifiers Object

### Structure

```json
{
  "identifiers": {
    "fips": "48201",
    "geoid": "48201",
    "name": "Harris County",
    "full_name": "Harris County, Texas",
    
    "state_fips": "48",
    "state_abbr": "TX",
    "state_name": "Texas",
    
    "cbsa_code": "26420",
    "cbsa_name": "Houston-The Woodlands-Sugar Land, TX",
    "cbsa_type": "metropolitan",
    
    "csa_code": "288",
    "csa_name": "Houston-The Woodlands, TX"
  }
}
```

### Identifier Fields by Type

| Type | Primary ID | Additional IDs |
|------|------------|----------------|
| state | state_fips | state_abbr, state_name |
| county | fips (5-digit) | state_fips, cbsa_code |
| tract | fips (11-digit) | county_fips, tract_code |
| block_group | fips (12-digit) | tract_fips, bg_code |
| msa | cbsa_code | csa_code, component_counties |
| zcta | zcta_code | state_fips (primary) |

---

## Hierarchy Object

### Structure

```json
{
  "hierarchy": {
    "nation": "US",
    "region": "South",
    "region_code": "3",
    "division": "West South Central",
    "division_code": "7",
    "state": {
      "fips": "48",
      "name": "Texas",
      "abbr": "TX"
    },
    "county": {
      "fips": "48201",
      "name": "Harris County"
    },
    "tract": {
      "fips": "48201311500",
      "code": "3115.00"
    },
    "block_group": {
      "fips": "482013115001",
      "code": "1"
    }
  }
}
```

### Hierarchy Levels

```
nation
└── region (4)
    └── division (9)
        └── state (50 + DC + territories)
            └── county (3,143)
                └── tract (~85,000)
                    └── block_group (~240,000)
```

---

## Characteristics Object

### Structure

```json
{
  "characteristics": {
    "urban_rural": {
      "classification": "urban",
      "urbanized_area": true,
      "urban_cluster": false,
      "rucc_code": 1,
      "rucc_description": "Metro - 1 million+ population"
    },
    
    "land_area": {
      "square_miles": 1777.0,
      "square_kilometers": 4602.4
    },
    
    "population_density": {
      "per_square_mile": 2662.4,
      "density_class": "high"
    },
    
    "special_designations": {
      "hpsa": {
        "primary_care": "partial",
        "mental_health": "full",
        "dental": "partial"
      },
      "mua": true,
      "frontier": false,
      "persistent_poverty": false
    }
  }
}
```

### Urban/Rural Classifications

| Classification | Definition |
|---------------|------------|
| `urban` | Within Urbanized Area (≥50,000 pop) |
| `urban_cluster` | Within Urban Cluster (2,500-49,999) |
| `suburban` | Metro area, outside principal city |
| `rural` | Not in Urbanized Area or Urban Cluster |
| `frontier` | <7 persons per square mile |

### Rural-Urban Continuum Codes (RUCC)

| Code | Description |
|------|-------------|
| 1 | Metro - 1 million+ population |
| 2 | Metro - 250,000 to 1 million |
| 3 | Metro - fewer than 250,000 |
| 4-9 | Non-metro (various gradations) |

---

## Boundaries Object

### Structure

```json
{
  "boundaries": {
    "bounding_box": {
      "north": 30.1855,
      "south": 29.4977,
      "east": -94.9127,
      "west": -95.9232
    },
    
    "centroid": {
      "latitude": 29.7604,
      "longitude": -95.3698
    },
    
    "geometry_source": "TIGER/Line 2022",
    "geometry_reference": "tl_2022_48_tract"
  }
}
```

---

## GeoMetadata Object

### Structure

```json
{
  "metadata": {
    "source": "Census Bureau",
    "vintage": 2022,
    "tiger_version": "2022",
    "acs_vintage": "2018-2022",
    "retrieved_at": "2024-12-23T10:00:00Z"
  }
}
```

---

## Type-Specific Examples

### State

```json
{
  "type": "state",
  "identifiers": {
    "fips": "48",
    "geoid": "48",
    "name": "Texas",
    "abbr": "TX"
  },
  "hierarchy": {
    "nation": "US",
    "region": "South",
    "division": "West South Central"
  },
  "characteristics": {
    "land_area": {"square_miles": 261231.71}
  }
}
```

### County

```json
{
  "type": "county",
  "identifiers": {
    "fips": "48201",
    "geoid": "48201",
    "name": "Harris County",
    "full_name": "Harris County, Texas",
    "state_fips": "48",
    "state_abbr": "TX",
    "cbsa_code": "26420"
  },
  "hierarchy": {
    "nation": "US",
    "region": "South",
    "division": "West South Central",
    "state": {"fips": "48", "name": "Texas", "abbr": "TX"}
  },
  "characteristics": {
    "urban_rural": {
      "classification": "urban",
      "rucc_code": 1
    }
  }
}
```

### Census Tract

```json
{
  "type": "tract",
  "identifiers": {
    "fips": "48201311500",
    "geoid": "48201311500",
    "tract_code": "3115.00",
    "county_fips": "48201",
    "county_name": "Harris County",
    "state_fips": "48",
    "state_abbr": "TX"
  },
  "hierarchy": {
    "nation": "US",
    "state": {"fips": "48", "name": "Texas"},
    "county": {"fips": "48201", "name": "Harris County"}
  },
  "characteristics": {
    "urban_rural": {"classification": "urban"},
    "land_area": {"square_miles": 1.24}
  }
}
```

### Metropolitan Statistical Area (MSA)

```json
{
  "type": "msa",
  "identifiers": {
    "cbsa_code": "26420",
    "geoid": "26420",
    "name": "Houston-The Woodlands-Sugar Land, TX",
    "cbsa_type": "metropolitan",
    "principal_city": "Houston",
    "csa_code": "288",
    "csa_name": "Houston-The Woodlands, TX"
  },
  "hierarchy": {
    "nation": "US",
    "region": "South",
    "states": ["TX"]
  },
  "characteristics": {
    "component_counties": [
      {"fips": "48201", "name": "Harris"},
      {"fips": "48157", "name": "Fort Bend"},
      {"fips": "48339", "name": "Montgomery"},
      {"fips": "48167", "name": "Galveston"},
      {"fips": "48039", "name": "Brazoria"},
      {"fips": "48291", "name": "Liberty"},
      {"fips": "48473", "name": "Waller"},
      {"fips": "48071", "name": "Chambers"},
      {"fips": "48015", "name": "Austin"}
    ],
    "county_count": 9
  }
}
```

### Custom Region

```json
{
  "type": "custom",
  "identifiers": {
    "custom_id": "houston-high-vulnerability",
    "name": "High-Vulnerability Houston Tracts",
    "description": "Census tracts in Houston with SVI ≥ 0.75"
  },
  "hierarchy": {
    "state": {"fips": "48", "name": "Texas"},
    "county": {"fips": "48201", "name": "Harris County"}
  },
  "characteristics": {
    "component_tracts": [
      "48201311500",
      "48201312100",
      "48201312200",
      "48201313400"
    ],
    "tract_count": 4,
    "selection_criteria": "svi_overall >= 0.75"
  }
}
```

---

## Validation Rules

1. **FIPS Format**: Must match expected digit count for type
2. **Hierarchy Consistency**: Child must be within parent
3. **CBSA Validity**: CBSA codes must be valid OMB designations
4. **Coordinate Bounds**: Bounding box coordinates must be valid lat/long

---

## Usage Patterns

### In PopulationProfile

```json
{
  "geography": {
    "type": "county",
    "identifiers": {
      "fips": "48201",
      "name": "Harris County"
    }
  }
}
```

### In CohortSpecification

```json
{
  "geography": {
    "type": "county",
    "identifiers": {"fips": "48201"},
    "filters": {"svi_min": 0.60}
  }
}
```

### In TrialSim Site Selection

```json
{
  "catchment_area": {
    "type": "msa",
    "identifiers": {"cbsa_code": "26420"},
    "radius_miles": 50
  }
}
```

---

## Related Models

- [PopulationProfile](population-profile.md) - Uses geography for location
- [CohortSpecification](cohort-specification.md) - Uses for constraints
- [Geography Codes Reference](../geography-codes.md) - FIPS/CBSA codes
