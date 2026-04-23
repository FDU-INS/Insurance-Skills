# HealthSim MCP Server

Model Context Protocol (MCP) server for HealthSim profile and journey management.

## Overview

This MCP server allows Claude (or other MCP-compatible AI assistants) to manage HealthSim profiles and journeys through conversational tools rather than requiring users to write JSON directly.

## Tools

### Profile Management

| Tool | Description |
|------|-------------|
| `build_profile` | Create a profile specification from parameters |
| `save_profile` | Save a profile to persistent storage (`~/.healthsim/profiles/`) |
| `load_profile` | Load a profile by name, ID, or from a template |
| `list_profiles` | List all saved profiles |
| `list_profile_templates` | List built-in profile templates |
| `get_profile_template` | Get details of a specific profile template |
| `execute_profile` | Execute a profile to generate entities |

### Journey Management

| Tool | Description |
|------|-------------|
| `build_journey` | Create a journey specification from parameters |
| `save_journey` | Save a journey to persistent storage (`~/.healthsim/journeys/`) |
| `load_journey` | Load a journey by name, ID, or from a template |
| `list_journeys` | List all saved journeys |
| `list_journey_templates` | List built-in journey templates |
| `get_journey_template` | Get details of a specific journey template |
| `execute_journey` | Execute a journey to generate event timelines |

## Usage

### Running the Server

```bash
# Using Python module
python -m healthsim.mcp.profile_server

# Or if installed
healthsim-mcp-profiles
```

### MCP Configuration

Add to your MCP settings (e.g., Claude desktop app):

```json
{
  "mcpServers": {
    "healthsim-profiles": {
      "command": "python",
      "args": ["-m", "healthsim.mcp.profile_server"],
      "env": {}
    }
  }
}
```

## Example Conversations

### Profile Creation

**User:** Create a Medicare diabetic profile with 500 patients, ages 65-85.

**Claude (using tools):**
1. Calls `build_profile` with:
   - name: "Medicare Diabetic Cohort"
   - count: 500
   - age_mean: 75
   - age_min: 65
   - age_max: 85
   - primary_condition_code: "E11"
   - coverage_type: "medicare"

2. Returns formatted profile summary

**User:** Save that and generate the patients.

**Claude (using tools):**
1. Calls `save_profile` with the JSON
2. Calls `execute_profile` to generate 500 patients
3. Returns execution summary

### Journey Creation

**User:** Create a diabetes management journey with quarterly visits and A1C labs.

**Claude (using tools):**
1. Calls `build_journey` with:
   - name: "Diabetes Quarterly Management"
   - duration_days: 365
   - events: [quarterly office visits, A1C labs, medication reviews]

2. Returns formatted journey summary

**User:** Execute that journey for patient-123 starting January 1st.

**Claude (using tools):**
1. Calls `execute_journey` with:
   - journey_name: "Diabetes Quarterly Management"
   - entity_id: "patient-123"
   - start_date: "2024-01-01"
2. Returns timeline of scheduled events

## Storage

Profiles and journeys are stored as JSON files in:
- `~/.healthsim/profiles/` - Saved profiles
- `~/.healthsim/journeys/` - Saved journeys

## Dependencies

Requires the `mcp` package:

```bash
pip install healthsim-core[mcp-server]
```

## Development

```bash
# Install dev dependencies
pip install healthsim-core[dev,mcp-server]

# Run tests
pytest packages/core/tests/mcp/
```

## See Also

- [Profile Schema](../../../../../docs/api/profile-schema.md) - Profile specification format
- [Journey Engine](../../../../../docs/api/journey-engine.md) - Journey specification format
- [Generative Framework Guide](../../../../../docs/guides/generative-framework.md) - Overview
