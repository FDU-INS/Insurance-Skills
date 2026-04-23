"""Generic session interfaces for product-specific implementations.

Provides abstract base classes that each product extends:
- PatientSim: PatientSession, PatientSessionManager
- MemberSim: MemberSession, MemberSessionManager
- RxMemberSim: RxMemberSession, RxMemberSessionManager
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

from .entity import EntityWithProvenance
from .provenance import Provenance, ProvenanceSummary
from .workspace import Workspace, WorkspaceMetadata

T = TypeVar("T")  # Primary entity type (Patient, Member, RxMember)


class Session(ABC, Generic[T]):
    """Abstract session containing a primary entity and related data.

    A Session wraps a primary entity (patient, member, etc.) with
    related entities (encounters, claims, prescriptions) and provenance.

    Product implementations:
    - PatientSession: Patient + encounters, diagnoses, labs, vitals, medications
    - MemberSession: Member + claims, authorizations, accumulators
    - RxMemberSession: RxMember + prescriptions, pharmacy_claims, prior_auths
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique session identifier."""
        ...

    @property
    @abstractmethod
    def primary_entity(self) -> T:
        """The primary entity (patient, member, etc.)."""
        ...

    @property
    @abstractmethod
    def provenance(self) -> Provenance:
        """Session provenance."""
        ...

    @abstractmethod
    def to_entities_with_provenance(self) -> dict[str, list[EntityWithProvenance]]:
        """Convert session to serializable entities with provenance.

        Returns:
            Dict mapping entity type to list of EntityWithProvenance
        """
        ...

    @abstractmethod
    def to_summary(self) -> dict[str, Any]:
        """Create summary dict for display.

        Returns:
            Dict with session overview information
        """
        ...


class SessionManager(ABC, Generic[T]):
    """Abstract session manager for workspace operations.

    Manages a collection of sessions and provides workspace
    save/load operations. Products extend this with their
    specific entity types and reconstruction logic.
    """

    @property
    @abstractmethod
    def product_name(self) -> str:
        """Product identifier (patientsim, membersim, rxmembersim)."""
        ...

    @abstractmethod
    def count(self) -> int:
        """Count sessions in workspace."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all sessions."""
        ...

    @abstractmethod
    def get_all(self) -> list[Session[T]]:
        """Get all sessions."""
        ...

    @abstractmethod
    def get_by_id(self, session_id: str) -> Session[T] | None:
        """Get session by ID."""
        ...

    @abstractmethod
    def add(self, entity: T, provenance: Provenance | None = None, **related: Any) -> Session[T]:
        """Add new session with primary entity.

        Args:
            entity: Primary entity (patient, member, etc.)
            provenance: Optional provenance for the entity
            **related: Related entities (encounters, claims, etc.)

        Returns:
            Created session
        """
        ...

    def _get_workspace_dir(self) -> Path | None:
        """Get workspace directory for persistence operations.

        Override in subclass to use a custom directory.
        Returns None to use the default WORKSPACES_DIR.
        """
        return None

    def save_workspace(
        self,
        name: str,
        description: str | None = None,
        tags: list[str] | None = None,
    ) -> Workspace:
        """Save current workspace.

        Args:
            name: Human-readable workspace name
            description: Optional description
            tags: Optional tags for filtering

        Returns:
            Saved Workspace instance
        """
        metadata = WorkspaceMetadata(
            name=name,
            description=description,
            tags=tags or [],
            product=self.product_name,
        )

        # Collect all entities from all sessions
        all_entities: dict[str, list[EntityWithProvenance]] = {}
        for session in self.get_all():
            for entity_type, entities in session.to_entities_with_provenance().items():
                if entity_type not in all_entities:
                    all_entities[entity_type] = []
                all_entities[entity_type].extend(entities)

        # Build provenance summary
        summary = ProvenanceSummary.from_entities(all_entities)

        workspace = Workspace(
            metadata=metadata,
            provenance_summary=summary,
            entities=all_entities,
        )
        workspace.save(directory=self._get_workspace_dir())
        return workspace

    def load_workspace(
        self,
        workspace_id: str | None = None,
        name: str | None = None,
        mode: str = "replace",
    ) -> tuple[Workspace, dict[str, Any]]:
        """Load workspace into session manager.

        Args:
            workspace_id: UUID of workspace to load
            name: Name to search for (if workspace_id not provided)
            mode: "replace" to clear first, "merge" to add to existing

        Returns:
            Tuple of (loaded Workspace, load statistics)

        Raises:
            ValueError: If neither workspace_id nor name provided, or not found
        """
        workspace_dir = self._get_workspace_dir()
        if workspace_id:
            workspace = Workspace.load(workspace_id, directory=workspace_dir)
        elif name:
            workspace = Workspace.find_by_name(name, directory=workspace_dir)
            if not workspace:
                raise ValueError(f"Workspace not found: {name}")
        else:
            raise ValueError("Must provide workspace_id or name")

        if mode == "replace":
            self.clear()

        # Subclass must implement entity reconstruction
        return self._load_entities_from_workspace(workspace)

    @abstractmethod
    def _load_entities_from_workspace(
        self,
        workspace: Workspace,
    ) -> tuple[Workspace, dict[str, Any]]:
        """Product-specific entity reconstruction from workspace.

        Args:
            workspace: Workspace to load entities from

        Returns:
            Tuple of (workspace, load statistics dict)
        """
        ...

    def list_workspaces(
        self,
        search: str | None = None,
        tags: list[str] | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """List saved workspaces for this product.

        Args:
            search: Text to search in name/description
            tags: Required tags (all must match)
            limit: Maximum results to return

        Returns:
            List of workspace summary dicts
        """
        workspaces = Workspace.list_all(
            search=search,
            tags=tags,
            product=self.product_name,
            directory=self._get_workspace_dir(),
        )
        return [
            {
                "workspace_id": w.metadata.workspace_id,
                "name": w.metadata.name,
                "description": w.metadata.description,
                "tags": w.metadata.tags,
                "created_at": w.metadata.created_at.isoformat(),
                "entity_count": w.get_entity_count(),
            }
            for w in workspaces[:limit]
        ]

    def delete_workspace(self, workspace_id: str) -> dict[str, Any] | None:
        """Delete a saved workspace.

        Args:
            workspace_id: UUID or name of workspace to delete

        Returns:
            Info dict about deleted workspace, or None if not found
        """
        workspace_dir = self._get_workspace_dir()
        workspace = None
        try:
            workspace = Workspace.load(workspace_id, directory=workspace_dir)
        except FileNotFoundError:
            # Try by name
            workspace = Workspace.find_by_name(workspace_id, directory=workspace_dir)

        if not workspace:
            return None

        info = {
            "workspace_id": workspace.metadata.workspace_id,
            "name": workspace.metadata.name,
            "entity_count": workspace.get_entity_count(),
        }
        Workspace.delete(workspace.metadata.workspace_id, directory=workspace_dir)
        return info

    def workspace_summary(self) -> dict[str, Any]:
        """Get summary of current workspace state.

        Returns:
            Dict with workspace overview information
        """
        sessions = self.get_all()

        if not sessions:
            return {
                "status": "empty",
                "message": f"No {self.product_name} entities in workspace",
                "entity_count": 0,
            }

        # Collect entity counts by type
        entity_counts: dict[str, int] = {}
        for session in sessions:
            for entity_type, entities in session.to_entities_with_provenance().items():
                entity_counts[entity_type] = entity_counts.get(entity_type, 0) + len(entities)

        return {
            "status": "active",
            "product": self.product_name,
            "session_count": len(sessions),
            "entity_counts": entity_counts,
            "total_entities": sum(entity_counts.values()),
        }
