"""Tests for provenance tracking."""

from datetime import datetime

from healthsim.state import EntityWithProvenance, Provenance, ProvenanceSummary, SourceType


class TestSourceType:
    """Tests for SourceType enum."""

    def test_source_type_values(self):
        """Test SourceType has expected values."""
        assert SourceType.LOADED.value == "loaded"
        assert SourceType.GENERATED.value == "generated"
        assert SourceType.DERIVED.value == "derived"

    def test_source_type_is_string_enum(self):
        """Test SourceType is a string enum."""
        assert str(SourceType.LOADED) == "SourceType.LOADED"
        assert SourceType.GENERATED == "generated"


class TestProvenance:
    """Tests for Provenance model."""

    def test_default_provenance(self):
        """Test default provenance creation."""
        prov = Provenance(source_type=SourceType.GENERATED)

        assert prov.source_type == SourceType.GENERATED
        assert prov.source_system is None
        assert prov.skill_used is None
        assert prov.derived_from == []
        assert isinstance(prov.created_at, datetime)
        assert prov.generation_params == {}

    def test_generated_factory(self):
        """Test generated() factory method."""
        prov = Provenance.generated(skill_used="diabetes_cohort", severity="moderate")

        assert prov.source_type == SourceType.GENERATED
        assert prov.skill_used == "diabetes_cohort"
        assert prov.generation_params == {"severity": "moderate"}

    def test_generated_factory_no_skill(self):
        """Test generated() factory without skill."""
        prov = Provenance.generated()

        assert prov.source_type == SourceType.GENERATED
        assert prov.skill_used is None

    def test_loaded_factory(self):
        """Test loaded() factory method."""
        prov = Provenance.loaded(source_system="legacy_ehr")

        assert prov.source_type == SourceType.LOADED
        assert prov.source_system == "legacy_ehr"

    def test_derived_factory(self):
        """Test derived() factory method."""
        prov = Provenance.derived(derived_from=["patient-123", "encounter-456"])

        assert prov.source_type == SourceType.DERIVED
        assert prov.derived_from == ["patient-123", "encounter-456"]

    def test_provenance_serialization(self):
        """Test provenance serializes to JSON correctly."""
        prov = Provenance.generated(skill_used="test_skill", param1="value1")

        data = prov.model_dump()

        assert data["source_type"] == "generated"
        assert data["skill_used"] == "test_skill"
        assert data["generation_params"] == {"param1": "value1"}

    def test_provenance_deserialization(self):
        """Test provenance deserializes from JSON correctly."""
        data = {
            "source_type": "loaded",
            "source_system": "test_system",
            "skill_used": None,
            "derived_from": [],
            "created_at": "2024-01-15T10:30:00",
            "generation_params": {},
        }

        prov = Provenance.model_validate(data)

        assert prov.source_type == SourceType.LOADED
        assert prov.source_system == "test_system"


class TestProvenanceSummary:
    """Tests for ProvenanceSummary model."""

    def test_empty_summary(self):
        """Test default empty summary."""
        summary = ProvenanceSummary()

        assert summary.total_entities == 0
        assert summary.by_source_type == {}
        assert summary.source_systems == []
        assert summary.skills_used == []

    def test_summary_with_values(self):
        """Test summary with explicit values."""
        summary = ProvenanceSummary(
            total_entities=10,
            by_source_type={"generated": 7, "loaded": 3},
            source_systems=["ehr", "claims"],
            skills_used=["diabetes", "cardiac"],
        )

        assert summary.total_entities == 10
        assert summary.by_source_type["generated"] == 7
        assert "ehr" in summary.source_systems
        assert "diabetes" in summary.skills_used

    def test_from_entities(self):
        """Test building summary from entity collections."""
        entities = {
            "patients": [
                EntityWithProvenance(
                    entity_id="p1",
                    entity_type="patients",
                    data={"name": "Test"},
                    provenance=Provenance.generated(skill_used="diabetes"),
                ),
                EntityWithProvenance(
                    entity_id="p2",
                    entity_type="patients",
                    data={"name": "Test2"},
                    provenance=Provenance.loaded(source_system="ehr"),
                ),
            ],
            "encounters": [
                EntityWithProvenance(
                    entity_id="e1",
                    entity_type="encounters",
                    data={"type": "inpatient"},
                    provenance=Provenance.generated(skill_used="icu"),
                ),
            ],
        }

        summary = ProvenanceSummary.from_entities(entities)

        assert summary.total_entities == 3
        assert summary.by_source_type["generated"] == 2
        assert summary.by_source_type["loaded"] == 1
        assert "ehr" in summary.source_systems
        assert "diabetes" in summary.skills_used
        assert "icu" in summary.skills_used

    def test_from_empty_entities(self):
        """Test building summary from empty collections."""
        summary = ProvenanceSummary.from_entities({})

        assert summary.total_entities == 0
        assert summary.by_source_type == {}
