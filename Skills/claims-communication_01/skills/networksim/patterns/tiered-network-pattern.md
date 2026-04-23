---
name: tiered-network-pattern
description: |
  Reusable tiered and narrow network configuration patterns for high-performance,
  value-based, and ACA exchange networks. Includes quality-based tiering,
  cost-based tiering, and hybrid approaches.
  
  Trigger phrases: "tiered network pattern", "narrow network", "high-performance network",
  "value-based network", "preferred provider tier", "centers of excellence",
  "ACA exchange network", "skinny network"
version: "1.0"
category: patterns
related_skills:
  - network-types
  - synthetic-network
  - hmo-network-pattern
  - ppo-network-pattern
---

# Tiered Network Pattern

## Overview

This pattern provides templates for tiered and narrow network configurations that use differential cost sharing to steer members toward high-value providers. These networks balance access with cost control through provider performance measurement.

Use this pattern when you need:
- Quality-based provider tiers
- Cost-based provider tiers
- Narrow/high-performance networks
- ACA exchange network configurations
- Centers of Excellence programs

---

## Tiering Approaches

### Quality-Based Tiering

Providers tiered by quality metrics and outcomes.

```json
{
  "tiering_approach": "Quality-Based",
  "description": "Providers assigned to tiers based on quality performance",
  "tier_criteria": {
    "tier_1_preferred": {
      "quality_threshold": "Top 25%",
      "metrics": [
        "HEDIS composite score",
        "Patient satisfaction (CAHPS)",
        "Readmission rates",
        "Complication rates",
        "Preventive care compliance"
      ],
      "minimum_volume": "Sufficient for measurement"
    },
    "tier_2_standard": {
      "quality_threshold": "25th-75th percentile",
      "metrics": "Same as Tier 1",
      "default_tier": true
    },
    "tier_3_basic": {
      "quality_threshold": "Bottom 25% or unmeasured",
      "metrics": "Same as Tier 1",
      "access_preservation": true
    }
  },
  "reassessment": {
    "frequency": "Annual",
    "appeals_process": true,
    "provisional_status": "New providers in Tier 2"
  }
}
```

### Cost-Based Tiering

Providers tiered by cost efficiency.

```json
{
  "tiering_approach": "Cost-Based",
  "description": "Providers assigned to tiers based on cost efficiency",
  "tier_criteria": {
    "tier_1_low_cost": {
      "cost_threshold": "Below 90% of market average",
      "measurement": "Episode-based or per-unit",
      "risk_adjustment": true,
      "minimum_quality": "Must meet quality floor"
    },
    "tier_2_average_cost": {
      "cost_threshold": "90-110% of market average",
      "default_tier": true
    },
    "tier_3_high_cost": {
      "cost_threshold": "Above 110% of market average",
      "inclusion_rationale": "Access preservation or unique services"
    }
  },
  "cost_measurement": {
    "methodology": "Total cost of care",
    "episode_grouper": "Symmetry or similar",
    "risk_adjustment": "HCC or DxCG",
    "outlier_handling": "Truncation at 99th percentile"
  }
}
```

### Hybrid Tiering (Quality + Cost)

Combined approach using both quality and cost.

```json
{
  "tiering_approach": "Hybrid",
  "description": "Providers tiered by combined quality and cost performance",
  "tier_matrix": {
    "high_quality_low_cost": {
      "tier": 1,
      "label": "Preferred",
      "quality": "Top 50%",
      "cost": "Below median"
    },
    "high_quality_high_cost": {
      "tier": 2,
      "label": "Quality",
      "quality": "Top 50%",
      "cost": "Above median"
    },
    "low_quality_low_cost": {
      "tier": 2,
      "label": "Value",
      "quality": "Bottom 50%",
      "cost": "Below median"
    },
    "low_quality_high_cost": {
      "tier": 3,
      "label": "Basic",
      "quality": "Bottom 50%",
      "cost": "Above median"
    }
  },
  "weighting": {
    "quality_weight": 0.60,
    "cost_weight": 0.40
  }
}
```

---

## Network Breadth Patterns

### Broad Tiered Network

```json
{
  "pattern_id": "TIERED-BROAD",
  "pattern_name": "Broad Tiered Network",
  "network_breadth": "Broad",
  "contracted_percentage": "80-95%",
  "tier_structure": {
    "tier_count": 3,
    "distribution": {
      "tier_1": "20-30% of providers",
      "tier_2": "50-60% of providers",
      "tier_3": "20-30% of providers"
    }
  },
  "cost_sharing_differential": {
    "tier_1_to_tier_2": "20-30% lower cost sharing",
    "tier_2_to_tier_3": "20-30% higher cost sharing"
  },
  "use_case": "Large employers wanting choice with incentives"
}
```

### Standard Tiered Network

```json
{
  "pattern_id": "TIERED-STANDARD",
  "pattern_name": "Standard Tiered Network",
  "network_breadth": "Standard",
  "contracted_percentage": "60-80%",
  "tier_structure": {
    "tier_count": 2,
    "distribution": {
      "tier_1_preferred": "40-50% of providers",
      "tier_2_participating": "50-60% of providers"
    }
  },
  "cost_sharing_differential": {
    "tier_1_to_tier_2": "25-40% lower cost sharing"
  },
  "use_case": "Balanced approach for mid-size employers"
}
```

### Narrow Network

```json
{
  "pattern_id": "NARROW",
  "pattern_name": "Narrow Network",
  "network_breadth": "Narrow",
  "contracted_percentage": "30-60%",
  "tier_structure": {
    "tier_count": 1,
    "distribution": {
      "in_network": "Selected high-value providers only"
    }
  },
  "selection_criteria": {
    "quality": "Top performers",
    "cost": "Below market average",
    "access": "Meets adequacy standards",
    "willingness": "Accepts lower rates for volume"
  },
  "use_case": "ACA exchange, cost-sensitive employers"
}
```

### Ultra-Narrow Network

```json
{
  "pattern_id": "ULTRA-NARROW",
  "pattern_name": "Ultra-Narrow Network",
  "network_breadth": "Ultra-Narrow",
  "contracted_percentage": "<30%",
  "tier_structure": {
    "tier_count": 1,
    "distribution": {
      "in_network": "Limited to specific systems/groups"
    }
  },
  "characteristics": {
    "single_system": true,
    "accountable_care": true,
    "risk_bearing": true,
    "integrated_delivery": true
  },
  "use_case": "ACO-based products, select employers"
}
```

---

## Template Configuration

### Tiered Network Template

```json
{
  "network_id": "{{NETWORK_ID}}",
  "network_name": "{{PAYER_NAME}} Tiered Network",
  "network_type": "{{PPO | EPO}}",
  "network_breadth": "{{Standard | Narrow}}",
  "tiering_enabled": true,
  "effective_date": "{{YYYY-MM-DD}}",
  
  "tiering_methodology": {
    "approach": "{{Quality | Cost | Hybrid}}",
    "data_sources": [
      "Claims data",
      "Quality reporting",
      "Patient satisfaction surveys"
    ],
    "measurement_period": "{{12 | 24}} months",
    "update_frequency": "Annual",
    "appeals_process": true
  },
  
  "tier_structure": {
    "tier_count": {{2 | 3}},
    "tiers": [
      {
        "tier_id": "TIER-1",
        "tier_name": "{{Preferred | Premier | Blue}}",
        "tier_level": 1,
        "criteria": {
          "quality_percentile_min": 75,
          "cost_percentile_max": 50,
          "patient_satisfaction_min": 4.0
        },
        "cost_sharing": {
          "deductible_waiver": {{true | false}},
          "copay_reduction": {{0 | 10 | 20}},
          "coinsurance": 0.10
        }
      },
      {
        "tier_id": "TIER-2",
        "tier_name": "{{Standard | Enhanced | White}}",
        "tier_level": 2,
        "criteria": {
          "quality_percentile_min": 25,
          "cost_percentile_max": 75,
          "default_tier": true
        },
        "cost_sharing": {
          "copay": "{{Standard}}",
          "coinsurance": 0.20
        }
      },
      {
        "tier_id": "TIER-3",
        "tier_name": "{{Basic | Participating | Access}}",
        "tier_level": 3,
        "criteria": {
          "quality_percentile_min": 0,
          "access_preservation": true
        },
        "cost_sharing": {
          "copay_surcharge": {{20 | 30 | 50}},
          "coinsurance": 0.35
        }
      }
    ]
  },
  
  "out_of_network": {
    "coverage": {{true | false}},
    "cost_sharing": {
      "deductible_separate": true,
      "deductible_modifier": 2.0,
      "coinsurance": 0.50
    }
  },
  
  "steerage_tools": {
    "provider_search_tier_display": true,
    "cost_estimator": true,
    "care_navigation": true,
    "incentive_programs": true
  }
}
```

---

## Cost Sharing Differentials

### Example: 3-Tier Cost Sharing

```json
{
  "cost_sharing_by_tier": {
    "primary_care_visit": {
      "tier_1": {"copay": 15},
      "tier_2": {"copay": 30},
      "tier_3": {"copay": 50}
    },
    "specialist_visit": {
      "tier_1": {"copay": 30},
      "tier_2": {"copay": 50},
      "tier_3": {"copay": 75}
    },
    "inpatient_admission": {
      "tier_1": {"copay": 250, "coinsurance": 0.10},
      "tier_2": {"copay": 500, "coinsurance": 0.20},
      "tier_3": {"copay": 750, "coinsurance": 0.30}
    },
    "outpatient_surgery": {
      "tier_1": {"copay": 150, "coinsurance": 0.10},
      "tier_2": {"copay": 300, "coinsurance": 0.20},
      "tier_3": {"copay": 500, "coinsurance": 0.30}
    },
    "advanced_imaging": {
      "tier_1": {"copay": 100},
      "tier_2": {"copay": 200},
      "tier_3": {"copay": 350}
    }
  }
}
```

### Example: 2-Tier (Preferred/Standard)

```json
{
  "cost_sharing_by_tier": {
    "primary_care_visit": {
      "preferred": {"copay": 20},
      "standard": {"copay": 40}
    },
    "specialist_visit": {
      "preferred": {"copay": 35},
      "standard": {"copay": 60}
    },
    "inpatient_admission": {
      "preferred": {"coinsurance": 0.15},
      "standard": {"coinsurance": 0.25}
    },
    "outpatient_surgery": {
      "preferred": {"coinsurance": 0.15},
      "standard": {"coinsurance": 0.25}
    }
  }
}
```

---

## ACA Exchange Network Pattern

```json
{
  "pattern_id": "ACA-EXCHANGE",
  "pattern_name": "ACA Exchange Network",
  "regulatory_context": "Affordable Care Act Marketplace",
  
  "network_configuration": {
    "network_type": "EPO",
    "network_breadth": "Narrow",
    "out_of_network_coverage": false,
    "emergency_exception": true
  },
  
  "adequacy_requirements": {
    "regulatory_basis": "45 CFR 156.230",
    "time_distance_standards": {
      "primary_care": {"urban_miles": 10, "rural_miles": 30},
      "hospital": {"urban_miles": 20, "rural_miles": 60},
      "mental_health": {"urban_miles": 20, "rural_miles": 60},
      "oncology": {"urban_miles": 30, "rural_miles": 75}
    },
    "essential_community_providers": {
      "required_percentage": 0.35,
      "categories": [
        "Federally Qualified Health Centers",
        "Ryan White providers",
        "Family Planning providers",
        "Indian Health Service",
        "Substance use treatment centers"
      ]
    }
  },
  
  "provider_selection": {
    "criteria": [
      "Cost efficiency (below market)",
      "Quality metrics (above threshold)",
      "Essential services coverage",
      "Geographic distribution"
    ],
    "excluded": [
      "High-cost outliers",
      "Low-quality performers",
      "Non-compliant with network terms"
    ]
  },
  
  "metal_tier_alignment": {
    "bronze": {"actuarial_value": 0.60, "cost_sharing": "High"},
    "silver": {"actuarial_value": 0.70, "cost_sharing": "Moderate"},
    "gold": {"actuarial_value": 0.80, "cost_sharing": "Low"},
    "platinum": {"actuarial_value": 0.90, "cost_sharing": "Minimal"}
  }
}
```

---

## Centers of Excellence Pattern

```json
{
  "pattern_id": "COE",
  "pattern_name": "Centers of Excellence",
  "description": "Designated high-quality facilities for complex procedures",
  
  "coe_categories": [
    {
      "category": "Transplant",
      "procedures": ["Heart", "Liver", "Kidney", "Lung", "Bone Marrow"],
      "designation_criteria": {
        "volume_minimum": 50,
        "survival_rates": "Above national average",
        "accreditation": "Required"
      },
      "benefit_enhancement": {
        "travel_benefit": true,
        "lodging_benefit": true,
        "waived_deductible": true,
        "reduced_coinsurance": 0.10
      }
    },
    {
      "category": "Bariatric Surgery",
      "procedures": ["Gastric Bypass", "Sleeve Gastrectomy", "LAP-BAND"],
      "designation_criteria": {
        "volume_minimum": 100,
        "complication_rates": "Below benchmark",
        "accreditation": "MBSAQIP"
      },
      "benefit_enhancement": {
        "travel_benefit": true,
        "reduced_cost_sharing": true
      }
    },
    {
      "category": "Orthopedic Joint Replacement",
      "procedures": ["Hip Replacement", "Knee Replacement"],
      "designation_criteria": {
        "volume_minimum": 200,
        "readmission_rates": "Below benchmark",
        "patient_outcomes": "Top quartile"
      },
      "benefit_enhancement": {
        "bundled_pricing": true,
        "warranty": "90-day complication coverage"
      }
    },
    {
      "category": "Cardiac",
      "procedures": ["CABG", "Valve Replacement", "Complex PCI"],
      "designation_criteria": {
        "volume_minimum": 300,
        "mortality_rates": "Below expected",
        "accreditation": "STS rated"
      },
      "benefit_enhancement": {
        "travel_benefit": true,
        "reduced_cost_sharing": true
      }
    },
    {
      "category": "Cancer",
      "procedures": ["Complex oncology treatment"],
      "designation_criteria": {
        "designation": "NCI-designated or equivalent",
        "clinical_trials": "Available",
        "multidisciplinary": "Tumor boards required"
      },
      "benefit_enhancement": {
        "travel_benefit": true,
        "clinical_trial_coverage": true
      }
    }
  ],
  
  "travel_benefits": {
    "eligible_distance": 100,
    "airfare": "Coach class",
    "lodging_per_diem": 150,
    "companion_travel": true,
    "ground_transportation": true
  }
}
```

---

## Example: Complete Tiered Network Generation

**Prompt**: "Generate a quality-tiered PPO network for Texas large employer"

```json
{
  "network_id": "TX-TIERED-PPO-2024",
  "network_name": "HealthSelect Tiered PPO",
  "network_type": "PPO",
  "network_breadth": "Standard",
  "tiering_enabled": true,
  "effective_date": "2024-01-01",
  
  "payer": {
    "payer_id": "BCTX",
    "payer_name": "Blue Cross Texas",
    "line_of_business": "Commercial Large Group"
  },
  
  "geographic_coverage": {
    "states": ["TX"],
    "primary_markets": ["Dallas-Fort Worth", "Houston", "San Antonio", "Austin"]
  },
  
  "tiering_methodology": {
    "approach": "Hybrid",
    "quality_weight": 0.60,
    "cost_weight": 0.40,
    "quality_metrics": [
      "HEDIS scores",
      "Hospital readmission rates",
      "Patient satisfaction",
      "Preventive care rates"
    ],
    "cost_metrics": [
      "Episode cost vs benchmark",
      "Utilization patterns",
      "Generic prescribing rates"
    ],
    "measurement_period": "24 months",
    "update_frequency": "Annual"
  },
  
  "tier_structure": {
    "tier_count": 3,
    "tiers": [
      {
        "tier_id": "BLUE",
        "tier_name": "Blue Tier - Preferred",
        "tier_level": 1,
        "provider_count": 8500,
        "criteria": {
          "quality_percentile_min": 75,
          "cost_percentile_max": 60
        }
      },
      {
        "tier_id": "WHITE",
        "tier_name": "White Tier - Standard",
        "tier_level": 2,
        "provider_count": 18000,
        "criteria": {
          "quality_percentile_min": 25,
          "default_tier": true
        }
      },
      {
        "tier_id": "GRAY",
        "tier_name": "Gray Tier - Participating",
        "tier_level": 3,
        "provider_count": 6000,
        "criteria": {
          "access_preservation": true
        }
      }
    ]
  },
  
  "cost_sharing": {
    "primary_care": {
      "blue": 15, "white": 30, "gray": 50
    },
    "specialist": {
      "blue": 30, "white": 50, "gray": 75
    },
    "inpatient": {
      "blue": {"copay": 250, "coinsurance": 0.10},
      "white": {"copay": 500, "coinsurance": 0.20},
      "gray": {"copay": 750, "coinsurance": 0.30}
    }
  },
  
  "out_of_network": {
    "coverage": true,
    "deductible_separate": true,
    "coinsurance": 0.50
  },
  
  "contracted_systems_by_tier": {
    "blue_tier": [
      "Baylor Scott & White (select facilities)",
      "Texas Health Resources (select)",
      "Memorial Hermann (select)"
    ],
    "white_tier": [
      "Most Baylor Scott & White",
      "Most Texas Health",
      "HCA facilities"
    ],
    "gray_tier": [
      "Remaining contracted providers"
    ]
  }
}
```

---

## Validation Checklist

| Requirement | Validation |
|-------------|------------|
| Tier Count | 2-4 tiers typical |
| Tier Criteria | Documented and measurable |
| Cost Differential | Meaningful but not punitive |
| Access | Each tier meets adequacy minimums |
| Transparency | Tier assignment visible to members |
| Appeals | Process for provider tier disputes |

---

## Related Skills

- [Network Types](../reference/network-types.md) - Network type definitions
- [Synthetic Network](../synthetic/synthetic-network.md) - Generate tiered networks
- [HMO Network Pattern](hmo-network-pattern.md) - Closed network alternative
- [PPO Network Pattern](ppo-network-pattern.md) - Open access foundation

---

*Tiered Network Pattern is a template skill in the NetworkSim product.*
