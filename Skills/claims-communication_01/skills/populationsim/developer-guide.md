---
name: populationsim-developer-guide
description: |
  Developer guide for PopulationSim covering quick start, core concepts, 
  skill reference, workflows, output formats, integration points, and best 
  practices for working with population demographics and SDOH data.
---

# PopulationSim Developer Guide

## Overview

PopulationSim generates synthetic population demographics, health indicators, and social determinants of health (SDOH) for geographic areas. It serves as the foundational data layer for the HealthSim ecosystem.

---

## Quick Start

### 1. Basic Population Profile

```
User: Create a population profile for Harris County, Texas

Claude: I'll generate a comprehensive population profile for Harris County (FIPS 48201).

[Returns PopulationProfile with demographics, health indicators, SDOH]
```

### 2. SDOH-Focused Analysis

```
User: Analyze social vulnerability in census tracts around downtown Houston

Claude: I'll analyze SVI themes for tracts in the downtown Houston area.

[Returns tract-level SVI analysis with theme breakdowns]
```

### 3. Cohort Definition

```
User: Define a cohort of diabetic adults aged 40-70 in high-vulnerability areas

Claude: I'll create a CohortSpecification targeting diabetic patients in 
high-SDOH census tracts.

[Returns CohortSpecification with clinical and SDOH requirements]
```

---

## Core Concepts

### Geographic Hierarchy

PopulationSim works at multiple geographic levels:

| Level | FIPS Digits | Typical Use |
|-------|-------------|-------------|
| State | 2 | State-level analysis |
| County | 5 | Primary analysis unit |
| Census Tract | 11 | Fine-grained SDOH |
| Block Group | 12 | Most granular (ADI) |
| MSA/CBSA | 5 | Metropolitan areas |

### Data Sources

PopulationSim synthesizes data from:

| Source | Data Type | Update Frequency |
|--------|-----------|------------------|
| Census ACS 5-Year | Demographics | Annual |
| CDC PLACES | Health indicators | Annual |
| CDC/ATSDR SVI | Social vulnerability | Biennial |
| UW Neighborhood Atlas ADI | Area deprivation | Annual |
| USDA Food Access | Food deserts | Periodic |

### Key Models

1. **PopulationProfile** - Complete area snapshot
2. **CohortSpecification** - Population subsetting criteria
3. **GeographicEntity** - Location identification
4. **SDOHProfile** - Social determinants detail

---

## Skill Reference

### Foundation Skills

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| populationsim-foundation | Base demographics | "population profile", "demographics for" |
| geographic-intelligence | Area analysis | "analyze county", "tract-level data" |

### Health & SDOH Skills

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| health-patterns | CDC PLACES indicators | "health indicators", "disease prevalence" |
| sdoh-analysis | SVI/ADI analysis | "social vulnerability", "SDOH profile" |

### Cohort Skills

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| cohort-definition | Define populations | "define cohort", "target population" |

### Trial Support Skills

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| trial-site-analysis | Site feasibility | "trial site", "catchment area" |
| trial-enrollment-modeling | Enrollment simulation | "enrollment projection", "diversity targets" |

---

## Common Workflows

### Workflow 1: County Health Profile

```
Step 1: Request population profile
User: Create a population profile for Dallas County, Texas

Step 2: Review demographics
- Age distribution
- Race/ethnicity composition
- Household structure

Step 3: Examine health indicators
- Chronic condition prevalence
- Health behaviors
- Prevention rates

Step 4: Assess SDOH
- SVI overall and themes
- ADI percentiles
- Z-code prevalence estimates
```

### Workflow 2: High-SDOH Cohort for PatientSim

```
Step 1: Define geography
User: I need patients from high-vulnerability areas of Houston

Step 2: Set SDOH requirements
- SVI ≥ 0.70
- ADI percentile ≥ 70
- Transportation insecurity flag

Step 3: Add clinical criteria
- Age 30-65
- Include diabetes, hypertension
- Exclude pregnancy

Step 4: Generate cohort
- Target size: 1,000
- Enable PatientSim integration
- Include Z-code assignment
```

### Workflow 3: Trial Feasibility Assessment

```
Step 1: Define protocol criteria
User: Assess feasibility for a diabetes trial at three Texas sites

Step 2: Analyze catchment areas
- Houston (48201)
- Dallas (48113)
- San Antonio (48029)

Step 3: Calculate eligible populations
- Age/condition filters
- Exclusion criteria impact

Step 4: Project diversity achievement
- Race/ethnicity targets
- SDOH diversity goals

Step 5: Model retention
- SDOH-adjusted retention rates
- Recommended accommodations
```

---

## Output Formats

### PopulationProfile (JSON)

```json
{
  "profile_id": "pop-48201-2024-001",
  "geography": {
    "type": "county",
    "fips": "48201",
    "name": "Harris County"
  },
  "demographics": {
    "total_population": 4731145,
    "age_distribution": {...},
    "race_ethnicity": {...}
  },
  "health_indicators": {
    "chronic_conditions": {...},
    "health_behaviors": {...}
  },
  "sdoh_profile": {
    "svi": {...},
    "adi": {...},
    "z_code_mapping": {...}
  }
}
```

### CohortSpecification (JSON)

```json
{
  "cohort_id": "cohort-dm-high-sdoh-001",
  "geography": {
    "type": "county",
    "fips": "48201",
    "filters": {"svi_min": 0.70}
  },
  "demographics": {
    "age": {"min": 40, "max": 70}
  },
  "clinical_profile": {
    "conditions": {
      "diabetes": {"required": true}
    }
  },
  "size": {"target": 1000}
}
```

---

## Integration Points

### To PatientSim

PopulationSim provides:
- Age/sex/race distributions for patient generation
- Condition prevalence for diagnosis assignment
- Z-code rates for SDOH documentation

### To MemberSim

PopulationSim provides:
- Insurance coverage distribution
- Utilization patterns
- Risk adjustment factors

### To TrialSim

PopulationSim provides:
- Eligible population estimates
- Diversity profiles
- Retention risk factors

---

## Best Practices

### 1. Start Broad, Then Focus

Begin with county-level profiles, then drill into tracts for SDOH detail.

### 2. Use Appropriate Geography

- County: General analysis, insurance modeling
- Tract: SDOH analysis, vulnerability assessment
- Block group: Fine-grained ADI analysis

### 3. Validate Against Real Data

PopulationSim generates realistic estimates. For production use, validate against actual ACS/PLACES data.

### 4. Consider Temporal Aspects

- ACS 5-year estimates smooth annual fluctuations
- CDC PLACES data has 2-year lag
- SVI updates biennially

### 5. Document Assumptions

When creating cohorts, document:
- Geographic scope
- SDOH thresholds
- Clinical criteria rationale

---

## Troubleshooting

### "No data for this geography"

- Verify FIPS code format (state=2, county=5, tract=11)
- Check if area exists in reference data
- Some rural areas have limited PLACES coverage

### "SDOH rates seem too high/low"

- Verify SVI/ADI thresholds are in valid ranges
- Check if using tract vs. county-level data
- Review Z-code calculation methodology

### "Cohort too small/large"

- Adjust clinical criteria stringency
- Modify SDOH thresholds
- Expand/contract geographic scope

---

## Related Documentation

- [SKILL.md](SKILL.md) - Main skill reference
- [Data Sources](data-sources.md) - Source data details
- [Model Schemas](../../references/populationsim-models/) - Data model definitions
- [Integration Guide](integration/README.md) - Cross-product integration
