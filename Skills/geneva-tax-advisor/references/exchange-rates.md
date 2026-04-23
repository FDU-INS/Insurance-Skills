# Exchange Rates for Tax Filing

## Principle
- **Fortune / Debt (balance sheet):** Use **31.12 year-end rate**
- **Income / Expenses (P&L):** Use **annual average rate**

These are DIFFERENT rates. Common mistake to use the same for both.

## Where to Find Official Rates

### Primary source
AFC (Administration fédérale des contributions):
`https://www.ictax.admin.ch/extern/en.html#/ratelist/{YEAR}`

### Convenient summary
Fidinam annual table:
`https://www.fidinam.com/fr/blog/cours-des-devises-suisse-pour-{YEAR}`

## Application Rules

| What you're converting | Which rate |
|---|---|
| Property value (fortune) | 31.12 year-end |
| Remaining mortgage debt | 31.12 year-end |
| Foreign bank account balance | 31.12 year-end |
| Security value (if not on ictax in CHF) | 31.12 year-end |
| Rental income (loyers) | Annual average |
| Maintenance expenses (frais) | Annual average |
| Mortgage interest paid | Annual average |
| Dividends received | Annual average |
| Taxe foncière | Annual average |

## Example: EUR/CHF 2025
- **Year-end (31.12.2025):** 1 EUR = CHF 0.9305
- **Annual average 2025:** 1 EUR = CHF 0.9370

## Example: USD/CHF 2025
- **Year-end (31.12.2025):** 1 USD = CHF 0.79225
- **Annual average 2025:** 1 USD = CHF 0.83065

## GeTax Behavior
- For foreign properties entered with acquisition amount in foreign currency, GeTax may auto-convert using the year-end rate
- Always verify the converted CHF amount matches your manual calculation
- For securities, ictax already provides CHF values — no conversion needed if you use ictax directly
