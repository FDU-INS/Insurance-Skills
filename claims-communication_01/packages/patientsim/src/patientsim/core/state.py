"""State management models for PatientSim.

This module re-exports state management classes from healthsim-core,
providing backwards compatibility for PatientSim code.

The core classes (Provenance, EntityWithProvenance, etc.) are now
defined in healthsim.state and shared across all HealthSim products.

PatientSim-specific aliases:
- Scenario -> Workspace (cross-product term)
- ScenarioMetadata -> WorkspaceMetadata (cross-product term)
- SCENARIOS_DIR -> WORKSPACES_DIR (cross-product location)
"""

from pathlib import Path

# Re-export core classes from healthsim.state
from healthsim.state import (
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

# Legacy aliases for backwards compatibility
Scenario = Workspace
ScenarioMetadata = WorkspaceMetadata

# Legacy location (deprecated, use WORKSPACES_DIR)
SCENARIOS_DIR = Path.home() / ".healthsim" / "scenarios"

__all__ = [
    # Core types (from healthsim.state)
    "SourceType",
    "Provenance",
    "ProvenanceSummary",
    "EntityWithProvenance",
    "Session",
    "SessionManager",
    # Cross-product names
    "Workspace",
    "WorkspaceMetadata",
    "WORKSPACES_DIR",
    # Legacy aliases (deprecated, use cross-product names)
    "Scenario",
    "ScenarioMetadata",
    "SCENARIOS_DIR",
]
