"""
Tests for LLM client module.

Tests focus on:
1. Error handling and exception hierarchy
2. Response parsing and validation
3. Fallback explanations
4. Factory function behavior

Note: These tests do NOT make real API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.llm_client import (
    LLMClient,
    LLMError,
    LLMNotConfiguredError,
    LLMQuotaExhaustedError,
    LLMResponseError,
    LLMRateLimitError,
    LLMNetworkError,
    LLMReactionResult,
    LLMInsightResult,
    create_llm_client,
    generate_rule_based_explanation,
    generate_rule_based_summary_insight,
    DELTA_HAPPINESS_RANGE,
    DELTA_SUPPORT_RANGE,
    DELTA_INCOME_PCT_RANGE,
)
from src.data_models import (
    Citizen,
    CitizenState,
    Policy,
    PolicyDomain,
    IncomeLevel,
    CityZone,
    PoliticalView,
    ReactionMethod,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_citizen() -> Citizen:
    """Create a sample citizen for testing."""
    return Citizen(
        id=1,
        age=35,
        gender="Female",
        income_level=IncomeLevel.MIDDLE,
        city_zone=CityZone.SUBURBAN,
        education_years=16,
        profession="Software Engineer",
        family_size=3,
        political_view=PoliticalView.MODERATE,
        risk_tolerance=0.6,
        openness_to_change=0.7,
    )


@pytest.fixture
def sample_state() -> CitizenState:
    """Create a sample citizen state for testing."""
    return CitizenState(
        citizen_id=1,
        step=0,
        happiness=0.65,
        policy_support=0.1,
        income=75000.0,
        reaction_method=ReactionMethod.RULE_BASED,
    )


@pytest.fixture
def sample_policy() -> Policy:
    """Create a sample policy for testing."""
    return Policy(
        title="Education Reform",
        description="Comprehensive education funding increase.",
        domain=PolicyDomain.EDUCATION,
    )


# =============================================================================
# Test Exception Hierarchy
# =============================================================================

class TestExceptionHierarchy:
    """Test that all LLM exceptions inherit from LLMError."""
    
    def test_llm_not_configured_inherits_from_llm_error(self):
        assert issubclass(LLMNotConfiguredError, LLMError)
    
    def test_llm_quota_exhausted_inherits_from_llm_error(self):
        assert issubclass(LLMQuotaExhaustedError, LLMError)
    
    def test_llm_response_error_inherits_from_llm_error(self):
        assert issubclass(LLMResponseError, LLMError)
    
    def test_llm_rate_limit_error_inherits_from_llm_error(self):
        assert issubclass(LLMRateLimitError, LLMError)
    
    def test_llm_network_error_inherits_from_llm_error(self):
        assert issubclass(LLMNetworkError, LLMError)


# =============================================================================
# Test Factory Function
# =============================================================================

class TestCreateLLMClient:
    """Test the create_llm_client factory function."""
    
    def test_returns_none_for_empty_keys(self):
        result = create_llm_client([])
        assert result is None
    
    def test_returns_none_for_whitespace_keys(self):
        result = create_llm_client(["", "   ", "\t"])
        assert result is None
    
    def test_returns_none_for_none_keys(self):
        result = create_llm_client([None])  # type: ignore
        assert result is None
    
    def test_returns_client_for_valid_key(self):
        result = create_llm_client(["valid_key_12345"])
        assert result is not None
        assert isinstance(result, LLMClient)
    
    def test_filters_empty_keys(self):
        result = create_llm_client(["", "valid_key", ""])
        assert result is not None


# =============================================================================
# Test LLMClient Initialization
# =============================================================================

class TestLLMClientInit:
    """Test LLMClient initialization."""
    
    def test_raises_for_no_valid_keys(self):
        with pytest.raises(LLMNotConfiguredError):
            LLMClient([])
    
    def test_raises_for_all_empty_keys(self):
        with pytest.raises(LLMNotConfiguredError):
            LLMClient(["", "  "])
    
    def test_initializes_with_valid_keys(self):
        client = LLMClient(["key1", "key2"])
        assert client.is_available
    
    def test_strips_whitespace_from_keys(self):
        client = LLMClient(["  key1  ", "key2"])
        assert client.is_available
    
    def test_custom_model_name(self):
        client = LLMClient(["key1"], model_name="custom-model")
        assert client._model_name == "custom-model"


# =============================================================================
# Test Response Parsing
# =============================================================================

class TestResponseParsing:
    """Test JSON response parsing."""
    
    def test_parse_json_response_direct(self):
        client = LLMClient(["key1"])
        text = '{"delta_happiness": 0.05, "delta_support": 0.1}'
        result = client._parse_json_response(text)
        assert result["delta_happiness"] == 0.05
        assert result["delta_support"] == 0.1
    
    def test_parse_json_with_markdown_code_block(self):
        client = LLMClient(["key1"])
        text = '```json\n{"delta_happiness": 0.05}\n```'
        result = client._parse_json_response(text)
        assert result["delta_happiness"] == 0.05
    
    def test_parse_json_with_surrounding_text(self):
        client = LLMClient(["key1"])
        text = 'Here is the result: {"delta_happiness": 0.05} That is all.'
        result = client._parse_json_response(text)
        assert result["delta_happiness"] == 0.05
    
    def test_parse_json_raises_for_invalid(self):
        client = LLMClient(["key1"])
        with pytest.raises(LLMResponseError):
            client._parse_json_response("not valid json at all")


# =============================================================================
# Test Value Clamping
# =============================================================================

class TestValueClamping:
    """Test that values are properly clamped to valid ranges."""
    
    def test_clamp_within_range(self):
        client = LLMClient(["key1"])
        assert client._clamp(0.5, 0.0, 1.0) == 0.5
    
    def test_clamp_below_min(self):
        client = LLMClient(["key1"])
        assert client._clamp(-0.5, 0.0, 1.0) == 0.0
    
    def test_clamp_above_max(self):
        client = LLMClient(["key1"])
        assert client._clamp(1.5, 0.0, 1.0) == 1.0
    
    def test_delta_happiness_range_is_valid(self):
        assert DELTA_HAPPINESS_RANGE[0] < 0 < DELTA_HAPPINESS_RANGE[1]
    
    def test_delta_support_range_is_valid(self):
        assert DELTA_SUPPORT_RANGE[0] < 0 < DELTA_SUPPORT_RANGE[1]
    
    def test_delta_income_range_is_valid(self):
        assert DELTA_INCOME_PCT_RANGE[0] < 0 < DELTA_INCOME_PCT_RANGE[1]


# =============================================================================
# Test Result Data Types
# =============================================================================

class TestResultDataTypes:
    """Test LLM result data types."""
    
    def test_reaction_result_is_frozen(self):
        result = LLMReactionResult(
            delta_happiness=0.05,
            delta_support=0.1,
            delta_income_pct=0.02,
            explanation="Test explanation",
            raw_response="{}",
        )
        with pytest.raises(AttributeError):
            result.delta_happiness = 0.1  # type: ignore
    
    def test_insight_result_is_frozen(self):
        result = LLMInsightResult(
            insight="Test insight",
            key_factors=["factor1", "factor2"],
            raw_response="{}",
        )
        with pytest.raises(AttributeError):
            result.insight = "changed"  # type: ignore


# =============================================================================
# Test Rule-Based Fallback Explanations
# =============================================================================

class TestRuleBasedExplanations:
    """Test template-based fallback explanations."""
    
    def test_generates_explanation_for_positive_happiness(self, sample_citizen):
        explanation = generate_rule_based_explanation(
            citizen=sample_citizen,
            delta_happiness=0.05,
            delta_support=0.03,
            policy_domain="Education",
        )
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        assert "improved" in explanation.lower() or "increased" in explanation.lower()
    
    def test_generates_explanation_for_negative_happiness(self, sample_citizen):
        explanation = generate_rule_based_explanation(
            citizen=sample_citizen,
            delta_happiness=-0.05,
            delta_support=-0.03,
            policy_domain="Economy",
        )
        assert isinstance(explanation, str)
        assert "declined" in explanation.lower() or "decreased" in explanation.lower()
    
    def test_explanation_includes_income_level(self, sample_citizen):
        explanation = generate_rule_based_explanation(
            citizen=sample_citizen,
            delta_happiness=0.05,
            delta_support=0.03,
            policy_domain="Social",
        )
        # At least one template should mention income
        assert any(x in explanation.lower() for x in ["middle", "income"])
    
    def test_deterministic_template_selection(self, sample_citizen):
        # Same citizen ID should give same template
        exp1 = generate_rule_based_explanation(
            citizen=sample_citizen,
            delta_happiness=0.05,
            delta_support=0.03,
            policy_domain="Education",
        )
        exp2 = generate_rule_based_explanation(
            citizen=sample_citizen,
            delta_happiness=0.05,
            delta_support=0.03,
            policy_domain="Education",
        )
        assert exp1 == exp2


class TestRuleBasedSummaryInsight:
    """Test template-based summary insights."""
    
    def test_generates_insight_for_positive_change(self):
        insight = generate_rule_based_summary_insight(
            policy_domain="Education",
            happiness_change=0.05,
            support_change=0.03,
            gap_change=-0.02,
        )
        assert isinstance(insight, str)
        assert len(insight) > 0
        assert "improved" in insight.lower() or "gained" in insight.lower()
    
    def test_generates_insight_for_negative_change(self):
        insight = generate_rule_based_summary_insight(
            policy_domain="Economy",
            happiness_change=-0.05,
            support_change=-0.03,
            gap_change=0.02,
        )
        assert "declined" in insight.lower() or "lost" in insight.lower()
    
    def test_mentions_inequality(self):
        insight = generate_rule_based_summary_insight(
            policy_domain="Social",
            happiness_change=0.01,
            support_change=0.01,
            gap_change=0.05,
        )
        assert "inequality" in insight.lower()
    
    def test_describes_gap_widening(self):
        insight = generate_rule_based_summary_insight(
            policy_domain="Business",
            happiness_change=0.0,
            support_change=0.0,
            gap_change=0.02,
        )
        assert "widened" in insight.lower()
    
    def test_describes_gap_narrowing(self):
        insight = generate_rule_based_summary_insight(
            policy_domain="Social",
            happiness_change=0.0,
            support_change=0.0,
            gap_change=-0.02,
        )
        assert "narrowed" in insight.lower()


# =============================================================================
# Test Key Rotation Logic
# =============================================================================

class TestKeyRotation:
    """Test API key rotation behavior."""
    
    def test_initial_key_index_is_zero(self):
        client = LLMClient(["key1", "key2", "key3"])
        assert client._current_key_index == 0
    
    def test_rotate_marks_key_exhausted(self):
        client = LLMClient(["key1", "key2"])
        assert 0 not in client._exhausted_keys
        result = client._rotate_api_key()
        assert result is True
        assert 0 in client._exhausted_keys
    
    def test_rotate_moves_to_next_key(self):
        client = LLMClient(["key1", "key2", "key3"])
        client._rotate_api_key()
        assert client._current_key_index == 1
    
    def test_rotate_returns_false_when_all_exhausted(self):
        client = LLMClient(["key1"])
        result = client._rotate_api_key()
        assert result is False
    
    def test_is_available_with_non_exhausted_keys(self):
        client = LLMClient(["key1", "key2"])
        assert client.is_available is True
    
    def test_is_available_false_when_all_exhausted(self):
        client = LLMClient(["key1"])
        client._exhausted_keys.add(0)
        assert client.is_available is False
    
    def test_reset_exhausted_keys(self):
        client = LLMClient(["key1", "key2"])
        client._exhausted_keys.add(0)
        client._exhausted_keys.add(1)
        assert client.is_available is False
        
        client.reset_exhausted_keys()
        assert client.is_available is True
        assert len(client._exhausted_keys) == 0


# =============================================================================
# Test Integration with Data Models
# =============================================================================

class TestDataModelIntegration:
    """Test that LLM results work with data models."""
    
    def test_reaction_result_values_in_valid_range(self):
        # Simulating what generate_citizen_reaction would return
        result = LLMReactionResult(
            delta_happiness=0.15,
            delta_support=0.25,
            delta_income_pct=0.05,
            explanation="Test",
            raw_response="{}",
        )
        
        assert DELTA_HAPPINESS_RANGE[0] <= result.delta_happiness <= DELTA_HAPPINESS_RANGE[1]
        assert DELTA_SUPPORT_RANGE[0] <= result.delta_support <= DELTA_SUPPORT_RANGE[1]
        assert DELTA_INCOME_PCT_RANGE[0] <= result.delta_income_pct <= DELTA_INCOME_PCT_RANGE[1]
    
    def test_explanation_length_limit(self):
        result = LLMReactionResult(
            delta_happiness=0.0,
            delta_support=0.0,
            delta_income_pct=0.0,
            explanation="x" * 200,  # Max length
            raw_response="{}",
        )
        assert len(result.explanation) <= 200
