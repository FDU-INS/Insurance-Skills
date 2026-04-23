---
name: accumulator-tracking
description: "Member benefit accumulators including deductibles, out-of-pocket maximums, and cost-sharing tracking. Triggers: deductible, out-of-pocket, OOP, accumulator, cost-sharing, MOOP, coinsurance, member responsibility, year-to-date"
---

# Accumulator Tracking Cohort

A cohort template for generating member benefit accumulators including deductibles, out-of-pocket maximums, and cost-sharing tracking.

## For Claude

Use this skill when the user requests accumulator or cost-sharing cohorts. This teaches you how to generate **realistic accumulator states** across plan years with proper application to claims.

**When to apply this skill:**

- User mentions deductible, out-of-pocket, or OOP
- User requests accumulator or cost-sharing cohorts
- User specifies MOOP, coinsurance, or member responsibility
- User asks for year-to-date benefit tracking
- User needs accumulator application examples

**Key capabilities this skill provides:**

- How to structure individual vs family accumulators
- How to apply deductibles and coinsurance to claims
- How to track embedded vs aggregate family limits
- How to model mid-year accumulator states
- How to handle in-network vs out-of-network accumulators

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: MemberSim
- **Tags**: accumulators, deductible, oop, cost-sharing, payer
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic member benefit accumulator states. It models deductible and OOP tracking across a plan year, proper application to claims, and the interaction between individual and family limits.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "accumulator", "deductible", "out of pocket"
- "OOP", "MOOP", "max out of pocket"
- "cost sharing", "coinsurance"
- "member responsibility", "YTD"

**Accumulator Cohorts**:

- "Generate a member with partially met deductible"
- "Create an accumulator state near OOP max"
- "Generate a family accumulator example"

## Trigger Phrases

- accumulator
- deductible
- out of pocket
- OOP
- OOP max
- cost sharing
- coinsurance
- member responsibility
- year to date
- YTD
- max out of pocket
- MOOP

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| plan_type | string | PPO | HMO, PPO, EPO, HDHP |
| coverage_tier | string | individual | individual, individual_plus_one, family |
| accumulator_status | string | partial | not_met, partial, met |
| plan_year | int | current | Any valid year |

## Accumulator Types

### Standard Accumulators
| Accumulator | Description | Typical Limits |
|-------------|-------------|----------------|
| Deductible (Individual) | Per-person annual deductible | $250 - $5,000 |
| Deductible (Family) | Combined family deductible | $500 - $15,000 |
| OOP Max (Individual) | Per-person annual OOP limit | $3,000 - $9,450 |
| OOP Max (Family) | Combined family OOP limit | $6,000 - $18,900 |

### ACA Maximum Limits (2025)
| Tier | Individual OOP Max | Family OOP Max |
|------|-------------------|----------------|
| In-Network | $9,450 | $18,900 |
| Out-of-Network | No limit | No limit |

## Accumulator Structure

### Individual Accumulator
```json
{
  "accumulator_id": "ACC{member_id}{plan_year}",
  "member_id": "MEM001234",
  "plan_year": 2025,
  "tier": "individual",

  "deductible": {
    "in_network": {
      "applied": 350.00,
      "limit": 500.00,
      "remaining": 150.00,
      "met": false
    },
    "out_of_network": {
      "applied": 0.00,
      "limit": 1000.00,
      "remaining": 1000.00,
      "met": false
    }
  },

  "out_of_pocket": {
    "in_network": {
      "applied": 650.00,
      "limit": 3000.00,
      "remaining": 2350.00,
      "met": false
    },
    "out_of_network": {
      "applied": 0.00,
      "limit": 6000.00,
      "remaining": 6000.00,
      "met": false
    }
  },

  "last_updated": "2025-01-15T14:30:00Z"
}
```

### Family Accumulator
```json
{
  "accumulator_id": "ACC{subscriber_id}{plan_year}F",
  "subscriber_id": "MEM001234",
  "plan_year": 2025,
  "tier": "family",

  "embedded_individual_limits": true,
  "individual_deductible_limit": 500.00,
  "individual_oop_limit": 3000.00,

  "family_deductible": {
    "in_network": {
      "applied": 800.00,
      "limit": 1500.00,
      "remaining": 700.00,
      "met": false
    }
  },

  "family_oop": {
    "in_network": {
      "applied": 1200.00,
      "limit": 6000.00,
      "remaining": 4800.00,
      "met": false
    }
  },

  "member_contributions": [
    { "member_id": "MEM001234", "deductible": 350.00, "oop": 650.00 },
    { "member_id": "MEM001235", "deductible": 300.00, "oop": 400.00 },
    { "member_id": "MEM001236", "deductible": 150.00, "oop": 150.00 }
  ]
}
```

## Plan Configurations

### PPO Standard
```json
{
  "plan_code": "PPO-STANDARD",
  "plan_type": "PPO",
  "deductible_individual": 500.00,
  "deductible_family": 1500.00,
  "oop_max_individual": 3000.00,
  "oop_max_family": 6000.00,
  "copay_pcp": 25.00,
  "copay_specialist": 50.00,
  "copay_er": 250.00,
  "coinsurance_in_network": 0.20,
  "coinsurance_out_of_network": 0.40,
  "deductible_applies_to_copay": false
}
```

### HDHP with HSA
```json
{
  "plan_code": "HDHP-HSA",
  "plan_type": "HDHP",
  "deductible_individual": 1600.00,
  "deductible_family": 3200.00,
  "oop_max_individual": 4150.00,
  "oop_max_family": 8300.00,
  "copay_pcp": 0.00,
  "coinsurance_in_network": 0.20,
  "deductible_applies_to_copay": true,
  "hsa_eligible": true,
  "notes": "Deductible must be met before any coverage except preventive"
}
```

### HMO
```json
{
  "plan_code": "HMO-VALUE",
  "plan_type": "HMO",
  "deductible_individual": 0.00,
  "deductible_family": 0.00,
  "oop_max_individual": 4000.00,
  "oop_max_family": 8000.00,
  "copay_pcp": 20.00,
  "copay_specialist": 40.00,
  "copay_er": 150.00,
  "coinsurance_in_network": 0.00,
  "requires_pcp": true,
  "requires_referral": true
}
```

## Cost Sharing Calculation

### Calculation Order
```
1. Determine allowed amount (fee schedule)
2. Check if deductible applies to service type
3. Apply deductible (if not met)
4. Apply copay (fixed) OR coinsurance (percentage)
5. Check OOP maximum
6. Calculate plan payment vs member responsibility
7. Update accumulators
```

### Example Calculation
```json
{
  "claim": {
    "procedure_code": "99214",
    "charge_amount": 175.00,
    "allowed_amount": 125.00
  },

  "accumulator_before": {
    "deductible_applied": 300.00,
    "deductible_limit": 500.00,
    "oop_applied": 500.00,
    "oop_limit": 3000.00
  },

  "calculation": {
    "step_1": "Allowed amount = $125.00",
    "step_2": "Deductible remaining = $500 - $300 = $200",
    "step_3": "Deductible applied to this claim = $125.00",
    "step_4": "After deductible = $0.00",
    "step_5": "Member responsibility = $125.00 (deductible)",
    "step_6": "Plan payment = $0.00"
  },

  "accumulator_after": {
    "deductible_applied": 425.00,
    "deductible_limit": 500.00,
    "oop_applied": 625.00,
    "oop_limit": 3000.00
  },

  "adjudication": {
    "allowed_amount": 125.00,
    "deductible": 125.00,
    "copay": 0.00,
    "coinsurance": 0.00,
    "paid_amount": 0.00,
    "patient_responsibility": 125.00
  }
}
```

### OOP Max Calculation
```json
{
  "claim": {
    "allowed_amount": 500.00
  },

  "accumulator_before": {
    "deductible_met": true,
    "oop_applied": 2900.00,
    "oop_limit": 3000.00
  },

  "calculation": {
    "step_1": "Deductible met, apply coinsurance",
    "step_2": "Coinsurance (20%) = $100.00",
    "step_3": "OOP remaining = $3000 - $2900 = $100.00",
    "step_4": "Member coinsurance capped at $100.00",
    "step_5": "OOP MAX NOW MET"
  },

  "accumulator_after": {
    "deductible_met": true,
    "oop_applied": 3000.00,
    "oop_limit": 3000.00,
    "oop_met": true
  },

  "adjudication": {
    "allowed_amount": 500.00,
    "deductible": 0.00,
    "coinsurance": 100.00,
    "paid_amount": 400.00,
    "patient_responsibility": 100.00,
    "notes": "OOP maximum met. Future claims covered at 100%."
  }
}
```

## Accumulator Cross-Reference

### What Counts Toward Deductible
| Service | Counts? | Notes |
|---------|---------|-------|
| Office visit (copay plan) | No | Copay applies instead |
| Office visit (HDHP) | Yes | Deductible first |
| Specialist visit | Varies | Plan-specific |
| Lab/X-ray | Usually | After deductible |
| Hospital inpatient | Yes | Deductible + coinsurance |
| Emergency room | Varies | Some have ER copay |
| Preventive care | No | $0 per ACA |
| Prescription drugs | Varies | Separate Rx deductible |

### What Counts Toward OOP Max
| Item | Counts? |
|------|---------|
| Deductible | Yes |
| Copays | Yes |
| Coinsurance | Yes |
| Premiums | No |
| Balance billing (OON) | No |
| Non-covered services | No |
| Amounts over allowed | No |

## Examples

### Example 1: Mid-Year Accumulator Status

```json
{
  "member": {
    "member_id": "MEM001234",
    "name": { "given_name": "Jennifer", "family_name": "Williams" },
    "plan_code": "PPO-GOLD"
  },
  "plan": {
    "plan_type": "PPO",
    "deductible_individual": 500.00,
    "oop_max_individual": 3000.00,
    "copay_pcp": 25.00,
    "copay_specialist": 50.00,
    "coinsurance": 0.20
  },
  "accumulator": {
    "plan_year": 2025,
    "as_of_date": "2025-06-15",
    "deductible": {
      "applied": 500.00,
      "limit": 500.00,
      "met": true,
      "met_date": "2025-03-22"
    },
    "out_of_pocket": {
      "applied": 1450.00,
      "limit": 3000.00,
      "remaining": 1550.00,
      "met": false,
      "projected_met_date": null
    },
    "claims_ytd": 12,
    "total_charges_ytd": 8500.00,
    "total_allowed_ytd": 5200.00,
    "total_paid_by_plan": 3750.00,
    "total_member_responsibility": 1450.00
  }
}
```

### Example 2: Family Accumulator with Multiple Members

```json
{
  "family": {
    "subscriber_id": "MEM001234",
    "subscriber_name": "Robert Johnson",
    "plan_code": "PPO-FAMILY",
    "coverage_tier": "family"
  },
  "plan": {
    "deductible_individual": 500.00,
    "deductible_family": 1500.00,
    "oop_max_individual": 3500.00,
    "oop_max_family": 7000.00,
    "embedded_limits": true
  },
  "family_accumulator": {
    "plan_year": 2025,
    "as_of_date": "2025-07-01",
    "family_deductible": {
      "applied": 1100.00,
      "limit": 1500.00,
      "met": false
    },
    "family_oop": {
      "applied": 2200.00,
      "limit": 7000.00,
      "met": false
    }
  },
  "member_accumulators": [
    {
      "member_id": "MEM001234",
      "relationship": "subscriber",
      "name": "Robert Johnson",
      "individual_deductible": { "applied": 500.00, "limit": 500.00, "met": true },
      "individual_oop": { "applied": 1200.00, "limit": 3500.00, "met": false }
    },
    {
      "member_id": "MEM001235",
      "relationship": "spouse",
      "name": "Mary Johnson",
      "individual_deductible": { "applied": 400.00, "limit": 500.00, "met": false },
      "individual_oop": { "applied": 700.00, "limit": 3500.00, "met": false }
    },
    {
      "member_id": "MEM001236",
      "relationship": "child",
      "name": "Emily Johnson",
      "individual_deductible": { "applied": 200.00, "limit": 500.00, "met": false },
      "individual_oop": { "applied": 300.00, "limit": 3500.00, "met": false }
    }
  ]
}
```

### Example 3: HDHP Accumulator with HSA

```json
{
  "member": {
    "member_id": "MEM009999",
    "name": { "given_name": "Thomas", "family_name": "Anderson" },
    "plan_code": "HDHP-HSA-INDIVIDUAL"
  },
  "plan": {
    "plan_type": "HDHP",
    "hsa_eligible": true,
    "deductible_individual": 1600.00,
    "oop_max_individual": 4150.00,
    "coinsurance": 0.20,
    "deductible_applies_to_all_services": true
  },
  "accumulator": {
    "plan_year": 2025,
    "as_of_date": "2025-04-15",
    "deductible": {
      "applied": 800.00,
      "limit": 1600.00,
      "remaining": 800.00,
      "met": false
    },
    "out_of_pocket": {
      "applied": 800.00,
      "limit": 4150.00,
      "remaining": 3350.00,
      "met": false
    }
  },
  "hsa_account": {
    "balance": 2500.00,
    "ytd_contributions": 1200.00,
    "ytd_distributions": 700.00,
    "contribution_limit_2025": 4150.00,
    "remaining_contribution_room": 2950.00
  },
  "notes": "All services except preventive require deductible to be met first. Preventive care covered at 100%."
}
```

### Example 4: Claim Processing with Accumulator Update

```json
{
  "claim": {
    "claim_id": "CLM20250715000001",
    "service_date": "2025-07-15",
    "procedure_code": "99214",
    "charge_amount": 175.00
  },
  "accumulator_snapshot_before": {
    "deductible_applied": 400.00,
    "deductible_limit": 500.00,
    "oop_applied": 600.00,
    "oop_limit": 3000.00
  },
  "adjudication": {
    "allowed_amount": 125.00,
    "contractual_adjustment": 50.00,
    "deductible_applied_this_claim": 100.00,
    "copay": 25.00,
    "coinsurance": 0.00,
    "paid_amount": 0.00,
    "patient_responsibility": 125.00,
    "breakdown": {
      "deductible_portion": 100.00,
      "copay_portion": 25.00,
      "coinsurance_portion": 0.00
    }
  },
  "accumulator_snapshot_after": {
    "deductible_applied": 500.00,
    "deductible_limit": 500.00,
    "deductible_met": true,
    "deductible_met_date": "2025-07-15",
    "oop_applied": 725.00,
    "oop_limit": 3000.00
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Deductible amount | Non-negative | $1500 individual |
| OOP maximum | ≥ deductible | $6000 individual |
| Accumulator YTD | 0 to maximum | $2500 of $6000 OOP |
| Plan year | Valid date range | 2025-01-01 to 2025-12-31 |
| Tier | individual, family | "family" |
| Network | in-network, out-of-network | "in-network" |
| Service category | medical, pharmacy, combined | "medical" |
| Reset date | Plan year start | 2025-01-01 |

### Business Rules

- **Deductible Phase**: Member pays 100% until deductible met (up to allowed amount)
- **Coinsurance Phase**: Member pays coinsurance % after deductible
- **OOP Maximum**: Member pays $0 for covered services after OOP max reached
- **Family vs Individual**: Family may have embedded individual limits
- **In-Network vs OON**: Separate accumulators for each network tier
- **Excluded Services**: Some services don't count toward accumulators
- **Annual Reset**: Accumulators reset to $0 on plan year start date
- **Mid-Year Changes**: Job change may reset or transfer accumulators

## Related Skills

### MemberSim
- [SKILL.md](SKILL.md) - MemberSim overview
- [professional-claims.md](professional-claims.md) - Claim adjudication
- [facility-claims.md](facility-claims.md) - Hospital cost sharing
- [plan-benefits.md](plan-benefits.md) - Plan deductible/OOP limits

### Cross-Product: RxMemberSim
- [../rxmembersim/rx-accumulator.md](../rxmembersim/rx-accumulator.md) - Pharmacy accumulator tracking

> **Integration Pattern:** Many plans have integrated medical+Rx accumulators. When a member's medical deductible is met, pharmacy claims may also process differently. Use MemberSim for medical accumulators, RxMemberSim for pharmacy. For integrated plans, ensure accumulator totals are synchronized.

### References
- [../../references/data-models.md](../../references/data-models.md) - Accumulator schema
