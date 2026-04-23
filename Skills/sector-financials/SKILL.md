---
name: sector-financials
description: Deep-dive analysis of the Financials sector (XLF, KRE, KBE). Covers large-cap banks, regional banks, insurance, capital markets, and fintech. Interest rate sensitive — integrates closely with bonds output. Run as part of the US Equities phase in the daily orchestrator.
---

# Financials Sector Sub-Agent

## Inputs
- `config/watchlist.md` (XLF and financial ETFs)
- `config/preferences.md`
- Macro regime + bonds output from current session

> **Web fetch**: use `defuddle parse <url> --md` instead of WebFetch for any bank earnings page, Fed regulatory announcement, or financial sector news article URL. Not for API endpoints, `.json`, or `.md` files.

---

## Research Steps

### 1. Sector ETF Overview
- XLF, KRE, KBE levels and relative strength vs SPY

### 2. NIM / Rates
- Fed funds + curve shape implications for bank NIM

### 3. Credit Quality
- CRE, consumer, corporate credit stress signals

### 4. Capital Markets
- M&A/IPO pipeline and trading environment

### 5. Insurance
- Float benefit from rates + catastrophe risk

### 6. Regulation
- Basel rules, FDIC/OCC actions

### 7. Earnings/Catalysts
- Major bank earnings and guidance

### 8. Valuation
- P/B and sector valuation context

---

## Output Format

```
### 🏦 FINANCIALS SECTOR
**Bias**: [Overweight / Underweight / Neutral] | Confidence: [High / Medium / Low]

**ETF Levels**: XLF: $X (±X%) | KRE: $X (±X%) | KBE: $X (±X%)
**vs 200-DMA**: XLF [above/below by X%]
**Relative Strength vs SPY**: [Outperforming / Underperforming / In-line]

**Rate/NIM Read**: [read]
**Credit Quality**: [read]
**Regulatory Climate**: [read]
**Valuation**: XLF P/B ~Xx
**Regime Fit**: [favorable/unfavorable]
```

