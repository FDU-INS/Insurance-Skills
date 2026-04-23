---
name: laboratory-lb
description: |
  Generate SDTM LB (Laboratory Test Results) domain data with LOINC coding, 
  reference ranges, and abnormality flags. Covers chemistry, hematology, 
  urinalysis panels. Triggers: "laboratory", "LB domain", "lab results", 
  "chemistry panel", "CBC", "hematology", "LOINC".
---

# Laboratory Test Results (LB) Domain

The Laboratory domain captures clinical laboratory test results including chemistry panels, hematology, urinalysis, and specialized tests. LB is a Findings class domain with one record per test per time point per subject.

---

## For Claude

This is a **Findings class SDTM domain skill** for generating laboratory test results. LB data is critical for safety monitoring and efficacy assessment.

**Always apply this skill when you see:**
- Requests for laboratory or lab results data
- Chemistry panels (CMP, BMP), liver function tests (LFTs)
- Hematology (CBC, differential)
- Reference ranges or abnormality flags
- LOINC codes or lab coding

**Key responsibilities:**
- Generate physiologically realistic lab values
- Apply appropriate reference ranges by age/sex
- Use LOINC codes for standardization
- Flag clinically significant abnormalities
- Handle units and unit conversions

---

## SDTM Variables

### Required Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| STUDYID | Study Identifier | Char | Unique study ID |
| DOMAIN | Domain Abbreviation | Char | "LB" |
| USUBJID | Unique Subject ID | Char | From DM domain |
| LBSEQ | Sequence Number | Num | Unique within subject |
| LBTESTCD | Lab Test Short Name | Char | Test code (e.g., ALT) |
| LBTEST | Lab Test Name | Char | Full test name |
| LBORRES | Result or Finding in Original Units | Char | Original value |
| LBORRESU | Original Units | Char | Original unit |

### Expected Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| LBSTRESC | Character Result Std Format | Char | Standardized result |
| LBSTRESN | Numeric Result Std Units | Num | Numeric value |
| LBSTRESU | Standard Units | Char | SI units |
| LBSTNRLO | Reference Range Lower Limit Std | Num | Normal low |
| LBSTNRHI | Reference Range Upper Limit Std | Num | Normal high |
| LBNRIND | Reference Range Indicator | Char | NORMAL, HIGH, LOW |
| LBCAT | Category for Lab Test | Char | CHEMISTRY, HEMATOLOGY |
| LBSPEC | Specimen Type | Char | SERUM, PLASMA, URINE |
| LBMETHOD | Method of Test | Char | Test methodology |
| LBBLFL | Baseline Flag | Char | Y for baseline |
| LBDTC | Date/Time of Collection | Char | ISO 8601 |
| LBDY | Study Day | Num | Relative to RFSTDTC |
| VISITNUM | Visit Number | Num | Protocol visit |
| VISIT | Visit Name | Char | Visit description |
| LBLOINC | LOINC Code | Char | Standardized code |

---

## Common Laboratory Panels

### Chemistry Panel (CMP)

| LBTESTCD | LBTEST | LBSTRESU | Reference Range | LOINC |
|----------|--------|----------|-----------------|-------|
| ALT | Alanine Aminotransferase | U/L | 7-56 | 1742-6 |
| AST | Aspartate Aminotransferase | U/L | 10-40 | 1920-8 |
| ALP | Alkaline Phosphatase | U/L | 44-147 | 6768-6 |
| BILI | Total Bilirubin | umol/L | 3-21 | 1975-2 |
| ALB | Albumin | g/L | 35-50 | 1751-7 |
| CREAT | Creatinine | umol/L | 62-106 (M), 44-80 (F) | 2160-0 |
| BUN | Blood Urea Nitrogen | mmol/L | 2.5-7.1 | 3094-0 |
| GLUC | Glucose | mmol/L | 3.9-5.6 (fasting) | 2345-7 |
| SODIUM | Sodium | mmol/L | 136-145 | 2951-2 |
| POTASSIUM | Potassium | mmol/L | 3.5-5.0 | 2823-3 |
| CHLORIDE | Chloride | mmol/L | 98-106 | 2075-0 |
| CO2 | Carbon Dioxide | mmol/L | 23-29 | 2028-9 |
| CALCIUM | Calcium | mmol/L | 2.15-2.55 | 17861-6 |

### Liver Function Tests (LFTs)

| LBTESTCD | LBTEST | Clinical Significance |
|----------|--------|----------------------|
| ALT | Alanine Aminotransferase | Hepatocellular injury |
| AST | Aspartate Aminotransferase | Hepatocellular injury |
| ALP | Alkaline Phosphatase | Cholestasis |
| BILI | Total Bilirubin | Liver function |
| GGT | Gamma Glutamyl Transferase | Cholestasis/alcohol |
| DBILI | Direct Bilirubin | Conjugated bilirubin |

### Hematology (CBC)

| LBTESTCD | LBTEST | LBSTRESU | Reference Range | LOINC |
|----------|--------|----------|-----------------|-------|
| WBC | White Blood Cell Count | 10^9/L | 4.5-11.0 | 6690-2 |
| RBC | Red Blood Cell Count | 10^12/L | 4.5-5.5 (M), 4.0-5.0 (F) | 789-8 |
| HGB | Hemoglobin | g/L | 135-175 (M), 120-160 (F) | 718-7 |
| HCT | Hematocrit | ratio | 0.40-0.50 (M), 0.36-0.44 (F) | 4544-3 |
| PLAT | Platelet Count | 10^9/L | 150-400 | 777-3 |
| NEUT | Neutrophils | 10^9/L | 2.0-7.5 | 751-8 |
| LYMPH | Lymphocytes | 10^9/L | 1.0-4.0 | 731-0 |
| MONO | Monocytes | 10^9/L | 0.2-0.8 | 742-7 |

---

## Generation Patterns

### Baseline and On-Treatment Pattern

```json
{
  "domain": "LB",
  "generation_pattern": {
    "baseline": "Generate values within normal range (±1 SD)",
    "on_treatment": "Apply drug-specific effects",
    "variability": "Within-subject CV 5-15% depending on analyte"
  },
  "liver_toxicity_pattern": {
    "mild_elevation": "1.5-3x ULN",
    "moderate_elevation": "3-5x ULN",
    "severe_elevation": ">5x ULN"
  }
}
```

### Hy's Law Criteria

```json
{
  "hys_law": {
    "description": "Drug-induced liver injury marker",
    "criteria": {
      "alt_threshold": ">3x ULN",
      "bilirubin_threshold": ">2x ULN",
      "alp_threshold": "<2x ULN",
      "no_other_cause": true
    },
    "significance": "Predictive of severe hepatotoxicity"
  }
}
```

### Normal Value Generation

```json
{
  "normal_distribution": {
    "alt": { "mean": 28, "sd": 12, "min": 7, "max": 56 },
    "ast": { "mean": 25, "sd": 10, "min": 10, "max": 40 },
    "creatinine_male": { "mean": 88, "sd": 15, "min": 62, "max": 115 },
    "creatinine_female": { "mean": 65, "sd": 12, "min": 44, "max": 88 }
  }
}
```

---

## Examples

### Example 1: Generate Baseline Chemistry Panel

**Request:** "Generate baseline chemistry panel for 3 subjects in a hepatic safety study"

**Output:**

```json
{
  "domain": "LB",
  "metadata": {
    "studyid": "HEP-SAFE-001",
    "description": "Baseline Chemistry Panel",
    "n_subjects": 3,
    "n_tests_per_subject": 13
  },
  "records": [
    {
      "STUDYID": "HEP-SAFE-001",
      "DOMAIN": "LB",
      "USUBJID": "HEP-SAFE-001-001-0001",
      "LBSEQ": 1,
      "LBTESTCD": "ALT",
      "LBTEST": "Alanine Aminotransferase",
      "LBCAT": "CHEMISTRY",
      "LBORRES": "32",
      "LBORRESU": "U/L",
      "LBSTRESC": "32",
      "LBSTRESN": 32,
      "LBSTRESU": "U/L",
      "LBSTNRLO": 7,
      "LBSTNRHI": 56,
      "LBNRIND": "NORMAL",
      "LBSPEC": "SERUM",
      "LBBLFL": "Y",
      "LBDTC": "2024-03-01",
      "LBDY": 1,
      "VISITNUM": 2,
      "VISIT": "BASELINE",
      "LBLOINC": "1742-6"
    },
    {
      "STUDYID": "HEP-SAFE-001",
      "DOMAIN": "LB",
      "USUBJID": "HEP-SAFE-001-001-0001",
      "LBSEQ": 2,
      "LBTESTCD": "AST",
      "LBTEST": "Aspartate Aminotransferase",
      "LBCAT": "CHEMISTRY",
      "LBORRES": "28",
      "LBORRESU": "U/L",
      "LBSTRESC": "28",
      "LBSTRESN": 28,
      "LBSTRESU": "U/L",
      "LBSTNRLO": 10,
      "LBSTNRHI": 40,
      "LBNRIND": "NORMAL",
      "LBSPEC": "SERUM",
      "LBBLFL": "Y",
      "LBDTC": "2024-03-01",
      "LBDY": 1,
      "VISITNUM": 2,
      "VISIT": "BASELINE",
      "LBLOINC": "1920-8"
    },
    {
      "STUDYID": "HEP-SAFE-001",
      "DOMAIN": "LB",
      "USUBJID": "HEP-SAFE-001-001-0001",
      "LBSEQ": 3,
      "LBTESTCD": "BILI",
      "LBTEST": "Total Bilirubin",
      "LBCAT": "CHEMISTRY",
      "LBORRES": "12",
      "LBORRESU": "umol/L",
      "LBSTRESC": "12",
      "LBSTRESN": 12,
      "LBSTRESU": "umol/L",
      "LBSTNRLO": 3,
      "LBSTNRHI": 21,
      "LBNRIND": "NORMAL",
      "LBSPEC": "SERUM",
      "LBBLFL": "Y",
      "LBDTC": "2024-03-01",
      "LBDY": 1,
      "VISITNUM": 2,
      "VISIT": "BASELINE",
      "LBLOINC": "1975-2"
    }
  ]
}
```

### Example 2: Drug-Induced Liver Injury Pattern

**Request:** "Generate LB data showing Grade 3 ALT elevation developing over 8 weeks"

**Output:**

```json
{
  "domain": "LB",
  "records": [
    {
      "STUDYID": "DILI-001",
      "DOMAIN": "LB",
      "USUBJID": "DILI-001-002-0015",
      "LBSEQ": 1,
      "LBTESTCD": "ALT",
      "LBTEST": "Alanine Aminotransferase",
      "LBORRES": "28",
      "LBSTRESN": 28,
      "LBSTRESU": "U/L",
      "LBSTNRHI": 56,
      "LBNRIND": "NORMAL",
      "LBBLFL": "Y",
      "LBDY": 1,
      "VISIT": "BASELINE"
    },
    {
      "STUDYID": "DILI-001",
      "DOMAIN": "LB",
      "USUBJID": "DILI-001-002-0015",
      "LBSEQ": 5,
      "LBTESTCD": "ALT",
      "LBTEST": "Alanine Aminotransferase",
      "LBORRES": "78",
      "LBSTRESN": 78,
      "LBSTRESU": "U/L",
      "LBSTNRHI": 56,
      "LBNRIND": "HIGH",
      "LBDY": 15,
      "VISIT": "WEEK 2"
    },
    {
      "STUDYID": "DILI-001",
      "DOMAIN": "LB",
      "USUBJID": "DILI-001-002-0015",
      "LBSEQ": 9,
      "LBTESTCD": "ALT",
      "LBTEST": "Alanine Aminotransferase",
      "LBORRES": "142",
      "LBSTRESN": 142,
      "LBSTRESU": "U/L",
      "LBSTNRHI": 56,
      "LBNRIND": "HIGH",
      "LBDY": 29,
      "VISIT": "WEEK 4"
    },
    {
      "STUDYID": "DILI-001",
      "DOMAIN": "LB",
      "USUBJID": "DILI-001-002-0015",
      "LBSEQ": 13,
      "LBTESTCD": "ALT",
      "LBTEST": "Alanine Aminotransferase",
      "LBORRES": "298",
      "LBSTRESN": 298,
      "LBSTRESU": "U/L",
      "LBSTNRHI": 56,
      "LBNRIND": "HIGH",
      "LBDY": 57,
      "VISIT": "WEEK 8"
    }
  ],
  "toxicity_assessment": {
    "baseline_alt": 28,
    "peak_alt": 298,
    "uln": 56,
    "fold_uln": 5.3,
    "ctcae_grade": 3,
    "ctcae_criteria": "Grade 3: >5-20x ULN"
  }
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| LBSEQ | Unique positive integer per subject | 1, 2, 3 |
| LBTESTCD | From CDISC LB codelist | ALT, AST, CREAT |
| LBORRES | Numeric or character result | "32", "<1.0" |
| LBSTRESN | Numeric, null if non-numeric result | 32 |
| LBSTRESU | SI units standard | U/L, mmol/L |
| LBSTNRLO/HI | Numeric reference range | 7, 56 |
| LBNRIND | Derived from value vs range | NORMAL, HIGH, LOW |
| LBSPEC | Specimen type | SERUM, PLASMA |
| LBDTC | ISO 8601 format | 2024-03-15 |
| LBLOINC | Valid LOINC code | 1742-6 |

### Business Rules

- **Reference Range Indicator**: 
  - LBNRIND = "LOW" if LBSTRESN < LBSTNRLO
  - LBNRIND = "HIGH" if LBSTRESN > LBSTNRHI
  - LBNRIND = "NORMAL" otherwise

- **Sex-Specific Ranges**: Apply appropriate ranges for sex-dependent tests (creatinine, hemoglobin)

- **Unit Consistency**: LBSTRESU must be consistent within LBTESTCD across all records

- **Baseline Flag**: Only one LBBLFL = "Y" per subject per LBTESTCD

- **Physiological Plausibility**: Values must be within biologically possible ranges

- **Toxicity Grading**: CTCAE grades based on fold-change from ULN for liver tests

---

## Related Skills

### TrialSim Domains
- [README.md](README.md) - Domain overview
- [demographics-dm.md](demographics-dm.md) - Subject identifiers (USUBJID source)
- [adverse-events-ae.md](adverse-events-ae.md) - Lab abnormalities may trigger AEs
- [vital-signs-vs.md](vital-signs-vs.md) - Complementary safety data

### TrialSim Core
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Safety monitoring concepts
- [../therapeutic-areas/oncology.md](../therapeutic-areas/oncology.md) - Oncology-specific labs

### Cross-Product: PatientSim
- [../../patientsim/SKILL.md](../../patientsim/SKILL.md) - Lab result generation

> **Integration Pattern:** PatientSim lab results can be transformed to LB domain by:
> 1. Adding sequence numbers (LBSEQ)
> 2. Mapping to CDISC test codes (LBTESTCD)
> 3. Adding LOINC codes (LBLOINC)
> 4. Standardizing to SI units (LBSTRESU)
> 5. Adding reference ranges (LBSTNRLO, LBSTNRHI)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial LB domain skill with LOINC coding |
