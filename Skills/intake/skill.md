---
name: intake
description: Read sources on a foreign system, translate claims into Natural Framework terminology, and stream each into Synopsis for filing. Fan-out on thin sources. Elicit human judgment on ambiguous mappings.
argument-hint: <system-name-or-url>
allowed-tools: Read, Grep, Glob, Bash, Agent, Skill, WebFetch, WebSearch
---

# Intake: Foreign System Translation

Read sources on a foreign system, translate into framework-speak, and file incrementally via Synopsis. When sources are thin, fan out parallel agents to build richer evidence before asking the human.

## Theory

- **The six roles**: [The Natural Framework](/the-natural-framework) — Intake translates foreign vocabulary into these six roles. The quality of the translation determines whether Synopsis can file mechanically and whether Diagnose has clean input.
- **Streaming architecture**: [Caret Recorder](/caret-recorder) — perceive per-item, filter per-item, clear the buffer before the next item. By the time you've finished reading, the cache is already built.
- **Tower-aware mappings**: Mappings must specify stack level, not just role. "X = Remember" is insufficient — the correct label may be "X = Remember @ Consolidate." A role can be present at one level and missing at another. Intake proposes flat mappings; Diagnose refines to tower-level. But if the evidence clearly places a term inside a specific stack during Intake, note it in the glossary rationale.

## Input

A system name, URL, paper link, or repo path. The user may also provide initial reading material.

## Process

### Phase 0: Development stage

Before reading sources, ask the human: **what stage is this system?** (proof of concept / prototype / production / legacy). Record the answer in S.md metadata as `stage: <answer>`. Development stage determines whether gaps are failures or expected — a PoC missing Consolidate is on-schedule, not broken. This propagates to Diagnose and Prescribe automatically via S.md.

### Phase 1: Read and file

For each source:

1. **Read.** Fetch or open the source. Extract key claims, architecture decisions, and stated limitations. For code sources, cite file paths and function/symbol names — `run_soar.cpp` is not enough; `do_one_top_level_phase()` in `Core/SoarKernel/src/decision_process/run_soar.cpp` is. **For repositories**: also scan notable PRs (merged and rejected). PRs reveal design decisions, debates, and rejected alternatives that don't survive in the final code. Use `gh pr list --state all --limit 100 --json title,body,state,labels` or search for PRs touching key subsystems. Filter for PRs that changed architecture, added/removed learning mechanisms, or debated design trade-offs. Rejected PRs are especially valuable — they document paths not taken.
2. **Translate.** For each claim, produce a translation record:
   - `source`: source ID and section/page reference
   - `original`: the claim in the system's own vocabulary (quoted or paraphrased)
   - `system_term`: the foreign term being translated (e.g., "elaboration," "chunking")
   - `mapped_roles`: one or more framework roles. If ambiguous, list all candidates with a rationale for each — do not force a single choice. Ambiguous mappings are resolved at elicitation, not here. **Ambiguity triggers**: a term participates in two functionally distinct operations (e.g., RL both updates policy *and* biases selection), or the term spans two phases of the system's own processing.
   - `rationale`: why this mapping (one sentence)
   - `confidence`: high / medium / low. **Calibration**: if the term does double duty across distinct functions, confidence cannot be high for a single-role mapping — mark medium and flag as ambiguous.

   E.g., "Soar's 'elaboration' → Cache (parallel feature extraction) with competing hypothesis Cache+Filter (operator proposal as relevance gate)."
3. **File.** Write the claim directly to `soap/S.md` in the subject's own vocabulary, organized by the subject's own structural categories (not framework roles). Dedupe against existing entries — if a semantically similar claim exists, merge as convergent evidence. Update the glossary if the claim introduces a new system term. The translation record stays in Intake's cache — it informs the glossary's proposed mappings and feeds the elicitation quiz, but does not overwrite the subject's words in S.md. For large intakes (200+ claims), use `/synopsis` as a library function for mechanical dedupe and glossary updates.

Repeat across all sources. By the time Phase 1 finishes, the synopsis document is already built — in the subject's own terms.

### Phase 2: Assess source thickness

After filing all sources, assess **source thickness** per glossary term: how many independent sources provide evidence for the mapping?

- **Thick** (3+ sources converging): translation is likely correct. Ambiguity is about the term doing double duty, not about missing information.
- **Medium** (2 sources): proceed but flag for elicitation.
- **Thin** (1 source or code-only): mapping is an interpretation, not a translation. Candidate for fan-out.

Compute the thin-coverage ratio: (thin terms) / (total glossary terms).

- **≤30% thin**: skip fan-out, proceed to elicitation. The synopsis is rich enough.
- **>30% thin**: run Phase 3 before elicitation.

### Phase 3: Fan-out on thin sources

Well-documented systems skip this phase. Under-documented systems need it. The goal is to build richer evidence for thin-coverage terms so that elicitation questions are informed, not blind.

Run `/fan-out` on thin-coverage terms with three agent roles per term: **code** (grep implementation, trace call chains), **intent** (issues, PRs, commit messages), **pattern** (Parts Bin lookup). All agents share S.md as their research log via Synopsis dedup.

After agents return, codex filters for consensus. Update glossary: all agree → promote to medium; two agree → flag dissent; no agreement → `competing_hypotheses`; all empty → `insufficient_evidence`. Log dead ends in `open_questions` — a well-characterized dead end is worth more than an untested hypothesis.

**Parameters:** k=3 agents per term, one round only, max 10 thin terms per batch. The `/fan-out` skill handles shared memory, convergence, and pruning mechanics.

### Phase 4: Codex sniff + Elicitation (Attend — mandatory)

Before presenting to the human, send S.md to codex for review. Apply obvious improvements directly (framework leaks, weak provenance, miscalibrated confidence, missing discrepancy flags). Present only the ambiguous or debatable points to the human alongside the elicitation questions. This narrows the human's Attend to what actually requires judgment. **If codex is unavailable**, try Gemini as the reviewer. If neither is available, perform a self-review pass applying the same criteria. Log which reviewer was used or skipped.

The agent does Perceive (read sources), Cache+Filter (translate, dedupe, file), and optionally fan-out (diverge/converge on thin sources). But mapping foreign vocabulary to framework roles is a judgment call. The agent proposes candidates; the human selects. This step is Attend — without it, the pipeline emits unattended Cache. **If the human is unavailable, the pipeline stops. There is no fallback.**

**Present one question at a time.** Don't dump the full quiz. Let the human think about each mapping before seeing the next.

#### What to quiz

1. **Ambiguous translations.** For each entry in the glossary's "ambiguous mappings" table, present the competing role assignments and ask the human to select. These are the claims where error propagates fastest to Diagnose. If fan-out resolved some ambiguities, only present the survivors.
2. **Single-source structural claims.** For each claim with no convergent evidence (only one source, and fan-out didn't help), ask the human to confirm or dispute. Single-source claims are the weakest links.
3. **Coverage.** Ask whether any system term was missed or any translation should be reversed. **This question can change downstream skill specs** — if the human identifies a structural issue with the mapping approach itself (e.g., "flat mappings are too coarse"), propagate that feedback to the relevant skill spec before proceeding. Coverage questions are not just about completeness; they're about whether the mapping resolution is sufficient.

#### How to score

Each answer gets a confidence tag from the human: **high**, **medium**, **low**, or **unsure**.

- **high** — oracle is confident. Diagnose can trust this translation.
- **medium** — oracle leans one way but could be wrong. Diagnose should note uncertainty but proceed.
- **low** — oracle is guessing. Diagnose must treat this as `competing_hypotheses` and examine the source directly.
- **unsure** — oracle has no signal. Diagnose must treat this as `insufficient_evidence`.

#### What to record

Write an `## elicitation` section to `soap/S.md` (replacing any prior elicitation section on re-run) with:
- Each question asked
- The human's answer and confidence tag
- Fan-out resolution (if any terms were pre-resolved by fan-out, note which ones and how)
- Derived oracle reliability: fraction of answers at high or medium confidence

Oracle reliability below 50% is a stop signal — the translations are too uncertain for Diagnose to proceed without re-examining sources.

## Output

1. **`soap/S.md`** — built by writing claims directly, organized by the subject's own structure. For large intakes (200+ claims), use `/synopsis` for mechanical dedupe and glossary updates.
2. **Completion report** — after all sources are processed, report to the user: sources processed, claims filed, source thickness assessment, fan-out results (if triggered), ambiguous translations queued for elicitation, any sources that were inaccessible (`blocked`).
3. **Elicitation quiz** — the mandatory Attend step. Pipeline does not advance to Diagnose until the human completes the quiz.

If Synopsis is unavailable or `soap/S.md` cannot be written, Intake stops and reports the failure. Do not buffer claims in conversation context as a workaround.

## Convergence

After completing all phases (including elicitation), re-read S.md and run a self-check: are there claims in the sources that aren't in S.md? Glossary terms without mappings? Ambiguities that weren't elicited? If yes, run another pass (phases 1-4). If no, converged. Report what changed each pass so the human can see the delta shrinking. **Hard stop at 10 passes** — if still changing, the skill is oscillating. Stop, report what's fluctuating, and let the human decide.

## Contract

- **Postcondition**: every claim in the synopsis traces back through a translated claim to an original source; elicitation section records oracle confidence per ambiguous translation; thin-coverage terms have fan-out evidence or are flagged as insufficient
- **Does not**: evaluate claims or identify gaps (that's Diagnose)
- **Idempotency**: running Intake twice on the same sources produces the same synopsis. Elicitation section is replaced (not appended) on re-run, keyed by question content.
