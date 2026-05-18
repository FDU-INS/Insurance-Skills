---
name: cohort-specification
description: >
  Create complete CohortSpecification objects combining demographics, clinical
  profiles, and SDOH characteristics. The master skill for cohort definition
  that drives synthetic data generation. Triggers: "define cohort", "create
  cohort spec", "population specification", "cohort for [condition/geography]".
---

# Cohort Specification Skill

## Overview

The cohort-specification skill creates complete CohortSpecification objects that define target populations for synthetic data generation. It combines geographic analysis, health patterns, and SDOH profiles into actionable generation parameters.

**Primary Use Cases**:
- Define patient populations for PatientSim
- Specify member populations for MemberSim
- Create trial subject pools for TrialSim
- Establish baseline populations for cohorts

---

## Trigger Phrases

- "Define a cohort for [condition] in [geography]"
- "Create a cohort specification for [population]"
- "Generate population spec for [use case]"
- "Build a cohort matching [criteria]"
- "Cohort for diabetics in Houston"
- "Medicare population cohort for [area]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string/object | Yes | - | Geographic scope |
| `condition` | string | No | - | Primary condition (ICD-10 or name) |
| `population_type` | string | No | "general" | "general", "chronic", "trial", "plan" |
| `target_size` | int | No | 1000 | Number of records to generate |
| `age_range` | array | No | [0, 100] | [min, max] age |
| `insurance_filter` | string | No | - | Filter by coverage type |
| `sdoh_level` | string | No | "match_geography" | "low", "moderate", "high", "match_geography" |

---

## Data Sources (Embedded v2.0)

Cohort specifications are built from **real data** in the embedded data package:

| Component | Data Source | File |
|-----------|-------------|------|
| Demographics | SVI tract data | `data/tract/svi_tract_2022.csv` |
| Health Indicators | CDC PLACES | `data/county/places_county_2024.csv` |
| SVI Scores | SVI county/tract | `data/county/svi_county_2022.csv` |
| ADI Rankings | ADI block group | `data/block_group/adi_blockgroup_2023.csv` |
| Metro Counties | CBSA crosswalk | `data/crosswalks/cbsa_definitions.csv` |

### Data-First Specification Pattern

When building a CohortSpecification:
1. **Look up actual values** from embedded data files
2. **Use real prevalence rates** from CDC PLACES
3. **Use real demographic distributions** from SVI tract data
4. **Use real SVI/ADI scores** for SDOH profile
5. **Cite data sources** in the specification metadata

---

## Generation Process

### Step 1: Geographic Foundation
```
Input: "Houston metro"
→ Pull PopulationProfile for CBSA 26420
→ Extract baseline demographics, health indicators, SDOH
```

### Step 2: Apply Condition Filter (if specified)
```
Input: "diabetics"
→ Adjust age distribution (older)
→ Set primary condition E11
→ Apply comorbidity rates from CDC PLACES
```

### Step 3: Build Demographics
```
→ Age distribution (empirical or modeled)
→ Sex distribution
→ Race/ethnicity distribution
→ Adjust for condition if applicable
```

### Step 4: Build Clinical Profile
```
→ Primary condition and severity
→ Comorbidity rates
→ Expected medication patterns
```

### Step 5: Build SDOH Profile
```
→ SVI-derived social factors
→ Economic indicators
→ Z-code assignment rates
```

### Step 6: Set Insurance Mix
```
→ Based on geography or filter
→ Adjust for age (Medicare for 65+)
→ Adjust for income (Medicaid)
```

---

## Output Schema

```json
{
  "cohort_id": "houston_diabetics_2024_001",
  "name": "Houston Metro Adult Diabetics",
  "description": "Type 2 diabetics age 40+ in Houston MSA for care management",
  "target_size": 5000,
  "version": "1.0",
  
  "geography": {
    "type": "msa",
    "cbsa_code": "26420",
    "cbsa_name": "Houston-The Woodlands-Sugar Land, TX",
    "state": "TX",
    "population_source": 7245672
  },
  
  "selection_criteria": {
    "age_range": [40, 85],
    "primary_condition": "E11",
    "exclusions": ["E10", "O24"],
    "insurance_filter": null
  },
  
  "demographics": {
    "age": {
      "min": 40,
      "max": 85,
      "mean": 62.4,
      "std": 12.8,
      "distribution": {
        "40-49": 0.14,
        "50-59": 0.24,
        "60-69": 0.32,
        "70-79": 0.22,
        "80+": 0.08
      }
    },
    "sex": {
      "male": 0.47,
      "female": 0.53
    },
    "race_ethnicity": {
      "white_nh": 0.26,
      "black": 0.24,
      "hispanic": 0.40,
      "asian": 0.08,
      "other": 0.02
    }
  },
  
  "clinical_profile": {
    "primary_condition": {
      "code": "E11",
      "name": "Type 2 Diabetes Mellitus",
      "prevalence": 1.0,
      "severity_distribution": {
        "without_complications_E11.9": 0.35,
        "with_complications_E11.2-E11.6": 0.45,
        "with_multiple_E11.65": 0.20
      }
    },
    "comorbidities": {
      "I10": { "name": "Essential Hypertension", "rate": 0.72, "correlation": "high" },
      "E78.5": { "name": "Hyperlipidemia", "rate": 0.68, "correlation": "high" },
      "E66.9": { "name": "Obesity", "rate": 0.58, "correlation": "high" },
      "F32.9": { "name": "Depression", "rate": 0.26, "correlation": "moderate" },
      "N18.3": { "name": "CKD Stage 3", "rate": 0.18, "correlation": "high" },
      "I25.10": { "name": "CAD", "rate": 0.14, "correlation": "moderate" },
      "G62.9": { "name": "Neuropathy", "rate": 0.22, "correlation": "high" },
      "H35.0": { "name": "Retinopathy", "rate": 0.16, "correlation": "high" }
    },
    "multimorbidity": {
      "conditions_1": 0.12,
      "conditions_2": 0.28,
      "conditions_3": 0.32,
      "conditions_4_plus": 0.28
    },
    "medications": {
      "metformin": 0.72,
      "sulfonylurea": 0.28,
      "sglt2_inhibitor": 0.18,
      "glp1_agonist": 0.14,
      "insulin": 0.32,
      "ace_arb": 0.68,
      "statin": 0.64
    }
  },
  
  "sdoh_profile": {
    "source": "SVI_2022_CBSA_26420",
    "svi_overall": 0.58,
    "svi_themes": {
      "socioeconomic": 0.52,
      "household_composition": 0.48,
      "minority_language": 0.78,
      "housing_transportation": 0.54
    },
    "indicators": {
      "poverty_rate": 0.18,
      "uninsured_rate": 0.16,
      "limited_english": 0.14,
      "no_vehicle": 0.08,
      "food_insecurity": 0.12,
      "housing_instability": 0.09
    }
  },
  
  "z_code_rates": {
    "Z59.6": { "name": "Low income", "rate": 0.18 },
    "Z59.41": { "name": "Food insecurity", "rate": 0.12 },
    "Z60.3": { "name": "Acculturation difficulty", "rate": 0.14 },
    "Z59.82": { "name": "Transportation insecurity", "rate": 0.08 },
    "Z91.120": { "name": "Pt nonadherence intentional", "rate": 0.06 }
  },
  
  "insurance_mix": {
    "medicare": 0.42,
    "medicare_advantage": 0.22,
    "medicaid": 0.14,
    "dual_eligible": 0.08,
    "commercial_employer": 0.24,
    "commercial_individual": 0.04,
    "uninsured": 0.08
  },
  
  "utilization_patterns": {
    "pcp_visits_annual": { "mean": 4.2, "std": 2.1 },
    "specialist_visits_annual": { "mean": 2.8, "std": 1.8 },
    "ed_visits_annual": { "mean": 0.8, "std": 1.2 },
    "hospitalizations_annual": { "mean": 0.18, "std": 0.42 }
  },
  
  "generation_parameters": {
    "sampling_method": "stratified",
    "stratification_vars": ["age_group", "sex", "race_ethnicity"],
    "seed": null,
    "output_format": "fhir_r4"
  },
  
  "validation": {
    "demographic_source": "ACS_2022_5yr",
    "clinical_source": "CDC_PLACES_2024_MEPS",
    "sdoh_source": "CDC_SVI_2022",
    "confidence": "high",
    "notes": "Large MSA, reliable estimates"
  },
  
  "metadata": {
    "created_at": "2024-12-23T10:00:00Z",
    "created_by": "PopulationSim.cohort_specification",
    "use_case": "chronic_care_management",
    "target_product": ["PatientSim", "MemberSim"]
  }
}
```

---

## Examples

### Example 1: Disease Cohort

**Request**: "Define a cohort for heart failure patients in Philadelphia"

**Response**:

**CohortSpecification: Philadelphia Heart Failure**

```yaml
cohort_id: phila_hf_2024
name: Philadelphia Heart Failure Adults
target_size: 2500

geography:
  type: county
  fips: "42101"
  name: Philadelphia County

demographics:
  age:
    mean: 72.4
    range: [45, 95]
    distribution:
      45-64: 0.22
      65-74: 0.34
      75-84: 0.32
      85+: 0.12
  sex:
    male: 0.52
    female: 0.48
  race_ethnicity:
    white_nh: 0.38
    black: 0.42
    hispanic: 0.12
    asian: 0.06

clinical_profile:
  primary_condition: I50 (Heart Failure)
  severity:
    HFrEF (I50.2): 0.45
    HFpEF (I50.3): 0.40
    Unspecified (I50.9): 0.15
  comorbidities:
    I10 (HTN): 0.82
    E11 (DM): 0.42
    I48 (AFib): 0.38
    N18 (CKD): 0.35
    J44 (COPD): 0.24

sdoh_profile:
  svi_overall: 0.72
  poverty_rate: 0.22
  food_insecurity: 0.16

insurance_mix:
  medicare: 0.68
  medicaid: 0.18
  dual: 0.12
  commercial: 0.12
```

---

### Example 2: Health Plan Population

**Request**: "Create a Medicaid population cohort for Arizona"

**Response**:

**CohortSpecification: Arizona Medicaid**

```yaml
cohort_id: az_medicaid_2024
name: Arizona Medicaid Beneficiaries
target_size: 10000

geography:
  type: state
  fips: "04"
  name: Arizona

demographics:
  age:
    distribution:
      0-17: 0.42
      18-44: 0.32
      45-64: 0.18
      65+: 0.08
  sex:
    male: 0.48
    female: 0.52
  race_ethnicity:
    white_nh: 0.38
    hispanic: 0.42
    aian: 0.08
    black: 0.05
    asian: 0.04

clinical_profile:
  # Medicaid population has:
  high_prevalence:
    - Behavioral health (28%)
    - Asthma (12%)
    - Diabetes (9%)
  pediatric_focus:
    - Well child (42%)
    - EPSDT eligible

sdoh_profile:
  svi_overall: 0.68
  poverty_rate: 0.85  # Below 138% FPL
  food_insecurity: 0.28
  housing_instability: 0.18

insurance_mix:
  medicaid_managed: 0.88
  medicaid_ffs: 0.12
```

---

### Example 3: Clinical Trial Cohort

**Request**: "Cohort specification for a NASH clinical trial in the Southeast"

**Response**:

**CohortSpecification: Southeast NASH Trial**

```yaml
cohort_id: se_nash_trial_2024
name: Southeast NASH Trial Population
target_size: 500

geography:
  type: region
  states: [GA, FL, NC, SC, TN]

selection_criteria:
  primary_condition: K75.81 (NASH)
  age_range: [18, 70]
  exclusions:
    - K74.6 (Cirrhosis)
    - K72 (Hepatic failure)
    - B18 (Chronic viral hepatitis)
    - Z94.4 (Liver transplant)

demographics:
  age:
    mean: 52.4
    range: [18, 70]
  sex:
    male: 0.42
    female: 0.58
  race_ethnicity:
    white_nh: 0.58
    black: 0.22
    hispanic: 0.15
    asian: 0.05
  diversity_targets:
    minority: 0.40
    female: 0.50

clinical_profile:
  primary_condition: K75.81
  required_comorbidities:
    E66 (Obesity): 0.85
    E11 (DM): 0.55
    E78 (Dyslipidemia): 0.68
  fibrosis_stage:
    F2: 0.40
    F3: 0.60

trial_parameters:
  randomization_ratio: "1:1:1"
  expected_dropout: 0.15
  screening_to_enrollment: 0.35
```

---

## Validation Rules

### Required Fields
- [ ] cohort_id (unique)
- [ ] geography (type and identifier)
- [ ] demographics.age (range or distribution)
- [ ] demographics.sex

### Distribution Checks
- [ ] Age brackets sum to ~1.0
- [ ] Sex sums to 1.0
- [ ] Race/ethnicity sums to ~1.0
- [ ] Insurance mix sums to ~1.0

### Clinical Checks
- [ ] Comorbidity rates ≤ 1.0
- [ ] Comorbidity rates clinically plausible
- [ ] Severity distribution sums to ~1.0

### SDOH Checks
- [ ] SVI between 0 and 1
- [ ] Z-code rates match SDOH indicators

---

## Related Skills

- [demographic-distribution.md](demographic-distribution.md) - Demographics detail
- [clinical-prevalence-profile.md](clinical-prevalence-profile.md) - Clinical detail
- [sdoh-profile-builder.md](sdoh-profile-builder.md) - SDOH detail
- [county-profile.md](../geographic/county-profile.md) - Source data
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Clinical source
