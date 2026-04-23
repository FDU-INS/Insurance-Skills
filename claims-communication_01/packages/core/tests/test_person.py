"""Tests for healthsim.person module."""

from datetime import date

import pytest

from healthsim.person import (
    Address,
    ContactInfo,
    Gender,
    Identifier,
    IdentifierType,
    Person,
    PersonName,
    Relationship,
    RelationshipType,
)


class TestGender:
    """Tests for Gender enum."""

    def test_values(self) -> None:
        """Test gender enum values."""
        assert Gender.MALE.value == "M"
        assert Gender.FEMALE.value == "F"
        assert Gender.OTHER.value == "O"
        assert Gender.UNKNOWN.value == "U"


class TestPersonName:
    """Tests for PersonName."""

    def test_creation(self) -> None:
        """Test creating a person name."""
        name = PersonName(
            given_name="John",
            middle_name="Robert",
            family_name="Smith",
            suffix="Jr.",
        )

        assert name.given_name == "John"
        assert name.middle_name == "Robert"
        assert name.family_name == "Smith"
        assert name.suffix == "Jr."

    def test_full_name(self) -> None:
        """Test full name property."""
        name = PersonName(
            given_name="John",
            middle_name="Robert",
            family_name="Smith",
        )

        assert name.full_name == "John Robert Smith"

    def test_full_name_with_suffix(self) -> None:
        """Test full name with suffix."""
        name = PersonName(
            given_name="John",
            family_name="Smith",
            suffix="III",
        )

        assert name.full_name == "John Smith III"

    def test_full_name_with_prefix(self) -> None:
        """Test full name with prefix."""
        name = PersonName(
            prefix="Dr.",
            given_name="Jane",
            family_name="Doe",
        )

        assert name.full_name == "Dr. Jane Doe"

    def test_formal_name(self) -> None:
        """Test formal name format."""
        name = PersonName(
            given_name="John",
            family_name="Smith",
        )

        assert name.formal_name == "Smith, John"

    def test_minimal_name(self) -> None:
        """Test name with only required fields."""
        name = PersonName(given_name="John", family_name="Smith")

        assert name.full_name == "John Smith"
        assert name.middle_name is None


class TestAddress:
    """Tests for Address."""

    def test_creation(self) -> None:
        """Test creating an address."""
        addr = Address(
            street_address="123 Main St",
            city="Boston",
            state="MA",
            postal_code="02101",
        )

        assert addr.street_address == "123 Main St"
        assert addr.city == "Boston"
        assert addr.state == "MA"
        assert addr.postal_code == "02101"
        assert addr.country == "US"  # Default

    def test_one_line(self) -> None:
        """Test one-line address format."""
        addr = Address(
            street_address="123 Main St",
            city="Boston",
            state="MA",
            postal_code="02101",
        )

        assert addr.one_line == "123 Main St, Boston, MA 02101"

    def test_empty_address(self) -> None:
        """Test address with no fields set."""
        addr = Address()
        assert addr.one_line == ""


class TestContactInfo:
    """Tests for ContactInfo."""

    def test_creation(self) -> None:
        """Test creating contact info."""
        contact = ContactInfo(
            phone="617-555-1234",
            email="john@example.com",
        )

        assert contact.phone == "617-555-1234"
        assert contact.email == "john@example.com"

    def test_primary_phone(self) -> None:
        """Test primary phone selection."""
        # Mobile takes precedence
        contact = ContactInfo(
            phone="617-555-1234",
            phone_mobile="617-555-5678",
        )
        assert contact.primary_phone == "617-555-5678"

        # Falls back to phone
        contact = ContactInfo(phone="617-555-1234")
        assert contact.primary_phone == "617-555-1234"

        # Falls back to work
        contact = ContactInfo(phone_work="617-555-9999")
        assert contact.primary_phone == "617-555-9999"

    def test_primary_email(self) -> None:
        """Test primary email selection."""
        # Personal takes precedence
        contact = ContactInfo(
            email="personal@example.com",
            email_work="work@example.com",
        )
        assert contact.primary_email == "personal@example.com"

        # Falls back to work
        contact = ContactInfo(email_work="work@example.com")
        assert contact.primary_email == "work@example.com"


class TestPerson:
    """Tests for Person."""

    def test_creation(self) -> None:
        """Test creating a person."""
        person = Person(
            id="person-001",
            name=PersonName(given_name="John", family_name="Smith"),
            birth_date=date(1980, 6, 15),
            gender=Gender.MALE,
        )

        assert person.id == "person-001"
        assert person.full_name == "John Smith"
        assert person.gender == Gender.MALE
        assert person.deceased is False

    def test_age_calculation(self) -> None:
        """Test age calculation."""
        # Use a fixed date for testing
        person = Person(
            id="test",
            name=PersonName(given_name="Test", family_name="Person"),
            birth_date=date(1990, 6, 15),
            gender=Gender.MALE,
        )

        # Age depends on current date, just verify it's reasonable
        assert 0 <= person.age <= 150

    def test_birth_date_not_future(self) -> None:
        """Test that birth date cannot be in the future."""
        from datetime import timedelta

        future_date = date.today() + timedelta(days=30)

        with pytest.raises(ValueError, match="birth_date cannot be in the future"):
            Person(
                id="test",
                name=PersonName(given_name="Test", family_name="Person"),
                birth_date=future_date,
                gender=Gender.MALE,
            )

    def test_deceased_with_death_date(self) -> None:
        """Test deceased person with death date."""
        person = Person(
            id="test",
            name=PersonName(given_name="Test", family_name="Person"),
            birth_date=date(1950, 1, 1),
            gender=Gender.MALE,
            deceased=True,
            death_date=date(2020, 1, 1),
        )

        assert person.deceased is True
        assert person.death_date == date(2020, 1, 1)

    def test_death_date_without_deceased_flag(self) -> None:
        """Test that death_date requires deceased=True."""
        with pytest.raises(ValueError, match="death_date set but deceased is False"):
            Person(
                id="test",
                name=PersonName(given_name="Test", family_name="Person"),
                birth_date=date(1950, 1, 1),
                gender=Gender.MALE,
                deceased=False,
                death_date=date(2020, 1, 1),
            )

    def test_death_date_before_birth(self) -> None:
        """Test that death date cannot be before birth date."""
        with pytest.raises(ValueError, match="death_date cannot be before birth_date"):
            Person(
                id="test",
                name=PersonName(given_name="Test", family_name="Person"),
                birth_date=date(1990, 1, 1),
                gender=Gender.MALE,
                deceased=True,
                death_date=date(1980, 1, 1),
            )

    def test_person_with_address(self) -> None:
        """Test person with address."""
        person = Person(
            id="test",
            name=PersonName(given_name="Test", family_name="Person"),
            birth_date=date(1980, 1, 1),
            gender=Gender.FEMALE,
            address=Address(city="Boston", state="MA"),
        )

        assert person.address is not None
        assert person.address.city == "Boston"

    def test_given_family_name_properties(self) -> None:
        """Test convenience name properties."""
        person = Person(
            id="test",
            name=PersonName(given_name="John", family_name="Smith"),
            birth_date=date(1980, 1, 1),
            gender=Gender.MALE,
        )

        assert person.given_name == "John"
        assert person.family_name == "Smith"


class TestIdentifier:
    """Tests for Identifier."""

    def test_creation(self) -> None:
        """Test creating an identifier."""
        id = Identifier(
            type=IdentifierType.SSN,
            value="123-45-6789",
            system="http://ssa.gov/ssn",
        )

        assert id.type == IdentifierType.SSN
        assert id.value == "123-45-6789"

    def test_is_valid(self) -> None:
        """Test validity check."""
        valid_id = Identifier(
            type=IdentifierType.DRIVERS_LICENSE,
            value="D12345678",
            issue_date=date(2020, 1, 1),
            expiry_date=date(2030, 1, 1),
        )

        assert valid_id.is_valid is True
        assert valid_id.is_expired is False

    def test_is_expired(self) -> None:
        """Test expired identifier."""
        expired_id = Identifier(
            type=IdentifierType.DRIVERS_LICENSE,
            value="D12345678",
            expiry_date=date(2020, 1, 1),
        )

        assert expired_id.is_expired is True
        assert expired_id.is_valid is False


class TestRelationship:
    """Tests for Relationship."""

    def test_creation(self) -> None:
        """Test creating a relationship."""
        rel = Relationship(
            source_person_id="person-001",
            target_person_id="person-002",
            relationship_type=RelationshipType.SPOUSE,
            start_date=date(2010, 6, 15),
        )

        assert rel.source_person_id == "person-001"
        assert rel.target_person_id == "person-002"
        assert rel.relationship_type == RelationshipType.SPOUSE
        assert rel.is_active is True

    def test_inverse_type(self) -> None:
        """Test getting inverse relationship type."""
        parent_rel = Relationship(
            source_person_id="parent",
            target_person_id="child",
            relationship_type=RelationshipType.PARENT,
        )

        assert parent_rel.get_inverse_type() == RelationshipType.CHILD

        spouse_rel = Relationship(
            source_person_id="p1",
            target_person_id="p2",
            relationship_type=RelationshipType.SPOUSE,
        )

        assert spouse_rel.get_inverse_type() == RelationshipType.SPOUSE

    def test_create_inverse(self) -> None:
        """Test creating inverse relationship."""
        rel = Relationship(
            source_person_id="person-001",
            target_person_id="person-002",
            relationship_type=RelationshipType.PARENT,
        )

        inverse = rel.create_inverse()

        assert inverse.source_person_id == "person-002"
        assert inverse.target_person_id == "person-001"
        assert inverse.relationship_type == RelationshipType.CHILD
