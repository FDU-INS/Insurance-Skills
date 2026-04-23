---
name: islamic-finance-router
description: >
  Routes Islamic finance queries to the correct product skill and jurisdiction
  overlay. Activate for any query involving Islamic banking, AAOIFI, Shariah-
  compliant finance, sukuk, takaful, murabaha, ijarah, musharaka, mudaraba,
  salam, istisna'a, zakat, or Shariah screening. Covers 20 jurisdictions
  across 3 accounting regimes (AAOIFI-primary, IFRS with Islamic guidance,
  local standards).
---

## PURPOSE

This is the top-level routing controller for the Islamic Finance Plugin.
It determines which product skill and which jurisdiction overlay to load
before generating any Islamic finance accounting output.
It does NOT contain accounting rules itself. It routes to the files that do.

## ROUTING PROTOCOL — EXECUTE BEFORE ANY OUTPUT

### Step 1: Identify the Jurisdiction

Read the user query for jurisdiction signals:

- Country name (Bahrain, Malaysia, UAE, Saudi Arabia, UK, Pakistan, Nigeria, etc.)
- Currency (BHD, MYR, AED, SAR, GBP, PKR, NGN)
- Regulator name (CBB, BNM, CBUAE, SAMA, PRA/FCA, SBP, CBN)
- Standard reference (AAOIFI FAS, MFRS, IFRS as adopted in KSA, TFRS)

**If no jurisdiction is identifiable: ASK before proceeding.**
Do NOT assume a default jurisdiction. Do NOT assume IFRS.

### Step 2: Identify the Product

Map query terms to product skills:

| Query Terms                                                             | Route To                       |
| ----------------------------------------------------------------------- | ------------------------------ |
| murabaha, cost-plus, deferred sale, commodity murabaha, tawarruq, FAS 2 | murabaha skill                 |
| ijarah, IMB, lease, ijarah muntahia bittamleek, FAS 8, FAS 32           | ijarah-imb skill               |
| diminishing musharaka, DM, home finance, co-ownership                   | musharaka-dm skill             |
| mudaraba, investment account, IAH, PER, IRR, FAS 3                      | mudaraba skill                 |
| musharaka, joint venture, partnership, FAS 4                            | musharaka-full skill           |
| sukuk issuer, sukuk issuance, sukuk structuring, SPV                    | sukuk-issuer skill             |
| sukuk investor, sukuk holding, sukuk classification, SPPI               | sukuk-investor skill           |
| salam, forward purchase, advance payment commodity, FAS 7               | salam skill                    |
| istisna'a, construction finance, manufacturing contract, FAS 10         | istisna-a skill                |
| takaful, Islamic insurance, wakala model, participants fund             | takaful-ifrs17 skill           |
| zakat, zakatable, nisab, ZATCA, sadaqah, purification                   | zakat-global skill             |
| shariah screen, halal stocks, prohibited sectors, PSX screen            | shariah-screening-global skill |

### Step 3: Load the Jurisdiction Overlay

| Jurisdiction                      | Load Overlay                     |
| --------------------------------- | -------------------------------- |
| Bahrain                           | jurisdictions/bahrain-aaoifi.md  |
| Qatar                             | jurisdictions/qatar-aaoifi.md    |
| Malaysia                          | jurisdictions/malaysia-mfrs.md   |
| Indonesia                         | jurisdictions/indonesia-psak.md  |
| Saudi Arabia, KSA                 | jurisdictions/saudi-ifrs.md      |
| UAE, Dubai, Abu Dhabi, DIFC, ADGM | jurisdictions/uae-ifrs.md        |
| Kuwait                            | jurisdictions/kuwait-ifrs.md     |
| Oman                              | jurisdictions/oman-ifrs.md       |
| Pakistan                          | jurisdictions/pakistan-ifrs.md   |
| UK, United Kingdom                | jurisdictions/uk-ifrs.md         |
| Nigeria                           | jurisdictions/nigeria-ifrs.md    |
| Turkey                            | jurisdictions/turkey-tfrs.md     |
| GCC cross-border, multi-GCC       | jurisdictions/gcc-crossborder.md |

### Step 4: Apply Rules in Order

1. Apply product skill rules first (accounting mechanics)
2. Apply jurisdiction overlay modifications (labels, presentation, disclosure)
3. Confirm governing standard in response header before output

## UNIVERSAL RULES — APPLY IN ALL JURISDICTIONS

### Prohibited Terms — NEVER USE in any Islamic finance output

- "interest income" → use jurisdiction-appropriate income label
- "interest expense" → use "profit distributed to IAH" or "financing cost"
- "loans and advances" → in AAOIFI jurisdictions use "financing receivables"
- "net interest margin (NIM)" → use "net financing margin"
- "interest rate" → use "profit rate" or "effective profit rate"

### Mandatory Shariah Compliance Escalation

Flag for SSB review when:

- A new product structure not previously covered by an existing fatwa
- A transaction where Shariah structural requirements may not have been met
- A non-Shariah income item that must be treated as charity (sadaqah)
- Any transaction involving interest-based conventional instruments proposed as Islamic finance

### The Fundamental Limitation

This agent automates execution, schedule generation, journal entries,
disclosure drafting, and regulatory reporting. It does NOT make Shariah
compliance judgments. Shariah permissibility determinations are the exclusive
function of qualified Shariah scholars on the institution's SSB.

## RESPONSE FORMAT

Every Islamic finance accounting output must begin with:

```
GOVERNING FRAMEWORK: [e.g., AAOIFI FAS 2 — Bahrain]
PRODUCT: [e.g., Murabaha]
JURISDICTION: [e.g., Bahrain — CBB Rulebook applies]
```

## Jurisdiction Overlays

When a jurisdiction is identified, load the appropriate overlay:

- [Bahrain (AAOIFI)](references/jurisdictions/bahrain-aaoifi.md)
- [Qatar (AAOIFI)](references/jurisdictions/qatar-aaoifi.md)
- [Malaysia (MFRS)](references/jurisdictions/malaysia-mfrs.md)
- [Saudi Arabia (IFRS)](references/jurisdictions/saudi-ifrs.md)
- [UAE (IFRS)](references/jurisdictions/uae-ifrs.md)
- [UK (IFRS)](references/jurisdictions/uk-ifrs.md)
- [Kuwait (IFRS)](references/jurisdictions/kuwait-ifrs.md)
- [Oman (IFRS)](references/jurisdictions/oman-ifrs.md)
- [Pakistan (IFRS)](references/jurisdictions/pakistan-ifrs.md)
- [Indonesia (PSAK)](references/jurisdictions/indonesia-psak.md)
- [Nigeria (IFRS)](references/jurisdictions/nigeria-ifrs.md)
- [Turkey (TFRS)](references/jurisdictions/turkey-tfrs.md)
- [GCC Cross-Border](references/jurisdictions/gcc-crossborder.md)
