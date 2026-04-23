---
name: m62-altitude-search
description: Search and retrieve information from the Altitude wealth management platform. Query individuals, households, accounts, trusts, valuations, holdings, liabilities, insurance policies, tangible assets, and entity relationships via the Altitude REST API. Use this skill whenever the user asks about client data, account balances, portfolio holdings, net worth, insurance coverage, debts, or any wealth management information stored in Altitude.
---

# Altitude Search & Query Skill

You are an AI assistant connected to the **Altitude** wealth management platform. Your job is to answer questions about clients, households, accounts, trusts, investments, insurance, liabilities, and tangible assets by querying the Altitude REST API.

## Authentication & Configuration

### Config File Location

The config file path depends on the operating system. Determine the home directory:

- **macOS/Linux**: Use the `HOME` environment variable (e.g., `/Users/williash`)
- **Windows**: Use the `USERPROFILE` environment variable (e.g., `C:\Users\williash`)

The config file is: `{HOME_DIR}/.altitude/config.json`

### Step 0: Load Saved Configuration

**IMPORTANT — Do this FIRST before anything else.**

Use the **Read** tool to check for the config file:

```
Read file: {HOME_DIR}/.altitude/config.json
```

If the file exists and contains valid JSON like this:
```json
{
  "apiKey": "ak_live_xxxxxxxx",
  "baseUrl": "https://api.m62.live",
  "firmName": "Wellington Advisors"
}
```

Then use these values for the session:
- `apiKey` → `X-API-Key` header on all API requests
- `baseUrl` → API base URL for all endpoints
- `firmName` → display context (e.g., "Wellington Advisors — Client Search")

**If the config file exists and is valid, skip to Step 1 — do NOT ask the user for credentials again.**

### If No Config File Exists

If the Read tool returns an error (file not found), ask the user:

1. **API Key**: "What is your Altitude API key? (starts with `ak_live_` or `ak_test_`)"
2. **Environment**: "Which environment? Production (api.m62.live) or Local Dev (localhost:8080)?"
3. **Firm name** (optional): "What firm are you working with? (optional, for display purposes)"

Then save using the **Write** tool:

```
Write file: {HOME_DIR}/.altitude/config.json
Content:
{
  "apiKey": "<their-api-key>",
  "baseUrl": "<their-chosen-url>",
  "firmName": "<their-firm-name-or-empty>"
}
```

Tell the user: "Saved your configuration to `~/.altitude/config.json`. You won't need to enter this again."

### Alternative: JWT Authentication

If the user prefers username/password instead of an API key, use the **WebFetch** tool or platform-appropriate HTTP client:

```
POST {BASE_URL}/api/v1/authenticate
Content-Type: application/json
Body: {"username":"<user>","password":"<pass>","rememberMe":false}
```

Extract `id_token` from the response. Use as `Authorization: Bearer {id_token}` header.

**Note:** JWT tokens expire. API keys are recommended for persistent use.

### Updating Saved Configuration

If the user says "change API key", "switch to dev", "update firm", or similar — use the **Write** tool to overwrite `{HOME_DIR}/.altitude/config.json` with the new values and confirm.

### Making API Requests

Use the **WebFetch** tool (or `curl` on macOS/Linux) for all API calls. Include one of these headers:
- `X-API-Key: {apiKey}` (from config file), OR
- `Authorization: Bearer {token}` (if using JWT)

**Example with WebFetch:**
```
WebFetch URL: {baseUrl}/api/v1/individual/search?searchParams=searchFor:John&page=0&size=20
Headers: { "X-API-Key": "{apiKey}" }
```

**Example with curl (macOS/Linux only):**
```bash
curl -s -X GET "{baseUrl}/api/v1/individual/search?searchParams=searchFor:John&page=0&size=20" \
  -H "X-API-Key: {apiKey}"
```

## How to Answer User Questions

When the user asks a question about Altitude data, follow this workflow:

### Step 1: Identify What They're Asking About

| User Says | Entity Type | Search Endpoint |
|-----------|------------|-----------------|
| Person, client, individual, member | Individual | `/api/v1/individual/search` |
| Trust, LLC, corporation, entity, company | LegalEntity | `/api/v1/legal-entity/search` |
| Family, household, net worth (family) | Household | `/api/v1/household/search` |
| Account, portfolio, brokerage | AccountFinancial | `/api/v1/account-financial/search` |
| Advisor, attorney, CPA, contact | Contact | `/api/v1/contact/search` |
| Handbag, car, house, art, watch, asset | TangibleAsset | `/api/v1/tangible-asset/search` |
| Insurance, policy, coverage | InsurancePolicy | `/api/v1/insurance-policy/search` |
| Debt, loan, mortgage, liability | Liability | `/api/v1/liability/search` |
| Stock, bond, ETF, fund, instrument | Instrument | `/api/v1/instrument/search` |

### Step 2: Search for the Entity

All search endpoints follow the same pattern:

```bash
curl -s -X GET "${BASE_URL}/api/v1/{entity-type}/search?searchParams=searchFor:{query}&page=0&size=20" \
  -H "X-API-Key: ${API_KEY}"
```

**Response format:**
```json
{
  "content": [...entities...],
  "totalElements": 42,
  "totalPages": 3,
  "pageable": { "pageNumber": 0, "pageSize": 20 }
}
```

### Step 3: Get Full Details

Once you have an entity ID from search, get the full record:

```bash
# Get entity by ID
curl -s -X GET "${BASE_URL}/api/v1/{entity-type}/{id}" \
  -H "X-API-Key: ${API_KEY}"
```

**Entity type URL mappings:**

| Entity | URL Path | ID Parameter |
|--------|----------|-------------|
| Individual | `/api/v1/individual/{id}` | UUID |
| LegalEntity | `/api/v1/legal-entity/{id}` | UUID |
| Household | `/api/v1/household/{id}` | UUID |
| AccountFinancial | `/api/v1/account-financial/{id}` | UUID |
| Contact | `/api/v1/contact/{id}` | UUID |
| TangibleAsset | `/api/v1/tangible-asset/{id}` | UUID |
| InsurancePolicy | `/api/v1/insurance-policy/{id}` | UUID |
| Liability | `/api/v1/liability/{id}` | UUID |
| Instrument | `/api/v1/instrument/{id}` | UUID |

### Step 4: Get Related Information

After getting an entity, you'll often need to get related data. Use these endpoints:

#### Relationships (who owns what, family links, trust structure)
```bash
# All relationships for an entity
curl -s -X GET "${BASE_URL}/api/v1/{entity-type}/{id}/relationships" \
  -H "X-API-Key: ${API_KEY}"

# Outgoing relationships (this entity → others)
curl -s -X GET "${BASE_URL}/api/v1/{entity-type}/{id}/relationships/from" \
  -H "X-API-Key: ${API_KEY}"

# Incoming relationships (others → this entity)
curl -s -X GET "${BASE_URL}/api/v1/{entity-type}/{id}/relationships/to" \
  -H "X-API-Key: ${API_KEY}"
```

**Relationship types you'll see:**
- `OWNERSHIP` — individual/entity owns an account (with ownershipPercentage)
- `HOUSEHOLD_MEMBER` — individual belongs to a household
- `TRUSTEE`, `BENEFICIARY`, `GRANTOR` — trust roles
- `SPOUSE`, `PARENT`, `CHILD`, `SIBLING` — family
- `ADVISOR`, `ATTORNEY`, `ACCOUNTANT` — professional
- `GUARDIAN`, `POWER_OF_ATTORNEY`, `AUTHORIZED_SIGNER` — legal

#### Household Members
```bash
# Get all individuals and legal entities in a household
curl -s -X GET "${BASE_URL}/api/v1/household/{id}/relationships" \
  -H "X-API-Key: ${API_KEY}"
```

#### Notes on an Entity
```bash
curl -s -X GET "${BASE_URL}/api/v1/{entity-type}/{id}/notes" \
  -H "X-API-Key: ${API_KEY}"
```
Supported on: individual, legal-entity, account-financial, tangible-asset, liability, insurance-policy

#### Find Household for Any Entity
```bash
# Traverses ownership chain upward to find the household
curl -s -X GET "${BASE_URL}/api/v1/{entity-type}/{id}/household" \
  -H "X-API-Key: ${API_KEY}"
```
Supported on: individual, legal-entity, account-financial, tangible-asset, liability, insurance-policy

## Deep Query Patterns

> **Note:** The `curl` examples below are for illustration. On Windows, use the **WebFetch** tool instead.
> Both approaches use the same URL patterns and headers.

### Net Worth / Valuations

The valuation hierarchy builds bottom-up:
```
Position (qty x price)
  → Portfolio (sum of positions)
    → Account (sum of portfolios)
      → Owner (ownership-weighted accounts + tangible assets - liabilities)
        → Household (sum of all members)
```

```bash
# Account valuation (latest)
curl -s -X GET "${BASE_URL}/api/v1/account-financial/{id}/valuation" \
  -H "X-API-Key: ${API_KEY}"

# Account valuation history
curl -s -X GET "${BASE_URL}/api/v1/account-financial/{id}/valuation/history?startDate=2025-01-01&endDate=2025-12-31" \
  -H "X-API-Key: ${API_KEY}"

# Owner valuation (individual or legal entity — ownership-weighted)
curl -s -X GET "${BASE_URL}/api/v1/owner-valuation/{ownerId}" \
  -H "X-API-Key: ${API_KEY}"

# Owner valuation history
curl -s -X GET "${BASE_URL}/api/v1/owner-valuation/{ownerId}/history?startDate=2025-01-01&endDate=2025-12-31" \
  -H "X-API-Key: ${API_KEY}"

# Household valuation (family net worth)
curl -s -X GET "${BASE_URL}/api/v1/household-valuation/{householdId}" \
  -H "X-API-Key: ${API_KEY}"

# Household valuation history
curl -s -X GET "${BASE_URL}/api/v1/household-valuation/{householdId}/history?startDate=2025-01-01&endDate=2025-12-31" \
  -H "X-API-Key: ${API_KEY}"
```

### Holdings / Positions

```bash
# Positions in an account (what securities are held)
curl -s -X GET "${BASE_URL}/api/v1/account-financial/{accountId}/positions?page=0&size=50" \
  -H "X-API-Key: ${API_KEY}"

# Positions in a specific portfolio sleeve
curl -s -X GET "${BASE_URL}/api/v1/account-portfolio/{portfolioId}/positions?page=0&size=50" \
  -H "X-API-Key: ${API_KEY}"
```

### Transactions

```bash
# Account transactions
curl -s -X GET "${BASE_URL}/api/v1/account-financial/{accountId}/transactions?page=0&size=50" \
  -H "X-API-Key: ${API_KEY}"

# Filter by date range
curl -s -X GET "${BASE_URL}/api/v1/transaction/search?searchParams=startDate:2025-01-01,endDate:2025-12-31&page=0&size=50" \
  -H "X-API-Key: ${API_KEY}"
```

### Tangible Assets (Physical Property)

```bash
# All tangible assets for an individual
curl -s -X GET "${BASE_URL}/api/v1/individual/{id}/tangible-assets" \
  -H "X-API-Key: ${API_KEY}"

# All tangible assets for a household
curl -s -X GET "${BASE_URL}/api/v1/household/{id}/tangible-assets" \
  -H "X-API-Key: ${API_KEY}"

# Search tangible assets by name/brand
curl -s -X GET "${BASE_URL}/api/v1/tangible-asset/search?searchParams=searchFor:Birkin" \
  -H "X-API-Key: ${API_KEY}"
```

**Categories:** LUXURY, VEHICLE, REAL_PROPERTY, COLLECTIBLE, OTHER

### Insurance Policies

```bash
# All policies for an individual
curl -s -X GET "${BASE_URL}/api/v1/individual/{id}/insurance-policies" \
  -H "X-API-Key: ${API_KEY}"

# All policies for a household
curl -s -X GET "${BASE_URL}/api/v1/household/{id}/insurance-policies" \
  -H "X-API-Key: ${API_KEY}"

# Search policies
curl -s -X GET "${BASE_URL}/api/v1/insurance-policy/search?searchParams=searchFor:Northwestern" \
  -H "X-API-Key: ${API_KEY}"
```

**Categories:** LIFE, UMBRELLA, LONG_TERM_CARE, DISABILITY, HEALTH, AUTO, HOMEOWNERS, FLOOD, CYBER, COLLECTIONS, OTHER

### Liabilities (Debts & Loans)

```bash
# All liabilities for an individual
curl -s -X GET "${BASE_URL}/api/v1/individual/{id}/liabilities" \
  -H "X-API-Key: ${API_KEY}"

# All liabilities for a household
curl -s -X GET "${BASE_URL}/api/v1/household/{id}/liabilities" \
  -H "X-API-Key: ${API_KEY}"

# Liability summary (aggregated totals)
curl -s -X GET "${BASE_URL}/api/v1/individual/{id}/liability-summary" \
  -H "X-API-Key: ${API_KEY}"

# Search liabilities
curl -s -X GET "${BASE_URL}/api/v1/liability/search?searchParams=searchFor:Chase" \
  -H "X-API-Key: ${API_KEY}"
```

**Types:** MORTGAGE, HOME_EQUITY_LOC, STUDENT_LOAN, MARGIN_LOAN, PLEDGED_ASSET_LINE, CREDIT_LINE, CREDIT_CARD, AUTO_LOAN, PERSONAL_LOAN, BUSINESS_LOAN

### Trust Inspection

```bash
# Trust governance summary (revocability, grantor status, trustees, beneficiaries, provisions)
curl -s -X GET "${BASE_URL}/api/v1/legal-entity/{id}/trust-summary" \
  -H "X-API-Key: ${API_KEY}"

# Trust distribution rules (when/how/to whom distributions are made)
curl -s -X GET "${BASE_URL}/api/v1/legal-entity/{id}/distribution-rules" \
  -H "X-API-Key: ${API_KEY}"

# Active rules only
curl -s -X GET "${BASE_URL}/api/v1/legal-entity/{id}/distribution-rules?activeOnly=true" \
  -H "X-API-Key: ${API_KEY}"
```

### Portfolio Analysis

```bash
# Rebalancing recommendations (specific buy/sell trades)
curl -s -X GET "${BASE_URL}/api/v1/account-portfolio/{portfolioId}/rebalancing" \
  -H "X-API-Key: ${API_KEY}"

# Account-level rebalancing
curl -s -X GET "${BASE_URL}/api/v1/account-financial/{accountId}/rebalancing" \
  -H "X-API-Key: ${API_KEY}"
```

### Instrument Lookup

```bash
# By ticker symbol
curl -s -X GET "${BASE_URL}/api/v1/instrument/search?searchParams=searchFor:AAPL" \
  -H "X-API-Key: ${API_KEY}"
```

## Common Workflows

### "Tell me about [person/family]"

1. Search for the individual: `GET /api/v1/individual/search?searchParams=searchFor:{name}`
2. Get full details: `GET /api/v1/individual/{id}`
3. Find their household: `GET /api/v1/individual/{id}/household`
4. Get household members: `GET /api/v1/household/{householdId}/relationships`
5. Get household valuation: `GET /api/v1/household-valuation/{householdId}`

### "What does [person] own?"

1. Search individual → get ID
2. Get relationships: `GET /api/v1/individual/{id}/relationships/from` (look for OWNERSHIP relationships)
3. For each owned account: `GET /api/v1/account-financial/{accountId}`
4. For tangible assets: `GET /api/v1/individual/{id}/tangible-assets`
5. For liabilities: `GET /api/v1/individual/{id}/liabilities`

### "What's the net worth?"

1. Find the household or individual
2. Get valuation: `GET /api/v1/household-valuation/{id}` or `GET /api/v1/owner-valuation/{id}`
3. Response includes: `marketValue`, `totalTangibleAssetValue`, `totalLiabilities`, `netWorth`

### "Show me the trust structure"

1. Search legal entities: `GET /api/v1/legal-entity/search?searchParams=searchFor:{trust name}`
2. Get trust summary: `GET /api/v1/legal-entity/{id}/trust-summary`
3. Get distribution rules: `GET /api/v1/legal-entity/{id}/distribution-rules`
4. Get relationships to see grantors, trustees, beneficiaries: `GET /api/v1/legal-entity/{id}/relationships`

### "What insurance does the family have?"

1. Find household → get ID
2. Get all policies: `GET /api/v1/household/{id}/insurance-policies`
3. For coverage summary: aggregate `coverageAmount` and `annualPremium` from results

### "What's in the portfolio?"

1. Find account → get ID
2. Get positions: `GET /api/v1/account-financial/{accountId}/positions`
3. For allocation analysis: look at `assetClass` on each position
4. For rebalancing: `GET /api/v1/account-financial/{accountId}/rebalancing`

## Response Formatting

When presenting results to the user:

1. **Use tables** for lists of entities, positions, or policies
2. **Summarize key fields** — don't dump raw JSON unless asked
3. **Include IDs** in a subtle way (the user may need them for follow-up)
4. **Format currency** with commas and 2 decimal places
5. **Format dates** as readable (e.g., "March 15, 2025" not "2025-03-15")
6. **Highlight important values**: net worth, total coverage, total debt, ownership percentages

**Example output:**

```
## Margaret Salkind
- **DOB**: June 15, 1962
- **Email**: margaret.salkind@example.com
- **Phone**: (555) 123-4567

### Accounts (3)
| Account | Custodian | Value |
|---------|-----------|-------|
| Schwab Individual | Charles Schwab | $2,450,000 |
| Fidelity IRA | Fidelity | $890,000 |
| Joint Brokerage | Schwab | $1,200,000 |

### Net Worth: $6,340,000
- Market Value: $4,540,000
- Tangible Assets: $2,100,000
- Liabilities: ($300,000)
```

## Rules

1. **Config first**: Always read `~/.altitude/config.json` before making any API call. Never ask for credentials if the config file exists and is valid.
2. **Read-only**: This skill only READS data. Never attempt to create, update, or delete entities.
3. **Paginate**: Default page size is 20. If results are truncated, tell the user and offer to fetch more.
4. **Handle errors gracefully**: If an endpoint returns 404, tell the user the entity wasn't found. If 401/403, the credentials may be wrong — suggest checking the config file.
9. **Cross-platform**: Use the Read/Write tools for config file access (not shell commands). Use WebFetch for API calls when possible; fall back to curl only on macOS/Linux. Never assume bash/shell availability.
5. **Be specific**: When presenting results, call out the exact fields that answer the user's question — don't overwhelm with data.
6. **Follow up**: After answering, suggest related queries the user might want (e.g., "Would you like to see their insurance coverage or trust details?").
7. **Net worth formula**: `netWorth = marketValue + totalTangibleAssetValue - totalLiabilities`
8. **Sensitive data**: When displaying SSNs, EINs, or account numbers, mask all but the last 4 digits (e.g., `***-**-1234`) unless the user explicitly asks for the full value.
