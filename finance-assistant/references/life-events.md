# TaxDE Life Events — Full Tax Impact Guide

Each event is structured as:
- **Immediate**: Tax year of the event
- **Following years**: Strategic implications
- **What most people miss**: The non-obvious insight
- **Deadlines**: Must-not-miss dates
- **Year-end decisions**: Act before December 31
- **Steuerberater needed?**: Yes / No / Maybe

---

## Event 1: Having a Baby

### Immediate impact (year of birth)
- **Kindergeld**: Apply at Familienkasse immediately — NOT automatic. Back-pay only 6 months retroactive. Income threshold abolished since 2023 — everyone qualifies regardless of income.
- **Elterngeld**: Taxable as Lohnersatzleistung → triggers **Progressionsvorbehalt** (raises effective tax rate even though Elterngeld itself is tax-free). This often creates an unexpected Nachzahlung.
- **Steuerklasse**: If you're married, switching the higher earner to Klasse III (and lower earner to V) can significantly improve net Elterngeld, since Elterngeld is calculated on net income. This switch must happen **before** the last month of working before parental leave.
- **Kita costs**: Deductible from birth under §10 Abs. 1 Nr. 5 EStG (2024: 2/3 up to €4,000; 2025+: 80% up to €4,800 per child/year)

### Following years
- Kinderbetreuungskosten deductible until child turns 14
- Kinderfreibetrag Günstigerprüfung becomes relevant as income rises
- Child's Riester: state pays €300 Kinderzulage/year — add child to contract immediately
- Ausbildungsfreibetrag €1,200/year once child is in Ausbildung away from home

### What most people miss
Elterngeld Progressionsvorbehalt creates a tax bill for **both** partners in the year of birth, even the partner who didn't take parental leave — because household income is assessed jointly. Plan ahead: make additional Rürup/Riester contributions in that year to offset the effect.

Also: the Steuerklasse switch for Elterngeld optimization should happen **early in pregnancy**, not after birth. The window is often missed.

### Deadlines
- Kindergeld application: immediately (retroactive maximum 6 months)
- Steuerklasse switch: before last month of employment before Elternzeit
- Riester Kinderzulage: add child by December 31 of birth year (or file by end of year 2 after)

### Year-end decisions
- Maximize Kita payment in current calendar year if child turns 14 early next year (last chance)
- Consider topping up Rürup to offset Progressionsvorbehalt hit

### Steuerberater needed?
Maybe — if Elterngeld Progressionsvorbehalt creates a large bill or if both partners have complex income. DIY is fine for standard employment situations.

---

## Event 2: Getting Married

### Immediate impact (year of marriage)
- Ehegattensplitting applies for the **entire** year of marriage (even if married December 31)
- Must file jointly (Zusammenveranlagung) to get the benefit — it is NOT automatic
- Steuerklasse can be changed from the month after marriage

### Steuerklasse optimization
- **4/4**: Equal monthly withholding, usually small settlement at year-end
- **3/5**: Higher earner gets more net monthly; lower earner gets much less. Creates large settlement risk if income changes.
- **Factor method (Faktorverfahren)**: More accurate monthly withholding, closer to actual tax. Best if both work.
- **Rule of thumb**: 3/5 makes sense when one partner earns >60% of household income. Factor method almost always better than 3/5 for both partners' cashflow.

### Following years
- Joint assessment typically saves €500–€8,000+/year depending on income gap
- The higher the income gap between partners, the larger the Splittingvorteil
- Review Steuerklasse whenever incomes change significantly

### What most people miss
You can still choose between joint (Zusammenveranlagung) and separate (Einzelveranlagung) assessment each year — whichever is better. Separate assessment is almost never better but run the numbers for complex situations (one partner with large losses).

Also: if one partner is self-employed and has Gewerbesteuer, the §35 offset might interact differently with Splittingtarif.

### Deadlines
- File jointly: use `scripts/tax_dates.py` for the exact year-specific deadline. Example: an advised 2024 return is due on 2026-04-30.
- Steuerklasse change: apply to your Wohnsitzfinanzamt; takes effect following month

### Year-end decisions
- Change Steuerklasse in Q4 to optimize January net pay
- If Faktorverfahren, update factors each November for following year

### Steuerberater needed?
Usually no for standard situations. Yes if one partner is self-employed or has foreign income.

---

## Event 3: Divorce / Separation

### Immediate impact
- Separate assessment applies from the year of official separation (Trennungsjahr)
- Steuerklasse reverts: both partners to Klasse I (or Klasse II for custodial parent)
- Last year for Ehegattensplitting: the year BEFORE formal separation (or the year of separation if brief reconciliation — complex)
- Child custody affects: Kinderfreibetrag (transfer possible), Kindergeld payer, Entlastungsbetrag Alleinerziehende

### Following years
- Realsplitting (Anlage U): can deduct up to €13,805 Unterhalt paid to ex-spouse (who must declare it as income)
- Kinderfreibetrag: if child lives with both (50/50), split; if mainly with one parent, can transfer
- Entlastungsbetrag Alleinerziehende: €4,260/year for custodial parent

### What most people miss
The year of separation still counts as a married year for Splittingvorteil if any part of the year was spent together. Don't miss filing jointly for that year.

Realsplitting is often ignored because it requires cooperation — but it can save the payer thousands while only modestly increasing the receiver's tax (if receiver has low income).

### Deadlines
- Kindergeld: notify Familienkasse of custody arrangement immediately
- Steuerklasse change: apply within 4 weeks of separation to avoid overpayment

### Steuerberater needed?
Recommended — especially for Realsplitting, Kinderfreibetrag transfers, and property settlements.

---

## Event 4: Buying Property

### Immediate impact (year of purchase)
- Grunderwerbsteuer (3.5–6.5% depending on state) is NOT deductible for owner-occupiers
- Notarkosten and Maklerprovision are NOT deductible if you live in the property
- If you rent out the property: ALL purchase and ongoing costs become deductible via AfA

### Deductions for rented-out property (Anlage V)
- **AfA (Abschreibung)**: 3% of building value per year for buildings built after 31.12.2022; 2% for older buildings
- **Building value**: Total purchase price minus land value (Bodenrichtwert) — typically 60-80% of purchase price in cities
- **Renovations**: Major renovations in first 3 years can create Anschaffungsnahe Herstellungskosten trap (must be depreciated instead of immediately deducted if >15% of building value)
- **Ongoing**: Mortgage interest, maintenance, Hausgeld, insurance, property tax — all deductible

### Spekulationsfrist
- Sell after **10 years** of ownership: capital gain is completely **tax-free**
- Sell within 10 years: taxable as sonstiges Einkommen at personal rate
- **Exception**: Property you lived in yourself for the 2 years before sale (or the year of sale + 2 previous years)

### What most people miss
AfA begins from the date you could first use the property, not the date of payment. Start AfA immediately even if building work is ongoing.

For rented property: document ALL costs from the first day — Besichtigungsfahrten (inspection trips) are already deductible before you close.

### Deadlines
- Grundbuch transfer: triggers start of 10-year Spekulationsfrist
- AfA: starts with economic transfer (Besitzübergang), usually closing date

### Year-end decisions
- Time renovation invoices before December 31 to deduct in current year
- But watch the 15% Anschaffungsnahe trap if within 3 years of purchase

### Steuerberater needed?
Yes if: multiple properties, large renovation costs, unclear AfA calculation, or sale planning.

---

## Event 5: Going Freelance

### Immediate impact
- Register at Finanzamt with **Fragebogen zur steuerlichen Erfassung** within 1 month of starting
- Freiberufler (§18 EStG) vs. Gewerbetreibender (§15 EStG) — key distinction: Freiberufler exempt from Gewerbesteuer
- Choose Kleinunternehmerregelung (§19 UStG): exempt from VAT if previous year revenue <€25,000 AND current year expected <€100,000
- **EÜR** (Einnahmen-Überschuss-Rechnung): simple income-minus-expenses accounting

### Tax payments to plan for
- **Vorauszahlungen**: Finanzamt will set quarterly prepayments once first year filed
- **Umsatzsteuer Voranmeldungen**: monthly (year 1) or quarterly (if VAT <€7,500/year)
- **Gewerbesteuer**: quarterly advance payments (if Gewerbetreibender)

### Krankenversicherung implications
- Lose employer's KV contribution — must pay both halves yourself
- GKV: income-based (15.8% + Zusatzbeitrag of gross income, up to BBG)
- PKV: age/health-based — often cheaper when young and healthy
- **Mindestbeitrag trap**: GKV charges minimum even if income is low

### What most people miss
Year 1 cash flow crisis: you continue to owe income tax from your employment, PLUS you'll owe it on your freelance income. No employer withholds. You need a tax reserve of ~30-35% of net profit from day one.

Also: your KV costs are deductible as Sonderausgaben — significantly reduces the actual cost.

### Deadlines
- Fragebogen zur steuerlichen Erfassung: ideally within 4 weeks of starting
- First Voranmeldung: typically by the 10th of the following month
- Kleinunternehmer option: must be set when registering; cannot easily switch mid-year

### Steuerberater needed?
Recommended for year 1. Later, many self-employed manage DIY with TaxDE guidance.

---

## Event 6: Starting a Nebenjob

### Thresholds
- **Minijob**: up to **€538/month** (2024) — flat tax paid by employer, you owe nothing extra
- **€538.01–€2,000/month**: Gleitzone — reduced social contributions
- **Above €2,000**: Full sozialversicherungspflichtig

### For the employee
- Minijob: tax handled by employer, NOT declared separately (unless you file voluntarily)
- Above Minijob: declare on Anlage S (selbständig) or Anlage N (second employment)
- Watch for **Steuerprogression**: second job income is taxed at marginal rate (highest bracket of main job)
- Übungsleiterfreibetrag: €3,000/year tax-free if coaching, teaching, caretaking for public benefit (§3 Nr. 26 EStG)
- Ehrenamtspauschale: €840/year tax-free for volunteer work (§3 Nr. 26a EStG)

### What most people miss
Multiple Steuerklassen: if you have two employment jobs, the second is automatically Klasse VI — the highest withholding. You can reclaim this via your tax return, but you need to manage cashflow.

### Steuerberater needed?
No for standard cases. Yes if complex mix of income types.

---

## Event 7: Moving for Work (Umzug)

### Deductions
- **Umzugskostenpauschale**: Single: **€886** (2024); family: **€1,181** — deductible if job-related move
- Above Pauschale: actual costs (movers, double rent, school enrollment fees for children, integration course costs)
- **Conditions**: Primary reason for move must be to shorten commute by at least 1 hour total round-trip OR job requires move

### Doppelte Haushaltsführung (if maintaining old home)
- If you keep primary residence elsewhere and rent near new job:
  - Up to €1,000/month for accommodation near work
  - Meals first 3 months
  - Weekly travel home costs
- **Conditions**: Primary home genuinely maintained (not just registered), contributing substantially to costs

### What most people miss
The Umzugskostenpauschale can be claimed even if the employer pays for the move — as long as you had unreimbursed costs above the flat rate.

### Steuerberater needed?
No for standard cases. Maybe if Doppelte Haushaltsführung is complex.

---

## Event 8: Receiving a Large Bonus

### Fünftelregelung (§34 EStG)
- Treats irregular income (bonus, severance, back pay, certain termination payments) as if spread over 5 years
- **Formula**: Calculate tax on (normal income + 1/5 of bonus) × 5, subtract tax on normal income
- **When it helps**: When the bonus pushes you into a significantly higher bracket
- **When it doesn't help**: Already in Spitzensteuersatz zone; small bonuses

### Year-end offset strategies
- Extra pension contribution before Dec 31: €10,000 Rürup → saves ~€4,200 at 42% rate
- Harvesting investment losses
- Prepaying Handwerker labor invoices (§35a credit)
- Charitable donations in December instead of January

### What most people miss
The Fünftelregelung is automatic if the employer codes the bonus correctly on the Lohnsteuerbescheinigung (Feld 3/10). But employers sometimes don't apply it. Check the withholding statement.

### Steuerberater needed?
Maybe if bonus >€50,000 combined with other complex income.

---

## Event 9: Company Car Offer

### The 1%-Regelung
- **Monthly taxable benefit**: 1% of gross list price (Bruttolistenpreis, not your negotiated price)
- **Commute add-on**: 0.03% of list price × commute km/month
- **Electric / PHEV**: reduced rates
  - Full electric (range >60km / price ≤€70,000): **0.25%** of list price
  - PHEV (range >50km): **0.5%** of list price
  - Other electric/PHEV: **0.5%**

### Fahrtenbuch alternative
- Keep exact log of every trip (date, destination, purpose, km)
- Tax assessed on actual private use % — can be much less than 1%-Regelung
- **Worth it if**: Private use <30% or long commutes relative to list price
- **Risk**: If Fahrtenbuch incomplete, Finanzamt reverts to 1%-Regelung for entire year

### Cash vs. car calculation
- Net cash value of €600/month = €600 × (1 - marginal_rate) × 12 = annual net benefit
- Compare with: car costs of fuel, insurance, maintenance saved

### What most people miss
The gross list price for 1%-Regelung is the manufacturer's full list price — even if you negotiated a 20% discount or it's second-hand. The rule ignores the actual transaction price.

### Steuerberater needed?
No — TaxDE's Scenario Simulator handles this fully.

---

## Event 10: Moving to Germany as Expat

### Tax residency
- **Wohnsitz** (§8 AO): own or rented accommodation → full tax resident from day 1
- **Gewöhnlicher Aufenthalt** (§9 AO): stay >6 months without Wohnsitz → resident retroactive to day 1
- **Full Steuerpflicht**: worldwide income taxable in Germany (Welteinkommensprinzip)

### Double Taxation Agreements (DBA)
- Germany has DBAs with ~100 countries
- **Method**: Freistellungsmethode (exemption) or Anrechnungsmethode (credit)
- **Progressionsvorbehalt**: Exempt foreign income still raises your German tax rate
- EU/EEA: mostly Freistellung; USA: complex (Anrechnung; FATCA complications)

### Arrival year
- Only resident from date of arrival — but worldwide income from day 1 of German residency
- **Werbungskosten**: full-year amounts apply even if only part year
- Pre-arrival income: not German taxable (unless German-source)

### Partial year return
- Can claim full Werbungskosten, Sonderausgaben, Kinderfreibetrag amounts for the months resident
- Grundfreibetrag prorated

### What most people miss
Germany taxes worldwide income. Income from your home country accounts (dividends, rental income) is taxable in Germany even if you've already paid tax there.

US citizens face unique complexity: US also taxes worldwide income → both countries want full income. DBA provides relief but US-specific rules (FBAR, FATCA, RSU sourcing) require specialist advice.

### Steuerberater needed?
Yes for: US citizens, multiple-country situations, equity compensation (RSUs/options), departure planning.

---

## Event 11: Retirement

### Besteuerungsanteil by Rentenbeginn Year
The taxable portion of your gesetzliche Rente (DRV) depends on when you first received Rente:

| Year Rente started | Taxable % |
|--------------------|-----------|
| 2005 | 50% |
| 2010 | 60% |
| 2015 | 70% |
| 2020 | 80% |
| 2024 | 83% |
| 2040 | 100% |

**Note**: Once set, your taxable percentage does not change even as rates rise for later retirees.

### Tax planning in retirement
- **Günstigerprüfung on capital income**: If your income tax rate < 25%, claim refund of Abgeltungsteuer
- **Multiple pension types**: GRV + bAV + Riester all treated differently
- **Part-time work**: €10,908 Grundfreibetrag (2024) — up to this, pension + small work income is tax-free
- **Werbungskosten**: €102 minimum Pauschbetrag for pension; actual costs often higher

### What most people miss
The transition from employee to pensioner is a major simplification — many people over-file or under-file. The Günstigerprüfung for capital income is frequently missed by retirees with savings.

Also: disability upgrade to GdB 50 is worth pursuing if health deteriorates — Behinderungspauschbetrag €1,140/year adds up.

### Steuerberater needed?
Maybe — for first 2-3 years of retirement to set up the right structure. DIY once established.

---

## Event 12: Inheritance / Gift

### Freibeträge (Erbschaft- und Schenkungsteuer)
| Relationship | Freibetrag (every 10 years) |
|---|---|
| Spouse / registered partner | €500,000 |
| Child | €400,000 |
| Grandchild (parent deceased) | €400,000 |
| Grandchild | €200,000 |
| Parent (inheritance) | €100,000 |
| Sibling, nephew/niece | €20,000 |
| Other | €20,000 |

### 10-year rule
- The Freibetrag resets every 10 years → gifts can be repeated to multiply tax-free transfers
- Strategy for large estates: structured gifting over multiple decades

### Property exemption
- Hauptwohnstätte inherited by spouse/registered partner: **completely tax-free** if occupied immediately and for at least 10 years
- Child inheriting parent's home: exempt up to 200 m² if lived in immediately for 10 years

### Income tax implications
- Inheritance itself: Erbschaftsteuer is a separate tax (not income tax)
- Income FROM inherited assets: fully income taxable (dividends, rental, capital gains)
- **Stepped-up basis**: Germany does NOT provide stepped-up basis — inherited assets carry original acquisition cost for Spekulationsfrist and capital gains

### What most people miss
The Schenkung strategy: gift €400,000 to each child every 10 years — a family with 2 children can transfer €1.6M tax-free over two 10-year windows.

Also: large estates with business assets may qualify for Betriebsvermögen exemptions — specific rules, definitely get advice.

### Steuerberater needed?
Yes for any significant inheritance. The Erbschaftsteuererklärung has a mandatory deadline (3 months from knowledge of inheritance).
