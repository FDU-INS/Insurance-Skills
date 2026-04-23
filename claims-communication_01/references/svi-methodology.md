# Social Vulnerability Index (SVI) Methodology

## Overview

The CDC/ATSDR Social Vulnerability Index (SVI) uses U.S. Census data to identify communities that may need support before, during, or after disasters. PopulationSim uses SVI as a composite measure of social determinants of health (SDOH) at the census tract level.

**Source**: CDC/ATSDR  
**URL**: https://www.atsdr.cdc.gov/placeandhealth/svi/  
**Geography**: Census tract level  
**Update Frequency**: Biennial (follows ACS 5-year estimates)  
**Current Version**: 2022

---

## SVI Structure

### Four Themes, 16 Variables

The SVI comprises 4 themes, each capturing a different dimension of social vulnerability:

```
SVI Overall Score (0-1)
├── Theme 1: Socioeconomic Status (4 variables)
├── Theme 2: Household Composition & Disability (4 variables)  
├── Theme 3: Minority Status & Language (2 variables)
└── Theme 4: Housing Type & Transportation (6 variables)
```

---

## Theme 1: Socioeconomic Status

| Variable | ACS Table | Definition |
|----------|-----------|------------|
| Below Poverty | B17001 | % persons below federal poverty level |
| Unemployed | B23025 | % civilian (16+) unemployed |
| Per Capita Income | B19301 | Per capita income (inverse) |
| No High School Diploma | B15003 | % persons 25+ without HS diploma |

### Calculation

Each variable is ranked across all census tracts nationally, converted to percentile (0-1).

Theme 1 Score = Sum of percentile ranks / 4

### Interpretation

| Score | Vulnerability Level | Characteristics |
|-------|---------------------|-----------------|
| 0.00-0.25 | Low | Higher income, education, employment |
| 0.25-0.50 | Moderate | Near-average socioeconomic indicators |
| 0.50-0.75 | Moderate-High | Below-average economic status |
| 0.75-1.00 | High | Concentrated poverty, unemployment |

---

## Theme 2: Household Composition & Disability

| Variable | ACS Table | Definition |
|----------|-----------|------------|
| Aged 65 or Older | B01001 | % population aged 65+ |
| Aged 17 or Younger | B01001 | % population aged 17 or younger |
| Civilian with Disability | B18101 | % civilian noninstitutionalized with disability |
| Single-Parent Households | B11001 | % households with single parent and children |

### Rationale

These populations may have:
- Greater care needs
- Limited mobility during emergencies
- Dependency on others
- Financial constraints

### Interpretation

| Score | Vulnerability Level | Characteristics |
|-------|---------------------|-----------------|
| 0.00-0.25 | Low | Working-age adults, two-parent households |
| 0.25-0.50 | Moderate | Mixed age distribution |
| 0.50-0.75 | Moderate-High | Higher dependent populations |
| 0.75-1.00 | High | Concentrated elderly, children, disabled, single parents |

---

## Theme 3: Minority Status & Language

| Variable | ACS Table | Definition |
|----------|-----------|------------|
| Minority | B03002 | % minority (all except White, non-Hispanic) |
| Speaks English "Less than Well" | C16002 | % limited English households |

### Rationale

- Historical discrimination affects resource access
- Language barriers impede emergency communication
- Cultural differences may affect service utilization

### Interpretation

| Score | Vulnerability Level | Characteristics |
|-------|---------------------|-----------------|
| 0.00-0.25 | Low | Predominantly White, English-speaking |
| 0.25-0.50 | Moderate | Some diversity |
| 0.50-0.75 | Moderate-High | Significant minority population |
| 0.75-1.00 | High | Majority-minority, many limited English speakers |

---

## Theme 4: Housing Type & Transportation

| Variable | ACS Table | Definition |
|----------|-----------|------------|
| Multi-Unit Structures | B25024 | % housing in structures with 10+ units |
| Mobile Homes | B25024 | % housing that is mobile homes |
| Crowding | B25014 | % housing units with >1 person per room |
| No Vehicle | B25044 | % households with no vehicle available |
| Group Quarters | B26001 | % population living in group quarters |
| No Telephone Service | B25043 | % households without telephone service |

### Rationale

- Multi-unit housing: evacuation challenges
- Mobile homes: vulnerable to severe weather
- Crowding: disease transmission, evacuation difficulty
- No vehicle: limited evacuation capability
- Group quarters: institutional populations with special needs

### Interpretation

| Score | Vulnerability Level | Characteristics |
|-------|---------------------|-----------------|
| 0.00-0.25 | Low | Single-family homes, vehicle access |
| 0.25-0.50 | Moderate | Mixed housing types |
| 0.50-0.75 | Moderate-High | Dense housing, some transportation barriers |
| 0.75-1.00 | High | Dense rental, mobile homes, no vehicles |

---

## Overall SVI Calculation

### Step 1: Variable Percentile Ranking

For each of the 16 variables:
1. Rank all ~85,000 census tracts
2. Convert rank to percentile: `(rank - 1) / (n - 1)`
3. Result: 0 (lowest vulnerability) to 1 (highest vulnerability)

### Step 2: Theme Scores

For each theme:
```
Theme Score = Sum of variable percentiles within theme / Number of variables in theme
```

### Step 3: Overall Score

```
Overall SVI = Sum of all 16 variable percentiles / 16
```

### Step 4: Flag Assignment

Tracts in the top 10% nationally (≥0.90) are flagged as "high vulnerability" for each theme and overall.

---

## SVI Output Structure

### Full SVI Record

```json
{
  "svi": {
    "geography": {
      "state": "48",
      "county": "201",
      "tract": "311500",
      "fips": "48201311500"
    },
    
    "overall": {
      "score": 0.7234,
      "percentile_rank": 72,
      "flag": false
    },
    
    "themes": {
      "socioeconomic": {
        "score": 0.6842,
        "flag": false,
        "variables": {
          "poverty": 0.7124,
          "unemployment": 0.5823,
          "per_capita_income": 0.7412,
          "no_hs_diploma": 0.7008
        }
      },
      "household_composition": {
        "score": 0.5234,
        "flag": false,
        "variables": {
          "age_65_plus": 0.4521,
          "age_17_under": 0.6234,
          "disability": 0.5124,
          "single_parent": 0.5058
        }
      },
      "minority_language": {
        "score": 0.8912,
        "flag": false,
        "variables": {
          "minority": 0.9234,
          "limited_english": 0.8590
        }
      },
      "housing_transportation": {
        "score": 0.7948,
        "flag": false,
        "variables": {
          "multi_unit": 0.8124,
          "mobile_home": 0.1234,
          "crowding": 0.8234,
          "no_vehicle": 0.7834,
          "group_quarters": 0.2124,
          "no_telephone": 0.8142
        }
      }
    },
    
    "metadata": {
      "data_year": "2022",
      "source": "CDC_ATSDR_SVI",
      "version": "2022"
    }
  }
}
```

---

## SVI in PopulationSim

### Use Cases

1. **Geographic Filtering**: Select high-vulnerability areas
2. **Cohort Characteristics**: Add vulnerability profile to cohorts
3. **Health Equity Analysis**: Identify disparities by SVI
4. **Trial Site Selection**: Balance diversity and vulnerability
5. **Service Area Planning**: Target interventions

### CohortSpecification with SVI

```json
{
  "geography_filter": {
    "base": "county:48201",
    "constraint": "svi_overall >= 0.70"
  },
  "sdoh_profile": {
    "svi_mean": 0.78,
    "svi_theme_profile": {
      "socioeconomic": 0.72,
      "household_composition": 0.58,
      "minority_language": 0.88,
      "housing_transportation": 0.82
    }
  }
}
```

### SVI to Z-Code Mapping

| SVI Component | Related Z-Codes |
|---------------|-----------------|
| Poverty | Z59.6 (Low income) |
| Unemployment | Z56.0 (Unemployment) |
| No HS diploma | Z55.0 (Illiteracy/low literacy) |
| Single parent | Z63.5 (Disrupted family) |
| Limited English | Z60.3 (Acculturation difficulty) |
| No vehicle | Z59.82 (Transportation insecurity) |
| Crowding | Z59.1 (Inadequate housing) |

---

## Comparison: SVI vs ADI

| Feature | SVI | ADI |
|---------|-----|-----|
| Source | CDC/ATSDR | HRSAdmin |
| Geography | Census tract | Block group |
| Variables | 16 | 17 |
| Focus | Social vulnerability | Area deprivation |
| Themes | 4 distinct themes | 2 factor domains |
| Healthcare focus | Indirect | Direct (physician visits) |
| Update frequency | Biennial | Annual |

---

## Data Access

### CDC ATSDR SVI Portal

- Interactive mapping: https://www.atsdr.cdc.gov/placeandhealth/svi/interactive_map.html
- Data download: https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html

### Database Files

| File | Content |
|------|---------|
| SVI_[YEAR]_US.csv | National tract-level data |
| SVI_[YEAR]_[ST].csv | State-specific data |
| SVI_[YEAR]_US_county.csv | County-level aggregations |

---

## Limitations

1. **Correlation between themes**: Variables may overlap conceptually
2. **Equal weighting**: All variables weighted equally may not reflect actual risk
3. **Static data**: 5-year estimates lag current conditions
4. **Tract boundaries**: May not align with community boundaries
5. **Suppression**: Some tracts have missing data

---

## Related References

- [Census Variables](census-variables.md) - Underlying ACS variables
- [ADI Methodology](adi-methodology.md) - Complementary index
- [Geography Codes](geography-codes.md) - FIPS codes
- [SDOH Skills](../skills/populationsim/sdoh/svi-analysis.md) - SVI analysis skill
