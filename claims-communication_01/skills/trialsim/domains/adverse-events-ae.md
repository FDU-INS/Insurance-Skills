---
name: adverse-events-ae
description: |
  Generate SDTM AE (Adverse Events) domain data with MedDRA coding hierarchy, 
  severity grading, causality assessment, and outcome tracking. Foundation for 
  safety analysis. Triggers: "adverse events", "AE domain", "safety data", 
  "MedDRA", "SAE", "side effects", "toxicity".
---

# Adverse Events (AE) Domain

The Adverse Events domain captures all adverse events experienced by subjects during the clinical trial. AE data is coded using MedDRA (Medical Dictionary for Regulatory Activities) and includes severity, causality, and outcome information essential for safety analysis.

---

## For Claude

This is a **core SDTM domain skill** for generating adverse event data. The AE domain is **critical for safety assessment** and regulatory submissions.

**Always apply this skill when you see:**
- Requests for adverse event or safety data
- References to MedDRA coding or SOC/PT terms
- Side effects, toxicity, or treatment-emergent events
- Serious adverse events (SAE) requirements
- CTCAE grading or severity assessments

**Key responsibilities:**
- Apply correct MedDRA hierarchy (SOC → HLGT → HLT → PT → LLT)
- Generate realistic severity distributions by event type
- Assess causality based on temporal relationship and known drug profile
- Track outcomes and actions taken

---

## SDTM Variables

### Required Variables

| Variable | Label | Type | Description |
|----------|-------|------|-------------|
| STUDYID | Study Identifier | Char | Unique study ID |
| DOMAIN | Domain Abbreviation | Char | "AE" |
| USUBJID | Unique Subject ID | Char | From DM domain |
| AESEQ | Sequence Number | Num | Unique within subject |
| AETERM | Reported Term for AE | Char | Verbatim as reported |
| AEDECOD | Dictionary-Derived Term | Char | MedDRA Preferred Term |

### Expected Variables

| Variable | Label | Type | Controlled Terminology |
|----------|-------|------|------------------------|
| AEBODSYS | Body System or Organ Class | Char | MedDRA SOC |
| AESOC | Primary SOC | Char | MedDRA SOC code |
| AEHLGT | High Level Group Term | Char | MedDRA HLGT |
| AEHLT | High Level Term | Char | MedDRA HLT |
| AELLT | Lowest Level Term | Char | MedDRA LLT |
| AESEV | Severity/Intensity | Char | MILD, MODERATE, SEVERE |
| AESER | Serious Event | Char | Y, N |
| AEACN | Action Taken with Study Treatment | Char | (ACN) |
| AEREL | Causality | Char | (REL) |
| AEOUT | Outcome of AE | Char | (OUT) |
| AESTDTC | Start Date/Time | Char | ISO 8601 |
| AEENDTC | End Date/Time | Char | ISO 8601 |
| AESTDY | Study Day of Start | Num | Relative to RFSTDTC |
| AEENDY | Study Day of End | Num | Relative to RFSTDTC |
| AEENRF | End Relative to Reference Period | Char | BEFORE, DURING, AFTER |

### SAE-Related Variables

| Variable | Label | Description |
|----------|-------|-------------|
| AESCONG | Congenital Anomaly | Y if birth defect |
| AESDISAB | Persist/Signif Disability | Y if disabling |
| AESDTH | Results in Death | Y if fatal |
| AESHOSP | Requires Hospitalization | Y if hospitalized |
| AESLIFE | Life Threatening | Y if life threatening |
| AESMIE | Other Medically Important | Y if significant |

---

## Controlled Terminology

### Severity (AESEV)

| Value | CTCAE Equivalent |
|-------|------------------|
| MILD | Grade 1 |
| MODERATE | Grade 2 |
| SEVERE | Grade 3-4 |

### Action Taken (AEACN) - C66767

| Code | Meaning |
|------|---------|
| DRUG WITHDRAWN | Permanently discontinued |
| DOSE REDUCED | Dose lowered |
| DOSE NOT CHANGED | No change |
| DRUG INTERRUPTED | Temporarily stopped |
| NOT APPLICABLE | N/A |
| UNKNOWN | Unknown |

### Causality (AEREL) - C66768

| Code | Meaning |
|------|---------|
| RELATED | Drug-related |
| NOT RELATED | Not drug-related |
| POSSIBLY RELATED | Possible relationship |
| PROBABLY RELATED | Probable relationship |

### Outcome (AEOUT) - C66769

| Code | Meaning |
|------|---------|
| RECOVERED/RESOLVED | Complete resolution |
| RECOVERING/RESOLVING | Improving |
| NOT RECOVERED/NOT RESOLVED | Ongoing |
| RECOVERED/RESOLVED WITH SEQUELAE | Resolved with lasting effects |
| FATAL | Death |
| UNKNOWN | Unknown |

---

## MedDRA Hierarchy

MedDRA organizes adverse events in a 5-level hierarchy:

```
System Organ Class (SOC)
  └── High Level Group Term (HLGT)
      └── High Level Term (HLT)
          └── Preferred Term (PT) ← AEDECOD
              └── Lowest Level Term (LLT)
```

### Common SOC Categories

| SOC Code | System Organ Class |
|----------|-------------------|
| 10005329 | Blood and lymphatic system disorders |
| 10007541 | Cardiac disorders |
| 10017947 | Gastrointestinal disorders |
| 10018065 | General disorders and administration site conditions |
| 10021428 | Infections and infestations |
| 10022891 | Investigations |
| 10028395 | Musculoskeletal and connective tissue disorders |
| 10029104 | Nervous system disorders |
| 10037175 | Psychiatric disorders |
| 10038738 | Respiratory, thoracic and mediastinal disorders |
| 10040785 | Skin and subcutaneous tissue disorders |
| 10047065 | Vascular disorders |

---

## Generation Patterns

### Common AE Distribution by Drug Class

**Chemotherapy:**
| AE Term | SOC | Incidence | Severity Distribution |
|---------|-----|-----------|----------------------|
| Nausea | Gastrointestinal | 60-70% | Mild 50%, Mod 40%, Sev 10% |
| Fatigue | General disorders | 50-60% | Mild 40%, Mod 45%, Sev 15% |
| Neutropenia | Blood disorders | 40-50% | Mild 20%, Mod 40%, Sev 40% |
| Alopecia | Skin disorders | 40-60% | Mild 80%, Mod 20% |

**Checkpoint Inhibitors:**
| AE Term | SOC | Incidence | Grade 3-4 Rate |
|---------|-----|-----------|----------------|
| Fatigue | General disorders | 20-40% | 2-5% |
| Rash | Skin disorders | 15-25% | 1-3% |
| Diarrhea | Gastrointestinal | 10-20% | 2-4% |
| Hypothyroidism | Endocrine | 5-15% | 1% |
| Pneumonitis | Respiratory | 2-5% | 1-2% |

### Treatment-Emergent AE (TEAE) Definition

An AE is treatment-emergent if:
- Onset is on or after first dose of study drug, OR
- Pre-existing condition worsens after first dose

```json
{
  "teae_criteria": {
    "onset_rule": "AESTDTC >= RFSTDTC from DM",
    "worsening_rule": "Severity increases from baseline"
  }
}
```

---

## Examples

### Example 1: Generate Safety Data for Oncology Trial

**Request:** "Generate AE domain for 50 subjects in a checkpoint inhibitor trial with typical irAE patterns"

**Output:**

```json
{
  "domain": "AE",
  "metadata": {
    "studyid": "IO-TRIAL-001",
    "description": "Adverse Events - Checkpoint Inhibitor Trial",
    "n_subjects_with_ae": 45,
    "n_events": 127
  },
  "records": [
    {
      "STUDYID": "IO-TRIAL-001",
      "DOMAIN": "AE",
      "USUBJID": "IO-TRIAL-001-001-0005",
      "AESEQ": 1,
      "AETERM": "TIREDNESS",
      "AEDECOD": "Fatigue",
      "AEBODSYS": "General disorders and administration site conditions",
      "AESEV": "MILD",
      "AESER": "N",
      "AEACN": "DOSE NOT CHANGED",
      "AEREL": "POSSIBLY RELATED",
      "AEOUT": "NOT RECOVERED/NOT RESOLVED",
      "AESTDTC": "2024-04-10",
      "AEENDTC": null,
      "AESTDY": 15
    },
    {
      "STUDYID": "IO-TRIAL-001",
      "DOMAIN": "AE",
      "USUBJID": "IO-TRIAL-001-001-0005",
      "AESEQ": 2,
      "AETERM": "ITCHY SKIN RASH",
      "AEDECOD": "Rash pruritic",
      "AEBODSYS": "Skin and subcutaneous tissue disorders",
      "AEHLT": "Rashes, eruptions and exanthems NEC",
      "AESEV": "MODERATE",
      "AESER": "N",
      "AEACN": "DRUG INTERRUPTED",
      "AEREL": "RELATED",
      "AEOUT": "RECOVERED/RESOLVED",
      "AESTDTC": "2024-05-02",
      "AEENDTC": "2024-05-18",
      "AESTDY": 37,
      "AEENDY": 53
    },
    {
      "STUDYID": "IO-TRIAL-001",
      "DOMAIN": "AE",
      "USUBJID": "IO-TRIAL-001-002-0012",
      "AESEQ": 1,
      "AETERM": "PNEUMONITIS",
      "AEDECOD": "Pneumonitis",
      "AEBODSYS": "Respiratory, thoracic and mediastinal disorders",
      "AESEV": "SEVERE",
      "AESER": "Y",
      "AESCONG": "N",
      "AESDISAB": "N",
      "AESDTH": "N",
      "AESHOSP": "Y",
      "AESLIFE": "N",
      "AESMIE": "Y",
      "AEACN": "DRUG WITHDRAWN",
      "AEREL": "RELATED",
      "AEOUT": "RECOVERED/RESOLVED WITH SEQUELAE",
      "AESTDTC": "2024-06-15",
      "AEENDTC": "2024-07-20",
      "AESTDY": 75,
      "AEENDY": 110
    }
  ],
  "summary": {
    "teae_by_soc": {
      "General disorders": 42,
      "Skin disorders": 28,
      "Gastrointestinal": 22,
      "Endocrine": 15,
      "Respiratory": 8,
      "Other": 12
    },
    "by_severity": {
      "MILD": 68,
      "MODERATE": 45,
      "SEVERE": 14
    },
    "sae_count": 8,
    "drug_related": 89
  }
}
```

### Example 2: SAE Report with Full MedDRA Coding

**Request:** "Generate a serious adverse event record with complete MedDRA hierarchy"

**Output:**

```json
{
  "domain": "AE",
  "records": [
    {
      "STUDYID": "CARD-HF-001",
      "DOMAIN": "AE",
      "USUBJID": "CARD-HF-001-010-0088",
      "AESEQ": 1,
      "AETERM": "WORSENING HEART FAILURE WITH HOSPITALIZATION",
      "AEDECOD": "Cardiac failure congestive",
      "AEBODSYS": "Cardiac disorders",
      "AESOC": "10007541",
      "AEHLGT": "Cardiac disorder signs and symptoms",
      "AEHLT": "Heart failures NEC",
      "AELLT": "Congestive cardiac failure",
      "AESEV": "SEVERE",
      "AESER": "Y",
      "AESCONG": "N",
      "AESDISAB": "N",
      "AESDTH": "N",
      "AESHOSP": "Y",
      "AESLIFE": "Y",
      "AESMIE": "N",
      "AEACN": "DRUG WITHDRAWN",
      "AEREL": "POSSIBLY RELATED",
      "AEOUT": "RECOVERED/RESOLVED",
      "AESTDTC": "2024-08-22T14:30:00",
      "AEENDTC": "2024-09-05T10:00:00",
      "AESTDY": 142,
      "AEENDY": 156
    }
  ],
  "sae_narrative": "A 72-year-old male with NYHA Class III heart failure presented with acute decompensation on Study Day 142. Patient required hospitalization for IV diuretics and was stabilized after 14 days. Study drug was permanently discontinued. Event resolved without sequelae."
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| AESEQ | Unique positive integer per subject | 1, 2, 3 |
| AETERM | Non-empty verbatim text | "Headache" |
| AEDECOD | Valid MedDRA PT | "Headache" |
| AEBODSYS | Valid MedDRA SOC | "Nervous system disorders" |
| AESEV | From CDISC codelist | MILD, MODERATE, SEVERE |
| AESER | Y or N | Y |
| AESTDTC | ISO 8601, non-null | 2024-04-15 |
| AEENDTC | Null or ≥ AESTDTC | 2024-04-20 |
| AEREL | From CDISC codelist | RELATED |
| SAE flags | If AESER=Y, at least one flag = Y | AESHOSP = Y |

### Business Rules

- **Sequence Numbering**: AESEQ must be unique within each USUBJID, starting at 1
- **Timing Consistency**: AESTDTC must be on or after consent date (RFICDTC from DM)
- **SAE Completeness**: If AESER = "Y", at least one SAE criterion must be "Y"
- **Outcome Logic**: AEOUT = "FATAL" implies AESDTH = "Y"
- **MedDRA Consistency**: AEDECOD must be a valid PT under the specified SOC
- **Causality for Related**: If AEREL indicates relationship, document temporal/biologic plausibility
- **Action Consistency**: Severe events often require AEACN other than "DOSE NOT CHANGED"

---

## Related Skills

### TrialSim Domains
- [README.md](README.md) - Domain overview
- [demographics-dm.md](demographics-dm.md) - Subject identifiers (USUBJID source)
- [concomitant-meds-cm.md](concomitant-meds-cm.md) - Rescue medications for AEs
- [exposure-ex.md](exposure-ex.md) - Dose modifications due to AEs

### TrialSim Core
- [../clinical-trials-domain.md](../clinical-trials-domain.md) - Safety monitoring concepts
- [../therapeutic-areas/oncology.md](../therapeutic-areas/oncology.md) - Cancer-specific AE patterns

### Cross-Product: PatientSim
- [../../patientsim/SKILL.md](../../patientsim/SKILL.md) - Clinical event patterns

> **Integration Pattern:** PatientSim adverse drug reactions can be transformed to AE domain by:
> 1. Adding trial identifiers (STUDYID, AESEQ)
> 2. Applying MedDRA coding to reported terms
> 3. Adding trial-specific causality assessment
> 4. Formatting dates to ISO 8601

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial AE domain skill with MedDRA patterns |
