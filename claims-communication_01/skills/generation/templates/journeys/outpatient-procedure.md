---
name: outpatient-procedure-journey
description: Outpatient/ambulatory surgery procedure journey
type: journey_template
---

# Outpatient Procedure Journey

Same-day ambulatory surgery procedure journey template.

## Quick Start

```
User: "Create an outpatient colonoscopy journey"

Claude: "Creating outpatient procedure journey:
- Pre-procedure preparation
- Same-day procedure
- Post-procedure recovery
- Follow-up visit"
```

## Journey Specification

```json
{
  "template": {
    "id": "outpatient_procedure",
    "name": "Outpatient Procedure Episode",
    "version": "1.0",
    "duration": "14-30 days",
    "category": "surgical",
    "tags": ["outpatient", "ambulatory", "same_day", "procedure"]
  },
  
  "procedure_categories": {
    "diagnostic": ["colonoscopy", "egd", "bronchoscopy", "cystoscopy"],
    "minor_surgical": ["hernia_repair", "cholecystectomy", "knee_arthroscopy"],
    "pain_management": ["epidural_injection", "facet_block", "rfa"],
    "eye": ["cataract", "lasik"],
    "other": ["carpal_tunnel", "skin_lesion_excision"]
  },
  
  "phases": [
    {
      "name": "pre_procedure",
      "duration": "1-2 weeks",
      "events": [
        {"type": "specialist_consult", "timing": "day -14"},
        {"type": "pre_op_labs", "timing": "day -7", "conditional": "age>50 OR comorbidities"},
        {"type": "pre_op_clearance", "timing": "day -3", "conditional": "comorbidities"},
        {"type": "prep_instructions", "timing": "day -1"}
      ]
    },
    {
      "name": "procedure_day",
      "duration": "4-8 hours",
      "events": [
        {"type": "arrival", "timing": "T-2hr"},
        {"type": "pre_op_nursing", "timing": "T-1hr"},
        {"type": "anesthesia", "type": ["sedation", "mac", "regional", "general"]},
        {"type": "procedure", "duration": "15min-2hr"},
        {"type": "recovery_phase1", "duration": "30-60min"},
        {"type": "recovery_phase2", "duration": "30-60min"},
        {"type": "discharge", "timing": "same_day"}
      ]
    },
    {
      "name": "post_procedure",
      "duration": "1-2 weeks",
      "events": [
        {"type": "followup_call", "timing": "day 1"},
        {"type": "followup_visit", "timing": "day 7-14", "conditional": "surgical"}
      ]
    }
  ],
  
  "facility_types": ["asc", "hopd", "office_based"]
}
```

## Common Outpatient Procedures

| Procedure | Duration | Anesthesia | Follow-up |
|-----------|----------|------------|-----------|
| Colonoscopy | 30-45 min | Sedation | Results call |
| Cataract | 15-20 min | Local/MAC | Day 1 visit |
| Knee arthroscopy | 45-60 min | General/Regional | 1-2 week visit |
| Hernia repair | 45-90 min | General/Regional | 1 week visit |
| Epidural injection | 15-30 min | Local/sedation | 2 week call |

## Cost Profile

| Component | ASC | HOPD |
|-----------|-----|------|
| Facility fee | $1,500 - $4,000 | $3,000 - $10,000 |
| Anesthesia | $400 - $1,000 | $600 - $1,500 |
| Surgeon/provider | $500 - $2,000 | $500 - $2,000 |
| **Total** | **$2,400 - $7,000** | **$4,100 - $13,500** |

## Related Templates

- **[Surgical Episode](surgical-episode.md)** - Inpatient surgery
- **[Cardiac Surgery Episode](cardiac-surgery-episode.md)** - Major cardiac

---

*Part of the HealthSim Generative Framework Template Library*
