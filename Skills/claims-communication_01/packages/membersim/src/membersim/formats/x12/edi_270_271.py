"""X12 270/271 Eligibility Inquiry and Response generators."""

from datetime import date

from membersim.core.accumulator import Accumulator
from membersim.core.member import Member
from membersim.core.plan import Plan
from membersim.formats.x12.base import X12Config, X12Generator


class EDI270Generator(X12Generator):
    """Generate X12 270 Eligibility Inquiry."""

    def generate(
        self,
        member: Member,
        service_date: date | None = None,
        service_type: str = "30",  # Health Benefit Plan Coverage
    ) -> str:
        """Generate 270 eligibility inquiry."""
        self.reset()
        svc_date = service_date or date.today()

        self._isa_segment("HS")
        self._gs_segment("HS", self.config.sender_id, self.config.receiver_id)
        self._st_segment("270")

        # BHT - Beginning of Hierarchical Transaction
        self._add(
            "BHT",
            "0022",
            "13",
            f"INQ{svc_date.strftime('%Y%m%d%H%M%S')}",
            svc_date.strftime("%Y%m%d"),
            svc_date.strftime("%H%M"),
        )

        # HL - Information Source Level
        self._add("HL", "1", "", "20", "1")
        self._add("NM1", "PR", "2", "PAYER NAME", "", "", "", "", "PI", "PAYERID")

        # HL - Information Receiver Level
        self._add("HL", "2", "1", "21", "1")
        self._add("NM1", "1P", "2", "PROVIDER NAME", "", "", "", "", "XX", "1234567890")

        # HL - Subscriber Level
        self._add("HL", "3", "2", "22", "0")

        # NM1 - Subscriber
        self._add(
            "NM1",
            "IL",
            "1",
            member.name.family_name,
            member.name.given_name,
            "",
            "",
            "",
            "MI",
            member.member_id,
        )

        # DMG - Demographics
        gender_code = member.gender.value if hasattr(member.gender, "value") else str(member.gender)
        if gender_code.upper() in ("MALE", "M"):
            gender_code = "M"
        elif gender_code.upper() in ("FEMALE", "F"):
            gender_code = "F"
        else:
            gender_code = "U"

        self._add("DMG", "D8", member.birth_date.strftime("%Y%m%d"), gender_code)

        # DTP - Service Date
        self._add("DTP", "291", "D8", svc_date.strftime("%Y%m%d"))

        # EQ - Eligibility Inquiry
        self._add("EQ", service_type)

        self._se_segment()
        self._ge_segment()
        self._iea_segment()

        return self.to_string()


class EDI271Generator(X12Generator):
    """Generate X12 271 Eligibility Response."""

    def generate(
        self,
        member: Member,
        plan: Plan,
        accumulator: Accumulator | None = None,
        is_eligible: bool = True,
    ) -> str:
        """Generate 271 eligibility response."""
        self.reset()
        today = date.today()

        self._isa_segment("HB")
        self._gs_segment("HB", self.config.sender_id, self.config.receiver_id)
        self._st_segment("271")

        # BHT
        self._add(
            "BHT",
            "0022",
            "11",
            f"RSP{today.strftime('%Y%m%d%H%M%S')}",
            today.strftime("%Y%m%d"),
            today.strftime("%H%M"),
        )

        # HL Levels (similar to 270)
        self._add("HL", "1", "", "20", "1")
        self._add("NM1", "PR", "2", "PAYER NAME", "", "", "", "", "PI", "PAYERID")

        self._add("HL", "2", "1", "21", "1")
        self._add("NM1", "1P", "2", "PROVIDER NAME", "", "", "", "", "XX", "1234567890")

        self._add("HL", "3", "2", "22", "0")

        # Subscriber Info
        self._add(
            "NM1",
            "IL",
            "1",
            member.name.family_name,
            member.name.given_name,
            "",
            "",
            "",
            "MI",
            member.member_id,
        )

        gender_code = member.gender.value if hasattr(member.gender, "value") else str(member.gender)
        if gender_code.upper() in ("MALE", "M"):
            gender_code = "M"
        elif gender_code.upper() in ("FEMALE", "F"):
            gender_code = "F"
        else:
            gender_code = "U"

        self._add("DMG", "D8", member.birth_date.strftime("%Y%m%d"), gender_code)

        # DTP - Plan Dates
        self._add("DTP", "346", "D8", member.coverage_start.strftime("%Y%m%d"))

        # EB - Eligibility/Benefit Information
        if is_eligible and member.is_active:
            # Active Coverage
            self._add("EB", "1", "IND", "30", plan.plan_type, plan.plan_name)

            # Deductible Info
            self._add("EB", "C", "IND", "30", "DED", str(plan.deductible_individual), "23")
            if accumulator:
                remaining = accumulator.deductible_remaining
                self._add("EB", "C", "IND", "30", "DED", str(remaining), "29")  # Remaining

            # OOP Max
            self._add("EB", "G", "IND", "30", "", str(plan.oop_max_individual), "23")

            # Copays
            self._add("EB", "B", "IND", "98", "", str(plan.copay_pcp))  # PCP
            self._add("EB", "B", "IND", "99", "", str(plan.copay_specialist))  # Specialist

            # Coinsurance
            pct = int(plan.coinsurance * 100)
            self._add("EB", "A", "IND", "30", "", "", "", "", "", "", str(pct))
        else:
            # Inactive/Ineligible
            self._add("EB", "6", "IND", "30")  # Inactive

        self._se_segment()
        self._ge_segment()
        self._iea_segment()

        return self.to_string()


def generate_270(
    member: Member,
    service_date: date | None = None,
    config: X12Config | None = None,
) -> str:
    """Generate 270 eligibility inquiry."""
    return EDI270Generator(config).generate(member, service_date)


def generate_271(
    member: Member,
    plan: Plan,
    accumulator: Accumulator | None = None,
    is_eligible: bool = True,
    config: X12Config | None = None,
) -> str:
    """Generate 271 eligibility response."""
    return EDI271Generator(config).generate(member, plan, accumulator, is_eligible)
