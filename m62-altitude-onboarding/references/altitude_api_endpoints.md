# Altitude API - Detailed Endpoint Specifications

## Overview
This document contains comprehensive details for key Altitude API endpoints including authentication, search, relationships, document uploads, and PATCH operations.

**Updated:** 2026-04-17
**API Version:** 1.0.0
**API Title:** Altitude API
**Production URL:** https://api.m62.live
**Local Dev:** http://localhost:8080

> **Full OpenAPI spec:** For endpoints not covered here, search the full spec at
> `api-docs/api.json` (relative to this skill's directory). Use Glob to find it:
> `Glob pattern "**/m62-altitude-onboarding/**/api.json"`

---

## 0. AUTHENTICATION

### JWT Authentication
**Endpoint:** `POST /api/v1/authenticate`

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin",
  "rememberMe": false
}
```

**Response:**
```json
{
  "id_token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9..."
}
```

**Usage:** Include token in subsequent requests as `Authorization: Bearer {id_token}`

### API Key Authentication
**Header:** `X-API-Key: ak_live_xxxxxxxx`

Use the API key header for any endpoint. Recommended for automation and scripts.

**Example:**
```bash
curl -X GET "https://api.m62.live/api/v1/individual/search?searchFor=John" \
  -H "X-API-Key: ak_live_xxxxxxxx"
```

---

## 1. SEARCH ENDPOINTS

All search endpoints follow the same pattern and support pagination, sorting, and flexible query parameters.

**Common Query Parameters:**
- `searchParams` (required): Search parameters as query string. Supports `searchFor` for name/text search. Schema: `MultiValueMapStringString`
- `page` (optional): Zero-based page index (0..N). Type: integer. Default: 0. Minimum: 0
- `size` (optional): The size of the page to be returned. Type: integer. Default: 20. Minimum: 1
- `sort` (optional): Sorting criteria in the format: `property,(asc|desc)`. Type: array of strings. Multiple sort criteria are supported.
- `X-Tenant-ID` (optional, header): Tenant identifier for multi-tenant operations. Type: string

**Response Format (PagedModel):**
```json
{
  "content": [...],
  "pageable": {
    "pageNumber": 0,
    "pageSize": 20
  },
  "totalElements": 150,
  "totalPages": 8
}
```

### 1.1 GET /api/v1/individual/search
**Summary:** Search individuals

**Description:** Search for individuals using flexible query parameters. Supports text search in name, email, and phone fields.

**Response:** Array of `IndividualDto` objects in `content` field

**Example:**
```bash
curl -X GET "https://api.m62.live/api/v1/individual/search?searchFor=John&page=0&size=20" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 1.2 GET /api/v1/legal-entity/search
**Summary:** Search legal entities

**Description:** Search for legal entities using flexible query parameters.

**Response:** Array of `LegalEntityDto` objects in `content` field

---

### 1.3 GET /api/v1/household/search
**Summary:** Search households

**Description:** Search for households using flexible query parameters. Supports text search in name field.

**Response:** Array of `HouseholdDto` objects in `content` field

---

### 1.4 GET /api/v1/tangible-asset/search
**Summary:** Search tangible assets

**Description:** Search for tangible assets using flexible query parameters.

**Response:** Array of `TangibleAssetDto` objects in `content` field

---

### 1.5 GET /api/v1/account-financial/search
**Summary:** Search financial accounts

**Description:** Search for financial accounts using flexible query parameters. Supports text search in name and account number.

**Response:** Array of `AccountFinancialDto` objects in `content` field

---

### 1.6 GET /api/v1/contact/search
**Summary:** Search contacts

**Description:** Search for contacts using flexible query parameters. Supports text search in name, email, and phone.

**Response:** Array of `ContactDto` objects in `content` field

---

### 1.7 Count Endpoints
**GET /api/v1/{entity}/search/count**

Get total count of search results without pagination.

**Supported entities:** `individual`, `legal-entity`, `household`, `tangible-asset`, `account-financial`, `contact`

**Response:**
```json
{
  "count": 42
}
```

---

## 2. RELATIONSHIP ENDPOINTS

### 2.1 GET /api/v1/individual/{id}/relationships
**Summary:** Get all relationships for an individual

**Description:** Returns all relationships (both incoming and outgoing) for the individual entity.

**Path Parameters:**
- `id` (required): Individual ID (UUID). Type: string

**Query Parameters:**
- `X-Tenant-ID` (optional, header): Tenant identifier for multi-tenant operations. Type: string

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.2 GET /api/v1/individual/{id}/relationships/from
**Summary:** Get outgoing relationships from individual

**Description:** Returns outgoing relationships (relationships where this individual is the source).

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.3 GET /api/v1/individual/{id}/relationships/to
**Summary:** Get incoming relationships to individual

**Description:** Returns incoming relationships (relationships where this individual is the target).

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.4 GET /api/v1/legal-entity/{id}/relationships
**Summary:** Get all relationships for a legal entity

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.5 GET /api/v1/legal-entity/{id}/relationships/from
**Summary:** Get outgoing relationships from legal entity

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.6 GET /api/v1/legal-entity/{id}/relationships/to
**Summary:** Get incoming relationships to legal entity

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.7 GET /api/v1/account-financial/{id}/relationships
**Summary:** Get all relationships for a financial account

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.8 GET /api/v1/tangible-asset/{id}/relationships
**Summary:** Get all relationships for a tangible asset

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.9 GET /api/v1/household/{id}/relationships/from
**Summary:** Get outgoing relationships from a household

**Description:** Returns outgoing relationships (relationships where this household is the source). Available via RelationshipCapableResource.

**Response:** Array of `EntityRelationshipDto` objects

---

### 2.10 GET /api/v1/household/{id}/relationships/to
**Summary:** Get incoming relationships to a household

**Description:** Returns incoming relationships (relationships where this household is the target, e.g., MEMBER relationships from individuals).

**Response:** Array of `EntityRelationshipDto` objects

**Alternative standalone endpoint:** `GET /api/v1/entity-relationship/from/HOUSEHOLD/{householdId}` — returns the same data via the entity-relationship resource directly.

> **NOTE:** There is no combined `/api/v1/household/{id}/relationships` endpoint. Use `/from` and `/to` separately, or query via the standalone entity-relationship endpoints.

---

## 3. ENTITY RELATIONSHIP CREATION

### 3.1 POST /api/v1/entity-relationship
**Summary:** Create a new entity relationship

**Description:** Creates a new entity relationship in the system. This endpoint is used to add members to households and create relationships between entities.

**Query Parameters:**
- `tenantId` (optional): Tenant ID to use for this entity (admin only). Type: UUID string
- `X-Tenant-ID` (optional, header): Tenant identifier for multi-tenant operations. Type: string

**Request Body (application/json):**

Schema: `EntityRelationshipDto`

**Required Fields:**
- `relationshipType`: The type of relationship. Type: string
- `sourceEntityId`: UUID of the source entity
- `sourceEntityType`: Type of the source entity. Values: `HOUSEHOLD`, `INDIVIDUAL`, `LEGAL_ENTITY`, `USER`, `PARTY`, `FIRM`, `FUND`, `INSTRUMENT`, `CONTACT`, `ACCOUNT_FINANCIAL`, `TANGIBLE_ASSET`, `RELATIONSHIP_MANAGER`
- `targetEntityId`: UUID of the target entity
- `targetEntityType`: Type of the target entity. Values: same as sourceEntityType

**Optional Fields:**
- `percentage`: Ownership percentage or stake. Type: number. Example: 50.00 for 50%
- `role`: Role of the entity in the relationship. Type: string. Example: "Primary Owner", "Trustee"
- `description`: Human-readable description of the relationship. Type: string
- `notes`: Additional notes. Type: string
- `effectiveFrom`: Start date of the relationship. Type: date. Format: YYYY-MM-DD
- `effectiveTo`: End date of the relationship. Type: date. Format: YYYY-MM-DD
- `isPrimary`: Whether this is the primary relationship. Type: boolean
- `isSymmetric`: Whether the relationship is symmetric. Type: boolean
- `priority`: Priority level. Type: integer

**Valid RelationshipType Values:**
`OWNERSHIP`, `BENEFICIAL_OWNERSHIP`, `MEMBER`, `TRUSTEE`, `BENEFICIARY`, `GRANTOR`, `SUCCESSOR_TRUSTEE`, `SPOUSE`, `PARENT`, `CHILD`, `AUTHORIZED_SIGNER`, `POWER_OF_ATTORNEY`, `GUARDIAN`, `PARTNER`, `OFFICER`, `DIRECTOR`, `ADVISOR`, `ACCOUNTANT`, `ATTORNEY`

**Cardinality Constraints:**
- `SPOUSE`: max 1 on source entity
- `PARENT`: max 2 on target entity
- `GUARDIAN`: max 1 on target entity
- `OWNERSHIP`, `BENEFICIAL_OWNERSHIP`, `MEMBER`, `PARTNER`: percentage required

**Response:**
- **201 Created**: Entity relationship created successfully
  - Content-Type: `application/json`
  - Schema: `EntityRelationshipDto`
- **400 Bad Request**: Invalid input data
  - Schema: `ErrorResponse`
- **403 Forbidden**: Access denied due to tenant restrictions

**Example Request - Add Individual to Household:**
```json
{
  "relationshipType": "MEMBER",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440001",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "550e8400-e29b-41d4-a716-446655440002",
  "targetEntityType": "HOUSEHOLD",
  "percentage": 100.00,
  "isPrimary": true,
  "effectiveFrom": "2024-01-01"
}
```

**Example Request - Ownership in LLC:**
```json
{
  "relationshipType": "MEMBER",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440001",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "550e8400-e29b-41d4-a716-446655440003",
  "targetEntityType": "LEGAL_ENTITY",
  "percentage": 60.00,
  "role": "Member",
  "effectiveFrom": "2023-06-15"
}
```

**EntityRelationshipDto Structure:**

**Required Fields:**
- `relationshipType`: The type of relationship (e.g., OWNERSHIP, MEMBER, etc.). Type: string
- `sourceEntityId`: UUID of the source entity
- `sourceEntityType`: Type of the source entity (e.g., INDIVIDUAL, LEGAL_ENTITY, HOUSEHOLD)
- `targetEntityId`: UUID of the target entity
- `targetEntityType`: Type of the target entity (e.g., INDIVIDUAL, LEGAL_ENTITY, HOUSEHOLD)

**Optional Fields:**
- `id`: Relationship ID (UUID)
- `percentage`: Ownership percentage or stake. Type: number
- `role`: Role of the entity in the relationship. Type: string
- `description`: Human-readable description of the relationship
- `notes`: Additional notes
- `effectiveFrom`: Start date of the relationship. Type: date
- `effectiveTo`: End date of the relationship. Type: date
- `isPrimary`: Whether this is the primary relationship. Type: boolean
- `isSymmetric`: Whether the relationship is symmetric. Type: boolean
- `isSymmetricFlipped`: Whether the relationship is flipped. Type: boolean
- `priority`: Priority level. Type: integer
- `active`: Whether the relationship is active. Type: boolean
- `deleted`: Whether the relationship is deleted. Type: boolean
- `createdDate`: Timestamp of creation. Type: date-time
- `lastModifiedDate`: Timestamp of last modification. Type: date-time
- `createdBy`: User who created the relationship. Type: string
- `lastModifiedBy`: User who last modified the relationship. Type: string

---

## 4. DOCUMENT UPLOAD ENDPOINTS

All document upload endpoints use **multipart/form-data** format with the following structure:

**Request Format:**
```
POST /api/v1/{entity}/{id}/documents
Content-Type: multipart/form-data

Parts:
  createRequest (Content-Type: application/json): Document metadata
  file: <binary file>
  parsedData (Content-Type: application/json, optional): Pre-parsed document data

Query Parameters:
  sessionId (optional): UUID for batch tracking
  skipDuplicates (optional): boolean, default true
```

### 4.1 POST /api/v1/individual/{id}/documents
**Summary:** Upload a document for an individual

**Path Parameters:**
- `id` (required): Individual ID (UUID). Type: string

**Query Parameters:**
- `sessionId` (optional): Upload session ID for batch tracking. Type: UUID string
- `skipDuplicates` (optional): Skip uploading duplicate files (idempotent). Type: boolean. Default: true
- `X-Tenant-ID` (optional, header): Tenant identifier for multi-tenant operations. Type: string

**Request Body (multipart/form-data):**

**Part 1: createRequest (Content-Type: application/json)**

Schema: `IndividualDocumentCreateRequestDto`

**Part 2: file (Content-Type: application/octet-stream)**

Binary file content.

**Response:**
- **200 OK**: Document successfully attached
  - Schema: `IndividualDocumentDto`
- **400 Bad Request**: Invalid document data
- **404 Not Found**: Individual not found

---

### 4.2 POST /api/v1/legal-entity/{id}/documents
**Summary:** Upload a document for a legal entity

**Path Parameters:**
- `id` (required): Legal entity ID (UUID). Type: string

**Query Parameters:** Same as 4.1

**Request Body:** Multipart with `LegalEntityDocumentCreateRequestDto` and file

**Response:**
- **200 OK**: Document successfully attached
  - Schema: `LegalEntityDocumentDto`
- **400 Bad Request**: Invalid document data
- **404 Not Found**: Legal entity not found

---

### 4.3 POST /api/v1/account-financial/{id}/documents
**Summary:** Upload a document for a financial account

**Path Parameters:**
- `id` (required): Account ID (UUID). Type: string

**Query Parameters:** Same as 4.1

**Request Body:** Multipart with `AccountFinancialDocumentCreateRequestDto` and file

**Response:**
- **200 OK**: Document successfully attached
  - Schema: `AccountFinancialDocumentDto`

---

### 4.4 POST /api/v1/tangible-asset/{id}/documents
**Summary:** Upload a document for a tangible asset

**Path Parameters:**
- `id` (required): Tangible asset ID (UUID). Type: string

**Query Parameters:** Same as 4.1

**Request Body:** Multipart with `TangibleAssetDocumentCreateRequestDto` and file

**Response:**
- **200 OK**: Document successfully attached
  - Schema: `TangibleAssetDocumentDto`

---

### 4.5 ~~POST /api/v1/household/{id}/documents~~ — NOT SUPPORTED

> **Household does NOT support document upload.** There is no `HouseholdDocumentResource` or `HouseholdDocumentCreateRequestDto`.
>
> **Workaround:** Associate household-level documents with the primary individual or the primary legal entity in the household. Use the individual or legal entity document upload endpoints instead (sections 4.1 or 4.2).

---

### 4.6 POST /api/v1/insurance-policy/{policyId}/document

**Content-Type:** `multipart/form-data`

**Parts:**
- `createRequest` (application/json): `InsurancePolicyDocumentCreateRequestDto`
  - `documentSubType`: `DocumentTypeInsurancePolicy` enum value (e.g., POLICY_DECLARATION, CLAIM_FORM)
  - `title`, `description`, `tags` (inherited from base)
- `file`: The document file

**Query Parameters:**
- `sessionId` (optional): Upload session UUID for batch tracking
- `skipDuplicates` (optional, default: true): Skip if duplicate detected

**Response:** `InsurancePolicyDocumentDto`

### 4.7 POST /api/v1/liability/{liabilityId}/document

**Content-Type:** `multipart/form-data`

**Parts:**
- `createRequest` (application/json): `LiabilityDocumentCreateRequestDto`
  - `documentSubType`: `DocumentTypeLiability` enum value (e.g., LOAN_AGREEMENT, FORM_1098)
  - `title`, `description`, `tags` (inherited from base)
- `file`: The document file

**Query Parameters:**
- `sessionId` (optional): Upload session UUID for batch tracking
- `skipDuplicates` (optional, default: true): Skip if duplicate detected

**Response:** `LiabilityDocumentDto`

---

## 5. DOCUMENT REQUEST DTOs

### 5.1 Common Document Creation Request Fields

All document create request DTOs share these optional fields:

- `title`: String - Document title
- `description`: String - Document description
- `documentType`: Enum - Type of document. Values: `ACCOUNT`, `ACCOUNT_FINANCIAL`, `FUND`, `ORDER`, `INDIVIDUAL`, `LEGAL_ENTITY`, `INSTRUMENT`, `TANGIBLE_ASSET`, `OTHER`
- `documentSubType`: Enum - Document sub-type (see below for detailed lists)
- `contentType`: Enum - File content type. Values: `PDF`, `DOCX`, `DOC`, `XLSX`, `XLS`, `PPTX`, `PPT`, `TXT`, `CSV`, `JSON`, `XML`, `HTML`, `JPG`, `PNG`, `GIF`, `ZIP`, `MP4`, `MP3`
- `expiresAt`: String (date) - Document expiration date
- `tags`: Array of strings - Document tags (unique items)
- `associatedFormId`: UUID string - Associated form ID
- `docTypeHint`: String - Hint for document type detection

**IMPORTANT:** Always include `documentSubType`. If unsure, use `OTHER`.

### 5.2 IndividualDocumentCreateRequestDto

**Entity-Specific Fields:**
- `individualId`: UUID string - Individual ID

**Document Sub-Types:**
- **Identification:** `PASSPORT`, `DRIVERS_LICENSE`, `ENHANCED_DRIVERS_LICENSE`, `NATIONAL_ID`, `STATE_ID`, `BIRTH_CERTIFICATE`, `SOCIAL_SECURITY_CARD`, `CITIZENSHIP_CERTIFICATE`, `CERTIFICATE_OF_NATURALIZATION`, `PERMANENT_RESIDENT_CARD`, `MILITARY_ID`, `GLOBAL_ENTRY_CARD`, `TRIBAL_ID`, `CONSULAR_ID`, `FOREIGN_VOTER_CARD`, `REFUGEE_TRAVEL_DOCUMENT`, `DIPLOMATIC_ID`
- **Tax Documents:** `FORM_1040`, `FORM_W2`, `FORM_W9`, `FORM_1099_DIV`, `FORM_1099_INT`, `FORM_1099_B`, `FORM_1099_MISC`, `FORM_1099_R`, `FORM_K1_1065`, `FORM_K1_1120S`, `FORM_W8BEN`, `STATE_TAX_RETURN`, `PROPERTY_TAX_DOCUMENTS`
- **Compliance:** `ACCREDITED_INVESTOR_VERIFICATION`, `QUALIFIED_PURCHASER_VERIFICATION`, `AML_QUESTIONNAIRE`, `KYC_DOCUMENTATION`, `FATCA_CERTIFICATION`, `CRS_SELF_CERTIFICATION`, `OFAC_SCREENING`, `PEP_DISCLOSURE`
- **Financial:** `BANK_STATEMENT`, `INVESTMENT_STATEMENT`, `NET_WORTH_STATEMENT`, `CREDIT_REPORT`, `EMPLOYMENT_VERIFICATION`, `INCOME_VERIFICATION`, `FINANCIAL_STATEMENT`
- **Residence & Property:** `UTILITY_BILL`, `LEASE_AGREEMENT`, `PROPERTY_DEED`, `MORTGAGE_STATEMENT`
- **Legal:** `POWER_OF_ATTORNEY`, `NAME_CHANGE_DOCUMENT`, `MARRIAGE_CERTIFICATE`, `DIVORCE_DECREE`, `COURT_ORDER`
- **Investment:** `SUBSCRIPTION_AGREEMENT`, `INVESTMENT_POLICY_STATEMENT`, `INVESTMENT_QUESTIONNAIRE`, `INVESTOR_ACCREDITATION`
- **Default:** `OTHER`

### 5.3 LegalEntityDocumentCreateRequestDto

**Entity-Specific Fields:**
- `legalEntityId`: UUID string - Legal entity ID

**Document Sub-Types:**
- **Trust Documents:** `TRUST_AGREEMENT`, `TRUST_CERTIFICATION`, `TRUST_AMENDMENTS`, `REVOCABLE_TRUST_DOCUMENT`, `IRREVOCABLE_TRUST_DOCUMENT`, `TRUSTEE_CERTIFICATION`, `BENEFICIARY_DESIGNATION`, `TRUST_ASSET_SCHEDULE`
- **Corporate:** `ARTICLES_OF_INCORPORATION`, `CERTIFICATE_OF_INCORPORATION`, `CORPORATE_BYLAWS`, `CORPORATE_RESOLUTION`, `BOARD_MINUTES`, `SHAREHOLDER_MINUTES`, `STOCK_CERTIFICATE`, `STOCK_LEDGER`, `SHAREHOLDER_AGREEMENT`, `CERTIFICATE_OF_GOOD_STANDING`, `ANNUAL_REPORT`
- **LLC:** `ARTICLES_OF_ORGANIZATION`, `OPERATING_AGREEMENT`, `CERTIFICATE_OF_FORMATION`, `MEMBER_RESOLUTION`, `MEMBERSHIP_SCHEDULE`, `MANAGER_AUTHORIZATION`
- **Partnership:** `PARTNERSHIP_AGREEMENT`, `CERTIFICATE_OF_LIMITED_PARTNERSHIP`, `GENERAL_PARTNER_AUTHORIZATION`, `LIMITED_PARTNER_AGREEMENT`, `PARTNERSHIP_INTEREST_SCHEDULE`
- **Foundation:** `FOUNDATION_CHARTER`, `FOUNDATION_BYLAWS`, `BOARD_OF_DIRECTORS_ROSTER`, `GRANT_POLICY`
- **Tax & Registration:** `TAX_IDENTIFICATION`, `BUSINESS_LICENSE`, `BUSINESS_REGISTRATION`, `EIN_CONFIRMATION`, `DBA_CERTIFICATE`, `PROFESSIONAL_LICENSE`
- **Tax Returns:** `FORM_1065`, `FORM_1120`, `FORM_1120S`, `FORM_1041`, `FORM_K1_1065`, `FORM_K1_1120S`, `FORM_K1_1041`, `FORM_W9`, `FORM_W8BEN_E`, `STATE_TAX_RETURN`, `PROPERTY_TAX_DOCUMENTS`
- **Tax Exempt:** `TAX_EXEMPT_DETERMINATION`, `FORM_990`, `FORM_990_PF`, `CHARITABLE_REGISTRATION`, `SOLICITATION_LICENSE`
- **Compliance:** `AML_CERTIFICATION`, `KYC_DOCUMENTATION`, `BENEFICIAL_OWNERSHIP_CERTIFICATION`, `FATCA_CERTIFICATION`, `CRS_ENTITY_CERTIFICATION`, `OFAC_SCREENING`, `ACCREDITED_INVESTOR_VERIFICATION`, `QUALIFIED_PURCHASER_VERIFICATION`
- **Financial Statements:** `AUDITED_FINANCIALS`, `BALANCE_SHEET`, `INCOME_STATEMENT`, `CASH_FLOW_STATEMENT`, `BANK_STATEMENT`, `INVESTMENT_STATEMENT`, `BUSINESS_CREDIT_REPORT`
- **Legal & Authority:** `POWER_OF_ATTORNEY`, `AUTHORIZED_SIGNER_DOCUMENTATION`, `LEGAL_OPINION`, `INCUMBENCY_CERTIFICATE`, `CORPORATE_SEAL`
- **Investment:** `SUBSCRIPTION_AGREEMENT`, `INVESTMENT_POLICY_STATEMENT`, `INVESTOR_QUESTIONNAIRE`, `PPM_ACKNOWLEDGMENT`
- **Default:** `OTHER`

### 5.4 TangibleAssetDocumentCreateRequestDto

**Entity-Specific Fields:**
- `tangibleAssetId`: UUID string - Tangible asset ID

**Document Sub-Types:**
- **Ownership & Title:** `TITLE`, `DEED`, `REGISTRATION`, `BILL_OF_SALE`, `PURCHASE_RECEIPT`, `CERTIFICATE_OF_OWNERSHIP`, `TRANSFER_DOCUMENT`
- **Valuation & Assessment:** `APPRAISAL`, `VALUATION_REPORT`, `TAX_ASSESSMENT`, `COMPARABLE_ANALYSIS`, `BROKER_PRICE_OPINION`, `FMV_DETERMINATION`
- **Insurance:** `INSURANCE_POLICY`, `INSURANCE_CLAIM`, `COVERAGE_CERTIFICATE`, `INSURANCE_RIDER`, `INSURANCE_DECLARATION`, `INSURANCE_BINDER`, `PROOF_OF_INSURANCE`, `INSURANCE_RENEWAL`, `INSURANCE_CANCELLATION`
- **Maintenance & Condition:** `SERVICE_RECORD`, `INSPECTION_REPORT`, `WARRANTY`, `EXTENDED_WARRANTY`, `REPAIR_INVOICE`, `REPAIR_ESTIMATE`, `MAINTENANCE_LOG`, `RESTORATION_DOCUMENT`, `CONSERVATION_REPORT`
- **Liens & Agreements:** `LIEN`, `LIEN_RELEASE`, `LOAN_AGREEMENT`, `MORTGAGE`, `LEASE_AGREEMENT`, `RENTAL_AGREEMENT`, `LEGAL_AGREEMENT`, `POWER_OF_ATTORNEY`, `TRUST_DOCUMENT`
- **International/Shipping:** `BILL_OF_LADING`, `CUSTOMS_DECLARATION`, `IMPORT_EXPORT_DOCUMENT`
- **Tax & Financial:** `PROPERTY_TAX`, `DEPRECIATION_SCHEDULE`, `TAX_BASIS`, `EXCHANGE_1031`, `GIFT_TAX_DOCUMENT`, `ESTATE_TAX_DOCUMENT`, `CHARITABLE_DONATION_RECEIPT`
- **Authenticity & Provenance:** `CERTIFICATE_OF_AUTHENTICITY`, `CERTIFICATE_OF_ORIGIN`, `AUTHENTICATION_REPORT`, `PROVENANCE_HISTORY`, `AUCTION_DOCUMENTATION`, `CONDITION_REPORT`, `CATALOGUE_RAISONNE`, `EXHIBITION_HISTORY`, `LITERATURE_REFERENCE`, `EXPERT_OPINION`
- **Photos/Images:** `PRIMARY_PHOTO`, `DETAIL_PHOTO`, `CONDITION_PHOTO`, `RESTORATION_PHOTO`, `DAMAGE_PHOTO`, `PHOTO`
- **Vehicle/Aircraft/Marine:** `VEHICLE_HISTORY_REPORT`, `EMISSIONS_CERTIFICATE`, `SAFETY_INSPECTION`, `AIRWORTHINESS_CERTIFICATE`, `AIRCRAFT_LOGS`, `MARINE_SURVEY`, `COAST_GUARD_DOCUMENTATION`
- **Real Estate:** `SURVEY`, `TITLE_INSURANCE`, `HOME_INSPECTION`, `PEST_INSPECTION`, `ENVIRONMENTAL_ASSESSMENT`, `HOA_DOCUMENTS`, `ZONING_DOCUMENT`, `BUILDING_PERMIT`, `CERTIFICATE_OF_OCCUPANCY`, `FLOOR_PLANS`
- **Collectibles/Storage:** `CELLAR_INVENTORY`, `STORAGE_RECORDS`, `WINE_PROVENANCE`, `GRADING_CERTIFICATE`, `ENCAPSULATION_CERTIFICATE`
- **Estate & Beneficiary:** `BENEFICIARY_DESIGNATION`, `WILL_EXCERPT`, `DONATION_INTENT`, `ESTATE_APPRAISAL`
- **General:** `RECEIPT`, `CORRESPONDENCE`, `NOTES`, `OTHER`

### 5.5 AccountFinancialDocumentCreateRequestDto

**Entity-Specific Fields:**
- `accountFinancialId`: UUID string - Account ID

**Document Sub-Types:** Use appropriate subtype for financial documents (account statements, confirmations, etc.), default to `OTHER`

---

## 6. PATCH ENDPOINTS (PARTIAL UPDATES)

All PATCH endpoints support JSON Merge Patch semantics (RFC 7386), allowing selective field updates without affecting other properties. **Null values are ignored** (not treated as deletions).

### 6.1 PATCH /api/v1/individual/{id}
**Summary:** Partially update an individual

**Path Parameters:**
- `id` (required): Individual ID (UUID). Type: string. Pattern: `^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$`

**Query Parameters:**
- `includeDeleted` (optional): Include deleted entities. Type: boolean
- `scope` (optional): Data scope. Type: string. Values:
  - `FIRM` (user's firm only) - Default
  - `TENANT` (all firms in tenant)
  - `ALL_TENANTS` (all data)
  - `SHARED_REFERENCE` (shared reference data)
- `X-Tenant-ID` (optional, header): Tenant identifier. Type: string

**Request Body:**

Content-Type: `application/json` or `application/merge-patch+json`

Schema: `IndividualDto` (only provide fields you want to update)

**Response:**
- **200 OK**: Entity updated successfully
  - Schema: `IndividualDto` (updated entity)
- **400 Bad Request**: Invalid ID
- **404 Not Found**: Entity not found

**Accepts Partial Payloads:** Yes - only include fields you want to modify

---

### 6.2 PATCH /api/v1/legal-entity/{id}
**Summary:** Partially update a legal entity

**Path Parameters:**
- `id` (required): Legal entity ID (UUID)

**Query Parameters:** Same as 6.1

**Request Body:** Multipart with `LegalEntityDto`

**Response:**
- **200 OK**: Entity updated successfully
  - Schema: `LegalEntityDto`
- **400 Bad Request**: Invalid ID
- **404 Not Found**: Entity not found

---

### 6.3 PATCH /api/v1/tangible-asset/{id}
**Summary:** Partially update a tangible asset

**Path Parameters:**
- `id` (required): Tangible asset ID (UUID)

**Query Parameters:** Same as 6.1

**Request Body:** Multipart with `TangibleAssetDto`

**Response:**
- **200 OK**: Entity updated successfully
  - Schema: `TangibleAssetDto`
- **400 Bad Request**: Invalid ID
- **404 Not Found**: Entity not found

---

### 6.4 PATCH /api/v1/account-financial/{id}
**Summary:** Partially update a financial account

**Path Parameters:**
- `id` (required): Account ID (UUID)

**Query Parameters:** Same as 6.1

**Request Body:** Multipart with `AccountFinancialDto`

**Response:**
- **200 OK**: Entity updated successfully
  - Schema: `AccountFinancialDto`
- **400 Bad Request**: Invalid ID
- **404 Not Found**: Entity not found

---

### 6.5 PATCH /api/v1/contact/{id}
**Summary:** Partially update a contact

**Path Parameters:**
- `id` (required): Contact ID (UUID)

**Query Parameters:** Same as 6.1

**Request Body:** Multipart with `ContactDto`

**Response:**
- **200 OK**: Entity updated successfully
  - Schema: `ContactDto`
- **400 Bad Request**: Invalid ID
- **404 Not Found**: Entity not found

---

## 7. POST ENDPOINTS (CREATE)

All POST endpoints create new entities and return the created entity with a 201 status.

### 7.1 POST /api/v1/individual
**Summary:** Create a new individual

**Query Parameters:**
- `tenantId` (optional): Tenant ID to use (admin only). Type: UUID string
- `X-Tenant-ID` (optional, header): Tenant identifier. Type: string

**Request Body (application/json):**

Schema: `IndividualDto`

**Response:**
- **201 Created**: Entity created successfully
  - Schema: `IndividualDto`
- **400 Bad Request**: Invalid input data

---

### 7.2 POST /api/v1/legal-entity
**Summary:** Create a new legal entity

**Request Body:** `LegalEntityDto`

**Response:**
- **201 Created**: Entity created successfully
  - Schema: `LegalEntityDto`

---

### 7.3 POST /api/v1/tangible-asset
**Summary:** Create a new tangible asset

**Request Body:** `TangibleAssetDto`

**Response:**
- **201 Created**: Entity created successfully
  - Schema: `TangibleAssetDto`

---

### 7.4 POST /api/v1/household
**Summary:** Create a new household

**Request Body:** `HouseholdDto`

**Response:**
- **201 Created**: Entity created successfully
  - Schema: `HouseholdDto`

---

### 7.5 POST /api/v1/account-financial
**Summary:** Create a new financial account

**Request Body:** `AccountFinancialDto`

**Response:**
- **201 Created**: Entity created successfully
  - Schema: `AccountFinancialDto`

---

### 7.6 POST /api/v1/contact
**Summary:** Create a new contact

**Request Body:** `ContactDto`

**Response:**
- **201 Created**: Entity created successfully
  - Schema: `ContactDto`

---

## 8. ADDRESS FIELDS

All entities with addresses use the following `AddressDto` structure:

**Required Fields:**
- `addressLine1`: String - Street address. Example: "123 Main St"
- `city`: String - City name. Example: "New York"
- `state`: String - State code or name. Example: "NY"
- `postalCode`: String - ZIP or postal code. Example: "10001"
- `country`: CountryCode enum - ISO country code. Example: "US"
- `addressType`: AddressType enum - Type of address. Values: `PRIMARY`, `ADDITIONAL`

**Optional Fields:**
- `addressLine2`: String - Apartment, suite, etc. Example: "Suite 200"

**CountryCode Enum Values:**
Two-letter ISO 3166-1 codes (standard ISO country codes): `US`, `CA`, `GB`, `AU`, `DE`, `FR`, `JP`, `CN`, `IN`, `BR`, `MX`, etc.

**AddressType Enum Values:**
- `PRIMARY` - Primary address
- `ADDITIONAL` - Additional/secondary address

---

## 9. KEY FEATURES & BEHAVIORS

### 9.1 Search Endpoints
- **Pagination:** All search endpoints support pagination with `page` (0-based) and `size` (default 20, min 1)
- **Sorting:** Supports multi-field sorting using `sort` parameter with format `property,(asc|desc)`
- **Response Format:** All return `PagedModel` with `content`, `pageable`, `totalElements`, `totalPages`
- **Flexible Queries:** `searchParams` accepts flexible query strings

### 9.2 Relationships
- **Bidirectional Access:** Endpoints available for relationships from (`/from`) and to (`/to`) entities
- **Rich Metadata:** Relationships include ownership %, effective dates, roles, priority, and more
- **Symmetric Relationships:** Support for symmetric relationships that work both directions
- **Required Percentage:** OWNERSHIP, BENEFICIAL_OWNERSHIP, MEMBER, PARTNER relationships require `percentage` field

### 9.3 Document Uploads
- **Format:** Multipart/form-data (NOT JSON body)
- **Parts:** `createRequest` (application/json metadata) + `file` (binary content)
- **Session Tracking:** Optional `sessionId` for batch uploads and progress monitoring
- **Duplicate Prevention:** `skipDuplicates` flag for idempotent uploads (default: true)
- **Automatic Parsing:** Documents are automatically parsed
- **S3 Storage:** All documents stored in MinIO/S3

### 9.4 PATCH Operations
- **JSON Merge Patch:** Supports RFC 7386 semantics
- **Partial Updates:** Only include fields you want to change
- **Null Handling:** Null values are ignored (not treated as deletions)
- **Content Types:** Accept both `application/json` and `application/merge-patch+json`

### 9.5 Multi-Tenancy
- **Tenant Header:** `X-Tenant-ID` header available on most endpoints
- **Scope Parameter:** `scope` parameter on entity endpoints controls data visibility

---

## 10. AUTHENTICATION & HEADERS

**Bearer Token:**
```
Authorization: Bearer {id_token}
```

**API Key:**
```
X-API-Key: ak_live_xxxxxxxx
```

**Common Headers:**
- `X-Tenant-ID`: Optional tenant identifier for multi-tenant operations
- `Content-Type`: `application/json` or `application/merge-patch+json` (PATCH), `multipart/form-data` (uploads)

---

## 11. ERROR RESPONSES

Common error codes across all endpoints:
- **200/201**: Success (OK / Created)
- **400**: Bad Request - Invalid input data, invalid ID format, missing required fields
- **403**: Forbidden - Access denied due to permissions or tenant restrictions
- **404**: Not Found - Entity does not exist
- **409**: Conflict - Entity in use or deletion guard violation
- **500**: Internal Server Error

Error responses include:
- Schema: `ErrorResponse`
- Content: Error message and details

---

## 12. EXAMPLE WORKFLOWS

### Workflow: Onboarding a Household

**Step 1: Create the household**
```bash
POST /api/v1/household
Authorization: Bearer $TOKEN
Content-Type: application/json

{
  "householdName": "Smith Family",
  "description": "Primary household for the Smith family"
}
```

**Step 2: Create primary individual**
```bash
POST /api/v1/individual
Authorization: Bearer $TOKEN
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Smith",
  "email": "john@example.com",
  "dateOfBirth": "1960-05-15",
  "addressLegal": {
    "addressLine1": "123 Oak St",
    "city": "New York",
    "state": "NY",
    "postalCode": "10001",
    "country": "US",
    "addressType": "PRIMARY"
  }
}
```

**Step 3: Add individual to household**
```bash
POST /api/v1/entity-relationship
Authorization: Bearer $TOKEN
Content-Type: application/json

{
  "relationshipType": "MEMBER",
  "sourceEntityId": "{individual_uuid}",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "{household_uuid}",
  "targetEntityType": "HOUSEHOLD",
  "percentage": 100.0,
  "isPrimary": true
}
```

**Step 4: Upload identification document**
```bash
POST /api/v1/individual/{individual_uuid}/documents
Authorization: Bearer $TOKEN
Content-Type: multipart/form-data

--boundary
Content-Disposition: form-data; name="createRequest"
Content-Type: application/json

{
  "title": "Driver's License",
  "documentSubType": "DRIVERS_LICENSE",
  "contentType": "PNG"
}

--boundary
Content-Disposition: form-data; name="file"; filename="drivers_license.png"
Content-Type: application/octet-stream

<binary file content>
--boundary--
```

---

## 13. INSURANCE POLICY ENDPOINTS

Insurance policies represent coverage held by Individuals or LegalEntities. Supports LIFE, UMBRELLA, LONG_TERM_CARE, DISABILITY, HEALTH, AUTO, and OTHER categories. Uses a flat DTO approach where subtype-specific fields are present but null when not applicable -- the `policyCategory` discriminator tells the client which fields are relevant.

Ownership is tracked via entity relationships (OWNERSHIP, INSURED, BENEFICIARY types), not via fields on the policy itself.

### 13.1 GET /api/v1/insurance-policy
**Summary:** List all insurance policies with pagination

**Description:** Returns all insurance policies accessible to the current user's firm. Inherited from BaseTenantAwareResource.

**Query Parameters:**
- `includeDeleted` (optional): Include soft-deleted entities. Type: boolean. Default: false
- `scope` (optional): Data scope. Type: string. Values: `FIRM`, `TENANT`, `ALL_TENANTS`, `SHARED_REFERENCE`. Default: `FIRM`
- `page` (optional): Zero-based page index. Type: integer. Default: 0
- `size` (optional): Page size. Type: integer. Default: 20
- `sort` (optional): Sorting criteria `property,(asc|desc)`. Type: array of strings

**Response:**
- **200 OK**: Page of `InsurancePolicyDto` objects
- **403 Forbidden**: Access denied

---

### 13.2 GET /api/v1/insurance-policy/{id}
**Summary:** Get an insurance policy by ID

**Path Parameters:**
- `id` (required): Insurance policy ID (UUID). Type: string

**Query Parameters:**
- `includeDeleted` (optional): Include soft-deleted entities. Type: boolean. Default: false
- `scope` (optional): Data scope. Default: `FIRM`

**Response:**
- **200 OK**: `InsurancePolicyDto`
- **404 Not Found**: Policy not found

---

### 13.3 POST /api/v1/insurance-policy
**Summary:** Create a new insurance policy

**Request Body (application/json):**

Schema: `InsurancePolicyDto`

**Required Fields:**
- `policyCategory`: Enum. Values: `LIFE`, `UMBRELLA`, `LONG_TERM_CARE`, `DISABILITY`, `HEALTH`, `AUTO`, `HOMEOWNERS`, `FLOOD`, `CYBER`, `COLLECTIONS`, `WINDSTORM`, `OTHER`
- `name`: String (max 200). Display name for the policy
- `policyStatus`: Enum. Values: `ACTIVE`, `LAPSED`, `CANCELLED`, `PAID_UP`, `SURRENDERED`, `MATURED`, `PENDING`

**Optional Base Fields:**
- `policyNumber`: String (max 100). Policy number assigned by carrier
- `carrierName`: String (max 200). Name of the insurance carrier
- `coverageAmount`: BigDecimal. Total coverage amount (face value)
- `annualPremium`: BigDecimal. Annual premium amount
- `paymentFrequency`: Enum. Values: `MONTHLY`, `BI_WEEKLY`, `QUARTERLY`, `ANNUAL`, `INTEREST_ONLY`
- `effectiveDate`: Date. Coverage start date
- `expirationDate`: Date. Policy expiration or renewal date
- `applicationDate`: Date. Application submission date
- `issueDate`: Date. Policy issue date
- `description`: String (max 4000). Detailed description
- `deductible`: BigDecimal. Deductible amount
- `agentName`: String (max 200). Agent/broker name
- `agentPhone`: String (max 30). Agent phone
- `agentEmail`: String (max 200). Agent email
- `agentContactId`: UUID. Contact entity for the agent
- `policyDocumentId`: UUID. Policy document reference
- `notes`: String (max 4000). Free-text notes

**LIFE Subtype Fields (policyCategory = LIFE):**
- `lifePolicyType`: Enum. Values: check `/api/v1/insurance-policy/enums/life-policy-types`
- `deathBenefit`: BigDecimal. Death benefit amount
- `cashValue`: BigDecimal. Current cash value
- `cashValueAsOfDate`: Date
- `loanBalance`: BigDecimal. Outstanding policy loan
- `termLengthYears`: Integer. Term length in years
- `termExpirationDate`: Date
- `isConvertible`: Boolean. Whether term is convertible
- `conversionDeadline`: Date
- `isIlitOwned`: Boolean. Whether ILIT-owned
- `ilitLegalEntityId`: UUID. ILIT legal entity
- `isSecondToDie`: Boolean. Survivorship policy
- `secondInsuredIndividualId`: UUID
- `guaranteedDeathBenefit`: Boolean
- `riders`: String. Policy riders description
- `surrenderChargeSchedule`: String
- `dividendOption`: Enum. Values: check `/api/v1/insurance-policy/enums/dividend-options`

**UMBRELLA Subtype Fields (policyCategory = UMBRELLA):**
- `excessLiabilityCoverage`: BigDecimal
- `underlyingAutoRequired`: BigDecimal
- `underlyingHomeRequired`: BigDecimal
- `underlyingPoliciesDescription`: String
- `coversRentalProperties`: Boolean
- `coversWatercraft`: Boolean
- `uninsuredMotorist`: Boolean

**LONG_TERM_CARE Subtype Fields (policyCategory = LONG_TERM_CARE):**
- `dailyBenefitAmount`: BigDecimal
- `benefitPeriodDescription`: String
- `benefitPeriodMonths`: Integer
- `eliminationPeriodDays`: Integer
- `inflationProtectionType`: Enum. Values: check `/api/v1/insurance-policy/enums/inflation-protection-types`
- `coversHomeCare`: Boolean
- `coversAssistedLiving`: Boolean
- `coversNursingFacility`: Boolean
- `coversAdultDayCare`: Boolean
- `sharedBenefitRider`: Boolean
- `isPartnershipQualified`: Boolean
- `remainingBenefitPool`: BigDecimal

**DISABILITY Subtype Fields (policyCategory = DISABILITY):**
- `monthlyBenefitAmount`: BigDecimal
- `benefitPeriodDescription`: String (shared with LTC)
- `eliminationPeriodDays`: Integer (shared with LTC)
- `isOwnOccupation`: Boolean
- `ownOccupationPeriodDescription`: String
- `costOfLivingAdjustment`: Boolean
- `futureIncreaseOption`: Boolean
- `residualDisabilityRider`: Boolean
- `isGroupPolicy`: Boolean
- `isTaxableBenefit`: Boolean

**HOMEOWNERS Subtype Fields (policyCategory = HOMEOWNERS):**
- `dwellingCoverage`: BigDecimal. Coverage A: Dwelling
- `otherStructuresCoverage`: BigDecimal. Coverage B: Other structures
- `personalPropertyCoverage`: BigDecimal. Coverage C: Personal property/contents
- `lossOfUseCoverage`: BigDecimal. Coverage D: Loss of use
- `liabilityCoverage`: BigDecimal. Coverage E: Personal liability
- `medicalPaymentsCoverage`: BigDecimal. Coverage F: Medical payments
- `deductibleWindHail`: BigDecimal. Deductible for wind/hail
- `deductibleAllOtherPerils`: BigDecimal. Deductible for other perils
- `windExcluded`: Boolean. Whether wind/hurricane is excluded
- `constructionType`: String. Construction type (e.g., "Concrete Block")
- `yearBuilt`: Integer. Year dwelling was built

**FLOOD Subtype Fields (policyCategory = FLOOD):**
- `floodZone`: String. FEMA flood zone (e.g., "AE")
- `communityNumber`: String. NFIP community number
- `nfip`: Boolean. Whether NFIP vs private
- `buildingCoverage`: BigDecimal. Building/dwelling coverage
- `contentsCoverage`: BigDecimal. Contents coverage
- `hasElevationCertificate`: Boolean. Whether elevation cert is on file

**CYBER Subtype Fields (policyCategory = CYBER):**
- `aggregateLimit`: BigDecimal. Policy aggregate limit
- `retentionAmount`: BigDecimal. Self-insured retention
- `coversRansomware`: Boolean. Ransomware/extortion coverage
- `coversDataBreach`: Boolean. Data breach coverage
- `coversBusinessInterruption`: Boolean. Business interruption
- `coversSocialEngineering`: Boolean. Social engineering fraud
- `coversIdentityTheft`: Boolean. Identity theft restoration

**COLLECTIONS Subtype Fields (policyCategory = COLLECTIONS):**
- `totalScheduledValue`: BigDecimal. Total scheduled items value
- `blanketCoverageLimit`: BigDecimal. Blanket coverage for unscheduled items
- `agreedValue`: Boolean. Whether agreed value (no depreciation)
- `coversBreakage`: Boolean. Accidental breakage coverage
- `coversMysteriousDisappearance`: Boolean. Mysterious disappearance coverage
- `coversWorldwide`: Boolean. Worldwide coverage
- `scheduledItemCount`: Integer. Number of scheduled items
- `collectionCategories`: String. Categories covered (e.g., "Jewelry, Watches, Fine Art")

**Response:**
- **201 Created**: `InsurancePolicyDto` (created entity)
- **400 Bad Request**: Invalid input data

**Example Request (LIFE policy):**
```json
{
  "policyCategory": "LIFE",
  "name": "Northwestern Mutual Whole Life",
  "policyStatus": "ACTIVE",
  "policyNumber": "POL-2024-789456",
  "carrierName": "Northwestern Mutual",
  "coverageAmount": 2000000.00,
  "annualPremium": 18500.00,
  "paymentFrequency": "ANNUAL",
  "effectiveDate": "2020-01-01",
  "lifePolicyType": "WHOLE_LIFE",
  "deathBenefit": 2000000.00,
  "cashValue": 125000.00,
  "cashValueAsOfDate": "2026-01-01",
  "guaranteedDeathBenefit": true,
  "dividendOption": "PAID_UP_ADDITIONS"
}
```

---

### 13.4 PATCH /api/v1/insurance-policy/{id}
**Summary:** Partially update an insurance policy

**Path Parameters:**
- `id` (required): Insurance policy ID (UUID)

**Query Parameters:**
- `includeDeleted` (optional): boolean. Default: false
- `scope` (optional): Default: `FIRM`

**Request Body:** `InsurancePolicyDto` (only include fields to update)

**Content-Type:** `application/json` or `application/merge-patch+json`

**Response:**
- **200 OK**: `InsurancePolicyDto` (updated entity)
- **400 Bad Request**: Invalid ID
- **404 Not Found**: Policy not found

**Example Request:**
```json
{
  "cashValue": 135000.00,
  "cashValueAsOfDate": "2026-03-01",
  "annualPremium": 19200.00
}
```

---

### 13.5 DELETE /api/v1/insurance-policy/{id}
**Summary:** Soft delete an insurance policy

**Path Parameters:**
- `id` (required): Insurance policy ID (UUID)

**Query Parameters:**
- `force` (optional): Force permanent deletion (admin only). Type: boolean. Default: false

**Response:**
- **204 No Content**: Successfully deleted
- **404 Not Found**: Policy not found
- **409 Conflict**: Entity in use (deletion guard)

---

### 13.6 GET /api/v1/insurance-policy/by-individual/{individualId}
**Summary:** Get insurance policies by individual

**Description:** Retrieves all insurance policies associated with a specific Individual via OWNERSHIP and INSURED relationships.

**Path Parameters:**
- `individualId` (required): Individual UUID

**Query Parameters:**
- `page`, `size`, `sort` (optional): Pagination parameters

**Response:**
- **200 OK**: Page of `InsurancePolicyDto`

---

### 13.7 GET /api/v1/insurance-policy/by-legal-entity/{legalEntityId}
**Summary:** Get insurance policies by legal entity

**Description:** Retrieves all insurance policies owned by a specific LegalEntity via OWNERSHIP relationships. Use case: COLI, key person policies, ILIT-owned policies.

**Path Parameters:**
- `legalEntityId` (required): Legal Entity UUID

**Query Parameters:**
- `page`, `size`, `sort` (optional): Pagination parameters

**Response:**
- **200 OK**: Page of `InsurancePolicyDto`

---

### 13.8 GET /api/v1/insurance-policy/expiring-soon
**Summary:** Get policies expiring soon

**Description:** Retrieves all insurance policies expiring within the specified number of days. Use for compliance alerts and renewal reminders.

**Query Parameters:**
- `days` (optional): Number of days to look ahead. Type: integer. Default: 90
- `page`, `size`, `sort` (optional): Pagination parameters

**Response:**
- **200 OK**: Page of `InsurancePolicyDto`

---

### 13.9 GET /api/v1/insurance-policy/by-household/{householdId}

Retrieves all insurance policies owned by members of a household. Traverses Household → Individual/LegalEntity members → OWNERSHIP → Policies. Deduplicates shared policies.

**Parameters:**
- `householdId` (required): Household UUID

**Response:**
- **200 OK**: Page of `InsurancePolicyDto`

---

### 13.10 GET /api/v1/insurance-policy/summary/by-household/{householdId}

Aggregated insurance data for all household members: total coverage, total premium, policy count, breakdown by category.

**Parameters:**
- `householdId` (required): Household UUID

**Response:**
- **200 OK**: `InsurancePolicySummaryDto`

---

### 13.11 GET /api/v1/insurance-policy/summary/by-individual/{individualId}
**Summary:** Get insurance policy summary by individual

**Description:** Returns aggregated insurance data: total coverage, total annual premium, policy count, coverage breakdown by category.

**Path Parameters:**
- `individualId` (required): Individual UUID

**Response:**
- **200 OK**: `InsurancePolicySummaryDto`

**InsurancePolicySummaryDto Structure:**
```json
{
  "totalCoverage": 7500000.00,
  "totalAnnualPremium": 35000.00,
  "policyCount": 5,
  "coverageByCategory": {
    "LIFE": 2000000.00,
    "UMBRELLA": 5000000.00,
    "LONG_TERM_CARE": 500000.00
  }
}
```

---

### 13.12 Enum Listing Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/insurance-policy/enums/categories` | All policy categories (LIFE, UMBRELLA, LONG_TERM_CARE, DISABILITY, HEALTH, AUTO, HOMEOWNERS, FLOOD, CYBER, COLLECTIONS, WINDSTORM, OTHER) |
| `GET /api/v1/insurance-policy/enums/statuses` | All policy statuses (ACTIVE, LAPSED, CANCELLED, PAID_UP, SURRENDERED, MATURED, PENDING) |
| `GET /api/v1/insurance-policy/enums/life-policy-types` | All life policy types |
| `GET /api/v1/insurance-policy/enums/inflation-protection-types` | All inflation protection types |
| `GET /api/v1/insurance-policy/enums/dividend-options` | All dividend options |
| `GET /api/v1/insurance-policy/enums/document-types` | All insurance policy document types (27 values, 8 categories) |

**Response format for all enum endpoints:**
```json
[
  {
    "value": "LIFE",
    "displayName": "Life Insurance",
    "description": "Life insurance policy providing death benefit and potential cash value accumulation"
  }
]
```

---

### 13.13 Note Endpoints (via NoteResourceMixin)

Standard note CRUD endpoints nested under insurance policy:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/insurance-policy/{id}/notes` | Get all notes (newest first) |
| `GET` | `/api/v1/insurance-policy/{id}/notes/{noteId}` | Get a specific note |
| `POST` | `/api/v1/insurance-policy/{id}/notes` | Create a note |
| `PUT` | `/api/v1/insurance-policy/{id}/notes/{noteId}` | Update a note |
| `DELETE` | `/api/v1/insurance-policy/{id}/notes/{noteId}` | Delete a note |

**Create/Update Request Body:**
```json
{
  "noteText": "Policy premium increased by 5% at annual renewal."
}
```

**Response:** `InsurancePolicyNoteDto` (extends BaseNoteDto with `id`, `insurancePolicyId`, `insurancePolicyName`)

### 13.14 Document Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/insurance-policy/{policyId}/document` | Upload document (multipart) |
| `GET` | `/api/v1/insurance-policy/{policyId}/document` | List documents (paginated) |
| `DELETE` | `/api/v1/insurance-policy/{policyId}/document/{documentId}` | Soft-delete document |
| `GET` | `/api/v1/insurance-policy/{policyId}/document/{documentId}/download-url` | Get download URL |

**Upload:** Multipart form with `createRequest` (InsurancePolicyDocumentCreateRequestDto as JSON) + `file` (the document).

### 13.15 Supplemental Attribute Endpoints (via SupplementalAttributeResourceMixin)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/insurance-policy/{id}/attributes` | Get all supplemental attributes |
| `GET` | `/api/v1/insurance-policy/{id}/attributes/{attrKey}` | Get attribute by key |
| `POST` | `/api/v1/insurance-policy/{id}/attributes` | Create attribute value |
| `PUT` | `/api/v1/insurance-policy/{id}/attributes` | Add or update attribute |
| `PUT` | `/api/v1/insurance-policy/{id}/attributes/{attributeId}` | Update attribute by ID |
| `DELETE` | `/api/v1/insurance-policy/{id}/attributes/{attributeId}` | Delete attribute |

### 13.16 Household Filtering on List Endpoint

The main `GET /api/v1/insurance-policy` endpoint supports an optional `householdId` query parameter. When provided, results are filtered to only include policies owned by members of the specified household:

```
GET /api/v1/insurance-policy?householdId={uuid}
```

---

## 14. LIABILITY ENDPOINTS

Liabilities represent standalone debt obligations (mortgages, loans, credit lines, etc.) owned by Individuals or LegalEntities. Ownership is tracked via entity relationships (OWNERSHIP type). Total liabilities are subtracted from total assets to calculate net worth.

### 14.1 GET /api/v1/liability
**Summary:** List all liabilities with pagination

**Description:** Returns all liabilities accessible to the current user's firm. Inherited from BaseTenantAwareResource.

**Query Parameters:**
- `includeDeleted` (optional): Include soft-deleted entities. Type: boolean. Default: false
- `scope` (optional): Data scope. Values: `FIRM`, `TENANT`, `ALL_TENANTS`, `SHARED_REFERENCE`. Default: `FIRM`
- `page` (optional): Zero-based page index. Default: 0
- `size` (optional): Page size. Default: 20
- `sort` (optional): Sorting criteria `property,(asc|desc)`

**Response:**
- **200 OK**: Page of `LiabilityDto` objects
- **403 Forbidden**: Access denied

---

### 14.2 GET /api/v1/liability/{id}
**Summary:** Get a liability by ID

**Path Parameters:**
- `id` (required): Liability ID (UUID)

**Query Parameters:**
- `includeDeleted` (optional): boolean. Default: false
- `scope` (optional): Default: `FIRM`

**Response:**
- **200 OK**: `LiabilityDto`
- **404 Not Found**: Liability not found

---

### 14.3 POST /api/v1/liability
**Summary:** Create a new liability

**Request Body (application/json):**

Schema: `LiabilityDto`

**Required Fields:**
- `name`: String (max 200). Display name for the liability
- `liabilityType`: Enum. Values: `MORTGAGE`, `SECOND_MORTGAGE`, `HOME_EQUITY_LOC`, `STUDENT_LOAN`, `PERSONAL_LOAN`, `PRIVATE_LOAN`, `CREDIT_LINE`, `MARGIN_LOAN`, `AUTO_LOAN`, `BOAT_LOAN`, `AIRCRAFT_LOAN`, `ART_LOAN`, `BUSINESS_LOAN`, `CREDIT_CARD`, `PLEDGED_ASSET_LINE`, `OTHER`
- `liabilityStatus`: Enum. Values: `CURRENT`, `DELINQUENT`, `IN_DEFERMENT`, `IN_FORBEARANCE`, `PAID_OFF`, `DEFAULTED`, `CHARGED_OFF`

**Optional Fields:**
- `lenderName`: String (max 200). Lending institution name
- `accountNumber`: String (max 100). Loan/account number
- `originalBalance`: BigDecimal. Original principal at origination
- `currentBalance`: BigDecimal. Current outstanding balance
- `balanceAsOfDate`: Date. Date balance was last verified
- `creditLimit`: BigDecimal. Credit limit for revolving facilities
- `availableCredit`: BigDecimal. Available credit remaining
- `interestRate`: BigDecimal. Annual interest rate as percentage
- `interestRateType`: Enum. Values: `FIXED`, `VARIABLE`, `HYBRID`
- `indexRateDescription`: String (max 100). Index rate for variable loans (e.g., "Prime + 1.5%")
- `rateCap`: BigDecimal. Maximum rate cap for variable loans
- `rateFloor`: BigDecimal. Minimum rate floor for variable loans
- `monthlyPayment`: BigDecimal. Monthly payment amount
- `minimumPayment`: BigDecimal. Minimum payment for revolving credit
- `paymentFrequency`: Enum. Values: `MONTHLY`, `BI_WEEKLY`, `QUARTERLY`, `ANNUAL`, `INTEREST_ONLY`
- `nextPaymentDate`: Date
- `originationDate`: Date. Loan origination date
- `maturityDate`: Date. Loan maturity or renewal date
- `isSecured`: Boolean. Whether secured by collateral. Default: false
- `collateralDescription`: String (max 500). Description of collateral
- `linkedTangibleAssetId`: UUID. Cross-reference to tangible asset collateral
- `linkedAccountFinancialId`: UUID. Cross-reference to financial account
- `isInterestDeductible`: Boolean. Whether interest is tax-deductible. Default: false
- `interestDeductionType`: Enum. Values: `MORTGAGE_INTEREST`, `INVESTMENT_INTEREST`, `STUDENT_LOAN_INTEREST`, `BUSINESS_INTEREST`, `NONE`
- `interestPaidYtd`: BigDecimal. Interest paid year-to-date
- `interestPaidPriorYear`: BigDecimal. Interest paid prior year
- `hasLien`: Boolean. Whether the loan has a lien on the collateral asset
- `lienPosition`: String (max 20). Lien priority position (e.g., "FIRST", "SECOND")
- `lienRecordingInfo`: String (max 200). Lien recording information (county, instrument number)
- `payoffAmount`: BigDecimal. Current payoff amount (may include fees, differ from currentBalance)
- `payoffGoodThrough`: Date. Date through which the payoff quote is valid
- `lastPaymentDate`: Date. Date of the most recent payment made
- `notes`: String (max 4000). Free-text notes
- `description`: String (max 4000). Detailed description

**Response:**
- **201 Created**: `LiabilityDto` (created entity)
- **400 Bad Request**: Invalid input data

**Example Request (MORTGAGE):**
```json
{
  "name": "Chase Home Mortgage",
  "liabilityType": "MORTGAGE",
  "liabilityStatus": "CURRENT",
  "lenderName": "JPMorgan Chase",
  "accountNumber": "XXXX-1234",
  "originalBalance": 500000.00,
  "currentBalance": 425000.00,
  "balanceAsOfDate": "2026-03-01",
  "interestRate": 6.5000,
  "interestRateType": "FIXED",
  "monthlyPayment": 2750.00,
  "paymentFrequency": "MONTHLY",
  "nextPaymentDate": "2026-04-01",
  "originationDate": "2022-06-15",
  "maturityDate": "2052-06-15",
  "isSecured": true,
  "collateralDescription": "123 Main St, Anytown, CA 90210",
  "isInterestDeductible": true,
  "interestDeductionType": "MORTGAGE_INTEREST",
  "interestPaidYtd": 18750.00
}
```

---

### 14.4 PATCH /api/v1/liability/{id}
**Summary:** Partially update a liability

**Path Parameters:**
- `id` (required): Liability ID (UUID)

**Query Parameters:**
- `includeDeleted` (optional): boolean. Default: false
- `scope` (optional): Default: `FIRM`

**Request Body:** `LiabilityDto` (only include fields to update)

**Content-Type:** `application/json` or `application/merge-patch+json`

**Response:**
- **200 OK**: `LiabilityDto` (updated entity)
- **400 Bad Request**: Invalid ID
- **404 Not Found**: Liability not found

**Example Request:**
```json
{
  "currentBalance": 420000.00,
  "balanceAsOfDate": "2026-04-01",
  "interestPaidYtd": 21500.00
}
```

---

### 14.5 DELETE /api/v1/liability/{id}
**Summary:** Soft delete a liability

**Path Parameters:**
- `id` (required): Liability ID (UUID)

**Query Parameters:**
- `force` (optional): Force permanent deletion (admin only). Type: boolean. Default: false

**Response:**
- **204 No Content**: Successfully deleted
- **404 Not Found**: Liability not found
- **409 Conflict**: Entity in use (deletion guard)

---

### 14.6 GET /api/v1/liability/by-individual/{individualId}
**Summary:** Get liabilities by individual

**Description:** Retrieves all liabilities owned by a specific Individual via OWNERSHIP relationships. Handles direct ownership (100%) and partial ownership (joint liabilities).

**Path Parameters:**
- `individualId` (required): Individual UUID

**Query Parameters:**
- `page`, `size`, `sort` (optional): Pagination parameters

**Response:**
- **200 OK**: Page of `LiabilityDto`

---

### 14.7 GET /api/v1/liability/by-household/{householdId}
**Summary:** Get liabilities by household

**Description:** Retrieves all liabilities owned by members of a Household. Traverses Household -> Individual/LegalEntity members -> OWNERSHIP -> Liabilities. Deduplicates shared liabilities.

**Path Parameters:**
- `householdId` (required): Household UUID

**Query Parameters:**
- `page`, `size`, `sort` (optional): Pagination parameters

**Response:**
- **200 OK**: Page of `LiabilityDto`

---

### 14.8 GET /api/v1/liability/summary/by-individual/{individualId}
**Summary:** Get liability summary by individual

**Description:** Returns aggregated liability data: total outstanding balance, total monthly payment, liability count, balance breakdown by type.

**Path Parameters:**
- `individualId` (required): Individual UUID

**Response:**
- **200 OK**: `LiabilitySummaryDto`

**LiabilitySummaryDto Structure:**
```json
{
  "totalBalance": 750000.00,
  "totalMonthlyPayment": 5500.00,
  "liabilityCount": 4,
  "breakdownByType": {
    "MORTGAGE": 425000.00,
    "STUDENT_LOAN": 75000.00,
    "AUTO_LOAN": 35000.00,
    "CREDIT_CARD": 15000.00
  }
}
```

---

### 14.9 GET /api/v1/liability/summary/by-household/{householdId}
**Summary:** Get liability summary by household

**Description:** Returns aggregated liability data for all household members: total outstanding balance across all members, total monthly payment, liability count, balance breakdown by type.

**Path Parameters:**
- `householdId` (required): Household UUID

**Response:**
- **200 OK**: `LiabilitySummaryDto`

---

### 14.10 Enum Listing Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/liability/enums/types` | All liability types (MORTGAGE, SECOND_MORTGAGE, HOME_EQUITY_LOC, STUDENT_LOAN, PERSONAL_LOAN, PRIVATE_LOAN, CREDIT_LINE, MARGIN_LOAN, AUTO_LOAN, BOAT_LOAN, AIRCRAFT_LOAN, ART_LOAN, BUSINESS_LOAN, CREDIT_CARD, PLEDGED_ASSET_LINE, OTHER) |
| `GET /api/v1/liability/enums/statuses` | All liability statuses (CURRENT, DELINQUENT, IN_DEFERMENT, IN_FORBEARANCE, PAID_OFF, DEFAULTED, CHARGED_OFF) |
| `GET /api/v1/liability/enums/document-types` | All liability document types (13 values, 5 categories) |

**Response format for all enum endpoints:**
```json
[
  {
    "value": "MORTGAGE",
    "displayName": "Mortgage",
    "description": "Loan secured by real property (home, investment property)"
  }
]
```

---

### 14.11 Note Endpoints (via NoteResourceMixin)

Standard note CRUD endpoints nested under liability:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/liability/{id}/notes` | Get all notes (newest first) |
| `GET` | `/api/v1/liability/{id}/notes/{noteId}` | Get a specific note |
| `POST` | `/api/v1/liability/{id}/notes` | Create a note |
| `PUT` | `/api/v1/liability/{id}/notes/{noteId}` | Update a note |
| `DELETE` | `/api/v1/liability/{id}/notes/{noteId}` | Delete a note |

**Create/Update Request Body:**
```json
{
  "noteText": "Refinance application submitted to Chase, awaiting approval."
}
```

**Response:** `LiabilityNoteDto` (extends BaseNoteDto with `id`, `liabilityId`, `liabilityName`)

### 14.12 Document Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/liability/{liabilityId}/document` | Upload document (multipart) |
| `GET` | `/api/v1/liability/{liabilityId}/document` | List documents (paginated) |
| `DELETE` | `/api/v1/liability/{liabilityId}/document/{documentId}` | Soft-delete document |
| `GET` | `/api/v1/liability/{liabilityId}/document/{documentId}/download-url` | Get download URL |

**Upload:** Multipart form with `createRequest` (LiabilityDocumentCreateRequestDto as JSON) + `file` (the document).

### 14.13 Supplemental Attribute Endpoints (via SupplementalAttributeResourceMixin)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/liability/{id}/attributes` | Get all supplemental attributes |
| `GET` | `/api/v1/liability/{id}/attributes/{attrKey}` | Get attribute by key |
| `POST` | `/api/v1/liability/{id}/attributes` | Create attribute value |
| `PUT` | `/api/v1/liability/{id}/attributes` | Add or update attribute |
| `PUT` | `/api/v1/liability/{id}/attributes/{attributeId}` | Update attribute by ID |
| `DELETE` | `/api/v1/liability/{id}/attributes/{attributeId}` | Delete attribute |

---

## 15. NESTED PATCH PATTERNS (Embedded Entities on Parent)

Some entities are embedded within their parent entity and are updated via PATCH on the parent. They do not have their own standalone CRUD endpoints.

### 15.1 Estate Planning on Individual

**Endpoint:** `PATCH /api/v1/individual/{id}`

**Description:** Estate planning information is embedded on the Individual entity. Update it by including the `estatePlanning` object in the PATCH body. Only include the sections you want to update.

**Sections:**
- `will`: Will and testament information
- `healthcare`: Healthcare directive information
- `financialPoa`: Financial power of attorney information
- `guardianship`: Guardianship designations for minor children
- `maritalAgreement`: Prenuptial/postnuptial agreement information
- `estateReview`: Estate planning review and valuation information

**Example Request:**
```json
{
  "estatePlanning": {
    "will": {
      "hasWill": true,
      "willDate": "2024-01-15",
      "lastReviewedDate": "2025-06-01",
      "jurisdiction": "New York",
      "executorName": "Jane Smith",
      "executorIndividualId": "550e8400-e29b-41d4-a716-446655440001",
      "contingentExecutorName": "Robert Smith",
      "attorneyName": "Sarah Johnson, Esq.",
      "attorneyContactId": "550e8400-e29b-41d4-a716-446655440002",
      "notes": "Updated to include digital asset provisions"
    },
    "healthcare": {
      "hasHealthcareDirective": true,
      "directiveDate": "2024-03-20",
      "agentName": "Jane Smith",
      "agentIndividualId": "550e8400-e29b-41d4-a716-446655440001",
      "alternateAgentName": "Robert Smith",
      "hasLivingWill": true,
      "specificHealthcareWishes": "No extraordinary measures"
    },
    "financialPoa": {
      "hasFinancialPoa": true,
      "type": "DURABLE",
      "agentName": "Jane Smith",
      "agentIndividualId": "550e8400-e29b-41d4-a716-446655440001",
      "poaDate": "2024-01-15",
      "isCurrentlyEffective": true
    },
    "guardianship": {
      "hasGuardianDesignation": true,
      "guardianName": "Michael Johnson",
      "guardianIndividualId": "550e8400-e29b-41d4-a716-446655440003",
      "alternateGuardianName": "Sarah Johnson"
    },
    "maritalAgreement": {
      "hasPrenuptialAgreement": true,
      "prenuptialDate": "2018-06-01",
      "hasPostnuptialAgreement": false,
      "summary": "Separate property provisions for pre-marital assets",
      "attorneyContactId": "550e8400-e29b-41d4-a716-446655440004"
    },
    "estateReview": {
      "lastReviewDate": "2025-01-15",
      "nextReviewDate": "2028-01-15",
      "attorneyName": "Sarah Johnson, Esq.",
      "attorneyContactId": "550e8400-e29b-41d4-a716-446655440002",
      "estimatedEstateValue": 15000000.00,
      "estimatedEstateTaxLiability": 560000.00,
      "lifetimeGiftExclusionUsed": 2000000.00,
      "notes": "Review annually or upon major life changes"
    }
  }
}
```

**FinancialPoaType Enum Values:** `GENERAL`, `LIMITED`, `DURABLE`, `SPRINGING`

---

### 15.2 Philanthropic Profile on Individual

**Endpoint:** `PATCH /api/v1/individual/{id}`

**Description:** Philanthropic giving profile is embedded on the Individual entity. Update it by including the `philanthropicProfile` object in the PATCH body.

**Example Request:**
```json
{
  "philanthropicProfile": {
    "totalAnnualCharitableGiving": 250000.00,
    "givingAsOfYear": 2025,
    "preferredGivingVehicles": "DAF, Direct Gift",
    "charitableIntentNotes": "Focus on education and healthcare initiatives",
    "isMajorDonor": true,
    "hasCharitablePledge": false,
    "totalOutstandingPledges": 100000.00,
    "legacyGivingInterest": true,
    "notes": "Interested in establishing a private foundation"
  }
}
```

---

### 15.3 Charitable Details on Legal Entity

**Endpoint:** `PATCH /api/v1/legal-entity/{id}`

**Description:** Charitable details are embedded on the LegalEntity entity. Only populated for charitable entities (foundations, DAFs, CRTs, etc.). Update it by including the `charitableDetails` object in the PATCH body.

**CharitableVehicleType Enum Values:** Check via LegalEntity API response or codebase

**IrsExemptionStatus Enum Values:** Check via LegalEntity API response or codebase

**Sections:**
- Top-level fields: `charitableVehicleType`, `irsExemptionStatus`, `irsDeterminationDate`, `irsEin`, `missionStatement`, `focusAreas`, `notes`
- `daf`: Donor-Advised Fund specific details (`sponsorName`, `accountNumber`, `currentBalance`, `balanceAsOfDate`)
- `charitableTrust`: CRT/CLT specific details (`payoutRate`, `payoutFrequency`, `remainderBeneficiaryDescription`, `incomeBeneficiaryDescription`, `termDescription`, `termEndDate`, `initialFundingAmount`, `initialFundingDate`)
- `foundation`: Foundation/grantmaking details (`totalEndowment`, `endowmentAsOfDate`, `annualGrantBudget`, `minimumDistributionRequirement`, `hasPaidStaff`, `fiscalYearEnd`, `grantingFrequency`, `totalGrantsYtd`, `totalGrantsLastYear`)

**Example Request (Private Foundation):**
```json
{
  "charitableDetails": {
    "charitableVehicleType": "PRIVATE_FOUNDATION",
    "irsExemptionStatus": "STATUS_501C3",
    "irsDeterminationDate": "2015-03-15",
    "irsEin": "12-3456789",
    "missionStatement": "Supporting education access in underserved communities",
    "focusAreas": "Education, Healthcare",
    "foundation": {
      "totalEndowment": 10000000.00,
      "endowmentAsOfDate": "2025-12-31",
      "annualGrantBudget": 500000.00,
      "minimumDistributionRequirement": 500000.00,
      "hasPaidStaff": true,
      "fiscalYearEnd": "12-31",
      "grantingFrequency": "QUARTERLY",
      "totalGrantsYtd": 150000.00,
      "totalGrantsLastYear": 450000.00
    }
  }
}
```

**Example Request (Donor-Advised Fund):**
```json
{
  "charitableDetails": {
    "charitableVehicleType": "DONOR_ADVISED_FUND",
    "focusAreas": "Arts, Environment",
    "daf": {
      "sponsorName": "Fidelity Charitable",
      "accountNumber": "DAF-123456",
      "currentBalance": 500000.00,
      "balanceAsOfDate": "2025-12-31"
    }
  }
}
```

**Example Request (Charitable Remainder Trust):**
```json
{
  "charitableDetails": {
    "charitableVehicleType": "CHARITABLE_REMAINDER_TRUST",
    "charitableTrust": {
      "payoutRate": 5.0000,
      "payoutFrequency": "QUARTERLY",
      "remainderBeneficiaryDescription": "Smith Family Foundation",
      "incomeBeneficiaryDescription": "John Smith and Jane Smith",
      "termDescription": "20 years",
      "termEndDate": "2045-06-15",
      "initialFundingAmount": 1000000.00,
      "initialFundingDate": "2020-01-15"
    }
  }
}
```

---

### 15.4 Engagement Details on Entity Relationship

**Endpoint:** `POST /api/v1/entity-relationship` or `PATCH /api/v1/entity-relationship/{id}`

**Description:** Engagement details are an optional nested object on entity relationships, used for professional relationships (ADVISOR, ATTORNEY, ACCOUNTANT, etc.) to track fee structure, scope of services, and review history.

**Example Request (Create relationship with engagement details):**
```json
{
  "relationshipType": "ADVISOR",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440001",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "550e8400-e29b-41d4-a716-446655440002",
  "targetEntityType": "CONTACT",
  "isPrimary": true,
  "effectiveFrom": "2024-01-15",
  "engagementDetails": {
    "engagementStatus": "ACTIVE",
    "engagementStartDate": "2024-01-15",
    "feeStructureType": "RETAINER",
    "retainerAmount": 5000.00,
    "retainerFrequency": "MONTHLY",
    "estimatedAnnualCost": 60000.00,
    "scopeOfServices": "Comprehensive wealth management including investment advisory, tax planning, and estate planning coordination",
    "lastReviewDate": "2025-06-15",
    "nextReviewDate": "2026-06-15",
    "satisfactionRating": 4,
    "notes": "Annual review scheduled for Q2"
  }
}
```

**RelationshipEngagementDetailsDto Fields:**
- `engagementStatus`: Enum. Values: `ACTIVE`, `INACTIVE`, `ON_HOLD`, `TERMINATED`
- `engagementStartDate`: Date
- `engagementEndDate`: Date
- `feeStructureType`: Enum. Values: `HOURLY`, `RETAINER`, `FLAT_FEE`, `AUM_BASED`, `CONTINGENCY`, `PRO_BONO`
- `hourlyRate`: BigDecimal
- `retainerAmount`: BigDecimal
- `retainerFrequency`: Enum. Values: `MONTHLY`, `QUARTERLY`, `ANNUAL`
- `flatFeeAmount`: BigDecimal
- `aumBasisPoints`: Integer (100 = 1%)
- `estimatedAnnualCost`: BigDecimal
- `scopeOfServices`: String
- `engagementLetterDocumentId`: UUID
- `lastReviewDate`: Date
- `nextReviewDate`: Date
- `satisfactionRating`: Integer (1-5)
- `notes`: String

---

## 16. INSURANCE POLICY OWNERSHIP RELATIONSHIPS

Insurance policies are linked to people via entity relationships. Three relationship types are used:
- **OWNERSHIP**: Who owns the policy (pays premiums, has rights to cash value)
- **INSURED**: Who is insured under the policy (whose life/health is covered)
- **BENEFICIARY**: Who receives benefits upon claim/death

All use `POST /api/v1/entity-relationship` with `targetEntityType: "INSURANCE_POLICY"`.

### 16.1 Create OWNERSHIP Relationship (Policy Owner)
```json
{
  "relationshipType": "OWNERSHIP",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440001",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "550e8400-e29b-41d4-a716-446655440099",
  "targetEntityType": "INSURANCE_POLICY",
  "percentage": 100.00,
  "isPrimary": true,
  "effectiveFrom": "2020-01-01"
}
```

**Notes:**
- `sourceEntityType` can be `INDIVIDUAL` or `LEGAL_ENTITY` (for COLI, ILIT-owned, etc.)
- `percentage` is required for OWNERSHIP relationships
- For joint ownership, create multiple relationships with appropriate percentages

### 16.2 Create INSURED Relationship (Insured Person)
```json
{
  "relationshipType": "INSURED",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440001",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "550e8400-e29b-41d4-a716-446655440099",
  "targetEntityType": "INSURANCE_POLICY",
  "isPrimary": true,
  "effectiveFrom": "2020-01-01"
}
```

**Notes:**
- The source is the insured person, the target is the policy
- For second-to-die policies, create two INSURED relationships (one per insured)

### 16.3 Create BENEFICIARY Relationship (Policy Beneficiary)
```json
{
  "relationshipType": "BENEFICIARY",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440002",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "550e8400-e29b-41d4-a716-446655440099",
  "targetEntityType": "INSURANCE_POLICY",
  "percentage": 50.00,
  "role": "Primary Beneficiary",
  "effectiveFrom": "2020-01-01"
}
```

**Notes:**
- `sourceEntityType` can be `INDIVIDUAL`, `LEGAL_ENTITY` (for trusts as beneficiaries), or `HOUSEHOLD`
- `percentage` represents the beneficiary's share of the benefit
- `role` can be "Primary Beneficiary", "Contingent Beneficiary", etc.
- Multiple beneficiary relationships can be created with percentages that should total 100%

### 16.4 Common Insurance Policy Relationship Pattern

For a typical life insurance policy, create all three relationships:

1. **Owner** (who pays premiums and controls the policy):
```json
{ "relationshipType": "OWNERSHIP", "sourceEntityType": "INDIVIDUAL", "sourceEntityId": "{owner_id}", "targetEntityType": "INSURANCE_POLICY", "targetEntityId": "{policy_id}", "percentage": 100.00, "isPrimary": true }
```

2. **Insured** (whose life is covered):
```json
{ "relationshipType": "INSURED", "sourceEntityType": "INDIVIDUAL", "sourceEntityId": "{insured_id}", "targetEntityType": "INSURANCE_POLICY", "targetEntityId": "{policy_id}", "isPrimary": true }
```

3. **Beneficiary/Beneficiaries**:
```json
{ "relationshipType": "BENEFICIARY", "sourceEntityType": "INDIVIDUAL", "sourceEntityId": "{beneficiary1_id}", "targetEntityType": "INSURANCE_POLICY", "targetEntityId": "{policy_id}", "percentage": 50.00, "role": "Primary Beneficiary" }
```
```json
{ "relationshipType": "BENEFICIARY", "sourceEntityType": "INDIVIDUAL", "sourceEntityId": "{beneficiary2_id}", "targetEntityType": "INSURANCE_POLICY", "targetEntityId": "{policy_id}", "percentage": 50.00, "role": "Primary Beneficiary" }
```

---

## 17. LIABILITY OWNERSHIP RELATIONSHIPS

Liabilities are linked to owners via entity relationships using only the OWNERSHIP relationship type.

All use `POST /api/v1/entity-relationship` with `targetEntityType: "LIABILITY"`.

### 17.1 Create OWNERSHIP Relationship (Liability Owner)
```json
{
  "relationshipType": "OWNERSHIP",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440001",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "550e8400-e29b-41d4-a716-446655440088",
  "targetEntityType": "LIABILITY",
  "percentage": 100.00,
  "isPrimary": true,
  "effectiveFrom": "2022-06-15"
}
```

**Notes:**
- `sourceEntityType` can be `INDIVIDUAL` or `LEGAL_ENTITY`
- `percentage` is required for OWNERSHIP relationships
- For joint liabilities (e.g., joint mortgage), create multiple OWNERSHIP relationships:

```json
{
  "relationshipType": "OWNERSHIP",
  "sourceEntityId": "{spouse1_id}",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "{mortgage_id}",
  "targetEntityType": "LIABILITY",
  "percentage": 50.00,
  "isPrimary": true,
  "effectiveFrom": "2022-06-15"
}
```
```json
{
  "relationshipType": "OWNERSHIP",
  "sourceEntityId": "{spouse2_id}",
  "sourceEntityType": "INDIVIDUAL",
  "targetEntityId": "{mortgage_id}",
  "targetEntityType": "LIABILITY",
  "percentage": 50.00,
  "isPrimary": false,
  "effectiveFrom": "2022-06-15"
}
```

---

## 18. RUNTIME ENUM DISCOVERY ENDPOINTS

These endpoints return the valid enum values at runtime with display names and descriptions. Use these instead of hardcoding enum values -- the server is the source of truth.

**Response format for all enum endpoints:**
```json
[
  {
    "value": "MORTGAGE",
    "displayName": "Mortgage",
    "description": "Loan secured by real property (home, investment property)"
  }
]
```

### 18.1 Insurance Policy Enums

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/insurance-policy/enums/categories` | Policy categories (LIFE, UMBRELLA, LONG_TERM_CARE, DISABILITY, HEALTH, AUTO, OTHER) |
| `GET /api/v1/insurance-policy/enums/statuses` | Policy statuses (ACTIVE, LAPSED, CANCELLED, PAID_UP, SURRENDERED, MATURED, PENDING) |
| `GET /api/v1/insurance-policy/enums/life-policy-types` | Life policy subtypes (TERM, WHOLE_LIFE, UNIVERSAL, etc.) |
| `GET /api/v1/insurance-policy/enums/inflation-protection-types` | LTC inflation protection types |
| `GET /api/v1/insurance-policy/enums/dividend-options` | Whole life dividend options |
| `GET /api/v1/insurance-policy/enums/document-types` | Insurance policy document sub-types (27 values, 8 categories) |

### 18.2 Liability Enums

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/liability/enums/types` | Liability types (MORTGAGE, HOME_EQUITY_LOC, STUDENT_LOAN, etc.) |
| `GET /api/v1/liability/enums/statuses` | Liability statuses (CURRENT, DELINQUENT, IN_DEFERMENT, etc.) |
| `GET /api/v1/liability/enums/document-types` | Liability document sub-types (13 values, 5 categories) |

### 18.3 Account Financial Enums

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/account-financial/enums/categories` | Account categories (e.g., INVESTMENT, BANKING, RETIREMENT, etc.) |
| `GET /api/v1/account-financial/enums/subcategories?category={category}` | Subcategories filtered by parent category |
| `GET /api/v1/account-financial/enums/subcategories/all` | All subcategories across all categories |

### 18.4 Entity Relationship Enums

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/entity-relationship/entity-types` | Valid entity types for relationships (INDIVIDUAL, LEGAL_ENTITY, HOUSEHOLD, etc.) |
| `GET /api/v1/entity-relationship/relationship-types` | Valid relationship types (OWNERSHIP, MEMBER, TRUSTEE, BENEFICIARY, etc.) |
