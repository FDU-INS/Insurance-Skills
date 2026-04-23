---
name: bariatric-episode-journey
description: Bariatric surgery episode journey template
type: journey_template
---

# Bariatric Episode Journey

Complete bariatric surgery episode from evaluation through long-term follow-up.

## Quick Start

```
User: "Create a gastric bypass surgery episode"

Claude: "Creating bariatric journey:
- 6-month pre-operative program
- Surgical procedure
- Post-operative diet progression
- Long-term follow-up"
```

## Journey Specification

```json
{
  "template": {
    "id": "bariatric_episode",
    "name": "Bariatric Surgery Episode",
    "version": "1.0",
    "duration": "18 months",
    "category": "surgical",
    "tags": ["bariatric", "surgery", "obesity", "weight_loss"]
  },
  
  "procedure_types": {
    "gastric_sleeve": {"probability": 0.65, "los": 2},
    "gastric_bypass": {"probability": 0.30, "los": 3},
    "duodenal_switch": {"probability": 0.05, "los": 4}
  },
  
  "phases": [
    {
      "name": "pre_operative_program",
      "duration": "6 months",
      "events": [
        {"type": "bariatric_consult", "timing": "month -6"},
        {"type": "psych_evaluation", "timing": "month -5"},
        {"type": "nutritional_consult", "timing": "month -5", "frequency": "monthly"},
        {"type": "sleep_study", "timing": "month -4"},
        {"type": "egd", "timing": "month -3"},
        {"type": "medically_supervised_diet", "duration": "6 months"},
        {"type": "pre_op_clearance", "timing": "week -2"}
      ]
    },
    {
      "name": "surgery",
      "duration": "2-4 days",
      "events": [
        {"type": "admission", "timing": "day 0"},
        {"type": "surgery", "timing": "day 0"},
        {"type": "discharge", "timing": "day 2-4"}
      ]
    },
    {
      "name": "post_operative",
      "duration": "12 months",
      "events": [
        {"type": "followup", "timing": "week 1"},
        {"type": "followup", "timing": "week 2"},
        {"type": "followup", "timing": "month 1"},
        {"type": "followup", "timing": "month 3"},
        {"type": "followup", "timing": "month 6"},
        {"type": "followup", "timing": "month 12"},
        {"type": "nutritional_followup", "frequency": "quarterly"},
        {"type": "labs", "frequency": "quarterly"}
      ]
    }
  ],
  
  "outcomes": {
    "excess_weight_loss_1yr": {"mean": 65, "std": 15},
    "complication_rate": 0.08,
    "revision_rate_5yr": 0.05
  }
}
```

## Pre-Authorization Requirements

| Requirement | Duration/Details |
|-------------|------------------|
| BMI criteria | ≥40 or ≥35 with comorbidities |
| Supervised diet | 3-6 months |
| Psych clearance | Required |
| Nutritional education | 3+ sessions |
| Documentation | 2-5 years weight history |

## Cost Profile

| Component | Cost Range |
|-----------|-----------|
| Pre-operative program | $2,000 - $5,000 |
| Surgery & hospitalization | $20,000 - $35,000 |
| Follow-up care (year 1) | $3,000 - $6,000 |
| Supplements & labs | $500 - $1,500/year |
| **Total episode** | **$25,500 - $47,500** |

## Related Templates

- **[Surgical Episode](surgical-episode.md)** - General surgical template
- **[Commercial High-Cost](../profiles/commercial-high-cost.md)** - High-cost patterns

---

*Part of the HealthSim Generative Framework Template Library*
