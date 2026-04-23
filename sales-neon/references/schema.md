# Sales Navigator -- Schema Reference

Source of truth: `column_registry.yml` (repo root)
Hub ID: HUB-SALES-NAV-20260130
Schema: `sales`
Universal join key: `sales_id` (TEXT)

---

## Spine Table: `sales.sales_state`

Phase router -- authoritative source of sales process identity, gates sub-hub access.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| sales_id | TEXT | NO | Universal join key -- minted at intake, propagated to all sub-hub tables |
| current_phase | TEXT | NO | Active sub-hub gate -- one of: factfinder, insurance, systems, quotes |
| created_at | TIMESTAMPTZ | NO | Process inception timestamp |
| updated_at | TIMESTAMPTZ | NO | Last phase transition timestamp |

---

## Sub-Hub 1: FactFinder (Meeting 1)

### `sales.sales_factfinder` (CANONICAL)

Employer data captured during Fact Finder meeting -- company name, headcount, renewal timing.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| sales_id | TEXT | NO | FK to spine table |
| employer_name | TEXT | YES | Company name captured from prospect |
| employee_count | INTEGER | YES | Total number of employees at the company |
| renewal_month | INTEGER | YES | Benefits renewal month (1-12) |
| prior_broker | TEXT | YES | Name of previous insurance broker |
| created_at | TIMESTAMPTZ | YES | Record creation timestamp |
| updated_at | TIMESTAMPTZ | YES | Last update timestamp |

### `sales.sales_factfinder_errors` (ERROR)

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | BIGSERIAL | NO | Auto-increment PK |
| sales_id | TEXT | YES | FK to spine (nullable -- error may occur before entity exists) |
| error_code | TEXT | YES | Machine-readable error identifier |
| payload | JSONB | YES | Full error context as structured JSON |
| process_id | TEXT | YES | Originating process or agent identifier |
| created_at | TIMESTAMPTZ | YES | Append timestamp |

---

## Sub-Hub 2: Insurance (Meeting 2)

### `sales.sales_insurance` (CANONICAL)

Insurance education outcomes -- funding model and strategy selection.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| sales_id | TEXT | NO | FK to spine table |
| funding_model | TEXT | YES | Insurance funding model selected by prospect |
| strategy_selected | TEXT | YES | Insurance strategy chosen during education session |
| created_at | TIMESTAMPTZ | YES | Record creation timestamp |
| updated_at | TIMESTAMPTZ | YES | Last update timestamp |

### `sales.sales_insurance_errors` (ERROR)

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | BIGSERIAL | NO | Auto-increment PK |
| sales_id | TEXT | YES | FK to spine |
| error_code | TEXT | YES | Machine-readable error identifier |
| payload | JSONB | YES | Full error context as structured JSON |
| process_id | TEXT | YES | Originating process or agent identifier |
| created_at | TIMESTAMPTZ | YES | Append timestamp |

---

## Sub-Hub 3: Systems (Meeting 3)

### `sales.sales_systems` (CANONICAL)

Systems and operations assessment -- payroll, admin model, compliance.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| sales_id | TEXT | NO | FK to spine table |
| payroll_system | TEXT | YES | Payroll provider used by the prospect company |
| admin_model | TEXT | YES | Benefits administration model in use |
| compliance_owner | TEXT | YES | Party responsible for compliance oversight |
| created_at | TIMESTAMPTZ | YES | Record creation timestamp |
| updated_at | TIMESTAMPTZ | YES | Last update timestamp |

### `sales.sales_systems_errors` (ERROR)

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | BIGSERIAL | NO | Auto-increment PK |
| sales_id | TEXT | YES | FK to spine |
| error_code | TEXT | YES | Machine-readable error identifier |
| payload | JSONB | YES | Full error context as structured JSON |
| process_id | TEXT | YES | Originating process or agent identifier |
| created_at | TIMESTAMPTZ | YES | Append timestamp |

---

## Sub-Hub 4: Quotes (Meeting 4)

### `sales.sales_quotes` (CANONICAL)

Financial quotes and approval status -- triggers PROMOTE_TO_CLIENT on approval.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| sales_id | TEXT | NO | FK to spine table |
| quote_version | INTEGER | YES | Quote iteration number for this sales process |
| total_cost | NUMERIC | YES | Total quoted cost (USD_CENTS format) |
| approved_flag | BOOLEAN | YES | Approval status -- when true, fires PROMOTE_TO_CLIENT event |
| created_at | TIMESTAMPTZ | YES | Record creation timestamp |
| updated_at | TIMESTAMPTZ | YES | Last update timestamp |

### `sales.sales_quotes_errors` (ERROR)

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | BIGSERIAL | NO | Auto-increment PK |
| sales_id | TEXT | YES | FK to spine |
| error_code | TEXT | YES | Machine-readable error identifier |
| payload | JSONB | YES | Full error context as structured JSON |
| process_id | TEXT | YES | Originating process or agent identifier |
| created_at | TIMESTAMPTZ | YES | Append timestamp |

---

## Deprecated Tables (DO NOT USE)

The original migration used `sn_*` prefix tables. These are superseded per ADR-005:

| Deprecated Table | Replacement |
|-----------------|-------------|
| sn_prospect | sales.sales_state + sales.sales_factfinder |
| sn_sales_process | sales.sales_state |
| sn_meeting | Per-sub-hub CANONICAL tables |
| sn_meeting_outcome | Per-sub-hub CANONICAL tables |

---

## Join Pattern

All sub-hub tables join to spine on `sales_id`:

```sql
SELECT s.sales_id, s.current_phase,
       f.employer_name, f.employee_count,
       i.funding_model,
       sy.payroll_system,
       q.total_cost, q.approved_flag
FROM sales.sales_state s
LEFT JOIN sales.sales_factfinder f ON f.sales_id = s.sales_id
LEFT JOIN sales.sales_insurance i ON i.sales_id = s.sales_id
LEFT JOIN sales.sales_systems sy ON sy.sales_id = s.sales_id
LEFT JOIN sales.sales_quotes q ON q.sales_id = s.sales_id;
```
