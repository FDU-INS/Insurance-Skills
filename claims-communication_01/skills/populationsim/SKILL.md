---
name: populationsim
description: >
  PopulationSim provides population-level intelligence using public data sources.
  Use this skill for ANY request involving: (1) population demographics or profiles,
  (2) geographic health patterns or disparities, (3) social determinants of health (SDOH),
  (4) SVI or ADI analysis, (5) cohort definition or specification, (6) clinical trial
  feasibility, site selection, or enrollment projection, (7) service area analysis,
  (8) health equity assessment, (9) census data or ACS variables, (10) CDC PLACES health indicators.
---

# PopulationSim - Population Intelligence & Cohort Generation

## Overview

PopulationSim provides population-level intelligence using public data (Census ACS, CDC PLACES, SVI, ADI) for:

1. **Standalone Analysis**: Geographic profiling, health disparities, population comparisons
2. **Cross-Product Integration**: Cohort specs driving generation in PatientSim, MemberSim, RxMemberSim, TrialSim

**Key Differentiator**: PopulationSim analyzes real population characteristics and creates specifications — it does not generate synthetic records itself.

## Quick Reference

| I want to... | Use This Skill | Key Triggers |
|--------------|----------------|--------------|
| **Data Access (v2.0)** | | |
| Look up exact data values | `data-access/data-lookup.md` | "what is the exact", "look up", "from PLACES" |
| Resolve FIPS codes | `data-access/geography-lookup.md` | "FIPS for", "which county is", "list counties in MSA" |
| Aggregate geographic data | `data-access/data-aggregation.md` | "aggregate tracts", "metro total", "combine counties" |
| **Geographic Intelligence** | | |
| Profile a county or region | `geographic/county-profile.md` | "county profile", "demographics for", "health indicators" |
| Analyze census tracts | `geographic/census-tract-analysis.md` | "tract level", "granular", "hotspots" |
| Profile a metro area | `geographic/metro-area-profile.md` | "metro", "MSA", "metropolitan" |
| Define custom region | `geographic/custom-region-builder.md` | "service area", "combine", "custom region" |
| **Health Patterns** | | |
| Analyze disease prevalence | `health-patterns/chronic-disease-prevalence.md` | "diabetes rate", "prevalence", "CDC PLACES" |
| Analyze health behaviors | `health-patterns/health-behavior-patterns.md` | "smoking rate", "obesity", "physical activity" |
| Assess healthcare access | `health-patterns/healthcare-access-analysis.md` | "uninsured", "provider ratio", "access" |
| Identify health disparities | `health-patterns/health-outcome-disparities.md` | "disparities", "equity", "by race" |
| **SDOH Analysis** | | |
| Analyze SVI | `sdoh/svi-analysis.md` | "SVI", "social vulnerability", "vulnerable" |
| Analyze ADI | `sdoh/adi-analysis.md` | "ADI", "area deprivation", "deprived" |
| Analyze economics | `sdoh/economic-indicators.md` | "poverty", "income", "unemployment" |
| Analyze community factors | `sdoh/community-factors.md` | "housing", "transportation", "food access" |
| **Cohort Definition** | | |
| Define a cohort | `cohorts/cohort-specification.md` | "define cohort", "cohort spec", "population segment" |
| Build demographics | `cohorts/demographic-distribution.md` | "age distribution", "demographics for cohort" |
| Build clinical profile | `cohorts/clinical-prevalence-profile.md` | "comorbidity rates", "clinical profile" |
| Build SDOH profile | `cohorts/sdoh-profile-builder.md` | "SDOH profile", "Z-code rates" |
| **Trial Support** | | |
| Estimate trial feasibility | `trial-support/feasibility-estimation.md` | "feasibility", "eligible population" |
| Select trial sites | `trial-support/site-selection-support.md` | "site selection", "best locations" |
| Project enrollment | `trial-support/enrollment-projection.md` | "enrollment timeline", "recruitment rate" |

## Safety Guardrails

### All Generated Data is Synthetic

PopulationSim outputs **synthetic, fictional, simulated data** — never real patient records. All profiles and cohort specs are derived from aggregated public statistics and must not be treated as real patient data.

**Do NOT:**
- Present synthetic data as actual patient records
- Make clinical recommendations (e.g., "you should prescribe," "the patient needs") based on generated data
- Pull from or reference real patient databases — use only public reference data

**Do:**
- Remind users that all generated data is synthetic test data
- Use real, valid medical code systems for standards: **ICD-10** (diagnoses), **CPT/HCPCS** (procedures), **LOINC** (labs), **SNOMED** (clinical terms), **RxNorm/NDC** (medications), **NPI** (providers)
- Use real public reference data (Census ACS, CDC PLACES, SVI, ADI) for population characteristics

### Negative Examples — What PopulationSim Must NOT Do

| Scenario | Wrong Response | Correct Response |
|----------|----------------|------------------|
| "What should this patient take?" | "I recommend starting them on metformin" | "This is synthetic test data; PopulationSim does not provide clinical recommendations." |
| "Generate individual patient records" | Emit named patient rows | Route to **PatientSim** — PopulationSim produces population-level profiles and cohort specs, not individual records |
| "Show me real patient data from the database" | Pull from a patient database | "All PopulationSim data is synthetic. Real reference data (Census, PLACES) is population-level only." |
| Population prevalence as individual risk | "This patient has a 28% chance of obesity" | "The county obesity prevalence is 28.0% (CDC PLACES 2024)" — population rates are not individual probabilities |

### Edge Cases

- **Missing FIPS**: Validate inputs; return clear error if FIPS not found in crosswalk files
- **Partial data**: Some tracts lack PLACES or SVI coverage — flag gaps rather than imputing zeros
- **Invalid codes**: Only emit ICD-10, CPT, LOINC, RxNorm, NDC codes from recognized systems

## Output Types

### PopulationProfile

Geographic entity with demographics, health indicators, and SDOH indices:

```json
{
  "geography": {
    "type": "county",
    "fips": "06073",
    "name": "San Diego County",
    "state": "CA",
    "region": "Pacific"
  },
  "demographics": {
    "total_population": 3286069,
    "median_age": 37.1,
    "age_distribution": {
      "0-17": 0.21,
      "18-64": 0.62,
      "65+": 0.17
    },
    "race_ethnicity": {
      "white_nh": 0.43,
      "hispanic": 0.34,
      "asian": 0.12,
      "black": 0.05,
      "other": 0.06
    },
    "median_household_income": 102285,
    "poverty_rate": 0.103
  },
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "diabetes_prevalence": 0.095,
    "obesity_prevalence": 0.280,
    "hypertension_prevalence": 0.285,
    "depression_prevalence": 0.195,
    "smoking_prevalence": 0.098
  },
  "sdoh_indices": {
    "svi_overall": 0.42,
    "svi_themes": {
      "socioeconomic": 0.38,
      "household_composition": 0.45,
      "minority_language": 0.52,
      "housing_transportation": 0.35
    },
    "adi_national_rank": 35
  },
  "healthcare_access": {
    "uninsured_rate": 0.071,
    "pcp_per_100k": 82.4,
    "insurance_mix": {
      "employer": 0.52,
      "medicare": 0.15,
      "medicaid": 0.18,
      "individual": 0.08,
      "uninsured": 0.07
    }
  }
}
```

### CohortSpecification

Generation input for other HealthSim products:

```json
{
  "cohort_id": "houston_diabetics_2024",
  "name": "Houston Metro Diabetic Adults",
  "target_size": 10000,
  "geography": {
    "type": "msa",
    "cbsa_code": "26420",
    "name": "Houston-The Woodlands-Sugar Land, TX"
  },
  "demographics": {
    "age": {
      "min": 18, "max": 85, "mean": 58.4,
      "brackets": { "18-44": 0.18, "45-64": 0.42, "65-74": 0.28, "75+": 0.12 }
    },
    "sex": { "male": 0.48, "female": 0.52 },
    "race_ethnicity": { "white_nh": 0.28, "black": 0.22, "hispanic": 0.38, "asian": 0.08 }
  },
  "clinical_profile": {
    "primary_condition": { "icd10": "E11", "name": "Type 2 Diabetes" },
    "comorbidities": {
      "I10": { "name": "Hypertension", "rate": 0.71 },
      "E78": { "name": "Hyperlipidemia", "rate": 0.68 },
      "E66": { "name": "Obesity", "rate": 0.62 }
    }
  },
  "sdoh_profile": {
    "poverty_rate": 0.18,
    "uninsured_rate": 0.16,
    "food_insecurity": 0.15,
    "svi_mean": 0.58
  },
  "z_code_rates": {
    "Z59.6": { "name": "Low income", "rate": 0.18 },
    "Z59.41": { "name": "Food insecurity", "rate": 0.15 }
  },
  "insurance_mix": {
    "medicare": 0.38, "medicaid": 0.22, "commercial": 0.32, "uninsured": 0.08
  }
}
```

## Cross-Product Integration

### Integration Flow

```
                    ┌─────────────────────┐
                    │   PopulationSim     │
                    │  CohortSpecification│
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ PatientSim  │     │ MemberSim   │     │  TrialSim   │
    │ - patients  │     │ - members   │     │ - subjects  │
    │ - diagnoses │     │ - claims    │     │ - diversity │
    │ - SDOH codes│     │ - plans     │     │ - sites     │
    └──────┬──────┘     └──────┬──────┘     └─────────────┘
           │                   │
           └─────────┬─────────┘
                     ▼
              ┌─────────────┐
              │ RxMemberSim │
              │ - Rx claims │
              │ - adherence │
              └─────────────┘
```

### Integration Patterns

| Output | Receiver | Result |
|--------|----------|--------|
| CohortSpecification | PatientSim | Patients matching demographic/clinical profile |
| CohortSpecification | MemberSim | Members with realistic plan/utilization mix |
| CohortSpecification | TrialSim | Diverse trial subjects meeting FDA guidance |
| PopulationProfile | NetworkSim | Service area provider network design |

## Data Sources

Reference data (100% US coverage) accessible via healthsim MCP tools:

| Source               | Table                                                       | Records | Data Year     |
| -------------------- | ----------------------------------------------------------- | ------- | ------------- |
| CDC PLACES (County)  | `population.places_county` (via healthsim_query_reference)  | 3,143   | 2022 BRFSS    |
| CDC PLACES (Tract)   | `population.places_tract` (via healthsim_query_reference)   | 83,522  | 2022 BRFSS    |
| SVI (County)         | `population.svi_county` (via healthsim_query_reference)     | 3,144   | 2018-2022 ACS |
| SVI (Tract)          | `population.svi_tract` (via healthsim_query_reference)      | 84,120  | 2018-2022 ACS |
| ADI (Block Group)    | `population.adi_blockgroup` (via healthsim_query_reference) | 242,336 | 2019-2023 ACS |
| Geography Crosswalks | geography crosswalks (via healthsim_query)                  | Various | 2023 Census   |

### DuckDB Reference Tables

Reference data also available in DuckDB:

| Table | Source | Purpose |
|-------|--------|---------|
| `population.places_tract` | CDC PLACES | Tract-level health indicators |
| `population.places_county` | CDC PLACES | County-level health indicators |
| `population.svi_tract` | CDC SVI | Tract-level vulnerability |
| `population.svi_county` | CDC SVI | County-level vulnerability |
| `population.adi_blockgroup` | ADI | Block group deprivation |

See [Data Architecture](../../docs/data-architecture.md) for details.

## Directory Structure

```
skills/populationsim/
├── SKILL.md                           # This file - master router
├── README.md                          # Product overview
├── population-intelligence-domain.md  # Core domain knowledge
│
├── data/                              # Embedded Data Package (v2.0)
│   ├── README.md                      # Data dictionary
│   ├── county/                        # County-level files
│   ├── tract/                         # Tract-level files
│   ├── block_group/                   # Block group files (ADI)
│   └── crosswalks/                    # FIPS and CBSA mappings
│
├── data-access/                       # Data Access Skills (v2.0)
│   ├── README.md                      # Category overview
│   ├── data-lookup.md                 # Direct value lookups
│   ├── geography-lookup.md            # FIPS code resolution
│   └── data-aggregation.md            # Geographic aggregation
│
├── geographic/                        # Geographic Intelligence
│   ├── README.md                      # Category overview
│   ├── county-profile.md              # County-level profiles
│   ├── census-tract-analysis.md       # Tract-level analysis
│   ├── metro-area-profile.md          # MSA/CBSA profiles
│   └── custom-region-builder.md       # Custom region aggregation
│
├── health-patterns/                   # Health Analysis
│   ├── README.md                      # Category overview
│   ├── chronic-disease-prevalence.md  # Disease burden analysis
│   ├── health-behavior-patterns.md    # Risk factor analysis
│   ├── healthcare-access-analysis.md  # Coverage and access
│   └── health-outcome-disparities.md  # Disparity analysis
│
├── sdoh/                              # Social Determinants
│   ├── README.md                      # SDOH framework overview
│   ├── svi-analysis.md                # Social Vulnerability Index
│   ├── adi-analysis.md                # Area Deprivation Index
│   ├── economic-indicators.md         # Income, poverty, employment
│   └── community-factors.md           # Housing, transportation, food
│
├── cohorts/                           # Cohort Definition
│   ├── README.md                      # CohortSpecification schema
│   ├── cohort-specification.md        # Complete cohort definition
│   ├── demographic-distribution.md    # Age, sex, race distributions
│   ├── clinical-prevalence-profile.md # Comorbidity patterns
│   └── sdoh-profile-builder.md        # SDOH and Z-code rates
│
└── trial-support/                     # Clinical Trial Support
    ├── README.md                      # Trial integration overview
    ├── feasibility-estimation.md      # Eligible population modeling
    ├── site-selection-support.md      # Site network optimization
    └── enrollment-projection.md       # Timeline projections
```

## Quick Examples

### Example 1: County Health Profile

**Request:** "Profile San Diego County health indicators"

**Response:**

San Diego County, CA (FIPS 06073) Population Profile:

**Demographics** (ACS 2022 5-year):
- Total Population: 3,286,069
- Median Age: 37.1 years
- Race/Ethnicity: 43% White NH, 34% Hispanic, 12% Asian, 5% Black

**Health Indicators** (CDC PLACES 2024):
- Diabetes: 9.5% (vs 10.1% national)
- Obesity: 28.0% (vs 32.1% national)
- Hypertension: 28.5% (vs 32.4% national)

**SDOH Indices**:
- SVI Overall: 0.42 (moderate vulnerability)
- ADI National Rank: 35th percentile

### Example 2: Disparities by SVI Quartile

**Request:** "How do health outcomes vary across SVI quartiles?"

**Response:** Stratification by SVI quartile shows clear outcome variation:

| SVI Quartile | Diabetes | Obesity | Uninsured |
|---|---|---|---|
| Q1 (lowest vulnerability) | 8.2% | 26% | 5.1% |
| Q4 (highest vulnerability) | 13.8% | 38% | 14.2% |

Disparity: Q4 tracts show higher prevalence vs Q1 across all indicators; lower-vulnerability areas have better outcomes. See `health-patterns/health-outcome-disparities.md`.

### Example 3: Cohort for PatientSim

**Request:** "Define a cohort of high-risk diabetics in underserved California"

**Response:** Creates CohortSpecification with:
- Geography: CA census tracts with SVI ≥ 0.70
- Demographics: Hispanic 58%, mean age 58.4
- Comorbidities: HTN 71%, obesity 62%
- SDOH: Rx cost barrier 31%, food insecurity 22%

### Example 4: Trial Feasibility

**Request:** "Feasibility for T2DM trial: age 40-70, HbA1c 8-11%"

**Response:**

| Stage | Population | Conversion |
|-------|------------|------------|
| T2DM Prevalent | 34.2M | - |
| Age 40-70 | 24.8M | 72.5% |
| HbA1c 8-11% | 7.4M | 29.8% |
| After exclusions | 4.2M | - |

**Top Metros**: Houston (128K), Miami (115K), Los Angeles (108K)

## Related Products

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data
- [MemberSim](../membersim/SKILL.md) - Health plan member data
- [RxMemberSim](../rxmembersim/SKILL.md) - Pharmacy data
- [TrialSim](../trialsim/SKILL.md) - Clinical trial data
- [NetworkSim](../networksim/SKILL.md) - Provider networks

## Domain Knowledge

See [Population Intelligence Domain](population-intelligence-domain.md) for geographic hierarchy, census data, and SDOH frameworks.

---

## Generative Framework Integration

PopulationSim feeds the [Generative Framework](../generation/SKILL.md) via CohortSpecifications that drive synthetic generation in PatientSim, MemberSim, and TrialSim.
