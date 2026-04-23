# HealthSim Domain Knowledge Base

**Session 1 Deliverable - Knowledge Extraction**  
**Version**: 1.0  
**Date**: 2025-12-09  
**Purpose**: Comprehensive extraction of domain knowledge from healthsim-common, PatientSim, MemberSim, and RxMemberSim repositories for migration to Skills-first architecture.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Data Models & Schemas](#2-data-models--schemas)
3. [Validation Rules](#3-validation-rules)
4. [Format Specifications](#4-format-specifications)
5. [Reference Data Catalog](#5-reference-data-catalog)
6. [Cohort Patterns](#6-cohort-patterns)
7. [Generation Logic](#7-generation-logic)
8. [Code System Mappings](#8-code-system-mappings)

---

## 1. Overview

### 1.1 Product Family Architecture

HealthSim is a family of three products sharing a common foundation:

```
┌─────────────────────────────────────────────────────────────┐
│                    HealthSim Product Family                  │
├─────────────────┬─────────────────┬─────────────────────────┤
│   PatientSim    │   MemberSim     │     RxMemberSim         │
│   (Clinical)    │   (Payer)       │     (Pharmacy)          │
├─────────────────┴─────────────────┴─────────────────────────┤
│                     healthsim-common                          │
│  (Person, Temporal, Generation, Validation, Formats)        │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Core Concepts

| Concept | Description | Source Module |
|---------|-------------|---------------|
| **Person** | Base demographics, identifiers, contact info | healthsim-common/person |
| **Timeline** | Event sequencing with dependencies | healthsim-common/temporal |
| **Distribution** | Statistical generation patterns | healthsim-common/generation |
| **Validation** | Rule-based data quality | healthsim-common/validation |
| **Transformer** | Output format conversion | healthsim-common/formats |

### 1.3 Primary Use Cases

1. **EMR Integration Testing** - Generate HL7v2 ADT messages for admission/discharge workflows
2. **Claims Processing Testing** - Generate X12 837 claims with realistic adjudication
3. **Pharmacy Benefits Testing** - Generate NCPDP claims with DUR alerts
4. **Quality Measure Validation** - Generate patients for HEDIS/CMS measure testing
5. **Population Health Analytics** - Generate cohorts for analytics development

---

## 2. Data Models & Schemas

### 2.1 Core Person Model (healthsim-common)

The foundational person entity shared across all products:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Person",
  "type": "object",
  "required": ["id", "name", "birth_date", "gender"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier"
    },
    "name": {
      "type": "object",
      "required": ["given_name", "family_name"],
      "properties": {
        "given_name": { "type": "string" },
        "middle_name": { "type": "string" },
        "family_name": { "type": "string" },
        "suffix": { "type": "string" },
        "prefix": { "type": "string" }
      }
    },
    "birth_date": {
      "type": "string",
      "format": "date",
      "description": "YYYY-MM-DD format"
    },
    "gender": {
      "type": "string",
      "enum": ["M", "F", "O", "U"],
      "description": "M=Male, F=Female, O=Other, U=Unknown"
    },
    "address": {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "street_address_2": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string", "pattern": "^[A-Z]{2}$" },
        "postal_code": { "type": "string" },
        "country": { "type": "string", "default": "US" }
      }
    },
    "contact": {
      "type": "object",
      "properties": {
        "phone": { "type": "string" },
        "phone_mobile": { "type": "string" },
        "email": { "type": "string", "format": "email" }
      }
    },
    "deceased": { "type": "boolean", "default": false },
    "death_date": { "type": "string", "format": "date" }
  }
}
```

### 2.2 PatientSim Models

#### 2.2.1 Patient (extends Person)

```json
{
  "title": "Patient",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "properties": {
    "mrn": {
      "type": "string",
      "description": "Medical Record Number",
      "minLength": 1
    },
    "ssn": {
      "type": "string",
      "pattern": "^\\d{9}$",
      "description": "Social Security Number (9 digits, no dashes)"
    },
    "race": {
      "type": "string",
      "description": "Race/ethnicity"
    },
    "language": {
      "type": "string",
      "default": "en",
      "description": "Preferred language code"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": ["mrn"]
}
```

#### 2.2.2 Encounter

```json
{
  "title": "Encounter",
  "type": "object",
  "required": ["encounter_id", "patient_mrn", "class_code", "status", "admission_time"],
  "properties": {
    "encounter_id": { "type": "string", "minLength": 1 },
    "patient_mrn": { "type": "string", "minLength": 1 },
    "class_code": {
      "type": "string",
      "enum": ["I", "O", "E", "U", "OBS"],
      "description": "I=Inpatient, O=Outpatient, E=Emergency, U=Urgent, OBS=Observation"
    },
    "status": {
      "type": "string",
      "enum": ["planned", "arrived", "in-progress", "on-hold", "finished", "cancelled"]
    },
    "admission_time": { "type": "string", "format": "date-time" },
    "discharge_time": { "type": "string", "format": "date-time" },
    "facility": { "type": "string" },
    "department": { "type": "string" },
    "room": { "type": "string" },
    "bed": { "type": "string" },
    "chief_complaint": { "type": "string" },
    "admitting_diagnosis": { "type": "string" },
    "discharge_disposition": { "type": "string" },
    "attending_physician": { "type": "string" },
    "admitting_physician": { "type": "string" }
  }
}
```

#### 2.2.3 Diagnosis

```json
{
  "title": "Diagnosis",
  "type": "object",
  "required": ["code", "description", "patient_mrn", "diagnosed_date"],
  "properties": {
    "code": {
      "type": "string",
      "description": "ICD-10 diagnosis code"
    },
    "description": { "type": "string" },
    "type": {
      "type": "string",
      "enum": ["admitting", "working", "final", "differential"],
      "default": "final"
    },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "diagnosed_date": { "type": "string", "format": "date" },
    "resolved_date": { "type": "string", "format": "date" }
  }
}
```

#### 2.2.4 Medication

```json
{
  "title": "Medication",
  "type": "object",
  "required": ["name", "dose", "route", "frequency", "patient_mrn", "start_date"],
  "properties": {
    "name": { "type": "string" },
    "code": { "type": "string", "description": "RxNorm or NDC code" },
    "dose": { "type": "string", "description": "e.g., '500 mg', '10 units'" },
    "route": {
      "type": "string",
      "description": "PO, IV, IM, SubQ, INH, etc."
    },
    "frequency": {
      "type": "string",
      "description": "QD, BID, TID, QID, PRN, Q8H, etc."
    },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "start_date": { "type": "string", "format": "date-time" },
    "end_date": { "type": "string", "format": "date-time" },
    "status": {
      "type": "string",
      "enum": ["active", "completed", "stopped", "on-hold"],
      "default": "active"
    },
    "prescriber": { "type": "string" },
    "indication": { "type": "string" }
  }
}
```

#### 2.2.5 LabResult

```json
{
  "title": "LabResult",
  "type": "object",
  "required": ["test_name", "value", "patient_mrn", "collected_time"],
  "properties": {
    "test_name": { "type": "string" },
    "loinc_code": { "type": "string" },
    "value": { "type": "string" },
    "unit": { "type": "string" },
    "reference_range": { "type": "string" },
    "abnormal_flag": {
      "type": "string",
      "enum": ["H", "L", "HH", "LL", "A", "N", null],
      "description": "H=High, L=Low, HH=Critical High, LL=Critical Low, A=Abnormal"
    },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "collected_time": { "type": "string", "format": "date-time" },
    "resulted_time": { "type": "string", "format": "date-time" },
    "performing_lab": { "type": "string" },
    "ordering_provider": { "type": "string" }
  }
}
```

#### 2.2.6 VitalSign

```json
{
  "title": "VitalSign",
  "type": "object",
  "required": ["patient_mrn", "observation_time"],
  "properties": {
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "observation_time": { "type": "string", "format": "date-time" },
    "temperature": {
      "type": "number",
      "minimum": 90,
      "maximum": 110,
      "description": "Temperature in Fahrenheit"
    },
    "heart_rate": {
      "type": "integer",
      "minimum": 0,
      "maximum": 300,
      "description": "Beats per minute"
    },
    "respiratory_rate": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Breaths per minute"
    },
    "systolic_bp": {
      "type": "integer",
      "minimum": 0,
      "maximum": 300,
      "description": "mmHg"
    },
    "diastolic_bp": {
      "type": "integer",
      "minimum": 0,
      "maximum": 200,
      "description": "mmHg"
    },
    "spo2": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "description": "Oxygen saturation percentage"
    },
    "height_cm": { "type": "number", "minimum": 0, "maximum": 300 },
    "weight_kg": { "type": "number", "minimum": 0, "maximum": 500 }
  }
}
```

### 2.3 MemberSim Models

#### 2.3.1 Member (extends Person)

```json
{
  "title": "Member",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "required": ["member_id", "group_id", "coverage_start", "plan_code"],
  "properties": {
    "member_id": { "type": "string", "description": "Unique member identifier" },
    "subscriber_id": { "type": "string", "description": "For dependents, reference to subscriber" },
    "relationship_code": {
      "type": "string",
      "enum": ["18", "01", "19"],
      "default": "18",
      "description": "18=Self, 01=Spouse, 19=Child"
    },
    "group_id": { "type": "string", "description": "Employer/group identifier" },
    "coverage_start": { "type": "string", "format": "date" },
    "coverage_end": { "type": "string", "format": "date" },
    "plan_code": { "type": "string", "description": "Benefit plan identifier" },
    "pcp_npi": { "type": "string", "description": "Assigned PCP NPI (for HMO plans)" }
  }
}
```

#### 2.3.2 Claim

```json
{
  "title": "Claim",
  "type": "object",
  "required": ["claim_id", "claim_type", "member_id", "subscriber_id", "provider_npi", "service_date", "principal_diagnosis"],
  "properties": {
    "claim_id": { "type": "string" },
    "claim_type": {
      "type": "string",
      "enum": ["PROFESSIONAL", "INSTITUTIONAL", "DENTAL", "RX"]
    },
    "member_id": { "type": "string" },
    "subscriber_id": { "type": "string" },
    "provider_npi": { "type": "string", "pattern": "^\\d{10}$" },
    "facility_npi": { "type": "string" },
    "service_date": { "type": "string", "format": "date" },
    "admission_date": { "type": "string", "format": "date" },
    "discharge_date": { "type": "string", "format": "date" },
    "place_of_service": {
      "type": "string",
      "default": "11",
      "description": "11=Office, 21=Inpatient, 22=Outpatient, 23=ER"
    },
    "claim_lines": {
      "type": "array",
      "items": { "$ref": "#/definitions/ClaimLine" }
    },
    "principal_diagnosis": { "type": "string", "description": "ICD-10 code" },
    "other_diagnoses": {
      "type": "array",
      "items": { "type": "string" }
    },
    "authorization_number": { "type": "string" }
  }
}
```

#### 2.3.3 ClaimLine

```json
{
  "title": "ClaimLine",
  "type": "object",
  "required": ["line_number", "procedure_code", "service_date", "charge_amount"],
  "properties": {
    "line_number": { "type": "integer", "minimum": 1 },
    "procedure_code": { "type": "string", "description": "CPT/HCPCS code" },
    "procedure_modifiers": {
      "type": "array",
      "items": { "type": "string" },
      "maxItems": 4
    },
    "service_date": { "type": "string", "format": "date" },
    "units": { "type": "number", "default": 1 },
    "charge_amount": { "type": "number", "description": "Billed amount in dollars" },
    "diagnosis_pointers": {
      "type": "array",
      "items": { "type": "integer" },
      "default": [1]
    },
    "revenue_code": { "type": "string", "description": "For institutional claims" },
    "ndc_code": { "type": "string", "description": "Drug code if applicable" },
    "place_of_service": { "type": "string", "default": "11" }
  }
}
```

#### 2.3.4 Plan

```json
{
  "title": "Plan",
  "type": "object",
  "required": ["plan_code", "plan_name", "plan_type"],
  "properties": {
    "plan_code": { "type": "string" },
    "plan_name": { "type": "string" },
    "plan_type": {
      "type": "string",
      "enum": ["HMO", "PPO", "EPO", "POS", "HDHP"]
    },
    "coverage_type": {
      "type": "string",
      "enum": ["MEDICAL", "DENTAL", "VISION", "RX"],
      "default": "MEDICAL"
    },
    "deductible_individual": { "type": "number", "default": 500 },
    "deductible_family": { "type": "number", "default": 1500 },
    "oop_max_individual": { "type": "number", "default": 3000 },
    "oop_max_family": { "type": "number", "default": 6000 },
    "copay_pcp": { "type": "number", "default": 25 },
    "copay_specialist": { "type": "number", "default": 50 },
    "copay_er": { "type": "number", "default": 250 },
    "coinsurance": { "type": "number", "default": 0.20, "description": "0.20 = 20%" },
    "requires_pcp": { "type": "boolean", "default": false },
    "requires_referral": { "type": "boolean", "default": false }
  }
}
```

#### 2.3.5 Accumulator

```json
{
  "title": "Accumulator",
  "type": "object",
  "required": ["member_id", "plan_year", "deductible_limit", "oop_limit"],
  "properties": {
    "member_id": { "type": "string" },
    "plan_year": { "type": "integer" },
    "deductible_applied": { "type": "number", "default": 0 },
    "deductible_limit": { "type": "number" },
    "oop_applied": { "type": "number", "default": 0 },
    "oop_limit": { "type": "number" },
    "last_updated": { "type": "string", "format": "date-time" }
  }
}
```

### 2.4 RxMemberSim Models

#### 2.4.1 Prescription

```json
{
  "title": "Prescription",
  "type": "object",
  "required": ["prescription_number", "ndc", "drug_name", "quantity_prescribed", "days_supply", "prescriber_npi", "written_date", "expiration_date"],
  "properties": {
    "prescription_number": { "type": "string" },
    "ndc": { "type": "string", "pattern": "^\\d{11}$" },
    "drug_name": { "type": "string" },
    "quantity_prescribed": { "type": "number" },
    "days_supply": { "type": "integer" },
    "refills_authorized": { "type": "integer", "default": 0 },
    "refills_remaining": { "type": "integer", "default": 0 },
    "prescriber_npi": { "type": "string", "pattern": "^\\d{10}$" },
    "prescriber_name": { "type": "string" },
    "prescriber_dea": { "type": "string" },
    "written_date": { "type": "string", "format": "date" },
    "expiration_date": { "type": "string", "format": "date" },
    "daw_code": {
      "type": "string",
      "enum": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
      "default": "0",
      "description": "Dispense As Written code"
    },
    "diagnosis_codes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "directions": { "type": "string" }
  }
}
```

#### 2.4.2 PharmacyClaim

```json
{
  "title": "PharmacyClaim",
  "type": "object",
  "required": ["claim_id", "transaction_code", "service_date", "pharmacy_npi", "member_id", "cardholder_id", "bin", "pcn", "group_number", "prescription_number", "ndc", "quantity_dispensed", "days_supply", "prescriber_npi"],
  "properties": {
    "claim_id": { "type": "string" },
    "transaction_code": {
      "type": "string",
      "enum": ["B1", "B2", "B3"],
      "description": "B1=Billing, B2=Reversal, B3=Rebill"
    },
    "service_date": { "type": "string", "format": "date" },
    "pharmacy_npi": { "type": "string" },
    "pharmacy_ncpdp": { "type": "string" },
    "member_id": { "type": "string" },
    "cardholder_id": { "type": "string" },
    "person_code": { "type": "string" },
    "bin": { "type": "string", "pattern": "^\\d{6}$" },
    "pcn": { "type": "string" },
    "group_number": { "type": "string" },
    "prescription_number": { "type": "string" },
    "fill_number": { "type": "integer", "minimum": 0 },
    "ndc": { "type": "string" },
    "quantity_dispensed": { "type": "number" },
    "days_supply": { "type": "integer" },
    "daw_code": { "type": "string" },
    "compound_code": { "type": "string", "default": "0" },
    "prescriber_npi": { "type": "string" },
    "ingredient_cost_submitted": { "type": "number" },
    "dispensing_fee_submitted": { "type": "number" },
    "usual_customary_charge": { "type": "number" },
    "gross_amount_due": { "type": "number" },
    "prior_auth_number": { "type": "string" },
    "prior_auth_type": { "type": "string" },
    "dur_pps_code_counter": { "type": "integer", "default": 0 },
    "dur_reason_for_service": { "type": "string" },
    "dur_professional_service": { "type": "string" },
    "dur_result_of_service": { "type": "string" }
  }
}
```

#### 2.4.3 FormularyDrug

```json
{
  "title": "FormularyDrug",
  "type": "object",
  "required": ["ndc", "gpi", "drug_name", "tier", "covered"],
  "properties": {
    "ndc": { "type": "string" },
    "gpi": { "type": "string", "description": "Generic Product Identifier" },
    "drug_name": { "type": "string" },
    "tier": { "type": "integer", "minimum": 1, "maximum": 5 },
    "covered": { "type": "boolean", "default": true },
    "requires_pa": { "type": "boolean", "default": false },
    "requires_step_therapy": { "type": "boolean", "default": false },
    "step_therapy_group": { "type": "string" },
    "quantity_limit": { "type": "integer" },
    "quantity_limit_days": { "type": "integer" },
    "max_days_supply": { "type": "integer" },
    "min_age": { "type": "integer" },
    "max_age": { "type": "integer" },
    "gender_restriction": { "type": "string", "enum": ["M", "F", null] }
  }
}
```

---

## 3. Validation Rules

### 3.1 Structural Validation

#### 3.1.1 Required Fields

| Entity | Required Fields |
|--------|----------------|
| Person | id, name.given_name, name.family_name, birth_date, gender |
| Patient | Person fields + mrn |
| Encounter | encounter_id, patient_mrn, class_code, status, admission_time |
| Diagnosis | code, description, patient_mrn, diagnosed_date |
| Medication | name, dose, route, frequency, patient_mrn, start_date |
| LabResult | test_name, value, patient_mrn, collected_time |
| Member | Person fields + member_id, group_id, coverage_start, plan_code |
| Claim | claim_id, claim_type, member_id, provider_npi, service_date, principal_diagnosis |
| PharmacyClaim | claim_id, service_date, pharmacy_npi, member_id, ndc, quantity_dispensed |

#### 3.1.2 Referential Integrity Rules

```yaml
referential_integrity:
  # PatientSim
  - source: Encounter.patient_mrn
    target: Patient.mrn
    required: true
    
  - source: Diagnosis.patient_mrn
    target: Patient.mrn
    required: true
    
  - source: Diagnosis.encounter_id
    target: Encounter.encounter_id
    required: false
    
  - source: Medication.patient_mrn
    target: Patient.mrn
    required: true
    
  - source: LabResult.patient_mrn
    target: Patient.mrn
    required: true
    
  # MemberSim
  - source: Claim.member_id
    target: Member.member_id
    required: true
    
  - source: Member.subscriber_id
    target: Member.member_id
    required: false  # Only for dependents
    
  # RxMemberSim
  - source: PharmacyClaim.member_id
    target: Member.member_id
    required: true
```

### 3.2 Temporal Validation

#### 3.2.1 Date Order Rules

```yaml
temporal_rules:
  # General
  - rule: birth_date_not_future
    field: birth_date
    condition: birth_date <= today
    severity: ERROR
    
  - rule: death_after_birth
    condition: death_date >= birth_date
    severity: ERROR
    when: deceased == true
    
  # Encounters
  - rule: discharge_after_admission
    condition: discharge_time >= admission_time
    severity: ERROR
    when: discharge_time != null
    
  # Diagnoses
  - rule: resolved_after_diagnosed
    condition: resolved_date >= diagnosed_date
    severity: ERROR
    when: resolved_date != null
    
  # Medications
  - rule: med_end_after_start
    condition: end_date >= start_date
    severity: ERROR
    when: end_date != null
    
  # Labs
  - rule: resulted_after_collected
    condition: resulted_time >= collected_time
    severity: ERROR
    when: resulted_time != null
    
  # Coverage
  - rule: coverage_end_after_start
    condition: coverage_end >= coverage_start
    severity: ERROR
    when: coverage_end != null
```

#### 3.2.2 Age Validation

```yaml
age_validation:
  - rule: valid_age_range
    condition: age >= 0 AND age <= 150
    severity: ERROR
    
  - rule: reasonable_adult_age
    condition: age >= 0 AND age <= 120
    severity: WARNING
```

### 3.3 Clinical Validation (PatientSim)

#### 3.3.1 Age-Condition Appropriateness

```yaml
age_condition_rules:
  geriatric_conditions:
    codes: ["I25.10", "I50.9", "N18.3", "N18.4"]
    min_typical_age: 40
    severity: WARNING
    message: "Geriatric condition in patient under 40"
    
  pediatric_conditions:
    codes: ["J45.909"]  # Asthma
    max_typical_age: 18
    severity: INFO
    message: "Typically pediatric-onset condition"
```

#### 3.3.2 Gender-Condition Appropriateness

```yaml
gender_condition_rules:
  female_only:
    codes: []  # Pregnancy, gynecological - add as needed
    allowed_gender: F
    severity: ERROR
    
  male_only:
    codes: []  # Prostate - add as needed
    allowed_gender: M
    severity: ERROR
```

#### 3.3.3 Medication-Diagnosis Coherence

```yaml
medication_indication_rules:
  Metformin:
    expected_diagnoses: ["E11.9", "E11.65"]
    category: diabetes
    
  Insulin Glargine:
    expected_diagnoses: ["E10.9", "E11.9", "E11.65"]
    category: diabetes
    
  Lisinopril:
    expected_diagnoses: ["I10", "I11.9", "I50.9"]
    category: cardiovascular
    
  Amlodipine:
    expected_diagnoses: ["I10", "I11.9"]
    category: cardiovascular
    
  Metoprolol:
    expected_diagnoses: ["I10", "I11.9", "I25.10", "I48.91"]
    category: cardiovascular
    
  Azithromycin:
    expected_diagnoses: ["J18.9", "A49.9"]
    category: infection
    
  Ceftriaxone:
    expected_diagnoses: ["J18.9", "A41.9", "A49.9"]
    category: infection
    
  Vancomycin:
    expected_diagnoses: ["A41.9", "A49.9"]
    category: infection
```

#### 3.3.4 Vital Sign Plausibility

```yaml
vital_sign_rules:
  temperature:
    critical_high: 106.0
    critical_low: 92.0
    unit: Fahrenheit
    severity: WARNING
    
  heart_rate:
    critical_high: 180
    critical_low: 40
    unit: bpm
    severity: WARNING
    
  spo2:
    critical_low: 85
    unit: percent
    severity: WARNING
    
  pulse_pressure:
    min_normal: 20
    max_normal: 100
    calculation: systolic_bp - diastolic_bp
    severity: WARNING
    
  bmi:
    severely_underweight: 16
    severely_obese: 40
    severity: INFO
```

### 3.4 Claims Validation (MemberSim)

#### 3.4.1 Claim Structure Rules

```yaml
claim_rules:
  - rule: valid_npi_format
    field: provider_npi
    pattern: "^\\d{10}$"
    severity: ERROR
    
  - rule: valid_icd10_format
    field: principal_diagnosis
    pattern: "^[A-Z]\\d{2}(\\.\\d{1,4})?$"
    severity: ERROR
    
  - rule: valid_cpt_format
    field: procedure_code
    pattern: "^\\d{5}$"
    severity: ERROR
    
  - rule: positive_charge
    condition: charge_amount > 0
    severity: ERROR
    
  - rule: valid_pos_code
    field: place_of_service
    valid_values: ["11", "12", "21", "22", "23", "24", "31", "32", "41", "42"]
    severity: ERROR
```

### 3.5 Pharmacy Validation (RxMemberSim)

#### 3.5.1 DUR Rules

```yaml
dur_rules:
  drug_drug_interactions:
    - id: DD-001
      drug1_gpi_prefix: "8330"  # Warfarin
      drug2_gpi_prefix: "6610"  # NSAIDs
      significance: 1  # Major
      message: "Increased bleeding risk"
      
    - id: DD-005
      drug1_gpi_prefix: "6505"  # Opioids
      drug2_gpi_prefix: "5710"  # Benzodiazepines
      significance: 1  # Major
      message: "CNS depression - death risk"
      
  therapeutic_duplication:
    - gpi_class: "3940"
      class_name: "Statins"
      max_concurrent: 1
      
    - gpi_class: "4940"
      class_name: "PPIs"
      max_concurrent: 1
      
    - gpi_class: "5816"
      class_name: "SSRIs"
      max_concurrent: 1
      
  early_refill:
    threshold_percent: 0.80
    message: "Refill before 80% of supply used"
    
  age_restrictions:
    - drug_gpi: "6510"  # CNS Stimulants
      min_age: 6
      max_age: 65
      
  gender_restrictions:
    - drug_gpi: "4399"  # Testosterone
      allowed_gender: M
      
    - drug_gpi: "4320"  # Estrogens
      allowed_gender: F
```

---

## 4. Format Specifications

### 4.1 FHIR R4 Mappings

#### 4.1.1 Patient → FHIR Patient Resource

```yaml
fhir_patient_mapping:
  resourceType: Patient
  
  field_mappings:
    - source: mrn
      target: identifier[0].value
      system: "http://hospital.example.org/patient-mrn"
      
    - source: name.given_name
      target: name[0].given[0]
      
    - source: name.family_name
      target: name[0].family
      
    - source: gender
      target: gender
      transform:
        M: male
        F: female
        O: other
        U: unknown
        
    - source: birth_date
      target: birthDate
      format: "YYYY-MM-DD"
      
    - source: deceased
      target: deceasedBoolean
      when: death_date == null
      
    - source: death_date
      target: deceasedDateTime
      format: "YYYY-MM-DD"
      when: death_date != null
```

#### 4.1.2 Encounter → FHIR Encounter Resource

```yaml
fhir_encounter_mapping:
  resourceType: Encounter
  
  field_mappings:
    - source: encounter_id
      target: identifier[0].value
      system: "http://hospital.example.org/encounter-id"
      
    - source: status
      target: status
      # Direct mapping: planned, in-progress, finished, cancelled
      
    - source: class_code
      target: class.code
      system: "http://terminology.hl7.org/CodeSystem/v3-ActCode"
      transform:
        I: IMP
        O: AMB
        E: EMER
        U: OBSENC
        
    - source: patient_mrn
      target: subject.reference
      format: "Patient/{patient_resource_id}"
      
    - source: admission_time
      target: period.start
      format: ISO8601
      
    - source: discharge_time
      target: period.end
      format: ISO8601
```

#### 4.1.3 Diagnosis → FHIR Condition Resource

```yaml
fhir_condition_mapping:
  resourceType: Condition
  
  field_mappings:
    - source: code
      target: code.coding[0].code
      system: "http://hl7.org/fhir/sid/icd-10"
      
    - source: description
      target: code.coding[0].display
      
    - source: patient_mrn
      target: subject.reference
      format: "Patient/{patient_resource_id}"
      
    - source: diagnosed_date
      target: onsetDateTime
      format: "YYYY-MM-DD"
      
  defaults:
    clinicalStatus:
      coding:
        - system: "http://terminology.hl7.org/CodeSystem/condition-clinical"
          code: active
    verificationStatus:
      coding:
        - system: "http://terminology.hl7.org/CodeSystem/condition-ver-status"
          code: confirmed
```

#### 4.1.4 LabResult → FHIR Observation Resource

```yaml
fhir_observation_mapping:
  resourceType: Observation
  
  field_mappings:
    - source: loinc_code
      target: code.coding[0].code
      system: "http://loinc.org"
      
    - source: test_name
      target: code.coding[0].display
      
    - source: value (numeric)
      target: valueQuantity.value
      
    - source: unit
      target: valueQuantity.unit
      system: "http://unitsofmeasure.org"
      
    - source: value (string)
      target: valueString
      when: value is not numeric
      
    - source: collected_time
      target: effectiveDateTime
      format: ISO8601
      
  defaults:
    status: final
    category:
      coding:
        - system: "http://terminology.hl7.org/CodeSystem/observation-category"
          code: laboratory
```

#### 4.1.5 LOINC Code Mappings

```yaml
loinc_mappings:
  labs:
    Hemoglobin: ["718-7", "Hemoglobin [Mass/volume] in Blood"]
    Hematocrit: ["4544-3", "Hematocrit [Volume Fraction] of Blood"]
    WBC: ["6690-2", "Leukocytes [#/volume] in Blood"]
    Platelets: ["777-3", "Platelets [#/volume] in Blood"]
    Sodium: ["2951-2", "Sodium [Moles/volume] in Serum or Plasma"]
    Potassium: ["2823-3", "Potassium [Moles/volume] in Serum or Plasma"]
    Chloride: ["2075-0", "Chloride [Moles/volume] in Serum or Plasma"]
    Bicarbonate: ["1963-8", "Bicarbonate [Moles/volume] in Serum or Plasma"]
    BUN: ["3094-0", "Urea nitrogen [Mass/volume] in Serum or Plasma"]
    Creatinine: ["2160-0", "Creatinine [Mass/volume] in Serum or Plasma"]
    Glucose: ["2345-7", "Glucose [Mass/volume] in Serum or Plasma"]
    Calcium: ["17861-6", "Calcium [Mass/volume] in Serum or Plasma"]
    Lactate: ["2524-7", "Lactate [Moles/volume] in Blood"]
    
  vitals:
    heart_rate: ["8867-4", "Heart rate"]
    respiratory_rate: ["9279-1", "Respiratory rate"]
    temperature: ["8310-5", "Body temperature"]
    systolic_bp: ["8480-6", "Systolic blood pressure"]
    diastolic_bp: ["8462-4", "Diastolic blood pressure"]
    spo2: ["2708-6", "Oxygen saturation in Arterial blood"]
    height: ["8302-2", "Body height"]
    weight: ["29463-7", "Body weight"]
    bmi: ["39156-5", "Body mass index (BMI)"]
```

### 4.2 HL7v2 Message Structures

#### 4.2.1 ADT Message Structure

```
Message Types:
  ADT^A01 - Patient Admission
  ADT^A03 - Patient Discharge
  ADT^A08 - Patient Update

Segment Order:
  MSH - Message Header (required)
  EVN - Event Type (required)
  PID - Patient Identification (required)
  PV1 - Patient Visit (required)
  DG1 - Diagnosis (optional, repeating)
```

#### 4.2.2 MSH Segment Structure

```yaml
msh_segment:
  MSH-1: "|"  # Field Separator
  MSH-2: "^~\\&"  # Encoding Characters
  MSH-3: sending_application
  MSH-4: sending_facility
  MSH-5: receiving_application
  MSH-6: receiving_facility
  MSH-7: timestamp  # YYYYMMDDHHmmss
  MSH-8: ""  # Security
  MSH-9: message_type^trigger_event  # e.g., ADT^A01
  MSH-10: message_control_id
  MSH-11: "P"  # Processing ID (P=Production)
  MSH-12: "2.5"  # Version ID
```

#### 4.2.3 PID Segment Structure

```yaml
pid_segment:
  PID-1: "1"  # Set ID
  PID-2: ""  # Deprecated
  PID-3: mrn  # Patient Identifier
  PID-4: ""  # Deprecated
  PID-5: family_name^given_name  # Patient Name
  PID-6: ""  # Mother's Maiden Name
  PID-7: birth_date  # YYYYMMDD
  PID-8: gender  # M, F, O, U
  PID-9: ""  # Patient Alias
  PID-10: ""  # Race
  PID-11: ""  # Address
  # ... fields 12-28 typically empty
  PID-29: death_datetime  # If deceased
  PID-30: deceased_indicator  # Y/N
```

#### 4.2.4 PV1 Segment Structure

```yaml
pv1_segment:
  PV1-1: "1"  # Set ID
  PV1-2: patient_class  # I, O, E (Inpatient, Outpatient, Emergency)
  PV1-3: ""  # Assigned Location
  PV1-4: admission_type  # 1=Emergency, 2=Urgent, 3=Elective
  # ... fields 5-18 typically empty
  PV1-19: visit_number  # encounter_id
  # ... fields 20-35 typically empty
  PV1-36: discharge_disposition  # 01=Home, 02=Rehab, 03=SNF, 20=Expired
  # ... fields 37-43 typically empty
  PV1-44: admit_datetime  # YYYYMMDDHHmmss
  PV1-45: discharge_datetime
```

#### 4.2.5 DG1 Segment Structure

```yaml
dg1_segment:
  DG1-1: set_id  # Sequence number (1, 2, 3...)
  DG1-2: ""  # Deprecated
  DG1-3: diagnosis_code^description^I10  # ICD-10 code
  DG1-4: ""  # Deprecated
  DG1-5: ""  # Diagnosis Date/Time
  DG1-6: diagnosis_type  # A=Admitting, W=Working, F=Final
```

### 4.3 X12 EDI Formats (MemberSim)

#### 4.3.1 837P Professional Claim Structure

```
Transaction Set: 837P (Professional Claims)

Hierarchical Levels:
  HL*1*...*20*1~          Level 1: Information Source (Submitter)
    NM1*41*...*             Submitter Name
    HL*2*1*22*1~          Level 2: Information Receiver (Payer)
      NM1*40*...*           Payer Name
      HL*3*2*23*0~        Level 3: Billing Provider
        NM1*85*...*         Billing Provider Name
        HL*4*3*22*0~      Level 4: Subscriber
          NM1*IL*...*       Subscriber Name
          CLM*...*          Claim Information
            DTP*...*        Service Dates
            HI*...*         Diagnosis Codes
            NM1*82*...*     Rendering Provider
            SV1*...*        Professional Service Line
```

#### 4.3.2 837I Institutional Claim Structure

```
Transaction Set: 837I (Institutional Claims)

Similar hierarchy with additional segments:
  CLM*...*              Claim Information
    DTP*434*...*        Statement Dates
    CL1*...*            Institutional Claim Code
    HI*BK:...*          Principal Diagnosis
    HI*BF:...*          Other Diagnoses
    NM1*82*...*         Attending Provider
    SV2*...*            Institutional Service Line
      DTP*472*...*      Service Date
```

#### 4.3.3 835 Payment/Remittance Structure

```
Transaction Set: 835 (Payment/Remittance)

Key Segments:
  BPR*...*              Financial Information (payment amount, method)
  TRN*...*              Reassociation Trace Number
  N1*PR*...*            Payer Identification
  N1*PE*...*            Payee Identification
  LX*1~                 Header Number
    CLP*...*            Claim Payment Information
      NM1*QC*...*       Patient Name
      SVC*...*          Service Line Adjudication
        CAS*...*        Claim Adjustment (CARC codes)
```

#### 4.3.4 834 Enrollment Structure

```
Transaction Set: 834 (Benefit Enrollment)

Key Segments:
  BGN*...*              Beginning Segment
  N1*P5*...*            Sponsor Name
  N1*IN*...*            Payer Name
  INS*Y*18*...*         Member Level Detail (Y=Subscriber, 18=Self)
  REF*0F*...*           Subscriber Number
  NM1*IL*...*           Member Name
  DMG*D8*...*           Demographics (DOB, Gender)
  HD*...*               Health Coverage
  DTP*348*...*          Effective Date
```

### 4.4 NCPDP Formats (RxMemberSim)

#### 4.4.1 NCPDP D.0 Claim Request

```yaml
ncpdp_claim_segments:
  transmission_header:
    bin: "6-digit BIN"
    version: "D0"
    transaction_code: "B1"  # B1=Billing, B2=Reversal
    pcn: "Processor Control Number"
    
  patient_segment:
    patient_id: member_id
    date_of_birth: "YYYYMMDD"
    patient_gender: "1=Male, 2=Female"
    
  insurance_segment:
    cardholder_id: subscriber_id
    group_id: group_number
    person_code: "001=Self, 002=Spouse, 003=Child"
    relationship_code: "1=Cardholder, 2=Spouse, 3=Child"
    
  claim_segment:
    prescription_service_ref_number: rx_number
    product_service_id: ndc  # 11-digit
    quantity_dispensed: decimal
    days_supply: integer
    compound_code: "0=Not compound, 1=Compound"
    daw_code: "0-9"
    date_prescription_written: "YYYYMMDD"
    
  prescriber_segment:
    prescriber_id_qualifier: "01"  # NPI
    prescriber_id: npi
    
  pricing_segment:
    ingredient_cost_submitted: decimal
    dispensing_fee_submitted: decimal
    usual_customary_charge: decimal
    gross_amount_due: decimal
    
  dur_pps_segment:
    dur_pps_code_counter: integer
    reason_for_service_code: "MA, TD, ER, etc."
    professional_service_code: "M0, P0, R0"
    result_of_service_code: "1A, 1B, 1E"
```

#### 4.4.2 NCPDP Response Structure

```yaml
ncpdp_response_segments:
  response_header:
    transaction_response_status: "A=Accepted, R=Rejected"
    
  response_status:
    response_status: "P=Paid, R=Rejected, D=Duplicate"
    authorization_number: string
    
  response_reject:
    reject_code: string  # 70=Product Not Covered, 75=Prior Auth Required
    reject_count: integer
    
  response_pricing:
    ingredient_cost_paid: decimal
    dispensing_fee_paid: decimal
    total_amount_paid: decimal
    patient_pay_amount: decimal
    copay_amount: decimal
    coinsurance_amount: decimal
    deductible_amount: decimal
    
  response_dur:
    dur_alert_code: string
    clinical_significance_code: "1=Major, 2=Moderate, 3=Minor"
    other_pharmacy_indicator: string
    previous_fill_date: "YYYYMMDD"
    message: string
```

---

## 5. Reference Data Catalog

### 5.1 Code Systems

#### 5.1.1 ICD-10 Diagnosis Codes (Common)

```yaml
icd10_common:
  diabetes:
    - code: E11.9
      description: "Type 2 diabetes mellitus without complications"
    - code: E11.65
      description: "Type 2 diabetes with hyperglycemia"
    - code: E10.9
      description: "Type 1 diabetes mellitus without complications"
      
  cardiac:
    - code: I10
      description: "Essential (primary) hypertension"
    - code: I11.9
      description: "Hypertensive heart disease without heart failure"
    - code: I25.10
      description: "Atherosclerotic heart disease of native coronary artery"
    - code: I48.91
      description: "Atrial fibrillation, unspecified"
    - code: I50.9
      description: "Heart failure, unspecified"
      
  respiratory:
    - code: J44.0
      description: "COPD with acute lower respiratory infection"
    - code: J44.1
      description: "COPD with acute exacerbation"
    - code: J18.9
      description: "Pneumonia, unspecified organism"
    - code: J45.909
      description: "Unspecified asthma, uncomplicated"
      
  renal:
    - code: N18.3
      description: "Chronic kidney disease, stage 3"
    - code: N18.4
      description: "Chronic kidney disease, stage 4"
    - code: N17.9
      description: "Acute kidney failure, unspecified"
      
  infection:
    - code: A41.9
      description: "Sepsis, unspecified organism"
    - code: A49.9
      description: "Bacterial infection, unspecified"
      
  metabolic:
    - code: E78.5
      description: "Hyperlipidemia, unspecified"
    - code: E66.9
      description: "Obesity, unspecified"
```

#### 5.1.2 CPT Procedure Codes (Common)

```yaml
cpt_common:
  office_visits:
    - code: "99211"
      description: "Office visit, established, minimal"
    - code: "99212"
      description: "Office visit, established, straightforward"
    - code: "99213"
      description: "Office visit, established, low complexity"
    - code: "99214"
      description: "Office visit, established, moderate complexity"
    - code: "99215"
      description: "Office visit, established, high complexity"
    - code: "99201"
      description: "Office visit, new patient, straightforward"
    - code: "99203"
      description: "Office visit, new patient, low complexity"
    - code: "99204"
      description: "Office visit, new patient, moderate complexity"
    - code: "99205"
      description: "Office visit, new patient, high complexity"
      
  hospital:
    - code: "99221"
      description: "Initial hospital care, low severity"
    - code: "99222"
      description: "Initial hospital care, moderate severity"
    - code: "99223"
      description: "Initial hospital care, high severity"
    - code: "99231"
      description: "Subsequent hospital care, low complexity"
    - code: "99232"
      description: "Subsequent hospital care, moderate complexity"
    - code: "99233"
      description: "Subsequent hospital care, high complexity"
      
  emergency:
    - code: "99281"
      description: "ED visit, minimal"
    - code: "99282"
      description: "ED visit, low severity"
    - code: "99283"
      description: "ED visit, moderate severity"
    - code: "99284"
      description: "ED visit, high severity"
    - code: "99285"
      description: "ED visit, high severity with threat to life"
```

#### 5.1.3 Place of Service Codes

```yaml
place_of_service:
  - code: "11"
    description: "Office"
  - code: "12"
    description: "Home"
  - code: "21"
    description: "Inpatient Hospital"
  - code: "22"
    description: "On Campus-Outpatient Hospital"
  - code: "23"
    description: "Emergency Room – Hospital"
  - code: "24"
    description: "Ambulatory Surgical Center"
  - code: "31"
    description: "Skilled Nursing Facility"
  - code: "32"
    description: "Nursing Facility"
  - code: "41"
    description: "Ambulance – Land"
  - code: "42"
    description: "Ambulance – Air or Water"
  - code: "81"
    description: "Independent Laboratory"
```

### 5.2 Laboratory Reference Data

```yaml
lab_tests:
  basic_metabolic_panel:
    - name: Glucose
      loinc: "2345-7"
      normal_min: 70
      normal_max: 100
      unit: "mg/dL"
      critical_low: 40
      critical_high: 400
      
    - name: Sodium
      loinc: "2951-2"
      normal_min: 136
      normal_max: 145
      unit: "mmol/L"
      critical_low: 120
      critical_high: 160
      
    - name: Potassium
      loinc: "2823-3"
      normal_min: 3.5
      normal_max: 5.0
      unit: "mmol/L"
      critical_low: 2.5
      critical_high: 6.5
      
    - name: Chloride
      loinc: "2075-0"
      normal_min: 98
      normal_max: 107
      unit: "mmol/L"
      
    - name: CO2
      loinc: "2028-9"
      normal_min: 23
      normal_max: 29
      unit: "mmol/L"
      
    - name: BUN
      loinc: "3094-0"
      normal_min: 7
      normal_max: 20
      unit: "mg/dL"
      
    - name: Creatinine
      loinc: "2160-0"
      normal_min: 0.7
      normal_max: 1.3
      unit: "mg/dL"
      
    - name: Calcium
      loinc: "17861-6"
      normal_min: 8.5
      normal_max: 10.5
      unit: "mg/dL"
      
  cbc:
    - name: WBC
      loinc: "6690-2"
      normal_min: 4.5
      normal_max: 11.0
      unit: "x10^3/uL"
      
    - name: RBC
      loinc: "789-8"
      normal_min: 4.5
      normal_max: 5.9
      unit: "x10^6/uL"
      
    - name: Hemoglobin
      loinc: "718-7"
      normal_min: 13.5
      normal_max: 17.5
      unit: "g/dL"
      
    - name: Hematocrit
      loinc: "4544-3"
      normal_min: 39
      normal_max: 50
      unit: "%"
      
    - name: Platelets
      loinc: "777-3"
      normal_min: 150
      normal_max: 400
      unit: "x10^3/uL"
      
  liver_function:
    - name: ALT
      loinc: "1742-6"
      normal_min: 7
      normal_max: 56
      unit: "U/L"
      
    - name: AST
      loinc: "1920-8"
      normal_min: 10
      normal_max: 40
      unit: "U/L"
      
    - name: Bilirubin Total
      loinc: "1975-2"
      normal_min: 0.3
      normal_max: 1.2
      unit: "mg/dL"
      
    - name: Albumin
      loinc: "1751-7"
      normal_min: 3.5
      normal_max: 5.5
      unit: "g/dL"
      
  cardiac:
    - name: Troponin I
      loinc: "10839-9"
      normal_min: 0
      normal_max: 0.04
      unit: "ng/mL"
      
    - name: BNP
      loinc: "30934-4"
      normal_min: 0
      normal_max: 100
      unit: "pg/mL"
      
  other:
    - name: CRP
      loinc: "1988-5"
      normal_min: 0
      normal_max: 3.0
      unit: "mg/L"
      
    - name: HbA1c
      loinc: "4548-4"
      normal_min: 4.0
      normal_max: 5.6
      unit: "%"
```

### 5.3 Medication Reference Data

```yaml
medications:
  diabetes:
    - name: Metformin
      rxnorm: "860975"
      doses: ["500 mg", "850 mg", "1000 mg"]
      routes: ["PO"]
      frequencies: ["BID", "TID"]
      indication: "Type 2 diabetes"
      
    - name: Insulin Glargine
      rxnorm: "274783"
      doses: ["10 units", "20 units", "30 units"]
      routes: ["SubQ"]
      frequencies: ["QD"]
      indication: "Diabetes"
      
  hypertension:
    - name: Lisinopril
      rxnorm: "104376"
      doses: ["5 mg", "10 mg", "20 mg", "40 mg"]
      routes: ["PO"]
      frequencies: ["QD"]
      indication: "Hypertension"
      
    - name: Amlodipine
      rxnorm: "17767"
      doses: ["2.5 mg", "5 mg", "10 mg"]
      routes: ["PO"]
      frequencies: ["QD"]
      indication: "Hypertension"
      
    - name: Hydrochlorothiazide
      rxnorm: "5487"
      doses: ["12.5 mg", "25 mg", "50 mg"]
      routes: ["PO"]
      frequencies: ["QD"]
      indication: "Hypertension"
      
  cardiac:
    - name: Atorvastatin
      rxnorm: "83367"
      doses: ["10 mg", "20 mg", "40 mg", "80 mg"]
      routes: ["PO"]
      frequencies: ["QD"]
      indication: "Hyperlipidemia"
      
    - name: Aspirin
      rxnorm: "1191"
      doses: ["81 mg", "325 mg"]
      routes: ["PO"]
      frequencies: ["QD"]
      indication: "CAD prophylaxis"
      
    - name: Metoprolol
      rxnorm: "6918"
      doses: ["25 mg", "50 mg", "100 mg"]
      routes: ["PO"]
      frequencies: ["BID"]
      indication: "Hypertension/CAD"
      
  respiratory:
    - name: Albuterol
      rxnorm: "435"
      doses: ["90 mcg/actuation"]
      routes: ["INH"]
      frequencies: ["PRN"]
      indication: "Asthma/COPD"
      
    - name: Fluticasone
      rxnorm: "202318"
      doses: ["110 mcg/actuation", "220 mcg/actuation"]
      routes: ["INH"]
      frequencies: ["BID"]
      indication: "Asthma/COPD"
      
  infection:
    - name: Azithromycin
      rxnorm: "18631"
      doses: ["250 mg", "500 mg"]
      routes: ["PO"]
      frequencies: ["QD"]
      indication: "Bacterial infection"
      
    - name: Ceftriaxone
      rxnorm: "2193"
      doses: ["1 g", "2 g"]
      routes: ["IV"]
      frequencies: ["Q24H"]
      indication: "Bacterial infection"
      
    - name: Vancomycin
      rxnorm: "11124"
      doses: ["1 g", "1.5 g"]
      routes: ["IV"]
      frequencies: ["Q12H"]
      indication: "MRSA/serious infection"
```

### 5.4 Vital Sign Reference Ranges

```yaml
vital_ranges:
  adult:
    temperature:
      normal_min: 97.0
      normal_max: 99.5
      unit: "Fahrenheit"
    heart_rate:
      normal_min: 60
      normal_max: 100
      unit: "bpm"
    respiratory_rate:
      normal_min: 12
      normal_max: 20
      unit: "per minute"
    systolic_bp:
      normal_min: 90
      normal_max: 140
      unit: "mmHg"
    diastolic_bp:
      normal_min: 60
      normal_max: 90
      unit: "mmHg"
    spo2:
      normal_min: 95
      normal_max: 100
      unit: "percent"
      
  pediatric:
    temperature:
      normal_min: 97.0
      normal_max: 99.5
    heart_rate:
      normal_min: 70
      normal_max: 120
    respiratory_rate:
      normal_min: 20
      normal_max: 30
    systolic_bp:
      normal_min: 80
      normal_max: 120
    diastolic_bp:
      normal_min: 50
      normal_max: 80
    spo2:
      normal_min: 95
      normal_max: 100
```

### 5.5 Formulary Tier Definitions

```yaml
formulary_tiers:
  commercial_4tier:
    - tier: 1
      name: "Preferred Generic"
      copay: 10
      
    - tier: 2
      name: "Non-Preferred Generic"
      copay: 25
      
    - tier: 3
      name: "Preferred Brand"
      copay: 50
      
    - tier: 4
      name: "Non-Preferred Brand"
      copay: 80
      
    - tier: 5
      name: "Specialty"
      coinsurance: 0.25
      
  medicare_part_d:
    - tier: 1
      name: "Preferred Generic"
      copay: 5
      
    - tier: 2
      name: "Generic"
      copay: 15
      
    - tier: 3
      name: "Preferred Brand"
      copay: 47
      
    - tier: 4
      name: "Non-Preferred"
      coinsurance: 0.40
      
    - tier: 5
      name: "Specialty"
      coinsurance: 0.25
```

### 5.6 NCPDP Reject Codes (Common)

```yaml
ncpdp_reject_codes:
  - code: "70"
    description: "Product/Service Not Covered"
  - code: "75"
    description: "Prior Authorization Required"
  - code: "76"
    description: "Plan Limitations Exceeded"
  - code: "77"
    description: "Discontinued Product/Service ID Number"
  - code: "78"
    description: "Cost Exceeds Maximum"
  - code: "79"
    description: "Refill Too Soon"
  - code: "80"
    description: "Prescriber Not Found"
  - code: "81"
    description: "Claim Too Old"
  - code: "82"
    description: "Non-Matched Pharmacy Number"
  - code: "83"
    description: "Duplicate Paid/Captured Claim"
  - code: "88"
    description: "DUR Reject Error"
  - code: "MR"
    description: "Mandatory Reject"
```

### 5.7 Claim Adjustment Reason Codes (CARC)

```yaml
carc_codes:
  - code: "1"
    description: "Deductible amount"
  - code: "2"
    description: "Coinsurance amount"
  - code: "3"
    description: "Copay amount"
  - code: "4"
    description: "Procedure code inconsistent with modifier"
  - code: "45"
    description: "Charge exceeds fee schedule/maximum allowable"
  - code: "50"
    description: "Non-covered services"
  - code: "96"
    description: "Non-covered charge(s)"
  - code: "97"
    description: "Benefit included in another service payment"
```

---

## 6. Cohort Patterns

### 6.1 Clinical Cohorts (PatientSim)

#### 6.1.1 Diabetes Management Cohort

```yaml
cohort: diabetes_management
trigger_phrases:
  - "diabetic patient"
  - "diabetes"
  - "T2DM"
  - "A1C"
  - "blood sugar"
  - "metformin"
  - "insulin"

parameters:
  age_range: [45, 75]
  control_status: ["well-controlled", "moderate", "poorly-controlled"]
  duration_years: [0, 20]
  complications: ["nephropathy", "retinopathy", "neuropathy", "cardiovascular"]

disease_progression:
  stages:
    - name: "Pre-diabetes"
      a1c_range: [5.7, 6.4]
      duration: "1-5 years without intervention"
      
    - name: "New Diagnosis"
      a1c_range: [6.5, 8.5]
      medications: ["metformin"]
      
    - name: "Early Management"
      duration: "0-3 years"
      a1c_target: 7.0
      
    - name: "Medication Escalation"
      duration: "3-10 years"
      add_medications: ["SGLT2i", "GLP1-RA", "DPP4i"]
      
    - name: "Complex Regimens"
      duration: "10+ years"
      medications: ["basal insulin", "bolus insulin"]

comorbidities:
  hypertension:
    probability: 0.75
    codes: ["I10", "I11.9"]
  hyperlipidemia:
    probability: 0.70
    codes: ["E78.5", "E78.0"]
  obesity:
    probability: 0.85
    codes: ["E66.9", "E66.01"]
  ckd:
    probability: 0.40
    condition: "duration > 10 years"
    codes: ["N18.3", "N18.4"]

lab_patterns:
  well_controlled:
    a1c: [6.0, 7.0]
    fasting_glucose: [80, 120]
    egfr: [">60"]
  moderate:
    a1c: [7.0, 8.5]
    fasting_glucose: [120, 180]
    egfr: [45, 90]
  poorly_controlled:
    a1c: [8.5, 12.0]
    fasting_glucose: [180, 350]
    egfr: [30, 60]

encounter_patterns:
  routine:
    frequency: "every 3-6 months"
    visit_type: "99213-99214"
    labs: ["A1C", "BMP"]
  new_diagnosis:
    initial_visit: "99215"
    labs: ["A1C", "CMP", "lipids", "UA with micro"]
    follow_up: ["2 weeks phone", "4-6 weeks office", "3 months"]
```

#### 6.1.2 Heart Failure Cohort

```yaml
cohort: heart_failure
trigger_phrases:
  - "heart failure"
  - "CHF"
  - "HFrEF"
  - "HFpEF"
  - "ejection fraction"
  - "BNP"

parameters:
  age_range: [50, 85]
  ef_category: ["HFrEF (<40%)", "HFmrEF (40-49%)", "HFpEF (≥50%)"]
  nyha_class: [1, 2, 3, 4]

diagnosis_codes:
  primary:
    - code: I50.9
      description: "Heart failure, unspecified"
    - code: I50.2x
      description: "Systolic (HFrEF)"
    - code: I50.3x
      description: "Diastolic (HFpEF)"

medications:
  core_therapy:
    - name: "ACE-I or ARB"
      examples: ["lisinopril", "losartan"]
    - name: "Beta-blocker"
      examples: ["carvedilol", "metoprolol succinate"]
    - name: "SGLT2 inhibitor"
      examples: ["dapagliflozin", "empagliflozin"]

lab_patterns:
  bnp_by_severity:
    stable: [100, 300]
    decompensated: [500, 2000]
    severe: [2000, 10000]
```

#### 6.1.3 Sepsis Cohort

```yaml
cohort: sepsis
trigger_phrases:
  - "sepsis"
  - "septic"
  - "systemic infection"

diagnosis_codes:
  primary:
    - code: A41.9
      description: "Sepsis, unspecified organism"

vital_sign_patterns:
  sepsis_criteria:
    temperature: ["> 100.4 or < 96.8"]
    heart_rate: ["> 90"]
    respiratory_rate: ["> 20"]
    
  septic_shock:
    systolic_bp: ["< 90"]
    lactate: ["> 2.0"]

lab_patterns:
  typical:
    wbc: ["> 12 or < 4"]
    lactate: ["> 2.0"]
    creatinine: ["elevated from baseline"]

medications:
  antibiotics:
    - broad_spectrum: ["ceftriaxone", "vancomycin"]
    - timing: "within 1 hour of recognition"
```

### 6.2 Claims Cohorts (MemberSim)

#### 6.2.1 Professional Claims Cohort

```yaml
cohort: professional_claims
claim_type: PROFESSIONAL

encounter_types:
  office_visit:
    place_of_service: "11"
    cpt_codes:
      established: ["99211", "99212", "99213", "99214", "99215"]
    typical_charges:
      99213: [75, 125]
      99214: [125, 200]
```

#### 6.2.2 Facility Claims Cohort

```yaml
cohort: facility_claims
claim_type: INSTITUTIONAL

drg_examples:
  - drg: "470"
    description: "Major Joint Replacement"
    weight: 1.9079
    los_range: [2, 4]
    
  - drg: "871"
    description: "Sepsis without MV >96 hours with MCC"
    weight: 1.8739
    los_range: [5, 8]
```

### 6.3 Pharmacy Cohorts (RxMemberSim)

#### 6.3.1 DUR Alerts Cohort

```yaml
cohort: dur_review
dur_alert_types:
  drug_drug:
    code: "DD"
    examples:
      - drug1: "Warfarin"
        drug2: "NSAIDs"
        severity: 1
        message: "Increased bleeding risk"
        
  therapeutic_duplication:
    code: "TD"
    examples:
      - class: "Statins"
        max_concurrent: 1
        
  early_refill:
    code: "ER"
    threshold: "80% of days supply used"
```

---

## 7. Generation Logic

### 7.1 Identifier Generation

```yaml
identifiers:
  mrn:
    format: "MRN{sequence:08d}"
    example: "MRN00001234"
    
  member_id:
    format: "MEM{sequence:06d}"
    example: "MEM001234"
    
  claim_id:
    format: "CLM{YYYYMMDD}{sequence:06d}"
    example: "CLM20250115000001"
    
  npi:
    format: "10-digit with Luhn check"
    range: "1000000000-1999999999"
```

### 7.2 Distributions

```yaml
distributions:
  age:
    adult_default:
      bands:
        - range: [18, 30], weight: 0.20
        - range: [31, 45], weight: 0.25
        - range: [46, 60], weight: 0.25
        - range: [61, 75], weight: 0.20
        - range: [76, 90], weight: 0.10
        
  gender:
    default:
      M: 0.49
      F: 0.51
      
  plan_type:
    commercial:
      HMO: 0.35
      PPO: 0.40
      HDHP: 0.25
```

### 7.3 Reproducibility

```yaml
seed_management:
  master_seed:
    purpose: "Root seed for entire generation run"
    default: 42
    
  child_seeds:
    generation: "Derived from master seed + counter"
    isolation: "Each sub-generator gets independent seed"
```

---

## 8. Code System Mappings

### 8.1 Code System URIs

```yaml
code_system_uris:
  snomed_ct: "http://snomed.info/sct"
  loinc: "http://loinc.org"
  icd10_cm: "http://hl7.org/fhir/sid/icd-10-cm"
  cpt: "http://www.ama-assn.org/go/cpt"
  rxnorm: "http://www.nlm.nih.gov/research/umls/rxnorm"
  ndc: "http://hl7.org/fhir/sid/ndc"
  ucum: "http://unitsofmeasure.org"
```

### 8.2 GPI Prefixes

```yaml
gpi_prefixes:
  "3615": "ACE Inhibitors"
  "3617": "ARBs"
  "3940": "Statins"
  "8330": "Warfarin"
  "2710": "Metformin"
  "2720": "GLP-1 Agonists"
  "6505": "Opioids"
  "5710": "Benzodiazepines"
  "4940": "PPIs"
```

### 8.3 DAW Codes

```yaml
daw_codes:
  "0": "No Product Selection Indicated"
  "1": "Substitution Not Allowed by Prescriber"
  "2": "Patient Requested Brand"
  "3": "Pharmacist Selected"
```

### 8.4 DUR Codes

```yaml
dur_codes:
  reason_for_service:
    "MA": "Drug-Drug Interaction"
    "TD": "Therapeutic Duplication"
    "ER": "Early Refill"
    "HD": "High Dose"
    "PA": "Drug-Age Precaution"
    
  clinical_significance:
    "1": "Major - Do Not Dispense"
    "2": "Moderate - Use Caution"
    "3": "Minor - Minimal Risk"
```

---

## 9. Document Metadata

**Document**: HealthSim Domain Knowledge Base  
**Version**: 1.0  
**Created**: 2025-12-09  
**Purpose**: Session 1 deliverable for Skills-first migration  

**Source Repositories Analyzed**:
- healthsim-common (v0.2.0)
- patientsim (v0.3.0)
- membersim (v0.2.0)
- rxmembersim (v0.2.0)

**Knowledge Categories Extracted**:
1. Data Models & Schemas (9 entities)
2. Validation Rules (30+ rules)
3. Format Specifications (FHIR R4, HL7v2, X12, NCPDP)
4. Reference Data (ICD-10, CPT, LOINC, medications, labs)
5. Cohort Patterns (6 cohorts)
6. Generation Logic (identifiers, distributions, timelines)
7. Code System Mappings (15+ code systems)

**Next Steps (Session 2)**:
- Design Skills-first architecture using this knowledge base
- Create Skills file structure and templates
- Map existing cohorts to Skills format
- Plan MCP integration points

---

*End of Document*
