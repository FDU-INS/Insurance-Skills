"""Person demographics models.

Provides models for representing person demographics including
name, address, contact information, and core attributes.
"""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator

from healthsim.temporal.utils import calculate_age


class Gender(str, Enum):
    """Gender representation.

    Follows common standards for gender coding in data systems.

    Attributes:
        MALE: Male gender (M)
        FEMALE: Female gender (F)
        OTHER: Other gender identity (O)
        UNKNOWN: Unknown or not specified (U)
    """

    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    UNKNOWN = "U"


class PersonName(BaseModel):
    """Name components for a person.

    Attributes:
        given_name: First/given name
        middle_name: Middle name (optional)
        family_name: Last/family name
        suffix: Name suffix like Jr., Sr., III (optional)
        prefix: Name prefix like Dr., Mr., Mrs. (optional)

    Example:
        >>> name = PersonName(
        ...     given_name="John",
        ...     middle_name="Robert",
        ...     family_name="Smith",
        ...     suffix="Jr."
        ... )
        >>> name.full_name
        'John Robert Smith Jr.'
    """

    given_name: str
    middle_name: str | None = None
    family_name: str
    suffix: str | None = None
    prefix: str | None = None

    @property
    def full_name(self) -> str:
        """Get the complete formatted name."""
        parts = []
        if self.prefix:
            parts.append(self.prefix)
        parts.append(self.given_name)
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.family_name)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts)

    @property
    def formal_name(self) -> str:
        """Get formal name (Family, Given)."""
        return f"{self.family_name}, {self.given_name}"


class Address(BaseModel):
    """Physical address.

    Attributes:
        street_address: Street address line
        street_address_2: Additional address line (apt, suite, etc.)
        city: City name
        state: State/province code
        postal_code: ZIP/postal code
        country: Country code (defaults to US)

    Example:
        >>> addr = Address(
        ...     street_address="123 Main St",
        ...     city="Boston",
        ...     state="MA",
        ...     postal_code="02101"
        ... )
    """

    street_address: str | None = None
    street_address_2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str = "US"

    @property
    def one_line(self) -> str:
        """Get address as a single line."""
        parts = []
        if self.street_address:
            parts.append(self.street_address)
        if self.street_address_2:
            parts.append(self.street_address_2)
        if self.city:
            parts.append(self.city)
        if self.state and self.postal_code:
            parts.append(f"{self.state} {self.postal_code}")
        elif self.state:
            parts.append(self.state)
        elif self.postal_code:
            parts.append(self.postal_code)
        return ", ".join(parts)


class ContactInfo(BaseModel):
    """Contact information for a person.

    Attributes:
        phone: Primary phone number
        phone_mobile: Mobile phone number
        phone_work: Work phone number
        email: Email address
        email_work: Work email address

    Example:
        >>> contact = ContactInfo(
        ...     phone="617-555-1234",
        ...     email="john.smith@email.com"
        ... )
    """

    phone: str | None = None
    phone_mobile: str | None = None
    phone_work: str | None = None
    email: str | None = None
    email_work: str | None = None

    @property
    def primary_phone(self) -> str | None:
        """Get primary phone (mobile > phone > work)."""
        return self.phone_mobile or self.phone or self.phone_work

    @property
    def primary_email(self) -> str | None:
        """Get primary email (personal > work)."""
        return self.email or self.email_work


class Person(BaseModel):
    """Base person model with demographics.

    This is the foundational model for representing a person in HealthSim.
    Products should extend this class to add domain-specific fields.

    Attributes:
        id: Unique identifier for this person
        name: Person's name components
        birth_date: Date of birth
        gender: Gender
        address: Physical address (optional)
        contact: Contact information (optional)
        deceased: Whether person is deceased
        death_date: Date of death if deceased

    Example:
        >>> person = Person(
        ...     id="person-001",
        ...     name=PersonName(given_name="John", family_name="Smith"),
        ...     birth_date=date(1980, 6, 15),
        ...     gender=Gender.MALE
        ... )
        >>> person.age
        44  # depends on current date
    """

    id: str = Field(..., description="Unique identifier")
    name: PersonName
    birth_date: date
    gender: Gender
    address: Address | None = None
    contact: ContactInfo | None = None
    deceased: bool = False
    death_date: date | None = None

    @field_validator("birth_date")
    @classmethod
    def birth_date_not_future(cls, v: date) -> date:
        """Ensure birth date is not in the future."""
        if v > date.today():
            raise ValueError("birth_date cannot be in the future")
        return v

    @model_validator(mode="after")
    def validate_death_date(self) -> "Person":
        """Validate death date consistency."""
        if self.death_date:
            if not self.deceased:
                raise ValueError("death_date set but deceased is False")
            if self.death_date < self.birth_date:
                raise ValueError("death_date cannot be before birth_date")
            if self.death_date > date.today():
                raise ValueError("death_date cannot be in the future")
        if self.deceased and not self.death_date:
            # Deceased without date is allowed (date unknown)
            pass
        return self

    @property
    def age(self) -> int:
        """Calculate current age in years."""
        as_of = self.death_date if self.deceased and self.death_date else date.today()
        return calculate_age(self.birth_date, as_of)

    @property
    def full_name(self) -> str:
        """Get the person's full name."""
        return self.name.full_name

    @property
    def given_name(self) -> str:
        """Get the person's given/first name."""
        return self.name.given_name

    @property
    def family_name(self) -> str:
        """Get the person's family/last name."""
        return self.name.family_name
