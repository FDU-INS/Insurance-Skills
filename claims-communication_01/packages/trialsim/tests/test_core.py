"""Tests for TrialSim core generators and models."""

from datetime import date

import pytest

from trialsim.core import (
    AdverseEvent,
    AdverseEventGenerator,
    AECausality,
    AEOutcome,
    AESeverity,
    ArmType,
    Exposure,
    ExposureGenerator,
    Protocol,
    Site,
    Subject,
    SubjectStatus,
    TrialSubjectGenerator,
    Visit,
    VisitGenerator,
    VisitType,
)


class TestSubjectModels:
    """Tests for Subject model."""

    def test_subject_creation(self):
        """Test basic subject creation."""
        subject = Subject(
            protocol_id="PROTO-001",
            site_id="SITE-001",
            age=45,
            sex="M",
        )
        assert subject.protocol_id == "PROTO-001"
        assert subject.site_id == "SITE-001"
        assert subject.age == 45
        assert subject.status == SubjectStatus.SCREENING
        assert subject.subject_id.startswith("SUBJ-")

    def test_subject_with_arm(self):
        """Test subject with treatment arm."""
        subject = Subject(
            protocol_id="PROTO-001",
            site_id="SITE-001",
            age=55,
            sex="F",
            arm=ArmType.TREATMENT,
            status=SubjectStatus.RANDOMIZED,
        )
        assert subject.arm == ArmType.TREATMENT
        assert subject.status == SubjectStatus.RANDOMIZED


class TestSiteAndProtocol:
    """Tests for Site and Protocol models."""

    def test_site_creation(self):
        """Test site model creation."""
        site = Site(
            name="City Hospital",
            country="USA",
            region="Northeast",
        )
        assert site.name == "City Hospital"
        assert site.is_active is True
        assert site.site_id.startswith("SITE-")

    def test_protocol_creation(self):
        """Test protocol model creation."""
        protocol = Protocol(
            protocol_id="ABC-123",
            study_title="A Study of Drug X",
            phase="Phase 3",
            therapeutic_area="Oncology",
        )
        assert protocol.protocol_id == "ABC-123"
        assert protocol.phase == "Phase 3"
        assert protocol.planned_enrollment == 100


class TestTrialSubjectGenerator:
    """Tests for TrialSubjectGenerator."""

    def test_generate_single(self, subject_generator):
        """Test generating a single subject."""
        subject = subject_generator.generate(protocol_id="TEST-001")
        
        assert isinstance(subject, Subject)
        assert subject.protocol_id == "TEST-001"
        assert 18 <= subject.age <= 75
        assert subject.sex in ["M", "F"]
        assert subject.race is not None

    def test_generate_many(self, subject_generator):
        """Test generating multiple subjects."""
        subjects = subject_generator.generate_many(
            count=10,
            protocol_id="TEST-001",
            sites=["SITE-A", "SITE-B"],
        )
        
        assert len(subjects) == 10
        site_ids = {s.site_id for s in subjects}
        assert site_ids <= {"SITE-A", "SITE-B"}

    def test_reproducibility(self):
        """Test that seeded generation is reproducible."""
        gen1 = TrialSubjectGenerator(seed=123)
        gen2 = TrialSubjectGenerator(seed=123)
        
        s1 = gen1.generate(protocol_id="P1")
        s2 = gen2.generate(protocol_id="P1")
        
        assert s1.age == s2.age
        assert s1.sex == s2.sex


class TestVisitGenerator:
    """Tests for VisitGenerator."""

    def test_generate_schedule(self, visit_generator, sample_subject):
        """Test generating a visit schedule."""
        visits = visit_generator.generate_schedule(
            subject=sample_subject,
            duration_weeks=24,
            start_date=date(2025, 1, 1),
        )
        
        assert len(visits) > 0
        assert visits[0].visit_type == VisitType.SCREENING
        assert visits[1].visit_type == VisitType.RANDOMIZATION
        assert visits[-1].visit_type == VisitType.END_OF_STUDY

    def test_visit_attributes(self, visit_generator, sample_subject):
        """Test visit attributes are set correctly."""
        visits = visit_generator.generate_schedule(
            subject=sample_subject,
            duration_weeks=12,
        )
        
        for visit in visits:
            assert visit.subject_id == sample_subject.subject_id
            assert visit.protocol_id == sample_subject.protocol_id
            assert visit.visit_id.startswith("VST-")


class TestAdverseEventGenerator:
    """Tests for AdverseEventGenerator."""

    def test_generate_for_subject(self, ae_generator, sample_subject):
        """Test generating adverse events."""
        aes = ae_generator.generate_for_subject(
            subject=sample_subject,
            visit_count=10,
            ae_probability=1.0,  # Force AE generation
        )
        
        assert len(aes) == 10
        for ae in aes:
            assert ae.subject_id == sample_subject.subject_id
            assert ae.ae_term is not None
            assert ae.severity in list(AESeverity)

    def test_ae_severity_distribution(self, ae_generator, sample_subject):
        """Test that severe AEs are less common."""
        # Generate many AEs
        all_aes = []
        for _ in range(100):
            aes = ae_generator.generate_for_subject(
                subject=sample_subject,
                visit_count=5,
                ae_probability=1.0,
            )
            all_aes.extend(aes)
        
        # Count severities
        mild = sum(1 for ae in all_aes if ae.severity == AESeverity.GRADE_1)
        severe = sum(1 for ae in all_aes if ae.severity in [AESeverity.GRADE_4, AESeverity.GRADE_5])
        
        # Mild should be more common than severe
        assert mild > severe


class TestExposureGenerator:
    """Tests for ExposureGenerator."""

    def test_generate_for_subject(self, exposure_generator, sample_subject):
        """Test generating exposures."""
        exposures = exposure_generator.generate_for_subject(
            subject=sample_subject,
            drug_name="Test Drug",
            dose=50.0,
            duration_weeks=4,
        )
        
        assert len(exposures) == 4  # One per week
        for exp in exposures:
            assert exp.subject_id == sample_subject.subject_id
            assert exp.drug_name == "Test Drug"
            assert exp.dose == 50.0
            assert 80.0 <= exp.compliance_pct <= 100.0


class TestVisitModel:
    """Tests for Visit model."""

    def test_visit_creation(self):
        """Test basic visit creation."""
        visit = Visit(
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            site_id="SITE-001",
            visit_number=1,
            visit_name="Screening",
            visit_type=VisitType.SCREENING,
        )
        assert visit.visit_number == 1
        assert visit.visit_type == VisitType.SCREENING
        assert visit.visit_status == "scheduled"


class TestAdverseEventModel:
    """Tests for AdverseEvent model."""

    def test_ae_creation(self):
        """Test basic AE creation."""
        ae = AdverseEvent(
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            ae_term="Headache",
            onset_date=date(2025, 1, 15),
            severity=AESeverity.GRADE_1,
        )
        assert ae.ae_term == "Headache"
        assert ae.severity == AESeverity.GRADE_1
        assert ae.is_serious is False

    def test_serious_ae(self):
        """Test serious AE attributes."""
        ae = AdverseEvent(
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            ae_term="Cardiac arrest",
            onset_date=date(2025, 1, 15),
            severity=AESeverity.GRADE_4,
            is_serious=True,
            causality=AECausality.POSSIBLY,
            outcome=AEOutcome.RECOVERED,
        )
        assert ae.is_serious is True
        assert ae.causality == AECausality.POSSIBLY


class TestExposureModel:
    """Tests for Exposure model."""

    def test_exposure_creation(self):
        """Test basic exposure creation."""
        exp = Exposure(
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            drug_name="Drug X",
            dose=100.0,
            start_date=date(2025, 1, 1),
        )
        assert exp.drug_name == "Drug X"
        assert exp.dose == 100.0
        assert exp.compliance_pct == 100.0
