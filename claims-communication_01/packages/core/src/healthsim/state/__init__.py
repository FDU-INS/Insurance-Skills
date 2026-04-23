"""State management for HealthSim products.

This module provides the foundational classes for workspace persistence
and entity provenance tracking across all HealthSim products:

- PatientSim: Clinical patient data
- MemberSim: Health plan member and claims data
- RxMemberSim: Pharmacy benefit and prescription data

Core Classes:
    Provenance: Tracks entity lineage (loaded, generated, derived)
    ProvenanceSummary: Aggregate statistics for workspace provenance
    SourceType: Enum of provenance source types
    EntityWithProvenance: Generic entity wrapper with provenance
    Workspace: Saved collection of entities
    WorkspaceMetadata: Workspace descriptive information
    Session: Abstract base for product-specific sessions
    SessionManager: Abstract base for workspace operations

Auto-Persist Classes (Structured RAG Pattern):
    AutoPersistService: Main service for auto-persistence
    PersistResult: Result of entity persistence
    QueryResult: Paginated query results
    CohortSummary: Token-efficient cohort summary
    CohortBrief: Brief cohort info for listing

Usage:
    Products extend Session and SessionManager with their entity types:

    ```python
    from healthsim.state import Session, SessionManager, Provenance

    class PatientSession(Session[Patient]):
        # PatientSim-specific implementation
        ...

    class PatientSessionManager(SessionManager[Patient]):
        @property
        def product_name(self) -> str:
            return "patientsim"
        ...
    ```

    For auto-persist (recommended for token efficiency):

    ```python
    from healthsim.state import persist, get_summary, query_cohort

    # Persist entities - returns summary, not full data
    result = persist({'patients': patient_list}, context='diabetes cohort')
    
    # Load summary (~500 tokens instead of full data)
    summary = get_summary('diabetes-cohort-20241227')
    
    # Query for specific data with pagination
    results = query_cohort(cohort_id, "SELECT * FROM patients WHERE gender = 'F'")
    ```
"""

from .entity import EntityWithProvenance
from .provenance import Provenance, ProvenanceSummary, SourceType
from .session import Session, SessionManager
from .workspace import WORKSPACES_DIR, Workspace, WorkspaceMetadata
from .manager import (
    StateManager,
    get_manager,
    reset_manager,
    # Traditional methods (full data)
    save_cohort,
    load_cohort,
    list_cohorts,
    delete_cohort,
    cohort_exists,
    export_cohort_to_json,
    import_cohort_from_json,
    # Auto-persist convenience functions
    persist,
    get_summary,
    query_cohort,
)
from .legacy import (
    export_to_json,
    import_from_json,
    list_legacy_cohorts,
    migrate_legacy_cohort,
    migrate_all_legacy_cohorts,
    LEGACY_COHORTS_PATH,
)

# Auto-persist (Structured RAG Pattern)
from .auto_naming import (
    generate_cohort_name,
    extract_keywords,
    ensure_unique_name,
    sanitize_name,
    parse_cohort_name,
)
from .summary import (
    CohortSummary,
    generate_summary,
    get_cohort_by_name,
)
from .auto_persist import (
    AutoPersistService,
    PersistResult,
    QueryResult,
    CohortBrief,
    get_auto_persist_service,
    reset_service,
)

# Profile persistence
from .profile_manager import (
    ProfileManager,
    ProfileRecord,
    ProfileSummary,
    ExecutionRecord,
    get_profile_manager,
)

# Journey persistence
from .journey_manager import (
    JourneyManager,
    JourneyRecord,
    JourneySummary,
    JourneyExecutionRecord,
    get_journey_manager,
)

__all__ = [
    # Provenance
    "Provenance",
    "ProvenanceSummary",
    "SourceType",
    # Entity
    "EntityWithProvenance",
    # Workspace (file-based)
    "Workspace",
    "WorkspaceMetadata",
    "WORKSPACES_DIR",
    # Session (abstract)
    "Session",
    "SessionManager",
    # State Manager (DuckDB-backed)
    "StateManager",
    "get_manager",
    "reset_manager",
    # Traditional methods (full data in context)
    "save_cohort",
    "load_cohort",
    "list_cohorts",
    "delete_cohort",
    "cohort_exists",
    "export_cohort_to_json",
    "import_cohort_from_json",
    # Auto-persist convenience functions (token-efficient)
    "persist",
    "get_summary",
    "query_cohort",
    # Legacy JSON support
    "export_to_json",
    "import_from_json",
    "list_legacy_cohorts",
    "migrate_legacy_cohort",
    "migrate_all_legacy_cohorts",
    "LEGACY_COHORTS_PATH",
    # Auto-Naming
    "generate_cohort_name",
    "extract_keywords",
    "ensure_unique_name",
    "sanitize_name",
    "parse_cohort_name",
    # Summary
    "CohortSummary",
    "generate_summary",
    "get_cohort_by_name",
    # Auto-Persist Service
    "AutoPersistService",
    "PersistResult",
    "QueryResult",
    "CohortBrief",
    "get_auto_persist_service",
    "reset_service",
    # Profile Persistence
    "ProfileManager",
    "ProfileRecord",
    "ProfileSummary",
    "ExecutionRecord",
    "get_profile_manager",
    # Journey Persistence
    "JourneyManager",
    "JourneyRecord",
    "JourneySummary",
    "JourneyExecutionRecord",
    "get_journey_manager",
]
