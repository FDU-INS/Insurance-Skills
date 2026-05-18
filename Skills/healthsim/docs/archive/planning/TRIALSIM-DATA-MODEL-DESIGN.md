# TrialSim Data Model Design

## Overview

This document defines the canonical entity schemas and dimensional analytics model for TrialSim. Following HealthSim's established pattern, these are **loosely coupled**:

- **Canonical Model**: Source-of-truth JSON entities used for generation and transformation to output formats (SDTM, ADaM, FHIR ResearchStudy)
- **Dimensional Model**: Star schema optimized for analytics platforms (DuckDB, Databricks)

Users can request either format independently.

---

## Part 1: Canonical Entity Schemas

### Design Principles

1. **Extend Person**: Subject extends the core Person model (like Patient, Member, RxMember)
2. **Trial Context**: All entities reference study_id and site_id for context
3. **CDISC-Aligned**: Field names are readable but map cleanly to SDTM variables
4. **Referential Integrity**: Foreign keys to related entities documented

### Entity Hierarchy

```
Person (core)
├── Patient (PatientSim)
├── Member (MemberSim)
├── RxMember (RxMemberSim)
└── Subject (TrialSim) ←── NEW
    └── Links to Patient for medical history

Study
├── Site (1:M)
├── TreatmentArm (1:M)
├── VisitSchedule (1:M)
└── Subject (via Site, 1:M)
    ├── Randomization (1:1)
    ├── ActualVisit (1:M)
    │   ├── VitalSign (1:M)
    │   ├── LabResult (1:M)
    │   └── EfficacyAssessment (1:M)
    ├── AdverseEvent (1:M)
    ├── ConcomitantMed (1:M)
    ├── Exposure (1:M)
    ├── ProtocolDeviation (1:M)
    └── DispositionEvent (1:M)
```

---

### Study

The clinical trial protocol definition.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Study",
  "type": "object",
  "required": ["study_id", "protocol_title", "phase", "status"],
  "properties": {
    "study_id": {
      "type": "string",
      "description": "Unique study identifier (maps to STUDYID in SDTM)",
      "pattern": "^[A-Z0-9-]+$",
      "examples": ["ABC-123-001", "ONCO-2024-PH3"]
    },
    "protocol_title": {
      "type": "string",
      "description": "Full protocol title"
    },
    "protocol_number": {
      "type": "string",
      "description": "Sponsor's protocol number"
    },
    "phase": {
      "type": "string",
      "enum": ["Phase 1", "Phase 1/2", "Phase 2", "Phase 2/3", "Phase 3", "Phase 4"],
      "description": "Clinical trial phase"
    },
    "therapeutic_area": {
      "type": "string",
      "description": "Primary therapeutic area",
      "examples": ["Oncology", "Cardiovascular", "CNS", "Immunology"]
    },
    "indication": {
      "type": "string",
      "description": "Target disease/condition",
      "examples": ["Non-Small Cell Lung Cancer", "Heart Failure", "Alzheimer's Disease"]
    },
    "sponsor": {
      "type": "string",
      "description": "Sponsor organization name"
    },
    "status": {
      "type": "string",
      "enum": ["Planning", "Recruiting", "Active", "Completed", "Terminated", "Suspended"],
      "description": "Current study status"
    },
    "study_type": {
      "type": "string",
      "enum": ["Interventional", "Observational", "Expanded Access"],
      "default": "Interventional"
    },
    "design": {
      "type": "object",
      "properties": {
        "allocation": {
          "type": "string",
          "enum": ["Randomized", "Non-Randomized", "N/A"]
        },
        "intervention_model": {
          "type": "string",
          "enum": ["Parallel", "Crossover", "Sequential", "Single Group", "Factorial"]
        },
        "masking": {
          "type": "string",
          "enum": ["None (Open Label)", "Single", "Double", "Triple", "Quadruple"]
        },
        "primary_purpose": {
          "type": "string",
          "enum": ["Treatment", "Prevention", "Diagnostic", "Supportive Care", "Screening"]
        }
      }
    },
    "enrollment_target": {
      "type": "integer",
      "minimum": 1,
      "description": "Target number of subjects"
    },
    "start_date": {
      "type": "string",
      "format": "date",
      "description": "First subject first visit (FSFV) target"
    },
    "primary_completion_date": {
      "type": "string",
      "format": "date",
      "description": "Primary endpoint data collection complete"
    },
    "study_completion_date": {
      "type": "string",
      "format": "date",
      "description": "Last subject last visit (LSLV) target"
    }
  }
}
```

---

### Site

Investigational site conducting the trial.

```json
{
  "title": "Site",
  "type": "object",
  "required": ["site_id", "study_id", "site_name", "country"],
  "properties": {
    "site_id": {
      "type": "string",
      "description": "Site number within study",
      "pattern": "^[0-9]{3,4}$",
      "examples": ["001", "0101", "2001"]
    },
    "study_id": {
      "type": "string",
      "description": "Reference to parent Study"
    },
    "site_name": {
      "type": "string",
      "description": "Institution/facility name"
    },
    "facility_id": {
      "type": "string",
      "description": "Reference to NetworkSim Facility (if cross-product)"
    },
    "country": {
      "type": "string",
      "pattern": "^[A-Z]{2,3}$",
      "description": "ISO 3166-1 alpha-2/3 country code"
    },
    "region": {
      "type": "string",
      "description": "Geographic region for stratification",
      "examples": ["North America", "Europe", "Asia-Pacific"]
    },
    "principal_investigator": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "npi": { "type": "string", "pattern": "^[0-9]{10}$" },
        "specialty": { "type": "string" }
      }
    },
    "status": {
      "type": "string",
      "enum": ["Selected", "In Startup", "Active", "Closed", "Terminated"]
    },
    "activation_date": {
      "type": "string",
      "format": "date",
      "description": "Date site opened for enrollment"
    },
    "enrollment_target": {
      "type": "integer",
      "description": "Site-level enrollment target"
    },
    "enrollment_actual": {
      "type": "integer",
      "description": "Current enrolled count"
    }
  }
}
```

---

### Subject (extends Person)

Enrolled trial participant. Extends the core Person model.

```json
{
  "title": "Subject",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "required": ["subject_id", "study_id", "site_id", "informed_consent_date"],
  "properties": {
    "subject_id": {
      "type": "string",
      "description": "Subject identifier within site (last part of USUBJID)",
      "pattern": "^[0-9]{4}$",
      "examples": ["0001", "0023"]
    },
    "usubjid": {
      "type": "string",
      "description": "Unique Subject ID: STUDYID-SITEID-SUBJID",
      "pattern": "^[A-Z0-9-]+-[0-9]+-[0-9]+$",
      "examples": ["ABC-123-001-001-0001"]
    },
    "study_id": {
      "type": "string",
      "description": "Reference to Study"
    },
    "site_id": {
      "type": "string",
      "description": "Reference to Site"
    },
    "patient_ref": {
      "type": "string",
      "description": "Reference to PatientSim Patient (MRN) for medical history"
    },
    "screening_id": {
      "type": "string",
      "description": "Pre-randomization screening number"
    },
    "screening_date": {
      "type": "string",
      "format": "date",
      "description": "Date of screening visit"
    },
    "informed_consent_date": {
      "type": "string",
      "format": "date",
      "description": "Date informed consent signed (RFICDTC)"
    },
    "randomization_date": {
      "type": "string",
      "format": "date",
      "description": "Date of randomization (if randomized)"
    },
    "treatment_arm": {
      "type": "string",
      "description": "Assigned treatment arm code"
    },
    "status": {
      "type": "string",
      "enum": ["Screening", "Screen Failed", "Enrolled", "Randomized", "Active", "Completed", "Discontinued", "Lost to Follow-up", "Withdrawn"],
      "description": "Current subject status"
    },
    "race": {
      "type": "string",
      "enum": ["American Indian or Alaska Native", "Asian", "Black or African American", "Native Hawaiian or Other Pacific Islander", "White", "Multiple", "Unknown", "Not Reported"],
      "description": "FDA race categories"
    },
    "ethnicity": {
      "type": "string",
      "enum": ["Hispanic or Latino", "Not Hispanic or Latino", "Unknown", "Not Reported"],
      "description": "FDA ethnicity categories"
    }
  }
}
```

---

### TreatmentArm

Study arm definition (treatment vs control).

```json
{
  "title": "TreatmentArm",
  "type": "object",
  "required": ["arm_code", "arm_name", "arm_type", "study_id"],
  "properties": {
    "arm_code": {
      "type": "string",
      "description": "Short code for arm (maps to ARM in SDTM)",
      "examples": ["TRT", "PBO", "COMBO", "LOW", "HIGH"]
    },
    "arm_name": {
      "type": "string",
      "description": "Full arm description (maps to ARMCD)"
    },
    "arm_type": {
      "type": "string",
      "enum": ["Experimental", "Active Comparator", "Placebo Comparator", "Sham Comparator", "No Intervention"],
      "description": "Type of intervention"
    },
    "study_id": {
      "type": "string"
    },
    "randomization_ratio": {
      "type": "number",
      "description": "Ratio for randomization (e.g., 2 for 2:1)",
      "default": 1
    },
    "target_enrollment": {
      "type": "integer",
      "description": "Target subjects for this arm"
    },
    "treatment_description": {
      "type": "string",
      "description": "Description of intervention"
    },
    "dose": {
      "type": "string",
      "description": "Dose level if applicable",
      "examples": ["200mg", "10mg/kg", "1x10^6 cells"]
    },
    "schedule": {
      "type": "string",
      "description": "Dosing schedule",
      "examples": ["Q3W", "BID", "Single dose"]
    }
  }
}
```

---

### VisitSchedule

Protocol-defined visit schedule (planned visits).

```json
{
  "title": "VisitSchedule",
  "type": "object",
  "required": ["visit_num", "visit_name", "study_id"],
  "properties": {
    "visit_num": {
      "type": "number",
      "description": "Visit number (maps to VISITNUM)",
      "examples": [1, 2, 3, 99]
    },
    "visit_name": {
      "type": "string",
      "description": "Visit name (maps to VISIT)",
      "examples": ["Screening", "Baseline", "Week 4", "End of Treatment", "Follow-up"]
    },
    "study_id": {
      "type": "string"
    },
    "visit_type": {
      "type": "string",
      "enum": ["Screening", "Baseline", "Treatment", "End of Treatment", "Follow-up", "Early Termination", "Unscheduled"],
      "description": "Category of visit"
    },
    "target_day": {
      "type": "integer",
      "description": "Target study day (Day 1 = first treatment)",
      "examples": [-14, 1, 29, 85]
    },
    "window_before": {
      "type": "integer",
      "description": "Allowed days before target",
      "default": 0
    },
    "window_after": {
      "type": "integer",
      "description": "Allowed days after target",
      "default": 0
    },
    "required_assessments": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of required assessments",
      "examples": [["Vital Signs", "Labs", "AE Review", "RECIST"]]
    }
  }
}
```

---

### ActualVisit

Subject's actual visit occurrence.

```json
{
  "title": "ActualVisit",
  "type": "object",
  "required": ["usubjid", "visit_num", "visit_date"],
  "properties": {
    "usubjid": {
      "type": "string",
      "description": "Reference to Subject"
    },
    "visit_num": {
      "type": "number",
      "description": "Scheduled visit number (maps to VISITNUM)"
    },
    "visit_name": {
      "type": "string",
      "description": "Visit name (maps to VISIT)"
    },
    "visit_date": {
      "type": "string",
      "format": "date",
      "description": "Actual visit date"
    },
    "study_day": {
      "type": "integer",
      "description": "Calculated study day relative to first treatment"
    },
    "visit_status": {
      "type": "string",
      "enum": ["Completed", "Missed", "Partially Completed", "Unscheduled"],
      "description": "Visit completion status"
    },
    "window_deviation_days": {
      "type": "integer",
      "description": "Days outside visit window (0 = within window)"
    }
  }
}
```

---

### Randomization

Subject randomization record.

```json
{
  "title": "Randomization",
  "type": "object",
  "required": ["usubjid", "randomization_date", "arm_code"],
  "properties": {
    "usubjid": {
      "type": "string"
    },
    "randomization_number": {
      "type": "string",
      "description": "Randomization/enrollment number"
    },
    "randomization_date": {
      "type": "string",
      "format": "date"
    },
    "arm_code": {
      "type": "string",
      "description": "Assigned treatment arm"
    },
    "stratification_factors": {
      "type": "object",
      "description": "Stratification factor values",
      "examples": [{"region": "North America", "prior_therapy": "Yes", "pd_l1_status": "Positive"}]
    },
    "randomization_method": {
      "type": "string",
      "enum": ["IVRS", "IWRS", "Sealed Envelope", "Block", "Stratified Block"],
      "description": "Method used for randomization"
    }
  }
}
```

---

### AdverseEvent

Adverse event occurrence.

```json
{
  "title": "AdverseEvent",
  "type": "object",
  "required": ["usubjid", "aeterm", "aestdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "aeseq": {
      "type": "integer",
      "description": "Sequence number within subject"
    },
    "aeterm": {
      "type": "string",
      "description": "Reported term (verbatim)"
    },
    "aedecod": {
      "type": "string",
      "description": "MedDRA Preferred Term (PT)"
    },
    "aebodsys": {
      "type": "string",
      "description": "MedDRA System Organ Class (SOC)"
    },
    "aehlt": {
      "type": "string",
      "description": "MedDRA High Level Term (HLT)"
    },
    "aehlgt": {
      "type": "string",
      "description": "MedDRA High Level Group Term (HLGT)"
    },
    "aellt": {
      "type": "string",
      "description": "MedDRA Lowest Level Term (LLT)"
    },
    "aestdtc": {
      "type": "string",
      "format": "date",
      "description": "Start date"
    },
    "aeendtc": {
      "type": "string",
      "format": "date",
      "description": "End date (null if ongoing)"
    },
    "aesev": {
      "type": "string",
      "enum": ["Mild", "Moderate", "Severe"],
      "description": "Severity"
    },
    "aetoxgr": {
      "type": "string",
      "enum": ["1", "2", "3", "4", "5"],
      "description": "CTCAE grade (oncology)"
    },
    "aeser": {
      "type": "string",
      "enum": ["Y", "N"],
      "description": "Serious adverse event flag"
    },
    "aerel": {
      "type": "string",
      "enum": ["Not Related", "Unlikely", "Possibly", "Probably", "Definitely"],
      "description": "Relationship to study drug"
    },
    "aeacn": {
      "type": "string",
      "enum": ["None", "Dose Reduced", "Drug Interrupted", "Drug Withdrawn", "Not Applicable"],
      "description": "Action taken with study treatment"
    },
    "aeout": {
      "type": "string",
      "enum": ["Recovered/Resolved", "Recovering/Resolving", "Not Recovered/Not Resolved", "Recovered with Sequelae", "Fatal", "Unknown"],
      "description": "Outcome"
    },
    "aesae_criteria": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["Death", "Life-threatening", "Hospitalization", "Disability", "Congenital Anomaly", "Important Medical Event"]
      },
      "description": "SAE criteria met (if serious)"
    }
  }
}
```

---

### Exposure

Study drug exposure/dosing record.

```json
{
  "title": "Exposure",
  "type": "object",
  "required": ["usubjid", "extrt", "exstdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "exseq": {
      "type": "integer",
      "description": "Sequence number"
    },
    "extrt": {
      "type": "string",
      "description": "Treatment name"
    },
    "exdose": {
      "type": "number",
      "description": "Dose administered"
    },
    "exdosu": {
      "type": "string",
      "description": "Dose units",
      "examples": ["mg", "mg/kg", "mL", "cells"]
    },
    "exdosfrq": {
      "type": "string",
      "description": "Dosing frequency",
      "examples": ["ONCE", "QD", "BID", "Q3W"]
    },
    "exroute": {
      "type": "string",
      "description": "Route of administration",
      "examples": ["ORAL", "INTRAVENOUS", "SUBCUTANEOUS"]
    },
    "exstdtc": {
      "type": "string",
      "format": "date",
      "description": "Start date/time"
    },
    "exendtc": {
      "type": "string",
      "format": "date",
      "description": "End date/time"
    },
    "exadj": {
      "type": "string",
      "description": "Reason for dose adjustment",
      "examples": ["Toxicity", "Weight-based", "Protocol Amendment"]
    },
    "planned_dose": {
      "type": "number",
      "description": "Protocol-specified dose"
    },
    "dose_modification": {
      "type": "string",
      "enum": ["None", "Reduction", "Delay", "Interruption", "Discontinuation"],
      "description": "Type of dose modification"
    }
  }
}
```

---

### ConcomitantMed

Prior and concomitant medications.

```json
{
  "title": "ConcomitantMed",
  "type": "object",
  "required": ["usubjid", "cmtrt"],
  "properties": {
    "usubjid": { "type": "string" },
    "cmseq": { "type": "integer" },
    "cmtrt": {
      "type": "string",
      "description": "Medication name (generic)"
    },
    "cmdecod": {
      "type": "string",
      "description": "WHO Drug Dictionary preferred name"
    },
    "cmatc1cd": {
      "type": "string",
      "description": "ATC Level 1 code (Anatomical main group)"
    },
    "cmatc2cd": {
      "type": "string",
      "description": "ATC Level 2 code (Therapeutic subgroup)"
    },
    "cmatc3cd": {
      "type": "string",
      "description": "ATC Level 3 code (Pharmacological subgroup)"
    },
    "cmatc4cd": {
      "type": "string",
      "description": "ATC Level 4 code (Chemical subgroup)"
    },
    "cmdose": { "type": "number" },
    "cmdosu": { "type": "string" },
    "cmdosfrq": { "type": "string" },
    "cmroute": { "type": "string" },
    "cmstdtc": {
      "type": "string",
      "format": "date",
      "description": "Start date"
    },
    "cmendtc": {
      "type": "string",
      "format": "date",
      "description": "End date"
    },
    "cmindc": {
      "type": "string",
      "description": "Indication for medication"
    },
    "cmprior": {
      "type": "string",
      "enum": ["Y", "N"],
      "description": "Prior medication (before study start)"
    },
    "cmongo": {
      "type": "string",
      "enum": ["Y", "N"],
      "description": "Ongoing at study end"
    }
  }
}
```

---


### TrialLab

Laboratory test result in trial context.

```json
{
  "title": "TrialLab",
  "type": "object",
  "required": ["usubjid", "lbtestcd", "lbdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "lbseq": { "type": "integer" },
    "lbtestcd": {
      "type": "string",
      "description": "Lab test short name",
      "examples": ["ALT", "AST", "CREAT", "HGB", "WBC"]
    },
    "lbtest": {
      "type": "string",
      "description": "Lab test name"
    },
    "lbcat": {
      "type": "string",
      "description": "Category",
      "examples": ["CHEMISTRY", "HEMATOLOGY", "URINALYSIS", "COAGULATION"]
    },
    "lborres": {
      "type": "string",
      "description": "Result (original units)"
    },
    "lborresu": {
      "type": "string",
      "description": "Original units"
    },
    "lbstresc": {
      "type": "string",
      "description": "Result (standard character)"
    },
    "lbstresn": {
      "type": "number",
      "description": "Result (standard numeric)"
    },
    "lbstresu": {
      "type": "string",
      "description": "Standard units"
    },
    "lbstnrlo": {
      "type": "number",
      "description": "Reference range lower limit"
    },
    "lbstnrhi": {
      "type": "number",
      "description": "Reference range upper limit"
    },
    "lbnrind": {
      "type": "string",
      "enum": ["NORMAL", "LOW", "HIGH", "ABNORMAL"],
      "description": "Reference range indicator"
    },
    "lbdtc": {
      "type": "string",
      "format": "date",
      "description": "Collection date"
    },
    "visitnum": { "type": "number" },
    "visit": { "type": "string" },
    "loinc_code": {
      "type": "string",
      "description": "LOINC code for test"
    },
    "lbtoxgr": {
      "type": "string",
      "enum": ["0", "1", "2", "3", "4"],
      "description": "CTCAE toxicity grade (if applicable)"
    }
  }
}
```

---

### EfficacyAssessment

Efficacy/response assessment.

```json
{
  "title": "EfficacyAssessment",
  "type": "object",
  "required": ["usubjid", "assessment_type", "assessment_date"],
  "properties": {
    "usubjid": { "type": "string" },
    "assessment_seq": { "type": "integer" },
    "assessment_type": {
      "type": "string",
      "description": "Type of efficacy assessment",
      "examples": ["RECIST", "irRECIST", "RANO", "NYHA", "mMRC", "EDSS", "ADAS-Cog"]
    },
    "assessment_date": {
      "type": "string",
      "format": "date"
    },
    "visitnum": { "type": "number" },
    "response": {
      "type": "string",
      "description": "Response category (varies by assessment type)",
      "examples": ["CR", "PR", "SD", "PD", "NE"]
    },
    "response_confirmed": {
      "type": "boolean",
      "description": "Was response confirmed per protocol"
    },
    "target_lesion_sum": {
      "type": "number",
      "description": "Sum of target lesion diameters (RECIST)"
    },
    "change_from_baseline": {
      "type": "number",
      "description": "Percent change from baseline"
    },
    "new_lesions": {
      "type": "boolean",
      "description": "New lesions identified"
    },
    "score": {
      "type": "number",
      "description": "Numeric score (for scales like ADAS-Cog)"
    },
    "score_change": {
      "type": "number",
      "description": "Change from baseline score"
    }
  }
}
```

---

### DispositionEvent

Subject disposition milestones and status changes.

```json
{
  "title": "DispositionEvent",
  "type": "object",
  "required": ["usubjid", "dsdecod", "dsstdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "dsseq": { "type": "integer" },
    "dsterm": {
      "type": "string",
      "description": "Reported term (verbatim)"
    },
    "dsdecod": {
      "type": "string",
      "description": "Standardized disposition term",
      "examples": ["COMPLETED", "ADVERSE EVENT", "DEATH", "WITHDRAWAL BY SUBJECT", "LOST TO FOLLOW-UP", "PHYSICIAN DECISION", "PROTOCOL VIOLATION", "LACK OF EFFICACY"]
    },
    "dscat": {
      "type": "string",
      "enum": ["DISPOSITION EVENT", "PROTOCOL MILESTONE"],
      "description": "Category"
    },
    "dsscat": {
      "type": "string",
      "description": "Subcategory",
      "examples": ["STUDY TREATMENT", "STUDY PARTICIPATION", "INFORMED CONSENT", "RANDOMIZATION"]
    },
    "dsstdtc": {
      "type": "string",
      "format": "date",
      "description": "Disposition date"
    },
    "epoch": {
      "type": "string",
      "description": "Trial epoch",
      "examples": ["SCREENING", "TREATMENT", "FOLLOW-UP"]
    }
  }
}
```

---

### ProtocolDeviation

Protocol deviation record.

```json
{
  "title": "ProtocolDeviation",
  "type": "object",
  "required": ["usubjid", "dvterm", "dvstdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "dvseq": { "type": "integer" },
    "dvterm": {
      "type": "string",
      "description": "Deviation description"
    },
    "dvdecod": {
      "type": "string",
      "description": "Standardized deviation category",
      "examples": ["INFORMED CONSENT", "INCLUSION/EXCLUSION CRITERIA", "STUDY PROCEDURES", "STUDY TREATMENT", "CONCOMITANT MEDICATION", "VISIT SCHEDULE"]
    },
    "dvcat": {
      "type": "string",
      "enum": ["MAJOR", "MINOR"],
      "description": "Severity category"
    },
    "dvstdtc": {
      "type": "string",
      "format": "date",
      "description": "Deviation date"
    },
    "dvendtc": {
      "type": "string",
      "format": "date",
      "description": "Resolution date"
    },
    "impact_on_analysis": {
      "type": "string",
      "enum": ["None", "Excluded from Per-Protocol", "Excluded from ITT", "Sensitivity Analysis Required"]
    }
  }
}
```

---

### MedicalHistory

Subject's medical history (pre-existing conditions).

```json
{
  "title": "MedicalHistory",
  "type": "object",
  "required": ["usubjid", "mhterm"],
  "properties": {
    "usubjid": { "type": "string" },
    "mhseq": { "type": "integer" },
    "mhterm": {
      "type": "string",
      "description": "Reported term (verbatim)"
    },
    "mhdecod": {
      "type": "string",
      "description": "MedDRA Preferred Term"
    },
    "mhbodsys": {
      "type": "string",
      "description": "MedDRA System Organ Class"
    },
    "mhcat": {
      "type": "string",
      "description": "Category",
      "examples": ["PRIMARY DIAGNOSIS", "GENERAL MEDICAL HISTORY", "SURGICAL HISTORY"]
    },
    "mhstdtc": {
      "type": "string",
      "format": "date",
      "description": "Start date (approximate)"
    },
    "mhendtc": {
      "type": "string",
      "format": "date",
      "description": "End date (if resolved)"
    },
    "mhongo": {
      "type": "string",
      "enum": ["Y", "N"],
      "description": "Ongoing at screening"
    }
  }
}
```

---

## Entity Relationships Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                     STUDY                                        │
│  study_id, protocol_title, phase, therapeutic_area, indication, status          │
└──────────────────────────────────────────────────────────────────────────────────┘
        │                           │                           │
        │ 1:M                       │ 1:M                       │ 1:M
        ▼                           ▼                           ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────────────────┐
│      SITE       │      │  TREATMENT_ARM  │      │      VISIT_SCHEDULE         │
│  site_id        │      │  arm_code       │      │  visit_num, visit_name      │
│  country        │      │  arm_type       │      │  target_day, window         │
│  PI             │      │  dose, schedule │      └─────────────────────────────┘
└─────────────────┘      └─────────────────┘
        │                           │
        │ 1:M                       │
        ▼                           │
┌─────────────────────────────────┐│
│           SUBJECT               ││
│  usubjid, subject_id            ││
│  (extends Person)               ││
│  screening_date, consent_date   ◄┘ (assigned via RANDOMIZATION)
│  treatment_arm, status          │
│  patient_ref → PatientSim       │
└─────────────────────────────────┘
        │
        ├───────────────┬───────────────┬───────────────┬───────────────┐
        │               │               │               │               │
        │ 1:1           │ 1:M           │ 1:M           │ 1:M           │
        ▼               ▼               ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│RANDOMIZATION│ │ ACTUAL_VISIT│ │ADVERSE_EVENT│ │  EXPOSURE   │ │CONCOM_MED   │
│rand_number  │ │visit_num    │ │aeterm       │ │extrt, dose  │ │cmtrt        │
│arm_code     │ │visit_date   │ │MedDRA codes │ │modification │ │ATC codes    │
│strat_factors│ │study_day    │ │severity,SAE │ │route        │ │indication   │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────────┐
│  TRIAL_LAB  │ │VITAL_SIGN   │ │EFFICACY_ASSESS  │
│lbtestcd     │ │vstest       │ │assessment_type  │
│result, units│ │result       │ │response         │
│LOINC, grade │ │             │ │change_from_base │
└─────────────┘ └─────────────┘ └─────────────────┘

Additional Subject-Level Entities:
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ MEDICAL_HISTORY │  │PROTOCOL_DEVIATION│ │DISPOSITION_EVENT│
│ mhterm, MedDRA  │  │ dvterm, severity │  │ dsdecod, epoch  │
│ ongoing flag    │  │ impact           │  │ milestone       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Identity Correlation

TrialSim subjects can be correlated with other HealthSim products:

| TrialSim Entity | Correlated Entity | Linking Field | Notes |
|-----------------|-------------------|---------------|-------|
| Subject | Patient (PatientSim) | patient_ref → mrn | Medical history source |
| Subject | Person (core) | ssn | Cross-product correlation |
| Site | Facility (NetworkSim) | facility_id | Physical location |
| Principal Investigator | Provider (NetworkSim) | npi | Provider details |

### USUBJID Construction

The unique subject identifier follows CDISC convention:

```
USUBJID = STUDYID-SITEID-SUBJID
Example: ABC-123-001-0001
         │          │    │
         │          │    └── Subject number (4 digits)
         │          └─────── Site number (3 digits)
         └────────────────── Study ID
```

---

## Part 2: Dimensional Analytics Model

The dimensional model transforms canonical entities into a star schema optimized for analytics.

### Design Principles

1. **Loosely Coupled**: Independent from canonical model; transformation happens on request
2. **Denormalized**: Dimensions are flattened for query performance
3. **Conformed Dimensions**: Share dim_date with other products
4. **Analytics-First**: Grain chosen for common analytical questions

### Target Platforms

| Platform | Schema | Use Case |
|----------|--------|----------|
| DuckDB | analytics.trialsim_* | Local development, demos |
| Databricks | healthsim.gold.trialsim_* | Enterprise analytics |

---

### Dimension Tables

#### dim_study

Study-level attributes for grouping and filtering.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| study_key | INT | Surrogate key | 1 |
| study_id | VARCHAR | Natural key | "ABC-123-001" |
| protocol_title | VARCHAR | Full title | "A Phase 3, Randomized..." |
| phase | VARCHAR | Trial phase | "Phase 3" |
| therapeutic_area | VARCHAR | TA | "Oncology" |
| indication | VARCHAR | Disease target | "NSCLC" |
| sponsor | VARCHAR | Sponsor name | "Example Pharma" |
| study_type | VARCHAR | Interventional/Observational | "Interventional" |
| design_allocation | VARCHAR | Randomization type | "Randomized" |
| design_masking | VARCHAR | Blinding | "Double" |
| design_model | VARCHAR | Intervention model | "Parallel" |
| enrollment_target | INT | Target N | 300 |
| status | VARCHAR | Current status | "Active" |
| start_date | DATE | FSFV | 2024-01-15 |

```sql
CREATE TABLE dim_study (
    study_key INT PRIMARY KEY,
    study_id VARCHAR(50) NOT NULL,
    protocol_title VARCHAR(500),
    protocol_number VARCHAR(50),
    phase VARCHAR(20),
    therapeutic_area VARCHAR(100),
    indication VARCHAR(200),
    sponsor VARCHAR(200),
    study_type VARCHAR(50),
    design_allocation VARCHAR(50),
    design_masking VARCHAR(50),
    design_model VARCHAR(50),
    enrollment_target INT,
    status VARCHAR(50),
    start_date DATE,
    primary_completion_date DATE,
    study_completion_date DATE
);
```

---

#### dim_site

Site-level attributes for geographic and performance analysis.

| Column | Type | Description |
|--------|------|-------------|
| site_key | INT | Surrogate key |
| site_id | VARCHAR | Natural key (within study) |
| study_key | INT | FK to dim_study |
| site_name | VARCHAR | Institution name |
| country | VARCHAR | ISO country code |
| country_name | VARCHAR | Full country name |
| region | VARCHAR | Geographic region |
| pi_name | VARCHAR | Principal Investigator |
| pi_specialty | VARCHAR | PI specialty |
| status | VARCHAR | Site status |
| activation_date | DATE | Site activation |
| enrollment_target | INT | Site target |

```sql
CREATE TABLE dim_site (
    site_key INT PRIMARY KEY,
    site_id VARCHAR(10) NOT NULL,
    study_key INT REFERENCES dim_study(study_key),
    site_name VARCHAR(200),
    country VARCHAR(3),
    country_name VARCHAR(100),
    region VARCHAR(50),
    pi_name VARCHAR(100),
    pi_specialty VARCHAR(100),
    status VARCHAR(50),
    activation_date DATE,
    enrollment_target INT
);
```

---

#### dim_subject

Subject demographics and enrollment attributes.

| Column | Type | Description |
|--------|------|-------------|
| subject_key | INT | Surrogate key |
| usubjid | VARCHAR | Natural key (unique) |
| subject_id | VARCHAR | Subject number within site |
| study_key | INT | FK to dim_study |
| site_key | INT | FK to dim_site |
| arm_key | INT | FK to dim_treatment_arm |
| age | INT | Age at enrollment |
| age_band | VARCHAR | Age group (18-40, 41-64, 65+) |
| sex | VARCHAR | M/F |
| race | VARCHAR | FDA race category |
| ethnicity | VARCHAR | Hispanic/Not Hispanic |
| country | VARCHAR | Country of enrollment |
| screening_date | DATE | Screening visit |
| consent_date | DATE | Informed consent |
| randomization_date | DATE | Randomization (if applicable) |
| status | VARCHAR | Current status |
| patient_mrn | VARCHAR | Link to PatientSim (if available) |

```sql
CREATE TABLE dim_subject (
    subject_key INT PRIMARY KEY,
    usubjid VARCHAR(50) NOT NULL UNIQUE,
    subject_id VARCHAR(10),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    age INT,
    age_band VARCHAR(20),
    sex VARCHAR(10),
    race VARCHAR(100),
    ethnicity VARCHAR(50),
    country VARCHAR(3),
    screening_date DATE,
    consent_date DATE,
    randomization_date DATE,
    status VARCHAR(50),
    patient_mrn VARCHAR(50)
);
```

---

#### dim_treatment_arm

Treatment arm definitions.

```sql
CREATE TABLE dim_treatment_arm (
    arm_key INT PRIMARY KEY,
    arm_code VARCHAR(20) NOT NULL,
    arm_name VARCHAR(200),
    arm_type VARCHAR(50),  -- Experimental, Placebo, Active Comparator
    study_key INT REFERENCES dim_study(study_key),
    dose VARCHAR(50),
    schedule VARCHAR(50),
    randomization_ratio DECIMAL(3,1)
);
```

---

#### dim_visit_schedule

Protocol-defined visit schedule.

```sql
CREATE TABLE dim_visit_schedule (
    visit_schedule_key INT PRIMARY KEY,
    study_key INT REFERENCES dim_study(study_key),
    visit_num DECIMAL(5,1) NOT NULL,
    visit_name VARCHAR(100),
    visit_type VARCHAR(50),  -- Screening, Baseline, Treatment, Follow-up
    target_day INT,
    window_before INT,
    window_after INT,
    is_required BOOLEAN
);
```

---

#### dim_meddra

MedDRA hierarchy for adverse event analysis.

```sql
CREATE TABLE dim_meddra (
    meddra_key INT PRIMARY KEY,
    pt_code VARCHAR(10) NOT NULL,  -- Preferred Term code
    pt_term VARCHAR(200),
    hlt_code VARCHAR(10),          -- High Level Term
    hlt_term VARCHAR(200),
    hlgt_code VARCHAR(10),         -- High Level Group Term
    hlgt_term VARCHAR(200),
    soc_code VARCHAR(10),          -- System Organ Class
    soc_term VARCHAR(200)
);
```

---

#### dim_lab_test

Laboratory test definitions (shared concept with PatientSim).

```sql
CREATE TABLE dim_lab_test (
    lab_test_key INT PRIMARY KEY,
    lbtestcd VARCHAR(20) NOT NULL,
    lbtest VARCHAR(100),
    lbcat VARCHAR(50),            -- CHEMISTRY, HEMATOLOGY, etc.
    loinc_code VARCHAR(20),
    unit_standard VARCHAR(20),
    normal_lo DECIMAL(10,3),
    normal_hi DECIMAL(10,3)
);
```

---

#### dim_date (Shared)

Standard date dimension shared across all HealthSim products.

```sql
-- Already defined in dimensional-analytics.md
-- Reused for TrialSim
```

---

### Fact Tables

#### fact_enrollment

Grain: One row per subject enrollment milestone.

| Column | Type | Description |
|--------|------|-------------|
| enrollment_key | INT | Surrogate key |
| subject_key | INT | FK to dim_subject |
| study_key | INT | FK to dim_study |
| site_key | INT | FK to dim_site |
| arm_key | INT | FK to dim_treatment_arm |
| screening_date_key | INT | FK to dim_date |
| consent_date_key | INT | FK to dim_date |
| randomization_date_key | INT | FK to dim_date |
| **Measures** | | |
| days_screen_to_consent | INT | Days from screening to consent |
| days_consent_to_randomization | INT | Days from consent to randomization |
| screen_failure_flag | BOOLEAN | Did subject fail screening |
| screen_failure_reason | VARCHAR | Reason if failed |
| is_randomized | BOOLEAN | Subject was randomized |
| is_completed | BOOLEAN | Subject completed study |
| is_discontinued | BOOLEAN | Subject discontinued |

```sql
CREATE TABLE fact_enrollment (
    enrollment_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    screening_date_key INT REFERENCES dim_date(date_key),
    consent_date_key INT REFERENCES dim_date(date_key),
    randomization_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    days_screen_to_consent INT,
    days_consent_to_randomization INT,
    screen_failure_flag BOOLEAN,
    screen_failure_reason VARCHAR(200),
    is_randomized BOOLEAN,
    is_completed BOOLEAN,
    is_discontinued BOOLEAN,
    discontinuation_reason VARCHAR(200)
);
```

---

#### fact_visit

Grain: One row per actual visit.

```sql
CREATE TABLE fact_visit (
    visit_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    visit_schedule_key INT REFERENCES dim_visit_schedule(visit_schedule_key),
    visit_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    visit_num DECIMAL(5,1),
    study_day INT,
    window_deviation_days INT,  -- Days outside visit window
    is_within_window BOOLEAN,
    visit_status VARCHAR(50),   -- Completed, Missed, Partial
    assessments_planned INT,
    assessments_completed INT
);
```

---

#### fact_adverse_event

Grain: One row per adverse event occurrence.

```sql
CREATE TABLE fact_adverse_event (
    ae_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    site_key INT REFERENCES dim_site(site_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    meddra_key INT REFERENCES dim_meddra(meddra_key),
    onset_date_key INT REFERENCES dim_date(date_key),
    resolution_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    aeseq INT,
    aeterm VARCHAR(200),
    severity VARCHAR(20),
    ctcae_grade INT,
    is_serious BOOLEAN,
    is_related BOOLEAN,         -- Related to study drug
    is_treatment_emergent BOOLEAN,
    duration_days INT,
    action_taken VARCHAR(50),   -- Dose reduced, interrupted, etc.
    outcome VARCHAR(50),
    sae_criteria VARCHAR(200)   -- If serious, which criteria
);
```

---

#### fact_exposure

Grain: One row per dosing record.

```sql
CREATE TABLE fact_exposure (
    exposure_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    start_date_key INT REFERENCES dim_date(date_key),
    end_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    exseq INT,
    treatment_name VARCHAR(100),
    dose_administered DECIMAL(10,3),
    dose_unit VARCHAR(20),
    dose_planned DECIMAL(10,3),
    dose_percent DECIMAL(5,2),      -- % of planned dose
    is_dose_reduction BOOLEAN,
    is_dose_delay BOOLEAN,
    is_dose_interruption BOOLEAN,
    dose_modification_reason VARCHAR(100),
    duration_days INT,
    cumulative_dose DECIMAL(10,3)
);
```

---

#### fact_efficacy

Grain: One row per efficacy assessment.

```sql
CREATE TABLE fact_efficacy (
    efficacy_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    arm_key INT REFERENCES dim_treatment_arm(arm_key),
    visit_key INT REFERENCES fact_visit(visit_key),
    assessment_date_key INT REFERENCES dim_date(date_key),
    -- Attributes
    assessment_type VARCHAR(50),   -- RECIST, irRECIST, RANO, etc.
    visitnum DECIMAL(5,1),
    -- Measures
    response_category VARCHAR(20), -- CR, PR, SD, PD, NE
    is_responder BOOLEAN,          -- CR or PR
    target_lesion_sum DECIMAL(10,2),
    change_from_baseline_pct DECIMAL(5,2),
    is_confirmed_response BOOLEAN,
    new_lesions_flag BOOLEAN,
    score_value DECIMAL(10,2),     -- For numeric scales
    score_change DECIMAL(10,2)
);
```

---

#### fact_lab_result

Grain: One row per laboratory result.

```sql
CREATE TABLE fact_lab_result (
    lab_result_key INT PRIMARY KEY,
    subject_key INT REFERENCES dim_subject(subject_key),
    study_key INT REFERENCES dim_study(study_key),
    lab_test_key INT REFERENCES dim_lab_test(lab_test_key),
    visit_key INT REFERENCES fact_visit(visit_key),
    collection_date_key INT REFERENCES dim_date(date_key),
    -- Measures
    lbseq INT,
    result_numeric DECIMAL(15,5),
    result_character VARCHAR(50),
    result_unit VARCHAR(20),
    is_baseline BOOLEAN,
    baseline_value DECIMAL(15,5),
    change_from_baseline DECIMAL(15,5),
    pct_change_from_baseline DECIMAL(10,2),
    is_abnormal BOOLEAN,
    is_low BOOLEAN,
    is_high BOOLEAN,
    ctcae_grade INT,
    is_clinically_significant BOOLEAN
);
```

---

## Dimensional Model Diagram

```
                           ┌─────────────────┐
                           │    dim_study    │
                           │  (study attrs)  │
                           └────────┬────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    ┌─────────────┐         ┌──────────────┐         ┌──────────────┐
    │  dim_site   │         │dim_treatment_│         │dim_visit_    │
    │(geography)  │         │    arm       │         │  schedule    │
    └──────┬──────┘         └──────┬───────┘         └──────┬───────┘
           │                       │                        │
           └───────────┬───────────┴────────────┬───────────┘
                       │                        │
                       ▼                        │
                ┌─────────────┐                 │
                │ dim_subject │◄────────────────┘
                │(demographics│
                └──────┬──────┘
                       │
    ┌──────────────────┼──────────────────┬──────────────────┐
    │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼
┌────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│    fact_   │  │    fact_    │  │    fact_    │  │    fact_    │
│ enrollment │  │    visit    │  │adverse_event│  │  exposure   │
│(milestones)│  │ (compliance)│  │  (safety)   │  │  (dosing)   │
└────────────┘  └──────┬──────┘  └──────┬──────┘  └─────────────┘
                       │                │
                       │                ▼
                       │         ┌─────────────┐
                       │         │ dim_meddra  │
                       │         │(AE hierarch)│
                       │         └─────────────┘
                       │
            ┌──────────┴──────────┐
            │                     │
            ▼                     ▼
     ┌─────────────┐       ┌─────────────┐
     │fact_efficacy│       │fact_lab_    │
     │ (response)  │       │  result     │
     └─────────────┘       └──────┬──────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │dim_lab_test │
                           └─────────────┘

Shared:
┌─────────────┐
│  dim_date   │ ◄── All fact tables link here
│ (calendar)  │
└─────────────┘
```

---

## Example Analytics Queries

### Enrollment Velocity by Site

```sql
SELECT 
    s.site_name,
    s.country,
    COUNT(*) as subjects_enrolled,
    AVG(f.days_consent_to_randomization) as avg_days_to_randomize,
    SUM(CASE WHEN f.screen_failure_flag THEN 1 ELSE 0 END) as screen_failures,
    ROUND(100.0 * SUM(CASE WHEN f.screen_failure_flag THEN 1 ELSE 0 END) / COUNT(*), 1) as screen_failure_rate
FROM fact_enrollment f
JOIN dim_site s ON f.site_key = s.site_key
GROUP BY s.site_name, s.country
ORDER BY subjects_enrolled DESC;
```

### Safety: AE Rates by Treatment Arm

```sql
SELECT
    a.arm_name,
    m.soc_term as system_organ_class,
    COUNT(DISTINCT f.ae_key) as ae_count,
    COUNT(DISTINCT f.subject_key) as subjects_with_ae,
    SUM(CASE WHEN f.is_serious THEN 1 ELSE 0 END) as serious_ae_count,
    SUM(CASE WHEN f.ctcae_grade >= 3 THEN 1 ELSE 0 END) as grade_3_plus
FROM fact_adverse_event f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
JOIN dim_meddra m ON f.meddra_key = m.meddra_key
GROUP BY a.arm_name, m.soc_term
ORDER BY a.arm_name, ae_count DESC;
```

### Efficacy: Response Rate by Arm

```sql
SELECT
    a.arm_name,
    COUNT(DISTINCT f.subject_key) as evaluable_subjects,
    SUM(CASE WHEN f.response_category = 'CR' THEN 1 ELSE 0 END) as complete_response,
    SUM(CASE WHEN f.response_category = 'PR' THEN 1 ELSE 0 END) as partial_response,
    SUM(CASE WHEN f.is_responder THEN 1 ELSE 0 END) as total_responders,
    ROUND(100.0 * SUM(CASE WHEN f.is_responder THEN 1 ELSE 0 END) / COUNT(DISTINCT f.subject_key), 1) as orr_pct
FROM fact_efficacy f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
WHERE f.assessment_type = 'RECIST'
  AND f.is_confirmed_response = true
GROUP BY a.arm_name;
```

### Site Performance: Visit Compliance

```sql
SELECT
    s.site_name,
    COUNT(*) as total_visits,
    SUM(CASE WHEN f.is_within_window THEN 1 ELSE 0 END) as on_schedule,
    ROUND(100.0 * SUM(CASE WHEN f.is_within_window THEN 1 ELSE 0 END) / COUNT(*), 1) as compliance_rate,
    AVG(ABS(f.window_deviation_days)) as avg_deviation_days
FROM fact_visit f
JOIN dim_site s ON f.site_key = s.site_key
WHERE f.visit_status = 'Completed'
GROUP BY s.site_name
ORDER BY compliance_rate DESC;
```

### Dose Intensity Analysis

```sql
SELECT
    a.arm_name,
    COUNT(DISTINCT f.subject_key) as subjects,
    AVG(f.dose_percent) as avg_dose_intensity_pct,
    SUM(CASE WHEN f.is_dose_reduction THEN 1 ELSE 0 END) as dose_reductions,
    SUM(CASE WHEN f.is_dose_interruption THEN 1 ELSE 0 END) as dose_interruptions
FROM fact_exposure f
JOIN dim_treatment_arm a ON f.arm_key = a.arm_key
GROUP BY a.arm_name;
```

---

## Implementation Notes

### Canonical → Dimensional Transformation

The transformation from canonical to dimensional happens on request:

```
User: "Load this trial data to DuckDB for analytics"

Claude:
1. Reads canonical entities (JSON)
2. Generates dimension tables (denormalized)
3. Generates fact tables (aggregated metrics)
4. Executes SQL DDL + INSERT statements
```

### Cross-Product Analytics

When PatientSim and TrialSim data are correlated:

| TrialSim Dimension | PatientSim Dimension | Join Key |
|-------------------|---------------------|----------|
| dim_subject | dim_patient | patient_mrn |
| fact_lab_result | fact_lab_results | subject_key ↔ patient_key via mrn |

This enables queries like: "Compare baseline disease characteristics between responders and non-responders using PatientSim medical history."

---

## Next Steps

1. **Add canonical schemas to `references/data-models.md`**
2. **Add dimensional model to `formats/dimensional-analytics.md`**
3. **Create example conversation flows for DuckDB/Databricks loading**
4. **Test with sample trial generation**
