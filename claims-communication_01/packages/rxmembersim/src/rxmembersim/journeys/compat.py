"""Backward compatibility aliases for the scenarios → journeys migration.

This module provides aliases from the old scenario terminology to the new
journey terminology. These aliases are DEPRECATED and will be removed in v2.0.

Migration Guide:
    Old Import                            → New Import
    ------------------------------------- → -----------------------------------------
    from rxmembersim.scenarios import     → from rxmembersim.journeys import
        RxScenarioEngine                  →     JourneyEngine  
        RxScenarioDefinition              →     JourneySpecification
        RxTimeline                        →     Timeline

    from rxmembersim.scenarios.engine import → from rxmembersim.journeys.handlers import
        create_rx_scenario_engine            →     create_rx_journey_engine
"""

import warnings
from typing import Any

from healthsim.generation.journey_engine import (
    JourneyEngine,
    JourneySpecification,
    Timeline,
    TimelineEvent,
    EventDefinition,
    DelaySpec,
)

from pydantic import BaseModel, Field


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue a deprecation warning."""
    warnings.warn(
        f"{old_name} is deprecated and will be removed in v2.0. "
        f"Use {new_name} instead.",
        DeprecationWarning,
        stacklevel=3,
    )


# =============================================================================
# Class Aliases (Deprecated)
# =============================================================================

class RxScenarioDefinition(JourneySpecification):
    """DEPRECATED: Use JourneySpecification instead.
    
    This is a backward-compatible alias that will be removed in v2.0.
    """
    
    def __init__(self, **data: Any) -> None:
        _deprecation_warning("RxScenarioDefinition", "JourneySpecification")
        
        # Map old field names to new ones
        if "scenario_id" in data and "journey_id" not in data:
            data["journey_id"] = data.pop("scenario_id")
        
        super().__init__(**data)


class RxScenarioEngine(JourneyEngine):
    """DEPRECATED: Use JourneyEngine instead.
    
    This is a backward-compatible alias that will be removed in v2.0.
    """
    
    def __init__(self, seed: int | None = None) -> None:
        _deprecation_warning("RxScenarioEngine", "JourneyEngine")
        super().__init__(seed=seed)
    
    def create_timeline(
        self,
        rx_member: Any,
        scenario: "RxScenarioDefinition",
        start_date: Any = None,
        parameters: dict[str, Any] | None = None,
    ) -> "RxTimeline":
        """Create timeline from scenario (maps to journey engine)."""
        timeline = super().create_timeline(
            entity=rx_member,
            entity_type="rx_member",
            journey=scenario,
            start_date=start_date,
            parameters=parameters,
        )
        # Wrap in RxTimeline for backward compatibility
        return RxTimeline._from_timeline(timeline)


class RxTimeline(Timeline):
    """DEPRECATED: Use Timeline instead.
    
    This is a backward-compatible alias that will be removed in v2.0.
    Maintains the old RxTimeline interface for legacy code.
    """
    
    # Alias old field names
    @property
    def member_id(self) -> str:
        """Alias for entity_id."""
        return self.entity_id
    
    @property
    def scenario_ids(self) -> list[str]:
        """Alias for journey_ids."""
        return self.journey_ids
    
    @classmethod
    def _from_timeline(cls, timeline: Timeline) -> "RxTimeline":
        """Create RxTimeline from Timeline."""
        rt = cls(
            entity_id=timeline.entity_id,
            entity_type=timeline.entity_type,
            journey_ids=timeline.journey_ids,
            start_date=timeline.start_date,
            end_date=timeline.end_date,
        )
        rt.events = timeline.events
        rt.linked_timelines = timeline.linked_timelines
        return rt
    
    def get_events_by_type(self, event_type: str) -> list[TimelineEvent]:
        """Get all events of a specific type (legacy method)."""
        return [e for e in self.events if e.event_type == event_type]
    
    def get_events_for_drug(self, ndc: str) -> list[TimelineEvent]:
        """Get all events for a specific drug (legacy method)."""
        return [
            e for e in self.events 
            if e.result.get("ndc") == ndc or e.result.get("parameters", {}).get("ndc") == ndc
        ]


# =============================================================================
# Function Aliases (Deprecated)
# =============================================================================

def create_rx_scenario_engine(seed: int | None = None) -> RxScenarioEngine:
    """DEPRECATED: Use create_rx_journey_engine instead."""
    _deprecation_warning("create_rx_scenario_engine", "create_rx_journey_engine")
    from rxmembersim.journeys.handlers import create_rx_journey_engine
    
    engine = create_rx_journey_engine(seed)
    # Wrap in RxScenarioEngine for type compatibility
    wrapped = RxScenarioEngine.__new__(RxScenarioEngine)
    wrapped.__dict__.update(engine.__dict__)
    return wrapped


__all__ = [
    # Deprecated class aliases
    "RxScenarioDefinition",
    "RxScenarioEngine", 
    "RxTimeline",
    # Deprecated function aliases
    "create_rx_scenario_engine",
]
