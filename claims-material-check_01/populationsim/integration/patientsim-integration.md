---
name: patientsim-integration
description: |
  Integration guide for PopulationSim to PatientSim data flow. Describes how 
  demographic distributions, health indicators, SDOH Z-codes, and insurance 
  coverage map to FHIR Patient, Condition, Coverage, and Observation resources.
  Updated for PopulationSim v2.0 Embedded Data Package.
version: "2.0"
---

# PopulationSim → PatientSim Integration

## Overview

This document describes how PopulationSim demographic and SDOH data flows into PatientSim to generate clinically realistic synthetic patients.

**Version 2.0 Update:** This integration now uses PopulationSim's embedded data package with real CDC PLACES, SVI, and ADI data, providing 100% US geographic coverage with provenance tracking.

---

## Embedded Data Files (v2.0)

PatientSim accesses these files directly for data-driven generation:

| Data Source | File Path | Records | Key Columns |
|-------------|-----------|---------|-------------|
| CDC PLACES (County) | `populationsim/data/county/places_county_2024.csv` | 3,144 | CountyFIPS, DIABETES_CrudePrev, OBESITY_CrudePrev, etc. |
| CDC PLACES (Tract) | `populationsim/data/tract/places_tract_2024.csv` | 83,522 | TractFIPS, all health measures |
| CDC SVI (County) | `populationsim/data/county/svi_county_2022.csv` | 3,144 | FIPS, RPL_THEMES, EP_UNINSUR, etc. |
| CDC SVI (Tract) | `populationsim/data/tract/svi_tract_2022.csv` | 84,120 | FIPS, all SVI themes |
| ADI (Block Group) | `populationsim/data/block_group/adi_blockgroup_2023.csv` | 242,335 | FIPS, ADI_NATRANK, ADI_STAESSION |

---

## Integration Flow

```
PopulationProfile                    PatientSim
      │                                   │
      ├─ demographics ──────────────────► Patient demographics
      │   ├─ age_distribution            │  ├─ birthDate
      │   ├─ sex_distribution            │  ├─ gender
      │   └─ race_ethnicity              │  └─ race/ethnicity extensions
      │                                   │
      ├─ health_indicators ─────────────► Condition prevalence
      │   ├─ chronic_conditions          │  ├─ Condition resources
      │   └─ health_behaviors            │  └─ Observation resources
      │                                   │
      ├─ sdoh_profile ──────────────────► SDOH documentation
      │   └─ z_code_mapping              │  ├─ Encounter diagnoses
      │                                  │  └─ Social History
      │                                   │
      └─ healthcare_access ─────────────► Coverage & access
          └─ insurance_coverage          │  ├─ Coverage resource
                                         │  └─ Organization (payer)
```

---

## Demographic Mapping

### Age Distribution

PopulationSim provides age distribution by bands. PatientSim samples from this distribution:

```json
// PopulationProfile input
{
  "demographics": {
    "age_distribution": {
      "0_4": 0.062,
      "5_17": 0.168,
      "18_24": 0.098,
      "25_34": 0.148,
      "35_44": 0.138,
      "45_54": 0.128,
      "55_64": 0.118,
      "65_74": 0.082,
      "75_plus": 0.058
    }
  }
}

// PatientSim output (FHIR Patient)
{
  "resourceType": "Patient",
  "birthDate": "1962-03-15",  // Sampled from 55_64 band
  "extension": [{
    "url": "http://hl7.org/fhir/StructureDefinition/patient-age",
    "valueAge": {"value": 62, "unit": "years"}
  }]
}
```

### Sex Distribution

```json
// PopulationProfile input
{
  "demographics": {
    "sex_distribution": {
      "male": 0.492,
      "female": 0.508
    }
  }
}

// PatientSim output
{
  "resourceType": "Patient",
  "gender": "female"  // 50.8% probability
}
```

### Race/Ethnicity

```json
// PopulationProfile input
{
  "demographics": {
    "race_ethnicity": {
      "white_nh": 0.298,
      "black_nh": 0.192,
      "hispanic": 0.432,
      "asian_nh": 0.072
    }
  }
}

// PatientSim output (US Core extensions)
{
  "resourceType": "Patient",
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
      "extension": [
        {"url": "ombCategory", "valueCoding": {
          "system": "urn:oid:2.16.840.1.113883.6.238",
          "code": "2106-3",
          "display": "White"
        }},
        {"url": "text", "valueString": "White"}
      ]
    },
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
      "extension": [
        {"url": "ombCategory", "valueCoding": {
          "system": "urn:oid:2.16.840.1.113883.6.238",
          "code": "2186-5",
          "display": "Not Hispanic or Latino"
        }},
        {"url": "text", "valueString": "Not Hispanic or Latino"}
      ]
    }
  ]
}
```

---

## Condition Prevalence Mapping

### Chronic Condition Assignment

PopulationSim health indicators drive condition assignment probability:

```json
// PopulationProfile input
{
  "health_indicators": {
    "chronic_conditions": {
      "diabetes": 0.108,
      "hypertension": 0.348,
      "obesity": 0.342,
      "depression": 0.198
    }
  }
}

// PatientSim processing
// For each patient:
// - 10.8% chance of diabetes diagnosis
// - 34.8% chance of hypertension
// - With comorbidity correlations applied
```

### Comorbidity Correlations

Apply realistic comorbidity relationships:

| Condition A | Condition B | Correlation |
|-------------|-------------|-------------|
| Diabetes | Hypertension | 0.65 |
| Diabetes | Obesity | 0.58 |
| Obesity | Hypertension | 0.52 |
| Depression | Diabetes | 0.35 |

```json
// PatientSim Condition output
{
  "resourceType": "Condition",
  "clinicalStatus": {"coding": [{
    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
    "code": "active"
  }]},
  "code": {"coding": [{
    "system": "http://hl7.org/fhir/sid/icd-10-cm",
    "code": "E11.9",
    "display": "Type 2 diabetes mellitus without complications"
  }]},
  "subject": {"reference": "Patient/pt-001"},
  "onsetDateTime": "2018-06-15"
}
```

---

## SDOH Z-Code Integration

### Z-Code Prevalence to Encounter Diagnoses

PopulationSim Z-code rates drive encounter diagnosis documentation:

```json
// PopulationProfile SDOH input
{
  "sdoh_profile": {
    "z_code_mapping": {
      "prevalence_rates": {
        "Z59.6": {"rate": 0.146, "description": "Low income"},
        "Z59.41": {"rate": 0.118, "description": "Food insecurity"},
        "Z56.0": {"rate": 0.054, "description": "Unemployment"},
        "Z59.82": {"rate": 0.070, "description": "Transportation insecurity"}
      }
    }
  }
}

// PatientSim Encounter with SDOH
{
  "resourceType": "Encounter",
  "id": "enc-001",
  "diagnosis": [
    {
      "condition": {"reference": "Condition/cond-dm-001"},
      "rank": 1
    },
    {
      "condition": {"reference": "Condition/cond-sdoh-001"},
      "rank": 2
    }
  ]
}

// SDOH Condition
{
  "resourceType": "Condition",
  "id": "cond-sdoh-001",
  "category": [{
    "coding": [{
      "system": "http://hl7.org/fhir/us/core/CodeSystem/us-core-category",
      "code": "sdoh"
    }]
  }],
  "code": {"coding": [{
    "system": "http://hl7.org/fhir/sid/icd-10-cm",
    "code": "Z59.6",
    "display": "Low income"
  }]},
  "subject": {"reference": "Patient/pt-001"}
}
```

### SDOH Screening Observations

Generate Gravity Project-aligned SDOH screening:

```json
{
  "resourceType": "Observation",
  "status": "final",
  "category": [{
    "coding": [{
      "system": "http://hl7.org/fhir/us/sdoh-clinicalcare/CodeSystem/SDOHCC-CodeSystemTemporaryCodes",
      "code": "sdoh-category-food-insecurity"
    }]
  }],
  "code": {"coding": [{
    "system": "http://loinc.org",
    "code": "88122-7",
    "display": "Within the past 12 months, you worried that your food would run out before you got money to buy more"
  }]},
  "valueCodeableConcept": {"coding": [{
    "system": "http://loinc.org",
    "code": "LA28397-0",
    "display": "Often true"
  }]},
  "subject": {"reference": "Patient/pt-001"}
}
```

---

## Insurance Coverage Mapping

### Coverage Distribution

```json
// PopulationProfile input
{
  "healthcare_access": {
    "insurance_coverage": {
      "commercial": 0.482,
      "medicare": 0.148,
      "medicaid": 0.198,
      "dual_eligible": 0.032,
      "uninsured": 0.148
    }
  }
}

// PatientSim Coverage output
{
  "resourceType": "Coverage",
  "status": "active",
  "type": {"coding": [{
    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code": "EHCPOL",
    "display": "extended healthcare"
  }]},
  "subscriber": {"reference": "Patient/pt-001"},
  "beneficiary": {"reference": "Patient/pt-001"},
  "payor": [{"reference": "Organization/payer-bluecross-001"}],
  "class": [{
    "type": {"coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/coverage-class",
      "code": "plan"
    }]},
    "value": "PPO-Gold-500"
  }]
}
```

---

## Utilization Pattern Integration

### Encounter Density

PopulationSim utilization patterns inform encounter generation:

```json
// PopulationProfile input
{
  "utilization_patterns": {
    "ambulatory_visits_per_capita": 4.8,
    "ed_visits_per_1k": 428,
    "inpatient_admits_per_1k": 98,
    "sdoh_adjustments": {
      "ed_multiplier": 1.18,
      "preventive_reduction": 0.88
    }
  }
}

// PatientSim encounter generation rules:
// - High-SDOH patients: ED visits × 1.18
// - High-SDOH patients: Preventive visits × 0.88
// - Generate ~4.8 ambulatory visits/year per patient
```

---

## Example: Complete Patient Generation

### Input: CohortSpecification with PopulationSim Data

```json
{
  "cohort_id": "cohort-dm-sdoh-001",
  "geography": {"fips": "48201"},
  "demographics": {
    "age": {"min": 40, "max": 70}
  },
  "clinical_profile": {
    "conditions": {
      "diabetes": {"required": true}
    }
  },
  "sdoh_requirements": {
    "svi_min": 0.60
  },
  "size": {"target": 100}
}
```

### Output: PatientSim Bundle

```json
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "pt-001",
        "identifier": [{
          "system": "http://healthsim.example/ssn",
          "value": "123-45-6789"
        }, {
          "system": "http://healthsim.example/mrn",
          "value": "MRN-000001"
        }],
        "name": [{"family": "Garcia", "given": ["Maria"]}],
        "gender": "female",
        "birthDate": "1968-07-22",
        "address": [{
          "city": "Houston",
          "state": "TX",
          "postalCode": "77004"
        }]
      }
    },
    {
      "resource": {
        "resourceType": "Condition",
        "id": "cond-dm-001",
        "code": {"coding": [{
          "system": "http://hl7.org/fhir/sid/icd-10-cm",
          "code": "E11.9"
        }]},
        "subject": {"reference": "Patient/pt-001"}
      }
    },
    {
      "resource": {
        "resourceType": "Condition",
        "id": "cond-sdoh-001",
        "code": {"coding": [{
          "system": "http://hl7.org/fhir/sid/icd-10-cm",
          "code": "Z59.6"
        }]},
        "subject": {"reference": "Patient/pt-001"}
      }
    }
  ]
}
```

---

## Provenance Tracking (v2.0)

Data-driven generation includes complete provenance in output metadata:

```json
{
  "resourceType": "Bundle",
  "meta": {
    "extension": [{
      "url": "http://healthsim.io/fhir/StructureDefinition/generation-provenance",
      "extension": [
        {
          "url": "generationMode",
          "valueCode": "data_driven"
        },
        {
          "url": "geography",
          "valueReference": {
            "display": "Harris County, TX (FIPS: 48201)"
          }
        },
        {
          "url": "dataSource",
          "extension": [
            {"url": "source", "valueCode": "CDC_PLACES_2024"},
            {"url": "dataYear", "valueInteger": 2022},
            {"url": "file", "valueString": "populationsim/data/county/places_county_2024.csv"},
            {"url": "fieldsUsed", "valueString": "DIABETES_CrudePrev,OBESITY_CrudePrev"}
          ]
        },
        {
          "url": "dataSource",
          "extension": [
            {"url": "source", "valueCode": "CDC_SVI_2022"},
            {"url": "dataYear", "valueInteger": 2022},
            {"url": "file", "valueString": "populationsim/data/county/svi_county_2022.csv"},
            {"url": "fieldsUsed", "valueString": "RPL_THEMES,EP_UNINSUR"}
          ]
        }
      ]
    }]
  },
  "entry": [...]
}
```

### Provenance Source Registry

| Source Code | Full Name | Data Year | Methodology |
|-------------|-----------|-----------|-------------|
| CDC_PLACES_2024 | CDC PLACES 2024 Release | 2022 BRFSS | Model-based small area estimates |
| CDC_SVI_2022 | CDC/ATSDR Social Vulnerability Index | 2018-2022 ACS | Percentile ranking |
| ADI_2023 | Area Deprivation Index v4.0.1 | 2019-2023 ACS | Factor analysis composite |
| CENSUS_ACS_2022 | American Community Survey | 2022 | Survey estimates |

---

## Related Skills

- [PopulationSim Data Integration](../../patientsim/data-integration.md) - PatientSim lookup patterns
- [Geographic Intelligence](../geographic/county-profile.md)
- [Health Patterns](../health-patterns/chronic-disease-prevalence.md)
- [Cohort Definition](../cohorts/cohort-specification.md)
