---
name: journey-executor
description: Execute journey specifications to generate temporal event sequences
triggers:
  - execute journey
  - run journey
  - generate timeline
  - create events
---

# Journey Executor Skill

Execute approved journey specifications to generate temporal event sequences across HealthSim products.

## Overview

The Journey Executor generates time-based events following a JourneySpecification. It creates realistic timelines with encounters, labs, prescriptions, and claims that flow naturally over time.

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    JOURNEY EXECUTION FLOW                       │
└─────────────────────────────────────────────────────────────────┘

For each patient in profile:

    Journey Spec         Timeline              Events
    ┌─────────┐         ┌─────────┐          ┌─────────────┐
    │ Phases  │ ──────► │ Expand  │ ───────► │ Encounters  │
    │ Events  │         │ Dates   │          │ Labs        │
    │ Rules   │         │ Branch  │          │ Rx Fills    │
    └─────────┘         └─────────┘          │ Claims      │
                                             └─────────────┘
```

## Execution Process

### Step 1: Timeline Expansion

Convert relative timings to absolute dates:

```python
# Journey start = diagnosis date or enrollment date
journey_start = patient.diagnosis_date  # e.g., 2025-01-15

# Phase 1: Initial diagnosis (Month 1)
events[0].date = journey_start + 0 days      # 2025-01-15
events[1].date = journey_start + 7 days      # 2025-01-22

# Phase 2: Titration (Month 2-3)
events[2].date = journey_start + 30 days     # 2025-02-14
```

### Step 2: Apply Variance

Add realistic scheduling variance:

```python
# Specified: day 30 ± 7 days variance
base_date = journey_start + 30 days
variance = random_uniform(-7, +7)
actual_date = base_date + variance  # e.g., 2025-02-11
```

### Step 3: Evaluate Branching

Process conditional branches:

```python
if patient.a1c > 9.0 and month == 6:
    # Take "add_second_agent" branch
    add_events(second_agent_journey)
else:
    # Continue standard pathway
    continue_standard()
```

### Step 4: Generate Events

Create product-specific entities:

| Event Type | PatientSim | MemberSim | RxMemberSim |
|------------|------------|-----------|-------------|
| Encounter | Encounter + Conditions | Professional Claim | - |
| Lab | Observation | Claim line item | - |
| Prescription | MedicationRequest | - | Prescription + Fill |
| Admission | Encounter (inpatient) | Facility Claim | - |

## Execution Example

```
User: "Execute the diabetic first year journey for this cohort"

Claude: "Executing journey 'diabetic_first_year' for 200 patients...

Timeline generation:
- Expanding 12-month journey for each patient
- Applying ±7 day variance to appointments
- Evaluating branching conditions

Progress:
- Phase 1 (Initial): ████████████ 200/200
- Phase 2 (Titration): ████████████ 200/200
- Phase 3 (Stabilization): ████████████ 200/200
- Phase 4 (Ongoing): ████████████ 200/200

Branching results:
- Standard pathway: 156 patients (78%)
- Second agent added: 44 patients (22%)

Events generated:
- Encounters: 2,400 (12 per patient avg)
- Lab observations: 4,800
- Prescriptions: 2,400
- Pharmacy fills: 2,400
- Professional claims: 2,400
- Pharmacy claims: 2,400

Timeline span: 2025-01-15 to 2026-01-14

Save to cohort?"
```

## Event Generation Details

### Encounter Events

```json
{
  "event_type": "encounter",
  "generated": {
    "patientsim": {
      "encounter_id": "ENC00000001",
      "patient_mrn": "MRN00000001",
      "encounter_type": "ambulatory",
      "service_date": "2025-01-15",
      "provider_npi": "1234567890",
      "diagnoses": ["E11.9", "I10"],
      "cpt_codes": ["99214", "36415"]
    },
    "membersim": {
      "claim_id": "CLM20250115000001",
      "member_id": "MEM001234",
      "service_date": "2025-01-15",
      "claim_type": "PROFESSIONAL",
      "claim_lines": [
        {"cpt": "99214", "charge": 175.00},
        {"cpt": "36415", "charge": 15.00}
      ]
    }
  }
}
```

### Prescription Events

```json
{
  "event_type": "prescription",
  "generated": {
    "patientsim": {
      "rx_id": "RX00000001",
      "medication": "Metformin 1000mg",
      "prescriber_npi": "1234567890",
      "written_date": "2025-01-15",
      "quantity": 60,
      "days_supply": 30,
      "refills": 11
    },
    "rxmembersim": {
      "fill_id": "FILL20250115001",
      "ndc": "00093101901",
      "fill_date": "2025-01-15",
      "quantity": 60,
      "days_supply": 30,
      "pharmacy_npi": "9876543210",
      "cost": {
        "ingredient_cost": 12.50,
        "dispensing_fee": 3.00,
        "patient_pay": 10.00
      }
    }
  }
}
```

## Handling Recurrence

### Monthly Refills

```json
{
  "type": "prescription",
  "recurrence": "monthly",
  "details": {"medication": "metformin", "refill": true}
}
```

Generated events:
- Fill 1: 2025-01-15
- Fill 2: 2025-02-14
- Fill 3: 2025-03-16
- ... (with ±3 day variance)

### Quarterly Visits

```json
{
  "type": "encounter",
  "recurrence": "quarterly",
  "details": {"visit_type": "99214"}
}
```

Generated events:
- Visit 1: 2025-01-15 (baseline)
- Visit 2: 2025-04-12 (Q2)
- Visit 3: 2025-07-18 (Q3)
- Visit 4: 2025-10-14 (Q4)

## Branching Execution

### Probability-Based

```json
{
  "branching_rules": [
    {
      "condition": "random",
      "branch": "hospitalization",
      "probability": 0.15
    }
  ]
}
```

Result: ~15% of patients follow hospitalization branch

### Condition-Based

```json
{
  "branching_rules": [
    {
      "condition": "a1c > 9.0 at month 6",
      "branch": "intensify_treatment"
    }
  ]
}
```

Result: Patients with A1c > 9.0 at 6-month mark get intensified

## Validation

### Timeline Validation

| Check | Description |
|-------|-------------|
| Chronological order | Events in correct sequence |
| No future dates | All dates ≤ execution date |
| Gap limits | No unrealistic gaps between related events |
| Overlap detection | No conflicting concurrent events |

### Cross-Product Consistency

| Check | Description |
|-------|-------------|
| Encounter → Claim | Every encounter has corresponding claim |
| Rx → Fill | Every prescription has fill history |
| Diagnosis alignment | Claim DX matches clinical conditions |
| Provider consistency | Same provider across related events |

## Execution Report

```
═══════════════════════════════════════════════════════════════════
                    JOURNEY EXECUTION REPORT
═══════════════════════════════════════════════════════════════════

Journey: diabetic_first_year
Profile: medicare-diabetic-texas-001
Patients: 200
Duration: 12 months per patient

EVENT SUMMARY
──────────────────────────────────────────────────────────────────
Event Type          Count       Per Patient (avg)
Encounters          2,400       12.0
Lab Observations    4,800       24.0
Prescriptions       2,400       12.0
Pharmacy Fills      2,400       12.0
Professional Claims 2,400       12.0
Pharmacy Claims     2,400       12.0

BRANCHING RESULTS
──────────────────────────────────────────────────────────────────
Pathway                     Patients    Percentage
Standard management         156         78%
Second agent added          44          22%
  - Sulfonylurea            18          9%
  - SGLT2 inhibitor         14          7%
  - GLP-1 agonist           12          6%

TIMELINE STATISTICS
──────────────────────────────────────────────────────────────────
Earliest event:    2025-01-15
Latest event:      2026-01-14
Avg events/month:  200

═══════════════════════════════════════════════════════════════════
```

## Related Skills

- **[Journey Builder](../builders/journey-builder.md)** - Build specifications
- **[Profile Executor](profile-executor.md)** - Execute profiles
- **[Cross-Domain Sync](cross-domain-sync.md)** - Multi-product coordination
- **[State Management](../../common/state-management.md)** - Save cohorts

---

*Part of the HealthSim Generative Framework*
