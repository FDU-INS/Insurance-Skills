"""Backward compatibility aliases for PatientSim journeys.

This module provides deprecated aliases for migration from older terminology.
New code should use the journey-based naming directly.

Deprecation Notice:
    These aliases will be removed in v2.0. Please migrate to:
    - ScenarioDefinition -> JourneySpecification
    - ScenarioEngine -> JourneyEngine
    - PatientTimeline -> Timeline
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


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue a deprecation warning."""
    warnings.warn(
        f"{old_name} is deprecated and will be removed in v2.0. "
        f"Use {new_name} instead.",
        DeprecationWarning,
        stacklevel=3,
    )


class ScenarioDefinition(JourneySpecification):
    """Deprecated: Use JourneySpecification instead."""
    
    def __init__(self, **kwargs):
        _deprecation_warning("ScenarioDefinition", "JourneySpecification")
        super().__init__(**kwargs)


class ScenarioEngine(JourneyEngine):
    """Deprecated: Use JourneyEngine instead."""
    
    def __init__(self, seed: int | None = None):
        _deprecation_warning("ScenarioEngine", "JourneyEngine")
        super().__init__(seed)


class PatientTimeline(Timeline):
    """Deprecated: Use Timeline instead."""
    
    def __init__(self, **kwargs):
        _deprecation_warning("PatientTimeline", "Timeline")
        super().__init__(**kwargs)


class ScenarioEvent(EventDefinition):
    """Deprecated: Use EventDefinition instead."""
    
    def __init__(self, **kwargs):
        _deprecation_warning("ScenarioEvent", "EventDefinition")
        super().__init__(**kwargs)


class EventDelay(DelaySpec):
    """Deprecated: Use DelaySpec instead."""
    
    def __init__(self, **kwargs):
        _deprecation_warning("EventDelay", "DelaySpec")
        super().__init__(**kwargs)


# Type alias for backward compatibility
ScenarioMetadata = dict[str, Any]


class ScenarioLibrary:
    """Deprecated: Use PATIENT_JOURNEY_TEMPLATES dict instead.
    
    This class wraps the templates dict for backward compatibility.
    """
    
    def __init__(self):
        _deprecation_warning("ScenarioLibrary", "PATIENT_JOURNEY_TEMPLATES")
        from patientsim.journeys.templates import PATIENT_JOURNEY_TEMPLATES
        self._templates = PATIENT_JOURNEY_TEMPLATES
    
    def get(self, scenario_id: str) -> dict | None:
        """Get a scenario/journey template by ID."""
        return self._templates.get(scenario_id)
    
    def list(self) -> list[str]:
        """List available scenario/journey IDs."""
        return list(self._templates.keys())
    
    def __getitem__(self, key: str) -> dict:
        """Get a scenario/journey template by ID."""
        return self._templates[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if a scenario/journey exists."""
        return key in self._templates


__all__ = [
    "ScenarioDefinition",
    "ScenarioEngine",
    "ScenarioMetadata",
    "ScenarioEvent",
    "EventDelay",
    "PatientTimeline",
    "ScenarioLibrary",
]
