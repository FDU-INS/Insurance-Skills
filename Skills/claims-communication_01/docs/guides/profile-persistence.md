# Profile Persistence Guide

This guide covers saving, loading, and managing profile specifications using the `ProfileManager`.

## Overview

Profiles define **what** to generate - the demographic, clinical, and coverage characteristics of a synthetic population. The `ProfileManager` allows you to:

- Save profiles for reuse across sessions
- Track execution history for each profile
- Version profiles as they evolve
- Search and filter your profile library

## Quick Start

### Save a Profile

```python
from healthsim.state import StateManager
from healthsim.generation.profiles import ProfileSpecification, DemographicsSpec

# Create profile
profile = ProfileSpecification(
    name="medicare-diabetic",
    description="Medicare beneficiaries with Type 2 diabetes",
    demographics=DemographicsSpec(count=1000)
)

# Save it
manager = StateManager()
manager.profiles.save_profile(
    name="medicare-diabetic",
    profile_spec=profile,
    description="Standard Medicare diabetes cohort",
    products=["patientsim", "membersim"],
    tags=["medicare", "diabetes", "chronic"]
)
```

### Load a Profile

```python
# Load by name
record = manager.profiles.load_profile("medicare-diabetic")
profile_spec = record.profile_spec

# Use for generation
from healthsim import generate
result = generate(profile=profile_spec, products=["patientsim"])
```

### Record Execution

```python
# After generating a cohort, record the execution
manager.profiles.record_execution(
    profile_id=record.id,
    cohort_id=cohort_id,
    entity_count=1000,
    seed=42,
    duration_ms=1500
)
```

## Profile Management

### List Profiles

```python
# List all profiles
for summary in manager.profiles.list_profiles():
    print(f"{summary.name}: {summary.description}")
    print(f"  Products: {summary.products}")
    print(f"  Executions: {summary.execution_count}")

# Filter by product
membersim_profiles = manager.profiles.list_profiles(product="membersim")

# Filter by tags
diabetes_profiles = manager.profiles.list_profiles(tags=["diabetes"])

# Search by name/description
matching = manager.profiles.list_profiles(search="medicare")
```

### Update a Profile

```python
# Update with new spec (version increments automatically)
updated_spec = ProfileSpecification(
    name="medicare-diabetic",
    demographics=DemographicsSpec(count=2000)  # Increased count
)

manager.profiles.update_profile(
    name="medicare-diabetic",
    profile_spec=updated_spec
)

# Check version
record = manager.profiles.load_profile("medicare-diabetic")
print(f"Version: {record.version}")  # Version: 2
```

### Delete a Profile

```python
# Delete profile (keeps execution history by default)
manager.profiles.delete_profile("medicare-diabetic")

# Delete with execution history
manager.profiles.delete_profile("medicare-diabetic", delete_executions=True)
```

## Execution History

Track every time a profile is used:

```python
# Get execution history for a profile
executions = manager.profiles.get_executions(profile_id=record.id)

for exec in executions:
    print(f"Executed: {exec.executed_at}")
    print(f"  Cohort: {exec.cohort_id}")
    print(f"  Entities: {exec.entity_count}")
    print(f"  Seed: {exec.seed}")
    print(f"  Duration: {exec.duration_ms}ms")
```

### Link Cohorts to Profiles

```python
# Find which profile created a cohort
profile_record = manager.profiles.get_cohort_profile(cohort_id)
if profile_record:
    print(f"Cohort created from: {profile_record.name}")
```

### Re-execute with Same Seed

```python
# Get the exact spec and seed used for a cohort
exec_spec = manager.profiles.get_execution_spec(cohort_id)

# Re-run with identical parameters
from healthsim import generate
result = generate(
    profile=exec_spec["profile_spec"],
    products=exec_spec["products"],
    seed=exec_spec["seed"]
)
```

## Comparison: Profiles vs Journeys

| Aspect | Profile | Journey |
|--------|---------|---------|
| **Purpose** | WHAT to generate | HOW it evolves over TIME |
| **Contains** | Demographics, conditions, coverage | Event sequences, phases, timing |
| **Execution** | Per-cohort (batch) | Per-entity (individual) |
| **Manager** | `ProfileManager` | `JourneyManager` |
| **Tables** | `profiles`, `profile_executions` | `journeys`, `journey_executions` |

They work together:
1. **Profile** creates the cohort (1000 patients)
2. **Journey** creates each patient's timeline (encounters, claims, etc.)

## Data Model

### ProfileRecord

Full profile with specification:

```python
ProfileRecord(
    id: int,
    name: str,
    description: str,
    version: int,
    profile_spec: ProfileSpecification,
    products: List[str],
    tags: List[str],
    created_at: datetime,
    updated_at: datetime,
    metadata: dict
)
```

### ProfileSummary

Brief info for listing:

```python
ProfileSummary(
    id: int,
    name: str,
    description: str,
    version: int,
    products: List[str],
    tags: List[str],
    entity_count: int,          # From profile_spec
    execution_count: int,       # How many times executed
    last_executed: datetime,    # Most recent execution
    created_at: datetime,
    updated_at: datetime
)
```

### ProfileExecutionRecord

Execution history entry:

```python
ProfileExecutionRecord(
    id: int,
    profile_id: int,
    cohort_id: str,
    entity_count: int,
    seed: int,
    executed_at: datetime,
    status: str,              # "success", "failed", "partial"
    error_message: str,
    duration_ms: int,
    metadata: dict
)
```

## Best Practices

1. **Use descriptive names** - Make profiles easy to find
   ```python
   # Good: "commercial-hdhp-young-healthy"
   # Bad: "profile1"
   ```

2. **Tag consistently** - Use standard tags across profiles
   ```python
   tags=["commercial", "hdhp", "low-risk"]
   ```

3. **Track products** - Record which products the profile targets
   ```python
   products=["membersim", "rxmembersim"]
   ```

4. **Record all executions** - Build history for reproducibility
   ```python
   manager.profiles.record_execution(profile_id, cohort_id, ...)
   ```

5. **Version intentionally** - Updates auto-increment version
   ```python
   # Major changes: update_profile() bumps version
   # Minor metadata: use update_profile(..., bump_version=False)
   ```

## Database Schema

Profiles are stored in two tables:

**profiles**
- `id`, `name` (unique), `description`, `version`
- `profile_spec` (JSON) - Full ProfileSpecification
- `products`, `tags` (JSON arrays)
- `entity_count` (derived from spec)
- `created_at`, `updated_at`, `metadata`

**profile_executions**
- `id`, `profile_id` (FK)
- `cohort_id`, `entity_count`, `seed`
- `executed_at`, `status`, `error_message`
- `duration_ms`, `metadata`

## See Also

- [Journey Persistence](journey-persistence.md) - Persist temporal event sequences
- [Generative Framework](generative-framework.md) - Overview of generation system
- [Profile Schema](../api/profile-schema.md) - Specification format details
