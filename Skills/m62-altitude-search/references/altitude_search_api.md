# Altitude Search API Reference

## Authentication

### API Key (Recommended)
```bash
curl -H "X-API-Key: ak_live_xxxxxxxx" "${BASE_URL}/api/v1/..."
```

### JWT Token
```bash
TOKEN=$(curl -s -X POST "${BASE_URL}/api/v1/authenticate" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin","rememberMe":false}' | jq -r '.id_token')

curl -H "Authorization: Bearer ${TOKEN}" "${BASE_URL}/api/v1/..."
```

## Search Endpoints

All search endpoints use the same pattern:
```
GET /api/v1/{entity-type}/search?searchParams=searchFor:{query}&page=0&size=20
```

### Available Entity Search Endpoints

| Entity | Search URL | Key Search Fields |
|--------|-----------|-------------------|
| Individual | `/api/v1/individual/search` | firstName, lastName, email, phone |
| LegalEntity | `/api/v1/legal-entity/search` | legalName, dbaName, taxId, email |
| Household | `/api/v1/household/search` | name |
| AccountFinancial | `/api/v1/account-financial/search` | name, accountNumber |
| Contact | `/api/v1/contact/search` | firstName, lastName, email, phone |
| TangibleAsset | `/api/v1/tangible-asset/search` | name, description |
| InsurancePolicy | `/api/v1/insurance-policy/search` | name, policyNumber, carrier |
| Liability | `/api/v1/liability/search` | name, lender |
| Instrument | `/api/v1/instrument/search` | symbol, name, isin, cusip |
| Fund | `/api/v1/fund/search` | legalName, shortName |
| Strategy | `/api/v1/strategy/search` | name, description |
| Document | `/api/v1/document/search` | name, tags |
| Bank | `/api/v1/bank/search` | name |
| Custodian | `/api/v1/custodian/search` | name |

### Search Response Format
```json
{
  "content": [
    { "id": "uuid", "...entity fields..." }
  ],
  "pageable": { "pageNumber": 0, "pageSize": 20 },
  "totalElements": 42,
  "totalPages": 3,
  "first": true,
  "last": false
}
```

## Get Entity by ID

```
GET /api/v1/{entity-type}/{id}
```

All entities return their full DTO with all fields.

## Relationship Endpoints

```
GET /api/v1/{entity-type}/{id}/relationships      # All relationships
GET /api/v1/{entity-type}/{id}/relationships/from  # Outgoing (this entity → others)
GET /api/v1/{entity-type}/{id}/relationships/to    # Incoming (others → this entity)
```

**Supported on:** individual, legal-entity, household, account-financial, fund

### EntityRelationshipDto Fields
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Relationship ID |
| sourceEntityType | string | INDIVIDUAL, LEGAL_ENTITY, HOUSEHOLD, ACCOUNT_FINANCIAL, FUND, CONTACT |
| sourceEntityId | UUID | ID of source entity |
| sourceEntityName | string | Display name of source |
| targetEntityType | string | Same values as source |
| targetEntityId | UUID | ID of target entity |
| targetEntityName | string | Display name of target |
| relationshipType | string | See types below |
| ownershipPercentage | decimal | For OWNERSHIP relationships |
| role | string | Additional role info (e.g., "Accountant" for ADVISOR type) |
| isPrimary | boolean | Whether this is the primary relationship of its type |
| effectiveFrom | date | When relationship started |
| effectiveTo | date | When relationship ended (null = current) |
| currency | string | CURRENT or HISTORICAL |

### Relationship Types
**Ownership/Control:** OWNERSHIP, BENEFICIAL_OWNERSHIP, MEMBER, TRUSTEE, BENEFICIARY, GRANTOR, SUCCESSOR_TRUSTEE, AUTHORIZED_SIGNER, POWER_OF_ATTORNEY, GUARDIAN, INSURED, OFFICER, DIRECTOR, PARTNER
**Advisory:** ADVISOR, CUSTODIAN, ACCOUNTANT, ATTORNEY
**Family:** SPOUSE, PARENT, CHILD, SIBLING, SON_IN_LAW, DAUGHTER_IN_LAW, FATHER_IN_LAW, MOTHER_IN_LAW
**Entity:** PARENT_ENTITY, SUBSIDIARY, AFFILIATE

## Entity-Specific Endpoints

### Household

```bash
GET /api/v1/individual/{id}/household          # Find household for individual
GET /api/v1/legal-entity/{id}/household        # Find household for legal entity
GET /api/v1/account-financial/{id}/household   # Find household for account
```
Returns: `{ "id": "uuid", "name": "Smith Household" }` or 404

### Tangible Assets

```bash
GET /api/v1/individual/{id}/tangible-assets        # Person's physical assets
GET /api/v1/household/{id}/tangible-assets         # Household's physical assets
GET /api/v1/legal-entity/{id}/tangible-assets      # Entity's physical assets
```

### Insurance Policies

```bash
GET /api/v1/individual/{id}/insurance-policies     # Person's policies
GET /api/v1/household/{id}/insurance-policies      # Household's policies
GET /api/v1/legal-entity/{id}/insurance-policies   # Entity's policies
```

### Liabilities

```bash
GET /api/v1/individual/{id}/liabilities            # Person's debts
GET /api/v1/household/{id}/liabilities             # Household's debts
GET /api/v1/individual/{id}/liability-summary      # Aggregated debt totals
GET /api/v1/household/{id}/liability-summary       # Household debt totals
```

### Notes

```bash
GET /api/v1/{entity-type}/{id}/notes               # Entity notes
```
Supported on: individual, legal-entity, account-financial, tangible-asset, liability, insurance-policy

### Trust Inspection

```bash
GET /api/v1/legal-entity/{id}/trust-summary        # Governance, trustees, beneficiaries, provisions
GET /api/v1/legal-entity/{id}/distribution-rules   # Distribution rules
GET /api/v1/legal-entity/{id}/distribution-rules?activeOnly=true
GET /api/v1/legal-entity/{id}/distribution-rules?beneficiaryId={uuid}
```

## Valuation Endpoints

### Account Valuations
```bash
GET /api/v1/account-financial/{id}/valuation                          # Latest
GET /api/v1/account-financial/{id}/valuation?date=2025-12-31         # Specific date
GET /api/v1/account-financial/{id}/valuation/history?startDate=...&endDate=...  # Time series
```

### Owner Valuations (Individual/LegalEntity — ownership-weighted)
```bash
GET /api/v1/owner-valuation/{ownerId}                                # Latest
GET /api/v1/owner-valuation/{ownerId}/history?startDate=...&endDate=...
```

### Household Valuations (Family net worth)
```bash
GET /api/v1/household-valuation/{householdId}                        # Latest
GET /api/v1/household-valuation/{householdId}/history?startDate=...&endDate=...
```

### Valuation Response Fields
| Field | Description |
|-------|-------------|
| marketValue | Total market value of positions |
| costBasis | Total cost basis |
| unrealizedGainLoss | marketValue - costBasis |
| totalTangibleAssetValue | Physical assets value |
| totalLiabilities | Total debts |
| netWorth | marketValue + tangibleAssets - liabilities |
| dayReturn, mtdReturn, ytdReturn | Performance metrics |

## Holdings & Positions

```bash
GET /api/v1/account-financial/{accountId}/positions?page=0&size=50
GET /api/v1/account-portfolio/{portfolioId}/positions?page=0&size=50
```

### Position Response Fields
| Field | Description |
|-------|-------------|
| instrumentSymbol | Ticker symbol |
| instrumentName | Security name |
| quantity | Number of shares/units |
| costBasis | Total cost basis |
| marketValue | Current market value |
| unrealizedGainLoss | P&L |
| assetClass | EQUITY, FIXED_INCOME, etc. |
| lastPrice | Most recent price |

## Transactions

```bash
GET /api/v1/account-financial/{accountId}/transactions?page=0&size=50
```

### Transaction Types
BUY, SELL, DIVIDEND, INTEREST, DEPOSIT, WITHDRAWAL, FEE, CAPITAL_CALL, DISTRIBUTION, TRANSFER, STOCK_SPLIT, MERGER, SPINOFF

## Portfolio Analysis

```bash
GET /api/v1/account-portfolio/{portfolioId}/rebalancing   # Trade recommendations
GET /api/v1/account-financial/{accountId}/rebalancing      # Account-level rebalancing
```

### Rebalancing Response
```json
{
  "tradeRecommendations": [
    { "action": "SELL", "instrumentSymbol": "AAPL", "units": 50, "estimatedValue": 8500 },
    { "action": "BUY", "instrumentSymbol": "BND", "units": 100, "estimatedValue": 7200 }
  ],
  "projectedAllocations": [...],
  "summary": { "totalBuys": 2, "totalSells": 1, "netCashImpact": 1300 }
}
```

## Key Entity Schemas (Summary)

### IndividualDto
firstName, lastName, middleName, preferredName, salutation, suffix, dateOfBirth, dateOfDeath, email, phoneNumberPrimary, phoneNumberSecondary, ssn, taxId, taxIdType, gender, maritalStatus, citizenship, residency, occupation, employerName, jobTitle, biography, addressLegal, lifecycleStatus

### LegalEntityDto
legalName, dbaName, displayName, entityType (CORPORATION, LLC, TRUST, PARTNERSHIP, etc.), taxId, jurisdiction, formationDate, registrationNumber, email, phone, taxClassification, fiscalYearEnd, incorporationCountry, incorporationState, trustFields (revocable, grantorTrust, trustSitus, governingLaw, etc.), llcFields, corporationFields

### HouseholdDto
name, description

### AccountFinancialDto
name, accountNumber, accountCategory, accountSubcategory, taxStatus, active, custodian, strategy

### TangibleAssetDto
name, description, category (LUXURY, VEHICLE, REAL_PROPERTY, COLLECTIBLE, OTHER), assetType, estimatedValue, currency, acquisitionDate, condition, location, serialNumber

### InsurancePolicyDto
name, policyNumber, carrier, category (LIFE, UMBRELLA, LONG_TERM_CARE, etc.), coverageAmount, annualPremium, effectiveDate, expirationDate, status, subtypeFields (cashValue, deathBenefit, dailyBenefit, monthlyBenefit, etc.)

### LiabilityDto
name, liabilityType, lender, currentBalance, originalBalance, interestRate, interestRateType, monthlyPayment, originationDate, maturityDate, linkedTangibleAssetId, linkedAccountFinancialId
