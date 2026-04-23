"""RxMemberSim - Synthetic pharmacy benefit data generation."""

from rxmembersim.claims import (
    AdjudicationEngine,
    ClaimResponse,
    PharmacyClaim,
    TransactionCode,
)
from rxmembersim.core import (
    BenefitAccumulators,
    DrugReference,
    Pharmacy,
    Prescriber,
    Prescription,
    RxMember,
    RxMemberFactory,
    RxMemberGenerator,
)
from rxmembersim.dimensional import RxMemberSimDimensionalTransformer
from rxmembersim.formulary import (
    Formulary,
    FormularyGenerator,
    StepTherapyManager,
)

# Journey module (new API)
from rxmembersim.journeys import (
    # Core journey classes
    JourneyEngine,
    JourneySpecification,
    Timeline,
    TimelineEvent,
    EventDefinition,
    DelaySpec,
    EventCondition,
    RxEventType,
    # RxMemberSim-specific
    create_rx_journey_engine,
    RX_JOURNEY_TEMPLATES,
    get_rx_journey_template,
    # Backward compatibility aliases (deprecated)
    RxScenarioEngine,
    RxScenarioDefinition,
    LegacyRxTimeline,
)

# Legacy aliases for backward compatibility
BUILTIN_SCENARIOS = RX_JOURNEY_TEMPLATES
create_default_engine = create_rx_journey_engine
RxTimeline = LegacyRxTimeline


__version__ = "1.1.0"

__all__ = [
    # Core models
    "RxMember",
    "RxMemberFactory",
    "RxMemberGenerator",
    "BenefitAccumulators",
    "Prescription",
    "DrugReference",
    "Pharmacy",
    "Prescriber",
    # Claims
    "PharmacyClaim",
    "TransactionCode",
    "AdjudicationEngine",
    "ClaimResponse",
    # Formulary
    "Formulary",
    "FormularyGenerator",
    "StepTherapyManager",
    # Journey API (new)
    "JourneyEngine",
    "JourneySpecification",
    "Timeline",
    "TimelineEvent",
    "EventDefinition",
    "DelaySpec",
    "EventCondition",
    "RxEventType",
    "create_rx_journey_engine",
    "RX_JOURNEY_TEMPLATES",
    "get_rx_journey_template",
    # Backward compatibility (deprecated)
    "RxScenarioDefinition",
    "RxScenarioEngine",
    "RxTimeline",
    "create_default_engine",
    "BUILTIN_SCENARIOS",
    # Dimensional
    "RxMemberSimDimensionalTransformer",
]
