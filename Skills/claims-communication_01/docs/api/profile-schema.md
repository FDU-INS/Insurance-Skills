# Profile Schema Reference

This document describes the `ProfileSpecification` schema used to define population characteristics for data generation.

## Overview

A profile specification defines **what** to generate - the demographic, clinical, and coverage characteristics of a synthetic population. Profiles are JSON-serializable and can be persisted using the `ProfileManager`.

## Core Schema

```python
from healthsim.generation.profiles import ProfileSpecification

ProfileSpecification(
    name: str,                    # Unique identifier
    description: str = None,      # Human-readable description
    demographics: DemographicsSpec = None,
    clinical: ClinicalSpec = None,
    coverage: CoverageSpec = None,
    product_config: dict = None,  # Product-specific settings
    metadata: dict = None         # Custom metadata
)
```

## DemographicsSpec

Defines population demographics with support for distributions and geographic targeting.

```python
DemographicsSpec(
    count: int,                           # Number of entities to generate
    age: AgeSpec = None,                  # Age distribution
    gender: GenderSpec = None,            # Gender distribution
    geography: GeographySpec = None,      # Geographic distribution
    seed: int = None                      # Reproducibility seed
)
```

### AgeSpec

```python
AgeSpec(
    distribution: str = "normal",    # normal, uniform, categorical
    min: int = 0,
    max: int = 100,
    mean: float = None,              # For normal distribution
    std: float = None,               # For normal distribution
    categories: dict = None          # For categorical: {"18-35": 0.3, "36-55": 0.4, ...}
)
```

### GenderSpec

```python
GenderSpec(
    distribution: str = "categorical",
    categories: dict = {"M": 0.49, "F": 0.51}
)
```

### GeographySpec

```python
GeographySpec(
    state: str = None,               # Filter by state (e.g., "CA")
    county: str = None,              # Filter by county FIPS
    zip_code: str = None,            # Filter by ZIP code
    use_reference: bool = True       # Use PopulationSim reference data
)
```

## ClinicalSpec

Defines clinical characteristics including conditions and utilization patterns.

```python
ClinicalSpec(
    conditions: List[ConditionSpec] = None,
    utilization: UtilizationSpec = None,
    risk_profile: str = None         # "low", "moderate", "high", "complex"
)
```

### ConditionSpec

```python
ConditionSpec(
    code: str,                       # ICD-10 code (e.g., "E11.9")
    code_system: str = "ICD10",      # ICD10, SNOMED
    prevalence: float = 1.0,         # 0.0 to 1.0 - proportion with condition
    onset: OnsetSpec = None,         # When condition appears
    severity: str = None             # "mild", "moderate", "severe"
)
```

### UtilizationSpec

```python
UtilizationSpec(
    encounters_per_year: Distribution = None,
    inpatient_probability: float = 0.1,
    ed_probability: float = 0.2
)
```

## CoverageSpec

Defines insurance coverage characteristics (MemberSim, RxMemberSim).

```python
CoverageSpec(
    plan_type: str = None,           # "HMO", "PPO", "HDHP"
    lob: str = None,                 # "commercial", "medicare", "medicaid"
    effective_date: date = None,
    term_date: date = None,
    pharmacy_benefit: PharmacyBenefitSpec = None
)
```

## Distribution Types

Profiles support several distribution types for numeric values:

| Type | Parameters | Example |
|------|------------|---------|
| `normal` | mean, std | Age distribution |
| `uniform` | min, max | Random range |
| `lognormal` | mu, sigma | Cost distribution |
| `categorical` | categories (dict) | Gender, plan type |
| `constant` | value | Fixed value |

```python
Distribution(
    type: str,           # Distribution type
    params: dict         # Type-specific parameters
)
```

## Complete Example

```python
from healthsim.generation.profiles import (
    ProfileSpecification, DemographicsSpec, ClinicalSpec,
    AgeSpec, GenderSpec, ConditionSpec
)

profile = ProfileSpecification(
    name="medicare-diabetic-cohort",
    description="Medicare beneficiaries with Type 2 diabetes",
    demographics=DemographicsSpec(
        count=1000,
        age=AgeSpec(
            distribution="normal",
            min=65, max=95,
            mean=75, std=8
        ),
        gender=GenderSpec(
            categories={"M": 0.45, "F": 0.55}
        )
    ),
    clinical=ClinicalSpec(
        conditions=[
            ConditionSpec(
                code="E11.9",
                code_system="ICD10",
                prevalence=1.0  # All members have diabetes
            ),
            ConditionSpec(
                code="I10",
                prevalence=0.7  # 70% comorbid hypertension
            )
        ],
        risk_profile="high"
    ),
    metadata={
        "created_by": "demo",
        "use_case": "care management analytics"
    }
)
```

## Validation

Profiles are validated on creation:

```python
from healthsim.generation.profiles import ProfileValidator

validator = ProfileValidator()
result = validator.validate(profile)

if not result.is_valid:
    for error in result.errors:
        print(f"Error: {error}")
```

## Persistence

See [Profile Persistence Guide](../guides/profile-persistence.md) for saving and loading profiles.

## See Also

- [Generative Framework Guide](../guides/generative-framework.md) - Overview of generation system
- [Profile Persistence](../guides/profile-persistence.md) - Save and reuse profiles
- [Generation API](generation.md) - Full API reference
