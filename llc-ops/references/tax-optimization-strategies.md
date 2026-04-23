# Tax Optimization Strategies

Expert-level tax planning for single-member LLCs in software/consulting.

## The Big Picture

As a single-member LLC owner, you face **two** taxes on business profits:

1. **Self-Employment Tax (SE):** 15.3% (Social Security 12.4% + Medicare 2.9%)
2. **Income Tax:** 10-37% depending on bracket

Combined, you could be paying 37-52% on business profits. The strategies below legally reduce this burden.

---

## Strategy 1: S-Corp Election

**What it does:** Splits your business income into "salary" (subject to SE tax) and "distributions" (not subject to SE tax).

### The Math

**Without S-Corp (Default SMLLC):**
```
Net Profit: $100,000
SE Tax (15.3%): $15,300
Income Tax (22% bracket): $22,000
Total Tax: $37,300
Effective Rate: 37.3%
```

**With S-Corp ($50k salary, $50k distribution):**
```
Salary: $50,000
  Payroll Tax (15.3%): $7,650
  Income Tax (22%): $11,000
Distribution: $50,000
  SE Tax: $0
  Income Tax (22%): $11,000
Total Tax: $29,650
Savings: $7,650
```

### Break-Even Analysis

| Annual Profit | S-Corp Worth It? | Reason |
|---------------|------------------|--------|
| <$40k | No | Savings < complexity cost |
| $40-50k | Maybe | Break-even zone |
| $50-80k | Likely | Clear savings |
| >$80k | Yes | Significant savings |

### S-Corp Requirements

1. **Reasonable Salary:** IRS requires you pay yourself a "reasonable" salary. For software consultants, industry benchmarks suggest 60-70% of profits up to ~$100k.

2. **Payroll Processing:** Must run actual payroll. Options:
   - Gusto (~$40/month + $6/employee)
   - QuickBooks Payroll (~$50/month)
   - Wave Payroll (free in some states)

3. **Additional Filings:**
   - Form 1120-S (S-Corp return)
   - Schedule K-1 (to yourself)
   - Quarterly payroll filings (941)
   - Annual W-2 (to yourself)

### Timeline to Elect

- **By March 15** of the tax year you want it effective
- **Or within 75 days** of formation
- File **Form 2553** with IRS

### When NOT to Elect S-Corp

- Income is variable/uncertain
- Already have W-2 job with high withholding
- Don't want payroll complexity
- Planning to take on investors (complicates)

---

## Strategy 2: QBI Deduction (Section 199A)

**What it does:** Deduct 20% of Qualified Business Income from taxable income.

### Eligibility

| Income Level (Single) | Software/Consulting Eligible? |
|-----------------------|------------------------------|
| Below $182,100 (2024) | Yes, full 20% |
| $182,100 - $232,100 | Phased out (SSTB rules) |
| Above $232,100 | No (specified service trade) |

**Software consulting is a "Specified Service Trade or Business" (SSTB)**, which means the deduction phases out at higher incomes.

### The Math

```
Qualified Business Income: $80,000
QBI Deduction (20%): $16,000
Tax Savings (22% bracket): $3,520
```

### Maximizing QBI

1. Keep income below threshold if possible (timing strategies)
2. QBI is calculated AFTER S-Corp salary (for S-Corp owners)
3. Keep business expenses reasonable (inflated expenses reduce QBI)

---

## Strategy 3: Retirement Contributions

**What it does:** Tax-deductible contributions reduce taxable income NOW, grow tax-free, taxed later in retirement.

### Options Compared (2024)

| Vehicle | Contribution Limit | Best For |
|---------|-------------------|----------|
| **SEP IRA** | 25% of net SE income, max $69,000 | Simple setup, high earners |
| **Solo 401(k)** | $23,000 employee + 25% employer, max $69,000 | Maximum flexibility |
| **HSA** | $4,150 (individual) | Triple tax advantage |
| **Traditional IRA** | $7,000 | Low income years |

### SEP IRA Deep Dive

**Pros:**
- Easy to set up (Vanguard, Fidelity, Schwab)
- No annual filings
- Contribute up to filing deadline (+ extensions)
- High limits

**Cons:**
- Only employer contributions (no employee catch-up)
- Can't do Roth version
- Must include employees if you ever have any

**Contribution Calculation:**
```
Net Self-Employment Income: $100,000
Less: 50% of SE Tax: -$7,065
Adjusted: $92,935
SEP Contribution (25%): $23,234
```

### Solo 401(k) Deep Dive

**Pros:**
- Both employee AND employer contributions
- Roth option available
- Loan provision possible
- Higher effective contribution rate

**Cons:**
- More complex setup
- Annual filing (Form 5500-EZ) if >$250k
- Must establish by Dec 31 (can't wait until tax time)

**Contribution Calculation:**
```
Net Self-Employment Income: $100,000
Employee Contribution: $23,000 (direct)
Employer Contribution (25%): $23,234
Total: $46,234
```

### HSA (Triple Tax Advantage)

If you have a High Deductible Health Plan:
1. **Tax-deductible** contributions
2. **Tax-free** growth
3. **Tax-free** withdrawals for medical expenses

2024 Limits:
- Individual: $4,150
- Family: $8,300
- Catch-up (55+): +$1,000

---

## Strategy 4: Equipment & Depreciation

### Section 179 (Immediate Expense)

Deduct full cost of equipment in year purchased.

**2024 Limits:**
- Maximum deduction: $1,160,000
- Phase-out threshold: $2,890,000
- Qualifying: Computers, office equipment, software, vehicles (limited)

**When to Use:**
- Need deduction this year
- Income is high this year
- Equipment clearly for business

### Bonus Depreciation

Additional first-year depreciation beyond normal schedule.

| Year | Bonus Depreciation |
|------|-------------------|
| 2024 | 60% |
| 2025 | 40% |
| 2026 | 20% |
| 2027 | 0% |

**Strategy:** If considering large equipment purchase, sooner = better for depreciation.

### De Minimis Safe Harbor

Items ≤$2,500 can be expensed immediately without depreciation.

**Examples:**
- $2,000 monitor = expense immediately
- $3,000 laptop = should capitalize (but Section 179 available)

---

## Strategy 5: R&D Tax Credit

**What it does:** Credit (not just deduction) for qualified research activities.

### For Software Companies

**Qualified Activities:**
- Developing new software functionality
- Creating or improving algorithms
- Building experimental prototypes
- Resolving technical uncertainty

**NOT Qualified:**
- Routine bug fixes
- UI/UX tweaks without technical innovation
- Adaptation for individual customers

### For Startups (<$5M revenue)

Can apply up to **$250,000** against payroll taxes (Form 8974).

### Documentation Required

- Project descriptions
- Time allocation by project
- Technical challenges encountered
- Wages for developers

**Recommendation:** Work with CPA experienced in R&D credits. The documentation is specific.

---

## Strategy 6: Timing Strategies

### Income Deferral

- Delay sending invoices until January
- Delay signing new contracts until new year
- Collect deposits instead of full payment

**Best when:** Current year income is high, expect lower next year.

### Expense Acceleration

- Prepay next year's subscriptions in December
- Make estimated tax payment in December (counts for current year)
- Buy equipment before year-end

**Best when:** Current year income is high, want to reduce taxable income.

---

## Strategy 7: Health Insurance Deduction

Self-employed individuals can deduct 100% of health insurance premiums.

**Includes:**
- Medical insurance
- Dental insurance
- Vision insurance
- Long-term care insurance (age-limited)

**Limitation:** Cannot exceed net self-employment income.

---

## Annual Tax Planning Calendar

| Month | Action |
|-------|--------|
| **January** | Review prior year, estimate current year income |
| **March** | S-Corp election deadline (if electing) |
| **April** | Q1 estimated tax, file or extend prior year |
| **June** | Q2 estimated tax, mid-year projection update |
| **September** | Q3 estimated tax, year-end planning begins |
| **October** | Equipment purchase decisions, retirement funding review |
| **November** | Finalize year-end moves, max retirement contributions |
| **December** | Last chance: Solo 401k establishment, final prepayments |

---

## Red Flags to Avoid

1. **Unreasonably low S-Corp salary** — IRS watches for this
2. **Personal expenses as business** — Never
3. **Aggressive R&D claims without documentation** — Easy audit target
4. **Missing estimated payments** — Penalty accumulates
5. **Commingling funds** — Can pierce LLC veil

---

## When to Get Professional Help

**Always consult CPA for:**
- S-Corp election decision
- R&D credit claims
- Multi-state issues
- Investment income complexity
- Significant income changes

**The cost of a good CPA ($500-2000/year) often pays for itself in tax savings and peace of mind.**
