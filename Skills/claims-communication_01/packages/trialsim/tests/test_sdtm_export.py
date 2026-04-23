"""Tests for SDTM export functionality."""

import pytest
import tempfile
from datetime import date
from pathlib import Path

from trialsim.core.models import (
    AdverseEvent,
    AECausality,
    AEOutcome,
    AESeverity,
    ArmType,
    Exposure,
    Subject,
    SubjectStatus,
    Visit,
    VisitType,
)
from trialsim.formats.sdtm import (
    SDTMDomain,
    SDTMVariable,
    ExportConfig,
    ExportFormat,
    ExportResult,
    SDTMExporter,
    export_to_sdtm,
    create_sdtm_exporter,
    get_domain_variables,
    get_required_variables,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_subjects():
    """Create sample subjects for testing."""
    return [
        Subject(
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            site_id="SITE01",
            age=45,
            sex="M",
            race="WHITE",
            ethnicity="NOT HISPANIC OR LATINO",
            screening_date=date(2025, 1, 1),
            randomization_date=date(2025, 1, 15),
            arm=ArmType.TREATMENT,
            status=SubjectStatus.ON_TREATMENT,
        ),
        Subject(
            subject_id="SUBJ-002",
            protocol_id="PROTO-001",
            site_id="SITE01",
            age=52,
            sex="F",
            race="BLACK OR AFRICAN AMERICAN",
            ethnicity="NOT HISPANIC OR LATINO",
            screening_date=date(2025, 1, 5),
            randomization_date=date(2025, 1, 20),
            arm=ArmType.PLACEBO,
            status=SubjectStatus.ON_TREATMENT,
        ),
    ]


@pytest.fixture
def sample_visits(sample_subjects):
    """Create sample visits for testing."""
    subj = sample_subjects[0]
    return [
        Visit(
            visit_id="VST-001",
            subject_id=subj.subject_id,
            protocol_id=subj.protocol_id,
            site_id=subj.site_id,
            visit_number=1,
            visit_name="Screening",
            visit_type=VisitType.SCREENING,
            planned_date=date(2025, 1, 1),
            actual_date=date(2025, 1, 1),
            visit_status="completed",
        ),
        Visit(
            visit_id="VST-002",
            subject_id=subj.subject_id,
            protocol_id=subj.protocol_id,
            site_id=subj.site_id,
            visit_number=2,
            visit_name="Baseline",
            visit_type=VisitType.BASELINE,
            planned_date=date(2025, 1, 15),
            actual_date=date(2025, 1, 15),
            visit_status="completed",
        ),
        Visit(
            visit_id="VST-003",
            subject_id=subj.subject_id,
            protocol_id=subj.protocol_id,
            site_id=subj.site_id,
            visit_number=3,
            visit_name="Week 4",
            visit_type=VisitType.SCHEDULED,
            planned_date=date(2025, 2, 12),
            actual_date=date(2025, 2, 14),
            visit_status="completed",
        ),
    ]


@pytest.fixture
def sample_adverse_events(sample_subjects):
    """Create sample adverse events for testing."""
    subj = sample_subjects[0]
    return [
        AdverseEvent(
            ae_id="AE-001",
            subject_id=subj.subject_id,
            protocol_id=subj.protocol_id,
            ae_term="Headache",
            system_organ_class="Nervous system disorders",
            onset_date=date(2025, 1, 20),
            resolution_date=date(2025, 1, 22),
            severity=AESeverity.GRADE_1,
            is_serious=False,
            causality=AECausality.POSSIBLY,
            outcome=AEOutcome.RECOVERED,
        ),
        AdverseEvent(
            ae_id="AE-002",
            subject_id=subj.subject_id,
            protocol_id=subj.protocol_id,
            ae_term="Nausea",
            system_organ_class="Gastrointestinal disorders",
            onset_date=date(2025, 2, 1),
            severity=AESeverity.GRADE_2,
            is_serious=False,
            causality=AECausality.PROBABLY,
            outcome=AEOutcome.RECOVERING,
        ),
    ]


@pytest.fixture
def sample_exposures(sample_subjects):
    """Create sample exposures for testing."""
    subj = sample_subjects[0]
    return [
        Exposure(
            exposure_id="EXP-001",
            subject_id=subj.subject_id,
            protocol_id=subj.protocol_id,
            drug_name="Study Drug A",
            dose=100.0,
            dose_unit="mg",
            route="oral",
            start_date=date(2025, 1, 15),
            end_date=date(2025, 3, 15),
        ),
    ]


# =============================================================================
# Domain Tests
# =============================================================================

class TestSDTMDomains:
    """Tests for SDTM domain definitions."""

    def test_dm_variables_defined(self):
        """Test DM domain has variables defined."""
        vars = get_domain_variables(SDTMDomain.DM)
        assert len(vars) > 0
        assert any(v.name == "USUBJID" for v in vars)
        assert any(v.name == "AGE" for v in vars)

    def test_ae_variables_defined(self):
        """Test AE domain has variables defined."""
        vars = get_domain_variables(SDTMDomain.AE)
        assert len(vars) > 0
        assert any(v.name == "AETERM" for v in vars)
        assert any(v.name == "AESEV" for v in vars)

    def test_ex_variables_defined(self):
        """Test EX domain has variables defined."""
        vars = get_domain_variables(SDTMDomain.EX)
        assert len(vars) > 0
        assert any(v.name == "EXTRT" for v in vars)
        assert any(v.name == "EXDOSE" for v in vars)

    def test_sv_variables_defined(self):
        """Test SV domain has variables defined."""
        vars = get_domain_variables(SDTMDomain.SV)
        assert len(vars) > 0
        assert any(v.name == "VISITNUM" for v in vars)
        assert any(v.name == "VISIT" for v in vars)

    def test_required_variables(self):
        """Test getting required variables."""
        required = get_required_variables(SDTMDomain.DM)
        assert "STUDYID" in required
        assert "DOMAIN" in required
        assert "USUBJID" in required

    def test_variable_structure(self):
        """Test SDTMVariable structure."""
        vars = get_domain_variables(SDTMDomain.DM)
        usubjid = next(v for v in vars if v.name == "USUBJID")
        
        assert usubjid.label == "Unique Subject Identifier"
        assert usubjid.data_type == "Char"
        assert usubjid.required is True


# =============================================================================
# Exporter Tests
# =============================================================================

class TestSDTMExporter:
    """Tests for SDTMExporter."""

    def test_basic_creation(self):
        """Test creating an exporter."""
        exporter = SDTMExporter()
        assert exporter.config is not None
        assert exporter.config.study_id == "STUDY01"

    def test_creation_with_config(self):
        """Test creating with custom config."""
        config = ExportConfig(study_id="TEST001", sponsor="ACME")
        exporter = SDTMExporter(config)
        
        assert exporter.config.study_id == "TEST001"
        assert exporter.config.sponsor == "ACME"

    def test_export_dm_domain(self, sample_subjects):
        """Test exporting DM domain."""
        exporter = SDTMExporter()
        result = exporter.export(subjects=sample_subjects)
        
        assert result.success is True
        assert SDTMDomain.DM in result.domains_exported
        assert result.record_counts["DM"] == 2

    def test_export_ae_domain(self, sample_subjects, sample_adverse_events):
        """Test exporting AE domain."""
        exporter = SDTMExporter()
        result = exporter.export(
            subjects=sample_subjects,
            adverse_events=sample_adverse_events,
        )
        
        assert result.success is True
        assert SDTMDomain.AE in result.domains_exported
        assert result.record_counts["AE"] == 2

    def test_export_ex_domain(self, sample_subjects, sample_exposures):
        """Test exporting EX domain."""
        exporter = SDTMExporter()
        result = exporter.export(
            subjects=sample_subjects,
            exposures=sample_exposures,
        )
        
        assert result.success is True
        assert SDTMDomain.EX in result.domains_exported
        assert result.record_counts["EX"] == 1

    def test_export_sv_domain(self, sample_subjects, sample_visits):
        """Test exporting SV domain."""
        exporter = SDTMExporter()
        result = exporter.export(
            subjects=sample_subjects,
            visits=sample_visits,
        )
        
        assert result.success is True
        assert SDTMDomain.SV in result.domains_exported
        assert result.record_counts["SV"] == 3

    def test_export_all_domains(
        self,
        sample_subjects,
        sample_visits,
        sample_adverse_events,
        sample_exposures,
    ):
        """Test exporting all domains at once."""
        exporter = SDTMExporter()
        result = exporter.export(
            subjects=sample_subjects,
            visits=sample_visits,
            adverse_events=sample_adverse_events,
            exposures=sample_exposures,
        )
        
        assert result.success is True
        assert len(result.domains_exported) == 4

    def test_export_to_csv_files(self, sample_subjects, sample_adverse_events):
        """Test exporting to CSV files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = SDTMExporter()
            result = exporter.export(
                subjects=sample_subjects,
                adverse_events=sample_adverse_events,
                output_dir=tmpdir,
                format=ExportFormat.CSV,
            )
            
            assert result.success is True
            assert len(result.files_created) >= 2
            
            # Check files exist
            dm_path = Path(tmpdir) / "dm.csv"
            ae_path = Path(tmpdir) / "ae.csv"
            assert dm_path.exists()
            assert ae_path.exists()

    def test_export_to_json_files(self, sample_subjects):
        """Test exporting to JSON files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = SDTMExporter()
            result = exporter.export(
                subjects=sample_subjects,
                output_dir=tmpdir,
                format=ExportFormat.JSON,
            )
            
            assert result.success is True
            
            # Check file exists
            dm_path = Path(tmpdir) / "dm.json"
            assert dm_path.exists()

    def test_result_summary(self, sample_subjects, sample_adverse_events):
        """Test export result summary generation."""
        exporter = SDTMExporter()
        result = exporter.export(
            subjects=sample_subjects,
            adverse_events=sample_adverse_events,
        )
        
        summary = result.to_summary()
        
        assert "SDTM Export Summary" in summary
        assert "Success" in summary
        assert "DM:" in summary
        assert "AE:" in summary


class TestDMConversion:
    """Tests for DM domain conversion."""

    def test_usubjid_format(self, sample_subjects):
        """Test USUBJID is correctly formatted."""
        exporter = SDTMExporter(ExportConfig(study_id="TEST01"))
        records = exporter._convert_dm(sample_subjects)
        
        assert records[0]["USUBJID"] == "TEST01-SITE01-SUBJ-001"

    def test_sex_mapping(self, sample_subjects):
        """Test sex is mapped correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_dm(sample_subjects)
        
        assert records[0]["SEX"] == "M"
        assert records[1]["SEX"] == "F"

    def test_arm_mapping(self, sample_subjects):
        """Test arm is mapped correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_dm(sample_subjects)
        
        assert records[0]["ARMCD"] == "TREATMENT"
        assert records[1]["ARMCD"] == "PLACEBO"


class TestAEConversion:
    """Tests for AE domain conversion."""

    def test_severity_mapping(self, sample_subjects, sample_adverse_events):
        """Test severity is mapped correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_ae(sample_adverse_events, sample_subjects)
        
        assert records[0]["AESEV"] == "MILD"
        assert records[1]["AESEV"] == "MODERATE"

    def test_serious_flag(self, sample_subjects, sample_adverse_events):
        """Test serious flag is set correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_ae(sample_adverse_events, sample_subjects)
        
        assert records[0]["AESER"] == "N"

    def test_sequence_numbers(self, sample_subjects, sample_adverse_events):
        """Test sequence numbers are assigned correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_ae(sample_adverse_events, sample_subjects)
        
        assert records[0]["AESEQ"] == 1
        assert records[1]["AESEQ"] == 2

    def test_study_day_calculation(self, sample_subjects, sample_adverse_events):
        """Test study day is calculated correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_ae(sample_adverse_events, sample_subjects)
        
        # First AE onset is 5 days after randomization (Jan 20 - Jan 15 + 1 = 6)
        assert records[0]["AESTDY"] == 6


class TestEXConversion:
    """Tests for EX domain conversion."""

    def test_dose_mapping(self, sample_subjects, sample_exposures):
        """Test dose values are mapped correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_ex(sample_exposures, sample_subjects)
        
        assert records[0]["EXDOSE"] == 100.0
        assert records[0]["EXDOSU"] == "MG"

    def test_route_mapping(self, sample_subjects, sample_exposures):
        """Test route is mapped correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_ex(sample_exposures, sample_subjects)
        
        assert records[0]["EXROUTE"] == "ORAL"


class TestSVConversion:
    """Tests for SV domain conversion."""

    def test_visit_info(self, sample_subjects, sample_visits):
        """Test visit information is mapped correctly."""
        exporter = SDTMExporter()
        records = exporter._convert_sv(sample_visits, sample_subjects)
        
        assert records[0]["VISITNUM"] == 1
        assert records[0]["VISIT"] == "Screening"
        assert records[0]["EPOCH"] == "SCREENING"

    def test_epoch_mapping(self, sample_subjects, sample_visits):
        """Test epoch is mapped correctly for different visit types."""
        exporter = SDTMExporter()
        records = exporter._convert_sv(sample_visits, sample_subjects)
        
        assert records[0]["EPOCH"] == "SCREENING"
        assert records[1]["EPOCH"] == "BASELINE"
        assert records[2]["EPOCH"] == "TREATMENT"


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_export_to_sdtm(self, sample_subjects):
        """Test export_to_sdtm function."""
        result = export_to_sdtm(
            subjects=sample_subjects,
            study_id="CONV01",
        )
        
        assert result.success is True
        assert SDTMDomain.DM in result.domains_exported

    def test_create_sdtm_exporter(self):
        """Test create_sdtm_exporter function."""
        exporter = create_sdtm_exporter(
            study_id="FACTORY01",
            sponsor="TEST SPONSOR",
        )
        
        assert isinstance(exporter, SDTMExporter)
        assert exporter.config.study_id == "FACTORY01"
        assert exporter.config.sponsor == "TEST SPONSOR"
