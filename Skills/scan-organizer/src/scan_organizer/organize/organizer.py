"""Move classified PDFs into category subfolders with sidecar files."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import asdict
from pathlib import Path

from scan_organizer.classify.classifier import Classification
from scan_organizer.config import SCANS_DIR
from scan_organizer.organize.manifest import record_move


def _slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:60]


def _extract_id(filename: str) -> str:
    """Extract the numeric ID prefix from a scanner filename (e.g., '0001')."""
    match = re.match(r"(\d{4})", filename)
    return match.group(1) if match else filename.split(".")[0][:8]


def _parse_date_from_filename(filename: str) -> str | None:
    """Try to parse a date from the scanner filename format (YYMMDD)."""
    # Pattern: 0001_251219204406_001.pdf → 251219 = 2025-12-19
    match = re.search(r"_(\d{6})\d+_", filename)
    if match:
        raw = match.group(1)
        try:
            year = 2000 + int(raw[:2])
            month = int(raw[2:4])
            day = int(raw[4:6])
            if 1 <= month <= 12 and 1 <= day <= 31:
                return f"{year:04d}-{month:02d}-{day:02d}"
        except ValueError:
            pass
    return None


def organize(
    pdf_path: Path,
    markdown_text: str,
    classification: Classification,
    dry_run: bool = False,
) -> dict:
    """Move PDF to category subfolder and write sidecar files.

    Returns a result dict with source, destination, and metadata.
    """
    # Determine date — prefer classification, fallback to filename
    date = classification.date
    if not date:
        date = _parse_date_from_filename(pdf_path.name)
    if not date:
        date = "unknown-date"

    title_slug = _slugify(classification.title)
    original_id = _extract_id(pdf_path.name)

    dest_stem = f"{date}_{title_slug}_{original_id}"
    dest_dir = SCANS_DIR / classification.category
    dest_pdf = dest_dir / f"{dest_stem}.pdf"
    dest_md = dest_dir / f"{dest_stem}.md"
    dest_meta = dest_dir / f"{dest_stem}.meta.json"

    result = {
        "file": pdf_path.name,
        "category": classification.category,
        "title": classification.title,
        "date": date,
        "confidence": classification.confidence,
        "destination": str(dest_pdf),
        "dry_run": dry_run,
    }

    if dry_run:
        return result

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Move PDF
    shutil.move(str(pdf_path), str(dest_pdf))

    # Write markdown sidecar
    dest_md.write_text(markdown_text)

    # Write metadata sidecar
    meta = asdict(classification)
    meta["original_filename"] = pdf_path.name
    meta["dest_filename"] = dest_pdf.name
    dest_meta.write_text(json.dumps(meta, indent=2) + "\n")

    # Record in manifest
    record_move(
        original_path=pdf_path,
        dest_path=dest_pdf,
        category=classification.category,
        classification=meta,
    )

    return result
