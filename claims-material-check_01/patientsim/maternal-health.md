---
name: maternal-health
description: "Obstetric patients across pregnancy phases - prenatal care, labor and delivery, postpartum. Triggers: pregnancy, prenatal, obstetric, gestational diabetes, preeclampsia, labor, delivery, postpartum, OB, maternal"
---

# Maternal Health Cohort

A cohort template for generating obstetric patients across pregnancy phases including prenatal care, labor and delivery, and postpartum follow-up.

## For Claude

Use this skill when the user requests pregnancy or obstetric patient data. This teaches you how to generate **realistic maternal health cohorts** with appropriate prenatal visits, complications, and delivery outcomes.

**When to apply this skill:**

- User mentions pregnancy, prenatal, or obstetric care
- User requests gestational diabetes or preeclampsia cohorts
- User asks for labor and delivery data
- User needs postpartum encounter examples

**Key capabilities this skill provides:**

- How to model pregnancy by gestational age and trimester
- How to generate appropriate prenatal visit schedules
- How to create pregnancy complications (GDM, preeclampsia, preterm labor)
- How to model labor, delivery, and postpartum encounters

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: PatientSim
- **Tags**: obstetrics, pregnancy, prenatal, maternal-health, labor-delivery
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic obstetric patient data across all phases of pregnancy. It supports prenatal visit schedules, pregnancy complications, labor and delivery events, and postpartum follow-up with appropriate clinical documentation.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "pregnancy", "pregnant", "prenatal", "obstetric"
- "gestational diabetes", "GDM", "preeclampsia"
- "labor and delivery", "cesarean", "postpartum"
- "gravida", "para", "trimester"

**Clinical Cohorts**:

- "Generate a 28-week prenatal visit"
- "Create a gestational diabetes case with insulin"
- "Generate a severe preeclampsia admission"

## Trigger Phrases

- pregnancy
- pregnant patient
- prenatal
- obstetric
- OB patient
- labor and delivery
- postpartum
- gestational diabetes
- preeclampsia
- cesarean
- c-section
- maternal
- antepartum

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| gestational_age | string | 28 weeks | 8-42 weeks, or trimester (first, second, third) |
| pregnancy_type | string | singleton | singleton, twin, triplet |
| risk_level | string | low | low, moderate, high |
| complications | list | none | gdm, preeclampsia, preterm_labor, placenta_previa, iugr, multiple_gestation |
| delivery_type | string | vaginal | vaginal, cesarean, vbac |
| phase | string | antepartum | antepartum, intrapartum, postpartum |
| gravida | int | 1 | Number of pregnancies |
| para | int | 0 | Number of deliveries |
| geography | string | null | County/tract FIPS for data-driven rates |

## Data Sources (PopulationSim v2.0)

When geography is specified, maternal health cohorts use real population data:

### Embedded Data Lookup

```
File: skills/populationsim/data/county/places_county_2024.csv
Relevant columns for maternal health:
  - DIABETES_CrudePrev: Baseline diabetes (GDM risk proxy)
  - OBESITY_CrudePrev: Obesity (GDM, preeclampsia risk)
  - BPHIGH_CrudePrev: Hypertension (preeclampsia risk)
  - ACCESS2_CrudePrev: Uninsured (prenatal access)
```

### Data-Driven Risk Factors

| Condition | Risk Factors | PLACES Source |
|-----------|-------------|---------------|
| Gestational Diabetes | Obesity, age, ethnicity | OBESITY_CrudePrev, DIABETES_CrudePrev |
| Preeclampsia | Obesity, hypertension | OBESITY_CrudePrev, BPHIGH_CrudePrev |
| Preterm Birth | SDOH factors, stress | SVI RPL_THEMES |

### SDOH Impact on Maternal Outcomes

```
File: skills/populationsim/data/county/svi_county_2022.csv
Impact on maternal health:
  - EP_UNINSUR: Delayed prenatal care, late initiation
  - RPL_THEME1 (socioeconomic): Maternal mortality disparities
  - EP_MINRTY: Racial disparities in outcomes
```

## Diagnosis Codes

### Pregnancy Status

| Code | Description |
|------|-------------|
| Z33.1 | Pregnant state, incidental |
| Z34.00 | Supervision of normal first pregnancy, unspecified trimester |
| Z34.80 | Supervision of other normal pregnancy, unspecified trimester |
| Z34.90 | Supervision of normal pregnancy, unspecified |
| O09.00-O09.93 | Supervision of high-risk pregnancy |

### Gestational Diabetes

| Code | Description |
|------|-------------|
| O24.410 | GDM in pregnancy, diet controlled |
| O24.414 | GDM in pregnancy, insulin controlled |
| O24.415 | GDM in pregnancy, controlled by oral hypoglycemic drugs |
| O24.419 | GDM in pregnancy, unspecified control |

### Hypertensive Disorders

| Code | Description |
|------|-------------|
| O13.1-O13.9 | Gestational hypertension |
| O14.00-O14.05 | Mild to moderate preeclampsia |
| O14.10-O14.15 | Severe preeclampsia |
| O14.20-O14.25 | HELLP syndrome |
| O15.00-O15.9 | Eclampsia |
| O16.1-O16.9 | Unspecified maternal hypertension |

### Labor and Delivery

| Code | Description |
|------|-------------|
| O60.10-O60.14 | Preterm labor with preterm delivery |
| O62.0-O62.9 | Abnormalities of forces of labor |
| O68 | Labor complicated by fetal stress |
| O69.0-O69.9 | Labor complicated by cord complications |
| O70.0-O70.9 | Perineal laceration during delivery |
| O72.0-O72.3 | Postpartum hemorrhage |

### Delivery Outcome

| Code | Description |
|------|-------------|
| O80 | Single spontaneous delivery |
| O82 | Single delivery by cesarean section |
| Z37.0 | Single live birth |
| Z37.2 | Twins, both liveborn |
| Z37.1 | Single stillborn |

### Postpartum Complications

| Code | Description |
|------|-------------|
| O85 | Puerperal sepsis |
| O86.0-O86.89 | Other puerperal infections |
| O87.0-O87.9 | Venous complications in puerperium |
| O90.3 | Peripartum cardiomyopathy |
| O90.89 | Other complications of puerperium |
| F53.0 | Postpartum depression |
| F53.1 | Puerperal psychosis |

## Prenatal Visit Schedule

### Low-Risk Pregnancy

| Gestational Age | Visit Type | Key Screenings |
|-----------------|------------|----------------|
| 8-10 weeks | Initial OB visit | Dating US, prenatal panel |
| 11-13 weeks | First trimester screen | NT scan, PAPP-A, hCG |
| 15-20 weeks | Quad screen | AFP, hCG, estriol, inhibin-A |
| 18-22 weeks | Anatomy scan | Detailed fetal anatomy US |
| 24-28 weeks | Glucose challenge | 1-hour glucose tolerance |
| 28 weeks | Routine visit | Tdap, RhoGAM if Rh-negative |
| 32 weeks | Routine visit | Growth assessment |
| 36 weeks | Group B strep | GBS culture |
| 37-40 weeks | Weekly visits | NST if indicated |

### High-Risk Additions

| Condition | Additional Monitoring |
|-----------|----------------------|
| GDM | Weekly glucose logs, growth US q4 weeks |
| Preeclampsia | Twice weekly BP, weekly labs, BPP/NST |
| Multiple gestation | US q4 weeks, cervical length |
| IUGR | Weekly/biweekly Doppler studies |
| Prior preterm | Cervical length, progesterone |

## Common Lab Tests

### First Trimester Panel

| Test | LOINC | Normal Range |
|------|-------|--------------|
| Blood type | 883-9 | A, B, AB, O |
| Rh factor | 10331-7 | Positive/Negative |
| Antibody screen | 890-4 | Negative |
| CBC | 57021-8 | See CBC ranges |
| Rubella IgG | 8014-3 | Immune |
| Hepatitis B sAg | 5196-1 | Negative |
| HIV | 75622-1 | Negative |
| Syphilis (RPR) | 20507-0 | Nonreactive |
| Urinalysis | 24356-8 | Normal |
| Urine culture | 630-4 | No growth |

### Glucose Testing

| Test | LOINC | Normal/Threshold |
|------|-------|------------------|
| 1-hour glucose challenge | 1504-0 | <140 mg/dL |
| Fasting glucose (3-hour GTT) | 1558-6 | <95 mg/dL |
| 1-hour glucose (3-hour GTT) | 20438-8 | <180 mg/dL |
| 2-hour glucose (3-hour GTT) | 20436-2 | <155 mg/dL |
| 3-hour glucose (3-hour GTT) | 20437-0 | <140 mg/dL |

### Preeclampsia Labs

| Test | LOINC | Significance |
|------|-------|--------------|
| Urine protein/creatinine ratio | 2890-2 | ≥0.3 = significant |
| 24-hour urine protein | 2889-4 | ≥300 mg = proteinuria |
| AST | 1920-8 | Elevated in HELLP |
| ALT | 1742-6 | Elevated in HELLP |
| Platelets | 777-3 | <100K in HELLP |
| LDH | 2532-0 | Elevated in hemolysis |
| Creatinine | 2160-0 | Elevated = renal involvement |
| Uric acid | 3084-1 | Elevated in preeclampsia |

## Medications

### Prenatal Supplements

| Medication | Dose | Indication |
|------------|------|------------|
| Prenatal vitamin | 1 daily | All pregnancies |
| Folic acid | 400-4000 mcg daily | Neural tube defect prevention |
| Iron sulfate | 325 mg daily | Anemia prevention/treatment |
| Calcium + Vitamin D | 1000 mg/600 IU daily | Bone health |
| DHA/Omega-3 | 200-300 mg daily | Fetal brain development |

### GDM Management

| Medication | Dose | Notes |
|------------|------|-------|
| Insulin NPH | Variable | Basal insulin |
| Insulin lispro | Variable | Mealtime insulin |
| Metformin | 500-2000 mg daily | Alternative to insulin |
| Glyburide | 2.5-10 mg daily | Alternative to insulin |

### Preeclampsia Management

| Medication | Dose | Indication |
|------------|------|------------|
| Labetalol | 200-800 mg BID-TID | Hypertension |
| Nifedipine ER | 30-90 mg daily | Hypertension |
| Magnesium sulfate | 4-6g load, 1-2g/hr | Seizure prophylaxis |
| Hydralazine | 5-10 mg IV PRN | Acute hypertension |
| Betamethasone | 12 mg IM x2 | Fetal lung maturity (24-34 wks) |

### Labor Medications

| Medication | Dose | Indication |
|------------|------|------------|
| Oxytocin | 1-20 mU/min IV | Labor induction/augmentation |
| Misoprostol | 25 mcg vaginal | Cervical ripening |
| Epidural (bupivacaine) | 0.0625-0.125% | Labor analgesia |
| Fentanyl | 50-100 mcg IV | Labor analgesia |
| Cefazolin | 2g IV | Cesarean prophylaxis |

### Postpartum

| Medication | Dose | Indication |
|------------|------|------------|
| Ibuprofen | 600-800 mg q6h | Pain, anti-inflammatory |
| Oxycodone | 5-10 mg q4-6h PRN | Moderate-severe pain |
| Docusate | 100 mg BID | Stool softener |
| RhoGAM | 300 mcg IM | Rh-negative mother |
| Sertraline | 50-200 mg daily | Postpartum depression |

## Clinical Cohorts

### Cohort 1: Uncomplicated Prenatal Visit

**Request:** "Generate a 28-week prenatal visit for a healthy primigravida"

```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Jessica", "family_name": "Martinez" },
    "birth_date": "1992-04-15",
    "gender": "F",
    "age": 32
  },
  "pregnancy": {
    "gravida": 1,
    "para": 0,
    "edd": "2025-04-20",
    "gestational_age_weeks": 28,
    "gestational_age_days": 3,
    "lmp": "2024-07-14",
    "risk_level": "low"
  },
  "diagnoses": [
    { "code": "Z34.02", "description": "Supervision of normal first pregnancy, second trimester" }
  ],
  "vitals": {
    "observation_time": "2025-01-15T10:30:00",
    "weight_kg": 72.5,
    "weight_gain_kg": 8.2,
    "systolic_bp": 118,
    "diastolic_bp": 72,
    "fundal_height_cm": 28,
    "fetal_heart_rate": 145
  },
  "labs": [
    { "test_name": "1-hour glucose", "loinc_code": "1504-0", "value": "124", "unit": "mg/dL", "flag": null },
    { "test_name": "Hemoglobin", "loinc_code": "718-7", "value": "11.8", "unit": "g/dL", "flag": null },
    { "test_name": "Hematocrit", "loinc_code": "4544-3", "value": "35.2", "unit": "%", "flag": null }
  ],
  "medications": [
    { "name": "Prenatal vitamin", "dose": "1 tablet", "frequency": "QD", "status": "active" },
    { "name": "Iron sulfate", "dose": "325 mg", "frequency": "QD", "status": "active" }
  ],
  "immunizations": [
    { "vaccine": "Tdap", "cvx_code": "115", "date": "2025-01-15", "site": "left deltoid" }
  ],
  "encounter": {
    "class_code": "O",
    "chief_complaint": "28-week prenatal visit",
    "next_appointment": "2025-01-29"
  }
}
```

### Cohort 2: Gestational Diabetes Management

**Request:** "Generate a patient with gestational diabetes on insulin"

```json
{
  "patient": {
    "mrn": "MRN00000002",
    "name": { "given_name": "Amanda", "family_name": "Chen" },
    "birth_date": "1988-11-22",
    "gender": "F",
    "age": 36
  },
  "pregnancy": {
    "gravida": 2,
    "para": 1,
    "edd": "2025-03-15",
    "gestational_age_weeks": 32,
    "risk_level": "high"
  },
  "diagnoses": [
    { "code": "O24.414", "description": "GDM in pregnancy, insulin controlled" },
    { "code": "O09.512", "description": "Supervision of elderly primigravida, second trimester" },
    { "code": "Z3A.32", "description": "32 weeks gestation" }
  ],
  "vitals": {
    "observation_time": "2025-01-15T14:00:00",
    "weight_kg": 82.1,
    "systolic_bp": 122,
    "diastolic_bp": 78,
    "fundal_height_cm": 33,
    "fetal_heart_rate": 140
  },
  "labs": [
    { "test_name": "Fasting glucose", "loinc_code": "1558-6", "value": "92", "unit": "mg/dL", "flag": null },
    { "test_name": "2-hour postprandial glucose", "loinc_code": "1521-4", "value": "118", "unit": "mg/dL", "flag": null },
    { "test_name": "HbA1c", "loinc_code": "4548-4", "value": "5.8", "unit": "%", "flag": null }
  ],
  "medications": [
    { "name": "Insulin NPH", "dose": "10 units", "frequency": "QHS", "route": "SubQ", "status": "active" },
    { "name": "Insulin lispro", "dose": "4-6 units", "frequency": "AC meals", "route": "SubQ", "status": "active" },
    { "name": "Prenatal vitamin", "dose": "1 tablet", "frequency": "QD", "status": "active" }
  ],
  "glucose_log": [
    { "date": "2025-01-14", "fasting": 88, "post_breakfast": 112, "post_lunch": 108, "post_dinner": 115 },
    { "date": "2025-01-13", "fasting": 94, "post_breakfast": 122, "post_lunch": 118, "post_dinner": 125 }
  ],
  "imaging": [
    {
      "study": "Growth ultrasound",
      "date": "2025-01-15",
      "findings": "EFW 2100g (75th percentile), AFI 14 cm, BPP 8/8"
    }
  ],
  "encounter": {
    "class_code": "O",
    "chief_complaint": "GDM follow-up, glucose log review",
    "plan": "Continue current insulin regimen, repeat growth US in 4 weeks"
  }
}
```

### Cohort 3: Severe Preeclampsia Admission

**Request:** "Generate a patient admitted with severe preeclampsia at 34 weeks"

```json
{
  "patient": {
    "mrn": "MRN00000003",
    "name": { "given_name": "Rachel", "family_name": "Thompson" },
    "birth_date": "1995-06-08",
    "gender": "F",
    "age": 29
  },
  "pregnancy": {
    "gravida": 1,
    "para": 0,
    "edd": "2025-02-26",
    "gestational_age_weeks": 34,
    "gestational_age_days": 2,
    "risk_level": "high"
  },
  "diagnoses": [
    { "code": "O14.13", "description": "Severe preeclampsia, third trimester" },
    { "code": "Z3A.34", "description": "34 weeks gestation" }
  ],
  "vitals": {
    "observation_time": "2025-01-15T08:30:00",
    "weight_kg": 78.5,
    "systolic_bp": 168,
    "diastolic_bp": 104,
    "heart_rate": 92,
    "respiratory_rate": 18,
    "spo2": 98,
    "reflexes": "3+ with clonus"
  },
  "labs": [
    { "test_name": "Urine protein/creatinine", "loinc_code": "2890-2", "value": "1.8", "unit": "mg/mg", "flag": "H" },
    { "test_name": "Platelets", "loinc_code": "777-3", "value": "142", "unit": "x10^3/uL", "flag": null },
    { "test_name": "AST", "loinc_code": "1920-8", "value": "48", "unit": "U/L", "flag": "H" },
    { "test_name": "ALT", "loinc_code": "1742-6", "value": "52", "unit": "U/L", "flag": "H" },
    { "test_name": "Creatinine", "loinc_code": "2160-0", "value": "0.9", "unit": "mg/dL", "flag": null },
    { "test_name": "LDH", "loinc_code": "2532-0", "value": "280", "unit": "U/L", "flag": "H" },
    { "test_name": "Uric acid", "loinc_code": "3084-1", "value": "7.2", "unit": "mg/dL", "flag": "H" }
  ],
  "medications": [
    { "name": "Magnesium sulfate", "dose": "4g IV load then 2g/hr", "route": "IV", "status": "active", "indication": "seizure prophylaxis" },
    { "name": "Labetalol", "dose": "200 mg", "frequency": "BID", "route": "PO", "status": "active" },
    { "name": "Betamethasone", "dose": "12 mg", "route": "IM", "status": "active", "indication": "fetal lung maturity" }
  ],
  "fetal_monitoring": {
    "type": "continuous",
    "baseline_fhr": 145,
    "variability": "moderate",
    "accelerations": "present",
    "decelerations": "none",
    "category": "I"
  },
  "encounter": {
    "class_code": "I",
    "admission_time": "2025-01-15T06:45:00",
    "admitting_diagnosis": "O14.13",
    "chief_complaint": "Severe headache, elevated BP at home (160/100)",
    "plan": "Complete betamethasone course, delivery at 34 weeks if stable; immediate delivery if deterioration"
  }
}
```

### Cohort 4: Postpartum Visit

**Request:** "Generate a 6-week postpartum visit after uncomplicated vaginal delivery"

```json
{
  "patient": {
    "mrn": "MRN00000004",
    "name": { "given_name": "Emily", "family_name": "Davis" },
    "birth_date": "1990-03-12",
    "gender": "F",
    "age": 34
  },
  "pregnancy": {
    "gravida": 2,
    "para": 2,
    "delivery_date": "2024-12-01",
    "delivery_type": "NSVD",
    "gestational_age_at_delivery": "39w2d",
    "birth_weight_grams": 3450,
    "apgar_1min": 8,
    "apgar_5min": 9
  },
  "diagnoses": [
    { "code": "Z39.2", "description": "Routine postpartum follow-up" },
    { "code": "Z37.0", "description": "Single live birth" },
    { "code": "O80", "description": "Single spontaneous delivery" }
  ],
  "vitals": {
    "observation_time": "2025-01-15T11:00:00",
    "weight_kg": 68.2,
    "systolic_bp": 116,
    "diastolic_bp": 72
  },
  "physical_exam": {
    "uterus": "Involuted, non-tender",
    "lochia": "Alba, scant",
    "perineum": "Healed, no tenderness",
    "breasts": "Soft, non-tender, lactating",
    "mood_screen": "PHQ-9 score: 3 (minimal depression)"
  },
  "medications": [
    { "name": "Prenatal vitamin", "dose": "1 tablet", "frequency": "QD", "status": "active", "indication": "breastfeeding" }
  ],
  "contraception": {
    "method": "IUD",
    "type": "Mirena (levonorgestrel)",
    "placed_date": "2025-01-15"
  },
  "breastfeeding": {
    "status": "exclusive",
    "issues": "none"
  },
  "encounter": {
    "class_code": "O",
    "chief_complaint": "6-week postpartum visit",
    "plan": "Cleared for exercise and intercourse, IUD placed, continue prenatal vitamin while breastfeeding"
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Gestational age | 0-42 weeks | 38 weeks 2 days |
| EDD | Valid future date | 2025-06-15 |
| Gravida/Para | G≥P; P=TPAL format | G3P2012 |
| BP | Systolic/diastolic | 142/92 (preeclampsia) |
| Proteinuria | Negative to 4+ | 2+ (concerning) |
| GBS status | positive, negative, unknown | "positive" |
| Delivery type | vaginal, cesarean | "cesarean" |
| APGAR | 0-10 at 1 and 5 min | 8/9 |

### Business Rules

- **Prenatal Visits**: Monthly until 28 wks, biweekly 28-36 wks, weekly 36+ wks
- **Gestational Diabetes**: Screen at 24-28 weeks; earlier if risk factors
- **Preeclampsia**: BP ≥140/90 + proteinuria after 20 weeks; monitor closely
- **GBS Screening**: Collect at 36-37 weeks; treat if positive during labor
- **Term Pregnancy**: 37-42 weeks; delivery timing depends on risk factors
- **Post-Dates**: >42 weeks; consider induction by 41-42 weeks
- **High-Risk Conditions**: Chronic HTN, diabetes, multiple gestation, prior cesarean
- **Postpartum**: 6-week visit; screen for depression (Edinburgh scale)

## Related Skills

### PatientSim Cohorts

- [SKILL.md](SKILL.md) - PatientSim overview
- [diabetes-management.md](diabetes-management.md) - Pre-existing diabetes in pregnancy
- [heart-failure.md](heart-failure.md) - Peripartum cardiomyopathy

### Cross-Product: MemberSim

- [../membersim/professional-claims.md](../membersim/professional-claims.md) - Prenatal visit claims (global OB billing)
- [../membersim/facility-claims.md](../membersim/facility-claims.md) - Delivery claims (DRG 765-768), NICU if needed
- [../membersim/behavioral-health.md](../membersim/behavioral-health.md) - Postpartum depression screening/treatment claims

> **Integration Pattern:** Use PatientSim for prenatal visits, delivery, and postpartum care. Use MemberSim for global OB billing (59400/59510) or itemized claims, delivery facility DRGs.

### Cross-Product: RxMemberSim

- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Prenatal vitamins, postpartum medications
- [../rxmembersim/specialty-pharmacy.md](../rxmembersim/specialty-pharmacy.md) - Anticoagulants for high-risk pregnancies

> **Integration Pattern:** Use PatientSim for medication orders during pregnancy. Use RxMemberSim for pharmacy fills - prenatal vitamins (often OTC tier), postpartum contraception, and any maintenance medications.

### References

- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10-CM codes
