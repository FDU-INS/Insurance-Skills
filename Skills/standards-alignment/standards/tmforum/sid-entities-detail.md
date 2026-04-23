# TM Forum SID v4 — Core Entity Detail

Detailed definitions for 46 core SID entities (of 46 requested),
including inheritance chains and property tables.

## Party

> Generic Party structure used to define commonalities between sub concepts of Individual and Organization.

**SID Domain:** EngagedParty | **Extends:** Entity

Property | Type | Description
--- | --- | ---
id | string | Unique identifier of the organization
href | string | Hyperlink to access the organization
externalReference | ExternalReference[] | 
partyCharacteristic | Characteristic[] | 
taxExemptionCertificate | TaxExemptionCertificate[] | 
creditRating | PartyCreditProfile[] | 
relatedParty | RelatedParty[] | 
contactMedium | ContactMedium[] | 

## Individual

> Individual represents a single human being (a man, woman or child). The individual can be a customer, an employee or any other person that the organization needs to store information about.

**SID Domain:** EngagedParty | **Extends:** Party, Entity

Property | Type | Description
--- | --- | ---
gender | string | Gender
placeOfBirth | string | Reference to the place where the individual was born
countryOfBirth | string | Country where the individual was born
nationality | string | Nationality
maritalStatus | string | Marital status (married, divorced, widow ...)
birthDate | string (date-time) | Birth date
deathDate | string (date-time) | Date of death
title | string | Useful for titles (aristocratic, social,...) Pr, Dr, Sir, ...
aristocraticTitle | string | e.g.
generation | string | e.g..
givenName | string | First name of the individual
preferredGivenName | string | Contains the chosen name by which the individual prefers to be addressed.
familyNamePrefix | string | Family name prefix
familyName | string | Contains the non-chosen or inherited name.
legalName | string | Legal name or birth name (name one has for official purposes)
middleName | string | Middles name or initial
fullName | string | Full name flatten (first, middle, and last names)
formattedName | string | A fully formatted name in one string with all of its pieces in their proper place and all of the necessary punctuation.
location | string | Temporary current location od the individual (may be used if the individual has approved its sharing)
status | IndividualStateType | Status of the individual
otherName | OtherNameIndividual[] | 
individualIdentification | IndividualIdentification[] | 
disability | Disability[] | 
languageAbility | LanguageAbility[] | 
skill | Skill[] | 

## Organization

> Organization represents a group of people identified by shared interests or purpose. Examples include business, department and enterprise. Because of the complex nature of many businesses, both organizations and organization units are represented by the same data.

**SID Domain:** EngagedParty | **Extends:** Party, Entity

Property | Type | Description
--- | --- | ---
isLegalEntity | boolean | If value is true, the organization is a legal entity known by a national referential.
isHeadOffice | boolean | If value is true, the organization is the head office
organizationType | string | Type of Organization (company, department...)
tradingName | string | Name that the organization (unit) trades under
existsDuring | TimePeriod | 
name | string | Organization name (department name for example)
nameType | string | Type of the name : Co, Inc, Ltd,…
status | OrganizationStateType | Status of the organization
otherName | OtherNameOrganization[] | 
organizationIdentification | OrganizationIdentification[] | 
organizationChildRelationship | OrganizationChildRelationship[] | 
organizationParentRelationship | OrganizationParentRelationship | 

## PartyRole

> The part played by a party in a given context.

**SID Domain:** EngagedParty | **Extends:** Entity

Property | Type | Description
--- | --- | ---
href | string | Url used to reference the party role.
id | string | Unique identifier for PartyRoles
name | string | A word, term, or phrase by which the PartyRole is known and distinguished from other PartyRoles.
status | string | Used to track the lifecycle status of the party role.
statusReason | string | A string providing an explanation on the value of the status lifecycle.
validFor | TimePeriod | The time period that the PartyRole is valid for.
engagedParty | RelatedPartyRefOrValue | 
roleType | RoleTypeRef | 
account | AccountRef[] | 
paymentMethod | PaymentMethodRef[] | 
contactMedium | ContactMedium[] | 
characteristic | Characteristic[] | Describes the characteristic of a party role.
creditProfile | CreditProfile[] | 
agreement | AgreementRef[] | 
relatedParty | RelatedPartyRefOrValue[] | 

## Partner

> The part played by a party in a given context.

**SID Domain:** EngagedParty | **Extends:** Entity

Property | Type | Description
--- | --- | ---
href | string | Url used to reference the partner.
id | string | Unique identifier for Partners
name | string | A word, term, or phrase by which the Partner is known and distinguished from other Partners.
status | string | Used to track the lifecycle status of the partner.
statusReason | string | A string providing an explanation on the value of the status lifecycle.
validFor | TimePeriod | The time period that the Partner is valid for.
engagedParty | RelatedParty | The reference to the party engaged in this partnership.
account | AccountRef[] | 
paymentMethod | PaymentMethodRef[] | 
contactMedium | ContactMedium[] | 
characteristic | Characteristic[] | Describes the characteristic of a partner.
creditProfile | CreditProfile[] | 
agreement | AgreementRef[] | 
relatedParty | RelatedParty[] | 

## Partnership

> A partnership represents a formalized collaboration between various parties, each party playing a role in the partnership. The parties playing a role in the partnership represented by the Partner entity. The structure of a partnership is specified by a PartnershipSpecification which contain all the information for the setup of the partnership, including the list of identified roles and the agreement that should apply.

**SID Domain:** EngagedParty | **Extends:** Entity

Property | Type | Description
--- | --- | ---
description | string | An explanatory text regarding this partnership
href | string | The reference url for this partnership
id | string | The identifier of the partnership
name | string | An identifying name for the partnership.
specification | PartnershipSpecificationRef | The specification of this partnership.
partner | Partner[] | The list of partners of the partnership, where a partner represents a party playing a given role.

## Contact

> An individual or an organization used as a contact point for a given account and accessed via some contact medium.

**SID Domain:** EngagedParty | **Extends:** Entity

Property | Type | Description
--- | --- | ---
contactName | string | A displayable name for that contact
contactType | string | Type of contact (primary, secondary...)
partyRoleType | string | Identifies what kind of party role type is linked to the contact (a account manager...)
validFor | TimePeriod | Validity period of that contact
contactMedium | ContactMedium[] | 
relatedParty | RelatedParty | 

## DigitalIdentity

> DigitalIdentity is a class that allow to describe a digital identity for an individual or a resource or a specific party role. One of these three MUST be provided. If an individual is provided, this identity will be for all her/his partyRole. To avoid confusion it is recommended in this case to not provide partyRoleIdentified.

**SID Domain:** EngagedParty | **Extends:** Entity, Addressable

Property | Type | Description
--- | --- | ---
creationDate | string (date-time) | Date and time of the Digital Identity creation (timestamp)
lastUpdate | string (date-time) | Date and time of the Digital Identity last update (timestamp)
status | string | Used to indicate the current lifecycle status of this digital identity (unknown, active, suspended, archived).
nickname | string | Nickname associated to this digital identity (like Juanito17 or the QuebecMoose etc...).
validFor | TimePeriod | The period for which this digial identity is valid.
credential | /definitions/Credential[] | A list of credential/authentification method that are used for this digital identity.
contactMedium | /definitions/DigitalIdentityContactMedium[] | List of contact medium associated with the digital identity.
attachment | /definitions/AttachmentRefOrValue[] | List of attachment associated with this digital identity.
relatedParty | /definitions/RelatedParty[] | Parties who have an interest in this digital identity (like the organization in charge of providing identity).
partyRoleIdentified | /definitions/RelatedParty[] | Related Parties who are identified by this digital identity.
individualIdentified | PartyRef | Individual identified by this digital identity.
resourceIdentified | ResourceRef | Resource identified by this digital identity.

## Credential

> Credential is a class that allow to describe an authentification method.

**SID Domain:** EngagedParty | **Extends:** Extensible

Property | Type | Description
--- | --- | ---
id | string | an identifier for a credential/authentification method for this digital identity
state | string | Used to indicate the current lifecycle state of this credential (like active, inactive, expired).
trustLevel | string | A level of assurance associated with this credential - this could be used to limit/allow specific permission based on this trust level.
contactMedium | /definitions/DigitalIdentityContactMedium[] | List of contact medium associated with this credential/authentification method.
validFor | TimePeriod | The period for which this digial identity is valid.

## Account

> Generic Account structure used to define commonalities between sub concepts of PartyAccount and Financial Account.

**SID Domain:** EngagedParty | **Extends:** Entity

Property | Type | Description
--- | --- | ---
creditLimit | Money | The maximum amount of money that may be charged on an account
description | string | Detailed description of the party account
href | string | Unique reference of the account
id | string | Unique identifier of the account
lastModified | string (date-time) | Date of last modification of the account
name | string | Name of the account
state | string | Contains the lifecycle state such as: Active, Closed, Suspended and so on.
accountType | string | A categorization of an account, such as individual, joint, and so forth, whose instances share some of the same characteristics.
relatedParty | RelatedParty[] | 
taxExemption | TaxExemptionCertificate[] | 
contact | Contact[] | 
accountBalance | AccountBalance[] | 
accountRelationship | AccountRelationship[] | 

## Agreement

> An agreement represents a contract or arrangement, either written or verbal and sometimes enforceable by law, such as a service level agreement or a customer price agreement. An agreement involves a number of other business entities, such as products, services, and resources and/or their specifications.

**SID Domain:** EngagedParty | **Extends:** Entity

Property | Type | Description
--- | --- | ---
agreementPeriod | TimePeriod | The time period during which the Agreement is in effect.
completionDate | TimePeriod | Date at which the agreement is completed
description | string | Narrative that explains the agreement and details about the it , such as why the agreement is taking place.
documentNumber | integer | A reference number assigned to an Agreement that follows a prescribed numbering system.
href | string | Unique url identifying the agreement as a resource
id | string | Unique identifier for the agreement
initialDate | string (date-time) | Date at which the agreement was initialized
name | string | A human-readable name for the agreement
statementOfIntent | string | An overview and goals of the Agreement
status | string | The current status of the agreement.
agreementType | string | The type of the agreement.
version | string | A string identifying the version of the agreement
agreementSpecification | AgreementSpecificationRef | 
agreementItem | AgreementItem[] | 
engagedParty | RelatedParty[] | 
agreementAuthorization | AgreementAuthorization[] | 
characteristic | Characteristic[] | 
associatedAgreement | AgreementRef[] | 

## AgreementSpecification

> A template of an agreement that can be used when establishing partnerships

**SID Domain:** EngagedParty | **Extends:** Entity

Property | Type | Description
--- | --- | ---
description | string | A narrative that explains in detail what the agreement specification is about
href | string | Reference of the agreement specification
id | string | Unique identifier of the agreement specification
isBundle | boolean | If true, this agreement specification is a grouping of other agreement specifications.
lastUpdate | string (date-time) | Date and time of the last update
lifecycleStatus | string | Indicates the current lifecycle status
name | string | Name of the agreement specification
validFor | TimePeriod | The period for which the agreement specification is valid
version | string | Agreement specification version
serviceCategory | CategoryRef | 
specificationCharacteristic | AgreementSpecCharacteristic[] | 
relatedParty | RelatedParty[] | 
attachment | AttachmentRefOrValue[] | 
specificationRelationship | AgreementSpecificationRelationship[] | 

## Customer

**SID Domain:** Customer | **Extends:** Entity

Property | Type | Description
--- | --- | ---
href | string | Url used to reference the customer.
id | string | Unique identifier for Customers
name | string | A word, term, or phrase by which the Customer is known and distinguished from other Customers.
status | string | Used to track the lifecycle status of the customer.
statusReason | string | A string providing an explanation on the value of the status lifecycle.
validFor | TimePeriod | The time period that the Customer is valid for.
engagedParty | RelatedParty | The party - an organization or an individual - that is engaged as a customer.
account | AccountRef[] | 
paymentMethod | PaymentMethodRef[] | 
contactMedium | ContactMedium[] | 
characteristic | Characteristic[] | Describes the characteristic of a customer.
creditProfile | CreditProfile[] | 
agreement | AgreementRef[] | 
relatedParty | RelatedParty[] | 

## BillingAccount

> A party account used for billing purposes. It includes a description of the bill structure (frequency, presentation media, format and so on). It is a specialization of entity PartyAccount.

**SID Domain:** Customer | **Extends:** PartyAccount

Property | Type | Description
--- | --- | ---
ratingType | string | Indicates whether the account follows a specific payment option such as prepaid or postpaid

## CustomerBill

> The customer bill. Can be a regular recurring bill or an extra bill on demand by the customer or the csp.

**SID Domain:** Customer | **Extends:** Entity

Property | Type | Description
--- | --- | ---
id | string | Explanation: Unique identifier of he bill
href | string | Bill unique reference
amountDue | Money | 
appliedPayment | AppliedPayment[] | Applied payment is a payment associated with the bill.
billDate | string (date-time) | Bill date, external customer view (in consequence: different to the production date of the bill)
billDocument | AttachmentRefOrValue[] | 
billNo | string | Bill reference known by the customer or the party and displayed on the bill.
billingAccount | BillingAccountRef | 
billingPeriod | TimePeriod | 
billCycle | BillCycleRef | 
category | string | Category of the bill produced : normal, duplicate, interim, last, trial customer or credit note for example
financialAccount | FinancialAccountRef | 
lastUpdate | string (date-time) | Date of bill last update
nextBillDate | string (date-time) | ).
paymentDueDate | string (date-time) | Date at which the amount due should have been paid
paymentMethod | PaymentMethodRef | paymentMethod here is recognized to be not really necessary in a STANDARD.
relatedParty | RelatedParty[] | 
remainingAmount | Money | 
runType | CustomerBillRunType | onCycle (a bill can be created as a result of a cycle run) or offCycle (a bill can be created as a result of other events such as customer request or account close)
taxExcludedAmount | Money | 
taxIncludedAmount | Money | 
taxItem | TaxItem[] | 
state | CustomerBillStateType | Status of the bill

## Payment

> The Payment resource represents a performed payment. It contains both information about the payment and the payment method used to perform it.

**SID Domain:** Customer | **Extends:** Entity

Property | Type | Description
--- | --- | ---
id | string | Unique identifier of Payment
href | string | Hypertext Reference of the Payment
correlatorId | string | Unique identifier in the client for the payment in case it is needed to correlate
paymentDate | string (date-time) | Date when the payment was performed
name | string | Screen name of the payment
description | string | Text describing the contents of the payment
authorizationCode | string | Authorization code retrieved from an external payment gateway that could be used for conciliation
status | string | Status of the payment
statusDate | string (date-time) | Date when the status was recorded
amount | Money | Amount to be paid (net of taxes)
taxAmount | Money | Tax applied
totalAmount | Money | Amount to be paid (including taxes)
channel | ChannelRef | 
paymentItem | PaymentItem[] | 
relatedParty | RelatedParty[] | 
paymentMethod | PaymentMethodRefOrValue | 
account | AccountRef | 
pointOfInteraction | PointOfInteraction | 

## PaymentMethod

> A Payment Method is a pure-virtual super-class that defines a specific method of payment such as Direct Debit, Cash, Digital Wallet,Tokenized Card, Bank Account Transfer, Bank Account Debit, Bank Card, Voucher, Check, Bucket PaymentMethod, Account PaymentMethod, and Loyalty PaymentMethod with all details associated. Use the @type attribute to specify the concrete type in the API calls.

**SID Domain:** Customer | **Extends:** Entity

Property | Type | Description
--- | --- | ---
name | string | Friendly name assigned to the payment method
description | string | Text description of the contents of the payment method
isPreferred | boolean | If the method is the preferred one by the owner.
authorizationCode | string | Review: Authorization code provided by a financial institution.
status | string | Status of the payment method
statusDate | string (date-time) | The last time the payment method status changed.
statusReason | string | The reason for the last status change.
validFor | TimePeriod | Date interval in which the payment method is valid
@type | string | Type of payment method (e.g.: bank card, cash, voucher, etc).
relatedParty | RelatedParty | Reference to the customer or party that owns that payment method or can use it.
relatedPlace | RelatedPlace | Reference to a place for billing or delivery address, if different to that of the related party.
account | AccountRef[] | Reference to the accounts that are linked to the payment method.

## ProductOrder

> A Product Order is a type of order which  can  be used to place an order between a customer and a service provider or between a service provider and a partner and vice versa,

**SID Domain:** Customer | **Extends:** Entity

Property | Type | Description
--- | --- | ---
agreement | AgreementRef[] | A reference to an agreement defined in the context of the product order
billingAccount | BillingAccountRef | 
cancellationDate | string (date-time) | Date when the order is cancelled.
cancellationReason | string | Reason why the order is cancelled.
category | string | Used to categorize the order from a business perspective that can be useful for the OM system (e.g.
channel | RelatedChannel[] | 
completionDate | string (date-time) | Date when the order was completed
description | string | Description of the product order
expectedCompletionDate | string (date-time) | Expected delivery date amended by the provider
externalId | string | ID given by the consumer and only understandable by him (to facilitate his searches afterwards)
href | string | Hyperlink to access the order
id | string | ID created on repository side (OM system)
note | Note[] | 
notificationContact | string | Contact attached to the order to send back information regarding this order
orderDate | string (date-time) | Date when the order was created
orderTotalPrice | OrderPrice[] | 
payment | PaymentRef[] | 
priority | string | A way that can be used by consumers to prioritize orders in OM system (from 0 to 4 : 0 is the highest priority, and 4 the lowest)
productOfferingQualification | ProductOfferingQualificationRef[] | 
quote | QuoteRef[] | 
productOrderItem | ProductOrderItem[] | 
relatedParty | RelatedParty[] | 
requestedCompletionDate | string (date-time) | Requested delivery date from the requestor perspective
requestedStartDate | string (date-time) | Order fulfillment start date wished by the requestor.
state | ProductOrderStateType | Tracks the lifecycle status of the product order, such as Acknowledged, Rejected, InProgress, Pending and so on.

## ShoppingCart

> Shopping Cart resource is used for the temporarily selection and reservation of product offerings in e-commerce, call center and retail purchase. Shopping cart supports purchase of both physical and digital goods and service (e.g. handset, telecom network service). Shopping Cart contain list of cart items, a reference to customer (partyRole) or contact medium in case customer not exist, and the total items price including promotions

**SID Domain:** Customer | **Extends:** Entity

Property | Type | Description
--- | --- | ---
href | string | Hyperlink to access the shopping cart
id | string | Unique identifier created on provider side (e.g.
validFor | TimePeriod | The period for which the shopping cart is valid (e.g.
contactMedium | ContactMedium[] | 
cartTotalPrice | CartPrice[] | Total amount of the shopping cart, usually of money, that represents the actual price paid by the Customer for cart (considering only "Active" cart items)
cartItem | CartItem[] | 
relatedParty | RelatedParty[] | 

## Quote

> Quote can be used to negotiate service and product acquisition or modification between a customer and a service provider. Quote contain list of quote items, a reference to customer (partyRole), a list of productOffering and attached prices and conditions.

**SID Domain:** Customer | **Extends:** Entity

Property | Type | Description
--- | --- | ---
agreement | AgreementRef[] | A reference to an agreement defining the context of the quote
billingAccount | BillingAccountRef[] | A reference to a billing account to provide quote context information
category | string | Used to categorize the quote from a business perspective that can be useful for the CRM system (e.g.
contactMedium | ContactMedium[] | Information contact related to the quote requester
description | string | Description of the quote
effectiveQuoteCompletionDate | string (date-time) | Date when the quote has been completed
expectedFulfillmentStartDate | string (date-time) | this is the date wished by the requester to have the requested quote item delivered
expectedQuoteCompletionDate | string (date-time) | This is expected date - from quote supplier - to be able to send back a response for this quote
externalId | string | ID given by the consumer and only understandable by him (to facilitate his searches afterwards)
href | string | Hyperlink to access the quote
id | string | Unique identifier - attributed by quoting system
instantSyncQuote | boolean | An indicator which when the value is "true" means that requester expects to get quoting result immediately in the response.
note | Note[] | Free form text associated with the quote
authorization | Authorization[] | An authorization provided for the quote
quoteDate | string (date-time) | Date and time when the quote was created
quoteItem | QuoteItem[] | An item of the quote - it is used to descirbe an operation on a product to be quoted
quoteTotalPrice | QuotePrice[] | Quote total price
relatedParty | RelatedParty[] | A reference to a party playing a role in this quote (customer, seller, requester, etc.)
productOfferingQualification | ProductOfferingQualificationRef[] | A reference to a previously done product offering qualification
requestedQuoteCompletionDate | string (date-time) | This is requested date - from quote requester - to get a complete response for this quote
state | QuoteStateType | State of the quote : described in the state-machine diagram
validFor | TimePeriod | Quote validity period
version | string | Quote version - if the customer rejected the quote but negotiations still open a new version of the quote is managed

## Product

> A product offering procured by a customer or other interested party playing a party role. A product is realized as one or more service(s) and / or resource(s).

**SID Domain:** Product | **Extends:** Entity

Property | Type | Description
--- | --- | ---
agreement | AgreementItemRef[] | 
billingAccount | BillingAccountRef | 
description | string | Is the description of the product.
href | string | Reference of the product
id | string | Unique identifier of the product
isBundle | boolean | If true, the product is a ProductBundle which is an instantiation of a BundledProductOffering.
isCustomerVisible | boolean | If true, the product is visible by the customer.
name | string | Name of the product.
orderDate | string (date-time) | Is the date when the product was ordered
productCharacteristic | Characteristic[] | 
productOffering | ProductOfferingRef | 
productOrderItem | RelatedProductOrderItem[] | 
product | ProductRefOrValue[] | 
productPrice | ProductPrice[] | 
productRelationship | ProductRelationship[] | 
productSerialNumber | string | Is the serial number for the product.
productSpecification | ProductSpecificationRef | 
productTerm | ProductTerm[] | 
realizingResource | ResourceRef[] | 
realizingService | ServiceRef[] | 
relatedParty | RelatedParty[] | 
place | RelatedPlaceRefOrValue[] | 
startDate | string (date-time) | Is the date from which the product starts
status | ProductStatusType | Is the lifecycle status of the product.
terminationDate | string (date-time) | Is the date when the product was terminated

## ProductOffering

> Represents entities that are orderable from the provider of the catalog, this resource includes pricing information.

**SID Domain:** Product | **Extends:** Addressable, Extensible

Property | Type | Description
--- | --- | ---
description | string | Description of the productOffering
href | string | Reference of the ProductOffering
id | string | Unique identifier of the productOffering
isBundle | boolean | isBundle determines whether a productOffering represents a single productOffering (false), or a bundle of productOfferings (true).
isSellable | boolean | A flag indicating if this product offer can be sold stand-alone for sale or not.
lastUpdate | string (date-time) | Date and time of the last update
lifecycleStatus | string | Used to indicate the current lifecycle status
name | string | Name of the productOffering
statusReason | string | A string providing a complementary information on the value of the lifecycle status attribute.
validFor | TimePeriod | The period for which the productOffering is valid
version | string | ProductOffering version
place | PlaceRef[] | Place defines the places where the products are sold or delivered.
serviceLevelAgreement | SLARef | A service level agreement (SLA) is a type of agreement that represents a formal negotiated agreement between two parties designed to create a common understanding about products, services, priorities,
productSpecification | ProductSpecificationRef | A ProductSpecification is a detailed description of a tangible or intangible object made available externally in the form of a ProductOffering to customers or other parties playing a party role.
channel | ChannelRef[] | The channel defines the channel for selling product offerings.
serviceCandidate | ServiceCandidateRef | ServiceCandidate is an entity that makes a ServiceSpecification available to a catalog.
category | CategoryRef[] | The category resource is used to group product offerings, service and resource candidates in logical containers.
resourceCandidate | ResourceCandidateRef | A resource candidate is an entity that makes a ResourceSpecification available to a catalog.
productOfferingTerm | ProductOfferingTerm[] | A condition under which a ProductOffering is made available to Customers.
productOfferingPrice | ProductOfferingPriceRef[] | An amount, usually of money, that is asked for or allowed when a ProductOffering is bought, rented, or leased.
agreement | AgreementRef[] | An agreement represents a contract or arrangement, either written or verbal and sometimes enforceable by law, such as a service level agreement or a customer price agreement.
attachment | AttachmentRefOrValue[] | Complements the description of an element (for instance a product) through video, pictures...
marketSegment | MarketSegmentRef[] | provides references to the corresponding market segment as target of product offerings.
bundledProductOffering | BundledProductOffering[] | A type of ProductOffering that belongs to a grouping of ProductOfferings made available to the market.
prodSpecCharValueUse | ProductSpecificationCharacteristicValueUse[] | A use of the ProductSpecificationCharacteristicValue by a ProductOffering to which additional properties (attributes) apply or override the properties of similar properties contained in ProductSpecifi

## ProductSpecification

> Is a detailed description of a tangible or intangible object made available externally in the form of a ProductOffering to customers or other parties playing a party role.

**SID Domain:** Product | **Extends:** Addressable, Extensible

Property | Type | Description
--- | --- | ---
brand | string | The manufacturer or trademark of the specification
description | string | A narrative that explains in detail what the product specification is
href | string | Reference of the product specification
id | string | Unique identifier of the product specification
isBundle | boolean | isBundle determines whether a productSpecification represents a single productSpecification (false), or a bundle of productSpecification (true).
lastUpdate | string (date-time) | Date and time of the last update
lifecycleStatus | string | Used to indicate the current lifecycle status
name | string | Name of the product specification
productNumber | string | An identification number assigned to uniquely identity the specification
validFor | TimePeriod | The period for which the product specification is valid
version | string | Product specification version
relatedParty | RelatedParty[] | A related party defines party or party role linked to a specific entity.
productSpecCharacteristic | ProductSpecificationCharacteristic[] | A characteristic quality or distinctive feature of a ProductSpecification.
serviceSpecification | ServiceSpecificationRef[] | ServiceSpecification(s) required to realize a ProductSpecification.
productSpecificationRelationship | ProductSpecificationRelationship[] | A migration, substitution, dependency or exclusivity relationship between/among product specifications.
resourceSpecification | ResourceSpecificationRef[] | The ResourceSpecification is required to realize a ProductSpecification.
attachment | AttachmentRefOrValue[] | Complements the description of an element (for instance a product) through video, pictures...
bundledProductSpecification | BundledProductSpecification[] | A type of ProductSpecification that belongs to a grouping of ProductSpecifications made available to the market.
targetProductSchema | TargetProductSchema | A target product schema reference.

## Catalog

> A collection of Product Offerings, intended for a specific DistributionChannel, enhanced with additional information such as SLA parameters, invoicing and shipping details

**SID Domain:** Product | **Extends:** Addressable, Extensible

Property | Type | Description
--- | --- | ---
href | string | Unique reference of the catalog
id | string | Unique identifier of the Catalog
description | string | Description of this catalog
lastUpdate | string (date-time) | Date and time of the last update
lifecycleStatus | string | Used to indicate the current lifecycle status
name | string | Name of the catalog
catalogType | string | Indicates if the catalog is a product, service or resource catalog
validFor | TimePeriod | The period for which the catalog is valid
version | string | Catalog version
relatedParty | RelatedParty[] | List of parties involved in this catalog
category | CategoryRef[] | List of root categories contained in this catalog

## Category

> The category resource is used to group product offerings, service and resource candidates in logical containers. Categories can contain other categories and/or product offerings, resource or service candidates.

**SID Domain:** Product | **Extends:** Addressable, Extensible

Property | Type | Description
--- | --- | ---
description | string | Description of the category
href | string | Reference of the category
id | string | Unique identifier of the category
isRoot | boolean | If true, this Boolean indicates that the category is a root of categories
lastUpdate | string (date-time) | Date and time of the last update
lifecycleStatus | string | Used to indicate the current lifecycle status
name | string | Name of the category
parentId | string | Unique identifier of the parent category
productOffering | ProductOfferingRef[] | A product offering represents entities that are orderable from the provider of the catalog, this resource includes pricing information.
subCategory | CategoryRef[] | The category resource is used to group product offerings, service and resource candidates in logical containers.
validFor | TimePeriod | The period for which the category is valid
version | string | Category version

## Usage

> An occurrence of employing a Product, Service, or Resource for its intended purpose, which is of interest to the business and can have charges applied to it. It is comprised of characteristics, which represent attributes of usage.

**SID Domain:** Product | **Extends:** Entity

Property | Type | Description
--- | --- | ---
usageDate | string (date-time) | Date of usage
description | string | Description of usage
status | UsageStatusType | 
usageType | string | Type of usage
usageSpecification | UsageSpecificationRef | 
usageCharacteristic | UsageCharacteristic[] | 
relatedParty | RelatedParty[] | 
ratedProductUsage | RatedProductUsage[] | 

## Promotion

> Promotion is used to provide the additional discount, voucher, bonus or gift to the customer who meets the pre-defined criteria. Using promotion, the enterprise is able to attract the users and encourage more consumption, especially continuous purchases. Normally Promotion is not regarded as one type of product or product offering. It is often applied when the customer buys the product offerings with the price or amount surpassing the certain limit.

**SID Domain:** Product

Property | Type | Description
--- | --- | ---
@baseType | string | The base type for use in polymorphic collections.
@schemaLocation | string | A link to the schema describing a resource (for type extension).
@type | string | The class type of the actual resource (for type extension).
description | string | Details about the purpose of this promotion.
href | string | Hyperlink to access the promotion.
id | string | Unique identifier of promotion.
lastUpdate | string (date-time) | Latest update date of promotion.
lifecycleStatus | string | Value of promotion status.
name | string | Name of promotion.
pattern | PromotionPattern[] | 
promotionType | string | Type of promotion.
validFor | TimePeriod | The period for which the promotion is valid.
attachment | AttachmentRefOrValue[] | 

## Service

> Service is a base class for defining the Service hierarchy. All Services are characterized as either being possibly visible and usable by a Customer or not. This gives rise to the two subclasses of Service: CustomerFacingService and ResourceFacingService.

**SID Domain:** Service | **Extends:** /Entity

Property | Type | Description
--- | --- | ---
description | string | Free-text description of the service
isServiceEnabled | boolean | If FALSE and hasStarted is FALSE, this particular Service has NOT been enabled for use - if FALSE and hasStarted is TRUE then the service has failed
hasStarted | boolean | If TRUE, this Service has already been started
startMode | string | This attribute is an enumerated integer that indicates how the Service is started, such as: 0: Unknown; 1: Automatically by the managed environment; 2: Automatically by the owning device; 3: Manually
isStateful | boolean | If TRUE, this Service can be changed without affecting any other services
serviceDate | string | Date when the service was created (whatever its status).
startDate | string (date-time) | Date when the service starts
endDate | string (date-time) | Date when the service ends
serviceOrderItem | /definitions/RelatedServiceOrderItem[] | A list of service order items related to this service
note | /definitions/Note[] | A list of notes made on this service
id | string | Unique identifier of the service
href | string | Reference of the service
serviceType | string | Business type of the service
isBundle | boolean | If true, the service is a ServiceBundle which regroup a service hierachy.
name | string | Name of the service
state | /definitions/ServiceStateType | The life cycle state of the service, such as designed, reserved, active, etc...
category | string | Is it a customer facing or resource facing service
serviceSpecification | /definitions/ServiceSpecificationRef | The specification from which this service was instantiated
feature | /definitions/Feature[] | A list of feature associated with this service
relatedEntity | /definitions/RelatedEntityRefOrValue[] | A list of related entity in relationship with this service
serviceCharacteristic | /definitions/Characteristic[] | A list of characteristics that characterize this service (ServiceCharacteristic [*])
serviceRelationship | /definitions/ServiceRelationship[] | A list of service relationships (ServiceRelationship [*]).
supportingService | /definitions/ServiceRefOrValue[] | A list of supporting services (SupportingService [*]).
supportingResource | /definitions/ResourceRef[] | A list of supporting resources (SupportingResource [*]).Note: only Service of type RFS can be associated with Resources
relatedParty | /definitions/RelatedParty[] | A list of related party references (RelatedParty [*]).
place | RelatedPlaceRefOrValue[] | A list of places (Place [*]).

## ServiceSpecification

> ServiceSpecification is a class that offers characteristics to describe a type of service. Functionally, it acts as a template by which Services may be instantiated. By sharing the same specification, these services would therefore share the same set of characteristics.

**SID Domain:** Service | **Extends:** /definitions/EntitySpecification

Property | Type | Description
--- | --- | ---
resourceSpecification | /definitions/ResourceSpecificationRef[] | A list of resource specification references (ResourceSpecificationRef [*]).
serviceLevelSpecification | /definitions/ServiceLevelSpecificationRef[] | A list of service level specifications related to this service specification, and which will need to be satisifiable for corresponding service instances; e.g.
serviceSpecRelationship | /definitions/ServiceSpecRelationship[] | A list of service specifications related to this specification, e.g.
featureSpecification | /definitions/ServiceFeatureSpecification[] | A list of Features for this specification.

## ServiceOrder

**SID Domain:** Service | **Extends:** Entity

Property | Type | Description
--- | --- | ---
cancellationDate | string (date-time) | Date when the order is cancelled.
cancellationReason | string | Reason why the order is cancelled.
category | string | Used to categorize the order, useful for the OM system, such as: Broadband, TVOption
completionDate | string (date-time) | Effective delivery date amended by the provider
description | string | A free-text description of the service order
expectedCompletionDate | string (date-time) | Expected delivery date amended by the provider
externalId | string | ID given by the consumer to facilitate searches
externalReference | /definitions/ExternalReference[] | 
href | string | Hyperlink to access the order
id | string | ID created on repository side
note | /definitions/Note[] | Extra-information about the order; e.g.
notificationContact | string | Contact attached to the order to send back information regarding this order
orderDate | string (date-time) | 
serviceOrderItem | /definitions/ServiceOrderItem[] | A list of service order items to be processed by this order
orderRelationship | /definitions/ServiceOrderRelationship[] | A list of service orders related to this order (e.g.
priority | string | Can be used by consumers to prioritize orders in a Service Order Management system
relatedParty | /definitions/RelatedParty[] | A list of parties which are involved in this order and the role they are playing
requestedCompletionDate | string (date-time) | Requested delivery date from the requestors perspective
requestedStartDate | string (date-time) | Order start date wished by the requestor
startDate | string (date-time) | Date when the order was started for processing
state | /definitions/ServiceOrderStateType | State of the order: described in the state-machine diagram
milestone | /definitions/ServiceOrderMilestone[] | A list of milestones related to this order
jeopardyAlert | /definitions/ServiceOrderJeopardyAlert[] | A list of jeopardy alerts related to this order
errorMessage | /definitions/ServiceOrderErrorMessage | the error message if the order closed by an error

## ServiceCatalog

> The root entity for service catalog management. A service catalog is a group of service specifications made available through service candidates that an organization provides to the consumers (internal consumers like its employees or B2B customers or B2C customers).  A service catalog typically includes name, description and time period that is valid for. It will have a list of ServiceCandidate catalog items. A ServiceCandidate is an entity that makes a ServiceSpecification available to a catalog. A ServiceCandidate and its associated ServiceSpecification may be "published" - made visible -in any number of ServiceCatalogs, or in none.

**SID Domain:** Service | **Extends:** /definitions/Addressable, /definitions/Extensible

Property | Type | Description
--- | --- | ---
category | /definitions/ServiceCategoryRef[] | List of service categories associated with this catalog
description | string | Description of this catalog
lastUpdate | string (date-time) | Date and time of the last update
lifecycleStatus | string | Used to indicate the current lifecycle status
name | string | Name of the service catalog
relatedParty | /definitions/RelatedParty[] | List of parties or party roles related to this category
validFor | TimePeriod | The period for which the service catalog is valid
version | string | ServiceCatalog version

## ServiceCandidate

> ServiceCandidate is an entity that makes a service specification available to a catalog. A ServiceCandidate and its associated service specification may be published - made visible - in any number of service catalogs, or in none. One service specification can be composed of other service specifications.

**SID Domain:** Service | **Extends:** /definitions/Addressable, /definitions/Extensible

Property | Type | Description
--- | --- | ---
name | string | Name given to this REST resource
description | string | Description of this REST resource
version | string | the version of service candidate
validFor | TimePeriod | The period for which this REST resource is valid
lastUpdate | string (date-time) | Date and time of the last update of this REST resource
lifecycleStatus | string | Used to indicate the current lifecycle status of the service candidate.
category | /definitions/ServiceCategoryRef[] | List of categories for this candidate
serviceSpecification | /definitions/ServiceSpecificationRef | The service specification implied by this candidate

## ServiceQualification

> ServiceQualification is used to perform a technical eligibility. It allows to retrieve a list of services that are technically available in the context of the interaction (place, party, service characteristics, ...).

**SID Domain:** Service | **Extends:** Entity

Property | Type | Description
--- | --- | ---
href | string | Hyperlink to access the serviceQualification
id | string | Unique identifier of the serviceQualification resource
description | string | Description of the serviceQualification
effectiveQualificationDate | string (date-time) | Effective date to serviceQualification completion
instantSyncQualification | boolean | An indicator which when the value is "true" means that requester expects to get qualifcation result immediately in the response.
estimatedResponseDate | string (date-time) | Date when the requester expect to provide an answer for the qualification request.
expectedQualificationDate | string (date-time) | A date (DateTime).
expirationDate | string (date-time) | Date when the qualification response expires
state | /definitions/TaskStateType | State of the serviceQualification (acknowledged, inProgress, terminatedWithError, done)
relatedParty | RelatedParty[] | A list of related party references, defines party or party role linked to this request.
externalId | string | Identifier provided by the requester

## Resource

> Resource is an abstract entity that describes the common set of attributes shared by all concrete resources (e.g. TPE, EQUIPMENT) in the inventory.

**SID Domain:** Resource | **Extends:** Entity

Property | Type | Description
--- | --- | ---
category | string | Category of the concrete resource.
description | string | free-text description of the resource
endOperatingDate | string (date-time) | A date time( DateTime).
href | string | The URI for the object itself.
id | string | Identifier of an instance of the resource.
administrativeState | ResourceAdministrativeStateType | Tracks the lifecycle status of the resource, such as planning, installing, opereating, retiring and so on.
operationalState | ResourceOperationalStateType | Tracks the lifecycle status of the resource, such as planning, installing, opereating, retiring and so on.
resourceStatus | ResourceStatusType | Tracks the lifecycle status of the resource, such as planning, installing, opereating, retiring and so on.
usageState | ResourceUsageStateType | Tracks the lifecycle status of the resource, such as planning, installing, opereating, retiring and so on.
name | string | A string used to give a name to the resource
note | /definitions/Note[] | 
place | RelatedPlaceRefOrValue | 
relatedParty | /definitions/RelatedParty[] | 
resourceRelationship | /definitions/ResourceRelationship[] | 
resourceCharacteristic | /definitions/Characteristic[] | 
attachment | AttachmentRefOrValue[] | 
resourceSpecification | /definitions/ResourceSpecificationRef | 
startOperatingDate | string (date-time) | A date time( DateTime).
resourceVersion | string | A field that identifies the specific version of an instance of a resource.
activationFeature | /definitions/Feature[] | Configuration features

## ResourceSpecification

> Resources are physical or non-physical components (or some combination of these) within an enterprise's infrastructure or inventory. They are typically consumed or used by services (for example a physical port assigned to a service) or contribute to the realization of a Product (for example, a SIM card). They can be drawn from the Application, Computing and Network domains, and include, for example, Network Elements, software, IT systems, content and information, and technology components. A ResourceSpecification is a base class that represents a generic means for implementing a particular type of Resource. In essence, a ResourceSpecification defines the common attributes and relationships of a set of related Resources, while Resource defines a specific instance that is based on a particular ResourceSpecification.

**SID Domain:** Resource | **Extends:** Extensible, Addressable

Property | Type | Description
--- | --- | ---
id | string | Unique identifier of this REST resource
href | string (uri) | Hyperlink reference to this REST resource
name | string | Name given to this REST resource
description | string | Description of this REST resource
version | string | Resource Specification version
validFor | TimePeriod | The period for which this REST resource is valid
lastUpdate | string (date-time) | Date and time of the last update of this REST resource
lifecycleStatus | string | Used to indicate the current lifecycle status of the resource specification
isBundle | boolean | A flag indicates that if this resource specification is a bundled specification (true) or single (false).
category | string | Category of the target resource like NetworkConnectivity, PhysicalLinks, Generic, L2Network and so on.
targetResourceSchema | TargetResourceSchema | A target resource schema reference.
featureSpecification | FeatureSpecification[] | A list of Features for this specification.
attachment | AttachmentRefOrValue[] | Complements the description of an element (for instance a resource) through video, pictures ...
relatedParty | RelatedParty[] | A related party defines party or party role linked to a specific entity.
resourceSpecCharacteristic | ResourceSpecificationCharacteristic[] | A characteristic quality or distinctive feature of a ResourceSpecification.
resourceSpecRelationship | ResourceSpecificationRelationship[] | A migration, substitution, dependency or exclusivity relationship between/among resource specifications.

## ResourceOrder

> A Resource Order is a request to provision a set of Resources (logical and physical) triggered by the request to provision a Service through a Service Order

**SID Domain:** Resource | **Extends:** /Entity

Property | Type | Description
--- | --- | ---
id | string | Identifier of an instance of the Resource Order.
href | string (uri) | Hyperlink to access the order
cancellationDate | string (date-time) | Date when the order is cancelled - if cancelled, in RFC3339 (subset of ISO8601) format
cancellationReason | string | Reason why the order is cancelled - if cancelled
externalId | string | DEPRECATED: Use externalReference Instead.
externalReference | /definitions/ExternalReference[] | 
state | /definitions/ResourceOrderStateType | 
name | string | A string used to give a name to the Resource Order
description | string | Free-text description of the Resource Order
priority | integer | A way that can be used by consumers to prioritize orders in OM system (such as: 0 is the highest priority, and 4 the lowest)
orderType | string | Name of the Resource Order type
category | string | Used to categorize the order from a business perspective that can be useful for the order management system
orderDate | string (date-time) | Date when the order was created, in RFC3339 (subset of ISO8601) format
requestedStartDate | string (date-time) | Order start date wished by the requestor, in RFC3339 (subset of ISO8601) format
requestedCompletionDate | string (date-time) | Requested delivery date from the requestor perspective, in RFC3339 (subset of ISO8601) format
startDate | string (date-time) | Date when the order was actually started, in RFC3339 (subset of ISO8601) format
completionDate | string (date-time) | Date when the order was actually completed, in RFC3339 (subset of ISO8601) format
expectedCompletionDate | string (date-time) | Date when the order is expected to be completed, in RFC3339 (subset of ISO8601) format
orderItem | /definitions/ResourceOrderItem[] | 
note | /definitions/Note[] | 
relatedParty | /definitions/RelatedParty[] | 

## ResourceCatalog

> The root entity for resource catalog management. A resource catalog is a group of resource specifications made available through resource candidates that an organization provides to the consumers (internal consumers like its employees or B2B customers or B2C customers).

**SID Domain:** Resource | **Extends:** Entity

Property | Type | Description
--- | --- | ---
id | string | Unique identifier of the Catalog
href | string (uri) | Unique reference of the catalog
name | string | Name of the catalog
description | string | Description of this catalog
version | string | Catalog version
validFor | TimePeriod | The period for which the catalog is valid
lastUpdate | string (date-time) | Date and time of the last update
lifecycleStatus | string | Used to indicate the current lifecycle status
relatedParty | RelatedParty[] | List of parties involved in this catalog
category | ResourceCategoryRef[] | List of root categories contained in this catalog

## LogicalResource

> Logic resource is a type of resource that describes the common set of attributes shared by all concrete logical resources (e.g. TPE, MSISDN, IP Addresses) in the inventory.

**SID Domain:** Resource | **Extends:** Resource

Property | Type | Description
--- | --- | ---
value | string | the value of the logical resource.

## PhysicalResource

> Physical resource is a type of resource that describes the common set of attributes shared by all concrete physical resources (e.g. EQUIPMENT) in the inventory.

**SID Domain:** Resource | **Extends:** Resource

Property | Type | Description
--- | --- | ---
manufactureDate | string (date-time) | This is a string attribute that defines the date of manufacture of this item in the fixed format "dd/mm/yyyy".
powerState | string | This defines the current power status of the hardware item.
serialNumber | string | This is a string that represents a manufacturer-allocated number used to identify different instances of the same hardware item.
versionNumber | string | This is a string that identifies the version of this physical resource.

## GeographicAddress

> Structured textual way of describing how to find a Property in an urban area (country properties are often defined differently). Note : Address corresponds to SID UrbanPropertyAddress

**SID Domain:** Common | **Extends:** Place

Property | Type | Description
--- | --- | ---
city | string | City that the address is in
country | string | Country that the address is in
locality | string | An area of defined or undefined boundaries within a local authority or other legislatively defined area, usually rural or semi rural in nature.
postcode | string | descriptor for a postal delivery area, used to speed and simplify the delivery of mail (also know as zipcode)
stateOrProvince | string | the State or Province that the address is in
streetName | string | Name of the street or other street type
streetNr | string | Number identifying a specific property on a public street.
streetNrLast | string | Last number in a range of street numbers allocated to a property
streetNrLastSuffix | string | Last street number suffix for a ranged address
streetNrSuffix | string | the first street number suffix
streetSuffix | string | A modifier denoting a relative direction
streetType | string | alley, avenue, boulevard, brae, crescent, drive, highway, lane, terrace, parade, place, tarn, way, wharf
geographicLocation | GeographicLocationRefOrValue | 
geographicSubAddress | GeographicSubAddress[] | 

## GeographicSite

**SID Domain:** Common | **Extends:** Place

Property | Type | Description
--- | --- | ---
code | string | A code that may be used for some addressing schemes eg: [ANSI T1.253-1999]
description | string | Text describing additional information regarding the site
status | string | The condition of the GeographicSite, such as planned, underConstruction, cancelled, active, inactive, former
relatedParty | RelatedParty[] | 
calendar | CalendarPeriod[] | 
place | /definitions/PlaceRefOrValue[] | 
siteRelationship | GeographicSiteRelationship[] | 

## GeographicLocation

> A GeographicLocation is a pure-virtual super-class to the GeoJSON-aligned geometries of Point (addresses and locations), MultiPoint, LineString (streets, highways and boundaries), MultiLineString and Polygon (countries, provinces, tracts of land). Use the @type attribute to specify which of these is being specified by the geometry attribute.

**SID Domain:** Common | **Extends:** Place

Property | Type | Description
--- | --- | ---
id | string | Unique identifier of the geographic location
href | string | An URI used to access to the geographic location resource
@type | string | The name of the GeoJSON structure used in the geometry attribute
bbox | number[] | A bounding box array that contains the geometry.

## ContactMedium

> Indicates the contact medium that could be used to contact the party.

**SID Domain:** Common | **Extends:** Entity

Property | Type | Description
--- | --- | ---
preferred | boolean | If true, indicates that is the preferred contact medium
mediumType | string | Type of the contact medium, such as: email address, telephone number, postal address
validFor | TimePeriod | The time period that the contact medium is valid for
characteristic | MediumCharacteristic | Any additional characteristic(s) of this contact medium

## TroubleTicket

> A trouble ticket is a record of an issue that is created, tracked, and managed by a trouble ticket management system

**SID Domain:** Common | **Extends:** Entity

Property | Type | Description
--- | --- | ---
attachment | AttachmentRefOrValue[] | File(s) attached to the trouble ticket.
channel | ChannelRef | The channel that origin the trouble ticket
creationDate | string (date-time) | The date on which the trouble ticket was created
description | string | Description of the trouble or issue
expectedResolutionDate | string (date-time) | The expected resolution date determined by the trouble ticket system
externalId | string | Additional identifier coming from an external system
href | string | Hyperlink, a reference to the trouble ticket entity
id | string | Unique identifier of the trouble ticket
lastUpdate | string (date-time) | The date and time that the trouble ticked was last updated
name | string | Name of the trouble ticket, typically a short description provided by the user that create the ticket
note | Note[] | The note(s) that are associated to the ticket.
priority | string | The priority of the trouble ticket and how quickly the issue should be resolved.
relatedEntity | RelatedEntity[] | An entity that is related to the ticket such as a bill, a product, etc.
relatedParty | RelatedParty[] | The related party(ies) that are associated to the ticket.
requestedResolutionDate | string (date-time) | The resolution date requested by the user
resolutionDate | string (date-time) | The date and time the trouble ticket was resolved
severity | string | The severity of the issue.
status | TroubleTicketStatusType | The current status of the trouble ticket
statusChange | StatusChange[] | The status change history that are associated to the ticket.Populated by the server
statusChangeDate | string (date-time) | The date and time the status changed.
statusChangeReason | string | The reason for changing the status
troubleTicketRelationship | TroubleTicketRelationship[] | A list of trouble ticket relationships (TroubleTicketRelationship [*]).
ticketType | string | represent a business type of the trouble ticket e.g.

## Document

> Document is a tangible output from an activity

**SID Domain:** Common

Property | Type | Description
--- | --- | ---
binaryAttachment | AttachmentRefOrValue[] | 
category | CategoryRef[] | 
characteristic | Characteristic[] | 
creationDate | string (date-time) | The date and time the document was created.
description | string | free-text description of the document
documentRelationship | DocumentRef[] | 
documentSpecification | DocumentSpecification | 
href | string | The URI for the object itself.
id | string | Identifier of an instance of the document.
lastUpdate | string (date-time) | The date and time the document was last modified.
lifecycleState | string | The life cycle state of the document.
name | string | A string used to give a name to the document
relatedEntity | RelatedEntity | 
relatedParty | RelatedParty[] | 
documentType | string | Name of the document type
version | string | A particular form or variety of an artefact that is different from others or from the original.

## Notification

> The notification is sent to each listener who has subscribed to receive it.

**SID Domain:** Common | **Extends:** Entity

Property | Type | Description
--- | --- | ---
eventId | string | Identifier of the event
eventTime | string (date-time) | Creation date of the event
eventType | string | Type of event
fieldPath | string | details which field is missing, its structure is quite similar to GET filter criteria
resourcePath | string | To indicate which entity is concerned
