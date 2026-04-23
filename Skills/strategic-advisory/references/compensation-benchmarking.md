---
authority_level: secondary
effective_from: evergreen
last_verified: 2026-03-18
jurisdiction: federal
---

# Executive and Officer Compensation Benchmarking

**Purpose:** Methodology for benchmarking executive compensation in closely-held corporations to establish and defend reasonable compensation levels.

**Tier:** 3 (evergreen, no year indexing needed)

**Skills that reference this:** `fp-compensation-analysis`, `tx-officer-compensation`, `fp-strategic-advisory`

---

## Why Compensation Benchmarking Matters

Officer compensation in closely-held corporations sits at the intersection of tax compliance, audit defense, and talent retention. The IRS actively scrutinizes officer pay because the incentives for manipulation are structural:

- **C-corps** are incentivized to pay **higher** compensation — every dollar of officer salary is deductible, reducing double taxation (corporate tax on income + personal tax on dividends). Excessive compensation may be recharacterized as a non-deductible dividend under IRC 162(a)(1)
- **S-corps** are incentivized to pay **lower** compensation — distributions avoid FICA taxes (12.4% Social Security + 2.9% Medicare). Unreasonably low compensation triggers IRS reclassification of distributions as wages, plus penalties

A documented compensation benchmarking analysis is the primary defense in either scenario.

---

## IRS Reasonable Compensation Framework

### The 9-Factor Test

From the IRS Reasonable Compensation Job Aid (LB&I) and supporting case law:

1. **Training and education** — Formal education, professional certifications (CPA, PE, JD), specialized training relevant to the role
2. **Duties and responsibilities** — Scope of authority, reporting structure, number of direct reports, decision-making power
3. **Time and effort devoted** — Hours per week, full-time vs. part-time, seasonal variation; document with time records if possible
4. **Comparable compensation** — What similar positions pay in similar companies (the core of benchmarking)
5. **Revenue and complexity of the business** — Larger, more complex businesses justify higher compensation
6. **Nature and scope of work** — Range of functions performed; officer wearing multiple hats (CEO + CFO + sales) can justify aggregate compensation for all roles
7. **Compensation history** — Consistency over time; dramatic swings without business justification attract scrutiny
8. **Compensation relative to non-shareholder employees** — Extreme disparity (officer earns 20x the next-highest employee) is a red flag
9. **Compensation agreements** — Written employment contracts and board resolutions established before services are rendered carry significant weight

### The Independent Investor Test

Established in *Exacto Spring Corp v. Commissioner* (7th Cir. 1999): Would a hypothetical independent investor (outside shareholder with no control over compensation decisions) be satisfied with the return on equity after officer compensation is deducted?

- If compensation consumes all or nearly all corporate profits, leaving no return for shareholders, the compensation is likely excessive
- This test is particularly relevant for C-corps where the officer is also the controlling shareholder
- Calculate: (Net income after compensation) / shareholder equity = implied ROE. Compare to risk-adjusted market returns

---

## Data Sources for Compensation Benchmarking

### Tier 1: Government Data (Free, Authoritative)

- **BLS Occupational Employment and Wage Statistics (OES)** — Median and percentile wages by Standard Occupational Classification (SOC) code and metropolitan statistical area. Updated annually. Best free source for geographic-specific salary data. Available at bls.gov/oes
- **BLS Employment Cost Index** — Tracks compensation cost trends over time; useful for adjusting historical benchmarks to current dollars

### Tier 2: Commercial Compensation Databases

- **ERI Economic Research Institute** — Executive Compensation Assessor provides salary data by job title, industry, geography, and company revenue. Widely accepted by IRS examiners. Subscription-based
- **Salary.com CompAnalyst** — Market pricing tool with job-matched salary data. Covers executive and non-executive positions. Subscription-based
- **RCReports** — Specifically designed for reasonable compensation analysis in closely-held businesses. Produces IRS-ready reports. Per-report pricing available

### Tier 3: Free Supplemental Sources

- **Robert Half Salary Guide** — Published annually, free download. Covers accounting, finance, technology, and administrative positions. Useful as corroboration, not primary source
- **SEC Proxy Statements (DEF 14A)** — Executive compensation disclosure for public companies. Free via EDGAR. Useful for comparable company analysis when the client's industry has public peers
- **Trade association salary surveys** — Industry-specific data (e.g., AICPA compensation survey for accounting firms). Quality and availability vary by industry
- **Glassdoor, PayScale, LinkedIn Salary** — Crowdsourced data. Low reliability for IRS defense but useful for quick directional checks

---

## Benchmarking Methodology

### Step 1: Define the Position(s)

- Map the officer's actual duties to one or more standard job titles (SOC codes for BLS data, equivalent titles for commercial sources)
- For officers wearing multiple hats, identify each functional role separately: CEO duties, CFO duties, VP Sales duties, technical/production duties
- Document time allocation across roles (e.g., 40% executive management, 30% financial oversight, 30% client-facing sales)

### Step 2: Select Comparable Companies

- Match by industry (NAICS code, ideally 4-6 digit)
- Match by revenue size band — a CEO of a $2M company is not comparable to a CEO of a $200M company
- Match by geographic market — adjust for cost-of-living differentials between markets
- Match by company maturity — startup vs. established operations
- Document the selection rationale for each comparable

### Step 3: Apply Adjustments

- **Geographic adjustment** — Use BLS area wage differentials or ERI geographic cost factors to normalize data to the client's market
- **Revenue/size adjustment** — Compensation scales with company size; apply size-adjustment factors from the data source or regression analysis
- **Industry adjustment** — Some industries (finance, technology) pay systematically more than others (retail, food service) for equivalent roles
- **Experience adjustment** — Officer with 25 years of industry experience commands a premium over one with 5 years
- **Multi-role premium** — Aggregate the market value of each role, weighted by time allocation. This is the strongest argument for above-median compensation in small companies

### Step 4: Establish the Range

- Present compensation as a range (25th to 75th percentile), not a single number
- The recommended compensation level should fall within this range
- Position within the range based on qualitative factors (exceptional performance, unique expertise, founder premium)

### Step 5: Document the Analysis

- Create a written compensation study that a third party (IRS examiner, Tax Court judge) can follow
- Include: data sources used, comparable selection criteria, adjustment factors applied, final range and recommended level, rationale for positioning within the range
- Retain the underlying source data (printouts, report excerpts) in the workpaper file

---

## Documentation Package

A defensible compensation file includes:

- **Board resolution** — Minutes documenting the board's review and approval of officer compensation, referencing the benchmarking analysis
- **Written employment agreement** — Signed before the tax year begins, specifying base salary, bonus formula, benefits, and any contingent compensation
- **Compensation study** — The benchmarking analysis described above
- **Job description** — Written description of duties, responsibilities, authority, and time commitment
- **Time records** — Especially important when the officer performs multiple roles or works part-time
- **Dividend history** — For C-corps, demonstrating that the corporation pays dividends (or accumulates earnings for a documented business purpose) supports the argument that compensation is not disguised dividends

---

## Form 1120 Schedule E Requirements

Schedule E requires disclosure for each officer:

- Name and SSN
- Percent of time devoted to business (full-time = 100%)
- Percent of stock owned (common and preferred, end of year)
- Amount of compensation (salary + bonus + other forms)

This data feeds IRS automated screening. Triggers include: zero compensation with significant revenue, compensation exceeding 50% of gross receipts, dramatic year-over-year swings, and amounts far above industry medians.

---

## Section 162(m) — $1M Deduction Cap

IRC 162(m) limits the deduction for compensation paid to "covered employees" of publicly traded corporations to $1M per person. Post-TCJA (2018+), this covers the CEO, CFO, and next three highest-paid officers, with no performance-based exception.

This provision is generally **not applicable** to private C-corps. However, be aware of it for clients considering an IPO or SPAC transaction — the limitation applies from the first year of public trading.

---

## Accounting System Integration Notes

- Officer compensation should post to a dedicated account (e.g., "Officers' Compensation" or "Officer Salaries"), separate from regular employee wages
- The accounting system's payroll module generates W-2s and handles tax deposit scheduling for officer wages. Invoke `qbo-integration:qbo-coa` for platform-specific account setup
- For reconstructed years without actual payroll processing: record as journal entries to compensation expense with memo documenting the basis for the amount
- Pull the **Profit & Loss** report filtered to compensation accounts to compute compensation-to-revenue and compensation-to-net-income ratios for the independent investor test
- Track officer compensation separately in the COA to populate Schedule E without manual extraction

---

## Decision Points

- **Single role vs. multi-role valuation:** For officers performing one clearly defined role, benchmark to that role directly. For officers wearing multiple hats (common in small companies), aggregate the weighted market value of each role — this consistently produces higher defensible compensation
- **When to commission a formal study:** For compensation above $200K in a company with under $2M revenue, or any time the compensation-to-revenue ratio exceeds industry norms. Also recommended before any year with a significant compensation increase (>15%)
- **How to handle zero-compensation years:** Report $0 on Schedule E. Document why (pre-revenue startup, inactive period, personal financial circumstances). For C-corps, the risk is lower than for S-corps, but imputed compensation is possible if the officer was actively working
- **C-corp optimization:** Higher compensation reduces corporate income (lower corporate tax) but increases payroll tax. The crossover analysis depends on the marginal corporate tax rate (21% flat post-TCJA) vs. combined FICA rate (15.3% up to the Social Security wage base, 2.9% above it)

---

## Authoritative References

- IRC 162(a)(1) — Deduction for reasonable salaries and compensation
- IRC 162(m) — Limitation on deduction for covered employee compensation
- Treas. Reg. 1.162-7 — Compensation for personal services
- Treas. Reg. 1.162-9 — Bonuses to employees
- Exacto Spring Corp v. Commissioner, 196 F.3d 833 (7th Cir. 1999) — Independent investor test
- Elliotts, Inc. v. Commissioner, 716 F.2d 1241 (9th Cir. 1983) — Multi-factor analysis
- IRS Reasonable Compensation Job Aid (LB&I) — irs.gov
- BLS Occupational Employment and Wage Statistics — bls.gov/oes
- RCReports — Reasonable compensation analysis tool (rcreports.com)
