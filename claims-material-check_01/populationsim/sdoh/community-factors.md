---
name: community-factors
description: >
  Analyze community-level SDOH factors including housing, transportation, food
  access, and environmental conditions. Use for understanding structural barriers
  and neighborhood effects on health. Triggers: "housing", "transportation",
  "food desert", "food access", "community factors", "environmental health".
---

# Community Factors Skill

## Overview

The community-factors skill analyzes neighborhood and community-level factors that influence health, including housing conditions, transportation access, food environment, and environmental quality. These structural factors create the context in which health behaviors and outcomes occur.

**Primary Use Cases**:
- Housing quality and stability assessment
- Transportation barrier identification
- Food access/desert analysis
- Environmental health assessment
- Neighborhood effect quantification

---

## Trigger Phrases

- "Food deserts in [geography]"
- "Transportation access in [area]"
- "Housing conditions in [geography]"
- "Community health factors for [area]"
- "Environmental health in [region]"
- "Neighborhood factors affecting health"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | County, tract, or metro |
| `focus` | string | No | "all" | "housing", "transportation", "food", "environment" |
| `compare_to` | string | No | - | Geography for comparison |

---

## Data Sources (Embedded v2.0)

Community factor data comes from embedded SVI and CDC PLACES files:

| Category | File | Key Columns |
|----------|------|-------------|
| **Housing** | | |
| Multi-unit structures | `data/tract/svi_tract_2022.csv` | E_MUNIT, EP_MUNIT |
| Mobile homes | `data/tract/svi_tract_2022.csv` | E_MOBILE, EP_MOBILE |
| Crowding | `data/tract/svi_tract_2022.csv` | E_CROWD, EP_CROWD |
| Housing cost burden | `data/tract/svi_tract_2022.csv` | E_HBURD, EP_HBURD |
| **Transportation** | | |
| No vehicle | `data/tract/svi_tract_2022.csv` | E_NOVEH, EP_NOVEH |
| Lack of transportation | `data/county/places_county_2024.csv` | LACKTRPT_CrudePrev |
| **Social Needs** | | |
| Food insecurity | `data/county/places_county_2024.csv` | FOODINSECU_CrudePrev |
| Housing insecurity | `data/county/places_county_2024.csv` | HOUSINSECU_CrudePrev |
| Utility shutoff threat | `data/county/places_county_2024.csv` | SHUTUTILITY_CrudePrev |

### Data Lookup Pattern

```
1. Identify geography type and FIPS code
2. Read SVI tract file for housing/transportation indicators
3. Read PLACES county file for social needs measures
4. Combine into community factor profile
5. Return with source citations
```

---

## Community Factor Categories

### Housing Factors

| Factor | Definition | Source | Health Impact |
|--------|------------|--------|---------------|
| Housing Cost Burden | >30% income on housing | ACS | Stress, delayed care |
| Severe Cost Burden | >50% income on housing | ACS | Housing instability |
| Crowding | >1 person per room | ACS | Infectious disease spread |
| Substandard Housing | Lacking plumbing/kitchen | ACS | Sanitation, safety |
| Renter Instability | Renter-occupied units | ACS | Housing insecurity |
| Mobile Homes | Living in mobile homes | ACS | Environmental vulnerability |
| Vacancy Rate | Vacant housing units | ACS | Neighborhood decline |

### Transportation Factors

| Factor | Definition | Source | Health Impact |
|--------|------------|--------|---------------|
| No Vehicle | Households without vehicle | ACS | Appointment access |
| Long Commute | Commute >60 minutes | ACS | Time poverty, stress |
| Public Transit Use | Use public transportation | ACS | Transit dependency |
| Walk/Bike Commute | Active transportation | ACS | Physical activity |

### Food Environment

| Factor | Definition | Source | Health Impact |
|--------|------------|--------|---------------|
| Food Desert | Low access + low income | USDA | Poor nutrition, obesity |
| SNAP Recipients | Receiving food assistance | ACS | Food insecurity marker |
| Grocery Store Access | Distance to supermarket | USDA | Fresh food availability |
| Fast Food Density | Fast food per capita | Census | Unhealthy food environment |

### Environmental Factors

| Factor | Definition | Source | Health Impact |
|--------|------------|--------|---------------|
| Air Quality Index | PM2.5, ozone levels | EPA | Respiratory disease |
| Lead Risk | Pre-1960 housing | ACS/HUD | Developmental, neuro |
| Superfund Sites | Hazardous waste sites | EPA | Cancer, chronic disease |
| Urban Heat Island | Heat vulnerability | NASA | Heat-related illness |
| Green Space | Park access | Trust for Public Land | Mental health, activity |

---

## Output Schema

```json
{
  "analysis_type": "community_factors",
  "geography": {
    "type": "county",
    "fips": "17031",
    "name": "Cook County",
    "state": "IL"
  },
  "housing": {
    "cost_burden": {
      "rate": 0.382,
      "population_affected": 842000,
      "vs_national": 0.052
    },
    "severe_cost_burden": {
      "rate": 0.182,
      "population_affected": 401000
    },
    "crowding": {
      "rate": 0.042,
      "concentrated_areas": ["Pilsen", "Little Village", "Albany Park"]
    },
    "substandard": {
      "no_plumbing": 0.004,
      "no_kitchen": 0.008
    },
    "tenure": {
      "owner_occupied": 0.548,
      "renter_occupied": 0.452
    },
    "vacancy_rate": 0.092,
    "median_home_value": 286400,
    "median_rent": 1242,
    "housing_instability_index": 0.58
  },
  "transportation": {
    "no_vehicle": {
      "rate": 0.182,
      "households": 186000,
      "concentrated_areas": ["South Side", "West Side"]
    },
    "commute_patterns": {
      "drive_alone": 0.62,
      "public_transit": 0.24,
      "walk_bike": 0.06,
      "work_from_home": 0.08
    },
    "long_commute_60_plus": 0.128,
    "mean_commute_minutes": 34.2,
    "transit_access_score": 72,
    "healthcare_transit_access": {
      "hospital_within_30_min_transit": 0.82,
      "pharmacy_within_15_min": 0.74
    }
  },
  "food_environment": {
    "food_desert_tracts": {
      "count": 124,
      "pct_of_tracts": 0.098,
      "population": 412000
    },
    "snap_recipients": {
      "rate": 0.148,
      "households": 151000
    },
    "food_insecurity_rate": 0.112,
    "grocery_access": {
      "low_access_1_mile": 0.182,
      "low_access_half_mile": 0.312
    },
    "fast_food_density": {
      "per_1000_pop": 0.82,
      "vs_grocery_ratio": 4.2
    },
    "farmers_markets": 52
  },
  "environment": {
    "air_quality": {
      "aqi_days_unhealthy": 12,
      "pm25_annual_avg": 10.2,
      "ozone_days_exceeded": 8
    },
    "lead_risk": {
      "pre_1960_housing_pct": 0.42,
      "high_risk_tracts": 186,
      "children_at_risk": 124000
    },
    "superfund_sites": 14,
    "brownfield_sites": 248,
    "green_space": {
      "park_access_10_min": 0.72,
      "tree_canopy_pct": 0.18
    },
    "urban_heat": {
      "heat_island_intensity": 4.2,
      "high_vulnerability_tracts": 82
    }
  },
  "composite_indices": {
    "housing_instability_index": 0.58,
    "transportation_barrier_index": 0.42,
    "food_environment_index": 0.48,
    "environmental_burden_index": 0.52
  },
  "health_correlations": {
    "food_desert_obesity": {
      "in_food_desert": 0.362,
      "not_in_food_desert": 0.298,
      "gap": 0.064
    },
    "no_vehicle_missed_care": {
      "no_vehicle": 0.248,
      "has_vehicle": 0.124,
      "gap": 0.124
    },
    "housing_burden_depression": {
      "severe_burden": 0.284,
      "no_burden": 0.168,
      "gap": 0.116
    }
  },
  "cohort_sdoh_profile": {
    "housing_instability": 0.182,
    "transportation_barrier": 0.182,
    "food_insecurity": 0.112,
    "environmental_exposure": 0.082
  },
  "z_code_implications": {
    "Z59.1_inadequate_housing": 0.048,
    "Z59.82_transportation": 0.182,
    "Z59.41_food_insecurity": 0.112,
    "Z58.6_water_supply": 0.008
  },
  "metadata": {
    "data_sources": [
      "ACS_2022_5yr",
      "USDA_Food_Atlas_2021",
      "EPA_AQI_2023",
      "HUD_2022"
    ],
    "generated_at": "2024-12-23T10:00:00Z"
  }
}
```

---

## Examples

### Example 1: Food Desert Analysis

**Request**: "Analyze food deserts in Detroit metro"

**Response**:

**Detroit Metro Food Access Analysis**

**Food Desert Summary**:
| Metric | Detroit Metro | National |
|--------|---------------|----------|
| Food Desert Tracts | 186 (18.4%) | 10.2% |
| Population Affected | 524,000 | - |
| Low Access (1 mi) | 28.4% | 18.2% |

**County Breakdown**:
| County | Food Desert Tracts | Low Income + Low Access |
|--------|-------------------|-------------------------|
| Wayne | 142 (24.8%) | 412,000 people |
| Oakland | 24 (8.2%) | 68,000 people |
| Macomb | 18 (9.4%) | 44,000 people |

**Detroit City Detail**:
- 68% of tracts are food deserts
- Average distance to grocery: 2.4 miles
- Fast food to grocery ratio: 8.2:1 ⚠️

**Food Desert Characteristics**:
| Factor | Food Desert Tracts | Non-Food Desert |
|--------|-------------------|-----------------|
| Poverty Rate | 38.4% | 12.8% |
| No Vehicle | 28.4% | 8.2% |
| SNAP Recipients | 32.4% | 12.4% |
| Obesity Rate | 42.8% | 28.4% |
| Diabetes Rate | 16.8% | 10.2% |

**Health Impact**:
- Obesity: +14.4% in food deserts
- Diabetes: +6.6% in food deserts
- Hypertension: +8.2% in food deserts

---

### Example 2: Transportation Barriers

**Request**: "Transportation access barriers in rural Appalachia"

**Response**:

**Rural Appalachian Transportation Analysis**

**Region**: 54 rural Appalachian counties (KY, WV, VA, TN)

**Key Metrics**:
| Metric | Rural Appalachia | National | Gap |
|--------|------------------|----------|-----|
| No Vehicle | 8.4% | 8.2% | +0.2% |
| Long Commute | 18.4% | 9.8% | +8.6% ⚠️ |
| Mean Commute | 38.2 min | 27.6 min | +10.6 min |
| No Public Transit | 92.4% | 48.2% | +44.2% ⚠️ |

**Healthcare Access Impact**:
| Metric | Rural Appalachia | Urban | Gap |
|--------|------------------|-------|-----|
| Avg Distance to Hospital | 24.8 mi | 4.2 mi | +20.6 mi |
| Avg Distance to Pharmacy | 12.4 mi | 1.8 mi | +10.6 mi |
| Missed Appt (transport) | 18.4% | 6.2% | +12.2% |
| Delayed Care (access) | 24.8% | 12.4% | +12.4% |

**NEMT Need**:
- Estimated 42,000 Medicaid beneficiaries need NEMT
- Current NEMT coverage: ~60%
- Gap: ~17,000 beneficiaries underserved

**Z-Code Implications**:
- Z59.82 (Transportation insecurity): 18.4% prevalence
- Associated with: Missed appointments, delayed care, worse outcomes

---

### Example 3: Housing and Health

**Request**: "Housing factors affecting health in Los Angeles"

**Response**:

**Los Angeles County Housing-Health Analysis**

**Housing Cost Burden**:
| Level | Households | % of Total | Health Impact |
|-------|------------|------------|---------------|
| No Burden (<30%) | 2.1M | 58% | Baseline |
| Cost Burden (30-50%) | 0.9M | 25% | +15% depression |
| Severe Burden (>50%) | 0.6M | 17% | +32% depression |

**Housing Instability Indicators**:
| Factor | LA County | California | National |
|--------|-----------|------------|----------|
| Renter-Occupied | 52.4% | 44.2% | 35.8% |
| Median Rent | $1,842 | $1,764 | $1,242 |
| Rent as % Income | 32.4% | 29.8% | 24.2% |
| Eviction Rate | 2.4% | 1.8% | 2.2% |
| Homelessness | 0.8% | 0.4% | 0.2% |

**Housing Quality**:
| Issue | Prevalence | Concentrated Areas |
|-------|------------|-------------------|
| Crowding (>1/room) | 12.4% | Pico-Union, Koreatown |
| Pre-1960 Housing | 38.4% | South LA, East LA |
| Lead Risk | 24.8% | Same as above |

**Health Correlations**:
| Housing Factor | Health Outcome | Correlation |
|----------------|----------------|-------------|
| Severe Cost Burden | Depression | +32% |
| Crowding | COVID infection | +48% |
| Pre-1960 Housing | Child lead levels | +2.4x |
| Homelessness | Mortality | +4.8x |

**SDOH Z-Codes**:
- Z59.0 (Homelessness): 0.8%
- Z59.1 (Inadequate housing): 4.2%
- Z59.81 (Housing instability): 12.4%

---

## Validation Rules

### Input Validation
- Geography must be valid
- Focus area must be valid option

### Output Validation
- [ ] Percentages between 0 and 1
- [ ] Distances positive
- [ ] Counts match geography
- [ ] Indices properly scaled

---

## Related Skills

- [svi-analysis.md](svi-analysis.md) - Housing/transportation theme
- [adi-analysis.md](adi-analysis.md) - Housing quality variables
- [economic-indicators.md](economic-indicators.md) - Cost burden context
- [census-tract-analysis.md](../geographic/census-tract-analysis.md) - Tract mapping
- [health-outcome-disparities.md](../health-patterns/health-outcome-disparities.md) - Health links

---

## Data Sources

| Source | Content | Geography | Update |
|--------|---------|-----------|--------|
| Census ACS | Housing, transportation | All levels | Annual |
| USDA Food Atlas | Food access | Census Tract | Periodic |
| EPA | Air quality, Superfund | County, Site | Annual |
| HUD | Housing quality | Tract | Annual |
| CDC PLACES | Health outcomes | County, Tract | Annual |
