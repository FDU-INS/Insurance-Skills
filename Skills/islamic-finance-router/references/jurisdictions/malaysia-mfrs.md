---
name: malaysia-mfrs-overlay
version: 1.0
description: >
  Jurisdiction overlay for Malaysia Islamic Financial Institutions and corporations.
  Apply when jurisdiction = Malaysia, Bursa Malaysia, Bank Negara Malaysia (BNM),
  Securities Commission Malaysia (SC), MFRS, Ringgit, MYR.
regulator: Bank Negara Malaysia (BNM) for banks; SC Malaysia for capital markets
primary_standard: Malaysian Financial Reporting Standards (MFRS) — IFRS-equivalent
shariah_governance: BNM Shariah Advisory Council (SAC) — supreme authority on Shariah
author: Panaversity — The AI Agent Factory
---

## GOVERNING FRAMEWORK

Malaysia applies MFRS (Malaysian Financial Reporting Standards), which are
substantively word-for-word equivalent to IFRS as issued by the IASB.
MFRS is administered by the Malaysian Accounting Standards Board (MASB).

For Islamic finance transactions, the MASB does NOT issue separate Islamic accounting
standards. Instead, MASB has determined that MFRS (IFRS) applies to Islamic
transactions with appropriate additional disclosures.

The BNM Shariah Advisory Council (SAC) issues rulings that take precedence over
individual IFI Shariah Supervisory Board opinions.

---

## PRODUCT-SPECIFIC MALAYSIA RULES

**Murabaha under MFRS 9:**
- Apply IFRS 9 business model and SPPI tests.
- Murabaha receivables typically classified at AMORTISED COST.
- Income label: "Profit from Islamic Financing" or "Islamic Financing Income" — NOT "interest income."
- MASB guidance: murabaha recognised as financing transaction, profit amortised using effective profit rate.

**Ijarah / IMB under MFRS 16:**
- MFRS 16 (= IFRS 16) applies to all lease arrangements including Islamic structures.
- Lessor: assess finance lease vs. operating lease. IMB typically assessed as finance lease.
- Finance lease: derecognise asset, recognise net investment in lease.
- Lessee: ROU asset + lease liability for all leases except short-term/low-value exemptions.

**Diminishing Musharaka under MFRS 9:**
- Apply IFRS 9. DM home finance typically classified at amortised cost (HTC + SPPI pass).
- Income label: "Profit from Islamic Home Financing" — NOT "mortgage interest."

**Investment Accounts (Mudaraba) under MFRS 132:**
- BNM has determined: Investment Account deposits = financial liabilities under MFRS 132.
- Restricted Investment Accounts: BNM Policy Document on Investment Account governs
  whether these are on or off balance sheet.
- Do NOT present IAH funds as "Equity of Investment Account Holders" (AAOIFI treatment).
- Recognise as financial liabilities at amortised cost.

**Sukuk under MFRS 9:**
- Government Investment Issues (GII) and sovereign sukuk: classify at amortised cost if HTC.
- Corporate sukuk: apply SPPI test.
- Ijarah sukuk: typically SPPI pass → amortised cost or FVOCI.
- Musharakah sukuk: SPPI FAIL → FVTPL.
- Income label: "Income from Sukuk Investments" — NOT "interest income."

**Takaful under MFRS 17:**
- MFRS 17 (= IFRS 17) applies to takaful operators.
- BNM Financial Reporting for Takaful Operators Policy Document provides additional requirements.
- BNM Shariah Advisory Council ruling: MFRS 17 applies to the takaful operator's books.
- Family takaful: GMM model (long-term obligations).
- General takaful: PAA model (typically ≤12 months coverage).
- Participants' Fund is presented as a separate fund within the operator's consolidated accounts.

---

## BNM REGULATORY REQUIREMENTS

1. **Financial Reporting Policy Document:** BNM's binding document specifying financial
   reporting requirements for licensed banks. Supplements MFRS where BNM has specific positions.
2. **Financial Reporting for Takaful Operators Policy Document:** Specific to takaful.
3. **Investment Account Policy Document:** Governs RIA and URIA accounting.
4. **IFSB Capital Adequacy:** BNM has adopted IFSB-15 capital adequacy standards.
5. **Shariah Audit:** All IFIs must conduct annual Shariah audit. Findings disclosed.
6. **SAC Resolutions:** BNM SAC rulings are binding on all licensed Malaysian IFIs.

---

## SC MALAYSIA — CAPITAL MARKET REQUIREMENTS

For sukuk and Islamic fund products:
- SC Guidelines on Islamic Capital Market Products and Services
- SRI Sukuk Framework (Sustainable and Responsible Investment)
- Green Sukuk: Use of Proceeds reporting, Impact Report, SC verification
- Eligible Green Sukuk assets: renewables, green buildings, sustainable transport, water

---

## INCOME LABELS (MALAYSIA SPECIFIC)

| Product | Malaysia Label | NEVER Use |
|---|---|---|
| Murabaha | "Profit from Islamic Financing" | "Interest Income" |
| Ijarah | "Income from Islamic Financing — Ijarah" | "Finance Lease Income" |
| DM | "Profit from Islamic Home Financing" | "Mortgage Interest" |
| Sukuk | "Income from Sukuk Investments" | "Bond Interest" |
| IAH | "Profit Distribution to Investment Account Holders" | "Interest on Deposits" |

---

## RESPONSE HEADER FOR MALAYSIA OUTPUTS

Always begin outputs with:
```
GOVERNING FRAMEWORK: MFRS [X] (IFRS-equivalent) — Malaysia (BNM / SC Malaysia)
PRODUCT: [product name]
SAC RULING: [note if a BNM SAC ruling governs this product]
```
