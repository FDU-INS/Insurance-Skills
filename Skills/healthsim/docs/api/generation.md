# Generation API Reference

The HealthSim generation framework provides a unified API for generating synthetic healthcare data across all products.

## Unified Entry Point

```python
import healthsim

# Generate from any product
result = healthsim.generate("members", template="commercial-ppo-healthy", count=100)
result = healthsim.generate("patients", template="diabetic-senior", count=50)
result = healthsim.generate("rx", template="medicare-partd-polypharmacy", count=100)
result = healthsim.generate("trials", template="phase3-oncology-trial", count=200)
```

## Core Functions

### `healthsim.generate()`

Generate synthetic data using a profile specification.

```python
result = healthsim.generate(
    product="members",      # Product: members, patients, rx, trials
    template="...",         # Template name (optional)
    profile=None,           # Custom ProfileSpecification (optional)
    journey=None,           # Journey name or spec (optional)
    count=100,              # Number of entities
    seed=42,                # Random seed for reproducibility
    start_date=None,        # Journey start date
)
```

**Returns**: `ExecutionResult` or `OrchestratorResult` (when journey is provided)

### `healthsim.quick_sample()`

Generate a quick sample for testing.

```python
sample = healthsim.quick_sample("members", count=10)
```

### `healthsim.list_products()`

List available products.

```python
products = healthsim.list_products()
# ['membersim', 'patientsim', 'rxmembersim', 'trialsim']
```

### `healthsim.list_templates()`

List templates for a product.

```python
templates = healthsim.list_templates("members")
# ['commercial-ppo-healthy', 'medicare-advantage-diabetic', ...]
```

## Product-Specific Generation

Each product also provides its own generation API:

### MemberSim

```python
from membersim.generation import generate, quick_sample

result = generate("commercial-ppo-healthy", count=100, seed=42)
members = result.members  # List[GeneratedMember]
```

### PatientSim

```python
from patientsim.generation import generate, quick_sample

result = generate("diabetic-senior", count=50, seed=42)
patients = result.patients  # List[GeneratedPatient]
```

### RxMemberSim

```python
from rxmembersim.generation import generate, quick_sample

result = generate("medicare-partd-polypharmacy", count=100, seed=42)
rx_members = result.rx_members  # List[GeneratedRxMember]
```

### TrialSim

```python
from trialsim.generation import generate, quick_sample

result = generate("phase3-oncology-trial", count=200, seed=42)
subjects = result.subjects  # List[GeneratedSubject]
```

## ProfileSpecification

All products use a common `ProfileSpecification` schema:

```python
from healthsim.generation import ProfileSpecification

profile = ProfileSpecification(
    id="my-custom-profile",
    name="Custom Profile",
    demographics={
        "age_distribution": {"mean": 65, "std": 10},
        "gender_distribution": {"M": 0.48, "F": 0.52},
    },
    clinical={
        "conditions": [
            {"code": "E11", "name": "Type 2 Diabetes", "prevalence": 0.3}
        ]
    },
    generation={"count": 100, "seed": 42},
)
```

## Journeys

Generate entities with temporal event timelines:

```python
result = healthsim.generate(
    "patients",
    template="diabetic-senior",
    journey="diabetic-first-year",
    count=100,
)

# Access timelines
for entity in result.entities:
    print(f"Entity has {entity.pending_events} pending events")
    for event in entity.timeline.events:
        print(f"  {event.scheduled_date}: {event.name}")
```

## Reproducibility

All generation is fully reproducible with seed control:

```python
# Same seed = same output
r1 = healthsim.generate("members", count=100, seed=42)
r2 = healthsim.generate("members", count=100, seed=42)
assert r1.members[0].member_id == r2.members[0].member_id
```

## ExecutionResult

Results from profile execution:

```python
result = healthsim.generate("members", template="...", count=100)

result.count           # Number generated
result.seed            # Seed used
result.duration        # Execution time
result.profile_id      # Profile identifier
result.members         # Product-specific: generated entities
result.validation      # Validation report
```

## OrchestratorResult

Results when using journeys:

```python
result = healthsim.generate(..., journey="...")

result.entity_count    # Number of entities
result.event_count     # Total events across all timelines
result.journey_ids     # Journey IDs used
result.entities        # List[EntityWithTimeline]
result.get_events_by_date(date)  # Events on a specific date
```
