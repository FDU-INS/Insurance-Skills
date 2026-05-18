"""Backward compatibility aliases for TrialSim journeys.

This module provides deprecated aliases for migration from older terminology.
New code should use the journey-based naming directly.

Deprecation Notice:
    These aliases will be removed in v2.0. Please migrate to:
    - ProtocolDefinition -> JourneySpecification
    - ProtocolEngine -> JourneyEngine
    - SubjectTimeline -> Timeline
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


class ProtocolDefinition(JourneySpecification):
    """Deprecated: Use JourneySpecification instead."""
    
    def __init__(self, **kwargs):
        _deprecation_warning("ProtocolDefinition", "JourneySpecification")
        super().__init__(**kwargs)


class ProtocolEngine(JourneyEngine):
    """Deprecated: Use JourneyEngine instead."""
    
    def __init__(self, seed: int | None = None):
        _deprecation_warning("ProtocolEngine", "JourneyEngine")
        super().__init__(seed)


class SubjectTimeline(Timeline):
    """Deprecated: Use Timeline instead."""
    
    def __init__(self, **kwargs):
        _deprecation_warning("SubjectTimeline", "Timeline")
        super().__init__(**kwargs)


class ProtocolEvent(EventDefinition):
    """Deprecated: Use EventDefinition instead."""
    
    def __init__(self, **kwargs):
        _deprecation_warning("ProtocolEvent", "EventDefinition")
        super().__init__(**kwargs)


class VisitSchedule(DelaySpec):
    """Deprecated: Use DelaySpec instead."""
    
    def __init__(self, **kwargs):
        _deprecation_warning("VisitSchedule", "DelaySpec")
        super().__init__(**kwargs)


# Type alias for backward compatibility
ProtocolMetadata = dict[str, Any]


class ProtocolLibrary:
    """Deprecated: Use TRIAL_JOURNEY_TEMPLATES dict instead.
    
    This class wraps the templates dict for backward compatibility.
    """
    
    def __init__(self):
        _deprecation_warning("ProtocolLibrary", "TRIAL_JOURNEY_TEMPLATES")
        from trialsim.journeys.templates import TRIAL_JOURNEY_TEMPLATES
        self._templates = TRIAL_JOURNEY_TEMPLATES
    
    def get(self, protocol_id: str) -> dict | None:
        """Get a protocol/journey template by ID."""
        return self._templates.get(protocol_id)
    
    def list(self) -> list[str]:
        """List available protocol/journey IDs."""
        return list(self._templates.keys())
    
    def __getitem__(self, key: str) -> dict:
        """Get a protocol/journey template by ID."""
        return self._templates[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if a protocol/journey exists."""
        return key in self._templates


__all__ = [
    "ProtocolDefinition",
    "ProtocolEngine",
    "ProtocolMetadata",
    "ProtocolEvent",
    "VisitSchedule",
    "SubjectTimeline",
    "ProtocolLibrary",
]
