# Tutorial 5: Full Integration

**Time:** 30 minutes  
**Level:** Advanced  
**Products:** PatientSim, MemberSim, RxMemberSim, PopulationSim, NetworkSim

## What You'll Learn

- Combine profiles with journeys
- Generate complete longitudinal data
- Use all products together
- Create production-ready test data

## Step 1: Define the Scenario

Let's create a complete diabetes management program evaluation dataset:

```
You: "I need 200 Medicare diabetics with their first year of care after diagnosis"

Claude: "Perfect use case for Profile + Journey. I'll help you create:

1. **Population Profile**: 200 newly diagnosed diabetics
2. **Journey**: First-year diabetes management
3. **Cross-Product Output**: Clinical + claims + pharmacy

Let me build this step by step.

PROFILE: Newly Diagnosed Medicare Diabetics
────────────────────────────────────────────
• Count: 200 members
• Products: PatientSim, MemberSim, RxMemberSim
• Age: 65-85 (mean 72)
• Diagnosis: E11.9 (new diagnosis within last 30 days)
• Geography: National, population-weighted
• Plans: 55% MA, 45% Original Medicare

JOURNEY: diabetic_first_year
• Duration: 12 months from diagnosis
• Phases: Initial, Titration, Stabilization, Ongoing
• Events: ~12 visits, quarterly labs, monthly Rx fills

Ready to generate?"
```

## Step 2: Customize the Journey

```
You: "Yes, but add more detail on A1c testing - I want to track control over time"

Claude: "Enhanced A1c tracking in journey:

LAB SCHEDULE (A1c focus):
┌───────────┬─────────────────────────────┬────────────────────┐
│ Timepoint │ Labs                        │ Expected A1c Range │
├───────────┼─────────────────────────────┼────────────────────┤
│ Baseline  │ A1c, CMP, Lipids            │ 8.5-11.0%          │
│ Month 3   │ A1c, BMP                    │ 7.5-9.0%           │
│ Month 6   │ A1c, CMP, Lipids            │ 7.0-8.5%           │
│ Month 9   │ A1c, BMP                    │ 6.8-8.0%           │
│ Month 12  │ A1c, CMP, Lipids, Urine     │ 6.5-7.8%           │
└───────────┴─────────────────────────────┴────────────────────┘

A1c trajectory model:
• Responders (65%): Baseline → controlled (<7.5%) by month 6
• Partial responders (25%): Need 2nd agent, improve by month 9
• Non-responders (10%): Require treatment intensification

Proceed with generation?"
```

## Step 3: Execute the Full Generation

```
You: "Generate it"

Claude: "Generating 200 diabetic journeys (12 months each)...

Phase 1: Creating population
• Patients created... ████████████ 200/200
• Members linked... ████████████ 200/200
• Baseline conditions... ████████████ 200/200

Phase 2: Generating journeys
• Initial visits... ████████████ 200/200
• Medication starts... ████████████ 200/200
• Lab sequences... ████████████ 200/200
• Follow-up encounters... ████████████ 200/200

Phase 3: Cross-product sync
• Encounters → Claims... ████████████ 2,400/2,400
• Prescriptions → Fills... ████████████ 2,400/2,400
• Labs → Claim lines... ████████████ 4,800/4,800

✓ GENERATION COMPLETE (47.3 seconds)

SUMMARY:
┌─────────────────────────┬───────────┐
│ Entity Type             │ Count     │
├─────────────────────────┼───────────┤
│ Patients/Members        │ 200       │
│ Encounters              │ 2,412     │
│ Observations (Labs)     │ 4,824     │
│ Medications             │ 1,856     │
│ Prescription Fills      │ 2,408     │
│ Professional Claims     │ 2,412     │
│ Pharmacy Claims         │ 2,408     │
│ Total Claim Lines       │ 9,644     │
└─────────────────────────┴───────────┘

Saved as scenario: 'dm-first-year-cohort-2024'"
```

## Step 4: Validate the Results

```
You: "Show me the A1c improvement over time"

Claude: "A1c Trajectory Analysis for Cohort:

POPULATION A1c DISTRIBUTION BY QUARTER:

         Baseline    Q1         Q2         Q3         Q4
         (n=200)    (n=198)    (n=195)    (n=192)    (n=190)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mean      9.2%       8.3%       7.6%       7.3%       7.1%
Median    9.0%       8.1%       7.4%       7.2%       7.0%
<7.0%     0%         12%        32%        45%        52%
<8.0%     8%         38%        62%        71%        78%
>9.0%     62%        28%        12%        8%         6%

TREATMENT RESPONSE CATEGORIES:
• Excellent responders (A1c <7.0 by Q2): 32%
• Good responders (A1c <7.5 by Q4): 48%
• Partial responders (improvement but >7.5): 14%
• Treatment intensified (added 2nd agent): 22%

This pattern matches real-world first-year outcomes."
```

## Step 5: Query the Data

```
You: "Show me the SQL to analyze cost by A1c control"

Claude: "Here's the analysis query:

SELECT 
    CASE 
        WHEN latest_a1c < 7.0 THEN 'Controlled (<7%)'
        WHEN latest_a1c < 8.0 THEN 'Near Goal (7-8%)'
        WHEN latest_a1c < 9.0 THEN 'Uncontrolled (8-9%)'
        ELSE 'Poorly Controlled (>9%)'
    END as a1c_category,
    COUNT(DISTINCT m.member_id) as member_count,
    ROUND(AVG(total_cost), 2) as avg_total_cost,
    ROUND(AVG(rx_cost), 2) as avg_rx_cost,
    ROUND(AVG(medical_cost), 2) as avg_medical_cost,
    ROUND(AVG(visit_count), 1) as avg_visits
FROM main.members m
JOIN main.member_a1c_summary a ON m.member_id = a.member_id
JOIN main.member_cost_summary c ON m.member_id = c.member_id
WHERE m.scenario_id = 'dm-first-year-cohort-2024'
GROUP BY 1
ORDER BY 2 DESC;

Results:
┌─────────────────────┬───────┬───────────┬─────────┬──────────┬───────┐
│ A1c Category        │ Count │ Total $   │ Rx $    │ Medical $│ Visits│
├─────────────────────┼───────┼───────────┼─────────┼──────────┼───────┤
│ Controlled (<7%)    │ 104   │ $4,250    │ $1,420  │ $2,830   │ 11.2  │
│ Near Goal (7-8%)    │ 52    │ $5,890    │ $1,890  │ $4,000   │ 13.4  │
│ Uncontrolled (8-9%) │ 28    │ $7,450    │ $2,340  │ $5,110   │ 15.8  │
│ Poorly Controlled   │ 12    │ $12,200   │ $3,100  │ $9,100   │ 19.2  │
└─────────────────────┴───────┴───────────┴─────────┴──────────┴───────┘

Clear cost correlation with A1c control!"
```

## Complete Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FULL INTEGRATION FLOW                        │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────────┐         ┌──────────────┐
  │   Profile    │ ──────► │   Journey    │
  │   Builder    │         │   Builder    │
  └──────────────┘         └──────────────┘
         │                        │
         │                        │
         ▼                        ▼
  ┌──────────────┐         ┌──────────────┐
  │   Profile    │         │   Journey    │
  │   Executor   │ ◄─────► │   Executor   │
  └──────────────┘         └──────────────┘
         │                        │
         │    Cross-Domain Sync   │
         └───────────┬────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
┌────────┐      ┌────────┐      ┌────────┐
│Patient │      │ Member │      │RxMember│
│  Sim   │      │  Sim   │      │  Sim   │
└────────┘      └────────┘      └────────┘
    │                │                │
    ▼                ▼                ▼
Clinical         Claims          Pharmacy
Data             Data            Data
```

## Production Use Cases

| Use Case | Products | Key Features |
|----------|----------|--------------|
| **Demo Environment** | All | Complete, realistic data for sales demos |
| **Integration Testing** | All | Test EDI transactions (837, 834, 835) |
| **Analytics Development** | All | Build and test dashboards, reports |
| **ML Model Training** | All | Labeled, structured training data |
| **Care Program Evaluation** | All | Simulate intervention outcomes |

## Try It Yourself

1. "Generate a surgical episode cohort with 90-day outcomes"
2. "Create a new member onboarding dataset for 500 MA members"
3. "Build a CHF population with readmission events"

## Congratulations! 🎉

You've completed the HealthSim tutorial series! You can now:

- Generate individual patients and members
- Create clinical scenarios with conditions, meds, and labs
- Generate claims from encounters
- Build population cohorts with profiles
- Create longitudinal data with journeys
- Use all products together

## Next Steps

- Explore the [Example Library](../examples/) for more scenarios
- Read about [Templates](../../skills/generation/templates/) for pre-built configurations
- Check the [Skills Reference](../../skills/) for all capabilities

---

**← Previous:** [Tutorial 4: Population Cohort](04-population-cohort.md)  
**→ Back to:** [Tutorials Home](README.md)
