"""CLI entry point for scan-organizer."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import click

from scan_organizer.config import SCANS_DIR
from scan_organizer.organize.manifest import find_entry, remove_entry


def _restore_file(filename: str) -> Path:
    """Undo a processed file — move it back to scans root.

    Returns the restored path. Exits with error JSON on failure.
    """
    entry = find_entry(filename)
    if not entry:
        click.echo(json.dumps({"error": f"No manifest entry for '{filename}'"}), err=True)
        sys.exit(1)

    dest_path = Path(entry["dest_path"])
    original_name = entry["original_name"]
    restore_path = SCANS_DIR / original_name

    if not dest_path.exists():
        click.echo(json.dumps({"error": f"File not found at {dest_path}"}), err=True)
        sys.exit(1)

    shutil.move(str(dest_path), str(restore_path))

    # Remove sidecar files
    stem = dest_path.stem
    parent = dest_path.parent
    for ext in (".md", ".meta.json"):
        sidecar = parent / f"{stem}{ext}"
        if sidecar.exists():
            sidecar.unlink()

    remove_entry(filename)
    return restore_path


@click.group()
def cli():
    """Scan Organizer — OCR, classify, and organize scanned PDFs."""


@cli.command()
@click.option("--dry-run", is_flag=True, help="Classify but don't move files.")
@click.option("--file", "file_path", type=click.Path(exists=True), help="Process a single file.")
@click.option("--force", is_flag=True, help="Re-process already-processed files.")
def process(dry_run: bool, file_path: str | None, force: bool):
    """Process unorganized scans."""
    from scan_organizer.pipeline import process_all, process_file

    if file_path:
        result = process_file(Path(file_path), dry_run=dry_run)
        output = {"processed": 1 if result["status"] == "processed" else 0, "skipped": 0, "errors": 1 if result["status"] == "error" else 0, "results": [result]}
    else:
        output = process_all(dry_run=dry_run, force=force)

    click.echo(json.dumps(output, indent=2))


@cli.command()
def status():
    """Report scan inbox state."""
    from scan_organizer.pipeline import get_status

    click.echo(json.dumps(get_status(), indent=2))


@cli.command()
@click.argument("filename")
def undo(filename: str):
    """Undo a processed file — move it back to scans root."""
    restore_path = _restore_file(filename)
    click.echo(json.dumps({"undone": filename, "restored_to": str(restore_path)}))


@cli.command()
@click.argument("filename")
def reclass(filename: str):
    """Undo and re-process a file to reclassify it."""
    from scan_organizer.pipeline import process_file

    restore_path = _restore_file(filename)
    result = process_file(restore_path)
    click.echo(json.dumps(result, indent=2))


if __name__ == "__main__":
    cli()
