---
name: qatar-aaoifi-overlay
version: 1.0
description: >
  Jurisdiction overlay for Qatar Islamic Financial Institutions.
  Apply when jurisdiction = Qatar or Qatar Central Bank (QCB).
regulator: Qatar Central Bank (QCB)
primary_standard: AAOIFI Financial Accounting Standards (mandatory)
shariah_standard: AAOIFI Shariah Standards (mandatory)
author: Panaversity — The AI Agent Factory
---

## GOVERNING FRAMEWORK

AAOIFI Financial Accounting Standards are MANDATORY for Islamic financial institutions
licensed by the Qatar Central Bank. Qatar is one of only two jurisdictions globally
(with Bahrain) where AAOIFI is the mandatory primary accounting framework for IFIs.

The Qatar Financial Centre (QFC) Regulatory Authority governs IFIs operating
within the QFC — these entities may use IFRS, but AAOIFI remains the standard
for QCB-licensed institutions.

---

## KEY DIFFERENCES FROM BAHRAIN

Qatar applies the same AAOIFI mandatory framework as Bahrain with minor differences:

**QCB-specific:**
- QCB has its own Shariah governance framework separate from CBB's.
- QCB requires its own SSB review calendar (may differ from CBB schedule).
- Qatar's sovereign sukuk programme (Ministry of Finance) uses ijarah structures.
- Key institutions: Qatar Islamic Bank (QIB), Masraf Al Rayan, Qatar International Islamic Bank.

**IFRS for listed entities:** QIB and Masraf Al Rayan are listed. While AAOIFI is primary,
listed IFIs may also prepare supplementary IFRS disclosures for international investors.
Clarify with client which framework governs the primary financial statements.

---

## INCOME LABELS AND BALANCE SHEET PRESENTATION

Same as Bahrain AAOIFI overlay. Apply all rules from bahrain-aaoifi.md with
the following substitution:
- Regulator references: replace "CBB" with "QCB"
- Rulebook references: replace "CBB Rulebook" with "QCB Instructions"

---

## QCB REGULATORY REQUIREMENTS

1. **QCB Quarterly Returns:** Submit using QCB-specified templates.
2. **Liquidity Coverage Ratio (LCR):** IFSB-based Islamic LCR calculation.
   Qatar GIS (Government of Qatar Ijarah Sukuk) qualify as High Quality Liquid Assets.
3. **Capital adequacy:** IFSB-15 as adopted by QCB.
4. **NPF classification:** QCB minimum provisioning rates apply.

---

## RESPONSE HEADER FOR QATAR OUTPUTS

Always begin outputs with:
```
GOVERNING FRAMEWORK: AAOIFI FAS [X] — Qatar (QCB Mandatory)
PRODUCT: [product name]
```
