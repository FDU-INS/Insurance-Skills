# RxMemberSim Examples

Generate realistic pharmacy data including prescriptions, claims, DUR alerts, and copay assistance.

---

## Example 1: Simple Generic Prescription

### Prompt
```
Generate a pharmacy claim for lisinopril
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM001234",
    "cardholder_id": "001234001",
    "bin": "610014",
    "pcn": "RXGROUP",
    "group_number": "CORP001"
  },
  "prescription": {
    "prescription_number": "RX78901234",
    "ndc": "00093505601",
    "drug_name": "Lisinopril 10mg Tablet",
    "generic_name": "lisinopril",
    "quantity_prescribed": 30,
    "days_supply": 30,
    "refills_authorized": 5,
    "refills_remaining": 5,
    "prescriber_npi": "1234567890",
    "written_date": "2025-01-10",
    "daw_code": "0",
    "directions": "Take 1 tablet by mouth once daily"
  },
  "pharmacy": {
    "npi": "9876543210",
    "ncpdp": "1234567",
    "name": "CVS Pharmacy #1234",
    "address": "100 Main Street, Springfield, IL 62701"
  },
  "claim": {
    "claim_id": "RX20250115000001",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "ndc": "00093505601",
    "quantity_dispensed": 30,
    "days_supply": 30,
    "fill_number": 0,
    "ingredient_cost_submitted": 8.50,
    "dispensing_fee_submitted": 2.00,
    "usual_customary_charge": 15.00,
    "gross_amount_due": 10.50
  },
  "response": {
    "status": "paid",
    "transaction_response_status": "A",
    "message": "Claim Approved",
    "ingredient_cost_paid": 8.50,
    "dispensing_fee_paid": 1.75,
    "plan_paid": 0.25,
    "patient_pay_amount": 10.00,
    "copay_amount": 10.00,
    "tier": 1,
    "tier_description": "Generic",
    "authorization_number": "AUTH20250115001"
  }
}
```

### Key Points
- Tier 1 = Generic (lowest copay)
- NDC is real 11-digit code for lisinopril
- Fill_number 0 = new prescription
- DAW 0 = no product selection indicated (generic OK)

### Variations
```
Generate a refill for lisinopril (fill_number > 0)
Generate a 90-day supply for mail order
Generate a brand drug prescription
```

---

## Example 2: Drug Interaction Alert

### Prompt
```
Generate a pharmacy claim that triggers a drug-drug interaction alert
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM002345",
    "cardholder_id": "002345001"
  },
  "prescription": {
    "ndc": "00093737598",
    "drug_name": "Warfarin 5mg Tablet",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "medication_history": [
    {
      "ndc": "61314060710",
      "drug_name": "Ciprofloxacin 500mg Tablet",
      "last_fill_date": "2025-01-10",
      "days_supply": 10,
      "active": true
    }
  ],
  "claim": {
    "claim_id": "RX20250115000002",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "ndc": "00093737598",
    "quantity_dispensed": 30
  },
  "response": {
    "status": "paid_with_warning",
    "transaction_response_status": "A",
    "dur_response": {
      "alert_count": 1,
      "alerts": [
        {
          "dur_code": "DD",
          "dur_type": "Drug-Drug Interaction",
          "clinical_significance": "1",
          "severity": "Severe",
          "interacting_drug_ndc": "61314060710",
          "interacting_drug_name": "Ciprofloxacin 500mg",
          "clinical_message": "Concurrent use of warfarin and ciprofloxacin may increase anticoagulant effect and risk of bleeding",
          "recommendation": "Monitor INR closely. Consider alternative antibiotic if possible.",
          "professional_service_code": "MA",
          "result_of_service_code": "1A"
        }
      ]
    },
    "patient_pay_amount": 15.00
  }
}
```

### Key Points
- DUR code DD = Drug-Drug interaction
- Clinical significance 1 = Severe
- Warfarin + fluoroquinolone is real interaction
- Claim approved with warning (pharmacist counseling required)

### Variations
```
Generate a therapeutic duplication alert (TD)
Generate an early refill alert (ER)
Generate a high dose alert (HD)
```

---

## Example 3: Prior Authorization Required

### Prompt
```
Generate a rejected pharmacy claim for Ozempic requiring prior auth
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM003456",
    "name": { "given_name": "Sarah", "family_name": "Miller" },
    "plan_code": "COMM-RX"
  },
  "prescription": {
    "ndc": "00169408012",
    "drug_name": "Ozempic 1mg/dose Pen",
    "quantity_prescribed": 1,
    "days_supply": 28,
    "prescriber_npi": "1234567890",
    "diagnosis": "E11.9"
  },
  "claim": {
    "claim_id": "RX20250115000003",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "ndc": "00169408012",
    "quantity_dispensed": 1,
    "days_supply": 28,
    "ingredient_cost_submitted": 935.00
  },
  "response": {
    "status": "rejected",
    "transaction_response_status": "R",
    "reject_code": "75",
    "reject_message": "Prior Authorization Required",
    "additional_message_count": 1,
    "additional_messages": [
      {
        "code": "569",
        "text": "Brand drug requires prior authorization. Contact plan for PA criteria."
      }
    ],
    "pa_criteria_summary": [
      "Diagnosis of Type 2 diabetes (E11.x)",
      "Trial and failure of metformin (unless contraindicated)",
      "HbA1c >= 7.0% documented in last 90 days",
      "Prescribed by endocrinologist or documentation of specialist referral"
    ],
    "pa_contact": {
      "phone": "1-800-555-0123",
      "fax": "1-800-555-0124",
      "web": "www.rxplan.com/pa"
    }
  }
}
```

### Key Points
- Reject code 75 = Prior Authorization Required
- GLP-1 drugs commonly require PA
- PA criteria provided to guide submission
- High-cost brand drug ($935)

### Variations
```
Generate a step therapy rejection
Generate a quantity limit rejection (76)
Generate an age restriction rejection
```

---

## Example 4: Specialty Drug with Copay Assistance

### Prompt
```
Generate a specialty pharmacy claim for Humira with manufacturer copay card
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM004567",
    "name": { "given_name": "Karen", "family_name": "Anderson" },
    "plan_code": "PPO-RX-SPECIALTY",
    "insurance_type": "commercial"
  },
  "prescription": {
    "ndc": "00074433906",
    "drug_name": "Humira 40mg/0.4mL Pen",
    "quantity_prescribed": 2,
    "days_supply": 28,
    "diagnosis": "M05.79",
    "diagnosis_description": "Rheumatoid arthritis"
  },
  "specialty_pharmacy": {
    "npi": "1122334455",
    "name": "OptumRx Specialty",
    "type": "specialty"
  },
  "primary_claim": {
    "claim_id": "RX20250115000004",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "ndc": "00074433906",
    "quantity_dispensed": 2,
    "days_supply": 28,
    "ingredient_cost_submitted": 6800.00
  },
  "primary_response": {
    "status": "paid",
    "ingredient_cost_paid": 6300.00,
    "patient_pay_amount": 500.00,
    "calculation": {
      "cost_sharing_type": "coinsurance",
      "coinsurance_rate": "25%",
      "calculated_coinsurance": 1575.00,
      "specialty_per_fill_max": 500.00,
      "applied_patient_pay": 500.00
    },
    "tier": 5,
    "tier_description": "Specialty"
  },
  "copay_assistance": {
    "program_name": "Humira Complete Savings Card",
    "program_type": "manufacturer_copay_card",
    "eligibility": {
      "commercial_insurance": true,
      "medicare_excluded": true,
      "medicaid_excluded": true
    },
    "card_details": {
      "bin": "004682",
      "pcn": "CN",
      "group": "AHUCMP",
      "member_id": "HC123456789"
    },
    "secondary_claim": {
      "claim_id": "RX20250115000005",
      "amount_submitted": 500.00,
      "status": "paid",
      "program_paid": 495.00,
      "patient_pays": 5.00
    },
    "benefit_tracking": {
      "annual_max_benefit": 16000.00,
      "ytd_benefit_used": 495.00,
      "remaining_benefit": 15505.00
    }
  },
  "summary": {
    "drug_cost": 6800.00,
    "plan_paid": 6300.00,
    "copay_card_paid": 495.00,
    "final_patient_cost": 5.00
  }
}
```

### Key Points
- Tier 5 = Specialty (highest tier)
- 25% coinsurance with $500 max per fill
- Manufacturer copay card covers most of patient cost
- BIN 004682 is real Humira program identifier
- Medicare/Medicaid excluded from copay cards

### Variations
```
Generate a specialty claim without copay assistance
Generate a specialty claim with foundation assistance (Medicare patient)
Generate a biosimilar alternative scenario
```

---

## Example 5: Early Refill Scenario

### Prompt
```
Generate a pharmacy claim rejected for early refill
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM005678",
    "cardholder_id": "005678001"
  },
  "prescription": {
    "ndc": "00071015523",
    "drug_name": "Atorvastatin 20mg Tablet",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "fill_history": {
    "previous_fill": {
      "fill_date": "2024-12-27",
      "quantity": 30,
      "days_supply": 30,
      "next_fill_eligible": "2025-01-20"
    },
    "days_since_last_fill": 19,
    "percent_supply_used": 63,
    "days_early": 4
  },
  "claim": {
    "claim_id": "RX20250115000006",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "ndc": "00071015523",
    "quantity_dispensed": 30,
    "days_supply": 30,
    "fill_number": 3
  },
  "response": {
    "status": "rejected",
    "transaction_response_status": "R",
    "reject_code": "79",
    "reject_message": "Refill Too Soon",
    "dur_response": {
      "alerts": [
        {
          "dur_code": "ER",
          "dur_type": "Early Refill",
          "severity": "reject",
          "clinical_message": "Refill requested 4 days early. 63% of previous supply used.",
          "next_fill_date": "2025-01-20",
          "override_options": [
            "Vacation supply override",
            "Lost/stolen medication override",
            "Therapy change override"
          ]
        }
      ]
    }
  }
}
```

### Key Points
- Reject code 79 = Refill Too Soon
- Plans typically require 75-80% of supply used
- Override codes available for valid reasons
- Fill history shows calculation

### Variations
```
Generate an early refill that's approved with warning (75% used)
Generate a vacation supply override
Generate a lost medication override
```

---

## Example 6: Medicare Part D with Coverage Gap

### Prompt
```
Generate a Medicare Part D pharmacy claim in the coverage gap phase
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM006789",
    "mbi": "1EG4-TE5-MK72",
    "name": { "given_name": "Richard", "family_name": "Thompson" },
    "plan_code": "MAPD-STANDARD",
    "plan_type": "Medicare Part D"
  },
  "part_d_accumulators": {
    "year": 2025,
    "phase": "coverage_gap",
    "annual_deductible": {
      "limit": 545.00,
      "applied": 545.00,
      "met": true
    },
    "initial_coverage_limit": 5030.00,
    "total_drug_cost_ytd": 5250.00,
    "troop": {
      "description": "True Out-of-Pocket",
      "applied": 1450.00,
      "catastrophic_threshold": 8000.00,
      "remaining_to_catastrophic": 6550.00
    }
  },
  "prescription": {
    "ndc": "00310075190",
    "drug_name": "Januvia 100mg Tablet",
    "brand_generic": "brand",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "claim": {
    "claim_id": "RX20250115000007",
    "service_date": "2025-01-15",
    "ingredient_cost": 550.00,
    "dispensing_fee": 2.00,
    "total_drug_cost": 552.00
  },
  "response": {
    "status": "paid",
    "phase": "coverage_gap",
    "cost_sharing": {
      "brand_discount_program": {
        "manufacturer_discount_percent": 70,
        "manufacturer_pays": 385.00
      },
      "plan_pays": 0.00,
      "member_pays": 167.00,
      "member_coinsurance_rate": "25% after manufacturer discount"
    },
    "troop_credit": {
      "member_payment": 167.00,
      "manufacturer_discount_portion": 385.00,
      "total_troop_credit": 552.00,
      "note": "Both member payment and manufacturer discount count toward TrOOP"
    }
  },
  "updated_accumulators": {
    "troop": {
      "previous": 1450.00,
      "added": 552.00,
      "new_total": 2002.00,
      "remaining_to_catastrophic": 5998.00
    }
  }
}
```

### Key Points
- Coverage gap = "donut hole" phase
- Manufacturer pays 70% for brand drugs
- Member pays 25% of negotiated price
- Both member pay and manufacturer discount count toward TrOOP
- Reaching $8,000 TrOOP triggers catastrophic coverage

---

## More Examples

See also:
- [Cross-Domain Examples](cross-domain-examples.md) - Link Rx to patients and medical claims
- [Format Examples](format-examples.md) - Output as NCPDP D.0
