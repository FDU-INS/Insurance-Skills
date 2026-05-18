# HL7v2 ADT Message Format

## Trigger Phrases

- HL7
- HL7v2
- HL7 message
- ADT message
- ADT A01
- ADT A03
- admission message
- discharge message
- pipe delimited

## Overview

HL7v2 is the legacy standard for healthcare messaging, still widely used for ADT (Admit-Discharge-Transfer) events. This skill transforms HealthSim entities into HL7v2 ADT messages.

## Message Types

| Event | Message Type | Description |
|-------|--------------|-------------|
| A01 | ADT^A01 | Patient Admission |
| A02 | ADT^A02 | Patient Transfer |
| A03 | ADT^A03 | Patient Discharge |
| A04 | ADT^A04 | Patient Registration |
| A08 | ADT^A08 | Patient Information Update |
| A11 | ADT^A11 | Cancel Admission |
| A13 | ADT^A13 | Cancel Discharge |

## Message Structure

### Segment Order
```
MSH - Message Header (required)
EVN - Event Type (required)
PID - Patient Identification (required)
PV1 - Patient Visit (required)
PV2 - Patient Visit Additional (optional)
DG1 - Diagnosis (optional, repeating)
AL1 - Allergy (optional, repeating)
```

## Segment Definitions

### MSH - Message Header
```
MSH|^~\&|{sending_app}|{sending_facility}|{receiving_app}|{receiving_facility}|{timestamp}||{message_type}^{trigger}|{control_id}|P|2.5|||AL|NE|
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Field Separator | MSH-1 | Always pipe | `|` |
| Encoding Characters | MSH-2 | Component separators | `^~\&` |
| Sending Application | MSH-3 | Source system | `HEALTHSIM` |
| Sending Facility | MSH-4 | Source facility | `SPRINGFIELD_HOSP` |
| Receiving Application | MSH-5 | Destination system | `EMR` |
| Receiving Facility | MSH-6 | Destination facility | `MAIN_CAMPUS` |
| Date/Time | MSH-7 | Message timestamp | `20250115143000` |
| Message Type | MSH-9 | Type^Trigger | `ADT^A01` |
| Control ID | MSH-10 | Unique message ID | `MSG20250115001` |
| Processing ID | MSH-11 | P=Production, T=Test | `P` |
| Version ID | MSH-12 | HL7 version | `2.5` |

### EVN - Event Type
```
EVN|{trigger}|{recorded_datetime}||||{event_datetime}|
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Event Type | EVN-1 | Trigger event | `A01` |
| Recorded Date/Time | EVN-2 | When recorded | `20250115143000` |
| Event Date/Time | EVN-6 | When event occurred | `20250115140000` |

### PID - Patient Identification
```
PID|1||{mrn}^^^{assigning_auth}^MR||{family}^{given}^{middle}||{dob}|{gender}|||{street}^^{city}^{state}^{zip}^{country}||{phone}|||||||{ssn}|
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Set ID | PID-1 | Always 1 | `1` |
| Patient ID | PID-3 | MRN with authority | `MRN00000001^^^HOSP^MR` |
| Patient Name | PID-5 | Last^First^Middle | `SMITH^JOHN^ROBERT` |
| DOB | PID-7 | YYYYMMDD | `19750315` |
| Gender | PID-8 | M, F, O, U | `M` |
| Address | PID-11 | Street^^City^State^Zip | `123 MAIN ST^^SPRINGFIELD^IL^62701^USA` |
| Phone | PID-13 | Home phone | `5551234567` |
| SSN | PID-19 | Social Security | `123456789` |
| Death Date | PID-29 | If deceased | `20250115` |
| Death Indicator | PID-30 | Y/N | `Y` |

### PV1 - Patient Visit
```
PV1|1|{class}|{location}^^^{facility}||||{attending_npi}^{attending_name}|||||||||||{visit_number}|||||||||||||||||||{admit_datetime}|{discharge_datetime}||||||
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Set ID | PV1-1 | Always 1 | `1` |
| Patient Class | PV1-2 | I/O/E/U | `I` |
| Assigned Location | PV1-3 | Unit^Room^Bed | `ICU^101^A^^^SPRINGFIELD` |
| Admission Type | PV1-4 | 1=Emerg, 2=Urgent, 3=Elective | `1` |
| Attending Doctor | PV1-7 | NPI^Name | `1234567890^SMITH^JOHN^DR` |
| Visit Number | PV1-19 | Encounter ID | `ENC0000000001` |
| Discharge Disposition | PV1-36 | 01=Home, 20=Expired | `01` |
| Admit Date/Time | PV1-44 | YYYYMMDDHHMMSS | `20250110143000` |
| Discharge Date/Time | PV1-45 | YYYYMMDDHHMMSS | `20250115100000` |

### DG1 - Diagnosis
```
DG1|{set_id}||{code}^{description}^I10|||{type}|
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Set ID | DG1-1 | Sequence 1,2,3... | `1` |
| Diagnosis Code | DG1-3 | Code^Desc^System | `I50.23^Acute on chronic systolic HF^I10` |
| Diagnosis Type | DG1-6 | A=Admit, W=Working, F=Final | `A` |

## Patient Class Codes

| Code | Description | FHIR Equivalent |
|------|-------------|-----------------|
| I | Inpatient | IMP |
| O | Outpatient | AMB |
| E | Emergency | EMER |
| P | Preadmit | PRENC |
| R | Recurring patient | AMB |
| B | Obstetrics | IMP |
| C | Commercial account | AMB |

## Example Messages

### ADT^A01 - Patient Admission
```
MSH|^~\&|HEALTHSIM|SPRINGFIELD_HOSP|EMR|MAIN_CAMPUS|20250110143000||ADT^A01|MSG20250110001|P|2.5|||AL|NE|
EVN|A01|20250110143000||||20250110140000|
PID|1||MRN00000001^^^SPRINGFIELD_HOSP^MR||THOMPSON^ELEANOR^MARIE||19500812|F|||456 OAK AVE^^SPRINGFIELD^IL^62702^USA||5559876543|||||||987654321|
PV1|1|I|MED^201^A^^^SPRINGFIELD||||1234567890^JOHNSON^ROBERT^MD|||MED||||||||ENC0000000001|||||||||||||||||||20250110140000||||||
DG1|1||R06.00^Dyspnea^I10|||A|
DG1|2||I50.23^Acute on chronic systolic heart failure^I10|||W|
```

### ADT^A03 - Patient Discharge
```
MSH|^~\&|HEALTHSIM|SPRINGFIELD_HOSP|EMR|MAIN_CAMPUS|20250115100000||ADT^A03|MSG20250115002|P|2.5|||AL|NE|
EVN|A03|20250115100000||||20250115100000|
PID|1||MRN00000001^^^SPRINGFIELD_HOSP^MR||THOMPSON^ELEANOR^MARIE||19500812|F|||456 OAK AVE^^SPRINGFIELD^IL^62702^USA||5559876543|||||||987654321|
PV1|1|I|MED^201^A^^^SPRINGFIELD||||1234567890^JOHNSON^ROBERT^MD|||MED||||||||ENC0000000001|||||||||||||||||01||20250110140000|20250115100000|||||
DG1|1||I50.23^Acute on chronic systolic heart failure^I10|||F|
DG1|2||I10^Essential hypertension^I10|||F|
DG1|3||E11.9^Type 2 diabetes mellitus^I10|||F|
DG1|4||N18.3^Chronic kidney disease stage 3^I10|||F|
```

### ADT^A02 - Patient Transfer
```
MSH|^~\&|HEALTHSIM|SPRINGFIELD_HOSP|EMR|MAIN_CAMPUS|20250112160000||ADT^A02|MSG20250112001|P|2.5|||AL|NE|
EVN|A02|20250112160000||||20250112160000|
PID|1||MRN00000001^^^SPRINGFIELD_HOSP^MR||THOMPSON^ELEANOR^MARIE||19500812|F|||456 OAK AVE^^SPRINGFIELD^IL^62702^USA||5559876543|||||||987654321|
PV1|1|I|ICU^105^B^^^SPRINGFIELD||||1234567890^JOHNSON^ROBERT^MD|||MED||||||||ENC0000000001|||||||||||||||||||20250110140000||||||
PV2|||^Transfer from Med/Surg for closer monitoring|||||||||||||||||||||||||||||||||
```

### ADT^A04 - Patient Registration (Outpatient)
```
MSH|^~\&|HEALTHSIM|SPRINGFIELD_HOSP|EMR|MAIN_CAMPUS|20250115080000||ADT^A04|MSG20250115004|P|2.5|||AL|NE|
EVN|A04|20250115080000||||20250115080000|
PID|1||MRN00000002^^^SPRINGFIELD_HOSP^MR||GARCIA^MARIA^ELENA||19780422|F|||123 ELM ST^^SPRINGFIELD^IL^62701^USA||5551234567|||||||555667788|
PV1|1|O|CLINIC^ENDO^1^^^SPRINGFIELD||||9876543210^CHEN^LISA^MD|||END||||||||ENC0000000002|||||||||||||||||||20250115080000||||||
DG1|1||E11.9^Type 2 diabetes mellitus^I10|||A|
IN1|1|BCBS^Blue Cross Blue Shield|12345|Blue Cross Illinois||||GROUP001||||20250101|20251231||||||||||||||||||MEM001234|
```

### ADT^A08 - Patient Update
```
MSH|^~\&|HEALTHSIM|SPRINGFIELD_HOSP|EMR|MAIN_CAMPUS|20250115090000||ADT^A08|MSG20250115003|P|2.5|||AL|NE|
EVN|A08|20250115090000||||20250115090000|
PID|1||MRN00000001^^^SPRINGFIELD_HOSP^MR||THOMPSON^ELEANOR^MARIE||19500812|F|||789 NEW ADDRESS^^SPRINGFIELD^IL^62703^USA||5551112222|||||||987654321|
PV1|1|I|ICU^105^B^^^SPRINGFIELD||||1234567890^JOHNSON^ROBERT^MD|||MED||||||||ENC0000000001|||||||||||||||||||20250110140000||||||
```

### ADT^A11 - Cancel Admission
```
MSH|^~\&|HEALTHSIM|SPRINGFIELD_HOSP|EMR|MAIN_CAMPUS|20250115110000||ADT^A11|MSG20250115005|P|2.5|||AL|NE|
EVN|A11|20250115110000||||20250115110000|
PID|1||MRN00000003^^^SPRINGFIELD_HOSP^MR||WILSON^JAMES^ROBERT||19650710|M|||555 MAPLE DR^^SPRINGFIELD^IL^62704^USA||5552223333|||||||112233445|
PV1|1|I|MED^301^A^^^SPRINGFIELD||||5678901234^PATEL^ARUN^MD|||MED||||||||ENC0000000003|||||||||||||||||||20250115080000||||||
```

## Encoding Rules

### Field Separators
| Character | Purpose | Position |
|-----------|---------|----------|
| `|` | Field separator | MSH-1 |
| `^` | Component separator | MSH-2.1 |
| `~` | Repetition separator | MSH-2.2 |
| `\` | Escape character | MSH-2.3 |
| `&` | Subcomponent separator | MSH-2.4 |

### Date/Time Formats
| Format | Example | Use |
|--------|---------|-----|
| YYYYMMDD | 20250115 | Date only |
| YYYYMMDDHHMMSS | 20250115143000 | Date and time |
| YYYYMMDDHHMMSS+ZZZZ | 20250115143000-0500 | With timezone |

### Escape Sequences
| Sequence | Character |
|----------|-----------|
| `\F\` | Field separator (|) |
| `\S\` | Component separator (^) |
| `\R\` | Repetition separator (~) |
| `\E\` | Escape character (\) |
| `\T\` | Subcomponent separator (&) |

## Transformation from JSON

### Input (HealthSim JSON)
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Eleanor", "family_name": "Thompson" },
    "birth_date": "1950-08-12",
    "gender": "F"
  },
  "encounter": {
    "encounter_id": "ENC0000000001",
    "class_code": "I",
    "admission_time": "2025-01-10T14:00:00",
    "discharge_time": "2025-01-15T10:00:00",
    "discharge_disposition": "01"
  },
  "diagnoses": [
    { "code": "I50.23", "description": "Acute on chronic systolic heart failure", "type": "final" }
  ]
}
```

### Output (HL7v2 ADT^A03)
```
MSH|^~\&|HEALTHSIM|FACILITY|EMR|DEST|20250115100000||ADT^A03|MSG001|P|2.5|||AL|NE|
EVN|A03|20250115100000||||20250115100000|
PID|1||MRN00000001^^^FACILITY^MR||THOMPSON^ELEANOR||19500812|F|
PV1|1|I|||||||||||||||||ENC0000000001|||||||||||||||||01||20250110140000|20250115100000|||||
DG1|1||I50.23^Acute on chronic systolic heart failure^I10|||F|
```

## Validation Rules

1. **MSH segment must be first**
2. **Required segments**: MSH, EVN, PID, PV1
3. **Date format**: YYYYMMDD or YYYYMMDDHHMMSS
4. **Message Control ID**: Must be unique
5. **Patient Class**: Must be valid (I, O, E, P, R, B, C)
6. **Discharge before admit**: PV1-45 must be >= PV1-44

## Related Skills

- [hl7v2-orm.md](hl7v2-orm.md) - HL7v2 Order messages
- [hl7v2-oru.md](hl7v2-oru.md) - HL7v2 Results messages
- [../references/hl7v2-segments.md](../references/hl7v2-segments.md) - Complete segment reference
- [fhir-r4.md](fhir-r4.md) - Modern FHIR format
- [../skills/patientsim/SKILL.md](../skills/patientsim/SKILL.md) - Patient data
- [../skills/patientsim/orders-results.md](../skills/patientsim/orders-results.md) - Orders and results scenario
