---
name: profile-builder
description: |
  Guides users through building structured profile specifications via natural conversation.
  Interprets user intent, asks clarifying questions, applies domain knowledge, and produces
  validated JSON specifications ready for execution.
triggers:
  - build a profile
  - create a population profile
  - help me define a cohort
  - I need patients with
  - I need members with
  - set up a generation profile
  - profile builder
outputs:
  - ProfileSpecification (JSON)
  - JourneySpecification (JSON, optional)
---

# Profile Builder Skill

Build structured profile specifications through conversation for batch data generation.

## Overview

The Profile Builder separates **specification building** (creative, conversational) from **execution** (deterministic, mechanical). This gives users conversation-first flexibility while enabling reproducible generation.

## Conversation Flow

### Phase 1: Understand Intent

Start by capturing the high-level goal:

**Example Opening:**
```
User: "I need Medicare diabetic patients for testing"

Claude: "I'll help you build a profile for Medicare diabetic patients.

Quick questions to get started:

1. **Quantity**: How many patients? (default: 100)
2. **Products**: Which output do you need?
   - PatientSim (clinical data, HL7, FHIR)
   - MemberSim (claims, X12)
   - Both (integrated patient + claims)

Or just say 'use defaults' and I'll apply sensible starting values."
```

### Phase 2: Gather Requirements

For each category, offer defaults with option to customize:

**Demographics:**
```
"Demographics (Medicare population):
• Age 65+ (mean ~72) - OK or adjust?
• Standard M/F ratio (48/52) - OK or adjust?
• Geographic focus? (US national, or specific state/region)"
```

**Clinical:**
```
"Clinical (Diabetes):
• Type 2 diabetes (E11.x) - assumed, correct?
• Include standard comorbidities? (HTN 75%, hyperlipidemia 70%, etc.)
• Severity mix? (controlled/uncontrolled/with complications)"
```

### Phase 3: Refine Details

```
User: "Texas only, use standard comorbidities, mix of severity"

Claude: "Perfect. Building your profile with:
• 200 patients, PatientSim + MemberSim
• Medicare, 65+ (mean 72, std dev 8)
• Texas geography (will use real PopulationSim data for cities)
• Type 2 diabetes (100%) with:
  - 30% controlled (A1c < 7.0)
  - 50% uncontrolled (A1c 7.0-9.0)
  - 20% with complications

Standard Medicare diabetic comorbidities:
• Hypertension: 75%
• Hyperlipidemia: 70%
• CKD Stage 3+: 25%
• Heart failure: 15%
• Obesity: 40%

Coverage: 55% Medicare Advantage / 45% Original Medicare

Should I proceed with this profile, or would you like to adjust anything?"
```

### Phase 4: Output Specification

Present the complete JSON specification for review:

```json
{
  "profile": {
    "id": "medicare-diabetic-texas-001",
    "name": "Texas Medicare Diabetic Population",
    "version": "1.0",
    "created": "2025-01-15T10:30:00Z",
    
    "generation": {
      "count": 200,
      "products": ["patientsim", "membersim"],
      "seed": null,
      "validation": "strict"
    },
    
    "demographics": {
      "age": {
        "type": "normal",
        "mean": 72,
        "std_dev": 8,
        "min": 65,
        "max": 95
      },
      "gender": {
        "type": "categorical",
        "weights": {"M": 0.48, "F": 0.52}
      },
      "geography": {
        "source": "populationsim",
        "reference": {
          "state": "TX",
          "city_distribution": "population_weighted"
        }
      }
    },
    
    "clinical": {
      "primary_condition": {
        "code": "E11",
        "description": "Type 2 diabetes mellitus",
        "prevalence": 1.0
      },
      "severity": {
        "type": "categorical",
        "weights": {
          "controlled": 0.30,
          "uncontrolled": 0.50,
          "with_complications": 0.20
        }
      },
      "comorbidities": [
        {"code": "I10", "description": "Essential hypertension", "prevalence": 0.75},
        {"code": "E78", "description": "Hyperlipidemia", "prevalence": 0.70},
        {"code": "N18", "description": "CKD Stage 3+", "prevalence": 0.25},
        {"code": "I50", "description": "Heart failure", "prevalence": 0.15},
        {"code": "E66", "description": "Obesity", "prevalence": 0.40}
      ]
    },
    
    "coverage": {
      "type": "Medicare",
      "plan_distribution": {
        "Medicare Advantage": 0.55,
        "Original Medicare": 0.45
      }
    },
    
    "outputs": {
      "patientsim": {
        "formats": ["fhir_r4", "hl7v2_adt"],
        "include": ["patient", "conditions", "observations", "encounters"]
      },
      "membersim": {
        "formats": ["x12_837", "claims_csv"],
        "include": ["member", "claims", "eligibility"]
      }
    }
  }
}
```

## Specification Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `profile.id` | string | Unique identifier (lowercase, hyphens) |
| `profile.name` | string | Human-readable name |
| `generation.count` | integer | Number of entities (1-10,000) |
| `generation.products` | array | Target products |
| `demographics.age` | object | Age distribution |
| `demographics.gender` | object | Gender distribution |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `demographics.geography` | object | Geographic constraints |
| `clinical.primary_condition` | object | Primary diagnosis |
| `clinical.comorbidities` | array | Additional conditions |
| `coverage` | object | Insurance coverage details |
| `journey` | object | Temporal event sequence |

## Distribution Types

| Type | Use Case | Example |
|------|----------|---------|
| `categorical` | Discrete choices | `{"M": 0.48, "F": 0.52}` |
| `normal` | Bell curve | `{"mean": 72, "std_dev": 8}` |
| `log_normal` | Skewed positive | Healthcare costs |
| `uniform` | Equal probability | `{"min": 0, "max": 30}` |
| `explicit` | Exact values | `["48201", "48113", "48029"]` |

See [distribution-types.md](../distributions/distribution-types.md) for details.

## Using PopulationSim Reference Data

When geography is specified, offer real population data:

```
"I can pull actual demographic data for Texas from PopulationSim:
- Age distribution from ACS census data
- Race/ethnicity breakdown
- Health indicators from CDC PLACES
- Social vulnerability from SVI

Would you like to use real population data as your baseline?"
```

Reference-based profile:
```json
{
  "demographics": {
    "source": "populationsim",
    "reference": {
      "geography": {"type": "state", "code": "TX"},
      "datasets": ["acs_demographics", "cdc_places", "svi"]
    }
  }
}
```

## Adding a Journey

After profile approval, offer journey addition:

```
"Your population profile is ready. Would you like to add a journey
(timeline of events) for these patients?

Options:
1. No journey - Generate static patient data only
2. Standard journey - Use a pre-built template (e.g., 'diabetic first year')
3. Custom journey - Build a custom event sequence"
```

See [journey-builder.md](journey-builder.md) for journey specification.

## Profile Approval Flow

```
"Here's your complete profile specification:

[Display formatted JSON or summary table]

**Summary:**
- 200 Medicare patients with Type 2 diabetes
- Texas geography with PopulationSim data
- Standard comorbidity patterns
- 55% Medicare Advantage / 45% Original Medicare

Options:
1. **Approve** - Save and/or execute generation
2. **Modify** - Change specific values
3. **Add journey** - Include temporal event sequence
4. **Restart** - Start over with different parameters"
```

## Examples

### Example 1: Simple Profile

```
User: "I need 50 diabetic patients for testing"

Builder Output:
{
  "profile": {
    "id": "diabetic-simple-001",
    "name": "Simple Diabetic Population",
    "generation": {"count": 50, "products": ["patientsim"]},
    "demographics": {
      "age": {"type": "normal", "mean": 55, "std_dev": 15, "min": 18, "max": 85},
      "gender": {"type": "categorical", "weights": {"M": 0.48, "F": 0.52}}
    },
    "clinical": {
      "primary_condition": {"code": "E11", "prevalence": 1.0}
    }
  }
}
```

### Example 2: Geography-Based Profile

```
User: "Match the actual population of Harris County for my simulation"

Builder Output:
{
  "profile": {
    "id": "harris-county-reference-001",
    "name": "Harris County TX Population",
    "generation": {"count": 1000, "products": ["patientsim", "membersim"]},
    "demographics": {
      "source": "populationsim",
      "reference": {
        "geography": {"type": "county", "fips": "48201"},
        "datasets": ["acs_demographics", "cdc_places", "svi"]
      }
    }
  }
}
```

### Example 3: Profile with Journey

```
User: "200 Medicare diabetics with first year of care journey"

Builder Output: [See complete example in journey-builder.md]
```

## Validation Rules

Profiles are validated before execution:

| Rule | Severity | Description |
|------|----------|-------------|
| Required fields present | Error | All mandatory fields must exist |
| Value bounds | Error | Numbers within valid ranges |
| Distribution totals | Error | Weights must sum to 1.0 |
| Code validity | Warning | ICD-10, CPT codes are valid format |
| Cross-field consistency | Error | Age ≥ 65 if Medicare, etc. |

## Related Skills

- **[Quick Generate](quick-generate.md)** - Simple single-entity generation
- **[Journey Builder](journey-builder.md)** - Temporal event sequences
- **[Profile Executor](../executors/profile-executor.md)** - Execute specifications
- **[Distribution Types](../distributions/distribution-types.md)** - Statistical distributions
- **[State Management](../../common/state-management.md)** - Save specifications

---

*Part of the HealthSim Generative Framework*
