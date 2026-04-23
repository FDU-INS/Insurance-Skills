# PopulationSim Cross-Product Integration

## Overview

PopulationSim serves as the demographic and SDOH foundation for the entire HealthSim ecosystem. This directory contains scenarios demonstrating how PopulationSim integrates with other products to generate cohesive synthetic healthcare data.

---

## Integration Architecture

```
                    ┌─────────────────────────────────────┐
                    │          PopulationSim              │
                    │   Demographics • Health • SDOH      │
                    └─────────────────┬───────────────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
            ▼                         ▼                         ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│    PatientSim     │   │    MemberSim      │   │    TrialSim       │
│  Clinical/EMR     │   │  Payer/Claims     │   │  Clinical Trials  │
└─────────┬─────────┘   └─────────┬─────────┘   └─────────┬─────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────────────┐
                    │       Identity Correlation          │
                    │   Person → Patient → Member → Subject│
                    │         SSN as Universal Key        │
                    └─────────────────────────────────────┘
```

---

## Integration Scenarios

| Scenario | Description | Products |
|----------|-------------|----------|
| [Population to Patient](population-to-patient.md) | Generate patients from population profile | PopulationSim → PatientSim |
| [Population to Member](population-to-member.md) | Generate members with SDOH-driven plan selection | PopulationSim → MemberSim |
| [Population to Trial](population-to-trial.md) | Trial feasibility and subject generation | PopulationSim → TrialSim |
| [Full Ecosystem](full-ecosystem-cohort.md) | End-to-end multi-product generation | All products |

---

## Data Flow Patterns

### Pattern 1: Population → Patient

```
PopulationProfile
    │
    ├── Demographics
    │   └── Age, sex, race/ethnicity distributions
    │
    ├── Health Indicators
    │   └── Condition prevalence (diabetes, hypertension, etc.)
    │
    └── SDOH Profile
        └── Z-code prevalence rates
            │
            ▼
        PatientSim
            │
            ├── Generate Person entities
            ├── Assign conditions by prevalence
            ├── Attach SDOH Z-codes
            └── Create clinical encounters
```

### Pattern 2: Population → Member

```
PopulationProfile
    │
    ├── Healthcare Access
    │   └── Insurance coverage mix (commercial, Medicare, Medicaid)
    │
    ├── Economic Factors
    │   └── Income distribution, poverty rate
    │
    └── SDOH Profile
        └── Vulnerability indices
            │
            ▼
        MemberSim
            │
            ├── Plan selection based on income/SDOH
            ├── Generate enrollment records
            ├── Apply utilization patterns
            └── Create claims with SDOH adjustments
```

### Pattern 3: Population → Trial

```
PopulationProfile
    │
    ├── Demographics
    │   └── Diversity planning targets
    │
    ├── Health Indicators
    │   └── Target condition prevalence
    │
    └── Geography
        └── Site catchment analysis
            │
            ▼
        TrialSim
            │
            ├── Feasibility assessment
            ├── Enrollment projections
            ├── Diversity compliance
            └── Subject generation
```

---

## Identity Correlation

### Universal Identity Model

```json
{
  "person": {
    "ssn": "123-45-6789",
    "person_id": "uuid-person-001",
    "demographics": {
      "first_name": "Maria",
      "last_name": "Garcia",
      "date_of_birth": "1975-03-15",
      "sex": "female",
      "race": "hispanic"
    }
  },
  "product_identities": {
    "patientsim": {
      "mrn": "MRN-789012",
      "patient_id": "uuid-patient-001"
    },
    "membersim": {
      "member_id": "MEM-456789",
      "subscriber_id": "SUB-123456"
    },
    "trialsim": {
      "subject_id": "SUBJ-DM-001",
      "screening_id": "SCR-2024-0042"
    }
  }
}
```

### Correlation Rules

1. **SSN as Primary Key**: Universal correlator across all products
2. **Demographics Consistency**: Name, DOB, sex identical across products
3. **Address Synchronization**: Geographic location consistent
4. **Temporal Alignment**: Enrollment dates and encounters coordinated

---

## SDOH Propagation

### From PopulationSim

```json
{
  "sdoh_profile": {
    "svi_overall": 0.72,
    "z_code_rates": {
      "Z59.6": 0.146,
      "Z59.41": 0.118
    }
  }
}
```

### To PatientSim

```json
{
  "patient": {
    "conditions": [
      {"code": "Z59.6", "display": "Low income"},
      {"code": "Z59.41", "display": "Food insecurity"}
    ]
  }
}
```

### To MemberSim

```json
{
  "member": {
    "sdoh_risk_score": 0.72,
    "plan_recommendation": "medicaid_managed_care",
    "care_management_flag": true
  }
}
```

### To TrialSim

```json
{
  "subject": {
    "sdoh_considerations": {
      "transportation_barrier": true,
      "visit_flexibility_needed": true,
      "stipend_recommended": true
    }
  }
}
```

---

## Usage Examples

### Generate Correlated Population

```
User: Generate a population of 1000 people in Harris County, Texas 
with high SDOH vulnerability, then create patient records, member 
enrollments, and assess trial feasibility for a diabetes study.

PopulationSim Skills Used:
- generate-population-profile
- define-cohort
- generate-sdoh-profile

PatientSim Integration:
- Receive demographics and conditions
- Generate MRNs and encounters
- Attach Z-codes from SDOH profile

MemberSim Integration:
- Receive income and insurance mix
- Generate plan assignments
- Create enrollment records

TrialSim Integration:
- Receive diversity targets
- Assess feasibility
- Generate eligible subjects
```

### Health Equity Analysis

```
User: Analyze the impact of SDOH on diabetes outcomes across 
three Houston-area census tracts with different vulnerability levels.

PopulationSim Skills Used:
- analyze-census-tract (x3)
- compare-populations
- generate-sdoh-profile (x3)

Cross-Product Analysis:
- PatientSim: Clinical outcomes by SDOH level
- MemberSim: Utilization patterns by SDOH
- TrialSim: Enrollment barriers by SDOH
```

---

## Best Practices

### 1. Start with Population

Always begin with PopulationSim to establish demographic foundation before generating product-specific data.

### 2. Maintain Correlation

Use SSN as the universal correlator. Never generate identities independently in downstream products.

### 3. Propagate SDOH

Ensure SDOH characteristics flow consistently to all products. Z-codes in PatientSim should match prevalence from PopulationSim.

### 4. Validate Consistency

Cross-check demographics across products. Age, sex, and geographic location must be identical.

### 5. Document Assumptions

When adjusting prevalence or utilization for specific scenarios, document the rationale and source.

---

## Related Documentation

- [PopulationSim SKILL.md](../../../skills/populationsim/SKILL.md)
- [PatientSim SKILL.md](../../../skills/patientsim/SKILL.md)
- [MemberSim SKILL.md](../../../skills/membersim/SKILL.md)
- [TrialSim SKILL.md](../../../skills/trialsim/SKILL.md)
- [Data Architecture](../../../docs/data-architecture.md)
