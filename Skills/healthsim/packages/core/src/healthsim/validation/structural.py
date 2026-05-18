"""Structural validation utilities.

Provides validators for data structure and referential integrity checks.
"""

from collections.abc import Callable
from typing import Any, Protocol, TypeVar

from healthsim.validation.framework import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
)


class HasId(Protocol):
    """Protocol for objects with an ID field."""

    id: str


T = TypeVar("T", bound=HasId)


class ReferentialIntegrityValidator(BaseValidator):
    """Validator for referential integrity.

    Checks that references between objects are valid and consistent.

    Example:
        >>> validator = ReferentialIntegrityValidator()
        >>> result = validator.validate_reference(
        ...     source_id="123",
        ...     target_id="456",
        ...     source_field="order.person_id",
        ...     target_field="person.id",
        ... )
    """

    def validate(self, *args: Any, **kwargs: Any) -> ValidationResult:
        """Generic validate method - use specific methods instead."""
        return ValidationResult()

    def validate_reference(
        self,
        source_id: str | None,
        target_id: str | None,
        source_field: str,
        target_field: str,
    ) -> ValidationResult:
        """Validate that a reference matches its target.

        Args:
            source_id: The ID in the referencing object
            target_id: The ID in the referenced object
            source_field: Field name of the reference
            target_field: Field name being referenced

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult()

        if source_id is None or target_id is None:
            return result  # Can't validate None references

        if source_id != target_id:
            result.add_issue(
                code="REF_001",
                message=f"{source_field} ({source_id}) does not match {target_field} ({target_id})",
                severity=ValidationSeverity.ERROR,
                field_path=source_field,
                context={source_field: source_id, target_field: target_id},
            )

        return result

    def validate_required_reference(
        self,
        reference_id: str | None,
        field_name: str,
    ) -> ValidationResult:
        """Validate that a required reference is present.

        Args:
            reference_id: The reference ID to check
            field_name: Name of the reference field

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult()

        if reference_id is None or reference_id == "":
            result.add_issue(
                code="REF_002",
                message=f"{field_name} is required but not provided",
                severity=ValidationSeverity.ERROR,
                field_path=field_name,
            )

        return result

    def validate_unique_ids(
        self,
        items: list[T],
        id_field: str = "id",
        get_id: Callable[[T], str] | None = None,
    ) -> ValidationResult:
        """Validate that all items have unique IDs.

        Args:
            items: List of items to check
            id_field: Name of the ID field
            get_id: Optional function to extract ID from item

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult()
        seen_ids: dict[str, int] = {}

        for idx, item in enumerate(items):
            if get_id:
                item_id = get_id(item)
            else:
                item_id = getattr(item, id_field, None)

            if item_id is None:
                result.add_issue(
                    code="REF_003",
                    message=f"Item at index {idx} has no {id_field}",
                    severity=ValidationSeverity.ERROR,
                    field_path=f"[{idx}].{id_field}",
                )
                continue

            if item_id in seen_ids:
                result.add_issue(
                    code="REF_004",
                    message=f"Duplicate {id_field}: {item_id} (first at index {seen_ids[item_id]})",
                    severity=ValidationSeverity.ERROR,
                    field_path=f"[{idx}].{id_field}",
                    context={"duplicate_id": item_id, "first_index": seen_ids[item_id]},
                )
            else:
                seen_ids[item_id] = idx

        return result

    def validate_foreign_key(
        self,
        reference_id: str | None,
        valid_ids: set[str],
        field_name: str,
        allow_none: bool = True,
    ) -> ValidationResult:
        """Validate that a foreign key reference exists in the target set.

        Args:
            reference_id: The ID being referenced
            valid_ids: Set of valid target IDs
            field_name: Name of the foreign key field
            allow_none: Whether None references are allowed

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult()

        if reference_id is None:
            if not allow_none:
                result.add_issue(
                    code="REF_005",
                    message=f"{field_name} cannot be null",
                    severity=ValidationSeverity.ERROR,
                    field_path=field_name,
                )
            return result

        if reference_id not in valid_ids:
            result.add_issue(
                code="REF_006",
                message=f"{field_name} references non-existent ID: {reference_id}",
                severity=ValidationSeverity.ERROR,
                field_path=field_name,
                context={"invalid_id": reference_id},
            )

        return result
