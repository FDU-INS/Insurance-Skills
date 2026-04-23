"""
Generation Engine — Autoresearch Eval
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.eval_engine import (
    Criterion, TestCase, mentions_any, mentions_all, mentions_none,
    count_keywords, has_question, get_shared_cases, main_cli,
)

DOMAIN_CASES = [
    TestCase(id="gen-001", name="Distribution-based generation", category="workflow",
        user_request="Generate 100 patients with age distribution matching Medicare Advantage.",
        criteria=[
            Criterion("distribution", "Uses statistical distributions",
                      lambda r: mentions_any(r, ["distribution", "statistical", "realistic", "match"])),
            Criterion("ma_demographics", "Reflects MA demographics",
                      lambda r: mentions_any(r, ["Medicare", "65", "elderly", "senior"])),
        ]),
]

if __name__ == "__main__":
    main_cli("Generation Engine", DOMAIN_CASES, domain_key="generation")
