"""Tests for hazard model."""

import numpy as np
import pytest
from geo_infer_risk.core.hazard_model import EnhancedHazardModel


class TestEnhancedHazardModel:
    """Tests for the enhanced hazard model."""

    def setup_method(self) -> None:
        self.model = EnhancedHazardModel(
            hazard_type="flood",
            params={
                "return_periods": [10, 50, 100],
                "include_climate_change": False,
                "spatial_resolution": 9,
            },
        )

    def test_initialization(self) -> None:
        assert self.model.hazard_type == "flood"
        assert self.model.return_periods == [10, 50, 100]
        assert self.model.is_fitted is False

    def test_different_hazard_types(self) -> None:
        for htype in ["earthquake", "hurricane", "wildfire", "flood"]:
            m = EnhancedHazardModel(hazard_type=htype, params={})
            assert m.hazard_type == htype

    def test_default_parameters(self) -> None:
        m = EnhancedHazardModel(hazard_type="generic", params={})
        assert m.return_periods == [10, 25, 50, 100, 500]
        assert m.spatial_resolution == 9

    def test_climate_change_flag(self) -> None:
        m = EnhancedHazardModel(
            hazard_type="flood", params={"include_climate_change": True}
        )
        assert m.include_climate_change is True
