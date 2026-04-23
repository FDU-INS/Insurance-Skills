# TaxDE Freelancer Guide — Self-Employment in Germany

---

## 1. Freiberufler vs. Gewerbetreibender

### The decisive question: §18 vs. §15 EStG

**Freiberufler (§18 EStG)** — no Gewerbesteuer:
- Listed "catalog professions": doctors, lawyers, architects, engineers, tax advisors, journalists, authors, musicians, artists, teachers, scientists
- Or: comparable activity requiring special professional knowledge and personal involvement
- Key test: Is the work based on **personal, creative, specialized expertise**?

**Gewerbetreibender (§15 EStG)** — subject to Gewerbesteuer:
- Commercial activity (Gewerbebetrieb)
- IT developers: often treated as Freiberufler if solving problems creatively, but debated
- Copywriters/consultants: often Freiberufler
- Online shops, resellers, any buying/selling: always Gewerbetreibender

**Gray areas for IT**:
- Software developer (creative, problem-solving): likely Freiberufler
- IT support/maintenance: likely Gewerbetreibender
- Project manager without technical implementation: debated
- Test: Finanzamt looks at actual work content, not job title

**What Finanzamt decides**: Fill out Fragebogen accurately. If misclassified, Finanzamt may retroactively assess Gewerbesteuer + interest.

---

## 2. Registration Process

### Fragebogen zur steuerlichen Erfassung (FSE)

Filing deadline: Within 1 month of starting self-employment (no hard penalty but recommended).

**Online**: via ELSTER (mein.elster.de) — submit digitally
**Paper**: Download from your Finanzamt website

**Critical decisions in the Fragebogen**:

1. **Kleinunternehmerregelung**: §19 UStG — claim exemption from VAT
   - Expected revenue this year: <€100,000 (threshold for current year)
   - Revenue last year (or startup year): <€25,000
   - **See Section 3 for decision guide**

2. **Buchführungspflicht**: Select EÜR (Einnahmenüberschussrechnung) unless revenue >€600,000 or profit >€60,000 (threshold for mandatory Bilanzierung — rarely applicable to freelancers)

3. **Vorauszahlungen**: Estimated quarterly income tax payments — set conservatively in year 1 to avoid large bill

**After submitting FSE**:
- Finanzamt sends **Steuernummer** (within 2-6 weeks)
- For Gewerbetreibende: **Gewerbeanmeldung** at Gewerbeamt is ALSO required
- VAT registration (if not Kleinunternehmer): Umsatzsteuer-Identifikationsnummer from Bundeszentralamt für Steuern (automatically or on request)

---

## 3. Kleinunternehmerregelung (§19 UStG) — Decision Guide

### Qualify if:
- Revenue in previous year ≤ €25,000
- Expected revenue in current year ≤ €100,000

### Should you opt in?

**Opt IN (use Kleinunternehmer) if**:
- Your clients are primarily private individuals (B2C) — they cannot reclaim VAT
- Your clients are small businesses without VAT recovery (doctors, other Kleinunternehmer)
- Your own business costs are low (little input tax to reclaim)
- You want simplicity (no monthly Voranmeldungen)

**Opt OUT (regular VAT) if**:
- Your clients are primarily businesses (B2B) with full VAT recovery — they don't care about your 19%
- You have significant business purchases with input tax (office equipment, software, travel)
- You expect to grow past €25,000 quickly — forced switch mid-year is administratively painful
- You invoice internationally (B2B EU invoices are 0% VAT regardless)

**Break-even calculation**:
```
Input tax recoverable per year: [sum of VAT on your business purchases]
If input_tax > 0.19 × your_invoiced_revenue → opt out
If input_tax < 0.19 × revenue → often opt in (simpler, no cash flow timing issue)
```

**Once opted out**: Must stay out for at least 5 years (Bindungsfrist for voluntary waiver)

---

## 4. EÜR Structure

### Income Categories (Betriebseinnahmen)
- Umsatzerlöse (revenue)
- Umsatzsteuer vereinnahmt (VAT collected — if not Kleinunternehmer)
- Sonstige Betriebseinnahmen (other: refunds, insurance payouts, grants)

### Expense Categories (Betriebsausgaben)
Key deductible categories:
```
Büromaterial und Porto           Office supplies, postage
Telekommunikation                Phone, internet (100% if dedicated business line)
EDV-Kosten / Software            Software subscriptions, cloud tools
Literatur und Fachliteratur      Professional books, journals, online databases
Reisekosten                      Business travel (Fahrtkosten, Verpflegung, Unterkunft)
Bewirtungskosten                 Business meals (70% deductible)
Büro- und Raumkosten             Office rent (if separate office) or Arbeitszimmer proportion
AfA (Abschreibungen)             Depreciation on assets >€800 net
Gewerbesteuer                    Fully deductible as Betriebsausgabe
Beiträge und Versicherungen      Professional liability insurance, BU
Beratungskosten                  Steuerberater fees, legal fees
Fortbildung                      Training, conferences, courses
Werbung und Marketing            Website, ads, business cards
Bankgebühren                     Business account fees
Krankenversicherung (anteilig)   Self-employed KV as Sonderausgaben (not EÜR — separate)
```

### Common EÜR mistakes
1. **Mixing private and business**: Use a separate bank account for business
2. **Forgetting home office proportion**: If Arbeitszimmer, calculate rental proportion
3. **KV as EÜR cost**: GKV/PKV goes to Sonderausgaben, not EÜR
4. **Vorauszahlungen as cost**: Income tax prepayments are NOT a business expense
5. **Gewerbesteuer timing**: Deductible when paid, not when assessed
6. **Missing input tax**: Don't forget to track recoverable VAT separately

---

## 5. Depreciation Rules (AfA)

### GWG (Geringwertige Wirtschaftsgüter)
- **Net value ≤€250**: Fully expense in year of purchase (Sofortabschreibung)
- **€251–€800**: Fully expense in year of purchase (GWG — Geringwertige Wirtschaftsgüter)
- **>€800 net**: Depreciate over useful life (see table)

**Note**: Businesses can elect "Pool method" for items €251–€1,000 net (amortize pool over 5 years). Individual method (depreciate each item separately) is usually more favorable.

### Useful Life Table (Abschreibungstabelle — common items)
| Item | Years |
|------|-------|
| Laptop / Desktop computer | 3 |
| Tablet | 3 |
| Smartphone | 3 |
| Monitor | 3 |
| Printer / Scanner | 3 |
| Webcam / Headset | 3 |
| Server | 3 |
| External hard drive | 3 |
| Camera (professional) | 7 |
| Desk | 13 |
| Office chair | 13 |
| Bookshelf | 15 |
| Car | 6 |
| Bicycle (business) | 7 |
| Commercial software | 3 |

**Partial year**: In the year of purchase, prorate by months remaining. E.g., bought in October: 3 months / 12 = 25% of annual AfA.

---

## 6. Business Travel

### Fahrtkosten (Transportation)
- **Own car**: €0.30/km (or actual costs with Fahrtenbuch — rarely worth it for self-employed)
- **Public transport**: Actual costs
- **First-class train**: Allowed; reasonable for business
- **Flights**: Actual costs; document business purpose

### Verpflegungsmehraufwand (Meal Allowances — tax-free)
```
Absence 8–24 hours:   €14/day
Full day away:        €28/day
First/last day:       €14/day (if overnight)
Note: Only for absence from home >8 hours AND not just commuting
```

### Accommodation: Actual hotel costs (reasonable)

### Business meal documentation:
- Who attended (names), business purpose, date, place
- Must keep all receipts
- 70% deductible (not 100%) for meals with clients/business partners

---

## 7. Gewerbesteuer

### Only for Gewerbetreibende (not Freiberufler)

**Formula**:
```
1. Calculate Gewerbeertrag (similar to income but with add-backs)
2. Deduct Freibetrag: €24,500 (for natural persons/Einzelunternehmen)
3. Multiply by Steuermesszahl: 3.5%
4. Multiply by municipal Hebesatz: varies by city
5. Result = Gewerbesteuer liability
```

**Hebesatz by major city (2024)**:
| City | Hebesatz | Effective rate (on profit) |
|------|----------|--------------------------|
| Berlin | 410% | 14.35% |
| Hamburg | 470% | 16.45% |
| München | 490% | 17.15% |
| Frankfurt | 460% | 16.10% |
| Köln | 475% | 16.63% |
| Stuttgart | 420% | 14.70% |
| Düsseldorf | 440% | 15.40% |
| Hannover | 480% | 16.80% |
| Nürnberg | 427% | 14.95% |
| Dresden | 390% | 13.65% |
| Leipzig | 430% | 15.05% |

**§35 EStG offset**: Gewerbesteuer is credited against income tax: 4 × Messbetrag deductible from income tax.
Effective combined rate on freelance profit (Gewerbetreibende):
- At marginal rate 42% + Gewerbesteuer Berlin: ~48-52% combined (but offset reduces income tax)
- After §35 offset: typically around 45-48% for most scenarios in major cities

---

## 8. Umsatzsteuer Administration (VAT)

### Voranmeldungen (Advance Declarations)
- **Year 1 and year 2**: Monthly filings (by 10th of following month)
- **From year 3**: If previous year VAT <€7,500 → Quarterly; if <€1,000 → Annual only
- Dauerfristverlängerung: Apply for automatic 1-month extension. One-time 1/11 deposit required.

### Invoice Requirements (Pflichtangaben — mandatory)
All invoices >€250 must include:
1. Full name and address of supplier
2. Full name and address of recipient
3. Steuernummer or Umsatzsteuer-Identifikationsnummer (USt-IdNr.)
4. Invoice date
5. Invoice number (consecutive, unique)
6. Description of service/goods
7. Quantity and unit price
8. Applicable VAT rate (19%, 7%, or 0% for intra-EU B2B)
9. VAT amount or note "Umsatzsteuer wird vom Finanzamt nicht gesondert ausgewiesen" (Kleinunternehmer)
10. Total gross amount

**Invoices ≤€250 (Kleinbetragsrechnungen)**: Simplified requirements (no recipient name needed)

**Reverse charge (§13b UStG)**: When invoicing B2B to other EU member states, issue 0% VAT invoice with note "Steuerschuldnerschaft des Leistungsempfängers". Recipient accounts for VAT in their country.

---

## 9. Krankenversicherung for Self-Employed

### GKV (gesetzliche Krankenversicherung)
- **Rate**: 14.6% base + Zusatzbeitrag (~0.6–2.5% depending on provider) + 3.4% Pflegeversicherung
- **Income base**: Actual income (if low) up to BBG (€62,100 in 2024)
- **Mindestbeitrag (minimum)**:
  - Based on minimum assessment base: €1,178.33/month (2024) even if earning less
  - Minimum monthly KV: ~€200 (varies by Zusatzbeitrag)
- **Trap**: First year of low freelance income still triggers minimum contribution

### PKV (private Krankenversicherung)
- Fixed premium regardless of income
- Typically cheaper for young, healthy freelancers
- **Lock-in risk**: Returning to GKV after PKV requires income drop below Versicherungspflichtgrenze (€69,300 in 2024) — difficult after 45+
- Standard rate comparison tool: pkv.de or independent broker

### Beiträge as Sonderausgaben
- Self-employed can deduct their full KV contributions as Sonderausgaben
- GKV: Total contributions (employer + employee share, since self-employed pay both)
- PKV: Basisabsicherung portion only

---

## 10. Vorauszahlungen (Tax Prepayments)

### When triggered
- First assessment after first year of self-employment → Finanzamt sets quarterly Vorauszahlungen
- Thresholds: income tax >€400/year AND estimated annual income tax >€400

### Quarterly due dates
- March 10
- June 10
- September 10
- December 10

### Reducing Vorauszahlungen
If current year income significantly lower than previous year:
1. File **Antrag auf Anpassung der Vorauszahlungen** with Finanzamt
2. Provide current year income estimate
3. Finanzamt adjusts for remaining quarters
4. **No penalty** for reducing Vorauszahlungen if you had a reasonable basis

### Cash flow planning
**Month 1–12**: Set aside 30-35% of every invoice payment
- ~27-42%: income tax (depending on income level)
- ~1-2%: Kirchensteuer (if applicable)
- ~15-17%: KV (if GKV)
- Note: Social contributions (RV, AV) only if voluntarily contributing

---

## 11. Rürup Deep Dive for Self-Employed

### Why essential
- No employer pension contributions (no bAV without employee)
- Riester benefits often minimal for high earners without children
- Rürup is the main tax-efficient pension vehicle for self-employed

### Net cost calculation
```
Rürup contribution:    €10,000
Tax saving at 42%:    -€4,200 (for high earner)
Net cost:              €5,800
Your future pension includes €10,000 worth of contributions for €5,800 actual cost
```

At marginal rate 45% + Soli: net cost is just €5,195 for €10,000 in pension savings.

### Timing strategy
- **Variable contribution possible**: No minimum; can top up in December
- **December optimization**: If bonus month or good quarter → maximize before Dec 31
- **Bad year**: Contribute minimum or nothing — no obligation
- Carry forward not possible → use it or lose it each year

### Rider options (with main Rürup contract)
- **BU Rider (Berufsunfähigkeit)**: Disability coverage within Rürup — also tax-deductible
- **Premium waiver**: Most quality products include this
- **Avoid**: Expensive fund-based products with high TER — stick to low-cost index fund Rürup

### Providers comparison
Check TER (Total Expense Ratio) — target <0.5%. Compare:
- Condor, myLife, DWS, Volkswohl Bund: generally competitive
- Avoid: expensive bundled bank products, traditional Lebensversicherung-style Rürup

---

## 12. Sozialversicherung: What Self-Employed Don't Pay

### NOT required (unless voluntarily contributing):
- Rentenversicherung (pension): self-employed in most industries not required (except artists, some consultants under §2 SGB VI)
- Arbeitslosenversicherung (unemployment): not available and not required
- Unfallversicherung (accident): only for specific high-risk sectors mandated by Berufsgenossenschaft

### What you DO still pay:
- Krankenversicherung (health): required, GKV or PKV
- Pflegeversicherung (care): required, part of GKV or separate if PKV

### Künstlersozialkasse (KSK)
- Artists and journalists may qualify for subsidized KV via KSK
- KSK pays ~50% of KV/RV contributions
- Freelance writers, designers, photographers, musicians — check eligibility at kuenstlersozialkasse.de
