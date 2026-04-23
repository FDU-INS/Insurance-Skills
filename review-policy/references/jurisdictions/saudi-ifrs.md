---
name: saudi-ifrs-overlay
version: 1.0
description: >
  Jurisdiction overlay for Saudi Arabia Islamic Financial Institutions.
  Apply when jurisdiction = Saudi Arabia, KSA, SAMA, ZATCA, SAR, Tadawul.
regulator: Saudi Arabian Monetary Authority (SAMA) for banks; CMA for capital markets
primary_standard: IFRS as adopted in the Kingdom of Saudi Arabia
shariah_standard: AAOIFI Shariah Standards (voluntary but widely adopted)
zakat_authority: Zakat, Tax and Customs Authority (ZATCA)
author: Panaversity — The AI Agent Factory
---

## GOVERNING FRAMEWORK

Saudi Arabia requires listed companies and licensed banks to apply IFRS as adopted
in the Kingdom of Saudi Arabia. SAMA and the Capital Market Authority (CMA) are
the primary regulatory bodies.

In countries such as Kuwait and Saudi Arabia, Islamic banks' financial statements
are prepared in accordance with IFRS. Al Rajhi Bank — the world's largest Islamic bank
by capital — prepares IFRS-compliant financial statements.

AAOIFI Shariah Standards are widely adopted by Saudi IFIs as Shariah compliance
guidance, but AAOIFI Financial Accounting Standards are NOT mandatory.

---

## INCOME LABELS (KSA CONVENTION)

Saudi IFIs typically use "Murabaha Income" by convention even under IFRS
(because the income nature is clearly a trading profit, not interest).
This is acceptable under IFRS (IFRS does not mandate "interest income" specifically).

| Product | KSA Conventional Label | NEVER Use |
|---|---|---|
| Murabaha | "Murabaha Income" or "Income from Murabaha Financing" | "Interest Income" |
| Ijarah | "Rental Income from Ijarah" | "Finance Lease Income" |
| DM | "Income from Diminishing Musharaka" | "Mortgage Interest" |
| Sukuk | "Income from Sukuk" | "Interest on Bonds" |

---

## ZATCA ZAKAT — MANDATORY

Saudi Arabian IFIs pay zakat to ZATCA (not income tax, for Saudi-owned equity portions).

**ZATCA Zakat Base Formula:**
+ Share capital
+ All reserves (statutory, general, other)
+ Retained earnings (beginning of year)
− Fixed assets (net book value)
− Long-term investments (strategic holdings)
− Unamortised financing costs

Zakat = Zakat Base × 2.5% per lunar year

**Key rules:**
- Foreign-owned equity portions → income tax at 20%, not zakat.
- Saudi-owned portions → zakat replaces income tax.
- For a bank with mixed KSA/foreign ownership: proportionate calculation.
- Zakat is filed annually with ZATCA. Deadline: 120 days after fiscal year-end.
- Zakat is an EXPENSE in the income statement for the Saudi equity portion.

**Zakat journal entry:**
Dr: Zakat Expense [Calculated amount]
Cr: Zakat Payable — ZATCA [Same]

On payment:
Dr: Zakat Payable — ZATCA
Cr: Cash

---

## SAMA REGULATORY REQUIREMENTS

1. **Financial Reporting:** IFRS, supplemented by SAMA-specific prudential reporting.
2. **Capital Adequacy:** Basel III as adopted by SAMA, with IFSB Islamic supplements.
3. **NPF Classification:** SAMA has specific provisioning requirements.
   Apply IFRS 9 ECL in financial statements; SAMA's floor provisions for regulatory capital.
4. **Vision 2030 sukuk:** Follow IAS 32 / IFRS 9 for classification of sukuk issued under
   National Debt Management Centre programme.
5. **Saudi Green Finance Framework:** Saudi sovereign green sukuk follow ICMA Green Bond
   Principles and SC Saudi's Sustainable Finance Framework.

---

## KEY SAUDI REFERENCE INSTITUTIONS

- **Al Rajhi Bank:** World's largest Islamic bank by capital. IFRS financial statements.
  Reference case for Saudi IFI IFRS presentation standards.
- **Saudi National Bank (SNB):** Largest bank by assets (post-merger with Samba).
  Mixed conventional/Islamic products; IFRS.
- **Alinma Bank:** Pure-play Islamic bank. IFRS. Growing retail Islamic franchise.
- **Saudi Investment Bank (SIB):** Islamic banking division within larger bank.
- **Public Investment Fund (PIF):** Issues Vision 2030 sukuk. Ijarah and other structures.

---

## RESPONSE HEADER FOR SAUDI OUTPUTS

Always begin outputs with:
```
GOVERNING FRAMEWORK: IFRS as adopted in KSA — Saudi Arabia (SAMA)
PRODUCT: [product name]
ZAKAT NOTE: [If applicable, note ZATCA zakat applies]
```
