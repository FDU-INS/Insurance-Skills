---
name: distribution-types
description: Statistical distribution patterns for realistic healthcare data generation
triggers:
  - distribution
  - probability
  - random
  - weighted
  - bell curve
  - normal distribution
---

# Distribution Types

Statistical distribution patterns for generating realistic healthcare data at scale.

## Overview

Distributions control how values are assigned across a generated population. Choose the right distribution to match real-world healthcare patterns.

## Distribution Types

### Categorical Distribution

Discrete choices with specified probabilities.

```json
{
  "type": "categorical",
  "weights": {
    "M": 0.48,
    "F": 0.52
  }
}
```

**Use Cases:**
- Gender distribution
- Plan type selection (HMO/PPO/HDHP)
- Race/ethnicity categories
- Disease severity levels
- Visit types

**Rules:**
- Weights must sum to 1.0
- All categories must be explicitly listed

### Normal Distribution

Bell curve for continuous values clustered around a mean.

```json
{
  "type": "normal",
  "mean": 72,
  "std_dev": 8,
  "min": 65,
  "max": 95
}
```

**Use Cases:**
- Age distributions
- Lab values (A1c, cholesterol)
- Blood pressure
- BMI

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| mean | Yes | Center of distribution |
| std_dev | Yes | Standard deviation |
| min | No | Lower bound (truncated) |
| max | No | Upper bound (truncated) |

### Log-Normal Distribution

Skewed distribution for values that can't be negative and have a long tail.

```json
{
  "type": "log_normal",
  "mean": 5000,
  "std_dev": 8000,
  "min": 0
}
```

**Use Cases:**
- Healthcare costs
- Length of stay
- Claim amounts
- Wait times

**Characteristics:**
- Right-skewed (long tail toward high values)
- Always positive
- Common in healthcare economics

### Uniform Distribution

Equal probability across a range.

```json
{
  "type": "uniform",
  "min": 1,
  "max": 28
}
```

**Use Cases:**
- Day of month for service dates
- Random selection within a window
- Visit scheduling within allowed range

### Explicit Distribution

Specific values with exact weights.

```json
{
  "type": "explicit",
  "values": [
    {"value": "48201", "weight": 0.40},
    {"value": "48113", "weight": 0.35},
    {"value": "48029", "weight": 0.25}
  ]
}
```

**Use Cases:**
- Specific county FIPS codes
- Predefined provider NPIs
- Exact medication NDCs
- Fixed facility assignments

### Conditional Distribution

Distribution that varies based on other attributes.

```json
{
  "type": "conditional",
  "rules": [
    {
      "if": "severity == 'controlled'",
      "distribution": {"type": "normal", "mean": 6.5, "std_dev": 0.3}
    },
    {
      "if": "severity == 'uncontrolled'",
      "distribution": {"type": "normal", "mean": 8.5, "std_dev": 1.0}
    },
    {
      "if": "severity == 'with_complications'",
      "distribution": {"type": "normal", "mean": 9.2, "std_dev": 1.0}
    }
  ]
}
```

**Use Cases:**
- Lab values based on disease severity
- Costs based on comorbidity count
- Visit frequency based on risk tier
- eGFR based on CKD stage

## Common Healthcare Distributions

### Age Distributions

| Population | Distribution | Parameters |
|------------|--------------|------------|
| Medicare | Normal | mean: 72, std_dev: 8, min: 65 |
| Commercial Adults | Normal | mean: 42, std_dev: 12, min: 18, max: 64 |
| Medicaid Adults | Normal | mean: 35, std_dev: 10, min: 18, max: 64 |
| Pediatric | Uniform | min: 0, max: 17 |

### Cost Distributions

| Cost Type | Distribution | Typical Parameters |
|-----------|--------------|-------------------|
| Office Visit | Log-Normal | mean: 150, std_dev: 50 |
| ER Visit | Log-Normal | mean: 1500, std_dev: 2000 |
| Inpatient Stay | Log-Normal | mean: 15000, std_dev: 25000 |
| Generic Rx | Log-Normal | mean: 25, std_dev: 30 |
| Specialty Rx | Log-Normal | mean: 5000, std_dev: 10000 |

### Lab Value Distributions

| Lab Test | Distribution | Normal Range |
|----------|--------------|--------------|
| A1c (diabetic) | Conditional | Based on control |
| eGFR | Conditional | Based on CKD stage |
| LDL Cholesterol | Normal | mean: 130, std_dev: 40 |
| Blood Pressure Systolic | Normal | mean: 130, std_dev: 15 |

## Validation Rules

| Rule | Description |
|------|-------------|
| Weights sum to 1.0 | Categorical weights must total exactly 1.0 |
| Min < Max | Range bounds must be valid |
| Positive std_dev | Standard deviation must be > 0 |
| Valid conditions | Conditional rules must reference valid fields |

## Examples

### Example 1: Medicare Age Distribution

```json
{
  "age": {
    "type": "normal",
    "mean": 72,
    "std_dev": 8,
    "min": 65,
    "max": 95
  }
}
```

### Example 2: Diabetes Severity with Lab Correlation

```json
{
  "severity": {
    "type": "categorical",
    "weights": {
      "controlled": 0.30,
      "uncontrolled": 0.50,
      "with_complications": 0.20
    }
  },
  "a1c": {
    "type": "conditional",
    "rules": [
      {"if": "severity == 'controlled'", "distribution": {"type": "normal", "mean": 6.5, "std_dev": 0.3, "max": 7.0}},
      {"if": "severity == 'uncontrolled'", "distribution": {"type": "normal", "mean": 8.5, "std_dev": 1.0, "min": 7.0}},
      {"if": "severity == 'with_complications'", "distribution": {"type": "normal", "mean": 9.2, "std_dev": 1.0, "min": 8.0}}
    ]
  }
}
```

### Example 3: Plan Type by Market

```json
{
  "plan_type": {
    "type": "categorical",
    "weights": {
      "HMO": 0.35,
      "PPO": 0.45,
      "HDHP": 0.15,
      "POS": 0.05
    }
  }
}
```

### Example 4: Geographic Distribution

```json
{
  "county_fips": {
    "type": "explicit",
    "values": [
      {"value": "06037", "weight": 0.40, "note": "Los Angeles"},
      {"value": "06073", "weight": 0.30, "note": "San Diego"},
      {"value": "06059", "weight": 0.20, "note": "Orange"},
      {"value": "06065", "weight": 0.10, "note": "Riverside"}
    ]
  }
}
```

## Related Skills

- **[Profile Builder](../builders/profile-builder.md)** - Build profile specifications
- **[Age Distributions](age-distributions.md)** - Age-specific patterns
- **[Cost Distributions](cost-distributions.md)** - Cost modeling
- **[PopulationSim](../../populationsim/SKILL.md)** - Real demographic data

---

*Part of the HealthSim Generative Framework*
