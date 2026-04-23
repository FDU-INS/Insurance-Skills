---
name: formulary-for-rx
description: |
  Add formulary context to RxMemberSim prescriptions including tier placement,
  prior authorization requirements, step therapy protocols, and quantity limits.
  Supports coverage determination and clinical program application.
  
  Trigger phrases: "formulary for this drug", "is drug covered", "prior auth required",
  "step therapy for", "formulary tier", "quantity limit", "drug coverage",
  "therapeutic alternative", "formulary exception"
version: "1.0"
category: integration
related_skills:
  - synthetic-pharmacy-benefit
  - pharmacy-benefit-patterns
  - pharmacy-benefit-concepts
  - utilization-management
cross_product:
  - rxmembersim
---

# Formulary for Rx

## Overview

This integration skill adds formulary context to RxMemberSim prescriptions. It determines formulary status, tier placement, and clinical program requirements (prior authorization, step therapy, quantity limits) for prescription adjudication.

Use this skill when you need to:
- Determine if a drug is covered on formulary
- Identify formulary tier and cost sharing
- Check prior authorization requirements
- Apply step therapy protocols
- Enforce quantity limits
- Identify therapeutic alternatives
- Handle formulary exceptions

---

## Integration Pattern

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   RxMemberSim   │     │   Formulary for      │     │   NetworkSim    │
│   Prescription  │────▶│   Rx Skill           │────▶│   Formulary +   │
│                 │     │   (Coverage Logic)   │     │   Clinical Pgms │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

---

## Input Context

### Drug Context

```json
{
  "drug_context": {
    "ndc": "00006-0277-31",
    "drug_name": "Lipitor",
    "generic_name": "atorvastatin",
    "strength": "20mg",
    "dosage_form": "Tablet",
    "route": "Oral",
    "manufacturer": "Pfizer",
    "gpi": "3940200000",
    "therapeutic_class": "Statins",
    "ahfs_class": "24:06.08",
    "dea_schedule": null,
    "specialty_indicator": false
  }
}
```

### Prescription Context

```json
{
  "prescription_context": {
    "rx_number": "RX-2024-0012345",
    "quantity_prescribed": 90,
    "days_supply": 90,
    "prescriber": {
      "npi": "1234567890",
      "specialty": "Internal Medicine"
    },
    "diagnosis": {
      "code": "E78.0",
      "description": "Hyperlipidemia"
    },
    "prior_fills": 0,
    "new_therapy": true
  }
}
```

### Member Benefit Context

```json
{
  "member_benefit": {
    "member_id": "MEM-2024-001234",
    "formulary_id": "ESI-STANDARD-2024",
    "effective_date": "2024-01-01",
    "pbm": "Express Scripts",
    "tier_structure": {
      "tier_count": 4,
      "specialty_tier": 4
    }
  }
}
```

---

## Formulary Lookup Logic

### Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│                    Formulary Coverage Check                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │  Is drug on formulary?       │
               └──────────────────────────────┘
                      │              │
                     YES            NO
                      │              │
                      ▼              ▼
          ┌──────────────┐    ┌──────────────────┐
          │ Get tier     │    │ Check if         │
          │ assignment   │    │ excluded or      │
          └──────────────┘    │ non-formulary    │
                 │            └──────────────────┘
                 ▼                   │
          ┌──────────────┐          │
          │ Check        │          ▼
          │ clinical     │    ┌──────────────┐
          │ programs     │    │ Reject or    │
          └──────────────┘    │ high tier    │
                 │            └──────────────┘
                 ▼
          ┌──────────────┐
          │ Return tier  │
          │ + programs   │
          └──────────────┘
```

### Lookup Steps

```json
{
  "lookup_steps": [
    {
      "step": 1,
      "action": "Check formulary coverage by NDC/GPI",
      "query": "formulary_status, tier_id FROM formulary WHERE formulary_id = ? AND (ndc = ? OR gpi LIKE ?)"
    },
    {
      "step": 2,
      "action": "Get tier details and cost sharing",
      "output": "tier_name, copay, coinsurance"
    },
    {
      "step": 3,
      "action": "Check prior authorization list",
      "query": "pa_required, pa_criteria FROM pa_list WHERE drug_id = ?"
    },
    {
      "step": 4,
      "action": "Check step therapy protocols",
      "query": "st_required, step_drugs FROM step_therapy WHERE target_drug_id = ?"
    },
    {
      "step": 5,
      "action": "Check quantity limits",
      "query": "ql_type, quantity_per_period, period FROM quantity_limits WHERE drug_id = ?"
    }
  ]
}
```

---

## Output Schema

### Covered Drug - No Restrictions

```json
{
  "formulary_status": {
    "rx_number": "RX-2024-0012345",
    "drug": {
      "ndc": "00093-0677-01",
      "drug_name": "Atorvastatin 20mg",
      "brand_generic": "Generic"
    },
    
    "coverage": {
      "covered": true,
      "formulary_id": "ESI-STANDARD-2024",
      "formulary_status": "Formulary"
    },
    
    "tier": {
      "tier_id": 1,
      "tier_name": "Generic",
      "tier_description": "Generic medications"
    },
    
    "cost_sharing": {
      "copay_retail_30": 10,
      "copay_retail_90": 25,
      "copay_mail_90": 20,
      "coinsurance": null
    },
    
    "clinical_programs": {
      "prior_authorization": false,
      "step_therapy": false,
      "quantity_limit": {
        "applies": true,
        "quantity": 90,
        "per_days": 30,
        "exceeds_limit": false
      }
    },
    
    "restrictions": [],
    "alternatives": []
  }
}
```

### Covered Drug - Prior Authorization Required

```json
{
  "formulary_status": {
    "drug": {
      "ndc": "00074-3799-02",
      "drug_name": "Humira 40mg/0.8ml",
      "brand_generic": "Brand"
    },
    
    "coverage": {
      "covered": true,
      "formulary_status": "Formulary with PA"
    },
    
    "tier": {
      "tier_id": 4,
      "tier_name": "Specialty"
    },
    
    "cost_sharing": {
      "coinsurance": 0.25,
      "coinsurance_min": 100,
      "coinsurance_max": 400
    },
    
    "clinical_programs": {
      "prior_authorization": {
        "required": true,
        "type": "Clinical",
        "criteria": [
          "Diagnosis of rheumatoid arthritis (M05/M06) OR",
          "Diagnosis of psoriatic arthritis (L40.5x) OR",
          "Diagnosis of Crohn's disease (K50.x) OR",
          "Diagnosis of ulcerative colitis (K51.x)"
        ],
        "documentation_required": [
          "Confirmed diagnosis",
          "Prior DMARD trial (if RA/PsA)",
          "Prescriber specialty verification"
        ],
        "approval_duration_days": 365,
        "renewal_criteria": "Continued medical necessity"
      },
      "step_therapy": false,
      "quantity_limit": {
        "applies": true,
        "quantity": 2,
        "per_days": 28,
        "exceeds_limit": false
      }
    },
    
    "biosimilar_alternatives": [
      {"name": "Hadlima", "ndc": "00310-6210-02", "tier": 4},
      {"name": "Hyrimoz", "ndc": "00078-0830-68", "tier": 4}
    ]
  }
}
```

### Covered Drug - Step Therapy Required

```json
{
  "formulary_status": {
    "drug": {
      "ndc": "00173-0714-00",
      "drug_name": "Advair Diskus 250/50",
      "brand_generic": "Brand"
    },
    
    "coverage": {
      "covered": true,
      "formulary_status": "Formulary with ST"
    },
    
    "tier": {
      "tier_id": 3,
      "tier_name": "Non-Preferred Brand"
    },
    
    "clinical_programs": {
      "prior_authorization": false,
      "step_therapy": {
        "required": true,
        "protocol_name": "ICS/LABA Step Therapy",
        "step_1": {
          "drugs": ["Generic ICS (fluticasone, budesonide)"],
          "duration_days": 30,
          "criteria": "Trial and failure or contraindication"
        },
        "step_2": {
          "drugs": ["Wixela Inhub (authorized generic)", "Symbicort"],
          "duration_days": 30,
          "criteria": "Trial and failure of Step 1"
        },
        "target_drug": "Advair Diskus",
        "current_step_status": "Step 1 required",
        "override_criteria": [
          "Previous trial of Step 1 agent (claims history)",
          "Documented allergy to Step 1 agents",
          "Continuation of therapy"
        ]
      },
      "quantity_limit": {
        "applies": true,
        "quantity": 1,
        "per_days": 30
      }
    },
    
    "step_alternatives": [
      {"name": "Wixela Inhub", "tier": 2, "step_required": false},
      {"name": "Symbicort", "tier": 2, "step_required": false}
    ]
  }
}
```

### Non-Formulary Drug

```json
{
  "formulary_status": {
    "drug": {
      "ndc": "00069-0770-30",
      "drug_name": "Celebrex 200mg",
      "brand_generic": "Brand"
    },
    
    "coverage": {
      "covered": false,
      "formulary_status": "Excluded",
      "exclusion_reason": "Preferred alternative available"
    },
    
    "tier": null,
    "cost_sharing": null,
    
    "clinical_programs": {
      "prior_authorization": {
        "available": true,
        "type": "Exception Request",
        "criteria": [
          "Documented trials of 2+ generic NSAIDs",
          "Trials of meloxicam AND naproxen",
          "Medical necessity documentation"
        ],
        "approval_likelihood": "Low without documentation"
      }
    },
    
    "alternatives": [
      {
        "drug_name": "Meloxicam 15mg",
        "ndc": "00591-3458-01",
        "tier": 1,
        "tier_name": "Generic",
        "copay": 10,
        "therapeutic_equivalent": true
      },
      {
        "drug_name": "Naproxen 500mg",
        "ndc": "00603-4956-21",
        "tier": 1,
        "tier_name": "Generic",
        "copay": 10,
        "therapeutic_equivalent": true
      }
    ],
    
    "member_options": [
      "Fill with formulary alternative",
      "Request formulary exception with PA",
      "Pay cash price"
    ]
  }
}
```

### Quantity Limit Exceeded

```json
{
  "formulary_status": {
    "drug": {
      "ndc": "00591-0405-01",
      "drug_name": "Sumatriptan 100mg",
      "brand_generic": "Generic"
    },
    
    "coverage": {
      "covered": true,
      "formulary_status": "Formulary"
    },
    
    "tier": {
      "tier_id": 1,
      "tier_name": "Generic"
    },
    
    "clinical_programs": {
      "prior_authorization": false,
      "step_therapy": false,
      "quantity_limit": {
        "applies": true,
        "limit_type": "Per 30 days",
        "quantity_allowed": 9,
        "quantity_requested": 18,
        "exceeds_limit": true,
        "partial_fill_available": true,
        "partial_quantity": 9
      }
    },
    
    "quantity_limit_details": {
      "basis": "FDA labeling - max 4 doses/day for acute migraine",
      "clinical_rationale": "Medication overuse headache prevention",
      "override_available": true,
      "override_criteria": [
        "Neurologist prescription",
        "Chronic migraine diagnosis",
        "Documentation of appropriate use"
      ]
    },
    
    "adjudication_options": [
      {
        "option": "Partial fill",
        "quantity": 9,
        "processing": "Automatic"
      },
      {
        "option": "Quantity limit override",
        "requires": "Prior Authorization",
        "approval_time": "24-72 hours"
      }
    ]
  }
}
```

---

## Examples

### Example 1: Generic Statin (Covered, Tier 1)

**Drug Context**:
```json
{
  "drug": {"name": "Atorvastatin 20mg", "gpi": "3940002000"}
}
```

**Formulary Status**:
```json
{
  "coverage": {"covered": true, "formulary_status": "Formulary"},
  "tier": {"tier_id": 1, "tier_name": "Generic"},
  "cost_sharing": {"copay_retail_30": 10},
  "clinical_programs": {
    "prior_authorization": false,
    "step_therapy": false,
    "quantity_limit": {"applies": true, "quantity": 90, "per_days": 30}
  }
}
```

### Example 2: Brand SSRI with Step Therapy

**Drug Context**:
```json
{
  "drug": {"name": "Lexapro 10mg", "brand_generic": "Brand"}
}
```

**Formulary Status**:
```json
{
  "coverage": {"covered": true, "formulary_status": "Formulary with ST"},
  "tier": {"tier_id": 3, "tier_name": "Non-Preferred Brand"},
  "clinical_programs": {
    "step_therapy": {
      "required": true,
      "step_1_drugs": ["Generic escitalopram", "Sertraline", "Fluoxetine"],
      "step_duration": "30 days",
      "status": "Step 1 not completed"
    }
  },
  "alternatives": [
    {"name": "Escitalopram 10mg", "tier": 1, "copay": 10}
  ]
}
```

### Example 3: Specialty Biologic with PA

**Drug Context**:
```json
{
  "drug": {"name": "Enbrel 50mg", "specialty_indicator": true}
}
```

**Formulary Status**:
```json
{
  "coverage": {"covered": true, "formulary_status": "Specialty with PA"},
  "tier": {"tier_id": 4, "tier_name": "Specialty"},
  "cost_sharing": {"coinsurance": 0.25, "min": 100, "max": 400},
  "clinical_programs": {
    "prior_authorization": {
      "required": true,
      "criteria": ["RA/PsA/AS diagnosis", "Prior DMARD trial"]
    },
    "specialty_pharmacy": "Required - Accredo"
  },
  "biosimilar_alternatives": [
    {"name": "Erelzi", "tier": 4, "preferred": true}
  ]
}
```

### Example 4: Excluded Drug

**Drug Context**:
```json
{
  "drug": {"name": "Nexium 40mg", "brand_generic": "Brand"}
}
```

**Formulary Status**:
```json
{
  "coverage": {
    "covered": false,
    "formulary_status": "Excluded",
    "exclusion_reason": "Generic and OTC alternatives available"
  },
  "alternatives": [
    {"name": "Omeprazole 40mg", "tier": 1, "otc_available": true},
    {"name": "Esomeprazole 40mg (generic)", "tier": 1}
  ],
  "exception_available": {
    "requires": "PA with documented failures",
    "likelihood": "Low"
  }
}
```

---

## Clinical Program Criteria

### Prior Authorization Criteria by Class

```json
{
  "pa_criteria_by_class": {
    "biologics_ra": {
      "diagnosis_required": ["M05.x", "M06.x"],
      "step_therapy": "DMARD trial required",
      "documentation": ["Rheumatologist prescription", "Disease activity score"],
      "duration": 365
    },
    "specialty_dermatology": {
      "diagnosis_required": ["L40.x (psoriasis)", "L20.x (eczema)"],
      "step_therapy": "Topicals and/or phototherapy",
      "documentation": ["BSA affected", "Prior treatment history"],
      "duration": 365
    },
    "growth_hormone": {
      "diagnosis_required": ["E23.0", "E34.3", "Q96.x"],
      "documentation": ["Endocrinologist prescription", "Growth velocity data", "Bone age"],
      "duration": 180
    },
    "specialty_oncology": {
      "diagnosis_required": ["C00-C97"],
      "documentation": ["Oncologist prescription", "Pathology confirming diagnosis"],
      "duration": 180,
      "expedited_review": true
    }
  }
}
```

### Step Therapy Protocols

```json
{
  "step_therapy_protocols": {
    "antihypertensives": {
      "step_1": ["Lisinopril", "Amlodipine", "HCTZ"],
      "step_2": ["Losartan", "Metoprolol"],
      "step_3": ["Brand ARBs", "Combination products"],
      "duration_per_step": 30
    },
    "antidepressants": {
      "step_1": ["Sertraline", "Fluoxetine", "Escitalopram"],
      "step_2": ["Venlafaxine", "Bupropion", "Duloxetine"],
      "step_3": ["SNRIs", "Brand agents"],
      "duration_per_step": "6-8 weeks"
    },
    "diabetes_glp1": {
      "step_1": ["Metformin"],
      "step_2": ["Sulfonylureas OR Trulicity"],
      "step_3": ["Ozempic", "Victoza", "Mounjaro"],
      "duration_per_step": 90
    }
  }
}
```

---

## Validation Rules

| Rule | Validation |
|------|------------|
| NDC Valid | 11-digit NDC exists |
| Formulary Active | Formulary effective on service date |
| Tier Assignment | Drug assigned to valid tier |
| PA Criteria | PA requirements documented |
| ST Protocol | Step drugs on formulary |
| QL Reasonable | Quantity limit per FDA/clinical guidelines |

---

## Cross-Product Integration

### To RxMemberSim Claims

Formulary context flows to claim adjudication:

```json
{
  "ncpdp_claim": {
    "formulary_tier": "1",
    "copay_amount": 10.00,
    "pa_indicator": "N",
    "reject_codes": [],
    "daw_code": "0"
  }
}
```

### Rejection Response (PA Required)

```json
{
  "ncpdp_reject": {
    "reject_code": "75",
    "reject_message": "Prior Authorization Required",
    "additional_info": {
      "pa_phone": "1-800-555-0123",
      "pa_fax": "1-800-555-0124",
      "pa_criteria_id": "PA-BIO-001"
    }
  }
}
```

---

## Related Skills

- [Synthetic Pharmacy Benefit](../synthetic/synthetic-pharmacy-benefit.md) - Generate benefits
- [Pharmacy Benefit Patterns](../patterns/pharmacy-benefit-patterns.md) - Tier patterns
- [Utilization Management](../reference/utilization-management.md) - UM concepts
- [Pharmacy for Rx](pharmacy-for-rx.md) - Pharmacy routing

---

*Formulary for Rx is an integration skill in the NetworkSim product.*
