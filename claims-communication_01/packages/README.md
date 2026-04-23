# HealthSim Python Packages

This directory contains Python packages that provide supporting infrastructure for HealthSim.

## What's Here

| Package | Purpose | Status |
|---------|---------|--------|
| `core/` | Shared library: state management, validation, dimensional output, format utilities | Active |
| `patientsim/` | PatientSim MCP server and utilities | Active |
| `membersim/` | MemberSim MCP server and utilities | Active |
| `rxmembersim/` | RxMemberSim MCP server and utilities | Active |

## Package Contents

Each product package contains:
- `pyproject.toml` - Package configuration
- `src/{package}/` - Python source code
- `tests/` - Test suite
- `CLAUDE.md` - Product-specific Claude instructions

The `core/` package provides shared infrastructure:
- **State Management** - Workspace and session handling
- **Validation Framework** - Data validation rules
- **Dimensional Output** - Star schema transformers for analytics
- **Format Utilities** - Helpers for output format generation

## Important Note

These packages are **supporting infrastructure** for MCP servers and utilities. The primary HealthSim interface is through **Skills** (in `/skills/`), which Claude uses to generate synthetic data via conversation.

**Skills** = Domain knowledge and generation patterns (what users interact with)  
**Packages** = Python infrastructure for I/O operations (MCP servers, data loading)

## Development

To work on a package:

```bash
cd packages/{package}
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## See Also

- [Architecture Guide](../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) - Overall architecture
- [Development Process](../docs/HEALTHSIM-DEVELOPMENT-PROCESS.md) - Development workflow
- [Skills Directory](../skills/) - Domain knowledge and scenarios
