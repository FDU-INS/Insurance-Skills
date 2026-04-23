# MemberSim Examples

Generate realistic claims and payer data including professional claims, facility claims, and adjudication.

---

## Example 1: Simple Office Visit Claim

### Prompt
```
Generate a paid professional claim for an office visit
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM001234",
    "name": { "given_name": "Jennifer", "family_name": "Davis" },
    "birth_date": "1980-03-22",
    "gender": "F",
    "plan_code": "PPO-STANDARD",
    "group_id": "GRP00100"
  },
  "claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "provider_npi": "1234567890",
    "provider_name": "Springfield Medical Associates",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "I10",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "procedure_description": "Office visit, established patient, moderate complexity",
        "charge_amount": 175.00,
        "units": 1,
        "diagnosis_pointers": [1]
      }
    ],
    "total_charges": 175.00
  },
  "adjudication": {
    "status": "paid",
    "adjudication_date": "2025-01-18",
    "allowed_amount": 128.50,
    "deductible": 0.00,
    "copay": 30.00,
    "coinsurance": 0.00,
    "paid_amount": 98.50,
    "patient_responsibility": 30.00,
    "adjustment_codes": [
      {
        "group": "CO",
        "code": "45",
        "amount": 46.50,
        "description": "Charge exceeds fee schedule/maximum allowable"
      }
    ]
  }
}
```

### Key Points
- CPT 99214 is moderate complexity E&M
- CO-45 adjustment is standard (charge > allowed)
- Allowed = negotiated rate
- Paid = Allowed - Patient responsibility

### Variations
```
Generate a claim for a new patient office visit (99205)
Generate an out-of-network claim
Generate a claim with modifier 25
```

---

## Example 2: Denied Claim

### Prompt
```
Generate a denied professional claim for MRI requiring prior authorization
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM002345",
    "name": { "given_name": "Michael", "family_name": "Chen" },
    "plan_code": "HMO-PLUS"
  },
  "claim": {
    "claim_id": "CLM20250115000002",
    "claim_type": "PROFESSIONAL",
    "service_date": "2025-01-15",
    "place_of_service": "22",
    "principal_diagnosis": "M54.5",
    "diagnosis_description": "Low back pain",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "72148",
        "procedure_description": "MRI lumbar spine without contrast",
        "charge_amount": 1500.00,
        "units": 1
      }
    ],
    "total_charges": 1500.00,
    "prior_auth_number": null
  },
  "adjudication": {
    "status": "denied",
    "adjudication_date": "2025-01-17",
    "denial_reason": {
      "code": "CO-15",
      "description": "Authorization required",
      "message": "Prior authorization is required for this service. Please submit authorization request."
    },
    "allowed_amount": 0.00,
    "paid_amount": 0.00,
    "patient_responsibility": 0.00,
    "appeal_info": {
      "can_appeal": true,
      "appeal_deadline": "2025-07-17",
      "instructions": "Submit prior authorization or appeal with medical records demonstrating necessity"
    }
  }
}
```

### Key Points
- CO-15 = Authorization required
- Patient responsibility is $0 (not billed to member)
- Appeal information provided
- HMO plans commonly require PA for imaging

### Variations
```
Generate a denied claim for duplicate submission (CO-18)
Generate a denied claim for timely filing (CO-29)
Generate a denied claim for bundling (CO-97)
```

---

## Example 3: Claim with Deductible

### Prompt
```
Generate a claim where deductible applies, member has $500 deductible with $200 already met
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM003456",
    "name": { "given_name": "David", "family_name": "Wilson" },
    "plan_code": "HDHP-BRONZE"
  },
  "accumulator_before": {
    "individual_deductible": {
      "applied": 200.00,
      "limit": 500.00,
      "remaining": 300.00
    },
    "individual_oop": {
      "applied": 200.00,
      "limit": 3000.00,
      "remaining": 2800.00
    }
  },
  "claim": {
    "claim_id": "CLM20250115000003",
    "claim_type": "PROFESSIONAL",
    "service_date": "2025-01-15",
    "principal_diagnosis": "J06.9",
    "diagnosis_description": "Acute upper respiratory infection",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99213",
        "charge_amount": 125.00,
        "units": 1
      }
    ],
    "total_charges": 125.00
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 95.00,
    "deductible_applied": 95.00,
    "copay": 0.00,
    "coinsurance": 0.00,
    "paid_amount": 0.00,
    "patient_responsibility": 95.00,
    "notes": "Entire allowed amount applied to deductible"
  },
  "accumulator_after": {
    "individual_deductible": {
      "applied": 295.00,
      "limit": 500.00,
      "remaining": 205.00
    },
    "individual_oop": {
      "applied": 295.00,
      "limit": 3000.00,
      "remaining": 2705.00
    }
  }
}
```

### Key Points
- Deductible applies before coinsurance
- Plan paid $0 (all went to deductible)
- Accumulators updated correctly
- OOP also increments with deductible

### Variations
```
Generate a claim where deductible is already met
Generate a claim that satisfies remaining deductible and has coinsurance
Generate a family deductible scenario
```

---

## Example 4: Facility/Inpatient Claim

### Prompt
```
Generate an inpatient facility claim for heart failure admission with DRG
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM004567",
    "name": { "given_name": "Patricia", "family_name": "Brown" },
    "plan_code": "PPO-GOLD"
  },
  "claim": {
    "claim_id": "CLM20250115000004",
    "claim_type": "INSTITUTIONAL",
    "bill_type": "111",
    "member_id": "MEM004567",
    "facility_npi": "1122334455",
    "facility_name": "Springfield General Hospital",
    "admit_date": "2025-01-10",
    "discharge_date": "2025-01-14",
    "length_of_stay": 4,
    "discharge_status": "01",
    "admission_type": "1",
    "admission_source": "7",
    "principal_diagnosis": "I50.23",
    "principal_diagnosis_description": "Acute on chronic systolic heart failure",
    "secondary_diagnoses": [
      { "code": "I48.91", "description": "Atrial fibrillation" },
      { "code": "N18.3", "description": "CKD stage 3" },
      { "code": "E11.9", "description": "Type 2 diabetes" }
    ],
    "principal_procedure": {
      "code": "5A1955Z",
      "description": "Respiratory ventilation, greater than 24 hours"
    },
    "drg": {
      "code": "291",
      "description": "Heart Failure and Shock with MCC",
      "weight": 1.4286,
      "gmlos": 4.2,
      "amlos": 5.1
    },
    "revenue_lines": [
      {
        "line": 1,
        "revenue_code": "0120",
        "description": "Room & Board - Semi-Private",
        "units": 4,
        "charge_amount": 4800.00
      },
      {
        "line": 2,
        "revenue_code": "0250",
        "description": "Pharmacy",
        "charge_amount": 2150.00
      },
      {
        "line": 3,
        "revenue_code": "0300",
        "description": "Laboratory",
        "charge_amount": 1875.00
      },
      {
        "line": 4,
        "revenue_code": "0320",
        "description": "Radiology - Diagnostic",
        "charge_amount": 650.00
      },
      {
        "line": 5,
        "revenue_code": "0410",
        "description": "Respiratory Services",
        "charge_amount": 1200.00
      }
    ],
    "total_charges": 10675.00
  },
  "adjudication": {
    "status": "paid",
    "payment_method": "DRG",
    "drg_base_rate": 6500.00,
    "drg_payment": 9285.90,
    "calculation": "Base Rate ($6,500) x DRG Weight (1.4286) = $9,285.90",
    "deductible": 500.00,
    "coinsurance": 1757.18,
    "paid_amount": 7028.72,
    "patient_responsibility": 2257.18,
    "adjustment_codes": [
      {
        "group": "CO",
        "code": "45",
        "amount": 1389.10,
        "description": "Charges exceed DRG payment"
      }
    ]
  }
}
```

### Key Points
- Bill type 111 = Hospital Inpatient
- DRG 291 = HF with Major Complications
- DRG payment = Base Rate × Weight
- Revenue codes detail facility charges
- Coinsurance after deductible for inpatient

### Variations
```
Generate a surgical inpatient claim
Generate a claim with outlier payment (very long stay)
Generate a Medicare inpatient claim
```

---

## Example 5: Emergency Room Claim

### Prompt
```
Generate an ER claim for chest pain evaluation
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM005678",
    "name": { "given_name": "Robert", "family_name": "Taylor" },
    "birth_date": "1970-11-05",
    "plan_code": "PPO-STANDARD"
  },
  "claim": {
    "claim_id": "CLM20250115000005",
    "claim_type": "INSTITUTIONAL",
    "bill_type": "131",
    "facility_npi": "1122334455",
    "service_date": "2025-01-15",
    "principal_diagnosis": "R07.9",
    "principal_diagnosis_description": "Chest pain, unspecified",
    "secondary_diagnoses": [
      { "code": "I10", "description": "Essential hypertension" }
    ],
    "revenue_lines": [
      {
        "revenue_code": "0450",
        "description": "Emergency Room",
        "hcpcs": "99284",
        "charge_amount": 850.00
      },
      {
        "revenue_code": "0730",
        "description": "EKG/ECG",
        "hcpcs": "93000",
        "charge_amount": 125.00
      },
      {
        "revenue_code": "0300",
        "description": "Laboratory",
        "charge_amount": 450.00
      },
      {
        "revenue_code": "0320",
        "description": "Radiology",
        "hcpcs": "71046",
        "charge_amount": 275.00
      }
    ],
    "total_charges": 1700.00
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 1150.00,
    "er_copay": 150.00,
    "deductible": 0.00,
    "coinsurance": 200.00,
    "paid_amount": 800.00,
    "patient_responsibility": 350.00
  }
}
```

### Key Points
- Bill type 131 = Hospital Outpatient (ER)
- Revenue code 0450 = Emergency Room
- Higher ER copay typical for PPO plans
- Chest pain workup includes EKG, labs, CXR

---

## More Examples

See also:
- [Cross-Domain Examples](cross-domain-examples.md) - Link claims to patients
- [Format Examples](format-examples.md) - Output as X12 837
