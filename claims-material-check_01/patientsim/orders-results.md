---
name: orders-results
description: "Clinical orders (lab, radiology, medication) and their corresponding results with realistic values. Triggers: lab orders, test results, observations, ORM, ORU, lab panels, CMP, CBC, radiology orders, medication orders, LOINC"
---

# Orders and Results Cohort

A cohort template for generating clinical orders (laboratory, radiology, medication) and their corresponding results with realistic values and interpretations.

## For Claude

Use this skill when the user requests clinical orders or diagnostic results. This teaches you how to generate **realistic ORM/ORU messages** with appropriate test panels, result values, and critical value handling.

**When to apply this skill:**

- User mentions lab orders, test results, or observations
- User requests ORM or ORU message generation
- User asks for specific lab panels (CMP, CBC, etc.)
- User needs radiology or medication order examples

**Key capabilities this skill provides:**

- How to structure order and result messages
- How to generate appropriate reference ranges and abnormal flags
- How to model critical value workflows
- How to create condition-specific order panels

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: orders, results, laboratory, radiology, orm, oru, hl7v2
- **Updated**: 2025-01-15

## Purpose

This cohort generates clinical orders and results for laboratory, radiology, and medication workflows. It supports the complete order lifecycle from placement through completion with realistic result values and interpretations.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "lab order", "test order", "lab result", "test result"
- "ORM", "ORU", "observation"
- "CMP", "CBC", "lipid panel", "BMP"
- "radiology order", "imaging result"

**Order Cohorts**:

- "Generate a CMP with abnormal results"
- "Create a critical potassium value"
- "Generate a chest x-ray order with report"

## Trigger Phrases

- order
- lab order
- test order
- radiology order
- medication order
- lab result
- test result
- observation
- ORM
- ORU
- diagnostic
- requisition

## Overview

This cohort generates clinical orders (laboratory, radiology, medication) and their corresponding results/observations. It supports the complete order lifecycle from placement through completion with realistic result values.

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| order_type | string | lab | lab, radiology, medication, procedure |
| panel | string | cmp | cmp, bmp, cbc, lipid, thyroid, ua, custom |
| priority | string | routine | stat, asap, routine, preop, timed |
| status | string | completed | new, accepted, scheduled, in_progress, completed, cancelled |
| result_type | string | normal | normal, abnormal, critical, mixed |
| output_format | string | json | json, hl7v2_orm, hl7v2_oru, fhir |
| geography | string | null | County/tract FIPS for population-based abnormality rates |

## Data Sources (PopulationSim v2.0)

When geography is specified, result distributions reflect local population health patterns:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Key columns for lab patterns:
  - DIABETES_CrudePrev: Affects glucose, HbA1c distributions
  - KIDNEY_CrudePrev: Affects BUN, creatinine, eGFR
  - HIGHCHOL_CrudePrev: Affects lipid panel distributions
  - BPHIGH_CrudePrev: Cardiovascular panel context
```

### Data-Driven Result Distributions

| Condition | Affected Labs | Data-Driven Adjustment |
|-----------|---------------|------------------------|
| High diabetes area | Glucose, HbA1c | More elevated values in "random" panels |
| High CKD area | BUN, Creatinine | More abnormal renal function |
| High cholesterol area | LDL, Total Cholesterol | Higher baseline lipids |

### Example: Hidalgo County, TX (FIPS 48215)
```
From places_county_2024.csv:
  DIABETES_CrudePrev: 18.2% (very high)
  KIDNEY_CrudePrev: 4.1%
  HIGHCHOL_CrudePrev: 30.5%

Apply to generation:
  - Random CMP: 18% chance of elevated glucose (vs 10% generic)
  - HbA1c orders: Higher proportion >6.5%
  - Lipid panels: Shift distribution toward elevated LDL
```

## Order Types

### Laboratory Orders

| Panel | CPT | Tests Included | Typical TAT |
|-------|-----|----------------|-------------|
| BMP | 80048 | Glucose, BUN, Creatinine, Na, K, Cl, CO2, Ca | 1-2 hours |
| CMP | 80053 | BMP + Protein, Albumin, Bilirubin, ALP, ALT, AST | 2-4 hours |
| CBC | 85025 | WBC, RBC, Hgb, Hct, MCV, MCH, MCHC, RDW, Plt | 1 hour |
| CBC w/Diff | 85025 | CBC + Neutrophils, Lymphocytes, Monocytes, Eos, Baso | 1 hour |
| Lipid Panel | 80061 | Total Chol, HDL, LDL, Triglycerides | 2-4 hours |
| Thyroid Panel | 84443 | TSH, Free T4, Free T3 | 4-24 hours |
| HbA1c | 83036 | Hemoglobin A1c | 2-4 hours |
| UA | 81001 | Color, Clarity, pH, Specific Gravity, Protein, Glucose, Ketones, Blood | 1-2 hours |
| PT/INR | 85610 | Prothrombin Time, INR | 1 hour |
| BNP | 83880 | B-type Natriuretic Peptide | 1-2 hours |
| Troponin | 84484 | Troponin I or T | 1 hour |

### Radiology Orders

| Study | CPT | Modality | Typical TAT |
|-------|-----|----------|-------------|
| Chest X-ray 2v | 71046 | XR | 1-2 hours |
| Chest X-ray PA | 71045 | XR | 1-2 hours |
| CT Head w/o | 70450 | CT | 2-4 hours |
| CT Chest w/ | 71260 | CT | 2-4 hours |
| CT Abd/Pelvis w/ | 74177 | CT | 2-4 hours |
| MRI Brain w/ | 70553 | MR | 24-48 hours |
| MRI Lumbar w/o | 72148 | MR | 24-48 hours |
| US Abdomen | 76700 | US | 2-4 hours |
| Echo TTE | 93306 | US | 24-48 hours |
| Nuclear Stress | 78452 | NM | 24-48 hours |

### Medication Orders

| Category | Examples | Route |
|----------|----------|-------|
| Antibiotics | Ceftriaxone, Vancomycin, Azithromycin | IV, PO |
| Anticoagulants | Heparin, Enoxaparin, Warfarin | IV, SubQ, PO |
| Cardiac | Metoprolol, Lisinopril, Furosemide | IV, PO |
| Diabetes | Insulin, Metformin | SubQ, PO |
| Pain | Acetaminophen, Morphine, Hydrocodone | IV, PO |
| GI | Omeprazole, Ondansetron | IV, PO |

## Result Reference Ranges

### Chemistry (Adult)

| Test | LOINC | Low | High | Critical Low | Critical High | Unit |
|------|-------|-----|------|--------------|---------------|------|
| Glucose | 2345-7 | 70 | 100 | 40 | 500 | mg/dL |
| BUN | 3094-0 | 7 | 20 | 2 | 100 | mg/dL |
| Creatinine | 2160-0 | 0.7 | 1.3 | 0.3 | 10.0 | mg/dL |
| Sodium | 2951-2 | 136 | 145 | 120 | 160 | mmol/L |
| Potassium | 2823-3 | 3.5 | 5.0 | 2.5 | 6.5 | mmol/L |
| Chloride | 2075-0 | 98 | 106 | 80 | 120 | mmol/L |
| CO2 | 1963-8 | 22 | 29 | 10 | 40 | mmol/L |
| Calcium | 17861-6 | 8.6 | 10.2 | 6.0 | 14.0 | mg/dL |
| Protein | 2885-2 | 6.0 | 8.3 | | | g/dL |
| Albumin | 1751-7 | 3.5 | 5.0 | | | g/dL |
| Bilirubin | 1975-2 | 0.1 | 1.2 | | 15.0 | mg/dL |
| Alk Phos | 6768-6 | 44 | 147 | | | U/L |
| ALT | 1742-6 | 7 | 56 | | 1000 | U/L |
| AST | 1920-8 | 10 | 40 | | 1000 | U/L |

### Hematology

| Test | LOINC | Low | High | Critical Low | Critical High | Unit |
|------|-------|-----|------|--------------|---------------|------|
| WBC | 6690-2 | 4.5 | 11.0 | 1.0 | 30.0 | 10*3/uL |
| RBC | 789-8 | 4.0 | 5.5 | 2.0 | 7.0 | 10*6/uL |
| Hemoglobin | 718-7 | 12.0 | 17.5 | 7.0 | 20.0 | g/dL |
| Hematocrit | 4544-3 | 36 | 50 | 20 | 60 | % |
| Platelets | 777-3 | 150 | 400 | 50 | 1000 | 10*3/uL |

### Cardiac

| Test | LOINC | Normal | Abnormal | Critical | Unit |
|------|-------|--------|----------|----------|------|
| Troponin I | 10839-9 | <0.04 | 0.04-0.40 | >0.40 | ng/mL |
| BNP | 30934-4 | <100 | 100-400 | >400 | pg/mL |
| NT-proBNP | 33762-6 | <300 | 300-900 | >900 | pg/mL |

## Examples

### Example 1: CMP Order with Normal Results

```json
{
  "order": {
    "order_id": "ORD20250115001",
    "patient_mrn": "MRN00000001",
    "encounter_id": "ENC0000000001",
    "order_type": "LAB",
    "code": "80053",
    "code_system": "CPT",
    "description": "Comprehensive Metabolic Panel",
    "priority": "routine",
    "status": "completed",
    "ordered_datetime": "2025-01-15T14:30:22",
    "collected_datetime": "2025-01-15T15:00:00",
    "resulted_datetime": "2025-01-15T16:00:00",
    "ordering_provider": {
      "npi": "1234567890",
      "name": { "given_name": "Robert", "family_name": "Johnson" }
    },
    "performing_lab": {
      "id": "LAB001",
      "name": "Main Hospital Laboratory"
    }
  },
  "results": [
    { "code": "2345-7", "name": "Glucose", "value": 95, "unit": "mg/dL", "range": "70-100", "flag": "N" },
    { "code": "3094-0", "name": "BUN", "value": 15, "unit": "mg/dL", "range": "7-20", "flag": "N" },
    { "code": "2160-0", "name": "Creatinine", "value": 1.0, "unit": "mg/dL", "range": "0.7-1.3", "flag": "N" },
    { "code": "2951-2", "name": "Sodium", "value": 140, "unit": "mmol/L", "range": "136-145", "flag": "N" },
    { "code": "2823-3", "name": "Potassium", "value": 4.2, "unit": "mmol/L", "range": "3.5-5.0", "flag": "N" },
    { "code": "2075-0", "name": "Chloride", "value": 102, "unit": "mmol/L", "range": "98-106", "flag": "N" },
    { "code": "1963-8", "name": "CO2", "value": 25, "unit": "mmol/L", "range": "22-29", "flag": "N" },
    { "code": "17861-6", "name": "Calcium", "value": 9.5, "unit": "mg/dL", "range": "8.6-10.2", "flag": "N" },
    { "code": "2885-2", "name": "Total Protein", "value": 7.2, "unit": "g/dL", "range": "6.0-8.3", "flag": "N" },
    { "code": "1751-7", "name": "Albumin", "value": 4.2, "unit": "g/dL", "range": "3.5-5.0", "flag": "N" },
    { "code": "1975-2", "name": "Bilirubin Total", "value": 0.8, "unit": "mg/dL", "range": "0.1-1.2", "flag": "N" },
    { "code": "6768-6", "name": "Alkaline Phosphatase", "value": 72, "unit": "U/L", "range": "44-147", "flag": "N" },
    { "code": "1742-6", "name": "ALT", "value": 28, "unit": "U/L", "range": "7-56", "flag": "N" },
    { "code": "1920-8", "name": "AST", "value": 24, "unit": "U/L", "range": "10-40", "flag": "N" },
    { "code": "33914-3", "name": "eGFR", "value": 82, "unit": "mL/min/1.73m2", "range": ">60", "flag": "N" }
  ],
  "interpretation": "All results within normal limits."
}
```

### Example 2: CBC with Abnormal Results

```json
{
  "order": {
    "order_id": "ORD20250115002",
    "patient_mrn": "MRN00000002",
    "order_type": "LAB",
    "code": "85025",
    "description": "CBC with Differential",
    "priority": "stat",
    "status": "completed"
  },
  "results": [
    { "code": "6690-2", "name": "WBC", "value": 15.5, "unit": "10*3/uL", "range": "4.5-11.0", "flag": "H" },
    { "code": "789-8", "name": "RBC", "value": 3.8, "unit": "10*6/uL", "range": "4.0-5.5", "flag": "L" },
    { "code": "718-7", "name": "Hemoglobin", "value": 10.5, "unit": "g/dL", "range": "12.0-17.5", "flag": "L" },
    { "code": "4544-3", "name": "Hematocrit", "value": 32, "unit": "%", "range": "36-50", "flag": "L" },
    { "code": "787-2", "name": "MCV", "value": 76, "unit": "fL", "range": "80-100", "flag": "L" },
    { "code": "777-3", "name": "Platelets", "value": 180, "unit": "10*3/uL", "range": "150-400", "flag": "N" },
    { "code": "770-8", "name": "Neutrophils", "value": 78, "unit": "%", "range": "40-70", "flag": "H" },
    { "code": "736-9", "name": "Lymphocytes", "value": 15, "unit": "%", "range": "20-40", "flag": "L" }
  ],
  "interpretation": "Microcytic anemia with leukocytosis. Consider iron deficiency with possible infection or inflammation. Recommend iron studies and inflammatory markers."
}
```

### Example 3: Critical Lab Result

```json
{
  "order": {
    "order_id": "ORD20250115003",
    "patient_mrn": "MRN00000003",
    "order_type": "LAB",
    "code": "2823-3",
    "description": "Potassium",
    "priority": "stat",
    "status": "completed"
  },
  "results": [
    { "code": "2823-3", "name": "Potassium", "value": 6.8, "unit": "mmol/L", "range": "3.5-5.0", "flag": "HH" }
  ],
  "critical_value": {
    "acknowledged": true,
    "acknowledged_by": "Dr. Lisa Chen",
    "acknowledged_datetime": "2025-01-15T20:15:00",
    "read_back_confirmed": true
  },
  "interpretation": "CRITICAL VALUE: Severe hyperkalemia. Risk of cardiac arrhythmia. Immediate treatment recommended."
}
```

### Example 4: Radiology Order with Report

```json
{
  "order": {
    "order_id": "ORD20250115004",
    "patient_mrn": "MRN00000004",
    "order_type": "RAD",
    "code": "71046",
    "code_system": "CPT",
    "description": "Chest X-ray 2 Views",
    "priority": "routine",
    "status": "completed",
    "clinical_indication": "Shortness of breath, rule out pneumonia",
    "diagnosis_codes": ["R06.00"]
  },
  "report": {
    "accession_number": "RAD20250115001",
    "exam_datetime": "2025-01-15T11:00:00",
    "reported_datetime": "2025-01-15T12:00:00",
    "radiologist": {
      "npi": "4567890123",
      "name": { "given_name": "Sarah", "family_name": "Williams" }
    },
    "procedure": "CHEST, 2 VIEWS: PA and lateral views of the chest were obtained.",
    "comparison": "Chest X-ray dated 2024-06-15",
    "findings": {
      "lungs": "Clear bilaterally. No focal consolidation, mass, or nodule. No pleural effusion or pneumothorax.",
      "heart": "Normal size and contour. Mediastinal silhouette is unremarkable.",
      "bones": "No acute osseous abnormality."
    },
    "impression": "No acute cardiopulmonary abnormality.",
    "recommendations": null
  }
}
```

### Example 5: Medication Order

```json
{
  "order": {
    "order_id": "ORD20250115005",
    "patient_mrn": "MRN00000005",
    "encounter_id": "ENC0000000005",
    "order_type": "MEDICATION",
    "priority": "routine",
    "status": "active",
    "ordered_datetime": "2025-01-15T09:00:00"
  },
  "medication": {
    "ndc": "00093505601",
    "rxnorm": "314076",
    "drug_name": "Lisinopril 10mg Tab",
    "dose": {
      "value": 10,
      "unit": "mg"
    },
    "route": "oral",
    "frequency": "once daily",
    "timing": "morning",
    "duration": {
      "value": 30,
      "unit": "days"
    },
    "refills": 5,
    "indication": "Hypertension",
    "indication_code": "I10",
    "instructions": "Take one tablet by mouth every morning",
    "dispense_quantity": 30,
    "substitution_allowed": true
  },
  "prescriber": {
    "npi": "1234567890",
    "name": { "given_name": "Robert", "family_name": "Johnson" },
    "dea": "AJ1234567"
  }
}
```

### Example 6: Complete Order Flow (HL7v2)

**Request:** "Generate a lab order with results as HL7v2 ORM and ORU"

**ORM^O01 Output:**
```
MSH|^~\&|EHR|SPRINGFIELD|LAB|MAINLAB|20250115143022||ORM^O01|MSG001|P|2.5|||AL|NE|
PID|1||MRN00000001^^^SPRINGFIELD^MR||SMITH^JOHN^MICHAEL||19700315|M
PV1|1|I|MED^201^A|||||||||||||||ENC0000000001
ORC|NW|ORD20250115001^EHR|||SC||^^^^^R||20250115143022|||1234567890^Johnson^Robert^MD
OBR|1|ORD20250115001^EHR||80053^Comprehensive Metabolic Panel^CPT|R|20250115143022|||||1234567890^Johnson^Robert^MD|||Blood
```

**ORU^R01 Output:**
```
MSH|^~\&|LAB|MAINLAB|EHR|SPRINGFIELD|20250115160000||ORU^R01|MSG002|P|2.5|||AL|NE|
PID|1||MRN00000001^^^SPRINGFIELD^MR||SMITH^JOHN^MICHAEL||19700315|M
OBR|1|ORD20250115001^EHR|LAB001^LAB|80053^Comprehensive Metabolic Panel^CPT||20250115143022|20250115150000|||||1234567890^Johnson^Robert^MD|||Blood|||9876543210^Jones^Mary^MT||||||20250115160000|||F
OBX|1|NM|2345-7^Glucose^LN||95|mg/dL|70-100|N|||F|||20250115150000
OBX|2|NM|3094-0^BUN^LN||15|mg/dL|7-20|N|||F|||20250115150000
OBX|3|NM|2160-0^Creatinine^LN||1.0|mg/dL|0.7-1.3|N|||F|||20250115150000
OBX|4|NM|2951-2^Sodium^LN||140|mmol/L|136-145|N|||F|||20250115150000
OBX|5|NM|2823-3^Potassium^LN||4.2|mmol/L|3.5-5.0|N|||F|||20250115150000
```

## Condition-Specific Panels

### Diabetes Monitoring

```json
{
  "condition": "diabetes",
  "recommended_orders": [
    { "code": "83036", "name": "HbA1c", "frequency": "every 3 months" },
    { "code": "80053", "name": "CMP", "frequency": "every 6 months" },
    { "code": "80061", "name": "Lipid Panel", "frequency": "annually" },
    { "code": "81001", "name": "Urinalysis", "frequency": "annually" },
    { "code": "36483-7", "name": "Urine Microalbumin/Creatinine", "frequency": "annually" }
  ]
}
```

### Heart Failure Monitoring

```json
{
  "condition": "heart_failure",
  "recommended_orders": [
    { "code": "80053", "name": "CMP", "frequency": "every 3 months" },
    { "code": "83880", "name": "BNP", "frequency": "as needed" },
    { "code": "93306", "name": "Echocardiogram", "frequency": "annually" },
    { "code": "71046", "name": "Chest X-ray", "frequency": "as needed" }
  ]
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Order code | Valid CPT/LOINC | 80053 (CMP), 2345-7 (glucose) |
| Result value | Within physiologic range | 95 mg/dL |
| Reference range | Low-high format | 70-100 mg/dL |
| Result status | final, preliminary, corrected | "final" |
| Order status | ordered, completed, cancelled | "completed" |
| Collection time | Valid datetime | 2025-01-15T08:30:00 |
| Result time | After collection time | 2025-01-15T10:15:00 |
| Abnormal flag | L, H, LL, HH, N | "H" (high) |

### Business Rules

- **Order-Result Pairing**: Each result must link to a valid order
- **Turnaround Time**: Labs typically 1-24 hours; imaging read within hours
- **Critical Values**: Immediate notification required (e.g., K+ >6.5)
- **Reference Ranges**: Age/sex-specific where applicable
- **Result Interpretation**: Abnormal flags based on reference range comparison
- **Panel Components**: CMP has 14 tests; CBC has 8+ parameters
- **Repeat Testing**: Abnormal results may prompt repeat confirmation
- **Result Amendment**: Corrected results must maintain original and correction

## Related Skills

- [SKILL.md](SKILL.md) - PatientSim overview
- [diabetes-management.md](diabetes-management.md) - Diabetes cohort
- [heart-failure.md](heart-failure.md) - Heart failure cohort
- [../../formats/hl7v2-orm.md](../../formats/hl7v2-orm.md) - Order message format
- [../../formats/hl7v2-oru.md](../../formats/hl7v2-oru.md) - Result message format
- [../../references/code-systems.md](../../references/code-systems.md) - LOINC, CPT codes
