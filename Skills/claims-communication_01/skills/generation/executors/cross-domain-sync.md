---
name: cross-domain-sync
description: Coordinate data generation across multiple HealthSim products
triggers:
  - cross-product
  - sync products
  - link entities
  - coordinate generation
---

# Cross-Domain Sync Skill

Coordinate data generation across multiple HealthSim products to ensure consistency and proper entity linking.

## Overview

When generating data that spans multiple products (PatientSim, MemberSim, RxMemberSim, TrialSim), Cross-Domain Sync ensures:

1. **Identity Correlation** - Same person across products
2. **Event Consistency** - Encounters match claims
3. **Referential Integrity** - All foreign keys valid
4. **Temporal Alignment** - Dates consistent across products

## Identity Correlation Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    IDENTITY CORRELATION                         │
└─────────────────────────────────────────────────────────────────┘

                         Person (Core)
                         ┌──────────┐
                         │ SSN      │ ← Universal correlator
                         │ DOB      │
                         │ Name     │
                         │ Gender   │
                         └────┬─────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │ Patient  │       │ Member   │       │ Subject  │
    │ (PatSim) │       │ (MemSim) │       │ (TriSim) │
    └──────────┘       └──────────┘       └──────────┘
         │                   │
         └─────────┬─────────┘
                   ▼
            ┌──────────┐
            │ RxMember │
            │(RxMemSim)│
            └──────────┘
```

## Cross-Product Triggers

| Trigger Event | Source | Target | Action |
|---------------|--------|--------|--------|
| Encounter | PatientSim | MemberSim | Generate claim |
| Prescription | PatientSim | RxMemberSim | Generate fill |
| Admission | PatientSim | MemberSim | Generate facility claim |
| Lab Order | PatientSim | MemberSim | Generate claim line |
| Trial Visit | TrialSim | PatientSim | Update EMR |

## Sync Operations

### 1. Patient ↔ Member Sync

When both PatientSim and MemberSim are in profile:

```json
{
  "sync": {
    "patient_to_member": {
      "correlator": "ssn",
      "mappings": [
        {"patient.mrn": "member.member_id_xref"},
        {"patient.conditions": "member.diagnoses"},
        {"patient.encounters": "member.claims"}
      ]
    }
  }
}
```

Generated linkage:
```
Patient MRN00000001 ←→ Member MEM001234
├── SSN: xxx-xx-1234 (shared)
├── DOB: 1952-03-18 (validated match)
├── Encounter ENC001 → Claim CLM001
├── Encounter ENC002 → Claim CLM002
└── Condition E11.9 → Claim DX E11.9
```

### 2. Prescription ↔ Fill Sync

When PatientSim and RxMemberSim are in profile:

```json
{
  "sync": {
    "prescription_to_fill": {
      "correlator": "rx_number",
      "mappings": [
        {"prescription.ndc": "fill.ndc"},
        {"prescription.quantity": "fill.quantity"},
        {"prescription.prescriber_npi": "fill.prescriber_npi"}
      ],
      "fill_pattern": {
        "initial_fill_delay": {"min": 0, "max": 3, "unit": "days"},
        "refill_timing": "days_supply - 7 days"
      }
    }
  }
}
```

### 3. Encounter ↔ Claim Sync

Automatic claim generation from encounters:

| Encounter Type | Claim Type | Key Fields |
|----------------|------------|------------|
| Ambulatory | Professional (837P) | CPT, DX, Provider NPI |
| Inpatient | Facility (837I) | DRG, Admit/Discharge, Facility NPI |
| ER | Professional or Facility | Based on admit status |
| Lab | Professional (837P) | CPT for lab codes |

```
Encounter ENC001 (Office Visit)
├── Service Date: 2025-01-15
├── Provider: NPI 1234567890
├── DX: E11.9, I10
├── CPT: 99214, 36415
│
└── Generated Claim CLM001
    ├── Service Date: 2025-01-15
    ├── Billing NPI: 1234567890
    ├── DX: E11.9, I10
    └── Lines:
        ├── Line 1: 99214, $175.00
        └── Line 2: 36415, $15.00
```

### 4. Trial Subject ↔ Patient Sync

When TrialSim is in profile:

```json
{
  "sync": {
    "subject_to_patient": {
      "correlator": "patient_ref",
      "mappings": [
        {"subject.demographics": "patient.demographics"},
        {"subject.baseline_conditions": "patient.conditions"},
        {"trial.visit": "patient.encounter"}
      ]
    }
  }
}
```

## Provider Assignment

Cross-Domain Sync uses NetworkSim for consistent provider assignment:

```
Profile specifies: geography = "Harris County, TX"

NetworkSim provides:
├── PCPs: 1,200 available in geography
├── Specialists: 800 available
├── Facilities: 45 available
└── Pharmacies: 320 available

Assignment rules:
├── Each patient gets 1 PCP (sticky assignment)
├── Specialists assigned by condition
├── Facility assigned by encounter type
└── Pharmacy assigned by proximity (optional)
```

## Consistency Validation

### Pre-Generation Checks

| Check | Description |
|-------|-------------|
| Product compatibility | All products can be generated together |
| Required fields | Each product has required correlators |
| Geography coverage | NetworkSim has providers in specified area |

### Post-Generation Checks

| Check | Description |
|-------|-------------|
| Link completeness | All entities properly linked |
| Date consistency | No claim before encounter |
| Code consistency | Claim DX matches condition |
| Provider validity | All NPIs exist in NetworkSim |

## Sync Report

```
═══════════════════════════════════════════════════════════════════
                    CROSS-DOMAIN SYNC REPORT
═══════════════════════════════════════════════════════════════════

Products: PatientSim, MemberSim, RxMemberSim

IDENTITY CORRELATION
──────────────────────────────────────────────────────────────────
Patient ↔ Member links:    200/200 (100%)
Patient ↔ RxMember links:  200/200 (100%)

EVENT SYNCHRONIZATION
──────────────────────────────────────────────────────────────────
Trigger                 Source Count    Target Count    Match
Encounter → Claim       2,400           2,400           100%
Prescription → Fill     2,400           2,400           100%
Lab Order → Claim Line  4,800           4,800           100%

PROVIDER ASSIGNMENT
──────────────────────────────────────────────────────────────────
Provider Type       Assigned    Unique NPIs    Coverage
PCP                 200         45             100%
Endocrinology       88          12             100%
Ophthalmology       200         8              100%
Pharmacy            200         32             100%

CONSISTENCY VALIDATION
──────────────────────────────────────────────────────────────────
Check                           Status
Date consistency                ✓ Pass
Diagnosis alignment             ✓ Pass
Provider validity               ✓ Pass
Referential integrity           ✓ Pass

═══════════════════════════════════════════════════════════════════
```

## Error Handling

### Missing Provider Coverage

```
⚠ Warning: Insufficient provider coverage

Geography: Rural County, TX
Missing: Endocrinology (0 in-network)

Options:
1. Expand geography to nearest MSA
2. Generate synthetic provider
3. Skip specialist encounters
```

### Date Conflict

```
✗ Error: Date inconsistency detected

Claim CLM001234 date: 2025-01-10
Encounter ENC00456 date: 2025-01-15

Claim cannot precede encounter. Auto-fixing...
Adjusted claim date to 2025-01-15
```

## Configuration

### Sync Preferences

```json
{
  "cross_domain_sync": {
    "claim_generation": {
      "auto_generate": true,
      "delay_days": {"min": 0, "max": 3}
    },
    "fill_generation": {
      "auto_generate": true,
      "initial_delay": {"min": 0, "max": 3},
      "refill_window": 7
    },
    "provider_assignment": {
      "pcp_sticky": true,
      "specialist_by_condition": true,
      "prefer_real_npis": true
    }
  }
}
```

## Related Skills

- **[Identity Correlation](../../common/identity-correlation.md)** - Core linking model
- **[Profile Executor](profile-executor.md)** - Execute profiles
- **[Journey Executor](journey-executor.md)** - Execute journeys
- **[NetworkSim](../../networksim/SKILL.md)** - Provider data

---

*Part of the HealthSim Generative Framework*
