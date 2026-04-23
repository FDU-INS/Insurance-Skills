# MCP Development Guide

Guide to developing MCP servers and tools for HealthSim products.

## MCP Overview

Model Context Protocol (MCP) enables Claude to call HealthSim functionality as tools. HealthSim products typically provide three MCP servers:

1. **Generation Server** - Entity generation tools
2. **Export Server** - Format export tools
3. **Validation Server** - Quality assurance tools

## Server Architecture

Each MCP server follows this pattern:

```python
from mcp.server import Server
from mcp.types import TextContent, Tool

server = Server("healthsim-generation")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="generate_entity",
            description="Generate a single synthetic entity",
            inputSchema={
                "type": "object",
                "properties": {
                    "age_range": {"type": "array"},
                    "gender": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "generate_entity":
        return await generate_entity(arguments)
```

## Adding a New Tool

### Example: Add `modify_entity` Tool

**1. Define Tool Schema:**

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools
        Tool(
            name="modify_entity",
            description="Modify an existing entity's demographics or data",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_id": {
                        "type": "string",
                        "description": "Entity ID to modify"
                    },
                    "modifications": {
                        "type": "object",
                        "description": "Fields to modify",
                        "properties": {
                            "age": {"type": "integer"},
                            "add_field": {"type": "string"}
                        }
                    }
                },
                "required": ["entity_id", "modifications"]
            }
        )
    ]
```

**2. Implement Tool Handler:**

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "modify_entity":
        entity_id = arguments["entity_id"]
        mods = arguments["modifications"]

        # Get entity from session state
        entity = get_entity_from_session(entity_id)

        # Apply modifications
        if "age" in mods:
            # Recalculate birth_date for new age
            today = date.today()
            entity.birth_date = date(today.year - mods["age"], today.month, today.day)

        if "add_field" in mods:
            # Add new field value
            entity.custom_field = mods["add_field"]

        # Save updated entity
        save_entity_to_session(entity)

        return [TextContent(
            type="text",
            text=f"Modified entity {entity_id}: {', '.join(mods.keys())}"
        )]
```

**3. Add Session State Management:**

```python
# Global session state (in-memory for development)
_session_entities: dict[str, Entity] = {}

def save_entity_to_session(entity: Entity):
    _session_entities[entity.id] = entity

def get_entity_from_session(entity_id: str) -> Entity:
    if entity_id not in _session_entities:
        raise ValueError(f"Entity {entity_id} not found")
    return _session_entities[entity_id]
```

**4. Test Tool:**

```python
# tests/mcp/test_generation_server.py

import pytest
from mcp.client import ClientSession

@pytest.mark.asyncio
async def test_modify_entity_tool():
    """Test modify_entity tool."""
    async with ClientSession() as client:
        # First generate an entity
        result = await client.call_tool(
            "generate_entity",
            {"age_range": [60, 70]}
        )

        entity_id = extract_id_from_result(result)

        # Now modify the entity
        result = await client.call_tool(
            "modify_entity",
            {
                "entity_id": entity_id,
                "modifications": {
                    "age": 75,
                    "add_field": "new value"
                }
            }
        )

        assert "Modified entity" in result[0].text
```

## Tool Best Practices

### 1. Clear Tool Names

❌ **Bad:**
```python
Tool(name="gen_ent")  # Cryptic
```

✅ **Good:**
```python
Tool(name="generate_entity")  # Clear, action-verb
```

### 2. Tool Selection Guidance in Descriptions

When multiple tools can handle similar operations, include explicit guidance in the docstrings about when to use each tool:

```python
@mcp.tool()
def save_cohort(...):
    """Save a cohort to the database.
    
    ⚠️  USE healthsim_add_entities INSTEAD when:
    - Total entity count exceeds 50 (to avoid token limit truncation)
    - Building cohorts incrementally across multiple calls
    
    This tool REPLACES ALL entities. Only use for small, complete datasets.
    """

@mcp.tool()
def add_entities(...):
    """Add entities incrementally (RECOMMENDED for most use cases).
    
    ✅ USE THIS TOOL when:
    - Total entity count exceeds 50
    - Building cohorts in batches
    - Adding to existing cohorts
    """
```

This ensures Claude automatically selects the right tool based on the use case.

### 3. Descriptive Input Schemas

❌ **Bad:**
```python
inputSchema={
    "type": "object",
    "properties": {"params": {"type": "object"}}  # Vague
}
```

✅ **Good:**
```python
inputSchema={
    "type": "object",
    "properties": {
        "age_range": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "Min and max age [min, max]"
        },
        "gender": {
            "type": "string",
            "enum": ["M", "F", "O"],
            "description": "Gender"
        }
    }
}
```

### 4. Helpful Error Messages

```python
try:
    entity = generate_entity(arguments)
except ValueError as e:
    return [TextContent(
        type="text",
        text=f"Error generating entity: {str(e)}\n\nTip: Check that age_range is [min, max] with min < max"
    )]
```

### 5. Return Structured Output

```python
return [TextContent(
    type="text",
    text=f"""Generated Entity:
- Name: {entity.full_name}
- ID: {entity.id}
- Age: {entity.age}
- Gender: {entity.gender}
"""
)]
```

## Testing MCP Servers

### Manual Testing

```bash
# Start server manually
python -m product.mcp.generation_server

# Test with mcp-client
mcp-client \
  --server "python -m product.mcp.generation_server" \
  --tool generate_entity \
  --args '{"age_range": [60, 70]}'
```

### Integration Testing

```python
import pytest
from mcp.client import ClientSession

@pytest.mark.asyncio
async def test_generation_workflow():
    """Test complete generation workflow."""
    async with ClientSession() as client:
        # Generate entity
        result = await client.call_tool("generate_entity", {})
        assert "Generated" in result[0].text

        # Export to format
        result = await client.call_tool("export_format", {})
        assert "Exported" in result[0].text

        # Validate
        result = await client.call_tool("validate_entities", {})
        assert "Validation" in result[0].text
```

## Debugging

### Enable Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.debug(f"Tool called: {name} with {arguments}")
    # ... implementation
```

### Test in Claude Desktop

1. Add server to `claude_desktop_config.json`
2. Restart Claude Desktop
3. Check logs: `~/Library/Logs/Claude/mcp-server-*.log`

## Deployment

### For Claude Desktop

Users configure in `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "product-generation": {
      "command": "/path/to/.venv/bin/python",
      "args": ["-m", "product.mcp.generation_server"],
      "cwd": "/path/to/product"
    }
  }
}
```

### For Claude Code

Automatic discovery via `.claude/mcp-config.json`:

```json
{
  "mcpServers": {
    "product-generation": {
      "command": "python",
      "args": ["-m", "product.mcp.generation_server"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## See Also

- [MCP Configuration Guide](configuration.md) - User setup
- [MCP Integration Guide](integration-guide.md) - Integration overview
- [Extension Philosophy](../extensions/philosophy.md) - Adding capabilities
- [MCP Tools Extension Guide](../extensions/mcp-tools.md) - Adding MCP tools
