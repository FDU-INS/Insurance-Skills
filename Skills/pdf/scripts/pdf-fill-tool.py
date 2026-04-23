#!/usr/bin/env python3
"""Wrapper for pdf-fill-overlay.js that accepts inline JSON config.

Used by Steward's tool executor. Writes config JSON to a temp file,
then calls pdf-fill-overlay.js with it.

Usage:
    pdf-fill-tool.py <source_pdf> <output_pdf> <config_json>

Example:
    pdf-fill-tool.py original.pdf filled.pdf '{"pageWidth": 612, "pageHeight": 792, "totalPages": 1, "pages": [{"page": 1, "fields": [{"x": 200, "y": 150, "text": "Hello", "fontSize": 10}]}]}'
"""

import json
import os
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILL_SCRIPT = os.path.join(SCRIPT_DIR, "pdf-fill-overlay.js")


def main():
    if len(sys.argv) < 4:
        print("Usage: pdf-fill-tool.py <source_pdf> <output_pdf> <config_json>", file=sys.stderr)
        sys.exit(1)

    source_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    config_json = sys.argv[3]

    # Validate JSON
    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing config JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Write config to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_path = f.name

    try:
        result = subprocess.run(
            ["node", FILL_SCRIPT, source_pdf, config_path, output_pdf],
            capture_output=True, text=True, cwd=SCRIPT_DIR
        )
        if result.stdout:
            sys.stdout.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)
        sys.exit(result.returncode)
    finally:
        os.unlink(config_path)


if __name__ == "__main__":
    main()
