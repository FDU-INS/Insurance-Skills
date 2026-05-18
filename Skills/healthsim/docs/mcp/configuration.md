# MCP Server Configuration

This guide explains how to set up HealthSim MCP servers for use with Claude Desktop, Claude Code, and other MCP-compatible clients.

## Overview

HealthSim provides MCP servers that expose capabilities as tools for Claude:

### Core Infrastructure

1. **HealthSim MCP Server** (`healthsim-mcp`) - **REQUIRED** for DuckDB access
   - Single connection holder for the HealthSim DuckDB database
   - Solves file locking issues that prevent concurrent access
   - Provides cohort management and SQL query tools

### Product Servers (Optional)

2. **Generation Server** - Create synthetic patients, members, or prescriptions
3. **Export Server** - Transform data to healthcare formats (FHIR, HL7v2, X12, NCPDP, MIMIC)
4. **Validation Server** - Validate clinical plausibility and data integrity

---

## HealthSim MCP Server (Core)

The HealthSim MCP server is the **single connection holder** for the DuckDB database. This architecture solves the file locking issue where DuckDB allows only one write connection at a time.

### Why This Server?

DuckDB uses file-level locking. If multiple processes try to access the database:
- First process gets the lock ✅
- Subsequent processes are blocked ❌

The HealthSim MCP server maintains the single connection and exposes database operations as MCP tools.

### Installation

```bash
# Install MCP package
pip install mcp pydantic

# Or use anaconda if that's your Python environment
/Users/markoswald/anaconda3/bin/pip install mcp pydantic
```

### Configuration (Claude Desktop)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "healthsim-mcp": {
      "command": "/Users/markoswald/anaconda3/bin/python",
      "args": [
        "/Users/markoswald/Developer/projects/healthsim-workspace/packages/mcp-server/healthsim_mcp.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src:/Users/markoswald/Developer/projects/healthsim-workspace/packages/mcp-server"
      }
    }
  }
}
```

**Important**: Adjust the Python path to match your environment. Find it with:
```bash
which python3
# or
/Users/markoswald/anaconda3/bin/python --version
```

### Available Tools

| Tool | Description | Read-Only |
|------|-------------|:---------:|
| `healthsim_list_cohorts` | List all saved cohorts | ✅ |
| `healthsim_load_cohort` | Load a cohort by name/ID | ✅ |
| `healthsim_save_cohort` | Save entities as a cohort | ❌ |
| `healthsim_delete_cohort` | Delete a cohort (requires confirm=True) | ❌ |
| `healthsim_get_cohort_summary` | Get token-efficient cohort summary | ✅ |
| `healthsim_query` | Execute read-only SQL queries | ✅ |
| `healthsim_query_reference` | Query PopulationSim reference data | ✅ |
| `healthsim_tables` | List all database tables | ✅ |

### Reference Data Tables

| Table | Rows | Description |
|-------|------|-------------|
| `ref_places_county` | 3,143 | CDC PLACES county-level health indicators |
| `ref_places_tract` | 83,522 | CDC PLACES tract-level health indicators |
| `ref_svi_county` | 3,144 | Social Vulnerability Index by county |
| `ref_svi_tract` | 84,120 | Social Vulnerability Index by tract |
| `ref_adi_blockgroup` | 242,336 | Area Deprivation Index by block group |

### Usage Examples

```
# List cohorts
Use healthsim_list_cohorts

# Query reference data
Use healthsim_query_reference with table="places_county" and state="CA"

# Run custom SQL
Use healthsim_query with sql="SELECT countyname, obesity_crudeprev FROM ref_places_county WHERE stateabbr = 'TX' ORDER BY obesity_crudeprev DESC LIMIT 10"

# Save a cohort
Use healthsim_save_cohort with:
- name: "my-cohort"
- entities: {"patients": [...], "encounters": [...]}
- description: "Test cohort"
- tags: ["test", "demo"]
```

### Replacing Previous Configuration

If you previously used `healthsim-duckdb` (mcp-server-motherduck), **remove it**:

```json
// REMOVE THIS:
"healthsim-duckdb": {
  "command": "uvx",
  "args": ["mcp-server-motherduck", "--db-path", "..."]
}
```

The new `healthsim-mcp` server provides the same query capability plus cohort management.

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Product installed: `pip install -e .`
- Virtual environment activated (recommended)

### Configuration File

Each product includes a pre-configured MCP configuration file at `.claude/mcp-config.json`:

```json
{
  "mcpServers": {
    "patientsim-generation": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "description": "Generate synthetic patients and cohorts",
      "cwd": "${workspaceFolder}"
    },
    "patientsim-export": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.export_server"],
      "description": "Export patients to healthcare data formats",
      "cwd": "${workspaceFolder}"
    },
    "patientsim-validation": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.validation_server"],
      "description": "Validate patient data for clinical plausibility",
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## Setup for Claude Desktop

### macOS/Linux

1. **Locate Claude Desktop Config**:
   ```bash
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json

   # Linux
   ~/.config/Claude/claude_desktop_config.json
   ```

2. **Add Server Configurations**:
   ```bash
   # Copy the server configurations
   cat .claude/mcp-config.json
   ```

3. **Edit claude_desktop_config.json**:
   ```json
   {
     "mcpServers": {
       "patientsim-generation": {
         "command": "/path/to/your/venv/bin/python",
         "args": ["-m", "patientsim.mcp.generation_server"],
         "cwd": "/path/to/patientsim"
       },
       "patientsim-export": {
         "command": "/path/to/your/venv/bin/python",
         "args": ["-m", "patientsim.mcp.export_server"],
         "cwd": "/path/to/patientsim"
       },
       "patientsim-validation": {
         "command": "/path/to/your/venv/bin/python",
         "args": ["-m", "patientsim.mcp.validation_server"],
         "cwd": "/path/to/patientsim"
       }
     }
   }
   ```

4. **Replace Paths**:
   - Replace `/path/to/your/venv/bin/python` with your virtual environment's Python path
   - Replace `/path/to/patientsim` with your product directory path

5. **Restart Claude Desktop**:
   - Quit Claude Desktop completely
   - Relaunch Claude Desktop
   - MCP servers will start automatically

### Windows

1. **Locate Claude Desktop Config**:
   ```powershell
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Edit Configuration**:
   ```json
   {
     "mcpServers": {
       "patientsim-generation": {
         "command": "C:\\path\\to\\venv\\Scripts\\python.exe",
         "args": ["-m", "patientsim.mcp.generation_server"],
         "cwd": "C:\\path\\to\\patientsim"
       }
     }
   }
   ```

3. **Restart Claude Desktop**

## Setup for Claude Code

Claude Code automatically discovers MCP configuration in `.claude/mcp-config.json` within your workspace.

### Automatic Setup

1. **Open Project in Claude Code**:
   ```bash
   code /path/to/patientsim
   ```

2. **Verify Configuration**:
   - Claude Code reads `.claude/mcp-config.json`
   - Servers start automatically when needed

### Manual Path Configuration

If using a specific Python interpreter:

1. **Edit `.claude/mcp-config.json`**:
   ```json
   {
     "mcpServers": {
       "patientsim-generation": {
         "command": "/absolute/path/to/venv/bin/python",
         "args": ["-m", "patientsim.mcp.generation_server"],
         "cwd": "${workspaceFolder}"
       }
     }
   }
   ```

2. **Use `${workspaceFolder}` variable** - Claude Code expands this automatically

## Available Tools

### Generation Server Tools

**Patient/Member Generation:**
- **`generate_patient`** / **`generate_member`** - Generate a single entity
- **`generate_cohort`** - Generate multiple entities
- **`list_cohorts`** - Show available clinical cohorts
- **`describe_cohort`** - Get cohort details
- **`modify_patient`** - Modify existing entity
- **`get_patient_details`** - View entity information

**State Management (Save/Load Cohorts):**
- **`save_cohort`** - Save current workspace to a named cohort
- **`load_cohort`** - Load a saved cohort
- **`list_saved_cohorts`** - List all saved cohorts
- **`delete_cohort`** - Delete a saved cohort
- **`workspace_summary`** - View current workspace state

### Export Server Tools

- **`export_fhir`** - Export to FHIR R4 Bundle
- **`export_hl7v2`** - Export to HL7v2 messages (ADT^A01, ORU^R01)
- **`export_x12`** - Export to X12 837/835 format (claims)
- **`export_ncpdp`** - Export to NCPDP D.0 format (pharmacy)
- **`export_mimic`** - Export to MIMIC-III CSV/Parquet format
- **`export_json`** - Export to native JSON format
- **`list_export_formats`** - Show available export formats

### Validation Server Tools

- **`validate_patients`** - Validate clinical plausibility
- **`validate_for_export`** - Validate for specific export format
- **`fix_validation_issues`** - Auto-fix common validation issues
- **`explain_validation_rule`** - Get explanation for validation rules

## Testing MCP Servers

### Manual Testing

Test each server independently before configuring Claude:

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Test generation server
python -m patientsim.mcp.generation_server
# Should output: "INFO:patientsim.mcp:Starting PatientSim MCP Generation Server"
# Press Ctrl+C to stop

# Test export server
python -m patientsim.mcp.export_server
# Should output: "INFO:patientsim.mcp.export:Starting PatientSim MCP Export Server"

# Test validation server
python -m patientsim.mcp.validation_server
# Should output: "INFO:patientsim.mcp.validation:Starting PatientSim MCP Validation Server"
```

### Testing with MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a debugging tool for MCP servers:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Test a server
mcp-inspector python -m patientsim.mcp.generation_server
```

This opens a web UI showing:
- Available tools
- Tool schemas
- Request/response inspection
- Error debugging

## Troubleshooting

### Servers Not Appearing in Claude

**Symptom**: MCP tools don't appear in Claude's tool list

**Solutions**:
1. **Verify Python path** - Use absolute path to Python interpreter:
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```

2. **Check working directory** - Ensure `cwd` points to product root:
   ```json
   {
     "cwd": "/absolute/path/to/patientsim"
   }
   ```

3. **Restart Claude Desktop** - Completely quit and relaunch

4. **Check Claude logs**:
   ```bash
   # macOS
   ~/Library/Logs/Claude/

   # Linux
   ~/.config/Claude/logs/

   # Windows
   %APPDATA%\Claude\logs\
   ```

### Import Errors

**Symptom**: Server starts but shows `ModuleNotFoundError`

**Solutions**:
1. **Install product**:
   ```bash
   pip install -e .
   ```

2. **Verify installation**:
   ```bash
   python -c "import patientsim; print(patientsim.__file__)"
   ```

3. **Use correct Python interpreter** - Ensure MCP config uses the same Python where product is installed

### Server Crashes

**Symptom**: MCP server starts but crashes immediately

**Solutions**:
1. **Check dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

2. **View server logs** - Run server manually to see error messages

3. **Check Python version**:
   ```bash
   python --version  # Should be 3.10+
   ```

## Advanced Configuration

### Environment Variables

Pass environment variables to MCP servers:

```json
{
  "mcpServers": {
    "patientsim-generation": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "env": {
        "PATIENTSIM_LOG_LEVEL": "DEBUG",
        "PATIENTSIM_OUTPUT_DIR": "/custom/export/path"
      }
    }
  }
}
```

### Multiple Instances

Run separate instances for different projects:

```json
{
  "mcpServers": {
    "patientsim-dev": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "cwd": "/path/to/dev/patientsim"
    },
    "patientsim-prod": {
      "command": "python",
      "args": ["-m", "patientsim.mcp.generation_server"],
      "cwd": "/path/to/prod/patientsim"
    }
  }
}
```

## Session Management

MCP servers share session state:
- **Generation server** creates entities and stores them in session
- **Export server** exports entities from the same session
- **Validation server** validates entities in the session

**Example workflow**:
```text
1. User: "Generate 5 diabetic patients"
   → generation_server creates patients, stores in session

2. User: "Validate them"
   → validation_server reads patients from session, validates

3. User: "Export to FHIR"
   → export_server reads patients from session, exports to FHIR

4. User: "Clear the session"
   → Session cleared, start fresh
```

## Security Considerations

### Data Privacy

- **All data is synthetic** - MCP servers generate fictional data only
- **No PHI** - Servers refuse requests that could create PHI lookalikes
- **Local execution** - Servers run locally, no cloud uploads

### File System Access

MCP servers can:
- ✅ Write exports to designated output directory
- ✅ Read cohort skills from `skills/` directory
- ❌ **Cannot** read arbitrary files outside product directory
- ❌ **Cannot** modify source code

### Network Access

- ❌ MCP servers do **not** make network requests
- ❌ MCP servers do **not** upload data
- ✅ All processing is local-only

## See Also

- [MCP Integration Guide](integration-guide.md)
- [MCP Development Guide](development-guide.md)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
