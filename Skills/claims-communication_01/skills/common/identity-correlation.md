---
name: Identity Correlation
description: Links entities across HealthSim products using SSN as universal correlator
triggers:
  - link patient
  - link member
  - correlate
  - find related
  - cross-product
  - same person
---

# Identity Correlation Skill

Links entities across HealthSim products to enable realistic cross-domain cohorts. Uses SSN as the universal correlator to connect Person → Patient → Member → RxMember → Subject.

## Overview

Healthcare data spans multiple systems: EMRs (patients), claims systems (members), pharmacy systems (rx_members), and clinical trials (subjects). In reality, these all represent the **same person**. HealthSim uses a deliberate identity correlation pattern to maintain this linkage.

## The SSN Correlation Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                      PERSON (Root)                          │
│  SSN: 123-45-6789 (Universal Correlator)                   │
│  Demographics: Name, DOB, Gender, Address                   │
└─────────────────────────────┬───────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│    PATIENT    │    │    MEMBER     │    │    SUBJECT    │
│  (PatientSim) │    │  (MemberSim)  │    │  (TrialSim)   │
│               │    │               │    │               │
│ MRN: MRN00042 │    │ ID: MEM123456 │    │ USUBJID: 0042 │
│ SSN: ********6789│ │ SSN: ********6789│ │ SSN: ********6789│
└───────────────┘    └───────┬───────┘    └───────────────┘
                             │
                    ┌────────▼────────┐
                    │   RX_MEMBER     │
                    │ (RxMemberSim)   │
                    │                 │
                    │ Cardholder: same│
                    │ as Member       │
                    └─────────────────┘
```

## Trigger Phrases

- "Link this patient to their member record"
- "Find all claims for patient MRN00012345"
- "Show the member record for this trial subject"
- "Correlate encounters with pharmacy claims"
- "Find the same person across products"

## How It Works

### 1. Person is Created First

When generating a patient, member, or subject, HealthSim first creates a **Person** entity with core demographics:

```json
{
  "entity_type": "person",
  "ssn": "123-45-6789",
  "name": { "given_name": "Maria", "family_name": "Santos" },
  "birth_date": "1968-05-22",
  "gender": "F",
  "address": { "city": "San Diego", "state": "CA", "zip": "92101" }
}
```

### 2. Domain Entities Reference Person

Each domain entity (patient, member, subject) stores the SSN for correlation:

**Patient (PatientSim)**
```json
{
  "entity_type": "patient",
  "mrn": "MRN00000042",
  "ssn": "123-45-6789",
  "name": { "given_name": "Maria", "family_name": "Santos" }
}
```

**Member (MemberSim)**
```json
{
  "entity_type": "member",
  "member_id": "MEM123456",
  "ssn": "123-45-6789",
  "subscriber_id": "SUB789012"
}
```

**Subject (TrialSim)**
```json
{
  "entity_type": "subject",
  "usubjid": "ONCO-2025-001-005-0042",
  "patient_ref": "MRN00000042",
  "ssn": "123-45-6789"
}
```

### 3. Cross-Product Queries Use SSN

```sql
-- Find all records for a person across products
SELECT 
  p.mrn,
  m.member_id,
  s.usubjid
FROM patients p
LEFT JOIN members m ON p.ssn = m.ssn
LEFT JOIN subjects s ON p.ssn = s.ssn
WHERE p.mrn = 'MRN00000042';
```

## Cross-Domain Triggers

When generating data, certain events trigger generation in related products:

| Trigger Event | Source Product | Target Product | What Gets Generated |
|---------------|----------------|----------------|---------------------|
| Encounter created | PatientSim | MemberSim | Professional/Facility claim |
| Prescription created | PatientSim | RxMemberSim | Pharmacy claim |
| Pharmacy fill | RxMemberSim | MemberSim | Pharmacy claim for integrated plans |
| Trial visit | TrialSim | PatientSim | Linked encounter |
| Hospitalization | PatientSim | MemberSim | Facility claim + Professional claims |

## Example: Complete Cross-Product Generation

```
Generate a diabetic patient with:
- EMR record (PatientSim)
- Health plan membership (MemberSim)
- Pharmacy benefits (RxMemberSim)
- Recent office visit with claim
- Metformin prescription with pharmacy claim
```

Results in correlated entities:

```
Person (SSN: ***-**-6789)
├── Patient (MRN: MRN00000042)
│   ├── Encounter (office visit)
│   └── Prescription (metformin)
├── Member (ID: MEM123456)
│   └── Professional Claim (for office visit)
└── RxMember (Cardholder: MEM123456)
    └── Pharmacy Claim (for metformin)
```

## Provider Correlation (NPI)

Providers are correlated using NPI rather than SSN:

```sql
-- Find provider for an encounter
SELECT 
  e.encounter_id,
  p.provider_name,
  p.primary_specialty
FROM encounters e
JOIN network.providers p ON e.provider_npi = p.npi
WHERE e.encounter_date = '2025-01-15';
```

## Validation Rules

| Rule | Description |
|------|-------------|
| SSN Format | 9 digits, ###-##-#### format |
| SSN Uniqueness | One SSN per person across all products |
| Cross-Product Match | SSN must match when linking entities |
| Demographics Consistency | Name, DOB, gender should match across linked entities |

## Examples

### Link Patient to Member

```
Find the member record for patient MRN00000042
```

```sql
SELECT m.*
FROM members m
JOIN patients p ON m.ssn = p.ssn
WHERE p.mrn = 'MRN00000042';
```

### Find All Claims for Patient

```
Show all claims for patient MRN00000042
```

```sql
SELECT c.*
FROM claims c
JOIN members m ON c.member_id = m.member_id
JOIN patients p ON m.ssn = p.ssn
WHERE p.mrn = 'MRN00000042';
```

### Trial Subject EMR History

```
Get the medical history for trial subject USUBJID 0042
```

```sql
SELECT p.*, d.*, m.*
FROM patients p
JOIN diagnoses d ON p.id = d.patient_id
JOIN medications m ON p.id = m.patient_id
JOIN subjects s ON p.ssn = s.ssn
WHERE s.usubjid LIKE '%0042';
```

## Related Skills

- **[State Management](state-management.md)** - Cohort persistence
- **[DuckDB Skill](duckdb-skill.md)** - Database queries
- **[Generation: Cross-Domain Sync](../generation/executors/cross-domain-sync.md)** - Automated cross-product triggers

## Related Documentation

- [HealthSim Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md)
- [Cross-Domain Examples](../../hello-healthsim/examples/cross-domain-examples.md)
- [Data Architecture](../../docs/data-architecture.md)

---

*Identity correlation is automatic in HealthSim. When you generate linked data, the SSN correlation is handled behind the scenes.*
