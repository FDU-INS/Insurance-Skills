---
name: provider-for-encounter
description: |
  Generate appropriate provider entities for PatientSim encounters.
  Matches provider specialty to encounter type, diagnosis, and procedures.
  Supports attending, consulting, referring, and ordering provider roles.
  
  Trigger phrases: "provider for this encounter", "attending physician for",
  "generate provider for admission", "specialist for referral",
  "ordering provider for", "surgeon for procedure"
version: "1.0"
category: integration
related_skills:
  - synthetic-provider
  - synthetic-facility
cross_product:
  - patientsim
  - trialsim
---

# Provider for Encounter

## Overview

This integration skill generates appropriate provider entities for PatientSim encounters. It analyzes the encounter context (type, diagnosis, procedures, location) and generates providers with matching specialties, credentials, and affiliations.

Use this skill when you need to:
- Add realistic attending physicians to inpatient admissions
- Generate specialists for referral encounters
- Create ordering providers for lab/imaging orders
- Assign surgeons to procedural encounters
- Generate consulting physicians for complex cases

---

## Integration Pattern

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   PatientSim    │     │   Provider for       │     │   NetworkSim    │
│   Encounter     │────▶│   Encounter Skill    │────▶│   Provider      │
│   Context       │     │   (Matching Logic)   │     │   Entity        │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

---

## Input Context

### Required Context from PatientSim

```json
{
  "encounter_context": {
    "encounter_type": "inpatient | outpatient | emergency | ambulatory",
    "encounter_class": "AMB | EMER | IMP | OBSENC | PRENC | SS | VR",
    "service_type": "Medical | Surgical | OB | Psych | Rehab | ICU",
    "primary_diagnosis": {
      "code": "ICD-10 code",
      "description": "Diagnosis description",
      "category": "Cardiac | Oncology | Orthopedic | etc."
    },
    "procedures": [
      {
        "code": "CPT or ICD-10-PCS",
        "description": "Procedure description",
        "type": "Surgical | Diagnostic | Therapeutic"
      }
    ],
    "facility": {
      "type": "Hospital | Clinic | ASC | SNF",
      "location": {
        "city": "City",
        "state": "ST",
        "county_fips": "FIPS code"
      }
    }
  }
}
```

### Optional Context

```json
{
  "optional_context": {
    "patient_age": 65,
    "patient_sex": "M | F",
    "insurance_type": "Commercial | Medicare | Medicaid",
    "acuity": "Low | Medium | High | Critical",
    "referral_reason": "Specialty consultation reason",
    "existing_providers": ["NPIs of already-assigned providers"]
  }
}
```

---

## Provider Role Mapping

### By Encounter Type

| Encounter Type | Primary Role | Additional Roles |
|----------------|--------------|------------------|
| Inpatient | Attending | Admitting, Consulting, Referring |
| Outpatient | Treating | Referring, Ordering |
| Emergency | ED Physician | Consulting, Admitting |
| Ambulatory Surgery | Surgeon | Anesthesiologist, Assistant |
| Office Visit | Provider | Referring (if specialist) |

### By Service Line

| Service Line | Primary Specialty | Common Consultants |
|--------------|-------------------|-------------------|
| Medical | Internal Medicine, Hospitalist | Cardiology, Pulmonology, Nephrology, ID |
| Surgical | General Surgery, Specialty | Anesthesia, Hospitalist |
| Cardiac | Cardiology | Cardiac Surgery, EP, Interventional |
| Orthopedic | Orthopedic Surgery | PM&R, Pain Management |
| Oncology | Medical Oncology | Radiation Oncology, Surgical Oncology |
| OB/GYN | OB/GYN | MFM, Neonatology |
| Pediatric | Pediatrics | Pediatric subspecialties |
| Psychiatric | Psychiatry | Psychology, Social Work |
| Neurological | Neurology | Neurosurgery, PM&R |

---

## Specialty Matching Rules

### Diagnosis-to-Specialty Mapping

```json
{
  "diagnosis_specialty_map": {
    "I20-I25": {"primary": "Cardiology", "surgical": "Cardiothoracic Surgery"},
    "I50": {"primary": "Cardiology", "consult": ["Nephrology", "Pulmonology"]},
    "J44": {"primary": "Pulmonology", "consult": ["Internal Medicine"]},
    "N18": {"primary": "Nephrology", "consult": ["Internal Medicine"]},
    "E11": {"primary": "Endocrinology", "pcp": "Internal Medicine"},
    "C00-C97": {"primary": "Oncology", "surgical": "Surgical Oncology"},
    "M00-M99": {"primary": "Orthopedic Surgery", "consult": ["Rheumatology", "PM&R"]},
    "F20-F48": {"primary": "Psychiatry", "consult": ["Psychology"]},
    "G20-G26": {"primary": "Neurology", "surgical": "Neurosurgery"},
    "K70-K77": {"primary": "Gastroenterology", "surgical": "General Surgery"},
    "O00-O9A": {"primary": "OB/GYN", "consult": ["MFM", "Neonatology"]}
  }
}
```

### Procedure-to-Specialty Mapping

```json
{
  "procedure_specialty_map": {
    "33xxx": "Cardiothoracic Surgery",
    "27xxx": "Orthopedic Surgery",
    "43xxx": "General Surgery",
    "47xxx": "General Surgery",
    "49xxx": "General Surgery",
    "59xxx": "OB/GYN",
    "61xxx": "Neurosurgery",
    "92920-92944": "Interventional Cardiology",
    "36xxx": "Vascular Surgery",
    "CPT_anesthesia": "Anesthesiology"
  }
}
```

---

## Generation Workflow

### Step 1: Analyze Encounter Context

```json
{
  "analysis": {
    "encounter_type": "inpatient",
    "service_line": "Cardiac",
    "primary_diagnosis": "I21.0 - STEMI",
    "procedures": ["92920 - PCI"],
    "acuity": "Critical",
    "required_roles": ["Attending", "Interventional Cardiologist", "Consulting"]
  }
}
```

### Step 2: Determine Required Providers

```json
{
  "required_providers": [
    {
      "role": "Attending",
      "specialty": "Cardiology",
      "taxonomy": "207RC0000X",
      "required": true
    },
    {
      "role": "Proceduralist",
      "specialty": "Interventional Cardiology",
      "taxonomy": "207RC0001X",
      "required": true
    },
    {
      "role": "Consulting",
      "specialty": "Hospitalist",
      "taxonomy": "208M00000X",
      "required": false
    }
  ]
}
```

### Step 3: Generate Providers

Use [synthetic-provider](../synthetic/synthetic-provider.md) with matched parameters.

---

## Output Schema

```json
{
  "encounter_providers": {
    "encounter_id": "ENC-2024-001234",
    "facility_npi": "1234567890",
    
    "attending_provider": {
      "npi": "1987654321",
      "role": "Attending",
      "provider": {
        "last_name": "Chen",
        "first_name": "Michael",
        "credential": "MD, FACC"
      },
      "taxonomy": {
        "code": "207RC0000X",
        "display_name": "Cardiovascular Disease"
      },
      "assignment_reason": "Primary diagnosis I21.0 maps to Cardiology"
    },
    
    "procedural_provider": {
      "npi": "1876543210",
      "role": "Proceduralist",
      "provider": {
        "last_name": "Patel",
        "first_name": "Anita",
        "credential": "MD, FACC, FSCAI"
      },
      "taxonomy": {
        "code": "207RC0001X",
        "display_name": "Interventional Cardiology"
      },
      "procedure_performed": "92920",
      "assignment_reason": "PCI procedure requires Interventional Cardiology"
    },
    
    "consulting_providers": [
      {
        "npi": "1765432109",
        "role": "Consulting",
        "provider": {
          "last_name": "Williams",
          "first_name": "Sarah",
          "credential": "MD"
        },
        "taxonomy": {
          "code": "207R00000X",
          "display_name": "Internal Medicine"
        },
        "consult_reason": "Medical co-management",
        "assignment_reason": "Complex cardiac case with comorbidities"
      }
    ],
    
    "integration_metadata": {
      "source_product": "patientsim",
      "source_encounter_type": "inpatient",
      "matching_logic": "diagnosis_procedure_combined",
      "generated_at": "2024-12-24T10:30:00Z"
    }
  }
}
```

---

## Examples

### Example 1: Inpatient Heart Failure Admission

**PatientSim Context**:
```json
{
  "encounter_type": "inpatient",
  "primary_diagnosis": {"code": "I50.9", "description": "Heart failure, unspecified"},
  "facility": {"type": "Hospital", "location": {"city": "Houston", "state": "TX"}}
}
```

**Generated Providers**:
```json
{
  "attending_provider": {
    "npi": "1234567890",
    "provider": {"last_name": "Rodriguez", "first_name": "Maria", "credential": "MD, FACC"},
    "taxonomy": {"code": "207RC0000X", "display_name": "Cardiovascular Disease"},
    "assignment_reason": "Heart failure diagnosis (I50.9) maps to Cardiology"
  },
  "consulting_providers": [
    {
      "npi": "1345678901",
      "provider": {"last_name": "Kim", "first_name": "David", "credential": "MD"},
      "taxonomy": {"code": "207RN0300X", "display_name": "Nephrology"},
      "consult_reason": "Cardiorenal syndrome evaluation"
    }
  ]
}
```

### Example 2: Outpatient Orthopedic Surgery

**PatientSim Context**:
```json
{
  "encounter_type": "ambulatory",
  "encounter_class": "SS",
  "procedures": [{"code": "27447", "description": "Total knee arthroplasty"}],
  "facility": {"type": "ASC", "location": {"city": "Phoenix", "state": "AZ"}}
}
```

**Generated Providers**:
```json
{
  "surgical_provider": {
    "npi": "1456789012",
    "role": "Surgeon",
    "provider": {"last_name": "Thompson", "first_name": "Robert", "credential": "MD, FAAOS"},
    "taxonomy": {"code": "207X00000X", "display_name": "Orthopedic Surgery"},
    "procedure_performed": "27447"
  },
  "anesthesia_provider": {
    "npi": "1567890123",
    "role": "Anesthesiologist",
    "provider": {"last_name": "Lee", "first_name": "Jennifer", "credential": "MD"},
    "taxonomy": {"code": "207L00000X", "display_name": "Anesthesiology"},
    "anesthesia_type": "Regional"
  }
}
```

### Example 3: Emergency Department Visit

**PatientSim Context**:
```json
{
  "encounter_type": "emergency",
  "primary_diagnosis": {"code": "R10.9", "description": "Abdominal pain"},
  "acuity": "High",
  "facility": {"type": "Hospital", "location": {"city": "Chicago", "state": "IL"}}
}
```

**Generated Providers**:
```json
{
  "ed_provider": {
    "npi": "1678901234",
    "role": "ED Physician",
    "provider": {"last_name": "Martinez", "first_name": "Carlos", "credential": "MD, FACEP"},
    "taxonomy": {"code": "207P00000X", "display_name": "Emergency Medicine"}
  },
  "consulting_providers": [
    {
      "npi": "1789012345",
      "role": "Surgical Consult",
      "provider": {"last_name": "Brown", "first_name": "Amanda", "credential": "MD, FACS"},
      "taxonomy": {"code": "208G00000X", "display_name": "General Surgery"},
      "consult_reason": "Surgical abdomen evaluation"
    }
  ]
}
```

### Example 4: TrialSim Principal Investigator

**TrialSim Context**:
```json
{
  "study": {"therapeutic_area": "Oncology", "indication": "NSCLC"},
  "site": {"location": {"city": "Boston", "state": "MA"}, "type": "Academic Medical Center"}
}
```

**Generated Provider**:
```json
{
  "principal_investigator": {
    "npi": "1890123456",
    "role": "Principal Investigator",
    "provider": {"last_name": "Sullivan", "first_name": "Katherine", "credential": "MD, PhD"},
    "taxonomy": {"code": "207RH0003X", "display_name": "Hematology & Oncology"},
    "academic_affiliation": "Dana-Farber Cancer Institute",
    "research_credentials": ["Board Certified Medical Oncology", "GCP Certified"],
    "assignment_reason": "NSCLC trial requires Medical Oncologist with research credentials"
  }
}
```

---

## Validation Rules

| Rule | Validation |
|------|------------|
| Specialty Match | Provider specialty matches diagnosis/procedure |
| NPI Format | Valid 10-digit with Luhn check |
| Taxonomy Valid | Code exists in NUCC taxonomy |
| Role Appropriate | Role matches encounter type |
| Geographic Match | Provider location matches facility |
| Credential Match | Credentials appropriate for specialty |

---

## Cross-Product Integration

### To PatientSim

Provider entities integrate into PatientSim encounters:

```json
{
  "fhir_encounter": {
    "participant": [
      {
        "type": [{"coding": [{"code": "ATND", "display": "attender"}]}],
        "individual": {"reference": "Practitioner/{{npi}}"}
      }
    ]
  }
}
```

### To TrialSim

Provider entities become site investigators:

```json
{
  "trial_site": {
    "principal_investigator": {
      "npi": "{{npi}}",
      "name": "{{provider.last_name}}, {{provider.first_name}}",
      "role": "PI"
    }
  }
}
```

---

## Related Skills

- [Synthetic Provider](../synthetic/synthetic-provider.md) - Generate provider entities
- [Synthetic Facility](../synthetic/synthetic-facility.md) - Generate facility context
- [Network for Member](network-for-member.md) - Network context for claims

---

*Provider for Encounter is an integration skill in the NetworkSim product.*
