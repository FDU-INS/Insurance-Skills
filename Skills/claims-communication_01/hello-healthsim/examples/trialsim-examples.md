# TrialSim Examples

Generate synthetic clinical trial data for testing CDISC-compliant systems, regulatory submission pipelines, and clinical data management tools.

> **TrialSim generates synthetic clinical trial data only.** This is test data for software development, not actual clinical research data. The trial designs, adverse event patterns, and efficacy results are simulated for realistic software testing scenarios.

---

## Quick Start Examples

### Example 1: Generate a Simple Phase III Trial

```
Generate a Phase III oncology trial with 200 subjects
```

This creates:
- Study design with treatment arms
- 200 randomized subjects with demographics
- Baseline characteristics
- Randomization to treatment arms

### Example 2: Generate Adverse Events

```
Generate adverse events for a Phase III immunotherapy trial with 150 subjects
```

This creates:
- Treatment-emergent adverse events (TEAEs)
- Serious adverse events (SAEs)
- Immune-related adverse events (irAEs)
- MedDRA-coded terms with severity grades

### Example 3: Generate Screen Failures

```
Generate screening data with 30% screen failure rate for 100 randomized subjects
```

This creates:
- Complete screening funnel (identified → randomized)
- Screen failure reasons by category
- Eligibility assessments

---

## Phase I: Dose Escalation Examples

### 3+3 Design

```
Generate a Phase I dose escalation study using 3+3 design with 5 dose levels
```

**What you get:**
- 5 dose cohorts (10mg, 20mg, 40mg, 80mg, 160mg)
- 3-6 subjects per cohort based on DLT patterns
- Dose-limiting toxicity events with CTCAE grades
- Escalation decisions documented
- Maximum tolerated dose (MTD) determination

**Example Output Summary:**
```json
{
  "study_design": {
    "design_type": "3+3",
    "dose_levels": [
      {"level": 1, "dose": "10mg", "subjects": 3, "dlts": 0, "decision": "ESCALATE"},
      {"level": 2, "dose": "20mg", "subjects": 3, "dlts": 0, "decision": "ESCALATE"},
      {"level": 3, "dose": "40mg", "subjects": 3, "dlts": 1, "decision": "EXPAND"},
      {"level": 3, "dose": "40mg", "subjects": 6, "dlts": 1, "decision": "ESCALATE"},
      {"level": 4, "dose": "80mg", "subjects": 3, "dlts": 2, "decision": "MTD_EXCEEDED"},
      {"level": 5, "dose": "160mg", "subjects": 0, "dlts": 0, "decision": "NOT_OPENED"}
    ],
    "mtd": "40mg",
    "rp2d": "40mg"
  }
}
```

### BOIN Design

```
Generate a Phase I BOIN design study with target toxicity rate 30%
```

**What you get:**
- Bayesian Optimal Interval (BOIN) escalation rules
- Target DLT rate: 30% (default)
- Lambda_e and Lambda_d boundaries
- Dose allocation based on observed DLT rates
- Isotonic regression for MTD selection

**Example BOIN Boundaries:**
```
Target: 30% | Lambda_e: 0.236 | Lambda_d: 0.359

Decision Rules:
- If observed DLT rate < 0.236 → ESCALATE
- If 0.236 ≤ DLT rate ≤ 0.359 → STAY
- If observed DLT rate > 0.359 → DE-ESCALATE
```

### CRM Design

```
Generate a Phase I CRM study with 6 dose levels, target 25% DLT rate
```

**What you get:**
- Continual Reassessment Method design
- Model-based dose recommendations
- Posterior toxicity probability estimates
- Skeleton (prior toxicity probabilities)
- Coherent dose transitions

### First-in-Human (FIH) SAD/MAD

```
Generate a first-in-human study with SAD and MAD cohorts
```

**What you get:**
- **SAD (Single Ascending Dose):**
  - Healthy volunteer cohorts
  - Sentinel dosing (2 subjects → remaining)
  - 48-hour safety observation periods
  - Intensive PK sampling (pre-dose, 0.5, 1, 2, 4, 8, 12, 24, 48h)
  
- **MAD (Multiple Ascending Dose):**
  - 7-14 day dosing periods
  - Steady-state PK assessment
  - Accumulation ratio calculations
  - Trough level monitoring

**Example SAD Cohort:**
```json
{
  "cohort": "SAD Cohort 1",
  "dose": "10mg",
  "subjects": [
    {"id": "101-001", "sentinel": true, "dose_date": "2024-01-15"},
    {"id": "101-002", "sentinel": true, "dose_date": "2024-01-15"},
    {"id": "101-003", "sentinel": false, "dose_date": "2024-01-17"},
    {"id": "101-004", "sentinel": false, "dose_date": "2024-01-17"},
    {"id": "101-005", "sentinel": false, "dose_date": "2024-01-17"},
    {"id": "101-006", "sentinel": false, "dose_date": "2024-01-17"}
  ],
  "pk_samples": 12,
  "dlts": 0,
  "decision": "ESCALATE"
}
```

### Expansion Cohorts

```
Generate Phase I expansion cohorts for 3 tumor types at RP2D
```

**What you get:**
- Indication-specific cohorts (e.g., NSCLC, melanoma, RCC)
- 20-40 subjects per indication
- Preliminary efficacy signals
- Safety confirmation at RP2D
- Biomarker correlations

---

## Phase II: Proof-of-Concept Examples

### Simon's Two-Stage Design

```
Generate a Phase II Simon's optimal two-stage design, p0=0.10, p1=0.30
```

**What you get:**
- Two-stage enrollment with interim futility
- Stage 1: Enroll n1 subjects, stop if ≤r1 responses
- Stage 2: Continue to N total if >r1 responses
- Optimal design (minimizes expected sample size under H0)

**Example Simon's Design Output:**
```json
{
  "design_type": "Simon's Two-Stage Optimal",
  "null_response_rate": 0.10,
  "alternative_response_rate": 0.30,
  "alpha": 0.05,
  "power": 0.80,
  "stage_1": {
    "n": 10,
    "r": 1,
    "rule": "Stop if ≤1 response in first 10 subjects"
  },
  "stage_2": {
    "N": 29,
    "R": 5,
    "rule": "Reject H0 if ≥6 responses in 29 subjects"
  },
  "expected_sample_size_h0": 17.4,
  "probability_early_termination": 0.736,
  "results": {
    "stage_1_responses": 3,
    "stage_1_decision": "CONTINUE TO STAGE 2",
    "total_responses": 8,
    "total_subjects": 29,
    "response_rate": 0.276,
    "conclusion": "REJECT H0 - PROCEED TO PHASE III"
  }
}
```

### Simon's Minimax Design

```
Generate a Phase II Simon's minimax design for rare tumor, p0=0.05, p1=0.20
```

**What you get:**
- Minimax design (minimizes maximum sample size)
- Higher probability of going to Stage 2
- Lower total N but higher expected N under H0

### Phase II Randomized

```
Generate a randomized Phase II with 2:1 randomization, 80 subjects
```

**What you get:**
- Treatment arm: 53 subjects
- Control arm: 27 subjects
- Response rate comparison
- Preliminary efficacy signals

### MCP-Mod Dose-Ranging

```
Generate a Phase IIb dose-ranging study using MCP-Mod with 5 dose levels
```

**What you get:**
- Multiple Comparison Procedure with Modeling (MCP-Mod)
- Candidate dose-response models (Emax, sigmoid Emax, linear, quadratic, exponential)
- Dose levels: Placebo, 25mg, 50mg, 100mg, 200mg
- Model selection via contrast tests
- Target dose estimation

**Example MCP-Mod Output:**
```json
{
  "design_type": "MCP-Mod",
  "doses": [0, 25, 50, 100, 200],
  "subjects_per_arm": 50,
  "candidate_models": [
    {"model": "Emax", "ed50": 50, "contrast_p": 0.002},
    {"model": "Sigmoid Emax", "ed50": 75, "h": 2, "contrast_p": 0.008},
    {"model": "Linear", "contrast_p": 0.045},
    {"model": "Quadratic", "contrast_p": 0.089},
    {"model": "Exponential", "contrast_p": 0.156}
  ],
  "selected_model": "Emax",
  "target_dose": "100mg",
  "dose_response_curve": {
    "placebo_effect": 2.5,
    "max_effect": 8.2,
    "ed50": 48,
    "ed90": 145
  }
}
```

### Futility Analysis

```
Generate Phase II with interim futility analysis at 50% enrollment
```

**What you get:**
- Interim analysis at n/2 subjects
- Conditional power calculation
- Predictive probability of success
- Go/No-Go decision framework

---

## Phase III: Pivotal Trial Examples

### Superiority Trial

```
Generate a Phase III superiority trial for first-line metastatic NSCLC with 500 subjects
```

**What you get:**
- Large randomized population
- 1:1 randomization to treatment vs SOC
- Primary endpoint: Progression-free survival
- Secondary: Overall survival, ORR, DOR
- Stratification factors (PD-L1 status, smoking history)

### Non-Inferiority Trial

```
Generate a Phase III non-inferiority trial with NI margin of 1.3 HR
```

**What you get:**
- Non-inferiority margin specification
- Sample size for NI conclusion
- One-sided testing at α=0.025
- Sensitivity analyses (per-protocol, as-treated)

### Multi-Regional Trial

```
Generate a global Phase III trial with sites in US, EU, and Asia
```

**What you get:**
- Regional distribution per ICH E17
- Site distribution: 40% US, 35% EU, 25% Asia
- Ethnic sensitivity considerations
- Regional consistency analysis plan

### DSMB Interim Analysis

```
Generate Phase III with 2 interim analyses and O'Brien-Fleming boundaries
```

**What you get:**
- DSMB charter structure
- Interim looks at 33% and 67% information
- O'Brien-Fleming alpha spending
- Efficacy and futility boundaries
- Sample size re-estimation option

---

## Therapeutic Area Examples

### Oncology

```
Generate an oncology trial for Stage IV melanoma with RECIST assessments
```

**What you get:**
- Tumor measurements per RECIST 1.1
- Target lesion selection (≤5 total, ≤2 per organ)
- Best overall response (CR, PR, SD, PD)
- Progression-free survival data
- Overall survival data
- Tumor response kinetics

**Example RECIST Data:**
```json
{
  "subject_id": "CDISC01-101-0001",
  "target_lesions": [
    {"id": "TL01", "location": "Liver", "baseline": 45, "week8": 32, "week16": 28},
    {"id": "TL02", "location": "Lung RLL", "baseline": 23, "week8": 18, "week16": 15}
  ],
  "sum_of_diameters": {
    "baseline": 68,
    "nadir": 43,
    "percent_change_from_baseline": -36.8
  },
  "best_overall_response": "PR",
  "confirmed": true,
  "confirmation_date": "2024-05-15"
}
```

### Cardiovascular

```
Generate a cardiovascular outcomes trial with MACE endpoint
```

**What you get:**
- Major Adverse Cardiovascular Events (MACE)
- Component events (CV death, MI, stroke)
- Time-to-event data
- Heart failure hospitalizations
- Cardiac biomarkers (troponin, BNP)
- Adjudication process

### CNS/Neurology

```
Generate a Phase III Alzheimer's disease trial with cognitive endpoints
```

**What you get:**
- ADAS-Cog scores over time (0-70 scale, higher = worse)
- MMSE assessments (0-30 scale, lower = worse)
- CDR-SB ratings (0-18 scale)
- MRI volumetric data (hippocampal volume)
- Amyloid PET results
- Functional assessments (ADCS-ADL)

### Cell & Gene Therapy

```
Generate a CAR-T cell therapy trial with long-term follow-up
```

**What you get:**
- Single-dose administration (lymphodepletion + infusion)
- Cytokine release syndrome (CRS) events graded per ASTCT
- Neurotoxicity (ICANS) assessments
- Complete response rates by Day 28
- Duration of response
- 5-year follow-up visits (quarterly Year 1, semi-annual Years 2-5)
- B-cell aplasia monitoring
- Immunoglobulin replacement therapy

---

## SDTM Domain Examples

### Demographics (DM)

```
Generate DM domain for 50 subjects in a Phase III diabetes trial
```

**Example Output:**
```csv
STUDYID,DOMAIN,USUBJID,SUBJID,RFSTDTC,RFENDTC,SITEID,AGE,AGEU,SEX,RACE,ETHNIC,ARMCD,ARM,COUNTRY
CDISC01,DM,CDISC01-101-0001,0001,2024-01-15,2024-07-15,101,58,YEARS,M,WHITE,NOT HISPANIC OR LATINO,TRT,Semaglutide 1mg,USA
CDISC01,DM,CDISC01-101-0002,0002,2024-01-18,2024-07-20,101,52,YEARS,F,BLACK OR AFRICAN AMERICAN,NOT HISPANIC OR LATINO,PBO,Placebo,USA
CDISC01,DM,CDISC01-102-0001,0001,2024-01-20,2024-07-22,102,64,YEARS,M,ASIAN,NOT HISPANIC OR LATINO,TRT,Semaglutide 1mg,USA
```

### Adverse Events (AE)

```
Generate AE domain with immune-related adverse events for checkpoint inhibitor trial
```

**Example Output:**
```csv
STUDYID,DOMAIN,USUBJID,AESEQ,AETERM,AEDECOD,AEBODSYS,AESEV,AETOXGR,AESER,AEREL,AEACN,AEOUT,AESTDTC,AEENDTC
CDISC01,AE,CDISC01-101-0001,1,Diarrhea,Diarrhoea,Gastrointestinal disorders,MODERATE,2,N,PROBABLE,DOSE NOT CHANGED,RECOVERED/RESOLVED,2024-02-15,2024-02-22
CDISC01,AE,CDISC01-101-0001,2,Thyroid function abnormal,Hypothyroidism,Endocrine disorders,MILD,1,N,PROBABLE,DOSE NOT CHANGED,NOT RECOVERED/NOT RESOLVED,2024-03-10,
CDISC01,AE,CDISC01-101-0001,3,Pneumonitis,Pneumonitis,Respiratory disorders,SEVERE,3,Y,DEFINITE,DRUG WITHDRAWN,RECOVERED/RESOLVED WITH SEQUELAE,2024-04-05,2024-05-20
```

### Laboratory (LB)

```
Generate LB domain with hepatic function panel for 20 subjects
```

**Example Output:**
```csv
STUDYID,DOMAIN,USUBJID,LBSEQ,LBTESTCD,LBTEST,LBCAT,LBORRES,LBORRESU,LBSTRESN,LBSTRESU,LBNRIND,VISITNUM,VISIT,LBDTC
CDISC01,LB,CDISC01-101-0001,1,ALT,Alanine Aminotransferase,CHEMISTRY,28,U/L,28,U/L,NORMAL,1,SCREENING,2024-01-10
CDISC01,LB,CDISC01-101-0001,2,AST,Aspartate Aminotransferase,CHEMISTRY,24,U/L,24,U/L,NORMAL,1,SCREENING,2024-01-10
CDISC01,LB,CDISC01-101-0001,3,BILI,Bilirubin,CHEMISTRY,0.8,mg/dL,0.8,mg/dL,NORMAL,1,SCREENING,2024-01-10
CDISC01,LB,CDISC01-101-0001,4,ALT,Alanine Aminotransferase,CHEMISTRY,45,U/L,45,U/L,HIGH,5,WEEK 4,2024-02-12
```

### Vital Signs (VS)

```
Generate VS domain with pre-dose and post-dose vital signs
```

**Example Output:**
```csv
STUDYID,DOMAIN,USUBJID,VSSEQ,VSTESTCD,VSTEST,VSPOS,VSORRES,VSORRESU,VSSTRESN,VSSTRESU,VISITNUM,VISIT,VSTPT,VSTPTNUM,VSDTC
CDISC01,VS,CDISC01-101-0001,1,SYSBP,Systolic Blood Pressure,SITTING,128,mmHg,128,mmHg,2,DAY 1,PRE-DOSE,-15,2024-01-15T08:45
CDISC01,VS,CDISC01-101-0001,2,SYSBP,Systolic Blood Pressure,SITTING,132,mmHg,132,mmHg,2,DAY 1,1 HR POST-DOSE,60,2024-01-15T10:00
CDISC01,VS,CDISC01-101-0001,3,DIABP,Diastolic Blood Pressure,SITTING,82,mmHg,82,mmHg,2,DAY 1,PRE-DOSE,-15,2024-01-15T08:45
```

### Exposure (EX)

```
Generate EX domain for IV infusion regimen
```

**Example Output:**
```csv
STUDYID,DOMAIN,USUBJID,EXSEQ,EXTRT,EXDOSE,EXDOSU,EXDOSFRM,EXDOSFRQ,EXROUTE,EXSTDTC,EXENDTC,EPOCH,EXADJ
CDISC01,EX,CDISC01-101-0001,1,PEMBROLIZUMAB,200,mg,INJECTION,Q3W,INTRAVENOUS,2024-01-15,2024-01-15,TREATMENT,
CDISC01,EX,CDISC01-101-0001,2,PEMBROLIZUMAB,200,mg,INJECTION,Q3W,INTRAVENOUS,2024-02-05,2024-02-05,TREATMENT,
CDISC01,EX,CDISC01-101-0001,3,PEMBROLIZUMAB,200,mg,INJECTION,Q3W,INTRAVENOUS,2024-02-26,2024-02-26,TREATMENT,DOSE DELAY DUE TO AE
```

### Disposition (DS)

```
Generate DS domain with protocol milestones and discontinuations
```

**Example Output:**
```csv
STUDYID,DOMAIN,USUBJID,DSSEQ,DSTERM,DSDECOD,DSCAT,DSSCAT,EPOCH,DSSTDTC
CDISC01,DS,CDISC01-101-0001,1,INFORMED CONSENT OBTAINED,INFORMED CONSENT OBTAINED,PROTOCOL MILESTONE,STUDY PARTICIPATION,SCREENING,2024-01-10
CDISC01,DS,CDISC01-101-0001,2,RANDOMIZED,RANDOMIZED,PROTOCOL MILESTONE,STUDY PARTICIPATION,SCREENING,2024-01-15
CDISC01,DS,CDISC01-101-0001,3,COMPLETED,COMPLETED,DISPOSITION EVENT,STUDY COMPLETION,FOLLOW-UP,2024-07-15
CDISC01,DS,CDISC01-101-0002,1,INFORMED CONSENT OBTAINED,INFORMED CONSENT OBTAINED,PROTOCOL MILESTONE,STUDY PARTICIPATION,SCREENING,2024-01-12
CDISC01,DS,CDISC01-101-0002,2,RANDOMIZED,RANDOMIZED,PROTOCOL MILESTONE,STUDY PARTICIPATION,SCREENING,2024-01-18
CDISC01,DS,CDISC01-101-0002,3,ADVERSE EVENT,ADVERSE EVENT,DISPOSITION EVENT,TREATMENT,TREATMENT,2024-04-20
```

### Medical History (MH)

```
Generate MH domain for oncology trial subjects with comorbidities
```

**Example Output:**
```csv
STUDYID,DOMAIN,USUBJID,MHSEQ,MHTERM,MHDECOD,MHBODSYS,MHCAT,MHPRESP,MHOCCUR,MHSTDTC,MHONGO
CDISC01,MH,CDISC01-101-0001,1,Type 2 diabetes,Type 2 diabetes mellitus,Metabolism and nutrition disorders,GENERAL MEDICAL HISTORY,Y,Y,2018-06-15,Y
CDISC01,MH,CDISC01-101-0001,2,Hypertension,Hypertension,Vascular disorders,GENERAL MEDICAL HISTORY,Y,Y,2015-03-20,Y
CDISC01,MH,CDISC01-101-0001,3,Prior lung cancer surgery,Lobectomy,Surgical and medical procedures,ONCOLOGY HISTORY,N,Y,2022-08-10,N
```

### Concomitant Medications (CM)

```
Generate CM domain with supportive care medications
```

**Example Output:**
```csv
STUDYID,DOMAIN,USUBJID,CMSEQ,CMTRT,CMDECOD,CMCLAS,CMINDC,CMDOSE,CMDOSU,CMDOSFRQ,CMROUTE,CMSTDTC,CMENDTC,CMONGO
CDISC01,CM,CDISC01-101-0001,1,METFORMIN,METFORMIN,BIGUANIDES,Type 2 Diabetes,1000,mg,BID,ORAL,2018-06-20,,Y
CDISC01,CM,CDISC01-101-0001,2,ONDANSETRON,ONDANSETRON,SEROTONIN ANTAGONISTS,Nausea prophylaxis,8,mg,PRN,ORAL,2024-01-15,2024-07-15,N
CDISC01,CM,CDISC01-101-0001,3,DEXAMETHASONE,DEXAMETHASONE,CORTICOSTEROIDS,Infusion reaction prophylaxis,8,mg,ONCE,INTRAVENOUS,2024-01-15,2024-01-15,N
```

---

## ADaM Analysis Dataset Examples

### ADSL (Subject-Level)

```
Generate ADSL for Phase III trial with population flags
```

**Example Output:**
```csv
STUDYID,USUBJID,SITEID,TRT01P,TRT01A,TRTSDT,TRTEDT,AGE,AGEGR1,SEX,RACE,SAFFL,ITTFL,FASFL,EFFFL,EOSSTT,DCSREAS
CDISC01,CDISC01-101-0001,101,Pembrolizumab 200mg,Pembrolizumab 200mg,23391,23543,58,<65,M,WHITE,Y,Y,Y,Y,COMPLETED,
CDISC01,CDISC01-101-0002,101,Placebo,Placebo,23394,23456,52,<65,F,BLACK,Y,Y,Y,Y,DISCONTINUED,ADVERSE EVENT
CDISC01,CDISC01-102-0001,102,Pembrolizumab 200mg,Pembrolizumab 200mg,23396,23548,64,<65,M,ASIAN,Y,Y,Y,Y,COMPLETED,
```

### ADAE (Adverse Event Analysis)

```
Generate ADAE with treatment-emergent flags and first occurrence flags
```

**Example Output:**
```csv
STUDYID,USUBJID,AESEQ,TRTA,AEDECOD,AEBODSYS,AESEV,AESER,ASTDT,AENDT,ASTDY,TRTEMFL,AOCCFL,AOCCPFL,ASER01FL,ADRGIFL
CDISC01,CDISC01-101-0001,1,Pembrolizumab 200mg,Fatigue,General disorders,MILD,N,23408,23415,18,Y,Y,Y,N,Y
CDISC01,CDISC01-101-0001,2,Pembrolizumab 200mg,Diarrhoea,Gastrointestinal disorders,MODERATE,N,23425,23432,35,Y,Y,Y,N,Y
CDISC01,CDISC01-101-0001,3,Pembrolizumab 200mg,Fatigue,General disorders,MODERATE,N,23450,23458,60,Y,N,N,N,Y
```

### ADTTE (Time-to-Event)

```
Generate ADTTE for overall survival and progression-free survival
```

**Example Output:**
```csv
STUDYID,USUBJID,PARAMCD,PARAM,STARTDT,ADT,AVAL,AVALU,CNSR,EVNTDESC,CNSDTDSC,TRTA,ANL01FL
CDISC01,CDISC01-101-0001,OS,Overall Survival,23391,23755,365,DAYS,1,,ALIVE AT DATA CUTOFF,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0001,PFS,Progression-Free Survival,23391,23572,182,DAYS,0,DISEASE PROGRESSION,,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0002,OS,Overall Survival,23394,23650,257,DAYS,0,DEATH,,Placebo,Y
CDISC01,CDISC01-101-0002,PFS,Progression-Free Survival,23394,23512,119,DAYS,0,DISEASE PROGRESSION,,Placebo,Y
```

### ADLB (Laboratory Analysis)

```
Generate ADLB with baseline and change from baseline for ALT
```

**Example Output:**
```csv
STUDYID,USUBJID,PARAMCD,PARAM,AVISIT,AVISITN,ADT,AVAL,BASE,CHG,PCHG,ANRIND,BNRIND,ABLFL,TRTA
CDISC01,CDISC01-101-0001,ALT,Alanine Aminotransferase (U/L),BASELINE,0,23389,28,28,,,NORMAL,NORMAL,Y,Pembrolizumab 200mg
CDISC01,CDISC01-101-0001,ALT,Alanine Aminotransferase (U/L),WEEK 4,4,23417,45,28,17,60.7,HIGH,NORMAL,,Pembrolizumab 200mg
CDISC01,CDISC01-101-0001,ALT,Alanine Aminotransferase (U/L),WEEK 8,8,23445,38,28,10,35.7,NORMAL,NORMAL,,Pembrolizumab 200mg
```

---

## Safety Data Examples

### Dose-Limiting Toxicities

```
Generate DLTs for Phase I dose escalation
```

**What you get:**
- DLT events by dose level
- CTCAE grade assignments
- DLT evaluation window (typically 21-28 days)
- Attribution to study drug
- Dose cohort decisions

### Serious Adverse Events (SAEs)

```
Generate SAEs for Phase III with seriousness criteria
```

**Example SAE Record:**
```json
{
  "subject_id": "CDISC01-101-0001",
  "ae_term": "Pneumonitis",
  "meddra_pt": "Pneumonitis",
  "meddra_soc": "Respiratory, thoracic and mediastinal disorders",
  "onset_date": "2024-04-05",
  "severity": "SEVERE",
  "ctcae_grade": 3,
  "serious": "Y",
  "seriousness_criteria": {
    "death": "N",
    "life_threatening": "N",
    "hospitalization": "Y",
    "disability": "N",
    "congenital_anomaly": "N",
    "medically_important": "Y"
  },
  "causality": "RELATED",
  "action_taken": "DRUG WITHDRAWN",
  "outcome": "RECOVERED/RESOLVED WITH SEQUELAE",
  "resolution_date": "2024-05-20"
}
```

---

## Enrollment & Recruitment Examples

### Complete Screening Funnel

```
Generate a complete screening funnel for 200 randomized subjects
```

**Output includes:**
```json
{
  "funnel": {
    "identified": 450,
    "pre_screened": 380,
    "consented": 320,
    "screened": 310,
    "screen_failed": 95,
    "eligible": 215,
    "randomized": 200
  },
  "conversion_rates": {
    "pre_screen_to_consent": 0.84,
    "consent_to_screen": 0.97,
    "screen_to_eligible": 0.69,
    "eligible_to_randomized": 0.93,
    "overall": 0.44
  },
  "screen_failure_reasons": {
    "inclusion_not_met": 45,
    "exclusion_met": 35,
    "withdrew_consent": 10,
    "lost_to_followup": 5
  }
}
```

---

## Format Export Examples

### Export to SDTM

```
Generate a Phase III trial and export as SDTM datasets
```

**Output includes:**
- DM (Demographics)
- AE (Adverse Events)
- CM (Concomitant Medications)
- DS (Disposition)
- EX (Exposure)
- LB (Laboratory)
- MH (Medical History)
- VS (Vital Signs)

### Export to ADaM

```
Generate analysis datasets for a survival trial
```

**Output includes:**
- ADSL (Subject-Level)
- ADAE (Adverse Event Analysis)
- ADTTE (Time-to-Event Analysis)
- ADLB (Laboratory Analysis)
- ADRS (Response Analysis)

---

## Quick Reference

### Trial Phase Requests

| Request | Skill Used | Key Features |
|---------|------------|--------------|
| "Phase I 3+3 design" | phase1-dose-escalation.md | DLT-based escalation, MTD |
| "Phase I BOIN design" | phase1-dose-escalation.md | Bayesian intervals |
| "Phase I CRM" | phase1-dose-escalation.md | Model-based dosing |
| "Phase II Simon's two-stage" | phase2-proof-of-concept.md | Futility stopping |
| "Phase II MCP-Mod" | phase2-proof-of-concept.md | Dose-response modeling |
| "Phase III superiority" | phase3-pivotal.md | Primary efficacy |
| "Phase III non-inferiority" | phase3-pivotal.md | NI margin testing |

### Therapeutic Area Triggers

| Say This | Get This |
|----------|----------|
| "oncology", "cancer", "tumor" | RECIST, tumor response, survival |
| "cardiovascular", "heart", "MACE" | CV outcomes, cardiac biomarkers |
| "CNS", "neuro", "Alzheimer's" | Cognitive scales, imaging |
| "gene therapy", "CAR-T", "CGT" | Long-term follow-up, CRS, ICANS |

### SDTM Domain Triggers

| Domain | Trigger Phrases |
|--------|-----------------|
| DM | "demographics", "subject characteristics" |
| AE | "adverse events", "safety", "TEAEs" |
| CM | "concomitant medications", "prior meds" |
| LB | "laboratory", "labs", "chemistry", "hematology" |
| VS | "vital signs", "blood pressure", "vitals" |
| EX | "exposure", "dosing", "treatment administered" |
| DS | "disposition", "discontinuation", "completion" |
| MH | "medical history", "comorbidities" |

---

## Tips for Best Results

1. **Specify the phase** - "Phase I 3+3" is more specific than just "dose escalation"

2. **Include design parameters** - "Simon's two-stage with p0=0.10, p1=0.30"

3. **Request specific domains** - "Generate DM and AE domains"

4. **Use therapeutic area context** - "Oncology Phase III" activates RECIST patterns

5. **Ask for specific formats** - "as SDTM" or "as ADaM" for regulatory output

6. **Combine requests** - "Phase III NSCLC trial with 200 subjects, AE and LB domains, as SDTM"

---

## Dimensional Analytics Examples

TrialSim supports generating data in star schema format for BI analytics, dashboards, and operational reporting.

### Example 1: Basic Dimensional Model for DuckDB

```
Generate a Phase III oncology trial with 100 subjects as star schema for DuckDB
```

**What you get:**
- `dim_study` - Study attributes (phase, indication, sponsor)
- `dim_site` - 10 sites with geography
- `dim_subject` - 100 subjects with demographics
- `dim_treatment_arm` - 2 arms (experimental + placebo)
- `fact_enrollment` - Enrollment milestones per subject
- `fact_adverse_event` - Treatment-emergent AEs
- `fact_efficacy` - RECIST tumor assessments

### Example 2: Safety Surveillance Analytics

```
Generate 200 subjects for Phase III cardiovascular trial with full safety data 
in dimensional format. Include AE rates by SOC.
```

**What you get:**
- Complete star schema with MedDRA dimension
- Safety fact tables with CTCAE grades
- Query-ready structure for:
  - AE incidence by treatment arm
  - SAE rates by System Organ Class
  - Time-to-first-AE analysis

**Sample Query Output:**
```sql
-- Generated by Claude for safety surveillance
SELECT
    a.arm_name,
    m.soc_term as system_organ_class,
    COUNT(*) as ae_count,
    SUM(CASE WHEN f.is_serious THEN 1 ELSE 0 END) as sae_count,
    SUM(CASE WHEN f.ctcae_grade >= 3 THEN 1 ELSE 0 END) as grade_3_plus
FROM fact_adverse_event f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
JOIN dim_meddra m ON f.meddra_key = m.meddra_key
GROUP BY a.arm_name, m.soc_term
ORDER BY ae_count DESC;
```

### Example 3: Enrollment Operations Dashboard

```
Create a clinical trial operations dashboard dataset with enrollment velocity 
and site performance metrics. Load to DuckDB.
```

**What you get:**
- `fact_enrollment` with screening-to-randomization metrics
- `fact_visit` with protocol compliance metrics
- Site-level aggregations ready for dashboards:
  - Subjects screened/enrolled by site
  - Screen failure rates
  - Visit compliance percentages

### Example 4: Local DuckDB Analytics

```
Generate Phase II CNS trial with 80 subjects and full dimensional model for DuckDB
```

**What you get:**
1. Canonical trial data (JSON)
2. Dimensional model transformation
3. DuckDB CREATE TABLE statements
4. INSERT statements with all data
5. Sample analytics queries

**Enterprise Platforms (Future):** Direct loading to Databricks, Snowflake, and MotherDuck is planned for Phase 3. For now, export from DuckDB to your enterprise platform using standard ETL tools.

### Example 5: Cross-Product Analytics Setup

```
Generate 50 trial subjects with PatientSim linkage for cross-product analytics.
Include patient_mrn for EMR correlation.
```

**What you get:**
- `dim_subject` with `patient_mrn` field populated
- Matching `dim_patient` entries in PatientSim schema
- Ready for cross-product queries:
  - Correlate baseline disease burden with trial response
  - Link EMR medical history with trial adverse events
  - Analyze prior therapies impact on efficacy

### Example 6: Complete Trial Analytics Package

```
Generate a complete Phase III NSCLC trial package for analytics:
- 300 subjects (200 treatment, 100 placebo)
- 25 sites across NA and EU
- 12-month follow-up
- Full safety, efficacy, and operations data
- Star schema for DuckDB

Then show me:
1. Enrollment velocity by site
2. AE rates by arm and SOC
3. ORR by treatment arm
```

**Complete workflow:**
1. Claude generates comprehensive trial data
2. Creates star schema tables in DuckDB
3. Runs the requested analytics queries
4. Presents results in formatted tables

---

## See Also

### Phase Skills
- [Phase 1 Dose Escalation](../../skills/trialsim/phase1-dose-escalation.md)
- [Phase 2 Proof-of-Concept](../../skills/trialsim/phase2-proof-of-concept.md)
- [Phase 3 Pivotal](../../skills/trialsim/phase3-pivotal.md)

### SDTM Domain Skills
- [Demographics (DM)](../../skills/trialsim/domains/demographics-dm.md)
- [Adverse Events (AE)](../../skills/trialsim/domains/adverse-events-ae.md)
- [Laboratory (LB)](../../skills/trialsim/domains/laboratory-lb.md)
- [Vital Signs (VS)](../../skills/trialsim/domains/vital-signs-vs.md)
- [Exposure (EX)](../../skills/trialsim/domains/exposure-ex.md)
- [Disposition (DS)](../../skills/trialsim/domains/disposition-ds.md)
- [Medical History (MH)](../../skills/trialsim/domains/medical-history-mh.md)
- [Concomitant Medications (CM)](../../skills/trialsim/domains/concomitant-meds-cm.md)

### Therapeutic Area Skills
- [Oncology](../../skills/trialsim/therapeutic-areas/oncology.md)
- [Cardiovascular](../../skills/trialsim/therapeutic-areas/cardiovascular.md)
- [CNS/Neurology](../../skills/trialsim/therapeutic-areas/cns.md)
- [Cell & Gene Therapy](../../skills/trialsim/therapeutic-areas/cgt.md)

### Format Skills
- [CDISC SDTM Format](../../formats/cdisc-sdtm.md)
- [CDISC ADaM Format](../../formats/cdisc-adam.md)
- [Dimensional Analytics](../../formats/dimensional-analytics.md)

### Reference Materials
- [TrialSim Canonical Models](../../references/data-models.md#trialsim-models)
