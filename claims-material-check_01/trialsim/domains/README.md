# SDTM Domain Skills

Skills for generating CDISC SDTM-compliant domain datasets for clinical trial submissions.

---

## Quick Reference

| Domain | Skill | Class | Description | Triggers |
|--------|-------|-------|-------------|----------|
| **DM** | [demographics-dm.md](demographics-dm.md) | Special Purpose | Subject demographics | "demographics", "DM domain", "subject data" |
| **AE** | [adverse-events-ae.md](adverse-events-ae.md) | Events | Adverse events | "adverse events", "AE domain", "safety data" |
| **CM** | [concomitant-meds-cm.md](concomitant-meds-cm.md) | Interventions | Prior/concomitant meds | "concomitant meds", "CM domain", "prior meds" |
| **LB** | [laboratory-lb.md](laboratory-lb.md) | Findings | Laboratory test results | "lab results", "LB domain", "laboratory" |
| **VS** | [vital-signs-vs.md](vital-signs-vs.md) | Findings | Vital sign measurements | "vital signs", "VS domain", "vitals" |
| **EX** | [exposure-ex.md](exposure-ex.md) | Interventions | Study drug exposure | "exposure", "EX domain", "dosing" |
| **DS** | [disposition-ds.md](disposition-ds.md) | Events | Subject disposition | "disposition", "DS domain", "discontinuation" |
| **MH** | [medical-history-mh.md](medical-history-mh.md) | Events | Medical history | "medical history", "MH domain" |

---

## Implementation Status

| Domain | Status | Notes |
|--------|--------|-------|
| DM | ✅ Complete | Demographics - required for all studies |
| AE | ✅ Complete | Adverse events with MedDRA coding |
| CM | ✅ Complete | Concomitant medications with WHO-DD |
| LB | ✅ Complete | Laboratory with LOINC coding |
| VS | ✅ Complete | Vital signs |
| EX | ✅ Complete | Study drug exposure with dose modifications |
| DS | ✅ Complete | Subject disposition and discontinuation |
| MH | ✅ Complete | Medical history with MedDRA coding |

---

## SDTM General Observation Classes

### Special Purpose Domains
- **DM** - Demographics (one record per subject)
- **SV** - Subject Visits
- **SE** - Subject Elements

### Interventions Class
Study treatments and non-study therapies:
- **EX** - Exposure (study drug)
- **CM** - Concomitant Medications
- **EC** - Exposure as Collected
- **SU** - Substance Use

### Events Class
Occurrences and incidents:
- **AE** - Adverse Events
- **DS** - Disposition
- **MH** - Medical History
- **CE** - Clinical Events

### Findings Class
Observations, measurements, and assessments:
- **LB** - Laboratory Test Results
- **VS** - Vital Signs
- **EG** - ECG Test Results
- **PE** - Physical Examination
- **QS** - Questionnaires

---

## Common SDTM Variables

### Identifier Variables (Required)

| Variable | Label | Description |
|----------|-------|-------------|
| STUDYID | Study Identifier | Unique study identifier |
| DOMAIN | Domain Abbreviation | Two-character domain code |
| USUBJID | Unique Subject ID | Study + Site + Subject (globally unique) |

### Timing Variables

| Variable | Label | Format |
|----------|-------|--------|
| --DTC | Date/Time of Collection | ISO 8601 (YYYY-MM-DDTHH:MM:SS) |
| --DY | Study Day | Relative to RFSTDTC |
| VISITNUM | Visit Number | Numeric |
| VISIT | Visit Name | Character |

### Core Variables by Class

**Interventions:**
- `--TRT` - Treatment name
- `--DECOD` - Standardized term
- `--DOSE` - Dose
- `--DOSU` - Dose units
- `--DOSFRQ` - Dosing frequency

**Events:**
- `--TERM` - Reported term
- `--DECOD` - Dictionary term
- `--BODSYS` - Body system
- `--SEV` - Severity
- `--SER` - Serious flag

**Findings:**
- `--TESTCD` - Test code
- `--TEST` - Test name
- `--ORRES` - Original result
- `--ORRESU` - Original units
- `--STRESC` - Standardized result

---

## Controlled Terminology

SDTM domains use CDISC Controlled Terminology. Key codelists:

| Codelist | Domains | Examples |
|----------|---------|----------|
| SEX | DM | M, F, U |
| RACE | DM | WHITE, BLACK OR AFRICAN AMERICAN, ASIAN |
| ETHNIC | DM | HISPANIC OR LATINO, NOT HISPANIC OR LATINO |
| AEOUT | AE | RECOVERED/RESOLVED, NOT RECOVERED/NOT RESOLVED |
| ACN | AE, CM | DRUG WITHDRAWN, DOSE REDUCED |
| ROUTE | EX, CM | ORAL, INTRAVENOUS, SUBCUTANEOUS |
| UNIT | LB, VS, EX | mg, mL, mmHg, kg |

---

## Related Resources

### TrialSim
- [../SKILL.md](../SKILL.md) - TrialSim master skill
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Domain knowledge
- [../phase3-pivotal.md](../phase3-pivotal.md) - Phase 3 trial patterns

### Formats
- [../../../formats/cdisc-sdtm.md](../../../formats/cdisc-sdtm.md) - SDTM output format

### External References
- [CDISC SDTM IG](https://www.cdisc.org/standards/foundational/sdtm) - Official implementation guide
- [CDISC Controlled Terminology](https://www.cdisc.org/standards/terminology) - Code lists

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2024-12 | Added EX, DS, MH domain skills |
| 1.0 | 2024-12 | Initial domain directory with DM, AE, CM, LB, VS |
