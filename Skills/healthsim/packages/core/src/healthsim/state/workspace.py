"""Workspace persistence for cross-product state management.

A Workspace represents a saved collection of entities (patients, members, etc.)
that can be persisted to disk and loaded later. Replaces the PatientSim-specific
"Scenario" concept with a product-agnostic design.
"""

from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from .entity import EntityWithProvenance
from .provenance import ProvenanceSummary

# Default storage location (cross-product)
WORKSPACES_DIR = Path.home() / ".healthsim" / "workspaces"


class WorkspaceMetadata(BaseModel):
    """Metadata for a saved workspace.

    Attributes:
        workspace_id: Unique identifier (UUID)
        name: Human-readable name
        description: Optional description
        tags: Optional tags for filtering
        created_at: Creation timestamp
        updated_at: Last update timestamp
        product: Source product identifier
        schema_version: Data format version
    """

    workspace_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    product: str = "unknown"  # "patientsim", "membersim", "rxmembersim"
    schema_version: str = "2.0"


class Workspace(BaseModel):
    """A complete saved workspace with entities and provenance.

    Workspaces are product-agnostic containers that can hold entities
    from any HealthSim product. The entities dict maps entity types
    (e.g., "patients", "members") to lists of EntityWithProvenance.
    """

    metadata: WorkspaceMetadata
    provenance_summary: ProvenanceSummary = Field(default_factory=ProvenanceSummary)
    entities: dict[str, list[EntityWithProvenance]] = Field(default_factory=dict)

    def save(self, directory: Path | None = None) -> Path:
        """Save workspace to disk.

        Uses atomic write (temp file + rename) for safety.

        Args:
            directory: Optional custom directory (defaults to WORKSPACES_DIR)

        Returns:
            Path to the saved file
        """
        save_dir = directory or WORKSPACES_DIR
        save_dir.mkdir(parents=True, exist_ok=True)
        file_path = save_dir / f"{self.metadata.workspace_id}.json"
        temp_path = file_path.with_suffix(".tmp")
        temp_path.write_text(self.model_dump_json(indent=2))
        temp_path.rename(file_path)
        return file_path

    @classmethod
    def load(cls, workspace_id: str, directory: Path | None = None) -> "Workspace":
        """Load workspace from disk by ID.

        Args:
            workspace_id: UUID of the workspace to load
            directory: Optional custom directory

        Returns:
            Loaded Workspace instance

        Raises:
            FileNotFoundError: If workspace file doesn't exist
        """
        load_dir = directory or WORKSPACES_DIR
        file_path = load_dir / f"{workspace_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Workspace not found: {workspace_id}")
        return cls.model_validate_json(file_path.read_text())

    @classmethod
    def find_by_name(cls, name: str, directory: Path | None = None) -> "Workspace | None":
        """Find workspace by name (case-insensitive partial match).

        Args:
            name: Name or partial name to search for
            directory: Optional custom directory

        Returns:
            First matching Workspace or None
        """
        load_dir = directory or WORKSPACES_DIR
        if not load_dir.exists():
            return None
        for file_path in load_dir.glob("*.json"):
            try:
                workspace = cls.model_validate_json(file_path.read_text())
                if name.lower() in workspace.metadata.name.lower():
                    return workspace
            except Exception:
                continue
        return None

    @classmethod
    def list_all(
        cls,
        search: str | None = None,
        tags: list[str] | None = None,
        product: str | None = None,
        directory: Path | None = None,
    ) -> list["Workspace"]:
        """List all workspaces with optional filters.

        Args:
            search: Text to search in name/description
            tags: Required tags (all must match)
            product: Filter by product name
            directory: Optional custom directory

        Returns:
            List of matching Workspaces, sorted by created_at descending
        """
        load_dir = directory or WORKSPACES_DIR
        if not load_dir.exists():
            return []

        workspaces = []
        for file_path in load_dir.glob("*.json"):
            try:
                ws = cls.model_validate_json(file_path.read_text())

                # Filter by product
                if product and ws.metadata.product != product:
                    continue

                # Filter by search
                if search:
                    search_lower = search.lower()
                    name_match = search_lower in ws.metadata.name.lower()
                    desc_match = (
                        ws.metadata.description and search_lower in ws.metadata.description.lower()
                    )
                    if not (name_match or desc_match):
                        continue

                # Filter by tags
                if tags and not all(t in ws.metadata.tags for t in tags):
                    continue

                workspaces.append(ws)
            except Exception:
                continue

        return sorted(workspaces, key=lambda w: w.metadata.created_at, reverse=True)

    @classmethod
    def delete(cls, workspace_id: str, directory: Path | None = None) -> bool:
        """Delete workspace file.

        Args:
            workspace_id: UUID of workspace to delete
            directory: Optional custom directory

        Returns:
            True if deleted, False if not found
        """
        load_dir = directory or WORKSPACES_DIR
        file_path = load_dir / f"{workspace_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def get_entity_count(self, entity_type: str | None = None) -> int:
        """Count entities, optionally by type.

        Args:
            entity_type: Optional type to filter by

        Returns:
            Number of entities
        """
        if entity_type:
            return len(self.entities.get(entity_type, []))
        return sum(len(entities) for entities in self.entities.values())

    def get_entity_types(self) -> list[str]:
        """Get list of entity types in this workspace.

        Returns:
            List of entity type names with non-zero counts
        """
        return [k for k, v in self.entities.items() if v]

    def add_entities(
        self,
        entity_type: str,
        entities: list[EntityWithProvenance],
    ) -> None:
        """Add entities to the workspace.

        Args:
            entity_type: Type category for the entities
            entities: List of entities to add
        """
        if entity_type not in self.entities:
            self.entities[entity_type] = []
        self.entities[entity_type].extend(entities)
        self.metadata.updated_at = datetime.now()

    def to_summary(self) -> dict[str, Any]:
        """Create summary dict for display.

        Returns:
            Dict with workspace overview information
        """
        return {
            "workspace_id": self.metadata.workspace_id,
            "name": self.metadata.name,
            "description": self.metadata.description,
            "product": self.metadata.product,
            "tags": self.metadata.tags,
            "created_at": self.metadata.created_at.isoformat(),
            "updated_at": self.metadata.updated_at.isoformat(),
            "entity_counts": {k: len(v) for k, v in self.entities.items()},
            "total_entities": self.get_entity_count(),
            "provenance": {
                "total": self.provenance_summary.total_entities,
                "by_source": self.provenance_summary.by_source_type,
                "skills_used": self.provenance_summary.skills_used,
            },
        }
