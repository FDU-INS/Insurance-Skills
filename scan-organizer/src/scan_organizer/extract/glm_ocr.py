"""OCR image-heavy pages via a vision model (OpenAI-compatible API)."""

from __future__ import annotations

import base64
import io
from pathlib import Path

import requests
from pdf2image import convert_from_path

from scan_organizer.config import OCR_API_KEY, OCR_MODEL, OCR_TIMEOUT, OCR_URL

OCR_PROMPT = (
    "OCR this document page. Extract all text preserving structure, "
    "tables, and formatting. Output as markdown."
)


def render_page_to_base64(pdf_path: Path, page_num: int, dpi: int = 200) -> str:
    """Render a single PDF page to a base64-encoded PNG."""
    images = convert_from_path(
        str(pdf_path),
        first_page=page_num,
        last_page=page_num,
        dpi=dpi,
    )
    buf = io.BytesIO()
    images[0].save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def ocr_page(pdf_path: Path, page_num: int) -> str:
    """Send a rendered page image to a vision model and return extracted text."""
    img_b64 = render_page_to_base64(pdf_path, page_num)

    payload = {
        "model": OCR_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": OCR_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_b64}",
                        },
                    },
                ],
            }
        ],
    }

    headers = {"Content-Type": "application/json"}
    if OCR_API_KEY:
        headers["Authorization"] = f"Bearer {OCR_API_KEY}"

    resp = requests.post(OCR_URL, json=payload, headers=headers, timeout=OCR_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]
