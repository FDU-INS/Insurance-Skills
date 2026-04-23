"""Tests for Session and SessionManager abstract interfaces."""

from typing import Any
from uuid import uuid4

import pytest

from healthsim.state import (
    EntityWithProvenance,
    Provenance,
    Session,
    SessionManager,
    Workspace,
)


class MockEntity:
    """Mock entity for testing."""

    def __init__(self, entity_id: str, name: str):
        self.id = entity_id
        self.name = name

    def model_dump(self) -> dict:
        return {"id": self.id, "name": self.name}


class MockSession(Session[MockEntity]):
    """Concrete Session implementation for testing."""

    def __init__(
        self,
        entity: MockEntity,
        related_items: list[dict] | None = None,
        provenance: Provenance | None = None,
    ):
        self._id = str(uuid4())[:8]
        self._entity = entity
        self.related_items = related_items or []
        self._provenance = provenance or Provenance.generated()

    @property
    def id(self) -> str:
        return self._id

    @property
    def primary_entity(self) -> MockEntity:
        return self._entity

    @property
    def provenance(self) -> Provenance:
        return self._provenance

    def to_entities_with_provenance(self) -> dict[str, list[EntityWithProvenance]]:
        entities = {
            "mock_entities": [
                EntityWithProvenance(
                    entity_id=self._entity.id,
                    entity_type="mock_entities",
                    data=self._entity.model_dump(),
                    provenance=self._provenance,
                )
            ]
        }
        if self.related_items:
            entities["related_items"] = [
                EntityWithProvenance(
                    entity_id=item.get("id", str(uuid4())),
                    entity_type="related_items",
                    data=item,
                    provenance=self._provenance,
                )
                for item in self.related_items
            ]
        return entities

    def to_summary(self) -> dict[str, Any]:
        return {
            "id": self._id,
            "entity_name": self._entity.name,
            "related_count": len(self.related_items),
        }


class MockSessionManager(SessionManager[MockEntity]):
    """Concrete SessionManager implementation for testing."""

    def __init__(self, workspace_dir=None):
        self._sessions: list[MockSession] = []
        self._workspace_dir = workspace_dir

    def _get_workspace_dir(self):
        """Return custom workspace directory for testing."""
        return self._workspace_dir

    @property
    def product_name(self) -> str:
        return "mocksim"

    def count(self) -> int:
        return len(self._sessions)

    def clear(self) -> None:
        self._sessions = []

    def get_all(self) -> list[Session[MockEntity]]:
        return self._sessions

    def get_by_id(self, session_id: str) -> Session[MockEntity] | None:
        for session in self._sessions:
            if session.id == session_id:
                return session
        return None

    def add(
        self,
        entity: MockEntity,
        provenance: Provenance | None = None,
        **related: Any,
    ) -> Session[MockEntity]:
        session = MockSession(
            entity=entity,
            related_items=related.get("related_items"),
            provenance=provenance,
        )
        self._sessions.append(session)
        return session

    def _load_entities_from_workspace(
        self,
        workspace: Workspace,
    ) -> tuple[Workspace, dict[str, Any]]:
        stats = {"loaded": 0, "skipped": 0}

        mock_entities = workspace.entities.get("mock_entities", [])
        for entity_data in mock_entities:
            entity = MockEntity(
                entity_id=entity_data.data["id"],
                name=entity_data.data["name"],
            )
            # Get related items
            related = workspace.entities.get("related_items", [])
            self.add(
                entity,
                provenance=entity_data.provenance,
                related_items=[r.data for r in related],
            )
            stats["loaded"] += 1

        return workspace, stats


@pytest.fixture
def temp_workspace_dir(tmp_path):
    """Create temporary workspace directory."""
    workspace_dir = tmp_path / "workspaces"
    workspace_dir.mkdir()
    return workspace_dir


@pytest.fixture
def session_manager(temp_workspace_dir):
    """Create a MockSessionManager with temp directory."""
    return MockSessionManager(workspace_dir=temp_workspace_dir)


class TestSession:
    """Tests for Session abstract interface."""

    def test_session_properties(self):
        """Test session has required properties."""
        entity = MockEntity("e1", "Test Entity")
        session = MockSession(entity)

        assert session.id  # Should have ID
        assert session.primary_entity == entity
        assert session.provenance is not None

    def test_session_to_entities_with_provenance(self):
        """Test session converts to entities with provenance."""
        entity = MockEntity("e1", "Test Entity")
        related = [{"id": "r1", "value": 1}, {"id": "r2", "value": 2}]
        session = MockSession(entity, related_items=related)

        entities = session.to_entities_with_provenance()

        assert "mock_entities" in entities
        assert len(entities["mock_entities"]) == 1
        assert entities["mock_entities"][0].entity_id == "e1"

        assert "related_items" in entities
        assert len(entities["related_items"]) == 2

    def test_session_to_summary(self):
        """Test session creates summary."""
        entity = MockEntity("e1", "Test Entity")
        session = MockSession(entity, related_items=[{"id": "r1"}])

        summary = session.to_summary()

        assert summary["entity_name"] == "Test Entity"
        assert summary["related_count"] == 1


class TestSessionManager:
    """Tests for SessionManager abstract interface."""

    def test_manager_product_name(self, session_manager):
        """Test manager has product name."""
        assert session_manager.product_name == "mocksim"

    def test_manager_add_and_count(self, session_manager):
        """Test adding sessions and counting."""
        assert session_manager.count() == 0

        entity = MockEntity("e1", "Entity 1")
        session_manager.add(entity)

        assert session_manager.count() == 1

        entity2 = MockEntity("e2", "Entity 2")
        session_manager.add(entity2)

        assert session_manager.count() == 2

    def test_manager_clear(self, session_manager):
        """Test clearing all sessions."""
        session_manager.add(MockEntity("e1", "Entity 1"))
        session_manager.add(MockEntity("e2", "Entity 2"))

        assert session_manager.count() == 2

        session_manager.clear()

        assert session_manager.count() == 0

    def test_manager_get_all(self, session_manager):
        """Test getting all sessions."""
        session_manager.add(MockEntity("e1", "Entity 1"))
        session_manager.add(MockEntity("e2", "Entity 2"))

        sessions = session_manager.get_all()

        assert len(sessions) == 2

    def test_manager_get_by_id(self, session_manager):
        """Test getting session by ID."""
        entity = MockEntity("e1", "Entity 1")
        added = session_manager.add(entity)

        found = session_manager.get_by_id(added.id)

        assert found is not None
        assert found.primary_entity.name == "Entity 1"

        # Not found
        not_found = session_manager.get_by_id("nonexistent")
        assert not_found is None

    def test_manager_workspace_summary_empty(self, session_manager):
        """Test workspace summary when empty."""
        summary = session_manager.workspace_summary()

        assert summary["status"] == "empty"
        assert summary["entity_count"] == 0

    def test_manager_workspace_summary_with_sessions(self, session_manager):
        """Test workspace summary with sessions."""
        session_manager.add(
            MockEntity("e1", "Entity 1"),
            related_items=[{"id": "r1"}],
        )
        session_manager.add(MockEntity("e2", "Entity 2"))

        summary = session_manager.workspace_summary()

        assert summary["status"] == "active"
        assert summary["product"] == "mocksim"
        assert summary["session_count"] == 2
        assert summary["entity_counts"]["mock_entities"] == 2


class TestSessionManagerPersistence:
    """Tests for SessionManager save/load operations."""

    def test_save_workspace(self, session_manager, temp_workspace_dir):
        """Test saving workspace."""
        session_manager.add(
            MockEntity("e1", "Entity 1"),
            provenance=Provenance.generated(skill_used="test_skill"),
            related_items=[{"id": "r1", "value": 100}],
        )
        session_manager.add(MockEntity("e2", "Entity 2"))

        workspace = session_manager.save_workspace(
            name="Test Workspace",
            description="A test workspace",
            tags=["test"],
        )

        assert workspace.metadata.name == "Test Workspace"
        assert workspace.metadata.product == "mocksim"
        assert workspace.get_entity_count() == 3  # 2 entities + 1 related item

        # Verify file was saved
        file_path = temp_workspace_dir / f"{workspace.metadata.workspace_id}.json"
        assert file_path.exists()

    def test_save_empty_workspace(self, session_manager):
        """Test saving empty workspace."""
        workspace = session_manager.save_workspace(name="Empty")

        assert workspace.get_entity_count() == 0

    def test_load_workspace_by_id(self, session_manager, temp_workspace_dir):
        """Test loading workspace by ID."""
        # Save a workspace
        session_manager.add(MockEntity("e1", "Entity 1"))
        saved = session_manager.save_workspace(name="To Load")
        session_manager.clear()

        # Load it back
        workspace, stats = session_manager.load_workspace(
            workspace_id=saved.metadata.workspace_id,
        )

        assert workspace.metadata.name == "To Load"
        assert session_manager.count() == 1
        assert stats["loaded"] == 1

    def test_load_workspace_by_name(self, session_manager, temp_workspace_dir):
        """Test loading workspace by name."""
        session_manager.add(MockEntity("e1", "Entity 1"))
        session_manager.save_workspace(name="Named Workspace")
        session_manager.clear()

        workspace, _ = session_manager.load_workspace(name="Named")

        assert "Named Workspace" in workspace.metadata.name
        assert session_manager.count() == 1

    def test_load_workspace_replace_mode(self, session_manager, temp_workspace_dir):
        """Test loading workspace replaces existing sessions."""
        session_manager.add(MockEntity("existing", "Existing"))
        assert session_manager.count() == 1

        # Save a different workspace
        session_manager.clear()
        session_manager.add(MockEntity("new", "New"))
        session_manager.save_workspace(name="New Workspace")
        session_manager.clear()

        # Add something else
        session_manager.add(MockEntity("other", "Other"))
        assert session_manager.count() == 1

        # Load in replace mode
        session_manager.load_workspace(name="New", mode="replace")

        # Should only have the loaded workspace
        assert session_manager.count() == 1
        sessions = session_manager.get_all()
        assert sessions[0].primary_entity.name == "New"

    def test_load_workspace_not_found(self, session_manager):
        """Test loading non-existent workspace."""
        with pytest.raises(ValueError, match="not found"):
            session_manager.load_workspace(name="Does Not Exist")

    def test_load_workspace_no_params(self, session_manager):
        """Test loading workspace without params raises error."""
        with pytest.raises(ValueError, match="Must provide"):
            session_manager.load_workspace()

    def test_list_workspaces(self, session_manager, temp_workspace_dir):
        """Test listing workspaces."""
        # Create workspaces
        session_manager.add(MockEntity("e1", "Entity 1"))
        session_manager.save_workspace(name="Workspace 1", tags=["test"])
        session_manager.save_workspace(name="Workspace 2")
        session_manager.save_workspace(name="Other")

        # List all for this product
        workspaces = session_manager.list_workspaces()

        assert len(workspaces) == 3
        assert all(w["name"] for w in workspaces)

        # Search
        searched = session_manager.list_workspaces(search="Workspace")
        assert len(searched) == 2

        # Tags
        tagged = session_manager.list_workspaces(tags=["test"])
        assert len(tagged) == 1

        # Limit
        limited = session_manager.list_workspaces(limit=2)
        assert len(limited) == 2

    def test_delete_workspace(self, session_manager, temp_workspace_dir):
        """Test deleting workspace."""
        session_manager.add(MockEntity("e1", "Entity 1"))
        saved = session_manager.save_workspace(name="To Delete")

        # Delete by ID
        result = session_manager.delete_workspace(saved.metadata.workspace_id)

        assert result is not None
        assert result["name"] == "To Delete"

        # Verify it's gone
        workspaces = session_manager.list_workspaces()
        assert len(workspaces) == 0

    def test_delete_workspace_by_name(self, session_manager, temp_workspace_dir):
        """Test deleting workspace by name."""
        session_manager.add(MockEntity("e1", "Entity 1"))
        session_manager.save_workspace(name="Delete By Name")

        result = session_manager.delete_workspace("Delete By Name")

        assert result is not None

    def test_delete_workspace_not_found(self, session_manager):
        """Test deleting non-existent workspace."""
        result = session_manager.delete_workspace("nonexistent")

        assert result is None
