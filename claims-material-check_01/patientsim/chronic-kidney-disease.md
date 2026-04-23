---
name: chronic-kidney-disease
description: "Chronic kidney disease patients across all stages including dialysis and transplant evaluation. Triggers: CKD, kidney disease, renal failure, eGFR, creatinine, dialysis, nephrology, ESRD, transplant"
---

# Chronic Kidney Disease Cohort

A cohort template for generating patients with chronic kidney disease across all stages, including dialysis and transplant evaluation.

## For Claude

Use this skill when the user requests CKD patient data or nephrology cohorts. This teaches you how to generate **realistic CKD patients** with stage-appropriate lab values, medications, and encounter patterns.

**When to apply this skill:**

- User mentions CKD, kidney disease, or renal failure
- User requests eGFR or creatinine-based cohorts
- User asks for dialysis patient data
- User needs nephrology encounter examples

**Key capabilities this skill provides:**

- How to stage CKD properly (1-5, 5D) based on eGFR and albuminuria
- How to generate stage-appropriate lab abnormalities
- How to model CKD medication regimens (phosphate binders, ESAs, etc.)
- How to create nephrology follow-up patterns

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: ckd, nephrology, dialysis, renal, chronic-disease
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic chronic kidney disease patients across all stages. It models the complete CKD spectrum from early-stage with proteinuria through end-stage renal disease on dialysis, with appropriate lab patterns, medications, and comorbidities.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "CKD", "chronic kidney disease", "renal failure"
- "eGFR", "creatinine", "BUN"
- "dialysis", "hemodialysis", "peritoneal dialysis"
- "nephrology", "nephrologist"

**Clinical Cohorts**:

- "Generate a stage 4 CKD patient"
- "Create a diabetic nephropathy case"
- "Generate a patient preparing for dialysis"

## Trigger Phrases

- CKD
- chronic kidney disease
- kidney disease
- renal failure
- eGFR
- creatinine elevated
- dialysis
- nephropathy
- nephrologist
- kidney function

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| age_range | range | 50-80 | Any valid adult range |
| ckd_stage | int | 3 | 1, 2, 3a, 3b, 4, 5 |
| etiology | string | diabetic | diabetic, hypertensive, glomerular, polycystic, unknown |
| dialysis_status | string | none | none, hemodialysis, peritoneal |
| progression | string | stable | stable, progressing, acute_on_chronic |
| geography | string | null | County/tract FIPS for data-driven rates |

## Data Sources (PopulationSim v2.0)

When geography is specified, CKD cohorts use real CDC PLACES data:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
CKD-related columns:
  - KIDNEY_CrudePrev: Chronic kidney disease prevalence (%)
  - DIABETES_CrudePrev: Diabetes (primary CKD cause)
  - BPHIGH_CrudePrev: Hypertension (primary CKD cause)
```

### Data-Driven Etiology Weighting

CDC PLACES provides underlying condition rates that inform CKD etiology distribution:

| Etiology | Default Weight | Data-Driven Adjustment |
|----------|---------------|------------------------|
| Diabetic nephropathy | 45% | Higher if DIABETES > national avg (10.1%) |
| Hypertensive | 30% | Higher if BPHIGH > national avg (32.4%) |
| Glomerular | 10% | Static |
| Other | 15% | Static |

**Example: Hidalgo County, TX (FIPS 48215)**
```
From places_county_2024.csv:
  KIDNEY_CrudePrev: 3.8%
  DIABETES_CrudePrev: 16.2%  (60% above national)
  BPHIGH_CrudePrev: 31.8%
  
Adjusted etiology weights:
  - Diabetic: 55% (increased due to high diabetes)
  - Hypertensive: 25%
  - Other: 20%
```

### SDOH Context for CKD

Higher SVI areas have:
- Later stage at diagnosis (worse access to screening)
- Lower rates of nephrology referral
- Higher ESKD initiation rates
- More emergent dialysis starts

## CKD Staging

### Stage Classification by eGFR

| Stage | eGFR (mL/min/1.73m2) | ICD-10 | Description |
|-------|----------------------|--------|-------------|
| 1 | >= 90 | N18.1 | Normal or high GFR with kidney damage |
| 2 | 60-89 | N18.2 | Mildly decreased GFR with kidney damage |
| 3a | 45-59 | N18.3 | Mildly to moderately decreased |
| 3b | 30-44 | N18.3 | Moderately to severely decreased |
| 4 | 15-29 | N18.4 | Severely decreased |
| 5 | < 15 | N18.5 | Kidney failure (ESKD) |
| 5D | < 15 + dialysis | N18.6 | ESKD on dialysis |

### Albuminuria Categories

| Category | UACR (mg/g) | Description |
|----------|-------------|-------------|
| A1 | < 30 | Normal to mildly increased |
| A2 | 30-300 | Moderately increased (microalbuminuria) |
| A3 | > 300 | Severely increased (macroalbuminuria) |

## Diagnosis Codes

### Primary CKD Codes
| Code | Description |
|------|-------------|
| N18.1 | CKD, stage 1 |
| N18.2 | CKD, stage 2 |
| N18.3 | CKD, stage 3 |
| N18.4 | CKD, stage 4 |
| N18.5 | CKD, stage 5 |
| N18.6 | End stage renal disease |
| N18.9 | CKD, unspecified |

### Etiology Codes
| Code | Description | Use With |
|------|-------------|----------|
| E11.22 | Type 2 DM with diabetic CKD | Diabetic nephropathy |
| I12.9 | Hypertensive CKD | Hypertensive nephropathy |
| N03.9 | Chronic nephritic syndrome | Glomerulonephritis |
| Q61.3 | Polycystic kidney, autosomal dominant | PKD |

### Common Comorbidities
| Probability | Code | Description |
|-------------|------|-------------|
| 85% | I10/I12.9 | Hypertension |
| 65% | E11.22 | Type 2 diabetes with CKD |
| 50% | D63.1 | Anemia of CKD |
| 45% | E21.1 | Secondary hyperparathyroidism |
| 40% | I50.9 | Heart failure |
| 35% | E83.51 | Hypocalcemia |
| 30% | E87.5 | Hyperkalemia |
| 25% | I25.10 | Coronary artery disease |

## Lab Patterns by Stage

### CKD Stage 3 (eGFR 30-59)
```json
{
  "creatinine": { "min": 1.5, "max": 2.5, "unit": "mg/dL", "flag": "H" },
  "egfr": { "min": 30, "max": 59, "unit": "mL/min/1.73m2", "flag": "L" },
  "bun": { "min": 25, "max": 45, "unit": "mg/dL", "flag": "H" },
  "potassium": { "min": 4.5, "max": 5.5, "unit": "mmol/L", "flag": null },
  "phosphorus": { "min": 4.0, "max": 5.5, "unit": "mg/dL", "flag": "H" },
  "calcium": { "min": 8.5, "max": 9.5, "unit": "mg/dL", "flag": null },
  "hemoglobin": { "min": 10.5, "max": 12.5, "unit": "g/dL", "flag": "L" },
  "pth": { "min": 70, "max": 150, "unit": "pg/mL", "flag": "H" },
  "urine_microalbumin": { "min": 30, "max": 300, "unit": "mg/g", "flag": "H" }
}
```

### CKD Stage 4 (eGFR 15-29)
```json
{
  "creatinine": { "min": 2.5, "max": 5.0, "unit": "mg/dL", "flag": "H" },
  "egfr": { "min": 15, "max": 29, "unit": "mL/min/1.73m2", "flag": "L" },
  "bun": { "min": 45, "max": 80, "unit": "mg/dL", "flag": "H" },
  "potassium": { "min": 5.0, "max": 6.0, "unit": "mmol/L", "flag": "H" },
  "phosphorus": { "min": 5.0, "max": 7.0, "unit": "mg/dL", "flag": "H" },
  "calcium": { "min": 8.0, "max": 9.0, "unit": "mg/dL", "flag": "L" },
  "hemoglobin": { "min": 9.0, "max": 11.0, "unit": "g/dL", "flag": "L" },
  "pth": { "min": 150, "max": 400, "unit": "pg/mL", "flag": "H" },
  "bicarbonate": { "min": 18, "max": 22, "unit": "mmol/L", "flag": "L" }
}
```

### CKD Stage 5/ESKD (eGFR < 15)
```json
{
  "creatinine": { "min": 5.0, "max": 12.0, "unit": "mg/dL", "flag": "HH" },
  "egfr": { "min": 5, "max": 15, "unit": "mL/min/1.73m2", "flag": "L" },
  "bun": { "min": 80, "max": 150, "unit": "mg/dL", "flag": "HH" },
  "potassium": { "min": 5.5, "max": 6.5, "unit": "mmol/L", "flag": "HH" },
  "phosphorus": { "min": 6.0, "max": 10.0, "unit": "mg/dL", "flag": "HH" },
  "calcium": { "min": 7.5, "max": 8.5, "unit": "mg/dL", "flag": "L" },
  "hemoglobin": { "min": 7.5, "max": 10.0, "unit": "g/dL", "flag": "L" },
  "pth": { "min": 400, "max": 1500, "unit": "pg/mL", "flag": "HH" },
  "bicarbonate": { "min": 15, "max": 20, "unit": "mmol/L", "flag": "L" }
}
```

## Medication Patterns

### Blood Pressure Control
```json
{
  "first_line": {
    "name": "Lisinopril",
    "code": "104376",
    "dose": "20 mg",
    "route": "PO",
    "frequency": "QD",
    "note": "ACEi/ARB for proteinuria reduction"
  },
  "second_line": {
    "name": "Amlodipine",
    "code": "17767",
    "dose": "10 mg",
    "route": "PO",
    "frequency": "QD"
  }
}
```

### Anemia Management
```json
{
  "epo_stimulating_agent": {
    "name": "Epoetin alfa",
    "code": "9374",
    "dose": "10000 units",
    "route": "SubQ",
    "frequency": "Weekly",
    "indication": "D63.1"
  },
  "iron_supplementation": {
    "name": "Ferrous sulfate",
    "code": "4167",
    "dose": "325 mg",
    "route": "PO",
    "frequency": "TID"
  }
}
```

### Mineral Bone Disease
```json
{
  "phosphate_binder": {
    "name": "Sevelamer",
    "code": "273279",
    "dose": "800 mg",
    "route": "PO",
    "frequency": "TID with meals"
  },
  "vitamin_d": {
    "name": "Calcitriol",
    "code": "1534",
    "dose": "0.25 mcg",
    "route": "PO",
    "frequency": "QD"
  }
}
```

### Potassium Management
```json
{
  "potassium_binder": {
    "name": "Patiromer",
    "code": "1876449",
    "dose": "8.4 g",
    "route": "PO",
    "frequency": "QD",
    "indication": "E87.5"
  }
}
```

## Encounter Patterns

### Nephrology Follow-Up
- **Frequency by Stage**:
  - Stage 3a: Every 6 months
  - Stage 3b: Every 3-4 months
  - Stage 4: Every 2-3 months
  - Stage 5: Monthly
- **CPT Code**: 99214 or 99215
- **Labs**: CMP, CBC, PTH, phosphorus (at each visit)

### Dialysis Access Evaluation (Stage 4-5)
- **Timing**: When eGFR < 20
- **Referral**: Vascular surgery for AV fistula
- **CPT**: 99214 + referral

### Dialysis Session (Stage 5D)
- **Frequency**: 3x weekly (hemodialysis)
- **CPT**: 90935 (hemodialysis procedure)
- **Duration**: 3-4 hours per session

## Example Output

### CKD Stage 4 with Diabetic Nephropathy

```json
{
  "patient": {
    "mrn": "MRN00000003",
    "name": { "given_name": "James", "family_name": "Thompson" },
    "birth_date": "1955-07-22",
    "gender": "M"
  },
  "diagnoses": [
    { "code": "N18.4", "description": "Chronic kidney disease, stage 4", "diagnosed_date": "2024-03-15" },
    { "code": "E11.22", "description": "Type 2 DM with diabetic chronic kidney disease", "diagnosed_date": "2015-06-10" },
    { "code": "I12.9", "description": "Hypertensive chronic kidney disease", "diagnosed_date": "2018-09-20" },
    { "code": "D63.1", "description": "Anemia in chronic kidney disease", "diagnosed_date": "2023-11-08" },
    { "code": "E21.1", "description": "Secondary hyperparathyroidism", "diagnosed_date": "2024-01-15" },
    { "code": "E78.5", "description": "Hyperlipidemia", "diagnosed_date": "2012-04-22" }
  ],
  "medications": [
    { "name": "Lisinopril", "dose": "10 mg", "frequency": "QD", "status": "active" },
    { "name": "Amlodipine", "dose": "10 mg", "frequency": "QD", "status": "active" },
    { "name": "Insulin Glargine", "dose": "25 units", "frequency": "QHS", "status": "active" },
    { "name": "Epoetin alfa", "dose": "10000 units", "frequency": "Weekly", "route": "SubQ", "status": "active" },
    { "name": "Sevelamer", "dose": "800 mg", "frequency": "TID", "status": "active" },
    { "name": "Calcitriol", "dose": "0.25 mcg", "frequency": "QD", "status": "active" },
    { "name": "Sodium bicarbonate", "dose": "650 mg", "frequency": "TID", "status": "active" }
  ],
  "labs": [
    { "test_name": "Creatinine", "loinc_code": "2160-0", "value": "3.8", "unit": "mg/dL", "flag": "H" },
    { "test_name": "eGFR", "loinc_code": "48642-3", "value": "18", "unit": "mL/min/1.73m2", "flag": "L" },
    { "test_name": "BUN", "loinc_code": "3094-0", "value": "62", "unit": "mg/dL", "flag": "H" },
    { "test_name": "Potassium", "loinc_code": "2823-3", "value": "5.4", "unit": "mmol/L", "flag": "H" },
    { "test_name": "Phosphorus", "loinc_code": "2777-1", "value": "5.8", "unit": "mg/dL", "flag": "H" },
    { "test_name": "Calcium", "loinc_code": "17861-6", "value": "8.4", "unit": "mg/dL", "flag": "L" },
    { "test_name": "Hemoglobin", "loinc_code": "718-7", "value": "9.8", "unit": "g/dL", "flag": "L" },
    { "test_name": "PTH", "loinc_code": "2731-8", "value": "285", "unit": "pg/mL", "flag": "H" },
    { "test_name": "Bicarbonate", "loinc_code": "1963-8", "value": "19", "unit": "mmol/L", "flag": "L" },
    { "test_name": "HbA1c", "loinc_code": "4548-4", "value": "7.2", "unit": "%", "flag": "H" }
  ],
  "encounter": {
    "class_code": "O",
    "chief_complaint": "CKD follow-up, AV fistula planning discussion",
    "admission_time": "2025-01-15T10:30:00"
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| eGFR | 0-120 mL/min/1.73m² | 25 (Stage 4) |
| CKD stage | 1-5 based on eGFR | Stage 4 (eGFR 15-29) |
| Creatinine | Positive, inversely correlates with eGFR | 3.2 mg/dL |
| BUN | Positive, elevated in CKD | 45 mg/dL |
| Potassium | 3.5-6.5 mEq/L (may be elevated) | 5.8 mEq/L |
| Hemoglobin | Anemia common in CKD | 10.2 g/dL |
| Phosphorus | May be elevated | 5.5 mg/dL |
| PTH | Elevated in CKD | 180 pg/mL |

### Business Rules

- **CKD Staging**: Stage 1 (eGFR ≥90), Stage 2 (60-89), Stage 3a (45-59), Stage 3b (30-44), Stage 4 (15-29), Stage 5 (<15)
- **Anemia Management**: ESAs when Hgb <10; target 10-11.5 g/dL
- **Mineral Bone Disease**: Phosphate binders, vitamin D analogs, calcimimetics
- **Medication Adjustment**: Many drugs require dose adjustment or avoidance in CKD
- **ACEi/ARB**: Renoprotective but monitor creatinine/potassium closely
- **Dialysis Initiation**: Usually when eGFR <10-15 or symptomatic uremia
- **Transplant Evaluation**: Begin when eGFR <20
- **Comorbidities**: HTN, diabetes, and CVD very common

## Related Skills

### PatientSim Cohorts

- [SKILL.md](SKILL.md) - PatientSim overview
- [diabetes-management.md](diabetes-management.md) - Diabetic nephropathy
- [heart-failure.md](heart-failure.md) - Cardiorenal syndrome

### Cross-Product: MemberSim

- [../membersim/professional-claims.md](../membersim/professional-claims.md) - Nephrology office visit claims
- [../membersim/facility-claims.md](../membersim/facility-claims.md) - Dialysis facility claims, AV fistula procedures

> **Integration Pattern:** Use PatientSim for CKD staging and clinical progression. Use MemberSim for dialysis facility claims (revenue codes 082x) and nephrology E&M claims.

### Cross-Product: RxMemberSim

- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Renal medication fills (sevelamer, calcitriol, sodium bicarbonate)
- [../rxmembersim/specialty-pharmacy.md](../rxmembersim/specialty-pharmacy.md) - ESAs (epoetin alfa, darbepoetin), calcimimetics

> **Integration Pattern:** Use PatientSim for medication orders and lab monitoring. Use RxMemberSim for specialty pharmacy patterns - ESAs often require PA and have strict utilization management.

### References

- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10 codes
