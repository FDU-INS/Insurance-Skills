# TM Forum SID (Shared Information/Data) — Standard Guidance

## Overview

TM Forum's SID v4.0.0 provides a standardized information model for the telecoms
industry, organised by the Open API Data Model into 10 functional domains:

- **EngagedParty** — Party (Individual/Organization), Party Roles, Accounts, Agreements, Partnerships, identity
- **Customer** — Customer management, billing, payment, ordering, quotes, carts, risk assessment
- **Product** — Product catalog, offerings, specifications, inventory, usage, promotions
- **Service** — Service catalog, specifications, orders, problems, tests, qualification
- **Resource** — Physical and logical resources, catalog, alarms, inventory
- **Common** — Shared base types, geographic/address, events, documents, tickets
- **Analytics** — Data analytics and performance measurement
- **MarketingSales** — Market segments, competitors, leads, loyalty
- **Customer360** — Unified customer view
- **Iot** — IoT device management and telemetry

**For MD-DDL modelling, reference the SID entity schemas, NOT API operations or eTOM processes.**

## Local Reference Files

This directory contains pre-extracted reference data from TM Forum Open API
Data Model v4.0.0 (Apache 2.0 licence). Use these files for local lookup.

File | Contents | Use for
--- | --- | ---
[sid-entities.md](sid-entities.md) | All ~782 SID entities (name, domain, description) | Finding candidate SID entity names
[sid-entities-detail.md](sid-entities-detail.md) | ~46 core entities with inheritance and full properties | Property-level mapping and inheritance chains
[sid-domains.md](sid-domains.md) | 10 SID domains with entity listings | Understanding where a concept sits in SID's taxonomy

## SID Entity Model Structure

SID uses a layered entity hierarchy with JSON Schema `allOf` inheritance:

```text
Entity (abstract base — Common)
├─ Addressable (id, href)
└─ Extensible (@type, @baseType, @schemaLocation)

Party (abstract — EngagedParty, extends Entity)
├─ Individual (Person)
└─ Organization (Company)

PartyRole (EngagedParty, extends Entity)
├─ Customer (Customer domain)
├─ Partner (EngagedParty)
└─ ... other roles

Product (Product domain, extends Entity)
├─ ProductOffering
├─ ProductSpecification
└─ Catalog / Category

Service (Service domain, extends Entity)
├─ ServiceSpecification
├─ ServiceOrder
└─ ServiceCatalog

Resource (Resource domain, extends Entity)
├─ LogicalResource
├─ PhysicalResource
├─ ResourceSpecification
└─ ResourceCatalog
```

## Finding SID Entities

### Deterministic Lookup Process (No Guessing)

Use this tiered approach — local reference files first.

#### Step 1 — Search the local entity index

Open [sid-entities.md](sid-entities.md) and search for the entity name or close variants.
Build a short candidate list (max 3–5) based on:

- Exact or close name match
- Description alignment with user intent
- SID domain relevance to the telecoms modelling context

#### Step 2 — Check the core entity detail

If the candidate is in [sid-entities-detail.md](sid-entities-detail.md), use the local
data for inheritance chains (`Extends`) and property tables.

#### Step 3 — Check the domain taxonomy

Open [sid-domains.md](sid-domains.md) to understand which SID domain owns the concept.
This provides context for whether the entity is in the right functional area.

#### Step 4 — GitHub fallback for non-cached entities

For entities NOT in the detail cache, inspect the raw schema at:

`https://raw.githubusercontent.com/tmforum-apis/Open_Api_And_Data_Model/master/schemas/{Domain}/{EntityName}.schema.json`

Replace `{Domain}` and `{EntityName}` accordingly (e.g., `EngagedParty/Party.schema.json`).

### Query Expansion Heuristics

If Step 1 returns weak results, retry search with variants before concluding no match:

- Singular/plural: `Customer` / `Customers`
- Role vs subject: `Customer` / `PartyRole`
- Synonyms: `Person`, `Individual`, `Organization`, `Company`
- Telecoms terms: `Service`, `Resource`, `Product`, `Network`, `Subscriber`
- Spec vs instance: `ProductOffering` vs `Product`, `ServiceSpecification` vs `Service`

Record which variant produced the selected match.

### Mapping Quality Decision

Use this decision table after candidate resolution:

Signal | Action
--- | ---
Concept name and definition match closely | Reference directly; no qualification required
Concept is a specialisation of a SID entity | Reference the parent and note the specialisation in description
Concept partially overlaps a SID entity | Reference with explicit qualification (`Partial alignment`) and state the gap
No convincing SID counterpart | Do not force a reference; leave reference empty

## Common SID Mappings

Business Term | SID Entity | SID Domain
--- | --- | ---
Customer | Customer | Customer
Individual, Person | Individual | EngagedParty
Company, Organisation | Organization | EngagedParty
Party (abstract) | Party | EngagedParty
Account | Account | EngagedParty
Billing Account | BillingAccount | Customer
Agreement, Contract | Agreement | EngagedParty
Product | Product | Product
Product Offering | ProductOffering | Product
Product Catalog | Catalog | Product
Service | Service | Service
Network Resource | Resource | Resource
Physical Device | PhysicalResource | Resource
Logical Resource | LogicalResource | Resource
Order | ProductOrder | Customer
Service Order | ServiceOrder | Service
Resource Order | ResourceOrder | Resource
Payment | Payment | Customer
Quote | Quote | Customer
Address | GeographicAddress | Common
Location, Site | GeographicSite | Common
Trouble Ticket | TroubleTicket | Common
Document | Document | Common

Treat this table as a starting hypothesis only. Always confirm against the local
[sid-entities.md](sid-entities.md) index.

## SID Party / PartyRole Pattern

**Critical Pattern**: SID uses the same abstract Party and Party Role pattern as BIAN.

**Party** = The identity (Individual or Organization)
**PartyRole** = The business role they play (Customer, Partner, etc.)

### SID Customer vs Subscriber Distinction

TM Forum distinguishes between:

- **Customer** — the business relationship holder (who signs the contract, who pays)
- **Subscriber** — the service user (who uses the phone, who consumes the bandwidth)

In telecoms, these are often different people. Example:

- Company X is the **Customer** (pays the bill)
- Employee Y is the **Subscriber** (uses the mobile service)

When modelling telecoms domains, ask: "Are Customer and Subscriber managed by
different teams with different data requirements?"

**If YES**: Model as separate entities, both specialising PartyRole.
**If NO**: Model Customer only, with a subscriber relationship.

## SID vs eTOM

**Don't confuse these**:

TM Forum Component | Purpose | Use in MD-DDL
--- | --- | ---
SID (Information Framework) | Entity/data model (e.g., "Party", "Product", "Service") | Reference in MD-DDL
eTOM (Business Process Framework) | Process model (e.g., "Order Handling", "Problem Management") | Do not reference in MD-DDL
TAM (Application Framework) | Application architecture (e.g., "CRM", "Billing") | Do not reference in MD-DDL

**Only reference SID entities in MD-DDL models.** eTOM and TAM are process/application
frameworks, not data standards.

## Version and Source

- **Schema version:** v4.0.0 (TM Forum Open API Data Model, Apache 2.0 licence)
- **Source:** `tmforum-apis/Open_Api_And_Data_Model` on GitHub
- **Note:** TM Forum has released newer SID versions (up to v25.0.0 as of March 2026)
  through its membership portal. The v4.0.0 schemas are the most complete publicly
  available version. Core entity structures (Party, Product, Service, Resource) have
  remained stable across versions.

## Regeneration

To regenerate these reference files from the cached schemas:

```shell
python references/industry_standards/tmforum/extract-references.py
```

To re-download schemas from GitHub first:

```shell
python references/industry_standards/tmforum/extract-references.py --download
```

Schema cache location: `references/industry_standards/tmforum/v4/schemas/`
