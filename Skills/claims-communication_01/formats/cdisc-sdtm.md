---
name: cdisc-sdtm-format
description: |
  Transform TrialSim canonical JSON to CDISC SDTM domain datasets for regulatory 
  submission. Covers all implemented domains: DM, AE, CM, LB, VS, EX, DS, MH.
  Triggers: "SDTM", "regulatory submission", "FDA format", "tabulation datasets".
---

# CDISC SDTM Format

Transform TrialSim canonical JSON to CDISC Study Data Tabulation Model (SDTM) datasets for regulatory submission.

---

## Overview

SDTM (Study Data Tabulation Model) is the FDA-required format for clinical trial data submissions to regulatory agencies. This skill maps TrialSim canonical entities to standard SDTM domain datasets.

### SDTM Principles

| Principle | Description |
|-----------|-------------|
| **One Record Per** | Each domain has a defined observation unit |
| **Standard Variables** | Identifier, topic, timing, qualifier variables |
| **Controlled Terminology** | CDISC-defined codelists for categorical values |
| **ISO 8601 Dates** | All dates in YYYY-MM-DD or YYYY-MM-DDThh:mm:ss format |
| **Character Data** | All variables stored as character (even numeric values) |

### Domain Classes

| Class | Domains | Observation Unit |
|-------|---------|------------------|
| **Special Purpose** | DM | One record per subject |
| **Events** | AE, DS, MH | One record per event |
| **Interventions** | CM, EX | One record per intervention record |
| **Findings** | LB, VS | One record per finding per time point |

---

## Identifier Variables

Common across all domains:

| Variable | Label | Description | Source |
|----------|-------|-------------|--------|
| STUDYID | Study Identifier | Unique study identifier | `Study.study_id` |
| DOMAIN | Domain Abbreviation | Two-character domain code | Fixed per domain |
| USUBJID | Unique Subject ID | Globally unique subject identifier | `Subject.subject_id` |
| --SEQ | Sequence Number | Domain-specific sequence | Auto-generated |

**USUBJID Construction:**
```
USUBJID = STUDYID + "-" + SITEID + "-" + SUBJID
Example: "CDISC01-101-0001"
```

---

## Demographics (DM)

**Class:** Special Purpose | **One record per subject**

### Variable Mapping

| SDTM Variable | Label | Source | CT/Format |
|---------------|-------|--------|-----------|
| STUDYID | Study Identifier | `Study.study_id` | |
| DOMAIN | Domain Abbreviation | "DM" | |
| USUBJID | Unique Subject Identifier | `Subject.subject_id` | |
| SUBJID | Subject Identifier for the Study | `Subject.subject_number` | |
| RFSTDTC | Subject Reference Start Date/Time | `Subject.first_dose_date` | ISO 8601 |
| RFENDTC | Subject Reference End Date/Time | `Subject.last_dose_date` | ISO 8601 |
| RFXSTDTC | Date/Time of First Study Treatment | `Subject.first_dose_date` | ISO 8601 |
| RFXENDTC | Date/Time of Last Study Treatment | `Subject.last_dose_date` | ISO 8601 |
| RFICDTC | Date/Time of Informed Consent | `Subject.consent_date` | ISO 8601 |
| RFPENDTC | Date/Time of End of Participation | `Subject.end_participation_date` | ISO 8601 |
| DTHDTC | Date/Time of Death | `Subject.death_date` | ISO 8601 |
| DTHFL | Subject Death Flag | Derived from death_date | Y/null |
| SITEID | Study Site Identifier | `Site.site_id` | |
| INVID | Investigator Identifier | `Site.investigator_id` | |
| INVNAM | Investigator Name | `Site.investigator_name` | |
| BRTHDTC | Date/Time of Birth | `Subject.birth_date` | ISO 8601 |
| AGE | Age | `Subject.age_at_consent` | |
| AGEU | Age Units | "YEARS" | AGEU CT |
| SEX | Sex | `Subject.sex` | SEX CT |
| RACE | Race | `Subject.race` | RACE CT |
| ETHNIC | Ethnicity | `Subject.ethnicity` | ETHNIC CT |
| ARMCD | Planned Arm Code | `Subject.arm_code` | |
| ARM | Description of Planned Arm | `Subject.arm_name` | |
| ACTARMCD | Actual Arm Code | `Subject.actual_arm_code` | |
| ACTARM | Description of Actual Arm | `Subject.actual_arm_name` | |
| COUNTRY | Country | `Site.country` | ISO 3166-1 |
| DMDTC | Date/Time of Collection | `Subject.demographics_date` | ISO 8601 |
| DMDY | Study Day of Collection | Derived | |

### Controlled Terminology

**SEX:**
| Code | Decode |
|------|--------|
| M | MALE |
| F | FEMALE |
| U | UNKNOWN |
| UNDIFFERENTIATED | UNDIFFERENTIATED |

**RACE:**
| Code |
|------|
| AMERICAN INDIAN OR ALASKA NATIVE |
| ASIAN |
| BLACK OR AFRICAN AMERICAN |
| NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER |
| WHITE |
| MULTIPLE |
| OTHER |
| UNKNOWN |
| NOT REPORTED |

**ETHNIC:**
| Code |
|------|
| HISPANIC OR LATINO |
| NOT HISPANIC OR LATINO |
| NOT REPORTED |
| UNKNOWN |

### Transformation Example

**Canonical JSON Input:**
```json
{
  "subject": {
    "subject_id": "CDISC01-101-0001",
    "subject_number": "0001",
    "consent_date": "2024-01-10",
    "first_dose_date": "2024-01-15",
    "last_dose_date": "2024-06-15",
    "age_at_consent": 52,
    "sex": "M",
    "race": "WHITE",
    "ethnicity": "NOT HISPANIC OR LATINO",
    "arm_code": "TRT",
    "arm_name": "Treatment 10mg"
  },
  "site": {
    "site_id": "101",
    "country": "USA",
    "investigator_name": "Dr. Smith"
  },
  "study": {
    "study_id": "CDISC01"
  }
}
```

**SDTM DM Output:**
```
STUDYID,DOMAIN,USUBJID,SUBJID,RFSTDTC,RFENDTC,RFICDTC,SITEID,INVNAM,AGE,AGEU,SEX,RACE,ETHNIC,ARMCD,ARM,COUNTRY
CDISC01,DM,CDISC01-101-0001,0001,2024-01-15,2024-06-15,2024-01-10,101,Dr. Smith,52,YEARS,M,WHITE,NOT HISPANIC OR LATINO,TRT,Treatment 10mg,USA
```

---

## Adverse Events (AE)

**Class:** Events | **One record per adverse event**

### Variable Mapping

| SDTM Variable | Label | Source | CT/Format |
|---------------|-------|--------|-----------|
| STUDYID | Study Identifier | `Study.study_id` | |
| DOMAIN | Domain Abbreviation | "AE" | |
| USUBJID | Unique Subject Identifier | `Subject.subject_id` | |
| AESEQ | Sequence Number | Auto-increment per subject | |
| AESPID | Sponsor-Defined Identifier | `AdverseEvent.event_id` | |
| AETERM | Reported Term for the AE | `AdverseEvent.reported_term` | |
| AEMODIFY | Modified Reported Term | `AdverseEvent.modified_term` | |
| AEDECOD | Dictionary-Derived Term | `AdverseEvent.meddra_pt` | MedDRA PT |
| AEBODSYS | Body System or Organ Class | `AdverseEvent.meddra_soc` | MedDRA SOC |
| AESOC | Primary SOC | `AdverseEvent.meddra_soc` | MedDRA SOC |
| AEHLGT | High Level Group Term | `AdverseEvent.meddra_hlgt` | MedDRA HLGT |
| AEHLT | High Level Term | `AdverseEvent.meddra_hlt` | MedDRA HLT |
| AELLTCD | LLT Code | `AdverseEvent.meddra_llt_code` | |
| AEPTCD | PT Code | `AdverseEvent.meddra_pt_code` | |
| AESEV | Severity/Intensity | `AdverseEvent.severity` | AESEV CT |
| AESER | Serious Event | `AdverseEvent.serious` | NY CT |
| AEACN | Action Taken with Study Treatment | `AdverseEvent.action_taken` | ACN CT |
| AEACNOTH | Other Action Taken | `AdverseEvent.other_action` | |
| AEREL | Causality | `AdverseEvent.causality` | AEREL CT |
| AEOUT | Outcome of AE | `AdverseEvent.outcome` | OUT CT |
| AESCAN | Involves Cancer | `AdverseEvent.involves_cancer` | NY CT |
| AESCONG | Congenital Anomaly | `AdverseEvent.congenital_anomaly` | NY CT |
| AESDISAB | Persist/Signif Disability | `AdverseEvent.disability` | NY CT |
| AESDTH | Results in Death | `AdverseEvent.results_in_death` | NY CT |
| AESHOSP | Requires Hospitalization | `AdverseEvent.hospitalization` | NY CT |
| AESLIFE | Is Life Threatening | `AdverseEvent.life_threatening` | NY CT |
| AESMIE | Other Medically Important | `AdverseEvent.medically_important` | NY CT |
| AECONTRT | Concomitant Treatment Given | `AdverseEvent.treatment_given` | NY CT |
| AETOXGR | Standard Toxicity Grade | `AdverseEvent.ctcae_grade` | AETOXGR CT |
| AESTDTC | Start Date/Time of AE | `AdverseEvent.start_date` | ISO 8601 |
| AEENDTC | End Date/Time of AE | `AdverseEvent.end_date` | ISO 8601 |
| AESTDY | Study Day of Start | Derived | |
| AEENDY | Study Day of End | Derived | |
| AEDUR | Duration of AE | Derived | ISO 8601 |
| AEENRF | End Relative to Reference Period | Derived | STENRF CT |
| AESTRF | Start Relative to Reference Period | Derived | STENRF CT |

### Controlled Terminology

**AESEV:**
| Code |
|------|
| MILD |
| MODERATE |
| SEVERE |

**ACN (Action Taken):**
| Code |
|------|
| DOSE NOT CHANGED |
| DOSE REDUCED |
| DRUG INTERRUPTED |
| DRUG WITHDRAWN |
| NOT APPLICABLE |
| UNKNOWN |

**AEREL (Causality):**
| Code |
|------|
| NOT RELATED |
| UNLIKELY |
| POSSIBLE |
| PROBABLE |
| DEFINITE |

**OUT (Outcome):**
| Code |
|------|
| RECOVERED/RESOLVED |
| RECOVERING/RESOLVING |
| NOT RECOVERED/NOT RESOLVED |
| RECOVERED/RESOLVED WITH SEQUELAE |
| FATAL |
| UNKNOWN |

### Transformation Example

**Canonical JSON Input:**
```json
{
  "adverse_event": {
    "event_id": "AE001",
    "reported_term": "headache",
    "meddra_pt": "Headache",
    "meddra_pt_code": "10019211",
    "meddra_soc": "Nervous system disorders",
    "severity": "MILD",
    "serious": "N",
    "causality": "POSSIBLE",
    "action_taken": "DOSE NOT CHANGED",
    "outcome": "RECOVERED/RESOLVED",
    "start_date": "2024-02-01",
    "end_date": "2024-02-03"
  }
}
```

**SDTM AE Output:**
```
STUDYID,DOMAIN,USUBJID,AESEQ,AETERM,AEDECOD,AEBODSYS,AESEV,AESER,AEREL,AEACN,AEOUT,AESTDTC,AEENDTC
CDISC01,AE,CDISC01-101-0001,1,headache,Headache,Nervous system disorders,MILD,N,POSSIBLE,DOSE NOT CHANGED,RECOVERED/RESOLVED,2024-02-01,2024-02-03
```

---

## Concomitant Medications (CM)

**Class:** Interventions | **One record per medication record**

### Variable Mapping

| SDTM Variable | Label | Source | CT/Format |
|---------------|-------|--------|-----------|
| STUDYID | Study Identifier | `Study.study_id` | |
| DOMAIN | Domain Abbreviation | "CM" | |
| USUBJID | Unique Subject Identifier | `Subject.subject_id` | |
| CMSEQ | Sequence Number | Auto-increment per subject | |
| CMSPID | Sponsor-Defined Identifier | `ConcomitantMed.med_id` | |
| CMTRT | Reported Name of Drug | `ConcomitantMed.medication_name` | |
| CMMODIFY | Modified Reported Name | `ConcomitantMed.modified_name` | |
| CMDECOD | Standardized Medication Name | `ConcomitantMed.who_drug_name` | WHO Drug |
| CMCLAS | Medication Class | `ConcomitantMed.atc_class` | ATC |
| CMCLASCD | Medication Class Code | `ConcomitantMed.atc_code` | ATC |
| CMINDC | Indication | `ConcomitantMed.indication` | |
| CMDOSE | Dose per Administration | `ConcomitantMed.dose` | |
| CMDOSU | Dose Units | `ConcomitantMed.dose_unit` | UNIT CT |
| CMDOSFRM | Dose Form | `ConcomitantMed.dose_form` | FRM CT |
| CMDOSFRQ | Dosing Frequency per Interval | `ConcomitantMed.frequency` | FREQ CT |
| CMROUTE | Route of Administration | `ConcomitantMed.route` | ROUTE CT |
| CMSTDTC | Start Date/Time of Medication | `ConcomitantMed.start_date` | ISO 8601 |
| CMENDTC | End Date/Time of Medication | `ConcomitantMed.end_date` | ISO 8601 |
| CMSTDY | Study Day of Start | Derived | |
| CMENDY | Study Day of End | Derived | |
| CMSTRF | Start Relative to Reference | `ConcomitantMed.start_relative` | STENRF CT |
| CMENRF | End Relative to Reference | `ConcomitantMed.end_relative` | STENRF CT |
| CMONGO | Ongoing | `ConcomitantMed.ongoing` | NY CT |
| CMPRTRT | Pre-Treatment Medication | Derived | NY CT |

### Transformation Example

**SDTM CM Output:**
```
STUDYID,DOMAIN,USUBJID,CMSEQ,CMTRT,CMDECOD,CMCLAS,CMINDC,CMDOSE,CMDOSU,CMDOSFRM,CMDOSFRQ,CMROUTE,CMSTDTC,CMENDTC,CMONGO
CDISC01,CM,CDISC01-101-0001,1,METFORMIN,METFORMIN,BIGUANIDES,Type 2 Diabetes,500,mg,TABLET,BID,ORAL,2020-03-15,,Y
CDISC01,CM,CDISC01-101-0001,2,LISINOPRIL,LISINOPRIL,ACE INHIBITORS,Hypertension,10,mg,TABLET,QD,ORAL,2019-06-01,,Y
```

---

## Laboratory Results (LB)

**Class:** Findings | **One record per test per time point**

### Variable Mapping

| SDTM Variable | Label | Source | CT/Format |
|---------------|-------|--------|-----------|
| STUDYID | Study Identifier | `Study.study_id` | |
| DOMAIN | Domain Abbreviation | "LB" | |
| USUBJID | Unique Subject Identifier | `Subject.subject_id` | |
| LBSEQ | Sequence Number | Auto-increment per subject | |
| LBTESTCD | Lab Test Short Name | `LabResult.test_code` | LBTESTCD CT |
| LBTEST | Lab Test Name | `LabResult.test_name` | LBTEST CT |
| LBCAT | Category for Lab Test | `LabResult.category` | |
| LBSCAT | Subcategory | `LabResult.subcategory` | |
| LBORRES | Result or Finding in Original Units | `LabResult.original_value` | |
| LBORRESU | Original Units | `LabResult.original_unit` | UNIT CT |
| LBORNRLO | Reference Range Lower Limit-Orig | `LabResult.ref_range_low` | |
| LBORNRHI | Reference Range Upper Limit-Orig | `LabResult.ref_range_high` | |
| LBSTRESC | Character Result/Finding in Std | `LabResult.standard_value` | |
| LBSTRESN | Numeric Result/Finding in Std | `LabResult.numeric_value` | |
| LBSTRESU | Standard Units | `LabResult.standard_unit` | UNIT CT |
| LBSTNRLO | Reference Range Lower Limit-Std | `LabResult.std_ref_low` | |
| LBSTNRHI | Reference Range Upper Limit-Std | `LabResult.std_ref_high` | |
| LBNRIND | Reference Range Indicator | Derived | NRIND CT |
| LBSPEC | Specimen Type | `LabResult.specimen` | SPEC CT |
| LBMETHOD | Method of Test | `LabResult.method` | METHOD CT |
| LBBLFL | Baseline Flag | Derived | NY CT |
| LBFAST | Fasting Status | `LabResult.fasting` | NY CT |
| LBDTC | Date/Time of Specimen Collection | `LabResult.collection_date` | ISO 8601 |
| LBDY | Study Day of Specimen Collection | Derived | |
| VISITNUM | Visit Number | `Visit.visit_number` | |
| VISIT | Visit Name | `Visit.visit_name` | |
| LBTOX | Toxicity | `LabResult.toxicity_term` | |
| LBTOXGR | Standard Toxicity Grade | `LabResult.ctcae_grade` | LBTOXGR CT |
| LBSTAT | Completion Status | `LabResult.status` | STAT CT |
| LBREASND | Reason Not Done | `LabResult.reason_not_done` | |
| LBLOINC | LOINC Code | `LabResult.loinc_code` | LOINC |

### Common LBTESTCD Values

| LBTESTCD | LBTEST | LBCAT | Typical Units |
|----------|--------|-------|---------------|
| ALT | Alanine Aminotransferase | CHEMISTRY | U/L |
| AST | Aspartate Aminotransferase | CHEMISTRY | U/L |
| BILI | Bilirubin | CHEMISTRY | mg/dL |
| CREAT | Creatinine | CHEMISTRY | mg/dL |
| GGT | Gamma Glutamyl Transferase | CHEMISTRY | U/L |
| GLUC | Glucose | CHEMISTRY | mg/dL |
| HBA1C | Hemoglobin A1C | CHEMISTRY | % |
| WBC | Leukocytes | HEMATOLOGY | 10^9/L |
| RBC | Erythrocytes | HEMATOLOGY | 10^12/L |
| HGB | Hemoglobin | HEMATOLOGY | g/dL |
| HCT | Hematocrit | HEMATOLOGY | % |
| PLAT | Platelets | HEMATOLOGY | 10^9/L |
| NEUT | Neutrophils | HEMATOLOGY | 10^9/L |

### Transformation Example

**SDTM LB Output:**
```
STUDYID,DOMAIN,USUBJID,LBSEQ,LBTESTCD,LBTEST,LBCAT,LBORRES,LBORRESU,LBORNRLO,LBORNRHI,LBSTRESN,LBSTRESU,LBNRIND,LBBLFL,VISITNUM,VISIT,LBDTC
CDISC01,LB,CDISC01-101-0001,1,ALT,Alanine Aminotransferase,CHEMISTRY,35,U/L,10,40,35,U/L,NORMAL,Y,1,SCREENING,2024-01-10
CDISC01,LB,CDISC01-101-0001,2,ALT,Alanine Aminotransferase,CHEMISTRY,42,U/L,10,40,42,U/L,HIGH,N,5,WEEK 4,2024-02-12
CDISC01,LB,CDISC01-101-0001,3,CREAT,Creatinine,CHEMISTRY,0.9,mg/dL,0.7,1.2,0.9,mg/dL,NORMAL,Y,1,SCREENING,2024-01-10
```

---

## Vital Signs (VS)

**Class:** Findings | **One record per measurement per time point**

### Variable Mapping

| SDTM Variable | Label | Source | CT/Format |
|---------------|-------|--------|-----------|
| STUDYID | Study Identifier | `Study.study_id` | |
| DOMAIN | Domain Abbreviation | "VS" | |
| USUBJID | Unique Subject Identifier | `Subject.subject_id` | |
| VSSEQ | Sequence Number | Auto-increment per subject | |
| VSTESTCD | Vital Signs Test Short Name | `VitalSign.test_code` | VSTESTCD CT |
| VSTEST | Vital Signs Test Name | `VitalSign.test_name` | VSTEST CT |
| VSPOS | Vital Signs Position of Subject | `VitalSign.position` | POSITION CT |
| VSORRES | Result or Finding in Original Units | `VitalSign.original_value` | |
| VSORRESU | Original Units | `VitalSign.original_unit` | UNIT CT |
| VSSTRESC | Character Result/Finding in Std | `VitalSign.standard_value` | |
| VSSTRESN | Numeric Result/Finding in Std | `VitalSign.numeric_value` | |
| VSSTRESU | Standard Units | `VitalSign.standard_unit` | UNIT CT |
| VSSTAT | Completion Status | `VitalSign.status` | STAT CT |
| VSREASND | Reason Not Done | `VitalSign.reason_not_done` | |
| VSLOC | Location of Measurement | `VitalSign.location` | LOC CT |
| VSBLFL | Baseline Flag | Derived | NY CT |
| VSDTC | Date/Time of Measurements | `VitalSign.measurement_date` | ISO 8601 |
| VSDY | Study Day of Measurements | Derived | |
| VISITNUM | Visit Number | `Visit.visit_number` | |
| VISIT | Visit Name | `Visit.visit_name` | |
| VSTPT | Planned Time Point Name | `VitalSign.timepoint` | |
| VSTPTNUM | Planned Time Point Number | `VitalSign.timepoint_num` | |

### VSTESTCD Values

| VSTESTCD | VSTEST | Standard Unit |
|----------|--------|---------------|
| SYSBP | Systolic Blood Pressure | mmHg |
| DIABP | Diastolic Blood Pressure | mmHg |
| PULSE | Pulse Rate | beats/min |
| RESP | Respiratory Rate | breaths/min |
| TEMP | Temperature | C |
| HEIGHT | Height | cm |
| WEIGHT | Weight | kg |
| BMI | Body Mass Index | kg/m2 |

### Transformation Example

**SDTM VS Output:**
```
STUDYID,DOMAIN,USUBJID,VSSEQ,VSTESTCD,VSTEST,VSPOS,VSORRES,VSORRESU,VSSTRESN,VSSTRESU,VSBLFL,VISITNUM,VISIT,VSDTC
CDISC01,VS,CDISC01-101-0001,1,SYSBP,Systolic Blood Pressure,SITTING,128,mmHg,128,mmHg,Y,1,SCREENING,2024-01-10
CDISC01,VS,CDISC01-101-0001,2,DIABP,Diastolic Blood Pressure,SITTING,82,mmHg,82,mmHg,Y,1,SCREENING,2024-01-10
CDISC01,VS,CDISC01-101-0001,3,PULSE,Pulse Rate,SITTING,72,beats/min,72,beats/min,Y,1,SCREENING,2024-01-10
CDISC01,VS,CDISC01-101-0001,4,WEIGHT,Weight,,78.5,kg,78.5,kg,Y,1,SCREENING,2024-01-10
```

---

## Exposure (EX)

**Class:** Interventions | **One record per exposure record**

### Variable Mapping

| SDTM Variable | Label | Source | CT/Format |
|---------------|-------|--------|-----------|
| STUDYID | Study Identifier | `Study.study_id` | |
| DOMAIN | Domain Abbreviation | "EX" | |
| USUBJID | Unique Subject Identifier | `Subject.subject_id` | |
| EXSEQ | Sequence Number | Auto-increment per subject | |
| EXTRT | Name of Treatment | `Exposure.treatment_name` | |
| EXCAT | Category of Treatment | `Exposure.category` | |
| EXDOSE | Dose per Administration | `Exposure.dose` | |
| EXDOSU | Dose Units | `Exposure.dose_unit` | UNIT CT |
| EXDOSFRM | Dose Form | `Exposure.dose_form` | FRM CT |
| EXDOSFRQ | Dosing Frequency per Interval | `Exposure.frequency` | FREQ CT |
| EXROUTE | Route of Administration | `Exposure.route` | ROUTE CT |
| EXLOT | Lot Number | `Exposure.lot_number` | |
| EXADJ | Reason for Dose Adjustment | `Exposure.adjustment_reason` | |
| EXSTDTC | Start Date/Time of Treatment | `Exposure.start_date` | ISO 8601 |
| EXENDTC | End Date/Time of Treatment | `Exposure.end_date` | ISO 8601 |
| EXSTDY | Study Day of Start | Derived | |
| EXENDY | Study Day of End | Derived | |
| EXDUR | Duration | Derived | ISO 8601 |
| EXTRTV | Treatment Vehicle | `Exposure.vehicle` | |
| EXVAMT | Infusion Volume | `Exposure.infusion_volume` | |
| EXVAMTU | Infusion Volume Units | `Exposure.infusion_unit` | UNIT CT |
| VISITNUM | Visit Number | `Visit.visit_number` | |
| VISIT | Visit Name | `Visit.visit_name` | |
| EPOCH | Epoch | `Visit.epoch` | EPOCH CT |

### Controlled Terminology

**ROUTE:**
| Code |
|------|
| ORAL |
| INTRAVENOUS |
| SUBCUTANEOUS |
| INTRAMUSCULAR |
| TOPICAL |
| TRANSDERMAL |
| INHALATION |

**FREQ (Dosing Frequency):**
| Code | Decode |
|------|--------|
| QD | Once Daily |
| BID | Twice Daily |
| TID | Three Times Daily |
| QID | Four Times Daily |
| Q3W | Every 3 Weeks |
| Q4W | Every 4 Weeks |
| ONCE | Once |

### Transformation Example

**SDTM EX Output:**
```
STUDYID,DOMAIN,USUBJID,EXSEQ,EXTRT,EXDOSE,EXDOSU,EXDOSFRM,EXDOSFRQ,EXROUTE,EXSTDTC,EXENDTC,EXADJ,EPOCH
CDISC01,EX,CDISC01-101-0001,1,PEMBROLIZUMAB,200,mg,INJECTION,Q3W,INTRAVENOUS,2024-01-15,2024-01-15,,TREATMENT
CDISC01,EX,CDISC01-101-0001,2,PEMBROLIZUMAB,200,mg,INJECTION,Q3W,INTRAVENOUS,2024-02-05,2024-02-05,,TREATMENT
CDISC01,EX,CDISC01-101-0001,3,PEMBROLIZUMAB,200,mg,INJECTION,Q3W,INTRAVENOUS,2024-02-26,2024-02-26,DOSE DELAY DUE TO AE,TREATMENT
```

---

## Disposition (DS)

**Class:** Events | **One record per disposition event**

### Variable Mapping

| SDTM Variable | Label | Source | CT/Format |
|---------------|-------|--------|-----------|
| STUDYID | Study Identifier | `Study.study_id` | |
| DOMAIN | Domain Abbreviation | "DS" | |
| USUBJID | Unique Subject Identifier | `Subject.subject_id` | |
| DSSEQ | Sequence Number | Auto-increment per subject | |
| DSSPID | Sponsor-Defined Identifier | `Disposition.event_id` | |
| DSTERM | Reported Term for Disposition Event | `Disposition.reported_term` | |
| DSDECOD | Standardized Disposition Term | `Disposition.standard_term` | DSDECOD CT |
| DSCAT | Category for Disposition Event | `Disposition.category` | DSCAT CT |
| DSSCAT | Subcategory for Disposition Event | `Disposition.subcategory` | |
| DSEPOCH | Epoch of Disposition Event | `Disposition.epoch` | EPOCH CT |
| DSSTDTC | Start Date/Time of Disposition | `Disposition.event_date` | ISO 8601 |
| DSSTDY | Study Day of Start | Derived | |

### Controlled Terminology

**DSCAT:**
| Code |
|------|
| DISPOSITION EVENT |
| PROTOCOL MILESTONE |
| OTHER EVENT |

**DSSCAT (Subcategory):**
| Code |
|------|
| STUDY PARTICIPATION |
| TREATMENT |
| STUDY COMPLETION |

**DSDECOD (Protocol Milestones):**
| Code |
|------|
| INFORMED CONSENT OBTAINED |
| RANDOMIZED |
| TREATMENT STARTED |
| TREATMENT COMPLETED |
| STUDY COMPLETED |

**DSDECOD (Discontinuation Reasons):**
| Code |
|------|
| ADVERSE EVENT |
| DEATH |
| LACK OF EFFICACY |
| LOST TO FOLLOW-UP |
| PHYSICIAN DECISION |
| PROTOCOL DEVIATION |
| PROTOCOL VIOLATION |
| WITHDRAWAL BY SUBJECT |
| STUDY TERMINATED BY SPONSOR |
| COMPLETED |

### Transformation Example

**SDTM DS Output:**
```
STUDYID,DOMAIN,USUBJID,DSSEQ,DSTERM,DSDECOD,DSCAT,DSSCAT,DSSTDTC
CDISC01,DS,CDISC01-101-0001,1,Informed Consent Obtained,INFORMED CONSENT OBTAINED,PROTOCOL MILESTONE,STUDY PARTICIPATION,2024-01-10
CDISC01,DS,CDISC01-101-0001,2,Randomized,RANDOMIZED,PROTOCOL MILESTONE,STUDY PARTICIPATION,2024-01-15
CDISC01,DS,CDISC01-101-0001,3,Treatment Started,TREATMENT STARTED,PROTOCOL MILESTONE,TREATMENT,2024-01-15
CDISC01,DS,CDISC01-101-0001,4,Completed Study,COMPLETED,DISPOSITION EVENT,STUDY COMPLETION,2024-07-15
```

---

## Medical History (MH)

**Class:** Events | **One record per medical history event**

### Variable Mapping

| SDTM Variable | Label | Source | CT/Format |
|---------------|-------|--------|-----------|
| STUDYID | Study Identifier | `Study.study_id` | |
| DOMAIN | Domain Abbreviation | "MH" | |
| USUBJID | Unique Subject Identifier | `Subject.subject_id` | |
| MHSEQ | Sequence Number | Auto-increment per subject | |
| MHSPID | Sponsor-Defined Identifier | `MedHistory.condition_id` | |
| MHTERM | Reported Term for Medical History | `MedHistory.reported_term` | |
| MHMODIFY | Modified Reported Term | `MedHistory.modified_term` | |
| MHDECOD | Dictionary-Derived Term | `MedHistory.meddra_pt` | MedDRA PT |
| MHBODSYS | Body System or Organ Class | `MedHistory.meddra_soc` | MedDRA SOC |
| MHCAT | Category for Medical History | `MedHistory.category` | |
| MHSCAT | Subcategory for Medical History | `MedHistory.subcategory` | |
| MHPRESP | Pre-Specified | `MedHistory.pre_specified` | NY CT |
| MHOCCUR | Medical History Occurrence | `MedHistory.occurred` | NY CT |
| MHSTDTC | Start Date/Time of History | `MedHistory.start_date` | ISO 8601 |
| MHENDTC | End Date/Time of History | `MedHistory.end_date` | ISO 8601 |
| MHSTTPT | Start Relative to Reference | `MedHistory.start_reference` | |
| MHENTPT | End Relative to Reference | `MedHistory.end_reference` | |
| MHENRF | End Relative to Reference Period | Derived | STENRF CT |
| MHONGO | Ongoing | `MedHistory.ongoing` | NY CT |
| MHDY | Study Day of Start | Derived | |

### Controlled Terminology

**MHENRF (End Relative to Reference):**
| Code | Description |
|------|-------------|
| BEFORE | Ended before reference period |
| DURING | Ended during reference period |
| AFTER | Ended after reference period |
| ONGOING | Still ongoing |

### Transformation Example

**SDTM MH Output:**
```
STUDYID,DOMAIN,USUBJID,MHSEQ,MHTERM,MHDECOD,MHBODSYS,MHCAT,MHPRESP,MHOCCUR,MHSTDTC,MHENDTC,MHONGO
CDISC01,MH,CDISC01-101-0001,1,Type 2 Diabetes,Type 2 diabetes mellitus,Metabolism and nutrition disorders,GENERAL MEDICAL HISTORY,Y,Y,2018-06-15,,Y
CDISC01,MH,CDISC01-101-0001,2,Hypertension,Hypertension,Vascular disorders,GENERAL MEDICAL HISTORY,Y,Y,2019-03-20,,Y
CDISC01,MH,CDISC01-101-0001,3,Appendectomy,Appendicectomy,Surgical and medical procedures,SURGICAL HISTORY,N,Y,2005-08-10,2005-08-12,N
```

---

## Validation Rules

### Domain-Level Rules

| Rule | Description | Applies To |
|------|-------------|------------|
| STUDYID-001 | STUDYID must be consistent across all domains | All |
| USUBJID-001 | USUBJID must be unique and consistent | All |
| DOMAIN-001 | DOMAIN must be two characters | All |
| SEQ-001 | --SEQ must be unique within USUBJID and DOMAIN | All |
| DATE-001 | All dates must be ISO 8601 format | All |
| DATE-002 | Start date must be ≤ end date | AE, CM, EX, MH |

### Cross-Domain Rules

| Rule | Description |
|------|-------------|
| DM-AE-001 | AE.AESTDTC should be ≥ DM.RFSTDTC for treatment-emergent AEs |
| DM-EX-001 | EX dates must fall within DM.RFSTDTC to DM.RFENDTC |
| DM-DS-001 | DS completion date should match DM.RFPENDTC |
| EX-AE-001 | Dose modifications in EX should correlate with AEs |
| MH-CM-001 | Chronic MH conditions should have corresponding ongoing CMs |

### Controlled Terminology Rules

| Rule | Description |
|------|-------------|
| CT-001 | SEX values must be from SEX codelist |
| CT-002 | RACE values must be from RACE codelist |
| CT-003 | All --DECOD values must be from appropriate dictionary |
| CT-004 | Route values must be from ROUTE codelist |
| CT-005 | Unit values must be from UNIT codelist |

---

## Related Skills

### Domain Skills
- [demographics-dm.md](../skills/trialsim/domains/demographics-dm.md)
- [adverse-events-ae.md](../skills/trialsim/domains/adverse-events-ae.md)
- [concomitant-meds-cm.md](../skills/trialsim/domains/concomitant-meds-cm.md)
- [laboratory-lb.md](../skills/trialsim/domains/laboratory-lb.md)
- [vital-signs-vs.md](../skills/trialsim/domains/vital-signs-vs.md)
- [exposure-ex.md](../skills/trialsim/domains/exposure-ex.md)
- [disposition-ds.md](../skills/trialsim/domains/disposition-ds.md)
- [medical-history-mh.md](../skills/trialsim/domains/medical-history-mh.md)

### Format Skills
- [CDISC ADaM Format](cdisc-adam.md) - Analysis datasets

### Reference
- [TrialSim SKILL](../skills/trialsim/SKILL.md) - Source data generation
- [Clinical Trials Domain](../skills/trialsim/clinical-trials-domain.md) - Domain knowledge

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-18 | Initial version with DM, AE, CM, SV mappings |
| 2.0 | 2024-12-21 | Complete rewrite: Added LB, VS, EX, DS, MH; full CT references; validation rules |
