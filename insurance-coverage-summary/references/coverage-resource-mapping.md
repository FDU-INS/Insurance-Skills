# FHIR Coverage Resource Field Mappings

## Coverage Resource (R4) -- Complete Field Reference

### Resource Structure

| FHIR Path | Cardinality | Data Type | Description |
|-----------|-------------|-----------|-------------|
| Coverage.identifier | 0..* | Identifier | Business identifiers for this coverage |
| Coverage.status | 1..1 | code | active, cancelled, draft, entered-in-error |
| Coverage.type | 0..1 | CodeableConcept | Coverage category (HMO, PPO, etc.) |
| Coverage.policyHolder | 0..1 | Reference(Patient/RelatedPerson/Organization) | Owner of the policy |
| Coverage.subscriber | 0..1 | Reference(Patient/RelatedPerson) | Plan subscriber |
| Coverage.subscriberId | 0..1 | string | Member/subscriber ID number |
| Coverage.beneficiary | 1..1 | Reference(Patient) | The patient who benefits |
| Coverage.dependent | 0..1 | string | Dependent number |
| Coverage.relationship | 0..1 | CodeableConcept | Beneficiary-to-subscriber relationship |
| Coverage.period | 0..1 | Period | Coverage effective period |
| Coverage.payor | 1..* | Reference(Organization/Patient/RelatedPerson) | Insurance company |
| Coverage.class | 0..* | BackboneElement | Plan classification details |
| Coverage.order | 0..1 | positiveInt | Relative order of coverage (1=primary) |
| Coverage.network | 0..1 | string | Network name |
| Coverage.costToBeneficiary | 0..* | BackboneElement | Patient cost sharing |
| Coverage.subrogation | 0..1 | boolean | Subrogation rights |
| Coverage.contract | 0..* | Reference(Contract) | Contract details |

### Coverage.status Codes

| Code | Display | Description |
|------|---------|-------------|
| active | Active | Coverage is currently in effect |
| cancelled | Cancelled | Coverage has been terminated |
| draft | Draft | Coverage is being set up, not yet active |
| entered-in-error | Entered in Error | Coverage was created in error |

### Coverage.type Codes

**System:** `http://terminology.hl7.org/CodeSystem/v3-ActCode`

| Code | Display | Description |
|------|---------|-------------|
| EHCPOL | Extended healthcare | Extended health care policy |
| HSAPOL | Health spending account | HSA-based coverage |
| AUTOPOL | Automobile | Auto insurance coverage |
| COL | Collision | Collision coverage |
| UNINSMOT | Uninsured motorist | Uninsured motorist coverage |
| PUBLICPOL | Public | Government-funded coverage |
| DENTPRG | Dental program | Dental insurance |
| DISEPRG | Disease program | Disease management program |
| CANPRG | Women's cancer | Women's cancer detection program |
| ENDRENAL | End renal program | End-stage renal disease program |
| HIVAIDS | HIV-AIDS program | HIV/AIDS program |
| MANDPOL | Mandatory health program | Mandatory health insurance |
| MENTPRG | Mental health program | Mental health coverage |
| SAFNET | Safety net | Safety net coverage |
| SUBPRG | Substance use program | Substance use disorder program |
| SUBSIDIZ | Subsidized health program | Subsidized coverage |
| SUBSIDMC | Subsidized managed care | Subsidized managed care |
| SUBSUPP | Subsidized supplemental | Subsidized supplemental health |
| WCBPOL | Worker's comp | Workers' compensation coverage |

### Additional Insurance Type Codes

**System:** `http://terminology.hl7.org/CodeSystem/v2-0072` (commonly used in practice)

| Code | Display |
|------|---------|
| 12 | Medicare Secondary Working Aged Beneficiary or Spouse with Employer Group Health Plan |
| 13 | Medicare Secondary End-Stage Renal Disease Beneficiary |
| 14 | Medicare Secondary, No-fault Insurance including Auto is Primary |
| 15 | Medicare Secondary Worker's Compensation |
| 16 | Medicare Secondary Public Health Service or Other Federal Agency |
| 41 | Medicare Secondary Black Lung |
| 42 | Medicare Secondary Veteran's Administration |
| 43 | Medicare Secondary Disabled Beneficiary Under Age 65 with Large Group Health Plan (LGHP) |
| 47 | Medicare Secondary, Other Liability Insurance is Primary |
| AP | Auto Insurance Policy |
| C1 | Commercial |
| CP | Medicare Conditionally Primary |
| GP | Group Policy |
| HM | Health Maintenance Organization (HMO) |
| HN | Health Maintenance Organization (HMO) -- Medicare Risk |
| IP | Individual Policy |
| MA | Medicare Part A |
| MB | Medicare Part B |
| MC | Medicaid |
| OF | Other Federal Program |
| SP | Supplemental Policy |

### Coverage.class -- Classification Types

The `class` array contains multiple entries, each representing a different level of classification:

| class.type Code | Description | Example Value | Example Name |
|-----------------|-------------|---------------|--------------|
| group | Group | 123456 | Acme Corporation |
| subgroup | SubGroup | ABC | Division A |
| plan | Plan | PPO-Gold | PPO Gold Plan |
| subplan | SubPlan | PPO-Gold-Dental | Dental Rider |
| class | Class | Employee+Family | Employee Plus Family |
| subclass | SubClass | Full-Time | Full-Time Employee |
| sequence | Sequence | 1 | (Sequence number) |
| rxbin | RX BIN | 004336 | RX BIN Number |
| rxpcn | RX PCN | ADV | RX PCN |
| rxid | RX ID | MRX12345 | RX Member ID |
| rxgroup | RX Group | RXGRP001 | RX Group Name |

**System for class type codes:** `http://terminology.hl7.org/CodeSystem/coverage-class`

### Coverage.relationship Codes

**System:** `http://terminology.hl7.org/CodeSystem/subscriber-relationship`

| Code | Display | Description |
|------|---------|-------------|
| self | Self | Beneficiary is the subscriber |
| spouse | Spouse | Beneficiary is spouse of subscriber |
| child | Child | Beneficiary is child of subscriber |
| parent | Parent | Beneficiary is parent of subscriber |
| common | Common Law Spouse | Common law spouse |
| other | Other | Other relationship |
| injured | Injured Party | Injured party (auto/liability) |

### Coverage.costToBeneficiary

```json
{
  "costToBeneficiary": [
    {
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/coverage-copay-type",
          "code": "copay"
        }]
      },
      "valueMoney": {
        "value": 25.00,
        "currency": "USD"
      }
    },
    {
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/coverage-copay-type",
          "code": "coinsurance"
        }]
      },
      "valueQuantity": {
        "value": 20,
        "unit": "%"
      }
    }
  ]
}
```

**Copay Type Codes:**

| Code | Display |
|------|---------|
| gpvisit | GP Office Visit |
| spvisit | Specialist Office Visit |
| emergency | Emergency |
| inpthosp | Inpatient Hospital |
| televisit | Tele Visit |
| urgentcare | Urgent Care |
| copay | Copay Amount |
| coinsurance | Coinsurance Rate |
| deductible | Deductible |

## Coordination of Benefits (COB) Rules

### Standard COB Priority Rules

When a patient has multiple active Coverage resources and `order` is not populated, apply these rules to determine primary vs secondary:

#### Rule 1: Employee vs Dependent
- Coverage where `relationship` = "self" (the person is the subscriber) takes priority over coverage where the person is a dependent
- Exception: Medicare rules may override this

#### Rule 2: Birthday Rule (for Dependent Children)
- When a child is covered under both parents' plans
- The plan of the parent whose birthday (month and day, NOT year) falls earlier in the calendar year is primary
- If same birthday: plan that has covered the parent longer is primary
- If parents are divorced: custodial parent's plan is primary, then stepparent's plan, then non-custodial parent's plan

#### Rule 3: Active vs COBRA/Continuation
- Active employee coverage is primary over COBRA or state continuation coverage

#### Rule 4: Longer Coverage
- If no other rule applies, the plan that has covered the person longer is primary

### Medicare Coordination Rules

| Scenario | Primary | Secondary |
|----------|---------|-----------|
| Working aged (65+) with EGHP (20+ employees) | EGHP | Medicare |
| Working aged (65+) without EGHP | Medicare | (none or supplemental) |
| Disabled (< 65) with LGHP (100+ employees) | LGHP | Medicare |
| Disabled (< 65) without LGHP | Medicare | (other) |
| ESRD -- first 30 months | EGHP | Medicare |
| ESRD -- after 30 months | Medicare | EGHP |
| Workers' Compensation claim | Workers' Comp | Medicare |
| Auto insurance / liability claim | Auto/Liability | Medicare |
| Veterans Affairs | VA | Medicare (separate systems) |

### Medicaid Coordination Rules

- Medicaid is almost always the payer of last resort
- If patient has any other active coverage, that coverage is primary
- Exception: Some state-specific Medicaid programs may have different rules
- Indian Health Service: Medicaid may coordinate with IHS

### Medicare Supplement (Medigap) Coordination

- Medigap is always secondary to Medicare
- Medigap pays after Medicare's payment determination
- Medigap plan type (A through N) determines what it covers:
  - Part A coinsurance, hospital costs, blood, Part B copayment/coinsurance, skilled nursing coinsurance
  - Some plans cover Part B excess charges and foreign travel emergency

## Organization Resource -- Payor Details

### Key Fields for Insurance Organizations

| FHIR Path | Description | Use |
|-----------|-------------|-----|
| Organization.name | Company name | Display in summary |
| Organization.identifier | NPI, Tax ID, Payer ID | Claims submission |
| Organization.type | Organization type | Classification |
| Organization.telecom | Phone, fax, website | Contact for verification |
| Organization.address | Mailing address | Claims mailing address |
| Organization.contact | Named contacts | Specific department contacts |

### Payer ID Systems

| System | Description | Example |
|--------|-------------|---------|
| `http://hl7.org/fhir/sid/us-npi` | National Provider Identifier | 1234567890 |
| `urn:oid:2.16.840.1.113883.4.4` | IRS Tax ID (EIN) | 12-3456789 |
| `http://www.cms.gov/Medicare/Coding/NationalProvIdentStand` | CMS Payer ID | 00450 |
| (varies by clearinghouse) | Electronic Payer ID | BCBSTX001 |

## Provider-Specific Notes

### EPIC
- Coverage resources populated from registration/insurance verification
- Class array typically includes group, plan, and sometimes rxbin/rxpcn
- `subscriberId` usually populated as the member ID on the insurance card
- May include coverage extensions for authorization status
- Benefits detail usually NOT in FHIR Coverage; available through EPIC's eligibility API

### Cerner
- Coverage resources follow standard R4 mapping
- May have separate Coverage resources for medical vs pharmacy vs dental
- Subscriber and policyholder references usually point to Patient or RelatedPerson
- `order` field more commonly populated than in other systems

### GCP Healthcare API
- Standard FHIR R4 Coverage mapping
- Depends entirely on source data quality
- No provider-specific extensions

## Common Validation Checks

| Check | How to Verify | Flag If |
|-------|--------------|---------|
| Coverage active | `status` = "active" AND `period` is current | Status mismatch with period |
| Subscriber ID present | `subscriberId` is non-null and non-empty | Missing (required for claims) |
| Payor resolves | `payor` reference returns valid Organization | Reference broken or Organization missing |
| Group number present | `class` array contains entry with type "group" | Missing (common for commercial plans) |
| Plan name present | `class` array contains entry with type "plan" | Missing (affects identification) |
| Order specified | `order` field is populated for each active Coverage | Multiple active with no order = COB ambiguity |
| Period valid | `period.start` <= `period.end` (if both present) | Start after end = data error |
| No duplicate active | Only one Coverage per payor with overlapping active periods | Duplicate = data entry error |
