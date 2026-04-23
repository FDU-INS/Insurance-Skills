# HL7v2 ORU Observation/Result Message Format

## Trigger Phrases

- ORU
- HL7 result
- lab result message
- observation message
- ORU R01
- lab results
- test results
- radiology report
- pathology result

## Overview

HL7v2 ORU (Observation Result Unsolicited) is used to transmit clinical observations and test results from laboratories, radiology, and other diagnostic systems. This skill transforms HealthSim observation entities into HL7v2 ORU messages.

## Message Types

| Event | Message Type | Description |
|-------|--------------|-------------|
| R01 | ORU^R01 | Unsolicited Observation Message |
| R03 | ORU^R03 | Display Oriented Results (Query Response) |
| R30 | ORU^R30 | Unsolicited Point-of-Care Observation |
| R31 | ORU^R31 | Unsolicited New Point-of-Care Device |
| R32 | ORU^R32 | Unsolicited Pre-Ordered Point-of-Care |

## Message Structure

### ORU^R01 Segment Order
```
MSH - Message Header (required)
PID - Patient Identification (required)
PV1 - Patient Visit (optional)
ORC - Common Order (optional)
OBR - Observation Request (required)
  OBX - Observation/Result (required, repeating)
  NTE - Notes (optional, repeating)
  SPM - Specimen (optional)
```

## Key Segments

### OBR - Observation Request (Results Context)

```
OBR|1|ORD001234^EHR|LAB001234^LAB|80053^Comprehensive Metabolic Panel^CPT||20250115143022|20250115150000|||1234567890^Johnson^Robert^MD|||Blood|||9876543210^Jones^Mary^MT||||||20250115160000|||F|||||||9876543210^Jones^Mary^MT
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Set ID | OBR-1 | Sequence number | `1` |
| Placer Order Number | OBR-2 | Original order ID | `ORD001234^EHR` |
| Filler Order Number | OBR-3 | Lab accession number | `LAB001234^LAB` |
| Universal Service ID | OBR-4 | Test/panel code | `80053^CMP^CPT` |
| Requested Date/Time | OBR-6 | When ordered | `20250115143022` |
| Observation Date/Time | OBR-7 | Specimen collected | `20250115150000` |
| Ordering Provider | OBR-16 | Ordering physician | |
| Results Report Date/Time | OBR-22 | When results reported | `20250115160000` |
| Result Status | OBR-25 | P=Preliminary, F=Final | `F` |
| Principal Result Interpreter | OBR-32 | Pathologist/Radiologist | |

### OBX - Observation/Result

```
OBX|1|NM|2345-7^Glucose^LN||98|mg/dL|70-100|N|||F|||20250115150000||9876543210^Jones^Mary^MT
```

| Field | Position | Description | Example |
|-------|----------|-------------|---------|
| Set ID | OBX-1 | Sequence number | `1` |
| Value Type | OBX-2 | NM, ST, CE, TX, etc. | `NM` |
| Observation Identifier | OBX-3 | LOINC code | `2345-7^Glucose^LN` |
| Observation Sub-ID | OBX-4 | For related results | |
| Observation Value | OBX-5 | The result | `98` |
| Units | OBX-6 | Unit of measure | `mg/dL` |
| Reference Range | OBX-7 | Normal range | `70-100` |
| Abnormal Flags | OBX-8 | N, L, H, LL, HH, A | `N` |
| Result Status | OBX-11 | P, F, C, X | `F` |
| Observation Date/Time | OBX-14 | When observed | `20250115150000` |
| Responsible Observer | OBX-16 | Who performed | |
| Producer's ID | OBX-15 | Performing lab | |

## Value Types (OBX-2)

| Code | Type | Description | Example Use |
|------|------|-------------|-------------|
| NM | Numeric | Quantitative results | Lab values, vitals |
| ST | String | Simple text | Text results |
| TX | Text | Multi-line text | Reports, comments |
| CE | Coded Entry | Code^Text^System | Coded findings |
| CWE | Coded with Exceptions | Code with extensions | Flexible coding |
| SN | Structured Numeric | Comparator + number | `>100`, `<0.5` |
| FT | Formatted Text | Rich text | Narrative reports |
| ED | Encapsulated Data | Binary content | Images, PDFs |
| RP | Reference Pointer | External reference | Image links |
| DTM | Date/Time | Temporal value | Event times |

## Abnormal Flags (OBX-8)

| Flag | Description | Clinical Significance |
|------|-------------|----------------------|
| N | Normal | Within reference range |
| L | Low | Below reference range |
| H | High | Above reference range |
| LL | Critical Low | Critically low - immediate action |
| HH | Critical High | Critically high - immediate action |
| A | Abnormal | Abnormal (non-directional) |
| AA | Critical Abnormal | Critically abnormal |
| U | Significant Change Up | Increased from previous |
| D | Significant Change Down | Decreased from previous |
| < | Below Absolute Low | Below detectable limit |
| > | Above Absolute High | Above measurable limit |
| S | Susceptible | Microbiology |
| R | Resistant | Microbiology |
| I | Intermediate | Microbiology |

## Result Status Codes (OBR-25, OBX-11)

| Code | Description | Action |
|------|-------------|--------|
| O | Order Received | Pending |
| I | Specimen In Lab | Processing |
| S | Scheduled | Awaiting collection |
| A | Some Results Available | Partial |
| P | Preliminary | Subject to change |
| C | Corrected | Replaces previous |
| R | Results Stored | Not yet verified |
| F | Final | Complete, verified |
| X | Canceled | Order canceled |
| W | Wrong/Unable | Error in processing |

## Example Messages

### Complete Metabolic Panel (Final)

```
MSH|^~\&|LAB|MAIN_LAB|EHR|SPRINGFIELD_HOSP|20250115160000||ORU^R01|MSG20250115001|P|2.5|||AL|NE|
PID|1||MRN00000001^^^SPRINGFIELD_HOSP^MR||SMITH^JOHN^MICHAEL||19700315|M|||123 MAIN ST^^SPRINGFIELD^IL^62701^USA||5551234567|||||||123456789|
PV1|1|I|MED^201^A^^^SPRINGFIELD||||1234567890^Johnson^Robert^MD|||MED||||||||ENC0000000001|
ORC|RE|ORD001234^EHR|LAB001234^LAB||CM||||||1234567890^Johnson^Robert^MD|||||||||||||||
OBR|1|ORD001234^EHR|LAB001234^LAB|80053^Comprehensive Metabolic Panel^CPT||20250115143022|20250115150000|||1234567890^Johnson^Robert^MD|||Blood^^Blood specimen|||9876543210^Jones^Mary^MT||||||20250115160000|||F|||||||9876543210^Jones^Mary^MT
OBX|1|NM|2345-7^Glucose^LN||98|mg/dL|70-100|N|||F|||20250115150000||9876543210
OBX|2|NM|3094-0^BUN^LN||18|mg/dL|7-20|N|||F|||20250115150000||9876543210
OBX|3|NM|2160-0^Creatinine^LN||1.1|mg/dL|0.7-1.3|N|||F|||20250115150000||9876543210
OBX|4|NM|2951-2^Sodium^LN||140|mmol/L|136-145|N|||F|||20250115150000||9876543210
OBX|5|NM|2823-3^Potassium^LN||4.2|mmol/L|3.5-5.0|N|||F|||20250115150000||9876543210
OBX|6|NM|2075-0^Chloride^LN||102|mmol/L|98-106|N|||F|||20250115150000||9876543210
OBX|7|NM|1963-8^Bicarbonate^LN||24|mmol/L|22-29|N|||F|||20250115150000||9876543210
OBX|8|NM|17861-6^Calcium^LN||9.5|mg/dL|8.6-10.2|N|||F|||20250115150000||9876543210
OBX|9|NM|2885-2^Total Protein^LN||7.0|g/dL|6.0-8.3|N|||F|||20250115150000||9876543210
OBX|10|NM|1751-7^Albumin^LN||4.0|g/dL|3.5-5.0|N|||F|||20250115150000||9876543210
OBX|11|NM|1975-2^Bilirubin Total^LN||0.8|mg/dL|0.1-1.2|N|||F|||20250115150000||9876543210
OBX|12|NM|6768-6^Alk Phos^LN||75|U/L|44-147|N|||F|||20250115150000||9876543210
OBX|13|NM|1742-6^ALT^LN||25|U/L|7-56|N|||F|||20250115150000||9876543210
OBX|14|NM|1920-8^AST^LN||22|U/L|10-40|N|||F|||20250115150000||9876543210
OBX|15|NM|33914-3^eGFR^LN||78|mL/min/1.73m2|>60|N|||F|||20250115150000||9876543210
NTE|1|L|All results within normal limits.
```

### Critical Lab Result

```
MSH|^~\&|LAB|MAIN_LAB|EHR|SPRINGFIELD_HOSP|20250115201500||ORU^R01|MSG20250115002|P|2.5|||AL|NE|
PID|1||MRN00000002^^^SPRINGFIELD_HOSP^MR||GARCIA^MARIA^ELENA||19551020|F|||456 OAK AVE^^SPRINGFIELD^IL^62702^USA||5559876543|||||||987654321|
PV1|1|E|ED^BAY5^1^^^SPRINGFIELD||||9876543210^Chen^Lisa^MD|||EM||||||||ENC0000000002|
OBR|1|ORD001235^EHR|LAB001235^LAB|2823-3^Potassium^LN||20250115200000|20250115200500|||||9876543210^Chen^Lisa^MD|||Blood|||5678901234^Tech^Lab^MT||||||20250115201500|||F
OBX|1|NM|2823-3^Potassium^LN||6.8|mmol/L|3.5-5.0|HH|||F|||20250115200500||5678901234
NTE|1|L|CRITICAL VALUE - Physician notified at 20:15. Dr. Chen acknowledged.
```

### CBC with Differential

```
MSH|^~\&|LAB|MAIN_LAB|EHR|SPRINGFIELD_HOSP|20250115140000||ORU^R01|MSG20250115003|P|2.5|||AL|NE|
PID|1||MRN00000003^^^SPRINGFIELD_HOSP^MR||THOMPSON^ELEANOR^MARIE||19500812|F|||789 ELM ST^^SPRINGFIELD^IL^62703^USA||5555551234|
OBR|1|ORD001236^EHR|LAB001236^LAB|85025^CBC with Differential^CPT||20250115130000|20250115133000|||||||Blood|||||||20250115140000|||F
OBX|1|NM|6690-2^WBC^LN||7.5|10*3/uL|4.5-11.0|N|||F|||20250115133000
OBX|2|NM|789-8^RBC^LN||4.2|10*6/uL|4.0-5.5|N|||F|||20250115133000
OBX|3|NM|718-7^Hemoglobin^LN||12.8|g/dL|12.0-16.0|N|||F|||20250115133000
OBX|4|NM|4544-3^Hematocrit^LN||38.5|%|36-46|N|||F|||20250115133000
OBX|5|NM|787-2^MCV^LN||88|fL|80-100|N|||F|||20250115133000
OBX|6|NM|785-6^MCH^LN||29|pg|27-33|N|||F|||20250115133000
OBX|7|NM|786-4^MCHC^LN||33|g/dL|32-36|N|||F|||20250115133000
OBX|8|NM|788-0^RDW^LN||13.5|%|11.5-14.5|N|||F|||20250115133000
OBX|9|NM|777-3^Platelets^LN||250|10*3/uL|150-400|N|||F|||20250115133000
OBX|10|NM|770-8^Neutrophils %^LN||62|%|40-70|N|||F|||20250115133000
OBX|11|NM|736-9^Lymphocytes %^LN||28|%|20-40|N|||F|||20250115133000
OBX|12|NM|5905-5^Monocytes %^LN||7|%|2-8|N|||F|||20250115133000
OBX|13|NM|713-8^Eosinophils %^LN||2|%|1-4|N|||F|||20250115133000
OBX|14|NM|706-2^Basophils %^LN||1|%|0-2|N|||F|||20250115133000
```

### Radiology Report

```
MSH|^~\&|RIS|RADIOLOGY|EHR|SPRINGFIELD_HOSP|20250115120000||ORU^R01|MSG20250115004|P|2.5|||AL|NE|
PID|1||MRN00000003^^^SPRINGFIELD_HOSP^MR||THOMPSON^ELEANOR^MARIE||19500812|F|||789 ELM ST^^SPRINGFIELD^IL^62703^USA||5555551234|
OBR|1|ORD001236^EHR|RAD001236^RIS|71046^XR Chest 2 Views^CPT||20250115101500|20250115110000|||||5678901234^Patel^Arun^MD||||||4567890123^WILLIAMS^SARAH^MD||||||20250115120000|||F|||||||4567890123^WILLIAMS^SARAH^MD
OBX|1|TX|71046&IMP^Impression^LN||Lungs are clear. No pneumothorax or pleural effusion. Heart size is normal. No acute cardiopulmonary abnormality.|||N|||F|||20250115120000
OBX|2|TX|71046&GDT^Procedure^LN||CHEST, 2 VIEWS: PA and lateral views of the chest were obtained.|||N|||F|||20250115120000
OBX|3|TX|71046&FND^Findings^LN||LUNGS: Clear bilaterally. No focal consolidation, mass, or nodule. No pleural effusion or pneumothorax.\X0D\\X0A\HEART: Normal size and contour. Mediastinal silhouette is unremarkable.\X0D\\X0A\BONY STRUCTURES: No acute osseous abnormality.|||N|||F|||20250115120000
OBX|4|CE|71046&PROC^Procedure Code^LN||71046^XR Chest 2 Views^CPT|||N|||F|||20250115120000
NTE|1|P|Comparison: Chest X-ray dated 2024-06-15
```

### Preliminary Results (Pending)

```
MSH|^~\&|LAB|MAIN_LAB|EHR|SPRINGFIELD_HOSP|20250115180000||ORU^R01|MSG20250115005|P|2.5|||AL|NE|
PID|1||MRN00000004^^^SPRINGFIELD_HOSP^MR||WILSON^JAMES^ROBERT||19650710|M|||555 MAPLE DR^^SPRINGFIELD^IL^62704^USA||5552223333|
OBR|1|ORD001237^EHR|LAB001237^LAB|87040^Blood Culture^CPT||20250115120000|20250115121500|||||||Blood|||||||20250115180000|||P
OBX|1|TX|87040^Blood Culture^LN||Preliminary: No growth at 48 hours. Final results pending.|||N|||P|||20250115180000
NTE|1|L|Culture incubation continues. Final report in 72 hours if no growth.
```

### HbA1c with Interpretation

```
MSH|^~\&|LAB|MAIN_LAB|EHR|SPRINGFIELD_HOSP|20250115150000||ORU^R01|MSG20250115006|P|2.5|||AL|NE|
PID|1||MRN00000005^^^SPRINGFIELD_HOSP^MR||MARTINEZ^CARLOS^ANTONIO||19680220|M|||321 PINE ST^^SPRINGFIELD^IL^62705^USA||5553334444|
OBR|1|ORD001238^EHR|LAB001238^LAB|83036^Hemoglobin A1C^CPT||20250115140000|20250115141500|||||||Blood|||||||20250115150000|||F
OBX|1|NM|4548-4^Hemoglobin A1c^LN||8.5|%|<5.7|H|||F|||20250115141500
OBX|2|NM|4548-4^Hemoglobin A1c^LN|eAG|196|mg/dL||||F|||20250115141500
OBX|3|TX|4548-4&INT^Interpretation^LN||Elevated HbA1c consistent with poorly controlled diabetes mellitus. Target for most patients with diabetes is <7.0%. Recommend medication adjustment and lifestyle counseling.|||A|||F|||20250115141500
NTE|1|L|eAG (estimated Average Glucose) calculated from HbA1c using ADAG formula.
```

## Transformation from JSON

### Input (HealthSim Observation)
```json
{
  "observation": {
    "observation_id": "OBS001234",
    "order_id": "ORD001234",
    "status": "final",
    "effective_datetime": "2025-01-15T15:00:00",
    "results": [
      {
        "code": "2345-7",
        "name": "Glucose",
        "value": 98,
        "unit": "mg/dL",
        "reference_range": "70-100",
        "interpretation": "normal"
      }
    ]
  },
  "patient": {
    "mrn": "MRN00000001"
  }
}
```

### Output (HL7v2 ORU^R01)
```
MSH|^~\&|LAB|FACILITY|EHR|HOSPITAL|20250115160000||ORU^R01|MSG001|P|2.5|||AL|NE|
PID|1||MRN00000001^^^FACILITY^MR||||||||||||||||||
OBR|1||OBS001234^LAB|2345-7^Glucose^LN|||20250115150000||||||||||||||20250115160000|||F
OBX|1|NM|2345-7^Glucose^LN||98|mg/dL|70-100|N|||F|||20250115150000
```

## Common LOINC Codes

### Chemistry
| LOINC | Name | Units | Reference Range |
|-------|------|-------|-----------------|
| 2345-7 | Glucose | mg/dL | 70-100 |
| 3094-0 | BUN | mg/dL | 7-20 |
| 2160-0 | Creatinine | mg/dL | 0.7-1.3 |
| 2951-2 | Sodium | mmol/L | 136-145 |
| 2823-3 | Potassium | mmol/L | 3.5-5.0 |
| 4548-4 | HbA1c | % | <5.7 |

### Hematology
| LOINC | Name | Units | Reference Range |
|-------|------|-------|-----------------|
| 6690-2 | WBC | 10*3/uL | 4.5-11.0 |
| 718-7 | Hemoglobin | g/dL | 12.0-17.5 |
| 4544-3 | Hematocrit | % | 36-50 |
| 777-3 | Platelets | 10*3/uL | 150-400 |

## Validation Rules

1. **OBR required**: Every ORU must have OBR segment
2. **OBX-2 required**: Value type must be specified
3. **OBX-3 required**: Observation identifier required
4. **OBX-5/OBX-2 match**: Value must match declared type
5. **Critical values**: LL/HH flags require notification documentation
6. **Final status**: F status means results are verified

## Related Skills

- [hl7v2-adt.md](hl7v2-adt.md) - ADT messages
- [hl7v2-orm.md](hl7v2-orm.md) - Order messages
- [../references/hl7v2-segments.md](../references/hl7v2-segments.md) - Segment reference
- [../references/code-systems.md](../references/code-systems.md) - LOINC codes
- [../skills/patientsim/orders-results.md](../skills/patientsim/orders-results.md) - Orders/results scenario
