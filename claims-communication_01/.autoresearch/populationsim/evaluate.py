"""
PopulationSim — Autoresearch Eval
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.eval_engine import (
    Criterion, TestCase, mentions_any, mentions_all, mentions_none,
    count_keywords, has_question, get_shared_cases, main_cli,
)

DOMAIN_CASES = [
    TestCase(id="pop-001", name="County-level population generation", category="workflow",
        user_request="Generate a population profile for Miami-Dade County.",
        criteria=[
            Criterion("county_reference", "Uses county-level reference data",
                      lambda r: mentions_any(r, ["county", "Miami-Dade", "Census", "reference"])),
            Criterion("sdoh_context", "Includes SDOH indicators",
                      lambda r: mentions_any(r, ["SVI", "SDOH", "ADI", "social", "vulnerability"])),
            Criterion("demographics", "Includes age/sex/race demographics",
                      lambda r: mentions_any(r, ["age", "sex", "race", "demographics", "distribution"])),
        ]),
    TestCase(id="pop-002", name="Health disparities modeling", category="domain_accuracy",
        user_request="How do health outcomes vary across SVI quartiles in our population?",
        criteria=[
            Criterion("svi_stratification", "Stratifies by SVI",
                      lambda r: mentions_any(r, ["SVI", "quartile", "vulnerability", "stratif"])),
            Criterion("outcome_variation", "Shows outcome differences",
                      lambda r: mentions_any(r, ["disparit", "difference", "higher", "lower", "variation"])),
        ]),
]

if __name__ == "__main__":
    main_cli("PopulationSim", DOMAIN_CASES, domain_key="populationsim")
