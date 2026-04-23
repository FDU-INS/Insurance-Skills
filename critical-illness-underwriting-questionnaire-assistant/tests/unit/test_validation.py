"""Tests for risk validation utilities."""

import pytest
from geo_infer_risk.utils.validation import validate_config, ValidationResult


class TestValidation:
    """Tests for config validation."""

    def test_validate_config_returns_result(self) -> None:
        config = {"hazard_type": "flood", "return_periods": [10, 50, 100]}
        result = validate_config(config)
        assert isinstance(result, ValidationResult)

    def test_validation_result_has_is_valid(self) -> None:
        config = {"hazard_type": "flood"}
        result = validate_config(config)
        assert hasattr(result, "is_valid")

    def test_empty_config(self) -> None:
        result = validate_config({})
        assert isinstance(result, ValidationResult)
