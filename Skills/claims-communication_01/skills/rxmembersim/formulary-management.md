---
name: formulary-management
description: "Formulary structures including tier configurations, step therapy, quantity limits, and coverage policies. Triggers: formulary, drug tier, step therapy, prior authorization required, quantity limit, non-formulary, preferred drug, coverage policy"
---

# Formulary Management Cohort

A cohort template for generating formulary structures including tier configurations, step therapy, and coverage policies.

## For Claude

Use this skill when the user requests formulary or drug coverage cohorts. This teaches you how to generate **realistic formulary configurations** with tier structures, utilization management, and alternatives.

**When to apply this skill:**

- User mentions formulary or drug coverage
- User requests tier structure or preferred drug cohorts
- User specifies step therapy or prior authorization
- User asks for quantity limit examples
- User needs formulary exception cohorts

**Key capabilities this skill provides:**

- How to structure multi-tier formularies
- How to model step therapy requirements
- How to configure quantity limits by drug
- How to handle prior authorization criteria
- How to generate formulary alternative suggestions

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: RxMemberSim
- **Tags**: pharmacy, formulary, coverage, step-therapy, PBM
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic formulary management configurations. It models complete formulary structures with tiering, utilization management, and coverage policies for various plan types.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "formulary", "drug coverage", "tier"
- "preferred drug", "non-preferred"
- "step therapy", "prior authorization"
- "quantity limit", "formulary exception"

**Formulary Cohorts**:

- "Generate a 4-tier formulary structure"
- "Create step therapy requirements"
- "Generate a non-formulary rejection"

## Trigger Phrases

- formulary
- drug coverage
- tier
- preferred drug
- non-preferred
- covered medications
- step therapy
- prior authorization
- quantity limit
- formulary exception
- formulary alternative

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| plan_type | string | commercial | commercial, medicare_part_d, medicaid, exchange |
| tier_structure | string | 4tier | 3tier, 4tier, 5tier, 6tier |
| coverage_status | string | covered | covered, not_covered, covered_with_pa |
| step_therapy | bool | false | true, false |
| quantity_limits | bool | false | true, false |

## Formulary Structure

### Tier Definitions

#### Commercial 5-Tier
| Tier | Name | Cost Sharing | Drug Type |
|------|------|--------------|-----------|
| 1 | Preferred Generic | $10 copay | Generic, low cost |
| 2 | Non-Preferred Generic | $25 copay | Generic, higher cost |
| 3 | Preferred Brand | $50 copay | Brand, preferred |
| 4 | Non-Preferred Brand | $80 copay | Brand, non-preferred |
| 5 | Specialty | 25% coinsurance ($100-$500 max) | Specialty drugs |

#### Medicare Part D
| Tier | Name | Cost Sharing (Standard) |
|------|------|------------------------|
| 1 | Preferred Generic | $0-$5 |
| 2 | Generic | $5-$15 |
| 3 | Preferred Brand | $42-$50 |
| 4 | Non-Preferred | 40% coinsurance |
| 5 | Specialty | 25% coinsurance |

### Medicare Part D Phases
```json
{
  "phases": [
    {
      "phase": "Deductible",
      "limit_2025": 590.00,
      "member_pays": "100%"
    },
    {
      "phase": "Initial Coverage",
      "limit_2025": 5030.00,
      "member_pays": "Copay/coinsurance per tier"
    },
    {
      "phase": "Coverage Gap (Donut Hole)",
      "limit_2025": 8000.00,
      "member_pays": "25% for brand and generic"
    },
    {
      "phase": "Catastrophic",
      "threshold": "TrOOP > $8000",
      "member_pays": "$0 (IRA 2025 cap)"
    }
  ]
}
```

## Formulary Drug Entry

### Drug Record Structure
```json
{
  "ndc": "11-digit NDC",
  "gpi": "14-digit GPI",
  "drug_name": "string",
  "generic_name": "string",
  "brand_name": "string or null",
  "manufacturer": "string",
  "strength": "string",
  "dosage_form": "string",
  "route": "string",

  "formulary_status": {
    "covered": true,
    "tier": 1,
    "tier_name": "Preferred Generic",
    "effective_date": "2025-01-01",
    "termination_date": null
  },

  "utilization_management": {
    "prior_auth_required": false,
    "step_therapy_required": false,
    "step_therapy_group": null,
    "quantity_limit": 30,
    "quantity_limit_days": 30,
    "max_days_supply": 90,
    "age_limit_min": null,
    "age_limit_max": null,
    "gender_limit": null
  },

  "clinical_info": {
    "therapeutic_class": "string",
    "ahfs_class": "string",
    "controlled_substance_schedule": null
  }
}
```

## Prior Authorization Rules

### PA-Required Categories
```json
{
  "pa_categories": [
    {
      "category": "Specialty Biologics",
      "gpi_prefix": "66",
      "pa_required": true,
      "criteria": [
        "Diagnosis documentation",
        "Trial of conventional therapy",
        "Prescribed by specialist"
      ]
    },
    {
      "category": "GLP-1 Agonists",
      "drugs": ["Ozempic", "Wegovy", "Mounjaro"],
      "pa_required": true,
      "criteria": [
        "Diagnosis of Type 2 diabetes OR BMI ≥ 30",
        "Trial of metformin (diabetes indication)",
        "Documentation of lifestyle modifications (weight loss indication)"
      ]
    },
    {
      "category": "Specialty Oncology",
      "gpi_prefix": "2199",
      "pa_required": true,
      "criteria": [
        "Oncologist prescription",
        "Diagnosis and staging documentation",
        "Prior therapy history"
      ]
    }
  ]
}
```

### PA Decision Criteria
```json
{
  "pa_criteria_example": {
    "drug": "Humira",
    "indications": [
      {
        "diagnosis": "Rheumatoid Arthritis",
        "icd10_codes": ["M05.xx", "M06.xx"],
        "criteria": [
          "Trial and failure of methotrexate for 12 weeks (unless contraindicated)",
          "Prescribed by rheumatologist"
        ],
        "approval_duration": "12 months"
      },
      {
        "diagnosis": "Psoriasis",
        "icd10_codes": ["L40.0", "L40.1"],
        "criteria": [
          "Moderate-to-severe plaque psoriasis (BSA > 10% or PASI > 10)",
          "Trial of phototherapy or topical therapy",
          "Prescribed by dermatologist"
        ],
        "approval_duration": "12 months"
      }
    ]
  }
}
```

## Step Therapy Rules

### Step Therapy Groups
```json
{
  "step_therapy": [
    {
      "group_name": "Proton Pump Inhibitors",
      "step_1_drugs": ["Omeprazole", "Pantoprazole", "Lansoprazole"],
      "step_2_drugs": ["Esomeprazole (Nexium)", "Dexlansoprazole (Dexilant)"],
      "step_1_requirement": "30-day trial of Step 1 drug",
      "documentation": "Claim history reviewed automatically"
    },
    {
      "group_name": "ADHD Medications",
      "step_1_drugs": ["Methylphenidate IR", "Amphetamine salts IR"],
      "step_2_drugs": ["Concerta", "Vyvanse", "Adderall XR"],
      "step_1_requirement": "Trial of immediate-release formulation",
      "documentation": "Prior claims or prescriber attestation"
    },
    {
      "group_name": "Non-Sedating Antihistamines",
      "step_1_drugs": ["Loratadine", "Cetirizine", "Fexofenadine (generic)"],
      "step_2_drugs": ["Xyzal", "Clarinex"],
      "step_1_requirement": "Trial of OTC antihistamine"
    },
    {
      "group_name": "Diabetes - GLP-1 Agonists",
      "step_1_drugs": ["Metformin"],
      "step_2_drugs": ["Trulicity", "Ozempic", "Victoza"],
      "step_1_requirement": "90-day trial of metformin (unless contraindicated)",
      "step_1_bypass": "eGFR < 30, lactic acidosis history, allergy"
    }
  ]
}
```

## Quantity Limits

### Common Quantity Limits
```json
{
  "quantity_limits": [
    {
      "category": "Triptan Migraine Medications",
      "drugs": ["Sumatriptan", "Rizatriptan", "Eletriptan"],
      "quantity_limit": 9,
      "per_days": 30,
      "rationale": "FDA max dosing frequency"
    },
    {
      "category": "Controlled Substances - Schedule II",
      "limit_type": "days_supply",
      "max_days_supply": 30,
      "early_refill_threshold": 0.90,
      "rationale": "DEA regulations, abuse prevention"
    },
    {
      "category": "Erectile Dysfunction",
      "drugs": ["Sildenafil", "Tadalafil"],
      "quantity_limit": 6,
      "per_days": 30,
      "coverage_note": "Covered for erectile dysfunction only"
    },
    {
      "category": "Specialty Injectables",
      "drugs": ["Humira", "Enbrel"],
      "quantity_limit": 2,
      "per_days": 28,
      "rationale": "One injection every 2 weeks"
    }
  ]
}
```

## Formulary Alternatives

### Alternative Drug Recommendations
```json
{
  "alternatives": {
    "non_formulary_drug": {
      "ndc": "12345678901",
      "drug_name": "Nexium 40mg",
      "status": "non-formulary",
      "reject_code": "70"
    },
    "formulary_alternatives": [
      {
        "ndc": "00093514210",
        "drug_name": "Omeprazole 40mg",
        "tier": 1,
        "copay": 10.00,
        "savings": 140.00,
        "therapeutic_equivalent": true
      },
      {
        "ndc": "00093543701",
        "drug_name": "Pantoprazole 40mg",
        "tier": 1,
        "copay": 10.00,
        "savings": 140.00,
        "therapeutic_equivalent": true
      },
      {
        "ndc": "00378543577",
        "drug_name": "Esomeprazole 40mg",
        "tier": 2,
        "copay": 25.00,
        "savings": 125.00,
        "note": "Same active ingredient as Nexium"
      }
    ]
  }
}
```

## Formulary Exception Process

### Exception Request
```json
{
  "exception_request": {
    "request_id": "EXC20250115000001",
    "member_id": "MEM001234",
    "drug_requested": {
      "ndc": "12345678901",
      "drug_name": "Brand Drug X",
      "current_status": "non-formulary"
    },
    "exception_type": "formulary",
    "reason": "Therapeutic failure on formulary alternatives",
    "supporting_documentation": [
      "Trial of Drug A: 30 days, discontinued due to GI side effects",
      "Trial of Drug B: 45 days, inadequate response",
      "Trial of Drug C: Contraindicated due to allergy"
    ],
    "prescriber_attestation": true,
    "request_date": "2025-01-15"
  },
  "exception_decision": {
    "decision": "approved",
    "decision_date": "2025-01-18",
    "approved_tier": 3,
    "effective_date": "2025-01-18",
    "expiration_date": "2026-01-17",
    "conditions": "Annual renewal required with documentation of continued need"
  }
}
```

## Examples

### Example 1: Formulary Lookup - Covered

```json
{
  "request": {
    "ndc": "00071015523",
    "member_id": "MEM001234",
    "plan_code": "RX-STANDARD"
  },
  "formulary_response": {
    "ndc": "00071015523",
    "drug_name": "Atorvastatin 20mg Tablet",
    "generic_name": "Atorvastatin Calcium",
    "manufacturer": "Pfizer",
    "formulary_status": {
      "covered": true,
      "tier": 1,
      "tier_name": "Preferred Generic",
      "copay_30_day": 10.00,
      "copay_90_day_mail": 25.00
    },
    "utilization_management": {
      "prior_auth_required": false,
      "step_therapy_required": false,
      "quantity_limit": 30,
      "quantity_limit_days": 30,
      "max_days_supply": 90
    },
    "clinical_info": {
      "therapeutic_class": "HMG-CoA Reductase Inhibitors",
      "common_uses": ["High cholesterol", "Cardiovascular prevention"]
    }
  }
}
```

### Example 2: Step Therapy Required

```json
{
  "claim": {
    "claim_id": "RX20250115000001",
    "ndc": "00002140780",
    "drug_name": "Trulicity 1.5mg/0.5mL",
    "quantity_dispensed": 4,
    "days_supply": 28
  },
  "response": {
    "status": "rejected",
    "reject_code": "75",
    "reject_message": "Step Therapy Required"
  },
  "step_therapy_info": {
    "step_therapy_group": "GLP-1 Agonists for Diabetes",
    "current_step": 1,
    "required_step_1_drugs": ["Metformin"],
    "step_1_requirement": "90-day trial of metformin",
    "member_history": {
      "metformin_claims_found": false,
      "step_1_met": false
    },
    "options": [
      "Fill metformin and retry after 90 days",
      "Request exception if metformin contraindicated",
      "Prescriber can submit step therapy override"
    ],
    "bypass_criteria": [
      "eGFR < 30 mL/min",
      "History of lactic acidosis",
      "Documented metformin allergy"
    ]
  }
}
```

### Example 3: Quantity Limit Exceeded

```json
{
  "claim": {
    "claim_id": "RX20250115000002",
    "ndc": "00173068201",
    "drug_name": "Imitrex 100mg Tablet",
    "quantity_dispensed": 18,
    "days_supply": 30
  },
  "response": {
    "status": "rejected",
    "reject_code": "76",
    "reject_message": "Plan Limitations Exceeded"
  },
  "quantity_limit_info": {
    "drug_name": "Sumatriptan 100mg",
    "quantity_limit": 9,
    "per_days": 30,
    "quantity_requested": 18,
    "quantity_over_limit": 9,
    "rationale": "Triptan quantity limits based on FDA dosing guidelines",
    "options": [
      "Reduce quantity to 9 tablets per 30 days",
      "Request quantity limit exception with documentation",
      "Consider preventive migraine therapy"
    ],
    "exception_criteria": [
      "Documented chronic migraine (≥15 headache days/month)",
      "Failure of preventive therapies",
      "Specialist prescription (neurologist/headache specialist)"
    ]
  }
}
```

### Example 4: Non-Formulary with Alternatives

```json
{
  "claim": {
    "claim_id": "RX20250115000003",
    "ndc": "00186077660",
    "drug_name": "Nexium 40mg Capsule",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "response": {
    "status": "rejected",
    "reject_code": "70",
    "reject_message": "Product/Service Not Covered"
  },
  "formulary_info": {
    "drug_name": "Nexium 40mg",
    "status": "non-formulary",
    "reason": "Brand drug with generic alternatives available"
  },
  "alternatives": [
    {
      "ndc": "00093514210",
      "drug_name": "Omeprazole 40mg Capsule",
      "tier": 1,
      "copay": 10.00,
      "covered": true,
      "clinical_note": "First-line PPI, same mechanism of action"
    },
    {
      "ndc": "00378037701",
      "drug_name": "Esomeprazole 40mg Capsule",
      "tier": 1,
      "copay": 10.00,
      "covered": true,
      "clinical_note": "Generic equivalent to Nexium (same active isomer)"
    },
    {
      "ndc": "00093543701",
      "drug_name": "Pantoprazole 40mg Tablet",
      "tier": 1,
      "copay": 10.00,
      "covered": true,
      "clinical_note": "Alternative PPI"
    }
  ],
  "exception_available": true,
  "exception_criteria": "Medical necessity documentation showing failure of formulary alternatives"
}
```

### Example 5: Medicare Part D Coverage

```json
{
  "member": {
    "member_id": "MED001234",
    "plan_type": "Medicare Part D",
    "plan_name": "SilverScript Choice"
  },
  "drug_lookup": {
    "ndc": "00003089421",
    "drug_name": "Eliquis 5mg Tablet"
  },
  "coverage_response": {
    "covered": true,
    "tier": 3,
    "tier_name": "Preferred Brand",
    "phase_pricing": {
      "deductible_phase": {
        "applies": true,
        "member_pays": "100% until $590 deductible met"
      },
      "initial_coverage": {
        "copay": 47.00,
        "30_day_supply": true
      },
      "coverage_gap": {
        "member_pays": "25%",
        "estimated_cost": 145.00
      },
      "catastrophic": {
        "member_pays": "$0",
        "note": "IRA 2025 $2000 OOP cap"
      }
    },
    "utilization_management": {
      "prior_auth_required": false,
      "quantity_limit": 60,
      "quantity_limit_days": 30
    },
    "manufacturer_discount": {
      "program": "Eliquis Savings Card (not for Medicare)",
      "eligible": false,
      "reason": "Medicare beneficiaries not eligible for manufacturer copay cards"
    }
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Tier number | 1-6 (or plan-specific) | Tier 1 (generic), Tier 5 (specialty) |
| Copay/coinsurance | Non-negative, tier-appropriate | $10 (T1), $50 (T3), 20% (T5) |
| PA required | Boolean flag | true (requires prior auth) |
| Step therapy | Array of required prior drugs | ["metformin", "sulfonylurea"] |
| Quantity limit | Per-fill or per-month | 30 tablets/fill, 90/month |
| GPI | 14-digit drug classification | 27100030000310 |
| Formulary status | on/off formulary, tier | "Preferred Brand", "Non-Formulary" |
| Effective date | Valid date range | 2025-01-01 to 2025-12-31 |

### Business Rules

- **Tier Structure**: Generic (T1) < Preferred Brand (T2) < Non-Preferred Brand (T3) < Specialty (T4-5)
- **Step Therapy**: Must try/fail lower-cost options before covering higher-tier drugs
- **Prior Authorization**: Required for specialty, high-cost, or high-risk drugs
- **Quantity Limits**: Prevent stockpiling; encourage appropriate use
- **Age/Gender Limits**: Some drugs limited by age or gender (e.g., fertility drugs)
- **Diagnosis Requirements**: Some drugs require specific ICD-10 codes
- **Specialty Tier**: Typically coinsurance (20-33%) rather than fixed copay
- **Formulary Updates**: Typically quarterly; new drugs may be excluded initially

## Related Skills

### RxMemberSim
- [SKILL.md](SKILL.md) - RxMemberSim overview
- [retail-pharmacy.md](retail-pharmacy.md) - Claim with formulary check
- [specialty-pharmacy.md](specialty-pharmacy.md) - Specialty tier drugs
- [rx-prior-auth.md](rx-prior-auth.md) - PA requirements by formulary status
- [dur-alerts.md](dur-alerts.md) - Clinical edits

### Cross-Product: MemberSim
- [../membersim/plan-benefits.md](../membersim/plan-benefits.md) - Medical plan design

> **Integration Pattern:** Formulary structure (this skill) defines pharmacy benefit drug coverage. Use MemberSim plan-benefits for medical benefit structure. Coordinated plan design ensures consistent deductibles, OOP maximums, and tier structures across medical and pharmacy.

### Cross-Product: PatientSim
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Diabetes drug tiers and alternatives
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - Cardiac medication tiers

> **Integration Pattern:** Use formulary-management to determine which medications are covered and at what cost. This informs PatientSim medication selection when generating realistic patient cohorts.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - GPI, NDC codes
