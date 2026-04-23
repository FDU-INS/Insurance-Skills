---
name: age-distributions
description: Age distribution patterns for realistic healthcare population generation
triggers:
  - age distribution
  - age range
  - demographics
  - population age
---

# Age Distributions

Age distribution patterns for generating realistic healthcare populations across different coverage types.

## Overview

Age is the single most important demographic variable in healthcare. It correlates with:
- Disease prevalence
- Healthcare utilization
- Cost patterns
- Coverage eligibility

## Distribution by Coverage Type

### Medicare (Age 65+)

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

**Breakdown:**
| Age Band | Percentage | Characteristics |
|----------|------------|-----------------|
| 65-69 | 25% | Recently enrolled, often healthier |
| 70-74 | 25% | Established Medicare beneficiaries |
| 75-79 | 20% | Increasing chronic conditions |
| 80-84 | 15% | Higher utilization |
| 85+ | 15% | Highest complexity, often dual-eligible |

### Medicare Advantage

Similar to traditional Medicare but may skew slightly younger:

```json
{
  "age": {
    "type": "normal",
    "mean": 71,
    "std_dev": 7,
    "min": 65,
    "max": 95
  }
}
```

### Commercial Adults (18-64)

```json
{
  "age": {
    "type": "normal",
    "mean": 42,
    "std_dev": 12,
    "min": 18,
    "max": 64
  }
}
```

**By Employer Type:**
| Employer | Mean Age | Std Dev | Notes |
|----------|----------|---------|-------|
| Large employer | 42 | 12 | Balanced workforce |
| Tech company | 35 | 8 | Skews younger |
| Manufacturing | 48 | 10 | Skews older |
| Government | 45 | 11 | Stable, older workforce |

### Medicaid Adults

```json
{
  "age": {
    "type": "normal",
    "mean": 35,
    "std_dev": 10,
    "min": 18,
    "max": 64
  }
}
```

**Expansion Population:** Mean age ~38, includes more adults 45-64.

### Pediatric (0-17)

```json
{
  "age": {
    "type": "uniform",
    "min": 0,
    "max": 17
  }
}
```

**Or weighted by healthcare utilization:**

```json
{
  "age": {
    "type": "categorical",
    "weights": {
      "0-1": 0.15,
      "2-5": 0.20,
      "6-11": 0.30,
      "12-17": 0.35
    }
  }
}
```

### Dual Eligible (Medicare + Medicaid)

```json
{
  "age": {
    "type": "normal",
    "mean": 75,
    "std_dev": 9,
    "min": 65,
    "max": 100
  }
}
```

**Note:** Skews older and includes a higher proportion of 85+ individuals.

## Clinical Trial Age Distributions

### Phase 3 Oncology

```json
{
  "age": {
    "type": "normal",
    "mean": 62,
    "std_dev": 10,
    "min": 18,
    "max": 80
  }
}
```

### Phase 3 Cardiovascular

```json
{
  "age": {
    "type": "normal",
    "mean": 65,
    "std_dev": 9,
    "min": 40,
    "max": 85
  }
}
```

### Phase 1 Healthy Volunteers

```json
{
  "age": {
    "type": "uniform",
    "min": 18,
    "max": 55
  }
}
```

## Age Band Distributions

For reporting or stratification by standard age bands:

```json
{
  "age_band": {
    "type": "categorical",
    "weights": {
      "0-17": 0.22,
      "18-34": 0.21,
      "35-49": 0.19,
      "50-64": 0.20,
      "65+": 0.18
    }
  }
}
```

## Age-Correlated Attributes

### Comorbidity Count

```json
{
  "comorbidity_count": {
    "type": "conditional",
    "rules": [
      {"if": "age < 40", "distribution": {"type": "categorical", "weights": {"0": 0.6, "1": 0.3, "2": 0.1}}},
      {"if": "age >= 40 && age < 65", "distribution": {"type": "categorical", "weights": {"0": 0.3, "1": 0.35, "2": 0.25, "3+": 0.1}}},
      {"if": "age >= 65", "distribution": {"type": "categorical", "weights": {"0": 0.1, "1": 0.2, "2": 0.3, "3+": 0.4}}}
    ]
  }
}
```

### Healthcare Utilization

```json
{
  "annual_visits": {
    "type": "conditional",
    "rules": [
      {"if": "age < 18", "distribution": {"type": "normal", "mean": 4, "std_dev": 2, "min": 0}},
      {"if": "age >= 18 && age < 65", "distribution": {"type": "normal", "mean": 3, "std_dev": 2, "min": 0}},
      {"if": "age >= 65", "distribution": {"type": "normal", "mean": 8, "std_dev": 4, "min": 0}}
    ]
  }
}
```

## Examples

### Example 1: Medicare Advantage Population

```json
{
  "profile_id": "ma-population",
  "demographics": {
    "age": {
      "type": "normal",
      "mean": 71,
      "std_dev": 7,
      "min": 65,
      "max": 95
    },
    "gender": {
      "type": "categorical",
      "weights": {"M": 0.44, "F": 0.56}
    }
  }
}
```

### Example 2: Commercial Family Coverage

```json
{
  "profile_id": "commercial-family",
  "demographics": {
    "member_type": {
      "type": "categorical",
      "weights": {
        "subscriber": 0.35,
        "spouse": 0.25,
        "dependent": 0.40
      }
    },
    "age": {
      "type": "conditional",
      "rules": [
        {"if": "member_type == 'subscriber'", "distribution": {"type": "normal", "mean": 42, "std_dev": 10, "min": 18, "max": 64}},
        {"if": "member_type == 'spouse'", "distribution": {"type": "normal", "mean": 40, "std_dev": 10, "min": 18, "max": 64}},
        {"if": "member_type == 'dependent'", "distribution": {"type": "uniform", "min": 0, "max": 25}}
      ]
    }
  }
}
```

## Related Skills

- **[Distribution Types](distribution-types.md)** - All distribution patterns
- **[Cost Distributions](cost-distributions.md)** - Healthcare cost modeling
- **[Profile Builder](../builders/profile-builder.md)** - Build complete profiles
- **[PopulationSim](../../populationsim/SKILL.md)** - Real demographic data

---

*Part of the HealthSim Generative Framework*
