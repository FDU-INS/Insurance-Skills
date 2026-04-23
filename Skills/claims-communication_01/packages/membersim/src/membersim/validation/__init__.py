"""Validation module for MemberSim.

Re-exports healthsim-core validation infrastructure and provides
member-specific validators.
"""

from healthsim.validation import (
    BaseValidator,
    CompositeValidator,
    StructuralValidator,
    ValidationIssue,
    ValidationMessage,
    ValidationResult,
    ValidationSeverity,
    Validator,
)

from membersim.validation.claims_validator import ClaimsValidator, MemberValidator

__all__ = [
    # Re-exported from healthsim-core
    "ValidationResult",
    "ValidationIssue",
    "ValidationMessage",
    "ValidationSeverity",
    "BaseValidator",
    "Validator",
    "CompositeValidator",
    "StructuralValidator",
    # Member-specific validators
    "MemberValidator",
    "ClaimsValidator",
]
