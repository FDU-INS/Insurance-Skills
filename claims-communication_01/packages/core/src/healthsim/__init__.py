"""HealthSim Core - Shared foundation for HealthSim product family.

This library provides generic infrastructure for building simulation
and synthetic data generation products.

Modules:
    person: Person demographics, identifiers, relationships
    temporal: Timeline management, periods, date utilities
    generation: Base generator, distributions, reproducibility
    validation: Validation framework, results, base validators
    formats: Base transformer, JSON/CSV utilities
    skills: Skill schema, loader, composer
    config: Settings management, logging
    dimensional: Analytics-ready star schema output layer
    state: Workspace persistence, provenance tracking, session management
    benefits: Benefit accumulators, cost sharing infrastructure
"""

__version__ = "1.0.0"

from .benefits import (
    Accumulator,
    AccumulatorLevel,
    AccumulatorSet,
    AccumulatorType,
    BenefitType,
    NetworkTier,
    create_integrated_accumulators,
    create_medical_accumulators,
    create_pharmacy_accumulators,
)
from .dimensional import (
    BaseDimensionalTransformer,
    DuckDBDimensionalWriter,
    generate_dim_date,
)
from .state import (
    WORKSPACES_DIR,
    EntityWithProvenance,
    Provenance,
    ProvenanceSummary,
    Session,
    SessionManager,
    SourceType,
    Workspace,
    WorkspaceMetadata,
)

from .unified_generate import (
    generate,
    quick_sample,
    list_products,
    list_templates,
)

__all__ = [
    "__version__",
    # Unified Generation
    "generate",
    "quick_sample",
    "list_products",
    "list_templates",
    # Benefits
    "Accumulator",
    "AccumulatorLevel",
    "AccumulatorSet",
    "AccumulatorType",
    "BenefitType",
    "NetworkTier",
    "create_medical_accumulators",
    "create_pharmacy_accumulators",
    "create_integrated_accumulators",
    # Dimensional
    "generate_dim_date",
    "BaseDimensionalTransformer",
    "DuckDBDimensionalWriter",
    # State management
    "Provenance",
    "ProvenanceSummary",
    "SourceType",
    "EntityWithProvenance",
    "Workspace",
    "WorkspaceMetadata",
    "WORKSPACES_DIR",
    "Session",
    "SessionManager",
]
