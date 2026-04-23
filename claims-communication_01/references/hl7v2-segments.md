# HL7v2 Segments Reference

## Overview

This reference defines HL7v2 segment structures used across ADT, ORM, and ORU message types. All segments follow HL7 v2.5.1 specification.

## Common Segments

### MSH - Message Header

Required in all messages. Defines message metadata.

```
MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|YYYYMMDDHHMMSS||MessageType^TriggerEvent^Structure|ControlID|P|2.5.1|||AL|NE||
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| MSH-1 | Field Separator | Always pipe | `|` |
| MSH-2 | Encoding Characters | Component, repetition, escape, subcomponent | `^~\&` |
| MSH-3 | Sending Application | Source system | `HEALTHSIM` |
| MSH-4 | Sending Facility | Source facility | `HOSPITAL` |
| MSH-5 | Receiving Application | Destination system | `EMR` |
| MSH-6 | Receiving Facility | Destination facility | `CLINIC` |
| MSH-7 | Date/Time of Message | YYYYMMDDHHMMSS | `20250115143022` |
| MSH-9 | Message Type | Type^Event^Structure | `ADT^A01^ADT_A01` |
| MSH-10 | Message Control ID | Unique identifier | `MSG00001234` |
| MSH-11 | Processing ID | P=Production, T=Training, D=Debug | `P` |
| MSH-12 | Version ID | HL7 version | `2.5.1` |
| MSH-15 | Accept Ack Type | AL=Always, NE=Never, ER=Error | `AL` |
| MSH-16 | Application Ack Type | AL=Always, NE=Never | `NE` |

### EVN - Event Type

Event information segment.

```
EVN|A01|20250115143022||ADMIT|1234567890^Smith^John^MD^^^DR|20250115143000|HOSPITAL
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| EVN-1 | Event Type Code | Event that triggered message | `A01` |
| EVN-2 | Recorded Date/Time | When event was recorded | `20250115143022` |
| EVN-4 | Event Reason Code | Reason for event | `ADMIT` |
| EVN-5 | Operator ID | User who entered event | `NPI^Last^First^Suffix^^^Role` |
| EVN-6 | Event Occurred | When event actually occurred | `20250115143000` |
| EVN-7 | Event Facility | Where event occurred | `HOSPITAL` |

### PID - Patient Identification

Patient demographics. Required in most messages.

```
PID|1||PAT001234^^^HOSPITAL^MR||Smith^John^Michael^^Mr.||19700315|M||2106-3^White^CDCREC|123 Main St^^Springfield^IL^62701^USA||5551234567^PRN^PH|5559876543^WPN^PH|ENG|M|CHR|SSN123456789^^^SSA^SS||123-45-6789||||||||N
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| PID-1 | Set ID | Sequence number | `1` |
| PID-3 | Patient Identifier List | ID^^^Authority^Type | `PAT001234^^^HOSPITAL^MR` |
| PID-5 | Patient Name | Family^Given^Middle^Suffix^Prefix | `Smith^John^Michael^^Mr.` |
| PID-7 | Date of Birth | YYYYMMDD | `19700315` |
| PID-8 | Sex | M, F, O, U, A, N | `M` |
| PID-10 | Race | Code^Text^System | `2106-3^White^CDCREC` |
| PID-11 | Patient Address | Street^^City^State^Zip^Country | `123 Main St^^Springfield^IL^62701^USA` |
| PID-13 | Home Phone | Number^Use^Type | `5551234567^PRN^PH` |
| PID-14 | Business Phone | Number^Use^Type | `5559876543^WPN^PH` |
| PID-15 | Primary Language | Code | `ENG` |
| PID-16 | Marital Status | S, M, D, W, A, P, I, U | `M` |
| PID-17 | Religion | Code | `CHR` |
| PID-18 | Patient Account Number | Account^^^Authority^Type | `ACCT001^^^HOSPITAL^AN` |
| PID-19 | SSN | Social Security Number | `123-45-6789` |
| PID-30 | Patient Death Indicator | Y/N | `N` |

### PV1 - Patient Visit

Encounter/visit information.

```
PV1|1|I|ICU^101^A^^^N||||1234567890^Smith^John^MD^^^NPI^L^^^NPI|5678901234^Jones^Mary^NP^^^NPI||MED|||A|||9876543210^Brown^Robert^MD|||||||||||||||||||HOSPITAL||ADM|||20250115140000|
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| PV1-1 | Set ID | Sequence number | `1` |
| PV1-2 | Patient Class | I=Inpatient, O=Outpatient, E=Emergency | `I` |
| PV1-3 | Assigned Location | Unit^Room^Bed^^^Building | `ICU^101^A^^^N` |
| PV1-4 | Admission Type | E=Emergency, U=Urgent, R=Routine | `E` |
| PV1-7 | Attending Doctor | NPI^Last^First^Middle^Suffix^Prefix^Type^Source | `1234567890^Smith^John^MD^^^NPI` |
| PV1-8 | Referring Doctor | Same format as PV1-7 | |
| PV1-9 | Consulting Doctor | Same format as PV1-7 | |
| PV1-10 | Hospital Service | Medical service code | `MED` |
| PV1-14 | Admit Source | 1=Physician, 2=Clinic, 7=ER | `7` |
| PV1-15 | Ambulatory Status | A=Ambulatory | `A` |
| PV1-17 | Admitting Doctor | Same format as PV1-7 | |
| PV1-19 | Visit Number | Encounter ID | `ENC20250115001` |
| PV1-36 | Discharge Disposition | 01=Home, 02=SNF, 20=Expired | `01` |
| PV1-39 | Servicing Facility | Facility code | `HOSPITAL` |
| PV1-44 | Admit Date/Time | YYYYMMDDHHMMSS | `20250115140000` |
| PV1-45 | Discharge Date/Time | YYYYMMDDHHMMSS | |

### PV2 - Patient Visit Additional Info

Extended visit details.

```
PV2|||^Chest Pain||||||20250115||||||||||||||||||||||||V
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| PV2-3 | Admit Reason | Code^Text | `^Chest Pain` |
| PV2-8 | Expected Admit Date | YYYYMMDD | `20250115` |
| PV2-38 | Mode of Arrival | A=Ambulance, C=Car, W=Walk | `A` |

### DG1 - Diagnosis

Diagnosis information. Repeatable.

```
DG1|1|I10|I10^Essential Hypertension^ICD10||20250115|A||||||||||1234567890^Smith^John^MD
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| DG1-1 | Set ID | Sequence number | `1` |
| DG1-2 | Diagnosis Coding Method | I10=ICD-10 | `I10` |
| DG1-3 | Diagnosis Code | Code^Text^System | `I10^Essential Hypertension^ICD10` |
| DG1-5 | Diagnosis Date/Time | YYYYMMDD | `20250115` |
| DG1-6 | Diagnosis Type | A=Admitting, F=Final, W=Working | `A` |
| DG1-15 | Diagnosis Priority | 1=Primary, 2+=Secondary | `1` |
| DG1-16 | Diagnosing Clinician | NPI^Last^First^Suffix | |

### AL1 - Allergy Information

Patient allergies. Repeatable.

```
AL1|1|DA|70618^Penicillin^RxNorm|SV|Anaphylaxis|20150320
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| AL1-1 | Set ID | Sequence number | `1` |
| AL1-2 | Allergen Type | DA=Drug, FA=Food, EA=Environmental | `DA` |
| AL1-3 | Allergen Code | Code^Text^System | `70618^Penicillin^RxNorm` |
| AL1-4 | Severity | SV=Severe, MO=Moderate, MI=Mild | `SV` |
| AL1-5 | Reaction | Reaction description | `Anaphylaxis` |
| AL1-6 | Identification Date | YYYYMMDD | `20150320` |

### IN1 - Insurance

Insurance information. Repeatable for multiple coverages.

```
IN1|1|BCBS^Blue Cross Blue Shield|12345|Blue Cross of Illinois|PO Box 1234^^Chicago^IL^60601|8005551234|GROUP001||Health Plan|||20250101|20251231||SELF|Smith^John||19700315|123 Main St^^Springfield^IL^62701|||1||||||||||||||MEM001234||||||M
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| IN1-1 | Set ID | Sequence number (1=Primary) | `1` |
| IN1-2 | Insurance Plan ID | Plan Code^Name | `BCBS^Blue Cross` |
| IN1-3 | Insurance Company ID | Payer ID | `12345` |
| IN1-4 | Insurance Company Name | Payer name | `Blue Cross of Illinois` |
| IN1-5 | Insurance Company Address | Address | |
| IN1-8 | Group Number | Group ID | `GROUP001` |
| IN1-12 | Plan Effective Date | YYYYMMDD | `20250101` |
| IN1-13 | Plan Expiration Date | YYYYMMDD | `20251231` |
| IN1-16 | Insured Name | Same as PID-5 format | |
| IN1-18 | Insured DOB | YYYYMMDD | |
| IN1-36 | Policy Number | Member ID | `MEM001234` |
| IN1-43 | Insured Sex | M, F, O, U | `M` |

## Order Segments (ORM)

### ORC - Common Order

Order control segment.

```
ORC|NW|ORD001234^EHR|LAB001234^LAB||SC||^^^^^R||20250115143022|1234567890^Smith^John^MD|||||HOSPITAL^Main Hospital
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| ORC-1 | Order Control | NW=New, CA=Cancel, DC=Discontinue, XO=Change | `NW` |
| ORC-2 | Placer Order Number | ID^Application | `ORD001234^EHR` |
| ORC-3 | Filler Order Number | ID^Application | `LAB001234^LAB` |
| ORC-5 | Order Status | SC=Scheduled, IP=In Progress, CM=Complete, CA=Canceled | `SC` |
| ORC-6 | Response Flag | Always populate | |
| ORC-7 | Quantity/Timing | Priority | `^^^^^R` (Routine) |
| ORC-9 | Date/Time of Transaction | YYYYMMDDHHMMSS | `20250115143022` |
| ORC-10 | Entered By | Ordering provider | |
| ORC-12 | Ordering Provider | NPI^Last^First^Suffix | `1234567890^Smith^John^MD` |
| ORC-21 | Ordering Facility | Facility code^Name | `HOSPITAL^Main Hospital` |

### OBR - Observation Request

Observation/test request details.

```
OBR|1|ORD001234^EHR|LAB001234^LAB|80053^Comprehensive Metabolic Panel^CPT||20250115143022|20250115150000|||1234567890^Smith^John^MD||||Blood|||5678901234^Jones^Mary^MT||||||20250115160000|||F|||||||1234567890^Smith^John^MD
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| OBR-1 | Set ID | Sequence number | `1` |
| OBR-2 | Placer Order Number | Same as ORC-2 | |
| OBR-3 | Filler Order Number | Same as ORC-3 | |
| OBR-4 | Universal Service ID | Code^Text^System | `80053^Comprehensive Metabolic Panel^CPT` |
| OBR-6 | Requested Date/Time | YYYYMMDDHHMMSS | `20250115143022` |
| OBR-7 | Observation Date/Time | Specimen collection time | `20250115150000` |
| OBR-10 | Collector Identifier | Who collected specimen | |
| OBR-15 | Specimen Source | Specimen type | `Blood` |
| OBR-16 | Ordering Provider | Same as ORC-12 | |
| OBR-22 | Results Report Date/Time | When results available | `20250115160000` |
| OBR-25 | Result Status | P=Preliminary, F=Final, C=Corrected | `F` |
| OBR-32 | Principal Result Interpreter | Resulted by | |

## Observation Segments (ORU)

### OBX - Observation/Result

Individual observation/result values. Repeatable.

```
OBX|1|NM|2345-7^Glucose^LN||98|mg/dL|70-100|N|||F|||20250115150000||1234567890^Smith^John^MT
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| OBX-1 | Set ID | Sequence number | `1` |
| OBX-2 | Value Type | NM=Numeric, ST=String, CE=Coded, TX=Text | `NM` |
| OBX-3 | Observation Identifier | Code^Text^System | `2345-7^Glucose^LN` |
| OBX-4 | Observation Sub-ID | For related observations | |
| OBX-5 | Observation Value | The result value | `98` |
| OBX-6 | Units | Unit of measure | `mg/dL` |
| OBX-7 | Reference Range | Normal range | `70-100` |
| OBX-8 | Abnormal Flags | N=Normal, L=Low, H=High, A=Abnormal | `N` |
| OBX-11 | Observation Result Status | P=Preliminary, F=Final, C=Corrected | `F` |
| OBX-14 | Date/Time of Observation | YYYYMMDDHHMMSS | `20250115150000` |
| OBX-16 | Responsible Observer | Performed by | |

### Value Type Codes (OBX-2)

| Code | Type | Example Use |
|------|------|-------------|
| NM | Numeric | Lab values, vitals |
| ST | String | Text results |
| CE | Coded Entry | Coded findings |
| TX | Text | Narrative text |
| FT | Formatted Text | Rich text |
| ED | Encapsulated Data | Images, PDFs |
| RP | Reference Pointer | External reference |
| SN | Structured Numeric | Complex numeric |
| CWE | Coded with Exceptions | Coded + text |
| DTM | Date/Time | Temporal values |

### Abnormal Flags (OBX-8)

| Flag | Meaning | Description |
|------|---------|-------------|
| N | Normal | Within reference range |
| L | Low | Below reference range |
| H | High | Above reference range |
| LL | Critical Low | Critically low |
| HH | Critical High | Critically high |
| A | Abnormal | Abnormal (non-numeric) |
| AA | Critically Abnormal | Critical abnormal |
| < | Below Detection | Below measurable limit |
| > | Above Detection | Above measurable limit |

### NTE - Notes and Comments

Free-text notes. Repeatable.

```
NTE|1|L|Patient was fasting for 12 hours prior to specimen collection.
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| NTE-1 | Set ID | Sequence number | `1` |
| NTE-2 | Source of Comment | L=Lab, P=Provider, O=Other | `L` |
| NTE-3 | Comment | Free text | `Patient was fasting...` |

## Specimen Segments

### SPM - Specimen

Specimen details (HL7 v2.5+).

```
SPM|1|SPM001234^EHR||119297000^Blood specimen^SCT|||||||||||||20250115150000|20250115150500
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| SPM-1 | Set ID | Sequence number | `1` |
| SPM-2 | Specimen ID | Specimen identifier | `SPM001234^EHR` |
| SPM-4 | Specimen Type | Code^Text^System | `119297000^Blood specimen^SCT` |
| SPM-17 | Specimen Collection Date/Time | YYYYMMDDHHMMSS | `20250115150000` |
| SPM-18 | Specimen Received Date/Time | YYYYMMDDHHMMSS | `20250115150500` |

## Pharmacy/Medication Segments

### RXA - Pharmacy/Treatment Administration

Medication administration.

```
RXA|0|1|20250115140000|20250115140000|0993-5056-01^Lisinopril 10mg Tablet^NDC|1||TAB||1234567890^Smith^John^RN|||||||20260115|A
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| RXA-1 | Give Sub-ID Counter | Always 0 | `0` |
| RXA-2 | Administration Sub-ID | Sequence | `1` |
| RXA-3 | Date/Time Start | When started | `20250115140000` |
| RXA-4 | Date/Time End | When completed | `20250115140000` |
| RXA-5 | Administered Code | Code^Text^System | NDC or RxNorm |
| RXA-6 | Administered Amount | Quantity | `1` |
| RXA-7 | Administered Units | Unit | `TAB` |
| RXA-10 | Administering Provider | Who gave | |
| RXA-18 | Substance/Treatment Refusal Reason | Refusal reason | |
| RXA-20 | Completion Status | CP=Complete, RE=Refused, NA=Not Administered | `A` |

### RXE - Pharmacy/Treatment Encoded Order

Medication order details.

```
RXE|^^^^^R|0993-5056-01^Lisinopril 10mg Tablet^NDC|10||mg|TAB|||30||0||1234567890^Smith^John^MD|||||20250115|100|||||||PHARMACY01
```

| Field | Name | Description | Example |
|-------|------|-------------|---------|
| RXE-1 | Quantity/Timing | Priority/timing | `^^^^^R` |
| RXE-2 | Give Code | Code^Text^System | NDC or RxNorm |
| RXE-3 | Give Amount - Minimum | Dose | `10` |
| RXE-5 | Give Units | Unit of dose | `mg` |
| RXE-6 | Give Dosage Form | Form | `TAB` |
| RXE-10 | Dispense Amount | Quantity to dispense | `30` |
| RXE-13 | Ordering Provider's DEA Number | DEA | |
| RXE-14 | Pharmacist Verifier ID | Verified by | |
| RXE-19 | Needs Human Review | Y/N | |
| RXE-31 | Dispense Package Method | Package type | |

## Common Code Tables

### Patient Class (PV1-2)

| Code | Description |
|------|-------------|
| I | Inpatient |
| O | Outpatient |
| E | Emergency |
| P | Preadmit |
| R | Recurring |
| B | Obstetrics |
| C | Commercial |
| N | Not Applicable |
| U | Unknown |

### Admit Source (PV1-14)

| Code | Description |
|------|-------------|
| 1 | Physician Referral |
| 2 | Clinic Referral |
| 3 | HMO Referral |
| 4 | Transfer from Hospital |
| 5 | Transfer from SNF |
| 6 | Transfer from Another Facility |
| 7 | Emergency Room |
| 8 | Court/Law Enforcement |
| 9 | Information Not Available |

### Discharge Disposition (PV1-36)

| Code | Description |
|------|-------------|
| 01 | Discharged to Home |
| 02 | Discharged to Short-term Hospital |
| 03 | Discharged to SNF |
| 04 | Discharged to ICF |
| 05 | Discharged to Another Type of Institution |
| 06 | Discharged Home Under Care of Home Health |
| 07 | Left Against Medical Advice |
| 20 | Expired |
| 30 | Still Patient |
| 43 | Discharged to Federal Hospital |
| 50 | Hospice - Home |
| 51 | Hospice - Medical Facility |

### Order Control (ORC-1)

| Code | Description |
|------|-------------|
| NW | New Order |
| OK | Order Accepted |
| CA | Cancel Order |
| OC | Order Canceled |
| DC | Discontinue Order |
| HD | Hold Order |
| RL | Release Hold |
| XO | Change Order |
| RU | Replaced Unsolicited |
| RE | Observations to Follow |
| SC | Status Changed |

### Result Status (OBR-25, OBX-11)

| Code | Description |
|------|-------------|
| O | Order Received |
| I | Specimen In Lab |
| S | Scheduled |
| A | Some Results Available |
| P | Preliminary |
| C | Corrected |
| R | Results Stored |
| F | Final |
| X | Order Canceled |

## Related Skills

- [../formats/hl7v2-adt.md](../formats/hl7v2-adt.md) - ADT message formatting
- [../formats/hl7v2-orm.md](../formats/hl7v2-orm.md) - Order message formatting
- [../formats/hl7v2-oru.md](../formats/hl7v2-oru.md) - Results message formatting
- [code-systems.md](code-systems.md) - Code systems (LOINC, CPT, etc.)
