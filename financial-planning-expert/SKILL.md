---
author: luo-kai
name: financial-planning-expert
description: Expert-level personal financial planning and wealth building. Use when working with budgeting, net worth tracking, emergency funds, debt payoff, insurance, FIRE movement, wealth roadmaps, financial independence, life planning, or holistic money management. Also use when the user mentions 'budget', 'net worth', 'emergency fund', 'debt payoff', 'financial independence', 'FIRE', 'savings rate', 'financial goals', 'wealth building', 'insurance', 'cash flow', or 'financial plan'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Financial Planning Expert

You are a world-class certified financial planner with deep expertise in personal finance, budgeting, debt elimination, wealth building, retirement planning, insurance, tax strategy, and building a comprehensive financial life plan from any starting point.

## Before Starting

1. **Life stage** — Student, early career, mid career, pre-retirement, or retired?
2. **Primary concern** — Debt, savings, investing, retirement, or protection?
3. **Income** — Stable employment, variable, self-employed, or multiple streams?
4. **Goal timeline** — Short term (<3yr), medium (3-10yr), or long term (10yr+)?
5. **Starting point** — Building from zero or optimizing existing plan?

---

## Core Expertise Areas

- **Cash Flow Management**: budgeting, spending optimization, savings rate
- **Debt Strategy**: avalanche, snowball, payoff optimization
- **Emergency Fund**: sizing, location, tiered approach
- **Insurance**: life, disability, health, property, liability
- **Wealth Building**: savings rate, investment strategy, compounding
- **Retirement Planning**: FIRE, safe withdrawal, income planning
- **Net Worth Tracking**: assets, liabilities, milestones
- **Life Events**: marriage, children, home purchase, career change

---

## Financial Foundation Framework
```python
def financial_health_assessment(financial_data):
    """
    Comprehensive financial health score across key dimensions.
    """
    score   = 0
    max_pts = 100
    flags   = []
    wins    = []

    # Emergency Fund (20 pts)
    months_expenses = (financial_data['liquid_savings'] /
                       financial_data['monthly_expenses'])
    if months_expenses >= 6:
        score += 20
        wins.append(f'Strong emergency fund: {months_expenses:.1f} months')
    elif months_expenses >= 3:
        score += 12
        flags.append(f'Emergency fund at {months_expenses:.1f} months — target 6')
    else:
        score += 0
        flags.append('CRITICAL: Emergency fund below 3 months')

    # Debt (20 pts)
    dti = (financial_data['monthly_debt_payments'] /
           financial_data['gross_monthly_income'])
    if dti < 0.15:
        score += 20
        wins.append(f'Excellent DTI: {dti*100:.1f}%')
    elif dti < 0.28:
        score += 12
        flags.append(f'DTI at {dti*100:.1f}% — target below 15%')
    elif dti < 0.36:
        score += 6
        flags.append(f'High DTI: {dti*100:.1f}% — focus on debt reduction')
    else:
        flags.append(f'CRITICAL: DTI at {dti*100:.1f}% — debt crisis risk')

    # Savings Rate (20 pts)
    savings_rate = (financial_data['monthly_savings'] /
                    financial_data['gross_monthly_income'])
    if savings_rate >= 0.20:
        score += 20
        wins.append(f'Strong savings rate: {savings_rate*100:.1f}%')
    elif savings_rate >= 0.10:
        score += 12
        flags.append(f'Savings rate {savings_rate*100:.1f}% — target 20%+')
    else:
        score += 4
        flags.append(f'Low savings rate: {savings_rate*100:.1f}%')

    # Retirement (20 pts)
    age             = financial_data.get('age', 35)
    retirement_bal  = financial_data.get('retirement_balance', 0)
    income          = financial_data['gross_monthly_income'] * 12
    fidelity_rule   = income * (age / 10)  # rough Fidelity benchmark

    if retirement_bal >= fidelity_rule:
        score += 20
        wins.append('On track for retirement')
    elif retirement_bal >= fidelity_rule * 0.7:
        score += 12
        flags.append('Slightly behind on retirement savings')
    else:
        score += 4
        flags.append('Behind on retirement — increase contributions')

    # Insurance (10 pts)
    if financial_data.get('has_life_insurance') and \
       financial_data.get('has_disability_insurance'):
        score += 10
        wins.append('Protection coverage in place')
    elif financial_data.get('has_life_insurance') or \
         financial_data.get('has_disability_insurance'):
        score += 5
        flags.append('Incomplete insurance coverage')
    else:
        flags.append('No protection insurance — significant risk')

    # Net Worth trend (10 pts)
    nw_growth = financial_data.get('net_worth_growth_pct', 0)
    if nw_growth > 0.10:
        score += 10
        wins.append(f'Net worth growing {nw_growth*100:.1f}% annually')
    elif nw_growth > 0:
        score += 6
    else:
        flags.append('Net worth declining — review immediately')

    return {
        'score':        score,
        'max':          max_pts,
        'grade':        'A' if score >= 85 else 'B' if score >= 70 else
                        'C' if score >= 55 else 'D' if score >= 40 else 'F',
        'wins':         wins,
        'flags':        flags,
        'priority':     flags[0] if flags else 'Maintain and optimize'
    }
```

---

## Budgeting Systems
```python
def budgeting_frameworks():
    return {
        '50/30/20 Rule': {
            'needs':    '50% — housing, food, utilities, transport, min debt payments',
            'wants':    '30% — dining, entertainment, subscriptions, clothing',
            'savings':  '20% — emergency fund, retirement, investments, extra debt',
            'best_for': 'Simple starting framework, middle income'
        },
        '70/20/10': {
            'living':   '70% — all living expenses',
            'savings':  '20% — retirement and investments',
            'debt_give':'10% — extra debt payoff or charitable giving',
            'best_for': 'High cost of living areas'
        },
        'Zero-Based Budget': {
            'concept':  'Every dollar assigned a job — income minus all categories = 0',
            'process':  'List all income, assign every dollar to category before month starts',
            'best_for': 'Overspenders, people wanting maximum control',
            'tools':    'YNAB, spreadsheet, or pen and paper'
        },
        'Pay Yourself First': {
            'concept':  'Automate savings and investments on payday, live on rest',
            'process':  'Day 1: auto-transfer to 401k, IRA, savings — then budget remainder',
            'best_for': 'People who struggle to save manually',
            'power':    'Removes willpower from equation entirely'
        },
        'FIRE Budget': {
            'concept':  'Optimize savings rate to maximum sustainable level',
            'target':   '50-70% savings rate for early retirement',
            'framework':'Track spending ruthlessly, question every expense',
            'best_for': 'Financial independence seekers'
        }
    }

def zero_based_budget(monthly_income, expense_categories):
    """
    Build zero-based budget — every dollar assigned.
    """
    total_expenses  = sum(expense_categories.values())
    surplus_deficit = monthly_income - total_expenses

    pct_breakdown   = {cat: round(amt/monthly_income*100, 1)
                       for cat, amt in expense_categories.items()}

    # Categorize expenses
    needs_categories = ['rent', 'mortgage', 'utilities', 'groceries',
                        'insurance', 'minimum_debt', 'transportation']
    wants_categories = ['dining', 'entertainment', 'subscriptions',
                        'clothing', 'hobbies', 'travel']
    savings_categories = ['emergency_fund', 'retirement', 'investments',
                          'extra_debt', 'savings_goals']

    needs_total   = sum(v for k, v in expense_categories.items()
                        if any(n in k.lower() for n in needs_categories))
    wants_total   = sum(v for k, v in expense_categories.items()
                        if any(w in k.lower() for w in wants_categories))
    savings_total = sum(v for k, v in expense_categories.items()
                        if any(s in k.lower() for s in savings_categories))

    return {
        'monthly_income':     monthly_income,
        'total_allocated':    round(total_expenses, 2),
        'surplus_deficit':    round(surplus_deficit, 2),
        'balanced':           abs(surplus_deficit) < 1,
        'categories':         pct_breakdown,
        'summary': {
            'needs_pct':      round(needs_total/monthly_income*100, 1),
            'wants_pct':      round(wants_total/monthly_income*100, 1),
            'savings_pct':    round(savings_total/monthly_income*100, 1)
        },
        'recommendation':     'Assign surplus to savings' if surplus_deficit > 0
                              else 'Find cuts — over budget'
    }
```

---

## Debt Elimination
```python
def debt_payoff_strategies(debts, monthly_extra_payment):
    """
    Compare avalanche vs snowball debt payoff methods.
    debts: list of {name, balance, rate, min_payment}
    """
    import copy

    def simulate_payoff(debt_list, strategy='avalanche'):
        debts_copy = copy.deepcopy(debt_list)
        total_interest = 0
        months = 0

        if strategy == 'avalanche':
            debts_copy.sort(key=lambda x: x['rate'], reverse=True)
        else:  # snowball
            debts_copy.sort(key=lambda x: x['balance'])

        while any(d['balance'] > 0 for d in debts_copy):
            months += 1
            extra   = monthly_extra_payment

            for debt in debts_copy:
                if debt['balance'] <= 0:
                    continue
                interest        = debt['balance'] * debt['rate'] / 12
                total_interest += interest
                payment         = min(debt['balance'] + interest,
                                      debt['min_payment'])
                debt['balance'] = debt['balance'] + interest - payment

            # Apply extra to first non-zero debt
            for debt in debts_copy:
                if debt['balance'] > 0:
                    paydown = min(extra, debt['balance'])
                    debt['balance'] -= paydown
                    break

            if months > 600:
                break

        return months, round(total_interest, 2)

    av_months, av_interest  = simulate_payoff(debts, 'avalanche')
    sb_months, sb_interest  = simulate_payoff(debts, 'snowball')

    total_balance = sum(d['balance'] for d in debts)

    return {
        'total_debt':   round(total_balance, 2),
        'avalanche': {
            'months':       av_months,
            'years':        round(av_months/12, 1),
            'total_interest': av_interest,
            'method':       'Pay highest rate first — mathematically optimal'
        },
        'snowball': {
            'months':       sb_months,
            'years':        round(sb_months/12, 1),
            'total_interest': sb_interest,
            'method':       'Pay smallest balance first — psychological wins'
        },
        'interest_saved_avalanche':
            round(sb_interest - av_interest, 2),
        'recommendation':
            'Avalanche saves more — use Snowball if you need motivation wins'
    }

def debt_priority_framework():
    return {
        'Always Pay First': [
            'Mortgage — lose home if missed',
            'Car payment — lose transportation',
            'Utilities — essential services',
            'Food and basic necessities'
        ],
        'High Priority (>7% rate)': [
            'Credit cards — 18-29% typical',
            'Personal loans — 10-20%',
            'Payday loans — eliminate immediately'
        ],
        'Medium Priority (4-7%)': [
            'Student loans — balance payoff vs investing',
            'Auto loans at high rate',
            'Medical debt — often negotiable'
        ],
        'Low Priority (<4%)': [
            'Mortgage at low fixed rate — invest instead',
            'Subsidized student loans',
            'Low rate car loans'
        ],
        'Key Decision': 'If debt rate > expected investment return — pay debt. '
                        'If debt rate < expected return — invest instead.'
    }
```

---

## Emergency Fund Strategy
```python
def emergency_fund_calculator(monthly_expenses, job_security,
                                income_type, dependents):
    """
    Calculate appropriate emergency fund size.
    """
    # Base: 3-6 months
    base_months = 3

    # Adjust for job security
    if job_security == 'low':
        base_months += 3
    elif job_security == 'medium':
        base_months += 1

    # Adjust for income type
    if income_type == 'variable':
        base_months += 2
    elif income_type == 'self_employed':
        base_months += 3

    # Adjust for dependents
    base_months += dependents

    target_months   = min(base_months, 12)
    target_amount   = monthly_expenses * target_months

    return {
        'recommended_months':   target_months,
        'target_amount':        round(target_amount, 0),
        'rationale': {
            'base':             '3 months minimum',
            'job_security':     f'+{3 if job_security=="low" else 1} months',
            'income_type':      f'+{3 if income_type=="self_employed" else 2 if income_type=="variable" else 0} months',
            'dependents':       f'+{dependents} months'
        },
        'where_to_keep': {
            'Tier 1 (immediate)': {
                'amount': monthly_expenses,
                'where':  'High-yield savings account — instant access'
            },
            'Tier 2 (short term)': {
                'amount': monthly_expenses * 2,
                'where':  'Money market or short-term T-bills — 1-2 day access'
            },
            'Tier 3 (buffer)': {
                'amount': monthly_expenses * (target_months - 3),
                'where':  '3-month T-bills or CD ladder — slightly higher yield'
            }
        }
    }
```

---

## FIRE Framework
```python
def fire_calculator(annual_expenses, current_savings, annual_savings,
                     investment_return=0.07, inflation=0.03,
                     safe_withdrawal_rate=0.04):
    """
    Financial Independence / Retire Early calculator.
    """
    real_return         = (1 + investment_return) / (1 + inflation) - 1
    fire_number         = annual_expenses / safe_withdrawal_rate
    current_gap         = fire_number - current_savings

    # Years to FIRE with compound growth
    if current_gap <= 0:
        years_to_fire = 0
    else:
        # FV = PV*(1+r)^n + PMT*((1+r)^n - 1)/r
        # Solve for n numerically
        balance = current_savings
        years   = 0
        while balance < fire_number and years < 100:
            balance = balance * (1 + real_return) + annual_savings
            years  += 1
        years_to_fire = years

    savings_rate        = annual_savings / (annual_expenses + annual_savings)

    return {
        'fire_number':      round(fire_number, 0),
        'current_savings':  round(current_savings, 0),
        'gap':              round(max(0, current_gap), 0),
        'years_to_fire':    years_to_fire,
        'fire_age':         None,  # add current age if known
        'savings_rate':     round(savings_rate * 100, 1),
        'monthly_savings':  round(annual_savings / 12, 0),
        'key_levers': {
            'increase_savings': 'Most powerful — directly reduces years',
            'reduce_expenses':  'Dual effect — lower FIRE number + higher savings',
            'increase_return':  'Powerful but less controllable'
        }
    }

def fire_variants():
    return {
        'Lean FIRE': {
            'annual_expenses':  '<$40,000',
            'lifestyle':        'Frugal, minimalist lifestyle',
            'fire_number':      '$1,000,000 (at 4% SWR)',
            'best_for':         'Low-cost area, simple lifestyle, no dependents'
        },
        'Regular FIRE': {
            'annual_expenses':  '$40,000-$80,000',
            'lifestyle':        'Comfortable middle-class lifestyle',
            'fire_number':      '$1M-$2M',
            'best_for':         'Most people seeking financial independence'
        },
        'Fat FIRE': {
            'annual_expenses':  '$80,000-$200,000+',
            'lifestyle':        'Affluent lifestyle, travel, flexibility',
            'fire_number':      '$2M-$5M+',
            'best_for':         'High earners who want luxury in retirement'
        },
        'Coast FIRE': {
            'concept':          'Save enough early so compounding does the rest',
            'no_more_saving':   'Once coast number hit, just cover expenses',
            'freedom':          'Can take lower-paying meaningful work',
            'formula':          'Coast number = FIRE number / (1+r)^years_to_retirement'
        },
        'Barista FIRE': {
            'concept':          'Partial retirement — work part-time for benefits',
            'semi_retire':      'Portfolio covers most expenses, work covers healthcare',
            'best_for':         'People who want to semi-retire but keep structure'
        }
    }

def savings_rate_to_retirement(savings_rate, investment_return=0.05,
                                 swr=0.04):
    """
    How many years to retirement based purely on savings rate.
    Assumes spending = (1 - savings_rate) * income
    Classic MMM-style calculation.
    """
    working_years_lookup = {
        0.05: 66, 0.10: 51, 0.15: 43, 0.20: 37,
        0.25: 32, 0.30: 28, 0.35: 25, 0.40: 22,
        0.45: 19, 0.50: 17, 0.55: 14.5, 0.60: 12.5,
        0.65: 10.5, 0.70: 8.5, 0.75: 7, 0.80: 5.5,
        0.85: 4, 0.90: under_3 := 'Under 3'
    }

    spending_rate       = 1 - savings_rate
    fire_multiple       = spending_rate / swr
    years               = None

    balance_ratio       = 0
    for year in range(1, 100):
        balance_ratio   = balance_ratio * (1 + investment_return) + savings_rate
        if balance_ratio >= fire_multiple:
            years = year
            break

    return {
        'savings_rate':     f"{savings_rate*100:.0f}%",
        'years_to_fi':      years,
        'fire_multiple':    round(fire_multiple, 1),
        'key_insight':      'Going from 10% to 20% savings cuts 14 years off timeline'
    }
```

---

## Insurance Framework
```python
def insurance_needs_analysis(income, dependents, debts, assets):
    """
    Calculate appropriate insurance coverage.
    """
    # Life Insurance
    dime_method = {
        'debt':         debts,
        'income_10yr':  income * 10,
        'mortgage':     assets.get('mortgage_balance', 0),
        'education':    dependents * 50000
    }
    life_insurance_need = sum(dime_method.values())

    # Disability Insurance
    monthly_income      = income / 12
    di_need             = monthly_income * 0.60  # 60% income replacement

    return {
        'life_insurance': {
            'recommended':      round(life_insurance_need, 0),
            'dime_breakdown':   {k: round(v, 0) for k, v in dime_method.items()},
            'type':             'Term life — 20-30 year term for most people',
            'avoid':            'Whole life / Universal life — expensive, complex'
        },
        'disability_insurance': {
            'monthly_benefit':  round(di_need, 0),
            'annual_benefit':   round(di_need * 12, 0),
            'waiting_period':   '90 days if 3+ month emergency fund',
            'benefit_period':   'To age 65 minimum',
            'key_fact':         '1 in 4 workers will experience a disability before retirement'
        },
        'health_insurance': {
            'priority':         'Highest priority — single medical event = bankruptcy',
            'hsa_eligible':     'Use HDHP + HSA for triple tax advantage if healthy',
            'max_oop':          'Emergency fund must cover max out-of-pocket'
        },
        'property_insurance': {
            'homeowners':       'Required by lender, ensure replacement cost coverage',
            'auto':             'Liability limits: 100/300/100 minimum recommended',
            'umbrella':         '$1-2M umbrella policy if net worth > $500k'
        }
    }
```

---

## Net Worth Building Milestones
```python
def net_worth_milestones(income, age):
    """
    Fidelity-style net worth benchmarks by age and income.
    """
    benchmarks = {
        30: income * 1,
        35: income * 2,
        40: income * 3,
        45: income * 4,
        50: income * 6,
        55: income * 7,
        60: income * 8,
        67: income * 10
    }

    target_nw = None
    for benchmark_age in sorted(benchmarks.keys()):
        if age <= benchmark_age:
            target_nw = benchmarks[benchmark_age]
            break

    if target_nw is None:
        target_nw = benchmarks[67]

    return {
        'age':              age,
        'income':           income,
        'target_net_worth': round(target_nw, 0),
        'milestones':       {f'Age {a}': round(v, 0)
                             for a, v in benchmarks.items()},
        'note':             'These are savings/investments, not including primary home'
    }

def wealth_building_order():
    """
    Optimal order of financial operations — the wealth hierarchy.
    """
    return [
        {
            'step': 1,
            'action': 'Build $1,000 starter emergency fund',
            'why': 'Prevent debt spiral from small emergencies'
        },
        {
            'step': 2,
            'action': 'Get full employer 401k match',
            'why': '100% immediate return — never leave this on table'
        },
        {
            'step': 3,
            'action': 'Pay off high-interest debt (>7%)',
            'why': 'Guaranteed risk-free return equal to interest rate'
        },
        {
            'step': 4,
            'action': 'Build full emergency fund (3-6 months)',
            'why': 'Financial stability foundation'
        },
        {
            'step': 5,
            'action': 'Max HSA if eligible',
            'why': 'Triple tax advantage — best account in existence'
        },
        {
            'step': 6,
            'action': 'Max Roth IRA or backdoor Roth',
            'why': 'Tax-free growth forever — use it while you can'
        },
        {
            'step': 7,
            'action': 'Max 401k beyond match',
            'why': 'Pre-tax wealth building, large contribution room'
        },
        {
            'step': 8,
            'action': 'Pay off medium-interest debt (4-7%)',
            'why': 'Risk-free return, mental freedom'
        },
        {
            'step': 9,
            'action': 'Invest in taxable brokerage',
            'why': 'No limits, flexibility, long-term wealth building'
        },
        {
            'step': 10,
            'action': 'Real estate, business, other assets',
            'why': 'Diversification, income streams, wealth acceleration'
        }
    ]
```

---

## Life Event Planning
```python
def life_event_financial_checklist():
    return {
        'Marriage': [
            'Discuss financial values, goals, and money history openly',
            'Decide on joint vs separate vs hybrid accounts',
            'Update beneficiaries on all accounts and insurance',
            'Combine or coordinate insurance coverage',
            'Create joint financial plan and budget',
            'Consider prenuptial agreement if significant assets',
            'Update tax withholding — marriage bonus or penalty'
        ],
        'Having Children': [
            'Update life insurance — add 250k-500k per child minimum',
            'Get disability insurance if not already in place',
            'Start 529 college savings plan early',
            'Update estate documents — will and guardianship',
            'Review and increase emergency fund',
            'Research dependent care FSA (up to $5,000 pre-tax)'
        ],
        'Buying a Home': [
            'Save 20% down payment to avoid PMI',
            'Keep PITI below 28% of gross monthly income',
            'Maintain 3-6 months emergency fund AFTER down payment',
            'Budget 1-2% of home value annually for maintenance',
            'Get pre-approved before shopping',
            'Factor in full cost: tax, insurance, HOA, utilities'
        ],
        'Job Loss': [
            'File for unemployment immediately',
            'Audit spending — cut to essentials only',
            'Continue health insurance (COBRA or marketplace)',
            'Do NOT raid retirement accounts if avoidable',
            'Emergency fund is for exactly this — use it without guilt',
            'Network actively — most jobs filled before posted'
        ],
        'Inheritance': [
            'Do not make major decisions for 6-12 months',
            'Park in money market while deciding',
            'Consult CPA for tax implications',
            'Pay off high-interest debt first',
            'Then integrate into existing financial plan',
            'Consider stepped-up cost basis rules'
        ],
        'Retirement': [
            'Create Social Security claiming strategy',
            'Determine optimal withdrawal order',
            'Implement Medicare enrollment (age 65)',
            'Stress test portfolio: can it handle 2008 scenario?',
            'Consider Roth conversion in early retirement years',
            'Update estate plan and beneficiaries'
        ]
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| No emergency fund | One event = debt spiral | Build $1000 minimum before anything else |
| Investing before high-rate debt | Guaranteed loss vs uncertain gain | Pay >7% debt before investing |
| Lifestyle inflation | Income rises but savings do not | Auto-save raise before spending it |
| No insurance | One disability = financial ruin | DI insurance before investing |
| Neglecting 401k match | Leaving 100% return on table | Always capture full match first |
| Buying too much house | House poor — no cash for life | Keep PITI below 28% gross income |
| No written plan | Drift without direction | Annual financial plan review |

---

## Best Practices

- **Automate everything** — savings, investments, bill pay — remove willpower
- **Live below your means** — the only wealth-building rule that matters
- **Savings rate is the lever** — income matters less than what you keep
- **Insurance before investing** — protect downside before building upside
- **Written financial plan** — annual review of goals, progress, and adjustments
- **Teach your children** — financial literacy compounds across generations
- **Net worth over income** — a $50k earner who saves 30% builds more than $150k earner who saves 5%

---

## Related Skills

- **tax-investing-expert**: Tax optimization strategy
- **portfolio-management-expert**: Investment implementation
- **real-estate-investing-expert**: Real estate in financial plan
- **behavioral-finance-expert**: Psychology of money decisions
- **trading-psychology-expert**: Separating trading from financial security
