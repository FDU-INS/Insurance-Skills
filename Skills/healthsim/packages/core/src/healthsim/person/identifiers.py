"""Person identifier management.

Provides classes for managing various types of identifiers
associated with a person.
"""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class IdentifierType(str, Enum):
    """Types of identifiers.

    Products can extend this with domain-specific types.

    Attributes:
        SSN: Social Security Number
        DRIVERS_LICENSE: Driver's license number
        PASSPORT: Passport number
        NATIONAL_ID: National ID number
        TAX_ID: Tax identification number
        CUSTOM: Custom/domain-specific identifier
    """

    SSN = "SSN"
    DRIVERS_LICENSE = "DL"
    PASSPORT = "PASSPORT"
    NATIONAL_ID = "NATIONAL_ID"
    TAX_ID = "TAX_ID"
    CUSTOM = "CUSTOM"


class Identifier(BaseModel):
    """An identifier for a person.

    Represents a single identifier with its type, value, and metadata.

    Attributes:
        type: Type of identifier
        value: The identifier value
        system: System/namespace for the identifier (optional)
        issuer: Issuing authority (optional)
        issue_date: When the identifier was issued (optional)
        expiry_date: When the identifier expires (optional)
        is_primary: Whether this is the primary identifier of its type

    Example:
        >>> id_ssn = Identifier(
        ...     type=IdentifierType.SSN,
        ...     value="123-45-6789",
        ...     system="http://ssa.gov/ssn"
        ... )
        >>> id_dl = Identifier(
        ...     type=IdentifierType.DRIVERS_LICENSE,
        ...     value="D12345678",
        ...     issuer="MA RMV",
        ...     issue_date=date(2020, 1, 15),
        ...     expiry_date=date(2025, 1, 15)
        ... )
    """

    type: IdentifierType
    value: str
    system: str | None = None
    issuer: str | None = None
    issue_date: date | None = None
    expiry_date: date | None = None
    is_primary: bool = True

    @property
    def is_expired(self) -> bool:
        """Check if the identifier is expired."""
        if self.expiry_date is None:
            return False
        return date.today() > self.expiry_date

    @property
    def is_valid(self) -> bool:
        """Check if the identifier is currently valid.

        An identifier is valid if it has been issued (issue_date <= today)
        and has not expired.
        """
        today = date.today()

        if self.issue_date and self.issue_date > today:
            return False

        if self.expiry_date and self.expiry_date < today:
            return False

        return True


class IdentifierSet(BaseModel):
    """Collection of identifiers for a person.

    Manages multiple identifiers and provides lookup methods.

    Attributes:
        identifiers: List of identifiers

    Example:
        >>> ids = IdentifierSet()
        >>> ids.add(Identifier(type=IdentifierType.SSN, value="123-45-6789"))
        >>> ids.get_by_type(IdentifierType.SSN)
        Identifier(type=<IdentifierType.SSN: 'SSN'>, value='123-45-6789', ...)
    """

    identifiers: list[Identifier] = Field(default_factory=list)

    def add(self, identifier: Identifier) -> None:
        """Add an identifier to the set.

        Args:
            identifier: Identifier to add
        """
        self.identifiers.append(identifier)

    def get_by_type(self, id_type: IdentifierType) -> Identifier | None:
        """Get the primary identifier of a specific type.

        Args:
            id_type: Type of identifier to find

        Returns:
            Primary identifier of that type, or None if not found
        """
        for identifier in self.identifiers:
            if identifier.type == id_type and identifier.is_primary:
                return identifier
        # Fall back to any identifier of that type
        for identifier in self.identifiers:
            if identifier.type == id_type:
                return identifier
        return None

    def get_all_by_type(self, id_type: IdentifierType) -> list[Identifier]:
        """Get all identifiers of a specific type.

        Args:
            id_type: Type of identifier to find

        Returns:
            List of identifiers of that type
        """
        return [i for i in self.identifiers if i.type == id_type]

    def get_by_system(self, system: str) -> Identifier | None:
        """Get identifier by system/namespace.

        Args:
            system: System URI to match

        Returns:
            Identifier with matching system, or None
        """
        for identifier in self.identifiers:
            if identifier.system == system:
                return identifier
        return None

    def __len__(self) -> int:
        """Return number of identifiers."""
        return len(self.identifiers)

    def __iter__(self):
        """Iterate over identifiers."""
        return iter(self.identifiers)
