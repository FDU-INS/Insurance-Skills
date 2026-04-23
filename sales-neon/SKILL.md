---
name: sales-neon
description: >
  Neon PostgreSQL vault/archive configuration, schema, and operational patterns for the Sales Navigator hub
  (HUB-SALES-NAV-20260130). Use this skill whenever querying, migrating, debugging, or making
  data-layer decisions in the sales-navigator repo. Trigger on: Neon, PostgreSQL, Postgres,
  database, schema, sales_state, sales_factfinder, sales_insurance, sales_systems, sales_quotes,
  column_registry, migration, connection pooling, NEON_DATABASE_URL,
  pipeline tracking, prospect data, meeting data, CF D1, CF KV, Cloudflare Workers,
  or any reference to the sales data layer.
  Also trigger when discussing CRM intake, 4-meeting process state, quote approval, or
  PROMOTE_TO_CLIENT events. If the question touches relational data in this repo, this skill
  applies even if the user does not mention Neon by name.
master_skill: IMO-Creator/skills/neon/SKILL.md
hub_id: HUB-SALES-NAV-20260130
---

# Sales Navigator -- Neon + CF D1 Skill

## Architecture (BAR-100 Shift)

The data layer follows a two-tier model:

| Tier | Technology | Role |
|------|-----------|------|
| **Working** | CF D1 / CF KV | Active queries, runtime state, application traffic |
| **Vault** | Neon Serverless PostgreSQL | Archival storage, migrations, canonical schema authority |

CF Workers serve as the compute layer. The Figma UI design layer connects to CF Workers,
which read/write CF D1 for working data and sync to Neon vault for long-term persistence.

## What This Repo Uses

| Component | Value |
|-----------|-------|
| Hub ID | HUB-SALES-NAV-20260130 |
| Hub Name | sales-navigator |
| Working Database | CF D1 (Cloudflare Workers runtime) |
| Vault Database | Neon Serverless PostgreSQL |
| Working KV | CF KV (session state, caches) |
| Schema | `sales` (canonical), `sn_*` prefix (deprecated) |
| Compute Layer | CF Workers |
| Design Layer | Figma UI |
| Secrets Provider | Doppler (`doppler run -- npm run dev`) |
| Column Registry | `column_registry.yml` (canonical schema spine) |
| Canonical Migration | `sales/migrations/001_sales_schema.sql` (targets Neon vault, per ADR-005) |
| Deprecated Migration | `src/data/migrations/001_create_sales_navigator_schema.sql` (sn_* prefix, DO NOT execute) |

## Connection Configuration

All secrets are injected via Doppler. No `.env` files with real values are permitted.

| Variable | Purpose | Injected By |
|----------|---------|-------------|
| `NEON_DATABASE_URL` | Neon vault connection string (migrations, archive sync) | Doppler |
| `CF_D1_DATABASE_ID` | CF D1 working database identifier | Doppler |
| `CF_ACCOUNT_ID` | Cloudflare account identifier | Doppler |
| `CF_API_TOKEN` | Cloudflare API token for Workers/D1/KV | Doppler |
| `COMPOSIO_API_KEY` | External API calls via Composio MCP | Doppler |

**Neon vault connection pattern (migrations and archive only):**
```
# Pooled (archive reads, sync operations)
postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require

# Direct (migrations, admin, pg_dump)
postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

**Critical:** Neon is vault/archive ONLY. All application-level queries go through CF D1.
Use the Neon pooled endpoint for archive sync operations. Use the direct endpoint only for
migrations and `pg_dump`. See master skill `IMO-Creator/skills/neon/SKILL.md` for full
connection pooling rules and PgBouncer transaction-mode constraints.

## Schema / Data Model

The canonical schema is defined in `column_registry.yml`. All generated TypeScript types and
Zod schemas are projections of this file and must never be hand-edited.

### Spine Table

| Table | Purpose |
|-------|---------|
| `sales.sales_state` | Phase router -- authoritative identity, gates sub-hub access |

Columns: `sales_id` (UUID PK, universal join key), `legal_name` (TEXT), `domicile_state` (TEXT), `current_phase` (TEXT: factfinder/insurance/systems/quotes), `status` (TEXT), `source` (TEXT), `version` (INT), `created_at`, `updated_at`

### Sub-Hub Tables (4 meetings)

| Sub-Hub | Canonical Table | Error Table | Key Columns |
|---------|----------------|-------------|-------------|
| Meeting 1: FactFinder | `sales.sales_factfinder` | `sales.sales_factfinder_errors` | employer_name, employee_count, renewal_month, prior_broker |
| Meeting 2: Insurance | `sales.sales_insurance` | `sales.sales_insurance_errors` | funding_model, strategy_selected |
| Meeting 3: Systems | `sales.sales_systems` | `sales.sales_systems_errors` | payroll_system, admin_model, compliance_owner |
| Meeting 4: Quotes | `sales.sales_quotes` | `sales.sales_quotes_errors` | quote_version, total_cost (USD_CENTS), approved_flag |

All sub-hub tables join to spine via `sales_id` (TEXT). Each sub-hub has exactly 1 CANONICAL
and 1 ERROR table per OWN-10a/OWN-10b.

For the full column-level schema reference, see `references/schema.md`.

## Operational Patterns

### Phase Progression
The `sales.sales_state.current_phase` column gates which sub-hub is active:
```
factfinder -> insurance -> systems -> quotes -> [PROMOTE_TO_CLIENT]
```

### Query Pattern (Working Layer)
Application queries go through CF Workers reading/writing CF D1. For vault operations
(reporting, archival queries), CF Workers connect to Neon via the pooled endpoint.

### Schema Changes
1. Update `column_registry.yml`
2. Run `./scripts/codegen-generate.sh`
3. Generated output lands in `src/data/hub/generated/` and `src/data/spokes/generated/`
4. Pre-commit hook enforces sync between registry and generated output
5. Apply migration to Neon vault, then sync D1 schema

### Error Tables
All error tables are append-only. Columns: `id` (BIGSERIAL in Neon vault; INTEGER AUTOINCREMENT in D1),
`sales_id` (nullable FK), `error_code`, `payload` (JSONB in Neon; TEXT/JSON in D1), `process_id`, `created_at`.

## Known Issues

- **Deprecated sn_* prefix**: The original migration (`001_create_sales_navigator_schema.sql`)
  used `sn_prospect`, `sn_sales_process`, `sn_meeting`, `sn_meeting_outcome` tables. These
  are superseded by the `sales.*` schema per ADR-005. Do not execute the deprecated migration.
- **D1 type mapping**: CF D1 uses SQLite under the hood. BIGSERIAL maps to INTEGER AUTOINCREMENT,
  JSONB maps to TEXT (with JSON validation in application layer), TIMESTAMPTZ maps to TEXT (ISO-8601).
  The `column_registry.yml` declares Neon vault types; D1 equivalents are derived at migration time.

## Cost Profile

| Resource | Expected Usage | Plan Consideration |
|----------|---------------|-------------------|
| CF D1 | Low -- sales process is human-paced, not high-throughput | Free tier likely sufficient during development |
| CF KV | Minimal -- session state, caches | Free tier covers this |
| CF Workers | Low compute -- API routing and D1 queries | Free tier (100k req/day) covers dev |
| Neon Vault | < 0.5GB for prospect/meeting archive data | Free tier covers this |
| Neon Branches | Dev/staging branches for safe migration testing | Launch plan if > default branch limit |

See master skill `IMO-Creator/skills/neon/references/pricing.md` for full Neon pricing breakdown.
