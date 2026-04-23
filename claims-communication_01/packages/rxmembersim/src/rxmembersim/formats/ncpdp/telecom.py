"""NCPDP Telecommunication Standard generator."""
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from ...claims.claim import PharmacyClaim
    from ...claims.response import ClaimResponse


class NCPDPSegment(BaseModel):
    """Base NCPDP segment."""

    segment_id: str
    fields: dict[str, str]


class NCPDPTelecomGenerator:
    """Generate NCPDP Telecommunication messages."""

    SEGMENT_SEPARATOR = chr(0x1E)  # ASCII 30
    FIELD_SEPARATOR = chr(0x1C)  # ASCII 28
    GROUP_SEPARATOR = chr(0x1D)  # ASCII 29

    def generate_b1_request(self, claim: "PharmacyClaim") -> str:
        """Generate B1 (billing) request message."""
        segments = []

        # Transaction Header (AM segment)
        segments.append(self._build_header_segment(claim))

        # Patient Segment (01)
        segments.append(self._build_patient_segment(claim))

        # Insurance Segment (04)
        segments.append(self._build_insurance_segment(claim))

        # Claim Segment (07)
        segments.append(self._build_claim_segment(claim))

        # Pricing Segment (11)
        segments.append(self._build_pricing_segment(claim))

        return self.SEGMENT_SEPARATOR.join(segments)

    def generate_b2_reversal(
        self, claim: "PharmacyClaim", original_auth: str
    ) -> str:
        """Generate B2 (reversal) request message."""
        segments = []
        segments.append(self._build_header_segment(claim, transaction_code="B2"))
        segments.append(self._build_patient_segment(claim))
        segments.append(self._build_insurance_segment(claim))
        segments.append(self._build_claim_segment(claim, original_auth=original_auth))
        return self.SEGMENT_SEPARATOR.join(segments)

    def generate_b3_rebill(self, claim: "PharmacyClaim", original_auth: str) -> str:
        """Generate B3 (rebill) request message."""
        segments = []
        segments.append(self._build_header_segment(claim, transaction_code="B3"))
        segments.append(self._build_patient_segment(claim))
        segments.append(self._build_insurance_segment(claim))
        segments.append(self._build_claim_segment(claim, original_auth=original_auth))
        segments.append(self._build_pricing_segment(claim))
        return self.SEGMENT_SEPARATOR.join(segments)

    def generate_response(self, response: "ClaimResponse") -> str:
        """Generate response message."""
        segments = []

        # Response Header (20)
        segments.append(self._build_response_header(response))

        # Response Status (21)
        segments.append(self._build_response_status(response))

        if response.response_status == "P":
            # Response Pricing (23)
            segments.append(self._build_response_pricing(response))

        return self.SEGMENT_SEPARATOR.join(segments)

    def _build_header_segment(
        self, claim: "PharmacyClaim", transaction_code: str = "B1"
    ) -> str:
        """Build transaction header segment."""
        fields = [
            "AM01",
            f"D0{transaction_code}",
            f"C1{claim.bin}",
            f"C2{claim.pcn}",
            f"D1{datetime.now().strftime('%Y%m%d')}",
            f"D2{claim.service_date.strftime('%Y%m%d')}",
        ]
        return self.FIELD_SEPARATOR.join(fields)

    def _build_patient_segment(self, claim: "PharmacyClaim") -> str:
        """Build patient segment (01)."""
        fields = [
            "AM01",
            f"C2{claim.cardholder_id}",
            f"C3{claim.person_code}",
            f"CA{claim.member_id}",
        ]
        return self.FIELD_SEPARATOR.join(fields)

    def _build_insurance_segment(self, claim: "PharmacyClaim") -> str:
        """Build insurance segment (04)."""
        fields = [
            "AM04",
            f"C1{claim.bin}",
            f"C2{claim.pcn}",
            f"C3{claim.group_number}",
            f"CC{claim.cardholder_id}",
        ]
        return self.FIELD_SEPARATOR.join(fields)

    def _build_claim_segment(
        self, claim: "PharmacyClaim", original_auth: str | None = None
    ) -> str:
        """Build claim segment (07)."""
        fields = [
            "AM07",
            f"D2{claim.ndc}",
            f"E1{self._format_quantity(claim.quantity_dispensed)}",
            f"D3{claim.days_supply:03d}",
            f"D6{claim.daw_code}",
            f"D7{claim.prescription_number}",
            f"D8{claim.fill_number:02d}",
            f"DE{claim.compound_code}",
            f"EM{claim.prescriber_npi}",
            f"DB{claim.pharmacy_npi}",
        ]
        if original_auth:
            fields.append(f"F3{original_auth}")
        if claim.prior_auth_number:
            fields.append(f"EU{claim.prior_auth_number}")
        return self.FIELD_SEPARATOR.join(fields)

    def _build_pricing_segment(self, claim: "PharmacyClaim") -> str:
        """Build pricing segment (11)."""
        fields = [
            "AM11",
            f"D9{self._format_currency(claim.ingredient_cost_submitted)}",
            f"DC{self._format_currency(claim.dispensing_fee_submitted)}",
            f"DQ{self._format_currency(claim.gross_amount_due)}",
            f"DU{self._format_currency(claim.usual_customary_charge)}",
        ]
        return self.FIELD_SEPARATOR.join(fields)

    def _build_response_header(self, response: "ClaimResponse") -> str:
        """Build response header segment (20)."""
        fields = [
            "AM20",
            f"AN{response.transaction_response_status}",
            f"F3{response.authorization_number or ''}",
        ]
        return self.FIELD_SEPARATOR.join(fields)

    def _build_response_status(self, response: "ClaimResponse") -> str:
        """Build response status segment (21)."""
        fields = [
            "AM21",
            f"AN{response.response_status}",
        ]
        # Add reject codes if rejected
        for i, reject in enumerate(response.reject_codes[:5], start=1):  # Max 5 rejects
            fields.append(f"F{i}{reject.code}")
        if response.message:
            fields.append(f"FQ{response.message[:200]}")
        return self.FIELD_SEPARATOR.join(fields)

    def _build_response_pricing(self, response: "ClaimResponse") -> str:
        """Build response pricing segment (23)."""
        fields = [
            "AM23",
        ]
        if response.ingredient_cost_paid is not None:
            fields.append(f"F5{self._format_currency(response.ingredient_cost_paid)}")
        if response.dispensing_fee_paid is not None:
            fields.append(f"F6{self._format_currency(response.dispensing_fee_paid)}")
        if response.total_amount_paid is not None:
            fields.append(f"F9{self._format_currency(response.total_amount_paid)}")
        if response.patient_pay_amount is not None:
            fields.append(f"F5{self._format_currency(response.patient_pay_amount)}")
        if response.copay_amount is not None:
            fields.append(f"FE{self._format_currency(response.copay_amount)}")
        if response.deductible_amount is not None:
            fields.append(f"FH{self._format_currency(response.deductible_amount)}")
        return self.FIELD_SEPARATOR.join(fields)

    def _format_currency(self, amount: Decimal) -> str:
        """Format currency as 8-digit integer (cents)."""
        cents = int(amount * 100)
        return f"{cents:08d}"

    def _format_quantity(self, qty: Decimal) -> str:
        """Format quantity as string with 3 decimal places."""
        return f"{qty:.3f}"

    def parse_response(self, message: str) -> dict:
        """Parse NCPDP response message into dictionary."""
        result: dict[str, str | list[str]] = {}
        segments = message.split(self.SEGMENT_SEPARATOR)

        for segment in segments:
            fields = segment.split(self.FIELD_SEPARATOR)
            for field in fields:
                if len(field) >= 2:
                    field_id = field[:2]
                    field_value = field[2:]
                    if field_id in result:
                        # Handle multiple values (e.g., reject codes)
                        existing = result[field_id]
                        if isinstance(existing, list):
                            existing.append(field_value)
                        else:
                            result[field_id] = [existing, field_value]
                    else:
                        result[field_id] = field_value

        return result
