---
name: enrollment-eligibility
description: "Member enrollment transactions (834) and eligibility verification responses (270/271). Triggers: enrollment, eligibility, member add, 834, 270, 271, COBRA, open enrollment, QLE, coverage verification"
---

# Enrollment and Eligibility Cohort

A cohort template for generating member enrollment transactions and eligibility verification responses.

## For Claude

Use this skill when the user requests enrollment or eligibility cohorts. This teaches you how to generate **realistic enrollment transactions** (834) and eligibility responses (270/271).

**When to apply this skill:**

- User mentions enrollment, eligibility, or member add
- User requests 834, 270, or 271 transactions
- User specifies COBRA, open enrollment, or QLE
- User asks for eligibility verification cohorts
- User needs coverage verification examples

**Key capabilities this skill provides:**

- How to structure 834 enrollment transactions
- How to generate 270/271 eligibility inquiries and responses
- How to model qualifying life events and effective dates
- How to handle COBRA and continuation coverage
- How to represent coverage tiers and dependent relationships

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: MemberSim
- **Tags**: enrollment, eligibility, 834, 270, 271, payer
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic enrollment and eligibility transactions. It models member adds, changes, terminations, and eligibility verification with proper effective dates and coverage details.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "enrollment", "eligibility", "member enrollment"
- "834", "270", "271"
- "eligibility check", "coverage verification"
- "COBRA", "open enrollment", "QLE"

**Enrollment Cohorts**:

- "Generate a new member enrollment"
- "Create an eligibility verification response"
- "Generate a COBRA enrollment"

## Trigger Phrases

- enrollment
- eligibility
- member enrollment
- benefit enrollment
- 834
- 270
- 271
- eligibility check
- eligibility inquiry
- coverage verification
- member add
- new member
- termination
- COBRA
- open enrollment
- qualifying life event
- QLE

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| transaction_type | string | add | add, change, termination, reinstatement |
| coverage_type | string | employee_only | employee_only, employee_spouse, employee_children, family |
| plan_type | string | PPO | HMO, PPO, EPO, POS, HDHP |
| enrollment_reason | string | new_hire | new_hire, open_enrollment, qle, cobra |
| effective_date | date | first_of_month | Any valid date |

## Enrollment Transaction Types

### Add (INS*Y)
New member enrollment into a benefit plan.

**Trigger Conditions:**
- New hire enrollment
- Open enrollment selection
- Qualifying life event (marriage, birth, etc.)
- COBRA election

**Required Data Elements:**
- Subscriber demographics
- Dependent demographics (if applicable)
- Plan selection
- Coverage dates
- Premium information

**Example Request:** "Generate a new employee enrollment for family coverage"

### Change (INS*Y with change reason)
Modification to existing enrollment.

**Trigger Conditions:**
- Address change
- Dependent add/remove
- Plan change
- PCP change (HMO)
- Name change (marriage/divorce)

**Required Data Elements:**
- Member identifier
- Change effective date
- Changed data elements
- Change reason code

**Example Request:** "Generate an enrollment change to add a newborn dependent"

### Termination (INS*N)
End of coverage for a member.

**Trigger Conditions:**
- Employment termination
- Loss of eligibility
- Voluntary disenrollment
- Death
- COBRA exhaustion

**Required Data Elements:**
- Member identifier
- Termination date
- Termination reason
- COBRA eligibility indicator

**Example Request:** "Generate a termination due to employment end"

### Reinstatement
Restoration of previously terminated coverage.

**Trigger Conditions:**
- Retroactive reinstatement
- Error correction
- Return from leave
- COBRA late election

**Required Data Elements:**
- Original enrollment reference
- Reinstatement date
- Gap coverage handling

**Example Request:** "Generate a reinstatement for return from medical leave"

## Coverage Tiers

| Tier Code | Description | Includes |
|-----------|-------------|----------|
| EE | Employee Only | Subscriber only |
| ES | Employee + Spouse | Subscriber + spouse/domestic partner |
| EC | Employee + Child(ren) | Subscriber + dependent children |
| FAM | Family | Subscriber + spouse + children |

## Relationship Codes

| Code | Description | Use When |
|------|-------------|----------|
| 18 | Self | Subscriber |
| 01 | Spouse | Legally married spouse |
| 19 | Child | Biological/adopted child under age limit |
| 15 | Stepchild | Child of spouse |
| 53 | Life Partner | Domestic partner |
| 29 | Significant Other | Unmarried partner |
| 23 | Sponsored Dependent | Other dependent (disabled adult child) |

## Enrollment Reason Codes

| Code | Description | Cohort |
|------|-------------|----------|
| 02 | New Hire | Employment start |
| 07 | Open Enrollment | Annual enrollment period |
| 08 | Qualifying Life Event | Marriage, birth, etc. |
| 25 | COBRA | Continuation coverage |
| 33 | Dependent Aging Out | Reaches age limit |
| 41 | Termination of Employment | Job loss |
| 43 | Death | Subscriber or dependent death |

## Qualifying Life Events (QLE)

| Event | Enrollment Window | Effective Date Rule |
|-------|-------------------|---------------------|
| Marriage | 30-60 days | Date of marriage or first of next month |
| Birth/Adoption | 30-60 days | Date of birth/adoption |
| Divorce | 30-60 days | Date decree is final |
| Loss of Other Coverage | 30-60 days | Date of loss |
| Move to New Service Area | 30-60 days | First of next month |
| Gain of Dependent | 30-60 days | Date of event |
| Loss of Dependent | 30-60 days | First of next month |

## Eligibility Verification

### 270 - Eligibility Inquiry

Request information about a member's coverage.

**Inquiry Types:**
| Code | Description |
|------|-------------|
| 30 | Health Benefit Plan Coverage |
| 33 | Chiropractic |
| 35 | Dental Care |
| 47 | Hospital |
| 48 | Hospital Inpatient |
| 50 | Hospital Outpatient |
| 86 | Emergency Services |
| 88 | Pharmacy |
| 98 | Professional (Physician) |
| MH | Mental Health |
| UC | Urgent Care |

**Example Request:** "Check eligibility for hospital services"

### 271 - Eligibility Response

Response to eligibility inquiry.

**Response Types:**
| Code | Description |
|------|-------------|
| 1 | Active Coverage |
| 2 | Active - Full Risk Capitation |
| 3 | Active - Services Capitated |
| 4 | Active - Services Capitated to Primary Care |
| 5 | Active - Pending Investigation |
| 6 | Inactive |
| 7 | Inactive - Pending Eligibility Update |
| 8 | Inactive - Pending Investigation |

**Benefit Information Codes:**
| Code | Description |
|------|-------------|
| A | Co-Insurance |
| B | Co-Payment |
| C | Deductible |
| F | Limitations |
| G | Out of Pocket (Stop Loss) |
| I | Non-Covered |
| R | Other or Additional Payor |
| Y | Contact Following Entity |

## Plan Configurations

### HMO Plan
```json
{
  "plan_type": "HMO",
  "plan_code": "HMO-STD",
  "network_requirement": "in_network_only",
  "pcp_required": true,
  "referral_required": true,
  "benefits": {
    "individual_deductible": 0,
    "family_deductible": 0,
    "individual_oop_max": 3000,
    "family_oop_max": 6000,
    "pcp_copay": 20,
    "specialist_copay": 40,
    "er_copay": 150,
    "inpatient_copay": 250
  }
}
```

### PPO Plan
```json
{
  "plan_type": "PPO",
  "plan_code": "PPO-GOLD",
  "network_requirement": "in_network_preferred",
  "pcp_required": false,
  "referral_required": false,
  "benefits": {
    "in_network": {
      "individual_deductible": 500,
      "family_deductible": 1000,
      "individual_oop_max": 4000,
      "family_oop_max": 8000,
      "coinsurance": 20,
      "pcp_copay": 25,
      "specialist_copay": 50
    },
    "out_of_network": {
      "individual_deductible": 1500,
      "family_deductible": 3000,
      "individual_oop_max": 8000,
      "family_oop_max": 16000,
      "coinsurance": 40
    }
  }
}
```

### HDHP Plan
```json
{
  "plan_type": "HDHP",
  "plan_code": "HDHP-HSA",
  "network_requirement": "in_network_preferred",
  "hsa_eligible": true,
  "benefits": {
    "in_network": {
      "individual_deductible": 1600,
      "family_deductible": 3200,
      "individual_oop_max": 7000,
      "family_oop_max": 14000,
      "coinsurance": 20,
      "preventive_covered_at_100": true
    },
    "out_of_network": {
      "individual_deductible": 3200,
      "family_deductible": 6400,
      "individual_oop_max": 14000,
      "family_oop_max": 28000,
      "coinsurance": 40
    }
  },
  "hsa": {
    "employer_contribution": 500,
    "individual_max_contribution": 4150,
    "family_max_contribution": 8300
  }
}
```

## Examples

### Example 1: New Hire Enrollment

**Request:** "Generate a new hire enrollment for employee with family coverage"

```json
{
  "enrollment": {
    "transaction_type": "add",
    "effective_date": "2025-02-01",
    "enrollment_reason": "new_hire",
    "group": {
      "group_id": "GRP001234",
      "group_name": "Acme Corporation",
      "division": "DIV001"
    },
    "subscriber": {
      "member_id": "MEM001234567",
      "ssn": "123-45-6789",
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
      "email": "michael.johnson@email.com",
      "phone": "555-234-5678",
      "employment": {
        "hire_date": "2025-01-15",
        "status": "active",
        "hours_per_week": 40,
        "job_title": "Software Engineer"
      }
    },
    "dependents": [
      {
        "member_id": "MEM001234568",
        "relationship": "01",
        "name": {
          "given_name": "Sarah",
          "family_name": "Johnson"
        },
        "birth_date": "1987-07-22",
        "gender": "F",
        "ssn": "987-65-4321"
      },
      {
        "member_id": "MEM001234569",
        "relationship": "19",
        "name": {
          "given_name": "Emma",
          "family_name": "Johnson"
        },
        "birth_date": "2015-11-10",
        "gender": "F",
        "ssn": "456-78-9012"
      }
    ],
    "coverage": {
      "coverage_tier": "FAM",
      "plan_selections": [
        {
          "benefit_type": "medical",
          "plan_code": "PPO-GOLD",
          "coverage_start": "2025-02-01",
          "premium_amount": 850.00,
          "employer_contribution": 650.00,
          "employee_contribution": 200.00
        },
        {
          "benefit_type": "dental",
          "plan_code": "DENT-STD",
          "coverage_start": "2025-02-01",
          "premium_amount": 75.00,
          "employer_contribution": 50.00,
          "employee_contribution": 25.00
        },
        {
          "benefit_type": "vision",
          "plan_code": "VIS-BASIC",
          "coverage_start": "2025-02-01",
          "premium_amount": 20.00,
          "employer_contribution": 10.00,
          "employee_contribution": 10.00
        }
      ]
    }
  }
}
```

### Example 2: Qualifying Life Event (Birth)

**Request:** "Generate an enrollment change to add a newborn"

```json
{
  "enrollment": {
    "transaction_type": "change",
    "effective_date": "2025-01-20",
    "enrollment_reason": "qle",
    "qle_type": "birth",
    "qle_date": "2025-01-20",
    "subscriber": {
      "member_id": "MEM001234567",
      "name": {
        "given_name": "Michael",
        "family_name": "Johnson"
      }
    },
    "changes": {
      "coverage_tier": {
        "from": "ES",
        "to": "FAM"
      },
      "dependents_added": [
        {
          "member_id": "MEM001234570",
          "relationship": "19",
          "name": {
            "given_name": "William",
            "family_name": "Johnson"
          },
          "birth_date": "2025-01-20",
          "gender": "M",
          "ssn": "pending"
        }
      ],
      "premium_change": {
        "from": 650.00,
        "to": 850.00,
        "employee_contribution_change": 50.00
      }
    }
  }
}
```

### Example 3: Termination

**Request:** "Generate a termination for employment end"

```json
{
  "enrollment": {
    "transaction_type": "termination",
    "effective_date": "2025-01-31",
    "termination_reason": "voluntary_resignation",
    "last_day_worked": "2025-01-17",
    "subscriber": {
      "member_id": "MEM001234567",
      "name": {
        "given_name": "Michael",
        "family_name": "Johnson"
      }
    },
    "coverage_termination": {
      "medical": {
        "plan_code": "PPO-GOLD",
        "last_coverage_date": "2025-01-31"
      },
      "dental": {
        "plan_code": "DENT-STD",
        "last_coverage_date": "2025-01-31"
      },
      "vision": {
        "plan_code": "VIS-BASIC",
        "last_coverage_date": "2025-01-31"
      }
    },
    "cobra": {
      "eligible": true,
      "notification_date": "2025-02-14",
      "election_deadline": "2025-04-15",
      "available_coverage": ["medical", "dental", "vision"],
      "cobra_premium": {
        "medical": 867.00,
        "dental": 76.50,
        "vision": 20.40
      }
    },
    "dependents_terminated": [
      {
        "member_id": "MEM001234568",
        "relationship": "01",
        "last_coverage_date": "2025-01-31",
        "cobra_eligible": true
      },
      {
        "member_id": "MEM001234569",
        "relationship": "19",
        "last_coverage_date": "2025-01-31",
        "cobra_eligible": true
      }
    ]
  }
}
```

### Example 4: Eligibility Inquiry and Response

**Request:** "Check eligibility for a member for hospital services"

```json
{
  "inquiry": {
    "transaction_type": "270",
    "trace_number": "TRN20250115001",
    "inquiry_date": "2025-01-15",
    "service_date": "2025-01-20",
    "subscriber": {
      "member_id": "MEM001234567",
      "name": {
        "given_name": "Michael",
        "family_name": "Johnson"
      },
      "birth_date": "1985-03-15"
    },
    "provider": {
      "npi": "1234567890",
      "name": "Springfield General Hospital",
      "taxonomy": "282N00000X"
    },
    "service_types": ["30", "47", "48"]
  },
  "response": {
    "transaction_type": "271",
    "trace_number": "TRN20250115001",
    "response_date": "2025-01-15",
    "subscriber": {
      "member_id": "MEM001234567",
      "name": {
        "given_name": "Michael",
        "family_name": "Johnson"
      },
      "birth_date": "1985-03-15",
      "eligibility_status": "1",
      "eligibility_status_description": "Active Coverage"
    },
    "payer": {
      "payer_id": "BCBS001",
      "payer_name": "Blue Cross Blue Shield of Illinois"
    },
    "plan": {
      "plan_code": "PPO-GOLD",
      "plan_name": "PPO Gold Plan",
      "group_id": "GRP001234",
      "group_name": "Acme Corporation"
    },
    "coverage": {
      "coverage_start": "2025-02-01",
      "coverage_end": null
    },
    "benefits": {
      "hospital_inpatient": {
        "service_type": "48",
        "coverage_level": "IND",
        "in_network": {
          "deductible": {
            "amount": 500.00,
            "remaining": 175.00
          },
          "coinsurance": 20,
          "out_of_pocket": {
            "limit": 4000.00,
            "remaining": 3675.00
          },
          "prior_auth_required": true
        },
        "out_of_network": {
          "deductible": {
            "amount": 1500.00,
            "remaining": 1500.00
          },
          "coinsurance": 40,
          "out_of_pocket": {
            "limit": 8000.00,
            "remaining": 8000.00
          }
        }
      },
      "hospital_outpatient": {
        "service_type": "50",
        "coverage_level": "IND",
        "in_network": {
          "copay": 100.00,
          "deductible_applies": true,
          "prior_auth_required": false
        }
      }
    },
    "pcp": {
      "required": false,
      "assigned": null
    },
    "messages": [
      "Prior authorization required for inpatient admissions",
      "Contact member services for benefit questions: 1-800-555-1234"
    ]
  }
}
```

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| X12 834 | "as 834", "X12 enrollment" | Enrollment file submission |
| X12 270 | "as 270", "eligibility inquiry" | Eligibility request |
| X12 271 | "as 271", "eligibility response" | Eligibility response |
| CSV | "as CSV" | Bulk enrollment export |
| SQL | "as SQL" | Database loading |

## Validation Rules

### Enrollment
1. Subscriber SSN must be valid format
2. Dependent birth dates must be before enrollment
3. Coverage effective date must be >= enrollment submission date
4. Dependents must have valid relationship codes
5. Children must be under age limit (typically 26 for medical)
6. QLE enrollment must be within enrollment window

### Eligibility
1. Service date must be within coverage period
2. Member ID must match subscriber or dependent
3. Provider NPI must be valid 10-digit format
4. Service type codes must be valid

## Related Skills

### MemberSim
- [SKILL.md](SKILL.md) - MemberSim overview
- [professional-claims.md](professional-claims.md) - Professional claims
- [plan-benefits.md](plan-benefits.md) - Plan selection during enrollment
- [accumulator-tracking.md](accumulator-tracking.md) - Accumulator tracking

### Cross-Product: RxMemberSim
- [../rxmembersim/rx-enrollment.md](../rxmembersim/rx-enrollment.md) - Pharmacy benefit enrollment

> **Integration Pattern:** Medical enrollment (this skill) and pharmacy enrollment often occur together. Use MemberSim for medical coverage enrollment. Use RxMemberSim for pharmacy benefit setup (BIN, PCN, group number). Ensure coverage dates are synchronized.

### References
- [../../formats/x12-834.md](../../formats/x12-834.md) - X12 834 Enrollment format
- [../../formats/x12-270-271.md](../../formats/x12-270-271.md) - X12 270/271 Eligibility format
- [../../references/code-systems.md](../../references/code-systems.md) - Code systems
