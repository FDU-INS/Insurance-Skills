# Document-to-Entity Association Mapping

When uploading documents to Altitude, each document must be associated with the correct
entity type and given the right `documentSubType`. This reference defines those mappings.

## How to Determine the Target Entity

The primary rule: **a document associates with the entity it is ABOUT, not the entity
that merely appears in it.**

For example, a trust agreement names individuals as grantor, trustee, and beneficiaries,
but the document itself is ABOUT the trust (a Legal Entity). So it associates with the
Legal Entity, not the Individual.

> **Note on Households:** Household does NOT support direct document uploads. There is no
> `DocumentTypeHousehold` enum and no document upload endpoint on the household resource.
> Household-level documents (estate planning summaries, family meeting notes, entity
> hierarchy diagrams, etc.) should be associated with the **primary individual** or the
> **primary legal entity** in the household, using `documentSubType: "OTHER"`.

## Individual Documents

Upload via: `POST /api/v1/individual/{individualId}/document`

**Request format (multipart/form-data):**
```
Content-Type: multipart/form-data

Parts:
  createRequest (application/json):
  {
    "title": "Brett Podolsky - Driver's License",
    "description": "Florida driver's license",
    "documentType": "INDIVIDUAL",
    "contentType": "PNG",
    "documentSubType": "DRIVERS_LICENSE"
  }
  file: <binary file data>
```

| Document Type | documentSubType | How to Identify |
|---|---|---|
| Driver's License | `DRIVERS_LICENSE` | Filename contains "Driver", "DL", "License"; image of a state-issued DL |
| Passport | `PASSPORT` | Filename contains "Passport"; image of passport document |
| Social Security Card | `SOCIAL_SECURITY_CARD` | Filename contains "SSN", "Social Security" |
| Birth Certificate | `BIRTH_CERTIFICATE` | Filename contains "Birth" |
| Federal Tax Return (1040) | `FORM_1040` | Filename contains "1040", "Tax Return" + individual names; filed as personal return |
| W-2 | `FORM_W2` | Filename contains "W-2", "W2" |
| 1099-DIV | `FORM_1099_DIV` | Filename contains "1099-DIV" or "1099 DIV" |
| 1099-INT | `FORM_1099_INT` | Filename contains "1099-INT" or "1099 INT" |
| 1099-B | `FORM_1099_B` | Filename contains "1099-B" or "1099 B" |
| 1099-MISC | `FORM_1099_MISC` | Filename contains "1099-MISC" |
| 1099-R | `FORM_1099_R` | Filename contains "1099-R" |
| 1099 Composite | `FORM_1099_DIV` | Filename contains "1099 Composite" or "Consolidated" + individual name |
| W-9 (personal) | `FORM_W9` | W-9 filed under individual name (not entity) |
| State Tax Return | `STATE_TAX_RETURN` | State-specific tax return for individual |
| Property Tax Document | `PROPERTY_TAX_DOCUMENTS` | Property tax bills/receipts for individually-owned property |
| Power of Attorney | `POWER_OF_ATTORNEY` | Filename contains "POA", "Power of Attorney", "GPOA" |
| Will / Testament | `OTHER` | Filename contains "Will", "Testament" -- associate with the testator |
| Healthcare Directive | `OTHER` | Filename contains "AHCD", "Health Care", "Advance Directive" -- associate with the principal |
| HIPAA Authorization | `OTHER` | Filename contains "HIPAA" -- associate with the principal individual |
| Living Will | `OTHER` | Filename contains "Living Will" -- associate with the declarant |
| Marriage Certificate | `MARRIAGE_CERTIFICATE` | Filename contains "Marriage" |
| Net Worth Statement | `NET_WORTH_STATEMENT` | Personal financial statement |
| Bank Statement (personal) | `BANK_STATEMENT` | Personal bank account statement |
| Investment Statement (personal) | `INVESTMENT_STATEMENT` | Personal brokerage/investment account statement |
| Employment Verification | `EMPLOYMENT_VERIFICATION` | Employment verification letter |

### Special Rules for Individuals
- **1099s in individual names**: Associate with the individual named on the 1099
- **1099s for trusts/entities**: Associate with the Legal Entity, not the individual
- **Joint tax returns**: Associate with the primary filer (first name on return)
- **Onboarding sheets**: These are multi-entity; extract data but associate with the primary individual

### All Valid DocumentTypeIndividual Values (58 values)

`PASSPORT`, `DRIVERS_LICENSE`, `ENHANCED_DRIVERS_LICENSE`, `NATIONAL_ID`, `STATE_ID`, `BIRTH_CERTIFICATE`, `SOCIAL_SECURITY_CARD`, `CITIZENSHIP_CERTIFICATE`, `CERTIFICATE_OF_NATURALIZATION`, `PERMANENT_RESIDENT_CARD`, `MILITARY_ID`, `GLOBAL_ENTRY_CARD`, `TRIBAL_ID`, `CONSULAR_ID`, `FOREIGN_VOTER_CARD`, `REFUGEE_TRAVEL_DOCUMENT`, `DIPLOMATIC_ID`, `FORM_1040`, `FORM_W2`, `FORM_W9`, `FORM_1099_DIV`, `FORM_1099_INT`, `FORM_1099_B`, `FORM_1099_MISC`, `FORM_1099_R`, `FORM_K1_1065`, `FORM_K1_1120S`, `FORM_W8BEN`, `STATE_TAX_RETURN`, `PROPERTY_TAX_DOCUMENTS`, `ACCREDITED_INVESTOR_VERIFICATION`, `QUALIFIED_PURCHASER_VERIFICATION`, `AML_QUESTIONNAIRE`, `KYC_DOCUMENTATION`, `FATCA_CERTIFICATION`, `CRS_SELF_CERTIFICATION`, `OFAC_SCREENING`, `PEP_DISCLOSURE`, `BANK_STATEMENT`, `INVESTMENT_STATEMENT`, `NET_WORTH_STATEMENT`, `CREDIT_REPORT`, `EMPLOYMENT_VERIFICATION`, `INCOME_VERIFICATION`, `FINANCIAL_STATEMENT`, `UTILITY_BILL`, `LEASE_AGREEMENT`, `PROPERTY_DEED`, `MORTGAGE_STATEMENT`, `POWER_OF_ATTORNEY`, `NAME_CHANGE_DOCUMENT`, `MARRIAGE_CERTIFICATE`, `DIVORCE_DECREE`, `COURT_ORDER`, `SUBSCRIPTION_AGREEMENT`, `INVESTMENT_POLICY_STATEMENT`, `INVESTMENT_QUESTIONNAIRE`, `INVESTOR_ACCREDITATION`, `OTHER`

---

## Legal Entity Documents

Upload via: `POST /api/v1/legal-entity/{legalEntityId}/document`

**Request format (multipart/form-data):**
```
Content-Type: multipart/form-data

Parts:
  createRequest (application/json):
  {
    "title": "Smith Revocable Trust - Original Agreement",
    "description": "Trust agreement dated January 15, 2015",
    "documentType": "LEGAL_ENTITY",
    "contentType": "PDF",
    "documentSubType": "TRUST_AGREEMENT"
  }
  file: <binary file data>
```

### Trust Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Trust Agreement | `TRUST_AGREEMENT` | Filename contains "Trust" + "Agreement", "A&R", "Restated" |
| Trust Certification | `TRUST_CERTIFICATION` | Filename contains "Certification of Trust" |
| Trust Amendments | `TRUST_AMENDMENTS` | Filename contains "Amendment" + trust name |
| Revocable Trust | `REVOCABLE_TRUST_DOCUMENT` | Trust document where isRevocable = true |
| Irrevocable Trust | `IRREVOCABLE_TRUST_DOCUMENT` | Trust document where isRevocable = false |
| Trustee Certification | `TRUSTEE_CERTIFICATION` | Trustee identity/authority certification |
| Beneficiary Designation | `BENEFICIARY_DESIGNATION` | Beneficiary designation forms |
| Trust Asset Schedule | `TRUST_ASSET_SCHEDULE` | Schedule of trust assets, Exhibit A |

### LLC Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Articles of Organization | `ARTICLES_OF_ORGANIZATION` | Filename contains "Articles of Organization", "AOO" |
| Operating Agreement | `OPERATING_AGREEMENT` | Filename contains "Operating Agreement" |
| Certificate of Formation | `CERTIFICATE_OF_FORMATION` | Filename contains "Certificate of Formation" |
| Member Resolution | `MEMBER_RESOLUTION` | Filename contains "Resolution" + LLC context |
| Membership Schedule | `MEMBERSHIP_SCHEDULE` | Schedule of members and ownership interests |
| Manager Authorization | `MANAGER_AUTHORIZATION` | Manager authorization documents |

### Corporation Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Articles of Incorporation | `ARTICLES_OF_INCORPORATION` | Filename contains "Articles of Incorporation", "AOI" |
| Certificate of Incorporation | `CERTIFICATE_OF_INCORPORATION` | Filename contains "Certificate of Incorporation" |
| Corporate Bylaws | `CORPORATE_BYLAWS` | Filename contains "Bylaws" |
| Corporate Resolution | `CORPORATE_RESOLUTION` | Filename contains "Resolution" + corporate context |
| Board Minutes | `BOARD_MINUTES` | Board of directors meeting minutes |
| Shareholder Minutes | `SHAREHOLDER_MINUTES` | Shareholder meeting minutes |
| Stock Certificate | `STOCK_CERTIFICATE` | Stock certificates |
| Stock Ledger | `STOCK_LEDGER` | Stock transfer ledger |
| Shareholder Agreement | `SHAREHOLDER_AGREEMENT` | Shareholder agreement |
| Certificate of Good Standing | `CERTIFICATE_OF_GOOD_STANDING` | Good standing certificates |
| Annual Report | `ANNUAL_REPORT` | Corporate annual report filing |

### Partnership Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Partnership Agreement | `PARTNERSHIP_AGREEMENT` | Filename contains "Partnership Agreement" |
| Certificate of Limited Partnership | `CERTIFICATE_OF_LIMITED_PARTNERSHIP` | Certificate of LP formation |
| General Partner Authorization | `GENERAL_PARTNER_AUTHORIZATION` | GP authorization documents |
| Limited Partner Agreement | `LIMITED_PARTNER_AGREEMENT` | LP agreement |
| Partnership Interest Schedule | `PARTNERSHIP_INTEREST_SCHEDULE` | Schedule of partner interests |

### Foundation Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Foundation Charter | `FOUNDATION_CHARTER` | Foundation charter/articles |
| Foundation Bylaws | `FOUNDATION_BYLAWS` | Foundation bylaws |
| Board of Directors Roster | `BOARD_OF_DIRECTORS_ROSTER` | List of board members |
| Grant Policy | `GRANT_POLICY` | Grant-making policy document |

### Tax & Registration Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Tax Identification | `TAX_IDENTIFICATION` | Tax identification documents |
| EIN Letter | `EIN_CONFIRMATION` | Filename contains "EIN"; IRS letter assigning EIN |
| Business License | `BUSINESS_LICENSE` | Business license |
| Business Registration | `BUSINESS_REGISTRATION` | Filename contains "Sunbiz", "Secretary of State" filing |
| DBA Certificate | `DBA_CERTIFICATE` | Fictitious name registration |
| Professional License | `PROFESSIONAL_LICENSE` | Professional license |
| Form 1065 (Partnership) | `FORM_1065` | Partnership tax return |
| Form 1120 (C-Corp) | `FORM_1120` | C-Corporation tax return |
| Form 1120S (S-Corp) | `FORM_1120S` | S-Corporation tax return |
| Form 1041 (Trust/Estate) | `FORM_1041` | Fiduciary income tax return |
| K-1 (Partnership) | `FORM_K1_1065` | Schedule K-1 from partnership (Form 1065) |
| K-1 (S-Corp) | `FORM_K1_1120S` | Schedule K-1 from S-Corp (Form 1120S) |
| K-1 (Trust) | `FORM_K1_1041` | Schedule K-1 from trust/estate (Form 1041) |
| W-9 (entity) | `FORM_W9` | W-9 filed under entity name |
| W-8BEN-E | `FORM_W8BEN_E` | Certificate of foreign status for entities |
| State Tax Return (entity) | `STATE_TAX_RETURN` | State return for the entity |
| Property Tax Documents | `PROPERTY_TAX_DOCUMENTS` | Property tax records for entity-owned property |
| Tax Exempt Determination | `TAX_EXEMPT_DETERMINATION` | IRS determination letter |
| Form 990 | `FORM_990` | Exempt organization return |
| Form 990-PF | `FORM_990_PF` | Private foundation return |
| Charitable Registration | `CHARITABLE_REGISTRATION` | State charitable registration |
| Solicitation License | `SOLICITATION_LICENSE` | Charitable solicitation license |

### Compliance Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| AML Certification | `AML_CERTIFICATION` | AML certification |
| KYC Documentation | `KYC_DOCUMENTATION` | KYC documentation for entity |
| Beneficial Ownership Certification | `BENEFICIAL_OWNERSHIP_CERTIFICATION` | Beneficial ownership cert (FinCEN, CTA) |
| FATCA Certification | `FATCA_CERTIFICATION` | FATCA certification |
| CRS Entity Certification | `CRS_ENTITY_CERTIFICATION` | CRS self-certification for entities |
| OFAC Screening | `OFAC_SCREENING` | OFAC screening results |
| Accredited Investor Verification | `ACCREDITED_INVESTOR_VERIFICATION` | Accredited investor verification |
| Qualified Purchaser Verification | `QUALIFIED_PURCHASER_VERIFICATION` | Qualified purchaser verification |

### Financial Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Audited Financials | `AUDITED_FINANCIALS` | Audited financial statements |
| Balance Sheet | `BALANCE_SHEET` | Balance sheet |
| Income Statement | `INCOME_STATEMENT` | Income statement / P&L |
| Cash Flow Statement | `CASH_FLOW_STATEMENT` | Cash flow statement |
| Entity Bank Statement | `BANK_STATEMENT` | Bank statement in entity name |
| Entity Investment Statement | `INVESTMENT_STATEMENT` | Investment statement in entity name |
| Business Credit Report | `BUSINESS_CREDIT_REPORT` | Business credit report |

### Legal & Authorization Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Power of Attorney | `POWER_OF_ATTORNEY` | POA for the entity |
| Authorized Signer Documentation | `AUTHORIZED_SIGNER_DOCUMENTATION` | Authorized signer documentation |
| Legal Opinion | `LEGAL_OPINION` | Legal opinion letter |
| Incumbency Certificate | `INCUMBENCY_CERTIFICATE` | Incumbency certificate |
| Corporate Seal | `CORPORATE_SEAL` | Corporate seal impression |
| Subscription Agreement | `SUBSCRIPTION_AGREEMENT` | Fund subscription docs |
| Investment Policy Statement | `INVESTMENT_POLICY_STATEMENT` | IPS for entity |
| Investor Questionnaire | `INVESTOR_QUESTIONNAIRE` | Investor questionnaire |
| PPM Acknowledgment | `PPM_ACKNOWLEDGMENT` | PPM acknowledgment |
| Other | `OTHER` | Other legal entity document |

### All Valid DocumentTypeLegalEntity Values (80 values)

`TRUST_AGREEMENT`, `TRUST_CERTIFICATION`, `TRUST_AMENDMENTS`, `REVOCABLE_TRUST_DOCUMENT`, `IRREVOCABLE_TRUST_DOCUMENT`, `TRUSTEE_CERTIFICATION`, `BENEFICIARY_DESIGNATION`, `TRUST_ASSET_SCHEDULE`, `ARTICLES_OF_INCORPORATION`, `CERTIFICATE_OF_INCORPORATION`, `CORPORATE_BYLAWS`, `CORPORATE_RESOLUTION`, `BOARD_MINUTES`, `SHAREHOLDER_MINUTES`, `STOCK_CERTIFICATE`, `STOCK_LEDGER`, `SHAREHOLDER_AGREEMENT`, `CERTIFICATE_OF_GOOD_STANDING`, `ANNUAL_REPORT`, `ARTICLES_OF_ORGANIZATION`, `OPERATING_AGREEMENT`, `CERTIFICATE_OF_FORMATION`, `MEMBER_RESOLUTION`, `MEMBERSHIP_SCHEDULE`, `MANAGER_AUTHORIZATION`, `PARTNERSHIP_AGREEMENT`, `CERTIFICATE_OF_LIMITED_PARTNERSHIP`, `GENERAL_PARTNER_AUTHORIZATION`, `LIMITED_PARTNER_AGREEMENT`, `PARTNERSHIP_INTEREST_SCHEDULE`, `FOUNDATION_CHARTER`, `FOUNDATION_BYLAWS`, `BOARD_OF_DIRECTORS_ROSTER`, `GRANT_POLICY`, `TAX_IDENTIFICATION`, `BUSINESS_LICENSE`, `BUSINESS_REGISTRATION`, `EIN_CONFIRMATION`, `DBA_CERTIFICATE`, `PROFESSIONAL_LICENSE`, `FORM_1065`, `FORM_1120`, `FORM_1120S`, `FORM_1041`, `FORM_K1_1065`, `FORM_K1_1120S`, `FORM_K1_1041`, `FORM_W9`, `FORM_W8BEN_E`, `STATE_TAX_RETURN`, `PROPERTY_TAX_DOCUMENTS`, `TAX_EXEMPT_DETERMINATION`, `FORM_990`, `FORM_990_PF`, `CHARITABLE_REGISTRATION`, `SOLICITATION_LICENSE`, `AML_CERTIFICATION`, `KYC_DOCUMENTATION`, `BENEFICIAL_OWNERSHIP_CERTIFICATION`, `FATCA_CERTIFICATION`, `CRS_ENTITY_CERTIFICATION`, `OFAC_SCREENING`, `ACCREDITED_INVESTOR_VERIFICATION`, `QUALIFIED_PURCHASER_VERIFICATION`, `AUDITED_FINANCIALS`, `BALANCE_SHEET`, `INCOME_STATEMENT`, `CASH_FLOW_STATEMENT`, `BANK_STATEMENT`, `INVESTMENT_STATEMENT`, `BUSINESS_CREDIT_REPORT`, `POWER_OF_ATTORNEY`, `AUTHORIZED_SIGNER_DOCUMENTATION`, `LEGAL_OPINION`, `INCUMBENCY_CERTIFICATE`, `CORPORATE_SEAL`, `SUBSCRIPTION_AGREEMENT`, `INVESTMENT_POLICY_STATEMENT`, `INVESTOR_QUESTIONNAIRE`, `PPM_ACKNOWLEDGMENT`, `OTHER`

---

## AccountFinancial Documents

Upload via: `POST /api/v1/account-financial/{accountId}/document`

**Request format (multipart/form-data):**
```
Content-Type: multipart/form-data

Parts:
  createRequest (application/json):
  {
    "title": "Morgan Stanley Account Application",
    "description": "New account opening application",
    "documentType": "ACCOUNT_FINANCIAL",
    "contentType": "PDF",
    "documentSubType": "ACCOUNT_APPLICATION"
  }
  file: <binary file data>
```

| Document Type | documentSubType | How to Identify |
|---|---|---|
| Account Agreement | `ACCOUNT_AGREEMENT` | Account agreement documents |
| Account Application | `ACCOUNT_APPLICATION` | New account forms, custodian applications |
| Transfer Form | `TRANSFER_FORM` | ACAT forms, transfer documents |
| Beneficiary Designation | `BENEFICIARY_DESIGNATION` | TOD/beneficiary forms |
| Investment Policy Statement | `INVESTMENT_POLICY_STATEMENT` | IPS documents |
| Fee Schedule | `FEE_SCHEDULE` | Advisory fee agreements |
| Custody Agreement | `CUSTODY_AGREEMENT` | Custodial agreement |
| Brokerage Statement | `BROKERAGE_STATEMENT` | Brokerage account statement |
| Margin Agreement | `MARGIN_AGREEMENT` | Margin agreement |
| Options Agreement | `OPTIONS_AGREEMENT` | Options trading agreement |
| Trade Confirmation | `TRADE_CONFIRMATION` | Trade confirmation |
| IRA Adoption Agreement | `IRA_ADOPTION_AGREEMENT` | IRA custodial agreements |
| 401k Plan Document | `PLAN_DOCUMENT_401K` | 401k/403b plan documents |
| RMD Notice | `RMD_NOTICE` | Required minimum distribution notice |
| Rollover Certification | `ROLLOVER_CERTIFICATION` | Rollover certification |
| Subscription Agreement | `SUBSCRIPTION_AGREEMENT` | Fund subscription docs |

### All Valid DocumentTypeAccountFinancial Values (92 values)

`ACCOUNT_AGREEMENT`, `ACCOUNT_APPLICATION`, `TRANSFER_FORM`, `BENEFICIARY_DESIGNATION`, `PASSPORT`, `DRIVERS_LICENSE`, `ENHANCED_DRIVERS_LICENSE`, `NATIONAL_ID`, `STATE_ID`, `BIRTH_CERTIFICATE`, `SOCIAL_SECURITY_CARD`, `PERMANENT_RESIDENT_CARD`, `MILITARY_ID`, `GLOBAL_ENTRY_CARD`, `TRIBAL_ID`, `CONSULAR_ID`, `CITIZENSHIP_CERTIFICATE`, `CERTIFICATE_OF_NATURALIZATION`, `FOREIGN_VOTER_CARD`, `REFUGEE_TRAVEL_DOCUMENT`, `DIPLOMATIC_ID`, `TAX_IDENTIFICATION`, `ADDRESS_PROOF`, `UTILITY_BILL`, `CREDIT_REPORT`, `EMPLOYMENT_VERIFICATION`, `INCOME_VERIFICATION`, `BANK_STATEMENT`, `VOIDED_CHECK`, `DIRECT_DEPOSIT_FORM`, `WIRE_INSTRUCTIONS`, `ACH_AUTHORIZATION`, `CUSTODIAL_STATEMENT`, `CUSTODY_AGREEMENT`, `FEE_SCHEDULE`, `BROKERAGE_STATEMENT`, `MARGIN_AGREEMENT`, `OPTIONS_AGREEMENT`, `TRADE_CONFIRMATION`, `FORM_1099`, `FORM_1099_DIV`, `FORM_1099_INT`, `FORM_1099_B`, `FORM_1099_MISC`, `FORM_1099_R`, `FORM_K1_1065`, `FORM_K1_1120S`, `FORM_K1_1041`, `FORM_W2`, `FORM_W2G`, `FORM_5498`, `FORM_8949`, `TAX_SUMMARY`, `IRA_ADOPTION_AGREEMENT`, `PLAN_DOCUMENT_401K`, `RMD_NOTICE`, `ROLLOVER_CERTIFICATION`, `POWER_OF_ATTORNEY`, `AUTHORIZED_SIGNER`, `CORPORATE_RESOLUTION`, `TRUST_AGREEMENT`, `TRUST_CERTIFICATION`, `TRUST_AMENDMENTS`, `REVOCABLE_TRUST_DOCUMENT`, `IRREVOCABLE_TRUST_DOCUMENT`, `TRUSTEE_CERTIFICATION`, `ARTICLES_OF_INCORPORATION`, `CERTIFICATE_OF_INCORPORATION`, `OPERATING_AGREEMENT`, `PARTNERSHIP_AGREEMENT`, `ARTICLES_OF_ORGANIZATION`, `BUSINESS_LICENSE`, `BUSINESS_REGISTRATION`, `CERTIFICATE_OF_GOOD_STANDING`, `BYLAWS`, `EIN_CONFIRMATION`, `AML_DOCUMENTATION`, `KYC_DOCUMENTATION`, `FATCA_CRS_FORM`, `FORM_W9`, `FORM_W8BEN`, `FINANCIAL_STATEMENT`, `INVESTMENT_POLICY_STATEMENT`, `TAX_EXEMPT_DETERMINATION`, `FORM_990`, `CHARITABLE_REGISTRATION`, `PROBATE_DOCUMENT`, `DEATH_CERTIFICATE`, `EXECUTOR_APPOINTMENT`, `CORRESPONDENCE`, `NOTIFICATION`, `OTHER`

---

## Tangible Asset Documents

Upload via: `POST /api/v1/tangible-asset/{assetId}/document`

**Request format (multipart/form-data):**
```
Content-Type: multipart/form-data

Parts:
  createRequest (application/json):
  {
    "title": "Vacation Home - Deed",
    "description": "Warranty deed for Aspen property",
    "documentType": "TANGIBLE_ASSET",
    "contentType": "PDF",
    "documentSubType": "DEED"
  }
  file: <binary file data>
```

### Ownership Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Title Document | `TITLE` | Vehicle title, property title |
| Property Deed | `DEED` | Filename contains "Deed", "Warranty Deed" |
| Registration | `REGISTRATION` | Vehicle/vessel registration |
| Bill of Sale | `BILL_OF_SALE` | Purchase documentation |
| Purchase Receipt | `PURCHASE_RECEIPT` | Purchase receipt |
| Certificate of Ownership | `CERTIFICATE_OF_OWNERSHIP` | Ownership certificate |
| Transfer Document | `TRANSFER_DOCUMENT` | Ownership transfer documentation |

### Valuation Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Appraisal Report | `APPRAISAL` | Professional appraisal/valuation |
| Valuation Report | `VALUATION_REPORT` | Formal valuation report |
| Tax Assessment | `TAX_ASSESSMENT` | Tax assessment value |
| Comparable Analysis | `COMPARABLE_ANALYSIS` | Comparable market analysis |
| Broker Price Opinion | `BROKER_PRICE_OPINION` | BPO / broker valuation |
| Fair Market Value Determination | `FMV_DETERMINATION` | FMV determination |

### Insurance Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Insurance Policy | `INSURANCE_POLICY` | Insurance policy document for the asset |
| Insurance Claim | `INSURANCE_CLAIM` | Insurance claim documentation |
| Coverage Certificate | `COVERAGE_CERTIFICATE` | Certificate of coverage |
| Insurance Rider | `INSURANCE_RIDER` | Policy rider/endorsement |
| Insurance Declaration | `INSURANCE_DECLARATION` | Dec page from insurance policy |
| Insurance Binder | `INSURANCE_BINDER` | Temporary insurance binder |
| Proof of Insurance | `PROOF_OF_INSURANCE` | Proof of insurance |
| Insurance Renewal | `INSURANCE_RENEWAL` | Insurance renewal notice |
| Insurance Cancellation | `INSURANCE_CANCELLATION` | Insurance cancellation notice |

### Maintenance Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Service Record | `SERVICE_RECORD` | Service/maintenance record |
| Inspection Report | `INSPECTION_REPORT` | Inspection report |
| Warranty | `WARRANTY` | Warranty documentation |
| Extended Warranty | `EXTENDED_WARRANTY` | Extended warranty |
| Repair Invoice | `REPAIR_INVOICE` | Repair invoice |
| Repair Estimate | `REPAIR_ESTIMATE` | Repair estimate |
| Maintenance Log | `MAINTENANCE_LOG` | Maintenance log |
| Restoration Document | `RESTORATION_DOCUMENT` | Restoration documentation |
| Conservation Report | `CONSERVATION_REPORT` | Art/item conservation report |

### Legal Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Lien | `LIEN` | Lien filing against the asset |
| Lien Release | `LIEN_RELEASE` | Lien release/satisfaction |
| Loan Agreement | `LOAN_AGREEMENT` | Loan secured by the asset |
| Mortgage | `MORTGAGE` | Mortgage agreement, payoff statement |
| Lease Agreement | `LEASE_AGREEMENT` | Lease agreement |
| Rental Agreement | `RENTAL_AGREEMENT` | Rental agreement |
| Legal Agreement | `LEGAL_AGREEMENT` | General legal agreement |
| Power of Attorney | `POWER_OF_ATTORNEY` | POA for the asset |
| Trust Document | `TRUST_DOCUMENT` | Trust document related to the asset |
| Bill of Lading | `BILL_OF_LADING` | Shipping bill of lading |
| Customs Declaration | `CUSTOMS_DECLARATION` | Customs declaration |
| Import/Export Document | `IMPORT_EXPORT_DOCUMENT` | Import/export documentation |

### Tax Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Property Tax | `PROPERTY_TAX` | Property tax bill/assessment |
| Depreciation Schedule | `DEPRECIATION_SCHEDULE` | Depreciation schedule |
| Tax Basis | `TAX_BASIS` | Tax basis documentation |
| 1031 Exchange | `EXCHANGE_1031` | 1031 exchange documentation |
| Gift Tax Document | `GIFT_TAX_DOCUMENT` | Gift tax documentation |
| Estate Tax Document | `ESTATE_TAX_DOCUMENT` | Estate tax documentation |
| Charitable Donation Receipt | `CHARITABLE_DONATION_RECEIPT` | Charitable donation receipt |

### Provenance Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Certificate of Authenticity | `CERTIFICATE_OF_AUTHENTICITY` | For art, watches, collectibles |
| Certificate of Origin | `CERTIFICATE_OF_ORIGIN` | Origin certification |
| Authentication Report | `AUTHENTICATION_REPORT` | Authentication report |
| Provenance History | `PROVENANCE_HISTORY` | Ownership history chain |
| Auction Documentation | `AUCTION_DOCUMENTATION` | Auction records |
| Condition Report | `CONDITION_REPORT` | Condition assessment |
| Catalogue Raisonne | `CATALOGUE_RAISONNE` | Catalogue raisonne reference |
| Exhibition History | `EXHIBITION_HISTORY` | Exhibition records |
| Literature Reference | `LITERATURE_REFERENCE` | Published literature references |
| Expert Opinion | `EXPERT_OPINION` | Expert opinion letter |

### Image Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Primary Photo | `PRIMARY_PHOTO` | Main photo of the asset |
| Detail Photo | `DETAIL_PHOTO` | Detail/close-up photo |
| Condition Photo | `CONDITION_PHOTO` | Photo documenting condition |
| Restoration Photo | `RESTORATION_PHOTO` | Photo of restoration work |
| Damage Photo | `DAMAGE_PHOTO` | Photo documenting damage |
| Photo | `PHOTO` | General photo of the asset |

### Vehicle Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Vehicle History Report | `VEHICLE_HISTORY_REPORT` | Carfax or similar |
| Emissions Certificate | `EMISSIONS_CERTIFICATE` | Emissions test certificate |
| Safety Inspection | `SAFETY_INSPECTION` | Safety inspection report |
| Airworthiness Certificate | `AIRWORTHINESS_CERTIFICATE` | Aircraft airworthiness certificate |
| Aircraft Logs | `AIRCRAFT_LOGS` | Aircraft maintenance logs |
| Marine Survey | `MARINE_SURVEY` | Marine survey report |
| Coast Guard Documentation | `COAST_GUARD_DOCUMENTATION` | USCG documentation |

### Real Property Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Survey | `SURVEY` | Property survey |
| Title Insurance | `TITLE_INSURANCE` | Title insurance policy |
| Home Inspection | `HOME_INSPECTION` | Home inspection report |
| Pest Inspection | `PEST_INSPECTION` | Pest/termite inspection |
| Environmental Assessment | `ENVIRONMENTAL_ASSESSMENT` | Environmental assessment |
| HOA Documents | `HOA_DOCUMENTS` | HOA docs, CC&Rs |
| Zoning Document | `ZONING_DOCUMENT` | Zoning documentation |
| Building Permit | `BUILDING_PERMIT` | Building permit |
| Certificate of Occupancy | `CERTIFICATE_OF_OCCUPANCY` | Certificate of occupancy |
| Floor Plans | `FLOOR_PLANS` | Floor plans/blueprints |

### Wine Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Cellar Inventory | `CELLAR_INVENTORY` | Wine cellar inventory |
| Storage Records | `STORAGE_RECORDS` | Wine storage records |
| Wine Provenance | `WINE_PROVENANCE` | Wine provenance documentation |

### Collectible Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Grading Certificate | `GRADING_CERTIFICATE` | Grading certificate (coins, cards, etc.) |
| Encapsulation Certificate | `ENCAPSULATION_CERTIFICATE` | Encapsulation certificate |

### Estate Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Beneficiary Designation | `BENEFICIARY_DESIGNATION` | Beneficiary designation for the asset |
| Will Excerpt | `WILL_EXCERPT` | Will excerpt referencing the asset |
| Donation Intent | `DONATION_INTENT` | Donation intent letter |
| Estate Appraisal | `ESTATE_APPRAISAL` | Estate appraisal |

### General Documents
| Document Type | documentSubType | How to Identify |
|---|---|---|
| Receipt | `RECEIPT` | General receipt |
| Correspondence | `CORRESPONDENCE` | General correspondence |
| Notes | `NOTES` | Notes related to the asset |
| Other | `OTHER` | Other tangible asset document |

### All Valid DocumentTypeTangibleAsset Values (97 values)

**Ownership:** `TITLE`, `DEED`, `REGISTRATION`, `BILL_OF_SALE`, `PURCHASE_RECEIPT`, `CERTIFICATE_OF_OWNERSHIP`, `TRANSFER_DOCUMENT`
**Valuation:** `APPRAISAL`, `VALUATION_REPORT`, `TAX_ASSESSMENT`, `COMPARABLE_ANALYSIS`, `BROKER_PRICE_OPINION`, `FMV_DETERMINATION`
**Insurance:** `INSURANCE_POLICY`, `INSURANCE_CLAIM`, `COVERAGE_CERTIFICATE`, `INSURANCE_RIDER`, `INSURANCE_DECLARATION`, `INSURANCE_BINDER`, `PROOF_OF_INSURANCE`, `INSURANCE_RENEWAL`, `INSURANCE_CANCELLATION`
**Maintenance:** `SERVICE_RECORD`, `INSPECTION_REPORT`, `WARRANTY`, `EXTENDED_WARRANTY`, `REPAIR_INVOICE`, `REPAIR_ESTIMATE`, `MAINTENANCE_LOG`, `RESTORATION_DOCUMENT`, `CONSERVATION_REPORT`
**Legal:** `LIEN`, `LIEN_RELEASE`, `LOAN_AGREEMENT`, `MORTGAGE`, `LEASE_AGREEMENT`, `RENTAL_AGREEMENT`, `LEGAL_AGREEMENT`, `POWER_OF_ATTORNEY`, `TRUST_DOCUMENT`, `BILL_OF_LADING`, `CUSTOMS_DECLARATION`, `IMPORT_EXPORT_DOCUMENT`
**Tax:** `PROPERTY_TAX`, `DEPRECIATION_SCHEDULE`, `TAX_BASIS`, `EXCHANGE_1031`, `GIFT_TAX_DOCUMENT`, `ESTATE_TAX_DOCUMENT`, `CHARITABLE_DONATION_RECEIPT`
**Provenance:** `CERTIFICATE_OF_AUTHENTICITY`, `CERTIFICATE_OF_ORIGIN`, `AUTHENTICATION_REPORT`, `PROVENANCE_HISTORY`, `AUCTION_DOCUMENTATION`, `CONDITION_REPORT`, `CATALOGUE_RAISONNE`, `EXHIBITION_HISTORY`, `LITERATURE_REFERENCE`, `EXPERT_OPINION`
**Image:** `PRIMARY_PHOTO`, `DETAIL_PHOTO`, `CONDITION_PHOTO`, `RESTORATION_PHOTO`, `DAMAGE_PHOTO`, `PHOTO`
**Vehicle:** `VEHICLE_HISTORY_REPORT`, `EMISSIONS_CERTIFICATE`, `SAFETY_INSPECTION`, `AIRWORTHINESS_CERTIFICATE`, `AIRCRAFT_LOGS`, `MARINE_SURVEY`, `COAST_GUARD_DOCUMENTATION`
**Real Property:** `SURVEY`, `TITLE_INSURANCE`, `HOME_INSPECTION`, `PEST_INSPECTION`, `ENVIRONMENTAL_ASSESSMENT`, `HOA_DOCUMENTS`, `ZONING_DOCUMENT`, `BUILDING_PERMIT`, `CERTIFICATE_OF_OCCUPANCY`, `FLOOR_PLANS`
**Wine:** `CELLAR_INVENTORY`, `STORAGE_RECORDS`, `WINE_PROVENANCE`
**Collectible:** `GRADING_CERTIFICATE`, `ENCAPSULATION_CERTIFICATE`
**Estate:** `BENEFICIARY_DESIGNATION`, `WILL_EXCERPT`, `DONATION_INTENT`, `ESTATE_APPRAISAL`
**General:** `RECEIPT`, `CORRESPONDENCE`, `NOTES`, `OTHER`

---

## Insurance Policy Documents

Insurance policies are standalone entities. Upload documents to the insurance policy entity.

Upload via: `POST /api/v1/insurance-policy/{policyId}/document`

**Request format (multipart/form-data):**
```
Content-Type: multipart/form-data

Parts:
  createRequest (application/json):
  {
    "title": "Northwestern Mutual - Whole Life Policy",
    "description": "Whole life insurance policy #NWM-12345",
    "documentType": "INSURANCE_POLICY",
    "contentType": "PDF",
    "documentSubType": "POLICY_DECLARATION"
  }
  file: <binary file data>
```

| Document Type | documentSubType | How to Identify | Association |
|---|---|---|---|
| Life insurance policy/declaration | `POLICY_DECLARATION` | Filename contains "Life", "Policy Declaration", "Death Benefit" | Primary (POST/PATCH insurance-policy) |
| Full policy contract | `POLICY_CONTRACT` | Filename contains "Policy Contract", "Full Policy" | Primary |
| Policy amendment/endorsement | `POLICY_AMENDMENT` | Filename contains "Amendment", "Endorsement", "Rider Change" | Primary |
| Policy renewal notice | `POLICY_RENEWAL` | Filename contains "Renewal", "Renewal Notice" | Primary |
| Schedule of benefits | `POLICY_SCHEDULE` | Filename contains "Schedule of Benefits", "Coverage Schedule" | Primary |
| Umbrella policy declaration | `POLICY_DECLARATION` | Filename contains "Umbrella", "Excess Liability" | Primary |
| LTC policy | `POLICY_DECLARATION` | Filename contains "Long Term Care", "LTC" | Primary |
| Disability policy | `POLICY_DECLARATION` | Filename contains "Disability", "Income Protection" | Primary |
| Health insurance card/policy | `POLICY_DECLARATION` | Filename contains "Health", "Medical", "Insurance Card" | Primary |
| Auto insurance declaration | `POLICY_DECLARATION` | Filename contains "Auto Insurance", "Vehicle Insurance" | Primary |
| Insurance application | `APPLICATION` | Filename contains "Insurance Application", "Application for" | Primary |
| Underwriting report | `UNDERWRITING_REPORT` | Filename contains "Underwriting", "Risk Assessment" | Primary |
| Medical exam results | `MEDICAL_EXAM` | Filename contains "Medical Exam", "Paramedical" | Primary |
| Medical records | `MEDICAL_RECORDS` | Filename contains "Medical Records" | Primary |
| Beneficiary designation | `BENEFICIARY_DESIGNATION` | Filename contains "Beneficiary Designation" in insurance context | Primary (also creates BENEFICIARY relationship) |
| Beneficiary change | `BENEFICIARY_CHANGE` | Filename contains "Beneficiary Change", "Change of Beneficiary" | Primary |
| Premium notice/billing | `PREMIUM_NOTICE` | Filename contains "Premium", "Payment Due", "Billing" for insurance | Secondary (updates annualPremium) |
| Payment receipt | `PAYMENT_RECEIPT` | Filename contains "Payment Receipt", "Premium Payment" | Secondary |
| Billing statement | `BILLING_STATEMENT` | Filename contains "Billing Statement", "Premium Statement" | Secondary |
| Annual policy statement | `ANNUAL_STATEMENT` | Filename contains "Annual Statement", "Year-End Statement" | Primary |
| Policy illustration | `ILLUSTRATION` | Filename contains "Illustration", "Projection", "Hypothetical" | Primary |
| In-force ledger | `IN_FORCE_LEDGER` | Filename contains "In-Force", "In Force Ledger" | Primary |
| Claim form | `CLAIM_FORM` | Filename contains "Claim Form", "Notice of Claim" | Primary |
| Claim correspondence | `CLAIM_CORRESPONDENCE` | Filename contains "Claim Letter", "Claims Correspondence" | Primary |
| Claim settlement | `CLAIM_SETTLEMENT` | Filename contains "Claim Settlement", "Settlement Agreement" | Primary |
| Power of Attorney | `POWER_OF_ATTORNEY` | Filename contains "POA" in insurance context | Primary |
| Trust assignment | `TRUST_ASSIGNMENT` | Filename contains "Trust Assignment", "Assignment to Trust" in insurance context | Primary |
| Irrevocable assignment | `IRREVOCABLE_ASSIGNMENT` | Filename contains "Irrevocable Assignment" in insurance context | Primary |
| Ownership change | `OWNERSHIP_CHANGE` | Filename contains "Ownership Change", "Transfer of Ownership" in insurance context | Primary |
| General correspondence | `CORRESPONDENCE` | General insurance correspondence | Secondary |
| Other insurance document | `OTHER` | Insurance-related document not matching above | Primary |

### Special Rules for Insurance Policies
- **Policy owner**: Also associate with the Individual who owns the policy (create OWNERSHIP relationship)
- **Insured person**: Also associate with the Individual who is insured (create INSURED relationship if different from owner)
- **Beneficiary designation forms**: Create BENEFICIARY relationships from named beneficiaries to the policy
- **Multi-insured policies** (e.g., survivorship life): Associate with all insured individuals

### All Valid DocumentTypeInsurancePolicy Values (26 values)

`POLICY_DECLARATION`, `POLICY_CONTRACT`, `POLICY_AMENDMENT`, `POLICY_RENEWAL`, `POLICY_SCHEDULE`, `APPLICATION`, `UNDERWRITING_REPORT`, `MEDICAL_EXAM`, `MEDICAL_RECORDS`, `CLAIM_FORM`, `CLAIM_CORRESPONDENCE`, `CLAIM_SETTLEMENT`, `PREMIUM_NOTICE`, `PAYMENT_RECEIPT`, `BILLING_STATEMENT`, `BENEFICIARY_DESIGNATION`, `BENEFICIARY_CHANGE`, `POWER_OF_ATTORNEY`, `TRUST_ASSIGNMENT`, `IRREVOCABLE_ASSIGNMENT`, `OWNERSHIP_CHANGE`, `ANNUAL_STATEMENT`, `ILLUSTRATION`, `IN_FORCE_LEDGER`, `CORRESPONDENCE`, `OTHER`

---

## Liability Documents

Liabilities are standalone entities. Upload documents to the liability entity.

Upload via: `POST /api/v1/liability/{liabilityId}/document`

**Request format (multipart/form-data):**
```
Content-Type: multipart/form-data

Parts:
  createRequest (application/json):
  {
    "title": "Chase Mortgage Statement - March 2026",
    "description": "Monthly mortgage statement for 123 Main St",
    "documentType": "LIABILITY",
    "contentType": "PDF",
    "documentSubType": "LOAN_STATEMENT"
  }
  file: <binary file data>
```

| Document Type | documentSubType | How to Identify | Association |
|---|---|---|---|
| Loan agreement | `LOAN_AGREEMENT` | Filename contains "Loan Agreement", "Credit Agreement" | Primary (POST/PATCH liability) |
| Promissory note | `PROMISSORY_NOTE` | Filename contains "Promissory Note", "Note" in loan context | Primary |
| Mortgage deed | `MORTGAGE_DEED` | Filename contains "Mortgage Deed", "Deed of Trust" | Primary |
| Collateral agreement | `COLLATERAL_AGREEMENT` | Filename contains "Collateral Agreement", "Security Agreement", "Pledge Agreement" | Primary |
| Line of credit agreement | `LINE_OF_CREDIT_AGREEMENT` | Filename contains "Line of Credit", "LOC Agreement", "HELOC Agreement" | Primary |
| Refinance documents | `REFINANCE_DOCUMENTS` | Filename contains "Refinance", "Refi", "Loan Modification" | Primary |
| Amortization schedule | `AMORTIZATION_SCHEDULE` | Filename contains "Amortization", "Payment Schedule", "Repayment Schedule" | Primary |
| Payoff statement | `PAYOFF_STATEMENT` | Filename contains "Payoff Statement", "Payoff Quote", "Payoff Letter" | Primary |
| Account/loan statement | `ACCOUNT_STATEMENT` | Filename contains "Mortgage Statement", "Loan Statement", "HELOC Statement", "Student Loan Statement", "Auto Loan Statement", credit card issuer + "Statement", "Margin Statement" | Primary |
| Form 1098 | `FORM_1098` | Filename contains "1098", "Mortgage Interest Statement" | Primary (updates interestPaidYtd/interestPaidPriorYear) |
| Insurance certificate | `INSURANCE_CERTIFICATE` | Filename contains "Insurance Certificate", "Proof of Insurance" in loan/collateral context | Primary |
| General correspondence | `CORRESPONDENCE` | General lender correspondence not matching above | Secondary |
| Other liability document | `OTHER` | Liability-related document not matching above | Primary |

### Special Rules for Liabilities
- **Borrower(s)**: Also associate with the Individual(s) who are borrowers (create OWNERSHIP relationship from Individual to Liability)
- **Co-borrower**: If a co-borrower is identified, create a second OWNERSHIP relationship
- **Secured liabilities**: If a liability references a tangible asset (e.g., mortgage on a property), note the collateral in `collateralDescription`
- **Form 1098**: Extract interestPaidYtd and interestPaidPriorYear from this document to update liability fields

### All Valid DocumentTypeLiability Values (13 values)

`LOAN_AGREEMENT`, `PROMISSORY_NOTE`, `MORTGAGE_DEED`, `COLLATERAL_AGREEMENT`, `LINE_OF_CREDIT_AGREEMENT`, `REFINANCE_DOCUMENTS`, `AMORTIZATION_SCHEDULE`, `PAYOFF_STATEMENT`, `ACCOUNT_STATEMENT`, `FORM_1098`, `INSURANCE_CERTIFICATE`, `CORRESPONDENCE`, `OTHER`

---

## Estate Planning Documents (Individual PATCH)

Estate planning documents associate with the Individual and update the nested `estatePlanning` object via PATCH. These are NOT separate entities.

Upload via: `POST /api/v1/individual/{individualId}/document`

| Document Type | documentSubType | How to Identify | Updates |
|---|---|---|---|
| Last will and testament | `OTHER` | Filename contains "Will", "Last Will", "Testament" | `estatePlanning.will` section |
| Healthcare directive/living will | `OTHER` | Filename contains "AHCD", "Healthcare Directive", "Living Will", "Advance Directive" | `estatePlanning.healthcare` section |
| Power of attorney (financial) | `POWER_OF_ATTORNEY` | Filename contains "POA", "Power of Attorney", "GPOA" -- financial context | `estatePlanning.financialPoa` section |
| Guardianship designation | `OTHER` | Filename contains "Guardianship", "Guardian Designation" | `estatePlanning.guardianship` section |
| Prenuptial/postnuptial agreement | `OTHER` | Filename contains "Prenup", "Prenuptial", "Postnuptial", "Marital Agreement" | `estatePlanning.maritalAgreement` section |
| Estate planning review/summary | `OTHER` | Filename contains "Estate Review", "Estate Plan Summary", "Planning Summary" | `estatePlanning.estateReview` section |

### Special Rules for Estate Planning Documents
- These documents associate with the Individual (testator/principal), not with a separate entity
- Data extracted updates the `estatePlanning` nested object on Individual via PATCH
- Related persons identified (e.g., named executor, guardian, POA agent) should be matched and linked via entity relationships

---

## Charitable & Philanthropic Documents

Charitable documents associate with either the Legal Entity (for DAFs, foundations, charitable trusts) or the Individual (for personal philanthropic data).

### Legal Entity Charitable Documents

Upload via: `POST /api/v1/legal-entity/{legalEntityId}/document`

| Document Type | documentSubType | How to Identify | Updates |
|---|---|---|---|
| Donor-advised fund statement | `OTHER` | Filename contains "DAF", "Donor-Advised", "Donor Advised" + entity name | `charitableDetails` (DAF section) |
| Private foundation tax return (990-PF) | `FORM_990_PF` | Filename contains "990-PF", "990PF", "Private Foundation Return" | `charitableDetails` (foundation section) |
| Charitable trust agreement | `TRUST_AGREEMENT` | Filename contains "Charitable Trust", "CRT", "CLT", "CRAT", "CRUT" | `charitableDetails` (trust section) |

### Individual Philanthropic Documents

Upload via: `POST /api/v1/individual/{individualId}/document`

| Document Type | documentSubType | How to Identify | Updates |
|---|---|---|---|
| Donation receipts/acknowledgments | `OTHER` | Filename contains "Donation Receipt", "Charitable Receipt", "Acknowledgment" | `philanthropicProfile` fields |
| Charitable pledge agreement | `OTHER` | Filename contains "Pledge Agreement", "Charitable Pledge" | `philanthropicProfile` (hasCharitablePledge, totalOutstandingPledges) |

### Special Rules for Charitable Documents
- **Legal entity charitable details** are nested on the LegalEntity and updated via PATCH
- **Individual philanthropic profile** is nested on the Individual and updated via PATCH
- **990-PF**: Rich source for foundation details -- extract total assets, total grants, grant recipients
- **DAF statements**: Extract sponsoring organization, account balance, grant history

---

## Engagement Documents (EntityRelationship PATCH)

Engagement documents associate with the professional relationship between entities (e.g., advisor-client, attorney-client). These update the `engagementDetails` nested object on the EntityRelationship.

Upload documents to the primary entity in the relationship (typically the Individual or Household being served), but extract data to update the EntityRelationship via PATCH.

| Document Type | documentSubType | How to Identify | Updates |
|---|---|---|---|
| Engagement letter (advisor/attorney/CPA) | `OTHER` | Filename contains "Engagement Letter", "Advisory Agreement", "Retainer" | `engagementDetails` on professional relationship |
| Fee schedule | `FEE_SCHEDULE` | Filename contains "Fee Schedule", "Fee Agreement" in professional context | `engagementDetails` fee fields |
| Service agreement | `OTHER` | Filename contains "Service Agreement", "Scope of Services" | `engagementDetails.scopeOfServices` |

### Special Rules for Engagement Documents
- **Match the relationship first**: Identify both parties (e.g., advisor Contact + client Individual), find or create the EntityRelationship, then PATCH `engagementDetails`
- **Engagement letters** often name both parties, effective dates, and fee structures -- extract all
- **Fee schedules** update fee-related fields on the engagementDetails nested object

---

## Multi-Entity Documents

Some documents contain information about multiple entities. Rules:

| Document Type | Primary Association | Also Extract For |
|---|---|---|
| Onboarding Sheet | Primary Individual | All entities mentioned |
| Estate Planning Summary | Primary Individual | All trusts, entities mentioned |
| Estate Flowchart/Diagram | Primary Individual | Relationship mapping only |
| Meeting Notes | Primary Individual | Contextual info for all |
| Insurance Summary (multi-asset) | Primary Individual | Each asset's insurance details |
| Insurance Summary (multi-policy) | Primary Individual | Each insurance policy entity |
| LLC Summary Document | Primary Individual (if overview) or first LLC | All LLCs mentioned |
| Loan consolidation document | Primary Individual | Each liability entity |
| Net worth statement | Primary Individual | Liabilities, insurance policies, tangible assets mentioned |

For multi-entity documents, upload the document to the primary entity and extract
data for all mentioned entities.

---

## contentType Mapping

Map file extensions to `contentType` enum values:
| Extension | contentType |
|---|---|
| .pdf | `PDF` |
| .docx | `DOCX` |
| .doc | `DOC` |
| .xlsx | `XLSX` |
| .xls | `XLS` |
| .pptx | `PPTX` |
| .ppt | `PPT` |
| .txt | `TXT` |
| .csv | `CSV` |
| .json | `JSON` |
| .xml | `XML` |
| .html | `HTML` |
| .jpg, .jpeg | `JPG` |
| .png | `PNG` |
| .gif | `GIF` |
| .zip | `ZIP` |
| .mp4 | `MP4` |
| .mp3 | `MP3` |

---

## Document Metadata Model

Each entity type has its own `DocumentType{EntityName}` Java enum with a `displayName` and `category` field. When creating documents via the API, the `documentSubType` field must be a valid value from the corresponding enum:

| Entity Type | Enum Class | Example Values |
|---|---|---|
| Individual | `DocumentTypeIndividual` | DRIVERS_LICENSE, PASSPORT, FORM_1040, FORM_W2, POWER_OF_ATTORNEY |
| Legal Entity | `DocumentTypeLegalEntity` | TRUST_AGREEMENT, OPERATING_AGREEMENT, ARTICLES_OF_INCORPORATION, EIN_CONFIRMATION |
| Account Financial | `DocumentTypeAccountFinancial` | ACCOUNT_APPLICATION, ACCOUNT_AGREEMENT, BENEFICIARY_DESIGNATION |
| Tangible Asset | `DocumentTypeTangibleAsset` | DEED, TITLE, APPRAISAL, BILL_OF_SALE, CERTIFICATE_OF_AUTHENTICITY |
| Insurance Policy | `DocumentTypeInsurancePolicy` | POLICY_DECLARATION, POLICY_CONTRACT, BENEFICIARY_DESIGNATION, ANNUAL_STATEMENT |
| Liability | `DocumentTypeLiability` | LOAN_AGREEMENT, ACCOUNT_STATEMENT, MORTGAGE_DEED, FORM_1098 |

> **Note:** Household does NOT have a DocumentType enum. There is no document upload endpoint for households. Associate household-level documents with the primary individual or legal entity instead.

**To discover all valid values at runtime**, call the entity's enum endpoint:
- `GET /api/v1/insurance-policy/enums/document-types`
- `GET /api/v1/liability/enums/document-types`
- `GET /api/v1/account-financial/enums/document-types`
- `GET /api/v1/{entity}/enums/document-types` (where entity is `insurance-policy`, `liability`, `account-financial`, or other document-supporting entity)

Each enum value includes `displayName` (human-readable) and `category` (logical grouping) for classification.
