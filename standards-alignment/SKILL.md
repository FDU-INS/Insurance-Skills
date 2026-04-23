---
name: standards-alignment
description: Use this skill when the user mentions a named industry standard (BIAN, ISO 20022, FHIR, ACORD, TM Forum, etc.), when modelling a recognised industry domain (banking, payments, insurance, healthcare, telecoms, retail), or when populating the Reference column of any MD-DDL summary table. Also use when the user asks whether a concept already exists in a standard, or when two modelled concepts might map to the same standard object.
---

# Skill: Standards Alignment

Covers how to find, evaluate, and reference external industry standards within
MD-DDL models. No additional spec section is required — standards are referenced
in the `Reference` column of domain summary tables and in entity YAML.

---

## Standards by Domain

| Industry | Primary Standards | Use for |
|---|---|---|
| Banking / Financial Services | BIAN BOM, FIBO | Entity and relationship semantics |
| Payments | ISO 20022, SWIFT MX, PCI DSS | Message schemas, party roles, transaction types |
| Risk & Compliance | Basel III / BCBS, FATF | Risk entities, regulatory metadata |
| Local Compliance | APRA (AU), FCA (UK), OCC (US) | Retention, classification, regulatory_scope |
| Cross-jurisdiction Privacy | GDPR, CCPA, PDPA | PII metadata, retention, consent events |
| Insurance | ACORD, IAIS | Policy, claim, underwriting entities |
| Healthcare | HL7 FHIR, SNOMED CT, ICD-10 | Clinical entities, terminology |
| Telecoms | TM Forum SID, eTOM | Party, product, service entities |
| Retail / Supply Chain | GS1, eCl@ss | Product, location, shipment entities |
| Cross-industry | ISO 8601 (dates), ISO 4217 (currency), ISO 3166 (country) | Attribute types and enum values |

---

## How to Apply a Standard Reference

### Step 1 — Confirm the mapping exists
Do not silently map a concept to a standard if the fit is approximate. Check that
the standard actually defines a counterpart to the entity or attribute being modelled.

For BIAN BOM, use the dedicated guidance in [BIAN standard guidance](./standards/bian/README.md).
It defines the deterministic lookup sequence, local reference files for name matching
and attribute inspection, candidate disambiguation rules, version parameters,
and no-guess policy.
Default to BIAN v13 until v14 snapshots are available — see the version selection rules in [BIAN standard guidance](./standards/bian/README.md).

For TM Forum SID, use the dedicated guidance in [TM Forum standard guidance](./standards/tmforum/README.md).
It defines the deterministic lookup sequence, local reference files for entity
name matching and property inspection, SID domain taxonomy, the Party/PartyRole
pattern, and the Customer vs Subscriber distinction critical for telecoms modelling.

For ACORD, use the curated guidance in [ACORD standard guidance](./standards/acord/README.md).
It covers core insurance entities (Policy, Coverage, Claim), party role patterns
(PolicyHolder, Insured, Claimant, Beneficiary), ACORD naming conventions, and
code lists. Note that ACORD schemas are membership-gated — mappings should note
confidence level explicitly.

For ISO 20022, consult the message definition catalogue for the relevant message type.

For HL7 FHIR, use the dedicated guidance in [FHIR standard guidance](./standards/fhir/README.md).
It defines a deterministic lookup sequence using local cache files for resource
and terminology mapping before falling back to live FHIR pages.

### Step 2 — Note material differences
If the standard's definition differs from the user's intent, say so explicitly:

> "In BIAN BOM, 'Party' is defined as [standard definition]. Your usage adds [X].
> This is close enough to reference BIAN, but we should note the extension in the
> entity description."

### Step 3 — Format the reference link
Use the `Reference` column in summary tables and in entity descriptions:

```markdown
| `Customer` (`entities/customer.md#customer`) | `Party Role` (`entities/party_role.md#party-role`) | A Party with an active product relationship. | `BIAN BOM - Party Role` (`https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole`) |
```

For multiple applicable standards, list the most specific first.

### Step 4 — Carry references into metadata
When a regulatory standard applies to the domain, add it to `regulatory_scope`
in the domain YAML — not just to the Reference column:

```yaml
regulatory_scope:
  - GDPR
  - BCBS 239
  - APRA CPS 234
```

---

## Approximate vs. Exact Mapping

| Signal | Action |
|---|---|
| Concept name and definition match the standard closely | Reference directly; no note needed |
| Concept is a specialisation of a standard object | Reference the parent; note the specialisation in the entity description |
| Concept partially overlaps a standard object | Reference with a qualification: "Partial alignment — [difference]" |
| No standard counterpart exists | Do not force a reference; leave the Reference column empty |

**Never fabricate a reference URL** to make the model look more aligned than it is.
A missing reference is honest; a wrong one is harmful.

For BIAN specifics (including local reference files, lookup order and exact-name resolution), follow [BIAN standard guidance](./standards/bian/README.md).
For TM Forum SID specifics (including SID domain taxonomy and Party/Customer/Subscriber patterns), follow [TM Forum standard guidance](./standards/tmforum/README.md).
For ACORD specifics (including insurance entity hierarchies and party role patterns), follow [ACORD standard guidance](./standards/acord/README.md).
For FHIR specifics (including resource and terminology cache files and healthcare mapping patterns), follow [FHIR standard guidance](./standards/fhir/README.md).

---

## Standard Reconciliation Protocol

Use this protocol when the user's model decomposition and the standard's
decomposition genuinely differ — not just in naming, but in how concepts are
split, merged, or specialised. This is common when an organisation has evolved
its own terminology or when the standard is more abstract than the user's model.

### When to Trigger

Trigger reconciliation when any of these occur:

- User's single concept maps to multiple standard objects (split)
- Multiple user concepts map to a single standard object (merge)
- User concept and standard object overlap partially with distinct extensions
- User asks "how does our model relate to [standard]?" in structural terms

### Step 1 — Build the Comparison Table

Present a structured side-by-side to the user:

```markdown
Your Model | Standard | Overlap | Gap | Options
--- | --- | --- | --- | ---
Customer | BIAN Party Role | Both represent a business relationship to the organisation | Your Customer includes identity (name, DOB); BIAN separates identity into Party | (a) Split into Party + Customer Role (b) Keep Customer, reference BIAN Party Role with note
Account Holder | BIAN Party Role | Both represent a party acting in a capacity | Your Account Holder is a specialisation of Customer; BIAN treats both as Party Role subtypes | (a) Model as separate entity specialising Party Role (b) Treat as Customer attribute
```

### Step 2 — Evaluate Each Option

For each row, apply these decision criteria:

Criterion | What to check
--- | ---
Ownership | Does each concept have a distinct owning team?
Lifecycle | Does each concept have an independent lifecycle?
Attributes | Does each concept carry meaningfully different attributes?
Governance | Do different regulatory requirements apply?
Standard alignment value | Does aligning more closely improve interoperability or auditability?
Cost of divergence | What breaks if we don't align? (reporting, integration, audit trails)

### Step 3 — Propose a Resolution

For each row, recommend one of:

Resolution | When appropriate
--- | ---
**Adopt standard decomposition** | Standard's split adds genuine value; aligning improves interoperability
**Keep user decomposition, reference standard** | User's split reflects real operational boundaries; reference with qualification note
**Hybrid** | Adopt standard's abstract parent, keep user's specialisations as subtypes
**No alignment** | Concepts are superficially similar but semantically different; forced alignment would mislead

### Step 4 — Document the Decision

For each resolved concept, produce an annotation in the entity description that
records the reconciliation:

```markdown
### Customer
The party with an active product or service relationship.

**Standards reconciliation:**
- BIAN equivalent: Party Role (partial alignment — BIAN separates identity
  into Party; our Customer carries identity attributes directly)
- Decision: Kept as single entity; reference BIAN Party Role with qualification
- Rationale: Customer team owns both identity and relationship data; splitting
  would fragment operational ownership
```

This makes the alignment decision auditable and prevents future contributors
from re-asking the same question.

---

## Worked Example: BIAN Alignment for Financial Crime

This example demonstrates the standards alignment process applied to core entities
from the `examples/Financial Crime/` domain, mapping against the BIAN Business
Object Model (v13 — current production baseline; v14 pending snapshot availability).

### Step 1 — Identify candidate mappings

MD-DDL Entity | BIAN BOM Candidate | Confidence
--- | --- | ---
Party | Party | High — both represent an individual or organisation
Person | IndividualEntity | High — BIAN separates natural persons from legal entities
Company | Organisation | High — BIAN equivalent of legal entity
Party Role | PartyRole | High — BIAN uses the same abstraction
Customer | CustomerRole | High — BIAN models Customer as a PartyRole subtype
Account | Account | High — direct match on definition and semantics
Transaction | AccountEntry | Medium — BIAN uses AccountEntry for ledger movements; financial transaction is broader

### Step 2 — Evaluate differences

MD-DDL Entity | BIAN Difference | Impact
--- | --- | ---
Party | BIAN's Party is abstract with IndividualEntity and Organisation subtypes. MD-DDL models Person and Company as subtypes of Party. | Structural match — inheritance hierarchy is aligned
Party Role | BIAN's PartyRole is abstract. MD-DDL matches this pattern. | No difference
Customer | BIAN's CustomerRole inherits from PartyRole. MD-DDL's Customer inherits from Party Role. | Aligned
Transaction | BIAN's AccountEntry is narrowly scoped to account postings. MD-DDL's Transaction covers the full payment event including payer, payee, and payment initiator roles. | Material difference — Transaction is broader than AccountEntry

### Step 3 — Resolution

Entity | Resolution | Rationale
--- | --- | ---
Party, Person, Company | Adopt standard decomposition | MD-DDL's inheritance hierarchy already matches BIAN's Party → IndividualEntity / Organisation pattern
Party Role, Customer | Adopt standard decomposition | Both model the role abstraction identically
Transaction | Keep MD-DDL decomposition, reference BIAN with qualification | Transaction includes payment orchestration (Payer, Payee, Payment Initiator) beyond BIAN's AccountEntry scope

### Step 4 — Resulting Reference column entries

```markdown
Entity | Reference
--- | ---
Party | BIAN BOM - Party
Person | BIAN BOM - IndividualEntity
Company | BIAN BOM - Organisation
Party Role | BIAN BOM - PartyRole
Customer | BIAN BOM - CustomerRole
Transaction | BIAN BOM - AccountEntry (partial — Transaction extends beyond ledger movements to include payment roles and initiator context)
```

### Key takeaway

Not every entity maps 1:1 to a standard. Transaction → AccountEntry is a legitimate
partial alignment. The reconciliation note ensures future contributors understand
why the mapping is qualified rather than exact.

---

## Regulatory Metadata Prompt

When a domain's `regulatory_scope` is being populated, prompt the user with this
checklist. Many teams underspecify this because they assume "someone else handles
compliance."

- Does this domain hold personal data about individuals? → GDPR / CCPA / PDPA
- Does this domain support financial reporting? → SOX / BCBS 239
- Does this domain hold transaction or payment data? → PCI DSS / AML / FATF
- Does this domain support credit risk assessment? → Basel III
- Does this domain hold health information? → HIPAA / HL7
- Is the institution regulated in Australia? → APRA CPS 234 / CPG 235
- Is the institution regulated in the EU? → DORA / EU 5AMLD / 6AMLD
- Is the institution regulated in the UK? → FCA COBS / SYSC

For each applicable framework, confirm with the user whether it affects:
- The `classification` or `pii` flags
- The `default_retention` value
- Any specific attribute-level governance (e.g., credit scores under ECOA)
