"""Tests for validation."""

from datetime import date, timedelta

from rxmembersim.validation.framework import ValidationResult
from rxmembersim.validation.pharmacy_validator import (
    ClaimValidator,
    MemberEligibilityValidator,
    NDCValidator,
    NPIValidator,
)


class TestNDCValidator:
    """Tests for NDCValidator."""

    def test_valid_ndc(self) -> None:
        """Test valid NDC passes validation."""
        validator = NDCValidator()
        result = validator.validate("00071015523")
        assert result.valid is True

    def test_ndc_with_dashes(self) -> None:
        """Test NDC with dashes is handled."""
        validator = NDCValidator()
        # 5-4-2 format: 00071-0155-23 = 11 digits
        result = validator.validate("00071-0155-23")
        assert result.valid is True

    def test_invalid_length(self) -> None:
        """Test NDC with invalid length fails."""
        validator = NDCValidator()
        result = validator.validate("12345")
        assert result.valid is False
        assert any(i.code == "NDC001" for i in result.issues)

    def test_non_numeric(self) -> None:
        """Test NDC with non-numeric characters fails."""
        validator = NDCValidator()
        result = validator.validate("0007A015523")
        assert result.valid is False

    def test_placeholder_ndc(self) -> None:
        """Test placeholder NDC generates warning."""
        validator = NDCValidator()
        result = validator.validate("00000000000")
        assert result.valid is True  # Valid format
        assert len(result.warnings) == 1
        assert any(i.code == "NDC003" for i in result.issues)


class TestNPIValidator:
    """Tests for NPIValidator."""

    def test_valid_npi(self) -> None:
        """Test valid NPI passes validation."""
        validator = NPIValidator()
        result = validator.validate("1234567890")
        assert result.valid is True

    def test_invalid_length(self) -> None:
        """Test NPI with invalid length fails."""
        validator = NPIValidator()
        result = validator.validate("123456")
        assert result.valid is False

    def test_non_numeric_npi(self) -> None:
        """Test NPI with non-numeric characters fails."""
        validator = NPIValidator()
        result = validator.validate("123456789A")
        assert result.valid is False
        assert any(i.code == "NPI002" for i in result.issues)

    def test_npi_prefix_warning(self) -> None:
        """Test NPI with invalid prefix generates warning."""
        validator = NPIValidator()
        result = validator.validate("9999999999")
        assert result.valid is True
        assert len(result.warnings) == 1
        assert any(i.code == "NPI003" for i in result.issues)


class TestMemberEligibilityValidator:
    """Tests for MemberEligibilityValidator."""

    def test_active_member(self) -> None:
        """Test active member passes validation."""
        from rxmembersim import RxMemberFactory

        validator = MemberEligibilityValidator()
        member = RxMemberFactory().generate()
        result = validator.validate(member)
        assert result.valid is True

    def test_future_effective_date(self) -> None:
        """Test member with future effective date fails."""
        from rxmembersim import RxMemberFactory

        validator = MemberEligibilityValidator()
        member = RxMemberFactory().generate()
        member.effective_date = date.today() + timedelta(days=30)
        result = validator.validate(member)
        assert result.valid is False
        assert any(i.code == "ELIG001" for i in result.issues)

    def test_terminated_member(self) -> None:
        """Test terminated member fails validation."""
        from rxmembersim import RxMemberFactory

        validator = MemberEligibilityValidator()
        member = RxMemberFactory().generate()
        member.termination_date = date.today() - timedelta(days=30)
        result = validator.validate(member)
        assert result.valid is False
        assert any(i.code == "ELIG002" for i in result.issues)


class TestClaimValidator:
    """Tests for ClaimValidator."""

    def test_valid_claim(self) -> None:
        """Test valid claim passes validation."""
        from datetime import date
        from decimal import Decimal

        from rxmembersim.claims.claim import PharmacyClaim, TransactionCode

        validator = ClaimValidator()
        claim = PharmacyClaim(
            claim_id="CLM001",
            transaction_code=TransactionCode.BILLING,
            service_date=date.today(),
            pharmacy_npi="1234567890",
            member_id="MEM001",
            cardholder_id="CH001",
            person_code="01",
            bin="610014",
            pcn="RXTEST",
            group_number="GRP001",
            prescription_number="RX123456",
            fill_number=0,
            ndc="00071015523",
            quantity_dispensed=Decimal("30"),
            days_supply=30,
            daw_code="0",
            prescriber_npi="1234567890",
            ingredient_cost_submitted=Decimal("100.00"),
            dispensing_fee_submitted=Decimal("2.00"),
            patient_paid_submitted=Decimal("10.00"),
            usual_customary_charge=Decimal("120.00"),
            gross_amount_due=Decimal("112.00"),
        )
        result = validator.validate(claim)
        assert result.valid is True


class TestValidationResult:
    """Tests for ValidationResult."""

    def test_add_error(self) -> None:
        """Test adding error invalidates result."""
        result = ValidationResult()
        result.add_error("field1", "Error message")
        assert result.valid is False
        assert len(result.errors) == 1

    def test_add_warning(self) -> None:
        """Test adding warning doesn't invalidate result."""
        result = ValidationResult()
        result.add_warning("field1", "Warning message")
        assert result.valid is True  # Warnings don't invalidate
        assert len(result.warnings) == 1

    def test_add_info(self) -> None:
        """Test adding info doesn't invalidate result."""
        result = ValidationResult()
        result.add_info("field1", "Info message")
        assert result.valid is True
        assert len(result.issues) == 1

    def test_multiple_issues(self) -> None:
        """Test result with multiple issues."""
        result = ValidationResult()
        result.add_error("field1", "Error 1")
        result.add_warning("field2", "Warning 1")
        result.add_info("field3", "Info 1")
        assert result.valid is False
        assert len(result.issues) == 3
        assert len(result.errors) == 1
        assert len(result.warnings) == 1
