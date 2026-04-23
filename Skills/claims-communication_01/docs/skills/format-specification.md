# HealthSim Skills File Format Specification

**Version**: 1.0
**Last Updated**: 2025-11-26

## Overview

Skills files are the core abstraction in HealthSim that enable natural language configuration and reusable cohort templates. They are Markdown documents with structured sections that serve three purposes:

1. **Context for Claude** - Provide domain knowledge for conversation
2. **Configuration Templates** - Define reusable cohort patterns
3. **Generation Rules** - Specify constraints and distributions

## Design Philosophy

Skills files bridge human readability and machine parseability:
- **Human-First**: Written in Markdown, readable as documentation
- **LLM-Friendly**: Structured for Claude to interpret naturally
- **Programmatic**: Parseable into typed objects for code use
- **Composable**: Skills can reference and extend other skills

## File Structure

### Complete Example

```markdown
# Septic Patient Cohort
Generate patients presenting with sepsis and systemic infection.

## Metadata
- **Type**: cohort-template
- **Version**: 1.0
- **Author**: Clinical Team
- **Tags**: infectious-disease, critical-care, emergency

## Purpose
This skill generates realistic septic patient presentations for emergency department
and ICU training cohorts. Includes appropriate vital signs, labs, and medications.

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 60-85 | Patient age range (sepsis more common in elderly) |
| severity | enum | severe | Severity: moderate, severe, septic-shock |
| source | enum | pneumonia | Infection source: pneumonia, uti, abdominal |

## Generation Rules

### Demographics
- Age: {{age_range}}
- Gender: any

### Conditions
**Primary Diagnosis**:
- A41.9 (Sepsis, unspecified organism)

**Infection Source** (based on {{source}} parameter):
- pneumonia: J18.9 (Pneumonia, unspecified organism)
- uti: N39.0 (Urinary tract infection)
- abdominal: K65.9 (Peritonitis, unspecified)

**Comorbidities** (80% probability):
- I10 (Hypertension)
- E11.9 (Type 2 diabetes)
- N18.3 (CKD stage 3)

### Vital Signs
**Temperature**: 101-104°F (fever)
**Heart Rate**: 110-140 bpm (tachycardia)
**Respiratory Rate**: 24-32 /min (tachypnea)
**Blood Pressure**:
- moderate: 100-110/60-70 (hypotension)
- severe/septic-shock: 85-95/50-60 (severe hypotension)
**SpO2**: 88-92% (hypoxia)

### Laboratory
**Infection Markers**:
- WBC: 15-25 x10^3/uL (leukocytosis)
- CRP: 100-200 mg/L (elevated)
- Lactate: 2.5-4.0 mmol/L (moderate), 4.0-8.0 (severe)

**Organ Function**:
- Creatinine: 1.5-2.5 mg/dL (AKI)
- BUN: 30-50 mg/dL
- Bilirubin: 1.5-3.0 mg/dL

### Medications
**Antibiotics** (broad-spectrum):
- Ceftriaxone 2g IV Q24H
- Vancomycin 1.5g IV Q12H

**Supportive**:
- Normal Saline 1L IV bolus (fluid resuscitation)
- Norepinephrine 0.1-0.5 mcg/kg/min (if septic-shock)

### Timeline
1. **ED Admission**: Initial presentation
2. **Hour 1**: Blood cultures, antibiotics started
3. **Hour 3**: Repeat vitals, initial labs resulted
4. **Hour 6**: Admit to ICU if severe/septic-shock

## Variations

### Variation: Septic Shock
Override severity to septic-shock:
- Blood Pressure: 70-85/40-50 mmHg
- Lactate: 6.0-10.0 mmol/L
- Add vasopressors (Norepinephrine)
- Mechanical ventilation likely

### Variation: Community-Acquired Pneumonia Source
Override source to pneumonia:
- Add respiratory symptoms
- Chest X-ray findings
- Consider Azithromycin instead of Vancomycin

## Examples

### Example 1: Basic Sepsis Case
```
User: Generate a septic patient using default parameters
Expected:
- 60-85 year old patient
- Sepsis diagnosis with pneumonia source
- Elevated WBC, CRP, lactate
- Tachycardia, fever, hypotension
- Ceftriaxone + Vancomycin started
```

### Example 2: Septic Shock Case
```
User: Generate a septic shock patient
Expected:
- Severe hypotension (BP < 90 systolic)
- High lactate (> 4.0)
- Vasopressor support required
- ICU admission
```

## Clinical References
- Surviving Sepsis Campaign Guidelines
- SIRS Criteria (Systemic Inflammatory Response Syndrome)
- qSOFA Score (Quick Sequential Organ Failure Assessment)

## Dependencies
None - this is a standalone cohort template.
```

## Required Sections

### 1. Title (H1)
The skill name. Should be descriptive and unique.

```markdown
# Septic Patient Cohort
```

### 2. Description (First paragraph)
Brief overview of what the skill provides. Immediately follows the title.

```markdown
Generate patients presenting with sepsis and systemic infection.
```

### 3. Metadata Section
Structured metadata using bullet list format.

**Required Fields**:
- **Type**: One of `domain-knowledge`, `cohort-template`, `format-spec`, `validation-rules`
- **Version**: Semantic version (e.g., "1.0", "2.1.3")

**Optional Fields**:
- **Author**: Creator or maintaining team
- **Tags**: Comma-separated tags for categorization
- **Created**: ISO date (YYYY-MM-DD)
- **Updated**: ISO date (YYYY-MM-DD)

```markdown
## Metadata
- **Type**: cohort-template
- **Version**: 1.0
- **Author**: Clinical Team
- **Tags**: infectious-disease, critical-care
```

### 4. Purpose Section
Detailed explanation of when and why to use this skill. Required for all skill types.

```markdown
## Purpose
This skill generates realistic septic patient presentations for emergency department
and ICU training cohorts.
```

## Optional Sections (Type-Specific)

### For `cohort-template` Skills

#### Parameters Section
Defines configurable parameters using a table format.

**Table Columns**:
- **Parameter**: Parameter name (use snake_case)
- **Type**: Data type (`range`, `enum`, `boolean`, `integer`, `string`)
- **Default**: Default value
- **Description**: What the parameter controls

```markdown
## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age_range | range | 60-85 | Patient age range |
| severity | enum | severe | Severity: moderate, severe, septic-shock |
```

**Parameter Types**:
- `range`: Numeric range (e.g., "60-85", "2.0-4.5")
- `enum`: Fixed set of values (list allowed values in description)
- `boolean`: true/false
- `integer`: Whole number
- `string`: Free text

#### Generation Rules Section
Defines how to generate patient data. Use structured subsections:

```markdown
## Generation Rules

### Demographics
- Age: {{age_range}}
- Gender: weighted(male: 0.6, female: 0.4)
- Race: any

### Conditions
**Primary Diagnosis**:
- ICD-10 code and description

**Comorbidities** (probability):
- ICD-10 code (probability value)

### Vital Signs
- Parameter: range or value (description)

### Laboratory
- Test Name: range unit (interpretation)

### Medications
- Drug name dose route frequency (indication)

### Timeline
1. Time point: Event description
2. Time point: Event description
```

**Template Variables**:
- Use `{{parameter_name}}` to reference parameters
- Use `weighted(option1: 0.6, option2: 0.4)` for probabilistic selection
- Use `any` for no constraint

#### Variations Section
Define named variations that override base parameters.

```markdown
## Variations

### Variation: Name
Description of what this variation changes.
- Parameter: override value
- Add: additional elements
```

### For `domain-knowledge` Skills

#### Knowledge Section
Structured information for Claude's context. Use subsections for organization.

```markdown
## Knowledge

### Clinical Concepts
- **Sepsis**: Life-threatening organ dysfunction caused by dysregulated host response to infection
- **SIRS**: Systemic Inflammatory Response Syndrome

### Terminology
- **qSOFA**: Quick Sequential Organ Failure Assessment score
- **MAP**: Mean Arterial Pressure

### Diagnostic Criteria
1. Criterion one
2. Criterion two
```

### For `validation-rules` Skills

#### Rules Section
Validation rules to enforce.

```markdown
## Rules

### Rule: Name
- **Code**: RULE_001
- **Severity**: error | warning | info
- **Condition**: When this rule applies
- **Check**: What to validate
- **Message**: Error message template
```

### For `format-spec` Skills

#### Format Section
Specification of output format requirements.

```markdown
## Format

### Structure
Description of format structure.

### Required Fields
- Field name: description

### Encoding Rules
- Rule description
```

## Universal Optional Sections

### Examples Section
Usage examples showing expected behavior.

```markdown
## Examples

### Example 1: Title
```
User: [what user says]
Expected: [what should happen]
```
```

### References Section
External links and citations.

```markdown
## References
- Link to resource
- Citation to guideline
```

### Dependencies Section
Other skills this skill requires or extends.

```markdown
## Dependencies
- skills/domain/clinical-basics.md
- skills/formats/hl7v2-adt.md
```

## Composition Rules

When multiple skills are loaded together:

1. **Metadata**: Cannot conflict
   - Type must be compatible
   - Version conflicts flagged as warnings

2. **Parameters**: Later skills override earlier
   - Warning if parameter redefined with different type
   - Defaults can be overridden

3. **Generation Rules**:
   - Additive by default
   - Explicit override: Use `override: true` annotation
   - Conflicts should warn

4. **Knowledge**:
   - Always additive
   - Sections merged by heading

5. **Dependencies**:
   - Resolved recursively
   - Circular dependencies rejected

## Validation Rules

### File-Level Validation
- Must be valid Markdown
- Must have H1 title as first heading
- Must have description paragraph after title
- Must have Metadata section with required fields

### Metadata Validation
- Type must be one of allowed values
- Version must be valid semantic version
- Tags must be comma-separated if present

### Parameter Validation
- Table must have all required columns
- Parameter names must be valid identifiers
- Types must be recognized types
- Defaults must match declared type

### Generation Rules Validation
- Template variables must reference declared parameters
- ICD-10 codes should be valid format (letter + digits)
- Ranges must be valid (min <= max)

## File Naming Convention

Skills should be organized in a directory structure:

```
skills/
├── domain/              # Domain knowledge skills
│   ├── clinical-basics.md
│   └── infectious-disease.md
├── skills/           # Cohort templates
│   ├── sepsis.md
│   ├── diabetes-management.md
│   └── cardiac-arrest.md
├── formats/            # Format specifications
│   ├── hl7v2-adt.md
│   └── fhir-r4.md
└── validation/         # Validation rules
    └── clinical-plausibility.md
```

**Naming Convention**:
- Use kebab-case: `sepsis-cohort.md`
- Be descriptive: `type2-diabetes-outpatient.md`
- Avoid version in filename: Use Metadata.Version instead

## Best Practices

### Writing Skills

1. **Keep it Focused**: One clear purpose per skill
2. **Be Explicit**: Specify ranges and probabilities clearly
3. **Include Context**: Purpose and examples help understanding
4. **Use Parameters**: Make skills configurable rather than creating many variants
5. **Document Assumptions**: Note clinical reasoning in comments

### Using Template Variables

```markdown
# Good: Clear parameter usage
- Age: {{age_range}}
- Severity: {{severity_level}}

# Bad: Unclear or missing parameters
- Age: 60-85 (hardcoded, not configurable)
- Severity: {{level}} (parameter not declared)
```

### Defining Ranges

```markdown
# Good: Explicit ranges with units
- Glucose: 200-350 mg/dL (hyperglycemia)
- Temperature: 101.0-103.5°F (fever)

# Bad: Ambiguous ranges
- Glucose: high
- Temperature: elevated
```

### Probability Notation

```markdown
# Good: Clear probabilities
- Gender: weighted(male: 0.55, female: 0.45)
- Comorbidity: 80% (occurs in 80% of generated patients)

# Acceptable: Descriptive probabilities
- Comorbidity: likely (> 70%)
- Comorbidity: rare (< 10%)
```

## Extensibility

The format is designed for extension:

1. **Custom Sections**: Skills can include additional H2 sections for specific needs
2. **Annotations**: Use `<!-- comment -->` for parsing hints
3. **YAML Frontmatter**: Optional for additional metadata (future)

### Example Custom Section

```markdown
## Clinical Notes Template
Template text for generated clinical notes, using {{parameter}} substitution.

<!-- parser: template-text -->
Patient presents with {{chief_complaint}}. Vital signs show {{vitals_summary}}.
Assessment: {{diagnosis}}
Plan: {{treatment_plan}}
```

## Version History

- **1.0** (2025-11-26): Initial specification

## See Also

- [Skills Format v2.0 Specification](format-specification-v2.md) - Claude-optimized format
- [Migration Guide](migration-guide.md) - Migrating v1.0 to v2.0
- [Creating Skills](creating-skills.md) - Guide to authoring skills
