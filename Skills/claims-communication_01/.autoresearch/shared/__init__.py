# Shared autoresearch eval infrastructure for HealthSim
from .eval_engine import (
    Criterion, TestCase, CaseResult,
    mentions_any, mentions_all, mentions_none, count_keywords, has_question,
    get_shared_cases, get_skill_content, run_evaluation, main_cli,
    CAT_DOMAIN, CAT_WORKFLOW, CAT_PHI, CAT_SAFETY, CAT_STRUCTURAL, CAT_RESPONSE,
)
from .reference_loader import (
    load_icd10_codes, load_loinc_codes, load_snomed_codes,
    load_oncology_drugs, load_code_system_oids, load_all_known_codes,
)
from .structural_checks import (
    get_shared_l2_criteria, get_domain_l2_criteria,
)
from .llm_harness import get_l3_cases
