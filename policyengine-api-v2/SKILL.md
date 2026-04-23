---
name: analyze-latest-policy-sweep
description: Analyze latest policy analysis sweep runs (*_policy_analysis_*) by comparing episodes/summary metrics, diagnostics, and video artifacts; generate a concise markdown report and optional frame snapshots.
---

# Analyze Latest Policy Sweep

Use this skill when asked to compare recent `*_policy_analysis_*` benchmark runs (fast_pysf_planner, PPO, ORCA, etc.) and produce a summary report with diagnostics and video links.

## Quick start
1) Confirm run directories exist and contain `episodes.jsonl` + `summary.json`.
2) Load metrics from `episodes.jsonl` and aggregates from `summary.json`.
3) Produce a report in `specs/409-planner-comparison/`.

## Required report contents
- Aggregate metrics table (success rate, collision rate, time_to_goal_norm, avg_speed, near_misses, comfort_exposure, energy, jerk/curvature raw + filtered if present).
- Worst collision scenarios (top 5) per run.
- Lowest success scenarios (bottom 5) per run.
- Top problem episodes (score = collisions*10 + comfort*2 + failure) with video paths.
- Diagnostics: path_efficiency saturation, `shortest_path_len` presence, low-speed filter behavior (ε=0.1).

## Optional
- Extract frames (25/50/75% of duration) for top problem episodes using ffmpeg into `output/analysis/<report_id>/frames/` and list PNG paths in the report.

## Template
Use `specs/409-planner-comparison/analyze_latest_policy_sweep_prompt.md` as a template if you need a consistent structure.

## Video naming convention
`output/recordings/<run_dir>/<scenario>_seed<seed>_<policy>.mp4`

## Diagnostics details
- **Path-efficiency saturation**: fraction with `path_efficiency >= 0.999` (clipped at 1.0).
- **Shortest path presence**: ensure `shortest_path_len` is present in metrics when available.
- **Low-speed filter**: report `low_speed_frac` and filtered metrics (`jerk_mean_eps0p1`, `curvature_mean_eps0p1` when present). Reason: curvature divides by |v|^3; near-zero speed inflates noise.
