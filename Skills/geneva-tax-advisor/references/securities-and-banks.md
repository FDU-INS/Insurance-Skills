# Securities & Bank Accounts

## Bank Account Fields in GeTax (F2)
For each bank account, GeTax asks:
- **Intérêts bruts soumis à l'impôt anticipé** — Gross interest WITH withholding tax deducted (35% above CHF 200 threshold)
- **Intérêts bruts non soumis à l'impôt anticipé** — Gross interest WITHOUT withholding tax (below threshold or foreign accounts)
- **Solde du compte au 31 décembre** — Balance at year-end → goes to Fortune column
- **Frais bancaires** — Bank management/account fees (enter as POSITIVE value, GeTax deducts automatically). This is a deductible expense against wealth income!
- **Intérêts échus de capitaux d'épargne** — Accrued savings interest
- **Impôt anticipé** — Withholding tax amount (for reclaim)

**Key rule:** Enter ALL fees from your bank statements (frais de gestion, frais de compte). They reduce your taxable wealth income.

## Bank Accounts (F2)

### What to declare
Every bank/postal account worldwide as of 31.12:
- Current accounts (checking)
- Savings accounts (Livret A, épargne, etc.)
- Brokerage cash balances (IBKR, Fidelity, etc.)
- Foreign accounts (convert to CHF at 31.12 rate)

### What NOT to declare here
- **Pillar 3a accounts** — exempt during constitution, declared only on 3a deduction page
- **Pillar 2 (LPP)** — not declared in fortune

### Per account, enter:
- Bank name and location
- Account number
- Balance at 31.12
- Interest earned during year (if any)

## Securities (F3)

### Use ictax for fiscal values
**Always use ictax.admin.ch** for:
- Share/fund values at 31.12 (Kurswert/valeur fiscale) — NOT broker's market close price
- Taxable income per share (zu versteuernder Ertrag) — NOT gross dividend

URL pattern: `https://www.ictax.admin.ch/extern/en.html#/security/{ISIN}/{YYYYMMDD}`

### Why ictax matters
- ictax values can differ from market close (usually in your favor for fortune)
- For fund income: "zu versteuernder Ertrag" is LOWER than gross dividends because capital gains distributions are tax-free for Swiss private investors
- Using broker statements instead of ictax = overpaying tax

### Per security, enter:
- Name, ISIN, number of shares at 31.12
- Fiscal value per share (from ictax) × number = total fortune value
- Taxable income (from ictax) × number = total rendement
- Currency + conversion rate

## DA-1 vs RSI (Foreign Dividend Tax Reclaim)

### DA-1 (Demande de dégrèvement d'impôt anticipé)
**Use when:** Foreign broker (IBKR, Fidelity, DEGIRO, etc.) withheld tax at treaty rate

For US securities via foreign broker:
- US withholds 15% (treaty rate)
- You reclaim this 15% via DA-1
- Settings in GeTax: ☑ DA-1, Pays: États-Unis, Pourcentage: 15.00, Montant: LEAVE BLANK (auto-calculated)

### RSI (R-US 164 — Récupération supplémentaire d'impôt)
**Use when:** Swiss broker (Swissquote, UBS, PostFinance, etc.) withheld additional Swiss tax on top of US withholding

- Total 30% was withheld (15% US + 15% Swiss additional)
- RSI reclaims the Swiss additional 15%
- Only applies to Swiss-domiciled custodians

### CRITICAL RULES
- **Never check both DA-1 and RSI** for the same security
- DA-1 = foreign broker, RSI = Swiss broker — they are mutually exclusive
- If unsure which broker type: check where the shares are custodied

### ESPP & RSU
- **RSU income:** Declared as employment income (field 5 in Annexe A), already included in salary certificate
- **ESPP discount:** Employment income at purchase date
- **ESPP/RSU shares held:** Declare in securities at ictax fiscal value
- **Capital gains on sale:** Tax-free for Swiss private investors (no entry needed)

## Exchange Rates for Securities

### Where to find official rates
- ictax.admin.ch → shows rates used for each security
- fidinam.com → annual summary table
- AFC (Administration fédérale des contributions) → official source

### Which rate to use
| Item | Rate |
|---|---|
| Security value (fortune) | 31.12 year-end rate |
| Dividend income | Annual average rate |
| Interest income | Annual average rate |
| Foreign account balance | 31.12 year-end rate |

## Common Mistakes
1. Using broker market close instead of ictax fiscal values
2. Using gross dividends instead of ictax "taxable income" for funds
3. Checking both DA-1 and RSI for the same security
4. Forgetting to declare foreign brokerage cash balances
5. Declaring Pillar 3a in bank accounts (it's exempt)
6. Not declaring ESPP shares after purchase
7. Forgetting bank custody fees (frais de garde) — these are deductible!
