# Stedi Claim Responses

## Table of Contents
- Response types
- Synchronous submission response
- 277CA acknowledgments
- 835 ERA responses
- Discovering inbound responses
- Correlation strategy
- Interpreting common statuses
- Duplicate handling and crossover notes

## Response types

After claim submission, you work with:

- **Immediate API response** (synchronous)
- **277CA claim acknowledgments** (asynchronous)
- **835 ERA** adjudication/remittance (asynchronous)

## Synchronous submission response

Submission APIs return immediate status and reference metadata. Common fields:

- `status`
- `claimReference.correlationId`
- `claimReference.patientControlNumber`
- `claimReference.serviceLines[].lineItemControlNumber`
- `errors[]` (when rejected by Stedi edits)
- `x12` (includes initial acknowledgment representation)

Key point: immediate success means Stedi accepted/processed submission path; it does not mean payer adjudication is complete.

## 277CA acknowledgments

`277CA` indicates whether claim data was accepted/rejected for processing stages.

Important rules:
- Rejection in 277CA is not a denial.
- Denial/payment outcomes come later in ERA/status results.
- You may receive multiple 277CAs for one claim (Stedi phase + payer phase).

Useful interpretation fields often include:
- Category code (for example `A1` accepted, `A3` unprocessable)
- Status code details (reason granularity)
- `patientAccountNumber` / referenced trace values
- Sometimes payer claim control number (PCCN) once entered payer system

## 835 ERA responses

`835` contains final adjudication/remittance details:
- paid/denied/adjusted amounts
- claim-level adjustment reasons
- service-line adjustment reasons
- payer control identifiers and payment/reassociation details

Typical correlation fields:
- claim-level patient control number
- service-line control numbers (`lineItemControlNumber`)

Transaction enrollment is required for ERA processing with most payers.

## Discovering inbound responses

### Option A: Webhooks (recommended)

Use webhook events for processed inbound transactions and fetch corresponding report payloads.

Operational requirements:
- acknowledge quickly
- store event IDs/transaction IDs
- deduplicate (retries and duplicate transmissions happen)

### Option B: Polling

Use poll endpoint with time window or page token.

Filter logic for claims response pipeline:
- `direction = INBOUND`
- `x12.transactionSetIdentifier in {277, 835}`

Persist processed transaction IDs to avoid reprocessing.

## Correlation strategy

Use deterministic keys in this order:

1. **PCN** (`claimInformation.patientControlNumber`) at claim level
2. **Stedi correlation ID** (`claimReference.correlationId`) as fallback
3. **Service-line control number** (`providerControlNumber`/`lineItemControlNumber`) for line-level mapping

Recommended internal data model:

```json
{
  "claimKey": "pcn-or-correlation-id",
  "submission": {
    "transactionId": "..."
  },
  "responses": [
    {
      "type": "277CA",
      "transactionId": "...",
      "statusSummary": "accepted|rejected"
    },
    {
      "type": "835",
      "transactionId": "...",
      "paymentSummary": "paid|partial|denied"
    }
  ]
}
```

## Interpreting common statuses

- **277CA accepted:** claim entered next processing stage; continue monitoring.
- **277CA rejected:** correct data and resubmit (frequency logic in lifecycle doc).
- **No ERA yet:** run status check if outside expected window.
- **835 with adjustments:** parse adjustment codes and retain for secondary submissions/appeals.

## Duplicate handling and crossover notes

### Duplicate handling

Payers can retransmit duplicate ERAs or repeated notifications. Use deterministic duplicate keys:
- transaction ID + type
- ERA check/EFT trace number
- claim key + payer control number + amount/date tuple

### Crossover claims

In COB scenarios, claim may be forwarded to another payer. You may receive additional responses and need separate enrollment/monitoring logic for crossover payer flows.
