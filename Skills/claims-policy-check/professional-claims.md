---
name: professional-claims
description: "Professional (CMS-1500/837P) claims for physician and outpatient services. Triggers: professional claim, 837P, CMS-1500, physician billing, office visit claims, E&M codes, outpatient procedures, claim adjudication"
---

# Professional Claims Cohort

A cohort template for generating professional (CMS-1500/837P) claims for physician and outpatient services, including E&M visits, procedures, and diagnostics.

## For Claude

Use this skill when the user requests professional claims or physician billing cohorts. This teaches you how to generate **realistic professional claims** with appropriate E&M coding, procedure modifiers, and adjudication patterns.

**When to apply this skill:**

- User mentions professional claim, 837P, or CMS-1500
- User requests physician billing or office visit claims
- User specifies E&M codes or outpatient procedures
- User asks for claim adjudication cohorts
- User needs provider billing examples

**Key capabilities this skill provides:**

- How to select appropriate E&M codes based on visit complexity
- How to apply modifiers correctly (25, 59, LT/RT, etc.)
- How to structure claim lines with diagnosis pointers
- How to model adjudication with CARC codes
- How to handle network vs out-of-network cohorts

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: MemberSim
- **Tags**: claims, professional, billing, payer, 837P
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic professional claims for physician services. It models the complete claim lifecycle from service to adjudication, including E&M code selection, procedure coding, modifier usage, and payment calculation.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "professional claim", "837P", "CMS-1500"
- "physician claim", "office visit claim"
- "E&M claim", "outpatient claim"
- "provider claim", "billing"

**Claim Cohorts**:

- "Generate a professional claim for an office visit"
- "Create a claim with E&M and procedure"
- "Generate a denied claim example"

## Trigger Phrases

- professional claim
- 837P
- physician claim
- office visit claim
- E&M claim
- CMS-1500
- provider claim
- outpatient claim

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| visit_type | string | established | new, established |
| complexity | string | moderate | minimal, straightforward, low, moderate, high |
| place_of_service | string | 11 | See POS codes below |
| network_status | string | in-network | in-network, out-of-network |
| claim_status | string | paid | paid, denied, pending, partial |
| specialty | string | primary_care | primary_care, cardiology, orthopedics, etc. |

## Place of Service Codes

| Code | Description | Typical CPT |
|------|-------------|-------------|
| 11 | Office | 99211-99215 |
| 12 | Home | 99341-99350 |
| 21 | Inpatient Hospital | 99221-99223 |
| 22 | Outpatient Hospital | 99201-99215 |
| 23 | Emergency Room | 99281-99285 |
| 24 | Ambulatory Surgical Center | Surgical CPT |
| 31 | Skilled Nursing Facility | 99304-99318 |
| 81 | Independent Laboratory | 80000-89999 |

## E&M Code Selection

### Office/Outpatient Visits (99202-99215)

#### New Patient (99202-99205)
| Code | MDM Level | Typical Time | Charge Range |
|------|-----------|--------------|--------------|
| 99202 | Straightforward | 15-29 min | $75-125 |
| 99203 | Low | 30-44 min | $125-175 |
| 99204 | Moderate | 45-59 min | $175-250 |
| 99205 | High | 60-74 min | $250-350 |

#### Established Patient (99211-99215)
| Code | MDM Level | Typical Time | Charge Range |
|------|-----------|--------------|--------------|
| 99211 | Minimal | 5-10 min | $25-50 |
| 99212 | Straightforward | 10-19 min | $50-85 |
| 99213 | Low | 20-29 min | $85-125 |
| 99214 | Moderate | 30-39 min | $125-175 |
| 99215 | High | 40-54 min | $175-250 |

### Emergency Department (99281-99285)
| Code | Severity | Charge Range |
|------|----------|--------------|
| 99281 | Self-limited | $75-150 |
| 99282 | Low | $150-250 |
| 99283 | Moderate | $250-400 |
| 99284 | High | $400-600 |
| 99285 | High + threat to life | $600-900 |

## Common Procedure Codes by Specialty

### Primary Care
```json
{
  "office_visits": ["99212", "99213", "99214", "99215"],
  "preventive": ["99385", "99386", "99395", "99396"],
  "procedures": ["36415", "81002", "87880", "96372"],
  "vaccines": ["90471", "90472", "90658", "90715"]
}
```

### Cardiology
```json
{
  "office_visits": ["99213", "99214", "99215"],
  "diagnostics": ["93000", "93306", "93307", "93880"],
  "stress_tests": ["93015", "93016", "93017", "93018"],
  "monitoring": ["93224", "93225", "93226", "93227"]
}
```

### Orthopedics
```json
{
  "office_visits": ["99213", "99214", "99215"],
  "injections": ["20610", "20605", "20600"],
  "imaging": ["73721", "73722", "73630"],
  "casts": ["29075", "29085", "29105"]
}
```

## Claim Structure

### Claim Header
```json
{
  "claim_id": "CLM{YYYYMMDD}{sequence:06d}",
  "claim_type": "PROFESSIONAL",
  "member_id": "string",
  "subscriber_id": "string",
  "provider_npi": "10-digit NPI",
  "provider_taxonomy": "taxonomy code",
  "facility_npi": "optional, for facility billing",
  "service_date": "YYYY-MM-DD",
  "place_of_service": "2-digit POS code",
  "principal_diagnosis": "ICD-10 code",
  "other_diagnoses": ["array of ICD-10 codes"],
  "referring_provider_npi": "optional"
}
```

### Claim Line
```json
{
  "line_number": 1,
  "procedure_code": "5-digit CPT/HCPCS",
  "procedure_modifiers": ["25", "59", etc.],
  "service_date": "YYYY-MM-DD",
  "units": 1,
  "charge_amount": 175.00,
  "diagnosis_pointers": [1, 2],
  "place_of_service": "11",
  "rendering_provider_npi": "optional if different from billing"
}
```

## Common Modifiers

| Modifier | Description | Use Case |
|----------|-------------|----------|
| 25 | Significant, separately identifiable E&M | E&M + procedure same day |
| 59 | Distinct procedural service | Unbundling |
| 76 | Repeat procedure by same physician | Multiple of same procedure |
| 77 | Repeat procedure by another physician | Different provider |
| LT | Left side | Bilateral procedures |
| RT | Right side | Bilateral procedures |
| TC | Technical component | Radiology |
| 26 | Professional component | Radiology |

## Fee Schedule and Allowed Amounts

### Medicare-Based Calculation
```json
{
  "methodology": "RBRVS",
  "formula": "(Work RVU * Work GPCI + PE RVU * PE GPCI + MP RVU * MP GPCI) * Conversion Factor",
  "conversion_factor_2025": 32.74,
  "example_99214": {
    "work_rvu": 1.50,
    "pe_rvu": 1.87,
    "mp_rvu": 0.11,
    "total_rvu": 3.48,
    "allowed_medicare": 113.93
  }
}
```

### Commercial Payer Typical
```json
{
  "methodology": "Percent of Medicare",
  "typical_range": "110% - 150% of Medicare",
  "example_99214": {
    "medicare_allowed": 113.93,
    "commercial_allowed": "125.32 - 170.90"
  }
}
```

## Adjudication Patterns

### Paid Claim
```json
{
  "adjudication": {
    "status": "paid",
    "allowed_amount": 125.00,
    "deductible": 0.00,
    "copay": 25.00,
    "coinsurance": 0.00,
    "paid_amount": 100.00,
    "patient_responsibility": 25.00,
    "adjustment_codes": [
      { "code": "CO-45", "amount": 50.00, "description": "Charge exceeds fee schedule" }
    ]
  }
}
```

### Denied Claim
```json
{
  "adjudication": {
    "status": "denied",
    "allowed_amount": 0.00,
    "paid_amount": 0.00,
    "denial_reason_code": "CO-4",
    "denial_message": "Procedure code inconsistent with modifier",
    "patient_responsibility": 0.00
  }
}
```

### Pending/Pended Claim
```json
{
  "adjudication": {
    "status": "pending",
    "pend_reason": "Medical records requested",
    "pend_code": "W1",
    "expected_resolution_date": "2025-02-15"
  }
}
```

## Common Denial Cohorts

| Cohort | CARC | Description | Resolution |
|----------|------|-------------|------------|
| Duplicate claim | CO-18 | Duplicate submission | Verify original payment |
| Auth required | CO-15 | Prior authorization required | Submit authorization |
| Non-covered | CO-50 | Non-covered services | Member appeal or pay |
| Timely filing | CO-29 | Claim filed too late | Appeal with proof |
| Invalid diagnosis | CO-11 | Diagnosis inconsistent | Correct and resubmit |
| Bundling | CO-97 | Included in another service | Review coding |

## Examples

### Example 1: Standard Office Visit (Paid)

```json
{
  "member": {
    "member_id": "MEM001234",
    "name": { "given_name": "Michael", "family_name": "Chen" },
    "birth_date": "1982-03-22",
    "gender": "M",
    "plan_code": "PPO-STANDARD",
    "group_id": "GRP00100"
  },
  "provider": {
    "npi": "1234567890",
    "name": "Springfield Medical Associates",
    "taxonomy": "207Q00000X",
    "address": {
      "city": "Springfield",
      "state": "IL",
      "postal_code": "62701"
    }
  },
  "claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "provider_npi": "1234567890",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "I10",
    "other_diagnoses": ["E78.5", "E66.9"],
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "charge_amount": 175.00,
        "units": 1,
        "diagnosis_pointers": [1, 2, 3]
      }
    ],
    "total_charges": 175.00
  },
  "adjudication": {
    "status": "paid",
    "adjudication_date": "2025-01-20",
    "allowed_amount": 128.50,
    "deductible": 0.00,
    "copay": 30.00,
    "coinsurance": 0.00,
    "paid_amount": 98.50,
    "patient_responsibility": 30.00,
    "check_number": "CHK20250120001234",
    "adjustment_codes": [
      { "group": "CO", "code": "45", "amount": 46.50 }
    ]
  }
}
```

### Example 2: E&M with Procedure (Modifier 25)

```json
{
  "claim": {
    "claim_id": "CLM20250115000002",
    "claim_type": "PROFESSIONAL",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "L03.115",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "procedure_modifiers": ["25"],
        "charge_amount": 175.00,
        "units": 1,
        "diagnosis_pointers": [1]
      },
      {
        "line_number": 2,
        "procedure_code": "10060",
        "charge_amount": 250.00,
        "units": 1,
        "diagnosis_pointers": [1]
      }
    ],
    "total_charges": 425.00
  },
  "adjudication": {
    "status": "paid",
    "line_adjudications": [
      { "line": 1, "allowed": 128.50, "paid": 98.50, "copay": 30.00 },
      { "line": 2, "allowed": 185.00, "paid": 148.00, "coinsurance": 37.00 }
    ],
    "total_allowed": 313.50,
    "total_paid": 246.50,
    "total_patient_responsibility": 67.00
  }
}
```

### Example 3: Out-of-Network Claim

```json
{
  "claim": {
    "claim_id": "CLM20250115000003",
    "claim_type": "PROFESSIONAL",
    "network_status": "out-of-network",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "M54.5",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "charge_amount": 225.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "network_status": "out-of-network",
    "allowed_amount": 100.00,
    "deductible": 50.00,
    "coinsurance": 20.00,
    "paid_amount": 30.00,
    "patient_responsibility": 195.00,
    "balance_billing": 125.00,
    "notes": "OON allowed = 80% of Medicare. Member responsible for balance."
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Claim ID | Unique identifier | CLM-2025-001234 |
| Service date | Valid date, not future | 2025-01-15 |
| CPT code | Valid 5-digit CPT | 99214 (office visit) |
| ICD-10 code | Valid diagnosis code | E11.9 (Type 2 DM) |
| Place of service | 2-digit POS code | 11 (office), 22 (outpatient) |
| Provider NPI | 10-digit valid NPI | 1234567890 |
| Billed amount | Positive amount | $150.00 |
| Units | Positive integer | 1 |
| Modifier | Valid CPT modifier | 25 (significant E&M) |

### Business Rules

- **E&M Level Selection**: Match complexity to documentation (99211-99215)
- **Modifier 25**: Required for E&M with same-day procedure
- **Place of Service**: Must match claim type (11=office, 22=outpatient hospital)
- **Diagnosis Pointer**: Each CPT must link to supporting diagnosis
- **Prior Authorization**: Some services require PA number on claim
- **Timely Filing**: Claims must be filed within payer deadline (typically 90-365 days)
- **NPI Validation**: Rendering and billing NPI must be active and enrolled
- **Duplicate Check**: Same provider/patient/date/CPT rejected as duplicate

## Related Skills

### MemberSim
- [SKILL.md](SKILL.md) - MemberSim overview
- [facility-claims.md](facility-claims.md) - Institutional claims
- [prior-authorization.md](prior-authorization.md) - PA requirements
- [accumulator-tracking.md](accumulator-tracking.md) - Cost sharing

### Cross-Product: PatientSim
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Diabetes office visits (99213/99214)
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - Cardiology visits
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - Psychiatry/therapy visits

> **Integration Pattern:** Use PatientSim to generate clinical encounters. Use MemberSim to generate corresponding professional claims with matching dates, diagnosis codes, and appropriate E&M levels.

### Cross-Product: RxMemberSim
- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Prescriptions from office visits

> **Integration Pattern:** Office visits often result in new prescriptions. Correlate visit dates with prescription written dates in RxMemberSim.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - CPT, ICD-10 codes
- [../../formats/x12-837.md](../../formats/x12-837.md) - 837P format
