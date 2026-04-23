#!/usr/bin/env python3
"""Link claim-side evidence objects to observation-side evidence objects."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

SKILL_NAME = "eco-link-claims-to-observations"
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
RUNTIME_SRC = WORKSPACE_ROOT / "eco-concil-runtime" / "src"
if str(RUNTIME_SRC) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SRC))

from eco_council_runtime.kernel.analysis_plane import (  # noqa: E402
    load_claim_candidate_context,
    load_claim_cluster_context,
    load_merged_observation_context,
    load_observation_candidate_context,
    sync_claim_observation_link_result_set,
)


def normalize_space(value: Any) -> str:
    return " ".join(str(value).split())


def maybe_text(value: Any) -> str:
    if value is None:
        return ""
    return normalize_space(value)


def maybe_number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def pretty_json(data: Any, pretty: bool) -> str:
    if pretty:
        return json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True)
    return json.dumps(data, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def stable_hash(*parts: Any) -> str:
    joined = "||".join(maybe_text(part) for part in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_run_dir(run_dir: str) -> Path:
    return Path(run_dir).expanduser().resolve()


def resolve_path(run_dir: Path, path_text: str, default_name: str) -> Path:
    text = maybe_text(path_text)
    if not text:
        return (run_dir / "analytics" / default_name).resolve()
    candidate = Path(text).expanduser()
    if not candidate.is_absolute():
        candidate = run_dir / candidate
    return candidate.resolve()


def load_json_if_exists(path: Path) -> Any | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def unique_refs(refs: list[dict[str, Any]], limit: int) -> list[dict[str, str]]:
    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        artifact_ref = maybe_text(ref.get("artifact_ref"))
        if not artifact_ref or artifact_ref in seen:
            continue
        seen.add(artifact_ref)
        deduped.append(
            {
                "signal_id": maybe_text(ref.get("signal_id")),
                "artifact_path": maybe_text(ref.get("artifact_path")),
                "record_locator": maybe_text(ref.get("record_locator")),
                "artifact_ref": artifact_ref,
            }
        )
        if len(deduped) >= limit:
            break
    return deduped


def source_available(value: Any) -> bool:
    text = maybe_text(value)
    return bool(text) and not text.startswith("missing-")


def parse_utc(value: str) -> datetime | None:
    text = maybe_text(value)
    if not text:
        return None
    normalized = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def normalize_claim_items(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    if isinstance(payload.get("clusters"), list):
        items = payload.get("clusters", [])
        normalized: list[dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            normalized.append(
                {
                    "claim_id": maybe_text(item.get("cluster_id")),
                    "claim_type": maybe_text(item.get("claim_type")),
                    "text": maybe_text(item.get("representative_statement") or item.get("cluster_label")),
                    "time_window": item.get("time_window") if isinstance(item.get("time_window"), dict) else {},
                    "member_count": item.get("member_count"),
                    "evidence_refs": (
                        item.get("evidence_refs")
                        if isinstance(item.get("evidence_refs"), list)
                        else (
                            item.get("public_refs")
                            if isinstance(item.get("public_refs"), list)
                            else []
                        )
                    ),
                }
            )
        return normalized
    items = payload.get("candidates", []) if isinstance(payload.get("candidates"), list) else []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "claim_id": maybe_text(item.get("claim_id")),
                "claim_type": maybe_text(item.get("claim_type")),
                "text": maybe_text(item.get("statement") or item.get("summary")),
                "time_window": item.get("time_window") if isinstance(item.get("time_window"), dict) else {},
                "member_count": item.get("source_signal_count"),
                "evidence_refs": (
                    item.get("evidence_refs")
                    if isinstance(item.get("evidence_refs"), list)
                    else (
                        item.get("public_refs")
                        if isinstance(item.get("public_refs"), list)
                        else []
                    )
                ),
            }
        )
    return normalized


def normalize_observation_items(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    if isinstance(payload.get("merged_observations"), list):
        items = payload.get("merged_observations", [])
        normalized: list[dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            normalized.append(
                {
                    "observation_id": maybe_text(item.get("merged_observation_id")),
                    "metric": maybe_text(item.get("metric")),
                    "value": item.get("value_summary", {}).get("mean") if isinstance(item.get("value_summary"), dict) else item.get("value"),
                    "time_window": item.get("time_window") if isinstance(item.get("time_window"), dict) else {},
                    "source_skills": item.get("source_skills") if isinstance(item.get("source_skills"), list) else [],
                    "member_count": item.get("member_count"),
                    "place_scope": item.get("place_scope") if isinstance(item.get("place_scope"), dict) else {},
                    "evidence_refs": item.get("provenance_refs") if isinstance(item.get("provenance_refs"), list) else [],
                }
            )
        return normalized
    items = payload.get("candidates", []) if isinstance(payload.get("candidates"), list) else []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "observation_id": maybe_text(item.get("observation_id")),
                "metric": maybe_text(item.get("metric")),
                "value": item.get("value"),
                "time_window": item.get("time_window") if isinstance(item.get("time_window"), dict) else {},
                "source_skills": item.get("source_skills") if isinstance(item.get("source_skills"), list) else [],
                "member_count": item.get("source_signal_count"),
                "place_scope": item.get("place_scope") if isinstance(item.get("place_scope"), dict) else {},
                "evidence_refs": item.get("provenance_refs") if isinstance(item.get("provenance_refs"), list) else [],
            }
        )
    return normalized


def select_claim_input_context(
    run_dir_path: Path,
    *,
    run_id: str,
    round_id: str,
    claim_cluster_path: str,
    claim_candidates_path: str,
) -> dict[str, Any]:
    cluster_context = load_claim_cluster_context(
        run_dir_path,
        run_id=run_id,
        round_id=round_id,
        claim_cluster_path=claim_cluster_path,
    )
    candidate_context = load_claim_candidate_context(
        run_dir_path,
        run_id=run_id,
        round_id=round_id,
        claim_candidates_path=claim_candidates_path,
        db_path=maybe_text(cluster_context.get("db_path")),
    )
    if source_available(cluster_context.get("claim_cluster_source")):
        return {
            "selected_kind": "claim-cluster",
            "selected_source": maybe_text(cluster_context.get("claim_cluster_source")),
            "selected_file": maybe_text(cluster_context.get("claim_cluster_file")),
            "selected_wrapper": cluster_context.get("claim_cluster_wrapper", {}),
            "db_path": maybe_text(candidate_context.get("db_path"))
            or maybe_text(cluster_context.get("db_path")),
            "cluster_context": cluster_context,
            "candidate_context": candidate_context,
            "warnings": [],
        }
    if source_available(candidate_context.get("claim_candidate_source")):
        return {
            "selected_kind": "claim-candidate",
            "selected_source": maybe_text(
                candidate_context.get("claim_candidate_source")
            ),
            "selected_file": maybe_text(candidate_context.get("claim_candidates_file")),
            "selected_wrapper": candidate_context.get("claim_candidates_wrapper", {}),
            "db_path": maybe_text(candidate_context.get("db_path"))
            or maybe_text(cluster_context.get("db_path")),
            "cluster_context": cluster_context,
            "candidate_context": candidate_context,
            "warnings": [],
        }
    cluster_file = maybe_text(cluster_context.get("claim_cluster_file"))
    candidate_file = maybe_text(candidate_context.get("claim_candidates_file"))
    return {
        "selected_kind": "missing-claim-input",
        "selected_source": "missing-claim-input",
        "selected_file": candidate_file or cluster_file,
        "selected_wrapper": candidate_context.get("claim_candidates_wrapper", {}),
        "db_path": maybe_text(candidate_context.get("db_path"))
        or maybe_text(cluster_context.get("db_path")),
        "cluster_context": cluster_context,
        "candidate_context": candidate_context,
        "warnings": [
            {
                "code": "missing-claim-input",
                "message": "No claim-side artifact or analysis result was found "
                f"at {cluster_file} or {candidate_file}.",
            }
        ],
    }


def select_observation_input_context(
    run_dir_path: Path,
    *,
    run_id: str,
    round_id: str,
    merged_observations_path: str,
    observation_candidates_path: str,
    db_path: str = "",
) -> dict[str, Any]:
    merged_context = load_merged_observation_context(
        run_dir_path,
        run_id=run_id,
        round_id=round_id,
        merged_observations_path=merged_observations_path,
        db_path=db_path,
    )
    candidate_context = load_observation_candidate_context(
        run_dir_path,
        run_id=run_id,
        round_id=round_id,
        observation_candidates_path=observation_candidates_path,
        db_path=maybe_text(merged_context.get("db_path")) or db_path,
    )
    if source_available(merged_context.get("merged_observation_source")):
        return {
            "selected_kind": "merged-observation",
            "selected_source": maybe_text(
                merged_context.get("merged_observation_source")
            ),
            "selected_file": maybe_text(
                merged_context.get("merged_observations_file")
            ),
            "selected_wrapper": merged_context.get(
                "merged_observations_wrapper", {}
            ),
            "db_path": maybe_text(candidate_context.get("db_path"))
            or maybe_text(merged_context.get("db_path")),
            "merged_context": merged_context,
            "candidate_context": candidate_context,
            "warnings": [],
        }
    if source_available(candidate_context.get("observation_candidate_source")):
        return {
            "selected_kind": "observation-candidate",
            "selected_source": maybe_text(
                candidate_context.get("observation_candidate_source")
            ),
            "selected_file": maybe_text(
                candidate_context.get("observation_candidates_file")
            ),
            "selected_wrapper": candidate_context.get(
                "observation_candidates_wrapper", {}
            ),
            "db_path": maybe_text(candidate_context.get("db_path"))
            or maybe_text(merged_context.get("db_path")),
            "merged_context": merged_context,
            "candidate_context": candidate_context,
            "warnings": [],
        }
    merged_file = maybe_text(merged_context.get("merged_observations_file"))
    candidates_file = maybe_text(candidate_context.get("observation_candidates_file"))
    return {
        "selected_kind": "missing-observation-input",
        "selected_source": "missing-observation-input",
        "selected_file": candidates_file or merged_file,
        "selected_wrapper": candidate_context.get("observation_candidates_wrapper", {}),
        "db_path": maybe_text(candidate_context.get("db_path"))
        or maybe_text(merged_context.get("db_path")),
        "merged_context": merged_context,
        "candidate_context": candidate_context,
        "warnings": [
            {
                "code": "missing-observation-input",
                "message": "No observation-side artifact or analysis result was "
                f"found at {merged_file} or {candidates_file}.",
            }
        ],
    }


def infer_metric_preferences(text: str) -> dict[str, float]:
    folded = maybe_text(text).casefold()
    preferences: dict[str, float] = {}
    if any(token in folded for token in ("smoke", "wildfire", "haze", "air quality", "pollution", "contamination")):
        preferences.update({"pm2_5": 1.0, "pm10": 0.8, "o3": 0.55})
    if any(token in folded for token in ("heat", "hot", "temperature", "warm")):
        preferences.update({"temperature_2m": 1.0, "apparent_temperature": 0.85})
    if any(token in folded for token in ("rain", "flood", "storm", "precipitation")):
        preferences.update({"precipitation": 1.0, "precipitation_sum": 0.9, "rain": 0.9})
    if any(token in folded for token in ("wind", "gust")):
        preferences.update({"wind_speed_10m": 1.0, "wind_gusts_10m": 0.9})
    return preferences


def time_score(claim: dict[str, Any], observation: dict[str, Any]) -> tuple[float, str]:
    claim_window = claim.get("time_window") if isinstance(claim.get("time_window"), dict) else {}
    observation_window = observation.get("time_window") if isinstance(observation.get("time_window"), dict) else {}
    claim_start = parse_utc(maybe_text(claim_window.get("start_utc") or claim_window.get("end_utc")))
    observation_start = parse_utc(maybe_text(observation_window.get("start_utc") or observation_window.get("end_utc")))
    if claim_start is None or observation_start is None:
        return 0.35, "missing-time-window"
    hours = abs((claim_start - observation_start).total_seconds()) / 3600.0
    if hours <= 24:
        return 1.0, "same-day-window"
    if hours <= 72:
        return 0.7, "nearby-window"
    if hours <= 168:
        return 0.4, "week-window"
    return 0.1, "distant-window"


def intensity_relation(text: str, metric: str, value: float | None) -> tuple[str, str]:
    if value is None:
        return "contextual", "missing-numeric-value"
    folded = maybe_text(text).casefold()
    metric_name = maybe_text(metric)
    if any(token in folded for token in ("smoke", "wildfire", "haze", "pollution")) and metric_name in {"pm2_5", "pm10", "o3"}:
        if metric_name == "pm2_5" and value >= 35:
            return "support", "high-pm2_5"
        if metric_name == "pm10" and value >= 50:
            return "support", "high-pm10"
        if metric_name == "o3" and value >= 70:
            return "support", "high-o3"
        if metric_name == "pm2_5" and value <= 12:
            return "contradiction", "low-pm2_5"
    if any(token in folded for token in ("heat", "hot", "temperature")) and metric_name in {"temperature_2m", "apparent_temperature"}:
        if value >= 30:
            return "support", "high-temperature"
        if value <= 18:
            return "contradiction", "low-temperature"
    if any(token in folded for token in ("rain", "flood", "storm", "precipitation")) and metric_name in {"precipitation", "precipitation_sum", "rain"}:
        if value >= 5:
            return "support", "high-precipitation"
        if value <= 1:
            return "contradiction", "low-precipitation"
    return "contextual", "metric-context-only"


def evaluate_link(claim: dict[str, Any], observation: dict[str, Any]) -> tuple[float, str, list[str]]:
    preferences = infer_metric_preferences(maybe_text(claim.get("text")))
    metric_name = maybe_text(observation.get("metric"))
    metric_score = preferences.get(metric_name, 0.0)
    time_component, time_reason = time_score(claim, observation)
    source_diversity = 1.0 if len(observation.get("source_skills", [])) > 1 or int(observation.get("member_count") or 0) > 1 else 0.55
    relation, intensity_reason = intensity_relation(maybe_text(claim.get("text")), metric_name, maybe_number(observation.get("value")))
    if metric_score == 0.0 and relation == "contextual":
        return 0.0, "contextual", ["no-metric-affinity", time_reason]
    score = min(1.0, metric_score * 0.65 + time_component * 0.2 + source_diversity * 0.15)
    if relation == "support":
        score = min(1.0, score + 0.12)
    elif relation == "contradiction":
        score = min(0.95, score + 0.08)
    reasons = [f"metric-affinity:{metric_score:.2f}", time_reason, intensity_reason]
    return score, relation, reasons


def link_claims_to_observations_skill(
    run_dir: str,
    run_id: str,
    round_id: str,
    claim_cluster_path: str,
    claim_candidates_path: str,
    merged_observations_path: str,
    observation_candidates_path: str,
    output_path: str,
    min_score: float,
    top_links_per_claim: int,
) -> dict[str, Any]:
    run_dir_path = resolve_run_dir(run_dir)
    output_file = resolve_path(run_dir_path, output_path, f"claim_observation_links_{round_id}.json")

    claim_input = select_claim_input_context(
        run_dir_path,
        run_id=run_id,
        round_id=round_id,
        claim_cluster_path=claim_cluster_path,
        claim_candidates_path=claim_candidates_path,
    )
    observation_input = select_observation_input_context(
        run_dir_path,
        run_id=run_id,
        round_id=round_id,
        merged_observations_path=merged_observations_path,
        observation_candidates_path=observation_candidates_path,
        db_path=maybe_text(claim_input.get("db_path")),
    )
    claim_cluster_context = claim_input["cluster_context"]
    claim_candidate_context = claim_input["candidate_context"]
    merged_context = observation_input["merged_context"]
    observation_candidate_context = observation_input["candidate_context"]
    claim_source_file = Path(maybe_text(claim_input.get("selected_file")))
    observation_source_file = Path(maybe_text(observation_input.get("selected_file")))
    claim_input_source = maybe_text(claim_input.get("selected_source"))
    observation_input_source = maybe_text(observation_input.get("selected_source"))
    claim_input_kind = maybe_text(claim_input.get("selected_kind"))
    observation_input_kind = maybe_text(observation_input.get("selected_kind"))
    warnings: list[dict[str, str]] = list(claim_input.get("warnings", []))
    warnings.extend(observation_input.get("warnings", []))

    claims = normalize_claim_items(claim_input.get("selected_wrapper"))
    observations = normalize_observation_items(observation_input.get("selected_wrapper"))
    links: list[dict[str, Any]] = []
    unmatched_claim_count = 0
    contradiction_count = 0
    for claim in claims:
        ranked_links: list[tuple[float, str, list[str], dict[str, Any]]] = []
        for observation in observations:
            score, relation, reasons = evaluate_link(claim, observation)
            if score < min_score:
                continue
            ranked_links.append((score, relation, reasons, observation))
        ranked_links.sort(key=lambda item: (-item[0], maybe_text(item[3].get("observation_id"))))
        if not ranked_links:
            unmatched_claim_count += 1
            continue
        for score, relation, reasons, observation in ranked_links[: max(1, top_links_per_claim)]:
            if relation == "contradiction":
                contradiction_count += 1
            link_id = "claimobs-" + stable_hash(run_id, round_id, claim.get("claim_id"), observation.get("observation_id"))[:12]
            evidence_refs = unique_refs(list(claim.get("evidence_refs", [])) + list(observation.get("evidence_refs", [])), 12)
            links.append(
                {
                    "schema_version": "n2.1",
                    "link_id": link_id,
                    "run_id": run_id,
                    "round_id": round_id,
                    "claim_id": maybe_text(claim.get("claim_id")),
                    "observation_id": maybe_text(observation.get("observation_id")),
                    "relation": relation,
                    "confidence": round(score, 3),
                    "method": "heuristic-metric-time-v1",
                    "match_summary": f"Linked claim {claim.get('claim_id')} to observation {observation.get('observation_id')} as {relation}.",
                    "rule_trace": reasons,
                    "evidence_refs": evidence_refs,
                }
            )
    wrapper = {
        "schema_version": "n2.1",
        "skill": SKILL_NAME,
        "run_id": run_id,
        "round_id": round_id,
        "generated_at_utc": utc_now_iso(),
        "query_basis": {
            "claim_input_path": str(claim_source_file),
            "observation_input_path": str(observation_source_file),
            "claim_input_source": claim_input_source or "missing-claim-input",
            "claim_input_kind": claim_input_kind or "missing-claim-input",
            "observation_input_source": observation_input_source
            or "missing-observation-input",
            "observation_input_kind": observation_input_kind
            or "missing-observation-input",
            "min_score": float(min_score),
            "top_links_per_claim": max(1, int(top_links_per_claim)),
            "selection_mode": "rank-observations-per-claim",
            "method": "heuristic-metric-time-v1",
        },
        "claim_input_path": str(claim_source_file),
        "observation_input_path": str(observation_source_file),
        "claim_input_source": claim_input_source or "missing-claim-input",
        "claim_input_kind": claim_input_kind or "missing-claim-input",
        "observation_input_source": observation_input_source
        or "missing-observation-input",
        "observation_input_kind": observation_input_kind
        or "missing-observation-input",
        "observed_inputs": {
            "claim_clusters_present": source_available(
                claim_cluster_context.get("claim_cluster_source")
            ),
            "claim_clusters_artifact_present": bool(
                claim_cluster_context.get("claim_cluster_artifact_present")
            ),
            "claim_candidates_present": source_available(
                claim_candidate_context.get("claim_candidate_source")
            ),
            "claim_candidates_artifact_present": bool(
                claim_candidate_context.get("claim_candidates_artifact_present")
            ),
            "merged_observations_present": source_available(
                merged_context.get("merged_observation_source")
            ),
            "merged_observations_artifact_present": bool(
                merged_context.get("merged_observations_artifact_present")
            ),
            "observation_candidates_present": source_available(
                observation_candidate_context.get("observation_candidate_source")
            ),
            "observation_candidates_artifact_present": bool(
                observation_candidate_context.get(
                    "observation_candidates_artifact_present"
                )
            ),
        },
        "input_analysis_sync": {
            "claim_clusters": claim_cluster_context.get("analysis_sync", {}),
            "claim_candidates": claim_candidate_context.get("analysis_sync", {}),
            "merged_observations": merged_context.get("analysis_sync", {}),
            "observation_candidates": observation_candidate_context.get(
                "analysis_sync", {}
            ),
        },
        "link_count": len(links),
        "links": links,
    }
    write_json(output_file, wrapper)
    analysis_sync = sync_claim_observation_link_result_set(
        run_dir_path,
        expected_run_id=run_id,
        round_id=round_id,
        links_path=output_file,
        db_path=maybe_text(observation_input.get("db_path"))
        or maybe_text(claim_input.get("db_path")),
    )
    wrapper["db_path"] = maybe_text(analysis_sync.get("db_path"))
    wrapper["analysis_sync"] = analysis_sync
    write_json(output_file, wrapper)
    artifact_refs: list[dict[str, str]] = [
        {
            "signal_id": "",
            "artifact_path": str(output_file),
            "record_locator": "$.links",
            "artifact_ref": f"{output_file}:$.links",
        }
    ]
    for link in links:
        artifact_refs.extend(link["evidence_refs"])
    if not links:
        warnings.append({"code": "no-links", "message": "No claim-observation links met the requested score threshold."})
    gap_hints: list[str] = []
    if unmatched_claim_count:
        gap_hints.append(f"{unmatched_claim_count} claim-side evidence objects still have no linked observation support.")
    if not links:
        gap_hints.append("No evidence links are available for board review yet.")
    challenge_hints: list[str] = []
    if contradiction_count:
        challenge_hints.append(f"{contradiction_count} links are contradiction-leaning and should be reviewed by challenger workflows.")
    return {
        "status": "completed",
        "summary": {
            "skill": SKILL_NAME,
            "run_id": run_id,
            "round_id": round_id,
            "claim_input_count": len(claims),
            "observation_input_count": len(observations),
            "link_count": len(links),
            "output_path": str(output_file),
            "claim_input_source": claim_input_source or "missing-claim-input",
            "observation_input_source": observation_input_source
            or "missing-observation-input",
            "db_path": maybe_text(analysis_sync.get("db_path")),
        },
        "receipt_id": "evidence-receipt-" + stable_hash(SKILL_NAME, run_id, round_id, str(output_file))[:20],
        "batch_id": "evbatch-" + stable_hash(SKILL_NAME, run_id, round_id, str(output_file))[:16],
        "artifact_refs": unique_refs(artifact_refs, 40),
        "canonical_ids": [link["link_id"] for link in links],
        "warnings": warnings,
        "analysis_sync": analysis_sync,
        "input_analysis_sync": wrapper.get("input_analysis_sync", {}),
        "board_handoff": {
            "candidate_ids": [link["link_id"] for link in links],
            "evidence_refs": unique_refs(artifact_refs, 20),
            "gap_hints": gap_hints,
            "challenge_hints": challenge_hints,
            "suggested_next_skills": ["eco-derive-claim-scope", "eco-derive-observation-scope", "eco-score-evidence-coverage"],
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Link claim-side evidence objects to observation-side evidence objects.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--round-id", required=True)
    parser.add_argument("--claim-cluster-path", default="")
    parser.add_argument("--claim-candidates-path", default="")
    parser.add_argument("--merged-observations-path", default="")
    parser.add_argument("--observation-candidates-path", default="")
    parser.add_argument("--output-path", default="")
    parser.add_argument("--min-score", type=float, default=0.35)
    parser.add_argument("--top-links-per-claim", type=int, default=3)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = link_claims_to_observations_skill(
        run_dir=args.run_dir,
        run_id=args.run_id,
        round_id=args.round_id,
        claim_cluster_path=args.claim_cluster_path,
        claim_candidates_path=args.claim_candidates_path,
        merged_observations_path=args.merged_observations_path,
        observation_candidates_path=args.observation_candidates_path,
        output_path=args.output_path,
        min_score=args.min_score,
        top_links_per_claim=args.top_links_per_claim,
    )
    print(pretty_json(payload, args.pretty))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
