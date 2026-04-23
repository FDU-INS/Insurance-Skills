-- Copyright (c) 2026 Snowflake Inc. All rights reserved.
-- Licensed under the Snowflake Skills License.
-- Refer to the LICENSE file in the root of this repository for full terms.

-- Custom evaluation metric for the insurance claim routing demo.
-- Scores predictions on three weighted dimensions:
--   claim_route (exact match, weight 0.5)
--   citation (substring match, weight 0.3)
--   confidence (1 - MSE, weight 0.2)
--
-- Substitution variables: {database}, {schema}

CREATE OR REPLACE FUNCTION {database}.{schema}.DEMO_CLAIM_ROUTING_METRIC(
    EXPECTED VARCHAR,
    PREDICTED VARCHAR
)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.12'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'evaluate'
AS $$
import ast
import json

def _parse_json(text):
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        pass
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        pass
    return None

def evaluate(expected, predicted):
    exp = _parse_json(expected)
    pred = _parse_json(predicted)
    if exp is None or pred is None:
        return {"score": 0.0, "feedback": "Could not parse expected/predicted as JSON"}

    sub_scores = []
    feedback_parts = []

    # claim_route: exact match (weight 0.5)
    exp_route = str(exp.get("claim_route", "")).strip().lower()
    pred_route = str(pred.get("claim_route", "")).strip().lower()
    route_score = 1.0 if exp_route == pred_route else 0.0
    sub_scores.append(("route", route_score, 0.5))
    feedback_parts.append(f"route={'match' if route_score == 1.0 else 'MISMATCH: expected=' + exp_route + ' got=' + pred_route}")

    # citation: contains check (weight 0.3)
    exp_citation = str(exp.get("citation", "")).strip().lower()
    pred_citation = str(pred.get("citation", "")).strip().lower()
    if not exp_citation:
        citation_score = 1.0
    else:
        citation_score = 1.0 if exp_citation in pred_citation else 0.0
    sub_scores.append(("citation", citation_score, 0.3))
    feedback_parts.append(f"citation={'found' if citation_score == 1.0 else 'missing'}")

    # confidence: 1 - MSE (weight 0.2)
    try:
        exp_conf = float(exp.get("confidence", 0.5))
        pred_conf = float(pred.get("confidence", 0.5))
        conf_score = max(0.0, 1.0 - (exp_conf - pred_conf) ** 2)
    except (TypeError, ValueError):
        conf_score = 0.0
    sub_scores.append(("confidence", conf_score, 0.2))
    feedback_parts.append(f"confidence={conf_score:.2f}")

    total_weight = sum(w for _, _, w in sub_scores)
    combined = sum(s * w for _, s, w in sub_scores) / total_weight if total_weight > 0 else 0.0

    detail = " | ".join(feedback_parts)
    breakdown = ", ".join(f"{name}={s:.2f}*{w}" for name, s, w in sub_scores)
    feedback = f"{detail} [weights: {breakdown}]"

    return {"score": combined, "feedback": feedback}
$$;
