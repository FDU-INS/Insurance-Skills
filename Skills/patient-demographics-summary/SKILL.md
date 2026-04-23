---
name: patient-demographics-summary
description: |
  Retrieves and formats a complete patient demographic summary from FHIR Patient, RelatedPerson, and Coverage resources.
  Use when user asks to "pull demographics", "get patient info", "show patient details", "who is this patient",
  "patient summary", "emergency contacts", "insurance info", or needs a quick overview of non-clinical patient data.
  Do NOT use for clinical summaries, lab results, medication lists, or diagnosis reviews.
metadata:
  author: LangCare
  version: 1.0.0
  mcp-server: langcare-mcp-fhir
  category: patient-data
---

# Patient Demographics Summary

## Overview

Pull structured demographic data from FHIR Patient, RelatedPerson, and Coverage resources. Format into a consolidated summary including identifiers, contact information, emergency contacts, insurance, preferred language, communication preferences, and advance directive status. Flag missing critical data elements that may affect care delivery.

## FHIR Resources Used

| Resource | Purpose | Key Fields |
|----------|---------|------------|
| Patient | Core demographics | name, birthDate, gender, address, telecom, communication, identifier, extension |
| RelatedPerson | Emergency contacts, guarantors | name, telecom, relationship, period |
| Coverage | Insurance information | status, type, subscriberId, payor, period, class |

## Instructions

### Step 1: Retrieve Patient Resource

```
Tool: fhir_read
resourceType: "Patient"
id: "[patient-id]"
```

Extract the following fields:
- **Identifiers**: MRN (`identifier` where `type.coding.code` = "MR"), SSN (last 4 only), driver's license
- **Name**: `name` array -- use `name.use` = "official" as primary; note maiden names (`use` = "maiden")
- **Birth Date**: `birthDate` (calculate age)
- **Gender**: `gender` (administrative gender)
- **Race/Ethnicity**: US Core extensions at `extension` where URL = `http://hl7.org/fhir/us/core/StructureDefinition/us-core-race` and `http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity`
- **Address**: `address` array -- identify `use` = "home" vs "work" vs "temp"
- **Telecom**: `telecom` array -- phone (`system` = "phone"), email (`system` = "email"), fax
- **Preferred Language**: `communication` array where `preferred` = true
- **Marital Status**: `maritalStatus`
- **Deceased**: `deceasedBoolean` or `deceasedDateTime`
- **Managing Organization**: `managingOrganization`

### Step 2: Retrieve Emergency Contacts and Related Persons

```
Tool: fhir_search
resourceType: "RelatedPerson"
queryParams: "patient=[patient-id]"
```

For each RelatedPerson:
- Extract name, relationship type (`relationship.coding.code`), phone, email
- Check `period` to confirm the relationship is current (no `end` date or `end` > today)
- Identify relationship roles: emergency contact, next of kin, guarantor, power of attorney

### Step 3: Retrieve Insurance Coverage

```
Tool: fhir_search
resourceType: "Coverage"
queryParams: "patient=[patient-id]&status=active"
```

For each active Coverage:
- Plan name from `class` where `type.coding.code` = "plan"
- Group number from `class` where `type.coding.code` = "group"
- Subscriber ID from `subscriberId`
- Payor organization from `payor` reference
- Coverage period from `period`
- Coverage order (`order` field: 1 = primary, 2 = secondary)

### Step 4: Check for Advance Directives

```
Tool: fhir_search
resourceType: "Consent"
queryParams: "patient=[patient-id]&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes|acd"
```

If no results, also search:
```
Tool: fhir_search
resourceType: "DocumentReference"
queryParams: "patient=[patient-id]&type=http://loinc.org|64298-3"
```

LOINC 64298-3 = Power of attorney / Advance directive

### Step 5: Flag Missing Critical Data

Scan the collected data and flag any of the following as missing:
- No emergency contact (zero RelatedPerson resources or none with emergency contact relationship)
- No active insurance coverage
- No preferred language specified
- No allergy documentation status (check if `AllergyIntolerance` search returns zero results -- this indicates allergies have not been reviewed, not that there are none)
- No advance directive on file
- Missing phone number or email
- Missing address

### Step 6: Format Output

Present the summary in this structure:

```
PATIENT DEMOGRAPHICS
====================
Name: [official name]
MRN: [identifier]
DOB: [birthDate] (Age: [calculated])
Gender: [gender]
Race/Ethnicity: [from extensions]
Preferred Language: [language]
Marital Status: [status]

CONTACT INFORMATION
===================
Home Phone: [telecom]
Mobile Phone: [telecom]
Email: [telecom]
Home Address: [address]

EMERGENCY CONTACTS
==================
1. [name] - [relationship] - [phone]
2. [name] - [relationship] - [phone]

INSURANCE COVERAGE
==================
Primary: [plan name] - ID: [subscriberId] - Group: [group]
Secondary: [plan name] - ID: [subscriberId] - Group: [group]

ADVANCE DIRECTIVES
==================
Status: [On file / Not on file]

MISSING DATA FLAGS
==================
- [list of flagged items]
```

## Examples

### Example 1: Complete Demographics Pull

**User says:** "Pull up demographics for patient 12345"

**Actions:**
1. `fhir_read` Patient/12345 -- returns full Patient resource with name, DOB, address, telecom, US Core race/ethnicity extensions
2. `fhir_search` RelatedPerson?patient=12345 -- returns 2 entries: spouse (emergency contact), adult child (next of kin)
3. `fhir_search` Coverage?patient=12345&status=active -- returns 1 active Coverage: Blue Cross PPO, primary
4. `fhir_search` Consent?patient=12345&category=... -- returns 1 advance directive

**Result:**
```
PATIENT DEMOGRAPHICS
====================
Name: Maria Garcia
MRN: MRN-12345
DOB: 1958-03-15 (Age: 67)
Gender: Female
Race/Ethnicity: Hispanic or Latino / White
Preferred Language: Spanish
Marital Status: Married

CONTACT INFORMATION
===================
Home Phone: (555) 234-5678
Mobile Phone: (555) 876-5432
Email: mgarcia@email.com
Home Address: 456 Oak Ave, Austin, TX 78701

EMERGENCY CONTACTS
==================
1. Roberto Garcia - Spouse - (555) 234-5679
2. Ana Garcia-Lopez - Daughter - (555) 345-6789

INSURANCE COVERAGE
==================
Primary: Blue Cross Blue Shield PPO - ID: BCB998877 - Group: GRP-4421

ADVANCE DIRECTIVES
==================
Status: On file (dated 2022-06-10)

MISSING DATA FLAGS
==================
- No secondary insurance on file
```

### Example 2: Patient With Missing Critical Data

**User says:** "Who is patient abc-789? Get me their info."

**Actions:**
1. `fhir_read` Patient/abc-789 -- returns minimal Patient resource: name and DOB only, no telecom, no extensions
2. `fhir_search` RelatedPerson?patient=abc-789 -- returns 0 entries
3. `fhir_search` Coverage?patient=abc-789&status=active -- returns 0 entries
4. `fhir_search` Consent?patient=abc-789&category=... -- returns 0 entries

**Result:**
```
PATIENT DEMOGRAPHICS
====================
Name: James Wilson
MRN: Not recorded
DOB: 1990-11-22 (Age: 35)
Gender: Male
Race/Ethnicity: Not documented
Preferred Language: Not specified
Marital Status: Unknown

CONTACT INFORMATION
===================
No contact information on file

EMERGENCY CONTACTS
==================
None documented

INSURANCE COVERAGE
==================
No active coverage found

ADVANCE DIRECTIVES
==================
Status: Not on file

MISSING DATA FLAGS [CRITICAL]
==============================
- No phone number or email
- No home address
- No emergency contact
- No active insurance coverage
- No preferred language
- Race/ethnicity not documented
- No advance directive on file
- Allergy documentation status unknown
```

## Troubleshooting

### No Patient Resource Found
- Verify the patient ID is correct. Try searching by name and DOB instead:
  ```
  Tool: fhir_search
  resourceType: "Patient"
  queryParams: "family=[lastname]&given=[firstname]&birthdate=[YYYY-MM-DD]"
  ```
- Check if the ID format matches the FHIR server's expectations (some use UUIDs, others use numeric IDs).

### RelatedPerson Search Returns Empty But Patient Has Emergency Contact in Record
- Some EHR systems store emergency contacts as extensions on the Patient resource rather than as separate RelatedPerson resources. Check `Patient.contact` array for embedded contact entries:
  ```
  Patient.contact[].relationship
  Patient.contact[].name
  Patient.contact[].telecom
  ```
- EPIC systems often use the `Patient.contact` array instead of RelatedPerson resources.

### Coverage Resources Missing Plan Details
- The `class` array may use different type codes depending on the payer. Check for `type.coding.code` values: "plan", "group", "subplan", "subgroup", "rxbin", "rxpcn".
- Some systems populate plan details in the `payor` referenced Organization resource. Follow the reference with `fhir_read` on the Organization.

## Related Skills

- `clinical-summary-generator` -- for clinical data beyond demographics
- `insurance-coverage-summary` -- for deeper insurance analysis including coordination of benefits
- `allergy-adverse-reaction-summary` -- when allergy documentation flag is raised
