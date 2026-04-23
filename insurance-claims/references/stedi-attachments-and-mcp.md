# Stedi Attachments and MCP

## Table of Contents
- 275 attachments overview
- Supported payer and enrollment checks
- JSON attachment flow
- X12/SFTP attachment flow
- Required attachment fields
- MCP server scope and relevance

## 275 attachments overview

`275` attachments provide supporting documents for claims (for example operative reports, imaging, medical records).

Attachment support varies by payer and by claim type. Always verify support before submission.

## Supported payer and enrollment checks

Before sending attachments:
- confirm payer supports unsolicited 275 attachments
- verify transaction enrollment requirements for 275
- validate attachment size/type constraints for target payer

If unsupported, deterministic scripts should fail with a clear, actionable message and skip submission.

## JSON attachment flow

Recommended deterministic sequence:

1. Call create-attachment endpoint to obtain:
   - pre-signed upload URL
   - attachment ID
2. Upload file via `PUT` to pre-signed URL.
3. Submit claim with attachment reference fields including attachment ID.

Benefits:
- cleaner script structure
- explicit artifact IDs
- easier retry/error recovery

## X12/SFTP attachment flow

In raw X12 and SFTP flows:
- submit claim transaction with attachment reference elements
- submit 275 attachment transaction
- ensure both reference matching identifiers

SFTP is often preferred for larger attachments or existing X12 pipelines.

## Required attachment fields

At minimum, include:
- `attachmentReportTypeCode` (document/report type)
- `attachmentTransmissionCode` (`EL` for electronic transmission through Stedi)
- one identifier path:
  - `attachmentId` (JSON upload workflow), or
  - `attachmentControlNumber` (when externally managed flow requires it)

Missing or inconsistent attachment identifiers are a common rejection source.

## MCP server scope and relevance

Stedi MCP server is primarily for eligibility workflows (`search_for_payer`, `eligibility_check`) and troubleshooting those checks.

For this insurance-claims skill:
- keep claims submission/validation/status/retrieval in deterministic scripts
- optionally use MCP-enabled eligibility checks pre-claim to improve payer/member data quality before submission

MCP should be treated as a complementary pre-claim tool, not the primary claims submission engine.
