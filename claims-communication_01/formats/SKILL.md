---
name: formats
description: Output format specifications for healthcare data standards. Use when generating or converting data to FHIR R4, HL7v2 (ADT/ORM/ORU), C-CDA, X12 (837/835/834/270-271), NCPDP D.0, CDISC SDTM/ADaM, CSV, SQL, or dimensional analytics formats.
---

# Output Formats Reference

Format specifications for all supported output types across HealthSim products.

## Available Formats

### Healthcare Standards
- [FHIR R4](fhir-r4.md) — HL7 FHIR R4 resources (PatientSim)
- [HL7v2 ADT](hl7v2-adt.md) — Admit/Discharge/Transfer messages
- [HL7v2 ORM](hl7v2-orm.md) — Order messages
- [HL7v2 ORU](hl7v2-oru.md) — Results messages
- [C-CDA](ccda-format.md) — Consolidated CDA documents

### Claims & Enrollment (X12)
- [X12 837](x12-837.md) — Professional/Institutional claims
- [X12 835](x12-835.md) — Remittance advice
- [X12 834](x12-834.md) — Enrollment/benefit maintenance
- [X12 270/271](x12-270-271.md) — Eligibility inquiry/response

### Pharmacy
- [NCPDP D.0](ncpdp-d0.md) — Pharmacy claims telecommunication

### Clinical Trials
- [CDISC SDTM](cdisc-sdtm.md) — Study Data Tabulation Model
- [CDISC ADaM](cdisc-adam.md) — Analysis Data Model

### Analytics
- [CSV](csv.md) — Flat file export
- [SQL](sql.md) — Database insert/DDL statements
- [Dimensional Analytics](dimensional-analytics.md) — Star schema fact/dimension tables

## Usage

When generating data in any product, specify the desired output format. Each format file contains the complete field mapping, validation rules, and example output.
