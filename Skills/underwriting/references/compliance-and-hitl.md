# Compliance Gates and HITL Patterns

## Sanctions Screening — 3-Gate Escalation

Sanctions screening is the most compliance-critical check in underwriting.
Use a cost-tiered escalation to avoid spending $5+ per entity when a $0.01
check would have cleared them.

### Gate 1: Basic Watchlist Check (~$0.01/entity)

- Quick lookup against primary sanctions lists (OFAC SDN, EU Consolidated,
  UK HMT, UN Security Council).
- Exact name match against watchlist entries.
- **Clear** → proceed to next pipeline step.
- **Flag** → escalate to Gate 2.

### Gate 2: Enhanced Screening (~$0.50/entity)

- Fuzzy matching with configurable threshold (typically 80% similarity).
- Alias detection and transliteration matching.
- Related entity analysis (officers, beneficial owners).
- **Clear** → proceed.
- **Flag** → escalate to Gate 3.

### Gate 3: Full Compliance Review (~$5.00 + human)

- Comprehensive screening against extended lists.
- **Mandatory HITL** — Blocking pattern. No progress until compliance officer
  explicitly clears or rejects.
- Human sees: entity details, screening results, match details, potential
  aliases, related entities.
- Human actions: clear (false positive), confirm (true match → reject
  submission), escalate to MLRO.

### Asset-Level Screening

Screen every extracted entity, not just the insured:
- Insured company and its officers
- All asset locations (country-level sanctions)
- Key persons named in the submission
- Beneficial owners (if available)

When assets are sanctioned, produce a **partial coverage proposal**:
- Identify which assets are cleared vs. restricted
- Calculate included vs. excluded insured values
- Flag for underwriter decision on partial coverage

---

## HITL Gate Inventory

A typical underwriting pipeline has 8-12 HITL gates. Below is a reference
inventory. Customise per deployment.

| # | Gate | Approving Roles | Pattern | Trigger |
|---|------|----------------|---------|---------|
| 1 | Submission Review | Underwriter, Operations | Async | Low triage confidence, unknown sender |
| 2 | Compliance Review | Compliance | Blocking | Unresolved compliance items |
| 3 | Sanctions Review | Compliance | Blocking | Sanctions flag at any gate |
| 4 | Clearance Conflict | Compliance | Blocking | Conflicting quotes for same insured |
| 5 | Identity Review | Operations | Async | Low identity confidence |
| 6 | Extraction Review | Operations | Async | Field confidence below threshold |
| 7 | Asset Classification | Operations, Underwriter | Async | Ambiguous asset type or value |
| 8 | Disambiguation | Operations, Underwriter | Async | Multiple candidate values for a field |
| 9 | Request More Info | Underwriter, Operations | Async | Critical gaps in extracted data |
| 10 | UW Input Required | Senior Underwriter | Async | Complex judgment needed (exclusions, pricing) |

### Gate Authorization

Use a policy engine (Cedar, OPA, or equivalent) to control gate access:

- **Default-deny**: No one can approve a gate unless explicitly permitted.
- **Forbid-wins**: A forbid policy always overrides a permit policy.
- **Deterministic**: Same inputs always produce the same authorization decision.
- **Outside LLM loop**: Policy evaluation happens in the orchestration layer,
  not inside the agent's reasoning. Agents cannot be prompt-injected past gates.

Example Cedar policy pattern:

```cedar
// Only compliance officers can approve sanctions review gates
permit(
  principal in Group::"compliance",
  action == Action::"approve_gate",
  resource == Gate::"sanctions_review"
);

// Block all agent tool access when kill switch is active
forbid(
  principal,
  action,
  resource
) when {
  context.kill_switch_active == true
};

// Agent can only invoke tools for cases in its assigned LoB
permit(
  principal,
  action == Action::"invoke_tool",
  resource
) when {
  resource.lob in principal.lob_access
};

// Block writes to quote system when compliance is not cleared
forbid(
  principal,
  action == Action::"write_to_quote_system",
  resource
) when {
  context.compliance_status != "cleared"
};
```

### Service Degradation

Not all external services can degrade gracefully. Compliance-critical
services must block — the pipeline cannot proceed without them.

| Service | Degradation Strategy |
|---------|---------------------|
| Enrichment API down | Skip enrichment, proceed with extraction-only data. Flag in decision package. |
| Sanctions API down | BLOCK. Cannot proceed without sanctions check. Queue for retry. |
| Licensing API down | BLOCK. Cannot verify licensing status. Queue for retry. |
| Credit check API down | Skip, proceed with available data. Flag as incomplete. |
| Model throttled | Fall through fallback chain. If all fail, queue for retry. |

**Rule**: Compliance-critical services (sanctions, licensing, clearance)
never degrade. Non-critical services (enrichment, credit checks) can be
skipped with flags in the decision package.

---

## Confidence Calibration Details

### Two-Stage Hybrid Estimation

**Stage 1: Business Rules (Deterministic, ~0ms)**

Rules evaluated in priority order:
1. Low Confidence rules first (if any match → always HITL, no override)
2. High Confidence rules second (all conditions must be met)
3. Medium Confidence is the default (anything not matching Low or High)

Low Confidence triggers (any one is sufficient):
- Financial field above monetary threshold (e.g., > $1M coverage)
- Contract-critical field (named insured, effective/expiry dates)
- OCR quality below 70%
- Multiple candidate values found
- Unrecognised document type or first submission from this broker
- Exclusion or endorsement language detected
- Sanctions fuzzy match
- Field value outside expected range

High Confidence triggers (all must be met):
- Known broker + recognised document type
- Low-risk field type (broker name, submission date, reference number)
- Exact match in expected document location
- OCR quality > 90%
- Historical accuracy > 98% for this broker/document combination
- No contradictory signals

**Stage 2: Self-Consistency Sampling (Statistical, ~2-5s)**

For Medium Confidence outputs only:

```python
# Pseudocode for self-consistency sampling
async def self_consistency_check(prompt, field_name, config):
    n_samples = config.sample_count  # default: 5
    temperature = config.temperature  # default: 0.7

    # Run N extractions in parallel
    responses = await asyncio.gather(*[
        extract_field(prompt, temperature=temperature)
        for _ in range(n_samples)
    ])

    # Compute agreement
    values = [r.value for r in responses]
    most_common = Counter(values).most_common(1)[0]
    agreement_rate = most_common[1] / n_samples

    return {
        "value": most_common[0],
        "agreement_rate": agreement_rate,
        "confidence_band": map_to_band(agreement_rate),
        "all_samples": values
    }
```

Configuration is per-field-criticality and per-LoB via policy packs:
- `sample_count`: 3-10 (default 5)
- `temperature`: 0.5-1.0 (default 0.7)
- `model_tier`: Can use cheaper model for sampling
- `timeout`: Per-sample and total timeout with fail-safe to HITL

### ECE Monitoring

Expected Calibration Error measures prediction-accuracy alignment:

```
ECE = SUM over bins( |accuracy_in_bin - midpoint_of_bin| * (cases_in_bin / total) )
```

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| ECE (overall) | < 0.05 | >= 0.08 | >= 0.10 |
| Override rate (per field) | 5-15% | > 20% or < 2% | > 25% |
| High-confidence error rate | < 1% | >= 2% | >= 5% |

**Recalibration triggers**:
- Critical ECE → auto-tighten thresholds by 5 percentage points
- Override rate > 20% → flag field for prompt review
- High-confidence errors > 5% → automatic firebreak (field reverts to HITL)

---

## Automation Bias Safeguards

### Safeguard 1: Confidence Bands, Not Scores

Never display raw numeric confidence (e.g., "87.3%") to reviewers. Use bands:
- **High** (green) — "AI assessment: High confidence"
- **Medium** (amber) — "AI assessment: Medium confidence — review recommended"
- **Low** (red) — "AI assessment: Low confidence — careful review required"

Numeric precision creates false authority that anchors reviewer judgment.

### Safeguard 2: Independent Assessment First

When a reviewer opens a HITL task:
1. Show the source document with relevant section highlighted
2. Prompt: "Review the highlighted section. What is the [field name]?"
3. Reviewer enters their independent assessment
4. **Only then** reveal the AI value and confidence band
5. If they agree → confirm with minimal friction
6. If they disagree → prompt for rationale

### Safeguard 3: Progressive Disclosure

Reveal AI reasoning in stages:
1. Source document with highlights
2. Reviewer's independent assessment prompt
3. AI value and confidence band
4. Full AI reasoning chain (expandable)

### Safeguard 4: Minimum Interaction

"Confirm" button requires:
- Evidence section viewed (tracked via viewport events)
- Independent assessment entered
- AI value viewed
- For critical fields: explicit "I have reviewed the source evidence" checkbox

### Safeguard 5: Rubber-Stamp Detection

Track review time distributions per reviewer:
- Reviews under 10 seconds → flagged as potential rubber-stamps
- Mean review time < 10s over 20-task window → supervisor alert
- Rubber-stamp rates included in monitoring dashboard

---

## Firebreak Controls

Emergency controls to halt or restrict automation:

| Level | Name | Effect | Authorization |
|-------|------|--------|---------------|
| 1 | Continue Manually | Pause this case only | Any operator |
| 2 | Pause Workflow Type | All cases of this type revert to manual | Admin or supervisor |
| 3 | Shadow-Only | AI runs but does not write to downstream systems | Admin only |
| 4 | Kill Switch | Complete halt of automated processing | Dual authorization (Admin AND Compliance) |

Design principles:
- Firebreaks override operating modes immediately for new cases.
- In-flight cases under a firebreak revert to manual processing.
- Deactivating a firebreak does NOT auto-restore previous mode — explicit
  admin action required to re-enable automation.
- All firebreak activations/deactivations are recorded in an immutable audit ledger.
