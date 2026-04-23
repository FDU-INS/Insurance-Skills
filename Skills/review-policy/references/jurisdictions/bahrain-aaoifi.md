---
name: bahrain-aaoifi-overlay
version: 1.0
description: >
  Jurisdiction overlay for Bahrain Islamic Financial Institutions.
  Apply when jurisdiction = Bahrain or Central Bank of Bahrain (CBB).
  Modifies product SKILL.md outputs to conform to AAOIFI FAS mandatory regime.
regulator: Central Bank of Bahrain (CBB)
primary_standard: AAOIFI Financial Accounting Standards (mandatory)
shariah_standard: AAOIFI Shariah Standards (mandatory)
author: Panaversity — The AI Agent Factory
---

## GOVERNING FRAMEWORK

AAOIFI Financial Accounting Standards are MANDATORY for all Islamic financial institutions
licensed by the Central Bank of Bahrain.

The CBB Rulebook (Volume 2 for Islamic banks) incorporates AAOIFI requirements.
AAOIFI Shariah Standards are mandatory for product structuring.
IFRS is NOT the primary standard for Bahraini IFIs.

Where AAOIFI FAS does not address a specific transaction, apply IFRS as guidance
(not as a mandatory override).

---

## INCOME LABELS (MANDATORY — OVERRIDE IFRS DEFAULTS)

| Product | Correct Label | NEVER Use |
|---|---|---|
| Murabaha | "Murabaha Income" | "Interest Income," "Financing Income" |
| Ijarah | "Ijarah Income" or "Rental Income from Ijarah" | "Lease Income," "Finance Lease Income" |
| Diminishing Musharaka | "Musharaka Rental Income" | "Home Finance Income," "Mortgage Income" |
| Mudaraba | "Income Distributed to Investment Account Holders" | "Interest on Deposits" |
| Musharaka | "Income from Musharaka" | "Interest," "Dividend" (unless equity instrument) |
| Sukuk | "Income from Sukuk Investments" or "Return on Sukuk" | "Interest on Bonds" |

---

## BALANCE SHEET PRESENTATION (MANDATORY)

**Assets — NEVER use "Loans and Advances":**
- Murabaha receivables → "Murabaha Receivables"
- Ijarah assets → "Ijarah Assets" (net of accumulated depreciation)
- DM investments → "Diminishing Musharaka Investments"
- Musharaka → "Musharaka Investments"
- Sukuk (HTM equivalent) → "Investments in Sukuk"

**Liabilities — Exclude IAH from liability section:**
Investment Account Holders' funds → separate section:
"Equity of Investment Account Holders" — between liabilities and shareholders' equity.

**Shareholders' equity section:**
Standard equity components (share capital, retained earnings, reserves) —
separate from IAH equity above.

---

## CBB RULEBOOK REQUIREMENTS

1. **CBB Prudential Information Return (PIR):** Submit quarterly using AAOIFI-based line items.
2. **CBB Disclosure Standards (Module PD):** Annual public disclosure including Shariah
   compliance report, SSB composition, and SSB opinion on financial statements.
3. **Capital Adequacy:** Apply IFSB (Islamic Financial Services Board) capital adequacy
   standards as adopted by CBB. IFSB-15: Revised Capital Adequacy Standard.
4. **Non-performing finance:** Follow AAOIFI FAS 30 classification (Stage 1/2/3).
   CBB's minimum provisioning rates apply.
5. **Profit Equalization Reserve and Investment Risk Reserve:** Disclose separately.
   CBB has specific limits on PER and IRR builds.

---

## MANDATORY SSB DISCLOSURES (AAOIFI GOVERNANCE STANDARDS)

Include in EVERY Bahraini IFI annual report:
1. Shariah Supervisory Board composition (names, qualifications, independence)
2. SSB report: opinion on the IFI's compliance with Shariah rules for the year
3. Fatwa references for all significant products offered
4. Non-Shariah income received (if any) and disposal as charity (sadaqah)
5. Zakat: amount payable / paid, basis of calculation, recipients

---

## AAOIFI FAS REFERENCE — BAHRAIN MANDATORY STANDARDS

| Product | Governing FAS |
|---|---|
| Murabaha | FAS 2 |
| Mudaraba (investment accounts) | FAS 3 |
| Musharaka and DM | FAS 4 |
| Salam | FAS 7 |
| Ijarah and IMB | FAS 32 (supersedes FAS 8) |
| Istisna'a | FAS 10 |
| Investments | FAS 25 |
| Sukuk issuance | FAS 33 |
| Impairment | FAS 30 |
| Zakat and Charity | AAOIFI Governance Standard 9 |

---

## RESPONSE HEADER FOR BAHRAIN OUTPUTS

Always begin outputs with:
```
GOVERNING FRAMEWORK: AAOIFI FAS [X] — Bahrain (CBB Mandatory)
PRODUCT: [product name]
```
