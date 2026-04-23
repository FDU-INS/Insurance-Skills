"""Claim payment and remittance model."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class LinePayment(BaseModel):
    """Payment details for a single claim line."""

    line_number: int = Field(..., description="Reference to claim line")
    charged_amount: Decimal = Field(..., description="Original billed amount")
    allowed_amount: Decimal = Field(..., description="Contracted/allowed amount")
    paid_amount: Decimal = Field(..., description="Amount paid by plan")

    # Member cost sharing
    deductible_amount: Decimal = Field(Decimal("0"), description="Applied to deductible")
    copay_amount: Decimal = Field(Decimal("0"), description="Copay amount")
    coinsurance_amount: Decimal = Field(Decimal("0"), description="Coinsurance amount")

    # Adjustment codes
    adjustment_reason: str = Field("", description="CARC code")
    remark_codes: list[str] = Field(default_factory=list, description="RARC codes")

    @property
    def patient_responsibility(self) -> Decimal:
        """Calculate total member cost share."""
        return self.deductible_amount + self.copay_amount + self.coinsurance_amount

    @property
    def adjustment_amount(self) -> Decimal:
        """Calculate write-off/adjustment."""
        return self.charged_amount - self.allowed_amount


class Payment(BaseModel):
    """Complete claim payment/remittance."""

    payment_id: str = Field(..., description="Unique payment identifier")
    claim_id: str = Field(..., description="Reference to original claim")
    payment_date: date = Field(..., description="Date of payment")
    check_number: str = Field(..., description="Check/EFT reference number")

    line_payments: list[LinePayment] = Field(default_factory=list)

    @property
    def total_charged(self) -> Decimal:
        """Total charged amount across all lines."""
        return sum(lp.charged_amount for lp in self.line_payments)

    @property
    def total_allowed(self) -> Decimal:
        """Total allowed amount across all lines."""
        return sum(lp.allowed_amount for lp in self.line_payments)

    @property
    def total_paid(self) -> Decimal:
        """Total paid by plan."""
        return sum(lp.paid_amount for lp in self.line_payments)

    @property
    def total_patient_responsibility(self) -> Decimal:
        """Total member cost share."""
        return sum(lp.patient_responsibility for lp in self.line_payments)


# Common CARC codes
CARC_CODES = {
    "1": "Deductible amount",
    "2": "Coinsurance amount",
    "3": "Copay amount",
    "4": "The procedure code is inconsistent with the modifier used",
    "45": "Charge exceeds fee schedule/maximum allowable",
    "50": "These are non-covered services",
    "96": "Non-covered charge(s)",
    "97": "The benefit for this service is included in the payment/allowance for another",
}
