---
name: adt-workflow
description: "Admit/Discharge/Transfer events following HL7v2 ADT messaging patterns. Triggers: ADT, admission, discharge, transfer, patient movement, census, inpatient workflow, A01, A02, A03, bed management"
---

# ADT Workflow Cohort

A cohort template for generating Admit/Discharge/Transfer events following HL7v2 ADT messaging patterns.

## For Claude

Use this skill when the user requests ADT events or patient movement workflows. This teaches you how to generate **realistic ADT messages** including A01 (admit), A02 (transfer), A03 (discharge), and other event types with proper location coding and temporal sequences.

**When to apply this skill:**

- User mentions ADT, admission, discharge, or transfer events
- User requests patient movement or census data
- User asks for inpatient workflow simulation
- User needs HL7v2 ADT message examples

**Key capabilities this skill provides:**

- How to generate proper ADT event sequences
- How to code locations (units, rooms, beds)
- How to apply admission sources and discharge dispositions
- How to model complete inpatient stay workflows

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: adt, admission, discharge, transfer, hl7v2, inpatient
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic Admit/Discharge/Transfer events for patient movement tracking. It supports the complete ADT lifecycle from registration through discharge with proper location coding and event sequencing.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "ADT", "admit", "admission", "discharge", "transfer"
- "A01", "A02", "A03", "A04", "A08"
- "patient movement", "census", "bed management"
- "inpatient workflow"

**Workflow Cohorts**:

- "Generate an admission for chest pain"
- "Create a complete inpatient stay with transfers"
- "Generate ADT events for an ED-to-admit conversion"

## Trigger Phrases

- ADT
- admission
- admit patient
- discharge
- transfer
- patient movement
- inpatient admission
- hospital admission
- patient registration
- bed management
- census
- admit/discharge/transfer

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| event_type | string | A01 | A01, A02, A03, A04, A08, A11, A13 |
| encounter_class | string | I | I (Inpatient), O (Outpatient), E (Emergency), U (Urgent), OBS (Observation) |
| patient_class | string | I | I, O, E, P (Preadmit), R (Recurring), B (Obstetrics) |
| admission_type | string | E | E (Emergency), R (Routine), U (Urgent), C (Elective) |
| length_of_stay | range | 1-7 | Days for inpatient stay |
| include_preadmit | bool | false | Include prior outpatient registration |
| geography | string | null | County/tract FIPS for data-driven demographics |

## Data Sources (PopulationSim v2.0)

When geography is specified, ADT cohorts use real population data for demographics and utilization patterns:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Key columns for utilization:
  - TotalPopulation: Population for scaling
  - ACCESS2_CrudePrev: Uninsured rate (affects admission patterns)
  - CHECKUP_CrudePrev: Preventive care access

File: skills/populationsim/data/county/svi_county_2022.csv
Key columns:
  - RPL_THEMES: Overall vulnerability (affects ED utilization)
  - EP_AGE65: Age 65+ percentage (Medicare population)
  - EP_UNINSUR: Uninsured rate
```

### Data-Driven Patterns

| Pattern | Generic Default | Data-Driven Adjustment |
|---------|-----------------|------------------------|
| ED admission rate | 15% | Higher if SVI > 0.75 |
| Payer mix | 40% commercial | Based on EP_UNINSUR, EP_AGE65 |
| LOS | 4.5 days avg | Longer if high vulnerability |
| Readmit risk | 15% | Higher if ACCESS2 > 20% |

### Example: Harris County, TX (FIPS 48201)
```
From svi_county_2022.csv:
  RPL_THEMES: 0.68 (high vulnerability)
  EP_AGE65: 10.8%
  EP_UNINSUR: 22.1%
  
Apply to ADT generation:
  - Higher ED-to-admit conversion (RPL > 0.5)
  - Medicare: ~11%, Uninsured: ~22%, Commercial: ~45%, Medicaid: ~22%
  - Increased readmission probability
```

## ADT Event Types

### A01 - Admit/Visit Notification

The primary admission event when a patient arrives for inpatient care.

**Trigger Conditions:**
- Patient arrives at hospital for admission
- ED patient converted to inpatient
- Direct admission from physician office
- Scheduled surgical admission

**Required Data Elements:**
- Patient demographics (PID)
- Visit information (PV1)
- Admission diagnosis (DG1)
- Insurance information (IN1)
- Attending physician
- Assigned bed location

**Example Request:** "Generate an A01 admission for a patient with chest pain"

### A02 - Transfer

Patient movement between units, rooms, or beds within the facility.

**Trigger Conditions:**
- Unit-to-unit transfer (e.g., ICU to stepdown)
- Room change
- Bed swap
- Level of care change

**Required Data Elements:**
- Prior location (PV1-3)
- New location (PV1-6)
- Transfer reason
- Transfer timestamp
- New attending (if changed)

**Example Request:** "Generate an A02 transfer from ICU to telemetry unit"

### A03 - Discharge/End Visit

Patient discharge from the facility or end of outpatient visit.

**Trigger Conditions:**
- Patient leaving facility
- End of outpatient encounter
- Death discharge
- Transfer to another facility

**Required Data Elements:**
- Discharge date/time (PV1-45)
- Discharge disposition (PV1-36)
- Discharge diagnosis (final)
- Follow-up instructions
- Pending orders status

**Example Request:** "Generate an A03 discharge to home with follow-up"

### A04 - Register a Patient

Outpatient registration or preadmission registration.

**Trigger Conditions:**
- Patient arrives for outpatient visit
- Preadmission testing
- Pre-surgical registration
- Emergency department registration

**Required Data Elements:**
- Patient demographics (PID)
- Account information
- Insurance (IN1)
- Expected provider
- Appointment reference

**Example Request:** "Generate an A04 registration for outpatient lab work"

### A08 - Update Patient Information

Demographics or visit information update.

**Trigger Conditions:**
- Address change
- Insurance update
- Next of kin change
- Diagnosis update
- Attending physician change

**Required Data Elements:**
- Updated fields only
- Original and updated values
- Update timestamp
- User performing update

**Example Request:** "Generate an A08 to update patient insurance"

### A11 - Cancel Admit/Visit

Cancel a previously transmitted A01 admission.

**Trigger Conditions:**
- Erroneous admission entry
- Patient left before admission complete
- Duplicate registration
- Wrong patient admitted

**Required Data Elements:**
- Original admission event reference
- Cancellation reason
- Cancellation timestamp
- Cancelled by (user)

**Example Request:** "Generate an A11 to cancel an admission entered in error"

### A13 - Cancel Discharge

Cancel a previously transmitted A03 discharge.

**Trigger Conditions:**
- Patient returned before leaving
- Discharge entered prematurely
- Patient condition changed
- Documentation error

**Required Data Elements:**
- Original discharge event reference
- Readmission bed assignment
- Cancellation reason

**Example Request:** "Generate an A13 to cancel a discharge - patient returned"

## Workflow Patterns

### Pattern 1: Standard Inpatient Stay

Complete admission through discharge workflow:

```
1. A04 - Register patient (optional, for scheduled admissions)
2. A01 - Admit patient
3. A02 - Transfer to appropriate unit (if needed)
4. A08 - Update diagnosis/information (as needed)
5. A03 - Discharge patient
```

**Timeline Example:**
```json
{
  "events": [
    { "event": "A01", "time": "2025-01-15T14:30:00", "location": "ED" },
    { "event": "A02", "time": "2025-01-15T18:00:00", "from": "ED", "to": "MED-201A" },
    { "event": "A02", "time": "2025-01-17T10:00:00", "from": "MED-201A", "to": "MED-305B" },
    { "event": "A03", "time": "2025-01-19T11:00:00", "disposition": "01" }
  ]
}
```

### Pattern 2: ED to Inpatient Conversion

Emergency department visit converting to admission:

```
1. A04 - ED Registration
2. A01 - Admit as inpatient (class change E to I)
3. A02 - Transfer from ED to inpatient unit
4. A03 - Discharge
```

### Pattern 3: Observation to Inpatient

Observation status converting to full inpatient:

```
1. A01 - Admit to observation (class OBS)
2. A08 - Update class to inpatient (class I)
3. A03 - Discharge
```

### Pattern 4: Cancelled Admission

Admission cancelled before patient actually arrives:

```
1. A01 - Admit patient (pre-registered)
2. A11 - Cancel admission (patient no-show or error)
```

### Pattern 5: Cancelled Discharge

Patient returns after discharge initiated:

```
1. A03 - Discharge patient
2. A13 - Cancel discharge
3. A08 - Update status back to admitted
4. A03 - Final discharge (later)
```

## Location Coding

### Unit Codes

| Code | Unit Name | Type |
|------|-----------|------|
| ED | Emergency Department | Emergency |
| ICU | Intensive Care Unit | Critical |
| CCU | Cardiac Care Unit | Critical |
| MICU | Medical ICU | Critical |
| SICU | Surgical ICU | Critical |
| SDU | Step-Down Unit | Intermediate |
| TELE | Telemetry | Intermediate |
| MED | Medical/Surgical | Acute |
| SURG | Surgical | Acute |
| PEDS | Pediatrics | Acute |
| OB | Obstetrics | Acute |
| NICU | Neonatal ICU | Critical |
| PSYCH | Psychiatry | Behavioral |
| REHAB | Rehabilitation | Post-Acute |
| OBS | Observation | Observation |

### Room/Bed Format

```
{unit}-{room}{bed}

Examples:
- MED-201A (Medical unit, room 201, bed A)
- ICU-10 (ICU, room 10, single bed)
- ED-BAY3 (Emergency, bay 3)
- SURG-412B (Surgical unit, room 412, bed B)
```

## Admission Sources

| Code | Description | Use When |
|------|-------------|----------|
| 1 | Physician Referral | Direct admit from office |
| 2 | Clinic Referral | Transfer from clinic |
| 3 | HMO Referral | HMO-authorized admission |
| 4 | Transfer from Hospital | From another facility |
| 5 | Transfer from SNF | From skilled nursing |
| 6 | Transfer from Other | From other healthcare facility |
| 7 | Emergency Room | ED-originated admission |
| 8 | Court/Law Enforcement | Legal/psychiatric hold |
| 9 | Information Not Available | Unknown source |

## Discharge Dispositions

| Code | Description | Use When |
|------|-------------|----------|
| 01 | Home/Self Care | Standard discharge home |
| 02 | Short-term Hospital | Transfer to acute care |
| 03 | SNF | Transfer to skilled nursing |
| 04 | ICF | Transfer to intermediate care |
| 05 | Other Institution | Cancer center, children's, etc. |
| 06 | Home with Home Health | Home with HHA services |
| 07 | Left AMA | Against medical advice |
| 20 | Expired | Death |
| 21 | Expired in ED | Death in emergency dept |
| 43 | Federal Hospital | VA, military |
| 50 | Hospice - Home | Hospice at home |
| 51 | Hospice - Facility | Hospice in a facility |
| 62 | Inpatient Rehab | Transfer to rehab |
| 63 | LTCH | Long-term care hospital |
| 65 | Psychiatric | Transfer to psych |
| 66 | Critical Access | Transfer to CAH |

## Examples

### Example 1: Standard Admission (A01)

**Request:** "Generate an A01 admission for chest pain"

```json
{
  "event_type": "A01",
  "event_time": "2025-01-15T14:30:00",
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Robert", "family_name": "Johnson" },
    "birth_date": "1958-06-20",
    "gender": "M",
    "ssn": "123-45-6789",
    "address": {
      "street_address": "456 Oak Avenue",
      "city": "Springfield",
      "state": "IL",
      "postal_code": "62702"
    },
    "phone": "555-234-5678"
  },
  "encounter": {
    "encounter_id": "ENC0000000001",
    "account_number": "A20250115001",
    "patient_class": "I",
    "admission_type": "E",
    "admission_source": "7",
    "admission_time": "2025-01-15T14:30:00",
    "location": {
      "point_of_care": "ED",
      "room": "BAY5",
      "bed": null,
      "facility": "SPRINGFIELD",
      "building": null,
      "floor": "1"
    },
    "attending_provider": {
      "npi": "1234567890",
      "name": { "given_name": "Sarah", "family_name": "Williams" },
      "specialty": "Internal Medicine"
    },
    "admitting_provider": {
      "npi": "1234567890",
      "name": { "given_name": "Sarah", "family_name": "Williams" }
    },
    "chief_complaint": "Chest pain, onset 2 hours ago"
  },
  "diagnoses": [
    {
      "code": "R07.9",
      "description": "Chest pain, unspecified",
      "type": "admitting",
      "coding_system": "ICD-10-CM"
    }
  ],
  "insurance": [
    {
      "sequence": 1,
      "plan_id": "BCBS001",
      "plan_name": "Blue Cross Blue Shield PPO",
      "member_id": "XYZ123456789",
      "group_number": "GRP001",
      "subscriber": {
        "name": { "given_name": "Robert", "family_name": "Johnson" },
        "relationship": "Self"
      }
    }
  ]
}
```

### Example 2: Transfer (A02)

**Request:** "Generate an A02 transfer from ICU to telemetry"

```json
{
  "event_type": "A02",
  "event_time": "2025-01-17T08:00:00",
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Robert", "family_name": "Johnson" }
  },
  "encounter": {
    "encounter_id": "ENC0000000001",
    "account_number": "A20250115001",
    "patient_class": "I"
  },
  "transfer": {
    "prior_location": {
      "point_of_care": "ICU",
      "room": "10",
      "bed": null,
      "facility": "SPRINGFIELD"
    },
    "new_location": {
      "point_of_care": "TELE",
      "room": "305",
      "bed": "A",
      "facility": "SPRINGFIELD"
    },
    "transfer_reason": "Stable for step-down",
    "new_attending": {
      "npi": "2345678901",
      "name": { "given_name": "Michael", "family_name": "Chen" }
    }
  }
}
```

### Example 3: Discharge (A03)

**Request:** "Generate an A03 discharge to home"

```json
{
  "event_type": "A03",
  "event_time": "2025-01-19T11:00:00",
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Robert", "family_name": "Johnson" }
  },
  "encounter": {
    "encounter_id": "ENC0000000001",
    "account_number": "A20250115001",
    "patient_class": "I",
    "admission_time": "2025-01-15T14:30:00",
    "discharge_time": "2025-01-19T11:00:00",
    "length_of_stay_days": 4,
    "discharge_disposition": "01"
  },
  "diagnoses": [
    {
      "code": "I21.09",
      "description": "STEMI involving other coronary artery",
      "type": "principal",
      "coding_system": "ICD-10-CM"
    },
    {
      "code": "I25.10",
      "description": "Atherosclerotic heart disease",
      "type": "secondary",
      "coding_system": "ICD-10-CM"
    },
    {
      "code": "I10",
      "description": "Essential hypertension",
      "type": "secondary",
      "coding_system": "ICD-10-CM"
    }
  ],
  "procedures": [
    {
      "code": "92928",
      "description": "PCI with stent placement",
      "date": "2025-01-15",
      "coding_system": "CPT"
    }
  ],
  "discharge_instructions": {
    "activity": "Light activity, no heavy lifting for 2 weeks",
    "diet": "Heart-healthy, low sodium",
    "medications": [
      "Aspirin 81mg daily",
      "Clopidogrel 75mg daily",
      "Atorvastatin 80mg at bedtime",
      "Metoprolol 25mg twice daily"
    ],
    "follow_up": [
      {
        "provider": "Dr. Michael Chen",
        "specialty": "Cardiology",
        "timeframe": "1 week"
      },
      {
        "provider": "Primary Care",
        "specialty": "Internal Medicine",
        "timeframe": "2 weeks"
      }
    ],
    "return_precautions": [
      "Return to ED for chest pain",
      "Return for shortness of breath",
      "Return for bleeding at catheter site"
    ]
  }
}
```

### Example 4: Complete Workflow Timeline

**Request:** "Generate a complete ADT workflow for a 4-day admission"

```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Maria", "family_name": "Garcia" },
    "birth_date": "1965-03-15",
    "gender": "F"
  },
  "encounter": {
    "encounter_id": "ENC0000000001",
    "account_number": "A20250115002"
  },
  "adt_events": [
    {
      "sequence": 1,
      "event_type": "A04",
      "event_time": "2025-01-15T06:00:00",
      "description": "Pre-admission registration for scheduled surgery",
      "location": "PRE-ADMIT"
    },
    {
      "sequence": 2,
      "event_type": "A01",
      "event_time": "2025-01-15T07:30:00",
      "description": "Admission for total knee replacement",
      "location": "SURG-401A",
      "admission_type": "C",
      "admission_source": "1"
    },
    {
      "sequence": 3,
      "event_type": "A02",
      "event_time": "2025-01-15T14:00:00",
      "description": "Post-op transfer to surgical unit",
      "from_location": "OR-2",
      "to_location": "SURG-401A"
    },
    {
      "sequence": 4,
      "event_type": "A08",
      "event_time": "2025-01-16T10:00:00",
      "description": "Update attending physician",
      "update_field": "Attending Provider",
      "old_value": "Dr. Williams (Surgeon)",
      "new_value": "Dr. Chen (Hospitalist)"
    },
    {
      "sequence": 5,
      "event_type": "A02",
      "event_time": "2025-01-17T09:00:00",
      "description": "Transfer to rehab unit",
      "from_location": "SURG-401A",
      "to_location": "REHAB-205A"
    },
    {
      "sequence": 6,
      "event_type": "A03",
      "event_time": "2025-01-19T10:30:00",
      "description": "Discharge to home with PT services",
      "discharge_disposition": "06",
      "length_of_stay": 4
    }
  ]
}
```

## HL7v2 Output Format

When outputting as HL7v2 ADT message, use the [HL7v2 ADT Format](../../formats/hl7v2-adt.md) transformation skill.

**Request:** "Generate an A01 admission as HL7v2"

```
MSH|^~\&|PATIENTSIM|FACILITY|EMR|FACILITY|20250115143000||ADT^A01^ADT_A01|MSG00001|P|2.5.1|||AL|NE||ASCII|||
EVN|A01|20250115143000|||1234567890^Williams^Sarah^M^^^MD|20250115143000|
PID|1||MRN00000001^^^FACILITY^MR||Johnson^Robert^M^^^^L||19580620|M||2106-3^White^HL70005|456 Oak Avenue^^Springfield^IL^62702^USA^H||^PRN^PH^^1^555^2345678|||||123-45-6789|||N^Non-Hispanic^HL70189|||||||
PV1|1|I|ED^BAY5^^^^^SPRINGFIELD||||1234567890^Williams^Sarah^M^^^MD|||MED||||7|||1234567890^Williams^Sarah^M^^^MD|IN||||||||||||||||||||||||||20250115143000||||||
DG1|1||R07.9^Chest pain, unspecified^I10||20250115|A|||||||||
IN1|1|1^BCBS001|Blue Cross Blue Shield PPO|BCBS^^^^^|123 Insurance Way^^Chicago^IL^60601|^^^^^1^800^5551234|GRP001||||||||Johnson^Robert|01|19580620|456 Oak Avenue^^Springfield^IL^62702|||||||||||||||XYZ123456789||||||||
```

## FHIR Output Format

When outputting as FHIR, use the [FHIR R4 Format](../../formats/fhir-r4.md) transformation skill.

**Request:** "Generate an A01 admission as FHIR"

The Encounter resource includes:
- status: `in-progress`
- class: `IMP` (inpatient)
- type: `99221` (Initial hospital care)
- period.start: admission datetime
- hospitalization.admitSource
- location array with status `active`

## Validation Rules

### A01 Admission
1. Patient MRN must exist or be created
2. Encounter ID must be unique
3. Admission time must be present
4. Location must be specified
5. Attending provider required
6. At least one diagnosis recommended

### A02 Transfer
1. Valid encounter must exist
2. Prior location must match current
3. New location must differ from prior
4. Transfer time must be after admission

### A03 Discharge
1. Valid encounter must exist
2. Discharge time must be after admission
3. Discharge disposition required
4. Final diagnosis required
5. Length of stay must be calculated

### A11 Cancel Admit
1. Original A01 must exist
2. Cannot cancel if transfers or discharges exist
3. Cancellation reason required

## Related Skills

- [SKILL.md](SKILL.md) - PatientSim overview
- [orders-results.md](orders-results.md) - Orders and results for encounters
- [../../formats/hl7v2-adt.md](../../formats/hl7v2-adt.md) - HL7v2 ADT format
- [../../formats/fhir-r4.md](../../formats/fhir-r4.md) - FHIR format
- [../../references/hl7v2-segments.md](../../references/hl7v2-segments.md) - HL7v2 segment reference
- [../../references/code-systems.md](../../references/code-systems.md) - Code systems
