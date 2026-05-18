# Testing Patterns for HealthSim Skills

## Overview

This guide provides testing patterns to verify that generated healthcare data is correct, consistent, and realistic. Use these patterns to validate skill outputs before use in downstream systems.

## Testing Categories

1. **Structural Tests** - Verify data formats and required fields
2. **Semantic Tests** - Verify data meanings and relationships
3. **Integration Tests** - Verify cross-skill consistency
4. **Realistic Data Tests** - Verify clinical/business realism

## Structural Test Patterns

### Pattern 1: Required Field Presence

Verify all required fields are present and non-empty.

**Test Template:**
```json
{
  "test_name": "required_fields_patient",
  "entity": "Patient",
  "required_fields": [
    "mrn",
    "name.given_name",
    "name.family_name",
    "birth_date",
    "gender"
  ],
  "assertion": "all fields present and non-null"
}
```

**Example Test Cases:**
```json
{
  "tests": [
    {
      "name": "patient_has_mrn",
      "input": { "mrn": "PAT001234" },
      "expected": "pass",
      "actual": "pass"
    },
    {
      "name": "patient_missing_mrn",
      "input": { "mrn": null },
      "expected": "fail",
      "actual": "fail",
      "error": "Required field 'mrn' is missing"
    }
  ]
}
```

### Pattern 2: Format Validation

Verify field values match expected formats.

**Test Template:**
```json
{
  "test_name": "format_validation",
  "tests": [
    {
      "field": "npi",
      "pattern": "^[0-9]{10}$",
      "valid_examples": ["1234567893"],
      "invalid_examples": ["123456789", "12345678901", "ABC1234567"]
    },
    {
      "field": "icd10_code",
      "pattern": "^[A-Z][0-9]{2}(\\.[A-Z0-9]{1,4})?$",
      "valid_examples": ["E11.9", "I10", "Z23"],
      "invalid_examples": ["250.00", "E11", "11.9"]
    },
    {
      "field": "ndc",
      "pattern": "^[0-9]{11}$",
      "valid_examples": ["00093505601"],
      "invalid_examples": ["0093505601", "00093-5056-01"]
    }
  ]
}
```

### Pattern 3: Enumeration Validation

Verify coded values are from allowed value sets.

**Test Template:**
```json
{
  "test_name": "enum_validation",
  "tests": [
    {
      "field": "gender",
      "allowed_values": ["M", "F", "O", "U"],
      "test_values": [
        { "value": "M", "expected": "pass" },
        { "value": "male", "expected": "fail" },
        { "value": "X", "expected": "fail" }
      ]
    },
    {
      "field": "encounter_class",
      "allowed_values": ["I", "O", "E", "U", "OBS"],
      "test_values": [
        { "value": "I", "expected": "pass" },
        { "value": "inpatient", "expected": "fail" }
      ]
    }
  ]
}
```

## Semantic Test Patterns

### Pattern 4: Date Ordering

Verify dates follow logical sequences.

**Test Template:**
```json
{
  "test_name": "date_ordering",
  "rules": [
    {
      "name": "birth_before_encounter",
      "condition": "patient.birth_date < encounter.period_start",
      "error": "Encounter cannot occur before birth"
    },
    {
      "name": "admission_before_discharge",
      "condition": "encounter.period_start <= encounter.period_end",
      "error": "Discharge cannot precede admission"
    },
    {
      "name": "prescription_before_fill",
      "condition": "prescription.written_date <= claim.fill_date",
      "error": "Fill cannot precede prescription"
    }
  ]
}
```

**Example Test:**
```json
{
  "test_name": "inpatient_encounter_dates",
  "input": {
    "patient": { "birth_date": "1970-05-15" },
    "encounter": {
      "period_start": "2025-01-10",
      "period_end": "2025-01-15"
    }
  },
  "checks": [
    { "rule": "birth_before_encounter", "result": "pass" },
    { "rule": "admission_before_discharge", "result": "pass" }
  ]
}
```

### Pattern 5: Clinical Coherence

Verify clinical relationships make sense.

**Test Template:**
```json
{
  "test_name": "diagnosis_medication_coherence",
  "medication_indication_rules": [
    {
      "medication_class": "metformin",
      "required_diagnoses": ["E08", "E09", "E10", "E11", "E13"],
      "error": "Metformin requires diabetes diagnosis"
    },
    {
      "medication_class": "ace_inhibitor",
      "required_diagnoses": ["I10", "I50", "I25", "N18"],
      "error": "ACE inhibitor requires HTN, CHF, CAD, or CKD diagnosis"
    }
  ]
}
```

**Example Test:**
```json
{
  "test_name": "medication_has_indication",
  "input": {
    "medications": [
      { "name": "Lisinopril", "ndc": "00093505601" }
    ],
    "diagnoses": ["E11.9", "I10"]
  },
  "check": "Lisinopril has indication (I10 - hypertension)",
  "result": "pass"
}
```

### Pattern 6: Age-Gender Appropriateness

Verify conditions and procedures are appropriate for demographics.

**Test Template:**
```json
{
  "test_name": "demographic_appropriateness",
  "rules": [
    {
      "condition_prefix": "O",
      "description": "Pregnancy codes",
      "required_gender": ["F"],
      "age_range": [10, 55]
    },
    {
      "condition_prefix": "N40",
      "description": "Prostate conditions",
      "required_gender": ["M"],
      "age_range": [40, 120]
    },
    {
      "condition_prefix": "P",
      "description": "Perinatal codes",
      "age_range": [0, 0.08]
    }
  ]
}
```

## Integration Test Patterns

### Pattern 7: Cross-Entity Identifier Consistency

Verify identifiers match across related entities.

**Test Template:**
```json
{
  "test_name": "identifier_consistency",
  "linked_entities": [
    {
      "source": "patient.mrn",
      "target": "encounter.patient_id",
      "rule": "must_match"
    },
    {
      "source": "encounter.provider_npi",
      "target": "claim.rendering_provider_npi",
      "rule": "must_match"
    },
    {
      "source": "prescription.id",
      "target": "pharmacy_claim.prescription_reference",
      "rule": "must_match"
    }
  ]
}
```

**Example Test:**
```json
{
  "test_name": "patient_encounter_claim_linked",
  "input": {
    "patient": { "mrn": "PAT001234" },
    "encounter": {
      "id": "ENC001",
      "patient_id": "PAT001234"
    },
    "claim": {
      "id": "CLM20250115001",
      "member_id": "MEM001234",
      "encounter_reference": "ENC001"
    }
  },
  "checks": [
    { "rule": "encounter links to patient", "result": "pass" },
    { "rule": "claim links to encounter", "result": "pass" }
  ]
}
```

### Pattern 8: Diagnosis Consistency Across Domains

Verify diagnoses flow correctly from clinical to claims.

**Test Template:**
```json
{
  "test_name": "diagnosis_flow",
  "flow": "encounter → claim",
  "checks": [
    {
      "name": "principal_diagnosis_matches",
      "condition": "claim.principal_diagnosis IN encounter.diagnoses"
    },
    {
      "name": "all_claim_diagnoses_from_encounter",
      "condition": "ALL claim.diagnoses IN encounter.diagnoses"
    }
  ]
}
```

### Pattern 9: Cost Sharing Calculations

Verify claim adjudication math is correct.

**Test Template:**
```json
{
  "test_name": "cost_sharing_math",
  "input": {
    "charge_amount": 500.00,
    "allowed_amount": 400.00,
    "deductible_remaining": 100.00,
    "copay": 25.00,
    "coinsurance_rate": 0.20
  },
  "expected_calculations": {
    "contractual_adjustment": 100.00,
    "deductible_applied": 100.00,
    "after_deductible": 300.00,
    "copay_applied": 25.00,
    "coinsurance_base": 275.00,
    "coinsurance_amount": 55.00,
    "patient_responsibility": 180.00,
    "plan_pays": 220.00
  },
  "validation": {
    "sum_check": "patient_responsibility + plan_pays = allowed_amount",
    "result": "180.00 + 220.00 = 400.00 ✓"
  }
}
```

### Pattern 10: Accumulator Updates

Verify accumulators update correctly after claims.

**Test Template:**
```json
{
  "test_name": "accumulator_updates",
  "before_claim": {
    "deductible_met": 1200.00,
    "deductible_limit": 1500.00,
    "oop_met": 2500.00,
    "oop_limit": 6000.00
  },
  "claim": {
    "patient_responsibility": 340.00,
    "deductible_applied": 300.00
  },
  "expected_after": {
    "deductible_met": 1500.00,
    "deductible_remaining": 0.00,
    "oop_met": 2840.00,
    "oop_remaining": 3160.00
  }
}
```

## Format-Specific Test Patterns

### Pattern 11: X12 Envelope Validation

Verify X12 transaction structure is correct.

**Test Template:**
```json
{
  "test_name": "x12_envelope",
  "checks": [
    {
      "name": "ISA_IEA_match",
      "rule": "ISA13 == IEA02"
    },
    {
      "name": "GS_GE_match",
      "rule": "GS06 == GE02"
    },
    {
      "name": "ST_SE_match",
      "rule": "ST02 == SE02"
    },
    {
      "name": "segment_count",
      "rule": "SE01 == actual_segment_count"
    }
  ]
}
```

**Example:**
```
ISA*...*000000001*...~
...
ST*837*0001~
... (26 segments) ...
SE*28*0001~
GE*1*1~
IEA*1*000000001~

Checks:
- ISA13 (000000001) == IEA02 (000000001) ✓
- ST02 (0001) == SE02 (0001) ✓
- SE01 (28) == segment count (28) ✓
```

### Pattern 12: FHIR Resource Validation

Verify FHIR resources meet R4 requirements.

**Test Template:**
```json
{
  "test_name": "fhir_resource_validation",
  "resource_type": "Patient",
  "checks": [
    {
      "name": "resourceType_present",
      "path": "resourceType",
      "expected": "Patient"
    },
    {
      "name": "identifier_structure",
      "path": "identifier[0]",
      "required_fields": ["system", "value"]
    },
    {
      "name": "reference_format",
      "path": "managingOrganization.reference",
      "pattern": "^Organization/[a-zA-Z0-9\\-]+$"
    }
  ]
}
```

### Pattern 13: HL7v2 Message Validation

Verify HL7v2 message structure.

**Test Template:**
```json
{
  "test_name": "hl7v2_message",
  "message_type": "ADT^A01",
  "required_segments": ["MSH", "EVN", "PID", "PV1"],
  "segment_order_checks": [
    { "segment": "MSH", "position": 1 },
    { "segment": "EVN", "position": 2 },
    { "segment": "PID", "position": 3 }
  ],
  "field_checks": [
    {
      "segment": "MSH",
      "field": 9,
      "expected": "ADT^A01^ADT_A01"
    }
  ]
}
```

### Pattern 14: NCPDP Transaction Validation

Verify NCPDP D.0 transaction fields.

**Test Template:**
```json
{
  "test_name": "ncpdp_transaction",
  "transaction_code": "B1",
  "required_fields": [
    { "field_id": "101-A1", "name": "BIN", "format": "6 digits" },
    { "field_id": "102-A2", "name": "Version", "expected": "D0" },
    { "field_id": "103-A3", "name": "Transaction Code", "expected": "B1" },
    { "field_id": "407-D7", "name": "NDC", "format": "11 digits" }
  ]
}
```

## Realistic Data Test Patterns

### Pattern 15: Distribution Validation

Verify generated data follows realistic distributions.

**Test Template:**
```json
{
  "test_name": "distribution_check",
  "sample_size": 1000,
  "distributions": [
    {
      "field": "gender",
      "expected_distribution": {
        "M": 0.49,
        "F": 0.51
      },
      "tolerance": 0.05
    },
    {
      "field": "age_group",
      "expected_distribution": {
        "0-17": 0.22,
        "18-64": 0.62,
        "65+": 0.16
      },
      "tolerance": 0.03
    }
  ]
}
```

### Pattern 16: Temporal Pattern Validation

Verify data shows realistic temporal patterns.

**Test Template:**
```json
{
  "test_name": "temporal_patterns",
  "checks": [
    {
      "name": "er_visits_by_day",
      "pattern": "weekends higher",
      "expected_ratio": 1.2
    },
    {
      "name": "flu_claims_by_month",
      "pattern": "seasonal (Oct-Mar higher)",
      "peak_months": [10, 11, 12, 1, 2, 3]
    },
    {
      "name": "prescription_refills",
      "pattern": "28-30 day intervals",
      "expected_range": [25, 35]
    }
  ]
}
```

### Pattern 17: Comorbidity Validation

Verify condition patterns follow clinical reality.

**Test Template:**
```json
{
  "test_name": "comorbidity_patterns",
  "checks": [
    {
      "primary_condition": "E11 (Type 2 Diabetes)",
      "expected_comorbidities": [
        { "code": "I10", "name": "Hypertension", "frequency": 0.75 },
        { "code": "E78", "name": "Hyperlipidemia", "frequency": 0.65 },
        { "code": "N18", "name": "CKD", "frequency": 0.40 }
      ]
    },
    {
      "primary_condition": "I50 (Heart Failure)",
      "expected_comorbidities": [
        { "code": "I10", "name": "Hypertension", "frequency": 0.80 },
        { "code": "I25", "name": "CAD", "frequency": 0.60 },
        { "code": "E11", "name": "Diabetes", "frequency": 0.45 }
      ]
    }
  ]
}
```

## Test Execution Patterns

### Pattern 18: Single Entity Test

Test individual entity generation.

**Example:**
```json
{
  "prompt": "Generate a 55-year-old female patient with type 2 diabetes and hypertension",
  "expected_output": {
    "patient": {
      "gender": "F",
      "age_range": [54, 56],
      "conditions": {
        "must_include": ["E11", "I10"]
      }
    }
  },
  "validations": [
    "gender == 'F'",
    "calculate_age(birth_date) BETWEEN 54 AND 56",
    "conditions contains code starting with 'E11'",
    "conditions contains code starting with 'I10'"
  ]
}
```

### Pattern 19: Multi-Step Flow Test

Test complete data generation flows.

**Example:**
```json
{
  "flow_name": "patient_to_claim",
  "steps": [
    {
      "step": 1,
      "prompt": "Generate a diabetes patient",
      "output_key": "patient"
    },
    {
      "step": 2,
      "prompt": "Generate an office visit encounter for {{patient}}",
      "output_key": "encounter",
      "validations": [
        "encounter.patient_id == patient.mrn",
        "encounter.diagnoses includes patient.conditions"
      ]
    },
    {
      "step": 3,
      "prompt": "Generate a professional claim for {{encounter}}",
      "output_key": "claim",
      "validations": [
        "claim.service_date == encounter.period_start",
        "claim.diagnoses subset of encounter.diagnoses"
      ]
    }
  ]
}
```

### Pattern 20: Edge Case Test

Test boundary conditions and edge cases.

**Test Template:**
```json
{
  "test_name": "edge_cases",
  "cases": [
    {
      "name": "newborn_patient",
      "input": { "birth_date": "today" },
      "validations": ["age == 0", "no adult conditions"]
    },
    {
      "name": "centenarian",
      "input": { "birth_date": "105 years ago" },
      "validations": ["age == 105", "geriatric conditions appropriate"]
    },
    {
      "name": "zero_dollar_claim",
      "input": { "oop_max_met": true },
      "validations": ["patient_responsibility == 0"]
    },
    {
      "name": "deductible_exactly_met",
      "input": { "deductible_remaining": 100, "charge": 100 },
      "validations": ["deductible_applied == 100", "deductible_met_flag == true"]
    }
  ]
}
```

## Test Results Format

### Standard Test Result Structure

```json
{
  "test_suite": "HealthSim Skills Validation",
  "run_date": "2025-01-15T10:30:00Z",
  "summary": {
    "total_tests": 50,
    "passed": 48,
    "failed": 2,
    "pass_rate": 0.96
  },
  "results": [
    {
      "test_name": "patient_required_fields",
      "category": "structural",
      "status": "passed",
      "duration_ms": 12
    },
    {
      "test_name": "diagnosis_medication_coherence",
      "category": "semantic",
      "status": "failed",
      "error": "Lisinopril prescribed without HTN/CHF/CKD diagnosis",
      "input": { "medications": ["Lisinopril"], "diagnoses": ["J45.20"] },
      "expected": "HTN, CHF, or CKD diagnosis required",
      "actual": "Only Asthma (J45.20) present"
    }
  ]
}
```

## Additional Format Test Patterns

### Pattern 21: HL7v2 ORM Order Validation

Verify ORM order messages are correctly structured.

**Test Template:**
```json
{
  "test_name": "hl7v2_orm_validation",
  "message_type": "ORM^O01",
  "required_segments": ["MSH", "PID", "ORC", "OBR"],
  "checks": [
    { "segment": "ORC", "field": 1, "name": "Order Control", "valid_values": ["NW", "CA", "DC", "XO"] },
    { "segment": "ORC", "field": 2, "name": "Placer Order Number", "required": true },
    { "segment": "OBR", "field": 4, "name": "Universal Service ID", "format": "code^text^system" }
  ]
}
```

### Pattern 22: HL7v2 ORU Results Validation

Verify ORU result messages contain valid observations.

**Test Template:**
```json
{
  "test_name": "hl7v2_oru_validation",
  "message_type": "ORU^R01",
  "required_segments": ["MSH", "PID", "OBR", "OBX"],
  "checks": [
    { "segment": "OBX", "field": 2, "name": "Value Type", "valid_values": ["NM", "ST", "TX", "CE"] },
    { "segment": "OBX", "field": 3, "name": "Observation ID", "format": "LOINC code" },
    { "segment": "OBX", "field": 5, "name": "Value", "matches_type": "OBX-2" },
    { "segment": "OBX", "field": 8, "name": "Abnormal Flag", "valid_values": ["N", "L", "H", "LL", "HH", "A"] },
    { "segment": "OBX", "field": 11, "name": "Result Status", "valid_values": ["P", "F", "C", "X"] }
  ]
}
```

### Pattern 23: CSV Export Validation

Verify CSV output is properly formatted.

**Test Template:**
```json
{
  "test_name": "csv_export_validation",
  "checks": [
    { "name": "header_row_present", "condition": "first_row_is_header" },
    { "name": "consistent_column_count", "condition": "all_rows_same_field_count" },
    { "name": "proper_quoting", "condition": "fields_with_delimiters_are_quoted" },
    { "name": "date_format_consistent", "pattern": "YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS" },
    { "name": "no_trailing_delimiter", "condition": "lines_end_after_last_field" }
  ]
}
```

**Example:**
```csv
mrn,given_name,family_name,birth_date,gender
MRN00000001,John,Smith,1970-03-15,M
MRN00000002,"Smith, Jr.",Robert,1985-06-20,M

Checks:
- Header row present ✓
- All rows have 5 fields ✓
- "Smith, Jr." properly quoted ✓
- Dates in ISO format ✓
```

### Pattern 24: SQL Insert Validation

Verify SQL statements are syntactically correct.

**Test Template:**
```json
{
  "test_name": "sql_insert_validation",
  "dialect": "postgresql",
  "checks": [
    { "name": "valid_table_name", "pattern": "^[a-z_][a-z0-9_]*$" },
    { "name": "proper_string_escaping", "condition": "single_quotes_doubled" },
    { "name": "null_handling", "condition": "NULL_keyword_not_quoted" },
    { "name": "date_format", "pattern": "YYYY-MM-DD" },
    { "name": "transaction_wrapper", "condition": "BEGIN_and_COMMIT_present" }
  ]
}
```

**Example:**
```sql
BEGIN;
INSERT INTO patients (mrn, family_name, birth_date, deceased_date)
VALUES ('MRN00000001', 'O''Brien', '1970-03-15', NULL);
COMMIT;

Checks:
- Table name valid ✓
- O'Brien escaped as O''Brien ✓
- NULL not quoted ✓
- Transaction wrapped ✓
```

### Pattern 25: Order-to-Result Consistency

Verify lab orders result in matching observations.

**Test Template:**
```json
{
  "test_name": "order_result_consistency",
  "order": {
    "code": "80053",
    "description": "Comprehensive Metabolic Panel"
  },
  "expected_results": [
    { "loinc": "2345-7", "name": "Glucose", "required": true },
    { "loinc": "3094-0", "name": "BUN", "required": true },
    { "loinc": "2160-0", "name": "Creatinine", "required": true },
    { "loinc": "2951-2", "name": "Sodium", "required": true },
    { "loinc": "2823-3", "name": "Potassium", "required": true }
  ],
  "validations": [
    "all required results present",
    "values within reference ranges or flagged appropriately",
    "result status matches order status",
    "observation datetime >= order datetime"
  ]
}
```

## Related Skills

- [integration-guide.md](integration-guide.md) - Cross-skill integration
- [../references/validation-rules.md](../references/validation-rules.md) - Validation rules
- [../references/hl7v2-segments.md](../references/hl7v2-segments.md) - HL7v2 segment reference
- [../SKILL.md](../SKILL.md) - Root router
