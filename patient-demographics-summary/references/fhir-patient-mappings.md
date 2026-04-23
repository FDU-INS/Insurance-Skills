# FHIR Patient Resource Field Mappings

## Patient Resource (R4)

### Core Data Elements

| FHIR Path | Description | Cardinality | Data Type |
|-----------|-------------|-------------|-----------|
| Patient.identifier | MRN, SSN, DL, etc. | 0..* | Identifier |
| Patient.active | Whether record is active | 0..1 | boolean |
| Patient.name | Legal, maiden, nickname | 0..* | HumanName |
| Patient.telecom | Phone, email, fax | 0..* | ContactPoint |
| Patient.gender | Administrative gender | 0..1 | code |
| Patient.birthDate | Date of birth | 0..1 | date |
| Patient.deceased[x] | Boolean or dateTime | 0..1 | boolean/dateTime |
| Patient.address | Home, work, temp | 0..* | Address |
| Patient.maritalStatus | Marital status code | 0..1 | CodeableConcept |
| Patient.multipleBirth[x] | Multiple birth indicator | 0..1 | boolean/integer |
| Patient.photo | Patient photo | 0..* | Attachment |
| Patient.contact | Emergency contacts (inline) | 0..* | BackboneElement |
| Patient.communication | Language preferences | 0..* | BackboneElement |
| Patient.generalPractitioner | PCP reference | 0..* | Reference |
| Patient.managingOrganization | Custodian organization | 0..1 | Reference |
| Patient.link | Links to other patient records | 0..* | BackboneElement |

### Identifier Type Codes

| Code | Display | System |
|------|---------|--------|
| MR | Medical Record Number | `http://terminology.hl7.org/CodeSystem/v2-0203` |
| SS | Social Security Number | `http://terminology.hl7.org/CodeSystem/v2-0203` |
| DL | Driver's License | `http://terminology.hl7.org/CodeSystem/v2-0203` |
| PPN | Passport Number | `http://terminology.hl7.org/CodeSystem/v2-0203` |
| PI | Patient Internal Identifier | `http://terminology.hl7.org/CodeSystem/v2-0203` |

### HumanName.use Codes

| Code | Meaning |
|------|---------|
| usual | Name commonly used |
| official | Legal name |
| temp | Temporary name |
| nickname | Preferred informal name |
| anonymous | Anonymous name |
| old | Previously used name |
| maiden | Maiden name (pre-marriage) |

### ContactPoint System Codes

| Code | Description |
|------|-------------|
| phone | Voice telephone |
| fax | Fax machine |
| email | Email address |
| pager | Pager |
| url | Web URL |
| sms | SMS-capable phone |
| other | Other contact method |

### ContactPoint Use Codes

| Code | Description |
|------|-------------|
| home | Home contact |
| work | Work contact |
| temp | Temporary contact |
| old | No longer in use |
| mobile | Mobile device |

### Address Use Codes

| Code | Description |
|------|-------------|
| home | Home address |
| work | Work address |
| temp | Temporary address |
| old | Previous address |
| billing | Billing address |

## US Core Extensions

### Race (Required by US Core)

**URL:** `http://hl7.org/fhir/us/core/StructureDefinition/us-core-race`

Structure:
```json
{
  "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
  "extension": [
    {
      "url": "ombCategory",
      "valueCoding": {
        "system": "urn:oid:2.16.840.1.113883.6.238",
        "code": "2106-3",
        "display": "White"
      }
    },
    {
      "url": "text",
      "valueString": "White"
    }
  ]
}
```

**OMB Race Categories:**

| Code | Display |
|------|---------|
| 1002-5 | American Indian or Alaska Native |
| 2028-9 | Asian |
| 2054-5 | Black or African American |
| 2076-8 | Native Hawaiian or Other Pacific Islander |
| 2106-3 | White |

### Ethnicity (Required by US Core)

**URL:** `http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity`

**OMB Ethnicity Categories:**

| Code | Display |
|------|---------|
| 2135-2 | Hispanic or Latino |
| 2186-5 | Not Hispanic or Latino |

### Birth Sex (US Core)

**URL:** `http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex`

| Code | Display |
|------|---------|
| F | Female |
| M | Male |
| UNK | Unknown |

### Gender Identity (US Core 6.1+)

**URL:** `http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity`

| Code | Display |
|------|---------|
| male | Male |
| female | Female |
| non-binary | Non-binary |
| transgender-male | Transgender male |
| transgender-female | Transgender female |
| other | Other |
| non-disclose | Does not wish to disclose |

## Patient.contact (Inline Emergency Contacts)

Some EHR systems (notably EPIC) embed emergency contacts in the Patient resource instead of using RelatedPerson.

```json
{
  "contact": [
    {
      "relationship": [
        {
          "coding": [
            {
              "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
              "code": "C",
              "display": "Emergency Contact"
            }
          ]
        }
      ],
      "name": {
        "family": "Garcia",
        "given": ["Roberto"]
      },
      "telecom": [
        {
          "system": "phone",
          "value": "(555) 234-5679",
          "use": "home"
        }
      ],
      "gender": "male"
    }
  ]
}
```

### Contact Relationship Codes (v2-0131)

| Code | Display |
|------|---------|
| C | Emergency Contact |
| N | Next of Kin |
| E | Employer |
| F | Federal Agency |
| I | Insurance Company |
| S | State Agency |
| U | Unknown |

## Communication / Language Preferences

```json
{
  "communication": [
    {
      "language": {
        "coding": [
          {
            "system": "urn:ietf:bcp:47",
            "code": "es",
            "display": "Spanish"
          }
        ]
      },
      "preferred": true
    }
  ]
}
```

### Common BCP-47 Language Codes

| Code | Language |
|------|----------|
| en | English |
| es | Spanish |
| zh | Chinese |
| fr | French |
| de | German |
| it | Italian |
| ja | Japanese |
| ko | Korean |
| pt | Portuguese |
| ru | Russian |
| ar | Arabic |
| vi | Vietnamese |
| tl | Tagalog |

## Marital Status Codes

**System:** `http://terminology.hl7.org/CodeSystem/v3-MaritalStatus`

| Code | Display |
|------|---------|
| A | Annulled |
| D | Divorced |
| I | Interlocutory |
| L | Legally Separated |
| M | Married |
| P | Polygamous |
| S | Never Married |
| T | Domestic Partner |
| U | Unmarried |
| W | Widowed |
| UNK | Unknown |

## RelatedPerson Resource

### Relationship Codes

**System:** `http://terminology.hl7.org/CodeSystem/v3-RoleCode`

| Code | Display |
|------|---------|
| FAMMEMB | Family Member |
| CHILD | Child |
| PRNT | Parent |
| SPS | Spouse |
| SIBLING | Sibling |
| EXT | Extended Family |
| FRND | Friend |
| GUARD | Guardian |
| POWATT | Power of Attorney |
| ECON | Emergency Contact |
| NOK | Next of Kin |

### Key Fields

| FHIR Path | Description |
|-----------|-------------|
| RelatedPerson.patient | Reference to Patient |
| RelatedPerson.relationship | Relationship type |
| RelatedPerson.name | Contact name |
| RelatedPerson.telecom | Phone, email |
| RelatedPerson.gender | Gender |
| RelatedPerson.birthDate | Date of birth |
| RelatedPerson.address | Address |
| RelatedPerson.period | When relationship is/was active |

## Provider-Specific Notes

### EPIC
- Emergency contacts stored in `Patient.contact` array, not RelatedPerson
- Race/ethnicity populated in US Core extensions
- MRN identifier type = "MR" with system = organization-specific OID
- MyChart status may appear in extensions

### Cerner
- Uses RelatedPerson for emergency contacts
- May include additional identifier types (encounter-specific)
- Language preferences in `Patient.communication`

### GCP Healthcare API
- Standard FHIR R4 mapping
- No provider-specific extensions
- Supports all US Core extensions if source data includes them
