"""
HealthSim — Level 2 Structural Checks
=======================================
Pure-Python validators for SKILL.md structural quality.
No API key needed. Each function returns a Callable[[str], bool]
compatible with the Criterion.check interface.
"""
import re
from pathlib import Path

_SKILLS = Path(__file__).resolve().parent.parent.parent / "skills"


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def has_section(heading: str):
    """Check that a markdown H2 section exists (case-insensitive)."""
    pattern = re.compile(rf"^##\s+.*{re.escape(heading)}", re.IGNORECASE | re.MULTILINE)
    def check(content: str) -> bool:
        return bool(pattern.search(content))
    return check


def has_frontmatter():
    """Check that YAML frontmatter (---) block exists."""
    def check(content: str) -> bool:
        return content.strip().startswith("---")
    return check


def frontmatter_has_field(field: str):
    """Check that a specific field exists in YAML frontmatter."""
    def check(content: str) -> bool:
        fm = _extract_frontmatter(content)
        return f"{field}:" in fm
    return check


def word_count_within(limit: int):
    """Check that total word count is at or below limit."""
    def check(content: str) -> bool:
        words = len(content.split())
        return words <= limit
    return check


def word_count_above(minimum: int):
    """Check that total word count meets a minimum threshold."""
    def check(content: str) -> bool:
        words = len(content.split())
        return words >= minimum
    return check


def min_worked_examples(n: int):
    """Check that at least N code blocks (```json, ```yaml, ```python) exist."""
    def check(content: str) -> bool:
        blocks = re.findall(r"```(?:json|yaml|python)", content)
        return len(blocks) >= n
    return check


def has_json_example():
    """Check that at least one JSON code block exists."""
    def check(content: str) -> bool:
        return "```json" in content
    return check


def has_negative_examples():
    """Check for negative example patterns (what NOT to do)."""
    def check(content: str) -> bool:
        lower = content.lower()
        return any(p in lower for p in [
            "not to generate", "not generate", "do not", "don't",
            "what not", "negative example", "never",
        ])
    return check


def has_edge_cases():
    """Check for edge case handling content."""
    def check(content: str) -> bool:
        lower = content.lower()
        return any(p in lower for p in [
            "edge case", "missing field", "invalid code", "partial data",
            "missing", "unknown", "invalid",
        ])
    return check


def mentions_all_code_systems(required: list[str]):
    """Check that all required code system names are mentioned."""
    def check(content: str) -> bool:
        upper = content.upper()
        return all(cs.upper() in upper for cs in required)
    return check


def all_md_links_resolve(skill_dir: str):
    """Check that all relative markdown links point to existing files."""
    def check(content: str) -> bool:
        base = _SKILLS / skill_dir
        links = re.findall(r"\[.*?\]\(((?!http|#)[^)]+\.md)\)", content)
        if not links:
            return True  # No links = vacuously true
        broken = []
        for link in links:
            target = (base / link).resolve()
            if not target.exists():
                broken.append(link)
        return len(broken) == 0
    return check


def sub_skill_files_exist(skill_dir: str, expected_files: list[str]):
    """Check that expected sub-skill .md files exist on disk."""
    def check(content: str) -> bool:
        base = _SKILLS / skill_dir
        return all((base / f).exists() for f in expected_files)
    return check


def has_cohort_table():
    """Check that a cohort routing table exists (| Cohort | ... | File |)."""
    def check(content: str) -> bool:
        return bool(re.search(r"\|\s*\*?\*?Cohort\*?\*?\s*\|", content, re.IGNORECASE))
    return check


def has_cross_product_links():
    """Check that cross-product integration links exist."""
    def check(content: str) -> bool:
        lower = content.lower()
        return "cross-product" in lower or "integration pattern" in lower
    return check


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _extract_frontmatter(content: str) -> str:
    """Extract YAML frontmatter block."""
    if not content.strip().startswith("---"):
        return ""
    parts = content.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


# ---------------------------------------------------------------------------
# L2 Shared Criteria (apply to ALL skills)
# ---------------------------------------------------------------------------

def get_shared_l2_criteria():
    """Return shared L2 criteria that apply to every skill domain."""
    from .eval_engine import Criterion, TestCase

    return [
        TestCase(
            id="l2-shared",
            name="Shared structural quality",
            category="structural",
            user_request="(structural check — reads SKILL.md directly)",
            criteria=[
                Criterion("l2-frontmatter", "Has YAML frontmatter block",
                          has_frontmatter()),
                Criterion("l2-frontmatter-name", "Frontmatter has name field",
                          frontmatter_has_field("name")),
                Criterion("l2-frontmatter-desc", "Frontmatter has description field",
                          frontmatter_has_field("description")),
                Criterion("l2-word-limit", "Word count ≤ 2000",
                          word_count_within(2000)),
                Criterion("l2-word-minimum", "Word count ≥ 500",
                          word_count_above(500)),
                Criterion("l2-safety-section", "Has Safety Guardrails section",
                          has_section("Safety Guardrails")),
                Criterion("l2-json-example", "Has at least one JSON example",
                          has_json_example()),
                Criterion("l2-negative-examples", "Has negative examples",
                          has_negative_examples()),
                Criterion("l2-edge-cases", "Has edge case handling",
                          has_edge_cases()),
                Criterion("l2-cross-product", "Has cross-product integration links",
                          has_cross_product_links()),
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# L2 Domain-Specific Criteria
# ---------------------------------------------------------------------------

def get_domain_l2_criteria(domain: str):
    """Return domain-specific L2 criteria for a given skill."""
    from .eval_engine import Criterion, TestCase

    specs = _DOMAIN_L2.get(domain)
    if not specs:
        return []

    return [
        TestCase(
            id=f"l2-{domain}",
            name=f"{domain} structural quality",
            category="structural",
            user_request="(structural check — reads SKILL.md directly)",
            criteria=specs,
        ),
    ]


def _make_domain_l2():
    """Build domain-specific L2 criteria. Deferred to avoid circular import."""
    from .eval_engine import Criterion

    return {
        "patientsim": [
            Criterion("l2-cohort-table", "Has cohort routing table",
                      has_cohort_table()),
            Criterion("l2-coherence-rules", "Has clinical coherence rules",
                      has_section("Clinical Coherence")),
            Criterion("l2-code-systems", "References ICD-10, CPT, LOINC, RxNorm",
                      mentions_all_code_systems(["ICD-10", "CPT", "LOINC", "RxNorm"])),
            Criterion("l2-links-resolve", "All markdown links resolve",
                      all_md_links_resolve("patientsim")),
        ],
        "membersim": [
            Criterion("l2-adjudication", "Has adjudication logic section",
                      has_section("Adjudication")),
            Criterion("l2-code-systems", "References ICD-10, CPT, HCPCS, NPI",
                      mentions_all_code_systems(["ICD-10", "CPT", "HCPCS", "NPI"])),
            Criterion("l2-cohort-table", "Has cohort routing table",
                      has_cohort_table()),
            Criterion("l2-links-resolve", "All markdown links resolve",
                      all_md_links_resolve("membersim")),
        ],
        "rxmembersim": [
            Criterion("l2-dur-types", "Has DUR alert type table",
                      has_section("DUR Alert")),
            Criterion("l2-reject-codes", "Has reject codes reference",
                      has_section("Reject Code")),
            Criterion("l2-code-systems", "References NDC, RxNorm, NPI, NCPDP",
                      mentions_all_code_systems(["NDC", "RxNorm", "NPI", "NCPDP"])),
            Criterion("l2-links-resolve", "All markdown links resolve",
                      all_md_links_resolve("rxmembersim")),
        ],
        "populationsim": [
            Criterion("l2-data-sources", "Has data sources section",
                      has_section("Data Source")),
            Criterion("l2-sdoh-codes", "References SVI, ADI, SDOH",
                      mentions_all_code_systems(["SVI", "ADI", "SDOH"])),
            Criterion("l2-examples", "Has at least 2 worked examples",
                      min_worked_examples(2)),
        ],
        "networksim": [
            Criterion("l2-data-sources", "Has data sources section",
                      has_section("Data Source")),
            Criterion("l2-codes", "References NPI, NUCC, FIPS",
                      mentions_all_code_systems(["NPI", "NUCC", "FIPS"])),
            Criterion("l2-validation", "Has validation rules",
                      has_section("Validation")),
            Criterion("l2-links-resolve", "All markdown links resolve",
                      all_md_links_resolve("networksim")),
        ],
        "trialsim": [
            Criterion("l2-sdtm-domains", "References SDTM domain routing",
                      mentions_all_code_systems(["SDTM", "DM", "AE", "LB"])),
            Criterion("l2-adam-mention", "References ADaM datasets",
                      mentions_all_code_systems(["ADaM", "ADSL"])),
            Criterion("l2-code-systems", "References MedDRA, LOINC, ATC",
                      mentions_all_code_systems(["MedDRA", "LOINC", "ATC"])),
            Criterion("l2-links-resolve", "All markdown links resolve",
                      all_md_links_resolve("trialsim")),
        ],
        "generation": [
            Criterion("l2-distribution-types", "Has distribution types section",
                      has_section("Distribution")),
            Criterion("l2-journey-patterns", "Has journey patterns section",
                      has_section("Journey")),
            Criterion("l2-product-integration", "References product integration",
                      has_section("Integration")),
        ],
    }


# Lazy init to avoid circular imports
_DOMAIN_L2 = None

def _ensure_domain_l2():
    global _DOMAIN_L2
    if _DOMAIN_L2 is None:
        _DOMAIN_L2 = _make_domain_l2()

# Patch get_domain_l2_criteria to lazy-init
_orig_get_domain = get_domain_l2_criteria

def get_domain_l2_criteria(domain: str):
    _ensure_domain_l2()
    return _orig_get_domain(domain)
