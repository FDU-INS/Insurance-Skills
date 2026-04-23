# Plan Canonical Model

The canonical data model for health plan benefit structures in NetworkSim.

## Overview

A Plan represents a configured set of benefits including medical, pharmacy, and ancillary coverage. Plans define cost sharing, coverage limits, and network requirements.

## Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Plan",
  "type": "object",
  "required": ["plan_id", "name", "network_id", "effective_date"],
  "properties": {
    "plan_id": {
      "type": "string",
      "pattern": "^PLAN-[A-Z]{3}-[0-9]{4}$"
    },
    "name": { "type": "string" },
    "network_id": { "type": "string" },
    "metal_tier": {
      "type": "string",
      "enum": ["Bronze", "Silver", "Gold", "Platinum", "Catastrophic"]
    },
    "actuarial_value": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "medical_benefits": {
      "type": "object",
      "properties": {
        "deductible": {
          "type": "object",
          "properties": {
            "individual": { "type": "number" },
            "family": { "type": "number" }
          }
        },
        "out_of_pocket_max": {
          "type": "object",
          "properties": {
            "individual": { "type": "number" },
            "family": { "type": "number" }
          }
        },
        "copays": {
          "type": "object",
          "properties": {
            "pcp_visit": { "type": "number" },
            "specialist_visit": { "type": "number" },
            "urgent_care": { "type": "number" },
            "er_visit": { "type": "number" }
          }
        },
        "coinsurance": {
          "type": "object",
          "properties": {
            "in_network": { "type": "number" },
            "out_of_network": { "type": "number" }
          }
        }
      }
    },
    "pharmacy_benefits": {
      "type": "object",
      "properties": {
        "formulary_id": { "type": "string" },
        "tiers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "tier": { "type": "integer" },
              "name": { "type": "string" },
              "retail_30_copay": { "type": "number" },
              "retail_90_copay": { "type": "number" },
              "mail_90_copay": { "type": "number" }
            }
          }
        },
        "specialty_coinsurance": { "type": "number" },
        "specialty_max": { "type": "number" }
      }
    },
    "effective_date": { "type": "string", "format": "date" },
    "termination_date": { "type": "string", "format": "date" }
  }
}
```

## Example

### Gold PPO Plan

```json
{
  "plan_id": "PLAN-PPO-0001",
  "name": "Gold PPO 500",
  "network_id": "NETWORK-PPO-0001",
  "metal_tier": "Gold",
  "actuarial_value": 0.80,
  "medical_benefits": {
    "deductible": {
      "individual": 500,
      "family": 1000
    },
    "out_of_pocket_max": {
      "individual": 4000,
      "family": 8000
    },
    "copays": {
      "pcp_visit": 25,
      "specialist_visit": 50,
      "urgent_care": 75,
      "er_visit": 250
    },
    "coinsurance": {
      "in_network": 0.20,
      "out_of_network": 0.40
    }
  },
  "pharmacy_benefits": {
    "formulary_id": "FORM-STD-2025",
    "tiers": [
      { "tier": 1, "name": "Generic", "retail_30_copay": 10, "mail_90_copay": 25 },
      { "tier": 2, "name": "Preferred Brand", "retail_30_copay": 35, "mail_90_copay": 87 },
      { "tier": 3, "name": "Non-Preferred", "retail_30_copay": 70, "mail_90_copay": 175 },
      { "tier": 4, "name": "Specialty", "retail_30_copay": null, "mail_90_copay": null }
    ],
    "specialty_coinsurance": 0.20,
    "specialty_max": 250
  },
  "effective_date": "2025-01-01"
}
```

## Metal Tier Actuarial Values

| Tier | AV Range | Typical Deductible |
|------|----------|-------------------|
| Platinum | 88-92% | $0-500 |
| Gold | 78-82% | $500-1,500 |
| Silver | 68-72% | $2,000-4,000 |
| Bronze | 58-62% | $5,000-8,000 |
| Catastrophic | <60% | >$8,000 |

## Cross-Product Usage

### MemberSim
- Cost share calculations
- Accumulator tracking
- COB determination

### RxMemberSim
- Tier assignment
- Copay calculations
- DAW penalties

## Related Models

- [Network Model](network-model.md) - Provider access
- [Pharmacy Model](pharmacy-model.md) - Pharmacy network
