# Facility Canonical Model

The canonical data model for healthcare facilities in NetworkSim.

## Overview

A Facility represents a healthcare institution (hospital, clinic, nursing home, etc.) registered with CMS and identified by a CCN (CMS Certification Number). Facilities may also have NPIs for billing purposes.

## Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Facility",
  "type": "object",
  "required": ["ccn", "name", "type", "location"],
  "properties": {
    "ccn": {
      "type": "string",
      "pattern": "^[0-9A-Z]{6}$",
      "description": "CMS Certification Number"
    },
    "npi": {
      "type": "string",
      "pattern": "^[0-9]{10}$",
      "description": "Optional organizational NPI"
    },
    "name": {
      "type": "string",
      "description": "Facility legal name"
    },
    "doing_business_as": {
      "type": "string",
      "description": "Trade name if different"
    },
    "type": {
      "type": "string",
      "enum": [
        "short_term_acute",
        "long_term_acute",
        "critical_access",
        "psychiatric",
        "rehabilitation",
        "childrens",
        "skilled_nursing",
        "home_health",
        "hospice",
        "ambulatory_surgery",
        "dialysis",
        "rural_health_clinic",
        "federally_qualified_health_center"
      ]
    },
    "location": {
      "type": "object",
      "properties": {
        "address_1": { "type": "string" },
        "address_2": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string", "pattern": "^[A-Z]{2}$" },
        "zip": { "type": "string" },
        "county_fips": { "type": "string", "pattern": "^[0-9]{5}$" },
        "phone": { "type": "string" },
        "latitude": { "type": "number" },
        "longitude": { "type": "number" }
      },
      "required": ["city", "state", "zip"]
    },
    "beds": {
      "type": "object",
      "properties": {
        "total": { "type": "integer" },
        "icu": { "type": "integer" },
        "psychiatric": { "type": "integer" },
        "rehabilitation": { "type": "integer" }
      }
    },
    "services": {
      "type": "object",
      "properties": {
        "emergency": { "type": "boolean" },
        "trauma_level": { 
          "type": "string",
          "enum": ["Level I", "Level II", "Level III", "Level IV", "None"]
        },
        "cardiac_surgery": { "type": "boolean" },
        "cardiac_cath": { "type": "boolean" },
        "nicu": { "type": "boolean" },
        "burn_unit": { "type": "boolean" }
      }
    },
    "ownership": {
      "type": "string",
      "enum": [
        "government_federal",
        "government_state",
        "government_local",
        "nonprofit_church",
        "nonprofit_other",
        "for_profit_individual",
        "for_profit_partnership",
        "for_profit_corporation"
      ]
    },
    "quality": {
      "type": "object",
      "properties": {
        "overall_rating": { 
          "type": "integer",
          "minimum": 1,
          "maximum": 5
        },
        "mortality_rating": { "type": "string" },
        "safety_rating": { "type": "string" },
        "readmission_rating": { "type": "string" },
        "patient_experience_rating": { "type": "string" }
      }
    },
    "certification_date": {
      "type": "string",
      "format": "date"
    },
    "accreditation": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["Joint Commission", "DNV", "CIHQ", "HFAP"]
      }
    }
  }
}
```

## Example

### Acute Care Hospital

```json
{
  "ccn": "450358",
  "npi": "1234567890",
  "name": "Memorial Hermann - Texas Medical Center",
  "type": "short_term_acute",
  "location": {
    "address_1": "6411 Fannin St",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "county_fips": "48201",
    "phone": "713-704-4000",
    "latitude": 29.7101,
    "longitude": -95.3969
  },
  "beds": {
    "total": 1073,
    "icu": 234,
    "psychiatric": 0,
    "rehabilitation": 60
  },
  "services": {
    "emergency": true,
    "trauma_level": "Level I",
    "cardiac_surgery": true,
    "cardiac_cath": true,
    "nicu": true,
    "burn_unit": true
  },
  "ownership": "nonprofit_other",
  "quality": {
    "overall_rating": 4,
    "mortality_rating": "Same as National",
    "safety_rating": "Above National",
    "readmission_rating": "Same as National"
  },
  "certification_date": "1965-07-01",
  "accreditation": ["Joint Commission"]
}
```

### Critical Access Hospital

```json
{
  "ccn": "481301",
  "name": "Big Bend Regional Medical Center",
  "type": "critical_access",
  "location": {
    "address_1": "2600 Highway 118 N",
    "city": "Alpine",
    "state": "TX",
    "zip": "79830",
    "county_fips": "48043"
  },
  "beds": {
    "total": 25
  },
  "services": {
    "emergency": true,
    "trauma_level": "Level IV"
  },
  "ownership": "government_local"
}
```

## CCN Format

The CCN encodes facility type and state:

| Position | Meaning |
|----------|---------|
| 1-2 | State code (01-99) |
| 3-4 | Facility type |
| 5-6 | Sequence number |

**Facility Type Codes:**
- 00-08: Short-term acute care
- 13: Critical access hospital
- 20-22: Long-term care
- 40-44: Psychiatric
- 50-59: Skilled nursing

## Database Mapping

Maps to `network.facilities` table:

| Model Field | Database Column |
|-------------|-----------------|
| ccn | ccn |
| name | facility_name |
| type | type |
| location.city | city |
| location.state | state |
| location.zip | zip |
| beds.total | beds |

## Quality Integration

Joins with `network.hospital_quality`:

```sql
SELECT 
    f.facility_name,
    f.city,
    hq.hospital_overall_rating,
    hq.mortality_national_comparison
FROM network.facilities f
JOIN network.hospital_quality hq ON f.ccn = hq.facility_id
WHERE hq.hospital_overall_rating IN ('4', '5');
```

## Cross-Product Usage

### PatientSim
- Admission facility for inpatient encounters
- Emergency department visits
- Ambulatory surgery location

### MemberSim
- Facility billing (837I claims)
- DRG assignment
- Room and board charges

### TrialSim
- Clinical trial site
- Research facility designation
- IRB affiliation

## Related Models

- [Provider Model](provider-model.md) - Affiliated providers
- [Network Model](network-model.md) - Network participation
