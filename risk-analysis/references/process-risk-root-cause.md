# Process Risk and Root Cause Analysis

Reference content consolidated from Dumas et al. (2013) *Fundamentals of Business Process Management* and Page (2015) *The Power of Business Process Improvement*.

---

## Root Cause Analysis — Ishikawa/Fishbone Diagram (Dumas et al., 2013)

### The 6 Ms Framework

Organise potential causes of a process problem into six categories:

```
        Man             Method          Machine
         \               |               /
          \              |              /
           \             |             /
            ─────────────┼─────────────
                    [PROBLEM]
            ─────────────┼─────────────
           /             |             \
          /              |              \
         /               |               \
     Material      Measurement        Milieu
```

| Category | Focus Area | Example Causes |
|---|---|---|
| **Man** (People/Skills) | Staff capability, training, motivation | Untrained staff, high turnover, unclear responsibilities |
| **Method** (Process Design) | Procedures, workflows, policies | Missing SOPs, overly complex approval chains, undocumented steps |
| **Machine** (Equipment/Systems) | Technology, tools, infrastructure | Outdated software, unreliable equipment, insufficient capacity |
| **Material** (Inputs/Data) | Raw materials, information, data quality | Poor-quality inputs, incomplete data, unreliable suppliers |
| **Measurement** (Metrics/Feedback) | KPIs, monitoring, feedback loops | No performance metrics, delayed reporting, wrong KPIs tracked |
| **Milieu** (Environment/Culture) | Workplace conditions, organisational culture | Poor workplace layout, blame culture, resistance to change |

### Methodology

1. **Define the problem** — State clearly and specifically what is going wrong
2. **Draw the fishbone** — Create the diagram with the 6 Ms as main branches
3. **Brainstorm causes** — For each M, identify possible causes (involve the team)
4. **Apply 5 Whys** — For the most likely causes, drill deeper (see below)
5. **Prioritise** — Rank causes by likelihood and impact
6. **Develop countermeasures** — Create specific actions to address root causes

---

## 5 Whys Technique (Dumas et al., 2013)

A simple but powerful technique for drilling past symptoms to root causes:

### Process

1. **State the problem** clearly
2. **Ask "Why?"** — Why does this problem occur?
3. **For each answer, ask "Why?" again** — Repeat up to five times
4. **Identify the root cause** — The root cause is the point where, if eliminated, the problem would not recur

### Example

```
Problem: Customer orders are frequently delivered late.

Why? → Because the packing team finishes late.
Why? → Because they receive the pick list late.
Why? → Because the warehouse system generates pick lists in batch at 2pm.
Why? → Because the system was configured for overnight orders only.
Why? → Because the original setup did not account for same-day orders.

Root cause: System configuration does not support current order patterns.
Countermeasure: Reconfigure system for real-time pick list generation.
```

### Key Principle

A true root cause has two properties:
- **If eliminated**, the problem would be prevented from recurring
- **It is actionable** — the organisation can do something about it

---

## Pareto Analysis (Dumas et al., 2013)

### The 80/20 Rule

In most processes, approximately 20% of causes account for 80% of issues. Pareto analysis helps focus improvement efforts where they will have the greatest impact.

### Application Steps

1. **Collect data** — Log all process issues/defects over a defined period
2. **Categorise** — Group issues by type or cause
3. **Count frequency** — Tally occurrences for each category
4. **Sort descending** — Rank from most frequent to least
5. **Calculate cumulative percentage** — Running total as % of all issues
6. **Draw the Pareto chart** — Bar chart (frequency) with cumulative % line
7. **Identify the vital few** — Focus on categories up to the 80% cumulative mark

### Example Format

| Issue Category | Frequency | % of Total | Cumulative % | Action |
|---|---|---|---|---|
| Late supplier delivery | 45 | 36% | 36% | Address first |
| Data entry errors | 30 | 24% | 60% | Address second |
| System downtime | 18 | 14% | 74% | Address third |
| Stock discrepancy | 10 | 8% | 82% | — |
| Other (7 categories) | 22 | 18% | 100% | — |

The top three categories (74%) should be the focus of risk mitigation in the business plan.

---

## Issue Register (Dumas et al., 2013)

### Structure

A formal log for tracking identified process issues, their analysis, and resolution:

| Field | Description | Example |
|---|---|---|
| **Issue ID** | Unique identifier | ISS-001 |
| **Issue name** | Short descriptive name | Late order fulfilment |
| **Description** | Detailed explanation of the issue | Orders taking 5+ days vs. 2-day target |
| **Impact dimension** | Which Devil's Quadrangle dimension is affected: Time / Cost / Quality / Flexibility | Time |
| **Qualitative impact** | Narrative description of consequences | Customer complaints, lost repeat business |
| **Quantitative impact** | Estimated magnitude | Adds 3 days to cycle time; affects 30% of orders |
| **Possible causes** | Root causes identified via Ishikawa/5 Whys | Batch processing, supplier delays |
| **Suggested improvements** | Potential solutions with trade-off notes | Real-time processing (cost: system upgrade UGX 15M) |
| **Priority** | High/Medium/Low based on impact × feasibility | High |

### Linking to Devil's Quadrangle

Map each issue to one or more performance dimensions to ensure balanced risk coverage:

- **Time issues** — Delays, bottlenecks, excessive cycle times
- **Cost issues** — Waste, rework costs, excess inventory carrying costs
- **Quality issues** — Defects, errors, customer complaints, compliance failures
- **Flexibility issues** — Inability to handle variations, slow response to changes

---

## Internal Controls Framework (Page, 2015)

### Methodology

A systematic approach to identifying operational risks within processes:

1. **Walk through the process map** — Examine each activity box one by one
2. **Ask "What can go wrong?"** — For every activity, brainstorm potential failures, errors, and risks
3. **Place warning symbols first** — Mark all identified risks on the process map before discussing solutions
4. **Discuss solutions second** — Only after all risks are identified, develop internal controls for each

**Key principle:** Identify all risks first, solve second. This prevents the common mistake of fixing obvious problems while missing less visible but more critical risks.

### Internal Controls Table

| Activity # | Activity Description | Possible Issue(s) | Internal Control(s) |
|---|---|---|---|
| 1 | Receive customer order | Incomplete information; duplicate order | Mandatory fields on order form; system duplicate check |
| 2 | Verify payment | Fraudulent payment; payment not received | Payment gateway verification; 24-hour hold for new customers |
| 3 | Pick items from stock | Wrong items picked; items out of stock | Barcode scanning verification; real-time stock alerts |
| 4 | Pack and ship | Damaged in transit; wrong address | Quality check before sealing; address verification step |
| 5 | Invoice customer | Incorrect pricing; delayed invoice | System-generated pricing from catalogue; auto-invoice on dispatch |

### Types of Internal Controls

| Control Type | Purpose | Example |
|---|---|---|
| **Preventive** | Stop the issue from occurring | Input validation, access restrictions, mandatory approvals |
| **Detective** | Identify issues when they occur | Exception reports, reconciliations, audit logs |
| **Corrective** | Fix issues after they occur | Return procedures, rework processes, complaint resolution |

For business plans, demonstrate a mix of all three types across core processes.

---

## Stakeholder Analysis for Risk (Dumas et al., 2013)

### Four Dimensions

Assess each stakeholder across four factors to understand risk exposure from people:

| Dimension | Question | Scale |
|---|---|---|
| **Interest** | How much does this stakeholder care about the process/change? | Low / Medium / High |
| **Influence** | How much power does this stakeholder have over the process? | Low / Medium / High |
| **Impact** | How much will this stakeholder be affected by the process/change? | Low / Medium / High |
| **Attitude** | Is the stakeholder supportive or resistant? | Supportive / Neutral / Resistant |

### Stakeholder Risk Matrix

```
High Influence │ Keep satisfied  │ Manage closely
               │ (inform, consult│ (engage, involve)
               │  — risk: can    │  — risk: can block
               │  block quietly) │  if not managed)
───────────────┼─────────────────┼──────────────────
Low Influence  │ Monitor         │ Keep informed
               │ (minimal effort │ (regular updates
               │  — low risk)    │  — risk: morale)
               └─────────────────┴──────────────────
                 Low Interest      High Interest
```

### Application in Business Plans

Identify stakeholders who pose risks due to:
- **High influence + resistant attitude** — Can block or undermine operations
- **High impact + low awareness** — May resist when changes affect them unexpectedly
- **Regulatory stakeholders** — Government agencies with enforcement power

---

## Process-Related Risk Categories

### Mapped to Devil's Quadrangle Dimensions

| Risk Dimension | Risk Type | Example Risks | Mitigation Approaches |
|---|---|---|---|
| **Time** | Delay risks | Supplier lead times, approval bottlenecks, seasonal demand spikes | Buffer stock, parallel processing, SLAs with suppliers |
| **Cost** | Cost overrun risks | Input price volatility, rework costs, hidden overhead, scope creep | Fixed-price contracts, process costing, variance monitoring |
| **Quality** | Quality failure risks | Defective inputs, untrained staff, equipment failure, compliance gaps | Quality checks, training programmes, preventive maintenance, audits |
| **Flexibility** | Rigidity risks | Single-source dependency, inflexible systems, narrow skill sets | Multiple suppliers, modular systems, cross-training |

### Cross-Dimensional Risks

Some risks affect multiple dimensions simultaneously:

| Risk | Time Impact | Cost Impact | Quality Impact | Flexibility Impact |
|---|---|---|---|---|
| Key supplier failure | Delivery delays | Emergency procurement costs | Quality uncertainty | Forced to find alternatives |
| Staff turnover | Recruitment time | Hiring/training costs | Knowledge loss | Reduced capacity |
| System failure | Process stoppage | Revenue loss, recovery costs | Data integrity risk | Manual workarounds needed |
| Regulatory change | Compliance timeline | Compliance costs | New standards to meet | Process redesign required |

---

## Application in Business Plan Risk Analysis

### For Process-Level Risks

1. **Map core processes** from the operations plan (Section 08)
2. **Walk through each process** using Page's "What can go wrong?" approach
3. **Document in the internal controls table** format
4. **Apply root cause analysis** (Ishikawa + 5 Whys) for significant risks
5. **Use Pareto analysis** to prioritise the vital few risks for detailed mitigation

### For Strategic-Level Risks

1. **Map risks to Devil's Quadrangle dimensions** to ensure balanced coverage
2. **Conduct stakeholder analysis** for change-related and people risks
3. **Maintain an issue register** for ongoing risk tracking
4. **Link to the financial projections** (Section 10) — quantify cost impacts where possible

### Integration with Other Sections

- **Section 08 (Operations Plan)** — Source of process-level risks; internal controls table
- **Section 10 (Financial Projections)** — Quantified cost impact of risks; contingency budgets
- **Section 13 (Implementation Timeline)** — Risk-adjusted milestone planning
- **Meta: Financial Stress Test** — Scenario analysis for high-impact risks

---

## Citations

- Dumas, M., La Rosa, M., Mendling, J. & Reijers, H.A. (2013) *Fundamentals of Business Process Management*. Berlin: Springer.
- Page, S. (2015) *The Power of Business Process Improvement: 10 Simple Steps to Increase Effectiveness, Efficiency, and Adaptability*. 2nd edn. New York: AMACOM.
