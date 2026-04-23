# Risk Identification, Assessment & Response Methods

*Sources: Raydugin, Project Risk Management: Essential Methods for Project Teams and Decision Makers (Wiley, 2013); Murray-Webster & Pullan, Making Risk Management Work, 2nd ed. (Routledge); Olson & Wu, Enterprise Risk Management Models (Springer, 2017).*

---

## 1. Three-Part Uncertainty Naming Convention (Raydugin)

The most common failure in risk registers is vague risk descriptions that no one can act on. Raydugin's three-part naming convention forces clarity:

```
[CAUSE] → [RISK EVENT] → [IMPACT ON OBJECTIVES]
```

**Format:** "Due to [cause], there is a risk that [risk event] might occur, which would result in [impact]."

### Examples

| Weak Description | Three-Part Description |
|---|---|
| "Supplier risk" | "Due to sole-sourcing from a single cement supplier, there is a risk that supply disruption might occur, resulting in construction delays of 4–8 weeks and cost overruns of UGX 15M+" |
| "Market risk" | "Due to lower-than-projected consumer incomes in the target area, there is a risk that demand for premium products might underperform, resulting in revenue shortfall of 30% in Year 1" |
| "Key person risk" | "Due to dependence on a single founder-manager, there is a risk of incapacity or departure, resulting in operational paralysis and inability to secure additional financing" |

**Why it works:** The three-part format:
- Clarifies the **cause** (what triggers the risk) — enables prevention
- Identifies the **event** (what actually happens) — enables monitoring
- Specifies the **impact** (consequence in quantitative or qualitative terms) — enables prioritisation

---

## 2. Risk Identification Methods (Raydugin, Murray-Webster)

### Risk Breakdown Structure (RBS)

Organise risks into a hierarchy before identification to ensure completeness:

```
Project/Business Risks
├── External Risks
│   ├── Market (demand, competition, pricing)
│   ├── Regulatory (licences, compliance changes)
│   ├── Environmental (weather, climate, ecological)
│   └── Political/Social (elections, community opposition)
├── Commercial/Financial Risks
│   ├── Credit (debtors not paying)
│   ├── Currency (UGX/USD fluctuation)
│   ├── Funding (loan drawdown delays)
│   └── Input cost inflation
├── Operational Risks
│   ├── Supply chain (input availability, quality)
│   ├── People (skills availability, retention, health)
│   ├── Technology (system failure, data loss)
│   └── Quality (rework, product defects)
└── Strategic Risks
    ├── Business model (value proposition viability)
    ├── Assumptions (market size over-estimated)
    └── Growth (scaling challenges)
```

### Bowtie Diagram (Raydugin)

The Bowtie diagram visualises both sides of a risk event simultaneously — causes on the left, consequences on the right — and overlays the prevention and mitigation controls.

```
                    PREVENTION              MITIGATION
                    (reduce likelihood)     (reduce impact)
                         ↓                       ↓
Cause A ─────────┐                          ┌───────── Consequence 1
                 │                          │
Cause B ─────────┼──── [RISK EVENT] ────────┼───────── Consequence 2
                 │                          │
Cause C ─────────┘                          └───────── Consequence 3
```

**Key insight:** Prevention controls act on the left side (causes). Mitigation controls act on the right side (consequences). Most businesses only plan mitigation — they should also plan prevention.

**Worked example: Crop failure (agriculture business)**
```
Causes:                               Consequences:
Drought/dry spell ──────┐             ┌──── Revenue shortfall (UGX X)
Pest outbreak ──────────┼──[CROP]─────┼──── Working capital crisis
Input supply failure ───┘  FAILURE    └──── Loan default risk

Prevention controls:           Mitigation controls:
- Irrigation system            - Crop insurance policy
- IPM pest monitoring          - Emergency credit facility
- Certified seed use           - Diversified income sources
- Early warning monitoring     - Government relief programmes
```

---

## 3. Risk Assessment Matrix (Raydugin, Murray-Webster)

### Standard 5×5 Probability-Impact Matrix

Rate each risk on Likelihood (1–5) and Impact (1–5). Score = Likelihood × Impact.

| | **1-Rare** | **2-Unlikely** | **3-Possible** | **4-Likely** | **5-Almost Certain** |
|---|---|---|---|---|---|
| **5-Critical** | 5 | 10 | 15 | 20 | **25** |
| **4-Major** | 4 | 8 | 12 | **16** | **20** |
| **3-Moderate** | 3 | 6 | **9** | **12** | 15 |
| **2-Minor** | 2 | 4 | 6 | 8 | 10 |
| **1-Negligible** | 1 | 2 | 3 | 4 | 5 |

**Scoring guide:**
- **Score 15–25 (Red — Critical):** Immediate action required; consider whether strategy is viable
- **Score 8–12 (Amber — High):** Active management plan with owner and deadline
- **Score 4–6 (Yellow — Medium):** Monitor regularly; contingency plan in place
- **Score 1–3 (Green — Low):** Accept; review periodically

### Impact Scale Definitions (adapt to business size)

| Score | Revenue Impact | Cash Flow Impact | Reputation Impact |
|---|---|---|---|
| 1 — Negligible | <1% of revenue | Minor timing issue | No external impact |
| 2 — Minor | 1–5% of revenue | 1–2 weeks delay | Internal only |
| 3 — Moderate | 5–15% of revenue | 1–2 months | Local press/customer complaints |
| 4 — Major | 15–30% of revenue | >3 months | Regulatory action |
| 5 — Critical | >30% or business failure | Business-threatening | Permanent reputational damage |

---

## 4. Five Risk Addressing Strategies (Raydugin)

Once risks are assessed, select one of five addressing strategies for each:

### 1. AVOID
Eliminate the cause of the risk entirely by changing the plan.
> Example: "We will not enter the Northern Uganda market in Year 1, eliminating the security risk until the business is established."
- Best for: High-likelihood, high-impact risks where mitigation is too costly
- Cost: Often means giving up opportunity

### 2. REDUCE/MITIGATE
Take proactive action to reduce likelihood, impact, or both.
> Example: "We will install a solar backup system to reduce the impact of power outages from 8 hours/day to <30 minutes/day."
- Best for: Risks that are worth taking but need management
- Cost: Investment in controls, redundancy, training

### 3. TRANSFER
Shift the financial consequence of the risk to another party.
> Example: "We will purchase crop insurance to transfer the financial risk of drought to the insurer."
> Example: "Fixed-price contracts with suppliers transfer input cost inflation risk."
- Best for: Insurable risks or risks manageable through contract
- Cost: Insurance premiums, contract terms

### 4. ACCEPT (Passive)
Acknowledge the risk and take no pre-emptive action; deal with it if it occurs.
> Example: "We accept the risk of minor regulatory changes and will adapt as required."
- Best for: Low-score risks where mitigation cost exceeds potential loss
- Key requirement: Document the acceptance explicitly — never silently ignore a risk

### 5. EXPLOIT (Opportunity)
Increase likelihood of a positive uncertainty (upside risk = opportunity).
> Example: "We will increase our marketing budget if early demand signals are stronger than projected, to exploit the market faster."
- Best for: When a favourable scenario is possible and the business has capacity to capture it
- Note: Opportunities are risks too — manage them actively

---

## 5. Behavioural Biases in Risk Assessment (Murray-Webster)

**Critical insight:** Risk identification and assessment are profoundly affected by cognitive biases. Identify and counteract them.

### Triple Strand of Influences on Risk Perception

| Strand | Description | Business Example |
|---|---|---|
| **Conscious** | Observable factors: proximity, urgency, manageability | "This risk feels manageable because I've faced it before" — may understate it |
| **Subconscious (Heuristics)** | Mental shortcuts: availability bias, anchoring, representativeness | "We won't fail — no one in this sector has" — availability bias ignoring base rates |
| **Affective** | Emotional response: fear, excitement, hope | "This is our dream business" — optimism bias inflating opportunity, deflating risk |

### Key Heuristics to Watch (Murray-Webster)

| Bias | Description | Risk Management Error |
|---|---|---|
| **Availability bias** | Weight most memorable events most heavily | Overestimate risks that recently happened nearby; underestimate unfamiliar risks |
| **Optimism bias** | Believe you will beat the average | Underestimate costs, timelines, competitive response |
| **Proximity bias** | Prioritise immediate/close risks over distant ones | Ignore long-term risks (climate, market shift) |
| **Manageability bias** | Prefer risks you feel you can handle | Underestimate truly novel risks |
| **Anchoring** | Over-rely on first information received | Financial projections anchored to early assumptions even when evidence changes |
| **Group think** | Groups converge to consensus, suppressing dissent | Risk workshops miss contrarian views |

### Counteracting Bias in Business Plans

1. **Use multiple identification methods** — checklists, expert input, industry benchmarks — not just founder intuition
2. **Seek independent review** — ask someone outside the team to challenge risk scores
3. **Use base rates** — how often do businesses like this fail, and why?
4. **Separate identification from assessment** — list all risks first before scoring any
5. **Include upside risks** — risks you might exploit, not just threats to manage

---

## 6. Risk Register Design (Raydugin)

A complete risk register for a business plan should contain:

| Column | Content |
|---|---|
| Risk ID | Unique reference number (R001, R002...) |
| Risk Description | Three-part format: Cause → Event → Impact |
| Risk Category | Market / Financial / Operational / Strategic / Regulatory |
| Likelihood (L) | 1–5 score |
| Impact (I) | 1–5 score |
| Risk Score (L×I) | 1–25 |
| Priority | Red / Amber / Yellow / Green |
| Addressing Strategy | Avoid / Reduce / Transfer / Accept / Exploit |
| Response Action | Specific action, not vague ("monitor the risk") |
| Action Owner | Named person responsible |
| Target Date | When action will be complete |
| Residual Likelihood | After action |
| Residual Impact | After action |
| Residual Score | After action |
| Monitoring Trigger | What signal indicates the risk is materialising |
| Contingency Plan | What to do if the risk materialises despite prevention |

**Common pitfalls (Murray-Webster):**
- Confusing **risks** (uncertain future events) with **issues** (problems that have already occurred)
- A risk register full of cobwebs — created once, never updated
- Vague response actions: "we will monitor this risk" is not a response
- No ownership — risks assigned to "management" rather than a named individual

---

## 7. Supercritical Risks (Raydugin)

Some risks score so high (typically 20–25 on the 5×5 matrix) that they require special treatment beyond the standard risk register:

**Supercritical risk = any risk that could cause project/business failure on its own**

Management of supercritical risks requires:
1. **Escalation** — management and investor review, not just operational response
2. **Dedicated response plan** — separate workstream with dedicated resources
3. **Executive ownership** — CEO/Director personally responsible, not delegated
4. **Early warning system** — specific triggers defined well in advance
5. **Go/No-Go decision gate** — if the risk cannot be reduced below critical threshold, reconsider the venture

> **Business plan implication:** If your risk analysis identifies a supercritical risk (score 20+) with no credible mitigation, this is a showstopper that must be addressed before the plan is financed.

---

## 8. Risk Communication in Business Plans

### What Investors and Lenders Expect

Investors trust founders who acknowledge risks honestly. The risk analysis section should:

1. **Show you've done the thinking** — systematic identification, not a superficial list of 5 generic risks
2. **Quantify where possible** — "cost overrun risk of UGX 15M" is more credible than "cost risk"
3. **Demonstrate mitigation** — every high/critical risk needs a credible, specific response
4. **Show residual risk** — after mitigation, what is the remaining exposure?
5. **Signal risk appetite alignment** — the business takes informed, bounded risks, not reckless ones

### Risk Disclosure Structure for a Business Plan

```
1. Risk identification methodology (how did you identify risks?)
2. Priority risks (top 5–8, described in three-part format)
3. Risk register summary (matrix showing all risks by category)
4. Mitigation plan (specific actions for each high/critical risk)
5. Insurance coverage (what is transferred)
6. Monitoring framework (how will you track risks ongoing?)
7. Contingency reserves (financial buffer for residual risk)
```

---

## 9. Contingency Reserves

| Reserve Type | Purpose | Typical Amount |
|---|---|---|
| **Known-unknown reserve** | Budgeted for identified risks that may or may not materialise | 5–15% of project cost |
| **Unknown-unknown reserve** | Management reserve for unforeseen events | 2–10% of total budget |
| **Working capital buffer** | Cash to survive revenue shortfall | 2–3 months of fixed costs |

> **Rule of thumb (Raydugin):** Never present financial projections without a contingency line. Its absence signals naivety.

---

## 10. Citation Format

- Three-part naming, bowtie diagrams, 5 addressing strategies, risk register, supercritical risks, PETRA: (Raydugin, *Project Risk Management*, Wiley, 2013)
- Behavioural biases (triple strand, heuristics), risk appetite, risk communication pitfalls, 10 golden guidelines: (Murray-Webster & Pullan, *Making Risk Management Work*, 2nd ed., Routledge)
- ERM framework, COSO, risk categories, risk maturity: (Olson & Wu, *Enterprise Risk Management Models*, 2nd ed., Springer, 2017)
