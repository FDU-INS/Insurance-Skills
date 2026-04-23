"""Tests for RxMemberSim session management."""

from datetime import date
from decimal import Decimal

import pytest
from healthsim.state import Provenance

from rxmembersim.claims.claim import PharmacyClaim, TransactionCode
from rxmembersim.core.member import (
    BenefitAccumulators,
    MemberDemographics,
    RxMember,
)
from rxmembersim.core.prescription import DAWCode, Prescription
from rxmembersim.mcp.session import RxMemberSession, RxMemberSessionManager


@pytest.fixture
def sample_demographics():
    """Create sample member demographics."""
    return MemberDemographics(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1980, 5, 15),
        gender="M",
        address_line1="123 Main St",
        city="Springfield",
        state="IL",
        zip_code="62701",
    )


@pytest.fixture
def sample_accumulators():
    """Create sample benefit accumulators."""
    return BenefitAccumulators(
        deductible_met=Decimal("150.00"),
        deductible_remaining=Decimal("350.00"),
        oop_met=Decimal("500.00"),
        oop_remaining=Decimal("5500.00"),
    )


@pytest.fixture
def sample_rx_member(sample_demographics, sample_accumulators):
    """Create a sample RxMember."""
    return RxMember(
        member_id="RXM-00000001",
        cardholder_id="RXM-00000001",
        person_code="01",
        bin="610014",
        pcn="RXTEST",
        group_number="GRP001",
        demographics=sample_demographics,
        effective_date=date(2024, 1, 1),
        accumulators=sample_accumulators,
        plan_code="GOLD",
        formulary_id="FORM001",
    )


@pytest.fixture
def sample_prescription():
    """Create a sample prescription."""
    return Prescription(
        prescription_number="RX123456",
        ndc="00000012345",
        drug_name="Lisinopril 10mg",
        quantity_prescribed=Decimal("30"),
        days_supply=30,
        refills_authorized=11,
        refills_remaining=11,
        prescriber_npi="1234567890",
        prescriber_name="Dr. Smith",
        written_date=date(2024, 6, 1),
        expiration_date=date(2025, 6, 1),
        daw_code=DAWCode.NO_SELECTION,
    )


@pytest.fixture
def sample_pharmacy_claim(sample_rx_member):
    """Create a sample pharmacy claim."""
    return PharmacyClaim(
        claim_id="CLM000001",
        transaction_code=TransactionCode.BILLING,
        service_date=date(2024, 6, 15),
        pharmacy_npi="9876543210",
        pharmacy_ncpdp="1234567",
        member_id=sample_rx_member.member_id,
        cardholder_id=sample_rx_member.cardholder_id,
        person_code="01",
        bin=sample_rx_member.bin,
        pcn=sample_rx_member.pcn,
        group_number=sample_rx_member.group_number,
        prescription_number="RX123456",
        fill_number=1,
        ndc="00000012345",
        quantity_dispensed=Decimal("30"),
        days_supply=30,
        daw_code="0",
        prescriber_npi="1234567890",
        ingredient_cost_submitted=Decimal("15.00"),
        dispensing_fee_submitted=Decimal("2.00"),
        usual_customary_charge=Decimal("20.00"),
        gross_amount_due=Decimal("17.00"),
    )


@pytest.fixture
def temp_workspace_dir(tmp_path):
    """Create temporary workspace directory."""
    return tmp_path


@pytest.fixture
def session_manager(temp_workspace_dir):
    """Create a session manager with temp directory."""
    return RxMemberSessionManager(workspace_dir=temp_workspace_dir)


class TestRxMemberSession:
    """Tests for RxMemberSession class."""

    def test_create_session_minimal(self, sample_rx_member):
        """Test creating session with just an rx_member."""
        session = RxMemberSession(rx_member=sample_rx_member)

        assert session.id is not None
        assert len(session.id) == 8
        assert session.rx_member == sample_rx_member
        assert session.primary_entity == sample_rx_member
        assert session.prescriptions == []
        assert session.pharmacy_claims == []
        assert session.dur_alerts == []
        assert session.prior_auths == []

    def test_create_session_with_prescriptions(
        self, sample_rx_member, sample_prescription
    ):
        """Test creating session with prescriptions."""
        session = RxMemberSession(
            rx_member=sample_rx_member,
            prescriptions=[sample_prescription],
        )

        assert len(session.prescriptions) == 1
        assert session.prescriptions[0].prescription_number == "RX123456"

    def test_to_summary(
        self, sample_rx_member, sample_prescription, sample_pharmacy_claim
    ):
        """Test summary generation."""
        session = RxMemberSession(
            rx_member=sample_rx_member,
            prescriptions=[sample_prescription],
            pharmacy_claims=[sample_pharmacy_claim],
        )

        summary = session.to_summary()

        assert "id" in summary
        assert "member_id" in summary
        assert "name" in summary
        assert "bin" in summary
        assert summary["prescription_count"] == 1
        assert summary["claims_count"] == 1

    def test_to_entities_with_provenance(
        self, sample_rx_member, sample_prescription, sample_pharmacy_claim
    ):
        """Test conversion to entities with provenance."""
        session = RxMemberSession(
            rx_member=sample_rx_member,
            prescriptions=[sample_prescription],
            pharmacy_claims=[sample_pharmacy_claim],
            provenance=Provenance.generated(skill_used="test"),
        )

        entities = session.to_entities_with_provenance()

        assert "rx_members" in entities
        assert len(entities["rx_members"]) == 1
        assert entities["rx_members"][0].entity_type == "rx_members"

        assert "prescriptions" in entities
        assert len(entities["prescriptions"]) == 1

        assert "pharmacy_claims" in entities
        assert len(entities["pharmacy_claims"]) == 1

    def test_from_entities_with_provenance(
        self, sample_rx_member, sample_pharmacy_claim
    ):
        """Test reconstructing session from entities."""
        original = RxMemberSession(
            rx_member=sample_rx_member,
            pharmacy_claims=[sample_pharmacy_claim],
        )

        entities = original.to_entities_with_provenance()
        rx_member_entity = entities["rx_members"][0]

        reconstructed = RxMemberSession.from_entities_with_provenance(
            rx_member_entity, entities
        )

        assert reconstructed.rx_member.member_id == original.rx_member.member_id
        assert len(reconstructed.pharmacy_claims) == 1
        assert reconstructed.pharmacy_claims[0].claim_id == "CLM000001"


class TestRxMemberSessionManager:
    """Tests for RxMemberSessionManager class."""

    def test_product_name(self, session_manager):
        """Test product name is correct."""
        assert session_manager.product_name == "rxmembersim"

    def test_add_and_count(self, session_manager, sample_rx_member):
        """Test adding rx_members and counting."""
        assert session_manager.count() == 0

        session_manager.add_rx_member(sample_rx_member)
        assert session_manager.count() == 1

    def test_clear(self, session_manager, sample_rx_member):
        """Test clearing all sessions."""
        session_manager.add_rx_member(sample_rx_member)
        assert session_manager.count() == 1

        session_manager.clear()
        assert session_manager.count() == 0

    def test_get_by_member_id(self, session_manager, sample_rx_member):
        """Test getting session by member ID."""
        session_manager.add_rx_member(sample_rx_member)

        found = session_manager.get_by_member_id(sample_rx_member.member_id)
        assert found is not None
        assert found.rx_member.member_id == sample_rx_member.member_id

        not_found = session_manager.get_by_member_id("nonexistent")
        assert not_found is None

    def test_get_latest(self, session_manager, sample_rx_member, sample_demographics):
        """Test getting latest session."""
        # Create second member
        acc2 = BenefitAccumulators(
            deductible_met=Decimal("0"),
            deductible_remaining=Decimal("500"),
            oop_met=Decimal("0"),
            oop_remaining=Decimal("6000"),
        )
        m2 = RxMember(
            member_id="RXM-00000002",
            cardholder_id="RXM-00000002",
            person_code="01",
            bin="610014",
            pcn="RXTEST",
            group_number="GRP002",
            demographics=sample_demographics,
            effective_date=date(2024, 1, 1),
            accumulators=acc2,
        )

        session_manager.add_rx_member(sample_rx_member)
        session_manager.add_rx_member(m2)

        latest = session_manager.get_latest()
        assert latest is not None
        assert latest.rx_member.member_id == "RXM-00000002"

    def test_add_claim(
        self, session_manager, sample_rx_member, sample_pharmacy_claim
    ):
        """Test adding claim to rx_member session."""
        session_manager.add_rx_member(sample_rx_member)

        result = session_manager.add_claim(
            sample_rx_member.member_id, sample_pharmacy_claim
        )
        assert result is True

        session = session_manager.get_by_member_id(sample_rx_member.member_id)
        assert len(session.pharmacy_claims) == 1

        # Try adding to nonexistent member
        result = session_manager.add_claim("nonexistent", sample_pharmacy_claim)
        assert result is False


class TestRxMemberSessionManagerWorkspace:
    """Tests for workspace save/load operations."""

    @pytest.fixture
    def session_manager(self, temp_workspace_dir):
        """Create session manager with temp directory."""
        return RxMemberSessionManager(workspace_dir=temp_workspace_dir)

    def test_save_workspace(
        self, session_manager, sample_rx_member, sample_pharmacy_claim
    ):
        """Test saving workspace."""
        session_manager.add_rx_member(
            sample_rx_member,
            pharmacy_claims=[sample_pharmacy_claim],
            provenance=Provenance.generated(skill_used="test"),
        )

        workspace = session_manager.save_workspace(
            name="Test Workspace",
            description="Testing save",
            tags=["test"],
        )

        assert workspace.metadata.name == "Test Workspace"
        assert workspace.metadata.product == "rxmembersim"
        assert workspace.get_entity_count("rx_members") == 1
        assert workspace.get_entity_count("pharmacy_claims") == 1

    def test_save_and_load_workspace(
        self, session_manager, sample_rx_member, sample_pharmacy_claim, temp_workspace_dir
    ):
        """Test saving and loading workspace."""
        session_manager.add_rx_member(
            sample_rx_member, pharmacy_claims=[sample_pharmacy_claim]
        )
        workspace = session_manager.save_workspace(name="Load Test")
        session_manager.clear()

        # Load by ID
        loaded, stats = session_manager.load_workspace(
            workspace_id=workspace.metadata.workspace_id
        )

        assert loaded.metadata.name == "Load Test"
        assert stats["rx_members_loaded"] == 1
        assert session_manager.count() == 1

    def test_load_workspace_by_name(
        self, session_manager, sample_rx_member, temp_workspace_dir
    ):
        """Test loading workspace by name."""
        session_manager.add_rx_member(sample_rx_member)
        session_manager.save_workspace(name="Named Workspace")
        session_manager.clear()

        loaded, _ = session_manager.load_workspace(name="Named")

        assert "Named Workspace" in loaded.metadata.name
        assert session_manager.count() == 1

    def test_list_workspaces(
        self, session_manager, sample_rx_member, temp_workspace_dir
    ):
        """Test listing workspaces."""
        session_manager.add_rx_member(sample_rx_member)

        session_manager.save_workspace(name="Workspace 1", tags=["test"])
        session_manager.save_workspace(name="Workspace 2")

        workspaces = session_manager.list_workspaces()

        assert len(workspaces) == 2
        names = [w["name"] for w in workspaces]
        assert "Workspace 1" in names

        # Filter by tag
        tagged = session_manager.list_workspaces(tags=["test"])
        assert len(tagged) == 1

    def test_delete_workspace(
        self, session_manager, sample_rx_member, temp_workspace_dir
    ):
        """Test deleting workspace."""
        session_manager.add_rx_member(sample_rx_member)
        workspace = session_manager.save_workspace(name="To Delete")

        result = session_manager.delete_workspace(workspace.metadata.workspace_id)

        assert result is not None
        assert result["name"] == "To Delete"

        # Verify deleted
        workspaces = session_manager.list_workspaces()
        assert len(workspaces) == 0

    def test_workspace_summary(
        self, session_manager, sample_rx_member, sample_pharmacy_claim
    ):
        """Test workspace summary."""
        # Empty summary
        empty_summary = session_manager.workspace_summary()
        assert empty_summary["status"] == "empty"

        # With data
        session_manager.add_rx_member(
            sample_rx_member, pharmacy_claims=[sample_pharmacy_claim]
        )
        summary = session_manager.workspace_summary()

        assert summary["status"] == "active"
        assert summary["product"] == "rxmembersim"
        assert summary["session_count"] == 1
        assert "rx_members" in summary["entity_counts"]
