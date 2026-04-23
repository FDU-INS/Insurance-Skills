# Population to Patient Integration

## Overview

This scenario demonstrates how PopulationSim data flows into PatientSim to generate clinically realistic patient records with demographically accurate distributions and SDOH characteristics.

---

## Integration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      PopulationSim                               │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │Demographics │  │   Health    │  │      SDOH Profile       │  │
│  │             │  │ Indicators  │  │                         │  │
│  │ • Age dist  │  │ • Diabetes  │  │ • SVI: 0.72             │  │
│  │ • Sex dist  │  │ • HTN       │  │ • Z59.6 rate: 0.146     │  │
│  │ • Race/eth  │  │ • Obesity   │  │ • Z59.41 rate: 0.118    │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
│         │                │                      │                │
└─────────┼────────────────┼──────────────────────┼────────────────┘
          │                │                      │
          ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       PatientSim                                 │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Person    │  │ Conditions  │  │     Encounters          │  │
│  │             │  │             │  │                         │  │
│  │ • SSN       │  │ • ICD-10    │  │ • Office visits         │  │
│  │ • Name      │  │ • Onset     │  │ • ED visits             │  │
│  │ • DOB       │  │ • Status    │  │ • Inpatient             │  │
│  │ • Address   │  │             │  │ • Z-code documentation  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Workflow

### Step 1: Generate Population Profile

**PopulationSim Skill**: `generate-population-profile`

```
User: Generate a population profile for census tract 48201311500 
in Harris County, Texas.
```

**Output**:
```json
{
  "geography": {
    "type": "tract",
    "fips": "48201311500"
  },
  "demographics": {
    "total_population": 4200,
    "age_distribution": {
      "0_17": 0.28,
      "18_44": 0.38,
      "45_64": 0.22,
      "65_plus": 0.12
    },
    "sex_distribution": {
      "male": 0.48,
      "female": 0.52
    },
    "race_ethnicity": {
      "hispanic": 0.62,
      "black_nh": 0.18,
      "white_nh": 0.14,
      "asian_nh": 0.04
    }
  },
  "health_indicators": {
    "diabetes": 0.128,
    "hypertension": 0.362,
    "obesity": 0.348
  },
  "sdoh_profile": {
    "svi_overall": 0.78,
    "z_code_rates": {
      "Z59.6": 0.182,
      "Z59.41": 0.142,
      "Z56.0": 0.068
    }
  }
}
```

### Step 2: Define Cohort Specification

**PopulationSim Skill**: `define-cohort`

```
User: Define a cohort of 500 adults aged 35-70 with diabetes 
from this population for PatientSim generation.
```

**Output**:
```json
{
  "cohort_id": "cohort-dm-tract48201311500-001",
  "name": "Diabetes Cohort - High SDOH Tract",
  "demographics": {
    "age": {"min": 35, "max": 70},
    "distribution": "population_based"
  },
  "clinical_profile": {
    "conditions": {
      "diabetes": {"prevalence": 1.0, "required": true},
      "hypertension": {"prevalence": 0.55},
      "obesity": {"prevalence": 0.48}
    }
  },
  "sdoh_requirements": {
    "inherit_from_population": true,
    "z_code_prevalence": {
      "Z59.6": 0.182,
      "Z59.41": 0.142
    }
  },
  "size": {"target": 500}
}
```

### Step 3: Generate Patients in PatientSim

**PatientSim Skill**: `generate-patient-cohort`

```
User: Generate 500 patients based on the diabetes cohort specification.
```

**Patient Generation Logic**:

1. **Demographics Assignment**
   - Sample age from 35-70 using population age distribution
   - Assign sex per population sex distribution
   - Assign race/ethnicity per population distribution
   - Generate realistic names matching ethnicity

2. **Condition Assignment**
   - All patients receive E11.9 (Type 2 diabetes)
   - 55% receive I10 (Essential hypertension)
   - 48% receive E66.9 (Obesity)
   - Apply comorbidity correlations

3. **SDOH Z-Code Assignment**
   - 18.2% receive Z59.6 (Low income)
   - 14.2% receive Z59.41 (Food insecurity)
   - 6.8% receive Z56.0 (Unemployment)
   - Apply realistic overlap patterns

4. **Encounter Generation**
   - Apply SDOH-adjusted utilization rates
   - Higher ED utilization for high-SVI patients
   - Lower preventive care for high-vulnerability

---

## Data Mapping

### Demographics Mapping

| PopulationSim Field | PatientSim Field | Transformation |
|---------------------|------------------|----------------|
| `age_distribution` | `patient.birthDate` | Sample from distribution |
| `sex_distribution` | `patient.gender` | Direct mapping |
| `race_ethnicity.hispanic` | `patient.ethnicity` + `patient.race` | Split to FHIR codes |
| `geography.fips` | `patient.address.postalCode` | Map tract to ZIPs |

### Health Indicators Mapping

| PopulationSim Field | PatientSim Field | Transformation |
|---------------------|------------------|----------------|
| `health_indicators.diabetes` | `condition[E11.9]` | Prevalence → assignment |
| `health_indicators.hypertension` | `condition[I10]` | Prevalence → assignment |
| `health_indicators.obesity` | `condition[E66.9]` | Prevalence → assignment |

### SDOH Mapping

| PopulationSim Field | PatientSim Field | Transformation |
|---------------------|------------------|----------------|
| `z_code_rates.Z59.6` | `condition[Z59.6]` | Prevalence → assignment |
| `z_code_rates.Z59.41` | `condition[Z59.41]` | Prevalence → assignment |
| `svi_overall` | `encounter.utilization_adjustment` | SVI → multipliers |

---

## Example Generated Patient

```json
{
  "patient": {
    "id": "patient-uuid-001",
    "mrn": "MRN-789012",
    "identifiers": {
      "ssn": "123-45-6789"
    },
    "name": {
      "given": ["Maria", "Elena"],
      "family": "Garcia"
    },
    "birthDate": "1975-03-15",
    "gender": "female",
    "race": {
      "code": "2106-3",
      "display": "White"
    },
    "ethnicity": {
      "code": "2135-2",
      "display": "Hispanic or Latino"
    },
    "address": {
      "line": ["4521 Telephone Rd"],
      "city": "Houston",
      "state": "TX",
      "postalCode": "77023"
    }
  },
  
  "conditions": [
    {
      "code": "E11.9",
      "display": "Type 2 diabetes mellitus without complications",
      "onset": "2018-06-15",
      "status": "active"
    },
    {
      "code": "I10",
      "display": "Essential (primary) hypertension",
      "onset": "2016-02-10",
      "status": "active"
    },
    {
      "code": "E66.9",
      "display": "Obesity, unspecified",
      "onset": "2015-08-22",
      "status": "active"
    },
    {
      "code": "Z59.6",
      "display": "Low income",
      "onset": "2020-01-15",
      "status": "active",
      "category": "sdoh"
    },
    {
      "code": "Z59.41",
      "display": "Food insecurity",
      "onset": "2021-03-20",
      "status": "active",
      "category": "sdoh"
    }
  ],
  
  "encounters": [
    {
      "type": "office_visit",
      "date": "2024-09-15",
      "reason": "Diabetes follow-up",
      "diagnoses": ["E11.9", "I10", "Z59.41"],
      "provider": "Dr. Sarah Chen"
    },
    {
      "type": "ed_visit",
      "date": "2024-07-22",
      "reason": "Hyperglycemia",
      "diagnoses": ["E11.65", "Z59.6"],
      "disposition": "discharged"
    }
  ],
  
  "sdoh_context": {
    "population_svi": 0.78,
    "assigned_z_codes": ["Z59.6", "Z59.41"],
    "utilization_adjustment": 1.18,
    "care_barriers": ["transportation", "food_access"]
  }
}
```

---

## SDOH-Adjusted Utilization

### Utilization Multipliers by SVI

| SVI Quartile | ED Visits | Inpatient | Preventive | No-Show |
|--------------|-----------|-----------|------------|---------|
| Q1 (0-0.25) | 0.85x | 0.90x | 1.10x | 0.85x |
| Q2 (0.25-0.50) | 0.95x | 0.95x | 1.02x | 0.95x |
| Q3 (0.50-0.75) | 1.08x | 1.05x | 0.92x | 1.12x |
| Q4 (0.75-1.0) | 1.22x | 1.15x | 0.82x | 1.28x |

### Example Calculation

For a patient with SVI = 0.78 (Q4):
- Base ED visits/year: 0.35
- Adjusted ED visits: 0.35 × 1.22 = 0.43

---

## Validation Checklist

- [ ] Patient age distribution matches population profile
- [ ] Sex distribution within ±2% of population
- [ ] Race/ethnicity distribution within ±5% of population
- [ ] Diabetes prevalence = 100% (required condition)
- [ ] Hypertension prevalence ≈ 55%
- [ ] Z59.6 prevalence ≈ 18.2%
- [ ] Z59.41 prevalence ≈ 14.2%
- [ ] ED utilization elevated for high-SVI patients
- [ ] SSN format valid and unique

---

## Related Scenarios

- [Population to Member](population-to-member.md) - Add claims data
- [Population to Trial](population-to-trial.md) - Trial enrollment
- [Full Ecosystem](full-ecosystem-cohort.md) - Complete integration
