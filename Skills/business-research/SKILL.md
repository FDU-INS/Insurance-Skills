---
name: business-research
description: Research advisor for ACT business setup — Pty Ltd registration, accountants, insurance, R&D tax incentive, family trusts, compliance, and migration. Use when the user asks about any business setup topic, costs, providers, or next steps.
---

# Business Setup Research Advisor

## When Triggered
- "Research [accountants/insurance/R&D/trusts/etc.]"
- "What do we need for [business setup area]?"
- "Compare [providers/options] for [business need]"
- "What are the costs for [setup step]?"
- "Help me prepare for [accountant meeting/ASIC registration/etc.]"
- "What's next for the Pty Ltd setup?"
- Any question about Australian business registration, tax, compliance

## Research Areas

### 1. Accountant Selection
- Compare startup accounting firms (Standard Ledger, Azure Group, William Buck, Pitcher Partners, Grant Thornton)
- Pricing models: fixed fee vs hourly vs percentage
- Key questions to ask during consultation
- R&D tax claim capability (software + physical)
- Xero integration and automation support
- NFP/charity compliance experience (for AKT)
- Reference: `references/accountant-comparison.md`

### 2. Pty Ltd Registration
- ASIC registration process and costs ($576)
- Director obligations and responsibilities
- Constitution options (replaceable rules vs custom)
- Shareholder structure with family trusts
- Company secretary requirements
- Registered office options
- Reference: `docs/legal/entity-structure.md` (Entity 3 section)

### 3. Family Trust Setup
- Discretionary trust structure and benefits
- Individual vs corporate trustee pros/cons
- Trust deed requirements and costs
- Beneficiary classes and distribution rules
- TFN and ABN for trusts
- ATO scrutiny areas (PCG 2021/4, Division 7A)
- Reference: `docs/legal/entity-structure.md` (Entities 4 & 5 section)

### 4. R&D Tax Incentive
- Eligibility criteria for <$20M turnover companies
- Refundable offset calculation (43.5% for base rate entities)
- AusIndustry registration process and timing
- Documentation requirements (contemporaneous records)
- Software R&D vs physical R&D claims
- International R&D (World Tour 2026)
- R&D consultant selection (flat fee vs percentage)
- Reference: `docs/legal/entity-structure.md` (R&D section)

### 5. Insurance
- Public liability ($20M for Harvest lease)
- Workers compensation (QLD WorkCover)
- Professional indemnity (Innovation Studio consulting)
- Product liability (Goods marketplace, Harvest food)
- D&O insurance (AKT directors)
- Cyber insurance (digital platforms)
- Contents/equipment insurance
- Provider comparison and quote sources

### 6. Banking
- Business account options (NAB, others)
- Trust account requirements
- Tax reserve account strategy
- Grant fund segregation
- Payment infrastructure (PayID, direct debit)

### 7. Employment & Payroll
- Employer registration with ATO
- Single Touch Payroll (STP) setup
- Super guarantee obligations (11.5% → 12%)
- Family member employment rules and ATO scrutiny
- Timesheet and documentation requirements
- Fair Work compliance for casual/part-time

### 8. Migration (Sole Trader → Pty Ltd)
- Subscription transfer checklist
- Contract novation process
- Grant funder notification
- IP assignment (codebases, brands, methodologies)
- Lease transfer (Harvest, Farm)
- ABN/GST transition

### 9. Compliance & Ongoing
- BAS lodgement schedule (quarterly)
- ASIC annual review ($310/yr)
- ACNC annual information statement (AKT)
- Company tax return timeline
- Trust tax return timeline
- Record keeping requirements (5 years)

### 10. Trademark & IP Protection
- Trademark registration process (IP Australia)
- Priority brands: Empathy Ledger, JusticeHub, ALMA
- Cost estimates ($250 per class per mark)
- Timeline (7-8 months to registration)
- Trade secret documentation (LCAA framework)

## Research Methodology

### For Provider Comparisons
1. Check existing research in `.claude/cache/agents/scout/` and `.claude/cache/agents/oracle/`
2. Web search for current pricing and reviews
3. Check Australian-specific requirements
4. Compare at least 3 providers
5. Summarise with recommendation + rationale

### For Regulatory Questions
1. Check ATO, ASIC, ACNC official sources first
2. Cross-reference with professional guidance (CPA, tax institutes)
3. Note any recent changes or upcoming deadlines
4. Flag areas that need accountant confirmation
5. Always include "accountant to confirm" disclaimer for tax advice

### For Cost Estimates
1. Get current published pricing where available
2. Note price ranges (low/high) not just single figures
3. Include hidden costs (e.g., ASIC late fees, amendment fees)
4. Calculate Year 1 vs ongoing annual costs
5. Compare DIY vs professional service costs

## Output Format

Research outputs should follow this structure:

```markdown
# [Topic] Research — [Date]

## Summary
[2-3 sentence overview]

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Comparison Table (if applicable)
| Option | Cost | Pros | Cons | Recommendation |
|--------|------|------|------|----------------|

## Recommendations
1. Primary recommendation with rationale
2. Alternative if primary doesn't work

## Next Steps
- [ ] Action item 1
- [ ] Action item 2

## Sources
- [Source 1](url)
- [Source 2](url)

## Caveats
- "Accountant to confirm" items flagged here
```

## Output Destination
Save research to: `.claude/cache/agents/scout/business-[topic]-[date].md`

## File References
| Need | Reference |
|------|-----------|
| Entity structure | `docs/legal/entity-structure.md` |
| Financial controls | `docs/finance/controls.md` |
| Compliance calendar | `docs/governance/compliance-calendar.md` |
| Decision making | `docs/governance/decision-making.md` |
| Privacy policy | `docs/privacy/empathy-ledger-privacy-policy.md` |
| Grant acquittal | `docs/finance/grant-acquittal-template.md` |
| Accountant comparison | `references/accountant-comparison.md` |
| Setup costs | Business page — Accountant & Costs section |

## Entity Context (Quick Reference)

```
EXISTING:
  Sole Trader (ABN 21 591 780 066) — WINDING DOWN
  A Kind Tractor LTD (ABN 73 669 029 341) — DORMANT CHARITY

TO CREATE:
  A Curious Tractor Pty Ltd — MAIN OPERATING ENTITY
  Ben's Family Trust — TAX-EFFICIENT DISTRIBUTIONS
  Nic's Family Trust — TAX-EFFICIENT DISTRIBUTIONS

SITES:
  The Harvest — leased from philanthropist, $20M PL required
  The Farm — leased from Nic, R&D site

REVENUE:
  Innovation Studio, JusticeHub, Harvest, Goods, Grants, Empathy Ledger

FOUNDERS:
  Ben Knight (director, operations, dev)
  Nic Marchesi (director, creative, community)
```
