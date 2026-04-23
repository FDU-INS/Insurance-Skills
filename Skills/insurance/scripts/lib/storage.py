#!/usr/bin/env python3
"""Storage helpers for the insurance skill."""
import json
import os
import shutil
from datetime import datetime

WORKSPACE_ROOT = os.environ.get(
    "WORKSPACE_ROOT",
    os.path.expanduser("~/.openclaw/workspace"),
)
INSURANCE_DIR = os.path.join(WORKSPACE_ROOT, "memory", "insurance")


def ensure_dir() -> None:
    os.makedirs(INSURANCE_DIR, exist_ok=True)


def _path(filename: str) -> str:
    return os.path.join(INSURANCE_DIR, filename)


def load_json(filename: str, default: dict) -> dict:
    ensure_dir()
    filepath = _path(filename)

    if not os.path.exists(filepath):
        return default

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        corrupt_backup = f"{filepath}.corrupt.{timestamp}.bak"
        shutil.copy(filepath, corrupt_backup)
        return default


def save_json(filename: str, data: dict) -> None:
    ensure_dir()
    filepath = _path(filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
