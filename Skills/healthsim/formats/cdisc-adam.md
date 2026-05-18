---
name: cdisc-adam-format
description: |
  Transform TrialSim canonical data to CDISC ADaM analysis datasets for statistical 
  analysis and regulatory submission. Covers ADSL, ADAE, ADTTE, ADLB, ADTR, ADRS.
  Triggers: "ADaM", "analysis datasets", "statistical analysis", "efficacy analysis".
---

# CDISC ADaM Format

Transform TrialSim canonical JSON to CDISC Analysis Data Model (ADaM) datasets for statistical analysis.

---

## Overview

ADaM (Analysis Data Model) datasets are derived from SDTM and optimized for statistical analysis. They support traceability back to SDTM while providing analysis-ready structures.

### ADaM Principles

| Principle | Description |
|-----------|-------------|
| **Analysis-Ready** | Data structured for direct statistical analysis |
| **Traceability** | Clear derivation from SDTM source variables |
| **Clear Documentation** | Metadata in define.xml explains all derivations |
| **One Record Per** | Defined observation unit per dataset |

### ADaM Dataset Classes

| Class | Datasets | Description |
|-------|----------|-------------|
| **ADSL** | ADSL | Subject-level, one record per subject |
| **BDS** | ADAE, ADLB, ADTTE, ADTR, ADRS | Basic Data Structure, one record per parameter per time |
| **OCCDS** | ADAE (alternate) | Occurrence Data Structure for events |

---

## ADSL (Subject-Level Analysis Dataset)

**One record per subject** containing all baseline characteristics, treatment assignments, and population flags.

### Required Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| STUDYID | Study Identifier | DM.STUDYID | Direct |
| USUBJID | Unique Subject Identifier | DM.USUBJID | Direct |
| SUBJID | Subject Identifier | DM.SUBJID | Direct |
| SITEID | Study Site Identifier | DM.SITEID | Direct |
| ARM | Treatment Arm | DM.ARM | Direct |
| ARMCD | Arm Code | DM.ARMCD | Direct |
| ACTARM | Actual Treatment Arm | DM.ACTARM | Direct |
| ACTARMCD | Actual Arm Code | DM.ACTARMCD | Direct |

### Treatment Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| TRT01P | Planned Treatment for Period 01 | DM.ARM | Direct |
| TRT01PN | Planned Treatment (N) | Derived | Numeric code for TRT01P |
| TRT01A | Actual Treatment for Period 01 | DM.ACTARM | Direct |
| TRT01AN | Actual Treatment (N) | Derived | Numeric code for TRT01A |
| TRTSEQP | Planned Sequence of Treatments | Derived | For crossover designs |
| TRTSEQA | Actual Sequence of Treatments | Derived | For crossover designs |
| TRTSDT | Treatment Start Date | EX | First EXSTDTC |
| TRTEDT | Treatment End Date | EX | Last EXENDTC |
| TRTDURD | Treatment Duration (Days) | Derived | TRTEDT - TRTSDT + 1 |

### Demographic Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| AGE | Age | DM.AGE | Direct |
| AGEU | Age Units | DM.AGEU | Direct |
| AGEGR1 | Age Group 1 | Derived | <65 / >=65 |
| AGEGR1N | Age Group 1 (N) | Derived | 1=<65, 2=>=65 |
| SEX | Sex | DM.SEX | Direct |
| SEXN | Sex (N) | Derived | 1=M, 2=F |
| RACE | Race | DM.RACE | Direct |
| RACEN | Race (N) | Derived | Numeric code |
| ETHNIC | Ethnicity | DM.ETHNIC | Direct |
| COUNTRY | Country | DM.COUNTRY | Direct |

### Date Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| RFSTDTC | Subject Reference Start Date | DM.RFSTDTC | Direct |
| RFENDTC | Subject Reference End Date | DM.RFENDTC | Direct |
| RFICDT | Informed Consent Date | DM.RFICDTC | Numeric (SAS date) |
| RANDDT | Randomization Date | DS | DSSTDTC where DSDECOD='RANDOMIZED' |
| TRTSDT | Treatment Start Date | EX | First EXSTDTC (numeric) |
| TRTEDT | Treatment End Date | EX | Last EXENDTC (numeric) |
| EOSDT | End of Study Date | DS | DSSTDTC for study completion |
| EOSDY | Study Day of End of Study | Derived | EOSDT - TRTSDT + 1 |
| DTHDT | Death Date | DM.DTHDTC | Numeric (SAS date) |

### Population Flags

| Variable | Label | Derivation |
|----------|-------|------------|
| SAFFL | Safety Population Flag | Y if subject received at least one dose |
| ITTFL | Intent-to-Treat Flag | Y if subject was randomized |
| FASFL | Full Analysis Set Flag | Y if ITT with at least one post-baseline assessment |
| PPROTFL | Per-Protocol Population Flag | Y if no major protocol deviations |
| EFFFL | Efficacy Evaluable Flag | Y if has evaluable efficacy data |
| COMPLFL | Completer Flag | Y if completed study per protocol |
| DTHFL | Death Flag | Y if subject died |

### Disposition Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| EOSSTT | End of Study Status | DS | COMPLETED / DISCONTINUED |
| DCSREAS | Reason for Discontinuation | DS | DSDECOD for discontinuation |
| DCSREASP | Reason Specification | DS | DSTERM for OTHER |

### Baseline Variables (Examples)

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| BMIBL | Baseline BMI | VS | Weight/(Height^2) at baseline |
| WEIGHTBL | Baseline Weight (kg) | VS | VSSTRESN where VSTESTCD='WEIGHT' at baseline |
| HEIGHTBL | Baseline Height (cm) | VS | VSSTRESN where VSTESTCD='HEIGHT' at baseline |
| ECOGBL | Baseline ECOG Status | QS | Baseline ECOG score |
| DIAGTYPE | Diagnosis Type | MH | Primary diagnosis category |

### Derivation Rules

**Population Flags:**
```
SAFFL = "Y" if exists EX record with EXDOSE > 0
ITTFL = "Y" if exists DS record with DSDECOD = "RANDOMIZED"
FASFL = "Y" if ITTFL = "Y" AND exists post-baseline efficacy assessment
PPROTFL = "Y" if ITTFL = "Y" AND no major protocol deviations
```

**Age Group:**
```
AGEGR1 = "<65"  if AGE < 65
       = ">=65" if AGE >= 65
AGEGR1N = 1 if AGEGR1 = "<65"
        = 2 if AGEGR1 = ">=65"
```

### Transformation Example

**Canonical JSON Input:**
```json
{
  "subject": {
    "subject_id": "CDISC01-101-0001",
    "arm_code": "TRT",
    "arm_name": "Pembrolizumab 200mg",
    "first_dose_date": "2024-01-15",
    "last_dose_date": "2024-06-15",
    "consent_date": "2024-01-10",
    "randomization_date": "2024-01-14",
    "age_at_consent": 58,
    "sex": "M",
    "race": "WHITE",
    "end_of_study_status": "COMPLETED"
  }
}
```

**ADSL Output:**
```
STUDYID,USUBJID,SUBJID,SITEID,TRT01P,TRT01A,TRTSDT,TRTEDT,TRTDURD,AGE,AGEGR1,SEX,RACE,SAFFL,ITTFL,FASFL,EOSSTT
CDISC01,CDISC01-101-0001,0001,101,Pembrolizumab 200mg,Pembrolizumab 200mg,23391,23543,153,58,<65,M,WHITE,Y,Y,Y,COMPLETED
```

---

## ADAE (Adverse Event Analysis Dataset)

**One record per adverse event** with analysis flags and timing variables.

### Required Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| STUDYID | Study Identifier | AE.STUDYID | Direct |
| USUBJID | Unique Subject Identifier | AE.USUBJID | Direct |
| AESEQ | Sequence Number | AE.AESEQ | Direct |
| TRTA | Actual Treatment | ADSL.TRT01A | Merge |
| TRTAN | Actual Treatment (N) | ADSL.TRT01AN | Merge |
| AGE | Age | ADSL.AGE | Merge |
| AGEGR1 | Age Group | ADSL.AGEGR1 | Merge |
| SEX | Sex | ADSL.SEX | Merge |
| RACE | Race | ADSL.RACE | Merge |
| SAFFL | Safety Population Flag | ADSL.SAFFL | Merge |

### AE Identification Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| AETERM | Reported Term | AE.AETERM | Direct |
| AEDECOD | Dictionary-Derived Term | AE.AEDECOD | MedDRA PT |
| AEBODSYS | Body System or Organ Class | AE.AEBODSYS | MedDRA SOC |
| AESOC | Primary System Organ Class | AE.AESOC | Direct |
| AEHLT | High Level Term | AE.AEHLT | MedDRA HLT |
| AEHLGT | High Level Group Term | AE.AEHLGT | MedDRA HLGT |
| AELLT | Lowest Level Term | AE.AELLT | MedDRA LLT |
| AELLTCD | LLT Code | AE.AELLTCD | Direct |
| AEPTCD | PT Code | AE.AEPTCD | Direct |
| AESOCCD | SOC Code | AE.AESOCCD | Direct |

### AE Characteristic Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| AESEV | Severity/Intensity | AE.AESEV | Direct |
| AESEVN | Severity (N) | Derived | 1=MILD, 2=MODERATE, 3=SEVERE |
| AESER | Serious Event | AE.AESER | Direct |
| AESERN | Serious (N) | Derived | 0=N, 1=Y |
| AEREL | Causality | AE.AEREL | Direct |
| AERELN | Causality (N) | Derived | Numeric code |
| AEACN | Action Taken | AE.AEACN | Direct |
| AEOUT | Outcome | AE.AEOUT | Direct |
| AETOXGR | Toxicity Grade | AE.AETOXGR | CTCAE Grade |
| AETOXGRN | Toxicity Grade (N) | Derived | 1-5 |

### Timing Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| ASTDT | Analysis Start Date | AE.AESTDTC | Numeric (SAS date) |
| ASTDTF | Analysis Start Date Imputation | Derived | Imputation flag |
| AENDT | Analysis End Date | AE.AEENDTC | Numeric (SAS date) |
| AENDTF | Analysis End Date Imputation | Derived | Imputation flag |
| ASTDY | Analysis Start Day | Derived | ASTDT - TRTSDT + 1 |
| AENDY | Analysis End Day | Derived | AENDT - TRTSDT + 1 |
| ADURN | AE Duration (N) | Derived | AENDT - ASTDT + 1 |
| ADURU | AE Duration Units | Derived | "DAYS" |

### Analysis Flags

| Variable | Label | Derivation |
|----------|-------|------------|
| TRTEMFL | Treatment-Emergent Flag | Y if AE started on/after TRTSDT |
| PREFL | Pre-Treatment Flag | Y if AE started before TRTSDT |
| AETRTEM | Treatment-Emergent (text) | "TREATMENT-EMERGENT" / "NOT TREATMENT-EMERGENT" |
| AOCCFL | First Occurrence Flag | Y if first occurrence of this PT |
| AOCCSFL | First Occurrence in SOC Flag | Y if first AE in this SOC |
| AOCCPFL | First Occurrence per Parameter | Y if first per AEDECOD |
| AOCCxxFL | First Occurrence at xx Severity | Per severity level |
| ASER01FL | SAE Flag | Y if AESER = "Y" |
| ADRGIFL | Drug-Related Flag | Y if AEREL in (POSSIBLE, PROBABLE, DEFINITE) |
| ADTHFL | AE Led to Death | Y if AEOUT = "FATAL" |
| ADISCFL | AE Led to Discontinuation | Y if AEACN = "DRUG WITHDRAWN" |
| ADOSEFL | AE Led to Dose Modification | Y if AEACN in (DOSE REDUCED, DRUG INTERRUPTED) |

### Derivation Rules

**Treatment-Emergent:**
```
TRTEMFL = "Y" if:
  ASTDT >= TRTSDT 
  AND (ASTDT <= TRTEDT + 30 OR AENDT is missing)
  AND SAFFL = "Y"
```

**First Occurrence:**
```
AOCCFL = "Y" if this is the first occurrence of AEDECOD for this subject
        Sort by ASTDT, AESEQ ascending
        Flag first record per AEDECOD
```

### Transformation Example

**ADAE Output:**
```
STUDYID,USUBJID,AESEQ,TRTA,AEDECOD,AEBODSYS,AESEV,AESEVN,AESER,AEREL,ASTDT,AENDT,ASTDY,AENDY,ADURN,TRTEMFL,AOCCFL,SAFFL
CDISC01,CDISC01-101-0001,1,Pembrolizumab 200mg,Fatigue,General disorders,MILD,1,N,POSSIBLE,23408,23415,18,25,8,Y,Y,Y
CDISC01,CDISC01-101-0001,2,Pembrolizumab 200mg,Diarrhea,Gastrointestinal disorders,MODERATE,2,N,PROBABLE,23425,23432,35,42,8,Y,Y,Y
CDISC01,CDISC01-101-0001,3,Pembrolizumab 200mg,Pneumonitis,Respiratory disorders,SEVERE,3,Y,DEFINITE,23450,23465,60,75,16,Y,Y,Y
```

---

## ADTTE (Time-to-Event Analysis Dataset)

**One record per subject per parameter** for survival and time-to-event analyses.

### Required Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| STUDYID | Study Identifier | ADSL.STUDYID | Direct |
| USUBJID | Unique Subject Identifier | ADSL.USUBJID | Direct |
| PARAMCD | Parameter Code | Derived | Event type code |
| PARAM | Parameter | Derived | Event type description |
| PARAMN | Parameter (N) | Derived | Numeric code |

### Event Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| AVAL | Analysis Value | Derived | Time to event (days) |
| AVALU | Analysis Value Unit | Derived | "DAYS" |
| CNSR | Censor | Derived | 0=Event, 1=Censored |
| EVNTDESC | Event Description | Derived | Description of event |
| CNSDTDSC | Censor Date Description | Derived | Reason for censoring |

### Date Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| STARTDT | Time-to-Event Origin Date | ADSL.RANDDT | Randomization date |
| ADT | Analysis Date | Derived | Event or censor date |
| ADTF | Analysis Date Imputation Flag | Derived | Imputation method |

### Analysis Flags

| Variable | Label | Derivation |
|----------|-------|------------|
| ANL01FL | Analysis Flag 01 | Y if evaluable for primary analysis |
| ANL02FL | Analysis Flag 02 | Per-protocol population |

### Common Parameters

| PARAMCD | PARAM | Event Definition |
|---------|-------|------------------|
| OS | Overall Survival | Death from any cause |
| PFS | Progression-Free Survival | Disease progression or death |
| DOR | Duration of Response | Progression in responders |
| TTR | Time to Response | First confirmed response |
| TTDOSE | Time to Dose Modification | First dose reduction/interruption |
| EFS | Event-Free Survival | Progression, relapse, or death |

### Derivation Rules

**Overall Survival (OS):**
```
STARTDT = RANDDT (randomization date)

If subject died:
  ADT = DTHDT
  AVAL = ADT - STARTDT + 1
  CNSR = 0
  EVNTDESC = "DEATH"
Else:
  ADT = min(EOSDT, data cutoff date)
  AVAL = ADT - STARTDT + 1
  CNSR = 1
  CNSDTDSC = "ALIVE AT LAST CONTACT"
```

**Progression-Free Survival (PFS):**
```
STARTDT = RANDDT

If progression or death:
  ADT = min(progression date, death date)
  AVAL = ADT - STARTDT + 1
  CNSR = 0
  EVNTDESC = "DISEASE PROGRESSION" or "DEATH"
Else:
  ADT = last adequate tumor assessment date
  AVAL = ADT - STARTDT + 1
  CNSR = 1
  CNSDTDSC = "NO PROGRESSION AT LAST ASSESSMENT"
```

### Transformation Example

**ADTTE Output:**
```
STUDYID,USUBJID,PARAMCD,PARAM,STARTDT,ADT,AVAL,AVALU,CNSR,EVNTDESC,CNSDTDSC,TRTA,ANL01FL
CDISC01,CDISC01-101-0001,OS,Overall Survival,23390,23755,366,DAYS,1,,ALIVE AT DATA CUTOFF,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0001,PFS,Progression-Free Survival,23390,23572,183,DAYS,0,DISEASE PROGRESSION,,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0002,OS,Overall Survival,23392,23650,259,DAYS,0,DEATH,,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0002,PFS,Progression-Free Survival,23392,23512,121,DAYS,0,DISEASE PROGRESSION,,Pembrolizumab 200mg,Y
```

---

## ADLB (Laboratory Analysis Dataset)

**One record per subject per parameter per time point** for laboratory analysis.

### Required Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| STUDYID | Study Identifier | LB.STUDYID | Direct |
| USUBJID | Unique Subject Identifier | LB.USUBJID | Direct |
| PARAMCD | Parameter Code | LB.LBTESTCD | Direct |
| PARAM | Parameter | LB.LBTEST | With units |
| PARAMN | Parameter (N) | Derived | Numeric code |

### Result Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| AVAL | Analysis Value | LB.LBSTRESN | Numeric result |
| AVALC | Analysis Value (C) | LB.LBSTRESC | Character result |
| AVALU | Analysis Value Unit | LB.LBSTRESU | Standard units |
| BASE | Baseline Value | Derived | AVAL at baseline |
| BASEC | Baseline Value (C) | Derived | AVALC at baseline |
| CHG | Change from Baseline | Derived | AVAL - BASE |
| PCHG | Percent Change from Baseline | Derived | (CHG/BASE)*100 |

### Reference Range Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| A1LO | Analysis Range 1 Lower Limit | LB.LBSTNRLO | Standard range low |
| A1HI | Analysis Range 1 Upper Limit | LB.LBSTNRHI | Standard range high |
| ANRIND | Analysis Reference Range Ind | Derived | LOW/NORMAL/HIGH |
| BNRIND | Baseline Reference Range Ind | Derived | At baseline |
| SHIFT1 | Shift 1 | Derived | Baseline to post-baseline |

### Timing Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| ADT | Analysis Date | LB.LBDTC | Numeric date |
| ADTM | Analysis Date/Time | LB.LBDTC | With time |
| ADY | Analysis Day | Derived | ADT - TRTSDT + 1 |
| AVISIT | Analysis Visit | LB.VISIT | Visit name |
| AVISITN | Analysis Visit (N) | Derived | Visit number |
| ATPT | Analysis Timepoint | LB.LBTPT | Timepoint name |
| ATPTN | Analysis Timepoint (N) | Derived | Timepoint number |

### Analysis Flags

| Variable | Label | Derivation |
|----------|-------|------------|
| ABLFL | Baseline Record Flag | Y for baseline record |
| ANL01FL | Analysis Flag 01 | Y if evaluable |
| AENTMTFL | Treatment-Emergent Abnormality | Y if normal at baseline, abnormal post-baseline |
| LVOTFL | Last Value on Treatment | Y for last on-treatment value |
| WORSFL | Worst Post-Baseline Flag | Y for worst value |

### Shift Analysis

| SHIFT1 | Description |
|--------|-------------|
| LOW TO LOW | Low at baseline, low post-baseline |
| LOW TO NORMAL | Low at baseline, normal post-baseline |
| LOW TO HIGH | Low at baseline, high post-baseline |
| NORMAL TO LOW | Normal at baseline, low post-baseline |
| NORMAL TO NORMAL | Normal at baseline, normal post-baseline |
| NORMAL TO HIGH | Normal at baseline, high post-baseline |
| HIGH TO LOW | High at baseline, low post-baseline |
| HIGH TO NORMAL | High at baseline, normal post-baseline |
| HIGH TO HIGH | High at baseline, high post-baseline |

### Derivation Rules

**Baseline:**
```
ABLFL = "Y" for the last non-missing value before TRTSDT
If multiple on same day, use latest time
BASE = AVAL where ABLFL = "Y"
```

**Reference Range Indicator:**
```
ANRIND = "LOW"    if AVAL < A1LO
       = "NORMAL" if A1LO <= AVAL <= A1HI
       = "HIGH"   if AVAL > A1HI
```

**Change from Baseline:**
```
CHG = AVAL - BASE (only if both numeric)
PCHG = (CHG / BASE) * 100 (only if BASE != 0)
```

### Transformation Example

**ADLB Output:**
```
STUDYID,USUBJID,PARAMCD,PARAM,AVISIT,AVISITN,ADT,ADY,AVAL,AVALU,BASE,CHG,PCHG,A1LO,A1HI,ANRIND,BNRIND,SHIFT1,ABLFL,TRTA
CDISC01,CDISC01-101-0001,ALT,Alanine Aminotransferase (U/L),BASELINE,0,23389,-1,28,U/L,28,,,10,40,NORMAL,NORMAL,,Y,Pembrolizumab 200mg
CDISC01,CDISC01-101-0001,ALT,Alanine Aminotransferase (U/L),WEEK 4,4,23417,27,45,U/L,28,17,60.7,10,40,HIGH,NORMAL,NORMAL TO HIGH,,Pembrolizumab 200mg
CDISC01,CDISC01-101-0001,ALT,Alanine Aminotransferase (U/L),WEEK 8,8,23445,55,38,U/L,28,10,35.7,10,40,NORMAL,NORMAL,NORMAL TO NORMAL,,Pembrolizumab 200mg
```

---

## ADTR (Tumor Response Analysis Dataset)

**One record per subject per tumor per time point** for oncology tumor measurement analysis.

### Required Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| STUDYID | Study Identifier | TR.STUDYID | Direct |
| USUBJID | Unique Subject Identifier | TR.USUBJID | Direct |
| PARAMCD | Parameter Code | Derived | Lesion/sum identifier |
| PARAM | Parameter | Derived | Description |

### Tumor Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| TRLINKID | Tumor Link ID | TR.TRLINKID | Lesion identifier |
| TRGRPID | Tumor Group ID | TR.TRGRPID | Group identifier |
| TRLOC | Tumor Location | TR.TRLOC | Anatomic location |
| TRMETHOD | Assessment Method | TR.TRMETHOD | CT/MRI/etc. |

### Response Variables (RECIST 1.1)

| Variable | Label | Derivation |
|----------|-------|------------|
| AVAL | Analysis Value | Longest diameter (mm) |
| BASE | Baseline Value | AVAL at baseline |
| NADIR | Nadir Value | Minimum post-baseline AVAL |
| CHG | Change from Baseline | AVAL - BASE |
| PCHG | Percent Change from Baseline | (CHG/BASE)*100 |
| CHGNAD | Change from Nadir | AVAL - NADIR |
| PCHGNAD | Percent Change from Nadir | (CHGNAD/NADIR)*100 |

### Sum of Diameters (Target Lesions)

| PARAMCD | PARAM | Definition |
|---------|-------|------------|
| SUMDIAM | Sum of Diameters | Sum of longest diameters of target lesions |
| SUMNEWL | Sum Including New Lesions | SUMDIAM + new lesion measurements |

### Response Categories

| AVALC | Description | RECIST 1.1 Criteria |
|-------|-------------|---------------------|
| CR | Complete Response | Disappearance of all target lesions |
| PR | Partial Response | ≥30% decrease from baseline |
| SD | Stable Disease | Neither PR nor PD criteria met |
| PD | Progressive Disease | ≥20% increase from nadir + 5mm absolute |
| NE | Not Evaluable | Cannot be assessed |

---

## ADRS (Response Analysis Dataset)

**One record per subject per response assessment** for overall response analysis.

### Response Variables

| Variable | Label | Source | Derivation |
|----------|-------|--------|------------|
| PARAMCD | Parameter Code | Derived | Response type |
| PARAM | Parameter | Derived | Description |
| AVALC | Analysis Value (C) | Derived | Response category |
| AVAL | Analysis Value | Derived | Numeric code |

### Common Parameters

| PARAMCD | PARAM |
|---------|-------|
| OVRLRESP | Overall Response |
| BESTRESP | Best Overall Response |
| CBOR | Confirmed Best Overall Response |
| DCSREAS | Disease Control Status |

### Best Overall Response Derivation

```
BESTRESP hierarchy (in order of evaluation):
1. CR if any confirmed CR
2. PR if any confirmed PR (and no CR)
3. SD if stable ≥6 weeks (and no CR/PR)
4. PD if first assessment is PD
5. NE if none of above

CBOR = BESTRESP with confirmation requirement:
- CR requires confirmation ≥4 weeks later
- PR requires confirmation ≥4 weeks later
```

### Transformation Example

**ADRS Output:**
```
STUDYID,USUBJID,PARAMCD,PARAM,AVISIT,ADT,AVALC,AVAL,TRTA,ANL01FL
CDISC01,CDISC01-101-0001,OVRLRESP,Overall Response,WEEK 8,23445,PR,2,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0001,OVRLRESP,Overall Response,WEEK 16,23501,PR,2,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0001,OVRLRESP,Overall Response,WEEK 24,23557,PD,4,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0001,BESTRESP,Best Overall Response,,23501,PR,2,Pembrolizumab 200mg,Y
CDISC01,CDISC01-101-0001,CBOR,Confirmed Best Overall Response,,23501,PR,2,Pembrolizumab 200mg,Y
```

---

## Validation Rules

### Cross-Dataset Rules

| Rule | Description |
|------|-------------|
| ADSL-001 | Every USUBJID in BDS datasets must exist in ADSL |
| ADSL-002 | Population flags must be consistent across datasets |
| ADAE-001 | TRTEMFL requires TRTSDT from ADSL |
| ADTTE-001 | STARTDT must equal ADSL.RANDDT for randomized subjects |
| ADLB-001 | BASE must come from record with ABLFL="Y" |

### Variable Consistency

| Rule | Description |
|------|-------------|
| VAR-001 | USUBJID format must be consistent across all datasets |
| VAR-002 | Treatment variables must match ADSL values |
| VAR-003 | Date variables must be numeric SAS dates |
| VAR-004 | Derived flags must have supporting derivation |

---

## Related Skills

### Domain Skills
- [CDISC SDTM Format](cdisc-sdtm.md) - Source tabulation datasets
- [TrialSim SKILL](../skills/trialsim/SKILL.md) - Data generation

### Phase Skills
- [Phase 3 Pivotal](../skills/trialsim/phase3-pivotal.md) - Registration trial context

### Therapeutic Area Skills
- [Oncology](../skills/trialsim/therapeutic-areas/oncology.md) - Tumor response context

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-18 | Initial version with ADSL, ADAE, ADEFF |
| 2.0 | 2024-12-21 | Complete rewrite: Full ADSL, ADAE, ADTTE, ADLB, ADTR, ADRS |
