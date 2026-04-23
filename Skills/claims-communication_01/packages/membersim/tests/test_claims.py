"""Tests for Claim and Payment models."""

from datetime import date
from decimal import Decimal

from membersim import Claim, ClaimLine, Payment
from membersim.claims.payment import LinePayment


def test_claim_total_charge(sample_claim: Claim) -> None:
    """Test claim total charge calculation."""
    assert sample_claim.total_charge == Decimal("150.00")
    assert sample_claim.line_count == 1


def test_claim_all_diagnoses(sample_claim: Claim) -> None:
    """Test diagnosis list."""
    assert "E11.9" in sample_claim.all_diagnoses
    assert len(sample_claim.all_diagnoses) == 1


def test_claim_multiple_lines() -> None:
    """Test claim with multiple service lines."""
    claim = Claim(
        claim_id="CLM002",
        claim_type="PROFESSIONAL",
        member_id="MEM001",
        subscriber_id="MEM001",
        provider_npi="1234567890",
        service_date=date(2024, 3, 15),
        place_of_service="11",
        principal_diagnosis="J06.9",
        other_diagnoses=["R05.9"],
        claim_lines=[
            ClaimLine(
                line_number=1,
                procedure_code="99213",
                service_date=date(2024, 3, 15),
                charge_amount=Decimal("150.00"),
            ),
            ClaimLine(
                line_number=2,
                procedure_code="87880",  # Strep test
                service_date=date(2024, 3, 15),
                charge_amount=Decimal("45.00"),
            ),
        ],
    )

    assert claim.total_charge == Decimal("195.00")
    assert claim.line_count == 2
    assert len(claim.all_diagnoses) == 2


def test_payment_calculations() -> None:
    """Test payment amount calculations."""
    payment = Payment(
        payment_id="PAY001",
        claim_id="CLM001",
        payment_date=date(2024, 4, 1),
        check_number="CHK12345",
        line_payments=[
            LinePayment(
                line_number=1,
                charged_amount=Decimal("150.00"),
                allowed_amount=Decimal("100.00"),
                paid_amount=Decimal("75.00"),
                deductible_amount=Decimal("25.00"),
            ),
        ],
    )

    assert payment.total_charged == Decimal("150.00")
    assert payment.total_allowed == Decimal("100.00")
    assert payment.total_paid == Decimal("75.00")
    assert payment.total_patient_responsibility == Decimal("25.00")


def test_line_payment_calculations() -> None:
    """Test individual line payment calculations."""
    line_payment = LinePayment(
        line_number=1,
        charged_amount=Decimal("200.00"),
        allowed_amount=Decimal("150.00"),
        paid_amount=Decimal("100.00"),
        deductible_amount=Decimal("25.00"),
        copay_amount=Decimal("25.00"),
        coinsurance_amount=Decimal("0.00"),
    )

    assert line_payment.patient_responsibility == Decimal("50.00")
    assert line_payment.adjustment_amount == Decimal("50.00")


def test_payment_multiple_lines() -> None:
    """Test payment with multiple line payments."""
    payment = Payment(
        payment_id="PAY002",
        claim_id="CLM002",
        payment_date=date(2024, 4, 1),
        check_number="CHK12346",
        line_payments=[
            LinePayment(
                line_number=1,
                charged_amount=Decimal("150.00"),
                allowed_amount=Decimal("100.00"),
                paid_amount=Decimal("80.00"),
                coinsurance_amount=Decimal("20.00"),
            ),
            LinePayment(
                line_number=2,
                charged_amount=Decimal("45.00"),
                allowed_amount=Decimal("35.00"),
                paid_amount=Decimal("28.00"),
                coinsurance_amount=Decimal("7.00"),
            ),
        ],
    )

    assert payment.total_charged == Decimal("195.00")
    assert payment.total_allowed == Decimal("135.00")
    assert payment.total_paid == Decimal("108.00")
    assert payment.total_patient_responsibility == Decimal("27.00")
