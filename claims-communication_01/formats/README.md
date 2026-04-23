# Output Formats Reference

This directory contains format specifications for all supported output types across HealthSim products.

## Healthcare Standards

| Format | File | Products | Description |
|--------|------|----------|-------------|
| **FHIR R4** | [fhir-r4.md](fhir-r4.md) | PatientSim | HL7 FHIR R4 resources |
| **HL7v2 ADT** | [hl7v2-adt.md](hl7v2-adt.md) | PatientSim | Admit/Discharge/Transfer |
| **HL7v2 ORM** | [hl7v2-orm.md](hl7v2-orm.md) | PatientSim | Order messages |
| **HL7v2 ORU** | [hl7v2-oru.md](hl7v2-oru.md) | PatientSim | Results messages |
| **C-CDA** | [ccda-format.md](ccda-format.md) | PatientSim | Consolidated CDA |

## Claims & Enrollment (X12)

| Format | File | Products | Description |
|--------|------|----------|-------------|
| **X12 837** | [x12-837.md](x12-837.md) | MemberSim | Professional/Institutional claims |
| **X12 835** | [x12-835.md](x12-835.md) | MemberSim | Remittance advice |
| **X12 834** | [x12-834.md](x12-834.md) | MemberSim | Enrollment |
| **X12 270/271** | [x12-270-271.md](x12-270-271.md) | MemberSim | Eligibility inquiry/response |

## Pharmacy (NCPDP)

| Format | File | Products | Description |
|--------|------|----------|-------------|
| **NCPDP D.0** | [ncpdp-d0.md](ncpdp-d0.md) | RxMemberSim | Pharmacy claims |

## Clinical Trials (CDISC)

| Format | File | Products | Description |
|--------|------|----------|-------------|
| **CDISC SDTM** | [cdisc-sdtm.md](cdisc-sdtm.md) | TrialSim | Study Data Tabulation Model |
| **CDISC ADaM** | [cdisc-adam.md](cdisc-adam.md) | TrialSim | Analysis Data Model |

## Analytics & General

| Format | File | Products | Description |
|--------|------|----------|-------------|
| **Dimensional** | [dimensional-analytics.md](dimensional-analytics.md) | All | Star schema for BI |
| **SQL** | [sql.md](sql.md) | All | SQL DDL/DML output |
| **CSV** | [csv.md](csv.md) | All | Flat file export |

---

## Usage

Each format file contains:
- **Overview** - Format purpose and standards reference
- **Structure** - Segments, fields, or elements
- **Examples** - Complete sample outputs
- **Validation Rules** - Required fields, code sets
- **Cross-Product Integration** - How formats connect

## Related Documentation

- [Architecture Guide](../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) - Product architecture and format mappings
- [Data Architecture](../docs/data-architecture.md) - Database schema and storage
