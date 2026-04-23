"""Track file moves in a manifest for auditability and undo."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from scan_organizer.config import MANIFEST_PATH


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> list[dict]:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return []


def save_manifest(entries: list[dict]) -> None:
    MANIFEST_PATH.write_text(json.dumps(entries, indent=2) + "\n")


def is_processed(pdf_path: Path) -> bool:
    """Check if a file (by name + hash) has already been processed."""
    sha = _sha256(pdf_path)
    for entry in load_manifest():
        if entry.get("sha256") == sha and entry.get("original_name") == pdf_path.name:
            return True
    return False


def record_move(
    original_path: Path,
    dest_path: Path,
    category: str,
    classification: dict,
) -> None:
    """Append a move record to the manifest."""
    entries = load_manifest()
    entries.append({
        "original_name": original_path.name,
        "original_path": str(original_path),
        "dest_path": str(dest_path),
        "category": category,
        "sha256": _sha256(dest_path),
        "classification": classification,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    })
    save_manifest(entries)


def find_entry(filename: str) -> dict | None:
    """Find a manifest entry by destination filename."""
    for entry in load_manifest():
        dest = Path(entry["dest_path"])
        if dest.name == filename:
            return entry
    return None


def remove_entry(filename: str) -> dict | None:
    """Remove a manifest entry (for undo). Returns the removed entry or None."""
    entries = load_manifest()
    for i, entry in enumerate(entries):
        dest = Path(entry["dest_path"])
        if dest.name == filename:
            removed = entries.pop(i)
            save_manifest(entries)
            return removed
    return None
