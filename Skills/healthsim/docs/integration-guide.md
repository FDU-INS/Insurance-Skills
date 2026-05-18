# HealthSim Skills Integration Guide

## Overview

This guide explains how HealthSim skills work together to generate consistent, realistic healthcare data across clinical, claims, and pharmacy domains.

## Skill Hierarchy

```
SKILL.md (Root Router)
├── references/           (Shared Knowledge)
│   ├── code-systems.md
│   ├── terminology.md
│   ├── clinical-rules.md
│   ├── validation-rules.md
│   └── hl7v2-segments.md
├── skills/            (Domain Generators)
│   ├── patientsim/       (Clinical, Orders, Results)
│   ├── membersim/        (Claims)
│   └── rxmembersim/      (Pharmacy)
└── formats/              (Output Transformers)
    ├── fhir-r4.md        (FHIR R4 resources)
    ├── hl7v2-adt.md      (ADT messages)
    ├── hl7v2-orm.md      (Order messages)
    ├── hl7v2-oru.md      (Result messages)
    ├── x12-834.md        (Enrollment)
    ├── x12-270-271.md    (Eligibility)
    ├── x12-837.md        (Claims)
    ├── x12-835.md        (Remittance)
    ├── ncpdp-d0.md       (Pharmacy)
    ├── csv.md            (CSV export)
    └── sql.md            (SQL export)
```

## Data Flow Patterns

### Pattern 1: Clinical to Claims

Patient encounters generate claims data:

```
PatientSim Encounter → MemberSim Claim → X12 837 Format
```

**Example Flow:**
```json
{
  "step_1_patientsim": {
    "trigger": "Generate a diabetes patient with recent office visit",
    "output": {
      "patient": { "mrn": "PAT001", "conditions": ["E11.9"] },
      "encounter": {
        "class": "O",
        "type": "office_visit",
        "diagnoses": ["E11.9", "E78.5"],
        "procedures": ["99214"]
      }
    }
  },
  "step_2_membersim": {
    "input": "encounter from step 1",
    "output": {
      "claim": {
        "claim_id": "CLM20250115001",
        "claim_type": "PROFESSIONAL",
        "principal_diagnosis": "E11.9",
        "claim_lines": [
          { "cpt": "99214", "charge": 175.00 }
        ]
      }
    }
  },
  "step_3_format": {
    "input": "claim from step 2",
    "output": "X12 837P transaction"
  }
}
```

### Pattern 2: Clinical to Pharmacy

Patient conditions drive medication prescriptions:

```
PatientSim Condition → RxMemberSim Prescription → NCPDP D.0
```

**Example Flow:**
```json
{
  "step_1_patientsim": {
    "trigger": "Generate heart failure patient on standard therapy",
    "output": {
      "patient": { "mrn": "PAT002" },
      "conditions": ["I50.22"],
      "medications": [
        { "name": "Lisinopril", "dose": "20mg", "frequency": "daily" },
        { "name": "Metoprolol", "dose": "50mg", "frequency": "twice daily" }
      ]
    }
  },
  "step_2_rxmembersim": {
    "input": "medications from step 1",
    "output": {
      "prescription": {
        "ndc": "00093505601",
        "drug_name": "Lisinopril 20mg",
        "quantity": 30,
        "days_supply": 30
      },
      "claim": {
        "claim_id": "RX20250115001",
        "transaction_code": "B1"
      }
    }
  },
  "step_3_format": {
    "input": "claim from step 2",
    "output": "NCPDP D.0 B1 transaction"
  }
}
```

### Pattern 3: Claims to Remittance

Claims adjudication generates payment advice:

```
MemberSim Claim → MemberSim Adjudication → X12 835 Format
```

**Example Flow:**
```json
{
  "step_1_claim": {
    "claim_id": "CLM20250115001",
    "total_charge": 175.00
  },
  "step_2_adjudication": {
    "status": "paid",
    "allowed_amount": 150.00,
    "paid_amount": 125.00,
    "patient_responsibility": 25.00,
    "adjustments": [
      { "group": "CO", "code": "45", "amount": 25.00 }
    ]
  },
  "step_3_format": {
    "output": "X12 835 remittance advice"
  }
}
```

### Pattern 4: Enrollment to Claims

Member enrollment enables claims processing:

```
MemberSim Enrollment → X12 834 → Eligibility → Claim Processing
```

**Example Flow:**
```json
{
  "step_1_enrollment": {
    "trigger": "Generate new employee enrollment with family coverage",
    "output": {
      "enrollment": {
        "transaction_type": "add",
        "enrollment_reason": "new_hire",
        "subscriber": {
          "member_id": "MEM001234567",
          "name": "Michael Johnson"
        },
        "dependents": [
          { "relationship": "01", "name": "Sarah Johnson" },
          { "relationship": "19", "name": "Emma Johnson" }
        ],
        "coverage": {
          "plan_code": "PPO-GOLD",
          "coverage_tier": "FAM",
          "effective_date": "2025-02-01"
        }
      }
    }
  },
  "step_2_format": {
    "input": "enrollment from step 1",
    "output": "X12 834 enrollment transaction"
  },
  "step_3_eligibility_check": {
    "trigger": "Provider checks eligibility before service",
    "input": {
      "member_id": "MEM001234567",
      "service_date": "2025-02-15",
      "service_type": "48"
    },
    "output": {
      "270_inquiry": "X12 270 eligibility request",
      "271_response": {
        "status": "active",
        "deductible_remaining": 500.00,
        "oop_remaining": 4000.00
      }
    }
  },
  "step_4_claim": {
    "input": "verified eligibility",
    "output": {
      "claim": {
        "member_id": "MEM001234567",
        "claim_id": "CLM20250215001",
        "status": "paid"
      }
    }
  }
}
```

### Pattern 5: Orders to Results

Clinical orders generate lab/radiology results:

```
PatientSim Order → HL7v2 ORM → Lab/Radiology → HL7v2 ORU
```

**Example Flow:**
```json
{
  "step_1_order": {
    "trigger": "Generate a CMP lab order for diabetes patient",
    "output": {
      "order": {
        "order_id": "ORD20250115001",
        "order_type": "LAB",
        "code": "80053",
        "description": "Comprehensive Metabolic Panel",
        "priority": "routine",
        "status": "new"
      }
    }
  },
  "step_2_hl7v2_orm": {
    "input": "order from step 1",
    "output": "ORM^O01 message"
  },
  "step_3_results": {
    "input": "completed order",
    "output": {
      "results": [
        { "code": "2345-7", "name": "Glucose", "value": 142, "flag": "H" },
        { "code": "4548-4", "name": "HbA1c", "value": 8.2, "flag": "H" }
      ]
    }
  },
  "step_4_hl7v2_oru": {
    "input": "results from step 3",
    "output": "ORU^R01 message"
  }
}
```

### Pattern 6: Full Patient Journey

Complete patient lifecycle across all domains:

```
MemberSim (Enrollment) → X12 834
    ↓
MemberSim (Eligibility Check) → X12 270/271
    ↓
PatientSim (Registration)
    ↓
PatientSim (Encounter) → HL7v2 ADT A01
    ↓
PatientSim (Orders) → HL7v2 ORM
    ↓
PatientSim (Results) → HL7v2 ORU
    ↓
PatientSim (Diagnosis/Treatment) → FHIR Bundle
    ↓
MemberSim (Professional Claim) → X12 837P
    ↓
MemberSim (Adjudication) → X12 835
    ↓
RxMemberSim (Prescription Fill) → NCPDP D.0
    ↓
PatientSim (Discharge) → HL7v2 ADT A03
```

## Cross-Domain Consistency

### Shared Identifiers

All skills must use consistent identifiers across domains:

| Identifier | PatientSim | MemberSim | RxMemberSim |
|------------|------------|-----------|-------------|
| Patient | `patient.mrn` | `member.member_id` | `member.member_id` |
| Provider | `provider.npi` | `provider.npi` | `prescriber.npi` |
| Encounter | `encounter.id` | `claim.encounter_ref` | N/A |
| Diagnosis | `condition.code` | `claim.diagnosis` | `prescription.diagnosis` |

### Identifier Mapping Example

```json
{
  "patient_context": {
    "patientsim_mrn": "PAT001234",
    "membersim_member_id": "MEM001234",
    "rxmembersim_member_id": "MEM001234",
    "cardholder_id": "001234001"
  },
  "provider_context": {
    "patientsim_provider_npi": "1234567890",
    "membersim_billing_npi": "1234567890",
    "membersim_rendering_npi": "9876543210",
    "rxmembersim_prescriber_npi": "1234567890"
  }
}
```

## Diagnosis Consistency

### Clinical to Claims Mapping

PatientSim conditions must map correctly to claim diagnoses:

```json
{
  "patientsim_condition": {
    "code": "E11.65",
    "display": "Type 2 diabetes with hyperglycemia",
    "onset_date": "2020-03-15",
    "status": "active"
  },
  "membersim_claim": {
    "principal_diagnosis": "E11.65",
    "diagnosis_pointer": 1,
    "present_on_admission": "Y"
  }
}
```

### Diagnosis-Medication Alignment

Prescriptions must align with patient conditions:

| Condition | Expected Medications | NDC Examples |
|-----------|---------------------|--------------|
| E11.9 (T2DM) | Metformin, GLP-1 agonists | 00093-5850-01 |
| I50.22 (CHF) | ACE-I, Beta-blocker, Diuretic | 00093-5056-01 |
| I10 (HTN) | ACE-I, ARB, CCB | 00093-7180-01 |
| J44.1 (COPD) | LAMA, LABA, ICS | 00310-0165-30 |

## Date Consistency

### Timeline Rules

1. **Prescription written date** ≤ **Service date** ≤ **Fill date**
2. **Encounter date** = **Claim service date**
3. **Admission date** ≤ **Procedure dates** ≤ **Discharge date**
4. **Previous fill date** + **Days supply** ≤ **Refill date** (unless early refill)

### Example Timeline

```
2025-01-10: Encounter (office visit)
2025-01-10: Prescription written
2025-01-10: Claim service date
2025-01-11: Claim submitted
2025-01-12: Prescription filled
2025-01-15: Claim adjudicated
2025-01-20: 835 remittance generated
2025-02-08: Refill (day 27 of 30-day supply = 3 days early, 90% used)
```

## Cost Sharing Consistency

### Member Accumulator Flow

```
Deductible Status → Copay/Coinsurance Calculation → OOP Max Check
```

**Example:**
```json
{
  "accumulator_state": {
    "deductible": { "limit": 1500.00, "met": 1200.00, "remaining": 300.00 },
    "oop_max": { "limit": 6000.00, "met": 2500.00, "remaining": 3500.00 }
  },
  "claim_calculation": {
    "allowed_amount": 500.00,
    "deductible_applied": 300.00,
    "remaining_for_coinsurance": 200.00,
    "coinsurance_rate": 0.20,
    "coinsurance_amount": 40.00,
    "patient_responsibility": 340.00,
    "plan_pays": 160.00
  },
  "new_accumulator_state": {
    "deductible": { "met": 1500.00, "remaining": 0.00 },
    "oop_max": { "met": 2840.00, "remaining": 3160.00 }
  }
}
```

## Multi-Format Output

### Single Source, Multiple Formats

One clinical event can generate multiple format outputs:

```json
{
  "source_event": {
    "type": "inpatient_admission",
    "patient": { "mrn": "PAT001" },
    "encounter": { "id": "ENC001", "class": "I" }
  },
  "format_outputs": {
    "hl7v2": {
      "message_type": "ADT^A01",
      "segments": ["MSH", "EVN", "PID", "PV1", "DG1"]
    },
    "fhir": {
      "resourceType": "Bundle",
      "entry": ["Patient", "Encounter", "Condition"]
    },
    "x12_837i": {
      "transaction": "837",
      "claim_type": "institutional"
    }
  }
}
```

## Coordination of Benefits

### Primary/Secondary Claims

```json
{
  "cob_cohort": {
    "primary_payer": {
      "payer_id": "PAYER01",
      "claim_response": {
        "paid": 800.00,
        "patient_responsibility": 200.00
      }
    },
    "secondary_payer": {
      "payer_id": "PAYER02",
      "claim_submission": {
        "total_charge": 1000.00,
        "primary_paid": 800.00,
        "amount_claimed": 200.00
      },
      "claim_response": {
        "paid": 150.00,
        "patient_responsibility": 50.00
      }
    },
    "final_patient_pay": 50.00
  }
}
```

## Error Handling Patterns

### Rejected Claim Flow

```
Claim Submitted → Rejected (Code 75: PA Required)
    ↓
PA Request Submitted → Approved
    ↓
Claim Resubmitted (with PA number) → Paid
    ↓
835 Remittance Generated
```

### DUR Override Flow

```
Rx Claim Submitted → Soft Reject (Early Refill)
    ↓
Pharmacist Review → Override with DUR code
    ↓
Claim Resubmitted (with DUR/PPS segment) → Paid
```

## Prompt Chaining Examples

### Example 1: Generate Complete Patient with Claims

```
Prompt 1: "Generate a 65-year-old male patient with type 2 diabetes,
           hypertension, and CKD stage 3"
→ PatientSim generates patient demographics, conditions, medications

Prompt 2: "Generate a professional claim for an office visit for this patient"
→ MemberSim generates 837P claim with E11.9, I10, N18.3

Prompt 3: "Adjudicate this claim with $500 remaining deductible"
→ MemberSim generates adjudication, calculates cost sharing

Prompt 4: "Generate the 835 remittance for this claim"
→ Format skill generates X12 835 transaction
```

### Example 2: Pharmacy Claim with DUR

```
Prompt 1: "Generate a pharmacy claim for Lisinopril 20mg, quantity 30"
→ RxMemberSim generates NCPDP B1 claim

Prompt 2: "The patient filled this same medication 20 days ago
           with 30 days supply. Show the DUR alert."
→ RxMemberSim generates early refill alert (ER code)

Prompt 3: "Override the DUR alert with pharmacist consultation"
→ RxMemberSim generates claim with DUR/PPS override
```

## Best Practices

### 1. Maintain Context
When chaining prompts, explicitly reference previous outputs to maintain consistency.

### 2. Use Consistent Identifiers
Always use the same patient/member/provider identifiers across related transactions.

### 3. Respect Clinical Logic
Ensure medications align with conditions, procedures align with diagnoses.

### 4. Follow Timelines
Maintain logical date sequences across encounters, claims, and fills.

### 5. Validate Cross-References
Verify that claim references (encounter IDs, authorization numbers) are consistent.

## Analytics Database Integration

For loading data to analytics databases, HealthSim uses a conversation-first approach:

### DuckDB (Local)

```
User: Generate 10 patients in star schema format for DuckDB

Claude:
1. Generates CREATE TABLE + INSERT statements
2. Outputs SQL directly in conversation
3. User can copy/paste or save to file
```

### Databricks (Enterprise)

**Prerequisites**: Authenticated via Databricks CLI (`databricks auth profiles`)

```
User: Load 10 patients to Databricks. Use catalog 'dev_catalog', schema 'gold'.

Claude:
1. Confirms CLI authentication
2. Generates SQL (CREATE TABLE IF NOT EXISTS + INSERT)
3. Executes via: databricks api post /api/2.0/sql/statements
4. Reports success with row counts
```

No MCP server or Python scripts required - Claude generates SQL and executes via the SQL Statements API.

See [dimensional-analytics.md](../formats/dimensional-analytics.md) for star schema details.

## Related Skills

- [SKILL.md](../SKILL.md) - Root router
- [validation-rules.md](../references/validation-rules.md) - Validation rules
- [testing-patterns.md](testing-patterns.md) - Testing patterns
- [hl7v2-segments.md](../references/hl7v2-segments.md) - HL7v2 segment reference
- [orders-results.md](../skills/patientsim/orders-results.md) - Orders and results cohort
- [dimensional-analytics.md](../formats/dimensional-analytics.md) - Star schema format
