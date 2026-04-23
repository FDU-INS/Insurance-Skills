# TM Forum SID v4 — Domain Taxonomy

The SID (Shared Information/Data) model organises telecoms entities into
functional domains. Each domain groups related entity families.

Source: TM Forum Open API Data Model v4.0.0 (Apache 2.0)

## Analytics

> Data analytics, AI models, and performance measurement entities.

**38 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
AppUsageDataAnalytics | 
BillingAccountAnalytics | 
BillingSubscriptionAnalytics | 
CustomerAnalytics | 
CustomerHealthStatsAnalytics | 
CustomerInteractionAnalytics | 
DeviceAnalytics | 
EligibilityOfferAnalytics | 
HLRSubscriberAnalytics | 
IOTObservationAnalytics | 
IOTPropertyAnalytics | 
InvoiceLineItemAnalytics | 
LocationAnalytics | 
MobileDataXDRAnalytics | 
NetworkQualityAnalytics | 
OrderLineItemAnalytics | 
PaymentAnalytics | 
PointofSaleAnalytics | 
PricePlanAnalytics | 
ProductUsageAnalytics | 
PublicTransportLineAnalytics | 
PublicTransportStationAnalytics | 
PublictransportationJourneyAnalytics | 
PurchaseActivityAnalytics | 
RatedEventAnalytics | 
RatingBillingPostpaidXDRAnalytics | 
RatingBillingPostpaidXDRSa.Analytics | 
RatingBillingPrepaidXDRAnalytics | 
SMSCXDRAnalytics | 
SensorAnalytics | 
Service-ProductOfferAnalytics | 
SocialMediaAnalytics | 
SwitchXDRAnalytics | 
ThingAnalytics | 
WorkforceAnalytics | 
eNodeBAnalytics | 
eUICCProfileAnalytics | 
eUICCUsageAnalytics | 

## Common

> Shared base types, geographic/address entities, events, documents, and cross-domain utilities.

**296 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
AbstractEnvironment | A managed abstract environment resource
AbstractEnvironmentDefinition | Abstract environment definition
Address | Structured textual way of describing how to find a Property in an urban area (country properties are often defined differently).
Addressable | Base schema for adressable entities
AdhocCollection | 
AdministrativeState | This is enumeration for Administrative state
AiModel | AiModel is a base class for defining the AiModel hierarchy
AiModelSpecification | AiModelSpecification is a class that offers characteristics to describe a type of service.
AlgorithmParams | 
AlgorithmThresholdRule | A threshold rule that is a reference to an algorithm
AlternateGeographicAddress | 
Any | 
ApplicableTimePeriod | The period of time for which Capacity or CapacityDemand applies.
Area | Area corresponds to a geographic area as a city, a locality, a district, etc.
AssetUserRole | The AssetUserRole is the detailed information concerning an individual user role
Association | Association is the class that describes a relationship between two or more entities or entity specifications based on a given association specification (relationship type).
AssociationRole | This embedded object represents the role and type of each entity involved in a relationship.
AssociationRoleSpec | This embedded object represents the role and type of each entity involved in a relationship.
AssociationRoleSpecification | This embedded object represents the role and type of each entity involved in a relationship.
AssociationSpecification | AssociationSpecification is an association class that describes a type of relationship between two entities.
Attachment | Complements the description of an element (for instance a product) through video, pictures...
Attribute | 
AttributeValuePair | 
BaseEvent | Base event with common attributes.
BasePlusEvent | Base event with common attributes.
BooleanArrayCharacteristic | A characteristic which the value is a boolean array
BooleanArrayCharacteristicValueSpecification | A specification for a characteristic for which the value is an array booleans
BooleanCharacteristic | A characteristic which value is a boolean
BooleanCharacteristicValueSpecification | A specification for a characteristic for which the value is a boolean
BusinessInteraction | 
CalendarPeriod | 
CancelOrder | A Order cancel is a type of task which can be used to place a request to cancel an order
CancelReservation | A Cancel Reservation is a type of task which can be used to place a request to cancel a reservation
Capacity | Specific ability of an entity measured in quantity and units of quantity over an extended period.
CapacityAmount | Quantity that defines the Capacity.
ChangeRequest | Change Request is a type of request which can be used for the management and control of Change Management process between a customer and a service provider or between a service provider and a partner
ChangeRequestCharacteristic | Characteristics of the change request to instantiate or to modify
ChangeRequestSpecification | Defines a set of attributes related to Change Request.
Channel | The channel to which the resource reference to.
Characteristic | Describes a given characteristic of an object or entity through a name/value pair.
Characteristic | Describes a given characteristic of an object or entity through a name/value pair.
CharacteristicRelationship | Another Characteristic that is related to the current Characteristic;
CharacteristicSpecification | This class defines a characteristic specification.
CharacteristicSpecificationBase | This class defines a characteristic specification.
CharacteristicSpecificationRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among Characteristic specifications.
CharacteristicValueSpecification | specification of a value (number or text or an object) that can be assigned to a Characteristic.
CollectionType | This is enumeration for CollectionType state
Comment | Indicates the comments entered on the alarm.
CommonComponents | 
CommunicationMessage | Communication message means a notification approach in the format of a message which can be dispatched (sent) to the certain user by the system with the content which can be felt and understood by the
CommunicationRequestCharacteristic | The values of parameters which are used in the content if the content contains them.
CompressionEnumType | Enumeration of supported compressions.
CompressionType | File compression type.
ConcreteEnvironmentMetaModel | A managed concrete environment resource metamodel resource
ConcreteEnvironmentMetaModelDefinition | Test environment metamodel definition
Configuration | #TODO
Consequence | A threshold crossing or a threshold ceased to be crossing results in a Performance consequence.
ContactMedium | Indicates the contact medium that could be used to contact the party.
ContentType | Base64 content structure.
DLImplementation | Provides the definition of a Distributed Ledger technology implemementation
DayOfMonthRecurrence | 
DayOfWeekRecurrence | 
DigitalIdentityContactMedium | Indicates the contact medium that could be used to contact the party.
DistributedLedger | Document is a tangible output from an activity
Document | Document is a tangible output from an activity
DocumentAttachment | Attachment refers to extensions or additional parts that is or may be attached to something (agreements, contracts, appointments) to perform a particular function.
DocumentCharacteristic | is a list of name value pairs that define the document characteristics.
DocumentRelationship | Another document that is related to the current document;
DocumentSpecification | A document specification reference
Duration | A time interval in a given unit of time
Edge | Edge is a directed edge connecting vertices in a directed Graph.
EdgeSpecification | A directed Edge connects Vertices in a Graph.
EdgeSpecificationCharacteristic | This class defines the characteristic features of an edge specification.
EdgeSpecificationCharacteristicRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among EdgeSpecificationCharacteristics.
EmailMedium | Describes an email that could be used to contact a party (an individual or an organization)
Entitlement | An Entitlement defines access levels to operate over a given function that can be included in an asset.
Entity | Base entity schema for use in TMForum Open-APIs
EntityAttachment | Complements the description of an entity through video, pictures...
EntityCatalog | The root entity for entity catalog management.
EntityCatalogItem | An EntityCatalogItem is an entity that allows any ProductOffering, ServiceCandidate, ResourceCandidate, or even any object inheriting from RootEntity, to be available to a catalog.
EntityCategory | The (entity) category resource is used to group entity catalog items in logical containers.
EntityRelationship | A uni-directionmal relationship from this entity to a target entity instance
EntitySpecRelationship | A migration, substitution, dependency or exclusivity relationship between/among entity specifications.
EntitySpecification | EntitySpecification is a class that offers characteristics to describe a type of entity.
EntitySpecificationRelationship | A migration, substitution, dependency or exclusivity relationship between/among entity specifications.
EntityValue | Base entity value schema for use in TMForum Open-APIs
Error | Used when an API throws an Error, typically with a HTTP error response-code (3xx, 4xx, 5xx)
ErrorMessage | represents an Error
Event | event with common attributes.
Execution | The base for all Execution resources
ExportJob | Represents a task used to export resources to a file
Extensible | Base Extensible schema for use in TMForum Open-APIs
ExternalIdentifier | An identification of an entity that is owned by or originates in a software system different from the current system, for example a ProductOrder handed off from a commerce platform into an order handl
ExternalReference | External reference of the individual or reference in other system
Feature | Configuration feature.
FeatureRelationship | Configuration feature
FeatureSpecification | Specification for resource, service or product features
FeatureSpecificationCharacteristic | Configuration feature characteristic specification.
FeatureSpecificationCharacteristicRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among FeatureSpecificationCharacteristics.
FeatureSpecificationRelationship | Relationship between feature specifications
FederatedIdentity | #TODO
FileDescriptor | 
FileDocument | A document accompanying an entity
FileTransferData | 
FileTransferStatus | 
FloatArrayCharacteristic | A characteristic which the value is a number array of format float
FloatArrayCharacteristicValueSpecification | A specification for a characteristic for which the value is a number array of format floating point
FloatCharacteristic | A characteristic which value is a float number
FloatCharacteristicValueSpecification | A specification for a characteristic for which the value is a floating point number
GSMACommons | 
GeneralTestArtifact | A managed general test artifact resource
GeneralTestArtifactDefinition | General test artifact definition
GeoJSON | GeoJSON: A single position
GeoJsonLineString | Container for GeoJson LineString: A collection of Points forming a connected line
GeoJsonMultiLineString | A container for GeoJSON MultiLineString: A collection of distinct LineStrings
GeoJsonMultiPoint | Container for GeoJSON MultiPoint: A collection of Points
GeoJsonPoint | Container for a GeoJSON Point: A single position
GeoJsonPolygon | Container for GeoJSON Polygon: An array of linear rings
GeographicAddress | Structured textual way of describing how to find a Property in an urban area (country properties are often defined differently).
GeographicAddressValidation | This resource is used to manage address validation request and response
GeographicLocation | A GeographicLocation is a pure-virtual super-class to the GeoJSON-aligned geometries of Point (addresses and locations), MultiPoint, LineString (streets, highways and boundaries), MultiLineString and
GeographicPoint | A GeographicPoint defines a geographic point through coordinates.
GeographicSite | 
GeographicSiteRelationship | 
GeographicSubAddress | Representation of a GeographicSubAddress It is used for addressing within a property in an urban area (country properties are often defined differently).
Granularity | Sampling rate of the collection or production of performance indicators.
Graph | Graph is a directed graph representing edges connecting vertices.
GraphRelationship | A relationship between Graphs.
HeaderItem | An item typically included in a request or response
HourPeriod | 
Hub | A Hub is used to subscribe to an event notification
ImportJob | Represents a task used to import resources from a file
Incident | An Incident is a record of an event that has altered the operational state of a entity (Resource, Service or Customers Product)
IndicatorType | This is enumeration for Indicator Type
IntegerArrayCharacteristic | A characteristic which the value is a number array of format integer
IntegerArrayCharacteristicValueSpecification | A specification for a characteristic for which the value is a number array of format integer
IntegerCharacteristic | A characteristic which value is an integer number
IntegerCharacteristicValueSpecification | A specification for a characteristic for which the value is an integer number
JeopardyAlert | A JeopardyAlert represents a predicted exception during a process that may cause a risk to complete successfully the process.
License | 
LineString | GeoJSON: A collection of Points forming a connected line
LocationCharacteristic | Name/value pairs, used to extra characterized the Area (e.g.
LocationCommons | 
MEntity | MEntity represents an entity that describes the common set of attributes shared by all concrete entities (e.g.
ManagedEntity | ManagedEntity represents an entity that describes the common set of attributes shared by all concrete entities (e.g.
ManagementJob | 
MapArrayCharacteristic | A characteristic which value is a string
MapArrayCharacteristicValueSpecification | A specification for a characteristic for which the value is an array of mapped objects
MapCharacteristic | A characteristic which value is a mapped object
MapCharacteristicValueSpecification | A specification for a characteristic for which the value is a mapped object
Measurement | A counter/KPI to be used by the threshold rule
MeasurementCollectionJob | Used to control the periodic collection of performance indicators, implemented as a sub-entity of the PM Measurement Job.
MeasurementJob | A PM measurement job is the administrative entity defined by a client application to perform a periodic activity related to PM data.
MeasurementProductionJob | Used to control the periodic collection of performance indicators, implemented as a sub-entity of the PM Measurement Job.
MeasurementProductionJobAVCN | This is a notification generated from the entity MeasurementProductionJob
MediumCharacteristic | Describes the contact medium characteristics that could be used to contact a party (an individual or an organization)
MergeTopologyGraphJob | Merges two or more Graphs into a single graph.
Milestone | Milestone represents an action or event marking a significant change or stage in a process like an order process.
Money | A base / value business entity used to represent money
Monitor | Monitoring of resources
MonitoredClassCriteria | Specifies a monitored object class (a string) in conjunction with a filter object.
MonitoredInstancesCriteria | List of monitored instances
MonitoredObjectsCriteria | Monitored objects are specified by the MonitoredObjectsCriteria.
MonthlyScheduleDayOfWeekDefinition | 
MultiLineString | A collection of distinct LineStrings
MultiPoint | A collection of Points
Multilingual | Serialization format for multilingual text
MultilingualConverter | REST resource for multilingual conversion from the base language
MutlilingualEntry | 
NetworkFunction | 
NonFunctionalTestExecution | REST resource for the non-functional test execution lifecycle
NonFunctionalTestModel | A managed non-functional test model resource
NonFunctionalTestModelDefinition | Non-functional test model definition
NonFunctionalTestResult | A managed non-functional test result resource
NonFunctionalTestResultDefinition | Non-functional test result definition
Note | Extra information about a given entity
Notification | The notification is sent to each listener who has subscribed to receive it.
NumberArrayCharacteristic | A characteristic which the value is a number array
NumberArrayCharacteristicValueSpecification | A specification for a characteristic for which the value is a number array with no specific format
NumberCharacteristic | A characteristic which value is a number
NumberCharacteristicValueSpecification | A specification for a characteristic for which the value is a number of no specific format
Object | 
ObjectArrayCharacteristic | A characteristic which the value is a object array
ObjectArrayCharacteristicValueSpecification | A specification for a characteristic for which the value is an array of objects
ObjectCharacteristic | A characteristic which value is an object
ObjectCharacteristicValueSpecification | A specification for a characteristic for which the value is any object
ObjectName | 
OnDemandCollection | 
PackingEnumType | Enumeration of supported packing/packaging.
PackingType | Specify if the output file(s) are to be packed.
PerceivedSeverity | This datatype lists the possible severities that can be allocated to a Alarm.
PerformanceAlarmSpecification | The specification of how to populate the alarm fields when generating a threshold crossing alarm.
PerformanceConsequence | A Consequence can be applied as a result of a threshold crossing or a threshold ceasing to be crossed
PerformanceIndicatorGroupSpecification | 
PerformanceIndicatorSpecRelationship | Type of relationship such as aggregation, migration, substitution, dependency, exclusivity
PerformanceIndicatorSpecification | Holds the definition of the requested Performance indicator including: its name, value type, collection type, description and units.
Permission | The Permission resource represents the entitlement given by an individual (granter) to another individual (user) to get access to a set of his owned manageable assets.
PhoneMedium | Describes a phone number that could be used to contact a party (an individual or an organization)
Place | Place reference.
Point | GeoJSON: A single position
Polygon | An array of linear rings
Privilege | A Privilege is a detailed information concerning an individual access entitlement.
ProcessFlow | 
ProtocolTransferData | 
ProvisioningArtifact | A managed provisioning artifact resource
ProvisioningArtifactDefinition | Provisioning artifact definition
Quantity | An amount in a given unit
QuantityType | Representation of a quantity of something.
Receiver | Receivers of the communication message.
Record | A record in a worklog.
RelatedChannel | Related channel to another entity.
RelatedEntity | A reference to an entity, where the type of the entity is not known in advance.
RelatedObject | Defines objects linked with trouble ticket.
RelatedPlace | A Place and an associated role as installation adress, delivery address, etc....
ReportingPeriod | Possible values for the reporting period
Request | A response to a request
Reservation | reservation api resource
ReservationItem | An identified part of the reservation.
Resolution | The way one or more change request has been implementation through a direct remedy or task
Response | A response to a request
ResponseError | Used when an API throws an Error, typically with a HTTP error response-code (3xx, 4xx, 5xx)
RetrieveGeographicLocation | 
RetrieveLocationRelation | 
ScheduleDefinition | The schedule definition for running jobs.
Sender | Sender of the communication message.
SimpleThresholdRule | A threshold rule that is based on explicit definition of attributes that represent a Boolean expression
SiteRelationship | 
SpecCharRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among productSpecCharacteristics.
SpecCharacteristic | A characteristic quality or distinctive feature of a Specification.
SpecCharacteristicValue | A number or text that can be assigned to a SpecCharacteristic
SpecificationCharacteristic | A characteristic quality or distinctive feature of a Specification.
SpecificationCharacteristicRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among productSpecCharacteristics.
SpecificationCharacteristicValue | A number or text that can be assigned to a SpecificationCharacteristic
StatusChange | Holds the status notification reasons and associated date the status changed, populated by the server
Stream | 
Street | A street is a road in a city or locality that has buildings that are usually close together along one or both sides
StreetSegment | StreetSegment corresponds to a part of a street referenced by a number or a set of number.
StringArrayCharacteristic | A characteristic which the value is a string array
StringArrayCharacteristicValueSpecification | A specification for a characteristic for which the value is an array of strings
StringCharacteristic | A characteristic which value is a string
StringCharacteristicValueSpecification | A specification for a characteristic for which the value is a string
SubAddress | Representation of a SubAddress It is used for addressing within a property in an urban area (country properties are often defined differently).
SupportedLanguages | Enumeration for the supported languages in JADL multilingual support
Task | A step or task along in the process of implementation a Change Request.
TaskFlow | 
TaskFlowRelationship | Describes relationship between taskFlow
TaxDefinition | Reference of a tax definition.
Template | 
TestAgreement | 
TestCase | A managed test case resource
TestCaseDefinition | Test case definition
TestCaseExecution | REST resource for the test case execution lifecycle
TestCaseResult | A managed test case result resource
TestCaseResultDefinition | Test case result definition
TestContact | 
TestDataInstance | A managed test data instance resource
TestDataInstanceDefinition | Test data instance definition
TestDataSchema | A managed test data schema resource
TestDataSchemaDefinition | Test data schema definition
TestEnvironmentAllocationExecution | REST resource for test environment allocation lifecycle
TestEnvironmentProvisioningExecution | REST resource for test environment provisioning lifecycle
TestExecution | The base for all Test Execution resources
TestResourceAPI | A managed test resource API resource
TestResourceAPIDefinition | Test resource API definition
TestResult | Base schema for test results
TestScenario | A managed test scenario resource
TestScenarioDefinition | Test scenario definition
TestSuite | A managed test suite resource
TestSuiteDefinition | Test suite definition
TestSuiteExecution | REST resource for the test suite execution lifecycle
TestSuiteResult | A managed test case result resource
TestSuiteResultDefinition | Test suite result definition
TestVersion | 
Threshold | A threshold base entity containing threshold rules.This entity is mandatoryThis entity is extendableThis entity does not generate Object Creation notifications (NA)This entity generates Object Deletio
ThresholdCondition | 
ThresholdJob | 
ThresholdRule | ThresholdRule A base entity for concrete definition of thresholds.This datatype is abstract
ThresholdType | The Threshold Type may be either LogicDefinition or PreDefined
Ticket | A trouble ticket represents a record used for reporting and managing the resolution of resource problems
TicketRelationship | Represents a relationship between trouble tickets
TimePeriod | A period of time, either as a deadline (endDateTime only) a startDateTime only, or both
Topic | Is a event channel provided by the Event Streaming API
TopologyDiscoveryJob | Represents a task used to discover topology from providers
TroubleTicket | A trouble ticket is a record of an issue that is created, tracked, and managed by a trouble ticket management system
TroubleTicketRelationship | Represents a relationship between trouble Trouble Tickets
User | Generic User structure used to define commonalities between sub concepts of PartyUser and Financial User.
UserAsset | 
UserRole | A UserRole defines access levels to operate over a given function that can be included in an asset.
Userinfo | 
ValidFor | 
Value | 
Vertex | A Vertex is connected by directed Edges to other vertices in a Graph.
VertexSpecification | A Vertex is connected by directed Edges to other vertices in a Graph.
VertexSpecificationCharacteristic | This class defines the characteristic features of a vertex specification.
VertexSpecificationCharacteristicRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among VertexSpecificationCharacteristics.
WorkLog | A record of the work performed on the change request during the investigation and resolution process.

## Customer

> Customer management, billing, payment, ordering, quotes, shopping carts, and risk assessment.

**116 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
AccountPaymentMethod | Reference an internal account that could be billed directly to perform the payment.
AccumulatedBalance | Represents and tracks the aggregated amount remained or owed in certain account which is owned by certain customer for a set of buckets.
AdjustBalance | The AdjustBalance resource allows adjustments to be made to the original BalanceTopup e.g.
AppliedBillingRate | An applied billing rate presented on a bill.
AppliedBillingRateCharacteristic | An applied billing rate has dynamic characteristics according to the its type (characteristics are based on the service type, line of business or on others parameters)
AppliedBillingTaxRate | The applied billing tax rate represents taxes applied billing rate it refers to.
AppliedCustomerBillingRate | A customer bill displays applied billing rates created before or during the billing process.
AppliedPartyBillingRate | An applied billing rate presented on a party bill.
AppliedPayment | The applied payment is the result of lettering process.
Appointment | An Appointment is an arrangement to do something or meet someone at a particular time, at a place (for face to face appointment) or in a contact medium (for phone appointment).
AppointmentStateValues | 
Authorization | If special discount or special product offering price or specific condition need an approval for ISP sale representative it is described here.
AuthorizePayment | Task resource for operation authorize payment
BalanceAction | an abstract resource.
BalanceAdjustment | #TODO
BalanceDeduct | The Balance Deduct task resource is a detailed description of deduction operation.
BalanceDeductRollback | The Rollback Balance Deduct task resource is a detailed description of rollback deduction
BalanceReserve | The Balance Reserve Operation resource is a detailed description of a balance reserve operation requested over a subscription
BalanceTransfer | The BalanceTransfer resource is a detailed description of credit transfer operation requested between two buckets (reference to products owned by customers and consuming credit when using a service).
BalanceUnreserve | The Balance Unreserve Operation resource is a detailed description of a balance unreserve operation requested over a subscription
BankAccountDebit | A bank account debit method of payment.
BankAccountTransfer | A bank transfer method of payment.
BankCard | A bank card method of payment.
BankCardDetails | Detailed information for a bank card
BankCardMethod | 
Bill | The Bill entity is used to model a bill (aka an invoice).
BillCycle | A detailed description of a billing cycle and the various sub steps of a billing cycle.
BillCycleSpec | A detailed description of a billing cycle and the various sub steps of a billing cycle.
BillCycleSpecification | A detailed description of a billing cycle and the various sub steps of a billing cycle.
BillFormat | A detailed description of the way in which a bill is presented.
BillPresentationMedia | A mean of communicating a bill, supported by the associated bill format.
BillStructure | The structure of the bill for party accounts (billing or settlement).
BillingAccount | A party account used for billing purposes.
BillingCycleSpecification | A detailed description of when to initiate a billing cycle and the various sub steps of a billing cycle.
Bucket | A bucket (called UsageVolumProduct in the SID Model) represents and tracks a quantity of usage (remaining or consumed).
BucketPaymentMethod | Reference to a bucket that could be used to perform the payment, especially in the pre-paid environment.
BucketStatusExampleType | Possible values for the bucket status are (for example active,suspended,expired)
CartItem | An identified part of the shopping cart.
CartItemRelationship | Relationship among cart items mainly other than hierarchical relationships such as "relyOn", "dependentOn", "shipping" etc.
CartPrice | An amount, usually of money, that represents the actual price paid by the customer for this item.
CartTerm | 
Cash | A cash method of payment.
CashDetails | Cash has no additional data, but it could be extended to add information (e.g.: the cashier who took the payment, the person who paid, etc)
CashMethod | 
Check | A check method of payment.
CheckDetails | Detailed information of a check
CheckMethod | 
CounterType | Valid values for this type
CreditProfile | Credit profile for the party (containing credit scoring, ...).
Customer | 
Customer360 | 
CustomerBill | The customer bill.
CustomerBillOnDemand | This resource is used to manage the creation request of a customer bill in real-time (on demand).
CustomerBillRunType | Recommended Enumeration Type (not formal forced in standard): Valid values for the runType of a bill.
DigitalWallet | A digital wallet method of payment.
DigitalWalletDetails | Detailed information of a check
DigitalWalletMethod | 
DirectDebit | Direct Debit is a fully automated payment instrument which is generally used for recurrent payments.
Disability | Lack or inadequate strength or ability.
ImpactedBucket | A resource that references other buckets that have been impacted by the action of type TopupBalance,AdjustBalance,TransferBalance or ReserveBalance
ImpactedBucketItem | a resource used by the ImpactedBucket resource to capture the impact of a ImpactedBucket
InitiatePayment | Task resource for operation initiate payment
LoyaltyPaymentMethod | Reference to an account in a loyalty system that could be used to perform the payment.
OrderItem | An identified part of the order.
OrderItemPrice | An amount, usually of money, that represents the actual price paid by the Customer for this item or this order
OrderItemRelationship | 
OrderPrice | An amount, usually of money, that represents the actual price paid by the Customer for this item or this order
OrderRelationship | 
OrderTerm | Description of a productTerm linked to this orderItem.
PartyRoleProductOfferingRiskAssessment | This is a task resource allowing assessment of the risks associated with a party or party role that considers acquiring a specific product offering
PartyRoleRiskAssessment | This is a task resource allowing assessment of the risks associated with a party role
Payment | The Payment resource represents a performed payment.
PaymentItem | The paymentItem is the result of lettering process.
PaymentMethod | A Payment Method is a pure-virtual super-class that defines a specific method of payment such as Direct Debit, Cash, Digital Wallet,Tokenized Card, Bank Account Transfer, Bank Account Debit, Bank Card
PaymentPlan | Defines a plan for payment (when a party wants to spread his payments)
PaymentStatusExampleType | Possible values for the status of a payment
PointOfInteraction | POI consists of hardware and software which enables a Cardholder and/or an Acceptor to perform a Local Card transaction.
Price | Provides all amounts (tax included, duty free, tax rate), used currency and percentage to apply for Price Alteration.
PriceType | Describes the type of price (ex: oneTime, recurring, etc)
ProductOfferingRiskAssessment | This is a task resource allowing assessment of the risks associated with a product offering.
ProductOrder | A Product Order is a type of order which can be used to place an order between a customer and a service provider or between a service provider and a partner and vice versa,
ProductOrderItem | An identified part of the order.
ProductOrderRiskAssessment | This is a task resource allowing assessment of the risks associated with a product order - presumably submitted by a party role and containing one or more product offerings
ProductRelationship | Linked bucket to the one instantiate, such as [isAggregated] if the bucket is a part of other or [aggregator] is the bucket holds others
QueryProductRecommendation | Recommendation API is used to recommend offering quickly based on the history and real-time context of customer.
Quote | Quote can be used to negotiate service and product acquisition or modification between a customer and a service provider.
QuoteItem | A quote items describe an action to be performed on a productOffering or a product in order to get pricing elements and condition.
QuoteItemRelationship | Used to describe relationship between quote item.
QuotePrice | Description of price and discount awarded
RecurringPeriodType | Valid values for this type
Refund | The Refund resource represents a performed Refund.
RefundStatusExampleType | Possible values for the status of a refund
RelatedTopupBalance | Related Entity reference.
ReserveBalance | The ReserveBalance resource allows adjustments to be made to the original BalanceTopup eg increment the amount, alter the recharge periodicity
RiskAssessment | This is a generalized task resource allowing assessment of risks - it is expected that the resource will be specialized to reflect specific risks, such as risks associated with a party, or with an ord
RiskAssessmentResult | This resource reflects the risk assessment
RiskScore | This resource reflects a score for a specific risk
RiskType | Types of risk that can be assessed
SearchTimeSlot | This task resource is used to retrieve available time slots.
SettlementMethod | Is the way in which the CSP provides the payment
SettlementNoteAdvice | The settlement is about transferring money receiving by a CSP to a partner.
SettlementNoteImage | Is the image of the settlement note
SettlementNoteItem | Concerns a product identified by its catalogue reference.
ShoppingCart | Shopping Cart resource is used for the temporarily selection and reservation of product offerings in e-commerce, call center and retail purchase.
ShoppingCartRiskAssessment | This is a task resource allowing assessment of the risks associated with a shopping cart - presumably created by a party role and containing one or more product offerings
TaxItem | A tax item is created for each tax rate and tax type used in the bill.
TimeSlot | 
TokenizedCard | A Tokenized Card method of payment.
TokenizedCardDetails | Detailed information for a stored tokenized card
TokenizedCardMethod | 
TopupBalance | Represents a detailed description of a recharge operation requested over a bucket (defined by a specific product or reference to a product (i.e.: a commercial id such as an msisidn) and a service type
TransferBalance | The TransferBalance resource is a detailed description of credit transfer operation requested between two buckets (reference to products owned by customers and consuming credit when using a service).
UsageType | Valid values for the usage type are
Voucher | A voucher method of payment.
VoucherDetails | Detailed information of a voucher
VoucherMethod | 

## Customer360

> Unified customer view aggregating data from multiple domains.

**14 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
Customer360AccountVO | Generic Account structure used to define commonalities between sub concepts of PartyAccount and Financial Account.
Customer360AgreementVO | An agreement represents a contract or arrangement, either written or verbal and sometimes enforceable by law, such as a service level agreement or a customer price agreement.
Customer360AppointmentVO | An Appointment is an arrangement to do something or meet someone at a particular time, at a place (for face to face appointment) or in a contact medium (for phone appointment).
Customer360CustomerBillVO | The customer bill.
Customer360CustomerVO | 
Customer360InteractionItemVO | 
Customer360LoyaltyBalanceVO | A loyalty balance, containing a balance unit and value.
Customer360ProductOrderVO | A Product Order is a type of order which can be used to place an order between a customer and a service provider or between a service provider and a partner and vice versa,
Customer360ProductValueVO | A product offering procured by a customer or other interested party playing a party role.
Customer360PromotionVO | Promotion Resource is used to provide the additional discount, voucher, bonus or gift to the customer who meets the pre-defined criteria.
Customer360QuoteVO | Quote can be used to negotiate service and product acquisition or modification between a customer and a service provider.
Customer360ServiceProblemVO | The problem information for Middle B which is abstracted in the service layer from the issued event information by First B
Customer360TroubleTicketVO | A trouble ticket is a record of an issue that is created, tracked, and managed by a trouble ticket management system
Customer360UsageSpecificationVO | A detailed description of a usage event that are of interest to the business and can have charges applied to it.

## EngagedParty

> Party (Individual/Organization), Party Roles, Accounts, Agreements, Partnerships, and identity management.

**113 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
-  | A Credential based on a login and a password.
A credential provided by a resource like a PKI key | A Credential based on a login and a password.
Account | Generic Account structure used to define commonalities between sub concepts of PartyAccount and Financial Account.
AccountBalance | Balances linked to the account
AccountDirectDetails | 
AccountDirectMethod | A payment method using an internal account that could be billed directly to perform the payment
AccountRelationship | Significant connection between accounts.
Agreement | An agreement represents a contract or arrangement, either written or verbal and sometimes enforceable by law, such as a service level agreement or a customer price agreement.
AgreementAttachment | Represents a complementary piece of information to describe the agreement.
AgreementAuthorization | A business participant that is responsible for approving the agreement.
AgreementItem | A part of the agreement expressed in terms of a product offering and possibly including specific terms and conditions.
AgreementSpecCharacteristic | A characteristic quality or distinctive feature of an agreement.
AgreementSpecCharacteristicValue | A number or text that can be assigned to an agreement specification characteristic.
AgreementSpecification | A template of an agreement that can be used when establishing partnerships
AgreementSpecificationRelationship | A relationship between agreement specifications.
AgreementTermOrCondition | Aspects of the agreement not formally specified elsewhere in the agreement and that cannot be captured elsewhere in a formal notation, or automatically monitored and require a more human level of mana
AiContract | An Ai Contract represents a contract or arrangement, either written or verbal and sometimes enforceable by law, such as a service level agreement or a customer price agreement.
AiContractSpecification | A template of an agreement that can be used when establishing partnerships
AiContractViolation | 
AlternateShipmentProposal | Alternate shipment proposal is used when the requested shipment is not valid as specified in the request.
AlternateWorkProposal | Alternate work proposal is used when the requested unit of work is not valid as specified in the request.
BankAccount | Describes the information of a bank account
BankAccountDebitDetails | Detailed information for a bank account debit.
BankAccountDebitMethod | 
BankAccountTransferDetails | Detailed information for a bank account debit.
BankAccountTransferMethod | 
BiometricCredential | A Credential based on a login and a password.
CancelWorkOrder | 
CheckShipmentQualification | CheckShipmentQualification is used to validate the eligibility of specific shipments.
CheckShipmentQualificationItem | A ShipmentQualificationItem relates to a specific shipment being checked in a qualification operation.
CheckWorkQualification | CheckWorkQualification is used to validate specific units of work
CheckWorkQualificationItem | A WorkQualificationItem relates to a specific unit of work being checked in a qualification operation.
Contact | An individual or an organization used as a contact point for a given account and accessed via some contact medium.
Credential | Credential is a class that allow to describe an authentification method.
DigitalIdentity | DigitalIdentity is a class that allow to describe a digital identity for an individual or a resource or a specific party role.
FinancialAccount | An account of money owed by a party to another entity in exchange for goods or services that have been delivered or used.
Individual | Individual represents a single human being (a man, woman or child).
IndividualIdentification | Represents our registration of information used as proof of identity by an individual (passport, national identity card, drivers license, social security number, birth certificate)
InteractionItem | 
InteractionRelationship | 
LanguageAbility | Ability of an individual to understand or converse in a language.
Organization | Organization represents a group of people identified by shared interests or purpose.
OrganizationChildRelationship | Child references of an organization in a structure of organizations.
OrganizationIdentification | Represents our registration of information used as proof of identity by an organization
OrganizationParentRelationship | Parent references of an organization in a structure of organizations.
OtherName | To keep track of other names (for example the old name of a woman before marriage or an artist name)
OtherNameIndividual | Keeps track of other names, for example the old name of a woman before marriage or an artist name.
OtherNameOrganization | Keeps track of other names, for example the old name of an organization.
Partner | The part played by a party in a given context.
Partnership | A partnership represents a formalized collaboration between various parties, each party playing a role in the partnership.
PartnershipSpecification | A partnership specification contains all the information for the setup of a partnership of a given kind.
PartnershipType | A partnership type contains all the information for the setup of a partnership of a given kind.
Party | Generic Party structure used to define commonalities between sub concepts of Individual and Organization.
PartyAccount | Account used for billing or for settlement purposes concerning a given party (an organization or an individual).
PartyBill | 
PartyCreditProfile | An individual might be evaluated for its worthiness and this evaluation might be based on a credit rating given by a credit agency.
PartyInteraction | 
PartyInteractionStatusExampleType | Possible values for the status of party interaction (for example: open,inProgress,completed)
PartyPrivacyAgreement | A specific type of agreement that formalizes the privacy profiles requested for a party
PartyPrivacyAgreementStatusExampleType | Possible values for the status of party privacy profile agreement (for example: intialized, inProgress, rejected, pendingUpdate, validated)
PartyPrivacyProfile | A Party Privacy Profile represents the set of Privacy settings defined for a Party
PartyPrivacyProfileCharacteristic | A characteristic for an instantiated party profile, where the value indicates the allowed use of the characteristic
PartyPrivacyProfileSpecification | Party Privacy Profile Specification serves as a template for creating Privacy Profiles.
PartyPrivacyProfileSpecificationCharacteristic | A characteristic of the party privacy profile, whose value(s) would be supplied at runtime.
PartyPrivacyProfileSpecificationStatusExampleType | Possible values for the status of party privacy profile Specification (for example: inDesign, active, rejected, retired)
PartyPrivacyProfileStatusExampleType | Possible values for the status of party privacy profile (for example: created, terminated)
PartyPrivacyRoleSpecification | A PartyPrivacyRoleSpecification represents a specification of a role defined in the context of a given privacy spesification, such as Customer, User.
PartyRole | The part played by a party in a given context.
QueryShipmentQualification | QueryShipmentQualification is used to retrieve a list of shipments that are valid in the context of the interaction (place, party, shipment parameters, ...).
QueryWorkQualification | QueryWorkQualification is used to retrieve a list of units of work that are valid in the context of the interaction
RelatedParty | Related Entity reference.
RelatedPartyWithContactInfo | Related party specialization that includes contact information
RelatedShipment | A related shipment addressable entity
RelatedShippingOrder | A related shipping order addressable entity
RelatedWorkOrderItem | RelatedWorkOrderItem (WorkOrder item).
RoleSpecification | A RoleSpecification represents a specification of a role.
RoleType | A RoleType represents the type of a PartyRole, defined in the context of a given type of partnership, such as Buyer, Seller.
Rule | 
SLA | Part of a business agreement between a Service Provider and a Customer, quantitatively specifying the service performance level the Service Provider commits to deliver.
SLAViolation | 
ServiceLevelAgreement | Service Level Agreement
ServiceLevelAgreementViolation | 
SettlementAccount | A party account used for settlement purposes.
Shipment | 
ShipmentEligibilityUnavailabilityReason | Reason for eligibility result if the ShipmentQualification result is no (meaning the Shipment is not valid)
ShipmentItem | 
ShipmentQualification | ShipmentQualification is used to perform a validation on shipment parameters and options, in relation to a specific carrier.
ShipmentQualificationItem | A ShipmentQualificationItem relates to a specific shipment being checked in a qualification operation.
ShipmentQualificationItemRelationship | Structure used to describe relationship between shipmentQualification items from the same shipmentQualification .
ShipmentSpecification | Definition of the nature of a Shipment.
ShipmentSpecificationRelationship | A migration, substitution, dependency or exclusivity relationship between/among entity specifications.
ShippingInstruction | Instructions and details for the carrier
ShippingOrder | A Shipping Order is a document used by a business to specify what items are to be transferred from a storage location or warehouse to which person and to which new location.
ShippingOrderItem | A list of shipping order items
ShippingOrderProduct | The product order item
SignatureRequiredByType | Possible values for the signature requirement upon receiving the shipment
Skill | Skills evaluated for an individual with a level and possibly with a limited validity when an obsolescence is defined (Ex: the first-aid certificate first level is limited to one year and an update tra
TaxExemptionCertificate | A tax exemption certificate represents a tax exemption granted to a party (individual or organization) by a tax jurisdiction which may be a city, state, country,...
TokenCredential | A Credential based on a token.
Violation | 
Work | 
WorkEligibilityUnavailabilityReason | Reason for eligibility result if the WorkQualification result is no (meaning the Unit of Work is not valid)
WorkOrder | 
WorkOrderItem | An identified part of the order.
WorkPrice | An amount, usually of money, that represents the actual price paid by the Customer for this item or this order.
WorkQualification | 
WorkQualificationItem | A WorkQualificationItem relates to a specific unit of work being checked in a qualification operation.
WorkQualificationItemRelationship | Structure used to describe relationship between WorkQualification items from the same WorkQualification .
WorkQualificationRelationship | Structure used to describe relationship between WorkQualification item from the same WorkQualification.
WorkRelationship | 
WorkSpecification | Definition of the nature of a Work Unit.
WorkSpecificationRelationship | A migration, substitution, dependency or exclusivity relationship between/among entity specifications.
WorkforceEmployeeAssignment | Represents an assignment of a particular WorforceEmployeeRole for a particular unit of work in a specific timeframe.

## Iot

> Internet of Things device management and telemetry.

**0 entities** (excluding Ref wrappers and state types)

## MarketingSales

> Market segments, competitors, sales leads, and loyalty programs.

**2 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
SalesLead | A Sales Lead is the identification of a person or organization that has an interest in the goods and/or services provided in the prospect of them becoming Customers with one or more Subscriptions.
SalesLeadPriorityType | Urgency of working this salesLead

## Product

> Product catalog, offerings, specifications, inventory, usage, and promotions.

**67 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
AlternateProduct | In the context of a product offering qualification, this data structure is useful to describe alternate product than can be proposed
AlternateProductOfferingProposal | Alternate product Offering proposal is used when the requested product offering is not available with characteristic and date asked for.
BundledProductOffering | A type of ProductOffering that belongs to a grouping of ProductOfferings made available to the market.
BundledProductOfferingOption | A set of numbers that specifies the lower and upper limits for a ProductOffering that can be procured as part of the related BundledProductOffering.
BundledProductOfferingPriceRelationship | This represents a bundling pricing relationship, allowing a price to be composed of multiple other prices (e.g.
BundledProductSpecification | A type of ProductSpecification that belongs to a grouping of ProductSpecifications made available to the market.
CancelOrder | A Order cancel is a type of task which can be used to place a request to cancel an order
CancelProductOrder | Request for cancellation an existing product order
Catalog | A collection of Product Offerings, intended for a specific DistributionChannel, enhanced with additional information such as SLA parameters, invoicing and shipping details
Category | The category resource is used to group product offerings, service and resource candidates in logical containers.
ConsumptionSummary | The consumption counters (called ConsumptionSummary in the SID model) detail for example the different kind of consumption done on the bucket.
DLImplementation | Provides the definition of a Distributed Ledger technology implemementation
EligibilityUnavailabilityReason | Reason for eligibility result if the productOfferingQualification result is no (meaning the productOffering or productSpec is not available).
LoyaltyAccount | A loyalty account, containing loyalty balances.
LoyaltyAction | Contains information on a loyalty action that should be applied should certain conditions be met for a loyalty rule and program.
LoyaltyBalance | A loyalty balance, containing a balance unit and value.
LoyaltyCondition | A condition, comprised of a attribute that will be tested against a value.
LoyaltyEvent | A loyalty event notification.
LoyaltyEventType | An event type used to match filter incoming loyalty events.
LoyaltyExecutionPoint | A record of a loyalty action that was applied.
LoyaltyProgramMember | A person or group that opts in to a loyalty program.
LoyaltyProgramProduct | An instance of a loyalty program specification, linked to a specified loyalty member.
LoyaltyProgramProductSpec | A reference to a loyalty program specification.
LoyaltyRule | Loyalty rule, containing conditions, event types and actions.
LoyaltyRuleAction | Resource containing a the ID of a action to link to a loyalty rule.
LoyaltyRuleCondition | Resource containing a the ID of a condition to link to a loyalty rule.
LoyaltyRuleEventType | Resource containing a the ID of a event type to link to a loyalty rule.
NetworkProduct | An instantiated network product (specialization of a product) subscribed by a customer.
PriceAlteration | Is an amount, usually of money, that modifies the price charged for an order item.
PricingLogicAlgorithm | The PricingLogicAlgorithm entity represents an instantiation of an interface specification to external rating function (without a modeled bahavior in SID).
Product | A product offering procured by a customer or other interested party playing a party role.
ProductCharacteristic | Characteristics of the product to instantiate or to modify
ProductInventoryRelationship | Linked products to the one instantiate, such as [bundled] if the product is a bundle and you want to describe the bundled products inside this bundle; [reliesOn] if the product needs another already o
ProductOffering | Represents entities that are orderable from the provider of the catalog, this resource includes pricing information.
ProductOfferingPrice | Is based on both the basic cost to develop and produce products and the enterprises policy on revenue targets.
ProductOfferingPriceRelationship | Describes a non-composite relationship between product offering prices.
ProductOfferingQualification | ProductOfferingQualification is used to perform a commercial eligibility.
ProductOfferingQualificationItem | 
ProductOfferingTerm | A condition under which a ProductOffering is made available to Customers.
ProductPrice | An amount, usually of money, that represents the actual price paid by a Customer for a purchase, a rent or a lease of a Product.
ProductRelationship | Linked products to the one instantiate, such as [bundled] if the product is a bundle and you want to describe the bundled products inside this bundle; [reliesOn] if the product needs another already o
ProductRequest | 
ProductRestriction | In the context of a product order or a product offering qualification, this data structure captures the product information useful to order or qualified an existing subscribed product or to a new one.
ProductSpecification | Is a detailed description of a tangible or intangible object made available externally in the form of a ProductOffering to customers or other parties playing a party role.
ProductSpecificationCharacteristic | A characteristic quality or distinctive feature of a ProductSpecification.
ProductSpecificationCharacteristicRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among productSpecificationCharacteristics.
ProductSpecificationCharacteristicValueUse | A use of the ProductSpecificationCharacteristicValue by a ProductOffering to which additional properties (attributes) apply or override the properties of similar properties contained in ProductSpecifi
ProductSpecificationRelationship | A migration, substitution, dependency or exclusivity relationship between/among product specifications.
ProductTerm | Description of a productTerm linked to this product.
Promotion | Promotion is used to provide the additional discount, voucher, bonus or gift to the customer who meets the pre-defined criteria.
PromotionAction | Action of the promotion.
PromotionCriteria | Set of criteria to be followed by all parties.
PromotionCriteriaGroup | Set of group criteria to promotion.
PromotionPattern | Contains the conditions and benefits of the promotion toan eligible party
QualificationItemRelationship | Structure used to describe relationship between productOfferingQualification item from the same ProductOfferingQualification.
QueryUsageConsumption | An QueryUsageConsumption allows to manage the calculation request of an usage consumption
QuoteTerm | Description of aproduct Term linked to this quoteItem.
RatedProductUsage | An occurrence of employing a product for its intended purpose with all rating details
Recommendation | Recommendation API is used to recommend offering quickly based on the history and real-time context of customer.
RecommendationItem | A list of recommendation items.
RelatedProductOrderItem | RelatedProductOrderItem (ProductOrder item) .The product order item which triggered product creation/change/termination.
Usage | An occurrence of employing a Product, Service, or Resource for its intended purpose, which is of interest to the business and can have charges applied to it.
UsageCharacteristic | Provides the value of a given characteristic
UsageConsumption | An usage consumption enables to know at a given point the balances and the consumption counters related to various buckets (SMS, Voice, Data for example).
UsageSpecCharacteristic | A detailed description of an attribute that defines a particular type of usage, described by its name, category, type, presence and a set of allowed values
UsageSpecCharacteristicValue | A value that can be assigned to a UsageSpecCharacteristic.
UsageSpecification | A detailed description of a usage event that are of interest to the business and can have charges applied to it.

## Resource

> Physical and logical resources, resource catalog, alarms, and inventory.

**79 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
AckAlarms | Task resource for the acknowledge alarms operation
AdjustProductStock | AdjustProductStock is used to log and execute on or several Product Stock level change
AdjustProductStockItem | A list of AdjustProductStock items.
AffectedService | 
Alarm | This resource represents an alarm supporting the information model defined in ITU-T X.733.
AlarmType | Categorizes the alarm (X.733 8.1.1, 3GPP TS 32.111-2 Annex A)
AlarmedObject | Identifies the managed object instance associated with the alarm.
AlternateProductStock | AlternateProductStock is used to log and execute Alternate about product stock availability
AppliedCapacityAmount | The amount of ResourceCapacityDemand applied to a CapacityAmount.
AppliedResourceCapacity | 
CancelResourceOrder | Request for cancellation an existing resource order
CancelResourceReservation | 
CategoryType | 
CheckProductStock | CheckProductStock is used to log and execute check about product stock availability
CheckProductStockItem | CheckProductStockItem is used to log and execute query about one product (or configured product) stock availability
ClearAlarms | Task resource for clear alarms operation
CommentAlarms | Task resource for comment alarms operation
ConcreteResource | 
ConcreteResourceMapping | Individual mapping from an abstract resource to a list of concrete resources
Connection | An edge in a resource graph.
ConnectionSpecification | A specification for an edge in a resource graph.
CorrelatedAlarm | Indicates the alarms attached to this alarm as correlated alarms from a correlation point of view.
CrossedThresholdInformation | Identifies the details of the threshold that has been crossed.
DataAccessEndpoint | This is the endpoint exposed by the IoT Device to authorized users.
Device | 
DeviceCommons | 
GroupAlarms | Task resource for group alarms operation
Heal | Task Resource used to request healing of a Resource Function
IotDataEvent | #TODO
IotDevice | #TODO
IotDeviceSpecification | #TODO
IotManagementEvent | Generic IotManagementEvent structure used to define commonalities between sub concepts of PartyIotManagementEvent and Financial IotManagementEvent.
IotService | #TODO
IotServiceSpecification | #TODO
LogicalResource | Logic resource is a type of resource that describes the common set of attributes shared by all concrete logical resources (e.g.
LogicalResourceSpecification | This is an example of a derived class of ResourceSpecification, and is used to define the invariant characteristics and behavior (attributes, methods, constraints, and relationships) of a LogicalResou
MacAddressType | #TODO
Migrate | Task resource used to request migration of the Resource Function
ParentAlarm | Indicates the alarms attached to this alarm as parent alarms from a correlation point of view.
PerceivedSeverity | Lists the possible severities that can be allocated to an Alarm.
PerformanceAlarmSpecification | The specification of how to populate the alarm fields when generating a threshold crossing alarm
PhysicalResource | Physical resource is a type of resource that describes the common set of attributes shared by all concrete physical resources (e.g.
PhysicalResourceSpecification | This is an example of a derived class of ResourceSpecification, and is used to define the invariant characteristics and behavior (attributes, methods, constraints, and relationships) of a PhysicalReso
ProbableCause | This resource represents Probable Cause values defined in ITU-T X.733 and 3GPP TS 32.111-2 Annex B.
ProductStock | ProductStock is a base class for defining a product (or configured product with values characteristic) stock level.
ProductStockRelationship | Linked product stock with a type relationship.
ProductStockUsageType | Possible values for the usage of the stock level - This is illustrative
QueryProductStock | QueryProductStock is used to query product stock availability
RequestedPeriod | The period of time for which user requested to use the resources.
ReserveProductStock | ReserveProductStock is used to request a product stock reservation
ReserveProductStockItem | ReserveProductStockItem is used to request a stock reservation item for a product
Resource | Resource is an abstract entity that describes the common set of attributes shared by all concrete resources (e.g.
ResourceCandidate | ResourceCandidate is an entity that makes a resource specification available to a catalog.
ResourceCapacityDemand | the amount of capacity that is planned to be consumed or has been consumed.
ResourceCatalog | The root entity for resource catalog management.
ResourceCategory | The (resource) category resource is used to group resource candidates in logical containers.
ResourceCharacteristic | 
ResourceEntity | Base schema for REST Resources
ResourceFunction | A ResourceFunction is a behavior to transform inputs of any nature into outputs of any nature independently from the way it is provided.
ResourceFunctionSpecification | Specifies a function as a behavior to transform inputs of any nature into outputs of any nature independently from the way it is provided, for example a Medium to Large Enterprise Firewall.
ResourceGraph | Resource graph
ResourceGraphRelationship | Describes links between resource graphs.
ResourceGraphSpecification | Resource graph specification.
ResourceGraphSpecificationRelationship | Describes link between resource graph specifications.
ResourceOrder | A Resource Order is a request to provision a set of Resources (logical and physical) triggered by the request to provision a Service through a Service Order
ResourceOrderItem | An identified part of the order.
ResourceOrderItemRelationship | 
ResourceOrderRelationship | 
ResourceRelationship | Linked resources to the one instantiate, such as [bundled] if the resource is a bundle and you want to describe the bundled resources inside this bundle; [reliesOn] if the resource needs another alrea
ResourceReservation | 
ResourceReservationItem | 
ResourceSpecification | Resources are physical or non-physical components (or some combination of these) within an enterprise's infrastructure or inventory.
ResourceSpecificationCharacteristic | This class defines the characteristic features of a resource specification.
ResourceSpecificationCharacteristicRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among ResourceSpecificationCharacteristics.
ResourceSpecificationRelationship | A migration, substitution, dependency or exclusivity relationship between/among resource specifications.
Scale | Task Resource used to request scaling of a Resource Function
SupportingResource | 
UnAckAlarms | Task resource for unacknowledge alarms operation
UnGroupAlarms | Task resource for ungroup alarms operation

## Service

> Service catalog, specifications, orders, problems, tests, and qualification.

**57 entities** (excluding Ref wrappers and state types)

Entity | Description
--- | ---
AlternateServiceProposal | Alternate service proposal is used when the requested service is not available with characteristic and date asked for.
AppliedConsequence | An Applied Consequence defines the action (prescribed action or notification) to take when a MeasureThresholdRuleViolation occurs.
BaseService | In the context of a service order and depending on the action requested (add/modify/delete/noChange) this data structure captures the configuration to apply to an existing subscribed service or to a n
CancelServiceOrder | Request for cancellation an existing Service order
CheckServiceQualification | CheckServiceQualification is used to perform a technical eligibility on service configuration(s).
CheckServiceQualificationItem | A ServiceQualificationItem relates to a specific service being checked in a qualification operation.
FirstAlert | Indicates what first alerted the system to the problem.
ImpactPattern | Define the patterns of impact (optional), such as other service characteristics- Used when defining impact through another pattern than the pre-defined attributes
MeasureThresholdRuleViolation | A measureThresholdRuleViolation is a violation of a rule that defines the in the MericDefMeasureThresholdRule.
MetricDefMeasureConsequence | A MetricDefMeasureConsequence defines the action (prescribed action or notification) to take when a MetricDefMeasureThresholdRule is crossed.
MetricDefMeasureThresholdRule | A MetricDefMeasureThresholdRule is a rule that defines the condition (raise or clear) to achieve to apply consequences when a threshold is crossed or ceased to be crossed.
ProblemAcknowledgement | Task resource that requests acknowledgement of problems by the problem handler.
ProblemGroup | Task resource that requests Service Problems to be grouped together into a parent and set of children
ProblemUnacknowledgement | Task resource that requests unacknowledgement of problems, rolling back the status of the problems from Acknowledged to Submitted.
ProblemUngroup | Task resource that requests Service Problems to be ungrouped from a parent
QueryServiceQualification | QueryServiceQualification is used to retrieve a list of services that are technically available in the context of the interaction (place, party, service characteristics, ...).
RelatedServiceOrderItem | RelatedServiceOrderItem (a ServiceOrder item) .The service order item which triggered service creation/change/termination.
Service | Service is a base class for defining the Service hierarchy.
ServiceCandidate | ServiceCandidate is an entity that makes a service specification available to a catalog.
ServiceCatalog | The root entity for service catalog management.
ServiceCategory | The (service) category resource is used to group service candidates in logical containers.
ServiceCharacteristic | is a list of name value pairs that define the service characteristics
ServiceEligibilityUnavailabilityReason | Reason for eligibility result if the ServiceQualification result is no (meaning the Service is not available)
ServiceFeatureSpecification | Specification for service features
ServiceLevelObjective | Service level objectives are defined in terms of parameters and metrics, thresholds, and tolerances associated with the parameters.
ServiceLevelSpecConsequence | Some consequences for the provider of the Service are resulted when the service level objective does not meet.
ServiceLevelSpecParameter | Service Level Specification parameters can be one of two types.
ServiceLevelSpecification | A Service Level Specification represents a pre-defined or negotiated set of Service Level Objectives.
ServiceOrder | 
ServiceOrderErrorMessage | A ServiceOrderErrorMessage represents an error that causes a status change in a service order.
ServiceOrderItem | 
ServiceOrderItemRelationship | Linked service order item to the one containing this attribute
ServiceOrderJeopardyAlert | A ServiceOrderJeopardyAlert represents a predicted exception during a service order processing that would brings risk to complete successfully the ordetr.
ServiceOrderMilestone | ServiceOrderMilestone represents an action or event marking a significant change or stage in processing of a service order.
ServiceOrderRelationship | Linked service order to the one containing this attribute
ServiceProblem | The problem information for Middle B which is abstracted in the service layer from the issued event information by First B
ServiceProblemEventRecord | A record of an event (related to a service problem) received from another system
ServiceQualification | ServiceQualification is used to perform a technical eligibility.
ServiceQualificationItem | A ServiceQualificationItem relates to a specific service being checked in a qualification operation.
ServiceQualificationItemRelationship | Structure used to describe relationship between serviceQualification items from the same serviceQualification.
ServiceQualificationRelationship | 
ServiceRelationship | 
ServiceRelationshipType | Possible values for service relationship type
ServiceSpecCharRelationship | An aggregation, migration, substitution, dependency or exclusivity relationship between/among serviceSpecCharacteristics.
ServiceSpecCharacteristic | This class represents the key features of this service specification.
ServiceSpecCharacteristicValue | A ServiceSpecCharacteristicValue object is used to define a set of attributes, each of which can be assigned to a corresponding set of attributes in a ServiceSpecCharacteristic object.
ServiceSpecRelationship | A dependency, substitution or exclusivity relationship between/among service specifications.
ServiceSpecification | ServiceSpecification is a class that offers characteristics to describe a type of service.
ServiceTest | A service test is an entity that exists for a controlled test invocation on a service.
ServiceTestCharacteristic | The configuration of the service test is set by the service test characteristic.
ServiceTestSpecRelationship | A substitution, dependency or exclusivity relationship between/among service specifications.
ServiceTestSpecification | The service test specification describes the service test in terms of parameters to be configured and measures to be taken.
SupportingService | A collection of services that support this service (links between CFS -> RFS)
TerminationError | This indicates an error that caused a qualificationItem to be terminated.
TestMeasure | A TestMeasure specifies a measure of a specific aspect of a product, service, or resource test, such as lost packets or connectivity status
TestMeasureDefinition | A TestMeasureDefinition specifies a measure of a specific aspect of a product, service, or resource test, such as lost packets or connectivity status
TrackingRecord | Tracking records allow the tracking of modifications on the problem.
