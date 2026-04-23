# BIAN v13 — Core Class Detail

Detailed definitions for 45 core BO classes,
including inheritance, abstraction, and attribute lists.

## AccessArrangement

> An arrangement that allows or restricts the access to a service or product, channel or device through a specific access point Description: https://en.wikipedia.org/wiki/Access-control_list

**Extends:** Device Access Arrangement

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
PointOfAccessType | Pointofaccesstypevalues |  |  | 
AccessCredentialMethod | Authenticationmethodtypevalues |  |  | 

## Account

> A measuring state on which movements in value or amounts of assets, rights and obligations are registered.

**Extends:** Nostro Account

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
AccountStatus | Accountstatus |  |  | A characteristic of account which refers to the LifecycleStatus of account like opened, closed, blocked, etc.
AccountIdentification | Accountidentification |  |  | The identifier of account like Account Number.
AccountDate | Accountdatetime |  |  | A characteristic of account which refers to LifecycleDate of account (e.g., ClosingDate, OpeningDate, LiveDate, etc.)
AccountType | Accounttypevalues |  |  | Specifies the category of account like payment account, loan account, cash account, securities account, etc.
AccountPurpose | Text |  |  | 
AccountBalance | Accountbalance |  |  | The state of the obligations managed on the account, the result of all entries on the account.
AccountCurrency | Accountcurrency |  |  | 
AccountDescription | Text |  |  | A detailed explanation or commentary of account.
AccountName | Name |  |  | The name of account The account name is the name or names of the account owner(s) represented at an account level, as displayed by the ASPSP's online channels.

## Address

> A specific designation or description of a location, typically used for specifying the location or destination of something or someone

**Extends:** Phone Address

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
AddressType | Addresstypevalues |  |  | 
LocationReference | Location |  |  | 

## Agreement

> A formal or informal common understanding between two or more (legal competent) parties concerning one or more subject matters expressed in a set of arrangements, terms and conditions.

**Extends:** Savings Account Agreement

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
AgreementSignedDate | Date |  |  | Date on which the agreement was signed by all parties.
AgreementType | Agreementtypevalues |  | yes | Specifies the category of agreement.
AgreementValidityPeriod | Datetimeperiod |  |  | Period during which the agreement is valid
AgreementVersion | Text |  |  | 
AgreementStatus | Agreementstatus |  |  | A characteristic of agreement which refers to the LifecycleStatus of agreement (e.g., potential, offered, confirmed, completed, signed, terminated).
AgreementSubjectMatter | Text |  |  | 
AgreementIdentification | Identifier |  |  | The identifier of agreement like Agreement Number, Contract Number, Contract Registration Number, etc.
AgreementDate | Datetime |  |  | A characteristic of agreement which refers to 1) LifecycleDate of agreement (e.g., SignedDate, TerminatedDate, FulfilledDate) OR 2) ArrangedDate of agreement (e.g., StartingDate, EndingDate, ValidityP
AgreementDescription | Text |  |  | 

## Arrangement

> An agreed commitment to perform actions that meet obligations under an agreement

**Extends:** Savings Account Arrangement

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
ArrangementAction | Action |  |  | 
ArrangementStartDate | Datetime |  |  | 
ArrangementEndDate | Datetime |  |  | 
ArrangementStatus | Arrangementstatus |  |  | A characteristic of arrangement which refers to the LifecycleStatus of arrangement (e.g., requested, proposed, offered, accepted, cancelled, terminated, fulfilled, etc.)
ArrangementSubjectMatter | Subject |  |  | 
Arrangementtype | Arrangementtypevalues |  |  | 

## Audit

> Systematic examination and verification of a firm's books of account, transaction records, other relevant documents, and physical inspection of inventory by qualified accountants (called auditors) .

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
AuditType | String |  |  | 

## BalanceSheet

> A financial statement that reports a company's financial position at the end of a specified date.

*No attributes in cached data.*

## BankingProduct

> A package of services and/or goods, accompanied by term and condition which is offered as a whole to (internal or external) customers.

**Extends:** Merchant Service

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
ProductIdentification | Productidentification |  |  | The identifier of product e.g.
ProductType | Bankingproducttypevalues |  |  | Specifies the category/type/class of product like financial product.
ProductLifecycleStatus | Productstatus |  |  | Refers to the lifecycle of a product (e.g., initiated, announced, active, obsolete, withdrawn).
ProductPriority | Text |  |  | 
ProductDescription | Text |  |  | A detailed explanation or commentary of product.
ProductVersion | Text |  |  | 
ProductName | Name |  |  | The name of Product.

## CardPaymentService

> A payment service to execute payment transactions through a payment card, including online payments.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
CardPaymentServiceIdentifier | Identifier |  |  | 
CardPaymentServiceType | Cardpaymentservicetypevalues |  |  | Type of payment card as a product.
CardPaymentServiceConfiguration | Text |  |  | Configuration specified for the payment card product.

## Channel

> An interface through which parties can communicate or exchange goods or services.

**Extends:** eBranch Channel

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
ChannelType | Channeltypevalues |  |  | 

## ComplianceCheck

> An assessment to check the compliance

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
ComplianceCheckType | String |  |  | 

## ComplianceReport

> The report created by companies in order to comply to rules, standards, laws and regulations set by regulatory bodies and government agencies.

*No attributes in cached data.*

## Condition

> Condition is a premise upon which the fulfillment of an agreement depends General and special arrangements, provisions, requirements, rules, specifications, and standards that form an integral part of

**Extends:** Product Matching Condition

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
ConditionIdentification | Identifier |  |  | The identifier of Condition
ConditionName | Name |  |  | The name of Condition
ConditionValidityPeriod | Datetimeperiod |  |  | The validity period of Condition
ConditionDateAndTime | Datetime |  |  | 
ConditionStatus | Status |  |  | Refers to the lifecycle of a Condition

## ContactPoint

> Number, physical or virtual address, used for communication.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
ContactPointType | Contactpointtypevalues |  |  | 

## Correspondence

> The rendering of a document to a medium and the transmission of the rendering via a communication channel.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
CorrespondenceType | Correspondencetypevalues |  |  | The type of correspondence (e.g.
CorrespondenceAddress | Address |  |  | The address for message delivery (needs to match channel selection)
CorrespondenceDateTime | Datetime |  |  | Key dates used for the correspondence (e.g.
CorrespondenceContent | Text |  |  | The message content (aligned to template as appropriate)
CorrespondenceTemplate | Text |  |  | Template used to assemble standard format correspondence (can be supplied with the correspondence or maintained within the Correspondence service domain as appropriate)
CorrespondenceCommunicationMethod | Correspondencecommunicationmethodtypevalues |  |  | Communication method used for the transmission of a correspondence.
CorrespondenceAddressType | Addresstypevalues |  |  | 
CorrespondenceMedium | Correspondencemediumtypevalues |  |  | Medium through which the correspondence can be submitted such as paper, electronic or both.

## Country

> Nation with its own government.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
NationalRegulatoryAuthority | Involvedparty |  |  | Regulatory authority of the country.

## CurrentAccount

> A bank account upon which the financial position of current account agreement is managed.

*No attributes in cached data.*

## CustomerAgreement

> An agreement between a bank and its customer.

*No attributes in cached data.*

## DateTime

> A point in time.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
TimeIndication | String |  |  | Expression of the point in time is expressed according to "TimeIndicationType" e.g.
TimeIndicationType | String |  |  | 

## Device

> An item created to serve a particular need, such as a credit card, a smart phone, an electronic signature, an electronic key, etc.

**Extends:** Issued Device

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
DeviceIdentification | Deviceidentification |  |  | 
DeviceType | Devicetypevalues |  |  | Reference to the device type of the device A device has the characteristics of the device type it belongs to possibly specified e.g.
DeviceProperty | Text |  |  | Property of a device relevant for its use.
DeviceElement | Text |  |  | An element of the device that can be used independently and is individually identified e.g.
DeviceStatus | Status |  |  | The life cycle stage of a device e.g.
DeviceVersion | Number |  |  | 
DeviceDateTime | Datetime |  |  | 
DeviceDescription | Text |  |  | 
DeviceName | Name |  |  | 
DeviceLanguage | Text |  |  | Preferred language set on the device
DevicePhoneNumber | Text |  |  | Phone number associated with the device.
DeviceLocation | Location |  |  | Geographical location of the device.
DeviceManufacturer | Text |  |  | Manufacturer of the device.
DeviceCountry | Country |  |  | Country of the location.
DeviceAddress | Address |  |  | The address associated with the device like Internet Protocol address, email Address
DeviceAddressType | Addresstypevalues |  |  | 
DeviceOperatingSystem | Deviceoperatingsystemtypevalues |  |  | The operating system deployed on device.

## Document

> Something tangible that records something, such as a recording or a photograph, or a writing that can be used to furnish evidence or information (FIBO) Definition: A physical or digital representation

**Extends:** Transaction Document

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
DocumentIdentification | Identifier |  |  | An identifier that allows to uniquely refer to an instance of a Document.
DocumentVersion | Number |  |  | 
DocumentType | Financialdocumenttypevalues |  |  | Specifies the type of the document, for example commercial invoice.
DocumentStatus | Status |  |  | Status of the document (e.g.
DocumentDateTime | Datetime |  |  | 
DocumentName | Name |  |  | 
DocumentDateTimeType | Documentdatetimetypevalues |  |  | 
DocumentPurpose | Text |  |  | Specifies the function of the document.
DocumentFormat | Text |  |  | 
DocumentSubject | Text |  |  | 
DocumentDescription | Text |  |  | 
DocumentValidityPeriod | Datetimeperiod |  |  | 

## Event

> Something that happens, has happened, can happen or is planned to happen.

**Extends:** Credit Alert

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
EventType | Text |  |  | 
EventDateTime | Datetime |  |  | 
EventDescription | Text |  |  | 
EventSource | Object |  |  | 
EventLocation | Location |  |  | 
EventAction | Action |  |  | 
EventStatus | Status |  |  | 
EventValue | Value |  |  | 
EventValidityPeriod | Datetimeperiod |  |  | 
EventIdentification | Identifier |  |  | 

## FinancialInstrument

> A contract that gives rise to a financial asset of one entity and a financial liability or equity instrument of another entity.

**Extends:** Leasing Product

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
FinancialInstrumentType | Financialinstrumenttypevalues |  |  | 
FinancialInstrumentIdentification | Financialinstrumentidentification |  |  | 
FinancialInstrumentName | Name |  |  | 
FinancialInstrumentDate | Financialinstrumentdatetime |  |  | Key dates of financial instrument

## Goal

> A goal represents a high-level statement of intent, direction, or desired end state for an organization and its stakeholders.

**Extends:** Business Development Goal

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
GoalType | Goaltypevalues |  |  | The classification of Goal
GoalDefinition | Text |  |  | The definition of Goal
GoalName | Name |  |  | The name of Goal
GoalDateAndTime | Goaldatetime |  |  | The key dates and times of Goal like Setting Data, Planning Date, Start Date, Review Date, Completion Date.
GoalStatus | Goalstatus |  |  | The lifecycle status of Goal like Goal Setting, Planning, Execution, Monitoring and Evaluation, Completion or Achievement, Maintenance or Sustainment, Closure or Renewal

## Indicator

> Indicators are statistics used to measure current condition or existence of something

**Extends:** Customer Position State Indicator

*No attributes in cached data.*

## InsuranceAgreement

> An Agreement between an insurer and a customer to insure a risk object against some risk.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
InsuranceAgreementIdentifier | String |  |  | An identifier that allows to uniquely refer to an instance of an Insurance Agreement.

## LoanAccount

> A bank account upon which the financial position of loan account agreement is managed.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
LoanOutstandingAmount | String |  |  | The amount of a loan that has been disbursed but has not been repaid yet

## LoanAgreement

> Definition: A (Debt) Agreement into which is arranged that a party (lender) is giving money or financial instruments to another party (borrower) in exchange for future repayment of the loan value or p

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
LoanTermAndCondition | Condition |  |  | Term and condition to govern the use of loan product and the loan agreement in general.

## Location

> The definition of an addressable space/position both in real and virtual environments with associated uses and entitlements

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
LocationDescription | Text |  |  | A description of the property, particularly if it has landmark characteristics.
LocationDateTime | Datetime |  |  | Key dates associated with the directory entry (e.g.
LocationStatus | Status |  |  | The tracked status (e.g.
LocationType | Geographicalareatypevalues |  |  | Type of location (e.g.
LocationZoningType | Text |  |  | The planning or zoning status (e.g.
LocationNeighborhoodType | Text |  |  | The general purpose and neighborhood of the property (e.g.
LocationConstructionType | Text |  |  | The construction approach for a property at the location (e.g.
LocationOccupancyType | Text |  |  | The type of occupancy (e.g.
LocationValue | Value |  |  | The estimated (book) value of the property at the location - rental and purchase as appropriate.
LocationCapacity | Text |  |  | An indication of the size or scale of the property where appropriate (e.g.
LocationIdentification | Identifier |  |  | 
LocationAddress | Address |  |  | 
LocationName | Name |  |  | Name (label) of the location.
LocationTimeZone | Text |  |  | Local time zone.

## Merchant

> Party performing the card payment transaction.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
MerchantType | Merchanttypevalues |  |  | 
MerchantAddress | Address |  |  | 

## Notification

> A communication notifying or reporting a change in position or circumstance of mutual interest Examples: notification of an overdue payment notification of a coming due date notification of a change i

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
NotificationReference | Object |  |  | An identifier that allows to uniquely refer to an instance of a notification.
NotificationType | String |  |  | The attribute value of Notification Type, specifies the kind of Notification for this occurrence of Notification.
NotificationContent | String |  |  | 

## Obligation

> A duty that is specified in and imposed by an agreement.

*No attributes in cached data.*

## Party

> A party represents an autonomous entity in which a bank has a business interest.

**Extends:** Person

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
PartyName | Name |  |  | Name by which a party is known and which is usually used to identify that party.
PartyType | Partytypevalues |  |  | Specifies the type of party in different business contexts.
PartyDateTime | Datetime |  |  | 
PartyIdentification | Partyidentification |  |  | 
PartyLegalStructureType | Partylegalstructuretypevalues |  |  | 

## PartyRole

> A specific role of a specific Party in the specific relationship.

**Extends:** Clearing Involvement

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
PartyRoleType | Text |  |  | 
PartyRoleName | Name |  |  | 
PartyRoleValidityPeriod | Datetimeperiod |  |  | 
PartyInvolvementType | Partyinvolvementtypevalues |  |  | 

## Person

> Human entity, as distinguished from a corporate entity (which is sometimes referred to as an 'artificial person').

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
PersonIdentification | Personidentification |  |  | 
ResidentialStatus | Residentalstatustypevalues |  |  | Residential status of an individual, for example, non-permanent resident.
BirthDate | Date |  |  | Date on which a person is born.
Nationality | Country |  |  | Specifies the country where a person was born or is legally accepted as belonging to the country.
Ethnicity | Text |  |  | The religious identification of the person.
Religion | Text |  |  | 
PersonName | Personname |  |  | 
CivilStatus | Civilstatustypevalues |  |  | Specifies the civil status of a person (ISO20022 BM)
JobTitle | Text |  |  | Title of the function in an organisation.
PersonNamePrefix | Nameprefixtypevalues |  |  | Specifies the terms used to formally address a person.

## Plan

> A method for doing or achieving something, usually involving a series of actions or stages, or something you have arranged to do.

**Extends:** Administrative Plan

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
PlanGoal | Goal |  |  | 
PlanBudget | Budgetarrangement |  |  | An arrangement which is specifying an estimate of costs, revenues, and resources over a specified period, reflecting a reading of future financial conditions and goals.
PlannedAction | Plannedaction |  |  | An action that is arranged in a plan for doing or achieving something
PlanType | Plantypevalues |  |  | A Classification value that specifies the type of Plan
PlanValidityPeriod | Datetimeperiod |  |  | 
PlanDescription | Text |  |  | 

## ProductAgreement

> An agreement with the subject matter of the product between Customer and Provider.

**Extends:** Standing Order Agreement

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
ProductAgreementType | Productagreementtypevalues |  |  | 

## ProductFeature

> A detailed characteristic of a product expressed in offered services and the terms and conditions applicable to the delivery of the services.

**Extends:** Lien Feature

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
ProductFeatureType | Productfeaturetypevalues |  |  | The type or category of product/service features
ProductFeatureSpecification | Text |  |  | 

## RegulatoryReport

> Information needed due to regulatory and statutory requirements.

*No attributes in cached data.*

## RiskAssessment

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
RiskAssessmentViewpoint | String |  |  | The type of risk assessed e.g.

## SavingsAccount

> A bank account upon which the financial position of a saving account agreement is managed.

*No attributes in cached data.*

## Security

> Financial instruments representing a sum of rights of the investor vis-a-vis the issuer.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
SecurityAmount | Amount |  |  | 
SecurityPrice | Arrangement |  |  | The prevailing bank buy/sell quote for the security.ISO20022
SecurityIdentification | Securityidentification |  |  | 
SecurityBalance | Accountbalance |  |  | Balance of the account which holds a specific security.
SecurityStatus | Securitystatus |  |  | 
SecurityFees | Feearrangement |  |  | Fees related to securities.ISO20022
SecurityDate | Datetime |  |  | 
SecurityRate | Rate |  |  | Rating(s) of the security.ISO20022
SecurityTax | Taxarrangement |  |  | Tax details of the security.ISO20022
SecurityJurisdiction | Jurisdiction |  |  | Jurisdiction (country, county, state, province, city) in which the security is legally recorded for regulatory and/or tax purposes.ISO20022

## Strategy

> A high level plan to achieve one or more goals

**Extends:** Business Development Strategy

*No attributes in cached data.*

## TermDepositAgreement

> An agreement concering an interest bearing deposit between the Bank and a corporate customer.

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
TermDepositAgreementIdentification | Identifier |  |  | The reference with which a Corporate Deposit Agreement is identified
TermDepositAgreementType | Termdepositagreementtypevalues |  |  | 

## Transaction

> A planned or performed action in the context of concluding an agreement or fulfilling an arrangement Act to do something.

**Extends:** Lien Transaction

Attribute | Type | Mandatory | Multi-valued | Description
--- | --- | --- | --- | ---
TransactionIdentification | Identifier |  |  | An identifier that allows to uniquely refer to an instance of a transaction.
TransactionDate | Transactiondatetime |  |  | The Date that the transaction has occurred or is planned to occur.
TransactionType | Transactiontypevalues |  |  | Specifies the category of Transaction like payment transaction, accounting transaction, financial Transaction, banking transaction, etc.
TransactionDescription | Text |  |  | A detailed explanation or commentary of transaction.
TransactionStatus | Transactionstatus |  |  | A characteristic of transaction which refers to the LifecycleStatus of transaction (e.g., initiated, executed, confirmed, cancelled, etc.)
TransactionName | Name |  |  | The name of transaction.
