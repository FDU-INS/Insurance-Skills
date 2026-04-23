"""Validation framework for synthetic data.

Provides base classes and utilities for validating
generated data across all HealthSim products.

Example:
    >>> from healthsim.validation import ValidationResult, ValidationSeverity
    >>>
    >>> result = ValidationResult()
    >>> result.add_issue(
    ...     code="DATE_001",
    ...     message="Date is in the future",
    ...     severity=ValidationSeverity.ERROR,
    ... )
    >>> result.valid
    False
"""

from healthsim.validation.framework import (
    BaseValidator,
    CompositeValidator,
    StructuralValidator,
    ValidationIssue,
    ValidationMessage,
    ValidationResult,
    ValidationSeverity,
    Validator,
)
from healthsim.validation.structural import ReferentialIntegrityValidator
from healthsim.validation.temporal import TemporalValidator

__all__ = [
    # Results
    "ValidationResult",
    "ValidationIssue",
    "ValidationMessage",
    "ValidationSeverity",
    # Validators
    "BaseValidator",
    "Validator",
    "CompositeValidator",
    "TemporalValidator",
    "StructuralValidator",
    "ReferentialIntegrityValidator",
]
