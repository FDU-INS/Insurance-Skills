---
name: insurance-coverage-summary
description: |
  Retrieves and analyzes FHIR Coverage and Organization resources to produce a structured insurance summary with
  coordination of benefits analysis. Use when user asks to "check insurance", "coverage details", "verify coverage",
  "insurance summary", "what plan is the patient on", "primary vs secondary insurance", or "coverage status".
  Do NOT use for clinical data, demographics beyond insurance, or billing claim submission.
metadata:
  author: LangCare
  version: 1.0.0
  mcp-server: langcare-mcp-fhir
  category: patient-data
---

# Insurance Coverage Summary

## Overview

Pull Coverage and Organization resources to produce a consolidated insurance summary. Identify primary and secondary coverage, extract plan details, policy and group numbers, coverage periods, and payor organizations. Flag expired coverage, missing authorization data, coverage gaps, and coordination of benefits issues. Output a structured summary suitable for front-desk verification, prior authorization workflows, or care coordination.

## FHIR Resources Used

| Resource | Purpose | Search Parameters |
|----------|---------|-------------------|
| Coverage | Insurance plan details | patient, status |
| Organization | Payor/insurer details | Direct read by reference |
| Patient | Subscriber info, managing org | Direct read by ID |
| RelatedPerson | Subscriber if not self | Direct read by reference |

## Instructions

### Step 1: Pull All Coverage Resources

```
Tool: fhir_search
resourceType: "Coverage"
queryParams: "patient=[patient-id]"
```

Retrieve all Coverage resources regardless of status to capture full history. For each entry extract:

- `status`: active, cancelled, draft, entered-in-error
- `type`: Coverage type from `type.coding` (system `http://terminology.hl7.org/CodeSystem/v3-ActCode`)
- `policyHolder`: Reference to the policyholder (may be Patient, RelatedPerson, or Organization)
- `subscriber`: Reference to the subscriber
- `subscriberId`: Subscriber ID / Member ID
- `beneficiary`: Reference to the patient
- `dependent`: Dependent number
- `relationship`: Subscriber-to-beneficiary relationship (self, spouse, child, other)
- `period`: Coverage effective period (`start` and `end` dates)
- `payor`: Reference to the insurance Organization
- `class[]`: Coverage classification array, each with:
  - `type.coding.code`: "group", "subgroup", "plan", "subplan", "class", "subclass", "sequence", "rxbin", "rxpcn", "rxid", "rxgroup"
  - `value`: The identifier value
  - `name`: Human-readable name
- `order`: Coverage order (1 = primary, 2 = secondary, 3 = tertiary)
- `network`: Network name or identifier
- `costToBeneficiary[]`: Copay and coinsurance information
  - `type.coding.code`: "copay", "coinsurance", "deductible"
  - `valueMoney` or `valueQuantity`

### Step 2: Resolve Payor Organizations

For each Coverage resource, resolve the `payor` reference:

```
Tool: fhir_read
resourceType: "Organization"
id: "[payor-reference-id]"
```

Extract from the Organization:
- `name`: Insurance company name
- `telecom`: Phone number, website
- `address`: Mailing address
- `identifier`: NPI, Tax ID, payer ID
- `type`: Insurance company type classification

### Step 3: Determine Coverage Hierarchy

Establish primary vs secondary coverage:

1. Use `Coverage.order` field if populated (1 = primary, 2 = secondary)
2. If `order` is absent, apply coordination of benefits rules:
   - **Self-employed / Individual**: The patient's own employer plan is primary
   - **Spouse coverage**: Apply Birthday Rule for dependent children (plan of parent whose birthday falls earlier in calendar year is primary)
   - **Medicare**: Medicare is primary when patient is 65+ with no employer group health plan (EGHP) for 20+ employees. Medicare is secondary when patient has EGHP coverage.
   - **Medicaid**: Almost always secondary (payer of last resort)
   - **Workers' Compensation**: Primary for work-related injuries/illnesses
   - **Auto Insurance / Liability**: Primary for accident-related claims

### Step 4: Validate Coverage Status

For each Coverage resource, check:

**Active Coverage Validation:**
- `status` = "active"
- `period.start` <= today
- `period.end` is null OR `period.end` >= today
- `subscriberId` is populated
- `payor` reference resolves to a valid Organization

**Flag: Expired Coverage**
- `period.end` < today but `status` still = "active"
- Flag: "Coverage [plan name] has end date [date] in the past but status is still active. Verify with payor."

**Flag: Missing Subscriber ID**
- `subscriberId` is null or empty
- Flag: "Coverage [plan name] is missing subscriber/member ID. Required for claims submission."

**Flag: Missing Group Number**
- No `class` entry with `type` = "group"
- Flag: "Coverage [plan name] is missing group number."

**Flag: No Primary Coverage**
- Zero Coverage resources with `order` = 1 or no active coverage at all
- Flag: "No primary insurance coverage identified. Verify coverage status with patient."

**Flag: Dual Coverage Without Coordination**
- Multiple active coverages but `order` field not set on any
- Flag: "Multiple active coverages found but primary/secondary order not specified. Coordination of benefits determination required."

### Step 5: Extract Benefit Details (If Available)

Check for cost-to-beneficiary information:
- Copay amounts per visit type
- Coinsurance percentages
- Deductible amounts (individual and family)
- Out-of-pocket maximum

Note: Most FHIR servers do not populate `costToBeneficiary` in Coverage resources. If absent, note: "Benefit details not available in FHIR record. Verify with payor or eligibility check system."

### Step 6: Check for Related Authorization References

```
Tool: fhir_search
resourceType: "Claim"
queryParams: "patient=[patient-id]&status=active&_count=5&_sort=-created"
```

If Claim resources are available, check for:
- `insurance[].coverage`: References to Coverage resources
- `insurance[].preAuthRef`: Prior authorization numbers
- `insurance[].focal`: Which coverage is primary for this claim

If no Claim resources, skip this step.

### Step 7: Format Output

```
INSURANCE COVERAGE SUMMARY
============================
Patient: [name] ([patient-id])
Reviewed: [timestamp]
Total Coverage Records: [count] ([active count] active)

PRIMARY COVERAGE
================
Plan: [plan name from class]
Insurer: [Organization name]
Insurer Phone: [telecom]
Member ID: [subscriberId]
Group: [group class value] / [group class name]
Subscriber: [subscriber relationship] - [subscriber name if not self]
Network: [network]
Effective: [period.start] - [period.end or "Ongoing"]
Status: Active

Benefit Details (if available):
  Copay: $[amount] per [visit type]
  Coinsurance: [percentage]%
  Deductible: $[amount] (Individual) / $[amount] (Family)
  Out-of-Pocket Max: $[amount]

SECONDARY COVERAGE
==================
Plan: [plan name]
Insurer: [Organization name]
Member ID: [subscriberId]
Group: [group class value]
Effective: [period.start] - [period.end or "Ongoing"]
Status: Active

EXPIRED / INACTIVE COVERAGE
============================
1. [Plan name] - Expired: [period.end] - Status: [status]
   (Retained for historical reference)

FLAGS
=====
[!] [Any flagged issues from Step 4]

COORDINATION OF BENEFITS
=========================
Primary: [plan name] (Order: 1)
Secondary: [plan name] (Order: 2)
Determination method: [Coverage.order field / Birthday Rule / Medicare rules]
```

## Examples

### Example 1: Dual Coverage With Clear Hierarchy

**User says:** "What insurance does patient 22334 have?"

**Actions:**
1. `fhir_search` Coverage?patient=22334 -- returns 2 active Coverage resources
2. `fhir_read` Organization/[payor-id-1] -- Blue Cross Blue Shield
3. `fhir_read` Organization/[payor-id-2] -- Medicare

**Result:**
```
INSURANCE COVERAGE SUMMARY
============================
Patient: Margaret Thompson (22334)
Reviewed: 2026-02-07T09:00:00Z
Total Coverage Records: 2 (2 active)

PRIMARY COVERAGE
================
Plan: Blue Cross Blue Shield PPO
Insurer: Blue Cross Blue Shield of Texas
Insurer Phone: (800) 521-2227
Member ID: XYZ123456789
Group: GRP-88901 / Acme Corporation Employee Plan
Subscriber: Self
Network: PPO National
Effective: 2025-01-01 - 2025-12-31
Status: Active

SECONDARY COVERAGE
==================
Plan: Medicare Part B
Insurer: Centers for Medicare & Medicaid Services
Member ID: 1EG4-TE5-MK72
Group: N/A
Subscriber: Self
Effective: 2023-08-01 - Ongoing
Status: Active

COORDINATION OF BENEFITS
=========================
Primary: Blue Cross Blue Shield PPO (Order: 1)
  Reason: Patient has active employer group health plan (EGHP).
  Medicare is secondary when EGHP coverage exists.
Secondary: Medicare Part B (Order: 2)
```

### Example 2: Coverage Issues Detected

**User says:** "Check insurance for patient 55667"

**Actions:**
1. `fhir_search` Coverage?patient=55667 -- returns 3 Coverage resources (1 active, 1 expired still marked active, 1 cancelled)
2. `fhir_read` Organization/[payor-id] -- Aetna

**Result:**
```
INSURANCE COVERAGE SUMMARY
============================
Patient: Kevin Nguyen (55667)
Reviewed: 2026-02-07T09:15:00Z
Total Coverage Records: 3 (1 truly active)

PRIMARY COVERAGE
================
Plan: Aetna HMO
Insurer: Aetna Inc.
Insurer Phone: (800) 872-3862
Member ID: W123456789
Group: 0012345 / State University Health Plan
Subscriber: Self
Network: HMO Open Access
Effective: 2025-09-01 - 2026-08-31
Status: Active

EXPIRED / INACTIVE COVERAGE
============================
1. United Healthcare PPO - Status shows "active" but period ended 2025-08-31
   -> DATA QUALITY ISSUE: Status not updated to reflect termination
2. Medicaid - Status: Cancelled - Ended: 2025-08-31

FLAGS
=====
[!] EXPIRED COVERAGE NOT UPDATED: United Healthcare PPO (Coverage/cov-002) has
    period.end = 2025-08-31 but status remains "active". Update to "cancelled".
[!] SINGLE COVERAGE ONLY: No secondary insurance identified.
[!] MISSING BENEFIT DETAILS: No copay, coinsurance, or deductible data in
    FHIR record. Contact Aetna for benefit verification.

RECOMMENDATION
==============
Update Coverage/cov-002 status to reflect expiration:
  Tool: fhir_update
  resourceType: "Coverage"
  id: "cov-002"
  resource: { "status": "cancelled", ... }
```

### Example 3: No Coverage Found

**User says:** "Does patient 99888 have insurance?"

**Actions:**
1. `fhir_search` Coverage?patient=99888 -- returns 0 entries

**Result:**
```
INSURANCE COVERAGE SUMMARY
============================
Patient: Carlos Mendez (99888)
Reviewed: 2026-02-07T09:30:00Z
Total Coverage Records: 0

FLAGS
=====
[!] NO INSURANCE COVERAGE ON FILE
    No Coverage resources found for this patient. This may indicate:
    - Self-pay / uninsured patient
    - Coverage data not yet entered
    - Coverage stored in a different system not connected to this FHIR server

RECOMMENDATION
==============
1. Verify insurance status with patient
2. Check if coverage is documented in the practice management system
3. Screen for Medicaid/marketplace eligibility if uninsured
4. Document self-pay status if confirmed uninsured
```

## Troubleshooting

### Coverage Resources Lack Class Details (No Plan Name, No Group Number)
- Some EHR systems store minimal coverage data. The `class` array may be empty.
- Check `type` field for coverage type (HMO, PPO, Medicare, Medicaid).
- Resolve the `payor` Organization reference -- the organization name may be the only plan identifier available.
- For EPIC systems, coverage details may be in extensions rather than standard `class` elements.

### Multiple Coverage Resources With Same Payor
- This can happen when coverage is renewed annually and each period creates a new Coverage resource.
- Deduplicate by checking `period` overlap. The most recent non-expired Coverage is the current one.
- If periods overlap with the same payor and plan, take the one with the later `period.start`.

### Coverage.order Not Populated
- Many FHIR servers do not populate the `order` field.
- Apply coordination of benefits rules from Step 3 to determine primary vs secondary.
- If determination is ambiguous, flag for manual review: "Unable to determine primary vs secondary coverage programmatically. Manual coordination of benefits determination required."

## Related Skills

- `patient-demographics-summary` -- for complete demographics including insurance at a high level
- `clinical-summary-generator` -- for full clinical summary (does not include insurance details)
