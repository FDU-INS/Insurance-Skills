"""Settings management for HealthSim applications.

Provides a base settings class that can be extended by products
built on HealthSim Core.
"""

from pydantic import BaseModel, Field


class HealthSimSettings(BaseModel):
    """Base settings for HealthSim applications.

    Products should extend this class with their own settings.

    Example:
        >>> class PatientSimSettings(HealthSimSettings):
        ...     default_facility: str = "HOSPITAL"
        ...
        >>> settings = PatientSimSettings(debug=True)
        >>> settings.debug
        True
    """

    app_name: str = Field(default="healthsim", description="Application name")
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    random_seed: int | None = Field(default=None, description="Random seed for reproducibility")
    locale: str = Field(default="en_US", description="Locale for data generation")

    model_config = {"extra": "allow"}
