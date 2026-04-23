# Distributions

Statistical distribution patterns for realistic healthcare data generation.

## Overview

Distributions define how values are sampled during generation. Instead of hardcoded values, they enable realistic variability that matches real-world healthcare patterns.

## Skills in This Category

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| [distribution-types.md](distribution-types.md) | Core distribution patterns | Defining any variable attribute |

## Distribution Types

| Type | Use Case | Example |
|------|----------|---------|
| **Categorical** | Discrete choices | Gender (M/F), Plan Type (HMO/PPO) |
| **Normal** | Bell curve values | Age, Lab values, BMI |
| **Log-Normal** | Skewed positive values | Healthcare costs, Length of stay |
| **Uniform** | Equal probability | Day of month, Random selection |
| **Explicit** | Specific known values | County FIPS codes, Provider NPIs |
| **Conditional** | Value depends on other attributes | A1c by diabetes severity |

## Quick Reference

### Categorical
```json
{
  "type": "categorical",
  "weights": {"M": 0.48, "F": 0.52}
}
```

### Normal
```json
{
  "type": "normal",
  "mean": 72,
  "std_dev": 8,
  "min": 65,
  "max": 95
}
```

### Log-Normal
```json
{
  "type": "log_normal",
  "mean": 150,
  "std_dev": 75,
  "min": 50
}
```

### Conditional
```json
{
  "type": "conditional",
  "rules": [
    {"if": "severity == 'controlled'", "distribution": {"type": "normal", "mean": 6.5, "std_dev": 0.3}},
    {"if": "severity == 'uncontrolled'", "distribution": {"type": "normal", "mean": 9.0, "std_dev": 1.0}}
  ]
}
```

## Common Healthcare Distributions

### Age by Population

| Population | Distribution |
|------------|--------------|
| Medicare | Normal(72, 8) min=65 |
| Commercial | Normal(42, 12) min=18, max=64 |
| Medicaid Adult | Normal(38, 12) min=18 |
| Pediatric | Categorical by age bands |

### Healthcare Costs

| Service | Distribution |
|---------|--------------|
| Office Visit | LogNormal(μ=150, σ=75) |
| ER Visit | LogNormal(μ=1500, σ=800) |
| Inpatient Stay | LogNormal(μ=15000, σ=8000) |
| Pharmacy Fill | LogNormal(μ=50, σ=200) |

## Related Categories

- [Builders](../builders/) - Use distributions in profiles
- [Templates](../templates/) - Pre-configured distributions

---

*Part of the HealthSim Generative Framework*
