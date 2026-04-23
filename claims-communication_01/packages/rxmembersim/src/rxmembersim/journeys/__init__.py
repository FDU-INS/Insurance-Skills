"""RxMemberSim Journey Module.

This module provides journey (temporal event sequence) functionality for RxMemberSim,
built on top of the core HealthSim journey engine.

The module re-exports core journey engine classes and provides RxMemberSim-specific:
- Event handlers for pharmacy/PBM events
- Journey templates for common pharmacy scenarios
- Backward-compatible aliases for migration from scenarios

Usage:
    from rxmembersim.journeys import (
        JourneyEngine,
        JourneySpecification,
        Timeline,
        create_rx_journey_engine,
    )
    
    # Create engine with RxMemberSim handlers pre-registered
    engine = create_rx_journey_engine(seed=42)
    
    # Use a built-in template
    from rxmembersim.journeys.templates import NEW_THERAPY_START
    timeline = engine.create_timeline(rx_member, "rx_member", NEW_THERAPY_START)
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
    RxEventType,
    # Convenience functions
    create_journey_engine,
    create_simple_journey,
    get_journey_template,
    JOURNEY_TEMPLATES,
)

# RxMemberSim-specific exports
from rxmembersim.journeys.handlers import (
    create_rx_journey_engine,
    register_rx_handlers,
)
from rxmembersim.journeys.templates import (
    RX_JOURNEY_TEMPLATES,
    get_rx_journey_template,
    list_rx_journey_templates,
)

# Backward compatibility aliases (deprecated)
from rxmembersim.journeys.compat import (
    RxScenarioEngine,    # -> JourneyEngine
    RxScenarioDefinition, # -> JourneySpecification
    RxTimeline as LegacyRxTimeline,  # -> Timeline
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
    "RxEventType",
    "create_journey_engine",
    "create_simple_journey",
    "get_journey_template",
    "JOURNEY_TEMPLATES",
    # RxMemberSim-specific
    "create_rx_journey_engine",
    "register_rx_handlers",
    "RX_JOURNEY_TEMPLATES",
    "get_rx_journey_template",
    "list_rx_journey_templates",
    # Backward compatibility (deprecated)
    "RxScenarioEngine",
    "RxScenarioDefinition",
    "LegacyRxTimeline",
]
