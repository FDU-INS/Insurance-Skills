---
name: pakistan-ifrs-overlay
version: 1.0
description: >
  Jurisdiction overlay for Pakistan Islamic Financial Institutions.
  Apply when jurisdiction = Pakistan, SBP, SECP, PKR, Pakistani IFI.
regulator: State Bank of Pakistan (SBP) for banks; SECP for NBFCs and capital markets
primary_standard: IFRS (listed entities under Companies Act 2017); AAOIFI supplemental
shariah_governance: SBP Shariah Governance Framework (SGF), revised November 2024
author: Panaversity — The AI Agent Factory
---

## GOVERNING FRAMEWORK

Pakistan's Islamic banks listed on the Pakistan Stock Exchange apply IFRS as required
by the Companies Act 2017 and SECP. Unlisted IFIs may apply AAOIFI supplementally.

Where IFRS does not address a specific Islamic transaction, AAOIFI FAS may be applied
as supplemental guidance. Where AAOIFI and IFRS conflict, IFRS presentation typically
prevails for investor-facing financial statements, with AAOIFI Shariah disclosures added.

**CRITICAL — THE 2028 MANDATE:**
The Federal Shariat Court's April 2022 ruling declared riba unconstitutional.
Parliament has mandated full conversion to Islamic finance by January 2028.
All conventional banking must transition to Shariah-compliant products.
This transition is the most significant event in Pakistan's financial history.

---

## SBP SHARIAH GOVERNANCE FRAMEWORK (SGF) — REVISED NOVEMBER 2024

The SGF (effective January 2025) governs all Islamic Banking Institutions (IBIs):

**Shariah Supervisory Board (SSB) requirements:**
- Minimum 3 scholars; at least one must be a specialist in Islamic jurisprudence
- SSB must be independent; no conflicts of interest
- SSB must review and approve ALL new products before launch
- Annual SSB report must be included in the annual financial statements

**Shariah Audit:**
- Annual internal Shariah audit of all transactions and products
- External Shariah audit (for large IBIs) is encouraged
- Findings must be reported to the Board of Directors

**Non-Shariah income:**
- Any inadvertent non-Shariah income must be donated to charity (sadaqah)
- Cannot be included in retained earnings
- Must be disclosed in the Shariah compliance report

---

## SBP IBD QUARTERLY RETURNS

Pakistan IBIs submit quarterly returns to SBP's Islamic Banking Department (IBD):

**Key return tables:**
1. Balance sheet by product type (Murabaha, DM, Ijarah, Salam, Istisna'a, Running Musharaka)
2. Income statement by product type
3. Financing portfolio by sector (agriculture, SME, consumer, corporate)
4. Non-Performing Financing (NPF) analysis — AAOIFI FAS 30 staging
5. Investment portfolio (GIS, corporate sukuk, equity investments)
6. PER and IRR balances and movements
7. Shariah compliance metrics (non-Shariah income %, Shariah audit completion)

**IBD Quarterly Report deadline:** 10th of the month following quarter-end.

---

## INCOME LABELS (PAKISTAN)

| Product | Pakistan Label | NEVER Use |
|---|---|---|
| Murabaha | "Murabaha Income" | "Interest Income" |
| Ijarah / IMB | "Ijarah Income" or "Rental Income" | "Finance Lease Income" |
| DM | "Diminishing Musharaka Income" or "Home Finance Income" | "Mortgage Income" |
| Sukuk (GIS) | "Income from Government of Pakistan Ijarah Sukuk" | "Interest on T-Bills" |
| IAH | "Profit Distributed to Investment Account Holders" | "Interest on Deposits" |

---

## GOVERNMENT OF PAKISTAN IJARAH SUKUK (GIS)

GIS are sovereign sukuk issued by the Government of Pakistan and managed by SBP.
IBIs are required to maintain Statutory Liquidity Reserves in GIS (not T-Bills).
GIS classification by IBIs: amortised cost (HTC, SPPI pass — fixed certificate rate).
SBP open market operations now use GIS (not conventional T-Bills) for Islamic banks.

---

## SECP SUKUK REGULATIONS

SECP governs corporate sukuk issuance under:
- Sukuk (Privately Placed) Regulations 2017
- Listed Companies (Sukuk) Regulations (for PSX-listed sukuk)

Accounting treatment: apply IFRS 9 (issuer and investor) with SECP disclosure requirements.
Rating: PACRA and VIS Credit Rating Company are the two CRAs for Pakistan sukuk.

---

## ZAKAT (PAKISTAN CONTEXT)

Pakistan's Zakat and Ushr Ordinance 1980 requires source deduction from depositors.
The IFI is an agent, not the zakat payer. See zakat-global.md for details.

---

## RESPONSE HEADER FOR PAKISTAN OUTPUTS

Always begin outputs with:
```
GOVERNING FRAMEWORK: IFRS (listed) / AAOIFI supplemental — Pakistan (SBP SGF)
PRODUCT: [product name]
SBP NOTE: [note any SBP Shariah Governance Framework requirement relevant to the output]
```
