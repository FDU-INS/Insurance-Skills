---
name: specialty-distribution-pattern
description: |
  Reusable patterns for specialty pharmacy distribution including hub model,
  limited distribution, site-of-care optimization, and specialty network
  configurations. Use as templates for specialty pharmacy benefit design.
  
  Trigger phrases: "specialty distribution pattern", "hub model", "limited distribution",
  "specialty pharmacy network", "site of care", "buy and bill", "white bagging",
  "brown bagging", "specialty pharmacy routing", "REMS distribution"
version: "1.0"
category: patterns
related_skills:
  - specialty-pharmacy
  - synthetic-pharmacy
  - pharmacy-benefit-patterns
  - synthetic-pharmacy-benefit
---

# Specialty Distribution Pattern

## Overview

This skill provides reusable patterns for specialty pharmacy distribution models. Specialty drugs have unique distribution requirements due to cost, handling, clinical monitoring needs, and regulatory requirements (REMS).

Use this pattern when you need:
- Hub services configuration
- Limited distribution network design
- Site-of-care optimization rules
- Specialty pharmacy routing logic
- REMS compliance frameworks

---

## Distribution Model Patterns

### Open Distribution

All specialty pharmacies can dispense.

```json
{
  "pattern_id": "DIST-OPEN",
  "pattern_name": "Open Distribution",
  "description": "Drug available through any qualified specialty pharmacy",
  
  "characteristics": {
    "pharmacy_access": "Any specialty pharmacy",
    "manufacturer_restriction": false,
    "payer_restriction": false,
    "distribution_type": "Unrestricted"
  },
  
  "typical_drugs": [
    "Older specialty drugs",
    "Multiple manufacturer sources",
    "High-volume specialties"
  ],
  
  "pharmacy_requirements": {
    "accreditation": "URAC and/or ACHC preferred",
    "specialty_license": "State requirements",
    "cold_chain": "As required by drug",
    "clinical_programs": "Varies by payer"
  },
  
  "payer_considerations": {
    "network_design": "Broad specialty network",
    "preferred_pharmacy": "May designate preferred",
    "cost_control": "Via network discounts and rebates"
  },
  
  "examples": ["Humira (prior to biosimilars)", "Many oral oncology"]
}
```

### Limited Distribution

Manufacturer restricts to select pharmacies.

```json
{
  "pattern_id": "DIST-LIMITED",
  "pattern_name": "Limited Distribution",
  "description": "Manufacturer limits distribution to qualified pharmacies",
  
  "characteristics": {
    "pharmacy_access": "Select pharmacies only",
    "manufacturer_restriction": true,
    "authorization_required": true,
    "distribution_type": "Controlled"
  },
  
  "authorization_types": {
    "manufacturer_selected": {
      "description": "Manufacturer chooses pharmacies",
      "criteria": [
        "Clinical capability",
        "Geographic coverage",
        "Data reporting",
        "Contractual terms"
      ]
    },
    "application_based": {
      "description": "Pharmacies apply for authorization",
      "requirements": [
        "Accreditation",
        "Clinical staff credentials",
        "Technology requirements",
        "Volume commitments"
      ]
    }
  },
  
  "typical_drugs": [
    "REMS drugs",
    "Complex administration",
    "High-touch clinical needs",
    "Orphan drugs"
  ],
  
  "pharmacy_count": {
    "ultra_limited": "1-3 pharmacies",
    "limited": "4-10 pharmacies",
    "select": "11-25 pharmacies"
  },
  
  "payer_considerations": {
    "network_limitation": "Must contract with authorized pharmacies",
    "member_access": "May require travel or mail",
    "cost_negotiation": "Limited leverage"
  }
}
```

### Exclusive Distribution

Single pharmacy or pharmacy group.

```json
{
  "pattern_id": "DIST-EXCLUSIVE",
  "pattern_name": "Exclusive Distribution",
  "description": "Single pharmacy designated for product",
  
  "characteristics": {
    "pharmacy_access": "Single designated pharmacy",
    "manufacturer_restriction": true,
    "exclusive_arrangement": true,
    "distribution_type": "Exclusive"
  },
  
  "arrangement_types": {
    "manufacturer_owned": {
      "description": "Manufacturer operates pharmacy",
      "example": "Vertex CF pharmacy services"
    },
    "contracted_exclusive": {
      "description": "Exclusive contract with specialty pharmacy",
      "example": "Many REMS programs"
    },
    "hub_direct": {
      "description": "Hub dispenses directly",
      "example": "Some cell/gene therapies"
    }
  },
  
  "typical_drugs": [
    "Ultra-orphan drugs",
    "Cell and gene therapies",
    "Complex REMS requirements",
    "Extreme cold chain needs"
  ],
  
  "payer_considerations": {
    "network": "Must include designated pharmacy",
    "pricing": "Limited negotiation",
    "member_access": "Typically mail/delivery"
  }
}
```

---

## Hub Model Patterns

### Full-Service Hub

```json
{
  "pattern_id": "HUB-FULL-SERVICE",
  "pattern_name": "Full-Service Hub",
  "description": "Comprehensive patient support and coordination hub",
  
  "hub_services": {
    "patient_enrollment": {
      "enrollment_intake": true,
      "consent_management": true,
      "patient_demographics": true,
      "prescriber_verification": true
    },
    
    "benefit_investigation": {
      "insurance_verification": true,
      "prior_authorization_support": true,
      "appeals_support": true,
      "coverage_determination": true
    },
    
    "financial_assistance": {
      "copay_assistance": true,
      "foundation_referral": true,
      "manufacturer_pap": true,
      "bridge_program": true
    },
    
    "clinical_support": {
      "patient_education": true,
      "nurse_counseling": true,
      "adherence_monitoring": true,
      "side_effect_management": true
    },
    
    "logistics": {
      "pharmacy_coordination": true,
      "delivery_scheduling": true,
      "temperature_monitoring": true,
      "injection_training": true
    }
  },
  
  "hub_operators": [
    {"name": "Lash Group", "parent": "AmerisourceBergen"},
    {"name": "Conduent", "parent": "Conduent"},
    {"name": "TrialCard", "parent": "TrialCard"},
    {"name": "ConnectiveRx", "parent": "ConnectiveRx"},
    {"name": "McKesson Patient Relationship Solutions", "parent": "McKesson"}
  ],
  
  "data_reporting": {
    "enrollment_metrics": true,
    "time_to_therapy": true,
    "adherence_rates": true,
    "program_utilization": true
  }
}
```

### Limited Hub (BI/PA Only)

```json
{
  "pattern_id": "HUB-LIMITED",
  "pattern_name": "Limited Hub (BI/PA)",
  "description": "Focused on benefit investigation and prior authorization",
  
  "hub_services": {
    "benefit_investigation": {
      "insurance_verification": true,
      "prior_authorization_support": true,
      "appeals_support": true,
      "coverage_determination": true
    },
    
    "limited_financial": {
      "copay_card_enrollment": true,
      "foundation_referral": false,
      "pap": false
    },
    
    "clinical_support": {
      "patient_education": false,
      "nurse_counseling": false
    },
    
    "logistics": {
      "pharmacy_coordination": true,
      "direct_dispensing": false
    }
  },
  
  "use_cases": [
    "Lower-cost specialty drugs",
    "Established therapeutic areas",
    "Drugs with simpler administration"
  ]
}
```

### Hub + Dispensing Pharmacy

```json
{
  "pattern_id": "HUB-DISPENSING",
  "pattern_name": "Hub with Integrated Dispensing",
  "description": "Hub provides services and dispenses medication",
  
  "hub_services": {
    "all_full_service_hub": true,
    "integrated_dispensing": {
      "pharmacy_license": true,
      "accreditation": "URAC, ACHC",
      "direct_delivery": true,
      "clinical_pharmacist": true
    }
  },
  
  "workflow": {
    "enrollment": "Hub intake",
    "benefit_verification": "Hub BI team",
    "prior_authorization": "Hub PA team",
    "prescription_processing": "Hub pharmacy",
    "delivery": "Hub logistics",
    "clinical_follow_up": "Hub nurses"
  },
  
  "advantages": [
    "Single point of contact",
    "Faster time to therapy",
    "Unified patient experience",
    "Comprehensive data"
  ],
  
  "examples": [
    "Many orphan drug programs",
    "Cell and gene therapy programs"
  ]
}
```

---

## Site-of-Care Patterns

### Medical Benefit (Buy and Bill)

```json
{
  "pattern_id": "SOC-MEDICAL",
  "pattern_name": "Medical Benefit - Buy and Bill",
  "description": "Provider purchases, administers, and bills payer",
  
  "workflow": {
    "acquisition": "Provider purchases from distributor",
    "inventory": "Provider holds inventory",
    "administration": "Provider administers",
    "billing": "Claim under medical benefit"
  },
  
  "billing_details": {
    "drug_code": "J-code (HCPCS)",
    "administration_code": "Separate administration code",
    "place_of_service": "11 (Office), 22 (Hospital OP)",
    "reimbursement": "ASP + 6% (Medicare), Contracted (Commercial)"
  },
  
  "typical_settings": [
    "Hospital outpatient department",
    "Physician office infusion",
    "Oncology practice",
    "Rheumatology practice"
  ],
  
  "typical_drugs": [
    "IV infusions",
    "Injectable biologics",
    "Oncology treatments",
    "Complex infusions requiring monitoring"
  ],
  
  "payer_considerations": {
    "cost": "Often highest cost site",
    "340b_exposure": "Hospital HOPD may use 340B",
    "control": "Limited formulary control"
  }
}
```

### Specialty Pharmacy (White Bagging)

```json
{
  "pattern_id": "SOC-WHITE-BAG",
  "pattern_name": "White Bagging",
  "description": "Specialty pharmacy ships to provider for administration",
  
  "workflow": {
    "prescription": "Provider prescribes",
    "dispensing": "Specialty pharmacy fills",
    "shipping": "Ships to provider site",
    "administration": "Provider administers",
    "billing": "Pharmacy benefit for drug, Medical for admin"
  },
  
  "billing_split": {
    "drug": {
      "benefit": "Pharmacy",
      "billed_by": "Specialty pharmacy",
      "code": "NDC"
    },
    "administration": {
      "benefit": "Medical",
      "billed_by": "Provider",
      "code": "96413 (infusion), 96372 (injection)"
    }
  },
  
  "advantages": {
    "payer": [
      "Lower drug cost via specialty contracts",
      "Formulary control",
      "Utilization management",
      "Rebate capture"
    ],
    "member": [
      "Lower cost sharing (often)",
      "Counts toward Rx OOP"
    ]
  },
  
  "challenges": {
    "provider": [
      "Inventory management",
      "Waste concerns",
      "Workflow disruption",
      "Revenue loss"
    ],
    "logistics": [
      "Temperature control",
      "Timing coordination",
      "Unused product handling"
    ]
  },
  
  "provider_acceptance": "Variable, often resisted by hospitals"
}
```

### Home Infusion

```json
{
  "pattern_id": "SOC-HOME",
  "pattern_name": "Home Infusion",
  "description": "Drug administered in patient's home",
  
  "workflow": {
    "prescription": "Provider prescribes",
    "dispensing": "Home infusion pharmacy fills",
    "delivery": "Delivered to patient home",
    "administration": "Home infusion nurse or self-admin",
    "monitoring": "Ongoing clinical support"
  },
  
  "clinical_services": {
    "nursing": {
      "initial_training": true,
      "infusion_visits": "Per protocol",
      "monitoring_calls": true
    },
    "pharmacist": {
      "clinical_review": true,
      "drug_information": true,
      "care_coordination": true
    }
  },
  
  "billing": {
    "drug": "Pharmacy or medical benefit",
    "nursing": "Medical benefit",
    "supplies": "Bundled or separate"
  },
  
  "typical_drugs": [
    "IVIG",
    "Enzyme replacement therapies",
    "Some biologics",
    "Antibiotics (infectious disease)",
    "TPN/PPN"
  ],
  
  "advantages": [
    "Patient convenience",
    "Lower cost than hospital",
    "Improved quality of life"
  ],
  
  "patient_requirements": [
    "Stable condition",
    "Appropriate home environment",
    "Caregiver availability (if needed)",
    "No high-risk reactions expected"
  ]
}
```

### Ambulatory Infusion Center

```json
{
  "pattern_id": "SOC-AIC",
  "pattern_name": "Ambulatory Infusion Center",
  "description": "Freestanding outpatient infusion site",
  
  "characteristics": {
    "ownership": "Independent, health system, or PBM-affiliated",
    "setting": "Freestanding facility",
    "staffing": "Nurses and pharmacists",
    "hours": "Extended, often weekends"
  },
  
  "workflow": {
    "referral": "Provider refers patient",
    "scheduling": "AIC schedules",
    "drug_acquisition": "AIC acquires or white bag",
    "administration": "AIC nurses",
    "billing": "Varies by arrangement"
  },
  
  "cost_position": {
    "vs_hospital": "30-50% lower",
    "vs_physician_office": "Similar or lower",
    "vs_home": "Similar or higher"
  },
  
  "payer_strategy": {
    "preferred_site": true,
    "tiered_benefits": "Lower cost sharing for AIC",
    "narrow_network": "AIC-only for select drugs",
    "quality_requirements": "URAC accreditation"
  },
  
  "examples": [
    "Option Care Health",
    "Orsini",
    "Amber Specialty Pharmacy",
    "Health system-owned AICs"
  ]
}
```

---

## Site-of-Care Optimization Pattern

```json
{
  "pattern_id": "SOC-OPTIMIZATION",
  "pattern_name": "Site-of-Care Optimization Program",
  "description": "Comprehensive program to steer to most appropriate site",
  
  "program_components": {
    "clinical_review": {
      "trigger": "Prior authorization for infused drugs",
      "assessment": [
        "Drug characteristics",
        "Patient clinical status",
        "Reaction history",
        "Home environment"
      ]
    },
    
    "site_determination": {
      "algorithm": {
        "first_line": "Home infusion if appropriate",
        "second_line": "Ambulatory infusion center",
        "third_line": "Physician office",
        "last_resort": "Hospital outpatient"
      },
      "clinical_override": "For safety or patient needs"
    },
    
    "benefit_tiering": {
      "home_aic": {
        "tier": "Preferred",
        "copay": "Base copay"
      },
      "physician_office": {
        "tier": "Standard",
        "copay": "1.5x base"
      },
      "hospital_outpatient": {
        "tier": "Non-Preferred",
        "copay": "2x base or coinsurance"
      }
    },
    
    "provider_engagement": {
      "education": "Site-of-care benefits",
      "network": "Preferred site network",
      "incentives": "Value-based arrangements"
    },
    
    "patient_engagement": {
      "education": "Cost and convenience",
      "navigation": "Site selection assistance",
      "transportation": "If needed for preferred site"
    }
  },
  
  "savings_potential": {
    "drugs_targeted": "High-cost infusions ($10K+ per administration)",
    "typical_savings": "15-25% of drug spend for targeted drugs",
    "volume": "5-10% of specialty drug members"
  }
}
```

---

## REMS Distribution Pattern

```json
{
  "pattern_id": "REMS-DISTRIBUTION",
  "pattern_name": "REMS Restricted Distribution",
  "description": "FDA-mandated restricted distribution for safety",
  
  "rems_elements": {
    "etasu": {
      "description": "Elements to Assure Safe Use",
      "components": [
        "Prescriber certification",
        "Pharmacy certification",
        "Patient enrollment",
        "Dispensing requirements",
        "Monitoring requirements"
      ]
    }
  },
  
  "certification_requirements": {
    "prescriber": {
      "enrollment": "Register with REMS program",
      "training": "Complete training module",
      "agreement": "Sign prescriber agreement",
      "recertification": "Periodic renewal"
    },
    "pharmacy": {
      "enrollment": "Register with REMS program",
      "training": "Staff complete training",
      "systems": "Dispense verification system",
      "reporting": "Adverse event reporting"
    },
    "patient": {
      "enrollment": "Patient enrollment form",
      "counseling": "Documented counseling",
      "consent": "Informed consent",
      "monitoring": "Required labs/tests"
    }
  },
  
  "dispensing_workflow": {
    "pre_dispense": [
      "Verify prescriber certified",
      "Verify patient enrolled",
      "Confirm monitoring complete",
      "Check authorization code"
    ],
    "dispense": [
      "Document in REMS system",
      "Patient counseling",
      "Provide patient materials"
    ],
    "post_dispense": [
      "Report to REMS program",
      "Adverse event monitoring"
    ]
  },
  
  "example_programs": [
    {
      "program": "iPLEDGE",
      "drug": "Isotretinoin",
      "key_requirement": "Pregnancy prevention"
    },
    {
      "program": "Clozapine REMS",
      "drug": "Clozapine",
      "key_requirement": "ANC monitoring"
    },
    {
      "program": "THALOMID REMS",
      "drug": "Thalidomide",
      "key_requirement": "Pregnancy prevention"
    },
    {
      "program": "LEMTRADA REMS",
      "drug": "Alemtuzumab",
      "key_requirement": "Monitoring for autoimmune conditions"
    }
  ],
  
  "payer_considerations": {
    "pa_integration": "Verify REMS compliance in PA",
    "network": "Only certified pharmacies",
    "claims": "REMS indicator field"
  }
}
```

---

## Example: Complete Specialty Distribution Configuration

**Prompt**: "Generate specialty distribution configuration for new oncology drug"

```json
{
  "drug": {
    "name": "Oncomax",
    "generic_name": "fictizumab",
    "route": "IV infusion",
    "frequency": "Every 3 weeks",
    "wac_per_dose": 18500,
    "annual_cost": 296000
  },
  
  "distribution_model": {
    "type": "Limited Distribution",
    "pharmacy_count": 8,
    "selection_criteria": [
      "Oncology specialty accreditation",
      "Cold chain capability (-20°C)",
      "24/7 pharmacist availability",
      "Patient education capability",
      "REMS certification"
    ]
  },
  
  "hub_configuration": {
    "hub_provider": "Lash Group",
    "services": {
      "patient_enrollment": true,
      "benefit_investigation": true,
      "prior_authorization": true,
      "financial_assistance": true,
      "nurse_support": true,
      "pharmacy_coordination": true
    },
    "sla": {
      "enrollment_to_bi_complete": "48 hours",
      "pa_submission": "24 hours from BI",
      "time_to_therapy_target": "14 days"
    }
  },
  
  "site_of_care": {
    "approved_sites": [
      "Oncologist office (preferred)",
      "Hospital outpatient (if needed)",
      "Ambulatory infusion center (approved list)"
    ],
    "home_infusion": false,
    "rationale": "Infusion reaction monitoring required"
  },
  
  "specialty_pharmacy_network": [
    {
      "pharmacy": "CVS Specialty",
      "exclusive": false,
      "services": ["Dispensing", "Patient support"]
    },
    {
      "pharmacy": "Accredo",
      "exclusive": false,
      "services": ["Dispensing", "Patient support"]
    },
    {
      "pharmacy": "Biologics by McKesson",
      "exclusive": false,
      "services": ["Dispensing", "Patient support"]
    }
  ],
  
  "fulfillment_model": {
    "primary": "White bagging to oncology practice",
    "alternative": "Brown bagging for select patients",
    "buy_and_bill": "Allowed for contracted sites"
  },
  
  "clinical_programs": {
    "prior_authorization": {
      "required": true,
      "criteria": [
        "Confirmed diagnosis with biopsy",
        "Biomarker positive",
        "Prior therapy requirement"
      ]
    },
    "adherence_program": {
      "nurse_calls": "Pre-infusion reminder",
      "monitoring": "Lab tracking"
    },
    "side_effect_management": {
      "protocol": "Manufacturer-provided",
      "nurse_support": "Available 24/7"
    }
  },
  
  "payer_contracting": {
    "specialty_pharmacy_discount": "AWP - 18%",
    "white_bag_discount": "AWP - 20%",
    "340b_carve_out": true,
    "rebate_agreement": "Yes, outcomes-based"
  }
}
```

---

## Validation Checklist

| Requirement | Validation |
|-------------|------------|
| Distribution Type | Matches drug characteristics |
| Hub Services | Appropriate for drug complexity |
| Pharmacy Network | Includes authorized pharmacies |
| Site of Care | Clinically appropriate options |
| REMS Compliance | If applicable, fully addressed |
| Member Access | Geographic access adequate |

---

## Related Skills

- [Specialty Pharmacy](../reference/specialty-pharmacy.md) - Specialty pharmacy concepts
- [Synthetic Pharmacy](../synthetic/synthetic-pharmacy.md) - Generate specialty pharmacies
- [Pharmacy Benefit Patterns](pharmacy-benefit-patterns.md) - Tier and formulary patterns
- [Synthetic Pharmacy Benefit](../synthetic/synthetic-pharmacy-benefit.md) - Generate benefits

---

*Specialty Distribution Pattern is a template skill in the NetworkSim product.*
