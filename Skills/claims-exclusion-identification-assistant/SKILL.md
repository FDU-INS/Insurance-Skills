---
name: paper-claim-traceability-auditor
description: Map paper claims to code, config, tests, and artifacts for end-to-end traceability. Use when users ask for claim audit trails, evidence mapping, implementation to paper alignment, or submission traceability checks.
---
# paper-claim-traceability-auditor

Build claim-to-evidence trace maps suitable for audits and submission reviews.

## Execute

1. Extract explicit claims from user text or paper draft sections.
2. Map each claim to `configs/` and `main/` first because they define the core release path.
3. Add `tests/`, `scripts/`, `notebook/`, and outputs only as supporting traceability anchors; helper scripts must not override the semantics in `main/`.
4. Mark missing anchors or weak links as traceability gaps.
5. Distinguish static-confirmable claims from runtime-required claims.
6. Produce a structured traceability matrix with risk levels.

## Repository Anchors

- `doc/`
- `configs/`
- `main/`
- `tests/`
- `scripts/run_onefile_workflow.py`
- `notebook/Colab_Workflow.ipynb`

## Output Contract

- `claim`
- `code_anchor`
- `config_anchor`
- `test_anchor`
- `artifact_anchor`
- `gap_or_status`
