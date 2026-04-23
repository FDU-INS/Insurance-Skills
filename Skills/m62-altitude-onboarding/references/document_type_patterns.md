# Document Type Classification Patterns

Use these patterns to classify documents found in household folders. Classification is based
on filename patterns, folder location, and content inspection.

## Classification Rules

### By Folder Name (highest priority)
| Folder Pattern | Document Type |
|---|---|
| `Trust*`, `Estate*`, `Trust & Estate` | TRUST_ESTATE |
| `LLC*`, `Entity*`, `Formation*` | ENTITY_FORMATION |
| `Tax*`, `1099*`, `K-1*`, `K1*` | TAX |
| `Insurance*` | INSURANCE |
| `Identification*`, `ID*` | IDENTIFICATION |
| `Statements*`, `JPM*`, `Schwab*`, `Morgan*` | FINANCIAL_STATEMENT |
| `Meeting*`, `Notes*` | MEETING_NOTES |
| `Presentation*` | PRESENTATION |
| `Onboarding*` | ONBOARDING |

### By Filename Pattern
| Filename Pattern | Document Type | Entity Implications |
|---|---|---|
| `*Driver*License*`, `*DL*`, `*dl*` | ID_DRIVERS_LICENSE | Individual: name, DOB, address, DL number |
| `*Passport*`, `*passport*` | ID_PASSPORT | Individual: name, DOB, nationality, passport number |
| `*Trust*dtd*`, `*Revocable Trust*`, `*Irrevocable Trust*`, `*Living Trust*` | TRUST_AGREEMENT | Legal Entity (TRUST): all trust details, Individual: grantor, trustee, beneficiary |
| `*Will*`, `*Last Will*`, `*Testament*` | WILL | Individual: testator, executor, beneficiaries |
| `*Power of Attorney*`, `*POA*`, `*GPOA*` | POWER_OF_ATTORNEY | Individual: principal, agent |
| `*Health Care*`, `*AHCD*`, `*Advance*Directive*` | HEALTHCARE_DIRECTIVE | Individual: principal, healthcare agent |
| `*HIPAA*` | HIPAA_AUTHORIZATION | Individual: principal, authorized persons |
| `*Articles of Organization*`, `*AOO*` | LLC_FORMATION | Legal Entity (LLC): name, formation date, state, members |
| `*Operating Agreement*` | LLC_OPERATING_AGREEMENT | Legal Entity (LLC): management type, members, managers |
| `*Articles of Incorporation*`, `*AOI*` | CORP_FORMATION | Legal Entity (CORPORATION): name, formation date, state |
| `*Sunbiz*`, `*SUNBIZ*` | STATE_FILING | Legal Entity: registration details, registered agent |
| `*EIN*`, `*ein*` | EIN_LETTER | Legal Entity: EIN, legal name |
| `*W-2*`, `*w2*` | TAX_W2 | Individual: employer, wages, SSN |
| `*1099*` | TAX_1099 | Individual/Entity: income, account info |
| `*K-1*`, `*K1*` | TAX_K1 | Legal Entity: partnership/LLC income, Individual: partner info |
| `*Tax Return*`, `*1040*` | TAX_RETURN | Individual: comprehensive financial, SSN, filing status |
| `*Warranty Deed*`, `*Deed*` | PROPERTY_DEED | Tangible Asset (REAL_PROPERTY): property details, owner |
| `*Insurance*`, `*Policy*`, `*SOI*` | INSURANCE_POLICY | Insurance details for individual or asset |
| `*Payoff*`, `*Loan*`, `*Mortgage*`, `*Note*` | LOAN_DOCUMENT | Liability info linked to asset or entity |
| `*Account*Application*`, `*New Account*` | ACCOUNT_APPLICATION | AccountFinancial: type, owner, custodian |
| `*Monthly Statement*`, `*Quarterly Statement*`, `*Statement*`, `*stmt*`, `*STMT*` | ACCOUNT_STATEMENT | AccountFinancial: holdings, balances; Account info, holdings, balances |
| `*Custodian*`, `*Transfer*Form*` | CUSTODIAN_DOCUMENT | AccountFinancial: custodian details |
| `*Beneficiary*Designation*` | BENEFICIARY_DESIGNATION | AccountFinancial: TOD beneficiaries |
| `*IRA*`, `*401k*`, `*Retirement*` | RETIREMENT_DOCUMENT | AccountFinancial: retirement details |
| `*Onboarding*`, `*Client Information*` | ONBOARDING_SHEET | All entity types: comprehensive client data |
| `*Summary*`, `*Overview*` | SUMMARY_DOCUMENT | Mixed: overview of entities and relationships |
| `*Meeting Notes*`, `*Mtg Notes*` | MEETING_NOTES | Contextual info, action items |
| `*Presentation*`, `*.pptx` | PRESENTATION | Contextual info, financial summaries |
| `*Amendment*` | AMENDMENT | Legal Entity: changes to formation docs |
| `*Resolution*` | RESOLUTION | Legal Entity: corporate/LLC resolutions |
| `*Personal Guaranty*` | GUARANTY | Individual: guarantor info linked to loan |
| `*Assignment*` | ASSET_ASSIGNMENT | Asset transfers between entities |
| `*Certification of Trust*` | TRUST_CERTIFICATION | Trust: summary of key trust terms |
| `*Flowchart*`, `*Estate Chart*`, `*EP Diagram*` | ESTATE_CHART | Relationship mapping, entity hierarchy |
| `*Property Tax*`, `*PT *` | PROPERTY_TAX | Tangible Asset (REAL_PROPERTY): assessed value, parcel info |
| `*W9*`, `*w9*` | TAX_W9 | Entity: tax ID, classification, legal name |

### Image Files (.jpg, .jpeg, .png)
Images in household folders are typically:
- **Driver's licenses** — look for filename patterns or folder context
- **Passports** — similar
- **Family information sheets** — handwritten or scanned forms
- **Property photos** — less common in these folders

**Use Claude's Read tool** — Claude can see images natively and extract text/data from them.

### Email Files (.eml, .msg)
Emails often contain account confirmations, policy updates, advisor correspondence, and forwarded documents:
- **`.eml` files**: Parse with Python's built-in `email` module — extract From/To/Date/Subject, body text, and save attachments to process separately
- **`.msg` files**: Skip unless the user specifically requests — these are Outlook proprietary format and require `extract-msg` or similar library
- Look for: account numbers, policy numbers, balance updates, contact info, meeting summaries
- **Attachments**: Save to temp directory and classify/process each as its native file type (PDF, DOCX, etc.)

### PDF and Document Files
- **PDFs**: Use Claude's Read tool to read PDF files directly. Claude can read both text and scanned PDFs natively.
- **Word docs (.docx)**: Use the platform's `DOCX_CMD` from the Cross-Platform Setup in SKILL.md. Fallback chain: `textutil -convert txt file.docx` (macOS) → `pandoc file.docx -t plain` (cross-platform) → write a `docx_read.py` script (see SKILL.md → Standard Document Extraction for the exact script; install via `pip install python-docx`). Then read the text output with Claude's Read tool. **Do NOT use `python -c "..."` with embedded newlines — it breaks on Windows cmd and PowerShell. Always write to a `.py` file and run it.**
- **Spreadsheets (.xlsx)**: Write an `xlsx_read.py` script (see SKILL.md → Standard Document Extraction) and run `python xlsx_read.py "file.xlsx"`. Use `python` (not `python3`) — the Cross-Platform Setup in SKILL.md resolves the right command for the host OS.

## Extraction Priority

### Tier 1 — Core Identity & Formation (process first)
These documents establish the fundamental entities and their attributes:
- Onboarding sheets (most comprehensive single source)
- Driver's licenses / passports (authoritative for individual identity)
- Trust agreements (establish trust entities and roles)
- LLC operating agreements / articles of organization
- Articles of incorporation
- EIN letters (authoritative for tax IDs)
- Account applications (establish account entities and owners)

### Tier 1.5 — IRS Tax Forms (NEVER SKIP)
These are compact, single-page documents that are extremely data-dense. They establish
entity identity, ownership percentages, liability details, and financial flows. Always
process ALL of these regardless of household size:
- **Form 1098** (Mortgage Interest) — reveals: lender, outstanding balance, monthly payment, origination date, property address, borrowers. Creates: Liability (MORTGAGE) + TangibleAsset (REAL_PROPERTY) + OWNERSHIP relationships. A single 1098 produces 1 liability, 1 tangible asset, and 2+ relationships.
- **Schedule K-1 (Form 1065)** — reveals: LLC/partnership name, EIN, partner name, SSN, ownership %, profit/loss/capital sharing, capital account. Creates: LegalEntity + MEMBER/PARTNER relationships with exact percentages. K-1s are the AUTHORITATIVE source for ownership percentages.
- **Schedule K-1 (Form 1120S)** — same as above for S-Corps. Reveals shareholder ownership %.
- **Schedule K-1 (Form 1041)** — trust/estate K-1. Reveals beneficiary name + income allocation.
- **Form 1099-DIV / 1099-INT / 1099-B** — reveals: custodian/payer name, account number, income amounts. Cross-validates account existence and custodian relationships.
- **Form 1099-R** — retirement distributions. Reveals IRA/401k custodian and account info.
- **Form W-2** — reveals: employer name, EIN, wages, employee SSN. Creates/validates employment relationship.
- **Form 1099-MISC / 1099-NEC** — reveals: payer relationships, independent contractor income.
- **Form 5498** — IRA contribution info. Reveals IRA custodian, account value, contribution amounts.

**Why Tier 1.5?** These forms are structured IRS documents with exact field positions — extraction is near-perfect. They contain authoritative tax IDs (SSN/EIN), exact dollar amounts, and legal entity names that cross-validate data from other documents. Missing a K-1 means missing an ownership relationship. Missing a 1098 means missing a $1M+ liability.

### Tier 2 — Financial & Tax
These add financial context and verify identity:
- Personal tax returns / Form 1040 (SSN verification, filing status, income, occupations, dependents)
- Entity tax returns / Form 1065, 1120, 1120S, 1041 (entity financials, partner/shareholder lists)
- Insurance policy declarations (coverage details, asset values)
- Property tax bills (real property values and addresses)
- Account statements (account details, holdings, balances, advisor info)
- Beneficiary designations (account beneficiary updates)

### Tier 3 — Supplementary
These add context and fill gaps:
- Financial statements (account details, holdings)
- Meeting notes (relationship context, preferences)
- Presentations (financial summaries, planning info)
- Estate planning flowcharts (entity relationship maps)
- Warranty deeds (property ownership chain)

### Tier 4 — Low Priority (skip unless specifically needed)
- Duplicate files (in "zDupes" or "Copy of" prefix)
- Payment receipts and confirmations
- Correspondence (.msg files)
- Basis statements (unless verifying cost basis)

## Professional Contact Extraction

Professional contacts (attorneys, CPAs, advisors, insurance agents) are typically extracted FROM other documents rather than having their own dedicated document type. Look for:
- **Trust agreements**: drafting attorney name, law firm
- **Tax returns**: preparer name, firm, PTIN
- **Insurance policies**: agent name, agency
- **Estate planning summaries**: attorney, CPA references
- **Engagement letters**: full contact details

Create Contact entities for these professionals and link via ADVISOR/ACCOUNTANT/ATTORNEY relationships.

## Document-Type Extraction Checklists

For each document type, use these checklists to ensure complete extraction. After reading a document, verify every checkbox item was captured or explicitly marked as "not found."

### ONBOARDING_SHEET Checklist
Onboarding sheets are the richest single source. Extract EVERY item:
- [ ] **All named individuals** — first name, last name, DOB, SSN
- [ ] **All named entities** — LLC names, S-Corp names, Trust names, with entity type
- [ ] **Entity-to-entity relationships** — "X is the managing member of Y" → MEMBER relationship
- [ ] **Ownership structure chains** — "controlled 50/50 by A and B" → two OWNERSHIP relationships at 50%
- [ ] **Entity type precision** — S-Corp is `entityType: "CORPORATION"` (not LLC); LLC is `entityType: "LLC"`
- [ ] **All email addresses** with owner attribution
- [ ] **All phone numbers** with owner attribution
- [ ] **Shared address** — all individuals at same address get the same `addressLegal`
- [ ] **All named professionals** — attorneys, CPAs, CFOs, advisors — each becomes a Contact
- [ ] **Professional role specificity** — "employment attorney" vs "corporate attorney" vs "real estate attorney" → separate Contacts with specific `jobTitle`
- [ ] **Professional firm names** — go in Contact `biography` field (NOT companyName)
- [ ] **Absence data** — "estate planning not completed" → `estatePlanning.will.hasWill: false`; "no trusts" → note no TRUST entities
- [ ] **Account types mentioned** — checking, savings, IRAs, 401Ks, 529s, mortgage → future AccountFinancial entities

### TAX_RETURN (Form 1040) Checklist
Personal tax returns contain authoritative identity + financial data:
- [ ] **Full legal names** — from header, including middle names/initials
- [ ] **SSNs** — taxpayer and spouse (page 1, top right)
- [ ] **Home address** — authoritative address (page 1)
- [ ] **Filing status** — Single/MFJ/MFS/HOH/QSS → if MFJ, create SPOUSE relationship
- [ ] **Occupations** — both taxpayer and spouse (page 2, Sign Here section)
- [ ] **Dependents** — names, SSNs, relationships → Individual entities + PARENT/CHILD relationships; if blank, note "no dependents"
- [ ] **W-2 income** — line 1a, total wages → `financialProfile.annualIncome` approximation
- [ ] **Schedule 8/business income** — indicates business entity ownership
- [ ] **Named tax preparer** — name, firm, phone, PTIN, EIN → Contact with `jobTitle: "CPA"` + ACCOUNTANT relationship
- [ ] **Third party designee** — name, phone → may be the same CPA or a different contact
- [ ] **Digital assets question** — "Yes" indicates crypto/digital holdings

### TAX_RETURN (Form 1040) — Large PDF Deep Dive Checklist
For tax returns over 20 pages, use the Page Index Scan (see SKILL.md Phase 3) to find these
MANDATORY pages. Do not stop at the first 5 pages — the richest data is buried deeper.

**ALWAYS find and read these pages (in addition to the basic 1040 checklist above):**
- [ ] **Schedule E, Page 2 — Passthrough Income Summary** — Lists EVERY entity (LLC, LLP, S-Corp, Trust, Estate) from which the taxpayer receives K-1 income. Each line has: entity name, EIN, entity type (PARTNERSHIP/S CORPORATION/ESTATE OR TRUST), and income amounts. This is the single most important page for entity discovery.
- [ ] **Passthrough detail pages** (usually titled "2024 Income from Passthroughs") — Expanded view per entity with ordinary income, capital gains, SE earnings, retirement plan contributions, W-2 wages. If SE earnings are shown, taxpayer is a PARTNER (not employee).
- [ ] **K-1 summary page** — Aggregated K-1 data across all entities: total interest income, charitable contributions, retirement plans, SE earnings, Section 199A W-2 wages.
- [ ] **Schedule H (Household Employment)** — Present if family has nanny, housekeeper, or other domestic staff. Shows: employer name (usually spouse), employer EIN, total cash wages paid, state employment details. Wages of $50K+ indicate full-time domestic help.
- [ ] **Schedule A (Itemized Deductions)** — Mortgage interest (confirms mortgage exists), charitable contributions (signals philanthropic activity), state/local taxes (confirms residency states).
- [ ] **Schedule C (Sole Proprietorship)** — If present, indicates a business entity not yet captured.
- [ ] **Form 8949 / Schedule D** — Capital gains transactions. May reveal brokerage accounts not yet identified.
- [ ] **State return cover pages** — Multi-state filing (3+ states) indicates business interests, rental properties, or entities in multiple jurisdictions. Each state with a return is a flag for investigation.

### TAX_K1 (Schedule K-1) Checklist
K-1s are the AUTHORITATIVE source for ownership percentages. NEVER skip these:
- [ ] **Partnership/LLC name and EIN** — confirms LegalEntity identity (definitive match by EIN)
- [ ] **Entity address** — from header → LegalEntity `addressPrincipal`
- [ ] **Partner/member name and SSN/EIN** — confirms ownership relationship
- [ ] **Partner type** — general partner vs limited partner → MEMBER (general) vs PARTNER (limited) relationship
- [ ] **Ownership percentage** — for `percentage` field on relationship (Box J/K beginning + ending %)
- [ ] **Profit/loss/capital sharing ratios** — beginning and ending of year (may differ from ownership %)
- [ ] **Partner's share of income** — ordinary income/loss (Box 1), rental income (Box 2), interest (Box 5), dividends (Box 6a/6b)
- [ ] **Partner's capital account** — beginning balance, contributions, withdrawals, ending balance (Schedule L)
- [ ] **If partner is an entity** — EIN in partner ID field means the partner is a LegalEntity, not an Individual → entity-to-entity relationship
- [ ] **Number of K-1s attached** — indicates total number of partners/members in the entity

### TAX_1098 (Form 1098 Mortgage Interest) Checklist
1098s reveal mortgages, property collateral, and lender relationships. A single 1098 produces a Liability + TangibleAsset + multiple relationships. NEVER skip these:
- [ ] **Lender name** (Box header: Recipient's name) → `lenderName`
- [ ] **Lender TIN** — contextual
- [ ] **Borrower name(s)** (Payer's name) — may list both spouses → OWNERSHIP relationships for each
- [ ] **Borrower SSN** — cross-validates Individual identity
- [ ] **Mortgage interest paid** (Box 1) → `interestPaidYtd`; confirms `isInterestDeductible: true`, `interestDeductionType: "MORTGAGE_INTEREST"`
- [ ] **Outstanding principal** (Box 2) → `currentBalance` (as of Jan 1 of tax year)
- [ ] **Mortgage origination date** (Box 3) → `originationDate`
- [ ] **Ending principal balance** (Mortgage information section) → most current `currentBalance` + `balanceAsOfDate`
- [ ] **Total current payment** → `monthlyPayment`
- [ ] **Account number** → `accountNumber`
- [ ] **Property address** (Box 8) → `collateralDescription`, `isSecured: true`; ALSO creates a TangibleAsset (REAL_PROPERTY) if property address matches home address → `assetType: "PRIMARY_RESIDENCE"`
- [ ] **Number of properties** (Box 9) — if >1, there are multiple mortgaged properties
- [ ] **Real estate taxes paid** (Box 10) — contextual property tax data
- [ ] **Cross-reference**: If Box 8 property address = Individual's `addressLegal`, this is PRIMARY_RESIDENCE. If different, it's VACATION_HOME or RENTAL_PROPERTY.
- [ ] **Link liability to asset**: Set `linkedTangibleAssetId` on the Liability to point to the TangibleAsset once created.

### TAX_1099 (Form 1099-DIV / 1099-INT / 1099-B / 1099-R) Checklist
1099s confirm account existence and custodian relationships:
- [ ] **Payer/custodian name** — confirms AccountFinancial custodian (or creates new one)
- [ ] **Payer TIN** — cross-validates custodian identity
- [ ] **Recipient name and SSN/EIN** — confirms account owner
- [ ] **Account number** — `accountNumber` on AccountFinancial (definitive match key)
- [ ] **Income amounts** — contextual (dividends, interest, capital gains, distributions)
- [ ] **For 1099-R specifically**: Distribution code reveals IRA type (traditional, Roth, etc.) → AccountFinancial `subCategory`

### TAX_W2 (Form W-2) Checklist
- [ ] **Employee name and SSN** — confirms Individual identity
- [ ] **Employer name and EIN** — may create LegalEntity if employer is client's own business
- [ ] **Employer address** — LegalEntity `addressPrincipal`
- [ ] **Wages** (Box 1) → `financialProfile.annualIncome`
- [ ] **State/local wages** — confirms state of employment
- [ ] **Retirement plan checkbox** (Box 13) — indicates 401k/pension participation → potential AccountFinancial
- [ ] **If employer = one of the household's LLCs/Corps**: Creates or validates EMPLOYEE relationship

### ENTITY_TAX_RETURN (Form 1065 / 1120 / 1120S / 1041) Checklist
Entity-level tax returns validate legal entities and reveal financial health:
- [ ] **Entity name and EIN** — definitive LegalEntity identification
- [ ] **Entity address** → `addressPrincipal`
- [ ] **Entity type from form** — 1065=Partnership/LLC, 1120=C-Corp, 1120S=S-Corp, 1041=Trust/Estate
- [ ] **Number of partners/shareholders** — indicates entity complexity
- [ ] **Gross receipts** — contextual business size
- [ ] **Ordinary income/loss** — contextual
- [ ] **Officer/partner compensation** — from Schedule K or separate schedule
- [ ] **Preparer name, firm, phone, PTIN** → Contact + ACCOUNTANT relationship to entity
- [ ] **Attached K-1s** — each K-1 reveals a partner/member → process each separately using TAX_K1 checklist

### ACCOUNT_STATEMENT Checklist
Account statements establish financial accounts and their attributes:
- [ ] **Account number** — exact, including dashes/formatting (definitive match key)
- [ ] **Account title/registration** — exact legal name (e.g., "MICHAEL ERIC TUSK & LINDSAY GIBSON TUSK JT TEN")
- [ ] **Account type from registration** — JT TEN = Joint Tenants (subCategory: `JOINT_WITH_RIGHTS_OF_SURVIVORSHIP`), JT TIC = Joint Tenants in Common, TTEE = Trust, IRA, etc.
- [ ] **Custodian/institution name** — Morgan Stanley, Schwab, Fidelity, etc.
- [ ] **Statement period and date** — for context
- [ ] **Total market value** — ending balance (contextual, not stored as field)
- [ ] **Asset allocation summary** — 100% cash is notable, indicates uninvested
- [ ] **Financial advisor name/team** — from cover page → Contact entity + ADVISOR relationship
- [ ] **Advisor phone/branch address** — Contact fields
- [ ] **Account holders' full legal names** — cross-validates with other documents (may reveal middle names)
- [ ] **Mailing address on statement** — cross-validates home address

### LLC_OPERATING_AGREEMENT / LLC_FORMATION Checklist
- [ ] **Legal name** (exact, including "LLC" suffix)
- [ ] **DBA / FKA names** — former names go in `dbaName`
- [ ] **Formation date** → `formationDate`
- [ ] **Formation state** → `jurisdiction` + `incorporationState`
- [ ] **EIN** → `taxId`
- [ ] **Management type** — member-managed vs manager-managed → `llcManagementType`
- [ ] **All members with ownership percentages** → MEMBER relationships with `percentage`
- [ ] **Managing member** — especially if it's ANOTHER ENTITY (creates entity-to-entity relationship)
- [ ] **Registered agent** — name and address
- [ ] **Principal office address** → `addressPrincipal`

### TRUST_AGREEMENT Checklist
- [ ] **Trust name** (exact, including date if in name)
- [ ] **Grantor(s)** — name(s) → Individual entities + GRANTOR relationships
- [ ] **Trustee(s)** — name(s) → TRUSTEE relationships
- [ ] **Successor trustee(s)** → SUCCESSOR_TRUSTEE relationships
- [ ] **Beneficiaries** — primary and contingent → BENEFICIARY relationships
- [ ] **Revocable vs Irrevocable** → `trust.isRevocable`
- [ ] **Situs/jurisdiction** → `trust.situs`
- [ ] **Governing law** → `trust.governingLaw`
- [ ] **Date of trust** → `formationDate`
- [ ] **Tax ID / EIN** (irrevocable trusts have their own)
- [ ] **Spendthrift provision** → `trust.hasSpendthriftProvision`
- [ ] **Pour-over provisions** → `trust.hasPourOverProvision`, `trust.pourOverTrustName`
- [ ] **Distribution provisions** — HEMS, discretionary, mandatory → `trust.distributionProvisionsText`
- [ ] **Drafting attorney** — name, firm → Contact + ATTORNEY relationship

### INSURANCE_POLICY Checklist
- [ ] **Policy number** (definitive match key)
- [ ] **Carrier name** → `carrierName`
- [ ] **Policy type/category** → `policyCategory` (LIFE/UMBRELLA/LTC/DISABILITY/HEALTH/AUTO)
- [ ] **Life sub-type** → `lifePolicyType` (TERM/WHOLE_LIFE/UNIVERSAL/etc.)
- [ ] **Coverage/death benefit amount** → `coverageAmount`, `deathBenefit`
- [ ] **Premium amount and frequency** → `annualPremium`, `paymentFrequency`
- [ ] **Cash value** (for permanent life) → `cashValue`, `cashValueAsOfDate`
- [ ] **Policy owner** → OWNERSHIP relationship (may be ILIT, not the insured)
- [ ] **Insured person(s)** → INSURED relationship
- [ ] **Beneficiaries** — primary and contingent → BENEFICIARY relationships
- [ ] **Effective/expiration dates** → `effectiveDate`, `expirationDate`
- [ ] **Agent name** → Contact + INSURANCE_AGENT relationship

### LOAN_DOCUMENT / MORTGAGE Checklist
- [ ] **Lender name** → `lenderName`
- [ ] **Account number** → `accountNumber`
- [ ] **Loan type** → `liabilityType` (MORTGAGE/HOME_EQUITY_LOC/etc.)
- [ ] **Original balance** → `originalBalance`
- [ ] **Current balance** → `currentBalance`
- [ ] **Interest rate and type** → `interestRate`, `interestRateType` (FIXED/VARIABLE/HYBRID)
- [ ] **Monthly payment** → `monthlyPayment`
- [ ] **Origination and maturity dates** → `originationDate`, `maturityDate`
- [ ] **Collateral description** → `collateralDescription`, `linkedTangibleAssetId` (link to property)
- [ ] **Borrower(s)** → OWNERSHIP relationship(s)
- [ ] **Tax deductibility** → `isInterestDeductible`, `interestDeductionType`

### PROPERTY_DEED / PROPERTY_TAX Checklist
- [ ] **Property address** → TangibleAsset `name` + `realPropertyDetails`
- [ ] **Parcel/APN number** → `serialOrIdentifier`
- [ ] **Owner name(s)** → OWNERSHIP relationships
- [ ] **Assessed value / purchase price** → `currentValue` or `purchasePrice`
- [ ] **Property type** → `assetType` (PRIMARY_RESIDENCE/VACATION_HOME/RENTAL_PROPERTY/etc.)

### ID_DRIVERS_LICENSE / ID_PASSPORT Checklist
- [ ] **Full legal name** (including middle name)
- [ ] **Date of birth**
- [ ] **Address** (DL only)
- [ ] **DL/passport number** — contextual, not stored as primary field
- [ ] **Photo** — for Individual photo upload if supported
- [ ] **Expiration date** — contextual

## Cross-Document Inference Rules

After extracting from ALL documents, run these inference checks:

### Relationship Inference
| Signal | Inferred Relationship |
|--------|----------------------|
| Joint 1040 filing (MFJ) | SPOUSE (symmetric) between taxpayer and spouse |
| 1040 Dependents section lists children | PARENT→CHILD for BOTH parents (taxpayer + spouse) to each child |
| 1040 confirms family unit | OWNERSHIP: HOUSEHOLD → each Individual (adults 50%, children 0%). Direction: household is SOURCE, individual is TARGET. Do NOT use MEMBER for household links. |
| No dependents on 1040 | No PARENT/CHILD relationships needed (note absence) |
| K-1 with partner name + % | MEMBER or PARTNER relationship with `percentage` |
| K-1 shows self-employment (SE) earnings | Taxpayer is PARTNER (not EMPLOYEE) at the entity — SE income = partnership draw |
| K-1 from an Estate or Trust entity | Taxpayer is BENEFICIARY of that trust — receiving trust income distributions |
| "Managing member of X" | MEMBER relationship from manager entity → managed entity |
| Joint account title "JT TEN" | Both individuals → AccountFinancial via OWNERSHIP (50%/50%) |
| Account title "TTEES UAD [date]" | Creates a LegalEntity (TRUST) with `formationDate` from the UAD date, both named trustees get TRUSTEE + GRANTOR relationships (for living trusts) |
| "PLEDGED TO ML LENDER" or "pledged as collateral for Loan Management Account #" | Creates a Liability (PLEDGED_ASSET_LINE) with the referenced loan account number. Set `isSecured: true` and note the collateral accounts. |
| "FBO [child name]" on 529/UTMA account | PARENT is custodian/participant → OWNERSHIP relationship from parent to account |
| Trust names grantor | GRANTOR relationship from individual → trust LegalEntity |
| "TTEE" in account registration | Account owned by trust LegalEntity, not individual. `accountCategory: "ENTITY"` |
| Insurance policy owner ≠ insured | Separate OWNERSHIP and INSURED relationships |
| Schedule H (Household Employment) | Household has domestic staff — Lauren/Spencer is employer. Note the household employer EIN. |
| Schedule E Passthrough page lists entity names | Each named entity becomes a LegalEntity with EIN. Entity TYPE field tells you: PARTNERSHIP=LLP/LLC, S CORPORATION=CORPORATION, ESTATE OR TRUST=TRUST |
| 1040 page 2 "Your occupation" / "Spouse's occupation" | Set `Individual.occupation` for both. If occupation matches an entity name (e.g., "ATTORNEY" + law firm LLP), confirms the relationship type (PARTNER, not EMPLOYEE). |
| Multi-state tax filings (CA, CT, IL, etc.) | Indicates business interests or properties in those states — may signal additional entities not yet found |

### Multi-Hop Ownership Chains
When documents reveal entity hierarchies, create ALL intermediate relationships:
```
"Tusk Management is the managing member of Quince & Co, LLC"
"Tusk Management is an S-Corp, controlled 50/50 by Lindsay and Michael"
→ Creates:
  1. Lindsay → Tusk Management (OWNERSHIP, 50%)
  2. Michael → Tusk Management (OWNERSHIP, 50%)
  3. Tusk Management → Quince & Co (MEMBER, managing member)
  4. Tusk Management entityType = CORPORATION (S-Corp)
```

### Absence-as-Data
Explicitly record when expected data is ABSENT:
- No estate planning documents → `estatePlanning.will.hasWill: false` (or note "estate planning not started")
- No dependents on 1040 → note "no dependent children identified"
- No insurance policies found → note "no insurance coverage identified — flag for review"
- No trusts despite high net worth → note "no trust entities — potential planning gap"

### Name Enrichment Cross-Validation
When the same person appears in multiple documents, merge the MOST COMPLETE version:
- Onboarding sheet: "Lindsay Tusk" (first + last only)
- 1040: "LINDSAY TUSK" with SSN 591-22-6607
- Morgan Stanley statement: "LINDSAY GIBSON TUSK" (reveals middle name)
→ Final: `firstName: "Lindsay"`, `middleName: "Gibson"`, `lastName: "Tusk"`

## Special Handling

### Password-Protected PDFs
Some tax returns note a password in the filename (e.g., "pass 701431"). Note these but don't
attempt to decrypt — flag for the user.

### Scanned PDFs
PDFs from document management systems (prefix like "1IV4961-" or "1K57760-") are often
scanned images. Use Claude's vision capabilities to read them.

### Duplicate Detection
Files prefixed with "Copy of" or in folders named "zDupes" are duplicates. Skip them unless
the original is not found.
