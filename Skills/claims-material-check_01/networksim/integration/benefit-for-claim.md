---
name: benefit-for-claim
description: |
  Apply benefit structure context to MemberSim claims for realistic adjudication.
  Calculates deductibles, copays, coinsurance, and accumulator impacts.
  Handles medical and pharmacy benefit coordination.
  
  Trigger phrases: "benefit for this claim", "apply cost sharing", "calculate member cost",
  "deductible applies", "coinsurance calculation", "apply plan benefits",
  "accumulator update", "out-of-pocket calculation"
version: "1.0"
category: integration
related_skills:
  - synthetic-plan
  - network-for-member
  - hmo-network-pattern
  - ppo-network-pattern
cross_product:
  - membersim
  - rxmembersim
---

# Benefit for Claim

## Overview

This integration skill applies benefit structure context to MemberSim claims for realistic adjudication. It calculates member cost sharing including deductibles, copays, coinsurance, and out-of-pocket accumulator impacts.

Use this skill when you need to:
- Calculate member cost sharing for claims
- Apply deductible logic with accumulator tracking
- Determine copay vs coinsurance application
- Handle tiered benefit structures
- Coordinate medical and pharmacy benefits
- Track out-of-pocket accumulator progress

---

## Integration Pattern

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   MemberSim     │     │   Benefit for        │     │   NetworkSim    │
│   Claim         │────▶│   Claim Skill        │────▶│   Cost Sharing  │
│                 │     │   (Adjudication)     │     │   + Accumulators│
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

---

## Input Context

### Claim Context

```json
{
  "claim_context": {
    "claim_id": "CLM-2024-001234",
    "claim_type": "Professional | Facility | Pharmacy",
    "service_date": "2024-06-15",
    "allowed_amount": 250.00,
    "service_category": "Office Visit | Inpatient | Surgery | Lab | Rx",
    "service_code": "99213",
    "place_of_service": "11",
    "network_status": {
      "status": "IN_NETWORK",
      "tier": "Tier 1"
    },
    "provider": {
      "npi": "1234567890",
      "specialty": "Internal Medicine"
    }
  }
}
```

### Member Benefit Context

```json
{
  "member_benefit": {
    "member_id": "MEM-2024-001234",
    "plan_id": "PLAN-PPO-2024",
    "plan_type": "PPO",
    "effective_date": "2024-01-01",
    
    "cost_sharing": {
      "deductible": {
        "individual": 1500,
        "family": 3000,
        "embedded": true
      },
      "out_of_pocket_max": {
        "individual": 6000,
        "family": 12000,
        "includes_deductible": true
      },
      "coinsurance": {
        "in_network": 0.20,
        "out_of_network": 0.40
      }
    },
    
    "accumulators": {
      "deductible_ytd": {
        "individual": 750,
        "family": 1200
      },
      "oop_ytd": {
        "individual": 1100,
        "family": 2400
      }
    }
  }
}
```

---

## Cost Sharing Calculation Logic

### Calculation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Cost Sharing Calculation                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │  Check OOP Max               │
               │  (Is member at OOP max?)     │
               └──────────────────────────────┘
                      │              │
                     YES            NO
                      │              │
                      ▼              ▼
          ┌──────────────┐    ┌──────────────────┐
          │ Plan pays    │    │ Check deductible │
          │ 100%         │    │ (Is deductible   │
          │ Member = $0  │    │  satisfied?)     │
          └──────────────┘    └──────────────────┘
                                    │        │
                                   YES       NO
                                    │        │
                                    ▼        ▼
                          ┌────────────┐  ┌────────────┐
                          │ Apply      │  │ Apply to   │
                          │ copay or   │  │ deductible │
                          │ coinsurance│  │ first      │
                          └────────────┘  └────────────┘
                                    │              │
                                    ▼              ▼
                          ┌────────────────────────────┐
                          │ Check OOP accumulation     │
                          │ Cap at remaining OOP       │
                          └────────────────────────────┘
```

### Calculation Formula

```json
{
  "calculation_steps": [
    {
      "step": 1,
      "check": "OOP Max Status",
      "formula": "IF oop_ytd >= oop_max THEN member_responsibility = 0"
    },
    {
      "step": 2,
      "check": "Deductible Status",
      "formula": "deductible_remaining = MAX(0, deductible - deductible_ytd)"
    },
    {
      "step": 3,
      "apply": "Deductible",
      "formula": "deductible_applied = MIN(allowed_amount, deductible_remaining)"
    },
    {
      "step": 4,
      "apply": "Coinsurance/Copay",
      "formula": "IF copay_service THEN member_coinsurance = copay ELSE member_coinsurance = (allowed_amount - deductible_applied) × coinsurance_rate"
    },
    {
      "step": 5,
      "apply": "OOP Cap",
      "formula": "total_member = MIN(deductible_applied + member_coinsurance, oop_remaining)"
    },
    {
      "step": 6,
      "calculate": "Plan Payment",
      "formula": "plan_paid = allowed_amount - total_member"
    }
  ]
}
```

---

## Service-Specific Cost Sharing

### Cost Sharing by Service Type

```json
{
  "service_cost_sharing": {
    "office_visit_primary": {
      "applies": "Copay",
      "in_network": 30,
      "out_of_network": null,
      "deductible_waived": true
    },
    "office_visit_specialist": {
      "applies": "Copay",
      "in_network": 50,
      "out_of_network": null,
      "deductible_waived": true
    },
    "preventive_care": {
      "applies": "None",
      "in_network": 0,
      "out_of_network": "Coinsurance",
      "aca_preventive": true
    },
    "diagnostic_lab": {
      "applies": "Coinsurance",
      "in_network": 0.20,
      "out_of_network": 0.40,
      "deductible_applies": true
    },
    "diagnostic_imaging": {
      "applies": "Coinsurance",
      "in_network": 0.20,
      "out_of_network": 0.40,
      "deductible_applies": true
    },
    "inpatient_admission": {
      "applies": "Copay + Coinsurance",
      "facility_copay": 500,
      "coinsurance": 0.20,
      "deductible_applies": true
    },
    "outpatient_surgery": {
      "applies": "Copay + Coinsurance",
      "facility_copay": 250,
      "coinsurance": 0.20,
      "deductible_applies": true
    },
    "emergency_room": {
      "applies": "Copay",
      "copay": 250,
      "waived_if_admitted": true,
      "in_out_same": true
    },
    "urgent_care": {
      "applies": "Copay",
      "in_network": 50,
      "out_of_network": 75
    }
  }
}
```

---

## Output Schema

### Complete Adjudication Result

```json
{
  "claim_adjudication": {
    "claim_id": "CLM-2024-001234",
    "adjudication_date": "2024-06-16",
    "status": "Processed",
    
    "amounts": {
      "billed_amount": 350.00,
      "allowed_amount": 250.00,
      "network_discount": 100.00
    },
    
    "cost_sharing_applied": {
      "service_type": "Specialist Office Visit",
      "cost_sharing_type": "Copay",
      "network_tier": "In-Network",
      
      "deductible": {
        "applies": false,
        "reason": "Copay service - deductible waived",
        "amount_applied": 0.00
      },
      
      "copay": {
        "applies": true,
        "amount": 50.00,
        "basis": "Specialist visit copay"
      },
      
      "coinsurance": {
        "applies": false,
        "rate": null,
        "amount": 0.00
      },
      
      "oop_cap_applied": false
    },
    
    "payment_summary": {
      "member_responsibility": 50.00,
      "plan_paid": 200.00,
      "provider_write_off": 100.00
    },
    
    "accumulator_updates": {
      "deductible": {
        "prior_ytd": 750.00,
        "this_claim": 0.00,
        "new_ytd": 750.00,
        "remaining": 750.00
      },
      "out_of_pocket": {
        "prior_ytd": 1100.00,
        "this_claim": 50.00,
        "new_ytd": 1150.00,
        "remaining": 4850.00
      }
    }
  }
}
```

---

## Examples

### Example 1: Office Visit with Copay

**Claim Context**:
```json
{
  "service_type": "Office Visit - Primary Care",
  "allowed_amount": 150.00,
  "network_status": "IN_NETWORK"
}
```

**Member Accumulators**:
```json
{
  "deductible_ytd": 500,
  "deductible_max": 1500,
  "oop_ytd": 800,
  "oop_max": 6000
}
```

**Adjudication Result**:
```json
{
  "cost_sharing_applied": {
    "service_type": "Primary Care Visit",
    "cost_sharing_type": "Copay",
    "deductible_applies": false,
    "copay": 30.00,
    "coinsurance": 0.00
  },
  "payment_summary": {
    "member_responsibility": 30.00,
    "plan_paid": 120.00
  },
  "accumulator_updates": {
    "deductible_applied": 0.00,
    "oop_applied": 30.00,
    "new_oop_ytd": 830.00
  }
}
```

### Example 2: Lab Work with Deductible

**Claim Context**:
```json
{
  "service_type": "Diagnostic Lab",
  "allowed_amount": 200.00,
  "network_status": "IN_NETWORK"
}
```

**Member Accumulators**:
```json
{
  "deductible_ytd": 1400,
  "deductible_max": 1500,
  "oop_ytd": 2000,
  "oop_max": 6000
}
```

**Adjudication Result**:
```json
{
  "cost_sharing_applied": {
    "service_type": "Diagnostic Lab",
    "cost_sharing_type": "Deductible + Coinsurance",
    
    "deductible": {
      "remaining_before": 100.00,
      "applied_to_claim": 100.00,
      "satisfied_with_claim": true
    },
    
    "coinsurance": {
      "after_deductible_amount": 100.00,
      "rate": 0.20,
      "amount": 20.00
    }
  },
  "payment_summary": {
    "member_responsibility": 120.00,
    "plan_paid": 80.00
  },
  "accumulator_updates": {
    "deductible_applied": 100.00,
    "new_deductible_ytd": 1500.00,
    "deductible_satisfied": true,
    "oop_applied": 120.00,
    "new_oop_ytd": 2120.00
  }
}
```

### Example 3: Inpatient Admission (Facility + Coinsurance)

**Claim Context**:
```json
{
  "service_type": "Inpatient Admission",
  "allowed_amount": 25000.00,
  "network_status": "IN_NETWORK",
  "los_days": 4
}
```

**Member Accumulators**:
```json
{
  "deductible_ytd": 1500,
  "deductible_max": 1500,
  "oop_ytd": 3500,
  "oop_max": 6000
}
```

**Adjudication Result**:
```json
{
  "cost_sharing_applied": {
    "service_type": "Inpatient Admission",
    "cost_sharing_type": "Copay + Coinsurance",
    
    "deductible": {
      "status": "Already satisfied",
      "applied_to_claim": 0.00
    },
    
    "facility_copay": {
      "per_admission": 500.00,
      "applied": 500.00
    },
    
    "coinsurance": {
      "base_amount": 24500.00,
      "rate": 0.20,
      "calculated": 4900.00,
      "oop_cap_applied": true,
      "actual_applied": 2000.00
    }
  },
  "payment_summary": {
    "member_responsibility": 2500.00,
    "plan_paid": 22500.00
  },
  "accumulator_updates": {
    "oop_applied": 2500.00,
    "new_oop_ytd": 6000.00,
    "oop_max_reached": true,
    "remaining_claims_at_100_percent": true
  }
}
```

### Example 4: Out-of-Network Claim (PPO)

**Claim Context**:
```json
{
  "service_type": "Specialist Visit",
  "billed_amount": 400.00,
  "allowed_amount": 200.00,
  "network_status": "OUT_OF_NETWORK"
}
```

**Adjudication Result**:
```json
{
  "cost_sharing_applied": {
    "network_tier": "Out-of-Network",
    "cost_sharing_type": "Separate Deductible + Coinsurance",
    
    "allowed_calculation": {
      "methodology": "UCR 80th percentile",
      "allowed": 200.00,
      "member_balance_bill": 200.00
    },
    
    "deductible": {
      "oon_deductible": 3000,
      "oon_deductible_ytd": 500,
      "applied_to_claim": 200.00
    },
    
    "coinsurance": {
      "rate": 0.40,
      "amount": 0.00,
      "reason": "Applied to deductible first"
    }
  },
  "payment_summary": {
    "member_deductible": 200.00,
    "member_coinsurance": 0.00,
    "member_balance_bill": 200.00,
    "total_member_responsibility": 400.00,
    "plan_paid": 0.00
  }
}
```

### Example 5: Preventive Care (ACA $0)

**Claim Context**:
```json
{
  "service_type": "Annual Wellness Visit",
  "procedure_code": "G0438",
  "allowed_amount": 250.00,
  "network_status": "IN_NETWORK",
  "preventive_indicator": true
}
```

**Adjudication Result**:
```json
{
  "cost_sharing_applied": {
    "service_type": "Preventive Care",
    "aca_preventive": true,
    "deductible_waived": true,
    "copay_waived": true,
    "coinsurance_waived": true,
    "member_cost": 0.00
  },
  "payment_summary": {
    "member_responsibility": 0.00,
    "plan_paid": 250.00
  },
  "accumulator_updates": {
    "deductible_applied": 0.00,
    "oop_applied": 0.00,
    "note": "Preventive services do not apply to accumulators"
  }
}
```

---

## Tiered Benefit Handling

### Tiered Network Cost Sharing

```json
{
  "tiered_cost_sharing": {
    "tier_1_preferred": {
      "copay_pcp": 15,
      "copay_specialist": 30,
      "coinsurance": 0.10,
      "facility_copay": 250
    },
    "tier_2_standard": {
      "copay_pcp": 30,
      "copay_specialist": 50,
      "coinsurance": 0.20,
      "facility_copay": 500
    },
    "tier_3_basic": {
      "copay_pcp": 50,
      "copay_specialist": 75,
      "coinsurance": 0.35,
      "facility_copay": 750
    },
    "out_of_network": {
      "deductible_separate": true,
      "deductible_multiplier": 2.0,
      "coinsurance": 0.50,
      "oop_separate": true
    }
  }
}
```

---

## Validation Rules

| Rule | Validation |
|------|------------|
| Deductible Logic | Deductible applied before coinsurance |
| OOP Cap | Member cost capped at OOP remaining |
| Copay vs Coinsurance | Correct type for service |
| Network Tier | Correct tier cost sharing applied |
| Preventive | ACA preventive at $0 in-network |
| Accumulator Math | Prior + claim = new YTD |

---

## Cross-Product Integration

### To MemberSim Claims

Cost sharing applies to claim adjudication:

```json
{
  "x12_835": {
    "CLP": {
      "claim_status": "1",
      "total_charge": 350.00,
      "payment_amount": 200.00
    },
    "CAS": [
      {"group_code": "PR", "reason_code": "2", "amount": 50.00},
      {"group_code": "CO", "reason_code": "45", "amount": 100.00}
    ]
  }
}
```

### To RxMemberSim

Same logic applies to pharmacy claims with pharmacy-specific cost sharing.

---

## Related Skills

- [Synthetic Plan](../synthetic/synthetic-plan.md) - Generate plan structures
- [Network for Member](network-for-member.md) - Determine network status
- [PPO Network Pattern](../patterns/ppo-network-pattern.md) - PPO cost sharing
- [Tiered Network Pattern](../patterns/tiered-network-pattern.md) - Tiered cost sharing

---

*Benefit for Claim is an integration skill in the NetworkSim product.*
