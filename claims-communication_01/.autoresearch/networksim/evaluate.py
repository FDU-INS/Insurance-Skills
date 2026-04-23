"""
NetworkSim — Autoresearch Eval
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.eval_engine import (
    Criterion, TestCase, mentions_any, mentions_all, mentions_none,
    count_keywords, has_question, get_shared_cases, main_cli,
)

DOMAIN_CASES = [
    TestCase(id="net-001", name="Provider network generation", category="workflow",
        user_request="Create a provider network for San Diego with PCPs and specialists.",
        criteria=[
            Criterion("provider_types", "Includes multiple provider types",
                      lambda r: mentions_any(r, ["PCP", "specialist", "primary care", "family medicine"])),
            Criterion("real_reference", "References real data sources (NPPES)",
                      lambda r: mentions_any(r, ["NPPES", "NPI", "real", "registry"])),
            Criterion("geography", "Scoped to requested geography",
                      lambda r: mentions_any(r, ["San Diego", "county", "ZIP", "geography"])),
        ]),
    TestCase(id="net-002", name="Network adequacy", category="domain_accuracy",
        user_request="Does our network meet CMS adequacy standards?",
        criteria=[
            Criterion("adequacy_standards", "References CMS network adequacy rules",
                      lambda r: mentions_any(r, ["adequacy", "CMS", "time", "distance", "ratio"])),
            Criterion("gap_identification", "Identifies gaps if present",
                      lambda r: mentions_any(r, ["gap", "shortage", "insufficient", "need"])),
        ]),
]

if __name__ == "__main__":
    main_cli("NetworkSim", DOMAIN_CASES, domain_key="networksim")
