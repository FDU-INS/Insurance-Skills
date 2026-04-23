# Provider Canonical Model

The canonical data model for healthcare providers in NetworkSim.

## Overview

A Provider represents an individual healthcare professional or organization registered in the NPPES (National Plan and Provider Enumeration System). This is the foundational entity for all provider-related operations in HealthSim.

## Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Provider",
  "type": "object",
  "required": ["npi", "entity_type", "enumeration_date"],
  "properties": {
    "npi": {
      "type": "string",
      "pattern": "^[0-9]{10}$",
      "description": "10-digit National Provider Identifier"
    },
    "entity_type": {
      "type": "string",
      "enum": ["individual", "organization"],
      "description": "1=Individual, 2=Organization"
    },
    "name": {
      "type": "object",
      "properties": {
        "last": { "type": "string" },
        "first": { "type": "string" },
        "middle": { "type": "string" },
        "prefix": { "type": "string" },
        "suffix": { "type": "string" },
        "credential": { "type": "string" }
      },
      "required": ["last"]
    },
    "organization_name": {
      "type": "string",
      "description": "For entity_type=organization"
    },
    "taxonomy": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": {
            "type": "string",
            "pattern": "^[0-9A-Z]{10}$",
            "description": "NUCC taxonomy code"
          },
          "classification": { "type": "string" },
          "specialization": { "type": "string" },
          "primary": { "type": "boolean" }
        }
      },
      "minItems": 1,
      "maxItems": 15
    },
    "practice_location": {
      "type": "object",
      "properties": {
        "address_1": { "type": "string" },
        "address_2": { "type": "string" },
        "city": { "type": "string" },
        "state": { 
          "type": "string",
          "pattern": "^[A-Z]{2}$"
        },
        "zip": { 
          "type": "string",
          "pattern": "^[0-9]{5}(-[0-9]{4})?$"
        },
        "county_fips": {
          "type": "string",
          "pattern": "^[0-9]{5}$"
        },
        "phone": { "type": "string" },
        "fax": { "type": "string" }
      },
      "required": ["city", "state", "zip"]
    },
    "mailing_location": {
      "type": "object",
      "description": "Same structure as practice_location"
    },
    "gender": {
      "type": "string",
      "enum": ["M", "F", "U"]
    },
    "enumeration_date": {
      "type": "string",
      "format": "date",
      "description": "Date NPI was assigned"
    },
    "last_update_date": {
      "type": "string",
      "format": "date"
    },
    "deactivation_date": {
      "type": "string",
      "format": "date"
    },
    "reactivation_date": {
      "type": "string",
      "format": "date"
    },
    "sole_proprietor": {
      "type": "string",
      "enum": ["Y", "N", "X"]
    }
  }
}
```

## Example

### Individual Provider (Physician)

```json
{
  "npi": "1234567893",
  "entity_type": "individual",
  "name": {
    "last": "Johnson",
    "first": "Sarah",
    "middle": "Elizabeth",
    "credential": "MD, FACC"
  },
  "taxonomy": [
    {
      "code": "207RC0000X",
      "classification": "Internal Medicine",
      "specialization": "Cardiovascular Disease",
      "primary": true
    }
  ],
  "practice_location": {
    "address_1": "123 Medical Center Drive",
    "address_2": "Suite 400",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "county_fips": "48201",
    "phone": "713-555-0100"
  },
  "gender": "F",
  "enumeration_date": "2015-03-15",
  "last_update_date": "2024-11-01"
}
```

### Organization Provider (Group Practice)

```json
{
  "npi": "1987654321",
  "entity_type": "organization",
  "organization_name": "Houston Cardiology Associates, PLLC",
  "taxonomy": [
    {
      "code": "207RC0000X",
      "classification": "Internal Medicine",
      "specialization": "Cardiovascular Disease",
      "primary": true
    },
    {
      "code": "207RI0011X",
      "classification": "Internal Medicine",
      "specialization": "Interventional Cardiology",
      "primary": false
    }
  ],
  "practice_location": {
    "address_1": "456 Heart Center Blvd",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "county_fips": "48201",
    "phone": "713-555-0200"
  },
  "enumeration_date": "2010-06-20",
  "last_update_date": "2024-10-15"
}
```

## NPI Validation

NPIs use the Luhn algorithm for checksum validation:

```python
def validate_npi(npi: str) -> bool:
    """Validate NPI using Luhn algorithm."""
    if not npi.isdigit() or len(npi) != 10:
        return False
    
    # Add prefix "80840" for healthcare prefix
    prefixed = "80840" + npi[:-1]
    
    # Luhn algorithm
    total = 0
    for i, digit in enumerate(reversed(prefixed)):
        d = int(digit)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    
    check_digit = (10 - (total % 10)) % 10
    return check_digit == int(npi[-1])
```

## Taxonomy Codes

Common taxonomy codes for reference:

| Code | Classification | Specialization |
|------|---------------|----------------|
| 207Q00000X | Family Medicine | General |
| 207R00000X | Internal Medicine | General |
| 207RC0000X | Internal Medicine | Cardiovascular Disease |
| 207RG0100X | Internal Medicine | Gastroenterology |
| 207RN0300X | Internal Medicine | Nephrology |
| 207RP1001X | Internal Medicine | Pulmonary Disease |
| 208D00000X | General Practice | - |
| 363L00000X | Nurse Practitioner | General |
| 363LA2100X | Nurse Practitioner | Acute Care |

## Database Mapping

Maps to `network.providers` table:

| Model Field | Database Column |
|-------------|-----------------|
| npi | npi |
| entity_type | entity_type_code (1/2) |
| name.last | last_name |
| name.first | first_name |
| name.credential | credential |
| taxonomy[0].code | taxonomy_1 |
| practice_location.state | practice_state |
| practice_location.city | practice_city |
| practice_location.zip | practice_zip |
| practice_location.county_fips | county_fips |

## Cross-Product Usage

### PatientSim
- Attending provider for encounters
- Ordering provider for labs/imaging
- Referring provider for referrals

### MemberSim
- Billing provider on claims
- Rendering provider on claims
- Network status determination

### TrialSim
- Principal investigator
- Site staff credentials
- Protocol compliance verification

## Related Models

- [Facility Model](facility-model.md) - Healthcare facilities
- [Network Model](network-model.md) - Network configurations
- [PopulationSim Population Profile](../populationsim-models/population-profile.md) - Population demographics
