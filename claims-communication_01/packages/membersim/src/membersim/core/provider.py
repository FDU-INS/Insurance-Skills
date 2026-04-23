"""Healthcare provider model."""

from datetime import date

from healthsim.person import Address
from pydantic import BaseModel, Field


class Provider(BaseModel):
    """Healthcare provider in the network."""

    model_config = {"frozen": True}

    npi: str = Field(..., description="National Provider Identifier (10 digits)")
    tax_id: str = Field(..., description="Tax identification number")
    name: str = Field(..., description="Provider name")
    specialty: str = Field(..., description="Taxonomy code or specialty name")
    provider_type: str = Field("INDIVIDUAL", description="INDIVIDUAL, GROUP, FACILITY")
    address: Address = Field(..., description="Practice address")

    # Network participation
    network_status: str = Field("IN_NETWORK", description="IN_NETWORK, OUT_OF_NETWORK, PAR")
    effective_date: date = Field(..., description="Network participation start date")
    termination_date: date | None = Field(None, description="Network participation end date")

    # Panel info (for PCPs)
    accepting_patients: bool = Field(True, description="Currently accepting new patients")
    panel_size: int | None = Field(None, description="Current patient panel size")

    @property
    def is_active(self) -> bool:
        """Check if provider is currently active in network."""
        today = date.today()
        if self.termination_date is None:
            return self.effective_date <= today
        return self.effective_date <= today <= self.termination_date


# Common specialties with taxonomy codes
SPECIALTIES = {
    "207Q00000X": "Family Medicine",
    "207R00000X": "Internal Medicine",
    "208000000X": "Pediatrics",
    "207RC0000X": "Cardiovascular Disease",
    "207RE0101X": "Endocrinology",
    "2084N0400X": "Neurology",
    "207X00000X": "Orthopedic Surgery",
    "208600000X": "General Surgery",
    "282N00000X": "General Acute Care Hospital",
    "261QU0200X": "Urgent Care Clinic",
}
