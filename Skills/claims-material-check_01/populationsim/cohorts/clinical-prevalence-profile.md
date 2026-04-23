---
name: clinical-prevalence-profile
description: >
  Build clinical profiles with disease prevalence, comorbidity patterns, and
  severity distributions for cohorts. Combines CDC PLACES data with clinical
  knowledge for realistic disease burden. Triggers: "clinical profile",
  "comorbidity rates", "disease prevalence for cohort", "severity distribution".
---

# Clinical Prevalence Profile Skill

## Overview

The clinical-prevalence-profile skill creates comprehensive clinical profiles for cohorts, including disease prevalence rates, comorbidity patterns, severity distributions, and expected medication utilization. It leverages CDC PLACES data combined with clinical guidelines and evidence-based comorbidity correlations.

**Primary Use Cases**:
- Define disease burden for chronic cohorts
- Set comorbidity rates
- Establish severity distributions
- Guide medication assignment
- Support clinical realism in synthetic data

---

## Trigger Phrases

- "Clinical profile for [condition] cohort"
- "Comorbidity rates for diabetics"
- "What conditions co-occur with heart failure?"
- "Severity distribution for COPD patients"
- "Disease burden for [geography]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `primary_condition` | string | Yes | - | ICD-10 code or condition name |
| `geography` | string | No | "national" | Geographic adjustment |
| `age_range` | array | No | [18, 100] | Age filter |
| `severity_detail` | bool | No | true | Include severity breakdown |
| `include_medications` | bool | No | true | Include expected meds |

---

## Data Sources (Embedded v2.0)

Clinical prevalence data comes from embedded CDC PLACES files:

| Condition | File | Column |
|-----------|------|--------|
| Diabetes | `data/county/places_county_2024.csv` | DIABETES_CrudePrev |
| Obesity | `data/county/places_county_2024.csv` | OBESITY_CrudePrev |
| Hypertension | `data/county/places_county_2024.csv` | BPHIGH_CrudePrev |
| High Cholesterol | `data/county/places_county_2024.csv` | HIGHCHOL_CrudePrev |
| CHD | `data/county/places_county_2024.csv` | CHD_CrudePrev |
| Stroke | `data/county/places_county_2024.csv` | STROKE_CrudePrev |
| COPD | `data/county/places_county_2024.csv` | COPD_CrudePrev |
| Asthma | `data/county/places_county_2024.csv` | CASTHMA_CrudePrev |
| CKD | `data/county/places_county_2024.csv` | KIDNEY_CrudePrev |
| Arthritis | `data/county/places_county_2024.csv` | ARTHRITIS_CrudePrev |
| Depression | `data/county/places_county_2024.csv` | DEPRESSION_CrudePrev |
| Cancer | `data/county/places_county_2024.csv` | CANCER_CrudePrev |

### Data-First Clinical Profile Pattern

```
1. Look up geographic prevalence from PLACES for primary condition
2. Apply comorbidity rates from clinical knowledge (below)
3. Adjust comorbidities based on geographic health profile
4. Calculate severity distribution from epidemiological patterns
5. Return profile with PLACES source citation
```

---

## Core Comorbidity Patterns

### Type 2 Diabetes (E11)
```json
{
  "primary": "E11",
  "comorbidities": {
    "I10": { "name": "Hypertension", "rate": 0.71, "strength": "strong" },
    "E78": { "name": "Hyperlipidemia", "rate": 0.68, "strength": "strong" },
    "E66": { "name": "Obesity", "rate": 0.62, "strength": "strong" },
    "F32": { "name": "Depression", "rate": 0.28, "strength": "moderate" },
    "N18": { "name": "CKD", "rate": 0.25, "strength": "strong" },
    "G62.9": { "name": "Neuropathy", "rate": 0.22, "strength": "strong" },
    "H35.0": { "name": "Retinopathy", "rate": 0.18, "strength": "strong" },
    "I25": { "name": "CAD", "rate": 0.16, "strength": "moderate" },
    "I50": { "name": "Heart Failure", "rate": 0.12, "strength": "moderate" }
  }
}
```

### Heart Failure (I50)
```json
{
  "primary": "I50",
  "comorbidities": {
    "I10": { "name": "Hypertension", "rate": 0.82, "strength": "strong" },
    "I48": { "name": "Atrial Fibrillation", "rate": 0.42, "strength": "strong" },
    "E11": { "name": "Diabetes", "rate": 0.38, "strength": "moderate" },
    "N18": { "name": "CKD", "rate": 0.35, "strength": "strong" },
    "J44": { "name": "COPD", "rate": 0.28, "strength": "moderate" },
    "I25": { "name": "CAD", "rate": 0.52, "strength": "strong" },
    "F32": { "name": "Depression", "rate": 0.22, "strength": "moderate" },
    "D64.9": { "name": "Anemia", "rate": 0.18, "strength": "moderate" }
  }
}
```

### COPD (J44)
```json
{
  "primary": "J44",
  "comorbidities": {
    "I10": { "name": "Hypertension", "rate": 0.58, "strength": "moderate" },
    "I25": { "name": "CAD", "rate": 0.32, "strength": "moderate" },
    "F32": { "name": "Depression", "rate": 0.38, "strength": "strong" },
    "F41": { "name": "Anxiety", "rate": 0.32, "strength": "moderate" },
    "E66": { "name": "Obesity", "rate": 0.28, "strength": "moderate" },
    "G47.3": { "name": "Sleep Apnea", "rate": 0.22, "strength": "moderate" },
    "J45": { "name": "Asthma overlap", "rate": 0.18, "strength": "moderate" }
  }
}
```

### Depression (F32)
```json
{
  "primary": "F32",
  "comorbidities": {
    "F41": { "name": "Anxiety", "rate": 0.58, "strength": "strong" },
    "G47.0": { "name": "Insomnia", "rate": 0.45, "strength": "strong" },
    "R45.81": { "name": "Low self-esteem", "rate": 0.38, "strength": "moderate" },
    "F10-F19": { "name": "Substance use", "rate": 0.24, "strength": "moderate" },
    "E66": { "name": "Obesity", "rate": 0.22, "strength": "moderate" },
    "M54.5": { "name": "Chronic pain", "rate": 0.28, "strength": "moderate" }
  }
}
```

---

## Severity Distributions

### Diabetes Severity
```json
{
  "E11.9": { "desc": "Without complications", "rate": 0.35 },
  "E11.65": { "desc": "With hyperglycemia", "rate": 0.18 },
  "E11.22": { "desc": "With CKD", "rate": 0.12 },
  "E11.40": { "desc": "With neuropathy", "rate": 0.14 },
  "E11.311": { "desc": "With retinopathy", "rate": 0.08 },
  "E11.51": { "desc": "With PAD", "rate": 0.06 },
  "E11.8": { "desc": "With multiple complications", "rate": 0.07 }
}
```

### Heart Failure Severity
```json
{
  "I50.9": { "desc": "Unspecified", "rate": 0.15 },
  "I50.20": { "desc": "Systolic, unspecified", "rate": 0.18 },
  "I50.22": { "desc": "Systolic, chronic", "rate": 0.28 },
  "I50.30": { "desc": "Diastolic, unspecified", "rate": 0.12 },
  "I50.32": { "desc": "Diastolic, chronic", "rate": 0.18 },
  "I50.42": { "desc": "Combined, chronic", "rate": 0.09 }
}
```

### NYHA Classification (for HF)
```json
{
  "class_I": { "desc": "No limitation", "rate": 0.25 },
  "class_II": { "desc": "Slight limitation", "rate": 0.35 },
  "class_III": { "desc": "Marked limitation", "rate": 0.28 },
  "class_IV": { "desc": "Severe limitation", "rate": 0.12 }
}
```

---

## Output Schema

```json
{
  "clinical_profile": {
    "primary_condition": {
      "code": "E11",
      "name": "Type 2 Diabetes Mellitus",
      "icd10_family": "E11.x",
      "prevalence_in_cohort": 1.0
    },
    
    "severity_distribution": {
      "mild_uncomplicated": {
        "codes": ["E11.9", "E11.65"],
        "rate": 0.35,
        "hba1c_range": [6.5, 7.5]
      },
      "moderate_controlled": {
        "codes": ["E11.65", "E11.22"],
        "rate": 0.40,
        "hba1c_range": [7.5, 8.5]
      },
      "severe_uncontrolled": {
        "codes": ["E11.65", "E11.8"],
        "rate": 0.25,
        "hba1c_range": [8.5, 12.0]
      }
    },
    
    "comorbidities": {
      "cardiovascular": {
        "I10": { "name": "Hypertension", "rate": 0.71 },
        "I25.10": { "name": "CAD", "rate": 0.16 },
        "I50.9": { "name": "Heart Failure", "rate": 0.12 }
      },
      "metabolic": {
        "E78.5": { "name": "Hyperlipidemia", "rate": 0.68 },
        "E66.9": { "name": "Obesity", "rate": 0.62 }
      },
      "renal": {
        "N18.3": { "name": "CKD Stage 3", "rate": 0.15 },
        "N18.4": { "name": "CKD Stage 4", "rate": 0.06 },
        "N18.5": { "name": "CKD Stage 5", "rate": 0.02 }
      },
      "complications": {
        "G62.9": { "name": "Neuropathy", "rate": 0.22 },
        "H35.0": { "name": "Retinopathy", "rate": 0.18 },
        "E11.52": { "name": "PAD", "rate": 0.08 }
      },
      "mental_health": {
        "F32.9": { "name": "Depression", "rate": 0.28 },
        "F41.9": { "name": "Anxiety", "rate": 0.18 }
      }
    },
    
    "multimorbidity": {
      "comorbidity_count_distribution": {
        "0": 0.08,
        "1": 0.18,
        "2": 0.28,
        "3": 0.24,
        "4+": 0.22
      },
      "mean_conditions": 2.8,
      "charlson_index_mean": 3.4
    },
    
    "medications": {
      "diabetes_specific": {
        "metformin": { "rate": 0.72, "first_line": true },
        "sulfonylurea": { "rate": 0.28 },
        "sglt2_inhibitor": { "rate": 0.22 },
        "glp1_agonist": { "rate": 0.18 },
        "dpp4_inhibitor": { "rate": 0.14 },
        "insulin_basal": { "rate": 0.28 },
        "insulin_bolus": { "rate": 0.12 }
      },
      "comorbidity_related": {
        "ace_inhibitor": { "rate": 0.42, "for": "HTN/renal" },
        "arb": { "rate": 0.28, "for": "HTN/renal" },
        "statin": { "rate": 0.68, "for": "lipids/CV" },
        "aspirin": { "rate": 0.38, "for": "CV prevention" },
        "beta_blocker": { "rate": 0.24, "for": "HTN/CV" }
      },
      "polypharmacy": {
        "medications_5_plus": 0.48,
        "medications_10_plus": 0.18,
        "mean_medications": 6.2
      }
    },
    
    "lab_value_expectations": {
      "hba1c": { "mean": 7.8, "std": 1.4, "range": [6.5, 14.0] },
      "fasting_glucose": { "mean": 142, "std": 45 },
      "egfr": { "mean": 72, "std": 24 },
      "ldl": { "mean": 98, "std": 32 }
    }
  },
  
  "geographic_adjustment": {
    "applied": true,
    "geography": "Harris County, TX",
    "adjustments": {
      "diabetes_prevalence": 1.12,
      "obesity_prevalence": 1.08,
      "hypertension_prevalence": 1.04
    }
  },
  
  "validation": {
    "sources": ["CDC_PLACES_2024", "NHANES_2021", "ADA_Guidelines"],
    "evidence_level": "population_based"
  }
}
```

---

## Examples

### Example 1: COPD Clinical Profile

**Request**: "Clinical profile for COPD cohort age 50+"

**Response**:

**COPD Clinical Profile (Adults 50+)**

**Primary Condition**: J44 (Chronic Obstructive Pulmonary Disease)

**Severity (GOLD Classification)**:
| Stage | Description | Rate | FEV1 |
|-------|-------------|------|------|
| GOLD 1 | Mild | 18% | ≥80% |
| GOLD 2 | Moderate | 42% | 50-79% |
| GOLD 3 | Severe | 28% | 30-49% |
| GOLD 4 | Very Severe | 12% | <30% |

**Comorbidities**:
| Condition | ICD-10 | Rate | Relationship |
|-----------|--------|------|--------------|
| Hypertension | I10 | 62% | Common risk factors |
| CAD | I25 | 38% | Shared inflammation |
| Depression | F32 | 42% | Disease burden |
| Anxiety | F41 | 35% | Dyspnea-related |
| Osteoporosis | M81 | 28% | Steroid use |
| Heart Failure | I50 | 22% | Cor pulmonale |
| Lung Cancer | C34 | 8% | Smoking exposure |

**Medications**:
| Drug Class | Rate | Notes |
|------------|------|-------|
| LABA | 68% | Long-acting bronchodilator |
| LAMA | 62% | Tiotropium, etc. |
| ICS | 48% | Inhaled corticosteroid |
| LABA/LAMA combo | 42% | Combination inhaler |
| SABA rescue | 78% | Albuterol PRN |
| Oral steroid burst | 28%/yr | Exacerbation treatment |

---

### Example 2: Multimorbidity Profile

**Request**: "Comorbidity patterns for Medicare population"

**Response**:

**Medicare Population Comorbidity Profile**

**Population**: 65+ years, Medicare beneficiaries

**Top Chronic Conditions**:
| Rank | Condition | Prevalence |
|------|-----------|------------|
| 1 | Hypertension | 58.2% |
| 2 | Hyperlipidemia | 47.8% |
| 3 | Arthritis | 32.4% |
| 4 | Diabetes | 28.6% |
| 5 | Heart Disease | 26.8% |
| 6 | CKD | 24.2% |
| 7 | Depression | 18.4% |
| 8 | COPD | 12.8% |
| 9 | Heart Failure | 14.2% |
| 10 | Alzheimer's/Dementia | 11.8% |

**Multimorbidity Distribution**:
| # Conditions | Prevalence | Cost Impact |
|--------------|------------|-------------|
| 0-1 | 18% | Baseline |
| 2-3 | 32% | 2x |
| 4-5 | 28% | 4x |
| 6+ | 22% | 8x |

**Common Dyads**:
| Pair | Co-occurrence |
|------|---------------|
| HTN + HLD | 42% |
| HTN + DM | 28% |
| DM + HLD | 26% |
| HTN + CKD | 18% |

---

### Example 3: Regional Adjustment

**Request**: "Diabetes clinical profile adjusted for Mississippi Delta"

**Response**:

**Mississippi Delta Diabetes Profile**

*Adjusted for high-prevalence region*

**Baseline vs Adjusted Rates**:
| Metric | National | MS Delta | Adjustment |
|--------|----------|----------|------------|
| Diabetes prevalence | 10.2% | 14.8% | +4.6% |
| Obesity | 32.1% | 42.4% | +10.3% |
| HTN comorbidity | 71% | 78% | +7% |
| CKD comorbidity | 25% | 32% | +7% |

**Severity Shift**:
| Severity | National | MS Delta |
|----------|----------|----------|
| Mild/controlled | 35% | 24% |
| Moderate | 40% | 42% |
| Severe/uncontrolled | 25% | 34% ⚠️ |

**Complications** (higher rates):
| Complication | National | MS Delta |
|--------------|----------|----------|
| Retinopathy | 18% | 24% |
| Neuropathy | 22% | 28% |
| Nephropathy | 25% | 34% |
| Amputation | 0.8% | 1.4% |

---

## Validation Rules

### Required Fields
- [ ] Primary condition code valid
- [ ] Comorbidity rates ≤ 1.0
- [ ] Severity rates sum to ~1.0

### Clinical Plausibility
- [ ] Comorbidities clinically related
- [ ] Medication matches condition
- [ ] Lab values in possible range

---

## Related Skills

- [cohort-specification.md](cohort-specification.md) - Full cohort definition
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Geographic data
- [health-behavior-patterns.md](../health-patterns/health-behavior-patterns.md) - Risk factors
