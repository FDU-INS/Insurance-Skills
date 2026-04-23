---
name: facility-claims
description: "Institutional (UB-04/837I) claims for hospital inpatient, outpatient, and observation services. Triggers: facility claim, 837I, UB-04, hospital claims, inpatient, DRG, revenue codes, institutional, hospital billing"
---

# Facility Claims Cohort

A cohort template for generating institutional (UB-04/837I) claims for hospital inpatient, outpatient, and observation services.

## For Claude

Use this skill when the user requests facility/institutional claims or hospital billing cohorts. This teaches you how to generate **realistic facility claims** with DRG assignment, revenue codes, and institutional adjudication patterns.

**When to apply this skill:**

- User mentions facility claim, 837I, or UB-04
- User requests hospital or inpatient claims
- User specifies DRG, revenue codes, or room and board
- User asks for institutional claim cohorts
- User needs hospital billing examples

**Key capabilities this skill provides:**

- How to assign appropriate DRGs based on diagnoses and procedures
- How to structure revenue code lines for different services
- How to calculate length of stay and per-diem rates
- How to model inpatient vs outpatient adjudication
- How to handle admission types and discharge statuses

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: MemberSim
- **Tags**: claims, facility, institutional, billing, payer, 837I
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic facility claims for hospital services. It models DRG-based inpatient payments, outpatient APC reimbursement, observation stays, and the complete institutional claim lifecycle.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "facility claim", "837I", "UB-04"
- "inpatient claim", "hospital claim"
- "DRG", "revenue code", "room and board"
- "institutional claim"

**Claim Cohorts**:

- "Generate an inpatient claim for a hip replacement"
- "Create an outpatient facility claim"
- "Generate a hospital claim with DRG"

## Trigger Phrases

- facility claim
- institutional claim
- 837I
- inpatient claim
- hospital claim
- UB-04
- DRG
- revenue code
- room and board

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| claim_type | string | inpatient | inpatient, outpatient, observation |
| drg_category | string | medical | medical, surgical, psychiatric |
| length_of_stay | int | varies | Days based on DRG |
| network_status | string | in-network | in-network, out-of-network |
| claim_status | string | paid | paid, denied, pending |
| admission_type | string | elective | emergency, urgent, elective |

## Facility Claim Types

### Inpatient (Type of Bill 11x)
- Admission required for treatment
- Paid by DRG (MS-DRG for Medicare, often for commercial)
- Full room and board charges
- Expected LOS varies by DRG

### Outpatient (Type of Bill 13x)
- Same-day service, no overnight stay
- Paid by APC (Ambulatory Payment Classification) or fee schedule
- Common for ED visits, procedures, observation < 24 hours

### Observation (Type of Bill 13x with status indicator)
- Extended monitoring (typically 24-48 hours)
- Not classified as inpatient admission
- Paid as outpatient

## Type of Bill Codes

| Code | Description |
|------|-------------|
| 111 | Inpatient - Admit through discharge |
| 112 | Inpatient - Interim first claim |
| 113 | Inpatient - Interim continuing claim |
| 114 | Inpatient - Interim last claim |
| 131 | Outpatient - Hospital |
| 141 | Outpatient - Other (ASC) |
| 721 | Inpatient - Clinic |
| 831 | Ambulatory Surgery Center |

## Revenue Codes

### Room and Board
| Code | Description | Typical Daily Rate |
|------|-------------|-------------------|
| 0100 | All-inclusive room and board | $800-1500 |
| 0110 | Room and board - private | $1200-2500 |
| 0120 | Room and board - semi-private | $800-1800 |
| 0150 | Room and board - ICU | $3000-8000 |
| 0160 | Room and board - CCU | $3000-7000 |
| 0170 | Room and board - nursery | $1000-2000 |

### Ancillary Services
| Code | Description |
|------|-------------|
| 0250 | Pharmacy - general |
| 0258 | Pharmacy - IV solutions |
| 0260 | IV therapy |
| 0270 | Medical/surgical supplies |
| 0300 | Laboratory - general |
| 0320 | Radiology - diagnostic |
| 0350 | CT scan |
| 0360 | Operating room |
| 0370 | Anesthesia |
| 0410 | Respiratory services |
| 0420 | Physical therapy |
| 0450 | Emergency room |
| 0636 | Drugs requiring detailed coding |

## MS-DRG Assignment

### Common Medical DRGs
| DRG | Description | Weight | Mean LOS |
|-----|-------------|--------|----------|
| 291 | Heart failure with MCC | 1.2851 | 5.3 |
| 292 | Heart failure with CC | 0.9289 | 4.1 |
| 293 | Heart failure without CC/MCC | 0.6904 | 3.0 |
| 871 | Sepsis without MV >96 hrs with MCC | 1.8739 | 6.8 |
| 872 | Sepsis without MV >96 hrs with CC | 1.2281 | 5.0 |
| 189 | Pneumonia with MCC | 1.2987 | 5.2 |
| 190 | Pneumonia with CC | 0.8882 | 4.0 |
| 191 | Pneumonia without CC/MCC | 0.6912 | 3.0 |
| 683 | Renal failure with CC | 0.9541 | 4.2 |
| 682 | Renal failure with MCC | 1.4512 | 5.8 |

### Common Surgical DRGs
| DRG | Description | Weight | Mean LOS |
|-----|-------------|--------|----------|
| 470 | Major hip/knee joint replacement | 1.9079 | 2.4 |
| 473 | Cervical spinal fusion without CC/MCC | 2.8116 | 1.9 |
| 460 | Spinal fusion except cervical with MCC | 6.8455 | 7.8 |
| 329 | Major small/large bowel procedure with MCC | 3.5961 | 10.2 |
| 216 | Cardiac valve procedure with CC | 4.5612 | 8.5 |

## Claim Structure

### Facility Claim Header
```json
{
  "claim_id": "CLM{YYYYMMDD}{sequence:06d}",
  "claim_type": "INSTITUTIONAL",
  "type_of_bill": "111",
  "member_id": "string",
  "facility_npi": "10-digit NPI",
  "facility_name": "string",
  "admission_date": "YYYY-MM-DD",
  "admission_hour": "HH",
  "admission_type": "1=Emergency, 2=Urgent, 3=Elective",
  "admission_source": "1=Physician referral, 2=Clinic, 7=ED",
  "discharge_date": "YYYY-MM-DD",
  "discharge_hour": "HH",
  "discharge_status": "01-87",
  "principal_diagnosis": "ICD-10 code",
  "admitting_diagnosis": "ICD-10 code",
  "other_diagnoses": ["array of ICD-10 codes"],
  "principal_procedure": "ICD-10-PCS code",
  "other_procedures": ["array of procedure codes"],
  "drg_code": "3-digit DRG",
  "attending_npi": "10-digit NPI",
  "operating_npi": "optional"
}
```

### Discharge Status Codes
| Code | Description |
|------|-------------|
| 01 | Discharged to home or self-care |
| 02 | Discharged to short-term hospital |
| 03 | Discharged to SNF |
| 04 | Discharged to intermediate care facility |
| 05 | Discharged to other type of institution |
| 06 | Discharged to home under care of home health |
| 07 | Left against medical advice |
| 20 | Expired |
| 30 | Still a patient |
| 62 | Discharged to inpatient rehab facility |
| 63 | Discharged to long-term care hospital |

### Revenue Code Line
```json
{
  "line_number": 1,
  "revenue_code": "0120",
  "description": "Room and board - semi-private",
  "hcpcs_code": "optional CPT/HCPCS",
  "service_date": "YYYY-MM-DD",
  "units": 5,
  "charge_amount": 8500.00
}
```

## DRG Payment Calculation

### MS-DRG Payment Formula
```
Base Payment = (Labor Share × Wage Index + Non-Labor Share) × DRG Weight × Base Rate

Adjustments:
+ IME (Indirect Medical Education) if teaching hospital
+ DSH (Disproportionate Share) if qualifying hospital
+ Outlier payment if costs exceed threshold
```

### Commercial DRG Payment
```json
{
  "methodology": "case_rate",
  "options": [
    {
      "type": "percent_of_charges",
      "rate": 0.45,
      "example": "45% of total charges"
    },
    {
      "type": "percent_of_medicare",
      "rate": 1.50,
      "example": "150% of Medicare DRG payment"
    },
    {
      "type": "per_diem",
      "med_surg_rate": 1500,
      "icu_rate": 3500,
      "example": "Per diem with carve-outs"
    }
  ]
}
```

## Adjudication Patterns

### Inpatient Paid by DRG
```json
{
  "adjudication": {
    "status": "paid",
    "payment_method": "DRG",
    "drg_code": "291",
    "drg_weight": 1.2851,
    "base_rate": 7500.00,
    "drg_payment": 9638.25,
    "total_charges": 45000.00,
    "allowed_amount": 9638.25,
    "deductible": 500.00,
    "coinsurance": 1827.65,
    "paid_amount": 7310.60,
    "patient_responsibility": 2327.65
  }
}
```

### Outpatient Paid by APC
```json
{
  "adjudication": {
    "status": "paid",
    "payment_method": "APC",
    "apc_assignments": [
      { "apc": "5072", "description": "Level 2 Imaging", "payment": 245.50 },
      { "apc": "5114", "description": "Level 4 Minor Procedures", "payment": 520.00 }
    ],
    "total_apc_payment": 765.50,
    "allowed_amount": 765.50,
    "copay": 150.00,
    "paid_amount": 615.50
  }
}
```

## Examples

### Example 1: Heart Failure Admission (DRG 291)

```json
{
  "member": {
    "member_id": "MEM005678",
    "name": { "given_name": "Eleanor", "family_name": "Thompson" },
    "birth_date": "1950-08-12",
    "gender": "F",
    "plan_code": "PPO-GOLD"
  },
  "facility": {
    "npi": "1122334455",
    "name": "Springfield General Hospital",
    "address": { "city": "Springfield", "state": "IL" }
  },
  "claim": {
    "claim_id": "CLM20250115000010",
    "claim_type": "INSTITUTIONAL",
    "type_of_bill": "111",
    "member_id": "MEM005678",
    "facility_npi": "1122334455",
    "admission_date": "2025-01-10",
    "admission_type": "1",
    "admission_source": "7",
    "discharge_date": "2025-01-15",
    "discharge_status": "01",
    "length_of_stay": 5,
    "principal_diagnosis": "I50.23",
    "admitting_diagnosis": "R06.00",
    "other_diagnoses": ["I10", "E11.9", "N18.3", "I48.91"],
    "drg_code": "291",
    "attending_npi": "9876543210",
    "claim_lines": [
      { "revenue_code": "0120", "description": "Room - Semi-private", "units": 4, "charge": 7200.00 },
      { "revenue_code": "0150", "description": "Room - ICU", "units": 1, "charge": 4500.00 },
      { "revenue_code": "0250", "description": "Pharmacy", "units": 1, "charge": 3200.00 },
      { "revenue_code": "0300", "description": "Laboratory", "units": 1, "charge": 2800.00 },
      { "revenue_code": "0320", "description": "Radiology", "units": 1, "charge": 1500.00 },
      { "revenue_code": "0410", "description": "Respiratory", "units": 1, "charge": 1200.00 },
      { "revenue_code": "0730", "description": "EKG/ECG", "units": 1, "charge": 450.00 }
    ],
    "total_charges": 20850.00
  },
  "adjudication": {
    "status": "paid",
    "adjudication_date": "2025-01-25",
    "payment_method": "DRG",
    "drg_code": "291",
    "drg_description": "Heart failure with MCC",
    "drg_weight": 1.2851,
    "base_rate": 8500.00,
    "drg_payment": 10923.35,
    "allowed_amount": 10923.35,
    "deductible": 500.00,
    "coinsurance": 2084.67,
    "paid_amount": 8338.68,
    "patient_responsibility": 2584.67,
    "adjustment_codes": [
      { "group": "CO", "code": "45", "amount": 9926.65 }
    ]
  }
}
```

### Example 2: Outpatient Surgery (APC)

```json
{
  "claim": {
    "claim_id": "CLM20250115000011",
    "claim_type": "INSTITUTIONAL",
    "type_of_bill": "131",
    "admission_date": "2025-01-15",
    "discharge_date": "2025-01-15",
    "principal_diagnosis": "K80.20",
    "principal_procedure": "0FT44ZZ",
    "claim_lines": [
      { "revenue_code": "0360", "hcpcs": "47562", "description": "OR services - Lap chole", "charge": 8500.00 },
      { "revenue_code": "0370", "hcpcs": "00790", "description": "Anesthesia", "charge": 2200.00 },
      { "revenue_code": "0270", "description": "Supplies", "charge": 1500.00 },
      { "revenue_code": "0250", "description": "Pharmacy", "charge": 450.00 },
      { "revenue_code": "0710", "description": "Recovery room", "charge": 800.00 }
    ],
    "total_charges": 13450.00
  },
  "adjudication": {
    "status": "paid",
    "payment_method": "APC",
    "primary_apc": "5341",
    "apc_description": "Laparoscopic cholecystectomy",
    "apc_payment": 4850.00,
    "allowed_amount": 4850.00,
    "copay": 250.00,
    "paid_amount": 4600.00
  }
}
```

### Example 3: Emergency Department (Outpatient)

```json
{
  "claim": {
    "claim_id": "CLM20250115000012",
    "claim_type": "INSTITUTIONAL",
    "type_of_bill": "131",
    "admission_date": "2025-01-15",
    "discharge_date": "2025-01-15",
    "principal_diagnosis": "R07.9",
    "claim_lines": [
      { "revenue_code": "0450", "hcpcs": "99284", "description": "ED visit - Level 4", "charge": 1200.00 },
      { "revenue_code": "0300", "description": "Laboratory", "charge": 450.00 },
      { "revenue_code": "0320", "hcpcs": "71046", "description": "Chest X-ray", "charge": 350.00 },
      { "revenue_code": "0730", "hcpcs": "93000", "description": "EKG", "charge": 250.00 }
    ],
    "total_charges": 2250.00
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 985.00,
    "copay": 150.00,
    "paid_amount": 835.00
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Claim ID | Unique identifier | FAC-2025-001234 |
| Admission date | Valid date, not future | 2025-01-10 |
| Discharge date | On or after admission | 2025-01-14 |
| Revenue code | Valid 4-digit code | 0120 (room & board) |
| DRG | Valid MS-DRG | 470 (joint replacement) |
| Type of bill | 3-digit TOB code | 111 (inpatient admit) |
| Principal diagnosis | Valid ICD-10 | I50.9 (heart failure) |
| Facility NPI | 10-digit valid NPI | 1234567890 |
| Total charges | Positive amount | $45,000.00 |

### Business Rules

- **DRG Assignment**: Based on principal diagnosis, procedures, complications, age
- **Type of Bill**: First digit = facility type, second = bill classification, third = frequency
- **Revenue Codes**: Required for each service line; maps to department/service
- **Admission Type**: 1=Emergency, 2=Urgent, 3=Elective, 4=Newborn
- **Discharge Status**: 01=home, 02=SNF, 20=expired, 30=still patient
- **Length of Stay**: Discharge date - Admission date; affects DRG payment
- **Present on Admission**: POA indicators required for each diagnosis
- **Outlier Payments**: Extra-long stays or high-cost cases may receive outlier payment

## Related Skills

### MemberSim
- [SKILL.md](SKILL.md) - MemberSim overview
- [professional-claims.md](professional-claims.md) - Physician claims (often accompany facility)
- [prior-authorization.md](prior-authorization.md) - Inpatient PA

### Cross-Product: PatientSim
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - HF admissions (DRG 291-293)
- [../patientsim/ed-chest-pain.md](../patientsim/ed-chest-pain.md) - ED facility claims
- [../patientsim/sepsis-acute-care.md](../patientsim/sepsis-acute-care.md) - Sepsis DRG (870-872)
- [../patientsim/elective-joint.md](../patientsim/elective-joint.md) - Joint replacement DRG (469-470)
- [../patientsim/maternal-health.md](../patientsim/maternal-health.md) - Delivery DRG (765-768)
- [../patientsim/oncology/README.md](../patientsim/oncology/README.md) - Oncology infusion claims

> **Integration Pattern:** Use PatientSim to generate inpatient stays or ED visits. Use MemberSim facility-claims to generate corresponding 837I claims with matching admission/discharge dates, diagnosis codes, and appropriate DRG assignment.

### Cross-Product: RxMemberSim
- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Discharge prescription fills

> **Integration Pattern:** Inpatient stays result in discharge medications. Generate pharmacy claims in RxMemberSim 0-3 days after PatientSim discharge date.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - Revenue codes, DRGs
- [../../formats/x12-837.md](../../formats/x12-837.md) - 837I format
