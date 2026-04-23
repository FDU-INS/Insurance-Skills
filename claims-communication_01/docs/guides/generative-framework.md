# Generative Framework Guide

The HealthSim Generative Framework provides a unified approach to generating synthetic healthcare data across all products. This guide covers the complete workflow from profile specification to data generation and persistence.

## Overview

The framework follows a three-phase approach:

1. **Specification**: Define profiles that describe what to generate
2. **Generation**: Execute profiles to produce synthetic data
3. **Persistence**: Save profiles and results for reuse

```
┌─────────────────────────────────────────────────────────────────┐
│                    Generative Framework                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │   Profile   │───▶│  Execution  │───▶│  Cohort     │        │
│   │   Spec      │    │             │    │  Output     │        │
│   └─────────────┘    └─────────────┘    └─────────────┘        │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │ Reference   │    │   Skills    │    │   State     │        │
│   │   Data      │    │ (Clinical)  │    │  Manager    │        │
│   └─────────────┘    └─────────────┘    └─────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Simple Generation

```python
from healthsim import generate

# Generate 10 diabetic patients
result = generate(
    product="patientsim",
    count=10,
    condition="diabetes"
)

print(f"Generated {len(result['patients'])} patients")
```

### 2. Profile-Based Generation

```python
from healthsim.generation import ProfileExecutor

# Define a profile
profile = {
    "profile": {
        "id": "elderly-diabetic",
        "generation": {"count": 100, "seed": 42},
        "demographics": {
            "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65}
        },
        "clinical": {
            "primary_condition": {"code": "E11", "prevalence": 1.0}
        }
    }
}

# Execute
executor = ProfileExecutor()
result = executor.execute(profile)
```

### 3. Reference Data Integration

```python
from healthsim.generation import create_hybrid_profile_with_network
import duckdb

conn = duckdb.connect("healthsim.duckdb", read_only=True)

# Profile with real demographics and providers
spec = {
    "profile": {
        "id": "harris-diabetic",
        "demographics": {
            "source": "populationsim",
            "reference": {"type": "county", "fips": "48201"}  # Harris County
        },
        "providers": {
            "source": "networksim",
            "reference": {"state": "TX", "specialty": "endocrinology"}
        }
    }
}

hybrid = create_hybrid_profile_with_network(spec, conn)
```

## Profile Specification

### Structure

```python
{
    "profile": {
        "id": "unique-identifier",
        "product": "patientsim",  # or membersim, rxmembersim, trialsim
        "generation": {
            "count": 100,
            "seed": 42,           # Optional: for reproducibility
            "batch_size": 50      # Optional: for large generations
        },
        "demographics": { ... },
        "clinical": { ... },
        "coverage": { ... },      # MemberSim
        "pharmacy": { ... },      # RxMemberSim
        "trial": { ... }          # TrialSim
    }
}
```

### Demographics Section

```python
"demographics": {
    # Option 1: Manual specification
    "age": {"type": "normal", "mean": 65, "std_dev": 10, "min": 18, "max": 95},
    "gender": {"male": 0.48, "female": 0.52},
    
    # Option 2: Reference data
    "source": "populationsim",
    "reference": {"type": "county", "fips": "48201"}
}
```

### Clinical Section

```python
"clinical": {
    "primary_condition": {
        "code": "E11",
        "description": "Type 2 diabetes mellitus",
        "prevalence": 1.0
    },
    "comorbidities": [
        {"code": "I10", "prevalence": 0.7},   # Hypertension
        {"code": "E78", "prevalence": 0.5}    # Hyperlipidemia
    ]
}
```

## Skill Integration

Skills provide clinical knowledge for realistic data generation:

### Automatic Resolution

```python
from healthsim.generation import JourneyDefinition, EventDefinition

# Just specify the condition - skill is resolved automatically
journey = JourneyDefinition(
    id="dm-journey",
    events=[
        EventDefinition(
            id="office-visit",
            event_type="encounter",
            condition="diabetes",  # Automatically finds diabetes-management skill
            parameters={"class_code": "AMB"}
        )
    ]
)
```

### Explicit Skill Reference

```python
EventDefinition(
    id="labs",
    event_type="lab_order",
    parameters={
        "skill_ref": {
            "skill": "diabetes-management",
            "lookup": "monitoring.labs.hba1c"
        }
    }
)
```

### Available Skills

| Skill | Conditions | Content |
|-------|------------|---------|
| diabetes-management | diabetes, type2_diabetes | Labs, meds, complications |
| chronic-kidney-disease | ckd, renal_disease | Staging, dialysis |
| heart-failure | hf, chf | NYHA classification, meds |
| hypertension | htn, hypertension | BP targets, medications |
| copd | copd | Spirometry, inhalers |

## Profile Persistence

### Saving Profiles

```python
from healthsim.state import get_manager

manager = get_manager()

# Save a profile for reuse
profile_id = manager.profiles.save_profile(
    name="harris-diabetic-v1",
    profile_spec=spec,
    description="Diabetic patients in Harris County",
    tags=["diabetes", "texas", "elderly"]
)
```

### Loading and Executing

```python
# Load by name
profile = manager.profiles.load_profile("harris-diabetic-v1")

# Execute
executor = ProfileExecutor()
result = executor.execute(profile.profile_spec)

# Record execution
manager.profiles.record_execution(
    profile_id=profile.id,
    cohort_id=result.get("cohort_id"),
    seed=42,
    count=len(result["patients"]),
    duration_ms=1500
)
```

### Listing and Searching

```python
# List all diabetes profiles
profiles = manager.profiles.list_profiles(tags=["diabetes"])

# Search by name/description
profiles = manager.profiles.list_profiles(search="harris")

# Filter by product
profiles = manager.profiles.list_profiles(product="patientsim")
```

### Re-execution with Seed

```python
# Get the exact spec used in a previous execution
spec = manager.profiles.get_execution_spec(execution_id=123)

# Re-execute to reproduce results
result = executor.execute(spec)
```

## Journey Persistence

Journeys define temporal event sequences and can be persisted for reuse across profiles and products.

### Saving Journeys

```python
from healthsim.state import get_manager

manager = get_manager()

# Save a reusable journey
journey_id = manager.journeys.save_journey(
    name="diabetic-first-year",
    journey_spec={
        "journey_id": "diabetic-first-year",
        "name": "First Year Diabetes Management",
        "duration_days": 365,
        "products": ["patientsim"],
        "events": [
            {"event_id": "q1-visit", "event_type": "encounter", "delay": {"days": 0}},
            {"event_id": "q2-visit", "event_type": "encounter", "delay": {"days": 90}},
            {"event_id": "q3-visit", "event_type": "encounter", "delay": {"days": 180}},
            {"event_id": "q4-visit", "event_type": "encounter", "delay": {"days": 270}},
        ]
    },
    description="Quarterly visits for new diabetics",
    tags=["diabetes", "chronic-care"]
)
```

### Loading and Executing Journeys

```python
# Load by name
journey = manager.journeys.load_journey("diabetic-first-year")

# Execute for a patient
from healthsim.generation import JourneyEngine
engine = JourneyEngine()
events = engine.execute_journey(journey.journey_spec, patient, start_date)

# Record execution
manager.journeys.record_execution(
    journey_id=journey.id,
    entity_id=patient.id,
    start_date=start_date,
    events_generated=len(events),
    duration_ms=250
)
```

### Listing and Searching Journeys

```python
# List all chronic care journeys
journeys = manager.journeys.list_journeys(tags=["chronic-care"])

# Filter by product
journeys = manager.journeys.list_journeys(products=["patientsim"])

# Search by name
journeys = manager.journeys.list_journeys(search="diabetic")
```

### Linking Journeys to Profiles

```python
# Record execution with profile and cohort links
manager.journeys.record_execution(
    journey_id=journey_id,
    profile_id=profile_id,
    cohort_id=cohort_id,
    entity_id="patient-123",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31),
    events_generated=12
)

# Get all journeys executed for an entity
executions = manager.journeys.get_entity_journeys("patient-123")
```

## Journey Engine

The JourneyEngine generates sequences of healthcare events over time:

```python
from healthsim.generation import JourneyEngine, JourneyDefinition, EventDefinition
from healthsim.generation.person import Person
from datetime import date

# Define a journey
journey = JourneyDefinition(
    id="diabetic-year-one",
    duration_days=365,
    events=[
        EventDefinition(
            id="quarterly-visit",
            event_type="encounter",
            timing={"type": "recurring", "interval_days": 90},
            condition="diabetes"
        ),
        EventDefinition(
            id="annual-labs",
            event_type="lab_order",
            timing={"type": "fixed", "day": 30},
            parameters={"panels": ["cmp", "lipid", "hba1c"]}
        )
    ]
)

# Execute for a patient
engine = JourneyEngine()
person = Person(birth_date=date(1955, 3, 15), gender="M")
events = engine.execute(journey, person, start_date=date(2024, 1, 1))
```

## Orchestrator

The ProfileJourneyOrchestrator combines profiles with journeys:

```python
from healthsim.generation import ProfileJourneyOrchestrator

orchestrator = ProfileJourneyOrchestrator()

result = orchestrator.execute(
    profile_spec=profile,
    journey_id="diabetic-year-one",
    seed=42
)

# Result contains:
# - patients: Generated patient entities
# - encounters: All encounters from journey
# - diagnoses: All diagnoses
# - medications: All medication orders
# - labs: All lab results
```

## Reference Data

### PopulationSim (Demographics)

```python
from healthsim.generation import ReferenceProfileResolver

resolver = ReferenceProfileResolver(conn)

# County-level demographics
profile = resolver.resolve_county("48201")  # Harris County
print(f"Diabetes rate: {profile.pct_diabetes}%")
print(f"Obesity rate: {profile.pct_obesity}%")
print(f"65+ population: {profile.pct_age_65_plus}%")

# State-level aggregation
state_profile = resolver.resolve_state("TX")
```

### NetworkSim (Providers/Facilities)

```python
from healthsim.generation import NetworkSimResolver, TAXONOMY_MAP

resolver = NetworkSimResolver(conn)

# Find cardiologists in Houston
providers = resolver.find_providers(
    state="TX",
    city="HOUSTON",
    taxonomy=TAXONOMY_MAP["cardiology"],
    limit=20
)

# Find hospitals with 200+ beds
hospitals = resolver.find_facilities(
    state="TX",
    facility_type="hospital",
    min_beds=200
)
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `generate()` | Unified entry point for all products |
| `create_hybrid_profile()` | Merge user spec with PopulationSim |
| `create_hybrid_profile_with_network()` | Add NetworkSim providers/facilities |

### Classes

| Class | Purpose |
|-------|---------|
| `ProfileExecutor` | Execute profile specifications |
| `JourneyEngine` | Generate event sequences |
| `ProfileJourneyOrchestrator` | Combine profiles with journeys |
| `StateManager` | Cohort persistence |
| `ProfileManager` | Profile persistence |

### State Management

| Method | Description |
|--------|-------------|
| `manager.persist()` | Save entities (token-efficient) |
| `manager.get_summary()` | Load cohort summary |
| `manager.profiles.save_profile()` | Save profile spec |
| `manager.profiles.load_profile()` | Load profile by name/id |
| `manager.profiles.record_execution()` | Track execution history |

## Best Practices

1. **Use Seeds for Reproducibility**
   ```python
   {"generation": {"seed": 42}}
   ```

2. **Start with Reference Data**
   - Use PopulationSim for realistic demographics
   - Use NetworkSim for real provider assignments

3. **Save Profiles for Reuse**
   - Version your profiles
   - Tag for easy filtering

4. **Use Auto-Persist for Large Cohorts**
   ```python
   result = manager.persist(entities, context="...")
   # Returns summary, not full data
   ```

5. **Leverage Skills for Clinical Accuracy**
   - Skills contain validated clinical codes
   - Automatic resolution simplifies definitions

## See Also

- [Reference Data Guide](reference-data.md) - PopulationSim/NetworkSim integration
- [Skill Integration Guide](skill-integration.md) - Clinical knowledge integration
- [Profile Schema](../api/profile-schema.md) - Detailed specification format
- [API Documentation](../api/generation.md) - Full API reference
