---
name: profile-executor
description: Execute profile specifications to generate healthcare data at scale
triggers:
  - execute profile
  - run profile
  - generate from profile
  - batch generate
---

# Profile Executor Skill

Execute approved profile specifications to generate healthcare data deterministically.

## Overview

The Profile Executor is the **execution phase** of the two-phase architecture. It takes an approved ProfileSpecification and generates data following the exact parameters defined.

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROFILE EXECUTION FLOW                       │
└─────────────────────────────────────────────────────────────────┘

    ProfileSpec          Executor           Generated Data
    ┌─────────┐         ┌─────────┐        ┌─────────────┐
    │  JSON   │ ──────► │ Execute │ ─────► │  Entities   │
    │  Spec   │         │         │        │  + Claims   │
    └─────────┘         └─────────┘        │  + Labs     │
                             │              └─────────────┘
                             │
                             ▼
                     ┌─────────────┐
                     │  Validate   │
                     │  & Report   │
                     └─────────────┘
```

## Execution Commands

### Execute Immediately

```
User: "Execute this profile"

Claude: "Executing profile 'medicare-diabetic-texas-001'...

Progress:
- Generating 200 patients... ████████████ 100%
- Creating conditions... ████████████ 100%
- Generating claims... ████████████ 100%
- Linking cross-product... ████████████ 100%

✓ Generated 200 patients with 842 encounters, 1,680 claims

Validation:
✓ Age distribution: mean 71.8 (target: 72 ±5%)
✓ Gender ratio: 47/53 M/F (target: 48/52)
✓ Diabetes prevalence: 100%
✓ HTN comorbidity: 74% (target: 75%)

Save as cohort? (suggested name: 'medicare-diabetic-texas-001')"
```

### Execute with Options

```json
{
  "execution": {
    "profile_id": "medicare-diabetic-texas-001",
    "options": {
      "save_cohort": true,
      "cohort_name": "ma-diabetic-cohort-jan2025",
      "formats": ["fhir_r4", "x12_837"],
      "validation": "strict",
      "dry_run": false
    }
  }
}
```

## Execution Rules

### 1. Distribution Sampling

For each entity, sample from distributions:

```python
# Categorical sampling
gender = sample_categorical({"M": 0.48, "F": 0.52})

# Normal sampling (truncated)
age = sample_normal(mean=72, std=8, min=65, max=95)

# Conditional sampling
if severity == "controlled":
    a1c = sample_normal(mean=6.5, std=0.3, max=7.0)
```

### 2. Entity Generation Order

1. **Demographics first** - Age, gender, geography
2. **Clinical attributes** - Conditions, severity
3. **Derived values** - Labs based on conditions
4. **Coverage** - Plan assignment
5. **Cross-product linking** - Member↔Patient correlation

### 3. Cross-Product Consistency

When multiple products are specified:

```
Patient (PatientSim)     Member (MemberSim)
├── MRN: MRN00000001    ├── Member ID: MEM001234
├── SSN: xxx-xx-1234    ├── SSN: xxx-xx-1234  ← Same SSN
├── DOB: 1952-03-18     ├── DOB: 1952-03-18   ← Same DOB
└── Conditions          └── Claims
    └── E11.9               └── DX: E11.9     ← Consistent
```

### 4. Reference Data Integration

When PopulationSim reference is specified, the executor automatically resolves
real-world demographics from CDC PLACES and SVI data.

**Reference Resolution Process:**
1. Detect `demographics.source = "populationsim"` in profile spec
2. Query DuckDB for PLACES/SVI data matching geography
3. Extract age distribution, disease prevalence, socioeconomic data
4. Merge with user-specified overrides (user spec takes precedence)
5. Execute with merged profile

**Example - County Reference:**
```json
{
  "demographics": {
    "source": "populationsim",
    "reference": {"type": "county", "fips": "48201"}
  }
}
```

This resolves Harris County TX demographics:
- Age distribution from SVI (26% under 17, 63% 18-64, 11% 65+)
- Disease prevalence from PLACES (13.2% diabetes, 37.3% obesity)
- Socioeconomic from SVI (25% poverty, 21% uninsured)

**Hybrid Profile - Override Specific Values:**
```json
{
  "demographics": {
    "source": "populationsim",
    "reference": {"type": "county", "fips": "48201"},
    "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65}
  }
}
```

User's age override (Medicare seniors) is used, but gender and other
demographics come from PopulationSim reference data.

**Available Geography Levels:**
| Level | Code Format | Example |
|-------|-------------|---------|
| county | 5-digit FIPS | "48201" (Harris County TX) |
| state | 2-letter abbr | "TX" |

**Data Sources Queried:**
| Source | Data Available |
|--------|----------------|
| CDC PLACES | Disease prevalence (diabetes, obesity, HTN, COPD, etc.) |
| SVI | Age distribution, minority %, poverty %, uninsured % |

## Validation

### Pre-Execution Validation

| Check | Description | Severity |
|-------|-------------|----------|
| Schema valid | JSON matches ProfileSpec schema | Error |
| Required fields | All mandatory fields present | Error |
| Distribution sums | Categorical weights = 1.0 | Error |
| Code validity | ICD-10/CPT codes valid format | Warning |

### Post-Execution Validation

| Check | Description | Tolerance |
|-------|-------------|-----------|
| Distribution match | Generated vs. target distributions | ±5% |
| Required conditions | All entities have required conditions | 100% |
| Cross-product links | All entities linked correctly | 100% |
| Referential integrity | All foreign keys valid | 100% |

## Execution Report

```
═══════════════════════════════════════════════════════════════════
                    PROFILE EXECUTION REPORT
═══════════════════════════════════════════════════════════════════

Profile: medicare-diabetic-texas-001
Executed: 2025-01-15 10:45:32 UTC
Duration: 12.4 seconds

GENERATION SUMMARY
──────────────────────────────────────────────────────────────────
Entities Generated:
  - Patients:     200
  - Members:      200
  - Encounters:   842
  - Claims:       1,680
  - Observations: 2,400
  - Medications:  600

DISTRIBUTION VALIDATION
──────────────────────────────────────────────────────────────────
                    Target      Actual      Status
Age (mean)          72          71.8        ✓ Within tolerance
Age (std)           8           7.9         ✓ Within tolerance
Gender M/F          48/52       47/53       ✓ Within tolerance
Diabetes            100%        100%        ✓ Exact
HTN                 75%         74%         ✓ Within tolerance
Hyperlipidemia      70%         71%         ✓ Within tolerance
CKD                 25%         24%         ✓ Within tolerance
Heart Failure       15%         16%         ✓ Within tolerance

CROSS-PRODUCT LINKAGE
──────────────────────────────────────────────────────────────────
Patient ↔ Member:    200/200 linked (100%)
Encounter → Claim:   842/842 linked (100%)
Rx → Fill:           450/450 linked (100%)

OUTPUT FILES
──────────────────────────────────────────────────────────────────
Cohort saved: ma-diabetic-cohort-jan2025
  - main.patients:     200 rows
  - main.members:      200 rows
  - main.encounters:   842 rows
  - main.claims:       1,680 rows

═══════════════════════════════════════════════════════════════════
```

## Dry Run Mode

Preview generation without persisting:

```
User: "Dry run this profile"

Claude: "Dry run for profile 'medicare-diabetic-texas-001':

Would generate:
- 200 patients matching demographics
- ~800-900 encounters (4-5 per patient avg)
- ~1,600-1,800 claims
- ~2,400 observations

Sample patient:
{
  "mrn": "MRN00000001",
  "age": 74,
  "gender": "F",
  "conditions": ["E11.65", "I10", "E78.5"],
  "a1c": 7.8
}

Proceed with full execution?"
```

## Error Handling

### Validation Errors

```
✗ Execution failed: Validation errors

Errors:
1. Distribution weights for 'plan_type' sum to 1.05 (must be 1.0)
2. Required field 'demographics.age' is missing
3. Invalid ICD-10 code: 'E11.99' (should be E11.9)

Fix these issues and retry.
```

### Partial Failures

```
⚠ Execution completed with warnings

Generated: 198/200 patients (99%)

Warnings:
- 2 patients skipped: Could not assign provider in specified geography
- Retry with broader geography or add providers to NetworkSim

Saved partial results? (y/n)
```

## Related Skills

- **[Profile Builder](../builders/profile-builder.md)** - Build specifications
- **[Journey Executor](journey-executor.md)** - Execute journeys
- **[State Management](../../common/state-management.md)** - Save cohorts
- **[Cross-Domain Sync](cross-domain-sync.md)** - Multi-product coordination

---

*Part of the HealthSim Generative Framework*
