# scan-organizer

OCR, classify, and organize scanned PDFs into category subfolders using AI models.

Drop scanned PDFs into a watch directory. scan-organizer extracts text (Docling + vision OCR for image-heavy pages), classifies each document into a category using an LLM, and moves it into an organized folder structure with markdown and metadata sidecars.

## Features

- **Dual extraction** — Docling for structured PDFs, vision OCR for image-heavy pages
- **LLM classification** — Categorizes into: medical, financial, insurance, tax, legal, personal, household, other
- **Organized output** — Date-prefixed filenames, markdown text sidecars, JSON metadata
- **Manifest tracking** — Every move is logged with SHA-256 hash for auditability
- **Undo & reclassify** — Move files back or re-run classification
- **Any provider** — Works with Ollama, OpenAI, OpenRouter, LM Studio, or any OpenAI-compatible API
- **Memory safe** — Batch processing runs each file in a subprocess to prevent memory accumulation

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- An OpenAI-compatible API with a chat model and a vision model (e.g., local [Ollama](https://ollama.ai))
- `poppler-utils` (for `pdf2image` — `apt install poppler-utils` or `brew install poppler`)

## Setup

```bash
git clone <repo-url> && cd scan-organizer
cp .env.example .env
# Edit .env with your API endpoint and model names
```

### Example: Local Ollama

```bash
# .env
OPENAI_BASE_URL=http://localhost:11434/v1
CLASSIFY_MODEL=qwen3:8b
OCR_MODEL=minicpm-v:latest
```

### Example: OpenAI

```bash
# .env
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-...
CLASSIFY_MODEL=gpt-4o-mini
OCR_MODEL=gpt-4o
```

### Example: OpenRouter

```bash
# .env
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_API_KEY=sk-or-...
CLASSIFY_MODEL=qwen/qwen3-8b
OCR_MODEL=openai/gpt-4o
```

## Usage

```bash
# Check inbox status
uv run scan-organizer status

# Process all unorganized scans
uv run scan-organizer process

# Dry run — classify without moving
uv run scan-organizer process --dry-run

# Process a single file
uv run scan-organizer process --file ~/scans/document.pdf

# Undo (move back to inbox)
uv run scan-organizer undo 2025-12-20_lab-results_0003.pdf

# Reclassify
uv run scan-organizer reclass 2025-12-20_lab-results_0003.pdf
```

## Configuration

All settings are read from environment variables. Copy `.env.example` to `.env` and edit.

| Variable | Default | Description |
|---|---|---|
| `SCANS_DIR` | `~/scans` | Watch directory for unprocessed PDFs |
| `OPENAI_BASE_URL` | `http://localhost:11434/v1` | API base URL |
| `OPENAI_API_KEY` | *(empty)* | API key (not needed for local Ollama) |
| `CLASSIFY_MODEL` | `qwen3:8b` | Chat model for classification |
| `CLASSIFY_FALLBACK_MODEL` | *(empty)* | Optional fallback model |
| `OCR_MODEL` | `glm-ocr:latest` | Vision model for OCR |
| `OCR_BASE_URL` | *(same as OPENAI_BASE_URL)* | Optional separate OCR endpoint |
| `OCR_API_KEY` | *(same as OPENAI_API_KEY)* | Optional separate OCR key |
| `MIN_PAGE_TEXT_CHARS` | `50` | Pages below this threshold get OCR'd |
| `MAX_CLASSIFY_CHARS` | `28000` | Max text length sent to classifier |
| `OCR_TIMEOUT` | `600` | OCR request timeout (seconds) |
| `CLASSIFY_TIMEOUT` | `600` | Classification request timeout (seconds) |

## Output Structure

```
~/scans/
  medical/
    2025-12-20_lab-results_0003.pdf       # organized PDF
    2025-12-20_lab-results_0003.md        # extracted text
    2025-12-20_lab-results_0003.meta.json # classification metadata
  financial/
    ...
  .manifest.json                          # audit log for undo
```

## OpenClaw Integration

scan-organizer ships with a `SKILL.md` for [OpenClaw](https://docs.openclaw.ai). To add it as a skill:

1. **Symlink into workspace skills:**
   ```bash
   ln -s /path/to/scan-organizer ~/.openclaw/workspace/skills/scan-organizer
   ```

2. **Configure env vars** in `~/.openclaw/openclaw.json`:
   ```json5
   {
     skills: {
       entries: {
         "scan-organizer": {
           enabled: true,
           env: {
             OPENAI_BASE_URL: "http://your-server:11434/v1",
             CLASSIFY_MODEL: "qwen3:8b",
             OCR_MODEL: "glm-ocr:latest",
             SCANS_DIR: "/home/you/scans"
           }
         }
       }
     }
   }
   ```

3. **Restart the gateway:**
   ```bash
   systemctl --user restart openclaw-gateway
   ```

The agent can then process scans, check status, undo, and reclassify via chat.

## License

MIT
