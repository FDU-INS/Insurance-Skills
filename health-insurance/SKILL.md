---
name: Health Insurance
slug: health-insurance
version: 1.0.0
homepage: https://clawic.com/skills/health-insurance
description: Compare health insurance plans, estimate total yearly costs, and choose coverage that fits medical usage, prescriptions, and financial risk.
changelog: Initial release with plan comparison workflows, annual cost modeling, enrollment timing guidance, and local memory for recurring insurance decisions.
metadata: {"clawdbot":{"emoji":"🏥","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidelines and memory initialization.

## When to Use

User needs help choosing, comparing, or renewing health insurance coverage.
Agent evaluates medical usage patterns, estimates yearly costs across plan types, and recommends a plan strategy with clear trade-offs.

## Architecture

Memory lives in `~/health-insurance/`. See `memory-template.md` for structure.

```
~/health-insurance/
├── memory.md         # Status, profile, preferences, active decisions
├── comparisons/      # Plan comparisons and scenario snapshots
├── renewals/         # Renewal timelines and action logs
└── notes/            # Follow-up questions and pending documents
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Coverage framework | `coverage-framework.md` |
| Annual cost modeling | `cost-model.md` |
| Comparison checklist | `comparison-checklist.md` |
| Enrollment and renewal playbook | `enrollment-playbook.md` |

## Core Rules

### 1. Lock Decision Context First
Before comparing plans, clarify:
- Coverage target: individual, couple, or family
- Source: employer plan, public marketplace, private broker, or government program
- Geography and provider access requirements
- Hard constraints: budget ceiling, medication continuity, renewal deadline

### 2. Build a Real Utilization Profile
Estimate expected care load before discussing premiums:
- Routine care frequency (primary care, specialist, urgent care)
- Ongoing prescriptions and refill cadence
- Known procedures, therapies, or recurring diagnostics
- Worst-case risk profile for unexpected events

### 3. Compare Plan Mechanics Before Price
Always evaluate these mechanics before deciding on monthly premium:
- Network fit for current clinicians and facilities
- Deductible, out-of-pocket max, and coinsurance structure
- Copay design by care type (primary, specialist, urgent, emergency)
- Referral and prior-authorization friction for expected treatments
- Prescription formulary coverage for required medications

### 4. Model Yearly Cost With Scenarios
Use `cost-model.md` to calculate low, expected, and high-use annual totals.
Include premium, deductible exposure, copays, coinsurance, and non-covered risk.
Recommend using expected-cost and downside-risk together, not premium alone.

### 5. Protect Against Coverage Failure Modes
Run a risk check before final recommendation:
- Out-of-network emergency and balance-billing exposure
- Drug tier surprises and step-therapy limitations
- Referral bottlenecks that delay care
- High deductible plans that look cheap but shift excessive risk

### 6. Execute Enrollment With Evidence
Use `enrollment-playbook.md` to define exact actions, deadlines, and proof artifacts.
Store plan IDs, effective dates, and support contacts for appeal or billing disputes.
Never claim enrollment is complete without confirmation evidence.

### 7. Persist Data Only With Explicit Approval
Before writing to `~/health-insurance/memory.md`, ask for explicit confirmation.
Store only durable insurance context the user wants remembered for future decisions.

## Common Traps

- Choosing by monthly premium only -> hidden total annual cost becomes unaffordable.
- Ignoring provider network fit -> forced provider changes and unexpected out-of-network bills.
- Skipping formulary checks -> medication cost spikes after enrollment.
- Assuming all PPO or HMO plans behave similarly -> referral and authorization surprises.
- Treating deductible and out-of-pocket max as equivalent -> underestimating downside risk.
- Missing enrollment deadlines -> delayed coverage or locked plan options.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Nothing. This skill is instruction-only and local by default.

**Data stored locally:**
- Insurance profile and comparison context explicitly approved by the user.
- Stored in `~/health-insurance/memory.md`.

**This skill does NOT:**
- Access insurer or broker APIs automatically.
- Submit enrollment forms or claims without user direction.
- Read files outside `~/health-insurance/` for storage.
- Write memory without explicit user confirmation.
- Modify its own core instructions or auxiliary files.

## Trust

This is an instruction-only skill focused on structured health insurance decisions.
No credentials are required and no external service access is needed.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `health` — health planning context that informs insurance priorities
- `doctor` — provider interaction planning and visit preparation
- `compare` — structured side-by-side decision frameworks
- `money` — budgeting and cash-flow planning for premium and out-of-pocket costs

## Feedback

- If useful: `clawhub star health-insurance`
- Stay updated: `clawhub sync`
