---
name: healthsim
description: "HealthSim generates realistic synthetic healthcare data for testing EMR systems, claims processing, pharmacy benefits, and analytics. Use for ANY request involving: (1) synthetic patients, clinical data, or medical records, (2) healthcare claims, billing, or adjudication, (3) pharmacy prescriptions, formularies, or drug utilization, (4) HL7v2, FHIR, X12, or NCPDP formatted output, (5) healthcare testing cohorts or sample data generation."
---

# HealthSim - Synthetic Healthcare Data Generation

## Overview

HealthSim generates realistic synthetic healthcare data through natural conversation. Rather than writing code or configuration files, describe what you need and Claude generates appropriate data.

**Products:**

| Product | Domain | What It Generates |
|---------|--------|-------------------|
| **PatientSim** | Clinical/EMR | Patients, encounters, diagnoses, procedures, labs, vitals, medications |
| **MemberSim** | Payer/Claims | Members, professional claims, facility claims, payments, accumulators |
| **RxMemberSim** | Pharmacy/PBM | Prescriptions, pharmacy claims, formularies, DUR alerts, prior auths |

## Quick Start

### Generate Clinical Data

**Request:** "Generate a 65-year-old diabetic patient with hypertension"

Claude will produce a patient with:
- Demographics (age 65, realistic name/address)
- Diagnoses (E11.9 Type 2 diabetes, I10 hypertension)
- Medications (metformin, lisinopril)
- Labs (A1C, BMP with values in expected ranges)
- Comorbidities (likely hyperlipidemia, possible obesity)

### Generate Claims

**Request:** "Create a professional claim for an office visit"

Claude will produce:
- Claim header (provider NPI, member ID, service date)
- Service lines (CPT 99213/99214, charges)
- Diagnoses (ICD-10 codes)
- Adjudication (allowed, paid, patient responsibility)

### Generate Pharmacy Data

**Request:** "Generate a pharmacy claim that triggers a drug interaction alert"

Claude will produce:
- Prescription details (NDC, quantity, days supply)
- Pharmacy claim (BIN, PCN, cardholder ID)
- DUR alert (DD code, clinical significance, recommendation)
- Claim response (approved with warning or rejected)

## Cohort Skills

### PatientSim Cohorts

Load these for clinical data generation:

| Cohort | Use When | Key Elements |
|----------|----------|--------------|
| **Diabetes Management** | diabetic, A1C, glucose, metformin, insulin | Disease progression, medication escalation, complications |
| **Heart Failure** | CHF, HFrEF, BNP, ejection fraction | NYHA classification, GDMT therapy, decompensation |
| **Chronic Kidney Disease** | CKD, eGFR, dialysis, nephrology | CKD staging, progression, comorbidities |
| **Sepsis/Acute Care** | sepsis, infection, ICU, critical | Sepsis criteria, antibiotic protocols, ICU stay |

See: [skills/patientsim/](skills/patientsim/) for detailed skills

### MemberSim Cohorts

Load these for claims and payer data:

| Cohort | Use When | Key Elements |
|----------|----------|--------------|
| **Professional Claims** | office visit, 837P, physician claim | E&M coding, place of service, adjudication |
| **Facility Claims** | hospital, inpatient, 837I, DRG | Revenue codes, DRG assignment, LOS |
| **Prior Authorization** | prior auth, pre-cert, authorization | Request/response workflow, approval criteria |
| **Accumulator Tracking** | deductible, OOP, accumulator | Year-to-date tracking, family vs individual |
| **Value-Based Care** | quality measures, VBC, HEDIS | Attribution, measure compliance, incentives |

See: [skills/membersim/](skills/membersim/) for detailed skills

### RxMemberSim Cohorts

Load these for pharmacy and PBM data:

| Cohort | Use When | Key Elements |
|----------|----------|--------------|
| **Retail Pharmacy** | prescription fill, retail, copay | New/refill, pricing, patient pay |
| **Specialty Pharmacy** | specialty drug, biologics, hub | Limited distribution, PA, patient support |
| **DUR Alerts** | drug interaction, DUR, therapeutic dup | Alert types, severity, override |
| **Formulary Management** | formulary, tier, coverage | Tier structure, PA requirements, alternatives |
| **Prior Authorization** | pharmacy PA, step therapy | Clinical criteria, approval workflow |
| **Manufacturer Programs** | copay card, patient assistance | Copay assistance, rebates |

See: [skills/rxmembersim/](skills/rxmembersim/) for detailed skills

## Output Formats

### Default: JSON

By default, Claude outputs data as JSON objects that match the canonical data model.

### Healthcare Standards

Request specific formats:

| Format | Request Phrases | Use Case |
|--------|-----------------|----------|
| **FHIR R4** | "as FHIR", "FHIR bundle", "FHIR resources" | Interoperability, modern APIs |
| **HL7v2** | "as HL7", "ADT message", "HL7v2" | Legacy EMR integration |
| **X12 837** | "as 837", "X12 claim", "EDI format" | Claims submission |
| **X12 835** | "as 835", "remittance", "ERA" | Payment posting |
| **NCPDP D.0** | "as NCPDP", "pharmacy claim format" | Pharmacy transactions |

See: [formats/](formats/) for transformation skills

### Export Formats

| Format | Request Phrases |
|--------|-----------------|
| **CSV** | "as CSV", "save to CSV", "spreadsheet" |
| **Parquet** | "as Parquet", "for analytics" |
| **SQL INSERT** | "as SQL", "INSERT statements" |

## Generation Parameters

### Demographics

| Parameter | Default | Options |
|-----------|---------|---------|
| **age_range** | 18-90 | Any range, e.g., "pediatric (0-17)", "senior (65+)" |
| **gender** | weighted (49% M, 51% F) | "male", "female", specific distribution |
| **count** | 1 | Any number, batches for large counts |

### Clinical (PatientSim)

| Parameter | Options |
|-----------|---------|
| **conditions** | diabetes, heart failure, CKD, hypertension, COPD, etc. |
| **severity** | mild, moderate, severe, well-controlled, poorly-controlled |
| **complications** | with/without specific complications |

### Claims (MemberSim)

| Parameter | Options |
|-----------|---------|
| **claim_type** | professional, institutional, dental |
| **claim_status** | paid, denied, pending, partial |
| **network_status** | in-network, out-of-network |

### Pharmacy (RxMemberSim)

| Parameter | Options |
|-----------|---------|
| **fill_type** | new, refill |
| **drug_type** | generic, brand, specialty |
| **dur_alerts** | none, warning, reject |

## Reproducibility

For consistent results across sessions:

**Request:** "Generate 10 patients using seed 42"

Claude will:
1. Use seed 42 for all random selections
2. Generate identical output if same parameters used
3. Note the seed in output for reference

## Validation

Claude automatically validates generated data for:

- **Structural**: Required fields, data types, formats
- **Temporal**: Date ordering (discharge after admission, etc.)
- **Referential**: Foreign key relationships
- **Clinical**: Age-appropriate conditions, gender-appropriate conditions
- **Business**: Valid code combinations, realistic pricing

Request explicit validation: "Validate this patient data"

## Reference Data

For code lookups and documentation:

- [Data Models](references/data-models.md) - Entity schemas
- [Code Systems](references/code-systems.md) - ICD-10, CPT, LOINC, NDC
- [Validation Rules](references/validation-rules.md) - All validation rules
- [Generation Patterns](references/generation-patterns.md) - Distributions, seeds

## Examples

### Example 1: Simple Patient

**Request:** "Generate a patient"

**Output:**
```json
{
  "mrn": "MRN00000001",
  "name": {
    "given_name": "John",
    "family_name": "Smith"
  },
  "birth_date": "1975-03-15",
  "gender": "M",
  "address": {
    "street_address": "123 Main Street",
    "city": "Springfield",
    "state": "IL",
    "postal_code": "62701"
  }
}
```

### Example 2: Clinical Cohort

**Request:** "Generate a 58-year-old female with poorly controlled Type 2 diabetes"

**Output:**
```json
{
  "patient": {
    "mrn": "MRN00000002",
    "name": { "given_name": "Maria", "family_name": "Garcia" },
    "birth_date": "1967-08-22",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "E11.65", "description": "Type 2 diabetes with hyperglycemia" },
    { "code": "I10", "description": "Essential hypertension" },
    { "code": "E78.5", "description": "Hyperlipidemia" }
  ],
  "medications": [
    { "name": "Metformin", "dose": "1000 mg", "frequency": "BID" },
    { "name": "Glipizide", "dose": "10 mg", "frequency": "BID" },
    { "name": "Lisinopril", "dose": "20 mg", "frequency": "QD" }
  ],
  "labs": [
    { "test": "HbA1c", "value": "9.8", "unit": "%", "flag": "H" },
    { "test": "Glucose", "value": "245", "unit": "mg/dL", "flag": "H" },
    { "test": "Creatinine", "value": "1.2", "unit": "mg/dL" }
  ]
}
```

### Example 3: Professional Claim

**Request:** "Generate a paid professional claim for an office visit"

**Output:**
```json
{
  "claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "provider_npi": "1234567890",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "E11.9",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "charge_amount": 175.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 125.00,
    "paid_amount": 100.00,
    "deductible": 0.00,
    "copay": 25.00,
    "coinsurance": 0.00
  }
}
```

### Example 4: Pharmacy Claim with DUR

**Request:** "Generate a pharmacy claim that gets rejected for early refill"

**Output:**
```json
{
  "claim": {
    "claim_id": "RX20250115000001",
    "transaction_code": "B1",
    "ndc": "00071015523",
    "drug_name": "Atorvastatin 20mg",
    "quantity": 30,
    "days_supply": 30,
    "service_date": "2025-01-15"
  },
  "response": {
    "status": "rejected",
    "reject_code": "79",
    "reject_message": "Refill Too Soon",
    "dur_alert": {
      "type": "ER",
      "message": "Refill 12 days early (before 80% used)",
      "previous_fill_date": "2024-12-27",
      "days_early": 12
    }
  }
}
```

## Tips

1. **Be specific**: "diabetic patient with A1C of 9.5" beats "sick patient"
2. **Request format early**: "Generate as FHIR..." rather than converting after
3. **Use seeds**: For reproducible test data across sessions
4. **Batch large requests**: "Generate 100 in batches of 20"
5. **Validate sensitive data**: Request validation for production-like cohorts
