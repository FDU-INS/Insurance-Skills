#!/usr/bin/env python3
"""Schema and validation helpers for the insurance skill."""
import json
from datetime import datetime

ALLOWED_POLICY_TYPES = {
    "health",
    "home",
    "renters",
    "auto",
    "life",
    "umbrella",
    "business",
}

DEFAULT_POLICIES = {"policies": []}
DEFAULT_CLAIMS = {"claims": []}


def parse_json_object(raw: str, field_name: str) -> dict:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field_name} must be valid JSON.") from exc

    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a JSON object.")
    return value


def validate_date(date_str: str, field_name: str) -> str:
    if not date_str:
        return date_str
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field_name} must be in YYYY-MM-DD format.") from exc
    return date_str


def normalize_policy_type(policy_type: str) -> str:
    value = policy_type.strip().lower()
    if value not in ALLOWED_POLICY_TYPES:
        allowed = ", ".join(sorted(ALLOWED_POLICY_TYPES))
        raise ValueError(f"Invalid policy type '{policy_type}'. Allowed: {allowed}")
    return value


def non_negative_amount(value: float, field_name: str) -> float:
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative.")
    return value
