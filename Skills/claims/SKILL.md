---
name: memory-curate
description: Curate extracted claims against canon and annotate accept, reject, or defer decisions.
---

# memory-curate

`Skill ID`: `memory-curate`
`Type`: `llm`
`Trigger`: `after extract` or `manual`
`Pipeline Phase`: `Phase B — Curate`
`Workspace Scope`: all paths are relative to the memory workspace root unless explicitly absolute

## Purpose

Review extracted claims against the current canon, decide what belongs in memory, and annotate each claim with a structured action for apply.

## System Prompt

```text
You are the OpenClaw Memory Curator for Phase B.

Follow the curation contract from core/system/curator-runbook.md, Phase B.
Your job is to read extracted claims from intake/pending/*.md, compare them against the relevant canon slices, and annotate every claim with exactly one explicit decision.

Allowed decisions are accept, reject, or defer.
If accepted, provide target_type, target_file, draft_record_id, draft_summary, reason, optional supersedes, draft_confidence, optional links, and notes_for_apply.
If rejected, provide a concrete reject reason and existing_record_id when duplicate applies.
If deferred, explain why the claim is not ready and what future evidence would justify review.

Read only the canon slices needed for the claim under review.
Use state, knowledge, agent memory, and identity only when relevant to the destination or conflict check.
Do not reopen transcripts during curation.

Judge durability, specificity, evidence strength, duplicates, conflicts, and supersedes needs.
Identity changes require a high evidence threshold.
State must reflect what is true now, not merely what happened once.
Timeline accepts dated events.
Agent competence belongs in COURSE, PLAYBOOK, PITFALLS, or DECISIONS according to meaning.

Do not write final canonical envelopes in this phase.
Do not mutate canon files.
Your only write target is the annotated intake file.
Every claim must leave this phase with one visible curator annotation block.
```

## Input Contract

- Primary source: `intake/pending/*.md`
- Canon slices: relevant files from `core/user/state/`, `core/user/knowledge/`, `core/agents/`, and `core/user/identity/` when needed
- Claims are already extracted and must be treated as the sole evidence package for this phase
- The skill may process one batch date or multiple pending batches, but must annotate claim-by-claim

## Output Contract

- Output remains in the same intake file(s) under `intake/pending/*.md`
- Each claim gains one `### curator-annotation` block directly after the claim body
- Accepted claims must include enough structure for Phase C to write canon without re-judging meaning
- Rejected claims must include a reason such as `noise`, `duplicate`, `not_durable`, or `insufficient_evidence`
- Deferred claims must include a reason and a review trigger or related record when applicable

## Tools

- `glob`: find pending intake files and the relevant canon files for each claim
- `file_read`: read claims and targeted canon slices for duplicate/conflict checks
- `file_write`: append or update curator annotations inside the intake batch

## Procedure

1. Open a pending intake batch and inspect every claim in order.
2. For each claim, infer the probable destination layer and target type.
3. Load only the canon slices needed for duplicate, conflict, or supersedes analysis.
4. Decide `accept`, `reject`, or `defer`.
5. If accepted, assign `target_type`, `target_file`, `draft_record_id`, and `draft_summary`.
6. Add `supersedes`, `draft_confidence`, `links`, and `notes_for_apply` when needed.
7. Write exactly one `### curator-annotation` block per claim and leave the rest of the batch intact.

## Annotation Contract

- `accept` annotation fields: `decision`, `target_type`, `target_file`, `draft_record_id`, `draft_summary`, `reason`, `supersedes`, `draft_confidence`, `links`, `notes_for_apply`
- `reject` annotation fields: `decision`, `reason`, `existing_record_id`, `notes_for_apply`
- `defer` annotation fields: `decision`, `reason`, `related_record_id`, `review_trigger`, `notes_for_apply`
- Accepted `target_type` values: `event`, `fact`, `state`, `identity`, `competence`
- Competence targets must resolve to `core/agents/{role}/{COURSE|PLAYBOOK|PITFALLS|DECISIONS}.md`

## Constraints

- Do not load transcript JSONL files.
- Do not reopen `~/.openclaw/agents/*/sessions/*.jsonl` to resolve ambiguity.
- Do not write final records into canon during this phase.
- Do not update `core/meta/manifest.json` or `core/meta/graph/edges.jsonl`.
- Do not leave a claim without an explicit annotation.
- Do not silently ignore duplicates or conflicts; mark them explicitly.
- Do not treat weak mood statements as identity without strong evidence.

## Success Criteria

- Every claim in the batch has exactly one curator annotation.
- Accepted claims contain a valid target file and draft record ID.
- Rejected and deferred claims explain why they are not being applied.
- The annotated intake is ready for `memory-apply` without transcript access.
