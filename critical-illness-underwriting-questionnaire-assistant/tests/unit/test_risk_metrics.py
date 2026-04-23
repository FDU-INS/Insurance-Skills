"""Tests for risk metrics utilities."""

import numpy as np
import pytest
from geo_infer_risk.utils.risk_metrics import calculate_aal, calculate_ep_curve


class TestRiskMetrics:
    """Tests for risk metric calculations."""

    def test_calculate_aal(self) -> None:
        losses = np.array([1000.0, 2000.0, 500.0, 3000.0, 1500.0])
        aal = calculate_aal(losses)
        assert isinstance(aal, float)
        assert aal > 0

    def test_calculate_ep_curve(self) -> None:
        losses = np.array([1000.0, 2000.0, 500.0, 3000.0, 1500.0])
        ep_curve = calculate_ep_curve(losses)
        assert isinstance(ep_curve, dict) or isinstance(ep_curve, (list, np.ndarray, tuple))
