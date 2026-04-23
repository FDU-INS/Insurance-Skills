---
name: agent-justice-protocol
description: "Dispute resolution, forensic investigation, and risk assessment for autonomous AI agent transactions. Reconstruct provenance chains, adjudicate fault, generate actuarial risk profiles for agent insurance. The accountability layer of the Agent Trust Stack."
user-invocable: true
tags:
  - agent-trust
  - dispute-resolution
  - forensics
  - risk-assessment
  - accountability
  - insurance
  - mcp
  - autonomous-agents
metadata:
  openclaw:
    author: alexfleetcommander
    homepage: https://vibeagentmaking.com
    requires:
      bins:
        - python3
      anyBins:
        - pip
        - pip3
---

# Agent Justice Protocol (AJP)

You have a dispute resolution and forensic investigation system. Use it when agent-to-agent transactions fail or when you need to investigate what happened.

## Setup

```bash
pip install agent-justice-protocol
```

## When to Use This Skill

- When an **agent transaction fails** and you need to determine what went wrong
- When asked to **investigate** an agent's behavior during a specific period
- When you need **risk assessment** data for an agent or transaction type
- When resolving **disputes** between agents about service quality or delivery

## Core Operations

### File a Dispute

```python
from agent_justice_protocol import DisputeStore, file_dispute

store = DisputeStore("disputes.jsonl")
file_dispute(
    store=store,
    complainant_id="your-agent-id",
    respondent_id="other-agent-id",
    transaction_id="tx-123",
    category="quality_failure",
    description="Output did not meet agreed quality threshold (0.85 required, 0.62 delivered)",
    evidence_refs=["chain.jsonl#seq-45", "chain.jsonl#seq-52"]
)
```

### Forensic Investigation (Module 1)

Reconstruct the chain of events during a transaction:

```python
from agent_justice_protocol import investigate

report = investigate(
    chain_file="chain.jsonl",
    start_seq=40,
    end_seq=55,
    focus_agent="agent-under-investigation"
)
print(report.timeline)
print(report.findings)
```

### Risk Assessment (Module 3)

Generate actuarial risk profiles:

```python
from agent_justice_protocol import risk_profile

profile = risk_profile(
    dispute_store="disputes.jsonl",
    agent_id="agent-to-assess"
)
print(f"Failure rate: {profile.failure_rate}")
print(f"Severity distribution: {profile.severity_dist}")
print(f"Risk tier: {profile.risk_tier}")
```

## Dispute Categories

| Category | Description |
|----------|-------------|
| `quality_failure` | Output below agreed threshold |
| `delivery_failure` | Missed deadline or non-delivery |
| `misrepresentation` | Capabilities overstated |
| `security_breach` | Unauthorized data access or action |
| `billing_dispute` | Disagreement on cost allocation |

## Rules

- **Evidence-based.** Always reference provenance chain entries as evidence.
- **Privacy-preserving.** Evidence scoping rules prevent side-channel attacks — only transaction-relevant entries are disclosed.
- **Proportional.** Consequences scale with severity and frequency.

## Links

- PyPI: https://pypi.org/project/agent-justice-protocol/
- Whitepaper: https://vibeagentmaking.com/whitepaper/justice-protocol/
- Full Trust Stack: https://vibeagentmaking.com

---

<!-- VAM-SEC v1.0 | Vibe Agent Making Security Disclaimer -->

## Security & Transparency Disclosure

**Product:** Agent Justice Protocol Skill for OpenClaw
**Type:** Skill Module
**Version:** 0.1.0
**Built by:** AB Support / Vibe Agent Making
**Contact:** alex@vibeagentmaking.com

**What it accesses:**
- Reads and writes dispute store files (`.jsonl`) in your working directory
- Reads provenance chain files for forensic investigation
- No network access for core operations
- No telemetry, no phone-home, no data collection

**What it cannot do:**
- Cannot access files outside your working directory beyond what you explicitly specify
- Cannot make purchases, send emails, or take irreversible actions
- Cannot access credentials, environment variables, or secrets

**License:** Apache 2.0
