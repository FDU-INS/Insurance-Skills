---
name: diabetes-management
description: "Type 2 diabetes mellitus cohorts across all stages - pre-diabetes through complex insulin-dependent regimens with complications. Triggers: diabetes, T2DM, diabetic patient, A1C, blood sugar, glucose control, metformin, insulin, diabetes medications, nephropathy, retinopathy, neuropathy, disease progression"
---

# Type 2 Diabetes Management Cohort - Disease Progression Events

A cohort template for generating patients with Type 2 diabetes mellitus across all stages of disease progression, from pre-diabetes through complex insulin-dependent regimens with complications.

## For Claude

Use this skill when the user requests diabetic patients or diabetes management cohorts. This teaches you how to generate **realistic clinical progressions** for Type 2 diabetes across all stages - from newly diagnosed through complex multi-medication regimens with complications.

**When to apply this skill:**
- User mentions diabetes, T2DM, diabetic patient
- User requests A1C levels, blood sugar, glucose control cohorts
- User specifies metformin, insulin, or other diabetes medications
- User asks for chronic disease management cohorts
- User mentions diabetes complications (nephropathy, retinopathy, neuropathy)
- User needs disease progression modeling over time

**Key capabilities this skill provides:**
- How to generate disease progression from pre-diabetes through insulin-dependent stages
- How to match A1C levels with appropriate medication regimens
- How to apply complication probabilities based on disease duration
- How to create realistic lab panels for different control statuses
- How to sequence medication escalation appropriately
- How to model comorbidities (hypertension, hyperlipidemia, CKD)

## Metadata
- **Type**: cohort-template
- **Version**: 2.0
- **Author**: PatientSim
- **Tags**: diabetes, chronic-disease, endocrine, primary-care
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic Type 2 diabetes patients across the full spectrum of disease progression. It models the longitudinal management of diabetes from diagnosis through complex regimens, including medication escalation, complication development, and monitoring patterns.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:
- "diabetes", "diabetic", "T2DM", "Type 2 diabetes"
- "A1C", "hemoglobin A1C", "glycemic control"
- "blood sugar", "glucose", "hyperglycemia"
- "metformin", "insulin", "diabetes medications"
- "diabetes complications"

**Clinical Cohorts**:
- "Generate a diabetic patient"
- "Create a patient with poorly controlled diabetes"
- "Generate patients with diabetes and CKD"
- "Model disease progression over 10 years"

## Generation Guidelines

When generating diabetic patients:
1. **Match A1C to control status**: Well-controlled (<7%), moderate (7-8.5%), poor (>8.5%)
2. **Apply comorbidities**: Hypertension (75%), hyperlipidemia (70%), obesity (85%)
3. **Progress complications by duration**: CKD risk increases after 10 years
4. **Escalate medications appropriately**: Start metformin, add SGLT2/GLP-1, then insulin
5. **Include appropriate labs**: A1C, CMP, lipid panel, urine microalbumin

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 45-75 | Patient age range |
| diabetes_duration | range | 0-20 | Years since diagnosis |
| control_level | enum | moderate | well-controlled, moderate, poorly-controlled |
| has_complications | boolean | false | Whether to include complications |
| geography | string | null | County/tract FIPS for data-driven rates |

## Data Sources (PopulationSim v2.0)

When a geography is specified, diabetes cohorts are grounded in real CDC PLACES data:

### Embedded Data Lookup

**County-Level Diabetes Data:**
```
File: skills/populationsim/data/county/places_county_2024.csv
Columns:
  - DIABETES_CrudePrev: Crude diabetes prevalence (%)
  - DIABETES_AdjPrev: Age-adjusted prevalence (%)
  - OBESITY_CrudePrev: Obesity rate (comorbidity weighting)
  - KIDNEY_CrudePrev: CKD rate (complication probability)
```

**Tract-Level Diabetes Data:**
```
File: skills/populationsim/data/tract/places_tract_2024.csv
Same columns as county, for neighborhood-level precision
```

### Data-Driven Comorbidity Rates

Instead of using generic defaults, look up actual rates for the specified geography:

| Comorbidity | Generic Default | Data-Driven Source |
|-------------|-----------------|-------------------|
| Hypertension | 75% | BPHIGH_CrudePrev from PLACES |
| Obesity | 85% | OBESITY_CrudePrev from PLACES |
| CKD | 15% (after 10yr) | KIDNEY_CrudePrev from PLACES |
| Depression | 20% | DEPRESSION_CrudePrev from PLACES |

**Example: Harris County, TX (FIPS 48201)**
```
From places_county_2024.csv:
  DIABETES_CrudePrev: 12.1%
  OBESITY_CrudePrev: 32.8%
  BPHIGH_CrudePrev: 32.4%
  KIDNEY_CrudePrev: 3.2%
  DEPRESSION_CrudePrev: 17.8%

Apply to generation:
  - Base diabetes rate: 12.1% (vs national 10.1%)
  - Obesity comorbidity: Scale from 32.8% baseline
  - Hypertension comorbidity: Scale from 32.4% baseline
```

### SDOH Context for Diabetes

For diabetes patients, SVI and ADI affect:
- **Medication adherence**: Higher vulnerability → lower adherence probability
- **A1C control**: Higher ADI → worse average control
- **Complication rates**: Higher SVI → earlier complication onset

```
File: skills/populationsim/data/county/svi_county_2022.csv
Key columns:
  - RPL_THEMES: Overall vulnerability (0-1)
  - EP_UNINSUR: Uninsured percentage (access barriers)
  - EP_POV150: Poverty rate (medication affordability)
```

### Provenance in Output

When using data-driven generation, include provenance:

```json
{
  "patient": { "...": "..." },
  "diabetes_context": {
    "local_prevalence": 0.121,
    "comorbidity_weights": {
      "obesity": 0.328,
      "hypertension": 0.324
    },
    "sdoh_factors": {
      "svi_overall": 0.68,
      "uninsured_rate": 0.181
    },
    "provenance": {
      "source": "CDC_PLACES_2024",
      "geography": "Harris County, TX (48201)",
      "data_year": 2022
    }
  }
}
```

## Generation Rules

### Demographics
- Age range: 45-75 years (peak incidence)
- Higher prevalence in certain ethnic groups
- BMI typically > 25

### Conditions
- E11.9 - Type 2 diabetes mellitus without complications
- E11.65 - Type 2 diabetes mellitus with hyperglycemia
- E11.22 - Type 2 diabetes with diabetic chronic kidney disease
- I10 - Essential hypertension (75% comorbidity)
- E78.5 - Hyperlipidemia (70% comorbidity)

### Vital Signs
- Blood pressure often elevated (>130/80)
- BMI typically > 30

### Medications
- Metformin 500-2000mg daily (first-line)
- SGLT2 inhibitors (empagliflozin, dapagliflozin)
- GLP-1 agonists (semaglutide, dulaglutide)
- Insulin glargine for advanced disease

### Timeline
- Diagnosis → Metformin → Add second agent (2-3 years) → Insulin if needed (5+ years)
- A1C monitoring every 3-6 months
- Annual comprehensive exams

## Variations

### Newly Diagnosed Diabetes
- Duration: 0-1 years
- A1C: 6.5-8.5%
- Medications: Metformin only
- Complications: None

### Well-Controlled Long-Term
- Duration: 5-15 years
- A1C: <7%
- Medications: Metformin + one additional agent
- Good adherence pattern

### Poorly Controlled with Complications
- Duration: 10+ years
- A1C: >9%
- Medications: Multiple agents including insulin
- Complications: Nephropathy, retinopathy, neuropathy

## Examples

### Example 1: Newly Diagnosed
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Sarah", "family_name": "Johnson" },
    "birth_date": "1975-06-20",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "E11.9", "description": "Type 2 diabetes without complications" }
  ],
  "medications": [
    { "name": "Metformin", "dose": "500 mg", "frequency": "BID" }
  ],
  "labs": [
    { "test_name": "HbA1c", "value": "7.2", "unit": "%" }
  ]
}
```

## Trigger Phrases

- diabetic patient
- diabetes
- T2DM
- Type 2 diabetes
- A1C
- blood sugar
- metformin
- insulin
- hyperglycemia
- glucose control

## Dependencies

- healthcare/clinical-domain.md

## Disease Progression Stages

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| age_range | range | 45-75 | Any valid adult range |
| control_status | string | moderate | well-controlled, moderate, poorly-controlled |
| duration_years | range | 0-20 | Years since diagnosis |
| complications | list | none | nephropathy, retinopathy, neuropathy, cardiovascular |

## Disease Progression Stages

### Stage 1: Pre-diabetes
- **A1C Range**: 5.7% - 6.4%
- **Duration**: 1-5 years without intervention
- **Codes**: R73.03 (Prediabetes)
- **Medications**: Lifestyle modification only

### Stage 2: New Diagnosis
- **A1C Range**: 6.5% - 8.5%
- **Codes**: E11.9 (Type 2 diabetes without complications)
- **Medications**: Metformin 500mg BID, titrate to 1000mg BID
- **Initial Labs**: A1C, CMP, lipid panel, UA with microalbumin
- **Follow-up**: 2 weeks phone, 4-6 weeks office, then q3 months

### Stage 3: Early Management (0-3 years)
- **A1C Target**: < 7.0%
- **Medications**: Metformin + possible second agent
- **Monitoring**: A1C every 3 months until stable, then every 6 months

### Stage 4: Medication Escalation (3-10 years)
- **A1C Range**: Variable, may be above target
- **Add Medications**:
  - SGLT2 inhibitors (empagliflozin, dapagliflozin)
  - GLP-1 receptor agonists (semaglutide, dulaglutide)
  - DPP-4 inhibitors (sitagliptin, linagliptin)
- **Considerations**: Cardiovascular or renal benefit preferred agents

### Stage 5: Complex Regimens (10+ years)
- **Insulin Required**: Basal insulin (glargine, degludec)
- **Possible Addition**: Bolus insulin for meals
- **A1C Target**: May relax to < 8.0% in elderly
- **Higher Complication Rate**: Check for nephropathy, retinopathy

## Comorbidities

| Comorbidity | Probability | ICD-10 Codes | Notes |
|-------------|-------------|--------------|-------|
| Hypertension | 75% | I10, I11.9 | Nearly universal in T2DM |
| Hyperlipidemia | 70% | E78.5, E78.0 | Statin therapy indicated |
| Obesity | 85% | E66.9, E66.01 | BMI > 30 common |
| CKD Stage 3+ | 40% | N18.3, N18.4 | Increases with duration > 10 years |
| CAD | 30% | I25.10 | Major cause of mortality |
| Retinopathy | 25% | E11.3x | Annual eye exams required |
| Neuropathy | 35% | E11.4x | Check monofilament yearly |

## Lab Patterns by Control Status

### Well-Controlled
```json
{
  "a1c": { "min": 6.0, "max": 7.0, "flag": null },
  "fasting_glucose": { "min": 80, "max": 120, "flag": null },
  "creatinine": { "min": 0.8, "max": 1.2, "flag": null },
  "egfr": { "min": 60, "max": 120, "flag": null },
  "urine_microalbumin": { "min": 0, "max": 30, "flag": null }
}
```

### Moderate Control
```json
{
  "a1c": { "min": 7.0, "max": 8.5, "flag": "H" },
  "fasting_glucose": { "min": 120, "max": 180, "flag": "H" },
  "creatinine": { "min": 1.0, "max": 1.5, "flag": null },
  "egfr": { "min": 45, "max": 90, "flag": null },
  "urine_microalbumin": { "min": 30, "max": 300, "flag": "H" }
}
```

### Poorly Controlled
```json
{
  "a1c": { "min": 8.5, "max": 12.0, "flag": "H" },
  "fasting_glucose": { "min": 180, "max": 350, "flag": "HH" },
  "creatinine": { "min": 1.3, "max": 2.5, "flag": "H" },
  "egfr": { "min": 30, "max": 60, "flag": "L" },
  "urine_microalbumin": { "min": 300, "max": 3000, "flag": "HH" }
}
```

## Medication Patterns

### First-Line Therapy
```json
{
  "name": "Metformin",
  "code": "860975",
  "dose": "1000 mg",
  "route": "PO",
  "frequency": "BID",
  "indication": "E11.9"
}
```

### Add-On Therapies (by priority)

1. **SGLT2 Inhibitor** (if CKD or CVD risk)
```json
{
  "name": "Empagliflozin",
  "code": "1545653",
  "dose": "10 mg",
  "route": "PO",
  "frequency": "QD",
  "indication": "E11.65"
}
```

2. **GLP-1 Receptor Agonist** (if weight loss desired)
```json
{
  "name": "Semaglutide",
  "code": "1991302",
  "dose": "0.5 mg",
  "route": "SubQ",
  "frequency": "Weekly",
  "indication": "E11.65"
}
```

3. **Basal Insulin** (if A1C > 10% or significant hyperglycemia)
```json
{
  "name": "Insulin Glargine",
  "code": "274783",
  "dose": "10 units",
  "route": "SubQ",
  "frequency": "QHS",
  "indication": "E11.65"
}
```

## Encounter Patterns

### Routine Follow-Up
- **Frequency**: Every 3-6 months
- **CPT Code**: 99213 or 99214
- **Labs**: A1C, BMP
- **Class Code**: O (Outpatient)

### New Diagnosis Visit
- **CPT Code**: 99215 or 99205
- **Labs**: A1C, CMP, lipid panel, UA with microalbumin, TSH
- **Education**: Diabetes self-management, nutrition referral
- **Follow-up Schedule**:
  - Phone check at 2 weeks
  - Office visit at 4-6 weeks
  - Quarterly thereafter

### Annual Comprehensive Visit
- **CPT Code**: 99214 or 99215
- **Labs**: A1C, CMP, lipid panel, UA with microalbumin
- **Referrals**: Ophthalmology (dilated eye exam), Podiatry (foot exam)
- **Screenings**: Depression (PHQ-9), foot monofilament exam

## Example Output

### Poorly Controlled Type 2 Diabetes with Complications

```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Robert", "family_name": "Martinez" },
    "birth_date": "1960-04-12",
    "gender": "M"
  },
  "diagnoses": [
    { "code": "E11.65", "description": "Type 2 diabetes with hyperglycemia", "diagnosed_date": "2015-03-20" },
    { "code": "E11.22", "description": "Type 2 diabetes with diabetic CKD", "diagnosed_date": "2022-08-15" },
    { "code": "I10", "description": "Essential hypertension", "diagnosed_date": "2014-11-10" },
    { "code": "E78.5", "description": "Hyperlipidemia", "diagnosed_date": "2015-06-22" },
    { "code": "N18.3", "description": "Chronic kidney disease, stage 3", "diagnosed_date": "2022-08-15" }
  ],
  "medications": [
    { "name": "Metformin", "dose": "1000 mg", "frequency": "BID", "status": "active" },
    { "name": "Empagliflozin", "dose": "10 mg", "frequency": "QD", "status": "active" },
    { "name": "Insulin Glargine", "dose": "30 units", "frequency": "QHS", "status": "active" },
    { "name": "Lisinopril", "dose": "20 mg", "frequency": "QD", "status": "active" },
    { "name": "Atorvastatin", "dose": "40 mg", "frequency": "QHS", "status": "active" }
  ],
  "labs": [
    { "test_name": "HbA1c", "loinc_code": "4548-4", "value": "9.2", "unit": "%", "flag": "H" },
    { "test_name": "Glucose", "loinc_code": "2345-7", "value": "215", "unit": "mg/dL", "flag": "H" },
    { "test_name": "Creatinine", "loinc_code": "2160-0", "value": "1.6", "unit": "mg/dL", "flag": "H" },
    { "test_name": "eGFR", "loinc_code": "48642-3", "value": "48", "unit": "mL/min/1.73m2", "flag": "L" },
    { "test_name": "Urine Microalbumin", "loinc_code": "14957-5", "value": "180", "unit": "mg/L", "flag": "H" }
  ],
  "encounter": {
    "class_code": "O",
    "chief_complaint": "Diabetes follow-up, A1C elevated",
    "admission_time": "2025-01-15T09:00:00"
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| A1C | 4.0-14.0% (realistic range) | 8.5% (uncontrolled) |
| Fasting glucose | 70-400 mg/dL | 145 mg/dL |
| eGFR | 0-120 mL/min/1.73m² | 65 (CKD stage 2) |
| Creatinine | Positive, correlates with eGFR | 1.2 mg/dL |
| Diabetes type | Type 1, Type 2, GDM, other | "Type 2" |
| Medications | Appropriate for A1C level | Metformin + SGLT2i |
| Diagnosis code | Valid ICD-10 | E11.9, E11.65 |
| Duration | Years since diagnosis | 8 years |

### Business Rules

- **Medication Escalation**: Start metformin → add second agent if A1C >7.5% → add third if still uncontrolled
- **eGFR Thresholds**: Metformin contraindicated if eGFR <30; adjust dose if 30-45
- **A1C Targets**: <7% for most adults; <8% for elderly or complex patients
- **Complication Screening**: Annual eye exam, foot exam, urine microalbumin
- **Insulin Initiation**: If A1C >10% or oral agents fail; start basal, may add bolus
- **GLP-1/SGLT2i**: Preferred add-ons for CV or renal benefit; often require PA
- **Hypoglycemia Risk**: Higher with sulfonylureas and insulin
- **Weight Considerations**: GLP-1s and SGLT2i promote weight loss; insulin may cause gain

## Related Skills

### PatientSim
- [SKILL.md](SKILL.md) - PatientSim overview
- [chronic-kidney-disease.md](chronic-kidney-disease.md) - CKD cohorts (common comorbidity)
- [heart-failure.md](heart-failure.md) - Heart failure cohorts

### Cross-Product: MemberSim
- [../membersim/professional-claims.md](../membersim/professional-claims.md) - Office visit claims for diabetes management
- [../membersim/accumulator-tracking.md](../membersim/accumulator-tracking.md) - Deductible/OOP tracking for chronic care

> **Integration Pattern:** Use PatientSim for clinical encounters and lab monitoring. Use MemberSim for E&M claims (99213/99214) and chronic care management billing.

### Cross-Product: RxMemberSim
- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Oral diabetes medication fills
- [../rxmembersim/specialty-pharmacy.md](../rxmembersim/specialty-pharmacy.md) - GLP-1 agonists, insulin
- [../rxmembersim/rx-prior-auth.md](../rxmembersim/rx-prior-auth.md) - PA for newer agents (SGLT2i, GLP-1)
- [../rxmembersim/formulary-management.md](../rxmembersim/formulary-management.md) - Tier placement for diabetes drugs

> **Integration Pattern:** Use PatientSim for medication orders and clinical monitoring. Use RxMemberSim for pharmacy fills, refill patterns, and adherence tracking.

### References
- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10, LOINC codes
