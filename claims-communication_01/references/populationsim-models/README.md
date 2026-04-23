# PopulationSim Model Reference

## Overview

This directory contains the canonical data models for PopulationSim. These schemas define the structure for population profiles, cohort specifications, geographic entities, and SDOH assessments.

> **Note**: This folder is named `populationsim-models` to distinguish it from the multi-product `data-models.md` file in the parent folder. PopulationSim models are in a separate folder due to their complexity and interdependence.

---

## Core Models

| Model | Description | Primary Use |
|-------|-------------|-------------|
| [PopulationProfile](population-profile.md) | Comprehensive population snapshot | Geographic area analysis |
| [CohortSpecification](cohort-specification.md) | Cohort generation criteria | Population subsetting |
| [GeographicEntity](geographic-entity.md) | Geographic identification | Location reference |
| [SDOHProfile](sdoh-profile.md) | Social determinants assessment | SDOH analysis |

---

## Model Relationships

```
                    ┌─────────────────────┐
                    │  CohortSpecification │
                    │  (Input criteria)    │
                    └──────────┬──────────┘
                               │
                               ▼
┌─────────────────┐   ┌─────────────────────┐
│ GeographicEntity │◄──│   PopulationProfile  │
│ (Location)       │   │   (Output snapshot)  │
└─────────────────┘   └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     SDOHProfile      │
                    │ (Embedded or linked) │
                    └─────────────────────┘
```

---

## Model Hierarchy

### PopulationProfile
The primary output model containing:
- Demographics (age, sex, race/ethnicity)
- Health indicators (CDC PLACES measures)
- SDOH profile (embedded or referenced)
- Healthcare access metrics
- Utilization patterns

### CohortSpecification
The primary input model defining:
- Geographic constraints
- Demographic requirements
- Clinical criteria
- SDOH thresholds
- Integration settings

### GeographicEntity
Reusable geography reference:
- Census hierarchy (state → county → tract → block group)
- CBSA/MSA identification
- Urban/rural classification
- Special designations (HPSA, MUA)

### SDOHProfile
Detailed social determinants:
- Composite indices (SVI, ADI)
- Domain-specific factors
- Z-code prevalence mapping
- Healthcare access barriers

---

## Cross-Product Usage

### PatientSim
- Uses PopulationProfile for demographic distributions
- Uses SDOHProfile for Z-code assignment
- Uses CohortSpecification for patient filtering

### MemberSim
- Uses PopulationProfile for insurance mix
- Uses SDOHProfile for utilization adjustments
- Uses GeographicEntity for service area definition

### TrialSim
- Uses CohortSpecification for eligibility simulation
- Uses PopulationProfile for feasibility assessment
- Uses SDOHProfile for diversity planning

---

## Schema Versioning

All models include version metadata:

```json
{
  "metadata": {
    "version": "1.0",
    "created_at": "2024-12-23T10:30:00Z",
    "schema_version": "populationsim-models-v1"
  }
}
```

---

## Validation

Models should be validated against:
1. Required field presence
2. Value range constraints
3. Cross-field consistency
4. Geographic code validity
5. Sum-to-one distributions

---

## Related References

- [Geography Codes](../geography-codes.md) - FIPS, CBSA codes
- [Census Variables](../census-variables.md) - ACS variable dictionary
- [CDC PLACES Indicators](../cdc-places-indicators.md) - Health measures
- [SVI Methodology](../svi-methodology.md) - Social Vulnerability Index
- [ADI Methodology](../adi-methodology.md) - Area Deprivation Index
- [Code Systems](../code-systems.md) - Medical coding standards
