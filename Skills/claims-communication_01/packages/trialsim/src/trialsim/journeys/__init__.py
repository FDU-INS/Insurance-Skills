"""TrialSim Journey Module.

This module provides journey (temporal event sequence) functionality for TrialSim,
built on top of the core HealthSim journey engine.

The module re-exports core journey engine classes and provides TrialSim-specific:
- Event handlers for clinical trial events (screening, visits, AEs)
- Journey templates for common trial protocols
- Backward-compatible aliases for migration from protocols

Usage:
    from trialsim.journeys import (
        JourneyEngine,
        JourneySpecification,
        Timeline,
        create_trial_journey_engine,
    )
    
    # Create engine with TrialSim handlers pre-registered
    engine = create_trial_journey_engine(seed=42)
    
    # Use a built-in template
    from trialsim.journeys.templates import TRIAL_JOURNEY_TEMPLATES
    template = TRIAL_JOURNEY_TEMPLATES["phase3-oncology-standard"]
    timeline = engine.create_timeline(subject, "subject", template)
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
    TrialEventType,
    # Convenience functions
    create_journey_engine,
    create_simple_journey,
    get_journey_template,
    JOURNEY_TEMPLATES,
)

# TrialSim-specific exports
from trialsim.journeys.handlers import (
    create_trial_journey_engine,
    register_trial_handlers,
    TrialSimHandlers,
)
from trialsim.journeys.templates import (
    TRIAL_JOURNEY_TEMPLATES,
    get_trial_journey_template,
    list_trial_journey_templates,
)

# Backward compatibility aliases (deprecated, will be removed in v2.0)
from trialsim.journeys.compat import (
    ProtocolDefinition,  # -> JourneySpecification
    ProtocolEngine,      # -> JourneyEngine
    ProtocolMetadata,    # -> extracted from JourneySpecification
    ProtocolEvent,       # -> EventDefinition
    VisitSchedule,       # -> DelaySpec
    SubjectTimeline,     # -> Timeline
    ProtocolLibrary,     # -> dict of templates
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
    "TrialEventType",
    "create_journey_engine",
    "create_simple_journey",
    "get_journey_template",
    "JOURNEY_TEMPLATES",
    # TrialSim-specific
    "create_trial_journey_engine",
    "register_trial_handlers",
    "TrialSimHandlers",
    "TRIAL_JOURNEY_TEMPLATES",
    "get_trial_journey_template",
    "list_trial_journey_templates",
    # Backward compatibility (deprecated)
    "ProtocolDefinition",
    "ProtocolEngine",
    "ProtocolMetadata",
    "ProtocolEvent",
    "VisitSchedule",
    "SubjectTimeline",
    "ProtocolLibrary",
]
