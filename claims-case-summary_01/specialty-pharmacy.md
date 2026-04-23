---
name: specialty-pharmacy
description: "Specialty pharmacy transactions for high-cost biologics, injectables, and limited distribution drugs. Triggers: specialty pharmacy, biologic, injectable, Humira, Enbrel, Remicade, biosimilar, limited distribution, cold chain, hub services, copay assistance"
---

# Specialty Pharmacy Cohort

A cohort template for generating specialty pharmacy transactions for high-cost biologics, injectables, and limited distribution drugs.

## For Claude

Use this skill when the user requests specialty pharmacy or biologic medication cohorts. This teaches you how to generate **realistic specialty drug claims** with prior authorization, copay assistance, and hub services.

**When to apply this skill:**

- User mentions specialty pharmacy or specialty drug
- User requests biologics, biosimilars, or injectable cohorts
- User specifies hub services or limited distribution
- User asks for copay assistance or patient support programs
- User needs high-cost drug billing examples

**Key capabilities this skill provides:**

- How to structure specialty pharmacy claims
- How to model limited distribution drug requirements
- How to integrate copay assistance and patient support
- How to handle prior authorization for specialty drugs
- How to generate specialty tier cost-sharing

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: RxMemberSim
- **Tags**: pharmacy, specialty, biologics, PBM, high-cost
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic specialty pharmacy transactions. It models high-cost medication dispensing including biologics, limited distribution requirements, copay assistance, and hub services.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "specialty pharmacy", "specialty drug"
- "biologics", "biosimilar", "injectable"
- "limited distribution", "specialty tier"
- "high-cost drug", "hub services"

**Specialty Cohorts**:

- "Generate a specialty pharmacy claim"
- "Create a biologic prescription fill"
- "Generate a claim with copay assistance"

## Trigger Phrases

- specialty pharmacy
- specialty drug
- specialty medication
- biologics
- biosimilar
- injectable
- self-administered
- limited distribution
- specialty tier
- high-cost drug
- hub services

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| drug_category | string | biologic | biologic, biosimilar, oral_specialty, injectable |
| therapy_area | string | autoimmune | autoimmune, oncology, ms, hiv, hepatitis, rare_disease |
| distribution | string | specialty_only | specialty_only, limited_distribution, retail_specialty |
| copay_assistance | bool | false | true, false |
| claim_status | string | paid | paid, rejected, pa_required |

## Specialty Drug Characteristics

### What Makes a Drug "Specialty"
- **Cost**: Typically > $1,000/month
- **Administration**: Often injectable or infused
- **Storage**: May require refrigeration or special handling
- **Distribution**: Limited distribution network
- **Monitoring**: Requires clinical monitoring
- **Adherence**: Complex dosing regimens

### Common Therapy Areas
| Area | Example Drugs | Typical Cost/Month |
|------|---------------|-------------------|
| Autoimmune | Humira, Enbrel, Stelara | $5,000 - $15,000 |
| Oncology | Ibrance, Revlimid, Keytruda | $10,000 - $20,000 |
| Multiple Sclerosis | Tecfidera, Ocrevus, Tysabri | $6,000 - $10,000 |
| HIV | Biktarvy, Triumeq, Dovato | $3,000 - $4,000 |
| Hepatitis C | Harvoni, Epclusa, Mavyret | $25,000 - $30,000/course |
| Rare Disease | Spinraza, Zolgensma | $100,000+ |

## Specialty Pharmacy Workflow

```
1. Prescription received (often from specialist)
   ↓
2. Benefits investigation (coverage, PA status)
   ↓
3. Prior authorization (if required)
   ↓
4. Financial assistance screening
   ↓
5. Patient enrollment and consent
   ↓
6. Clinical intake assessment
   ↓
7. Order processing and claim submission
   ↓
8. Medication preparation and shipping
   ↓
9. Delivery (cold chain if needed)
   ↓
10. Follow-up and refill coordination
```

## Limited Distribution Drugs (LDD)

### Distribution Restrictions
```json
{
  "ldd_drug_example": {
    "drug_name": "Revlimid",
    "manufacturer": "Bristol-Myers Squibb",
    "rems_program": "Revlimid REMS",
    "authorized_pharmacies": [
      "CVS Specialty",
      "Walgreens Specialty",
      "Optum Specialty"
    ],
    "patient_requirements": [
      "Enrollment in REMS program",
      "Pregnancy test (if applicable)",
      "Signed patient agreement"
    ]
  }
}
```

### REMS Programs
| Drug | REMS Name | Key Requirements |
|------|-----------|------------------|
| Revlimid | Revlimid REMS | Pregnancy prevention |
| Clozapine | Clozaril REMS | ANC monitoring |
| Isotretinoin | iPLEDGE | Pregnancy prevention |
| Tysabri | TOUCH | JC virus monitoring |

## Specialty Drug Database

### Autoimmune/Inflammatory
```json
{
  "humira": {
    "ndc": "00074433906",
    "drug_name": "Humira 40mg/0.4mL Pen",
    "manufacturer": "AbbVie",
    "gpi": "6627001000",
    "awp": 7500.00,
    "typical_dose": "40mg every 2 weeks",
    "quantity_per_fill": 2,
    "days_supply": 28,
    "storage": "refrigerated",
    "administration": "subcutaneous self-injection"
  },
  "enbrel": {
    "ndc": "58406044504",
    "drug_name": "Enbrel 50mg/mL Syringe",
    "manufacturer": "Amgen",
    "awp": 6800.00,
    "typical_dose": "50mg weekly",
    "quantity_per_fill": 4,
    "days_supply": 28
  },
  "stelara": {
    "ndc": "57894006001",
    "drug_name": "Stelara 45mg/0.5mL",
    "manufacturer": "Janssen",
    "awp": 14000.00,
    "typical_dose": "45mg every 12 weeks (after loading)",
    "quantity_per_fill": 1,
    "days_supply": 84
  }
}
```

### Oncology (Oral)
```json
{
  "ibrance": {
    "ndc": "00069017030",
    "drug_name": "Ibrance 125mg Capsule",
    "manufacturer": "Pfizer",
    "awp": 15000.00,
    "indication": "HR+/HER2- breast cancer",
    "typical_dose": "125mg daily x 21 days, 7 days off",
    "quantity_per_fill": 21,
    "days_supply": 28
  },
  "revlimid": {
    "ndc": "59572041028",
    "drug_name": "Revlimid 25mg Capsule",
    "manufacturer": "Bristol-Myers Squibb",
    "awp": 18000.00,
    "indication": "Multiple myeloma",
    "rems_required": true,
    "limited_distribution": true
  }
}
```

## Pricing and Cost Sharing

### Specialty Tier (Tier 5)
```json
{
  "tier": 5,
  "tier_name": "Specialty",
  "cost_sharing_type": "coinsurance",
  "coinsurance_rate": 0.25,
  "minimum_copay": 100.00,
  "maximum_copay": 500.00,
  "notes": "25% coinsurance with $100 min, $500 max per fill"
}
```

### Specialty Cost Example
```json
{
  "drug": "Humira 40mg",
  "ingredient_cost": 6500.00,
  "cost_sharing_calculation": {
    "coinsurance_rate": 0.25,
    "calculated_coinsurance": 1625.00,
    "maximum_copay": 500.00,
    "patient_responsibility": 500.00,
    "plan_responsibility": 6000.00
  }
}
```

## Copay Assistance Programs

### Manufacturer Copay Cards
```json
{
  "program": {
    "drug_name": "Humira",
    "program_name": "Humira Complete",
    "bin": "004682",
    "pcn": "CN",
    "group": "AHUCMP",
    "eligibility": [
      "Commercial insurance",
      "Not Medicare/Medicaid",
      "U.S. resident"
    ],
    "benefit": {
      "type": "copay_reduction",
      "max_per_fill": "Actual copay up to annual max",
      "annual_maximum": 16000.00,
      "patient_pays": 5.00
    }
  }
}
```

### Coordination of Benefits
```json
{
  "primary_claim": {
    "ingredient_cost": 6500.00,
    "plan_paid": 6000.00,
    "patient_responsibility": 500.00
  },
  "copay_card_claim": {
    "bin": "004682",
    "amount_applied": 495.00
  },
  "final_patient_pay": 5.00
}
```

### Foundation Assistance
```json
{
  "foundation_program": {
    "foundation_name": "Patient Access Network Foundation",
    "disease_fund": "Rheumatoid Arthritis",
    "eligibility": {
      "income_limit": "500% FPL",
      "insurance_required": true
    },
    "grant_amount": "Up to annual out-of-pocket maximum",
    "application_required": true
  }
}
```

## Hub Services

### Patient Support Services
```json
{
  "hub_services": {
    "drug_name": "Stelara",
    "hub_name": "Janssen CarePath",
    "services": [
      {
        "service": "Benefits Investigation",
        "description": "Verify coverage and PA status"
      },
      {
        "service": "Prior Authorization Support",
        "description": "Assist with PA submission"
      },
      {
        "service": "Copay Assistance Enrollment",
        "description": "Enroll in manufacturer copay program"
      },
      {
        "service": "Injection Training",
        "description": "Nurse educator for self-injection"
      },
      {
        "service": "Adherence Support",
        "description": "Refill reminders and check-ins"
      },
      {
        "service": "Side Effect Management",
        "description": "Clinical support for adverse events"
      }
    ],
    "contact": "1-800-JANSSEN"
  }
}
```

## Examples

### Example 1: Specialty Claim with Copay Assistance

```json
{
  "member": {
    "member_id": "MEM001234",
    "name": { "given_name": "Susan", "family_name": "Martinez" },
    "plan_code": "RX-SPECIALTY"
  },
  "specialty_pharmacy": {
    "npi": "1122334455",
    "name": "OptumRx Specialty",
    "type": "specialty"
  },
  "prescription": {
    "prescription_number": "SPX001234",
    "ndc": "00074433906",
    "drug_name": "Humira 40mg/0.4mL Pen",
    "quantity_prescribed": 2,
    "days_supply": 28,
    "prescriber_npi": "5566778899",
    "prescriber_specialty": "Rheumatology",
    "diagnosis": "M05.79"
  },
  "primary_claim": {
    "claim_id": "RX20250115000010",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "ndc": "00074433906",
    "quantity_dispensed": 2,
    "days_supply": 28,
    "ingredient_cost_submitted": 6800.00,
    "dispensing_fee_submitted": 0.00
  },
  "primary_response": {
    "status": "paid",
    "ingredient_cost_paid": 6300.00,
    "patient_pay_amount": 500.00,
    "coinsurance_amount": 500.00,
    "formulary_tier": 5,
    "tier_name": "Specialty"
  },
  "copay_assistance": {
    "program_name": "Humira Complete",
    "copay_card_bin": "004682",
    "secondary_claim_submitted": true,
    "assistance_amount": 495.00,
    "final_patient_pay": 5.00,
    "annual_max_benefit": 16000.00,
    "ytd_benefit_used": 495.00,
    "remaining_benefit": 15505.00
  },
  "summary": {
    "drug_cost": 6800.00,
    "plan_paid": 6300.00,
    "copay_card_paid": 495.00,
    "member_paid": 5.00
  }
}
```

### Example 2: Prior Auth Required for Specialty

```json
{
  "claim": {
    "claim_id": "RX20250115000011",
    "ndc": "57894006001",
    "drug_name": "Stelara 45mg/0.5mL",
    "quantity_dispensed": 1,
    "days_supply": 84,
    "ingredient_cost_submitted": 14200.00
  },
  "response": {
    "status": "rejected",
    "reject_code": "75",
    "reject_message": "Prior Authorization Required",
    "pa_criteria": [
      "Diagnosis of moderate-to-severe plaque psoriasis or psoriatic arthritis",
      "Trial and failure of methotrexate (unless contraindicated)",
      "Trial and failure of one TNF inhibitor",
      "Prescribed by dermatologist or rheumatologist"
    ],
    "pa_phone": "1-800-555-0123",
    "pa_fax": "1-800-555-0124",
    "hub_support": {
      "name": "Janssen CarePath",
      "phone": "1-877-CarePath",
      "services": ["PA submission assistance", "Appeals support"]
    }
  }
}
```

### Example 3: Limited Distribution Drug

```json
{
  "claim": {
    "claim_id": "RX20250115000012",
    "ndc": "59572041028",
    "drug_name": "Revlimid 25mg Capsule",
    "quantity_dispensed": 21,
    "days_supply": 28
  },
  "response": {
    "status": "rejected",
    "reject_code": "76",
    "reject_message": "Limited Distribution - Must use authorized specialty pharmacy",
    "authorized_pharmacies": [
      "CVS Specialty: 1-800-237-2767",
      "Walgreens Specialty: 1-888-347-3416",
      "Accredo: 1-800-803-2523"
    ],
    "rems_requirement": {
      "program_name": "Revlimid REMS",
      "patient_enrollment_required": true,
      "prescriber_certification_required": true,
      "pharmacy_certification_required": true
    }
  }
}
```

### Example 4: Biosimilar Alternative

```json
{
  "original_claim": {
    "ndc": "00074433906",
    "drug_name": "Humira 40mg",
    "ingredient_cost": 6800.00,
    "patient_copay": 500.00
  },
  "biosimilar_alternative": {
    "offered": true,
    "options": [
      {
        "ndc": "55513073001",
        "drug_name": "Hadlima 40mg",
        "manufacturer": "Samsung Bioepis",
        "ingredient_cost": 5100.00,
        "patient_copay": 375.00,
        "savings": 125.00
      },
      {
        "ndc": "00069054801",
        "drug_name": "Amjevita 40mg",
        "manufacturer": "Amgen",
        "ingredient_cost": 5300.00,
        "patient_copay": 400.00,
        "savings": 100.00
      }
    ],
    "message": "Biosimilar alternatives available with lower cost sharing"
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| NDC format | 11-digit numeric | 00074433906 (Humira) |
| Days supply | Typically 28-30 for injectables | 28 days |
| Quantity | Match dosing schedule | 2 pens (biweekly dosing) |
| Prior auth | Required for most specialty drugs | PA approved before fill |
| Specialty pharmacy | Must be accredited/contracted | CVS Specialty, Accredo |
| Cold chain | Temperature-sensitive drugs flagged | Requires refrigeration |
| Limited distribution | Some drugs have exclusive networks | Only 3 pharmacies dispense |
| REMS | Risk Evaluation required for some drugs | Revlimid REMS enrollment |
| Refill timing | Typically 75-80% of days supply | Allow refill at day 21 of 28 |

### Business Rules

- **Prior Authorization**: Most specialty drugs require PA; approval typically valid 6-12 months
- **Step Therapy**: Many require trial/failure of lower-cost alternatives first
- **Quantity Limits**: Often limited to 30-day supply regardless of cost savings
- **Biosimilar Substitution**: Not automatic like generic substitution; requires prescriber approval
- **Copay Assistance**: Most brand specialty drugs have manufacturer copay cards ($0-$5 copay common)
- **Hub Services**: Many drugs require enrollment (refill reminders, adherence support)
- **Accumulator Programs**: Manufacturer assistance may or may not count toward deductible/OOP

## Related Skills

### RxMemberSim
- [SKILL.md](SKILL.md) - RxMemberSim overview
- [retail-pharmacy.md](retail-pharmacy.md) - Standard retail fills
- [rx-prior-auth.md](rx-prior-auth.md) - PA requirements for specialty drugs
- [dur-alerts.md](dur-alerts.md) - Drug interaction checks
- [formulary-management.md](formulary-management.md) - PA and step therapy
- [manufacturer-programs.md](manufacturer-programs.md) - Copay assistance

### Cross-Product: PatientSim
- [../patientsim/oncology/README.md](../patientsim/oncology/README.md) - Oral oncolytics (Ibrance, Tagrisso, Revlimid)
- [../patientsim/chronic-kidney-disease.md](../patientsim/chronic-kidney-disease.md) - ESAs, calcimimetics
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - Entresto (sacubitril/valsartan)

> **Integration Pattern:** Use PatientSim for specialty medication orders and clinical monitoring. Use RxMemberSim specialty-pharmacy for dispensing - includes limited distribution, cold chain requirements, patient counseling, and adherence programs.

### Cross-Product: MemberSim
- [../membersim/prior-authorization.md](../membersim/prior-authorization.md) - Medical benefit drugs (infused biologics)

> **Integration Pattern:** Some specialty drugs are covered under medical benefit (infused) vs. pharmacy benefit (oral/self-injectable). Use MemberSim PA for medical benefit drugs, RxMemberSim for pharmacy benefit drugs.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - NDC, GPI codes
