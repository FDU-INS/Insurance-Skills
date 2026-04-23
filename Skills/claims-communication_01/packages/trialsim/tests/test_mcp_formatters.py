"""Tests for TrialSim MCP formatters."""

import pytest
from datetime import date
from unittest.mock import MagicMock

from trialsim.mcp.formatters import (
    format_subject_summary,
    format_cohort_summary,
    format_visit_schedule,
    format_adverse_events,
    format_exposures,
    format_skill_list,
    format_skill_details,
    format_success,
    format_error,
)
from trialsim.core.models import (
    Subject,
    SubjectStatus,
    ArmType,
    Visit,
    VisitType,
    AdverseEvent,
    AESeverity,
    AECausality,
    AEOutcome,
    Exposure,
)


class TestFormatSubjectSummary:
    """Tests for format_subject_summary."""

    def test_basic_subject(self):
        """Test formatting a basic subject."""
        subject = Subject(
            subject_id="SUBJ-001",
            protocol_id="ABC-123",
            site_id="SITE-001",
            age=55,
            sex="M",
            status=SubjectStatus.ENROLLED,
        )
        result = format_subject_summary(subject)
        
        assert "SUBJ-001" in result
        assert "ABC-123" in result
        assert "55 years" in result
        assert "enrolled" in result.lower()

    def test_subject_with_arm(self):
        """Test formatting subject with treatment arm."""
        subject = Subject(
            subject_id="SUBJ-002",
            protocol_id="ABC-123",
            site_id="SITE-001",
            age=62,
            sex="F",
            status=SubjectStatus.ON_TREATMENT,
            arm=ArmType.TREATMENT,
        )
        result = format_subject_summary(subject)
        
        assert "Treatment Arm" in result
        assert "treatment" in result.lower()

    def test_subject_with_randomization_date(self):
        """Test formatting subject with randomization date."""
        subject = Subject(
            subject_id="SUBJ-003",
            protocol_id="ABC-123",
            site_id="SITE-001",
            age=48,
            sex="M",
            status=SubjectStatus.RANDOMIZED,
            randomization_date=date(2025, 6, 15),
        )
        result = format_subject_summary(subject)
        
        # Check randomization date is displayed
        assert "2025-06-15" in result
        assert "Randomized:" in result


class TestFormatCohortSummary:
    """Tests for format_cohort_summary."""

    def test_empty_cohort(self):
        """Test formatting empty cohort."""
        result = format_cohort_summary([])
        assert "No subjects generated" in result

    def test_cohort_with_subjects(self):
        """Test formatting cohort with subjects."""
        subjects = [
            Subject(
                subject_id=f"SUBJ-{i:03d}",
                protocol_id="ABC-123",
                site_id="SITE-001",
                age=50 + i,
                sex="M" if i % 2 == 0 else "F",
                status=SubjectStatus.ENROLLED,
            )
            for i in range(5)
        ]
        result = format_cohort_summary(subjects)
        
        assert "Generated 5 Subjects" in result
        assert "Average age" in result
        assert "Demographics" in result
        assert "Sample Subjects" in result

    def test_cohort_with_skill(self):
        """Test formatting cohort with skill name."""
        subjects = [
            Subject(
                subject_id="SUBJ-001",
                protocol_id="ABC-123",
                site_id="SITE-001",
                age=55,
                sex="M",
                status=SubjectStatus.ENROLLED,
            )
        ]
        result = format_cohort_summary(subjects, skill="phase3_oncology")
        
        assert "phase3_oncology" in result


class TestFormatVisitSchedule:
    """Tests for format_visit_schedule."""

    def test_empty_schedule(self):
        """Test formatting empty visit schedule."""
        result = format_visit_schedule([])
        assert "No visits scheduled" in result

    def test_visit_schedule(self):
        """Test formatting visit schedule."""
        visits = [
            Visit(
                visit_id="V001",
                subject_id="SUBJ-001",
                protocol_id="ABC-123",
                site_id="SITE-001",
                visit_number=1,
                visit_name="Screening",
                visit_type=VisitType.SCREENING,
                planned_date=date(2025, 6, 1),
                visit_status="completed",
            ),
            Visit(
                visit_id="V002",
                subject_id="SUBJ-001",
                protocol_id="ABC-123",
                site_id="SITE-001",
                visit_number=2,
                visit_name="Baseline",
                visit_type=VisitType.BASELINE,
                planned_date=date(2025, 6, 15),
                visit_status="scheduled",
            ),
        ]
        result = format_visit_schedule(visits)
        
        assert "2 visits" in result
        assert "Screening" in result
        assert "Baseline" in result


class TestFormatAdverseEvents:
    """Tests for format_adverse_events."""

    def test_no_adverse_events(self):
        """Test formatting when no adverse events."""
        result = format_adverse_events([])
        assert "No adverse events recorded" in result

    def test_adverse_events(self):
        """Test formatting adverse events."""
        aes = [
            AdverseEvent(
                ae_id="AE001",
                subject_id="SUBJ-001",
                protocol_id="ABC-123",
                ae_term="Headache",
                severity=AESeverity.GRADE_1,
                onset_date=date(2025, 6, 20),
                is_serious=False,
            ),
            AdverseEvent(
                ae_id="AE002",
                subject_id="SUBJ-001",
                protocol_id="ABC-123",
                ae_term="Nausea",
                severity=AESeverity.GRADE_2,
                onset_date=date(2025, 6, 22),
                is_serious=False,
                causality=AECausality.POSSIBLY,
            ),
        ]
        result = format_adverse_events(aes)
        
        assert "2" in result
        assert "Headache" in result
        assert "Nausea" in result
        assert "Grade" in result


class TestFormatExposures:
    """Tests for format_exposures."""

    def test_no_exposures(self):
        """Test formatting when no exposures."""
        result = format_exposures([])
        assert "No exposures recorded" in result

    def test_exposures(self):
        """Test formatting drug exposures."""
        exposures = [
            Exposure(
                exposure_id="EXP001",
                subject_id="SUBJ-001",
                protocol_id="ABC-123",
                drug_name="Study Drug A",
                dose=100.0,
                dose_unit="mg",
                start_date=date(2025, 6, 15),
                compliance_pct=95.5,
            ),
        ]
        result = format_exposures(exposures)
        
        assert "Study Drug A" in result
        assert "100" in result
        assert "mg" in result
        assert "95.5%" in result


class TestFormatSkills:
    """Tests for skill formatting functions."""

    def test_empty_skill_list(self):
        """Test formatting empty skill list."""
        result = format_skill_list([])
        assert "No skills available" in result

    def test_skill_list(self):
        """Test formatting skill list."""
        skills = [
            {"name": "phase3_oncology", "description": "Phase 3 oncology trial"},
            {"name": "phase2_diabetes", "description": "Phase 2 diabetes trial"},
        ]
        result = format_skill_list(skills)
        
        assert "Available TrialSim Skills" in result
        assert "phase3_oncology" in result
        assert "phase2_diabetes" in result

    def test_skill_details(self):
        """Test formatting skill details."""
        skill = {
            "name": "phase3_oncology",
            "description": "Phase 3 oncology trial with tumor assessments",
            "parameters": {
                "treatment_cycles": {"description": "Number of treatment cycles"},
            },
        }
        result = format_skill_details(skill)
        
        assert "phase3_oncology" in result
        assert "treatment_cycles" in result


class TestUtilityFormatters:
    """Tests for utility formatting functions."""

    def test_format_success(self):
        """Test success message formatting."""
        result = format_success("Operation completed")
        assert "✓" in result
        assert "Operation completed" in result

    def test_format_error(self):
        """Test error message formatting."""
        result = format_error("Something went wrong")
        assert "Error" in result
        assert "Something went wrong" in result
