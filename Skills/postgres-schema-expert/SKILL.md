---
name: postgres-schema-expert
description: Instructions for managing the PostgreSQL schema, writing SQL queries, and maintaining data integrity for the insurance analytics project.
---

# PostgreSQL Schema Expert Skill

This skill covers the database layer of the insurance analytics project: the `insurance` schema, table definitions, indexes, SQL patterns, and data-integrity rules.

## Schema overview

All tables live in the `insurance` schema inside the `insurdb` database.

```
insurance
├── member      – one row per enrolled health-plan member
├── provider    – one row per healthcare provider
└── claim       – one row per insurance claim (child of member + provider)
```

The DDL lives in `src/sql/ddl_create_tables.sql` and is applied with:

```bash
# DATABASE_URL uses the SQLAlchemy format (postgresql+psycopg2://...).
# psql requires a driver-free URL — strip the +psycopg2 prefix:
PSQL_URL="${DATABASE_URL/+psycopg2/}"
psql "$PSQL_URL" -f src/sql/ddl_create_tables.sql
# or use the Makefile shortcut (handles the URL conversion for you):
make db-init
```

## Table definitions

### `insurance.member`

| Column | Type | Notes |
|---|---|---|
| `member_id` | `BIGSERIAL` PRIMARY KEY | Auto-incrementing surrogate key |
| `person_id` | `BIGINT` | External identifier |
| `dob` | `DATE` | Date of birth — used to derive age in Python |
| `gender` | `VARCHAR(10)` | `'male'` / `'female'` / `'U'` — Kaggle datasets map the source `sex` column to `gender`; `'U'` is the default when gender is absent |
| `region` | `VARCHAR(50)` | Geographic region (e.g. `'Northeast'`) |
| `effective_date` | `DATE` | Coverage start date |
| `termination_date` | `DATE` | Coverage end date (`NULL` = still active) |

### `insurance.provider`

| Column | Type | Notes |
|---|---|---|
| `provider_id` | `BIGSERIAL` PRIMARY KEY | Auto-incrementing surrogate key |
| `specialty` | `VARCHAR(80)` | Medical specialty (e.g. `'Cardiology'`) |
| `in_network` | `BOOLEAN` | `TRUE` = in-network, `FALSE` = out-of-network |
| `region` | `VARCHAR(50)` | Geographic region of the provider |

### `insurance.claim`

| Column | Type | Notes |
|---|---|---|
| `claim_id` | `BIGSERIAL` PRIMARY KEY | Auto-incrementing surrogate key |
| `member_id` | `BIGINT` FK → `member` | Required — every claim belongs to a member |
| `provider_id` | `BIGINT` FK → `provider` | Required — every claim belongs to a provider |
| `service_date` | `DATE` | Date the service was rendered |
| `diagnosis_code` | `VARCHAR(8)` | ICD-10 code (e.g. `'Z00.00'`) |
| `procedure_code` | `VARCHAR(8)` | CPT code (e.g. `'99213'`) |
| `billed_amount` | `NUMERIC(12,2)` | Amount the provider billed |
| `allowed_amount` | `NUMERIC(12,2)` | Maximum amount the plan will pay |
| `paid_amount` | `NUMERIC(12,2)` | Amount actually paid by the plan |
| `place_of_service` | `VARCHAR(20)` | E.g. `'Office'`, `'Hospital'` |

## Indexes

```sql
-- Speeds up joins from claim → member
CREATE INDEX IF NOT EXISTS idx_claim_member      ON insurance.claim(member_id);
-- Speeds up date-range queries on claims
CREATE INDEX IF NOT EXISTS idx_claim_service_date ON insurance.claim(service_date);
```

Add new indexes only when a slow query is identified. Over-indexing slows down INSERT/UPDATE.

## Common SQL query patterns

### Monthly paid totals by region

```sql
SELECT
    DATE_TRUNC('month', c.service_date) AS month,
    m.region,
    COUNT(*)                            AS claim_count,
    SUM(c.paid_amount)                  AS paid_total
FROM insurance.claim c
JOIN insurance.member m ON c.member_id = m.member_id
GROUP BY 1, 2
ORDER BY 1, 2;
```

### In-network vs out-of-network comparison

```sql
SELECT
    p.in_network,
    COUNT(*)           AS claims,
    AVG(c.paid_amount) AS avg_paid,
    SUM(c.paid_amount) AS total_paid
FROM insurance.claim c
JOIN insurance.provider p ON c.provider_id = p.provider_id
GROUP BY p.in_network;
```

### Claims for currently active members only

```sql
SELECT c.*
FROM insurance.claim c
JOIN insurance.member m ON c.member_id = m.member_id
WHERE m.termination_date IS NULL
   OR m.termination_date > CURRENT_DATE;
```

### Top 10 providers by paid amount

```sql
SELECT
    c.provider_id,
    p.specialty,
    SUM(c.paid_amount) AS paid_total
FROM insurance.claim c
JOIN insurance.provider p ON c.provider_id = p.provider_id
GROUP BY 1, 2
ORDER BY paid_total DESC
LIMIT 10;
```

## Resetting and re-initialising the database

```bash
# Drop and recreate the schema, then re-apply DDL
make db-reset

# Equivalent raw SQL (strip the +psycopg2 driver prefix for psql compatibility)
PSQL_URL="${DATABASE_URL/+psycopg2/}"
psql "$PSQL_URL" -c "DROP SCHEMA IF EXISTS insurance CASCADE;"
psql "$PSQL_URL" -c "CREATE SCHEMA insurance;"
psql "$PSQL_URL" -f src/sql/ddl_create_tables.sql
```

## Load behaviour and idempotency

`src/load.py` uses a **truncate-then-load** strategy so repeated runs are safe:

```sql
-- Runs inside a single transaction
TRUNCATE insurance.claim, insurance.provider, insurance.member CASCADE;
```

This means every `make kaggle-load` call replaces all data. Do not run it on a production database with live data unless you intend to replace everything.

## Data-integrity rules

1. **Foreign keys** – Every `claim` must reference an existing `member` and `provider`. PostgreSQL enforces this automatically.
2. **Numeric scale** – `NUMERIC(12,2)` stores up to 10 digits before the decimal and exactly 2 after. Never store amounts as `FLOAT` — floating-point rounding causes accounting errors.
3. **Date columns** – Always store dates as `DATE`, never as `VARCHAR`. This enables range comparisons and `DATE_TRUNC` without casting.
4. **Schema isolation** – All objects live in the `insurance` schema, not `public`. This keeps the database clean if other schemas are added later.

## Environment variable

The application connects using the `DATABASE_URL` environment variable:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/insurdb
```

The `psql` CLI accepts a slightly different format (no driver prefix):

```bash
psql "postgresql://postgres:postgres@localhost:5432/insurdb"
```
