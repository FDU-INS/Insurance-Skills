# HealthSim Installation Guide

Complete installation instructions for HealthSim workspace including all dependencies.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Git LFS Setup](#git-lfs-setup)
4. [Python Environment](#python-environment)
5. [DuckDB Configuration](#duckdb-configuration)
6. [Claude Integration](#claude-integration)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Git** | 2.0+ | For repository cloning |
| **Git LFS** | 3.0+ | For large database files (required) |
| **Python** | 3.10+ | For healthsim-core package |
| **Claude Desktop or Code** | Latest | AI conversation interface |

### Operating System Support

- ✅ macOS (M1/M2/Intel)
- ✅ Linux (Ubuntu 20.04+, Debian, RHEL/CentOS)
- ✅ Windows (10/11 with WSL2 recommended)

---

## Quick Start

For experienced users, here's the minimal setup:

```bash
# 1. Install Git LFS
brew install git-lfs  # macOS
# or: apt-get install git-lfs  # Linux
# or: download from https://git-lfs.com  # Windows

# 2. Clone with LFS
git lfs install
git clone https://github.com/mark64oswald/healthsim-workspace.git
cd healthsim-workspace

# 3. Setup Python
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
cd packages/core
pip install -e .

# 4. Verify
python -c "from healthsim.db import get_connection; print('✅ HealthSim ready!')"
```

**Continue reading for detailed steps and explanations.**

---

## Git LFS Setup

HealthSim uses **Git Large File Storage (LFS)** to version control the database file (`healthsim.duckdb`, 1.16 GB). Git LFS is **required** - without it, you'll get pointer files instead of the actual database.

### Why Git LFS?

Regular Git is not designed for large binary files. Git LFS stores large files on a separate server while keeping small pointer files in the repository. This keeps clones fast while still providing version control for large assets.

### Installation

#### macOS (Homebrew)
```bash
brew install git-lfs
git lfs install
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install git-lfs
git lfs install
```

#### Linux (RHEL/CentOS)
```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash
sudo yum install git-lfs
git lfs install
```

#### Windows
1. Download installer from https://git-lfs.com
2. Run the installer
3. Open Git Bash and run: `git lfs install`

### Verifying Git LFS

After installation, verify Git LFS is working:

```bash
# Check Git LFS is installed
git lfs version
# Should output: git-lfs/3.x.x (GitHub; ...)

# Check LFS is initialized
git lfs env
# Should show LFS configuration
```

### Cloning with LFS

When cloning the HealthSim repository, Git LFS will automatically download large files:

```bash
# Clone repository (LFS files download automatically)
git clone https://github.com/mark64oswald/healthsim-workspace.git
cd healthsim-workspace

# Verify database file was downloaded (not a pointer)
ls -lh healthsim.duckdb
# Should show ~1.2 GB file, not a few hundred bytes

# Check LFS tracking
git lfs ls-files
# Should list: healthsim.duckdb
```

### Troubleshooting Git LFS

**Problem:** Database file is only a few KB (pointer file)

```bash
# Manually fetch LFS files
git lfs fetch
git lfs checkout
```

**Problem:** "This repository is over its data quota"

Git LFS has bandwidth limits on free GitHub accounts. If you encounter this:
1. Wait for the quota to reset (monthly)
2. Contact the repository owner
3. Or clone without LFS initially and download database separately

**Problem:** Slow clones

```bash
# Clone without LFS files initially
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/mark64oswald/healthsim-workspace.git
cd healthsim-workspace

# Download only the database file
git lfs pull --include="healthsim.duckdb"
```

---

## Python Environment

HealthSim requires Python 3.10 or newer.

### Check Python Version

```bash
python3 --version
# Should output: Python 3.10.x or higher
```

### Create Virtual Environment

Always use a virtual environment to avoid dependency conflicts:

```bash
cd healthsim-workspace

# Create virtual environment
python3 -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Your prompt should now show (.venv)
```

### Install HealthSim Core

The `healthsim-core` package includes all necessary dependencies including DuckDB:

```bash
cd packages/core
pip install -e .
```

This installs:
- `duckdb` - Embedded analytical database (no separate installation needed)
- `pydantic` - Data validation
- `pytest` - Testing framework
- Other dependencies as specified in `pyproject.toml`

### Verify Installation

```bash
python -c "import duckdb; print(f'DuckDB {duckdb.__version__}')"
# Should output: DuckDB 1.1.x

python -c "from healthsim.db import get_connection; print('HealthSim ready!')"
# Should output: HealthSim ready!
```

---

## DuckDB Configuration

DuckDB is an embedded database (like SQLite) - there's no separate server to install or configure.

### Database Location

The HealthSim database is located at:
```
healthsim-workspace/healthsim.duckdb
```

This file contains three schemas:
- **main**: Entity tables (patients, members, encounters, claims)
- **population**: Demographics and health indicators (416K records)
- **network**: Healthcare providers and facilities (10.4M records)

### Database Size & Performance

| Metric | Value |
|--------|-------|
| File size | 1.16 GB |
| Total records | 10.8M+ |
| Schemas | 3 (main, population, network) |
| Tables | 31 |
| Indexes | 8 (on network schema) |

**Performance characteristics:**
- Read queries: Very fast (in-process, no network)
- Aggregations: Optimized for analytics workloads
- Joins: Efficient cross-schema joins supported
- Concurrency: Single-writer, multiple-reader

### Connection Management

HealthSim uses a singleton connection pattern to prevent file locking issues:

```python
from healthsim.db import get_connection

# Get connection (automatically creates if needed)
conn = get_connection()

# Query across schemas
result = conn.execute("""
    SELECT COUNT(*) FROM network.providers 
    WHERE practice_state = 'CA'
""").fetchone()

print(f"California providers: {result[0]:,}")
```

### Schema Organization

Query tables using schema-qualified names:

```sql
-- Main schema (entities)
SELECT * FROM patients LIMIT 10;
SELECT * FROM main.encounters WHERE patient_id = 'P001';

-- Population schema (demographics)
SELECT * FROM population.svi_county WHERE st_abbr = 'CA';
SELECT * FROM population.places_county WHERE obesity_rate > 30;

-- Network schema (providers)
SELECT * FROM network.providers WHERE taxonomy_1 LIKE '%Cardiology%';
SELECT * FROM network.facilities WHERE state = 'TX';

-- Cross-schema joins
SELECT 
    p.st_abbr,
    COUNT(DISTINCT n.npi) as provider_count
FROM population.svi_county p
LEFT JOIN network.providers n ON n.practice_state = p.st_abbr
GROUP BY p.st_abbr;
```

### Database Utilities

Test database connection:
```bash
python test_mcp_connection.py
```

Run database queries:
```python
from healthsim.db import get_connection

conn = get_connection()

# List all tables
tables = conn.execute("""
    SELECT table_schema, table_name, 
           (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = t.table_schema) as schema_tables
    FROM information_schema.tables t
    WHERE table_schema IN ('main', 'population', 'network')
    ORDER BY table_schema, table_name
""").fetchall()

for schema, table, count in tables:
    print(f"{schema}.{table}")
```

---

## Claude Integration

HealthSim is designed for use with Claude Desktop or Claude Code.

### Option 1: Claude Desktop (Recommended)

Add HealthSim to a Claude Project:

1. Open Claude Desktop
2. Create a new Project (or use existing)
3. Go to Project Settings → Project knowledge
4. Add `healthsim-workspace` directory

**Or** configure as MCP server in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "healthsim": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/absolute/path/to/healthsim-workspace"
      ]
    },
    "healthsim-mcp": {
      "command": "/path/to/python",
      "args": [
        "/absolute/path/to/healthsim-workspace/packages/mcp-server/healthsim_mcp.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/healthsim-workspace/packages/core/src:/absolute/path/to/healthsim-workspace/packages/mcp-server"
      }
    }
  }
}
```

### Option 2: Claude Code

```bash
cd healthsim-workspace
claude
```

### Initial Test

Try these prompts in Claude:

```
Generate 3 diabetic patients in California with varying A1C levels
```

```
Show me provider statistics for Texas from the network schema
```

```
Query the population schema for counties with high obesity rates
```

---

## Managed Agent Infrastructure (Cloud Deployment)

To deploy HealthSim as a cloud-hosted Managed Agent, you need three additional services alongside the local setup above. The local setup remains your development environment — these services are deployment targets.

### Railway (MCP Server Hosting)

Railway hosts the HealthSim MCP server as an HTTP service that the Managed Agent calls.

```bash
# Install Railway CLI
brew install railway

# Login
railway login

# Deploy (from project root — uses the Dockerfile)
railway up
```

Set these environment variables in the Railway dashboard:
- `MCP_TRANSPORT=http`
- `MCP_PORT=8001`
- `HEALTHSIM_MCP_TOKEN` — a shared secret (generate with `openssl rand -hex 32`)
- `MOTHERDUCK_TOKEN` — your MotherDuck access token

### MotherDuck (Cloud DuckDB)

MotherDuck hosts the reference data (NPPES providers, CDC PLACES, SVI) and generated cohort data.

1. Create an account at [motherduck.com](https://motherduck.com)
2. Go to Settings → Access Tokens → Create Token
3. Add the token to `.env` as `MOTHERDUCK_TOKEN`
4. Run the migration script:

```bash
source .env
.venv/bin/python scripts/migrate_to_motherduck.py --full
.venv/bin/python scripts/migrate_to_motherduck.py --verify
```

### Anthropic Platform (Agent Runtime)

1. Get an API key from [platform.claude.com/settings/keys](https://platform.claude.com/settings/keys)
2. Add to `.env` as `ANTHROPIC_API_KEY`
3. Run the deploy scripts:

```bash
source .env
.venv/bin/python deploy/push-skills.py --all
.venv/bin/python deploy/push-agent.py
.venv/bin/python deploy/push-environment.py
```

4. Test with the CLI: `./deploy/run.sh`
5. Or test via the Console UI at [platform.claude.com](https://platform.claude.com) → Managed Agents

For the full operations guide, see [docs/MANAGED-AGENT-GUIDE.md](docs/MANAGED-AGENT-GUIDE.md).

---

## Verification

### 1. Check Python Installation

```bash
cd healthsim-workspace
source .venv/bin/activate  # If not already activated

python -c "
from healthsim.db import get_connection, DEFAULT_DB_PATH
import duckdb

print('✓ Python environment working')
print(f'✓ DuckDB version: {duckdb.__version__}')
print(f'✓ Database path: {DEFAULT_DB_PATH}')
print(f'✓ Database exists: {DEFAULT_DB_PATH.exists()}')

conn = get_connection()
result = conn.execute('SELECT COUNT(*) FROM information_schema.tables').fetchone()
print(f'✓ Database connection: {result[0]} tables found')
"
```

### 2. Run Connection Test

```bash
python test_mcp_connection.py
```

Expected output:
```
================================================================================
Testing MCP Server Database Connection
================================================================================

Database Path: /path/to/healthsim.duckdb
Database Exists: True
Database Size: 1.65 GB

✓ Connection successful

[... schema details ...]

✓ Cross-schema JOIN successful
✓ Database connection working
✓ All three schemas accessible (main, population, network)
✓ Cross-schema JOINs functional
✓ MCP server ready for use
```

### 3. Test Data Generation

In Claude, try:

```
Generate a patient with type 2 diabetes
```

You should see a JSON patient record with realistic clinical data.

---

## Troubleshooting

### Database File Issues

**Problem:** `healthsim.duckdb` not found

```bash
# Check if file exists
ls -lh healthsim.duckdb

# If missing, ensure Git LFS downloaded it
git lfs ls-files
git lfs pull --include="healthsim.duckdb"
```

**Problem:** Database file is locked

```bash
# Check for other Python processes
ps aux | grep python

# Kill any healthsim processes
pkill -f healthsim

# Verify no .wal or .lock files
ls healthsim.duckdb*
# Clean up if needed:
rm healthsim.duckdb.wal healthsim.duckdb.lock
```

**Problem:** Permission denied

```bash
chmod 644 healthsim.duckdb
```

### Python Environment Issues

**Problem:** `ModuleNotFoundError: No module named 'healthsim'`

```bash
# Ensure you're in virtual environment
which python
# Should show: /path/to/healthsim-workspace/.venv/bin/python

# Reinstall package
cd packages/core
pip install -e .
```

**Problem:** Wrong Python version

```bash
# Check version
python --version

# Use Python 3.10+ explicitly
python3.10 -m venv .venv
```

### Git LFS Issues

**Problem:** Database is tiny (pointer file)

```bash
# Check if it's a pointer
cat healthsim.duckdb | head -3
# If you see "version https://git-lfs.github.com", it's a pointer

# Fix:
git lfs install
git lfs pull
```

**Problem:** Git LFS bandwidth exceeded

Download database separately:
1. Go to GitHub releases
2. Download `healthsim.duckdb` attachment
3. Place in workspace root

### Performance Issues

**Problem:** Queries are slow

```bash
# Check database size
ls -lh healthsim.duckdb

# Vacuum database
python -c "
from healthsim.db import get_connection
conn = get_connection()
conn.execute('VACUUM')
print('✓ Database vacuumed')
"
```

**Problem:** Out of memory

DuckDB can use significant memory for large queries. Try:
```python
conn.execute("SET memory_limit='4GB'")
conn.execute("SET temp_directory='/path/to/large/disk'")
```

---

## Next Steps

After successful installation:

1. **Read [Hello HealthSim](hello-healthsim/README.md)** - Quick start guide
2. **Try [Examples](hello-healthsim/examples/)** - Sample generation requests
3. **Review [SKILL.md](SKILL.md)** - Master skill reference
4. **Explore [Architecture Docs](docs/)** - System design and patterns

---

## Support

- **Issues:** https://github.com/mark64oswald/healthsim-workspace/issues
- **Discussions:** https://github.com/mark64oswald/healthsim-workspace/discussions
- **Documentation:** [docs/](docs/)

---

**Installation complete!** You're ready to generate synthetic healthcare data with HealthSim.
