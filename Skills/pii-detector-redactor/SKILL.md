---
name: pii-detector-redactor
description: |
  Detects and redacts personally identifiable information from documents and agent outputs. Identifies names, addresses, email addresses, phone numbers, national insurance numbers, passport details, bank account numbers, and other PII categories with configurable redaction styles and audit logging for GDPR compliance.
version: "1.0.0"
author: "agentops"
license: "MIT"
x-agent:
  industries: [cross-industry]
  risk_level: elevated
  requires_approval: false
  memory_blocks: []
  mcp_dependencies: []
  tools: [file-read]
  trigger_keywords: [PII, redaction, personal data, GDPR, data protection, anonymise, privacy]
  run_after: []
  compatibility: "Agent Platform >= 1.0"
---

# PII Detector and Redactor

## Purpose

Scans documents and agent-generated outputs to identify personally identifiable information across multiple PII categories, then applies configurable redaction to prevent unauthorised disclosure. The skill supports detection of both structured PII (such as national insurance numbers and email addresses following known formats) and unstructured PII (such as names embedded in free text or contextual identifiers that could re-identify individuals). All detection and redaction actions are logged to an audit trail to satisfy GDPR accountability requirements under Article 5(2).

## When to Use

- Before sharing agent outputs externally where the source data may contain personal information about individuals
- When processing customer correspondence, support tickets, or feedback that must be anonymised for analysis
- Prior to storing conversation logs or training data where data subjects have not consented to retention of their personal details
- When generating reports from datasets containing employee records, patient information, or client details
- As a pre-processing step before passing documents to third-party APIs or external services
- When responding to data subject access requests that require redaction of third-party PII before disclosure
- During data migration or archival processes where retention policies require anonymisation of aged records

## Instructions

1. Receive the input document or text to be scanned. Identify the document type (free text, structured form, CSV, JSON) and select the appropriate parsing strategy for each format.
2. Execute pattern-based detection across all standard PII categories: full names, dates of birth, postal addresses, email addresses, phone numbers (UK and international formats), national insurance numbers, passport numbers, driving licence numbers, bank account and sort code combinations, credit/debit card numbers, IP addresses, and vehicle registration numbers.
3. Apply contextual analysis to detect PII that does not follow fixed patterns. This includes names that appear without surrounding identifiers, job titles combined with department names that could identify individuals in small organisations, and unique combinations of non-PII attributes that together constitute indirect identifiers.
4. Classify each detected PII instance by category and assign a confidence score based on pattern strength and contextual signals. Flag items below the confidence threshold for human review rather than automatic redaction.
5. Apply the configured redaction style to all confirmed PII instances. Supported styles are: full replacement with category label (e.g., [REDACTED-EMAIL]), partial masking retaining structure (e.g., j****.s****@****.com), consistent pseudonymisation using deterministic token mapping (e.g., replacing "Jane Smith" with "Person-A7" consistently throughout the document), or complete removal.
6. Generate the redacted output document preserving all non-PII content, formatting, and document structure. Ensure that redaction markers do not break sentence grammar or data structure integrity.
7. Produce an audit log entry recording: document identifier, timestamp, number of PII instances detected per category, redaction style applied, confidence scores, and any items flagged for human review.

## Output Format

- **Redacted Document**: The complete document with all confirmed PII replaced according to the configured redaction style. Formatting and structure of the original document are preserved.
- **Detection Summary**: A table listing PII categories detected, count of instances per category, average confidence score per category, and redaction method applied.
- **Flagged Items**: A list of potential PII instances that fell below the confidence threshold, presented with surrounding context (with the suspected PII highlighted) for human review and decision.
- **Audit Log Entry**: A structured JSON record containing the document identifier, processing timestamp, operator or agent identifier, detection statistics, redaction configuration used, and a hash of the original document for integrity verification.

## Quality Checks

- All standard UK PII formats (NI numbers, NHS numbers, UK postcodes, UK mobile and landline numbers) must be detected with a minimum 95% recall rate on structured patterns
- Redaction must be applied consistently; the same PII value appearing multiple times in a document must be redacted in every occurrence
- Pseudonymisation tokens must be deterministic within a single document so that references to the same individual remain internally consistent
- The redacted output must not contain residual PII in metadata, headers, footers, or embedded fields that were outside the primary text body
- Confidence scores must be calibrated so that high-confidence detections (above 0.9) have a false positive rate below 2%
- Audit log entries must be generated for every processing run, including runs where no PII is detected

## Limitations

- Cannot detect PII that is encoded, encrypted, or embedded within images, audio, or binary file formats; only text-based content is processed
- Contextual detection of indirect identifiers depends on the size and nature of the dataset; in very small populations, combinations of non-PII attributes may be identifying but undetectable without external reference data
- Language support is currently limited to English; names and addresses in other languages may have reduced detection accuracy
- Does not assess whether the presence of PII is lawful under applicable data protection regulations; the skill detects and redacts but does not provide legal compliance advice
- Pseudonymisation is not equivalent to anonymisation under GDPR; the mapping between pseudonyms and original values must be managed separately and securely
- Performance may degrade on documents exceeding 500 pages or 2 million characters due to the computational cost of contextual analysis
