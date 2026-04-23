# PatientSim Examples

Generate realistic clinical data including patients, diagnoses, medications, and lab results.

---

## Example 1: Simple Patient

### Prompt
```
Generate a patient
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": {
      "given_name": "Robert",
      "family_name": "Johnson"
    },
    "birth_date": "1978-06-15",
    "gender": "M",
    "address": {
      "street_address": "456 Oak Avenue",
      "city": "Springfield",
      "state": "IL",
      "postal_code": "62704"
    },
    "phone": "217-555-0142",
    "ssn_last_four": "4521"
  }
}
```

### Key Points
- Random demographics generated
- MRN follows pattern MRN + 8 digits
- Realistic US address and phone

### Variations
```
Generate a 45-year-old female patient
Generate a pediatric patient (age 8)
Generate an elderly patient over 80
```

---

## Example 2: Diabetic Patient

### Prompt
```
Generate a 62-year-old male with Type 2 diabetes
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000002",
    "name": { "given_name": "William", "family_name": "Martinez" },
    "birth_date": "1962-09-23",
    "gender": "M"
  },
  "diagnoses": [
    {
      "code": "E11.9",
      "description": "Type 2 diabetes mellitus without complications",
      "diagnosed_date": "2018-03-15",
      "status": "active"
    },
    {
      "code": "I10",
      "description": "Essential hypertension",
      "diagnosed_date": "2017-06-20",
      "status": "active"
    },
    {
      "code": "E78.5",
      "description": "Hyperlipidemia, unspecified",
      "diagnosed_date": "2018-03-15",
      "status": "active"
    }
  ],
  "medications": [
    {
      "name": "Metformin",
      "rxnorm_code": "860975",
      "dose": "1000 mg",
      "route": "PO",
      "frequency": "BID",
      "status": "active"
    },
    {
      "name": "Lisinopril",
      "rxnorm_code": "314076",
      "dose": "20 mg",
      "route": "PO",
      "frequency": "QD",
      "status": "active"
    },
    {
      "name": "Atorvastatin",
      "rxnorm_code": "617312",
      "dose": "40 mg",
      "route": "PO",
      "frequency": "QD",
      "status": "active"
    }
  ],
  "labs": [
    {
      "test_name": "HbA1c",
      "loinc_code": "4548-4",
      "value": "7.2",
      "unit": "%",
      "reference_range": "4.0-5.6",
      "flag": "H",
      "collected_date": "2025-01-10"
    },
    {
      "test_name": "Glucose, Fasting",
      "loinc_code": "1558-6",
      "value": "142",
      "unit": "mg/dL",
      "reference_range": "70-100",
      "flag": "H",
      "collected_date": "2025-01-10"
    }
  ]
}
```

### Key Points
- Comorbidities added (HTN, hyperlipidemia are common with diabetes)
- Medications match conditions
- Labs reflect disease state (elevated A1C, glucose)
- All codes are real (ICD-10, RxNorm, LOINC)

### Variations
```
Generate a poorly controlled diabetic with A1C of 9.5
Generate a diabetic with nephropathy complications
Generate a newly diagnosed Type 2 diabetic
```

---

## Example 3: Heart Failure Patient

### Prompt
```
Generate a 75-year-old with heart failure, NYHA Class III
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000003",
    "name": { "given_name": "Dorothy", "family_name": "Williams" },
    "birth_date": "1949-04-12",
    "gender": "F"
  },
  "diagnoses": [
    {
      "code": "I50.22",
      "description": "Chronic systolic (congestive) heart failure",
      "diagnosed_date": "2020-08-10",
      "status": "active"
    },
    {
      "code": "I48.91",
      "description": "Unspecified atrial fibrillation",
      "diagnosed_date": "2021-02-15",
      "status": "active"
    },
    {
      "code": "I10",
      "description": "Essential hypertension",
      "diagnosed_date": "2005-11-20",
      "status": "active"
    },
    {
      "code": "N18.3",
      "description": "Chronic kidney disease, stage 3",
      "diagnosed_date": "2022-06-01",
      "status": "active"
    }
  ],
  "medications": [
    {
      "name": "Sacubitril/Valsartan",
      "dose": "97/103 mg",
      "frequency": "BID",
      "indication": "Heart failure"
    },
    {
      "name": "Carvedilol",
      "dose": "25 mg",
      "frequency": "BID",
      "indication": "Heart failure, AFib rate control"
    },
    {
      "name": "Spironolactone",
      "dose": "25 mg",
      "frequency": "QD",
      "indication": "Heart failure"
    },
    {
      "name": "Furosemide",
      "dose": "40 mg",
      "frequency": "BID",
      "indication": "Fluid management"
    },
    {
      "name": "Apixaban",
      "dose": "5 mg",
      "frequency": "BID",
      "indication": "AFib anticoagulation"
    }
  ],
  "labs": [
    {
      "test_name": "BNP",
      "loinc_code": "30934-4",
      "value": "650",
      "unit": "pg/mL",
      "reference_range": "<100",
      "flag": "H"
    },
    {
      "test_name": "Creatinine",
      "loinc_code": "2160-0",
      "value": "1.6",
      "unit": "mg/dL",
      "flag": "H"
    },
    {
      "test_name": "eGFR",
      "loinc_code": "48642-3",
      "value": "42",
      "unit": "mL/min/1.73m2",
      "flag": "L"
    },
    {
      "test_name": "Potassium",
      "loinc_code": "2823-3",
      "value": "4.8",
      "unit": "mEq/L"
    }
  ],
  "vitals": {
    "weight": "185 lbs",
    "blood_pressure": "118/72",
    "heart_rate": "78",
    "oxygen_saturation": "94%"
  },
  "functional_status": {
    "nyha_class": "III",
    "ejection_fraction": "30%",
    "description": "Marked limitation of physical activity. Comfortable at rest. Less than ordinary activity causes fatigue, palpitation, or dyspnea."
  }
}
```

### Key Points
- GDMT (guideline-directed medical therapy) medications included
- AFib common comorbidity with anticoagulation
- BNP elevated consistent with NYHA III
- CKD common in heart failure patients
- EF reduced (HFrEF) matching systolic HF diagnosis

### Variations
```
Generate a heart failure patient with preserved ejection fraction (HFpEF)
Generate a decompensated heart failure requiring hospitalization
Generate a post-MI patient with new heart failure
```

---

## Example 4: Patient with Encounter

### Prompt
```
Generate an outpatient encounter for a diabetic follow-up visit
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000004",
    "name": { "given_name": "James", "family_name": "Anderson" },
    "birth_date": "1965-12-08",
    "gender": "M"
  },
  "encounter": {
    "encounter_id": "ENC20250115001",
    "class": "outpatient",
    "type": "office visit",
    "status": "finished",
    "start_time": "2025-01-15T10:30:00",
    "end_time": "2025-01-15T11:00:00",
    "location": {
      "facility": "Springfield Medical Associates",
      "department": "Internal Medicine"
    },
    "provider": {
      "npi": "1234567890",
      "name": "Dr. Sarah Chen",
      "specialty": "Internal Medicine"
    },
    "reason_for_visit": "Diabetes mellitus follow-up",
    "chief_complaint": "Here for diabetes check, feeling well"
  },
  "diagnoses": [
    { "code": "E11.65", "description": "Type 2 diabetes with hyperglycemia" },
    { "code": "I10", "description": "Essential hypertension" }
  ],
  "vitals": {
    "blood_pressure": "138/82",
    "heart_rate": "76",
    "weight": "198 lbs",
    "height": "5'10\"",
    "bmi": "28.4"
  },
  "labs_ordered": [
    { "test": "HbA1c", "loinc": "4548-4" },
    { "test": "Comprehensive Metabolic Panel", "loinc": "24323-8" },
    { "test": "Lipid Panel", "loinc": "24331-1" }
  ],
  "assessment_plan": [
    {
      "diagnosis": "Type 2 diabetes mellitus",
      "assessment": "A1C at goal (7.1%), continue current regimen",
      "plan": "Continue metformin 1000mg BID, recheck A1C in 3 months"
    },
    {
      "diagnosis": "Hypertension",
      "assessment": "Blood pressure slightly elevated today",
      "plan": "Continue lisinopril 20mg daily, patient to monitor at home"
    }
  ],
  "follow_up": "Return in 3 months for diabetes follow-up"
}
```

### Key Points
- Complete encounter with timing
- Provider details included
- Vitals appropriate for patient
- Labs ordered match clinical context
- Assessment and plan documented

---

## Example 5: Inpatient Admission

### Prompt
```
Generate an admission for a patient with pneumonia, including ADT events
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000005",
    "name": { "given_name": "Margaret", "family_name": "Thompson" },
    "birth_date": "1952-07-30",
    "gender": "F"
  },
  "admission": {
    "encounter_id": "ENC20250115002",
    "class": "inpatient",
    "admit_source": "Emergency Room",
    "admit_type": "Emergency",
    "admit_datetime": "2025-01-14T18:45:00",
    "attending_physician": {
      "npi": "1234567890",
      "name": "Dr. Michael Roberts"
    }
  },
  "adt_events": [
    {
      "event_type": "A01",
      "event_description": "Admit/Visit Notification",
      "datetime": "2025-01-14T18:45:00",
      "location": {
        "unit": "Medical 3A",
        "room": "312",
        "bed": "A"
      }
    },
    {
      "event_type": "A02",
      "event_description": "Transfer",
      "datetime": "2025-01-15T08:30:00",
      "from_location": { "unit": "Medical 3A", "room": "312", "bed": "A" },
      "to_location": { "unit": "Telemetry 4B", "room": "425", "bed": "A" },
      "reason": "Cardiac monitoring required"
    }
  ],
  "diagnoses": [
    {
      "code": "J18.9",
      "description": "Pneumonia, unspecified organism",
      "type": "admitting",
      "poa": "Y"
    },
    {
      "code": "J96.01",
      "description": "Acute respiratory failure with hypoxia",
      "type": "secondary",
      "poa": "Y"
    },
    {
      "code": "I48.91",
      "description": "Atrial fibrillation",
      "type": "secondary",
      "poa": "Y"
    }
  ],
  "vitals_on_admission": {
    "temperature": "101.8 F",
    "blood_pressure": "98/62",
    "heart_rate": "112",
    "respiratory_rate": "24",
    "oxygen_saturation": "88% on room air"
  },
  "orders": [
    {
      "order_type": "Medication",
      "order": "Ceftriaxone 1g IV q24h",
      "indication": "Pneumonia"
    },
    {
      "order_type": "Medication",
      "order": "Azithromycin 500mg IV q24h",
      "indication": "Pneumonia"
    },
    {
      "order_type": "Respiratory",
      "order": "Oxygen 4L/min nasal cannula",
      "indication": "Hypoxia"
    },
    {
      "order_type": "Lab",
      "order": "CBC, BMP, Procalcitonin, Blood cultures x2"
    },
    {
      "order_type": "Imaging",
      "order": "Chest X-ray portable"
    }
  ],
  "current_status": {
    "location": { "unit": "Telemetry 4B", "room": "425", "bed": "A" },
    "condition": "Stable",
    "level_of_care": "Acute"
  }
}
```

### Key Points
- ADT events track patient movement
- Present on Admission (POA) indicators included
- Vitals consistent with sepsis/pneumonia presentation
- Orders appropriate for community-acquired pneumonia
- Transfer documented with reason

---

## More Examples

See also:
- [Cross-Domain Examples](cross-domain-examples.md) - Combine with claims
- [Format Examples](format-examples.md) - Output as FHIR or HL7v2
