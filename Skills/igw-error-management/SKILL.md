---
name: igw-error-management
description: MCP skill for IGW (InsurGateway) error management — list, analyze, report, and manage insurance integration errors across test and production environments. Invoke whenever user asks about IGW errors, insurance gateway issues, success rates, or error reports.
author: yusufaltunbicak
version: "2.0.0"
tags:
  - igw
  - insurgateway
  - insurance
  - error-management
  - mcp
  - sigorta
  - entegrasyon
---

# IGW Error Management MCP Skill

Use this skill when the user wants to investigate, analyze, report on, or manage InsurGateway (IGW) integration errors. Covers error listing, log inspection, root cause analysis, success rate reports, and error status management for Turkish insurance integrations.

## Environments

Two MCP server instances are available:

| Server | Prefix | Use Case |
|--------|--------|----------|
| `igw-error-management-test` | Test environment | Development, debugging, safe exploration |
| `igw-error-management-prod` | Production environment | Real production errors, live data |

**IMPORTANT:** Always confirm which environment the user intends. Default to **test** unless explicitly told otherwise. Production write operations (pin, status update, send report, bug report) should be confirmed with the user before execution.

## Tool Reference

### Error Queries (Read-Only)

#### `igw_errors_list` — List errors with filters

Returns grouped errors with categories and detailed error entries.

| Parameter | Type | Description |
|-----------|------|-------------|
| `BeginDate` | string (ISO 8601) | Start date filter (e.g. `2026-03-01T00:00:00`) |
| `EndDate` | string (ISO 8601) | End date filter |
| `AgentId` | number | Filter by agent/acente ID |
| `BranchId` | number | Filter by branch ID (Kasko, Trafik, etc.) |
| `ProductId` | number | Filter by product ID |
| `InsuranceCompanyId` | number | Filter by insurance company ID |
| `ServiceOperationId` | number | 1 = Teklif (Proposal), 2 = Polica (Policy) |
| `NotAnalysed` | boolean | Show only not-analysed errors |
| `Solved` | boolean | Show only solved errors |
| `InProgress` | boolean | Show only in-progress errors |
| `NothingToDo` | boolean | Show only nothing-to-do errors |
| `UserMistake` | boolean | Show only user-mistake errors |
| `ConnectionError` | boolean | Show only connection errors |
| `OperationTimeout` | boolean | Show only timeout errors |
| `ErrorQuery` | string | Free text search in error messages |
| `IncludeProducts` | boolean | Include product details in response |
| `ClientChannel` | string | Filter by client channel |
| `PageNumber` | number | Page number (default: 1) |
| `PageSize` | number | Items per page (default: 20) |
| `SortColumn` | string | Sort by: `GroupCount`, `AgentName`, `LastErrorDate`, `InsuranceCompanyName`, `ProductName` |
| `SortDescending` | boolean | Sort direction |

#### `igw_errors_summary` — Error statistics

Lightweight status counts per service operation. Same filters as `igw_errors_list` (without pagination). Great for quick overview dashboards.

#### `igw_errors_operations` — Service operations with error stats

Shows which operations (Teklif/Police) produce errors and their counts. Same filter options.

#### `igw_errors_logs` — Detailed error log entries

Returns error logs with request/response data. Same filters as `igw_errors_list`.

#### `igw_errors_log_detail` — Single error log detail

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | number | Error log ID |

Returns full request/response XML/JSON payload sent to the insurance company and response received. Essential for debugging specific integration failures.

#### `igw_errors_analyze` — Analyze a specific error

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | number | Error ID |

Returns analysis details including possible root causes, affected products, and resolution suggestions.

### Reports (Read-Only)

All report tools share these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `BeginDate` | string (ISO 8601) | Start date |
| `EndDate` | string (ISO 8601) | End date |
| `AgentId` | number | Filter by agent |
| `BranchId` | number | Filter by branch |
| `ProductId` | number | Filter by product |
| `InsuranceCompanyId` | number | Filter by company |
| `ServiceOperationId` | number | 1 = Teklif, 2 = Police |

#### `igw_errors_success_rate` — Overall success/failure rates

Breakdown by Genel (Overall), Teklifler (Proposals), Policeler (Policies).

#### `igw_errors_report_by_branch` — Report by branch

Error breakdown by branch: Kasko, Trafik, Tamallayici Saglik, DASK, etc.

#### `igw_errors_report_by_company` — Report by insurance company

Error breakdown by company: Allianz, Zurich, Doga, Bereket, etc.

#### `igw_errors_report_by_agent` — Report by agent

Error breakdown by acente/agent with success rates.

### Error Actions (Write Operations)

#### `igw_errors_pin` — Pin/unpin error

| Parameter | Type | Description |
|-----------|------|-------------|
| `errorId` | number | Error ID to pin/unpin |
| `isPinned` | boolean | `true` to pin, `false` to unpin |

#### `igw_errors_update_status` — Update analysis status

| Parameter | Type | Description |
|-----------|------|-------------|
| `errorExplanationHash` | string | Error explanation hash identifier |
| `analyzeStatus` | number | Status value (0-6, see table below) |
| `serviceOperationId` | number | Optional: 1 = Teklif, 2 = Police |

#### `igw_errors_send_report` — Send error report to team

| Parameter | Type | Description |
|-----------|------|-------------|
| `errorId` | number | Error ID |
| `description` | string | Report description explaining the issue |

#### `igw_errors_send_bug_report` — File a bug report

| Parameter | Type | Description |
|-----------|------|-------------|
| `referenceNo` | string | Reference number (e.g. `IGW-12345`) |

### Lookups (Read-Only)

#### `igw_products_search` — Search insurance products

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Product name search (e.g. "Allianz Kasko", "Bereket Trafik") |
| `page` | number | Page number |
| `pageSize` | number | Items per page |

Returns product IDs for use as filters in other tools.

#### `igw_insurance_companies` — List all insurance companies

No parameters. Returns company IDs and names. Common companies:

| ID | Company |
|----|---------|
| 45 | Allianz |
| 18 | Zurich |
| 43 | Doga Sigorta |
| 57 | Bereket Sigorta |

## Error Analysis Status Values

| Value | Turkish | English | Use When |
|-------|---------|---------|----------|
| 0 | Analiz Edilmedi | Not Analysed | Default state, not yet reviewed |
| 1 | Inceleniyor | In Progress | Currently being investigated |
| 2 | Cozuldu | Solved | Fix has been applied |
| 3 | Sirket Kurali / Onlenemez Hata | Nothing To Do | Insurance company rule, cannot be fixed |
| 4 | Kullanici Hatasi | User Mistake | End user input error |
| 5 | Servis Baglanti Hatasi | Connection Error | Service connectivity issue |
| 6 | Zaman Asimi | Operation Timeout | Request timed out |

## Common Workflows

### Quick daily error check

```
1. igw_errors_summary (last 24h) → get status overview
2. igw_errors_list (NotAnalysed=true, last 24h) → find new unreviewed errors
3. igw_errors_success_rate (last 24h) → check overall health
```

### Investigate a specific error

```
1. igw_errors_list (with filters) → find the error group
2. igw_errors_logs (same filters) → get log entries
3. igw_errors_log_detail (id) → inspect full request/response payload
4. igw_errors_analyze (id) → get root cause analysis
5. igw_errors_update_status → mark as investigated
```

### Company-specific error analysis

```
1. igw_insurance_companies → get company ID
2. igw_errors_report_by_company (date range) → see which companies have issues
3. igw_errors_list (InsuranceCompanyId=X) → drill into specific company errors
4. igw_errors_logs → inspect detailed failures
```

### Branch performance report

```
1. igw_errors_report_by_branch (date range) → branch-level success rates
2. igw_errors_report_by_company (BranchId=X) → which companies fail in that branch
3. igw_errors_list (BranchId=X, SortColumn=GroupCount, SortDescending=true) → most frequent errors
```

### Product search and filter

```
1. igw_products_search (query="Kasko") → find product IDs
2. igw_errors_list (ProductId=X) → errors for that specific product
```

### Error triage workflow

```
1. igw_errors_list (NotAnalysed=true, SortColumn=GroupCount, SortDescending=true) → highest impact first
2. igw_errors_analyze (id) → understand the error
3. igw_errors_update_status → categorize (Solved, UserMistake, ConnectionError, etc.)
4. igw_errors_send_report (if needed) → notify the team
5. igw_errors_send_bug_report (if genuine bug) → file with IGW team
```

### Track a pinned error

```
1. igw_errors_pin (errorId, isPinned=true) → pin for follow-up
2. igw_errors_list (date range) → check if error recurs
3. igw_errors_pin (errorId, isPinned=false) → unpin when resolved
```

## Agent Best Practices

- **Date ranges:** Always use ISO 8601 format. For "last 24 hours", calculate from current time. For "today", use midnight to now.
- **Pagination:** Start with `PageSize=20`. If user needs more, increase or paginate.
- **Sorting:** Default to `LastErrorDate` descending for recent errors, `GroupCount` descending for most frequent.
- **Error investigation:** Always check `igw_errors_log_detail` before concluding on root cause — the request/response payload is the ground truth.
- **Status updates on prod:** Always confirm with the user before changing error status in production.
- **Reports:** When user asks for "error report", clarify if they want by branch, company, or agent — or provide all three for a comprehensive view.
- **Turkish context:** Many field values are in Turkish (branch names, error messages). Be prepared to translate or explain when needed.
- **Service operations:** Teklif = Proposal (quote request), Police = Policy (policy issuance). These are the two main operation types.
- **Free text search:** Use `ErrorQuery` parameter for searching specific error messages, XML tags, or insurance company error codes.
- **Large responses:** Results are auto-truncated at 25,000 characters. If data seems incomplete, narrow filters or reduce page size.

## Safety Notes

- **Environment awareness:** Always verify test vs production before write operations.
- **Status changes:** Updating error status affects the team's workflow. Confirm with user before bulk status updates.
- **Bug reports:** `igw_errors_send_bug_report` sends to the IGW team. Only use for genuine bugs, not user errors or known issues.
- **Error reports:** `igw_errors_send_report` sends to the internal team. Include clear, actionable descriptions.
- **Credentials:** MCP server handles authentication automatically. Never ask users for IGW credentials in chat.
