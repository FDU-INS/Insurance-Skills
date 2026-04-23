---
name: pharmacy-for-rx
description: |
  Generate appropriate pharmacy entities for RxMemberSim prescriptions.
  Matches pharmacy type to drug characteristics, network requirements,
  and patient preferences. Handles retail, specialty, and mail-order routing.
  
  Trigger phrases: "pharmacy for this prescription", "dispense at which pharmacy",
  "specialty pharmacy for", "mail order routing", "pharmacy network for rx",
  "limited distribution pharmacy", "preferred pharmacy for"
version: "1.0"
category: integration
related_skills:
  - synthetic-pharmacy
  - specialty-distribution-pattern
  - pharmacy-benefit-patterns
cross_product:
  - rxmembersim
---

# Pharmacy for Rx

## Overview

This integration skill generates appropriate pharmacy entities for RxMemberSim prescriptions. It analyzes drug characteristics, network requirements, and patient context to route prescriptions to the correct pharmacy type.

Use this skill when you need to:
- Route prescriptions to appropriate pharmacy type
- Select specialty pharmacy for specialty drugs
- Apply mail-order routing rules
- Enforce limited distribution requirements
- Determine preferred vs standard pharmacy

---

## Integration Pattern

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   RxMemberSim   │     │   Pharmacy for       │     │   NetworkSim    │
│   Prescription  │────▶│   Rx Skill           │────▶│   Pharmacy      │
│   Context       │     │   (Routing Logic)    │     │   Entity        │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

---

## Input Context

### Prescription Context

```json
{
  "prescription_context": {
    "rx_number": "RX-2024-0012345",
    "drug": {
      "ndc": "00006-0277-31",
      "drug_name": "Keytruda",
      "generic_name": "pembrolizumab",
      "drug_class": "Antineoplastic",
      "route": "IV",
      "specialty_indicator": true,
      "limited_distribution": true,
      "rems_required": false
    },
    "prescriber": {
      "npi": "1234567890",
      "specialty": "Oncology"
    },
    "quantity": 1,
    "days_supply": 21,
    "refills_remaining": 5
  }
}
```

### Member Context

```json
{
  "member_context": {
    "member_id": "MEM-2024-001234",
    "pharmacy_benefit": {
      "pbm": "Express Scripts",
      "network_id": "ESI-PREFERRED-2024",
      "specialty_pharmacy": "Accredo",
      "mail_pharmacy": "Express Scripts Mail",
      "preferred_retail": true
    },
    "location": {
      "zip": "60601",
      "state": "IL"
    },
    "preferences": {
      "preferred_pharmacy_npi": "1987654321",
      "mail_order_enrolled": true
    }
  }
}
```

---

## Pharmacy Routing Logic

### Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│                    Pharmacy Routing                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │  Is drug specialty?          │
               │  (AWP > $1000 or             │
               │   specialty indicator)        │
               └──────────────────────────────┘
                      │              │
                     YES            NO
                      │              │
                      ▼              ▼
          ┌──────────────┐    ┌──────────────────┐
          │ Route to     │    │ Check days       │
          │ Specialty    │    │ supply           │
          │ Pharmacy     │    └──────────────────┘
          └──────────────┘           │
                 │            ┌──────┴──────┐
                 │           >30         ≤30
                 │            │            │
                 ▼            ▼            ▼
          ┌──────────────┐  ┌────────┐  ┌──────────┐
          │ Check Ltd    │  │ Mail   │  │ Retail   │
          │ Distribution │  │ Order  │  │ Pharmacy │
          └──────────────┘  │ or     │  └──────────┘
                 │          │ Retail │
                 ▼          │ 90     │
          ┌──────────────┐  └────────┘
          │ Authorized   │
          │ SP Network   │
          └──────────────┘
```

### Routing Rules

```json
{
  "routing_rules": {
    "specialty_drug": {
      "criteria": [
        "AWP per 30-day supply > $1000",
        "specialty_indicator = true",
        "Route = Injectable/Infusion",
        "Requires clinical monitoring",
        "Cold chain storage required"
      ],
      "route_to": "Specialty Pharmacy",
      "network": "Limited specialty network"
    },
    
    "limited_distribution": {
      "criteria": [
        "limited_distribution = true",
        "REMS program drug"
      ],
      "route_to": "Authorized pharmacy only",
      "network": "Manufacturer-designated"
    },
    
    "maintenance_mail": {
      "criteria": [
        "days_supply >= 30",
        "chronic/maintenance medication",
        "member enrolled in mail program",
        "fill count >= maintenance_fill_threshold"
      ],
      "route_to": "Mail Order Pharmacy",
      "incentive": "Lower copay for mail"
    },
    
    "retail_preferred": {
      "criteria": [
        "days_supply <= 30",
        "acute medication",
        "preferred_retail = true"
      ],
      "route_to": "Preferred Retail Network",
      "incentive": "Lower copay at preferred"
    },
    
    "retail_standard": {
      "criteria": [
        "Not specialty",
        "Not maintenance mail",
        "Not preferred retail"
      ],
      "route_to": "Standard Retail Network"
    }
  }
}
```

---

## Output Schema

### Retail Pharmacy Assignment

```json
{
  "pharmacy_assignment": {
    "rx_number": "RX-2024-0012345",
    "routing_type": "RETAIL_PREFERRED",
    
    "pharmacy": {
      "ncpdp_id": "3456789",
      "npi": "1987654321",
      "pharmacy_name": "CVS Pharmacy #4521",
      "chain": "CVS",
      "pharmacy_type": "Retail Chain",
      "address": {
        "street": "123 Main Street",
        "city": "Chicago",
        "state": "IL",
        "zip": "60601"
      },
      "phone": "312-555-0123"
    },
    
    "network_status": {
      "in_network": true,
      "network_tier": "Preferred",
      "network_id": "ESI-PREFERRED-2024"
    },
    
    "cost_sharing": {
      "tier": 1,
      "tier_name": "Generic",
      "copay": 10,
      "days_supply_dispensed": 30,
      "preferred_savings": 5
    },
    
    "routing_reason": "Member preferred pharmacy in network"
  }
}
```

### Mail Order Pharmacy Assignment

```json
{
  "pharmacy_assignment": {
    "rx_number": "RX-2024-0012346",
    "routing_type": "MAIL_ORDER",
    
    "pharmacy": {
      "ncpdp_id": "9999901",
      "npi": "1876543210",
      "pharmacy_name": "Express Scripts Mail Pharmacy",
      "pharmacy_type": "Mail Order",
      "address": {
        "city": "St. Louis",
        "state": "MO"
      }
    },
    
    "network_status": {
      "in_network": true,
      "network_tier": "Mail",
      "pbm_owned": true
    },
    
    "cost_sharing": {
      "tier": 2,
      "tier_name": "Preferred Brand",
      "copay": 70,
      "days_supply_dispensed": 90,
      "mail_savings": 20
    },
    
    "delivery": {
      "method": "FedEx",
      "estimated_delivery": "3-5 business days",
      "signature_required": false,
      "temperature_controlled": false
    },
    
    "routing_reason": "Maintenance medication - 90-day mail eligible"
  }
}
```

### Specialty Pharmacy Assignment

```json
{
  "pharmacy_assignment": {
    "rx_number": "RX-2024-0012347",
    "routing_type": "SPECIALTY",
    
    "pharmacy": {
      "ncpdp_id": "5678901",
      "npi": "1765432109",
      "pharmacy_name": "Accredo Specialty Pharmacy",
      "pharmacy_type": "Specialty",
      "parent_company": "Express Scripts",
      "address": {
        "city": "Memphis",
        "state": "TN"
      },
      "specialty_services": {
        "clinical_support": true,
        "24_7_pharmacist": true,
        "patient_education": true,
        "adherence_monitoring": true
      }
    },
    
    "network_status": {
      "in_network": true,
      "exclusive_specialty": true,
      "network_id": "ESI-SPECIALTY-2024"
    },
    
    "cost_sharing": {
      "tier": 4,
      "tier_name": "Specialty",
      "coinsurance": 0.25,
      "minimum": 100,
      "maximum": 400,
      "days_supply_dispensed": 30
    },
    
    "clinical_services": {
      "welcome_call": true,
      "refill_reminders": true,
      "nurse_support": true,
      "side_effect_monitoring": true
    },
    
    "delivery": {
      "method": "FedEx Priority",
      "temperature_controlled": true,
      "signature_required": true,
      "estimated_delivery": "Next business day"
    },
    
    "routing_reason": "Specialty drug - routed to exclusive specialty pharmacy"
  }
}
```

### Limited Distribution Pharmacy

```json
{
  "pharmacy_assignment": {
    "rx_number": "RX-2024-0012348",
    "routing_type": "LIMITED_DISTRIBUTION",
    
    "drug": {
      "name": "Lemtrada",
      "generic_name": "alemtuzumab",
      "rems_program": "LEMTRADA REMS"
    },
    
    "pharmacy": {
      "ncpdp_id": "7890123",
      "npi": "1654321098",
      "pharmacy_name": "BioSciences Specialty",
      "pharmacy_type": "Limited Distribution Specialty",
      "manufacturer_authorized": true,
      "rems_certified": true
    },
    
    "rems_compliance": {
      "program_name": "LEMTRADA REMS",
      "pharmacy_certified": true,
      "prescriber_certified": true,
      "patient_enrolled": true,
      "authorization_number": "LEM-2024-12345"
    },
    
    "hub_integration": {
      "hub_provider": "Sanofi Patient Connection",
      "enrollment_complete": true,
      "financial_assistance": "Copay card active"
    },
    
    "routing_reason": "REMS-restricted drug - limited distribution network"
  }
}
```

---

## Examples

### Example 1: Acute Antibiotic (Retail)

**RxMemberSim Context**:
```json
{
  "drug": {"name": "Amoxicillin 500mg", "specialty_indicator": false},
  "days_supply": 10,
  "member_location": {"zip": "60601"}
}
```

**Pharmacy Assignment**:
```json
{
  "routing_type": "RETAIL_STANDARD",
  "pharmacy": {
    "pharmacy_name": "Walgreens #1234",
    "pharmacy_type": "Retail Chain",
    "distance_miles": 0.3
  },
  "cost_sharing": {
    "tier": 1,
    "copay": 10
  },
  "routing_reason": "Acute medication - retail pharmacy"
}
```

### Example 2: Maintenance Statin (Mail Order)

**RxMemberSim Context**:
```json
{
  "drug": {"name": "Atorvastatin 40mg", "therapeutic_class": "Statin"},
  "days_supply": 90,
  "fill_number": 4,
  "member": {"mail_order_enrolled": true}
}
```

**Pharmacy Assignment**:
```json
{
  "routing_type": "MAIL_ORDER",
  "pharmacy": {
    "pharmacy_name": "CVS Caremark Mail",
    "pharmacy_type": "Mail Order"
  },
  "cost_sharing": {
    "tier": 1,
    "copay": 20,
    "days_supply": 90,
    "retail_90_copay": 30,
    "mail_savings": 10
  },
  "routing_reason": "Maintenance medication - member enrolled in mail"
}
```

### Example 3: Oncology Injectable (Specialty)

**RxMemberSim Context**:
```json
{
  "drug": {"name": "Opdivo", "ndc": "00003-3772-11", "specialty_indicator": true, "awp": 14500},
  "route": "IV Infusion",
  "days_supply": 28
}
```

**Pharmacy Assignment**:
```json
{
  "routing_type": "SPECIALTY",
  "pharmacy": {
    "pharmacy_name": "Biologics by McKesson",
    "pharmacy_type": "Specialty",
    "oncology_specialized": true
  },
  "site_of_care": {
    "dispensing_method": "White Bagging",
    "delivery_to": "Oncology clinic",
    "administration_site": "Physician office infusion"
  },
  "clinical_services": {
    "oncology_nurses": true,
    "financial_counseling": true,
    "manufacturer_copay_card": true
  },
  "routing_reason": "Oncology specialty drug - specialty pharmacy required"
}
```

### Example 4: REMS Drug (Limited Distribution)

**RxMemberSim Context**:
```json
{
  "drug": {"name": "Clozapine", "rems_required": true, "rems_program": "Clozapine REMS"},
  "member": {"rems_enrolled": true}
}
```

**Pharmacy Assignment**:
```json
{
  "routing_type": "LIMITED_DISTRIBUTION",
  "pharmacy": {
    "pharmacy_name": "REMS Certified Pharmacy",
    "rems_certified": true,
    "clozapine_certified": true
  },
  "rems_compliance": {
    "anc_monitoring_current": true,
    "last_anc_date": "2024-06-10",
    "anc_value": 2500,
    "dispensing_authorized": true
  },
  "routing_reason": "Clozapine REMS - certified pharmacy required"
}
```

---

## Pharmacy Network Preferences

### Preferred vs Standard Retail

```json
{
  "retail_network_tiers": {
    "preferred": {
      "criteria": "Higher discount, preferred contract",
      "examples": ["CVS", "Walgreens", "Rite Aid"],
      "copay_differential": -5
    },
    "standard": {
      "criteria": "Network participant, standard terms",
      "examples": ["Independent pharmacies", "Grocery"],
      "copay_differential": 0
    },
    "out_of_network": {
      "criteria": "Not contracted",
      "coverage": "Reimbursement at network rate minus differential",
      "member_pays": "Difference + higher cost share"
    }
  }
}
```

### Specialty Network Configuration

```json
{
  "specialty_network": {
    "exclusive": {
      "description": "Single specialty pharmacy required",
      "pharmacy": "Accredo",
      "enforcement": "Claims reject at non-designated"
    },
    "preferred": {
      "description": "Preferred specialty pharmacy encouraged",
      "preferred_sp": ["Accredo", "CVS Specialty"],
      "other_sp": "Higher cost sharing",
      "differential": "10% higher coinsurance"
    },
    "open": {
      "description": "Any specialty pharmacy in network",
      "cost_sharing": "Same across specialty network"
    }
  }
}
```

---

## Validation Rules

| Rule | Validation |
|------|------------|
| Specialty Classification | Drug meets specialty criteria |
| Network Status | Pharmacy in member's network |
| REMS Compliance | Pharmacy certified for REMS drugs |
| Limited Distribution | Pharmacy authorized for LD drugs |
| Days Supply | Appropriate for pharmacy type |
| Mail Eligibility | Member enrolled if mail required |

---

## Cross-Product Integration

### To RxMemberSim Claims

Pharmacy assignment flows to claim:

```json
{
  "ncpdp_claim": {
    "pharmacy_id": "3456789",
    "pharmacy_service_type": "01",
    "dispensing_status": "P",
    "service_provider_id_qualifier": "07"
  }
}
```

### From NetworkSim Pharmacy

Use [Synthetic Pharmacy](../synthetic/synthetic-pharmacy.md) to generate full entity.

---

## Related Skills

- [Synthetic Pharmacy](../synthetic/synthetic-pharmacy.md) - Generate pharmacy entities
- [Specialty Distribution Pattern](../patterns/specialty-distribution-pattern.md) - Distribution models
- [Pharmacy Benefit Patterns](../patterns/pharmacy-benefit-patterns.md) - Benefit structures
- [Formulary for Rx](formulary-for-rx.md) - Formulary context

---

*Pharmacy for Rx is an integration skill in the NetworkSim product.*
