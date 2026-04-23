"""
RxMemberSim — Autoresearch Eval
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.eval_engine import (
    Criterion, TestCase, mentions_any, mentions_all, mentions_none,
    count_keywords, has_question, get_shared_cases, main_cli,
)

DOMAIN_CASES = [
    TestCase(id="rx-001", name="Pharmacy claim generation", category="domain_accuracy",
        user_request="Generate a pharmacy claim for a 30-day supply of metformin.",
        criteria=[
            Criterion("rx_details", "Includes prescription details",
                      lambda r: mentions_any(r, ["NDC", "metformin", "quantity", "days supply", "30"])),
            Criterion("pharmacy_claim", "Includes pharmacy claim fields",
                      lambda r: mentions_any(r, ["BIN", "PCN", "pharmacy", "claim"])),
            Criterion("pricing", "Includes pricing breakdown",
                      lambda r: mentions_any(r, ["ingredient cost", "dispensing fee", "copay", "paid"])),
        ]),
    TestCase(id="rx-002", name="DUR alert triggering", category="domain_accuracy",
        user_request="Generate a pharmacy claim that triggers a drug interaction alert.",
        criteria=[
            Criterion("dur_alert", "Produces a DUR alert",
                      lambda r: mentions_any(r, ["DUR", "drug utilization review", "alert", "interaction"])),
            Criterion("clinical_significance", "Includes clinical significance",
                      lambda r: mentions_any(r, ["severity", "clinical significance", "recommendation"])),
            Criterion("response_code", "Includes claim response",
                      lambda r: mentions_any(r, ["approved", "rejected", "warning", "response"])),
        ]),
    TestCase(id="rx-003", name="Formulary and tier assignment", category="domain_accuracy",
        user_request="What formulary tier is atorvastatin on?",
        criteria=[
            Criterion("tier_assignment", "Provides formulary tier",
                      lambda r: mentions_any(r, ["tier", "formulary", "preferred", "generic"])),
            Criterion("pa_requirement", "Notes PA requirements if applicable",
                      lambda r: mentions_any(r, ["prior authorization", "PA", "step therapy", "quantity limit"])),
        ]),
]

if __name__ == "__main__":
    main_cli("RxMemberSim", DOMAIN_CASES, domain_key="rxmembersim")
