# Data Models Reference

Canonical entity schemas for all HealthSim data types. Extracted from Domain Knowledge Base Section 2.

## Table of Contents

- [Core Person Model](#core-person-model)
- [PatientSim Models](#patientsim-models)
  - [Patient](#patient-extends-person)
  - [Encounter](#encounter)
  - [Diagnosis](#diagnosis)
  - [Medication](#medication)
  - [LabResult](#labresult)
  - [VitalSign](#vitalsign)
  - [Order](#order)
  - [RadiologyReport](#radiologyreport)
  - [ADTEvent](#adtevent)
  - [Location](#location)
- [MemberSim Models](#membersim-models)
  - [Member](#member-extends-person)
  - [Claim](#claim)
  - [ClaimLine](#claimline)
  - [Plan](#plan)
  - [PlanServiceBenefit](#planservicebenefit)
  - [PharmacyBenefit](#pharmacybenefit)
  - [Accumulator](#accumulator)
  - [Group](#group)
- [RxMemberSim Models](#rxmembersim-models)
  - [Prescription](#prescription)
  - [PharmacyClaim](#pharmacyclaim)
  - [FormularyDrug](#formularydrug)
  - [RxMember](#rxmember)
  - [RxPlan](#rxplan)
  - [RxAccumulator](#rxaccumulator)
  - [PharmacyPriorAuth](#pharmacypriorauth)
  - [ClaimResponse](#claimresponse)
  - [DURAlert](#duralert)
  - [CopayAssistance](#copayassistance)
- [TrialSim Models](#trialsim-models)
  - [Subject](#subject-extends-person)
  - [Study](#study)
  - [Site](#site)
  - [TreatmentArm](#treatmentarm)
  - [VisitSchedule](#visitschedule)
  - [ActualVisit](#actualvisit)
  - [Randomization](#randomization)
  - [AdverseEvent](#adverseevent)
  - [Exposure](#exposure)
  - [ConcomitantMed](#concomitantmed)
  - [TrialLab](#triallab)
  - [EfficacyAssessment](#efficacyassessment)
  - [MedicalHistory](#medicalhistory)
  - [DispositionEvent](#dispositionevent)
  - [ProtocolDeviation](#protocoldeviation)
- [Cross-Product Identity Correlation](#cross-product-identity-correlation)

---

## Core Person Model

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

---

## PatientSim Models

### Patient (extends Person)

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

### Encounter

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

**Encounter Class Codes:**

| Code | Description | Typical Duration |
|------|-------------|------------------|
| I | Inpatient | 1-14 days |
| O | Outpatient | 15-60 minutes |
| E | Emergency | 1-12 hours |
| U | Urgent Care | 30 min - 2 hours |
| OBS | Observation | 8-48 hours |

### Diagnosis

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

### Medication

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

**Common Frequency Codes:**

| Code | Meaning |
|------|---------|
| QD | Once daily |
| BID | Twice daily |
| TID | Three times daily |
| QID | Four times daily |
| Q4H | Every 4 hours |
| Q6H | Every 6 hours |
| Q8H | Every 8 hours |
| Q12H | Every 12 hours |
| PRN | As needed |
| HS | At bedtime |
| AC | Before meals |
| PC | After meals |

### LabResult

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
      "description": "H=High, L=Low, HH=Critical High, LL=Critical Low, A=Abnormal, N=Normal"
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

### VitalSign

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

**Vital Sign Reference Ranges (Adult):**

| Vital | Normal Min | Normal Max | Unit |
|-------|------------|------------|------|
| temperature | 97.0 | 99.5 | °F |
| heart_rate | 60 | 100 | bpm |
| respiratory_rate | 12 | 20 | /min |
| systolic_bp | 90 | 140 | mmHg |
| diastolic_bp | 60 | 90 | mmHg |
| spo2 | 95 | 100 | % |

### Order

```json
{
  "title": "Order",
  "type": "object",
  "required": ["order_id", "patient_mrn", "order_type", "code", "status", "ordered_datetime"],
  "properties": {
    "order_id": { "type": "string" },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "order_type": {
      "type": "string",
      "enum": ["LAB", "RAD", "MEDICATION", "PROCEDURE"],
      "description": "Type of order"
    },
    "code": { "type": "string", "description": "CPT, LOINC, or other procedure code" },
    "code_system": {
      "type": "string",
      "enum": ["CPT", "LOINC", "ICD-10-PCS", "HCPCS"],
      "default": "CPT"
    },
    "description": { "type": "string" },
    "priority": {
      "type": "string",
      "enum": ["stat", "asap", "routine", "preop", "timed"],
      "default": "routine"
    },
    "status": {
      "type": "string",
      "enum": ["new", "accepted", "scheduled", "in_progress", "completed", "cancelled"],
      "default": "new"
    },
    "ordered_datetime": { "type": "string", "format": "date-time" },
    "scheduled_datetime": { "type": "string", "format": "date-time" },
    "collected_datetime": { "type": "string", "format": "date-time" },
    "resulted_datetime": { "type": "string", "format": "date-time" },
    "ordering_provider": {
      "type": "object",
      "properties": {
        "npi": { "type": "string" },
        "name": { "$ref": "#/definitions/Name" }
      }
    },
    "performing_lab": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" }
      }
    },
    "clinical_indication": { "type": "string" },
    "diagnosis_codes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "specimen_type": { "type": "string", "description": "For lab orders: Blood, Urine, etc." }
  }
}
```

**Order Types:**

| Type | Description | Common Codes |
|------|-------------|--------------|
| LAB | Laboratory orders | CPT 80000-89999, LOINC |
| RAD | Radiology/imaging orders | CPT 70000-79999 |
| MEDICATION | Medication orders | RxNorm, NDC |
| PROCEDURE | Surgical/therapeutic procedures | CPT, ICD-10-PCS |

**Order Priority Codes:**

| Priority | Description | Expected TAT |
|----------|-------------|--------------|
| stat | Immediate | 1 hour |
| asap | As soon as possible | 2-4 hours |
| routine | Standard | 24-48 hours |
| preop | Pre-operative | Before surgery |
| timed | Specific time | As scheduled |

### RadiologyReport

```json
{
  "title": "RadiologyReport",
  "type": "object",
  "required": ["accession_number", "order_id", "patient_mrn", "exam_datetime"],
  "properties": {
    "accession_number": { "type": "string" },
    "order_id": { "type": "string" },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "procedure_code": { "type": "string" },
    "procedure_name": { "type": "string" },
    "modality": {
      "type": "string",
      "enum": ["XR", "CT", "MR", "US", "NM", "PET", "FL"],
      "description": "XR=X-ray, CT=CT scan, MR=MRI, US=Ultrasound, NM=Nuclear Med, PET=PET scan, FL=Fluoroscopy"
    },
    "exam_datetime": { "type": "string", "format": "date-time" },
    "reported_datetime": { "type": "string", "format": "date-time" },
    "radiologist": {
      "type": "object",
      "properties": {
        "npi": { "type": "string" },
        "name": { "$ref": "#/definitions/Name" }
      }
    },
    "clinical_indication": { "type": "string" },
    "comparison": { "type": "string", "description": "Prior studies compared" },
    "technique": { "type": "string" },
    "findings": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "Findings by anatomic region"
    },
    "impression": { "type": "string" },
    "recommendations": { "type": "string" },
    "critical_finding": { "type": "boolean", "default": false },
    "critical_acknowledged_by": { "type": "string" },
    "critical_acknowledged_datetime": { "type": "string", "format": "date-time" }
  }
}
```

**Radiology Modality Codes:**

| Code | Description | Examples |
|------|-------------|----------|
| XR | X-ray/Radiograph | Chest X-ray, bone films |
| CT | Computed Tomography | CT head, CT chest |
| MR | Magnetic Resonance | MRI brain, MRI spine |
| US | Ultrasound | Abdominal US, Echo |
| NM | Nuclear Medicine | Bone scan, thyroid uptake |
| PET | Positron Emission Tomography | PET/CT |
| FL | Fluoroscopy | Swallow study, angiography |

### ADTEvent

```json
{
  "title": "ADTEvent",
  "type": "object",
  "required": ["event_type", "event_time", "patient_mrn", "encounter_id"],
  "properties": {
    "event_id": { "type": "string" },
    "event_type": {
      "type": "string",
      "enum": ["A01", "A02", "A03", "A04", "A08", "A11", "A13"],
      "description": "HL7 ADT event type"
    },
    "event_time": { "type": "string", "format": "date-time" },
    "patient_mrn": { "type": "string" },
    "encounter_id": { "type": "string" },
    "patient_class": {
      "type": "string",
      "enum": ["I", "O", "E", "P", "R", "B", "U", "OBS"],
      "description": "I=Inpatient, O=Outpatient, E=Emergency, P=Preadmit, R=Recurring, B=Obstetrics, U=Unknown, OBS=Observation"
    },
    "admission_type": {
      "type": "string",
      "enum": ["E", "R", "U", "C"],
      "description": "E=Emergency, R=Routine, U=Urgent, C=Elective"
    },
    "admission_source": {
      "type": "string",
      "description": "Source of admission (1-9)"
    },
    "location": { "$ref": "#/definitions/Location" },
    "prior_location": { "$ref": "#/definitions/Location" },
    "discharge_disposition": { "type": "string" },
    "attending_provider": {
      "type": "object",
      "properties": {
        "npi": { "type": "string" },
        "name": { "$ref": "#/definitions/Name" }
      }
    },
    "transfer_reason": { "type": "string" },
    "cancellation_reason": { "type": "string" },
    "description": { "type": "string" }
  }
}
```

**ADT Event Types:**

| Event | Name | Description |
|-------|------|-------------|
| A01 | Admit | Patient admission notification |
| A02 | Transfer | Patient transferred between locations |
| A03 | Discharge | Patient discharged or visit ended |
| A04 | Register | Outpatient/preadmit registration |
| A08 | Update | Patient information update |
| A11 | Cancel Admit | Cancel a previous admission |
| A13 | Cancel Discharge | Cancel a previous discharge |

### Location

```json
{
  "title": "Location",
  "type": "object",
  "properties": {
    "facility": { "type": "string", "description": "Facility/hospital code" },
    "building": { "type": "string" },
    "floor": { "type": "string" },
    "point_of_care": {
      "type": "string",
      "description": "Unit code (ED, ICU, MED, etc.)"
    },
    "room": { "type": "string" },
    "bed": { "type": "string" },
    "location_type": {
      "type": "string",
      "enum": ["nursing_unit", "room", "bed", "clinic", "department", "operating_room"],
      "default": "nursing_unit"
    },
    "location_status": {
      "type": "string",
      "enum": ["active", "housekeeping", "occupied", "unoccupied", "contaminated", "closed"],
      "default": "active"
    }
  }
}
```

**Hospital Unit Codes:**

| Code | Unit Name | Type |
|------|-----------|------|
| ED | Emergency Department | Emergency |
| ICU | Intensive Care Unit | Critical |
| CCU | Cardiac Care Unit | Critical |
| MICU | Medical ICU | Critical |
| SICU | Surgical ICU | Critical |
| NICU | Neonatal ICU | Critical |
| SDU | Step-Down Unit | Intermediate |
| TELE | Telemetry | Intermediate |
| MED | Medical/Surgical | Acute |
| SURG | Surgical | Acute |
| PEDS | Pediatrics | Acute |
| OB | Obstetrics | Acute |
| PSYCH | Psychiatry | Behavioral |
| REHAB | Rehabilitation | Post-Acute |
| OBS | Observation | Observation |
| OR | Operating Room | Procedural |
| PACU | Post-Anesthesia Care | Recovery |
| L&D | Labor & Delivery | OB |

---

## MemberSim Models

### Member (extends Person)

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

### Claim

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

### ClaimLine

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

### Plan

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
      "enum": ["HMO", "PPO", "EPO", "POS", "HDHP", "INDEMNITY"]
    },
    "metal_tier": {
      "type": "string",
      "enum": ["bronze", "silver", "gold", "platinum"],
      "description": "ACA metal tier based on actuarial value"
    },
    "coverage_type": {
      "type": "string",
      "enum": ["MEDICAL", "DENTAL", "VISION", "RX"],
      "default": "MEDICAL"
    },
    "network_requirement": {
      "type": "string",
      "enum": ["in_network_only", "in_network_preferred"],
      "description": "How network affects coverage"
    },
    "cost_sharing": {
      "type": "object",
      "properties": {
        "in_network": { "$ref": "#/definitions/CostSharingTier" },
        "out_of_network": { "$ref": "#/definitions/CostSharingTier" }
      }
    },
    "copays": {
      "type": "object",
      "properties": {
        "pcp_visit": { "type": "number" },
        "specialist_visit": { "type": "number" },
        "urgent_care": { "type": "number" },
        "emergency_room": { "type": "number" },
        "telehealth": { "type": "number" },
        "mental_health_outpatient": { "type": "number" },
        "physical_therapy": { "type": "number" }
      }
    },
    "hospital": {
      "type": "object",
      "properties": {
        "inpatient_copay_per_admission": { "type": "number" },
        "inpatient_coinsurance": { "type": "integer" },
        "outpatient_surgery_copay": { "type": "number" },
        "ambulance_copay": { "type": "number" }
      }
    },
    "pcp_required": { "type": "boolean", "default": false },
    "referral_required": { "type": "boolean", "default": false },
    "hsa_eligible": { "type": "boolean", "default": false },
    "hsa": {
      "type": "object",
      "properties": {
        "employer_contribution_individual": { "type": "number" },
        "employer_contribution_family": { "type": "number" },
        "individual_contribution_limit": { "type": "number" },
        "family_contribution_limit": { "type": "number" },
        "catch_up_contribution_55_plus": { "type": "number" }
      }
    },
    "effective_date": { "type": "string", "format": "date" },
    "termination_date": { "type": "string", "format": "date" }
  }
}
```

**CostSharingTier Definition:**

```json
{
  "title": "CostSharingTier",
  "type": "object",
  "properties": {
    "individual_deductible": { "type": "number" },
    "family_deductible": { "type": "number" },
    "individual_oop_max": { "type": "number" },
    "family_oop_max": { "type": "number" },
    "coinsurance_percent": { "type": "integer", "description": "20 = 20%" },
    "deductible_applies_to_copays": { "type": "boolean", "default": false }
  }
}
```

**Plan Type Characteristics:**

| Plan Type | PCP Required | Referral Required | OON Coverage | Deductible |
|-----------|--------------|-------------------|--------------|------------|
| HMO | Yes | Yes | Emergency only | Often $0 |
| PPO | No | No | Yes (higher cost) | Moderate |
| EPO | No | No | Emergency only | Moderate |
| POS | Yes | Yes (in-network) | Yes (higher cost) | Moderate |
| HDHP | No | No | Yes | High (IRS minimum) |

### PlanServiceBenefit

Service-level benefit configuration:

```json
{
  "title": "PlanServiceBenefit",
  "type": "object",
  "required": ["plan_code", "service_type", "network_tier", "cost_sharing_type"],
  "properties": {
    "plan_code": { "type": "string" },
    "service_type": {
      "type": "string",
      "enum": [
        "pcp_visit", "specialist_visit", "urgent_care", "emergency_room",
        "inpatient", "outpatient_surgery", "lab_work", "xray", "advanced_imaging",
        "mental_health_outpatient", "mental_health_inpatient", "physical_therapy",
        "preventive", "telehealth", "ambulance", "skilled_nursing", "home_health"
      ]
    },
    "network_tier": {
      "type": "string",
      "enum": ["in_network", "out_of_network", "tier_1", "tier_2", "tier_3"]
    },
    "cost_sharing_type": {
      "type": "string",
      "enum": ["copay", "coinsurance", "covered_100"]
    },
    "cost_sharing_amount": {
      "type": "number",
      "description": "Dollar amount for copay, percentage for coinsurance"
    },
    "deductible_applies": { "type": "boolean", "default": true },
    "annual_limit": { "type": "integer", "description": "Visit limit per year" },
    "prior_auth_required": { "type": "boolean", "default": false }
  }
}
```

### PharmacyBenefit

Pharmacy tier structure:

```json
{
  "title": "PharmacyBenefit",
  "type": "object",
  "required": ["plan_code", "tier", "tier_name"],
  "properties": {
    "plan_code": { "type": "string" },
    "tier": { "type": "integer", "minimum": 1, "maximum": 5 },
    "tier_name": { "type": "string" },
    "tier_description": { "type": "string" },
    "retail_30_copay": { "type": "number" },
    "retail_90_copay": { "type": "number" },
    "mail_90_copay": { "type": "number" },
    "specialty_coinsurance": { "type": "integer", "description": "Percentage" },
    "specialty_max": { "type": "number", "description": "Maximum copay for specialty" },
    "deductible_applies": { "type": "boolean", "default": false },
    "quantity_limit_days": { "type": "integer" },
    "prior_auth_common": { "type": "boolean", "default": false },
    "step_therapy_common": { "type": "boolean", "default": false }
  }
}
```

**Standard Pharmacy Tiers:**

| Tier | Name | Typical Copay | Description |
|------|------|---------------|-------------|
| 1 | Preferred Generic | $10-15 | Low-cost generics |
| 2 | Non-Preferred Generic | $20-30 | Other generics |
| 3 | Preferred Brand | $40-60 | Formulary brand drugs |
| 4 | Non-Preferred Brand | $75-100 | Non-formulary brands |
| 5 | Specialty | 20-30% | Biologics, specialty injectables |

### Accumulator

```json
{
  "title": "Accumulator",
  "type": "object",
  "required": ["member_id", "plan_code", "plan_year", "accumulator_type"],
  "properties": {
    "accumulator_id": { "type": "string" },
    "member_id": { "type": "string" },
    "plan_code": { "type": "string" },
    "plan_year": { "type": "integer" },
    "accumulator_type": {
      "type": "string",
      "enum": ["deductible", "oop_max", "rx_deductible", "rx_oop_max"],
      "description": "Type of accumulator being tracked"
    },
    "individual_applied": { "type": "number", "default": 0 },
    "individual_limit": { "type": "number" },
    "family_applied": { "type": "number", "default": 0 },
    "family_limit": { "type": "number" },
    "as_of_date": { "type": "string", "format": "date" },
    "last_updated": { "type": "string", "format": "date-time" }
  }
}
```

**Accumulator Types:**

| Type | Description | Resets |
|------|-------------|--------|
| deductible | Medical deductible | Jan 1 |
| oop_max | Medical out-of-pocket maximum | Jan 1 |
| rx_deductible | Pharmacy deductible (if separate) | Jan 1 |
| rx_oop_max | Pharmacy out-of-pocket maximum | Jan 1 |

### Group

Employer group configuration:

```json
{
  "title": "Group",
  "type": "object",
  "required": ["group_id", "group_name", "effective_date"],
  "properties": {
    "group_id": { "type": "string" },
    "group_name": { "type": "string" },
    "tax_id": { "type": "string", "pattern": "^\\d{2}-\\d{7}$" },
    "address": { "$ref": "#/definitions/Address" },
    "effective_date": { "type": "string", "format": "date" },
    "termination_date": { "type": "string", "format": "date" },
    "contact_name": { "type": "string" },
    "contact_email": { "type": "string", "format": "email" },
    "contact_phone": { "type": "string" },
    "offered_plans": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Plan codes offered to this group"
    }
  }
}
```

---

## RxMemberSim Models

### Prescription

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

**DAW Codes:**

| Code | Description |
|------|-------------|
| 0 | No Product Selection Indicated |
| 1 | Substitution Not Allowed by Prescriber |
| 2 | Patient Requested Brand |
| 3 | Pharmacist Selected |
| 4 | Generic Not Available |
| 5 | Brand Dispensed as Generic |
| 6 | Override |
| 7 | Brand Mandated by Law |
| 8 | Generic Not Available in Marketplace |
| 9 | Other |

### PharmacyClaim

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

### FormularyDrug

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

**Formulary Tier Structure:**

| Tier | Name | Typical Copay |
|------|------|---------------|
| 1 | Preferred Generic | $10 |
| 2 | Non-Preferred Generic | $25 |
| 3 | Preferred Brand | $50 |
| 4 | Non-Preferred Brand | $80 |
| 5 | Specialty | 25% coinsurance |

### RxMember

Pharmacy member with PBM-specific identifiers:

```json
{
  "title": "RxMember",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "required": ["member_id", "cardholder_id", "bin", "pcn", "group_number", "rx_plan_code", "coverage_start"],
  "properties": {
    "member_id": { "type": "string" },
    "subscriber_id": { "type": "string" },
    "cardholder_id": {
      "type": "string",
      "description": "ID printed on pharmacy card"
    },
    "person_code": {
      "type": "string",
      "enum": ["01", "02", "03", "04", "05", "06", "07", "08", "09"],
      "description": "01=Cardholder, 02=Spouse, 03+=Dependents"
    },
    "relationship_code": {
      "type": "string",
      "enum": ["1", "2", "3", "4"],
      "description": "1=Cardholder, 2=Spouse, 3=Dependent, 4=Other"
    },
    "bin": {
      "type": "string",
      "pattern": "^\\d{6}$",
      "description": "Bank Identification Number (6 digits)"
    },
    "pcn": {
      "type": "string",
      "description": "Processor Control Number"
    },
    "group_number": { "type": "string" },
    "rx_plan_code": { "type": "string" },
    "coverage_start": { "type": "string", "format": "date" },
    "coverage_end": { "type": "string", "format": "date" },
    "mail_order_eligible": { "type": "boolean", "default": true },
    "specialty_eligible": { "type": "boolean", "default": true }
  }
}
```

**Person Code Values:**

| Code | Description |
|------|-------------|
| 01 | Cardholder/Subscriber |
| 02 | Spouse |
| 03 | Child 1 |
| 04 | Child 2 |
| 05 | Child 3 |
| 06-09 | Additional dependents |

### RxPlan

Pharmacy benefit plan configuration:

```json
{
  "title": "RxPlan",
  "type": "object",
  "required": ["rx_plan_code", "rx_plan_name"],
  "properties": {
    "rx_plan_code": { "type": "string" },
    "rx_plan_name": { "type": "string" },
    "formulary_id": { "type": "string" },
    "plan_type": {
      "type": "string",
      "enum": ["commercial", "medicare_part_d", "medicaid", "exchange"],
      "default": "commercial"
    },
    "tier_count": { "type": "integer", "minimum": 3, "maximum": 6, "default": 5 },
    "deductible": {
      "type": "object",
      "properties": {
        "individual": { "type": "number" },
        "family": { "type": "number" },
        "applies_to_specialty": { "type": "boolean", "default": true }
      }
    },
    "oop_max": {
      "type": "object",
      "properties": {
        "individual": { "type": "number" },
        "family": { "type": "number" },
        "combined_with_medical": { "type": "boolean", "default": false }
      }
    },
    "tier_copays": {
      "type": "object",
      "properties": {
        "tier_1_retail_30": { "type": "number" },
        "tier_1_retail_90": { "type": "number" },
        "tier_1_mail_90": { "type": "number" },
        "tier_2_retail_30": { "type": "number" },
        "tier_2_retail_90": { "type": "number" },
        "tier_2_mail_90": { "type": "number" },
        "tier_3_retail_30": { "type": "number" },
        "tier_3_retail_90": { "type": "number" },
        "tier_3_mail_90": { "type": "number" },
        "tier_4_retail_30": { "type": "number" },
        "tier_4_retail_90": { "type": "number" },
        "tier_4_mail_90": { "type": "number" },
        "tier_5_coinsurance": { "type": "integer" },
        "tier_5_max": { "type": "number" }
      }
    },
    "specialty_pharmacy_required": { "type": "boolean", "default": true },
    "mail_order_mandatory_maintenance": { "type": "boolean", "default": false },
    "daw_penalty": {
      "type": "object",
      "properties": {
        "applies": { "type": "boolean", "default": true },
        "penalty_type": { "type": "string", "enum": ["difference", "percentage", "flat"] },
        "penalty_amount": { "type": "number" }
      }
    },
    "effective_date": { "type": "string", "format": "date" },
    "termination_date": { "type": "string", "format": "date" }
  }
}
```

### RxAccumulator

Pharmacy-specific accumulator tracking:

```json
{
  "title": "RxAccumulator",
  "type": "object",
  "required": ["member_id", "rx_plan_code", "plan_year", "accumulator_type"],
  "properties": {
    "accumulator_id": { "type": "string" },
    "member_id": { "type": "string" },
    "rx_plan_code": { "type": "string" },
    "plan_year": { "type": "integer" },
    "accumulator_type": {
      "type": "string",
      "enum": ["rx_deductible", "rx_oop_max", "specialty_oop", "brand_penalty", "troop"],
      "description": "Type of pharmacy accumulator"
    },
    "individual_applied": { "type": "number", "default": 0 },
    "individual_limit": { "type": "number" },
    "family_applied": { "type": "number", "default": 0 },
    "family_limit": { "type": "number" },
    "as_of_date": { "type": "string", "format": "date" },
    "last_claim_date": { "type": "string", "format": "date" },
    "last_updated": { "type": "string", "format": "date-time" }
  }
}
```

**Pharmacy Accumulator Types:**

| Type | Description | Notes |
|------|-------------|-------|
| rx_deductible | Pharmacy deductible | May be separate from medical |
| rx_oop_max | Pharmacy out-of-pocket max | May be separate from medical |
| specialty_oop | Specialty drug OOP | Some plans track separately |
| brand_penalty | Brand when generic available | DAW penalty accumulator |
| troop | True Out-of-Pocket (Medicare) | For Part D coverage phases |

### PharmacyPriorAuth

Pharmacy prior authorization request and response:

```json
{
  "title": "PharmacyPriorAuth",
  "type": "object",
  "required": ["pa_id", "member_id", "ndc", "status", "request_date"],
  "properties": {
    "pa_id": { "type": "string" },
    "member_id": { "type": "string" },
    "prescriber_npi": { "type": "string" },
    "prescriber_name": { "type": "string" },
    "pharmacy_npi": { "type": "string" },
    "ndc": { "type": "string" },
    "drug_name": { "type": "string" },
    "gpi": { "type": "string" },
    "quantity_requested": { "type": "number" },
    "days_supply_requested": { "type": "integer" },
    "diagnosis_codes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "pa_type": {
      "type": "string",
      "enum": ["formulary_exception", "step_therapy_override", "quantity_limit", "age_edit", "clinical_pa"],
      "default": "clinical_pa"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "approved", "denied", "cancelled", "expired"],
      "default": "pending"
    },
    "urgency": {
      "type": "string",
      "enum": ["standard", "urgent", "expedited"],
      "default": "standard"
    },
    "request_date": { "type": "string", "format": "date" },
    "decision_date": { "type": "string", "format": "date" },
    "effective_date": { "type": "string", "format": "date" },
    "expiration_date": { "type": "string", "format": "date" },
    "approved_quantity": { "type": "number" },
    "approved_days_supply": { "type": "integer" },
    "approved_refills": { "type": "integer" },
    "denial_reason": { "type": "string" },
    "denial_code": { "type": "string" },
    "appeal_deadline": { "type": "string", "format": "date" },
    "clinical_notes": { "type": "string" },
    "supporting_documentation": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

**PA Status Workflow:**

| Status | Description | Next States |
|--------|-------------|-------------|
| pending | Request submitted, awaiting review | approved, denied, cancelled |
| approved | PA approved, ready for use | expired |
| denied | PA denied | (appeal possible) |
| cancelled | Request withdrawn | - |
| expired | Approval period ended | - |

### ClaimResponse

Pharmacy claim adjudication response:

```json
{
  "title": "ClaimResponse",
  "type": "object",
  "required": ["claim_id", "response_status"],
  "properties": {
    "claim_id": { "type": "string" },
    "authorization_number": { "type": "string" },
    "response_status": {
      "type": "string",
      "enum": ["A", "R", "P", "D"],
      "description": "A=Accepted, R=Rejected, P=Paid with changes, D=Duplicate"
    },
    "reject_codes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "NCPDP reject codes if rejected"
    },
    "reject_messages": {
      "type": "array",
      "items": { "type": "string" }
    },
    "ingredient_cost_paid": { "type": "number" },
    "dispensing_fee_paid": { "type": "number" },
    "incentive_amount_paid": { "type": "number" },
    "flat_sales_tax_paid": { "type": "number" },
    "percentage_sales_tax_paid": { "type": "number" },
    "total_amount_paid": { "type": "number" },
    "patient_pay_amount": { "type": "number" },
    "copay_amount": { "type": "number" },
    "coinsurance_amount": { "type": "number" },
    "deductible_amount": { "type": "number" },
    "amount_exceeding_periodic_benefit_max": { "type": "number" },
    "basis_of_reimbursement": {
      "type": "string",
      "enum": ["MAC", "AWP", "WAC", "340B", "UC", "OTHER"]
    },
    "formulary_tier": { "type": "integer" },
    "dur_alerts": {
      "type": "array",
      "items": { "$ref": "#/definitions/DURAlert" }
    },
    "message": { "type": "string" },
    "additional_messages": {
      "type": "array",
      "items": { "type": "string" }
    },
    "help_desk_phone": { "type": "string" }
  }
}
```

### DURAlert

Drug Utilization Review alert:

```json
{
  "title": "DURAlert",
  "type": "object",
  "required": ["alert_type", "severity"],
  "properties": {
    "alert_type": {
      "type": "string",
      "enum": ["DD", "TD", "ER", "HD", "LD", "DA", "DG", "DC", "MX", "PA"],
      "description": "DUR alert type code"
    },
    "severity": {
      "type": "string",
      "enum": ["informational", "warning", "reject"],
      "default": "warning"
    },
    "description": { "type": "string" },
    "clinical_significance": {
      "type": "string",
      "enum": ["1", "2", "3"],
      "description": "1=Major, 2=Moderate, 3=Minor"
    },
    "conflicting_drug": {
      "type": "object",
      "properties": {
        "ndc": { "type": "string" },
        "drug_name": { "type": "string" },
        "last_fill_date": { "type": "string", "format": "date" }
      }
    },
    "reason_for_service_code": {
      "type": "string",
      "description": "NCPDP Reason for Service code"
    },
    "professional_service_code": {
      "type": "string",
      "description": "NCPDP Professional Service code"
    },
    "result_of_service_code": {
      "type": "string",
      "description": "NCPDP Result of Service code"
    },
    "message": { "type": "string" },
    "recommendation": { "type": "string" }
  }
}
```

**DUR Alert Types:**

| Code | Type | Description |
|------|------|-------------|
| DD | Drug-Drug | Interaction between two medications |
| TD | Therapeutic Duplication | Multiple drugs in same class |
| ER | Early Refill | Before 75-80% of supply used |
| HD | High Dose | Exceeds max recommended dose |
| LD | Low Dose | Below therapeutic dose |
| DA | Drug-Age | Age precaution (pediatric/geriatric) |
| DG | Drug-Gender | Gender-specific precaution |
| DC | Drug-Disease | Contraindicated condition |
| MX | Drug-Pregnancy | Pregnancy category warning |
| PA | Prior Auth Required | PA edit triggered |

### CopayAssistance

Manufacturer copay assistance program:

```json
{
  "title": "CopayAssistance",
  "type": "object",
  "required": ["program_id", "program_name", "ndc_list"],
  "properties": {
    "program_id": { "type": "string" },
    "program_name": { "type": "string" },
    "manufacturer": { "type": "string" },
    "program_bin": { "type": "string" },
    "program_pcn": { "type": "string" },
    "program_group": { "type": "string" },
    "ndc_list": {
      "type": "array",
      "items": { "type": "string" }
    },
    "max_benefit_per_fill": { "type": "number" },
    "max_annual_benefit": { "type": "number" },
    "min_patient_pay": {
      "type": "number",
      "description": "Minimum patient responsibility after assistance"
    },
    "eligibility": {
      "type": "object",
      "properties": {
        "commercial_only": { "type": "boolean", "default": true },
        "medicare_excluded": { "type": "boolean", "default": true },
        "medicaid_excluded": { "type": "boolean", "default": true },
        "income_limit": { "type": "number" },
        "age_min": { "type": "integer" },
        "age_max": { "type": "integer" }
      }
    },
    "effective_date": { "type": "string", "format": "date" },
    "expiration_date": { "type": "string", "format": "date" },
    "terms_url": { "type": "string", "format": "uri" }
  }
}
```

---

## Required Fields Summary

| Entity | Required Fields |
|--------|-----------------|
| Person | id, name.given_name, name.family_name, birth_date, gender |
| Patient | Person fields + mrn |
| Encounter | encounter_id, patient_mrn, class_code, status, admission_time |
| Diagnosis | code, description, patient_mrn, diagnosed_date |
| Medication | name, dose, route, frequency, patient_mrn, start_date |
| LabResult | test_name, value, patient_mrn, collected_time |
| Order | order_id, patient_mrn, order_type, code, status, ordered_datetime |
| RadiologyReport | accession_number, order_id, patient_mrn, exam_datetime |
| ADTEvent | event_type, event_time, patient_mrn, encounter_id |
| Group | group_id, group_name, effective_date |
| Plan | plan_code, plan_name, plan_type |
| PlanServiceBenefit | plan_code, service_type, network_tier, cost_sharing_type |
| PharmacyBenefit | plan_code, tier, tier_name |
| Member | Person fields + member_id, group_id, coverage_start, plan_code |
| Accumulator | member_id, plan_code, plan_year, accumulator_type |
| Claim | claim_id, claim_type, member_id, provider_npi, service_date, principal_diagnosis |
| PharmacyClaim | claim_id, service_date, pharmacy_npi, member_id, ndc, quantity_dispensed |
| Prescription | rx_number, patient_mrn, prescriber_npi, ndc, quantity, days_supply, date_written |
| FormularyDrug | ndc, drug_name, tier |
| RxMember | member_id, cardholder_id, bin, pcn, group_number, rx_plan_code, coverage_start |
| RxPlan | rx_plan_code, plan_name, plan_type |
| RxAccumulator | member_id, rx_plan_code, plan_year |
| PharmacyPriorAuth | pa_id, member_id, ndc, status, request_date |
| ClaimResponse | claim_id, transaction_response_status, response_datetime |
| DURAlert | alert_id, claim_id, dur_code, dur_type, clinical_significance |
| CopayAssistance | program_id, member_id, ndc, program_type, program_start |

## Referential Integrity

| Source | Target | Required |
|--------|--------|----------|
| Encounter.patient_mrn | Patient.mrn | Yes |
| Diagnosis.patient_mrn | Patient.mrn | Yes |
| Diagnosis.encounter_id | Encounter.encounter_id | No |
| Medication.patient_mrn | Patient.mrn | Yes |
| LabResult.patient_mrn | Patient.mrn | Yes |
| LabResult.encounter_id | Encounter.encounter_id | No |
| Order.patient_mrn | Patient.mrn | Yes |
| Order.encounter_id | Encounter.encounter_id | No |
| RadiologyReport.patient_mrn | Patient.mrn | Yes |
| RadiologyReport.order_id | Order.order_id | Yes |
| ADTEvent.patient_mrn | Patient.mrn | Yes |
| ADTEvent.encounter_id | Encounter.encounter_id | Yes |
| Member.group_id | Group.group_id | Yes |
| Member.plan_code | Plan.plan_code | Yes |
| Member.subscriber_id | Member.member_id | No (dependents only) |
| PlanServiceBenefit.plan_code | Plan.plan_code | Yes |
| PharmacyBenefit.plan_code | Plan.plan_code | Yes |
| Accumulator.member_id | Member.member_id | Yes |
| Accumulator.plan_code | Plan.plan_code | Yes |
| Claim.member_id | Member.member_id | Yes |
| PharmacyClaim.member_id | Member.member_id | Yes |
| Prescription.patient_mrn | Patient.mrn | Yes |
| Prescription.encounter_id | Encounter.encounter_id | No |
| RxMember.rx_plan_code | RxPlan.rx_plan_code | Yes |
| RxMember.subscriber_id | RxMember.member_id | No (dependents only) |
| RxAccumulator.member_id | RxMember.member_id | Yes |
| RxAccumulator.rx_plan_code | RxPlan.rx_plan_code | Yes |
| PharmacyPriorAuth.member_id | RxMember.member_id | Yes |
| PharmacyPriorAuth.ndc | FormularyDrug.ndc | No |
| ClaimResponse.claim_id | PharmacyClaim.claim_id | Yes |
| DURAlert.claim_id | PharmacyClaim.claim_id | Yes |
| CopayAssistance.member_id | RxMember.member_id | Yes |
| CopayAssistance.ndc | FormularyDrug.ndc | No |

---

## TrialSim Models

TrialSim entities support clinical trial data generation with CDISC compliance. The Subject entity extends the core Person model, following the same pattern as Patient, Member, and RxMember.

### Entity Hierarchy

```
Study
├── Site (1:M)
├── TreatmentArm (1:M)
├── VisitSchedule (1:M)
└── Subject (via Site, 1:M)
    ├── Randomization (1:1)
    ├── ActualVisit (1:M)
    ├── AdverseEvent (1:M)
    ├── Exposure (1:M)
    ├── ConcomitantMed (1:M)
    ├── TrialLab (1:M)
    ├── EfficacyAssessment (1:M)
    ├── MedicalHistory (1:M)
    ├── ProtocolDeviation (1:M)
    └── DispositionEvent (1:M)
```

### Subject (extends Person)

Trial participant. Extends the core Person model with trial-specific identifiers.

```json
{
  "title": "Subject",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "required": ["subject_id", "study_id", "site_id", "informed_consent_date"],
  "properties": {
    "subject_id": {
      "type": "string",
      "description": "Subject identifier within site",
      "pattern": "^[0-9]{4}$"
    },
    "usubjid": {
      "type": "string",
      "description": "Unique Subject ID: STUDYID-SITEID-SUBJID (CDISC format)",
      "pattern": "^[A-Z0-9-]+-[0-9]+-[0-9]+$"
    },
    "study_id": {
      "type": "string",
      "description": "Reference to Study"
    },
    "site_id": {
      "type": "string",
      "description": "Reference to Site"
    },
    "patient_ref": {
      "type": "string",
      "description": "Reference to PatientSim Patient (MRN) for medical history linkage"
    },
    "screening_id": {
      "type": "string",
      "description": "Pre-randomization screening number"
    },
    "screening_date": {
      "type": "string",
      "format": "date"
    },
    "informed_consent_date": {
      "type": "string",
      "format": "date",
      "description": "Maps to RFICDTC in SDTM"
    },
    "randomization_date": {
      "type": "string",
      "format": "date"
    },
    "treatment_arm": {
      "type": "string",
      "description": "Assigned treatment arm code"
    },
    "status": {
      "type": "string",
      "enum": ["Screening", "Screen Failed", "Enrolled", "Randomized", "Active", "Completed", "Discontinued", "Lost to Follow-up", "Withdrawn"]
    },
    "race": {
      "type": "string",
      "enum": ["American Indian or Alaska Native", "Asian", "Black or African American", "Native Hawaiian or Other Pacific Islander", "White", "Multiple", "Unknown", "Not Reported"],
      "description": "FDA race categories"
    },
    "ethnicity": {
      "type": "string",
      "enum": ["Hispanic or Latino", "Not Hispanic or Latino", "Unknown", "Not Reported"]
    }
  }
}
```

**USUBJID Construction:**

| Component | Source | Example |
|-----------|--------|---------|
| STUDYID | Study.study_id | ABC-123-001 |
| SITEID | Site.site_id | 001 |
| SUBJID | Subject.subject_id | 0001 |
| **USUBJID** | Concatenated | ABC-123-001-001-0001 |

### Study

Clinical trial protocol definition.

```json
{
  "title": "Study",
  "type": "object",
  "required": ["study_id", "protocol_title", "phase", "status"],
  "properties": {
    "study_id": {
      "type": "string",
      "description": "Unique study identifier (maps to STUDYID)",
      "pattern": "^[A-Z0-9-]+$"
    },
    "protocol_title": { "type": "string" },
    "protocol_number": { "type": "string" },
    "phase": {
      "type": "string",
      "enum": ["Phase 1", "Phase 1/2", "Phase 2", "Phase 2/3", "Phase 3", "Phase 4"]
    },
    "therapeutic_area": { "type": "string" },
    "indication": { "type": "string" },
    "sponsor": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["Planning", "Recruiting", "Active", "Completed", "Terminated", "Suspended"]
    },
    "study_type": {
      "type": "string",
      "enum": ["Interventional", "Observational", "Expanded Access"],
      "default": "Interventional"
    },
    "design": {
      "type": "object",
      "properties": {
        "allocation": {
          "type": "string",
          "enum": ["Randomized", "Non-Randomized", "N/A"]
        },
        "intervention_model": {
          "type": "string",
          "enum": ["Parallel", "Crossover", "Sequential", "Single Group", "Factorial"]
        },
        "masking": {
          "type": "string",
          "enum": ["None (Open Label)", "Single", "Double", "Triple", "Quadruple"]
        },
        "primary_purpose": {
          "type": "string",
          "enum": ["Treatment", "Prevention", "Diagnostic", "Supportive Care", "Screening"]
        }
      }
    },
    "enrollment_target": { "type": "integer", "minimum": 1 },
    "start_date": { "type": "string", "format": "date" },
    "primary_completion_date": { "type": "string", "format": "date" },
    "study_completion_date": { "type": "string", "format": "date" }
  }
}
```

### Site

Investigational site conducting the trial.

```json
{
  "title": "Site",
  "type": "object",
  "required": ["site_id", "study_id", "site_name", "country"],
  "properties": {
    "site_id": {
      "type": "string",
      "description": "Site number within study",
      "pattern": "^[0-9]{3,4}$"
    },
    "study_id": { "type": "string" },
    "site_name": { "type": "string" },
    "facility_id": {
      "type": "string",
      "description": "Reference to NetworkSim Facility (cross-product)"
    },
    "country": {
      "type": "string",
      "pattern": "^[A-Z]{2,3}$",
      "description": "ISO 3166-1 country code"
    },
    "region": { "type": "string" },
    "principal_investigator": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "npi": { "type": "string", "pattern": "^[0-9]{10}$" },
        "specialty": { "type": "string" }
      }
    },
    "status": {
      "type": "string",
      "enum": ["Selected", "In Startup", "Active", "Closed", "Terminated"]
    },
    "activation_date": { "type": "string", "format": "date" },
    "enrollment_target": { "type": "integer" },
    "enrollment_actual": { "type": "integer" }
  }
}
```

### TreatmentArm

Study arm definition.

```json
{
  "title": "TreatmentArm",
  "type": "object",
  "required": ["arm_code", "arm_name", "arm_type", "study_id"],
  "properties": {
    "arm_code": {
      "type": "string",
      "description": "Short code (maps to ARM in SDTM)"
    },
    "arm_name": {
      "type": "string",
      "description": "Full description (maps to ARMCD)"
    },
    "arm_type": {
      "type": "string",
      "enum": ["Experimental", "Active Comparator", "Placebo Comparator", "Sham Comparator", "No Intervention"]
    },
    "study_id": { "type": "string" },
    "randomization_ratio": { "type": "number", "default": 1 },
    "target_enrollment": { "type": "integer" },
    "treatment_description": { "type": "string" },
    "dose": { "type": "string" },
    "schedule": { "type": "string" }
  }
}
```

### VisitSchedule

Protocol-defined visit schedule.

```json
{
  "title": "VisitSchedule",
  "type": "object",
  "required": ["visit_num", "visit_name", "study_id"],
  "properties": {
    "visit_num": { "type": "number", "description": "Maps to VISITNUM" },
    "visit_name": { "type": "string", "description": "Maps to VISIT" },
    "study_id": { "type": "string" },
    "visit_type": {
      "type": "string",
      "enum": ["Screening", "Baseline", "Treatment", "End of Treatment", "Follow-up", "Early Termination", "Unscheduled"]
    },
    "target_day": { "type": "integer", "description": "Target study day (Day 1 = first treatment)" },
    "window_before": { "type": "integer", "default": 0 },
    "window_after": { "type": "integer", "default": 0 },
    "required_assessments": { "type": "array", "items": { "type": "string" } }
  }
}
```

### ActualVisit

Subject's actual visit occurrence.

```json
{
  "title": "ActualVisit",
  "type": "object",
  "required": ["usubjid", "visit_num", "visit_date"],
  "properties": {
    "usubjid": { "type": "string" },
    "visit_num": { "type": "number" },
    "visit_name": { "type": "string" },
    "visit_date": { "type": "string", "format": "date" },
    "study_day": { "type": "integer" },
    "visit_status": {
      "type": "string",
      "enum": ["Completed", "Missed", "Partially Completed", "Unscheduled"]
    },
    "window_deviation_days": {
      "type": "integer",
      "description": "Days outside visit window (0 = within window)"
    }
  }
}
```

### Randomization

Subject randomization record.

```json
{
  "title": "Randomization",
  "type": "object",
  "required": ["usubjid", "randomization_date", "arm_code"],
  "properties": {
    "usubjid": { "type": "string" },
    "randomization_number": { "type": "string" },
    "randomization_date": { "type": "string", "format": "date" },
    "arm_code": { "type": "string" },
    "stratification_factors": {
      "type": "object",
      "description": "Key-value pairs for stratification"
    },
    "randomization_method": {
      "type": "string",
      "enum": ["IVRS", "IWRS", "Sealed Envelope", "Block", "Stratified Block"]
    }
  }
}
```

### AdverseEvent

Adverse event with full MedDRA hierarchy.

```json
{
  "title": "AdverseEvent",
  "type": "object",
  "required": ["usubjid", "aeterm", "aestdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "aeseq": { "type": "integer" },
    "aeterm": { "type": "string", "description": "Reported term (verbatim)" },
    "aedecod": { "type": "string", "description": "MedDRA Preferred Term (PT)" },
    "aebodsys": { "type": "string", "description": "MedDRA System Organ Class (SOC)" },
    "aehlt": { "type": "string", "description": "MedDRA High Level Term (HLT)" },
    "aehlgt": { "type": "string", "description": "MedDRA High Level Group Term (HLGT)" },
    "aellt": { "type": "string", "description": "MedDRA Lowest Level Term (LLT)" },
    "aestdtc": { "type": "string", "format": "date" },
    "aeendtc": { "type": "string", "format": "date" },
    "aesev": { "type": "string", "enum": ["Mild", "Moderate", "Severe"] },
    "aetoxgr": { "type": "string", "enum": ["1", "2", "3", "4", "5"], "description": "CTCAE grade" },
    "aeser": { "type": "string", "enum": ["Y", "N"] },
    "aerel": { "type": "string", "enum": ["Not Related", "Unlikely", "Possibly", "Probably", "Definitely"] },
    "aeacn": { "type": "string", "enum": ["None", "Dose Reduced", "Drug Interrupted", "Drug Withdrawn", "Not Applicable"] },
    "aeout": { "type": "string", "enum": ["Recovered/Resolved", "Recovering/Resolving", "Not Recovered/Not Resolved", "Recovered with Sequelae", "Fatal", "Unknown"] },
    "aesae_criteria": {
      "type": "array",
      "items": { "type": "string", "enum": ["Death", "Life-threatening", "Hospitalization", "Disability", "Congenital Anomaly", "Important Medical Event"] }
    }
  }
}
```

**MedDRA Hierarchy:**

| Level | Abbreviation | Example |
|-------|--------------|---------|
| System Organ Class | SOC | Gastrointestinal disorders |
| High Level Group Term | HLGT | Gastrointestinal motility and defaecation conditions |
| High Level Term | HLT | Diarrhoea (excl infective) |
| Preferred Term | PT | Diarrhoea |
| Lowest Level Term | LLT | Loose stools |

### Exposure

Study drug exposure/dosing record.

```json
{
  "title": "Exposure",
  "type": "object",
  "required": ["usubjid", "extrt", "exstdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "exseq": { "type": "integer" },
    "extrt": { "type": "string", "description": "Treatment name" },
    "exdose": { "type": "number" },
    "exdosu": { "type": "string", "description": "Dose units (mg, mg/kg, mL, cells)" },
    "exdosfrq": { "type": "string", "description": "Frequency (ONCE, QD, BID, Q3W)" },
    "exroute": { "type": "string", "description": "Route (ORAL, INTRAVENOUS, SUBCUTANEOUS)" },
    "exstdtc": { "type": "string", "format": "date" },
    "exendtc": { "type": "string", "format": "date" },
    "exadj": { "type": "string", "description": "Reason for dose adjustment" },
    "planned_dose": { "type": "number" },
    "dose_modification": { "type": "string", "enum": ["None", "Reduction", "Delay", "Interruption", "Discontinuation"] }
  }
}
```

### ConcomitantMed

Prior and concomitant medications with ATC classification.

```json
{
  "title": "ConcomitantMed",
  "type": "object",
  "required": ["usubjid", "cmtrt"],
  "properties": {
    "usubjid": { "type": "string" },
    "cmseq": { "type": "integer" },
    "cmtrt": { "type": "string", "description": "Medication name (generic)" },
    "cmdecod": { "type": "string", "description": "WHO Drug Dictionary preferred name" },
    "cmatc1cd": { "type": "string", "description": "ATC Level 1 (Anatomical main group)" },
    "cmatc2cd": { "type": "string", "description": "ATC Level 2 (Therapeutic subgroup)" },
    "cmatc3cd": { "type": "string", "description": "ATC Level 3 (Pharmacological subgroup)" },
    "cmatc4cd": { "type": "string", "description": "ATC Level 4 (Chemical subgroup)" },
    "cmdose": { "type": "number" },
    "cmdosu": { "type": "string" },
    "cmdosfrq": { "type": "string" },
    "cmroute": { "type": "string" },
    "cmstdtc": { "type": "string", "format": "date" },
    "cmendtc": { "type": "string", "format": "date" },
    "cmindc": { "type": "string", "description": "Indication" },
    "cmprior": { "type": "string", "enum": ["Y", "N"], "description": "Prior to study start" },
    "cmongo": { "type": "string", "enum": ["Y", "N"], "description": "Ongoing at study end" }
  }
}
```

### TrialLab

Laboratory test result in trial context.

```json
{
  "title": "TrialLab",
  "type": "object",
  "required": ["usubjid", "lbtestcd", "lbdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "lbseq": { "type": "integer" },
    "lbtestcd": { "type": "string", "description": "Lab test short name (ALT, AST, CREAT, HGB, WBC)" },
    "lbtest": { "type": "string", "description": "Lab test full name" },
    "lbcat": { "type": "string", "description": "Category (CHEMISTRY, HEMATOLOGY, URINALYSIS, COAGULATION)" },
    "lborres": { "type": "string", "description": "Result (original units)" },
    "lborresu": { "type": "string", "description": "Original units" },
    "lbstresn": { "type": "number", "description": "Result (standard numeric)" },
    "lbstresu": { "type": "string", "description": "Standard units" },
    "lbstnrlo": { "type": "number", "description": "Reference range lower limit" },
    "lbstnrhi": { "type": "number", "description": "Reference range upper limit" },
    "lbnrind": { "type": "string", "enum": ["NORMAL", "LOW", "HIGH", "ABNORMAL"] },
    "lbdtc": { "type": "string", "format": "date" },
    "visitnum": { "type": "number" },
    "visit": { "type": "string" },
    "loinc_code": { "type": "string" },
    "lbtoxgr": { "type": "string", "enum": ["0", "1", "2", "3", "4"], "description": "CTCAE toxicity grade" }
  }
}
```

### EfficacyAssessment

Efficacy/response assessment.

```json
{
  "title": "EfficacyAssessment",
  "type": "object",
  "required": ["usubjid", "assessment_type", "assessment_date"],
  "properties": {
    "usubjid": { "type": "string" },
    "assessment_seq": { "type": "integer" },
    "assessment_type": { "type": "string", "description": "Assessment type (RECIST, irRECIST, RANO, NYHA, mMRC, EDSS, ADAS-Cog)" },
    "assessment_date": { "type": "string", "format": "date" },
    "visitnum": { "type": "number" },
    "response": { "type": "string", "description": "Response category (CR, PR, SD, PD, NE)" },
    "response_confirmed": { "type": "boolean" },
    "target_lesion_sum": { "type": "number", "description": "Sum of target lesion diameters (RECIST)" },
    "change_from_baseline": { "type": "number", "description": "Percent change from baseline" },
    "new_lesions": { "type": "boolean" },
    "score": { "type": "number", "description": "Numeric score (for scales)" },
    "score_change": { "type": "number", "description": "Change from baseline score" }
  }
}
```

**Common Assessment Types:**

| Assessment | Domain | Response Categories |
|------------|--------|---------------------|
| RECIST 1.1 | Oncology | CR, PR, SD, PD, NE |
| irRECIST | Immuno-Oncology | iCR, iPR, iSD, iUPD, iCPD |
| RANO | Neuro-Oncology | CR, PR, SD, PD |
| NYHA | Cardiovascular | Class I, II, III, IV |
| ADAS-Cog | CNS (Alzheimer's) | 0-70 score |
| EDSS | CNS (MS) | 0-10 score |

### MedicalHistory

Subject's medical history (pre-existing conditions).

```json
{
  "title": "MedicalHistory",
  "type": "object",
  "required": ["usubjid", "mhterm"],
  "properties": {
    "usubjid": { "type": "string" },
    "mhseq": { "type": "integer" },
    "mhterm": { "type": "string", "description": "Reported term (verbatim)" },
    "mhdecod": { "type": "string", "description": "MedDRA Preferred Term" },
    "mhbodsys": { "type": "string", "description": "MedDRA System Organ Class" },
    "mhcat": { "type": "string", "description": "Category (PRIMARY DIAGNOSIS, GENERAL MEDICAL HISTORY, SURGICAL HISTORY)" },
    "mhstdtc": { "type": "string", "format": "date" },
    "mhendtc": { "type": "string", "format": "date" },
    "mhongo": { "type": "string", "enum": ["Y", "N"], "description": "Ongoing at screening" }
  }
}
```

### DispositionEvent

Subject disposition milestones.

```json
{
  "title": "DispositionEvent",
  "type": "object",
  "required": ["usubjid", "dsdecod", "dsstdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "dsseq": { "type": "integer" },
    "dsterm": { "type": "string", "description": "Reported term (verbatim)" },
    "dsdecod": { "type": "string", "description": "Standardized term" },
    "dscat": { "type": "string", "enum": ["DISPOSITION EVENT", "PROTOCOL MILESTONE"] },
    "dsscat": { "type": "string", "description": "Subcategory (STUDY TREATMENT, STUDY PARTICIPATION)" },
    "dsstdtc": { "type": "string", "format": "date" },
    "epoch": { "type": "string", "description": "Trial epoch (SCREENING, TREATMENT, FOLLOW-UP)" }
  }
}
```

**Standard Disposition Terms (CDISC CT):**

| Category | Terms |
|----------|-------|
| Completion | COMPLETED |
| Discontinuation | ADVERSE EVENT, DEATH, LACK OF EFFICACY, LOST TO FOLLOW-UP, PHYSICIAN DECISION, PROTOCOL VIOLATION, WITHDRAWAL BY SUBJECT |

### ProtocolDeviation

Protocol deviation record.

```json
{
  "title": "ProtocolDeviation",
  "type": "object",
  "required": ["usubjid", "dvterm", "dvstdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "dvseq": { "type": "integer" },
    "dvterm": { "type": "string", "description": "Deviation description" },
    "dvdecod": { "type": "string", "description": "Standardized category" },
    "dvcat": { "type": "string", "enum": ["MAJOR", "MINOR"] },
    "dvstdtc": { "type": "string", "format": "date" },
    "dvendtc": { "type": "string", "format": "date" },
    "impact_on_analysis": { "type": "string", "enum": ["None", "Excluded from Per-Protocol", "Excluded from ITT", "Sensitivity Analysis Required"] }
  }
}
```

### TrialSim Entity Relationships

| Parent Entity | Child Entity | Relationship | Foreign Key |
|---------------|--------------|--------------|-------------|
| Study | Site | 1:M | site.study_id |
| Study | TreatmentArm | 1:M | arm.study_id |
| Study | VisitSchedule | 1:M | schedule.study_id |
| Site | Subject | 1:M | subject.site_id |
| Subject | Randomization | 1:1 | randomization.usubjid |
| Subject | ActualVisit | 1:M | visit.usubjid |
| Subject | AdverseEvent | 1:M | ae.usubjid |
| Subject | Exposure | 1:M | ex.usubjid |
| Subject | ConcomitantMed | 1:M | cm.usubjid |
| Subject | TrialLab | 1:M | lb.usubjid |
| Subject | EfficacyAssessment | 1:M | eff.usubjid |
| Subject | MedicalHistory | 1:M | mh.usubjid |
| Subject | DispositionEvent | 1:M | ds.usubjid |
| Subject | ProtocolDeviation | 1:M | dv.usubjid |
| TreatmentArm | Randomization | 1:M | randomization.arm_code |

### TrialSim Cross-Product Linking

| TrialSim Entity | Correlated Entity | Linking Field | Purpose |
|-----------------|-------------------|---------------|---------|
| Subject | Patient (PatientSim) | patient_ref → mrn | Medical history source |
| Subject | Person (core) | ssn | Cross-product identity |
| Site | Facility (NetworkSim) | facility_id | Physical location details |
| PI | Provider (NetworkSim) | npi | Provider credentials |

---

## Cross-Product Identity Correlation

When generating data that spans multiple HealthSim products (e.g., a patient journey from clinical encounter to claims to pharmacy), use these patterns to maintain identity consistency.

### Entity Inheritance Model

All person entities inherit from the Core Person Model:

```
                    ┌──────────────┐
                    │    Person    │
                    │  (id, name,  │
                    │  birth_date, │
                    │   gender)    │
                    └──────┬───────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Patient    │   │    Member    │   │   RxMember   │
│  (+ mrn,     │   │ (+ member_id,│   │(+ cardholder_│
│    ssn)      │   │  subscriber_ │   │  id, bin,    │
│              │   │  id, group_  │   │  pcn, group_ │
│              │   │  id)         │   │  number)     │
└──────────────┘   └──────────────┘   └──────────────┘
       │                   │                   │
       │                   │                   │
       ▼                   ▼                   ▼
   PatientSim          MemberSim          RxMemberSim
```

### Identity Linking Keys

When the same person exists across multiple products, use these fields to correlate:

| Link Type | Primary Key | Secondary Keys | Notes |
|-----------|-------------|----------------|-------|
| **Universal** | SSN | - | Most reliable cross-product link (when available) |
| **Medical-to-Payer** | Patient.ssn = Member.ssn | Patient.mrn ↔ Member.member_id (via mapping) | Claims reference patient's clinical events |
| **Payer-to-Pharmacy** | Member.member_id = RxMember.member_id | Member.subscriber_id = RxMember.subscriber_id | Often same ID in integrated systems |
| **Medical-to-Pharmacy** | Patient.ssn = RxMember.ssn | - | Prescriptions link to patient records |

### Cross-Product Identity Pattern

When generating a person who appears in multiple products:

```json
{
  "_comment": "Cross-product identity correlation object",
  "correlation_id": "CORR-2025-001",
  "person": {
    "ssn": "123456789",
    "name": {
      "given_name": "Maria",
      "family_name": "Garcia"
    },
    "birth_date": "1958-03-15",
    "gender": "F"
  },
  "identities": {
    "patientsim": {
      "mrn": "MRN-001234",
      "facility": "General Hospital"
    },
    "membersim": {
      "member_id": "MEM-ABC123",
      "subscriber_id": "MEM-ABC123",
      "group_id": "GRP-ACME-001",
      "plan_code": "GOLD-PPO-2025"
    },
    "rxmembersim": {
      "cardholder_id": "RX-ABC123",
      "person_code": "01",
      "bin": "610014",
      "pcn": "RXGROUP",
      "group_number": "ACME2025"
    },
    "trialsim": {
      "subject_id": "SUBJ-TRL-001",
      "screening_id": "SCR-2025-0042"
    }
  }
}
```

### Event Correlation Across Products

When an event in one product should correlate to events in other products:

| Source Event (Product) | Correlated Event (Product) | Timing | Linking Fields |
|------------------------|---------------------------|--------|----------------|
| Encounter (PatientSim) | Claim (MemberSim) | +0-14 days | service_date ≈ admission_date; diagnosis codes match |
| Medication order (PatientSim) | Prescription (RxMemberSim) | Same day | NDC matches; prescriber_npi consistent |
| Discharge (PatientSim) | PharmacyClaim (RxMemberSim) | +0-3 days | Discharge meds → retail fills |
| Prior Auth approved (MemberSim) | Encounter scheduled (PatientSim) | +1-30 days | Auth number referenced |
| Subject enrollment (TrialSim) | Encounters (PatientSim) | Per protocol | Study visits generate encounters |

### Generation Guidelines

**Single-Product Generation:**
- Generate Person attributes first
- Add product-specific identifiers (MRN, member_id, cardholder_id)
- SSN is optional but recommended for future correlation

**Multi-Product Generation:**
1. Generate base Person with SSN
2. Create product-specific identities with consistent Person attributes
3. Use SSN as the correlation key
4. Ensure dates/events align logically across products

**Example: Patient with Heart Failure Journey**

```
Day 0:  PatientSim - ED encounter, CHF diagnosis (I50.9)
Day 3:  PatientSim - Inpatient discharge with medications
Day 5:  MemberSim  - Facility claim submitted (matches encounter dates, DRG 291)
Day 3:  RxMemberSim - Discharge prescription filled (furosemide, carvedilol)
Day 30: PatientSim - Cardiology follow-up encounter
Day 32: MemberSim  - Professional claim submitted (99214)
```

### TrialSim Identity Considerations

Clinical trial subjects have additional identity layers:

| Context | Identifier | Notes |
|---------|------------|-------|
| Trial-internal | subject_id | Randomization ID, blinded |
| Screening | screening_id | Pre-randomization tracking |
| Site EMR | mrn | If site uses local EMR for source data |
| Sponsor systems | subject_id | De-identified for sponsor |

For trials with EMR integration (eSource), the subject_id correlates to a Patient.mrn at the site level.
