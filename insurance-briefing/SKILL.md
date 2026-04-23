---
name: insurance-briefing
description: >
  This skill should be used when the user asks for an "insurance briefing",
  "sigorta brifing", "insurance digest", "sigorta haberleri",
  "insurance news summary", or wants to understand the editorial philosophy
  behind the insurance briefing system. Also triggers when the user mentions
  "insurance briefing plugin" or wants a curated daily overview of the Turkish
  insurance sector.
version: 0.1.0
---

# Insurance Briefing System

A multi-agent pipeline designed for Turkish insurance professionals that produces a curated daily briefing blending regulatory intelligence with market insights and cross-domain analysis.

## Editorial Philosophy

The briefing serves two audiences living in the same person:

1. **The Practitioner** — an underwriter, risk manager, or actuary who needs to know what changed in regulation, what market signals matter, and how non-insurance developments affect their underwriting and pricing decisions. Senior underwriter directness: no filler, sharp analysis, efficient reading.

2. **The Strategist** — a member of leadership or someone in market-facing roles who needs to understand *why* things happen, how global patterns echo in Turkey's market, and how seemingly unrelated developments create competitive opportunity or threat. Executive-level insight: backstories, hidden mechanisms, the "I never thought about it that way" moments.

Every briefing must serve both. Regulatory updates and market moves serve the practitioner. The deep dives and cross-domain radar serve the strategist. The best pieces serve both simultaneously.

## Pipeline Architecture

The briefing is produced by a 3-stage multi-agent pipeline:

### Stage 1: Domain Scouts (parallel)

Four specialized agents search their domains simultaneously:

- **regulatory-scout** — SEDDK decisions, law changes, compliance requirements, solvency standards, reinsurance rules
- **market-scout** — Premium trends, underwriting results, premium distribution by line, investment performance, M&A
- **industry-scout** — Competitive moves, company strategy shifts, distribution channel evolution, product innovation
- **cross-domain-scout** — Macroeconomic data, interest rates, inflation, geopolitical events, CAT risks with Turkish relevance

Each scout returns a structured list of 5-8 candidate stories ranked by importance and Turkish relevance.

### Stage 2: Cross-Pollinator (editorial intelligence)

A single agent receives all scout outputs and performs editorial curation:

- Selects the best 6-10 stories across all domains
- Identifies 1-2 cross-domain connections
- Picks one story for deep-dive treatment
- Flags 1-2 radar pieces (non-obvious insurance mechanisms)
- Outputs a structured editorial plan

### Stage 3: Briefing Composer

A single agent takes the editorial plan and writes the final markdown briefing with consistent voice and structure.

## Briefing Sections

The insurance briefing is organized into five main sections:

- **Gündem** (Agenda) — 4-6 most consequential stories of the day
- **Derinlemesine** (Deep Dive) — 2-3 medium-depth features with analysis
- **Radar** — 1-2 pieces about non-obvious insurance mechanisms in non-insurance news
- **Gelişmeler** (Developments) — Continuity: updates on stories from previous briefings
- **Küresel Reasürans** (Global Reinsurance) — 2-3 brief items on international developments with Turkish relevance

See `references/briefing-structure.md` for the full section-by-section specification.

## Scout Strategies

See `references/scout-strategies.md` for domain-specific search strategies, quality criteria, and Turkish-language search tips.

## Editorial Standards

See `references/editorial-philosophy.md` for the full editorial guidelines, the two tests (Practitioner Test and Implications Test), voice guidelines per section, and quality benchmarks.

## Story Continuity & Tracking

See `references/tracker-schema.md` for the story tracker schema and how the briefing maintains cross-session memory of developing insurance stories.

## Domain Context

See `references/insurance-domain-context.md` for institutional knowledge about the Turkish insurance market: regulatory bodies, top insurers, market structure, and key terminology.
