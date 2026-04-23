# Financial Management

CFO-level financial operations for ID8Labs LLC.

## Core Principle

**Cash is king.** Revenue is vanity, profit is sanity, but cash is reality. Know where you stand at all times.

---

## Banking Structure

### Recommended Account Setup

```
┌─────────────────────────────────────────────────┐
│               ID8Labs LLC Banking               │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │  Operating  │  │ Tax Reserve │  │Emergency│ │
│  │   Account   │  │   Account   │  │  Fund   │ │
│  │             │  │             │  │         │ │
│  │ Day-to-day  │  │ 25-35% of   │  │ 3-6 mo  │ │
│  │ expenses    │  │ revenue     │  │expenses │ │
│  └─────────────┘  └─────────────┘  └─────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Operating Account

**Purpose:** All revenue in, all expenses out.

**Flow:**
1. Client payments deposited here
2. Move % to tax reserve immediately
3. Pay business expenses from here
4. Owner draws from here (after reserves)

### Tax Reserve Account

**Purpose:** Never scramble for tax money.

**Rule:** Transfer 25-35% of every deposit immediately.

| Income Level | Suggested Reserve |
|--------------|-------------------|
| <$50k | 25% |
| $50k-$100k | 30% |
| >$100k | 35% |

**Only withdraw for:**
- Quarterly estimated payments
- Annual tax payment
- CPA fees (it's tax-related)

### Emergency Fund

**Purpose:** Survive revenue gaps.

**Target:** 3-6 months of fixed expenses.

**Don't touch for:**
- Equipment purchases
- Growth investments
- "Good opportunities"

**Only touch for:**
- Actual emergencies (client disappears, health issue)
- After operating account exhausted

### Bank Recommendations

| Bank | Best For | Notes |
|------|----------|-------|
| **Mercury** | Tech startups | No fees, great dashboard, integrations |
| **Chase** | Physical access | Branch network, lending relationship |
| **Relay** | Multiple accounts | Easy sub-accounts, no fees |
| **Novo** | Small business | Simple, integrates with accounting |

---

## Cash Flow Management

### Key Metrics

```
Monthly Revenue          What came in
- Monthly Expenses       What went out
─────────────────────    ───────────
= Net Cash Flow          Are you growing or shrinking?

Cash Balance             What's in the bank now
÷ Monthly Expenses       What you spend per month
─────────────────────    ───────────
= Runway (months)        How long can you survive?
```

### Cash Flow Rhythm

**Weekly:**
- [ ] Check bank balance
- [ ] Note pending inflows (invoices due)
- [ ] Note pending outflows (bills due)

**Monthly:**
- [ ] Reconcile all transactions
- [ ] Calculate actual vs projected
- [ ] Update cash flow projection
- [ ] Review runway

**Quarterly:**
- [ ] Deep review of spending patterns
- [ ] Assess revenue trends
- [ ] Update annual projection
- [ ] Make estimated tax payment

### Simple Projection Template

```
Month:         Jan    Feb    Mar    Apr    ...

CASH IN
Revenue        $      $      $      $
Other          $      $      $      $
Total In       $      $      $      $

CASH OUT
Fixed Expenses
  - Software   $      $      $      $
  - Insurance  $      $      $      $
  - Other      $      $      $      $
Variable
  - Contractors$      $      $      $
  - Marketing  $      $      $      $
Taxes          $      $      $      $
Owner Draw     $      $      $      $
Total Out      $      $      $      $

Net Flow       $      $      $      $
End Balance    $      $      $      $
```

---

## Revenue Management

### Invoicing Best Practices

**Send invoices:**
- Immediately upon completion
- On milestone completion (for larger projects)
- On first of month (for retainers)

**Include:**
- Clear payment terms (Net 15, Net 30)
- Multiple payment methods (ACH preferred, credit card as backup)
- Late payment terms (if any)

**Standard terms for different clients:**
- Startups: 50% upfront, 50% on completion
- Established companies: Net 30
- Large enterprise: Net 30-60 (negotiate)

### Payment Methods

| Method | Cost | Speed | Best For |
|--------|------|-------|----------|
| ACH | ~$0 | 2-3 days | Regular clients |
| Wire | $15-30 | Same day | Large/urgent |
| Credit Card | 2.5-3% | Instant | Convenience |
| PayPal | 2.9% + $0.30 | Instant | International |
| Stripe | 2.9% + $0.30 | 2 days | Product payments |

**Recommendation:** Offer ACH as default, credit card for convenience (consider 3% surcharge).

### Revenue Recognition

**For services:**
- Recognize when services delivered
- Deposits are liabilities until earned
- Track earned vs unearned

**For tax purposes (cash basis):**
- Count when payment received
- Doesn't matter when invoiced

---

## Expense Management

### Fixed vs Variable

**Fixed (predictable monthly):**
- Software subscriptions
- Insurance
- Hosting/infrastructure
- Any ongoing tools

**Variable (changes month to month):**
- Contractors
- Marketing spend
- Travel
- Equipment

### Expense Review Cadence

**Monthly:**
- Review all charges
- Identify unused subscriptions
- Categorize for taxes

**Quarterly:**
- Cancel unused tools
- Negotiate annual deals (often 10-20% savings)
- Review contractor ROI

**Annually:**
- Full subscription audit
- Insurance review
- Renegotiate major vendors

### Subscription Audit Template

| Service | Cost/mo | Essential? | Last Used | Action |
|---------|---------|------------|-----------|--------|
| Supabase | $25 | Yes | Daily | Keep |
| Tool X | $49 | No | 2mo ago | Cancel |
| Tool Y | $99 | Maybe | Weekly | Review |

---

## Owner Draws (Paying Yourself)

### As Disregarded Entity (Default SMLLC)

**Legal structure:**
- All profit is "pass-through" — it's your money
- No formal payroll required
- Transfer from business to personal = "owner draw"

**Process:**
1. Ensure tax reserve funded
2. Ensure emergency fund adequate
3. Transfer remaining to personal

**Record keeping:**
- Track all draws
- Keep consistent schedule if possible
- Document as "owner draw" not "salary"

### If Elected S-Corp

**Must have formal payroll:**
- "Reasonable salary" runs through payroll
- FICA/withholding deducted
- Remaining profit taken as "distribution"

**Process:**
1. Run payroll (salary portion)
2. Take distributions (profit portion)
3. Record separately for taxes

---

## Runway Management

### Calculating Runway

```
Cash on Hand: $50,000
Monthly Fixed Expenses: $3,000
Monthly Variable (average): $2,000
Monthly Total: $5,000

Runway = $50,000 ÷ $5,000 = 10 months
```

### Runway Targets

| Runway | Status | Action |
|--------|--------|--------|
| >12 months | Healthy | Normal operations |
| 6-12 months | Adequate | Monitor closely |
| 3-6 months | Warning | Reduce expenses, accelerate revenue |
| <3 months | Critical | Emergency mode, cut non-essential |

### Extending Runway

**Revenue side:**
- Accelerate invoicing
- Offer discount for early payment
- Pursue quick-win projects

**Expense side:**
- Pause non-essential subscriptions
- Delay equipment purchases
- Reduce owner draw

**External:**
- Line of credit (establish before you need it)
- Payment terms with vendors

---

## Financial Health Metrics

### Monthly Dashboard

| Metric | Target | Actual |
|--------|--------|--------|
| Revenue | $ | $ |
| Net Profit | $ | $ |
| Profit Margin | % | % |
| Cash Balance | $ | $ |
| Runway (months) | 6+ | |
| Tax Reserve | $ | $ |
| Collected vs Billed | % | % |

### Warning Signs

**Revenue:**
- Single client >50% of revenue (concentration risk)
- Declining month-over-month
- Long collection times (>45 days)

**Expenses:**
- Expense ratio increasing
- Subscriptions growing faster than revenue
- Contractor costs exceeding value

**Cash:**
- Runway shrinking
- Tax reserve raided
- Owner draw exceeding sustainable level

---

## Working with Professionals

### Bookkeeper vs CPA vs CFO

| Role | What They Do | When You Need |
|------|--------------|---------------|
| **Bookkeeper** | Categorize transactions, reconcile, basic reports | Revenue >$50k or you hate it |
| **CPA** | Tax strategy, tax filing, compliance | Always (at least for taxes) |
| **CFO** | Financial strategy, fundraising, major decisions | Revenue >$500k or fundraising |

### Finding a Good CPA

**Look for:**
- Experience with small businesses
- Proactive, not just reactive
- Responsive communication
- Fixed-fee for annual return
- Available for questions year-round

**Red flags:**
- Only talks to you at tax time
- Doesn't explain things
- Very cheap (you get what you pay for)
- Not interested in your business

**Cost estimate:** $500-$2,000/year for Schedule C filing and basic guidance.

---

## Tools & Automation

### Recommended Stack

| Function | Tool | Cost |
|----------|------|------|
| Banking | Mercury, Chase | Free-$15/mo |
| Invoicing | Wave, Stripe Invoicing | Free-3% |
| Expense Tracking | Wave, Copilot | Free-$15/mo |
| Accounting | Wave (free), QuickBooks | Free-$30/mo |
| Receipt Capture | Dext, Expensify | $12-20/mo |

### For Solo Consultant (Keep It Simple)

**Minimum viable stack:**
1. Business bank account (Mercury)
2. Invoicing (Wave — free)
3. Expense tracking (spreadsheet or Wave)
4. Receipt photos (organized folder)

**Don't need:**
- Complex accounting software
- Payroll (until S-Corp)
- Separate bookkeeper (initially)

---

## Quarterly Financial Checklist

- [ ] All transactions categorized
- [ ] Receipts captured for >$75 expenses
- [ ] Cash flow projection updated
- [ ] Runway calculated
- [ ] Tax reserve adequate
- [ ] Estimated tax payment made
- [ ] Owner draws recorded
- [ ] Unusual expenses flagged for CPA
