---
name: cross-product-integration
description: |
  Master integration guide for PopulationSim across the HealthSim ecosystem. 
  Describes how PopulationSim serves as the demographic and SDOH foundation 
  for PatientSim, MemberSim, RxMemberSim, and TrialSim.
---

# PopulationSim Cross-Product Integration

## Overview

PopulationSim serves as the demographic and SDOH foundation for the HealthSim ecosystem. This guide describes how PopulationSim integrates with PatientSim, MemberSim, RxMemberSim, and TrialSim to create coherent synthetic healthcare data.

---

## Integration Architecture

```
                         ┌─────────────────┐
                         │  PopulationSim  │
                         │  (Foundation)   │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
     ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
     │   PatientSim   │  │   MemberSim    │  │    TrialSim    │
     │   (Clinical)   │  │   (Payer)      │  │   (Research)   │
     └───────┬────────┘  └───────┬────────┘  └────────────────┘
             │                   │
             ▼                   ▼
     ┌────────────────┐  ┌────────────────┐
     │  RxMemberSim   │  │  NetworkSim    │
     │  (Pharmacy)    │  │  (Providers)   │
     └────────────────┘  └────────────────┘
```

---

## Data Flow Patterns

### Pattern 1: Population → Cohort → Patients

```
PopulationProfile          CohortSpecification         PatientSim
     │                           │                         │
     │  demographics ──────────► │  age/sex/race ─────────► Patient
     │  health_indicators ─────► │  conditions ───────────► Diagnoses
     │  sdoh_profile ──────────► │  sdoh_requirements ────► Z-Codes
     │  healthcare_access ─────► │  insurance ────────────► Coverage
```

### Pattern 2: Population → Members → Claims

```
PopulationProfile          MemberSim                   Claims
     │                           │                         │
     │  insurance_coverage ────► │  plan_distribution ───► Enrollment
     │  utilization_patterns ──► │  service_use ─────────► 837 Claims
     │  sdoh_profile ──────────► │  risk_adjustment ─────► HCC Scores
```

### Pattern 3: Population → Feasibility → Enrollment

```
PopulationProfile          TrialSim                    Trial Data
     │                           │                         │
     │  demographics ──────────► │  diversity_targets ───► Subject Demographics
     │  health_indicators ─────► │  condition_prevalence ► Eligibility Pool
     │  geography ─────────────► │  site_catchment ──────► Site Assignment
```

---

## Identity Correlation

### Universal Correlator: SSN

All HealthSim products use SSN as the universal correlator:

```json
{
  "person": {
    "ssn": "123-45-6789",
    "identities": {
      "patientsim": {"mrn": "MRN-001234"},
      "membersim": {"member_id": "MEM-567890"},
      "rxmembersim": {"rx_member_id": "RX-567890"},
      "trialsim": {"subject_id": "SUBJ-001"}
    }
  }
}
```

### Entity Hierarchy

```
Person (base)
├── ssn (universal correlator)
├── demographics (from PopulationSim)
├── sdoh_profile (from PopulationSim)
│
├── Patient (PatientSim extension)
│   ├── mrn
│   ├── clinical_data
│   └── encounters
│
├── Member (MemberSim extension)
│   ├── member_id
│   ├── enrollment
│   └── claims
│
├── RxMember (RxMemberSim extension)
│   ├── rx_member_id
│   ├── rx_claims
│   └── pharmacy_data
│
└── Subject (TrialSim extension)
    ├── subject_id
    ├── screening_data
    └── trial_visits
```

---

## Integration Points

### PopulationSim → PatientSim

| PopulationSim Output | PatientSim Input | Usage |
|---------------------|------------------|-------|
| `demographics.age_distribution` | Patient age generation | Match population age structure |
| `demographics.sex_distribution` | Patient sex assignment | Match population sex ratio |
| `demographics.race_ethnicity` | Patient race/ethnicity | Match population diversity |
| `health_indicators.chronic_conditions` | Diagnosis prevalence | Condition assignment rates |
| `sdoh_profile.z_code_mapping` | Encounter Z-codes | SDOH documentation |
| `healthcare_access.insurance_coverage` | Patient coverage | Primary payer assignment |

### PopulationSim → MemberSim

| PopulationSim Output | MemberSim Input | Usage |
|---------------------|-----------------|-------|
| `healthcare_access.insurance_coverage` | Plan mix | Commercial/Medicare/Medicaid distribution |
| `utilization_patterns` | Service utilization | Claims frequency/cost |
| `sdoh_profile.economic` | Premium tier | Cost sharing level |
| `geography` | Service area | Network assignment |

### PopulationSim → TrialSim

| PopulationSim Output | TrialSim Input | Usage |
|---------------------|----------------|-------|
| `demographics` | Diversity targets | Enrollment planning |
| `health_indicators` | Prevalence rates | Feasibility assessment |
| `sdoh_profile` | Retention risk | Protocol adherence modeling |
| `geography` | Site selection | Catchment area analysis |

---

## Cohort Workflows

### Workflow 1: Generate Diabetic Population for Claims Analysis

```yaml
cohort: diabetic_claims_population
steps:
  1_population_profile:
    skill: geographic-intelligence
    input:
      geography: {type: county, fips: "48201"}
    output: population_profile

  2_cohort_definition:
    skill: cohort-definition
    input:
      source_profile: population_profile
      clinical:
        conditions:
          diabetes: {prevalence: 1.0, required: true}
      demographics:
        age: {min: 40, max: 75}
      size: {target: 5000}
    output: cohort_spec

  3_patient_generation:
    product: patientsim
    skill: patient-panel
    input:
      cohort: cohort_spec
      include_encounters: true
    output: patients

  4_member_enrollment:
    product: membersim
    skill: member-enrollment
    input:
      patients: patients
      plan_distribution: population_based
    output: members

  5_claims_generation:
    product: membersim
    skill: claims-generation
    input:
      members: members
      timeframe: {start: "2024-01-01", end: "2024-12-31"}
    output: claims_837
```

### Workflow 2: Trial Feasibility with SDOH Diversity

```yaml
cohort: trial_feasibility_sdoh
steps:
  1_catchment_analysis:
    skill: trial-site-analysis
    input:
      protocol_id: "DM-CARDIO-001"
      site_locations:
        - {name: "Houston Medical Center", fips: "48201"}
        - {name: "Dallas University", fips: "48113"}
      radius_miles: 30
    output: catchment_profiles

  2_sdoh_assessment:
    skill: sdoh-analysis
    input:
      profiles: catchment_profiles
      focus_themes: [socioeconomic, minority_language]
    output: sdoh_analysis

  3_diversity_planning:
    skill: trial-enrollment-modeling
    input:
      catchment: catchment_profiles
      sdoh: sdoh_analysis
      protocol:
        condition: diabetes
        target_n: 500
        diversity_requirements:
          minority_pct: 0.40
          high_sdoh_pct: 0.30
    output: enrollment_plan

  4_subject_simulation:
    product: trialsim
    skill: subject-enrollment
    input:
      enrollment_plan: enrollment_plan
      simulate_screening: true
    output: trial_subjects
```

### Workflow 3: High-SDOH Patient Panel with Complete Records

```yaml
cohort: high_sdoh_complete_records
steps:
  1_vulnerability_cohort:
    skill: cohort-definition
    input:
      geography: {type: county, fips: "48201"}
      sdoh_requirements:
        vulnerability_level: high
        svi_min: 0.70
      demographics:
        age: {min: 18, max: 65}
      size: {target: 1000}
    output: cohort

  2_patients_with_sdoh:
    product: patientsim
    skill: patient-panel
    input:
      cohort: cohort
      sdoh_z_codes: true
      encounter_types: [ed, inpatient, ambulatory]
    output: patients

  3_pharmacy_records:
    product: rxmembersim
    skill: pharmacy-claims
    input:
      patients: patients
      include_adherence: true
    output: rx_claims

  4_payer_claims:
    product: membersim
    skill: claims-generation
    input:
      patients: patients
      rx_claims: rx_claims
      include_sdoh_adjustments: true
    output: complete_claims
```

---

## Configuration Examples

### Integration Settings in CohortSpecification

```json
{
  "integration": {
    "patientsim": {
      "enabled": true,
      "generate_clinical_data": true,
      "encounter_density": "moderate",
      "include_labs": true,
      "include_vitals": true
    },
    "membersim": {
      "enabled": true,
      "plan_distribution": "population_based",
      "generate_claims": true,
      "claim_types": ["professional", "institutional"]
    },
    "rxmembersim": {
      "enabled": true,
      "generate_rx_claims": true,
      "include_adherence_metrics": true
    },
    "trialsim": {
      "enabled": false
    },
    "identity_correlation": {
      "ssn_as_correlator": true,
      "generate_mrns": true,
      "generate_member_ids": true,
      "mrn_format": "MRN-{sequence:06d}",
      "member_id_format": "MEM-{sequence:09d}"
    }
  }
}
```

### Cross-Product Output Bundle

```json
{
  "bundle_id": "bundle-2024-001",
  "cohort_id": "cohort-diabetes-high-sdoh-001",
  "generated_at": "2024-12-23T10:30:00Z",
  
  "outputs": {
    "populationsim": {
      "population_profile": "pop-48201-2024-001.json",
      "sdoh_analysis": "sdoh-48201-2024-001.json"
    },
    "patientsim": {
      "patients": "patients-001.ndjson",
      "encounters": "encounters-001.ndjson",
      "format": "fhir_r4"
    },
    "membersim": {
      "enrollments": "enrollment-834.x12",
      "claims": "claims-837p.x12",
      "format": "x12_5010"
    },
    "rxmembersim": {
      "rx_claims": "rx-claims-d0.ncpdp",
      "format": "ncpdp_d0"
    }
  },
  
  "correlation_index": {
    "file": "correlation-index.json",
    "description": "SSN to product ID mapping"
  }
}
```

---

## Best Practices

### 1. Start with PopulationSim

Always begin workflows with PopulationSim to establish demographic and SDOH foundations.

### 2. Use Consistent Geography

Maintain geographic consistency across products - use same FIPS codes and tract selections.

### 3. Enable Identity Correlation

Always enable SSN correlation when generating cross-product data.

### 4. Validate SDOH Alignment

Ensure Z-codes in PatientSim match SDOH rates from PopulationSim.

### 5. Match Insurance Distribution

MemberSim plan mix should reflect PopulationProfile insurance coverage.

---

## Related Documentation

- [PatientSim Integration](patientsim-integration.md)
- [MemberSim Integration](membersim-integration.md)
- [TrialSim Integration](trialsim-integration.md)
- [PatientSim SKILL](../../patientsim/SKILL.md)
- [MemberSim SKILL](../../membersim/SKILL.md)
- [RxMemberSim SKILL](../../rxmembersim/SKILL.md)
- [TrialSim SKILL](../../trialsim/SKILL.md)
