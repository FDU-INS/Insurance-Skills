# HealthSim DuckDB Schema

**Version**: 1.0  
**Status**: Active  
**Last Updated**: December 2024

## Overview

The HealthSim DuckDB database provides persistent storage for canonical entities across all six products. It serves as the operational data store for cohorts, enabling cross-product queries and analytics.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HealthSim Workspace                          │
├─────────────────────────────────────────────────────────────────────┤
│  Conversation Layer                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │  Claude + Skills → Generate JSON entities in conversation       ││
│  └─────────────────────────────────────────────────────────────────┘│
│                              ↓                                       │
│  Persistence Layer                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │  cohorts/saved/*.json  ←→  DuckDB (healthsim.duckdb)          ││
│  │       ↑                           ↑                              ││
│  │  cohort_loader.py         cohort_saver.py                    ││
│  └─────────────────────────────────────────────────────────────────┘│
│                              ↓                                       │
│  Query Layer                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │  SQL queries via MCP (healthsim-duckdb) or Python scripts       ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

## Database Location

```
/Users/markoswald/Developer/projects/healthsim-workspace/healthsim.duckdb
```

## Table Summary

| Layer | Tables | Description |
|-------|--------|-------------|
| **Core** | 3 | Shared entities (persons, providers, facilities) |
| **PatientSim** | 8 | Clinical/EMR entities |
| **MemberSim** | 5 | Payer/claims entities |
| **RxMemberSim** | 5 | Pharmacy/PBM entities |
| **TrialSim** | 8 | Clinical trials entities |
| **PopulationSim** | 5 | Demographics/SDOH entities |
| **NetworkSim** | 4 | Provider network entities |
| **State Management** | 3 | Cohort tracking |
| **Total** | **41** | |

---

## Core Entities

### persons
Universal person record - base for Patient, Member, RxMember, Subject.

| Column | Type | Description |
|--------|------|-------------|
| person_id | VARCHAR | Primary key |
| ssn | VARCHAR | **Universal correlator** across products |
| given_name | VARCHAR | First name |
| family_name | VARCHAR | Last name |
| date_of_birth | DATE | |
| gender | VARCHAR | |
| race | VARCHAR | |
| ethnicity | VARCHAR | |
| address_line1 | VARCHAR | |
| city | VARCHAR | |
| state | VARCHAR | |
| postal_code | VARCHAR | |
| county | VARCHAR | |
| census_tract | VARCHAR | For PopulationSim joins |
| county_fips | VARCHAR | For PopulationSim joins |

### providers
Healthcare providers across all products.

| Column | Type | Description |
|--------|------|-------------|
| provider_id | VARCHAR | Primary key |
| npi | VARCHAR | National Provider Identifier (unique) |
| provider_type | VARCHAR | physician, nurse, pharmacist, investigator |
| specialty | VARCHAR | |
| taxonomy_code | VARCHAR | |
| dea_number | VARCHAR | For controlled substances |

### facilities
Healthcare facilities (hospitals, clinics, pharmacies, trial sites).

| Column | Type | Description |
|--------|------|-------------|
| facility_id | VARCHAR | Primary key |
| npi | VARCHAR | Facility NPI |
| facility_type | VARCHAR | hospital, clinic, pharmacy, lab, trial_site |
| name | VARCHAR | |
| county_fips | VARCHAR | For PopulationSim joins |

---

## PatientSim Entities (Clinical/EMR)

### patients
Extends persons with clinical-specific data.

| Column | Type | Description |
|--------|------|-------------|
| patient_id | VARCHAR | Primary key |
| person_id | VARCHAR | FK → persons |
| mrn | VARCHAR | Medical record number (unique) |
| primary_care_provider_id | VARCHAR | |

### encounters
Clinical visits and admissions.

| Column | Type | Description |
|--------|------|-------------|
| encounter_id | VARCHAR | Primary key |
| patient_id | VARCHAR | FK → patients |
| facility_id | VARCHAR | |
| encounter_type | VARCHAR | inpatient, outpatient, emergency |
| start_datetime | TIMESTAMP | |
| drg_code | VARCHAR | For inpatient |

### diagnoses
ICD-10 diagnosis codes.

| Column | Type | Description |
|--------|------|-------------|
| diagnosis_id | VARCHAR | Primary key |
| encounter_id | VARCHAR | FK → encounters |
| code | VARCHAR | ICD-10-CM code |
| diagnosis_type | VARCHAR | principal, secondary |
| present_on_admission | VARCHAR | Y, N, U, W |

### procedures
CPT/HCPCS procedure codes.

| Column | Type | Description |
|--------|------|-------------|
| procedure_id | VARCHAR | Primary key |
| encounter_id | VARCHAR | FK → encounters |
| code | VARCHAR | CPT/HCPCS code |
| modifiers | VARCHAR | Comma-separated |

### lab_results
Laboratory test results.

| Column | Type | Description |
|--------|------|-------------|
| lab_result_id | VARCHAR | Primary key |
| test_code | VARCHAR | LOINC code |
| value_numeric | DECIMAL | |
| abnormal_flag | VARCHAR | N, L, H, LL, HH |

### medications
Medication orders and administrations.

### allergies
Patient allergies.

### vitals
Vital sign measurements.

---

## MemberSim Entities (Payer/Claims)

### members
Extends persons with payer-specific data.

| Column | Type | Description |
|--------|------|-------------|
| member_id | VARCHAR | Primary key |
| person_id | VARCHAR | FK → persons |
| subscriber_id | VARCHAR | |
| payer_name | VARCHAR | |
| plan_type | VARCHAR | HMO, PPO, EPO, HDHP |
| individual_deductible | DECIMAL | |
| individual_oop_max | DECIMAL | |

### accumulators
Year-to-date deductible/OOP tracking.

### claims
Professional and institutional claims.

| Column | Type | Description |
|--------|------|-------------|
| claim_id | VARCHAR | Primary key |
| member_id | VARCHAR | FK → members |
| encounter_id | VARCHAR | Link to PatientSim |
| claim_type | VARCHAR | professional, institutional |
| total_billed | DECIMAL | |
| total_paid | DECIMAL | |
| total_patient_resp | DECIMAL | |

### claim_lines
Line-level claim detail.

| Column | Type | Description |
|--------|------|-------------|
| claim_line_id | VARCHAR | Primary key |
| claim_id | VARCHAR | FK → claims |
| procedure_code | VARCHAR | CPT/HCPCS |
| deductible_applied | DECIMAL | |
| copay_applied | DECIMAL | |
| coinsurance_applied | DECIMAL | |

### authorizations
Prior authorization records.

---

## RxMemberSim Entities (Pharmacy/PBM)

### rx_members
Extends persons with pharmacy benefit data.

| Column | Type | Description |
|--------|------|-------------|
| rx_member_id | VARCHAR | Primary key |
| person_id | VARCHAR | FK → persons |
| member_id | VARCHAR | Link to MemberSim |
| rx_bin | VARCHAR | Bank ID Number |
| rx_pcn | VARCHAR | Processor Control Number |
| cardholder_id | VARCHAR | |

### prescriptions
Prescription orders.

| Column | Type | Description |
|--------|------|-------------|
| prescription_id | VARCHAR | Primary key |
| ndc | VARCHAR | 11-digit NDC |
| prescriber_npi | VARCHAR | |
| days_supply | INTEGER | |
| daw_code | VARCHAR | Dispense As Written |

### pharmacy_claims
Pharmacy claim transactions.

| Column | Type | Description |
|--------|------|-------------|
| pharmacy_claim_id | VARCHAR | Primary key |
| rx_member_id | VARCHAR | FK → rx_members |
| transaction_code | VARCHAR | B1=billing, B2=reversal |
| ndc | VARCHAR | |
| plan_paid | DECIMAL | |
| patient_pay | DECIMAL | |

### dur_alerts
Drug utilization review alerts.

### pharmacies
Pharmacy locations.

---

## TrialSim Entities (Clinical Trials)

### studies
Clinical trial protocols.

| Column | Type | Description |
|--------|------|-------------|
| study_id | VARCHAR | Primary key |
| protocol_number | VARCHAR | |
| phase | VARCHAR | I, II, III, IV |
| therapeutic_area | VARCHAR | |
| target_enrollment | INTEGER | |

### sites
Trial sites.

| Column | Type | Description |
|--------|------|-------------|
| site_id | VARCHAR | Primary key |
| study_id | VARCHAR | FK → studies |
| facility_id | VARCHAR | Link to facilities |
| pi_name | VARCHAR | Principal Investigator |

### treatment_arms
Study treatment arms.

### subjects
Extends persons with trial-specific data.

| Column | Type | Description |
|--------|------|-------------|
| subject_id | VARCHAR | Primary key |
| person_id | VARCHAR | FK → persons |
| patient_id | VARCHAR | Link to PatientSim |
| study_id | VARCHAR | FK → studies |
| usubjid | VARCHAR | CDISC unique ID |
| arm_code | VARCHAR | Randomized arm |

### adverse_events
CDISC-compliant AE records.

| Column | Type | Description |
|--------|------|-------------|
| ae_id | VARCHAR | Primary key |
| subject_id | VARCHAR | FK → subjects |
| aeterm | VARCHAR | Reported term |
| aedecod | VARCHAR | MedDRA PT |
| aesev | VARCHAR | MILD, MODERATE, SEVERE |
| aerel | VARCHAR | Causality assessment |

### visit_schedule
Planned visit definitions.

### actual_visits
Subject visit occurrences.

### disposition_events
Subject disposition (completed, discontinued).

---

## PopulationSim Entities (Demographics/SDOH)

### geographic_entities
Geographic reference data.

| Column | Type | Description |
|--------|------|-------------|
| geo_id | VARCHAR | Primary key |
| geo_type | VARCHAR | state, county, tract |
| state_fips | VARCHAR | |
| county_fips | VARCHAR | |
| tract_fips | VARCHAR | |

### population_profiles
Demographic distributions.

| Column | Type | Description |
|--------|------|-------------|
| profile_id | VARCHAR | Primary key |
| geo_id | VARCHAR | FK → geographic_entities |
| total_population | INTEGER | |
| pct_65_plus | DECIMAL | |
| median_income | INTEGER | |

### health_indicators
CDC PLACES-style health metrics.

| Column | Type | Description |
|--------|------|-------------|
| indicator_id | VARCHAR | Primary key |
| geo_id | VARCHAR | FK → geographic_entities |
| pct_diabetes | DECIMAL | |
| pct_obesity | DECIMAL | |

### sdoh_indices
Social determinants indices.

| Column | Type | Description |
|--------|------|-------------|
| sdoh_id | VARCHAR | Primary key |
| geo_id | VARCHAR | FK → geographic_entities |
| svi_overall | DECIMAL | CDC SVI percentile |
| adi_national_rank | INTEGER | ADI rank 1-100 |

### cohort_specifications
Generation input specifications.

---

## NetworkSim Entities (Provider Networks)

### networks
Network definitions.

| Column | Type | Description |
|--------|------|-------------|
| network_id | VARCHAR | Primary key |
| network_type | VARCHAR | PPO, HMO, EPO |
| payer_name | VARCHAR | |

### network_providers
Provider-network assignments.

### network_facilities
Facility-network assignments.

### provider_specialties
Specialty taxonomy lookup.

---

## State Management

### cohorts
Named cohort containers.

| Column | Type | Description |
|--------|------|-------------|
| cohort_id | VARCHAR | Primary key |
| name | VARCHAR | Unique name |
| entity_count | INTEGER | |
| products | VARCHAR | JSON array of products |
| is_active | BOOLEAN | |

### cohort_entities
Junction table linking entities to cohorts.

| Column | Type | Description |
|--------|------|-------------|
| cohort_id | VARCHAR | FK → cohorts |
| entity_type | VARCHAR | person, patient, claim, etc. |
| entity_id | VARCHAR | Entity primary key |

### cohort_tags
Tag-based filtering.

| Column | Type | Description |
|--------|------|-------------|
| cohort_id | VARCHAR | FK → cohorts |
| tag | VARCHAR | e.g., "diabetes", "emergency" |

---

## Cross-Product Relationships

```
Person (Core)
├── Patient (PatientSim) via person_id
│   └── Encounter → Diagnosis, Procedure, Lab, Medication
├── Member (MemberSim) via person_id
│   └── Claim → ClaimLine
├── RxMember (RxMemberSim) via person_id
│   └── Prescription → PharmacyClaim
└── Subject (TrialSim) via person_id
    └── AdverseEvent, ActualVisit

Geographic Entity (PopulationSim)
├── Person via county_fips/census_tract
├── Facility via county_fips
└── Population Profile → Health Indicators → SDOH Indices

Provider (Core)
├── NetworkProvider (NetworkSim)
├── Encounter.attending_provider_id (PatientSim)
├── Prescription.prescriber_npi (RxMemberSim)
└── Site.pi_provider_id (TrialSim)
```

---

## Sample Queries

### Cross-Product: Patient Journey
```sql
SELECT 
    per.given_name, per.family_name,
    m.plan_name, m.individual_deductible,
    e.encounter_type, e.start_datetime,
    c.total_billed, c.total_patient_resp
FROM persons per
JOIN members m ON per.person_id = m.person_id
JOIN patients p ON per.person_id = p.person_id
JOIN encounters e ON p.patient_id = e.patient_id
JOIN claims c ON e.encounter_id = c.encounter_id
WHERE per.ssn = '555-12-3456';
```

### PopulationSim: High-Risk Areas
```sql
SELECT 
    g.county_name, g.state_name,
    h.pct_diabetes, h.pct_obesity,
    s.svi_overall, s.adi_national_rank
FROM geographic_entities g
JOIN health_indicators h ON g.geo_id = h.geo_id
JOIN sdoh_indices s ON g.geo_id = s.geo_id
WHERE h.pct_diabetes > 15
  AND s.svi_overall > 0.75
ORDER BY s.svi_overall DESC;
```

### TrialSim: Subject Disposition
```sql
SELECT 
    st.protocol_number, st.phase,
    sub.usubjid, sub.arm_code,
    d.dsdecod as disposition
FROM studies st
JOIN subjects sub ON st.study_id = sub.study_id
LEFT JOIN disposition_events d ON sub.subject_id = d.subject_id
WHERE st.study_id = 'ABC-123';
```
