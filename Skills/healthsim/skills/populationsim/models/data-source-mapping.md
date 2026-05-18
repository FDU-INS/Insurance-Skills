---
name: data-source-mapping
description: >
  Maps external data sources to PopulationSim model fields. Use this reference
  to understand data lineage and ensure consistent source attribution.
---

# Data Source Mapping

## Overview

PopulationSim integrates data from multiple public sources to create comprehensive population profiles. This document maps each data source to the model fields it populates.

---

## Primary Data Sources

### Census American Community Survey (ACS)

**Source**: U.S. Census Bureau
**URL**: https://data.census.gov
**Update**: Annual (1-year and 5-year estimates)

| ACS Table | PopulationSim Field | Model |
|-----------|---------------------|-------|
| S0101 | demographics.age.* | PopulationProfile |
| B03002 | demographics.race_ethnicity.* | PopulationProfile |
| S1901 | sdoh_indices.economic.median_household_income | PopulationProfile |
| S1701 | sdoh_indices.economic.poverty_rate | PopulationProfile |
| S2301 | sdoh_indices.economic.unemployment_rate | PopulationProfile |
| S2701 | healthcare_access.insurance_coverage.* | PopulationProfile |
| S1501 | sdoh_indices.education.* | PopulationProfile |
| DP04 | sdoh_indices.housing.* | PopulationProfile |
| S1601 | sdoh_indices.language.limited_english | PopulationProfile |

---

### CDC PLACES

**Source**: CDC Division of Population Health
**URL**: https://www.cdc.gov/places/
**Update**: Annual

| PLACES Measure | PopulationSim Field | Model |
|----------------|---------------------|-------|
| DIABETES | health_indicators.outcomes.diabetes | PopulationProfile |
| OBESITY | health_indicators.outcomes.obesity | PopulationProfile |
| BPHIGH | health_indicators.outcomes.hypertension | PopulationProfile |
| CHD | health_indicators.outcomes.chd | PopulationProfile |
| STROKE | health_indicators.outcomes.stroke | PopulationProfile |
| COPD | health_indicators.outcomes.copd | PopulationProfile |
| CASTHMA | health_indicators.outcomes.asthma | PopulationProfile |
| CANCER | health_indicators.outcomes.cancer | PopulationProfile |
| KIDNEY | health_indicators.outcomes.kidney | PopulationProfile |
| DEPRESSION | health_indicators.outcomes.depression | PopulationProfile |
| CSMOKING | health_indicators.behaviors.smoking | PopulationProfile |
| LPA | health_indicators.behaviors.physical_inactivity | PopulationProfile |
| BINGE | health_indicators.behaviors.binge_drinking | PopulationProfile |
| SLEEP | health_indicators.behaviors.short_sleep | PopulationProfile |
| CHECKUP | health_indicators.prevention.checkup | PopulationProfile |
| DENTAL | health_indicators.prevention.dental | PopulationProfile |
| MAMMOUSE | health_indicators.prevention.mammography | PopulationProfile |
| COLON_SCREEN | health_indicators.prevention.colorectal_screening | PopulationProfile |
| CHOLSCREEN | health_indicators.prevention.cholesterol_screening | PopulationProfile |

---

### CDC Social Vulnerability Index (SVI)

**Source**: CDC/ATSDR
**URL**: https://www.atsdr.cdc.gov/placeandhealth/svi/
**Update**: Biennial

| SVI Variable | PopulationSim Field | Model |
|--------------|---------------------|-------|
| RPL_THEMES | sdoh_indices.svi.overall | PopulationProfile |
| RPL_THEME1 | sdoh_indices.svi.theme1_socioeconomic | PopulationProfile |
| RPL_THEME2 | sdoh_indices.svi.theme2_household | PopulationProfile |
| RPL_THEME3 | sdoh_indices.svi.theme3_minority | PopulationProfile |
| RPL_THEME4 | sdoh_indices.svi.theme4_housing | PopulationProfile |
| E_POV150 | sdoh_profile.indicators.poverty_150_pct | CohortSpec |
| E_UNEMP | sdoh_profile.indicators.unemployment | CohortSpec |
| E_UNINSUR | sdoh_profile.indicators.uninsured_rate | CohortSpec |
| E_NOHSDP | sdoh_profile.indicators.no_hs_diploma | CohortSpec |
| E_LIMENG | sdoh_profile.indicators.limited_english | CohortSpec |
| E_NOVEH | sdoh_profile.indicators.no_vehicle | CohortSpec |

---

### Area Deprivation Index (ADI)

**Source**: Neighborhood Atlas (UW Madison)
**URL**: https://www.neighborhoodatlas.medicine.wisc.edu/
**Update**: Periodic

| ADI Field | PopulationSim Field | Model |
|-----------|---------------------|-------|
| ADI_NATRANK | sdoh_indices.adi.national_percentile | PopulationProfile |
| ADI_STAESSION | sdoh_indices.adi.state_decile | PopulationProfile |

---

### USDA Food Environment Atlas

**Source**: USDA Economic Research Service
**URL**: https://www.ers.usda.gov/data-products/food-environment-atlas/
**Update**: Periodic

| Atlas Field | PopulationSim Field | Model |
|-------------|---------------------|-------|
| LACCESS_POP10 | sdoh_profile.indicators.food_desert_pop | CohortSpec |
| SNAP_PART | sdoh_profile.indicators.snap_participation | CohortSpec |
| FFRPTH17 | community_factors.food_environment.fast_food_density | CohortSpec |
| GROCPTH17 | community_factors.food_environment.grocery_density | CohortSpec |

---

## Field-to-Source Mapping

### Demographics

| Field | Primary Source | Backup Source |
|-------|----------------|---------------|
| age.distribution | ACS S0101 | Decennial Census |
| sex.male/female | ACS S0101 | Decennial Census |
| race_ethnicity.* | ACS B03002 | Decennial Census |
| total_population | ACS B01001 | Census PEP |

### Health Indicators

| Field | Primary Source | Backup Source |
|-------|----------------|---------------|
| outcomes.* | CDC PLACES | BRFSS (state) |
| behaviors.* | CDC PLACES | BRFSS (state) |
| prevention.* | CDC PLACES | BRFSS (state) |

### SDOH

| Field | Primary Source | Backup Source |
|-------|----------------|---------------|
| svi.* | CDC SVI | Calculated from ACS |
| adi.* | Neighborhood Atlas | - |
| economic.* | ACS | SAIPE (poverty) |
| housing.* | ACS DP04 | HUD |

### Healthcare Access

| Field | Primary Source | Backup Source |
|-------|----------------|---------------|
| insurance_coverage.* | ACS S2701 | SAHIE |
| provider_availability.* | AHRF | NPPES (derived) |
| hpsa_status.* | HRSA HPSA | - |

---

## Data Quality Notes

### Reliability by Geography

| Level | ACS | PLACES | SVI | ADI |
|-------|-----|--------|-----|-----|
| State | ✓✓✓ | ✓✓✓ | ✓✓✓ | n/a |
| County | ✓✓✓ | ✓✓✓ | ✓✓✓ | n/a |
| Tract | ✓✓ | ✓✓ | ✓✓ | n/a |
| Block Group | ✓ | n/a | n/a | ✓✓ |

Legend: ✓✓✓ = High, ✓✓ = Moderate, ✓ = Lower (check MOE)

### Update Lag

| Source | Reference Period | Available | Lag |
|--------|-----------------|-----------|-----|
| ACS 1-year | Year N | Sept N+1 | ~9 months |
| ACS 5-year | Years N-4 to N | Dec N+1 | ~12 months |
| CDC PLACES | BRFSS N-1 | Fall N | ~18 months |
| CDC SVI | ACS 5-year | ~1 year after ACS | ~24 months |

---

## Related References

- [cdc-places-measures.md](../references/cdc-places-measures.md)
- [svi-variables.md](../references/svi-variables.md)
- [acs-tables.md](../references/acs-tables.md)
