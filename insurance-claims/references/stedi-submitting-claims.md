# Stedi Submitting Claims

## Table of Contents
- API-first model
- Endpoints by claim type
- Required headers
- Required high-level JSON objects
- Professional claim skeleton (837P)
- Institutional and dental differences
- Conditional requirements
- Coordination of benefits fields
- Attachments overview for submissions

## API-first model

For this skill, use Stedi APIs with deterministic scripts. Prefer JSON endpoints so scripts can validate structured payloads before submit and parse structured responses after submit.

Stedi translates JSON to HIPAA X12 for payer routing and returns JSON responses.

## Endpoints by claim type

- `837P` Professional claims (JSON): Professional Claims endpoint
- `837I` Institutional claims (JSON): Institutional Claims endpoint
- `837D` Dental claims (JSON): Dental Claims endpoint
- Raw X12 variants exist for each claim type if needed later

Use payer ID (`tradingPartnerServiceId`) from Payer Network/Payers API.

## Required headers

Every submission script should include:

- `Authorization: <STEDI_API_KEY>`
- `Content-Type: application/json`
- `Idempotency-Key: <unique-key>` (strongly recommended)

Idempotency keys prevent duplicate submissions during network retries.

## Required high-level JSON objects

Across claims, these top-level structures are central:

- `tradingPartnerServiceId`
- `tradingPartnerName`
- `submitter`
- `receiver`
- `subscriber` (and optional `dependent`)
- `claimInformation`
- Provider section (for example `billing`; plus rendering/attending structures by claim type)

Commonly required inside `claimInformation`:
- `patientControlNumber`
- `claimChargeAmount`
- `claimFrequencyCode`
- `claimFilingCode`
- Service line array (`serviceLines`)

## Professional claim skeleton (837P)

Use this as a starter payload shape for deterministic scripts.

```json
{
  "usageIndicator": "P",
  "tradingPartnerServiceId": "6400",
  "tradingPartnerName": "Cigna",
  "submitter": {
    "organizationName": "Example Submitter Org",
    "submitterIdentification": "SUBMITTER_ID",
    "contactInformation": {
      "name": "Claims Desk",
      "phoneNumber": "5552223333"
    }
  },
  "receiver": {
    "organizationName": "Cigna"
  },
  "subscriber": {
    "memberId": "MEMBER12345",
    "paymentResponsibilityLevelCode": "P",
    "firstName": "John",
    "lastName": "Doe",
    "gender": "M",
    "dateOfBirth": "19800101",
    "address": {
      "address1": "123 Main St",
      "city": "City",
      "state": "NY",
      "postalCode": "123450000"
    }
  },
  "billing": {
    "providerType": "BillingProvider",
    "npi": "1999999984",
    "taxonomyCode": "2084P0800X",
    "organizationName": "Example Clinic",
    "address": {
      "address1": "123 Main St",
      "city": "City",
      "state": "NY",
      "postalCode": "123450000"
    }
  },
  "claimInformation": {
    "claimFilingCode": "CI",
    "patientControlNumber": "ABC123DEF4567890",
    "claimChargeAmount": "109.20",
    "placeOfServiceCode": "02",
    "claimFrequencyCode": "1",
    "signatureIndicator": "Y",
    "benefitsAssignmentCertificationIndicator": "Y",
    "releaseInformationCode": "Y",
    "healthCareCodeInformation": [
      {
        "diagnosisTypeCode": "ABK",
        "diagnosisCode": "F1111"
      }
    ],
    "serviceLines": [
      {
        "serviceDate": "20240101",
        "providerControlNumber": "LINECTRL001",
        "professionalService": {
          "procedureIdentifier": "HC",
          "procedureCode": "90837",
          "lineItemChargeAmount": "109.20",
          "measurementUnit": "UN",
          "serviceUnitCount": "1",
          "compositeDiagnosisCodePointers": {
            "diagnosisCodePointers": ["1"]
          }
        }
      }
    ]
  }
}
```

For test submissions, set:
- `usageIndicator: "T"` (JSON)

## Institutional and dental differences

### Institutional (837I)
- Includes facility/admission style data and institutional coding constructs.
- May require revenue-code oriented service lines and institutional claim pricing/adjudication elements.

### Dental (837D)
- Includes dental-specific procedure context (for example tooth/surface/oral cavity structures where applicable).
- Uses ADA-oriented coding patterns.

Implementation note: keep separate payload schema files per claim type in scripts/templates to avoid mixed-field errors.

## Conditional requirements

Stedi uses required + conditionally required objects:
- Required means always present.
- Conditional means required only in certain scenarios.

Example pattern:
- `subscriber` is broadly required.
- `dependent` may be omitted when patient is subscriber.
- A provider supervisory structure may be required only in supervised care situations.

Script design recommendation:
- Perform local pre-flight validation and classify failures as:
  - `missing_required`
  - `missing_conditional`
  - `format_error`

## Coordination of benefits fields

For secondary/tertiary submissions:
- Set `subscriber.paymentResponsibilityLevelCode` to:
  - `S` for secondary
  - `T` for tertiary
- Include prior payer adjudication details in `claimInformation.otherSubscriberInformation`.
- Include claim-level and line-level adjudication amounts from prior payer ERA when required.

## Attachments overview for submissions

If claim requires supporting documents:
- Include attachment reference fields in claim payload (`attachmentReportTypeCode`, `attachmentTransmissionCode`, and attachment identifier field).
- For JSON workflows, create/upload attachment first and pass attachment ID in claim submission fields.

See `stedi-attachments-and-mcp.md` for full attachment flow.
