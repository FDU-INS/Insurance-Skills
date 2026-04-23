---
name: medical-history-mh
description: |
  Generate SDTM MH (Medical History) domain data for pre-existing conditions,
  surgical history, and baseline medical status. Essential for eligibility 
  verification and baseline characterization. Triggers: "medical history", 
  "MH domain", "pre-existing conditions", "past medical history", "PMH",
  "comorbidities", "baseline conditions".
---

# Medical History (MH) Domain

The Medical History domain captures a subject's pre-existing conditions, prior surgeries, and relevant medical events that occurred before or at the start of the study. MH is an **Events class** domain essential for eligibility assessment and baseline characterization.

---

## For Claude

This is a **core SDTM domain skill** for generating subject medical history. MH records document conditions that existed prior to study entry and may influence eligibility, safety, or efficacy analysis.

**Always apply this skill when you see:**
- Requests for subject medical history data
- Pre-existing or baseline conditions
- Comorbidity documentation
- Prior surgical history
- Eligibility criteria verification data
- Historical conditions for inclusion/exclusion assessment

**Key responsibilities:**
- Generate medical history records with MedDRA coding
- Distinguish current vs. resolved conditions
- Track condition onset and resolution timing
- Link to inclusion/exclusion criteria assessment
- Apply CDISC controlled terminology

---

## SDTM Variables

### Required Variables

| Variable | Label | Type | Length | Description |
|----------|-------|------|--------|-------------|
| STUDYID | Study Identifier | Char | 20 | Unique study ID |
| DOMAIN | Domain Abbreviation | Char | 2 | "MH" |
| USUBJID | Unique Subject ID | Char | 40 | From DM domain |
| MHSEQ | Sequence Number | Num | 8 | Unique within subject |
| MHTERM | Reported Term | Char | 200 | Condition as reported |
| MHDECOD | Dictionary-Derived Term | Char | 200 | MedDRA Preferred Term |
| MHCAT | Category | Char | 40 | General category |

### Expected Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| MHBODSYS | Body System or Organ Class | Char | MedDRA System Organ Class |
| MHSTDTC | Start Date/Time | Char | Condition onset date |
| MHENDTC | End Date/Time | Char | Condition resolution date |
| MHPRESP | Pre-Specified | Char | Y if pre-specified on CRF |
| MHOCCUR | Occurrence | Char | Y/N for pre-specified items |

### Permissible Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| MHSCAT | Subcategory | Char | Subcategorization |
| MHENRF | End Relative to Reference | Char | BEFORE, DURING, AFTER |
| MHPTCD | MedDRA PT Code | Num | Numeric PT code |
| MHSOC | Primary SOC Name | Char | MedDRA SOC |
| MHSOCCD | Primary SOC Code | Num | Numeric SOC code |
| MHLLT | MedDRA LLT | Char | Lowest Level Term |
| MHHLT | MedDRA HLT | Char | High Level Term |
| MHHLGT | MedDRA HLGT | Char | High Level Group Term |

---

## MedDRA Coding

Medical history conditions are coded using MedDRA hierarchy:

### Hierarchy Levels

| Level | Abbreviation | Description | Example |
|-------|--------------|-------------|---------|
| System Organ Class | SOC | Highest level | Cardiac disorders |
| High Level Group Term | HLGT | Broad grouping | Coronary artery disorders |
| High Level Term | HLT | Specific grouping | Ischaemic coronary artery disorders |
| Preferred Term | PT | Standard term | Myocardial infarction |
| Lowest Level Term | LLT | Verbatim mapping | Heart attack |

### Common Medical History SOCs

| SOC | Common Conditions |
|-----|-------------------|
| Cardiac disorders | Hypertension, atrial fibrillation, MI, heart failure |
| Endocrine disorders | Diabetes mellitus, hypothyroidism, hyperthyroidism |
| Metabolism and nutrition disorders | Hyperlipidemia, obesity, vitamin deficiency |
| Musculoskeletal disorders | Osteoarthritis, rheumatoid arthritis, osteoporosis |
| Psychiatric disorders | Depression, anxiety, insomnia |
| Respiratory disorders | Asthma, COPD, sleep apnea |
| Nervous system disorders | Migraine, neuropathy, stroke |
| Gastrointestinal disorders | GERD, peptic ulcer, IBS |
| Renal and urinary disorders | Chronic kidney disease, nephrolithiasis |

---

## Generation Patterns

### Therapeutic Area-Specific

Generate conditions relevant to the indication being studied:

```json
{
  "domain": "MH",
  "therapeutic_area": "cardiovascular",
  "required_conditions": ["Hypertension", "Hyperlipidemia"],
  "common_comorbidities": ["Type 2 diabetes mellitus", "Obesity", "Atrial fibrillation"],
  "exclusionary_history": ["Recent MI within 6 months", "Stroke within 12 months"]
}
```

### Oncology Baseline

For cancer trials requiring tumor history:

```json
{
  "domain": "MH",
  "therapeutic_area": "oncology",
  "primary_diagnosis": {
    "term": "Non-small cell lung cancer",
    "stage": "Stage IIIB",
    "histology": "Adenocarcinoma"
  },
  "prior_treatments": ["Platinum-based chemotherapy", "Radiation therapy"],
  "comorbidities": ["COPD", "Hypertension"]
}
```

### Pre-Specified CRF Collection

When specific conditions are prompted on CRF:

```json
{
  "domain": "MH",
  "pattern": "prespecified",
  "conditions": [
    { "term": "Hypertension", "presp": "Y", "collect_if_absent": true },
    { "term": "Diabetes mellitus", "presp": "Y", "collect_if_absent": true },
    { "term": "Hyperlipidemia", "presp": "Y", "collect_if_absent": true },
    { "term": "Coronary artery disease", "presp": "Y", "collect_if_absent": true }
  ]
}
```

---

## Examples

### Example 1: Cardiovascular Trial Medical History

**Request:** "Generate MH domain for a heart failure patient with typical comorbidities for a Phase 3 HF trial"

**Output:**

```json
{
  "domain": "MH",
  "metadata": {
    "studyid": "HF-PH3-001",
    "usubjid": "HF-PH3-001-005-0234",
    "condition_count": 6
  },
  "records": [
    {
      "STUDYID": "HF-PH3-001",
      "DOMAIN": "MH",
      "USUBJID": "HF-PH3-001-005-0234",
      "MHSEQ": 1,
      "MHTERM": "HEART FAILURE WITH REDUCED EJECTION FRACTION",
      "MHDECOD": "Cardiac failure",
      "MHCAT": "PRIMARY DIAGNOSIS",
      "MHBODSYS": "Cardiac disorders",
      "MHSTDTC": "2021-06",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    },
    {
      "STUDYID": "HF-PH3-001",
      "DOMAIN": "MH",
      "USUBJID": "HF-PH3-001-005-0234",
      "MHSEQ": 2,
      "MHTERM": "ESSENTIAL HYPERTENSION",
      "MHDECOD": "Hypertension",
      "MHCAT": "CARDIOVASCULAR",
      "MHBODSYS": "Vascular disorders",
      "MHSTDTC": "2015-03",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    },
    {
      "STUDYID": "HF-PH3-001",
      "DOMAIN": "MH",
      "USUBJID": "HF-PH3-001-005-0234",
      "MHSEQ": 3,
      "MHTERM": "TYPE 2 DIABETES MELLITUS",
      "MHDECOD": "Type 2 diabetes mellitus",
      "MHCAT": "METABOLIC",
      "MHBODSYS": "Metabolism and nutrition disorders",
      "MHSTDTC": "2018-09",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    },
    {
      "STUDYID": "HF-PH3-001",
      "DOMAIN": "MH",
      "USUBJID": "HF-PH3-001-005-0234",
      "MHSEQ": 4,
      "MHTERM": "HYPERLIPIDEMIA",
      "MHDECOD": "Hyperlipidaemia",
      "MHCAT": "METABOLIC",
      "MHBODSYS": "Metabolism and nutrition disorders",
      "MHSTDTC": "2016-01",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    },
    {
      "STUDYID": "HF-PH3-001",
      "DOMAIN": "MH",
      "USUBJID": "HF-PH3-001-005-0234",
      "MHSEQ": 5,
      "MHTERM": "ATRIAL FIBRILLATION",
      "MHDECOD": "Atrial fibrillation",
      "MHCAT": "CARDIOVASCULAR",
      "MHBODSYS": "Cardiac disorders",
      "MHSTDTC": "2022-02",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    },
    {
      "STUDYID": "HF-PH3-001",
      "DOMAIN": "MH",
      "USUBJID": "HF-PH3-001-005-0234",
      "MHSEQ": 6,
      "MHTERM": "CHRONIC KIDNEY DISEASE STAGE 3",
      "MHDECOD": "Chronic kidney disease",
      "MHCAT": "RENAL",
      "MHBODSYS": "Renal and urinary disorders",
      "MHSTDTC": "2020-11",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    }
  ],
  "summary": {
    "by_category": {
      "PRIMARY DIAGNOSIS": 1,
      "CARDIOVASCULAR": 2,
      "METABOLIC": 2,
      "RENAL": 1
    }
  }
}
```

### Example 2: Oncology Prior Cancer History

**Request:** "Generate MH for an NSCLC patient with prior chemotherapy and relevant surgical history"

**Output:**

```json
{
  "domain": "MH",
  "metadata": {
    "studyid": "LUNG-IO-001",
    "usubjid": "LUNG-IO-001-012-0089",
    "condition_count": 5
  },
  "records": [
    {
      "STUDYID": "LUNG-IO-001",
      "DOMAIN": "MH",
      "USUBJID": "LUNG-IO-001-012-0089",
      "MHSEQ": 1,
      "MHTERM": "NON-SMALL CELL LUNG CANCER STAGE IIIB ADENOCARCINOMA",
      "MHDECOD": "Non-small cell lung cancer",
      "MHCAT": "PRIMARY DIAGNOSIS",
      "MHSCAT": "PRIMARY TUMOR",
      "MHBODSYS": "Neoplasms benign, malignant and unspecified",
      "MHSTDTC": "2023-03",
      "MHENRF": "BEFORE"
    },
    {
      "STUDYID": "LUNG-IO-001",
      "DOMAIN": "MH",
      "USUBJID": "LUNG-IO-001-012-0089",
      "MHSEQ": 2,
      "MHTERM": "PRIOR CARBOPLATIN/PEMETREXED CHEMOTHERAPY",
      "MHDECOD": "Chemotherapy",
      "MHCAT": "PRIOR CANCER THERAPY",
      "MHSCAT": "SYSTEMIC THERAPY",
      "MHBODSYS": "Surgical and medical procedures",
      "MHSTDTC": "2023-05",
      "MHENDTC": "2023-09",
      "MHENRF": "BEFORE"
    },
    {
      "STUDYID": "LUNG-IO-001",
      "DOMAIN": "MH",
      "USUBJID": "LUNG-IO-001-012-0089",
      "MHSEQ": 3,
      "MHTERM": "PRIOR RADIATION THERAPY TO CHEST",
      "MHDECOD": "Radiation therapy",
      "MHCAT": "PRIOR CANCER THERAPY",
      "MHSCAT": "RADIATION",
      "MHBODSYS": "Surgical and medical procedures",
      "MHSTDTC": "2023-06",
      "MHENDTC": "2023-07",
      "MHENRF": "BEFORE"
    },
    {
      "STUDYID": "LUNG-IO-001",
      "DOMAIN": "MH",
      "USUBJID": "LUNG-IO-001-012-0089",
      "MHSEQ": 4,
      "MHTERM": "COPD",
      "MHDECOD": "Chronic obstructive pulmonary disease",
      "MHCAT": "GENERAL MEDICAL HISTORY",
      "MHBODSYS": "Respiratory, thoracic and mediastinal disorders",
      "MHSTDTC": "2018",
      "MHENRF": "BEFORE"
    },
    {
      "STUDYID": "LUNG-IO-001",
      "DOMAIN": "MH",
      "USUBJID": "LUNG-IO-001-012-0089",
      "MHSEQ": 5,
      "MHTERM": "HYPERTENSION",
      "MHDECOD": "Hypertension",
      "MHCAT": "GENERAL MEDICAL HISTORY",
      "MHBODSYS": "Vascular disorders",
      "MHSTDTC": "2015",
      "MHENRF": "BEFORE"
    }
  ]
}
```

### Example 3: Pre-Specified Medical History with Negatives

**Request:** "Generate MH for a diabetes trial where specific cardiovascular conditions are pre-specified on the CRF, including conditions the patient does NOT have"

**Output:**

```json
{
  "domain": "MH",
  "metadata": {
    "studyid": "DM2-CV-001",
    "usubjid": "DM2-CV-001-008-0156",
    "prespecified_collection": true
  },
  "records": [
    {
      "STUDYID": "DM2-CV-001",
      "DOMAIN": "MH",
      "USUBJID": "DM2-CV-001-008-0156",
      "MHSEQ": 1,
      "MHTERM": "TYPE 2 DIABETES MELLITUS",
      "MHDECOD": "Type 2 diabetes mellitus",
      "MHCAT": "PRIMARY INDICATION",
      "MHBODSYS": "Metabolism and nutrition disorders",
      "MHSTDTC": "2019-04",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    },
    {
      "STUDYID": "DM2-CV-001",
      "DOMAIN": "MH",
      "USUBJID": "DM2-CV-001-008-0156",
      "MHSEQ": 2,
      "MHTERM": "HYPERTENSION",
      "MHDECOD": "Hypertension",
      "MHCAT": "CARDIOVASCULAR RISK",
      "MHBODSYS": "Vascular disorders",
      "MHSTDTC": "2017-08",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    },
    {
      "STUDYID": "DM2-CV-001",
      "DOMAIN": "MH",
      "USUBJID": "DM2-CV-001-008-0156",
      "MHSEQ": 3,
      "MHTERM": "MYOCARDIAL INFARCTION",
      "MHDECOD": "Myocardial infarction",
      "MHCAT": "CARDIOVASCULAR RISK",
      "MHBODSYS": "Cardiac disorders",
      "MHPRESP": "Y",
      "MHOCCUR": "N"
    },
    {
      "STUDYID": "DM2-CV-001",
      "DOMAIN": "MH",
      "USUBJID": "DM2-CV-001-008-0156",
      "MHSEQ": 4,
      "MHTERM": "STROKE",
      "MHDECOD": "Cerebrovascular accident",
      "MHCAT": "CARDIOVASCULAR RISK",
      "MHBODSYS": "Nervous system disorders",
      "MHPRESP": "Y",
      "MHOCCUR": "N"
    },
    {
      "STUDYID": "DM2-CV-001",
      "DOMAIN": "MH",
      "USUBJID": "DM2-CV-001-008-0156",
      "MHSEQ": 5,
      "MHTERM": "PERIPHERAL ARTERIAL DISEASE",
      "MHDECOD": "Peripheral arterial occlusive disease",
      "MHCAT": "CARDIOVASCULAR RISK",
      "MHBODSYS": "Vascular disorders",
      "MHPRESP": "Y",
      "MHOCCUR": "N"
    },
    {
      "STUDYID": "DM2-CV-001",
      "DOMAIN": "MH",
      "USUBJID": "DM2-CV-001-008-0156",
      "MHSEQ": 6,
      "MHTERM": "CHRONIC KIDNEY DISEASE",
      "MHDECOD": "Chronic kidney disease",
      "MHCAT": "CARDIOVASCULAR RISK",
      "MHBODSYS": "Renal and urinary disorders",
      "MHSTDTC": "2022-01",
      "MHENRF": "BEFORE",
      "MHPRESP": "Y",
      "MHOCCUR": "Y"
    },
    {
      "STUDYID": "DM2-CV-001",
      "DOMAIN": "MH",
      "USUBJID": "DM2-CV-001-008-0156",
      "MHSEQ": 7,
      "MHTERM": "HYPERLIPIDEMIA",
      "MHDECOD": "Hyperlipidaemia",
      "MHCAT": "METABOLIC",
      "MHBODSYS": "Metabolism and nutrition disorders",
      "MHSTDTC": "2018-06",
      "MHENRF": "BEFORE",
      "MHPRESP": "N",
      "MHOCCUR": "Y"
    }
  ],
  "summary": {
    "prespecified_present": ["TYPE 2 DIABETES MELLITUS", "HYPERTENSION", "CHRONIC KIDNEY DISEASE"],
    "prespecified_absent": ["MYOCARDIAL INFARCTION", "STROKE", "PERIPHERAL ARTERIAL DISEASE"],
    "additional_conditions": ["HYPERLIPIDEMIA"]
  }
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| MHSEQ | Positive integer, unique within USUBJID | 1, 2, 3 |
| MHTERM | Non-empty reported condition | ESSENTIAL HYPERTENSION |
| MHDECOD | MedDRA Preferred Term | Hypertension |
| MHBODSYS | MedDRA System Organ Class | Vascular disorders |
| MHSTDTC | ISO 8601 format (may be partial) | 2018, 2018-06, 2018-06-15 |
| MHENDTC | Must be ≥ MHSTDTC if present | 2023-01 |
| MHPRESP | Y if pre-specified on CRF | Y |
| MHOCCUR | Y/N, required if MHPRESP = Y | Y, N |
| MHENRF | BEFORE, DURING, AFTER, ONGOING | BEFORE |

### Business Rules

- **Pre-Existing Requirement**: All MH records should represent conditions existing before or at study start
- **MHENRF Logic**: 
  - BEFORE = ended before study reference period
  - DURING = ongoing at study reference period
  - AFTER = should not occur in MH (use AE domain instead)
- **Pre-Specified Collection**: When MHPRESP = "Y", MHOCCUR must be populated
- **Partial Dates**: Onset dates may be partial (year only, year-month) for historical conditions
- **MedDRA Mapping**: MHDECOD must be valid MedDRA PT; MHBODSYS must be corresponding SOC
- **Oncology Specifics**: Prior cancer therapies are typically coded as "Surgical and medical procedures" SOC
- **Eligibility Link**: Medical history should support inclusion/exclusion criteria assessment

---

## Related Skills

### TrialSim Domains
- [README.md](README.md) - Domain overview and SDTM basics
- [demographics-dm.md](demographics-dm.md) - Subject identifiers
- [adverse-events-ae.md](adverse-events-ae.md) - New events during study (vs. MH pre-existing)
- [concomitant-meds-cm.md](concomitant-meds-cm.md) - Medications for MH conditions

### TrialSim Core
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Trial design and terminology
- [../recruitment-enrollment.md](../recruitment-enrollment.md) - I/E criteria assessment

### Therapeutic Areas
- [../therapeutic-areas/oncology.md](../therapeutic-areas/oncology.md) - Cancer history patterns
- [../therapeutic-areas/cardiovascular.md](../therapeutic-areas/cardiovascular.md) - CV risk factors
- [../therapeutic-areas/cns.md](../therapeutic-areas/cns.md) - Psychiatric history

### Cross-Product: PatientSim
- [../../patientsim/SKILL.md](../../patientsim/SKILL.md) - Patient condition history

> **Integration Pattern:** MH data correlates with:
> - CM domain for ongoing treatments of chronic conditions
> - AE domain (pre-existing conditions may worsen during study)
> - PatientSim condition history transforms to trial MH format
> - I/E criteria verification from recruitment-enrollment.md

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial MH domain skill |
