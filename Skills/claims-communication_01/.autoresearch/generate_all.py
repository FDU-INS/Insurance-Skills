#!/usr/bin/env python3
"""HealthSim Eval Factory — Generates evals for all 8 skill domains.

Generates Level 1 (keyword), Level 2 (structural), and Level 3 (LLM) evals.
L2/L3 are loaded dynamically from shared modules — no per-domain config needed.
"""
import sys
from pathlib import Path

DOMAINS = {
    "patientsim": {
        "display_name": "PatientSim",
        "test_cases": [
            ("pat-001", "Diabetic patient generation", "domain_accuracy",
             "Generate a 65-year-old diabetic patient with hypertension.",
             [("demographics", "Includes age-appropriate demographics",
               ["65", "age", "demographics", "name"]),
              ("diabetes_dx", "Assigns diabetes ICD-10 code",
               ["E11", "diabetes", "ICD-10"]),
              ("hypertension_dx", "Assigns hypertension code",
               ["I10", "hypertension"]),
              ("medications", "Includes appropriate medications",
               ["metformin", "lisinopril", "medication"]),
              ("labs", "Includes relevant lab results",
               ["A1C", "lab", "BMP", "glucose"])]),
            ("pat-002", "Encounter types", "workflow",
             "Create an inpatient encounter for pneumonia.",
             [("inpatient_setting", "Sets inpatient encounter type",
               ["inpatient", "admission", "hospital"]),
              ("pneumonia_dx", "Assigns pneumonia diagnosis",
               ["J18", "pneumonia", "respiratory"]),
              ("procedures", "Includes appropriate procedures",
               ["CPT", "procedure", "chest", "imaging"])]),
            ("pat-003", "Clinical cohort routing", "workflow",
             "Generate a heart failure cohort of 20 patients.",
             [("cohort_size", "Creates requested number of patients",
               ["20", "cohort", "patients", "group"]),
              ("hf_diagnosis", "Assigns heart failure diagnoses",
               ["I50", "heart failure", "CHF"]),
              ("clinical_realism", "Includes realistic comorbidities",
               ["comorbid", "hypertension", "diabetes", "CKD", "renal"])]),
            ("pat-004", "Output format compliance", "domain_accuracy",
             "Generate a patient record in FHIR R4 format.",
             [("fhir_mention", "References FHIR R4 format",
               ["FHIR", "R4", "resource", "Bundle"]),
              ("structured_output", "Produces structured data",
               ["Patient", "Encounter", "Condition", "resource"])]),
        ],
    },
    "membersim": {
        "display_name": "MemberSim",
        "test_cases": [
            ("mem-001", "Professional claim generation", "domain_accuracy",
             "Create a professional claim for an office visit.",
             [("claim_header", "Includes claim header fields",
               ["claim", "provider", "NPI", "member"]),
              ("cpt_codes", "Uses valid CPT codes",
               ["99213", "99214", "CPT", "office visit"]),
              ("adjudication", "Includes adjudication detail",
               ["allowed", "paid", "copay", "coinsurance", "adjudicat"])]),
            ("mem-002", "Facility claim with DRG", "domain_accuracy",
             "Generate a facility claim for a 3-day inpatient stay.",
             [("facility_claim", "Creates facility/institutional claim",
               ["facility", "institutional", "UB-04", "inpatient"]),
              ("drg", "Assigns appropriate DRG",
               ["DRG", "MS-DRG", "grouper"]),
              ("room_board", "Includes room and board charges",
               ["room", "board", "per diem", "revenue code"])]),
            ("mem-003", "Accumulator tracking", "domain_accuracy",
             "Show the member's deductible and out-of-pocket accumulator status.",
             [("deductible", "Tracks deductible accumulation",
               ["deductible", "accumulated", "remaining"]),
              ("oop_max", "Tracks out-of-pocket maximum",
               ["out-of-pocket", "OOP", "maximum", "MOOP"])]),
        ],
    },
    "rxmembersim": {
        "display_name": "RxMemberSim",
        "test_cases": [
            ("rx-001", "Pharmacy claim generation", "domain_accuracy",
             "Generate a pharmacy claim for a 30-day supply of metformin.",
             [("rx_details", "Includes prescription details",
               ["NDC", "metformin", "quantity", "days supply", "30"]),
              ("pharmacy_claim", "Includes pharmacy claim fields",
               ["BIN", "PCN", "pharmacy", "claim"]),
              ("pricing", "Includes pricing breakdown",
               ["ingredient cost", "dispensing fee", "copay", "paid"])]),
            ("rx-002", "DUR alert triggering", "domain_accuracy",
             "Generate a pharmacy claim that triggers a drug interaction alert.",
             [("dur_alert", "Produces a DUR alert",
               ["DUR", "drug utilization review", "alert", "interaction"]),
              ("clinical_significance", "Includes clinical significance",
               ["severity", "clinical significance", "recommendation"]),
              ("response_code", "Includes claim response",
               ["approved", "rejected", "warning", "response"])]),
            ("rx-003", "Formulary and tier assignment", "domain_accuracy",
             "What formulary tier is atorvastatin on?",
             [("tier_assignment", "Provides formulary tier",
               ["tier", "formulary", "preferred", "generic"]),
              ("pa_requirement", "Notes PA requirements if applicable",
               ["prior authorization", "PA", "step therapy", "quantity limit"])]),
        ],
    },
    "trialsim": {
        "display_name": "TrialSim",
        "test_cases": [
            ("trial-001", "CDISC SDTM output", "domain_accuracy",
             "Generate clinical trial data in SDTM format for a Phase 2 oncology study.",
             [("sdtm_domains", "References SDTM domains",
               ["DM", "AE", "LB", "EX", "SDTM"]),
              ("oncology_context", "Appropriate for oncology trial",
               ["oncology", "tumor", "RECIST", "response"]),
              ("study_design", "Reflects Phase 2 design",
               ["Phase 2", "randomiz", "arm", "dose"])]),
            ("trial-002", "ADaM derivation", "domain_accuracy",
             "Derive ADSL and ADTTE datasets from the SDTM data.",
             [("adsl", "Creates ADSL (subject-level) dataset",
               ["ADSL", "subject-level", "baseline"]),
              ("adtte", "Creates time-to-event dataset",
               ["ADTTE", "time-to-event", "CNSR", "AVAL"])]),
        ],
    },
    "populationsim": {
        "display_name": "PopulationSim",
        "test_cases": [
            ("pop-001", "County-level population generation", "workflow",
             "Generate a population profile for Miami-Dade County.",
             [("county_reference", "Uses county-level reference data",
               ["county", "Miami-Dade", "Census", "reference"]),
              ("sdoh_context", "Includes SDOH indicators",
               ["SVI", "SDOH", "ADI", "social", "vulnerability"]),
              ("demographics", "Includes age/sex/race demographics",
               ["age", "sex", "race", "demographics", "distribution"])]),
            ("pop-002", "Health disparities modeling", "domain_accuracy",
             "How do health outcomes vary across SVI quartiles in our population?",
             [("svi_stratification", "Stratifies by SVI",
               ["SVI", "quartile", "vulnerability", "stratif"]),
              ("outcome_variation", "Shows outcome differences",
               ["disparit", "difference", "higher", "lower", "variation"])]),
        ],
    },
    "networksim": {
        "display_name": "NetworkSim",
        "test_cases": [
            ("net-001", "Provider network generation", "workflow",
             "Create a provider network for San Diego with PCPs and specialists.",
             [("provider_types", "Includes multiple provider types",
               ["PCP", "specialist", "primary care", "family medicine"]),
              ("real_reference", "References real data sources (NPPES)",
               ["NPPES", "NPI", "real", "registry"]),
              ("geography", "Scoped to requested geography",
               ["San Diego", "county", "ZIP", "geography"])]),
            ("net-002", "Network adequacy", "domain_accuracy",
             "Does our network meet CMS adequacy standards?",
             [("adequacy_standards", "References CMS network adequacy rules",
               ["adequacy", "CMS", "time", "distance", "ratio"]),
              ("gap_identification", "Identifies gaps if present",
               ["gap", "shortage", "insufficient", "need"])]),
        ],
    },
    "generation": {
        "display_name": "Generation Engine",
        "test_cases": [
            ("gen-001", "Distribution-based generation", "workflow",
             "Generate 100 patients with age distribution matching Medicare Advantage.",
             [("distribution", "Uses statistical distributions",
               ["distribution", "statistical", "realistic", "match"]),
              ("ma_demographics", "Reflects MA demographics",
               ["Medicare", "65", "elderly", "senior"])]),
        ],
    },
}


def generate_evaluate_py(domain_key, config):
    test_case_code = []
    for tc_id, tc_name, tc_cat, tc_req, tc_crit in config["test_cases"]:
        criteria_code = []
        for cn, cd, ckw in tc_crit:
            kl = ", ".join(f'"{k}"' for k in ckw)
            fn = "mentions_none" if ("NOT" in cd or cn.startswith("no_")) else "mentions_any"
            criteria_code.append(f'            Criterion("{cn}", "{cd}",\n                      lambda r: {fn}(r, [{kl}])),')
        cs = "\n".join(criteria_code)
        test_case_code.append(f'    TestCase(id="{tc_id}", name="{tc_name}", category="{tc_cat}",\n'
            f'        user_request="{tc_req}",\n        criteria=[\n{cs}\n        ]),')
    cases = "\n".join(test_case_code)
    return f'"""\n{config["display_name"]} — Autoresearch Eval\n"""\n'  \
        f'import sys\nfrom pathlib import Path\n'  \
        f'sys.path.insert(0, str(Path(__file__).resolve().parent.parent))\n'  \
        f'from shared.eval_engine import (\n'  \
        f'    Criterion, TestCase, mentions_any, mentions_all, mentions_none,\n'  \
        f'    count_keywords, has_question, get_shared_cases, main_cli,\n)\n\n'  \
        f'DOMAIN_CASES = [\n{cases}\n]\n\n'  \
        f'if __name__ == "__main__":\n    main_cli("{config["display_name"]}", DOMAIN_CASES, domain_key="{domain_key}")\n'


def generate_program_md(domain_key, config):
    return f"""# {config["display_name"]} SKILL.md — Autoresearch Program

## Objective
Maximize pass rate on evaluate.py by optimizing skills/{domain_key}/SKILL.md.

## Target File
`skills/{domain_key}/SKILL.md`

## Eval Levels
- **Level 1 (keyword):** Does the SKILL.md mention the right terms?
- **Level 2 (structural):** Does the SKILL.md have required sections, valid links, word budget?
- **Level 3 (response):** Does Claude produce correct output when guided by this skill?

## Rules
1. One change per experiment.
2. Never modify evaluate.py.
3. Most HealthSim skills are ALREADY over 2000 words — default to tightening
   and refactoring to sub-skill files, not adding content.
4. Preserve frontmatter name and triggers.

## Mutation Strategies

### Level 1 (keyword matching)
1. Tighten verbose language — say the same thing in fewer words
2. Move detailed tables/examples into sub-skill .md files (no word limit)
3. Add safety guardrails if missing (all data is synthetic, no clinical advice)
4. Add negative examples (what NOT to generate)
5. Strengthen code system references (ICD-10, CPT, LOINC, RxNorm, NDC)
6. Add edge case handling (missing fields, invalid codes, partial data)

### Level 2 (structural quality)
7. Add YAML frontmatter with name and description fields
8. Add required sections: Safety Guardrails, Examples, Edge Cases
9. Fix broken markdown links to sub-skill files
10. Ensure word count stays ≤ 2000

### Level 3 (response quality)
11. Add worked JSON examples that demonstrate correct output structure
12. Add clinical coherence rules (medications match diagnoses)
13. Add code validation guidance (use real ICD-10/CPT/LOINC codes, not invented ones)
14. Add temporal ordering rules (diagnosis before treatment, labs after orders)
"""


def generate_all(output_dir, domains, force=False):
    generated, skipped = [], []
    for dk, cfg in domains.items():
        dd = Path(output_dir) / dk
        ep = dd / "evaluate.py"
        pp = dd / "program.md"
        if ep.exists() and not force:
            skipped.append(dk); continue
        dd.mkdir(parents=True, exist_ok=True)
        ep.write_text(generate_evaluate_py(dk, cfg))
        pp.write_text(generate_program_md(dk, cfg))
        nc = sum(len(tc[4]) for tc in cfg["test_cases"])
        generated.append((dk, nc, 7))
    return generated, skipped


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HealthSim Eval Factory")
    parser.add_argument("--output", "-o", default=".", help="Output dir")
    parser.add_argument("--force", "-f", action="store_true")
    parser.add_argument("--list", "-l", action="store_true")
    args = parser.parse_args()
    if args.list:
        print(f"{'Domain':<20} {'Cases':>6} {'L1 Crit':>10} {'L2':>5} {'L3':>5}")
        print("-" * 50)
        for k, c in sorted(DOMAINS.items()):
            n = len(c["test_cases"])
            cr = sum(len(tc[4]) for tc in c["test_cases"]) + 7
            print(f"{k:<20} {n:>6} {cr:>10} {'yes':>5} {'yes':>5}")
        sys.exit(0)
    generated, skipped = generate_all(Path(args.output), DOMAINS, args.force)
    print("=" * 56)
    print("  HealthSim Eval Factory — Generation Complete")
    print("=" * 56)
    for d, nd, ns in generated:
        print(f"  ✓ {d:<20} {nd} domain + {ns} shared + L2 + L3")
    if skipped:
        print(f"\n  Skipped (use --force):")
        for s in skipped: print(f"    → {s}")
    print(f"\n  Total: {len(generated)} generated, {len(skipped)} skipped")
