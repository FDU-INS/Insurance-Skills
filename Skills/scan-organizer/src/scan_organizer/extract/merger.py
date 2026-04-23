"""Merge Docling and GLM-OCR outputs into unified markdown."""

from __future__ import annotations

from pathlib import Path

from scan_organizer.extract.docling_extractor import DoclingResult
from scan_organizer.extract.glm_ocr import ocr_page


def merge(pdf_path: Path, docling_result: DoclingResult) -> str:
    """Combine Docling text with GLM-OCR for low-text pages.

    Returns a single markdown string with page separators.
    """
    parts: list[str] = []

    for page in docling_result.pages:
        if page.needs_ocr:
            try:
                ocr_text = ocr_page(pdf_path, page.page_num)
            except Exception as exc:
                ocr_text = f"[OCR failed for page {page.page_num}: {exc}]"
            # Use OCR text if it's substantially better, otherwise keep what we have
            text = ocr_text if len(ocr_text.strip()) > len(page.text.strip()) else page.text
        else:
            text = page.text

        parts.append(text.strip())

    return "\n\n---\n\n".join(parts)
