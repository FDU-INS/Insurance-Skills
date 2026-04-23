# Altitude API — Domain Guide

> Compact reference for finding the right API domain.
> For full endpoint details (parameters, request body, response schema),
> search `api.json` in the `api-docs/` directory using Grep or Read.

## How to Look Up Full Endpoint Details

When you need exact parameters or schemas for an endpoint:
1. Find the api.json path: `Glob pattern "**/m62-altitude-api/**/api.json"`
2. Search for the endpoint: `Grep pattern "/api/v1/individual/search" path="{api.json path}"`
3. Read the surrounding context (~50 lines) to see parameters, request body, and response schema
4. If you need a schema definition, search: `Grep pattern "IndividualDto" path="{api.json path}"`

## Common CRUD Patterns

Most entity types follow these URL patterns:
```
GET    /api/v1/{type}/search?searchParams=searchFor:{query}&page=0&size=20
GET    /api/v1/{type}/{id}              # Get by ID
POST   /api/v1/{type}                   # Create new
PATCH  /api/v1/{type}/{id}              # Partial update (send only changed fields)
PUT    /api/v1/{type}/{id}              # Full replace
DELETE /api/v1/{type}/{id}              # Delete
```

**Entity type URL segments:** `individual`, `legal-entity`, `household`,
`account-financial`, `contact`, `tangible-asset`, `insurance-policy`, `liability`,
`instrument`, `fund`, `strategy`, `document`, `order`

## Cross-Entity Patterns

```
GET /api/v1/{type}/{id}/relationships        # All relationships
GET /api/v1/{type}/{id}/relationships/from   # Outgoing
GET /api/v1/{type}/{id}/relationships/to     # Incoming
GET /api/v1/{type}/{id}/notes                # Notes
GET /api/v1/{type}/{id}/household            # Find parent household
GET /api/v1/{type}/{id}/insurance-policies   # Insurance policies
GET /api/v1/{type}/{id}/liabilities          # Debts
GET /api/v1/{type}/{id}/tangible-assets      # Physical assets
```

---

### Individuals (People)
*51 endpoints* | Prefix: `/api/v1/individual`
- GET `/api/v1/individual/search` — Search individuals
- GET `/api/v1/individual/{id}` — Get an entity by ID
- PUT `/api/v1/individual/{id}` — Update an existing entity
- DELETE `/api/v1/individual/{id}` — Delete an entity
- PATCH `/api/v1/individual/{id}` — Partially update an entity
- GET `/api/v1/individual/{id}/valuation/history` — Get individual valuation history
- GET `/api/v1/individual/{id}/valuations/chart` — Get individual valuation chart data
- GET `/api/v1/individual` — Get all clients
- POST `/api/v1/individual` — Create a new entity
- GET `/api/v1/individual/{id}/household` — Get household for entity
- *+ 41 more (search api.json for `api/v1/individual` to see all)*

### Legal Entities (Trusts, LLCs, Corps)
*57 endpoints* | Prefix: `/api/v1/legal-entity`
- GET `/api/v1/legal-entity/search` — Search legal entities
- GET `/api/v1/legal-entity/{id}` — Get an entity by ID
- PUT `/api/v1/legal-entity/{id}` — Update an existing entity
- DELETE `/api/v1/legal-entity/{id}` — Delete an entity
- PATCH `/api/v1/legal-entity/{id}` — Partially update an entity
- GET `/api/v1/legal-entity/{id}/valuation/history` — Get legal entity valuation history
- GET `/api/v1/legal-entity/{id}/valuations/chart` — Get legal entity valuation chart data
- GET `/api/v1/legal-entity` — Get all legal entities
- POST `/api/v1/legal-entity` — Create a new entity
- GET `/api/v1/legal-entity/{id}/household` — Get household for entity
- *+ 47 more (search api.json for `api/v1/legal-entity` to see all)*

### Households (Family Groups)
*28 endpoints* | Prefix: `/api/v1/household`
- GET `/api/v1/household/search` — Search households
- GET `/api/v1/household/{id}` — Get an entity by ID
- PUT `/api/v1/household/{id}` — Update an existing entity
- DELETE `/api/v1/household/{id}` — Delete an entity
- PATCH `/api/v1/household/{id}` — Partially update an entity
- GET `/api/v1/household/{id}/valuation/history` — Get household valuation history
- GET `/api/v1/household/{id}/valuations/chart` — Get household valuation chart data
- GET `/api/v1/household` — Get all entities
- POST `/api/v1/household` — Create a new entity
- GET `/api/v1/household/{id}/relationships` — Get all relationships
- *+ 18 more (search api.json for `api/v1/household` to see all)*

### Financial Accounts
*77 endpoints* | Prefix: `/api/v1/account-financial`
- GET `/api/v1/account-financial/search` — Search financial accounts
- GET `/api/v1/account-financial/{id}` — Get an entity by ID
- PUT `/api/v1/account-financial/{id}` — Update an existing entity
- DELETE `/api/v1/account-financial/{id}` — Delete an entity
- PATCH `/api/v1/account-financial/{id}` — Partially update an entity
- GET `/api/v1/account-portfolio/{id}` — Get portfolio by ID
- GET `/api/v1/account-portfolio/{id}/valuations/chart` — Get portfolio valuation chart data
- GET `/api/v1/account-financial` — Get all entities
- POST `/api/v1/account-financial` — Create a new entity
- GET `/api/v1/account-financial/{accountId}/valuations/chart` — Get account valuation chart data
- *+ 67 more (search api.json for `api/v1/account-financial` to see all)*

### Tangible Assets
*78 endpoints* | Prefix: `/api/v1/tangible-asset`
- GET `/api/v1/tangible-asset/search` — Search tangible assets
- GET `/api/v1/tangible-asset/{id}` — Get tangible asset by ID
- PUT `/api/v1/tangible-asset/{id}` — Update an existing entity
- DELETE `/api/v1/tangible-asset/{id}` — Delete tangible asset
- PATCH `/api/v1/tangible-asset/{id}` — Partially update an entity
- GET `/api/v1/tangible-asset` — Get all tangible assets
- POST `/api/v1/tangible-asset` — Create a new entity
- GET `/api/v1/tangible-asset/{id}/household` — Get household for entity
- GET `/api/v1/tangible-asset/{id}/liabilities` — Get liabilities for an asset
- POST `/api/v1/tangible-asset/{id}/liabilities` — Add liability to asset
- *+ 68 more (search api.json for `api/v1/tangible-asset` to see all)*

### Insurance Policies
*37 endpoints* | Prefix: `/api/v1/insurance-policy`
- GET `/api/v1/insurance-policy/{id}` — Get an entity by ID
- PUT `/api/v1/insurance-policy/{id}` — Update an existing entity
- DELETE `/api/v1/insurance-policy/{id}` — Delete an entity
- PATCH `/api/v1/insurance-policy/{id}` — Partially update an entity
- GET `/api/v1/insurance-policy` — Get all insurance policies
- POST `/api/v1/insurance-policy` — Create a new entity
- GET `/api/v1/insurance-policy/{id}/household` — Get household for entity
- GET `/api/v1/insurance-policy/{id}/notes` — Get all notes
- POST `/api/v1/insurance-policy/{id}/notes` — Create a new note
- GET `/api/v1/insurance-policy/{id}/notes/{noteId}` — Get a specific note
- *+ 27 more (search api.json for `api/v1/insurance-policy` to see all)*

### Liabilities (Debts & Loans)
*33 endpoints* | Prefix: `/api/v1/liability`
- GET `/api/v1/liability/{id}` — Get an entity by ID
- PUT `/api/v1/liability/{id}` — Update an existing entity
- DELETE `/api/v1/liability/{id}` — Delete an entity
- PATCH `/api/v1/liability/{id}` — Partially update an entity
- GET `/api/v1/liability` — Get all liabilities
- POST `/api/v1/liability` — Create a new entity
- GET `/api/v1/liability/{id}/household` — Get household for entity
- GET `/api/v1/liability/{id}/notes` — Get all notes
- POST `/api/v1/liability/{id}/notes` — Create a new note
- GET `/api/v1/liability/{id}/notes/{noteId}` — Get a specific note
- *+ 23 more (search api.json for `api/v1/liability` to see all)*

### Contacts (Advisors, Attorneys, CPAs)
*8 endpoints* | Prefix: `/api/v1/contact`
- GET `/api/v1/contact/search` — Search contacts
- GET `/api/v1/contact/{id}` — Get an entity by ID
- PUT `/api/v1/contact/{id}` — Update an existing entity
- DELETE `/api/v1/contact/{id}` — Delete a contact
- PATCH `/api/v1/contact/{id}` — Partially update an entity
- GET `/api/v1/contact` — Get all entities
- POST `/api/v1/contact` — Create a new entity
- GET `/api/v1/contact/count` — Count entities

### Instruments (Securities)
*34 endpoints* | Prefix: `/api/v1/instrument`
- GET `/api/v1/instrument/search` — Search instruments with advanced filtering
- GET `/api/v1/instrument/{id}` — Get instrument by ID with latest price
- PUT `/api/v1/instrument/{id}` — Update an existing entity
- DELETE `/api/v1/instrument/{id}` — Delete an entity
- PATCH `/api/v1/instrument/{id}` — Partially update an entity
- GET `/api/v1/instrument` — Get all entities
- POST `/api/v1/instrument` — Create a new entity
- GET `/api/v1/instrument/{id}/prices/chart` — Get instrument price chart data
- GET `/api/v1/instrument/{id}/relationships` — Get all relationships
- GET `/api/v1/instrument/{id}/relationships/from` — Get outgoing relationships
- *+ 24 more (search api.json for `api/v1/instrument` to see all)*

### Positions & Holdings
*30 endpoints* | Prefix: `/api/v1/position`
- GET `/api/v1/position/search` — Search positions with advanced filtering
- GET `/api/v1/position/{id}` — Get an entity by ID
- PUT `/api/v1/position/{id}` — Update an existing entity
- DELETE `/api/v1/position/{id}` — Delete an entity
- PATCH `/api/v1/position/{id}` — Partially update an entity
- GET `/api/v1/position` — Get all entities
- POST `/api/v1/position` — Create a new entity
- GET `/api/v1/position/count` — Count entities
- PUT `/api/v1/position/{id}/price` — Update position price and recalculate metrics
- POST `/api/v1/position/{id}/snapshot` — Create a position snapshot for historical tracking
- *+ 20 more (search api.json for `api/v1/position` to see all)*

### Transactions
*19 endpoints* | Prefix: `/api/v1/transaction`
- GET `/api/v1/transaction/search` — Search transactions with combined filters
- GET `/api/v1/transaction/{id}` — Get an entity by ID
- PUT `/api/v1/transaction/{id}` — Update an existing entity
- DELETE `/api/v1/transaction/{id}` — Delete an entity
- PATCH `/api/v1/transaction/{id}` — Partially update an entity
- GET `/api/v1/transaction` — Get all entities
- POST `/api/v1/transaction` — Create a new entity
- GET `/api/v1/transaction/count` — Count entities
- GET `/api/v1/transaction/summary` — Transaction value summary by type
- PUT `/api/v1/transaction/{id}/cancel` — Cancel a transaction
- *+ 9 more (search api.json for `api/v1/transaction` to see all)*

### Entity Relationships
*32 endpoints* | Prefix: `/api/v1/entity-relationship`
- GET `/api/v1/entity-relationship/{id}` — Get an entity by ID
- PUT `/api/v1/entity-relationship/{id}` — Update an existing entity
- DELETE `/api/v1/entity-relationship/{id}` — Delete an entity
- PATCH `/api/v1/entity-relationship/{id}` — Partially update an entity
- GET `/api/v1/entity-relationship` — Get all entities
- POST `/api/v1/entity-relationship` — Create a new entity
- GET `/api/v1/entity-relationship/count` — Count entities
- GET `/api/v1/entity-relationship/from/{sourceType}/{sourceId}/history` — Get full relationship history (audit trail)
- GET `/api/v1/entity-relationship/household-universe/{entityType}/{entityId}` — Get all entities within the same household context
- PUT `/api/v1/entity-relationship/{id}/end` — End a relationship (preserves history)
- *+ 22 more (search api.json for `api/v1/entity-relationship` to see all)*

### Documents & Uploads
*68 endpoints* | Prefix: `/api/v1/document`
- GET `/api/v1/document/search/count` — Count documents matching search criteria
- GET `/api/v1/document/search` — Search documents with dynamic parameters
- GET `/api/v1/document/{id}` — Get an entity by ID
- PUT `/api/v1/document/{id}` — Update an existing entity
- DELETE `/api/v1/document/{id}` — Delete an entity
- PATCH `/api/v1/document/{id}` — Partially update an entity
- GET `/api/v1/document` — Get all entities
- POST `/api/v1/document` — Create a new entity
- GET `/api/v1/document-upload-session` — List upload sessions
- POST `/api/v1/document-upload-session` — Create upload session
- *+ 58 more (search api.json for `api/v1/document` to see all)*

### Funds (Investment Products)
*68 endpoints* | Prefix: `/api/v1/fund`
- GET `/api/v1/fund/search/count` — Count funds matching search criteria
- POST `/api/v1/fund-documents/search` — Search fund documents
- GET `/api/v1/fund/search` — Search funds with advanced filtering
- GET `/api/v1/fund-performance/{id}` — Get performance record by ID
- DELETE `/api/v1/fund-performance/{id}` — Delete performance record
- GET `/api/v1/fund/shareclass/{id}` — Get an entity by ID
- PUT `/api/v1/fund/shareclass/{id}` — Update an existing entity
- DELETE `/api/v1/fund/shareclass/{id}` — Delete an entity
- PATCH `/api/v1/fund/shareclass/{id}` — Partially update an entity
- GET `/api/v1/fund/{fundId}/shareclass/{id}` — Get an entity by ID
- *+ 58 more (search api.json for `api/v1/fund` to see all)*

### Orders (Trade Orders)
*30 endpoints* | Prefix: `/api/v1/order`
- GET `/api/v1/order/search/count` — Count orders matching search criteria
- POST `/api/v1/order-documents/search` — Search order documents
- GET `/api/v1/order/search` — Search orders with dynamic parameters
- GET `/api/v1/order/{id}` — Get an entity by ID
- PUT `/api/v1/order/{id}` — Update an existing entity
- DELETE `/api/v1/order/{id}` — Delete an entity
- PATCH `/api/v1/order/{id}` — Partially update an entity
- GET `/api/v1/order` — Get all entities
- POST `/api/v1/order` — Create a new entity
- GET `/api/v1/order/count` — Count entities
- *+ 20 more (search api.json for `api/v1/order` to see all)*

### Investment Strategies
*20 endpoints* | Prefix: `/api/v1/strategy`
- GET `/api/v1/strategy/search/count` — Count strategies matching criteria
- GET `/api/v1/strategy/search` — Search strategies with faceted filtering
- POST `/api/v1/strategy/search` — Search strategies with request body
- GET `/api/v1/strategy/{id}` — Get an entity by ID
- PUT `/api/v1/strategy/{id}` — Update an existing strategy (ADMIN only)
- DELETE `/api/v1/strategy/{id}` — Delete a strategy (ADMIN only)
- PATCH `/api/v1/strategy/{id}` — Partially update a strategy (ADMIN only)
- GET `/api/v1/strategy` — Get all entities
- POST `/api/v1/strategy` — Create a new strategy (ADMIN only)
- GET `/api/v1/strategy/count` — Count entities
- *+ 10 more (search api.json for `api/v1/strategy` to see all)*

### Model Portfolios
*17 endpoints* | Prefix: `/api/v1/model-portfolio`
- GET `/api/v1/model-portfolio/search/count` — Count model portfolios matching criteria
- GET `/api/v1/model-portfolio/search` — Search model portfolios with faceted filtering
- POST `/api/v1/model-portfolio/search` — Search model portfolios with request body
- GET `/api/v1/model-portfolio/{id}` — Get model portfolio by ID
- PUT `/api/v1/model-portfolio/{id}` — Update an existing model portfolio
- DELETE `/api/v1/model-portfolio/{id}` — Delete a model portfolio
- PATCH `/api/v1/model-portfolio/{id}` — Partially update a model portfolio
- GET `/api/v1/model-portfolio` — Get all model portfolios
- POST `/api/v1/model-portfolio` — Create a new model portfolio
- GET `/api/v1/model-portfolio/{id}/rebalancing-plan` — Generate rebalancing plan
- *+ 7 more (search api.json for `api/v1/model-portfolio` to see all)*

### Fee Schedules (Billing)
*17 endpoints* | Prefix: `/api/v1/fee-schedule`
- GET `/api/v1/fee-schedule/search` — Search fee schedules
- GET `/api/v1/fee-schedule/{id}` — Get an entity by ID
- PUT `/api/v1/fee-schedule/{id}` — Update an existing entity
- DELETE `/api/v1/fee-schedule/{id}` — Delete an entity
- PATCH `/api/v1/fee-schedule/{id}` — Partially update an entity
- GET `/api/v1/fee-schedule` — Get all entities
- POST `/api/v1/fee-schedule` — Create a new entity
- GET `/api/v1/fee-schedule/{id}/usage/count` — Count fee schedule usage
- GET `/api/v1/fee-schedule/count` — Count entities
- POST `/api/v1/fee-schedule/{id}/activate` — Activate fee schedule
- *+ 7 more (search api.json for `api/v1/fee-schedule` to see all)*

### Firm Management
*50 endpoints* | Prefix: `/api/v1/firm`
- GET `/api/v1/firm-entity-preferences/{id}` — Get firm entity preference by ID
- PUT `/api/v1/firm-entity-preferences/{id}` — Update firm entity preference
- DELETE `/api/v1/firm-entity-preferences/{id}` — Delete firm entity preference
- GET `/api/v1/firm/representative/{id}` — Get an entity by ID
- PUT `/api/v1/firm/representative/{id}` — Update an existing entity
- DELETE `/api/v1/firm/representative/{id}` — Delete an entity
- PATCH `/api/v1/firm/representative/{id}` — Partially update an entity
- GET `/api/v1/firm/{firmId}/integration/{id}` — Get integration by ID
- PUT `/api/v1/firm/{firmId}/integration/{id}` — Update integration
- DELETE `/api/v1/firm/{firmId}/integration/{id}` — Delete integration
- *+ 40 more (search api.json for `api/v1/firm` to see all)*

### Compliance Tracking
*23 endpoints* | Prefix: `/api/v1/compliance-tracking`
- GET `/api/v1/compliance-tracking/{id}` — Get an entity by ID
- PUT `/api/v1/compliance-tracking/{id}` — Update an existing entity
- DELETE `/api/v1/compliance-tracking/{id}` — Delete an entity
- PATCH `/api/v1/compliance-tracking/{id}` — Partially update an entity
- GET `/api/v1/compliance-tracking` — Get all entities
- POST `/api/v1/compliance-tracking` — Create a new entity
- GET `/api/v1/compliance-tracking/count` — Count entities
- PUT `/api/v1/compliance-tracking/{id}/aml-status` — Update AML status for a compliance record
- POST `/api/v1/compliance-tracking/{id}/ctr` — Record a CTR filing for a compliance record
- PUT `/api/v1/compliance-tracking/{id}/fatca-status` — Update FATCA status for a compliance record
- *+ 13 more (search api.json for `api/v1/compliance-tracking` to see all)*

### Workflows, Tasks & Exceptions
*63 endpoints* | Prefix: `/api/v1/workflow`
- GET `/api/v1/workflow-exception/{id}` — Get a task exception by ID
- GET `/api/v1/workflow-execution/{id}` — Get a workflow execution by ID
- DELETE `/api/v1/workflow-execution/{id}` — Soft delete a workflow execution
- GET `/api/v1/workflow-template/{id}` — Get a workflow template by ID
- PUT `/api/v1/workflow-template/{id}` — Update a workflow template with optional node definitions
- DELETE `/api/v1/workflow-template/{id}` — Delete a workflow template
- GET `/api/v1/workflow-exception` — Get all open task exceptions
- GET `/api/v1/workflow-exception-assignment-rule` — Get all assignment rules
- POST `/api/v1/workflow-exception-assignment-rule` — Create a new assignment rule
- GET `/api/v1/workflow-execution` — Get all workflow executions
- *+ 53 more (search api.json for `api/v1/workflow` to see all)*

### Onboarding Workflows
*39 endpoints* | Prefix: `/api/v1/onboarding`
- GET `/api/v1/onboarding/draft/by-workflow/{workflowId}/summary` — Get draft status summary
- GET `/api/v1/onboarding/draft/{draftId}/relationships` — Get draft relationships
- GET `/api/v1/onboarding/workflow/count` — Count onboarding workflows
- POST `/api/v1/onboarding/workflow/match-search` — Search for entity matches
- GET `/api/v1/onboarding/workflow/{workflowId}/export` — Export completed workflow
- GET `/api/v1/onboarding/workflow/{workflowId}/relationships` — List draft relationships
- GET `/api/v1/onboarding/draft/by-workflow/{workflowId}` — Get drafts by workflow
- POST `/api/v1/onboarding/draft/decisions/bulk` — Submit bulk decisions
- POST `/api/v1/onboarding/draft/relationship/{relationshipId}/approve` — Approve relationship
- POST `/api/v1/onboarding/draft/relationship/{relationshipId}/reject` — Reject relationship
- *+ 29 more (search api.json for `api/v1/onboarding` to see all)*

### Trust Distributions & Rules
*27 endpoints* | Prefix: `/api/v1/trust-distribution`
- GET `/api/v1/trust-distribution-rule/{id}` — Get an entity by ID
- PUT `/api/v1/trust-distribution-rule/{id}` — Update an existing entity
- DELETE `/api/v1/trust-distribution-rule/{id}` — Delete an entity
- PATCH `/api/v1/trust-distribution-rule/{id}` — Partially update an entity
- GET `/api/v1/trust-distribution/{id}` — Get an entity by ID
- PUT `/api/v1/trust-distribution/{id}` — Update an existing entity
- DELETE `/api/v1/trust-distribution/{id}` — Delete an entity
- PATCH `/api/v1/trust-distribution/{id}` — Partially update an entity
- GET `/api/v1/trust-distribution` — Get all entities
- POST `/api/v1/trust-distribution` — Create a new entity
- *+ 17 more (search api.json for `api/v1/trust-distribution` to see all)*

### Supplemental Attributes (Custom Fields)
*56 endpoints* | Prefix: `/api/v1/supplemental-attribute-category`
- GET `/api/v1/supplemental-attribute-category/{id}` — Get an entity by ID
- PUT `/api/v1/supplemental-attribute-category/{id}` — Update an existing entity
- DELETE `/api/v1/supplemental-attribute-category/{id}` — Delete an entity
- PATCH `/api/v1/supplemental-attribute-category/{id}` — Partially update an entity
- GET `/api/v1/supplemental-attribute-choice-list/{id}` — Get an entity by ID
- PUT `/api/v1/supplemental-attribute-choice-list/{id}` — Update an existing entity
- DELETE `/api/v1/supplemental-attribute-choice-list/{id}` — Delete an entity
- PATCH `/api/v1/supplemental-attribute-choice-list/{id}` — Partially update an entity
- GET `/api/v1/supplemental-attribute-definition/{id}` — Get an entity by ID
- PUT `/api/v1/supplemental-attribute-definition/{id}` — Update an existing entity
- *+ 46 more (search api.json for `api/v1/supplemental-attribute-category` to see all)*

### Authentication & User Management
*162 endpoints* | Prefix: `/api/v1/authenticate`
- GET `/api/v1/account-financial/search` — Search financial accounts
- GET `/api/v1/account-financial/{id}` — Get an entity by ID
- PUT `/api/v1/account-financial/{id}` — Update an existing entity
- DELETE `/api/v1/account-financial/{id}` — Delete an entity
- PATCH `/api/v1/account-financial/{id}` — Partially update an entity
- GET `/api/v1/account-portfolio/{id}` — Get portfolio by ID
- GET `/api/v1/account-portfolio/{id}/valuations/chart` — Get portfolio valuation chart data
- DELETE `/api/v1/admin/field-source-config/{id}` — Delete a field source override
- GET `/api/v1/admin/sso/identity-providers/{id}` — Get IdP configuration
- PUT `/api/v1/admin/sso/identity-providers/{id}` — Update IdP configuration
- *+ 152 more (search api.json for `api/v1/authenticate` to see all)*

### Reference Data (Enums & Lookups)
*125 endpoints* | Prefix: `/api/v1/enums`
- GET `/api/v1/references/household/{id}` — Get all references to a household
- GET `/api/v1/references/account/{id}` — Get all references to an account
- GET `/api/v1/references/bank/{id}` — Get all references to a bank
- GET `/api/v1/references/contact/{id}` — Get all references to a contact
- GET `/api/v1/references/custodian/{id}` — Get all references to a custodian
- GET `/api/v1/references/document/{id}` — Get all references to a document
- GET `/api/v1/references/firm/{id}` — Get all references to a firm
- GET `/api/v1/references/fund-share-class/{id}` — Get all references to a fund share class
- GET `/api/v1/references/fund/{id}` — Get all references to a fund
- GET `/api/v1/references/household/{id}/count` — Get reference count for a household
- *+ 115 more (search api.json for `api/v1/enums` to see all)*

### Integrations (Addepar, Custodians, Banks)
*115 endpoints* | Prefix: `/api/v1/integrations`
- GET `/api/v1/integrations/externalentity/search` — Search entities
- GET `/api/v1/integrations/addepar/portfolio-queries/{id}` — Get a portfolio query definition by ID
- PUT `/api/v1/integrations/addepar/portfolio-queries/{id}` — Update an existing portfolio query definition
- DELETE `/api/v1/integrations/addepar/portfolio-queries/{id}` — Soft-delete a portfolio query definition
- GET `/api/v1/integrations/administrator/{id}` — Get an entity by ID
- PUT `/api/v1/integrations/administrator/{id}` — Update an existing administrator (ADMIN only)
- DELETE `/api/v1/integrations/administrator/{id}` — Delete an administrator (ADMIN only)
- PATCH `/api/v1/integrations/administrator/{id}` — Partially update an administrator (ADMIN only)
- GET `/api/v1/integrations/bank/bankaccount/{id}` — Get an entity by ID
- PUT `/api/v1/integrations/bank/bankaccount/{id}` — Update an existing entity
- *+ 105 more (search api.json for `api/v1/integrations` to see all)*

### System & Valuations
*96 endpoints* | Prefix: `/api/v1/system`
- POST `/api/v1/system/valuations/households` — Manually trigger household valuation snapshots
- GET `/api/v1/version` — Get application version
- GET `/api/v1/rollup/households/{householdId}` — Get household rollup
- POST `/api/v1/system/instruments/cache/export` — Export instruments to cache
- POST `/api/v1/system/instruments/prices/cache/export` — Export price data to local cache
- GET `/api/v1/system/operations/jobs/{jobName}/history` — Get job execution history
- POST `/api/v1/system/valuation/fill-gaps` — Fill valuation gaps (dev only)
- GET `/api/v1/system/valuation/health` — Check valuation health (detect gaps)
- POST `/api/v1/system/valuation/historical` — Generate historical valuations
- POST `/api/v1/system/valuation/run` — Run full portfolio valuation
- *+ 86 more (search api.json for `api/v1/system` to see all)*
