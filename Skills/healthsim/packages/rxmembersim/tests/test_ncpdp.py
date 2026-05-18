"""Tests for NCPDP formats."""
from datetime import date
from decimal import Decimal

import pytest

from rxmembersim.claims.claim import PharmacyClaim, TransactionCode
from rxmembersim.claims.response import ClaimResponse, RejectCode
from rxmembersim.core.pharmacy import Pharmacy, PharmacyGenerator, PharmacyType
from rxmembersim.core.prescriber import (
    Prescriber,
    PrescriberGenerator,
    PrescriberSpecialty,
    PrescriberType,
)
from rxmembersim.formats.ncpdp.reject_codes import (
    RejectCategory,
    get_reject_category,
    get_reject_description,
    is_dur_reject,
    is_hard_reject,
)
from rxmembersim.formats.ncpdp.script import (
    NCPDPScriptGenerator,
    NewRxMessage,
    RxChangeMessage,
    RxChangeType,
    RxRenewalMessage,
)
from rxmembersim.formats.ncpdp.telecom import NCPDPTelecomGenerator


class TestNCPDPTelecom:
    """Tests for NCPDP Telecommunication generator."""

    @pytest.fixture
    def claim(self) -> PharmacyClaim:
        """Create a test claim."""
        return PharmacyClaim(
            claim_id="CLM001",
            transaction_code=TransactionCode.BILLING,
            service_date=date(2025, 1, 15),
            pharmacy_npi="1234567890",
            member_id="MEM001",
            cardholder_id="CH001",
            person_code="01",
            bin="610014",
            pcn="RXTEST",
            group_number="GRP001",
            prescription_number="RX123456",
            fill_number=1,
            ndc="00071015523",
            quantity_dispensed=Decimal("30"),
            days_supply=30,
            daw_code="0",
            prescriber_npi="0987654321",
            ingredient_cost_submitted=Decimal("150.00"),
            dispensing_fee_submitted=Decimal("2.50"),
            usual_customary_charge=Decimal("175.00"),
            gross_amount_due=Decimal("152.50"),
        )

    @pytest.fixture
    def response(self) -> ClaimResponse:
        """Create a test response."""
        return ClaimResponse(
            claim_id="CLM001",
            transaction_response_status="A",
            response_status="P",
            authorization_number="AUTH123456789",
            ingredient_cost_paid=Decimal("150.00"),
            dispensing_fee_paid=Decimal("2.50"),
            total_amount_paid=Decimal("122.50"),
            patient_pay_amount=Decimal("30.00"),
            copay_amount=Decimal("30.00"),
        )

    def test_generate_b1_request(self, claim: PharmacyClaim) -> None:
        """Test B1 claim request generation."""
        generator = NCPDPTelecomGenerator()
        message = generator.generate_b1_request(claim)

        # Check message contains expected segments
        assert "AM01" in message  # Header
        assert "AM04" in message  # Insurance
        assert "AM07" in message  # Claim
        assert "AM11" in message  # Pricing

        # Check key fields are present
        assert claim.bin in message
        assert claim.ndc in message
        assert claim.prescriber_npi in message

    def test_generate_b2_reversal(self, claim: PharmacyClaim) -> None:
        """Test B2 reversal request generation."""
        generator = NCPDPTelecomGenerator()
        message = generator.generate_b2_reversal(claim, "AUTH123")

        # Check transaction code is B2
        assert "D0B2" in message
        # Check original auth is included
        assert "AUTH123" in message

    def test_generate_b3_rebill(self, claim: PharmacyClaim) -> None:
        """Test B3 rebill request generation."""
        generator = NCPDPTelecomGenerator()
        message = generator.generate_b3_rebill(claim, "AUTH123")

        # Check transaction code is B3
        assert "D0B3" in message

    def test_generate_response(self, response: ClaimResponse) -> None:
        """Test response generation."""
        generator = NCPDPTelecomGenerator()
        message = generator.generate_response(response)

        # Check response segments
        assert "AM20" in message  # Response header
        assert "AM21" in message  # Response status
        assert "AM23" in message  # Response pricing (paid claim)

        # Check auth number is present
        assert "AUTH123456789" in message

    def test_generate_rejection_response(self) -> None:
        """Test rejection response generation."""
        response = ClaimResponse(
            claim_id="CLM001",
            transaction_response_status="R",
            response_status="R",
            reject_codes=[
                RejectCode(code="75", description="Prior Authorization Required")
            ],
        )

        generator = NCPDPTelecomGenerator()
        message = generator.generate_response(response)

        # Check reject code is present
        assert "75" in message

    def test_parse_response(self) -> None:
        """Test response parsing."""
        generator = NCPDPTelecomGenerator()

        # Create a simple test message
        test_message = (
            f"AM20{generator.FIELD_SEPARATOR}ANA{generator.FIELD_SEPARATOR}F3AUTH123"
        )

        result = generator.parse_response(test_message)
        assert result.get("AN") == "A"
        assert result.get("F3") == "AUTH123"


class TestNCPDPScript:
    """Tests for NCPDP SCRIPT generator."""

    @pytest.fixture
    def new_rx_message(self) -> NewRxMessage:
        """Create a test NewRx message."""
        return NewRxMessage(
            message_id="MSG-001",
            prescriber_npi="1234567890",
            prescriber_first_name="John",
            prescriber_last_name="Smith",
            prescriber_address="123 Medical Center Dr",
            prescriber_city="Boston",
            prescriber_state="MA",
            prescriber_zip="02101",
            prescriber_phone="617-555-1234",
            prescriber_dea="AS1234567",
            patient_first_name="Jane",
            patient_last_name="Doe",
            patient_dob=date(1985, 6, 15),
            patient_gender="F",
            patient_address="456 Main St",
            patient_city="Boston",
            patient_state="MA",
            patient_zip="02102",
            drug_description="Lipitor 10mg Tablet",
            ndc="00071015523",
            quantity="30",
            days_supply=30,
            directions="Take 1 tablet by mouth daily",
            refills=5,
        )

    def test_generate_new_rx(self, new_rx_message: NewRxMessage) -> None:
        """Test NewRx message generation."""
        generator = NCPDPScriptGenerator()
        xml = generator.generate_new_rx(new_rx_message)

        # Check XML structure
        assert '<?xml version="1.0"' in xml
        assert "<Message" in xml
        assert "<NewRx>" in xml
        assert "<Prescriber>" in xml
        assert "<Patient>" in xml
        assert "<MedicationPrescribed>" in xml

        # Check content
        assert "1234567890" in xml  # Prescriber NPI
        assert "Jane" in xml  # Patient first name
        assert "Lipitor" in xml  # Drug description
        assert "00071015523" in xml  # NDC

    def test_generate_new_rx_with_pharmacy(self, new_rx_message: NewRxMessage) -> None:
        """Test NewRx with directed pharmacy."""
        new_rx_message.pharmacy_ncpdp = "1234567"
        new_rx_message.pharmacy_npi = "9876543210"
        new_rx_message.pharmacy_name = "Test Pharmacy"

        generator = NCPDPScriptGenerator()
        xml = generator.generate_new_rx(new_rx_message)

        assert "<Pharmacy>" in xml
        assert "1234567" in xml
        assert "Test Pharmacy" in xml

    def test_generate_rx_change(self) -> None:
        """Test RxChange message generation."""
        message = RxChangeMessage(
            message_id="MSG-002",
            relates_to_message_id="MSG-001",
            change_type=RxChangeType.GENERIC_SUBSTITUTION,
            change_reason="Brand not in stock",
            original_drug_description="Lipitor 10mg Tablet",
            original_ndc="00071015523",
            proposed_drug_description="Atorvastatin 10mg Tablet",
            proposed_ndc="00093720101",
            proposed_quantity="30",
            proposed_days_supply=30,
            pharmacy_ncpdp="1234567",
            pharmacy_npi="9876543210",
        )

        generator = NCPDPScriptGenerator()
        xml = generator.generate_rx_change(message)

        assert "<RxChangeRequest>" in xml
        assert "MSG-001" in xml  # Relates to
        assert "Lipitor" in xml  # Original drug
        assert "Atorvastatin" in xml  # Proposed drug

    def test_generate_rx_renewal(self) -> None:
        """Test RxRenewal message generation."""
        message = RxRenewalMessage(
            message_id="MSG-003",
            patient_first_name="Jane",
            patient_last_name="Doe",
            patient_dob=date(1985, 6, 15),
            prescription_number="RX123456",
            drug_description="Lipitor 10mg Tablet",
            ndc="00071015523",
            quantity="30",
            days_supply=30,
            last_fill_date=date(2025, 1, 1),
            pharmacy_ncpdp="1234567",
            pharmacy_npi="9876543210",
            pharmacy_name="Test Pharmacy",
            prescriber_npi="1234567890",
        )

        generator = NCPDPScriptGenerator()
        xml = generator.generate_rx_renewal(message)

        assert "<RxRenewalRequest>" in xml
        assert "RX123456" in xml  # Prescription number
        assert "Test Pharmacy" in xml

    def test_generate_cancel_rx(self) -> None:
        """Test CancelRx message generation."""
        generator = NCPDPScriptGenerator()
        xml = generator.generate_cancel_rx(
            message_id="MSG-004",
            relates_to="MSG-001",
            prescriber_npi="1234567890",
            patient_first="Jane",
            patient_last="Doe",
            patient_dob=date(1985, 6, 15),
            drug_description="Lipitor 10mg Tablet",
            cancel_reason="Patient request",
        )

        assert "<CancelRx>" in xml
        assert "MSG-001" in xml  # Relates to
        assert "Patient request" in xml

    def test_parse_message(self, new_rx_message: NewRxMessage) -> None:
        """Test XML message parsing."""
        generator = NCPDPScriptGenerator()
        xml = generator.generate_new_rx(new_rx_message)

        parsed = generator.parse_message(xml)

        assert "Header" in parsed
        assert "Body" in parsed


class TestRejectCodes:
    """Tests for reject codes reference."""

    def test_get_reject_description(self) -> None:
        """Test getting reject description."""
        assert get_reject_description("75") == "Prior Authorization Required"
        assert get_reject_description("80") == "Drug-Drug Interaction"
        assert "Unknown" in get_reject_description("ZZ")

    def test_get_reject_category(self) -> None:
        """Test getting reject category."""
        assert get_reject_category("65") == RejectCategory.ELIGIBILITY
        assert get_reject_category("75") == RejectCategory.COVERAGE
        assert get_reject_category("80") == RejectCategory.DUR
        assert get_reject_category("90") == RejectCategory.QUANTITY

    def test_is_hard_reject(self) -> None:
        """Test hard reject identification."""
        assert is_hard_reject("65") is True  # Patient Not Covered
        assert is_hard_reject("75") is False  # PA Required (can get PA)
        assert is_hard_reject("99") is True  # Host Error

    def test_is_dur_reject(self) -> None:
        """Test DUR reject identification."""
        assert is_dur_reject("80") is True
        assert is_dur_reject("81") is True
        assert is_dur_reject("75") is False


class TestPharmacy:
    """Tests for Pharmacy model."""

    def test_create_pharmacy(self) -> None:
        """Test creating a pharmacy."""
        pharmacy = Pharmacy(
            ncpdp_id="1234567",
            npi="1234567890",
            name="Test Pharmacy",
            address_line1="123 Main St",
            city="Boston",
            state="MA",
            zip_code="02101",
            phone="617-555-1234",
        )

        assert pharmacy.ncpdp_id == "1234567"
        assert pharmacy.pharmacy_type == PharmacyType.RETAIL

    def test_generate_pharmacy(self) -> None:
        """Test pharmacy generator."""
        generator = PharmacyGenerator()
        pharmacy = generator.generate()

        assert len(pharmacy.ncpdp_id) == 7
        assert len(pharmacy.npi) == 10
        assert pharmacy.name

    def test_generate_specialty_pharmacy(self) -> None:
        """Test specialty pharmacy generation."""
        generator = PharmacyGenerator()
        pharmacy = generator.generate_specialty()

        assert pharmacy.pharmacy_type == PharmacyType.SPECIALTY
        assert pharmacy.specialty_certified is True

    def test_generate_mail_order_pharmacy(self) -> None:
        """Test mail order pharmacy generation."""
        generator = PharmacyGenerator()
        pharmacy = generator.generate_mail_order()

        assert pharmacy.pharmacy_type == PharmacyType.MAIL_ORDER


class TestPrescriber:
    """Tests for Prescriber model."""

    def test_create_prescriber(self) -> None:
        """Test creating a prescriber."""
        prescriber = Prescriber(
            npi="1234567890",
            dea="AS1234567",
            first_name="John",
            last_name="Smith",
            credential=PrescriberType.MD,
            specialty=PrescriberSpecialty.CARDIOLOGY,
        )

        assert prescriber.npi == "1234567890"
        assert prescriber.full_name == "John Smith"
        assert prescriber.display_name == "John Smith, MD"

    def test_generate_prescriber(self) -> None:
        """Test prescriber generator."""
        generator = PrescriberGenerator()
        prescriber = generator.generate()

        assert len(prescriber.npi) == 10
        assert prescriber.first_name
        assert prescriber.last_name

    def test_generate_specialist(self) -> None:
        """Test generating specialist."""
        generator = PrescriberGenerator()
        prescriber = generator.generate_specialist(PrescriberSpecialty.ONCOLOGY)

        assert prescriber.specialty == PrescriberSpecialty.ONCOLOGY

    def test_generate_mid_level(self) -> None:
        """Test generating mid-level provider."""
        generator = PrescriberGenerator()
        prescriber = generator.generate_mid_level()

        assert prescriber.credential in [PrescriberType.NP, PrescriberType.PA]

    def test_prescriber_without_dea(self) -> None:
        """Test prescriber without controlled substance authority."""
        generator = PrescriberGenerator()
        prescriber = generator.generate(can_prescribe_controlled=False)

        assert prescriber.dea is None
        assert prescriber.can_prescribe_controlled is False
