---
name: geneva-tax-advisor
version: 1.2.0
description: >
  Guide taxpayers through filing Geneva (Switzerland) tax returns with GeTax.
  Covers salary, professional expenses (forfaitaire vs effectifs), pillar 3a/3b,
  health insurance, medical expenses, securities (DA-1/RSI), foreign property,
  bank accounts, debts, crypto, and dual-income couples.
  Use when filing via GeTax, optimizing ICC/IFD deductions, declaring foreign
  property or income, handling DA-1 reclaims, or navigating Geneva cantonal tax rules.
metadata:
  openclaw:
    emoji: "🇨🇭"
---

# Geneva Tax Advisor

Your guide to filing Geneva tax returns with GeTax — built from real filing experience, not theory.

## How to Use This Skill

1. **Before each section:** Read the relevant reference file for field-by-field guidance
2. **Before advising on any rule:** Look up the official GeTax guide page — never guess
3. **Always verify from source docs:** Read salary certs, bank statements, and insurance attestations directly

## GeTax Section Flow

Work through sections in this order:

| Section | What to Do | Read First |
|---------|-----------|------------|
| **Page de garde** | Personal info. Commune = **residence**, not workplace | — |
| **Annexe A** | Salary per spouse. Check field 15 for hidden deductions | `references/salary-and-expenses.md` |
| **Pilier 3a** | Pension deductions (NOT in bank accounts section) | `references/deductions-checklist.md` |
| **Déductions** | Insurance premiums, medical expenses, donations | `references/insurance-medical.md` |
| **Immeubles** | Property — get BOTH copro + rental management statements | `references/property-foreign.md` or `references/property-geneva.md` |
| **Intérêts et dettes** | Mortgages, loans, overdrawn accounts | `references/debts-and-interest.md` |
| **État des titres** | Securities, ALL bank accounts, bank fees | `references/securities-and-banks.md` |
| **Récapitulation** | Review totals. Enter source tax for ALL spouses | — |

## The 3 Decisions That Matter Most

### 1. Forfaitaire vs Effectifs (Professional Expenses)

**⚠️ ICC meal deductions require a commute >2h/day by public transport.** IFD has no such restriction.

```
Commute > 2h by public transport?
├── YES → Compare effectifs vs forfaitaire for both ICC and IFD
└── NO  → ICC: forfaitaire wins (meals blocked)
          IFD: compare meals (3'200) + transport vs forfaitaire (min 2'000 / max 4'000)
```

You **can split**: forfaitaire for ICC + effectifs for IFD. GeTax allows it.

Read `references/salary-and-expenses.md` for the full comparison.

### 2. Forfaitaire vs Effectifs (Property Maintenance)

- **ICC:** NO forfait for rental properties — effective costs only
- **IFD:** 10% forfait (≤10yr) or 20% (>10yr) of loyers encaissés
- Effectifs often wins when copro charges + management fees + taxe foncière + works are included

### 3. DA-1 vs RSI (Foreign Dividends)

- **DA-1:** Foreign broker (IBKR, Fidelity, DEGIRO)
- **RSI:** Swiss broker (Swissquote, UBS)
- **Never both** for the same security

## Top Gotchas

These are the mistakes that actually cost people money. Full list in `references/gotchas.md`.

1. **Field 15 on salary certs** — Amat, APGM, Krankentaggeld hiding there → add to field 9
2. **ICC meals require >2h commute** — most people don't qualify; forfaitaire wins for ICC
3. **Medical expenses ICC threshold is only 0.5%** — almost always worth claiming (IFD is 5%, much harder)
4. **Foreign medical/dental is deductible** — no territoriality restriction
5. **Bank fees are deductible** — enter in F2 as positive values, auto-deducted
6. **Source tax for BOTH spouses** — check every salary cert field 12
7. **Exchange rates differ** — fortune/debt = 31.12 year-end; income/interest = annual average
8. **Copro ≠ rental statement** — always request both; copro often has thousands more in charges

## Planning Ahead

- **3a for non-LPP spouse:** Higher rate (20% net income, max 36'288)
- **3b / assurance-vie:** Geneva couple deduction 3'518 for ~CHF 100/year policy cost
- **LPP buyback:** Most powerful Swiss tax deduction — unlimited up to pension gap
- **From 2026:** Retroactive 3a contributions for missed years from 2025+

## Reference Files

| File | Read When |
|------|-----------|
| `references/salary-and-expenses.md` | User mentions salary, employer, professional expenses, or commute |
| `references/insurance-medical.md` | User mentions health insurance, premiums, medical bills, dental, or glasses |
| `references/property-foreign.md` | User mentions foreign property, rental income, or French apartment |
| `references/property-geneva.md` | User mentions Geneva property, valeur locative, or owner-occupied |
| `references/debts-and-interest.md` | User mentions mortgage, loan, debt, or interest |
| `references/securities-and-banks.md` | User mentions stocks, ETFs, dividends, bank accounts, or DA-1 |
| `references/special-cases.md` | User mentions crypto, vehicle, TOU, quasi-résident, or donations |
| `references/deductions-checklist.md` | User wants a full overview of available deductions and limits |
| `references/exchange-rates.md` | User has foreign currency amounts to convert |
| `references/gotchas.md` | User asks for tips, common mistakes, or optimization |

## Official Sources

- GeTax guide: `getax.ch/support/guide/declaration{YEAR}/`
- ictax (securities): `ictax.admin.ch/extern/en.html`
- Exchange rates: `fidinam.com/fr/blog/cours-des-devises-suisse-pour-{YEAR}`
- Tax rates: `ge.ch/taux-donnees-fiscales`
- TOU/rectification: `ge.ch/demande-rectification-taxation-ordinaire-ulterieure`
