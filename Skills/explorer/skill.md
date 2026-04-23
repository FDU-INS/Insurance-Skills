---
name: explorer
description: "Explore 122 Ethereum use case ideas from the Use Case Lab database. Use when the user asks about Ethereum use cases, wants to brainstorm product ideas, needs to research what's being built in a specific domain, or wants to find real-world examples of Ethereum applications. Covers 16 domains: AI, business operations, civil society, commerce, environment, finance, food & agriculture, government, health, identity, insurance, logistics & trade, media, real estate, science, and utilities. Each idea includes a problem statement, solution sketch, why Ethereum is needed, real project examples, and research resources."
---

# Use Case Lab Explorer

Search, browse, and research 122 curated Ethereum use case ideas across 16 domains.

## Setup

On first use, fetch the ideas database:

```bash
mkdir -p {{SKILL_PATH}}/references && curl -sL https://usecaselab.org/ideas.json -o {{SKILL_PATH}}/references/ideas.json
```

If `{{SKILL_PATH}}/references/ideas.json` already exists, skip this step.

## Quick search

```bash
# Search by keyword
jq --arg q "payments" '[.[] | select((.title + " " + .problem + " " + .solution) | ascii_downcase | contains($q | ascii_downcase))] | .[] | {id, title, domains, problem: (.problem[:150] + "...")}' {{SKILL_PATH}}/references/ideas.json

# Filter by domain
jq --arg d "finance" '[.[] | select(.domains[] == $d)] | .[] | {id, title, domains}' {{SKILL_PATH}}/references/ideas.json

# Combine domain + keyword
jq --arg d "ai" --arg q "agent" '[.[] | select(.domains[] == $d) | select((.title + " " + .problem) | ascii_downcase | contains($q | ascii_downcase))] | .[] | {id, title, domains, problem: (.problem[:150] + "...")}' {{SKILL_PATH}}/references/ideas.json

# List all domains with counts
jq -r '.[].domains[]' {{SKILL_PATH}}/references/ideas.json | sort | uniq -c | sort -rn
```

## Deep dive

```bash
jq '.[] | select(.id == "IDEA_ID")' {{SKILL_PATH}}/references/ideas.json
```

Each idea has: **problem**, **solution**, **whyEthereum** (Verifiability/Composability/Enforcement), **examples** (name, url, description), **resources**, **domains**.

## Domains

| Domain | Focus |
|--------|-------|
| ai | Autonomous agents, verifiable inference, compute markets |
| business-operations | Payroll, invoicing, cap tables, agreements, bookkeeping |
| civil-society | Whistleblowing, cash transfers, impact certificates, community ownership |
| commerce | Merchant payments, marketplaces, storefronts, cooperative commerce |
| environment | Carbon verification, grid automation, EV charging, regeneration |
| finance | Crowdfunding, lending, equity tokenization, trade finance |
| food-and-agriculture | Provenance, traceability, farmer finance, harvest pre-financing |
| government | Digital ID, elections, public policy, permitting, compliance |
| health | Patient records, clinical trials, pharmaceutical traceability |
| identity | Age verification, credentials, verifiable reputation, SSI |
| insurance | Parametric policies, risk pools, claims adjudication |
| logistics-and-trade | Bills of lading, customs, delivery payments, inventory |
| media | Creator monetization, streaming, publishing, ticketing |
| real-estate-and-housing | Land titles, mortgage rails, fractional ownership |
| science | Knowledge graphs, clinical trials, open science, research funding |
| utilities | Decentralized compute, storage, VPN, connectivity |

## Brainstorming workflow

1. Search by keyword or domain to find relevant ideas
2. Read full entries for the best matches
3. Identify patterns — recurring problems, most-leveraged Ethereum capabilities
4. Cross-reference examples across ideas to find active projects
5. Surface resources for deeper research

## Connecting ideas to action

- Highlight **examples** — teams already building
- Reference **whyEthereum** for the specific technical advantage
- Point to **resources** for deeper reading
- Suggest the Use Case Lab Toolkit at https://usecaselab.org/toolkit for starter code (Nexth), Ethereum knowledge (EthSkills), and community support
