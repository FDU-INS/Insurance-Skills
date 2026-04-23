"""Category definitions and classification prompt template."""

from scan_organizer.config import CATEGORIES

CATEGORY_DESCRIPTIONS = {
    "medical": "Medical records, lab results, prescriptions, doctor's notes, health insurance EOBs",
    "financial": "Bank statements, investment reports, receipts, invoices, pay stubs",
    "insurance": "Insurance policies, claims, coverage documents (non-health)",
    "tax": "Tax returns, W-2s, 1099s, tax correspondence, property tax bills",
    "legal": "Legal contracts, court documents, deeds, wills, notarized documents",
    "personal": "Personal correspondence, vital records (birth/marriage certificates), ID copies",
    "household": "Home repairs, warranties, appliance manuals, utility bills, HOA documents",
    "other": "Documents that don't clearly fit any other category",
}

CLASSIFY_PROMPT = """\
You are a document classifier. Analyze the following scanned document text and classify it.

## Categories
{categories}

## Document text
{text}

## Instructions
Respond with ONLY a JSON object (no markdown fences, no explanation):
{{"category": "<one of the categories above>", "confidence": <0.0-1.0>, "title": "<short descriptive title>", "date": "<YYYY-MM-DD or null if unknown>", "keywords": ["<keyword1>", "<keyword2>", ...]}}

Rules:
- Pick the single best category. If unsure, use "other".
- title should be a brief, descriptive slug (e.g., "lab-results", "bank-statement-december").
- date should be the document date if visible, otherwise null.
- keywords: 3-5 relevant terms from the document.
- confidence: your certainty in the classification (0.0 = no idea, 1.0 = certain).\
"""


def build_prompt(text: str) -> str:
    """Build the classification prompt with category taxonomy."""
    cat_lines = "\n".join(
        f"- **{cat}**: {CATEGORY_DESCRIPTIONS[cat]}" for cat in CATEGORIES
    )
    return CLASSIFY_PROMPT.format(categories=cat_lines, text=text)
