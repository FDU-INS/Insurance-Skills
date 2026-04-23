# Journey Persistence Guide

The HealthSim Journey Manager provides persistence for journey specifications - the temporal event sequences that define how healthcare events unfold over time. This guide covers saving, loading, versioning, and tracking journey executions.

## Overview

Journeys are "recipes" for generating healthcare timelines. Like profiles (which define *what* to generate), journeys define *how* entities progress through healthcare events over time.

| Concept | Purpose | Example |
|---------|---------|---------|
| **Profile** | What entities to generate | 100 diabetic patients, age 65+, in Texas |
| **Journey** | How events unfold over time | Quarterly visits, labs, annual screenings |

## Quick Start

### Saving a Journey

```python
from healthsim.state import get_manager

manager = get_manager()

# Define a journey specification
journey_spec = {
    "journey_id": "diabetic-first-year",
    "name": "First Year Diabetes Management",
    "duration_days": 365,
    "products": ["patientsim"],
    "events": [
        {
            "event_id": "quarterly-visit",
            "name": "Quarterly PCP Visit",
            "event_type": "encounter",
            "delay": {"min_days": 90, "max_days": 90}
        },
        {
            "event_id": "hba1c-lab",
            "name": "HbA1c Lab Order",
            "event_type": "lab_order",
            "delay": {"min_days": 90, "max_days": 90}
        },
        {
            "event_id": "annual-eye-exam",
            "name": "Annual Ophthalmology Visit",
            "event_type": "encounter",
            "delay": {"min_days": 60, "max_days": 60}
        }
    ]
}

# Save the journey
journey_id = manager.journeys.save_journey(
    name="diabetic-first-year",
    journey_spec=journey_spec,
    description="Quarterly visits with labs for new diabetics",
    tags=["diabetes", "chronic-care", "primary-care"]
)

print(f"Saved journey: {journey_id}")
```

### Loading and Using a Journey

```python
# Load by name
journey = manager.journeys.load_journey("diabetic-first-year")

# Access the specification
print(f"Duration: {journey.duration_days} days")
print(f"Events: {journey.event_count}")
print(f"Version: {journey.version}")

# Use with JourneyEngine
from healthsim.generation import JourneyEngine, JourneySpecification

engine = JourneyEngine()
spec = JourneySpecification.from_dict(journey.journey_spec)
timeline = engine.create_timeline(spec, patient, start_date)
```

### Recording Executions

```python
import time

start = time.time()
events = engine.execute_timeline(timeline)
duration_ms = int((time.time() - start) * 1000)

# Record the execution
manager.journeys.record_execution(
    journey_id=journey.id,
    entity_id=patient.id,
    start_date=start_date,
    end_date=start_date + timedelta(days=365),
    events_generated=len(events),
    duration_ms=duration_ms
)
```

## Journey Management

### Listing Journeys

```python
# List all journeys
all_journeys = manager.journeys.list_journeys()

# Filter by product
patient_journeys = manager.journeys.list_journeys(products=["patientsim"])

# Filter by tags
diabetes_journeys = manager.journeys.list_journeys(tags=["diabetes"])

# Search by name/description
cardiac_journeys = manager.journeys.list_journeys(search="cardiac")

# Each result is a JourneySummary with execution stats
for j in all_journeys:
    print(f"{j.name}: {j.event_count} events, executed {j.execution_count} times")
```

### Updating Journeys

```python
# Update specification (bumps version)
updated = manager.journeys.update_journey(
    "diabetic-first-year",
    journey_spec=new_spec
)
print(f"Now at version {updated.version}")

# Update metadata only
manager.journeys.update_journey(
    "diabetic-first-year",
    description="Updated description",
    tags=["diabetes", "hedis"],
    bump_version=False  # Don't increment version for metadata-only changes
)
```

### Deleting Journeys

```python
# Delete journey and execution history
manager.journeys.delete_journey("old-journey")

# Delete journey but keep execution history
manager.journeys.delete_journey("old-journey", delete_executions=False)
```

## Execution History

### Tracking Executions

```python
# Record successful execution
exec_id = manager.journeys.record_execution(
    journey_id=journey.id,
    profile_id="profile-abc123",  # Optional: link to profile
    cohort_id="cohort-xyz789",    # Optional: link to cohort
    entity_id="patient-001",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31),
    events_generated=48,
    duration_ms=1500,
    metadata={"source": "batch-generation"}
)

# Record failed execution
manager.journeys.record_execution(
    journey_id=journey.id,
    entity_id="patient-002",
    events_generated=0,
    status="failed",
    error_message="Missing required condition for event"
)
```

### Viewing Execution History

```python
# Get executions for a journey
executions = manager.journeys.get_executions("diabetic-first-year", limit=10)

for exec in executions:
    print(f"  {exec.executed_at}: {exec.events_generated} events for {exec.entity_id}")

# Get all journeys for a specific entity
patient_journeys = manager.journeys.get_entity_journeys("patient-001")

for exec in patient_journeys:
    print(f"  Journey {exec.journey_id}: {exec.start_date} to {exec.end_date}")
```

## Integration with Profiles

Journeys work alongside profiles in the generation workflow:

```python
from healthsim.state import get_manager
from healthsim.generation import ProfileJourneyOrchestrator

manager = get_manager()

# Load both profile and journey
profile = manager.profiles.load_profile("harris-diabetic")
journey = manager.journeys.load_journey("diabetic-first-year")

# Execute together
orchestrator = ProfileJourneyOrchestrator()
result = orchestrator.execute(
    profile_spec=profile.profile_spec,
    journey_spec=journey.journey_spec,
    seed=42
)

# Record both executions
profile_exec_id = manager.profiles.record_execution(
    profile_id=profile.id,
    cohort_id=result["cohort_id"],
    seed=42,
    count=len(result["patients"])
)

for patient in result["patients"]:
    manager.journeys.record_execution(
        journey_id=journey.id,
        profile_id=profile.id,
        cohort_id=result["cohort_id"],
        entity_id=patient["id"],
        events_generated=len(result["encounters"])
    )
```

## Multi-Product Journeys

Journeys can span multiple products:

```python
# Define a cross-product journey
cross_product_spec = {
    "journey_id": "new-member-onboarding",
    "name": "New Member Onboarding Journey",
    "duration_days": 90,
    "products": ["membersim", "patientsim", "rxmembersim"],
    "events": [
        # MemberSim: Enrollment
        {
            "event_id": "enrollment",
            "event_type": "new_enrollment",
            "product": "membersim"
        },
        # PatientSim: Welcome visit
        {
            "event_id": "welcome-visit",
            "event_type": "encounter",
            "product": "patientsim",
            "delay": {"min_days": 14, "max_days": 30}
        },
        # RxMemberSim: First prescription
        {
            "event_id": "first-rx",
            "event_type": "prescription_fill",
            "product": "rxmembersim",
            "delay": {"min_days": 14, "max_days": 45}
        }
    ]
}

manager.journeys.save_journey(
    name="new-member-onboarding",
    journey_spec=cross_product_spec,
    products=["membersim", "patientsim", "rxmembersim"],
    tags=["onboarding", "multi-product"]
)
```

## Built-in Journey Templates

Import standard journey templates:

```python
# Import built-in templates
count = manager.journeys.import_builtin_journeys()
print(f"Imported {count} built-in journey templates")

# List available templates
builtin = manager.journeys.list_journeys(tags=["builtin"])
for j in builtin:
    print(f"  {j.name}: {j.description}")
```

## Data Model

### JourneyRecord

Full journey with specification:

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique journey ID |
| `name` | str | Unique human-readable name |
| `description` | str | Description |
| `version` | int | Version number (auto-increments) |
| `journey_spec` | dict | Full JourneySpecification |
| `products` | list[str] | Products this applies to |
| `tags` | list[str] | Tags for filtering |
| `duration_days` | int | Journey duration |
| `event_count` | int | Number of events |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

### JourneySummary

Brief info for listing:

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Journey ID |
| `name` | str | Journey name |
| `description` | str | Description |
| `version` | int | Version number |
| `products` | list[str] | Products |
| `tags` | list[str] | Tags |
| `duration_days` | int | Duration |
| `event_count` | int | Event count |
| `execution_count` | int | Times executed |
| `last_executed` | datetime | Last execution time |

### JourneyExecutionRecord

Execution history entry:

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Execution ID |
| `journey_id` | str | Journey that was executed |
| `profile_id` | str | Profile used (optional) |
| `cohort_id` | str | Cohort created (optional) |
| `entity_id` | str | Entity ID |
| `start_date` | date | Journey start |
| `end_date` | date | Journey end |
| `events_generated` | int | Events created |
| `duration_ms` | int | Execution time |
| `status` | str | completed/failed/partial |

## Best Practices

1. **Use meaningful names** - Journey names should describe the clinical scenario
2. **Tag consistently** - Use tags like `diabetes`, `cardiac`, `chronic`, `acute`
3. **Version major changes** - Update spec triggers version bump automatically
4. **Track executions** - Always record executions for reproducibility
5. **Link to profiles** - Connect journey executions to profiles and cohorts

## See Also

- [Generative Framework Guide](generative-framework.md) - Complete generation workflow
- [Profile Persistence](profile-persistence.md) - Profile management
- [Reference Data Guide](reference-data.md) - PopulationSim/NetworkSim integration
