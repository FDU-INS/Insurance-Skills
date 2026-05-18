"""Tests for EntityWithProvenance."""

from pydantic import BaseModel

from healthsim.state import EntityWithProvenance, Provenance, SourceType


class SampleModel(BaseModel):
    """Sample model for testing."""

    name: str
    value: int


class TestEntityWithProvenance:
    """Tests for EntityWithProvenance wrapper."""

    def test_create_basic_entity(self):
        """Test creating entity with basic data."""
        entity = EntityWithProvenance(
            entity_id="test-123",
            entity_type="patients",
            data={"name": "John Doe", "age": 45},
        )

        assert entity.entity_id == "test-123"
        assert entity.entity_type == "patients"
        assert entity.data["name"] == "John Doe"
        assert entity.provenance.source_type == SourceType.GENERATED

    def test_entity_with_explicit_provenance(self):
        """Test creating entity with explicit provenance."""
        prov = Provenance.loaded(source_system="legacy_db")
        entity = EntityWithProvenance(
            entity_id="test-456",
            entity_type="members",
            data={"member_id": "M001"},
            provenance=prov,
        )

        assert entity.provenance.source_type == SourceType.LOADED
        assert entity.provenance.source_system == "legacy_db"

    def test_from_model(self):
        """Test creating entity from Pydantic model."""
        model = SampleModel(name="Test", value=42)

        entity = EntityWithProvenance.from_model(
            model=model,
            entity_id="sample-001",
            entity_type="samples",
        )

        assert entity.entity_id == "sample-001"
        assert entity.entity_type == "samples"
        assert entity.data["name"] == "Test"
        assert entity.data["value"] == 42

    def test_from_model_with_provenance(self):
        """Test creating entity from model with custom provenance."""
        model = SampleModel(name="Test", value=100)
        prov = Provenance.generated(skill_used="test_skill")

        entity = EntityWithProvenance.from_model(
            model=model,
            entity_id="sample-002",
            entity_type="samples",
            provenance=prov,
        )

        assert entity.provenance.skill_used == "test_skill"

    def test_entity_serialization(self):
        """Test entity serializes to JSON correctly."""
        entity = EntityWithProvenance(
            entity_id="test-789",
            entity_type="claims",
            data={"claim_id": "C001", "amount": 150.00},
            provenance=Provenance.generated(),
        )

        data = entity.model_dump()

        assert data["entity_id"] == "test-789"
        assert data["entity_type"] == "claims"
        assert data["data"]["claim_id"] == "C001"
        assert data["provenance"]["source_type"] == "generated"

    def test_entity_deserialization(self):
        """Test entity deserializes from JSON correctly."""
        data = {
            "entity_id": "test-abc",
            "entity_type": "prescriptions",
            "data": {"drug_name": "Metformin", "quantity": 30},
            "provenance": {
                "source_type": "generated",
                "source_system": None,
                "skill_used": "diabetes",
                "derived_from": [],
                "created_at": "2024-01-15T10:30:00",
                "generation_params": {},
            },
        }

        entity = EntityWithProvenance.model_validate(data)

        assert entity.entity_id == "test-abc"
        assert entity.entity_type == "prescriptions"
        assert entity.data["drug_name"] == "Metformin"
        assert entity.provenance.skill_used == "diabetes"

    def test_entity_types(self):
        """Test various entity types work correctly."""
        entity_types = [
            "patients",
            "encounters",
            "diagnoses",
            "labs",
            "vitals",
            "members",
            "claims",
            "authorizations",
            "accumulators",
            "rx_members",
            "prescriptions",
            "pharmacy_claims",
            "prior_auths",
        ]

        for entity_type in entity_types:
            entity = EntityWithProvenance(
                entity_id=f"{entity_type}-001",
                entity_type=entity_type,
                data={"test": True},
            )
            assert entity.entity_type == entity_type
