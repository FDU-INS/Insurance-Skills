"""Tests for underwriting models."""

import pytest
from geo_infer_risk.underwriting.models.underwriting_models import (
    Decision,
    DecisionStatus,
    Guideline,
    GuidelineType,
    UnderwritingCase,
    UnderwritingQueue,
)


class TestDecision:
    """Tests for Decision dataclass."""

    def test_import(self) -> None:
        assert Decision is not None

    def test_decision_status_values(self) -> None:
        assert DecisionStatus.APPROVED.value == "approved"
        assert DecisionStatus.DECLINED.value == "declined"


class TestGuideline:
    """Tests for Guideline dataclass."""

    def test_import(self) -> None:
        assert Guideline is not None

    def test_guideline_type_values(self) -> None:
        assert GuidelineType.MANDATORY.value == "mandatory"


class TestUnderwritingCase:
    """Tests for UnderwritingCase dataclass."""

    def test_import(self) -> None:
        assert UnderwritingCase is not None


class TestUnderwritingQueue:
    """Tests for UnderwritingQueue."""

    def test_import(self) -> None:
        assert UnderwritingQueue is not None
