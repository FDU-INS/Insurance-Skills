"""Tests for exposure model."""

import numpy as np
import pytest
from geo_infer_risk.core.exposure_model import EnhancedExposureModel


class TestEnhancedExposureModel:
    """Tests for the enhanced exposure model."""

    def setup_method(self) -> None:
        self.model = EnhancedExposureModel(
            exposure_type="property",
            params={
                "value_type": "replacement_cost",
                "aggregation_level": "building",
            },
        )

    def test_initialization(self) -> None:
        assert self.model.exposure_type == "property"
        assert self.model.value_type == "replacement_cost"
        assert self.model.aggregation_level == "building"

    def test_different_exposure_types(self) -> None:
        for etype in ["property", "population", "infrastructure", "business"]:
            m = EnhancedExposureModel(exposure_type=etype, params={})
            assert m.exposure_type == etype

    def test_default_time_scenarios(self) -> None:
        m = EnhancedExposureModel(exposure_type="population", params={})
        assert "day" in m.time_scenarios
        assert "night" in m.time_scenarios

    def test_spatial_resolution_default(self) -> None:
        m = EnhancedExposureModel(exposure_type="property", params={})
        assert m.spatial_resolution == 9
