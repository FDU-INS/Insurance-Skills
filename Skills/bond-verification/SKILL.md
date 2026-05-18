---
name: bond-verification
description: Formally verify construction payment bonds by extracting fields from bond documents and cross-referencing against Treasury Circular 570, state licensing, and underwriting limits. Use whenever the user uploads a payment bond PDF, mentions bond verification, asks "is this bond valid", references AIA A312, or needs to verify a surety company's authority to write bonds. Also trigger on "verify bond", "check surety", "payment bond", "performance bond", or "Circular 570."
---

# Payment Bond Formal Verification

Verify that a construction payment bond is valid, the surety is authorized, and the bond covers the project requirements. This is the marketplace's trust layer — operators won't bid on tasks without verified payment security.

## Workflow

### 1. Accept bond document

Accept: pasted bond text, PDF file path, or extracted fields (bond number, surety, principal, obligee, penal sum, date). If a PDF, extract text and identify the AIA A312 or ConsensusDocs 260 field structure.

### 2. Extract bond fields

Identify and extract these fields. Mark each as FOUND or NOT FOUND:

- Bond number
- Surety company name
- Surety NAIC code (if present)
- Principal (contractor) legal name and address
- Obligee (project owner / agency)
- Project description / contract reference
- Penal sum (bond amount in dollars)
- Effective date
- Expiration date (if any — many bonds are open-ended until project completion)
- Power of Attorney reference
- Surety agent name and signature

### 3. Verify surety against Circular 570

Read `references/circular-570-verification.md` for the verification process.

Check:
- Is the surety listed on Treasury Circular 570? (federally approved)
- Is the surety licensed in the project's state?
- Is the penal sum within the surety's underwriting limit?
- What is the surety's AM Best rating? (A- or better is standard)

### 4. Verify bond coverage

Check:
- Does the penal sum cover the total task value(s) being posted?
- Is the effective date before or on the task posting date?
- Does the obligee match the project owner referenced in the RFP?
- Does the principal match the entity posting tasks on the marketplace?

### 5. Generate verification report

Output:

```json
{
  "verification_status": "VERIFIED | FAILED | PARTIAL",
  "bond_number": "...",
  "surety": {
    "name": "...",
    "circular_570_listed": true,
    "state_licensed": true,
    "underwriting_limit": "$...",
    "am_best_rating": "A+",
    "naic_code": "..."
  },
  "principal": "...",
  "obligee": "...",
  "penal_sum": "$...",
  "coverage_sufficient": true,
  "effective_date": "...",
  "checks": [
    {"check": "Surety on Circular 570", "result": "PASS|FAIL", "detail": "..."},
    {"check": "Licensed in MI", "result": "PASS|FAIL", "detail": "..."},
    {"check": "Penal sum covers tasks", "result": "PASS|FAIL", "detail": "..."},
    {"check": "Bond is current", "result": "PASS|FAIL", "detail": "..."},
    {"check": "Obligee matches project", "result": "PASS|FAIL", "detail": "..."},
    {"check": "Principal matches poster", "result": "PASS|FAIL", "detail": "..."}
  ],
  "warnings": [],
  "requires_human": ["Contact surety to confirm bond is active (not cancelled)"]
}
```

### 6. Validate output

```bash
python scripts/validate_bond_verification.py < report.json
```

## References

- `references/circular-570-verification.md` — How to check Circular 570, state licensing, and underwriting limits. Includes URLs for Treasury data download and surety verification portals.
- `references/bond-field-definitions.md` — AIA A312 and ConsensusDocs 260 field definitions and where to find them in the document.

## What this skill explicitly CANNOT do

This skill verifies the bond document against public records. It does NOT:
- Contact the surety to confirm the bond is still active
- Verify the Power of Attorney authenticity
- Provide legal advice on bond adequacy
- Replace attorney review for disputed bonds

These limitations are stated in every output under `requires_human`.
