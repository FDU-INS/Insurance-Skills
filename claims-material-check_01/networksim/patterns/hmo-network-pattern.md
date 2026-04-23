---
name: hmo-network-pattern
description: |
  Reusable HMO network configuration pattern with gatekeeper model,
  closed network, referral requirements, and capitation-ready structures.
  Use as starting template for HMO network generation.
  
  Trigger phrases: "HMO network pattern", "gatekeeper model", "closed network template",
  "HMO configuration", "capitated network", "staff model HMO"
version: "1.0"
category: patterns
related_skills:
  - network-types
  - synthetic-network
  - synthetic-plan
---

# HMO Network Pattern

## Overview

This pattern provides a reusable template for generating HMO (Health Maintenance Organization) network configurations. HMOs use a gatekeeper model where members must select a Primary Care Physician (PCP) who coordinates all care and provides referrals to specialists.

Use this pattern when you need:
- Closed network configuration
- PCP gatekeeper requirements
- Referral-based specialist access
- Capitation-ready provider structures

---

## Pattern Variants

### Staff Model HMO

Physicians are employed directly by the HMO.

```json
{
  "pattern_id": "HMO-STAFF",
  "pattern_name": "Staff Model HMO",
  "characteristics": {
    "provider_relationship": "Employed",
    "facility_ownership": "HMO-owned",
    "integration_level": "Fully integrated",
    "geographic_focus": "Single market"
  },
  "network_configuration": {
    "network_type": "HMO",
    "network_breadth": "Narrow",
    "pcp_required": true,
    "referral_required": true,
    "out_of_network_coverage": false,
    "single_entity": true
  },
  "provider_structure": {
    "pcp_model": "Employed physicians",
    "specialist_model": "Employed physicians",
    "facility_model": "Owned medical centers",
    "ancillary_model": "In-house services"
  },
  "payment_model": {
    "pcp_payment": "Salary + quality bonus",
    "specialist_payment": "Salary",
    "capitation": "Global budget",
    "risk_sharing": "Full organization risk"
  },
  "examples": ["Kaiser Permanente", "Group Health (historical)"]
}
```

### Group Model HMO

HMO contracts exclusively with a single multi-specialty group.

```json
{
  "pattern_id": "HMO-GROUP",
  "pattern_name": "Group Model HMO",
  "characteristics": {
    "provider_relationship": "Exclusive contract",
    "facility_ownership": "Mixed (HMO + group)",
    "integration_level": "High integration",
    "geographic_focus": "Regional"
  },
  "network_configuration": {
    "network_type": "HMO",
    "network_breadth": "Narrow",
    "pcp_required": true,
    "referral_required": true,
    "out_of_network_coverage": false
  },
  "provider_structure": {
    "pcp_model": "Medical group employed",
    "specialist_model": "Medical group employed",
    "facility_model": "Contracted hospitals",
    "ancillary_model": "Mixed in-house and contracted"
  },
  "payment_model": {
    "pcp_payment": "Capitation to group",
    "specialist_payment": "Internal group allocation",
    "capitation": "Professional capitation",
    "risk_sharing": "Group assumes professional risk"
  },
  "examples": ["HealthPartners", "Geisinger"]
}
```

### IPA Model HMO

HMO contracts with Independent Practice Association of private physicians.

```json
{
  "pattern_id": "HMO-IPA",
  "pattern_name": "IPA Model HMO",
  "characteristics": {
    "provider_relationship": "IPA contract",
    "facility_ownership": "Contracted",
    "integration_level": "Moderate integration",
    "geographic_focus": "Multi-market"
  },
  "network_configuration": {
    "network_type": "HMO",
    "network_breadth": "Standard",
    "pcp_required": true,
    "referral_required": true,
    "out_of_network_coverage": false
  },
  "provider_structure": {
    "pcp_model": "IPA member physicians",
    "specialist_model": "IPA member + contracted",
    "facility_model": "Contracted hospitals",
    "ancillary_model": "Contracted network"
  },
  "payment_model": {
    "pcp_payment": "Capitation or fee-for-service",
    "specialist_payment": "Fee-for-service with withhold",
    "capitation": "Primary care capitation",
    "risk_sharing": "IPA risk pools"
  },
  "examples": ["Many regional HMOs"]
}
```

### Network Model HMO

HMO contracts with multiple medical groups and IPAs.

```json
{
  "pattern_id": "HMO-NETWORK",
  "pattern_name": "Network Model HMO",
  "characteristics": {
    "provider_relationship": "Multiple contracts",
    "facility_ownership": "Contracted",
    "integration_level": "Variable",
    "geographic_focus": "Broad geographic"
  },
  "network_configuration": {
    "network_type": "HMO",
    "network_breadth": "Standard to Broad",
    "pcp_required": true,
    "referral_required": true,
    "out_of_network_coverage": false
  },
  "provider_structure": {
    "pcp_model": "Multiple groups and IPAs",
    "specialist_model": "Multiple groups and direct contracts",
    "facility_model": "Multiple hospital systems",
    "ancillary_model": "Broad contracted network"
  },
  "payment_model": {
    "pcp_payment": "Varies by group",
    "specialist_payment": "Varies by group",
    "capitation": "Delegated to groups",
    "risk_sharing": "Varied risk arrangements"
  },
  "examples": ["Aetna HMO", "United HMO", "Cigna HMO"]
}
```

---

## Template Configuration

### Base HMO Network Template

```json
{
  "network_id": "{{NETWORK_ID}}",
  "network_name": "{{PAYER_NAME}} HMO Network",
  "network_type": "HMO",
  "network_breadth": "{{Standard | Narrow}}",
  "effective_date": "{{YYYY-MM-DD}}",
  "status": "Active",
  
  "payer": {
    "payer_id": "{{PAYER_ID}}",
    "payer_name": "{{PAYER_NAME}}",
    "line_of_business": "{{Commercial | Medicare | Medicaid}}"
  },
  
  "geographic_coverage": {
    "coverage_type": "{{State | Regional | Local}}",
    "states": ["{{STATE_CODES}}"],
    "counties": [
      {
        "state": "{{STATE}}",
        "county_fips": "{{FIPS}}",
        "county_name": "{{COUNTY}}"
      }
    ]
  },
  
  "tier_structure": {
    "tier_count": 1,
    "tiers": [
      {
        "tier_id": "IN-NETWORK",
        "tier_name": "In-Network Only",
        "tier_level": 1,
        "description": "Must use network providers except emergency",
        "cost_sharing_modifier": 1.0
      }
    ]
  },
  
  "access_requirements": {
    "pcp_required": true,
    "pcp_selection": {
      "required": true,
      "auto_assignment": true,
      "change_frequency": "Monthly",
      "effective_date_rules": "First of next month"
    },
    "referral_required": true,
    "referral_rules": {
      "self_referral_allowed": ["OB/GYN", "Mental Health", "Preventive"],
      "standing_referral": true,
      "specialist_as_pcp": false,
      "validity_period_days": 90
    },
    "preauthorization_required": true,
    "out_of_network_coverage": false,
    "emergency_exception": true
  },
  
  "adequacy_standards": {
    "primary_care": {
      "time_minutes": 10,
      "distance_miles": 5,
      "provider_ratio": "1:1500",
      "appointment_standard_days": 5
    },
    "specialty": {
      "time_minutes": 30,
      "distance_miles": 30,
      "appointment_standard_days": 15
    },
    "hospital": {
      "time_minutes": 30,
      "distance_miles": 30
    },
    "behavioral_health": {
      "time_minutes": 20,
      "distance_miles": 20,
      "appointment_standard_days": 10
    }
  },
  
  "pcp_panel_management": {
    "panel_size_target": 2000,
    "panel_size_max": 2500,
    "age_adjusted": true,
    "acuity_adjusted": true,
    "new_patient_acceptance": {
      "tracking": true,
      "minimum_open_pcps_percentage": 0.20
    }
  },
  
  "care_management": {
    "care_coordination": true,
    "disease_management": true,
    "case_management": true,
    "utilization_management": true,
    "quality_programs": ["HEDIS", "CAHPS", "Stars"]
  }
}
```

---

## PCP Configuration Template

```json
{
  "pcp_requirements": {
    "eligible_specialties": [
      {"taxonomy": "207Q00000X", "name": "Family Medicine"},
      {"taxonomy": "207R00000X", "name": "Internal Medicine"},
      {"taxonomy": "208000000X", "name": "Pediatrics"},
      {"taxonomy": "207V00000X", "name": "Obstetrics & Gynecology"},
      {"taxonomy": "363L00000X", "name": "Nurse Practitioner"},
      {"taxonomy": "363A00000X", "name": "Physician Assistant"}
    ],
    "credentialing": {
      "board_certification_required": false,
      "hospital_privileges_required": false,
      "ehr_required": true,
      "quality_reporting_required": true
    },
    "practice_requirements": {
      "minimum_hours_per_week": 20,
      "after_hours_coverage": true,
      "weekend_availability": "Preferred",
      "telehealth_capability": true
    }
  },
  
  "pcp_payment": {
    "base_capitation": {
      "pmpm_adult": 25.00,
      "pmpm_pediatric": 18.00,
      "pmpm_geriatric": 45.00,
      "age_sex_adjustment": true
    },
    "quality_incentive": {
      "available_pmpm": 5.00,
      "metrics": ["HEDIS", "Patient Satisfaction", "Generic Dispensing"],
      "payment_frequency": "Quarterly"
    },
    "risk_adjustment": {
      "methodology": "HCC-based",
      "prospective": true,
      "retrospective_settlement": true
    }
  }
}
```

---

## Referral Configuration Template

```json
{
  "referral_management": {
    "referral_types": [
      {
        "type": "Standard",
        "description": "Single visit or episode",
        "validity_days": 90,
        "visits_allowed": 3
      },
      {
        "type": "Standing",
        "description": "Ongoing specialist care",
        "validity_days": 365,
        "visits_allowed": "Unlimited",
        "conditions": ["Chronic conditions", "Complex care"]
      },
      {
        "type": "Urgent",
        "description": "Expedited access needed",
        "validity_days": 30,
        "visits_allowed": 1,
        "turnaround_hours": 24
      }
    ],
    
    "self_referral_services": [
      "OB/GYN (annual exam and routine care)",
      "Mental Health (initial assessment)",
      "Substance Use Treatment",
      "Preventive Care",
      "Emergency Services",
      "Urgent Care",
      "Family Planning"
    ],
    
    "referral_workflow": {
      "submission_method": ["Portal", "Fax", "Phone"],
      "auto_approval_criteria": [
        "In-network specialist",
        "Standard referral type",
        "No prior auth required for service"
      ],
      "review_required": [
        "Out-of-area specialist",
        "High-cost procedure",
        "Experimental treatment"
      ],
      "turnaround_standard": {
        "routine_hours": 48,
        "urgent_hours": 24,
        "emergent_hours": 2
      }
    }
  }
}
```

---

## Example: Complete HMO Network Generation

**Prompt**: "Generate an HMO network for a Medicare Advantage plan in Los Angeles County"

**Using Pattern**:

```json
{
  "network_id": "CA-MA-HMO-2024-001",
  "network_name": "HealthFirst Medicare HMO",
  "network_type": "HMO",
  "network_breadth": "Standard",
  "effective_date": "2024-01-01",
  "status": "Active",
  
  "payer": {
    "payer_id": "HFMA",
    "payer_name": "HealthFirst Medicare Advantage",
    "line_of_business": "Medicare"
  },
  
  "geographic_coverage": {
    "coverage_type": "Local",
    "states": ["CA"],
    "counties": [
      {"state": "CA", "county_fips": "06037", "county_name": "Los Angeles"}
    ],
    "msas": ["31080"]
  },
  
  "tier_structure": {
    "tier_count": 1,
    "tiers": [
      {
        "tier_id": "IN-NETWORK",
        "tier_name": "HMO Network",
        "tier_level": 1,
        "cost_sharing_modifier": 1.0
      }
    ]
  },
  
  "access_requirements": {
    "pcp_required": true,
    "pcp_selection": {
      "required": true,
      "auto_assignment": true,
      "change_frequency": "Monthly"
    },
    "referral_required": true,
    "referral_rules": {
      "self_referral_allowed": ["Mental Health", "Annual Wellness"],
      "standing_referral": true
    },
    "out_of_network_coverage": false,
    "emergency_exception": true
  },
  
  "adequacy_standards": {
    "primary_care": {
      "time_minutes": 10,
      "distance_miles": 5,
      "provider_ratio": "1:1000"
    },
    "specialty": {
      "time_minutes": 30,
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
    "specialists": 4800,
    "facilities": 45,
    "pharmacies": 380
  },
  
  "contracted_systems": [
    {"system_name": "Cedars-Sinai", "contract_type": "Full"},
    {"system_name": "UCLA Health", "contract_type": "Full"},
    {"system_name": "Providence", "contract_type": "Partial"},
    {"system_name": "Kaiser", "contract_type": "Excluded"}
  ],
  
  "medicare_specific": {
    "contract_id": "H1234",
    "plan_id": "001",
    "snp_type": null,
    "star_rating": 4
  }
}
```

---

## Validation Checklist

When using this pattern, verify:

| Requirement | Validation |
|-------------|------------|
| PCP Required | Must be `true` for HMO |
| Referral Required | Must be `true` for HMO |
| OON Coverage | Must be `false` (except emergency) |
| Tier Count | Typically 1 (single tier) |
| Adequacy | Must meet CMS/state minimums |
| Self-Referral | Must include mandated services |

---

## Related Skills

- [Network Types](../reference/network-types.md) - HMO definition and concepts
- [Synthetic Network](../synthetic/synthetic-network.md) - Generate network from pattern
- [PPO Network Pattern](ppo-network-pattern.md) - Contrast with open access model

---

*HMO Network Pattern is a template skill in the NetworkSim product.*
