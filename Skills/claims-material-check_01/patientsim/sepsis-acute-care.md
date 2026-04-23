---
name: sepsis-acute-care
description: "Sepsis patients across severity levels with SEP-1 bundle compliance and ICU care patterns. Triggers: sepsis, septic shock, SIRS, critical care, ICU, bacteremia, bloodstream infection, acute care, qSOFA"
---

# Sepsis and Acute Care Cohort

A cohort template for generating sepsis patients across severity levels with SEP-1 bundle compliance and ICU-level care patterns.

## For Claude

Use this skill when the user requests sepsis or critical care patient data. This teaches you how to generate **realistic sepsis presentations** with appropriate vital signs, lab patterns, and treatment bundles.

**When to apply this skill:**

- User mentions sepsis, septic shock, or SIRS
- User requests critical care or ICU cohorts
- User asks for bacteremia or bloodstream infection data
- User needs acute care encounter examples

**Key capabilities this skill provides:**

- How to classify sepsis severity (sepsis, severe sepsis, septic shock)
- How to generate SOFA score-appropriate organ dysfunction
- How to model SEP-1 bundle compliance (antibiotics, fluids, vasopressors)
- How to create ICU admission patterns

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: sepsis, critical-care, icu, acute-care, infection
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic sepsis patients across the severity spectrum. It implements Sepsis-3 definitions, SOFA scoring, and SEP-1 quality measure bundle compliance with appropriate vital signs, lab abnormalities, and treatment patterns.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "sepsis", "septic shock", "SIRS"
- "bacteremia", "bloodstream infection"
- "ICU admission", "critical care"
- "SEP-1", "sepsis bundle"

**Clinical Cohorts**:

- "Generate a septic shock patient from pneumonia"
- "Create a urosepsis case requiring ICU"
- "Generate sepsis with multi-organ dysfunction"

## Trigger Phrases

- sepsis
- septic
- systemic infection
- SIRS
- septic shock
- bacteremia
- blood stream infection
- ICU admission
- critical care
- acute infection

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| age_range | range | 45-85 | Any valid adult range |
| severity | string | sepsis | sepsis, severe_sepsis, septic_shock |
| source | string | pneumonia | pneumonia, urinary, abdominal, skin_soft_tissue, unknown |
| organism | string | unspecified | gram_positive, gram_negative, mixed, fungal, unspecified |
| icu_required | bool | false | Based on severity |
| geography | string | null | County/tract FIPS for data-driven rates |

## Data Sources (PopulationSim v2.0)

When geography is specified, sepsis cohorts use real population health data:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Relevant columns for sepsis/acute care:
  - ACCESS2_CrudePrev: Lack of insurance (delayed care → ED presentation)
  - KIDNEY_CrudePrev: CKD prevalence (sepsis risk factor)
  - DIABETES_CrudePrev: Diabetes (infection risk)
  - COPD_CrudePrev: COPD (respiratory infection source)
```

### Data-Driven Patterns

| Factor | PLACES Source | Impact on Sepsis |
|--------|---------------|------------------|
| ED Presentation | ACCESS2_CrudePrev | Higher uninsured → more ED sepsis |
| Comorbidities | DIABETES, KIDNEY, COPD | Higher rates → worse outcomes |
| Infection Source | COPD_CrudePrev | Higher COPD → more pneumonia source |

### SDOH Impact on Outcomes

```
File: skills/populationsim/data/county/svi_county_2022.csv
Impact on sepsis outcomes:
  - RPL_THEMES > 0.75: Delayed presentation, higher mortality
  - EP_UNINSUR > 20%: ED-dominant care pattern
  - EP_AGE65 high: More sepsis cases from nursing facilities
```

## Sepsis Definitions

### Sepsis-3 Criteria
- **Sepsis**: Suspected or confirmed infection PLUS SOFA score >= 2
- **Septic Shock**: Sepsis PLUS vasopressors required to maintain MAP >= 65 AND lactate > 2 mmol/L despite adequate fluid resuscitation

### qSOFA (Quick SOFA) - Screening
Score 1 point for each:
- Respiratory rate >= 22/min
- Altered mental status (GCS < 15)
- Systolic BP <= 100 mmHg

### SOFA Score Components
| System | Score 0 | Score 1 | Score 2 | Score 3 | Score 4 |
|--------|---------|---------|---------|---------|---------|
| Respiration (PaO2/FiO2) | >= 400 | < 400 | < 300 | < 200 + vent | < 100 + vent |
| Coagulation (Platelets) | >= 150 | < 150 | < 100 | < 50 | < 20 |
| Liver (Bilirubin) | < 1.2 | 1.2-1.9 | 2.0-5.9 | 6.0-11.9 | > 12.0 |
| Cardiovascular | MAP >= 70 | MAP < 70 | Dopa <= 5 | Dopa > 5 | Dopa > 15 |
| CNS (GCS) | 15 | 13-14 | 10-12 | 6-9 | < 6 |
| Renal (Creatinine) | < 1.2 | 1.2-1.9 | 2.0-3.4 | 3.5-4.9 | > 5.0 |

## Diagnosis Codes

### Primary Sepsis Codes
| Code | Description | Severity |
|------|-------------|----------|
| A41.9 | Sepsis, unspecified organism | Sepsis |
| A41.01 | Sepsis due to MSSA | Sepsis |
| A41.02 | Sepsis due to MRSA | Sepsis |
| A41.51 | Sepsis due to E. coli | Sepsis |
| A41.52 | Sepsis due to Pseudomonas | Sepsis |
| R65.20 | Severe sepsis without shock | Severe sepsis |
| R65.21 | Severe sepsis with septic shock | Septic shock |

### Source Codes
| Source | Code | Description |
|--------|------|-------------|
| Pneumonia | J18.9 | Pneumonia, unspecified organism |
| Urinary | N39.0 | Urinary tract infection, site not specified |
| Abdominal | K65.0 | Generalized acute peritonitis |
| Skin | L03.90 | Cellulitis, unspecified |
| Line infection | T80.211A | BSI due to central venous catheter |

### Organ Dysfunction Codes
| Code | Description |
|------|-------------|
| N17.9 | Acute kidney failure, unspecified |
| J96.01 | Acute respiratory failure with hypoxia |
| D65 | Disseminated intravascular coagulation |
| K72.01 | Acute hepatic failure |
| G93.1 | Encephalopathy |

## Vital Sign Patterns

### Sepsis (SIRS criteria met)
```json
{
  "temperature": { "min": 100.5, "max": 103.0, "unit": "F", "flag": "H" },
  "heart_rate": { "min": 95, "max": 125, "unit": "bpm", "flag": "H" },
  "respiratory_rate": { "min": 22, "max": 30, "unit": "/min", "flag": "H" },
  "systolic_bp": { "min": 90, "max": 110, "unit": "mmHg", "flag": "L" },
  "diastolic_bp": { "min": 55, "max": 70, "unit": "mmHg", "flag": "L" },
  "spo2": { "min": 90, "max": 95, "unit": "%", "flag": "L" }
}
```

### Septic Shock
```json
{
  "temperature": { "min": 95.0, "max": 103.5, "unit": "F", "flag": "A" },
  "heart_rate": { "min": 110, "max": 150, "unit": "bpm", "flag": "HH" },
  "respiratory_rate": { "min": 28, "max": 40, "unit": "/min", "flag": "HH" },
  "systolic_bp": { "min": 70, "max": 90, "unit": "mmHg", "flag": "L" },
  "diastolic_bp": { "min": 40, "max": 55, "unit": "mmHg", "flag": "L" },
  "spo2": { "min": 85, "max": 92, "unit": "%", "flag": "L" },
  "map": { "min": 50, "max": 65, "unit": "mmHg", "note": "Requires vasopressors" }
}
```

### Hypothermic Sepsis (elderly/immunocompromised)
```json
{
  "temperature": { "min": 95.0, "max": 97.5, "unit": "F", "flag": "L" },
  "heart_rate": { "min": 90, "max": 120, "unit": "bpm", "flag": "H" },
  "note": "Hypothermia indicates poor prognosis"
}
```

## Lab Patterns

### Early Sepsis
```json
{
  "wbc": { "min": 12.0, "max": 25.0, "unit": "x10^3/uL", "flag": "H" },
  "lactate": { "min": 2.0, "max": 4.0, "unit": "mmol/L", "flag": "H" },
  "creatinine": { "min": 1.2, "max": 2.0, "unit": "mg/dL", "flag": "H" },
  "procalcitonin": { "min": 2.0, "max": 10.0, "unit": "ng/mL", "flag": "H" },
  "crp": { "min": 50, "max": 150, "unit": "mg/L", "flag": "H" },
  "platelets": { "min": 100, "max": 150, "unit": "x10^3/uL", "flag": "L" },
  "glucose": { "min": 140, "max": 200, "unit": "mg/dL", "flag": "H" }
}
```

### Severe Sepsis/Septic Shock
```json
{
  "wbc": { "min": 2.0, "max": 30.0, "unit": "x10^3/uL", "flag": "A", "note": "May be low or high" },
  "lactate": { "min": 4.0, "max": 10.0, "unit": "mmol/L", "flag": "HH" },
  "creatinine": { "min": 2.5, "max": 5.0, "unit": "mg/dL", "flag": "HH" },
  "procalcitonin": { "min": 10.0, "max": 100.0, "unit": "ng/mL", "flag": "HH" },
  "platelets": { "min": 50, "max": 100, "unit": "x10^3/uL", "flag": "L" },
  "bilirubin": { "min": 2.0, "max": 6.0, "unit": "mg/dL", "flag": "H" },
  "inr": { "min": 1.5, "max": 3.0, "unit": "", "flag": "H" },
  "ph": { "min": 7.20, "max": 7.35, "unit": "", "flag": "L" },
  "bicarbonate": { "min": 15, "max": 20, "unit": "mmol/L", "flag": "L" }
}
```

### Leukopenic Sepsis (immunocompromised)
```json
{
  "wbc": { "min": 0.5, "max": 2.0, "unit": "x10^3/uL", "flag": "LL" },
  "anc": { "min": 0.1, "max": 0.5, "unit": "x10^3/uL", "flag": "LL" },
  "note": "Neutropenic fever - high mortality risk"
}
```

## Medication Patterns

### Hour-1 Bundle (SEP-1)

#### Antibiotics - Empiric Broad Spectrum
```json
{
  "community_acquired_pneumonia": [
    { "name": "Ceftriaxone", "dose": "2 g", "route": "IV", "frequency": "Q24H" },
    { "name": "Azithromycin", "dose": "500 mg", "route": "IV", "frequency": "Q24H" }
  ],
  "healthcare_associated": [
    { "name": "Piperacillin-Tazobactam", "dose": "4.5 g", "route": "IV", "frequency": "Q6H" },
    { "name": "Vancomycin", "dose": "1.5 g", "route": "IV", "frequency": "Q12H" }
  ],
  "suspected_mrsa": {
    "name": "Vancomycin",
    "code": "11124",
    "dose": "25 mg/kg",
    "route": "IV",
    "frequency": "Q8-12H",
    "note": "Adjust for renal function"
  },
  "suspected_pseudomonas": {
    "name": "Cefepime",
    "code": "25043",
    "dose": "2 g",
    "route": "IV",
    "frequency": "Q8H"
  }
}
```

#### Fluid Resuscitation
```json
{
  "initial_bolus": {
    "name": "Lactated Ringer's",
    "dose": "30 mL/kg",
    "route": "IV",
    "timing": "Within 3 hours",
    "note": "Approximately 2-3 L for average adult"
  }
}
```

### Vasopressors (if MAP < 65 after fluids)
```json
{
  "first_line": {
    "name": "Norepinephrine",
    "code": "7512",
    "dose": "0.1-0.5 mcg/kg/min",
    "route": "IV continuous",
    "note": "Central line preferred"
  },
  "second_line": {
    "name": "Vasopressin",
    "code": "11213",
    "dose": "0.03-0.04 units/min",
    "route": "IV continuous"
  },
  "refractory_shock": {
    "name": "Epinephrine",
    "code": "3616",
    "dose": "0.1-0.5 mcg/kg/min",
    "route": "IV continuous"
  }
}
```

### Adjunctive Therapies
```json
{
  "stress_dose_steroids": {
    "name": "Hydrocortisone",
    "dose": "200 mg/day",
    "route": "IV",
    "frequency": "50 mg Q6H or continuous",
    "indication": "Refractory shock despite vasopressors"
  },
  "blood_products": {
    "prbc": "Transfuse if Hgb < 7 g/dL",
    "platelets": "Transfuse if < 10 or < 20 with bleeding"
  }
}
```

## Encounter Patterns

### Emergency Department Presentation
- **Class Code**: E
- **CPT**: 99285
- **Critical Care Time**: 99291 (first 30-74 min), 99292 (each additional 30 min)
- **Disposition**: ICU admission 70%, floor admission 20%, transfer 10%

### ICU Admission
- **Class Code**: I
- **Location**: ICU
- **CPT**: 99223 (initial), 99233 (subsequent)
- **Critical Care**: 99291/99292 daily
- **Expected LOS**: 5-14 days for septic shock

### Sepsis DRGs
| DRG | Description | Weight | Expected LOS |
|-----|-------------|--------|--------------|
| 870 | Sepsis with MV > 96 hours | 4.9 | 12-18 days |
| 871 | Sepsis without MV > 96 hours with MCC | 1.87 | 6-10 days |
| 872 | Sepsis without MV > 96 hours with CC | 1.23 | 4-6 days |

## Example Output

### Septic Shock from Pneumonia

```json
{
  "patient": {
    "mrn": "MRN00000004",
    "name": { "given_name": "Dorothy", "family_name": "Anderson" },
    "birth_date": "1948-02-14",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "R65.21", "description": "Severe sepsis with septic shock", "type": "admitting" },
    { "code": "A41.9", "description": "Sepsis, unspecified organism", "type": "final" },
    { "code": "J18.9", "description": "Pneumonia, unspecified organism", "type": "final" },
    { "code": "N17.9", "description": "Acute kidney injury", "type": "final" },
    { "code": "J96.01", "description": "Acute respiratory failure with hypoxia", "type": "final" },
    { "code": "E11.9", "description": "Type 2 diabetes mellitus", "diagnosed_date": "2010-05-15" },
    { "code": "I10", "description": "Essential hypertension", "diagnosed_date": "2008-03-20" }
  ],
  "medications": [
    { "name": "Piperacillin-Tazobactam", "dose": "4.5 g", "route": "IV", "frequency": "Q6H", "status": "active" },
    { "name": "Vancomycin", "dose": "1.25 g", "route": "IV", "frequency": "Q12H", "status": "active" },
    { "name": "Norepinephrine", "dose": "0.15 mcg/kg/min", "route": "IV", "frequency": "Continuous", "status": "active" },
    { "name": "Hydrocortisone", "dose": "50 mg", "route": "IV", "frequency": "Q6H", "status": "active" },
    { "name": "Lactated Ringer's", "dose": "150 mL/hr", "route": "IV", "frequency": "Continuous", "status": "active" },
    { "name": "Insulin Regular", "dose": "Variable", "route": "IV", "frequency": "Continuous", "status": "active" }
  ],
  "labs": [
    { "test_name": "WBC", "loinc_code": "6690-2", "value": "18.5", "unit": "x10^3/uL", "flag": "H" },
    { "test_name": "Lactate", "loinc_code": "2524-7", "value": "5.8", "unit": "mmol/L", "flag": "HH" },
    { "test_name": "Creatinine", "loinc_code": "2160-0", "value": "3.2", "unit": "mg/dL", "flag": "HH" },
    { "test_name": "Procalcitonin", "loinc_code": "33959-8", "value": "28.5", "unit": "ng/mL", "flag": "HH" },
    { "test_name": "Platelets", "loinc_code": "777-3", "value": "85", "unit": "x10^3/uL", "flag": "L" },
    { "test_name": "Bilirubin Total", "loinc_code": "1975-2", "value": "2.8", "unit": "mg/dL", "flag": "H" },
    { "test_name": "pH", "loinc_code": "2744-1", "value": "7.28", "unit": "", "flag": "L" },
    { "test_name": "Bicarbonate", "loinc_code": "1963-8", "value": "17", "unit": "mmol/L", "flag": "L" },
    { "test_name": "Glucose", "loinc_code": "2345-7", "value": "185", "unit": "mg/dL", "flag": "H" }
  ],
  "vitals": {
    "observation_time": "2025-01-15T03:45:00",
    "temperature": 102.8,
    "heart_rate": 118,
    "respiratory_rate": 28,
    "systolic_bp": 82,
    "diastolic_bp": 48,
    "spo2": 89,
    "map": 59
  },
  "encounter": {
    "class_code": "I",
    "status": "in-progress",
    "department": "ICU",
    "chief_complaint": "Fever, confusion, shortness of breath",
    "admission_time": "2025-01-14T22:30:00",
    "admitting_diagnosis": "R65.21"
  }
}
```

## SEP-1 Bundle Compliance

For quality measure compliance, ensure:

1. **Hour 1 (from time zero)**:
   - Blood cultures obtained before antibiotics
   - Broad-spectrum antibiotics administered
   - Lactate measured

2. **Hour 3**:
   - 30 mL/kg crystalloid for hypotension or lactate >= 4

3. **Hour 6**:
   - Vasopressors if hypotension persists after fluid resuscitation
   - Repeat lactate if initial lactate elevated

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| SOFA score | 0-24 | 8 (organ dysfunction) |
| qSOFA | 0-3 | 2 (positive screen) |
| Lactate | Positive, mmol/L | 4.2 mmol/L (elevated) |
| MAP | Positive, mmHg | 58 mmHg (hypotensive) |
| WBC | Positive, cells/mcL | 18,500 (leukocytosis) |
| Temperature | 95-105°F or 35-41°C | 102.4°F (fever) |
| Creatinine | Positive, may be elevated | 2.1 mg/dL |
| Bilirubin | Positive, may be elevated | 3.5 mg/dL |

### Business Rules

- **Sepsis Definition**: Infection + SOFA ≥2 (or increase by 2)
- **Septic Shock**: Sepsis + vasopressors + lactate >2 despite fluids
- **SEP-1 Bundle**: Blood cultures, lactate, antibiotics, fluids within 3 hours
- **Time Zero**: When sepsis first recognized (not arrival time)
- **Fluid Resuscitation**: 30 mL/kg crystalloid for hypotension or lactate ≥4
- **Antibiotic Timing**: Broad-spectrum within 1 hour of recognition
- **Source Control**: Drain abscesses, remove infected devices
- **Mortality**: Increases ~8% per hour of delayed antibiotics

## Related Skills

### PatientSim Cohorts
- [SKILL.md](SKILL.md) - PatientSim overview
- [adt-workflow.md](adt-workflow.md) - Admission/transfer to ICU
- [orders-results.md](orders-results.md) - Lab ordering for sepsis workup

### Cross-Product: MemberSim
- [../membersim/facility-claims.md](../membersim/facility-claims.md) - ICU facility claims, sepsis DRG (870-872)
- [../membersim/professional-claims.md](../membersim/professional-claims.md) - Critical care billing (99291/99292)

> **Integration Pattern:** Use PatientSim for sepsis clinical progression and SEP-1 bundle compliance. Use MemberSim for high-acuity facility claims - sepsis with MCC (DRG 870) is high-cost admission.

### Cross-Product: RxMemberSim
- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Discharge antibiotic prescriptions

> **Integration Pattern:** Use PatientSim for IV antibiotic orders during admission. Use RxMemberSim for oral step-down antibiotics at discharge (if applicable).

### References
- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10, LOINC codes
- [../../references/validation-rules.md](../../references/validation-rules.md) - Clinical coherence rules
