# InsurGateway Error Management MCP Server

[![npm version](https://img.shields.io/npm/v/igw-error-management-mcp.svg)](https://www.npmjs.com/package/igw-error-management-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for tracking, analyzing, and reporting errors from [InsurGateway](https://insurgateway.com/).

## Features

- **Error Tracking** — List, filter, sort, and search errors by date, branch, product, company, agent, status, and free text
- **Error Logs** — View detailed request/response logs for each error
- **Error Analysis** — Get analysis details with possible causes and suggestions
- **Error Actions** — Pin errors, update status, send reports, and file bug reports
- **Reports** — Success rates, branch/agent/company breakdowns
- **Lookups** — Search products and list insurance companies for filtering

## Setup

Choose your tool below. Replace credentials with your own.

### Environments

| Environment | `IGW_BASE_URL` |
|-------------|----------------|
| Test | `https://testgatewayapi.insurapps.net/api` |
| Production | `https://gatewayapi.insurapps.net/api` |

---

### Claude Code

```bash
claude mcp add-json --scope user igw-error-management '{
  "command": "npx",
  "args": ["-y", "igw-error-management-mcp@latest"],
  "env": {
    "IGW_BASE_URL": "https://testgatewayapi.insurapps.net/api",
    "IGW_USERNAME": "your-username",
    "IGW_PASSWORD": "your-password",
    "IGW_WEB_API_KEY": "your-api-key"
  }
}'
```

### Claude Desktop

Edit config file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "igw-error-management": {
      "command": "npx",
      "args": ["-y", "igw-error-management-mcp@latest"],
      "env": {
        "IGW_BASE_URL": "https://testgatewayapi.insurapps.net/api",
        "IGW_USERNAME": "your-username",
        "IGW_PASSWORD": "your-password",
        "IGW_WEB_API_KEY": "your-api-key"
      }
    }
  }
}
```

Restart Claude Desktop after saving.

### Cursor

Add to `.cursor/mcp.json` in your project root (or `~/.cursor/mcp.json` for global):

```json
{
  "mcpServers": {
    "igw-error-management": {
      "command": "npx",
      "args": ["-y", "igw-error-management-mcp@latest"],
      "env": {
        "IGW_BASE_URL": "https://testgatewayapi.insurapps.net/api",
        "IGW_USERNAME": "your-username",
        "IGW_PASSWORD": "your-password",
        "IGW_WEB_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "igw-error-management": {
      "command": "npx",
      "args": ["-y", "igw-error-management-mcp@latest"],
      "env": {
        "IGW_BASE_URL": "https://testgatewayapi.insurapps.net/api",
        "IGW_USERNAME": "your-username",
        "IGW_PASSWORD": "your-password",
        "IGW_WEB_API_KEY": "your-api-key"
      }
    }
  }
}
```

### OpenAI Codex CLI

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.igw-error-management]
command = "npx"
args = ["-y", "igw-error-management-mcp@latest"]

[mcp_servers.igw-error-management.env]
IGW_BASE_URL = "https://testgatewayapi.insurapps.net/api"
IGW_USERNAME = "your-username"
IGW_PASSWORD = "your-password"
IGW_WEB_API_KEY = "your-api-key"
```

### Antigravity (Firebase Studio)

Add to `.idx/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "igw-error-management": {
      "command": "npx",
      "args": ["-y", "igw-error-management-mcp@latest"],
      "env": {
        "IGW_BASE_URL": "https://testgatewayapi.insurapps.net/api",
        "IGW_USERNAME": "your-username",
        "IGW_PASSWORD": "your-password",
        "IGW_WEB_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Example Queries

Once set up, try asking your AI assistant:

- *"Son 24 saatte hangi hatalar var?"*
- *"Quick Sigorta'daki çözülmemiş hataları göster"*
- *"Trafik branşında en çok hata veren sigorta şirketleri hangileri?"*
- *"Bu hatanın request/response detayına bak"*
- *"Son 1 haftada ConnectionError olan hataları listele"*
- *"Allianz Sigorta'nın ürünlerinde timeout hatalarını getir"*
- *"Bu hatayı analiz et, ne olmuş?"*
- *"Bu hatayı IGW ekibine bug olarak raporla"*
- *"Hata mesajında 'araç tarzı' geçen tüm kayıtları bul"*
- *"Doğa Sigorta'nın başarı oranını göster"*
- *"Branş bazında hata raporu çek"*
- *"Bu hatanın durumunu 'Çözüldü' olarak güncelle"*
- *"Hangi sigorta şirketleri aktif?"*
- *"Kasko ürünlerini ara"*

## Tools

### Error Queries (read-only)

| Tool | Description |
|------|-------------|
| `igw_errors_list` | List errors with filters, sorting, pagination, and free text search |
| `igw_errors_summary` | Lightweight error statistics — status counts per operation type |
| `igw_errors_operations` | Get error operations — which service operations produce errors |
| `igw_errors_logs` | Get detailed error log entries |
| `igw_errors_log_detail` | Get full request/response data for a specific error log |
| `igw_errors_analyze` | Analyze a specific error — possible causes and suggestions |

### Reports (read-only)

| Tool | Description |
|------|-------------|
| `igw_errors_success_rate` | Overall success/failure rates (proposals and policies) |
| `igw_errors_report_by_branch` | Error report broken down by branch (Kasko, Trafik, etc.) |
| `igw_errors_report_by_company` | Error report broken down by insurance company |
| `igw_errors_report_by_agent` | Error report broken down by agent |

### Error Actions (write)

| Tool | Description |
|------|-------------|
| `igw_errors_pin` | Pin/unpin an error for tracking |
| `igw_errors_update_status` | Update error analysis status (Solved, InProgress, UserMistake, etc.) |
| `igw_errors_send_report` | Send an error report with description to the relevant team |
| `igw_errors_send_bug_report` | Send a bug report by reference number to InsurGateway |

### Lookups (read-only)

| Tool | Description |
|------|-------------|
| `igw_products_search` | Search products by name — get product IDs for error filters |
| `igw_insurance_companies` | List available insurance companies — get company IDs for error filters |

### Key Parameters for `igw_errors_list`

| Parameter | Description |
|-----------|-------------|
| `BeginDate` / `EndDate` | Date range (ISO 8601) |
| `ErrorQuery` | Free text search within error messages |
| `SortColumn` | Sort by: `GroupCount`, `AgentName`, `LastErrorDate`, `InsuranceCompanyName`, `ProductName` |
| `SortDescending` | Sort direction (true = highest first) |
| `PageNumber` / `PageSize` | Pagination (default page size: 10) |
| `AgentId` | Filter by specific agent |
| `InsuranceCompanyId` | Filter by insurance company |
| `ServiceOperationId` | 1 = Teklif (Proposal), 2 = Poliçe (Policy) |

### AnalyzeStatus Values

| Value | Status |
|-------|--------|
| 0 | Not Analysed (Analiz Edilmedi) |
| 1 | In Progress (İnceleniyor) |
| 2 | Solved (Çözüldü) |
| 3 | Nothing To Do (Şirket Kuralı / Önlenemez Hata) |
| 4 | User Mistake (Kullanıcı Hatası) |
| 5 | Connection Error (Servis Bağlantı Hatası) |
| 6 | Operation Timeout (Zaman Aşımı) |

## Claude Code Skill (Optional)

[Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills), Claude Code'un belirli araclari daha etkili kullanmasini saglayan ogretilebilir talimat dosyalaridir. Bu repo, IGW hata yonetimi icin ozel bir skill dosyasi (`SKILL.md`) icerir. Skill yuklendiginde Claude Code; tool parametrelerini, is akislarini, hata durumlarini ve best practice'leri bilir — her seferinde aciklamaniza gerek kalmaz.

> **Not:** Skill kurulumu MCP server kurulumundan bagimsizdir. MCP server'i yukledikten sonra opsiyonel olarak skill'i de ekleyebilirsiniz.

### Kurulum

```bash
# Skill dosyasini Claude Code'a yukle
claude skill add --name igw-error-management --source-url https://raw.githubusercontent.com/yusufaltunbicak/igw-error-management-mcp/main/SKILL.md
```

Alternatif olarak, dosyayi manuel indirip yukleyebilirsiniz:

```bash
# SKILL.md'yi indir ve Claude Code skills dizinine kopyala
mkdir -p ~/.claude/skills/igw-error-management
curl -o ~/.claude/skills/igw-error-management/SKILL.md \
  https://raw.githubusercontent.com/yusufaltunbicak/igw-error-management-mcp/main/SKILL.md
```

## License

MIT
