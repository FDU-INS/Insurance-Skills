---
name: cross-product-integration
description: >
  Defines how PopulationSim integrates with other HealthSim products including
  PatientSim, MemberSim, and TrialSim. Covers data flow, entity mapping, and
  correlation patterns.
---

# Cross-Product Integration

## Overview

PopulationSim serves as the demographic intelligence layer for the HealthSim ecosystem. It provides population profiles and cohort specifications that drive realistic data generation across PatientSim, MemberSim, and TrialSim.

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PopulationSim                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │
│  │  Population     │  │    Cohort       │  │     SDOH        │      │
│  │  Profile        │  │  Specification  │  │    Profile      │      │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘      │
│           │                    │                    │                │
│           └────────────────────┼────────────────────┘                │
│                                │                                     │
└────────────────────────────────┼─────────────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PatientSim    │    │   MemberSim     │    │    TrialSim     │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │  Patient  │  │    │  │  Member   │  │    │  │  Subject  │  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Entity Correlation

### Person → Patient → Member → Subject

The HealthSim identity model extends a base Person entity across contexts:

```json
{
  "Person": {
    "ssn": "123-45-6789",
    "name": { "given": "John", "family": "Smith" },
    "birthDate": "1965-03-15",
    "gender": "male",
    "race": "white_nh",
    "address": { "city": "Houston", "state": "TX", "zip": "77001" }
  },
  
  "Patient": {
    "extends": "Person",
    "mrn": "MRN-12345678",
    "conditions": ["E11.9", "I10"],
    "encounters": [],
    "medications": []
  },
  
  "Member": {
    "extends": "Person",
    "member_id": "MBR-87654321",
    "plan": { "type": "medicare_advantage", "plan_id": "H1234" },
    "claims": []
  },
  
  "Subject": {
    "extends": "Person",
    "subject_id": "SUBJ-001",
    "study_id": "STUDY-2024-001",
    "site_id": "SITE-042",
    "randomization": "ARM-A"
  }
}
```

---

## PopulationSim → PatientSim

### Data Flow

```
CohortSpecification
├── demographics.age → Patient.birthDate (calculated)
├── demographics.sex → Patient.gender
├── demographics.race_ethnicity → Patient.extension[us-core-race]
├── geography → Patient.address
├── clinical_profile.primary_condition → Condition[0]
├── clinical_profile.comorbidities → Condition[1..n]
├── clinical_profile.severity → Condition.severity
├── clinical_profile.medications → MedicationRequest[]
├── sdoh_profile → Condition[] (Z-codes)
└── z_code_rates → Condition[] (Z-codes, weighted)
```

### Example Transformation

**CohortSpecification Input**:
```json
{
  "demographics": {
    "age": { "mean": 62, "std": 12 },
    "sex": { "male": 0.48, "female": 0.52 },
    "race_ethnicity": { "white_nh": 0.28, "hispanic": 0.44 }
  },
  "clinical_profile": {
    "primary_condition": { "code": "E11.9" },
    "comorbidities": {
      "I10": { "rate": 0.71 },
      "E78.5": { "rate": 0.68 }
    }
  },
  "z_code_rates": {
    "Z59.6": { "rate": 0.18 }
  }
}
```

**PatientSim Output**:
```json
{
  "resourceType": "Patient",
  "birthDate": "1962-06-15",
  "gender": "female",
  "extension": [{
    "url": "us-core-race",
    "valueCoding": { "code": "2106-3", "display": "White" }
  }]
}
```

---

## PopulationSim → MemberSim

### Data Flow

```
CohortSpecification
├── demographics → Member.demographics
├── geography → Member.address, Plan.serviceArea
├── insurance_mix → Member.coverage
│   ├── medicare → Medicare parts, MA plans
│   ├── medicaid → State Medicaid program
│   ├── commercial → Employer/individual plans
│   └── dual → Medicare-Medicaid coordination
├── clinical_profile → Member.riskScore (HCC calculation)
├── sdoh_profile → Member.utilizationPattern
└── utilization_patterns → Claim.expectedFrequency
```

### Insurance Type Mapping

| CohortSpec Insurance | MemberSim Coverage |
|---------------------|-------------------|
| medicare | Medicare FFS (Part A/B) |
| medicare_advantage | Medicare Advantage (Part C) |
| medicaid | State Medicaid MCO |
| dual_eligible | D-SNP or FIDE-SNP |
| commercial_employer | Group commercial |
| commercial_individual | ACA marketplace |
| uninsured | Self-pay, charity care |

---

## PopulationSim → TrialSim

### Data Flow

```
CohortSpecification
├── demographics → Subject eligibility
│   ├── age_range → Inclusion criterion
│   └── sex → Inclusion/stratification
├── geography → Site selection
│   ├── population → Feasibility assessment
│   └── disease_prevalence → Expected enrollment
├── clinical_profile → Screening criteria
│   ├── primary_condition → Required diagnosis
│   ├── comorbidities → Exclusion criteria
│   └── severity → Eligibility filter
├── sdoh_profile → Diversity metrics
│   └── race_ethnicity → FDA diversity targets
└── selection_criteria → Protocol I/E criteria
```

### Site Feasibility Calculation

```
Expected Subjects = Population 
                    × Prevalence 
                    × Age/Sex Filter
                    × Exclusion Rate
                    × Enrollment Rate
                    × Competition Factor

Example:
  Harris County Population: 4,731,145
  × Diabetes Prevalence: 0.108
  × Adult 40-75: 0.42
  × Exclusion (CKD Stage 4+): 0.92
  × Enrollment Rate: 0.05
  × Competition: 0.70
  ≈ 7,500 potential subjects
```

---

## Cohort Integration

### Multi-Product Cohort Example

**Cohort**: "Houston Diabetic Family"

```yaml
PopulationSim:
  geography: Harris County, TX
  cohort: Adult diabetics

PatientSim:
  patient: Maria Garcia (E11.9, I10, E66)
  encounters: 
    - PCP visits (4/year)
    - Endocrine consult (2/year)
    - ED visit (1/year - hypoglycemia)
  
MemberSim:
  member: Maria Garcia (same SSN)
  coverage: Medicare Advantage (H1234)
  claims:
    - Professional claims (matching encounters)
    - Pharmacy claims (metformin, lisinopril)
    - DME claims (glucose monitor)

TrialSim:
  subject: Maria Garcia (same SSN)
  study: SGLT2i cardiovascular outcomes
  screening: Eligible (HbA1c 8.2%, no exclusions)
  randomization: Treatment arm
```

---

## Identity Correlation

### SSN as Universal Correlator

```
Person.ssn = "123-45-6789"
     │
     ├──▶ Patient.ssn = "123-45-6789"
     │         └── MRN = "MRN-12345678"
     │
     ├──▶ Member.ssn = "123-45-6789"
     │         └── Member ID = "MBR-87654321"
     │
     └──▶ Subject.ssn = "123-45-6789"
               └── Subject ID = "SUBJ-001"
```

### Cross-Reference Table

| Entity | Primary ID | Secondary ID | Correlator |
|--------|-----------|--------------|------------|
| Person | SSN | - | - |
| Patient | MRN | Patient UUID | SSN |
| Member | Member ID | Subscriber ID | SSN |
| Subject | Subject ID | Screening ID | SSN |

---

## Related Documentation

- [PatientSim SKILL](../../patientsim/SKILL.md) - Patient canonical model and generation patterns
- [MemberSim SKILL](../../membersim/SKILL.md) - Member canonical model and claim patterns
- [TrialSim SKILL](../../trialsim/SKILL.md) - Subject model and trial patterns
- [Data Models Reference](../../../references/data-models.md) - Complete canonical model definitions
