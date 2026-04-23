---
name: network-for-member
description: |
  Add network context to MemberSim member entities and claims.
  Determines network status, tier assignment, and cost sharing based on
  provider-network relationships. Supports in/out-of-network determination.
  
  Trigger phrases: "network for this member", "determine network status",
  "is provider in network", "network tier for claim", "add network context",
  "in-network or out-of-network"
version: "1.0"
category: integration
related_skills:
  - synthetic-network
  - synthetic-plan
  - hmo-network-pattern
  - ppo-network-pattern
  - tiered-network-pattern
cross_product:
  - membersim
---

# Network for Member

## Overview

This integration skill adds network context to MemberSim member entities and claims. It determines provider network status, assigns appropriate network tiers, and calculates tier-based cost sharing for claim adjudication.

Use this skill when you need to:
- Determine if a provider is in-network for a member's plan
- Assign network tier for tiered network products
- Calculate tier-appropriate cost sharing
- Handle out-of-network claims processing
- Apply network-based utilization rules

---

## Integration Pattern

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   MemberSim     │     │   Network for        │     │   NetworkSim    │
│   Member/Claim  │────▶│   Member Skill       │────▶│   Network +     │
│                 │     │   (Status Logic)     │     │   Cost Sharing  │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

---

## Input Context

### Member Context

```json
{
  "member_context": {
    "member_id": "MEM-2024-001234",
    "plan": {
      "plan_id": "PLAN-PPO-2024",
      "plan_type": "PPO",
      "network_id": "NET-IL-PPO-001"
    },
    "coverage_effective_date": "2024-01-01",
    "coverage_termination_date": null,
    "location": {
      "state": "IL",
      "county_fips": "17031",
      "zip": "60601"
    }
  }
}
```

### Claim/Service Context

```json
{
  "service_context": {
    "service_date": "2024-06-15",
    "service_type": "Professional | Facility | Ancillary",
    "provider": {
      "npi": "1234567890",
      "name": "Dr. Jane Smith",
      "taxonomy": "207R00000X"
    },
    "facility": {
      "npi": "1987654321",
      "name": "Chicago General Hospital",
      "type": "Hospital"
    },
    "place_of_service": "21",
    "procedure_codes": ["99213", "36415"],
    "diagnosis_codes": ["E11.9"]
  }
}
```

---

## Network Status Determination

### Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│                    Network Status Check                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │  Is provider in network      │
               │  roster for member's plan?   │
               └──────────────────────────────┘
                      │              │
                     YES            NO
                      │              │
                      ▼              ▼
          ┌──────────────┐    ┌──────────────────┐
          │ Check tier   │    │ Is this HMO/EPO? │
          │ assignment   │    └──────────────────┘
          └──────────────┘           │        │
                 │                  YES       NO
                 ▼                   │        │
          ┌──────────────┐          ▼        ▼
          │ Return tier  │    ┌────────┐  ┌──────────┐
          │ + cost share │    │ DENY   │  │ OON Tier │
          └──────────────┘    │(unless │  │ + OON    │
                              │ emerg) │  │ cost     │
                              └────────┘  │ sharing  │
                                          └──────────┘
```

### Network Lookup Logic

```json
{
  "lookup_steps": [
    {
      "step": 1,
      "action": "Get member's network_id from plan",
      "source": "member_context.plan.network_id"
    },
    {
      "step": 2,
      "action": "Query network roster for provider NPI",
      "query": "SELECT tier_id, effective_date, termination_date FROM network_roster WHERE network_id = ? AND provider_npi = ?"
    },
    {
      "step": 3,
      "action": "Check effective dates",
      "validation": "service_date BETWEEN effective_date AND COALESCE(termination_date, '9999-12-31')"
    },
    {
      "step": 4,
      "action": "Return network status and tier",
      "output": "network_status, tier_id, cost_sharing"
    }
  ]
}
```

---

## Network Status Output

### In-Network (Single Tier)

```json
{
  "network_status": {
    "status": "IN_NETWORK",
    "network_id": "NET-IL-PPO-001",
    "network_name": "Blue Cross PPO Illinois",
    "tier": {
      "tier_id": "IN-NETWORK",
      "tier_name": "In-Network",
      "tier_level": 1
    },
    "provider_participation": {
      "npi": "1234567890",
      "participating": true,
      "effective_date": "2020-01-01",
      "contract_type": "Standard"
    },
    "cost_sharing": {
      "deductible_applies": true,
      "deductible_type": "In-Network",
      "coinsurance": 0.20,
      "copay": null,
      "oop_max_applies": true
    }
  }
}
```

### In-Network (Tiered - Preferred)

```json
{
  "network_status": {
    "status": "IN_NETWORK",
    "network_id": "NET-TX-TIERED-001",
    "network_name": "HealthSelect Tiered PPO",
    "tier": {
      "tier_id": "BLUE",
      "tier_name": "Blue Tier - Preferred",
      "tier_level": 1
    },
    "tier_reason": "Provider quality score in top 25%",
    "provider_participation": {
      "npi": "1234567890",
      "participating": true,
      "tier_effective_date": "2024-01-01",
      "quality_score": 92
    },
    "cost_sharing": {
      "deductible_applies": true,
      "coinsurance": 0.10,
      "copay": 15,
      "copay_type": "Primary Care",
      "tier_differential": "20% lower than standard tier"
    }
  }
}
```

### In-Network (Tiered - Standard)

```json
{
  "network_status": {
    "status": "IN_NETWORK",
    "network_id": "NET-TX-TIERED-001",
    "tier": {
      "tier_id": "WHITE",
      "tier_name": "White Tier - Standard",
      "tier_level": 2
    },
    "cost_sharing": {
      "deductible_applies": true,
      "coinsurance": 0.20,
      "copay": 30,
      "copay_type": "Primary Care"
    }
  }
}
```

### Out-of-Network (PPO)

```json
{
  "network_status": {
    "status": "OUT_OF_NETWORK",
    "network_id": "NET-IL-PPO-001",
    "tier": {
      "tier_id": "OUT-OF-NETWORK",
      "tier_name": "Out-of-Network",
      "tier_level": 99
    },
    "provider_participation": {
      "npi": "1234567890",
      "participating": false
    },
    "cost_sharing": {
      "deductible_applies": true,
      "deductible_type": "Out-of-Network",
      "deductible_separate": true,
      "coinsurance": 0.40,
      "reimbursement_basis": "UCR_80",
      "balance_billing": {
        "allowed": true,
        "member_responsible": true,
        "surprise_billing_protection": "Federal NSA applies"
      },
      "oop_max_applies": true,
      "oop_max_separate": true
    }
  }
}
```

### Out-of-Network (HMO - Denied)

```json
{
  "network_status": {
    "status": "OUT_OF_NETWORK",
    "network_id": "NET-CA-HMO-001",
    "network_type": "HMO",
    "tier": null,
    "provider_participation": {
      "npi": "1234567890",
      "participating": false
    },
    "coverage_determination": {
      "covered": false,
      "denial_reason": "Non-participating provider in closed network",
      "denial_code": "CO-4",
      "exception_possible": false
    },
    "emergency_exception": {
      "applicable": "Only if Place of Service = 23 (Emergency Room)",
      "current_pos": "11",
      "exception_applies": false
    }
  }
}
```

### Emergency Exception

```json
{
  "network_status": {
    "status": "OUT_OF_NETWORK",
    "network_type": "HMO",
    "emergency_exception": {
      "applicable": true,
      "reason": "Place of Service 23 (Emergency Room)",
      "coverage": "Covered as in-network",
      "cost_sharing": {
        "deductible_applies": true,
        "deductible_type": "In-Network",
        "coinsurance": 0.20,
        "balance_billing": {
          "allowed": false,
          "reason": "Federal No Surprises Act protection"
        }
      },
      "regulatory_basis": "No Surprises Act (2022)"
    }
  }
}
```

---

## Cost Sharing Calculation

### By Network Type

| Network Type | In-Network | Out-of-Network |
|--------------|------------|----------------|
| HMO | Covered per plan | Not covered (except emergency) |
| EPO | Covered per plan | Not covered (except emergency) |
| PPO | Tier 1 cost sharing | Higher deductible + coinsurance |
| POS | In-network cost sharing | OON with referral |
| Tiered PPO | Tier-based cost sharing | OON tier cost sharing |

### Tier-Based Cost Sharing Example

```json
{
  "cost_sharing_by_tier": {
    "service_type": "Office Visit - Primary Care",
    "service_code": "99213",
    
    "tier_1_preferred": {
      "copay": 15,
      "coinsurance": null,
      "deductible_waived": true
    },
    "tier_2_standard": {
      "copay": 30,
      "coinsurance": null,
      "deductible_waived": true
    },
    "tier_3_basic": {
      "copay": 50,
      "coinsurance": null,
      "deductible_waived": false
    },
    "out_of_network": {
      "copay": null,
      "coinsurance": 0.40,
      "deductible_applies": true,
      "deductible_separate": true
    }
  }
}
```

---

## Examples

### Example 1: PPO In-Network Claim

**MemberSim Context**:
```json
{
  "member": {"plan_type": "PPO", "network_id": "NET-IL-PPO-001"},
  "claim": {"provider_npi": "1234567890", "service_date": "2024-06-15"}
}
```

**Network Status Result**:
```json
{
  "network_status": {
    "status": "IN_NETWORK",
    "tier": {"tier_id": "IN-NETWORK", "tier_level": 1},
    "cost_sharing": {
      "deductible_applies": true,
      "coinsurance": 0.20,
      "deductible_remaining": 750
    }
  },
  "adjudication_impact": {
    "allowed_amount_source": "Contracted rate",
    "member_responsibility": "Deductible + 20% coinsurance",
    "balance_billing": "Not applicable"
  }
}
```

### Example 2: Tiered Network - Preferred Tier

**MemberSim Context**:
```json
{
  "member": {"plan_type": "PPO", "network_id": "NET-TX-TIERED-001"},
  "claim": {"provider_npi": "1456789012", "cpt": "99213", "service_type": "Office Visit"}
}
```

**Network Status Result**:
```json
{
  "network_status": {
    "status": "IN_NETWORK",
    "tier": {
      "tier_id": "BLUE",
      "tier_name": "Blue Tier - Preferred",
      "tier_level": 1
    },
    "tier_assignment_reason": "Provider quality score: 94 (top quartile)",
    "cost_sharing": {
      "copay": 15,
      "coinsurance": null,
      "deductible_waived": true,
      "member_cost": 15.00
    }
  },
  "tier_comparison": {
    "if_standard_tier": {"copay": 30, "savings": 15},
    "if_basic_tier": {"copay": 50, "savings": 35}
  }
}
```

### Example 3: HMO Out-of-Network (Denied)

**MemberSim Context**:
```json
{
  "member": {"plan_type": "HMO", "network_id": "NET-CA-HMO-001"},
  "claim": {"provider_npi": "1567890123", "place_of_service": "11"}
}
```

**Network Status Result**:
```json
{
  "network_status": {
    "status": "OUT_OF_NETWORK",
    "network_type": "HMO",
    "covered": false,
    "denial": {
      "reason": "Non-participating provider",
      "code": "CO-4",
      "message": "This service is not covered when provided by out-of-network providers"
    },
    "member_options": [
      "Find an in-network provider",
      "Request out-of-network exception (medical necessity)",
      "Pay full charges out of pocket"
    ]
  }
}
```

### Example 4: Emergency Exception

**MemberSim Context**:
```json
{
  "member": {"plan_type": "EPO", "network_id": "NET-AZ-EPO-001"},
  "claim": {
    "provider_npi": "1678901234",
    "place_of_service": "23",
    "diagnosis": "R10.0",
    "service_type": "Emergency"
  }
}
```

**Network Status Result**:
```json
{
  "network_status": {
    "status": "OUT_OF_NETWORK",
    "emergency_exception": {
      "applies": true,
      "reason": "Emergency services at POS 23",
      "processed_as": "IN_NETWORK",
      "regulatory_protection": "No Surprises Act"
    },
    "cost_sharing": {
      "apply_in_network_cost_sharing": true,
      "copay": 250,
      "coinsurance": 0.20,
      "balance_billing_protected": true
    }
  }
}
```

---

## Validation Rules

| Rule | Validation |
|------|------------|
| Network Active | Network effective on service date |
| Provider Roster | Provider in roster for service date |
| Plan Match | Member's plan linked to network |
| Tier Valid | Tier assignment current |
| POS Check | Emergency exception only for POS 23 |
| Date Range | Service date within coverage period |

---

## Cross-Product Integration

### From MemberSim

Claim receives network context:

```json
{
  "claim": {
    "claim_id": "CLM-2024-001234",
    "network_context": {
      "network_status": "IN_NETWORK",
      "tier_id": "TIER-1",
      "cost_sharing_applied": {
        "copay": 30,
        "coinsurance": 0.20
      }
    }
  }
}
```

### Adjudication Impact

```json
{
  "adjudication": {
    "allowed_amount": 150.00,
    "member_deductible": 0.00,
    "member_coinsurance": 30.00,
    "member_copay": 0.00,
    "plan_paid": 120.00,
    "network_discount": 50.00,
    "balance_billing": 0.00
  }
}
```

---

## Related Skills

- [Synthetic Network](../synthetic/synthetic-network.md) - Generate networks
- [Synthetic Plan](../synthetic/synthetic-plan.md) - Generate plan structures
- [Tiered Network Pattern](../patterns/tiered-network-pattern.md) - Tiered network templates
- [Benefit for Claim](benefit-for-claim.md) - Apply benefit structures

---

*Network for Member is an integration skill in the NetworkSim product.*
