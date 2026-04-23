"""Validation framework for pharmacy data."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ValidationSeverity(str, Enum):
    """Severity level of validation issues."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationIssue(BaseModel):
    """A single validation issue."""

    field: str
    message: str
    severity: ValidationSeverity
    code: str | None = None
    actual_value: Any | None = None
    expected_value: Any | None = None


class ValidationResult(BaseModel):
    """Result of validation with issues."""

    valid: bool = True
    issues: list[ValidationIssue] = Field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        """Get all error-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Get all warning-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]

    def add_error(self, field: str, message: str, **kwargs: Any) -> None:
        """Add an error issue."""
        self.issues.append(
            ValidationIssue(
                field=field,
                message=message,
                severity=ValidationSeverity.ERROR,
                **kwargs,
            )
        )
        self.valid = False

    def add_warning(self, field: str, message: str, **kwargs: Any) -> None:
        """Add a warning issue."""
        self.issues.append(
            ValidationIssue(
                field=field,
                message=message,
                severity=ValidationSeverity.WARNING,
                **kwargs,
            )
        )

    def add_info(self, field: str, message: str, **kwargs: Any) -> None:
        """Add an info issue."""
        self.issues.append(
            ValidationIssue(
                field=field,
                message=message,
                severity=ValidationSeverity.INFO,
                **kwargs,
            )
        )


class Validator:
    """Base validator class."""

    def validate(self, data: Any) -> ValidationResult:
        """Validate data and return result."""
        raise NotImplementedError
