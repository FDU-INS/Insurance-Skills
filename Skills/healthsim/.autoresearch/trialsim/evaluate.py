"""
TrialSim — Autoresearch Eval
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.eval_engine import (
    Criterion, TestCase, mentions_any, mentions_all, mentions_none,
    count_keywords, has_question, get_shared_cases, main_cli,
)

DOMAIN_CASES = [
    TestCase(id="trial-001", name="CDISC SDTM output", category="domain_accuracy",
        user_request="Generate clinical trial data in SDTM format for a Phase 2 oncology study.",
        criteria=[
            Criterion("sdtm_domains", "References SDTM domains",
                      lambda r: mentions_any(r, ["DM", "AE", "LB", "EX", "SDTM"])),
            Criterion("oncology_context", "Appropriate for oncology trial",
                      lambda r: mentions_any(r, ["oncology", "tumor", "RECIST", "response"])),
            Criterion("study_design", "Reflects Phase 2 design",
                      lambda r: mentions_any(r, ["Phase 2", "randomiz", "arm", "dose"])),
        ]),
    TestCase(id="trial-002", name="ADaM derivation", category="domain_accuracy",
        user_request="Derive ADSL and ADTTE datasets from the SDTM data.",
        criteria=[
            Criterion("adsl", "Creates ADSL (subject-level) dataset",
                      lambda r: mentions_any(r, ["ADSL", "subject-level", "baseline"])),
            Criterion("adtte", "Creates time-to-event dataset",
                      lambda r: mentions_any(r, ["ADTTE", "time-to-event", "CNSR", "AVAL"])),
        ]),
]

if __name__ == "__main__":
    main_cli("TrialSim", DOMAIN_CASES, domain_key="trialsim")
