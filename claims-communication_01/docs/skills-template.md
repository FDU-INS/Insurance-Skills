# SKILL.md Template

**Purpose**: Standard structure for all product SKILL.md files  
**Template From**: PatientSim SKILL.md (gold standard)

---

## Required Sections

### 1. YAML Frontmatter

```yaml
---
name: healthsim-[product]
description: "[Brief description]. Use when user requests: (1) [use case 1], (2) [use case 2], (3) [specific cohorts], (4) [output formats]."
---
```

**Critical**: Include trigger phrases in description for Claude routing.

---

### 2. Title Section

```markdown
# [Product Name] - [Brief Subtitle]
```

---

### 3. For Claude Section

```markdown
## For Claude

Use this skill when [primary trigger]. This is the primary skill for [core function].

**When to apply this skill:**

- User mentions [keyword 1]
- User requests [keyword 2]
- User specifies [cohorts]
- User asks for [output formats]

**Key capabilities:**

- [Capability 1]
- [Capability 2]
- [Capability 3]

For specific [cohorts], load the appropriate skill from the table below.
```

---

### 4. Overview Section

```markdown
## Overview

[Product] generates [primary output type], including:
- [Output category 1]
- [Output category 2]
- [Output category 3]
```

---

### 5. Quick Start Section

```markdown
## Quick Start

### Simple [Entity]

**Request:** "[Simple request]"

```json
{
  // Example output
}
```

### [Cohort]

**Request:** "[More complex request]"

Claude loads [[skill-file.md]](skill-file.md) and produces [result].
```

**Note**: Include 2-3 examples showing progression from simple to complex.

---

### 6. Cohort/Skill Table

```markdown
## Cohort Skills

Load the appropriate cohort based on user request:

| Cohort | Trigger Phrases | File |
|----------|-----------------|------|
| **[Cohort 1]** | keyword1, keyword2, keyword3 | [skill-file.md](skill-file.md) |
| **[Cohort 2]** | keyword1, keyword2 | [skill-file.md](skill-file.md) |
| **Subdirectory** | | |
| ↳ [Sub-cohort] | keywords | [subdir/skill.md](subdir/skill.md) |
```

**Note**: Use `↳` prefix for subdirectory skills. Group related skills together.

---

### 7. Generation Parameters

```markdown
## Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| [param1] | [type] | [default] | [description] |
| [param2] | [type] | [default] | [description] |
```

---

### 8. Output Entities (or equivalent)

```markdown
## Output Entities

### [Entity 1]
[Description of entity and key fields]

### [Entity 2]
[Description of entity and key fields]

See [data-models.md](../../references/data-models.md) for complete schemas.
```

---

### 9. Domain-Specific Rules (optional but recommended)

```markdown
## [Domain] Rules

[Product] ensures generated data is [domain-appropriate]:

1. **[Rule 1]**: [Description]
2. **[Rule 2]**: [Description]
3. **[Rule 3]**: [Description]
```

---

### 10. Output Formats

```markdown
## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| [Format 2] | "[trigger]" | [use case] |
```

---

### 11. Data Integration Section (if applicable)

```markdown
## Data Integration (PopulationSim v2.0)

[Product] integrates with PopulationSim's embedded data package...

### Enabling Data-Driven Generation

[Parameters and examples]

### Embedded Data Sources

[Table of data sources with files and use cases]

### Provenance Tracking

[Example of provenance metadata]
```

---

### 12. Examples Section

```markdown
## Examples

### Example 1: [Simple Case]

**Request:** "[Request text]"

**Output:**
```json
{
  // Complete example output
}
```

### Example 2: [Complex Case]

**Request:** "[Request text]"

[Description of output complexity and combinations]
```

---

### 13. Related Skills Section

```markdown
## Related Skills

### [Category 1]
- [skill-file.md](skill-file.md) - [Description]

### Cross-Product: [Product] ([Domain])

[Product] [entities] connect to [this product]:

| [This Product] [Entity] | [Other Product] Skill | [Relationship] |
|-------------------------|----------------------|----------------|
| [entity 1] | [skill.md](../product/skill.md) | [description] |

> **Integration Pattern:** [Description of how to integrate]

### Cross-Product: PopulationSim (Demographics & SDOH) - v2.0 Data Integration

[Data-driven generation patterns with examples]

### Output Formats
- [../../formats/format.md](../../formats/format.md) - [Description]
```

---

## Checklist

Before considering a SKILL.md complete:

- [ ] YAML frontmatter with name and description (including trigger phrases)
- [ ] "For Claude" section with when to apply and key capabilities
- [ ] Overview section
- [ ] Quick Start with 2-3 examples
- [ ] Cohort/Skill table with all skills listed
- [ ] Generation Parameters table
- [ ] Output Entities (or equivalent)
- [ ] Output Formats table
- [ ] At least 2 complete examples
- [ ] Related Skills section with:
  - [ ] Internal skill links
  - [ ] Cross-Product: MemberSim (if applicable)
  - [ ] Cross-Product: RxMemberSim (if applicable)
  - [ ] Cross-Product: PopulationSim (v2.0 data integration)
  - [ ] Cross-Product: NetworkSim (if applicable)
  - [ ] Cross-Product: TrialSim (if applicable)
  - [ ] Output Formats links

---

## Product-Specific Adaptations

| Product | Unique Sections |
|---------|-----------------|
| PatientSim | Clinical Coherence Rules |
| MemberSim | Adjudication Logic, Denial Reasons |
| RxMemberSim | DUR Alert Types, Formulary Concepts |
| TrialSim | Phase Skills, SDTM Domains, Therapeutic Areas |
| PopulationSim | Data Sources, Geographic Levels, SDOH Categories |
| NetworkSim | Reference Skills, Synthetic Skills, Integration Skills |

**Note**: Product-specific sections should come after standard sections but before Examples.

---

*Last Updated: December 2025*
