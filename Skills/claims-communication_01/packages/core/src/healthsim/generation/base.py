"""Base generator classes.

Provides the foundation for building data generators with
reproducibility and common generation utilities.
"""

import uuid
from datetime import date, datetime, timedelta

from healthsim.generation.distributions import WeightedChoice
from healthsim.generation.reproducibility import SeedManager
from healthsim.person.demographics import (
    Address,
    ContactInfo,
    Gender,
    Person,
    PersonName,
)
from healthsim.temporal.utils import random_date_in_range


class BaseGenerator:
    """Base class for data generators.

    Provides common utilities for generating data with reproducibility.
    Products should extend this class to add domain-specific generation.

    Attributes:
        seed_manager: Manages random seeds for reproducibility
        faker: Faker instance for generating realistic data

    Example:
        >>> class MyGenerator(BaseGenerator):
        ...     def generate_item(self) -> dict:
        ...         return {
        ...             "id": self.generate_id("ITEM"),
        ...             "name": self.faker.word()
        ...         }
        ...
        >>> gen = MyGenerator(seed=42)
        >>> gen.generate_item()
        {'id': 'ITEM-a1b2c3d4', 'name': 'word'}
    """

    def __init__(self, seed: int | None = None, locale: str = "en_US") -> None:
        """Initialize the generator.

        Args:
            seed: Random seed for reproducibility (None for random)
            locale: Locale for Faker
        """
        self.seed_manager = SeedManager(seed=seed, locale=locale)
        self.faker = self.seed_manager.faker

    @property
    def rng(self):
        """Get the random number generator."""
        return self.seed_manager.rng

    def reset(self) -> None:
        """Reset the generator to initial seed state."""
        self.seed_manager.reset()
        # Update faker reference since seed_manager.reset() creates a new instance
        self.faker = self.seed_manager.faker

    def generate_id(self, prefix: str = "") -> str:
        """Generate a unique identifier.

        Args:
            prefix: Prefix for the ID (e.g., "PERSON", "ORDER")

        Returns:
            Unique identifier string
        """
        unique_part = uuid.uuid4().hex[:8].upper()
        if prefix:
            return f"{prefix}-{unique_part}"
        return unique_part

    def random_choice(self, options: list) -> any:
        """Select randomly from a list.

        Args:
            options: List of options

        Returns:
            Randomly selected item
        """
        return self.seed_manager.get_random_choice(options)

    def random_int(self, min_val: int, max_val: int) -> int:
        """Generate random integer in range.

        Args:
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)

        Returns:
            Random integer
        """
        return self.seed_manager.get_random_int(min_val, max_val)

    def random_float(self, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Generate random float in range.

        Args:
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Random float
        """
        return self.seed_manager.get_random_float(min_val, max_val)

    def random_bool(self, probability: float = 0.5) -> bool:
        """Generate random boolean.

        Args:
            probability: Probability of True (0.0 to 1.0)

        Returns:
            Random boolean
        """
        return self.seed_manager.get_random_bool(probability)

    def weighted_choice(self, options: list[tuple[any, float]]) -> any:
        """Select from weighted options.

        Args:
            options: List of (item, weight) tuples

        Returns:
            Selected item
        """
        wc = WeightedChoice(options=options)
        return wc.select(self.rng)

    def random_date_between(self, start: date, end: date) -> date:
        """Generate random date in range.

        Args:
            start: Start date (inclusive)
            end: End date (inclusive)

        Returns:
            Random date in range
        """
        return random_date_in_range(start, end, self.rng)

    def random_datetime_between(self, start: datetime, end: datetime) -> datetime:
        """Generate random datetime in range.

        Args:
            start: Start datetime (inclusive)
            end: End datetime (inclusive)

        Returns:
            Random datetime in range
        """
        delta = end - start
        random_seconds = self.rng.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)


class PersonGenerator(BaseGenerator):
    """Generator for Person instances.

    Generates realistic person data including names, addresses,
    and contact information.

    Example:
        >>> gen = PersonGenerator(seed=42)
        >>> person = gen.generate_person(age_range=(25, 65))
        >>> print(f"{person.full_name}, age {person.age}")
        John Smith, age 42
    """

    def generate_person(
        self,
        age_range: tuple[int, int] | None = None,
        gender: Gender | None = None,
        include_address: bool = True,
        include_contact: bool = True,
    ) -> Person:
        """Generate a random person.

        Args:
            age_range: (min_age, max_age) or None for default (18, 85)
            gender: Specific gender or None for random
            include_address: Whether to generate address
            include_contact: Whether to generate contact info

        Returns:
            Generated Person instance
        """
        if age_range is None:
            age_range = (18, 85)

        # Generate gender
        if gender is None:
            gender = self.random_choice([Gender.MALE, Gender.FEMALE])

        # Generate name based on gender
        name = self.generate_name(gender)

        # Generate birth date based on age range
        birth_date = self.generate_birth_date(age_range)

        # Generate optional components
        address = self.generate_address() if include_address else None
        contact = self.generate_contact() if include_contact else None

        return Person(
            id=self.generate_id("PERSON"),
            name=name,
            birth_date=birth_date,
            gender=gender,
            address=address,
            contact=contact,
        )

    def generate_name(self, gender: Gender | None = None) -> PersonName:
        """Generate a random person name.

        Args:
            gender: Gender for name generation

        Returns:
            Generated PersonName
        """
        if gender == Gender.MALE:
            given_name = self.faker.first_name_male()
        elif gender == Gender.FEMALE:
            given_name = self.faker.first_name_female()
        else:
            given_name = self.faker.first_name()

        # Sometimes add middle name (50% chance)
        middle_name = self.faker.first_name() if self.random_bool(0.5) else None

        return PersonName(
            given_name=given_name,
            middle_name=middle_name,
            family_name=self.faker.last_name(),
        )

    def generate_birth_date(self, age_range: tuple[int, int]) -> date:
        """Generate a random birth date within age range.

        Args:
            age_range: (min_age, max_age) in years

        Returns:
            Generated birth date
        """
        min_age, max_age = age_range
        today = date.today()

        # Calculate date range
        max_birth_date = today - timedelta(days=min_age * 365)
        min_birth_date = today - timedelta(days=max_age * 365)

        return self.random_date_between(min_birth_date, max_birth_date)

    def generate_address(self) -> Address:
        """Generate a random address.

        Returns:
            Generated Address
        """
        return Address(
            street_address=self.faker.street_address(),
            city=self.faker.city(),
            state=self.faker.state_abbr(),
            postal_code=self.faker.postcode(),
            country="US",
        )

    def generate_contact(self) -> ContactInfo:
        """Generate random contact information.

        Returns:
            Generated ContactInfo
        """
        return ContactInfo(
            phone=self.faker.phone_number(),
            phone_mobile=self.faker.phone_number() if self.random_bool(0.7) else None,
            email=self.faker.email(),
        )

    def generate_ssn(self) -> str:
        """Generate a random SSN-formatted string.

        Note: This generates fake SSNs for testing only.

        Returns:
            SSN-formatted string (XXX-XX-XXXX)
        """
        return self.faker.ssn()
