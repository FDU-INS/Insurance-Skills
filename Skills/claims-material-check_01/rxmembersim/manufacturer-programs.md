---
name: manufacturer-programs
description: "Manufacturer assistance programs including copay cards, patient assistance programs, and hub services. Triggers: copay card, copay assistance, PAP, patient assistance, manufacturer program, hub services, free drug program, accumulator adjustment"
---

# Manufacturer Programs Cohort

A cohort template for generating manufacturer assistance programs including copay cards, patient assistance programs, and hub services.

## For Claude

Use this skill when the user requests manufacturer program or copay assistance cohorts. This teaches you how to generate **realistic patient support programs** with copay cards, PAPs, and accumulator adjustment policies.

**When to apply this skill:**

- User mentions manufacturer program or copay card
- User requests patient assistance program or PAP
- User specifies copay coupon or copay accumulator
- User asks for hub program or bridge program examples
- User needs foundation assistance cohorts

**Key capabilities this skill provides:**

- How to structure copay card programs and limits
- How to model patient assistance eligibility criteria
- How to handle accumulator adjustment programs
- How to integrate hub services with specialty fills
- How to generate manufacturer rebate cohorts

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: RxMemberSim
- **Tags**: pharmacy, manufacturer, copay-card, PAP, hub-services
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic manufacturer assistance programs. It models copay cards, patient assistance programs, foundation grants, and hub services that support patient access to medications.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "manufacturer program", "copay card"
- "patient assistance program", "PAP"
- "copay coupon", "copay accumulator"
- "hub program", "bridge program"

**Program Cohorts**:

- "Generate a copay card enrollment"
- "Create a PAP eligibility check"
- "Generate an accumulator adjustment cohort"

## Trigger Phrases

- manufacturer program
- copay card
- copay assistance
- patient assistance program
- PAP
- free drug program
- manufacturer rebate
- copay coupon
- copay accumulator
- maximizer program
- bridge program
- hub program
- patient support program
- foundation assistance

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| program_type | string | copay_card | copay_card, pap, foundation, bridge, free_goods |
| patient_insurance | string | commercial | commercial, medicare, medicaid, uninsured |
| drug_type | string | brand | brand, specialty, biosimilar |
| accumulator_policy | string | none | none, accumulator_adjustment, maximizer |
| enrollment_status | string | active | pending, active, expired, rejected |

## Overview

Manufacturer programs help patients afford medications through various financial assistance mechanisms. These programs vary based on insurance status and medication type.

### Program Types by Patient Insurance

| Insurance Type | Eligible Programs |
|----------------|-------------------|
| Commercial | Copay cards, Bridge programs |
| Medicare Part D | PAP (usually), Foundation assistance |
| Medicaid | PAP (usually), Foundation (limited) |
| Uninsured | PAP, Free goods, Foundation |

## Copay Card Programs

### How Copay Cards Work

```
1. Patient fills prescription at pharmacy
   ↓
2. Primary insurance processes claim
   ↓
3. Patient responsibility determined (copay/coinsurance)
   ↓
4. Copay card submitted as secondary payer
   ↓
5. Copay card pays portion/all of patient cost
   ↓
6. Patient pays reduced amount (often $0-$5)
```

### Copay Card Structure

```json
{
  "copay_card": {
    "program_id": "CP001234",
    "program_name": "DrugName Savings Card",
    "manufacturer": "Example Pharma",
    "drug_ndc_list": ["12345678901", "12345678902"],
    "bin": "610020",
    "pcn": "SAVINGS",
    "group": "CPCARD01",
    "member_id": "format: auto-generated or pre-assigned",
    "eligibility_criteria": {
      "insurance_required": true,
      "insurance_types_allowed": ["commercial"],
      "insurance_types_excluded": ["medicare", "medicaid", "tricare"],
      "age_minimum": 18,
      "us_resident": true
    },
    "benefit_structure": {
      "benefit_type": "dollar_cap",
      "max_per_fill": 500.00,
      "annual_maximum": 6000.00,
      "patient_pays_minimum": 0.00,
      "effective_date": "2025-01-01",
      "expiration_date": "2025-12-31"
    }
  }
}
```

### Common Copay Card Benefit Types

| Type | Description | Example |
|------|-------------|---------|
| **Fixed Copay** | Patient pays fixed amount | "Pay no more than $10" |
| **Dollar Cap** | Card pays up to max per fill | "Up to $500 per fill" |
| **Percentage** | Card pays percentage of cost | "Covers 80% of copay" |
| **Full Coverage** | Card covers entire copay | "$0 copay for eligible patients" |

### Copay Card BINs and PCNs (Sample)

| Processor | BIN | PCN | Notes |
|-----------|-----|-----|-------|
| ConnectiveRx | 610020 | CNRX | Multi-manufacturer |
| TrialCard | 610524 | TCC | Enrollment-based |
| Inmar | 600426 | 54 | Instant activation |
| McKesson | 016523 | PCN varies | Large portfolio |
| PSKW | 610279 | 01260000 | Multiple programs |

## Patient Assistance Programs (PAP)

### PAP Overview

Patient Assistance Programs provide free medications to qualifying patients who lack adequate insurance coverage.

### PAP Eligibility Criteria

```json
{
  "pap_program": {
    "program_id": "PAP001234",
    "program_name": "DrugName Patient Assistance",
    "manufacturer": "Example Pharma",
    "eligibility": {
      "insurance_status": ["uninsured", "underinsured", "medicare_no_coverage"],
      "income_requirements": {
        "type": "federal_poverty_level",
        "maximum_fpl_percentage": 400,
        "household_size_considered": true
      },
      "residency": "us_resident_or_territory",
      "age_requirement": null,
      "disease_specific": true,
      "diagnosis_codes": ["E11.9", "E11.65"]
    },
    "application_requirements": [
      "Completed application form",
      "Proof of income (tax return, pay stubs)",
      "Proof of residency",
      "Prescription from licensed provider",
      "Insurance denial letter (if applicable)"
    ],
    "benefit": {
      "type": "free_medication",
      "supply_duration": "90 days per shipment",
      "refill_process": "automatic with valid prescription",
      "enrollment_period": "12 months, renewable"
    }
  }
}
```

### 2025 Federal Poverty Level Guidelines

| Household Size | 100% FPL | 200% FPL | 300% FPL | 400% FPL |
|----------------|----------|----------|----------|----------|
| 1 | $15,060 | $30,120 | $45,180 | $60,240 |
| 2 | $20,440 | $40,880 | $61,320 | $81,760 |
| 3 | $25,820 | $51,640 | $77,460 | $103,280 |
| 4 | $31,200 | $62,400 | $93,600 | $124,800 |
| Each Add'l | +$5,380 | +$10,760 | +$16,140 | +$21,520 |

## Foundation Assistance Programs

### Independent Charitable Foundations

Foundations provide financial assistance independently from manufacturers to avoid Anti-Kickback Statute concerns.

```json
{
  "foundation_program": {
    "foundation_name": "Patient Access Network Foundation",
    "tax_id": "XX-XXXXXXX",
    "disease_fund": "Rheumatoid Arthritis",
    "fund_status": "open",
    "eligibility": {
      "insurance_required": true,
      "insurance_types": ["medicare", "commercial_high_cost"],
      "income_limit_fpl": 500,
      "diagnosis_required": true
    },
    "benefit": {
      "assistance_type": "cost_sharing",
      "covers": ["copays", "coinsurance", "deductibles"],
      "annual_maximum": 15000.00,
      "payment_method": "direct_to_pharmacy"
    },
    "application": {
      "method": ["online", "phone", "fax"],
      "processing_time": "3-5 business days",
      "documentation_required": [
        "Insurance card copy",
        "Prescription",
        "Income verification",
        "Diagnosis confirmation"
      ]
    }
  }
}
```

### Major Foundations

| Foundation | Disease Areas | Income Limit |
|------------|---------------|--------------|
| PAN Foundation | Multiple | Up to 500% FPL |
| Patient Advocate Foundation | Multiple | Varies by fund |
| HealthWell Foundation | Multiple | Up to 500% FPL |
| The Assistance Fund | Multiple | Up to 500% FPL |
| Good Days | Multiple | Up to 500% FPL |
| CancerCare | Oncology | Varies |

## Bridge Programs

### Purpose

Bridge programs provide free medication while patients await insurance approval (prior authorization) or assistance program enrollment.

```json
{
  "bridge_program": {
    "program_id": "BR001234",
    "program_name": "QuickStart Bridge",
    "manufacturer": "Example Pharma",
    "purpose": "coverage_during_pa_review",
    "eligibility": {
      "pa_pending": true,
      "commercial_insurance": true,
      "new_start_only": true
    },
    "benefit": {
      "supply_provided": "30 days",
      "maximum_uses": 1,
      "free_of_charge": true
    },
    "requirements": [
      "Prescription on file",
      "PA submitted to payer",
      "Enrollment in hub program"
    ]
  }
}
```

## Hub Services Integration

### Hub Program Structure

Manufacturer hubs coordinate multiple support services for patients on specialty medications.

```json
{
  "hub_program": {
    "program_name": "Complete Care Hub",
    "manufacturer": "Example Pharma",
    "drugs_supported": ["DrugA", "DrugB"],
    "contact": {
      "phone": "1-800-XXX-XXXX",
      "fax": "1-800-XXX-XXXY",
      "website": "www.completecareprogram.com",
      "hours": "M-F 8am-8pm ET"
    },
    "services": {
      "benefits_investigation": {
        "description": "Verify insurance coverage and patient responsibility",
        "turnaround": "24-48 hours"
      },
      "prior_authorization_support": {
        "description": "Assist with PA submission and appeals",
        "includes": ["Clinical information gathering", "Letter of medical necessity"]
      },
      "copay_assistance_enrollment": {
        "description": "Enroll patients in copay card or foundation programs",
        "automatic_screening": true
      },
      "bridge_program": {
        "description": "Free drug during PA review",
        "duration": "Up to 30 days"
      },
      "specialty_pharmacy_coordination": {
        "description": "Route prescription to preferred specialty pharmacy",
        "shipment_tracking": true
      },
      "adherence_support": {
        "description": "Refill reminders and check-in calls",
        "nurse_educator_available": true
      },
      "patient_education": {
        "description": "Injection training, side effect management",
        "formats": ["phone", "video", "in-home nurse"]
      }
    },
    "enrollment": {
      "method": ["fax_enrollment_form", "eRx", "phone"],
      "patient_consent_required": true
    }
  }
}
```

## Copay Accumulators and Maximizers

### Copay Accumulator Adjustment Programs

Some health plans exclude manufacturer copay assistance from counting toward deductible/OOP maximum.

```json
{
  "accumulator_policy": {
    "policy_type": "accumulator_adjustment",
    "description": "Copay card payments do not count toward deductible or OOP max",
    "impact_on_patient": {
      "cohort": "Patient on $6000 brand drug with $500 copay",
      "without_accumulator": {
        "copay_card_pays": 500.00,
        "counts_toward_deductible": 500.00,
        "patient_pays": 0.00
      },
      "with_accumulator": {
        "copay_card_pays": 500.00,
        "counts_toward_deductible": 0.00,
        "patient_pays": 0.00,
        "future_impact": "Must pay full deductible from own pocket"
      }
    }
  }
}
```

### Copay Maximizer Programs

Maximizers coordinate manufacturer assistance to ensure patient costs count toward accumulators.

```json
{
  "maximizer_program": {
    "program_type": "copay_maximizer",
    "description": "Adjusts copay to use manufacturer assistance while crediting patient accumulators",
    "mechanism": {
      "step_1": "Plan sets copay equal to manufacturer max assistance",
      "step_2": "Manufacturer copay card covers full amount",
      "step_3": "Full amount credits to patient deductible/OOP"
    },
    "example": {
      "drug_cost": 6000.00,
      "normal_copay": 500.00,
      "manufacturer_annual_max": 15000.00,
      "maximizer_copay": 1250.00,
      "explanation": "Copay set to $1250/fill (12 fills = $15000 annual max)",
      "patient_pays": 0.00,
      "credits_to_accumulator": 1250.00
    }
  }
}
```

## Claims Processing

### Primary + Copay Card COB

```json
{
  "cob_claim_sequence": {
    "primary_claim": {
      "transaction": "B1",
      "bin": "610014",
      "pcn": "PRIMARY",
      "group": "COMM001",
      "cardholder_id": "MEM001234",
      "ndc": "12345678901",
      "ingredient_cost": 450.00,
      "response": {
        "status": "paid",
        "plan_paid": 350.00,
        "patient_pay": 100.00
      }
    },
    "secondary_claim": {
      "transaction": "B1",
      "other_coverage_code": "8",
      "bin": "610020",
      "pcn": "COPAY",
      "group": "CPCARD01",
      "cardholder_id": "AUTO12345678",
      "ndc": "12345678901",
      "ingredient_cost": 100.00,
      "other_payer_amount_paid": 350.00,
      "response": {
        "status": "paid",
        "plan_paid": 95.00,
        "patient_pay": 5.00
      }
    },
    "final_patient_cost": 5.00
  }
}
```

### Other Coverage Codes (NCPDP)

| Code | Description | Use Case |
|------|-------------|----------|
| 0 | Not specified | Default |
| 1 | No other coverage | No secondary |
| 2 | Other coverage exists, claim not billed | COB not submitted |
| 3 | Other coverage billed, payment collected | After primary payment |
| 8 | Claim billing for copay | Copay card as secondary |

## Sample Drug Programs

### Diabetes Programs

```json
{
  "jardiance_program": {
    "drug": "Jardiance (empagliflozin)",
    "manufacturer": "Boehringer Ingelheim",
    "programs": {
      "copay_card": {
        "name": "Jardiance Savings Card",
        "bin": "004682",
        "pcn": "CN",
        "group": "JARSAVE",
        "benefit": "Pay as little as $10/month",
        "annual_max": 3000.00,
        "eligibility": "Commercial insurance"
      },
      "pap": {
        "name": "Boehringer Ingelheim Cares Foundation",
        "income_limit": "400% FPL",
        "supply": "Free 90-day supply"
      }
    }
  }
}
```

### Autoimmune Programs

```json
{
  "humira_programs": {
    "drug": "Humira (adalimumab)",
    "manufacturer": "AbbVie",
    "programs": {
      "copay_card": {
        "name": "Humira Complete",
        "bin": "004682",
        "pcn": "CN",
        "group": "AHUCMP",
        "benefit": "Pay as little as $5/month",
        "annual_max": 16000.00,
        "eligibility": "Commercial insurance"
      },
      "pap": {
        "name": "AbbVie Patient Assistance Foundation",
        "income_limit": "600% FPL",
        "supply": "Free medication"
      },
      "hub": {
        "name": "Humira Complete",
        "phone": "1-800-4HUMIRA",
        "services": ["Nurse Ambassador", "Sharps disposal", "Injection training"]
      }
    }
  }
}
```

### Oncology Programs

```json
{
  "ibrance_programs": {
    "drug": "Ibrance (palbociclib)",
    "manufacturer": "Pfizer",
    "programs": {
      "copay_card": {
        "name": "Pfizer Oncology Together Co-Pay Savings",
        "benefit": "Pay $0 per prescription",
        "annual_max": 25000.00,
        "eligibility": "Commercial insurance"
      },
      "pap": {
        "name": "Pfizer Patient Assistance Program",
        "income_limit": "400% FPL",
        "supply": "Free medication"
      },
      "hub": {
        "name": "Pfizer Oncology Together",
        "phone": "1-877-744-5675",
        "services": ["Financial assistance navigation", "Treatment support"]
      }
    }
  }
}
```

## Examples

### Example 1: Copay Card Enrollment

```json
{
  "enrollment": {
    "program_name": "DrugX Savings Program",
    "enrollment_date": "2025-01-15",
    "status": "active",
    "member_id": "SAV123456789",
    "card_details": {
      "bin": "610020",
      "pcn": "DRUGXSAVE",
      "group": "DX001",
      "member_id": "SAV123456789"
    },
    "benefit_summary": {
      "max_per_fill": 500.00,
      "annual_maximum": 6000.00,
      "patient_pays": "As low as $0",
      "effective_date": "2025-01-15",
      "expiration_date": "2025-12-31"
    },
    "terms": {
      "insurance_required": true,
      "excluded_insurance": ["Medicare", "Medicaid", "Tricare"],
      "refills_covered": "unlimited within annual max"
    }
  }
}
```

### Example 2: Copay Card Claim with Primary COB

```json
{
  "member": {
    "member_id": "MEM001234",
    "name": { "given_name": "Robert", "family_name": "Chen" },
    "insurance": "Commercial PPO"
  },
  "prescription": {
    "ndc": "50090156001",
    "drug_name": "Jardiance 25mg",
    "quantity": 30,
    "days_supply": 30
  },
  "primary_claim": {
    "claim_id": "RX20250115000020",
    "bin": "610014",
    "pcn": "RXGROUP",
    "ingredient_cost": 580.00,
    "response": {
      "status": "paid",
      "plan_paid": 480.00,
      "patient_pay": 100.00,
      "tier": 3
    }
  },
  "copay_card_claim": {
    "claim_id": "RX20250115000021",
    "bin": "004682",
    "pcn": "CN",
    "group": "JARSAVE",
    "member_id": "JS123456789",
    "amount_submitted": 100.00,
    "response": {
      "status": "paid",
      "program_paid": 90.00,
      "patient_pay": 10.00,
      "ytd_benefit_used": 90.00,
      "remaining_annual_benefit": 2910.00
    }
  },
  "summary": {
    "drug_cost": 580.00,
    "insurance_paid": 480.00,
    "copay_card_paid": 90.00,
    "patient_paid": 10.00
  }
}
```

### Example 3: PAP Application and Approval

```json
{
  "pap_application": {
    "application_id": "PAP20250115001",
    "program_name": "AbbVie Patient Assistance Foundation",
    "drug_requested": "Humira",
    "patient": {
      "name": "Maria Santos",
      "dob": "1965-03-22",
      "insurance_status": "Medicare Part D with coverage gap"
    },
    "income_verification": {
      "household_size": 2,
      "annual_income": 38000.00,
      "fpl_percentage": 186,
      "income_limit": "600% FPL",
      "meets_criteria": true
    },
    "documents_received": [
      { "type": "application_form", "status": "complete" },
      { "type": "prescription", "status": "complete" },
      { "type": "tax_return", "status": "complete" },
      { "type": "insurance_card", "status": "complete" }
    ],
    "status": "approved",
    "approval_details": {
      "approval_date": "2025-01-18",
      "coverage_start": "2025-01-20",
      "coverage_end": "2026-01-19",
      "renewal_required": true,
      "renewal_date": "2025-12-01"
    },
    "benefit": {
      "medication_provided": "Humira 40mg pen",
      "supply": "90-day supply per shipment",
      "cost_to_patient": 0.00,
      "delivery_method": "Direct to patient home"
    }
  }
}
```

### Example 4: Foundation Grant

```json
{
  "foundation_grant": {
    "foundation": "Patient Access Network Foundation",
    "fund": "Rheumatoid Arthritis Fund",
    "application_id": "PAN20250115001",
    "patient": {
      "name": "William Thompson",
      "insurance": "Medicare Part D",
      "diagnosis": "M05.79 - Rheumatoid arthritis"
    },
    "financial_screening": {
      "household_size": 1,
      "annual_income": 52000.00,
      "fpl_percentage": 345,
      "income_limit": "500% FPL",
      "eligible": true
    },
    "grant_details": {
      "status": "approved",
      "approval_date": "2025-01-16",
      "grant_amount": 12000.00,
      "coverage_type": "cost_sharing",
      "covers": ["copays", "coinsurance"],
      "effective_date": "2025-01-16",
      "expiration_date": "2025-12-31"
    },
    "payment_method": {
      "type": "direct_to_pharmacy",
      "pharmacy_name": "CVS Specialty",
      "coordinator_phone": "1-866-316-PANF"
    }
  }
}
```

### Example 5: Bridge Program Supply

```json
{
  "bridge_supply": {
    "program_name": "Stelara QuickStart",
    "request_id": "BR20250115001",
    "status": "approved",
    "patient": {
      "name": "Jennifer Walsh",
      "insurance": "Commercial PPO"
    },
    "clinical_info": {
      "diagnosis": "L40.0 - Psoriasis vulgaris",
      "drug_requested": "Stelara 45mg",
      "prescriber_npi": "1234567890"
    },
    "pa_status": {
      "submitted_date": "2025-01-10",
      "payer": "Aetna",
      "status": "under_review",
      "expected_decision": "2025-01-25"
    },
    "bridge_approval": {
      "approved_date": "2025-01-15",
      "supply_provided": "1 syringe (45mg)",
      "days_supply": 84,
      "cost_to_patient": 0.00,
      "delivery": {
        "method": "Overnight",
        "pharmacy": "Janssen CarePath Pharmacy",
        "tracking": "1Z999AA10123456784"
      }
    }
  }
}
```

### Example 6: Accumulator Impact Cohort

```json
{
  "accumulator_cohort": {
    "patient": {
      "name": "David Park",
      "plan_type": "HDHP with accumulator policy"
    },
    "plan_details": {
      "deductible": 3000.00,
      "oop_max": 6000.00,
      "accumulator_policy": "active",
      "policy_description": "Manufacturer assistance does not apply to deductible or OOP"
    },
    "medication": {
      "drug": "Ozempic 1mg",
      "monthly_cost": 950.00,
      "copay_card_available": true,
      "copay_card_annual_max": 6000.00
    },
    "monthly_breakdown": {
      "january": {
        "drug_cost": 950.00,
        "applied_to_deductible": 0.00,
        "copay_card_pays": 950.00,
        "patient_pays": 0.00,
        "deductible_remaining": 3000.00,
        "notes": "Copay card covers full cost, nothing applies to deductible"
      },
      "july": {
        "copay_card_ytd": 5700.00,
        "copay_card_remaining": 300.00,
        "drug_cost": 950.00,
        "copay_card_pays": 300.00,
        "deductible_remaining": 3000.00,
        "patient_pays": 650.00,
        "notes": "Copay card exhausted, patient must now pay toward deductible"
      },
      "august_forward": {
        "patient_responsibility": "Full cost until deductible met",
        "monthly_patient_cost": 950.00,
        "notes": "Patient faces $3000 deductible + remaining months of drug cost"
      }
    },
    "annual_impact": {
      "with_accumulator": {
        "copay_card_paid": 6000.00,
        "patient_paid": 5400.00,
        "total_patient_cost": 5400.00
      },
      "without_accumulator": {
        "copay_card_paid": 6000.00,
        "patient_paid": 0.00,
        "deductible_credited": 3000.00,
        "total_patient_cost": 0.00
      }
    }
  }
}
```

## Compliance Considerations

### Anti-Kickback Statute (AKS) Safe Harbors

| Program Type | AKS Consideration |
|--------------|-------------------|
| Copay cards (commercial) | Generally permitted |
| Copay cards (Medicare/Medicaid) | Prohibited (with limited exceptions) |
| PAPs | Must be independent from manufacturer |
| Foundation assistance | Must be bona fide charity |

### Best Practices

1. **Copay Cards**: Only for commercially insured; exclude government programs
2. **PAPs**: Income verification required; no patient solicitation
3. **Foundations**: Independent governance; disease-based (not drug-specific)
4. **Documentation**: Maintain records of eligibility verification

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Program ID | Unique identifier | HUMIRA-COMPLETE-2025 |
| Program BIN | 6-digit copay card processor | 004682 |
| Program PCN | Processor control number | CN |
| Program Group | Group identifier | HUMIRACPC |
| Max benefit | Annual max in dollars | $16000/year |
| Per-fill max | Max per transaction | $500/fill |
| Remaining benefit | Non-negative, ≤ max | $14500 remaining |
| Eligibility | Commercial only (typically) | No Medicare Part D |
| Effective dates | Valid date range | 2025-01-01 to 2025-12-31 |

### Business Rules

- **Copay Card Eligibility**: Commercial insurance only; Medicare/Medicaid excluded
- **Per-Fill Maximum**: Caps assistance per transaction (e.g., $500/fill)
- **Annual Maximum**: Total yearly benefit cap (e.g., $16,000/year)
- **Stacking Rules**: May combine with insurance; applied as secondary payer
- **Accumulator Adjustment**: Plan may/may not count manufacturer assistance toward deductible
- **Hub Enrollment**: Required for many specialty drugs (refill reminders, adherence)
- **PAP Income Limits**: Patient Assistance Programs have income eligibility (e.g., <400% FPL)
- **Foundation Independence**: Charitable foundations must be drug-agnostic

## Related Skills

### RxMemberSim
- [SKILL.md](SKILL.md) - RxMemberSim overview
- [specialty-pharmacy.md](specialty-pharmacy.md) - Specialty drug distribution and copay assistance
- [formulary-management.md](formulary-management.md) - Tier structure affecting cost sharing
- [rx-accumulator.md](rx-accumulator.md) - Deductible and OOP tracking

### Cross-Product: PatientSim
- [../patientsim/oncology/README.md](../patientsim/oncology/README.md) - Oncology copay assistance (high utilization)
- [../patientsim/chronic-kidney-disease.md](../patientsim/chronic-kidney-disease.md) - ESA manufacturer programs

> **Integration Pattern:** Use PatientSim to establish clinical need for high-cost specialty drugs. Use manufacturer-programs to model copay assistance enrollment, benefit application, and accumulator adjustment. Common for oral oncolytics, biologics, and specialty drugs.

### Cross-Product: MemberSim
- [../membersim/accumulator-tracking.md](../membersim/accumulator-tracking.md) - Accumulator adjustment programs

> **Integration Pattern:** Some manufacturers fund "accumulator adjustment" programs to help patients reach deductible/OOP faster. Coordinate with MemberSim accumulators for accurate cost tracking.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - NCPDP codes
- [../../formats/ncpdp-d0.md](../../formats/ncpdp-d0.md) - Claims format with COB
