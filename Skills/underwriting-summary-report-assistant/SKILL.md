---
name: cost-driver-decomposition
description: Decompose and explain healthcare cost growth into contributing factors including utilization changes, unit price shifts, case mix evolution, and population changes. Use when analyzing PMPM cost trends, explaining cost variance to leadership, preparing actuarial summaries, or identifying cost reduction opportunities.

metadata:
  display_name: "Cost Driver Decomposition"
  short_description: "Break down healthcare cost growth by contributing factors"
  default_prompt: "Analyze my cost driver decomposition and recommend clear next actions"
  version: "1.0.0"
  tags:
    - healthcare
  icon_path: "assets/icon.png"
---

# Cost Driver Decomposition

## Overview

This skill breaks down total healthcare cost changes into their component drivers — utilization rate changes, unit cost (price) changes, case-mix/severity shifts, population composition changes, and benefit design effects. It applies actuarial decomposition methods, Kitagawa-Blinder-Oaxaca analysis, and service-category drill-downs to produce transparent, auditable explanations of cost trends.

## When to Use

- Explaining year-over-year or quarter-over-quarter PMPM cost changes to leadership
- Preparing cost trend analysis for actuarial reviews or rate-setting
- Identifying the root causes of cost growth for targeted intervention
- Comparing cost drivers across plans, lines of business, or provider networks
- Supporting VBC contract negotiations with transparent cost trend data

## Required Inputs

| Input | Description | Format |
|-------|-------------|--------|
| Claims data | Allowed amounts, service dates, CPT/HCPCS, revenue codes, DRG | Claims detail |
| Enrollment data | Member months, plan type, LOB, age/sex | Enrollment file |
| Service categories | Inpatient, outpatient, professional, pharmacy, ancillary | Category mapping |
| Network data | In-network vs. OON, contracted rates, provider type | Network file |
| Benefit design | Copay/coinsurance structure, deductible levels, formulary tier | Plan design |
| Prior period data | Same data elements for comparison period(s) | Historical claims |

## Methodology

### Step 1 — Normalize to PMPM Basis

Convert all cost data to per-member-per-month (PMPM) for trend comparability:

- Total allowed PMPM = Total allowed amount / Total member months
- Calculate PMPM for each service category (IP, OP, Professional, Rx, Other)
- Adjust for incomplete periods: apply completion factors for claims lag (IBNR)
- Standardize benefit design impacts to allowed-amount basis (remove member cost-sharing)

### Step 2 — Decompose Cost into Price × Utilization × Mix

Apply the fundamental cost identity:

```
Cost PMPM = Utilization Rate × Unit Cost × Case Mix Index
```

For each service category, separate:

- **Utilization rate**: Admits/1000, visits/1000, scripts/1000, units/1000
- **Unit cost**: Cost per admit, cost per visit, cost per script, cost per unit
- **Case mix**: Average DRG weight (IP), average RVU (professional), average AWP (Rx)

Calculate the contribution of each component to total cost change using the decomposition:

```
ΔCost = ΔUtil × Price₀ × Mix₀ + Util₀ × ΔPrice × Mix₀ + Util₀ × Price₀ × ΔMix + interaction terms
```

### Step 3 — Service Category Drill-Down

Decompose each major service category into sub-categories:

**Inpatient**:
- Medical vs. surgical admissions
- Top 10 DRGs by cost contribution and trend
- Length of stay trends (geometric mean LOS vs. expected)
- Readmission-driven costs

**Outpatient**:
- Facility outpatient vs. ambulatory surgery center
- ED costs (visit volume × cost per visit)
- Advanced imaging (MRI, CT, PET) utilization and unit cost
- Site-of-service shift analysis (hospital outpatient → freestanding)

**Professional**:
- E&M visit trends by complexity level (99213 vs. 99214/99215)
- Specialist referral patterns and cost per referral episode
- Telehealth substitution effects

**Pharmacy**:
- Generic vs. brand vs. specialty drug mix
- Top 10 drugs by cost and trend (new-to-market drugs driving growth)
- Biosimilar adoption rates
- Specialty pharmacy concentration (top 1% of claims driving what % of Rx cost)

### Step 4 — Population Mix Adjustment

Isolate cost changes due to population composition shifts:

- Age/sex factor adjustment: apply prior-period age/sex cost relativities to current population
- Risk score adjustment: compare average RAF score shifts between periods
- Enrollment mix: proportion changes across LOB, plan design, geographic area
- New member vs. continuing member cost differential

### Step 5 — Identify Actionable Cost Drivers

Categorize each driver by controllability:

| Category | Controllable? | Intervention Lever |
|----------|---------------|-------------------|
| Unit price increases | Partially | Network contracting, reference-based pricing |
| Utilization growth | Partially | UM programs, care management, prior auth |
| Case mix severity | Limited | Risk adjustment accuracy, documentation |
| Population aging | Not controllable | Adjust expectations and pricing |
| New technology/drugs | Limited | Formulary management, clinical pathways |
| Site-of-service shift | Yes | Benefit design, steering programs |
| Waste/low-value care | Yes | Choosing Wisely campaigns, clinical decision support |

### Step 6 — Benchmark Cost Drivers

Compare observed drivers against external references:

- Medical CPI components for price trend expectations
- Milliman HCG or Optum normative databases for utilization trends
- PwC/Deloitte annual medical cost trend surveys (typically 6-8% total trend)
- Plan-specific historical trend corridors

### Step 7 — Construct Cost Driver Narrative

Synthesize findings into a structured explanation:

```
Example narrative structure:
"Total medical cost PMPM increased 7.2% ($485 → $520). This was driven by:
 • Unit price increases: +3.8% (hospital rate escalators +4.2%, offset by Rx generic conversions)
 • Utilization changes: +2.1% (ED visits +8%, offset by IP admits −3%)
 • Case mix: +0.9% (higher acuity surgical cases, new specialty drug starts)
 • Population mix: +0.4% (aging, risk score increase)
 Of the 7.2% trend, approximately 3.5 points are addressable through site-of-service
 steering, ED diversion programs, and specialty pharmacy management."
```

## Output Specification

```
Cost Driver Report:
├── Executive Summary (total PMPM trend, top 3 drivers, actionable share)
├── PMPM Trend Summary (by service category, current vs. prior)
├── Decomposition Waterfall (price, utilization, mix contributions)
├── Service Category Deep Dives (IP, OP, Professional, Rx)
├── Population Mix Analysis (age/sex, risk score, enrollment changes)
├── Benchmark Comparison (observed vs. expected by driver)
├── Controllability Assessment (actionable vs. non-actionable drivers)
├── Cost Reduction Opportunity Inventory (estimated savings by lever)
└── Methodology and Data Notes (IBNR factors, normalization methods)
```

## Analysis Framework

### Cost Trend Decomposition Waterfall

Present as a waterfall chart data structure:

| Component | Contribution | Running Total |
|-----------|-------------|---------------|
| Starting PMPM | $485.00 | $485.00 |
| + Price changes | +$18.43 | $503.43 |
| + Utilization changes | +$10.19 | $513.62 |
| + Case mix shift | +$4.37 | $517.99 |
| + Population mix | +$1.94 | $519.93 |
| + Interaction | +$0.07 | $520.00 |
| = Ending PMPM | | $520.00 |

## Examples

**Example 1 — Annual Cost Trend for Commercial Plan**
Decompose a 9.1% PMPM increase for a 120,000-member commercial plan. Price contributed +4.2% (hospital contract escalators), utilization +2.8% (driven by 14% ED growth and specialty referral increases), pharmacy mix +1.6% (two new specialty drugs), population +0.5%. Identify $14M addressable through ED diversion ($4M), site-of-service steering ($6M), and specialty pharmacy step therapy ($4M).

**Example 2 — MA Plan Cost Driver Analysis**
Explain why a 40,000-member MA plan's medical loss ratio increased from 84% to 87%. Decompose: inpatient cost +11% (3 high-cost transplant cases contributed 40% of IP increase), outpatient +6% (advanced imaging), pharmacy +9% (Part B drugs). After removing outlier cases, underlying trend is 5.8%, within actuarial expectations.

## Guidelines

- Always apply IBNR completion factors before trend comparison; incomplete data understates recent costs
- Separate one-time events (catastrophic claims, COVID-19 surges) from underlying trend
- Use allowed amounts (not paid amounts) for trend analysis to neutralize benefit design changes
- Apply large-claim pooling (truncate at $250K or plan-specific threshold) for stable trend estimates
- Report both per-member and total-dollar perspectives — they tell different stories

## Validation Checklist

- [ ] PMPM calculations use correct member-month denominators
- [ ] IBNR/completion factors are applied and documented
- [ ] Decomposition components sum to total observed change (reconciliation check)
- [ ] Large claims are identified and impact is quantified separately
- [ ] Service category mappings are consistent across periods
- [ ] Benchmark sources are current and relevant to population type
- [ ] Controllable vs. uncontrollable classification is clinically sound

## HIPAA Compliance

This skill processes aggregate financial and utilization data. When patient-level claims are used in decomposition, all processing must comply with HIPAA Privacy and Security Rules. Apply minimum necessary data access. Large-claim analyses that reference specific cases must be de-identified in reports per 45 CFR §164.514. Cost reports shared with brokers, consultants, or external actuaries require Business Associate Agreements. Never include member identifiers in cost trend outputs.
