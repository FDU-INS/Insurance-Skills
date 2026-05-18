---
name: healthsim-architecture-guide
description: "Authoritative reference for HealthSim architecture, patterns, and conventions. Read this first when developing new skills or products."
---

# HealthSim Architecture Guide

**Version**: 4.0  
**Last Updated**: 2025-12-28  
**Purpose**: Authoritative reference for HealthSim architecture, patterns, and conventions.

---

## Table of Contents

1. [Philosophy](#1-philosophy)
2. [Product Family](#2-product-family)
3. [Product Relationships](#3-product-relationships)
4. [Directory Organization](#4-directory-organization)
5. [Skills Architecture](#5-skills-architecture)
6. [Canonical Data Models](#6-canonical-data-models)
7. [Output Formats](#7-output-formats)
8. [Data Architecture](#8-data-architecture)
9. [Extension Patterns](#9-extension-patterns)

---

## 1. Philosophy

### 1.1 Core Principles

**Conversation-First / Configuration via Conversation**

HealthSim replaces traditional programming with conversational AI. Users describe what they need; Claude generates realistic synthetic healthcare data using domain knowledge encoded in Skills.

**Why This Matters**
- No coding required for data generation
- Natural language is more accessible than APIs
- Domain expertise lives in Skills, not code
- Iteration is conversational, not compile-debug cycles

### 1.2 Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Single Unified Repository** | Users clone once, get everything |
| **Skills as Knowledge, Not Code** | Skills contain domain knowledge; Claude generates data |
| **Progressive Disclosure** | Master skill routes to detailed skills |
| **Format-Agnostic Generation** | Generate canonical JSON first, then transform |
| **Unified DuckDB Database** | Single database for entities, state, and reference data |
| **MCP for I/O Only** | MCP servers handle file/database ops; generation is conversational |

---

## 2. Product Family

### 2.1 Current Products

| Product | Domain | Primary Standards | Status |
|---------|--------|-------------------|--------|
| **PatientSim** | Clinical/EMR | FHIR R4, HL7v2, C-CDA | Active |
| **MemberSim** | Payer/Claims | X12 837/835, 834, 270/271 | Active |
| **RxMemberSim** | Pharmacy/PBM | NCPDP D.0 | Active |
| **TrialSim** | Clinical Trials | CDISC SDTM/ADaM | Active |
| **PopulationSim** | Demographics/SDOH | Census, ACS, SDOH indices | Active |
| **NetworkSim** | Provider Networks | NPPES, NPI, taxonomy | Active |

### 2.2 Product Capabilities Matrix

| Need | Primary Product | Supporting Products |
|------|----------------|---------------------|
| Patient demographics | PatientSim | PopulationSim (real rates) |
| Clinical encounters | PatientSim | NetworkSim (providers) |
| Lab results | PatientSim | - |
| Medication orders | PatientSim | RxMemberSim (fills) |
| Professional claims | MemberSim | PatientSim (encounter), NetworkSim (provider) |
| Facility claims | MemberSim | PatientSim (admission), NetworkSim (facility) |
| Pharmacy claims | RxMemberSim | PatientSim (medication), NetworkSim (pharmacy) |
| Trial subjects | TrialSim | PatientSim (baseline), PopulationSim (diversity) |
| SDTM domains | TrialSim | - |
| Provider entities | NetworkSim | - |
| Population statistics | PopulationSim | - |

---

## 3. Product Relationships

### 3.1 Architecture Diagram

```
                           ┌─────────────────────────────────────────────────────────┐
                           │                    HealthSim Ecosystem                   │
                           └─────────────────────────────────────────────────────────┘
                                                      │
              ┌──────────────────────────────────────┼──────────────────────────────────────┐
              │                                      │                                      │
              ▼                                      ▼                                      ▼
    ┌──────────────────┐                  ┌──────────────────┐                  ┌──────────────────┐
    │   Data Layer     │                  │  Generation      │                  │  Network Layer   │
    │                  │                  │  Products        │                  │                  │
    │  PopulationSim   │─────────────────▶│                  │◀────────────────│   NetworkSim     │
    │                  │  Demographics,   │  PatientSim      │  Providers,     │                  │
    │  • CDC PLACES    │  SDOH, rates     │  MemberSim       │  facilities,    │  • 8.9M NPIs     │
    │  • SVI           │                  │  RxMemberSim     │  pharmacies     │  • Facilities    │
    │  • ADI           │                  │  TrialSim        │                 │  • Quality Data  │
    │                  │                  │                  │                  │                  │
    └──────────────────┘                  └──────────────────┘                  └──────────────────┘
```

### 3.2 Data Flow Between Products

**Clinical → Claims → Pharmacy Flow**

```
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   PatientSim  │─────▶│   MemberSim   │─────▶│  RxMemberSim  │
│               │      │               │      │               │
│  • Encounter  │      │  • Claim      │      │  • Rx Claim   │
│  • Diagnosis  │      │  • Adjudicate │      │  • DUR Check  │
│  • Medication │      │  • Payment    │      │  • Fill       │
└───────────────┘      └───────────────┘      └───────────────┘
       │                      │                      │
       └──────────────────────┴──────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │    NetworkSim     │
                    │   (Provider NPI)  │
                    └───────────────────┘
```

**Trial Enrollment Flow**

```
┌───────────────┐      ┌───────────────┐
│   PatientSim  │─────▶│   TrialSim    │
│               │      │               │
│  • Patient    │      │  • Subject    │
│  • History    │      │  • Consent    │
│  • Baseline   │      │  • Randomize  │
│               │      │  • SDTM       │
└───────────────┘      └───────────────┘
       ▲                      ▲
       │                      │
┌──────┴──────┐      ┌────────┴────────┐
│PopulationSim│      │   NetworkSim    │
│ (Diversity) │      │ (Investigator)  │
└─────────────┘      └─────────────────┘
```

### 3.3 Identity Correlation

```
                    ┌─────────────────────────────────────┐
                    │               Person                │
                    │  (SSN as universal correlator)      │
                    └─────────────────────────────────────┘
                                     │
         ┌───────────────┬───────────┼───────────┬───────────────┐
         │               │           │           │               │
         ▼               ▼           ▼           ▼               ▼
    ┌─────────┐    ┌─────────┐ ┌─────────┐ ┌─────────┐    ┌─────────┐
    │ Patient │    │ Member  │ │RxMember │ │ Subject │    │ Patient │
    │  (MRN)  │    │(Member  │ │(Cardholder│ │(Subject │    │ (MRN)   │
    │         │    │   ID)   │ │   ID)   │ │   ID)   │    │         │
    └─────────┘    └─────────┘ └─────────┘ └─────────┘    └─────────┘
         │               │           │           │               │
    PatientSim     MemberSim   RxMemberSim   TrialSim      PatientSim
```

### 3.4 Common Workflows

| Workflow | Steps |
|----------|-------|
| **Simple Patient** | User Request → PatientSim → JSON/FHIR output |
| **Patient with Claims** | PatientSim → MemberSim (+ NetworkSim provider) → X12 output |
| **Complete Care Episode** | PatientSim admission → MemberSim claim → PatientSim discharge → RxMemberSim fills → MemberSim follow-up |
| **Data-Driven Population** | PopulationSim (lookup rates) → PatientSim/MemberSim (apply rates) → Output with provenance |
| **Clinical Trial** | TrialSim study → PatientSim baseline → TrialSim visits/AEs → SDTM output |

---

## 4. Directory Organization

### 4.1 Repository Structure

```
healthsim-workspace/
├── SKILL.md                           # Master entry point (routing)
├── README.md                          # Repository overview
├── CHANGELOG.md                       # Version history
├── healthsim.duckdb                   # Unified database (~1.7 GB via Git LFS)
│
├── docs/                              # Documentation
│   ├── HEALTHSIM-ARCHITECTURE-GUIDE.md    # This document
│   ├── HEALTHSIM-DEVELOPMENT-PROCESS.md
│   ├── data-architecture.md           # Database schema details
│   └── contributing.md
│
├── references/                        # Shared reference data
│   ├── code-systems.md               # ICD-10, CPT, LOINC, NDC
│   ├── terminology.md
│   └── validation-rules.md
│
├── formats/                           # Output format transformations
│   ├── fhir-r4.md
│   ├── hl7v2-adt.md
│   ├── x12-837.md
│   ├── ncpdp-d0.md
│   ├── cdisc-sdtm.md
│   └── dimensional-analytics.md
│
├── skills/                            # Domain-specific skills
│   ├── common/
│   │   └── state-management.md
│   ├── patientsim/
│   ├── membersim/
│   ├── rxmembersim/
│   ├── trialsim/
│   ├── populationsim/
│   └── networksim/
│
├── hello-healthsim/                   # Tutorials and examples
│   ├── README.md
│   └── examples/
│
├── packages/                          # Python infrastructure
│   ├── core/                          # Shared healthsim-core library
│   ├── patientsim/
│   ├── membersim/
│   └── rxmembersim/
│
└── scripts/                           # Utility scripts
```

### 4.2 Organization Principles

| Principle | Implementation |
|-----------|----------------|
| **Skills are flat** | Cohort files directly in `skills/{product}/` |
| **Formats are shared** | ALL output formats in root `formats/` |
| **References are shared** | ALL reference data in root `references/` |
| **Subcategories allowed** | Use sparingly (oncology/, pediatrics/, therapeutic-areas/) |
| **Python is separate** | Python packages in `packages/`, not mixed with skills |

---

## 5. Skills Architecture

### 5.1 Skill Types

| Type | Purpose | Location |
|------|---------|----------|
| **Master Skill** | Entry point, routing | `SKILL.md` (root) |
| **Product Skill** | Product overview | `skills/{product}/SKILL.md` |
| **Cohort Skill** | Specific use case | `skills/{product}/*.md` |
| **Format Skill** | Output transformation | `formats/*.md` |
| **Reference Skill** | Code lookups, rules | `references/*.md` |

### 5.2 Required YAML Frontmatter

Every skill MUST have:

```yaml
---
name: {skill-name}
description: "{What this skill does}. Use when user requests: {trigger 1}, {trigger 2}."
---
```

### 5.3 Standard Skill Sections

1. **Overview** - What this skill does
2. **Trigger Phrases** - When to activate
3. **Parameters** - Configurable options
4. **Generation Patterns** - Domain knowledge
5. **Examples** - At least 2 complete examples
6. **Validation Rules** - How to verify output
7. **Related Skills** - Links to related content

---

## 6. Canonical Data Models

### 6.1 Entity Extension Pattern

| Product | Base | Extended Entity |
|---------|------|-----------------|
| PatientSim | Person | Patient |
| MemberSim | Person | Member |
| RxMemberSim | Member | RxMember |
| TrialSim | Patient | Subject |
| PopulationSim | Person | PopulationMember |
| NetworkSim | - | Provider |

### 6.2 Standard Code Systems

| Data Type | Code System |
|-----------|-------------|
| Diagnoses | ICD-10-CM |
| Procedures | CPT/HCPCS |
| Labs | LOINC |
| Medications | NDC/RxNorm |
| Providers | NPI |
| Trial Domains | CDISC |
| Adverse Events | MedDRA |

---

## 7. Output Formats

### 7.1 Healthcare Standards

| Format | Skill | Use Case |
|--------|-------|----------|
| FHIR R4 | `formats/fhir-r4.md` | Modern interoperability |
| C-CDA | `formats/ccda-format.md` | Clinical documents |
| HL7v2 | `formats/hl7v2-*.md` | Legacy EMR |
| X12 | `formats/x12-*.md` | Claims, enrollment |
| NCPDP | `formats/ncpdp-d0.md` | Pharmacy |
| CDISC SDTM | `formats/cdisc-sdtm.md` | Trial regulatory |
| CDISC ADaM | `formats/cdisc-adam.md` | Trial analysis |

### 7.2 Export Formats

| Format | Skill | Use Case |
|--------|-------|----------|
| CSV | `formats/csv.md` | Spreadsheets |
| SQL | `formats/sql.md` | Database loading |
| Dimensional | `formats/dimensional-analytics.md` | Star schema |

### 7.3 Format by Product

| Product | Native Output | Healthcare Standards |
|---------|--------------|---------------------|
| PatientSim | JSON | FHIR R4, HL7v2, C-CDA |
| MemberSim | JSON | X12 837/835/834/270/271 |
| RxMemberSim | JSON | NCPDP D.0 |
| TrialSim | JSON | CDISC SDTM, CDISC ADaM |
| PopulationSim | JSON | CohortSpecification |
| NetworkSim | JSON | - |

---

## 8. Data Architecture

### 8.1 Unified DuckDB Database

HealthSim uses a single DuckDB database with three schemas:

| Schema | Purpose | Tables |
|--------|---------|--------|
| **main** | Generated entities + state management | patients, encounters, claims, cohorts, etc. |
| **network** | Real NPPES provider data | providers (8.9M), facilities, quality metrics |
| **population** | Real CDC/Census demographic data | places_county, svi_tract, adi_blockgroup, etc. |

**Location**: `healthsim-workspace/healthsim.duckdb` (~1.7 GB, distributed via Git LFS)

### 8.2 State Management

Cohorts are named snapshots containing generated entities with full provenance:

| Tool | Purpose | Token Cost |
|------|---------|------------|
| `healthsim_save_cohort` | Persist entities to database | - |
| `healthsim_load_cohort` | Load all entities (full data) | High |
| `healthsim_get_cohort_summary` | Load metadata + samples only | ~500 tokens |
| `healthsim_query` | SQL query against entities | Variable |
| `healthsim_list_cohorts` | List saved cohorts | Low |
| `healthsim_delete_cohort` | Remove cohort | - |

**Pattern Selection**:
- Small cohorts (<50 entities): Use `load_cohort` for full data
- Large cohorts (50+ entities): Use `get_summary` + `query` for token efficiency

See [Data Architecture Guide](data-architecture.md) for complete schema documentation.

---

## 9. Extension Patterns

### 9.1 Adding a New Skill

1. Create file in `skills/{product}/`
2. Add YAML frontmatter with triggers
3. Include at least 2 examples
4. Link from product SKILL.md
5. Add hello-healthsim example

### 9.2 Adding a New Product

1. Create `skills/{newproduct}/` directory
2. Create product SKILL.md
3. Update master SKILL.md routing
4. Update VS Code workspace
5. Update this architecture guide
6. Add hello-healthsim quickstart

### 9.3 Cross-Product Integration

When generating data that spans multiple products, follow these patterns:

**Identity Correlation:**
- Person is the base entity
- SSN serves as universal correlator
- Each product adds domain-specific identifiers (MRN, Member ID, Subject ID)

**Cross-Product Mappings:**

| Domain | PatientSim | MemberSim | RxMemberSim | TrialSim |
|--------|------------|-----------|-------------|----------|
| Oncology | `oncology/*.md` | `facility-claims.md` | `specialty-pharmacy.md` | `therapeutic-areas/oncology.md` |
| Cardiovascular | `heart-failure.md` | `facility-claims.md` | `retail-pharmacy.md` | `therapeutic-areas/cardiovascular.md` |
| Diabetes | `diabetes-management.md` | `professional-claims.md` | `retail-pharmacy.md` | - |

**Integration Pattern Examples:**

| Cohort | PatientSim | → MemberSim | → RxMemberSim |
|----------|------------|-------------|---------------|
| HF Admission | Inpatient encounter, meds, labs | Facility claim (DRG 291-293) | Discharge Rx fills (0-3 days) |
| Diabetes Visit | Office encounter, A1C | Professional claim (99214) | Rx fills same day |
| Oncology | Treatment regimen | Infusion claims (J-codes) | Oral oncolytic fills |

### 9.4 Checklist

- [ ] YAML frontmatter with name and description
- [ ] Trigger phrases included
- [ ] At least 2 complete examples
- [ ] Links use correct relative paths
- [ ] CHANGELOG.md updated

---

**Repository**: https://github.com/mark64oswald/healthsim-workspace

*End of Document*
