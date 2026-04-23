# Stedi Enrollment and Payers

## Table of Contents
- Transaction enrollment basics
- Enrollment types to track
- Payer Network usage
- Payers API usage pattern
- COB and multi-payer responsibilities
- Operational recommendations

## Transaction enrollment basics

Transaction enrollment registers a provider for specific transaction types with specific payers.

Important behavior:
- Enrollment requirements are payer-specific.
- Enrollment for one transaction type does not automatically enroll other transaction types.
- In some cases, moving enrollment to Stedi can replace existing clearinghouse enrollment for that same transaction type.

Always check payer support and enrollment requirements before production submissions.

## Enrollment types to track

Maintain enrollment status by `(provider, payer, transactionType)`:

- `837` claims (professional/institutional/dental)
- `835` ERA (typically required to receive ERAs)
- `275` attachments (where supported/required)
- `276/277` real-time status checks (may require separate enrollment)

Recommended internal status states:
- `not_started`
- `pending`
- `live`
- `rejected`
- `expired_or_revoked`

## Payer Network usage

Use Stedi Payer Network as the source of truth for:
- primary payer IDs
- aliases
- supported transaction types
- enrollment requirements by transaction

Practical lookup sequence:
1. Search by payer name and known aliases.
2. Confirm supported transaction type for current workflow.
3. Choose canonical payer ID (or approved alias) for deterministic scripts.

## Payers API usage pattern

Use API-based payer lookup in script flows:
- search candidate payer
- fetch payer details
- validate transaction support before submit

Guardrail:
- If transaction type is unsupported, block submission and return deterministic remediation guidance.

## COB and multi-payer responsibilities

Coordination of Benefits (COB) affects routing and payload requirements.

Before claim submission:
- Run COB/eligibility checks where applicable.
- Confirm primary/secondary/tertiary payer order.
- Set `paymentResponsibilityLevelCode` correctly (`P`, `S`, `T`).
- Include prior payer adjudication info for downstream payer submissions when required.

## Operational recommendations

- Cache payer lookup results with short TTL but refresh often enough for payer config changes.
- Keep explicit payer override maps for known edge cases.
- Store enrollment history with timestamps for supportability.
- Fail fast when enrollment status is not live for required transaction types.
