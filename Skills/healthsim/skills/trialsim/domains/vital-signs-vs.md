---
name: vital-signs-vs
description: |
  Generate SDTM VS (Vital Signs) domain data with blood pressure, heart rate, 
  temperature, weight, and other measurements at scheduled visits. Triggers: 
  "vital signs", "VS domain", "vitals", "blood pressure", "heart rate", 
  "temperature", "weight", "BMI".
---

# Vital Signs (VS) Domain

The Vital Signs domain captures measurements of body functions including blood pressure, heart rate, respiratory rate, temperature, height, and weight. VS is a Findings class domain with one record per measurement per time point per subject.

---

## For Claude

This is a **Findings class SDTM domain skill** for generating vital sign measurements. VS data is collected at every study visit and is essential for safety monitoring.

**Always apply this skill when you see:**
- Requests for vital signs or physiological measurements
- Blood pressure, pulse, temperature, respiration data
- Weight/height/BMI tracking
- Orthostatic vital signs
- Safety monitoring at scheduled visits

**Key responsibilities:**
- Generate realistic physiological values within normal/abnormal ranges
- Create visit-scheduled measurements with appropriate timing
- Handle position-dependent measurements (supine, sitting, standing)
- Flag clinically significant abnormalities

---

## SDTM Variables

### Required Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| STUDYID | Study Identifier | Char | Unique study ID |
| DOMAIN | Domain Abbreviation | Char | "VS" |
| USUBJID | Unique Subject ID | Char | From DM domain |
| VSSEQ | Sequence Number | Num | Unique within subject |
| VSTESTCD | Vital Signs Test Short Name | Char | Test code (e.g., SYSBP) |
| VSTEST | Vital Signs Test Name | Char | Full test name |
| VSORRES | Result or Finding in Original Units | Char | Observed value |
| VSORRESU | Original Units | Char | Unit of measure |

### Expected Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| VSSTRESC | Character Result/Finding Std Format | Char | Standardized result |
| VSSTRESN | Numeric Result/Finding Std Units | Num | Numeric value |
| VSSTRESU | Standard Units | Char | Standard unit |
| VSSTAT | Completion Status | Char | NOT DONE if missing |
| VSREASND | Reason Not Done | Char | Reason if VSSTAT = NOT DONE |
| VSPOS | Position of Subject | Char | SITTING, STANDING, SUPINE |
| VSLOC | Location of Measurement | Char | e.g., ARM, LEG |
| VSLAT | Laterality | Char | LEFT, RIGHT |
| VSBLFL | Baseline Flag | Char | Y for baseline record |
| VSDTC | Date/Time of Collection | Char | ISO 8601 |
| VSDY | Study Day | Num | Relative to RFSTDTC |
| VISITNUM | Visit Number | Num | Protocol visit number |
| VISIT | Visit Name | Char | Visit description |

---

## Controlled Terminology

### Test Codes (VSTESTCD)

| VSTESTCD | VSTEST | VSORRESU | Normal Range |
|----------|--------|----------|--------------|
| SYSBP | Systolic Blood Pressure | mmHg | 90-139 |
| DIABP | Diastolic Blood Pressure | mmHg | 60-89 |
| PULSE | Pulse Rate | beats/min | 60-100 |
| RESP | Respiratory Rate | breaths/min | 12-20 |
| TEMP | Temperature | C | 36.1-37.2 |
| HEIGHT | Height | cm | N/A |
| WEIGHT | Weight | kg | N/A |
| BMI | Body Mass Index | kg/m2 | 18.5-24.9 |
| OXYSAT | Oxygen Saturation | % | 95-100 |

### Position (VSPOS) - C71148

| Value | Description |
|-------|-------------|
| SITTING | Seated position |
| STANDING | Upright position |
| SUPINE | Lying face up |
| PRONE | Lying face down |
| SEMI-RECUMBENT | Partially reclined |

---

## Generation Patterns

### Standard Visit Schedule

```json
{
  "domain": "VS",
  "visit_schedule": [
    { "visitnum": 1, "visit": "SCREENING", "vsdy": -14, "tests": ["SYSBP", "DIABP", "PULSE", "RESP", "TEMP", "HEIGHT", "WEIGHT"] },
    { "visitnum": 2, "visit": "BASELINE", "vsdy": 1, "tests": ["SYSBP", "DIABP", "PULSE", "RESP", "TEMP", "WEIGHT"] },
    { "visitnum": 3, "visit": "WEEK 4", "vsdy": 29, "tests": ["SYSBP", "DIABP", "PULSE", "RESP", "TEMP", "WEIGHT"] },
    { "visitnum": 4, "visit": "WEEK 8", "vsdy": 57, "tests": ["SYSBP", "DIABP", "PULSE", "RESP", "TEMP", "WEIGHT"] },
    { "visitnum": 5, "visit": "WEEK 12", "vsdy": 85, "tests": ["SYSBP", "DIABP", "PULSE", "RESP", "TEMP", "WEIGHT"] },
    { "visitnum": 6, "visit": "END OF TREATMENT", "vsdy": 85, "tests": ["SYSBP", "DIABP", "PULSE", "RESP", "TEMP", "WEIGHT"] }
  ]
}
```

### Orthostatic Vital Signs

For orthostatic BP assessment, generate measurements at:
1. Supine (after 5 min rest)
2. Standing (immediately)
3. Standing (after 3 min)

```json
{
  "orthostatic_sequence": [
    { "position": "SUPINE", "timing": "After 5 min rest" },
    { "position": "STANDING", "timing": "Immediately" },
    { "position": "STANDING", "timing": "After 3 min" }
  ],
  "orthostatic_hypotension": {
    "definition": "SBP drop ≥20 mmHg or DBP drop ≥10 mmHg on standing"
  }
}
```

### Physiological Variability

| Measurement | Intra-subject SD | Diurnal Range |
|-------------|------------------|---------------|
| Systolic BP | 8-12 mmHg | ±10 mmHg |
| Diastolic BP | 6-8 mmHg | ±8 mmHg |
| Heart Rate | 5-10 bpm | ±15 bpm |
| Temperature | 0.3°C | 0.5-1.0°C |
| Weight | 0.5-1.0 kg | Daily fluctuation |

---

## Examples

### Example 1: Generate Vital Signs for Phase 3 Trial

**Request:** "Generate VS domain data for 3 subjects over 4 visits in a hypertension trial"

**Output:**

```json
{
  "domain": "VS",
  "metadata": {
    "studyid": "HTN-PH3-001",
    "description": "Vital Signs - Hypertension Phase 3 Trial",
    "n_subjects": 3,
    "n_records": 42
  },
  "records": [
    {
      "STUDYID": "HTN-PH3-001",
      "DOMAIN": "VS",
      "USUBJID": "HTN-PH3-001-001-0001",
      "VSSEQ": 1,
      "VSTESTCD": "SYSBP",
      "VSTEST": "Systolic Blood Pressure",
      "VSORRES": "152",
      "VSORRESU": "mmHg",
      "VSSTRESN": 152,
      "VSSTRESU": "mmHg",
      "VSPOS": "SITTING",
      "VSBLFL": "Y",
      "VSDTC": "2024-03-01",
      "VSDY": 1,
      "VISITNUM": 2,
      "VISIT": "BASELINE"
    },
    {
      "STUDYID": "HTN-PH3-001",
      "DOMAIN": "VS",
      "USUBJID": "HTN-PH3-001-001-0001",
      "VSSEQ": 2,
      "VSTESTCD": "DIABP",
      "VSTEST": "Diastolic Blood Pressure",
      "VSORRES": "96",
      "VSORRESU": "mmHg",
      "VSSTRESN": 96,
      "VSSTRESU": "mmHg",
      "VSPOS": "SITTING",
      "VSBLFL": "Y",
      "VSDTC": "2024-03-01",
      "VSDY": 1,
      "VISITNUM": 2,
      "VISIT": "BASELINE"
    },
    {
      "STUDYID": "HTN-PH3-001",
      "DOMAIN": "VS",
      "USUBJID": "HTN-PH3-001-001-0001",
      "VSSEQ": 3,
      "VSTESTCD": "PULSE",
      "VSTEST": "Pulse Rate",
      "VSORRES": "78",
      "VSORRESU": "beats/min",
      "VSSTRESN": 78,
      "VSSTRESU": "beats/min",
      "VSPOS": "SITTING",
      "VSBLFL": "Y",
      "VSDTC": "2024-03-01",
      "VSDY": 1,
      "VISITNUM": 2,
      "VISIT": "BASELINE"
    },
    {
      "STUDYID": "HTN-PH3-001",
      "DOMAIN": "VS",
      "USUBJID": "HTN-PH3-001-001-0001",
      "VSSEQ": 7,
      "VSTESTCD": "SYSBP",
      "VSTEST": "Systolic Blood Pressure",
      "VSORRES": "138",
      "VSORRESU": "mmHg",
      "VSSTRESN": 138,
      "VSSTRESU": "mmHg",
      "VSPOS": "SITTING",
      "VSDTC": "2024-04-26",
      "VSDY": 57,
      "VISITNUM": 4,
      "VISIT": "WEEK 8"
    },
    {
      "STUDYID": "HTN-PH3-001",
      "DOMAIN": "VS",
      "USUBJID": "HTN-PH3-001-001-0001",
      "VSSEQ": 8,
      "VSTESTCD": "DIABP",
      "VSTEST": "Diastolic Blood Pressure",
      "VSORRES": "88",
      "VSORRESU": "mmHg",
      "VSSTRESN": 88,
      "VSSTRESU": "mmHg",
      "VSPOS": "SITTING",
      "VSDTC": "2024-04-26",
      "VSDY": 57,
      "VISITNUM": 4,
      "VISIT": "WEEK 8"
    }
  ],
  "summary": {
    "sysbp_change": {
      "baseline_mean": 154.2,
      "week8_mean": 136.5,
      "change": -17.7
    }
  }
}
```

### Example 2: Orthostatic Vital Signs

**Request:** "Generate orthostatic BP measurements for a subject with documented orthostatic hypotension"

**Output:**

```json
{
  "domain": "VS",
  "records": [
    {
      "STUDYID": "NEURO-001",
      "DOMAIN": "VS",
      "USUBJID": "NEURO-001-003-0022",
      "VSSEQ": 1,
      "VSTESTCD": "SYSBP",
      "VSTEST": "Systolic Blood Pressure",
      "VSORRES": "138",
      "VSORRESU": "mmHg",
      "VSSTRESN": 138,
      "VSSTRESU": "mmHg",
      "VSPOS": "SUPINE",
      "VSDTC": "2024-05-15T09:00:00",
      "VSDY": 29,
      "VISITNUM": 3,
      "VISIT": "WEEK 4"
    },
    {
      "STUDYID": "NEURO-001",
      "DOMAIN": "VS",
      "USUBJID": "NEURO-001-003-0022",
      "VSSEQ": 2,
      "VSTESTCD": "DIABP",
      "VSTEST": "Diastolic Blood Pressure",
      "VSORRES": "82",
      "VSORRESU": "mmHg",
      "VSSTRESN": 82,
      "VSSTRESU": "mmHg",
      "VSPOS": "SUPINE",
      "VSDTC": "2024-05-15T09:00:00",
      "VSDY": 29,
      "VISITNUM": 3,
      "VISIT": "WEEK 4"
    },
    {
      "STUDYID": "NEURO-001",
      "DOMAIN": "VS",
      "USUBJID": "NEURO-001-003-0022",
      "VSSEQ": 3,
      "VSTESTCD": "SYSBP",
      "VSTEST": "Systolic Blood Pressure",
      "VSORRES": "112",
      "VSORRESU": "mmHg",
      "VSSTRESN": 112,
      "VSSTRESU": "mmHg",
      "VSPOS": "STANDING",
      "VSDTC": "2024-05-15T09:02:00",
      "VSDY": 29,
      "VISITNUM": 3,
      "VISIT": "WEEK 4"
    },
    {
      "STUDYID": "NEURO-001",
      "DOMAIN": "VS",
      "USUBJID": "NEURO-001-003-0022",
      "VSSEQ": 4,
      "VSTESTCD": "DIABP",
      "VSTEST": "Diastolic Blood Pressure",
      "VSORRES": "68",
      "VSORRESU": "mmHg",
      "VSSTRESN": 68,
      "VSSTRESU": "mmHg",
      "VSPOS": "STANDING",
      "VSDTC": "2024-05-15T09:02:00",
      "VSDY": 29,
      "VISITNUM": 3,
      "VISIT": "WEEK 4"
    }
  ],
  "orthostatic_assessment": {
    "sysbp_drop": 26,
    "diabp_drop": 14,
    "orthostatic_hypotension": true,
    "criteria_met": "SBP drop ≥20 mmHg AND DBP drop ≥10 mmHg"
  }
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| VSSEQ | Unique positive integer per subject | 1, 2, 3 |
| VSTESTCD | From CDISC VS codelist | SYSBP, DIABP, PULSE |
| VSORRES | Numeric string for measurements | "120" |
| VSORRESU | Matches VSTESTCD standard | mmHg, beats/min |
| VSSTRESN | Numeric, = VSORRES for most VS | 120 |
| VSPOS | From Position codelist when applicable | SITTING |
| VSDTC | ISO 8601 format | 2024-03-15T10:30:00 |
| VSBLFL | "Y" only for baseline record per test | Y |

### Business Rules

- **Physiological Plausibility**: Values must be within physiologically possible ranges
  - Systolic BP: 70-250 mmHg
  - Diastolic BP: 40-150 mmHg
  - Heart rate: 30-220 bpm
  - Temperature: 34-42°C
  - Oxygen saturation: 70-100%
  
- **BP Relationship**: Systolic BP must be > Diastolic BP (by at least 10 mmHg)

- **Baseline Flag**: Only one VSBLFL = "Y" per subject per VSTESTCD

- **Visit Consistency**: VISITNUM and VISIT must match protocol schedule

- **Height Stability**: HEIGHT should only change at screening (adults)

- **Weight Trajectory**: Weight changes should be physiologically realistic (<5% per month typical)

---

## Related Skills

### TrialSim Domains
- [README.md](README.md) - Domain overview
- [demographics-dm.md](demographics-dm.md) - Subject identifiers (USUBJID source)
- [laboratory-lb.md](laboratory-lb.md) - Related safety measurements
- [adverse-events-ae.md](adverse-events-ae.md) - VS abnormalities may trigger AEs

### TrialSim Core
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Visit schedule concepts
- [../therapeutic-areas/cardiovascular.md](../therapeutic-areas/cardiovascular.md) - CV-specific vital signs

### Cross-Product: PatientSim
- [../../patientsim/SKILL.md](../../patientsim/SKILL.md) - Vital sign generation

> **Integration Pattern:** PatientSim vital signs can be transformed to VS domain by:
> 1. Adding sequence numbers (VSSEQ)
> 2. Mapping to CDISC test codes (VSTESTCD)
> 3. Adding visit context (VISITNUM, VISIT, VSDY)
> 4. Standardizing units per CDISC terminology

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial VS domain skill |
