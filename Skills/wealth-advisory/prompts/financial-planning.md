# Financial Planning & Advisory

## Role Context

```
You are a senior financial planner and wealth advisor with deep expertise in retirement
planning, Monte Carlo simulation, insurance analysis, education funding, and cash flow
optimization. You hold the CFP, ChFC, and CLU designations with 15+ years of experience
serving affluent families ($1M-$25M investable assets). You communicate complex concepts
clearly, always grounding recommendations in quantitative analysis while acknowledging
uncertainty. You consider tax implications in every recommendation and coordinate with
the client's CPA and estate attorney. You adhere to the fiduciary standard and disclose
conflicts of interest.
```

## What This Desk Does

The financial planning team builds comprehensive, goals-based plans that connect a client's current resources to their future objectives. Unlike pure investment management, financial planning integrates cash flow, tax projection, insurance, estate, and behavioral considerations into a unified roadmap. The team uses Monte Carlo simulation and scenario analysis to stress-test plans under thousands of market environments, providing probability-weighted guidance rather than deterministic forecasts. Every plan is a living document, updated as circumstances change -- market moves, tax law shifts, family events, or evolving goals.

---

## 1. Retirement Planning

Accumulation strategy, decumulation design, withdrawal rate analysis, and Social Security optimization.

**The 4% Rule and Its Variants:**

The original Bengen (1994) / Trinity Study finding: a 4% initial withdrawal rate, adjusted annually for inflation, survived all 30-year historical periods for a 50/50 stock/bond portfolio.

Key modifications for modern planning:
- **Guardrails approach** (Guyton-Klinger): increase/decrease withdrawals based on portfolio performance; typical band: 4% +/- 20% (3.2% floor, 4.8% ceiling)
- **Dynamic withdrawal**: spend a fixed percentage of current portfolio value each year (eliminates ruin risk but creates income volatility)
- **Required Minimum Distribution (RMD) method**: withdraw based on IRS life expectancy tables
- **Constant real spending**: traditional 4% rule, CPI-adjusted annually

**Present Value of Retirement Liability:**

PV = sum from t=1 to T of [ Annual_Spending_t / (1 + r)^t ]

Where:
- Annual_Spending_t = base spending x (1 + inflation)^t
- r = expected real return (nominal return - inflation)
- T = planning horizon (life expectancy + longevity buffer, typically age 95-100)

### Retirement Readiness Assessment

```
Assess retirement readiness for a client with the following profile:

- Current age: [age], planned retirement age: [retirement age]
- Current portfolio: $[amount] ([asset allocation breakdown])
- Annual retirement spending goal: $[amount] in today's dollars
- Social Security estimated benefit: $[monthly amount] at age [claiming age]
- Pension: $[amount/none], COLA-adjusted: [yes/no]
- Annual savings rate: $[amount] across [account types: 401k, IRA, taxable]
- Other income in retirement: [rental, part-time, annuity]

Perform the following analysis:
1. Retirement gap analysis: present value of spending needs vs. current + projected assets
2. Required return to close the gap (solve for r in PV equation)
3. Optimal Social Security claiming strategy:
   - Compare NPV of benefits at ages 62, FRA ([age]), and 70
   - Breakeven age between early and delayed claiming
   - Spousal benefit coordination if married
4. Tax bracket management: Roth conversion ladder strategy during "gap years" (retirement to RMD age)
5. Sequence of returns risk: how does a 30% drawdown in year 1 of retirement affect plan survival?
6. Three scenarios: base case, conservative (lower returns, higher inflation), and adverse (recession at retirement)
```

### Decumulation Strategy Design

```
A client is [age], recently retired, with the following assets:
- Tax-deferred (401k/IRA): $[amount]
- Roth IRA: $[amount]
- Taxable brokerage: $[amount]
- Cash/savings: $[amount]
- Social Security: $[monthly] starting at age [age]
- Annual spending need: $[amount], of which $[amount] is non-discretionary

Design an optimal decumulation strategy:
1. Account withdrawal sequencing:
   - Which accounts to draw from first to minimize lifetime tax burden?
   - Roth conversion opportunities before RMDs begin at age 73/75
   - Capital gains harvesting in low-income years
2. Guardrails withdrawal policy:
   - Initial withdrawal rate: [X]%
   - Upper guardrail (cut spending if portfolio drops): [X]%
   - Lower guardrail (increase spending if portfolio grows): [X]%
3. Cash reserve / bucket strategy:
   - Bucket 1 (0-2 years): cash and short-term bonds for near-term spending
   - Bucket 2 (3-7 years): intermediate bonds and balanced funds
   - Bucket 3 (8+ years): equities for long-term growth
4. RMD planning: project RMDs and their tax impact from age 73 to 95
5. Legacy and longevity: at what spending level is there a 90%+ probability of leaving $[target] to heirs?
```

---

## 2. Monte Carlo Simulation

Portfolio survival probability, confidence intervals, stress scenarios, and spending flexibility analysis.

**Monte Carlo Methodology:**

1. Define input distributions:
   - Expected return (mu) and volatility (sigma) for each asset class
   - Correlation matrix across asset classes
   - Inflation distribution (mean and standard deviation)
2. Generate N simulations (typically 1,000-10,000):
   - Each simulation: draw random annual returns from the defined distributions
   - Apply spending, taxes, contributions, and rebalancing each year
   - Track portfolio value through the full planning horizon
3. Measure outcomes:
   - Probability of success = (simulations where portfolio > $0 at end) / N
   - Percentile outcomes: 10th, 25th, 50th, 75th, 90th percentile terminal wealth
   - Shortfall magnitude: average deficit in failed scenarios

**Key Limitations:**
- Assumes returns are normally/lognormally distributed (fat tails underweighted)
- Historical correlations may not hold in stress periods
- Does not capture behavioral responses (panic selling, overspending)
- Garbage in, garbage out: output quality depends entirely on input assumptions

### Monte Carlo Plan Stress Test

```
Run a Monte Carlo simulation for the following retirement plan:

Portfolio: $[amount]
Allocation: [X]% equities (expected return [X]%, volatility [X]%), [X]% bonds (expected return [X]%, volatility [X]%), [X]% alternatives
Correlation between equities and bonds: [X]
Annual spending: $[amount], inflation-adjusted at [X]% per year
Time horizon: [X] years
Tax rate on withdrawals: [X]% (blended)
Additional income: $[amount] starting at year [X] (Social Security)

Provide:
1. Probability of success (portfolio survives full horizon) for:
   - Base spending level
   - Spending + 10% (upside lifestyle)
   - Spending - 15% (essential only)
2. Percentile distribution of terminal wealth (10th, 25th, 50th, 75th, 90th)
3. Worst-case analysis: what happens in the bottom 5% of scenarios?
4. Sensitivity analysis: which input variable has the greatest impact on success probability?
   (spending level, return assumption, inflation, time horizon)
5. Spending flexibility value: how much does a willingness to cut spending by 15% in bad years
   improve success probability?
6. Sequence of returns stress test: front-load a -30% equity return in year 1; how does this
   change the probability distribution?
```

### Scenario Planning Framework

```
A client is concerned about the following specific scenarios. For each, model the impact
on their financial plan (current portfolio: $[amount], annual spending: $[amount]):

1. Stagflation: 2% real returns, 5% inflation for 10 years, then normalization
2. Japan scenario: 0% nominal equity returns for 20 years, low inflation
3. High-growth: 10% nominal equity returns sustained for 15 years
4. Early health crisis: $[amount] in medical/LTC costs at age [X] for [Y] years
5. Longevity surprise: both spouses live to age 100

For each scenario, report:
- Plan success probability
- Median terminal wealth
- Required spending adjustment to maintain 85%+ success probability
- Recommended portfolio adjustment (if any)
```

---

## 3. Insurance Analysis

Life insurance needs, long-term care planning, disability coverage, and annuity evaluation.

**Human Capital Model:**

Human capital = present value of future earnings

HC = sum from t=1 to T of [ E(Income_t) x (1 - tax_t) x Survival_t / (1 + r)^t ]

Where:
- E(Income_t) = expected income in year t (growing at wage inflation)
- Survival_t = probability of being alive and working in year t
- r = personal discount rate
- Human capital declines over career; financial capital should increase to replace it

**Life Insurance Need:**
Life insurance need = PV(future obligations) - existing assets - survivor income
= PV(income replacement) + PV(education costs) + PV(debt payoff) + estate liquidity needs - current financial assets - survivor Social Security - group coverage

### Life Insurance Needs Analysis

```
Determine the appropriate life insurance coverage for a client:

- Age: [age], health: [standard/preferred/highly preferred]
- Annual income: $[amount], expected growth rate: [X]%
- Spouse income: $[amount/none]
- Children: [number], ages [ages]
- Mortgage balance: $[amount], other debts: $[amount]
- Current financial assets: $[amount]
- Existing group life coverage: $[amount]
- Education funding goal: $[amount per child]
- Desired income replacement: [X]% for [Y] years

Calculate:
1. Income replacement need using human capital model (PV of after-tax income through age [X])
2. Specific obligations: mortgage payoff + education funding + final expenses
3. Offset: existing assets + survivor Social Security + group coverage + spouse income
4. Net insurance need = total obligations - total offsets
5. Policy type recommendation:
   - Term (10/20/30 year) for temporary needs
   - Whole life / universal life for permanent needs (estate liquidity, charitable)
   - Second-to-die for estate tax planning
6. Premium comparison and total cost analysis across policy types
```

### Annuity Evaluation Framework

```
A client (age [age], [risk tolerance]) is considering allocating $[amount] to an annuity
for guaranteed retirement income. Compare the following options:

1. Single Premium Immediate Annuity (SPIA):
   - Estimate monthly payout based on current rates for [age/gender/joint option]
   - Calculate implied internal rate of return at various longevity assumptions
   - Mortality credit value: how does pooling improve individual outcomes?

2. Fixed Indexed Annuity (FIA):
   - Participation rate: [X]%, cap: [X]%, floor: 0%
   - Expected return modeling vs. direct equity/bond allocation
   - Surrender schedule and liquidity constraints

3. Variable Annuity with GLWB (Guaranteed Lifetime Withdrawal Benefit):
   - Benefit base growth rate: [X]%
   - Guaranteed withdrawal rate: [X]% at age [X]
   - Total fee analysis: M&E + sub-account fees + rider fee = [total]
   - Breakeven analysis: at what age does the guarantee become valuable?

4. Comparison with systematic withdrawal from investment portfolio:
   - Probability of annuity outperforming portfolio withdrawal
   - Flexibility trade-off: annuity certainty vs. portfolio optionality
   - Tax treatment: exclusion ratio (SPIA) vs. ordinary income (qualified)
   - Legacy value: annuity (reduced/none) vs. portfolio (remaining balance)
```

---

## 4. Education Planning

529 plans, financial aid optimization, gifting strategies, and multi-generational education funding.

### Education Funding Strategy

```
A client wants to fund education for [number] children, ages [ages]:

- Target institutions: [public in-state / public out-of-state / private / elite]
- Current projected cost per year: $[amount], inflation rate: [X]%
- Current 529 balance: $[amount] in [state plan]
- Annual savings available: $[amount]
- Grandparent involvement: [yes/no, amount available]
- Financial aid eligibility concern: [yes/no]
- MAGI: $[amount]

Develop an education funding plan:
1. Total projected cost (4 years per child, inflation-adjusted)
2. Funding gap: projected cost - current 529 FV - future contributions FV
3. 529 plan optimization:
   - State tax deduction value (if applicable): $[state] plan benefit
   - Superfunding: 5-year gift tax averaging ($[amount] per beneficiary)
   - Investment glide path: aggressive -> moderate -> conservative as enrollment approaches
4. Financial aid strategy:
   - FAFSA EFC calculation impact of 529 ownership (parent vs. grandparent vs. student)
   - Timing of grandparent 529 distributions (new FAFSA rules effective 2024)
   - CSS Profile considerations for elite private institutions
5. Alternatives: Coverdell ESA, UTMA, I-bonds, taxable account, Roth IRA (contributions)
6. Excess funding plan: what if child receives scholarships or chooses lower-cost path?
```

---

## 5. Cash Flow Planning

Budgeting, emergency reserves, debt management, and savings rate optimization.

**Savings Rate Optimization:**

Optimal savings rate depends on:
- Target replacement ratio (typically 70-85% of pre-retirement income)
- Years to retirement
- Expected real return
- Current savings as % of target

Simplified formula:
Required annual savings = FV_need / [ ((1+r)^n - 1) / r ]
Where FV_need = PV_retirement_liability x (1+r)^years_to_retirement

### Comprehensive Cash Flow Analysis

```
Analyze the cash flow position for a client household:

Income:
- Salary/wages: $[amount] (gross), filing status: [single/MFJ]
- Bonus/RSU vesting: $[amount] (variable, estimate)
- Investment income: $[amount] (dividends, interest, capital gains)
- Other: $[rental, side business, etc.]

Fixed expenses:
- Housing (mortgage/rent, property tax, insurance): $[amount]
- Debt service (auto, student loans, other): $[amount]
- Insurance premiums (health, life, disability, umbrella): $[amount]
- Childcare/education: $[amount]

Variable/discretionary:
- Living expenses (food, transportation, utilities): $[amount]
- Lifestyle (travel, dining, entertainment): $[amount]

Current savings:
- 401(k)/403(b): $[amount] (employer match: [X]%)
- IRA/Roth IRA: $[amount]
- Taxable savings: $[amount]
- Emergency fund: $[amount] (target: [X] months expenses)

Provide:
1. Net cash flow analysis: after-tax income - total expenses - current savings
2. Savings rate: current vs. target (what rate is needed to reach retirement goal?)
3. Emergency fund adequacy: current months of coverage vs. recommended (3-6 months)
4. Debt optimization:
   - Rank debts by after-tax interest rate
   - Avalanche (highest rate first) vs. snowball (smallest balance first) payoff strategy
   - Refinancing opportunities given current rates
5. Tax optimization: are they maximizing pre-tax/Roth contributions? HSA? Backdoor Roth?
6. Cash flow surplus deployment priority:
   a. Employer match (guaranteed 100% return)
   b. High-interest debt payoff
   c. Emergency fund to target
   d. Max tax-advantaged accounts
   e. Taxable investing / additional goals
```

### Debt Management Strategy

```
A client has the following debts and is seeking an optimal payoff strategy:

| Debt | Balance | Interest Rate | Monthly Payment | Tax Deductible? |
|---|---|---|---|---|
| [Mortgage] | $[amount] | [X]% | $[amount] | [Yes/No] |
| [Student loans] | $[amount] | [X]% | $[amount] | [Partial] |
| [Auto loan] | $[amount] | [X]% | $[amount] | [No] |
| [Credit cards] | $[amount] | [X]% | $[amount] | [No] |
| [Other] | $[amount] | [X]% | $[amount] | [No] |

Additional monthly cash flow available for debt payoff: $[amount]
Marginal tax rate: [X]%
Risk-free rate / expected investment return: [X]%

Analyze:
1. After-tax cost of each debt: rate x (1 - tax_benefit)
2. Optimal payoff ordering by after-tax cost
3. Total interest saved by accelerating payoff vs. minimum payments
4. Breakeven analysis: at what investment return does investing beat debt payoff?
5. Refinancing analysis: which debts could benefit from rate reduction?
6. Timeline to debt-free status under recommended plan
```

---

## See Also

- [Private Banking](private-banking.md) -- UHNW advisory, custom lending, structured solutions
- [Estate & Tax Planning](estate-tax-planning.md) -- Trusts, gift tax, charitable strategies
- [Portfolio Construction](portfolio-construction.md) -- Goals-based allocation, tax-aware management
- [Alternative Investments](alternative-investments.md) -- PE, hedge funds, real estate
- [Asset Management](../asset-management/) -- Institutional portfolio management
