"""Base validation framework for patient data validation.

This module re-exports core validation classes from healthsim-core
and provides the foundation for PatientSim-specific validation.
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

__all__ = [
    # Core validation types
    "ValidationSeverity",
    "ValidationIssue",
    "ValidationMessage",  # Alias for ValidationIssue
    "ValidationResult",
    # Validators
    "BaseValidator",
    "Validator",  # Alias for BaseValidator
    "CompositeValidator",
    "StructuralValidator",
]
