---
name: scan-organizer
description: OCR, classify, and organize scanned PDFs into category subfolders using AI vision and language models. Processes medical, financial, insurance, tax, legal, personal, and household documents.
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["uv"]},"install":[{"id":"uv-sync","kind":"uv","label":"Install scan-organizer dependencies"}]}}
---

# Scan Organizer

Processes scanned PDFs — extracts text (Docling + vision OCR), classifies by category using an LLM, and organizes into subfolders with markdown and metadata sidecars. Works with any OpenAI-compatible API (Ollama, OpenAI, OpenRouter, etc.).

## Categories

`medical`, `financial`, `insurance`, `tax`, `legal`, `personal`, `household`, `other`

## Commands

Run from the scan-organizer project directory.

### Process new scans
```bash
uv run scan-organizer process
```

### Dry run (classify without moving)
```bash
uv run scan-organizer process --dry-run
```

### Process a single file
```bash
uv run scan-organizer process --file /path/to/scan.pdf
```

### Force re-process all (including already processed)
```bash
uv run scan-organizer process --force
```

### Check inbox status
```bash
uv run scan-organizer status
```

### Undo a processed file (move back to inbox)
```bash
uv run scan-organizer undo <filename>
```

### Reclassify a file
```bash
uv run scan-organizer reclass <filename>
```

## Output Format

All commands output JSON to stdout. Progress messages go to stderr.

### Process output
```json
{"processed": 3, "skipped": 7, "errors": 0, "results": [{"file": "...", "category": "medical", "title": "...", "destination": "..."}]}
```

### Status output
```json
{"inbox_count": 10, "unprocessed": 3, "already_processed": 7, "categories": {"medical": 2, "financial": 3}}
```

## Architecture

1. **Extract** — Docling parses PDF structure and native text
2. **OCR** — Pages with sparse text are rendered to PNG and sent to a vision model
3. **Classify** — Merged text sent to a language model for categorization
4. **Organize** — PDF moved to `<scans_dir>/<category>/`, `.md` + `.meta.json` sidecars written

## File Organization

```
<scans_dir>/
  medical/
    2025-12-20_lab-results_0003.pdf
    2025-12-20_lab-results_0003.md
    2025-12-20_lab-results_0003.meta.json
  financial/
    ...
  .manifest.json    <- tracks all moves for undo
```

## Tips

- Run `status` first to see how many unprocessed scans are in the inbox
- Use `--dry-run` to preview classifications before moving files
- The manifest tracks all moves for auditability
- If a classification is wrong, use `reclass` to undo and re-process
