# FHIR R4 Format Transformation

## Trigger Phrases

- FHIR
- FHIR R4
- FHIR bundle
- FHIR resources
- FHIR patient
- FHIR encounter
- as FHIR
- interoperability

## Overview

FHIR (Fast Healthcare Interoperability Resources) R4 is the current normative release for healthcare data exchange. This skill transforms HealthSim entities into compliant FHIR R4 resources.

## Supported Resource Types

| HealthSim Entity | FHIR Resource | Profile |
|------------------|---------------|---------|
| Patient | Patient | US Core Patient |
| Encounter | Encounter | US Core Encounter |
| Diagnosis | Condition | US Core Condition |
| Medication | MedicationRequest | US Core MedicationRequest |
| LabResult | Observation | US Core Laboratory Result |
| VitalSign | Observation | US Core Vital Signs |
| Member | Patient + Coverage | US Core |
| Claim | Claim | CARIN BB |

## Patient Resource

### Mapping
```yaml
patient_mapping:
  resourceType: Patient

  id: "generated UUID"

  identifier:
    - system: "http://hospital.example.org/patient-mrn"
      value: patient.mrn
      type:
        coding:
          - system: "http://terminology.hl7.org/CodeSystem/v2-0203"
            code: "MR"
            display: "Medical Record Number"

  name:
    - use: "official"
      family: patient.name.family_name
      given: [patient.name.given_name, patient.name.middle_name]
      prefix: [patient.name.prefix]
      suffix: [patient.name.suffix]

  gender:
    M: "male"
    F: "female"
    O: "other"
    U: "unknown"

  birthDate: patient.birth_date  # YYYY-MM-DD

  deceasedBoolean: patient.deceased  # if no death_date
  deceasedDateTime: patient.death_date  # if death_date exists

  address:
    - use: "home"
      line: [patient.address.street_address, patient.address.street_address_2]
      city: patient.address.city
      state: patient.address.state
      postalCode: patient.address.postal_code
      country: patient.address.country

  telecom:
    - system: "phone"
      value: patient.contact.phone
      use: "home"
    - system: "phone"
      value: patient.contact.phone_mobile
      use: "mobile"
    - system: "email"
      value: patient.contact.email
```

### Example Output
```json
{
  "resourceType": "Patient",
  "id": "patient-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"]
  },
  "identifier": [
    {
      "system": "http://hospital.example.org/patient-mrn",
      "value": "MRN00000001",
      "type": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "MR",
            "display": "Medical Record Number"
          }
        ]
      }
    }
  ],
  "name": [
    {
      "use": "official",
      "family": "Smith",
      "given": ["John", "Robert"]
    }
  ],
  "gender": "male",
  "birthDate": "1975-03-15",
  "address": [
    {
      "use": "home",
      "line": ["123 Main Street"],
      "city": "Springfield",
      "state": "IL",
      "postalCode": "62701",
      "country": "US"
    }
  ],
  "telecom": [
    {
      "system": "phone",
      "value": "555-123-4567",
      "use": "home"
    }
  ]
}
```

## Encounter Resource

### Mapping
```yaml
encounter_mapping:
  resourceType: Encounter

  id: "generated UUID"

  identifier:
    - system: "http://hospital.example.org/encounter-id"
      value: encounter.encounter_id

  status:
    planned: "planned"
    arrived: "arrived"
    in-progress: "in-progress"
    on-hold: "onleave"
    finished: "finished"
    cancelled: "cancelled"

  class:
    system: "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    code:
      I: "IMP"      # Inpatient
      O: "AMB"      # Ambulatory
      E: "EMER"     # Emergency
      U: "ACUTE"    # Urgent
      OBS: "OBSENC" # Observation

  type:
    - coding:
        - system: "http://snomed.info/sct"
          code: "encounter type SNOMED code"

  subject:
    reference: "Patient/{patient_id}"

  participant:
    - individual:
        reference: "Practitioner/{attending_npi}"
        display: encounter.attending_physician

  period:
    start: encounter.admission_time  # ISO 8601
    end: encounter.discharge_time

  reasonCode:
    - text: encounter.chief_complaint

  hospitalization:
    dischargeDisposition:
      coding:
        - system: "http://terminology.hl7.org/CodeSystem/discharge-disposition"
          code: encounter.discharge_disposition
```

### Example Output
```json
{
  "resourceType": "Encounter",
  "id": "encounter-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-encounter"]
  },
  "identifier": [
    {
      "system": "http://hospital.example.org/encounter-id",
      "value": "ENC0000000001"
    }
  ],
  "status": "finished",
  "class": {
    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code": "IMP",
    "display": "inpatient encounter"
  },
  "type": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "32485007",
          "display": "Hospital admission"
        }
      ]
    }
  ],
  "subject": {
    "reference": "Patient/patient-001"
  },
  "period": {
    "start": "2025-01-10T14:30:00Z",
    "end": "2025-01-15T10:00:00Z"
  },
  "reasonCode": [
    {
      "text": "Shortness of breath"
    }
  ],
  "hospitalization": {
    "dischargeDisposition": {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/discharge-disposition",
          "code": "home",
          "display": "Home"
        }
      ]
    }
  }
}
```

## Condition Resource (Diagnosis)

### Mapping
```yaml
condition_mapping:
  resourceType: Condition

  id: "generated UUID"

  clinicalStatus:
    coding:
      - system: "http://terminology.hl7.org/CodeSystem/condition-clinical"
        code: "active"  # or resolved if resolved_date exists

  verificationStatus:
    coding:
      - system: "http://terminology.hl7.org/CodeSystem/condition-ver-status"
        code:
          final: "confirmed"
          working: "provisional"
          differential: "differential"
          admitting: "provisional"

  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/condition-category"
          code: "encounter-diagnosis"

  code:
    coding:
      - system: "http://hl7.org/fhir/sid/icd-10-cm"
        code: diagnosis.code
        display: diagnosis.description

  subject:
    reference: "Patient/{patient_id}"

  encounter:
    reference: "Encounter/{encounter_id}"

  onsetDateTime: diagnosis.diagnosed_date
  abatementDateTime: diagnosis.resolved_date
```

### Example Output
```json
{
  "resourceType": "Condition",
  "id": "condition-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-condition"]
  },
  "clinicalStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
        "code": "active"
      }
    ]
  },
  "verificationStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
        "code": "confirmed"
      }
    ]
  },
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/condition-category",
          "code": "encounter-diagnosis"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sid/icd-10-cm",
        "code": "I50.23",
        "display": "Acute on chronic systolic heart failure"
      }
    ]
  },
  "subject": {
    "reference": "Patient/patient-001"
  },
  "encounter": {
    "reference": "Encounter/encounter-001"
  },
  "onsetDateTime": "2025-01-10"
}
```

## Observation Resource (Lab Results)

### Mapping
```yaml
observation_mapping:
  resourceType: Observation

  id: "generated UUID"

  status: "final"

  category:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/observation-category"
          code: "laboratory"

  code:
    coding:
      - system: "http://loinc.org"
        code: lab_result.loinc_code
        display: lab_result.test_name

  subject:
    reference: "Patient/{patient_id}"

  encounter:
    reference: "Encounter/{encounter_id}"

  effectiveDateTime: lab_result.collected_time

  valueQuantity:
    value: lab_result.value  # numeric
    unit: lab_result.unit
    system: "http://unitsofmeasure.org"
    code: lab_result.unit  # UCUM code

  interpretation:
    - coding:
        - system: "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
          code:
            H: "H"
            L: "L"
            HH: "HH"
            LL: "LL"
            N: "N"

  referenceRange:
    - low:
        value: reference_min
        unit: lab_result.unit
      high:
        value: reference_max
        unit: lab_result.unit
```

### Example Output
```json
{
  "resourceType": "Observation",
  "id": "observation-001",
  "meta": {
    "profile": ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-observation-lab"]
  },
  "status": "final",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "laboratory",
          "display": "Laboratory"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "4548-4",
        "display": "Hemoglobin A1c/Hemoglobin.total in Blood"
      }
    ]
  },
  "subject": {
    "reference": "Patient/patient-001"
  },
  "effectiveDateTime": "2025-01-15T08:30:00Z",
  "valueQuantity": {
    "value": 9.2,
    "unit": "%",
    "system": "http://unitsofmeasure.org",
    "code": "%"
  },
  "interpretation": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
          "code": "H",
          "display": "High"
        }
      ]
    }
  ],
  "referenceRange": [
    {
      "low": {
        "value": 4.0,
        "unit": "%"
      },
      "high": {
        "value": 5.6,
        "unit": "%"
      },
      "text": "Normal: 4.0-5.6%"
    }
  ]
}
```

## Bundle Resource

### Transaction Bundle
```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "fullUrl": "urn:uuid:patient-001",
      "resource": { "resourceType": "Patient", "..." },
      "request": {
        "method": "POST",
        "url": "Patient"
      }
    },
    {
      "fullUrl": "urn:uuid:encounter-001",
      "resource": { "resourceType": "Encounter", "..." },
      "request": {
        "method": "POST",
        "url": "Encounter"
      }
    }
  ]
}
```

### Document Bundle (for complete patient record)
```json
{
  "resourceType": "Bundle",
  "type": "document",
  "identifier": {
    "system": "http://hospital.example.org/bundles",
    "value": "bundle-001"
  },
  "timestamp": "2025-01-15T10:00:00Z",
  "entry": [
    {
      "fullUrl": "urn:uuid:composition-001",
      "resource": {
        "resourceType": "Composition",
        "status": "final",
        "type": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "34133-9",
              "display": "Summarization of episode note"
            }
          ]
        }
      }
    }
  ]
}
```

## FHIR NDJSON Format

### What is NDJSON?

NDJSON (Newline Delimited JSON) is a format where each line contains exactly one complete, valid JSON object. Unlike standard FHIR JSON bundles, NDJSON doesn't wrap resources in a Bundle—each resource stands alone on its own line.

### When to Use NDJSON vs Standard FHIR JSON

| Format | Use Case | Request With |
|--------|----------|--------------|
| **FHIR Bundle (JSON)** | API transactions, single patient records, document exchange | "as FHIR", "as FHIR Bundle" |
| **FHIR NDJSON** | Bulk data export, analytics pipelines, data warehouse loading, streaming | "as FHIR NDJSON", "as bulk FHIR" |

### Key Differences

| Aspect | Standard FHIR JSON | FHIR NDJSON |
|--------|-------------------|-------------|
| **Structure** | Resources wrapped in Bundle | One resource per line, no wrapper |
| **Line breaks** | Allowed within resource (pretty-print) | NO line breaks within resource |
| **File extension** | `.json` | `.ndjson` |
| **Content-Type** | `application/fhir+json` | `application/fhir+ndjson` |
| **References** | Internal URN references in bundle | Typically use literal resource IDs |
| **Use case** | API calls, single transactions | Bulk export, analytics, streaming |

### NDJSON Example

Each line is a complete FHIR resource (shown here with line numbers for clarity):

```text
{"resourceType":"Patient","id":"patient-001","name":[{"family":"Smith","given":["John"]}],"gender":"male","birthDate":"1975-03-15"}
{"resourceType":"Patient","id":"patient-002","name":[{"family":"Garcia","given":["Maria"]}],"gender":"female","birthDate":"1965-08-22"}
{"resourceType":"Patient","id":"patient-003","name":[{"family":"Johnson","given":["Robert"]}],"gender":"male","birthDate":"1958-11-30"}
```

**Note:** In actual NDJSON files, each JSON object must be on a single line with no internal line breaks.

### FHIR Bulk Data Export Format

The [FHIR Bulk Data Access specification](https://hl7.org/fhir/uv/bulkdata/) uses NDJSON for exporting large datasets. When exporting bulk data:

1. **Separate files by resource type**: `Patient.ndjson`, `Observation.ndjson`, `Condition.ndjson`
2. **One resource per line**: No Bundle wrapper
3. **No internal formatting**: Each JSON object is minified to a single line

Example file structure for bulk export:

```text
export/
├── Patient.ndjson        # All patients, one per line
├── Observation.ndjson    # All observations, one per line
├── Condition.ndjson      # All conditions, one per line
├── MedicationRequest.ndjson
└── Encounter.ndjson
```

### Converting Between Formats

**Bundle → NDJSON:**
Extract each `entry[].resource` and write as a single line.

**NDJSON → Bundle:**
Read each line, parse as JSON, wrap in Bundle with appropriate `entry[]` structure.

### Trigger Phrases for NDJSON

- "as NDJSON"
- "as FHIR NDJSON"
- "bulk export format"
- "for bulk data"
- "newline delimited"
- "for analytics"
- "for data warehouse"

---

## Complete Patient Bundle Example

```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "fullUrl": "urn:uuid:patient-dm-001",
      "resource": {
        "resourceType": "Patient",
        "id": "patient-dm-001",
        "identifier": [
          {
            "system": "http://hospital.example.org/patient-mrn",
            "value": "MRN00000001"
          }
        ],
        "name": [
          {
            "family": "Garcia",
            "given": ["Maria", "Elena"]
          }
        ],
        "gender": "female",
        "birthDate": "1965-08-22"
      },
      "request": {
        "method": "POST",
        "url": "Patient"
      }
    },
    {
      "fullUrl": "urn:uuid:condition-dm-001",
      "resource": {
        "resourceType": "Condition",
        "clinicalStatus": {
          "coding": [
            {
              "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
              "code": "active"
            }
          ]
        },
        "code": {
          "coding": [
            {
              "system": "http://hl7.org/fhir/sid/icd-10-cm",
              "code": "E11.65",
              "display": "Type 2 diabetes with hyperglycemia"
            }
          ]
        },
        "subject": {
          "reference": "urn:uuid:patient-dm-001"
        },
        "onsetDateTime": "2015-03-20"
      },
      "request": {
        "method": "POST",
        "url": "Condition"
      }
    },
    {
      "fullUrl": "urn:uuid:observation-a1c-001",
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "category": [
          {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "laboratory"
              }
            ]
          }
        ],
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "4548-4",
              "display": "Hemoglobin A1c"
            }
          ]
        },
        "subject": {
          "reference": "urn:uuid:patient-dm-001"
        },
        "effectiveDateTime": "2025-01-15",
        "valueQuantity": {
          "value": 9.2,
          "unit": "%",
          "system": "http://unitsofmeasure.org"
        }
      },
      "request": {
        "method": "POST",
        "url": "Observation"
      }
    }
  ]
}
```

## Code System URIs

| Code System | URI |
|-------------|-----|
| ICD-10-CM | http://hl7.org/fhir/sid/icd-10-cm |
| SNOMED CT | http://snomed.info/sct |
| LOINC | http://loinc.org |
| CPT | http://www.ama-assn.org/go/cpt |
| RxNorm | http://www.nlm.nih.gov/research/umls/rxnorm |
| NDC | http://hl7.org/fhir/sid/ndc |
| UCUM | http://unitsofmeasure.org |

## Related Skills

- [hl7v2-adt.md](hl7v2-adt.md) - Legacy HL7v2 messages
- [x12-837.md](x12-837.md) - Claims format
- [../skills/patientsim/SKILL.md](../skills/patientsim/SKILL.md) - Patient data source
- [../references/data-models.md](../references/data-models.md) - Entity schemas
