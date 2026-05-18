---
name: ppo-network-pattern
description: |
  Reusable PPO network configuration pattern with open access model,
  in-network/out-of-network tiers, no referral requirements, and
  fee-for-service structures. Use as starting template for PPO generation.
  
  Trigger phrases: "PPO network pattern", "open access model", "PPO template",
  "PPO configuration", "fee-for-service network", "dual-tier network"
version: "1.0"
category: patterns
related_skills:
  - network-types
  - synthetic-network
  - synthetic-plan
  - hmo-network-pattern
---

# PPO Network Pattern

## Overview

This pattern provides a reusable template for generating PPO (Preferred Provider Organization) network configurations. PPOs offer open access to any provider, with financial incentives (lower cost sharing) to use in-network providers. No referrals are required for specialist care.

Use this pattern when you need:
- Open access network configuration
- In-network/out-of-network cost sharing tiers
- No PCP or referral requirements
- Fee-for-service payment structures

---

## Pattern Variants

### Standard PPO

Traditional PPO with broad network and meaningful OON benefits.

```json
{
  "pattern_id": "PPO-STANDARD",
  "pattern_name": "Standard PPO",
  "characteristics": {
    "network_breadth": "Broad",
    "oon_benefit_level": "Meaningful (40-60% coinsurance)",
    "provider_flexibility": "Maximum",
    "cost_position": "Higher premium"
  },
  "network_configuration": {
    "network_type": "PPO",
    "network_breadth": "Broad",
    "pcp_required": false,
    "referral_required": false,
    "out_of_network_coverage": true,
    "balance_billing_protection": "Limited"
  },
  "tier_structure": {
    "in_network": {
      "deductible_modifier": 1.0,
      "coinsurance": 0.20,
      "oop_max_modifier": 1.0
    },
    "out_of_network": {
      "deductible_modifier": 2.0,
      "coinsurance": 0.40,
      "oop_max_modifier": 2.0,
      "reimbursement_basis": "UCR or Medicare + %"
    }
  },
  "payment_model": {
    "provider_payment": "Fee-for-service",
    "fee_schedule": "Negotiated rates",
    "risk_sharing": "None or minimal"
  }
}
```

### Value PPO

PPO with incentivized high-value providers and narrower network.

```json
{
  "pattern_id": "PPO-VALUE",
  "pattern_name": "Value PPO",
  "characteristics": {
    "network_breadth": "Standard",
    "oon_benefit_level": "Reduced (50-70% coinsurance)",
    "provider_flexibility": "Moderate",
    "cost_position": "Moderate premium"
  },
  "network_configuration": {
    "network_type": "PPO",
    "network_breadth": "Standard",
    "pcp_required": false,
    "referral_required": false,
    "out_of_network_coverage": true,
    "provider_selection": "Quality and cost screened"
  },
  "tier_structure": {
    "in_network": {
      "deductible_modifier": 1.0,
      "coinsurance": 0.20,
      "oop_max_modifier": 1.0
    },
    "out_of_network": {
      "deductible_modifier": 2.5,
      "coinsurance": 0.50,
      "oop_max_modifier": 2.5
    }
  },
  "provider_criteria": {
    "quality_threshold": "Top 60%",
    "cost_threshold": "Within 120% of benchmark",
    "patient_experience": "Required minimum score"
  }
}
```

### Premium PPO

High-touch PPO with concierge features and maximum access.

```json
{
  "pattern_id": "PPO-PREMIUM",
  "pattern_name": "Premium PPO",
  "characteristics": {
    "network_breadth": "Broadest",
    "oon_benefit_level": "Generous (30-40% coinsurance)",
    "provider_flexibility": "Maximum plus concierge",
    "cost_position": "Highest premium"
  },
  "network_configuration": {
    "network_type": "PPO",
    "network_breadth": "Broad",
    "pcp_required": false,
    "referral_required": false,
    "out_of_network_coverage": true,
    "enhanced_services": true
  },
  "tier_structure": {
    "in_network": {
      "deductible_modifier": 1.0,
      "coinsurance": 0.10,
      "oop_max_modifier": 1.0
    },
    "out_of_network": {
      "deductible_modifier": 1.5,
      "coinsurance": 0.30,
      "oop_max_modifier": 1.5
    }
  },
  "enhanced_features": {
    "concierge_service": true,
    "direct_specialist_scheduling": true,
    "centers_of_excellence_access": true,
    "second_opinion_program": true,
    "care_navigation": true
  }
}
```

### National PPO

PPO with nationwide access for mobile/traveling populations.

```json
{
  "pattern_id": "PPO-NATIONAL",
  "pattern_name": "National PPO",
  "characteristics": {
    "network_breadth": "National",
    "oon_benefit_level": "Standard",
    "provider_flexibility": "Maximum geographic",
    "cost_position": "Higher premium"
  },
  "network_configuration": {
    "network_type": "PPO",
    "network_breadth": "Broad",
    "geographic_coverage": "All 50 states + territories",
    "pcp_required": false,
    "referral_required": false,
    "out_of_network_coverage": true
  },
  "network_access": {
    "wrap_network": true,
    "rental_networks": ["PHCS", "MultiPlan", "First Health"],
    "direct_contracts": "Major markets",
    "traveling_member_program": true
  },
  "use_cases": [
    "National employers",
    "Remote workforce",
    "Traveling executives",
    "Retiree populations"
  ]
}
```

---

## Template Configuration

### Base PPO Network Template

```json
{
  "network_id": "{{NETWORK_ID}}",
  "network_name": "{{PAYER_NAME}} PPO Network",
  "network_type": "PPO",
  "network_breadth": "{{Broad | Standard}}",
  "effective_date": "{{YYYY-MM-DD}}",
  "status": "Active",
  
  "payer": {
    "payer_id": "{{PAYER_ID}}",
    "payer_name": "{{PAYER_NAME}}",
    "line_of_business": "{{Commercial | Medicare}}"
  },
  
  "geographic_coverage": {
    "coverage_type": "{{National | Regional | State}}",
    "states": ["{{STATE_CODES}}"],
    "service_area": "{{DESCRIPTION}}"
  },
  
  "tier_structure": {
    "tier_count": 2,
    "tiers": [
      {
        "tier_id": "IN-NETWORK",
        "tier_name": "In-Network",
        "tier_level": 1,
        "description": "Contracted providers with negotiated rates",
        "cost_sharing_modifier": 1.0
      },
      {
        "tier_id": "OUT-OF-NETWORK",
        "tier_name": "Out-of-Network",
        "tier_level": 2,
        "description": "Non-contracted providers with higher cost sharing",
        "cost_sharing_modifier": 2.0
      }
    ]
  },
  
  "access_requirements": {
    "pcp_required": false,
    "pcp_selection": {
      "required": false,
      "incentivized": "{{true | false}}",
      "pcp_incentive_amount": "{{AMOUNT if incentivized}}"
    },
    "referral_required": false,
    "preauthorization_required": true,
    "preauthorization_services": [
      "Inpatient admission",
      "Advanced imaging",
      "Specialty drugs",
      "Elective surgery",
      "Durable medical equipment > $500"
    ],
    "out_of_network_coverage": true
  },
  
  "out_of_network_rules": {
    "reimbursement_methodology": "{{UCR | Medicare + % | Fee Schedule}}",
    "ucr_percentile": "{{80 | 90 | 100}}",
    "medicare_percentage": "{{150 | 200 | 250}}",
    "balance_billing": {
      "allowed": true,
      "member_responsible": true,
      "surprise_billing_protection": "{{State law | Federal NSA}}"
    },
    "deductible": {
      "separate": true,
      "amount_modifier": 2.0
    },
    "coinsurance": 0.40,
    "out_of_pocket_maximum": {
      "separate": true,
      "amount_modifier": 2.0
    }
  },
  
  "adequacy_standards": {
    "primary_care": {
      "time_minutes": 15,
      "distance_miles": 10,
      "provider_ratio": "1:2000"
    },
    "specialty": {
      "time_minutes": 30,
      "distance_miles": 30
    },
    "hospital": {
      "time_minutes": 30,
      "distance_miles": 30
    }
  },
  
  "provider_contracting": {
    "contract_term_years": 3,
    "fee_schedule_update": "Annual",
    "credentialing": "NCQA standards",
    "termination_notice_days": 90
  }
}
```

---

## Cost Sharing Templates

### Standard PPO Cost Sharing

```json
{
  "cost_sharing": {
    "deductible": {
      "individual_in_network": 1500,
      "family_in_network": 3000,
      "individual_out_of_network": 3000,
      "family_out_of_network": 6000,
      "embedded": true,
      "cross_accumulation": false
    },
    "coinsurance": {
      "in_network": 0.20,
      "out_of_network": 0.40
    },
    "out_of_pocket_maximum": {
      "individual_in_network": 6000,
      "family_in_network": 12000,
      "individual_out_of_network": 12000,
      "family_out_of_network": 24000,
      "embedded": true,
      "includes_deductible": true,
      "cross_accumulation": false
    },
    "copays": {
      "primary_care": {"in_network": 30, "out_of_network": null},
      "specialist": {"in_network": 50, "out_of_network": null},
      "urgent_care": {"in_network": 50, "out_of_network": 75},
      "emergency_room": {"in_network": 250, "out_of_network": 250}
    }
  }
}
```

### High-Deductible PPO (HDHP)

```json
{
  "cost_sharing": {
    "deductible": {
      "individual_in_network": 3200,
      "family_in_network": 6400,
      "individual_out_of_network": 6000,
      "family_out_of_network": 12000,
      "embedded": false,
      "hsa_eligible": true
    },
    "coinsurance": {
      "in_network": 0.10,
      "out_of_network": 0.30
    },
    "out_of_pocket_maximum": {
      "individual_in_network": 6550,
      "family_in_network": 13100,
      "individual_out_of_network": 13100,
      "family_out_of_network": 26200,
      "embedded": true,
      "includes_deductible": true
    },
    "copays": null,
    "all_services_subject_to_deductible": true,
    "preventive_exception": true
  }
}
```

### Low-Deductible Premium PPO

```json
{
  "cost_sharing": {
    "deductible": {
      "individual_in_network": 500,
      "family_in_network": 1000,
      "individual_out_of_network": 1000,
      "family_out_of_network": 2000,
      "embedded": true
    },
    "coinsurance": {
      "in_network": 0.10,
      "out_of_network": 0.30
    },
    "out_of_pocket_maximum": {
      "individual_in_network": 3000,
      "family_in_network": 6000,
      "individual_out_of_network": 6000,
      "family_out_of_network": 12000,
      "embedded": true,
      "includes_deductible": true
    },
    "copays": {
      "primary_care": {"in_network": 20, "out_of_network": null},
      "specialist": {"in_network": 35, "out_of_network": null},
      "urgent_care": {"in_network": 35, "out_of_network": 50},
      "emergency_room": {"in_network": 150, "out_of_network": 150}
    }
  }
}
```

---

## Out-of-Network Reimbursement Patterns

### UCR-Based Reimbursement

```json
{
  "oon_reimbursement": {
    "methodology": "UCR",
    "description": "Usual, Customary, and Reasonable",
    "percentile": 80,
    "data_source": "FAIR Health",
    "geographic_adjustment": true,
    "calculation": "Min(billed_charge, UCR_80th_percentile)",
    "member_responsibility": "Deductible + Coinsurance + Balance Bill"
  }
}
```

### Medicare-Based Reimbursement

```json
{
  "oon_reimbursement": {
    "methodology": "Medicare + Percentage",
    "description": "Percentage of Medicare Fee Schedule",
    "medicare_percentage": 150,
    "geographic_adjustment": "GPCI applied",
    "calculation": "Medicare_Allowable × 1.50",
    "member_responsibility": "Deductible + Coinsurance + Balance Bill"
  }
}
```

### Reference-Based Pricing

```json
{
  "oon_reimbursement": {
    "methodology": "Reference-Based Pricing",
    "description": "Fixed percentage of Medicare regardless of billed",
    "medicare_percentage": 140,
    "applies_to": "Inpatient and outpatient facility",
    "balance_billing_protection": "Plan negotiates or member assistance",
    "member_hold_harmless": true
  }
}
```

---

## Example: Complete PPO Network Generation

**Prompt**: "Generate a standard commercial PPO network for Illinois"

**Using Pattern**:

```json
{
  "network_id": "IL-PPO-2024-001",
  "network_name": "Blue Cross PPO Illinois",
  "network_type": "PPO",
  "network_breadth": "Broad",
  "effective_date": "2024-01-01",
  "status": "Active",
  
  "payer": {
    "payer_id": "BCBS-IL",
    "payer_name": "Blue Cross Blue Shield of Illinois",
    "line_of_business": "Commercial"
  },
  
  "geographic_coverage": {
    "coverage_type": "State",
    "states": ["IL"],
    "counties": "All Illinois counties"
  },
  
  "tier_structure": {
    "tier_count": 2,
    "tiers": [
      {
        "tier_id": "IN-NETWORK",
        "tier_name": "BlueCard PPO",
        "tier_level": 1,
        "cost_sharing_modifier": 1.0
      },
      {
        "tier_id": "OUT-OF-NETWORK",
        "tier_name": "Out-of-Network",
        "tier_level": 2,
        "cost_sharing_modifier": 2.0
      }
    ]
  },
  
  "access_requirements": {
    "pcp_required": false,
    "referral_required": false,
    "preauthorization_required": true,
    "out_of_network_coverage": true
  },
  
  "out_of_network_rules": {
    "reimbursement_methodology": "UCR",
    "ucr_percentile": 80,
    "balance_billing": {
      "allowed": true,
      "surprise_billing_protection": "Federal NSA"
    },
    "deductible_separate": true,
    "coinsurance": 0.40
  },
  
  "provider_counts": {
    "total_providers": 45000,
    "primary_care": 8500,
    "specialists": 28000,
    "facilities": 220,
    "pharmacies": 3200
  },
  
  "contracted_systems": [
    {"system_name": "Northwestern Medicine", "contract_type": "Full"},
    {"system_name": "Advocate Aurora", "contract_type": "Full"},
    {"system_name": "Rush System", "contract_type": "Full"},
    {"system_name": "OSF Healthcare", "contract_type": "Full"},
    {"system_name": "Carle Health", "contract_type": "Full"}
  ],
  
  "bluecard_access": {
    "enabled": true,
    "national_network": "BlueCard PPO",
    "traveling_member": true
  }
}
```

---

## Validation Checklist

When using this pattern, verify:

| Requirement | Validation |
|-------------|------------|
| PCP Required | Must be `false` for PPO |
| Referral Required | Must be `false` for PPO |
| OON Coverage | Must be `true` for PPO |
| Tier Count | Minimum 2 (In-Network, Out-of-Network) |
| OON Deductible | Typically 2× in-network |
| OON Coinsurance | Typically 40-50% |
| Balance Billing | Document member responsibility |

---

## Related Skills

- [Network Types](../reference/network-types.md) - PPO definition and concepts
- [Synthetic Network](../synthetic/synthetic-network.md) - Generate network from pattern
- [HMO Network Pattern](hmo-network-pattern.md) - Contrast with gatekeeper model
- [Tiered Network Pattern](tiered-network-pattern.md) - Add performance tiers

---

*PPO Network Pattern is a template skill in the NetworkSim product.*
