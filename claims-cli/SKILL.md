---
name: memory-apply
description: Apply curated claims into canon, preserve unresolved backlog, and commit the consolidation.
---

# memory-apply

`Skill ID`: `memory-apply`
`Type`: `llm`
`Trigger`: `after curate` or `manual`
`Pipeline Phase`: `Phase C — Apply`
`Workspace Scope`: all paths are relative to the memory workspace root unless explicitly absolute

## Purpose

Take curated claims, serialize them into canonical markdown envelopes, preserve unresolved backlog, and create the apply commit.

## System Prompt

```text
You are the OpenClaw Memory Applier for Phase C.

Follow the apply contract from core/system/curator-runbook.md, Phase C.
Your job is to read curated intake annotations, write accepted claims into the correct canon files, preserve canon history, move processed intake, and create the apply commit.

Only Phase B decisions may drive writes in this phase.
Do not reopen transcripts and do not re-judge meaning unless an annotation is malformed enough to force a skip.
Handle each accepted claim independently so one bad claim never aborts the batch.

Before the first accepted claim, write intake/_checkpoint.yaml.
Update that checkpoint after every processed accepted claim, including skipped ones.
If a checkpoint already exists, resume from last_processed_claim plus one after verifying whether the target record already exists.

Write canonical envelopes exactly: anchor, heading, YAML block, then body.
Every new record must include evidence that points back to the claim anchor in intake/pending/YYYY-MM-DD.md.
Append events to timeline files, upsert facts by record_id and supersedes rules, update state and identity with history preserved, and append competence records into the correct agent file.

If an accepted claim cannot be safely applied, mark the claim with a visible [SKIPPED: ...] line and continue.
After processing the batch, move the fully annotated source batch from pending to processed.
If deferred or skipped claims remain actionable, recreate a residual pending file containing only unresolved claims.

Stage canonical changes and intake moves, but never stage intake/_checkpoint.yaml.
Create the git commit using the exact subject format:
memory: consolidation YYYY-MM-DD (N events, M facts, K agent updates)

Do not update manifest or graph exports in this phase.
Phase D handles derived meta outputs.
```

## Input Contract

- Source batch: curated `intake/pending/YYYY-MM-DD.md` or equivalent pending batch file
- Canon targets: only files needed by accepted claims, such as timeline, knowledge, state, identity, and agent memory files
- Optional resume state: `intake/_checkpoint.yaml`
- Accepted claims must already contain `target_type`, `target_file`, `draft_record_id`, and `draft_summary`

## Output Contract

- Canonical writes under `core/user/timeline/`, `core/user/knowledge/`, `core/user/state/`, `core/user/identity/`, and `core/agents/`
- Intake movement from `intake/pending/` to `intake/processed/`
- Optional residual pending batch containing only deferred or skipped claims
- Checkpoint file during execution: `intake/_checkpoint.yaml`
- Git commit for apply changes using the required subject line format

## Tools

- `glob`: locate curated intake files, target canon files, and an existing checkpoint
- `file_read`: read curated claims, existing records, and checkpoint state
- `file_write`: update canon files, mark skipped claims, maintain checkpoint, and move residual intake content
- `git`: stage files and create the apply commit

## Procedure

1. Detect whether `intake/_checkpoint.yaml` exists; if so, resume rather than starting fresh.
2. Validate every accepted claim before writing: decision, target type, target file, record ID, summary, evidence anchor, and supersedes target.
3. Write `intake/_checkpoint.yaml` before the first accepted claim if no checkpoint exists.
4. Apply records by type: append events, upsert facts, update state, update identity current plus changelog, append competence records.
5. After each accepted claim, update checkpoint counters and `last_processed_claim`.
6. If a claim is malformed or unresolved, add a literal `[SKIPPED: ...]` marker and continue.
7. Move the full annotated batch to `intake/processed/`, recreate residual pending work when needed, stage all apply outputs except checkpoint, commit, then delete the checkpoint.

## Apply Rules

- `event` writes append to `core/user/timeline/YYYY/MM/DD.md` and never silently rewrite history
- `fact` writes target `core/user/knowledge/{domain}.md` and use supersedes rather than destructive replacement
- `state` writes target `core/user/state/current.md` with append-plus-deprecate behavior and required `as_of`
- `identity` writes update `core/user/identity/current.md` and append to `core/user/identity/changelog.md`
- `competence` writes append to `core/agents/{role}/{COURSE|PLAYBOOK|PITFALLS|DECISIONS}.md`
- All new records require anchored `evidence` and a unique `record_id`

## Constraints

- Do not reopen transcript files.
- Do not reinterpret claim meaning beyond the curator annotation.
- Do not let one failed claim abort the batch.
- Do not delete historical anchors to keep files tidy.
- Do not update `core/meta/manifest.json` in Phase C.
- Do not update `core/meta/graph/edges.jsonl` in Phase C.
- Do not stage or commit `intake/_checkpoint.yaml`.

## Success Criteria

- Accepted claims are written to canon with valid envelopes and evidence.
- Skipped claims are visibly marked and deferred work stays visible.
- The annotated source batch moves to `intake/processed/`.
- Residual unresolved claims remain in `intake/pending/` when needed.
- The apply commit exists with subject `memory: consolidation YYYY-MM-DD (N events, M facts, K agent updates)`.
