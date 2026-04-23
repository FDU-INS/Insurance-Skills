"""
Finance Assistant Document Sorter
Classifies, renames, and sorts financial documents from a messy folder.
Supports PDF, images (JPG/PNG), and scanned documents (OCR fallback).
"""

from __future__ import annotations
import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Optional imports (graceful degradation) ────────────────────────────────────

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


# ── Document category definitions ─────────────────────────────────────────────

DOCUMENT_CATEGORIES = {
    "income": {
        "keywords": [
            "lohnsteuerbescheinigung", "bruttoarbeitslohn", "arbeitgeber",
            "bescheinigung für", "arbeitnehmer", "steuerklasse",
            "elstam", "lohnsteuerabzug",
        ],
        "subfolder": "01_Income/",
        "rename_pattern": "{year}_Lohnsteuerbescheinigung_{employer}.pdf",
        "extract_fields": ["gross", "lohnsteuer", "kv_ag", "rv_ag", "steuerklasse"],
    },
    "tax_office": {
        "keywords": [
            "steuerbescheid", "einkommensteuerbescheid", "festsetzung",
            "finanzamt", "steuererstattung", "nachzahlung", "einspruch",
        ],
        "subfolder": "09_TaxOffice/",
        "rename_pattern": "{year}_Steuerbescheid_{year_assessed}.pdf",
        "extract_fields": ["assessed_tax", "refund_or_payment", "assessment_year"],
    },
    "insurance_kv": {
        "keywords": [
            "krankenversicherung", "zusatzbeitrag", "pflegeversicherung",
            "beitragsbescheinigung", "krankenkasse", "aok", "tk", "barmer",
            "dak", "ikk", "hek", "hkk", "bkk",
        ],
        "subfolder": "02_Insurance/",
        "rename_pattern": "{year}_KV_{provider}_{amount}.pdf",
        "extract_fields": ["provider", "annual_amount", "zusatzbeitrag_rate"],
    },
    "insurance_life": {
        "keywords": [
            "lebensversicherung", "risikolebensversicherung", "berufsunfähigkeit",
            "bu-versicherung", "haftpflicht", "unfallversicherung",
        ],
        "subfolder": "02_Insurance/",
        "rename_pattern": "{year}_Insurance_{type}_{provider}.pdf",
        "extract_fields": ["provider", "annual_premium"],
    },
    "riester": {
        "keywords": [
            "riester", "zulagenantrag", "altersvorsorge-zulage",
            "zulagebescheinigung", "riester-rente",
        ],
        "subfolder": "04_Pension/Riester/",
        "rename_pattern": "{year}_Riester_{provider}.pdf",
        "extract_fields": ["contribution", "zulage", "provider"],
    },
    "ruerup": {
        "keywords": [
            "rürup", "basis-rente", "basisrente", "basisrentenvertrag",
        ],
        "subfolder": "04_Pension/Ruerup/",
        "rename_pattern": "{year}_Ruerup_{provider}.pdf",
        "extract_fields": ["contribution", "provider"],
    },
    "bav": {
        "keywords": [
            "betriebliche altersvorsorge", "bav", "direktversicherung",
            "pensionskasse", "pensionsfonds", "entgeltumwandlung",
        ],
        "subfolder": "04_Pension/bAV/",
        "rename_pattern": "{year}_bAV_{provider}.pdf",
        "extract_fields": ["contribution"],
    },
    "childcare": {
        "keywords": [
            "kindergarten", "kita", "kinderbetreuung", "tagesmutter",
            "kindertagesstätte", "krippe", "hort", "betreuungsentgelt",
            "elternbeitrag",
        ],
        "subfolder": "03_Family/Childcare/",
        "rename_pattern": "{year}_Kita_{month}_{amount}.pdf",
        "extract_fields": ["total_paid", "period", "child_name"],
    },
    "kindergeld": {
        "keywords": [
            "kindergeld", "familienkasse", "kinderfreibetrag",
            "kindergeldbescheid",
        ],
        "subfolder": "03_Family/Kindergeld/",
        "rename_pattern": "{year}_Kindergeld.pdf",
        "extract_fields": ["annual_amount"],
    },
    "investment": {
        "keywords": [
            "jahressteuerbescheinigung", "kapitalertrag", "depot",
            "dividende", "zinsen", "veräußerungsgewinn",
            "verlustverrechnungstopf", "vorabpauschale", "freistellungsauftrag",
        ],
        "subfolder": "08_Investments/",
        "rename_pattern": "{year}_Investment_{bank}.pdf",
        "extract_fields": ["kapitalertraege", "kest_paid", "soli_paid", "bank"],
    },
    "rental": {
        "keywords": [
            "nebenkostenabrechnung", "betriebskostenabrechnung", "mietvertrag",
            "grundsteuer", "hausgeld", "wohngeld", "verwalterabrechnung",
        ],
        "subfolder": "06_Property/Vermietung/",
        "rename_pattern": "{year}_Property_Rental_{amount}.pdf",
        "extract_fields": ["period", "total_amount"],
    },
    "handwerker": {
        "keywords": [
            "handwerkerleistung", "montage", "installation", "reparatur",
            "lohnanteil", "arbeitskosten", "handwerkerrechnung",
            "dienstleistung", "haushaltshilfe",
        ],
        "subfolder": "06_Property/Handwerker/",
        "rename_pattern": "{year}_Handwerker_{contractor}_{amount}.pdf",
        "extract_fields": ["labor_amount", "material_amount", "total_amount", "contractor"],
    },
    "equipment": {
        "keywords": [
            "rechnung", "kaufbeleg", "quittung",
            "laptop", "computer", "monitor", "drucker", "scanner",
            "schreibtisch", "bürostuhl", "headset", "webcam",
            "tastatur", "maus", "festplatte",
        ],
        "subfolder": "05_Equipment/",
        "rename_pattern": "{year}_Equipment_{item}_{amount}.pdf",
        "extract_fields": ["item_description", "amount", "date"],
    },
    "donation": {
        "keywords": [
            "spende", "zuwendungsbestätigung", "spendenquittung",
            "gemeinnützig", "spendenbescheinigung",
        ],
        "subfolder": "07_Donations/",
        "rename_pattern": "{year}_Donation_{org}_{amount}.pdf",
        "extract_fields": ["amount", "organization", "date"],
    },
    "pension_statement": {
        "keywords": [
            "rentenversicherung", "rentenauskunft", "rentenbescheid",
            "deutsche rentenversicherung", "drv", "renteninformation",
        ],
        "subfolder": "04_Pension/DRV/",
        "rename_pattern": "{year}_Renteninformation.pdf",
        "extract_fields": ["expected_pension", "contributions_to_date"],
    },
    "unknown": {
        "keywords": [],
        "subfolder": "00_NeedsReview/",
        "rename_pattern": "REVIEW_{original_name}.pdf",
        "extract_fields": [],
    },
}

# ── Text extraction ────────────────────────────────────────────────────────────

def extract_text(filepath: str) -> str:
    """Extract text from PDF or image. Returns empty string on failure."""
    path = Path(filepath)
    ext = path.suffix.lower()

    # PDF
    if ext == ".pdf":
        try:
            with open(filepath, "rb") as fh:
                header = fh.read(5)
            if header != b"%PDF-":
                return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            pass

        text = ""
        if HAS_PDFPLUMBER:
            try:
                with pdfplumber.open(filepath) as pdf:
                    for page in pdf.pages[:5]:  # First 5 pages
                        text += page.extract_text() or ""
                if text.strip():
                    return text
            except Exception:
                pass

        if HAS_PYPDF:
            try:
                reader = pypdf.PdfReader(filepath)
                for page in reader.pages[:5]:
                    text += page.extract_text() or ""
                if text.strip():
                    return text
            except Exception:
                pass

        # OCR fallback for scanned PDFs
        if HAS_OCR and HAS_PIL:
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(filepath, dpi=200, first_page=1, last_page=3)
                for img in images:
                    text += pytesseract.image_to_string(img, lang="deu") + "\n"
                return text
            except Exception:
                pass

    # Image
    elif ext in (".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".gif"):
        if HAS_OCR and HAS_PIL:
            try:
                img = Image.open(filepath)
                return pytesseract.image_to_string(img, lang="deu")
            except Exception:
                pass
        if HAS_PIL:
            return f"[Image: {path.name} — OCR not available, install pytesseract]"

    return ""


# ── Classification ─────────────────────────────────────────────────────────────

def classify_document(text: str, filename: str) -> str:
    """Return category key for a document given its text and filename."""
    combined = (text + " " + filename).lower()

    scores: dict[str, int] = {}
    for cat, config in DOCUMENT_CATEGORIES.items():
        if cat == "unknown":
            continue
        score = sum(1 for kw in config["keywords"] if kw in combined)
        if score > 0:
            scores[cat] = score

    if not scores:
        return "unknown"

    # Disambiguate overlapping categories
    best = max(scores, key=lambda c: scores[c])

    # Special rules
    if "income" in scores and "tax_office" in scores:
        best = "tax_office" if "bescheid" in combined else "income"
    if "equipment" in scores and "handwerker" in scores:
        best = "handwerker" if "lohnanteil" in combined or "montage" in combined else "equipment"

    return best


# ── Value extraction ───────────────────────────────────────────────────────────

def extract_year(text: str, filename: str) -> Optional[str]:
    """Extract most likely tax/document year from text or filename."""
    candidates = re.findall(r'\b(20[12]\d)\b', text + " " + filename)
    if not candidates:
        return str(datetime.now().year - 1)
    from collections import Counter
    most_common = Counter(candidates).most_common(1)[0][0]
    return most_common


def extract_amount(text: str) -> Optional[float]:
    """Extract the most prominent monetary amount from text."""
    # Look for patterns like €1.234,56 or 1.234,56 EUR or 1234.56
    patterns = [
        r'€\s*([\d.]+,\d{2})',       # €1.234,56
        r'([\d.]+,\d{2})\s*€',       # 1.234,56 €
        r'([\d.]+,\d{2})\s*EUR',     # German format
        r'\b(\d{1,6}\.\d{2})\b',     # 1234.56
    ]
    amounts = []
    for pattern in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            raw = m.group(1).replace(".", "").replace(",", ".")
            try:
                amounts.append(float(raw))
            except ValueError:
                pass
    if not amounts:
        return None
    # Return the largest amount (likely the main figure)
    return max(amounts)


def extract_entity(text: str, cat: str) -> str:
    """Extract entity name (employer, provider, org) from text."""
    text_lower = text.lower()

    # Known providers
    known = {
        "tk": "TK", "techniker": "TK", "barmer": "Barmer", "aok": "AOK",
        "dak": "DAK", "ikk": "IKK", "hek": "HEK",
        "allianz": "Allianz", "zurich": "Zurich", "generali": "Generali",
        "dws": "DWS", "union investment": "Union", "deka": "Deka",
        "comdirect": "Comdirect", "ing": "ING", "dkb": "DKB",
        "consorsbank": "Consors", "norisbank": "Norisbank",
        "deutsche bank": "DeutscheBank", "commerzbank": "Commerzbank",
        "sparkasse": "Sparkasse", "volksbank": "Volksbank",
        "unicef": "UNICEF", "unhcr": "UNHCR", "caritas": "Caritas",
        "rotes kreuz": "RotesKreuz", "wwf": "WWF",
    }
    for key, name in known.items():
        if key in text_lower:
            return name

    return "Unknown"


# ── Renaming ───────────────────────────────────────────────────────────────────

def build_new_name(
    cat: str,
    year: str,
    amount: Optional[float],
    entity: str,
    original_name: str,
    month: Optional[str] = None,
) -> str:
    """Build a standardised filename."""
    config = DOCUMENT_CATEGORIES[cat]
    pattern = config["rename_pattern"]
    ext = Path(original_name).suffix.lower() or ".pdf"

    amount_str = f"{int(amount)}" if amount else "0"
    month_str = month or "00"

    name = pattern.format(
        year=year,
        employer=entity,
        provider=entity,
        org=entity,
        bank=entity,
        contractor=entity,
        type=cat,
        item=entity,
        amount=amount_str,
        month=month_str,
        year_assessed=year,
        original_name=Path(original_name).stem,
    )
    if name.endswith(".pdf"):
        name = name[:-4] + ext
    # Sanitize
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'_+', '_', name)
    if not name.endswith(ext):
        name = Path(original_name).stem + "_sorted" + ext
    return name


# ── Main sort function ─────────────────────────────────────────────────────────

def sort_folder(
    folder_path: str,
    dry_run: bool = False,
    profile: Optional[dict] = None,
) -> dict:
    """
    Scan, classify, and sort all documents in folder_path.

    dry_run=True: show plan without moving files.
    Returns a manifest dict.
    """
    folder = Path(folder_path)
    if not folder.exists():
        return {"error": f"Folder not found: {folder_path}"}

    supported_ext = {".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".bmp"}
    files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in supported_ext]

    if not files:
        return {"error": "No supported files found in folder.", "files": []}

    manifest = {
        "folder": str(folder),
        "total_files": len(files),
        "classified": [],
        "unclassified": [],
        "moved": [],
        "errors": [],
        "missing_documents": [],
        "extracted_data": {},
    }

    for f in files:
        try:
            text = extract_text(str(f))
            cat = classify_document(text, f.name)
            year = extract_year(text, f.name)
            amount = extract_amount(text)
            entity = extract_entity(text, cat)
            new_name = build_new_name(cat, year or "2024", amount, entity, f.name)

            subfolder = DOCUMENT_CATEGORIES[cat]["subfolder"]
            dest_dir = folder / subfolder
            dest_path = dest_dir / new_name

            entry = {
                "original": f.name,
                "category": cat,
                "category_label": DOCUMENT_CATEGORIES[cat]["rename_pattern"],
                "new_name": new_name,
                "destination": str(dest_path),
                "year": year,
                "amount_found": amount,
                "entity": entity,
            }

            if cat == "unknown":
                manifest["unclassified"].append(entry)
            else:
                manifest["classified"].append(entry)

            # Extract key data
            if text:
                manifest["extracted_data"][f.name] = _extract_key_data(cat, text, year, amount)

            if not dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(dest_path))
                manifest["moved"].append({"from": f.name, "to": str(dest_path)})

        except Exception as e:
            manifest["errors"].append({"file": f.name, "error": str(e)})

    # Check for expected-but-missing documents based on profile
    if profile:
        manifest["missing_documents"] = _check_missing(manifest["classified"], profile)

    return manifest


def _extract_key_data(cat: str, text: str, year: Optional[str], amount: Optional[float]) -> dict:
    """Extract category-specific key figures from document text."""
    data = {"year": year, "primary_amount": amount}

    text_l = text.lower()

    if cat == "income":
        # Try to find specific fields
        gross_match = re.search(r'bruttoarbeitslohn[^\d]*([\d.]+,\d{2})', text_l)
        lohnsteuer_match = re.search(r'lohnsteuer[^\d]*([\d.]+,\d{2})', text_l)
        if gross_match:
            try:
                data["gross"] = float(gross_match.group(1).replace(".", "").replace(",", "."))
            except Exception:
                pass
        if lohnsteuer_match:
            try:
                data["lohnsteuer"] = float(lohnsteuer_match.group(1).replace(".", "").replace(",", "."))
            except Exception:
                pass
        data["type"] = "Lohnsteuerbescheinigung"

    elif cat == "investment":
        kest_match = re.search(r'kapitalertragsteuer[^\d]*([\d.]+,\d{2})', text_l)
        if kest_match:
            try:
                data["kest_paid"] = float(kest_match.group(1).replace(".", "").replace(",", "."))
            except Exception:
                pass
        data["type"] = "Jahressteuerbescheinigung"

    elif cat == "childcare":
        data["type"] = "Kita/Kinderbetreuung"
        if amount:
            data["deductible"] = round(min(amount, 6000) * 2 / 3, 2)

    elif cat == "handwerker":
        # Look for labor/material split
        labor_match = re.search(r'(lohn|arbeit)[^\d]*([\d.]+,\d{2})', text_l)
        if labor_match:
            try:
                data["labor_amount"] = float(labor_match.group(2).replace(".", "").replace(",", "."))
            except Exception:
                pass
        data["type"] = "Handwerkerrechnung §35a"

    elif cat == "donation":
        data["type"] = "Spendenquittung"
        data["simplified_proof_ok"] = (amount or 0) <= 300

    return data


def _check_missing(classified: list, profile: dict) -> list:
    """Based on profile, identify expected documents that weren't found."""
    found_cats = {e["category"] for e in classified}
    missing = []

    emp_type = profile.get("employment", {}).get("type", "")
    children = profile.get("family", {}).get("children", [])
    ins = profile.get("insurance", {})
    special = profile.get("special", {})

    if "angestellter" in emp_type and "income" not in found_cats:
        missing.append({
            "document": "Lohnsteuerbescheinigung",
            "why": "Required for employees — request from your employer or via ELSTER",
        })

    if not any(c in found_cats for c in ["insurance_kv", "insurance_life"]):
        missing.append({
            "document": "Krankenversicherung Beitragsbescheinigung",
            "why": "Deductible as Sonderausgaben — request from your Krankenkasse",
        })

    if ins.get("riester") and "riester" not in found_cats:
        missing.append({
            "document": "Riester Zulagebescheinigung",
            "why": "Needed for Anlage AV — request from your Riester provider",
        })

    if children and "childcare" not in found_cats:
        for child in children:
            if child.get("kita"):
                missing.append({
                    "document": "Kita Jahresrechnung / Betreuungsnachweis",
                    "why": "Deductible as Kinderbetreuungskosten §10 — request from Kita",
                })
                break

    if special.get("capital_income") and "investment" not in found_cats:
        missing.append({
            "document": "Jahressteuerbescheinigung (Bank/Broker)",
            "why": "Needed for Anlage KAP — request from each bank/broker",
        })

    return missing


# ── Display ────────────────────────────────────────────────────────────────────

def format_manifest_display(manifest: dict, dry_run: bool = False) -> str:
    """Return formatted manifest summary for user display."""
    lines = [
        f"{'📋 Document Sort Preview' if dry_run else '✅ Documents Sorted'}",
        f"Folder: {manifest.get('folder', '')}",
        f"Files found: {manifest.get('total_files', 0)}\n",
    ]

    classified = manifest.get("classified", [])
    if classified:
        lines.append(f"Classified ({len(classified)} files):")
        for entry in classified:
            lines.append(f"  {entry['original']}")
            lines.append(f"    → {entry['category'].upper()} | {entry['new_name']}")
            if entry.get("amount_found"):
                lines.append(f"       Amount: €{entry['amount_found']:,.2f}  Year: {entry.get('year', '?')}")

    unclassified = manifest.get("unclassified", [])
    if unclassified:
        lines.append(f"\n⚠️  Needs Review ({len(unclassified)} files):")
        for entry in unclassified:
            lines.append(f"  {entry['original']} → 00_NeedsReview/")

    missing = manifest.get("missing_documents", [])
    if missing:
        lines.append(f"\n📌 Expected but not found:")
        for m in missing:
            lines.append(f"  • {m['document']}")
            lines.append(f"    {m['why']}")

    errors = manifest.get("errors", [])
    if errors:
        lines.append(f"\n❌ Errors ({len(errors)}):")
        for e in errors:
            lines.append(f"  {e['file']}: {e['error']}")

    if dry_run:
        lines.append("\nThis is a preview. Files have NOT been moved yet.")
        lines.append("Reply 'yes' to confirm, or 'cancel' to abort.")

    return "\n".join(lines)


if __name__ == "__main__":
    import tempfile, os

    # Create a temp folder with dummy files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create dummy files
        Path(tmpdir, "document1.pdf").write_text("Lohnsteuerbescheinigung Bruttoarbeitslohn 65000,00 EUR")
        Path(tmpdir, "receipt.pdf").write_text("Rechnung Laptop Dell XPS 950,00 € Kaufbeleg")
        Path(tmpdir, "kita.pdf").write_text("Kita Elternbeitrag Kindergarten Betreuungsentgelt 250,00 €")
        Path(tmpdir, "random.pdf").write_text("Invoice random content")

        manifest = sort_folder(tmpdir, dry_run=True)
        print(format_manifest_display(manifest, dry_run=True))
