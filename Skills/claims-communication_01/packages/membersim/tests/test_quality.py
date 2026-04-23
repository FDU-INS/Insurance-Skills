"""Tests for quality measures and care gaps."""

from datetime import date

from healthsim.person import Address, Gender, PersonName

from membersim import Member
from membersim.authorization import Authorization, AuthorizationStatus
from membersim.formats.x12 import generate_278_request, generate_278_response
from membersim.quality import (
    HEDIS_MEASURES,
    GapStatus,
    generate_care_gaps,
    generate_measure_status,
    get_measure,
    get_measures_for_member,
)

# ============================================================================
# HEDIS Measure Tests
# ============================================================================


class TestHEDISMeasures:
    """Tests for HEDIS measure definitions."""

    def test_hedis_measures_defined(self) -> None:
        """Test that HEDIS measures are defined."""
        assert "BCS" in HEDIS_MEASURES
        assert "CDC-A1C" in HEDIS_MEASURES
        assert "COL" in HEDIS_MEASURES
        assert "CCS" in HEDIS_MEASURES
        assert "CDC-EYE" in HEDIS_MEASURES
        assert "CBP" in HEDIS_MEASURES

    def test_get_measure(self) -> None:
        """Test getting a specific measure."""
        bcs = get_measure("BCS")
        assert bcs.measure_id == "BCS"
        assert bcs.min_age == 50
        assert bcs.max_age == 74
        assert bcs.gender == "F"

    def test_get_measure_unknown_raises(self) -> None:
        """Test that unknown measure raises error."""
        try:
            get_measure("UNKNOWN")
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "Unknown measure" in str(e)

    def test_bcs_measure_details(self) -> None:
        """Test BCS measure has correct details."""
        bcs = get_measure("BCS")
        assert bcs.measure_name == "Breast Cancer Screening"
        assert "77067" in bcs.compliant_codes  # Mammogram code
        assert "Z90.1" in bcs.exclusion_codes  # Mastectomy exclusion

    def test_cdc_a1c_measure_details(self) -> None:
        """Test CDC-A1C measure details."""
        cdc = get_measure("CDC-A1C")
        assert cdc.min_age == 18
        assert cdc.max_age == 75
        assert cdc.gender is None  # Both genders
        assert "83036" in cdc.compliant_codes  # HbA1c test


class TestMeasuresForMember:
    """Tests for get_measures_for_member function."""

    def test_measures_for_female_55(self) -> None:
        """Test applicable measures for 55-year-old female."""
        measures = get_measures_for_member(age=55, gender="F")
        assert "BCS" in measures
        assert "CCS" in measures
        assert "COL" in measures
        assert "CBP" in measures

    def test_measures_for_male_55(self) -> None:
        """Test applicable measures for 55-year-old male."""
        measures = get_measures_for_member(age=55, gender="M")
        assert "BCS" not in measures  # Women only
        assert "CCS" not in measures  # Women only
        assert "COL" in measures  # All adults
        assert "CBP" in measures

    def test_measures_for_young_adult(self) -> None:
        """Test measures for 25-year-old female."""
        measures = get_measures_for_member(age=25, gender="F")
        assert "BCS" not in measures  # Age 50+
        assert "CCS" in measures  # Age 21-64
        assert "COL" not in measures  # Age 50+
        assert "CBP" in measures

    def test_measures_for_diabetic(self) -> None:
        """Test CDC measures for diabetic member."""
        measures = get_measures_for_member(
            age=55,
            gender="M",
            diagnoses=["E11.9"],  # Type 2 diabetes
        )
        assert "CDC-A1C" in measures
        assert "CDC-EYE" in measures

    def test_measures_for_non_diabetic(self) -> None:
        """Test CDC measures excluded for non-diabetic member."""
        measures = get_measures_for_member(age=55, gender="M", diagnoses=[])
        assert "CDC-A1C" not in measures
        assert "CDC-EYE" not in measures


# ============================================================================
# Care Gap Generation Tests
# ============================================================================


class TestCareGapGeneration:
    """Tests for care gap generation."""

    def test_generate_measure_status_not_applicable(self, sample_address: Address) -> None:
        """Test measure status for member outside denominator."""
        # Create 25-year-old male - not eligible for BCS
        member = Member(
            id="person-001",
            name=PersonName(given_name="John", family_name="Smith"),
            birth_date=date(1999, 1, 1),
            gender=Gender.MALE,
            address=sample_address,
            member_id="MEM001",
            relationship_code="18",
            group_id="GRP001",
            coverage_start=date(2024, 1, 1),
            plan_code="PPO",
        )

        status = generate_measure_status(
            member=member,
            measure_id="BCS",
            measure_year=2024,
            seed=42,
        )

        assert status.member_id == "MEM001"
        assert status.measure_id == "BCS"
        assert not status.in_denominator
        assert status.gap_status == GapStatus.NOT_APPLICABLE

    def test_generate_measure_status_in_denominator(self, sample_address: Address) -> None:
        """Test measure status for member in denominator."""
        # Create 55-year-old female - eligible for BCS
        member = Member(
            id="person-002",
            name=PersonName(given_name="Jane", family_name="Doe"),
            birth_date=date(1969, 6, 15),
            gender=Gender.FEMALE,
            address=sample_address,
            member_id="MEM002",
            relationship_code="18",
            group_id="GRP001",
            coverage_start=date(2024, 1, 1),
            plan_code="PPO",
        )

        status = generate_measure_status(
            member=member,
            measure_id="BCS",
            measure_year=2024,
            seed=42,
        )

        assert status.member_id == "MEM002"
        assert status.in_denominator
        assert status.gap_status in [
            GapStatus.OPEN,
            GapStatus.CLOSED,
            GapStatus.EXCLUDED,
        ]

    def test_generate_care_gaps_population(self, sample_address: Address) -> None:
        """Test care gap generation for a population."""
        # Create diverse population
        members = [
            Member(
                id="person-001",
                name=PersonName(given_name="Jane", family_name="Doe"),
                birth_date=date(1969, 6, 15),
                gender=Gender.FEMALE,
                address=sample_address,
                member_id="MEM001",
                relationship_code="18",
                group_id="GRP001",
                coverage_start=date(2024, 1, 1),
                plan_code="PPO",
            ),
            Member(
                id="person-002",
                name=PersonName(given_name="John", family_name="Smith"),
                birth_date=date(1970, 3, 20),
                gender=Gender.MALE,
                address=sample_address,
                member_id="MEM002",
                relationship_code="18",
                group_id="GRP001",
                coverage_start=date(2024, 1, 1),
                plan_code="PPO",
            ),
        ]

        results = generate_care_gaps(
            members=members,
            measures=["COL"],  # Both eligible
            gap_rate=0.5,
            seed=42,
        )

        assert len(results) == 2
        for status in results:
            assert status.measure_id == "COL"
            assert status.in_denominator


class TestMemberMeasureStatus:
    """Tests for MemberMeasureStatus model."""

    def test_has_open_gap_true(self) -> None:
        """Test has_open_gap property when gap is open."""
        from membersim.quality.measure import MemberMeasureStatus

        status = MemberMeasureStatus(
            member_id="MEM001",
            measure_id="BCS",
            measure_year=2024,
            in_denominator=True,
            in_numerator=False,
            gap_status=GapStatus.OPEN,
        )

        assert status.has_open_gap

    def test_has_open_gap_false_closed(self) -> None:
        """Test has_open_gap property when gap is closed."""
        from membersim.quality.measure import MemberMeasureStatus

        status = MemberMeasureStatus(
            member_id="MEM001",
            measure_id="BCS",
            measure_year=2024,
            in_denominator=True,
            in_numerator=True,
            gap_status=GapStatus.CLOSED,
            last_service_date=date(2024, 3, 15),
        )

        assert not status.has_open_gap


# ============================================================================
# Authorization Tests
# ============================================================================


class TestAuthorization:
    """Tests for Authorization model."""

    def test_create_authorization(self) -> None:
        """Test creating an authorization."""
        auth = Authorization(
            auth_number="AUTH001",
            member_id="MEM001",
            provider_npi="1234567890",
            service_type="OUTPATIENT",
            procedure_codes=["70553"],  # MRI
            diagnosis_codes=["M54.5"],  # Low back pain
            request_date=date(2024, 3, 1),
        )

        assert auth.auth_number == "AUTH001"
        assert auth.status == AuthorizationStatus.PENDING
        assert auth.is_pending
        assert not auth.is_approved

    def test_approved_authorization(self) -> None:
        """Test approved authorization."""
        auth = Authorization(
            auth_number="AUTH002",
            member_id="MEM001",
            provider_npi="1234567890",
            service_type="OUTPATIENT",
            procedure_codes=["70553"],
            diagnosis_codes=["M54.5"],
            request_date=date(2024, 3, 1),
            decision_date=date(2024, 3, 2),
            status=AuthorizationStatus.APPROVED,
            approved_units=1,
            effective_start=date(2024, 3, 15),
            effective_end=date(2024, 4, 15),
        )

        assert auth.is_approved
        assert not auth.is_pending
        assert auth.approved_units == 1

    def test_denied_authorization(self) -> None:
        """Test denied authorization."""
        auth = Authorization(
            auth_number="AUTH003",
            member_id="MEM001",
            provider_npi="1234567890",
            service_type="OUTPATIENT",
            procedure_codes=["70553"],
            diagnosis_codes=["M54.5"],
            request_date=date(2024, 3, 1),
            decision_date=date(2024, 3, 2),
            status=AuthorizationStatus.DENIED,
            denial_code="MNC",
            denial_reason="Medical necessity criteria not met",
        )

        assert not auth.is_approved
        assert auth.denial_code == "MNC"


# ============================================================================
# X12 278 Tests
# ============================================================================


class TestEDI278Generator:
    """Tests for X12 278 Prior Authorization generators."""

    def test_generate_278_request(self) -> None:
        """Test 278 request generation."""
        auth = Authorization(
            auth_number="AUTH001",
            member_id="MEM001",
            provider_npi="1234567890",
            service_type="OUTPATIENT",
            procedure_codes=["70553"],
            diagnosis_codes=["M54.5"],
            request_date=date(2024, 3, 1),
            effective_start=date(2024, 3, 15),
        )

        edi = generate_278_request(auth)

        # Check envelope
        assert "ISA*" in edi
        assert "GS*HI*" in edi
        assert "ST*278*" in edi

        # Check BHT segment
        assert "BHT*0007*13*AUTH001*" in edi

        # Check UM segment present
        assert "UM*" in edi

        # Check diagnosis
        assert "HI*ABK:M54.5~" in edi

        # Check service
        assert "SV1*HC:70553*" in edi

    def test_generate_278_response_approved(self) -> None:
        """Test 278 response generation for approved auth."""
        auth = Authorization(
            auth_number="AUTH001",
            member_id="MEM001",
            provider_npi="1234567890",
            service_type="OUTPATIENT",
            procedure_codes=["70553"],
            diagnosis_codes=["M54.5"],
            request_date=date(2024, 3, 1),
            decision_date=date(2024, 3, 2),
            status=AuthorizationStatus.APPROVED,
            approved_units=1,
            effective_start=date(2024, 3, 15),
            effective_end=date(2024, 4, 15),
        )

        edi = generate_278_response(auth)

        # Check envelope
        assert "ISA*" in edi
        assert "ST*278*" in edi

        # Check BHT response code
        assert "BHT*0007*11*AUTH001*" in edi

        # Check AAA segment with approved code
        assert "AAA*Y**A1~" in edi

        # Check HSD segment for approved units
        assert "HSD*VS*1~" in edi

    def test_generate_278_response_denied(self) -> None:
        """Test 278 response generation for denied auth."""
        auth = Authorization(
            auth_number="AUTH002",
            member_id="MEM001",
            provider_npi="1234567890",
            service_type="OUTPATIENT",
            procedure_codes=["70553"],
            diagnosis_codes=["M54.5"],
            request_date=date(2024, 3, 1),
            decision_date=date(2024, 3, 2),
            status=AuthorizationStatus.DENIED,
            denial_code="MNC",
        )

        edi = generate_278_response(auth)

        # Check AAA segment with denied code
        assert "AAA*Y**A3~" in edi  # A3 = Not Certified
