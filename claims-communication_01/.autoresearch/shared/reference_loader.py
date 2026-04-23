"""
HealthSim — Reference Data Loader
==================================
Loads medical code reference CSVs into cached sets for O(1) code validation.
Used by Level 3 (LLM-in-the-loop) evals to verify generated codes are real.
"""
import csv
from functools import lru_cache
from pathlib import Path

_REFS = Path(__file__).resolve().parent.parent.parent / "references"
_CCDA = _REFS / "ccda"
_ONCO = _REFS / "oncology"


def _load_column(csv_path: Path, column: str) -> set[str]:
    """Load a single column from a CSV into a set of lowercase-stripped strings."""
    if not csv_path.exists():
        return set()
    codes = set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            val = row.get(column, "").strip()
            if val:
                codes.add(val)
    return codes


def _load_columns(csv_path: Path, columns: list[str]) -> set[str]:
    """Load multiple columns from a CSV into a single set."""
    if not csv_path.exists():
        return set()
    codes = set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for col in columns:
                val = row.get(col, "").strip()
                if val:
                    codes.add(val)
    return codes


@lru_cache(maxsize=1)
def load_icd10_codes() -> set[str]:
    """ICD-10-CM codes from C-CDA mappings + oncology reference."""
    codes = _load_column(_CCDA / "ccda-snomed-problem-mappings.csv", "icd10_code")
    codes |= _load_column(_ONCO / "oncology-icd10-codes.csv", "code")
    return codes


@lru_cache(maxsize=1)
def load_loinc_codes() -> set[str]:
    """LOINC codes from lab panels + vital signs + tumor markers."""
    codes = _load_columns(
        _CCDA / "ccda-loinc-lab-panels.csv", ["panel_loinc", "test_loinc"]
    )
    codes |= _load_column(_CCDA / "ccda-vital-signs-loinc.csv", "loinc_code")
    codes |= _load_column(_ONCO / "oncology-tumor-markers.csv", "loinc_code")
    return codes


@lru_cache(maxsize=1)
def load_snomed_codes() -> set[str]:
    """SNOMED CT codes from C-CDA problem mappings."""
    return _load_column(_CCDA / "ccda-snomed-problem-mappings.csv", "snomed_code")


@lru_cache(maxsize=1)
def load_oncology_drugs() -> set[str]:
    """Oncology drug names (generic + brand) from reference."""
    return _load_columns(
        _ONCO / "oncology-medications.csv", ["generic_name", "brand_name"]
    )


@lru_cache(maxsize=1)
def load_code_system_oids() -> set[str]:
    """Code system OIDs from C-CDA reference."""
    return _load_column(_CCDA / "ccda-code-systems.csv", "oid")


@lru_cache(maxsize=1)
def load_all_known_codes() -> dict[str, set[str]]:
    """Load all reference code sets into a single dict for convenience."""
    return {
        "icd10": load_icd10_codes(),
        "loinc": load_loinc_codes(),
        "snomed": load_snomed_codes(),
        "oncology_drugs": load_oncology_drugs(),
        "oids": load_code_system_oids(),
    }
