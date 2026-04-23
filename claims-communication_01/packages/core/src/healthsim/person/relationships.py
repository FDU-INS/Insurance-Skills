"""Person relationship management.

Provides classes for modeling relationships between persons.
"""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class RelationshipType(str, Enum):
    """Types of relationships between persons.

    Products can extend this with domain-specific relationships.

    Attributes:
        SPOUSE: Married partner
        PARENT: Parent of
        CHILD: Child of
        SIBLING: Brother/sister
        GUARDIAN: Legal guardian
        DEPENDENT: Legal dependent
        EMERGENCY_CONTACT: Emergency contact
        EMPLOYER: Employer
        EMPLOYEE: Employee
        OTHER: Other relationship type
    """

    SPOUSE = "spouse"
    PARENT = "parent"
    CHILD = "child"
    SIBLING = "sibling"
    GUARDIAN = "guardian"
    DEPENDENT = "dependent"
    EMERGENCY_CONTACT = "emergency_contact"
    EMPLOYER = "employer"
    EMPLOYEE = "employee"
    OTHER = "other"


class Relationship(BaseModel):
    """A relationship between two persons.

    Represents a directional relationship from one person to another.

    Attributes:
        source_person_id: ID of the person this relationship is from
        target_person_id: ID of the related person
        relationship_type: Type of relationship
        start_date: When the relationship started (optional)
        end_date: When the relationship ended (optional)
        is_active: Whether the relationship is currently active
        notes: Additional notes about the relationship

    Example:
        >>> rel = Relationship(
        ...     source_person_id="person-001",
        ...     target_person_id="person-002",
        ...     relationship_type=RelationshipType.SPOUSE,
        ...     start_date=date(2010, 6, 15)
        ... )
    """

    source_person_id: str
    target_person_id: str
    relationship_type: RelationshipType
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool = True
    notes: str | None = None

    @property
    def is_current(self) -> bool:
        """Check if the relationship is currently active."""
        if not self.is_active:
            return False
        if self.end_date and self.end_date <= date.today():
            return False
        return True

    def get_inverse_type(self) -> RelationshipType:
        """Get the inverse relationship type.

        For example, if this is a PARENT relationship, the inverse is CHILD.

        Returns:
            The inverse relationship type
        """
        inverses = {
            RelationshipType.PARENT: RelationshipType.CHILD,
            RelationshipType.CHILD: RelationshipType.PARENT,
            RelationshipType.SPOUSE: RelationshipType.SPOUSE,
            RelationshipType.SIBLING: RelationshipType.SIBLING,
            RelationshipType.GUARDIAN: RelationshipType.DEPENDENT,
            RelationshipType.DEPENDENT: RelationshipType.GUARDIAN,
            RelationshipType.EMPLOYER: RelationshipType.EMPLOYEE,
            RelationshipType.EMPLOYEE: RelationshipType.EMPLOYER,
            RelationshipType.EMERGENCY_CONTACT: RelationshipType.OTHER,
            RelationshipType.OTHER: RelationshipType.OTHER,
        }
        return inverses.get(self.relationship_type, RelationshipType.OTHER)

    def create_inverse(self) -> "Relationship":
        """Create the inverse relationship.

        Returns:
            A new Relationship representing the inverse
        """
        return Relationship(
            source_person_id=self.target_person_id,
            target_person_id=self.source_person_id,
            relationship_type=self.get_inverse_type(),
            start_date=self.start_date,
            end_date=self.end_date,
            is_active=self.is_active,
            notes=self.notes,
        )


class RelationshipGraph(BaseModel):
    """Graph of relationships between persons.

    Manages a collection of relationships and provides query methods.

    Attributes:
        relationships: List of all relationships

    Example:
        >>> graph = RelationshipGraph()
        >>> graph.add_relationship(Relationship(
        ...     source_person_id="person-001",
        ...     target_person_id="person-002",
        ...     relationship_type=RelationshipType.SPOUSE
        ... ))
        >>> graph.get_related_persons("person-001", RelationshipType.SPOUSE)
        ['person-002']
    """

    relationships: list[Relationship] = Field(default_factory=list)

    def add_relationship(
        self,
        relationship: Relationship,
        create_inverse: bool = False,
    ) -> None:
        """Add a relationship to the graph.

        Args:
            relationship: Relationship to add
            create_inverse: Whether to also create the inverse relationship
        """
        self.relationships.append(relationship)
        if create_inverse:
            self.relationships.append(relationship.create_inverse())

    def get_relationships_for_person(
        self,
        person_id: str,
        active_only: bool = True,
    ) -> list[Relationship]:
        """Get all relationships for a person.

        Args:
            person_id: ID of the person
            active_only: Only return active relationships

        Returns:
            List of relationships where person is the source
        """
        results = []
        for rel in self.relationships:
            if rel.source_person_id == person_id:
                if not active_only or rel.is_current:
                    results.append(rel)
        return results

    def get_related_persons(
        self,
        person_id: str,
        relationship_type: RelationshipType | None = None,
        active_only: bool = True,
    ) -> list[str]:
        """Get IDs of persons related to a given person.

        Args:
            person_id: ID of the person
            relationship_type: Filter by type (optional)
            active_only: Only include active relationships

        Returns:
            List of related person IDs
        """
        related = []
        for rel in self.get_relationships_for_person(person_id, active_only):
            if relationship_type is None or rel.relationship_type == relationship_type:
                related.append(rel.target_person_id)
        return related

    def has_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipType | None = None,
    ) -> bool:
        """Check if a relationship exists between two persons.

        Args:
            source_id: ID of the source person
            target_id: ID of the target person
            relationship_type: Type of relationship to check (optional)

        Returns:
            True if relationship exists
        """
        for rel in self.relationships:
            if rel.source_person_id == source_id and rel.target_person_id == target_id:
                if relationship_type is None or rel.relationship_type == relationship_type:
                    return True
        return False

    def remove_relationship(self, source_id: str, target_id: str) -> bool:
        """Remove a relationship between two persons.

        Args:
            source_id: ID of the source person
            target_id: ID of the target person

        Returns:
            True if a relationship was removed
        """
        for i, rel in enumerate(self.relationships):
            if rel.source_person_id == source_id and rel.target_person_id == target_id:
                del self.relationships[i]
                return True
        return False
