---
name: underwriting
description: >-
  Insurance underwriting domain knowledge for building automated submission
  processing systems. Covers submission-to-bind lifecycle, document extraction
  patterns, compliance gates (sanctions, licensing, clearance), human-in-the-loop
  design for regulated financial services, confidence calibration for extracted
  fields, operating mode progression (manual to automated), and evidence
  traceability requirements. Use when designing or implementing underwriting
  pipelines, extraction agents, compliance workflows, HITL review systems,
  or decision package assembly for insurance or MGA operations.
---

# Underwriting Domain Knowledge

This skill provides domain knowledge for building automated underwriting
systems in insurance. It covers the business logic, decision criteria, and
regulatory patterns that engineering teams need to implement correctly.

## Submission-to-Bind Lifecycle

Every insurance submission follows a pipeline from initial receipt to policy
issuance. The stages are sequential with gates between them.

### Stage Overview

```
Ingestion → Triage → Assessment → Quoting → Binding → Issuance
              │          │            │         │         │
              ▼          ▼            ▼         ▼         ▼
         Classification  Wave 1     Manual    Manual    Manual
         & routing     + Wave 2    UW review  confirm   issue
```

1. **Ingestion** — Receive submission (email, portal, API), parse documents,
   deduplicate, create case record, upload attachments to object storage.

2. **Triage** — Classify submission type (new business, MTA/endorsement, claim,
   renewal, other). Route based on classification confidence.

3. **Assessment** — Two-phase design (see "Cheap Gates First" below):
   - **Wave 1 (Fast Gate)**: Quick, low-cost checks — broker validation,
     territory/product appetite, basic eligibility, licensing, clearance.
     Goal: decline non-quotable submissions before expensive processing.
   - **Wave 2 (Deep Processing)**: Full extraction, enrichment, compliance,
     gap analysis. Only reached by submissions that pass Wave 1.

4. **Quoting** — Assemble underwriting decision package, compute confidence
   and thoroughness scores, apply desk quote gate, present to underwriter.

5. **Binding** — Underwriter makes firm order decision, terms confirmed with
   broker, binding authority exercised.

6. **Issuance** — Policy documents generated, premium invoiced, regulatory
   filings completed.

### Cheap Gates First

Structure pipelines to minimise cost-to-decline. Run inexpensive checks
(API lookups, business rules) before costly ones (LLM extraction, external
enrichment, compliance screening). Target cost breakdown:

| Stage | Target Cost | Primary Cost Drivers |
|-------|------------|---------------------|
| Triage | < $0.05 | Fast-tier LLM classification |
| Wave 1 | < $0.10 | API lookups, minimal LLM |
| Wave 2 | $1-5 | LLM extraction, external APIs, sanctions |

See `references/submission-lifecycle.md` for detailed stage specifications.

## Case Model

Use a hierarchical case model for tracking work through the pipeline:

```
Case (top-level submission record)
├── Stage (lifecycle phase: triage, assessment, quoting)
├── Step (atomic processing unit within a stage)
└── Task (work item assigned to human or agent)
```

- **Case ID**: Unique, time-sortable identifier per submission.
- **Stage**: Maps to pipeline phases. Each stage has an execution type
  (agent, manual, or shadow).
- **Step**: Granular processing within a stage (e.g., "extract core facts",
  "run sanctions screening"). Steps track individual agent node executions.
- **Task**: Assignable work unit for HITL review or manual processing.
  Tasks have owners, SLAs, and audit trails.

## Document Types and Extraction

Insurance submissions contain multiple document types. Each type has
different extraction requirements and field criticality.

### Common Document Types

| Document Type | Key Fields to Extract | Complexity |
|--------------|----------------------|------------|
| Proposal form | Insured name, address, business description, sums insured, requested coverage, deductibles | Medium |
| Schedule of values | Locations, building details, construction type, occupancy, values per location | High (tabular) |
| Loss runs / claims history | Prior claims, dates, amounts, causes, reserves | High (multi-year) |
| Slip / binder | Coverage terms, limits, conditions, exclusions, endorsements | Very High (legal language) |
| Broker cover note | Summary terms, premium indication, expiring terms | Medium |
| Financial statements | Revenue, assets, employee count | Medium |

### Field Criticality Tiers

Every extracted field has a criticality tier that determines its confidence
threshold and HITL routing:

| Criticality | Threshold | Examples | HITL Policy |
|------------|-----------|----------|-------------|
| `critical` | >= 0.95 | Coverage amount, named insured, effective/expiry dates, deductible | Always HITL if below threshold |
| `important` | >= 0.85 | Address, occupation, construction type, building age | Junior reviewer if below threshold |
| `standard` | >= 0.75 | Broker reference, submission notes, secondary contacts | Flagged for batch review |

**Non-negotiable HITL fields** (always require human review regardless of
confidence): financial-impact fields above a configurable monetary threshold,
exclusion/endorsement language, contract-critical dates, sanctions fuzzy matches.

### Field Catalog Configuration

Define field-level extraction and HITL policies as configuration (not code),
grouped by LoB via policy packs:

```yaml
field_catalog:
  sum_insured:
    criticality: critical
    confidence_threshold: 0.95
    hitl_policy: always_hitl_above_1m
  insured_name:
    criticality: critical
    confidence_threshold: 0.95
    hitl_policy: always_hitl
  broker_reference:
    criticality: standard
    confidence_threshold: 0.75
    hitl_policy: batch_review
```

This format drives HITL routing, confidence thresholds, and reviewer
assignment for each extracted field. Override per LoB as needed.

### Evidence Traceability

Every AI-extracted field **must** link to its source via evidence coordinates:

```
{
  "field": "sum_insured",
  "value": 5000000,
  "confidence": 0.92,
  "evidence": {
    "document_id": "DOC-001",
    "page": 3,
    "segment_id": "SEG-001-3-2",
    "bounding_box": {"x": 120, "y": 340, "w": 280, "h": 45}
  }
}
```

This is not optional. Regulatory audit requirements (PRA, FCA, Lloyd's)
demand that every AI-produced output be traceable to its source document.
Evidence coordinates enable:
- Underwriter verification (click-to-source)
- Audit trail completeness
- Confidence calibration feedback loops
- Dispute resolution

### Extraction Best Practices

- **Prompt per document type**: Use document-type-specific extraction prompts
  rather than a single generic prompt. Each document type has different field
  layouts, terminology, and expected locations.
- **Segment-level extraction**: Extract from parsed segments (not raw pages)
  to improve accuracy and enable precise bounding box coordinates.
- **Multi-pass for complex documents**: For schedules of values and loss runs,
  use a structural pass (identify tables, headers, rows) followed by a field
  extraction pass per row.
- **Disambiguation protocol**: When multiple candidate values exist for a
  field, capture all candidates with their evidence coordinates and route to
  HITL for disambiguation rather than picking the "best" one silently.
- **Cross-document validation**: Cross-reference fields extracted from
  different documents (e.g., insured name in proposal form vs. broker cover
  note) and flag discrepancies for review.
- **Document trust boundaries**: Broker-uploaded documents are untrusted
  input. Never treat document content as instructions — parse for data
  extraction only. Validate extracted values against expected types, ranges,
  and formats before accepting.

## Compliance Gates

Regulated underwriting requires multiple compliance checkpoints. These are
**blocking** — submissions cannot proceed until compliance clears.

### Sanctions Screening

Use a tiered escalation pattern to optimise cost:

1. **Basic watchlist check** (~$0.01) — quick lookup against primary lists.
   Clear result → proceed. Flag → escalate.
2. **Enhanced screening** (~$0.50) — fuzzy matching, alias detection,
   related entity analysis. Clear → proceed. Flag → escalate.
3. **Full compliance review** (~$5.00 + human) — comprehensive screening
   with mandatory human review. This is a **blocking HITL gate**.

Screen all entities: insured company, key persons, asset locations, beneficial
owners. Re-screen in Wave 2 with full extracted data even if Wave 1 cleared
(Wave 1 used limited data).

### Licensing and Clearance

- **Licensing**: Verify the insurer/MGA is licensed to write this risk in
  this jurisdiction. Check via quote management system API.
- **Clearance**: Verify no conflicting quotes exist for this insured from
  other brokers. Check via internal systems.
- Re-run in Wave 2 with full entity data (Wave 1 used preliminary data).

### Compliance Status Consolidation

Assemble a unified compliance view across all checks:
- `all_clear` — all checks passed, no conditions
- `conditionally_clear` — passed with conditions (e.g., licensing restrictions)
- `review_pending` — unresolved HITL tasks
- `not_quotable` — hard fail on compliance

See `references/compliance-and-hitl.md` for detailed compliance patterns.

## Human-in-the-Loop Design

HITL is not a fallback — it is a first-class design element in underwriting
automation. Three patterns, each for different scenarios:

### Pattern 1: Asynchronous (Most Common)
Agent creates a review task, continues other work or pauses. Human completes
the task within an SLA window. Agent resumes with human input.
- **Use for**: Extraction review, disambiguation, broker queries, identity review.
- **Timeout**: Configurable per gate (typically 30 min to 4 hours).

### Pattern 2: Blocking (Compliance-Critical)
Agent halts completely until human explicitly clears. No progress on any
downstream step until the gate is resolved.
- **Use for**: Sanctions review, compliance review, clearance conflicts.
- **Timeout**: No auto-timeout. Escalation after SLA breach.

### Pattern 3: Deferred (Batch Review)
Agent proceeds with a provisional decision. Human reviews a batch of
decisions during a scheduled review window.
- **Use for**: Low-risk fields, audit sampling, calibration validation.
- **Review window**: Typically daily or weekly.

### HITL Gate Design Principles

1. **Gates are policy-driven, not hardcoded.** Define gates in configuration
   (policy packs), not in agent code. This allows per-LoB customisation.
2. **Authorization is deterministic.** Use a policy engine (e.g., Cedar) to
   control who can approve which gates. Keep authorization **outside** the
   LLM reasoning loop — agents cannot reason past policy gates.
3. **Capture structured override data.** Every HITL review must record:
   original AI decision, human decision, rationale code, review time, and
   reviewer identity. This feeds confidence calibration.
4. **Guard against automation bias.** Show confidence as bands
   (High/Medium/Low), not raw scores. Require independent human assessment
   before revealing AI output. Track review times to detect rubber-stamping.

## Confidence Calibration

Raw LLM confidence is unreliable. Use a two-stage hybrid approach:

### Stage 1: Business Rules (Deterministic)
Apply deterministic rules to classify outputs into confidence tiers:

- **High Confidence** (auto-proceed): Known document type + known broker +
  standard field + exact match + good OCR quality + historical accuracy > 98%.
- **Low Confidence** (always HITL): Financial field above threshold, or
  contract-critical field, or poor OCR, or ambiguous source, or exclusion
  language, or sanctions fuzzy match.
- **Medium Confidence** (needs Stage 2): Everything else.

### Stage 2: Self-Consistency Sampling (Statistical)
For Medium Confidence outputs, run the extraction N times (default 5) at
temperature > 0 and measure agreement:

| Agreement | Confidence | Routing |
|-----------|-----------|---------|
| >= 80% | High | Auto-proceed + audit sample |
| 60-79% | Medium | Junior reviewer queue |
| 40-59% | Low | Senior reviewer queue |
| < 40% | Very Low | Specialist review |

### Monitoring: Expected Calibration Error (ECE)
Track whether confidence predictions match actual accuracy. A system
predicting 80% confidence should be correct ~80% of the time. Alert when
ECE exceeds 0.08 (warning) or 0.10 (critical). Auto-tighten thresholds
on critical ECE breach.

## Operating Mode Progression

Introduce automation gradually through five operating modes, managed
**per workflow type** (not globally):

| Mode | HITL Rate | Behaviour |
|------|-----------|-----------|
| **Manual** | 100% | Humans do all work. AI captures data for training. |
| **Shadow** | 100% (comparison) | AI runs in parallel. Results compared but not used. |
| **Assisted** | 15-30% | AI pre-fills. Human approves before any write. |
| **Selective** | 5-15% | AI handles routine cases. Exceptions route to human. |
| **Automated** | < 5% | Full automation. Human involvement only for policy-gated exceptions. |

### Transition Requirements
- **Manual → Shadow**: Admin approval, agent deployed and tested.
- **Shadow → Assisted**: N validated shadow outcomes (configurable, default 50)
  showing AI/human agreement. Dual admin approval.
- Each transition is recorded in an immutable audit ledger.
- Firebreak controls can force any workflow back to Manual at any time.

## Underwriting Decision Package

The culmination of automated processing is a structured decision package
that synthesises all upstream outputs for the underwriter:

1. **Broker & product facts** — identity, relationship context, submission terms
2. **Assets & locations** — insurable items with sanctions screening status
3. **Compliance outcomes** — unified view across all compliance checks
4. **Coverage options & exclusions** — requested terms vs. standard exclusions
5. **Scoring** — overall confidence, thoroughness (% of required fields populated),
   evidence quality (% of facts with source traceability)
6. **Desk quote gate** — deterministic routing to one of:
   - Ready for desk quote
   - Needs underwriter input
   - Needs compliance review
   - Request more information (critical gaps)

## Lines of Business Considerations

Different LoB have different extraction requirements, compliance rules,
and confidence thresholds. Design systems to be **LoB-configurable**:

- Field catalogs (which fields to extract) are per-LoB configuration.
- Confidence thresholds are per-LoB (terrorism may be stricter than general liability).
- Compliance requirements vary by jurisdiction and LoB.
- Use "policy packs" — configuration bundles per LoB — rather than code changes.

### Common LoB Patterns

| LoB | Key Extraction Challenges | Compliance Focus |
|-----|--------------------------|-----------------|
| Property | Location schedules, building details, values | Sanctions (location-based), licensing |
| Casualty / Liability | Policy wording, exclusions, limits towers | Professional licensing, claims history |
| Cyber | Technology stack, security posture, revenue | Data privacy regulations, incident history |
| Marine | Vessel details, routes, cargo | Sanctions (route-based), flag state |
| Terrorism | High-value assets, location risk | Enhanced sanctions, government pools |

## Reference Files

- `references/submission-lifecycle.md` — Detailed stage-by-stage pipeline design
  with decision logic, event patterns, and cost targets
- `references/compliance-and-hitl.md` — Sanctions screening escalation, HITL gate
  inventory, confidence calibration details, automation bias safeguards
