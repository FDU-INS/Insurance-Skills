"""Person demographics and identity management.

This module provides the base Person model and related classes for
representing individuals in HealthSim applications.
"""

from healthsim.person.demographics import (
    Address,
    ContactInfo,
    Gender,
    Person,
    PersonName,
)
from healthsim.person.identifiers import Identifier, IdentifierType
from healthsim.person.relationships import Relationship, RelationshipType

__all__ = [
    # Demographics
    "Gender",
    "PersonName",
    "Address",
    "ContactInfo",
    "Person",
    # Identifiers
    "IdentifierType",
    "Identifier",
    # Relationships
    "RelationshipType",
    "Relationship",
]
