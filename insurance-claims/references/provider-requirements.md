# Provider and Payer Requirements (Stedi)

## Purpose

Use this as a deterministic preflight checklist before any claim, status, attachment, or ERA-related action.

## What to verify first

For each workflow, evaluate requirements by tuple:

`(provider, payer, transactionType, environment)`

Where:
- `provider` = NPI + provider identity data used in enrollment
- `payer` = canonical payer ID from Stedi network/API
- `transactionType` = one of `837P`, `837I`, `837D`, `835`, `276/277`, `275`
- `environment` = test or production

## Authoritative sources

- Payer Network: [https://www.stedi.com/healthcare/network](https://www.stedi.com/healthcare/network)
- Transaction enrollment docs: [https://www.stedi.com/docs/healthcare/transaction-enrollment](https://www.stedi.com/docs/healthcare/transaction-enrollment)
- Payers API (programmatic support/metadata checks)

## Core rules

1. **Enrollment is clearinghouse-specific**
   - If payer requires enrollment, prior enrollment through another clearinghouse does not automatically satisfy Stedi enrollment.

2. **835 ERA is single-clearinghouse**
   - Switching ERA enrollment to Stedi typically stops ERA delivery through previous clearinghouse for that payer/provider.

3. **Claims can be sent without ERA switch**
   - You can submit claims through Stedi and keep ERAs routed elsewhere until ERA enrollment is switched.

4. **Credentialing is outside Stedi**
   - Providers credential directly with payers.
   - Stedi does not run credentialing workflows.

5. **Requirements vary by transaction type**
   - Enrollment/support for `837` does not imply support/enrollment for `835`, `275`, or `276/277`.

## Deterministic preflight checks

Run these before calling submission/status actions:

1. **Resolve payer**
   - Normalize input payer name/alias to canonical payer ID.
   - If unresolved, fail with action: `lookup_payer`.

2. **Check transaction support**
   - Confirm target transaction type is supported for payer.
   - If unsupported, fail fast with actionable message.

3. **Check enrollment requirement**
   - If enrollment required, verify local enrollment status is `live`.
   - If not `live`, block action and return next-step guidance.

4. **Check provider identifiers**
   - Ensure NPI and any payer-specific provider identifiers required by workflow are present.
   - For insurance discovery scenarios, optional Medicaid Provider ID can improve some payer results.

5. **Check environment safety**
   - Test and production credentials/config must not be mixed.
   - Block if environment mismatch is detected.

## Suggested error contract

Use structured errors so the skill can provide clear remediation:

```json
{
  "ok": false,
  "code": "ENROLLMENT_REQUIRED",
  "message": "Provider is not live for payer 6400 and transaction 835.",
  "context": {
    "providerNpi": "1999999984",
    "payerId": "6400",
    "transactionType": "835"
  },
  "nextActions": [
    "Submit enrollment request",
    "Check enrollment status in Stedi portal/API",
    "Retry when status is live"
  ]
}
```

## Minimal policy matrix

Track this internally for deterministic behavior:

```json
{
  "providerNpi": "1999999984",
  "payerId": "6400",
  "transactions": {
    "837P": { "supported": true, "requiresEnrollment": true, "enrollmentStatus": "live" },
    "835":  { "supported": true, "requiresEnrollment": true, "enrollmentStatus": "pending" },
    "276/277": { "supported": true, "requiresEnrollment": true, "enrollmentStatus": "live" },
    "275":  { "supported": false, "requiresEnrollment": false, "enrollmentStatus": "not_started" }
  }
}
```

## How this should be used in the skill

- Call the preflight checker before:
  - claim submissions
  - claim status checks
  - attachment submissions
  - ERA retrieval operations dependent on enrollment
- If any check fails, stop execution and return deterministic remediation steps instead of attempting a best-effort API call.
