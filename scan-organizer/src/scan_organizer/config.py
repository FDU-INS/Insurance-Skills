"""Configuration — all values read from environment variables."""

import os
from pathlib import Path

# Directories
SCANS_DIR = Path(os.environ.get("SCANS_DIR", Path.home() / "scans"))
MANIFEST_PATH = SCANS_DIR / ".manifest.json"

# Categories
CATEGORIES = [
    "medical",
    "financial",
    "insurance",
    "tax",
    "legal",
    "personal",
    "household",
    "other",
]

# API endpoints (OpenAI-compatible)
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
CLASSIFY_URL = f"{OPENAI_BASE_URL}/chat/completions"

# OCR can optionally use a different provider
OCR_BASE_URL = os.environ.get("OCR_BASE_URL", OPENAI_BASE_URL)
OCR_API_KEY = os.environ.get("OCR_API_KEY", OPENAI_API_KEY)
OCR_URL = f"{OCR_BASE_URL}/chat/completions"

# Models
OCR_MODEL = os.environ.get("OCR_MODEL", "glm-ocr:latest")
CLASSIFY_MODEL = os.environ.get("CLASSIFY_MODEL", "qwen3:8b")
CLASSIFY_FALLBACK_MODEL = os.environ.get("CLASSIFY_FALLBACK_MODEL", "")

# Thresholds
MIN_PAGE_TEXT_CHARS = int(os.environ.get("MIN_PAGE_TEXT_CHARS", "50"))
MAX_CLASSIFY_CHARS = int(os.environ.get("MAX_CLASSIFY_CHARS", "28000"))

# Timeouts (seconds)
OCR_TIMEOUT = int(os.environ.get("OCR_TIMEOUT", "600"))
CLASSIFY_TIMEOUT = int(os.environ.get("CLASSIFY_TIMEOUT", "600"))
