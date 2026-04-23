"""X12 834 Benefit Enrollment generator."""

from datetime import date

from membersim.core.member import Member
from membersim.formats.x12.base import X12Config, X12Generator


class EDI834Generator(X12Generator):
    """Generate X12 834 Benefit Enrollment transactions."""

    def __init__(self, config: X12Config | None = None):
        super().__init__(config)

    def generate(
        self,
        members: list[Member],
        maintenance_type: str = "021",  # 021=Addition
        group_id: str | None = None,
    ) -> str:
        """
        Generate 834 enrollment transaction.

        Args:
            members: List of members to include
            maintenance_type: 021=Addition, 001=Change, 024=Termination
            group_id: Override group ID (uses member's group_id if not specified)

        Returns:
            X12 834 transaction string
        """
        self.reset()

        # Envelope
        self._isa_segment("BE")
        self._gs_segment("BE", self.config.sender_id, self.config.receiver_id)
        self._st_segment("834")

        # BGN - Beginning Segment
        today_str = date.today().strftime("%Y%m%d")
        self._add("BGN", "00", f"REF{today_str}", today_str)

        # N1 Loop - Sponsor/Payer
        self._add("N1", "P5", "SPONSOR NAME", "FI", "123456789")
        self._add("N1", "IN", "PAYER NAME", "FI", "987654321")

        # Process each member
        for member in members:
            self._generate_member_loop(member, maintenance_type, group_id)

        # Trailers
        self._se_segment()
        self._ge_segment()
        self._iea_segment()

        return self.to_string()

    def _generate_member_loop(
        self,
        member: Member,
        maintenance_type: str,
        group_id: str | None,
    ) -> None:
        """Generate INS loop for a single member."""
        gid = group_id or member.group_id

        # INS - Member Level Detail
        is_subscriber = "Y" if member.is_subscriber else "N"
        self._add(
            "INS",
            is_subscriber,
            member.relationship_code,
            maintenance_type,
            "",  # Maintenance Reason Code
            "A",  # Benefit Status Code (A=Active)
        )

        # REF - Member Identifiers
        self._add("REF", "0F", member.member_id)  # Subscriber Number
        if member.subscriber_id and not member.is_subscriber:
            self._add("REF", "23", member.subscriber_id)  # Group Policy Number
        self._add("REF", "1L", gid)  # Group Number

        # DTP - Coverage Dates
        self._add("DTP", "356", "D8", member.coverage_start.strftime("%Y%m%d"))
        if member.coverage_end:
            self._add("DTP", "357", "D8", member.coverage_end.strftime("%Y%m%d"))

        # NM1 - Member Name
        self._add(
            "NM1",
            "IL",  # Insured
            "1",  # Person
            member.name.family_name,
            member.name.given_name,
            "",  # Middle name
            "",  # Prefix
            "",  # Suffix
            "MI",  # Member ID Qualifier
            member.member_id,
        )

        # DMG - Demographics
        gender_code = member.gender.value if hasattr(member.gender, "value") else str(member.gender)
        # Map gender to X12 codes
        if gender_code.upper() in ("MALE", "M"):
            gender_code = "M"
        elif gender_code.upper() in ("FEMALE", "F"):
            gender_code = "F"
        else:
            gender_code = "U"

        self._add(
            "DMG",
            "D8",
            member.birth_date.strftime("%Y%m%d"),
            gender_code,
        )

        # N3/N4 - Address
        if member.address:
            self._add("N3", member.address.street_address)
            self._add(
                "N4",
                member.address.city,
                member.address.state,
                member.address.postal_code,
            )

        # HD - Health Coverage
        self._add(
            "HD",
            "021" if maintenance_type == "021" else "001",
            "",
            "HLT",  # Health
            member.plan_code,
        )

        # DTP - Coverage dates in HD loop
        self._add("DTP", "348", "D8", member.coverage_start.strftime("%Y%m%d"))


def generate_834(
    members: list[Member],
    maintenance_type: str = "021",
    config: X12Config | None = None,
) -> str:
    """Convenience function to generate 834."""
    generator = EDI834Generator(config)
    return generator.generate(members, maintenance_type)
