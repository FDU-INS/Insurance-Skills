"""Tests for journey validation framework."""

import pytest
from datetime import date, datetime

from healthsim.generation.journey_validation import (
    ValidationSeverity,
    ValidationCategory,
    ValidationIssue,
    ValidationResult,
    JourneySpecValidator,
    TimelineValidator,
    CrossEventValidator,
    JourneyValidator,
    validate_journey_spec,
    validate_timeline,
    validate_events,
    create_journey_validator,
)


class TestValidationIssue:
    """Tests for ValidationIssue."""

    def test_basic_creation(self):
        """Test creating a validation issue."""
        issue = ValidationIssue(
            code="TEST_001",
            message="Test message",
            severity=ValidationSeverity.ERROR,
            category=ValidationCategory.SCHEMA,
        )
        
        assert issue.code == "TEST_001"
        assert issue.message == "Test message"
        assert issue.severity == ValidationSeverity.ERROR
        assert issue.category == ValidationCategory.SCHEMA

    def test_with_path_and_context(self):
        """Test issue with path and context."""
        issue = ValidationIssue(
            code="TEST_002",
            message="Field error",
            severity=ValidationSeverity.WARNING,
            category=ValidationCategory.TEMPORAL,
            path="$.events[0].date",
            context={"expected": "2025-01-01", "actual": "2024-01-01"},
        )
        
        assert issue.path == "$.events[0].date"
        assert issue.context["expected"] == "2025-01-01"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        issue = ValidationIssue(
            code="TEST_003",
            message="Test",
            severity=ValidationSeverity.INFO,
            category=ValidationCategory.BUSINESS,
        )
        
        d = issue.to_dict()
        
        assert d["code"] == "TEST_003"
        assert d["severity"] == "info"
        assert d["category"] == "business"


class TestValidationResult:
    """Tests for ValidationResult."""

    def test_initial_state(self):
        """Test initial state is passed."""
        result = ValidationResult(passed=True)
        
        assert result.passed is True
        assert len(result.issues) == 0

    def test_add_error(self):
        """Test adding an error."""
        result = ValidationResult(passed=True)
        
        result.add_error(
            code="ERR_001",
            message="Error occurred",
            category=ValidationCategory.SCHEMA,
        )
        
        assert result.passed is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "ERR_001"

    def test_add_warning(self):
        """Test adding a warning doesn't fail validation."""
        result = ValidationResult(passed=True)
        
        result.add_warning(
            code="WARN_001",
            message="Warning",
            category=ValidationCategory.TEMPORAL,
        )
        
        assert result.passed is True  # Warnings don't fail
        assert len(result.warnings) == 1

    def test_add_info(self):
        """Test adding info."""
        result = ValidationResult(passed=True)
        
        result.add_info(
            code="INFO_001",
            message="Info",
            category=ValidationCategory.COMPLETENESS,
        )
        
        assert result.passed is True
        assert len(result.info) == 1

    def test_merge_results(self):
        """Test merging two results."""
        result1 = ValidationResult(passed=True)
        result1.add_warning("W1", "Warning 1", ValidationCategory.SCHEMA)
        
        result2 = ValidationResult(passed=True)
        result2.add_error("E1", "Error 1", ValidationCategory.SCHEMA)
        
        result1.merge(result2)
        
        assert result1.passed is False
        assert len(result1.issues) == 2

    def test_formatted_string(self):
        """Test formatted output."""
        result = ValidationResult(passed=True)
        result.add_error("E1", "Error message", ValidationCategory.SCHEMA)
        result.add_warning("W1", "Warning message", ValidationCategory.TEMPORAL)
        
        formatted = result.to_formatted_string()
        
        assert "JOURNEY VALIDATION REPORT" in formatted
        assert "FAILED" in formatted
        assert "ERRORS" in formatted
        assert "WARNINGS" in formatted


class TestJourneySpecValidator:
    """Tests for JourneySpecValidator."""

    def test_valid_spec(self):
        """Test validating a valid specification."""
        spec = {
            "name": "test-journey",
            "events": [
                {"event_type": "encounter", "name": "visit1"},
                {"event_type": "lab_order", "name": "labs"},
            ],
        }
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert result.passed is True

    def test_missing_events(self):
        """Test spec with no events."""
        spec = {"name": "empty-journey"}
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert result.passed is False
        assert any(i.code == "SPEC_NO_EVENTS" for i in result.errors)

    def test_empty_events(self):
        """Test spec with empty events list."""
        spec = {"name": "empty-journey", "events": []}
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert result.passed is False

    def test_missing_event_type(self):
        """Test event missing event_type."""
        spec = {
            "name": "test",
            "events": [{"name": "some_event"}],
        }
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert result.passed is False
        assert any(i.code == "EVENT_NO_TYPE" for i in result.errors)

    def test_duplicate_event_ids(self):
        """Test duplicate event IDs."""
        spec = {
            "name": "test",
            "events": [
                {"event_type": "encounter", "id": "evt1"},
                {"event_type": "lab_order", "id": "evt1"},  # Duplicate
            ],
        }
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert result.passed is False
        assert any(i.code == "EVENT_DUPLICATE_ID" for i in result.errors)

    def test_invalid_delay(self):
        """Test invalid delay specification."""
        spec = {
            "name": "test",
            "events": [
                {
                    "event_type": "encounter",
                    "delay": {"min_days": 10, "max_days": 5},  # Invalid
                },
            ],
        }
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert result.passed is False
        assert any(i.code == "DELAY_MAX_LESS_THAN_MIN" for i in result.errors)

    def test_negative_delay(self):
        """Test negative delay."""
        spec = {
            "name": "test",
            "events": [
                {
                    "event_type": "encounter",
                    "delay": {"min_days": -5},
                },
            ],
        }
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert result.passed is False
        assert any(i.code == "DELAY_NEGATIVE_MIN" for i in result.errors)

    def test_invalid_duration(self):
        """Test invalid duration specification."""
        spec = {
            "name": "test",
            "events": [{"event_type": "encounter"}],
            "duration": {"min_days": 30, "max_days": 10},
        }
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert result.passed is False
        assert any(i.code == "DURATION_MAX_LESS_THAN_MIN" for i in result.errors)

    def test_missing_identifier_warning(self):
        """Test warning when no name or id."""
        spec = {
            "events": [{"event_type": "encounter"}],
        }
        
        validator = JourneySpecValidator()
        result = validator.validate(spec)
        
        assert len(result.warnings) > 0
        assert any(i.code == "SPEC_NO_IDENTIFIER" for i in result.warnings)

    def test_custom_rule(self):
        """Test adding custom validation rule."""
        def require_description(spec, result):
            if "description" not in spec:
                result.add_warning(
                    "CUSTOM_NO_DESC",
                    "Missing description",
                    ValidationCategory.COMPLETENESS,
                )
        
        validator = JourneySpecValidator()
        validator.add_rule(require_description)
        
        result = validator.validate({
            "name": "test",
            "events": [{"event_type": "encounter"}],
        })
        
        assert any(i.code == "CUSTOM_NO_DESC" for i in result.warnings)


class TestTimelineValidator:
    """Tests for TimelineValidator."""

    def test_valid_timeline(self):
        """Test validating a valid timeline."""
        timeline = {
            "events": [
                {"event_type": "encounter", "date": "2025-01-01"},
                {"event_type": "lab_order", "date": "2025-01-02"},
            ]
        }
        
        validator = TimelineValidator()
        result = validator.validate(timeline)
        
        assert result.passed is True

    def test_non_chronological_warning(self):
        """Test warning for non-chronological events."""
        timeline = {
            "events": [
                {"event_type": "encounter", "date": "2025-01-10"},
                {"event_type": "lab_order", "date": "2025-01-05"},  # Before
            ]
        }
        
        validator = TimelineValidator()
        result = validator.validate(timeline)
        
        assert any(i.code == "TIMELINE_NOT_CHRONOLOGICAL" for i in result.warnings)

    def test_missing_date_warning(self):
        """Test warning for missing date."""
        timeline = {
            "events": [
                {"event_type": "encounter"},  # No date
            ]
        }
        
        validator = TimelineValidator()
        result = validator.validate(timeline)
        
        assert any(i.code == "EVENT_MISSING_DATE" for i in result.warnings)

    def test_date_too_old(self):
        """Test error for dates before 1900."""
        timeline = {
            "events": [
                {"event_type": "encounter", "date": "1850-01-01"},
            ]
        }
        
        validator = TimelineValidator()
        result = validator.validate(timeline)
        
        assert result.passed is False
        assert any(i.code == "EVENT_DATE_TOO_OLD" for i in result.errors)

    def test_future_date_info(self):
        """Test info for future dates."""
        future_date = date.today().replace(year=date.today().year + 1)
        timeline = {
            "events": [
                {"event_type": "encounter", "date": future_date.isoformat()},
            ]
        }
        
        validator = TimelineValidator()
        result = validator.validate(timeline)
        
        assert any(i.code == "EVENT_FUTURE_DATE" for i in result.info)

    def test_datetime_handling(self):
        """Test handling datetime objects."""
        timeline = {
            "events": [
                {"event_type": "encounter", "date": datetime(2025, 1, 1, 10, 30)},
            ]
        }
        
        validator = TimelineValidator()
        result = validator.validate(timeline)
        
        # Should handle datetime without error
        assert result.passed is True


class TestCrossEventValidator:
    """Tests for CrossEventValidator."""

    def test_valid_events(self):
        """Test validating valid related events."""
        events = [
            {
                "event_type": "encounter",
                "patient_id": "PAT-001",
                "date": "2025-01-10",
            },
            {
                "event_type": "claim",
                "patient_id": "PAT-001",
                "date": "2025-01-12",
            },
        ]
        
        validator = CrossEventValidator()
        result = validator.validate(events)
        
        assert result.passed is True

    def test_claim_before_encounter(self):
        """Test error when claim is before encounter."""
        events = [
            {
                "event_type": "encounter",
                "patient_id": "PAT-001",
                "service_date": "2025-01-15",
            },
            {
                "event_type": "claim",
                "patient_id": "PAT-001",
                "service_date": "2025-01-10",  # Before encounter
            },
        ]
        
        validator = CrossEventValidator()
        result = validator.validate(events)
        
        assert result.passed is False
        assert any(i.code == "CLAIM_BEFORE_ENCOUNTER" for i in result.errors)

    def test_discharge_before_admission(self):
        """Test error when discharge is before admission."""
        events = [
            {
                "event_type": "admission",
                "patient_id": "PAT-001",
                "admit_date": "2025-01-15",
            },
            {
                "event_type": "discharge",
                "patient_id": "PAT-001",
                "discharge_date": "2025-01-10",  # Before admission
            },
        ]
        
        validator = CrossEventValidator()
        result = validator.validate(events)
        
        assert result.passed is False
        assert any(i.code == "DISCHARGE_BEFORE_ADMISSION" for i in result.errors)

    def test_fill_before_prescription(self):
        """Test error when fill is before prescription."""
        events = [
            {
                "event_type": "prescription",
                "patient_id": "PAT-001",
                "written_date": "2025-01-15",
            },
            {
                "event_type": "fill",
                "patient_id": "PAT-001",
                "fill_date": "2025-01-10",  # Before prescription
            },
        ]
        
        validator = CrossEventValidator()
        result = validator.validate(events)
        
        assert result.passed is False
        assert any(i.code == "FILL_BEFORE_PRESCRIPTION" for i in result.errors)

    def test_result_before_order(self):
        """Test error when result is before order."""
        events = [
            {
                "event_type": "lab_order",
                "patient_id": "PAT-001",
                "order_date": "2025-01-15",
            },
            {
                "event_type": "lab_result",
                "patient_id": "PAT-001",
                "result_date": "2025-01-10",  # Before order
            },
        ]
        
        validator = CrossEventValidator()
        result = validator.validate(events)
        
        assert result.passed is False
        assert any(i.code == "RESULT_BEFORE_ORDER" for i in result.errors)

    def test_unrelated_events_ignored(self):
        """Test that unrelated events are not cross-validated."""
        events = [
            {
                "event_type": "encounter",
                "patient_id": "PAT-001",
                "date": "2025-01-15",
            },
            {
                "event_type": "claim",
                "patient_id": "PAT-002",  # Different patient
                "date": "2025-01-10",
            },
        ]
        
        validator = CrossEventValidator()
        result = validator.validate(events)
        
        # Should pass because events are for different patients
        assert result.passed is True

    def test_custom_rule(self):
        """Test adding custom cross-event rule."""
        def check_same_provider(source, target, result):
            if source.get("provider_id") != target.get("provider_id"):
                result.add_warning(
                    "PROVIDER_MISMATCH",
                    "Provider mismatch between encounter and claim",
                    ValidationCategory.REFERENTIAL,
                )
        
        validator = CrossEventValidator()
        validator.add_rule("encounter", "claim", check_same_provider)
        
        events = [
            {
                "event_type": "encounter",
                "patient_id": "PAT-001",
                "provider_id": "NPI-001",
                "date": "2025-01-10",
            },
            {
                "event_type": "claim",
                "patient_id": "PAT-001",
                "provider_id": "NPI-002",  # Different provider
                "date": "2025-01-12",
            },
        ]
        
        result = validator.validate(events)
        
        assert any(i.code == "PROVIDER_MISMATCH" for i in result.warnings)


class TestJourneyValidator:
    """Tests for combined JourneyValidator."""

    def test_validate_specification(self):
        """Test validating specification through combined validator."""
        validator = JourneyValidator()
        
        spec = {
            "name": "test",
            "events": [{"event_type": "encounter"}],
        }
        
        result = validator.validate_specification(spec)
        
        assert result.passed is True

    def test_validate_timeline(self):
        """Test validating timeline through combined validator."""
        validator = JourneyValidator()
        
        timeline = {
            "events": [
                {"event_type": "encounter", "date": "2025-01-01"},
            ]
        }
        
        result = validator.validate_timeline(timeline)
        
        assert result.passed is True

    def test_validate_all(self):
        """Test running all validations."""
        validator = JourneyValidator()
        
        spec = {
            "name": "test",
            "events": [{"event_type": "encounter"}],
        }
        
        timeline = {
            "events": [
                {"event_type": "encounter", "date": "2025-01-01"},
            ]
        }
        
        events = [
            {"event_type": "encounter", "patient_id": "P1", "date": "2025-01-01"},
        ]
        
        result = validator.validate_all(spec, timeline, events)
        
        assert result.passed is True


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_validate_journey_spec(self):
        """Test validate_journey_spec function."""
        spec = {
            "name": "test",
            "events": [{"event_type": "encounter"}],
        }
        
        result = validate_journey_spec(spec)
        
        assert result.passed is True

    def test_validate_timeline_function(self):
        """Test validate_timeline function."""
        timeline = {
            "events": [
                {"event_type": "encounter", "date": "2025-01-01"},
            ]
        }
        
        result = validate_timeline(timeline)
        
        assert result.passed is True

    def test_validate_events_function(self):
        """Test validate_events function."""
        events = [
            {"event_type": "encounter", "patient_id": "P1", "date": "2025-01-01"},
        ]
        
        result = validate_events(events)
        
        assert result.passed is True

    def test_create_journey_validator(self):
        """Test factory function."""
        validator = create_journey_validator()
        
        assert isinstance(validator, JourneyValidator)
        assert validator.spec_validator is not None
        assert validator.timeline_validator is not None
        assert validator.cross_event_validator is not None
