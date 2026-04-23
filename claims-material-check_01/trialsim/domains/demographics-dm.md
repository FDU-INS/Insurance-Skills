---
name: demographics-dm
description: |
  Generate SDTM DM (Demographics) domain data with subject identifiers, 
  demographics, treatment arms, and reference dates. Required for all clinical 
  trial submissions. Triggers: "demographics", "DM domain", "subject data", 
  "USUBJID", "treatment arms", "randomization".
---

# Demographics (DM) Domain

The Demographics domain provides essential subject-level information required for all clinical trial submissions. DM contains one record per subject and serves as the foundation that all other SDTM domains reference via USUBJID.

---

## For Claude

This is a **core SDTM domain skill** for generating subject demographics. The DM domain is **required for every clinical trial dataset** - always include it first.

**Always apply this skill when you see:**
- Requests for clinical trial demographics
- SDTM dataset generation
- Subject-level data with treatment arms
- References to USUBJID, subject identifiers
- Trial enrollment or randomization data

**Key responsibilities:**
- Generate globally unique USUBJID values
- Assign treatment arms per randomization ratio
- Calculate age from birth date and reference start date
- Apply CDISC controlled terminology for SEX, RACE, ETHNIC

---

## SDTM Variables

### Required Variables

| Variable | Label | Type | Length | Description |
|----------|-------|------|--------|-------------|
| STUDYID | Study Identifier | Char | 20 | Unique study ID |
| DOMAIN | Domain Abbreviation | Char | 2 | "DM" |
| USUBJID | Unique Subject ID | Char | 40 | STUDYID-SITEID-SUBJID |
| SUBJID | Subject ID for Study | Char | 20 | Subject ID within study |
| RFSTDTC | Subject Reference Start Date/Time | Char | 19 | First study treatment date (ISO 8601) |
| RFENDTC | Subject Reference End Date/Time | Char | 19 | Last study treatment date (ISO 8601) |
| SITEID | Study Site Identifier | Char | 10 | Site number |
| AGE | Age | Num | 8 | Age at RFSTDTC |
| AGEU | Age Units | Char | 6 | YEARS |
| SEX | Sex | Char | 1 | M, F, U |
| RACE | Race | Char | 60 | CDISC controlled terminology |
| ETHNIC | Ethnicity | Char | 40 | HISPANIC OR LATINO, NOT HISPANIC OR LATINO |
| ARMCD | Planned Arm Code | Char | 20 | Treatment arm code |
| ARM | Description of Planned Arm | Char | 200 | Treatment arm description |
| COUNTRY | Country | Char | 3 | ISO 3166-1 alpha-3 |

### Expected Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| BRTHDTC | Date/Time of Birth | Char | ISO 8601 format |
| RFICDTC | Date/Time of Informed Consent | Char | Consent signature date |
| RFPENDTC | Date/Time of End of Participation | Char | Last contact date |
| DTHFL | Subject Death Flag | Char | Y or null |
| DTHDTC | Date/Time of Death | Char | Death date if applicable |
| ACTARMCD | Actual Arm Code | Char | May differ from planned |
| ACTARM | Description of Actual Arm | Char | May differ from planned |

---

## Controlled Terminology

### SEX (C66731)

| Code | Decode |
|------|--------|
| M | MALE |
| F | FEMALE |
| U | UNKNOWN |

### RACE (C74457)

| Value |
|-------|
| WHITE |
| BLACK OR AFRICAN AMERICAN |
| ASIAN |
| AMERICAN INDIAN OR ALASKA NATIVE |
| NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER |
| MULTIPLE |
| OTHER |
| UNKNOWN |
| NOT REPORTED |

### ETHNIC (C66790)

| Value |
|-------|
| HISPANIC OR LATINO |
| NOT HISPANIC OR LATINO |
| NOT REPORTED |
| UNKNOWN |

---

## Generation Patterns

### Standard Two-Arm Trial

```json
{
  "domain": "DM",
  "study": {
    "studyid": "TRIAL-2024-001",
    "arms": [
      { "armcd": "TRT", "arm": "Treatment 100mg QD", "ratio": 1 },
      { "armcd": "PBO", "arm": "Placebo", "ratio": 1 }
    ]
  },
  "sites": [
    { "siteid": "001", "country": "USA", "enrollment": 50 },
    { "siteid": "002", "country": "USA", "enrollment": 40 }
  ],
  "demographics": {
    "age_range": [18, 75],
    "sex_distribution": { "M": 0.48, "F": 0.52 },
    "race_distribution": {
      "WHITE": 0.65,
      "BLACK OR AFRICAN AMERICAN": 0.15,
      "ASIAN": 0.12,
      "OTHER": 0.08
    }
  }
}
```

### Multi-Arm Dose-Finding

```json
{
  "domain": "DM",
  "study": {
    "studyid": "DOSE-FIND-001",
    "arms": [
      { "armcd": "LOW", "arm": "Low Dose 50mg", "ratio": 1 },
      { "armcd": "MED", "arm": "Medium Dose 100mg", "ratio": 1 },
      { "armcd": "HIGH", "arm": "High Dose 200mg", "ratio": 1 },
      { "armcd": "PBO", "arm": "Placebo", "ratio": 1 }
    ]
  }
}
```

### USUBJID Generation

USUBJID must be globally unique across all studies. Standard format:

```
USUBJID = STUDYID + "-" + SITEID + "-" + SUBJID
Example: TRIAL-2024-001-001-0042
```

---

## Examples

### Example 1: Generate Demographics for Phase 3 Trial

**Request:** "Generate DM domain for a Phase 3 diabetes trial with 200 subjects, 2:1 randomization to treatment vs placebo, across 10 US sites"

**Output:**

```json
{
  "domain": "DM",
  "metadata": {
    "studyid": "DM2-PH3-001",
    "description": "Phase 3 Diabetes Trial Demographics",
    "n_subjects": 200,
    "n_sites": 10
  },
  "records": [
    {
      "STUDYID": "DM2-PH3-001",
      "DOMAIN": "DM",
      "USUBJID": "DM2-PH3-001-001-0001",
      "SUBJID": "0001",
      "RFSTDTC": "2024-03-15",
      "RFENDTC": "2024-09-20",
      "SITEID": "001",
      "BRTHDTC": "1968-07-22",
      "AGE": 55,
      "AGEU": "YEARS",
      "SEX": "F",
      "RACE": "WHITE",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "ARMCD": "TRT",
      "ARM": "Metformin XR 1000mg BID",
      "COUNTRY": "USA"
    },
    {
      "STUDYID": "DM2-PH3-001",
      "DOMAIN": "DM",
      "USUBJID": "DM2-PH3-001-001-0002",
      "SUBJID": "0002",
      "RFSTDTC": "2024-03-18",
      "RFENDTC": "2024-09-25",
      "SITEID": "001",
      "BRTHDTC": "1975-11-03",
      "AGE": 48,
      "AGEU": "YEARS",
      "SEX": "M",
      "RACE": "BLACK OR AFRICAN AMERICAN",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "ARMCD": "TRT",
      "ARM": "Metformin XR 1000mg BID",
      "COUNTRY": "USA"
    },
    {
      "STUDYID": "DM2-PH3-001",
      "DOMAIN": "DM",
      "USUBJID": "DM2-PH3-001-002-0003",
      "SUBJID": "0003",
      "RFSTDTC": "2024-03-20",
      "RFENDTC": "2024-09-28",
      "SITEID": "002",
      "BRTHDTC": "1960-02-14",
      "AGE": 64,
      "AGEU": "YEARS",
      "SEX": "F",
      "RACE": "ASIAN",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "ARMCD": "PBO",
      "ARM": "Placebo",
      "COUNTRY": "USA"
    }
  ],
  "summary": {
    "by_arm": {
      "TRT": 133,
      "PBO": 67
    },
    "by_sex": {
      "M": 96,
      "F": 104
    },
    "age_stats": {
      "mean": 54.2,
      "sd": 11.8,
      "min": 22,
      "max": 74
    }
  }
}
```

### Example 2: Global Multi-Site Demographics

**Request:** "Generate DM for an oncology trial with 50 subjects from USA, Germany, and Japan"

**Output:**

```json
{
  "domain": "DM",
  "metadata": {
    "studyid": "ONC-GLOB-001",
    "description": "Global Oncology Trial Demographics",
    "n_subjects": 50
  },
  "records": [
    {
      "STUDYID": "ONC-GLOB-001",
      "DOMAIN": "DM",
      "USUBJID": "ONC-GLOB-001-US01-0001",
      "SUBJID": "0001",
      "RFSTDTC": "2024-04-01",
      "RFENDTC": "2024-12-15",
      "SITEID": "US01",
      "BRTHDTC": "1962-05-18",
      "AGE": 61,
      "AGEU": "YEARS",
      "SEX": "M",
      "RACE": "WHITE",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "ARMCD": "COMBO",
      "ARM": "Pembrolizumab + Chemotherapy",
      "COUNTRY": "USA",
      "DTHFL": "Y",
      "DTHDTC": "2024-11-22"
    },
    {
      "STUDYID": "ONC-GLOB-001",
      "DOMAIN": "DM",
      "USUBJID": "ONC-GLOB-001-DE01-0015",
      "SUBJID": "0015",
      "RFSTDTC": "2024-04-10",
      "RFENDTC": "2025-01-05",
      "SITEID": "DE01",
      "BRTHDTC": "1970-09-30",
      "AGE": 53,
      "AGEU": "YEARS",
      "SEX": "F",
      "RACE": "WHITE",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "ARMCD": "MONO",
      "ARM": "Pembrolizumab Monotherapy",
      "COUNTRY": "DEU"
    },
    {
      "STUDYID": "ONC-GLOB-001",
      "DOMAIN": "DM",
      "USUBJID": "ONC-GLOB-001-JP01-0032",
      "SUBJID": "0032",
      "RFSTDTC": "2024-04-22",
      "RFENDTC": null,
      "SITEID": "JP01",
      "BRTHDTC": "1958-12-05",
      "AGE": 65,
      "AGEU": "YEARS",
      "SEX": "M",
      "RACE": "ASIAN",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "ARMCD": "COMBO",
      "ARM": "Pembrolizumab + Chemotherapy",
      "COUNTRY": "JPN"
    }
  ],
  "summary": {
    "by_country": {
      "USA": 20,
      "DEU": 15,
      "JPN": 15
    }
  }
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| USUBJID | Globally unique, concatenation of STUDYID-SITEID-SUBJID | DM2-PH3-001-001-0001 |
| AGE | Non-negative integer, calculated at RFSTDTC | 55 |
| AGEU | Must be "YEARS" for adults | YEARS |
| SEX | From CDISC codelist C66731 | M, F, U |
| RACE | From CDISC codelist C74457 | WHITE |
| ETHNIC | From CDISC codelist C66790 | NOT HISPANIC OR LATINO |
| RFSTDTC | ISO 8601 format, ≤ RFENDTC | 2024-03-15 |
| COUNTRY | ISO 3166-1 alpha-3 | USA, DEU, JPN |
| ARMCD | Short code, no spaces | TRT, PBO, LOW |
| ARM | Full description matching ARMCD | Treatment 100mg QD |

### Business Rules

- **One Record Per Subject**: DM must have exactly one record per USUBJID
- **Age Calculation**: AGE = floor((RFSTDTC - BRTHDTC) / 365.25)
- **Randomization Ratio**: Subject counts by arm should approximate the specified ratio
- **Treatment Assignment**: ARMCD/ARM must match values in the Trial Arms dataset (TA)
- **Death Consistency**: If DTHFL = "Y", DTHDTC must be populated and ≤ RFENDTC
- **Site Distribution**: Realistic enrollment patterns (not perfectly equal across sites)
- **Demographic Diversity**: Race/ethnicity should reflect geographic population and recruitment practices

---

## Related Skills

### TrialSim Domains
- [README.md](README.md) - Domain overview and SDTM basics
- [adverse-events-ae.md](adverse-events-ae.md) - AE domain references USUBJID from DM
- [vital-signs-vs.md](vital-signs-vs.md) - VS domain references USUBJID from DM

### TrialSim Core
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Trial design and terminology
- [../phase3-pivotal.md](../phase3-pivotal.md) - Phase 3 trial patterns
- [../recruitment-enrollment.md](../recruitment-enrollment.md) - Enrollment funnel

### Cross-Product: PatientSim
- [../../patientsim/SKILL.md](../../patientsim/SKILL.md) - Patient demographics foundation

> **Integration Pattern:** PatientSim's patient demographics can be transformed to DM domain format by:
> 1. Adding trial-specific identifiers (STUDYID, USUBJID)
> 2. Adding treatment arm assignment (ARMCD, ARM)
> 3. Adding reference dates (RFSTDTC, RFENDTC)
> 4. Mapping to CDISC controlled terminology

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial DM domain skill |
