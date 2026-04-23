# Scout Strategies

Domain-specific search strategies and quality criteria for each scout agent.

## General Search Principles

All scouts should:

1. **Search for today's news first** — use date-qualified queries with current date or "bugün" (today)
2. **Diversify sources** — don't rely on a single publication; cross-reference across Turkish and international outlets
3. **Prioritize primary reporting** — original reporting and official statements over aggregated summaries
4. **Look for the "second story"** — beyond the headline, what's the underlying trend or shift?
5. **Flag surprises** — anything unexpected or counterintuitive gets bonus points
6. **Turkish-language coverage** — use both Turkish and English queries for comprehensive coverage

## Regulatory Scout

### Primary Search Queries (Turkish & English)
- "SEDDK yeni karar", "SEDDK kararı", "Insurance Regulation Authority Turkey", "SEDDK circular"
- "Sigorta kanunu değişikliği", "insurance law change Turkey"
- "Sigortalama yönetmeliği", "underwriting regulation", "solvency margin Turkey"
- "DASK deprem sigortası", "earthquake insurance DASK", "DASK mechanismi"
- "Reinsurance geri transfer", "reinsurance cession", "sigorta şirketi lisans"
- "Hazinenin sigorta politikası", "Insurance Ministry announcement"

### Quality Criteria
- **High value**: SEDDK decision or ruling, new regulation passed/effective, significant enforcement action, solvency requirement change, DASK guidance, policy from Ministry of Finance
- **Medium value**: SEDDK consultation, proposed regulation, guideline update from industry association
- **Low value**: Opinion pieces without regulatory backing, rumor-stage policy proposals

### Look Beyond Headlines
- SEDDK monthly statistics releases — market share shifts, premium growth by line
- Quiet regulatory guidance updates that change how underwriting works
- Solvency reports and capital adequacy discussions
- DASK retention and reinsurance cession announcements
- New underwriting or claims procedures mandated by regulator
- Compliance timelines for new standards
- Market exit or license suspension decisions

### Output Format

```
## Regulatory Scout Report

### Top Stories (ranked by impact on Turkish market)

**1. [Headline]**
- Source: SEDDK / Ministry / Turkish publication
- Summary: [2-3 sentence summary]
- Insurance impact: [1-2 sentences on significance for underwriting/pricing/reserves]
- Scope: [Does this apply to all insurers, specific lines, specific segments?]

**2. [Headline]**
...

### Key Regulatory Data This Week
- [SEDDK data release, market statistics, compliance deadline]

### Emerging Compliance Issues
- [1-2 items worth monitoring but not yet headline-worthy]
```

---

## Market Scout

### Primary Search Queries (Turkish & English)
- "Sigorta pazarı", "Turkish insurance market", "prim büyümesi", "premium growth Turkey"
- "Sigorta şirketi kazancı", "insurance company earnings", "teknik kar", "technical profit"
- "Yatırım geliri sigorta", "investment returns insurance", "faiz oranları", "interest rates Turkey"
- "Sigorta prim dağılımı", "premium distribution by line", "motor sigorta prim", "health insurance premium"
- "Birleşme devralma sigorta", "M&A insurance Turkey", "şirket satışı", "company acquisition"
- "Reasürans maliyeti", "reinsurance cost", "reasürans premium"

### Quality Criteria
- **High value**: Market-moving premium growth data, company earnings/results, significant M&A, premium distribution shifts by major line, investment return trends, reinsurance pricing changes
- **Medium value**: Quarterly market statistics, notable funding rounds, investor presentations, analyst reports
- **Low value**: Speculative trading analysis, unconfirmed market rumors, minor product pricing adjustments

### Look Beyond Headlines
- Premium growth rates by line — what's growing, what's shrinking, why?
- Market share shifts — which companies are gaining/losing ground?
- Investment yield trends — how are insurance companies' asset portfolios performing?
- Combined ratio movements — are underwriting results stable or degrading?
- Claims inflation by line — are claim costs rising faster than premiums?
- Reinsurance price trends — what does international reinsurance pricing tell us?
- Distribution channel shifts — are motor and property moving online? Healthcare through partnerships?

### Output Format

```
## Market Scout Report

### Top Stories (ranked by market significance)

**1. [Headline]**
- Source: TSB / Company PR / Turkish business press
- Summary: [2-3 sentence summary]
- Market implications: [Which companies affected? What does this mean for pricing?]
- Trend signal: [What does this tell us about market direction?]

**2. [Headline]**
...

### Market Metrics This Week
- [Key data release: premium growth, earnings, market share, investment returns]

### Emerging Market Trends
- [1-2 things worth watching: distribution channel shifts, competitive moves, pricing pressures]
```

---

## Industry Scout

### Primary Search Queries (Turkish & English)
- "Sigorta şirketi strateji", "insurance company strategy Turkey", "ürün lansmanı", "product launch"
- "Dijital sigorta", "digital insurance Turkey", "insurtech", "online insurance"
- "Bancassurance Türkiye", "bank insurance", "aracı sigorta", "insurance broker"
- "İnsan kaynakları sigorta", "insurance recruitment", "şirkete katılım", "executive appointment"
- "Distribüsyon kanalı", "distribution channel insurance", "broker network"
- "Ürün yeniliği sigorta", "product innovation insurance", "risk management"

### Quality Criteria
- **High value**: Major product launch, significant distribution deal, company strategy announcement, competitive repositioning, market exit or major entry
- **Medium value**: Executive changes, technology investments, distribution network expansion, partnership announcements
- **Low value**: Minor product tweaks, routine hiring, marketing announcements without strategic implications

### Look Beyond Headlines
- Which companies are investing in digital infrastructure?
- Distribution channel partnerships — who's partnering with banks, e-commerce platforms, agents?
- Product innovation — are companies launching new coverage areas or line combinations?
- Market consolidation signals — are smaller players being absorbed or facing pressure?
- Technology partnerships — is AI being applied to claims, underwriting, distribution?
- International parent company moves affecting Turkish operations
- Executive reshuffles signaling strategic direction changes

### Output Format

```
## Industry Scout Report

### Top Stories (ranked by competitive impact)

**1. [Headline]**
- Source: Company announcement / Turkish business press
- Summary: [2-3 sentence summary]
- Competitive implications: [What does this mean for competitive positioning?]
- Market signal: [What does this reveal about where the industry is heading?]

**2. [Headline]**
...

### Distribution & Product Trends
- [Key moves in how insurance is sold and what's being built]

### Strategic Positioning Watch
- [1-2 companies or moves to monitor for broader implications]
```

---

## Cross-Domain Scout

### Primary Search Queries (Turkish & English)
- "Türkiye enflasyon", "Turkey inflation", "fiyat artışı", "price increases"
- "Merkez Bankası faiz", "TCMB interest rate", "central bank Turkey", "monetary policy"
- "Ücret artışı", "wage growth Turkey", "işçi maliyeti", "labor cost"
- "Deprem Türkiye", "earthquake Turkey", "doğal afet", "natural disaster CAT"
- "Ekonomik göstergeler", "economic indicators Turkey", "GSYH", "GDP growth"
- "Dış ticaret", "foreign trade", "ihracat ithalatça", "exports imports"
- "Jeopolitik risk", "geopolitical risk Turkey", "uluslararası ilişkiler", "international relations"
- "İklim değişikliği Türkiye", "climate change Turkey", "hava koşulları", "weather events"

### Quality Criteria
- **High value**: Macroeconomic data releases (inflation, interest rates, employment), significant natural disasters, geopolitical events affecting Turkey, climate-related weather extremes, labor market shifts
- **Medium value**: Economic forecasts from credible institutions, regional climate patterns, international business developments relevant to Turkish economy
- **Low value**: Speculative economic commentary, unconfirmed forecasts, minor geopolitical updates without Turkish relevance

### Look Beyond Headlines - Insurance Mechanisms
- **Inflation data → Claims costs** — Consumer price inflation drives bodily injury and health claims upward
- **Interest rate moves → Investment returns** — TCMB rate changes affect insurance company asset yields and ALM strategies
- **Wage growth → Workers' compensation costs** — Labor cost inflation affects workers' comp and employers' liability claims
- **Natural disasters → CAT exposure and DASK** — Earthquake, flood, storm events illuminate Turkey's exposure and activate DASK mechanics
- **Currency moves → Claims costs** — If TL weakens, imported materials and medicines become more expensive (affects claims severity)
- **Unemployment trends → Premium demand** — Economic downturns affect motor, health, and other lines' demand and pricing
- **Geopolitical tension → Credit risk** — Political instability affects insurer credit quality and reinsurance relationships

### Output Format

```
## Cross-Domain Scout Report

### Top Stories (ranked by insurance implications)

**1. [Headline]**
- Source: Turkish Central Bank / Statistical Office / International news
- Summary: [2-3 sentence summary]
- Insurance mechanism: [What is the concrete transmission to insurance business?]
- Affected lines: [Which insurance lines feel this pressure?]
- Timeline: [How quickly will this flow through to underwriting/pricing?]

**2. [Headline]**
...

### Macroeconomic Signals
- [Key data: inflation, interest rates, employment, geopolitical]

### Emerging Exposures
- [1-2 cross-domain risks worth monitoring: climate trends, economic shifts, geopolitical developments]
```

---

## Turkish-Language Search Tips

All scouts should use both Turkish and English queries for maximum coverage:

- Turkish sources often publish 6-12 hours ahead of English-language summaries
- SEDDK, TSB, DASK, and Ministry of Finance publish primarily in Turkish
- Company announcements may appear first in Turkish press before English translation
- Use Turkish terms correctly:
  - Sigorta = insurance
  - Sigortalama = underwriting
  - Prim = premium
  - Hasar = claims
  - Deprem = earthquake
  - Reasürans = reinsurance
  - Müşteri = customer/policyholder
  - Tekniktekâr = technical profit
  - Kombinasyon oranı = combined ratio
  - Zarar oranı = loss ratio

**Recommended sources:**
- seddk.gov.tr (SEDDK official announcements)
- tsb.org.tr (Insurance Association of Turkey)
- Demiryolcu, Dış Ticaret, Türkiye newspapers for business news
- Haberler.com, Radikal, and other Turkish business press
