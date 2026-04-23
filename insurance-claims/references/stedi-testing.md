# Stedi Testing

## Table of Contents
- Test mode vs claim testing
- Submitting test claims
- Stedi Test Payer workflow
- Expected test responses
- Correlating test responses
- Promotion checklist to production

## Test mode vs claim testing

Stedi portal test mode is primarily for eligibility-style mock workflows. Claims processing features are limited there.

For claim pipeline validation, use test claim submissions and the Stedi Test Payer workflow instead.

## Submitting test claims

API test signaling:
- JSON endpoints: set `usageIndicator` to `T`
- Raw X12 endpoints: set `ISA15` to `T`

Behavior:
- Test claims are not sent to real payer adjudication paths by default.
- You still get test acknowledgment behavior to validate submission and handling logic.

## Stedi Test Payer workflow

Use the Stedi Test Payer (for example `STEDITEST`) for end-to-end testing.

Recommended sequence:
1. Ensure provider enrollment for test payer + needed transaction type (especially `835`).
2. Submit test claim with `usageIndicator: T`.
3. Monitor for test `277CA`.
4. Retrieve generated test `835 ERA`.
5. Validate parser and correlation logic.

## Expected test responses

- `277CA`: confirms processing acceptance/rejection style behavior.
- `835 ERA`: test payer responses are deterministic and useful for validating parser/correlation pipelines.

Do not assume production payout behavior from test ERA outcomes.

## Correlating test responses

Use same keys as production:
- `patientControlNumber` for claim-level correlation
- service-line control number for line-level mapping
- transaction IDs for retrieval operations

The test environment should prove that your deterministic scripts can:
- submit
- discover inbound responses
- retrieve reports
- correlate to original claim
- classify outcome

## Promotion checklist to production

Before switching to production:
- Verify strict env separation (`STEDI_API_KEY` test vs prod secrets).
- Confirm payer IDs and enrollment status for real payers.
- Disable test payload defaults (`usageIndicator: P` in prod).
- Keep idempotency, deduplication, and retry logic enabled.
