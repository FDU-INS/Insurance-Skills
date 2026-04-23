# Stedi Best Practices

## Table of Contents
- Patient Control Number (PCN)
- Idempotency and retries
- Claim filing code selection
- Character and formatting restrictions
- Subscriber/dependent modeling
- Service-line identifiers
- Status check request strategy
- Security and operational hygiene

## Patient Control Number (PCN)

PCN is your primary claim correlation key across 277CA, 835, and status checks.

Best practices:
- Use alphanumeric only.
- Keep length at 17 chars or less.
- Use high-entropy random values (not sequential).
- Never reuse PCN for a different claim.
- Generate a new PCN on resubmissions/corrections/cancellations.

Recommended deterministic format:
- Prefix by claim type + random body (for example `P-<16charrandom>`), while still staying within payer constraints.

## Idempotency and retries

Always send `Idempotency-Key` for submission endpoints.

Rules:
- Use a fresh key per logical submission attempt.
- Reuse the same key only when retrying the same exact payload after transient failure.
- Persist idempotency keys with request hash for traceability.

Retry model:
- Retry network/timeouts with same idempotency key.
- Do not blindly retry validation failures (`400`) without payload correction.

## Claim filing code selection

Claim Filing Indicator Code must match payer expectations.

Practical workflow:
1. Try deriving payer type from eligibility response (`insuranceType`) when available.
2. Map obvious cases (`CI`, `MC`, `MA`/`MB`).
3. If not determinable, use payer-approved fallback (often `ZZ`) and monitor response.
4. On rejection, update payer-specific override map for future deterministic behavior.

## Character and formatting restrictions

Use only valid X12-compatible characters in data values.

Avoid delimiter characters in JSON data values:
- `~`
- `*`
- `:`
- `^`

Normalize and validate before submission:
- phone numbers -> digits only
- postal code formatting -> canonicalized
- date fields -> strict `YYYYMMDD`

## Subscriber/dependent modeling

If dependent has unique member ID, model them as `subscriber` and omit `dependent`.

Only include `dependent` when subscriber is different person and payer expects that relationship model.

Mismodeled subscriber/dependent is a common rejection cause.

## Service-line identifiers

Always provide deterministic service-line control identifiers:
- Professional/dental: `providerControlNumber`
- Institutional: line item control identifier

Why:
- 835 may adjudicate subsets of lines.
- You need stable line-level matching for payment and adjustments.

## Status check request strategy

For 276/277 real-time status checks:
- Wait at least 7 days after submission (and often longer).
- Start with minimal base request fields.
- Use date-of-service ranges up to 30 days and avoid future dates.
- Expand request detail only when base request returns no match.

Over-constraining status requests often reduces match rates.

## Security and operational hygiene

- Keep API key in `STEDI_API_KEY`; never hardcode.
- Redact PHI in logs by default.
- Log claim keys and transaction IDs, not full payloads, unless explicitly needed in secure traces.
- Implement webhook deduplication and idempotent consumers.
- Use environment guards so test and production cannot be mixed accidentally.
