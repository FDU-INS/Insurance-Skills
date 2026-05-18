---
name: journey-patterns
description: Common temporal patterns for healthcare event sequences
type: reference
---

# Journey Patterns Reference

This document describes the common patterns used to structure healthcare event journeys.

## Pattern Overview

| Pattern | Structure | Use Cases |
|---------|-----------|-----------|
| **Linear** | A → B → C | Simple sequences, routine care |
| **Branching** | A → B → (C OR D) | Decision points, outcomes |
| **Cyclic** | A → B → C → A... | Recurring care, refills |
| **Protocol** | Structured schedule | Clinical trials, treatment cycles |
| **Lifecycle** | Multi-phase progression | Disease progression, membership |

---

## Linear Pattern

### Description
Events occur in a fixed sequence, one after another. The simplest pattern.

### Structure
```
┌───┐     ┌───┐     ┌───┐     ┌───┐
│ A │ ──► │ B │ ──► │ C │ ──► │ D │
└───┘     └───┘     └───┘     └───┘
```

### Schema
```json
{
  "pattern": "linear",
  "events": [
    {"id": "A", "timing": {"day": 0}},
    {"id": "B", "timing": {"day": 7}},
    {"id": "C", "timing": {"day": 14}},
    {"id": "D", "timing": {"day": 21}}
  ]
}
```

### Healthcare Examples

**Routine Vaccination**
```
Schedule appointment → Receive vaccine → Post-vaccine check (if needed)
```

**Simple Lab Order**
```
Order placed → Specimen collected → Results available → Provider review
```

**Referral Completion**
```
PCP referral → Specialist appointment → Report back to PCP
```

### When to Use
- Routine, predictable care sequences
- Administrative workflows
- Simple diagnostic pathways
- Training/tutorial cohorts

---

## Branching Pattern

### Description
Events reach decision points where different paths are taken based on conditions.

### Structure
```
                    ┌───┐
               ┌──► │ C │ (if condition)
┌───┐    ┌───┐│    └───┘
│ A │ ─► │ B │┤
└───┘    └───┘│    ┌───┐
               └──► │ D │ (else)
                    └───┘
```

### Schema
```json
{
  "pattern": "branching",
  "events": [
    {"id": "A", "timing": {"day": 0}},
    {"id": "B", "timing": {"day": 7}}
  ],
  "branch_point": {
    "after": "B",
    "condition": "lab_result > threshold",
    "branches": {
      "true": [{"id": "C", "timing": {"day": 14}}],
      "false": [{"id": "D", "timing": {"day": 14}}]
    }
  }
}
```

### Healthcare Examples

**ER Chest Pain Workup**
```
ER arrival → Initial workup → 
  IF troponin positive → Admit to CCU → Cardiac cath
  ELSE → Discharge → Cardiology follow-up
```

**Diabetes Treatment Escalation**
```
Quarterly visit → A1c check →
  IF A1c > 8.0 → Add second agent → Increase monitoring
  ELSE → Continue current therapy
```

**Cancer Screening**
```
Screening test →
  IF positive → Diagnostic workup → Biopsy → (Malignant OR Benign paths)
  ELSE → Routine follow-up schedule
```

### Branching Types

| Type | Description | Example |
|------|-------------|---------|
| **Condition-based** | Clinical value determines path | A1c > 9.0 |
| **Probability-based** | Random with set probability | 15% complication rate |
| **Multi-way** | More than 2 options | Severity: mild/moderate/severe |
| **Nested** | Branches within branches | Decision trees |

### Multi-way Branch Schema
```json
{
  "branch_point": {
    "condition": "severity",
    "branches": {
      "mild": [{"id": "outpatient_treatment"}],
      "moderate": [{"id": "observation_stay"}],
      "severe": [{"id": "icu_admission"}]
    }
  }
}
```

---

## Cyclic Pattern

### Description
Events repeat on a regular schedule, creating loops in the timeline.

### Structure
```
┌───┐     ┌───┐     ┌───┐
│ A │ ──► │ B │ ──► │ C │ ──┐
└───┘     └───┘     └───┘   │
  ▲                         │
  └─────────────────────────┘
        (repeat)
```

### Schema
```json
{
  "pattern": "cyclic",
  "cycle": {
    "events": [
      {"id": "A", "timing": {"day": 0}},
      {"id": "B", "timing": {"day": 7}},
      {"id": "C", "timing": {"day": 14}}
    ],
    "recurrence": {
      "frequency": "monthly",
      "count": 12,
      "end_condition": "duration_12_months"
    }
  }
}
```

### Healthcare Examples

**Medication Refill Cycle**
```
Fill prescription → Take medication (30 days) → Refill → [repeat]
```

**Quarterly Diabetes Monitoring**
```
Office visit → Labs (A1c, CMP) → Review results → [repeat quarterly]
```

**Dialysis Schedule**
```
Dialysis session → Recovery → [repeat 3x/week]
```

**Chemotherapy Cycles**
```
Day 1: Infusion → Days 2-7: Recovery → Day 8: Labs → Days 9-21: Rest → [repeat]
```

### Recurrence Options

| Option | Schema | Description |
|--------|--------|-------------|
| Fixed count | `"count": 12` | Repeat exactly 12 times |
| Duration | `"duration": "12 months"` | Repeat for time period |
| Until condition | `"until": "goal_achieved"` | Repeat until criteria met |
| Indefinite | `"indefinite": true` | Continue until stopped |

### Variance in Cycles
```json
{
  "recurrence": {
    "frequency": "monthly",
    "variance": {
      "days": 3,
      "type": "uniform"
    }
  }
}
```

---

## Protocol Pattern

### Description
Highly structured schedule following a defined clinical protocol. Common in clinical trials and standardized treatment regimens.

### Structure
```
Cycle 1                    Cycle 2                    Cycle 3
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│ D1  D8  D15  D21    │   │ D1  D8  D15  D21    │   │ D1  D8  D15  D21    │
│ ●   ●   ●    ○      │   │ ●   ●   ●    ○      │   │ ●   ●   ●    ○      │
└─────────────────────┘   └─────────────────────┘   └─────────────────────┘
● = Treatment day  ○ = Rest
```

### Schema
```json
{
  "pattern": "protocol",
  "protocol": {
    "name": "FOLFOX",
    "cycle_length_days": 14,
    "total_cycles": 12,
    "schedule": [
      {
        "day": 1,
        "events": [
          {"type": "infusion", "drug": "oxaliplatin", "dose": "85 mg/m²"},
          {"type": "infusion", "drug": "leucovorin", "dose": "400 mg/m²"},
          {"type": "infusion", "drug": "5-FU bolus", "dose": "400 mg/m²"},
          {"type": "infusion", "drug": "5-FU continuous", "dose": "2400 mg/m²", "duration": "46 hours"}
        ]
      },
      {
        "day": 2,
        "events": [
          {"type": "disconnect", "drug": "5-FU pump"}
        ]
      },
      {
        "day": 8,
        "events": [
          {"type": "labs", "panels": ["CBC", "CMP"]}
        ],
        "optional": true
      }
    ],
    "assessments": {
      "pre_cycle": ["CBC", "CMP", "neuropathy_grade"],
      "imaging": {"frequency": "every_4_cycles", "type": "CT"}
    },
    "dose_modifications": [
      {"condition": "ANC < 1500", "action": "delay_1_week"},
      {"condition": "neuropathy_grade >= 2", "action": "reduce_oxaliplatin_25%"}
    ]
  }
}
```

### Healthcare Examples

**Clinical Trial Protocol**
```
Screening → Baseline → 
  Cycle 1: Day 1, Day 8, Day 15 → 
  Cycle 2: Day 1, Day 8, Day 15 → 
  ... → 
  End of Treatment → Follow-up visits
```

**Vaccination Series**
```
Dose 1 (Day 0) → Dose 2 (Week 4) → Dose 3 (Week 8) → Dose 4 (Month 6)
```

**Physical Therapy Protocol**
```
Week 1-2: 3x/week, passive ROM →
Week 3-4: 3x/week, active ROM →
Week 5-8: 2x/week, strengthening →
Week 9-12: 1x/week, functional training
```

### Protocol Features

| Feature | Description |
|---------|-------------|
| **Windows** | Allowable timing variance (e.g., Day 8 ± 2 days) |
| **Holds** | Pause protocol for adverse events |
| **Modifications** | Dose adjustments based on toxicity |
| **Discontinuation** | Criteria for stopping early |

---

## Lifecycle Pattern

### Description
Multi-phase progression representing major life or health status transitions over extended periods.

### Structure
```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Phase 1 │ → │  Phase 2 │ → │  Phase 3 │ → │  Phase 4 │
│  (onset) │   │ (active) │   │ (stable) │   │(maintain)│
└──────────┘   └──────────┘   └──────────┘   └──────────┘
   Months        Months         Years          Ongoing
```

### Schema
```json
{
  "pattern": "lifecycle",
  "phases": [
    {
      "name": "onset",
      "duration": "1-3 months",
      "characteristics": ["diagnosis", "initial_treatment", "education"],
      "transition_criteria": "stable_on_therapy"
    },
    {
      "name": "active_treatment",
      "duration": "3-12 months",
      "characteristics": ["titration", "monitoring", "complication_watch"],
      "transition_criteria": "goals_achieved"
    },
    {
      "name": "stable",
      "duration": "1-5 years",
      "characteristics": ["maintenance", "routine_monitoring", "prevention"],
      "transition_criteria": "progression OR remission"
    },
    {
      "name": "advanced",
      "duration": "variable",
      "characteristics": ["intensified_treatment", "specialty_care"],
      "terminal": true
    }
  ]
}
```

### Healthcare Examples

**Diabetes Lifecycle**
```
Pre-diabetes → New Diagnosis → Early Management → Stable Control → 
  Complications → Advanced Disease
```

**Cancer Journey**
```
Screening → Diagnosis → Active Treatment → Survivorship → 
  (Recurrence → Treatment) OR (Long-term Survivorship)
```

**Membership Lifecycle**
```
Prospect → New Member → Engaged Member → Loyal Member → 
  (Retained) OR (Disenrolled)
```

**Pregnancy Journey**
```
Preconception → First Trimester → Second Trimester → Third Trimester →
  Delivery → Postpartum → Pediatric Care
```

### Phase Transitions

| Transition Type | Trigger | Example |
|-----------------|---------|---------|
| **Time-based** | Duration elapsed | 90 days in phase |
| **Event-based** | Specific event occurs | Goal A1c achieved |
| **Condition-based** | Clinical criteria met | Remission confirmed |
| **Administrative** | External trigger | Coverage terminated |

---

## Combining Patterns

Complex journeys often combine multiple patterns:

### Example: Cancer Treatment Journey

```
Lifecycle (overall structure)
├── Phase 1: Diagnosis (Linear)
│   └── Screening → Biopsy → Staging
├── Phase 2: Treatment Decision (Branching)
│   └── Surgery vs. Chemo vs. Radiation
├── Phase 3: Active Treatment (Protocol + Cyclic)
│   └── FOLFOX protocol with 14-day cycles
└── Phase 4: Survivorship (Lifecycle continues)
    └── Surveillance schedule (Cyclic)
```

### Nested Pattern Schema
```json
{
  "pattern": "lifecycle",
  "phases": [
    {
      "name": "diagnosis",
      "sub_pattern": "linear",
      "events": [...]
    },
    {
      "name": "treatment",
      "sub_pattern": "protocol",
      "protocol": {...}
    },
    {
      "name": "maintenance",
      "sub_pattern": "cyclic",
      "cycle": {...}
    }
  ]
}
```

---

## Pattern Selection Guide

| Cohort | Recommended Pattern |
|----------|---------------------|
| Simple appointment sequence | Linear |
| ER visit with uncertain outcome | Branching |
| Monthly medication refills | Cyclic |
| Chemotherapy treatment | Protocol |
| Chronic disease management | Lifecycle |
| Clinical trial | Protocol + Branching |
| New member onboarding | Lifecycle + Linear |
| Surgical episode | Linear + Branching |

---

*Part of the HealthSim Generative Framework*
