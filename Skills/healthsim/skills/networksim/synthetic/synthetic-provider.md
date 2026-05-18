---
name: synthetic-provider
description: |
  Generate realistic synthetic healthcare provider entities with NPI, credentials,
  taxonomy codes, practice locations, and hospital affiliations. Supports individual
  providers (physicians, NPs, PAs) and organizational providers (group practices).
  
  Trigger phrases: "generate provider", "create physician", "synthetic NPI",
  "generate doctor", "create specialist", "provider for", "attending physician",
  "referring provider", "rendering provider", "prescriber"
version: "1.0"
category: synthetic
related_skills:
  - network-types
  - synthetic-facility
  - provider-for-encounter
cross_product:
  - patientsim: Attending, referring, ordering providers for encounters
  - membersim: Rendering, billing providers for claims
  - rxmembersim: Prescribers for prescriptions
  - trialsim: Principal investigators, sub-investigators for trials
---

# Synthetic Provider Generation

## Overview

Generate realistic synthetic healthcare provider entities for use across the HealthSim ecosystem. Providers are identified by NPI (National Provider Identifier) and include physicians, nurse practitioners, physician assistants, and organizational providers.

This skill generates the **canonical provider entity** that can be:
- Used directly as JSON
- Transformed to FHIR Practitioner/PractitionerRole
- Flattened to NPPES-style CSV
- Integrated into other HealthSim products

---

## Trigger Phrases

Use this skill when you see:
- "Generate a provider"
- "Create a cardiologist in Houston"
- "Generate a physician for this encounter"
- "Create an NPI for a specialist"
- "Generate a nurse practitioner"
- "Create a group practice"
- "Generate a prescriber"

---

## Generation Parameters

### Required Context

| Parameter | Description | Default |
|-----------|-------------|---------|
| **specialty** | Medical specialty or taxonomy | General Practice |
| **location** | City, state, or county | Random US location |

### Optional Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **entity_type** | `individual` or `organization` | individual |
| **gender** | M, F, or weighted random | Weighted by specialty |
| **credentials** | MD, DO, NP, PA, etc. | Based on taxonomy |
| **accepting_new_patients** | true/false | true (80%) |
| **languages** | Array of languages | ["English"] |
| **hospital_affiliations** | Generate affiliations | 1-2 for specialists |
| **group_practice** | Include group association | 50% for specialists |

---

## Canonical Schema

### Individual Provider

```json
{
  "npi": "string (10 digits, Luhn-valid)",
  "entity_type": "individual",
  "provider": {
    "last_name": "string",
    "first_name": "string",
    "middle_name": "string (optional)",
    "name_prefix": "string (optional, e.g., Dr.)",
    "name_suffix": "string (optional, e.g., Jr.)",
    "credential": "string (e.g., MD, DO, NP, PA)",
    "gender": "M | F",
    "date_of_birth": "YYYY-MM-DD (optional)"
  },
  "taxonomy": {
    "primary": {
      "code": "string (10 char NUCC code)",
      "classification": "string",
      "specialization": "string (optional)",
      "display_name": "string",
      "is_primary": true
    },
    "secondary": [
      {
        "code": "string",
        "classification": "string",
        "specialization": "string",
        "display_name": "string",
        "is_primary": false
      }
    ]
  },
  "practice_location": {
    "address_line_1": "string",
    "address_line_2": "string (optional)",
    "city": "string",
    "state": "string (2 char)",
    "zip": "string (5 or 9 digits)",
    "county": "string",
    "county_fips": "string (5 digits)",
    "phone": "string (10 digits)",
    "fax": "string (optional)"
  },
  "mailing_address": {
    "address_line_1": "string",
    "city": "string",
    "state": "string",
    "zip": "string"
  },
  "hospital_affiliations": [
    {
      "name": "string",
      "ccn": "string (6 digits)",
      "npi": "string (10 digits)",
      "privileges": ["string"]
    }
  ],
  "group_practice": {
    "name": "string",
    "npi": "string (10 digits)",
    "tax_id": "string (XX-XXXXXXX)"
  },
  "certifications": {
    "board_certified": true,
    "board": "string",
    "initial_certification": "YYYY",
    "recertification_due": "YYYY"
  },
  "licenses": [
    {
      "state": "string (2 char)",
      "number": "string",
      "status": "Active | Inactive",
      "expiration": "YYYY-MM-DD"
    }
  ],
  "education": {
    "medical_school": "string",
    "graduation_year": "YYYY",
    "residency": "string",
    "fellowship": "string (optional)"
  },
  "accepting_new_patients": true,
  "languages": ["string"],
  "enumeration_date": "YYYY-MM-DD",
  "last_update": "YYYY-MM-DD"
}
```

### Organizational Provider

```json
{
  "npi": "string (10 digits, Luhn-valid)",
  "entity_type": "organization",
  "organization": {
    "name": "string",
    "doing_business_as": "string (optional)",
    "organization_type": "string (e.g., Group Practice, Clinic)"
  },
  "taxonomy": {
    "primary": {
      "code": "string",
      "classification": "string",
      "specialization": "string",
      "display_name": "string",
      "is_primary": true
    }
  },
  "practice_location": {
    "address_line_1": "string",
    "city": "string",
    "state": "string",
    "zip": "string",
    "county_fips": "string",
    "phone": "string"
  },
  "authorized_official": {
    "last_name": "string",
    "first_name": "string",
    "title": "string",
    "phone": "string"
  },
  "tax_id": "string (XX-XXXXXXX)",
  "enumeration_date": "YYYY-MM-DD",
  "last_update": "YYYY-MM-DD"
}
```

---

## Common Taxonomy Codes

### Primary Care

| Code | Classification | Specialization | Display |
|------|----------------|----------------|---------|
| 207Q00000X | Family Medicine | - | Family Medicine |
| 207R00000X | Internal Medicine | - | Internal Medicine |
| 208D00000X | General Practice | - | General Practice |
| 363L00000X | Nurse Practitioner | - | Nurse Practitioner |
| 363A00000X | Physician Assistant | - | Physician Assistant |
| 208000000X | Pediatrics | - | Pediatrics |

### Cardiology

| Code | Classification | Specialization | Display |
|------|----------------|----------------|---------|
| 207RC0000X | Internal Medicine | Cardiovascular Disease | Cardiologist |
| 207RI0011X | Internal Medicine | Interventional Cardiology | Interventional Cardiologist |
| 207RC0001X | Internal Medicine | Clinical Cardiac Electrophysiology | Electrophysiologist |
| 207RC0200X | Internal Medicine | Advanced Heart Failure | Heart Failure Specialist |

### Orthopedics

| Code | Classification | Specialization | Display |
|------|----------------|----------------|---------|
| 207X00000X | Orthopaedic Surgery | - | Orthopedic Surgeon |
| 207XS0114X | Orthopaedic Surgery | Sports Medicine | Sports Medicine Orthopedist |
| 207XS0106X | Orthopaedic Surgery | Hand Surgery | Hand Surgeon |
| 207XP3100X | Orthopaedic Surgery | Pediatric Orthopaedics | Pediatric Orthopedist |

### Oncology

| Code | Classification | Specialization | Display |
|------|----------------|----------------|---------|
| 207RH0003X | Internal Medicine | Hematology & Oncology | Medical Oncologist |
| 2086S0102X | Surgery | Surgical Oncology | Surgical Oncologist |
| 2085R0001X | Radiology | Radiation Oncology | Radiation Oncologist |
| 207RG0300X | Internal Medicine | Geriatric Medicine | Geriatric Oncologist |

### Mental Health

| Code | Classification | Specialization | Display |
|------|----------------|----------------|---------|
| 2084P0800X | Psychiatry & Neurology | Psychiatry | Psychiatrist |
| 2084P0804X | Psychiatry & Neurology | Child & Adolescent Psychiatry | Child Psychiatrist |
| 2084P0805X | Psychiatry & Neurology | Addiction Psychiatry | Addiction Psychiatrist |
| 103T00000X | Psychologist | Clinical | Clinical Psychologist |

### Emergency Medicine

| Code | Classification | Specialization | Display |
|------|----------------|----------------|---------|
| 207P00000X | Emergency Medicine | - | Emergency Physician |
| 207PE0004X | Emergency Medicine | Pediatric Emergency Medicine | Pediatric EM Physician |
| 207PT0002X | Emergency Medicine | Medical Toxicology | Toxicologist |

---

## NPI Generation Rules

### Format

- 10 digits
- First digit: 1 or 2 (US providers)
- Must pass Luhn check digit validation

### Luhn Algorithm

```
NPI: 1234567890

1. Double alternating digits from right: 0, 7*2=14, 5, 3*2=6, 1
2. Sum digits: 0+1+4+8+6+5+6+4+3+2 = 39
3. Check: (39 + check_digit) mod 10 = 0
4. Check digit = 1
```

### Generation Pattern

```
Position 1: 1 (individual) or 2 (organization)
Positions 2-9: Random digits
Position 10: Luhn check digit
```

---

## Examples

### Example 1: Basic Provider Generation

**Prompt**: "Generate a cardiologist in Houston"

**Response**:

```json
{
  "npi": "1234567893",
  "entity_type": "individual",
  "provider": {
    "last_name": "Patel",
    "first_name": "Anil",
    "middle_name": "Kumar",
    "credential": "MD, FACC",
    "gender": "M"
  },
  "taxonomy": {
    "primary": {
      "code": "207RC0000X",
      "classification": "Internal Medicine",
      "specialization": "Cardiovascular Disease",
      "display_name": "Cardiologist",
      "is_primary": true
    }
  },
  "practice_location": {
    "address_line_1": "6624 Fannin Street",
    "address_line_2": "Suite 1780",
    "city": "Houston",
    "state": "TX",
    "zip": "77030",
    "county": "Harris",
    "county_fips": "48201",
    "phone": "7135551234",
    "fax": "7135551235"
  },
  "hospital_affiliations": [
    {
      "name": "Houston Methodist Hospital",
      "ccn": "450358",
      "privileges": ["Admitting", "Surgical", "Cath Lab"]
    },
    {
      "name": "Memorial Hermann - Texas Medical Center",
      "ccn": "450068",
      "privileges": ["Admitting", "Consulting"]
    }
  ],
  "certifications": {
    "board_certified": true,
    "board": "American Board of Internal Medicine - Cardiovascular Disease",
    "initial_certification": "2012",
    "recertification_due": "2032"
  },
  "licenses": [
    {
      "state": "TX",
      "number": "M1234567",
      "status": "Active",
      "expiration": "2026-08-31"
    }
  ],
  "accepting_new_patients": true,
  "languages": ["English", "Hindi", "Gujarati"],
  "enumeration_date": "2010-05-15",
  "last_update": "2024-01-15"
}
```

---

### Example 2: Specialist with Fellowship

**Prompt**: "Generate an interventional cardiologist in Boston with full credentials"

**Response**:

```json
{
  "npi": "1456789012",
  "entity_type": "individual",
  "provider": {
    "last_name": "O'Brien",
    "first_name": "Katherine",
    "middle_name": "Marie",
    "credential": "MD, FACC, FSCAI",
    "gender": "F"
  },
  "taxonomy": {
    "primary": {
      "code": "207RI0011X",
      "classification": "Internal Medicine",
      "specialization": "Interventional Cardiology",
      "display_name": "Interventional Cardiologist",
      "is_primary": true
    },
    "secondary": [
      {
        "code": "207RC0000X",
        "classification": "Internal Medicine",
        "specialization": "Cardiovascular Disease",
        "display_name": "Cardiologist",
        "is_primary": false
      }
    ]
  },
  "practice_location": {
    "address_line_1": "55 Fruit Street",
    "address_line_2": "Gray-Bigelow Building, Suite 800",
    "city": "Boston",
    "state": "MA",
    "zip": "02114",
    "county": "Suffolk",
    "county_fips": "25025",
    "phone": "6177261234",
    "fax": "6177261235"
  },
  "hospital_affiliations": [
    {
      "name": "Massachusetts General Hospital",
      "ccn": "220071",
      "privileges": ["Admitting", "Surgical", "Cath Lab", "Structural Heart"]
    },
    {
      "name": "Brigham and Women's Hospital",
      "ccn": "220110",
      "privileges": ["Consulting"]
    }
  ],
  "group_practice": {
    "name": "Massachusetts General Hospital Cardiology Associates",
    "npi": "1987654321",
    "tax_id": "04-1234567"
  },
  "certifications": {
    "board_certified": true,
    "board": "American Board of Internal Medicine - Interventional Cardiology",
    "initial_certification": "2015",
    "recertification_due": "2025"
  },
  "licenses": [
    {
      "state": "MA",
      "number": "256789",
      "status": "Active",
      "expiration": "2025-12-31"
    }
  ],
  "education": {
    "medical_school": "Harvard Medical School",
    "graduation_year": 2006,
    "residency": "Massachusetts General Hospital - Internal Medicine",
    "fellowship": "Brigham and Women's Hospital - Interventional Cardiology"
  },
  "accepting_new_patients": true,
  "languages": ["English", "Spanish"],
  "enumeration_date": "2012-07-01",
  "last_update": "2024-06-15"
}
```

---

### Example 3: Nurse Practitioner in Primary Care

**Prompt**: "Generate a family nurse practitioner in rural Iowa"

**Response**:

```json
{
  "npi": "1678901234",
  "entity_type": "individual",
  "provider": {
    "last_name": "Johnson",
    "first_name": "Emily",
    "credential": "APRN, FNP-BC",
    "gender": "F"
  },
  "taxonomy": {
    "primary": {
      "code": "363LF0000X",
      "classification": "Nurse Practitioner",
      "specialization": "Family",
      "display_name": "Family Nurse Practitioner",
      "is_primary": true
    }
  },
  "practice_location": {
    "address_line_1": "305 Main Street",
    "city": "Decorah",
    "state": "IA",
    "zip": "52101",
    "county": "Winneshiek",
    "county_fips": "19191",
    "phone": "5633821234"
  },
  "hospital_affiliations": [
    {
      "name": "Winneshiek Medical Center",
      "ccn": "161327",
      "privileges": ["Admitting", "Emergency"]
    }
  ],
  "group_practice": {
    "name": "Decorah Family Medicine",
    "npi": "1234509876",
    "tax_id": "42-1234567"
  },
  "certifications": {
    "board_certified": true,
    "board": "American Nurses Credentialing Center - Family NP",
    "initial_certification": "2018",
    "recertification_due": "2028"
  },
  "licenses": [
    {
      "state": "IA",
      "number": "RN123456",
      "status": "Active",
      "expiration": "2025-06-30"
    }
  ],
  "education": {
    "medical_school": "University of Iowa College of Nursing",
    "graduation_year": 2017
  },
  "accepting_new_patients": true,
  "languages": ["English"],
  "enumeration_date": "2018-01-15",
  "last_update": "2024-03-01"
}
```

---

### Example 4: Organizational Provider (Group Practice)

**Prompt**: "Generate a multi-specialty group practice in Phoenix"

**Response**:

```json
{
  "npi": "2345678901",
  "entity_type": "organization",
  "organization": {
    "name": "Arizona Specialty Care Associates, PLLC",
    "doing_business_as": "Arizona Specialty Care",
    "organization_type": "Multi-Specialty Group Practice"
  },
  "taxonomy": {
    "primary": {
      "code": "193200000X",
      "classification": "Multi-Specialty",
      "specialization": "Group Practice",
      "display_name": "Multi-Specialty Group",
      "is_primary": true
    }
  },
  "practice_location": {
    "address_line_1": "2901 North Central Avenue",
    "address_line_2": "Suite 1200",
    "city": "Phoenix",
    "state": "AZ",
    "zip": "85012",
    "county": "Maricopa",
    "county_fips": "04013",
    "phone": "6025551000",
    "fax": "6025551001"
  },
  "authorized_official": {
    "last_name": "Martinez",
    "first_name": "Robert",
    "title": "Chief Executive Officer",
    "phone": "6025551002"
  },
  "tax_id": "86-1234567",
  "enumeration_date": "2005-03-15",
  "last_update": "2024-01-01"
}
```

---

## Cross-Product Integration

### PatientSim Integration

Generate providers for clinical encounters:

```
PatientSim Encounter → NetworkSim → Provider Entity

Context needed:
- Encounter type (inpatient, outpatient, ED)
- Diagnosis category
- Patient location
- Service required (attending, consulting, referring)
```

**Example**:
```
"Generate an attending physician for this heart failure admission in Dallas"

Response includes:
- Cardiologist or hospitalist based on facility type
- Hospital affiliation matching the facility
- Appropriate taxonomy code for the service
```

### MemberSim Integration

Generate providers for claims:

```
MemberSim Claim → NetworkSim → Rendering/Billing Provider

Context needed:
- Claim type (professional, facility)
- Service codes
- Place of service
- Network status requirement
```

### RxMemberSim Integration

Generate prescribers for prescriptions:

```
RxMemberSim Prescription → NetworkSim → Prescriber

Context needed:
- Drug type (controlled, specialty, standard)
- DEA requirement
- Specialty appropriateness
```

### TrialSim Integration

Generate investigators for trials:

```
TrialSim Protocol → NetworkSim → Principal Investigator

Context needed:
- Therapeutic area
- Trial phase
- Site facility
- Required credentials
```

---

## Validation Rules

### NPI Validation

| Rule | Validation |
|------|------------|
| Length | Exactly 10 digits |
| Format | Numeric only |
| Prefix | Must start with 1 (individual) or 2 (organization) |
| Check Digit | Must pass Luhn algorithm |

### Taxonomy Validation

| Rule | Validation |
|------|------------|
| Length | Exactly 10 characters |
| Format | Alphanumeric |
| Lookup | Must be valid NUCC taxonomy code |
| Primary | Exactly one primary taxonomy required |

### Address Validation

| Rule | Validation |
|------|------------|
| State | Valid 2-letter state code |
| ZIP | 5 digits or 9 digits (ZIP+4) |
| County FIPS | 5 digits (2 state + 3 county) |
| Phone | 10 digits |

### Business Rules

| Rule | Description |
|------|-------------|
| Credential Match | Credential must match taxonomy (MD/DO for physician taxonomies) |
| Gender Distribution | Varies by specialty (reflect actual workforce) |
| Age Reasonability | Provider age should be 28-75 typically |
| License State | Must match practice location state |
| Hospital Affiliation | Should be geographically reasonable |

---

## Output Formats

### Canonical JSON (Default)

Full provider entity as shown in examples above.

### FHIR R4 Practitioner

```json
{
  "resourceType": "Practitioner",
  "id": "1234567893",
  "identifier": [
    {
      "system": "http://hl7.org/fhir/sid/us-npi",
      "value": "1234567893"
    }
  ],
  "name": [
    {
      "family": "Patel",
      "given": ["Anil", "Kumar"],
      "suffix": ["MD", "FACC"]
    }
  ],
  "telecom": [
    {
      "system": "phone",
      "value": "7135551234",
      "use": "work"
    }
  ],
  "address": [
    {
      "use": "work",
      "line": ["6624 Fannin Street", "Suite 1780"],
      "city": "Houston",
      "state": "TX",
      "postalCode": "77030"
    }
  ],
  "gender": "male",
  "qualification": [
    {
      "code": {
        "coding": [
          {
            "system": "http://nucc.org/provider-taxonomy",
            "code": "207RC0000X",
            "display": "Cardiovascular Disease"
          }
        ]
      }
    }
  ]
}
```

### NPPES-Style Flat

```csv
NPI,Entity Type,Last Name,First Name,Credential,Taxonomy 1,Taxonomy 1 Primary,Address 1,City,State,ZIP,Phone
1234567893,1,Patel,Anil,MD FACC,207RC0000X,Y,6624 Fannin Street Suite 1780,Houston,TX,77030,7135551234
```

---

## Related Skills

- [Network Types](../reference/network-types.md) - Network context for provider
- [Synthetic Facility](synthetic-facility.md) - Generate affiliated facilities
- [Provider for Encounter](../integration/provider-for-encounter.md) - PatientSim integration
- [Network for Member](../integration/network-for-member.md) - MemberSim network context

---

*Synthetic Provider is a generation skill in the NetworkSim product.*
