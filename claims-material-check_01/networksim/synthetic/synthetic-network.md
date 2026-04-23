---
name: synthetic-network
description: |
  Generate realistic synthetic provider network configurations including
  network type, provider/facility rosters, geographic coverage, and
  access standards. Creates complete network definitions for testing.
  
  Trigger phrases: "generate network", "create provider network",
  "PPO network", "HMO network", "narrow network", "tiered network",
  "network configuration", "provider roster", "network for plan"
version: "1.0"
category: synthetic
related_skills:
  - network-types
  - network-adequacy
  - synthetic-provider
  - synthetic-facility
cross_product:
  - membersim: Network status for claims adjudication
  - patientsim: In-network vs out-of-network encounters
---

# Synthetic Network Generation

## Overview

Generate realistic synthetic provider network configurations for health plans. Networks define which providers and facilities are contracted to serve members, at what reimbursement levels, and with what access standards.

This skill generates the **canonical network entity** that includes:
- Network definition and type
- Provider/facility roster structure
- Geographic coverage area
- Access and adequacy metrics
- Tiering configuration (if applicable)

---

## Trigger Phrases

Use this skill when you see:
- "Generate a provider network"
- "Create a PPO network for Texas"
- "Generate an HMO network configuration"
- "Create a narrow network for an exchange plan"
- "Generate a tiered network"
- "Create a network roster"
- "Generate network coverage for this plan"

---

## Network Configuration Types

### By Access Model

| Type | Provider Choice | Referral Required | OON Coverage | Use Case |
|------|-----------------|-------------------|--------------|----------|
| HMO | Closed network | Yes (PCP gatekeeper) | None/Emergency | Cost control |
| PPO | Open network | No | Reduced benefit | Flexibility |
| EPO | Closed network | No | None/Emergency | Middle ground |
| POS | Hybrid | At point of service | If no referral | Choice |

### By Network Breadth

| Type | Provider % | Premium Impact | Member Impact |
|------|------------|----------------|---------------|
| Broad | 80-95% of market | Higher | Maximum choice |
| Standard | 60-80% of market | Moderate | Good choice |
| Narrow | 30-60% of market | Lower | Limited choice |
| Ultra-Narrow | <30% of market | Lowest | Restricted |

### By Tier Structure

| Type | Tiers | Cost Sharing Variation | Complexity |
|------|-------|------------------------|------------|
| Single Tier | 1 | None | Simple |
| Two-Tier | 2 | Preferred vs Standard | Common |
| Three-Tier | 3 | High Performance, Preferred, Standard | Complex |
| Value-Based | Variable | Quality/cost based | Most complex |

---

## Canonical Schema

### Network Definition

```json
{
  "network_id": "string",
  "network_name": "string",
  "network_type": "HMO | PPO | EPO | POS",
  "network_breadth": "Broad | Standard | Narrow | Ultra-Narrow",
  "effective_date": "YYYY-MM-DD",
  "termination_date": "YYYY-MM-DD | null",
  "status": "Active | Pending | Terminated",
  "description": "string",
  "payer": {
    "payer_id": "string",
    "payer_name": "string",
    "line_of_business": "Commercial | Medicare | Medicaid | Exchange"
  },
  "geographic_coverage": {
    "coverage_type": "National | Regional | State | Local",
    "states": ["string (2 char)"],
    "counties": [
      {
        "state": "string",
        "county_fips": "string",
        "county_name": "string"
      }
    ],
    "zip_codes": ["string"],
    "msas": ["string (CBSA code)"]
  },
  "tier_structure": {
    "tier_count": "integer (1-4)",
    "tiers": [
      {
        "tier_id": "string",
        "tier_name": "string",
        "tier_level": "integer",
        "description": "string",
        "cost_sharing_modifier": "number (1.0 = base)",
        "criteria": {
          "quality_threshold": "number (optional)",
          "cost_threshold": "number (optional)",
          "designation": "string (optional)"
        }
      }
    ]
  },
  "access_requirements": {
    "pcp_required": "boolean",
    "referral_required": "boolean",
    "preauthorization_required": "boolean",
    "out_of_network_coverage": "boolean",
    "oon_cost_sharing": {
      "deductible_separate": "boolean",
      "coinsurance_rate": "number (0-1)",
      "oop_max_separate": "boolean"
    }
  },
  "adequacy_standards": {
    "primary_care": {
      "time_minutes": "integer",
      "distance_miles": "number",
      "provider_ratio": "string (e.g., 1:2000)"
    },
    "specialty": {
      "time_minutes": "integer",
      "distance_miles": "number"
    },
    "hospital": {
      "time_minutes": "integer",
      "distance_miles": "number"
    },
    "pharmacy": {
      "time_minutes": "integer",
      "distance_miles": "number"
    }
  },
  "provider_counts": {
    "total_providers": "integer",
    "primary_care": "integer",
    "specialists": "integer",
    "facilities": "integer",
    "pharmacies": "integer"
  },
  "contracted_systems": [
    {
      "system_id": "string",
      "system_name": "string",
      "contract_type": "Full | Partial | Anchor",
      "tier": "string (tier_id)"
    }
  ],
  "excluded_providers": {
    "exclusion_count": "integer",
    "exclusion_reasons": ["string"]
  },
  "network_management": {
    "credentialing_entity": "string",
    "recredentialing_cycle_months": "integer",
    "directory_update_frequency": "string"
  }
}
```

### Network Roster Entry

```json
{
  "roster_entry_id": "string",
  "network_id": "string",
  "provider_type": "Individual | Organization | Facility",
  "provider": {
    "npi": "string",
    "name": "string",
    "taxonomy_code": "string",
    "specialty": "string"
  },
  "contract": {
    "effective_date": "YYYY-MM-DD",
    "termination_date": "YYYY-MM-DD | null",
    "status": "Active | Pending | Terminated",
    "contract_type": "Par | Non-Par | Value-Based",
    "tier_assignment": "string (tier_id)",
    "fee_schedule": "string (fee schedule reference)"
  },
  "practice_locations": [
    {
      "location_id": "string",
      "address": {
        "street_address": "string",
        "city": "string",
        "state": "string",
        "zip": "string",
        "county_fips": "string"
      },
      "accepting_new_patients": "boolean",
      "age_restrictions": {
        "min_age": "integer | null",
        "max_age": "integer | null"
      },
      "gender_restrictions": "M | F | null",
      "panel_status": "Open | Limited | Closed",
      "hours": "string"
    }
  ],
  "hospital_affiliations": [
    {
      "facility_npi": "string",
      "facility_name": "string",
      "privileges": ["string"]
    }
  ],
  "languages": ["string"],
  "accepting_medicaid": "boolean",
  "accepting_medicare": "boolean",
  "telehealth_available": "boolean",
  "pcp_eligible": "boolean",
  "quality_designations": [
    {
      "program": "string",
      "designation": "string",
      "effective_date": "YYYY-MM-DD"
    }
  ]
}
```

---

## Generation Parameters

### Required Context

| Parameter | Description | Default |
|-----------|-------------|---------|
| **network_type** | HMO, PPO, EPO, POS | PPO |
| **geography** | States, counties, or MSAs | Single state |

### Optional Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **breadth** | Broad, Standard, Narrow | Standard |
| **tier_count** | 1-4 tiers | 1 (single tier) |
| **line_of_business** | Commercial, Medicare, etc. | Commercial |
| **payer** | Specific payer | Generic |
| **include_roster** | Generate sample roster | false |
| **roster_size** | Number of roster entries | 50 |

---

## Examples

### Example 1: Standard PPO Network

**Prompt**: "Generate a PPO network for Arizona"

**Response**:

```json
{
  "network_id": "AZ-PPO-2024-001",
  "network_name": "Arizona Choice PPO",
  "network_type": "PPO",
  "network_breadth": "Standard",
  "effective_date": "2024-01-01",
  "termination_date": null,
  "status": "Active",
  "description": "Standard PPO network covering all Arizona counties with broad provider access",
  "payer": {
    "payer_id": "BCBS-AZ",
    "payer_name": "Blue Cross Blue Shield of Arizona",
    "line_of_business": "Commercial"
  },
  "geographic_coverage": {
    "coverage_type": "State",
    "states": ["AZ"],
    "counties": [
      {"state": "AZ", "county_fips": "04013", "county_name": "Maricopa"},
      {"state": "AZ", "county_fips": "04019", "county_name": "Pima"},
      {"state": "AZ", "county_fips": "04005", "county_name": "Coconino"},
      {"state": "AZ", "county_fips": "04027", "county_name": "Yuma"}
    ],
    "msas": ["38060", "46060"]
  },
  "tier_structure": {
    "tier_count": 1,
    "tiers": [
      {
        "tier_id": "STANDARD",
        "tier_name": "In-Network",
        "tier_level": 1,
        "description": "All contracted providers",
        "cost_sharing_modifier": 1.0
      }
    ]
  },
  "access_requirements": {
    "pcp_required": false,
    "referral_required": false,
    "preauthorization_required": true,
    "out_of_network_coverage": true,
    "oon_cost_sharing": {
      "deductible_separate": true,
      "coinsurance_rate": 0.50,
      "oop_max_separate": true
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
    },
    "pharmacy": {
      "time_minutes": 15,
      "distance_miles": 5
    }
  },
  "provider_counts": {
    "total_providers": 12500,
    "primary_care": 2800,
    "specialists": 6200,
    "facilities": 85,
    "pharmacies": 890
  },
  "contracted_systems": [
    {
      "system_id": "BANNER",
      "system_name": "Banner Health",
      "contract_type": "Full",
      "tier": "STANDARD"
    },
    {
      "system_id": "HCC",
      "system_name": "HonorHealth",
      "contract_type": "Full",
      "tier": "STANDARD"
    },
    {
      "system_id": "DIG",
      "system_name": "Dignity Health",
      "contract_type": "Full",
      "tier": "STANDARD"
    }
  ],
  "network_management": {
    "credentialing_entity": "BCBS Arizona",
    "recredentialing_cycle_months": 36,
    "directory_update_frequency": "Monthly"
  }
}
```

---

### Example 2: Tiered HMO Network

**Prompt**: "Generate a tiered HMO network for Los Angeles with quality-based tiers"

**Response**:

```json
{
  "network_id": "CA-HMO-TIER-2024-001",
  "network_name": "Select Care Tiered HMO",
  "network_type": "HMO",
  "network_breadth": "Standard",
  "effective_date": "2024-01-01",
  "status": "Active",
  "description": "Quality-tiered HMO with cost incentives for high-performing providers",
  "payer": {
    "payer_id": "KP-SCAL",
    "payer_name": "Kaiser Permanente Southern California",
    "line_of_business": "Commercial"
  },
  "geographic_coverage": {
    "coverage_type": "Regional",
    "states": ["CA"],
    "counties": [
      {"state": "CA", "county_fips": "06037", "county_name": "Los Angeles"},
      {"state": "CA", "county_fips": "06059", "county_name": "Orange"},
      {"state": "CA", "county_fips": "06065", "county_name": "Riverside"},
      {"state": "CA", "county_fips": "06071", "county_name": "San Bernardino"}
    ],
    "msas": ["31080", "40140"]
  },
  "tier_structure": {
    "tier_count": 3,
    "tiers": [
      {
        "tier_id": "T1-ELITE",
        "tier_name": "Elite Tier",
        "tier_level": 1,
        "description": "Top quality and efficiency performers",
        "cost_sharing_modifier": 0.75,
        "criteria": {
          "quality_threshold": 90,
          "cost_threshold": 0.90,
          "designation": "Blue Distinction Center+"
        }
      },
      {
        "tier_id": "T2-PREFERRED",
        "tier_name": "Preferred Tier",
        "tier_level": 2,
        "description": "Above-average quality and efficiency",
        "cost_sharing_modifier": 1.0,
        "criteria": {
          "quality_threshold": 75,
          "cost_threshold": 1.05
        }
      },
      {
        "tier_id": "T3-STANDARD",
        "tier_name": "Standard Tier",
        "tier_level": 3,
        "description": "Meets minimum network standards",
        "cost_sharing_modifier": 1.5,
        "criteria": {
          "quality_threshold": 50,
          "cost_threshold": 1.20
        }
      }
    ]
  },
  "access_requirements": {
    "pcp_required": true,
    "referral_required": true,
    "preauthorization_required": true,
    "out_of_network_coverage": false,
    "oon_cost_sharing": null
  },
  "adequacy_standards": {
    "primary_care": {
      "time_minutes": 10,
      "distance_miles": 5,
      "provider_ratio": "1:1500"
    },
    "specialty": {
      "time_minutes": 20,
      "distance_miles": 15
    },
    "hospital": {
      "time_minutes": 20,
      "distance_miles": 15
    }
  },
  "provider_counts": {
    "total_providers": 8500,
    "primary_care": 2200,
    "specialists": 4100,
    "facilities": 65,
    "pharmacies": 420
  },
  "tier_distribution": {
    "T1-ELITE": {"providers": 1275, "percentage": 0.15},
    "T2-PREFERRED": {"providers": 4250, "percentage": 0.50},
    "T3-STANDARD": {"providers": 2975, "percentage": 0.35}
  }
}
```

---

### Example 3: Narrow Network for ACA Exchange

**Prompt**: "Generate a narrow network for an ACA exchange plan in Georgia"

**Response**:

```json
{
  "network_id": "GA-EXCH-NAR-2024-001",
  "network_name": "Essential Care Network",
  "network_type": "EPO",
  "network_breadth": "Narrow",
  "effective_date": "2024-01-01",
  "status": "Active",
  "description": "Cost-effective narrow network for Marketplace plans",
  "payer": {
    "payer_id": "AMB-GA",
    "payer_name": "Ambetter of Georgia",
    "line_of_business": "Exchange"
  },
  "geographic_coverage": {
    "coverage_type": "State",
    "states": ["GA"],
    "counties": [
      {"state": "GA", "county_fips": "13121", "county_name": "Fulton"},
      {"state": "GA", "county_fips": "13089", "county_name": "DeKalb"},
      {"state": "GA", "county_fips": "13135", "county_name": "Gwinnett"},
      {"state": "GA", "county_fips": "13067", "county_name": "Cobb"},
      {"state": "GA", "county_fips": "13063", "county_name": "Clayton"}
    ],
    "msas": ["12060"]
  },
  "tier_structure": {
    "tier_count": 1,
    "tiers": [
      {
        "tier_id": "IN-NETWORK",
        "tier_name": "In-Network Only",
        "tier_level": 1,
        "description": "Contracted providers only; no OON except emergency",
        "cost_sharing_modifier": 1.0
      }
    ]
  },
  "access_requirements": {
    "pcp_required": false,
    "referral_required": false,
    "preauthorization_required": true,
    "out_of_network_coverage": false,
    "oon_cost_sharing": null
  },
  "adequacy_standards": {
    "primary_care": {
      "time_minutes": 15,
      "distance_miles": 10,
      "provider_ratio": "1:2500"
    },
    "specialty": {
      "time_minutes": 45,
      "distance_miles": 45
    },
    "hospital": {
      "time_minutes": 30,
      "distance_miles": 30
    }
  },
  "provider_counts": {
    "total_providers": 3200,
    "primary_care": 780,
    "specialists": 1650,
    "facilities": 22,
    "pharmacies": 185
  },
  "contracted_systems": [
    {
      "system_id": "GRADY",
      "system_name": "Grady Health System",
      "contract_type": "Anchor",
      "tier": "IN-NETWORK"
    },
    {
      "system_id": "WH-ATL",
      "system_name": "Wellstar Health System",
      "contract_type": "Partial",
      "tier": "IN-NETWORK"
    }
  ],
  "essential_community_providers": {
    "fqhc_count": 12,
    "rhc_count": 0,
    "dsh_hospital_count": 3,
    "ecp_percentage": 0.35
  },
  "excluded_providers": {
    "exclusion_count": 8500,
    "exclusion_reasons": [
      "Cost efficiency threshold not met",
      "Quality metrics below standard",
      "Geographic redundancy"
    ]
  }
}
```

---

### Example 4: Medicare Advantage Network

**Prompt**: "Generate a Medicare Advantage PPO network for Florida"

**Response**:

```json
{
  "network_id": "FL-MA-PPO-2024-001",
  "network_name": "Medicare Choice PPO",
  "network_type": "PPO",
  "network_breadth": "Broad",
  "effective_date": "2024-01-01",
  "status": "Active",
  "description": "Comprehensive Medicare Advantage PPO with national PFFS OON coverage",
  "payer": {
    "payer_id": "HUM-FL",
    "payer_name": "Humana",
    "line_of_business": "Medicare"
  },
  "geographic_coverage": {
    "coverage_type": "State",
    "states": ["FL"],
    "counties": [
      {"state": "FL", "county_fips": "12086", "county_name": "Miami-Dade"},
      {"state": "FL", "county_fips": "12011", "county_name": "Broward"},
      {"state": "FL", "county_fips": "12099", "county_name": "Palm Beach"},
      {"state": "FL", "county_fips": "12057", "county_name": "Hillsborough"},
      {"state": "FL", "county_fips": "12095", "county_name": "Orange"}
    ]
  },
  "tier_structure": {
    "tier_count": 2,
    "tiers": [
      {
        "tier_id": "IN-NETWORK",
        "tier_name": "In-Network",
        "tier_level": 1,
        "description": "Contracted providers",
        "cost_sharing_modifier": 1.0
      },
      {
        "tier_id": "OUT-OF-NETWORK",
        "tier_name": "Out-of-Network",
        "tier_level": 2,
        "description": "Non-contracted Medicare providers",
        "cost_sharing_modifier": 1.5
      }
    ]
  },
  "access_requirements": {
    "pcp_required": false,
    "referral_required": false,
    "preauthorization_required": true,
    "out_of_network_coverage": true,
    "oon_cost_sharing": {
      "deductible_separate": false,
      "coinsurance_rate": 0.40,
      "oop_max_separate": false
    }
  },
  "adequacy_standards": {
    "primary_care": {
      "time_minutes": 10,
      "distance_miles": 5,
      "provider_ratio": "1:1500"
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
  "provider_counts": {
    "total_providers": 45000,
    "primary_care": 8500,
    "specialists": 22000,
    "facilities": 320,
    "pharmacies": 4200
  },
  "medicare_specific": {
    "cms_contract_id": "H1234",
    "plan_benefit_package": "001",
    "star_rating": 4,
    "snp_type": null,
    "dsnp_medicaid_states": []
  }
}
```

---

## Cross-Product Integration

### MemberSim Integration

Network determines claim adjudication:

```
MemberSim Claim → NetworkSim Network → Adjudication Rules

Network provides:
- In-network vs out-of-network status
- Tier assignment for cost sharing
- Access requirements (referral, preauth)
```

### PatientSim Integration

Network constrains provider selection:

```
PatientSim Encounter → NetworkSim Network → Provider Pool

Network provides:
- Available providers in network
- PCP panel for HMO
- Referral requirements
```

---

## Validation Rules

### Network Validation

| Rule | Validation |
|------|------------|
| Network ID | Unique identifier format |
| Dates | Effective ≤ Termination if both present |
| Coverage | At least one state or county |

### Tier Validation

| Rule | Validation |
|------|------------|
| Tier Count | 1-4 tiers |
| Tier Levels | Sequential 1, 2, 3... |
| Modifier | > 0, typically 0.5-2.0 |

### Adequacy Validation

| Rule | Validation |
|------|------------|
| Time/Distance | Must meet CMS minimums |
| Provider Ratios | Industry standard ranges |

---

## Related Skills

- [Network Types](../reference/network-types.md) - Network type definitions
- [Network Adequacy](../reference/network-adequacy.md) - Access standards
- [Synthetic Provider](synthetic-provider.md) - Generate roster providers
- [Synthetic Plan](synthetic-plan.md) - Plan using this network

---

*Synthetic Network is a generation skill in the NetworkSim product.*
