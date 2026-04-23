# Pharmacy Canonical Model

The canonical data model for pharmacies in NetworkSim.

## Overview

A Pharmacy represents a licensed dispensing location identified by an NCPDP Provider ID. Pharmacies include retail, specialty, mail-order, and hospital pharmacies.

## Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Pharmacy",
  "type": "object",
  "required": ["ncpdp_id", "name", "type", "location"],
  "properties": {
    "ncpdp_id": {
      "type": "string",
      "pattern": "^[0-9]{7}$",
      "description": "NCPDP Provider ID"
    },
    "npi": {
      "type": "string",
      "pattern": "^[0-9]{10}$"
    },
    "dea": {
      "type": "string",
      "pattern": "^[A-Z]{2}[0-9]{7}$",
      "description": "DEA registration number"
    },
    "name": {
      "type": "string"
    },
    "doing_business_as": {
      "type": "string"
    },
    "type": {
      "type": "string",
      "enum": [
        "retail_chain",
        "retail_independent",
        "mail_order",
        "specialty",
        "hospital",
        "clinic",
        "long_term_care",
        "compounding"
      ]
    },
    "chain_code": {
      "type": "string",
      "description": "Parent company code (e.g., CVS, WAG)"
    },
    "location": {
      "type": "object",
      "properties": {
        "address_1": { "type": "string" },
        "address_2": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" },
        "zip": { "type": "string" },
        "county_fips": { "type": "string" },
        "phone": { "type": "string" },
        "fax": { "type": "string" }
      }
    },
    "hours": {
      "type": "object",
      "properties": {
        "open_24_hours": { "type": "boolean" },
        "weekday_open": { "type": "string" },
        "weekday_close": { "type": "string" },
        "weekend_open": { "type": "string" },
        "weekend_close": { "type": "string" }
      }
    },
    "services": {
      "type": "object",
      "properties": {
        "immunizations": { "type": "boolean" },
        "mtm": { "type": "boolean", "description": "Medication Therapy Management" },
        "compounding": { "type": "boolean" },
        "dme": { "type": "boolean", "description": "Durable Medical Equipment" },
        "delivery": { "type": "boolean" },
        "drive_thru": { "type": "boolean" }
      }
    },
    "specialty_accreditation": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["URAC", "ACHC", "Joint Commission"]
      }
    },
    "limited_distribution": {
      "type": "boolean",
      "description": "Authorized for limited distribution drugs"
    }
  }
}
```

## Example

### Retail Chain Pharmacy

```json
{
  "ncpdp_id": "3456789",
  "npi": "1234567890",
  "dea": "FC1234567",
  "name": "CVS Pharmacy #1234",
  "doing_business_as": "CVS Pharmacy",
  "type": "retail_chain",
  "chain_code": "CVS",
  "location": {
    "address_1": "1234 Main Street",
    "city": "Houston",
    "state": "TX",
    "zip": "77002",
    "county_fips": "48201",
    "phone": "713-555-0100",
    "fax": "713-555-0101"
  },
  "hours": {
    "open_24_hours": false,
    "weekday_open": "08:00",
    "weekday_close": "22:00",
    "weekend_open": "09:00",
    "weekend_close": "21:00"
  },
  "services": {
    "immunizations": true,
    "mtm": true,
    "compounding": false,
    "dme": true,
    "delivery": true,
    "drive_thru": true
  }
}
```

### Specialty Pharmacy

```json
{
  "ncpdp_id": "9876543",
  "npi": "1987654321",
  "name": "Optum Specialty Pharmacy",
  "type": "specialty",
  "location": {
    "address_1": "4500 East Cotton Center Blvd",
    "city": "Phoenix",
    "state": "AZ",
    "zip": "85040"
  },
  "services": {
    "delivery": true,
    "mtm": true
  },
  "specialty_accreditation": ["URAC", "ACHC"],
  "limited_distribution": true
}
```

## Chain Codes

| Code | Chain Name |
|------|------------|
| CVS | CVS Health |
| WAG | Walgreens |
| RAD | Rite Aid |
| WMT | Walmart |
| TGT | Target |
| KRO | Kroger |
| PBX | Publix |

## Cross-Product Usage

### RxMemberSim
- Dispensing pharmacy on claims
- Network status (retail/specialty/mail)
- Days supply rules by pharmacy type

### MemberSim
- Pharmacy benefit carve-out claims
- Accumulator updates

## Related Models

- [Provider Model](provider-model.md) - Pharmacist providers
- [Network Model](network-model.md) - PBM network participation
