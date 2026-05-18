---
name: concomitant-meds-cm
description: |
  Generate SDTM CM (Concomitant/Prior Medications) domain data with WHO-Drug 
  Dictionary coding, ATC classification, and indication mapping. Triggers: 
  "concomitant medications", "CM domain", "prior meds", "background therapy", 
  "rescue medication", "ATC code".
---

# Concomitant Medications (CM) Domain

The Concomitant/Prior Medications domain captures all non-study medications taken by subjects before and during the trial. CM is an Interventions class domain that uses WHO Drug Dictionary coding and ATC classification.

---

## For Claude

This is an **Interventions class SDTM domain skill** for generating medication data. CM captures the complete medication history for drug interaction analysis and safety assessment.

**Always apply this skill when you see:**
- Requests for concomitant or prior medication data
- Background therapy or maintenance medications
- Rescue medications for adverse events
- Drug-drug interaction analysis needs
- WHO Drug Dictionary or ATC classification

**Key responsibilities:**
- Generate realistic polypharmacy patterns by indication/age
- Apply WHO Drug Dictionary coding
- Classify by ATC therapeutic category
- Track indication and temporal relationship to study

---

## SDTM Variables

### Required Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| STUDYID | Study Identifier | Char | Unique study ID |
| DOMAIN | Domain Abbreviation | Char | "CM" |
| USUBJID | Unique Subject ID | Char | From DM domain |
| CMSEQ | Sequence Number | Num | Unique within subject |
| CMTRT | Reported Name of Drug | Char | Verbatim medication name |
| CMDECOD | Standardized Medication Name | Char | WHO Drug preferred name |

### Expected Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| CMCAT | Category for Medication | Char | PRIOR, CONCOMITANT |
| CMINDC | Indication | Char | Reason for medication |
| CMDOSE | Dose per Administration | Num | Dose amount |
| CMDOSU | Dose Units | Char | mg, mL, etc. |
| CMDOSFRQ | Dosing Frequency | Char | QD, BID, TID, PRN |
| CMROUTE | Route of Administration | Char | ORAL, IV, SC |
| CMSTDTC | Start Date/Time | Char | ISO 8601 |
| CMENDTC | End Date/Time | Char | ISO 8601 |
| CMSTDY | Study Day of Start | Num | Relative to RFSTDTC |
| CMENDY | Study Day of End | Num | Relative to RFSTDTC |
| CMENRF | End Relative to Reference Period | Char | BEFORE, DURING, AFTER |
| CMONGO | Ongoing | Char | Y if still taking |
| CMATC1CD | ATC Level 1 Code | Char | Anatomical main group |
| CMATC2CD | ATC Level 2 Code | Char | Therapeutic subgroup |
| CMATC3CD | ATC Level 3 Code | Char | Pharmacological subgroup |
| CMATC4CD | ATC Level 4 Code | Char | Chemical subgroup |

---

## Controlled Terminology

### Route (CMROUTE) - C66729

| Code | Description |
|------|-------------|
| ORAL | By mouth |
| INTRAVENOUS | Into vein |
| SUBCUTANEOUS | Under skin |
| INTRAMUSCULAR | Into muscle |
| TOPICAL | On skin |
| INHALATION | Into lungs |
| OPHTHALMIC | Into eye |
| TRANSDERMAL | Through skin |

### Frequency (CMDOSFRQ) - C71113

| Code | Description | Times/Day |
|------|-------------|-----------|
| QD | Once daily | 1 |
| BID | Twice daily | 2 |
| TID | Three times daily | 3 |
| QID | Four times daily | 4 |
| Q8H | Every 8 hours | 3 |
| Q12H | Every 12 hours | 2 |
| QW | Once weekly | 0.14 |
| QM | Once monthly | 0.03 |
| PRN | As needed | Variable |

---

## ATC Classification System

The Anatomical Therapeutic Chemical (ATC) system classifies drugs in 5 levels:

| Level | Description | Example |
|-------|-------------|---------|
| 1st | Anatomical main group | A (Alimentary tract) |
| 2nd | Therapeutic subgroup | A10 (Drugs for diabetes) |
| 3rd | Pharmacological subgroup | A10B (Blood glucose lowering) |
| 4th | Chemical subgroup | A10BA (Biguanides) |
| 5th | Chemical substance | A10BA02 (Metformin) |

### Common ATC Groups

| Code | Group | Common Medications |
|------|-------|-------------------|
| A02BC | Proton pump inhibitors | Omeprazole, pantoprazole |
| A10BA | Biguanides | Metformin |
| B01AC | Platelet aggregation inhibitors | Aspirin, clopidogrel |
| C03CA | Sulfonamide diuretics | Furosemide |
| C07AB | Beta blockers, selective | Metoprolol, atenolol |
| C09AA | ACE inhibitors | Lisinopril, enalapril |
| C10AA | HMG CoA reductase inhibitors | Atorvastatin, rosuvastatin |
| J01 | Antibacterials | Various antibiotics |
| M01AE | Propionic acid derivatives | Ibuprofen, naproxen |
| N02BE | Anilides | Acetaminophen |
| N05BA | Benzodiazepine derivatives | Lorazepam, alprazolam |
| N06AB | SSRIs | Sertraline, escitalopram |

---

## Generation Patterns

### Polypharmacy by Age Group

| Age Group | Mean # Meds | Common Categories |
|-----------|-------------|-------------------|
| 18-40 | 1-2 | Contraceptives, NSAIDs, vitamins |
| 41-60 | 3-5 | Antihypertensives, statins, metformin |
| 61-75 | 5-8 | Multiple CV, GI protection, pain |
| 75+ | 7-12 | Polypharmacy, anticoagulants |

### Diabetes Patient Typical Medications

```json
{
  "condition": "Type 2 Diabetes",
  "typical_medications": [
    {
      "cmtrt": "METFORMIN",
      "cmdecod": "Metformin",
      "cmatc4cd": "A10BA",
      "cmdose": 1000,
      "cmdosu": "mg",
      "cmdosfrq": "BID",
      "cmindc": "Type 2 Diabetes Mellitus"
    },
    {
      "cmtrt": "LISINOPRIL",
      "cmdecod": "Lisinopril",
      "cmatc4cd": "C09AA",
      "cmdose": 10,
      "cmdosu": "mg",
      "cmdosfrq": "QD",
      "cmindc": "Hypertension"
    },
    {
      "cmtrt": "ATORVASTATIN",
      "cmdecod": "Atorvastatin",
      "cmatc4cd": "C10AA",
      "cmdose": 40,
      "cmdosu": "mg",
      "cmdosfrq": "QD",
      "cmindc": "Hyperlipidemia"
    },
    {
      "cmtrt": "ASPIRIN",
      "cmdecod": "Acetylsalicylic acid",
      "cmatc4cd": "B01AC",
      "cmdose": 81,
      "cmdosu": "mg",
      "cmdosfrq": "QD",
      "cmindc": "Cardiovascular prophylaxis"
    }
  ]
}
```

### Rescue Medication Pattern

```json
{
  "rescue_medication": {
    "trigger": "Adverse event requiring treatment",
    "timing": "CMSTDTC should be on or after AE onset",
    "indication": "Should reference the AE term",
    "duration": "Typically short-term"
  },
  "example": {
    "ae_term": "Nausea",
    "rescue_med": "Ondansetron",
    "cmatc4cd": "A04AA",
    "relationship": "CMSTDTC = AESTDTC (same day)"
  }
}
```

---

## Examples

### Example 1: Generate Baseline Concomitant Medications

**Request:** "Generate CM domain for a 65-year-old diabetic patient with hypertension entering a cardiovascular trial"

**Output:**

```json
{
  "domain": "CM",
  "metadata": {
    "studyid": "CV-OUTCOMES-001",
    "usubjid": "CV-OUTCOMES-001-005-0042",
    "description": "Baseline Concomitant Medications",
    "n_medications": 6
  },
  "records": [
    {
      "STUDYID": "CV-OUTCOMES-001",
      "DOMAIN": "CM",
      "USUBJID": "CV-OUTCOMES-001-005-0042",
      "CMSEQ": 1,
      "CMTRT": "METFORMIN 1000MG TABLET",
      "CMDECOD": "Metformin",
      "CMCAT": "PRIOR",
      "CMINDC": "Type 2 Diabetes Mellitus",
      "CMDOSE": 1000,
      "CMDOSU": "mg",
      "CMDOSFRQ": "BID",
      "CMROUTE": "ORAL",
      "CMSTDTC": "2020-03-15",
      "CMONGO": "Y",
      "CMENRF": "DURING",
      "CMATC1CD": "A",
      "CMATC2CD": "A10",
      "CMATC3CD": "A10B",
      "CMATC4CD": "A10BA"
    },
    {
      "STUDYID": "CV-OUTCOMES-001",
      "DOMAIN": "CM",
      "USUBJID": "CV-OUTCOMES-001-005-0042",
      "CMSEQ": 2,
      "CMTRT": "LISINOPRIL 20MG TABLET",
      "CMDECOD": "Lisinopril",
      "CMCAT": "PRIOR",
      "CMINDC": "Hypertension",
      "CMDOSE": 20,
      "CMDOSU": "mg",
      "CMDOSFRQ": "QD",
      "CMROUTE": "ORAL",
      "CMSTDTC": "2018-06-01",
      "CMONGO": "Y",
      "CMENRF": "DURING",
      "CMATC1CD": "C",
      "CMATC2CD": "C09",
      "CMATC3CD": "C09A",
      "CMATC4CD": "C09AA"
    },
    {
      "STUDYID": "CV-OUTCOMES-001",
      "DOMAIN": "CM",
      "USUBJID": "CV-OUTCOMES-001-005-0042",
      "CMSEQ": 3,
      "CMTRT": "ATORVASTATIN 40MG TABLET",
      "CMDECOD": "Atorvastatin",
      "CMCAT": "PRIOR",
      "CMINDC": "Hyperlipidemia",
      "CMDOSE": 40,
      "CMDOSU": "mg",
      "CMDOSFRQ": "QD",
      "CMROUTE": "ORAL",
      "CMSTDTC": "2019-01-10",
      "CMONGO": "Y",
      "CMENRF": "DURING",
      "CMATC1CD": "C",
      "CMATC2CD": "C10",
      "CMATC3CD": "C10A",
      "CMATC4CD": "C10AA"
    },
    {
      "STUDYID": "CV-OUTCOMES-001",
      "DOMAIN": "CM",
      "USUBJID": "CV-OUTCOMES-001-005-0042",
      "CMSEQ": 4,
      "CMTRT": "ASPIRIN 81MG TABLET",
      "CMDECOD": "Acetylsalicylic acid",
      "CMCAT": "PRIOR",
      "CMINDC": "Cardiovascular prophylaxis",
      "CMDOSE": 81,
      "CMDOSU": "mg",
      "CMDOSFRQ": "QD",
      "CMROUTE": "ORAL",
      "CMSTDTC": "2018-06-01",
      "CMONGO": "Y",
      "CMENRF": "DURING",
      "CMATC1CD": "B",
      "CMATC2CD": "B01",
      "CMATC3CD": "B01A",
      "CMATC4CD": "B01AC"
    },
    {
      "STUDYID": "CV-OUTCOMES-001",
      "DOMAIN": "CM",
      "USUBJID": "CV-OUTCOMES-001-005-0042",
      "CMSEQ": 5,
      "CMTRT": "OMEPRAZOLE 20MG CAPSULE",
      "CMDECOD": "Omeprazole",
      "CMCAT": "PRIOR",
      "CMINDC": "Gastroesophageal reflux",
      "CMDOSE": 20,
      "CMDOSU": "mg",
      "CMDOSFRQ": "QD",
      "CMROUTE": "ORAL",
      "CMSTDTC": "2021-04-20",
      "CMONGO": "Y",
      "CMENRF": "DURING",
      "CMATC1CD": "A",
      "CMATC2CD": "A02",
      "CMATC3CD": "A02B",
      "CMATC4CD": "A02BC"
    }
  ],
  "summary": {
    "by_atc_level1": {
      "A": 2,
      "B": 1,
      "C": 2
    },
    "ongoing_count": 5
  }
}
```

### Example 2: Rescue Medication for Adverse Event

**Request:** "Generate CM record for ondansetron given to treat chemotherapy-induced nausea"

**Output:**

```json
{
  "domain": "CM",
  "records": [
    {
      "STUDYID": "ONC-CHEMO-001",
      "DOMAIN": "CM",
      "USUBJID": "ONC-CHEMO-001-003-0028",
      "CMSEQ": 8,
      "CMTRT": "ONDANSETRON 8MG IV",
      "CMDECOD": "Ondansetron",
      "CMCAT": "CONCOMITANT",
      "CMSCAT": "RESCUE MEDICATION",
      "CMINDC": "Chemotherapy-induced nausea",
      "CMDOSE": 8,
      "CMDOSU": "mg",
      "CMDOSFRQ": "Q8H",
      "CMROUTE": "INTRAVENOUS",
      "CMSTDTC": "2024-05-15",
      "CMENDTC": "2024-05-17",
      "CMSTDY": 22,
      "CMENDY": 24,
      "CMONGO": "N",
      "CMENRF": "DURING",
      "CMATC1CD": "A",
      "CMATC2CD": "A04",
      "CMATC3CD": "A04A",
      "CMATC4CD": "A04AA"
    }
  ],
  "related_ae": {
    "aeterm": "Nausea",
    "aestdtc": "2024-05-15",
    "relationship": "Rescue medication started same day as AE onset"
  }
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| CMSEQ | Unique positive integer per subject | 1, 2, 3 |
| CMTRT | Non-empty verbatim name | "Metformin 1000mg" |
| CMDECOD | WHO Drug preferred name | "Metformin" |
| CMDOSE | Positive numeric if applicable | 1000 |
| CMDOSU | From CDISC unit codelist | mg, mL |
| CMDOSFRQ | From frequency codelist | QD, BID |
| CMROUTE | From route codelist | ORAL |
| CMSTDTC | ISO 8601, ≤ CMENDTC if present | 2024-03-15 |
| CMONGO | "Y" if ongoing, null otherwise | Y |
| CMENRF | BEFORE, DURING, or AFTER reference period | DURING |

### Business Rules

- **Category Logic**: 
  - CMCAT = "PRIOR" if CMENDTC < RFSTDTC (from DM)
  - CMCAT = "CONCOMITANT" if medication overlaps study period

- **Ongoing Medications**: If CMONGO = "Y", CMENDTC should be null

- **Indication Required**: CMINDC should be populated for meaningful analysis

- **Dose Consistency**: CMDOSE + CMDOSU + CMDOSFRQ should represent complete dosing

- **ATC Hierarchy**: ATC codes must follow proper hierarchy (1→2→3→4)

- **Rescue Medication Timing**: Rescue meds should align temporally with related AEs

---

## Related Skills

### TrialSim Domains
- [README.md](README.md) - Domain overview
- [demographics-dm.md](demographics-dm.md) - Subject identifiers (USUBJID source)
- [adverse-events-ae.md](adverse-events-ae.md) - AEs that trigger rescue meds
- [exposure-ex.md](exposure-ex.md) - Study drug (excluded from CM)

### TrialSim Core
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Protocol medication rules
- [../therapeutic-areas/oncology.md](../therapeutic-areas/oncology.md) - Supportive care patterns

### Cross-Product: RxMemberSim
- [../../rxmembersim/SKILL.md](../../rxmembersim/SKILL.md) - Prescription drug patterns

> **Integration Pattern:** RxMemberSim prescription data can inform CM generation by:
> 1. Using NDC-to-ATC mapping for classification
> 2. Applying realistic polypharmacy patterns by condition
> 3. Generating indication-appropriate medication sets
> 4. Calculating dosing from dispensing records

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial CM domain skill with ATC classification |
