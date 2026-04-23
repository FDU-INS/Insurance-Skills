---
name: bear-query
description: Query the Bear EHR database using the semantic layer. Use when asked about clients, billing, appointments, insurance, clinical data, procedures, scheduling, programs, staff, vitals, diagnoses, revenue, claims, or any data question about the Bear application.
allowed-tools: Read, Grep, Glob
---

# Bear EHR Database Query Skill

You have access to the Bear EHR MariaDB database via MCP tools (`mcp__bear-db__execute_query`, `mcp__bear-db__get_table_info`, `mcp__bear-db__get_schema`).

## Before Writing Any Query

1. **Read the semantic layer** docs in `/home/andres/code/claude/semantic/` to understand the schema
2. **Start with** `00_query_guide.md` for query patterns, naming conventions, and caveats
3. **Read the relevant domain file** (01-15) for the specific tables involved

## Domain Files Quick Reference

| # | File | Use When Asking About |
|---|------|-----------------------|
| 00 | `00_query_guide.md` | NL-to-SQL patterns, status derivation, caveats |
| 01 | `01_people_demographics.md` | Clients, demographics, addresses, phones |
| 02 | `02_programs_enrollment.md` | Programs, enrollment, locations |
| 03 | `03_insurance_coverage.md` | Insurance policies, payors, plans, authorizations |
| 04 | `04_appointments_scheduling.md` | Scheduling, calendar, appointment types |
| 05 | `05_encounters_forms.md` | Clinical documentation, encounter forms |
| 06 | `06_billing_revenue.md` | Charges, claims, payments, revenue cycle |
| 07 | `07_clinical_data.md` | Diagnoses, medications, vitals, labs |
| 08 | `08_users_staff.md` | Staff, providers, credentials, roles |
| 09 | `09_tfc.md` | Treatment Foster Care |
| 10 | `10_otp.md` | Opioid Treatment Program |
| 11 | `11_transportation.md` | Client transportation |
| 12 | `12_crew_groups.md` | Group therapy sessions |
| 13 | `13_bed_management.md` | Residential bed tracking |
| 14 | `14_prescriptions_erx.md` | Electronic prescribing |
| 15 | `15_labs.md` | Laboratory orders and results |

## Critical Rules

### MariaDB Syntax (NOT PostgreSQL)
- Use `CASE WHEN` not `FILTER(WHERE)`
- Use `CURDATE()` not `CURRENT_DATE`
- Use `TIMESTAMPDIFF()` for date math
- Use `DATE_FORMAT()` for date formatting
- `tinyint(1)` is boolean — use `= 1` / `= 0`, NOT `IS TRUE` / `IS FALSE`

### Soft Deletes
- Most tables use `deleted_at IS NULL` to filter active records
- **Always** include this filter unless the user wants historical data
- Some tables (like `cssrs_suicides`, `suicidal_ideations`, `client_high_risks`) do NOT have `deleted_at` — check with `get_table_info` first if unsure

### Names Are in a Separate Table
- Client names: `JOIN names n ON n.person_id = p.id AND n.deleted_at IS NULL`
- Staff names: `JOIN people p ON p.identifiable_id = u.id AND p.identifiable_type = 'User'` then `JOIN names n ON n.person_id = p.id`
- For latest name: use `MAX(n.id)` subquery or `ORDER BY n.id DESC LIMIT 1`

### STI Tables
- `people.type = 'Client'` for patients
- `companies.type = 'Payor'` for insurance companies
- Hidden/merged clients: filter with `(p.hidden IS NULL OR p.hidden = 0)`

### Money Columns
- ALL financial amounts are `*_cents` columns (integers)
- Always divide by `100.0` for dollar display: `amount_cents / 100.0 AS amount_dollars`

### Appointment Status (Timestamp-Based)
- No `status` column — derive from timestamps:
  - Completed: `checked_out_at IS NOT NULL`
  - No-show: `noshow_at IS NOT NULL`
  - Cancelled: `cancelled_at IS NOT NULL`
  - Checked in: `checked_in_at IS NOT NULL AND checked_out_at IS NULL`
  - Valid: `deleted_by IS NULL AND cancelled_at IS NULL AND noshow_at IS NULL`

### Insurance
- Self-pay payor: `companies.id = 1` (scope `self_pay` / `not_self_pay` in Rails)
- Priority values: `first`, `second`, `third`, `fourth`, `fifth`, `self`
- Cards (images): `pictures` table with `picturable_type = 'InsurancePolicy'`

### Vitals
- BP columns: `bp_right_arm_sys`, `bp_right_arm_dia`, `bp_left_arm_sys`, `bp_left_artm_dia` (note typo on left arm diastolic)
- High BP threshold: systolic >= 130 OR diastolic >= 80

### Suicide Risk (C-SSRS)
- Main table: `cssrs_suicides` (no `deleted_at` column)
- Ideations: `suicidal_ideations` joined via `cssrs_suicide_id`
- Risk assessments: `risk_assessments` (has `deleted_at`)

## Query Workflow

1. Read the relevant semantic layer file(s)
2. If unsure about a column, use `mcp__bear-db__get_table_info` to verify
3. Write the query using MariaDB syntax
4. Present results in a clear table format
5. Highlight key insights and anomalies
6. When results are large, get summary counts first, then drill down

## Responding

- Always show the data in a formatted markdown table
- Add key takeaways / insights after the data
- Flag data quality issues (nulls, suspicious values, inconsistencies)
- Offer to drill deeper or pivot the analysis
- When providing ActiveRecord equivalents, give them as one-liners for easy console paste

$ARGUMENTS
