# Full Ecosystem Integration Cohort

## Overview

This cohort demonstrates end-to-end integration across the entire HealthSim ecosystem, following a family through enrollment, clinical care, and clinical trial participation—all anchored by PopulationSim demographic and SDOH foundations.

---

## Cohort: The Garcia Family Journey

### Family Profile

The Garcia family lives in a high-vulnerability census tract in Houston, Texas. This cohort traces their healthcare journey across all HealthSim products.

```
┌─────────────────────────────────────────────────────────────────┐
│                     The Garcia Family                            │
│                                                                  │
│  Maria Garcia (49)          Carlos Garcia (52)                  │
│  - Type 2 Diabetes          - Hypertension                      │
│  - Hypertension             - Hyperlipidemia                    │
│  - Food insecurity          - Food insecurity                   │
│                                                                  │
│  Sofia Garcia (22)          Miguel Garcia (17)                  │
│  - Asthma                   - Healthy                           │
│  - Young adult              - High school student               │
│                                                                  │
│  Location: Census Tract 48201311500, Harris County, TX          │
│  SVI: 0.78  |  ADI: 76  |  Median Income: $42,500               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Population Foundation (PopulationSim)

### Census Tract Profile

```json
{
  "geography": {
    "type": "tract",
    "fips": "48201311500",
    "name": "Tract 3115.00",
    "county": "Harris County",
    "state": "TX"
  },
  
  "demographics": {
    "total_population": 4200,
    "median_age": 32.4,
    "race_ethnicity": {
      "hispanic": 0.68,
      "black_nh": 0.14,
      "white_nh": 0.12,
      "asian_nh": 0.04
    }
  },
  
  "health_indicators": {
    "diabetes": 0.128,
    "hypertension": 0.362,
    "asthma": 0.098,
    "obesity": 0.348
  },
  
  "sdoh_profile": {
    "svi": {
      "overall": 0.78,
      "theme_1_socioeconomic": 0.72,
      "theme_3_minority_language": 0.88
    },
    "adi_national_percentile": 76,
    "economic": {
      "median_household_income": 42500,
      "poverty_rate": 0.228
    },
    "z_code_rates": {
      "Z59.6": 0.182,
      "Z59.41": 0.148,
      "Z56.0": 0.072
    }
  },
  
  "healthcare_access": {
    "insurance_coverage": {
      "commercial": 0.42,
      "medicare": 0.12,
      "medicaid": 0.28,
      "uninsured": 0.18
    }
  }
}
```

---

## Step 2: Family Member Generation (PatientSim)

### Maria Garcia - Patient Record

```json
{
  "patient": {
    "id": "patient-maria-001",
    "mrn": "MRN-789012",
    "ssn": "123-45-6789",
    
    "demographics": {
      "name": {"given": ["Maria", "Elena"], "family": "Garcia"},
      "birthDate": "1975-03-15",
      "gender": "female",
      "race": "white",
      "ethnicity": "Hispanic or Latino",
      "language": "Spanish",
      "address": {
        "line": ["4521 Telephone Rd, Apt 4B"],
        "city": "Houston",
        "state": "TX",
        "postalCode": "77023"
      }
    },
    
    "conditions": [
      {
        "code": "E11.65",
        "display": "Type 2 diabetes with hyperglycemia",
        "onset": "2018-06-15",
        "status": "active"
      },
      {
        "code": "I10",
        "display": "Essential hypertension",
        "onset": "2016-02-10",
        "status": "active"
      },
      {
        "code": "E66.01",
        "display": "Morbid obesity due to excess calories",
        "onset": "2015-08-22",
        "status": "active"
      },
      {
        "code": "Z59.6",
        "display": "Low income",
        "category": "sdoh"
      },
      {
        "code": "Z59.41",
        "display": "Food insecurity",
        "category": "sdoh"
      }
    ],
    
    "medications": [
      {"name": "Metformin", "dose": "1000mg", "frequency": "BID"},
      {"name": "Lisinopril", "dose": "20mg", "frequency": "daily"},
      {"name": "Atorvastatin", "dose": "40mg", "frequency": "daily"}
    ],
    
    "recent_labs": {
      "hba1c": {"value": 8.4, "date": "2024-09-01"},
      "egfr": {"value": 68, "date": "2024-09-01"},
      "ldl": {"value": 128, "date": "2024-09-01"}
    }
  }
}
```

### Carlos Garcia - Patient Record

```json
{
  "patient": {
    "id": "patient-carlos-001",
    "mrn": "MRN-789013",
    "ssn": "234-56-7890",
    
    "demographics": {
      "name": {"given": ["Carlos", "Miguel"], "family": "Garcia"},
      "birthDate": "1972-07-22",
      "gender": "male",
      "race": "white",
      "ethnicity": "Hispanic or Latino"
    },
    
    "conditions": [
      {"code": "I10", "display": "Essential hypertension"},
      {"code": "E78.5", "display": "Hyperlipidemia"},
      {"code": "Z59.6", "display": "Low income", "category": "sdoh"},
      {"code": "Z59.41", "display": "Food insecurity", "category": "sdoh"}
    ]
  }
}
```

### Family Relationships

```json
{
  "family_unit": {
    "household_id": "HH-GARCIA-001",
    "address": "4521 Telephone Rd, Apt 4B, Houston, TX 77023",
    "members": [
      {"ssn": "123-45-6789", "role": "head", "name": "Maria Garcia"},
      {"ssn": "234-56-7890", "role": "spouse", "name": "Carlos Garcia"},
      {"ssn": "345-67-8901", "role": "child", "name": "Sofia Garcia"},
      {"ssn": "456-78-9012", "role": "child", "name": "Miguel Garcia"}
    ],
    "household_income": 48000,
    "fpl_percentage": 185,
    "sdoh_shared": ["Z59.41", "Z59.6"]
  }
}
```

---

## Step 3: Health Plan Enrollment (MemberSim)

### Family Enrollment Decision Tree

```
Household Income: $48,000 (185% FPL for family of 4)

├── Maria & Carlos: Employer Coverage (small business)
│   ├── Plan: Employer HMO Bronze
│   ├── Premium: $680/month (employer pays $400)
│   └── High deductible, moderate copays
│
├── Sofia (22): Aged off parents' plan
│   ├── ACA Exchange enrollment
│   ├── Plan: Silver CSR (income 185% FPL)
│   └── Subsidy: $320/month
│
└── Miguel (17): Dependent coverage
    └── Covered under parents' employer plan
```

### Maria's Member Record

```json
{
  "member": {
    "member_id": "MEM-456789",
    "subscriber_id": "SUB-123456",
    "ssn": "123-45-6789",
    "relationship": "subscriber",
    
    "enrollment": {
      "plan": {
        "plan_id": "EMP-HMO-BRONZE-2024",
        "plan_name": "SmallBiz HMO Bronze",
        "plan_type": "HMO",
        "metal_tier": "bronze",
        "carrier": "Blue Cross Blue Shield"
      },
      "effective_date": "2024-01-01",
      "coverage_tier": "employee_plus_family"
    },
    
    "benefits": {
      "deductible_individual": 4500,
      "deductible_family": 9000,
      "oop_max_individual": 8500,
      "oop_max_family": 17000,
      "copay_pcp": 40,
      "copay_specialist": 75,
      "copay_er": 350
    },
    
    "accumulators": {
      "deductible_met": 3200,
      "oop_met": 4100,
      "as_of_date": "2024-10-01"
    },
    
    "sdoh_context": {
      "care_management_enrolled": true,
      "chronic_care_program": "diabetes_management",
      "community_health_worker": true,
      "food_insecurity_referral": true
    }
  }
}
```

### Sofia's Exchange Member Record

```json
{
  "member": {
    "member_id": "MEM-567890",
    "ssn": "345-67-8901",
    "relationship": "self",
    
    "enrollment": {
      "plan": {
        "plan_id": "ACA-SILVER-CSR94-2024",
        "plan_name": "Ambetter Silver CSR 94",
        "plan_type": "HMO",
        "metal_tier": "silver",
        "csr_variant": "94"
      },
      "effective_date": "2024-01-01",
      "marketplace": "healthcare.gov",
      "aptc_amount": 320,
      "premium_after_aptc": 45
    },
    
    "benefits": {
      "deductible_individual": 75,
      "oop_max_individual": 1150,
      "copay_pcp": 0,
      "copay_specialist": 5
    }
  }
}
```

---

## Step 4: Clinical Encounters (PatientSim)

### Maria's Encounters - 2024

```json
{
  "encounters": [
    {
      "encounter_id": "ENC-2024-001",
      "type": "office_visit",
      "date": "2024-02-15",
      "provider": "Dr. Sarah Chen, MD",
      "facility": "Community Health Center",
      "reason": "Diabetes follow-up",
      "diagnoses": ["E11.65", "I10", "Z59.41"],
      "procedures": [
        {"code": "99214", "description": "Office visit, moderate"}
      ],
      "orders": [
        {"type": "lab", "code": "83036", "name": "HbA1c"},
        {"type": "lab", "code": "80053", "name": "CMP"}
      ],
      "sdoh_actions": [
        "Referred to food pantry program",
        "Connected with CHW for nutrition counseling"
      ]
    },
    
    {
      "encounter_id": "ENC-2024-002",
      "type": "ed_visit",
      "date": "2024-05-22",
      "facility": "Ben Taub Hospital ED",
      "reason": "Hyperglycemia, nausea",
      "diagnoses": ["E11.65", "R11.10"],
      "disposition": "discharged",
      "sdoh_context": {
        "barrier_noted": "Ran out of metformin - cost concern",
        "referral": "Patient assistance program"
      }
    },
    
    {
      "encounter_id": "ENC-2024-003",
      "type": "office_visit",
      "date": "2024-06-10",
      "provider": "Dr. Sarah Chen, MD",
      "reason": "Post-ED follow-up",
      "diagnoses": ["E11.65", "I10", "Z59.6"],
      "notes": "Enrolled in 340B pharmacy program for medications"
    },
    
    {
      "encounter_id": "ENC-2024-004",
      "type": "specialist_visit",
      "date": "2024-09-15",
      "provider": "Dr. Michael Rodriguez, Endocrinology",
      "reason": "Diabetes management optimization",
      "diagnoses": ["E11.65", "E11.40"],
      "procedures": [
        {"code": "99214", "description": "Office visit"},
        {"code": "83036", "name": "HbA1c"}
      ],
      "clinical_trial_discussion": {
        "protocol": "DM-CARDIO-2024-001",
        "interest_expressed": true,
        "referral_to_research": true
      }
    }
  ]
}
```

---

## Step 5: Claims Generation (MemberSim)

### Maria's 2024 Claims

```json
{
  "claims": [
    {
      "claim_id": "CLM-2024-00123",
      "member_id": "MEM-456789",
      "claim_type": "professional",
      "service_date": "2024-02-15",
      "provider_npi": "1234567890",
      "place_of_service": "11",
      "diagnoses": [
        {"code": "E11.65", "pointer": 1},
        {"code": "I10", "pointer": 2},
        {"code": "Z59.41", "pointer": 3}
      ],
      "procedures": [
        {"code": "99214", "modifier": null, "charge": 185.00, "units": 1}
      ],
      "amounts": {
        "billed": 185.00,
        "allowed": 142.00,
        "paid": 0.00,
        "patient_responsibility": 142.00,
        "applied_to_deductible": 142.00
      }
    },
    
    {
      "claim_id": "CLM-2024-00456",
      "claim_type": "facility",
      "service_date": "2024-05-22",
      "facility_npi": "9876543210",
      "bill_type": "131",
      "diagnoses": [
        {"code": "E11.65", "pointer": 1},
        {"code": "R11.10", "pointer": 2}
      ],
      "revenue_codes": [
        {"code": "0450", "description": "ED", "charge": 1250.00}
      ],
      "amounts": {
        "billed": 1250.00,
        "allowed": 850.00,
        "paid": 0.00,
        "patient_responsibility": 350.00,
        "applied_to_deductible": 500.00
      }
    },
    
    {
      "claim_id": "CLM-2024-00789",
      "claim_type": "pharmacy",
      "service_date": "2024-06-15",
      "pharmacy_npi": "5678901234",
      "prescriptions": [
        {
          "ndc": "00087607101",
          "drug_name": "Metformin 1000mg",
          "quantity": 60,
          "days_supply": 30,
          "daw": 0,
          "charge": 45.00,
          "allowed": 12.00,
          "patient_pay": 0.00,
          "program": "340B"
        }
      ]
    }
  ]
}
```

---

## Step 6: Clinical Trial Participation (TrialSim)

### Trial Screening

```json
{
  "screening": {
    "screening_id": "SCR-2024-0042",
    "protocol_id": "DM-CARDIO-2024-001",
    "subject_candidate": {
      "ssn": "123-45-6789",
      "name": "Maria Garcia"
    },
    "screening_date": "2024-10-01",
    
    "eligibility_assessment": {
      "inclusion_criteria": [
        {"criterion": "age_40_75", "value": 49, "status": "pass"},
        {"criterion": "t2dm_diagnosis", "duration_months": 76, "status": "pass"},
        {"criterion": "hba1c_7_10.5", "value": 8.4, "status": "pass"},
        {"criterion": "cv_risk", "type": "hypertension", "status": "pass"}
      ],
      "exclusion_criteria": [
        {"criterion": "esrd", "status": "not_present"},
        {"criterion": "active_cancer", "status": "not_present"},
        {"criterion": "pregnancy", "status": "not_applicable"}
      ],
      "overall": "eligible"
    },
    
    "sdoh_assessment": {
      "barriers": [
        {"type": "transportation", "severity": "low", "has_vehicle": true},
        {"type": "work_schedule", "severity": "moderate", "prefers_evening": true},
        {"type": "language", "severity": "moderate", "spanish_preferred": true},
        {"type": "food_insecurity", "severity": "moderate", "fasting_concern": true}
      ],
      "accommodations": [
        "Spanish consent form and materials",
        "Bilingual study coordinator",
        "Evening visit availability",
        "Meals provided at study visits",
        "Enhanced stipend ($75 per visit)"
      ]
    }
  }
}
```

### Subject Enrollment

```json
{
  "subject": {
    "subject_id": "SUBJ-DM-CARDIO-042",
    "protocol_id": "DM-CARDIO-2024-001",
    "site": "Houston Methodist Research Institute",
    
    "person": {
      "ssn": "123-45-6789",
      "first_name": "Maria",
      "last_name": "Garcia"
    },
    
    "enrollment": {
      "consent_date": "2024-10-08",
      "consent_version": "3.0",
      "consent_language": "Spanish",
      "randomization_date": "2024-10-15",
      "randomization_arm": "treatment",
      "subject_number": 42
    },
    
    "diversity_contribution": {
      "race": "white",
      "ethnicity": "hispanic",
      "sex": "female",
      "age_group": "45-54"
    },
    
    "sdoh_support_plan": {
      "transportation": "self_transport",
      "language_support": "spanish_coordinator",
      "visit_timing": "evening_preferred",
      "stipend_enhanced": true,
      "meals_provided": true
    }
  }
}
```

---

## Identity Correlation Summary

### Garcia Family Cross-Product IDs

| Person | SSN | PatientSim MRN | MemberSim ID | TrialSim ID |
|--------|-----|----------------|--------------|-------------|
| Maria | 123-45-6789 | MRN-789012 | MEM-456789 | SUBJ-DM-CARDIO-042 |
| Carlos | 234-56-7890 | MRN-789013 | MEM-456790 | - |
| Sofia | 345-67-8901 | MRN-789014 | MEM-567890 | - |
| Miguel | 456-78-9012 | MRN-789015 | MEM-456791 | - |

---

## Data Flow Validation

```
PopulationSim (Tract 48201311500)
    │
    ├── Demographics → All family members match tract distribution
    │
    ├── Health Indicators → Maria's diabetes consistent with 12.8% prevalence
    │
    ├── SDOH Profile → Z59.6, Z59.41 applied to family
    │
    └── Insurance Mix → Family coverage reflects 42% commercial rate
          │
          ▼
PatientSim
    │
    ├── Patient records with correlated SSNs
    ├── Conditions with SDOH Z-codes
    └── Encounters with barrier documentation
          │
          ▼
MemberSim
    │
    ├── Enrollment records linked by SSN
    ├── Claims with SDOH diagnosis codes
    └── Care management flags active
          │
          ▼
TrialSim
    │
    ├── Subject linked by SSN
    ├── Eligibility from clinical history
    └── SDOH accommodations from profile
```

---

## Related Cohorts

- [Population to Patient](population-to-patient.md)
- [Population to Member](population-to-member.md)
- [Population to Trial](population-to-trial.md)
