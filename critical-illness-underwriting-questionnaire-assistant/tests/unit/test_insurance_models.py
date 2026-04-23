"""Tests for insurance models."""

import numpy as np
import pandas as pd
import pytest
from geo_infer_risk.core.insurance_models import (
    InsuranceConfig,
    PropertyInsuranceModel,
    LiabilityInsuranceModel,
    CatastropheInsuranceModel,
    InsuranceManager,
)


def _make_property_data() -> pd.DataFrame:
    return pd.DataFrame({
        "property_type": ["residential", "commercial", "residential"],
        "property_value": [200000, 500000, 300000],
        "loss_amount": [4000, 15000, 6000],
        "premium": [1000, 2500, 1500],
        "location": ["medium_risk", "high_risk", "low_risk"],
        "claim_frequency": [0.02, 0.05, 0.01],
        "construction_type": ["frame", "ordinary", "fire_resistive"],
    })


def _make_liability_data() -> pd.DataFrame:
    return pd.DataFrame({
        "business_type": ["general", "professional", "general"],
        "claim_frequency": [0.01, 0.02, 0.015],
        "claim_severity": [50000, 100000, 75000],
        "premium": [500, 1000, 750],
    })


class TestPropertyInsuranceModel:
    """Tests for property insurance model."""

    def setup_method(self) -> None:
        self.model = PropertyInsuranceModel()
        self.model.fit(_make_property_data())

    def test_fit_sets_fitted(self) -> None:
        assert self.model.is_fitted is True

    def test_calculate_premium_positive(self) -> None:
        premium = self.model.calculate_premium({
            "property_value": 250000,
            "property_type": "residential",
            "location": "medium_risk",
        })
        assert premium > 0

    def test_estimate_losses_keys(self) -> None:
        losses = self.model.estimate_losses({
            "property_value": 250000,
            "property_type": "residential",
        })
        assert "expected_loss" in losses
        assert "var_95" in losses
        assert "cvar_95" in losses

    def test_safety_features_reduce_premium(self) -> None:
        p1 = self.model.calculate_premium({
            "property_value": 200000,
            "safety_features": [],
        })
        p2 = self.model.calculate_premium({
            "property_value": 200000,
            "safety_features": ["sprinkler_system", "alarm_system"],
        })
        assert p2 < p1

    def test_unfitted_model_raises(self) -> None:
        model = PropertyInsuranceModel()
        with pytest.raises(ValueError):
            model.calculate_premium({"property_value": 100000})


class TestLiabilityInsuranceModel:
    """Tests for liability insurance model."""

    def setup_method(self) -> None:
        self.model = LiabilityInsuranceModel()
        self.model.fit(_make_liability_data())

    def test_fit_sets_fitted(self) -> None:
        assert self.model.is_fitted is True

    def test_calculate_premium_positive(self) -> None:
        premium = self.model.calculate_premium({
            "liability_limit": 1000000,
            "business_type": "general",
            "annual_revenue": 500000,
        })
        assert premium > 0

    def test_estimate_losses(self) -> None:
        losses = self.model.estimate_losses({
            "liability_limit": 1000000,
            "business_type": "general",
        })
        assert losses["expected_loss"] >= 0
        assert losses["max_loss"] == 1000000


class TestCatastropheInsuranceModel:
    """Tests for catastrophe insurance model."""

    def setup_method(self) -> None:
        self.model = CatastropheInsuranceModel()
        self.model.fit(pd.DataFrame({"dummy": [1]}))

    def test_calculate_premium_hurricane(self) -> None:
        premium = self.model.calculate_premium({
            "coverage_limit": 1000000,
            "location": {"lat": 30, "lon": -80},
            "catastrophe_types": ["hurricane"],
        })
        assert premium > 0

    def test_multi_peril_premium(self) -> None:
        p_single = self.model.calculate_premium({
            "coverage_limit": 1000000,
            "location": {"lat": 35, "lon": -90},
            "catastrophe_types": ["earthquake"],
        })
        p_multi = self.model.calculate_premium({
            "coverage_limit": 1000000,
            "location": {"lat": 35, "lon": -90},
            "catastrophe_types": ["earthquake", "flood"],
        })
        assert p_multi > p_single


class TestInsuranceManager:
    """Tests for the insurance manager."""

    def setup_method(self) -> None:
        self.manager = InsuranceManager()

    def test_models_initialized(self) -> None:
        assert "property" in self.manager.models
        assert "liability" in self.manager.models
        assert "catastrophe" in self.manager.models

    def test_fit_model(self) -> None:
        success = self.manager.fit_model("property", _make_property_data())
        assert success is True

    def test_fit_unknown_model(self) -> None:
        success = self.manager.fit_model("unknown", pd.DataFrame())
        assert success is False
