# TrialSim Canonical Models - DRAFT

> **Purpose**: This content will be added to `references/data-models.md` after the RxMemberSim Models section.
> 
> **Review Status**: DRAFT - Pending approval

---

## TrialSim Models

TrialSim entities support clinical trial data generation with CDISC compliance. The Subject entity extends the core Person model, following the same pattern as Patient, Member, and RxMember.

### Entity Hierarchy

```
Study
├── Site (1:M)
├── TreatmentArm (1:M)
├── VisitSchedule (1:M)
└── Subject (via Site, 1:M)
    ├── Randomization (1:1)
    ├── ActualVisit (1:M)
    ├── AdverseEvent (1:M)
    ├── Exposure (1:M)
    ├── ConcomitantMed (1:M)
    ├── TrialLab (1:M)
    ├── EfficacyAssessment (1:M)
    ├── MedicalHistory (1:M)
    ├── ProtocolDeviation (1:M)
    └── DispositionEvent (1:M)
```

### Subject (extends Person)

Trial participant. Extends the core Person model with trial-specific identifiers.

```json
{
  "title": "Subject",
  "allOf": [{ "$ref": "#/definitions/Person" }],
  "required": ["subject_id", "study_id", "site_id", "informed_consent_date"],
  "properties": {
    "subject_id": {
      "type": "string",
      "description": "Subject identifier within site",
      "pattern": "^[0-9]{4}$"
    },
    "usubjid": {
      "type": "string",
      "description": "Unique Subject ID: STUDYID-SITEID-SUBJID (CDISC format)",
      "pattern": "^[A-Z0-9-]+-[0-9]+-[0-9]+$"
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
      "description": "Reference to PatientSim Patient (MRN) for medical history linkage"
    },
    "screening_id": {
      "type": "string",
      "description": "Pre-randomization screening number"
    },
    "screening_date": {
      "type": "string",
      "format": "date"
    },
    "informed_consent_date": {
      "type": "string",
      "format": "date",
      "description": "Maps to RFICDTC in SDTM"
    },
    "randomization_date": {
      "type": "string",
      "format": "date"
    },
    "treatment_arm": {
      "type": "string",
      "description": "Assigned treatment arm code"
    },
    "status": {
      "type": "string",
      "enum": ["Screening", "Screen Failed", "Enrolled", "Randomized", "Active", "Completed", "Discontinued", "Lost to Follow-up", "Withdrawn"]
    },
    "race": {
      "type": "string",
      "enum": ["American Indian or Alaska Native", "Asian", "Black or African American", "Native Hawaiian or Other Pacific Islander", "White", "Multiple", "Unknown", "Not Reported"],
      "description": "FDA race categories"
    },
    "ethnicity": {
      "type": "string",
      "enum": ["Hispanic or Latino", "Not Hispanic or Latino", "Unknown", "Not Reported"]
    }
  }
}
```

**USUBJID Construction:**

| Component | Source | Example |
|-----------|--------|---------|
| STUDYID | Study.study_id | ABC-123-001 |
| SITEID | Site.site_id | 001 |
| SUBJID | Subject.subject_id | 0001 |
| **USUBJID** | Concatenated | ABC-123-001-001-0001 |

### Study

Clinical trial protocol definition.

```json
{
  "title": "Study",
  "type": "object",
  "required": ["study_id", "protocol_title", "phase", "status"],
  "properties": {
    "study_id": {
      "type": "string",
      "description": "Unique study identifier (maps to STUDYID)",
      "pattern": "^[A-Z0-9-]+$"
    },
    "protocol_title": {
      "type": "string"
    },
    "protocol_number": {
      "type": "string"
    },
    "phase": {
      "type": "string",
      "enum": ["Phase 1", "Phase 1/2", "Phase 2", "Phase 2/3", "Phase 3", "Phase 4"]
    },
    "therapeutic_area": {
      "type": "string"
    },
    "indication": {
      "type": "string"
    },
    "sponsor": {
      "type": "string"
    },
    "status": {
      "type": "string",
      "enum": ["Planning", "Recruiting", "Active", "Completed", "Terminated", "Suspended"]
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
      "minimum": 1
    },
    "start_date": {
      "type": "string",
      "format": "date"
    },
    "primary_completion_date": {
      "type": "string",
      "format": "date"
    },
    "study_completion_date": {
      "type": "string",
      "format": "date"
    }
  }
}
```

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
      "pattern": "^[0-9]{3,4}$"
    },
    "study_id": {
      "type": "string"
    },
    "site_name": {
      "type": "string"
    },
    "facility_id": {
      "type": "string",
      "description": "Reference to NetworkSim Facility (cross-product)"
    },
    "country": {
      "type": "string",
      "pattern": "^[A-Z]{2,3}$",
      "description": "ISO 3166-1 country code"
    },
    "region": {
      "type": "string"
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
      "format": "date"
    },
    "enrollment_target": {
      "type": "integer"
    },
    "enrollment_actual": {
      "type": "integer"
    }
  }
}
```

### TreatmentArm

Study arm definition.

```json
{
  "title": "TreatmentArm",
  "type": "object",
  "required": ["arm_code", "arm_name", "arm_type", "study_id"],
  "properties": {
    "arm_code": {
      "type": "string",
      "description": "Short code (maps to ARM in SDTM)"
    },
    "arm_name": {
      "type": "string",
      "description": "Full description (maps to ARMCD)"
    },
    "arm_type": {
      "type": "string",
      "enum": ["Experimental", "Active Comparator", "Placebo Comparator", "Sham Comparator", "No Intervention"]
    },
    "study_id": {
      "type": "string"
    },
    "randomization_ratio": {
      "type": "number",
      "default": 1
    },
    "target_enrollment": {
      "type": "integer"
    },
    "treatment_description": {
      "type": "string"
    },
    "dose": {
      "type": "string"
    },
    "schedule": {
      "type": "string"
    }
  }
}
```

### VisitSchedule

Protocol-defined visit schedule.

```json
{
  "title": "VisitSchedule",
  "type": "object",
  "required": ["visit_num", "visit_name", "study_id"],
  "properties": {
    "visit_num": {
      "type": "number",
      "description": "Maps to VISITNUM"
    },
    "visit_name": {
      "type": "string",
      "description": "Maps to VISIT"
    },
    "study_id": {
      "type": "string"
    },
    "visit_type": {
      "type": "string",
      "enum": ["Screening", "Baseline", "Treatment", "End of Treatment", "Follow-up", "Early Termination", "Unscheduled"]
    },
    "target_day": {
      "type": "integer",
      "description": "Target study day (Day 1 = first treatment)"
    },
    "window_before": {
      "type": "integer",
      "default": 0
    },
    "window_after": {
      "type": "integer",
      "default": 0
    },
    "required_assessments": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

### ActualVisit

Subject's actual visit occurrence.

```json
{
  "title": "ActualVisit",
  "type": "object",
  "required": ["usubjid", "visit_num", "visit_date"],
  "properties": {
    "usubjid": {
      "type": "string"
    },
    "visit_num": {
      "type": "number"
    },
    "visit_name": {
      "type": "string"
    },
    "visit_date": {
      "type": "string",
      "format": "date"
    },
    "study_day": {
      "type": "integer"
    },
    "visit_status": {
      "type": "string",
      "enum": ["Completed", "Missed", "Partially Completed", "Unscheduled"]
    },
    "window_deviation_days": {
      "type": "integer",
      "description": "Days outside visit window (0 = within window)"
    }
  }
}
```

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
      "type": "string"
    },
    "randomization_date": {
      "type": "string",
      "format": "date"
    },
    "arm_code": {
      "type": "string"
    },
    "stratification_factors": {
      "type": "object",
      "description": "Key-value pairs for stratification"
    },
    "randomization_method": {
      "type": "string",
      "enum": ["IVRS", "IWRS", "Sealed Envelope", "Block", "Stratified Block"]
    }
  }
}
```

### AdverseEvent

Adverse event with full MedDRA hierarchy.

```json
{
  "title": "AdverseEvent",
  "type": "object",
  "required": ["usubjid", "aeterm", "aestdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "aeseq": { "type": "integer" },
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
      "format": "date"
    },
    "aeendtc": {
      "type": "string",
      "format": "date"
    },
    "aesev": {
      "type": "string",
      "enum": ["Mild", "Moderate", "Severe"]
    },
    "aetoxgr": {
      "type": "string",
      "enum": ["1", "2", "3", "4", "5"],
      "description": "CTCAE grade"
    },
    "aeser": {
      "type": "string",
      "enum": ["Y", "N"]
    },
    "aerel": {
      "type": "string",
      "enum": ["Not Related", "Unlikely", "Possibly", "Probably", "Definitely"]
    },
    "aeacn": {
      "type": "string",
      "enum": ["None", "Dose Reduced", "Drug Interrupted", "Drug Withdrawn", "Not Applicable"]
    },
    "aeout": {
      "type": "string",
      "enum": ["Recovered/Resolved", "Recovering/Resolving", "Not Recovered/Not Resolved", "Recovered with Sequelae", "Fatal", "Unknown"]
    },
    "aesae_criteria": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["Death", "Life-threatening", "Hospitalization", "Disability", "Congenital Anomaly", "Important Medical Event"]
      }
    }
  }
}
```

**MedDRA Hierarchy:**

| Level | Abbreviation | Example |
|-------|--------------|---------|
| System Organ Class | SOC | Gastrointestinal disorders |
| High Level Group Term | HLGT | Gastrointestinal motility and defaecation conditions |
| High Level Term | HLT | Diarrhoea (excl infective) |
| Preferred Term | PT | Diarrhoea |
| Lowest Level Term | LLT | Loose stools |

### Exposure

Study drug exposure/dosing record.

```json
{
  "title": "Exposure",
  "type": "object",
  "required": ["usubjid", "extrt", "exstdtc"],
  "properties": {
    "usubjid": { "type": "string" },
    "exseq": { "type": "integer" },
    "extrt": {
      "type": "string",
      "description": "Treatment name"
    },
    "exdose": { "type": "number" },
    "exdosu": {
      "type": "string",
      "description": "Dose units (mg, mg/kg, mL, cells)"
    },
    "exdosfrq": {
      "type": "string",
      "description": "Frequency (ONCE, QD, BID, Q3W)"
    },
    "exroute": {
      "type": "string",
      "description": "Route (ORAL, INTRAVENOUS, SUBCUTANEOUS)"
    },
    "exstdtc": {
      "type": "string",
      "format": "date"
    },
    "exendtc": {
      "type": "string",
      "format": "date"
    },
    "exadj": {
      "type": "string",
      "description": "Reason for dose adjustment"
    },
    "planned_dose": { "type": "number" },
    "dose_modification": {
      "type": "string",
      "enum": ["None", "Reduction", "Delay", "Interruption", "Discontinuation"]
    }
  }
}
```

### ConcomitantMed

Prior and concomitant medications with ATC classification.

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
      "description": "ATC Level 1 (Anatomical main group)"
    },
    "cmatc2cd": {
      "type": "string",
      "description": "ATC Level 2 (Therapeutic subgroup)"
    },
    "cmatc3cd": {
      "type": "string",
      "description": "ATC Level 3 (Pharmacological subgroup)"
    },
    "cmatc4cd": {
      "type": "string",
      "description": "ATC Level 4 (Chemical subgroup)"
    },
    "cmdose": { "type": "number" },
    "cmdosu": { "type": "string" },
    "cmdosfrq": { "type": "string" },
    "cmroute": { "type": "string" },
    "cmstdtc": {
      "type": "string",
      "format": "date"
    },
    "cmendtc": {
      "type": "string",
      "format": "date"
    },
    "cmindc": {
      "type": "string",
      "description": "Indication"
    },
    "cmprior": {
      "type": "string",
      "enum": ["Y", "N"],
      "description": "Prior to study start"
    },
    "cmongo": {
      "type": "string",
      "enum": ["Y", "N"],
      "description": "Ongoing at study end"
    }
  }
}
```

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
      "description": "Lab test short name (ALT, AST, CREAT, HGB, WBC)"
    },
    "lbtest": {
      "type": "string",
      "description": "Lab test full name"
    },
    "lbcat": {
      "type": "string",
      "description": "Category (CHEMISTRY, HEMATOLOGY, URINALYSIS, COAGULATION)"
    },
    "lborres": {
      "type": "string",
      "description": "Result (original units)"
    },
    "lborresu": {
      "type": "string",
      "description": "Original units"
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
      "enum": ["NORMAL", "LOW", "HIGH", "ABNORMAL"]
    },
    "lbdtc": {
      "type": "string",
      "format": "date"
    },
    "visitnum": { "type": "number" },
    "visit": { "type": "string" },
    "loinc_code": { "type": "string" },
    "lbtoxgr": {
      "type": "string",
      "enum": ["0", "1", "2", "3", "4"],
      "description": "CTCAE toxicity grade"
    }
  }
}
```

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
      "description": "Assessment type (RECIST, irRECIST, RANO, NYHA, mMRC, EDSS, ADAS-Cog)"
    },
    "assessment_date": {
      "type": "string",
      "format": "date"
    },
    "visitnum": { "type": "number" },
    "response": {
      "type": "string",
      "description": "Response category (CR, PR, SD, PD, NE)"
    },
    "response_confirmed": {
      "type": "boolean"
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
      "type": "boolean"
    },
    "score": {
      "type": "number",
      "description": "Numeric score (for scales)"
    },
    "score_change": {
      "type": "number",
      "description": "Change from baseline score"
    }
  }
}
```

**Common Assessment Types:**

| Assessment | Domain | Response Categories |
|------------|--------|---------------------|
| RECIST 1.1 | Oncology | CR, PR, SD, PD, NE |
| irRECIST | Immuno-Oncology | iCR, iPR, iSD, iUPD, iCPD |
| RANO | Neuro-Oncology | CR, PR, SD, PD |
| NYHA | Cardiovascular | Class I, II, III, IV |
| ADAS-Cog | CNS (Alzheimer's) | 0-70 score |
| EDSS | CNS (MS) | 0-10 score |

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
      "description": "Category (PRIMARY DIAGNOSIS, GENERAL MEDICAL HISTORY, SURGICAL HISTORY)"
    },
    "mhstdtc": {
      "type": "string",
      "format": "date"
    },
    "mhendtc": {
      "type": "string",
      "format": "date"
    },
    "mhongo": {
      "type": "string",
      "enum": ["Y", "N"],
      "description": "Ongoing at screening"
    }
  }
}
```

### DispositionEvent

Subject disposition milestones.

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
      "description": "Standardized term"
    },
    "dscat": {
      "type": "string",
      "enum": ["DISPOSITION EVENT", "PROTOCOL MILESTONE"]
    },
    "dsscat": {
      "type": "string",
      "description": "Subcategory (STUDY TREATMENT, STUDY PARTICIPATION)"
    },
    "dsstdtc": {
      "type": "string",
      "format": "date"
    },
    "epoch": {
      "type": "string",
      "description": "Trial epoch (SCREENING, TREATMENT, FOLLOW-UP)"
    }
  }
}
```

**Standard Disposition Terms (CDISC CT):**

| Category | Terms |
|----------|-------|
| Completion | COMPLETED |
| Discontinuation | ADVERSE EVENT, DEATH, LACK OF EFFICACY, LOST TO FOLLOW-UP, PHYSICIAN DECISION, PROTOCOL VIOLATION, WITHDRAWAL BY SUBJECT |

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
      "description": "Standardized category"
    },
    "dvcat": {
      "type": "string",
      "enum": ["MAJOR", "MINOR"]
    },
    "dvstdtc": {
      "type": "string",
      "format": "date"
    },
    "dvendtc": {
      "type": "string",
      "format": "date"
    },
    "impact_on_analysis": {
      "type": "string",
      "enum": ["None", "Excluded from Per-Protocol", "Excluded from ITT", "Sensitivity Analysis Required"]
    }
  }
}
```

---

## TrialSim Identity Correlation

### Cross-Product Linking

| TrialSim Entity | Correlated Entity | Linking Field | Purpose |
|-----------------|-------------------|---------------|---------|
| Subject | Patient (PatientSim) | patient_ref → mrn | Medical history source |
| Subject | Person (core) | ssn | Cross-product identity |
| Site | Facility (NetworkSim) | facility_id | Physical location details |
| PI | Provider (NetworkSim) | npi | Provider credentials |

### Event Correlation

| Source Event (Product) | Correlated Event (Product) | Timing | Notes |
|------------------------|---------------------------|--------|-------|
| Subject enrollment (TrialSim) | Encounters (PatientSim) | Per protocol | Study visits generate encounters |
| AdverseEvent (TrialSim) | Diagnosis (PatientSim) | Same event | If site EMR used as source |
| TrialLab (TrialSim) | LabResult (PatientSim) | Same collection | If site EMR used as source |

### Identity Flow Example

```
Person (core)
├── ssn: "123456789"
├── name: { given_name: "Jane", family_name: "Doe" }
└── birth_date: "1965-03-15"
    │
    ├─► Patient (PatientSim)
    │   └── mrn: "MRN-12345"
    │       └── [Diagnoses, Encounters, Labs, etc.]
    │
    └─► Subject (TrialSim)
        ├── usubjid: "ABC-123-001-0001"
        ├── patient_ref: "MRN-12345"  ◄── Links to Patient
        └── [Trial-specific data]
```
