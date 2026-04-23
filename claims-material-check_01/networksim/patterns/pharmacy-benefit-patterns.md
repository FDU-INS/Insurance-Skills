---
name: pharmacy-benefit-patterns
description: |
  Reusable pharmacy benefit configuration patterns including tier structures,
  cost sharing models, formulary approaches, and clinical program templates.
  Use as starting templates for pharmacy benefit generation.
  
  Trigger phrases: "pharmacy benefit pattern", "formulary template", "tier structure pattern",
  "4-tier formulary", "5-tier formulary", "closed formulary", "incentive formulary",
  "specialty tier pattern", "copay vs coinsurance"
version: "1.0"
category: patterns
related_skills:
  - pharmacy-benefit-concepts
  - synthetic-pharmacy-benefit
  - synthetic-plan
  - pbm-operations
---

# Pharmacy Benefit Patterns

## Overview

This skill provides reusable templates for pharmacy benefit configurations. These patterns represent common industry approaches to formulary design, tier structures, and cost sharing models.

Use this pattern when you need:
- Standard tier structure configurations
- Cost sharing model templates
- Formulary approach patterns
- Clinical program configurations
- Specialty pharmacy benefit templates

---

## Tier Structure Patterns

### 2-Tier (Generic/Brand)

Simplest structure separating generic and brand drugs.

```json
{
  "pattern_id": "TIER-2-GENERIC-BRAND",
  "pattern_name": "2-Tier Generic/Brand",
  "tier_count": 2,
  "description": "Simple generic vs brand differentiation",
  
  "tiers": [
    {
      "tier": 1,
      "name": "Generic",
      "description": "FDA-approved generic drugs",
      "formulary_status": "Preferred",
      "typical_cost_sharing": {
        "copay": {"retail_30": 10, "retail_90": 25, "mail_90": 20},
        "coinsurance": null
      }
    },
    {
      "tier": 2,
      "name": "Brand",
      "description": "Brand-name drugs",
      "formulary_status": "Non-Preferred",
      "typical_cost_sharing": {
        "copay": {"retail_30": 35, "retail_90": 90, "mail_90": 70},
        "coinsurance": null
      }
    }
  ],
  
  "use_cases": [
    "Simple benefit designs",
    "High generic utilization goals",
    "Small employer groups"
  ],
  
  "pros": ["Simple to understand", "Easy to administer", "Maximizes generic use"],
  "cons": ["No brand differentiation", "Limited formulary steering"]
}
```

### 3-Tier (Generic/Preferred Brand/Non-Preferred Brand)

Classic structure with brand differentiation.

```json
{
  "pattern_id": "TIER-3-CLASSIC",
  "pattern_name": "3-Tier Classic",
  "tier_count": 3,
  "description": "Generic with preferred/non-preferred brand differentiation",
  
  "tiers": [
    {
      "tier": 1,
      "name": "Generic",
      "description": "Generic drugs and select low-cost brands",
      "formulary_status": "Preferred",
      "typical_cost_sharing": {
        "copay": {"retail_30": 10, "retail_90": 25, "mail_90": 20}
      }
    },
    {
      "tier": 2,
      "name": "Preferred Brand",
      "description": "Preferred brand-name drugs with rebates",
      "formulary_status": "Preferred",
      "typical_cost_sharing": {
        "copay": {"retail_30": 35, "retail_90": 90, "mail_90": 70}
      }
    },
    {
      "tier": 3,
      "name": "Non-Preferred Brand",
      "description": "Non-preferred brands, typically with alternatives",
      "formulary_status": "Non-Preferred",
      "typical_cost_sharing": {
        "copay": {"retail_30": 60, "retail_90": 150, "mail_90": 120}
      }
    }
  ],
  
  "formulary_strategy": {
    "tier_2_criteria": [
      "Manufacturer rebate agreement",
      "Clinical preference when therapeutic alternatives exist",
      "First-line therapy for condition"
    ],
    "tier_3_criteria": [
      "No rebate or lower rebate",
      "Preferred alternative available",
      "Second-line or specialty use"
    ]
  },
  
  "use_cases": ["Standard commercial plans", "Most common structure"]
}
```

### 4-Tier (Generic/Preferred/Non-Preferred/Specialty)

Adds dedicated specialty tier.

```json
{
  "pattern_id": "TIER-4-SPECIALTY",
  "pattern_name": "4-Tier with Specialty",
  "tier_count": 4,
  "description": "Separates specialty drugs into dedicated tier",
  
  "tiers": [
    {
      "tier": 1,
      "name": "Generic",
      "description": "Generic drugs",
      "typical_cost_sharing": {
        "copay": {"retail_30": 10, "retail_90": 25, "mail_90": 20}
      }
    },
    {
      "tier": 2,
      "name": "Preferred Brand",
      "description": "Preferred brand-name drugs",
      "typical_cost_sharing": {
        "copay": {"retail_30": 35, "retail_90": 90, "mail_90": 70}
      }
    },
    {
      "tier": 3,
      "name": "Non-Preferred Brand",
      "description": "Non-preferred brand drugs",
      "typical_cost_sharing": {
        "copay": {"retail_30": 60, "retail_90": 150, "mail_90": 120}
      }
    },
    {
      "tier": 4,
      "name": "Specialty",
      "description": "High-cost specialty medications",
      "specialty_tier": true,
      "typical_cost_sharing": {
        "copay": null,
        "coinsurance": {"percentage": 0.25, "minimum": 100, "maximum": 500}
      },
      "dispensing_rules": {
        "days_supply": 30,
        "specialty_pharmacy_required": true,
        "mail_order_available": false
      }
    }
  ],
  
  "specialty_criteria": {
    "cost_threshold": 1000,
    "characteristics": [
      "Biologics",
      "Injectable/infusible",
      "Requires special handling",
      "Requires clinical monitoring",
      "Orphan drugs"
    ]
  },
  
  "use_cases": ["Most commercial plans", "Medicare Part D"]
}
```

### 5-Tier (With Preferred Specialty)

Adds specialty differentiation.

```json
{
  "pattern_id": "TIER-5-PREFERRED-SPECIALTY",
  "pattern_name": "5-Tier with Preferred Specialty",
  "tier_count": 5,
  "description": "Differentiates preferred vs non-preferred specialty",
  
  "tiers": [
    {
      "tier": 1,
      "name": "Preferred Generic",
      "typical_cost_sharing": {"copay": {"retail_30": 5}}
    },
    {
      "tier": 2,
      "name": "Generic",
      "typical_cost_sharing": {"copay": {"retail_30": 15}}
    },
    {
      "tier": 3,
      "name": "Preferred Brand",
      "typical_cost_sharing": {"copay": {"retail_30": 40}}
    },
    {
      "tier": 4,
      "name": "Non-Preferred",
      "includes": ["Non-preferred brand", "Non-preferred generic"],
      "typical_cost_sharing": {"copay": {"retail_30": 80}}
    },
    {
      "tier": 5,
      "name": "Specialty",
      "typical_cost_sharing": {
        "coinsurance": {"percentage": 0.30, "maximum": 400}
      }
    }
  ],
  
  "use_cases": ["Large employers", "Medicare Part D Enhanced"]
}
```

### 6-Tier (Comprehensive)

Maximum differentiation including preventive tier.

```json
{
  "pattern_id": "TIER-6-COMPREHENSIVE",
  "pattern_name": "6-Tier Comprehensive",
  "tier_count": 6,
  "description": "Full differentiation with preventive and dual specialty tiers",
  
  "tiers": [
    {
      "tier": 1,
      "name": "Preventive",
      "description": "ACA-required preventive medications",
      "typical_cost_sharing": {"copay": 0},
      "includes": ["Contraceptives", "Statins for prevention", "Aspirin"]
    },
    {
      "tier": 2,
      "name": "Preferred Generic",
      "typical_cost_sharing": {"copay": {"retail_30": 10}}
    },
    {
      "tier": 3,
      "name": "Non-Preferred Generic",
      "typical_cost_sharing": {"copay": {"retail_30": 25}}
    },
    {
      "tier": 4,
      "name": "Preferred Brand",
      "typical_cost_sharing": {"copay": {"retail_30": 45}}
    },
    {
      "tier": 5,
      "name": "Non-Preferred Brand",
      "typical_cost_sharing": {"copay": {"retail_30": 90}}
    },
    {
      "tier": 6,
      "name": "Specialty",
      "typical_cost_sharing": {
        "coinsurance": {"percentage": 0.30, "maximum": 500}
      }
    }
  ],
  
  "use_cases": ["Complex benefit designs", "Large self-insured employers"]
}
```

---

## Cost Sharing Model Patterns

### Copay-Only Model

```json
{
  "pattern_id": "COPAY-ONLY",
  "pattern_name": "Copay-Only",
  "description": "Fixed dollar copays for all tiers",
  
  "cost_sharing": {
    "tier_1": {"retail_30": 10, "retail_90": 25, "mail_90": 20},
    "tier_2": {"retail_30": 35, "retail_90": 90, "mail_90": 70},
    "tier_3": {"retail_30": 60, "retail_90": 150, "mail_90": 120},
    "tier_4": {"retail_30": 100, "retail_90": null, "mail_90": null}
  },
  
  "characteristics": {
    "predictability": "High - members know cost upfront",
    "drug_cost_sensitivity": "Low - same copay regardless of drug cost",
    "trend_exposure": "Plan absorbs cost increases"
  },
  
  "best_for": ["Traditional benefit designs", "Predictable member costs"]
}
```

### Coinsurance Model

```json
{
  "pattern_id": "COINSURANCE-ONLY",
  "pattern_name": "Coinsurance-Only",
  "description": "Percentage coinsurance for all tiers",
  
  "cost_sharing": {
    "tier_1": {"coinsurance": 0.10},
    "tier_2": {"coinsurance": 0.25},
    "tier_3": {"coinsurance": 0.40},
    "tier_4": {"coinsurance": 0.30, "maximum": 500}
  },
  
  "characteristics": {
    "predictability": "Low - varies with drug cost",
    "drug_cost_sensitivity": "High - members pay more for expensive drugs",
    "trend_exposure": "Shared with member"
  },
  
  "considerations": {
    "minimum_required": false,
    "maximum_required": "Recommended for high-cost drugs",
    "member_education": "Need to explain variable costs"
  },
  
  "best_for": ["Cost-conscious designs", "HDHP plans"]
}
```

### Hybrid Model (Copay + Coinsurance)

```json
{
  "pattern_id": "HYBRID",
  "pattern_name": "Hybrid Copay/Coinsurance",
  "description": "Copays for traditional drugs, coinsurance for specialty",
  
  "cost_sharing": {
    "tier_1": {
      "type": "copay",
      "amount": {"retail_30": 10, "retail_90": 25, "mail_90": 20}
    },
    "tier_2": {
      "type": "copay",
      "amount": {"retail_30": 35, "retail_90": 90, "mail_90": 70}
    },
    "tier_3": {
      "type": "copay",
      "amount": {"retail_30": 60, "retail_90": 150, "mail_90": 120}
    },
    "tier_4_specialty": {
      "type": "coinsurance",
      "percentage": 0.25,
      "minimum": 100,
      "maximum": 500
    }
  },
  
  "rationale": {
    "traditional_tiers": "Predictable copays for routine medications",
    "specialty_tier": "Coinsurance shares cost for expensive drugs"
  },
  
  "best_for": ["Most common commercial approach", "Balanced design"]
}
```

### HDHP/HSA-Compatible Model

```json
{
  "pattern_id": "HDHP-HSA",
  "pattern_name": "HDHP HSA-Compatible",
  "description": "All drugs apply to deductible until met",
  
  "cost_sharing": {
    "pre_deductible": {
      "all_tiers": "100% member responsibility",
      "exception": "IRS-approved preventive drugs at $0"
    },
    "post_deductible": {
      "tier_1": {"coinsurance": 0.10},
      "tier_2": {"coinsurance": 0.20},
      "tier_3": {"coinsurance": 0.30},
      "tier_4": {"coinsurance": 0.25, "maximum": 400}
    }
  },
  
  "preventive_exception": {
    "applicable": true,
    "reference": "IRS Notice 2019-45",
    "covered_conditions": [
      "Statins (high cholesterol)",
      "Blood pressure medications",
      "Diabetes medications (when not diabetic)",
      "Contraceptives"
    ]
  },
  
  "deductible_integration": {
    "combined_with_medical": true,
    "rx_carve_out": false
  },
  
  "best_for": ["HSA-eligible plans", "Consumer-directed health plans"]
}
```

---

## Formulary Approach Patterns

### Open Formulary

```json
{
  "pattern_id": "FORMULARY-OPEN",
  "pattern_name": "Open Formulary",
  "description": "Minimal restrictions, broad coverage",
  
  "characteristics": {
    "drug_coverage": "Most FDA-approved drugs covered",
    "prior_authorization": "Minimal",
    "step_therapy": "Limited",
    "exclusions": "Few (cosmetic, experimental)"
  },
  
  "tier_assignment": {
    "method": "Cost-based with rebate consideration",
    "preferred_criteria": "Rebate agreement",
    "non_preferred": "Available without restrictions"
  },
  
  "use_cases": ["Premium benefit designs", "Union plans", "Executive plans"],
  "cost_impact": "Higher plan costs, lower member friction"
}
```

### Incentive Formulary

```json
{
  "pattern_id": "FORMULARY-INCENTIVE",
  "pattern_name": "Incentive Formulary",
  "description": "All drugs covered with financial incentives for preferred",
  
  "characteristics": {
    "drug_coverage": "Broad coverage",
    "prior_authorization": "Moderate",
    "step_therapy": "Moderate",
    "exclusions": "Therapeutic duplicates, some high-cost"
  },
  
  "tier_assignment": {
    "method": "Clinical and economic evaluation",
    "preferred_criteria": [
      "Clinical efficacy",
      "Safety profile",
      "Rebate/pricing",
      "First-line therapy status"
    ]
  },
  
  "steering_mechanisms": {
    "tier_differential": "Significant ($25+ difference)",
    "generic_incentives": "Maximum difference from brand",
    "biosimilar_incentives": "Preferred tier placement"
  },
  
  "use_cases": ["Most commercial plans"],
  "cost_impact": "Moderate plan costs, moderate member friction"
}
```

### Closed Formulary

```json
{
  "pattern_id": "FORMULARY-CLOSED",
  "pattern_name": "Closed Formulary",
  "description": "Only formulary drugs covered, exceptions via PA",
  
  "characteristics": {
    "drug_coverage": "Limited to formulary drugs",
    "prior_authorization": "Required for non-formulary",
    "step_therapy": "Extensive",
    "exclusions": "Significant exclusion list"
  },
  
  "non_formulary_handling": {
    "coverage": "Not covered without exception",
    "exception_process": "Medical necessity PA",
    "approval_criteria": [
      "Tried and failed formulary alternatives",
      "Contraindication to alternatives",
      "Documented medical necessity"
    ]
  },
  
  "use_cases": ["Cost-focused employers", "Medicaid MCOs", "Some Medicare Part D"],
  "cost_impact": "Lowest plan costs, highest member friction"
}
```

### Exclusion List Formulary

```json
{
  "pattern_id": "FORMULARY-EXCLUSION",
  "pattern_name": "Exclusion List Formulary",
  "description": "Broad coverage with defined exclusion list",
  
  "characteristics": {
    "drug_coverage": "Most drugs unless excluded",
    "exclusion_rationale": [
      "Therapeutic equivalent available",
      "Cost significantly higher than alternative",
      "Limited clinical differentiation"
    ]
  },
  
  "typical_exclusions": [
    "Brand when generic available",
    "Me-too drugs in crowded classes",
    "High-cost low-value medications",
    "Lifestyle/cosmetic drugs"
  ],
  
  "excluded_drug_handling": {
    "coverage": "Not covered",
    "exceptions": "Limited, medical necessity only",
    "transition": "New exclusions: 90-day transition fill"
  },
  
  "use_cases": ["Most PBMs default", "Express Scripts NSF", "CVS Standard Control"],
  "cost_impact": "Moderate savings, moderate friction"
}
```

---

## Clinical Program Patterns

### Standard Clinical Management

```json
{
  "pattern_id": "CLINICAL-STANDARD",
  "pattern_name": "Standard Clinical Programs",
  
  "prior_authorization": {
    "scope": "High-cost and specialty drugs",
    "typical_categories": [
      "Specialty medications",
      "High-cost brands with alternatives",
      "Abuse-potential medications",
      "Growth hormones",
      "Biologics"
    ],
    "turnaround": {
      "standard": "72 hours",
      "urgent": "24 hours"
    }
  },
  
  "step_therapy": {
    "scope": "Therapeutic classes with clear hierarchy",
    "typical_protocols": [
      {
        "class": "PPIs",
        "steps": ["Generic PPI", "Brand PPI"]
      },
      {
        "class": "Statins",
        "steps": ["Generic statin", "High-intensity generic", "Brand"]
      },
      {
        "class": "NSAIDs",
        "steps": ["OTC ibuprofen/naproxen", "Rx NSAID", "COX-2"]
      }
    ],
    "override": "Prior authorization for step skip"
  },
  
  "quantity_limits": {
    "scope": "Safety and cost management",
    "basis": "FDA labeling, clinical guidelines",
    "common_limits": [
      {"drug_class": "Triptans", "limit": "9 units/month"},
      {"drug_class": "Opioids", "limit": "MME-based"},
      {"drug_class": "Sleep aids", "limit": "30 tablets/month"}
    ]
  }
}
```

### Enhanced Clinical Management

```json
{
  "pattern_id": "CLINICAL-ENHANCED",
  "pattern_name": "Enhanced Clinical Programs",
  
  "all_standard_programs": true,
  
  "additional_programs": {
    "drug_utilization_review": {
      "prospective": true,
      "concurrent": true,
      "retrospective": true,
      "clinical_alerts": [
        "Drug-drug interactions",
        "Therapeutic duplication",
        "Drug-age precautions",
        "Drug-disease contraindications",
        "Early refill limits"
      ]
    },
    
    "opioid_management": {
      "mme_monitoring": true,
      "mme_threshold": 90,
      "prescriber_limits": true,
      "pharmacy_limits": true,
      "lock_in_program": true
    },
    
    "medication_therapy_management": {
      "eligible_population": "Chronic conditions, polypharmacy",
      "services": [
        "Comprehensive medication review",
        "Targeted intervention programs",
        "Personal medication list",
        "Medication action plan"
      ]
    },
    
    "biosimilar_programs": {
      "auto_substitution": false,
      "preferred_biosimilar": true,
      "reference_product_tier": "Higher tier if biosimilar available"
    }
  }
}
```

---

## Example: Complete Pharmacy Benefit Pattern

**Prompt**: "Generate a 4-tier pharmacy benefit pattern for large employer"

```json
{
  "benefit_id": "RX-LARGE-EMP-2024",
  "benefit_name": "Large Employer 4-Tier Rx Benefit",
  "pattern_basis": "TIER-4-SPECIALTY",
  
  "tier_structure": {
    "tier_count": 4,
    "tiers": [
      {
        "tier": 1,
        "name": "Generic",
        "cost_sharing": {
          "retail_30": 10,
          "retail_90": 25,
          "mail_90": 20
        }
      },
      {
        "tier": 2,
        "name": "Preferred Brand",
        "cost_sharing": {
          "retail_30": 35,
          "retail_90": 90,
          "mail_90": 70
        }
      },
      {
        "tier": 3,
        "name": "Non-Preferred",
        "cost_sharing": {
          "retail_30": 70,
          "retail_90": 175,
          "mail_90": 140
        }
      },
      {
        "tier": 4,
        "name": "Specialty",
        "cost_sharing": {
          "coinsurance": 0.25,
          "minimum": 100,
          "maximum": 400
        }
      }
    ]
  },
  
  "pharmacy_network": {
    "retail_preferred": true,
    "preferred_savings": "Additional $5 off copay",
    "90_day_retail": true,
    "mail_order": {
      "mandatory": false,
      "maintenance_after_fills": 3,
      "incentive": "Lower copay"
    },
    "specialty": {
      "limited_network": true,
      "exclusive_specialty": "CVS Specialty"
    }
  },
  
  "formulary": {
    "type": "Incentive with exclusions",
    "formulary_id": "Standard Control 2024",
    "exclusion_list": true,
    "drug_count": 3500
  },
  
  "clinical_programs": {
    "prior_authorization": true,
    "step_therapy": true,
    "quantity_limits": true,
    "dtp_enforcement": true,
    "opioid_management": true,
    "biosimilar_preferred": true
  },
  
  "accumulators": {
    "copay_assistance": "Accumulator Adjustment Program",
    "third_party_payments": "May not count to deductible/OOP"
  },
  
  "annual_limits": {
    "deductible": {
      "individual": 250,
      "family": 500,
      "applies_to": "Brand drugs only"
    },
    "out_of_pocket_max": {
      "individual": 3000,
      "family": 6000,
      "integrated_with_medical": true
    }
  }
}
```

---

## Related Skills

- [Pharmacy Benefit Concepts](../reference/pharmacy-benefit-concepts.md) - Tier and formulary concepts
- [Synthetic Pharmacy Benefit](../synthetic/synthetic-pharmacy-benefit.md) - Generate from patterns
- [PBM Operations](../reference/pbm-operations.md) - PBM processing context
- [Specialty Pharmacy](../reference/specialty-pharmacy.md) - Specialty tier context

---

*Pharmacy Benefit Patterns is a template skill in the NetworkSim product.*
