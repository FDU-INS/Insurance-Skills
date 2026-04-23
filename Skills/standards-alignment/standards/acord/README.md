# ACORD (Association for Cooperative Operations Research and Development) — Standard Guidance

## Overview

ACORD defines data standards for the global insurance and reinsurance industry.
The standard covers Property & Casualty (P&C), Life & Annuity, Reinsurance,
and Next-Generation Digital Standards (NGDS). ACORD's XML and JSON schemas define
canonical entity names, attribute sets, and code lists for insurance data exchange.

**ACORD schemas are membership-gated.** Unlike BIAN or TM Forum, there are no
publicly downloadable schema files. This guidance is manually curated from
ACORD's published documentation and industry-standard terminology.

**For MD-DDL modelling, reference ACORD's entity and data element names,
NOT message envelope structures or transmission wrappers.**

## ACORD Data Model Structure

ACORD uses a layered entity model organised around insurance lifecycle stages:

```text
Party (abstract)
├─ Person (individual)
└─ Organization (company, agency, carrier)

Policy
├─ Coverage
│   ├─ Auto Coverage (Liability, Comprehensive, Collision)
│   ├─ Property Coverage (Home, Renters, Commercial)
│   └─ Life Coverage (Term, Whole, Universal)
├─ Endorsement
└─ Schedule

Claim
├─ Claim Item (line-level detail)
├─ Loss (the insured event)
└─ Reserve (financial provision)

Agreement / Contract
├─ Reinsurance Treaty
└─ Binder
```

## Core ACORD Entities

### Party Model

ACORD separates identity from role, similar to BIAN and TM Forum:

Entity | Description
--- | ---
Party | Abstract base — a person or organisation involved in insurance
Person | A natural person (insured individual, claimant, beneficiary)
Organization | A legal entity (carrier, agency, broker, managing general agent)
Party Role | The capacity in which a party acts (see Party Roles below)

### Party Roles

ACORD defines specific party roles. Each has distinct attributes and lifecycle:

Role | Description | Typical Owner
--- | --- | ---
Policy Holder | Party that owns and is financially responsible for a policy | Policy Administration
Insured | Party whose life, health, or property is covered | Underwriting
Claimant | Party who submits a claim for benefits | Claims
Beneficiary | Party designated to receive policy benefits | Life & Annuity
Agent | Licensed insurance agent who sells policies | Distribution
Broker | Intermediary who represents the insured (not the carrier) | Distribution
Underwriter | Party who evaluates and prices risk | Underwriting
Adjuster | Party who investigates and settles claims | Claims
Third Party Administrator | External party managing claims or benefits | Operations

**Decision guidance**: In insurance, different roles have very different attributes
and processes. Model each major role as a separate entity specialising Party Role,
not as enum values on a single entity.

### Policy and Coverage Model

Entity | Description
--- | ---
Policy | The insurance contract between carrier and policy holder
Coverage | A specific protection within a policy (e.g., liability, collision)
Endorsement | A modification to a policy's terms or coverage
Schedule | A list of covered items (vehicles, properties, equipment)
Premium | The price charged for coverage
Deductible | The amount the insured pays before coverage applies

### Claims Model

Entity | Description
--- | ---
Claim | A request for payment under a policy's coverage
Claim Item | A line-level detail within a claim (per coverage, per loss)
Loss | The insured event that triggered the claim (accident, theft, damage)
Reserve | Financial provision set aside for expected claim payment
Payment | Disbursement to claimant, provider, or third party
Subrogation | Recovery action against a third party responsible for the loss

### Underwriting Model

Entity | Description
--- | ---
Application | A request for insurance coverage (pre-policy)
Quote | A proposed price for requested coverage
Risk Assessment | Evaluation of the risk presented by the applicant
Inspection | Physical examination of property or vehicle
Loss History | Prior claims record used in risk evaluation

## ACORD Naming Conventions

ACORD uses specific terminology that differs from general business language:

Business Term | ACORD Term | Notes
--- | --- | ---
Insurance Contract | Policy | Always "Policy" in ACORD context
Insurance Product | Line of Business | "Personal Auto", "Commercial Property", etc.
Customer | Policy Holder | The purchasing party; "Customer" is not an ACORD term
Claim Request | Claim | Includes both first-party and third-party claims
Premium Payment | Premium | Distinct from claim Payment
Policy Change | Endorsement | Any modification to policy terms
Risk Category | Class Code | Numeric codes for risk classification

## ACORD Code Lists

ACORD maintains extensive code lists (similar to ISO code sets). Common ones:

Code List | Examples | Use in MD-DDL
--- | --- | ---
Transaction Type | New Business, Renewal, Endorsement, Cancellation | Enum values
Coverage Type | Liability, Comprehensive, Collision, Medical | Enum values
Loss Type | Accident, Theft, Fire, Weather, Liability | Enum values
Party Role Type | Insured, Agent, Broker, Adjuster, Claimant | Enum values or entities (see guidance above)
Payment Type | Claim Payment, Premium Payment, Commission | Enum values
Status codes | Active, Expired, Cancelled, Suspended | Enum values per entity lifecycle

## Finding ACORD Entities

### Lookup Process

Since ACORD schemas are not publicly available for automated lookup:

1. **Check this guidance file** for the entity name in the tables above
2. **Use ACORD terminology** — map business terms using the naming conventions table
3. **Check ACORD's public resources** at [acord.org](https://www.acord.org) for
   high-level data model descriptions
4. **For detailed schema verification**, ACORD membership is required

### Mapping Quality Decision

Signal | Action
--- | ---
Entity name matches an ACORD concept in this guide | Reference with `ACORD - {EntityName}`
Entity is a specialisation of an ACORD concept | Reference the parent, note the specialisation
Entity partially overlaps an ACORD concept | Reference with `Partial alignment` qualification
No ACORD counterpart in this guide | Do not fabricate a reference; leave empty

**Important**: Because we cannot verify against full ACORD schemas, be explicit
about the mapping confidence level. Prefer qualifications like "Aligned with
ACORD Party model" over precise schema element references that cannot be verified.

## Common Insurance Patterns in MD-DDL

### Pattern 1: Policy–Coverage Hierarchy

```markdown
# Entities

### Policy
The insurance contract between the carrier and the policy holder.
- references: ACORD - Policy

### Coverage
A specific protection provided within a policy.
- specializes: Policy (component)
- references: ACORD - Coverage

### Auto Liability Coverage
Liability protection for motor vehicle accidents.
- specializes: Coverage
- references: ACORD - Coverage (Auto Liability)
```

### Pattern 2: Claim Lifecycle

```markdown
# Entities

### Claim
A request for payment under a policy's coverage terms.
- references: ACORD - Claim

### Claim Item
A line-level detail within a claim, typically one per coverage.
- references: ACORD - ClaimItem

# Events

### Claim Filed
Triggered when an insured party or claimant submits a claim.
- actor: Claimant
- entity: Claim
```

### Pattern 3: Party Roles in Insurance

```markdown
# Entities

### Policy Holder
Party that owns and is financially responsible for an insurance policy.
- specializes: Party Role
- references: ACORD - PolicyHolder

### Insured Party
Party whose life, health, or property is covered by the policy.
- specializes: Party Role
- references: ACORD - Insured
```

## ACORD vs Other Standards

When modelling insurance domains that also touch financial services:

Standard | Use for | Combine with ACORD?
--- | --- | ---
ISO 20022 | Payment message structures | Yes — premium payments, claim disbursements
BIAN BOM | Banking operations | Yes — when insurer is also a bank (bancassurance)
FATF / AML | Anti-money laundering | Yes — suspicious premium patterns, fraud detection
GDPR / CCPA | Privacy regulation | Yes — PII in policy holder and claimant records

## Version and Source

- **Standard:** ACORD Data Standards
- **Coverage:** P&C, Life & Annuity, Reinsurance, NGDS
- **Source:** [acord.org](https://www.acord.org) (membership required for full schemas)
- **This file:** Manually curated from ACORD published documentation and
  industry-standard insurance terminology. Not generated from schemas.
- **Limitations:** Entity names and descriptions reflect common ACORD usage.
  Attribute-level detail requires ACORD membership for verification.
