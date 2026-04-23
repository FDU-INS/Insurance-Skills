# Output Format Templates

Templates for three depth levels and three cadences. Choose based on user preference — default to Standard Format at Monthly cadence.

---

## Standard Format (Default) — Monthly Cadence

```markdown
# 🛡️ DTC Life Insurance Landscape Brief

**Period**: [Start Date] – [End Date] ([N]-day lookback)
**Cadence**: [Weekly | Monthly | Quarterly]
**Sources Reviewed**: [N] items across [N] sources
**Generated**: [Current Date]
**Time Windows**: 📅 This Month ([N] items) · 🌱 Emerging ([N] items) · 🔭 Horizon ([N] items)

---

## Executive Summary

[5–8 sentences. Lead with the 3–5 most significant developments in DTC life insurance this period. State what happened, what it means for distribution and product strategy, and who should care. Written for a busy distribution executive, founder, or investor who may read only this section. Explicitly call out if any `[HORIZON]` regulatory items have moved closer to effect.]

---

## 🔗 Cross-Platform Highlights

Stories corroborated across 3+ independent sources — the strongest signals in this research.

### [Headline 1] `[Industry + Reddit + LinkedIn]` `[30d]`

**What happened**: [2–3 sentence overview]

**Why it matters for DTC**: [1–2 sentences on strategic significance for direct distribution]

**The conversation**: [What are practitioners or consumers actually saying? Quote a top Reddit comment or LinkedIn post directly.]

📊 **Signal**: [Engagement summary — e.g., "4 independent trade outlets covered, 287 upvotes on r/LifeInsurance, multiple LinkedIn executive reactions"]
🎯 **Distribution implication**: [What DTC operators should consider doing or watching]

---

### [Headline 2] `[Industry + X]` `[30d]`

[Same structure]

---

## 📅 This Month — Key Developments

*Primary findings within the current period. Ordered by impact.*

### [Headline] `[Primary source]` `[30d]`

**What happened**: [2–3 sentences]

**Why it matters**: [Why this is worth flagging — consumer impact, competitive shift, regulatory signal]

📊 **Signal**: [Source and engagement indicator]
🎯 **Implication**: [Actionable consideration for DTC practitioners]

---

## 📦 Product & Underwriting

### [Headline] `[30d]`

**Summary**: [One-sentence overview]

**Key Points**:
- [Detail 1]
- [Detail 2]
- [Detail 3]

**Impact**: [Scope: carriers / distributors / consumers | Magnitude: Incremental / Notable / Major / Market-shifting]
**Source**: [Attribution — per Insurance Journal, per carrier newsroom, per r/LifeInsurance]
**Distribution implication**: [What DTC operators should consider doing in response]

---

[Repeat for each finding within the category]

---

## 💻 Distribution & Technology

[Same structure — findings relevant to DTC platform innovation, embedded insurance, digital UX]

---

## 💰 Funding & M&A

[Same structure — insurtech funding, acquisitions, strategic partnerships]

---

## ⚖️ Regulation & Compliance

[Same structure — NAIC, state departments, federal legislation. Note effective dates prominently.]

---

## 📊 Market & Industry Data

[Same structure — LIMRA stats, AM Best data, industry surveys]

---

[Include only categories that have findings. Skip empty categories.]

---

## 💬 Consumer Sentiment Snapshot

*What real buyers, applicants, and policyholders are saying on Reddit and social — this period.*

**Where consumers are expressing friction**:
> "[Direct quote from top Reddit comment]" — r/LifeInsurance, [N] upvotes

> "[Direct quote from another top comment]" — r/personalfinance, [N] upvotes

**What consumers are saying about [specific carrier/product from research]**:
> "[Direct quote]" — r/LifeInsurance

**Emerging patterns** (recurring across multiple threads):
- **[Pattern 1]**: [Description — e.g., "Multiple threads report confusion about accelerated underwriting rescission conditions"]
- **[Pattern 2]**: [Description]

**Sentiment direction**: [Net positive / Negative / Mixed for DTC channel overall] — [1 sentence explanation]

---

## 🔭 Horizon — Regulatory Pipeline & Emerging Signals

*Proposed rules, pending legislation, early-stage developments, and `[HORIZON]`-tagged items not yet impacting operations. These are tomorrow's compliance requirements and strategic challenges.*

### [Regulatory Item Title] `[HORIZON]` `[NAIC | State | Federal]`

**Current status**: [Proposed | In comment period | Passed committee | Signed | Effective date pending]
**Affected parties**: [Carriers | Distributors | Agents | Consumers]
**Proposed effective date**: [Date or "TBD"]

**What it would require**: [1–2 sentences on the practical compliance requirement]

**Why flag it now**: [Lead time rationale — what actions can be taken now while it's still in pipeline]

**Watch for**: [Next milestone — e.g., "NAIC committee vote expected Q2 2026", "Comment period closes March 15"]

---

### [Early-Stage Trend] `[EMERGING]`

**What's building**: [1–2 sentences on the trend being observed]

**Evidence**: [What signals were found — subreddit discussion, multiple startup announcements, investor commentary]

**Timeline to mainstream**: [Early indicator / 1–2 years / 2–5 years]

**Strategic implication**: [What to watch or prepare for]

---

## 🎯 Strategic Takeaways

1. **[Finding]** — [What DTC distribution practitioners should consider doing about it]
2. **[Finding]** — [What DTC distribution practitioners should consider doing about it]
3. **[Finding]** — [What DTC distribution practitioners should consider doing about it]
4. **[Finding]** — [What DTC distribution practitioners should consider doing about it]
5. **[Finding]** — [What DTC distribution practitioners should consider doing about it]

---

[STATS BLOCK — see SKILL.md for format]

---

[FOLLOW-UP INVITATION — see SKILL.md for format]
```

---

## Standard Format — Weekly Variant

Adapt the monthly template with these changes:
- Time window label: **📅 This Week** instead of **This Month**
- Use `[7d]` tags throughout
- Shorten executive summary to 3–5 sentences (tighter cadence = tighter summary)
- **Skip** Market & Industry Data category unless LIMRA or ACLI released weekly data
- **Expand** the Cross-Platform Highlights section — weekly cadence should lead harder on breaking developments
- Consumer Sentiment Snapshot can be brief (3–5 notable comments vs. full pattern analysis)
- Horizon section still required — regulatory pipeline does not move at weekly cadence

---

## Standard Format — Quarterly Variant

Adapt the monthly template with these changes:
- Time window label: **📅 This Quarter** + **YTD Context** sub-section
- Use `[90d]` tags for current quarter findings
- Add a **YTD Context** sub-section after Executive Summary: 2–3 sentences placing the quarter in full-year context
- **Expand** Market & Industry Data — LIMRA publishes quarterly application activity; this is the anchor data point for quarterly briefs
- **Expand** Emerging Trends category — quarterly cadence reveals patterns not visible in weekly/monthly
- **Expand** Horizon section into a **Next Quarter Outlook** with 3–5 items to watch
- Add **Quarter-Over-Quarter Comparison** note in executive summary when prior period data is available
- Strategic Takeaways should number 7–10 items (broader coverage window = more takeaways)

---

## Brief Format (Headlines Only)

Use when user requests "just the headlines" or "quick brief".

```markdown
# 🛡️ DTC Life Insurance — [Monthly | Weekly | Quarterly] Headlines
**Period**: [Start] – [End] | **Generated**: [Date]

## Top Stories
1. **[Headline]** — [One sentence. Source.] `[30d]`
2. **[Headline]** — [One sentence. Source.] `[30d]`
3. **[Headline]** — [One sentence. Source.] `[7d]`
4. **[Headline]** — [One sentence. Source.] `[30d]`
5. **[Headline]** — [One sentence. Source.] `[EMERGING]`

## Regulatory Pipeline
- **[Item]** — [Status + one sentence on implication] `[HORIZON]`
- **[Item]** — [Status + one sentence on implication] `[HORIZON]`

## Consumer Sentiment Signal
- [One-sentence summary of Reddit/social mood this period]

## 3 Things to Watch
1. [Forward-looking item]
2. [Forward-looking item]
3. [Forward-looking item]

[STATS BLOCK — abbreviated]
```

---

## Deep Format

Activate when user requests "deep analysis" or "full strategic brief". Includes everything in Standard, plus:

**After Executive Summary**: Add **Market Context** section — 3–5 paragraphs setting the current DTC landscape, macro factors (interest rates, mortality trends, consumer financial stress), and how they shape the quarter's developments.

**After Categorized Findings**: Add **Competitive Intelligence** section — carrier-by-carrier positioning notes based on research findings. Explicitly name which carriers are gaining or losing ground on DTC capability, consumer sentiment, or regulatory standing.

**After Consumer Sentiment**: Add **Consumer Decision Journey Analysis** — based on Reddit research, map where consumers are entering, stalling, and exiting the life insurance funnel. What moments of confusion map to which categories of findings.

**Horizon section expanded**: Add forward-looking scenarios for the top 2–3 regulatory items. Scenario A (passes as proposed) / Scenario B (modified) / Scenario C (stalled). One paragraph each.

**Strategic Takeaways expanded to 10**: Include 3 carrier-level, 3 distribution/platform, 2 consumer-facing, 2 regulatory/compliance.

**Add Appendix**: Full list of sources reviewed with publication names and dates.
