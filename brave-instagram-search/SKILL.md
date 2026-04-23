---
name: brave-instagram-search
description: "Fast Instagram lead generation using Brave Search API. Scrapes 100+ insurance agent leads from Instagram via Google search results. Use when user wants quick lead volume via Brave search method, needs 100+ leads fast, or says 'brave instagram', 'brave search leads', 'get 100 leads', or wants high-volume lead generation without browser automation."
---

# Brave Instagram Search

Fast, high-volume Instagram lead generation using Brave Search API. Gets 100+ leads in under a minute by searching Google-indexed Instagram profiles.

## When to Use

- User says "brave instagram", "brave search", or "use brave"
- Need 100+ leads quickly
- Want volume over rich contact data
- Previous agent-browser method is blocked/returning 0 leads
- User explicitly requests this skill

## Quick Start

```bash
cd skills/brave-instagram-search/scripts
npx tsx brave-search-leads.ts 100
```

### Output
- Saves to SQLite database (avoids duplicates)
- Appends to master CSV file (`leads/instagram-leads-master.csv`)
- Reports lead count with contact info stats

## How It Works

1. **Brave Search API** queries Google-indexed Instagram profiles
2. **Search terms rotate** through insurance niches (carriers, states, specialties)
3. **Duplicate detection** via database hash constraint
4. **CSV + Drive upload** for easy access

### Search Term Categories
- **Core roles:** insurance agent, broker, advisor, specialist
- **Product niches:** life, final expense, medicare, iul, annuities
- **Carriers:** major insurers + imo/fmo partners
- **States:** geographic targeting (50 states rotate)
- **Titles:** agency manager, upline, wholesaler, producer

> **Tip:** When leads dry up, update `SEARCH_TERMS` in the script with fresh carriers, states, or niche keywords.

## Comparison

| Method | Speed | Volume | Contact Data | Best For |
|--------|-------|--------|--------------|----------|
| **Brave Search** | 30s | 100+ leads | Basic (username, bio, followers) | Volume, quick batches |
| Agent Browser | 10-15min | 0-50 leads | Rich (email, phone, location) | Deep contact info |

## Usage

### Default: 100 Leads
```bash
npx tsx brave-search-leads.ts
```

### Custom Count
```bash
npx tsx brave-search-leads.ts 200
```

### Skip CSV (Database only)
```bash
npx tsx brave-search-leads.ts 100 --no-csv
```

## Data Extracted

| Field | Example |
|-------|---------|
| username | @garcia_agency |
| full_name | The Garcia Agency |
| bio | American Family Insurance... |
| followers | 4,375 |
| following | 493 |
| posts | 196 |
| niche | auto_home / life_insurance |
| source_url | https://instagram.com/... |

## Notes

- **No phone/email extraction** — use agent-browser skill for that
- **Fast iteration** — run multiple times for 500+ leads
- **Duplicate-free** — database prevents re-scraping same profiles
- **Master CSV** — all leads appended to single file at `leads/instagram-leads-master.csv`

## Files

```
skills/brave-instagram-search/
├── SKILL.md                      # This file
└── scripts/
    └── brave-search-leads.ts     # Main scraper script
```

Last updated: 2026-02-02 (search terms refreshed)
