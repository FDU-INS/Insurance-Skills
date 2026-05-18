"""Tests for state management models and cohort persistence.

These tests verify the healthsim-core state classes work correctly
when used through the PatientSim re-export layer.
"""

import json
import tempfile
from pathlib import Path

import pytest

from patientsim.core.state import (
    EntityWithProvenance,
    Provenance,
    ProvenanceSummary,
    Scenario,
    SourceType,
    Workspace,
    WorkspaceMetadata,
)


class TestProvenance:
    """Tests for Provenance model."""

    def test_create_generated_provenance(self):
        """Test creating provenance for generated entity."""
        prov = Provenance.generated(skill_used="diabetes-management")

        assert prov.source_type == SourceType.GENERATED
        # Note: source_system is None by default in cross-product version
        assert prov.source_system is None
        assert prov.skill_used == "diabetes-management"
        assert prov.created_at is not None

    def test_create_loaded_provenance(self):
        """Test creating provenance for loaded entity."""
        prov = Provenance.loaded(source_system="csv-import")

        assert prov.source_type == SourceType.LOADED
        assert prov.source_system == "csv-import"
        assert prov.skill_used is None

    def test_create_derived_provenance(self):
        """Test creating provenance for derived entity."""
        prov = Provenance.derived(
            derived_from=["patient-001", "encounter-001"],
        )

        assert prov.source_type == SourceType.DERIVED
        assert prov.derived_from == ["patient-001", "encounter-001"]

    def test_provenance_with_generation_params(self):
        """Test provenance includes generation parameters."""
        # Use **kwargs syntax for generation params
        prov = Provenance.generated(age_range=[50, 70], gender="F")

        assert prov.generation_params["age_range"] == [50, 70]
        assert prov.generation_params["gender"] == "F"

    def test_provenance_serialization(self):
        """Test provenance serializes to JSON correctly."""
        prov = Provenance.generated(skill_used="test-skill")
        data = prov.model_dump(mode="json")

        assert data["source_type"] == "generated"
        assert data["skill_used"] == "test-skill"
        assert "created_at" in data


class TestWorkspaceMetadata:
    """Tests for WorkspaceMetadata model."""

    def test_create_metadata_minimal(self):
        """Test creating metadata with just name."""
        meta = WorkspaceMetadata(name="test-scenario")

        assert meta.name == "test-scenario"
        assert meta.workspace_id is not None
        assert meta.description is None
        assert meta.tags == []
        assert meta.created_at is not None

    def test_create_metadata_complete(self):
        """Test creating metadata with all fields."""
        meta = WorkspaceMetadata(
            name="diabetes-cohort",
            description="25 diabetic patients for testing",
            tags=["diabetes", "training"],
            product="patientsim",
        )

        assert meta.name == "diabetes-cohort"
        assert meta.description == "25 diabetic patients for testing"
        assert meta.tags == ["diabetes", "training"]
        assert meta.product == "patientsim"

    def test_scenario_alias_works(self):
        """Test ScenarioMetadata alias works (legacy compatibility)."""
        # Scenario is an alias for Workspace (legacy)
        meta = Workspace(metadata=WorkspaceMetadata(name="alias-test"))
        assert meta.metadata.name == "alias-test"
        assert meta.metadata.workspace_id is not None


class TestEntityWithProvenance:
    """Tests for EntityWithProvenance wrapper."""

    def test_create_entity_with_provenance(self):
        """Test wrapping entity data with provenance."""
        prov = Provenance.generated()
        entity = EntityWithProvenance(
            entity_id="patient-001",  # entity_id is required
            entity_type="patient",
            data={"mrn": "MRN-001", "name": "John Doe"},
            provenance=prov,
        )

        assert entity.entity_id == "patient-001"
        assert entity.entity_type == "patient"
        assert entity.data["mrn"] == "MRN-001"
        assert entity.provenance.source_type == SourceType.GENERATED


class TestWorkspace:
    """Tests for Workspace model (Scenario alias) and persistence."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for workspace storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_patient_entity(self):
        """Create a sample patient entity with provenance."""
        prov = Provenance.generated(skill_used="test")
        return EntityWithProvenance(
            entity_id="patient-001",
            entity_type="patient",
            data={
                "mrn": "MRN-12345",
                "name": {"given_name": "John", "family_name": "Doe"},
                "birth_date": "1980-01-15",
                "gender": "M",
            },
            provenance=prov,
        )

    def test_create_empty_workspace(self):
        """Test creating workspace with no entities."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(name="empty-workspace"),
        )

        assert workspace.metadata.name == "empty-workspace"
        assert workspace.get_entity_count("patients") == 0
        assert workspace.get_entity_count() == 0

    def test_create_workspace_with_entities(self, sample_patient_entity):
        """Test creating workspace with entities."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(name="test-cohort"),
            entities={"patients": [sample_patient_entity]},
        )

        assert workspace.get_entity_count("patients") == 1
        assert workspace.get_entity_count() == 1

    def test_save_and_load_workspace(self, temp_dir, sample_patient_entity):
        """Test saving and loading a workspace."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(
                name="persistence-test",
                description="Testing save/load",
                tags=["test"],
            ),
            entities={"patients": [sample_patient_entity]},
        )

        # Save
        file_path = workspace.save(directory=temp_dir)
        assert file_path.exists()
        assert file_path.suffix == ".json"

        # Load
        loaded = Workspace.load(workspace.metadata.workspace_id, directory=temp_dir)

        assert loaded.metadata.name == "persistence-test"
        assert loaded.metadata.description == "Testing save/load"
        assert loaded.get_entity_count("patients") == 1

    def test_scenario_alias_save_and_load(self, temp_dir, sample_patient_entity):
        """Test Scenario alias works for save/load (legacy compatibility)."""
        # Scenario is an alias for Workspace (legacy)
        scenario = Scenario(
            metadata=WorkspaceMetadata(name="alias-test"),
            entities={"patients": [sample_patient_entity]},
        )

        file_path = scenario.save(directory=temp_dir)
        assert file_path.exists()

        # Load using Scenario.load (legacy alias)
        loaded = Scenario.load(scenario.metadata.workspace_id, directory=temp_dir)
        assert loaded.metadata.name == "alias-test"

    def test_find_by_name(self, temp_dir, sample_patient_entity):
        """Test finding workspace by name."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(name="diabetes-cohort"),
            entities={"patients": [sample_patient_entity]},
        )
        workspace.save(directory=temp_dir)

        # Exact match
        found = Workspace.find_by_name("diabetes-cohort", directory=temp_dir)
        assert found is not None
        assert found.metadata.name == "diabetes-cohort"

        # Partial match
        found = Workspace.find_by_name("diabetes", directory=temp_dir)
        assert found is not None

        # Case insensitive
        found = Workspace.find_by_name("DIABETES", directory=temp_dir)
        assert found is not None

        # Not found
        found = Workspace.find_by_name("cardiac", directory=temp_dir)
        assert found is None

    def test_list_all_workspaces(self, temp_dir, sample_patient_entity):
        """Test listing all workspaces."""
        # Create multiple workspaces
        for name in ["workspace-a", "workspace-b", "workspace-c"]:
            workspace = Workspace(
                metadata=WorkspaceMetadata(name=name),
                entities={"patients": [sample_patient_entity]},
            )
            workspace.save(directory=temp_dir)

        workspaces = Workspace.list_all(directory=temp_dir)

        assert len(workspaces) == 3
        # Should be sorted by creation date (newest first)
        names = [w.metadata.name for w in workspaces]
        assert "workspace-a" in names
        assert "workspace-b" in names
        assert "workspace-c" in names

    def test_list_workspaces_with_search(self, temp_dir, sample_patient_entity):
        """Test filtering workspaces by search string."""
        for name, desc in [
            ("diabetes-cohort", "Diabetic patients"),
            ("cardiac-test", "Heart failure patients"),
            ("mixed-cohort", "Various conditions"),
        ]:
            workspace = Workspace(
                metadata=WorkspaceMetadata(name=name, description=desc),
                entities={"patients": [sample_patient_entity]},
            )
            workspace.save(directory=temp_dir)

        # Search by name
        results = Workspace.list_all(search="diabetes", directory=temp_dir)
        assert len(results) == 1
        assert results[0].metadata.name == "diabetes-cohort"

        # Search by description
        results = Workspace.list_all(search="heart", directory=temp_dir)
        assert len(results) == 1
        assert results[0].metadata.name == "cardiac-test"

    def test_list_workspaces_with_tags(self, temp_dir, sample_patient_entity):
        """Test filtering workspaces by tags."""
        for name, tags in [
            ("workspace-1", ["training", "diabetes"]),
            ("workspace-2", ["training", "cardiac"]),
            ("workspace-3", ["production"]),
        ]:
            workspace = Workspace(
                metadata=WorkspaceMetadata(name=name, tags=tags),
                entities={"patients": [sample_patient_entity]},
            )
            workspace.save(directory=temp_dir)

        # Filter by single tag
        results = Workspace.list_all(tags=["training"], directory=temp_dir)
        assert len(results) == 2

        # Filter by multiple tags (AND logic)
        results = Workspace.list_all(tags=["training", "diabetes"], directory=temp_dir)
        assert len(results) == 1
        assert results[0].metadata.name == "workspace-1"

    def test_list_workspaces_limit_via_slice(self, temp_dir, sample_patient_entity):
        """Test limiting workspace results via slicing."""
        for i in range(10):
            workspace = Workspace(
                metadata=WorkspaceMetadata(name=f"workspace-{i}"),
                entities={"patients": [sample_patient_entity]},
            )
            workspace.save(directory=temp_dir)

        # list_all returns all, slice to limit
        results = Workspace.list_all(directory=temp_dir)[:5]
        assert len(results) == 5

    def test_delete_workspace(self, temp_dir, sample_patient_entity):
        """Test deleting a workspace."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(name="to-delete"),
            entities={"patients": [sample_patient_entity]},
        )
        workspace.save(directory=temp_dir)

        workspace_id = workspace.metadata.workspace_id

        # Verify exists
        loaded = Workspace.load(workspace_id, directory=temp_dir)
        assert loaded is not None

        # Delete
        result = Workspace.delete(workspace_id, directory=temp_dir)
        assert result is True

        # Verify deleted
        with pytest.raises(FileNotFoundError):
            Workspace.load(workspace_id, directory=temp_dir)

    def test_delete_nonexistent_workspace(self, temp_dir):
        """Test deleting non-existent workspace returns False."""
        result = Workspace.delete("nonexistent-id", directory=temp_dir)
        assert result is False

    def test_load_nonexistent_workspace(self, temp_dir):
        """Test loading non-existent workspace raises error."""
        with pytest.raises(FileNotFoundError):
            Workspace.load("nonexistent-id", directory=temp_dir)

    def test_provenance_summary(self, sample_patient_entity):
        """Test provenance summary aggregation."""
        # Create entities with different provenance types
        loaded_prov = Provenance.loaded(source_system="test")
        generated_prov = Provenance.generated(skill_used="diabetes")
        derived_prov = Provenance.derived(derived_from=["p1"])

        entities = {
            "patients": [
                EntityWithProvenance(
                    entity_id="p1",
                    entity_type="patient",
                    data={"mrn": "MRN-1"},
                    provenance=generated_prov,
                ),
                EntityWithProvenance(
                    entity_id="p2",
                    entity_type="patient",
                    data={"mrn": "MRN-2"},
                    provenance=loaded_prov,
                ),
            ],
            "diagnoses": [
                EntityWithProvenance(
                    entity_id="d1",
                    entity_type="diagnosis",
                    data={"code": "E11.9"},
                    provenance=derived_prov,
                ),
            ],
        }

        summary = ProvenanceSummary.from_entities(entities)

        assert summary.total_entities == 3
        assert summary.by_source_type["generated"] == 1
        assert summary.by_source_type["loaded"] == 1
        assert summary.by_source_type["derived"] == 1
        assert "diabetes" in summary.skills_used

    def test_workspace_file_format(self, temp_dir, sample_patient_entity):
        """Test workspace file is valid JSON with expected structure."""
        workspace = Workspace(
            metadata=WorkspaceMetadata(
                name="format-test",
                description="Testing JSON format",
                tags=["test"],
            ),
            entities={"patients": [sample_patient_entity]},
            provenance_summary=ProvenanceSummary(
                total_entities=1,
                by_source_type={"generated": 1},
            ),
        )
        file_path = workspace.save(directory=temp_dir)

        # Read and parse JSON
        content = json.loads(file_path.read_text())

        # Check structure
        assert "metadata" in content
        assert "entities" in content
        assert "provenance_summary" in content

        # Check metadata
        assert content["metadata"]["name"] == "format-test"
        assert content["metadata"]["description"] == "Testing JSON format"
        assert content["metadata"]["tags"] == ["test"]

        # Check entities
        assert "patients" in content["entities"]
        assert len(content["entities"]["patients"]) == 1

        # Check entity has provenance
        patient = content["entities"]["patients"][0]
        assert "provenance" in patient
        assert patient["provenance"]["source_type"] == "generated"


# Legacy compatibility tests
class TestScenarioAlias:
    """Test that Scenario alias works correctly (legacy compatibility)."""

    def test_scenario_is_workspace_alias(self):
        """Test Scenario is an alias for Workspace."""
        assert Scenario is Workspace
