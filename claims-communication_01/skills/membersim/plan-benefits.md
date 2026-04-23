---
name: plan-benefits
description: "Health plan benefit structures including HMO, PPO, HDHP with cost-sharing configurations. Triggers: plan, benefit plan, plan design, HMO, PPO, HDHP, copay structure, deductible, plan configuration, cost sharing"
---

# Plan & Benefits Configuration Cohort

A cohort template for generating health plan benefit structures including HMO, PPO, HDHP, and other plan types with cost-sharing configurations.

## For Claude

Use this skill when the user requests plan design or benefit configuration cohorts. This teaches you how to generate **realistic plan structures** with appropriate cost-sharing, network tiers, and coverage limits.

**When to apply this skill:**

- User mentions plan, benefit plan, or plan design
- User requests HMO, PPO, HDHP, or other plan types
- User specifies copay structure or deductible design
- User asks for plan configuration examples
- User needs benefit structure documentation

**Key capabilities this skill provides:**

- How to structure plan types (HMO, PPO, EPO, POS, HDHP)
- How to configure cost-sharing tiers and copay structures
- How to model network types and tier differentials
- How to set up HSA-eligible plan requirements
- How to integrate medical and pharmacy benefits

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: MemberSim
- **Tags**: plan-design, benefits, payer, configuration
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic health plan benefit configurations. It models complete plan structures with cost-sharing, network rules, and coverage limits appropriate to each plan type.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "plan", "benefit plan", "plan design"
- "HMO", "PPO", "HDHP", "EPO"
- "copay structure", "deductible structure"
- "cost sharing", "network tier"

**Plan Cohorts**:

- "Generate an HMO plan configuration"
- "Create an HDHP with HSA"
- "Generate a tiered network PPO plan"

## Trigger Phrases

- plan
- benefit plan
- plan design
- benefit structure
- coverage plan
- HMO plan
- PPO plan
- HDHP
- high deductible
- plan configuration
- benefit configuration
- copay structure
- deductible structure
- cost sharing
- network tier
- plan tier

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| plan_type | string | PPO | HMO, PPO, EPO, POS, HDHP, INDEMNITY |
| metal_tier | string | gold | bronze, silver, gold, platinum |
| network_type | string | broad | broad, narrow, tiered |
| hsa_eligible | bool | false | true, false |
| include_rx | bool | true | true, false |
| include_dental | bool | false | true, false |
| include_vision | bool | false | true, false |

## Plan Types

### HMO (Health Maintenance Organization)

Managed care with gatekeeping and network restrictions.

**Characteristics:**
- PCP required and acts as gatekeeper
- Referrals required for specialists
- In-network only (no OON coverage except emergency)
- Lower premiums, lower out-of-pocket
- Typically no deductible for in-network services

```json
{
  "plan_type": "HMO",
  "plan_code": "HMO-STD",
  "plan_name": "HMO Standard Plan",
  "network_requirement": "in_network_only",
  "pcp_required": true,
  "referral_required": true,
  "benefits": {
    "in_network": {
      "individual_deductible": 0,
      "family_deductible": 0,
      "individual_oop_max": 3000,
      "family_oop_max": 6000,
      "pcp_copay": 20,
      "specialist_copay": 40,
      "urgent_care_copay": 50,
      "er_copay": 150,
      "inpatient_copay": 250,
      "outpatient_surgery_copay": 200,
      "preventive_covered_100": true
    },
    "out_of_network": {
      "covered": false,
      "emergency_only": true
    }
  }
}
```

### PPO (Preferred Provider Organization)

Flexible network with in-network and out-of-network options.

**Characteristics:**
- No PCP required
- No referrals required
- In-network preferred but OON covered at lower benefit
- Higher premiums, more flexibility
- Deductible applies to most services

```json
{
  "plan_type": "PPO",
  "plan_code": "PPO-GOLD",
  "plan_name": "PPO Gold Plan",
  "network_requirement": "in_network_preferred",
  "pcp_required": false,
  "referral_required": false,
  "benefits": {
    "in_network": {
      "individual_deductible": 500,
      "family_deductible": 1000,
      "individual_oop_max": 4000,
      "family_oop_max": 8000,
      "coinsurance": 20,
      "pcp_copay": 25,
      "specialist_copay": 50,
      "urgent_care_copay": 75,
      "er_copay": 150,
      "inpatient_coinsurance": 20,
      "outpatient_surgery_coinsurance": 20,
      "preventive_covered_100": true,
      "deductible_applies_to_copays": false
    },
    "out_of_network": {
      "individual_deductible": 1500,
      "family_deductible": 3000,
      "individual_oop_max": 8000,
      "family_oop_max": 16000,
      "coinsurance": 40,
      "deductible_applies": true,
      "balance_billing_allowed": true
    }
  }
}
```

### EPO (Exclusive Provider Organization)

Hybrid between HMO and PPO.

**Characteristics:**
- No PCP required
- No referrals required
- In-network only (like HMO)
- Typically lower cost than PPO

```json
{
  "plan_type": "EPO",
  "plan_code": "EPO-STANDARD",
  "plan_name": "EPO Standard Plan",
  "network_requirement": "in_network_only",
  "pcp_required": false,
  "referral_required": false,
  "benefits": {
    "in_network": {
      "individual_deductible": 250,
      "family_deductible": 500,
      "individual_oop_max": 3500,
      "family_oop_max": 7000,
      "coinsurance": 15,
      "pcp_copay": 20,
      "specialist_copay": 40,
      "er_copay": 150
    },
    "out_of_network": {
      "covered": false,
      "emergency_only": true
    }
  }
}
```

### POS (Point of Service)

Combination of HMO and PPO features.

**Characteristics:**
- PCP required
- Referrals required for in-network specialist
- OON covered without referral at higher cost
- Moderate flexibility and cost

```json
{
  "plan_type": "POS",
  "plan_code": "POS-CHOICE",
  "plan_name": "POS Choice Plan",
  "network_requirement": "in_network_preferred",
  "pcp_required": true,
  "referral_required": true,
  "benefits": {
    "in_network": {
      "individual_deductible": 300,
      "family_deductible": 600,
      "individual_oop_max": 3500,
      "family_oop_max": 7000,
      "coinsurance": 15,
      "pcp_copay": 20,
      "specialist_copay": 35
    },
    "out_of_network": {
      "individual_deductible": 1000,
      "family_deductible": 2000,
      "individual_oop_max": 6000,
      "family_oop_max": 12000,
      "coinsurance": 35,
      "referral_required": false
    }
  }
}
```

### HDHP (High Deductible Health Plan)

IRS-qualified plan compatible with HSA.

**Characteristics:**
- High deductible before plan pays
- HSA-eligible (if no other coverage)
- Lower premiums
- No copays until deductible met (except preventive)
- IRS minimum deductible and maximum OOP limits

```json
{
  "plan_type": "HDHP",
  "plan_code": "HDHP-HSA",
  "plan_name": "HDHP with HSA",
  "network_requirement": "in_network_preferred",
  "pcp_required": false,
  "referral_required": false,
  "hsa_eligible": true,
  "benefits": {
    "in_network": {
      "individual_deductible": 1600,
      "family_deductible": 3200,
      "individual_oop_max": 7050,
      "family_oop_max": 14100,
      "coinsurance": 20,
      "deductible_applies_to_all": true,
      "preventive_covered_100": true,
      "preventive_exempt_from_deductible": true
    },
    "out_of_network": {
      "individual_deductible": 3200,
      "family_deductible": 6400,
      "individual_oop_max": 14100,
      "family_oop_max": 28200,
      "coinsurance": 40
    }
  },
  "hsa": {
    "employer_contribution_individual": 500,
    "employer_contribution_family": 1000,
    "individual_contribution_limit": 4150,
    "family_contribution_limit": 8300,
    "catch_up_contribution_55_plus": 1000
  }
}
```

## Metal Tiers (ACA Marketplace)

Actuarial value determines metal tier:

| Tier | Actuarial Value | Cost Sharing |
|------|-----------------|--------------|
| Bronze | 60% | High deductible, low premium |
| Silver | 70% | Moderate cost sharing |
| Gold | 80% | Lower deductible, higher premium |
| Platinum | 90% | Lowest cost sharing, highest premium |

### Bronze Plan Example
```json
{
  "metal_tier": "bronze",
  "actuarial_value": 60,
  "plan_code": "BRONZE-6000",
  "individual_deductible": 6000,
  "family_deductible": 12000,
  "individual_oop_max": 8700,
  "family_oop_max": 17400,
  "coinsurance": 40,
  "pcp_copay_after_deductible": 40,
  "monthly_premium_individual": 250
}
```

### Silver Plan Example
```json
{
  "metal_tier": "silver",
  "actuarial_value": 70,
  "plan_code": "SILVER-3000",
  "individual_deductible": 3000,
  "family_deductible": 6000,
  "individual_oop_max": 8700,
  "family_oop_max": 17400,
  "coinsurance": 30,
  "pcp_copay": 35,
  "monthly_premium_individual": 400
}
```

### Gold Plan Example
```json
{
  "metal_tier": "gold",
  "actuarial_value": 80,
  "plan_code": "GOLD-1000",
  "individual_deductible": 1000,
  "family_deductible": 2000,
  "individual_oop_max": 6000,
  "family_oop_max": 12000,
  "coinsurance": 20,
  "pcp_copay": 25,
  "monthly_premium_individual": 550
}
```

### Platinum Plan Example
```json
{
  "metal_tier": "platinum",
  "actuarial_value": 90,
  "plan_code": "PLATINUM-250",
  "individual_deductible": 250,
  "family_deductible": 500,
  "individual_oop_max": 4000,
  "family_oop_max": 8000,
  "coinsurance": 10,
  "pcp_copay": 15,
  "monthly_premium_individual": 700
}
```

## Service-Specific Benefits

### Professional Services

| Service | Typical Benefit |
|---------|-----------------|
| PCP Office Visit | $20-$40 copay |
| Specialist Visit | $40-$75 copay |
| Preventive Care | 100% covered |
| Telehealth | $0-$25 copay |
| Mental Health Outpatient | $25-$50 copay |
| Physical Therapy | $40-$60 copay per visit |
| Chiropractic | $40 copay, 20 visit limit |
| Allergy Testing | Subject to deductible |
| Lab Work | Subject to deductible or $0-$30 copay |
| X-Ray/Imaging | Subject to deductible |
| Advanced Imaging (MRI/CT) | Subject to deductible + 20% coinsurance |

### Facility Services

| Service | Typical Benefit |
|---------|-----------------|
| Emergency Room | $150-$500 copay (waived if admitted) |
| Urgent Care | $50-$100 copay |
| Inpatient Hospital | $250-$500/day or 20% coinsurance |
| Outpatient Surgery | $200-$500 copay or 20% coinsurance |
| Ambulance | $150-$300 copay or 20% coinsurance |
| Skilled Nursing | 20% coinsurance, 60-day limit |
| Inpatient Rehab | 20% coinsurance, 30-day limit |
| Hospice | 100% covered |

### Pharmacy Benefits

| Tier | Description | Typical Cost |
|------|-------------|--------------|
| Tier 1 | Preferred Generic | $10-$15 |
| Tier 2 | Non-Preferred Generic | $20-$30 |
| Tier 3 | Preferred Brand | $40-$60 |
| Tier 4 | Non-Preferred Brand | $75-$100 |
| Tier 5 | Specialty | 20-30% coinsurance |

```json
{
  "pharmacy_benefits": {
    "deductible_applies": false,
    "retail_30_day": {
      "tier_1": 10,
      "tier_2": 25,
      "tier_3": 50,
      "tier_4": 80,
      "tier_5_coinsurance": 25
    },
    "mail_order_90_day": {
      "tier_1": 25,
      "tier_2": 62.50,
      "tier_3": 125,
      "tier_4": 200,
      "tier_5_coinsurance": 25
    },
    "specialty_max": 250,
    "day_supply_limit_specialty": 30
  }
}
```

## Network Tiers

Some plans have tiered networks with different cost sharing:

```json
{
  "network_tiers": {
    "tier_1": {
      "description": "Preferred providers - lowest cost",
      "pcp_copay": 15,
      "specialist_copay": 30,
      "coinsurance": 10
    },
    "tier_2": {
      "description": "Participating providers - moderate cost",
      "pcp_copay": 25,
      "specialist_copay": 50,
      "coinsurance": 20
    },
    "tier_3": {
      "description": "Out-of-network - highest cost",
      "deductible": 2000,
      "coinsurance": 40,
      "balance_billing": true
    }
  }
}
```

## Benefit Exclusions

Common exclusions from coverage:

| Category | Common Exclusions |
|----------|-------------------|
| Cosmetic | Cosmetic surgery, teeth whitening |
| Experimental | Experimental treatments, clinical trials |
| Custodial | Long-term custodial care |
| Alternative | Acupuncture (unless rider), naturopathy |
| Dental/Vision | Adult routine (unless included) |
| Workers Comp | Work-related injuries |
| Non-Compliance | Services when non-compliant with treatment |
| Travel | Non-emergency care outside service area |
| Weight Loss | Weight loss surgery (unless criteria met) |
| Infertility | IVF (varies by state/employer) |

## Prior Authorization Requirements

Services typically requiring prior authorization:

| Service Category | Examples |
|------------------|----------|
| Inpatient Admissions | All elective, some urgent |
| Surgery | Most non-emergency procedures |
| Advanced Imaging | MRI, CT, PET scans |
| Specialty Drugs | Biologics, specialty injectables |
| DME | Wheelchairs, CPAP, prosthetics |
| Outpatient Procedures | Colonoscopy, cardiac cath |
| Mental Health | Inpatient psych, residential treatment |
| Rehabilitation | Inpatient rehab, SNF |
| Home Health | Skilled nursing, PT at home |

## Examples

### Example 1: Complete PPO Plan

**Request:** "Generate a PPO Gold plan configuration"

```json
{
  "plan": {
    "plan_code": "PPO-GOLD-2025",
    "plan_name": "PPO Gold Plan 2025",
    "plan_type": "PPO",
    "metal_tier": "gold",
    "effective_date": "2025-01-01",
    "termination_date": null,
    "network": {
      "network_id": "BROAD-NATIONAL",
      "network_name": "National Broad Network",
      "network_type": "broad",
      "provider_count": 850000,
      "hospital_count": 5500
    },
    "eligibility": {
      "pcp_required": false,
      "referral_required": false,
      "waiting_period_days": 0,
      "pre_existing_waiting_period": 0
    },
    "cost_sharing": {
      "in_network": {
        "individual_deductible": 500,
        "family_deductible": 1000,
        "individual_oop_max": 4000,
        "family_oop_max": 8000,
        "coinsurance_percent": 20,
        "deductible_applies_to_copays": false
      },
      "out_of_network": {
        "individual_deductible": 1500,
        "family_deductible": 3000,
        "individual_oop_max": 8000,
        "family_oop_max": 16000,
        "coinsurance_percent": 40,
        "reimbursement_basis": "UCR_80"
      }
    },
    "copays": {
      "pcp_visit": 25,
      "specialist_visit": 50,
      "urgent_care": 75,
      "emergency_room": 150,
      "telehealth": 0,
      "mental_health_outpatient": 25,
      "physical_therapy": 40,
      "lab_work": 0,
      "xray": 0,
      "advanced_imaging": null
    },
    "hospital": {
      "inpatient_copay_per_day": null,
      "inpatient_copay_per_admission": 250,
      "inpatient_coinsurance": 20,
      "inpatient_day_limit": null,
      "outpatient_surgery_copay": 200,
      "ambulance_copay": 150
    },
    "pharmacy": {
      "separate_deductible": false,
      "deductible_amount": 0,
      "retail_30_day": {
        "tier_1_generic": 10,
        "tier_2_preferred_brand": 35,
        "tier_3_non_preferred": 60,
        "tier_4_specialty_coinsurance": 25
      },
      "mail_90_day": {
        "tier_1_generic": 25,
        "tier_2_preferred_brand": 87.50,
        "tier_3_non_preferred": 150
      },
      "specialty_copay_max": 250
    },
    "preventive": {
      "covered_at_100": true,
      "deductible_exempt": true,
      "services_included": [
        "Annual physical exam",
        "Well-child visits",
        "Immunizations",
        "Cancer screenings",
        "Prenatal care"
      ]
    },
    "exclusions": [
      "Cosmetic surgery",
      "Experimental treatments",
      "Long-term custodial care",
      "Services outside of service area except emergency"
    ],
    "prior_auth_required": [
      "Inpatient admissions (elective)",
      "Advanced imaging (MRI, CT, PET)",
      "Specialty medications",
      "Outpatient surgery",
      "DME over $500"
    ],
    "premium": {
      "employee_only": {
        "total": 650,
        "employer_contribution": 520,
        "employee_contribution": 130
      },
      "employee_spouse": {
        "total": 1300,
        "employer_contribution": 910,
        "employee_contribution": 390
      },
      "employee_children": {
        "total": 1100,
        "employer_contribution": 770,
        "employee_contribution": 330
      },
      "family": {
        "total": 1750,
        "employer_contribution": 1225,
        "employee_contribution": 525
      }
    }
  }
}
```

### Example 2: HDHP with HSA

**Request:** "Generate an HDHP plan with HSA"

```json
{
  "plan": {
    "plan_code": "HDHP-HSA-2025",
    "plan_name": "HDHP with Health Savings Account",
    "plan_type": "HDHP",
    "hsa_eligible": true,
    "effective_date": "2025-01-01",
    "eligibility": {
      "pcp_required": false,
      "referral_required": false
    },
    "cost_sharing": {
      "in_network": {
        "individual_deductible": 1600,
        "family_deductible": 3200,
        "individual_oop_max": 7050,
        "family_oop_max": 14100,
        "coinsurance_percent": 20,
        "deductible_applies_to_all_non_preventive": true
      },
      "out_of_network": {
        "individual_deductible": 3200,
        "family_deductible": 6400,
        "individual_oop_max": 14100,
        "family_oop_max": 28200,
        "coinsurance_percent": 40
      }
    },
    "hsa": {
      "employer_seed_individual": 500,
      "employer_seed_family": 1000,
      "contribution_limit_individual": 4150,
      "contribution_limit_family": 8300,
      "catch_up_55_plus": 1000,
      "eligible_expenses": [
        "Medical care",
        "Prescription drugs",
        "Dental care",
        "Vision care",
        "COBRA premiums",
        "Long-term care premiums"
      ]
    },
    "pharmacy": {
      "deductible_applies": true,
      "preventive_drugs_exempt": true,
      "after_deductible": {
        "tier_1_generic": 10,
        "tier_2_preferred_brand": 35,
        "tier_3_non_preferred": 60,
        "tier_4_specialty_coinsurance": 25
      }
    },
    "preventive": {
      "covered_at_100": true,
      "deductible_exempt": true,
      "preventive_drug_list": [
        "Statins",
        "ACE inhibitors",
        "Blood pressure medications",
        "Diabetes medications",
        "Contraceptives"
      ]
    },
    "premium": {
      "employee_only": {
        "total": 450,
        "employer_contribution": 400,
        "employee_contribution": 50
      },
      "family": {
        "total": 1200,
        "employer_contribution": 1000,
        "employee_contribution": 200
      }
    }
  }
}
```

### Example 3: HMO Plan

**Request:** "Generate an HMO plan"

```json
{
  "plan": {
    "plan_code": "HMO-STANDARD-2025",
    "plan_name": "HMO Standard Plan",
    "plan_type": "HMO",
    "effective_date": "2025-01-01",
    "network": {
      "network_id": "HMO-REGIONAL",
      "network_name": "Regional HMO Network",
      "service_area": ["IL", "IN", "WI"],
      "provider_count": 25000,
      "hospital_count": 150
    },
    "eligibility": {
      "pcp_required": true,
      "pcp_selection_required_within_days": 30,
      "referral_required": true,
      "referral_valid_days": 90
    },
    "cost_sharing": {
      "in_network": {
        "individual_deductible": 0,
        "family_deductible": 0,
        "individual_oop_max": 3000,
        "family_oop_max": 6000
      },
      "out_of_network": {
        "covered": false,
        "exceptions": ["Emergency services", "Dialysis when traveling"]
      }
    },
    "copays": {
      "pcp_visit": 20,
      "specialist_visit": 40,
      "urgent_care": 50,
      "emergency_room": 150,
      "telehealth": 0,
      "mental_health_outpatient": 20,
      "physical_therapy": 40,
      "lab_work": 0,
      "xray": 0,
      "advanced_imaging": 100
    },
    "hospital": {
      "inpatient_copay_per_admission": 250,
      "outpatient_surgery_copay": 150,
      "ambulance_copay": 100
    },
    "premium": {
      "employee_only": {
        "total": 500,
        "employer_contribution": 425,
        "employee_contribution": 75
      },
      "family": {
        "total": 1350,
        "employer_contribution": 1080,
        "employee_contribution": 270
      }
    }
  }
}
```

## Plan Comparison Table

**Request:** "Compare available plan options"

```json
{
  "plan_comparison": {
    "plan_year": 2025,
    "plans": [
      {
        "plan_code": "HMO-STD",
        "plan_type": "HMO",
        "deductible_individual": 0,
        "deductible_family": 0,
        "oop_max_individual": 3000,
        "oop_max_family": 6000,
        "pcp_copay": 20,
        "specialist_copay": 40,
        "er_copay": 150,
        "premium_employee_only": 75,
        "premium_family": 270,
        "pcp_required": true,
        "oon_coverage": false
      },
      {
        "plan_code": "PPO-GOLD",
        "plan_type": "PPO",
        "deductible_individual": 500,
        "deductible_family": 1000,
        "oop_max_individual": 4000,
        "oop_max_family": 8000,
        "pcp_copay": 25,
        "specialist_copay": 50,
        "er_copay": 150,
        "coinsurance": 20,
        "premium_employee_only": 130,
        "premium_family": 525,
        "pcp_required": false,
        "oon_coverage": true
      },
      {
        "plan_code": "HDHP-HSA",
        "plan_type": "HDHP",
        "deductible_individual": 1600,
        "deductible_family": 3200,
        "oop_max_individual": 7050,
        "oop_max_family": 14100,
        "coinsurance": 20,
        "premium_employee_only": 50,
        "premium_family": 200,
        "pcp_required": false,
        "oon_coverage": true,
        "hsa_eligible": true,
        "employer_hsa_contribution": 500
      }
    ]
  }
}
```

## Validation Rules

1. **HDHP Compliance**: Deductibles must meet IRS minimums, OOP max cannot exceed IRS limits
2. **ACA Compliance**: Essential health benefits must be covered, no annual/lifetime limits on EHB
3. **Parity Requirements**: Mental health benefits must be equal to medical benefits
4. **Network Adequacy**: Sufficient providers in specialty and geography
5. **Cost Sharing Limits**: OOP max cannot exceed federal limits
6. **Preventive Care**: ACA-compliant plans must cover preventive at 100% in-network

## Related Skills

### MemberSim
- [SKILL.md](SKILL.md) - MemberSim overview
- [enrollment-eligibility.md](enrollment-eligibility.md) - Enrollment with plan selection
- [accumulator-tracking.md](accumulator-tracking.md) - Tracking against plan limits
- [professional-claims.md](professional-claims.md) - Claims adjudication using plan benefits
- [prior-authorization.md](prior-authorization.md) - PA requirements by plan

### Cross-Product: RxMemberSim
- [../rxmembersim/formulary-management.md](../rxmembersim/formulary-management.md) - Pharmacy benefit tiers, formulary structure
- [../rxmembersim/rx-accumulator.md](../rxmembersim/rx-accumulator.md) - Pharmacy deductible/OOP tracking

> **Integration Pattern:** Medical and pharmacy benefits are often separate but coordinated. Use MemberSim for medical plan design. Use RxMemberSim for pharmacy benefit design. Many plans have combined medical+Rx deductibles and OOP maximums - ensure consistency.

### References
- [../../formats/csv.md](../../formats/csv.md) - CSV export for plans
- [../../formats/sql.md](../../formats/sql.md) - SQL schema for plans
- [../../references/code-systems.md](../../references/code-systems.md) - Code systems
