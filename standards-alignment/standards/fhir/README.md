# HL7 FHIR (Fast Healthcare Interoperability Resources) — Standard Guidance

## Overview

HL7 FHIR is the primary interoperability standard for healthcare data exchange.
FHIR R4 (v4.0.1) defines resource models (Patient, Encounter, Condition, etc.),
terminology assets (CodeSystem, ValueSet), and REST patterns.

For MD-DDL modelling, reference FHIR resources and terminology definitions, not
transport-specific API implementation details.

## Local Reference Files

This directory contains pre-extracted reference data from FHIR R4.
Use these files for local lookup before browsing live documentation.

File | Contents | Use for
--- | --- | ---
[resources.md](resources.md) | Full resource index from StructureDefinition entries | Find candidate FHIR resources by name and canonical URL
[resources-detail.md](resources-detail.md) | Core healthcare resource details with key fields and base types | Attribute-level mapping and inheritance/context checks
[terminology.md](terminology.md) | CodeSystem and ValueSet index | Mapping MD-DDL enums and coded attributes

## Deterministic Lookup Process (No Guessing)

Use this process for FHIR alignment decisions:

1. Search [resources.md](resources.md) for the entity name or close variants.
2. Inspect [resources-detail.md](resources-detail.md) for candidate resource
   structure, base type, and key fields.
3. If the concept is coded (diagnosis type, procedure code, medication class),
   inspect [terminology.md](terminology.md) for matching CodeSystem/ValueSet.
4. If no clear match is found, use the live FHIR docs as fallback:
   `https://hl7.org/fhir/R4/resourcelist.html`

## Mapping Quality Decision

Signal | Action
--- | ---
Concept and definition match a FHIR resource closely | Reference directly; no qualification needed
Concept is a specialization of a FHIR resource | Reference parent resource and note specialization in description
Concept partially overlaps FHIR | Reference with qualification (`Partial alignment`) and explain the gap
No convincing FHIR counterpart | Do not force alignment; leave reference empty

## Common FHIR Mappings

Business Term | FHIR Resource | Notes
--- | --- | ---
Patient | Patient | Core individual receiving care
Encounter | Encounter | Care interaction over time
Diagnosis | Condition | Problem/diagnosis representation
Procedure | Procedure | Clinical procedure or intervention
Medication Administration | MedicationAdministration | Medication given to patient
Care Plan | CarePlan | Planned care activities
Provider | Practitioner / PractitionerRole | Person vs role separation
Facility | Organization / Location | Org identity vs physical site
Coverage | Coverage | Insurance coverage details
Claim | Claim | Financial reimbursement request
Consent | Consent | Permissions and privacy constraints

## FHIR Terminology in MD-DDL

When a concept is represented as a coded set:

- Use MD-DDL enum if the value set is stable and small for your domain slice.
- Use a reference entity if code metadata/versioning is required.
- Record the FHIR ValueSet or CodeSystem canonical URL in the `Reference` column.

## Regeneration

To regenerate local FHIR reference files:

```shell
python references/industry_standards/fhir/extract-references.py --download
```

This command downloads and caches these FHIR R4 bundles to:

- `references/industry_standards/fhir/r4/profiles-resources.json`
- `references/industry_standards/fhir/r4/valuesets.json`
- `references/industry_standards/fhir/r4/v3-codesystems.json`
- `references/industry_standards/fhir/r4/v2-tables.json`

Then it regenerates:

- `resources.md`
- `resources-detail.md`
- `terminology.md`

## Version and Source

- FHIR release: R4 (v4.0.1)
- Source bundles:
   `https://hl7.org/fhir/R4/profiles-resources.json`
   `https://hl7.org/fhir/R4/valuesets.json`
   `https://hl7.org/fhir/R4/v3-codesystems.json`
   `https://hl7.org/fhir/R4/v2-tables.json`
- License: CC0 (FHIR R4 specification)
