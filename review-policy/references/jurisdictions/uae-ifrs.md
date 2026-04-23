---
name: uae-ifrs-overlay
version: 1.0
description: >
  Jurisdiction overlay for UAE Islamic Financial Institutions.
  Apply when jurisdiction = UAE, Dubai, Abu Dhabi, CBUAE, DIFC, ADGM, AED.
regulator: Central Bank of UAE (CBUAE); DFSA for DIFC entities; FSRA for ADGM entities
primary_standard: IFRS
shariah_standard: AAOIFI Shariah Standards (voluntary for CBUAE-licensed; voluntary in DIFC)
author: Panaversity — The AI Agent Factory
---

## GOVERNING FRAMEWORK

The UAE Central Bank requires all licensed banks and financial institutions to apply IFRS.
Dubai Islamic Bank — the world's second largest Islamic bank — prepares IFRS financial statements.

The Dubai International Financial Centre (DIFC) and Abu Dhabi Global Market (ADGM)
are separate financial free zones with their own regulatory frameworks (DFSA and FSRA respectively).
DIFC/ADGM entities also apply IFRS, but AAOIFI standards may be voluntarily used.

---

## INCOME LABELS (UAE IFRS CONVENTION)

| Product | UAE Label | NEVER Use |
|---|---|---|
| Murabaha | "Financing Income — Murabaha" or "Islamic Financing Income" | "Interest Income" |
| Ijarah | "Income from Islamic Financing — Ijarah" | "Interest" |
| DM | "Profit from Home Finance" | "Mortgage Interest" |
| Sukuk | "Income from Islamic Investments" | "Interest on Bonds" |

---

## CBUAE REGULATORY REQUIREMENTS

1. **Financial Reporting:** IFRS mandatory. CBUAE has specific reporting templates.
2. **Capital Adequacy:** UAE adopts Basel III + IFSB Islamic banking supplements.
3. **IFSB-15:** Capital adequacy for Islamic banking windows within conventional groups.
4. **NPF Classification:** CBUAE's classification and provisioning circular applies.
   IFRS 9 ECL governs financial statements; CBUAE sets minimum regulatory provisions.
5. **CBUAE Consumer Finance Framework:** Governs Islamic home finance products.
6. **Zakat:** Not mandatory for UAE IFIs. Voluntary disclosure only.

## DIFC-SPECIFIC NOTES

DIFC entities are regulated by the DFSA (Dubai Financial Services Authority).
IFRS is mandatory for DIFC entities.
AAOIFI Shariah standards may be applied voluntarily as internal governance.
DIFC courts apply common law; Shariah compliance is contractual, not statutory.

---

## UAE VISION 2031 AND ISLAMIC FINANCE

UAE aims to lift Islamic banking assets to AED 2.56 trillion by 2031.
Key drivers: Dubai Islamic Economy Development Centre initiatives,
Expo 2020 legacy projects, green sukuk for sustainability projects.

For green sukuk issued under UAE sustainable finance frameworks:
- Apply IAS 32 / IFRS 9 for classification (same as standard sukuk)
- Add Use of Proceeds disclosures per ICMA Green Bond Principles
- CBUAE Sustainable Finance Framework provides additional guidance

---

## KEY UAE REFERENCE INSTITUTIONS

- **Dubai Islamic Bank (DIB):** World's second largest Islamic bank. IFRS. Reference case.
- **Abu Dhabi Islamic Bank (ADIB):** Major UAE Islamic bank. IFRS.
- **Emirates Islamic:** Islamic subsidiary of Emirates NBD. IFRS.
- **Noor Bank** (merged into DIB): Former standalone Islamic bank.

---

## RESPONSE HEADER FOR UAE OUTPUTS

Always begin outputs with:
```
GOVERNING FRAMEWORK: IFRS — UAE (CBUAE) [or DIFC/DFSA if applicable]
PRODUCT: [product name]
```
