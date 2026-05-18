# HealthSim Context for Claude Code

**Purpose:** Essential patterns and context for Claude Code sessions. Read this file first before any implementation work.

---

## Core Philosophy

**Conversation-First:** HealthSim generates synthetic healthcare data via natural language + Skills. No Python libraries or APIs - Skills contain domain knowledge, Claude generates data dynamically.

**Skills are Knowledge, Not Code:** Each skill file teaches Claude about a domain (e.g., pharmacy claims, clinical trials) so it can generate realistic data through conversation.

---

## Directory Structure

```
healthsim-workspace/
├── docs/                          # Architecture guides, development process
├── formats/                       # Output format specifications (JSON, FHIR, X12, SDTM)
├── references/                    # Code systems, data models, shared references
├── hello-healthsim/               # Getting started examples
│
├── skills/
│   ├── common/                    # Shared skills (state management)
│   ├── patientsim/                # Clinical/EMR cohorts
│   ├── membersim/                 # Payer/claims cohorts
│   ├── rxmembersim/               # Pharmacy/PBM cohorts
│   └── trialsim/                  # Clinical trials cohorts
│       ├── SKILL.md               # Master routing skill
│       ├── README.md              # Directory index
│       ├── therapeutic-areas/     # Disease-specific patterns
│       └── rwe/                   # Real-world evidence
│
└── packages/core/                 # Python validation (tests only)
```

**Rule:** Cohorts go in `skills/{product}/`, NOT in subdirectories unless there's a clear grouping (like `therapeutic-areas/`).

---

## Quality Patterns (MANDATORY)

### 1. YAML Frontmatter

Every skill file MUST start with:

```yaml
---
name: skill-name
description: "Brief description. Triggers: phrase1, phrase2, phrase3"
---

# Skill Title
```

### 2. Validation Rules Section

Every cohort skill MUST have a Validation Rules section with this EXACT format:

```markdown
## Validation Rules

| Field | Requirement | Example |
|-------|-------------|---------|
| field_name | Format or constraint | Sample value |
| another_field | Another constraint | Another sample |

### Business Rules

- **Rule Name**: Description of realistic business logic
- **Another Rule**: More guidance for realistic data generation
```

**Use tables, not bullet lists for field validation.**

### 3. Related Skills Section

Every skill MUST end with Related Skills:

```markdown
## Related Skills

### [Same Product]
- [SKILL.md](SKILL.md) - Product overview
- [related-skill.md](related-skill.md) - Description

### Cross-Product: [Other Product]
- [../otherprod/skill.md](../otherprod/skill.md) - Integration description

> **Integration Pattern:** Brief explanation of how products connect.
```

### 4. Examples

Every skill MUST have at least 2 complete examples with:
- Request (what user asks)
- Response (complete JSON output)

---

## Skill File Template

```markdown
---
name: skill-name
description: "Description with trigger phrases. Triggers: trigger1, trigger2"
---

# Skill Title

Brief overview paragraph.

## For Claude

When to use this skill and key decision points.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1 | string | Yes | What it does |

## Generation Patterns

### Pattern Name
Description and JSON structure.

## Examples

### Example 1: Basic Cohort

**Request:** "Generate a [thing]"

**Response:**
```json
{
  "field": "value"
}
```

### Example 2: Complex Cohort

**Request:** "Generate [complex thing]"

**Response:**
```json
{
  "field": "value"
}
```

## Validation Rules

| Field | Requirement | Example |
|-------|-------------|---------|
| field | constraint | sample |

### Business Rules

- **Rule Name**: Description

## Related Skills

### [Product]
- [SKILL.md](SKILL.md) - Overview

### Cross-Product: [Other Product]
- [link](link) - Description

> **Integration Pattern:** How they connect.
```

---

## Commit Message Format

```
[Product] Brief description

- Detail 1
- Detail 2
```

Examples:
- `[TrialSim] Add DM domain skill`
- `[Skills] Add validation rules to pharmacy skills`
- `[Docs] Update architecture guide with integration patterns`

---

## Products Overview

| Product | Domain | Key Standards |
|---------|--------|---------------|
| PatientSim | Clinical/EMR | FHIR, HL7v2, C-CDA |
| MemberSim | Payer/Claims | X12 837/835/834 |
| RxMemberSim | Pharmacy/PBM | NCPDP D.0 |
| TrialSim | Clinical Trials | CDISC SDTM/ADaM |
| PopulationSim | Demographics/SDOH | Census, ACS, SVI, ADI |
| NetworkSim | Provider Networks | NPPES, NPI (planned) |

---

## Cross-Product Integration

Entities inherit and extend:
```
Person (base)
├── Patient (PatientSim) - clinical encounters
├── Member (MemberSim) - insurance claims
├── RxMember (RxMemberSim) - pharmacy claims
└── Subject (TrialSim) - trial participation
```

**SSN is the universal correlator** when linking across products.

---

## Key Reference Documents

Before major implementation, read:
- `docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` - Overall architecture
- `docs/HEALTHSIM-DEVELOPMENT-PROCESS.md` - Workflow, checklists
- `references/data-models.md` - Entity schemas
- `references/code-systems.md` - ICD-10, CPT, LOINC, etc.

For TrialSim specifically:
- `docs/TRIALSIM-DEVELOPMENT-PLAN.md` - Roadmap
- `skills/trialsim/clinical-trials-domain.md` - Domain knowledge

---

## Common Pitfalls to Avoid

1. **Missing YAML frontmatter** - Every skill needs it
2. **Bullet-list validation rules** - Use tables, not bullets
3. **Missing examples** - Need at least 2 complete JSON examples
4. **Forgetting Related Skills** - Every skill needs cross-references
5. **Wrong directory** - Skills go in `skills/{product}/`, not nested deeply
6. **No CHANGELOG update** - Update `CHANGELOG.md` every session
7. **Vague commit messages** - Use `[Product] Description` format

---

## Verification Checklist

Before committing any new skill:

- [ ] YAML frontmatter with `name` and `description`
- [ ] At least 2 complete examples with JSON
- [ ] Validation Rules table (not bullets)
- [ ] Business Rules subsection
- [ ] Related Skills section with cross-product links
- [ ] README.md updated (if applicable)
- [ ] CHANGELOG.md updated
- [ ] Tests pass: `cd packages/core && python -m pytest tests/ -q`

---

## Current Status (December 2024)

- **PatientSim:** 18 skills ✅
- **MemberSim:** 9 skills ✅
- **RxMemberSim:** 9 skills ✅
- **TrialSim:** 13 skills ✅ (Phase 1 complete, Phase 2 next)
- **Tests:** 476/476 passing

**Next up:** TrialSim Phase 2 - SDTM domain skills (DM, AE, CM, LB, VS, EX, DS, MH)

---

*This file is the essential context for Claude Code sessions. When in doubt, check the full documentation in `docs/`.*
