---
name: synthetic-pharmacy-benefit
description: |
  Generate detailed synthetic pharmacy benefit designs including formulary
  structure, tier configurations, specialty programs, and PBM integration.
  Extends synthetic-plan with deep pharmacy benefit detail.
  
  Trigger phrases: "generate pharmacy benefit", "create formulary design",
  "pharmacy tier structure", "specialty benefit", "PBM benefit design",
  "drug benefit", "Part D design", "pharmacy cost sharing"
version: "1.0"
category: synthetic
related_skills:
  - pharmacy-benefit-concepts
  - pbm-operations
  - specialty-pharmacy
  - synthetic-plan
cross_product:
  - rxmembersim: Pharmacy benefit for claim adjudication
---

# Synthetic Pharmacy Benefit Generation

## Overview

Generate detailed synthetic pharmacy benefit designs for health plans. This skill provides deeper pharmacy benefit configuration than the pharmacy section of synthetic-plan, including formulary structure, clinical programs, specialty management, and PBM operational details.

Use this skill when you need:
- Detailed formulary tier structures
- Clinical program configurations (PA, ST, QL)
- Specialty pharmacy benefit design
- PBM integration specifications
- Part D benefit phase details

---

## Trigger Phrases

Use this skill when you see:
- "Generate a pharmacy benefit"
- "Create a formulary structure"
- "Design pharmacy tiers"
- "Generate specialty pharmacy benefit"
- "Create a Part D benefit design"
- "Generate PBM benefit configuration"

---

## Benefit Design Types

### By Tier Count

| Tiers | Structure | Use Case |
|-------|-----------|----------|
| 2-Tier | Generic / Brand | Simple, older plans |
| 3-Tier | Generic / Preferred Brand / Non-Preferred | Traditional |
| 4-Tier | + Specialty | Most common commercial |
| 5-Tier | + Preferred Generic | Incentivize generics |
| 6-Tier | + Preventive / Non-Essential | Complex designs |

### By Cost Sharing Model

| Model | Description | Trend |
|-------|-------------|-------|
| Copay | Fixed dollar amounts | Traditional |
| Coinsurance | Percentage of cost | Growing |
| Hybrid | Copay (low tiers) + Coinsurance (high) | Common |
| Deductible-First | All tiers subject to deductible | HDHP |

### By Formulary Type

| Type | Description | Restriction Level |
|------|-------------|-------------------|
| Open | All drugs covered | Low |
| Incentive | Tiered cost sharing | Medium |
| Closed | Non-formulary not covered | High |
| Exclusion List | Specific drugs excluded | Variable |

---

## Canonical Schema

### Pharmacy Benefit Design

```json
{
  "benefit_id": "string",
  "benefit_name": "string",
  "effective_date": "YYYY-MM-DD",
  "termination_date": "YYYY-MM-DD | null",
  "status": "Active | Pending | Terminated",
  "pbm": {
    "pbm_name": "string",
    "pbm_id": "string",
    "bin": "string (6 digits)",
    "pcn": "string",
    "group_id": "string",
    "help_desk_phone": "string"
  },
  "formulary": {
    "formulary_id": "string",
    "formulary_name": "string",
    "formulary_type": "Open | Incentive | Closed | Exclusion",
    "drug_count": "integer",
    "last_updated": "YYYY-MM-DD",
    "p_and_t_review_cycle": "string"
  },
  "cost_sharing": {
    "deductible": {
      "individual": "number | null",
      "family": "number | null",
      "applies_to_tiers": ["integer"],
      "combined_with_medical": "boolean"
    },
    "out_of_pocket_maximum": {
      "individual": "number | null",
      "family": "number | null",
      "combined_with_medical": "boolean"
    },
    "tier_structure": {
      "tier_count": "integer",
      "tiers": [
        {
          "tier_number": "integer",
          "tier_name": "string",
          "tier_type": "Generic | Preferred Generic | Preferred Brand | Non-Preferred Brand | Specialty | Preventive",
          "description": "string",
          "cost_sharing": {
            "type": "Copay | Coinsurance | Hybrid",
            "retail_30_day": "number",
            "retail_90_day": "number | null",
            "mail_90_day": "number | null",
            "specialty_30_day": "number | null"
          },
          "deductible_applies": "boolean",
          "day_supply_limits": {
            "retail_max": "integer",
            "mail_max": "integer",
            "specialty_max": "integer"
          }
        }
      ]
    },
    "specialty_cost_sharing": {
      "tier_number": "integer",
      "coinsurance_rate": "number (0-1)",
      "maximum_copay": "number | null",
      "minimum_copay": "number | null",
      "annual_maximum": "number | null",
      "deductible_applies": "boolean"
    }
  },
  "pharmacy_network": {
    "network_type": "Open | Preferred | Limited | Exclusive",
    "preferred_network": {
      "enabled": "boolean",
      "differential": "number (additional cost at non-preferred)"
    },
    "ninety_day_retail": {
      "enabled": "boolean",
      "pharmacies": ["string"]
    },
    "mail_order": {
      "enabled": "boolean",
      "mandatory_for_maintenance": "boolean",
      "fill_limit_before_mandatory": "integer | null"
    },
    "specialty_pharmacy": {
      "limited_distribution": "boolean",
      "designated_pharmacies": ["string"],
      "mandatory_specialty": "boolean"
    }
  },
  "clinical_programs": {
    "prior_authorization": {
      "enabled": "boolean",
      "drug_count": "integer",
      "categories": ["string"],
      "turnaround_time_hours": {
        "standard": "integer",
        "urgent": "integer"
      }
    },
    "step_therapy": {
      "enabled": "boolean",
      "drug_count": "integer",
      "categories": ["string"],
      "override_criteria": ["string"]
    },
    "quantity_limits": {
      "enabled": "boolean",
      "drug_count": "integer",
      "limit_types": ["Per Fill", "Per Day", "Per Month", "Days Supply"]
    },
    "drug_utilization_review": {
      "prospective": "boolean",
      "concurrent": "boolean",
      "retrospective": "boolean",
      "alert_types": ["DD", "TD", "DA", "DC", "ER", "ID", "MX", "PA", "PG"]
    },
    "medication_therapy_management": {
      "enabled": "boolean",
      "eligibility_criteria": {
        "chronic_condition_count": "integer",
        "drug_count": "integer",
        "annual_cost_threshold": "number"
      }
    }
  },
  "specialty_programs": {
    "specialty_management": {
      "enabled": "boolean",
      "therapeutic_categories": ["string"],
      "clinical_management": "boolean",
      "adherence_monitoring": "boolean",
      "outcomes_tracking": "boolean"
    },
    "biosimilar_program": {
      "enabled": "boolean",
      "biosimilar_preferred": "boolean",
      "reference_product_tier": "integer",
      "biosimilar_tier": "integer"
    },
    "specialty_copay_assistance": {
      "accumulator_adjustment": "boolean",
      "maximizer_program": "boolean"
    }
  },
  "manufacturer_programs": {
    "copay_card_policy": {
      "accepted": "boolean",
      "accumulator_adjustment": "boolean",
      "maximizer_program": "boolean"
    },
    "patient_assistance": {
      "coordination": "boolean"
    },
    "rebate_eligible": "boolean"
  },
  "dispensing_rules": {
    "brand_penalty": {
      "enabled": "boolean",
      "daw_penalty_amount": "number"
    },
    "new_to_market": {
      "coverage": "Excluded | Non-Preferred | Review Required"
    },
    "compound_medications": {
      "covered": "boolean",
      "pa_required": "boolean",
      "ingredient_cost_limit": "number | null"
    },
    "vaccine_coverage": {
      "covered_at_pharmacy": "boolean",
      "covered_vaccines": ["string"]
    }
  },
  "accumulators": {
    "deductible_accumulator": "boolean",
    "oop_accumulator": "boolean",
    "brand_accumulator": "boolean",
    "specialty_accumulator": "boolean",
    "family_accumulator_type": "Aggregate | Embedded"
  },
  "appeals_and_exceptions": {
    "formulary_exception_process": "boolean",
    "tiering_exception_process": "boolean",
    "appeal_levels": "integer",
    "external_review": "boolean"
  }
}
```

### Part D Specific Schema

```json
{
  "part_d_benefit": {
    "plan_type": "PDP | MA-PD",
    "contract_id": "string",
    "plan_id": "string",
    "benefit_phases": {
      "deductible": {
        "amount": "number",
        "applies_to_tiers": ["integer"]
      },
      "initial_coverage": {
        "limit": "number",
        "tier_structure": {
          "tiers": []
        }
      },
      "coverage_gap": {
        "threshold": "number",
        "generic_coinsurance": "number",
        "brand_coinsurance": "number",
        "gap_discount_program": "boolean"
      },
      "catastrophic": {
        "threshold": "number",
        "generic_copay": "number",
        "brand_copay": "number",
        "coinsurance": "number"
      }
    },
    "lis_status": {
      "full_subsidy": {
        "copay_generic": "number",
        "copay_brand": "number"
      },
      "partial_subsidy_levels": [
        {
          "level": "integer",
          "copay_generic": "number",
          "copay_brand": "number",
          "deductible_percentage": "number"
        }
      ]
    },
    "troop_definition": {
      "includes_copay_assistance": "boolean",
      "includes_gap_discount": "boolean"
    }
  }
}
```

---

## Examples

### Example 1: Standard Commercial 4-Tier Benefit

**Prompt**: "Generate a standard commercial pharmacy benefit with 4 tiers"

**Response**:

```json
{
  "benefit_id": "RX-COMM-2024-001",
  "benefit_name": "Standard Rx Benefit",
  "effective_date": "2024-01-01",
  "status": "Active",
  "pbm": {
    "pbm_name": "Express Scripts",
    "pbm_id": "ESI",
    "bin": "003858",
    "pcn": "A4",
    "group_id": "ESRX001",
    "help_desk_phone": "8002824545"
  },
  "formulary": {
    "formulary_id": "ESI-NF-2024",
    "formulary_name": "Express Scripts National Formulary",
    "formulary_type": "Incentive",
    "drug_count": 4500,
    "last_updated": "2024-01-01"
  },
  "cost_sharing": {
    "deductible": {
      "individual": null,
      "family": null,
      "applies_to_tiers": [],
      "combined_with_medical": false
    },
    "tier_structure": {
      "tier_count": 4,
      "tiers": [
        {
          "tier_number": 1,
          "tier_name": "Generic",
          "tier_type": "Generic",
          "description": "FDA-approved generic medications",
          "cost_sharing": {
            "type": "Copay",
            "retail_30_day": 10,
            "retail_90_day": 25,
            "mail_90_day": 20
          },
          "deductible_applies": false,
          "day_supply_limits": {
            "retail_max": 30,
            "mail_max": 90
          }
        },
        {
          "tier_number": 2,
          "tier_name": "Preferred Brand",
          "tier_type": "Preferred Brand",
          "description": "Preferred brand-name medications",
          "cost_sharing": {
            "type": "Copay",
            "retail_30_day": 35,
            "retail_90_day": 90,
            "mail_90_day": 70
          },
          "deductible_applies": false,
          "day_supply_limits": {
            "retail_max": 30,
            "mail_max": 90
          }
        },
        {
          "tier_number": 3,
          "tier_name": "Non-Preferred Brand",
          "tier_type": "Non-Preferred Brand",
          "description": "Non-preferred brand and non-preferred generics",
          "cost_sharing": {
            "type": "Copay",
            "retail_30_day": 60,
            "retail_90_day": 150,
            "mail_90_day": 120
          },
          "deductible_applies": false,
          "day_supply_limits": {
            "retail_max": 30,
            "mail_max": 90
          }
        },
        {
          "tier_number": 4,
          "tier_name": "Specialty",
          "tier_type": "Specialty",
          "description": "Specialty medications requiring special handling",
          "cost_sharing": {
            "type": "Coinsurance",
            "specialty_30_day": 0.25
          },
          "deductible_applies": false,
          "day_supply_limits": {
            "specialty_max": 30
          }
        }
      ]
    },
    "specialty_cost_sharing": {
      "tier_number": 4,
      "coinsurance_rate": 0.25,
      "maximum_copay": 250,
      "minimum_copay": 50,
      "deductible_applies": false
    }
  },
  "pharmacy_network": {
    "network_type": "Preferred",
    "preferred_network": {
      "enabled": true,
      "differential": 10
    },
    "ninety_day_retail": {
      "enabled": true,
      "pharmacies": ["CVS", "Walgreens", "Kroger", "Costco"]
    },
    "mail_order": {
      "enabled": true,
      "mandatory_for_maintenance": false,
      "fill_limit_before_mandatory": null
    },
    "specialty_pharmacy": {
      "limited_distribution": true,
      "designated_pharmacies": ["Accredo", "CVS Specialty", "Walgreens Specialty"],
      "mandatory_specialty": true
    }
  },
  "clinical_programs": {
    "prior_authorization": {
      "enabled": true,
      "drug_count": 850,
      "categories": ["Specialty", "Biologics", "Controlled Substances", "High-Cost Brand"],
      "turnaround_time_hours": {
        "standard": 72,
        "urgent": 24
      }
    },
    "step_therapy": {
      "enabled": true,
      "drug_count": 320,
      "categories": ["PPIs", "Statins", "ACE/ARBs", "SSRIs", "Diabetes"],
      "override_criteria": ["Contraindication", "Prior failure", "Clinical inappropriateness"]
    },
    "quantity_limits": {
      "enabled": true,
      "drug_count": 450,
      "limit_types": ["Per Fill", "Per Day", "Days Supply"]
    },
    "drug_utilization_review": {
      "prospective": true,
      "concurrent": true,
      "retrospective": true,
      "alert_types": ["DD", "TD", "DA", "DC", "ER", "MX", "PA"]
    }
  },
  "specialty_programs": {
    "specialty_management": {
      "enabled": true,
      "therapeutic_categories": ["Oncology", "Rheumatology", "MS", "Hepatitis C", "HIV"],
      "clinical_management": true,
      "adherence_monitoring": true,
      "outcomes_tracking": true
    },
    "biosimilar_program": {
      "enabled": true,
      "biosimilar_preferred": true,
      "reference_product_tier": 4,
      "biosimilar_tier": 3
    }
  },
  "manufacturer_programs": {
    "copay_card_policy": {
      "accepted": true,
      "accumulator_adjustment": true,
      "maximizer_program": false
    }
  },
  "dispensing_rules": {
    "brand_penalty": {
      "enabled": true,
      "daw_penalty_amount": 50
    },
    "vaccine_coverage": {
      "covered_at_pharmacy": true,
      "covered_vaccines": ["Influenza", "COVID-19", "Shingles", "Pneumonia", "Tdap"]
    }
  }
}
```

---

### Example 2: Medicare Part D Benefit

**Prompt**: "Generate a Medicare Part D benefit design for 2024"

**Response**:

```json
{
  "benefit_id": "RX-PARTD-2024-001",
  "benefit_name": "Medicare Part D Standard Benefit",
  "effective_date": "2024-01-01",
  "status": "Active",
  "pbm": {
    "pbm_name": "CVS Caremark",
    "pbm_id": "CAREMARK",
    "bin": "004336",
    "pcn": "MCAIDADV",
    "help_desk_phone": "8009018123"
  },
  "formulary": {
    "formulary_id": "CMS-APPROVED-2024",
    "formulary_name": "SilverScript Plus Formulary",
    "formulary_type": "Incentive",
    "drug_count": 3200
  },
  "part_d_benefit": {
    "plan_type": "PDP",
    "contract_id": "S5678",
    "plan_id": "001",
    "benefit_phases": {
      "deductible": {
        "amount": 545,
        "applies_to_tiers": [3, 4, 5]
      },
      "initial_coverage": {
        "limit": 5030,
        "tier_structure": {
          "tiers": [
            {
              "tier_number": 1,
              "tier_name": "Preferred Generic",
              "copay_30_day": 0,
              "copay_90_day_mail": 0,
              "deductible_applies": false
            },
            {
              "tier_number": 2,
              "tier_name": "Generic",
              "copay_30_day": 10,
              "copay_90_day_mail": 20,
              "deductible_applies": false
            },
            {
              "tier_number": 3,
              "tier_name": "Preferred Brand",
              "copay_30_day": 47,
              "copay_90_day_mail": 141,
              "deductible_applies": true
            },
            {
              "tier_number": 4,
              "tier_name": "Non-Preferred Drug",
              "coinsurance": 0.45,
              "deductible_applies": true
            },
            {
              "tier_number": 5,
              "tier_name": "Specialty Tier",
              "coinsurance": 0.25,
              "maximum_copay": 100,
              "deductible_applies": true
            }
          ]
        }
      },
      "coverage_gap": {
        "threshold": 5030,
        "generic_coinsurance": 0.25,
        "brand_coinsurance": 0.25,
        "gap_discount_program": true,
        "manufacturer_discount": 0.70
      },
      "catastrophic": {
        "threshold": 8000,
        "generic_copay": 4.15,
        "brand_copay": 10.35,
        "coinsurance": 0.05,
        "whichever_is_greater": true
      }
    },
    "lis_status": {
      "full_subsidy": {
        "copay_generic": 4.50,
        "copay_brand": 11.20
      },
      "partial_subsidy_levels": [
        {
          "level": 1,
          "copay_generic": 4.50,
          "copay_brand": 11.20,
          "deductible_percentage": 0
        },
        {
          "level": 2,
          "copay_generic": 4.50,
          "copay_brand": 11.20,
          "deductible_percentage": 0.25
        },
        {
          "level": 3,
          "copay_generic": 4.50,
          "copay_brand": 11.20,
          "deductible_percentage": 0.50
        }
      ]
    },
    "troop_definition": {
      "includes_copay_assistance": false,
      "includes_gap_discount": true
    }
  },
  "clinical_programs": {
    "prior_authorization": {
      "enabled": true,
      "categories": ["Specialty", "Opioids", "Antipsychotics"]
    },
    "step_therapy": {
      "enabled": true,
      "categories": ["Diabetes", "Cardiovascular", "Respiratory"]
    },
    "quantity_limits": {
      "enabled": true,
      "opioid_morphine_equivalent_limit": 90
    }
  },
  "protected_classes": {
    "anticonvulsants": true,
    "antidepressants": true,
    "antineoplastics": true,
    "antipsychotics": true,
    "antiretrovirals": true,
    "immunosuppressants": true
  },
  "transition_supply": {
    "enabled": true,
    "days_supply": 30,
    "retail_or_mail": "Retail",
    "applies_to": "New enrollees and formulary changes"
  }
}
```

---

### Example 3: HDHP Pharmacy Benefit

**Prompt**: "Generate an HSA-compatible pharmacy benefit where all drugs apply to deductible"

**Response**:

```json
{
  "benefit_id": "RX-HDHP-2024-001",
  "benefit_name": "HSA-Compatible Pharmacy Benefit",
  "effective_date": "2024-01-01",
  "status": "Active",
  "pbm": {
    "pbm_name": "OptumRx",
    "pbm_id": "OPTUM",
    "bin": "610014",
    "pcn": "HDHP",
    "help_desk_phone": "8007972903"
  },
  "cost_sharing": {
    "deductible": {
      "individual": 3200,
      "family": 6400,
      "applies_to_tiers": [1, 2, 3, 4],
      "combined_with_medical": true
    },
    "out_of_pocket_maximum": {
      "individual": 6550,
      "family": 13100,
      "combined_with_medical": true
    },
    "tier_structure": {
      "tier_count": 3,
      "tiers": [
        {
          "tier_number": 1,
          "tier_name": "Generic",
          "cost_sharing": {
            "type": "Coinsurance",
            "retail_30_day": 0.10,
            "retail_90_day": 0.10,
            "mail_90_day": 0.10
          },
          "deductible_applies": true
        },
        {
          "tier_number": 2,
          "tier_name": "Brand",
          "cost_sharing": {
            "type": "Coinsurance",
            "retail_30_day": 0.25,
            "retail_90_day": 0.25,
            "mail_90_day": 0.25
          },
          "deductible_applies": true
        },
        {
          "tier_number": 3,
          "tier_name": "Specialty",
          "cost_sharing": {
            "type": "Coinsurance",
            "specialty_30_day": 0.30
          },
          "deductible_applies": true
        }
      ]
    }
  },
  "hsa_preventive_exception": {
    "enabled": true,
    "covered_pre_deductible": [
      "Statins for cardiovascular disease",
      "ACE inhibitors for CHF",
      "Beta blockers post-MI",
      "Inhaled corticosteroids for asthma",
      "Insulin for diabetes",
      "SSRIs for depression",
      "Anticoagulants for atrial fibrillation"
    ],
    "irs_notice_2019_45_compliant": true
  },
  "pharmacy_network": {
    "network_type": "Open",
    "mail_order": {
      "enabled": true,
      "mandatory_for_maintenance": false
    },
    "specialty_pharmacy": {
      "mandatory_specialty": true
    }
  },
  "dispensing_rules": {
    "brand_penalty": {
      "enabled": true,
      "daw_penalty_amount": 75
    }
  }
}
```

---

### Example 4: Specialty-Focused Benefit

**Prompt**: "Generate a pharmacy benefit with robust specialty management programs"

**Response**:

```json
{
  "benefit_id": "RX-SPEC-2024-001",
  "benefit_name": "Specialty-Focused Pharmacy Benefit",
  "effective_date": "2024-01-01",
  "status": "Active",
  "pbm": {
    "pbm_name": "Magellan Rx",
    "pbm_id": "MAGELLAN",
    "bin": "015599",
    "pcn": "SPEC01"
  },
  "specialty_cost_sharing": {
    "tier_number": 5,
    "coinsurance_rate": 0.20,
    "maximum_copay": 200,
    "minimum_copay": 50,
    "annual_maximum_out_of_pocket": 3600,
    "deductible_applies": true
  },
  "specialty_programs": {
    "specialty_management": {
      "enabled": true,
      "therapeutic_categories": [
        {
          "category": "Oncology",
          "drugs": ["Ibrance", "Keytruda", "Opdivo", "Tagrisso", "Lynparza"],
          "clinical_management": "High-touch",
          "adherence_target": 0.95
        },
        {
          "category": "Rheumatology",
          "drugs": ["Humira", "Enbrel", "Rinvoq", "Xeljanz", "Orencia"],
          "clinical_management": "Standard",
          "biosimilar_available": true
        },
        {
          "category": "Multiple Sclerosis",
          "drugs": ["Ocrevus", "Tysabri", "Tecfidera", "Aubagio", "Kesimpta"],
          "clinical_management": "High-touch",
          "nursing_support": true
        },
        {
          "category": "Inflammatory Bowel Disease",
          "drugs": ["Remicade", "Entyvio", "Stelara", "Skyrizi"],
          "clinical_management": "Standard"
        },
        {
          "category": "Hepatitis C",
          "drugs": ["Epclusa", "Mavyret", "Harvoni"],
          "clinical_management": "Cure-based",
          "outcomes_based_contract": true
        }
      ],
      "clinical_management": true,
      "adherence_monitoring": true,
      "outcomes_tracking": true
    },
    "biosimilar_program": {
      "enabled": true,
      "biosimilar_preferred": true,
      "auto_substitution": false,
      "reference_product_tier": 5,
      "biosimilar_tier": 4,
      "products": [
        {"reference": "Humira", "biosimilars": ["Hadlima", "Hyrimoz", "Cyltezo"]},
        {"reference": "Remicade", "biosimilars": ["Inflectra", "Renflexis", "Avsola"]},
        {"reference": "Neulasta", "biosimilars": ["Fulphila", "Ziextenzo", "Udenyca"]},
        {"reference": "Herceptin", "biosimilars": ["Ogivri", "Herzuma", "Kanjinti"]}
      ]
    },
    "specialty_copay_assistance": {
      "accumulator_adjustment": true,
      "maximizer_program": true,
      "maximizer_details": {
        "eligible_drugs": ["High-cost specialty with manufacturer program"],
        "member_oop_cap": 150,
        "manufacturer_funds_applied_to": "Plan cost, not member OOP"
      }
    },
    "site_of_care": {
      "enabled": true,
      "home_infusion_preferred": true,
      "physician_office_allowed": true,
      "hospital_outpatient_penalty": 500,
      "eligible_drugs": ["Remicade", "Entyvio", "Orencia IV"]
    },
    "specialty_lite": {
      "enabled": true,
      "oral_oncology_fills_at_retail": 1,
      "then_specialty_required": true
    }
  },
  "pharmacy_network": {
    "specialty_pharmacy": {
      "limited_distribution": true,
      "designated_pharmacies": [
        {"name": "Accredo", "pbm": "Express Scripts", "therapeutic_focus": ["General Specialty"]},
        {"name": "AllianceRx Walgreens", "pbm": "Walgreens", "therapeutic_focus": ["Oncology", "Transplant"]},
        {"name": "CVS Specialty", "pbm": "CVS Caremark", "therapeutic_focus": ["General Specialty"]},
        {"name": "Biologics by McKesson", "pbm": "Multiple", "therapeutic_focus": ["Rheumatology", "IBD"]}
      ],
      "mandatory_specialty": true,
      "white_bagging_policy": "Allowed with PA",
      "brown_bagging_prohibited": true
    }
  },
  "clinical_programs": {
    "prior_authorization": {
      "enabled": true,
      "specialty_pa_required": true,
      "clinical_criteria": "NCCN, ACR, AAN guidelines",
      "reauthorization_period_months": 12
    },
    "step_therapy": {
      "enabled": true,
      "biologic_step_required": true,
      "steps": [
        {"step": 1, "requirement": "Conventional DMARD (methotrexate)"},
        {"step": 2, "requirement": "Preferred biologic or biosimilar"},
        {"step": 3, "requirement": "Non-preferred biologic with PA"}
      ]
    }
  },
  "manufacturer_programs": {
    "copay_card_policy": {
      "accepted": true,
      "accumulator_adjustment": true,
      "maximizer_program": true
    },
    "patient_assistance": {
      "coordination": true,
      "hub_partnership": true
    },
    "outcomes_based_contracts": {
      "enabled": true,
      "drugs_with_obc": ["Epclusa", "Zolgensma", "Luxturna"]
    }
  }
}
```

---

## Cross-Product Integration

### RxMemberSim Integration

Pharmacy benefit drives claim adjudication:

```
RxMemberSim Claim + NetworkSim Pharmacy Benefit → Adjudication

Benefit provides:
- Tier assignment and cost sharing
- Clinical program edits (PA, ST, QL)
- Network status (preferred, specialty)
- Accumulator application
```

### MemberSim Integration

Pharmacy benefit coordinates with medical:

```
MemberSim Plan + NetworkSim Pharmacy Benefit → Combined Benefit

Coordination:
- Combined vs separate deductibles
- Combined vs separate OOP max
- Medical pharmacy (buy-and-bill) handling
```

---

## Validation Rules

### Cost Sharing Validation

| Rule | Validation |
|------|------------|
| Tier Sequence | Tier numbers must be sequential 1, 2, 3... |
| Cost Increase | Higher tiers should have higher cost sharing |
| Maximum | Specialty max should be reasonable ($100-$500) |

### Part D Validation

| Rule | Validation |
|------|------------|
| Deductible | ≤ $545 for 2024 |
| ICL | = $5,030 for 2024 |
| Catastrophic | TrOOP = $8,000 for 2024 |
| Protected Classes | All 6 required |

### HSA Compatibility

| Rule | Validation |
|------|------------|
| Deductible | ≥ $1,600 individual / $3,200 family |
| All Drugs | Must apply to deductible (except IRS preventive) |
| Combined | Should combine with medical |

---

## Related Skills

- [Pharmacy Benefit Concepts](../reference/pharmacy-benefit-concepts.md) - Foundational concepts
- [PBM Operations](../reference/pbm-operations.md) - PBM functions
- [Specialty Pharmacy](../reference/specialty-pharmacy.md) - Specialty operations
- [Synthetic Plan](synthetic-plan.md) - Full plan including pharmacy

---

*Synthetic Pharmacy Benefit is a generation skill in the NetworkSim product.*
