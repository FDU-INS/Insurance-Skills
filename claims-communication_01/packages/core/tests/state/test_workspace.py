"""Tests for Workspace persistence."""

from datetime import datetime

import pytest

from healthsim.state import (
    EntityWithProvenance,
    Provenance,
    ProvenanceSummary,
    Workspace,
    WorkspaceMetadata,
)


@pytest.fixture
def temp_workspace_dir(tmp_path):
    """Create a temporary workspace directory."""
    workspace_dir = tmp_path / "workspaces"
    workspace_dir.mkdir()
    return workspace_dir


@pytest.fixture
def sample_entities():
    """Create sample entities for testing."""
    return {
        "patients": [
            EntityWithProvenance(
                entity_id="p1",
                entity_type="patients",
                data={"name": "John Doe", "age": 45},
                provenance=Provenance.generated(skill_used="diabetes"),
            ),
            EntityWithProvenance(
                entity_id="p2",
                entity_type="patients",
                data={"name": "Jane Smith", "age": 62},
                provenance=Provenance.generated(skill_used="cardiac"),
            ),
        ],
        "encounters": [
            EntityWithProvenance(
                entity_id="e1",
                entity_type="encounters",
                data={"patient_id": "p1", "type": "inpatient"},
                provenance=Provenance.generated(),
            ),
        ],
    }


class TestWorkspaceMetadata:
    """Tests for WorkspaceMetadata model."""

    def test_default_metadata(self):
        """Test default metadata creation."""
        meta = WorkspaceMetadata(name="Test Workspace")

        assert meta.name == "Test Workspace"
        assert meta.workspace_id  # UUID should be generated
        assert meta.description is None
        assert meta.tags == []
        assert meta.product == "unknown"
        assert meta.schema_version == "2.0"
        assert isinstance(meta.created_at, datetime)

    def test_metadata_with_all_fields(self):
        """Test metadata with all fields specified."""
        meta = WorkspaceMetadata(
            workspace_id="test-uuid-123",
            name="Full Workspace",
            description="A test workspace",
            tags=["test", "demo"],
            product="patientsim",
        )

        assert meta.workspace_id == "test-uuid-123"
        assert meta.description == "A test workspace"
        assert meta.tags == ["test", "demo"]
        assert meta.product == "patientsim"


class TestWorkspace:
    """Tests for Workspace model."""

    def test_create_empty_workspace(self):
        """Test creating empty workspace."""
        meta = WorkspaceMetadata(name="Empty Test")
        workspace = Workspace(metadata=meta)

        assert workspace.metadata.name == "Empty Test"
        assert workspace.entities == {}
        assert workspace.get_entity_count() == 0

    def test_workspace_with_entities(self, sample_entities):
        """Test workspace with entities."""
        meta = WorkspaceMetadata(name="With Entities", product="patientsim")
        workspace = Workspace(
            metadata=meta,
            entities=sample_entities,
        )

        assert workspace.get_entity_count() == 3
        assert workspace.get_entity_count("patients") == 2
        assert workspace.get_entity_count("encounters") == 1

    def test_get_entity_types(self, sample_entities):
        """Test getting entity types."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(name="Types Test"),
            entities=sample_entities,
        )

        types = workspace.get_entity_types()
        assert "patients" in types
        assert "encounters" in types

    def test_add_entities(self):
        """Test adding entities to workspace."""
        workspace = Workspace(metadata=WorkspaceMetadata(name="Add Test"))

        new_entities = [
            EntityWithProvenance(
                entity_id="m1",
                entity_type="members",
                data={"member_id": "M001"},
                provenance=Provenance.generated(),
            ),
        ]

        workspace.add_entities("members", new_entities)

        assert workspace.get_entity_count("members") == 1
        assert workspace.metadata.updated_at is not None

    def test_to_summary(self, sample_entities):
        """Test workspace summary generation."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(
                name="Summary Test",
                description="Test description",
                product="patientsim",
                tags=["test"],
            ),
            entities=sample_entities,
            provenance_summary=ProvenanceSummary(
                total_entities=3,
                by_source_type={"generated": 3},
                skills_used=["diabetes", "cardiac"],
            ),
        )

        summary = workspace.to_summary()

        assert summary["name"] == "Summary Test"
        assert summary["description"] == "Test description"
        assert summary["product"] == "patientsim"
        assert summary["entity_counts"]["patients"] == 2
        assert summary["total_entities"] == 3
        assert "diabetes" in summary["provenance"]["skills_used"]


class TestWorkspacePersistence:
    """Tests for workspace save/load operations."""

    def test_save_and_load(self, temp_workspace_dir, sample_entities):
        """Test saving and loading workspace."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(
                name="Persistence Test",
                product="patientsim",
            ),
            entities=sample_entities,
        )

        # Save
        file_path = workspace.save(directory=temp_workspace_dir)
        assert file_path.exists()

        # Load
        loaded = Workspace.load(
            workspace.metadata.workspace_id,
            directory=temp_workspace_dir,
        )

        assert loaded.metadata.name == "Persistence Test"
        assert loaded.get_entity_count() == 3
        assert loaded.entities["patients"][0].data["name"] == "John Doe"

    def test_load_not_found(self, temp_workspace_dir):
        """Test loading non-existent workspace."""
        with pytest.raises(FileNotFoundError):
            Workspace.load("nonexistent-id", directory=temp_workspace_dir)

    def test_find_by_name(self, temp_workspace_dir, sample_entities):
        """Test finding workspace by name."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(
                name="Diabetes Cohort",
                product="patientsim",
            ),
            entities=sample_entities,
        )
        workspace.save(directory=temp_workspace_dir)

        # Exact match
        found = Workspace.find_by_name("Diabetes Cohort", directory=temp_workspace_dir)
        assert found is not None
        assert found.metadata.name == "Diabetes Cohort"

        # Partial match (case-insensitive)
        found = Workspace.find_by_name("diabetes", directory=temp_workspace_dir)
        assert found is not None

        # Not found
        not_found = Workspace.find_by_name("Cardiac", directory=temp_workspace_dir)
        assert not_found is None

    def test_list_all(self, temp_workspace_dir, sample_entities):
        """Test listing all workspaces."""
        # Create multiple workspaces
        for i, (name, product) in enumerate(
            [
                ("Patient Cohort 1", "patientsim"),
                ("Patient Cohort 2", "patientsim"),
                ("Member Test", "membersim"),
            ]
        ):
            workspace = Workspace(
                metadata=WorkspaceMetadata(
                    name=name,
                    product=product,
                    tags=["test"] if i == 0 else [],
                ),
                entities=sample_entities if product == "patientsim" else {},
            )
            workspace.save(directory=temp_workspace_dir)

        # List all
        all_workspaces = Workspace.list_all(directory=temp_workspace_dir)
        assert len(all_workspaces) == 3

        # Filter by product
        patient_workspaces = Workspace.list_all(
            product="patientsim",
            directory=temp_workspace_dir,
        )
        assert len(patient_workspaces) == 2

        # Filter by search
        cohort_workspaces = Workspace.list_all(
            search="cohort",
            directory=temp_workspace_dir,
        )
        assert len(cohort_workspaces) == 2

        # Filter by tags
        tagged_workspaces = Workspace.list_all(
            tags=["test"],
            directory=temp_workspace_dir,
        )
        assert len(tagged_workspaces) == 1

    def test_delete(self, temp_workspace_dir, sample_entities):
        """Test deleting workspace."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(name="To Delete"),
            entities=sample_entities,
        )
        file_path = workspace.save(directory=temp_workspace_dir)
        assert file_path.exists()

        # Delete
        result = Workspace.delete(
            workspace.metadata.workspace_id,
            directory=temp_workspace_dir,
        )
        assert result is True
        assert not file_path.exists()

        # Delete non-existent
        result = Workspace.delete("nonexistent", directory=temp_workspace_dir)
        assert result is False

    def test_list_empty_directory(self, temp_workspace_dir):
        """Test listing from empty directory."""
        workspaces = Workspace.list_all(directory=temp_workspace_dir)
        assert workspaces == []

    def test_list_nonexistent_directory(self, tmp_path):
        """Test listing from non-existent directory."""
        nonexistent = tmp_path / "does_not_exist"
        workspaces = Workspace.list_all(directory=nonexistent)
        assert workspaces == []
