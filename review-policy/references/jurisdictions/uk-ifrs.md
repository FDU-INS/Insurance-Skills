---
name: uk-ifrs-overlay
version: 1.0
description: >
  Jurisdiction overlay for UK Islamic Financial Institutions.
  Apply when jurisdiction = UK, United Kingdom, England, PRA, FCA, GBP, Sterling.
regulator: Prudential Regulation Authority (PRA) and Financial Conduct Authority (FCA)
primary_standard: IFRS (FRS 101/102 for smaller entities)
tax_authority: HM Revenue and Customs (HMRC)
author: Panaversity — The AI Agent Factory
---

## GOVERNING FRAMEWORK

In the United Kingdom, all financial institutions — including the five fully-fledged
Islamic banks — are required to use IFRS. There is NO separate Islamic accounting
framework; PRA/FCA regulations apply equally to Islamic and conventional banks.

UK Islamic banks: Al Rayan Bank (largest), Gatehouse Bank, QIB (UK),
Al Ahli United Bank (UK), Bank of London and the Middle East (BLME).

AAOIFI: No mandatory status. Used voluntarily for internal Shariah governance only.

---

## HMRC ALTERNATIVE FINANCE ARRANGEMENTS — CRITICAL TAX RULES

HMRC has enacted specific tax legislation (Finance Acts 2005–2009) to ensure
Islamic finance products receive tax treatment equivalent to their conventional counterparts.
This is the most important UK-specific rule for Islamic finance advisers.

**Key HMRC equivalence rules:**

| Islamic Product | HMRC Tax Treatment | Legislation |
|---|---|---|
| Murabaha | Mark-up treated as interest for tax; bank pays corporation tax on "interest" equivalent | Finance Act 2005 |
| Diminishing Musharaka | Rental treated as interest (deductible for borrower, taxable for bank) | Finance Act 2005 |
| Ijarah / IMB | Rental treated as interest (Finance Act 2005 and SDLT provisions) | Finance Act 2005/2006 |
| Sukuk (Alternative Finance Investment Bonds) | Distributions treated as interest; issuer gets tax deduction | Finance Act 2007 |
| UK Sovereign Sukuk | AFIB treatment applies | Finance Act 2007 |

**SDLT (Stamp Duty Land Transfer) Relief:**
Islamic mortgages (DM structures) are exempt from double SDLT — the SDLT that
would otherwise arise because (1) the bank buys the property and (2) then transfers to customer.
Finance Act 2003 s71A-s73 provides relief: SDLT on one transfer only.

**Advisory obligation:** When advising UK clients on Islamic finance:
Always note HMRC's equivalence position. The Islamic label does not change tax treatment.
Murabaha profit IS "interest" for UK corporation tax and income tax purposes.

---

## PRA/FCA REGULATORY FRAMEWORK

**Capital Requirements:** UK Islamic banks apply the same Basel III / UK CRR capital
requirements as conventional banks. No Islamic-specific capital treatment.
The PRA does not grant concessions for Shariah-based structures.

**IFSB guidance:** The PRA does not adopt IFSB standards. UK Islamic banks
operate under standard Basel III / UK CRR framework.

**Investment Account Holders:** Because UK Islamic banks apply IFRS, IAH deposits
are classified as financial liabilities under IAS 32. The PRA requires them to be
included in total regulatory liabilities. There is no "Equity of IAH" presentation.

**Financial Promotions:** FCA Consumer Duty (July 2023) requires Islamic banking
products to be clearly described. Cannot mislead consumers about the nature
of the arrangement. "No interest" marketing is acceptable if accurate, but must
not create misunderstanding about costs (mark-up / profit rate must be disclosed).

---

## INCOME LABELS (UK IFRS)

| Product | UK Label | NEVER Use |
|---|---|---|
| Murabaha | "Profit from Home Finance" or "Income from Islamic Financing" | "Interest" |
| DM | "Profit from Home Finance" | "Mortgage Interest" |
| Ijarah | "Financing Income — Ijarah" | "Lease Interest" |
| Sukuk | "Income from Islamic Investments" | "Bond Interest" |

Note: HMRC treats all of the above as interest for TAX purposes even though
the accounting label and product documentation avoid the word "interest."
This distinction between accounting characterisation and tax characterisation
is unique to the UK and must be flagged in all UK advisory work.

---

## KEY UK REFERENCE INSTITUTIONS

- **Al Rayan Bank:** Largest UK Islamic bank. IFRS financial statements. Reference case.
- **Gatehouse Bank:** UK Islamic bank focused on buy-to-let. IFRS.
- **BLME (Bank of London and the Middle East):** Corporate and institutional Islamic bank.
- **UK Sovereign Sukuk:** Issued 2014 (GBP 200M), 2021 (GBP 500M). AFIB structure.
  Listed on London Stock Exchange.

---

## RESPONSE HEADER FOR UK OUTPUTS

Always begin outputs with:
```
GOVERNING FRAMEWORK: IFRS — United Kingdom (PRA/FCA)
PRODUCT: [product name]
HMRC NOTE: [note HMRC tax equivalence treatment if advisory context]
```
