---
name: synthetic-plan
description: |
  Generate realistic synthetic health plan benefit structures including
  medical benefits, cost sharing, accumulators, coverage rules, and
  plan documents. Supports commercial, Medicare, Medicaid, and Exchange plans.
  
  Trigger phrases: "generate plan", "create benefit plan", "plan design",
  "gold plan", "silver plan", "HDHP plan", "HMO plan", "PPO plan",
  "deductible structure", "cost sharing", "benefit structure"
version: "1.0"
category: synthetic
related_skills:
  - network-types
  - plan-structures
  - synthetic-network
  - pharmacy-benefit-concepts
cross_product:
  - membersim: Plan benefits for claims adjudication
  - rxmembersim: Pharmacy benefit tier for drug claims
---

# Synthetic Plan Generation

## Overview

Generate realistic synthetic health plan benefit structures for use across the HealthSim ecosystem. Plans define the coverage rules, cost sharing, and benefit limits that govern how claims are adjudicated.

This skill generates the **canonical plan entity** that includes:
- Plan identification and type
- Medical benefit structure
- Cost sharing (deductibles, copays, coinsurance)
- Accumulator definitions
- Coverage rules and exclusions
- Pharmacy benefit summary (links to RxMemberSim)

---

## Trigger Phrases

Use this skill when you see:
- "Generate a health plan"
- "Create a PPO benefit plan"
- "Generate a Silver ACA plan"
- "Create an HDHP with HSA"
- "Generate a Medicare Advantage plan"
- "Create cost sharing for a plan"
- "Generate a plan with tiered benefits"

---

## Plan Types by Market

### Commercial Plans

| Type | Description | Key Characteristics |
|------|-------------|---------------------|
| Traditional PPO | Fee-for-service with network | Broad access, moderate cost |
| HMO | Managed care | Lower cost, restricted access |
| HDHP | High deductible health plan | HSA-eligible, consumer-directed |
| POS | Point of service | Hybrid HMO/PPO |

### ACA Marketplace (Exchange)

| Metal Tier | Actuarial Value | Target Member |
|------------|-----------------|---------------|
| Bronze | 60% | Young, healthy, low utilizers |
| Silver | 70% | Moderate utilizers, CSR eligible |
| Gold | 80% | Higher utilizers, predictable costs |
| Platinum | 90% | High utilizers, maximum coverage |
| Catastrophic | <60% | Under 30 or hardship exempt |

### Medicare

| Type | Description | Key Features |
|------|-------------|--------------|
| Original Medicare | FFS Parts A+B | Government-administered |
| Medicare Advantage | Part C managed care | Private plan, all-in-one |
| Part D | Prescription drug | Standalone or MA-PD |
| Medigap | Supplement to Original | Fills gaps in A+B |

### Medicaid

| Type | Description | Eligibility |
|------|-------------|-------------|
| Traditional | State-administered FFS | Income-based |
| Managed Care | Private plan administration | State contracts |
| CHIP | Children's coverage | Income-based, children |

---

## Canonical Schema

### Plan Definition

```json
{
  "plan_id": "string",
  "plan_name": "string",
  "plan_marketing_name": "string",
  "plan_year": "integer (YYYY)",
  "effective_date": "YYYY-MM-DD",
  "termination_date": "YYYY-MM-DD | null",
  "status": "Active | Pending | Terminated",
  "payer": {
    "payer_id": "string",
    "payer_name": "string"
  },
  "plan_type": {
    "market_segment": "Commercial | Medicare | Medicaid | Exchange",
    "product_type": "HMO | PPO | EPO | POS | HDHP | PFFS",
    "funding_type": "Fully Insured | Self-Funded | Level-Funded",
    "metal_tier": "Bronze | Silver | Gold | Platinum | Catastrophic | null",
    "actuarial_value": "number (0.5-1.0)"
  },
  "network": {
    "network_id": "string",
    "network_name": "string",
    "network_type": "string"
  },
  "geographic_coverage": {
    "states": ["string"],
    "service_area_id": "string"
  },
  "cost_sharing": {
    "deductible": {
      "individual_in_network": "number",
      "family_in_network": "number",
      "individual_out_of_network": "number | null",
      "family_out_of_network": "number | null",
      "embedded": "boolean",
      "applies_to_rx": "boolean"
    },
    "out_of_pocket_maximum": {
      "individual_in_network": "number",
      "family_in_network": "number",
      "individual_out_of_network": "number | null",
      "family_out_of_network": "number | null",
      "embedded": "boolean",
      "includes_deductible": "boolean"
    },
    "coinsurance": {
      "in_network": "number (0-1)",
      "out_of_network": "number (0-1) | null"
    }
  },
  "medical_benefits": {
    "preventive_care": {
      "cost_sharing": "No Cost | Copay | Coinsurance",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "notes": "string"
    },
    "primary_care_visit": {
      "cost_sharing": "Copay | Coinsurance | Deductible + Coinsurance",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean"
    },
    "specialist_visit": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean"
    },
    "emergency_room": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "waived_if_admitted": "boolean"
    },
    "urgent_care": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean"
    },
    "inpatient_hospital": {
      "cost_sharing": "string",
      "copay_per_day": "number | null",
      "copay_per_admission": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "day_limit": "integer | null"
    },
    "outpatient_surgery": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean"
    },
    "lab_xray": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean"
    },
    "advanced_imaging": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "preauthorization_required": "boolean"
    },
    "mental_health_outpatient": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "visit_limit": "integer | null"
    },
    "mental_health_inpatient": {
      "cost_sharing": "string",
      "copay_per_day": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "day_limit": "integer | null"
    },
    "rehabilitation": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "visit_limit": "integer"
    },
    "skilled_nursing": {
      "cost_sharing": "string",
      "copay_per_day": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "day_limit": "integer"
    },
    "home_health": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean",
      "visit_limit": "integer | null"
    },
    "durable_medical_equipment": {
      "cost_sharing": "string",
      "coinsurance": "number",
      "deductible_applies": "boolean"
    },
    "telehealth": {
      "cost_sharing": "string",
      "copay": "number | null",
      "coinsurance": "number | null",
      "deductible_applies": "boolean"
    }
  },
  "pharmacy_benefit": {
    "integrated_with_medical": "boolean",
    "separate_deductible": "boolean",
    "rx_deductible": {
      "individual": "number | null",
      "family": "number | null"
    },
    "tier_structure": {
      "tier_count": "integer",
      "tiers": [
        {
          "tier_number": "integer",
          "tier_name": "string",
          "cost_sharing_type": "Copay | Coinsurance",
          "retail_30_day": "number",
          "retail_90_day": "number | null",
          "mail_90_day": "number | null",
          "deductible_applies": "boolean"
        }
      ]
    },
    "specialty_tier": {
      "coinsurance": "number",
      "maximum_copay": "number | null",
      "deductible_applies": "boolean",
      "specialty_pharmacy_required": "boolean"
    }
  },
  "hsa_hra": {
    "hsa_eligible": "boolean",
    "hra_available": "boolean",
    "employer_contribution": "number | null",
    "contribution_type": "HSA | HRA | FSA | null"
  },
  "coverage_rules": {
    "waiting_period_days": "integer",
    "preexisting_condition_exclusion": "boolean",
    "age_limit_dependent": "integer",
    "domestic_partner_coverage": "boolean",
    "infertility_coverage": "boolean",
    "bariatric_surgery_coverage": "boolean",
    "hearing_aids_coverage": "boolean"
  },
  "utilization_management": {
    "preauthorization_required": ["string"],
    "step_therapy_drugs": ["string"],
    "referral_required": "boolean",
    "concurrent_review": "boolean"
  },
  "regulatory_compliance": {
    "aca_compliant": "boolean",
    "essential_health_benefits": "boolean",
    "mental_health_parity": "boolean",
    "preventive_care_mandate": "boolean"
  },
  "documents": {
    "summary_of_benefits_coverage": "string (URL)",
    "evidence_of_coverage": "string (URL)",
    "provider_directory": "string (URL)",
    "formulary": "string (URL)"
  }
}
```

---

## Generation Parameters

### Required Context

| Parameter | Description | Default |
|-----------|-------------|---------|
| **market_segment** | Commercial, Medicare, etc. | Commercial |
| **product_type** | HMO, PPO, HDHP, etc. | PPO |

### Optional Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **metal_tier** | Bronze-Platinum (Exchange) | Silver |
| **plan_year** | Coverage year | Current year |
| **state** | State for compliance | Random |
| **deductible_range** | Low/Medium/High | Medium |
| **hsa_eligible** | HDHP with HSA | false |
| **network_id** | Link to network | Generate new |
| **include_pharmacy** | Full pharmacy detail | true |

---

## Examples

### Example 1: Standard Commercial PPO

**Prompt**: "Generate a commercial PPO plan with moderate cost sharing"

**Response**:

```json
{
  "plan_id": "COMM-PPO-2024-001",
  "plan_name": "Choice Plus PPO",
  "plan_marketing_name": "Blue Choice Plus PPO",
  "plan_year": 2024,
  "effective_date": "2024-01-01",
  "status": "Active",
  "payer": {
    "payer_id": "BCBS-IL",
    "payer_name": "Blue Cross Blue Shield of Illinois"
  },
  "plan_type": {
    "market_segment": "Commercial",
    "product_type": "PPO",
    "funding_type": "Fully Insured",
    "metal_tier": null,
    "actuarial_value": 0.78
  },
  "network": {
    "network_id": "IL-PPO-CHOICE",
    "network_name": "Blue Choice Network",
    "network_type": "PPO"
  },
  "cost_sharing": {
    "deductible": {
      "individual_in_network": 1500,
      "family_in_network": 3000,
      "individual_out_of_network": 3000,
      "family_out_of_network": 6000,
      "embedded": true,
      "applies_to_rx": false
    },
    "out_of_pocket_maximum": {
      "individual_in_network": 6000,
      "family_in_network": 12000,
      "individual_out_of_network": 12000,
      "family_out_of_network": 24000,
      "embedded": true,
      "includes_deductible": true
    },
    "coinsurance": {
      "in_network": 0.20,
      "out_of_network": 0.40
    }
  },
  "medical_benefits": {
    "preventive_care": {
      "cost_sharing": "No Cost",
      "copay": null,
      "deductible_applies": false,
      "notes": "100% covered for in-network preventive services"
    },
    "primary_care_visit": {
      "cost_sharing": "Copay",
      "copay": 30,
      "deductible_applies": false
    },
    "specialist_visit": {
      "cost_sharing": "Copay",
      "copay": 50,
      "deductible_applies": false
    },
    "emergency_room": {
      "cost_sharing": "Copay + Coinsurance",
      "copay": 250,
      "coinsurance": 0.20,
      "deductible_applies": true,
      "waived_if_admitted": true
    },
    "urgent_care": {
      "cost_sharing": "Copay",
      "copay": 50,
      "deductible_applies": false
    },
    "inpatient_hospital": {
      "cost_sharing": "Deductible + Coinsurance",
      "copay_per_day": null,
      "coinsurance": 0.20,
      "deductible_applies": true,
      "day_limit": null
    },
    "outpatient_surgery": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.20,
      "deductible_applies": true
    },
    "lab_xray": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.20,
      "deductible_applies": true
    },
    "advanced_imaging": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.20,
      "deductible_applies": true,
      "preauthorization_required": true
    },
    "mental_health_outpatient": {
      "cost_sharing": "Copay",
      "copay": 30,
      "deductible_applies": false,
      "visit_limit": null
    },
    "mental_health_inpatient": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.20,
      "deductible_applies": true,
      "day_limit": null
    },
    "rehabilitation": {
      "cost_sharing": "Copay",
      "copay": 40,
      "deductible_applies": false,
      "visit_limit": 60
    },
    "skilled_nursing": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.20,
      "deductible_applies": true,
      "day_limit": 60
    },
    "durable_medical_equipment": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.20,
      "deductible_applies": true
    },
    "telehealth": {
      "cost_sharing": "Copay",
      "copay": 0,
      "deductible_applies": false
    }
  },
  "pharmacy_benefit": {
    "integrated_with_medical": false,
    "separate_deductible": false,
    "tier_structure": {
      "tier_count": 4,
      "tiers": [
        {
          "tier_number": 1,
          "tier_name": "Generic",
          "cost_sharing_type": "Copay",
          "retail_30_day": 10,
          "retail_90_day": 25,
          "mail_90_day": 20,
          "deductible_applies": false
        },
        {
          "tier_number": 2,
          "tier_name": "Preferred Brand",
          "cost_sharing_type": "Copay",
          "retail_30_day": 35,
          "retail_90_day": 90,
          "mail_90_day": 70,
          "deductible_applies": false
        },
        {
          "tier_number": 3,
          "tier_name": "Non-Preferred Brand",
          "cost_sharing_type": "Copay",
          "retail_30_day": 60,
          "retail_90_day": 150,
          "mail_90_day": 120,
          "deductible_applies": false
        },
        {
          "tier_number": 4,
          "tier_name": "Specialty",
          "cost_sharing_type": "Coinsurance",
          "retail_30_day": 0.25,
          "deductible_applies": true
        }
      ]
    },
    "specialty_tier": {
      "coinsurance": 0.25,
      "maximum_copay": 250,
      "deductible_applies": true,
      "specialty_pharmacy_required": true
    }
  },
  "hsa_hra": {
    "hsa_eligible": false,
    "hra_available": false
  },
  "utilization_management": {
    "preauthorization_required": [
      "Inpatient admission",
      "Advanced imaging (MRI, CT, PET)",
      "Specialty drugs",
      "Elective surgery"
    ],
    "referral_required": false
  },
  "regulatory_compliance": {
    "aca_compliant": true,
    "essential_health_benefits": true,
    "mental_health_parity": true,
    "preventive_care_mandate": true
  }
}
```

---

### Example 2: HDHP with HSA

**Prompt**: "Generate an HSA-eligible high deductible health plan"

**Response**:

```json
{
  "plan_id": "COMM-HDHP-2024-001",
  "plan_name": "HSA Advantage HDHP",
  "plan_marketing_name": "Consumer Choice HSA Plan",
  "plan_year": 2024,
  "effective_date": "2024-01-01",
  "status": "Active",
  "payer": {
    "payer_id": "AETNA",
    "payer_name": "Aetna"
  },
  "plan_type": {
    "market_segment": "Commercial",
    "product_type": "HDHP",
    "funding_type": "Self-Funded",
    "metal_tier": null,
    "actuarial_value": 0.68
  },
  "network": {
    "network_id": "AETNA-OA",
    "network_name": "Aetna Open Access",
    "network_type": "PPO"
  },
  "cost_sharing": {
    "deductible": {
      "individual_in_network": 3200,
      "family_in_network": 6400,
      "individual_out_of_network": 6000,
      "family_out_of_network": 12000,
      "embedded": false,
      "applies_to_rx": true
    },
    "out_of_pocket_maximum": {
      "individual_in_network": 6550,
      "family_in_network": 13100,
      "individual_out_of_network": 13100,
      "family_out_of_network": 26200,
      "embedded": true,
      "includes_deductible": true
    },
    "coinsurance": {
      "in_network": 0.10,
      "out_of_network": 0.30
    }
  },
  "medical_benefits": {
    "preventive_care": {
      "cost_sharing": "No Cost",
      "copay": null,
      "deductible_applies": false,
      "notes": "HSA-eligible preventive care covered pre-deductible"
    },
    "primary_care_visit": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.10,
      "deductible_applies": true
    },
    "specialist_visit": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.10,
      "deductible_applies": true
    },
    "emergency_room": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.10,
      "deductible_applies": true,
      "waived_if_admitted": false
    },
    "urgent_care": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.10,
      "deductible_applies": true
    },
    "inpatient_hospital": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.10,
      "deductible_applies": true
    },
    "outpatient_surgery": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.10,
      "deductible_applies": true
    }
  },
  "pharmacy_benefit": {
    "integrated_with_medical": true,
    "separate_deductible": false,
    "tier_structure": {
      "tier_count": 3,
      "tiers": [
        {
          "tier_number": 1,
          "tier_name": "Generic",
          "cost_sharing_type": "Coinsurance",
          "retail_30_day": 0.10,
          "mail_90_day": 0.10,
          "deductible_applies": true
        },
        {
          "tier_number": 2,
          "tier_name": "Brand",
          "cost_sharing_type": "Coinsurance",
          "retail_30_day": 0.25,
          "mail_90_day": 0.25,
          "deductible_applies": true
        },
        {
          "tier_number": 3,
          "tier_name": "Specialty",
          "cost_sharing_type": "Coinsurance",
          "retail_30_day": 0.30,
          "deductible_applies": true
        }
      ]
    }
  },
  "hsa_hra": {
    "hsa_eligible": true,
    "hra_available": false,
    "employer_contribution": 1000,
    "contribution_type": "HSA"
  },
  "irs_limits_2024": {
    "minimum_deductible_individual": 1600,
    "minimum_deductible_family": 3200,
    "maximum_oop_individual": 8050,
    "maximum_oop_family": 16100,
    "contribution_limit_individual": 4150,
    "contribution_limit_family": 8300,
    "catch_up_55_plus": 1000
  }
}
```

---

### Example 3: ACA Silver Plan

**Prompt**: "Generate a Silver ACA marketplace plan"

**Response**:

```json
{
  "plan_id": "EXCH-SLV-2024-001",
  "plan_name": "Marketplace Silver 70",
  "plan_marketing_name": "Silver Essential",
  "plan_year": 2024,
  "effective_date": "2024-01-01",
  "status": "Active",
  "payer": {
    "payer_id": "OSCAR",
    "payer_name": "Oscar Health"
  },
  "plan_type": {
    "market_segment": "Exchange",
    "product_type": "EPO",
    "funding_type": "Fully Insured",
    "metal_tier": "Silver",
    "actuarial_value": 0.70
  },
  "network": {
    "network_id": "OSCAR-SLCT",
    "network_name": "Oscar Select Network",
    "network_type": "EPO"
  },
  "geographic_coverage": {
    "states": ["NY"],
    "service_area_id": "NY001"
  },
  "cost_sharing": {
    "deductible": {
      "individual_in_network": 4500,
      "family_in_network": 9000,
      "individual_out_of_network": null,
      "family_out_of_network": null,
      "embedded": true,
      "applies_to_rx": true
    },
    "out_of_pocket_maximum": {
      "individual_in_network": 9450,
      "family_in_network": 18900,
      "individual_out_of_network": null,
      "family_out_of_network": null,
      "embedded": true,
      "includes_deductible": true
    },
    "coinsurance": {
      "in_network": 0.30,
      "out_of_network": null
    }
  },
  "cost_sharing_reduction_variants": {
    "csr_94": {
      "deductible_individual": 200,
      "deductible_family": 400,
      "oop_max_individual": 3000,
      "oop_max_family": 6000
    },
    "csr_87": {
      "deductible_individual": 600,
      "deductible_family": 1200,
      "oop_max_individual": 3000,
      "oop_max_family": 6000
    },
    "csr_73": {
      "deductible_individual": 3500,
      "deductible_family": 7000,
      "oop_max_individual": 6800,
      "oop_max_family": 13600
    }
  },
  "medical_benefits": {
    "preventive_care": {
      "cost_sharing": "No Cost",
      "deductible_applies": false
    },
    "primary_care_visit": {
      "cost_sharing": "Copay",
      "copay": 35,
      "deductible_applies": false
    },
    "specialist_visit": {
      "cost_sharing": "Copay",
      "copay": 70,
      "deductible_applies": false
    },
    "emergency_room": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.30,
      "deductible_applies": true
    },
    "urgent_care": {
      "cost_sharing": "Copay",
      "copay": 75,
      "deductible_applies": false
    },
    "inpatient_hospital": {
      "cost_sharing": "Deductible + Coinsurance",
      "coinsurance": 0.30,
      "deductible_applies": true
    },
    "mental_health_outpatient": {
      "cost_sharing": "Copay",
      "copay": 35,
      "deductible_applies": false
    }
  },
  "pharmacy_benefit": {
    "integrated_with_medical": true,
    "tier_structure": {
      "tier_count": 4,
      "tiers": [
        {"tier_number": 1, "tier_name": "Generic", "retail_30_day": 15, "deductible_applies": false},
        {"tier_number": 2, "tier_name": "Preferred Brand", "retail_30_day": 50, "deductible_applies": false},
        {"tier_number": 3, "tier_name": "Non-Preferred", "retail_30_day": 100, "deductible_applies": true},
        {"tier_number": 4, "tier_name": "Specialty", "retail_30_day": 0.40, "deductible_applies": true}
      ]
    }
  },
  "essential_health_benefits": {
    "ambulatory_patient_services": true,
    "emergency_services": true,
    "hospitalization": true,
    "maternity_and_newborn": true,
    "mental_health_substance_use": true,
    "prescription_drugs": true,
    "rehabilitative_habilitative": true,
    "laboratory_services": true,
    "preventive_wellness_chronic": true,
    "pediatric_services": true
  },
  "regulatory_compliance": {
    "aca_compliant": true,
    "qhp_certified": true,
    "essential_health_benefits": true,
    "mental_health_parity": true,
    "no_annual_limits": true,
    "no_lifetime_limits": true,
    "no_preexisting_exclusion": true
  }
}
```

---

### Example 4: Medicare Advantage Plan

**Prompt**: "Generate a Medicare Advantage HMO plan"

**Response**:

```json
{
  "plan_id": "MA-HMO-2024-001",
  "plan_name": "Medicare Advantage Choice HMO",
  "plan_marketing_name": "UnitedHealthcare Medicare Advantage (HMO)",
  "plan_year": 2024,
  "effective_date": "2024-01-01",
  "status": "Active",
  "payer": {
    "payer_id": "UHC-MA",
    "payer_name": "UnitedHealthcare"
  },
  "plan_type": {
    "market_segment": "Medicare",
    "product_type": "HMO",
    "funding_type": "Medicare Advantage",
    "snp_type": null
  },
  "medicare_specific": {
    "contract_id": "H1234",
    "plan_id": "001",
    "segment_id": "000",
    "cms_star_rating": 4,
    "part_d_included": true,
    "part_d_lis_level": null,
    "moop_type": "Mandatory",
    "frailty_adjustment": false
  },
  "cost_sharing": {
    "monthly_premium": 0,
    "part_b_premium_reduction": 0,
    "deductible": {
      "medical": 0,
      "drug": 545
    },
    "out_of_pocket_maximum": {
      "in_network": 5900,
      "out_of_network": null
    }
  },
  "medical_benefits": {
    "inpatient_hospital": {
      "days_1_5": 350,
      "days_6_plus": 0,
      "lifetime_reserve": 0
    },
    "skilled_nursing": {
      "days_1_20": 0,
      "days_21_100": 188,
      "day_limit": 100
    },
    "primary_care_visit": {
      "copay": 0
    },
    "specialist_visit": {
      "copay": 40
    },
    "emergency_room": {
      "copay": 90,
      "waived_if_admitted": true
    },
    "urgent_care": {
      "copay": 40
    },
    "outpatient_surgery_asc": {
      "copay": 250
    },
    "outpatient_surgery_hospital": {
      "copay": 350
    },
    "diagnostic_tests": {
      "copay": 0
    },
    "lab_services": {
      "copay": 0
    },
    "x_ray": {
      "copay": 10
    },
    "advanced_imaging": {
      "copay": 250
    }
  },
  "supplemental_benefits": {
    "dental": {
      "preventive": "Covered - $0",
      "comprehensive": "$2000 annual maximum",
      "copay_percentage": 0.50
    },
    "vision": {
      "routine_exam": "$0 copay",
      "eyewear_allowance": 200
    },
    "hearing": {
      "routine_exam": "$0 copay",
      "hearing_aid_allowance": 1500
    },
    "fitness": {
      "program": "SilverSneakers",
      "included": true
    },
    "otc_allowance": {
      "quarterly_amount": 60,
      "annual_amount": 240
    },
    "transportation": {
      "trips_per_year": 24,
      "one_way_trips": true
    },
    "telehealth": {
      "copay": 0
    },
    "meals": {
      "post_discharge_meals": 14,
      "meals_per_day": 2
    }
  },
  "part_d": {
    "deductible": 545,
    "initial_coverage_limit": 5030,
    "catastrophic_threshold": 8000,
    "tier_structure": {
      "tier_count": 5,
      "tiers": [
        {"tier": 1, "name": "Preferred Generic", "copay_30": 0, "copay_90": 0},
        {"tier": 2, "name": "Generic", "copay_30": 10, "copay_90": 20},
        {"tier": 3, "name": "Preferred Brand", "copay_30": 47, "copay_90": 141},
        {"tier": 4, "name": "Non-Preferred Drug", "coinsurance": 0.45},
        {"tier": 5, "name": "Specialty", "coinsurance": 0.25, "max": 100}
      ]
    },
    "coverage_gap": {
      "generic_coinsurance": 0.25,
      "brand_coinsurance": 0.25
    },
    "catastrophic": {
      "generic_copay": 4.15,
      "brand_copay": 10.35,
      "coinsurance": 0.05
    }
  }
}
```

---

## Cross-Product Integration

### MemberSim Integration

Plan defines adjudication rules:

```
MemberSim Claim + NetworkSim Plan → Adjudication

Plan provides:
- Deductible amount and status
- Copay or coinsurance for service
- OOP max tracking
- Coverage rules (limits, exclusions)
```

### RxMemberSim Integration

Plan defines pharmacy benefits:

```
RxMemberSim Claim + NetworkSim Plan → Drug Adjudication

Plan provides:
- Tier structure and cost sharing
- Specialty pharmacy requirements
- Prior authorization rules
- Rx deductible (if separate)
```

---

## Validation Rules

### Cost Sharing Validation

| Rule | Validation |
|------|------------|
| HDHP Minimum | Deductible ≥ IRS minimum ($1,600/$3,200 for 2024) |
| HDHP Maximum | OOP max ≤ IRS maximum ($8,050/$16,100 for 2024) |
| ACA OOP Max | ≤ $9,450/$18,900 for 2024 |
| Family ≥ Individual | Family amounts ≥ individual amounts |

### ACA Compliance

| Rule | Validation |
|------|------------|
| Metal Tier AV | Bronze 60%, Silver 70%, Gold 80%, Platinum 90% (±2%) |
| EHB Coverage | All 10 essential health benefits required |
| Preventive Care | No cost sharing for preventive services |
| Mental Health Parity | Equal to medical benefits |

---

## Related Skills

- [Plan Structures](../reference/plan-structures.md) - Benefit component details
- [Network Types](../reference/network-types.md) - Network model context
- [Synthetic Network](synthetic-network.md) - Associated network
- [Pharmacy Benefit Concepts](../reference/pharmacy-benefit-concepts.md) - Rx benefit detail

---

*Synthetic Plan is a generation skill in the NetworkSim product.*
