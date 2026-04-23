"""Extract text from PDFs using Docling."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from docling.document_converter import DocumentConverter

from scan_organizer.config import MIN_PAGE_TEXT_CHARS


@dataclass
class PageResult:
    page_num: int
    text: str
    needs_ocr: bool


@dataclass
class DoclingResult:
    pages: list[PageResult] = field(default_factory=list)
    full_markdown: str = ""


def extract(pdf_path: Path) -> DoclingResult:
    """Parse a PDF with Docling and return per-page text plus OCR flags."""
    converter = DocumentConverter()
    conv_result = converter.convert(str(pdf_path))
    doc = conv_result.document

    full_md = doc.export_to_markdown()

    # Docling doesn't always expose per-page text cleanly.
    # We split by page-level items if available, otherwise treat as single page.
    pages: list[PageResult] = []

    # Try to get per-page text from document items
    page_texts: dict[int, list[str]] = {}
    for item in doc.iterate_items():
        # Items have a prov (provenance) list with page numbers
        if hasattr(item, "prov") and item.prov:
            page_no = item.prov[0].page_no
        else:
            page_no = 1
        text = item.export_to_markdown() if hasattr(item, "export_to_markdown") else str(item)
        page_texts.setdefault(page_no, []).append(text)

    if not page_texts:
        # Fallback: single page with all text
        pages.append(PageResult(
            page_num=1,
            text=full_md,
            needs_ocr=len(full_md.strip()) < MIN_PAGE_TEXT_CHARS,
        ))
    else:
        for page_num in sorted(page_texts.keys()):
            text = "\n\n".join(page_texts[page_num])
            pages.append(PageResult(
                page_num=page_num,
                text=text,
                needs_ocr=len(text.strip()) < MIN_PAGE_TEXT_CHARS,
            ))

    return DoclingResult(pages=pages, full_markdown=full_md)
