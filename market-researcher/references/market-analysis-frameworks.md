# Market Analysis Frameworks

## Market Sizing

### TAM / SAM / SOM

```
TAM (Total Addressable Market)
│   Total revenue opportunity if 100% market share achieved
│   Method: Industry reports, government data, trade associations
│
├── SAM (Serviceable Addressable Market)
│   │   Portion of TAM targetable with current product/service
│   │   Method: TAM × geographic/demographic/product filters
│   │
│   └── SOM (Serviceable Obtainable Market)
│       Realistic capture within 1-3 years
│       Method: SAM × realistic penetration rate (typically 1-5% for new entrants)
```

**Top-Down Sizing:**
```
Total industry revenue (from reports)
× Relevant segment percentage
× Geographic filter
× Target demographic filter
= Market size estimate
```

**Bottom-Up Sizing:**
```
Number of potential customers (from census/industry data)
× Average revenue per customer (from comparable companies)
× Realistic penetration rate
= Market size estimate
```

**Always present both methods** and note if they converge or diverge. Divergence signals uncertainty.

### Market Growth Analysis

```markdown
## [Industry] Market Overview

### Market Size
- **Current size**: $X billion ([year], [source])
- **Projected size**: $X billion by [year] ([source])
- **CAGR**: X% ([period], [source])

### Growth Drivers
1. [Driver] — [quantified impact if available]
2. [Driver] — [quantified impact if available]
3. [Driver] — [quantified impact if available]

### Growth Inhibitors
1. [Barrier] — [quantified impact if available]
2. [Barrier] — [quantified impact if available]

### Key Segments
| Segment | Size | Growth | Share |
|---------|------|--------|-------|
| [Seg 1] | $Xbn | X% | X% |
| [Seg 2] | $Xbn | X% | X% |
| [Seg 3] | $Xbn | X% | X% |
```

## Competitive Landscape

### Industry Map Template

```markdown
## Competitive Landscape: [Industry]

### Market Leaders (>20% share)
| Company | Revenue | Share | Strength | Weakness |
|---------|---------|-------|----------|----------|
| [Name] | $X | X% | [key] | [key] |

### Challengers (5-20% share)
| Company | Revenue | Share | Differentiator |
|---------|---------|-------|---------------|
| [Name] | $X | X% | [what sets apart] |

### Emerging Players (<5% share)
| Company | Funding | Traction | Watch Because |
|---------|---------|----------|---------------|
| [Name] | $X | [metric] | [why relevant] |

### Competitive Dynamics
- **Consolidation trend**: [acquiring or fragmenting?]
- **Pricing pressure**: [race to bottom or premium shift?]
- **Innovation pace**: [who's leading and with what?]
- **Barriers to entry**: [high/medium/low — why?]
```

## Trend Analysis

### PESTEL Framework

Use for macro-environment scanning:

| Factor | Current State | Trend Direction | Impact on [Topic] |
|--------|--------------|----------------|--------------------|
| **Political** | [regulation, policy] | ↑↓→ | [how it affects] |
| **Economic** | [GDP, inflation, spending] | ↑↓→ | [how it affects] |
| **Social** | [demographics, behavior] | ↑↓→ | [how it affects] |
| **Technological** | [innovation, adoption] | ↑↓→ | [how it affects] |
| **Environmental** | [sustainability, climate] | ↑↓→ | [how it affects] |
| **Legal** | [compliance, IP, labor] | ↑↓→ | [how it affects] |

### Trend Maturity Assessment

```
Emerging (0-2 years visible)  → Early signals, limited data, high uncertainty
Growing (2-5 years visible)   → Clear trajectory, growing data, moderate confidence
Mature (5+ years visible)     → Well-documented, abundant data, high confidence
Declining                     → Peak passed, alternatives emerging
```

## Data Presentation Standards

### When Presenting Numbers

- Always include **source and date** for every statistic
- Show **ranges** when estimates vary: "$4.2B-$5.8B (varies by source)"
- Note **methodology differences** between sources if they produce different numbers
- Use **consistent units** within each analysis (don't mix millions and billions)
- Convert currencies to user's currency with exchange rate noted
- Mark estimates as estimates: "~$4.5B (estimated)" vs. "$4.5B (reported)"

### Confidence Indicators

Use confidence tags when synthesizing from multiple sources:

- **Strong consensus** — 3+ authoritative sources agree within 10%
- **Moderate consensus** — 2+ sources agree, some variance
- **Single source** — Only one source found; treat with caution
- **Conflicting data** — Sources disagree significantly; present range and explain why
- **Estimated** — Calculated from available data, not directly reported
