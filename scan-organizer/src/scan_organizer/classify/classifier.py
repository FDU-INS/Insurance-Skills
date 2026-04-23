"""Send text to an LLM for classification via OpenAI-compatible API."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

import requests

from scan_organizer.config import (
    CATEGORIES,
    CLASSIFY_FALLBACK_MODEL,
    CLASSIFY_MODEL,
    CLASSIFY_TIMEOUT,
    CLASSIFY_URL,
    MAX_CLASSIFY_CHARS,
    OPENAI_API_KEY,
)
from scan_organizer.classify.categories import build_prompt


@dataclass
class Classification:
    category: str = "other"
    confidence: float = 0.0
    title: str = "unknown"
    date: str | None = None
    keywords: list[str] = field(default_factory=list)
    model_used: str = ""
    error: str | None = None


def _call_model(model: str, text: str) -> dict:
    """Call a model via OpenAI-compatible endpoint and parse JSON response."""
    prompt = build_prompt(text[:MAX_CLASSIFY_CHARS])

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }

    headers = {"Content-Type": "application/json"}
    if OPENAI_API_KEY:
        headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"

    resp = requests.post(CLASSIFY_URL, json=payload, headers=headers, timeout=CLASSIFY_TIMEOUT)
    resp.raise_for_status()

    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    # Strip markdown fences if the model wraps its response
    content = content.strip()
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    # Handle thinking blocks (qwen3, deepseek, etc.)
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

    return json.loads(content)


def classify(text: str) -> Classification:
    """Classify document text. Tries primary model, falls back on failure."""
    models = [CLASSIFY_MODEL]
    if CLASSIFY_FALLBACK_MODEL:
        models.append(CLASSIFY_FALLBACK_MODEL)

    last_error = "no models configured"
    for model in models:
        try:
            result = _call_model(model, text)
            category = result.get("category", "other").lower()
            if category not in CATEGORIES:
                category = "other"
            return Classification(
                category=category,
                confidence=float(result.get("confidence", 0.5)),
                title=result.get("title", "unknown"),
                date=result.get("date"),
                keywords=result.get("keywords", []),
                model_used=model,
            )
        except Exception as exc:
            last_error = str(exc)
            continue

    return Classification(
        category="other",
        confidence=0.0,
        title="unknown",
        error=f"All models failed. Last error: {last_error}",
    )
