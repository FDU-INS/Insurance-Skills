# Platform Search Guide — DTC Life Insurance

Search query templates and strategy for each source. Replace `[lookback_date]` with the date matching your cadence (7, 30, or 90 days ago) in YYYY-MM-DD format.

**Tool Resolution Order**: For each platform, use MCP tool (if connected) → bundled script (if available) → web search fallback. See the Tool Discovery section in SKILL.md.

---

## Industry Publications — Primary Research Source

> **MCP tools**: any web search tool  
> **Web fallback**: direct site fetches and targeted web queries

### Why Industry Publications Matter
Industry trade press is the record of authority for life insurance. Insurance Journal, Coverager, AM Best, and LIMRA set the agenda for what professionals consider significant. A story here rarely gets there without meaningful research or a genuine primary event.

### Publication Targets

| Publication | Focus | URL Pattern |
|-------------|-------|-------------|
| **Insurance Journal** | Broad industry news, DTC, regulation | `insurancejournal.com` |
| **Coverager** | Insurtech-focused, DTC, innovation | `coverager.com` |
| **AM Best** | Financial ratings, carrier strength, market data | `ambest.com` |
| **LIMRA** | Research data, distribution, consumer insight | `limra.com` |
| **ACLI** | Life insurer advocacy, data, regulatory positions | `acli.com` |
| **National Underwriter Life & Health** | Products, underwriting, distribution | `nationalunderwriter.com` |
| **ThinkAdvisor** | Distribution, financial advisors, product news | `thinkadvisor.com` |
| **InsuranceNewsNet** | Carrier, product, regulatory news | `insurancenewsnet.com` |
| **Life Annuity Specialist** | Life and annuity product news | `lifeannuityspecialist.com` |

### Search Queries

**New DTC product launches**:
```
site:insurancejournal.com OR site:coverager.com "life insurance" ("launch" OR "new product" OR "now available" OR "expanded") after:[lookback_date]
```

**Carrier and underwriting changes**:
```
site:insurancejournal.com OR site:thinkadvisor.com "life insurance" ("underwriting" OR "accelerated" OR "no-exam" OR "instant issue") after:[lookback_date]
```

**Insurtech / DTC platform news**:
```
site:coverager.com OR site:insurancejournal.com ("insurtech" OR "direct-to-consumer" OR "DTC" OR "online life insurance") after:[lookback_date]
```

**Regulatory and compliance**:
```
site:insurancejournal.com OR site:naic.org ("life insurance" OR "NAIC") ("regulation" OR "bulletin" OR "model law" OR "legislation") after:[lookback_date]
```

**Market data and LIMRA reports**:
```
site:limra.com OR site:acli.com ("life insurance" OR "term life" OR "direct") ("sales" OR "data" OR "statistics" OR "research") after:[lookback_date]
```

**AM Best ratings changes**:
```
site:ambest.com "life insurance" ("rating" OR "upgraded" OR "downgraded" OR "affirmed") after:[lookback_date]
```

### What to Extract
- Headline and publication date
- The substantive event (product launch, regulatory action, data release, rating change)
- Direct quotes from executives or regulators — these carry authority signal
- Any data points (dollar figures, growth percentages, sales volumes)
- Whether this is a primary source or secondary coverage of another primary event

---

## Reddit

> **MCP tools**: `reddit`, any tool with "reddit" + "search"  
> **Script**: `scripts/search_reddit.py "term life insurance" --days 30 --subreddits LifeInsurance,personalfinance,financialindependence`  
> **Web fallback**: `site:reddit.com` queries

### Why Reddit Matters for DTC Insurance Research
Reddit is the consumer and practitioner truth layer. On r/LifeInsurance, real applicants share real experiences — policy denials they don't understand, prices they found confusing, carriers they loved or hated. This is qualitative consumer research at scale, available in real time. Top comments with high upvotes are often contrarian, accurate, or revealing of systemic issues.

On r/personalfinance and r/financialindependence, life insurance comes up in financial planning context — how much to buy, whether to trust agents, whole vs. term debates. These threads reveal consumer mental models and decision friction.

### Key Subreddits

| Subreddit | Focus |
|-----------|-------|
| **r/LifeInsurance** | Primary target — real buyer and agent experiences, product questions, carrier complaints |
| **r/personalfinance** | Term life in financial planning context, "how much do I need", whole vs. term debates |
| **r/financialindependence** | FIRE community life insurance — high engagement, financially sophisticated |
| **r/Insurance** | Broader insurance discussion — occasionally surfaces life insurance trends |
| **r/Frugal** | Budget-conscious consumers — price sensitivity signals |
| **r/smallbusiness** | Business owner life insurance, key person, buy-sell — emerging DTC opportunity |

### Search Queries

**Consumer experiences with DTC carriers**:
```
site:reddit.com (r/LifeInsurance OR r/personalfinance) ("Policygenius" OR "Ladder" OR "Ethos" OR "Haven Life" OR "Bestow" OR "Fabric" OR "Sproutt") after:[lookback_date]
```

**Underwriting frustrations and friction**:
```
site:reddit.com r/LifeInsurance ("denied" OR "declined" OR "postponed" OR "rated") after:[lookback_date]
```

**Consumer curiosity and education moments**:
```
site:reddit.com (r/personalfinance OR r/LifeInsurance) ("term life" OR "whole life" OR "life insurance") ("should I" OR "is it worth" OR "best company") after:[lookback_date]
```

**Emerging product or carrier discussions**:
```
site:reddit.com r/LifeInsurance (new OR launched OR "just got" OR "anyone tried") after:[lookback_date]
```

### What to Extract
- Thread title, subreddit, upvote count, comment count, post date
- **Top comment text and upvote count** — this is where the real consumer insight lives
- Specific carriers, products, or platforms mentioned (positive and negative)
- Friction points: application difficulty, pricing confusion, agent vs. direct debates
- Sentiment: enthusiasm, frustration, skepticism, surprise
- Patterns: multiple threads expressing the same experience = systemic signal

---

## Regulatory Sources

> **Primary method**: Web fetch of official regulatory sites  
> **No MCP tool or script needed** — these are authoritative, public sources

### Why Regulatory Sources Matter
Proposed rules today become compliance requirements in 18–36 months. State insurance departments, NAIC committees, and federal agencies telegraph changes well in advance. Surfacing these items early gives distribution and product teams time to respond.

### Key Regulatory Sources

| Source | What to Find | URL |
|--------|-------------|-----|
| **NAIC** | Model laws under development, committee meetings, bulletins | `naic.org/committees` |
| **CA Dept of Insurance** | Rate filings, bulletins, CA-specific actions (large market) | `insurance.ca.gov/0250-insurers/0300-insurers/` |
| **NY DFS** | NY-specific bulletins, circular letters (NY has significant influence) | `dfs.ny.gov/industry_guidance` |
| **TX TDI** | TX-specific bulletins, rate filings, market actions | `tdi.texas.gov/bulletins/` |
| **FL OIR** | FL-specific bulletins, market conduct actions | `floir.com` |
| **ACLI** | Legislative tracker, regulatory positions, advocacy updates | `acli.com/advocacy` |
| **Congress.gov** | Federal life insurance legislation, ERISA changes | `congress.gov` |
| **IRS Newsroom** | Tax treatment guidance (life insurance, MEC rules, COLI) | `irs.gov/newsroom` |

### Search Queries

**NAIC model law developments**:
```
site:naic.org "life insurance" OR "model law" OR "model regulation" after:[lookback_date]
```

**State regulatory bulletins (major markets)**:
```
site:insurance.ca.gov OR site:dfs.ny.gov OR site:tdi.texas.gov "life insurance" ("bulletin" OR "circular" OR "notice") after:[lookback_date]
```

**Federal legislation**:
```
site:congress.gov "life insurance" after:[lookback_date]
```

**Consumer protection actions**:
```
"life insurance" ("fine" OR "penalty" OR "cease and desist" OR "market conduct") ("department of insurance" OR "commissioner") after:[lookback_date]
```

### What to Extract
- Regulatory action type (model law, bulletin, fine, pending legislation)
- Who it affects (carriers, distributors, consumers, specific product types)
- Current status (proposed → comment period → adopted → effective date)
- Timeline to effect (when will this impact operations?)
- States affected (NAIC model laws must be adopted by individual states — note adoption status)

---

## X / Twitter

> **MCP tools**: `twitter`, `x-search`, `socialdata`, any tool with "tweet" + "search"  
> **Script**: none (API requires paid access)  
> **Web fallback**: `site:x.com` or `site:twitter.com` queries

### Why X Matters
X carries executive announcements, company launches, and candid industry reactions. Insurtech founders and carrier executives often announce product changes on X before formal press releases. Industry analysts post market commentary that surfaces before trade coverage.

### Key Accounts to Watch
Load `references/key_voices.md` for the full list. Priority targets: insurtech founders, carrier CMOs/CEOs of DTC-focused carriers, NAIC leadership, influential insurance journalists and analysts.

### Search Queries

**Carrier and product announcements**:
```
site:x.com OR site:twitter.com "life insurance" ("launch" OR "new" OR "now available" OR "excited to announce") after:[lookback_date]
```

**Industry reactions and commentary**:
```
site:x.com "life insurance" OR "insurtech" OR "DTC insurance" after:[lookback_date]
```

**Consumer/viral moments**:
```
site:x.com "life insurance" (min_faves:500 OR "viral") after:[lookback_date]
```

---

## LinkedIn

> **MCP tools**: any linkedin tool  
> **Web fallback**: `site:linkedin.com` queries

### Why LinkedIn Matters
LinkedIn surfaces insider industry moves that don't make trade press: executive moves signaling strategic direction, product team posts announcing beta launches, distribution leader commentary on market conditions. The "professional" framing produces more candid analysis than press releases.

### Search Queries

**Executive and product announcements**:
```
site:linkedin.com "life insurance" ("excited to announce" OR "launching" OR "new product" OR "new partnership") after:[lookback_date]
```

**Industry commentary and analysis**:
```
site:linkedin.com "DTC" OR "direct-to-consumer" "life insurance" after:[lookback_date]
```

**Carrier hires signaling strategic direction**:
```
site:linkedin.com "life insurance" ("head of digital" OR "chief distribution" OR "VP of growth" OR "director of direct") after:[lookback_date]
```

### What to Extract
- Executive name, company, role
- Content of the announcement or commentary
- Engagement (likes, comments, reshares) — signals how resonant this is within the industry
- Whether this is a primary announcement or reaction to external news

---

## Hacker News

> **MCP tools**: `hackernews`, `hn`, any tool with "hn" + "search"  
> **Script**: `scripts/search_hackernews.py "life insurance" --days 30 --limit 15`  
> **Web fallback**: `site:news.ycombinator.com` queries

### Why HN Matters
HN is where insurtech products get their first technical scrutiny. When a DTC life insurance platform launches an API, introduces ML-based underwriting, or raises a round, it often surfaces on HN. The comment threads contain unusually informed technical and product criticism. "Show HN" posts from life insurance startups are especially high signal — founders sharing something they built.

### Search Queries

```
site:news.ycombinator.com "life insurance" OR "insurtech" OR "instant life insurance" OR "no-exam life" after:[lookback_date]
```

```
hn.algolia.com life insurance DTC embedded insurance embedded fintech
```

### What to Extract
- Post title, score (HN points), comment count
- Notable comments and their upvote-equivalent signals
- Whether this is a "Show HN" (building something) vs. news link
- Technical insights in comment threads (underwriting algorithm criticism, data concerns, API design reactions)

---

## YouTube

> **MCP tools**: any youtube tool  
> **Web fallback**: `site:youtube.com` queries

### Why YouTube Matters
YouTube personal finance creators have significant influence over how consumers perceive and select life insurance. Channels like Policygenius's own content, independent agents explaining products, and general "best life insurance" comparison videos shape consumer expectations and conversion barriers. High-view videos indicate mainstream consumer awareness moments.

### Key Channels to Watch

| Creator/Channel | Type | Focus |
|-----------------|------|-------|
| Policygenius | DTC brand | Product education, comparison |
| Andrei Jikh | Personal finance | Investment/insurance for millennials |
| Graham Stephan | Personal finance | High-reach recommendations |
| Mark Tilbury | Personal finance | YA/Gen-Z financial literacy |
| Local insurance agents | Practitioner | Real underwriting and product explanation |

### Search Queries

```
site:youtube.com "life insurance" ("best" OR "review" OR "avoid" OR "you need") after:[lookback_date]
```

```
site:youtube.com "term life insurance" OR "no exam life insurance" OR "online life insurance" after:[lookback_date]
```

### What to Extract
- Video title, channel, view count, publish date
- Core thesis of the video (positive on DTC? warns against? comparing specific carriers?)
- Comment sentiment (are viewers sharing their own purchase experiences?)
- Whether specific DTC carriers are named and in what context

---

## TikTok

> **MCP tools**: any tiktok tool  
> **Web fallback**: `site:tiktok.com` queries

### Why TikTok Matters
TikTok's #FinTok and #PersonalFinance communities are how younger consumers encounter (and form opinions about) life insurance. Viral videos explaining term vs. whole life, or calling out agent practices, shape purchase decisions for Gen Z and younger millennials. High-view TikToks are leading indicators of mainstream consumer awareness moments.

### Search Queries

```
site:tiktok.com "life insurance" after:[lookback_date]
```

```
site:tiktok.com "term life" OR "whole life" OR "final expense" OR "life insurance" (min views 50000) after:[lookback_date]
```

### What to Extract
- Creator handle, video view count, topic
- Whether content is pro-DTC, pro-agent, or skeptical of insurance generally
- Consumer misconceptions being spread at scale (these are distribution challenges)
- Specific carriers or platforms mentioned

---

## Management Consulting Firms — Research Reports

> **Primary method**: Web search targeting firm research portals and publication indexes  
> **Cadence note**: Check quarterly briefs and annual outlooks; skip for weekly briefs unless a major report just dropped

### Why Consulting Research Matters (and Its Limits)
Consulting firm insurance reports serve as **trend validators and quantifiers**, not signal originators. When McKinsey publishes that DTC life insurance grew 18% YoY, that number becomes the benchmark everyone cites — worth including. But the trend was already visible in LIMRA data and Reddit discussion months earlier.

**Search pattern**: Most firms gate their research behind email registration. Prioritize finding executive summaries, press release versions, and trade press coverage of the reports over the full gated PDFs.

### Priority Firms for DTC Life Insurance

| Firm | Best Insurance Research | Typical Cadence |
|------|------------------------|-----------------|
| **Oliver Wyman** | Actuarial and underwriting innovation; protection gap; reinsurance | Quarterly + topical |
| **McKinsey** | Annual insurance outlook; digital distribution; consumer behavior | Annual + quarterly |
| **Deloitte** | Insurance industry outlook; regulatory; insurtech investment | Annual + topical |
| **Bain** | NPS benchmarks; customer experience in insurance | Annual |
| **Accenture** | Embedded insurance; AI in underwriting; digital distribution | Topical |
| **BCG** | Insurance distribution strategy | Annual + topical |
| **EY / PwC / KPMG** | Regulatory, tax, M&A context | Annual + topical |

### Search Queries

**Annual outlook reports (run at quarterly cadence or when a new report drops)**:
```
site:mckinsey.com OR site:deloitte.com OR site:oliverwyman.com "life insurance" ("outlook" OR "trends" OR "digital" OR "direct") after:[lookback_date]
```

**DTC and digital distribution focus**:
```
site:accenture.com OR site:bcg.com OR site:oliverwyman.com "life insurance" ("direct-to-consumer" OR "digital distribution" OR "embedded" OR "insurtech") after:[lookback_date]
```

**Consumer behavior and experience data**:
```
site:bain.com OR site:mckinsey.com OR site:pwc.com "life insurance" ("customer" OR "consumer" OR "experience" OR "NPS" OR "loyalty") after:[lookback_date]
```

**Regulatory and compliance outlook**:
```
site:ey.com OR site:deloitte.com OR site:kpmg.com "life insurance" ("regulation" OR "compliance" OR "tax" OR "regulatory outlook") after:[lookback_date]
```

**Trade press coverage of consulting reports** (often more accessible than the gated original):
```
site:insurancejournal.com OR site:coverager.com ("McKinsey" OR "Deloitte" OR "Oliver Wyman" OR "Accenture" OR "Bain" OR "BCG") "life insurance" after:[lookback_date]
```

### What to Extract
- Specific quantified findings (percentages, dollar figures, market share data) — these are the citation-worthy outputs
- The trend being described and its direction
- Publication date and the data vintage (when was the underlying data collected?)
- Whether the finding is primary research or meta-analysis of existing data
- Trade press coverage that makes the key stat accessible without gating

### Signal Weight Reminder
Tag consulting research findings as `[Consulting]` in your notes during research. When drafting:
- Use consulting data to **add quantification** to trends already surfaced by primary sources
- Route to 📊 Market & Industry Data or 🌱 Emerging Trends categories
- Note the data vintage when citing: "per McKinsey (2025 data)" not just "per McKinsey"
- Never use a consulting report as the sole source for a finding in Cross-Platform Highlights

---

## Carrier Websites — Direct Monitoring

For the leading DTC carriers, check their newsroom/blog directly as part of each research cycle.

### Target Carrier Newsrooms

| Carrier | DTC Focus | Newsroom URL Pattern |
|---------|-----------|---------------------|
| Haven Life (MassMutual) | Online term | `havenlife.com/blog` |
| Ladder | Online term, adjustable coverage | `ladderlife.com/blog` |
| Ethos | Online term, final expense | `ethoslife.com/blog` |
| Bestow | Online term | `bestow.com/blog` |
| Fabric by Gerber | Young family focus | `meetfabric.com/blog` |
| Policygenius | Comparison/broker | `policygenius.com/life-insurance/` |
| YOURide / Dayforward | Income-based DTC | carrier blog |
| Legal & General America | Online term (Banner) | `lgamerica.com/newsroom` |
| Protective Life | Online term (iPiP) | `protective.com/newsroom` |

### What to Look For
- New product features or coverage changes
- Underwriting guideline updates (accelerated underwriting changes are competitive signal)
- Pricing changes or promotional campaigns
- API/distribution partnership announcements
- Executive changes signaling strategic direction
