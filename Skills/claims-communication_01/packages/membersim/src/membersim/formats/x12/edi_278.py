"""X12 278 Healthcare Services Review - Prior Authorization."""

from datetime import date

from membersim.authorization.prior_auth import Authorization
from membersim.formats.x12.base import X12Config, X12Generator


class EDI278RequestGenerator(X12Generator):
    """Generate X12 278 Prior Authorization Request."""

    def generate(self, auth: Authorization) -> str:
        """Generate 278 request transaction."""
        self.reset()

        self._isa_segment("HS")
        self._gs_segment("HI", self.config.sender_id, self.config.receiver_id)
        self._st_segment("278")

        # BHT - Beginning of Hierarchical Transaction
        self._add(
            "BHT",
            "0007",  # Structure Code
            "13",  # Original (13=Request)
            auth.auth_number,
            auth.request_date.strftime("%Y%m%d"),
            "0000",  # Time placeholder
        )

        # HL - Utilization Management Organization
        self._add("HL", "1", "", "20", "1")
        self._add("NM1", "X3", "2", "UM ORG NAME", "", "", "", "", "PI", "UMORGID")

        # HL - Requester (Provider)
        self._add("HL", "2", "1", "21", "1")
        self._add("NM1", "1P", "1", "PROVIDER", "REQUESTING", "", "", "", "XX", auth.provider_npi)

        # HL - Subscriber
        self._add("HL", "3", "2", "22", "1")
        self._add("NM1", "IL", "1", "MEMBERLAST", "MEMBERFIRST", "", "", "", "MI", auth.member_id)

        # TRN - Trace Number
        self._add("TRN", "1", auth.auth_number, "REQUESTERID")

        # UM - Health Care Services Review
        urgency_code = "S" if auth.urgency == "STANDARD" else "U"
        review_code = "HS" if auth.review_type == "PROSPECTIVE" else "IN"
        cert_type = "I" if auth.service_type == "INPATIENT" else "O"
        self._add("UM", review_code, cert_type, urgency_code)

        # DTP - Service Dates
        if auth.effective_start:
            self._add("DTP", "472", "D8", auth.effective_start.strftime("%Y%m%d"))

        # HI - Diagnosis Information
        if auth.diagnosis_codes:
            dx_elements = [f"ABK:{auth.diagnosis_codes[0]}"]
            for dx in auth.diagnosis_codes[1:4]:
                dx_elements.append(f"ABF:{dx}")
            self._add("HI", *dx_elements)

        # SV1/SV2 - Service Information
        for proc in auth.procedure_codes:
            self._add("SV1", f"HC:{proc}", "", "UN", "1")

        self._se_segment()
        self._ge_segment()
        self._iea_segment()

        return self.to_string()


class EDI278ResponseGenerator(X12Generator):
    """Generate X12 278 Prior Authorization Response."""

    def generate(self, auth: Authorization) -> str:
        """Generate 278 response transaction."""
        self.reset()

        self._isa_segment("HB")
        self._gs_segment("HI", self.config.sender_id, self.config.receiver_id)
        self._st_segment("278")

        # BHT
        decision_date = auth.decision_date or date.today()
        self._add(
            "BHT",
            "0007",
            "11",  # Response
            auth.auth_number,
            decision_date.strftime("%Y%m%d"),
        )

        # HL Levels (similar structure)
        self._add("HL", "1", "", "20", "1")
        self._add("NM1", "X3", "2", "UM ORG NAME", "", "", "", "", "PI", "UMORGID")

        self._add("HL", "2", "1", "21", "1")
        self._add("NM1", "1P", "1", "PROVIDER", "", "", "", "", "XX", auth.provider_npi)

        self._add("HL", "3", "2", "22", "0")
        self._add("NM1", "IL", "1", "MEMBERLAST", "MEMBERFIRST", "", "", "", "MI", auth.member_id)

        # TRN
        self._add("TRN", "1", auth.auth_number, "UMORGID")

        # AAA - Request Validation
        if auth.status == "APPROVED":
            action_code = "A1"  # Certified in Total
        elif auth.status == "MODIFIED":
            action_code = "A2"  # Certified Partial
        elif auth.status == "DENIED":
            action_code = "A3"  # Not Certified
        else:
            action_code = "A4"  # Pended

        self._add("AAA", "Y", "", action_code)

        # UM - Certification Info
        cert_type = "I" if auth.service_type == "INPATIENT" else "O"
        self._add("UM", "HS", cert_type, "", action_code)

        # DTP - Certified Dates
        if auth.effective_start and auth.status in ["APPROVED", "MODIFIED"]:
            end_date = auth.effective_end or auth.effective_start
            date_range = f"{auth.effective_start.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"
            self._add("DTP", "472", "RD8", date_range)

        # HSD - Health Care Services Delivery (approved units)
        if auth.approved_units and auth.status in ["APPROVED", "MODIFIED"]:
            self._add("HSD", "VS", str(auth.approved_units))

        self._se_segment()
        self._ge_segment()
        self._iea_segment()

        return self.to_string()


def generate_278_request(auth: Authorization, config: X12Config | None = None) -> str:
    """Generate 278 authorization request."""
    return EDI278RequestGenerator(config).generate(auth)


def generate_278_response(auth: Authorization, config: X12Config | None = None) -> str:
    """Generate 278 authorization response."""
    return EDI278ResponseGenerator(config).generate(auth)
