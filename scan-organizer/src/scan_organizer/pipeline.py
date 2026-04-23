"""Orchestrate: ingest → extract → classify → organize."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scan_organizer.classify.classifier import classify
from scan_organizer.config import SCANS_DIR
from scan_organizer.extract.docling_extractor import extract
from scan_organizer.extract.merger import merge
from scan_organizer.organize.manifest import is_processed
from scan_organizer.organize.organizer import organize

PROJECT_DIR = Path(__file__).resolve().parents[2]


def find_unprocessed() -> list[Path]:
    """Find PDF files in the scans root that haven't been processed yet."""
    pdfs = sorted(SCANS_DIR.glob("*.pdf"))
    return [p for p in pdfs if not is_processed(p)]


def process_file(pdf_path: Path, dry_run: bool = False) -> dict:
    """Run the full pipeline on a single PDF.

    Returns a result dict with processing details.
    """
    result = {"file": pdf_path.name, "status": "unknown"}

    try:
        # 1. Extract text with Docling
        print(f"  Extracting text from {pdf_path.name}...", file=sys.stderr)
        docling_result = extract(pdf_path)

        # 2. Merge with GLM-OCR for image-heavy pages
        print(f"  Merging text (OCR for {sum(1 for p in docling_result.pages if p.needs_ocr)} pages)...", file=sys.stderr)
        markdown_text = merge(pdf_path, docling_result)

        # 3. Classify
        print(f"  Classifying...", file=sys.stderr)
        classification = classify(markdown_text)
        print(f"  → {classification.category} ({classification.confidence:.0%}): {classification.title}", file=sys.stderr)

        # 4. Organize
        result = organize(pdf_path, markdown_text, classification, dry_run=dry_run)
        result["status"] = "processed"

    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)
        print(f"  ERROR: {exc}", file=sys.stderr)

    return result


def _subprocess_one(pdf_path: Path, dry_run: bool) -> dict:
    """Process a single file in a fresh subprocess to free memory between files."""
    cmd = ["uv", "run", "scan-organizer", "process", "--file", str(pdf_path)]
    if dry_run:
        cmd.append("--dry-run")

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(PROJECT_DIR),
            timeout=900,
        )
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {pdf_path.name} exceeded 15 minutes, skipping", file=sys.stderr)
        return {"file": pdf_path.name, "status": "error", "error": "timeout (15m)"}

    # Forward stderr (progress messages) to our stderr
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)

    if proc.returncode != 0:
        return {"file": pdf_path.name, "status": "error", "error": f"exit code {proc.returncode}"}

    try:
        output = json.loads(proc.stdout)
        results = output.get("results", [])
        return results[0] if results else {"file": pdf_path.name, "status": "error", "error": "no result"}
    except (json.JSONDecodeError, IndexError):
        return {"file": pdf_path.name, "status": "error", "error": "bad output"}


def process_all(dry_run: bool = False, force: bool = False) -> dict:
    """Process all unprocessed PDFs, each in its own subprocess for memory safety."""
    all_pdfs = sorted(SCANS_DIR.glob("*.pdf"))
    unprocessed = all_pdfs if force else find_unprocessed()
    skipped = len(all_pdfs) - len(unprocessed)

    results = []
    errors = 0

    for i, pdf_path in enumerate(unprocessed, 1):
        print(f"\n[{i}/{len(unprocessed)}] Processing {pdf_path.name}...", file=sys.stderr)
        result = _subprocess_one(pdf_path, dry_run=dry_run)
        results.append(result)
        if result.get("status") == "error":
            errors += 1

    return {
        "processed": len(results) - errors,
        "skipped": skipped,
        "errors": errors,
        "results": results,
    }


def get_status() -> dict:
    """Report on the current state of the scans directory."""
    all_pdfs = sorted(SCANS_DIR.glob("*.pdf"))
    unprocessed = find_unprocessed()
    already = len(all_pdfs) - len(unprocessed)

    # Count files in category subdirs
    categories: dict[str, int] = {}
    for subdir in SCANS_DIR.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("."):
            count = len(list(subdir.glob("*.pdf")))
            if count > 0:
                categories[subdir.name] = count

    return {
        "inbox_count": len(all_pdfs),
        "unprocessed": len(unprocessed),
        "already_processed": already,
        "categories": categories,
    }
