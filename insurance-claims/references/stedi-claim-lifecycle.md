# Stedi Claim Lifecycle

## Table of Contents
- Lifecycle stages
- Edits vs repairs
- Handling edit rejections
- Resubmission and cancellation rules
- Claim Frequency Code decision table
- Payer Claim Control Number (PCCN)
- Real-time status checks

## Lifecycle stages

1. Build claim payload.
2. Run local deterministic validation.
3. Submit to Stedi.
4. Stedi applies repairs and edits.
5. Receive initial acceptance/rejection.
6. Payer receives and processes claim.
7. Receive 277CA acknowledgments.
8. Claim adjudication.
9. Receive 835 ERA.

## Edits vs repairs

### Repairs
- Automatic, deterministic normalizations.
- Example: formatting cleanup.
- No action needed from your side.

### Edits
- Validation rules that can reject submission.
- Failures return structured errors and follow-up action hints.
- You must correct and resubmit.

SNIP categories (high level) help classify failures: syntax, HIPAA constraints, balancing, situational dependencies, code set validity, service-type fit, payer/government partner specifics.

## Handling edit rejections

Recommended deterministic flow:

1. Capture full error payload and trace ID.
2. Classify errors into:
   - data format
   - missing required data
   - invalid code/value
   - balancing mismatch
3. Apply correction rules.
4. Re-run local validator.
5. Resubmit with appropriate Claim Frequency Code.

Common failures:
- invalid subscriber DOB
- invalid diagnosis/procedure code
- total claim amount != service line totals

## Resubmission and cancellation rules

You typically need:
- corrected data
- new unique PCN
- proper Claim Frequency Code
- PCCN when required

### Claim Frequency Code decision table

| Scenario | Claim entered payer system? | Code |
| --- | --- | --- |
| Stedi rejected before payer | No | `1` |
| Payer rejected before entry/adjudication | No | `1` |
| Payer rejected after entry with PCCN | Yes | `7` (except Medicare rules) |
| Correcting adjudicated claim | Yes | `7` (except Medicare rules) |
| Void/cancel existing payer-side claim | Yes | `8` |

Medicare nuance:
- Often resubmit with `1`.
- PCCN handling may differ; follow payer-specific instructions.

## Payer Claim Control Number (PCCN)

PCCN identifies the payer-side claim instance you are replacing/voiding.

Where to find PCCN:
- 277CA (`tradingPartnerClaimNumber` field family)
- 276/277 status responses
- 835 ERA claim payment info

When using code `7` or `8`, include PCCN unless payer-specific guidance says otherwise.

## Real-time status checks

Use status checks when ERA is delayed or operationally required.

Best practice sequence:
1. Wait at least 7 days after submission.
2. Start with minimal request data.
3. Use date-of-service range (avoid future dates; keep narrow but not overly narrow).
4. Add claim number/PCCN only if needed to resolve ambiguity.

Status checks are not substitutes for 277CA:
- 277CA: processing acceptance/rejection.
- 276/277 status: progression/adjudication view for claims already in payer systems.
