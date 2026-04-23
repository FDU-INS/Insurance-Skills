---
name: prior-authorization
description: "Prior authorization requests and decisions for medical services, procedures, and medications. Triggers: prior authorization, prior auth, PA, pre-certification, medical necessity, utilization management, UM, authorization approval, denial"
---

# Prior Authorization Cohort

A cohort template for generating prior authorization requests and decisions for medical services, procedures, and medications.

## For Claude

Use this skill when the user requests prior authorization or utilization management cohorts. This teaches you how to generate **realistic PA workflows** with clinical criteria, decision rationale, and appeal processes.

**When to apply this skill:**

- User mentions prior authorization, prior auth, or PA
- User requests pre-certification or medical necessity cohorts
- User specifies utilization management or UM
- User asks for authorization approval/denial examples
- User needs PA workflow documentation

**Key capabilities this skill provides:**

- How to structure PA requests with required clinical information
- How to apply medical necessity criteria for decisions
- How to model approval, denial, and pended cohorts
- How to handle urgent vs standard review timelines
- How to generate appeal and peer-to-peer review cohorts

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: MemberSim
- **Tags**: prior-auth, utilization-management, payer, authorization
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic prior authorization workflows. It models the complete PA lifecycle from request through decision, including clinical criteria evaluation, turnaround times, and appeal processes.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "prior authorization", "prior auth", "PA"
- "pre-certification", "pre-cert"
- "medical necessity", "utilization management"
- "authorization required"

**PA Cohorts**:

- "Generate a PA request for an MRI"
- "Create a denied prior authorization"
- "Generate an appeal for a PA denial"

## Trigger Phrases

- prior authorization
- prior auth
- PA
- pre-certification
- pre-cert
- pre-authorization
- authorization required
- medical necessity
- utilization management
- UM

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| service_type | string | procedure | procedure, imaging, inpatient, medication, dme |
| decision | string | approved | approved, denied, pended, partial |
| urgency | string | standard | urgent, standard |
| review_type | string | prospective | prospective, concurrent, retrospective |

## Prior Authorization Workflow

### Request Lifecycle
```
1. Provider submits PA request
   ↓
2. Initial screening (auto-approval criteria)
   ↓
3. Clinical review (if not auto-approved)
   ↓
4. Medical director review (if needed)
   ↓
5. Decision: Approved / Denied / Pended
   ↓
6. Notification to provider and member
   ↓
7. Appeal (if denied)
```

### Review Types

| Type | Timing | Use Case |
|------|--------|----------|
| Prospective | Before service | Elective procedures, imaging, specialty drugs |
| Concurrent | During service | Inpatient stay extensions, ongoing treatment |
| Retrospective | After service | Emergency, urgent situations |

## Services Requiring Authorization

### Common PA-Required Services
| Category | Examples | Typical Turnaround |
|----------|----------|-------------------|
| **Advanced Imaging** | MRI, CT, PET scan | 24-72 hours |
| **Surgical Procedures** | Joint replacement, spine surgery | 3-5 business days |
| **Inpatient Admission** | Elective admission, observation | 24 hours |
| **Specialty Drugs** | Biologics, oncology, specialty Rx | 3-5 business days |
| **DME** | Power wheelchairs, CPAP, prosthetics | 3-5 business days |
| **Outpatient Services** | PT/OT beyond initial eval, infusions | 24-72 hours |
| **Genetic Testing** | Hereditary cancer panels | 5-7 business days |

### Imaging Prior Auth
| CPT Range | Description | Common Dx Requiring Auth |
|-----------|-------------|-------------------------|
| 70551-70553 | MRI Brain | Headache, MS |
| 72141-72158 | MRI Spine | Back pain, radiculopathy |
| 73721-73723 | MRI Lower Extremity | Joint pain |
| 71250-71275 | CT Chest | Pulmonary nodule |
| 74176-74178 | CT Abdomen/Pelvis | Abdominal pain |
| 78814-78816 | PET Scan | Cancer staging |

## PA Request Structure

### Request Data Elements
```json
{
  "auth_request_id": "PA{YYYYMMDD}{sequence:06d}",
  "request_date": "YYYY-MM-DD",
  "urgency": "standard | urgent",
  "review_type": "prospective | concurrent | retrospective",

  "member": {
    "member_id": "string",
    "name": "string",
    "birth_date": "YYYY-MM-DD",
    "plan_code": "string"
  },

  "requesting_provider": {
    "npi": "10-digit NPI",
    "name": "string",
    "phone": "string",
    "fax": "string"
  },

  "servicing_provider": {
    "npi": "10-digit NPI",
    "name": "string",
    "facility_name": "string (if applicable)"
  },

  "service_requested": {
    "service_type": "procedure | imaging | inpatient | medication | dme",
    "procedure_codes": ["CPT/HCPCS codes"],
    "diagnosis_codes": ["ICD-10 codes"],
    "place_of_service": "POS code",
    "quantity": 1,
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  },

  "clinical_information": {
    "clinical_notes": "string",
    "supporting_documentation": ["list of attachments"],
    "previous_treatments": ["string"],
    "lab_results": ["relevant labs"]
  }
}
```

## Decision Criteria

### Auto-Approval Criteria
```json
{
  "criteria": [
    {
      "name": "gold_card_provider",
      "description": "Provider has >90% approval rate",
      "action": "auto_approve"
    },
    {
      "name": "meets_clinical_guidelines",
      "description": "Request matches clinical pathway criteria",
      "action": "auto_approve"
    },
    {
      "name": "emergency_admission",
      "description": "Emergency inpatient admission",
      "action": "auto_approve_3_days"
    }
  ]
}
```

### Medical Necessity Criteria (InterQual/MCG Style)
```json
{
  "imaging_criteria": {
    "mri_lumbar_spine": {
      "approved_if": [
        "Conservative treatment failed x 6 weeks",
        "Progressive neurological deficit",
        "Suspected spinal infection or tumor",
        "Post-surgical evaluation",
        "Cauda equina symptoms"
      ],
      "denied_if": [
        "Initial evaluation of uncomplicated back pain",
        "No prior conservative treatment",
        "Duplicate imaging within 12 months"
      ]
    }
  }
}
```

## PA Response Structure

### Approved Response
```json
{
  "auth_response_id": "PAR{YYYYMMDD}{sequence:06d}",
  "auth_request_id": "PA20250115000001",
  "decision": "approved",
  "decision_date": "2025-01-17",
  "authorization_number": "AUTH20250117000001",

  "approved_services": {
    "procedure_codes": ["72148"],
    "quantity_approved": 1,
    "effective_date": "2025-01-17",
    "expiration_date": "2025-04-17",
    "place_of_service": "22"
  },

  "servicing_provider": {
    "npi": "1234567890",
    "name": "Springfield Imaging Center"
  },

  "notes": "Approved for MRI lumbar spine without contrast. Valid for 90 days.",

  "reviewer": {
    "type": "clinical_reviewer",
    "name": "Jane Smith, RN"
  }
}
```

### Denied Response
```json
{
  "auth_response_id": "PAR20250115000002",
  "auth_request_id": "PA20250115000002",
  "decision": "denied",
  "decision_date": "2025-01-17",

  "denial_reason": {
    "code": "MN-001",
    "description": "Does not meet medical necessity criteria",
    "clinical_rationale": "Conservative treatment not attempted for minimum 6 weeks. No evidence of progressive neurological deficit or red flag symptoms."
  },

  "reviewer": {
    "type": "medical_director",
    "name": "Dr. Robert Johnson, MD"
  },

  "appeal_rights": {
    "can_appeal": true,
    "appeal_deadline": "2025-02-16",
    "appeal_instructions": "Submit written appeal with additional clinical documentation within 30 days.",
    "peer_to_peer_available": true
  },

  "alternative_recommendations": [
    "Complete 6 weeks of physical therapy",
    "Trial of NSAIDs if not contraindicated",
    "X-ray of lumbar spine if not already performed"
  ]
}
```

### Pended Response (Additional Info Needed)
```json
{
  "auth_response_id": "PAR20250115000003",
  "auth_request_id": "PA20250115000003",
  "decision": "pended",
  "decision_date": "2025-01-16",

  "pend_reason": {
    "code": "INFO-001",
    "description": "Additional clinical information required"
  },

  "information_requested": [
    "Physical therapy notes from past 6 weeks",
    "Recent lab results (if applicable)",
    "Previous imaging reports"
  ],

  "response_deadline": "2025-01-26",
  "auto_denial_warning": "Request will be denied if information not received by deadline."
}
```

## Turnaround Time Requirements

| Urgency | Decision Deadline | Notification Deadline |
|---------|-------------------|----------------------|
| Urgent (pre-service) | 24 hours | 24 hours |
| Standard (pre-service) | 3 business days | 3 business days |
| Concurrent | 1 business day | 1 business day |
| Retrospective | 30 calendar days | 30 calendar days |

## Examples

### Example 1: MRI Prior Auth - Approved

```json
{
  "request": {
    "auth_request_id": "PA20250115000001",
    "request_date": "2025-01-15",
    "urgency": "standard",
    "review_type": "prospective",
    "member": {
      "member_id": "MEM001234",
      "name": { "given_name": "David", "family_name": "Miller" },
      "birth_date": "1975-04-18",
      "plan_code": "PPO-GOLD"
    },
    "requesting_provider": {
      "npi": "1234567890",
      "name": "Dr. Sarah Williams",
      "specialty": "Orthopedic Surgery"
    },
    "service_requested": {
      "service_type": "imaging",
      "procedure_codes": ["72148"],
      "procedure_description": "MRI lumbar spine without contrast",
      "diagnosis_codes": ["M54.5", "M54.16"],
      "diagnosis_description": ["Low back pain", "Lumbar radiculopathy"],
      "place_of_service": "22",
      "quantity": 1
    },
    "clinical_information": {
      "clinical_notes": "Patient with 8 weeks of low back pain radiating to left leg. Failed 6 weeks of PT. Taking NSAIDs with partial relief. No red flag symptoms.",
      "previous_treatments": ["Physical therapy x 6 weeks", "NSAID trial"],
      "imaging_history": "X-ray lumbar spine 2024-11-15: mild degenerative changes"
    }
  },
  "response": {
    "auth_response_id": "PAR20250115000001",
    "decision": "approved",
    "decision_date": "2025-01-16",
    "authorization_number": "AUTH20250116001234",
    "approved_services": {
      "procedure_codes": ["72148"],
      "quantity_approved": 1,
      "effective_date": "2025-01-16",
      "expiration_date": "2025-04-16"
    },
    "notes": "Approved. Patient meets criteria: failed conservative treatment x 6 weeks with radicular symptoms.",
    "reviewer": {
      "type": "clinical_reviewer",
      "credentials": "RN"
    }
  }
}
```

### Example 2: Inpatient Surgery - Approved with Conditions

```json
{
  "request": {
    "auth_request_id": "PA20250115000002",
    "request_date": "2025-01-15",
    "urgency": "standard",
    "review_type": "prospective",
    "member": {
      "member_id": "MEM005678",
      "name": { "given_name": "Patricia", "family_name": "Anderson" }
    },
    "service_requested": {
      "service_type": "inpatient",
      "procedure_codes": ["27447"],
      "procedure_description": "Total knee arthroplasty",
      "diagnosis_codes": ["M17.11"],
      "diagnosis_description": ["Primary osteoarthritis, right knee"],
      "facility_npi": "1122334455",
      "facility_name": "Springfield Orthopedic Hospital",
      "requested_los": 3
    }
  },
  "response": {
    "auth_response_id": "PAR20250115000002",
    "decision": "approved",
    "decision_date": "2025-01-17",
    "authorization_number": "AUTH20250117005678",
    "approved_services": {
      "procedure_codes": ["27447"],
      "approved_los": 2,
      "effective_date": "2025-02-01",
      "expiration_date": "2025-03-01"
    },
    "conditions": [
      "Approved for 2 days inpatient. Extension requires concurrent review.",
      "Pre-surgical clearance required before admission."
    ],
    "notes": "Approved for TKA with 2 day LOS per clinical guidelines. Day 3+ requires concurrent review for medical necessity."
  }
}
```

### Example 3: Specialty Medication - Denied (Step Therapy)

```json
{
  "request": {
    "auth_request_id": "PA20250115000003",
    "request_date": "2025-01-15",
    "service_requested": {
      "service_type": "medication",
      "drug_name": "Humira",
      "ndc": "00074433906",
      "diagnosis_codes": ["M05.79"],
      "diagnosis_description": ["Rheumatoid arthritis"],
      "quantity": 2,
      "days_supply": 28
    }
  },
  "response": {
    "auth_response_id": "PAR20250115000003",
    "decision": "denied",
    "decision_date": "2025-01-17",
    "denial_reason": {
      "code": "ST-001",
      "description": "Step therapy requirement not met",
      "clinical_rationale": "Patient has not tried required first-line therapy. Plan requires trial of methotrexate or other conventional DMARD for minimum 12 weeks before biologic approval."
    },
    "step_therapy_requirements": {
      "required_drugs": ["Methotrexate", "Sulfasalazine", "Hydroxychloroquine"],
      "minimum_trial_duration": "12 weeks",
      "failure_criteria": "Inadequate response or documented intolerance"
    },
    "appeal_rights": {
      "can_appeal": true,
      "appeal_deadline": "2025-02-16",
      "exception_criteria": "Medical contraindication to first-line agents, or previous trial documentation from prior plan"
    }
  }
}
```

## Integration with Claims

When a claim is submitted:
1. System checks if PA is required for procedure/diagnosis combination
2. If required, verify valid authorization exists
3. Match authorization number, dates, and approved services
4. Deny claim if no valid PA or PA expired

```json
{
  "claim_pa_validation": {
    "claim_id": "CLM20250115000001",
    "procedure_code": "72148",
    "service_date": "2025-01-20",
    "pa_check": {
      "pa_required": true,
      "authorization_number": "AUTH20250116001234",
      "auth_status": "valid",
      "auth_effective_date": "2025-01-16",
      "auth_expiration_date": "2025-04-16",
      "validation_result": "PASS"
    }
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Auth number | Unique identifier | AUTH-2025-001234 |
| Request date | Valid date, not future | 2025-01-10 |
| Decision date | On or after request date | 2025-01-12 |
| Status | pending, approved, denied, expired | "approved" |
| Service code | Valid CPT/HCPCS | 27447 (total knee) |
| Diagnosis code | Valid ICD-10 | M17.11 (knee OA) |
| Provider NPI | 10-digit valid NPI | 1234567890 |
| Approval duration | Valid date range | 90 days |
| Units approved | Positive integer | 1 |

### Business Rules

- **Turnaround Time**: Standard 5-15 business days; urgent 24-72 hours
- **Clinical Criteria**: Service-specific requirements (e.g., BMI, conservative treatment)
- **Medical Necessity**: Must document why service is required
- **Retro Authorization**: Emergency services may be authorized after the fact
- **Peer-to-Peer**: Provider can request clinical review with payer MD on denial
- **Appeal Rights**: Denials can be appealed; timeline varies by payer
- **Auth Validity**: Approvals expire; service must occur within validity period
- **Units vs. Duration**: Some PAs approve specific units; others approve time period

## Related Skills

### MemberSim
- [SKILL.md](SKILL.md) - MemberSim overview
- [professional-claims.md](professional-claims.md) - Claims requiring PA
- [facility-claims.md](facility-claims.md) - Inpatient PA

### Cross-Product: PatientSim
- [../patientsim/elective-joint.md](../patientsim/elective-joint.md) - Elective surgery requiring PA
- [../patientsim/oncology/README.md](../patientsim/oncology/README.md) - Oncology treatment PA

> **Integration Pattern:** Use PatientSim to identify procedures requiring authorization. Use MemberSim to model the PA workflow - submission, review, approval/denial, then claim with auth number.

### Cross-Product: RxMemberSim
- [../rxmembersim/rx-prior-auth.md](../rxmembersim/rx-prior-auth.md) - Pharmacy prior authorization

> **Integration Pattern:** Medical PA (this skill) covers procedures and services. Pharmacy PA (RxMemberSim) covers drug-specific authorizations. Some treatments require both - e.g., infused biologics may need medical PA while oral specialty drugs need pharmacy PA.

### References
- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
