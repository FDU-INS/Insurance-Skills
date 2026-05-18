# Journey Engine API Reference

This document describes the `JourneyEngine` class and related components for creating and executing temporal event sequences.

## Overview

The Journey Engine transforms `JourneySpecification` objects into executed timelines of events for entities. It handles:

- Event scheduling with delays and conditions
- Skill integration for clinical accuracy
- Cross-product event coordination
- Timeline state management

## Core Classes

### JourneyEngine

The main engine for executing journeys.

```python
from healthsim.generation.journeys import JourneyEngine

engine = JourneyEngine(
    handlers: dict = None,           # Product-specific event handlers
    skill_resolver: SkillResolver = None,
    skill_registry: SkillRegistry = None
)
```

#### Methods

**create_timeline(entity, journey_spec, start_date) → Timeline**

Creates an event timeline for a single entity.

```python
from datetime import date

timeline = engine.create_timeline(
    entity=patient,
    journey_spec=journey_spec,
    start_date=date(2024, 1, 1)
)
```

**execute_journey(entity, journey_spec, start_date) → ExecutionResult**

Fully executes a journey, generating all events.

```python
result = engine.execute_journey(
    entity=patient,
    journey_spec=journey_spec,
    start_date=date(2024, 1, 1)
)

print(f"Generated {len(result.events)} events")
```

**schedule_events(timeline) → List[ScheduledEvent]**

Schedules events based on timeline phases and delays.

**evaluate_condition(condition, entity, context) → bool**

Evaluates whether a conditional event should execute.

### JourneySpecification

Defines the structure of a journey.

```python
from healthsim.generation.journeys import JourneySpecification

JourneySpecification(
    name: str,
    description: str = None,
    phases: List[PhaseDefinition] = None,
    events: List[EventDefinition] = None,  # Flat event list (alternative to phases)
    duration_days: int = None,
    products: List[str] = None,            # Products this journey targets
    metadata: dict = None
)
```

### PhaseDefinition

Groups related events into logical phases.

```python
PhaseDefinition(
    name: str,
    description: str = None,
    duration_days: int = None,
    events: List[EventDefinition] = None,
    entry_condition: EventCondition = None
)
```

### EventDefinition

Defines a single event in a journey.

```python
EventDefinition(
    event_type: str,                 # "encounter", "claim", "prescription", etc.
    delay: DelaySpec = None,         # When event occurs
    parameters: dict = None,         # Event-specific parameters
    condition: str = None,           # Auto-resolved condition (e.g., "diabetes")
    skill_ref: SkillReference = None,# Explicit skill reference
    repeat: RepeatSpec = None,       # For recurring events
    triggers: List[TriggerSpec] = None  # Cross-product triggers
)
```

### DelaySpec

Controls event timing.

```python
DelaySpec(
    days: int = None,                # Fixed delay in days
    min_days: int = None,            # Random range minimum
    max_days: int = None,            # Random range maximum
    distribution: str = "uniform",   # "uniform", "normal"
    relative_to: str = "phase_start" # "phase_start", "previous_event", "journey_start"
)
```

### EventCondition

Conditional event execution.

```python
EventCondition(
    field: str,                      # Entity field to check
    operator: str,                   # "eq", "ne", "gt", "lt", "in", "contains"
    value: Any                       # Comparison value
)
```

## Skill Integration

The Journey Engine supports two methods for integrating clinical skills:

### Automatic Resolution (Recommended)

Use the `condition` field for automatic skill lookup:

```python
EventDefinition(
    event_type="encounter",
    condition="diabetes",  # Auto-resolves via SkillRegistry
    parameters={
        "encounter_type": "office_visit"
    }
)
```

### Explicit Reference

Use `skill_ref` for precise control:

```python
EventDefinition(
    event_type="encounter",
    skill_ref=SkillReference(
        skill="diabetes-management",
        lookup="monitoring.lab_panels.basic_metabolic",
        fallback={"code": "80048"}
    )
)
```

## Event Handlers

Product-specific handlers process events:

```python
from healthsim.generation.journeys import EventHandler

class PatientSimEncounterHandler(EventHandler):
    def handle(self, event: ScheduledEvent, entity, context) -> GeneratedEvent:
        # Generate PatientSim-specific encounter
        return GeneratedEvent(...)
```

Register handlers with the engine:

```python
engine = JourneyEngine(handlers={
    "patientsim": {
        "encounter": PatientSimEncounterHandler(),
        "diagnosis": PatientSimDiagnosisHandler()
    }
})
```

## Complete Example

```python
from healthsim.generation.journeys import (
    JourneyEngine, JourneySpecification, PhaseDefinition,
    EventDefinition, DelaySpec
)
from datetime import date

# Define journey
journey = JourneySpecification(
    name="diabetic-first-year",
    description="First year care journey for newly diagnosed diabetic",
    phases=[
        PhaseDefinition(
            name="initial_assessment",
            duration_days=30,
            events=[
                EventDefinition(
                    event_type="encounter",
                    condition="diabetes",
                    parameters={"encounter_type": "initial_visit"}
                ),
                EventDefinition(
                    event_type="lab_order",
                    delay=DelaySpec(days=0),
                    parameters={"panel": "HbA1c"}
                )
            ]
        ),
        PhaseDefinition(
            name="ongoing_management",
            duration_days=335,
            events=[
                EventDefinition(
                    event_type="encounter",
                    condition="diabetes",
                    delay=DelaySpec(min_days=80, max_days=100),
                    repeat=RepeatSpec(count=3)
                )
            ]
        )
    ],
    products=["patientsim"]
)

# Execute
engine = JourneyEngine()
result = engine.execute_journey(
    entity=patient,
    journey_spec=journey,
    start_date=date(2024, 1, 1)
)

for event in result.events:
    print(f"{event.date}: {event.event_type}")
```

## Timeline Object

The `Timeline` tracks journey state:

```python
timeline.entity          # The entity being processed
timeline.journey_spec    # The specification
timeline.start_date      # Journey start
timeline.current_phase   # Active phase
timeline.events          # Scheduled events
timeline.executed        # Completed events
timeline.context         # Accumulated context data
```

## Persistence

See [Journey Persistence Guide](../guides/journey-persistence.md) for saving and reusing journeys.

## See Also

- [Generative Framework Guide](../guides/generative-framework.md) - Overview
- [Skill Integration Guide](../guides/skill-integration.md) - Skills in journeys
- [Journey Persistence](../guides/journey-persistence.md) - Save and reuse journeys
- [Profile Schema](profile-schema.md) - Population specifications
