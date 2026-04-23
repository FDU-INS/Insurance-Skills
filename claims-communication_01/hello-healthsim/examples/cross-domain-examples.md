# Cross-Domain Examples

Generate data that spans multiple HealthSim products for realistic end-to-end scenarios.

---

## Example 1: Patient with Medical and Pharmacy Claims

### Prompt
```
Generate a diabetic patient with their recent office visit claim and pharmacy claim for metformin
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "member_id": "MEM001234",
    "name": { "given_name": "Maria", "family_name": "Santos" },
    "birth_date": "1968-05-22",
    "gender": "F"
  },
  "clinical_data": {
    "diagnoses": [
      { "code": "E11.9", "description": "Type 2 diabetes mellitus without complications" },
      { "code": "I10", "description": "Essential hypertension" },
      { "code": "E78.5", "description": "Hyperlipidemia" }
    ],
    "medications": [
      { "name": "Metformin", "dose": "1000 mg", "frequency": "BID" },
      { "name": "Lisinopril", "dose": "20 mg", "frequency": "QD" },
      { "name": "Atorvastatin", "dose": "20 mg", "frequency": "QD" }
    ],
    "recent_labs": [
      { "test": "HbA1c", "value": "7.4", "unit": "%", "date": "2025-01-15" },
      { "test": "Creatinine", "value": "0.9", "unit": "mg/dL", "date": "2025-01-15" }
    ]
  },
  "professional_claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "E11.9",
    "other_diagnoses": ["I10", "E78.5"],
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "description": "Office visit, established, moderate complexity",
        "charge_amount": 175.00
      },
      {
        "line_number": 2,
        "procedure_code": "36415",
        "description": "Venipuncture",
        "charge_amount": 15.00
      }
    ],
    "total_charges": 190.00,
    "adjudication": {
      "status": "paid",
      "allowed_amount": 138.00,
      "copay": 30.00,
      "paid_amount": 108.00
    }
  },
  "pharmacy_claims": [
    {
      "claim_id": "RX20250115000001",
      "member_id": "MEM001234",
      "service_date": "2025-01-15",
      "ndc": "00093101901",
      "drug_name": "Metformin 1000mg Tablet",
      "quantity": 60,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00,
        "plan_paid": 5.50
      }
    },
    {
      "claim_id": "RX20250115000002",
      "member_id": "MEM001234",
      "service_date": "2025-01-15",
      "ndc": "00093505601",
      "drug_name": "Lisinopril 20mg Tablet",
      "quantity": 30,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00,
        "plan_paid": 3.00
      }
    },
    {
      "claim_id": "RX20250115000003",
      "member_id": "MEM001234",
      "service_date": "2025-01-15",
      "ndc": "00071015523",
      "drug_name": "Atorvastatin 20mg Tablet",
      "quantity": 30,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00,
        "plan_paid": 4.50
      }
    }
  ],
  "consistency_check": {
    "member_id_match": true,
    "diagnoses_match": true,
    "medications_to_rx_match": true,
    "service_dates_aligned": true
  }
}
```

### Key Points
- Same `member_id` across all claims
- Clinical diagnoses match claim diagnoses
- Medications in clinical data have corresponding pharmacy claims
- Quantity 60 for metformin = BID dosing for 30 days

---

## Example 2: Hospitalization with Follow-Up

### Prompt
```
Generate a heart failure patient with inpatient admission, follow-up visit, and related pharmacy claims
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000002",
    "member_id": "MEM002345",
    "name": { "given_name": "James", "family_name": "Wilson" },
    "birth_date": "1952-11-08",
    "gender": "M"
  },
  "episode_timeline": [
    { "event": "Admission", "date": "2025-01-05" },
    { "event": "Discharge", "date": "2025-01-09" },
    { "event": "Follow-up Visit", "date": "2025-01-16" },
    { "event": "Medication Fills", "date": "2025-01-09" }
  ],
  "facility_claim": {
    "claim_id": "CLM20250109000001",
    "claim_type": "INSTITUTIONAL",
    "bill_type": "111",
    "member_id": "MEM002345",
    "admit_date": "2025-01-05",
    "discharge_date": "2025-01-09",
    "length_of_stay": 4,
    "principal_diagnosis": "I50.23",
    "drg": {
      "code": "291",
      "description": "Heart Failure and Shock with MCC"
    },
    "total_charges": 28500.00,
    "adjudication": {
      "status": "paid",
      "drg_payment": 12500.00,
      "deductible": 500.00,
      "coinsurance": 2400.00,
      "paid_amount": 9600.00
    }
  },
  "follow_up_claim": {
    "claim_id": "CLM20250116000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM002345",
    "service_date": "2025-01-16",
    "place_of_service": "11",
    "principal_diagnosis": "I50.23",
    "claim_lines": [
      {
        "procedure_code": "99215",
        "description": "Post-discharge follow-up, high complexity",
        "charge_amount": 225.00
      }
    ],
    "adjudication": {
      "status": "paid",
      "allowed_amount": 165.00,
      "copay": 40.00,
      "paid_amount": 125.00
    }
  },
  "pharmacy_claims": [
    {
      "claim_id": "RX20250109000001",
      "service_date": "2025-01-09",
      "ndc": "00078060061",
      "drug_name": "Entresto 97/103mg Tablet",
      "quantity": 60,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 3,
        "patient_pay": 75.00,
        "note": "New start at discharge"
      }
    },
    {
      "claim_id": "RX20250109000002",
      "service_date": "2025-01-09",
      "ndc": "00378395201",
      "drug_name": "Carvedilol 25mg Tablet",
      "quantity": 60,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00
      }
    },
    {
      "claim_id": "RX20250109000003",
      "service_date": "2025-01-09",
      "ndc": "00591555601",
      "drug_name": "Furosemide 40mg Tablet",
      "quantity": 60,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00
      }
    }
  ],
  "quality_measures": {
    "transition_of_care": {
      "follow_up_within_7_days": true,
      "medication_reconciliation": true,
      "discharge_instructions_provided": true
    }
  }
}
```

### Key Points
- Timeline shows logical sequence
- Follow-up within 7 days (quality measure)
- Discharge medications align with GDMT for HF
- Entresto (brand) on Tier 3 with higher copay
- DRG 291 matches principal diagnosis

---

## Example 3: Prior Auth Flow

### Prompt
```
Generate a complete prior authorization flow: initial denial, PA submission, approval, and successful fill
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM003456",
    "name": { "given_name": "Lisa", "family_name": "Chen" },
    "plan_code": "HMO-STANDARD"
  },
  "prior_auth_timeline": [
    { "event": "Initial claim rejected", "date": "2025-01-10" },
    { "event": "PA submitted", "date": "2025-01-10" },
    { "event": "PA approved", "date": "2025-01-13" },
    { "event": "Claim approved", "date": "2025-01-13" }
  ],
  "initial_rejection": {
    "claim_id": "RX20250110000001",
    "service_date": "2025-01-10",
    "ndc": "00002140280",
    "drug_name": "Trulicity 1.5mg Pen",
    "response": {
      "status": "rejected",
      "reject_code": "75",
      "reject_message": "Prior Authorization Required"
    }
  },
  "prior_auth_request": {
    "pa_id": "PA20250110000001",
    "request_date": "2025-01-10",
    "drug_name": "Trulicity 1.5mg",
    "ndc": "00002140280",
    "diagnosis": "E11.65",
    "clinical_information": {
      "current_medications": ["Metformin 1000mg BID"],
      "a1c_value": "8.9%",
      "a1c_date": "2025-01-05",
      "metformin_trial_duration": "6 months",
      "contraindications": "None",
      "prescriber_rationale": "A1C not at goal despite maximum metformin. GLP-1 RA preferred for cardiovascular benefit."
    },
    "submission_method": "ePA"
  },
  "prior_auth_decision": {
    "pa_id": "PA20250110000001",
    "decision_date": "2025-01-13",
    "status": "approved",
    "approval_details": {
      "effective_date": "2025-01-13",
      "expiration_date": "2026-01-13",
      "approved_quantity": "4 pens per 28 days",
      "override_code": "08",
      "auth_number": "AUTH20250113001"
    }
  },
  "successful_claim": {
    "claim_id": "RX20250113000001",
    "service_date": "2025-01-13",
    "ndc": "00002140280",
    "drug_name": "Trulicity 1.5mg Pen",
    "quantity": 4,
    "days_supply": 28,
    "prior_auth_number": "AUTH20250113001",
    "response": {
      "status": "paid",
      "ingredient_cost_paid": 875.00,
      "patient_pay_amount": 125.00,
      "tier": 4,
      "message": "Prior authorization on file"
    }
  }
}
```

### Key Points
- Complete PA workflow from rejection to approval
- Clinical information justifies approval
- Override code 08 = Prior authorization on file
- PA auth number links rejection to approval
- 1-year approval typical for chronic medications

---

## Example 4: Value-Based Care Report

### Prompt
```
Generate a diabetic patient with quality measure compliance status and care gaps
```

### Expected Output
```json
{
  "patient": {
    "member_id": "MEM004567",
    "name": { "given_name": "Robert", "family_name": "Martinez" },
    "birth_date": "1960-03-15",
    "gender": "M",
    "pcp_npi": "1234567890",
    "attributed_provider": "Dr. Sarah Johnson"
  },
  "clinical_summary": {
    "diagnoses": [
      { "code": "E11.65", "description": "Type 2 diabetes with hyperglycemia" },
      { "code": "I10", "description": "Essential hypertension" },
      { "code": "E78.5", "description": "Hyperlipidemia" }
    ],
    "most_recent_labs": {
      "a1c": { "value": "7.8", "date": "2024-11-20" },
      "ldl": { "value": "118", "date": "2024-11-20" },
      "creatinine": { "value": "1.1", "date": "2024-11-20" }
    },
    "most_recent_vitals": {
      "blood_pressure": "142/88",
      "date": "2024-12-15"
    }
  },
  "quality_measures": {
    "measurement_year": 2025,
    "applicable_measures": [
      {
        "measure_id": "CDC-HBD",
        "measure_name": "Hemoglobin A1c Control for Patients with Diabetes",
        "target": "A1C < 8.0%",
        "status": "compliant",
        "evidence": { "a1c": "7.8%", "date": "2024-11-20" }
      },
      {
        "measure_id": "CDC-BPD",
        "measure_name": "Blood Pressure Control for Patients with Diabetes",
        "target": "BP < 140/90",
        "status": "non_compliant",
        "evidence": { "bp": "142/88", "date": "2024-12-15" },
        "care_gap": true
      },
      {
        "measure_id": "CDC-EYE",
        "measure_name": "Eye Exam for Patients with Diabetes",
        "target": "Retinal exam in measurement year",
        "status": "non_compliant",
        "last_exam": "2023-02-10",
        "care_gap": true
      },
      {
        "measure_id": "SPD",
        "measure_name": "Statin Therapy for Patients with Diabetes",
        "target": "On statin therapy",
        "status": "compliant",
        "evidence": { "medication": "Atorvastatin 40mg", "active": true }
      }
    ]
  },
  "care_gaps": [
    {
      "gap": "Blood Pressure Control",
      "recommendation": "Schedule follow-up to address BP. Consider medication adjustment.",
      "priority": "high"
    },
    {
      "gap": "Diabetic Eye Exam",
      "recommendation": "Refer to ophthalmology for dilated retinal exam",
      "priority": "high",
      "overdue_by": "23 months"
    }
  ],
  "risk_score": {
    "hcc_categories": [
      { "hcc": 19, "description": "Diabetes with Complications", "source": "E11.65" }
    ],
    "raf_score": 1.125,
    "risk_level": "moderate"
  }
}
```

### Key Points
- Quality measures match actual HEDIS specs
- Care gaps identified with actionable recommendations
- HCC risk score for payment adjustment
- Combines clinical data with payer quality program

---

## Example 5: Oncology Patient Journey

### Prompt
```
Generate a breast cancer patient with clinical data, facility infusion claim, and oral chemotherapy pharmacy claim
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000005",
    "member_id": "MEM005678",
    "name": { "given_name": "Jennifer", "family_name": "Thompson" },
    "birth_date": "1968-04-12",
    "gender": "F"
  },
  "clinical_data": {
    "cancer_diagnosis": {
      "code": "C50.911",
      "description": "Malignant neoplasm of unspecified site of right female breast",
      "diagnosed_date": "2024-10-15"
    },
    "staging": {
      "tnm": { "t": "T2", "n": "N1", "m": "M0" },
      "ajcc_stage": "IIB",
      "stage_date": "2024-10-20"
    },
    "biomarkers": {
      "er_status": "positive",
      "er_percent": 85,
      "pr_status": "positive",
      "pr_percent": 60,
      "her2_status": "negative",
      "her2_score": "1+",
      "ki67_percent": 18
    },
    "treatment_plan": {
      "surgery": { "type": "Lumpectomy", "date": "2024-11-01" },
      "chemotherapy": "TC (Docetaxel + Cyclophosphamide)",
      "radiation": "Whole breast radiation planned",
      "hormonal_therapy": "Anastrozole planned post-chemo"
    }
  },
  "facility_claim": {
    "claim_id": "CLM20250115000005",
    "claim_type": "INSTITUTIONAL",
    "facility_type": "outpatient_hospital",
    "member_id": "MEM005678",
    "service_date": "2025-01-15",
    "principal_diagnosis": "C50.911",
    "claim_lines": [
      {
        "line_number": 1,
        "revenue_code": "0335",
        "procedure_code": "96413",
        "hcpcs_code": "J9171",
        "description": "Docetaxel injection, 1mg",
        "units": 120,
        "charge_amount": 4800.00
      },
      {
        "line_number": 2,
        "revenue_code": "0335",
        "procedure_code": "96415",
        "description": "Chemotherapy infusion, additional hour",
        "units": 1,
        "charge_amount": 250.00
      },
      {
        "line_number": 3,
        "revenue_code": "0250",
        "hcpcs_code": "J2405",
        "description": "Ondansetron injection (antiemetic)",
        "units": 8,
        "charge_amount": 120.00
      }
    ],
    "prior_auth": {
      "auth_number": "PA20241101-54321",
      "status": "approved"
    },
    "adjudication": {
      "status": "paid",
      "allowed_amount": 4200.00,
      "deductible": 0.00,
      "coinsurance": 840.00,
      "paid_amount": 3360.00
    }
  },
  "pharmacy_claim": {
    "claim_id": "RX20250115000005",
    "member_id": "MEM005678",
    "service_date": "2025-01-15",
    "ndc": "00310075090",
    "drug_name": "Anastrozole 1mg Tablet",
    "quantity": 30,
    "days_supply": 30,
    "prescriber_npi": "1234567890",
    "pharmacy_type": "retail",
    "response": {
      "status": "paid",
      "tier": 2,
      "patient_pay": 15.00,
      "plan_paid": 42.00,
      "note": "Hormonal therapy for ER+ breast cancer"
    }
  },
  "care_coordination": {
    "oncologist": "Dr. Michael Rodriguez",
    "treatment_center": "Regional Cancer Center",
    "next_infusion": "2025-02-05",
    "labs_due": "2025-01-29"
  },
  "consistency_check": {
    "diagnosis_code_match": true,
    "treatment_matches_biomarkers": true,
    "prior_auth_on_file": true,
    "hormonal_therapy_appropriate": true
  }
}
```

### Key Points

- Clinical staging (T2 N1 M0 = Stage IIB) matches treatment intensity
- Biomarkers (ER+, PR+, HER2-) justify hormonal therapy selection
- Docetaxel J-code (J9171) with revenue code 0335 (chemotherapy)
- Anastrozole (hormonal therapy) matches ER-positive status
- Prior authorization required for infusion chemotherapy
- Cross-product consistency: clinical → facility claim → pharmacy claim

---

## Example 6: Clinical Trial Subject with EMR Linkage

### Prompt
```
Generate a clinical trial subject enrolled in a Phase III oncology trial with linked PatientSim medical history for baseline characteristics analysis
```

### Expected Output
```json
{
  "trial_subject": {
    "usubjid": "ONCO-2025-001-005-0042",
    "subject_id": "0042",
    "site_id": "005",
    "study_id": "ONCO-2025-001",
    "patient_ref": "MRN00000042",
    "screening_date": "2025-01-08",
    "informed_consent_date": "2025-01-08",
    "randomization_date": "2025-01-15",
    "treatment_arm": "TRT",
    "status": "Active",
    "demographics": {
      "age": 62,
      "sex": "F",
      "race": "White",
      "ethnicity": "Not Hispanic or Latino"
    }
  },
  "linked_patient": {
    "mrn": "MRN00000042",
    "name": { "given_name": "Margaret", "family_name": "Thompson" },
    "birth_date": "1962-09-14",
    "diagnoses": [
      { 
        "code": "C34.90", 
        "description": "Malignant neoplasm of unspecified part of bronchus or lung",
        "onset_date": "2024-11-15"
      },
      { "code": "J44.9", "description": "COPD, unspecified" },
      { "code": "I10", "description": "Essential hypertension" }
    ],
    "baseline_tumor_size_mm": 45,
    "egfr_status": "Wild-type",
    "pdl1_expression": "50%",
    "prior_therapies": []
  },
  "trial_medical_history": {
    "domain": "MH",
    "records": [
      {
        "USUBJID": "ONCO-2025-001-005-0042",
        "MHSEQ": 1,
        "MHTERM": "Chronic obstructive pulmonary disease",
        "MHDECOD": "Chronic obstructive pulmonary disease",
        "MHBODSYS": "Respiratory, thoracic and mediastinal disorders",
        "MHCAT": "GENERAL MEDICAL HISTORY",
        "MHSTDTC": "2019-06-01",
        "MHONGO": "Y"
      },
      {
        "USUBJID": "ONCO-2025-001-005-0042",
        "MHSEQ": 2,
        "MHTERM": "Hypertension",
        "MHDECOD": "Hypertension",
        "MHBODSYS": "Vascular disorders",
        "MHCAT": "GENERAL MEDICAL HISTORY",
        "MHSTDTC": "2015-03-15",
        "MHONGO": "Y"
      }
    ]
  },
  "baseline_efficacy": {
    "assessment_type": "RECIST",
    "assessment_date": "2025-01-12",
    "response": "NE",
    "target_lesion_sum": 45,
    "measurable_disease": true
  },
  "correlation_keys": {
    "usubjid_to_mrn": "ONCO-2025-001-005-0042 → MRN00000042",
    "ssn": "shared for cross-product identity"
  }
}
```

### Key Points

- **Subject.patient_ref** links to **Patient.mrn** for cross-product analytics
- Medical history from PatientSim populates SDTM MH domain
- Baseline tumor characteristics correlate with trial efficacy endpoints
- Same person identity (SSN) maintained across both products
- Enables analytics: "Does baseline tumor burden predict response?"

---

## Example 7: Trial Subject with Site Provider Linkage

### Prompt
```
Generate a Phase III trial site with principal investigator from NetworkSim provider registry
```

### Expected Output
```json
{
  "trial_site": {
    "site_id": "012",
    "study_id": "CV-OUTCOMES-001",
    "site_name": "Memorial Heart Institute",
    "facility_id": "FAC-MHI-001",
    "country": "USA",
    "region": "Southeast",
    "status": "Active",
    "activation_date": "2024-06-15",
    "enrollment_target": 50,
    "enrollment_actual": 38,
    "principal_investigator": {
      "name": "Dr. James Chen",
      "npi": "1234567890",
      "specialty": "Cardiovascular Medicine"
    }
  },
  "linked_provider": {
    "npi": "1234567890",
    "name": { "given_name": "James", "family_name": "Chen" },
    "credentials": ["MD", "FACC"],
    "specialty": "Cardiovascular Medicine",
    "primary_taxonomy": "207RC0000X",
    "practice_address": {
      "street": "500 Medical Center Drive",
      "city": "Atlanta",
      "state": "GA",
      "postal_code": "30322"
    }
  },
  "linked_facility": {
    "facility_id": "FAC-MHI-001",
    "name": "Memorial Heart Institute",
    "type": "specialty_hospital",
    "beds": 250,
    "address": {
      "street": "500 Medical Center Drive",
      "city": "Atlanta",
      "state": "GA",
      "postal_code": "30322"
    },
    "certifications": ["JCI", "ACC Chest Pain Center"]
  },
  "correlation_keys": {
    "site_facility_id": "012 → FAC-MHI-001",
    "pi_npi": "Site PI → Provider.npi"
  }
}
```

### Key Points

- **Site.facility_id** links to **NetworkSim Facility**
- **PI.npi** links to **NetworkSim Provider**
- Enables geographic analysis of trial sites
- Supports site feasibility assessments with real provider data

---

## Example 8: Cross-Product Dimensional Analytics

### Prompt
```
Generate star schema data for analyzing trial efficacy by baseline patient characteristics.
Include 20 subjects with PatientSim linkage for cross-product queries.
```

### Expected Output Summary
```sql
-- Dimensional model enables cross-product analytics

-- TrialSim tables created:
-- dim_study, dim_site, dim_subject (with patient_mrn), dim_treatment_arm
-- fact_enrollment, fact_efficacy, fact_adverse_event

-- PatientSim tables created (matching subjects):
-- dim_patient (with mrn matching dim_subject.patient_mrn)
-- fact_diagnoses (baseline conditions)

-- Example cross-product query: Response by baseline tumor burden
SELECT
    CASE 
        WHEN p.baseline_tumor_size < 50 THEN 'Low (<50mm)'
        WHEN p.baseline_tumor_size < 100 THEN 'Medium (50-100mm)'
        ELSE 'High (>100mm)'
    END as tumor_burden,
    COUNT(DISTINCT ts.subject_key) as subjects,
    SUM(CASE WHEN fe.is_responder THEN 1 ELSE 0 END) as responders,
    ROUND(100.0 * SUM(CASE WHEN fe.is_responder THEN 1 ELSE 0 END) / 
        COUNT(DISTINCT ts.subject_key), 1) as orr_pct
FROM trialsim.dim_subject ts
JOIN patientsim.dim_patient p ON ts.patient_mrn = p.mrn
JOIN trialsim.fact_efficacy fe ON ts.subject_key = fe.subject_key
WHERE fe.assessment_type = 'RECIST'
GROUP BY 1
ORDER BY orr_pct DESC;
```

### Key Points

- **dim_subject.patient_mrn** joins to **dim_patient.mrn**
- Enables analysis of trial outcomes by EMR-sourced baseline characteristics
- Star schema optimized for BI tools (Tableau, Power BI, Looker)
- Uses DuckDB for local analytics (enterprise exports planned for Phase 3)

---

## More Examples

These cross-domain examples show how HealthSim maintains consistency across products. Use them as templates for your own complex scenarios.

---

## Example: v2.0 Data-Driven Cross-Product Generation

### Prompt
```
Generate 10 diabetic patients in Harris County, TX with their medical and pharmacy claims.
Use real population data for realistic demographics and prevalence rates.
```

### Data Lookup (Behind the Scenes)
```
# PopulationSim reads embedded data:
From data/county/places_county_2024.csv (FIPS 48201):
  DIABETES_CrudePrev: 12.1%
  OBESITY_CrudePrev: 32.8%
  BPHIGH_CrudePrev: 32.4%

From data/county/svi_county_2022.csv (FIPS 48201):
  RPL_THEMES: 0.68 (high vulnerability)
  EP_MINRTY: 72.1%
  EP_UNINSUR: 22.1%
```

### Applied Generation Logic
```json
{
  "generation_context": {
    "geography": "Harris County, TX (48201)",
    "applied_rates": {
      "comorbidity_obesity": 0.328,
      "comorbidity_hypertension": 0.324,
      "minority_demographics": 0.721,
      "adherence_modifier": -0.15
    },
    "data_sources": ["CDC_PLACES_2024", "CDC_SVI_2022"]
  }
}
```

### Expected Outputs

**PatientSim**: 10 patients with realistic:
- Demographics matching 72% minority population
- Comorbidities: ~80% with hypertension, ~85% with obesity
- A1C values reflecting high-SVI adherence patterns

**MemberSim**: 10 medical claims with:
- E&M codes (99213/99214)
- Diabetes-related CPTs (83036 A1c, etc.)
- Cost-sharing reflecting plan mix

**RxMemberSim**: Pharmacy claims with:
- Metformin (70%+ of patients)
- GLP-1/SGLT2 inhibitors (20-30%)
- Adherence rates ~70% (high SVI modifier)

### Key Insight

With v2.0 data integration, cross-product generation is **grounded in real population data**. The 10 patients aren't generic—they reflect actual Harris County health patterns from CDC data.

---

## Example: Cross-Product Auto-Persist Workflow

This example demonstrates using auto-persist to build a complete clinical trial dataset across multiple HealthSim products, then clone it for A/B testing.

### Scenario: Phase 3 Diabetes Trial Dataset

#### Step 1: Generate Base Population (PopulationSim)

**User Prompt:**
```
Generate 200 diabetes patients in Arizona using real population data.
Focus on Phoenix metro area with high diabetes prevalence.
Persist this as my trial-candidate-pool.
```

**Claude Response:**
```
[Generating population using Arizona PLACES/SVI data...]
[Auto-persisting to database...]

**Saved "trial-candidate-pool"**

| Metric | Value |
|--------|-------|
| Patients | 200 |
| Counties | Maricopa (85%), Pima (15%) |
| Age Range | 35-72 (mean: 54) |
| Gender | 48% male, 52% female |
| Diabetes Prevalence | Based on Maricopa 11.8% baseline |
| Comorbidities | HTN (68%), Obesity (45%), CKD (12%) |

Data sourced from CDC PLACES 2024 and SVI 2022.
```

#### Step 2: Add Clinical History (PatientSim)

**User Prompt:**
```
For my trial-candidate-pool, add 2 years of clinical history including
A1C labs, medication records, and encounters. Persist to the same scenario.
```

**Claude Response:**
```
[Adding clinical data to 200 patients...]
[Auto-persisting encounters, labs, medications...]

**Updated "trial-candidate-pool"**

| Entity Type | Count |
|-------------|-------|
| Patients | 200 |
| Encounters | 1,847 |
| Lab Results | 4,212 |
| Medications | 2,890 |
| Diagnoses | 3,456 |

Clinical patterns:
- A1C range: 6.5-12.1% (mean: 8.2%)
- 78% on metformin, 34% on GLP-1, 22% on insulin
- Average 9 encounters/patient over 2 years
```

#### Step 3: Enroll Qualified Subjects (TrialSim)

**User Prompt:**
```
Query my trial-candidate-pool for patients with A1C between 7.5-10%,
on stable metformin, no CKD stage 4+. Enroll them in a Phase 3 
SGLT2 trial with 2:1 randomization. Save as sglt2-phase3-trial.
```

**Claude Response:**
```
[Querying candidate pool with eligibility criteria...]
[Found 142 eligible patients (71% of pool)]
[Creating trial with 2:1 randomization...]
[Auto-persisting...]

**Saved "sglt2-phase3-trial"**

| Entity Type | Count |
|-------------|-------|
| Subjects | 142 |
| Treatment Arm | 95 (SGLT2 + Metformin) |
| Control Arm | 47 (Placebo + Metformin) |

Linked from trial-candidate-pool:
- Full clinical history preserved
- Baseline A1C: 7.5-9.8% (mean: 8.4%)
- All subjects on stable metformin ≥3 months
```

#### Step 4: Clone for Analysis Scenarios

**User Prompt:**
```
Clone sglt2-phase3-trial twice:
1. "best-case-scenario" - for optimistic projections
2. "conservative-scenario" - for safety analysis
Tag both with "analysis" and "q1-planning"
```

**Claude Response:**
```
[Cloning scenario with new IDs...]
[Cloning scenario with new IDs...]
[Adding tags...]

**Created 2 clones from "sglt2-phase3-trial"**

| Clone | Subjects | Tags |
|-------|----------|------|
| best-case-scenario | 142 | analysis, q1-planning |
| conservative-scenario | 142 | analysis, q1-planning |

All entity IDs regenerated. Clones are independent - 
modify one without affecting the others.

Next steps:
- Adjust efficacy assumptions in each clone
- Generate different adverse event profiles
- Compare outcomes across scenarios
```

#### Step 5: Export for External Analysis

**User Prompt:**
```
Export conservative-scenario to Parquet for our Databricks analysis.
```

**Claude Response:**
```
[Exporting to Parquet format...]

**Exported "conservative-scenario" to Parquet**

| Entity Type | Rows | File |
|-------------|------|------|
| subjects | 142 | subjects.parquet |
| patients | 142 | patients.parquet |
| encounters | 1,312 | encounters.parquet |
| lab_results | 2,986 | lab_results.parquet |
| medications | 2,044 | medications.parquet |

**Location**: `~/Downloads/conservative-scenario-parquet/`
**Total Size**: 1.2 MB

Load in Databricks:
```python
df = spark.read.parquet(
    'file:///path/to/conservative-scenario-parquet/'
)
```

### Key Points

This workflow demonstrates:

1. **Cross-Product Data Flow**: PopulationSim → PatientSim → TrialSim
2. **Token Efficiency**: 200 patients + 12,000+ related entities without context overflow
3. **Scenario Branching**: Clone for parallel analysis paths
4. **Export Flexibility**: Parquet for big data platforms

The `scenario_id` column links all entities across products, enabling queries like:
```sql
-- Find all clinical data for trial subjects
SELECT p.*, e.*, l.*
FROM patients p
JOIN encounters e ON p.id = e.patient_id
JOIN lab_results l ON e.id = l.encounter_id
WHERE p.scenario_id = 'conservative-scenario'
```

---

See also:
- [Format Examples](format-examples.md) - Transform cross-domain data to standards
- [Oncology Examples](oncology-examples.md) - Detailed oncology patient scenarios
- [TrialSim Examples](trialsim-examples.md) - Clinical trial specific scenarios
- [Auto-Persist Examples](auto-persist-examples.md) - Detailed auto-persist workflows
