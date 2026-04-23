# HealthSim Generative Framework Guide

## Overview

The Generative Framework is the core data generation system for HealthSim. It enables reproducible, realistic healthcare data generation across all HealthSim products through a unified architecture.

### Mental Model

```
Profile Specification + Journey Specification = Generated Data

Profile  →  WHO (demographics, conditions, coverage)
Journey  →  WHAT HAPPENS (events over time)
Output   →  Realistic healthcare entities and transactions
```

### Design Philosophy

The framework follows "Configuration via Conversation" - you describe what you want in natural language, and Claude translates that into specifications that execute deterministically.

---

## Two-Phase Architecture

### Phase 1: Profile Generation

The Profile Executor generates **point-in-time entities** - patients, members, providers, facilities - with their static attributes.

```
┌─────────────────────────────────────────────────────────────┐
│                    Profile Specification                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Demographics │  │  Clinical   │  │     Coverage       │  │
│  │ - Age        │  │ - Diagnoses │  │ - Plan type        │  │
│  │ - Gender     │  │ - Labs      │  │ - Effective dates  │  │
│  │ - Geography  │  │ - Meds      │  │ - Group            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Profile Executor                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │Seed Manager │→ │Distribution │→ │ Entity Generator    │  │
│  │(Hierarchy)  │  │  Sampling   │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                ┌─────────────────────┐
                │ Generated Entities  │
                │ - Patient records   │
                │ - Member records    │
                │ - Provider records  │
                └─────────────────────┘
```

### Phase 2: Journey Execution

The Journey Engine generates **events over time** - encounters, claims, prescriptions - based on journeys (temporal event sequences).

```
┌─────────────────────────────────────────────────────────────┐
│                   Journey Specification                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Events    │  │ Conditions  │  │     Triggers        │  │
│  │ - Type      │  │ - Age >= 65 │  │ - Cross-product     │  │
│  │ - Timing    │  │ - Has dx    │  │ - dx → claim        │  │
│  │ - Depends   │  │             │  │ - med → fill        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Journey Engine                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Timeline   │→ │   Event     │→ │Product Handlers     │  │
│  │ Scheduler   │  │  Executor   │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                ┌─────────────────────┐
                │   Generated Events  │
                │ - Encounters        │
                │ - Claims            │
                │ - Prescriptions     │
                └─────────────────────┘
```

---

## Distribution Types

The framework supports multiple distribution types for realistic data variation:

| Distribution | Use Case | Parameters |
|--------------|----------|------------|
| **Normal** | Age, lab values, vitals | mean, std_dev, min, max |
| **LogNormal** | Costs, lengths of stay | mean, sigma |
| **Uniform** | Random selection in range | min, max |
| **Categorical** | Gender, race, plan type | weights dict |
| **AgeBand** | Age groups by category | bands with prevalence |
| **Explicit** | Fixed value lists | values list |
| **Conditional** | Value depends on context | rules with conditions |

### Distribution Selection Guide

```
Start Here:
│
├── Is there a fixed set of options?
│   ├── Yes → Are they equally likely?
│   │         ├── Yes → Categorical with equal weights
│   │         └── No  → Categorical with weighted probabilities
│   │
│   └── No → Is the value continuous?
│            ├── Yes → Is it normally distributed?
│            │         ├── Yes → Normal
│            │         └── No  → Is it right-skewed (costs, durations)?
│            │                   ├── Yes → LogNormal
│            │                   └── No  → Uniform or custom
│            │
│            └── No → Does it depend on other attributes?
│                     ├── Yes → Conditional
│                     └── No  → Explicit list
```

---

## Reference Data Integration

The framework can populate profiles from real-world reference data (CDC PLACES, SVI).

### Available Reference Sources

| Source | Level | Data Points |
|--------|-------|-------------|
| CDC PLACES | County, Tract | Diabetes, obesity, hypertension, COPD, cancer, depression rates |
| CDC SVI | County, Tract | Age distribution, race/ethnicity, poverty, uninsured rates |

### Hybrid Profile Example

Combine reference data with custom overrides:

```python
# Use Harris County TX demographics, but override age for Medicare population
user_spec = {
    "profile": {
        "demographics": {
            "source": "populationsim",
            "reference": {"type": "county", "fips": "48201"},
            "age": {"type": "normal", "mean": 72, "std_dev": 8}  # Override
        }
    }
}
hybrid = create_hybrid_profile(user_spec, conn)
# Reference fills: gender, race, conditions from real county data
# User override: age distribution for Medicare
```

---

## Journey System

### Event Types by Product

**PatientSim Events:**
- ADT: admission, discharge, transfer
- Clinical: encounter, observation, procedure, medication_order, lab_order, lab_result, diagnosis
- Care: referral, care_plan_update

**MemberSim Events:**
- Enrollment: new_enrollment, termination, plan_change
- Claims: claim_professional, claim_institutional, claim_pharmacy
- Quality: gap_identified, gap_closed

**RxMemberSim Events:**
- Prescription: new_rx, refill, fill, reversal
- Therapy: therapy_start, therapy_change, therapy_discontinue
- Adherence: adherence_gap, mpr_threshold

**TrialSim Events:**
- Enrollment: screening, randomization, withdrawal
- Visits: scheduled_visit, unscheduled_visit
- Safety: adverse_event, serious_adverse_event

### Event Timing

Events can be scheduled with various delay patterns:

```python
# Fixed delay
delay = DelaySpec(days=30)

# Random within range
delay = DelaySpec(days=30, days_min=20, days_max=40, distribution="uniform")

# Normal distribution around mean
delay = DelaySpec(days=30, days_min=20, days_max=40, distribution="normal")
```

### Event Dependencies

Events can depend on other events:

```json
{
  "events": [
    {"event_id": "dx", "name": "Diagnosis", "delay": {"days": 0}},
    {"event_id": "lab", "name": "A1C Test", "delay": {"days": 7}, "depends_on": "dx"},
    {"event_id": "med", "name": "Start Metformin", "delay": {"days": 3}, "depends_on": "dx"}
  ]
}
```

### Conditional Events

Events can have conditions:

```json
{
  "event_id": "senior_screening",
  "name": "Annual Wellness Visit",
  "conditions": [
    {"field": "entity.age", "operator": "gte", "value": 65}
  ]
}
```

---

## Cross-Product Coordination

The trigger system enables events in one product to spawn events in others.

### Default Healthcare Triggers

| Source Event | Target Product | Target Event | Typical Delay |
|--------------|----------------|--------------|---------------|
| diagnosis | membersim | claim_professional | 1-7 days |
| medication_order | membersim | claim_pharmacy | 0-3 days |
| medication_order | rxmembersim | fill | 0-3 days |
| lab_order | patientsim | lab_result | 1-5 days |
| gap_identified | patientsim | care_plan_update | 3-14 days |

### Linked Entities

Cross-product coordination uses linked entities:

```python
coordinator = CrossProductCoordinator()

# Create entity with cross-product IDs
linked = coordinator.create_linked_entity("E001", {
    "patient_id": "P001",
    "member_id": "M001",
    "rx_member_id": "RX001"
})

# Execute coordinated timeline
results = coordinator.execute_coordinated(linked, up_to_date=date.today())
```

---

## Reproducibility

All generation is deterministic with proper seeding.

### Hierarchical Seeds

```python
# Master seed controls entire generation
executor = ProfileExecutor(master_seed=42)

# Entity-level seeds derive from master
# Entity 1: seed = hash(42, 1) → consistent Patient P001
# Entity 2: seed = hash(42, 2) → consistent Patient P002

# Attribute-level seeds derive from entity
# P001.age: seed = hash(entity_seed, "age")
# P001.gender: seed = hash(entity_seed, "gender")
```

### Regenerating Specific Entities

```python
# Regenerate just entity 5 with same results
entity_5 = executor.generate_entity(index=5)  # Uses derived seed
```

---


## API Reference

### Profile Module

```python
from healthsim.generation import (
    # Distributions
    NormalDistribution,
    LogNormalDistribution,
    CategoricalDistribution,
    AgeBandDistribution,
    UniformIntDistribution,
    ExplicitDistribution,
    ConditionalDistribution,
    create_distribution,
    
    # Profile
    ProfileSpecification,
    ProfileExecutor,
    ExecutionResult,
    GeneratedEntity,
    
    # Reference Data
    ReferenceProfileResolver,
    resolve_geography,
    create_hybrid_profile,
)
```

### Journey Module

```python
from healthsim.generation import (
    # Engine
    JourneyEngine,
    create_journey_engine,
    
    # Specifications
    JourneySpecification,
    EventDefinition,
    EventCondition,
    DelaySpec,
    
    # Timeline
    Timeline,
    TimelineEvent,
    
    # Event Types
    BaseEventType,
    PatientEventType,
    MemberEventType,
    RxEventType,
    TrialEventType,
    
    # Templates
    get_journey_template,
    create_simple_journey,
    JOURNEY_TEMPLATES,
)
```

### Trigger Module

```python
from healthsim.generation import (
    # Coordination
    CrossProductCoordinator,
    LinkedEntity,
    create_coordinator,
    
    # Registry
    TriggerRegistry,
    RegisteredTrigger,
    TriggerPriority,
)
```

---

## Quick Start Examples

### Example 1: Simple Profile Generation

```python
from healthsim.generation import ProfileExecutor, create_distribution

# Create a simple profile spec
spec = {
    "generation": {"count": 10, "seed": 42},
    "demographics": {
        "age": {"type": "normal", "mean": 45, "std_dev": 15, "min": 18, "max": 90},
        "gender": {"type": "categorical", "weights": {"M": 0.49, "F": 0.51}}
    }
}

# Execute
executor = ProfileExecutor(master_seed=42)
result = executor.execute(spec)

# Access entities
for entity in result.entities:
    print(f"{entity.entity_id}: Age {entity.attributes['age']}, Gender {entity.attributes['gender']}")
```

### Example 2: Journey with Timeline

```python
from datetime import date
from healthsim.generation import (
    JourneyEngine,
    create_simple_journey,
)

# Create journey
journey = create_simple_journey(
    "diabetes-care",
    "Diabetes Care Journey",
    events=[
        {"event_id": "dx", "name": "Diagnosis", "event_type": "diagnosis", 
         "delay": {"days": 0}},
        {"event_id": "lab", "name": "Initial A1C", "event_type": "lab_order",
         "delay": {"days": 7}, "depends_on": "dx"},
        {"event_id": "med", "name": "Start Metformin", "event_type": "medication_order",
         "delay": {"days": 3}, "depends_on": "dx"},
    ]
)

# Create engine and timeline
engine = JourneyEngine(seed=42)
patient = {"patient_id": "P001", "name": "John Doe"}
timeline = engine.create_timeline(patient, "patient", journey, start_date=date(2025, 1, 1))

# View scheduled events
for event in timeline.events:
    print(f"{event.scheduled_date}: {event.event_name} ({event.event_type})")
```

### Example 3: Reference-Based Profile

```python
import duckdb
from healthsim.generation import ReferenceProfileResolver, create_hybrid_profile

# Connect to reference database
conn = duckdb.connect("healthsim_current.duckdb")

# Get real demographics from Harris County, TX
resolver = ReferenceProfileResolver(conn)
profile = resolver.resolve_county("48201")

print(f"Population: {profile.population:,}")
print(f"Diabetes prevalence: {profile.pct_diabetes}%")
print(f"Obesity prevalence: {profile.pct_obesity}%")

# Create profile spec from reference
spec = resolver.to_profile_spec(profile)
```

### Example 4: Cross-Product Generation

```python
from datetime import date
from healthsim.generation import (
    CrossProductCoordinator,
    JourneyEngine,
    get_journey_template,
)

# Setup coordinator
coordinator = CrossProductCoordinator()

# Create linked entity
linked = coordinator.create_linked_entity("E001", {
    "patient_id": "P001",
    "member_id": "M001"
})

# Create product engines
patient_engine = JourneyEngine(seed=42)
member_engine = JourneyEngine(seed=42)

coordinator.register_product_engine("patientsim", patient_engine)
coordinator.register_product_engine("membersim", member_engine)

# Get diabetic journey (spans both products)
journey = get_journey_template("diabetic-first-year")

# Create timelines
patient_timeline = patient_engine.create_timeline(
    {"patient_id": "P001"}, "patient", journey, date(2025, 1, 1)
)
coordinator.add_timeline(linked, "patientsim", patient_timeline)

# Execute coordinated events
results = coordinator.execute_coordinated(linked, up_to_date=date(2025, 3, 31))
```

---

## Built-in Templates

### Profile Templates

| Template | Description | Products |
|----------|-------------|----------|
| `medicare-diabetic` | Medicare beneficiary with Type 2 diabetes | patientsim, membersim |
| `commercial-healthy` | Working-age commercial member, healthy | membersim |
| `medicaid-pediatric` | Medicaid pediatric population | patientsim, membersim |
| `medicare-advantage-complex` | MA member with multiple chronic conditions | membersim |
| `commercial-maternity` | Commercial maternity episode | patientsim, membersim |

### Journey Templates

| Template | Description | Duration |
|----------|-------------|----------|
| `diabetic-first-year` | First year of diabetic care | 365 days |
| `new-member-onboarding` | New member enrollment and onboarding | 90 days |
| `surgical-episode` | Surgical episode from pre-op to recovery | 90 days |
| `hf-exacerbation` | Heart failure exacerbation cycle | 60 days |
| `oncology-treatment-cycle` | Chemotherapy treatment cycle | 21 days |

---

## Best Practices

### 1. Start with Templates

Use built-in templates as starting points, then customize:

```
"Use the Medicare diabetic template with 50 patients in Texas"
```

### 2. Use Reference Data

For realistic geographic variation, leverage CDC PLACES and SVI data:

```python
profile = resolver.resolve_county("48201")  # Real Harris County data
```

### 3. Seed Everything

Always provide seeds for reproducibility:

```python
executor = ProfileExecutor(master_seed=42)
engine = JourneyEngine(seed=42)
```

### 4. Layer Journeys

Combine multiple journeys for complex scenarios:

```python
# Base enrollment + disease-specific journey
timeline1 = engine.create_timeline(member, "member", enrollment_journey)
timeline2 = engine.create_timeline(patient, "patient", diabetic_journey)
```

### 5. Validate Outputs

Use validation to catch specification errors early:

```python
result = executor.execute(spec)
if not result.validation.is_valid:
    for error in result.validation.errors:
        print(f"Error: {error}")
```

---

## File Locations

### Python Modules
- `packages/core/src/healthsim/generation/distributions.py` - Distribution types
- `packages/core/src/healthsim/generation/profile_schema.py` - Profile specifications
- `packages/core/src/healthsim/generation/profile_executor.py` - Profile execution
- `packages/core/src/healthsim/generation/reference_profiles.py` - Reference data integration
- `packages/core/src/healthsim/generation/journey_engine.py` - Journey execution
- `packages/core/src/healthsim/generation/triggers.py` - Cross-product triggers

### Skills (for Claude)
- `skills/generation/SKILL.md` - Main generation skill
- `skills/generation/builders/profile-builder.md` - Profile building guidance
- `skills/generation/executors/profile-executor.md` - Execution guidance
- `skills/generation/distributions/distribution-types.md` - Distribution reference

### Templates
- `skills/generation/templates/profiles/` - Profile templates
- `skills/generation/templates/journeys/` - Journey templates

---

*HealthSim Generative Framework v1.0 | Last Updated: 2026-01-04*
