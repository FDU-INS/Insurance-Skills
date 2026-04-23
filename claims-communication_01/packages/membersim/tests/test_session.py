"""Tests for MemberSim session management."""

from datetime import date

import pytest
from healthsim.state import Provenance

from membersim.claims.claim import Claim, ClaimLine
from membersim.core.member import MemberFactory
from membersim.mcp.session import MemberSession, MemberSessionManager


@pytest.fixture
def member_factory():
    """Create a member factory with fixed seed."""
    return MemberFactory(seed=42)


@pytest.fixture
def sample_member(member_factory):
    """Generate a sample member."""
    return member_factory.generate_one()


@pytest.fixture
def sample_claim(sample_member):
    """Create a sample claim for the member."""
    from decimal import Decimal

    line = ClaimLine(
        line_number=1,
        procedure_code="99213",
        charge_amount=Decimal("150.00"),
        units=Decimal("1"),
        service_date=date(2024, 6, 15),
        diagnosis_pointers=[1],
    )

    return Claim(
        claim_id="CLM000001",
        member_id=sample_member.member_id,
        subscriber_id=sample_member.member_id,
        provider_npi="1234567890",
        service_date=date(2024, 6, 15),
        claim_type="PROFESSIONAL",
        principal_diagnosis="J06.9",
        claim_lines=[line],
    )


@pytest.fixture
def temp_workspace_dir(tmp_path):
    """Create temporary workspace directory."""
    return tmp_path


@pytest.fixture
def session_manager(temp_workspace_dir):
    """Create a session manager with temp directory."""
    return MemberSessionManager(workspace_dir=temp_workspace_dir)


class TestMemberSession:
    """Tests for MemberSession class."""

    def test_create_session_minimal(self, sample_member):
        """Test creating session with just a member."""
        session = MemberSession(member=sample_member)

        assert session.id is not None
        assert len(session.id) == 8
        assert session.member == sample_member
        assert session.primary_entity == sample_member
        assert session.claims == []
        assert session.authorizations == []
        assert session.care_gaps == []

    def test_create_session_with_claims(self, sample_member, sample_claim):
        """Test creating session with claims."""
        session = MemberSession(
            member=sample_member,
            claims=[sample_claim],
        )

        assert len(session.claims) == 1
        assert session.claims[0].claim_id == "CLM000001"

    def test_to_summary(self, sample_member, sample_claim):
        """Test summary generation."""
        session = MemberSession(
            member=sample_member,
            claims=[sample_claim],
        )

        summary = session.to_summary()

        assert "id" in summary
        assert "member_id" in summary
        assert "name" in summary
        assert "plan_code" in summary
        assert summary["claims_count"] == 1

    def test_to_entities_with_provenance(self, sample_member, sample_claim):
        """Test conversion to entities with provenance."""
        session = MemberSession(
            member=sample_member,
            claims=[sample_claim],
            provenance=Provenance.generated(skill_used="test"),
        )

        entities = session.to_entities_with_provenance()

        assert "members" in entities
        assert len(entities["members"]) == 1
        assert entities["members"][0].entity_type == "members"

        assert "claims" in entities
        assert len(entities["claims"]) == 1

    def test_from_entities_with_provenance(self, sample_member, sample_claim):
        """Test reconstructing session from entities."""
        original = MemberSession(
            member=sample_member,
            claims=[sample_claim],
        )

        entities = original.to_entities_with_provenance()
        member_entity = entities["members"][0]

        reconstructed = MemberSession.from_entities_with_provenance(
            member_entity, entities
        )

        assert reconstructed.member.member_id == original.member.member_id
        assert len(reconstructed.claims) == 1
        assert reconstructed.claims[0].claim_id == "CLM000001"


class TestMemberSessionManager:
    """Tests for MemberSessionManager class."""

    def test_product_name(self, session_manager):
        """Test product name is correct."""
        assert session_manager.product_name == "membersim"

    def test_add_and_count(self, session_manager, sample_member):
        """Test adding members and counting."""
        assert session_manager.count() == 0

        session_manager.add_member(sample_member)
        assert session_manager.count() == 1

    def test_clear(self, session_manager, sample_member):
        """Test clearing all sessions."""
        session_manager.add_member(sample_member)
        assert session_manager.count() == 1

        session_manager.clear()
        assert session_manager.count() == 0

    def test_get_by_member_id(self, session_manager, sample_member):
        """Test getting session by member ID."""
        session_manager.add_member(sample_member)

        found = session_manager.get_by_member_id(sample_member.member_id)
        assert found is not None
        assert found.member.member_id == sample_member.member_id

        not_found = session_manager.get_by_member_id("nonexistent")
        assert not_found is None

    def test_get_latest(self, session_manager, member_factory):
        """Test getting latest session."""
        m1 = member_factory.generate_one()
        m2 = member_factory.generate_one()

        session_manager.add_member(m1)
        session_manager.add_member(m2)

        latest = session_manager.get_latest()
        assert latest is not None
        assert latest.member.member_id == m2.member_id

    def test_add_claim(self, session_manager, sample_member, sample_claim):
        """Test adding claim to member session."""
        session_manager.add_member(sample_member)

        result = session_manager.add_claim(sample_member.member_id, sample_claim)
        assert result is True

        session = session_manager.get_by_member_id(sample_member.member_id)
        assert len(session.claims) == 1

        # Try adding to nonexistent member
        result = session_manager.add_claim("nonexistent", sample_claim)
        assert result is False


class TestMemberSessionManagerWorkspace:
    """Tests for workspace save/load operations."""

    @pytest.fixture
    def session_manager(self, temp_workspace_dir):
        """Create session manager with temp directory."""
        return MemberSessionManager(workspace_dir=temp_workspace_dir)

    def test_save_workspace(self, session_manager, sample_member, sample_claim):
        """Test saving workspace."""
        session_manager.add_member(
            sample_member,
            claims=[sample_claim],
            provenance=Provenance.generated(skill_used="test"),
        )

        workspace = session_manager.save_workspace(
            name="Test Workspace",
            description="Testing save",
            tags=["test"],
        )

        assert workspace.metadata.name == "Test Workspace"
        assert workspace.metadata.product == "membersim"
        assert workspace.get_entity_count("members") == 1
        assert workspace.get_entity_count("claims") == 1

    def test_save_and_load_workspace(
        self, session_manager, sample_member, sample_claim, temp_workspace_dir
    ):
        """Test saving and loading workspace."""
        session_manager.add_member(sample_member, claims=[sample_claim])
        workspace = session_manager.save_workspace(name="Load Test")
        session_manager.clear()

        # Load by ID
        loaded, stats = session_manager.load_workspace(
            workspace_id=workspace.metadata.workspace_id
        )

        assert loaded.metadata.name == "Load Test"
        assert stats["members_loaded"] == 1
        assert session_manager.count() == 1

    def test_load_workspace_by_name(
        self, session_manager, sample_member, temp_workspace_dir
    ):
        """Test loading workspace by name."""
        session_manager.add_member(sample_member)
        session_manager.save_workspace(name="Named Workspace")
        session_manager.clear()

        loaded, _ = session_manager.load_workspace(name="Named")

        assert "Named Workspace" in loaded.metadata.name
        assert session_manager.count() == 1

    def test_list_workspaces(
        self, session_manager, sample_member, temp_workspace_dir
    ):
        """Test listing workspaces."""
        session_manager.add_member(sample_member)

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
        self, session_manager, sample_member, temp_workspace_dir
    ):
        """Test deleting workspace."""
        session_manager.add_member(sample_member)
        workspace = session_manager.save_workspace(name="To Delete")

        result = session_manager.delete_workspace(workspace.metadata.workspace_id)

        assert result is not None
        assert result["name"] == "To Delete"

        # Verify deleted
        workspaces = session_manager.list_workspaces()
        assert len(workspaces) == 0

    def test_workspace_summary(self, session_manager, sample_member, sample_claim):
        """Test workspace summary."""
        # Empty summary
        empty_summary = session_manager.workspace_summary()
        assert empty_summary["status"] == "empty"

        # With data
        session_manager.add_member(sample_member, claims=[sample_claim])
        summary = session_manager.workspace_summary()

        assert summary["status"] == "active"
        assert summary["product"] == "membersim"
        assert summary["session_count"] == 1
        assert "members" in summary["entity_counts"]
