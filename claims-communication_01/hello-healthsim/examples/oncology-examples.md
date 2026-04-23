# Oncology Examples

Generate realistic oncology patient data including cancer diagnoses, staging, biomarkers, treatment regimens, and surveillance protocols.

---

## Example 1: Early-Stage Breast Cancer Patient

### Prompt
```
Generate a 55-year-old female with newly diagnosed Stage IIA ER-positive, HER2-negative breast cancer
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000010",
    "name": { "given_name": "Margaret", "family_name": "Thompson" },
    "birth_date": "1969-08-22",
    "gender": "F"
  },
  "diagnoses": [
    {
      "code": "C50.911",
      "description": "Malignant neoplasm of unspecified site of right female breast",
      "diagnosed_date": "2025-01-18",
      "status": "active",
      "staging": {
        "system": "AJCC_8th_edition",
        "stage_group": "IIA",
        "clinical_stage": "cT2 N0 M0",
        "pathologic_stage": "pT2 N0 (sn) M0"
      }
    }
  ],
  "biomarkers": {
    "estrogen_receptor": { "status": "positive", "percentage": 95 },
    "progesterone_receptor": { "status": "positive", "percentage": 80 },
    "her2": { "ihc_score": "1+", "status": "negative" },
    "ki67": { "percentage": 15, "interpretation": "low" },
    "molecular_subtype": "luminal_a"
  },
  "genomic_testing": {
    "test_name": "Oncotype DX",
    "recurrence_score": 18,
    "risk_category": "low",
    "chemotherapy_benefit": "unlikely_to_benefit"
  },
  "pathology": {
    "histology": "invasive_ductal_carcinoma",
    "grade": 1,
    "tumor_size_cm": 2.3,
    "margins": { "status": "negative", "closest_margin_mm": 4 },
    "lymph_nodes": {
      "sentinel_nodes_examined": 3,
      "sentinel_nodes_positive": 0
    }
  },
  "treatment_plan": {
    "intent": "curative",
    "surgery": {
      "procedure": "Lumpectomy with sentinel lymph node biopsy",
      "date": "2025-02-05",
      "status": "completed"
    },
    "radiation": {
      "regimen": "Whole breast radiation 40 Gy in 15 fractions",
      "start_date": "2025-03-10",
      "status": "scheduled"
    },
    "hormonal_therapy": {
      "medication": "Letrozole 2.5 mg daily",
      "duration": "5-10 years",
      "status": "active"
    }
  },
  "medications": [
    {
      "name": "Letrozole",
      "dose": "2.5 mg",
      "frequency": "daily",
      "indication": "Adjuvant hormonal therapy for ER-positive breast cancer"
    },
    {
      "name": "Calcium carbonate",
      "dose": "600 mg",
      "frequency": "BID",
      "indication": "Bone health with aromatase inhibitor"
    },
    {
      "name": "Vitamin D3",
      "dose": "2000 IU",
      "frequency": "daily",
      "indication": "Bone health with aromatase inhibitor"
    }
  ],
  "surveillance": {
    "clinical_exam": "every 6 months for 5 years, then annually",
    "mammogram": "annually starting 6-12 months post-radiation",
    "dexa_scan": "baseline, then every 2 years on AI"
  }
}
```

### Key Points
- Molecular subtype (Luminal A) drives treatment decisions
- Oncotype DX score determines chemotherapy benefit
- ER+/HER2- tumors typically receive hormonal therapy
- Bone health monitoring required with aromatase inhibitors
- Stage IIA = T2 N0 M0 (tumor >2cm, node-negative)

### Variations
```
Generate a Stage IIIA triple-negative breast cancer patient requiring neoadjuvant chemotherapy
Generate a HER2-positive breast cancer patient on trastuzumab and pertuzumab
Generate a metastatic breast cancer patient with bone metastases
Generate a BRCA2-positive breast cancer patient
```

---

## Example 2: Lung Cancer with Targeted Therapy

### Prompt
```
Generate a 68-year-old male former smoker with Stage IV NSCLC adenocarcinoma, EGFR exon 19 deletion positive, with brain metastases
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000011",
    "name": { "given_name": "Robert", "family_name": "Nakamura" },
    "birth_date": "1956-11-14",
    "gender": "M"
  },
  "social_history": {
    "tobacco": {
      "status": "former",
      "pack_years": 30,
      "quit_date": "2010-06-01"
    }
  },
  "diagnoses": [
    {
      "code": "C34.91",
      "description": "Malignant neoplasm of unspecified part of right bronchus or lung",
      "diagnosed_date": "2025-01-10",
      "status": "active",
      "staging": {
        "system": "AJCC_8th_edition",
        "stage_group": "IVB",
        "clinical_stage": "cT2a N2 M1c",
        "m1_sites": ["brain"]
      }
    },
    {
      "code": "C79.31",
      "description": "Secondary malignant neoplasm of brain",
      "diagnosed_date": "2025-01-12",
      "status": "active",
      "note": "3 lesions, largest 1.2 cm right parietal"
    }
  ],
  "biomarkers": {
    "histology": "adenocarcinoma",
    "egfr": {
      "status": "positive",
      "mutation": "exon_19_deletion",
      "test_method": "NGS"
    },
    "alk": { "status": "negative" },
    "ros1": { "status": "negative" },
    "kras": { "status": "negative" },
    "pd_l1": { "tps": "10%", "interpretation": "low" }
  },
  "imaging": [
    {
      "type": "CT Chest/Abdomen/Pelvis",
      "date": "2025-01-10",
      "findings": "3.2 cm right upper lobe mass with mediastinal adenopathy"
    },
    {
      "type": "MRI Brain",
      "date": "2025-01-12",
      "findings": "3 enhancing lesions: right parietal 1.2 cm, left frontal 0.8 cm, right cerebellar 0.6 cm"
    },
    {
      "type": "PET/CT",
      "date": "2025-01-14",
      "findings": "FDG-avid right lung primary, mediastinal nodes. No extracranial metastases."
    }
  ],
  "treatment_plan": {
    "intent": "palliative",
    "brain_metastases": {
      "treatment": "Stereotactic radiosurgery (SRS)",
      "date": "2025-01-22",
      "status": "completed"
    },
    "systemic_therapy": {
      "regimen": "Osimertinib 80 mg daily",
      "start_date": "2025-01-28",
      "rationale": "EGFR exon 19 deletion - CNS-penetrant TKI preferred",
      "status": "active"
    }
  },
  "medications": [
    {
      "name": "Osimertinib",
      "brand": "Tagrisso",
      "dose": "80 mg",
      "frequency": "daily",
      "indication": "EGFR-mutated NSCLC"
    },
    {
      "name": "Dexamethasone",
      "dose": "4 mg",
      "frequency": "BID",
      "indication": "Brain metastases edema",
      "status": "tapering"
    }
  ],
  "performance_status": {
    "ecog": 1,
    "description": "Restricted in physically strenuous activity but ambulatory"
  },
  "surveillance": {
    "mri_brain": "every 3 months",
    "ct_chest_abd_pelvis": "every 3 months",
    "clinical_assessment": "every 4 weeks"
  }
}
```

### Key Points
- EGFR mutation status determines first-line therapy
- Osimertinib preferred for brain metastases (CNS penetration)
- SRS for oligometastatic brain disease before starting TKI
- PD-L1 testing important but not used when driver mutation present
- Regular imaging surveillance to monitor response

### Variations
```
Generate an ALK-positive NSCLC patient on alectinib
Generate a NSCLC patient with high PD-L1 (>50%) on pembrolizumab monotherapy
Generate a KRAS G12C mutated NSCLC patient
Generate a small cell lung cancer (SCLC) limited stage patient
```

---

## Example 3: Colorectal Cancer with MSI-High Status

### Prompt
```
Generate a 58-year-old male with Stage III colon cancer, MSI-high, after curative resection
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000012",
    "name": { "given_name": "David", "family_name": "O'Brien" },
    "birth_date": "1966-04-18",
    "gender": "M"
  },
  "diagnoses": [
    {
      "code": "C18.2",
      "description": "Malignant neoplasm of ascending colon",
      "diagnosed_date": "2025-01-05",
      "status": "active",
      "staging": {
        "system": "AJCC_8th_edition",
        "stage_group": "IIIB",
        "pathologic_stage": "pT3 N1b M0"
      }
    }
  ],
  "biomarkers": {
    "msi_status": {
      "result": "MSI-High",
      "test_method": "IHC",
      "mlh1": "absent",
      "msh2": "present",
      "msh6": "present",
      "pms2": "absent"
    },
    "kras": { "status": "wild_type" },
    "nras": { "status": "wild_type" },
    "braf": { "status": "V600E_positive" },
    "her2": { "status": "negative" }
  },
  "pathology": {
    "histology": "adenocarcinoma",
    "differentiation": "moderately_differentiated",
    "tumor_size_cm": 5.2,
    "depth_of_invasion": "through muscularis propria into pericolorectal tissues",
    "lymph_nodes": {
      "examined": 18,
      "positive": 3
    },
    "margins": { "proximal": "negative", "distal": "negative" },
    "lymphovascular_invasion": true,
    "perineural_invasion": false,
    "tumor_deposits": 0
  },
  "surgery": {
    "procedure": "Right hemicolectomy",
    "date": "2025-01-08",
    "approach": "laparoscopic",
    "surgeon": "Dr. Patricia Kim",
    "status": "completed"
  },
  "genetic_counseling": {
    "status": "referred",
    "indication": "MSI-high tumor, BRAF V600E positive suggestive of sporadic MLH1 methylation",
    "lynch_syndrome_evaluation": "pending"
  },
  "treatment_plan": {
    "intent": "curative",
    "adjuvant_chemotherapy": {
      "regimen": "CAPOX",
      "details": "Capecitabine + Oxaliplatin",
      "duration": "3 months (6 cycles)",
      "start_date": "2025-02-05",
      "status": "active"
    }
  },
  "medications": [
    {
      "name": "Capecitabine",
      "dose": "1000 mg/m2",
      "frequency": "BID days 1-14 of 21-day cycle",
      "indication": "Adjuvant chemotherapy"
    },
    {
      "name": "Oxaliplatin",
      "dose": "130 mg/m2",
      "frequency": "Day 1 of 21-day cycle",
      "indication": "Adjuvant chemotherapy"
    },
    {
      "name": "Ondansetron",
      "dose": "8 mg",
      "frequency": "TID as needed",
      "indication": "Chemotherapy-induced nausea"
    }
  ],
  "labs": [
    {
      "test_name": "CEA",
      "loinc_code": "2039-6",
      "value": "2.8",
      "unit": "ng/mL",
      "reference_range": "<3.0",
      "collected_date": "2025-01-28",
      "note": "Post-operative, normalized"
    }
  ],
  "surveillance": {
    "cea": "every 3 months for 2 years, then every 6 months",
    "ct_chest_abd_pelvis": "every 6-12 months for 5 years",
    "colonoscopy": "1 year post-op, then per findings"
  }
}
```

### Key Points
- MSI-high status has prognostic and therapeutic implications
- BRAF V600E with MSI-H suggests sporadic (methylation) vs Lynch syndrome
- Stage III receives adjuvant chemotherapy
- 3-month adjuvant (IDEA trial) now standard for T1-3 N1
- CEA monitoring for recurrence surveillance
- Genetic counseling indicated for all MSI-H tumors

### Variations
```
Generate a rectal cancer patient requiring neoadjuvant chemoradiation (total neoadjuvant therapy)
Generate a metastatic colorectal cancer patient with liver-limited disease suitable for resection
Generate a Lynch syndrome patient with colorectal cancer
Generate a KRAS-mutated metastatic colorectal cancer patient
```

---

## Example 4: Cancer Patient with Comorbidities

### Prompt
```
Generate a 70-year-old male with Stage IIIB colon cancer who has CKD Stage 3b and Type 2 diabetes requiring chemotherapy dose adjustments
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000013",
    "name": { "given_name": "William", "family_name": "Patterson" },
    "birth_date": "1954-09-03",
    "gender": "M"
  },
  "diagnoses": [
    {
      "code": "C18.7",
      "description": "Malignant neoplasm of sigmoid colon",
      "diagnosed_date": "2025-01-10",
      "status": "active",
      "primary": true,
      "staging": {
        "system": "AJCC_8th_edition",
        "stage_group": "IIIB",
        "pathologic_stage": "pT3 N2a M0"
      }
    },
    {
      "code": "N18.32",
      "description": "Chronic kidney disease, stage 3b",
      "diagnosed_date": "2021-05-15",
      "status": "active"
    },
    {
      "code": "E11.65",
      "description": "Type 2 diabetes mellitus with hyperglycemia",
      "diagnosed_date": "2015-03-20",
      "status": "active"
    },
    {
      "code": "I10",
      "description": "Essential hypertension",
      "diagnosed_date": "2012-08-10",
      "status": "active"
    }
  ],
  "renal_function": {
    "creatinine": 1.9,
    "egfr": 38,
    "egfr_unit": "mL/min/1.73m2",
    "ckd_stage": "3b",
    "implications": "Requires chemotherapy dose adjustment"
  },
  "treatment_plan": {
    "intent": "curative",
    "adjuvant_chemotherapy": {
      "regimen": "Modified FOLFOX6 (dose-adjusted)",
      "modifications": [
        {
          "drug": "Oxaliplatin",
          "standard_dose": "85 mg/m2",
          "adjusted_dose": "65 mg/m2",
          "reason": "CKD Stage 3b - GFR 38"
        },
        {
          "drug": "5-FU bolus",
          "modification": "Omitted",
          "reason": "Reduce toxicity in setting of renal impairment"
        }
      ],
      "duration": "3 months (6 cycles)",
      "status": "active"
    }
  },
  "medications": [
    {
      "name": "Oxaliplatin",
      "dose": "65 mg/m2",
      "frequency": "Day 1 of 14-day cycle",
      "indication": "Adjuvant chemotherapy (dose-reduced for CKD)"
    },
    {
      "name": "Leucovorin",
      "dose": "400 mg/m2",
      "frequency": "Day 1 of 14-day cycle",
      "indication": "5-FU modulation"
    },
    {
      "name": "5-Fluorouracil",
      "dose": "2400 mg/m2",
      "frequency": "46-hour continuous infusion, Day 1-2",
      "indication": "Adjuvant chemotherapy"
    },
    {
      "name": "Metformin",
      "dose": "500 mg",
      "frequency": "BID",
      "indication": "Type 2 diabetes (dose reduced for CKD)",
      "note": "Reduced from 1000mg BID due to GFR <45"
    },
    {
      "name": "Glipizide",
      "dose": "5 mg",
      "frequency": "daily",
      "indication": "Type 2 diabetes"
    },
    {
      "name": "Lisinopril",
      "dose": "10 mg",
      "frequency": "daily",
      "indication": "Hypertension, diabetic nephropathy"
    }
  ],
  "labs": [
    {
      "test_name": "Creatinine",
      "value": "1.9",
      "unit": "mg/dL",
      "flag": "H"
    },
    {
      "test_name": "eGFR",
      "value": "38",
      "unit": "mL/min/1.73m2",
      "flag": "L"
    },
    {
      "test_name": "HbA1c",
      "value": "7.8",
      "unit": "%",
      "flag": "H"
    },
    {
      "test_name": "Glucose, Fasting",
      "value": "156",
      "unit": "mg/dL",
      "flag": "H"
    },
    {
      "test_name": "CEA",
      "value": "3.2",
      "unit": "ng/mL",
      "note": "Normalized post-resection"
    }
  ],
  "care_coordination": {
    "oncology": "Dr. James Mitchell - chemotherapy management",
    "nephrology": "Dr. Sarah Lee - CKD monitoring during treatment",
    "endocrinology": "Dr. Robert Chen - diabetes management with steroids",
    "tumor_board": "Discussed 2025-01-15, multi-disciplinary plan approved"
  },
  "monitoring_plan": {
    "renal_function": "CBC/CMP before each cycle",
    "glucose": "Daily home monitoring, may need adjustment with dexamethasone",
    "neuropathy": "Assessment before each cycle for oxaliplatin toxicity"
  },
  "performance_status": {
    "ecog": 1,
    "description": "Ambulatory, capable of self-care, unable to carry out strenuous work"
  }
}
```

### Key Points
- Oxaliplatin dose reduced 25% for GFR <45 mL/min
- 5-FU bolus often omitted in renal impairment
- Metformin requires dose reduction when GFR <45
- Multi-specialty coordination essential (oncology, nephrology, endocrine)
- Steroids in antiemetic regimen will worsen glucose control
- More frequent lab monitoring required

### Variations
```
Generate a cancer patient with heart failure requiring anthracycline avoidance
Generate an oncology patient on anticoagulation with thrombocytopenia risk
Generate a cancer patient with cirrhosis requiring dose adjustments
Generate a frail elderly patient (ECOG 2) with reduced dose chemotherapy
```

---

## Example 5: Cancer Survivorship

### Prompt
```
Generate a breast cancer survivor 5 years post-treatment in surveillance phase
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000014",
    "name": { "given_name": "Susan", "family_name": "Mitchell" },
    "birth_date": "1965-02-28",
    "gender": "F"
  },
  "cancer_history": {
    "primary_diagnosis": {
      "code": "Z85.3",
      "description": "Personal history of malignant neoplasm of breast",
      "original_diagnosis_date": "2020-01-15",
      "original_stage": "IIA",
      "molecular_subtype": "Luminal A (ER+/PR+/HER2-)"
    },
    "treatment_summary": {
      "surgery": {
        "procedure": "Left lumpectomy with sentinel lymph node biopsy",
        "date": "2020-02-10"
      },
      "radiation": {
        "type": "Whole breast radiation",
        "completion_date": "2020-04-15"
      },
      "systemic_therapy": {
        "hormonal": "Anastrozole 1mg daily x 5 years",
        "completion_date": "2025-02-15"
      }
    },
    "current_status": "No evidence of disease (NED)"
  },
  "diagnoses": [
    {
      "code": "Z85.3",
      "description": "Personal history of malignant neoplasm of breast",
      "status": "active"
    },
    {
      "code": "M81.0",
      "description": "Age-related osteoporosis without current pathological fracture",
      "diagnosed_date": "2022-06-10",
      "status": "active",
      "note": "Aromatase inhibitor-related"
    },
    {
      "code": "M25.511",
      "description": "Pain in right shoulder",
      "diagnosed_date": "2021-03-15",
      "status": "active",
      "note": "Aromatase inhibitor-related arthralgias"
    }
  ],
  "medications": [
    {
      "name": "Alendronate",
      "dose": "70 mg",
      "frequency": "weekly",
      "indication": "Osteoporosis (AI-related bone loss)"
    },
    {
      "name": "Calcium carbonate",
      "dose": "600 mg",
      "frequency": "BID",
      "indication": "Bone health"
    },
    {
      "name": "Vitamin D3",
      "dose": "2000 IU",
      "frequency": "daily",
      "indication": "Bone health"
    }
  ],
  "survivorship_care_plan": {
    "surveillance": {
      "mammogram": "Annual bilateral (or unilateral if mastectomy)",
      "clinical_breast_exam": "Every 6-12 months",
      "dexa_scan": "Every 2 years"
    },
    "late_effects_monitoring": {
      "bone_health": "Continue bisphosphonate, monitor DEXA",
      "cardiovascular": "Annual lipid panel, encourage exercise",
      "secondary_malignancy": "Standard age-appropriate cancer screening"
    },
    "lifestyle_recommendations": {
      "exercise": "150 minutes moderate activity per week",
      "weight": "Maintain healthy BMI",
      "alcohol": "Limit to <1 drink/day"
    }
  },
  "labs": [
    {
      "test_name": "Vitamin D, 25-OH",
      "value": "42",
      "unit": "ng/mL",
      "reference_range": "30-100",
      "status": "normal"
    }
  ],
  "imaging": [
    {
      "type": "Mammogram",
      "date": "2024-12-10",
      "result": "BIRADS 1 - Negative",
      "next_due": "2025-12-10"
    },
    {
      "type": "DEXA Scan",
      "date": "2024-06-15",
      "result": "T-score spine -2.6, hip -2.1",
      "interpretation": "Osteoporosis"
    }
  ],
  "next_appointments": [
    {
      "date": "2025-06-15",
      "provider": "Dr. Emily Rodriguez",
      "specialty": "Medical Oncology",
      "reason": "Annual survivorship visit"
    }
  ]
}
```

### Key Points
- Z85.3 code indicates personal history of breast cancer
- Long-term effects of aromatase inhibitors (osteoporosis, arthralgias)
- Survivorship care plan includes surveillance and late effects monitoring
- Annual mammogram remains standard for surveillance
- Lifestyle factors important for reducing recurrence risk
- Transition from active treatment to survivorship care

### Variations
```
Generate a lymphoma survivor with cardiac monitoring for prior anthracycline exposure
Generate a colorectal cancer survivor with colonoscopy surveillance
Generate a childhood cancer survivor with long-term follow-up needs
Generate a lung cancer survivor post-lobectomy
```

---

## Example 6: Oncology Emergency

### Prompt
```
Generate a patient presenting with febrile neutropenia during chemotherapy
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000015",
    "name": { "given_name": "Linda", "family_name": "Gonzalez" },
    "birth_date": "1970-07-22",
    "gender": "F"
  },
  "oncology_context": {
    "primary_cancer": "Breast cancer, Stage IIB",
    "current_treatment": {
      "regimen": "AC-T (dose-dense)",
      "current_cycle": "Cycle 3 of 4 AC",
      "last_treatment_date": "2025-01-20",
      "days_since_treatment": 10
    }
  },
  "presentation": {
    "chief_complaint": "Fever and chills",
    "onset": "6 hours ago",
    "symptoms": ["fever", "chills", "fatigue", "mild sore throat"],
    "no_localizing_symptoms": true
  },
  "diagnoses": [
    {
      "code": "D70.1",
      "description": "Agranulocytosis secondary to cancer chemotherapy",
      "status": "active"
    },
    {
      "code": "R50.81",
      "description": "Fever presenting with conditions classified elsewhere",
      "status": "active"
    },
    {
      "code": "C50.912",
      "description": "Malignant neoplasm of unspecified site of left female breast",
      "status": "active"
    }
  ],
  "vitals": {
    "temperature": "101.8 F (38.8 C)",
    "blood_pressure": "98/62",
    "heart_rate": "108",
    "respiratory_rate": "18",
    "oxygen_saturation": "97% on room air"
  },
  "labs": [
    {
      "test_name": "WBC",
      "value": "0.8",
      "unit": "x10^9/L",
      "reference_range": "4.5-11.0",
      "flag": "CRITICAL LOW"
    },
    {
      "test_name": "ANC",
      "value": "0.2",
      "unit": "x10^9/L",
      "reference_range": ">1.5",
      "flag": "CRITICAL LOW",
      "interpretation": "Severe neutropenia"
    },
    {
      "test_name": "Hemoglobin",
      "value": "10.2",
      "unit": "g/dL",
      "flag": "L"
    },
    {
      "test_name": "Platelets",
      "value": "145",
      "unit": "x10^9/L",
      "status": "normal"
    },
    {
      "test_name": "Creatinine",
      "value": "0.9",
      "unit": "mg/dL",
      "status": "normal"
    },
    {
      "test_name": "Lactate",
      "value": "1.8",
      "unit": "mmol/L",
      "reference_range": "<2.0",
      "status": "normal"
    }
  ],
  "risk_stratification": {
    "mascc_score": 18,
    "interpretation": "High-risk febrile neutropenia (MASCC <21)",
    "factors": ["inpatient at onset", "hypotension", "active cancer on chemo"]
  },
  "workup_ordered": [
    "Blood cultures x2 (peripheral)",
    "Urinalysis and culture",
    "Chest X-ray",
    "Respiratory viral panel"
  ],
  "treatment": {
    "disposition": "Admission to oncology unit",
    "antibiotics": {
      "empiric_regimen": "Cefepime 2g IV q8h",
      "start_time": "Within 1 hour of presentation",
      "rationale": "Anti-pseudomonal beta-lactam for febrile neutropenia"
    },
    "supportive_care": [
      "IV fluids for hypotension",
      "Strict neutropenic precautions",
      "Daily CBC monitoring"
    ],
    "growth_factor": {
      "medication": "Pegfilgrastim",
      "timing": "Consider if prolonged neutropenia expected",
      "status": "pending oncology input"
    }
  },
  "oncology_notification": {
    "attending": "Dr. Michael Rivera",
    "notified": true,
    "recommendations": "Continue antibiotics, may add G-CSF, will evaluate in AM"
  }
}
```

### Key Points
- Febrile neutropenia is an oncologic emergency
- ANC <500 with fever requires immediate broad-spectrum antibiotics
- Time to antibiotics is critical (within 1 hour)
- MASCC score helps risk-stratify patients
- Blood cultures before antibiotics if possible, but don't delay treatment
- Growth factors may be indicated for high-risk patients

### Variations
```
Generate a patient with tumor lysis syndrome
Generate a patient with malignant spinal cord compression
Generate a patient with superior vena cava syndrome
Generate a patient with hypercalcemia of malignancy
```

---

## More Examples

See also:
- [PatientSim Examples](patientsim-examples.md) - General clinical data
- [MemberSim Examples](membersim-examples.md) - Claims with oncology scenarios
- [RxMemberSim Examples](rxmembersim-examples.md) - Specialty pharmacy for oncology drugs
- [Cross-Domain Examples](cross-domain-examples.md) - Complete oncology journeys
- [Format Examples](format-examples.md) - Export oncology data as FHIR or HL7v2
