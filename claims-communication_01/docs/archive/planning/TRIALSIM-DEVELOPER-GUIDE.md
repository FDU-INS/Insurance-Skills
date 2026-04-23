# TrialSim Developer Guide

**Version**: 3.0  
**Date**: December 2024  
**Status**: Active Development (Phase 2 Complete)  
**Purpose**: Comprehensive guide for TrialSim clinical trials data generation

---

## Executive Summary

TrialSim generates synthetic clinical trial data for:
- Testing CDISC-compliant systems (SDTM/ADaM)
- Regulatory submission pipeline validation
- Clinical data management system development
- Statistical programming training

### Current State (December 2024)

| Category | Skills | Status |
|----------|--------|--------|
| **Core** | SKILL.md, README, clinical-trials-domain, recruitment-enrollment | ✅ Complete |
| **Trial Phases** | Phase 1, 2, 3 | ✅ Complete |
| **SDTM Domains** | DM, AE, VS, LB, CM, EX, DS, MH | ✅ Complete |
| **Therapeutic Areas** | Oncology, CNS, CV, CGT | ✅ Complete |
| **RWE** | Overview, Synthetic Control | ✅ Complete |
| **Total Skills** | 20 | |

---

## 1. Architecture

### Directory Structure

```
skills/trialsim/
├── SKILL.md                           # Master router
├── README.md                          # Quick reference
├── clinical-trials-domain.md          # Core domain knowledge
├── recruitment-enrollment.md          # Screening funnel
│
├── phase1-dose-escalation.md          # Phase I (3+3, BOIN, CRM)
├── phase2-proof-of-concept.md         # Phase II (Simon's, MCP-Mod)
├── phase3-pivotal.md                  # Phase III registration
│
├── domains/                           # CDISC SDTM Domains
│   ├── README.md
│   ├── demographics-dm.md             # Required for all studies
│   ├── adverse-events-ae.md           # MedDRA coded safety
│   ├── vital-signs-vs.md              # VS measurements
│   ├── laboratory-lb.md               # LOINC coded labs
│   ├── concomitant-meds-cm.md         # WHO Drug/ATC coded
│   ├── exposure-ex.md                 # Study drug dosing
│   ├── disposition-ds.md              # Subject status
│   └── medical-history-mh.md          # Baseline conditions
│
├── therapeutic-areas/                 # Indication-specific
│   ├── README.md
│   ├── oncology.md                    # RECIST, ORR, PFS, OS
│   ├── cns.md                         # Cognitive scales, imaging
│   ├── cardiovascular.md              # MACE, CV outcomes
│   └── cgt.md                         # Cell & gene therapy
│
└── rwe/                               # Real World Evidence
    ├── README.md
    ├── overview.md                    # RWE fundamentals
    └── synthetic-control.md           # External control arms
```

### Key Design Decisions

1. **Flat structure at top level** - Phase skills at root level
2. **Subdirectories for categories** - `domains/`, `therapeutic-areas/`, `rwe/`
3. **YAML frontmatter required** - Every skill has name, description with triggers
4. **Validation rules required** - Table format with business rules

---

## 2. Skill Template

Every TrialSim skill follows this structure:

```markdown
---
name: skill-name
description: |
  Brief description of what this skill generates.
  Triggers: "phrase1", "phrase2", "phrase3"
---

# Skill Title

Brief introduction paragraph.

---

## For Claude

This is a **[type]** skill for generating [what].

**Always apply this skill when you see:**
- Trigger 1
- Trigger 2

**Combine with:**
- [other-skill.md](other-skill.md) - For X
- [format.md](../../formats/format.md) - For Y output

---

## When to Use This Skill

Use this skill when the user:
- Request type 1
- Request type 2

---

## Example Requests → Responses

| User Says | Claude Interprets | Key Features |
|-----------|-------------------|--------------|
| "..." | ... | ... |

---

## Generation Patterns

### Pattern 1
[Domain knowledge and realistic generation guidance]

---

## Complete Examples

### Example 1: [Cohort]

**Prompt:** "..."

**Output:**
```json
{
  // Complete JSON example
}
```

---

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Field | Constraint | Value |

### Business Rules

- **Rule Name**: Description

---

## Related Skills

### TrialSim
- [SKILL.md](SKILL.md) - Overview
- [related.md](related.md) - Related skill

### Cross-Product: PatientSim
- [../patientsim/skill.md](../patientsim/skill.md) - Integration

> **Integration Pattern:** Description of how products work together.
```

---

## 3. CDISC Standards Reference

### SDTM Domain Priority

| Priority | Domain | Purpose | Coding Standard |
|----------|--------|---------|-----------------|
| Critical | DM | Demographics | - |
| Critical | AE | Adverse Events | MedDRA |
| Critical | LB | Laboratory | LOINC |
| High | VS | Vital Signs | - |
| High | CM | Concomitant Meds | WHO Drug/ATC |
| High | EX | Exposure | - |
| High | DS | Disposition | CDISC CT |
| Medium | MH | Medical History | MedDRA |

### Standard Variable Prefixes

| Domain | Prefix | Example Variables |
|--------|--------|-------------------|
| DM | - | USUBJID, SUBJID, SITEID, RFSTDTC |
| AE | AE | AETERM, AEDECOD, AESTDTC, AESER |
| LB | LB | LBTESTCD, LBORRES, LBSTRESN, LBLOINC |
| VS | VS | VSTESTCD, VSORRES, VSSTRESN |
| CM | CM | CMTRT, CMDECOD, CMSTDTC |

### MedDRA Hierarchy (for AE)

```
System Organ Class (SOC)
  └── High Level Group Term (HLGT)
      └── High Level Term (HLT)
          └── Preferred Term (PT)
              └── Lowest Level Term (LLT)
```

---

## 4. Cross-Product Integration

### Identity Correlation

```
Person (common)
  ├── Patient (PatientSim) ─── SSN correlator
  ├── Member (MemberSim) ──── SSN correlator
  ├── RxMember (RxMemberSim) ─ SSN correlator
  └── Subject (TrialSim) ──── USUBJID (internal)
                               └── links to Patient via screening
```

### Integration Patterns

| TrialSim Cohort | PatientSim Source | Key Link |
|-------------------|-------------------|----------|
| Oncology trial subjects | `oncology/*.md` | Diagnosis, staging |
| CV outcomes trial | `heart-failure.md` | Baseline LVEF, NYHA |
| CNS trial subjects | `behavioral-health.md` | Cognitive baseline |
| CGT recipients | Custom generation | Disease confirmation |

> **Integration Pattern:** Use PatientSim for realistic baseline clinical characteristics. TrialSim adds protocol-specific assessments, randomization, and SDTM-formatted data.

---

## 5. Output Formats

| Format | Request Phrase | Use Case |
|--------|----------------|----------|
| JSON | default | Internal processing |
| SDTM | "as SDTM" | FDA submission |
| ADaM | "as ADaM" | Statistical analysis |
| CSV | "as CSV" | Quick review |

### SDTM Output Structure

```json
{
  "domain": "AE",
  "metadata": {
    "study_id": "ONCO-2025-001",
    "sdtm_version": "3.3",
    "created": "2025-12-20"
  },
  "records": [
    {
      "STUDYID": "ONCO-2025-001",
      "DOMAIN": "AE",
      "USUBJID": "ONCO-2025-001-001-0001",
      "AESEQ": 1,
      "AETERM": "Nausea",
      "AEDECOD": "Nausea",
      "AEBODSYS": "Gastrointestinal disorders"
    }
  ]
}
```

---

## 6. Development Roadmap

### Completed ✅

| Phase | Content | Status |
|-------|---------|--------|
| 1 | Foundation (SKILL.md, domain knowledge, Phase 3) | ✅ |
| 2 | SDTM Domains (8 domains) | ✅ |
| 2 | Trial Phases (Phase 1, 2) | ✅ |
| 2 | Therapeutic Areas (4 areas) | ✅ |
| 2 | RWE Foundation | ✅ |
| 2 | Recruitment/Enrollment | ✅ |

### Future Phases

| Phase | Content | Priority | Est. Effort |
|-------|---------|----------|-------------|
| 3 | Phase 4 Post-Market | High | 1 week |
| 3 | Adaptive Designs (platform, basket, umbrella) | High | 2 weeks |
| 3 | Rare Disease Trials | Medium | 1 week |
| 4 | ADaM Domains (ADSL, ADAE, ADTTE) | Medium | 2 weeks |
| 4 | Additional Therapeutic Areas | Lower | Ongoing |
| 5 | PopulationSim Integration | Foundation | TBD |
| 5 | NetworkSim Integration | Foundation | TBD |

### Phase 3 Priorities

1. **Phase 4 Post-Market Surveillance**
   - PSUR/PBRER generation
   - Signal detection patterns
   - Risk management plans

2. **Adaptive Trial Designs**
   - Bayesian adaptive randomization
   - Sample size re-estimation
   - Platform trial standing infrastructure

3. **Rare Disease/Small Population**
   - Natural history studies
   - Single-arm with external control
   - N-of-1 designs

---

## 7. Quality Checklist

### New Skill Creation

- [ ] YAML frontmatter with name and description (including triggers)
- [ ] "For Claude" section with activation criteria
- [ ] At least 2 complete examples with JSON output
- [ ] Validation Rules table with business rules
- [ ] Related Skills section with cross-product integration
- [ ] Linked from SKILL.md Quick Links table
- [ ] CHANGELOG.md updated

### Code Review

- [ ] SDTM variable names match CDISC standard
- [ ] MedDRA/LOINC/ATC codes are realistic
- [ ] Date formats are ISO 8601 (YYYY-MM-DD)
- [ ] USUBJID format: STUDYID-SITEID-SUBJID
- [ ] Controlled terminology from CDISC CT

---

## 8. Key Reference Files

| Document | Location | Purpose |
|----------|----------|---------|
| Prompt Guide | `docs/TRIALSIM-PROMPT-GUIDE.md` | Usage examples |
| Architecture Guide | `docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` | Cross-product patterns |
| Development Process | `docs/HEALTHSIM-DEVELOPMENT-PROCESS.md` | Workflow |
| CDISC SDTM Format | `formats/cdisc-sdtm.md` | Output transformation |
| CDISC ADaM Format | `formats/cdisc-adam.md` | Analysis datasets |
| Code Systems | `references/code-systems.md` | ICD-10, LOINC, MedDRA |
| Data Models | `references/data-models.md` | Entity schemas |

---

## Appendix: Glossary

| Term | Definition |
|------|------------|
| **ADaM** | Analysis Data Model (CDISC) |
| **CGT** | Cell and Gene Therapy |
| **CDISC** | Clinical Data Interchange Standards Consortium |
| **CT** | Controlled Terminology |
| **DLT** | Dose-Limiting Toxicity |
| **EDC** | Electronic Data Capture |
| **I/E** | Inclusion/Exclusion criteria |
| **MedDRA** | Medical Dictionary for Regulatory Activities |
| **MTD** | Maximum Tolerated Dose |
| **ORR** | Objective Response Rate |
| **OS** | Overall Survival |
| **PFS** | Progression-Free Survival |
| **RECIST** | Response Evaluation Criteria in Solid Tumors |
| **RWE** | Real World Evidence |
| **SDTM** | Study Data Tabulation Model |
| **USUBJID** | Unique Subject Identifier |

---

*Last Updated: December 2024*
