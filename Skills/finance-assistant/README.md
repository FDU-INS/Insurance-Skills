# Finance Assistant Skill

> Personal finance copilot for **Claude Code** and **Claude Cowork** — budgets, savings goals, investments, debt optimization, taxes, insurance, net worth, bank import, and scenario modeling. Privacy-first: all data stays on your machine, encrypted at rest.

---

## Table of Contents

1. [What It Does](#what-it-does)
2. [Quick Start](#quick-start)
3. [Locales](#locales)
4. [How It Works](#how-it-works)
5. [Data Storage Layout](#data-storage-layout)
6. [Security & Privacy](#security--privacy)
7. [Bank Statement Import](#bank-statement-import)
8. [Module Reference](#module-reference)
9. [Example Conversations](#example-conversations)
10. [Running Tests](#running-tests)

---

## What It Does

Finance Assistant covers the full personal finance lifecycle across 11 operating modes:

| Mode | What you say | What you get |
|------|-------------|-------------|
| **Budget Manager** | "how am I doing on my budget?" | Variance by category, overspend alerts, pace warnings |
| **Transaction Logger** | "I spent €42 at REWE" | Logged, auto-categorized, budget actuals updated |
| **Savings Planner** | "I want to save €10k for a trip" | Timeline projection, monthly contribution needed |
| **Investment Tracker** | "show my portfolio" | Allocation, total return, XIRR, rebalance suggestions |
| **Debt Optimizer** | "best way to pay off my debts?" | Avalanche vs snowball comparison, debt-free date, interest saved |
| **Tax Module** | "what can I deduct?" | Locale-specific deductions (German 2024-2026 bundled) |
| **Insurance Reviewer** | "do I have enough coverage?" | Coverage gap analysis, renewal alerts |
| **Net Worth Dashboard** | "where do I stand?" | Net worth with 7-domain health score and trend |
| **Data Import** | "import this DKB CSV" | Parse → preview → categorize → deduplicate → import |
| **Scenario Lab** | "should I rent or buy?" | Before/after comparison with multi-year projection |
| **Specialist Handoff** | complex case | Structured brief for a Steuerberater or financial adviser |

### Proactive Session Alerts

Every session start checks five domains automatically:
- Budget overspend or pacing warnings ("85% of Groceries used at 16% of month")
- Upcoming recurring payments in the next 7 days
- Savings goal deadlines within 45 days
- Tax filing deadlines within 45 days (German locale)
- Monthly FIRE progress bar (`[████████░░░░░░░░░░░░] 42.3% — €317k / €750k`)

---

## Quick Start

### 1. Clone the skill

```bash
git clone --recurse-submodules https://github.com/googlarz/finance-assistant-skill.git
cd finance-assistant-skill
pip install -r requirements.txt
```

---

### Install in Claude Code

Add as a skill in `~/.claude/settings.json`:

```json
{
  "skills": [
    {
      "name": "finance-assistant",
      "path": "/path/to/finance-assistant-skill"
    }
  ]
}
```

Then start a session: `What's my financial health?`

---

### Install in Claude Cowork

Cowork gives you the same agent capabilities as Claude Code in a desktop-friendly interface. For the best experience, set it up as a dedicated project:

**1. Create a new project**
Open Cowork → Projects → **New Project**. Name it something like `Finance`.

**2. Add a project instruction**
In the project's Instructions field, add:

```
Always load and use the Finance Assistant skill /finance-assistant-skill.
Start every session by running skill.py to load my profile and surface any alerts.
```

**3. Start the project**
Open the Finance project and say: `What's my financial health?`

Claude will load your profile, surface any session alerts (budget warnings, upcoming bills, tax deadlines), and be ready for any finance question.

> **Tip:** Pin the Finance project to your Cowork sidebar so it's one click away at the start of each day.

---

## Locales

Tax rules and social contribution logic live in locale plugins — country-specific modules that the skill loads dynamically.

Locales are maintained in a separate git submodule at **https://github.com/googlarz/finance-assistant-locales**. The `--recurse-submodules` flag in the clone command above pulls them automatically.

The **German locale (`de`)** is bundled with full 2024–2026 support, covering income tax, social contributions, deduction discovery, filing deadlines, and GKV/PKV thresholds.

New locales can be contributed independently to the locales repository without touching the main skill code. See the [locales repo](https://github.com/googlarz/finance-assistant-locales) for the plugin interface, provenance format, and contribution guide.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code / Cowork                         │
│                                                                 │
│   You ──► skill.py ──► profile_manager ──► session_alerts      │
│                │                                                │
│                ▼                                                │
│         ┌──────────────────────────────────────────┐           │
│         │              11 Modes                    │           │
│         │  Budget · Transactions · Goals           │           │
│         │  Investments · Debt · Tax · Insurance    │           │
│         │  Net Worth · Import · Scenarios · Handoff│           │
│         └──────────────┬───────────────────────────┘           │
│                        │                                        │
│              ┌─────────▼──────────┐                            │
│              │   scripts/*.py     │  ◄── locale plugins        │
│              │  (real math, not   │       locales/de/          │
│              │   hallucination)   │       locales/xx/ ...      │
│              └─────────┬──────────┘                            │
│                        │                                        │
│              ┌─────────▼──────────┐                            │
│              │    .finance/       │  local only, never uploaded │
│              │  profile · budgets │  encrypted at rest          │
│              │  investments · tax │  chmod 600, git-ignored     │
│              └────────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

### Profile-First Architecture

Every session starts by loading your stored profile with `profile_manager.py`. All scripts operate on this profile + the `.finance/` data directory. Nothing is hardcoded; everything adapts to your locale, currency, and situation.

### Insight Pipeline

The insight engine (`insight_engine.py`) runs after every major data update. It dispatches to domain-specific generators:

```
budget_insights → savings_insights → investment_insights
→ debt_insights → insurance_insights → tax_insights → net_worth_insights
```

Each insight carries a 4-level status:
- `ready` — actionable right now
- `needs_input` — needs one more fact from you
- `needs_evidence` — needs a document or statement
- `detected` — background risk found, FYI

And a confidence label: `Definitive` | `Likely` | `Debatable` | `Avoid`

### Locale Plugin System

Tax rules are country-specific plugins in `locales/<country_code>/`. Each locale exports a standard interface:

```python
LOCALE_CODE = "de"
SUPPORTED_YEARS = [2024, 2025, 2026]
def get_tax_rules(year) -> dict
def calculate_tax(profile, year) -> dict
def get_filing_deadlines(year) -> list[dict]
def get_social_contributions(gross, year) -> dict
def generate_tax_claims(profile, year) -> list[dict]
```

The German locale is fully bundled via the `locales/` submodule. New locales can be scaffolded automatically via `locale_loader.py`.

### Multi-Currency

All amounts use the `Money` class (backed by `Decimal`) to avoid floating-point errors. Exchange rates are cached in `.finance/exchange_rates.json` with a 24-hour TTL; fallback rates are clearly marked as lower confidence.

---

## Data Storage Layout

All data is project-local in `.finance/`. No cloud sync, no external APIs, no telemetry.

```
.finance/
├── finance_profile.json          # Core profile (employment, housing, goals, preferences)
├── accounts/
│   ├── accounts.json             # Account registry (no IBANs stored)
│   └── transactions/
│       └── <account>_<year>.json # Transaction log by account and year
├── budgets/
│   ├── 2025.json                 # Annual budget
│   └── 2025-04.json             # Monthly budget with actuals
├── goals/
│   └── goals.json               # Savings goals with progress
├── investments/
│   ├── portfolio.json            # Holdings with current values
│   └── snapshots/
│       └── 2025-04-01.json      # Point-in-time portfolio snapshots
├── debt/
│   ├── debts.json               # Debt registry with rates and balances
│   └── payoff_plans/
│       └── <plan_id>.json       # Avalanche/snowball simulation results
├── insurance/
│   └── policies.json            # Insurance policies and renewal dates
├── net_worth/
│   └── snapshots/
│       └── 2025-04-01.json      # Monthly net worth snapshots
├── taxes/
│   └── de/
│       ├── 2024.json            # Tax year data
│       └── 2024-claims.json     # Deduction claims for filing
├── imports/
│   └── import_log.json          # Import history for deduplication
├── workspace/
│   └── 2025.json                # Financial health dashboard
├── exchange_rates.json           # Cached FX rates (24h TTL)
└── audit/
    └── access_log.json           # Audit trail of all data access
```

**What is never stored:**
- Bank login credentials, passwords, PINs, TANs
- Full IBAN or bank account numbers
- Credit card numbers or CVV codes
- Tax IDs, passport numbers, national IDs
- Raw document contents

---

## Security & Privacy

### Design Principles

1. **Local-only**: All data lives in `.finance/` on your machine. No network calls for your personal data. No telemetry. No cloud sync.
2. **Structured summaries, not raw data**: Transaction amounts and categories are stored, not raw bank statements or login sessions.
3. **You own the delete button**: Every data category can be deleted individually or all at once.
4. **Encryption at rest**: Fernet AES-128-CBC + HMAC-SHA256 — the same authenticated encryption scheme used in production web services.
5. **Passphrase quality enforced**: The system rejects weak passphrases before encrypting (minimum 12 chars, character variety required), because a strong cipher with a weak key is still weak.
6. **Atomic writes**: Encrypted files are written to a `.enc.tmp` file first, then atomically renamed — a power failure or crash cannot leave a half-encrypted, unreadable file.
7. **File permissions**: `harden_permissions()` sets `.finance/` to `700` (owner-only directory) and all files to `600` (owner-only read/write). Other OS users on the same machine cannot read your data.
8. **Git guard**: On first session, `.finance/` is automatically added to `.gitignore` so financial data cannot be accidentally committed and pushed to a repository.
9. **Audit log**: Every significant data access (read, write, encrypt, export, delete) is logged to `audit/access_log.json` with a timestamp.
10. **Sanitize before sharing**: `sanitize_for_sharing(data)` strips all PII (names, employers, payees, addresses) before you share data to get help — financial amounts and structures are preserved.

### Encryption Details

```
Key derivation: PBKDF2-HMAC-SHA256
Iterations:     480,000 (NIST 2023 recommendation)
Salt:           16 bytes random per file (unique per encryption)
Cipher:         AES-128 in CBC mode (via Fernet)
MAC:            HMAC-SHA256 (Fernet built-in; prevents ciphertext tampering)
Encoding:       Base64url
Dependency:     pip install cryptography
```

Each file gets its own random salt. Two files encrypted with the same passphrase produce different ciphertexts — you cannot tell if two files contain the same data by comparing them.

The salt is stored alongside the ciphertext (standard practice — it only makes brute-force harder when combined with high iteration counts; it does not weaken the encryption).

### Encrypted Export

Backups can be encrypted before leaving your machine:

```python
# Encrypted backup — safe to store in cloud or email to yourself
export_all_data(passphrase="MyStr0ng!Passphrase")

# Plaintext export — keep offline only
export_all_data()
```

The encrypted export uses the same Fernet key derivation as individual file encryption. The passphrase is never stored anywhere.

### All Security Controls

```python
from scripts.data_safety import (
    get_privacy_summary,          # Full security status report
    get_data_inventory,           # Audit what's stored and where
    harden_permissions,           # chmod 600/700 on all .finance/ files
    check_permissions,            # Check for insecure file permissions
    ensure_gitignore_protection,  # Add .finance/ to .gitignore
    encrypt_sensitive_files,      # Encrypt profile, accounts, investments, debt
    decrypt_sensitive_files,      # Decrypt for use
    encrypt_file,                 # Encrypt a single file
    decrypt_file,                 # Decrypt a single file
    export_all_data,              # Export (plain or encrypted)
    import_data,                  # Import from export file
    delete_all_data,              # Permanent wipe (requires confirm=True)
    delete_category,              # Delete one category (requires confirm=True)
    sanitize_for_sharing,         # Strip PII before sharing for help
    get_access_log,               # View audit trail
)
```

### What Happens on First Session

```
skill.py (session start)
  ├── ensure_gitignore_protection()   # .finance/ → .gitignore
  ├── check_permissions()             # warn if group/world readable
  └── get_profile()                   # load or start onboarding
      └── (new user) show privacy statement
```

The privacy statement is shown once:

> *Your data lives only in `.finance/` on your machine — nothing is ever uploaded. You can encrypt it, export it, or delete it completely at any time. I never store bank credentials, card numbers, IBANs, or government IDs.*

### Threat Model

| Threat | Protection |
|--------|-----------|
| Another user on same machine reads your files | `harden_permissions()` — chmod 600/700 |
| Accidental `git push` of financial data | `ensure_gitignore_protection()` — automatic on session start |
| Laptop stolen, unencrypted disk | `encrypt_sensitive_files(passphrase)` + OS disk encryption (FileVault/LUKS) |
| Weak passphrase undermines AES | `_check_passphrase_strength()` — enforced before every encrypt call |
| Power failure during encryption corrupts file | Atomic write via `.enc.tmp` → `rename()` — POSIX atomic |
| Sharing data for help leaks names/employer | `sanitize_for_sharing()` — redacts all PII fields |
| Unexpected data access by a process | `get_access_log()` — timestamped audit trail |
| Cloud backup of export file exposes data | `export_all_data(passphrase=...)` — Fernet-encrypted export |

### Known Limitations

- **Memory**: Decrypted data resides in Python process memory while the skill is running. Python does not securely zero memory on deallocation. This is a fundamental Python limitation.
- **OS keychain**: Passphrases are not stored in the OS keychain (macOS Keychain, GNOME Keyring). You must provide the passphrase each session when using encrypted files. This is deliberate — no stored secret means no stored secret to steal.
- **Disk encryption**: If your disk is not encrypted (macOS FileVault, Linux LUKS), Fernet protects against OS-level access control bypass but not against forensic disk reads. Enable full-disk encryption for maximum protection.
- **Audit log**: The access log itself is protected by `harden_permissions()` but is not encrypted by default (it contains timestamps and action types, not financial amounts).

---

## Bank Statement Import

### Supported Formats

| Format | Banks / Sources |
|--------|----------------|
| CSV (auto-detected by header fingerprint) | DKB, ING-DiBa, Comdirect, N26, Wise (EUR), Revolut (EUR), generic fallback |
| MT940 | Any German bank (SWIFT standard) |
| OFX / QFX | Most German brokers, international banks |

### Import Flow

1. **Detect format** — header fingerprinting identifies the bank automatically
2. **Parse** — extract date, amount, payee, description
3. **Preview** — show first 10 transactions for review
4. **Confirm** — user approves before any data is written
5. **Auto-categorize** — keyword + payee rules assign categories
6. **Deduplicate** — exact-match deduplication against existing transactions
7. **Update** — account balance and budget actuals refreshed

### Auto-Categorization

`transaction_normalizer.py` maps transactions to 30 categories across 8 domains. `category_learner.py` remembers corrections and applies them to future imports from the same payee — the categorization improves over time.

---

## Module Reference

### Core

| Module | Purpose |
|--------|---------|
| `skill.py` | Session entry: load profile, run security checks, surface alerts |
| `finance_storage.py` | Path resolution and JSON persistence |
| `profile_manager.py` | v2 profile schema, deep-merge updates |
| `currency.py` | `Money` dataclass (Decimal), exchange rates with 24h cache |

### Accounts & Transactions

| Module | Purpose |
|--------|---------|
| `account_manager.py` | CRUD for checking/savings/investment/loan accounts |
| `transaction_logger.py` | Log income/expense with auto-categorization (30 categories) |
| `recurring_engine.py` | Auto-generate recurring transactions (rent, salary, subscriptions) |
| `category_learner.py` | Learn from corrections to improve future auto-categorization |

### Planning & Goals

| Module | Purpose |
|--------|---------|
| `budget_engine.py` | Create budgets, 50/30/20 auto-distribution, variance analysis |
| `goal_tracker.py` | Savings goals with completion projections |

### Wealth

| Module | Purpose |
|--------|---------|
| `investment_tracker.py` | Portfolio CRUD, allocation, FIRE number, monthly snapshots |
| `investment_returns.py` | TWR, XIRR (Newton's method), per-holding performance |
| `debt_optimizer.py` | Avalanche/snowball simulation, mortgage optimization, debt-free date |
| `insurance_analyzer.py` | Policy tracking, coverage gaps, renewal alerts |
| `net_worth_engine.py` | Aggregate assets + investments − liabilities, JSON snapshots |

### Tax

| Module | Purpose |
|--------|---------|
| `tax_engine.py` | Country-agnostic interface, delegates to locale plugin via `importlib` |
| `locale_registry.py` | Rule provenance (source URL, verification date, confidence) |
| `locale_loader.py` | Dynamic locale import, on-demand skeleton builder for new countries |
| `locales/de/` | Full German locale (2024-2026, all parameters filled) — via submodule (finance-assistant-locales) |

### Import

| Module | Purpose |
|--------|---------|
| `import_router.py` | Format detection and routing |
| `csv_importer.py` | DKB, ING-DiBa, Comdirect, N26, Wise, Revolut, generic |
| `mt940_importer.py` | SWIFT MT940 with graceful fallback if library not installed |
| `ofx_importer.py` | OFX/QFX with normalized date parsing |
| `transaction_normalizer.py` | Auto-categorize, deduplicate, normalize amounts |

### Intelligence & Output

| Module | Purpose |
|--------|---------|
| `insight_engine.py` | Cross-domain insights, 4-status model, sorted by urgency |
| `scenario_engine.py` | Salary comparison, FIRE projection, rent-vs-buy, debt-vs-invest, mortgage |
| `workspace_builder.py` | 7-domain weighted health score |
| `output_builder.py` | Structured deliverables assembled into an output suite |
| `report_renderer.py` | Markdown and HTML reports |
| `snapshot_scheduler.py` | Monthly auto-snapshots (portfolio and net worth) |
| `session_alerts.py` | Proactive session nudges (budget, bills, deadlines, FIRE) |
| `document_sorter.py` | Classify financial documents by type |
| `adviser_handoff.py` | Structured referral brief for Steuerberater or adviser |

### Security

| Module | Purpose |
|--------|---------|
| `data_safety.py` | Fernet AES encryption, permissions hardening, git guard, export, delete, sanitize, audit |

---

## Example Conversations

### Budget Check

```
You:  How am I doing on my April budget?
FA:   €340 of €400 food budget used (85%) — 28 days into 30-day month. On pace.
      Transport: €112 / €150 (75%) — fine.
      Eating out: €89 / €80 — OVER by €9 ⚠

      Suggestion: €11 left in eating out. One meal left this month.
      Adjacent: Groceries has €60 remaining — cooking covers the gap.
```

### FIRE Calculation

```
You:  When can I retire if I invest €1,500/month?
FA:   FIRE number: €900,000  (€36,000 expenses ÷ 4% withdrawal rate)
      Current portfolio: €180,000
      Monthly investment: €1,500 at 7% average return

      Projected FIRE date: 2044 (18 years)
      Formula: FV = PV×(1+r)^n + PMT×((1+r)^n−1)/r

      Confidence: Likely (assumes 7% return; actual will vary)
      What changes it: every extra €200/month cuts ~1 year.
```

### Debt Optimization

```
You:  Best strategy to pay off my 3 loans?
FA:   Avalanche (highest rate first):
        Credit card €3,200 @ 18.9% → Car loan €8,600 @ 5.9% → Ratenkredit €13,000 @ 3.4%
        Interest saved vs minimum: €2,840 | Debt-free: Nov 2027

      Snowball (smallest balance first):
        Same order (happens to match) in this case
        Interest saved vs minimum: €1,920 | Debt-free: Feb 2028

      → Avalanche saves €920 more and finishes 3 months earlier.
        Choose snowball only if you need the win of a quick first payoff.
```

### Tax Deductions (German)

```
You:  What can I deduct this year?
FA:   Profile: angestellt, Berlin, homeoffice 3 days/week

      ✓ Arbeitnehmer-Pauschbetrag: €1,230 (automatic)
      ✓ Homeoffice: €6/day × 210 days = €1,260 (at cap)
      ✓ Pendlerpauschale: €0 (homeoffice replaces commute)
      ? Gewerkschaftsbeitrag: enter your amount
      ? Fortbildungskosten: any training expenses this year?

      Estimated refund above Pauschbetrag: ~€340
      Confidence: Likely (exact figure needs actual receipts)
```

---

## Running Tests

```bash
python3 -m pytest tests/ -v
# 154 tests — all modules, all scenarios
```

Tests use an isolated `.finance/` directory per test via the `isolated_finance_dir` autouse fixture — they never touch real data.

Key test files:

| File | What it tests |
|------|-------------|
| `test_data_safety.py` | Encryption roundtrip, wrong passphrase, unique salts, permissions, git guard, encrypted export, sanitize |
| `test_session_alerts.py` | Budget warnings, goal deadline alerts, urgency sorting |
| `test_locale_de.py` | German tax calculation, 2026 parameters all non-null |
| `test_import_system.py` | CSV/MT940/OFX parsing, bank detection, deduplication |
| `test_scenario_engine.py` | FIRE, salary comparison, rent-vs-buy, debt-vs-invest |
| `test_workspace_builder.py` | 7-domain health score calculation |
| `test_investment_tracker.py` | FIRE number, portfolio growth projection, snapshots |
| `test_debt_optimizer.py` | Avalanche vs snowball, interest savings, debt-free date |
