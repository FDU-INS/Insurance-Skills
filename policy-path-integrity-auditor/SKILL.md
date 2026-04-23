---
name: openclaw-0270-policy-scoped-data-mediation
description: Collab Privacy Preserving Data Broker. Use when work requires policy-scoped data mediation for Collaboration and Negotiation with guardrails, traceable execution, and measurable outcomes.
---

# Collab Privacy Preserving Data Broker

## Mission
We need this skill because multi-agent systems underperform without explicit conflict resolution. This specific skill enables collaboration while minimizing raw data exposure.

## Activation Cues
- Task requires policy-scoped data mediation in Collaboration and Negotiation.
- Task needs explicit risk controls, approval gates, and traceable outcomes.
- Task output must include artifact handoff for humans and agents.

## Execution Plan
1. Define the scope and success metrics for `Collab Privacy Preserving Data Broker`, including at least three measurable KPIs tied to deadlocks and degraded trust.
2. Design and version the input/output contract for proposals, contention signals, and negotiated outcomes, then add schema validation and failure-mode handling.
3. Implement the core capability using policy-scoped data mediation, and produce privacy-scoped exchanges with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover deadlocks and degraded trust, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Runbook
Preflight:
- None specified.

Execution:
- None specified.

Recovery:
- None specified.

Handoff:
- None specified.

## Guardrails
- [quality] Require validations before promoting outputs.

## Success Metrics
- Primary metric: deadlocks
- Secondary metrics: degraded trust, decision drift
- Review cadence: weekly

## Output Contract
- Return a concise execution summary with key decisions.
- Return risk and mitigation notes with unresolved blockers.
- Return artifact target: `privacy-scoped exchanges`.
- Return recommended follow-up tasks for next wave execution.
