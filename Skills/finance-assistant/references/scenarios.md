# TaxDE Scenario Simulator Templates

Each template defines inputs, calculation steps, output format, and recommendation logic.
Always end with: "Want me to model any variations on this?"

---

## Template 1: Steuerklasse Optimizer

### Inputs from profile
- `partner_A_gross`: float
- `partner_B_gross`: float
- `children`: list
- `bundesland`: str (for Kirchensteuer)
- `kirchensteuer_A`, `kirchensteuer_B`: bool

### Calculation steps

**Step 1 — Calculate net monthly for each Steuerklasse combination**

Use standard LSt tables approximation:
- 4/4: each taxed individually on their own income
- 3/5: A gets III (no basic deductions multiplied), B gets V (very high withholding)
- Faktorverfahren: each taxed at their share of combined household tax

**Formula for Splittingvorteil**:
```
combined_income = A_gross + B_gross
tax_split = tax(combined_income / 2) × 2
tax_individual = tax(A_gross) + tax(B_gross)
splitting_advantage = tax_individual - tax_split
```

**Step 2 — Monthly cashflow comparison (3/5 vs 4/4)**

```
net_A_3 = A_gross/12 - lohnsteuer_III(A_gross/12) - social_contributions(A_gross/12)
net_B_5 = B_gross/12 - lohnsteuer_V(B_gross/12) - social_contributions(B_gross/12)
net_A_4 = A_gross/12 - lohnsteuer_IV(A_gross/12) - social_contributions(A_gross/12)
net_B_4 = B_gross/12 - lohnsteuer_IV(B_gross/12) - social_contributions(B_gross/12)
```

**Step 3 — Year-end settlement**

```
annual_settlement_3_5 = actual_joint_tax - (lohnsteuer_paid_A + lohnsteuer_paid_B)
annual_settlement_4_4 = actual_joint_tax - (lohnsteuer_paid_A + lohnsteuer_paid_B)
```
Note: Annual tax liability is identical in all combinations — only the timing of payment differs.

### Output format
```
═══ Steuerklasse Comparison ═══
Gross income: Partner A €[X] | Partner B €[Y]
Annual joint tax liability: €[Z] (identical in all scenarios)

Monthly net cashflow:
                    A net/mo    B net/mo    Combined    Year-end settlement
Klasse 4/4:        €[A_4]      €[B_4]      €[sum]      €[+/-]
Klasse 3/5:        €[A_3]      €[B_5]      €[sum]      €[+/-]
Faktorverfahren:   €[A_f]      €[B_f]      €[sum]      ~€0

Recommendation: [based on income split]
```

### Recommendation logic
- Income gap <20%: Faktorverfahren or 4/4 (minimal settlement)
- Income gap 20-40%: Faktorverfahren (best of both worlds)
- Income gap >40%: 3/5 for monthly cashflow advantage, but plan for year-end payment
- One partner not working: 3/5 obvious choice

---

## Template 2: Company Car vs. Cash

### Inputs from profile
- `list_price`: float (Bruttolistenpreis)
- `commute_km`: float
- `working_days_per_year`: int
- `marginal_tax_rate`: float
- `fuel_costs_monthly`: float (estimated if taking cash)
- `insurance_monthly`: float
- `car_type`: "petrol" | "diesel" | "electric_full" | "phev_50km+"

### Calculation steps

**Step 1 — Monthly taxable benefit**
```python
if car_type == "electric_full":
    rate = 0.0025  # 0.25%
elif car_type == "phev_50km+":
    rate = 0.005   # 0.5%
else:
    rate = 0.01    # 1%

monthly_benefit_base = list_price * rate
commute_benefit = list_price * 0.0003 * commute_km  # 0.03% × km
total_monthly_benefit = monthly_benefit_base + commute_benefit
```

**Step 2 — Monthly tax cost**
```
monthly_tax_cost = total_monthly_benefit × marginal_tax_rate
monthly_social_cost = min(total_monthly_benefit, 0) × 0.0975  # only if below BBG
net_monthly_car_cost = monthly_tax_cost + monthly_social_cost
```

**Step 3 — Cash alternative net value**
```
cash_net = cash_amount × (1 - marginal_tax_rate) × (1 - 0.0975)  # after tax + social
private_mobility_cost = fuel_monthly + insurance_monthly + annual_maintenance/12
```

**Step 4 — Annual comparison**
```
car_advantage = (cash_net × 12 + private_mobility_cost × 12) - (net_monthly_car_cost × 12)
```

### Output format
```
═══ Company Car vs. Cash Analysis ═══

Car: [model/list price €X]  |  Commute: [km]  |  Type: [petrol/electric/PHEV]

1% RULE CALCULATION:
  Base benefit:       €[X]/month (1% × €[list_price])
  Commute add-on:     €[Y]/month (0.03% × [km] km × €[list_price])
  Total benefit:      €[Z]/month
  Tax cost to you:    €[W]/month ([marginal_rate]% × €[Z])

ALTERNATIVE: €[cash] cash/month
  Net after tax:      €[cash_net]/month
  You still pay:      fuel ~€[fuel], insurance ~€[ins], maintenance ~€[maint]
  Net cash advantage: €[net_cash]/month

VERDICT:
[Company car saves you €X/month vs taking cash — mostly because of the electric rate]
OR
[Cash is €X/month better — the 1%-Regelung is too expensive at this list price]
```

### Electric car note
Always flag: Tesla Model 3 / full electric at 0.25% rate → monthly benefit dramatically lower than equivalent petrol car.

---

## Template 3: Homeoffice — Tagespauschale vs. Arbeitszimmer

### Inputs from profile
- `homeoffice_days_per_week`: float
- `homeoffice_room_sqm`: float
- `apartment_sqm`: float
- `annual_rent`: float
- `homeoffice_room_type`: "dedicated" | "shared"

### Calculation steps

**Tagespauschale**:
```
annual_days = min(homeoffice_days_per_week × 46, 210)
tagespauschale = min(annual_days × 6, 1260)
```

**Arbeitszimmer (if dedicated room)**:
```
room_proportion = room_sqm / apartment_sqm
deductible_base = annual_rent + annual_utilities + annual_insurance
arbeitszimmer = deductible_base × room_proportion
# Also includes proportional share of renovation/maintenance costs
```

**Breakeven**:
```
breakeven_annual_rent_for_room = 1260 / room_proportion
# If your rent × room_proportion > €1,260, Arbeitszimmer wins
```

### Recommendation logic
- Total apartment rent: check if `annual_rent × room_proportion > 1,260`
- If yes AND room is truly dedicated → Arbeitszimmer
- If no OR room is shared → Tagespauschale
- Note: If you work fully from home (Mittelpunkt), no cap on Arbeitszimmer

---

## Template 4: Bonus Optimization (Fünftelregelung)

### Inputs from profile
- `annual_salary`: float
- `bonus_amount`: float
- `year_end_tax_paid`: float (estimated LSt)
- `marginal_rate`: float

### Calculation steps

**Without Fünftelregelung**:
```
total_income = annual_salary + bonus_amount
tax_total = income_tax(total_income)
additional_tax = tax_total - income_tax(annual_salary)
```

**With Fünftelregelung (§34 EStG)**:
```
tax_base = income_tax(annual_salary + bonus_amount/5)
tax_normal = income_tax(annual_salary)
fünftel_tax = (tax_base - tax_normal) × 5
```

**Saving**:
```
saving = additional_tax - fünftel_tax
```

**Year-end offset via Rürup**:
```
max_ruerup_remaining = ruerup_annual_max - ruerup_already_contributed
ruerup_saving = max_ruerup_remaining × marginal_rate_after_bonus
net_ruerup_cost = max_ruerup_remaining × (1 - marginal_rate_after_bonus)
```

### Output format
```
═══ Bonus Optimization: €[bonus] ═══

Without optimization:
  Additional tax on bonus:  €[additional_tax]
  Net bonus received:       €[bonus - additional_tax]

With Fünftelregelung:
  Tax on bonus:             €[fünftel_tax]
  Saving vs. normal:        €[saving]
  Net bonus received:       €[bonus - fünftel_tax]

Additional strategies before Dec 31:
  Max Rürup top-up:   €[amount] → saves €[saving] at your rate → net cost €[net_cost]
  Harvest ETF losses: [if applicable from profile]
```

---

## Template 5: Salary vs. Benefits Optimization

### Inputs from profile
- `monthly_gross`: float
- `marginal_rate`: float
- `commute_km`: float
- `has_company_bike_offer`: bool (optional)

### Benefits to model

**bAV (§3 Nr. 63 EStG)**:
```
bav_gross_contribution = desired_amount  # e.g., €200/month
bav_actual_cost = bav_gross_contribution × (1 - marginal_rate - 0.0975)
# Because contributed pre-tax AND pre-social-contributions
effective_discount = marginal_rate + 0.0975  # typically 55-65%
```

**Jobrad (§40 Abs. 2 S. 1 Nr. 7 EStG)**:
```
bike_list_price = 2500  # example
monthly_benefit = bike_list_price × 0.0025  # 0.25% rule for bikes
monthly_tax_cost = monthly_benefit × marginal_rate
gross_lease_rate = 80  # typical employer lease cost
salary_sacrifice = gross_lease_rate
net_monthly_cost = salary_sacrifice - (salary_sacrifice × (marginal_rate + 0.0975))
                 + monthly_tax_cost
net_advantage = what_you_would_pay_for_bike_privately/36 - net_monthly_cost
```

**Jobticket (§3 Nr. 15 EStG)**:
```
deutschlandticket = 49  # current monthly cost
tax_free_benefit_value = 49  # full cost tax-free since 2020
net_saving_vs_private = 49 × (marginal_rate + 0.0975)
# i.e., employer pays €49 gross, you effectively get €49 of value instead of having
# to buy it from net salary
```

**Kinderbetreuungszuschuss (§3 Nr. 33 EStG)**:
```
kita_cost_monthly = kita_annual / 12
employer_pays_directly = kita_cost_monthly  # can be full Kita fee
tax_saving_vs_cash = kita_cost_monthly × marginal_rate
# Because employer can pay Kita directly — tax-free, unlimited amount
```

### Output format: Net advantage table

| Benefit | Gross cost to employer | Your net saving vs. taking cash |
|---------|----------------------|--------------------------------|
| bAV €200/mo | €200 | €[calc] |
| Jobrad €2,500 bike | ~€80/mo lease | €[calc] |
| Jobticket 49€ | €49 | €[calc] |
| Kita payment | €[cost] | €[calc] |

---

## Template 6: ETF / Investment Timing

### Inputs from profile
- `unrealized_gains`: float
- `unrealized_losses`: float
- `annual_dividends`: float
- `capital_income_ytd`: float
- `freistellungsauftrag_used`: float
- `freistellungsauftrag_total`: float (€1,000 or €2,000)

### Calculation steps

**Freistellungsauftrag remaining**:
```
remaining_fsa = freistellungsauftrag_total - freistellungsauftrag_used
can_realize_gains_free = remaining_fsa  # up to this amount, no tax
```

**Loss harvesting**:
```
net_taxable = max(0, unrealized_gains_to_realize - unrealized_losses_to_harvest)
kest_saving = unrealized_losses_to_harvest × 0.25  # (plus Soli)
kest_total_saving = kest_saving × 1.055  # including Soli
```

**Vorabpauschale (estimated)**:
```
# Published by BMF in January
# Estimated: Basiszins × 0.7 × fund_value × 0.7 (equity funds 30% reduction)
# At 2.29% Basiszins (2023): vorabpauschale ≈ 1.1% of fund value
vorabpauschale_annual = fund_value × basiszins × 0.7 × 0.7
vorabpauschale_tax = max(0, vorabpauschale_annual - remaining_fsa) × 0.25
```

### Output format
```
═══ ETF Tax Optimization ═══

Freistellungsauftrag: €[used]/€[total] used  |  €[remaining] remaining

If you sell €[gains] in gains before Dec 31:
  Tax owed: €[gains_tax] (after remaining FSA of €[remaining])

Loss harvesting opportunity:
  Unrealized losses: €[losses]
  If harvested: saves €[saving] in current year tax
  Wash sale: Germany has no wash sale rule → can immediately repurchase

Net action: Harvest €[losses] losses, save €[saving], reinvest immediately
```

---

## Template 7: GmbH Consideration

### Inputs from profile
- `annual_freelance_income`: float
- `personal_consumption_needs`: float (how much you need to live on)
- `bundesland`: str (for Gewerbesteuer Hebesatz)

### Calculation steps

**Hebesatz by city (2024)**:
```
hebesaetze = {
    "Berlin": 410, "Hamburg": 470, "München": 490,
    "Frankfurt": 460, "Köln": 475, "Stuttgart": 420,
    "Düsseldorf": 440, "Leipzig": 430, "Dresden": 390,
}
```

**Tax as sole trader (Freiberufler)**:
```
sole_trader_tax = income_tax(annual_income) + soli(income_tax)
# No Gewerbesteuer if Freiberufler
```

**Tax via GmbH (Gewerbetreibender)**:
```
gmbh_corp_tax = profit × 0.15  # Körperschaftsteuer
gmbh_soli = gmbh_corp_tax × 0.055
gewerbesteuer = profit × (messzahl * hebesatz / 100)
# messzahl = 3.5% for GmbH

total_gmbh_level = gmbh_corp_tax + gmbh_soli + gewerbesteuer

# Tax on distribution (Geschäftsführergehalt is expensed at GmbH level)
# Effective combined rate on retained earnings: ~30%
```

**Break-even calculation**:
```
# GmbH saves tax on retained earnings but costs more to run
gmbh_running_costs = 2500  # accounting, annual filings, steuerberater
gmbh_setup_cost = 1500    # Notar, registration
break_even_profit = where sole_trader_tax > gmbh_tax + running_costs
```

### Recommendation
- GmbH typically worth it at **net profit >€100,000-150,000** for Gewerbetreibende
- Not worthwhile for Freiberufler (no Gewerbesteuer anyway)
- Consider: liquidity lock-in, administrative burden, exit planning

---

## Template 8: Freelance Break-even

### Inputs from profile
- `current_salary_gross`: float
- `target_daily_rate`: float
- `working_days_per_year`: int (typically 220 billable)
- `expected_billable_pct`: float (0.6-0.8 typical for solo)

### Calculation steps

**Employee equivalent package (total cost to employer)**:
```
# What does employee actually cost — including all hidden benefits
salary_net = salary_gross × (1 - 0.1975 - avg_income_tax_rate)
vacation_value = salary_gross / 52 × 6  # 30 days paid leave
sick_pay_value = salary_gross × 0.02    # ~5 sick days
employer_kv_contribution = salary_gross × 0.0775  # half of GKV
employer_rv = salary_gross × 0.093
employer_av = salary_gross × 0.013
total_package = salary_gross + employer_kv_contribution + employer_rv + employer_av + vacation_value
```

**Freelance true income**:
```
billable_days = working_days_per_year × expected_billable_pct
gross_revenue = billable_days × daily_rate
business_expenses = estimate (equipment, insurance, BU, accountant, software)
freelance_gross_profit = gross_revenue - business_expenses

# Self-employed KV costs
if gkv: kv_cost = min(freelance_gross_profit, bbg_gkv) × 0.157
else: pkv_cost = based on profile

# Income tax (no splitting advantage if single)
income_tax_freelance = income_tax(freelance_gross_profit - kv_cost - ruerup)
freelance_net = freelance_gross_profit - kv_cost - income_tax_freelance
```

**Break-even daily rate**:
```
# Find daily_rate where freelance_net = salary_net
# Typical rule of thumb: daily_rate ≥ monthly_salary / 10
```

### Output format
```
═══ Freelance vs. Employment Break-even ═══

Your current package (true cost):
  Salary gross:             €[salary]
  + Hidden employer costs:  €[hidden]
  Total employment cost:    €[total]
  Your net after tax:       €[net]

At your target rate €[rate]/day ([billable_pct]% billable, [days] days):
  Gross revenue:            €[revenue]
  - Expenses:               €[expenses]
  - Self-employed KV:       €[kv]
  - Income tax:             €[tax]
  Freelance net:            €[freelance_net]

Compared to employment: [better/worse by €X]
Break-even rate: €[break_even]/day

Risk premium to consider: [non-billable periods, no sick pay, no employer KV]
```

---

## Template 9: Rent vs. Buy

### Inputs
- `property_price`: float
- `monthly_rent_current`: float
- `equity_available`: float
- `mortgage_rate`: float
- `marginal_tax_rate`: float
- `bundesland`: str (for Grunderwerbsteuer)

### Calculation steps

**Buy costs**:
```
grunderwerbsteuer_rates = {
    "Bayern": 0.035, "Sachsen": 0.035, "Hamburg": 0.045,
    "Berlin": 0.06, "Brandenburg": 0.065, "Schleswig-Holstein": 0.065,
    # ... etc
}
transaction_costs = (
    property_price × grunderwerbsteuer_rates[bundesland] +
    property_price × 0.015 +  # Notar + Grundbuch typically 1.5%
    property_price × 0.035    # Makler 3.5% if applicable
)
mortgage_principal = property_price - equity_available
monthly_mortgage = pmt(mortgage_rate/12, 300, -mortgage_principal)  # 25 years
monthly_interest = mortgage_principal × mortgage_rate / 12  # first month
monthly_repayment = monthly_mortgage - monthly_interest

# Ownership opportunity cost
equity_opportunity_cost = equity_available × 0.04 / 12  # 4% ETF return foregone
```

**Annual cost comparison**:
```
buy_annual_cost = (monthly_mortgage + monthly_maintenance + property_tax/12
                  + equity_opportunity_cost/12) × 12

rent_annual_cost = monthly_rent × 12
```

**Break-even (years to buy being better)**:
Break-even occurs when: property appreciation + savings on rent > transaction costs + ownership premium

### Note
For rented-out property, the calculation changes entirely — AfA, interest deduction, and rental income all enter the equation.

---

## Template 10: Retirement Income Sequencing

### Inputs from profile
- `gesetzliche_rente_monthly`: float
- `betriebliche_rente_monthly`: float
- `riester_rente_monthly`: float
- `capital_assets`: float (ETF/savings)
- `rente_beginn_year`: int
- `bundesland`: str

### Calculation steps

**Tax on each income type in retirement**:

GRV (gesetzliche Rente):
```
besteuerungsanteil = get_besteuerungsanteil(rente_beginn_year)
taxable_rente = gesetzliche_rente × besteuerungsanteil
```

bAV Rente: **fully taxable** as Einkünfte aus nichtselbständiger Arbeit (pre-tax contributions)

Riester Rente: **fully taxable** (contributions were tax-advantaged)

Capital drawdown from ETF/savings:
```
# Only the gain portion is taxable (Abgeltungsteuer 25%)
# Principal is tax-free
# Günstigerprüfung applies if personal rate < 25%
```

**Sequencing strategy**:
1. Fill Grundfreibetrag + Sparer-Pauschbetrag with pension income
2. Draw down fully-taxable sources (bAV, Riester) when marginal rate lowest
3. Use capital gains Günstigerprüfung if personal rate still < 25%
4. Keep ETFs growing until forced to draw; prefer capital over pension income in low-rate years

### Output format
```
═══ Retirement Income Sequencing ═══

Monthly income sources:
  GRV (Besteuerungsanteil [X]%):    €[taxable]/month taxable
  bAV:                               €[bav]/month fully taxable
  Riester:                           €[riester]/month fully taxable
  Capital drawdown:                  €[capital]/month (only gains taxable)

At age 67 estimated annual tax: €[tax]
Marginal rate: [X]%

Optimization: [draw bAV before Riester to empty higher-tax bucket first]
Estimated lifetime tax saving from sequencing: €[saving]
```
