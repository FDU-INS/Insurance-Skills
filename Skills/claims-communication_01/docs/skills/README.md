# HealthSim Skills Documentation

Skills are Claude's domain knowledge - structured documents that encode healthcare expertise for accurate synthetic data generation.

## What Are Skills?

Skills provide:
- **Clinical accuracy** - Validated codes, terminology, realistic patterns
- **Domain knowledge** - Healthcare workflows, regulations, best practices
- **Reusable patterns** - Common scenarios that can be referenced across journeys

## Skill Categories

### Product Skills

Each HealthSim product has domain-specific skills:

| Product | Skills Location | Focus |
|---------|-----------------|-------|
| **PatientSim** | `/skills/patientsim/` | Clinical encounters, diagnoses, procedures |
| **MemberSim** | `/skills/membersim/` | Claims, eligibility, benefits |
| **RxMemberSim** | `/skills/rxmembersim/` | Pharmacy claims, formularies, DUR |
| **TrialSim** | `/skills/trialsim/` | Clinical trials, CDISC, protocols |
| **PopulationSim** | `/skills/populationsim/` | Demographics, geography |
| **NetworkSim** | `/skills/networksim/` | Providers, facilities, networks |

### Common Skills

Shared across products:

| Skill | Purpose |
|-------|---------|
| `state-management.md` | Entity persistence patterns |
| `code-systems.md` | ICD-10, CPT, SNOMED references |
| `data-models.md` | Canonical entity structures |

## Using Skills in Generation

### Automatic Resolution

The `SkillRegistry` maps conditions to skills automatically:

```python
EventDefinition(
    event_type="encounter",
    condition="diabetes"  # Auto-resolves to diabetes-management skill
)
```

### Explicit Reference

Reference specific skill content:

```python
EventDefinition(
    event_type="encounter",
    skill_ref=SkillReference(
        skill="diabetes-management",
        lookup="monitoring.lab_panels.comprehensive",
        fallback={"code": "80053"}
    )
)
```

## Skill Format

Skills follow a standard structure:

```markdown
# Skill Name

## Overview
Brief description and use cases

## Clinical Context
Domain knowledge and workflows

## Data Elements
### Category
- **Element**: Description
  - Code: `12345`
  - System: ICD-10

## Generation Patterns
How to use this knowledge in generation

## Related Skills
Links to related skills
```

See [Format Specification](format-specification-v2.md) for complete details.

## Creating Skills

See [Creating Skills Guide](creating-skills.md) for:
- Skill structure and required sections
- Code system references
- Validation patterns
- Testing approaches

## Migration

If updating from older skill formats, see [Migration Guide](migration-guide.md).

## Related Documentation

- [Skill Integration Guide](../guides/skill-integration.md) - Using skills in journeys
- [Creating Skills](creating-skills.md) - How to write new skills
- [Format Specification](format-specification-v2.md) - Detailed format reference
