# HealthSim Skills-First Architecture

**Session 2 Deliverable - Architecture Design**  
**Version**: 1.0  
**Date**: 2025-12-09  
**Purpose**: Define the complete Skills-first architecture for HealthSim, replacing the Python library approach.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Skills Organization](#2-skills-organization)
3. [Skills File Format](#3-skills-file-format)
4. [Python-to-Skills Mapping](#4-python-to-skills-mapping)
5. [MCP Integration Points](#5-mcp-integration-points)
6. [Conversation Flow Patterns](#6-conversation-flow-patterns)
7. [Implementation Roadmap](#7-implementation-roadmap)

---

## 1. Architecture Overview

### 1.1 Design Philosophy

The Skills-first architecture replaces traditional Python libraries with conversational AI capabilities:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TRADITIONAL APPROACH                              │
│  User → Code → Python Library → Data Models → Output Formats        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ REPLACES
┌─────────────────────────────────────────────────────────────────────┐
│                    SKILLS-FIRST APPROACH                             │
│  User → Natural Language → Claude + Skills → Structured Output      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     HEALTHSIM SKILLS ECOSYSTEM                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  SCENARIO    │  │  REFERENCE   │  │     FORMAT                │  │
│  │  SKILLS      │  │  SKILLS      │  │     SKILLS                │  │
│  │              │  │              │  │                           │  │
│  │ • Diabetes   │  │ • ICD-10     │  │ • FHIR R4                 │  │
│  │ • Heart Fail │  │ • CPT        │  │ • HL7v2 ADT               │  │
│  │ • Sepsis     │  │ • LOINC      │  │ • X12 837/835             │  │
│  │ • Claims     │  │ • Medications│  │ • NCPDP D.0               │  │
│  │ • Pharmacy   │  │ • Lab Ranges │  │ • CSV/JSON                │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│         │                 │                      │                  │
│         └─────────────────┼──────────────────────┘                  │
│                           ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    CORE SKILLS                                │   │
│  │  • healthsim-overview (triggers all others)                   │   │
│  │  • data-model-reference (schemas)                             │   │
│  │  • validation-rules (coherence checks)                        │   │
│  │  • generation-patterns (reproducibility, distributions)       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                           │                                          │
│                           ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    MCP SERVERS                                │   │
│  │  • File System (read/write outputs)                           │   │
│  │  • Database (optional: Databricks, PostgreSQL)                │   │
│  │  • GitHub (version control, sharing)                          │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Skills as Knowledge, Not Code** | Skills contain domain knowledge and generation patterns; Claude generates data dynamically |
| **Progressive Disclosure** | Core overview skill triggers; detailed skills load only when needed |
| **Format-Agnostic Generation** | Generate canonical data first, then transform to any output format |
| **Conversation-Driven** | Natural language replaces configuration files and API calls |
| **MCP for I/O Only** | MCP servers handle file/database operations; generation is conversational |

---

## 2. Skills Organization

### 2.1 Directory Structure

```
healthsim-common/
├── SKILL.md                           # Master entry point
├── references/
│   ├── data-models.md                 # Entity schemas
│   ├── validation-rules.md            # All validation rules
│   ├── code-systems.md                # ICD-10, CPT, LOINC, etc.
│   └── generation-patterns.md         # Distributions, reproducibility
│
├── skills/
│   ├── patientsim/
│   │   ├── SKILL.md                   # PatientSim overview
│   │   ├── diabetes-management.md
│   │   ├── heart-failure.md
│   │   ├── chronic-kidney-disease.md
│   │   └── sepsis-acute-care.md
│   │
│   ├── membersim/
│   │   ├── SKILL.md                   # MemberSim overview
│   │   ├── professional-claims.md
│   │   ├── facility-claims.md
│   │   ├── prior-authorization.md
│   │   ├── accumulator-tracking.md
│   │   └── value-based-care.md
│   │
│   └── rxmembersim/
│       ├── SKILL.md                   # RxMemberSim overview
│       ├── retail-pharmacy.md
│       ├── specialty-pharmacy.md
│       ├── formulary-management.md
│       ├── dur-alerts.md
│       ├── prior-authorization.md
│       └── manufacturer-programs.md
│
├── formats/
│   ├── fhir-r4.md                     # FHIR R4 transformation
│   ├── hl7v2-adt.md                   # HL7v2 ADT messages
│   ├── x12-837.md                     # X12 837 claims
│   ├── x12-835.md                     # X12 835 remittance
│   ├── ncpdp-d0.md                    # NCPDP D.0 format
│   └── csv.md                         # CSV export
│
└── scripts/
    ├── validate_output.py             # Output validation
    └── format_converter.py            # Format transformation helpers
```

### 2.2 Skill Categories

| Category | Purpose | Loading Strategy |
|----------|---------|------------------|
| **Master Skill** | Entry point, routing to sub-skills | Always in context (metadata) |
| **Cohort Skills** | Clinical/business cohort patterns | Load when cohort matches |
| **Reference Skills** | Code systems, data models, rules | Load on demand |
| **Format Skills** | Output transformation patterns | Load when format requested |

### 2.3 Skill Naming Convention

```
Pattern: {product}-{domain}-{specificity}.md

Examples:
  patientsim-diabetes-management.md
  membersim-claims-professional.md
  rxmembersim-dur-alerts.md
  format-fhir-r4.md
  reference-icd10-codes.md
```

---

## 3. Skills File Format

### 3.1 YAML Frontmatter (Required)

Every skill MUST have YAML frontmatter with `name` and `description`:

```yaml
---
name: healthsim-diabetes-management
description: >
  Generate realistic Type 2 Diabetes patient cohorts including diagnosis,
  medication escalation, lab patterns, and complications. Use when user requests:
  (1) diabetic patients, (2) A1C/glucose testing, (3) diabetes medications like
  metformin or insulin, (4) diabetic complications, or (5) HEDIS diabetes measures.
---
```

### 3.2 Standard Skill Template

```markdown
---
name: {skill-name}
description: >
  {What this skill does}. Use when user requests: (1) {trigger 1}, (2) {trigger 2},
  (3) {trigger 3}. Part of HealthSim synthetic healthcare data generation.
---

# {Skill Title}

## Overview

{Brief description of what this skill generates and when to use it}

## Trigger Phrases

Activate this skill when user mentions:
- {phrase 1}
- {phrase 2}
- {phrase 3}

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| {param} | {type} | {default} | {description} |

## Generation Patterns

### {Pattern Category 1}

{Knowledge and rules for generating this aspect}

### {Pattern Category 2}

{Knowledge and rules for generating this aspect}

## Output Schemas

### {Entity 1}

```json
{
  "field": "type and constraints"
}
```

## Examples

### Example 1: {Cohort Name}

**User Request:** "{example request}"

**Generated Output:**
```json
{example output}
```

## Validation Rules

- {Rule 1}
- {Rule 2}

## Related Skills

- [{Related Skill 1}](path/to/skill.md) - {when to use}
- [{Related Skill 2}](path/to/skill.md) - {when to use}
```

### 3.3 Master Skill Template

The master SKILL.md serves as the entry point:

```markdown
---
name: healthsim
description: >
  HealthSim generates realistic synthetic healthcare data for testing EMR systems,
  claims processing, pharmacy benefits, and analytics. Use for ANY request involving:
  (1) synthetic patients or clinical data, (2) healthcare claims or billing,
  (3) pharmacy prescriptions or formularies, (4) HL7/FHIR/X12/NCPDP formats,
  (5) healthcare testing cohorts.
---

# HealthSim - Synthetic Healthcare Data Generation

## Overview

HealthSim is a family of Skills for generating realistic synthetic healthcare data:

| Product | Domain | Typical Outputs |
|---------|--------|-----------------|
| **PatientSim** | Clinical/EMR | Patients, encounters, diagnoses, labs, vitals |
| **MemberSim** | Payer/Claims | Members, claims, payments, accumulators |
| **RxMemberSim** | Pharmacy | Prescriptions, pharmacy claims, formularies, DUR |

## Quick Start

### Generate a Patient

"Generate a 65-year-old diabetic patient with hypertension"

→ Claude uses [diabetes-management.md](skills/patientsim/diabetes-management.md)

### Generate Claims

"Create professional claims for an office visit"

→ Claude uses [professional-claims.md](skills/membersim/professional-claims.md)

### Generate Pharmacy Data

"Generate a pharmacy claim with a DUR alert for drug interaction"

→ Claude uses [dur-alerts.md](skills/rxmembersim/dur-alerts.md)

## Skill Routing

Based on user request, load the appropriate cohort skill:

### PatientSim Cohorts
- [Diabetes Management](skills/patientsim/diabetes-management.md)
- [Heart Failure](skills/patientsim/heart-failure.md)
- [Chronic Kidney Disease](skills/patientsim/chronic-kidney-disease.md)
- [Sepsis/Acute Care](skills/patientsim/sepsis-acute-care.md)

### MemberSim Cohorts
- [Professional Claims](skills/membersim/professional-claims.md)
- [Facility Claims](skills/membersim/facility-claims.md)
- [Prior Authorization](skills/membersim/prior-authorization.md)
- [Accumulator Tracking](skills/membersim/accumulator-tracking.md)

### RxMemberSim Cohorts
- [Retail Pharmacy](skills/rxmembersim/retail-pharmacy.md)
- [Specialty Pharmacy](skills/rxmembersim/specialty-pharmacy.md)
- [DUR Alerts](skills/rxmembersim/dur-alerts.md)
- [Formulary Management](skills/rxmembersim/formulary-management.md)

## Output Formats

For format-specific output, load:
- [FHIR R4](formats/fhir-r4.md) - For FHIR bundles and resources
- [HL7v2 ADT](formats/hl7v2-adt.md) - For ADT messages
- [X12 837](formats/x12-837.md) - For professional/institutional claims
- [X12 835](formats/x12-835.md) - For remittance advice
- [NCPDP D.0](formats/ncpdp-d0.md) - For pharmacy claims

## Reference Data

For code lookups and validation:
- [Data Models](references/data-models.md) - Entity schemas
- [Code Systems](references/code-systems.md) - ICD-10, CPT, LOINC
- [Validation Rules](references/validation-rules.md) - Coherence checks
```

---

## 4. Python-to-Skills Mapping

### 4.1 Module Mapping

| Python Module | Skills Equivalent | Notes |
|--------------|-------------------|-------|
| `healthsim.person` | `references/data-models.md` (Person schema) | Schema as reference |
| `healthsim.generation.distributions` | `references/generation-patterns.md` | Claude implements distributions |
| `healthsim.generation.reproducibility` | `references/generation-patterns.md` (seed section) | Seed instructions for consistency |
| `healthsim.validation` | `references/validation-rules.md` | Rules as checklist |
| `patientsim.core.models` | `references/data-models.md` (Patient entities) | Entity schemas |
| `patientsim.core.reference_data` | `references/code-systems.md` | Code lookups |
| `patientsim.formats.fhir` | `formats/fhir-r4.md` | Transformation patterns |
| `patientsim.formats.hl7v2` | `formats/hl7v2-adt.md` | Message templates |
| `membersim.core.member` | `references/data-models.md` (Member entity) | Schema |
| `membersim.claims` | `skills/membersim/*.md` | Cohort patterns |
| `rxmembersim.dur` | `skills/rxmembersim/dur-alerts.md` | DUR rules |
| `rxmembersim.formulary` | `skills/rxmembersim/formulary-management.md` | Formulary patterns |

### 4.2 Functionality Translation

| Python Pattern | Skills Pattern |
|----------------|----------------|
| `class Patient(BaseModel)` | JSON schema in `data-models.md` |
| `def generate_one()` | Generation instructions in cohort skill |
| `WeightedChoice(options=[...])` | Distribution table in skill |
| `SeedManager(seed=42)` | "For reproducibility, use seed: 42" instruction |
| `validator` decorators | Validation checklist in skill |
| `FHIRTransformer.transform()` | Mapping tables in `fhir-r4.md` |
| `HL7v2Generator.generate_adt_a01()` | Message template in `hl7v2-adt.md` |

### 4.3 What Gets Lost (Acceptable Tradeoffs)

| Lost Capability | Mitigation | Impact |
|-----------------|------------|--------|
| Compile-time type checking | Claude validates at generation time | Low - caught immediately |
| Precise statistical distributions | Claude approximates well | Low for testing use case |
| Streaming large datasets | Generate in batches | Medium - manual batching |
| Unit test suite | Validation rules + spot checks | Low - different validation model |
| Import/dependency management | Skills self-contained | None - simpler |

---

## 5. MCP Integration Points

### 5.1 Required MCP Servers

| MCP Server | Purpose | When Used |
|------------|---------|-----------|
| **File System** | Save generated data to files | Always - output delivery |
| **GitHub** | Version control, sharing | Publishing datasets |

### 5.2 Database Integration (Conversation-First)

Database integration uses direct CLI commands rather than MCP servers, following the conversation-first philosophy:

| Database | Method | Authentication |
|----------|--------|----------------|
| **DuckDB** | Direct SQL generation | None (local/in-memory) |
| **Databricks** | `databricks sql -e` CLI | `databricks auth profiles` |
| **PostgreSQL** | Generated SQL scripts | User-managed connection |

### 5.3 MCP Tool Usage Patterns

#### Save Generated Data

```
User: "Generate 10 diabetic patients and save to CSV"

Claude:
1. Generate 10 patients using diabetes-management skill
2. Format as CSV
3. Use file system MCP to save: /output/patients.csv
4. Return download link
```

#### Load to Databricks (Conversation-First)

```
User: "Generate patients and load to Databricks"

Claude:
1. Confirm CLI authentication: databricks auth profiles
2. Generate SQL (CREATE TABLE + INSERT)
3. Execute via: databricks api post /api/2.0/sql/statements
4. Report success with row counts
```

No MCP server needed - just CLI auth and the SQL Statements API.

#### Publish to GitHub

```
User: "Create a sample dataset repository"

Claude:
1. Generate sample data across all domains
2. Create README documentation
3. Use GitHub MCP: create_repository, push_files
4. Return repository URL
```

### 5.4 MCP-Free Operations

These operations require NO MCP (pure conversation):

- Generating synthetic data (any volume Claude can output)
- Formatting data (JSON, CSV inline)
- Explaining schemas and rules
- Answering questions about healthcare data
- Validating user-provided data

---

## 6. Conversation Flow Patterns

### 6.1 Simple Generation Flow

```
User: "Generate a diabetic patient"
                │
                ▼
┌─────────────────────────────────────────┐
│ Claude loads: diabetes-management.md    │
│ Checks: age_range, control_status, etc. │
│ Applies: comorbidity probabilities      │
│ Generates: Patient + diagnoses + meds   │
└─────────────────────────────────────────┘
                │
                ▼
Claude outputs: JSON patient record with
               - Demographics
               - Diagnoses (E11.9, I10, E78.5)
               - Medications (metformin, lisinopril)
               - Labs (A1C, BMP)
```

### 6.2 Iterative Refinement Flow

```
User: "Generate a patient"
Claude: [generates basic patient]

User: "Make them older, with more complications"
Claude: [adjusts age to 72, adds nephropathy, neuropathy]

User: "Add an ER visit for chest pain"
Claude: [adds encounter, troponin labs, cardiology consult]

User: "Now format as FHIR bundle"
Claude: [loads fhir-r4.md, transforms to FHIR]
```

### 6.3 Batch Generation Flow

```
User: "Generate 100 members with varied demographics for testing"
                │
                ▼
Claude: "I'll generate 100 members. For reproducibility, I'll use
        seed 42 and apply these distributions:
        - Age: 18-75 (weighted toward 45-65)
        - Gender: 49% M, 51% F
        - Plan types: 35% HMO, 40% PPO, 25% HDHP
        
        Generating in batches of 20..."
                │
                ▼
[Generates 5 batches, outputs to file via MCP]
                │
                ▼
Claude: "Generated 100 members. Saved to /output/members.csv
        Summary:
        - Age range: 19-74 (mean: 48)
        - Gender: 48 M, 52 F
        - Plans: 34 HMO, 41 PPO, 25 HDHP"
```

### 6.4 Format Transformation Flow

```
User: "I have this patient data, convert to HL7v2 ADT A01"
[provides JSON patient]
                │
                ▼
Claude: [loads hl7v2-adt.md]
        [maps fields: mrn→PID-3, name→PID-5, etc.]
        [generates MSH, EVN, PID, PV1 segments]
                │
                ▼
Claude outputs:
MSH|^~\&|HEALTHSIM|HOSPITAL|EMR|HOSPITAL|20250115103000||ADT^A01|MSG001|P|2.5
EVN|A01|20250115103000
PID|1||MRN001||Smith^John||19650315|M
PV1|1|I|||...
```

### 6.5 Validation Flow

```
User: "Check if this patient data is valid"
[provides JSON]
                │
                ▼
Claude: [loads validation-rules.md]
        [checks structural rules]
        [checks temporal rules]
        [checks clinical coherence]
                │
                ▼
Claude: "Validation Results:
        ✓ Required fields present
        ✓ Date ordering valid
        ⚠ Warning: Metformin prescribed without diabetes diagnosis
        ✗ Error: discharge_time before admission_time"
```

---

## 7. Implementation Roadmap

### 7.1 Session 3-8 Plan

| Session | Focus | Deliverables |
|---------|-------|--------------|
| **Session 3** | Core Skills | Master SKILL.md, data-models.md, validation-rules.md |
| **Session 4** | PatientSim Cohorts | 4 clinical cohort skills with full examples |
| **Session 5** | MemberSim Cohorts | 5 claims cohort skills with X12 patterns |
| **Session 6** | RxMemberSim Cohorts | 6 pharmacy cohort skills with NCPDP patterns |
| **Session 7** | Format Skills | FHIR, HL7v2, X12, NCPDP transformation skills |
| **Session 8** | Integration & Testing | End-to-end testing, documentation, packaging |

### 7.2 Session 3 Specifics

**Objective**: Build the foundational Skills that all other Skills depend on.

**Deliverables**:

1. **Master SKILL.md** (~200 lines)
   - Complete frontmatter with comprehensive triggers
   - Skill routing table
   - Quick start examples
   
2. **references/data-models.md** (~500 lines)
   - All entity schemas from Domain Knowledge Base
   - JSON Schema format for each entity
   - Relationship documentation
   
3. **references/validation-rules.md** (~300 lines)
   - Structural validation rules
   - Temporal validation rules
   - Clinical coherence rules
   - Pharmacy validation rules
   
4. **references/code-systems.md** (~400 lines)
   - Common ICD-10 codes with descriptions
   - Common CPT codes with typical charges
   - LOINC mappings for labs
   - Medication reference data
   
5. **references/generation-patterns.md** (~200 lines)
   - Age distributions
   - Gender distributions
   - Identifier generation patterns
   - Reproducibility instructions

### 7.3 Quality Criteria

Each skill must meet these criteria:

| Criterion | Requirement |
|-----------|-------------|
| **Frontmatter** | Valid YAML with name + comprehensive description |
| **Triggers** | Clear activation phrases |
| **Examples** | At least 2 complete input/output examples |
| **Schemas** | JSON schemas for all generated entities |
| **Validation** | Explicit validation rules |
| **Cross-references** | Links to related skills |
| **Conciseness** | Under 500 lines (split if longer) |

### 7.4 Testing Approach

Skills are tested through conversation:

```
Test Case: Generate diabetic patient
1. Load diabetes-management skill
2. Request: "Generate a 55-year-old female with poorly controlled diabetes"
3. Verify output contains:
   - Age: 55
   - Gender: F
   - Diagnosis: E11.65 (T2DM with hyperglycemia)
   - A1C: 9.0-12.0% range
   - Medications: metformin + additional agent
   - Comorbidities: hypertension, hyperlipidemia with high probability
```

---

## 8. Appendix: Skill Templates

### 8.1 Cohort Skill Template

```markdown
---
name: healthsim-{cohort-name}
description: >
  Generate {cohort description}. Use when user requests: (1) {trigger 1},
  (2) {trigger 2}, (3) {trigger 3}. Part of HealthSim {product} cohorts.
---

# {Cohort Title}

## Overview

{What this cohort generates and clinical/business context}

## Trigger Phrases

- "{phrase 1}"
- "{phrase 2}"
- "{phrase 3}"

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| {param} | {type} | {default} | {valid values} |

## Clinical/Business Context

{Domain knowledge essential for realistic generation}

## Generation Rules

### {Category 1}: {Title}

{Specific rules and patterns}

### {Category 2}: {Title}

{Specific rules and patterns}

## Output Schema

```json
{
  "entity_type": {
    "field1": "type",
    "field2": "type"
  }
}
```

## Examples

### Example 1: {Name}

**Request**: "{user request}"

**Output**:
```json
{complete example output}
```

### Example 2: {Name}

**Request**: "{user request}"

**Output**:
```json
{complete example output}
```

## Validation Checklist

- [ ] {Validation rule 1}
- [ ] {Validation rule 2}

## Related Skills

- [Skill Name](path) - Use when {condition}
```

### 8.2 Format Skill Template

```markdown
---
name: healthsim-format-{format-name}
description: >
  Transform HealthSim data to {format} format. Use when user requests:
  (1) {format} output, (2) {standard} compliance, (3) {use case}.
---

# {Format Name} Transformation

## Overview

{What this format is and when to use it}

## Supported Transformations

| Source Entity | Target Resource/Segment |
|--------------|------------------------|
| {entity} | {target} |

## Mapping Tables

### {Entity} → {Target}

| Source Field | Target Field | Transformation |
|-------------|--------------|----------------|
| {source} | {target} | {rule} |

## Templates

### {Message/Resource Type}

```
{template with placeholders}
```

## Examples

### Example: {Cohort}

**Input**:
```json
{source data}
```

**Output**:
```
{formatted output}
```

## Validation

- {Format-specific validation rule 1}
- {Format-specific validation rule 2}
```

---

## Document Metadata

**Document**: HealthSim Skills-First Architecture  
**Version**: 1.0  
**Created**: 2025-12-09  
**Session**: 2 of 8  

**Architecture Decisions**:
- Skills as knowledge containers, not code
- Progressive disclosure for context efficiency
- MCP for I/O operations only
- Conversation-driven generation

**Next Session (3)**:
- Build core reference Skills
- Master SKILL.md with routing
- Data models, validation, code systems

---

*End of Document*
