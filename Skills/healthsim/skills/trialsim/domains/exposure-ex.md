---
name: exposure-ex
description: |
  Generate SDTM EX (Exposure) domain data for study drug administration records,
  including dosing, interruptions, modifications, and cumulative exposure. Essential
  for efficacy and safety analysis. Triggers: "exposure", "EX domain", "dosing",
  "drug administration", "dose modifications", "treatment exposure".
---

# Exposure (EX) Domain

The Exposure domain captures details of study drug administration including actual doses given, timing, route, and any modifications. EX is an **Interventions class** domain essential for understanding drug exposure in relation to safety and efficacy endpoints.

---

## For Claude

This is a **core SDTM domain skill** for generating study treatment exposure data. EX records document what drug the subject actually received, not what was planned.

**Always apply this skill when you see:**
- Requests for study drug exposure records
- Dosing history or administration data
- Dose modifications, interruptions, or discontinuations
- Treatment compliance analysis data
- References to cumulative drug exposure

**Key responsibilities:**
- Generate exposure records per administration event or summary period
- Track dose modifications with reasons
- Calculate cumulative exposure
- Link to disposition events for treatment discontinuation
- Apply CDISC controlled terminology for route, frequency, units

---

## SDTM Variables

### Required Variables

| Variable | Label | Type | Length | Description |
|----------|-------|------|--------|-------------|
| STUDYID | Study Identifier | Char | 20 | Unique study ID |
| DOMAIN | Domain Abbreviation | Char | 2 | "EX" |
| USUBJID | Unique Subject ID | Char | 40 | From DM domain |
| EXSEQ | Sequence Number | Num | 8 | Unique within subject |
| EXTRT | Name of Treatment | Char | 200 | Standardized drug name |
| EXDOSE | Dose | Num | 8 | Numeric dose value |
| EXDOSU | Dose Units | Char | 40 | mg, mcg, mL, etc. |
| EXDOSFRM | Dose Form | Char | 40 | TABLET, CAPSULE, INJECTION |
| EXROUTE | Route of Administration | Char | 40 | ORAL, INTRAVENOUS, SUBCUTANEOUS |
| EXSTDTC | Start Date/Time | Char | 19 | ISO 8601 format |
| EXENDTC | End Date/Time | Char | 19 | ISO 8601 format |

### Expected Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| EXDOSFRQ | Dosing Frequency | Char | QD, BID, TID, ONCE, etc. |
| EXLOT | Lot Number | Char | Drug lot/batch number |
| EPOCH | Epoch | Char | TREATMENT, FOLLOW-UP |
| VISITNUM | Visit Number | Num | Numeric visit identifier |
| VISIT | Visit Name | Char | Visit description |
| EXADJ | Reason for Dose Adjustment | Char | Reason for modification |
| EXCAT | Category of Treatment | Char | Categorization |
| EXSCAT | Subcategory | Char | Subcategorization |

### Permissible Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| EXTPT | Planned Time Point | Char | Time point description |
| EXDY | Study Day of Start | Num | Relative to RFSTDTC |
| EXENDY | Study Day of End | Num | Relative to RFSTDTC |
| EXDUR | Duration | Char | ISO 8601 duration (P7D) |

---

## Controlled Terminology

### ROUTE (C66729)

| Code | Decode |
|------|--------|
| ORAL | ORAL |
| INTRAVENOUS | INTRAVENOUS |
| SUBCUTANEOUS | SUBCUTANEOUS |
| INTRAMUSCULAR | INTRAMUSCULAR |
| TOPICAL | TOPICAL |
| INHALATION | INHALATION |
| TRANSDERMAL | TRANSDERMAL |

### DOSFRQ (C71113)

| Code | Description |
|------|-------------|
| QD | Once daily |
| BID | Twice daily |
| TID | Three times daily |
| QID | Four times daily |
| QW | Once weekly |
| Q2W | Every 2 weeks |
| Q3W | Every 3 weeks |
| Q4W | Every 4 weeks |
| ONCE | Single administration |

### UNIT (C71620)

| Code | Use |
|------|-----|
| mg | Milligrams |
| mcg | Micrograms |
| g | Grams |
| mL | Milliliters |
| mg/kg | Weight-based |
| mg/m2 | BSA-based |
| IU | International units |

### DOSFRM (C66726)

| Code |
|------|
| TABLET |
| CAPSULE |
| INJECTION |
| SOLUTION |
| POWDER FOR INJECTION |
| FILM-COATED TABLET |
| CREAM |
| PATCH |

---

## Generation Patterns

### Daily Oral Treatment

For chronic conditions with daily dosing:

```json
{
  "domain": "EX",
  "pattern": "daily_oral",
  "treatment": {
    "extrt": "METFORMIN",
    "exdose": 1000,
    "exdosu": "mg",
    "exdosfrq": "BID",
    "exdosfrm": "TABLET",
    "exroute": "ORAL"
  },
  "recording": "per_visit_summary"
}
```

### Infusion Cycles (Oncology)

For IV chemotherapy or immunotherapy:

```json
{
  "domain": "EX",
  "pattern": "infusion_cycle",
  "treatment": {
    "extrt": "PEMBROLIZUMAB",
    "exdose": 200,
    "exdosu": "mg",
    "exdosfrq": "Q3W",
    "exdosfrm": "INJECTION",
    "exroute": "INTRAVENOUS"
  },
  "cycles": 8,
  "recording": "per_administration"
}
```

### Weight-Based Dosing

For biologics or pediatric studies:

```json
{
  "domain": "EX",
  "pattern": "weight_based",
  "treatment": {
    "extrt": "ADALIMUMAB",
    "exdose": 40,
    "exdosu": "mg",
    "exdosfrq": "Q2W",
    "exdosfrm": "INJECTION",
    "exroute": "SUBCUTANEOUS"
  },
  "dose_calculation": "fixed"
}
```

---

## Examples

### Example 1: Oncology IV Infusion Records

**Request:** "Generate EX domain for a subject receiving 6 cycles of pembrolizumab 200mg Q3W with a dose delay at cycle 4 due to AE"

**Output:**

```json
{
  "domain": "EX",
  "metadata": {
    "studyid": "ONC-IO-001",
    "usubjid": "ONC-IO-001-001-0015",
    "treatment": "PEMBROLIZUMAB"
  },
  "records": [
    {
      "STUDYID": "ONC-IO-001",
      "DOMAIN": "EX",
      "USUBJID": "ONC-IO-001-001-0015",
      "EXSEQ": 1,
      "EXTRT": "PEMBROLIZUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 200,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q3W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "INTRAVENOUS",
      "EXSTDTC": "2024-01-15T09:30:00",
      "EXENDTC": "2024-01-15T10:00:00",
      "EXDY": 1,
      "VISITNUM": 2,
      "VISIT": "CYCLE 1 DAY 1",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "ONC-IO-001",
      "DOMAIN": "EX",
      "USUBJID": "ONC-IO-001-001-0015",
      "EXSEQ": 2,
      "EXTRT": "PEMBROLIZUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 200,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q3W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "INTRAVENOUS",
      "EXSTDTC": "2024-02-05T10:15:00",
      "EXENDTC": "2024-02-05T10:45:00",
      "EXDY": 22,
      "VISITNUM": 3,
      "VISIT": "CYCLE 2 DAY 1",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "ONC-IO-001",
      "DOMAIN": "EX",
      "USUBJID": "ONC-IO-001-001-0015",
      "EXSEQ": 3,
      "EXTRT": "PEMBROLIZUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 200,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q3W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "INTRAVENOUS",
      "EXSTDTC": "2024-02-26T09:00:00",
      "EXENDTC": "2024-02-26T09:30:00",
      "EXDY": 43,
      "VISITNUM": 4,
      "VISIT": "CYCLE 3 DAY 1",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "ONC-IO-001",
      "DOMAIN": "EX",
      "USUBJID": "ONC-IO-001-001-0015",
      "EXSEQ": 4,
      "EXTRT": "PEMBROLIZUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 200,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q3W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "INTRAVENOUS",
      "EXSTDTC": "2024-03-25T14:00:00",
      "EXENDTC": "2024-03-25T14:30:00",
      "EXDY": 71,
      "EXADJ": "DOSE DELAYED DUE TO ADVERSE EVENT",
      "VISITNUM": 5,
      "VISIT": "CYCLE 4 DAY 1",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "ONC-IO-001",
      "DOMAIN": "EX",
      "USUBJID": "ONC-IO-001-001-0015",
      "EXSEQ": 5,
      "EXTRT": "PEMBROLIZUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 200,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q3W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "INTRAVENOUS",
      "EXSTDTC": "2024-04-15T10:30:00",
      "EXENDTC": "2024-04-15T11:00:00",
      "EXDY": 92,
      "VISITNUM": 6,
      "VISIT": "CYCLE 5 DAY 1",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "ONC-IO-001",
      "DOMAIN": "EX",
      "USUBJID": "ONC-IO-001-001-0015",
      "EXSEQ": 6,
      "EXTRT": "PEMBROLIZUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 200,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q3W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "INTRAVENOUS",
      "EXSTDTC": "2024-05-06T09:45:00",
      "EXENDTC": "2024-05-06T10:15:00",
      "EXDY": 113,
      "VISITNUM": 7,
      "VISIT": "CYCLE 6 DAY 1",
      "EPOCH": "TREATMENT"
    }
  ],
  "summary": {
    "total_doses": 6,
    "cumulative_dose_mg": 1200,
    "dose_modifications": 1,
    "treatment_duration_days": 112
  }
}
```

### Example 2: Oral Daily Medication with Dose Reduction

**Request:** "Generate EX for a diabetes patient on metformin 1000mg BID with a dose reduction to 500mg BID at week 4 due to GI intolerance"

**Output:**

```json
{
  "domain": "EX",
  "metadata": {
    "studyid": "DM2-ORAL-001",
    "usubjid": "DM2-ORAL-001-003-0042",
    "treatment": "METFORMIN"
  },
  "records": [
    {
      "STUDYID": "DM2-ORAL-001",
      "DOMAIN": "EX",
      "USUBJID": "DM2-ORAL-001-003-0042",
      "EXSEQ": 1,
      "EXTRT": "METFORMIN",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 1000,
      "EXDOSU": "mg",
      "EXDOSFRQ": "BID",
      "EXDOSFRM": "TABLET",
      "EXROUTE": "ORAL",
      "EXSTDTC": "2024-03-01",
      "EXENDTC": "2024-03-28",
      "EXDY": 1,
      "EXENDY": 28,
      "VISITNUM": 2,
      "VISIT": "WEEK 1",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "DM2-ORAL-001",
      "DOMAIN": "EX",
      "USUBJID": "DM2-ORAL-001-003-0042",
      "EXSEQ": 2,
      "EXTRT": "METFORMIN",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 500,
      "EXDOSU": "mg",
      "EXDOSFRQ": "BID",
      "EXDOSFRM": "TABLET",
      "EXROUTE": "ORAL",
      "EXSTDTC": "2024-03-29",
      "EXENDTC": "2024-05-24",
      "EXDY": 29,
      "EXENDY": 85,
      "EXADJ": "DOSE REDUCED DUE TO GASTROINTESTINAL INTOLERANCE",
      "VISITNUM": 5,
      "VISIT": "WEEK 4",
      "EPOCH": "TREATMENT"
    }
  ],
  "summary": {
    "initial_dose_mg": 1000,
    "final_dose_mg": 500,
    "dose_reductions": 1,
    "treatment_duration_days": 85
  }
}
```

### Example 3: Subcutaneous Biologic with Missing Dose

**Request:** "Generate EX for a patient on adalimumab 40mg Q2W for 12 weeks who missed one dose"

**Output:**

```json
{
  "domain": "EX",
  "metadata": {
    "studyid": "RA-BIO-001",
    "usubjid": "RA-BIO-001-005-0088",
    "treatment": "ADALIMUMAB"
  },
  "records": [
    {
      "STUDYID": "RA-BIO-001",
      "DOMAIN": "EX",
      "USUBJID": "RA-BIO-001-005-0088",
      "EXSEQ": 1,
      "EXTRT": "ADALIMUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 40,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q2W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "SUBCUTANEOUS",
      "EXSTDTC": "2024-04-01",
      "EXENDTC": "2024-04-01",
      "EXDY": 1,
      "VISITNUM": 2,
      "VISIT": "WEEK 1",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "RA-BIO-001",
      "DOMAIN": "EX",
      "USUBJID": "RA-BIO-001-005-0088",
      "EXSEQ": 2,
      "EXTRT": "ADALIMUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 40,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q2W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "SUBCUTANEOUS",
      "EXSTDTC": "2024-04-15",
      "EXENDTC": "2024-04-15",
      "EXDY": 15,
      "VISITNUM": 3,
      "VISIT": "WEEK 3",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "RA-BIO-001",
      "DOMAIN": "EX",
      "USUBJID": "RA-BIO-001-005-0088",
      "EXSEQ": 3,
      "EXTRT": "ADALIMUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 40,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q2W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "SUBCUTANEOUS",
      "EXSTDTC": "2024-05-13",
      "EXENDTC": "2024-05-13",
      "EXDY": 43,
      "EXADJ": "DOSE DELAYED - SUBJECT MISSED WEEK 5 DOSE",
      "VISITNUM": 5,
      "VISIT": "WEEK 7",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "RA-BIO-001",
      "DOMAIN": "EX",
      "USUBJID": "RA-BIO-001-005-0088",
      "EXSEQ": 4,
      "EXTRT": "ADALIMUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 40,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q2W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "SUBCUTANEOUS",
      "EXSTDTC": "2024-05-27",
      "EXENDTC": "2024-05-27",
      "EXDY": 57,
      "VISITNUM": 6,
      "VISIT": "WEEK 9",
      "EPOCH": "TREATMENT"
    },
    {
      "STUDYID": "RA-BIO-001",
      "DOMAIN": "EX",
      "USUBJID": "RA-BIO-001-005-0088",
      "EXSEQ": 5,
      "EXTRT": "ADALIMUMAB",
      "EXCAT": "STUDY DRUG",
      "EXDOSE": 40,
      "EXDOSU": "mg",
      "EXDOSFRQ": "Q2W",
      "EXDOSFRM": "INJECTION",
      "EXROUTE": "SUBCUTANEOUS",
      "EXSTDTC": "2024-06-10",
      "EXENDTC": "2024-06-10",
      "EXDY": 71,
      "VISITNUM": 7,
      "VISIT": "WEEK 11",
      "EPOCH": "TREATMENT"
    }
  ],
  "summary": {
    "planned_doses": 6,
    "actual_doses": 5,
    "missed_doses": 1,
    "cumulative_dose_mg": 200,
    "compliance_pct": 83.3
  }
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| EXSEQ | Positive integer, unique within USUBJID | 1, 2, 3 |
| EXTRT | Non-empty, standardized drug name | PEMBROLIZUMAB |
| EXDOSE | Non-negative numeric (0 for skipped) | 200 |
| EXDOSU | From CDISC UNIT codelist | mg, mcg, mL |
| EXDOSFRQ | From CDISC DOSFRQ codelist | QD, BID, Q3W |
| EXROUTE | From CDISC ROUTE codelist | ORAL, INTRAVENOUS |
| EXSTDTC | ISO 8601 format, ≤ EXENDTC | 2024-01-15 |
| EXDY | Integer, calculated from RFSTDTC | 1, 22, 43 |
| EPOCH | From Trial Epochs | TREATMENT |

### Business Rules

- **Chronological Order**: EXSEQ should follow chronological order of dosing
- **Date Consistency**: EXSTDTC must be ≥ DM.RFSTDTC and ≤ DM.RFENDTC
- **Dose Modifications**: When dose changes, include EXADJ with reason
- **Study Day Calculation**: EXDY = (EXSTDTC - RFSTDTC) + 1 when EXSTDTC ≥ RFSTDTC
- **IV Duration**: For infusions, EXENDTC - EXSTDTC should reflect realistic infusion duration
- **Cumulative Exposure**: Sum of (EXDOSE × doses) should be calculable from records
- **Treatment Gaps**: Missing doses should be documentable through EXADJ or DS domain

---

## Related Skills

### TrialSim Domains
- [README.md](README.md) - Domain overview and SDTM basics
- [demographics-dm.md](demographics-dm.md) - Subject identifiers (USUBJID source)
- [adverse-events-ae.md](adverse-events-ae.md) - AEs often trigger dose modifications
- [disposition-ds.md](disposition-ds.md) - Treatment discontinuation events

### TrialSim Core
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Trial design and terminology
- [../phase3-pivotal.md](../phase3-pivotal.md) - Phase 3 trial exposure patterns

### Therapeutic Areas
- [../therapeutic-areas/oncology.md](../therapeutic-areas/oncology.md) - Chemotherapy dosing cycles
- [../therapeutic-areas/cgt.md](../therapeutic-areas/cgt.md) - CAR-T single administration

> **Integration Pattern:** EX records should correlate with:
> - AE domain for dose modification triggers
> - DS domain for treatment discontinuation
> - CM domain for rescue medications due to toxicity

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial EX domain skill |
