"""Tests for risk models."""

import numpy as np
import pytest
from geo_infer_risk.core.risk_models import (
    RiskModel,
    RiskParameters,
    HazardModel,
    VulnerabilityModel,
    ExposureModel,
)


class TestRiskModels:
    """Tests for risk model implementations."""

    def test_risk_model_import(self) -> None:
        assert RiskModel is not None

    def test_risk_parameters_import(self) -> None:
        assert RiskParameters is not None

    def test_hazard_model_import(self) -> None:
        assert HazardModel is not None

    def test_vulnerability_model_import(self) -> None:
        assert VulnerabilityModel is not None

    def test_exposure_model_import(self) -> None:
        assert ExposureModel is not None
