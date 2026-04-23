"""MemberSim - Synthetic health plan member data generation."""

from membersim.claims.claim import Claim, ClaimLine
from membersim.claims.payment import LinePayment, Payment
from membersim.core.accumulator import Accumulator
from membersim.core.member import Member, MemberGenerator
from membersim.core.plan import SAMPLE_PLANS, Plan
from membersim.core.provider import Provider
from membersim.core.subscriber import Subscriber
from membersim.dimensional import MemberSimDimensionalTransformer
from membersim.generation import (
    AgeDistribution,
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
    NormalDistribution,
    SeedManager,
    UniformDistribution,
    WeightedChoice,
)

# Journey module (new API)
from membersim.journeys import (
    # Core journey classes
    JourneyEngine,
    JourneySpecification,
    Timeline,
    TimelineEvent,
    EventDefinition,
    DelaySpec,
    EventCondition,
    MemberEventType,
    # MemberSim-specific
    create_member_journey_engine,
    MEMBER_JOURNEY_TEMPLATES,
    get_member_journey_template,
    # Backward compatibility aliases (deprecated)
    ScenarioDefinition,
    ScenarioEngine,
    MemberTimeline,
    ScenarioLibrary,
    EventDelay,
)

# Legacy alias for backward compatibility
BUILTIN_SCENARIOS = MEMBER_JOURNEY_TEMPLATES
create_default_engine = create_member_journey_engine


def register_builtin_scenarios() -> None:
    """DEPRECATED: Journey templates are auto-loaded. This is a no-op."""
    pass


__version__ = "0.1.0"

__all__ = [
    # Core models
    "Member",
    "MemberGenerator",
    "Subscriber",
    "Plan",
    "SAMPLE_PLANS",
    "Provider",
    "Accumulator",
    # Claims
    "Claim",
    "ClaimLine",
    "Payment",
    "LinePayment",
    # Dimensional
    "MemberSimDimensionalTransformer",
    # Generation
    "WeightedChoice",
    "UniformDistribution",
    "NormalDistribution",
    "AgeDistribution",
    "SeedManager",
    "CohortConstraints",
    "CohortProgress",
    "CohortGenerator",
    # Journey API (new)
    "JourneyEngine",
    "JourneySpecification",
    "Timeline",
    "TimelineEvent",
    "EventDefinition",
    "DelaySpec",
    "EventCondition",
    "MemberEventType",
    "create_member_journey_engine",
    "MEMBER_JOURNEY_TEMPLATES",
    "get_member_journey_template",
    # Backward compatibility (deprecated)
    "ScenarioDefinition",
    "ScenarioLibrary",
    "ScenarioEngine",
    "MemberTimeline",
    "EventDelay",
    "create_default_engine",
    "register_builtin_scenarios",
    "BUILTIN_SCENARIOS",
]
