---
name: rx-enrollment
description: "Pharmacy benefit enrollment and eligibility including member adds, changes, and terminations. Triggers: pharmacy enrollment, eligibility, BIN, PCN, group number, pharmacy benefit, member ID, cardholder, coverage activation"
---

# Pharmacy Enrollment Cohort

A cohort template for generating pharmacy benefit enrollment and eligibility transactions including member adds, changes, and terminations.

## For Claude

Use this skill when the user requests pharmacy enrollment or eligibility cohorts. This teaches you how to generate **realistic pharmacy benefit enrollment** with BIN/PCN/Group configurations and coverage activation.

**When to apply this skill:**

- User mentions rx enrollment or pharmacy enrollment
- User requests pharmacy eligibility or member cohorts
- User specifies BIN, PCN, or cardholder ID
- User asks for pharmacy card or coverage activation
- User needs PBM enrollment examples

**Key capabilities this skill provides:**

- How to structure pharmacy enrollment transactions
- How to configure BIN/PCN/Group identifiers
- How to model coverage effective dates
- How to handle cardholder vs dependent enrollment
- How to generate mail order eligibility flags

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: RxMemberSim
- **Tags**: pharmacy, enrollment, eligibility, PBM, member
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic pharmacy benefit enrollment transactions. It models member adds, changes, and terminations with proper BIN/PCN/Group configuration and coverage dates.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "rx enrollment", "pharmacy enrollment"
- "pharmacy eligibility", "rx member"
- "BIN PCN", "cardholder ID"
- "pharmacy card", "rx coverage"

**Enrollment Cohorts**:

- "Generate a pharmacy member enrollment"
- "Create a pharmacy eligibility record"
- "Generate a pharmacy coverage termination"

## Trigger Phrases

- rx enrollment
- pharmacy enrollment
- pharmacy eligibility
- rx member
- pharmacy member
- PBM enrollment
- rx card
- pharmacy card
- BIN PCN
- cardholder ID
- pharmacy coverage
- rx coverage start
- pharmacy benefit activation

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| transaction_type | string | add | add, change, termination, reinstatement |
| plan_type | string | commercial | commercial, medicare_d, medicaid |
| coverage_tier | string | employee_only | employee_only, employee_spouse, employee_children, family |
| effective_date | date | first_of_month | Any valid date |
| mail_order_eligible | boolean | true | true, false |

## Pharmacy Enrollment Transaction Types

### Add (New Enrollment)
New member activation for pharmacy benefits.

**Trigger Conditions:**
- New hire enrollment with pharmacy benefit
- Open enrollment plan selection
- Qualifying life event adding pharmacy coverage
- Medicare Part D enrollment
- COBRA election including pharmacy

**Required Data Elements:**
- Subscriber demographics
- BIN/PCN/Group assignment
- Cardholder ID
- Person codes for family members
- Rx plan selection
- Coverage effective date

**Example Request:** "Generate a new pharmacy enrollment for a family"

### Change
Modification to existing pharmacy enrollment.

**Trigger Conditions:**
- Plan change (different formulary/tier structure)
- Add/remove dependents
- Address change (may affect mail order)
- PCP change (for plans requiring PCP for Rx PA)
- Carrier change

**Required Data Elements:**
- Member cardholder ID
- Change effective date
- Changed data elements
- New BIN/PCN if carrier change

**Example Request:** "Generate an enrollment change for a new pharmacy plan"

### Termination
End of pharmacy coverage.

**Trigger Conditions:**
- Employment termination
- Loss of eligibility
- Medicare enrollment (commercial -> Part D)
- Death
- Voluntary disenrollment

**Required Data Elements:**
- Member cardholder ID
- Termination date
- Reason code
- COBRA eligibility

**Example Request:** "Generate a pharmacy termination"

## Pharmacy Member Data Elements

### RxMember Structure
```json
{
  "member_id": "MEM001234567",
  "cardholder_id": "ABC123456789",
  "bin": "003858",
  "pcn": "A4",
  "group_number": "RX1234",
  "person_code": "01",
  "rx_plan_code": "RX-COMMERCIAL-3TIER",
  "coverage_start": "2025-02-01",
  "coverage_end": null,
  "relationship_code": "18",
  "subscriber_id": null,
  "mail_order_eligible": true,
  "specialty_eligible": true
}
```

### Person Code Assignments

| Person Code | Description | Use When |
|-------------|-------------|----------|
| 01 | Subscriber/Cardholder | Primary member |
| 02 | Spouse | Spouse/domestic partner |
| 03 | Child 1 | First dependent child |
| 04 | Child 2 | Second dependent child |
| 05-09 | Additional dependents | Children 3+ |

### BIN/PCN Assignment

| PBM | BIN | PCN | Description |
|-----|-----|-----|-------------|
| Express Scripts | 003858 | A4 | Commercial |
| CVS Caremark | 004336 | ADV | Commercial |
| OptumRx | 610014 | 01 | Commercial |
| Humana Rx | 015581 | HRX | Medicare Part D |
| Test Environment | 012345 | TEST | Sandbox testing |

## Pharmacy Plan Types

### Commercial PBM
```json
{
  "rx_plan_code": "RX-COMMERCIAL-3TIER",
  "plan_name": "Commercial 3-Tier Formulary",
  "plan_type": "commercial",
  "formulary_id": "FORM2025-A",
  "tier_structure": [
    { "tier": 1, "name": "Preferred Generic", "copay_retail_30": 10.00, "copay_retail_90": 25.00, "copay_mail_90": 20.00 },
    { "tier": 2, "name": "Preferred Brand", "copay_retail_30": 35.00, "copay_retail_90": 87.50, "copay_mail_90": 70.00 },
    { "tier": 3, "name": "Non-Preferred", "copay_retail_30": 60.00, "copay_retail_90": 150.00, "copay_mail_90": 120.00 }
  ],
  "specialty_coinsurance": 25,
  "specialty_max_per_fill": 250.00,
  "rx_deductible": 0,
  "rx_oop_max": 2500.00,
  "combined_with_medical_oop": false
}
```

### Medicare Part D
```json
{
  "rx_plan_code": "RX-PARTD-STD",
  "plan_name": "Medicare Part D Standard",
  "plan_type": "medicare_d",
  "formulary_id": "FORM2025-PARTD",
  "benefit_phases": {
    "deductible": 590,
    "initial_coverage_limit": 5030,
    "coverage_gap_end": 8000,
    "catastrophic_threshold": 8000
  },
  "tier_structure": [
    { "tier": 1, "name": "Preferred Generic", "copay": 5.00 },
    { "tier": 2, "name": "Generic", "copay": 15.00 },
    { "tier": 3, "name": "Preferred Brand", "copay": 47.00 },
    { "tier": 4, "name": "Non-Preferred", "coinsurance": 40 },
    { "tier": 5, "name": "Specialty", "coinsurance": 25 }
  ],
  "coverage_gap_discount": 75,
  "low_income_subsidy": false
}
```

### High Deductible with HSA
```json
{
  "rx_plan_code": "RX-HDHP-HSA",
  "plan_name": "HDHP Pharmacy Benefit",
  "plan_type": "commercial",
  "formulary_id": "FORM2025-HDHP",
  "rx_deductible": 1600,
  "rx_deductible_applies_to": ["brand", "specialty"],
  "preventive_drugs_no_deductible": true,
  "post_deductible_tiers": [
    { "tier": 1, "name": "Generic", "copay": 10.00 },
    { "tier": 2, "name": "Preferred Brand", "copay": 40.00 },
    { "tier": 3, "name": "Non-Preferred Brand", "coinsurance": 30 },
    { "tier": 4, "name": "Specialty", "coinsurance": 20, "max_per_fill": 200.00 }
  ],
  "combined_with_medical_oop": true,
  "combined_oop_max": 7000
}
```

## Eligibility Verification

### Pharmacy Eligibility Request (E1)
```json
{
  "transaction_code": "E1",
  "request_datetime": "2025-01-15T10:30:00",
  "bin": "003858",
  "pcn": "A4",
  "cardholder_id": "ABC123456789",
  "group_number": "RX1234",
  "person_code": "01",
  "patient": {
    "first_name": "MICHAEL",
    "last_name": "JOHNSON",
    "date_of_birth": "1985-03-15",
    "gender": "M"
  },
  "date_of_service": "2025-01-15"
}
```

### Pharmacy Eligibility Response
```json
{
  "transaction_code": "E1",
  "response_status": "A",
  "response_datetime": "2025-01-15T10:30:01",
  "member": {
    "cardholder_id": "ABC123456789",
    "first_name": "MICHAEL",
    "last_name": "JOHNSON",
    "date_of_birth": "1985-03-15",
    "coverage_status": "active"
  },
  "plan": {
    "rx_plan_code": "RX-COMMERCIAL-3TIER",
    "plan_name": "Commercial 3-Tier Formulary",
    "group_number": "RX1234",
    "group_name": "Acme Corporation"
  },
  "coverage": {
    "effective_date": "2025-02-01",
    "termination_date": null,
    "mail_order_eligible": true,
    "specialty_eligible": true,
    "maintenance_choice": "90_day_required_after_3_fills"
  },
  "accumulators": {
    "rx_deductible": {
      "limit": 0,
      "applied": 0,
      "remaining": 0
    },
    "rx_oop_max": {
      "limit": 2500.00,
      "applied": 125.00,
      "remaining": 2375.00
    }
  },
  "messages": [
    "Mail order eligible for maintenance medications",
    "Specialty pharmacy: CVS Specialty 1-800-237-2767"
  ]
}
```

## Examples

### Example 1: New Pharmacy Enrollment

**Request:** "Generate a new pharmacy enrollment for a family with commercial coverage"

```json
{
  "enrollment": {
    "transaction_type": "add",
    "effective_date": "2025-02-01",
    "enrollment_reason": "new_hire",
    "rx_plan": {
      "rx_plan_code": "RX-COMMERCIAL-3TIER",
      "plan_name": "Commercial 3-Tier Formulary",
      "bin": "003858",
      "pcn": "A4",
      "group_number": "RX1234"
    },
    "subscriber": {
      "member_id": "MEM001234567",
      "cardholder_id": "ABC123456789",
      "person_code": "01",
      "name": {
        "given_name": "Michael",
        "family_name": "Johnson"
      },
      "birth_date": "1985-03-15",
      "gender": "M",
      "address": {
        "street_address": "456 Oak Avenue",
        "city": "Springfield",
        "state": "IL",
        "postal_code": "62702"
      },
      "relationship_code": "18"
    },
    "dependents": [
      {
        "member_id": "MEM001234568",
        "cardholder_id": "ABC123456789",
        "person_code": "02",
        "name": {
          "given_name": "Sarah",
          "family_name": "Johnson"
        },
        "birth_date": "1987-07-22",
        "gender": "F",
        "relationship_code": "01"
      },
      {
        "member_id": "MEM001234569",
        "cardholder_id": "ABC123456789",
        "person_code": "03",
        "name": {
          "given_name": "Emma",
          "family_name": "Johnson"
        },
        "birth_date": "2015-11-10",
        "gender": "F",
        "relationship_code": "19"
      }
    ],
    "coverage": {
      "coverage_tier": "family",
      "coverage_start": "2025-02-01",
      "mail_order_eligible": true,
      "specialty_eligible": true,
      "maintenance_choice": "90_day_required_after_3_fills"
    }
  }
}
```

### Example 2: Medicare Part D Enrollment

**Request:** "Generate a Medicare Part D enrollment for a 68-year-old"

```json
{
  "enrollment": {
    "transaction_type": "add",
    "effective_date": "2025-01-01",
    "enrollment_reason": "medicare_age_in",
    "rx_plan": {
      "rx_plan_code": "RX-PARTD-STD",
      "plan_name": "Medicare Part D Standard",
      "bin": "015581",
      "pcn": "HRX",
      "group_number": "PARTD2025",
      "cms_contract_id": "H1234",
      "pbp_id": "001"
    },
    "subscriber": {
      "member_id": "MBI1234567890",
      "cardholder_id": "MBI1234567890",
      "medicare_beneficiary_id": "1EG4-TE5-MK72",
      "person_code": "01",
      "name": {
        "given_name": "Robert",
        "family_name": "Williams"
      },
      "birth_date": "1957-06-15",
      "gender": "M",
      "address": {
        "street_address": "789 Maple Street",
        "city": "Chicago",
        "state": "IL",
        "postal_code": "60601"
      }
    },
    "coverage": {
      "coverage_start": "2025-01-01",
      "part_d_phase": "deductible",
      "low_income_subsidy": false,
      "lis_level": null,
      "late_enrollment_penalty": false,
      "creditable_coverage": true
    },
    "initial_accumulators": {
      "deductible": { "limit": 590, "applied": 0 },
      "troop": { "limit": 8000, "applied": 0 },
      "gross_drug_cost": { "applied": 0 }
    }
  }
}
```

### Example 3: Pharmacy Termination with COBRA

**Request:** "Generate a pharmacy termination with COBRA eligibility"

```json
{
  "enrollment": {
    "transaction_type": "termination",
    "effective_date": "2025-01-31",
    "termination_reason": "employment_end",
    "subscriber": {
      "member_id": "MEM001234567",
      "cardholder_id": "ABC123456789",
      "bin": "003858",
      "pcn": "A4",
      "name": {
        "given_name": "Michael",
        "family_name": "Johnson"
      }
    },
    "coverage_termination": {
      "last_coverage_date": "2025-01-31",
      "final_accumulators": {
        "rx_oop_max": {
          "limit": 2500.00,
          "applied": 450.00
        }
      }
    },
    "cobra": {
      "eligible": true,
      "notification_date": "2025-02-14",
      "election_deadline": "2025-04-15",
      "cobra_rx_plan": "RX-COBRA-3TIER",
      "cobra_bin": "003858",
      "cobra_pcn": "COBRA",
      "cobra_monthly_premium": 95.00,
      "coverage_continuation_months": 18
    },
    "dependents_terminated": [
      {
        "member_id": "MEM001234568",
        "person_code": "02",
        "last_coverage_date": "2025-01-31",
        "cobra_eligible": true
      },
      {
        "member_id": "MEM001234569",
        "person_code": "03",
        "last_coverage_date": "2025-01-31",
        "cobra_eligible": true
      }
    ]
  }
}
```

## Validation Rules

### Enrollment Validation
1. BIN must be exactly 6 digits
2. PCN must be alphanumeric, typically 2-10 characters
3. Cardholder ID format must match PBM requirements
4. Person codes must be unique within cardholder
5. Coverage effective date >= submission date
6. Dependents must have valid relationship codes
7. Medicare Part D requires valid MBI

### Eligibility Validation
1. Patient name must match enrollment
2. Date of birth must match enrollment
3. Date of service must be within coverage period
4. BIN/PCN/Group combination must be valid

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| NCPDP E1 | "as NCPDP eligibility" | Eligibility transaction |
| CSV | "as CSV" | Bulk enrollment export |
| SQL | "as SQL" | Database loading |

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Cardholder ID | Unique identifier | RX0001234567 |
| BIN | 6-digit processor ID | 003858 |
| PCN | Processor control number | A4, ADV |
| Group number | Plan group identifier | RXGROUP001 |
| Effective date | Valid date | 2025-01-01 |
| Term date | On or after effective | 2025-12-31, null (active) |
| Relationship | subscriber, spouse, dependent | "subscriber" |
| Person code | Position in family | 01 (subscriber), 02 (spouse) |
| DOB | Valid date, not future | 1975-05-15 |

### Business Rules

- **BIN/PCN/Group**: Required for claim routing; must match processor configuration
- **Cardholder ID**: Unique per member; may include check digit
- **Coverage Hierarchy**: Subscriber primary; dependents linked to subscriber
- **Effective Dates**: Coverage active from effective_date through term_date
- **COB (Coordination of Benefits)**: Member may have multiple pharmacy coverages
- **Medicare Part D**: Special enrollment rules and LIS (Low Income Subsidy) flags
- **COBRA**: Continuation coverage maintains same BIN/PCN/Group
- **Retroactive Changes**: Enrollment changes may be backdated for qualifying events

## Related Skills

### RxMemberSim
- [SKILL.md](SKILL.md) - RxMemberSim overview
- [retail-pharmacy.md](retail-pharmacy.md) - Retail pharmacy claims
- [rx-accumulator.md](rx-accumulator.md) - Pharmacy accumulator tracking
- [formulary-management.md](formulary-management.md) - Formulary assigned at enrollment

### Cross-Product: MemberSim
- [../membersim/enrollment-eligibility.md](../membersim/enrollment-eligibility.md) - Medical benefit enrollment

> **Integration Pattern:** Medical enrollment (MemberSim) and pharmacy enrollment (this skill) typically occur together. Use MemberSim for medical coverage setup, RxMemberSim for pharmacy benefit setup. Ensure coverage effective dates match, and subscriber/dependent relationships are consistent.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - Code systems
- [../../references/data-models.md](../../references/data-models.md) - Data models
