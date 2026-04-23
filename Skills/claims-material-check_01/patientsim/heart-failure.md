---
name: heart-failure
description: "Heart failure patients with guideline-directed medical therapy across NYHA classes and EF categories. Triggers: heart failure, CHF, ejection fraction, HFrEF, HFpEF, HFmrEF, decompensated heart failure, cardiology, GDMT, cardiac"
---

# Heart Failure Cohort

A cohort template for generating heart failure patients with guideline-directed medical therapy across all NYHA classes and ejection fraction categories.

## For Claude

Use this skill when the user requests heart failure patient data or cardiology cohorts. This teaches you how to generate **realistic heart failure patients** with appropriate GDMT, lab patterns, and encounter types.

**When to apply this skill:**

- User mentions heart failure, CHF, or ejection fraction
- User requests HFrEF, HFpEF, or HFmrEF cohorts
- User asks for decompensated heart failure admissions
- User needs cardiology encounter examples

**Key capabilities this skill provides:**

- How to classify heart failure by ejection fraction and NYHA class
- How to generate appropriate GDMT medication regimens
- How to model stable vs decompensated presentations
- How to create cardiology follow-up patterns

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: heart-failure, cardiology, chf, gdmt, chronic-disease
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic heart failure patients across the spectrum from compensated outpatient to acute decompensation requiring hospitalization. It implements current guideline-directed medical therapy and appropriate diagnostic workup patterns.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "heart failure", "CHF", "congestive heart failure"
- "HFrEF", "HFpEF", "HFmrEF", "ejection fraction"
- "BNP", "NT-proBNP", "decompensated"
- "NYHA class", "cardiomyopathy"

**Clinical Cohorts**:

- "Generate a patient with HFrEF on GDMT"
- "Create a decompensated heart failure admission"
- "Generate a heart failure clinic follow-up"

## Trigger Phrases

- heart failure
- CHF
- congestive heart failure
- HFrEF
- HFpEF
- HFmrEF
- ejection fraction
- BNP
- NT-proBNP
- cardiomyopathy
- decompensated
- NYHA

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| age_range | range | 50-85 | Any valid adult range |
| ef_category | string | HFrEF | HFrEF (<40%), HFmrEF (40-49%), HFpEF (>=50%) |
| nyha_class | int | 2 | 1, 2, 3, 4 |
| etiology | string | ischemic | ischemic, hypertensive, idiopathic, valvular |
| acuity | string | stable | stable, decompensated |
| geography | string | null | County/tract FIPS for data-driven rates |

## Data Sources (PopulationSim v2.0)

When geography is specified, heart failure cohorts use real CDC PLACES data:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Key columns for cardiovascular:
  - CHD_CrudePrev: Coronary heart disease prevalence
  - STROKE_CrudePrev: Stroke prevalence  
  - BPHIGH_CrudePrev: Hypertension (HF risk factor)
  - OBESITY_CrudePrev: Obesity (HF risk factor)
  - (Note: CKD not in PLACES - use national estimate ~3%)
```

### Data-Driven Comorbidity Rates

| Comorbidity | Generic Default | PLACES Column |
|-------------|-----------------|---------------|
| Hypertension | 80% | BPHIGH_CrudePrev |
| Diabetes | 40% | DIABETES_CrudePrev |
| CKD | 50% | (not in PLACES - use default) |
| Atrial fibrillation | 30% | (not in PLACES - use default) |
| COPD | 30% | COPD_CrudePrev |

### Example: Cook County, IL (FIPS 17031)
```
From places_county_2024.csv:
  CHD_CrudePrev: 5.8%
  BPHIGH_CrudePrev: 33.2%
  DIABETES_CrudePrev: 11.4%
  KIDNEY_CrudePrev: 3.4%
  
Apply to HF generation:
  - Hypertensive etiology weight: Higher if BPHIGH > 35%
  - Diabetes comorbidity: 11.4% baseline (scale for HF population)
  - CKD comorbidity: 3.4% baseline (scale for HF population)
```

## Classification

### Ejection Fraction Categories

| Category | EF Range | Code | Description |
|----------|----------|------|-------------|
| HFrEF | < 40% | I50.2x | Heart failure with reduced ejection fraction |
| HFmrEF | 40-49% | I50.2x | Heart failure with mildly reduced EF |
| HFpEF | >= 50% | I50.3x | Heart failure with preserved ejection fraction |

### NYHA Functional Classification

| Class | Symptoms | Activity Level |
|-------|----------|----------------|
| I | No symptoms | Ordinary physical activity does not cause symptoms |
| II | Mild symptoms | Comfortable at rest, ordinary activity causes symptoms |
| III | Moderate symptoms | Comfortable at rest, less than ordinary activity causes symptoms |
| IV | Severe symptoms | Symptoms at rest, unable to carry out any physical activity |

## Diagnosis Codes

### Primary Diagnoses
| Code | Description | Use Case |
|------|-------------|----------|
| I50.9 | Heart failure, unspecified | General HF |
| I50.20 | Unspecified systolic HF | HFrEF, unspecified acuity |
| I50.21 | Acute systolic HF | Decompensated HFrEF |
| I50.22 | Chronic systolic HF | Stable HFrEF |
| I50.23 | Acute on chronic systolic HF | Exacerbation of chronic HFrEF |
| I50.30 | Unspecified diastolic HF | HFpEF, unspecified acuity |
| I50.31 | Acute diastolic HF | Decompensated HFpEF |
| I50.32 | Chronic diastolic HF | Stable HFpEF |
| I50.33 | Acute on chronic diastolic HF | Exacerbation of chronic HFpEF |

### Common Comorbidities
| Probability | Code | Description |
|-------------|------|-------------|
| 80% | I10 | Essential hypertension |
| 60% | E11.9 | Type 2 diabetes |
| 55% | I25.10 | Coronary artery disease |
| 50% | I48.91 | Atrial fibrillation |
| 45% | N18.3/N18.4 | Chronic kidney disease |
| 40% | E78.5 | Hyperlipidemia |
| 30% | J44.9 | COPD |

## Guideline-Directed Medical Therapy (GDMT)

### HFrEF Core Therapy (Four Pillars)

1. **ACE Inhibitor or ARB/ARNI**
```json
{
  "first_choice": {
    "name": "Sacubitril/Valsartan",
    "code": "1656340",
    "dose": "49/51 mg",
    "route": "PO",
    "frequency": "BID"
  },
  "alternative": {
    "name": "Lisinopril",
    "code": "104376",
    "dose": "20 mg",
    "route": "PO",
    "frequency": "QD"
  }
}
```

2. **Beta-Blocker**
```json
{
  "options": [
    {
      "name": "Carvedilol",
      "code": "20352",
      "dose": "25 mg",
      "route": "PO",
      "frequency": "BID"
    },
    {
      "name": "Metoprolol Succinate",
      "code": "866514",
      "dose": "100 mg",
      "route": "PO",
      "frequency": "QD"
    }
  ]
}
```

3. **SGLT2 Inhibitor**
```json
{
  "name": "Dapagliflozin",
  "code": "1488574",
  "dose": "10 mg",
  "route": "PO",
  "frequency": "QD"
}
```

4. **Mineralocorticoid Receptor Antagonist (MRA)**
```json
{
  "name": "Spironolactone",
  "code": "9997",
  "dose": "25 mg",
  "route": "PO",
  "frequency": "QD"
}
```

### Additional Therapies

- **Diuretics** (for congestion): Furosemide 40mg QD-BID
- **Hydralazine/Nitrate** (if ACEi/ARB intolerant, especially African American patients)
- **Digoxin** (for rate control in AFib or persistent symptoms)
- **ICD/CRT** (device therapy for EF <= 35%)

## Lab Patterns

### Stable Heart Failure
```json
{
  "bnp": { "min": 100, "max": 300, "unit": "pg/mL", "flag": "H" },
  "sodium": { "min": 136, "max": 142, "unit": "mmol/L", "flag": null },
  "potassium": { "min": 4.0, "max": 5.0, "unit": "mmol/L", "flag": null },
  "creatinine": { "min": 1.0, "max": 1.5, "unit": "mg/dL", "flag": null },
  "egfr": { "min": 45, "max": 80, "unit": "mL/min/1.73m2", "flag": null }
}
```

### Decompensated Heart Failure
```json
{
  "bnp": { "min": 500, "max": 2000, "unit": "pg/mL", "flag": "HH" },
  "sodium": { "min": 128, "max": 135, "unit": "mmol/L", "flag": "L" },
  "potassium": { "min": 3.2, "max": 5.5, "unit": "mmol/L", "flag": null },
  "creatinine": { "min": 1.5, "max": 3.0, "unit": "mg/dL", "flag": "H" },
  "egfr": { "min": 25, "max": 50, "unit": "mL/min/1.73m2", "flag": "L" },
  "lactate": { "min": 1.5, "max": 4.0, "unit": "mmol/L", "flag": "H" }
}
```

### Severe/Cardiogenic Shock
```json
{
  "bnp": { "min": 2000, "max": 10000, "unit": "pg/mL", "flag": "HH" },
  "sodium": { "min": 125, "max": 132, "unit": "mmol/L", "flag": "L" },
  "creatinine": { "min": 2.5, "max": 5.0, "unit": "mg/dL", "flag": "HH" },
  "lactate": { "min": 4.0, "max": 10.0, "unit": "mmol/L", "flag": "HH" },
  "troponin": { "min": 0.1, "max": 2.0, "unit": "ng/mL", "flag": "HH" }
}
```

## Vital Sign Patterns

### Stable (NYHA I-II)
```json
{
  "heart_rate": { "min": 60, "max": 80 },
  "systolic_bp": { "min": 100, "max": 130 },
  "diastolic_bp": { "min": 60, "max": 80 },
  "respiratory_rate": { "min": 14, "max": 18 },
  "spo2": { "min": 95, "max": 99 }
}
```

### Decompensated (NYHA III-IV)
```json
{
  "heart_rate": { "min": 90, "max": 120 },
  "systolic_bp": { "min": 90, "max": 110 },
  "diastolic_bp": { "min": 55, "max": 75 },
  "respiratory_rate": { "min": 22, "max": 32 },
  "spo2": { "min": 88, "max": 94 },
  "weight_change": "+5 to +15 lbs (fluid retention)"
}
```

## Encounter Patterns

### Outpatient Follow-Up
- **Frequency**: Every 1-3 months for stable HF
- **CPT Code**: 99214
- **Class Code**: O
- **Labs**: BMP, BNP (optional)
- **Monitoring**: Weight, symptoms, medication adherence

### Inpatient Admission (Decompensation)
- **Class Code**: I
- **CPT**: 99223 (initial), 99232/99233 (subsequent)
- **Expected LOS**: 4-7 days
- **DRG**: 291 (HF with MCC), 292 (HF with CC), 293 (HF without CC/MCC)
- **Discharge Planning**: Follow-up within 7 days, home health if needed

### Emergency Department
- **Class Code**: E
- **CPT**: 99284 or 99285
- **Disposition**: Admit 60%, Observe 25%, Discharge 15%

## Example Output

### Decompensated HFrEF with Hospitalization

```json
{
  "patient": {
    "mrn": "MRN00000002",
    "name": { "given_name": "Margaret", "family_name": "Wilson" },
    "birth_date": "1952-11-08",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "I50.23", "description": "Acute on chronic systolic heart failure", "type": "admitting" },
    { "code": "I25.10", "description": "Atherosclerotic heart disease", "diagnosed_date": "2018-05-14" },
    { "code": "I48.91", "description": "Atrial fibrillation", "diagnosed_date": "2020-02-20" },
    { "code": "I10", "description": "Essential hypertension", "diagnosed_date": "2010-03-15" },
    { "code": "N18.3", "description": "Chronic kidney disease, stage 3", "diagnosed_date": "2021-08-10" }
  ],
  "medications": [
    { "name": "Sacubitril/Valsartan", "dose": "49/51 mg", "frequency": "BID", "status": "active" },
    { "name": "Carvedilol", "dose": "25 mg", "frequency": "BID", "status": "active" },
    { "name": "Dapagliflozin", "dose": "10 mg", "frequency": "QD", "status": "active" },
    { "name": "Spironolactone", "dose": "25 mg", "frequency": "QD", "status": "active" },
    { "name": "Furosemide", "dose": "80 mg", "route": "IV", "frequency": "BID", "status": "active" },
    { "name": "Apixaban", "dose": "5 mg", "frequency": "BID", "status": "active" }
  ],
  "labs": [
    { "test_name": "BNP", "loinc_code": "30934-4", "value": "1850", "unit": "pg/mL", "flag": "HH" },
    { "test_name": "Sodium", "loinc_code": "2951-2", "value": "132", "unit": "mmol/L", "flag": "L" },
    { "test_name": "Potassium", "loinc_code": "2823-3", "value": "4.8", "unit": "mmol/L", "flag": null },
    { "test_name": "Creatinine", "loinc_code": "2160-0", "value": "1.8", "unit": "mg/dL", "flag": "H" },
    { "test_name": "Troponin I", "loinc_code": "10839-9", "value": "0.08", "unit": "ng/mL", "flag": "H" }
  ],
  "vitals": {
    "observation_time": "2025-01-15T14:30:00",
    "heart_rate": 98,
    "systolic_bp": 102,
    "diastolic_bp": 68,
    "respiratory_rate": 24,
    "spo2": 91,
    "temperature": 98.2,
    "weight_kg": 82.5
  },
  "encounter": {
    "class_code": "I",
    "status": "in-progress",
    "chief_complaint": "Shortness of breath, leg swelling",
    "admission_time": "2025-01-14T18:45:00",
    "admitting_diagnosis": "I50.23"
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Ejection fraction | 0-80% (typically 10-70%) | 35% (HFrEF) |
| NYHA class | I, II, III, or IV | Class III |
| BNP | Positive, elevated in HF | 850 pg/mL |
| NT-proBNP | Positive, elevated in HF | 2500 pg/mL |
| Creatinine | Positive, may be elevated | 1.4 mg/dL |
| Potassium | 3.5-5.5 mEq/L (watch with ACEi/ARB) | 4.8 mEq/L |
| GDMT medications | Appropriate for EF category | Beta-blocker for HFrEF |
| Diuretic dose | Match fluid status | Furosemide 40-80mg |

### Business Rules

- **HFrEF (EF ≤40%)**: GDMT includes ACEi/ARB/ARNI, beta-blocker, MRA, SGLT2i
- **HFpEF (EF ≥50%)**: Focus on diuretics, BP control, treat comorbidities
- **HFmrEF (EF 41-49%)**: May benefit from HFrEF therapies
- **Decompensation**: IV diuretics, fluid restriction, daily weights
- **Lab Monitoring**: Creatinine and potassium with ACEi/ARB initiation/titration
- **Device Therapy**: ICD if EF ≤35%; CRT if EF ≤35% + wide QRS
- **Readmission Risk**: 30-day readmission ~20%; medication adherence critical
- **Cardiorenal Syndrome**: HF and CKD commonly coexist; affects medication choices

## Related Skills

### PatientSim Cohorts

- [SKILL.md](SKILL.md) - PatientSim overview
- [diabetes-management.md](diabetes-management.md) - Common comorbidity
- [chronic-kidney-disease.md](chronic-kidney-disease.md) - Cardiorenal syndrome

### Cross-Product: TrialSim

- [../trialsim/therapeutic-areas/cardiovascular.md](../trialsim/therapeutic-areas/cardiovascular.md) - CV outcomes trials, MACE endpoints, adjudicated events

> **Integration Pattern:** Use this PatientSim skill for clinical HF care journeys. When generating CV outcomes trial data, apply TrialSim cardiovascular skill for trial-specific endpoints and SDTM mapping.

### Cross-Product: MemberSim

- [../membersim/professional-claims.md](../membersim/professional-claims.md) - Cardiology office visit claims
- [../membersim/facility-claims.md](../membersim/facility-claims.md) - Heart failure admission claims (DRG 291, 292, 293)

> **Integration Pattern:** Use PatientSim for HF encounters and clinical progression. Use MemberSim for claims generation - facility claims for admissions, professional claims for cardiology follow-ups.

### Cross-Product: RxMemberSim

- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - GDMT medication fills (carvedilol, lisinopril, furosemide)
- [../rxmembersim/specialty-pharmacy.md](../rxmembersim/specialty-pharmacy.md) - Sacubitril/valsartan (Entresto), SGLT2 inhibitors

> **Integration Pattern:** Use PatientSim for medication orders. Use RxMemberSim for pharmacy fills post-discharge and ongoing refill patterns. HF readmission risk correlates with medication adherence.

### References

- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10 codes
