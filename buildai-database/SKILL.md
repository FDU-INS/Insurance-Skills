---
name: buildai-database
description: Query the BuildAI PostgreSQL database (read-only). Returns results as JSON for construction project data — projects, RFIs, submittals, budgets, change orders, daily logs, punch lists, insurance, vendors, pay applications.
metadata: {"clawdbot":{"emoji":"🗄️","requires":{"anyBins":["psql"]}}}
---

# BuildAI Database Query

Execute read-only SQL queries against the BuildAI PostgreSQL database (`buildai_demo`).

## Usage

```bash
bash command:"cd /home/apoorvgarg/buildai/packages/engine/skills/buildai-database && bash query.sh 'SELECT * FROM projects LIMIT 5'"
```

## Parameters

The script takes a single argument: a SQL query string.

**Safety:**
- Only SELECT and WITH (CTE) queries are allowed
- INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, REVOKE, EXEC are rejected
- Results are returned as JSON
- Queries are limited to 30 seconds

## Database Schema

### Tables

| Table | Description |
|-------|-------------|
| `projects` | Construction projects with status, contract sums, dates, stakeholders |
| `rfis` | Requests for Information — open/closed/void, with priority and assignee |
| `submittals` | Material/shop drawing submittals with approval tracking |
| `budget_line_items` | Cost codes with original/revised/committed/actual budget breakdowns |
| `change_orders` | Change order packages with amounts and reasons |
| `daily_logs` | Daily site logs — weather, workforce, delays, safety incidents |
| `punch_list_items` | Punch list items with status and priority |
| `insurance_certs` | Vendor insurance certificates with expiration tracking |
| `vendors` | Subcontractors/vendors with contract amounts and payments |
| `pay_applications` | Payment applications (AIA G702/G703 style) |

### Pre-Built Views (prefer these for common queries)

| View | Best For |
|------|----------|
| `v_project_dashboard` | Project overview — open RFIs, pending submittals, expiring certs |
| `v_overdue_rfis` | Overdue RFIs with days overdue |
| `v_expiring_insurance` | Insurance certs expiring within 90 days |
| `v_project_budget_summary` | Budget totals with variance analysis |

### Key Columns

**projects:** id, name, address, city, state, status (active/completed/on_hold), contract_sum, start_date, projected_completion, project_type

**rfis:** id, project_id, number, subject, status (open/closed/void), priority (normal/urgent/critical), assigned_to, due_date, days_open

**budget_line_items:** id, project_id, cost_code, description, original_budget, revised_budget, committed_costs, actual_costs, projected_final, variance, variance_percent

## Examples

```sql
-- Active projects overview
SELECT * FROM v_project_dashboard WHERE status = 'active';

-- Overdue RFIs
SELECT * FROM v_overdue_rfis ORDER BY days_overdue DESC;

-- Budget overruns
SELECT * FROM v_project_budget_summary WHERE total_variance < 0;

-- Expiring insurance in next 30 days
SELECT * FROM v_expiring_insurance WHERE days_until_expiration <= 30;

-- Workforce trends for a project
SELECT log_date, workforce_count, weather FROM daily_logs
WHERE project_id = 1 ORDER BY log_date DESC LIMIT 14;
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `/var/run/postgresql` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `buildai_demo` | Database name |
| `DB_USER` | `$USER` | Database user |
| `DB_PASSWORD` | (none) | Database password (optional for local peer auth) |
