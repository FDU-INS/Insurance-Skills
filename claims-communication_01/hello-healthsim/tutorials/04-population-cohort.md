# Tutorial 4: Population Cohort

**Time:** 25 minutes  
**Level:** Intermediate  
**Products:** PatientSim, MemberSim, PopulationSim

## What You'll Learn

- Use the Profile Builder for population-level generation
- Define demographic distributions
- Specify clinical characteristics
- Generate realistic cohorts at scale

## Step 1: Start the Profile Builder

For generating groups, use the Profile Builder:

```
You: "Help me build a profile for 100 Medicare diabetics"

Claude: "I'll help you build a profile for Medicare diabetics. Let me ask a few questions:

1. **Geography**: Should they be from a specific region?
   - National distribution
   - Specific state(s)
   - Metropolitan area

2. **Age range**: Typical Medicare (65+) or include disability (<65)?

3. **Severity**: What diabetes complexity?
   - Controlled (no complications)
   - With complications
   - Mixed (realistic distribution)

What's your preference?"
```

## Step 2: Specify Requirements

```
You: "Texas only, 65+, mixed severity with realistic comorbidities"

Claude: "Great! Here's your profile specification:

PROFILE: Texas Medicare Diabetics
─────────────────────────────────
Count: 100 members
Products: PatientSim, MemberSim, RxMemberSim

DEMOGRAPHICS:
• Age: 65-95 (mean 74, std 7)
• Gender: 48% M / 52% F
• Geography: Texas (population-weighted by county)

CLINICAL:
• Primary: E11.x (Type 2 Diabetes) - 100%
• Severity distribution:
  - Without complications: 40%
  - With complications: 45%
  - Uncontrolled: 15%
• Comorbidities (realistic prevalence):
  - Hypertension: 78%
  - Hyperlipidemia: 72%
  - Obesity: 42%
  - CKD Stage 3+: 28%
  - CAD: 25%

COVERAGE:
• Medicare Advantage: 55%
• Original Medicare: 45%
• Part D enrolled: 92%

Does this look right? I can adjust any parameters."
```

## Step 3: Refine the Profile

```
You: "Increase CKD to 35% and add heart failure at 20%"

Claude: "Updated profile:

COMORBIDITIES (revised):
• Hypertension: 78%
• Hyperlipidemia: 72%
• Obesity: 42%
• CKD Stage 3+: 35% ← increased
• Heart Failure: 20% ← added
• CAD: 25%

This creates a slightly higher-acuity cohort. Ready to generate?"
```

## Step 4: Generate the Cohort

```
You: "Generate it"

Claude: "Generating 100 Texas Medicare diabetics...

Progress:
• Creating patients... ████████████ 100%
• Creating members... ████████████ 100%
• Assigning conditions... ████████████ 100%
• Generating medications... ████████████ 100%
• Cross-product linking... ████████████ 100%

✓ GENERATION COMPLETE

Summary:
┌────────────────────┬───────────┬──────────┐
│ Attribute          │ Target    │ Actual   │
├────────────────────┼───────────┼──────────┤
│ Total members      │ 100       │ 100      │
│ Mean age           │ 74        │ 73.8     │
│ Male %             │ 48%       │ 47%      │
│ Diabetes           │ 100%      │ 100%     │
│ Hypertension       │ 78%       │ 76%      │
│ CKD                │ 35%       │ 34%      │
│ Heart Failure      │ 20%       │ 21%      │
└────────────────────┴───────────┴──────────┘

Saved as scenario: 'texas-medicare-diabetics-2024'"
```

## Step 5: Explore the Cohort

```
You: "Show me the distribution by county"

Claude: "Geographic distribution of cohort:

Texas Counties (top 10):
┌──────────────────┬───────┬────────────┐
│ County           │ Count │ % of Total │
├──────────────────┼───────┼────────────┤
│ Harris           │ 18    │ 18%        │
│ Dallas           │ 12    │ 12%        │
│ Tarrant          │ 9     │ 9%         │
│ Bexar            │ 8     │ 8%         │
│ Travis           │ 6     │ 6%         │
│ Collin           │ 4     │ 4%         │
│ El Paso          │ 4     │ 4%         │
│ Hidalgo          │ 4     │ 4%         │
│ Denton           │ 3     │ 3%         │
│ Fort Bend        │ 3     │ 3%         │
├──────────────────┼───────┼────────────┤
│ Other (42)       │ 29    │ 29%        │
└──────────────────┴───────┴────────────┘

Distribution weighted by Medicare population per county
(source: PopulationSim reference data)"
```

## Step 6: Use a Template

You can also start from a template:

```
You: "Use the Medicare diabetic template instead"

Claude: "Using template 'medicare-diabetic':

Pre-configured profile:
• Age: 65-95 (mean 72)
• Diabetes with standard comorbidities
• Medicare (55% MA, 45% Original)
• National geography

Customizations you can make:
• Count (default: 100)
• Geography (default: national)
• Severity distribution
• Specific comorbidity rates

Use defaults or customize?"
```

## Available Templates

| Template | Description |
|----------|-------------|
| `medicare-diabetic` | Medicare T2DM population |
| `commercial-healthy` | Working-age healthy adults |
| `medicaid-pediatric` | Medicaid children |
| `ma-complex` | High-risk MA members |
| `commercial-maternity` | Pregnant commercial members |

## Try It Yourself

1. "Build a profile for 50 commercial members with asthma"
2. "Create a Medicaid pediatric cohort for California"
3. "Generate 200 MA members with heart failure"

## What's Next?

In [Tutorial 5: Full Integration](05-full-integration.md), you'll combine profiles with journeys to generate complete longitudinal data across all products.

---

**← Previous:** [Tutorial 3: Claims Journey](03-claims-journey.md)  
**→ Next:** [Tutorial 5: Full Integration](05-full-integration.md)
