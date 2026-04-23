"""MemberSim Journey Module.

This module provides journey (temporal event sequence) functionality for MemberSim,
built on top of the core HealthSim journey engine.

The module re-exports core journey engine classes and provides MemberSim-specific:
- Event handlers for payer/claims events
- Journey templates for common member journeys
- Backward-compatible aliases for migration from scenarios

Usage:
    from membersim.journeys import (
        JourneyEngine,
        JourneySpecification,
        Timeline,
        create_member_journey_engine,
    )
    
    # Create engine with MemberSim handlers pre-registered
    engine = create_member_journey_engine(seed=42)
    
    # Use a built-in template
    from membersim.journeys.templates import NEW_MEMBER_ONBOARDING
    timeline = engine.create_timeline(member, "member", NEW_MEMBER_ONBOARDING)
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
    MemberEventType,
    # Convenience functions
    create_journey_engine,
    create_simple_journey,
    get_journey_template,
    JOURNEY_TEMPLATES,
)

# MemberSim-specific exports
from membersim.journeys.handlers import (
    create_member_journey_engine,
    register_member_handlers,
)
from membersim.journeys.templates import (
    MEMBER_JOURNEY_TEMPLATES,
    get_member_journey_template,
)

# Backward compatibility aliases (deprecated, will be removed in v2.0)
from membersim.journeys.compat import (
    ScenarioDefinition,  # -> JourneySpecification
    ScenarioEngine,      # -> JourneyEngine
    ScenarioMetadata,    # -> extracted from JourneySpecification
    ScenarioEvent,       # -> EventDefinition
    EventDelay,          # -> DelaySpec
    MemberTimeline,      # -> Timeline
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
    "MemberEventType",
    "create_journey_engine",
    "create_simple_journey",
    "get_journey_template",
    "JOURNEY_TEMPLATES",
    # MemberSim-specific
    "create_member_journey_engine",
    "register_member_handlers",
    "MEMBER_JOURNEY_TEMPLATES",
    "get_member_journey_template",
    # Backward compatibility (deprecated)
    "ScenarioDefinition",
    "ScenarioEngine",
    "ScenarioMetadata",
    "ScenarioEvent",
    "EventDelay",
    "MemberTimeline",
    "ScenarioLibrary",
]
