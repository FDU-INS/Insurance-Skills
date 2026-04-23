---
name: rx-prior-auth
description: "Pharmacy prior authorization requests including clinical PA, step therapy overrides, formulary exceptions, and ePA transactions. Triggers: pharmacy PA, prior authorization, step therapy, formulary exception, ePA, clinical criteria, PA denial, PA approval"
---

# Pharmacy Prior Authorization Cohort

A cohort template for generating pharmacy prior authorization requests including clinical PA, step therapy overrides, and formulary exceptions.

## For Claude

Use this skill when the user requests pharmacy prior authorization cohorts. This teaches you how to generate **realistic pharmacy PA workflows** with clinical criteria, ePA transactions, and decision outcomes.

**When to apply this skill:**

- User mentions pharmacy prior auth or rx PA
- User requests step therapy or formulary exception
- User specifies quantity limit override or age edit
- User asks for PA approval/denial examples
- User needs ePA transaction cohorts

**Key capabilities this skill provides:**

- How to structure pharmacy PA request transactions
- How to model clinical criteria for different drug types
- How to handle step therapy requirements
- How to generate ePA (electronic PA) workflows
- How to document PA decisions and overrides

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: RxMemberSim
- **Tags**: pharmacy, prior-auth, step-therapy, ePA, PBM
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic pharmacy prior authorization workflows. It models clinical PA, step therapy, formulary exceptions, and quantity limit overrides with appropriate clinical criteria and decision rationale.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "pharmacy prior auth", "rx prior auth"
- "drug prior auth", "medication PA"
- "step therapy", "formulary exception"
- "quantity limit override", "PA required"

**PA Cohorts**:

- "Generate a pharmacy PA request"
- "Create a step therapy override"
- "Generate a denied formulary exception"

## Trigger Phrases

- pharmacy prior auth
- rx prior auth
- drug prior auth
- medication PA
- step therapy
- step therapy override
- formulary exception
- quantity limit override
- non-formulary
- PA required
- PA rejected
- pharmacy authorization

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| pa_type | string | clinical_pa | formulary_exception, step_therapy_override, quantity_limit, age_edit, clinical_pa, specialty |
| decision | string | approved | approved, denied, pending, cancelled |
| urgency | string | standard | standard, urgent, expedited |
| drug_category | string | brand | generic, brand, specialty |
| outcome | string | approved | approved, denied, partial, pended |

## Pharmacy PA Workflow

### Request Lifecycle
```
1. Claim submitted, PA required (reject code 75)
   ↓
2. Pharmacy or prescriber initiates PA request
   ↓
3. Clinical review (criteria check)
   ↓
4. Decision: Approved / Denied / Pended
   ↓
5. If approved: Override code issued, claim resubmitted
   ↓
6. If denied: Appeal or therapeutic alternative
```

### Turnaround Times

| Urgency | Standard | Expedited |
|---------|----------|-----------|
| Standard | 72 hours | 24 hours |
| Medicare Part D | 72 hours | 24 hours |
| Commercial Urgent | 24 hours | Same day |

## PA Types

### Formulary Exception
Request to cover a non-formulary drug.

**When Required:**
- Drug not on plan formulary
- Brand requested when generic available
- Non-preferred drug without trying preferred alternative

**Approval Criteria:**
1. Medical necessity documentation
2. Failed/contraindicated formulary alternatives
3. Prescriber attestation

**Example Request:** "Generate a PA for non-formulary brand medication"

### Step Therapy Override
Request to skip required first-line therapy.

**When Required:**
- Drug requires trial of step 1 therapy first
- Patient new to therapy or new to plan
- Step therapy protocol not satisfied

**Approval Criteria:**
1. Previous trial of required drug(s)
2. Therapeutic failure documented
3. Contraindication to first-line agents
4. Clinical rationale for starting at advanced step

**Example Request:** "Generate a step therapy override for a biologic"

### Quantity Limit Override
Request to exceed plan quantity limits.

**When Required:**
- Quantity exceeds plan maximum
- Days supply exceeds limit
- Dosing schedule requires more units

**Approval Criteria:**
1. Prescriber-indicated dose
2. FDA-approved dosing within range
3. Clinical necessity for higher dose

**Example Request:** "Generate a quantity limit override for oxycodone"

### Age Edit Override
Request to bypass age restrictions.

**When Required:**
- Patient outside approved age range
- Pediatric patient needs adult formulation
- Geriatric restriction on specific medications

**Approval Criteria:**
1. Off-label use with clinical support
2. Specialist recommendation
3. No age-appropriate alternative

**Example Request:** "Generate an age edit override for pediatric patient"

### Clinical/Specialty PA
Full clinical review for high-cost or specialty drugs.

**When Required:**
- Specialty medications (biologics, oncology)
- High-cost medications
- Medications with serious safety concerns
- REMS program drugs

**Approval Criteria:**
1. Diagnosis confirmation
2. Clinical criteria met (lab values, prior therapies)
3. Prescriber specialty verification
4. Site of care requirements

**Example Request:** "Generate a specialty PA for adalimumab"

## PA Request Structure

### Request Data Elements
```json
{
  "pa_id": "RX-PA-2025-0001234",
  "request_date": "2025-01-15",
  "request_time": "10:30:00",
  "urgency": "standard",

  "member": {
    "member_id": "MEM001234567",
    "cardholder_id": "ABC123456789",
    "name": {
      "given_name": "Michael",
      "family_name": "Johnson"
    },
    "birth_date": "1985-03-15",
    "phone": "555-234-5678"
  },

  "rx_plan": {
    "bin": "003858",
    "pcn": "A4",
    "group_number": "RX1234",
    "rx_plan_code": "RX-COMMERCIAL-3TIER"
  },

  "prescriber": {
    "npi": "1234567890",
    "name": "Dr. Emily Chen",
    "specialty": "Rheumatology",
    "phone": "555-345-6789",
    "fax": "555-345-6790"
  },

  "medication": {
    "ndc": "00074437909",
    "drug_name": "Humira 40mg/0.4ml Pen",
    "quantity": 2,
    "days_supply": 28,
    "directions": "Inject 40mg subcutaneously every 2 weeks"
  },

  "pa_type": "specialty",
  "diagnosis": {
    "primary": {
      "code": "M05.79",
      "description": "Rheumatoid arthritis with rheumatoid factor of multiple sites"
    },
    "secondary": [
      {
        "code": "M06.00",
        "description": "Rheumatoid arthritis without rheumatoid factor, unspecified site"
      }
    ]
  },

  "clinical_information": {
    "duration_of_condition": "3 years",
    "previous_treatments": [
      {
        "drug_name": "Methotrexate",
        "dates": "2022-01 to 2024-06",
        "outcome": "Inadequate response, disease progression"
      },
      {
        "drug_name": "Sulfasalazine",
        "dates": "2023-03 to 2024-03",
        "outcome": "GI intolerance"
      }
    ],
    "lab_values": [
      {
        "test": "Rheumatoid Factor",
        "value": "85",
        "unit": "IU/mL",
        "date": "2024-12-01"
      },
      {
        "test": "CRP",
        "value": "2.8",
        "unit": "mg/dL",
        "date": "2024-12-01"
      },
      {
        "test": "ESR",
        "value": "42",
        "unit": "mm/hr",
        "date": "2024-12-01"
      }
    ],
    "supporting_documentation": [
      "Office notes from 2024-12-15",
      "Lab results from 2024-12-01",
      "X-ray report showing joint erosions"
    ]
  }
}
```

## Clinical Criteria Examples

### TNF Inhibitor (Humira, Enbrel, etc.)
```json
{
  "criteria_name": "TNF Inhibitor - Rheumatoid Arthritis",
  "approved_diagnoses": ["M05.x", "M06.x"],
  "requirements": [
    {
      "name": "diagnosis_confirmed",
      "description": "Diagnosis of rheumatoid arthritis",
      "required": true
    },
    {
      "name": "conventional_dmard_failure",
      "description": "Trial and failure of at least one conventional DMARD (methotrexate)",
      "required": true,
      "min_duration_weeks": 12
    },
    {
      "name": "no_active_infection",
      "description": "No active serious infection",
      "required": true
    },
    {
      "name": "negative_tb_test",
      "description": "Negative TB test or latent TB treatment completed",
      "required": true
    },
    {
      "name": "specialist_prescriber",
      "description": "Prescribed by rheumatologist",
      "required": true
    }
  ],
  "approval_duration_days": 365,
  "quantity_per_30_days": 2
}
```

### Step Therapy - PCSK9 Inhibitors
```json
{
  "criteria_name": "PCSK9 Inhibitor Step Therapy",
  "drugs": ["Repatha", "Praluent"],
  "approved_diagnoses": ["E78.0x", "E78.2", "I25.x"],
  "step_therapy_requirements": [
    {
      "step": 1,
      "drugs": ["atorvastatin 80mg", "rosuvastatin 40mg"],
      "min_duration_weeks": 12,
      "description": "Maximum tolerated statin"
    },
    {
      "step": 2,
      "drugs": ["ezetimibe 10mg"],
      "min_duration_weeks": 12,
      "description": "Statin + ezetimibe combination"
    }
  ],
  "override_criteria": [
    "Statin intolerance (documented myopathy)",
    "Homozygous familial hypercholesterolemia",
    "LDL-C remains >100 despite maximally tolerated therapy"
  ]
}
```

## PA Response Structure

### Approval Response
```json
{
  "pa_id": "RX-PA-2025-0001234",
  "status": "approved",
  "decision_date": "2025-01-17",
  "decision_time": "14:30:00",
  "reviewer": {
    "name": "Pharmacy Review Team",
    "credentials": "PharmD, RPh"
  },
  "approval_details": {
    "effective_date": "2025-01-17",
    "expiration_date": "2026-01-17",
    "override_code": "PA12345678",
    "approved_quantity": 2,
    "approved_days_supply": 28,
    "approved_fills": 12,
    "pharmacy_instructions": "Apply override code PA12345678 to claim submission"
  },
  "conditions": [
    "Must be dispensed by specialty pharmacy",
    "Renewal requires continued prescriber attestation"
  ],
  "messages": [
    "Prior authorization approved for 12 months",
    "CVS Specialty: 1-800-237-2767"
  ]
}
```

### Denial Response
```json
{
  "pa_id": "RX-PA-2025-0001235",
  "status": "denied",
  "decision_date": "2025-01-17",
  "decision_time": "16:45:00",
  "reviewer": {
    "name": "Dr. James Wilson",
    "credentials": "MD, Medical Director"
  },
  "denial_details": {
    "denial_reason_code": "STEP_THERAPY_NOT_MET",
    "denial_reason": "Step therapy requirements not satisfied",
    "clinical_rationale": "No documented trial of high-intensity statin prior to PCSK9 inhibitor request",
    "required_step_drugs": ["atorvastatin 80mg", "rosuvastatin 40mg"],
    "formulary_alternatives": [
      {
        "drug_name": "Atorvastatin 80mg",
        "tier": 1,
        "copay": "$10",
        "pa_required": false
      },
      {
        "drug_name": "Rosuvastatin 40mg",
        "tier": 1,
        "copay": "$10",
        "pa_required": false
      },
      {
        "drug_name": "Ezetimibe 10mg",
        "tier": 1,
        "copay": "$10",
        "pa_required": false
      }
    ]
  },
  "appeal_rights": {
    "standard_appeal_deadline": "2025-02-16",
    "expedited_appeal_available": true,
    "external_review_available": true,
    "appeal_contact": "PA Appeals Department, 1-800-555-0100"
  },
  "messages": [
    "Trial of high-intensity statin required before PCSK9 inhibitor coverage",
    "If statin intolerant, submit documentation of adverse reaction",
    "Expedited appeal available if clinically urgent"
  ]
}
```

### Pending Response
```json
{
  "pa_id": "RX-PA-2025-0001236",
  "status": "pending",
  "status_date": "2025-01-16",
  "pending_reason": "additional_information_required",
  "required_information": [
    {
      "item": "TB test results",
      "description": "Recent TB screening (within 6 months)",
      "urgent": true
    },
    {
      "item": "Lab results",
      "description": "CRP and ESR within last 30 days",
      "urgent": false
    },
    {
      "item": "Prior therapy documentation",
      "description": "Records showing methotrexate trial dates and outcome",
      "urgent": false
    }
  ],
  "response_deadline": "2025-01-23",
  "contact": {
    "phone": "1-800-555-0100",
    "fax": "1-800-555-0101",
    "portal": "https://provider.pbm.com/pa-portal"
  },
  "messages": [
    "Additional clinical information required",
    "Please respond by 2025-01-23 to avoid case closure",
    "Fax documentation with PA ID RX-PA-2025-0001236 clearly noted"
  ]
}
```

## Examples

### Example 1: Approved Step Therapy Override

**Request:** "Generate an approved step therapy override for Ozempic"

```json
{
  "pa_request": {
    "pa_id": "RX-PA-2025-0001237",
    "request_date": "2025-01-15",
    "urgency": "standard",
    "pa_type": "step_therapy_override",
    "member": {
      "member_id": "MEM001234567",
      "name": { "given_name": "Maria", "family_name": "Garcia" },
      "birth_date": "1975-08-22"
    },
    "medication": {
      "ndc": "00169413312",
      "drug_name": "Ozempic 2mg/1.5ml Pen",
      "quantity": 1,
      "days_supply": 28
    },
    "diagnosis": {
      "primary": { "code": "E11.9", "description": "Type 2 diabetes without complications" }
    },
    "clinical_information": {
      "previous_treatments": [
        {
          "drug_name": "Metformin 1000mg BID",
          "dates": "2020-01 to present",
          "outcome": "Currently on therapy"
        },
        {
          "drug_name": "Glipizide 10mg BID",
          "dates": "2022-06 to present",
          "outcome": "Added to regimen, A1C remains elevated"
        }
      ],
      "lab_values": [
        { "test": "HbA1c", "value": "9.2", "unit": "%", "date": "2025-01-10" }
      ],
      "clinical_notes": "Patient has failed dual oral therapy with A1C consistently above goal. GLP-1 RA indicated for glycemic control and cardiovascular benefit."
    }
  },
  "pa_response": {
    "pa_id": "RX-PA-2025-0001237",
    "status": "approved",
    "decision_date": "2025-01-17",
    "approval_details": {
      "effective_date": "2025-01-17",
      "expiration_date": "2026-01-17",
      "override_code": "PA98765432",
      "approved_quantity": 1,
      "approved_days_supply": 28,
      "approved_fills": 12
    },
    "messages": [
      "Step therapy override approved based on dual oral therapy failure",
      "Approval valid for 12 months with up to 12 fills"
    ]
  }
}
```

### Example 2: Denied Formulary Exception

**Request:** "Generate a denied formulary exception for brand medication"

```json
{
  "pa_request": {
    "pa_id": "RX-PA-2025-0001238",
    "request_date": "2025-01-15",
    "urgency": "standard",
    "pa_type": "formulary_exception",
    "member": {
      "member_id": "MEM001234568",
      "name": { "given_name": "John", "family_name": "Smith" },
      "birth_date": "1980-03-15"
    },
    "medication": {
      "ndc": "00071015340",
      "drug_name": "Lipitor 40mg Tablet",
      "quantity": 30,
      "days_supply": 30
    },
    "diagnosis": {
      "primary": { "code": "E78.0", "description": "Pure hypercholesterolemia" }
    },
    "clinical_information": {
      "clinical_notes": "Patient requests brand Lipitor due to preference"
    }
  },
  "pa_response": {
    "pa_id": "RX-PA-2025-0001238",
    "status": "denied",
    "decision_date": "2025-01-16",
    "denial_details": {
      "denial_reason_code": "THERAPEUTIC_EQUIVALENT_AVAILABLE",
      "denial_reason": "Generic therapeutic equivalent available",
      "clinical_rationale": "Atorvastatin (generic Lipitor) is therapeutically equivalent and available on formulary at Tier 1. Brand preference without documented medical necessity does not meet exception criteria.",
      "formulary_alternatives": [
        {
          "drug_name": "Atorvastatin 40mg",
          "tier": 1,
          "copay": "$10",
          "pa_required": false
        }
      ]
    },
    "appeal_rights": {
      "standard_appeal_deadline": "2025-02-15",
      "expedited_appeal_available": false,
      "appeal_contact": "PA Appeals Department, 1-800-555-0100"
    }
  }
}
```

### Example 3: Specialty PA with Quantity Limit

**Request:** "Generate a specialty PA for Humira with quantity limit"

```json
{
  "pa_request": {
    "pa_id": "RX-PA-2025-0001239",
    "request_date": "2025-01-15",
    "urgency": "standard",
    "pa_type": "specialty",
    "member": {
      "member_id": "MEM001234569",
      "name": { "given_name": "Jennifer", "family_name": "Williams" },
      "birth_date": "1970-05-10"
    },
    "medication": {
      "ndc": "00074437909",
      "drug_name": "Humira 40mg/0.4ml Pen",
      "quantity": 4,
      "days_supply": 28,
      "directions": "Inject 40mg subcutaneously weekly"
    },
    "diagnosis": {
      "primary": { "code": "L40.50", "description": "Arthropathic psoriasis, unspecified" }
    },
    "clinical_information": {
      "previous_treatments": [
        {
          "drug_name": "Methotrexate 25mg weekly",
          "dates": "2023-01 to 2024-09",
          "outcome": "Inadequate response"
        }
      ],
      "lab_values": [
        { "test": "TB QuantiFERON", "value": "Negative", "date": "2025-01-05" },
        { "test": "Hepatitis B Surface Antigen", "value": "Negative", "date": "2025-01-05" }
      ]
    }
  },
  "pa_response": {
    "pa_id": "RX-PA-2025-0001239",
    "status": "approved",
    "decision_date": "2025-01-18",
    "approval_details": {
      "effective_date": "2025-01-18",
      "expiration_date": "2026-01-18",
      "override_code": "PA55667788",
      "approved_quantity": 4,
      "approved_days_supply": 28,
      "approved_fills": 12,
      "quantity_limit_override": true
    },
    "specialty_requirements": {
      "specialty_pharmacy_required": true,
      "designated_pharmacy": "CVS Specialty",
      "pharmacy_phone": "1-800-237-2767",
      "patient_support_program": "Humira Complete"
    },
    "messages": [
      "Weekly dosing approved for psoriatic arthritis",
      "Must use CVS Specialty pharmacy",
      "Quantity limit override granted for 4 pens per 28 days"
    ]
  }
}
```

## Validation Rules

### Request Validation
1. NDC must be valid 11-digit format
2. Diagnosis codes must support requested medication
3. Prescriber NPI must be valid and active
4. Member must have active pharmacy coverage
5. Clinical documentation must be provided for specialty drugs

### Response Validation
1. Override codes must be unique
2. Expiration date cannot exceed 365 days for most drugs
3. Approved quantity must not exceed FDA max dosing
4. Appeal deadlines must meet regulatory requirements (72 hours Medicare Part D)

## Electronic Prior Authorization (ePA)

Electronic Prior Authorization (ePA) enables real-time digital PA transactions, replacing fax-based workflows.

### NCPDP SCRIPT Standard

```
Version: SCRIPT 2017071 (current)
Transaction Types:
  - PAInitiationRequest    # Start PA process
  - PAInitiationResponse   # Return questions
  - PARequest              # Submit answers
  - PAResponse             # Return decision
  - PAAppealRequest/Response
  - PACancelRequest/Response
```

### ePA Workflow

```
1. Prescriber sends Rx (NewRx)
   ↓
2. Pharmacy submits claim → Rejects: "PA Required" (75)
   ↓
3. Pharmacy sends PAInitiationRequest
   ↓
4. PBM returns PAInitiationResponse with questions
   ↓
5. Prescriber completes questions in EHR
   ↓
6. PARequest submitted with answers
   ↓
7. PBM processes, returns PAResponse
   ↓
8. If approved: PA number issued, claim resubmitted
```

### Real-Time Determination

```yaml
real_time_pa:
  auto_approval:
    response_time: "<30 seconds"
    eligibility:
      - Claims history shows prior use
      - Member has diagnosis on file
      - Step therapy already completed

  standard:
    response_time: "24-72 hours"
    requires: "Clinical pharmacist review"
```

### Question Set Structure

```yaml
question:
  id: "Q001"
  text: "Has the patient tried and failed metformin?"
  type: "boolean"
  required: true

question:
  id: "Q002"
  text: "What is the patient's current A1C?"
  type: "numeric"
  required: true
  validation:
    min: 4.0
    max: 20.0

question:
  id: "Q003"
  text: "Select all diagnoses that apply:"
  type: "multi_select"
  required: true
  options:
    - code: "E11.9"
      text: "Type 2 diabetes without complications"
    - code: "E11.65"
      text: "Type 2 diabetes with hyperglycemia"

# Conditional question
question:
  id: "Q004"
  text: "Why was metformin discontinued?"
  type: "single_select"
  required: true
  condition:
    question: "Q001"
    answer: true
  options:
    - "GI intolerance"
    - "Renal insufficiency"
    - "Lactic acidosis risk"
    - "Inadequate response"
```

### ePA Message Examples

**PAInitiationRequest:**
```xml
<PAInitiationRequest>
  <Patient>
    <MemberID>MEM001</MemberID>
    <DateOfBirth>1965-03-15</DateOfBirth>
  </Patient>
  <Drug>
    <NDC>00169413512</NDC>
    <DrugName>Ozempic</DrugName>
    <Quantity>1</Quantity>
    <DaysSupply>28</DaysSupply>
  </Drug>
  <Prescriber>
    <NPI>1234567890</NPI>
  </Prescriber>
</PAInitiationRequest>
```

**PAResponse (Approved):**
```xml
<PAResponse>
  <PARequestID>EPA-2024-001234</PARequestID>
  <Decision>APPROVED</Decision>
  <PANumber>PA-2024-567890</PANumber>
  <EffectiveDate>2024-01-15</EffectiveDate>
  <ExpirationDate>2024-07-15</ExpirationDate>
  <ApprovedQuantity>1</ApprovedQuantity>
</PAResponse>
```

### ePA Status Tracking

| Status | Description |
|--------|-------------|
| INITIATED | Request started, awaiting questions |
| PENDING_PRESCRIBER | Questions sent, awaiting answers |
| SUBMITTED | Answers received, under review |
| APPROVED | PA granted |
| DENIED | PA not granted |
| CANCELLED | Request withdrawn |
| APPEALED | Under appeal |

### ePA Performance Metrics

```yaml
epa_metrics:
  auto_approval_rate: "35-45%"
  avg_turnaround_time:
    auto: "<30 seconds"
    standard: "24-48 hours"
    complex: "48-72 hours"
  approval_rate: "75-85%"

comparison_to_fax:
  fax_turnaround: "3-5 days"
  epa_turnaround: "24-48 hours"
  improvement: "60-80% faster"
```

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| NCPDP P1/P2 | "as NCPDP PA" | PA transaction |
| NCPDP SCRIPT | "as ePA" | Electronic PA workflow |
| PDF | "PA letter" | Provider/member notification |
| CSV | "as CSV" | PA tracking report |

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| PA number | Unique identifier | PA-2025-001234 |
| Request date | Valid date, not future | 2025-01-15 |
| Decision date | On or after request date | 2025-01-17 |
| Decision | approved, denied, pending | "approved" |
| Approval duration | Months valid | 12 months |
| Drug NDC | Valid 11-digit NDC | 00074433906 |
| Diagnosis code | Valid ICD-10 | E11.9 (Type 2 diabetes) |
| Prescriber NPI | 10-digit valid NPI | 1234567890 |
| Clinical criteria | Boolean flags | prior_therapy_failed: true |

### Business Rules

- **Turnaround Time**: Standard PA 72 hours; urgent PA 24 hours
- **Clinical Criteria**: Drug-specific requirements (diagnosis, labs, prior therapies)
- **Step Therapy**: Requires documentation of trial/failure of required prior drugs
- **Formulary Exception**: Requires clinical justification for non-formulary drug
- **Approval Duration**: Typically 6-12 months; specialty drugs may be shorter
- **Appeal Process**: Denied PAs can be appealed with additional documentation
- **ePA Integration**: Electronic PA (NCPDP SCRIPT) enables real-time adjudication
- **Grandfathering**: Existing patients on drug may be auto-approved at renewal

## Related Skills

### RxMemberSim
- [SKILL.md](SKILL.md) - RxMemberSim overview
- [formulary-management.md](formulary-management.md) - Formulary and tier structure
- [specialty-pharmacy.md](specialty-pharmacy.md) - Specialty drug handling
- [dur-alerts.md](dur-alerts.md) - DUR and clinical edits

### Cross-Product: PatientSim
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - PA for GLP-1s, SGLT2i
- [../patientsim/oncology/README.md](../patientsim/oncology/README.md) - PA for oral oncolytics
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - PA for specialty psych meds

> **Integration Pattern:** Use PatientSim to establish clinical criteria for PA approval (diagnosis, lab values, prior therapies). Use RxMemberSim rx-prior-auth to model the PA workflow - criteria matching determines approval/denial.

### Cross-Product: MemberSim
- [../membersim/prior-authorization.md](../membersim/prior-authorization.md) - Medical benefit PA

> **Integration Pattern:** Pharmacy PA (this skill) covers drugs under pharmacy benefit. Medical PA (MemberSim) covers procedures and medical benefit drugs. Some treatments may require coordination between both.

### References
- [../../references/code-systems.md](../../references/code-systems.md) - Code systems
- [../../references/data-models.md](../../references/data-models.md) - Data models
