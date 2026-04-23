# TrialSim Development Plan

**Status**: Planning
**Version**: 1.0
**Created**: 2024-12-18
**Target Completion**: Q1 2025

---

## Executive Summary

TrialSim generates realistic synthetic clinical trial data for testing, training, regulatory submission preparation, and system development. This plan establishes a phased approach to build a comprehensive skill library covering trial designs, therapeutic areas, CDISC compliance, and regulatory cohorts.

### Why TrialSim Matters

1. **Regulatory Preparation**: FDA/EMA submissions require CDISC-compliant data (SDTM/ADaM mandatory since 2016)
2. **System Testing**: EDC, CTMS, safety databases need realistic test data
3. **Training**: Clinical operations teams need realistic cohorts
4. **Analytics Development**: Statistical programmers need analysis-ready datasets

---

## Architecture Overview

```
trialsim/
├── SKILL.md                          # Master routing skill
├── clinical-trials-domain.md         # Core domain knowledge (foundational)
│
├── trial-designs/                    # Study design patterns
│   ├── README.md
│   ├── traditional-rct.md            # Standard parallel RCT
│   ├── adaptive-designs.md           # Dose-finding, sample size re-estimation
│   ├── basket-trials.md              # Multiple diseases, one target
│   ├── umbrella-trials.md            # One disease, multiple targets
│   └── platform-trials.md            # Standing infrastructure, add/drop arms
│
├── trial-phases/                     # Phase-specific patterns
│   ├── README.md
│   ├── phase1-safety.md              # First-in-human, dose escalation
│   ├── phase2-efficacy.md            # Proof of concept, dose ranging
│   ├── phase3-pivotal.md             # Registration trials
│   └── phase4-postmarket.md          # Safety surveillance
│
├── therapeutic-areas/                # Disease-specific patterns
│   ├── README.md
│   ├── oncology/
│   │   ├── solid-tumors.md
│   │   ├── hematologic-malignancies.md
│   │   └── immuno-oncology.md
│   ├── cardiovascular/
│   │   ├── heart-failure.md
│   │   └── acute-coronary.md
│   ├── cns/
│   │   ├── alzheimers.md
│   │   └── depression.md
│   ├── immunology/
│   │   ├── rheumatoid-arthritis.md
│   │   └── inflammatory-bowel.md
│   ├── metabolic/
│   │   ├── diabetes.md
│   │   └── obesity.md
│   └── rare-diseases/
│       └── gene-therapy.md
│
├── data-domains/                     # SDTM domain generation
│   ├── README.md
│   ├── demographics-dm.md            # Subject demographics
│   ├── adverse-events-ae.md          # Safety events
│   ├── concomitant-meds-cm.md        # Prior/concomitant medications
│   ├── medical-history-mh.md         # Medical history
│   ├── exposure-ex.md                # Study drug exposure
│   ├── laboratory-lb.md              # Lab results
│   ├── vital-signs-vs.md             # Vitals
│   ├── ecg-eg.md                     # ECG findings
│   ├── disposition-ds.md             # Subject disposition
│   ├── efficacy-custom.md            # Efficacy endpoints (varies by TA)
│   └── tumor-response-rs.md          # RECIST/oncology response
│
├── operational/                      # Trial operations
│   ├── README.md
│   ├── site-selection.md             # Site/investigator patterns
│   ├── recruitment-enrollment.md     # Screening funnel
│   ├── randomization.md              # Stratification, blocking
│   ├── protocol-deviations.md        # Deviation types/patterns
│   └── discontinuation.md            # Dropout patterns
│
└── regulatory/                       # Regulatory cohorts
    ├── README.md
    ├── ind-submission.md             # IND safety data
    ├── nda-bla-submission.md         # Full submission package
    └── safety-reporting.md           # SAE/SUSAR reporting
```

---

## Phase 1: Foundation (Weeks 1-2)

**Goal**: Establish core domain knowledge and canonical data models

### Deliverables

| # | Deliverable | Description | Priority |
|---|-------------|-------------|----------|
| 1.1 | Enhanced `clinical-trials-domain.md` | Complete domain reference | Critical |
| 1.2 | Canonical data models | Trial, Site, Subject, Visit, AE entities | Critical |
| 1.3 | Reference data files | MedDRA SOC/PT samples, WHO Drug codes | High |
| 1.4 | `traditional-rct.md` | Standard RCT design skill | High |

### 1.1 Enhanced Domain Knowledge

Expand `clinical-trials-domain.md` to include:

```markdown
## Trial Phases (detailed)
- Phase 1a/1b distinctions
- Phase 2a/2b (exploratory vs confirmatory)
- Seamless Phase 2/3 designs

## Regulatory Framework
- ICH E6(R2) GCP requirements
- 21 CFR Part 11 (electronic records)
- FDA eCTD submission structure
- EMA requirements differences

## Key Roles
- Sponsor, CRO, Site relationships
- Principal Investigator responsibilities
- IRB/Ethics Committee oversight
- DSMB/DMC structure

## Visit Windows
- Scheduled vs actual visit dates
- Visit window calculations (+/- days)
- Unscheduled visit handling

## Population Definitions
- Intent-to-Treat (ITT)
- Modified ITT (mITT)
- Per-Protocol (PP)
- Safety Population
```

### 1.2 Canonical Data Models

Create `references/trialsim-entities.md`:

```json
// Study
{
  "study_id": "ABC-123-001",
  "protocol_number": "ABC-123",
  "protocol_title": "A Phase 3, Randomized...",
  "phase": "Phase 3",
  "therapeutic_area": "Oncology",
  "indication": "NSCLC",
  "sponsor": "Example Pharma",
  "design_type": "Parallel",
  "blinding": "Double-blind",
  "comparator": "Placebo",
  "target_enrollment": 450,
  "study_duration_months": 36,
  "arms": [...],
  "endpoints": {...}
}

// Site
{
  "site_id": "001",
  "site_number": "US-001",
  "facility_name": "Memorial Cancer Center",
  "country": "USA",
  "region": "North America",
  "investigator": {...},
  "irb_approval_date": "2024-01-10",
  "site_activation_date": "2024-02-01",
  "target_enrollment": 25
}

// Subject
{
  "subject_id": "ABC-123-001-0001",
  "site_id": "001",
  "screening_number": "SCR-0001",
  "screening_date": "2024-03-01",
  "consent_date": "2024-03-01",
  "randomization_date": "2024-03-08",
  "randomization_number": "R0001",
  "arm_code": "TRT",
  "arm_name": "Treatment",
  "status": "Active",
  "demographics": {...},
  "inclusion_criteria_met": true,
  "exclusion_criteria_met": false
}
```

### 1.3 Reference Data

Create reference files:
- `references/meddra-sample.csv` - Common SOC/PT/LLT codes
- `references/who-drug-sample.csv` - Common medication codes
- `references/country-codes.csv` - ISO 3166 country codes
- `references/units-ucum.csv` - Standard units

---

## Phase 2: Core Skills (Weeks 3-5)

**Goal**: Build essential trial-type and data-domain skills

### Deliverables

| # | Deliverable | Description | Priority |
|---|-------------|-------------|----------|
| 2.1 | `phase1-safety.md` | Phase 1 dose-escalation trials | High |
| 2.2 | `phase3-pivotal.md` | Enhanced pivotal trial skill | Critical |
| 2.3 | `demographics-dm.md` | SDTM DM domain generation | Critical |
| 2.4 | `adverse-events-ae.md` | SDTM AE domain generation | Critical |
| 2.5 | `disposition-ds.md` | Subject disposition | High |
| 2.6 | `laboratory-lb.md` | Lab results generation | High |
| 2.7 | `recruitment-enrollment.md` | Enhanced recruitment patterns | High |

### 2.1 Phase 1 Safety Trial Skill

```markdown
## Phase 1 Trial Characteristics

| Aspect | Typical Values |
|--------|----------------|
| Sample Size | 20-100 subjects |
| Duration | 6-12 months |
| Sites | 1-5 (often academic) |
| Design | 3+3 dose escalation, mTPI, BOIN |
| Population | Healthy volunteers or patients |
| Primary Endpoint | MTD, DLT, PK parameters |

## Dose Escalation Patterns
- 3+3 traditional design
- Accelerated titration
- mTPI (modified toxicity probability interval)
- BOIN (Bayesian optimal interval)
- CRM (continual reassessment method)

## DLT (Dose-Limiting Toxicity) Rules
- Grade 3+ non-hematologic toxicity
- Grade 4 hematologic toxicity
- Treatment-related death
- Study-specific criteria
```

### 2.4 Adverse Events Skill Structure

```markdown
## Adverse Event Patterns by Phase

### Phase 1
- Higher AE incidence (dose finding)
- More SAEs expected
- Detailed PK correlation

### Phase 3
- Treatment vs placebo comparison
- SOC distribution patterns
- TEAE vs non-TEAE classification

## MedDRA Coding
- System Organ Class (SOC)
- High Level Group Term (HLGT)
- High Level Term (HLT)
- Preferred Term (PT)
- Lowest Level Term (LLT)

## Severity Grading
- CTCAE v5.0 (oncology)
- Mild/Moderate/Severe (general)

## Causality Assessment
- Not related
- Unlikely
- Possible
- Probable
- Definite
```

---

## Phase 3: Therapeutic Areas (Weeks 6-8)

**Goal**: Build disease-specific trial patterns

### Deliverables

| # | Deliverable | Description | Priority |
|---|-------------|-------------|----------|
| 3.1 | `oncology/solid-tumors.md` | Solid tumor trials | Critical |
| 3.2 | `oncology/immuno-oncology.md` | IO/checkpoint inhibitors | High |
| 3.3 | `cardiovascular/heart-failure.md` | HF outcomes trials | High |
| 3.4 | `metabolic/diabetes.md` | T2DM trials | High |
| 3.5 | `cns/alzheimers.md` | AD/dementia trials | Medium |

### 3.1 Oncology Solid Tumors Skill

```markdown
## Oncology Trial Characteristics

| Aspect | Typical Values |
|--------|----------------|
| Endpoints | ORR, PFS, OS, DOR |
| Response Criteria | RECIST 1.1, iRECIST |
| Assessment Schedule | Every 6-8 weeks |
| Follow-up | Until progression/death |

## RECIST 1.1 Response Categories
- Complete Response (CR)
- Partial Response (PR)
- Stable Disease (SD)
- Progressive Disease (PD)

## Common Adverse Events by Drug Class
### Checkpoint Inhibitors
- Immune-related AEs (irAEs)
- Pneumonitis, colitis, hepatitis
- Thyroid dysfunction
- Skin reactions

### Chemotherapy
- Myelosuppression
- Nausea/vomiting
- Alopecia
- Fatigue

## Biomarker Stratification
- PD-L1 expression levels
- TMB (tumor mutational burden)
- MSI status
- Driver mutations (EGFR, ALK, etc.)
```

---

## Phase 4: Advanced Designs & Operations (Weeks 9-11)

**Goal**: Support modern trial designs and operational cohorts

### Deliverables

| # | Deliverable | Description | Priority |
|---|-------------|-------------|----------|
| 4.1 | `adaptive-designs.md` | Adaptive trial patterns | High |
| 4.2 | `basket-trials.md` | Basket/bucket design | Medium |
| 4.3 | `umbrella-trials.md` | Umbrella design | Medium |
| 4.4 | `platform-trials.md` | MAMS platform design | Medium |
| 4.5 | `protocol-deviations.md` | Deviation patterns | High |
| 4.6 | `discontinuation.md` | Dropout/withdrawal | High |

### 4.1 Adaptive Designs Skill

```markdown
## Adaptive Design Types

### Sample Size Re-estimation
- Blinded vs unblinded
- Interim analysis timing
- Conditional power calculations

### Response-Adaptive Randomization
- Shift allocation to better-performing arm
- Bayesian probability models

### Seamless Phase 2/3
- Single protocol, two stages
- Learning phase → Confirmatory phase
- Selected dose(s) carry forward

## Master Protocol Structures
- Basket: One drug, multiple diseases (common mutation)
- Umbrella: One disease, multiple drugs (multiple biomarkers)
- Platform: Standing trial, arms added/dropped
```

---

## Phase 5: CDISC Compliance & Formats (Weeks 12-14)

**Goal**: Complete SDTM/ADaM transformation capabilities

### Deliverables

| # | Deliverable | Description | Priority |
|---|-------------|-------------|----------|
| 5.1 | Enhanced `cdisc-sdtm.md` | All core domains | Critical |
| 5.2 | Enhanced `cdisc-adam.md` | ADSL, ADAE, ADTTE | Critical |
| 5.3 | `define-xml.md` | Define-XML generation | High |
| 5.4 | `sdtm-validation.md` | Pinnacle21 rules | High |

### SDTM Domain Coverage

| Domain | Code | Priority | Status |
|--------|------|----------|--------|
| Demographics | DM | Critical | Partial |
| Adverse Events | AE | Critical | Partial |
| Concomitant Meds | CM | High | Planned |
| Medical History | MH | High | Planned |
| Exposure | EX | Critical | Planned |
| Laboratory | LB | Critical | Planned |
| Vital Signs | VS | High | Planned |
| ECG | EG | Medium | Planned |
| Disposition | DS | Critical | Planned |
| Subject Visits | SV | High | Planned |
| Tumor Results | RS | High (onc) | Planned |
| Trial Arms | TA | Critical | Planned |
| Trial Elements | TE | Critical | Planned |
| Trial Visits | TV | Critical | Planned |
| Trial Summary | TS | Critical | Planned |

### ADaM Dataset Coverage

| Dataset | Code | Priority | Status |
|---------|------|----------|--------|
| Subject Level | ADSL | Critical | Partial |
| Adverse Events | ADAE | Critical | Partial |
| Efficacy | ADEFF | High | Planned |
| Laboratory | ADLB | High | Planned |
| Time-to-Event | ADTTE | Critical | Planned |
| Tumor Response | ADRS | High (onc) | Planned |

---

## Phase 6: Examples & Validation (Weeks 15-16)

**Goal**: Complete examples and quality validation

### Deliverables

| # | Deliverable | Description | Priority |
|---|-------------|-------------|----------|
| 6.1 | Hello-TrialSim examples | Starter examples | Critical |
| 6.2 | Complete cohort examples | Full trial datasets | High |
| 6.3 | Validation test suite | Automated testing | High |
| 6.4 | Documentation updates | README, guides | High |

### Hello-TrialSim Examples

```markdown
## hello-healthsim/trialsim/

### Basic Examples
- hello-phase3-dm.md          # Simple Phase 3, DM domain only
- hello-phase3-full.md        # Phase 3 with all core domains
- hello-oncology-basic.md     # Oncology trial basics
- hello-adaptive.md           # Simple adaptive design

### Complete Cohorts
- diabetes-cvot.md            # Cardiovascular outcomes trial
- nsclc-immunotherapy.md      # NSCLC checkpoint inhibitor
- alzheimers-phase3.md        # AD disease modification trial
- rare-disease-gene.md        # Gene therapy trial
```

---

## Reference Data Requirements

### MedDRA Terms (Sample Coverage)

| SOC | Example PTs | Use Case |
|-----|-------------|----------|
| Nervous system disorders | Headache, Dizziness | General |
| Gastrointestinal disorders | Nausea, Diarrhea | General |
| Skin disorders | Rash, Pruritus | IO/immunology |
| Respiratory disorders | Pneumonitis, Dyspnea | IO/oncology |
| Hepatobiliary disorders | Hepatitis, ALT increased | Safety |
| Immune system disorders | irAE patterns | IO |
| Neoplasms | Progression, metastasis | Oncology |
| Metabolism/nutrition | Hyperglycemia | Diabetes |

### WHO Drug/ATC Codes (Sample Coverage)

| ATC Class | Examples | Use Case |
|-----------|----------|----------|
| L01 Antineoplastics | Pembrolizumab, Docetaxel | Oncology |
| A10 Diabetes drugs | Metformin, Insulin | Diabetes |
| C Cardiovascular | Lisinopril, Atorvastatin | CV/conmeds |
| N Nervous system | Acetaminophen, Ibuprofen | Conmeds |

---

## Integration Points

### PatientSim → TrialSim

```json
// Extend Patient to create Subject
{
  "source": "PatientSim.Patient",
  "transform": {
    "add_fields": [
      "consent_date",
      "screening_number",
      "randomization_number",
      "arm_assignment",
      "subject_status"
    ],
    "rename_fields": {
      "mrn": "subject_id"
    },
    "apply_eligibility": {
      "inclusion_criteria": [...],
      "exclusion_criteria": [...]
    }
  }
}
```

### NetworkSim → TrialSim

```json
// Extend Provider to create Investigator
{
  "source": "NetworkSim.Provider",
  "transform": {
    "add_fields": [
      "medical_license_verified",
      "gcp_training_date",
      "cv_on_file",
      "financial_disclosure",
      "delegation_log"
    ]
  }
}
```

---

## Success Criteria

### Phase 1 (Foundation)
- [ ] Domain knowledge skill covers all essential concepts
- [ ] Canonical models defined with full entity schemas
- [ ] Reference data files created and linked

### Phase 2 (Core Skills)
- [ ] Can generate complete Phase 3 trial with core domains
- [ ] DM, AE, DS, LB domains produce valid SDTM
- [ ] Each skill has ≥2 complete examples

### Phase 3 (Therapeutic Areas)
- [ ] Oncology trials with RECIST response data
- [ ] CV outcomes trials with MACE endpoints
- [ ] Realistic therapeutic-specific patterns

### Phase 4 (Advanced)
- [ ] Adaptive designs generate appropriate interim data
- [ ] Master protocols produce correct sub-study structures
- [ ] Operational cohorts (deviations, dropouts) realistic

### Phase 5 (CDISC)
- [ ] SDTM output passes Pinnacle21 validation
- [ ] ADaM datasets have correct traceability
- [ ] Define-XML generation functional

### Phase 6 (Examples)
- [ ] Hello-TrialSim examples all functional
- [ ] Complete cohort examples demonstrate full capability
- [ ] Documentation complete and accurate

---

## Risk & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| CDISC complexity underestimated | High | Start with core domains, expand |
| Therapeutic area depth required | Medium | Focus on top 3 TAs first |
| Reference data gaps | Medium | Use synthetic/sample codes |
| Scope creep | High | Strict prioritization |

---

## Resource Estimates

| Phase | Estimated Effort | Dependencies |
|-------|------------------|--------------|
| Phase 1 | 8-10 hours | None |
| Phase 2 | 15-20 hours | Phase 1 |
| Phase 3 | 12-15 hours | Phase 2 |
| Phase 4 | 10-12 hours | Phase 2 |
| Phase 5 | 12-15 hours | Phases 2-4 |
| Phase 6 | 8-10 hours | All phases |
| **Total** | **65-82 hours** | |

---

## Next Steps

1. **Immediate**: Review and approve this plan
2. **Week 1**: Begin Phase 1 - Enhanced domain knowledge
3. **Checkpoint**: Review after Phase 2 completion
4. **Iterate**: Adjust based on learnings

---

## Appendix A: CDISC SDTM Domain Reference

### General Observation Classes

| Class | Domains | Description |
|-------|---------|-------------|
| Interventions | CM, EX, SU, PR | Treatments/procedures applied |
| Events | AE, DS, MH, CE | Occurrences (adverse, medical history) |
| Findings | LB, VS, EG, PE | Measurements and observations |
| Special Purpose | DM, CO, SE, SV | Demographics, comments, subject elements |
| Trial Design | TA, TE, TV, TI, TS | Study structure |

### Required Variables (all domains)

| Variable | Label | Type | Required |
|----------|-------|------|----------|
| STUDYID | Study Identifier | Char | Yes |
| DOMAIN | Domain Abbreviation | Char | Yes |
| USUBJID | Unique Subject ID | Char | Yes |

---

## Appendix B: Therapeutic Area Priorities

Based on 2024 clinical trial landscape:

| Rank | Therapeutic Area | % of Trials | Priority |
|------|------------------|-------------|----------|
| 1 | Oncology | 41% | Critical |
| 2 | CNS/Neurology | 12% | High |
| 3 | Cardiovascular | 10% | High |
| 4 | Immunology/Inflammation | 9% | High |
| 5 | Infectious Disease | 7% | Medium |
| 6 | Metabolic/Endocrine | 6% | High |
| 7 | Rare Diseases | 5% | Medium |
| 8 | Other | 10% | Low |

---

## Appendix C: Key Terminology

| Term | Definition |
|------|------------|
| SDTM | Study Data Tabulation Model - FDA submission format |
| ADaM | Analysis Data Model - Statistical analysis format |
| CDISC | Clinical Data Interchange Standards Consortium |
| eCTD | Electronic Common Technical Document |
| ICH-GCP | International Council for Harmonisation - Good Clinical Practice |
| RECIST | Response Evaluation Criteria In Solid Tumors |
| MedDRA | Medical Dictionary for Regulatory Activities |
| TEAE | Treatment-Emergent Adverse Event |
| ITT | Intent-to-Treat population |
| DLT | Dose-Limiting Toxicity |
| MTD | Maximum Tolerated Dose |
| DSMB | Data Safety Monitoring Board |
