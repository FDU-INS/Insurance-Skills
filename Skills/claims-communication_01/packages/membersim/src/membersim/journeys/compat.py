"""Backward compatibility aliases for the scenarios → journeys migration.

This module provides aliases from the old scenario terminology to the new
journey terminology. These aliases are DEPRECATED and will be removed in v2.0.

Migration Guide:
    Old Import                          → New Import
    ----------------------------------- → -----------------------------------------
    from membersim.scenarios import     → from membersim.journeys import
        ScenarioDefinition              →     JourneySpecification
        ScenarioEngine                  →     JourneyEngine  
        ScenarioMetadata                →     (use JourneySpecification fields)
        ScenarioEvent                   →     EventDefinition
        EventDelay                      →     DelaySpec
        MemberTimeline                  →     Timeline

    from membersim.scenarios.engine import → from membersim.journeys.handlers import
        create_default_engine              →     create_member_journey_engine
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
    EventCondition,
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

class ScenarioDefinition(JourneySpecification):
    """DEPRECATED: Use JourneySpecification instead.
    
    This is a backward-compatible alias that will be removed in v2.0.
    """
    
    def __init__(self, **data: Any) -> None:
        _deprecation_warning("ScenarioDefinition", "JourneySpecification")
        
        # Map old field names to new ones
        if "scenario_id" in data and "journey_id" not in data:
            data["journey_id"] = data.pop("scenario_id")
        
        super().__init__(**data)


class ScenarioEngine(JourneyEngine):
    """DEPRECATED: Use JourneyEngine instead.
    
    This is a backward-compatible alias that will be removed in v2.0.
    """
    
    def __init__(self, seed: int | None = None) -> None:
        _deprecation_warning("ScenarioEngine", "JourneyEngine")
        super().__init__(seed=seed)
    
    def create_timeline(
        self,
        member: Any,
        scenario: "ScenarioDefinition",
        start_date: Any = None,
        parameters: dict[str, Any] | None = None,
    ) -> "MemberTimeline":
        """Create timeline from scenario (maps to journey engine)."""
        timeline = super().create_timeline(
            entity=member,
            entity_type="member",
            journey=scenario,
            start_date=start_date,
            parameters=parameters,
        )
        # Wrap in MemberTimeline for backward compatibility
        return MemberTimeline._from_timeline(timeline)


class ScenarioMetadata(BaseModel):
    """DEPRECATED: Use JourneySpecification fields instead.
    
    This class is a backward-compatible wrapper. In the new API,
    metadata is embedded directly in JourneySpecification.
    """
    
    scenario_id: str = Field(..., description="Unique scenario identifier")
    name: str = Field(..., description="Human-readable name")
    description: str = Field("", description="Detailed description")
    category: str = Field("general", description="Scenario category")
    version: str = Field("1.0", description="Scenario version")
    author: str = Field("MemberSim", description="Scenario author")
    
    applicable_plan_types: list[str] = Field(default_factory=list)
    applicable_populations: list[str] = Field(default_factory=list)
    
    typical_duration_days: int = Field(365)
    expected_claims: int = Field(5)
    expected_cost_range: tuple = Field((1000, 5000))
    
    def __init__(self, **data: Any) -> None:
        _deprecation_warning("ScenarioMetadata", "JourneySpecification fields")
        super().__init__(**data)


class ScenarioEvent(EventDefinition):
    """DEPRECATED: Use EventDefinition instead.
    
    This is a backward-compatible alias that will be removed in v2.0.
    """
    
    def __init__(self, **data: Any) -> None:
        _deprecation_warning("ScenarioEvent", "EventDefinition")
        
        # Map old field names to new ones
        if "params" in data and "parameters" not in data:
            data["parameters"] = data.pop("params")
        
        super().__init__(**data)


class EventDelay(DelaySpec):
    """DEPRECATED: Use DelaySpec instead.
    
    This is a backward-compatible alias that will be removed in v2.0.
    """
    
    def __init__(self, **data: Any) -> None:
        _deprecation_warning("EventDelay", "DelaySpec")
        
        # Map old field names
        if "value" in data and "days" not in data:
            data["days"] = data.pop("value")
        if "min_value" in data and "days_min" not in data:
            data["days_min"] = data.pop("min_value")
        if "max_value" in data and "days_max" not in data:
            data["days_max"] = data.pop("max_value")
        
        super().__init__(**data)


class MemberTimeline(Timeline):
    """DEPRECATED: Use Timeline instead.
    
    This is a backward-compatible alias that will be removed in v2.0.
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
    def _from_timeline(cls, timeline: Timeline) -> "MemberTimeline":
        """Create MemberTimeline from Timeline."""
        mt = cls(
            entity_id=timeline.entity_id,
            entity_type=timeline.entity_type,
            journey_ids=timeline.journey_ids,
            start_date=timeline.start_date,
            end_date=timeline.end_date,
        )
        mt.events = timeline.events
        mt.linked_timelines = timeline.linked_timelines
        return mt


class ScenarioLibrary:
    """DEPRECATED: Use MEMBER_JOURNEY_TEMPLATES dict instead.
    
    This class provided a registry of scenario definitions.
    Use the templates module instead.
    """
    
    _scenarios: dict[str, ScenarioDefinition] = {}
    
    @classmethod
    def register(cls, scenario: ScenarioDefinition) -> None:
        """Register a scenario definition."""
        _deprecation_warning("ScenarioLibrary.register", "MEMBER_JOURNEY_TEMPLATES dict")
        cls._scenarios[scenario.journey_id] = scenario
    
    @classmethod
    def get(cls, scenario_id: str) -> ScenarioDefinition | None:
        """Get a scenario by ID."""
        _deprecation_warning("ScenarioLibrary.get", "get_member_journey_template")
        return cls._scenarios.get(scenario_id)
    
    @classmethod
    def list_all(cls) -> list[str]:
        """List all registered scenario IDs."""
        _deprecation_warning("ScenarioLibrary.list_all", "list_member_journey_templates")
        return list(cls._scenarios.keys())


# =============================================================================
# Function Aliases (Deprecated)
# =============================================================================

def create_default_engine(seed: int | None = None) -> ScenarioEngine:
    """DEPRECATED: Use create_member_journey_engine instead."""
    _deprecation_warning("create_default_engine", "create_member_journey_engine")
    from membersim.journeys.handlers import create_member_journey_engine
    
    engine = create_member_journey_engine(seed)
    # Wrap in ScenarioEngine for type compatibility
    wrapped = ScenarioEngine.__new__(ScenarioEngine)
    wrapped.__dict__.update(engine.__dict__)
    return wrapped


__all__ = [
    # Deprecated class aliases
    "ScenarioDefinition",
    "ScenarioEngine", 
    "ScenarioMetadata",
    "ScenarioEvent",
    "EventDelay",
    "MemberTimeline",
    "ScenarioLibrary",
    # Deprecated function aliases
    "create_default_engine",
]
