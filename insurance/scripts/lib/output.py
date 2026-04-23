#!/usr/bin/env python3
"""Standardized output helpers for the insurance skill."""
import json
from datetime import datetime
from typing import Optional


def ok(message: str, data: Optional[dict] = None) -> None:
    payload = {
        "status": "ok",
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "data": data or {},
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def error(message: str, data: Optional[dict] = None) -> None:
    payload = {
        "status": "error",
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "data": data or {},
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
