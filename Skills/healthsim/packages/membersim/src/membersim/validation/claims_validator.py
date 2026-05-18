"""Claims and member validation using healthsim-core validation framework."""

from __future__ import annotations

from datetime import date
from typing import Any

from healthsim.validation import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
)


class MemberValidator(BaseValidator):
    """Validator for Member data.

    Validates member demographics, identifiers, and coverage dates.

    Example:
        >>> validator = MemberValidator()
        >>> result = validator.validate(member)
        >>> if not result.valid:
        ...     for issue in result.issues:
        ...         print(f"{issue.severity}: {issue.message}")
    """

    def validate(self, data: Any) -> ValidationResult:
        """Validate member data.

        Args:
            data: Member instance or dict with member data

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult()

        # Handle both dict and object access
        if isinstance(data, dict):
            member_id = data.get("member_id")
            birth_date = data.get("birth_date")
            coverage_start = data.get("coverage_start")
            coverage_end = data.get("coverage_end")
            group_id = data.get("group_id")
        else:
            member_id = getattr(data, "member_id", None)
            birth_date = getattr(data, "birth_date", None)
            coverage_start = getattr(data, "coverage_start", None)
            coverage_end = getattr(data, "coverage_end", None)
            group_id = getattr(data, "group_id", None)

        # Required fields
        if not member_id:
            result.add_issue(
                code="MEM_001",
                message="Member ID is required",
                severity=ValidationSeverity.ERROR,
            )

        if not group_id:
            result.add_issue(
                code="MEM_002",
                message="Group ID is required",
                severity=ValidationSeverity.ERROR,
            )

        # Birth date validation
        if birth_date:
            if isinstance(birth_date, str):
                try:
                    birth_date = date.fromisoformat(birth_date)
                except ValueError:
                    result.add_issue(
                        code="MEM_003",
                        message=f"Invalid birth date format: {birth_date}",
                        severity=ValidationSeverity.ERROR,
                    )
                    birth_date = None

            if birth_date and birth_date > date.today():
                result.add_issue(
                    code="MEM_004",
                    message="Birth date cannot be in the future",
                    severity=ValidationSeverity.ERROR,
                )

        # Coverage date validation
        if coverage_start and coverage_end:
            if isinstance(coverage_start, str):
                coverage_start = date.fromisoformat(coverage_start)
            if isinstance(coverage_end, str):
                coverage_end = date.fromisoformat(coverage_end)

            if coverage_end < coverage_start:
                result.add_issue(
                    code="MEM_005",
                    message="Coverage end date cannot be before start date",
                    severity=ValidationSeverity.ERROR,
                )

        return result


class ClaimsValidator(BaseValidator):
    """Validator for Claims data.

    Validates claim structure, dates, amounts, and required fields.

    Example:
        >>> validator = ClaimsValidator()
        >>> result = validator.validate(claim)
        >>> if not result.valid:
        ...     for issue in result.issues:
        ...         print(f"{issue.severity}: {issue.message}")
    """

    def validate(self, data: Any) -> ValidationResult:
        """Validate claim data.

        Args:
            data: Claim instance or dict with claim data

        Returns:
            ValidationResult with any issues found
        """
        result = ValidationResult()

        # Handle both dict and object access
        if isinstance(data, dict):
            claim_id = data.get("claim_id")
            member_id = data.get("member_id")
            service_date = data.get("service_date")
            total_billed = data.get("total_billed")
            total_paid = data.get("total_paid")
            lines = data.get("lines", [])
        else:
            claim_id = getattr(data, "claim_id", None)
            member_id = getattr(data, "member_id", None)
            service_date = getattr(data, "service_date", None)
            total_billed = getattr(data, "total_billed", None)
            total_paid = getattr(data, "total_paid", None)
            lines = getattr(data, "lines", [])

        # Required fields
        if not claim_id:
            result.add_issue(
                code="CLM_001",
                message="Claim ID is required",
                severity=ValidationSeverity.ERROR,
            )

        if not member_id:
            result.add_issue(
                code="CLM_002",
                message="Member ID is required for claim",
                severity=ValidationSeverity.ERROR,
            )

        # Service date validation
        if service_date:
            if isinstance(service_date, str):
                try:
                    service_date = date.fromisoformat(service_date)
                except ValueError:
                    result.add_issue(
                        code="CLM_003",
                        message=f"Invalid service date format: {service_date}",
                        severity=ValidationSeverity.ERROR,
                    )
                    service_date = None

            if service_date and service_date > date.today():
                result.add_issue(
                    code="CLM_004",
                    message="Service date cannot be in the future",
                    severity=ValidationSeverity.WARNING,
                )

        # Amount validation
        if total_billed is not None and total_billed < 0:
            result.add_issue(
                code="CLM_005",
                message="Total billed amount cannot be negative",
                severity=ValidationSeverity.ERROR,
            )

        if total_paid is not None and total_paid < 0:
            result.add_issue(
                code="CLM_006",
                message="Total paid amount cannot be negative",
                severity=ValidationSeverity.ERROR,
            )

        if total_billed is not None and total_paid is not None and total_paid > total_billed:
            result.add_issue(
                code="CLM_007",
                message="Total paid cannot exceed total billed",
                severity=ValidationSeverity.WARNING,
            )

        # Claim lines validation
        if not lines:
            result.add_issue(
                code="CLM_008",
                message="Claim has no line items",
                severity=ValidationSeverity.WARNING,
            )

        return result
