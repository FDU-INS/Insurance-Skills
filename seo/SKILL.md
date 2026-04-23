---
name: seo
description: SEO analysis and optimization for TC Insurance. Sub-commands: audit, onpage, analytics, content, local, ai, full, report.
---

# /seo — SEO Analysis & Optimization

Herramienta de análisis SEO completo para TC Insurance. Funciona despachando agentes especializados según el sub-comando.

## Sub-comandos

Parse the first argument after `/seo` to determine which analysis to run:

| Command | Description |
|---------|-------------|
| `/seo audit` | Technical SEO: crawlability, structured data, Core Web Vitals, site structure |
| `/seo onpage` | On-Page SEO: title tags, meta descriptions, headings, internal linking |
| `/seo analytics` | Analytics setup: GTM, GA4, Meta Pixel, event tracking, consent |
| `/seo content` | Content SEO: topical authority, clusters, keywords, gaps, cannibalization |
| `/seo local` | Local SEO: NAP consistency, LocalBusiness schema, GBP, citations |
| `/seo ai` | AI SEO: GEO readiness, LLM visibility, E-E-A-T, citability |
| `/seo full` | Run ALL analyses in parallel, generate comprehensive report |
| `/seo report` | View latest report(s) or compare with previous |
| `/seo` (no args) | Show this help |

## Execution Flow

### 1. Parse Sub-command

Extract the sub-command from the skill args. If no args provided, show the help table above and stop.

### 2. Crawl Data Management (for audit, onpage, full)

Before dispatching agents that analyze the live site:

```
Check if docs/seo/data/crawl-{YYYY-MM-DD}.json exists (today's date)
```

If it does NOT exist:
1. Check if a dev server is running on localhost:3000 (`lsof -i :3000`)
2. If running: `node scripts/seo-crawl.mjs --localhost`
3. If NOT running: Ask the user whether to start dev server or use production URL
4. Wait for crawl to complete

If it exists: skip crawl, use existing data.

Store the crawl data path for agent prompts: `CRAWL_PATH=docs/seo/data/crawl-{date}.json`

### 3. Dispatch Agents

Use the Agent tool to dispatch the appropriate agent(s). Each agent is defined in `.claude/agents/`.

#### For `/seo audit`:
```
Dispatch seo-technical agent with prompt:
"Run in AUDIT mode. Crawl data is at {CRAWL_PATH}.
Perform a full Technical SEO audit following your audit mode instructions.
Save your report to docs/seo/reports/{YYYY-MM-DD}-audit.md"
```

#### For `/seo onpage`:
```
Dispatch seo-technical agent with prompt:
"Run in ON-PAGE mode. Crawl data is at {CRAWL_PATH}.
Perform a full On-Page SEO audit following your on-page mode instructions.
Save your report to docs/seo/reports/{YYYY-MM-DD}-onpage.md"
```

#### For `/seo analytics`:
```
Dispatch seo-technical agent with prompt:
"Run in ANALYTICS mode. No crawl data needed.
Audit the analytics setup following your analytics mode instructions.
Save your report to docs/seo/reports/{YYYY-MM-DD}-analytics.md"
```

#### For `/seo content`:
```
Dispatch seo-content agent with prompt:
"Perform a full Content SEO analysis following your instructions.
Save your report to docs/seo/reports/{YYYY-MM-DD}-content.md"
```

#### For `/seo local`:
```
Dispatch seo-local agent with prompt:
"Perform a full Local SEO audit following your instructions.
Save your report to docs/seo/reports/{YYYY-MM-DD}-local.md"
```

#### For `/seo ai`:
```
Dispatch seo-ai agent with prompt:
"Perform a full AI/GEO SEO analysis following your instructions.
Save your report to docs/seo/reports/{YYYY-MM-DD}-ai.md"
```

#### For `/seo full`:
1. Run crawl if needed (step 2)
2. Dispatch ALL agents IN PARALLEL using multiple Agent tool calls in a single message:
   - seo-technical (audit mode) with crawl path
   - seo-technical (onpage mode) with crawl path — **Note:** use a separate agent instance
   - seo-technical (analytics mode)
   - seo-content
   - seo-local
   - seo-ai
3. Once all agents complete, consolidate results into `docs/seo/reports/{YYYY-MM-DD}-full.md`:
   - Combined summary with overall score
   - Top P0 issues across all domains
   - Top P1 issues
   - Quick wins from each domain
   - Links to individual reports

#### For `/seo report`:
1. List all files in `docs/seo/reports/` sorted by date
2. Read the most recent report(s)
3. If a previous report of the same type exists, compute a delta:
   - Issues fixed since last report
   - New issues found
   - Score change (improved/declined)
4. Present summary to user

### 4. Report Saving

Every agent saves its own report to `docs/seo/reports/YYYY-MM-DD-{type}.md`.

For `/seo full`, additionally create a consolidated report that links to all individual reports.

### 5. Present Results

After the agent completes:
1. Read the generated report
2. Present a concise summary to the user:
   - Score
   - Number of P0/P1/P2 issues
   - Top 3 quick wins
   - Link to full report file

## Agent Reference

| Agent | File | Modes |
|-------|------|-------|
| seo-technical | `.claude/agents/seo-technical.md` | audit, onpage, analytics |
| seo-content | `.claude/agents/seo-content.md` | single mode |
| seo-local | `.claude/agents/seo-local.md` | single mode |
| seo-ai | `.claude/agents/seo-ai.md` | single mode |

## Key Files

- **Crawler:** `scripts/seo-crawl.mjs`
- **Crawl data:** `docs/seo/data/crawl-*.json`
- **Reports:** `docs/seo/reports/*.md`
- **Site config:** `src/config/site.ts`
- **Project guide:** `CLAUDE.md`

## Notes

- Agents generate reports with suggested fixes but do NOT auto-apply changes
- The user decides which fixes to implement after reviewing the report
- Reports are saved for historical tracking — running the same audit again allows comparison
- The crawler uses Playwright (already a project dependency)
- WebSearch is used by content, local, and AI agents for keyword research and competitive analysis
