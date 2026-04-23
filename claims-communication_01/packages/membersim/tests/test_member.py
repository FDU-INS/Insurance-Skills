"""Tests for Member and Subscriber models."""

from datetime import date

from healthsim.person import Address, Gender, PersonName

from membersim import Member
from membersim.core.subscriber import Subscriber


def test_member_creation(sample_member: Member) -> None:
    """Test basic member creation."""
    assert sample_member.member_id == "MEM001"
    assert sample_member.is_subscriber
    assert sample_member.is_active


def test_member_full_name(sample_member: Member) -> None:
    """Test full name property."""
    assert sample_member.full_name == "John Smith"


def test_member_not_subscriber(sample_name: PersonName, sample_address: Address) -> None:
    """Test dependent member (not subscriber)."""
    member = Member(
        id="person-002",
        name=sample_name,
        birth_date=date(2010, 3, 20),
        gender=Gender.MALE,
        address=sample_address,
        member_id="MEM002",
        subscriber_id="MEM001",
        relationship_code="19",  # Child
        group_id="GRP001",
        coverage_start=date(2024, 1, 1),
        plan_code="PPO_GOLD",
    )
    assert not member.is_subscriber
    assert member.relationship_code == "19"


def test_member_coverage_inactive(sample_name: PersonName, sample_address: Address) -> None:
    """Test inactive coverage."""
    member = Member(
        id="person-003",
        name=sample_name,
        birth_date=date(1980, 5, 15),
        gender=Gender.MALE,
        address=sample_address,
        member_id="MEM003",
        relationship_code="18",
        group_id="GRP001",
        coverage_start=date(2023, 1, 1),
        coverage_end=date(2023, 12, 31),
        plan_code="PPO_GOLD",
    )
    assert not member.is_active


def test_subscriber_with_dependents(sample_name: PersonName, sample_address: Address) -> None:
    """Test subscriber with dependent members."""
    subscriber = Subscriber(
        id="person-001",
        name=sample_name,
        birth_date=date(1980, 5, 15),
        gender=Gender.MALE,
        address=sample_address,
        member_id="SUB001",
        relationship_code="18",
        group_id="GRP001",
        coverage_start=date(2024, 1, 1),
        plan_code="PPO_GOLD",
        employer_id="EMP001",
        hire_date=date(2023, 6, 1),
    )

    assert subscriber.family_size == 1
    assert len(subscriber.get_all_members()) == 1


def test_subscriber_family_size(sample_name: PersonName, sample_address: Address) -> None:
    """Test subscriber family size with dependents."""
    child_name = PersonName(given_name="Jane", family_name="Smith")
    child = Member(
        id="person-002",
        name=child_name,
        birth_date=date(2015, 8, 10),
        gender=Gender.FEMALE,
        address=sample_address,
        member_id="MEM002",
        subscriber_id="SUB001",
        relationship_code="19",  # Child
        group_id="GRP001",
        coverage_start=date(2024, 1, 1),
        plan_code="PPO_GOLD",
    )

    subscriber = Subscriber(
        id="person-001",
        name=sample_name,
        birth_date=date(1980, 5, 15),
        gender=Gender.MALE,
        address=sample_address,
        member_id="SUB001",
        relationship_code="18",
        group_id="GRP001",
        coverage_start=date(2024, 1, 1),
        plan_code="PPO_GOLD",
        employer_id="EMP001",
        hire_date=date(2023, 6, 1),
        dependents=[child],
    )

    assert subscriber.family_size == 2
    assert len(subscriber.get_all_members()) == 2
