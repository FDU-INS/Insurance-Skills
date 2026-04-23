# Network Canonical Model

The canonical data model for provider networks in NetworkSim.

## Overview

A Network represents a configured set of providers, facilities, and pharmacies that provide care to health plan members. Networks define access rules, tier structures, and adequacy requirements.

## Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Network",
  "type": "object",
  "required": ["network_id", "name", "type", "effective_date"],
  "properties": {
    "network_id": {
      "type": "string",
      "pattern": "^NETWORK-[A-Z]{3}-[0-9]{4}$"
    },
    "name": {
      "type": "string"
    },
    "type": {
      "type": "string",
      "enum": ["HMO", "PPO", "EPO", "POS", "HDHP", "Medicare_Advantage", "Medicaid"]
    },
    "product_line": {
      "type": "string",
      "enum": ["commercial", "medicare", "medicaid", "exchange"]
    },
    "service_area": {
      "type": "object",
      "properties": {
        "states": {
          "type": "array",
          "items": { "type": "string", "pattern": "^[A-Z]{2}$" }
        },
        "counties": {
          "type": "array",
          "items": { "type": "string", "pattern": "^[0-9]{5}$" }
        },
        "zip_codes": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "tier_structure": {
      "type": "object",
      "properties": {
        "tier_count": { "type": "integer", "minimum": 1, "maximum": 4 },
        "tiers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "tier_number": { "type": "integer" },
              "name": { "type": "string" },
              "cost_share_multiplier": { "type": "number" }
            }
          }
        }
      }
    },
    "adequacy_standards": {
      "type": "object",
      "properties": {
        "standard": {
          "type": "string",
          "enum": ["CMS_MA", "NCQA", "State_Medicaid", "Custom"]
        },
        "pcp_ratio": { "type": "number", "description": "Members per PCP" },
        "time_distance": {
          "type": "object",
          "properties": {
            "urban_miles": { "type": "number" },
            "suburban_miles": { "type": "number" },
            "rural_miles": { "type": "number" }
          }
        }
      }
    },
    "effective_date": {
      "type": "string",
      "format": "date"
    },
    "termination_date": {
      "type": "string",
      "format": "date"
    },
    "status": {
      "type": "string",
      "enum": ["active", "pending", "terminated"]
    },
    "roster": {
      "type": "object",
      "properties": {
        "providers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "npi": { "type": "string" },
              "tier": { "type": "integer" },
              "effective_date": { "type": "string", "format": "date" },
              "termination_date": { "type": "string", "format": "date" },
              "accepting_new_patients": { "type": "boolean" }
            }
          }
        },
        "facilities": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "ccn": { "type": "string" },
              "tier": { "type": "integer" }
            }
          }
        },
        "pharmacies": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "ncpdp_id": { "type": "string" },
              "type": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

## Example

### PPO Network

```json
{
  "network_id": "NETWORK-PPO-0001",
  "name": "Blue Cross Preferred PPO",
  "type": "PPO",
  "product_line": "commercial",
  "service_area": {
    "states": ["TX"],
    "counties": ["48201", "48157", "48339"]
  },
  "tier_structure": {
    "tier_count": 2,
    "tiers": [
      { "tier_number": 1, "name": "Preferred", "cost_share_multiplier": 1.0 },
      { "tier_number": 2, "name": "Standard", "cost_share_multiplier": 1.5 }
    ]
  },
  "adequacy_standards": {
    "standard": "NCQA",
    "pcp_ratio": 1500,
    "time_distance": {
      "urban_miles": 10,
      "suburban_miles": 20,
      "rural_miles": 35
    }
  },
  "effective_date": "2025-01-01",
  "status": "active"
}
```

### Medicare Advantage Network

```json
{
  "network_id": "NETWORK-MA-0042",
  "name": "Aetna Medicare Preferred",
  "type": "Medicare_Advantage",
  "product_line": "medicare",
  "service_area": {
    "states": ["FL"],
    "counties": ["12086", "12011", "12099"]
  },
  "tier_structure": {
    "tier_count": 1,
    "tiers": [
      { "tier_number": 1, "name": "In-Network", "cost_share_multiplier": 1.0 }
    ]
  },
  "adequacy_standards": {
    "standard": "CMS_MA",
    "pcp_ratio": 1200,
    "time_distance": {
      "urban_miles": 10,
      "suburban_miles": 20,
      "rural_miles": 30
    }
  },
  "effective_date": "2025-01-01",
  "status": "active"
}
```

## Network Type Comparison

| Type | In-Network | Out-of-Network | Referrals |
|------|------------|----------------|-----------|
| HMO | Required | Emergency only | Required |
| PPO | Lower cost | Higher cost | Not required |
| EPO | Required | Emergency only | Not required |
| POS | Lower cost | Higher cost | For specialists |

## Cross-Product Usage

### MemberSim
- Network status on claims
- Cost share calculations
- Provider directory generation

### RxMemberSim  
- Pharmacy network determination
- Specialty pharmacy routing
- Mail-order eligibility

## Related Models

- [Provider Model](provider-model.md) - Network roster members
- [Facility Model](facility-model.md) - Contracted facilities
- [Pharmacy Model](pharmacy-model.md) - Pharmacy network
- [Plan Model](plan-model.md) - Benefit design
