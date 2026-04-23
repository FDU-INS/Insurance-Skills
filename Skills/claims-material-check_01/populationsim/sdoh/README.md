---
name: populationsim-sdoh
description: >
  SDOH (Social Determinants of Health) analysis skills for PopulationSim.
  Use for SVI analysis, ADI analysis, economic indicators, and community
  factors assessment. Primary data sources: CDC SVI, HRSA ADI, Census ACS.
---

# SDOH Analysis Skills

## Overview

SDOH (Social Determinants of Health) analysis skills provide detailed assessment of social, economic, and environmental factors that influence health outcomes. These skills leverage established indices (SVI, ADI) and Census data to characterize neighborhood-level social vulnerability and inform cohort SDOH profiles.

**Key Capability**: Translate social vulnerability indices into actionable SDOH profiles that drive realistic synthetic data generation.

---

## Skills in This Category

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [svi-analysis.md](svi-analysis.md) | CDC Social Vulnerability Index | "SVI", "social vulnerability", "vulnerable populations" |
| [adi-analysis.md](adi-analysis.md) | Area Deprivation Index | "ADI", "area deprivation", "neighborhood disadvantage" |
| [economic-indicators.md](economic-indicators.md) | Income, poverty, employment | "poverty", "income", "unemployment" |
| [community-factors.md](community-factors.md) | Housing, transportation, food | "housing", "transportation", "food desert" |

---

## SDOH Framework

### Five Domains of SDOH (Healthy People 2030)

| Domain | Components | HealthSim Relevance |
|--------|------------|---------------------|
| **Economic Stability** | Income, poverty, employment, food security | Insurance type, cost barriers |
| **Education Access** | Literacy, education level, language | Health literacy, adherence |
| **Healthcare Access** | Insurance, providers, transportation | Coverage, utilization |
| **Neighborhood** | Housing, crime, environmental quality | Z-codes, stress factors |
| **Social/Community** | Social support, discrimination, incarceration | Mental health, isolation |

### ICD-10 SDOH Z-Codes

| Category | Code Range | Examples |
|----------|------------|----------|
| Housing | Z59.0-Z59.9 | Homelessness, inadequate housing |
| Economic | Z59.41-Z59.9 | Food insecurity, low income |
| Education | Z55.0-Z55.9 | Illiteracy, limited education |
| Employment | Z56.0-Z56.9 | Unemployment, job stress |
| Social | Z60.0-Z60.9 | Social isolation, discrimination |
| Family | Z62.0-Z63.9 | Family disruption, abuse history |

---

## Key SDOH Indices

### Social Vulnerability Index (SVI)

CDC/ATSDR index ranking census tracts on 16 social factors across 4 themes:

| Theme | Variables | Health Relevance |
|-------|-----------|------------------|
| **Socioeconomic** | Poverty, unemployment, income, education, no insurance | Access, cost barriers |
| **Household Composition** | Age 65+, age <18, disability, single parent, English | Care needs, communication |
| **Minority/Language** | Minority status, limited English | Cultural competency, disparities |
| **Housing/Transportation** | Multi-unit, mobile homes, crowding, no vehicle, group quarters | Access barriers |

**Scale**: 0-1, where 1 = most vulnerable (highest percentile)

### Area Deprivation Index (ADI)

HRSA index measuring neighborhood socioeconomic disadvantage:

| Ranking | Scale | Interpretation |
|---------|-------|----------------|
| National Percentile | 1-100 | 100 = most disadvantaged nationally |
| State Decile | 1-10 | 10 = most disadvantaged in state |

**17 Variables** across income, education, employment, housing quality.

---

## Integration Points

### → Cohort Definition

SDOH indices inform sdoh_profile in CohortSpecification:

```json
{
  "sdoh_profile": {
    "rx_cost_barrier": 0.31,
    "food_insecurity": 0.22,
    "transportation_barrier": 0.18,
    "limited_english": 0.28
  }
}
```

### → PatientSim

SDOH profiles drive Z-code assignment:
- High SVI → Higher rates of Z59.x, Z60.x codes
- Food insecurity rate → Z59.41 assignment probability
- Transportation barrier → Z59.82 assignment probability

### → MemberSim

SDOH context affects:
- Insurance type distribution
- Utilization patterns
- ED vs primary care usage

### → TrialSim

SDOH factors affect:
- Site selection (underserved areas)
- Retention risk assessment
- Transportation support needs

---

## SDOH → Z-Code Mapping

| SVI/ADI Factor | Z-Code | Description |
|----------------|--------|-------------|
| Poverty | Z59.6 | Low income |
| Food insecurity | Z59.41 | Food insecurity |
| Inadequate housing | Z59.1 | Inadequate housing |
| No vehicle | Z59.82 | Transportation insecurity |
| Unemployment | Z56.0 | Unemployment |
| Limited English | Z60.3 | Acculturation difficulty |
| Social isolation | Z60.2 | Problems related to living alone |
| Single parent | Z63.5 | Disruption of family by separation |

---

## Skill Selection Guide

### Use svi-analysis.md when:
- Need composite vulnerability score
- Analyzing disaster/pandemic vulnerability
- Tract-level social factor analysis
- Identifying vulnerable populations

### Use adi-analysis.md when:
- Need neighborhood deprivation measure
- Block group-level granularity needed
- Analyzing health outcomes by disadvantage
- Within-state comparisons

### Use economic-indicators.md when:
- Focus on income/poverty
- Employment analysis
- Insurance coverage correlation
- Cost barrier assessment

### Use community-factors.md when:
- Housing quality analysis
- Transportation access
- Food access/deserts
- Environmental factors

---

## Data Quality Notes

### SVI
- Updated biennially (most recent: 2022)
- Available for all US census tracts
- Missing for unpopulated tracts

### ADI
- Updated annually
- Block group level (more granular than SVI)
- National and state rankings available

### Census ACS
- 5-year estimates for small areas
- Margin of error increases with smaller populations
- Annual updates

---

## Related Skills

- [Population Intelligence Domain](../population-intelligence-domain.md) - Core concepts
- [Geographic Intelligence](../geographic/README.md) - Geographic profiling
- [Health Patterns](../health-patterns/README.md) - Health-SDOH correlations
- [Cohort Definition](../cohorts/README.md) - SDOH profiles in cohorts

---

## Data Sources

| Source | Content | Geography | Update |
|--------|---------|-----------|--------|
| CDC/ATSDR SVI | 16 social factors | Census Tract | Biennial |
| HRSA ADI | 17 deprivation factors | Block Group | Annual |
| Census ACS | Demographics, economics | All levels | Annual |
| USDA Food Atlas | Food access | Census Tract | Periodic |
