# HL7v2 ORM Order Message Format

## Trigger Phrases

- ORM
- HL7 order
- order message
- ORM O01
- lab order
- radiology order
- medication order
- new order
- cancel order

## Overview

HL7v2 ORM (Order Message) is used to transmit orders for laboratory tests, radiology procedures, medications, and other clinical services. This skill transforms HealthSim order entities into HL7v2 ORM messages.

## Message Types

| Event | Message Type | Description |
|-------|--------------|-------------|
| O01 | ORM^O01 | General Order Message |
| O02 | ORR^O02 | General Order Response |

## Order Control Codes

| Code | Description | Use Case |
|------|-------------|----------|
| NW | New Order | Initial order placement |
| OK | Order Accepted | Acknowledgment |
| CA | Cancel Order Request | Request to cancel |
| OC | Order Canceled | Confirmation of cancel |
| DC | Discontinue Order | Stop ongoing order |
| HD | Hold Order | Temporarily suspend |
| RL | Release Hold | Resume held order |
| XO | Change Order | Modify existing order |
| SC | Status Changed | Order status update |
| RE | Observations to Follow | Results coming |

## Message Structure

### ORM^O01 Segment Order
```
MSH - Message Header (required)
PID - Patient Identification (required)
PV1 - Patient Visit (optional)
ORC - Common Order (required, repeating)
  OBR - Observation Request (required with ORC)
  NTE - Notes (optional, repeating)
  OBX - Observation (optional, for order details)
```

## Key Segments

### ORC - Common Order

```
ORC|NW|ORD001234^EHR|LAB001234^LAB||SC||^^^^^R||20250115143022|1234567890^Smith^John^MD|||SPRINGFIELD^Main Campus||5551234567||ORD001234|20250115143022|
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Order Control | ORC-1 | NW, CA, DC, etc. | `NW` |
| Placer Order Number | ORC-2 | Ordering system ID | `ORD001234^EHR` |
| Filler Order Number | ORC-3 | Fulfilling system ID | `LAB001234^LAB` |
| Order Status | ORC-5 | SC, IP, CM, CA | `SC` |
| Quantity/Timing | ORC-7 | Priority/schedule | `^^^^^R` |
| Date/Time of Transaction | ORC-9 | When ordered | `20250115143022` |
| Entered By | ORC-10 | User who entered | |
| Verified By | ORC-11 | User who verified | |
| Ordering Provider | ORC-12 | Ordering physician | `1234567890^Smith^John^MD` |
| Ordering Facility | ORC-21 | Facility code^Name | `SPRINGFIELD^Main Campus` |
| Order Effective Date/Time | ORC-15 | When to execute | |
| Placer Group Number | ORC-4 | Group multiple orders | |

### OBR - Observation Request

```
OBR|1|ORD001234^EHR|LAB001234^LAB|80053^Comprehensive Metabolic Panel^CPT||20250115143022|20250115150000|||1234567890^Smith^John^MD|||Blood|||9876543210^Jones^Mary^MT||||||20250115160000|||F
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Set ID | OBR-1 | Sequence number | `1` |
| Placer Order Number | OBR-2 | Same as ORC-2 | `ORD001234^EHR` |
| Filler Order Number | OBR-3 | Same as ORC-3 | `LAB001234^LAB` |
| Universal Service ID | OBR-4 | Test/procedure code | `80053^CMP^CPT` |
| Priority | OBR-5 | R=Routine, S=STAT | `R` |
| Requested Date/Time | OBR-6 | When ordered | `20250115143022` |
| Observation Date/Time | OBR-7 | Specimen collection | `20250115150000` |
| Collector Identifier | OBR-10 | Who collected | |
| Specimen Received | OBR-14 | When specimen received | |
| Specimen Source | OBR-15 | Specimen type | `Blood` |
| Ordering Provider | OBR-16 | Same as ORC-12 | |
| Results Report Date | OBR-22 | When results ready | `20250115160000` |
| Result Status | OBR-25 | P, F, C, X | `F` |

## Order Types

### Laboratory Orders

| Code (CPT/LOINC) | Description | Specimen |
|------------------|-------------|----------|
| 80053 | Comprehensive Metabolic Panel | Blood |
| 80048 | Basic Metabolic Panel | Blood |
| 85025 | Complete Blood Count | Blood |
| 81001 | Urinalysis | Urine |
| 83036 | Hemoglobin A1C | Blood |
| 80061 | Lipid Panel | Blood |
| 84443 | TSH | Blood |
| 84450 | AST | Blood |
| 84460 | ALT | Blood |

### Radiology Orders

| Code (CPT) | Description | Modality |
|------------|-------------|----------|
| 71046 | Chest X-ray 2 views | XR |
| 70553 | MRI Brain with contrast | MR |
| 74177 | CT Abdomen/Pelvis with contrast | CT |
| 76700 | Ultrasound Abdomen complete | US |
| 71250 | CT Chest without contrast | CT |
| 72148 | MRI Lumbar Spine without contrast | MR |
| 73721 | MRI Lower Extremity joint | MR |
| 78452 | Nuclear Stress Test | NM |

### Priority Codes (OBR-5, ORC-7)

| Code | Description | Typical Turnaround |
|------|-------------|-------------------|
| S | STAT | < 1 hour |
| A | ASAP | 1-4 hours |
| R | Routine | 24-48 hours |
| P | Preoperative | Before surgery |
| C | Callback | Call with results |
| T | Timing Critical | Specific time required |

## Example Messages

### New Lab Order (ORM^O01)

```
MSH|^~\&|EHR|SPRINGFIELD_HOSP|LAB|MAIN_LAB|20250115143022||ORM^O01|MSG20250115001|P|2.5|||AL|NE|
PID|1||MRN00000001^^^SPRINGFIELD_HOSP^MR||SMITH^JOHN^MICHAEL||19700315|M|||123 MAIN ST^^SPRINGFIELD^IL^62701^USA||5551234567|||||||123456789|
PV1|1|I|MED^201^A^^^SPRINGFIELD||||1234567890^JOHNSON^ROBERT^MD|||MED||||||||ENC0000000001|||||||||||||||||||20250115080000||||||
ORC|NW|ORD001234^EHR|LAB001234^LAB||SC||^^^^^R||20250115143022|NURSE001^Williams^Sarah^RN||1234567890^Johnson^Robert^MD|||SPRINGFIELD^Main Hospital||5551234567|||||||
OBR|1|ORD001234^EHR|LAB001234^LAB|80053^Comprehensive Metabolic Panel^CPT|R|20250115143022|||||1234567890^Johnson^Robert^MD|||Blood^^Blood specimen|||||||||||||
NTE|1|L|Patient is fasting since midnight.
```

### STAT Lab Order

```
MSH|^~\&|EHR|SPRINGFIELD_HOSP|LAB|MAIN_LAB|20250115200000||ORM^O01|MSG20250115002|P|2.5|||AL|NE|
PID|1||MRN00000002^^^SPRINGFIELD_HOSP^MR||GARCIA^MARIA^ELENA||19551020|F|||456 OAK AVE^^SPRINGFIELD^IL^62702^USA||5559876543|||||||987654321|
PV1|1|E|ED^BAY5^1^^^SPRINGFIELD||||9876543210^CHEN^LISA^MD|||EM||||||||ENC0000000002|||||||||||||||||||20250115195500||||||
ORC|NW|ORD001235^EHR|LAB001235^LAB||SC||^^^^^S||20250115200000|||9876543210^Chen^Lisa^MD|||SPRINGFIELD^Emergency Dept|||||||||||
OBR|1|ORD001235^EHR|LAB001235^LAB|82374^Carbon Dioxide^CPT|S|20250115200000|||||9876543210^Chen^Lisa^MD|||Blood^^Venous blood|||||||||||||
OBR|2|ORD001235^EHR|LAB001236^LAB|84295^Sodium^CPT|S|20250115200000|||||9876543210^Chen^Lisa^MD|||Blood^^Venous blood|||||||||||||
OBR|3|ORD001235^EHR|LAB001237^LAB|84132^Potassium^CPT|S|20250115200000|||||9876543210^Chen^Lisa^MD|||Blood^^Venous blood|||||||||||||
```

### Radiology Order

```
MSH|^~\&|EHR|SPRINGFIELD_HOSP|RIS|RADIOLOGY|20250115101500||ORM^O01|MSG20250115003|P|2.5|||AL|NE|
PID|1||MRN00000003^^^SPRINGFIELD_HOSP^MR||THOMPSON^ELEANOR^MARIE||19500812|F|||789 ELM ST^^SPRINGFIELD^IL^62703^USA||5555551234|||||||111223344|
PV1|1|O|RAD^WAITING^1^^^SPRINGFIELD||||5678901234^PATEL^ARUN^MD|||RAD||||||||ENC0000000003|||||||||||||||||||20250115101500||||||
ORC|NW|ORD001236^EHR|RAD001236^RIS||SC||^^^^^R||20250115101500|||5678901234^Patel^Arun^MD|||SPRINGFIELD^Radiology Dept|||||||||||
OBR|1|ORD001236^EHR|RAD001236^RIS|71046^XR Chest 2 Views^CPT|R|20250115101500|||||5678901234^Patel^Arun^MD||||||||||||||||^Shortness of breath
DG1|1||R06.00^Dyspnea unspecified^I10|||W|
NTE|1|P|Rule out pneumonia. Patient has had cough x 3 days.
```

### Cancel Order

```
MSH|^~\&|EHR|SPRINGFIELD_HOSP|LAB|MAIN_LAB|20250115150000||ORM^O01|MSG20250115004|P|2.5|||AL|NE|
PID|1||MRN00000001^^^SPRINGFIELD_HOSP^MR||SMITH^JOHN^MICHAEL||19700315|M|||123 MAIN ST^^SPRINGFIELD^IL^62701^USA||5551234567|||||||123456789|
ORC|CA|ORD001234^EHR|LAB001234^LAB||CA||||||1234567890^Johnson^Robert^MD|||||||Duplicate order entered in error|||||||||
OBR|1|ORD001234^EHR|LAB001234^LAB|80053^Comprehensive Metabolic Panel^CPT||20250115143022|||||1234567890^Johnson^Robert^MD|||||||||||||||||
```

### Medication Order

```
MSH|^~\&|EHR|SPRINGFIELD_HOSP|PHARMACY|MAIN_PHARM|20250115090000||ORM^O01|MSG20250115005|P|2.5|||AL|NE|
PID|1||MRN00000004^^^SPRINGFIELD_HOSP^MR||WILSON^JAMES^ROBERT||19650710|M|||555 MAPLE DR^^SPRINGFIELD^IL^62704^USA||5552223333|||||||445566778|
PV1|1|I|MED^301^A^^^SPRINGFIELD||||1234567890^Johnson^Robert^MD|||MED||||||||ENC0000000004|||||||||||||||||||20250115080000||||||
ORC|NW|ORD001237^EHR|RX001237^PHARM||SC||1^QD^D^20250115090000^20250120090000^R^Lisinopril 10mg daily||20250115090000|||1234567890^Johnson^Robert^MD|||SPRINGFIELD^Main Hospital|||||||||||
RXO|00093-5056-01^Lisinopril 10mg Tab^NDC|10||mg||PO|1|TAB|0|30|||1234567890^Johnson^Robert^MD|||||||||E11.9~I10|
RXR|PO^Oral^HL70162|
```

## Order Status Flow

```
NW (New Order)
    ↓
OK (Accepted) or UA (Unable to Accept)
    ↓
SC (Scheduled) → HD (Hold) → RL (Release)
    ↓
IP (In Progress)
    ↓
CM (Complete) or CA (Canceled)
```

## Transformation from JSON

### Input (HealthSim Order)
```json
{
  "order": {
    "order_id": "ORD001234",
    "order_type": "LAB",
    "status": "new",
    "priority": "routine",
    "ordered_datetime": "2025-01-15T14:30:22",
    "ordering_provider": {
      "npi": "1234567890",
      "name": { "given_name": "Robert", "family_name": "Johnson" }
    },
    "tests": [
      {
        "code": "80053",
        "name": "Comprehensive Metabolic Panel",
        "specimen_type": "Blood"
      }
    ]
  },
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "John", "family_name": "Smith" }
  }
}
```

### Output (HL7v2 ORM^O01)
```
MSH|^~\&|EHR|FACILITY|LAB|LAB_SYSTEM|20250115143022||ORM^O01|MSG001|P|2.5|||AL|NE|
PID|1||MRN00000001^^^FACILITY^MR||SMITH^JOHN||||||||||||||
ORC|NW|ORD001234^EHR|||SC||^^^^^R||20250115143022|||1234567890^Johnson^Robert^MD|||||||||||||||
OBR|1|ORD001234^EHR||80053^Comprehensive Metabolic Panel^CPT|R|20250115143022|||||1234567890^Johnson^Robert^MD|||Blood|||||||||||||
```

## Validation Rules

1. **ORC-1 required**: Order Control code must be present
2. **ORC-2 or ORC-3 required**: At least one order number needed
3. **OBR-4 required**: Universal Service ID must be present
4. **Provider NPI**: Must be valid 10-digit NPI
5. **Date/Time format**: YYYYMMDDHHMMSS
6. **Priority codes**: Must be S, A, R, P, C, or T

## Acknowledgment (ORR^O02)

```
MSH|^~\&|LAB|MAIN_LAB|EHR|SPRINGFIELD_HOSP|20250115143100||ORR^O02|MSG20250115101|P|2.5|||AL|NE|
MSA|AA|MSG20250115001|Order received successfully
ORC|OK|ORD001234^EHR|LAB001234^LAB||SC||^^^^^R||20250115143100|||||||||||||||||||
```

## Related Skills

- [hl7v2-adt.md](hl7v2-adt.md) - ADT messages
- [hl7v2-oru.md](hl7v2-oru.md) - Results messages
- [../references/hl7v2-segments.md](../references/hl7v2-segments.md) - Segment reference
- [../references/code-systems.md](../references/code-systems.md) - CPT, LOINC codes
- [../skills/patientsim/orders-results.md](../skills/patientsim/orders-results.md) - Orders scenario
