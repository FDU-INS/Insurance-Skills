---
name: market-researcher
description: "God-level internet research and data synthesis for any topic. Use when the user wants to research, compare, analyze, or find the best options for anything: business ideas, products (phones, laptops, gadgets), services (credit cards, banks, insurance), travel (hotels, flights, destinations), market trends, industry data, competitor analysis, pricing comparisons, consumer reviews, emerging opportunities, or any general-purpose research task. Triggers on: 'research', 'find the best', 'compare', 'what's the best', 'top 10', 'under X price', 'market data', 'industry trends', 'alternatives to', 'reviews of', or any request requiring internet research and data gathering."
---

# Market Researcher

Transform any research question into structured, actionable intelligence with verified data, source attribution, and clear recommendations.

## Core Research Process

Every research task follows this workflow:

```
User Question
    │
    ▼
1. SCOPE → Define what exactly needs answering
    │
    ▼
2. SEARCH → Gather data from multiple sources
    │
    ▼
3. VERIFY → Cross-reference and validate findings
    │
    ▼
4. SYNTHESIZE → Organize into structured insights
    │
    ▼
5. DELIVER → Present with sources and recommendations
```

## Step 1: Scope the Research

Before searching, clarify the research boundaries:

**Identify the research type:**

| Type | Example | Approach |
|------|---------|----------|
| **Product comparison** | "Best laptop under $1000" | Feature matrix + price-value scoring |
| **Service evaluation** | "Best credit cards for travel" | Benefits comparison + cost analysis |
| **Market analysis** | "AI industry trends 2026" | Data aggregation + trend mapping |
| **Opportunity research** | "Business ideas in health tech" | Market gap analysis + viability scoring |
| **Location/travel** | "Best hotels in Tokyo" | Rating aggregation + value scoring |
| **Competitor analysis** | "Alternatives to Notion" | Feature parity + differentiation mapping |
| **General inquiry** | "How does X work?" | Multi-source synthesis + expert consensus |

**Define constraints explicitly:**
- Budget range (if applicable)
- Geography/region
- Time sensitivity (current data vs. historical)
- User's experience level (beginner vs. expert)
- Priority factors (price vs. quality vs. speed vs. features)

**If constraints are unclear, ask.** One focused question beats five assumptions.

## Step 2: Search Strategy

### Source Priority Hierarchy

Prioritize sources in this order:

1. **Primary data** — Official websites, government databases, SEC filings, patent databases, published research papers
2. **Authoritative aggregators** — Industry reports (Gartner, Statista, IBISWorld), financial databases (Bloomberg, Yahoo Finance), review aggregators (Wirecutter, Consumer Reports)
3. **Expert content** — Domain-specific publications, verified expert analyses, peer-reviewed journals, established trade publications
4. **Community intelligence** — Reddit threads (sorted by top/best), Stack Exchange, Quora (verified authors), specialized forums
5. **News and media** — Recent articles from established outlets, press releases, conference coverage
6. **Social signals** — Trending topics, user sentiment, social media discussions (lowest reliability, use for directional signals only)

### Search Techniques

**Breadth-first for discovery:**
- Search the broad topic to understand the landscape
- Identify key players, categories, and dimensions
- Note recurring recommendations and patterns across multiple sources

**Depth-first for validation:**
- Drill into top candidates with specific queries
- Cross-reference claims across independent sources
- Look for disconfirming evidence (negative reviews, limitations, complaints)

**Temporal awareness:**
- Always check publication dates — outdated data kills research quality
- For products: specs and pricing change rapidly, verify current availability
- For markets: use the most recent data available, note the data vintage
- Flag when information may be stale

### Research Depth Calibration

| Request Complexity | Sources to Check | Time Investment |
|-------------------|-----------------|-----------------|
| Quick comparison (2-3 items) | 3-5 sources | Light |
| Thorough comparison (5-10 items) | 8-12 sources | Medium |
| Market analysis | 10-20 sources | Deep |
| Industry deep-dive | 20+ sources | Comprehensive |

## Step 3: Verify and Validate

### The Three-Source Rule

**Never present a claim backed by only one source.** Minimum verification:

- **Facts and statistics** → Confirm with 3+ independent sources
- **Product claims** → Cross-reference specs from manufacturer AND third-party reviewers
- **Market data** → Triangulate from multiple research firms or data providers
- **Pricing** → Verify from official source + at least one independent price tracker
- **Expert opinions** → Present as opinions, not facts; note consensus vs. dissent

### Red Flags to Watch For

- Affiliate-heavy "review" sites (prioritize unbiased sources)
- Outdated information presented as current
- Single-source claims repeated across multiple sites (echo chamber)
- Sponsored content disguised as editorial
- Survivorship bias (only successful examples shown)
- Small sample sizes extrapolated to broad conclusions

### Data Quality Tags

Tag every data point with confidence level:

- **HIGH** — Official sources, verified data, multiple confirmations
- **MEDIUM** — Reputable single source, expert opinion, recent but unconfirmed
- **LOW** — Anecdotal, single user report, potentially outdated
- **ESTIMATED** — Calculated or inferred from available data

## Step 4: Synthesize Findings

### Structure by Research Type

**For product/service comparisons** — See [references/comparison-templates.md](references/comparison-templates.md)

**For market analysis** — See [references/market-analysis-frameworks.md](references/market-analysis-frameworks.md)

**For opportunity/idea research** — See [references/opportunity-assessment.md](references/opportunity-assessment.md)

### Universal Synthesis Rules

1. **Lead with the answer** — Start with the recommendation or key finding, then supporting evidence
2. **Quantify everything possible** — Numbers > adjectives ("37% market growth" not "strong growth")
3. **Compare apples to apples** — Normalize units, currencies, time periods
4. **Show trade-offs explicitly** — Nothing is perfect; show what you gain and lose with each option
5. **Separate facts from opinions** — Clearly mark data vs. interpretation
6. **Attribute sources** — Every claim needs a source; every number needs a citation
7. **Include contrarian views** — Note where experts disagree and why

## Step 5: Deliver Results

### Output Format Decision Tree

```
What did the user ask for?
│
├─ "Best X for Y" → Ranked recommendation list with comparison table
├─ "Compare A vs B" → Head-to-head comparison matrix
├─ "Market data on X" → Data report with charts/tables
├─ "Ideas for X" → Scored opportunity list with viability assessment
├─ "How does X work?" → Structured explainer with sources
└─ General research → Executive summary + detailed findings
```

### Every Research Output Must Include

1. **Executive summary** (2-3 sentences answering the core question)
2. **Key findings** (structured data — tables, ranked lists, or matrices)
3. **Methodology note** (what was searched, how many sources, data vintage)
4. **Source list** (URLs, publication names, dates)
5. **Caveats** (limitations, data gaps, areas needing further research)
6. **Actionable next steps** (what the user should do with this information)

### Quality Standards

- **No filler** — Every sentence must add information value
- **No hedging without reason** — Be direct; qualify only when genuinely uncertain
- **No generic advice** — Tailor every finding to the user's specific constraints
- **Current data** — Flag anything older than 6 months; reject anything older than 2 years for fast-moving markets
- **Honest gaps** — If data doesn't exist or is unreliable, say so explicitly

## Research Modes

### Quick Research (respond within minutes)
- User needs a fast answer with reasonable confidence
- Check 3-5 top sources, provide ranked answer with brief rationale
- Mark as "quick research" — suggest deeper dive if needed

### Deep Research (comprehensive analysis)
- User needs thorough, decision-grade intelligence
- Check 10-20+ sources, build comparison matrices, verify all claims
- Provide full structured report with methodology notes

### Ongoing Research (iterative refinement)
- User refines criteria after seeing initial results
- Build on previous findings, narrow scope, add new dimensions
- Track what's been researched vs. what's new

## Special Research Domains

### Product Research (Electronics, Gadgets, Tools)
- Always include: price, key specs, user rating (aggregated), pros/cons
- Check for: recent model releases that may supersede recommendations
- Sources: manufacturer sites, Wirecutter, RTINGS, specialized review sites
- Watch for: regional availability, warranty differences, ecosystem lock-in

### Financial Products (Credit Cards, Banks, Insurance)
- Always include: APR/fees, rewards structure, eligibility, fine print
- Check for: promotional rates vs. ongoing rates, hidden fees
- Sources: official issuer sites, NerdWallet, Bankrate, regulatory filings
- Watch for: affiliate bias in comparison sites, regional availability

### Travel Research (Hotels, Flights, Destinations)
- Always include: price range, rating, location convenience, seasonal factors
- Check for: recent reviews (last 6 months), renovation status, hidden fees
- Sources: booking platforms, TripAdvisor, travel blogs, Google Maps reviews
- Watch for: fake reviews, seasonal pricing swings, currency fluctuations

### Market & Industry Research
- Always include: market size, growth rate, key players, trends
- Check for: methodology behind market size estimates, sample sizes
- Sources: Statista, IBISWorld, industry associations, SEC filings, research papers
- Watch for: conflicting estimates between research firms, outdated projections

### Business Ideas & Opportunities
- Always include: market gap, competition level, barrier to entry, revenue potential
- Check for: existing solutions, failure cases, regulatory requirements
- Sources: Crunchbase, Product Hunt, patent databases, startup databases
- Watch for: survivorship bias, overhyped markets, regulatory risks

## Anti-Patterns (Never Do These)

- ❌ Present AI-generated data as real research (always use actual sources)
- ❌ Give a single recommendation without alternatives
- ❌ Ignore the user's specific constraints (budget, location, experience)
- ❌ Copy-paste from one source without cross-referencing
- ❌ Present outdated data without flagging it
- ❌ Skip source attribution
- ❌ Use vague language ("many experts say", "studies show") without specifics
- ❌ Over-research simple questions (match depth to complexity)
- ❌ Present sponsored/affiliate content as unbiased research
