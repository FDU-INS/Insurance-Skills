"""Tests for cross-domain synchronization."""

import pytest
from datetime import date

from healthsim.generation.cross_domain_sync import (
    CrossDomainSync,
    SyncConfig,
    PersonIdentity,
    IdentityRegistry,
    TriggerRegistry,
    TriggerSpec,
    TriggerResult,
    TriggerType,
    ProductType,
    CorrelatorType,
    create_cross_domain_sync,
    hash_ssn,
)


class TestPersonIdentity:
    """Tests for PersonIdentity model."""

    def test_basic_creation(self):
        """Test creating a basic person identity."""
        identity = PersonIdentity(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1965, 3, 15),
            gender="M",
        )
        
        assert identity.correlation_id is not None
        assert identity.first_name == "John"
        assert identity.last_name == "Doe"
        assert identity.gender == "M"

    def test_with_product_ids(self):
        """Test identity with product-specific IDs."""
        identity = PersonIdentity(
            patient_id="PAT-12345678",
            member_id="MEM-87654321",
            rx_member_id="RXM-11111111",
        )
        
        assert identity.patient_id == "PAT-12345678"
        assert identity.member_id == "MEM-87654321"
        assert identity.rx_member_id == "RXM-11111111"

    def test_to_correlator_dict(self):
        """Test conversion to correlator dictionary."""
        identity = PersonIdentity(
            ssn_hash="abc123",
            date_of_birth=date(1965, 3, 15),
            gender="M",
            first_name="John",
            last_name="Doe",
        )
        
        correlators = identity.to_correlator_dict()
        
        assert correlators["ssn_hash"] == "abc123"
        assert correlators["dob"] == "1965-03-15"
        assert correlators["gender"] == "M"
        assert correlators["name"] == "DOE,JOHN"


class TestIdentityRegistry:
    """Tests for IdentityRegistry."""

    def test_register_identity(self):
        """Test registering an identity."""
        registry = IdentityRegistry()
        identity = PersonIdentity(
            patient_id="PAT-001",
            member_id="MEM-001",
        )
        
        correlation_id = registry.register(identity)
        
        assert correlation_id == identity.correlation_id
        assert registry.count() == 1

    def test_get_by_correlation_id(self):
        """Test retrieving by correlation ID."""
        registry = IdentityRegistry()
        identity = PersonIdentity(patient_id="PAT-001")
        registry.register(identity)
        
        retrieved = registry.get_by_correlation_id(identity.correlation_id)
        
        assert retrieved is not None
        assert retrieved.patient_id == "PAT-001"

    def test_get_by_product_id(self):
        """Test retrieving by product-specific ID."""
        registry = IdentityRegistry()
        identity = PersonIdentity(
            patient_id="PAT-001",
            member_id="MEM-001",
        )
        registry.register(identity)
        
        # Get by patient ID
        result = registry.get_by_product_id(ProductType.PATIENTSIM, "PAT-001")
        assert result is not None
        assert result.correlation_id == identity.correlation_id
        
        # Get by member ID
        result = registry.get_by_product_id(ProductType.MEMBERSIM, "MEM-001")
        assert result is not None
        assert result.correlation_id == identity.correlation_id

    def test_link_product_id(self):
        """Test linking a new product ID to existing identity."""
        registry = IdentityRegistry()
        identity = PersonIdentity(patient_id="PAT-001")
        registry.register(identity)
        
        # Link member ID
        success = registry.link_product_id(
            identity.correlation_id,
            ProductType.MEMBERSIM,
            "MEM-002"
        )
        
        assert success is True
        
        # Verify linkage
        result = registry.get_by_product_id(ProductType.MEMBERSIM, "MEM-002")
        assert result is not None
        assert result.patient_id == "PAT-001"
        assert result.member_id == "MEM-002"

    def test_find_matches_exact_ssn(self):
        """Test finding matches by SSN hash."""
        registry = IdentityRegistry()
        identity = PersonIdentity(
            ssn_hash="abc123def456",
            date_of_birth=date(1965, 3, 15),
        )
        registry.register(identity)
        
        matches = registry.find_matches(
            {"ssn_hash": "abc123def456"},
            min_confidence=0.8
        )
        
        assert len(matches) == 1
        assert matches[0][0].correlation_id == identity.correlation_id
        assert matches[0][1] >= 0.8

    def test_find_matches_no_match(self):
        """Test finding matches with no results."""
        registry = IdentityRegistry()
        identity = PersonIdentity(ssn_hash="abc123")
        registry.register(identity)
        
        matches = registry.find_matches(
            {"ssn_hash": "xyz789"},
            min_confidence=0.8
        )
        
        assert len(matches) == 0

    def test_get_all(self):
        """Test getting all identities."""
        registry = IdentityRegistry()
        identity1 = PersonIdentity(patient_id="PAT-001")
        identity2 = PersonIdentity(patient_id="PAT-002")
        registry.register(identity1)
        registry.register(identity2)
        
        all_ids = registry.get_all()
        
        assert len(all_ids) == 2


class TestTriggerRegistry:
    """Tests for TriggerRegistry."""

    def test_register_spec(self):
        """Test registering a trigger specification."""
        registry = TriggerRegistry()
        spec = TriggerSpec(
            trigger_type=TriggerType.ENCOUNTER_TO_CLAIM,
            source_product=ProductType.PATIENTSIM,
            target_product=ProductType.MEMBERSIM,
            source_event="encounter",
            target_event="claim",
        )
        
        registry.register_spec(spec)
        
        retrieved = registry.get_spec(TriggerType.ENCOUNTER_TO_CLAIM)
        assert retrieved is not None
        assert retrieved.source_event == "encounter"

    def test_fire_without_handler(self):
        """Test firing trigger without handler."""
        registry = TriggerRegistry()
        spec = TriggerSpec(
            trigger_type=TriggerType.ENCOUNTER_TO_CLAIM,
            source_product=ProductType.PATIENTSIM,
            target_product=ProductType.MEMBERSIM,
            source_event="encounter",
            target_event="claim",
        )
        registry.register_spec(spec)
        
        result = registry.fire(
            TriggerType.ENCOUNTER_TO_CLAIM,
            {"id": "ENC-001"}
        )
        
        assert result.success is False
        assert "No handler" in result.message

    def test_fire_disabled_trigger(self):
        """Test firing a disabled trigger."""
        registry = TriggerRegistry()
        spec = TriggerSpec(
            trigger_type=TriggerType.ENCOUNTER_TO_CLAIM,
            source_product=ProductType.PATIENTSIM,
            target_product=ProductType.MEMBERSIM,
            source_event="encounter",
            target_event="claim",
            enabled=False,
        )
        registry.register_spec(spec)
        
        result = registry.fire(
            TriggerType.ENCOUNTER_TO_CLAIM,
            {"id": "ENC-001"}
        )
        
        assert result.success is False
        assert "disabled" in result.message


class TestCrossDomainSync:
    """Tests for CrossDomainSync coordinator."""

    def test_basic_creation(self):
        """Test creating a CrossDomainSync instance."""
        sync = CrossDomainSync()
        
        assert sync.identity_registry is not None
        assert sync.trigger_registry is not None

    def test_creation_with_config(self):
        """Test creating with custom config."""
        config = SyncConfig(
            auto_generate_claims=False,
            claim_delay_days=(1, 5),
        )
        sync = CrossDomainSync(config=config)
        
        assert sync.config.auto_generate_claims is False
        assert sync.config.claim_delay_days == (1, 5)

    def test_create_linked_identity(self):
        """Test creating linked identity across products."""
        sync = CrossDomainSync(seed=42)
        
        identity = sync.create_linked_identity(
            products=[ProductType.PATIENTSIM, ProductType.MEMBERSIM],
            demographics={
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": date(1970, 5, 20),
                "gender": "F",
            }
        )
        
        assert identity.patient_id is not None
        assert identity.member_id is not None
        assert identity.first_name == "Jane"
        assert identity.last_name == "Smith"
        
        # Should be registered
        assert sync.identity_registry.count() == 1

    def test_create_linked_identity_with_ssn(self):
        """Test creating linked identity with SSN hash."""
        sync = CrossDomainSync(seed=42)
        
        identity = sync.create_linked_identity(
            products=[ProductType.PATIENTSIM],
            demographics={
                "ssn": "123-45-6789",
                "first_name": "John",
                "last_name": "Doe",
            }
        )
        
        assert identity.ssn_hash is not None
        assert len(identity.ssn_hash) == 16

    def test_create_multiple_linked_identities(self):
        """Test creating multiple linked identities."""
        sync = CrossDomainSync(seed=42)
        
        for i in range(5):
            sync.create_linked_identity(
                products=[ProductType.PATIENTSIM, ProductType.MEMBERSIM],
                demographics={"first_name": f"Person{i}"},
                seed=42 + i,
            )
        
        assert sync.identity_registry.count() == 5

    def test_default_triggers_registered(self):
        """Test that default triggers are registered."""
        sync = CrossDomainSync()
        
        # Check encounter_to_claim
        spec = sync.trigger_registry.get_spec(TriggerType.ENCOUNTER_TO_CLAIM)
        assert spec is not None
        assert spec.source_product == ProductType.PATIENTSIM
        assert spec.target_product == ProductType.MEMBERSIM
        
        # Check prescription_to_fill
        spec = sync.trigger_registry.get_spec(TriggerType.PRESCRIPTION_TO_FILL)
        assert spec is not None
        assert spec.source_product == ProductType.PATIENTSIM
        assert spec.target_product == ProductType.RXMEMBERSIM

    def test_validate_empty(self):
        """Test validation with no entities."""
        sync = CrossDomainSync()
        
        passed, errors, warnings = sync.validate({})
        
        assert passed is True
        assert len(errors) == 0

    def test_get_sync_report(self):
        """Test generating sync report."""
        sync = CrossDomainSync(seed=42)
        
        # Create some identities
        sync.create_linked_identity(
            products=[ProductType.PATIENTSIM, ProductType.MEMBERSIM],
            demographics={"first_name": "Test"},
        )
        
        report = sync.get_sync_report()
        
        assert report.identities_correlated == 1
        assert report.triggers_fired == 0

    def test_sync_report_formatted_string(self):
        """Test sync report formatting."""
        sync = CrossDomainSync(seed=42)
        sync.create_linked_identity(
            products=[ProductType.PATIENTSIM],
            demographics={"first_name": "Test"},
        )
        
        report = sync.get_sync_report(
            entities={ProductType.PATIENTSIM: []},
            triggers_fired=[],
        )
        
        formatted = report.to_formatted_string()
        
        assert "CROSS-DOMAIN SYNC REPORT" in formatted
        assert "IDENTITY CORRELATION" in formatted
        assert "VALIDATION" in formatted


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_create_cross_domain_sync(self):
        """Test factory function."""
        sync = create_cross_domain_sync(seed=42)
        
        assert isinstance(sync, CrossDomainSync)
        assert sync.seed == 42

    def test_hash_ssn(self):
        """Test SSN hashing."""
        hash1 = hash_ssn("123-45-6789")
        hash2 = hash_ssn("123456789")  # Same digits, different format
        hash3 = hash_ssn("987-65-4321")
        
        # Same SSN should produce same hash
        assert hash1 == hash2
        
        # Different SSN should produce different hash
        assert hash1 != hash3
        
        # Hash should be 16 characters
        assert len(hash1) == 16


class TestSyncConfig:
    """Tests for SyncConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = SyncConfig()
        
        assert config.auto_generate_claims is True
        assert config.auto_generate_fills is True
        assert config.claim_delay_days == (0, 3)
        assert config.refill_window_days == 7
        assert config.pcp_sticky_assignment is True

    def test_custom_values(self):
        """Test custom configuration values."""
        config = SyncConfig(
            auto_generate_claims=False,
            claim_delay_days=(2, 7),
            refill_window_days=14,
        )
        
        assert config.auto_generate_claims is False
        assert config.claim_delay_days == (2, 7)
        assert config.refill_window_days == 14
