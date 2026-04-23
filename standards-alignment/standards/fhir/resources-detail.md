# FHIR R4 Core Resources Detail

Auto-generated from `profiles-resources.json`. Do not edit manually.

Generated: 2026-03-07T01:05:15Z

This file captures a focused subset of high-value resource definitions
for healthcare modelling and standards alignment in MD-DDL.

## Patient

- Canonical: `http://hl7.org/fhir/StructureDefinition/Patient`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `active`

Demographics and other administrative information about an individual or animal receiving care or
other health-related services.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | An identifier for this patient
active | 0 | 1 | boolean | Whether this patient's record is in active use
name | 0 | * | HumanName | A name associated with the patient
telecom | 0 | * | ContactPoint | A contact detail for the individual
gender | 0 | 1 | code | male \| female \| other \| unknown
birthDate | 0 | 1 | date | The date of birth for the individual
deceased[x] | 0 | 1 | boolean, dateTime | Indicates if the individual is deceased or not
address | 0 | * | Address | An address for the individual
maritalStatus | 0 | 1 | CodeableConcept | Marital (civil) status of a patient
multipleBirth[x] | 0 | 1 | boolean, integer | Whether patient is part of a multiple birth
photo | 0 | * | Attachment | Image of the patient
contact | 0 | * | BackboneElement | A contact party (e.g. guardian, partner, friend) for the patient
communication | 0 | * | BackboneElement | A language which may be used to communicate with the patient about his or her health
generalPractitioner | 0 | * | Reference | Patient's nominated primary care provider
managingOrganization | 0 | 1 | Reference | Organization that is the custodian of the patient record
link | 0 | * | BackboneElement | Link to another patient resource that concerns the same actual person

## Encounter

- Canonical: `http://hl7.org/fhir/StructureDefinition/Encounter`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

An interaction between a patient and healthcare provider(s) for the purpose of providing healthcare
service(s) or assessing the health status of a patient.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Identifier(s) by which this encounter is known
status | 1 | 1 | code | planned \| arrived \| triaged \| in-progress \| onleave \| finished \| cancelled +
statusHistory | 0 | * | BackboneElement | List of past encounter statuses
class | 1 | 1 | Coding | Classification of patient encounter
classHistory | 0 | * | BackboneElement | List of past encounter classes
type | 0 | * | CodeableConcept | Specific type of encounter
serviceType | 0 | 1 | CodeableConcept | Specific type of service
priority | 0 | 1 | CodeableConcept | Indicates the urgency of the encounter
subject | 0 | 1 | Reference | The patient or group present at the encounter
episodeOfCare | 0 | * | Reference | Episode(s) of care that this encounter should be recorded against
basedOn | 0 | * | Reference | The ServiceRequest that initiated this encounter
participant | 0 | * | BackboneElement | List of participants involved in the encounter
appointment | 0 | * | Reference | The appointment that scheduled this encounter
period | 0 | 1 | Period | The start and end time of the encounter
length | 0 | 1 | Duration | Quantity of time the encounter lasted (less time absent)
reasonCode | 0 | * | CodeableConcept | Coded reason the encounter takes place
reasonReference | 0 | * | Reference | Reason the encounter takes place (reference)
diagnosis | 0 | * | BackboneElement | The list of diagnosis relevant to this encounter
account | 0 | * | Reference | The set of accounts that may be used for billing for this Encounter
hospitalization | 0 | 1 | BackboneElement | Details about the admission to a healthcare service
location | 0 | * | BackboneElement | List of locations where the patient has been
serviceProvider | 0 | 1 | Reference | The organization (facility) responsible for this encounter
partOf | 0 | 1 | Reference | Another Encounter this encounter is part of

## Condition

- Canonical: `http://hl7.org/fhir/StructureDefinition/Condition`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that
has risen to a level of concern.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External Ids for this condition
clinicalStatus | 0 | 1 | CodeableConcept | active \| recurrence \| relapse \| inactive \| remission \| resolved
verificationStatus | 0 | 1 | CodeableConcept | unconfirmed \| provisional \| differential \| confirmed \| refuted \| entered-in-error
category | 0 | * | CodeableConcept | problem-list-item \| encounter-diagnosis
severity | 0 | 1 | CodeableConcept | Subjective severity of condition
code | 0 | 1 | CodeableConcept | Identification of the condition, problem or diagnosis
bodySite | 0 | * | CodeableConcept | Anatomical location, if relevant
subject | 1 | 1 | Reference | Who has the condition?
encounter | 0 | 1 | Reference | Encounter created as part of
onset[x] | 0 | 1 | dateTime, Age, Period, Range, string | Estimated or actual date, date-time, or age
abatement[x] | 0 | 1 | dateTime, Age, Period, Range, string | When in resolution/remission
recordedDate | 0 | 1 | dateTime | Date record was first recorded
recorder | 0 | 1 | Reference | Who recorded the condition
asserter | 0 | 1 | Reference | Person who asserts this condition
stage | 0 | * | BackboneElement | Stage/grade, usually assessed formally
evidence | 0 | * | BackboneElement | Supporting evidence
note | 0 | * | Annotation | Additional information about the Condition

## Observation

- Canonical: `http://hl7.org/fhir/StructureDefinition/Observation`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `active`

Measurements and simple assertions made about a patient, device or other subject.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Business Identifier for observation
basedOn | 0 | * | Reference | Fulfills plan, proposal or order
partOf | 0 | * | Reference | Part of referenced event
status | 1 | 1 | code | registered \| preliminary \| final \| amended +
category | 0 | * | CodeableConcept | Classification of type of observation
code | 1 | 1 | CodeableConcept | Type of observation (code / type)
subject | 0 | 1 | Reference | Who and/or what the observation is about
focus | 0 | * | Reference | What the observation is about, when it is not about the subject of record
encounter | 0 | 1 | Reference | Healthcare event during which this observation is made
effective[x] | 0 | 1 | dateTime, Period, Timing, instant | Clinically relevant time/time-period for observation
issued | 0 | 1 | instant | Date/Time this version was made available
performer | 0 | * | Reference | Who is responsible for the observation
value[x] | 0 | 1 | Quantity, CodeableConcept, string, boolean, integer, Range, Ratio, SampledData, time, dateTime, Period | Actual result
dataAbsentReason | 0 | 1 | CodeableConcept | Why the result is missing
interpretation | 0 | * | CodeableConcept | High, low, normal, etc.
note | 0 | * | Annotation | Comments about the observation
bodySite | 0 | 1 | CodeableConcept | Observed body part
method | 0 | 1 | CodeableConcept | How it was done
specimen | 0 | 1 | Reference | Specimen used for this observation
device | 0 | 1 | Reference | (Measurement) Device
referenceRange | 0 | * | BackboneElement | Provides guide for interpretation
hasMember | 0 | * | Reference | Related resource that belongs to the Observation group
derivedFrom | 0 | * | Reference | Related measurements the observation is made from
component | 0 | * | BackboneElement | Component results

## Procedure

- Canonical: `http://hl7.org/fhir/StructureDefinition/Procedure`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

An action that is or was performed on or for a patient. This can be a physical intervention like an
operation, or less invasive like long term services, counseling, or hypnotherapy.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External Identifiers for this procedure
instantiatesCanonical | 0 | * | canonical | Instantiates FHIR protocol or definition
instantiatesUri | 0 | * | uri | Instantiates external protocol or definition
basedOn | 0 | * | Reference | A request for this procedure
partOf | 0 | * | Reference | Part of referenced event
status | 1 | 1 | code | preparation \| in-progress \| not-done \| on-hold \| stopped \| completed \| entered-in-error \| unknown
statusReason | 0 | 1 | CodeableConcept | Reason for current status
category | 0 | 1 | CodeableConcept | Classification of the procedure
code | 0 | 1 | CodeableConcept | Identification of the procedure
subject | 1 | 1 | Reference | Who the procedure was performed on
encounter | 0 | 1 | Reference | Encounter created as part of
performed[x] | 0 | 1 | dateTime, Period, string, Age, Range | When the procedure was performed
recorder | 0 | 1 | Reference | Who recorded the procedure
asserter | 0 | 1 | Reference | Person who asserts this procedure
performer | 0 | * | BackboneElement | The people who performed the procedure
location | 0 | 1 | Reference | Where the procedure happened
reasonCode | 0 | * | CodeableConcept | Coded reason procedure performed
reasonReference | 0 | * | Reference | The justification that the procedure was performed
bodySite | 0 | * | CodeableConcept | Target body sites
outcome | 0 | 1 | CodeableConcept | The result of procedure
report | 0 | * | Reference | Any report resulting from the procedure
complication | 0 | * | CodeableConcept | Complication following the procedure
complicationDetail | 0 | * | Reference | A condition that is a result of the procedure
followUp | 0 | * | CodeableConcept | Instructions for follow up

## Medication

- Canonical: `http://hl7.org/fhir/StructureDefinition/Medication`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

This resource is primarily used for the identification and definition of a medication for the
purposes of prescribing, dispensing, and administering a medication as well as for making statements
about medication use.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Business identifier for this medication
code | 0 | 1 | CodeableConcept | Codes that identify this medication
status | 0 | 1 | code | active \| inactive \| entered-in-error
manufacturer | 0 | 1 | Reference | Manufacturer of the item
form | 0 | 1 | CodeableConcept | powder \| tablets \| capsule +
amount | 0 | 1 | Ratio | Amount of drug in package
ingredient | 0 | * | BackboneElement | Active or inactive ingredient
batch | 0 | 1 | BackboneElement | Details about packaged medications

## MedicationRequest

- Canonical: `http://hl7.org/fhir/StructureDefinition/MedicationRequest`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

An order or request for both supply of the medication and the instructions for administration of the
medication to a patient. The resource is called "MedicationRequest" rather than
"MedicationPrescription" or "MedicationOrder" to generalize the use across inpatient and outpatient
settings, including care plans, etc., and to harmonize with workflow patterns.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External ids for this request
status | 1 | 1 | code | active \| on-hold \| cancelled \| completed \| entered-in-error \| stopped \| draft \| unknown
statusReason | 0 | 1 | CodeableConcept | Reason for current status
intent | 1 | 1 | code | proposal \| plan \| order \| original-order \| reflex-order \| filler-order \| instance-order \| option
category | 0 | * | CodeableConcept | Type of medication usage
priority | 0 | 1 | code | routine \| urgent \| asap \| stat
doNotPerform | 0 | 1 | boolean | True if request is prohibiting action
reported[x] | 0 | 1 | boolean, Reference | Reported rather than primary record
medication[x] | 1 | 1 | CodeableConcept, Reference | Medication to be taken
subject | 1 | 1 | Reference | Who or group medication request is for
encounter | 0 | 1 | Reference | Encounter created as part of encounter/admission/stay
supportingInformation | 0 | * | Reference | Information to support ordering of the medication
authoredOn | 0 | 1 | dateTime | When request was initially authored
requester | 0 | 1 | Reference | Who/What requested the Request
performer | 0 | 1 | Reference | Intended performer of administration
performerType | 0 | 1 | CodeableConcept | Desired kind of performer of the medication administration
recorder | 0 | 1 | Reference | Person who entered the request
reasonCode | 0 | * | CodeableConcept | Reason or indication for ordering or not ordering the medication
reasonReference | 0 | * | Reference | Condition or observation that supports why the prescription is being written
instantiatesCanonical | 0 | * | canonical | Instantiates FHIR protocol or definition
instantiatesUri | 0 | * | uri | Instantiates external protocol or definition
basedOn | 0 | * | Reference | What request fulfills
groupIdentifier | 0 | 1 | Identifier | Composite request this is part of
courseOfTherapyType | 0 | 1 | CodeableConcept | Overall pattern of medication administration

## MedicationAdministration

- Canonical: `http://hl7.org/fhir/StructureDefinition/MedicationAdministration`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Describes the event of a patient consuming or otherwise being administered a medication. This may be
as simple as swallowing a tablet or it may be a long running infusion. Related resources tie this
event to the authorizing prescription, and the specific encounter between patient and health care
practitioner.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External identifier
instantiates | 0 | * | uri | Instantiates protocol or definition
partOf | 0 | * | Reference | Part of referenced event
status | 1 | 1 | code | in-progress \| not-done \| on-hold \| completed \| entered-in-error \| stopped \| unknown
statusReason | 0 | * | CodeableConcept | Reason administration not performed
category | 0 | 1 | CodeableConcept | Type of medication usage
medication[x] | 1 | 1 | CodeableConcept, Reference | What was administered
subject | 1 | 1 | Reference | Who received medication
context | 0 | 1 | Reference | Encounter or Episode of Care administered as part of
supportingInformation | 0 | * | Reference | Additional information to support administration
effective[x] | 1 | 1 | dateTime, Period | Start and end time of administration
performer | 0 | * | BackboneElement | Who performed the medication administration and what they did
reasonCode | 0 | * | CodeableConcept | Reason administration performed
reasonReference | 0 | * | Reference | Condition or observation that supports why the medication was administered
request | 0 | 1 | Reference | Request administration performed against
device | 0 | * | Reference | Device used to administer
note | 0 | * | Annotation | Information about the administration
dosage | 0 | 1 | BackboneElement | Details of how medication was taken
eventHistory | 0 | * | Reference | A list of events of interest in the lifecycle

## AllergyIntolerance

- Canonical: `http://hl7.org/fhir/StructureDefinition/AllergyIntolerance`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Risk of harmful or undesirable, physiological response which is unique to an individual and
associated with exposure to a substance.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External ids for this item
clinicalStatus | 0 | 1 | CodeableConcept | active \| inactive \| resolved
verificationStatus | 0 | 1 | CodeableConcept | unconfirmed \| confirmed \| refuted \| entered-in-error
type | 0 | 1 | code | allergy \| intolerance - Underlying mechanism (if known)
category | 0 | * | code | food \| medication \| environment \| biologic
criticality | 0 | 1 | code | low \| high \| unable-to-assess
code | 0 | 1 | CodeableConcept | Code that identifies the allergy or intolerance
patient | 1 | 1 | Reference | Who the sensitivity is for
encounter | 0 | 1 | Reference | Encounter when the allergy or intolerance was asserted
onset[x] | 0 | 1 | dateTime, Age, Period, Range, string | When allergy or intolerance was identified
recordedDate | 0 | 1 | dateTime | Date first version of the resource instance was recorded
recorder | 0 | 1 | Reference | Who recorded the sensitivity
asserter | 0 | 1 | Reference | Source of the information about the allergy
lastOccurrence | 0 | 1 | dateTime | Date(/time) of last known occurrence of a reaction
note | 0 | * | Annotation | Additional text not captured in other fields
reaction | 0 | * | BackboneElement | Adverse Reaction Events linked to exposure to substance

## CarePlan

- Canonical: `http://hl7.org/fhir/StructureDefinition/CarePlan`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Describes the intention of how one or more practitioners intend to deliver care for a particular
patient, group or community for a period of time, possibly limited to care for a specific condition
or set of conditions.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External Ids for this plan
instantiatesCanonical | 0 | * | canonical | Instantiates FHIR protocol or definition
instantiatesUri | 0 | * | uri | Instantiates external protocol or definition
basedOn | 0 | * | Reference | Fulfills CarePlan
replaces | 0 | * | Reference | CarePlan replaced by this CarePlan
partOf | 0 | * | Reference | Part of referenced CarePlan
status | 1 | 1 | code | draft \| active \| on-hold \| revoked \| completed \| entered-in-error \| unknown
intent | 1 | 1 | code | proposal \| plan \| order \| option
category | 0 | * | CodeableConcept | Type of plan
title | 0 | 1 | string | Human-friendly name for the care plan
description | 0 | 1 | string | Summary of nature of plan
subject | 1 | 1 | Reference | Who the care plan is for
encounter | 0 | 1 | Reference | Encounter created as part of
period | 0 | 1 | Period | Time period plan covers
created | 0 | 1 | dateTime | Date record was first recorded
author | 0 | 1 | Reference | Who is the designated responsible party
contributor | 0 | * | Reference | Who provided the content of the care plan
careTeam | 0 | * | Reference | Who's involved in plan?
addresses | 0 | * | Reference | Health issues this plan addresses
supportingInfo | 0 | * | Reference | Information considered as part of plan
goal | 0 | * | Reference | Desired outcome of plan
activity | 0 | * | BackboneElement | Action to occur as part of plan
note | 0 | * | Annotation | Comments about the plan

## CareTeam

- Canonical: `http://hl7.org/fhir/StructureDefinition/CareTeam`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

The Care Team includes all the people and organizations who plan to participate in the coordination
and delivery of care for a patient.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External Ids for this team
status | 0 | 1 | code | proposed \| active \| suspended \| inactive \| entered-in-error
category | 0 | * | CodeableConcept | Type of team
name | 0 | 1 | string | Name of the team, such as crisis assessment team
subject | 0 | 1 | Reference | Who care team is for
encounter | 0 | 1 | Reference | Encounter created as part of
period | 0 | 1 | Period | Time period team covers
participant | 0 | * | BackboneElement | Members of the team
reasonCode | 0 | * | CodeableConcept | Why the care team exists
reasonReference | 0 | * | Reference | Why the care team exists
managingOrganization | 0 | * | Reference | Organization responsible for the care team
telecom | 0 | * | ContactPoint | A contact detail for the care team (that applies to all members)
note | 0 | * | Annotation | Comments made about the CareTeam

## Goal

- Canonical: `http://hl7.org/fhir/StructureDefinition/Goal`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Describes the intended objective(s) for a patient, group or organization care, for example, weight
loss, restoring an activity of daily living, obtaining herd immunity via immunization, meeting a
process improvement objective, etc.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External Ids for this goal
lifecycleStatus | 1 | 1 | code | proposed \| planned \| accepted \| active \| on-hold \| completed \| cancelled \| entered-in-error \| rejected
achievementStatus | 0 | 1 | CodeableConcept | in-progress \| improving \| worsening \| no-change \| achieved \| sustaining \| not-achieved \| no-progress \| not-attainable
category | 0 | * | CodeableConcept | E.g. Treatment, dietary, behavioral, etc.
priority | 0 | 1 | CodeableConcept | high-priority \| medium-priority \| low-priority
description | 1 | 1 | CodeableConcept | Code or text describing goal
subject | 1 | 1 | Reference | Who this goal is intended for
start[x] | 0 | 1 | date, CodeableConcept | When goal pursuit begins
target | 0 | * | BackboneElement | Target outcome for the goal
statusDate | 0 | 1 | date | When goal status took effect
statusReason | 0 | 1 | string | Reason for current status
expressedBy | 0 | 1 | Reference | Who's responsible for creating Goal?
addresses | 0 | * | Reference | Issues addressed by this goal
note | 0 | * | Annotation | Comments about the goal
outcomeCode | 0 | * | CodeableConcept | What result was achieved regarding the goal?
outcomeReference | 0 | * | Reference | Observation that resulted from goal

## Organization

- Canonical: `http://hl7.org/fhir/StructureDefinition/Organization`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A formally or informally recognized grouping of people or organizations formed for the purpose of
achieving some form of collective action. Includes companies, institutions, corporations,
departments, community groups, healthcare practice groups, payer/insurer, etc.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Identifies this organization across multiple systems
active | 0 | 1 | boolean | Whether the organization's record is still in active use
type | 0 | * | CodeableConcept | Kind of organization
name | 0 | 1 | string | Name used for the organization
alias | 0 | * | string | A list of alternate names that the organization is known as, or was known as in the past
telecom | 0 | * | ContactPoint | A contact detail for the organization
address | 0 | * | Address | An address for the organization
partOf | 0 | 1 | Reference | The organization of which this organization forms a part
contact | 0 | * | BackboneElement | Contact for the organization for a certain purpose
endpoint | 0 | * | Reference | Technical endpoints providing access to services operated for the organization

## Practitioner

- Canonical: `http://hl7.org/fhir/StructureDefinition/Practitioner`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A person who is directly or indirectly involved in the provisioning of healthcare.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | An identifier for the person as this agent
active | 0 | 1 | boolean | Whether this practitioner's record is in active use
name | 0 | * | HumanName | The name(s) associated with the practitioner
telecom | 0 | * | ContactPoint | A contact detail for the practitioner (that apply to all roles)
address | 0 | * | Address | Address(es) of the practitioner that are not role specific (typically home address)
gender | 0 | 1 | code | male \| female \| other \| unknown
birthDate | 0 | 1 | date | The date on which the practitioner was born
photo | 0 | * | Attachment | Image of the person
qualification | 0 | * | BackboneElement | Certification, licenses, or training pertaining to the provision of care
communication | 0 | * | CodeableConcept | A language the practitioner can use in patient communication

## PractitionerRole

- Canonical: `http://hl7.org/fhir/StructureDefinition/PractitionerRole`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A specific set of Roles/Locations/specialties/services that a practitioner may perform at an
organization for a period of time.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Business Identifiers that are specific to a role/location
active | 0 | 1 | boolean | Whether this practitioner role record is in active use
period | 0 | 1 | Period | The period during which the practitioner is authorized to perform in these role(s)
practitioner | 0 | 1 | Reference | Practitioner that is able to provide the defined services for the organization
organization | 0 | 1 | Reference | Organization where the roles are available
code | 0 | * | CodeableConcept | Roles which this practitioner may perform
specialty | 0 | * | CodeableConcept | Specific specialty of the practitioner
location | 0 | * | Reference | The location(s) at which this practitioner provides care
healthcareService | 0 | * | Reference | The list of healthcare services that this worker provides for this role's Organization/Location(s)
telecom | 0 | * | ContactPoint | Contact details that are specific to the role/location/service
availableTime | 0 | * | BackboneElement | Times the Service Site is available
notAvailable | 0 | * | BackboneElement | Not available during this time due to provided reason
availabilityExceptions | 0 | 1 | string | Description of availability exceptions
endpoint | 0 | * | Reference | Technical endpoints providing access to services operated for the practitioner with this role

## RelatedPerson

- Canonical: `http://hl7.org/fhir/StructureDefinition/RelatedPerson`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Information about a person that is involved in the care for a patient, but who is not the target of
healthcare, nor has a formal responsibility in the care process.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | A human identifier for this person
active | 0 | 1 | boolean | Whether this related person's record is in active use
patient | 1 | 1 | Reference | The patient this person is related to
relationship | 0 | * | CodeableConcept | The nature of the relationship
name | 0 | * | HumanName | A name associated with the person
telecom | 0 | * | ContactPoint | A contact detail for the person
gender | 0 | 1 | code | male \| female \| other \| unknown
birthDate | 0 | 1 | date | The date on which the related person was born
address | 0 | * | Address | Address where the related person can be contacted or visited
photo | 0 | * | Attachment | Image of the person
period | 0 | 1 | Period | Period of time that this relationship is considered valid
communication | 0 | * | BackboneElement | A language which may be used to communicate with about the patient's health

## Location

- Canonical: `http://hl7.org/fhir/StructureDefinition/Location`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Details and position information for a physical place where services are provided and resources and
participants may be stored, found, contained, or accommodated.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Unique code or number identifying the location to its users
status | 0 | 1 | code | active \| suspended \| inactive
operationalStatus | 0 | 1 | Coding | The operational status of the location (typically only for a bed/room)
name | 0 | 1 | string | Name of the location as used by humans
alias | 0 | * | string | A list of alternate names that the location is known as, or was known as, in the past
description | 0 | 1 | string | Additional details about the location that could be displayed as further information to identify the location beyond ...
mode | 0 | 1 | code | instance \| kind
type | 0 | * | CodeableConcept | Type of function performed
telecom | 0 | * | ContactPoint | Contact details of the location
address | 0 | 1 | Address | Physical location
physicalType | 0 | 1 | CodeableConcept | Physical form of the location
position | 0 | 1 | BackboneElement | The absolute geographic location
managingOrganization | 0 | 1 | Reference | Organization responsible for provisioning and upkeep
partOf | 0 | 1 | Reference | Another Location this one is physically a part of
hoursOfOperation | 0 | * | BackboneElement | What days/times during a week is this location usually open
availabilityExceptions | 0 | 1 | string | Description of availability exceptions
endpoint | 0 | * | Reference | Technical endpoints providing access to services operated for the location

## HealthcareService

- Canonical: `http://hl7.org/fhir/StructureDefinition/HealthcareService`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

The details of a healthcare service available at a location.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External identifiers for this item
active | 0 | 1 | boolean | Whether this HealthcareService record is in active use
providedBy | 0 | 1 | Reference | Organization that provides this service
category | 0 | * | CodeableConcept | Broad category of service being performed or delivered
type | 0 | * | CodeableConcept | Type of service that may be delivered or performed
specialty | 0 | * | CodeableConcept | Specialties handled by the HealthcareService
location | 0 | * | Reference | Location(s) where service may be provided
name | 0 | 1 | string | Description of service as presented to a consumer while searching
comment | 0 | 1 | string | Additional description and/or any specific issues not covered elsewhere
extraDetails | 0 | 1 | markdown | Extra details about the service that can't be placed in the other fields
photo | 0 | 1 | Attachment | Facilitates quick identification of the service
telecom | 0 | * | ContactPoint | Contacts related to the healthcare service
coverageArea | 0 | * | Reference | Location(s) service is intended for/available to
serviceProvisionCode | 0 | * | CodeableConcept | Conditions under which service is available/offered
eligibility | 0 | * | BackboneElement | Specific eligibility requirements required to use the service
program | 0 | * | CodeableConcept | Programs that this service is applicable to
characteristic | 0 | * | CodeableConcept | Collection of characteristics (attributes)
communication | 0 | * | CodeableConcept | The language that this service is offered in
referralMethod | 0 | * | CodeableConcept | Ways that the service accepts referrals
appointmentRequired | 0 | 1 | boolean | If an appointment is required for access to this service
availableTime | 0 | * | BackboneElement | Times the Service Site is available
notAvailable | 0 | * | BackboneElement | Not available during this time due to provided reason
availabilityExceptions | 0 | 1 | string | Description of availability exceptions
endpoint | 0 | * | Reference | Technical endpoints providing access to electronic services operated for the healthcare service

## Coverage

- Canonical: `http://hl7.org/fhir/StructureDefinition/Coverage`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Financial instrument which may be used to reimburse or pay for health care products and services.
Includes both insurance and self-payment.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Business Identifier for the coverage
status | 1 | 1 | code | active \| cancelled \| draft \| entered-in-error
type | 0 | 1 | CodeableConcept | Coverage category such as medical or accident
policyHolder | 0 | 1 | Reference | Owner of the policy
subscriber | 0 | 1 | Reference | Subscriber to the policy
subscriberId | 0 | 1 | string | ID assigned to the subscriber
beneficiary | 1 | 1 | Reference | Plan beneficiary
dependent | 0 | 1 | string | Dependent number
relationship | 0 | 1 | CodeableConcept | Beneficiary relationship to the subscriber
period | 0 | 1 | Period | Coverage start and end dates
payor | 1 | * | Reference | Issuer of the policy
class | 0 | * | BackboneElement | Additional coverage classifications
order | 0 | 1 | positiveInt | Relative order of the coverage
network | 0 | 1 | string | Insurer network
costToBeneficiary | 0 | * | BackboneElement | Patient payments for services/products
subrogation | 0 | 1 | boolean | Reimbursement to insurer
contract | 0 | * | Reference | Contract details

## Claim

- Canonical: `http://hl7.org/fhir/StructureDefinition/Claim`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A provider issued list of professional services and products which have been provided, or are to be
provided, to a patient which is sent to an insurer for reimbursement.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Business Identifier for claim
status | 1 | 1 | code | active \| cancelled \| draft \| entered-in-error
type | 1 | 1 | CodeableConcept | Category or discipline
subType | 0 | 1 | CodeableConcept | More granular claim type
use | 1 | 1 | code | claim \| preauthorization \| predetermination
patient | 1 | 1 | Reference | The recipient of the products and services
billablePeriod | 0 | 1 | Period | Relevant time frame for the claim
created | 1 | 1 | dateTime | Resource creation date
enterer | 0 | 1 | Reference | Author of the claim
insurer | 0 | 1 | Reference | Target
provider | 1 | 1 | Reference | Party responsible for the claim
priority | 1 | 1 | CodeableConcept | Desired processing ugency
fundsReserve | 0 | 1 | CodeableConcept | For whom to reserve funds
related | 0 | * | BackboneElement | Prior or corollary claims
prescription | 0 | 1 | Reference | Prescription authorizing services and products
originalPrescription | 0 | 1 | Reference | Original prescription if superseded by fulfiller
payee | 0 | 1 | BackboneElement | Recipient of benefits payable
referral | 0 | 1 | Reference | Treatment referral
facility | 0 | 1 | Reference | Servicing facility
careTeam | 0 | * | BackboneElement | Members of the care team
supportingInfo | 0 | * | BackboneElement | Supporting information
diagnosis | 0 | * | BackboneElement | Pertinent diagnosis information
procedure | 0 | * | BackboneElement | Clinical procedures performed
insurance | 1 | * | BackboneElement | Patient insurance information

## ClaimResponse

- Canonical: `http://hl7.org/fhir/StructureDefinition/ClaimResponse`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

This resource provides the adjudication details from the processing of a Claim resource.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Business Identifier for a claim response
status | 1 | 1 | code | active \| cancelled \| draft \| entered-in-error
type | 1 | 1 | CodeableConcept | More granular claim type
subType | 0 | 1 | CodeableConcept | More granular claim type
use | 1 | 1 | code | claim \| preauthorization \| predetermination
patient | 1 | 1 | Reference | The recipient of the products and services
created | 1 | 1 | dateTime | Response creation date
insurer | 1 | 1 | Reference | Party responsible for reimbursement
requestor | 0 | 1 | Reference | Party responsible for the claim
request | 0 | 1 | Reference | Id of resource triggering adjudication
outcome | 1 | 1 | code | queued \| complete \| error \| partial
disposition | 0 | 1 | string | Disposition Message
preAuthRef | 0 | 1 | string | Preauthorization reference
preAuthPeriod | 0 | 1 | Period | Preauthorization reference effective period
payeeType | 0 | 1 | CodeableConcept | Party to be paid any benefits payable
item | 0 | * | BackboneElement | Adjudication for claim line items
addItem | 0 | * | BackboneElement | Insurer added line items
adjudication | 0 | * |  | Header-level adjudication
total | 0 | * | BackboneElement | Adjudication totals
payment | 0 | 1 | BackboneElement | Payment Details
fundsReserve | 0 | 1 | CodeableConcept | Funds reserved status
formCode | 0 | 1 | CodeableConcept | Printed form identifier
form | 0 | 1 | Attachment | Printed reference or actual form
processNote | 0 | * | BackboneElement | Note concerning adjudication

## ExplanationOfBenefit

- Canonical: `http://hl7.org/fhir/StructureDefinition/ExplanationOfBenefit`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

This resource provides: the claim details; adjudication details from the processing of a Claim; and
optionally account balance information, for informing the subscriber of the benefits provided.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Business Identifier for the resource
status | 1 | 1 | code | active \| cancelled \| draft \| entered-in-error
type | 1 | 1 | CodeableConcept | Category or discipline
subType | 0 | 1 | CodeableConcept | More granular claim type
use | 1 | 1 | code | claim \| preauthorization \| predetermination
patient | 1 | 1 | Reference | The recipient of the products and services
billablePeriod | 0 | 1 | Period | Relevant time frame for the claim
created | 1 | 1 | dateTime | Response creation date
enterer | 0 | 1 | Reference | Author of the claim
insurer | 1 | 1 | Reference | Party responsible for reimbursement
provider | 1 | 1 | Reference | Party responsible for the claim
priority | 0 | 1 | CodeableConcept | Desired processing urgency
fundsReserveRequested | 0 | 1 | CodeableConcept | For whom to reserve funds
fundsReserve | 0 | 1 | CodeableConcept | Funds reserved status
related | 0 | * | BackboneElement | Prior or corollary claims
prescription | 0 | 1 | Reference | Prescription authorizing services or products
originalPrescription | 0 | 1 | Reference | Original prescription if superceded by fulfiller
payee | 0 | 1 | BackboneElement | Recipient of benefits payable
referral | 0 | 1 | Reference | Treatment Referral
facility | 0 | 1 | Reference | Servicing Facility
claim | 0 | 1 | Reference | Claim reference
claimResponse | 0 | 1 | Reference | Claim response reference
outcome | 1 | 1 | code | queued \| complete \| error \| partial
disposition | 0 | 1 | string | Disposition Message

## Account

- Canonical: `http://hl7.org/fhir/StructureDefinition/Account`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A financial tool for tracking value accrued for a particular purpose. In the healthcare field, used
to track charges for a patient, cost centers, etc.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Account number
status | 1 | 1 | code | active \| inactive \| entered-in-error \| on-hold \| unknown
type | 0 | 1 | CodeableConcept | E.g. patient, expense, depreciation
name | 0 | 1 | string | Human-readable label
subject | 0 | * | Reference | The entity that caused the expenses
servicePeriod | 0 | 1 | Period | Transaction window
coverage | 0 | * | BackboneElement | The party(s) that are responsible for covering the payment of this account, and what order should they be applied to ...
owner | 0 | 1 | Reference | Entity managing the Account
description | 0 | 1 | string | Explanation of purpose/use
guarantor | 0 | * | BackboneElement | The parties ultimately responsible for balancing the Account
partOf | 0 | 1 | Reference | Reference to a parent Account

## DiagnosticReport

- Canonical: `http://hl7.org/fhir/StructureDefinition/DiagnosticReport`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

The findings and interpretation of diagnostic tests performed on patients, groups of patients,
devices, and locations, and/or specimens derived from these. The report includes clinical context
such as requesting and provider information, and some mix of atomic results, images, textual and
coded interpretations, and formatted representation of diagnostic reports.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Business identifier for report
basedOn | 0 | * | Reference | What was requested
status | 1 | 1 | code | registered \| partial \| preliminary \| final +
category | 0 | * | CodeableConcept | Service category
code | 1 | 1 | CodeableConcept | Name/Code for this diagnostic report
subject | 0 | 1 | Reference | The subject of the report - usually, but not always, the patient
encounter | 0 | 1 | Reference | Health care event when test ordered
effective[x] | 0 | 1 | dateTime, Period | Clinically relevant time/time-period for report
issued | 0 | 1 | instant | DateTime this version was made
performer | 0 | * | Reference | Responsible Diagnostic Service
resultsInterpreter | 0 | * | Reference | Primary result interpreter
specimen | 0 | * | Reference | Specimens this report is based on
result | 0 | * | Reference | Observations
imagingStudy | 0 | * | Reference | Reference to full details of imaging associated with the diagnostic report
media | 0 | * | BackboneElement | Key images associated with this report
conclusion | 0 | 1 | string | Clinical conclusion (interpretation) of test results
conclusionCode | 0 | * | CodeableConcept | Codes for the clinical conclusion of test results
presentedForm | 0 | * | Attachment | Entire report as issued

## Specimen

- Canonical: `http://hl7.org/fhir/StructureDefinition/Specimen`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A sample to be used for analysis.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External Identifier
accessionIdentifier | 0 | 1 | Identifier | Identifier assigned by the lab
status | 0 | 1 | code | available \| unavailable \| unsatisfactory \| entered-in-error
type | 0 | 1 | CodeableConcept | Kind of material that forms the specimen
subject | 0 | 1 | Reference | Where the specimen came from. This may be from patient(s), from a location (e.g., the source of an environmental samp...
receivedTime | 0 | 1 | dateTime | The time when specimen was received for processing
parent | 0 | * | Reference | Specimen from which this specimen originated
request | 0 | * | Reference | Why the specimen was collected
collection | 0 | 1 | BackboneElement | Collection details
processing | 0 | * | BackboneElement | Processing and processing step details
container | 0 | * | BackboneElement | Direct container of specimen (tube/slide, etc.)
condition | 0 | * | CodeableConcept | State of the specimen
note | 0 | * | Annotation | Comments

## ImagingStudy

- Canonical: `http://hl7.org/fhir/StructureDefinition/ImagingStudy`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Representation of the content produced in a DICOM imaging study. A study comprises a set of series,
each of which includes a set of Service-Object Pair Instances (SOP Instances - images or other data)
acquired or produced in a common context. A series is of only one modality (e.g. X-ray, CT, MR,
ultrasound), but a study may have multiple series of different modalities.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Identifiers for the whole study
status | 1 | 1 | code | registered \| available \| cancelled \| entered-in-error \| unknown
modality | 0 | * | Coding | All series modality if actual acquisition modalities
subject | 1 | 1 | Reference | Who or what is the subject of the study
encounter | 0 | 1 | Reference | Encounter with which this imaging study is associated
started | 0 | 1 | dateTime | When the study was started
basedOn | 0 | * | Reference | Request fulfilled
referrer | 0 | 1 | Reference | Referring physician
interpreter | 0 | * | Reference | Who interpreted images
endpoint | 0 | * | Reference | Study access endpoint
numberOfSeries | 0 | 1 | unsignedInt | Number of Study Related Series
numberOfInstances | 0 | 1 | unsignedInt | Number of Study Related Instances
procedureReference | 0 | 1 | Reference | The performed Procedure reference
procedureCode | 0 | * | CodeableConcept | The performed procedure code
location | 0 | 1 | Reference | Where ImagingStudy occurred
reasonCode | 0 | * | CodeableConcept | Why the study was requested
reasonReference | 0 | * | Reference | Why was study performed
note | 0 | * | Annotation | User-defined comments
description | 0 | 1 | string | Institution-generated description
series | 0 | * | BackboneElement | Each study has one or more series of instances

## ServiceRequest

- Canonical: `http://hl7.org/fhir/StructureDefinition/ServiceRequest`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A record of a request for service such as diagnostic investigations, treatments, or operations to be
performed.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Identifiers assigned to this order
instantiatesCanonical | 0 | * | canonical | Instantiates FHIR protocol or definition
instantiatesUri | 0 | * | uri | Instantiates external protocol or definition
basedOn | 0 | * | Reference | What request fulfills
replaces | 0 | * | Reference | What request replaces
requisition | 0 | 1 | Identifier | Composite Request ID
status | 1 | 1 | code | draft \| active \| on-hold \| revoked \| completed \| entered-in-error \| unknown
intent | 1 | 1 | code | proposal \| plan \| directive \| order \| original-order \| reflex-order \| filler-order \| instance-order \| option
category | 0 | * | CodeableConcept | Classification of service
priority | 0 | 1 | code | routine \| urgent \| asap \| stat
doNotPerform | 0 | 1 | boolean | True if service/procedure should not be performed
code | 0 | 1 | CodeableConcept | What is being requested/ordered
orderDetail | 0 | * | CodeableConcept | Additional order information
quantity[x] | 0 | 1 | Quantity, Ratio, Range | Service amount
subject | 1 | 1 | Reference | Individual or Entity the service is ordered for
encounter | 0 | 1 | Reference | Encounter in which the request was created
occurrence[x] | 0 | 1 | dateTime, Period, Timing | When service should occur
asNeeded[x] | 0 | 1 | boolean, CodeableConcept | Preconditions for service
authoredOn | 0 | 1 | dateTime | Date request signed
requester | 0 | 1 | Reference | Who/what is requesting service
performerType | 0 | 1 | CodeableConcept | Performer role
performer | 0 | * | Reference | Requested performer
locationCode | 0 | * | CodeableConcept | Requested location
locationReference | 0 | * | Reference | Requested location

## Appointment

- Canonical: `http://hl7.org/fhir/StructureDefinition/Appointment`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or
device(s) for a specific date/time. This may result in one or more Encounter(s).

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | External Ids for this item
status | 1 | 1 | code | proposed \| pending \| booked \| arrived \| fulfilled \| cancelled \| noshow \| entered-in-error \| checked-in \| waitlist
cancelationReason | 0 | 1 | CodeableConcept | The coded reason for the appointment being cancelled
serviceCategory | 0 | * | CodeableConcept | A broad categorization of the service that is to be performed during this appointment
serviceType | 0 | * | CodeableConcept | The specific service that is to be performed during this appointment
specialty | 0 | * | CodeableConcept | The specialty of a practitioner that would be required to perform the service requested in this appointment
appointmentType | 0 | 1 | CodeableConcept | The style of appointment or patient that has been booked in the slot (not service type)
reasonCode | 0 | * | CodeableConcept | Coded reason this appointment is scheduled
reasonReference | 0 | * | Reference | Reason the appointment is to take place (resource)
priority | 0 | 1 | unsignedInt | Used to make informed decisions if needing to re-prioritize
description | 0 | 1 | string | Shown on a subject line in a meeting request, or appointment list
supportingInformation | 0 | * | Reference | Additional information to support the appointment
start | 0 | 1 | instant | When appointment is to take place
end | 0 | 1 | instant | When appointment is to conclude
minutesDuration | 0 | 1 | positiveInt | Can be less than start/end (e.g. estimate)
slot | 0 | * | Reference | The slots that this appointment is filling
created | 0 | 1 | dateTime | The date that this appointment was initially created
comment | 0 | 1 | string | Additional comments
patientInstruction | 0 | 1 | string | Detailed information and instructions for the patient
basedOn | 0 | * | Reference | The service request this appointment is allocated to assess
participant | 1 | * | BackboneElement | Participants involved in appointment
requestedPeriod | 0 | * | Period | Potential date/time interval(s) requested to allocate the appointment within

## Task

- Canonical: `http://hl7.org/fhir/StructureDefinition/Task`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A task to be performed.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Task Instance Identifier
instantiatesCanonical | 0 | 1 | canonical | Formal definition of task
instantiatesUri | 0 | 1 | uri | Formal definition of task
basedOn | 0 | * | Reference | Request fulfilled by this task
groupIdentifier | 0 | 1 | Identifier | Requisition or grouper id
partOf | 0 | * | Reference | Composite task
status | 1 | 1 | code | draft \| requested \| received \| accepted \| +
statusReason | 0 | 1 | CodeableConcept | Reason for current status
businessStatus | 0 | 1 | CodeableConcept | E.g. "Specimen collected", "IV prepped"
intent | 1 | 1 | code | unknown \| proposal \| plan \| order \| original-order \| reflex-order \| filler-order \| instance-order \| option
priority | 0 | 1 | code | routine \| urgent \| asap \| stat
code | 0 | 1 | CodeableConcept | Task Type
description | 0 | 1 | string | Human-readable explanation of task
focus | 0 | 1 | Reference | What task is acting on
for | 0 | 1 | Reference | Beneficiary of the Task
encounter | 0 | 1 | Reference | Healthcare event during which this task originated
executionPeriod | 0 | 1 | Period | Start and end time of execution
authoredOn | 0 | 1 | dateTime | Task Creation Date
lastModified | 0 | 1 | dateTime | Task Last Modified Date
requester | 0 | 1 | Reference | Who is asking for task to be done
performerType | 0 | * | CodeableConcept | Requested performer
owner | 0 | 1 | Reference | Responsible individual
location | 0 | 1 | Reference | Where task occurs
reasonCode | 0 | 1 | CodeableConcept | Why task is needed

## Communication

- Canonical: `http://hl7.org/fhir/StructureDefinition/Communication`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

An occurrence of information being transmitted; e.g. an alert that was sent to a responsible
provider, a public health agency that was notified about a reportable condition.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Unique identifier
instantiatesCanonical | 0 | * | canonical | Instantiates FHIR protocol or definition
instantiatesUri | 0 | * | uri | Instantiates external protocol or definition
basedOn | 0 | * | Reference | Request fulfilled by this communication
partOf | 0 | * | Reference | Part of this action
inResponseTo | 0 | * | Reference | Reply to
status | 1 | 1 | code | preparation \| in-progress \| not-done \| on-hold \| stopped \| completed \| entered-in-error \| unknown
statusReason | 0 | 1 | CodeableConcept | Reason for current status
category | 0 | * | CodeableConcept | Message category
priority | 0 | 1 | code | routine \| urgent \| asap \| stat
medium | 0 | * | CodeableConcept | A channel of communication
subject | 0 | 1 | Reference | Focus of message
topic | 0 | 1 | CodeableConcept | Description of the purpose/content
about | 0 | * | Reference | Resources that pertain to this communication
encounter | 0 | 1 | Reference | Encounter created as part of
sent | 0 | 1 | dateTime | When sent
received | 0 | 1 | dateTime | When received
recipient | 0 | * | Reference | Message recipient
sender | 0 | 1 | Reference | Message sender
reasonCode | 0 | * | CodeableConcept | Indication for message
reasonReference | 0 | * | Reference | Why was communication done?
payload | 0 | * | BackboneElement | Message payload
note | 0 | * | Annotation | Comments made about the communication

## Consent

- Canonical: `http://hl7.org/fhir/StructureDefinition/Consent`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A record of a healthcare consumer’s choices, which permits or denies identified recipient(s) or
recipient role(s) to perform one or more actions within a given policy context, for specific
purposes and periods of time.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Identifier for this record (external references)
status | 1 | 1 | code | draft \| proposed \| active \| rejected \| inactive \| entered-in-error
scope | 1 | 1 | CodeableConcept | Which of the four areas this resource covers (extensible)
category | 1 | * | CodeableConcept | Classification of the consent statement - for indexing/retrieval
patient | 0 | 1 | Reference | Who the consent applies to
dateTime | 0 | 1 | dateTime | When this Consent was created or indexed
performer | 0 | * | Reference | Who is agreeing to the policy and rules
organization | 0 | * | Reference | Custodian of the consent
source[x] | 0 | 1 | Attachment, Reference | Source from which this consent is taken
policy | 0 | * | BackboneElement | Policies covered by this consent
policyRule | 0 | 1 | CodeableConcept | Regulation that this consents to
verification | 0 | * | BackboneElement | Consent Verified by patient or family
provision | 0 | 1 | BackboneElement | Constraints to the base Consent.policyRule

## Provenance

- Canonical: `http://hl7.org/fhir/StructureDefinition/Provenance`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Provenance of a resource is a record that describes entities and processes involved in producing and
delivering or otherwise influencing that resource. Provenance provides a critical foundation for
assessing authenticity, enabling trust, and allowing reproducibility. Provenance assertions are a
form of contextual metadata and can themselves become important records with their own provenance.
Provenance statement indicates clinical significance in terms of confidence in authenticity,
reliabili...

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
target | 1 | * | Reference | Target Reference(s) (usually version specific)
occurred[x] | 0 | 1 | Period, dateTime | When the activity occurred
recorded | 1 | 1 | instant | When the activity was recorded / updated
policy | 0 | * | uri | Policy or plan the activity was defined by
location | 0 | 1 | Reference | Where the activity occurred, if relevant
reason | 0 | * | CodeableConcept | Reason the activity is occurring
activity | 0 | 1 | CodeableConcept | Activity that occurred
agent | 1 | * | BackboneElement | Actor involved
entity | 0 | * | BackboneElement | An entity used in this activity
signature | 0 | * | Signature | Signature on target

## AuditEvent

- Canonical: `http://hl7.org/fhir/StructureDefinition/AuditEvent`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A record of an event made for purposes of maintaining a security log. Typical uses include detection
of intrusion attempts and monitoring for inappropriate usage.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
type | 1 | 1 | Coding | Type/identifier of event
subtype | 0 | * | Coding | More specific type/id for the event
action | 0 | 1 | code | Type of action performed during the event
period | 0 | 1 | Period | When the activity occurred
recorded | 1 | 1 | instant | Time when the event was recorded
outcome | 0 | 1 | code | Whether the event succeeded or failed
outcomeDesc | 0 | 1 | string | Description of the event outcome
purposeOfEvent | 0 | * | CodeableConcept | The purposeOfUse of the event
agent | 1 | * | BackboneElement | Actor involved in the event
source | 1 | 1 | BackboneElement | Audit Event Reporter
entity | 0 | * | BackboneElement | Data or objects used

## Device

- Canonical: `http://hl7.org/fhir/StructureDefinition/Device`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A type of a manufactured item that is used in the provision of healthcare without being
substantially changed through that activity. The device may be a medical or non-medical device.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Instance identifier
definition | 0 | 1 | Reference | The reference to the definition for the device
udiCarrier | 0 | * | BackboneElement | Unique Device Identifier (UDI) Barcode string
status | 0 | 1 | code | active \| inactive \| entered-in-error \| unknown
statusReason | 0 | * | CodeableConcept | online \| paused \| standby \| offline \| not-ready \| transduc-discon \| hw-discon \| off
distinctIdentifier | 0 | 1 | string | The distinct identification string
manufacturer | 0 | 1 | string | Name of device manufacturer
manufactureDate | 0 | 1 | dateTime | Date when the device was made
expirationDate | 0 | 1 | dateTime | Date and time of expiry of this device (if applicable)
lotNumber | 0 | 1 | string | Lot number of manufacture
serialNumber | 0 | 1 | string | Serial number assigned by the manufacturer
deviceName | 0 | * | BackboneElement | The name of the device as given by the manufacturer
modelNumber | 0 | 1 | string | The model number for the device
partNumber | 0 | 1 | string | The part number of the device
type | 0 | 1 | CodeableConcept | The kind or type of device
specialization | 0 | * | BackboneElement | The capabilities supported on a device, the standards to which the device conforms for a particular purpose, and used...
version | 0 | * | BackboneElement | The actual design of the device or software version running on the device
property | 0 | * | BackboneElement | The actual configuration settings of a device as it actually operates, e.g., regulation status, time properties
patient | 0 | 1 | Reference | Patient to whom Device is affixed
owner | 0 | 1 | Reference | Organization responsible for device
contact | 0 | * | ContactPoint | Details for human/organization for support
location | 0 | 1 | Reference | Where the device is found
url | 0 | 1 | uri | Network address to contact device
note | 0 | * | Annotation | Device notes and comments

## DeviceMetric

- Canonical: `http://hl7.org/fhir/StructureDefinition/DeviceMetric`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

Describes a measurement, calculation or setting capability of a medical device.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | * | Identifier | Instance identifier
type | 1 | 1 | CodeableConcept | Identity of metric, for example Heart Rate or PEEP Setting
unit | 0 | 1 | CodeableConcept | Unit of Measure for the Metric
source | 0 | 1 | Reference | Describes the link to the source Device
parent | 0 | 1 | Reference | Describes the link to the parent Device
operationalStatus | 0 | 1 | code | on \| off \| standby \| entered-in-error
color | 0 | 1 | code | black \| red \| green \| yellow \| blue \| magenta \| cyan \| white
category | 1 | 1 | code | measurement \| setting \| calculation \| unspecified
measurementPeriod | 0 | 1 | Timing | Describes the measurement repetition time
calibration | 0 | * | BackboneElement | Describes the calibrations that have been performed or that are required to be performed

## DocumentReference

- Canonical: `http://hl7.org/fhir/StructureDefinition/DocumentReference`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A reference to a document of any kind for any purpose. Provides metadata about the document so that
the document can be discovered and managed. The scope of a document is any seralized object with a
mime-type, so includes formal patient centric documents (CDA), cliical notes, scanned paper, and
non-patient specific documents like policy text.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
masterIdentifier | 0 | 1 | Identifier | Master Version Specific Identifier
identifier | 0 | * | Identifier | Other identifiers for the document
status | 1 | 1 | code | current \| superseded \| entered-in-error
docStatus | 0 | 1 | code | preliminary \| final \| amended \| entered-in-error
type | 0 | 1 | CodeableConcept | Kind of document (LOINC if possible)
category | 0 | * | CodeableConcept | Categorization of document
subject | 0 | 1 | Reference | Who/what is the subject of the document
date | 0 | 1 | instant | When this document reference was created
author | 0 | * | Reference | Who and/or what authored the document
authenticator | 0 | 1 | Reference | Who/what authenticated the document
custodian | 0 | 1 | Reference | Organization which maintains the document
relatesTo | 0 | * | BackboneElement | Relationships to other documents
description | 0 | 1 | string | Human-readable description
securityLabel | 0 | * | CodeableConcept | Document security-tags
content | 1 | * | BackboneElement | Document referenced
context | 0 | 1 | BackboneElement | Clinical context of document

## Composition

- Canonical: `http://hl7.org/fhir/StructureDefinition/Composition`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `draft`

A set of healthcare-related information that is assembled together into a single logical package
that provides a single coherent statement of meaning, establishes its own context and that has
clinical attestation with regard to who is making the statement. A Composition defines the structure
and narrative content necessary for a document. However, a Composition alone does not constitute a
document. Rather, the Composition must be the first entry in a Bundle where Bundle.type=document,
and any...

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | 1 | Identifier | Version-independent identifier for the Composition
status | 1 | 1 | code | preliminary \| final \| amended \| entered-in-error
type | 1 | 1 | CodeableConcept | Kind of composition (LOINC if possible)
category | 0 | * | CodeableConcept | Categorization of Composition
subject | 0 | 1 | Reference | Who and/or what the composition is about
encounter | 0 | 1 | Reference | Context of the Composition
date | 1 | 1 | dateTime | Composition editing time
author | 1 | * | Reference | Who and/or what authored the composition
title | 1 | 1 | string | Human Readable name/title
confidentiality | 0 | 1 | code | As defined by affinity domain
attester | 0 | * | BackboneElement | Attests to accuracy of composition
custodian | 0 | 1 | Reference | Organization which maintains the composition
relatesTo | 0 | * | BackboneElement | Relationships to other compositions/documents
event | 0 | * | BackboneElement | The clinical service(s) being documented
section | 0 | * | BackboneElement | Composition is broken into sections

## Bundle

- Canonical: `http://hl7.org/fhir/StructureDefinition/Bundle`
- Base type: `Resource`
- Abstract: `no`
- Status: `active`

A container for a collection of resources.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
identifier | 0 | 1 | Identifier | Persistent identifier for the bundle
type | 1 | 1 | code | document \| message \| transaction \| transaction-response \| batch \| batch-response \| history \| searchset \| collection
timestamp | 0 | 1 | instant | When the bundle was assembled
total | 0 | 1 | unsignedInt | If search, the total number of matches
link | 0 | * | BackboneElement | Links related to this Bundle
entry | 0 | * | BackboneElement | Entry in the bundle - will have a resource or information
signature | 0 | 1 | Signature | Digital Signature

## ValueSet

- Canonical: `http://hl7.org/fhir/StructureDefinition/ValueSet`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `active`

A ValueSet resource instance specifies a set of codes drawn from one or more code systems, intended
for use in a particular context. Value sets link between [[[CodeSystem]]] definitions and their use
in [coded elements](terminologies.html).

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
url | 0 | 1 | uri | Canonical identifier for this value set, represented as a URI (globally unique)
identifier | 0 | * | Identifier | Additional identifier for the value set (business identifier)
version | 0 | 1 | string | Business version of the value set
name | 0 | 1 | string | Name for this value set (computer friendly)
title | 0 | 1 | string | Name for this value set (human friendly)
status | 1 | 1 | code | draft \| active \| retired \| unknown
experimental | 0 | 1 | boolean | For testing purposes, not real usage
date | 0 | 1 | dateTime | Date last changed
publisher | 0 | 1 | string | Name of the publisher (organization or individual)
contact | 0 | * | ContactDetail | Contact details for the publisher
description | 0 | 1 | markdown | Natural language description of the value set
useContext | 0 | * | UsageContext | The context that the content is intended to support
jurisdiction | 0 | * | CodeableConcept | Intended jurisdiction for value set (if applicable)
immutable | 0 | 1 | boolean | Indicates whether or not any change to the content logical definition may occur
purpose | 0 | 1 | markdown | Why this value set is defined
copyright | 0 | 1 | markdown | Use and/or publishing restrictions
compose | 0 | 1 | BackboneElement | Content logical definition of the value set (CLD)
expansion | 0 | 1 | BackboneElement | Used when the value set is "expanded"

## CodeSystem

- Canonical: `http://hl7.org/fhir/StructureDefinition/CodeSystem`
- Base type: `DomainResource`
- Abstract: `no`
- Status: `active`

The CodeSystem resource is used to declare the existence of and describe a code system or code
system supplement and its key properties, and optionally define a part or all of its content.

Field | Min | Max | Type(s) | Description
--- | --- | --- | --- | ---
url | 0 | 1 | uri | Canonical identifier for this code system, represented as a URI (globally unique) (Coding.system)
identifier | 0 | * | Identifier | Additional identifier for the code system (business identifier)
version | 0 | 1 | string | Business version of the code system (Coding.version)
name | 0 | 1 | string | Name for this code system (computer friendly)
title | 0 | 1 | string | Name for this code system (human friendly)
status | 1 | 1 | code | draft \| active \| retired \| unknown
experimental | 0 | 1 | boolean | For testing purposes, not real usage
date | 0 | 1 | dateTime | Date last changed
publisher | 0 | 1 | string | Name of the publisher (organization or individual)
contact | 0 | * | ContactDetail | Contact details for the publisher
description | 0 | 1 | markdown | Natural language description of the code system
useContext | 0 | * | UsageContext | The context that the content is intended to support
jurisdiction | 0 | * | CodeableConcept | Intended jurisdiction for code system (if applicable)
purpose | 0 | 1 | markdown | Why this code system is defined
copyright | 0 | 1 | markdown | Use and/or publishing restrictions
caseSensitive | 0 | 1 | boolean | If code comparison is case sensitive
valueSet | 0 | 1 | canonical | Canonical reference to the value set with entire code system
hierarchyMeaning | 0 | 1 | code | grouped-by \| is-a \| part-of \| classified-with
compositional | 0 | 1 | boolean | If code system defines a compositional grammar
versionNeeded | 0 | 1 | boolean | If definitions are not stable
content | 1 | 1 | code | not-present \| example \| fragment \| complete \| supplement
supplements | 0 | 1 | canonical | Canonical URL of Code System this adds designations and properties to
count | 0 | 1 | unsignedInt | Total concepts in the code system
filter | 0 | * | BackboneElement | Filter that can be used in a value set
