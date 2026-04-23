"""X12 837 Healthcare Claim generators."""

from datetime import date

from membersim.claims.claim import Claim
from membersim.formats.x12.base import X12Config, X12Generator


class EDI837PGenerator(X12Generator):
    """Generate X12 837P Professional Claims."""

    def generate(self, claims: list[Claim]) -> str:
        """Generate 837P for professional claims."""
        self.reset()

        # Envelope
        self._isa_segment("HC")
        self._gs_segment("HC", self.config.sender_id, self.config.receiver_id)
        self._st_segment("837")

        # BHT - Beginning of Hierarchical Transaction
        today = date.today()
        self._add(
            "BHT",
            "0019",
            "00",
            f"CLM{today.strftime('%Y%m%d%H%M%S')}",
            today.strftime("%Y%m%d"),
            today.strftime("%H%M"),
            "CH",  # Claim
        )

        # NM1 - Submitter
        self._add("NM1", "41", "2", "SUBMITTER NAME", "", "", "", "", "46", "SUBMITTERID")
        self._add("PER", "IC", "CONTACT NAME", "TE", "5551234567")

        # NM1 - Receiver
        self._add("NM1", "40", "2", "RECEIVER NAME", "", "", "", "", "46", "RECEIVERID")

        # Process each claim
        for idx, claim in enumerate(claims, 1):
            self._generate_claim_loop(claim, idx)

        # Trailers
        self._se_segment()
        self._ge_segment()
        self._iea_segment()

        return self.to_string()

    def _generate_claim_loop(self, claim: Claim, hl_id: int) -> None:
        """Generate 2000A/B/C loops for a claim."""

        # HL - Billing Provider Level
        self._add("HL", str(hl_id), "", "20", "1")

        # NM1 - Billing Provider
        self._add("NM1", "85", "2", "BILLING PROVIDER", "", "", "", "", "XX", claim.provider_npi)

        # HL - Subscriber Level
        self._add("HL", str(hl_id + 100), str(hl_id), "22", "0")

        # NM1 - Subscriber
        self._add("NM1", "IL", "1", "LASTNAME", "FIRSTNAME", "", "", "", "MI", claim.subscriber_id)

        # CLM - Claim Information
        self._add(
            "CLM",
            claim.claim_id,
            str(claim.total_charge),
            "",
            "",
            f"{claim.place_of_service}:B:1",  # Place of Service
            "Y",  # Provider Signature
            "A",  # Assignment
            "Y",  # Benefits Assignment
            "I",  # Release of Information
        )

        # DTP - Service Dates
        self._add("DTP", "472", "D8", claim.service_date.strftime("%Y%m%d"))

        # HI - Diagnosis Codes
        dx_codes = [f"ABK:{claim.principal_diagnosis}"]
        for dx in claim.other_diagnoses[:11]:
            dx_codes.append(f"ABF:{dx}")
        self._add("HI", *dx_codes[:12])

        # NM1 - Rendering Provider
        self._add("NM1", "82", "1", "PROVIDER", "RENDERING", "", "", "", "XX", claim.provider_npi)

        # LX/SV1 - Service Lines
        for line in claim.claim_lines:
            self._add("LX", str(line.line_number))

            # SV1 - Professional Service
            proc = f"HC:{line.procedure_code}"
            if line.procedure_modifiers:
                proc += ":" + ":".join(line.procedure_modifiers)

            self._add(
                "SV1",
                proc,
                str(line.charge_amount),
                "UN",
                str(line.units),
                "",
                "",
                ":".join(str(p) for p in line.diagnosis_pointers),
            )

            self._add("DTP", "472", "D8", line.service_date.strftime("%Y%m%d"))


class EDI837IGenerator(X12Generator):
    """Generate X12 837I Institutional Claims."""

    def generate(self, claims: list[Claim]) -> str:
        """Generate 837I for institutional claims."""
        self.reset()

        # Similar structure to 837P but with institutional segments
        # SV2 instead of SV1, revenue codes, etc.

        self._isa_segment("HC")
        self._gs_segment("HC", self.config.sender_id, self.config.receiver_id)
        self._st_segment("837")

        # BHT
        today = date.today()
        self._add(
            "BHT",
            "0019",
            "00",
            f"CLM{today.strftime('%Y%m%d%H%M%S')}",
            today.strftime("%Y%m%d"),
            today.strftime("%H%M"),
            "CH",
        )

        # NM1 - Submitter
        self._add("NM1", "41", "2", "SUBMITTER NAME", "", "", "", "", "46", "SUBMITTERID")
        self._add("PER", "IC", "CONTACT NAME", "TE", "5551234567")

        # NM1 - Receiver
        self._add("NM1", "40", "2", "RECEIVER NAME", "", "", "", "", "46", "RECEIVERID")

        for idx, claim in enumerate(claims, 1):
            self._generate_institutional_claim(claim, idx)

        self._se_segment()
        self._ge_segment()
        self._iea_segment()

        return self.to_string()

    def _generate_institutional_claim(self, claim: Claim, hl_id: int) -> None:
        """Generate institutional claim loops."""
        # HL levels
        self._add("HL", str(hl_id), "", "20", "1")
        self._add(
            "NM1",
            "85",
            "2",
            "FACILITY NAME",
            "",
            "",
            "",
            "",
            "XX",
            claim.facility_npi or claim.provider_npi,
        )

        self._add("HL", str(hl_id + 100), str(hl_id), "22", "0")
        self._add("NM1", "IL", "1", "LASTNAME", "FIRSTNAME", "", "", "", "MI", claim.subscriber_id)

        # CLM with institutional-specific elements
        type_of_bill = "0111"  # Hospital Inpatient
        self._add(
            "CLM",
            claim.claim_id,
            str(claim.total_charge),
            "",
            "",
            f"{type_of_bill}::1",
            "Y",
            "A",
            "Y",
            "I",
        )

        # DTP - Statement Dates
        if claim.admission_date:
            self._add("DTP", "435", "D8", claim.admission_date.strftime("%Y%m%d"))
        if claim.discharge_date:
            self._add("DTP", "096", "D8", claim.discharge_date.strftime("%Y%m%d"))

        # HI - Diagnosis
        self._add("HI", f"BK:{claim.principal_diagnosis}")

        # LX/SV2 - Service Lines
        for line in claim.claim_lines:
            self._add("LX", str(line.line_number))
            self._add(
                "SV2",
                line.revenue_code or "0120",
                f"HC:{line.procedure_code}",
                str(line.charge_amount),
                "UN",
                str(line.units),
            )
            self._add("DTP", "472", "D8", line.service_date.strftime("%Y%m%d"))


def generate_837p(claims: list[Claim], config: X12Config | None = None) -> str:
    """Convenience function for 837P generation."""
    return EDI837PGenerator(config).generate(claims)


def generate_837i(claims: list[Claim], config: X12Config | None = None) -> str:
    """Convenience function for 837I generation."""
    return EDI837IGenerator(config).generate(claims)
