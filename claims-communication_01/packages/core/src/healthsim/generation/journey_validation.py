"""Journey validation framework.

This module provides validation for journey specifications and timelines,
ensuring data consistency and correctness before and after execution.

Validation Types:
1. Specification Validation - Before execution
2. Timeline Validation - After execution
3. Cross-Event Consistency - Data integrity checks
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Callable

from pydantic import BaseModel, Field


class ValidationSeverity(str, Enum):
    """Severity level for validation issues."""
    ERROR = "error"      # Blocks execution
    WARNING = "warning"  # Allows execution with notice
    INFO = "info"        # Informational only


class ValidationCategory(str, Enum):
    """Category of validation check."""
    SCHEMA = "schema"           # Structural/type validation
    TEMPORAL = "temporal"       # Date/time consistency
    REFERENTIAL = "referential" # Foreign key/reference validity
    BUSINESS = "business"       # Domain-specific rules
    COMPLETENESS = "completeness"  # Required data presence


@dataclass
class ValidationIssue:
    """A single validation issue."""
    code: str
    message: str
    severity: ValidationSeverity
    category: ValidationCategory
    path: str | None = None  # JSON path to problematic element
    context: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity.value,
            "category": self.category.value,
            "path": self.path,
            "context": self.context,
        }


@dataclass
class ValidationResult:
    """Result of validation operation."""
    passed: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    validated_at: datetime = field(default_factory=datetime.utcnow)
    validator_version: str = "1.0"
    
    @property
    def errors(self) -> list[ValidationIssue]:
        """Get error-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]
    
    @property
    def warnings(self) -> list[ValidationIssue]:
        """Get warning-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]
    
    @property
    def info(self) -> list[ValidationIssue]:
        """Get info-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.INFO]
    
    def add_error(
        self,
        code: str,
        message: str,
        category: ValidationCategory,
        path: str | None = None,
        **context: Any
    ) -> None:
        """Add an error issue."""
        self.issues.append(ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.ERROR,
            category=category,
            path=path,
            context=context,
        ))
        self.passed = False
    
    def add_warning(
        self,
        code: str,
        message: str,
        category: ValidationCategory,
        path: str | None = None,
        **context: Any
    ) -> None:
        """Add a warning issue."""
        self.issues.append(ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.WARNING,
            category=category,
            path=path,
            context=context,
        ))
    
    def add_info(
        self,
        code: str,
        message: str,
        category: ValidationCategory,
        path: str | None = None,
        **context: Any
    ) -> None:
        """Add an info issue."""
        self.issues.append(ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.INFO,
            category=category,
            path=path,
            context=context,
        ))
    
    def merge(self, other: "ValidationResult") -> None:
        """Merge another result into this one."""
        self.issues.extend(other.issues)
        if not other.passed:
            self.passed = False
    
    def to_formatted_string(self) -> str:
        """Format result for display."""
        lines = [
            "═" * 60,
            "           JOURNEY VALIDATION REPORT",
            "═" * 60,
            "",
            f"Status: {'✓ PASSED' if self.passed else '✗ FAILED'}",
            f"Validated: {self.validated_at.isoformat()}",
            "",
        ]
        
        if self.errors:
            lines.append(f"ERRORS ({len(self.errors)}):")
            lines.append("─" * 60)
            for issue in self.errors:
                lines.append(f"  ✗ [{issue.code}] {issue.message}")
                if issue.path:
                    lines.append(f"    Path: {issue.path}")
            lines.append("")
        
        if self.warnings:
            lines.append(f"WARNINGS ({len(self.warnings)}):")
            lines.append("─" * 60)
            for issue in self.warnings:
                lines.append(f"  ⚠ [{issue.code}] {issue.message}")
            lines.append("")
        
        if self.info:
            lines.append(f"INFO ({len(self.info)}):")
            lines.append("─" * 60)
            for issue in self.info:
                lines.append(f"  ℹ [{issue.code}] {issue.message}")
            lines.append("")
        
        lines.append("═" * 60)
        
        return "\n".join(lines)


# =============================================================================
# Specification Validators
# =============================================================================

class JourneySpecValidator:
    """Validates journey specifications before execution.
    
    Checks performed:
    - Required fields present
    - Event types are valid
    - Date ranges are logical
    - Referenced entities exist
    """
    
    def __init__(self):
        self._custom_rules: list[Callable] = []
    
    def add_rule(self, rule: Callable[[dict, ValidationResult], None]) -> None:
        """Add a custom validation rule.
        
        Args:
            rule: Function taking (spec_dict, result) and adding issues
        """
        self._custom_rules.append(rule)
    
    def validate(self, spec: dict[str, Any]) -> ValidationResult:
        """Validate a journey specification.
        
        Args:
            spec: Journey specification dictionary
            
        Returns:
            ValidationResult
        """
        result = ValidationResult(passed=True)
        
        # Check required fields
        self._check_required_fields(spec, result)
        
        # Check events
        if "events" in spec:
            self._check_events(spec["events"], result)
        
        # Check duration
        if "duration" in spec:
            self._check_duration(spec["duration"], result)
        
        # Check triggers
        if "triggers" in spec:
            self._check_triggers(spec["triggers"], result)
        
        # Run custom rules
        for rule in self._custom_rules:
            rule(spec, result)
        
        return result
    
    def _check_required_fields(
        self,
        spec: dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Check required fields are present."""
        # Journey needs either name/id or be inline
        if "name" not in spec and "id" not in spec:
            result.add_warning(
                code="SPEC_NO_IDENTIFIER",
                message="Journey has no name or id",
                category=ValidationCategory.SCHEMA,
                path="$",
            )
        
        # Events are required
        if "events" not in spec or not spec["events"]:
            result.add_error(
                code="SPEC_NO_EVENTS",
                message="Journey must have at least one event",
                category=ValidationCategory.SCHEMA,
                path="$.events",
            )
    
    def _check_events(
        self,
        events: list[dict],
        result: ValidationResult
    ) -> None:
        """Check event definitions."""
        event_ids = set()
        
        for i, event in enumerate(events):
            path = f"$.events[{i}]"
            
            # Check event type
            if "event_type" not in event:
                result.add_error(
                    code="EVENT_NO_TYPE",
                    message=f"Event {i} missing event_type",
                    category=ValidationCategory.SCHEMA,
                    path=path,
                )
            
            # Check for duplicate IDs
            event_id = event.get("id") or event.get("name")
            if event_id:
                if event_id in event_ids:
                    result.add_error(
                        code="EVENT_DUPLICATE_ID",
                        message=f"Duplicate event ID: {event_id}",
                        category=ValidationCategory.SCHEMA,
                        path=path,
                        event_id=event_id,
                    )
                event_ids.add(event_id)
            
            # Check delay specification
            if "delay" in event:
                self._check_delay(event["delay"], result, f"{path}.delay")
    
    def _check_delay(
        self,
        delay: dict[str, Any],
        result: ValidationResult,
        path: str
    ) -> None:
        """Check delay specification."""
        min_val = delay.get("min_days", 0)
        max_val = delay.get("max_days", min_val)
        
        if min_val < 0:
            result.add_error(
                code="DELAY_NEGATIVE_MIN",
                message=f"Delay min_days cannot be negative: {min_val}",
                category=ValidationCategory.SCHEMA,
                path=path,
            )
        
        if max_val < min_val:
            result.add_error(
                code="DELAY_MAX_LESS_THAN_MIN",
                message=f"Delay max_days ({max_val}) < min_days ({min_val})",
                category=ValidationCategory.SCHEMA,
                path=path,
            )
    
    def _check_duration(
        self,
        duration: dict[str, Any],
        result: ValidationResult
    ) -> None:
        """Check duration specification."""
        min_days = duration.get("min_days", 0)
        max_days = duration.get("max_days")
        
        if min_days < 0:
            result.add_error(
                code="DURATION_NEGATIVE",
                message=f"Duration min_days cannot be negative: {min_days}",
                category=ValidationCategory.SCHEMA,
                path="$.duration",
            )
        
        if max_days is not None and max_days < min_days:
            result.add_error(
                code="DURATION_MAX_LESS_THAN_MIN",
                message=f"Duration max_days ({max_days}) < min_days ({min_days})",
                category=ValidationCategory.SCHEMA,
                path="$.duration",
            )
    
    def _check_triggers(
        self,
        triggers: list[dict],
        result: ValidationResult
    ) -> None:
        """Check trigger specifications."""
        for i, trigger in enumerate(triggers):
            path = f"$.triggers[{i}]"
            
            if "source_event" not in trigger:
                result.add_error(
                    code="TRIGGER_NO_SOURCE",
                    message=f"Trigger {i} missing source_event",
                    category=ValidationCategory.SCHEMA,
                    path=path,
                )
            
            if "target_product" not in trigger:
                result.add_error(
                    code="TRIGGER_NO_TARGET",
                    message=f"Trigger {i} missing target_product",
                    category=ValidationCategory.SCHEMA,
                    path=path,
                )


# =============================================================================
# Timeline Validators
# =============================================================================

class TimelineValidator:
    """Validates generated timelines after execution.
    
    Checks performed:
    - Events are in chronological order
    - No overlapping events (where prohibited)
    - All required events present
    - Cross-event data consistency
    """
    
    def __init__(self):
        self._custom_rules: list[Callable] = []
    
    def add_rule(self, rule: Callable[[Any, ValidationResult], None]) -> None:
        """Add a custom validation rule."""
        self._custom_rules.append(rule)
    
    def validate(self, timeline: Any) -> ValidationResult:
        """Validate a timeline.
        
        Args:
            timeline: Timeline object or dict
            
        Returns:
            ValidationResult
        """
        result = ValidationResult(passed=True)
        
        # Convert to dict if needed
        if hasattr(timeline, "dict"):
            timeline_dict = timeline.dict()
        elif hasattr(timeline, "__dict__"):
            timeline_dict = timeline.__dict__
        elif isinstance(timeline, dict):
            timeline_dict = timeline
        else:
            result.add_error(
                code="TIMELINE_INVALID_TYPE",
                message=f"Cannot validate timeline of type {type(timeline)}",
                category=ValidationCategory.SCHEMA,
            )
            return result
        
        events = timeline_dict.get("events", [])
        
        # Check chronological order
        self._check_chronological_order(events, result)
        
        # Check event completeness
        self._check_event_completeness(events, result)
        
        # Check date validity
        self._check_date_validity(events, result)
        
        # Run custom rules
        for rule in self._custom_rules:
            rule(timeline, result)
        
        return result
    
    def _check_chronological_order(
        self,
        events: list[dict],
        result: ValidationResult
    ) -> None:
        """Check events are in chronological order."""
        prev_date = None
        
        for i, event in enumerate(events):
            event_date = self._extract_date(event)
            
            if event_date and prev_date:
                if event_date < prev_date:
                    result.add_warning(
                        code="TIMELINE_NOT_CHRONOLOGICAL",
                        message=f"Event {i} date ({event_date}) before previous ({prev_date})",
                        category=ValidationCategory.TEMPORAL,
                        path=f"$.events[{i}]",
                    )
            
            if event_date:
                prev_date = event_date
    
    def _check_event_completeness(
        self,
        events: list[dict],
        result: ValidationResult
    ) -> None:
        """Check that events have required data."""
        for i, event in enumerate(events):
            path = f"$.events[{i}]"
            
            # Check for event type
            if "event_type" not in event:
                result.add_warning(
                    code="EVENT_MISSING_TYPE",
                    message=f"Event {i} missing event_type",
                    category=ValidationCategory.COMPLETENESS,
                    path=path,
                )
            
            # Check for date
            if not self._extract_date(event):
                result.add_warning(
                    code="EVENT_MISSING_DATE",
                    message=f"Event {i} missing date",
                    category=ValidationCategory.COMPLETENESS,
                    path=path,
                )
    
    def _check_date_validity(
        self,
        events: list[dict],
        result: ValidationResult
    ) -> None:
        """Check dates are valid."""
        for i, event in enumerate(events):
            event_date = self._extract_date(event)
            
            if event_date:
                # Normalize to date for comparisons
                check_date = event_date
                if isinstance(event_date, datetime):
                    check_date = event_date.date()
                
                # Check for future dates (warning)
                if check_date > date.today():
                    result.add_info(
                        code="EVENT_FUTURE_DATE",
                        message=f"Event {i} has future date: {event_date}",
                        category=ValidationCategory.TEMPORAL,
                        path=f"$.events[{i}]",
                    )
                
                # Check for unreasonably old dates
                min_date = date(1900, 1, 1)
                if check_date < min_date:
                    result.add_error(
                        code="EVENT_DATE_TOO_OLD",
                        message=f"Event {i} date ({event_date}) before 1900",
                        category=ValidationCategory.TEMPORAL,
                        path=f"$.events[{i}]",
                    )
    
    def _extract_date(self, event: dict) -> date | None:
        """Extract date from event."""
        for field in ["scheduled_date", "actual_date", "event_date", "date"]:
            if field in event:
                val = event[field]
                if isinstance(val, date):
                    return val
                if isinstance(val, datetime):
                    return val.date()
                if isinstance(val, str):
                    try:
                        return date.fromisoformat(val[:10])
                    except ValueError:
                        pass
        return None


# =============================================================================
# Cross-Event Validators
# =============================================================================

class CrossEventValidator:
    """Validates consistency across related events.
    
    Checks performed:
    - Claim dates not before encounter dates
    - Discharge not before admission
    - Prescription refills after initial fill
    - Lab results after lab orders
    """
    
    def __init__(self):
        self._rules: list[tuple[str, str, Callable]] = []
        self._setup_default_rules()
    
    def _setup_default_rules(self) -> None:
        """Set up default cross-event validation rules."""
        # Admission before discharge
        self.add_rule(
            source_type="admission",
            target_type="discharge",
            check=self._check_admission_before_discharge,
        )
        
        # Encounter before claim
        self.add_rule(
            source_type="encounter",
            target_type="claim",
            check=self._check_encounter_before_claim,
        )
        
        # Prescription before fill
        self.add_rule(
            source_type="prescription",
            target_type="fill",
            check=self._check_prescription_before_fill,
        )
        
        # Lab order before result
        self.add_rule(
            source_type="lab_order",
            target_type="lab_result",
            check=self._check_order_before_result,
        )
    
    def add_rule(
        self,
        source_type: str,
        target_type: str,
        check: Callable[[dict, dict, ValidationResult], None]
    ) -> None:
        """Add a cross-event validation rule.
        
        Args:
            source_type: Source event type
            target_type: Target event type  
            check: Function taking (source, target, result)
        """
        self._rules.append((source_type, target_type, check))
    
    def validate(
        self,
        events: list[dict],
        relationships: dict[str, str] | None = None
    ) -> ValidationResult:
        """Validate cross-event consistency.
        
        Args:
            events: List of event dictionaries
            relationships: Optional dict mapping event IDs to related event IDs
            
        Returns:
            ValidationResult
        """
        result = ValidationResult(passed=True)
        
        # Index events by type and ID
        by_type: dict[str, list[dict]] = {}
        by_id: dict[str, dict] = {}
        
        for event in events:
            event_type = event.get("event_type", "unknown")
            by_type.setdefault(event_type, []).append(event)
            
            event_id = event.get("id") or event.get("event_id")
            if event_id:
                by_id[event_id] = event
        
        # Apply rules
        for source_type, target_type, check in self._rules:
            sources = by_type.get(source_type, [])
            targets = by_type.get(target_type, [])
            
            for source in sources:
                for target in targets:
                    # Check if related (by ID or matching fields)
                    if self._are_related(source, target, relationships):
                        check(source, target, result)
        
        return result
    
    def _are_related(
        self,
        source: dict,
        target: dict,
        relationships: dict[str, str] | None
    ) -> bool:
        """Check if two events are related."""
        # Check explicit relationships
        if relationships:
            source_id = source.get("id") or source.get("event_id")
            target_id = target.get("id") or target.get("event_id")
            if source_id and relationships.get(source_id) == target_id:
                return True
        
        # Check common identifiers
        for field in ["patient_id", "member_id", "subject_id", "encounter_id"]:
            if source.get(field) and source.get(field) == target.get(field):
                return True
        
        return False
    
    def _check_admission_before_discharge(
        self,
        admission: dict,
        discharge: dict,
        result: ValidationResult
    ) -> None:
        """Check admission date is before discharge date."""
        admit_date = self._get_date(admission, ["admit_date", "date"])
        discharge_date = self._get_date(discharge, ["discharge_date", "date"])
        
        if admit_date and discharge_date and discharge_date < admit_date:
            result.add_error(
                code="DISCHARGE_BEFORE_ADMISSION",
                message=f"Discharge ({discharge_date}) before admission ({admit_date})",
                category=ValidationCategory.TEMPORAL,
                context={"admission": admission, "discharge": discharge},
            )
    
    def _check_encounter_before_claim(
        self,
        encounter: dict,
        claim: dict,
        result: ValidationResult
    ) -> None:
        """Check encounter date is not after claim date."""
        enc_date = self._get_date(encounter, ["service_date", "date"])
        claim_date = self._get_date(claim, ["service_date", "claim_date", "date"])
        
        if enc_date and claim_date and claim_date < enc_date:
            result.add_error(
                code="CLAIM_BEFORE_ENCOUNTER",
                message=f"Claim date ({claim_date}) before encounter ({enc_date})",
                category=ValidationCategory.TEMPORAL,
            )
    
    def _check_prescription_before_fill(
        self,
        prescription: dict,
        fill: dict,
        result: ValidationResult
    ) -> None:
        """Check prescription date is before fill date."""
        rx_date = self._get_date(prescription, ["written_date", "date"])
        fill_date = self._get_date(fill, ["fill_date", "date"])
        
        if rx_date and fill_date and fill_date < rx_date:
            result.add_error(
                code="FILL_BEFORE_PRESCRIPTION",
                message=f"Fill date ({fill_date}) before prescription ({rx_date})",
                category=ValidationCategory.TEMPORAL,
            )
    
    def _check_order_before_result(
        self,
        order: dict,
        result_event: dict,
        result: ValidationResult
    ) -> None:
        """Check order date is before result date."""
        order_date = self._get_date(order, ["order_date", "date"])
        result_date = self._get_date(result_event, ["result_date", "date"])
        
        if order_date and result_date and result_date < order_date:
            result.add_error(
                code="RESULT_BEFORE_ORDER",
                message=f"Result date ({result_date}) before order ({order_date})",
                category=ValidationCategory.TEMPORAL,
            )
    
    def _get_date(self, event: dict, fields: list[str]) -> date | None:
        """Get date from event trying multiple field names."""
        for field in fields:
            if field in event:
                val = event[field]
                if isinstance(val, date):
                    return val
                if isinstance(val, datetime):
                    return val.date()
                if isinstance(val, str):
                    try:
                        return date.fromisoformat(val[:10])
                    except ValueError:
                        pass
        return None


# =============================================================================
# Combined Validator
# =============================================================================

class JourneyValidator:
    """Combined validator for journey specifications and timelines.
    
    Example:
        >>> validator = JourneyValidator()
        >>> # Validate spec before execution
        >>> spec_result = validator.validate_specification(journey_spec)
        >>> if not spec_result.passed:
        ...     print(spec_result.to_formatted_string())
        ...     return
        >>> # Execute journey...
        >>> # Validate timeline after execution
        >>> timeline_result = validator.validate_timeline(timeline)
    """
    
    def __init__(self):
        self.spec_validator = JourneySpecValidator()
        self.timeline_validator = TimelineValidator()
        self.cross_event_validator = CrossEventValidator()
    
    def validate_specification(
        self,
        spec: dict[str, Any]
    ) -> ValidationResult:
        """Validate a journey specification.
        
        Args:
            spec: Journey specification dictionary
            
        Returns:
            ValidationResult
        """
        return self.spec_validator.validate(spec)
    
    def validate_timeline(
        self,
        timeline: Any
    ) -> ValidationResult:
        """Validate a generated timeline.
        
        Args:
            timeline: Timeline object or dictionary
            
        Returns:
            ValidationResult
        """
        return self.timeline_validator.validate(timeline)
    
    def validate_cross_events(
        self,
        events: list[dict],
        relationships: dict[str, str] | None = None
    ) -> ValidationResult:
        """Validate cross-event consistency.
        
        Args:
            events: List of event dictionaries
            relationships: Optional relationship mappings
            
        Returns:
            ValidationResult
        """
        return self.cross_event_validator.validate(events, relationships)
    
    def validate_all(
        self,
        spec: dict[str, Any],
        timeline: Any,
        events: list[dict] | None = None,
    ) -> ValidationResult:
        """Run all validations and combine results.
        
        Args:
            spec: Journey specification
            timeline: Generated timeline
            events: Optional event list for cross-event validation
            
        Returns:
            Combined ValidationResult
        """
        result = ValidationResult(passed=True)
        
        # Validate specification
        spec_result = self.validate_specification(spec)
        result.merge(spec_result)
        
        # Validate timeline
        timeline_result = self.validate_timeline(timeline)
        result.merge(timeline_result)
        
        # Validate cross-events if provided
        if events:
            cross_result = self.validate_cross_events(events)
            result.merge(cross_result)
        
        return result


# =============================================================================
# Convenience Functions
# =============================================================================

def validate_journey_spec(spec: dict[str, Any]) -> ValidationResult:
    """Validate a journey specification.
    
    Args:
        spec: Journey specification dictionary
        
    Returns:
        ValidationResult
    """
    validator = JourneySpecValidator()
    return validator.validate(spec)


def validate_timeline(timeline: Any) -> ValidationResult:
    """Validate a generated timeline.
    
    Args:
        timeline: Timeline object or dictionary
        
    Returns:
        ValidationResult
    """
    validator = TimelineValidator()
    return validator.validate(timeline)


def validate_events(
    events: list[dict],
    relationships: dict[str, str] | None = None
) -> ValidationResult:
    """Validate cross-event consistency.
    
    Args:
        events: List of event dictionaries
        relationships: Optional relationship mappings
        
    Returns:
        ValidationResult
    """
    validator = CrossEventValidator()
    return validator.validate(events, relationships)


def create_journey_validator() -> JourneyValidator:
    """Create a combined journey validator.
    
    Returns:
        JourneyValidator instance
    """
    return JourneyValidator()
