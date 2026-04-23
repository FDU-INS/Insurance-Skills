"""PatientSim Journey Module.

This module provides journey (temporal event sequence) functionality for PatientSim,
built on top of the core HealthSim journey engine.

The module re-exports core journey engine classes and provides PatientSim-specific:
- Event handlers for clinical events (ADT, orders, results)
- Journey templates for common clinical scenarios
- Backward-compatible aliases for migration from scenarios

Usage:
    from patientsim.journeys import (
        JourneyEngine,
        JourneySpecification,
        Timeline,
        create_patient_journey_engine,
    )
    
    # Create engine with PatientSim handlers pre-registered
    engine = create_patient_journey_engine(seed=42)
    
    # Use a built-in template
    from patientsim.journeys.templates import PATIENT_JOURNEY_TEMPLATES
    template = PATIENT_JOURNEY_TEMPLATES["diabetic-first-year"]
    timeline = engine.create_timeline(patient, "patient", template)
"""

# Re-export core journey engine classes
from healthsim.generation.journey_engine import (
    # Core classes
    JourneyEngine,
    JourneySpecification,
    Timeline,
    TimelineEvent,
    EventDefinition,
    DelaySpec,
    EventCondition,
    TriggerSpec,
    # Event types
    BaseEventType,
    PatientEventType,
    # Convenience functions
    create_journey_engine,
    create_simple_journey,
    get_journey_template,
    JOURNEY_TEMPLATES,
)

# PatientSim-specific exports
from patientsim.journeys.handlers import (
    create_patient_journey_engine,
    register_patient_handlers,
    PatientSimHandlers,
)
from patientsim.journeys.templates import (
    PATIENT_JOURNEY_TEMPLATES,
    get_patient_journey_template,
    list_patient_journey_templates,
)

# Backward compatibility aliases (deprecated, will be removed in v2.0)
from patientsim.journeys.compat import (
    ScenarioDefinition,  # -> JourneySpecification
    ScenarioEngine,      # -> JourneyEngine
    ScenarioMetadata,    # -> extracted from JourneySpecification
    ScenarioEvent,       # -> EventDefinition
    EventDelay,          # -> DelaySpec
    PatientTimeline,     # -> Timeline
    ScenarioLibrary,     # -> dict of templates
)

__all__ = [
    # Core re-exports
    "JourneyEngine",
    "JourneySpecification", 
    "Timeline",
    "TimelineEvent",
    "EventDefinition",
    "DelaySpec",
    "EventCondition",
    "TriggerSpec",
    "BaseEventType",
    "PatientEventType",
    "create_journey_engine",
    "create_simple_journey",
    "get_journey_template",
    "JOURNEY_TEMPLATES",
    # PatientSim-specific
    "create_patient_journey_engine",
    "register_patient_handlers",
    "PatientSimHandlers",
    "PATIENT_JOURNEY_TEMPLATES",
    "get_patient_journey_template",
    "list_patient_journey_templates",
    # Backward compatibility (deprecated)
    "ScenarioDefinition",
    "ScenarioEngine",
    "ScenarioMetadata",
    "ScenarioEvent",
    "EventDelay",
    "PatientTimeline",
    "ScenarioLibrary",
]
