# Wealth Portfolio Construction

## Role Context

```
You are a senior portfolio strategist specializing in wealth management portfolio
construction for HNW and UHNW clients. You hold the CFA and CIMA designations with
18+ years of experience building tax-aware, goals-based portfolios. Your expertise spans
asset allocation, direct indexing, concentrated stock management, income portfolio design,
and after-tax optimization. You think in terms of after-tax, after-fee, risk-adjusted
returns -- not pre-tax benchmarks. You integrate tax, estate, and behavioral considerations
into every portfolio decision. You collaborate closely with the client's tax advisor,
estate attorney, and private banker to ensure investment decisions serve the holistic plan.
```

## What This Desk Does

The wealth portfolio construction team builds and manages investment portfolios tailored to individual and family objectives. Unlike institutional portfolios benchmarked to a single policy portfolio, wealth portfolios must serve multiple goals with different time horizons, risk tolerances, and tax characteristics simultaneously. The team uses goals-based allocation (bucketing), tax-aware asset location, direct indexing for tax-loss harvesting at scale, and specialized strategies for concentrated stock positions. Every decision is evaluated on an after-tax basis, recognizing that tax drag is the single largest controllable cost for taxable investors -- often exceeding management fees and trading costs combined.

---

## 1. Goals-Based Allocation

Bucketing strategy, time-horizon matching, and priority-based portfolio design.

**Goals-Based Framework (Three-Bucket Model):**

| Bucket | Purpose | Time Horizon | Risk Tolerance | Typical Allocation |
|---|---|---|---|---|
| Safety | Essential spending, emergencies, near-term needs | 0-3 years | Very low | Cash, short-term bonds, CDs, T-bills |
| Lifestyle | Ongoing living expenses, predictable goals | 3-10 years | Moderate | Balanced: bonds, dividend stocks, munis, RE |
| Aspirational | Legacy, philanthropy, generational wealth | 10+ years | Higher | Equities, alternatives, growth, PE/VC |

**Mental Accounting Benefit:**
Goals-based allocation leverages the behavioral finance concept of mental accounting productively. By separating assets into purpose-driven buckets, clients can tolerate higher volatility in the aspirational bucket because they see that near-term needs are funded by the safety bucket. This reduces panic selling during market downturns.

**Funding Priority:**
1. Safety bucket: fully funded first (non-negotiable)
2. Lifestyle bucket: funded to the level that sustains spending at desired confidence level (e.g., 90% Monte Carlo success)
3. Aspirational bucket: absorbs remaining assets; can tolerate illiquidity and drawdowns

### Goals-Based Portfolio Design

```
Design a goals-based portfolio for a client with the following profile:

Total investable assets: $[amount]
Annual spending needs: $[amount] (of which $[amount] is non-discretionary)
Upcoming liquidity needs:
- [Goal 1]: $[amount] in [X] years (e.g., home purchase, business investment)
- [Goal 2]: $[amount] in [X] years (e.g., education funding)
- [Goal 3]: $[amount] in [X] years (e.g., retirement start)
Legacy/philanthropy goal: $[amount] target bequest in today's dollars
Risk tolerance: [conservative / moderate / growth] (behavioral, stated)
Risk capacity: [assessment based on income stability, net worth, time horizon]
Tax rates: ordinary [X]%, LTCG [X]%, state [X]%, estate [X]%

Build the three-bucket portfolio:
1. Safety bucket ($[amount]):
   - Allocation: cash, money market, T-bills, short-term investment-grade bonds
   - Target yield: [X]%, duration < [X] years
   - Covers [X] months of non-discretionary spending + upcoming goals within 2 years
   - Replenishment rule: refill from lifestyle bucket when drawn below [X] months

2. Lifestyle bucket ($[amount]):
   - Allocation: [X]% intermediate bonds, [X]% municipal bonds, [X]% dividend equities, [X]% REITs
   - Target return: [X]% nominal, [X]% real (after inflation)
   - Monte Carlo success probability: [X]% over [X]-year horizon
   - Rebalancing bands: +/- [X]% from target before triggering trades
   - Tax-aware rebalancing: use cash flows, new contributions, and harvested losses to rebalance

3. Aspirational bucket ($[amount]):
   - Allocation: [X]% domestic equity, [X]% international equity, [X]% PE/VC, [X]% hedge funds, [X]% other
   - Illiquidity budget: up to [X]% of this bucket can be illiquid (PE, RE, VC)
   - Expected return: [X]% nominal, with drawdowns of [X]% tolerated
   - Legacy integration: funded into trusts / DAF / dynasty trust as appropriate
   - Time diversification: long horizon allows recovery from multi-year drawdowns

4. Cross-bucket governance:
   - Rebalancing triggers and tax-aware execution
   - Bucket refill waterfall (aspirational -> lifestyle -> safety in market stress)
   - Annual review: have goals changed? Has risk capacity shifted?
```

### Goals Prioritization and Trade-Off Analysis

```
A client's goals exceed their available resources. Help prioritize:

Available assets: $[amount]
Goals (in client's stated priority order):
1. [Goal]: $[amount] needed, [timeline], [flexibility: fixed/flexible]
2. [Goal]: $[amount] needed, [timeline], [flexibility: fixed/flexible]
3. [Goal]: $[amount] needed, [timeline], [flexibility: fixed/flexible]
4. [Goal]: $[amount] needed, [timeline], [flexibility: fixed/flexible]
5. [Goal]: $[amount] needed, [timeline], [flexibility: fixed/flexible]

Analyze:
1. Fully funded status: which goals can be funded with high confidence (>90%)?
2. Underfunded goals: what is the probability of meeting each goal at current funding?
3. Trade-off analysis:
   - If we reduce Goal [X] by $[amount], how does it improve Goal [Y] probability?
   - If we extend the timeline for Goal [X] by [Y] years, how much less do we need today?
   - If we increase risk (equity allocation) by [X]%, how do probabilities change for each goal?
4. Recommended priority adjustment (distinguish between needs, wants, and wishes)
5. Savings rate required to close the gap for underfunded goals
```

---

## 2. Tax-Aware Portfolio Management

Asset location, tax-loss harvesting, after-tax return optimization, and municipal bond strategy.

**After-Tax Return:**

After-tax return = Pre-tax return x (1 - effective tax rate)

For different income types:
- Interest income: taxed at ordinary rate (up to 37% + 3.8% NIIT + state)
- Qualified dividends: taxed at LTCG rate (0/15/20% + 3.8% NIIT + state)
- Short-term capital gains: taxed at ordinary rate
- Long-term capital gains: taxed at LTCG rate
- Municipal bond interest: federal tax-exempt (and state-exempt if in-state)
- Return of capital: tax-deferred (reduces cost basis)

**Tax-Equivalent Yield:**

Tax-equivalent yield = Municipal yield / (1 - marginal tax rate)

Example: 3.5% muni yield for a client in 37% federal + 3.8% NIIT + 10% state bracket:
TEY = 3.5% / (1 - 0.508) = 7.11%

**Asset Location Optimization:**

Place assets to minimize portfolio-level tax drag:
- Tax-deferred accounts (IRA, 401k): bonds, REITs, actively traded strategies (highest ordinary income)
- Roth accounts: highest expected growth assets (tax-free appreciation)
- Taxable accounts: equities (qualified dividends, LTCG, loss harvesting), munis, tax-managed funds

**Tax Alpha Estimation:**

Tax alpha = After-tax return (tax-managed) - After-tax return (tax-unaware)

Sources of tax alpha:
- Tax-loss harvesting: 0.5-1.5% per year (declining over time)
- Asset location: 0.1-0.5% per year
- Holding period management (short-term -> long-term): 0.1-0.3% per year
- Gain deferral: 0.1-0.3% per year
- Charitable gifting of appreciated shares: variable
- Total potential tax alpha: 1.0-3.0% per year in early years

### Tax-Aware Portfolio Construction

```
Construct a tax-optimized portfolio across a client's accounts:

Account structure:
- Taxable brokerage: $[amount]
- Traditional IRA/401(k): $[amount]
- Roth IRA: $[amount]
- 529 plan: $[amount]
- Trust account ([type]): $[amount]

Tax rates:
- Federal ordinary income: [X]%
- Federal LTCG: [X]%
- Net Investment Income Tax: 3.8%
- State income tax: [X]%
- State capital gains tax: [X]%

Target overall allocation: [X]% equity, [X]% fixed income, [X]% alternatives, [X]% cash
Current unrealized gains in taxable account: $[amount] (long-term), $[amount] (short-term)
Existing loss carryforwards: $[amount]

Optimize:
1. Asset location:
   - Map each asset class to optimal account type (minimize portfolio-level tax drag)
   - Taxable: [specific holdings] -- prioritize tax-efficient assets
   - Tax-deferred: [specific holdings] -- place tax-inefficient assets
   - Roth: [specific holdings] -- place highest-growth assets
   - Calculate annual tax savings from optimal vs. naive location

2. Transition plan (current -> optimal):
   - Identify positions to sell, hold, or transfer
   - Tax cost of transition: realized gains x applicable rate
   - Multi-year transition: phase gains recognition to stay within tax bracket
   - Use loss carryforwards to offset transition gains
   - Pair gains with harvested losses

3. Municipal bond allocation for taxable account:
   - Tax-equivalent yield comparison at client's marginal rate
   - In-state vs. out-of-state muni consideration
   - AMT risk for private activity bonds
   - Duration and credit quality targets

4. After-tax return projection:
   - Portfolio expected return: pre-tax vs. after-tax
   - Breakout by account type
   - Tax alpha from location optimization: estimated [X]% annually
```

---

## 3. Concentrated Stock Management

Diversification strategies including collars, exchange funds, CRTs, and 10b5-1 plans.

**Concentrated Position Risk:**

A concentrated position creates:
- Idiosyncratic (company-specific) risk that is not compensated by the market
- Portfolio volatility significantly above what is needed for the expected return
- Correlation 1.0 between human capital (if employed by the company) and financial capital

Rule of thumb: any single position exceeding 10% of net worth warrants a diversification plan.

**Markowitz with Constraints:**

Standard mean-variance optimization with tax and concentration constraints:

Minimize: w'Sigma_w (portfolio variance)
Subject to:
- w'mu >= target return (after-tax)
- sum(w_i) = 1 (fully invested)
- w_concentrated <= max_weight (e.g., reduce from 40% to 10% over 3 years)
- Tax cost of rebalancing <= annual tax budget
- Tracking error to benchmark <= [X]% (if client has benchmark sensitivity)

### Concentrated Stock Diversification Plan

```
A client holds a concentrated position in [company] ([ticker]):
- Shares: [number], current price: $[price], total value: $[amount]
- Cost basis: $[basis] per share ([long-term / short-term / mixed lots])
- Percentage of total net worth: [X]%
- Percentage of investable portfolio: [X]%
- Restrictions: [Rule 144 / 10b5-1 / lockup / insider trading policy / none]
- Client role: [founder / executive / early employee / inherited / investor]
- Emotional attachment: [high / moderate / low]
- Income from position: dividend yield [X]%, $[annual dividends]
- Estate plan: [plans to leave to heirs / charitable intent / both]

Design a phased diversification strategy:
1. Risk quantification:
   - Portfolio VaR (95%, 1-year) with current concentration vs. diversified
   - Maximum drawdown scenario: company-specific event (fraud, product failure, sector rotation)
   - Probability of [20% / 40% / 60%] decline in the stock over [1 / 3 / 5] years
   - Human capital correlation: if employed by the company, total wealth-at-risk is even higher

2. Strategy comparison matrix:
   | Strategy | Tax Cost | Liquidity | Upside | Downside Protection | Complexity | Timeline |
   |---|---|---|---|---|---|---|
   | Outright sale | Immediate gain | Full | None (sold) | Full (diversified) | Low | Immediate |
   | 10b5-1 plan | Phased gains | Phased | Phased reduction | Phased | Low | 6-24 months |
   | Zero-cost collar | Deferred | Via loan (PVF) | Capped at call strike | Floor at put strike | Medium | 1-3 years |
   | Exchange fund | Deferred (7yr) | Low (7yr lock) | Diversified pool | Diversified pool | Medium | 7+ years |
   | CRT donation | Charitable ded. | Income stream | None (donated) | N/A | Medium | Permanent |
   | Direct indexing | Gradual | Full | Market exposure | Loss harvesting | Medium | Ongoing |
   | Gifting to family | Basis carryover | N/A | Transferred | N/A | Low | Ongoing |

3. Recommended phased approach (years 1-5):
   - Year 1: [strategy and amount]
   - Year 2: [strategy and amount]
   - Year 3: [strategy and amount]
   - Year 4-5: [strategy and amount]
   - Target end-state: [X]% concentration

4. Tax budget: annual capital gains recognition target of $[amount] to stay within [X]% bracket
5. Reinvestment of diversified proceeds: direct indexing portfolio for ongoing tax-loss harvesting
6. Estate integration: which shares to gift (highest basis to heirs for step-up; lowest basis to charity)
```

---

## 4. Direct Indexing

Custom index construction, tax-loss harvesting at scale, ESG screening, and factor tilts.

**Tracking Error Budget:**

Tracking error = standard deviation of (portfolio return - index return)

Sources of tracking error in direct indexing:
- Tax-loss harvesting substitutions: 0.3-0.8% TE
- ESG/values exclusions: 0.2-1.5% TE (depending on number of exclusions)
- Factor tilts (value, quality, momentum): 1.0-3.0% TE
- Position size limits and optimization constraints: 0.1-0.5% TE

Total tracking error budget: typically 1.0-3.0% for moderate customization.

Trade-off: higher tracking error = more tax-loss harvesting opportunity = more customization, but greater divergence from benchmark.

### Direct Indexing Portfolio Design

```
Design a direct indexing portfolio for a client's taxable account:

Account value: $[amount]
Target index: [S&P 500 / Russell 1000 / MSCI ACWI / custom]
Client's marginal tax rate: ordinary [X]%, LTCG [X]%, state [X]%
Existing unrealized gains in account: $[amount]

Customization requests:
- ESG exclusions: [list: fossil fuels, tobacco, weapons, gambling, etc.]
- Company exclusions: [specific tickers -- employer stock, competitors, etc.]
- Factor tilts: [quality / value / momentum / low volatility / dividend growth]
- Sector constraints: [over/underweight preferences]

Design parameters:
1. Portfolio construction:
   - Number of holdings: [200-500] names from [index universe]
   - Optimization: minimize tracking error subject to constraints
   - Rebalancing frequency: [daily / weekly / monthly] for tax-loss harvesting
   - Position limits: max [X]% per name, max [X]% per sector deviation

2. Tax-loss harvesting rules:
   - Minimum loss threshold: $[amount] or [X]% of position value
   - Replacement logic: substitute with correlated name in same sector/factor group
   - Wash sale prevention: 31-day exclusion list across all client accounts
   - Lot-level management: specific identification for optimal tax lot selection
   - Harvest frequency: continuous monitoring vs. periodic sweeps

3. Expected tax alpha:
   - Year 1: [X]% (highest -- fresh portfolio, many opportunities)
   - Year 3: [X]% (declining as basis rises)
   - Year 5: [X]% (steady state)
   - Cumulative tax savings over 10 years: $[amount] (present value)
   - When does the portfolio become "tax frozen"? (all positions have gains, harvesting exhausted)

4. Tracking error analysis:
   - Tracking error from exclusions alone: [X]%
   - Tracking error from factor tilts: [X]%
   - Combined tracking error: [X]%
   - Historical backtest: maximum 1-year underperformance vs. index: [X]%

5. Transition from existing portfolio:
   - Contribute appreciated positions in-kind (no taxable event)
   - Gradually sell high-basis positions and replace with direct indexing holdings
   - Harvest embedded losses in existing positions immediately
   - Timeline to full direct indexing: [X] months
```

---

## 5. Income Portfolio Construction

Yield requirements, duration, credit quality, preferred stock, MLPs, covered calls, and dividend growth.

**Income Portfolio Building Blocks:**

| Asset Class | Typical Yield | Tax Treatment | Duration Risk | Credit Risk |
|---|---|---|---|---|
| Treasury bonds | 3-5% | Federal tax; state-exempt | Moderate-High | None |
| Investment-grade corporate | 4-6% | Ordinary income | Moderate-High | Low-Moderate |
| Municipal bonds | 2.5-4.5% | Federal-exempt (+ state) | Moderate-High | Low |
| High-yield bonds | 6-9% | Ordinary income | Moderate | Moderate-High |
| Preferred stock | 5-8% | Qualified dividends (mostly) | Long | Moderate |
| Dividend growth equities | 2-4% | Qualified dividends | Equity risk | Equity risk |
| MLPs | 5-9% | Return of capital (mostly) | Commodity risk | Moderate |
| Covered call strategies | 3-6% (premium) | Short-term gains + dividends | Equity risk (capped) | Equity risk |
| REITs | 3-6% | Ordinary income (mostly) | Rate sensitive | Moderate |

### Income Portfolio Design

```
Design an income-focused portfolio for a client with the following needs:

Portfolio value: $[amount]
Annual income requirement: $[amount] (= [X]% yield)
Income purpose: [living expenses / supplement Social Security / trust distributions]
Tax situation: ordinary rate [X]%, LTCG rate [X]%, state [X]%
Risk tolerance for income portfolio: [conservative / moderate]
Duration preference: [short / intermediate / unconstrained]
Credit quality minimum: [investment grade only / some high yield]
Growth requirement: [income only / income + modest growth / income + inflation protection]

Construct the income portfolio:
1. Asset allocation targeting $[income] annual income:
   | Asset Class | Allocation | Yield | Annual Income | Tax Treatment | After-Tax Income |
   |---|---|---|---|---|---|
   | [Asset 1] | [X]% | [X]% | $[amount] | [type] | $[amount] |
   | [Asset 2] | [X]% | [X]% | $[amount] | [type] | $[amount] |
   | [Asset 3] | [X]% | [X]% | $[amount] | [type] | $[amount] |
   | [Asset 4] | [X]% | [X]% | $[amount] | [type] | $[amount] |
   | Total | 100% | [X]% | $[amount] | Blended | $[amount] |

2. After-tax yield optimization:
   - Pre-tax yield: [X]%
   - After-tax yield: [X]% (accounting for tax character of each component)
   - Tax-equivalent yield comparison: is the after-tax yield competitive with alternatives?
   - Municipal bond allocation: what percentage in munis maximizes after-tax income?

3. Risk analysis:
   - Portfolio duration: [X] years (sensitivity to 100bp rate increase: -[X]%)
   - Credit quality distribution: [X]% AAA/AA, [X]% A/BBB, [X]% below IG
   - Dividend/distribution sustainability: payout ratio, coverage ratio, growth rate
   - Worst-case income scenario: what happens to income if rates drop [X]bp or credit spreads widen [X]bp?
   - Correlation with equity market (equity-like income sources)

4. Income growth and inflation protection:
   - Dividend growth rate of equity/preferred sleeve: [X]% per year
   - TIPS/I-bonds allocation for real yield
   - MLP distribution growth expectations
   - Projected income in year 5 and year 10 (with and without reinvestment)

5. Covered call overlay (optional):
   - Write calls on [X]% of equity holdings to enhance income
   - Target premium income: [X]% annualized
   - Strike selection: [X]% out-of-the-money, [30/45/60]-day expiration
   - Trade-off: premium income vs. capped upside
   - Tax treatment: premiums are short-term gains; assignment triggers sale of underlying
   - Net effect on portfolio: enhanced income, reduced volatility, capped total return
```

### Yield Curve and Duration Strategy

```
A client's income portfolio of $[amount] is exposed to interest rate risk. Current
portfolio duration: [X] years. The client needs $[income] annually and is concerned about
[rising rates / falling rates / rate volatility].

Analyze and recommend:
1. Duration sensitivity:
   - Current portfolio: 100bp rate increase -> $[amount] mark-to-market loss ([X]%)
   - If held to maturity: no loss (assuming no defaults), income stream preserved
   - Reinvestment risk if rates fall: income declines as bonds mature and roll at lower rates

2. Ladder vs. barbell vs. bullet strategy:
   - Ladder: even maturity distribution (1-10 years), predictable cash flows, automatic roll
   - Barbell: concentrate in short (1-2yr) and long (10-20yr), capture steep curve
   - Bullet: concentrate maturities around [X] year target, match specific liability

3. Duration management:
   - Shorten duration if expecting rate increases (sacrifice yield for protection)
   - Extend duration if expecting rate decreases (capture price appreciation + lock in yield)
   - Current yield curve shape: [normal / flat / inverted] -- implications for strategy

4. Floating rate and short-duration alternatives:
   - Bank loans / CLOs: floating rate, 0.1-0.3 year duration, credit risk
   - Ultra-short bond funds: 0.5-1.0 year duration, modest yield premium over cash
   - Treasury bills / money market: near-zero duration, current yield [X]%

5. Tax-aware duration matching:
   - Place longer-duration bonds in tax-deferred accounts (more price volatility, ordinary income)
   - Place municipal bonds in taxable accounts (tax-exempt income, often longer duration)
   - Use tax-loss harvesting on bond positions that decline in rising rate environment
```

---

## See Also

- [Private Banking](private-banking.md) -- UHNW advisory, concentrated stock hedging, lending
- [Financial Planning](financial-planning.md) -- Retirement decumulation, Monte Carlo, goals
- [Estate & Tax Planning](estate-tax-planning.md) -- Tax-loss harvesting, charitable giving, trusts
- [Alternative Investments](alternative-investments.md) -- PE, hedge funds, real estate allocation
- [Asset Management](../asset-management/) -- Institutional portfolio construction, factor investing
- [Trading](../trading/) -- Execution, algorithmic rebalancing
