"""Shared test fixtures for MemberSim."""

from datetime import date
from decimal import Decimal

import pytest
from healthsim.person import Address, Gender, PersonName

from membersim import Claim, ClaimLine, Member, Plan, Provider


@pytest.fixture
def seed() -> int:
    """Fixed seed for reproducible tests."""
    return 42


@pytest.fixture
def sample_address() -> Address:
    """Sample address for testing."""
    return Address(
        street_address="123 Main St",
        city="Anytown",
        state="CA",
        postal_code="90210",
    )


@pytest.fixture
def sample_name() -> PersonName:
    """Sample person name for testing."""
    return PersonName(
        given_name="John",
        family_name="Smith",
    )


@pytest.fixture
def sample_member(sample_name: PersonName, sample_address: Address) -> Member:
    """Sample member for testing."""
    return Member(
        id="person-001",
        name=sample_name,
        birth_date=date(1980, 5, 15),
        gender=Gender.MALE,
        address=sample_address,
        member_id="MEM001",
        relationship_code="18",
        group_id="GRP001",
        coverage_start=date(2024, 1, 1),
        plan_code="PPO_GOLD",
    )


@pytest.fixture
def sample_plan() -> Plan:
    """Sample PPO plan for testing."""
    return Plan(
        plan_code="TEST_PPO",
        plan_name="Test PPO Plan",
        plan_type="PPO",
        deductible_individual=Decimal("500"),
        deductible_family=Decimal("1000"),
        oop_max_individual=Decimal("3000"),
        oop_max_family=Decimal("6000"),
        copay_pcp=Decimal("25"),
        copay_specialist=Decimal("50"),
        copay_er=Decimal("200"),
        coinsurance=Decimal("0.20"),
    )


@pytest.fixture
def sample_provider(sample_address: Address) -> Provider:
    """Sample provider for testing."""
    return Provider(
        npi="1234567890",
        tax_id="12-3456789",
        name="Dr. Jane Doe",
        specialty="207Q00000X",  # Family Medicine
        address=sample_address,
        effective_date=date(2020, 1, 1),
    )


@pytest.fixture
def sample_claim(sample_member: Member) -> Claim:
    """Sample claim for testing."""
    return Claim(
        claim_id="CLM001",
        claim_type="PROFESSIONAL",
        member_id=sample_member.member_id,
        subscriber_id=sample_member.member_id,
        provider_npi="1234567890",
        service_date=date(2024, 3, 15),
        place_of_service="11",
        principal_diagnosis="E11.9",  # Type 2 diabetes
        claim_lines=[
            ClaimLine(
                line_number=1,
                procedure_code="99213",  # Office visit
                service_date=date(2024, 3, 15),
                charge_amount=Decimal("150.00"),
            ),
        ],
    )
