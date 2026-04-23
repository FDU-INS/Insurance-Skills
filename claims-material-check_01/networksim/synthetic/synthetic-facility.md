---
name: synthetic-facility
description: |
  Generate realistic synthetic healthcare facility entities including hospitals,
  ambulatory surgery centers, skilled nursing facilities, clinics, and other
  care settings. Includes CCN, bed counts, services, and accreditation.
  
  Trigger phrases: "generate facility", "create hospital", "synthetic CCN",
  "generate clinic", "create ASC", "ambulatory surgery center", "SNF",
  "skilled nursing facility", "urgent care", "dialysis center", "facility for"
version: "1.0"
category: synthetic
related_skills:
  - network-types
  - synthetic-provider
  - network-adequacy
  - provider-for-encounter
cross_product:
  - patientsim: Facility for inpatient admissions, ED visits, procedures
  - membersim: Facility claims (837I), place of service
  - trialsim: Trial sites with facility characteristics
---

# Synthetic Facility Generation

## Overview

Generate realistic synthetic healthcare facility entities for use across the HealthSim ecosystem. Facilities are identified by CCN (CMS Certification Number) for Medicare-certified facilities, or by NPI for all provider organizations.

This skill generates the **canonical facility entity** that can be:
- Used directly as JSON
- Transformed to FHIR Location/Organization
- Flattened to CMS POS-style CSV
- Integrated into other HealthSim products

---

## Trigger Phrases

Use this skill when you see:
- "Generate a hospital"
- "Create a facility in Chicago"
- "Generate an ASC for orthopedic procedures"
- "Create a skilled nursing facility"
- "Generate a dialysis center"
- "Create an urgent care clinic"
- "Generate a facility for this admission"

---

## Facility Types

### Acute Care Hospitals

| Type | CCN Pattern | Description |
|------|-------------|-------------|
| Short-term Acute | XX-0001-0879 | General medical/surgical hospitals |
| Critical Access | XX-1300-1399 | Rural hospitals ≤25 beds, 96-hr stay limit |
| Long-term Acute | XX-2000-2299 | Average LOS >25 days |
| Psychiatric | XX-4000-4499 | Inpatient mental health |
| Rehabilitation | XX-3025-3099 | Inpatient rehab facilities |
| Children's | XX-3300-3399 | Pediatric specialty hospitals |

### Post-Acute Care

| Type | CCN Pattern | Description |
|------|-------------|-------------|
| Skilled Nursing | XX-5000-6499 | Post-acute and long-term nursing care |
| Home Health | XX-7000-7999 | Home-based skilled services |
| Hospice | XX-1500-1799 | End-of-life care |
| Inpatient Rehab | XX-3025-3099 | Intensive rehabilitation |

### Outpatient Facilities

| Type | CCN Pattern | Description |
|------|-------------|-------------|
| ASC | XX-AS0001-9999 | Ambulatory Surgery Centers |
| ESRD | XX-2300-2499 | Dialysis facilities |
| CORF | XX-8000-8499 | Comprehensive Outpatient Rehab |
| RHC | XX-A0001-9999 | Rural Health Clinics |
| FQHC | XX-A0001-9999 | Federally Qualified Health Centers |

### Other Settings

| Type | Place of Service | Description |
|------|------------------|-------------|
| Urgent Care | 20 | Walk-in immediate care |
| Physician Office | 11 | Outpatient practice location |
| Telehealth | 02 | Virtual care delivery |
| Mobile Unit | 15 | Mobile diagnostic/treatment |

---

## Generation Parameters

### Required Context

| Parameter | Description | Default |
|-----------|-------------|---------|
| **facility_type** | Type of facility | Short-term Acute |
| **location** | City, state, or county | Random US location |

### Optional Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **bed_count** | Number of beds (hospitals) | Based on type/area |
| **services** | Array of service lines | Based on type |
| **ownership** | Government, Non-profit, For-profit | Weighted random |
| **teaching_status** | Teaching, Non-teaching | Based on size/location |
| **trauma_level** | I, II, III, IV, V, None | Based on size/location |
| **accreditation** | Joint Commission, DNV, etc. | Joint Commission (70%) |
| **system_affiliation** | Health system membership | 60% affiliated |

---

## Canonical Schema

### Hospital Facility

```json
{
  "ccn": "string (6 char, XX-NNNN pattern)",
  "npi": "string (10 digits, Luhn-valid)",
  "facility_type": "string",
  "facility_subtype": "string",
  "name": "string",
  "doing_business_as": "string (optional)",
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
    "emergency_phone": "string (optional)",
    "fax": "string (optional)",
    "website": "string (optional)"
  },
  "characteristics": {
    "ownership_type": "Government | Non-profit | For-profit",
    "ownership_subtype": "string (e.g., Church-operated, Investor-owned)",
    "bed_count": {
      "total": "integer",
      "staffed": "integer",
      "icu": "integer",
      "psychiatric": "integer",
      "rehabilitation": "integer"
    },
    "teaching_status": "Major Teaching | Minor Teaching | Non-teaching",
    "medical_school_affiliation": "string (optional)",
    "trauma_designation": {
      "level": "I | II | III | IV | V | None",
      "pediatric_level": "I | II | None",
      "burn_center": "boolean"
    },
    "urban_rural": "Urban | Suburban | Rural",
    "critical_access": "boolean"
  },
  "services": [
    {
      "service_line": "string",
      "service_code": "string",
      "beds_allocated": "integer (optional)",
      "annual_volume": "integer (optional)"
    }
  ],
  "certifications": {
    "medicare_certified": "boolean",
    "medicaid_certified": "boolean",
    "accreditation": {
      "body": "Joint Commission | DNV GL | HFAP | CIHQ | State Only",
      "status": "Accredited | Provisional | None",
      "effective_date": "YYYY-MM-DD",
      "expiration_date": "YYYY-MM-DD"
    },
    "specialty_certifications": [
      {
        "type": "string",
        "certifying_body": "string",
        "status": "string"
      }
    ]
  },
  "system_affiliation": {
    "health_system": "string",
    "system_id": "string",
    "parent_organization": "string (optional)"
  },
  "quality_ratings": {
    "cms_star_rating": "integer (1-5)",
    "hcahps_summary": "integer (percentile)",
    "leapfrog_grade": "A | B | C | D | F"
  },
  "fiscal_year_end": "MM-DD",
  "initial_certification_date": "YYYY-MM-DD",
  "last_survey_date": "YYYY-MM-DD"
}
```

### Ambulatory Surgery Center

```json
{
  "ccn": "string (format: XX-ASNNNN)",
  "npi": "string (10 digits)",
  "facility_type": "Ambulatory Surgery Center",
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
    "fax": "string"
  },
  "characteristics": {
    "ownership_type": "string",
    "operating_rooms": "integer",
    "procedure_rooms": "integer",
    "recovery_bays": "integer"
  },
  "specialty_focus": ["string"],
  "surgical_specialties": [
    {
      "specialty": "string",
      "procedure_types": ["string"],
      "annual_volume": "integer"
    }
  ],
  "certifications": {
    "medicare_certified": "boolean",
    "accreditation": {
      "body": "AAAHC | Joint Commission | AAAASF",
      "status": "string",
      "effective_date": "YYYY-MM-DD"
    }
  },
  "hospital_affiliation": {
    "name": "string (optional)",
    "ccn": "string (optional)",
    "transfer_agreement": "boolean"
  }
}
```

### Skilled Nursing Facility

```json
{
  "ccn": "string (format: XX-5NNN)",
  "npi": "string (10 digits)",
  "facility_type": "Skilled Nursing Facility",
  "name": "string",
  "address": {
    "street_address": "string",
    "city": "string",
    "state": "string",
    "zip": "string",
    "county_fips": "string"
  },
  "characteristics": {
    "ownership_type": "string",
    "bed_count": {
      "total": "integer",
      "medicare_certified": "integer",
      "medicaid_certified": "integer"
    },
    "occupancy_rate": "number (0-1)",
    "in_hospital": "boolean",
    "continuing_care_community": "boolean"
  },
  "services": {
    "skilled_nursing": "boolean",
    "rehabilitation": "boolean",
    "memory_care": "boolean",
    "ventilator_care": "boolean",
    "dialysis": "boolean"
  },
  "staffing": {
    "rn_hours_per_resident_day": "number",
    "total_nurse_hours_per_resident_day": "number",
    "physical_therapy_available": "boolean",
    "occupational_therapy_available": "boolean"
  },
  "quality_ratings": {
    "cms_overall_rating": "integer (1-5)",
    "health_inspection_rating": "integer (1-5)",
    "staffing_rating": "integer (1-5)",
    "quality_measure_rating": "integer (1-5)"
  },
  "recent_surveys": {
    "last_standard_survey": "YYYY-MM-DD",
    "deficiencies_count": "integer",
    "immediate_jeopardy": "boolean"
  }
}
```

---

## CCN Generation Rules

### Format

CCN (CMS Certification Number) format varies by facility type:

| Facility Type | Format | Example |
|---------------|--------|---------|
| Short-term Hospital | SS-0NNN | 45-0358 |
| Critical Access | SS-13NN | 45-1301 |
| Psychiatric | SS-40NN | 45-4001 |
| SNF | SS-5NNN | 45-5001 |
| Home Health | SS-7NNN | 45-7001 |
| ASC | SS-ASNNNN | 45-AS0001 |
| ESRD | SS-23NN | 45-2301 |

Where SS = state code (01-56, including territories)

### State Codes

| Code | State | Code | State |
|------|-------|------|-------|
| 01 | Alabama | 27 | Minnesota |
| 02 | Alaska | 28 | Mississippi |
| 03 | Arizona | 29 | Missouri |
| 04 | Arkansas | 30 | Montana |
| 05 | California | 31 | Nebraska |
| 06 | Colorado | 32 | Nevada |
| 07 | Connecticut | 33 | New Hampshire |
| 08 | Delaware | 34 | New Jersey |
| 09 | DC | 35 | New Mexico |
| 10 | Florida | 36 | New York |
| 11 | Georgia | 37 | North Carolina |
| 12 | Hawaii | 38 | North Dakota |
| 13 | Idaho | 39 | Ohio |
| 14 | Illinois | 40 | Oklahoma |
| 15 | Indiana | 41 | Oregon |
| 16 | Iowa | 42 | Pennsylvania |
| 17 | Kansas | 43 | Puerto Rico |
| 18 | Kentucky | 44 | Rhode Island |
| 19 | Louisiana | 45 | South Carolina |
| 20 | Maine | 46 | South Dakota |
| 21 | Maryland | 47 | Tennessee |
| 22 | Massachusetts | 48 | Texas |
| 23 | Michigan | 49 | Utah |
| 24 | Michigan | 50 | Vermont |
| 25 | Minnesota | 51 | Virginia |
| 26 | Mississippi | 52 | Virgin Islands |

---

## Examples

### Example 1: Urban Teaching Hospital

**Prompt**: "Generate a large teaching hospital in Philadelphia"

**Response**:

```json
{
  "ccn": "390111",
  "npi": "1234567890",
  "facility_type": "Short-term Acute Care Hospital",
  "facility_subtype": "General Medical and Surgical",
  "name": "Philadelphia University Hospital",
  "doing_business_as": "Penn University Hospital",
  "address": {
    "street_address": "3400 Spruce Street",
    "city": "Philadelphia",
    "state": "PA",
    "zip": "19104",
    "county": "Philadelphia",
    "county_fips": "42101",
    "latitude": 39.9496,
    "longitude": -75.1932
  },
  "contact": {
    "main_phone": "2156628000",
    "emergency_phone": "2156628911",
    "website": "https://www.pennmedicine.org"
  },
  "characteristics": {
    "ownership_type": "Non-profit",
    "ownership_subtype": "Private Non-profit",
    "bed_count": {
      "total": 789,
      "staffed": 725,
      "icu": 120,
      "psychiatric": 45,
      "rehabilitation": 30
    },
    "teaching_status": "Major Teaching",
    "medical_school_affiliation": "University of Pennsylvania Perelman School of Medicine",
    "trauma_designation": {
      "level": "I",
      "pediatric_level": "I",
      "burn_center": true
    },
    "urban_rural": "Urban",
    "critical_access": false
  },
  "services": [
    {"service_line": "Cardiac Surgery", "service_code": "CARD", "beds_allocated": 48, "annual_volume": 1250},
    {"service_line": "Neurosurgery", "service_code": "NEUR", "beds_allocated": 36, "annual_volume": 890},
    {"service_line": "Transplant", "service_code": "TRNS", "beds_allocated": 24, "annual_volume": 450},
    {"service_line": "Oncology", "service_code": "ONCO", "beds_allocated": 60, "annual_volume": 2100},
    {"service_line": "Emergency", "service_code": "EMER", "annual_volume": 95000},
    {"service_line": "Labor & Delivery", "service_code": "LDEL", "beds_allocated": 30, "annual_volume": 4200}
  ],
  "certifications": {
    "medicare_certified": true,
    "medicaid_certified": true,
    "accreditation": {
      "body": "Joint Commission",
      "status": "Accredited",
      "effective_date": "2022-03-15",
      "expiration_date": "2025-03-14"
    },
    "specialty_certifications": [
      {"type": "Comprehensive Stroke Center", "certifying_body": "Joint Commission", "status": "Certified"},
      {"type": "Magnet Recognition", "certifying_body": "ANCC", "status": "Designated"},
      {"type": "NCI Comprehensive Cancer Center", "certifying_body": "NCI", "status": "Designated"}
    ]
  },
  "system_affiliation": {
    "health_system": "Penn Medicine",
    "system_id": "PENN",
    "parent_organization": "University of Pennsylvania Health System"
  },
  "quality_ratings": {
    "cms_star_rating": 4,
    "hcahps_summary": 78,
    "leapfrog_grade": "A"
  },
  "fiscal_year_end": "06-30",
  "initial_certification_date": "1966-07-01",
  "last_survey_date": "2024-02-15"
}
```

---

### Example 2: Critical Access Hospital

**Prompt**: "Generate a critical access hospital in rural Montana"

**Response**:

```json
{
  "ccn": "271301",
  "npi": "1456789012",
  "facility_type": "Critical Access Hospital",
  "facility_subtype": "CAH - Rural Emergency Hospital",
  "name": "Big Sky Medical Center",
  "address": {
    "street_address": "100 Hospital Drive",
    "city": "Choteau",
    "state": "MT",
    "zip": "59422",
    "county": "Teton",
    "county_fips": "30099",
    "latitude": 47.8128,
    "longitude": -112.1852
  },
  "contact": {
    "main_phone": "4064662100",
    "emergency_phone": "4064662911"
  },
  "characteristics": {
    "ownership_type": "Government",
    "ownership_subtype": "County",
    "bed_count": {
      "total": 25,
      "staffed": 18,
      "icu": 2,
      "psychiatric": 0,
      "rehabilitation": 0
    },
    "teaching_status": "Non-teaching",
    "trauma_designation": {
      "level": "IV",
      "pediatric_level": "None",
      "burn_center": false
    },
    "urban_rural": "Rural",
    "critical_access": true
  },
  "services": [
    {"service_line": "Emergency", "service_code": "EMER", "annual_volume": 3500},
    {"service_line": "General Surgery", "service_code": "SURG", "annual_volume": 180},
    {"service_line": "Obstetrics", "service_code": "OBST", "annual_volume": 85},
    {"service_line": "Swing Beds", "service_code": "SWNG", "beds_allocated": 6}
  ],
  "certifications": {
    "medicare_certified": true,
    "medicaid_certified": true,
    "accreditation": {
      "body": "State Only",
      "status": "Licensed",
      "effective_date": "2023-01-01",
      "expiration_date": "2025-12-31"
    }
  },
  "system_affiliation": {
    "health_system": "Benefis Health System",
    "system_id": "BENE",
    "parent_organization": "Benefis Health System"
  },
  "quality_ratings": {
    "cms_star_rating": 3
  },
  "fiscal_year_end": "12-31",
  "initial_certification_date": "1999-01-15",
  "last_survey_date": "2023-09-20"
}
```

---

### Example 3: Ambulatory Surgery Center

**Prompt**: "Generate an orthopedic ambulatory surgery center in Denver"

**Response**:

```json
{
  "ccn": "06AS0234",
  "npi": "1678901234",
  "facility_type": "Ambulatory Surgery Center",
  "name": "Rocky Mountain Orthopedic Surgery Center",
  "address": {
    "street_address": "1601 East 19th Avenue",
    "street_address_2": "Suite 400",
    "city": "Denver",
    "state": "CO",
    "zip": "80218",
    "county": "Denver",
    "county_fips": "08031",
    "latitude": 39.7456,
    "longitude": -104.9697
  },
  "contact": {
    "main_phone": "3038391000",
    "fax": "3038391001"
  },
  "characteristics": {
    "ownership_type": "For-profit",
    "ownership_subtype": "Physician-owned",
    "operating_rooms": 4,
    "procedure_rooms": 2,
    "recovery_bays": 12
  },
  "specialty_focus": ["Orthopedics", "Sports Medicine", "Spine"],
  "surgical_specialties": [
    {
      "specialty": "Orthopedic Surgery",
      "procedure_types": ["Arthroscopy", "Joint Replacement", "Fracture Repair", "Rotator Cuff"],
      "annual_volume": 2400
    },
    {
      "specialty": "Spine Surgery",
      "procedure_types": ["Discectomy", "Laminectomy", "Fusion"],
      "annual_volume": 600
    },
    {
      "specialty": "Pain Management",
      "procedure_types": ["Epidural", "Nerve Block", "Spinal Cord Stimulator"],
      "annual_volume": 1800
    }
  ],
  "certifications": {
    "medicare_certified": true,
    "accreditation": {
      "body": "AAAHC",
      "status": "Accredited",
      "effective_date": "2023-06-01"
    }
  },
  "hospital_affiliation": {
    "name": "Swedish Medical Center",
    "ccn": "060032",
    "transfer_agreement": true
  }
}
```

---

### Example 4: Skilled Nursing Facility

**Prompt**: "Generate a skilled nursing facility near Baltimore"

**Response**:

```json
{
  "ccn": "215234",
  "npi": "1890123456",
  "facility_type": "Skilled Nursing Facility",
  "name": "Chesapeake Bay Nursing and Rehabilitation Center",
  "address": {
    "street_address": "4800 York Road",
    "city": "Towson",
    "state": "MD",
    "zip": "21204",
    "county": "Baltimore",
    "county_fips": "24005",
    "latitude": 39.3947,
    "longitude": -76.6019
  },
  "contact": {
    "main_phone": "4103391000",
    "fax": "4103391001"
  },
  "characteristics": {
    "ownership_type": "For-profit",
    "ownership_subtype": "Chain-affiliated",
    "bed_count": {
      "total": 150,
      "medicare_certified": 120,
      "medicaid_certified": 150
    },
    "occupancy_rate": 0.87,
    "in_hospital": false,
    "continuing_care_community": false
  },
  "services": {
    "skilled_nursing": true,
    "rehabilitation": true,
    "memory_care": true,
    "ventilator_care": false,
    "dialysis": false
  },
  "staffing": {
    "rn_hours_per_resident_day": 0.75,
    "total_nurse_hours_per_resident_day": 3.8,
    "physical_therapy_available": true,
    "occupational_therapy_available": true
  },
  "quality_ratings": {
    "cms_overall_rating": 4,
    "health_inspection_rating": 3,
    "staffing_rating": 4,
    "quality_measure_rating": 5
  },
  "recent_surveys": {
    "last_standard_survey": "2024-01-15",
    "deficiencies_count": 4,
    "immediate_jeopardy": false
  },
  "chain_affiliation": {
    "chain_name": "Sunrise Senior Living",
    "chain_id": "SNRS"
  }
}
```

---

## Cross-Product Integration

### PatientSim Integration

Generate facilities for clinical encounters:

```
PatientSim Encounter → NetworkSim → Facility Entity

Context needed:
- Encounter type (inpatient, outpatient, ED, observation)
- Service required (cardiac surgery, orthopedics, etc.)
- Patient location (for geographic matching)
- Acuity level (trauma center needed?)
```

### MemberSim Integration

Generate facilities for institutional claims:

```
MemberSim 837I Claim → NetworkSim → Facility

Context needed:
- Claim type (inpatient, outpatient, SNF)
- DRG or revenue codes
- Network status requirement
- Place of service code
```

### TrialSim Integration

Generate trial site facilities:

```
TrialSim Protocol → NetworkSim → Site Facility

Context needed:
- Therapeutic area (oncology → NCI-designated?)
- Phase (Phase 1 → academic medical center?)
- Required capabilities (IRB, pharmacy, lab)
- Geographic requirements
```

---

## Validation Rules

### CCN Validation

| Rule | Validation |
|------|------------|
| Format | 6 characters for hospitals, varies by type |
| State Code | Must be valid CMS state code (01-56) |
| Type Range | Must match facility type pattern |

### Bed Count Validation

| Rule | Validation |
|------|------------|
| Total | > 0 for inpatient facilities |
| Staffed | ≤ Total |
| ICU | ≤ Total, typically 10-15% for large hospitals |
| CAH Limit | ≤ 25 for Critical Access Hospitals |

### Geographic Validation

| Rule | Validation |
|------|------------|
| County FIPS | Valid 5-digit FIPS code |
| State Match | Address state must match CCN state code |
| Urban/Rural | Must match county characteristics |

### Business Rules

| Rule | Description |
|------|-------------|
| CAH Location | Critical Access must be rural (>35 miles from other hospital) |
| Teaching Status | Major teaching requires medical school affiliation |
| Trauma Level | Level I requires teaching status and research |
| NPI Required | All facilities need NPI for claims |

---

## Related Skills

- [Network Adequacy](../reference/network-adequacy.md) - Access standards for facilities
- [Synthetic Provider](synthetic-provider.md) - Generate affiliated providers
- [Provider for Encounter](../integration/provider-for-encounter.md) - PatientSim integration
- [Network for Member](../integration/network-for-member.md) - MemberSim network context

---

*Synthetic Facility is a generation skill in the NetworkSim product.*
