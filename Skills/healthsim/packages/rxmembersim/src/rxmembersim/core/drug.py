"""Drug reference model."""
from enum import Enum

from pydantic import BaseModel


class DEASchedule(str, Enum):
    """DEA controlled substance schedules."""

    SCHEDULE_II = "2"
    SCHEDULE_III = "3"
    SCHEDULE_IV = "4"
    SCHEDULE_V = "5"
    NON_CONTROLLED = "0"


class DrugReference(BaseModel):
    """Drug reference information."""

    ndc: str  # 11-digit National Drug Code
    drug_name: str
    generic_name: str

    # Classification
    gpi: str  # Generic Product Identifier (14 chars)
    therapeutic_class: str

    # Characteristics
    strength: str
    dosage_form: str
    route_of_admin: str

    # Controlled substance
    dea_schedule: DEASchedule = DEASchedule.NON_CONTROLLED

    # Brand/generic
    is_brand: bool = False
    multi_source_code: str = "Y"  # Y=multi-source, N=single-source

    # Pricing reference
    awp: float | None = None  # Average Wholesale Price
    wac: float | None = None  # Wholesale Acquisition Cost
