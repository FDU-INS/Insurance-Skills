# Area Deprivation Index (ADI) Methodology

## Overview

The Area Deprivation Index (ADI) is a measure of neighborhood socioeconomic disadvantage based on income, education, employment, and housing quality indicators. Originally developed at the Health Resources and Services Administration (HRSA), the ADI provides rankings at the census block group level—the most granular geographic unit with reliable estimates.

**Original Source**: Health Resources and Services Administration (HRSA)  
**Current Maintainer**: University of Wisconsin School of Medicine and Public Health  
**URL**: https://www.neighborhoodatlas.medicine.wisc.edu/  
**Geography**: Census block group level  
**Update Frequency**: Annual  
**Current Version**: 2021 (v4.0)

---

## ADI Structure

### 17 Variables, 2 Factor Domains

The ADI is constructed from 17 ACS variables organized into two conceptual domains:

```
ADI Score
├── Factor 1: Socioeconomic Status
│   ├── Income indicators
│   ├── Education indicators
│   └── Employment indicators
└── Factor 2: Housing Quality
    ├── Home value indicators
    ├── Crowding indicators
    └── Household composition
```

---

## ADI Variables

### Income Domain (5 variables)

| Variable | ACS Source | Definition |
|----------|------------|------------|
| Median Family Income | B19113 | Median family income in past 12 months |
| Income Disparity | B19001 | % families with income <$10,000 ÷ % with income >$50,000 |
| Median Home Value | B25077 | Median value of owner-occupied units |
| Median Gross Rent | B25064 | Median gross rent |
| Median Monthly Mortgage | B25088 | Median monthly owner costs with mortgage |

### Poverty Domain (3 variables)

| Variable | ACS Source | Definition |
|----------|------------|------------|
| Below 150% FPL | C17002 | % population below 150% of federal poverty level |
| Single-Parent Families | B11003 | % families with female head, no spouse, with children |
| Public Assistance | B19057 | % families receiving public assistance income |

### Education Domain (2 variables)

| Variable | ACS Source | Definition |
|----------|------------|------------|
| No High School Diploma | B15003 | % population 25+ without HS diploma |
| High School Education | B15003 | % population 25+ with at least HS education |

### Employment Domain (2 variables)

| Variable | ACS Source | Definition |
|----------|------------|------------|
| Unemployment Rate | B23025 | % civilian labor force unemployed |
| Labor Force Participation | B23025 | % population 16+ not in labor force |

### Housing Quality Domain (5 variables)

| Variable | ACS Source | Definition |
|----------|------------|------------|
| Crowding | B25014 | % occupied housing units with >1 person per room |
| No Vehicle | B25044 | % occupied units with no vehicle available |
| No Telephone | B25043 | % occupied units without telephone service |
| No Complete Plumbing | B25047 | % occupied units lacking complete plumbing |
| No Complete Kitchen | B25052 | % occupied units lacking complete kitchen |

---

## ADI Calculation

### Step 1: Factor Analysis

The 17 variables are combined using factor analysis (principal component analysis) to create a single ADI score. The factor loadings determine the relative contribution of each variable.

### Step 2: National Ranking

1. All ~240,000 block groups are ranked
2. Ranks converted to percentiles (1-100)
3. Percentile 1 = least deprived, Percentile 100 = most deprived

### Step 3: State Decile

Within each state:
1. Block groups ranked within state
2. Converted to deciles (1-10)
3. Decile 1 = least deprived, Decile 10 = most deprived

---

## ADI Output Structure

### National Percentile Ranking

| Percentile Range | Deprivation Level | Characteristics |
|------------------|-------------------|-----------------|
| 1-20 | Very Low | Affluent areas, high resources |
| 21-40 | Low | Above-average socioeconomic status |
| 41-60 | Moderate | Near-national average |
| 61-80 | High | Below-average resources |
| 81-100 | Very High | Concentrated disadvantage |

### State Decile Ranking

| Decile | Within-State Position |
|--------|----------------------|
| 1-2 | Least deprived (top 20%) |
| 3-4 | Low deprivation |
| 5-6 | Moderate |
| 7-8 | High deprivation |
| 9-10 | Most deprived (bottom 20%) |

### Full ADI Record

```json
{
  "adi": {
    "geography": {
      "state": "48",
      "county": "201",
      "tract": "311500",
      "block_group": "1",
      "fips": "482013115001"
    },
    
    "rankings": {
      "national_percentile": 72,
      "state_decile": 7
    },
    
    "interpretation": {
      "national_level": "high_deprivation",
      "state_level": "above_median_deprivation"
    },
    
    "component_indicators": {
      "income": {
        "median_family_income": 42500,
        "income_disparity": 1.8,
        "median_home_value": 125000
      },
      "poverty": {
        "below_150_fpl": 0.284,
        "single_parent_families": 0.182,
        "public_assistance": 0.068
      },
      "education": {
        "no_hs_diploma": 0.218,
        "hs_or_higher": 0.782
      },
      "employment": {
        "unemployment": 0.072,
        "not_in_labor_force": 0.382
      },
      "housing": {
        "crowding": 0.082,
        "no_vehicle": 0.142,
        "no_telephone": 0.032,
        "no_plumbing": 0.004,
        "no_kitchen": 0.008
      }
    },
    
    "metadata": {
      "data_year": "2021",
      "acs_vintage": "2017-2021",
      "version": "4.0",
      "source": "UW_Neighborhood_Atlas"
    }
  }
}
```

---

## ADI in PopulationSim

### Use Cases

1. **Fine-Grained Analysis**: Block group level (vs SVI tract level)
2. **Healthcare Access Studies**: ADI includes healthcare-related variables
3. **Risk Stratification**: Identify high-risk neighborhoods
4. **Resource Allocation**: Target interventions to deprived areas
5. **Research Studies**: Widely used in health disparities research

### CohortSpecification with ADI

```json
{
  "geography_filter": {
    "base": "county:48201",
    "constraint": "adi_national_percentile >= 80"
  },
  "sdoh_profile": {
    "adi_mean_percentile": 85,
    "adi_distribution": {
      "very_high": 0.48,
      "high": 0.32,
      "moderate": 0.15,
      "low": 0.05
    }
  }
}
```

### ADI to Z-Code Mapping

| ADI Component | Related Z-Codes |
|---------------|-----------------|
| Below 150% FPL | Z59.6 (Low income) |
| Public assistance | Z59.7 (Insufficient insurance) |
| Unemployment | Z56.0 (Unemployment) |
| No HS diploma | Z55.0 (Illiteracy) |
| Single parent | Z63.5 (Disrupted family) |
| Crowding | Z59.1 (Inadequate housing) |
| No vehicle | Z59.82 (Transportation insecurity) |
| No telephone | Z59.89 (Other housing problems) |

---

## ADI vs SVI Comparison

| Feature | ADI | SVI |
|---------|-----|-----|
| **Geography** | Block group | Census tract |
| **Granularity** | ~240,000 units | ~85,000 units |
| **Population per unit** | ~1,500 avg | ~4,000 avg |
| **Variables** | 17 | 16 |
| **Themes** | 2 factors | 4 themes |
| **Ranking** | National percentile + State decile | Percentile only |
| **Housing quality** | Detailed (plumbing, kitchen) | Basic (structure type) |
| **Disability** | Not included | Included |
| **Language** | Not included | Included |
| **Use case** | Healthcare research | Emergency management |

### When to Use ADI vs SVI

| Scenario | Recommended Index | Rationale |
|----------|-------------------|-----------|
| Tract-level analysis | SVI | Native geography |
| Block group precision | ADI | Finer granularity |
| Healthcare access focus | ADI | Includes access variables |
| Emergency planning | SVI | Designed for this purpose |
| Disability analysis | SVI | Includes disability theme |
| Language access | SVI | Includes language theme |
| Housing quality | ADI | More detailed |
| Within-state comparison | ADI | State decile ranking |

---

## ADI in Healthcare Research

### CMS Uses

The Centers for Medicare & Medicaid Services (CMS) uses ADI for:
- Geographic adjustment of payment rates
- Identification of underserved areas
- Quality measure stratification
- Health equity analyses

### Research Applications

| Application | ADI Use |
|-------------|---------|
| Readmission risk | Higher ADI → Higher readmission rates |
| Mortality studies | ADI as covariate for socioeconomic status |
| Preventive care | Lower screening rates in high-ADI areas |
| Medication adherence | ADI predicts non-adherence |
| Trial enrollment | ADI affects enrollment likelihood |

---

## Data Access

### Neighborhood Atlas

- Interactive mapping: https://www.neighborhoodatlas.medicine.wisc.edu/
- Data download: Requires free registration
- API: Not publicly available

### Data Files

| File | Content | Format |
|------|---------|--------|
| US_2021_ADI_Census_Block_Group_v4.0.csv | National block group data | CSV |
| [State]_2021_ADI_Census_Block_Group_v4.0.csv | State-specific data | CSV |

### Key Fields

| Field | Description |
|-------|-------------|
| FIPS | 12-digit block group FIPS |
| ADI_NATRANK | National percentile (1-100) |
| ADI_STAESSION | State decile (1-10) |

---

## Limitations

1. **Suppression**: Block groups with small populations may be suppressed
2. **Version changes**: Variable definitions may change between versions
3. **Lag**: Based on 5-year ACS estimates
4. **Missing healthcare**: No direct healthcare utilization measures
5. **Urban bias**: Some housing variables less relevant in rural areas

---

## Related References

- [Census Variables](census-variables.md) - Underlying ACS variables
- [SVI Methodology](svi-methodology.md) - Complementary index
- [Geography Codes](geography-codes.md) - FIPS codes
- [SDOH Skills](../skills/populationsim/sdoh/adi-analysis.md) - ADI analysis skill
