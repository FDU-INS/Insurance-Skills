# Altcore API Schema Reference

**Updated:** 2026-04-17
**API Version:** 1.0.0
**Production URL:** https://api.m62.live
**Development URL:** http://localhost:8080

> **Full OpenAPI spec:** For schemas not covered here, search the full spec at
> `api-docs/api.json` (relative to this skill's directory). Use Glob to find it:
> `Glob pattern "**/m62-altitude-onboarding/**/api.json"`

---

## Authentication

### JWT Token Authentication

**Endpoint:** `POST /api/v1/authenticate`

```bash
POST /api/v1/authenticate
Content-Type: application/json

{
  "username": "admin",
  "password": "admin",
  "rememberMe": false
}
```

**Response:**
```json
{
  "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Usage:**
```bash
Authorization: Bearer {id_token}
```

### API Key Authentication (Recommended)

Include as a header on any `/api/v1/` endpoint:

```bash
X-API-Key: ak_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Default Users (Development)

| Username | Password | Roles |
|----------|----------|-------|
| `admin` | `admin` | ROLE_ADMIN, ROLE_ADMIN_TENANT, ROLE_USER |
| `verita.admin` | `demo123` | Firm admin for Verita demo firm |
| `wellington.admin` | `demo123` | Firm admin for Wellington demo firm |

---

## Entity Schemas

### IndividualDto

**Description:** Individual person entity for wealth management (owner, beneficiary, contact, advisor).

**Required Fields:** `firstName`, `lastName`

**Writable Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `salutation` | String | No | Title (Mr., Ms., Dr., etc.) |
| `firstName` | String | Yes | First name |
| `middleName` | String | No | Middle name |
| `lastName` | String | Yes | Last name |
| `suffix` | String | No | Suffix (Jr., Sr., III, etc.) |
| `dateOfBirth` | LocalDate | No | YYYY-MM-DD |
| `dateOfDeath` | LocalDate | No | YYYY-MM-DD |
| `ssn` | String | No | 9-digit SSN (stored encrypted) |
| `taxId` | String | No | Alternative tax ID when SSN not available |
| `taxIdType` | Enum | No | SSN, ITIN, EIN, FOREIGN_TIN, FOREIGN_ENTITY_TIN, VAT, GST, BUSINESS_NUMBER |
| `taxIdIssuingCountry` | String | No | ISO 3166-1 alpha-2 country code |
| `gender` | String | No | Gender value (no Java enum found -- may be a free-text String field; commonly MALE, FEMALE, OTHER) |
| `maritalStatus` | String | No | Marital status (no Java enum found -- may be a free-text String field; commonly SINGLE, MARRIED, DIVORCED, WIDOWED, DOMESTIC_PARTNERSHIP) |
| `citizenship` | String | No | ISO 3166-1 alpha-2 country code |
| `residency` | Enum | No | US_RESIDENT, FOREIGN_NATIONAL, GREEN_CARD_HOLDER, DUAL_RESIDENT |
| `lifecycleStatus` | Enum | No | DRAFT, PENDING_VERIFICATION, ACTIVE, INACTIVE, ARCHIVED |
| `email` | String | No | Primary email address |
| `phoneNumberPrimary` | String | No | Primary phone (E.164 format) |
| `phoneNumberSecondary` | String | No | Secondary phone (E.164 format) |
| `faxNumber` | String | No | Fax number |
| `occupation` | String | No | Job occupation |
| `employerName` | String | No | Current employer |
| `jobTitle` | String | No | Job title at employer |
| `employmentPositionOrRole` | String | No | Detailed position/role |
| `addressLegal` | AddressDto | No | Legal/residential address |
| `addressMailing` | AddressDto | No | Mailing address (if different) |
| `addressEmployer` | AddressDto | No | Employer address |
| `financialProfile` | IndividualFinancialProfileDto | No | Net worth, income, risk profile |
| `taxStatus` | TaxStatusDto | No | Tax classification, exemptions |
| `regulatoryStatus` | RegulatoryStatusDto | No | Accreditation, qualified status |
| `isPoliticallyExposedPerson` | Boolean | No | PEP status for AML/KYC |
| `registeredWithFinra` | Boolean | No | FINRA registration status |
| `finraCrdNumber` | String | No | CRD number if FINRA registered |
| `transferOnDeath` | TransferOnDeathDto | No | Beneficiary designations |
| `biography` | String | No | Notes/biography |
| `strategyId` | UUID | No | Linked investment strategy |
| `preferences` | Map<String, String> | No | User preferences (key-value) |
| `tags` | List<String> | No | Categorical tags |

**Nested Objects:**

**AddressDto:**
```json
{
  "addressLine1": "123 Main St",
  "addressLine2": "Suite 100",
  "city": "New York",
  "state": "NY",
  "postalCode": "10001",
  "country": "US",
  "addressType": "PRIMARY"
}
```

**IndividualFinancialProfileDto:**
```json
{
  "netWorth": 5000000.00,
  "netWorthLiquid": 1000000.00,
  "annualIncome": 250000.00,
  "investorSourceOfFunds": "SALE_OF_BUSINESS",
  "riskTolerance": "MODERATE",
  "timeHorizon": "LONG_TERM"
}
```

**TaxStatusDto:**
```json
{
  "taxStatus": "RESIDENT",
  "classification": "INDIVIDUAL",
  "exemptionBasis": "NONE",
  "backUpWithholding": false
}
```

**RegulatoryStatusDto:**
```json
{
  "accredited": true,
  "qualifiedClient": true,
  "qualifiedPurchaser": false
}
```

---

### LegalEntityDto

**Description:** Legal entity (corporation, LLC, trust, partnership, etc.) for business ownership.

**Required Fields:** `legalName`, `entityType`

**Writable Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `legalName` | String | Yes | Registered legal name |
| `dbaName` | String | No | Doing Business As name |
| `entityType` | Enum | Yes | CORPORATION, LLC, TRUST, PARTNERSHIP, LIMITED_PARTNERSHIP, LLP, FOUNDATION, ESTATE, SOLE_PROPRIETORSHIP, NON_PROFIT, GOVERNMENT_ENTITY, OTHER |
| `taxId` | String | No | EIN or equivalent |
| `jurisdiction` | String | No | State/country of formation |
| `incorporationState` | String | No | State of incorporation |
| `incorporationCountry` | String | No | Country of incorporation |
| `formationDate` | LocalDate | No | YYYY-MM-DD |
| `registrationNumber` | String | No | Secretary of State registration |
| `email` | String | No | Entity email |
| `phone` | String | No | Entity phone (E.164 format) |
| `addressPrincipal` | AddressDto | No | Principal place of business |
| `addressMailing` | AddressDto | No | Mailing address |
| `taxClassification` | Enum | No | SOLE_PROPRIETORSHIP, PARTNERSHIP, S_CORP, C_CORP, TRUST_ESTATE, LLC, DISREGARDED, COOPERATIVE, TAX_EXEMPT_ORG, FOREIGN |
| `fiscalYearEnd` | String | No | Month/day (MM-DD) |
| `nominee` | Boolean | No | Entity holds assets in nominee capacity |
| `taxStatus` | TaxStatusDto | No | Tax status details |
| `complianceTracking` | ComplianceTrackingDto | No | KYC/AML status |
| `regulatoryStatus` | RegulatoryStatusDto | No | Regulatory eligibility |
| `tags` | List<String> | No | Categorical tags |
| **LLC-Specific Fields** | | | |
| `llcManagementType` | Enum | No | MEMBER_MANAGED, MANAGER_MANAGED |
| `llcOperatingAgreementDate` | LocalDate | No | Operating agreement execution date |
| `llcAnnualFilingDueDate` | LocalDate | No | Next annual report due date |
| `llcLastAnnualFilingDate` | LocalDate | No | Last annual report filing date |
| **Corporation-Specific Fields** | | | |
| `corpAuthorizedShares` | Long | No | Authorized shares outstanding |
| `corpIssuedShares` | Long | No | Issued shares outstanding |
| **Trust-Specific Fields (when entityType=TRUST)** | | | |
| `isRevocable` | Boolean | No | Revocable vs. irrevocable trust |
| `isGrantor` | Boolean | No | Grantor retained control |
| `situs` | String | No | Trust situs/jurisdiction |
| `governingLaw` | String | No | Governing law jurisdiction |
| `grantorNamesExtracted` | String | No | Grantor names (comma-separated) |
| `trusteeNamesExtracted` | String | No | Trustee names (comma-separated) |
| `beneficiaryNamesExtracted` | String | No | Beneficiary names (comma-separated) |
| `successorTrusteeNamesExtracted` | String | No | Successor trustee names |
| `distributionProvisionsText` | String | No | Distribution rules and conditions |
| `powersOfTrusteeText` | String | No | Trustee powers and limitations |
| `terminationProvisionsText` | String | No | Trust termination conditions |
| `hasSpendthriftProvision` | Boolean | No | Includes spendthrift protection |
| `spendthriftProvisionText` | String | No | Spendthrift clause details |
| `hasPourOverProvision` | Boolean | No | Pour-over will provision |
| `pourOverTrustName` | String | No | Pour-over trust name |
| `pourOverTrustId` | UUID | No | Pour-over trust ID reference |
| `trustAliases` | List<String> | No | Alternative trust names |
| `trustPurpose` | String | No | Trust purpose statement |
| `initialFunding` | BigDecimal | No | Initial trust funding amount |
| `crummeyPowerHolders` | List<String> | No | Beneficiaries with Crummey powers |
| `trustProtector` | String | No | Trust protector name |
| `investmentAdvisor` | String | No | Investment advisor name |
| `distributionAdvisor` | String | No | Distribution advisor name |
| `gstExemptionStatus` | Enum | No | EXEMPT, NON_EXEMPT, ALLOCATION_PENDING |
| `perpetuitiesPeriod` | String | No | Generation-skipping tax period |
| `amendmentNumber` | Integer | No | Amendment number if amended |
| `lastAmendmentDate` | LocalDate | No | Date of last amendment |
| `isRestatement` | Boolean | No | Full restatement vs. amendment |
| `restatementDate` | LocalDate | No | Restatement date if applicable |

**Nested Objects:** See Individual for AddressDto, ComplianceTrackingDto, RegulatoryStatusDto, TaxStatusDto

---

### HouseholdDto

**Description:** Family/household grouping for net worth aggregation and reporting.

**Required Fields:** `name`

**Writable Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Household name (e.g., "Smith Family") |
| `description` | String | No | Description/notes |
| `billing` | HouseholdBillingDto | No | Billing contact and settings |

**Nested Objects:**

**HouseholdBillingDto:**
```json
{
  "billingContact": {
    "firstName": "John",
    "lastName": "Smith",
    "email": "billing@example.com",
    "phoneNumber": "+1-555-0100"
  },
  "billingAddress": {
    "addressLine1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "postalCode": "10001",
    "country": "US"
  },
  "billingFrequency": "QUARTERLY",
  "invoiceDeliveryMethod": "EMAIL"
}
```

---

### AccountFinancialDto

**Description:** Investment account (brokerage, retirement, etc.) holding securities and cash.

**Required Fields:** `name`, `accountCategory`, `subCategory`, `currencyCode`

**Writable Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Account name (e.g., "John's IRA") |
| `displayName` | String | No | Display name for UI |
| `accountNumber` | String | No | Account number at custodian |
| `accountCategory` | Enum | Yes | INDIVIDUAL, ENTITY |
| `subCategory` | Enum | Yes | INDIVIDUAL, JOINT_WITH_RIGHTS_OF_SURVIVORSHIP, JOINT_TENANTS_IN_COMMON, COMMUNITY_PROPERTY, UNIFORM_GIFT_OR_TRANSFER_TO_MINOR, OTHER_INDIVIDUAL, IRA, ROTH_IRA, SEP_IRA, SIMPLE_IRA, PENSION_401K, ROLLOVER_IRA, INHERITED_IRA, KEOGH_PLAN, PENSION_OR_PROFIT_SHARING_PLAN, SELF_DIRECTED_RETIREMENT_ACCOUNT, TRUST_INDIVIDUAL, GRANTOR_TRUST, REVOCABLE_TRUST, IRREVOCABLE_TRUST, SIMPLE_TRUST, COMPLEX_TRUST, CHARITABLE_TRUST, REMAINDER_TRUST, JOINT_TRUST, CORPORATION, C_CORP, S_CORP, PARTNERSHIP, LIMITED_PARTNERSHIP, LIMITED_LIABILITY_COMPANY, FUND_OF_FUNDS, JOINT_TENANTS_IN_COMMON_ENTITIES, JOINT_RIGHTS_OF_SURVIVORSHIP_ENTITIES, PRIVATE_FOUNDATION, ENDOWMENT, BENEFIT_PLAN, OTHER_TAX_EXEMPT_ORGANIZATION, ESTATE, OTHER_NON_INDIVIDUAL |
| `wrapper` | Enum | No | IRA, 401K, 529, UGMA, UTMA, etc. |
| `taxStatus` | Enum | No | TAXABLE, TAX_DEFERRED, TAX_FREE |
| `currencyCode` | String | Yes | ISO 4217 currency code (default: USD) |
| `onlineStatus` | Enum | No | ACTIVE, CLOSED, ON_HOLD, PENDING (default: ACTIVE) |
| `custodianId` | UUID | No | Custodian entity reference |
| `custodianAccountNumber` | String | No | Account number at custodian |
| `otherInstitutionName` | String | No | Non-custodian institution name |
| `otherInstitutionType` | String | No | Institution type classification |
| `strategyId` | UUID | No | Linked investment strategy |
| `relationshipManagerId` | UUID | No | RM responsible for account |
| `ownershipType` | Enum | No | PERCENT_BASED, EQUAL_SPLIT |
| `isRolledUp` | Boolean | No | Include in household rollup |
| `billing` | AccountBillingDto | No | Fee and billing details |
| `investmentProfile` | InvestmentProfileDto | No | Risk, objectives, constraints |
| `retirementDetails` | RetirementDetailsDto | No | Retirement-specific info |
| `tags` | List<String> | No | Categorical tags |

**Nested Objects:**

**AccountBillingDto:**
```json
{
  "feeScheduleId": "uuid",
  "billingMethod": "PERCENT_AUM",
  "feePercentage": 0.50,
  "minimumAnnualFee": 1000.00,
  "currency": "USD"
}
```

**InvestmentProfileDto:**
```json
{
  "riskTolerance": "MODERATE",
  "investmentObjectives": ["GROWTH", "INCOME"],
  "timeHorizon": "LONG_TERM",
  "constraints": ["NO_ALTERNATIVES"]
}
```

**RetirementDetailsDto:**
```json
{
  "beneficiaryDesignation": "SPOUSE_PRIMARY",
  "rolloverSource": "401K",
  "rolloverDate": "2024-01-15",
  "requiredMinimumDistribution": 50000.00
}
```

---

### ContactDto

**Description:** Contact person (not necessarily an investor).

**Required Fields:** `firstName`, `lastName`

**Writable Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `salutation` | String | No | Title (Mr., Ms., Dr., etc.) |
| `firstName` | String | Yes | First name |
| `middleInitial` | String | No | Middle initial |
| `lastName` | String | Yes | Last name |
| `suffix` | String | No | Suffix (Jr., Sr., III, etc.) |
| `dateOfBirth` | LocalDate | No | YYYY-MM-DD |
| `email` | String | No | Email address |
| `phoneNumberPrimary` | String | No | Primary phone (E.164 format) |
| `phoneNumberSecondary` | String | No | Secondary phone (E.164 format) |
| `faxNumber` | String | No | Fax number |
| `jobTitle` | String | No | Job title |
| `biography` | String | No | Notes/biography |
| `addressLegal` | AddressDto | No | Legal/residential address |
| `addressMailing` | AddressDto | No | Mailing address |

**Read-Only Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `fullName` | String | Computed full name (read-only) |

**Note:** ContactDto does NOT have `companyName`, `organization`, or `department` fields.

---

### TangibleAssetDto

**Description:** Non-financial physical assets (real estate, vehicles, collectibles, jewelry, art).

**Required Fields:** `name`

**Writable Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Asset name (e.g., "2024 Tesla Model S") |
| `description` | String | No | Detailed description |
| `category` | Enum | No | VEHICLE, REAL_PROPERTY, LUXURY, COLLECTIBLE, OTHER |
| `assetType` | Enum | No | CAR, MOTORCYCLE, BOAT, YACHT, AIRCRAFT, HELICOPTER, RV, PRIMARY_RESIDENCE, VACATION_HOME, RENTAL_PROPERTY, COMMERCIAL_PROPERTY, LAND, FARM_RANCH, TIMESHARE, WATCH, JEWELRY, HANDBAG, FASHION, LUXURY_OTHER, ART, WINE, ANTIQUE, MEMORABILIA, COINS, STAMPS, BOOKS, MUSICAL_INSTRUMENT, COLLECTIBLE_OTHER, EQUIPMENT, LIVESTOCK, FURNITURE, OTHER_TYPE |
| `status` | Enum | No | ACTIVE, SOLD, TRANSFERRED, DONATED, DISPOSED, STOLEN, LOST |
| `serialOrIdentifier` | String | No | VIN, Serial number, etc. |
| `currentValue` | BigDecimal | No | Current estimated value |
| `valuationDate` | LocalDate | No | Date of valuation |
| `valuationSource` | String | No | Source of valuation (appraiser, market, owner) |
| `currencyCode` | String | No | ISO 4217 currency code (default: USD) |
| `purchasePrice` | BigDecimal | No | Original purchase price |
| `purchaseDate` | LocalDate | No | Date of purchase |
| `acquisitionType` | Enum | No | PURCHASE, AUCTION, GIFT, INHERITANCE, COMMISSION, EXCHANGE, PRIZE |
| `taxBasis` | BigDecimal | No | Tax cost basis |
| `taxBasisDate` | LocalDate | No | Tax basis determination date |
| `sellerName` | String | No | Name of seller |
| `purchaseVenue` | String | No | Location or method of purchase |
| `location` | String | No | Current physical location |
| `storageFacility` | String | No | Safe deposit box, vault, etc. |
| `custodianName` | String | No | Custodian holding asset |
| `custodianContact` | String | No | Custodian contact info |
| `isInsured` | Boolean | No | Asset has insurance |
| `primaryInsurancePolicyNumber` | String | No | Insurance policy number |
| `insuredValue` | BigDecimal | No | Insurance coverage amount |
| `insuranceExpirationDate` | LocalDate | No | Insurance expiration date |
| `disposalDate` | LocalDate | No | Date asset was disposed |
| `disposalPrice` | BigDecimal | No | Sale/disposal price |
| `disposalMethod` | String | No | Sale, donation, destruction, etc. |
| `disposalNotes` | String | No | Notes on disposal |
| `buyerName` | String | No | Buyer name in disposal |
| `includedInEstate` | Boolean | No | Asset included in estate |
| `estateDisposition` | String | No | Estate distribution plan |
| `designatedBeneficiaryId` | UUID | No | Designated beneficiary |
| `estateNotes` | String | No | Estate-related notes |
| `vehicleDetails` | VehicleDetailsDto | No | Vehicle-specific info |
| `realPropertyDetails` | RealPropertyDetailsDto | No | Real property-specific info |
| `luxuryDetails` | LuxuryDetailsDto | No | Luxury item-specific info |
| `collectibleDetails` | CollectibleDetailsDto | No | Collectible-specific info |
| `notes` | String | No | General notes |
| `tags` | List<String> | No | Categorical tags |

**Nested Objects:**

**VehicleDetailsDto:**
```json
{
  "year": 2024,
  "make": "Tesla",
  "model": "Model S",
  "vin": "5TDJKRFH0LS123456",
  "mileage": 15000,
  "color": "Pearl White",
  "fuelType": "ELECTRIC"
}
```

**RealPropertyDetailsDto:**
```json
{
  "address": "123 Main St, New York, NY 10001",
  "propertyType": "SINGLE_FAMILY_HOME",
  "squareFootage": 3500,
  "yearBuilt": 1995,
  "lotSize": 0.5,
  "bedrooms": 4,
  "bathrooms": 3.5,
  "garage": "3-CAR"
}
```

**LuxuryDetailsDto:**
```json
{
  "brand": "Hermès",
  "model": "Birkin",
  "itemType": "HANDBAG",
  "colorDescription": "Black leather",
  "authentication": "CERTIFICATE_OF_AUTHENTICITY"
}
```

**CollectibleDetailsDto:**
```json
{
  "artist": "Pablo Picasso",
  "title": "Guernica",
  "medium": "Oil on canvas",
  "yearCreated": 1937,
  "condition": "EXCELLENT",
  "provenance": "Reina Sofía Museum acquisition chain"
}
```

---

### InsurancePolicyDto

**Description:** Insurance policy entity supporting multiple subtypes (life, umbrella, LTC, disability, health, auto, other). Uses a flat DTO structure where subtype-specific fields are present but null when not applicable. The `policyCategory` field determines which subtype fields are relevant.

**Required Fields:** `policyCategory`, `name`, `policyStatus`

**Endpoint:** `/api/v1/insurance-policy`

**Writable Fields (Base -- all categories):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `policyCategory` | Enum | Yes | LIFE, UMBRELLA, LONG_TERM_CARE, DISABILITY, HEALTH, AUTO, OTHER |
| `name` | String | Yes | Display name (max 200) |
| `policyNumber` | String | No | Policy number from carrier (max 100) |
| `carrierName` | String | No | Insurance carrier name (max 200) |
| `policyStatus` | Enum | Yes | ACTIVE, LAPSED, CANCELLED, PAID_UP, SURRENDERED, MATURED, PENDING |
| `coverageAmount` | BigDecimal | No | Total coverage amount (face value) |
| `annualPremium` | BigDecimal | No | Annual premium amount |
| `paymentFrequency` | Enum | No | MONTHLY, BI_WEEKLY, QUARTERLY, ANNUAL, INTEREST_ONLY |
| `effectiveDate` | LocalDate | No | Coverage effective date |
| `expirationDate` | LocalDate | No | Policy expiration/renewal date |
| `applicationDate` | LocalDate | No | Application submission date |
| `issueDate` | LocalDate | No | Date policy was issued |
| `description` | String | No | Policy description (max 4000) |
| `deductible` | BigDecimal | No | Deductible amount |
**Read-Only Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `owners` | List&lt;OwnershipInfoDto&gt; | Lightweight list of owners (individuals, households, or legal entities that own this policy via OWNERSHIP relationships). Each entry has: `ownerId` (UUID), `ownerName` (String), `ownerType` (HOUSEHOLD, INDIVIDUAL, or LEGAL_ENTITY), `ownershipPercentage` (BigDecimal), `role` (String), `isPrimary` (Boolean). |

**Life Insurance Fields (policyCategory = LIFE):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `lifePolicyType` | Enum | Yes* | TERM, WHOLE_LIFE, UNIVERSAL, VARIABLE_UNIVERSAL, INDEXED_UNIVERSAL, SURVIVORSHIP, GROUP_TERM |
| `deathBenefit` | BigDecimal | No | Death benefit amount |
| `cashValue` | BigDecimal | No | Current cash value (permanent policies) |
| `cashValueAsOfDate` | LocalDate | No | Cash value as-of date |
| `loanBalance` | BigDecimal | No | Outstanding policy loan balance |
| `termLengthYears` | Integer | No | Term length in years (term policies) |
| `termExpirationDate` | LocalDate | No | Term expiration date |
| `isConvertible` | Boolean | No | Whether term policy is convertible |
| `conversionDeadline` | LocalDate | No | Conversion option deadline |
| `isIlitOwned` | Boolean | No | Whether ILIT-owned (estate planning) |
| `ilitLegalEntityId` | UUID | No | ILIT legal entity reference |
| `isSecondToDie` | Boolean | No | Survivorship/second-to-die policy |
| `secondInsuredIndividualId` | UUID | No | Second insured individual ref |
| `guaranteedDeathBenefit` | Boolean | No | Whether death benefit is guaranteed |
| `riders` | String | No | Policy riders (free-text) |
| `surrenderChargeSchedule` | String | No | Surrender charge schedule |
| `dividendOption` | Enum | No | CASH, PREMIUM_REDUCTION, ACCUMULATE_AT_INTEREST, PAID_UP_ADDITIONS, ONE_YEAR_TERM |

**Umbrella Insurance Fields (policyCategory = UMBRELLA):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `excessLiabilityCoverage` | BigDecimal | No | Excess liability coverage amount |
| `underlyingAutoRequired` | BigDecimal | No | Required underlying auto liability limit |
| `underlyingHomeRequired` | BigDecimal | No | Required underlying homeowners limit |
| `underlyingPoliciesDescription` | String | No | Description of underlying policies |
| `coversRentalProperties` | Boolean | No | Whether rental properties are covered |
| `coversWatercraft` | Boolean | No | Whether watercraft is covered |
| `uninsuredMotorist` | Boolean | No | Whether uninsured motorist is included |

**Long-Term Care Fields (policyCategory = LONG_TERM_CARE):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dailyBenefitAmount` | BigDecimal | No | Maximum daily benefit |
| `benefitPeriodDescription` | String | No | Benefit period (e.g., "3 Years") |
| `benefitPeriodMonths` | Integer | No | Benefit period in months |
| `eliminationPeriodDays` | Integer | No | Elimination/waiting period in days |
| `inflationProtectionType` | Enum | No | NONE, SIMPLE, COMPOUND_3_PERCENT, COMPOUND_5_PERCENT, CPI_LINKED, FUTURE_PURCHASE_OPTION |
| `coversHomeCare` | Boolean | No | Whether home care is covered |
| `coversAssistedLiving` | Boolean | No | Whether assisted living is covered |
| `coversNursingFacility` | Boolean | No | Whether nursing facility is covered |
| `coversAdultDayCare` | Boolean | No | Whether adult day care is covered |
| `sharedBenefitRider` | Boolean | No | Whether shared benefit rider is included |
| `isPartnershipQualified` | Boolean | No | Whether Partnership-qualified (Medicaid) |
| `remainingBenefitPool` | BigDecimal | No | Remaining benefit pool dollars |

**Disability Fields (policyCategory = DISABILITY):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `monthlyBenefitAmount` | BigDecimal | No | Monthly benefit amount |
| `benefitPeriodDescription` | String | No | Benefit period (e.g., "To Age 65") |
| `eliminationPeriodDays` | Integer | No | Elimination/waiting period in days |
| `isOwnOccupation` | Boolean | No | Whether own-occupation coverage |
| `ownOccupationPeriodDescription` | String | No | Own-occ period before transitioning |
| `costOfLivingAdjustment` | Boolean | No | Whether COLA rider is included |
| `futureIncreaseOption` | Boolean | No | Whether future increase option available |
| `residualDisabilityRider` | Boolean | No | Whether residual disability rider included |
| `isGroupPolicy` | Boolean | No | Whether employer-provided group policy |
| `isTaxableBenefit` | Boolean | No | Whether benefits are taxable |

**Note:** `benefitPeriodDescription` and `eliminationPeriodDays` are shared between LTC and DISABILITY subtypes in the flat DTO.

**Ownership:** Linked to Individual or LegalEntity owners via EntityRelationship with `targetEntityType: INSURANCE_POLICY`. Owners are embedded in the response as the read-only `owners` field. Additional relationships: INSURED (person covered), BENEFICIARY (person who receives benefit). Notes are managed via `/{id}/notes` sub-resource (not a flat field). Documents are managed via `/{id}/document` sub-resource.

---

### LiabilityDto

**Description:** Standalone debt obligation (mortgage, loan, credit line, etc.) owned by an Individual or LegalEntity. Reduces net worth: Net Worth = Total Assets - Total Liabilities.

**Required Fields:** `name`, `liabilityType`, `liabilityStatus`

**Endpoint:** `/api/v1/liability`

**Writable Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Display name (max 200) |
| `liabilityType` | Enum | Yes | MORTGAGE, HOME_EQUITY_LOC, STUDENT_LOAN, PERSONAL_LOAN, CREDIT_LINE, MARGIN_LOAN, AUTO_LOAN, BUSINESS_LOAN, CREDIT_CARD, PLEDGED_ASSET_LINE, OTHER |
| `liabilityStatus` | Enum | Yes | CURRENT, DELINQUENT, IN_DEFERMENT, IN_FORBEARANCE, PAID_OFF, DEFAULTED, CHARGED_OFF |
| `lenderName` | String | No | Lending institution name (max 200) |
| `accountNumber` | String | No | Account/loan number (max 100) |
| `originalBalance` | BigDecimal | No | Original principal at origination |
| `currentBalance` | BigDecimal | No | Current outstanding balance |
| `balanceAsOfDate` | LocalDate | No | Date balance was last verified |
| `creditLimit` | BigDecimal | No | Credit limit (revolving credit) |
| `availableCredit` | BigDecimal | No | Available credit remaining |
| `interestRate` | BigDecimal | No | Annual interest rate as percentage |
| `interestRateType` | Enum | No | FIXED, VARIABLE, HYBRID |
| `indexRateDescription` | String | No | Index rate for variable loans (max 100) |
| `rateCap` | BigDecimal | No | Maximum interest rate cap |
| `rateFloor` | BigDecimal | No | Minimum interest rate floor |
| `monthlyPayment` | BigDecimal | No | Monthly payment amount |
| `minimumPayment` | BigDecimal | No | Minimum payment (revolving credit) |
| `paymentFrequency` | Enum | No | MONTHLY, BI_WEEKLY, QUARTERLY, ANNUAL, INTEREST_ONLY |
| `nextPaymentDate` | LocalDate | No | Next payment due date |
| `originationDate` | LocalDate | No | Loan origination date |
| `maturityDate` | LocalDate | No | Maturity or renewal date |
| `isSecured` | Boolean | No | Whether secured by collateral (default: false) |
| `collateralDescription` | String | No | Collateral description (max 500) |
| `linkedTangibleAssetId` | String | No | UUID of tangible asset as collateral |
| `linkedAccountFinancialId` | String | No | UUID of linked financial account |
| `isInterestDeductible` | Boolean | No | Whether interest is tax-deductible |
| `interestDeductionType` | Enum | No | MORTGAGE_INTEREST, INVESTMENT_INTEREST, STUDENT_LOAN_INTEREST, BUSINESS_INTEREST, NONE |
| `interestPaidYtd` | BigDecimal | No | Interest paid year-to-date |
| `interestPaidPriorYear` | BigDecimal | No | Interest paid prior year |
| `description` | String | No | Detailed description (max 4000) |

**Ownership:** Linked to Individual or LegalEntity owners via EntityRelationship with `targetEntityType: LIABILITY`. Co-borrowers and guarantors use ASSOCIATED_WITH relationships. Notes are managed via `/{id}/notes` sub-resource (not a flat field). Documents are managed via `/{id}/document` sub-resource.

---

### IndividualEstatePlanningDto (Nested on Individual)

**Description:** Estate planning information for an individual, including will, healthcare directive, financial POA, guardianship, marital agreements, and estate review. This is NOT a standalone entity -- it is set via PATCH on Individual.

**Required Fields:** None (all optional sections)

**How to set:** `PATCH /api/v1/individual/{id}` with `{ "estatePlanning": { ... } }`

**Top-Level Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Read-only identifier |
| `will` | WillInfoDto | Will and testament information |
| `healthcare` | HealthcareDirectiveInfoDto | Healthcare directive information |
| `financialPoa` | FinancialPoaInfoDto | Financial power of attorney |
| `guardianship` | GuardianshipInfoDto | Guardianship designations |
| `maritalAgreement` | MaritalAgreementInfoDto | Prenuptial/postnuptial agreements |
| `estateReview` | EstateReviewInfoDto | Estate review and valuations |

**WillInfoDto:**

| Field | Type | Description |
|-------|------|-------------|
| `hasWill` | Boolean | Whether the individual has an executed will |
| `willDate` | LocalDate | Date the will was executed |
| `lastReviewedDate` | LocalDate | Date will was last reviewed by attorney |
| `jurisdiction` | String | State/jurisdiction where will was executed |
| `executorName` | String | Primary executor name |
| `executorIndividualId` | UUID | Executor's Individual record UUID |
| `contingentExecutorName` | String | Contingent executor name |
| `contingentExecutorIndividualId` | UUID | Contingent executor's Individual UUID |
| `attorneyName` | String | Will attorney name |
| `attorneyContactId` | UUID | Attorney's Contact record UUID |
| `notes` | String | Additional notes |

**HealthcareDirectiveInfoDto:**

| Field | Type | Description |
|-------|------|-------------|
| `hasHealthcareDirective` | Boolean | Whether individual has a healthcare directive |
| `directiveDate` | LocalDate | Date directive was executed |
| `agentName` | String | Healthcare agent name |
| `agentIndividualId` | UUID | Agent's Individual record UUID |
| `alternateAgentName` | String | Alternate agent name |
| `alternateAgentIndividualId` | UUID | Alternate agent's Individual UUID |
| `hasLivingWill` | Boolean | Whether individual has a living will |
| `specificHealthcareWishes` | String | Treatment preferences |

**FinancialPoaInfoDto:**

| Field | Type | Description |
|-------|------|-------------|
| `hasFinancialPoa` | Boolean | Whether individual has a financial POA |
| `type` | Enum | GENERAL, LIMITED, DURABLE, SPRINGING |
| `agentName` | String | POA agent name |
| `agentIndividualId` | UUID | Agent's Individual record UUID |
| `poaDate` | LocalDate | Date the POA was executed |
| `isCurrentlyEffective` | Boolean | Whether the POA is currently in effect |

**GuardianshipInfoDto:**

| Field | Type | Description |
|-------|------|-------------|
| `hasGuardianDesignation` | Boolean | Whether guardian is designated |
| `guardianName` | String | Designated guardian name |
| `guardianIndividualId` | UUID | Guardian's Individual UUID |
| `alternateGuardianName` | String | Alternate guardian name |
| `alternateGuardianIndividualId` | UUID | Alternate guardian's Individual UUID |

**MaritalAgreementInfoDto:**

| Field | Type | Description |
|-------|------|-------------|
| `hasPrenuptialAgreement` | Boolean | Whether prenuptial agreement exists |
| `prenuptialDate` | LocalDate | Prenuptial execution date |
| `hasPostnuptialAgreement` | Boolean | Whether postnuptial agreement exists |
| `postnuptialDate` | LocalDate | Postnuptial execution date |
| `summary` | String | Summary of key terms |
| `attorneyContactId` | UUID | Attorney's Contact record UUID |

**EstateReviewInfoDto:**

| Field | Type | Description |
|-------|------|-------------|
| `lastReviewDate` | LocalDate | Last estate plan review date |
| `nextReviewDate` | LocalDate | Next scheduled review date |
| `attorneyName` | String | Estate planning attorney name |
| `attorneyContactId` | UUID | Attorney's Contact record UUID |
| `notes` | String | General estate plan notes |
| `estimatedEstateValue` | BigDecimal | Estimated total estate value |
| `estimatedEstateTaxLiability` | BigDecimal | Estimated federal estate tax |
| `lifetimeGiftExclusionUsed` | BigDecimal | Cumulative lifetime gift exclusion used |

---

### IndividualPhilanthropicProfileDto (Nested on Individual)

**Description:** Philanthropic giving profile for an individual capturing charitable activity, preferences, and pledges. This is NOT a standalone entity -- it is set via PATCH on Individual.

**Required Fields:** None (all optional)

**How to set:** `PATCH /api/v1/individual/{id}` with `{ "philanthropicProfile": { ... } }`

**Writable Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Read-only identifier |
| `totalAnnualCharitableGiving` | BigDecimal | Total annual charitable giving |
| `givingAsOfYear` | Integer | Year the giving figure represents |
| `preferredGivingVehicles` | Set&lt;GivingVehicleType&gt; | Preferred giving vehicles as an enum set. Values: DONOR_ADVISED_FUND, DIRECT_GIFT, BEQUEST, CHARITABLE_REMAINDER_TRUST, CHARITABLE_LEAD_TRUST, PRIVATE_FOUNDATION, POOLED_INCOME_FUND, CHARITABLE_GIFT_ANNUITY, QUALIFIED_CHARITABLE_DISTRIBUTION, OTHER |
| `charitableIntentNotes` | String | Notes about charitable intent and priorities |
| `isMajorDonor` | Boolean | Whether the individual is a major donor |
| `hasCharitablePledge` | Boolean | Whether outstanding pledges exist |
| `totalOutstandingPledges` | BigDecimal | Total outstanding pledge amount |
| `legacyGivingInterest` | Boolean | Interest in legacy/planned giving |
| `notes` | String | General philanthropic notes |

---

### LegalEntityCharitableDetailsDto (Nested on LegalEntity)

**Description:** Charitable details for a legal entity (foundation, DAF, charitable trust, etc.). Uses sections that are relevant based on the `charitableVehicleType`. This is NOT a standalone entity -- it is set via PATCH on LegalEntity.

**Required Fields:** None (all optional)

**How to set:** `PATCH /api/v1/legal-entity/{id}` with `{ "charitableDetails": { ... } }`

**Top-Level Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Read-only identifier |
| `charitableVehicleType` | Enum | DONOR_ADVISED_FUND, CHARITABLE_REMAINDER_UNITRUST, CHARITABLE_REMAINDER_ANNUITY_TRUST, CHARITABLE_LEAD_UNITRUST, CHARITABLE_LEAD_ANNUITY_TRUST, PRIVATE_FOUNDATION, COMMUNITY_FOUNDATION, SUPPORTING_ORGANIZATION, PUBLIC_CHARITY |
| `irsExemptionStatus` | Enum | STATUS_501C3, STATUS_501C4, STATUS_501C6, STATUS_501C7, NOT_EXEMPT, PENDING |
| `irsDeterminationDate` | LocalDate | IRS determination letter date |
| `irsEin` | String | IRS Employer Identification Number |
| `missionStatement` | String | Mission statement |
| `focusAreas` | String | Comma-separated focus areas |
| `notes` | String | General notes |
| `daf` | DafInfoDto | DAF-specific details (when DONOR_ADVISED_FUND) |
| `charitableTrust` | CharitableTrustInfoDto | Trust details (when CHARITABLE_REMAINDER_* or CHARITABLE_LEAD_*) |
| `foundation` | FoundationInfoDto | Foundation details (when PRIVATE_FOUNDATION, COMMUNITY_FOUNDATION, SUPPORTING_ORGANIZATION, PUBLIC_CHARITY) |

**DafInfoDto (charitableVehicleType = DONOR_ADVISED_FUND):**

| Field | Type | Description |
|-------|------|-------------|
| `sponsorName` | String | DAF sponsoring organization name |
| `accountNumber` | String | Account number at DAF sponsor |
| `currentBalance` | BigDecimal | Current DAF balance |
| `balanceAsOfDate` | LocalDate | Balance verification date |

**CharitableTrustInfoDto (charitableVehicleType = CHARITABLE_REMAINDER_* or CHARITABLE_LEAD_*):**

| Field | Type | Description |
|-------|------|-------------|
| `payoutRate` | BigDecimal | Annual payout rate as percentage |
| `payoutFrequency` | String | Distribution frequency |
| `remainderBeneficiaryDescription` | String | Remainder beneficiary description |
| `incomeBeneficiaryDescription` | String | Income beneficiary description |
| `termDescription` | String | Trust term description |
| `termEndDate` | LocalDate | Trust termination date |
| `initialFundingAmount` | BigDecimal | Initial funding amount |
| `initialFundingDate` | LocalDate | Initial funding date |

**FoundationInfoDto (charitableVehicleType = PRIVATE_FOUNDATION, COMMUNITY_FOUNDATION, SUPPORTING_ORGANIZATION, PUBLIC_CHARITY):**

| Field | Type | Description |
|-------|------|-------------|
| `totalEndowment` | BigDecimal | Total endowment value |
| `endowmentAsOfDate` | LocalDate | Endowment valuation date |
| `annualGrantBudget` | BigDecimal | Annual grant budget |
| `minimumDistributionRequirement` | BigDecimal | IRS minimum distribution requirement |
| `hasPaidStaff` | Boolean | Whether foundation has paid staff |
| `fiscalYearEnd` | String | Fiscal year end (MM-DD format) |
| `grantingFrequency` | String | How often grants are awarded |
| `totalGrantsYtd` | BigDecimal | Total grants year-to-date |
| `totalGrantsLastYear` | BigDecimal | Total grants last year |

---

### RelationshipEngagementDetailsDto (Nested on EntityRelationship)

**Description:** Professional engagement details for a relationship, capturing fee structure, scope of services, and review tracking. Applicable to ADVISOR, ATTORNEY, ACCOUNTANT, and similar professional relationships. This is NOT a standalone entity -- it is set when creating/updating a relationship.

**Required Fields:** None (all optional)

**How to set:** Include in EntityRelationship create/update: `POST /api/v1/entity-relationship` with `{ ..., "engagementDetails": { ... } }`

**Writable Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Read-only identifier |
| `engagementStatus` | Enum | ACTIVE, INACTIVE, ON_HOLD, TERMINATED |
| `engagementStartDate` | LocalDate | Engagement start date |
| `engagementEndDate` | LocalDate | Engagement end or scheduled end date |
| `feeStructureType` | Enum | HOURLY, RETAINER, FLAT_FEE, AUM_BASED, CONTINGENCY, PRO_BONO |
| `hourlyRate` | BigDecimal | Hourly rate (when HOURLY) |
| `retainerAmount` | BigDecimal | Retainer per period (when RETAINER) |
| `retainerFrequency` | Enum | MONTHLY, QUARTERLY, ANNUAL |
| `flatFeeAmount` | BigDecimal | Flat fee amount (when FLAT_FEE) |
| `aumBasisPoints` | Integer | AUM fee in basis points, 100 = 1% (when AUM_BASED) |
| `estimatedAnnualCost` | BigDecimal | Estimated total annual cost |
| `scopeOfServices` | String | Scope of services provided |
| `engagementLetterDocumentId` | String | UUID of engagement letter Document |
| `lastReviewDate` | LocalDate | Last engagement review date |
| `nextReviewDate` | LocalDate | Next scheduled review date |
| `satisfactionRating` | Integer | Client satisfaction (1-5 scale) |
| `notes` | String | General engagement notes |

---

## Key Enums

### LegalEntityType
CORPORATION, LLC, TRUST, PARTNERSHIP, LIMITED_PARTNERSHIP, LLP, FOUNDATION, ESTATE, SOLE_PROPRIETORSHIP, NON_PROFIT, GOVERNMENT_ENTITY, OTHER

### Individual Enums
**Gender:** (No Java enum found -- `gender` may be a free-text String field; commonly MALE, FEMALE, OTHER)
**MaritalStatus:** (No Java enum found -- `maritalStatus` may be a free-text String field; commonly SINGLE, MARRIED, DIVORCED, WIDOWED, DOMESTIC_PARTNERSHIP)
**TaxIdType:** SSN, ITIN, EIN, FOREIGN_TIN, FOREIGN_ENTITY_TIN, VAT, GST, BUSINESS_NUMBER
**Residency:** US_RESIDENT, FOREIGN_NATIONAL, GREEN_CARD_HOLDER, DUAL_RESIDENT, UNKNOWN
**EntityLifecycleStatus:** DRAFT, PENDING_VERIFICATION, ACTIVE, INACTIVE, ARCHIVED

### Financial Profile Enums
**InvestorRiskTolerance:** CONSERVATIVE, MODERATELY_CONSERVATIVE, MODERATE, MODERATE_AGGRESSIVE, AGGRESSIVE, VERY_AGGRESSIVE
**InvestorInvestmentTimeHorizon:** VERY_SHORT_TERM, SHORT_TERM, MEDIUM_TERM, LONG_TERM, VERY_LONG_TERM
**InvestorSourceOfFunds:** EMPLOYMENT_INCOME, BUSINESS_INCOME, INVESTMENT_INCOME, INHERITANCE, GIFT, SALE_OF_PROPERTY, SALE_OF_BUSINESS, LEGAL_SETTLEMENT, RETIREMENT_FUNDS, INSURANCE_PROCEEDS, LOTTERY_OR_GAMBLING, OTHER

### Document Enums
**DocumentContentType:** PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, TXT, CSV, JSON, XML, HTML, JPG, PNG, GIF, ZIP, MP4, MP3

### Account Enums
**AccountCategory:** INDIVIDUAL, ENTITY
**SubCategory (AccountCategorySubCategory):** INDIVIDUAL, JOINT_WITH_RIGHTS_OF_SURVIVORSHIP, JOINT_TENANTS_IN_COMMON, COMMUNITY_PROPERTY, UNIFORM_GIFT_OR_TRANSFER_TO_MINOR, OTHER_INDIVIDUAL, IRA, ROTH_IRA, SEP_IRA, SIMPLE_IRA, PENSION_401K, ROLLOVER_IRA, INHERITED_IRA, KEOGH_PLAN, PENSION_OR_PROFIT_SHARING_PLAN, SELF_DIRECTED_RETIREMENT_ACCOUNT, TRUST_INDIVIDUAL, GRANTOR_TRUST, REVOCABLE_TRUST, IRREVOCABLE_TRUST, SIMPLE_TRUST, COMPLEX_TRUST, CHARITABLE_TRUST, REMAINDER_TRUST, JOINT_TRUST, CORPORATION, C_CORP, S_CORP, PARTNERSHIP, LIMITED_PARTNERSHIP, LIMITED_LIABILITY_COMPANY, FUND_OF_FUNDS, JOINT_TENANTS_IN_COMMON_ENTITIES, JOINT_RIGHTS_OF_SURVIVORSHIP_ENTITIES, PRIVATE_FOUNDATION, ENDOWMENT, BENEFIT_PLAN, OTHER_TAX_EXEMPT_ORGANIZATION, ESTATE, OTHER_NON_INDIVIDUAL
**TaxStatus:** TAXABLE, TAX_DEFERRED, TAX_FREE
**OnlineStatus:** ACTIVE, CLOSED, ON_HOLD, PENDING
**OwnershipType:** PERCENT_BASED, EQUAL_SPLIT

### TangibleAsset Enums
**Category:** VEHICLE, REAL_PROPERTY, LUXURY, COLLECTIBLE, OTHER
**AssetType (TangibleAssetType):** CAR, MOTORCYCLE, BOAT, YACHT, AIRCRAFT, HELICOPTER, RV, PRIMARY_RESIDENCE, VACATION_HOME, RENTAL_PROPERTY, COMMERCIAL_PROPERTY, LAND, FARM_RANCH, TIMESHARE, WATCH, JEWELRY, HANDBAG, FASHION, LUXURY_OTHER, ART, WINE, ANTIQUE, MEMORABILIA, COINS, STAMPS, BOOKS, MUSICAL_INSTRUMENT, COLLECTIBLE_OTHER, EQUIPMENT, LIVESTOCK, FURNITURE, OTHER_TYPE
**Status (TangibleAssetStatus):** ACTIVE, SOLD, TRANSFERRED, DONATED, DISPOSED, STOLEN, LOST
**AcquisitionType (TangibleAssetAcquisitionType):** PURCHASE, AUCTION, GIFT, INHERITANCE, COMMISSION, EXCHANGE, PRIZE

### Insurance Policy Enums
**InsurancePolicyCategory:** LIFE, UMBRELLA, LONG_TERM_CARE, DISABILITY, HEALTH, AUTO, OTHER
**InsurancePolicyStatus:** ACTIVE, LAPSED, CANCELLED, PAID_UP, SURRENDERED, MATURED, PENDING
**LifePolicyType:** TERM, WHOLE_LIFE, UNIVERSAL, VARIABLE_UNIVERSAL, INDEXED_UNIVERSAL, SURVIVORSHIP, GROUP_TERM
**DividendOption:** CASH, PREMIUM_REDUCTION, ACCUMULATE_AT_INTEREST, PAID_UP_ADDITIONS, ONE_YEAR_TERM
**InflationProtectionType:** NONE, SIMPLE, COMPOUND_3_PERCENT, COMPOUND_5_PERCENT, CPI_LINKED, FUTURE_PURCHASE_OPTION
**PaymentFrequency:** MONTHLY, BI_WEEKLY, QUARTERLY, ANNUAL, INTEREST_ONLY

### Liability Enums
**LiabilityType:** MORTGAGE, HOME_EQUITY_LOC, STUDENT_LOAN, PERSONAL_LOAN, CREDIT_LINE, MARGIN_LOAN, AUTO_LOAN, BUSINESS_LOAN, CREDIT_CARD, PLEDGED_ASSET_LINE, OTHER
**LiabilityStatus:** CURRENT, DELINQUENT, IN_DEFERMENT, IN_FORBEARANCE, PAID_OFF, DEFAULTED, CHARGED_OFF
**InterestRateType:** FIXED, VARIABLE, HYBRID
**InterestDeductionType:** MORTGAGE_INTEREST, INVESTMENT_INTEREST, STUDENT_LOAN_INTEREST, BUSINESS_INTEREST, NONE

### Estate Planning Enums
**FinancialPoaType:** GENERAL, LIMITED, DURABLE, SPRINGING

### Charitable Enums
**CharitableVehicleType:** DONOR_ADVISED_FUND, CHARITABLE_REMAINDER_UNITRUST, CHARITABLE_REMAINDER_ANNUITY_TRUST, CHARITABLE_LEAD_UNITRUST, CHARITABLE_LEAD_ANNUITY_TRUST, PRIVATE_FOUNDATION, COMMUNITY_FOUNDATION, SUPPORTING_ORGANIZATION, PUBLIC_CHARITY
**IrsExemptionStatus:** STATUS_501C3, STATUS_501C4, STATUS_501C6, STATUS_501C7, NOT_EXEMPT, PENDING

### Engagement Enums
**EngagementStatus:** ACTIVE, INACTIVE, ON_HOLD, TERMINATED
**FeeStructureType:** HOURLY, RETAINER, FLAT_FEE, AUM_BASED, CONTINGENCY, PRO_BONO
**RetainerFrequency:** MONTHLY, QUARTERLY, ANNUAL

### EntityRelationshipType (Common for Onboarding)

| Type | Uses % | Symmetric | Description |
|------|--------|-----------|-------------|
| `OWNERSHIP` | Yes | No | Source owns X% of target |
| `BENEFICIAL_OWNERSHIP` | Yes | No | Source has beneficial ownership of target |
| `MEMBER` | Yes | No | Source is member of target (household or LLC) |
| `PARTNER` | Yes | No | Source is partner in target |
| `TRUSTEE` | No | No | Source is trustee of target trust |
| `SUCCESSOR_TRUSTEE` | No | No | Source is successor trustee of target trust |
| `GRANTOR` | No | No | Source is grantor/settlor of target trust |
| `BENEFICIARY` | Yes | No | Source is beneficiary of target |
| `SPOUSE` | No | Yes | Source is married to target (max 1) |
| `PARENT` | No | No | Source is parent of target (max 2 on target) |
| `CHILD` | No | No | Source is child of target |
| `SIBLING` | No | Yes | Source is sibling of target |
| `GUARDIAN` | No | No | Source is guardian of target (max 1 on target) |
| `POWER_OF_ATTORNEY` | No | No | Source has POA for target |
| `AUTHORIZED_SIGNER` | No | No | Source can sign for target |
| `OFFICER` | No | No | Source is officer of target |
| `DIRECTOR` | No | No | Source is director of target |
| `ADVISOR` | No | No | Source advises target |
| `ACCOUNTANT` | No | No | Source is accountant for target |
| `ATTORNEY` | No | No | Source is attorney for target |
| `CONTROL` | No | No | Source controls target |

### RelationshipEntityType (All 14)
INDIVIDUAL, LEGAL_ENTITY, HOUSEHOLD, ACCOUNT_FINANCIAL, ACCOUNT_PORTFOLIO, STRATEGY, FUND, FUND_SHARE_CLASS, CUSTODIAN, CONTACT, INVESTMENT_ORDER, TANGIBLE_ASSET, LIABILITY, INSURANCE_POLICY

---

## Common CRUD Endpoints

### Individual
```
GET    /api/v1/individual              # List
POST   /api/v1/individual              # Create
GET    /api/v1/individual/{id}         # Read
PATCH  /api/v1/individual/{id}         # Update
DELETE /api/v1/individual/{id}         # Delete
```

### LegalEntity
```
GET    /api/v1/legal-entity            # List
POST   /api/v1/legal-entity            # Create
GET    /api/v1/legal-entity/{id}       # Read
PATCH  /api/v1/legal-entity/{id}       # Update
DELETE /api/v1/legal-entity/{id}       # Delete
```

### Household
```
GET    /api/v1/household               # List
POST   /api/v1/household               # Create
GET    /api/v1/household/{id}          # Read
PATCH  /api/v1/household/{id}          # Update
DELETE /api/v1/household/{id}          # Delete
```

### AccountFinancial
```
GET    /api/v1/account-financial       # List
POST   /api/v1/account-financial       # Create
GET    /api/v1/account-financial/{id}  # Read
PATCH  /api/v1/account-financial/{id}  # Update
DELETE /api/v1/account-financial/{id}  # Delete
```

### Contact
```
GET    /api/v1/contact                 # List
POST   /api/v1/contact                 # Create
GET    /api/v1/contact/{id}            # Read
PATCH  /api/v1/contact/{id}            # Update
DELETE /api/v1/contact/{id}            # Delete
```

### TangibleAsset
```
GET    /api/v1/tangible-asset          # List
POST   /api/v1/tangible-asset          # Create
GET    /api/v1/tangible-asset/{id}     # Read
PATCH  /api/v1/tangible-asset/{id}     # Update
DELETE /api/v1/tangible-asset/{id}     # Delete
```

### InsurancePolicy
```
GET    /api/v1/insurance-policy         # List
POST   /api/v1/insurance-policy         # Create
GET    /api/v1/insurance-policy/{id}    # Read
PATCH  /api/v1/insurance-policy/{id}    # Update
DELETE /api/v1/insurance-policy/{id}    # Delete
```

### Liability
```
GET    /api/v1/liability                # List
POST   /api/v1/liability                # Create
GET    /api/v1/liability/{id}           # Read
PATCH  /api/v1/liability/{id}           # Update
DELETE /api/v1/liability/{id}           # Delete
```

### EntityRelationship
```
GET    /api/v1/entity-relationship     # List
POST   /api/v1/entity-relationship     # Create
GET    /api/v1/entity-relationship/{id}      # Read
PATCH  /api/v1/entity-relationship/{id}     # Update
DELETE /api/v1/entity-relationship/{id}     # Delete
```

---

## Example: Create Individual with Nested Objects

```bash
POST /api/v1/individual
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Smith",
  "dateOfBirth": "1975-06-15",
  "email": "john@example.com",
  "phoneNumberPrimary": "+1-555-0100",
  "gender": "MALE",
  "maritalStatus": "MARRIED",
  "citizenship": "US",
  "residency": "US_RESIDENT",
  "lifecycleStatus": "ACTIVE",
  "addressLegal": {
    "addressLine1": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "postalCode": "10001",
    "country": "US",
    "addressType": "PRIMARY"
  },
  "financialProfile": {
    "netWorth": 5000000.00,
    "netWorthLiquid": 1000000.00,
    "annualIncome": 250000.00,
    "investorSourceOfFunds": "SALE_OF_BUSINESS",
    "riskTolerance": "MODERATE",
    "timeHorizon": "LONG_TERM"
  },
  "regulatoryStatus": {
    "accredited": true,
    "qualifiedClient": true,
    "qualifiedPurchaser": false
  }
}
```

---

## Example: Create AccountFinancial

```bash
POST /api/v1/account-financial
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "name": "Smith Family Brokerage",
  "accountNumber": "ACC-123456",
  "accountCategory": "INDIVIDUAL",
  "subCategory": "TAXABLE",
  "currencyCode": "USD",
  "onlineStatus": "ACTIVE",
  "custodianAccountNumber": "CUST-987654",
  "ownershipType": "PERCENT_BASED",
  "isRolledUp": true,
  "billing": {
    "feeScheduleId": "fs-123",
    "billingMethod": "PERCENT_AUM",
    "feePercentage": 0.50,
    "minimumAnnualFee": 1000.00,
    "currency": "USD"
  },
  "investmentProfile": {
    "riskTolerance": "MODERATE",
    "investmentObjectives": ["GROWTH", "INCOME"],
    "timeHorizon": "LONG_TERM"
  }
}
```

---

## Example: Create TangibleAsset

```bash
POST /api/v1/tangible-asset
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "name": "Primary Residence",
  "category": "REAL_PROPERTY",
  "assetType": "PRIMARY_RESIDENCE",
  "status": "ACTIVE",
  "currentValue": 2500000.00,
  "valuationDate": "2024-03-10",
  "valuationSource": "RECENT_APPRAISAL",
  "currencyCode": "USD",
  "purchasePrice": 1800000.00,
  "purchaseDate": "2015-05-20",
  "acquisitionType": "PURCHASE",
  "taxBasis": 1800000.00,
  "taxBasisDate": "2015-05-20",
  "location": "New York, NY",
  "includedInEstate": true,
  "realPropertyDetails": {
    "address": "123 Main Street, New York, NY 10001",
    "propertyType": "SINGLE_FAMILY_HOME",
    "squareFootage": 4200,
    "yearBuilt": 1995,
    "lotSize": 0.75,
    "bedrooms": 5,
    "bathrooms": 4,
    "garage": "3-CAR"
  }
}
```

---

## Example: Create Relationship (Individual owns Account)

```bash
POST /api/v1/entity-relationship
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "relationshipType": "OWNERSHIP",
  "sourceEntityType": "INDIVIDUAL",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440000",
  "targetEntityType": "ACCOUNT_FINANCIAL",
  "targetEntityId": "660e8400-e29b-41d4-a716-446655440001",
  "percentage": 100.0,
  "isPrimary": true,
  "effectiveFrom": "2024-01-01"
}
```

---

## Example: Create Insurance Policy (Life)

```bash
POST /api/v1/insurance-policy
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "policyCategory": "LIFE",
  "name": "Northwestern Mutual Whole Life",
  "policyNumber": "POL-2024-789456",
  "carrierName": "Northwestern Mutual",
  "policyStatus": "ACTIVE",
  "coverageAmount": 2000000.00,
  "annualPremium": 18500.00,
  "paymentFrequency": "ANNUAL",
  "effectiveDate": "2020-01-01",
  "lifePolicyType": "WHOLE_LIFE",
  "deathBenefit": 2000000.00,
  "cashValue": 125000.00,
  "cashValueAsOfDate": "2026-01-01",
  "isIlitOwned": false,
  "isSecondToDie": false,
  "guaranteedDeathBenefit": true,
  "dividendOption": "PAID_UP_ADDITIONS",
  "riders": "Waiver of Premium, Accelerated Death Benefit"
}
```

---

## Example: Create Insurance Policy (Umbrella)

```bash
POST /api/v1/insurance-policy
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "policyCategory": "UMBRELLA",
  "name": "Chubb Umbrella Policy",
  "carrierName": "Chubb",
  "policyStatus": "ACTIVE",
  "coverageAmount": 5000000.00,
  "annualPremium": 1800.00,
  "paymentFrequency": "ANNUAL",
  "effectiveDate": "2025-01-01",
  "expirationDate": "2026-01-01",
  "excessLiabilityCoverage": 5000000.00,
  "underlyingAutoRequired": 500000.00,
  "underlyingHomeRequired": 500000.00,
  "coversRentalProperties": true,
  "coversWatercraft": false,
  "uninsuredMotorist": true
}
```

---

## Example: Create Liability (Mortgage)

```bash
POST /api/v1/liability
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "name": "Chase Home Mortgage",
  "liabilityType": "MORTGAGE",
  "liabilityStatus": "CURRENT",
  "lenderName": "JPMorgan Chase",
  "accountNumber": "XXXX-1234",
  "originalBalance": 500000.00,
  "currentBalance": 425000.00,
  "balanceAsOfDate": "2026-03-01",
  "interestRate": 6.50,
  "interestRateType": "FIXED",
  "monthlyPayment": 2750.00,
  "paymentFrequency": "MONTHLY",
  "originationDate": "2022-06-15",
  "maturityDate": "2052-06-15",
  "isSecured": true,
  "collateralDescription": "123 Main St, New York, NY 10001",
  "isInterestDeductible": true,
  "interestDeductionType": "MORTGAGE_INTEREST",
  "interestPaidYtd": 18750.00
}
```

---

## Example: Update Individual with Estate Planning

```bash
PATCH /api/v1/individual/{id}
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "estatePlanning": {
    "will": {
      "hasWill": true,
      "willDate": "2024-01-15",
      "lastReviewedDate": "2025-06-01",
      "jurisdiction": "New York",
      "executorName": "Jane Smith"
    },
    "healthcare": {
      "hasHealthcareDirective": true,
      "directiveDate": "2024-03-20",
      "agentName": "Jane Smith",
      "hasLivingWill": true
    },
    "financialPoa": {
      "hasFinancialPoa": true,
      "type": "DURABLE",
      "agentName": "Jane Smith",
      "isCurrentlyEffective": true
    },
    "guardianship": {
      "hasGuardianDesignation": true,
      "guardianName": "Michael Johnson",
      "alternateGuardianName": "Sarah Johnson"
    },
    "estateReview": {
      "lastReviewDate": "2025-01-15",
      "nextReviewDate": "2028-01-15",
      "estimatedEstateValue": 15000000.00,
      "estimatedEstateTaxLiability": 560000.00,
      "lifetimeGiftExclusionUsed": 2000000.00
    }
  }
}
```

---

## Example: Update Individual with Philanthropic Profile

```bash
PATCH /api/v1/individual/{id}
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "philanthropicProfile": {
    "totalAnnualCharitableGiving": 250000.00,
    "givingAsOfYear": 2025,
    "preferredGivingVehicles": ["DONOR_ADVISED_FUND", "DIRECT_GIFT"],
    "charitableIntentNotes": "Focus on education and healthcare in underserved communities",
    "isMajorDonor": true,
    "hasCharitablePledge": false,
    "legacyGivingInterest": true
  }
}
```

---

## Example: Update LegalEntity with Charitable Details (Foundation)

```bash
PATCH /api/v1/legal-entity/{id}
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "charitableDetails": {
    "charitableVehicleType": "PRIVATE_FOUNDATION",
    "irsExemptionStatus": "STATUS_501C3",
    "irsDeterminationDate": "2015-03-15",
    "irsEin": "12-3456789",
    "missionStatement": "Advancing educational opportunities for underserved youth",
    "focusAreas": "Education, Youth Development",
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

---

## Example: Create Relationship with Engagement Details

```bash
POST /api/v1/entity-relationship
Authorization: Bearer {id_token}
Content-Type: application/json

{
  "relationshipType": "ATTORNEY",
  "sourceEntityType": "CONTACT",
  "sourceEntityId": "550e8400-e29b-41d4-a716-446655440000",
  "targetEntityType": "INDIVIDUAL",
  "targetEntityId": "660e8400-e29b-41d4-a716-446655440001",
  "isPrimary": true,
  "effectiveFrom": "2024-01-15",
  "engagementDetails": {
    "engagementStatus": "ACTIVE",
    "engagementStartDate": "2024-01-15",
    "feeStructureType": "RETAINER",
    "retainerAmount": 5000.00,
    "retainerFrequency": "MONTHLY",
    "estimatedAnnualCost": 60000.00,
    "scopeOfServices": "Estate planning, trust administration, and tax advisory",
    "satisfactionRating": 4
  }
}
```

---

## Error Responses

**Standard 400 Bad Request:**
```json
{
  "type": "about:blank",
  "status": 400,
  "title": "Bad Request",
  "detail": "Validation failed"
}
```

**409 Conflict (Entity In Use):**
```json
{
  "type": "about:blank",
  "status": 409,
  "title": "Conflict",
  "detail": "Cannot delete: referenced by 2 AccountFinancial entities"
}
```

**401 Unauthorized:**
```json
{
  "type": "about:blank",
  "status": 401,
  "title": "Unauthorized",
  "detail": "Invalid or missing authentication"
}
```

**403 Forbidden:**
```json
{
  "type": "about:blank",
  "status": 403,
  "title": "Forbidden",
  "detail": "Insufficient permissions"
}
```

---

## Field Validation Rules

**Email:** RFC 5322 compliant
**Phone:** E.164 format (+1-555-0100 or +44-20-xxxx-xxxx)
**Date:** ISO 8601 (YYYY-MM-DD)
**UUID:** Standard 36-character format (with hyphens)
**Currency Code:** ISO 4217 (USD, EUR, GBP, etc.)
**Country Code:** ISO 3166-1 alpha-2 (US, GB, CA, etc.)

---

### BaseNoteDto (Abstract Base for All Notes)

**Description:** Abstract base for note DTOs. Insurance policy notes and liability notes extend this.

**Writable Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `noteText` | String | Yes | Note content (1-10,000 characters) |

**Read-Only Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `isEdited` | Boolean | Whether note was edited after creation |
| `canEdit` | Boolean | Whether current user can edit this note |
| `canDelete` | Boolean | Whether current user can delete this note |
| `createdBy` | String | User who created the note |
| `createdDate` | Instant | Creation timestamp |
| `lastModifiedBy` | String | User who last modified |
| `lastModifiedDate` | Instant | Last modification timestamp |

---

### InsurancePolicyNoteDto (extends BaseNoteDto)

**Description:** Note attached to an insurance policy. Managed via `/{id}/notes` sub-resource on insurance-policy.

**Additional Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Note identifier (read-only) |
| `insurancePolicyId` | String | ID of the parent insurance policy |
| `insurancePolicyName` | String | Name of the policy (read-only) |

---

### LiabilityNoteDto (extends BaseNoteDto)

**Description:** Note attached to a liability. Managed via `/{id}/notes` sub-resource on liability.

**Additional Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Note identifier (read-only) |
| `liabilityId` | String | ID of the parent liability |
| `liabilityName` | String | Name of the liability (read-only) |

---

### InsurancePolicyDocumentCreateRequestDto (extends DocumentCreateRequestDto)

**Description:** Request payload for uploading a document to an insurance policy. Sent as the `createRequest` part of a multipart POST to `/api/v1/insurance-policy/{policyId}/document`.

**Additional Fields (beyond base DocumentCreateRequestDto):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `insurancePolicyId` | UUID | No | Policy ID (optional if in URL path) |
| `documentSubType` | DocumentTypeInsurancePolicy | No | Document subtype for categorization |
| `docTypeHint` | String | No | Parser hint for extraction accuracy |

---

### InsurancePolicyDocumentDto (extends DocumentDto)

**Description:** Document attached to an insurance policy. Inherits all common document fields (title, description, s3Key, fileSize, mimeType, etc.).

**Additional Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `insurancePolicyId` | String | ID of the parent insurance policy (required) |
| `insurancePolicyName` | String | Name of the policy (read-only) |
| `documentSubType` | DocumentTypeInsurancePolicy | Document subtype (required) |
| `category` | String | Category derived from subtype (read-only) |

---

### LiabilityDocumentCreateRequestDto (extends DocumentCreateRequestDto)

**Description:** Request payload for uploading a document to a liability. Sent as the `createRequest` part of a multipart POST to `/api/v1/liability/{liabilityId}/document`.

**Additional Fields (beyond base DocumentCreateRequestDto):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `liabilityId` | UUID | No | Liability ID (optional if in URL path) |
| `documentSubType` | DocumentTypeLiability | No | Document subtype for categorization |
| `docTypeHint` | String | No | Parser hint for extraction accuracy |

---

### LiabilityDocumentDto (extends DocumentDto)

**Description:** Document attached to a liability. Inherits all common document fields (title, description, s3Key, fileSize, mimeType, etc.).

**Additional Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `liabilityId` | String | ID of the parent liability (required) |
| `liabilityName` | String | Name of the liability (read-only) |
| `documentSubType` | DocumentTypeLiability | Document subtype (required) |
| `category` | String | Category derived from subtype (read-only) |

---

### DocumentTypeInsurancePolicy Enum

**Values (27 total, 8 categories):**

| Value | Display Name | Category |
|-------|-------------|----------|
| `POLICY_DECLARATION` | Policy Declaration Page | Policy Document |
| `POLICY_CONTRACT` | Full Policy Contract | Policy Document |
| `POLICY_AMENDMENT` | Policy Amendment/Endorsement | Policy Document |
| `POLICY_RENEWAL` | Renewal Notice | Policy Document |
| `POLICY_SCHEDULE` | Policy Schedule of Benefits | Policy Document |
| `APPLICATION` | Insurance Application | Application |
| `UNDERWRITING_REPORT` | Underwriting Report | Application |
| `MEDICAL_EXAM` | Medical Exam Results | Application |
| `MEDICAL_RECORDS` | Medical Records | Application |
| `CLAIM_FORM` | Claim Form | Claims |
| `CLAIM_CORRESPONDENCE` | Claim Correspondence | Claims |
| `CLAIM_SETTLEMENT` | Claim Settlement | Claims |
| `PREMIUM_NOTICE` | Premium Notice | Billing |
| `PAYMENT_RECEIPT` | Payment Receipt | Billing |
| `BILLING_STATEMENT` | Billing Statement | Billing |
| `BENEFICIARY_DESIGNATION` | Beneficiary Designation Form | Beneficiary |
| `BENEFICIARY_CHANGE` | Beneficiary Change Request | Beneficiary |
| `POWER_OF_ATTORNEY` | Power of Attorney | Legal |
| `TRUST_ASSIGNMENT` | Trust Assignment | Legal |
| `IRREVOCABLE_ASSIGNMENT` | Irrevocable Assignment | Legal |
| `OWNERSHIP_CHANGE` | Ownership Change Request | Legal |
| `ANNUAL_STATEMENT` | Annual Policy Statement | Correspondence |
| `ILLUSTRATION` | Policy Illustration/Projection | Correspondence |
| `IN_FORCE_LEDGER` | In-Force Ledger | Correspondence |
| `CORRESPONDENCE` | General Correspondence | Correspondence |
| `OTHER` | Other Insurance Document | Other |

---

### DocumentTypeLiability Enum

**Values (13 total, 5 categories):**

| Value | Display Name | Category |
|-------|-------------|----------|
| `LOAN_AGREEMENT` | Loan Agreement | Legal Document |
| `PROMISSORY_NOTE` | Promissory Note | Legal Document |
| `MORTGAGE_DEED` | Mortgage Deed | Legal Document |
| `COLLATERAL_AGREEMENT` | Collateral Agreement | Legal Document |
| `LINE_OF_CREDIT_AGREEMENT` | Line of Credit Agreement | Legal Document |
| `REFINANCE_DOCUMENTS` | Refinance Documents | Legal Document |
| `AMORTIZATION_SCHEDULE` | Amortization Schedule | Statement |
| `PAYOFF_STATEMENT` | Payoff Statement | Statement |
| `ACCOUNT_STATEMENT` | Account Statement | Statement |
| `FORM_1098` | Form 1098 Mortgage Interest | Tax Document |
| `INSURANCE_CERTIFICATE` | Insurance Certificate | Correspondence |
| `CORRESPONDENCE` | General Correspondence | Correspondence |
| `OTHER` | Other Liability Document | Other |

---

### GivingVehicleType Enum

**Description:** Type of charitable giving vehicle preferred by an individual. Used on `IndividualPhilanthropicProfileDto.preferredGivingVehicles` as a Set.

**Values:**

| Value | Description |
|-------|-------------|
| `DONOR_ADVISED_FUND` | Donor recommends grants from a sponsoring organization's fund |
| `DIRECT_GIFT` | Direct outright gift to a charity |
| `BEQUEST` | Gift through will or estate plan |
| `CHARITABLE_REMAINDER_TRUST` | Income to donor, remainder to charity |
| `CHARITABLE_LEAD_TRUST` | Income to charity, remainder to heirs |
| `PRIVATE_FOUNDATION` | Family-funded, subject to IRS 5% minimum distribution |
| `POOLED_INCOME_FUND` | Commingled charitable investment pool |
| `CHARITABLE_GIFT_ANNUITY` | Fixed payments to donor, remainder to charity |
| `QUALIFIED_CHARITABLE_DISTRIBUTION` | Direct IRA distribution to charity (age 70.5+) |
| `OTHER` | Catch-all for uncommon or custom giving vehicles |

