"""
MemberSim — Autoresearch Eval
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.eval_engine import (
    Criterion, TestCase, mentions_any, mentions_all, mentions_none,
    count_keywords, has_question, get_shared_cases, main_cli,
)

DOMAIN_CASES = [
    TestCase(id="mem-001", name="Professional claim generation", category="domain_accuracy",
        user_request="Create a professional claim for an office visit.",
        criteria=[
            Criterion("claim_header", "Includes claim header fields",
                      lambda r: mentions_any(r, ["claim", "provider", "NPI", "member"])),
            Criterion("cpt_codes", "Uses valid CPT codes",
                      lambda r: mentions_any(r, ["99213", "99214", "CPT", "office visit"])),
            Criterion("adjudication", "Includes adjudication detail",
                      lambda r: mentions_any(r, ["allowed", "paid", "copay", "coinsurance", "adjudicat"])),
        ]),
    TestCase(id="mem-002", name="Facility claim with DRG", category="domain_accuracy",
        user_request="Generate a facility claim for a 3-day inpatient stay.",
        criteria=[
            Criterion("facility_claim", "Creates facility/institutional claim",
                      lambda r: mentions_any(r, ["facility", "institutional", "UB-04", "inpatient"])),
            Criterion("drg", "Assigns appropriate DRG",
                      lambda r: mentions_any(r, ["DRG", "MS-DRG", "grouper"])),
            Criterion("room_board", "Includes room and board charges",
                      lambda r: mentions_any(r, ["room", "board", "per diem", "revenue code"])),
        ]),
    TestCase(id="mem-003", name="Accumulator tracking", category="domain_accuracy",
        user_request="Show the member's deductible and out-of-pocket accumulator status.",
        criteria=[
            Criterion("deductible", "Tracks deductible accumulation",
                      lambda r: mentions_any(r, ["deductible", "accumulated", "remaining"])),
            Criterion("oop_max", "Tracks out-of-pocket maximum",
                      lambda r: mentions_any(r, ["out-of-pocket", "OOP", "maximum", "MOOP"])),
        ]),
]

if __name__ == "__main__":
    main_cli("MemberSim", DOMAIN_CASES, domain_key="membersim")
