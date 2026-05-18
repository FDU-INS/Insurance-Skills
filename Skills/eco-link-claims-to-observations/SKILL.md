---
name: eco-link-claims-to-observations
description: Link claim-side evidence objects to observation-side evidence objects, score support or contradiction heuristically, and persist a compact claim-observation link artifact for board review and challenge work.
---

# Eco Link Claims To Observations

## Core Goal
- Read claim-side and observation-side candidate or grouped result sets from the analysis plane, with artifact-compatible fallback behavior.
- Propose support, contradiction, or contextual links between them.
- Persist a link artifact for board review, challenge work, and later promotion gates.

## Triggering Conditions
- Need claim-to-observation evidence hypotheses instead of isolated candidate lists.
- Need a compact link layer before board, challenge, or promotion skills.
- Need stable link ids, rule traces, and provenance refs for auditability.

## Read/Write Contract
- Loads `claim-cluster` result sets from the analysis plane first and falls back to `claim-candidate` results only when the preferred claim-side grouping is missing.
- Loads `merged-observation` result sets from the analysis plane first and falls back to `observation-candidate` results only when the preferred observation-side grouping is missing.
- Uses `claim_candidate_clusters_<round_id>.json`, `claim_candidates_<round_id>.json`, `merged_observation_candidates_<round_id>.json`, and `observation_candidates_<round_id>.json` as the default artifact paths behind those result kinds.
- Writes `runs/<run_id>/analytics/claim_observation_links_<round_id>.json` by default.
- Syncs the same link result set into `runs/<run_id>/analytics/signal_plane.sqlite` as analysis-plane state.

## Required Input
- `run_dir`
- `run_id`
- `round_id`
- Optional:
  - `claim_cluster_path`
  - `claim_candidates_path`
  - `merged_observations_path`
  - `observation_candidates_path`
  - `output_path`
  - `min_score`
  - `top_links_per_claim`

## Output Contract
- `status`
- `summary`
- `receipt_id`
- `batch_id`
- `artifact_refs`
- `canonical_ids`
- `warnings`
- `analysis_sync`
- `input_analysis_sync`
- `board_handoff`

## References
- `../../docs/openclaw-project-overview.md`
- `../../docs/openclaw-next-phase-development-plan.md`

## Scripts
- `scripts/eco_link_claims_to_observations.py`
