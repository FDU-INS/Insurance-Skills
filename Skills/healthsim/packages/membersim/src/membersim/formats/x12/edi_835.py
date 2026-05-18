"""X12 835 Healthcare Claim Payment/Remittance generator."""

from datetime import date
from decimal import Decimal

from membersim.claims.payment import Payment
from membersim.formats.x12.base import X12Config, X12Generator


class EDI835Generator(X12Generator):
    """Generate X12 835 Remittance Advice."""

    def generate(self, payments: list[Payment]) -> str:
        """Generate 835 remittance for payments."""
        self.reset()

        self._isa_segment("HP")
        self._gs_segment("HP", self.config.sender_id, self.config.receiver_id)
        self._st_segment("835")

        # BPR - Financial Information
        total_amount = sum(p.total_paid for p in payments)
        today = date.today()
        self._add(
            "BPR",
            "I",  # Information Only (or "C" for actual payment)
            str(total_amount),
            "C",  # Credit
            "ACH",
            "CTX",
            "01",
            "ROUTING",
            "DA",
            "ACCOUNT",
            "PAYERID",
            "",
            "01",
            "PAYEEROUTING",
            "DA",
            "PAYEEACCOUNT",
            today.strftime("%Y%m%d"),
        )

        # TRN - Reassociation Trace Number
        check_num = payments[0].check_number if payments else "000"
        self._add("TRN", "1", check_num, "PAYERID")

        # REF - Receiver Identification
        self._add("REF", "EV", "RECEIVERID")

        # DTM - Production Date
        self._add("DTM", "405", today.strftime("%Y%m%d"))

        # N1 - Payer Identification
        self._add("N1", "PR", "PAYER NAME", "XV", "PAYERID")

        # N1 - Payee Identification
        self._add("N1", "PE", "PAYEE NAME", "XX", "PAYEENPI")

        # Process each payment
        for payment in payments:
            self._generate_payment_loop(payment)

        self._se_segment()
        self._ge_segment()
        self._iea_segment()

        return self.to_string()

    def _generate_payment_loop(self, payment: Payment) -> None:
        """Generate CLP loop for a payment."""

        # CLP - Claim Payment Information
        self._add(
            "CLP",
            payment.claim_id,
            "1",  # Claim Status: Processed as Primary
            str(payment.total_charged),
            str(payment.total_paid),
            str(payment.total_patient_responsibility),
            "12",  # Claim Filing Indicator
            payment.payment_id,
        )

        # DTM - Statement Dates
        self._add("DTM", "232", payment.payment_date.strftime("%Y%m%d"))

        # Generate SVC loops for each line
        for line_pay in payment.line_payments:
            # SVC - Service Payment Information
            self._add(
                "SVC",
                "HC:99213",  # Would need actual procedure code
                str(line_pay.charged_amount),
                str(line_pay.paid_amount),
                "",
                str(line_pay.line_number),
            )

            # DTM - Service Date
            self._add("DTM", "472", payment.payment_date.strftime("%Y%m%d"))

            # CAS - Claim Adjustment
            if line_pay.deductible_amount > Decimal("0"):
                self._add("CAS", "PR", "1", str(line_pay.deductible_amount))
            if line_pay.coinsurance_amount > Decimal("0"):
                self._add("CAS", "PR", "2", str(line_pay.coinsurance_amount))
            if line_pay.copay_amount > Decimal("0"):
                self._add("CAS", "PR", "3", str(line_pay.copay_amount))
            if line_pay.adjustment_amount > Decimal("0"):
                self._add("CAS", "CO", "45", str(line_pay.adjustment_amount))

            # AMT - Amounts
            self._add("AMT", "B6", str(line_pay.allowed_amount))


def generate_835(payments: list[Payment], config: X12Config | None = None) -> str:
    """Convenience function for 835 generation."""
    return EDI835Generator(config).generate(payments)
