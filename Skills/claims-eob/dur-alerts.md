---
name: dur-alerts
description: "Drug Utilization Review alerts including drug interactions, therapeutic duplication, early refill rejections, and clinical edits. Triggers: DUR, drug interaction, DDI, therapeutic duplication, early refill, clinical alert, drug-drug interaction, contraindication"
---

# Drug Utilization Review (DUR) Alerts Cohort

A cohort template for generating DUR alerts including drug interactions, therapeutic duplication, and early refill rejections.

## For Claude

Use this skill when the user requests DUR alert or drug interaction cohorts. This teaches you how to generate **realistic clinical edit alerts** with appropriate severity levels and pharmacist responses.

**When to apply this skill:**

- User mentions DUR or drug utilization review
- User requests drug interaction or duplication cohorts
- User specifies early refill or refill too soon
- User asks for clinical alert examples
- User needs prospective DUR cohorts

**Key capabilities this skill provides:**

- How to structure DUR alert codes and messages
- How to model drug-drug interaction severity levels
- How to handle pharmacist professional service codes
- How to generate override and rejection cohorts
- How to document result of service codes

## Metadata

- **Type**: cohort-template
- **Version**: 1.0
- **Author**: RxMemberSim
- **Tags**: pharmacy, DUR, drug-interaction, clinical-edit, PBM
- **Updated**: 2025-01-15

## Purpose

This cohort generates realistic drug utilization review alerts. It models prospective DUR checks including drug interactions, therapeutic duplication, dose alerts, and pharmacist intervention documentation.

## When to Use This Skill

Apply this skill when the user's request involves:

**Direct Keywords**:

- "DUR", "drug utilization review"
- "drug interaction", "drug-drug interaction"
- "therapeutic duplication", "early refill"
- "high dose", "contraindication"

**DUR Cohorts**:

- "Generate a drug interaction alert"
- "Create an early refill rejection"
- "Generate a DUR override cohort"

## Trigger Phrases

- DUR
- drug utilization review
- drug interaction
- drug-drug interaction
- therapeutic duplication
- early refill
- refill too soon
- high dose
- contraindication
- clinical alert
- prospective DUR

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| alert_type | string | DD | DD, TD, ER, HD, LD, DA, DG, DC |
| severity | string | moderate | major, moderate, minor |
| outcome | string | warning | warning, reject, override_required |
| professional_service | string | M0 | M0 (not reviewed), P0 (reviewed) |
| result_of_service | string | 1A | 1A (filled), 1B (not filled), 1C (modified) |

## DUR Alert Types

### Alert Type Reference
| Code | Type | Description | Typical Severity |
|------|------|-------------|------------------|
| DD | Drug-Drug Interaction | Interaction between two medications | Major/Moderate |
| TD | Therapeutic Duplication | Same therapeutic class | Moderate |
| ER | Early Refill | Refill before 80% supply used | Minor |
| HD | High Dose | Exceeds recommended maximum | Major |
| LD | Low Dose | Below therapeutic threshold | Minor |
| DA | Drug-Age | Age precaution | Moderate |
| DG | Drug-Gender | Gender precaution | Moderate |
| DC | Drug-Disease | Contraindicated condition | Major |
| MX | Maximum Therapy Duration | Exceeds max therapy days | Moderate |
| PG | Drug-Pregnancy | Pregnancy contraindication | Major |
| LR | Lactation Risk | Breastfeeding precaution | Moderate |

### Clinical Significance Codes
| Code | Level | Description | Action |
|------|-------|-------------|--------|
| 1 | Major | Life-threatening or permanent harm | Reject or requires override |
| 2 | Moderate | Significant but manageable | Warning, recommend review |
| 3 | Minor | Minimal clinical concern | Informational |

## Drug-Drug Interactions (DD)

### Major Interactions (Severity 1)
```json
{
  "major_interactions": [
    {
      "drug1_gpi_prefix": "8330",
      "drug1_class": "Warfarin",
      "drug2_gpi_prefix": "6610",
      "drug2_class": "NSAIDs",
      "severity": 1,
      "effect": "Increased bleeding risk",
      "mechanism": "NSAID inhibits platelet function and may displace warfarin from protein binding",
      "recommendation": "Avoid combination. If necessary, monitor INR closely and watch for bleeding.",
      "examples": {
        "drug1": ["Warfarin 5mg", "Coumadin 5mg"],
        "drug2": ["Ibuprofen 800mg", "Naproxen 500mg"]
      }
    },
    {
      "drug1_gpi_prefix": "6505",
      "drug1_class": "Opioids",
      "drug2_gpi_prefix": "5710",
      "drug2_class": "Benzodiazepines",
      "severity": 1,
      "effect": "CNS and respiratory depression - risk of death",
      "mechanism": "Additive CNS depressant effects",
      "recommendation": "Avoid concurrent use. FDA boxed warning.",
      "examples": {
        "drug1": ["Oxycodone 10mg", "Hydrocodone 10mg"],
        "drug2": ["Alprazolam 1mg", "Diazepam 5mg"]
      }
    },
    {
      "drug1_gpi_prefix": "3610",
      "drug1_class": "ACE Inhibitors",
      "drug2_gpi_prefix": "3620",
      "drug2_class": "ARBs",
      "severity": 1,
      "effect": "Hyperkalemia and acute kidney injury",
      "mechanism": "Dual RAAS blockade",
      "recommendation": "Avoid concurrent use.",
      "examples": {
        "drug1": ["Lisinopril 20mg", "Enalapril 10mg"],
        "drug2": ["Losartan 100mg", "Valsartan 160mg"]
      }
    }
  ]
}
```

### Moderate Interactions (Severity 2)
```json
{
  "moderate_interactions": [
    {
      "drug1_gpi_prefix": "3940",
      "drug1_class": "Statins",
      "drug2_gpi_prefix": "2130",
      "drug2_class": "Macrolide Antibiotics",
      "severity": 2,
      "effect": "Increased statin levels - myopathy risk",
      "mechanism": "CYP3A4 inhibition",
      "recommendation": "Monitor for muscle pain. Consider temporary statin hold.",
      "examples": {
        "drug1": ["Simvastatin 40mg", "Atorvastatin 80mg"],
        "drug2": ["Clarithromycin 500mg", "Erythromycin 500mg"]
      }
    },
    {
      "drug1_gpi_prefix": "5816",
      "drug1_class": "SSRIs",
      "drug2_gpi_prefix": "6120",
      "drug2_class": "Triptans",
      "severity": 2,
      "effect": "Serotonin syndrome risk",
      "mechanism": "Additive serotonergic effects",
      "recommendation": "Use with caution. Educate patient on symptoms.",
      "examples": {
        "drug1": ["Sertraline 100mg", "Fluoxetine 40mg"],
        "drug2": ["Sumatriptan 100mg", "Rizatriptan 10mg"]
      }
    }
  ]
}
```

## Therapeutic Duplication (TD)

### Same Drug Class
```json
{
  "therapeutic_duplication": [
    {
      "class_gpi": "3940",
      "class_name": "HMG-CoA Reductase Inhibitors (Statins)",
      "max_concurrent": 1,
      "severity": 2,
      "message": "Multiple statins on profile",
      "examples": [
        "Atorvastatin 40mg + Rosuvastatin 20mg",
        "Simvastatin 20mg + Pravastatin 40mg"
      ]
    },
    {
      "class_gpi": "4940",
      "class_name": "Proton Pump Inhibitors",
      "max_concurrent": 1,
      "severity": 2,
      "message": "Multiple PPIs on profile",
      "examples": [
        "Omeprazole 40mg + Pantoprazole 40mg"
      ]
    },
    {
      "class_gpi": "5816",
      "class_name": "SSRIs",
      "max_concurrent": 1,
      "severity": 2,
      "message": "Multiple SSRIs on profile",
      "examples": [
        "Sertraline 100mg + Escitalopram 20mg"
      ]
    },
    {
      "class_gpi": "6625",
      "class_name": "TNF Inhibitors",
      "max_concurrent": 1,
      "severity": 1,
      "message": "Multiple biologics on profile - infection risk",
      "examples": [
        "Humira + Enbrel"
      ]
    }
  ]
}
```

## Early Refill (ER)

### Refill Policy
```json
{
  "early_refill_rules": {
    "standard_threshold": 0.80,
    "threshold_description": "Refill allowed when 80% of supply used",
    "controlled_substance_threshold": 0.90,
    "calculation": {
      "days_elapsed": "service_date - previous_fill_date",
      "percent_used": "days_elapsed / previous_days_supply",
      "earliest_fill": "previous_fill_date + (previous_days_supply * 0.80)"
    }
  }
}
```

### Early Refill Cohorts
```json
{
  "cohorts": [
    {
      "cohort": "maintenance_medication",
      "previous_fill": "2025-01-01",
      "days_supply": 30,
      "attempt_date": "2025-01-22",
      "days_elapsed": 21,
      "percent_used": 0.70,
      "threshold": 0.80,
      "result": "rejected",
      "reject_code": "79",
      "earliest_fill_date": "2025-01-25",
      "message": "Refill too soon. 70% of supply used. Eligible on 01/25/2025."
    },
    {
      "cohort": "vacation_override",
      "previous_fill": "2025-01-01",
      "days_supply": 30,
      "attempt_date": "2025-01-20",
      "override_reason": "vacation_supply",
      "result": "approved_with_override",
      "professional_service_code": "P0",
      "result_of_service_code": "1A"
    }
  ]
}
```

## High/Low Dose Alerts (HD/LD)

### Maximum Daily Dose
```json
{
  "dose_alerts": [
    {
      "drug": "Metformin",
      "gpi": "2710004000",
      "max_daily_dose_mg": 2550,
      "typical_dose": "500-2000 mg/day",
      "alert_type": "HD",
      "severity": 2,
      "example_trigger": "Metformin 1000mg TID = 3000mg/day"
    },
    {
      "drug": "Gabapentin",
      "gpi": "7210002000",
      "max_daily_dose_mg": 3600,
      "typical_dose": "300-1800 mg/day",
      "alert_type": "HD",
      "severity": 2,
      "renal_adjustment_required": true
    },
    {
      "drug": "Lisinopril",
      "gpi": "3615001500",
      "max_daily_dose_mg": 80,
      "typical_dose": "10-40 mg/day",
      "alert_type": "HD",
      "severity": 2
    }
  ]
}
```

## Age-Related Alerts (DA)

### Pediatric Restrictions
```json
{
  "pediatric_alerts": [
    {
      "drug": "Ciprofloxacin",
      "gpi": "0420100000",
      "min_age": 18,
      "alert_type": "DA",
      "severity": 2,
      "reason": "Risk of tendon and cartilage damage in pediatric patients",
      "exception": "Certain serious infections where benefits outweigh risks"
    },
    {
      "drug": "CNS Stimulants",
      "gpi_prefix": "6510",
      "min_age": 6,
      "alert_type": "DA",
      "severity": 2,
      "reason": "Not recommended under age 6"
    }
  ]
}
```

### Geriatric Cautions (Beers Criteria)
```json
{
  "geriatric_alerts": [
    {
      "drug_class": "First-Generation Antihistamines",
      "gpi_prefix": "1210",
      "max_age": null,
      "min_age_for_caution": 65,
      "alert_type": "DA",
      "severity": 2,
      "reason": "Beers Criteria - anticholinergic effects, cognitive impairment",
      "examples": ["Diphenhydramine", "Chlorpheniramine"]
    },
    {
      "drug_class": "Benzodiazepines",
      "gpi_prefix": "5710",
      "min_age_for_caution": 65,
      "alert_type": "DA",
      "severity": 2,
      "reason": "Beers Criteria - fall risk, cognitive impairment"
    },
    {
      "drug_class": "Long-acting Sulfonylureas",
      "drug": "Glimepiride",
      "gpi": "2723001500",
      "min_age_for_caution": 65,
      "alert_type": "DA",
      "severity": 2,
      "reason": "Hypoglycemia risk in elderly"
    }
  ]
}
```

## DUR Response Codes

### Professional Service Codes
| Code | Description |
|------|-------------|
| 00 | No intervention |
| M0 | Prescriber consulted |
| P0 | Patient consulted |
| R0 | Pharmacist consulted other source |
| CC | Coordination of care |

### Result of Service Codes
| Code | Description |
|------|-------------|
| 1A | Filled as prescribed |
| 1B | Not filled - prescriber contacted |
| 1C | Filled with different dose |
| 1D | Filled with different directions |
| 1E | Filled with different drug |
| 1F | Rx not filled |
| 1G | Drug therapy unchanged |

## Examples

### Example 1: Major Drug Interaction - Reject

```json
{
  "claim": {
    "claim_id": "RX20250115000001",
    "ndc": "00093014801",
    "drug_name": "Oxycodone 10mg Tablet",
    "quantity_dispensed": 60,
    "days_supply": 30
  },
  "member_profile": {
    "member_id": "MEM001234",
    "current_medications": [
      {
        "ndc": "00093505910",
        "drug_name": "Alprazolam 1mg",
        "last_fill_date": "2025-01-05",
        "days_supply": 30
      }
    ]
  },
  "response": {
    "status": "rejected",
    "reject_code": "88",
    "reject_message": "DUR Reject Error"
  },
  "dur_alert": {
    "alert_id": "DUR20250115000001",
    "alert_type": "DD",
    "alert_description": "Drug-Drug Interaction",
    "severity": 1,
    "severity_description": "Major - Life-threatening",
    "conflicting_drug": {
      "ndc": "00093505910",
      "drug_name": "Alprazolam 1mg",
      "fill_date": "2025-01-05"
    },
    "clinical_message": "Concurrent use of opioids and benzodiazepines may result in profound sedation, respiratory depression, coma, and death. FDA Boxed Warning.",
    "recommendation": "Avoid concurrent use. If clinically necessary, limit doses and duration. Prescriber override required.",
    "override_allowed": true,
    "override_reason_codes": ["01", "02", "03"]
  }
}
```

### Example 2: Early Refill - Warning

```json
{
  "claim": {
    "claim_id": "RX20250115000002",
    "ndc": "00071015523",
    "drug_name": "Atorvastatin 20mg",
    "service_date": "2025-01-15",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "member_profile": {
    "previous_fill": {
      "service_date": "2024-12-27",
      "days_supply": 30,
      "quantity": 30
    }
  },
  "response": {
    "status": "paid",
    "authorization_number": "AUTH20250115002"
  },
  "dur_alert": {
    "alert_id": "DUR20250115000002",
    "alert_type": "ER",
    "alert_description": "Early Refill",
    "severity": 3,
    "severity_description": "Minor",
    "details": {
      "previous_fill_date": "2024-12-27",
      "previous_days_supply": 30,
      "current_service_date": "2025-01-15",
      "days_elapsed": 19,
      "percent_used": 63,
      "threshold_percent": 80,
      "days_early": 5
    },
    "clinical_message": "Refill 5 days early. 63% of previous supply used (threshold: 80%).",
    "action_taken": "Approved with warning",
    "professional_service_code": "M0",
    "result_of_service_code": "1A"
  }
}
```

### Example 3: Therapeutic Duplication

```json
{
  "claim": {
    "claim_id": "RX20250115000003",
    "ndc": "00310075590",
    "drug_name": "Rosuvastatin 20mg",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "member_profile": {
    "current_medications": [
      {
        "ndc": "00071015523",
        "drug_name": "Atorvastatin 20mg",
        "last_fill_date": "2025-01-01",
        "days_supply": 30,
        "status": "active"
      }
    ]
  },
  "response": {
    "status": "rejected",
    "reject_code": "88"
  },
  "dur_alert": {
    "alert_id": "DUR20250115000003",
    "alert_type": "TD",
    "alert_description": "Therapeutic Duplication",
    "severity": 2,
    "severity_description": "Moderate",
    "therapeutic_class": "HMG-CoA Reductase Inhibitors (Statins)",
    "conflicting_drug": {
      "ndc": "00071015523",
      "drug_name": "Atorvastatin 20mg",
      "fill_date": "2025-01-01"
    },
    "clinical_message": "Member already has an active statin prescription. Multiple statins are rarely clinically indicated and increase myopathy risk.",
    "recommendation": "Verify intent. If switching statins, discontinue previous therapy.",
    "override_allowed": true
  }
}
```

### Example 4: Geriatric Alert (Beers)

```json
{
  "claim": {
    "claim_id": "RX20250115000004",
    "ndc": "00781102101",
    "drug_name": "Diphenhydramine 25mg",
    "quantity_dispensed": 100,
    "days_supply": 30
  },
  "member": {
    "member_id": "MEM005678",
    "birth_date": "1940-05-15",
    "age": 84
  },
  "response": {
    "status": "paid"
  },
  "dur_alert": {
    "alert_id": "DUR20250115000004",
    "alert_type": "DA",
    "alert_description": "Drug-Age Precaution",
    "severity": 2,
    "severity_description": "Moderate",
    "beers_criteria": true,
    "clinical_message": "Diphenhydramine is on AGS Beers Criteria list for potentially inappropriate medications in older adults (age 65+). High anticholinergic burden may cause confusion, dry mouth, constipation, urinary retention, and increased fall risk.",
    "recommendation": "Consider non-anticholinergic alternatives for sleep or allergy.",
    "alternatives": [
      "Loratadine 10mg (non-sedating antihistamine)",
      "Melatonin 3mg (sleep)",
      "Cetirizine 10mg (low anticholinergic)"
    ],
    "action_taken": "Dispensed with warning",
    "professional_service_code": "P0",
    "result_of_service_code": "1A"
  }
}
```

## Validation Rules

| Rule | Requirement | Example |
|------|-------------|---------|
| DUR code | Valid NCPDP DUR/PPS codes | DD (Drug-Drug), TD (Therapeutic Dup) |
| Severity level | 1 (low) to 3 (high) or text | Severity 3, "Severe" |
| Professional service | Valid NCPDP service code | P0 (Patient Counseling) |
| Result of service | Valid NCPDP result code | 1A (Filled as prescribed) |
| Reason for service | Valid NCPDP reason code | DD (Drug-Drug Interaction) |
| Alert description | Clinical description of alert | "Warfarin + aspirin: increased bleeding" |
| Override required | Boolean for hard stops | true (requires pharmacist override) |

### Business Rules

- **Drug-Drug Interactions (DDI)**: Severity 1-3 based on clinical significance
- **Therapeutic Duplication**: Same drug class, different NDCs
- **Early Refill**: Typically reject if >25% of days supply remaining
- **Age Precautions**: Beers Criteria for patients ≥65
- **Pregnancy Precautions**: Category X drugs for female patients 12-50
- **Controlled Substance Monitoring**: PDMP checks for opioids, benzodiazepines
- **Quantity Limits**: Opioid quantity thresholds (e.g., >90 MME/day)
- **Pharmacist Override**: Some alerts are informational; others require intervention

## Related Skills

### RxMemberSim
- [SKILL.md](SKILL.md) - RxMemberSim overview
- [retail-pharmacy.md](retail-pharmacy.md) - Standard fills
- [specialty-pharmacy.md](specialty-pharmacy.md) - High-risk drug monitoring
- [formulary-management.md](formulary-management.md) - Coverage rules

### Cross-Product: PatientSim
- [../patientsim/elective-joint.md](../patientsim/elective-joint.md) - Post-op opioid monitoring
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - Psychiatric drug interactions

> **Integration Pattern:** Use PatientSim to establish patient medication list and clinical context. Use RxMemberSim dur-alerts to generate realistic drug-drug interactions, therapeutic duplications, and age-related precautions based on the patient's profile.

### Cross-Product: MemberSim
- [../membersim/professional-claims.md](../membersim/professional-claims.md) - PMP/PDMP integration context

> **Integration Pattern:** DUR alerts may trigger clinical interventions documented in MemberSim professional claims (pharmacist consultations, prescriber outreach).

### References
- [../../references/code-systems.md](../../references/code-systems.md) - GPI, DUR codes
