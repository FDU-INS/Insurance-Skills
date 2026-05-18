---
name: synthetic-pharmacy
description: |
  Generate realistic synthetic pharmacy entities including retail pharmacies,
  mail-order pharmacies, specialty pharmacies, and hospital pharmacies.
  Includes NCPDP Provider ID, DEA number, NPI, chain affiliation, and services.
  
  Trigger phrases: "generate pharmacy", "create drugstore", "synthetic NCPDP",
  "generate specialty pharmacy", "mail order pharmacy", "retail pharmacy",
  "CVS", "Walgreens", "hospital pharmacy", "compounding pharmacy", "340B pharmacy"
version: "1.0"
category: synthetic
related_skills:
  - pharmacy-benefit-concepts
  - specialty-pharmacy
  - synthetic-provider
  - pharmacy-for-rx
cross_product:
  - rxmembersim: Dispensing pharmacy for claims
  - patientsim: Medication dispensing location
  - membersim: Pharmacy network status
---

# Synthetic Pharmacy Generation

## Overview

Generate realistic synthetic pharmacy entities for use across the HealthSim ecosystem. Pharmacies are identified by NCPDP Provider ID (7 digits) and NPI (10 digits), with additional identifiers for DEA registration and state licenses.

This skill generates the **canonical pharmacy entity** that can be:
- Used directly as JSON
- Transformed to NCPDP provider format
- Flattened to pharmacy directory CSV
- Integrated into RxMemberSim claims

---

## Trigger Phrases

Use this skill when you see:
- "Generate a pharmacy"
- "Create a retail pharmacy in Seattle"
- "Generate a specialty pharmacy for oncology"
- "Create a mail-order pharmacy"
- "Generate a 340B pharmacy"
- "Create a compounding pharmacy"
- "Generate a hospital outpatient pharmacy"

---

## Pharmacy Types

### Retail Pharmacies

| Type | Description | Characteristics |
|------|-------------|-----------------|
| Chain | CVS, Walgreens, Rite Aid | High volume, standardized, extended hours |
| Grocery | Kroger, Safeway, Publix | Co-located with grocery, moderate volume |
| Mass Merchant | Walmart, Costco, Target | High volume, competitive pricing |
| Independent | Single-location owner | Personalized service, community-focused |
| Franchise | Medicine Shoppe, Health Mart | Independent with brand support |

### Specialty Pharmacies

| Type | Description | Characteristics |
|------|-------------|-----------------|
| Standalone | Dedicated specialty | Limited distribution, clinical services |
| Health System | Hospital-affiliated | Integrated care, 340B eligible |
| PBM-Owned | CVS Specialty, Express Scripts | Closed network, mail + limited retail |
| Manufacturer | Direct distribution | Single product focus |

### Mail-Order Pharmacies

| Type | Description | Characteristics |
|------|-------------|-----------------|
| PBM Mail | Express Scripts, OptumRx | 90-day supply, maintenance meds |
| Retail Mail | CVS Caremark, Walgreens | Hybrid retail/mail model |
| Digital-First | Amazon Pharmacy, Capsule | App-based, delivery focused |

### Institutional Pharmacies

| Type | Description | Characteristics |
|------|-------------|-----------------|
| Hospital Inpatient | Acute care medication | Unit-dose, IV admixture |
| Hospital Outpatient | Discharge, clinic | 340B eligible, specialty |
| Long-term Care | SNF, assisted living | Consultant services, packaging |
| Compounding | Custom formulations | Sterile and non-sterile |

---

## Generation Parameters

### Required Context

| Parameter | Description | Default |
|-----------|-------------|---------|
| **pharmacy_type** | Type of pharmacy | Retail Chain |
| **location** | City, state, or county | Random US location |

### Optional Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **chain** | Chain/banner name | Random based on type |
| **services** | Array of services | Based on type |
| **hours** | Operating hours | Based on type |
| **specialty_focus** | Therapeutic areas | None for retail |
| **340b_participation** | 340B Drug Program | Based on type |
| **preferred_network** | Network tier status | Standard |
| **languages** | Staff languages | ["English"] |

---

## Canonical Schema

### Retail Pharmacy

```json
{
  "ncpdp_provider_id": "string (7 digits)",
  "npi": "string (10 digits, Luhn-valid)",
  "dea_number": "string (9 char, 2 letters + 7 digits)",
  "pharmacy_type": "Retail",
  "pharmacy_subtype": "Chain | Independent | Grocery | Mass Merchant",
  "name": "string",
  "doing_business_as": "string",
  "chain_affiliation": {
    "chain_name": "string",
    "chain_code": "string (3-4 char)",
    "store_number": "string",
    "region": "string",
    "district": "string"
  },
  "address": {
    "street_address": "string",
    "street_address_2": "string (optional)",
    "city": "string",
    "state": "string (2 char)",
    "zip": "string (5 or 9 digits)",
    "county": "string",
    "county_fips": "string (5 digits)",
    "latitude": "number",
    "longitude": "number"
  },
  "contact": {
    "main_phone": "string (10 digits)",
    "fax": "string (10 digits)",
    "pharmacy_phone": "string (optional, if different)"
  },
  "hours": {
    "monday": {"open": "HH:MM", "close": "HH:MM"},
    "tuesday": {"open": "HH:MM", "close": "HH:MM"},
    "wednesday": {"open": "HH:MM", "close": "HH:MM"},
    "thursday": {"open": "HH:MM", "close": "HH:MM"},
    "friday": {"open": "HH:MM", "close": "HH:MM"},
    "saturday": {"open": "HH:MM", "close": "HH:MM"},
    "sunday": {"open": "HH:MM", "close": "HH:MM"},
    "twenty_four_hour": "boolean",
    "holiday_hours": "string (optional)"
  },
  "services": {
    "prescription_filling": true,
    "immunizations": "boolean",
    "medication_therapy_management": "boolean",
    "compounding": "boolean",
    "drive_through": "boolean",
    "delivery": "boolean",
    "curbside_pickup": "boolean",
    "covid_testing": "boolean",
    "clinical_services": ["string"]
  },
  "dispensing": {
    "ninety_day_supply": "boolean",
    "controlled_substances": "boolean",
    "specialty_medications": "boolean",
    "opioid_treatment": "boolean"
  },
  "network_participation": {
    "medicare_part_d": "boolean",
    "medicaid": "boolean",
    "network_tier": "Preferred | Standard | Non-preferred",
    "pbm_contracts": ["string"]
  },
  "licenses": [
    {
      "state": "string (2 char)",
      "license_number": "string",
      "status": "Active | Inactive",
      "expiration": "YYYY-MM-DD"
    }
  ],
  "pharmacist_in_charge": {
    "last_name": "string",
    "first_name": "string",
    "license_number": "string"
  },
  "staff": {
    "pharmacist_count": "integer",
    "technician_count": "integer",
    "languages": ["string"]
  },
  "volume": {
    "prescriptions_per_week": "integer",
    "specialty_percentage": "number (0-1)"
  },
  "accreditation": {
    "urac_accredited": "boolean",
    "achc_accredited": "boolean",
    "accreditation_types": ["string"]
  },
  "last_update": "YYYY-MM-DD"
}
```

### Specialty Pharmacy

```json
{
  "ncpdp_provider_id": "string (7 digits)",
  "npi": "string (10 digits)",
  "dea_number": "string",
  "pharmacy_type": "Specialty",
  "pharmacy_subtype": "Standalone | Health System | PBM-Owned | Manufacturer",
  "name": "string",
  "address": {
    "street_address": "string",
    "city": "string",
    "state": "string",
    "zip": "string",
    "county_fips": "string"
  },
  "contact": {
    "main_phone": "string",
    "fax": "string",
    "clinical_phone": "string",
    "patient_services_phone": "string"
  },
  "therapeutic_focus": [
    {
      "area": "string",
      "conditions": ["string"],
      "key_medications": ["string"]
    }
  ],
  "specialty_services": {
    "prior_authorization_support": "boolean",
    "benefits_investigation": "boolean",
    "financial_assistance": "boolean",
    "copay_assistance": "boolean",
    "patient_education": "boolean",
    "adherence_monitoring": "boolean",
    "outcomes_tracking": "boolean",
    "clinical_pharmacist_consultation": "boolean",
    "nursing_support": "boolean",
    "home_infusion": "boolean"
  },
  "distribution": {
    "limited_distribution_drugs": "boolean",
    "rems_certified": "boolean",
    "rems_programs": ["string"],
    "cold_chain_capable": "boolean",
    "next_day_delivery": "boolean",
    "same_day_delivery": "boolean"
  },
  "hub_services": {
    "hub_partner": "boolean",
    "manufacturer_contracts": ["string"],
    "patient_enrollment": "boolean"
  },
  "network_participation": {
    "exclusive_networks": ["string"],
    "preferred_specialty_network": "boolean",
    "pbm_contracts": ["string"]
  },
  "accreditation": {
    "urac_specialty": "boolean",
    "urac_specialty_expiration": "YYYY-MM-DD",
    "achc_specialty": "boolean",
    "joint_commission": "boolean",
    "nabp_verified": "boolean"
  },
  "health_system_affiliation": {
    "name": "string (optional)",
    "system_id": "string (optional)",
    "integrated_ehr": "boolean"
  },
  "340b_participation": {
    "enrolled": "boolean",
    "entity_type": "string",
    "id_340b": "string"
  }
}
```

### Mail-Order Pharmacy

```json
{
  "ncpdp_provider_id": "string (7 digits)",
  "npi": "string (10 digits)",
  "dea_number": "string",
  "pharmacy_type": "Mail Order",
  "pharmacy_subtype": "PBM | Retail | Digital-First",
  "name": "string",
  "corporate_address": {
    "street_address": "string",
    "city": "string",
    "state": "string",
    "zip": "string"
  },
  "distribution_centers": [
    {
      "name": "string",
      "address": {
        "city": "string",
        "state": "string",
        "zip": "string"
      },
      "states_served": ["string"],
      "capacity_prescriptions_per_day": "integer"
    }
  ],
  "contact": {
    "customer_service": "string",
    "pharmacist_line": "string",
    "fax": "string",
    "website": "string",
    "mobile_app": "boolean"
  },
  "services": {
    "auto_refill": "boolean",
    "medication_synchronization": "boolean",
    "ninety_day_supply": true,
    "pill_packaging": "boolean",
    "medication_reminders": "boolean",
    "pharmacist_chat": "boolean",
    "video_consultation": "boolean"
  },
  "shipping": {
    "standard_shipping_days": "integer",
    "expedited_available": "boolean",
    "signature_required_controlled": "boolean",
    "temperature_controlled": "boolean",
    "tracking_provided": "boolean"
  },
  "network_participation": {
    "pbm_affiliation": "string",
    "exclusive_mail": "boolean",
    "maintenance_choice": "boolean"
  },
  "licenses": [
    {
      "state": "string",
      "license_number": "string",
      "status": "Active"
    }
  ],
  "volume": {
    "prescriptions_per_month": "integer"
  }
}
```

---

## NCPDP Provider ID Generation

### Format

- 7 digits
- Assigned sequentially by NCPDP
- No check digit requirement

### Generation Pattern

```
Position 1-7: Sequential or random 7 digits
Range: 1000000 - 9999999
```

### Chain Numbering Patterns

Major chains have assigned ranges (approximated):

| Chain | Typical Range |
|-------|---------------|
| CVS | 3000000-3499999 |
| Walgreens | 4000000-4499999 |
| Walmart | 5000000-5299999 |
| Rite Aid | 3500000-3699999 |
| Kroger | 6000000-6299999 |

---

## DEA Number Generation

### Format

- 9 characters: 2 letters + 7 digits
- First letter: Registrant type
- Second letter: First letter of last name (individual) or business name (organization)
- Digits 1-6: Assigned number
- Digit 7: Check digit

### Registrant Type Codes

| Code | Type |
|------|------|
| A, B, F | Dispensers (pharmacies, hospitals) |
| M | Mid-level practitioners |
| P | Manufacturers |
| R | Researchers |
| X | Narcotic treatment programs |

### Check Digit Calculation

```
DEA: AB1234563

1. Sum of digits 1, 3, 5: 1 + 3 + 5 = 9
2. Sum of digits 2, 4, 6 × 2: (2 + 4 + 6) × 2 = 24
3. Total: 9 + 24 = 33
4. Check digit = last digit of total = 3
```

---

## Examples

### Example 1: Retail Chain Pharmacy

**Prompt**: "Generate a CVS pharmacy in suburban Chicago"

**Response**:

```json
{
  "ncpdp_provider_id": "3245678",
  "npi": "1234567890",
  "dea_number": "BC1234563",
  "pharmacy_type": "Retail",
  "pharmacy_subtype": "Chain",
  "name": "CVS Pharmacy #8234",
  "doing_business_as": "CVS Pharmacy",
  "chain_affiliation": {
    "chain_name": "CVS Health",
    "chain_code": "CVS",
    "store_number": "8234",
    "region": "Midwest",
    "district": "Chicago North"
  },
  "address": {
    "street_address": "2900 North Milwaukee Avenue",
    "city": "Northbrook",
    "state": "IL",
    "zip": "60062",
    "county": "Cook",
    "county_fips": "17031",
    "latitude": 42.1275,
    "longitude": -87.8289
  },
  "contact": {
    "main_phone": "8475591234",
    "fax": "8475591235",
    "pharmacy_phone": "8475591236"
  },
  "hours": {
    "monday": {"open": "08:00", "close": "22:00"},
    "tuesday": {"open": "08:00", "close": "22:00"},
    "wednesday": {"open": "08:00", "close": "22:00"},
    "thursday": {"open": "08:00", "close": "22:00"},
    "friday": {"open": "08:00", "close": "22:00"},
    "saturday": {"open": "09:00", "close": "21:00"},
    "sunday": {"open": "10:00", "close": "18:00"},
    "twenty_four_hour": false
  },
  "services": {
    "prescription_filling": true,
    "immunizations": true,
    "medication_therapy_management": true,
    "compounding": false,
    "drive_through": true,
    "delivery": true,
    "curbside_pickup": true,
    "covid_testing": true,
    "clinical_services": ["Flu shots", "COVID vaccines", "Blood pressure screening", "A1C testing"]
  },
  "dispensing": {
    "ninety_day_supply": true,
    "controlled_substances": true,
    "specialty_medications": false,
    "opioid_treatment": false
  },
  "network_participation": {
    "medicare_part_d": true,
    "medicaid": true,
    "network_tier": "Preferred",
    "pbm_contracts": ["CVS Caremark", "Express Scripts", "OptumRx"]
  },
  "licenses": [
    {
      "state": "IL",
      "license_number": "054-012345",
      "status": "Active",
      "expiration": "2025-07-31"
    }
  ],
  "pharmacist_in_charge": {
    "last_name": "Chen",
    "first_name": "Lisa",
    "license_number": "051-123456"
  },
  "staff": {
    "pharmacist_count": 3,
    "technician_count": 5,
    "languages": ["English", "Spanish", "Mandarin"]
  },
  "volume": {
    "prescriptions_per_week": 2200,
    "specialty_percentage": 0.02
  },
  "last_update": "2024-06-15"
}
```

---

### Example 2: Specialty Pharmacy

**Prompt**: "Generate an oncology specialty pharmacy affiliated with a health system in Houston"

**Response**:

```json
{
  "ncpdp_provider_id": "7891234",
  "npi": "1456789012",
  "dea_number": "BH2345674",
  "pharmacy_type": "Specialty",
  "pharmacy_subtype": "Health System",
  "name": "MD Anderson Specialty Pharmacy",
  "address": {
    "street_address": "1515 Holcombe Boulevard",
    "street_address_2": "Unit 446",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "county": "Harris",
    "county_fips": "48201"
  },
  "contact": {
    "main_phone": "7137453456",
    "fax": "7137453457",
    "clinical_phone": "7137453458",
    "patient_services_phone": "8885551234"
  },
  "therapeutic_focus": [
    {
      "area": "Oncology",
      "conditions": ["Breast Cancer", "Lung Cancer", "Colorectal Cancer", "Leukemia", "Lymphoma", "Multiple Myeloma"],
      "key_medications": ["Ibrance", "Keytruda", "Opdivo", "Revlimid", "Imbruvica", "Venetoclax"]
    },
    {
      "area": "Hematology",
      "conditions": ["Sickle Cell Disease", "Hemophilia", "ITP"],
      "key_medications": ["Oxbryta", "Hemlibra", "Promacta"]
    }
  ],
  "specialty_services": {
    "prior_authorization_support": true,
    "benefits_investigation": true,
    "financial_assistance": true,
    "copay_assistance": true,
    "patient_education": true,
    "adherence_monitoring": true,
    "outcomes_tracking": true,
    "clinical_pharmacist_consultation": true,
    "nursing_support": true,
    "home_infusion": false
  },
  "distribution": {
    "limited_distribution_drugs": true,
    "rems_certified": true,
    "rems_programs": ["Thalomid REMS", "Revlimid REMS", "Pomalyst REMS", "TIRF REMS"],
    "cold_chain_capable": true,
    "next_day_delivery": true,
    "same_day_delivery": true
  },
  "hub_services": {
    "hub_partner": true,
    "manufacturer_contracts": ["BMS Access Support", "Pfizer Oncology Together", "Lilly Oncology"],
    "patient_enrollment": true
  },
  "network_participation": {
    "exclusive_networks": [],
    "preferred_specialty_network": true,
    "pbm_contracts": ["CVS Specialty", "Express Scripts Specialty", "OptumRx Specialty"]
  },
  "accreditation": {
    "urac_specialty": true,
    "urac_specialty_expiration": "2025-12-31",
    "achc_specialty": true,
    "joint_commission": false,
    "nabp_verified": true
  },
  "health_system_affiliation": {
    "name": "MD Anderson Cancer Center",
    "system_id": "MDACC",
    "integrated_ehr": true
  },
  "340b_participation": {
    "enrolled": true,
    "entity_type": "Cancer Hospital",
    "id_340b": "TX1234"
  },
  "staff": {
    "pharmacist_count": 12,
    "technician_count": 20,
    "clinical_pharmacists": 6,
    "nurses": 4,
    "patient_navigators": 8
  }
}
```

---

### Example 3: Independent Community Pharmacy

**Prompt**: "Generate an independent pharmacy in a small town in Vermont"

**Response**:

```json
{
  "ncpdp_provider_id": "1234567",
  "npi": "1678901234",
  "dea_number": "BM3456785",
  "pharmacy_type": "Retail",
  "pharmacy_subtype": "Independent",
  "name": "Middlebury Pharmacy",
  "doing_business_as": "Middlebury Pharmacy & Gifts",
  "address": {
    "street_address": "63 Main Street",
    "city": "Middlebury",
    "state": "VT",
    "zip": "05753",
    "county": "Addison",
    "county_fips": "50001",
    "latitude": 44.0154,
    "longitude": -73.1677
  },
  "contact": {
    "main_phone": "8023881234",
    "fax": "8023881235"
  },
  "hours": {
    "monday": {"open": "09:00", "close": "18:00"},
    "tuesday": {"open": "09:00", "close": "18:00"},
    "wednesday": {"open": "09:00", "close": "18:00"},
    "thursday": {"open": "09:00", "close": "18:00"},
    "friday": {"open": "09:00", "close": "18:00"},
    "saturday": {"open": "09:00", "close": "14:00"},
    "sunday": {"open": null, "close": null},
    "twenty_four_hour": false
  },
  "services": {
    "prescription_filling": true,
    "immunizations": true,
    "medication_therapy_management": true,
    "compounding": true,
    "drive_through": false,
    "delivery": true,
    "curbside_pickup": true,
    "covid_testing": false,
    "clinical_services": ["Medication reviews", "Blister packaging", "Pet medications"]
  },
  "dispensing": {
    "ninety_day_supply": true,
    "controlled_substances": true,
    "specialty_medications": false,
    "opioid_treatment": false
  },
  "network_participation": {
    "medicare_part_d": true,
    "medicaid": true,
    "network_tier": "Standard",
    "pbm_contracts": ["PSAO Alliance", "Express Scripts", "OptumRx"]
  },
  "licenses": [
    {
      "state": "VT",
      "license_number": "PHR-1234",
      "status": "Active",
      "expiration": "2025-12-31"
    }
  ],
  "pharmacist_in_charge": {
    "last_name": "Morrison",
    "first_name": "James",
    "license_number": "RPH-5678"
  },
  "staff": {
    "pharmacist_count": 2,
    "technician_count": 3,
    "languages": ["English", "French"]
  },
  "volume": {
    "prescriptions_per_week": 450,
    "specialty_percentage": 0.00
  },
  "buying_group": {
    "name": "Good Neighbor Pharmacy",
    "psao": "McKesson"
  },
  "last_update": "2024-03-01"
}
```

---

### Example 4: Mail-Order Pharmacy

**Prompt**: "Generate a PBM mail-order pharmacy"

**Response**:

```json
{
  "ncpdp_provider_id": "9876543",
  "npi": "1890123456",
  "dea_number": "BE4567896",
  "pharmacy_type": "Mail Order",
  "pharmacy_subtype": "PBM",
  "name": "Express Scripts Pharmacy",
  "corporate_address": {
    "street_address": "One Express Way",
    "city": "St. Louis",
    "state": "MO",
    "zip": "63121"
  },
  "distribution_centers": [
    {
      "name": "Tempe Distribution Center",
      "address": {
        "city": "Tempe",
        "state": "AZ",
        "zip": "85281"
      },
      "states_served": ["AZ", "CA", "NV", "CO", "NM", "UT", "WA", "OR"],
      "capacity_prescriptions_per_day": 150000
    },
    {
      "name": "Franklin Distribution Center",
      "address": {
        "city": "Franklin",
        "state": "OH",
        "zip": "45005"
      },
      "states_served": ["OH", "IN", "MI", "KY", "PA", "WV", "NY", "NJ"],
      "capacity_prescriptions_per_day": 180000
    },
    {
      "name": "Horsham Distribution Center",
      "address": {
        "city": "Horsham",
        "state": "PA",
        "zip": "19044"
      },
      "states_served": ["PA", "NJ", "NY", "CT", "MA", "RI", "NH", "ME", "VT"],
      "capacity_prescriptions_per_day": 120000
    }
  ],
  "contact": {
    "customer_service": "8002824545",
    "pharmacist_line": "8007598340",
    "fax": "8003329872",
    "website": "https://www.express-scripts.com",
    "mobile_app": true
  },
  "services": {
    "auto_refill": true,
    "medication_synchronization": true,
    "ninety_day_supply": true,
    "pill_packaging": true,
    "medication_reminders": true,
    "pharmacist_chat": true,
    "video_consultation": true
  },
  "shipping": {
    "standard_shipping_days": 5,
    "expedited_available": true,
    "signature_required_controlled": true,
    "temperature_controlled": true,
    "tracking_provided": true
  },
  "network_participation": {
    "pbm_affiliation": "Express Scripts",
    "exclusive_mail": false,
    "maintenance_choice": true
  },
  "licenses": [
    {"state": "AZ", "license_number": "PHY-12345", "status": "Active"},
    {"state": "OH", "license_number": "PHY-23456", "status": "Active"},
    {"state": "PA", "license_number": "PHY-34567", "status": "Active"},
    {"state": "MO", "license_number": "PHY-45678", "status": "Active"}
  ],
  "volume": {
    "prescriptions_per_month": 8500000
  }
}
```

---

## Cross-Product Integration

### RxMemberSim Integration

Generate dispensing pharmacy for claims:

```
RxMemberSim Claim → NetworkSim → Pharmacy Entity

Context needed:
- Drug type (retail, specialty, controlled)
- Days supply (30 vs 90 day)
- Network requirements
- Member location (for retail)
```

**Example**:
```
"Generate a dispensing pharmacy for this specialty oncology claim"

Response includes:
- Specialty pharmacy with oncology focus
- URAC accreditation
- REMS certification if required
- Limited distribution capability
```

### PatientSim Integration

Generate pharmacy for medication history:

```
PatientSim Medication → NetworkSim → Dispensing Pharmacy

Context needed:
- Medication type
- Patient location
- Preferred pharmacy indicator
```

### MemberSim Integration

Generate pharmacy network context:

```
MemberSim Plan → NetworkSim → Pharmacy Network Status

Context needed:
- Plan pharmacy benefit design
- Preferred vs standard tier
- 90-day retail eligibility
```

---

## Validation Rules

### NCPDP Provider ID Validation

| Rule | Validation |
|------|------------|
| Length | Exactly 7 digits |
| Format | Numeric only |
| Range | 1000000-9999999 |

### DEA Number Validation

| Rule | Validation |
|------|------------|
| Length | Exactly 9 characters |
| Format | 2 letters + 7 digits |
| First Letter | Valid registrant type (A, B, F, M, P, R, X) |
| Check Digit | Must pass DEA algorithm |

### Address Validation

| Rule | Validation |
|------|------------|
| State | Valid 2-letter state code |
| ZIP | 5 digits or 9 digits (ZIP+4) |
| License State | Must have license for practice state |

### Business Rules

| Rule | Description |
|------|-------------|
| Chain Consistency | Store number format must match chain |
| Specialty Requirements | Specialty pharmacies need URAC or ACHC |
| 340B Eligibility | Only eligible entity types for 340B |
| REMS | Must be certified for REMS drugs dispensed |
| Hours Reasonability | Hours must be realistic for type |

---

## Related Skills

- [Pharmacy Benefit Concepts](../reference/pharmacy-benefit-concepts.md) - Benefit context
- [Specialty Pharmacy](../reference/specialty-pharmacy.md) - Specialty operations
- [Synthetic Provider](synthetic-provider.md) - Prescriber relationships
- [Pharmacy for Prescription](../integration/pharmacy-for-rx.md) - RxMemberSim integration

---

*Synthetic Pharmacy is a generation skill in the NetworkSim product.*
