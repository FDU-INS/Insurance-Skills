---
authority_level: secondary
effective_from: evergreen
last_verified: 2026-03-18
jurisdiction: N/A
---

# Business Insurance Adequacy Review

**Purpose:** Procedures for evaluating, gap-analyzing, and advising on business insurance coverage for C-corporation advisory clients.

**Tier**: 3 (evergreen, no year indexing needed)

**Skills**: `fp-insurance-review`, `fp-risk-advisory`, `fp-coverage-gap-analysis`

---

## Overview

Insurance adequacy review ensures a business carries sufficient coverage to protect against material risks without overpaying for redundant or misaligned policies. For C-corps, the review covers mandatory coverage (workers' comp, unemployment), core commercial lines, and specialized policies driven by the entity's industry, asset base, and contractual obligations.

---

## Core Coverage Types for C-Corps

- **General Liability (GL):** Third-party bodily injury, property damage, personal/advertising injury, medical payments. Foundation of any commercial program. Typical limits: $1M per occurrence / $2M aggregate.
- **Commercial Property:** Buildings, equipment, inventory, furniture — fire, wind, hail, vandalism, theft. Confirm valuation basis (replacement cost vs. actual cash value). Watch for sublimits on flood, earthquake, equipment breakdown.
- **Business Owners Policy (BOP):** Bundles GL and commercial property at lower combined premium. Common for small to mid-size C-corps. May include business interruption. Not available for all industries or revenue sizes.
- **Workers' Compensation:** State-mandated for businesses with employees. Medical expenses and lost wages for work-related injuries. Premiums based on payroll, job classification codes, and experience modification rate (EMR).
- **Commercial Auto:** Required if the business owns, leases, or uses vehicles. Covers liability, collision, comprehensive, uninsured/underinsured motorist. Hired and non-owned auto endorsement covers employee use of personal vehicles.
- **Umbrella / Excess Liability:** Additional liability limits above GL, commercial auto, and employers' liability. Typical increments: $1M to $10M. Cost-effective way to increase total protection.

---

## Specialized Coverage

- **Directors & Officers (D&O):** Personal liability protection for directors/officers for decisions in their corporate capacity. Critical for C-corps with outside directors, investors, or securities exposure.
- **Errors & Omissions (E&O / Professional Liability):** Claims from professional services — negligence, mistakes, failure to deliver. Required for service-based businesses. Some client contracts mandate minimum E&O limits.
- **Cyber Liability:** Data breach response, notification expenses, regulatory fines, business interruption from cyber events. Sublimits on ransomware and social engineering are common — review carefully.
- **Employment Practices Liability (EPLI):** Wrongful termination, discrimination, harassment, retaliation claims. Risk scales with headcount. Defense costs alone can be significant even when claims lack merit.
- **Key Person Life Insurance:** Financial loss from death or disability of a critical individual. Company owns the policy and is beneficiary. See valuation methods and tax treatment below.
- **Business Interruption / Business Income:** Lost revenue and continuing fixed expenses during disruption by a covered peril. Often included in BOP or commercial property. Requires careful calculation of coverage amount and waiting period.

---

## Coverage Gap Analysis Methodology

1. **Inventory assets and risks** — List all physical assets (property, equipment, vehicles, inventory), intangible assets (data, IP, reputation), human capital (key employees), and contractual obligations (leases, client agreements, loan covenants)
2. **Map to existing policy coverage** — For each risk, identify which current policy responds, with what limits, deductibles, and exclusions
3. **Identify gaps** — Risks with no coverage, inadequate limits, excessive deductibles, or exclusions that negate expected protection
4. **Quantify exposure** — Estimate the financial impact of each uncovered or underinsured risk (replacement cost, lost revenue, legal defense, regulatory penalties)
5. **Recommend adjustments** — Prioritize by severity and likelihood; present options with premium impact estimates

---

## Business Interruption Calculation

- **Revenue projection:** Estimate monthly revenue that would be lost during a disruption; use trailing 12-month average as baseline
- **Continuing expenses:** Fixed costs that continue during shutdown (rent, loan payments, insurance premiums, salaried payroll)
- **Extra expense coverage:** Additional costs to maintain operations during recovery (temporary space, equipment rental, overtime)
- **Waiting period / deductible:** Most policies impose a 48-72 hour waiting period before coverage begins; some use a dollar deductible instead
- **Coinsurance penalty:** If coverage amount is less than the required percentage (typically 80%) of actual business income, the insurer reduces the payout proportionally
- **Coverage period:** Match the indemnity period to realistic recovery time — 12 months is standard but may be insufficient for manufacturing or specialized operations

---

## Debt Covenant Insurance Requirements

Lenders frequently mandate specific coverage as affirmative covenants: commercial property covering collateral assets, GL with lender named as additional insured, key person life insurance on principals, business interruption covering debt service during disruption. Cross-reference with `fp/debt-covenant-analysis.md` for covenant monitoring procedures. Failure to maintain required insurance is a covenant breach that can trigger default.

---

## Key Person Insurance Valuation Methods

- **Multiple of compensation:** 5x to 10x annual salary plus benefits; simple but may not reflect actual economic contribution
- **Contribution to revenue:** Percentage of revenue directly attributable to the individual, projected over a replacement hiring timeline (typically 1-3 years)
- **Replacement cost:** Recruiting fees, training period, productivity ramp-up, and interim revenue loss during the transition
- **Lender-driven:** Some loan agreements specify minimum key person coverage amounts; these override internal valuation

---

## Annual Review Triggers

Reassess coverage adequacy whenever any of these occur: acquisition of significant new assets or equipment, new business locations or geographic expansion, revenue growth exceeding 20% year-over-year, new contracts with insurance requirements, mergers or acquisitions, changes in headcount, new regulatory requirements, prior-year claims experience, expiring policies approaching renewal.

---

## Common Underinsurance Triggers

- Property values appreciated but policy limits unchanged — especially real estate and specialized equipment
- Business revenue growth outpacing GL and umbrella limits
- Sublimits on specific perils (flood, cyber, terrorism) far below actual exposure
- Inventory or work-in-progress values exceeding reported amounts
- Contractor or subcontractor insurance gaps creating upstream liability
- New service lines introduced without updating E&O coverage scope

---

## Tax Treatment of Insurance Premiums

- **Generally deductible (IRC 162):** GL, commercial property, BOP, workers' comp, commercial auto, umbrella, D&O, E&O, cyber, EPLI, business interruption — ordinary and necessary business expenses
- **Key person life insurance — NOT deductible (IRC 264):** When the company is the policy owner and beneficiary, premiums are not deductible. However, death benefit proceeds are generally received tax-free (IRC 101), subject to transfer-for-value rules
- **Prepaid premiums:** If a policy period spans two tax years, the portion allocable to the subsequent year is a prepaid expense; deduct only the current-year portion (12-month rule under IRC 461 may apply for cash-basis taxpayers, but C-corps on accrual basis must always allocate)

---

## Accounting System Integration Notes

### Insurance Expense Tracking

- Create sub-accounts under Insurance Expense for each policy type (GL, Property, Workers' Comp, D&O, etc.) to enable per-category cost analysis. Invoke `qbo-integration:qbo-coa` for platform-specific account setup
- Record premiums when billed or paid depending on accounting method; for accrual-basis C-corps, accrue the expense over the policy period
- Tag policies with class or location if coverage varies by business segment

### Prepaid Insurance Amortization

- Record annual or multi-month premium payments to Prepaid Insurance (Other Current Asset)
- Create a recurring journal entry to amortize monthly: debit Insurance Expense, credit Prepaid Insurance
- At year-end, verify the Prepaid Insurance balance equals the unexpired portion of all active policies

### Reporting

- Run Profit and Loss by account detail filtered to insurance sub-accounts for annual coverage cost summary
- Compare year-over-year insurance expense to revenue for cost-as-percentage-of-revenue trend analysis

---

## Decision Points

- **BOP vs. standalone policies?** BOP is cost-effective for smaller C-corps but may have coverage caps that are inadequate for larger operations. Compare BOP limits against standalone GL + property quotes when revenue exceeds $5M or property values exceed $1M.
- **Claims-made vs. occurrence?** E&O and D&O are typically claims-made. Ensure tail coverage (extended reporting period) is purchased if switching carriers or if the policy lapses.
- **Self-insured retention (SIR) vs. deductible?** Higher SIR lowers premiums but requires the company to fund claims within the retention. Appropriate only if cash reserves support it.
- **Umbrella limit sizing?** Consider worst-case liability scenario (catastrophic injury, class action, regulatory penalty). Industry benchmarks and peer comparisons inform appropriate limits.
- **Cyber coverage scope?** Policies vary widely. Confirm coverage for ransomware, social engineering fraud, regulatory fines, and business interruption — not just data breach notification.

---

## References

- SBA — Get Business Insurance: sba.gov/business-guide/launch-your-business/get-business-insurance
- IRC 162 — Trade or Business Expenses (deductibility of insurance premiums)
- IRC 264 — Certain Amounts Paid in Connection with Insurance Contracts (non-deductibility of key person life premiums when company is beneficiary)
- IRC 101 — Certain Death Benefits (tax-free treatment of life insurance proceeds)
- IRMI (International Risk Management Institute) — coverage definitions and policy analysis: irmi.com
- III (Insurance Information Institute) — business insurance guides: iii.org/insurance-basics/business-insurance
- NAIC (National Association of Insurance Commissioners) — state regulatory requirements: naic.org
