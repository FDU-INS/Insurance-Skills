# Submission Lifecycle — Detailed Pipeline Design

## Stage 1: Email Ingestion

**Trigger**: Email arrives at submission inbox (Gmail API, Exchange, or portal upload).

### Pipeline Nodes

1. **Email Receive** — Capture email metadata, body, and attachments via API.
2. **Deduplication** — Check for existing case with same (sender, subject hash,
   attachment hashes). Duplicate → link to existing case, stop.
3. **Case Creation** — Assign unique case ID, create case record in primary
   datastore, start workflow execution with case ID as execution name
   (provides idempotency — same case ID cannot create two executions).
4. **Document Upload** — Upload attachments to object storage with path
   structure: `{lob_id}/{case_id}/{document_id}`. Emit `document.uploaded`.
5. **Document Parsing** — Parse each document into segments with bounding boxes.
   Assign segment IDs: `SEG-{doc_id}-{page}-{index}`. Store segments in
   relational database for SQL querying.

**Key outputs**: case_id, document IDs, segment IDs with bounding boxes.

**Events**: `email.received`, `email.duplicate_detected`, `case.created`,
`document.uploaded`, `document.parsed`.

---

## Stage 2: Triage (Agent)

**Trigger**: `case.created` event.

### Classification

Determine submission type: `new_submission`, `MTA/endorsement`, `claim`,
`renewal`, `complaint`, `other`.

**Model tier**: Fast (cheapest model) — this is classification, not reasoning.

**Decision logic**:
- Known broker + "submission" in subject + has attachments → high confidence `new_submission`
- Known broker + amendment/endorsement keywords → `MTA`
- Claim keywords + policy number reference → `claim`
- Complaint language patterns → `complaint`
- Everything else → `other` (always HITL)

### Confidence Assessment (Two-Stage)

**Stage 1 (Business rules)**:
- Known broker + standard subject + expected attachments → HIGH (>90%)
- Known broker + unusual subject OR unknown attachments → MEDIUM (70-90%)
- Unknown sender OR ambiguous OR multiple classifications → LOW (<70%)

**Stage 2 (Self-consistency, medium only)**:
Run classification 5x at temperature=0.7, measure agreement.

### Routing

| Confidence | Action |
|-----------|--------|
| HIGH (>90%) | Auto-proceed |
| MEDIUM, >80% agreement | Auto-proceed + 5% audit sample |
| MEDIUM, 60-80% agreement | Async HITL (junior reviewer, 30-min timeout) |
| LOW (<70%) | Async HITL (senior reviewer) |
| `other` classification | Always HITL |

### HITL Resolution (if triggered)

Human sees: email preview, proposed classification, confidence band, evidence.
Human actions: confirm, override classification, reject (not relevant).
Capture: original AI decision, human decision, override rationale, review time.

**Events**: `triage.started`, `triage.classification_done`, `triage.hitl_required`,
`triage.completed`, `triage.rejected`.

---

## Stage 3: Wave 1 — Fast Gate (Agent)

**Purpose**: Minimise cost-to-decline. Fast, cheap checks before expensive
deep processing.

**Trigger**: Triage completed with `new_submission` classification.

### Checks (Sequential)

1. **Broker Validation**
   - Known broker? Query knowledge base for broker entity.
     - Known + valid → proceed
     - Known + expired/suspended → HITL (broker onboarding)
     - Unknown → HITL (new broker, requires onboarding)
   - Broker in appetite? Cross-reference broker tier against product appetite rules.
   - **Model tier**: None — lookup + business rules.

2. **Product/Territory Signal**
   - Is the submission for a product the insurer writes?
   - Is the territory within appetite?
   - **Model tier**: Fast (lightweight extraction of product/territory mentions).
   - Clear match → proceed. No match → decline. Ambiguous → HITL.

3. **Basic Customer Identity**
   - Extract customer/insured name from email or first attachment.
   - Confirm identity via quote management API.
   - High confidence → proceed. Low confidence → HITL (identity review).

4. **Basic Eligibility**
   - Licensing eligibility check via quote management API.
   - Internal clearance check.
   - Licensed + cleared → proceed. Not licensed → decline.
     Clearance conflict → HITL (clearance review).

5. **Wave 1 Gate Decision**
   - All passed → proceed to Wave 2.
   - Any hard fail → decline, emit rejection event.
   - Any HITL triggered → pause, wait, re-evaluate.

**Cost target**: < $0.10 per submission.
**Events**: `broker.validated`, `eligibility.checked`, `wave1.completed`.

---

## Stage 4: Wave 2 — Deep Processing (Agent)

**Purpose**: Full extraction, enrichment, compliance, and decision package
preparation. Only reached by submissions that passed Wave 1.

### A. Sequential Extraction (order matters)

1. **Core Risk Facts** — Insured name, address, business description, sums
   insured, policy period, deductibles.
   - Model tier: Balanced.
   - Evidence coordinates mandatory on every field.
   - Financial fields → always HITL. Contract-critical → always HITL.

2. **Assets & Locations** — Properties, buildings, construction, occupancy,
   values per location.
   - Depends on: Core Risk Facts (need insured identity to disambiguate).
   - Model tier: Balanced.

3. **Limits & Coverage** — Coverage types, limits, sub-limits, extensions,
   exclusions, conditions.
   - Depends on: Core Risk Facts + Assets.
   - Model tier: Premium (exclusion language requires complex reasoning).
   - Exclusion/endorsement language → always HITL.

4. **Pricing Signals** — Prior premium, loss history, broker-indicated rate.
   - Depends on: All above.
   - Model tier: Balanced.
   - Conflicting pricing signals → HITL (disambiguation).

### B. Parallel Enrichment (independent, concurrent)

5. **Company Registry Lookup** — Registration status, officers, filings
   (e.g., Companies House for UK, SEC for US).
6. **Credit/Business Data Enrichment** — Credit risk score, employee count,
   revenue, industry codes (e.g., D&B, Experian).
7. **Internal Knowledge Lookup** — Prior submission history, claim history,
   relationship notes from internal data sources.

### C. Compliance (parallel with enrichment, some gates blocking)

8. **Asset-Level Sanctions Screening** — Screen all extracted entities against
   sanctions lists using the 3-gate escalation pattern (see compliance-and-hitl.md).
9. **Company Sanctions Check** — Same pattern for insured company entity.
10. **Advanced Licensing & Clearance** — Re-run with full extracted data
    (Wave 1 used preliminary data). Cache results to avoid duplicate API calls.

### D. Assembly & Decision Package

11. **Gap Resolution** — Compare extracted data against field catalog requirements.
    Missing critical fields → HITL (draft clarification questions for broker).
12. **Decision Package Assembly** — Compile all data into structured package
    with confidence, thoroughness, and evidence quality scores.
    Model tier: Premium (summary and scoring requires reasoning).
13. **Quote System Draft** — Create submission in quote management system in
    DRAFT state. This is a controlled write — exactly-once semantics required.

**Cost target**: $1-5 per submission.
**Events**: `extraction.started`, `extraction.completed`, `enrichment.completed`,
`compliance.completed`, `package.assembled`, `submission.created`.

---

## Event Catalog Pattern

Use a consistent event naming convention across all stages:

```
{domain}.{action}

Examples:
  email.received
  case.created
  triage.completed
  extraction.field_extracted
  sanctions.cleared
  package.assembled
  submission.created
```

Every event payload should include:
- `case_id` — which case this event belongs to
- `lob_id` — Line of Business
- `timestamp` — ISO 8601 UTC
- `actor_type` — `agent` or `human`
- `operating_mode` — current operating mode for audit
- `correlation_id` — for distributed tracing

---

## Orchestration Pattern

Use a hybrid orchestration approach:

- **State machine** for authoritative case state,
  exactly-once semantics on critical writes, and long-running pause/resume.
- **Event bus** for fan-out notifications, decoupled
  analytics consumption, and audit trail population.

The state machine owns the "what happens next" decisions. The event bus
distributes "what just happened" notifications. Never use the event bus
for state transitions — that creates eventual consistency bugs in a
pipeline that requires strict ordering.