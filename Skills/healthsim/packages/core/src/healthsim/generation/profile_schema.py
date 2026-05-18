"""Profile specification schema for data generation.

Defines the structure for profile specifications that describe
how to generate cohorts of healthcare entities.

The two-phase architecture:
  Phase 1 (Building): Conversational → ProfileSpecification JSON
  Phase 2 (Execution): ProfileSpecification → Generated Data
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class DistributionType(str, Enum):
    """Supported distribution types."""

    CATEGORICAL = "categorical"
    NORMAL = "normal"
    LOG_NORMAL = "log_normal"
    UNIFORM = "uniform"
    AGE_BANDS = "age_bands"
    EXPLICIT = "explicit"
    CONDITIONAL = "conditional"


class DistributionSpec(BaseModel):
    """Specification for a statistical distribution.

    Example:
        {"type": "normal", "mean": 72, "std_dev": 8, "min": 65, "max": 95}
    """

    type: DistributionType
    # For categorical
    weights: dict[str, float] | None = None
    # For normal/log_normal
    mean: float | None = None
    std_dev: float | None = None
    # For uniform and bounds
    min: float | None = None
    max: float | None = None
    # For age_bands
    bands: dict[str, float] | None = None
    # For explicit
    values: list[dict[str, Any]] | None = None
    # For conditional
    rules: list[dict[str, Any]] | None = None
    default: dict[str, Any] | None = None


class GeographyReference(BaseModel):
    """Reference to PopulationSim geography data."""

    source: Literal["populationsim"] = "populationsim"
    type: Literal["county", "state", "msa", "zip"] = "county"
    code: str | None = None  # FIPS code, state abbrev, etc.
    fips: str | None = None
    state: str | None = None
    city_distribution: str | None = None  # "population_weighted", "uniform"
    datasets: list[str] | None = None  # ["acs_demographics", "cdc_places", "svi"]


class ProviderReference(BaseModel):
    """Reference to NetworkSim provider data.
    
    Used to assign real provider NPIs from the NPPES database.
    
    Example:
        {"source": "networksim", "state": "TX", "specialty": "internal_medicine"}
    """
    source: Literal["networksim"] = "networksim"
    state: str | None = None
    city: str | None = None
    zip_code: str | None = None
    specialty: str | None = None  # Maps to taxonomy code via TAXONOMY_MAP
    entity_type: Literal["individual", "organization"] | None = None
    assignment: Literal["random", "nearest", "round_robin"] = "random"


class FacilityReference(BaseModel):
    """Reference to NetworkSim facility data.
    
    Used to assign real facility CCNs from CMS data.
    
    Example:
        {"source": "networksim", "state": "TX", "type": "hospital"}
    """
    source: Literal["networksim"] = "networksim"
    state: str | None = None
    city: str | None = None
    type: Literal["hospital", "snf", "hha", "hospice", "fqhc", "rhc", "asc", "other"] | None = None
    min_beds: int | None = None
    assignment: Literal["random", "nearest", "round_robin"] = "random"


class NetworkSimSpec(BaseModel):
    """NetworkSim provider and facility assignment specification."""
    
    primary_care_provider: ProviderReference | None = None
    specialists: dict[str, ProviderReference] | None = None  # condition -> provider ref
    primary_facility: FacilityReference | None = None
    facility_types: dict[str, FacilityReference] | None = None  # type -> facility ref


class DemographicsSpec(BaseModel):
    """Demographic attributes specification."""

    age: DistributionSpec | None = None
    gender: DistributionSpec | None = None
    race: DistributionSpec | None = None
    ethnicity: DistributionSpec | None = None
    geography: GeographyReference | None = None
    # For reference-based profiles
    source: Literal["explicit", "populationsim", "hybrid"] | None = None
    reference: GeographyReference | None = None


class ConditionSpec(BaseModel):
    """Clinical condition specification."""

    code: str  # ICD-10 code (e.g., "E11" for diabetes)
    description: str | None = None
    prevalence: float = 1.0  # 0.0 to 1.0
    severity: DistributionSpec | None = None


class ClinicalSpec(BaseModel):
    """Clinical attributes specification."""

    primary_condition: ConditionSpec | None = None
    comorbidities: list[ConditionSpec] | None = None
    severity: DistributionSpec | None = None
    # Lab values can be conditional on severity
    lab_values: dict[str, DistributionSpec] | None = None


class CoverageSpec(BaseModel):
    """Insurance coverage specification."""

    type: str | None = None  # "Medicare", "Medicaid", "Commercial"
    plan_distribution: dict[str, float] | None = None
    plan_type: DistributionSpec | None = None


class OutputSpec(BaseModel):
    """Output format specification for a product."""

    formats: list[str] | None = None  # ["fhir_r4", "hl7v2_adt", "x12_837"]
    include: list[str] | None = None  # ["patient", "conditions", "encounters"]


class GenerationSpec(BaseModel):
    """Generation control parameters."""

    count: int = Field(ge=1, le=100000, default=100)
    products: list[str] = ["patientsim"]  # Which products to generate for
    seed: int | None = None  # For reproducibility
    validation: Literal["strict", "warn", "none"] = "strict"


class JourneyReference(BaseModel):
    """Reference to a journey specification."""

    id: str | None = None
    template: str | None = None  # Pre-built journey template name
    inline: dict[str, Any] | None = None  # Inline journey definition


class ProfileSpecification(BaseModel):
    """Complete profile specification for cohort generation.

    This is the output of Phase 1 (Profile Builder) and the input
    to Phase 2 (Profile Executor).

    Example:
        ```json
        {
          "id": "medicare-diabetic-texas-001",
          "name": "Texas Medicare Diabetic Population",
          "version": "1.0",
          "generation": {"count": 200, "products": ["patientsim", "membersim"]},
          "demographics": {
            "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65}
          },
          "clinical": {
            "primary_condition": {"code": "E11", "prevalence": 1.0}
          }
        }
        ```
    """

    # Identification
    id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    name: str
    version: str = "1.0"
    description: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    # Generation parameters
    generation: GenerationSpec = Field(default_factory=GenerationSpec)

    # Entity specifications
    demographics: DemographicsSpec | None = None
    clinical: ClinicalSpec | None = None
    coverage: CoverageSpec | None = None

    # Output specifications per product
    outputs: dict[str, OutputSpec] | None = None

    # Optional journey
    journey: JourneyReference | None = None

    # Custom/extension fields
    custom: dict[str, Any] | None = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Ensure ID is lowercase with hyphens only."""
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("ID must contain only alphanumeric, hyphens, underscores")
        return v.lower()

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return self.model_dump_json(indent=2, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> "ProfileSpecification":
        """Deserialize from JSON string."""
        return cls.model_validate_json(json_str)

    def get_distribution(self, path: str) -> DistributionSpec | None:
        """Get a distribution spec by dot-notation path.

        Args:
            path: Dot-notation path like "demographics.age"

        Returns:
            DistributionSpec if found, None otherwise
        """
        parts = path.split(".")
        obj: Any = self
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return None
        return obj if isinstance(obj, DistributionSpec) else None


# Example profile templates as constants
PROFILE_TEMPLATES = {
    "medicare-diabetic": {
        "id": "medicare-diabetic-template",
        "name": "Medicare Diabetic Population",
        "generation": {"count": 100, "products": ["patientsim", "membersim"]},
        "demographics": {
            "age": {"type": "normal", "mean": 72, "std_dev": 8, "min": 65, "max": 95},
            "gender": {"type": "categorical", "weights": {"M": 0.48, "F": 0.52}},
        },
        "clinical": {
            "primary_condition": {"code": "E11", "description": "Type 2 diabetes", "prevalence": 1.0},
            "comorbidities": [
                {"code": "I10", "description": "Hypertension", "prevalence": 0.75},
                {"code": "E78", "description": "Hyperlipidemia", "prevalence": 0.70},
            ],
        },
        "coverage": {"type": "Medicare", "plan_distribution": {"Medicare Advantage": 0.55, "Original Medicare": 0.45}},
    },
    "commercial-healthy": {
        "id": "commercial-healthy-template",
        "name": "Healthy Commercial Population",
        "generation": {"count": 100, "products": ["membersim"]},
        "demographics": {
            "age": {"type": "normal", "mean": 38, "std_dev": 12, "min": 18, "max": 64},
            "gender": {"type": "categorical", "weights": {"M": 0.50, "F": 0.50}},
        },
        "coverage": {
            "type": "Commercial",
            "plan_distribution": {"PPO": 0.45, "HMO": 0.35, "HDHP": 0.15, "POS": 0.05},
        },
    },
    "medicaid-pediatric": {
        "id": "medicaid-pediatric-template",
        "name": "Medicaid Pediatric Population",
        "generation": {"count": 100, "products": ["patientsim", "membersim"]},
        "demographics": {
            "age": {
                "type": "age_bands",
                "bands": {"0-2": 0.15, "3-5": 0.15, "6-12": 0.35, "13-17": 0.35},
            },
            "gender": {"type": "categorical", "weights": {"M": 0.51, "F": 0.49}},
        },
        "coverage": {"type": "Medicaid"},
    },
}
