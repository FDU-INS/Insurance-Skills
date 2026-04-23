"""Base classes for X12 EDI generation."""

from datetime import datetime

from pydantic import BaseModel, Field


class X12Config(BaseModel):
    """Configuration for X12 transaction generation."""

    sender_id: str = Field("MEMBERSIM", description="ISA06 Interchange Sender ID")
    sender_qualifier: str = Field("ZZ", description="ISA05 Sender ID Qualifier")
    receiver_id: str = Field("RECEIVER", description="ISA08 Interchange Receiver ID")
    receiver_qualifier: str = Field("ZZ", description="ISA07 Receiver ID Qualifier")

    # Control numbers (auto-increment in real system)
    isa_control_number: int = Field(1, description="ISA13 Interchange Control Number")
    gs_control_number: int = Field(1, description="GS06 Group Control Number")
    st_control_number: int = Field(1, description="ST02 Transaction Set Control Number")


class X12Generator:
    """Base class for X12 transaction generators."""

    ELEMENT_SEPARATOR = "*"
    SEGMENT_TERMINATOR = "~"

    def __init__(self, config: X12Config | None = None):
        self.config = config or X12Config()
        self._segments: list[str] = []

    def _segment(self, *elements) -> str:
        """Create a segment from elements."""
        # Filter None values and convert to string
        parts = [str(e) if e is not None else "" for e in elements]
        return self.ELEMENT_SEPARATOR.join(parts) + self.SEGMENT_TERMINATOR

    def _add(self, *elements) -> None:
        """Add a segment to the transaction."""
        self._segments.append(self._segment(*elements))

    def _isa_segment(self, _functional_group_id: str) -> None:
        """Generate ISA Interchange Control Header."""
        now = datetime.now()
        self._add(
            "ISA",
            "00",
            " " * 10,  # Authorization
            "00",
            " " * 10,  # Security
            self.config.sender_qualifier.ljust(2),
            self.config.sender_id.ljust(15),
            self.config.receiver_qualifier.ljust(2),
            self.config.receiver_id.ljust(15),
            now.strftime("%y%m%d"),  # Date
            now.strftime("%H%M"),  # Time
            "^",  # Repetition Separator
            "00501",  # Version
            str(self.config.isa_control_number).zfill(9),
            "0",  # Acknowledgment Requested
            "P",  # Usage Indicator (P=Production)
            ":",  # Component Separator
        )

    def _gs_segment(self, functional_id: str, sender: str, receiver: str) -> None:
        """Generate GS Functional Group Header."""
        now = datetime.now()
        self._add(
            "GS",
            functional_id,
            sender,
            receiver,
            now.strftime("%Y%m%d"),
            now.strftime("%H%M"),
            str(self.config.gs_control_number),
            "X",
            "005010X220A1",
        )

    def _st_segment(self, transaction_code: str) -> None:
        """Generate ST Transaction Set Header."""
        self._add(
            "ST",
            transaction_code,
            str(self.config.st_control_number).zfill(4),
        )

    def _se_segment(self) -> None:
        """Generate SE Transaction Set Trailer."""
        # Count segments from ST to SE (inclusive)
        segment_count = len(
            [s for s in self._segments if s.startswith("ST") or not s.startswith(("ISA", "GS"))]
        )
        self._add("SE", str(segment_count + 1), str(self.config.st_control_number).zfill(4))

    def _ge_segment(self) -> None:
        """Generate GE Functional Group Trailer."""
        self._add("GE", "1", str(self.config.gs_control_number))

    def _iea_segment(self) -> None:
        """Generate IEA Interchange Control Trailer."""
        self._add("IEA", "1", str(self.config.isa_control_number).zfill(9))

    def to_string(self) -> str:
        """Convert segments to X12 string."""
        return "\n".join(self._segments)

    def reset(self) -> None:
        """Clear segments for new transaction."""
        self._segments = []
