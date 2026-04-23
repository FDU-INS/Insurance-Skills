# Skill Integration Guide

This guide explains how to use skill references in journey templates to dynamically resolve clinical codes and parameters from HealthSim skills.

## Overview

Journey templates traditionally hardcode clinical values:

```python
# Hardcoded approach (legacy)
{
    "event_type": "diagnosis",
    "parameters": {
        "icd10": "E11.9",
        "description": "Type 2 diabetes mellitus without complications"
    }
}
```

With skill integration, journeys reference skills instead:

```python
# Skill-aware approach
{
    "event_type": "diagnosis",
    "parameters": {
        "skill_ref": {
            "skill": "diabetes-management",
            "lookup": "diagnosis_code",
            "fallback": {"icd10": "E11.9", "description": "Type 2 diabetes"}
        }
    }
}
```

## Benefits

1. **Single Source of Truth**: Clinical codes defined once in skills
2. **Context-Aware**: Different codes based on entity attributes
3. **Maintainability**: Update codes in one place
4. **Documentation**: Skills include clinical rationale

## SkillReference Schema

A skill reference has four components:

| Field | Required | Description |
|-------|----------|-------------|
| `skill` | Yes | Name of the skill to reference |
| `lookup` | Yes | What to look up (e.g., "diagnosis_code", "medication") |
| `context` | No | Context for resolution (can include entity variables) |
| `fallback` | No | Default value if lookup fails |

### Example

```python
{
    "skill_ref": {
        "skill": "diabetes-management",
        "lookup": "diagnosis_code",
        "context": {"stage": "${entity.control_status}"},
        "fallback": {"icd10": "E11.9", "description": "Type 2 diabetes"}
    }
}
```

## Entity Variable Substitution

Use `${entity.attribute}` syntax to reference entity attributes:

```python
"parameters": {
    "severity": "${entity.control_status}",
    "skill_ref": {
        "skill": "diabetes-management",
        "lookup": "lab_order",
        "context": {"control_status": "${entity.control_status}"}
    }
}
```

When executed with an entity `{"control_status": "poorly-controlled"}`, the variables are resolved.

## Supported Lookups

The SkillResolver supports these lookup types:

| Lookup | Description | Typical Fields Returned |
|--------|-------------|------------------------|
| `diagnosis_code` | ICD-10 diagnosis code | `icd10`, `description` |
| `icd10` | ICD-10 code pattern match | `value` |
| `medication` | Medication information | `rxnorm`, `name`, `dose` |
| `first_line_medication` | First-line therapy | `rxnorm`, `drug_name` |
| `loinc` | Lab test code | `value` |
| `lab_order` | Lab order with ranges | `loinc`, `test_name`, `range` |

## Using Skill-Aware Journeys

### Available Templates

```python
from healthsim.generation import (
    SKILL_AWARE_TEMPLATES,
    list_skill_aware_templates,
    get_skill_aware_template,
)

# List available templates
templates = list_skill_aware_templates()
# ['diabetic-first-year-skill', 'ckd-management-skill', 
#  'hf-management-skill', 'pharmacy-adherence-skill']

# Get a specific template
template = get_skill_aware_template("diabetic-first-year-skill")
```

### Creating a Journey

```python
from healthsim.generation import JourneySpecification, get_skill_aware_template

template = get_skill_aware_template("diabetic-first-year-skill")
journey = JourneySpecification.model_validate(template)
```

### Executing Events

When events are executed, skill references are automatically resolved:

```python
from healthsim.generation import JourneyEngine
from datetime import date

engine = JourneyEngine(seed=42)

# Entity with attributes
entity = {
    "patient_id": "P001",
    "control_status": "moderate",
}

# Create timeline
timeline = engine.create_timeline(
    entity=entity,
    entity_type="patient",
    journey=journey,
    start_date=date(2025, 1, 1),
)

# Execute events - skill_ref is resolved automatically
for event in timeline.get_pending_events():
    result = engine.execute_event(timeline, event, entity)
    # Event handlers receive resolved parameters
```

## Creating Custom Skill-Aware Journeys

### Step 1: Define the Journey Template

```python
MY_JOURNEY = {
    "journey_id": "my-custom-journey",
    "name": "My Custom Journey",
    "description": "A journey using skill references",
    "products": ["patientsim"],
    "duration_days": 90,
    "events": [
        {
            "event_id": "initial_event",
            "name": "Initial Event",
            "event_type": "diagnosis",
            "product": "patientsim",
            "delay": {"days": 0},
            "parameters": {
                "skill_ref": {
                    "skill": "diabetes-management",
                    "lookup": "diagnosis_code",
                    "fallback": {"icd10": "Z00.00", "description": "Fallback"}
                }
            },
        },
    ],
}
```

### Step 2: Validate and Use

```python
journey = JourneySpecification.model_validate(MY_JOURNEY)
timeline = engine.create_timeline(entity, "patient", journey, date.today())
```

## Direct Skill Resolution

For one-off lookups outside of journeys:

```python
from healthsim.generation import resolve_skill_ref

# Quick lookup
result = resolve_skill_ref(
    skill="diabetes-management",
    lookup="diagnosis_code",
)
print(result)
# {'icd10': 'E11.9', 'description': 'Type 2 diabetes mellitus without complications'}
```

## Adding Skills for Resolution

Skills are markdown files in the `skills/` directory. To be resolved, a skill should include:

1. **Structured clinical codes** (ICD-10, RxNorm, LOINC)
2. **JSON code blocks** for medication/lab patterns
3. **Sections** matching lookup names

### Example Skill Structure

```markdown
---
name: my-condition
description: "Skill for my condition"
---

## Conditions
- E11.9 - My condition without complications
- E11.65 - My condition with complications

## Medication Patterns

### First-Line Therapy
```json
{
    "name": "DrugName",
    "code": "123456",
    "dose": "500 mg"
}
```
```

## Error Handling

### Fallback Behavior

If a skill can't be resolved, the fallback is used:

```python
{
    "skill_ref": {
        "skill": "nonexistent-skill",
        "lookup": "something",
        "fallback": {"default": "value"}  # Used when skill not found
    }
}
```

### No Fallback

If no fallback is provided and the skill can't be resolved, an empty dict is returned.

## Best Practices

1. **Always provide fallbacks** for critical parameters
2. **Use entity variables** for context-dependent resolution
3. **Keep skills focused** - one condition/domain per skill
4. **Document skills thoroughly** - include clinical rationale
5. **Test journeys** with different entity attributes

## Related Documentation

- [Generation API](../api/generation.md)
- [Journey Engine](../api/journey-engine.md)
- [Skills Reference](../skills/README.md)
