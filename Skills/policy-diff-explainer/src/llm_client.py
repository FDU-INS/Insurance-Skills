"""
PolicyPulse - LLM Client

Nebius OpenAI-compatible API wrapper with rate limiting and fallback support.
Reference: TECH_STACK.md Section 4 (LLM Provider: Nebius)

This module is ISOLATED from business logic.
It handles ONLY: API calls, rate limiting, retry, error classification.

Dependencies: openai
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.data_models import Citizen, CitizenState, Policy


logger = logging.getLogger("policypulse.llm_client")


# =============================================================================
# Exception Hierarchy
# =============================================================================

class LLMError(Exception):
    """Base exception for all LLM-related errors."""
    pass


class LLMNotConfiguredError(LLMError):
    """Raised when no API keys are configured."""
    pass


class LLMQuotaExhaustedError(LLMError):
    """Raised when all API keys have exhausted their quotas."""
    pass


class LLMResponseError(LLMError):
    """Raised when the LLM returns an unparseable response."""
    pass


class LLMRateLimitError(LLMError):
    """Raised when rate limit is hit (temporary, can retry)."""
    pass


class LLMNetworkError(LLMError):
    """Raised when network issues prevent API access."""
    pass


# =============================================================================
# Response Data Types
# =============================================================================

@dataclass(frozen=True)
class LLMReactionResult:
    """
    Parsed result from LLM citizen reaction generation.
    
    All numeric values are validated and clamped to valid ranges.
    """
    delta_happiness: float  # -0.3 to 0.3
    delta_support: float    # -0.5 to 0.5
    delta_income_pct: float  # -0.1 to 0.1 (percentage of current income)
    explanation: str        # Short factual explanation (max 200 chars)
    raw_response: str       # Original LLM response for debugging


@dataclass(frozen=True)
class LLMInsightResult:
    """
    Parsed result from LLM summary insight generation.
    """
    insight: str            # Short factual insight (max 300 chars)
    key_factors: list[str]  # Top 3 factors mentioned
    raw_response: str


# =============================================================================
# LLM Client Configuration
# =============================================================================

# Rate limiting constants
MIN_REQUEST_INTERVAL = 1.0  # seconds between requests
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2.0    # exponential backoff base

# Nebius API configuration
DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"
DEFAULT_MODEL = "openai/gpt-oss-120b"

# Response validation ranges (conservative)
DELTA_HAPPINESS_RANGE = (-0.3, 0.3)
DELTA_SUPPORT_RANGE = (-0.5, 0.5)
DELTA_INCOME_PCT_RANGE = (-0.1, 0.1)


# =============================================================================
# Prompt Templates
# =============================================================================

CITIZEN_REACTION_SYSTEM_PROMPT = """Simulate citizen policy reactions. Output valid JSON only: {"delta_happiness": number, "delta_support": number, "delta_income_pct": number, "explanation": string}. Be concise."""

CITIZEN_REACTION_USER_PROMPT = """Analyze this citizen's reaction to the policy:

## Citizen Profile
- Age: {age} years old
- Gender: {gender}
- Income Level: {income_level}
- City Zone: {city_zone}
- Education: {education_years} years
- Profession: {profession}
- Family Size: {family_size} people
- Political View: {political_view}
- Risk Tolerance: {risk_tolerance:.0%}
- Openness to Change: {openness:.0%}

## Current State (Step {step})
- Happiness: {happiness:.1%}
- Policy Support: {support:+.1%}
- Annual Income: ${income:,.0f}

## Policy
- Title: {policy_title}
- Domain: {policy_domain}
- Description: {policy_description}

Return a JSON object with these fields:
1. "delta_happiness": Change in happiness (-0.3 to 0.3)
2. "delta_support": Change in policy support (-0.5 to 0.5)
3. "delta_income_pct": Change in income as percentage (-0.1 to 0.1)
4. "explanation": One sentence factual explanation (max 200 chars)

Consider:
- How this policy domain affects this income level
- How political views align with this policy type
- How the citizen's zone affects policy exposure
- The citizen's personality traits

Return ONLY the JSON object, no other text."""


SUMMARY_INSIGHT_SYSTEM_PROMPT = """Analyze policy results. Output valid JSON only: {\"insight\": string, \"key_factors\": [strings]}. Be concise."""

SUMMARY_INSIGHT_USER_PROMPT = """Analyze these simulation results:

## Policy
- Title: {policy_title}
- Domain: {policy_domain}

## Key Metrics (Initial → Final)
- Average Happiness: {initial_happiness:.1%} → {final_happiness:.1%} ({happiness_change:+.1%})
- Average Support: {initial_support:+.1%} → {final_support:+.1%} ({support_change:+.1%})
- Average Income: ${initial_income:,.0f} → ${final_income:,.0f} ({income_change:+.1%})
- Happiness Gap (High-Low): {initial_gap:.1%} → {final_gap:.1%} ({gap_change:+.1%})

## Instructions
Return a JSON object with:
1. "insight": A 1-2 sentence factual summary of the results (max 300 chars)
2. "key_factors": List of 3 most important factors that influenced outcomes

Focus on:
- Which groups benefited or were harmed
- Whether inequality increased or decreased
- The overall direction of change

Return ONLY the JSON object, no other text."""


# =============================================================================
# LLM Client Class
# =============================================================================

class LLMClient:
    """
    Client for Nebius OpenAI-compatible API with rate limiting and key rotation.
    
    Safety features:
    - Rate limiting
    - Key rotation on quota exhaustion
    - Retry with exponential backoff
    - Error classification for proper fallback
    - Response validation with strict parsing
    
    Reference: TECH_STACK.md Section 4 (Fallback Chain)
    """

    def __init__(
        self,
        api_keys: list[str],
        model_name: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_BASE_URL,
        min_request_interval: float = MIN_REQUEST_INTERVAL,
    ) -> None:
        """
        Initialize the LLM client.
        
        Args:
            api_keys: List of API keys for rotation (non-empty strings only)
            model_name: Model to use (default: openai/gpt-oss-120b)
            base_url: API base URL (default: Nebius endpoint)
            min_request_interval: Minimum seconds between requests
            
        Raises:
            LLMNotConfiguredError: If no valid API keys provided
        """
        # Filter to valid keys only
        self._api_keys = [k.strip() for k in api_keys if k and k.strip()]
        
        if not self._api_keys:
            raise LLMNotConfiguredError("No valid API keys provided")
        
        self._model_name = model_name
        self._base_url = base_url
        self._min_interval = min_request_interval
        self._current_key_index = 0
        self._last_request_time = 0.0
        self._exhausted_keys: set[int] = set()
        
        # Lazy-load the openai module
        self._openai_module = None
        self._client = None
        
        logger.info(
            f"LLM client initialized with {len(self._api_keys)} key(s), "
            f"model={model_name}, base_url={base_url}"
        )

    def _ensure_initialized(self) -> None:
        """Lazy-initialize the OpenAI client."""
        if self._openai_module is None:
            try:
                import openai
                self._openai_module = openai
            except ImportError as e:
                raise LLMNotConfiguredError(
                    "openai package not installed. "
                    "Install with: pip install openai"
                ) from e
        
        if self._client is None:
            self._configure_client()

    def _configure_client(self) -> None:
        """Configure the OpenAI client with current API key."""
        if self._current_key_index in self._exhausted_keys:
            if not self._rotate_api_key():
                raise LLMQuotaExhaustedError("All API keys exhausted")
        
        current_key = self._api_keys[self._current_key_index]
        
        self._client = self._openai_module.OpenAI(
            base_url=self._base_url,
            api_key=current_key,
        )
        
        masked_key = f"{current_key[:8]}...{current_key[-4:]}" if len(current_key) > 12 else "***"
        logger.debug(f"Configured client with key {masked_key}")

    def _enforce_rate_limit(self) -> None:
        """Wait if needed to respect rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            wait_time = self._min_interval - elapsed
            logger.debug(f"Rate limit: waiting {wait_time:.2f}s")
            time.sleep(wait_time)

    def _rotate_api_key(self) -> bool:
        """
        Rotate to the next available API key.
        
        Returns:
            True if rotation succeeded, False if all keys exhausted
        """
        # Mark current key as exhausted
        self._exhausted_keys.add(self._current_key_index)
        
        # Find next non-exhausted key
        for i in range(len(self._api_keys)):
            next_idx = (self._current_key_index + 1 + i) % len(self._api_keys)
            if next_idx not in self._exhausted_keys:
                self._current_key_index = next_idx
                self._client = None  # Force reconfiguration
                logger.info(f"Rotated to API key index {next_idx}")
                return True
        
        logger.warning("All API keys exhausted")
        return False

    def _make_request(self, system_prompt: str, user_prompt: str) -> str:
        """
        Make a rate-limited request to the LLM.
        
        Args:
            system_prompt: The system prompt
            user_prompt: The user prompt
            
        Returns:
            The LLM response text
            
        Raises:
            LLMQuotaExhaustedError: All keys exhausted
            LLMRateLimitError: Temporary rate limit (can retry)
            LLMNetworkError: Network issues
            LLMResponseError: Invalid response
        """
        self._ensure_initialized()
        
        for attempt in range(MAX_RETRIES):
            try:
                self._enforce_rate_limit()
                self._last_request_time = time.time()
                
                response = self._client.chat.completions.create(
                    model=self._model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.3,  # Lower for more deterministic output
                    max_tokens=1500,  # Higher limit for reasoning models
                )
                
                # Validate response structure
                if not response.choices:
                    logger.error(f"LLM returned no choices. Response: {response}")
                    raise LLMResponseError("No choices in LLM response")
                
                # Nebius API may use reasoning_content instead of content
                message = response.choices[0].message
                content = message.content or getattr(message, 'reasoning_content', None)
                
                if not content or not content.strip():
                    logger.error(f"LLM returned empty content. Full response: {response}")
                    raise LLMResponseError("Empty response from LLM")
                
                return content.strip()
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Classify the error
                if "quota" in error_str or "429" in error_str or "rate_limit" in error_str:
                    logger.warning(f"Quota/rate limit hit: {e}")
                    if self._rotate_api_key():
                        self._configure_client()
                        continue
                    raise LLMQuotaExhaustedError(str(e)) from e
                
                elif "rate" in error_str:
                    # Temporary rate limit - backoff and retry
                    wait = RETRY_BACKOFF_BASE ** attempt
                    logger.warning(f"Rate limit, retry in {wait}s: {e}")
                    time.sleep(wait)
                    continue
                
                elif any(x in error_str for x in ["network", "connection", "timeout"]):
                    raise LLMNetworkError(str(e)) from e
                
                elif attempt < MAX_RETRIES - 1:
                    # Unknown error, retry with backoff
                    wait = RETRY_BACKOFF_BASE ** attempt
                    logger.warning(f"LLM error, retry in {wait}s: {e}")
                    time.sleep(wait)
                    continue
                
                else:
                    raise LLMResponseError(str(e)) from e
        
        raise LLMResponseError("Max retries exceeded")

    def _parse_json_response(self, text: str) -> dict[str, Any]:
        """
        Parse JSON from LLM response, handling common issues.
        
        Args:
            text: Raw LLM response text
            
        Returns:
            Parsed JSON dict
            
        Raises:
            LLMResponseError: If parsing fails
        """
        # Try to extract JSON from response
        # Handle cases where LLM includes markdown code blocks
        json_match = re.search(r'```json?\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        
        # Handle cases where JSON is wrapped in other text
        brace_start = text.find('{')
        brace_end = text.rfind('}')
        if brace_start != -1 and brace_end != -1:
            text = text[brace_start:brace_end + 1]
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise LLMResponseError(f"Failed to parse JSON: {e}\nRaw: {text[:200]}") from e

    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        """Clamp a value to a range."""
        return max(min_val, min(max_val, value))

    def generate_citizen_reaction(
        self,
        citizen: "Citizen",
        current_state: "CitizenState",
        policy: "Policy",
        step: int,
    ) -> LLMReactionResult:
        """
        Generate a citizen's reaction to a policy using the LLM.
        
        Args:
            citizen: The citizen's static attributes
            current_state: The citizen's current state
            policy: The policy being simulated
            step: Current simulation step
            
        Returns:
            LLMReactionResult with validated deltas and explanation
            
        Raises:
            LLMQuotaExhaustedError: If all API keys are exhausted
            LLMResponseError: If response cannot be parsed
            LLMNetworkError: If network issues prevent API access
        """
        # Build user prompt
        user_prompt = CITIZEN_REACTION_USER_PROMPT.format(
            age=citizen.age,
            gender=citizen.gender,
            income_level=citizen.income_level.value,
            city_zone=citizen.city_zone.value,
            education_years=citizen.education_years,
            profession=citizen.profession,
            family_size=citizen.family_size,
            political_view=citizen.political_view.value,
            risk_tolerance=citizen.risk_tolerance,
            openness=citizen.openness_to_change,
            step=step,
            happiness=current_state.happiness,
            support=current_state.policy_support,
            income=current_state.income,
            policy_title=policy.title,
            policy_domain=policy.domain.value,
            policy_description=policy.description,
        )
        
        # Make request with system and user prompts
        raw_response = self._make_request(CITIZEN_REACTION_SYSTEM_PROMPT, user_prompt)
        
        # Parse response
        data = self._parse_json_response(raw_response)
        
        # Extract and validate fields
        try:
            delta_happiness = self._clamp(
                float(data.get("delta_happiness", 0)),
                *DELTA_HAPPINESS_RANGE,
            )
            delta_support = self._clamp(
                float(data.get("delta_support", 0)),
                *DELTA_SUPPORT_RANGE,
            )
            delta_income_pct = self._clamp(
                float(data.get("delta_income_pct", 0)),
                *DELTA_INCOME_PCT_RANGE,
            )
            explanation = str(data.get("explanation", ""))[:200]
            
        except (ValueError, TypeError) as e:
            raise LLMResponseError(f"Invalid numeric values in response: {e}") from e
        
        return LLMReactionResult(
            delta_happiness=delta_happiness,
            delta_support=delta_support,
            delta_income_pct=delta_income_pct,
            explanation=explanation,
            raw_response=raw_response,
        )

    def generate_summary_insight(
        self,
        policy: "Policy",
        metrics: dict[str, float],
    ) -> LLMInsightResult:
        """
        Generate a summary insight for simulation results.
        
        Args:
            policy: The policy that was simulated
            metrics: Dictionary with keys:
                - initial_happiness, final_happiness, happiness_change
                - initial_support, final_support, support_change
                - initial_income, final_income, income_change
                - initial_gap, final_gap, gap_change
            
        Returns:
            LLMInsightResult with insight text and key factors
            
        Raises:
            LLMQuotaExhaustedError: If all API keys are exhausted
            LLMResponseError: If response cannot be parsed
        """
        user_prompt = SUMMARY_INSIGHT_USER_PROMPT.format(
            policy_title=policy.title,
            policy_domain=policy.domain.value,
            initial_happiness=metrics.get("initial_happiness", 0),
            final_happiness=metrics.get("final_happiness", 0),
            happiness_change=metrics.get("happiness_change", 0),
            initial_support=metrics.get("initial_support", 0),
            final_support=metrics.get("final_support", 0),
            support_change=metrics.get("support_change", 0),
            initial_income=metrics.get("initial_income", 0),
            final_income=metrics.get("final_income", 0),
            income_change=metrics.get("income_change", 0) / max(metrics.get("initial_income", 1), 1),
            initial_gap=metrics.get("initial_gap", 0),
            final_gap=metrics.get("final_gap", 0),
            gap_change=metrics.get("gap_change", 0),
        )
        
        raw_response = self._make_request(SUMMARY_INSIGHT_SYSTEM_PROMPT, user_prompt)
        data = self._parse_json_response(raw_response)
        
        insight = str(data.get("insight", ""))[:300]
        key_factors = data.get("key_factors", [])
        
        # Ensure key_factors is a list of strings
        if not isinstance(key_factors, list):
            key_factors = []
        key_factors = [str(f)[:100] for f in key_factors[:3]]
        
        return LLMInsightResult(
            insight=insight,
            key_factors=key_factors,
            raw_response=raw_response,
        )

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1500,
        temperature: float = 0.3,
    ) -> str:
        """
        Generic method to generate LLM responses for any prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation (0.0-1.0)
            
        Returns:
            The LLM response text
            
        Raises:
            LLMQuotaExhaustedError: All keys exhausted
            LLMNetworkError: Network issues
            LLMResponseError: Invalid response
        """
        self._ensure_initialized()
        
        for attempt in range(MAX_RETRIES):
            try:
                self._enforce_rate_limit()
                self._last_request_time = time.time()
                
                response = self._client.chat.completions.create(
                    model=self._model_name,
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                
                # Validate response structure
                if not response.choices:
                    logger.error(f"LLM returned no choices. Response: {response}")
                    raise LLMResponseError("No choices in LLM response")
                
                # Nebius API may use reasoning_content instead of content
                message = response.choices[0].message
                content = message.content or getattr(message, 'reasoning_content', None)
                
                if not content or not content.strip():
                    logger.error(f"LLM returned empty content. Full response: {response}")
                    raise LLMResponseError("Empty response from LLM")
                
                return content.strip()
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Classify the error
                if "quota" in error_str or "429" in error_str or "rate_limit" in error_str:
                    logger.warning(f"Quota/rate limit hit: {e}")
                    if self._rotate_api_key():
                        self._configure_client()
                        continue
                    raise LLMQuotaExhaustedError(str(e)) from e
                
                elif "rate" in error_str:
                    # Temporary rate limit - backoff and retry
                    wait = RETRY_BACKOFF_BASE ** attempt
                    logger.warning(f"Rate limit, retry in {wait}s: {e}")
                    time.sleep(wait)
                    continue
                
                elif any(x in error_str for x in ["network", "connection", "timeout"]):
                    raise LLMNetworkError(str(e)) from e
                
                elif attempt < MAX_RETRIES - 1:
                    # Unknown error, retry with backoff
                    wait = RETRY_BACKOFF_BASE ** attempt
                    logger.warning(f"LLM error, retry in {wait}s: {e}")
                    time.sleep(wait)
                    continue
                
                else:
                    raise LLMResponseError(str(e)) from e
        
        raise LLMResponseError("Max retries exceeded")

    @property
    def is_available(self) -> bool:
        """Check if the LLM client is available (has non-exhausted keys)."""
        return len(self._exhausted_keys) < len(self._api_keys)

    def reset_exhausted_keys(self) -> None:
        """Reset all exhausted keys (for retry after quota reset)."""
        self._exhausted_keys.clear()
        self._client = None
        logger.info("Reset all exhausted API keys")


# =============================================================================
# Factory Function
# =============================================================================

def create_llm_client(api_keys: list[str]) -> LLMClient | None:
    """
    Factory function to create an LLM client safely.
    
    Args:
        api_keys: List of API keys
        
    Returns:
        LLMClient if keys are valid, None otherwise
    """
    try:
        return LLMClient(api_keys)
    except LLMNotConfiguredError:
        logger.info("LLM client not configured (no API keys)")
        return None


# =============================================================================
# Template-Based Fallback Explanations
# =============================================================================

def generate_rule_based_explanation(
    citizen: "Citizen",
    delta_happiness: float,
    delta_support: float,
    policy_domain: str,
) -> str:
    """
    Generate a template-based explanation when AI is unavailable.
    
    Args:
        citizen: The citizen
        delta_happiness: Happiness change
        delta_support: Support change
        policy_domain: Policy domain name
        
    Returns:
        Short factual explanation string
    """
    # Determine direction
    happiness_dir = "improved" if delta_happiness > 0 else "declined" if delta_happiness < 0 else "unchanged"
    support_dir = "increased" if delta_support > 0 else "decreased" if delta_support < 0 else "stable"
    
    # Select template based on citizen attributes
    income = citizen.income_level.value.lower()
    politics = citizen.political_view.value.lower()
    
    templates = [
        f"As a {income}-income {politics} citizen, happiness {happiness_dir} and policy support {support_dir}.",
        f"{policy_domain} policy: {income}-income household saw {happiness_dir} wellbeing.",
        f"This {politics} voter's support {support_dir} following the {policy_domain.lower()} changes.",
    ]
    
    # Deterministic selection based on citizen ID
    template_idx = citizen.id % len(templates)
    return templates[template_idx]


def generate_rule_based_summary_insight(
    policy_domain: str,
    happiness_change: float,
    support_change: float,
    gap_change: float,
) -> str:
    """
    Generate a template-based summary insight when AI is unavailable.
    
    Args:
        policy_domain: Policy domain name
        happiness_change: Overall happiness change
        support_change: Overall support change
        gap_change: Inequality gap change
        
    Returns:
        Short factual summary string
    """
    # Determine directions
    if happiness_change > 0.02:
        happiness_desc = "significantly improved"
    elif happiness_change > 0:
        happiness_desc = "slightly improved"
    elif happiness_change < -0.02:
        happiness_desc = "significantly declined"
    elif happiness_change < 0:
        happiness_desc = "slightly declined"
    else:
        happiness_desc = "remained stable"
    
    if gap_change > 0.01:
        inequality_desc = "Inequality widened"
    elif gap_change < -0.01:
        inequality_desc = "Inequality narrowed"
    else:
        inequality_desc = "Inequality remained stable"
    
    support_desc = "gained" if support_change > 0 else "lost" if support_change < 0 else "maintained"
    
    return (
        f"The {policy_domain} policy {happiness_desc} overall happiness and {support_desc} public support. "
        f"{inequality_desc} between income groups."
    )
