---
name: rx-accumulator
description: "Pharmacy benefit accumulators including deductibles, OOP maximums, and Medicare Part D phases. Triggers: pharmacy accumulator, deductible, OOP maximum, Part D, coverage gap, donut hole, catastrophic phase, TrOOP"
---

# Pharmacy Accumulator Tracking Cohort

A cohort template for generating pharmacy benefit accumulators including deductibles, OOP maximums, and Medicare Part D phases.

## For Claude

Use this skill when the user requests pharmacy accumulator or Part D phase cohorts. This teaches you how to generate **realistic pharmacy cost-sharing** with TrOOP tracking, coverage gap, and catastrophic phase modeling.

**When to apply this skill:**

- User mentions rx accumulator or pharmacy deductible
- User requests Part D phase or donut hole cohorts
- User specifies TrOOP or true out of pocket
- User asks for pharmacy cost sharing examples
- User needs catastrophic coverage cohorts

**Key capabilities this skill provides:**

- How to structure pharmacy accumulators by plan type
- How to model Medicare Part D benefit phases
- How to track TrOOP and coverage gap entry
- How to handle specialty tier maximums
- How to generate DAW and brand penalty cohorts

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: RxMemberSim
- **Tags**: pharmacy, accumulator, Part-D, TrOOP, cost-sharing
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic pharmacy accumulator tracking. It models commercial pharmacy deductibles, Medicare Part D phases, and specialty tier maximums with proper cost-sharing calculations.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "rx accumulator", "pharmacy deductible"
- "rx out of pocket", "TrOOP"
- "Part D phase", "donut hole"
- "coverage gap", "catastrophic"

**Accumulator Cohorts**:

- "Generate a pharmacy accumulator state"
- "Create a Part D coverage gap cohort"
- "Generate a member in catastrophic phase"

## Trigger Phrases

- rx accumulator
- pharmacy accumulator
- rx deductible
- pharmacy deductible
- rx out of pocket
- rx OOP
- rx OOP max
- pharmacy cost sharing
- TrOOP
- true out of pocket
- Part D phase
- donut hole
- coverage gap
- catastrophic
- specialty max
- DAW penalty
- brand penalty

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| plan_type | string | commercial | commercial, medicare_d, hdhp |
| accumulator_status | string | partial | not_met, partial, met |
| plan_year | int | current | Any valid year |
| part_d_phase | string | icl | deductible, icl, coverage_gap, catastrophic |

## Accumulator Types

### Commercial Pharmacy Accumulators

| Accumulator | Description | Typical Limits |
|-------------|-------------|----------------|
| Rx Deductible (Individual) | Pharmacy-only deductible | $0 - $500 |
| Rx Deductible (Family) | Combined family Rx deductible | $0 - $1,000 |
| Rx OOP Max (Individual) | Pharmacy-only OOP limit | $1,000 - $4,000 |
| Rx OOP Max (Family) | Combined family Rx OOP limit | $2,000 - $8,000 |
| Specialty OOP Max | Per-fill specialty maximum | $100 - $500 |
| DAW/Brand Penalty | Accumulated brand penalties | No limit |

### Medicare Part D Accumulators (2025)

| Accumulator | Threshold | Description |
|-------------|-----------|-------------|
| Deductible Phase | $0 - $590 | Member pays 100% |
| Initial Coverage Limit | $590 - $5,030 | Standard copays apply |
| Coverage Gap (Donut Hole) | $5,030 - $8,000 | 25% coinsurance |
| Catastrophic Phase | >$8,000 TrOOP | $0 copay (IRA 2025) |

### True Out-of-Pocket (TrOOP) Components
Amounts that count toward TrOOP:
- Member deductible payments
- Member copays and coinsurance
- 70% of brand discount in coverage gap

Amounts that do NOT count toward TrOOP:
- Plan payments
- Low-Income Subsidy payments
- Manufacturer discount portion (30%)

## Accumulator Structure

### Commercial RxAccumulator
```json
{
  "member_id": "MEM001234567",
  "rx_plan_code": "RX-COMMERCIAL-3TIER",
  "plan_year": 2025,
  "as_of_date": "2025-06-15",

  "rx_deductible": {
    "individual": {
      "limit": 250.00,
      "applied": 250.00,
      "remaining": 0.00,
      "met": true,
      "met_date": "2025-02-15"
    },
    "family": {
      "limit": 500.00,
      "applied": 425.00,
      "remaining": 75.00,
      "met": false
    }
  },

  "rx_oop_max": {
    "individual": {
      "limit": 2500.00,
      "applied": 875.00,
      "remaining": 1625.00,
      "met": false
    },
    "family": {
      "limit": 5000.00,
      "applied": 1450.00,
      "remaining": 3550.00,
      "met": false
    }
  },

  "specialty_oop": {
    "per_fill_max": 250.00,
    "ytd_specialty_paid": 750.00,
    "fills_count": 3
  },

  "daw_brand_penalty": {
    "ytd_penalty_amount": 45.00,
    "penalty_claims_count": 3
  },

  "combined_with_medical": false,
  "last_updated": "2025-06-15T14:30:00Z"
}
```

### Medicare Part D RxAccumulator
```json
{
  "member_id": "MBI1234567890",
  "rx_plan_code": "RX-PARTD-STD",
  "plan_year": 2025,
  "as_of_date": "2025-09-15",

  "current_phase": "coverage_gap",
  "phase_details": {
    "deductible": {
      "limit": 590.00,
      "applied": 590.00,
      "met": true,
      "met_date": "2025-02-28"
    },
    "initial_coverage": {
      "limit": 5030.00,
      "gross_drug_cost": 5030.00,
      "passed_date": "2025-08-15"
    },
    "coverage_gap": {
      "gross_drug_cost_in_gap": 1250.00,
      "member_cost_in_gap": 312.50
    },
    "catastrophic": {
      "threshold": 8000.00,
      "troop_applied": 6125.00,
      "troop_remaining": 1875.00,
      "projected_entry_date": "2025-11-01"
    }
  },

  "troop": {
    "limit": 8000.00,
    "applied": 6125.00,
    "remaining": 1875.00,
    "met": false,
    "components": {
      "deductible_payments": 590.00,
      "copay_payments": 1850.00,
      "coinsurance_payments": 1560.00,
      "coverage_gap_brand_discount_70pct": 2125.00
    }
  },

  "gross_drug_cost_ytd": 12500.00,
  "low_income_subsidy": {
    "lis_level": null,
    "lis_copay_amount": null
  },

  "last_updated": "2025-09-15T10:30:00Z"
}
```

### HDHP Pharmacy Accumulator
```json
{
  "member_id": "MEM001234567",
  "rx_plan_code": "RX-HDHP-HSA",
  "plan_year": 2025,
  "as_of_date": "2025-06-15",

  "combined_deductible": {
    "individual": {
      "limit": 1600.00,
      "medical_applied": 850.00,
      "pharmacy_applied": 320.00,
      "total_applied": 1170.00,
      "remaining": 430.00,
      "met": false
    },
    "family": {
      "limit": 3200.00,
      "total_applied": 2100.00,
      "remaining": 1100.00,
      "met": false
    }
  },

  "combined_oop_max": {
    "individual": {
      "limit": 7000.00,
      "medical_applied": 1200.00,
      "pharmacy_applied": 450.00,
      "total_applied": 1650.00,
      "remaining": 5350.00,
      "met": false
    }
  },

  "preventive_rx_exemption": {
    "preventive_drugs_no_deductible": true,
    "preventive_rx_paid": 125.00
  },

  "hsa": {
    "contributions_ytd": 2500.00,
    "distributions_ytd": 1850.00,
    "balance": 3200.00
  },

  "last_updated": "2025-06-15T14:30:00Z"
}
```

## Accumulator Application Rules

### Claim Processing Order
```
1. Check member eligibility and coverage
   ↓
2. Retrieve current accumulators
   ↓
3. Apply deductible (if applicable)
   ↓
4. Calculate copay/coinsurance based on post-deductible rules
   ↓
5. Apply OOP max cap (if member has met OOP max)
   ↓
6. Apply specialty max (if applicable)
   ↓
7. Add DAW penalty (if brand requested when generic available)
   ↓
8. Return member cost and update accumulators
```

### Deductible Application
```json
{
  "deductible_applies_to": {
    "generic": false,
    "preferred_brand": true,
    "non_preferred_brand": true,
    "specialty": true
  },
  "preventive_exempt": true,
  "example_claim": {
    "drug": "Atorvastatin 40mg (Generic)",
    "tier": 1,
    "deductible_applies": false,
    "member_cost": 10.00
  }
}
```

### Medicare Part D Phase Transitions
```json
{
  "phase_transition_example": {
    "claim_date": "2025-08-15",
    "drug_name": "Eliquis 5mg",
    "gross_drug_cost": 650.00,
    "pre_claim_phase": "initial_coverage",
    "pre_claim_gross_ytd": 4650.00,
    "post_claim_gross_ytd": 5300.00,
    "post_claim_phase": "coverage_gap",
    "claim_split": {
      "initial_coverage_portion": 380.00,
      "coverage_gap_portion": 270.00
    },
    "member_cost_calculation": {
      "icl_copay": 47.00,
      "gap_25_percent": 67.50,
      "total_member_cost": 114.50
    }
  }
}
```

## Examples

### Example 1: Commercial Accumulator Status

**Request:** "Generate pharmacy accumulators for a family with partial deductible met"

```json
{
  "accumulator_summary": {
    "member_id": "MEM001234567",
    "subscriber_id": "MEM001234567",
    "rx_plan_code": "RX-COMMERCIAL-3TIER",
    "plan_year": 2025,
    "as_of_date": "2025-06-15",
    "family_members": [
      {
        "member_id": "MEM001234567",
        "name": "Michael Johnson",
        "relationship": "subscriber",
        "person_code": "01"
      },
      {
        "member_id": "MEM001234568",
        "name": "Sarah Johnson",
        "relationship": "spouse",
        "person_code": "02"
      },
      {
        "member_id": "MEM001234569",
        "name": "Emma Johnson",
        "relationship": "child",
        "person_code": "03"
      }
    ]
  },
  "individual_accumulators": [
    {
      "member_id": "MEM001234567",
      "rx_deductible": {
        "limit": 250.00,
        "applied": 250.00,
        "remaining": 0.00,
        "met": true,
        "met_date": "2025-02-15"
      },
      "rx_oop_max": {
        "limit": 2500.00,
        "applied": 575.00,
        "remaining": 1925.00,
        "met": false
      }
    },
    {
      "member_id": "MEM001234568",
      "rx_deductible": {
        "limit": 250.00,
        "applied": 125.00,
        "remaining": 125.00,
        "met": false
      },
      "rx_oop_max": {
        "limit": 2500.00,
        "applied": 225.00,
        "remaining": 2275.00,
        "met": false
      }
    },
    {
      "member_id": "MEM001234569",
      "rx_deductible": {
        "limit": 250.00,
        "applied": 50.00,
        "remaining": 200.00,
        "met": false
      },
      "rx_oop_max": {
        "limit": 2500.00,
        "applied": 85.00,
        "remaining": 2415.00,
        "met": false
      }
    }
  ],
  "family_accumulators": {
    "rx_deductible": {
      "limit": 500.00,
      "applied": 425.00,
      "remaining": 75.00,
      "met": false
    },
    "rx_oop_max": {
      "limit": 5000.00,
      "applied": 885.00,
      "remaining": 4115.00,
      "met": false
    }
  },
  "ytd_claims_summary": {
    "total_claims": 15,
    "total_gross_cost": 2450.00,
    "total_plan_paid": 1565.00,
    "total_member_paid": 885.00,
    "claims_by_member": [
      { "member_id": "MEM001234567", "claims": 8, "member_paid": 575.00 },
      { "member_id": "MEM001234568", "claims": 5, "member_paid": 225.00 },
      { "member_id": "MEM001234569", "claims": 2, "member_paid": 85.00 }
    ]
  }
}
```

### Example 2: Medicare Part D Accumulator in Coverage Gap

**Request:** "Generate a Medicare Part D accumulator in the coverage gap phase"

```json
{
  "accumulator_summary": {
    "member_id": "MBI1234567890",
    "medicare_beneficiary_id": "1EG4-TE5-MK72",
    "rx_plan_code": "RX-PARTD-STD",
    "plan_year": 2025,
    "as_of_date": "2025-09-15"
  },
  "part_d_phases": {
    "current_phase": "coverage_gap",
    "deductible": {
      "threshold": 590.00,
      "applied": 590.00,
      "status": "met",
      "met_date": "2025-02-28"
    },
    "initial_coverage": {
      "start": 590.00,
      "end": 5030.00,
      "gross_drug_cost_at_end": 5030.00,
      "passed_date": "2025-08-15"
    },
    "coverage_gap": {
      "start": 5030.00,
      "end": "until TrOOP reaches $8,000",
      "current_gross_drug_cost": 6280.00,
      "member_responsibility": "25% coinsurance",
      "manufacturer_discount": "Not applicable under IRA 2025"
    },
    "catastrophic": {
      "threshold": 8000.00,
      "projected_entry": "2025-11-01",
      "member_cost_after_entry": "$0 (IRA 2025)"
    }
  },
  "troop_accumulator": {
    "limit": 8000.00,
    "applied": 6125.00,
    "remaining": 1875.00,
    "met": false,
    "components_ytd": {
      "deductible_payments": 590.00,
      "icl_copays_coinsurance": 2850.00,
      "coverage_gap_payments": 685.00,
      "manufacturer_discount_70pct": 2000.00
    }
  },
  "gross_drug_cost_ytd": {
    "total": 12850.00,
    "by_phase": {
      "deductible": 590.00,
      "initial_coverage": 4440.00,
      "coverage_gap": 7820.00
    }
  },
  "low_income_subsidy": {
    "lis_status": "not_applicable",
    "lis_level": null
  },
  "recent_claims": [
    {
      "fill_date": "2025-09-10",
      "drug_name": "Eliquis 5mg",
      "gross_cost": 650.00,
      "member_cost": 162.50,
      "phase": "coverage_gap"
    },
    {
      "fill_date": "2025-08-15",
      "drug_name": "Jardiance 25mg",
      "gross_cost": 580.00,
      "member_cost": 114.50,
      "phase": "split_icl_gap"
    }
  ]
}
```

### Example 3: HDHP Combined Accumulator

**Request:** "Generate an HDHP accumulator with combined medical and pharmacy"

```json
{
  "accumulator_summary": {
    "member_id": "MEM001234567",
    "rx_plan_code": "RX-HDHP-HSA",
    "plan_year": 2025,
    "as_of_date": "2025-06-15",
    "combined_accumulator": true
  },
  "combined_deductible": {
    "individual": {
      "limit": 1600.00,
      "applied": 1170.00,
      "remaining": 430.00,
      "met": false,
      "breakdown": {
        "medical": 850.00,
        "pharmacy": 320.00
      }
    },
    "family": {
      "limit": 3200.00,
      "applied": 2100.00,
      "remaining": 1100.00,
      "met": false
    }
  },
  "combined_oop_max": {
    "individual": {
      "limit": 7000.00,
      "applied": 1650.00,
      "remaining": 5350.00,
      "met": false,
      "breakdown": {
        "medical": 1200.00,
        "pharmacy": 450.00
      }
    },
    "family": {
      "limit": 14000.00,
      "applied": 2850.00,
      "remaining": 11150.00,
      "met": false
    }
  },
  "pharmacy_specific": {
    "preventive_rx": {
      "exempt_from_deductible": true,
      "ytd_preventive_cost": 125.00,
      "drugs": ["Metformin", "Lisinopril", "Atorvastatin"]
    },
    "claims_before_deductible_met": {
      "paid_by_member": 320.00,
      "claims_count": 4
    },
    "claims_after_deductible_met": {
      "expected_date": "2025-07-15",
      "post_deductible_copays": "Standard tier copays apply"
    }
  },
  "hsa_account": {
    "current_balance": 3200.00,
    "contributions_ytd": {
      "employer": 500.00,
      "employee": 2000.00,
      "total": 2500.00
    },
    "distributions_ytd": {
      "medical": 1200.00,
      "pharmacy": 450.00,
      "dental": 150.00,
      "vision": 50.00,
      "total": 1850.00
    },
    "annual_limit": {
      "individual": 4300.00,
      "remaining_contribution_room": 1800.00
    }
  }
}
```

### Example 4: Accumulator Update from Claim

**Request:** "Generate an accumulator update after a pharmacy claim"

```json
{
  "claim": {
    "claim_id": "RX20250615000123",
    "fill_date": "2025-06-15",
    "member_id": "MEM001234567",
    "drug_name": "Lipitor 40mg",
    "ndc": "00071015523",
    "tier": 3,
    "gross_cost": 185.00,
    "days_supply": 30
  },
  "accumulator_before": {
    "rx_deductible": {
      "limit": 250.00,
      "applied": 200.00,
      "remaining": 50.00,
      "met": false
    },
    "rx_oop_max": {
      "limit": 2500.00,
      "applied": 425.00,
      "remaining": 2075.00,
      "met": false
    }
  },
  "cost_calculation": {
    "deductible_portion": {
      "remaining_deductible": 50.00,
      "applied_to_claim": 50.00
    },
    "post_deductible_cost": {
      "tier_3_copay": 60.00,
      "amount_after_deductible": 60.00
    },
    "total_member_cost": 110.00,
    "plan_paid": 75.00
  },
  "accumulator_after": {
    "rx_deductible": {
      "limit": 250.00,
      "applied": 250.00,
      "remaining": 0.00,
      "met": true,
      "met_date": "2025-06-15"
    },
    "rx_oop_max": {
      "limit": 2500.00,
      "applied": 535.00,
      "remaining": 1965.00,
      "met": false
    }
  },
  "member_message": "Your pharmacy deductible has been met. Future brand medications will be at standard copay."
}
```

## Accumulator Adjustment Rules

### Claim Reversals
When a claim is reversed, accumulators must be adjusted:
```json
{
  "reversal_claim_id": "RX20250615000123",
  "original_member_paid": 110.00,
  "accumulator_adjustment": {
    "rx_deductible_reduction": 50.00,
    "rx_oop_reduction": 110.00
  },
  "deductible_status_after": {
    "applied": 200.00,
    "met": false
  }
}
```

### Coordination of Benefits
When secondary coverage pays:
```json
{
  "primary_plan_paid": 100.00,
  "secondary_plan_paid": 25.00,
  "member_responsibility": 10.00,
  "accumulator_credit": {
    "primary_deductible": 0.00,
    "primary_oop": 10.00,
    "note": "Only member out-of-pocket applies to accumulators"
  }
}
```

## Validation Rules

### Accumulator Validation
1. Applied amount cannot exceed limit
2. Individual accumulator cannot exceed family accumulator
3. Family deductible met triggers all individual deductibles met
4. Part D phases must progress sequentially
5. TrOOP components must sum correctly

### Claim-Accumulator Consistency
1. Claim dates must be within plan year
2. Accumulator updates must match claim adjudication
3. Reversals must reduce accumulators appropriately
4. COB claims apply member responsibility only

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| CSV | "as CSV" | Accumulator reporting |
| SQL | "as SQL" | Database loading |
| PDF | "accumulator statement" | Member statements |

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Deductible amount | Non-negative | $500 individual, $1000 family |
| OOP maximum | ≥ deductible | $3000 individual |
| Accumulator YTD | Non-negative, ≤ maximum | $1250 of $3000 OOP |
| Plan year | Valid date range | 2025-01-01 to 2025-12-31 |
| Part D phase | Valid phase name | "Initial Coverage", "Coverage Gap" |
| TrOOP | True Out-of-Pocket tracking | $2100 of $8000 |
| Family tier | individual or family | "family" |
| Reset date | Plan year start | 2025-01-01 |

### Business Rules

- **Deductible Phase**: Member pays 100% until deductible met
- **Coinsurance Phase**: Member pays copay/coinsurance after deductible
- **OOP Maximum**: Member pays $0 after OOP max reached
- **Family Accumulation**: Family members may share accumulators
- **Part D Phases**: Deductible → Initial Coverage → Coverage Gap → Catastrophic
- **TrOOP Calculation**: Only certain costs count toward TrOOP (excludes premiums)
- **Accumulator Adjustment**: Manufacturer copay assistance may not count toward accumulators
- **Mid-Year Changes**: Job change may reset or carry over accumulators

## Related Skills

### RxMemberSim
- [SKILL.md](SKILL.md) - RxMemberSim overview
- [rx-enrollment.md](rx-enrollment.md) - Pharmacy enrollment
- [retail-pharmacy.md](retail-pharmacy.md) - Retail pharmacy claims
- [specialty-pharmacy.md](specialty-pharmacy.md) - High-cost specialty accumulation

### Cross-Product: MemberSim
- [../membersim/accumulator-tracking.md](../membersim/accumulator-tracking.md) - Medical benefit accumulators
- [../membersim/plan-benefits.md](../membersim/plan-benefits.md) - Combined deductible/OOP design

> **Integration Pattern:** For integrated medical+Rx plans, pharmacy costs (this skill) and medical costs (MemberSim) may share deductibles and OOP maximums. Ensure accumulator totals are synchronized across products. When medical deductible is met, pharmacy claims may adjudicate differently.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - Code systems
- [../../references/data-models.md](../../references/data-models.md) - Data models
