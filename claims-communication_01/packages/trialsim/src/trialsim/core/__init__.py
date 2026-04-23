"""Core module for TrialSim.

Provides the fundamental generators and models for clinical trial simulation.
"""

from trialsim.core.generator import (
    AdverseEventGenerator,
    ExposureGenerator,
    TrialSubjectGenerator,
    VisitGenerator,
)
from trialsim.core.models import (
    AdverseEvent,
    AECausality,
    AEOutcome,
    AESeverity,
    ArmType,
    Exposure,
    Protocol,
    Site,
    Subject,
    SubjectStatus,
    Visit,
    VisitType,
)

__all__ = [
    # Generators
    "TrialSubjectGenerator",
    "VisitGenerator",
    "AdverseEventGenerator",
    "ExposureGenerator",
    # Models
    "Subject",
    "Site",
    "Protocol",
    "Visit",
    "AdverseEvent",
    "Exposure",
    # Enums
    "ArmType",
    "SubjectStatus",
    "VisitType",
    "AESeverity",
    "AECausality",
    "AEOutcome",
]
