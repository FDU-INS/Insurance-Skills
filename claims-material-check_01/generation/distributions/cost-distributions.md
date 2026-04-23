---
name: cost-distributions
description: Healthcare cost distribution patterns for realistic claims and financial data generation
triggers:
  - cost distribution
  - claim amount
  - healthcare costs
  - allowed amount
  - billed amount
---

# Cost Distributions

Healthcare cost distribution patterns for generating realistic claims and financial data.

## Overview

Healthcare costs follow specific patterns that differ dramatically by:
- Service type (office visit vs surgery vs Rx)
- Setting (inpatient vs outpatient vs home)
- Population (commercial vs Medicare vs Medicaid)
- Disease complexity

Most healthcare costs are **right-skewed** with a long tail of high-cost cases.

## Distribution Characteristics

### Log-Normal Distribution

Most healthcare costs follow a log-normal pattern:
- Most claims cluster at lower values
- Long right tail (high-cost outliers)
- Always positive (no negative costs)

```json
{
  "cost": {
    "type": "log_normal",
    "mean": 150,
    "std_dev": 200,
    "min": 0
  }
}
```

### The 80/20 Rule

In healthcare: ~20% of patients account for ~80% of costs.

```json
{
  "cost_tier": {
    "type": "categorical",
    "weights": {
      "low": 0.60,
      "medium": 0.25,
      "high": 0.12,
      "catastrophic": 0.03
    }
  }
}
```

## Cost Distributions by Service Type

### Professional Claims

| Service | Mean | Std Dev | Range |
|---------|------|---------|-------|
| Office Visit (New) | $175 | $50 | $100-$400 |
| Office Visit (Est) | $125 | $40 | $75-$300 |
| Specialist Visit | $250 | $100 | $150-$600 |
| Telehealth | $85 | $25 | $50-$150 |

```json
{
  "office_visit_cost": {
    "type": "log_normal",
    "mean": 125,
    "std_dev": 75,
    "min": 50,
    "max": 500
  }
}
```

### Facility Claims

| Service | Mean | Std Dev | Range |
|---------|------|---------|-------|
| ER Visit | $1,500 | $2,000 | $300-$15,000 |
| Observation | $3,500 | $2,500 | $1,000-$15,000 |
| Inpatient (medical) | $12,000 | $15,000 | $3,000-$100,000 |
| Inpatient (surgical) | $25,000 | $30,000 | $5,000-$200,000 |
| Outpatient Surgery | $5,000 | $6,000 | $1,000-$40,000 |

```json
{
  "er_visit_cost": {
    "type": "log_normal",
    "mean": 1500,
    "std_dev": 2000,
    "min": 300,
    "max": 20000
  }
}
```

### Inpatient by DRG Complexity

```json
{
  "inpatient_cost": {
    "type": "conditional",
    "rules": [
      {"if": "drg_weight < 1.0", "distribution": {"type": "log_normal", "mean": 8000, "std_dev": 4000}},
      {"if": "drg_weight >= 1.0 && drg_weight < 2.0", "distribution": {"type": "log_normal", "mean": 15000, "std_dev": 8000}},
      {"if": "drg_weight >= 2.0 && drg_weight < 4.0", "distribution": {"type": "log_normal", "mean": 30000, "std_dev": 20000}},
      {"if": "drg_weight >= 4.0", "distribution": {"type": "log_normal", "mean": 75000, "std_dev": 50000}}
    ]
  }
}
```

### Pharmacy Claims

| Drug Type | Mean | Std Dev | Range |
|-----------|------|---------|-------|
| Generic | $25 | $30 | $4-$150 |
| Preferred Brand | $150 | $100 | $30-$500 |
| Non-Preferred Brand | $300 | $200 | $75-$1,000 |
| Specialty | $5,000 | $8,000 | $500-$50,000 |
| Gene Therapy | $500,000 | $300,000 | $100K-$2M |

```json
{
  "rx_cost": {
    "type": "conditional",
    "rules": [
      {"if": "tier == 'generic'", "distribution": {"type": "log_normal", "mean": 25, "std_dev": 30}},
      {"if": "tier == 'preferred'", "distribution": {"type": "log_normal", "mean": 150, "std_dev": 100}},
      {"if": "tier == 'non_preferred'", "distribution": {"type": "log_normal", "mean": 300, "std_dev": 200}},
      {"if": "tier == 'specialty'", "distribution": {"type": "log_normal", "mean": 5000, "std_dev": 8000}}
    ]
  }
}
```

## Cost Components

### Claim Adjudication

```json
{
  "billed_amount": {
    "type": "log_normal",
    "mean": 500,
    "std_dev": 400
  },
  "allowed_amount": {
    "type": "derived",
    "formula": "billed_amount * allowed_ratio",
    "allowed_ratio": {"type": "uniform", "min": 0.4, "max": 0.8}
  },
  "plan_paid": {
    "type": "derived",
    "formula": "allowed_amount - member_responsibility"
  },
  "member_responsibility": {
    "type": "derived",
    "formula": "copay + coinsurance + deductible_applied"
  }
}
```

### Member Cost Sharing

| Component | Commercial | Medicare | Medicaid |
|-----------|------------|----------|----------|
| PCP Copay | $20-30 | $0-20 | $0-5 |
| Specialist Copay | $40-60 | $20-40 | $0-5 |
| ER Copay | $100-250 | $50-100 | $0-10 |
| Rx Generic Copay | $5-15 | $0-10 | $0-3 |
| Inpatient Coinsurance | 10-20% | 0-20% | 0% |

## Distributions by Population

### Commercial Large Group

```json
{
  "annual_total_cost": {
    "type": "log_normal",
    "mean": 5500,
    "std_dev": 12000,
    "min": 0
  }
}
```

### Medicare Advantage

```json
{
  "annual_total_cost": {
    "type": "log_normal",
    "mean": 12000,
    "std_dev": 20000,
    "min": 0
  }
}
```

### Medicaid

```json
{
  "annual_total_cost": {
    "type": "log_normal",
    "mean": 4500,
    "std_dev": 15000,
    "min": 0
  }
}
```

## Condition-Specific Costs

### Diabetes (Annual)

```json
{
  "diabetes_annual_cost": {
    "type": "conditional",
    "rules": [
      {"if": "severity == 'controlled'", "distribution": {"type": "log_normal", "mean": 8000, "std_dev": 4000}},
      {"if": "severity == 'uncontrolled'", "distribution": {"type": "log_normal", "mean": 15000, "std_dev": 10000}},
      {"if": "severity == 'with_complications'", "distribution": {"type": "log_normal", "mean": 35000, "std_dev": 25000}}
    ]
  }
}
```

### Heart Failure (Annual)

```json
{
  "hf_annual_cost": {
    "type": "conditional",
    "rules": [
      {"if": "nyha_class == 'I'", "distribution": {"type": "log_normal", "mean": 10000, "std_dev": 5000}},
      {"if": "nyha_class == 'II'", "distribution": {"type": "log_normal", "mean": 18000, "std_dev": 10000}},
      {"if": "nyha_class == 'III'", "distribution": {"type": "log_normal", "mean": 35000, "std_dev": 20000}},
      {"if": "nyha_class == 'IV'", "distribution": {"type": "log_normal", "mean": 75000, "std_dev": 40000}}
    ]
  }
}
```

### Oncology Treatment Cycle

```json
{
  "chemo_cycle_cost": {
    "type": "log_normal",
    "mean": 15000,
    "std_dev": 20000,
    "min": 2000,
    "max": 100000
  }
}
```

## Seasonal and Temporal Patterns

### Monthly Utilization Adjustment

```json
{
  "monthly_adjustment": {
    "type": "categorical",
    "weights": {
      "jan": 1.15,
      "feb": 1.10,
      "mar": 1.05,
      "apr": 0.95,
      "may": 0.90,
      "jun": 0.85,
      "jul": 0.85,
      "aug": 0.90,
      "sep": 0.95,
      "oct": 1.00,
      "nov": 1.05,
      "dec": 1.25
    }
  }
}
```

**Note:** December spike is due to deductible/out-of-pocket max satisfaction.

## Examples

### Example 1: Commercial Professional Claim

```json
{
  "claim_type": "professional",
  "service_date": "2025-01-15",
  "cpt": "99213",
  "billed_amount": {"type": "log_normal", "mean": 150, "std_dev": 50},
  "allowed_pct": {"type": "uniform", "min": 0.50, "max": 0.75},
  "copay": 25
}
```

### Example 2: Medicare Inpatient Stay

```json
{
  "claim_type": "institutional",
  "admit_date": "2025-01-10",
  "discharge_date": "2025-01-14",
  "drg": "470",
  "drg_weight": 1.9,
  "billed_amount": {"type": "log_normal", "mean": 45000, "std_dev": 15000},
  "medicare_payment": {"type": "derived", "formula": "drg_weight * base_rate"},
  "base_rate": 7500
}
```

### Example 3: Specialty Pharmacy Fill

```json
{
  "claim_type": "pharmacy",
  "fill_date": "2025-01-20",
  "drug_tier": "specialty",
  "days_supply": 30,
  "ingredient_cost": {"type": "log_normal", "mean": 8000, "std_dev": 5000},
  "dispensing_fee": 15,
  "copay": {"type": "categorical", "weights": {"$100": 0.3, "$200": 0.4, "$500": 0.2, "20%": 0.1}}
}
```

## Related Skills

- **[Distribution Types](distribution-types.md)** - All distribution patterns
- **[Age Distributions](age-distributions.md)** - Demographics
- **[Profile Builder](../builders/profile-builder.md)** - Build complete profiles
- **[MemberSim](../../membersim/SKILL.md)** - Claims generation

---

*Part of the HealthSim Generative Framework*
