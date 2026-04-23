---
name: behavioral-health-claims
description: "Behavioral health professional claims including psychotherapy, psychiatric evaluation, and SUD treatment. Triggers: behavioral health claim, mental health claim, psychotherapy, psychiatry billing, substance abuse, SUD, therapy session, PHP, IOP"
---

# Behavioral Health Claims Cohort

A cohort template for generating behavioral health professional claims including psychotherapy, psychiatric evaluation, and substance use disorder treatment.

## For Claude

Use this skill when the user requests behavioral health claims or mental health billing cohorts. This teaches you how to generate **realistic behavioral health claims** with appropriate CPT codes, session lengths, and provider types.

**When to apply this skill:**

- User mentions behavioral health claim or mental health claim
- User requests psychotherapy or psychiatry billing
- User specifies substance abuse or SUD claims
- User asks for therapy session claims
- User needs PHP/IOP claim examples

**Key capabilities this skill provides:**

- How to select appropriate psychotherapy CPT codes by time
- How to code psychiatric evaluations and medication management
- How to structure partial hospitalization and IOP claims
- How to handle telehealth behavioral health billing
- How to apply mental health parity requirements

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: MemberSim
- **Tags**: behavioral-health, mental-health, claims, payer, psychiatry
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic behavioral health professional claims. It models psychotherapy, psychiatric evaluation, medication management, and substance use treatment with appropriate coding and adjudication.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "behavioral health claim", "mental health claim"
- "psychotherapy claim", "psychiatry claim"
- "substance abuse claim", "SUD claim"
- "therapy claim", "counseling claim"

**Claim Cohorts**:

- "Generate a psychotherapy claim"
- "Create a psychiatric evaluation claim"
- "Generate an IOP claim for substance use"

## Trigger Phrases

- behavioral health claim
- mental health claim
- psychiatry claim
- psychotherapy claim
- substance abuse claim
- SUD claim
- depression claim
- anxiety claim
- therapy claim
- counseling claim
- PHP claim (partial hospitalization)
- IOP claim (intensive outpatient)

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| service_type | string | psychotherapy | psychiatric_eval, psychotherapy, medication_management, substance_abuse, PHP, IOP |
| provider_type | string | psychologist | psychiatrist, psychologist, LCSW, LPC, LMFT |
| session_length | int | 45 | 30, 45, 53, 60, 90 |
| diagnosis_category | string | depression | depression, anxiety, bipolar, PTSD, SUD, schizophrenia |
| place_of_service | string | 11 | 11 (office), 02 (telehealth), 52 (PHP), 53 (CMHC) |
| claim_status | string | paid | paid, denied, pending |
| network_status | string | in-network | in-network, out-of-network |

## Place of Service Codes (Behavioral Health)

| Code | Description | Typical Services |
|------|-------------|------------------|
| 02 | Telehealth | Virtual therapy, telepsychiatry |
| 11 | Office | In-person therapy and psychiatry |
| 21 | Inpatient Hospital | Psychiatric hospitalization |
| 52 | Psychiatric Facility (PHP) | Partial hospitalization program |
| 53 | Community Mental Health Center | CMHC services |
| 55 | Residential Substance Abuse | SUD residential treatment |
| 57 | Non-residential Substance Abuse | SUD outpatient (IOP) |

## Common Diagnosis Codes

### Depressive Disorders

| Code | Description |
|------|-------------|
| F32.0 | Major depressive disorder, single episode, mild |
| F32.1 | Major depressive disorder, single episode, moderate |
| F32.2 | Major depressive disorder, single episode, severe |
| F33.0 | Major depressive disorder, recurrent, mild |
| F33.1 | Major depressive disorder, recurrent, moderate |
| F33.2 | Major depressive disorder, recurrent, severe |
| F34.1 | Dysthymic disorder (Persistent depressive disorder) |

### Anxiety Disorders

| Code | Description |
|------|-------------|
| F41.0 | Panic disorder |
| F41.1 | Generalized anxiety disorder |
| F40.10 | Social anxiety disorder |
| F40.00 | Agoraphobia |
| F42.2 | Obsessive-compulsive disorder, mixed |
| F43.10 | Post-traumatic stress disorder |
| F43.12 | PTSD, chronic |

### Bipolar and Related Disorders

| Code | Description |
|------|-------------|
| F31.0 | Bipolar I, current episode hypomanic |
| F31.1x | Bipolar I, current episode manic |
| F31.3x | Bipolar I, current episode depressed |
| F31.81 | Bipolar II disorder |
| F34.0 | Cyclothymic disorder |

### Substance Use Disorders

| Code | Description |
|------|-------------|
| F10.10 | Alcohol use disorder, mild |
| F10.20 | Alcohol use disorder, moderate |
| F11.10 | Opioid use disorder, mild |
| F11.20 | Opioid use disorder, moderate |
| F12.10 | Cannabis use disorder, mild |
| F14.10 | Cocaine use disorder, mild |
| F15.10 | Stimulant use disorder, mild |

### Psychotic Disorders

| Code | Description |
|------|-------------|
| F20.0 | Paranoid schizophrenia |
| F20.1 | Disorganized schizophrenia |
| F20.9 | Schizophrenia, unspecified |
| F25.0 | Schizoaffective disorder, bipolar type |
| F25.1 | Schizoaffective disorder, depressive type |

## Common Procedure Codes

### Psychiatric Evaluation

| Code | Description | Charge Range | Typical Use |
|------|-------------|--------------|-------------|
| 90791 | Psychiatric diagnostic evaluation | $200-400 | Initial psychiatry assessment |
| 90792 | Psychiatric diagnostic eval with medical services | $250-450 | Initial eval with E&M |

### Psychotherapy

| Code | Description | Charge Range | Session Length |
|------|-------------|--------------|----------------|
| 90832 | Psychotherapy, 30 minutes | $75-125 | 16-37 minutes |
| 90834 | Psychotherapy, 45 minutes | $125-175 | 38-52 minutes |
| 90837 | Psychotherapy, 60 minutes | $150-225 | 53+ minutes |
| 90839 | Psychotherapy for crisis, first 60 min | $175-275 | Crisis intervention |
| 90840 | Psychotherapy for crisis, each add'l 30 min | $85-125 | Crisis add-on |

### Psychotherapy Add-on Codes

| Code | Description | Charge Range | Use With |
|------|-------------|--------------|----------|
| +90833 | Psychotherapy add-on, 30 min | $50-85 | E&M codes |
| +90836 | Psychotherapy add-on, 45 min | $75-125 | E&M codes |
| +90838 | Psychotherapy add-on, 60 min | $100-150 | E&M codes |

### Medication Management

| Code | Description | Charge Range | Typical Use |
|------|-------------|--------------|-------------|
| 99213 | Office visit, low complexity | $85-125 | Med check, stable |
| 99214 | Office visit, moderate complexity | $125-175 | Med adjustment |
| 99215 | Office visit, high complexity | $175-250 | Complex polypharmacy |

### Group Therapy

| Code | Description | Charge Range |
|------|-------------|--------------|
| 90853 | Group psychotherapy | $35-75 |

### Family Therapy

| Code | Description | Charge Range |
|------|-------------|--------------|
| 90846 | Family therapy without patient | $125-175 |
| 90847 | Family therapy with patient | $150-200 |

### Substance Abuse Services

| Code | Description | Charge Range |
|------|-------------|--------------|
| H0001 | Alcohol/drug assessment | $150-250 |
| H0004 | Behavioral health counseling, per 15 min | $25-50 |
| H0005 | Alcohol/drug group counseling, per 15 min | $15-30 |
| H0015 | Alcohol/drug intensive outpatient (IOP), per hour | $75-125 |
| H0020 | Alcohol/drug methadone administration | $15-25 |
| H2035 | Alcohol/drug treatment, per hour | $50-100 |

### Telehealth Modifiers

| Modifier | Description | Use |
|----------|-------------|-----|
| 95 | Synchronous telemedicine | Real-time video |
| GT | Via interactive audio/video | Telehealth service |

## Examples

### Example 1: Individual Psychotherapy Session

**Request:** "Generate a paid claim for a 45-minute therapy session for depression"

```json
{
  "claim": {
    "claim_id": "CLM20250115BH001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "provider_npi": "1234567890",
    "provider_specialty": "psychologist",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "F33.1",
    "diagnosis_description": "Major depressive disorder, recurrent, moderate",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "90834",
        "description": "Psychotherapy, 45 minutes",
        "charge_amount": 150.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 120.00,
    "copay": 30.00,
    "paid_amount": 90.00,
    "patient_responsibility": 30.00
  }
}
```

### Example 2: Psychiatry Visit with Psychotherapy

**Request:** "Generate a claim for psychiatry medication management with therapy"

```json
{
  "claim": {
    "claim_id": "CLM20250115BH002",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM005678",
    "provider_npi": "9876543210",
    "provider_specialty": "psychiatrist",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "F31.81",
    "diagnosis_description": "Bipolar II disorder",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "description": "Office visit, moderate complexity",
        "charge_amount": 175.00,
        "units": 1
      },
      {
        "line_number": 2,
        "procedure_code": "90836",
        "modifier": null,
        "description": "Psychotherapy add-on, 45 minutes",
        "charge_amount": 100.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 200.00,
    "copay": 50.00,
    "paid_amount": 150.00,
    "patient_responsibility": 50.00
  }
}
```

### Example 3: Telehealth Therapy Session

**Request:** "Generate a telehealth psychotherapy claim"

```json
{
  "claim": {
    "claim_id": "CLM20250115BH003",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM003456",
    "provider_npi": "1234567890",
    "provider_specialty": "LCSW",
    "service_date": "2025-01-15",
    "place_of_service": "02",
    "principal_diagnosis": "F41.1",
    "diagnosis_description": "Generalized anxiety disorder",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "90837",
        "modifiers": ["95"],
        "description": "Psychotherapy, 60 minutes (telehealth)",
        "charge_amount": 175.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 140.00,
    "copay": 25.00,
    "paid_amount": 115.00,
    "patient_responsibility": 25.00
  }
}
```

### Example 4: Substance Abuse IOP

**Request:** "Generate a claim for intensive outpatient substance abuse treatment"

```json
{
  "claim": {
    "claim_id": "CLM20250115BH004",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM007890",
    "provider_npi": "5678901234",
    "provider_specialty": "substance_abuse_facility",
    "service_date": "2025-01-15",
    "place_of_service": "57",
    "principal_diagnosis": "F10.20",
    "diagnosis_description": "Alcohol use disorder, moderate",
    "secondary_diagnoses": [
      { "code": "F32.1", "description": "Major depressive disorder, single episode, moderate" }
    ],
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "H0015",
        "description": "Intensive outpatient treatment",
        "charge_amount": 300.00,
        "units": 3,
        "unit_description": "3 hours"
      },
      {
        "line_number": 2,
        "procedure_code": "90853",
        "description": "Group psychotherapy",
        "charge_amount": 50.00,
        "units": 1
      }
    ]
  },
  "prior_auth": {
    "auth_number": "PA20250101-BH789",
    "status": "approved",
    "approved_sessions": 36,
    "approved_through": "2025-03-31"
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 280.00,
    "copay": 0.00,
    "coinsurance": 56.00,
    "paid_amount": 224.00,
    "patient_responsibility": 56.00
  }
}
```

### Example 5: Denied Claim (Session Limit)

**Request:** "Generate a denied behavioral health claim for exceeding visit limits"

```json
{
  "claim": {
    "claim_id": "CLM20250115BH005",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM009012",
    "provider_npi": "1234567890",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "F33.0",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "90834",
        "charge_amount": 150.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "denied",
    "denial_reason": "CO-119",
    "denial_message": "Benefit maximum for this time period or occurrence has been reached",
    "allowed_amount": 0.00,
    "paid_amount": 0.00,
    "sessions_used": 52,
    "session_limit": 52,
    "appeal_info": "Member may request medical necessity exception for additional sessions"
  }
}
```

## Parity Compliance Notes

Mental Health Parity and Addiction Equity Act (MHPAEA) requires:

- **Quantitative limits** (visit limits, copays) cannot be more restrictive than medical/surgical
- **Non-quantitative limits** (prior auth, step therapy) must be comparable
- **Network adequacy** standards must apply equally

Common parity-related denial review triggers:

- Visit limits lower than medical specialist visits
- Higher copays for behavioral health than medical specialists
- More restrictive prior auth requirements
- Different network access standards

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| Claim ID | Unique identifier | BH-2025-001234 |
| Service date | Valid date, not future | 2025-01-15 |
| CPT code | Valid BH CPT | 90834 (45-min therapy) |
| ICD-10 code | Valid mental health diagnosis | F32.1 (moderate depression) |
| Provider type | Licensed BH provider | Psychiatrist, LCSW, PhD |
| Provider NPI | 10-digit valid NPI | 1234567890 |
| Session duration | Minutes per CPT code | 45 min (90834), 60 min (90837) |
| Place of service | Valid POS code | 11 (office), 02 (telehealth) |

### Business Rules

- **E&M vs. Psychotherapy**: Psychiatrists may bill both E&M and therapy same day (add-on codes)
- **Telehealth Modifier**: Telehealth sessions require POS 02 and may need modifier 95
- **Parity Compliance**: Mental health benefits must be comparable to medical benefits
- **Carve-Out**: Some plans carve out BH to separate administrator (Magellan, Optum BH)
- **Session Limits**: Some plans limit annual therapy visits (e.g., 30/year)
- **Provider Restrictions**: Must see in-network provider or pre-authorize out-of-network
- **Inpatient Authorization**: BH inpatient stays typically require concurrent review
- **SUD Services**: Substance use treatment has specific codes and requirements

## Related Skills

### MemberSim Cohorts

- [SKILL.md](SKILL.md) - MemberSim overview
- [professional-claims.md](professional-claims.md) - General professional claims
- [prior-authorization.md](prior-authorization.md) - PA workflows for behavioral health

### Cross-Product: PatientSim

- [../patientsim/SKILL.md](../patientsim/SKILL.md) - Clinical patient generation
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - Psychiatric encounters and treatment
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Depression comorbidity with chronic illness
- [../patientsim/maternal-health.md](../patientsim/maternal-health.md) - Postpartum depression

> **Integration Pattern:** Use PatientSim for psychiatric encounters and clinical documentation. Use MemberSim behavioral-health for claims - ensure diagnosis codes and visit types align with PatientSim encounters.

### Cross-Product: RxMemberSim

- [../rxmembersim/retail-pharmacy.md](../rxmembersim/retail-pharmacy.md) - Antidepressant, anxiolytic fills
- [../rxmembersim/rx-prior-auth.md](../rxmembersim/rx-prior-auth.md) - PA for controlled substances, specialty psych meds

> **Integration Pattern:** Use PatientSim for medication orders. Use RxMemberSim for pharmacy fills - psychiatric medications often have refill restrictions (Schedule II-IV), quantity limits, and PA requirements for newer agents.

### References

- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10-CM codes
- [../../references/mental-health-reference.md](../../references/mental-health-reference.md) - Behavioral health reference data
