---
name: disposition-ds
description: |
  Generate SDTM DS (Disposition) domain data tracking subject status, study
  completion, discontinuation reasons, and protocol milestones. Critical for
  subject flow analysis. Triggers: "disposition", "DS domain", "discontinuation",
  "study completion", "withdrawal", "early termination", "subject flow".
---

# Disposition (DS) Domain

The Disposition domain captures protocol milestones and subject status changes including informed consent, randomization, treatment completion, and study discontinuation. DS is an **Events class** domain critical for CONSORT flow diagrams and subject accountability.

---

## For Claude

This is a **core SDTM domain skill** for generating subject disposition events. DS records document the subject's journey through the study from consent to completion or discontinuation.

**Always apply this skill when you see:**
- Requests for subject disposition or status data
- Study completion or discontinuation records
- CONSORT diagram data requirements
- Protocol deviation tracking
- Subject flow analysis data

**Key responsibilities:**
- Generate disposition events for key milestones
- Track discontinuation reasons with appropriate coding
- Record both study-level and treatment-level disposition
- Maintain chronological consistency with other domains
- Apply CDISC controlled terminology for disposition terms

---

## SDTM Variables

### Required Variables

| Variable | Label | Type | Length | Description |
|----------|-------|------|--------|-------------|
| STUDYID | Study Identifier | Char | 20 | Unique study ID |
| DOMAIN | Domain Abbreviation | Char | 2 | "DS" |
| USUBJID | Unique Subject ID | Char | 40 | From DM domain |
| DSSEQ | Sequence Number | Num | 8 | Unique within subject |
| DSTERM | Reported Term | Char | 200 | Disposition event description |
| DSDECOD | Standardized Disposition Term | Char | 200 | CDISC controlled term |
| DSCAT | Category for Disposition | Char | 40 | DISPOSITION EVENT, PROTOCOL MILESTONE |
| DSSCAT | Subcategory | Char | 40 | STUDY, TREATMENT |
| DSSTDTC | Start Date/Time | Char | 19 | ISO 8601 format |

### Expected Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| EPOCH | Epoch | Char | SCREENING, TREATMENT, FOLLOW-UP |
| VISITNUM | Visit Number | Num | Numeric visit identifier |
| VISIT | Visit Name | Char | Visit description |
| DSDY | Study Day | Num | Relative to RFSTDTC |

### Permissible Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| DSSPID | Sponsor-Defined Identifier | Char | Sponsor's event ID |
| DSREFID | Reference ID | Char | Internal reference |

---

## Controlled Terminology

### DSCAT (Category)

| Value | Use |
|-------|-----|
| DISPOSITION EVENT | Subject status changes |
| PROTOCOL MILESTONE | Key protocol events |
| OTHER EVENT | Other significant events |

### DSSCAT (Subcategory)

| Value | Description |
|-------|-------------|
| STUDY PARTICIPATION | Overall study status |
| TREATMENT | Treatment-specific disposition |
| STUDY COMPLETION | End of study events |

### DSDECOD - Protocol Milestones

| Code | Description |
|------|-------------|
| INFORMED CONSENT OBTAINED | Subject signed ICF |
| RANDOMIZED | Subject randomized to treatment |
| ENROLLED | Subject formally enrolled |
| TREATMENT STARTED | First dose administered |
| TREATMENT COMPLETED | Completed planned treatment |
| STUDY COMPLETED | Completed all study procedures |

### DSDECOD - Discontinuation Reasons

| Code | Description |
|------|-------------|
| ADVERSE EVENT | Discontinued due to AE |
| DEATH | Subject died |
| LACK OF EFFICACY | Treatment not effective |
| LOST TO FOLLOW-UP | Unable to contact subject |
| PHYSICIAN DECISION | Investigator decision |
| PREGNANCY | Subject became pregnant |
| PROTOCOL DEVIATION | Significant deviation |
| PROTOCOL VIOLATION | Major violation |
| SPONSOR DECISION | Sponsor terminated |
| STUDY TERMINATED BY SPONSOR | Entire study stopped |
| WITHDRAWAL BY SUBJECT | Subject chose to withdraw |
| COMPLETED | Successfully completed |

---

## Generation Patterns

### Standard Completer

Subject who completes the study per protocol:

```json
{
  "domain": "DS",
  "pattern": "completer",
  "milestones": [
    "INFORMED CONSENT OBTAINED",
    "RANDOMIZED",
    "TREATMENT STARTED",
    "TREATMENT COMPLETED",
    "STUDY COMPLETED"
  ]
}
```

### Treatment Discontinuation (AE)

Subject who stops treatment early due to adverse event:

```json
{
  "domain": "DS",
  "pattern": "ae_discontinuation",
  "milestones": [
    "INFORMED CONSENT OBTAINED",
    "RANDOMIZED",
    "TREATMENT STARTED"
  ],
  "discontinuation": {
    "reason": "ADVERSE EVENT",
    "level": "TREATMENT",
    "followed_to_completion": true
  }
}
```

### Early Study Withdrawal

Subject who withdraws consent entirely:

```json
{
  "domain": "DS",
  "pattern": "withdrawal",
  "milestones": [
    "INFORMED CONSENT OBTAINED",
    "RANDOMIZED",
    "TREATMENT STARTED"
  ],
  "discontinuation": {
    "reason": "WITHDRAWAL BY SUBJECT",
    "level": "STUDY"
  }
}
```

---

## Examples

### Example 1: Study Completer

**Request:** "Generate DS domain for a subject who completed a 24-week clinical trial per protocol"

**Output:**

```json
{
  "domain": "DS",
  "metadata": {
    "studyid": "TRIAL-2024-001",
    "usubjid": "TRIAL-2024-001-001-0025",
    "outcome": "COMPLETED"
  },
  "records": [
    {
      "STUDYID": "TRIAL-2024-001",
      "DOMAIN": "DS",
      "USUBJID": "TRIAL-2024-001-001-0025",
      "DSSEQ": 1,
      "DSTERM": "INFORMED CONSENT OBTAINED",
      "DSDECOD": "INFORMED CONSENT OBTAINED",
      "DSCAT": "PROTOCOL MILESTONE",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-01-08",
      "DSDY": -7,
      "EPOCH": "SCREENING",
      "VISITNUM": 1,
      "VISIT": "SCREENING"
    },
    {
      "STUDYID": "TRIAL-2024-001",
      "DOMAIN": "DS",
      "USUBJID": "TRIAL-2024-001-001-0025",
      "DSSEQ": 2,
      "DSTERM": "RANDOMIZED",
      "DSDECOD": "RANDOMIZED",
      "DSCAT": "PROTOCOL MILESTONE",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-01-15",
      "DSDY": 1,
      "EPOCH": "TREATMENT",
      "VISITNUM": 2,
      "VISIT": "DAY 1/RANDOMIZATION"
    },
    {
      "STUDYID": "TRIAL-2024-001",
      "DOMAIN": "DS",
      "USUBJID": "TRIAL-2024-001-001-0025",
      "DSSEQ": 3,
      "DSTERM": "COMPLETED STUDY TREATMENT",
      "DSDECOD": "COMPLETED",
      "DSCAT": "DISPOSITION EVENT",
      "DSSCAT": "TREATMENT",
      "DSSTDTC": "2024-07-08",
      "DSDY": 175,
      "EPOCH": "TREATMENT",
      "VISITNUM": 14,
      "VISIT": "WEEK 24/END OF TREATMENT"
    },
    {
      "STUDYID": "TRIAL-2024-001",
      "DOMAIN": "DS",
      "USUBJID": "TRIAL-2024-001-001-0025",
      "DSSEQ": 4,
      "DSTERM": "COMPLETED STUDY",
      "DSDECOD": "COMPLETED",
      "DSCAT": "DISPOSITION EVENT",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-08-05",
      "DSDY": 203,
      "EPOCH": "FOLLOW-UP",
      "VISITNUM": 15,
      "VISIT": "FOLLOW-UP WEEK 4"
    }
  ]
}
```

### Example 2: Treatment Discontinuation Due to Adverse Event

**Request:** "Generate DS for a subject who discontinued treatment at week 8 due to grade 3 hepatotoxicity but remained in study for safety follow-up"

**Output:**

```json
{
  "domain": "DS",
  "metadata": {
    "studyid": "HEP-SAFE-001",
    "usubjid": "HEP-SAFE-001-003-0112",
    "outcome": "TREATMENT DISCONTINUED - STUDY COMPLETED"
  },
  "records": [
    {
      "STUDYID": "HEP-SAFE-001",
      "DOMAIN": "DS",
      "USUBJID": "HEP-SAFE-001-003-0112",
      "DSSEQ": 1,
      "DSTERM": "INFORMED CONSENT OBTAINED",
      "DSDECOD": "INFORMED CONSENT OBTAINED",
      "DSCAT": "PROTOCOL MILESTONE",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-02-01",
      "DSDY": -14,
      "EPOCH": "SCREENING",
      "VISITNUM": 1,
      "VISIT": "SCREENING"
    },
    {
      "STUDYID": "HEP-SAFE-001",
      "DOMAIN": "DS",
      "USUBJID": "HEP-SAFE-001-003-0112",
      "DSSEQ": 2,
      "DSTERM": "RANDOMIZED",
      "DSDECOD": "RANDOMIZED",
      "DSCAT": "PROTOCOL MILESTONE",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-02-15",
      "DSDY": 1,
      "EPOCH": "TREATMENT",
      "VISITNUM": 2,
      "VISIT": "DAY 1/BASELINE"
    },
    {
      "STUDYID": "HEP-SAFE-001",
      "DOMAIN": "DS",
      "USUBJID": "HEP-SAFE-001-003-0112",
      "DSSEQ": 3,
      "DSTERM": "DISCONTINUED TREATMENT DUE TO ADVERSE EVENT - HEPATOTOXICITY",
      "DSDECOD": "ADVERSE EVENT",
      "DSCAT": "DISPOSITION EVENT",
      "DSSCAT": "TREATMENT",
      "DSSTDTC": "2024-04-11",
      "DSDY": 56,
      "EPOCH": "TREATMENT",
      "VISITNUM": 6,
      "VISIT": "WEEK 8"
    },
    {
      "STUDYID": "HEP-SAFE-001",
      "DOMAIN": "DS",
      "USUBJID": "HEP-SAFE-001-003-0112",
      "DSSEQ": 4,
      "DSTERM": "COMPLETED STUDY - SAFETY FOLLOW-UP",
      "DSDECOD": "COMPLETED",
      "DSCAT": "DISPOSITION EVENT",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-05-09",
      "DSDY": 84,
      "EPOCH": "FOLLOW-UP",
      "VISITNUM": 8,
      "VISIT": "SAFETY FOLLOW-UP WEEK 4"
    }
  ],
  "summary": {
    "treatment_completed": false,
    "treatment_discontinuation_reason": "ADVERSE EVENT",
    "study_completed": true,
    "days_on_treatment": 55
  }
}
```

### Example 3: Withdrawal by Subject

**Request:** "Generate DS for a subject who withdrew consent at week 4 and left the study entirely"

**Output:**

```json
{
  "domain": "DS",
  "metadata": {
    "studyid": "CONSENT-001",
    "usubjid": "CONSENT-001-002-0067",
    "outcome": "WITHDRAWN"
  },
  "records": [
    {
      "STUDYID": "CONSENT-001",
      "DOMAIN": "DS",
      "USUBJID": "CONSENT-001-002-0067",
      "DSSEQ": 1,
      "DSTERM": "INFORMED CONSENT OBTAINED",
      "DSDECOD": "INFORMED CONSENT OBTAINED",
      "DSCAT": "PROTOCOL MILESTONE",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-03-01",
      "DSDY": -5,
      "EPOCH": "SCREENING",
      "VISITNUM": 1,
      "VISIT": "SCREENING"
    },
    {
      "STUDYID": "CONSENT-001",
      "DOMAIN": "DS",
      "USUBJID": "CONSENT-001-002-0067",
      "DSSEQ": 2,
      "DSTERM": "RANDOMIZED",
      "DSDECOD": "RANDOMIZED",
      "DSCAT": "PROTOCOL MILESTONE",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-03-06",
      "DSDY": 1,
      "EPOCH": "TREATMENT",
      "VISITNUM": 2,
      "VISIT": "DAY 1/BASELINE"
    },
    {
      "STUDYID": "CONSENT-001",
      "DOMAIN": "DS",
      "USUBJID": "CONSENT-001-002-0067",
      "DSSEQ": 3,
      "DSTERM": "SUBJECT WITHDREW CONSENT",
      "DSDECOD": "WITHDRAWAL BY SUBJECT",
      "DSCAT": "DISPOSITION EVENT",
      "DSSCAT": "TREATMENT",
      "DSSTDTC": "2024-04-03",
      "DSDY": 29,
      "EPOCH": "TREATMENT",
      "VISITNUM": 4,
      "VISIT": "WEEK 4"
    },
    {
      "STUDYID": "CONSENT-001",
      "DOMAIN": "DS",
      "USUBJID": "CONSENT-001-002-0067",
      "DSSEQ": 4,
      "DSTERM": "SUBJECT WITHDREW CONSENT - LEFT STUDY",
      "DSDECOD": "WITHDRAWAL BY SUBJECT",
      "DSCAT": "DISPOSITION EVENT",
      "DSSCAT": "STUDY PARTICIPATION",
      "DSSTDTC": "2024-04-03",
      "DSDY": 29,
      "EPOCH": "TREATMENT",
      "VISITNUM": 4,
      "VISIT": "WEEK 4"
    }
  ],
  "summary": {
    "treatment_completed": false,
    "treatment_discontinuation_reason": "WITHDRAWAL BY SUBJECT",
    "study_completed": false,
    "study_discontinuation_reason": "WITHDRAWAL BY SUBJECT",
    "days_on_study": 28
  }
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| DSSEQ | Positive integer, unique within USUBJID | 1, 2, 3 |
| DSTERM | Descriptive text of event | INFORMED CONSENT OBTAINED |
| DSDECOD | From CDISC controlled terminology | COMPLETED, ADVERSE EVENT |
| DSCAT | DISPOSITION EVENT or PROTOCOL MILESTONE | PROTOCOL MILESTONE |
| DSSCAT | STUDY PARTICIPATION or TREATMENT | TREATMENT |
| DSSTDTC | ISO 8601 format | 2024-03-15 |
| DSDY | Integer, can be negative for screening | -7, 1, 56 |
| EPOCH | From Trial Epochs | SCREENING, TREATMENT, FOLLOW-UP |

### Business Rules

- **Chronological Order**: Events must be in chronological order by DSSTDTC
- **Required Milestones**: INFORMED CONSENT OBTAINED must be first event for any enrolled subject
- **Dual Disposition**: Subjects may have separate TREATMENT and STUDY dispositions
- **Date Consistency**: 
  - INFORMED CONSENT date ≤ RANDOMIZATION date ≤ TREATMENT START
  - DSDY = (DSSTDTC - DM.RFSTDTC) + 1
- **Discontinuation Logic**: 
  - Treatment discontinuation doesn't require study discontinuation
  - Study discontinuation implies treatment discontinuation
- **Death Handling**: If DSDECOD = "DEATH", must match DM.DTHFL and DM.DTHDTC
- **Screen Failures**: Subjects who fail screening have INFORMED CONSENT but no RANDOMIZED event

---

## Related Skills

### TrialSim Domains
- [README.md](README.md) - Domain overview and SDTM basics
- [demographics-dm.md](demographics-dm.md) - Subject identifiers, RFSTDTC reference
- [adverse-events-ae.md](adverse-events-ae.md) - AEs that trigger discontinuation
- [exposure-ex.md](exposure-ex.md) - Treatment exposure before discontinuation

### TrialSim Core
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Trial design and terminology
- [../recruitment-enrollment.md](../recruitment-enrollment.md) - Screening and enrollment
- [../phase3-pivotal.md](../phase3-pivotal.md) - Phase 3 disposition patterns

### Cross-Product: PatientSim
- [../../patientsim/SKILL.md](../../patientsim/SKILL.md) - Patient care transitions

> **Integration Pattern:** DS events should correlate with:
> - DM.RFENDTC for treatment end date
> - AE domain for adverse event-related discontinuations
> - EX domain last dose date
> - Screen failure tracking in recruitment-enrollment.md

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial DS domain skill |
