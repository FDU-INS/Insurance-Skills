---
name: document-management
description: |
  Personal document management skill using Paperless-ngx. Use when: (1) Ingesting and filing
  new documents, (2) Searching for existing documents, (3) Applying tags and correspondents,
  (4) Managing retention policies, (5) Integrating documents with other personal workflows
  (tax prep, medical records, insurance claims). Tools: paperless-mcp for all document
  operations.
---

# Document Management

## Tool Mapping

| Task | Tool | Notes |
|------|------|-------|
| Search documents | `search_documents` | Full-text search across all documents |
| Get document details | `get_document` | Metadata, tags, correspondent, dates |
| Upload document | `upload_document` | Ingest new document with initial metadata |
| Update document metadata | `update_document` | Add/change tags, correspondent, dates, title |
| List/manage tags | `get_tags`, `create_tag` | Taxonomy management |
| List/manage correspondents | `get_correspondents`, `create_correspondent` | Organization/person who issued the document |
| List/manage document types | `get_document_types`, `create_document_type` | Classify by type |
| Download document | `get_document_content` | Retrieve original or archived version |

## Document Intake Workflow

### Standard Intake Procedure

For every new document:

1. **Upload** the document via `upload_document`
2. **Review auto-classification** — Paperless-ngx will attempt auto-tagging and correspondent matching
3. **Verify and correct metadata**:
   - Title: Clear, descriptive, includes date if relevant (e.g., "2026-02 Electricity Bill - Tata Power")
   - Date: The document's date (issue date, statement date), not the upload date
   - Correspondent: The organization or person who issued the document
   - Document type: Select from the taxonomy below
   - Tags: Apply all relevant tags from the taxonomy below
4. **Confirm filing** — Verify the document appears in expected searches

### Title Conventions

Use consistent title formatting for searchability:

| Document Type | Title Format | Example |
|--------------|-------------|---------|
| Monthly bills | `YYYY-MM [Service] Bill - [Provider]` | `2026-02 Electricity Bill - Tata Power` |
| Bank statements | `YYYY-MM [Account Type] Statement - [Bank]` | `2026-02 Savings Statement - HDFC` |
| Tax forms | `FY YYYY-YY [Form Name]` | `FY 2025-26 Form 16` |
| Insurance | `[Type] Policy - [Provider] - [Policy#]` | `Health Policy - Star Health - 12345` |
| Medical | `YYYY-MM-DD [Type] - [Provider/Doctor]` | `2026-02-15 Blood Test Results - Apollo Labs` |
| Contracts | `[Type] Agreement - [Party] - YYYY` | `Rental Agreement - Landlord Name - 2026` |
| Identity docs | `[Doc Type] - [Person]` | `Passport - Principal` |
| Receipts | `YYYY-MM-DD Receipt - [Vendor] - [Amount]` | `2026-02-20 Receipt - Amazon - 4500` |

## Tagging Taxonomy

### Primary Category Tags

Apply exactly one primary category tag per document:

| Tag | Use For |
|-----|---------|
| `financial` | Bank statements, investment statements, tax documents, pay slips |
| `medical` | Prescriptions, lab reports, discharge summaries, vaccination records |
| `legal` | Contracts, agreements, court documents, notarized documents |
| `education` | Certificates, transcripts, school communications, course materials |
| `home` | Property documents, utility bills, maintenance records, warranties |
| `vehicle` | Registration, insurance, service records, challans |
| `insurance` | All insurance policies and claims (health, life, vehicle, property) |
| `identity` | Passports, Aadhaar, PAN, driving license, voter ID |
| `employment` | Offer letters, appraisals, relieving letters, pay slips |
| `receipts` | Purchase receipts, invoices (not bills/statements) |

### Secondary Tags (Apply as Many as Relevant)

| Tag | Use For |
|-----|---------|
| `tax-relevant` | Any document needed for tax filing (80C, 80D, HRA, capital gains) |
| `active-policy` | Insurance policies currently in force |
| `expired` | Policies, contracts, IDs past their validity |
| `needs-renewal` | Documents approaching expiry (flag 30-60 days before) |
| `reimbursable` | Medical or business expenses eligible for reimbursement |
| `warranty-active` | Products still under warranty |
| `recurring` | Bills and statements that arrive regularly |
| `original-physical` | Physical original exists and is filed (note location in custom field) |
| `child-[name]` | Documents pertaining to a specific child |

### Tag Hygiene Rules

- Every document must have exactly one primary category tag
- Apply `tax-relevant` liberally — it is easier to remove than to find missing documents at tax time
- Review `needs-renewal` tagged documents monthly
- When a policy expires, replace `active-policy` with `expired` and remove `needs-renewal`

## Correspondent Management

### Correspondent Naming Conventions

- Use the official organization name, not abbreviations: "HDFC Bank" not "HDFC"
- For individuals (doctors, lawyers): "Dr. Firstname Lastname" or "Adv. Firstname Lastname"
- For government: "Income Tax Department", "RTO Hyderabad", etc.

### When to Create New Correspondents

- Only create a new correspondent when an existing one does not match
- Before creating, search existing correspondents for partial matches
- Merge duplicates when found (same entity, different name variants)

## Document Types

| Document Type | Description |
|--------------|-------------|
| Statement | Bank/credit card/investment periodic statements |
| Bill | Utility bills, service invoices |
| Policy | Insurance policies, warranty cards |
| Certificate | Educational, professional, birth/marriage certificates |
| Report | Medical reports, lab results, appraisals |
| Agreement | Contracts, rental agreements, loan agreements |
| Tax Form | Form 16, ITR acknowledgment, TDS certificates |
| ID Document | Passports, Aadhaar, PAN, licenses |
| Receipt | Purchase receipts, payment confirmations |
| Letter | Correspondence, notices, official communications |
| Prescription | Medical prescriptions |
| Claim | Insurance claims, reimbursement filings |

## Search Strategies

### Finding Documents

| Need | Search Approach |
|------|----------------|
| Specific document | Search by title keywords + date range |
| All docs from an org | Filter by correspondent |
| Tax season gathering | Filter by tag `tax-relevant` + date range for the FY |
| Active insurance | Filter by tags `insurance` + `active-policy` |
| Medical history | Filter by tag `medical` + correspondent (doctor/hospital) |
| Expiring documents | Filter by tag `needs-renewal` |
| Recent uploads | Sort by added date, descending |

### Search Tips

1. Use full-text search for content within documents (OCR text)
2. Combine tag filters with date ranges for precise results
3. When searching for a document you know exists but cannot find, try:
   - Search by correspondent instead of title
   - Broaden the date range
   - Search for distinctive terms from within the document content
   - Check if the document was tagged with an unexpected primary category

## Retention Policies

### How Long to Keep Documents

| Document Type | Retention Period | Notes |
|--------------|-----------------|-------|
| Tax returns and supporting docs | 7 years from filing | Legal requirement under IT Act |
| Bank statements | 7 years | Tax audit support |
| Pay slips | 7 years | Tax/employment verification |
| Insurance policies | Duration of policy + 3 years | Claims can be filed after expiry |
| Medical records | Indefinite | Lifetime medical history |
| Property documents | Indefinite | Ownership proof |
| Identity documents | Until replaced by renewed version | Keep expired passports indefinitely |
| Utility bills | 1 year | Unless needed for address proof |
| Receipts (general) | 1 year or warranty period | Whichever is longer |
| Receipts (tax-relevant) | 7 years | Same as tax documents |
| Employment documents | Indefinite | Career record |
| Educational certificates | Indefinite | Permanent record |
| Vehicle documents | Duration of ownership + 3 years | Transfer records for sold vehicles |
| Warranties | Duration of warranty | Delete after warranty expires unless claim pending |

### Retention Review Procedure

Quarterly:
1. Filter documents by `expired` tag
2. Check if retention period has passed
3. For documents past retention: verify no ongoing need, then archive or delete
4. For utility bills > 1 year old without `tax-relevant` tag: safe to delete

## Integration with Other Skills

### Tax Preparation (Budgeting Skill)

At tax time:
1. Search for all documents tagged `tax-relevant` within the financial year
2. Group by deduction section (80C, 80D, 24, etc.)
3. Verify completeness: each claimed deduction has supporting documentation
4. Cross-reference against actual-mcp transaction data for amount verification
5. Export or share relevant documents

### Medical Records (Family)

When visiting a doctor or during medical events:
1. Search for prior medical records by correspondent (hospital/doctor) or tag `medical`
2. Pull recent lab reports and prescriptions for reference
3. After the visit: upload any new documents and tag appropriately
4. For children: always apply the `child-[name]` tag

### Insurance Claims

When filing a claim:
1. Locate the active policy document: filter by `insurance` + `active-policy` + correspondent
2. Gather supporting documents (medical reports for health, FIR for vehicle, etc.)
3. Upload claim submission documents and tag as `claim`
4. Track claim status by adding notes to the claim document

## Common Pitfalls

1. **Skipping metadata at upload** — Always complete title, date, correspondent, type, and tags immediately. Documents without metadata become unfindable.
2. **Inconsistent titles** — Follow the title conventions above. A search for "electricity bill" should find all electricity bills.
3. **Missing tax-relevant tags** — When in doubt, tag it. Removing an unnecessary tag is cheaper than missing a deduction.
4. **Correspondent proliferation** — Search before creating. "HDFC Bank", "HDFC", and "HDFC Bank Ltd" should be one correspondent.
5. **Ignoring document dates** — The document date is the date on the document (statement date, issue date), not when you uploaded it. Paperless uses this for date-range filtering.
6. **Not reviewing needs-renewal** — Check monthly. An expired insurance policy with no renewal is a risk, not just a filing issue.
