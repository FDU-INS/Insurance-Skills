"""MCP Server for TrialSim state management capabilities.

This module implements a Model Context Protocol (MCP) server that exposes
cohort save/load tools for workspace persistence.

Tools:
- save_cohort: Save workspace to a named cohort
- load_cohort: Load a cohort into workspace
- list_saved_cohorts: List saved cohorts with filtering
- delete_cohort: Delete a saved cohort
- workspace_summary: Get current workspace state
"""

import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trialsim.mcp.state")

# Initialize MCP server
app = Server("trialsim-state")


def format_cohort_saved(cohort: Any) -> str:
    """Format cohort save confirmation."""
    lines = [
        f'**Saved: "{cohort.metadata.name}"**',
        "",
        "**Cohort Summary:**",
        f"- Cohort ID: `{cohort.metadata.workspace_id}`",
        f"- Subjects: {cohort.get_entity_count('subjects')}",
        f"- Visits: {cohort.get_entity_count('visits')}",
        f"- Adverse Events: {cohort.get_entity_count('adverse_events')}",
        f"- Exposures: {cohort.get_entity_count('exposures')}",
        f"- Total entities: {cohort.get_entity_count()}",
    ]

    if cohort.metadata.description:
        lines.append(f"- Description: {cohort.metadata.description}")

    if cohort.metadata.tags:
        lines.append(f"- Tags: {', '.join(cohort.metadata.tags)}")

    lines.append("")
    lines.append(f'You can load this anytime with: `load "{cohort.metadata.name}"`')

    return "\n".join(lines)


def format_cohort_loaded(cohort: Any, summary: dict) -> str:
    """Format cohort load confirmation."""
    lines = [
        f'**Loaded: "{cohort.metadata.name}"**',
        "",
        f"- Subjects loaded: {summary.get('subjects_loaded', 0)}",
        f"- Visits loaded: {summary.get('visits_loaded', 0)}",
        f"- Total entities: {summary.get('total_entities', 0)}",
    ]

    lines.append("")
    lines.append("Ready to continue! What would you like to work on?")

    return "\n".join(lines)


def format_cohort_list(cohorts: list[dict]) -> str:
    """Format list of saved cohorts."""
    if not cohorts:
        return (
            "No saved cohorts found.\n\n"
            "Create some subjects and use `save_cohort` to save your work."
        )

    lines = ["**Your Saved Cohorts:**", ""]

    for s in cohorts:
        name = s["name"]
        created = s["created_at"][:10]  # Just the date
        subject_count = s.get("subject_count", 0)
        tags = ", ".join(s.get("tags", [])) if s.get("tags") else ""

        line = f"- **{name}** ({created}) - {subject_count} subjects"
        if tags:
            line += f" [tags: {tags}]"
        if s.get("description"):
            line += f"\n  _{s['description']}_"

        lines.append(line)

    lines.append("")
    lines.append("Use `load_cohort` with a name to restore a cohort.")

    return "\n".join(lines)


def format_cohort_deleted(info: dict) -> str:
    """Format cohort deletion confirmation."""
    return f"**Deleted:** \"{info['name']}\"\n- {info.get('subject_count', 0)} subjects removed"


def format_error(message: str) -> str:
    """Format error message."""
    return f"**Error:** {message}"


def format_workspace_summary(summary: dict) -> str:
    """Format workspace summary."""
    if summary.get("subject_count", 0) == 0:
        return (
            "**Workspace is empty**\n\n"
            "Start by generating subjects with `generate_subject` or `generate_subject_cohort`."
        )

    lines = [
        "**Current Workspace:**",
        "",
        f"- Subjects: {summary.get('subject_count', 0)}",
        f"- Visits: {summary.get('visit_count', 0)}",
        f"- Adverse Events: {summary.get('ae_count', 0)}",
        f"- Exposures: {summary.get('exposure_count', 0)}",
    ]

    if summary.get("protocols"):
        lines.append("")
        lines.append("**Protocols:**")
        for protocol in summary["protocols"]:
            lines.append(f"- {protocol}")

    return "\n".join(lines)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available state management tools."""
    return [
        Tool(
            name="save_cohort",
            description=(
                "Save the current workspace as a named cohort. "
                "Captures all subjects, visits, AEs, and exposures."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the saved cohort",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description",
                    },
                    "tags": {
                        "type": "array",
                        "description": "Optional tags for organization",
                        "items": {"type": "string"},
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="load_cohort",
            description="Load a previously saved cohort into the workspace.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of cohort to load",
                    },
                    "cohort_id": {
                        "type": "string",
                        "description": "Or cohort ID to load",
                    },
                },
            },
        ),
        Tool(
            name="list_saved_cohorts",
            description="List all saved cohorts with optional filtering.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "description": "Filter by tag",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number to return",
                        "default": 20,
                    },
                },
            },
        ),
        Tool(
            name="delete_cohort",
            description="Delete a saved cohort.",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "string",
                        "description": "ID of cohort to delete",
                    },
                },
                "required": ["cohort_id"],
            },
        ),
        Tool(
            name="workspace_summary",
            description="Get a summary of the current workspace state.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "save_cohort":
            return await handle_save_cohort(arguments)
        elif name == "load_cohort":
            return await handle_load_cohort(arguments)
        elif name == "list_saved_cohorts":
            return await handle_list_cohorts(arguments)
        elif name == "delete_cohort":
            return await handle_delete_cohort(arguments)
        elif name == "workspace_summary":
            return await handle_workspace_summary(arguments)
        else:
            return [TextContent(type="text", text=format_error(f"Unknown tool: {name}"))]
    except Exception as e:
        logger.exception(f"Error in tool {name}")
        return [TextContent(type="text", text=format_error(str(e)))]


async def handle_save_cohort(arguments: dict) -> list[TextContent]:
    """Handle save_cohort tool call."""
    # Placeholder - would integrate with actual state management
    name = arguments.get("name")
    if not name:
        return [TextContent(type="text", text=format_error("Cohort name is required"))]
    
    # TODO: Integrate with TrialSim session manager when implemented
    return [TextContent(
        type="text",
        text=f"**Note:** State management for TrialSim is not yet fully implemented.\n\n"
             f"Cohort '{name}' would be saved here."
    )]


async def handle_load_cohort(arguments: dict) -> list[TextContent]:
    """Handle load_cohort tool call."""
    name = arguments.get("name")
    cohort_id = arguments.get("cohort_id")
    
    if not name and not cohort_id:
        return [TextContent(type="text", text=format_error("Either name or cohort_id is required"))]
    
    # TODO: Integrate with TrialSim session manager when implemented
    return [TextContent(
        type="text",
        text=f"**Note:** State management for TrialSim is not yet fully implemented.\n\n"
             f"Cohort '{name or cohort_id}' would be loaded here."
    )]


async def handle_list_cohorts(arguments: dict) -> list[TextContent]:
    """Handle list_saved_cohorts tool call."""
    # TODO: Integrate with actual state management
    return [TextContent(
        type="text",
        text="**Note:** State management for TrialSim is not yet fully implemented.\n\n"
             "No saved cohorts available."
    )]


async def handle_delete_cohort(arguments: dict) -> list[TextContent]:
    """Handle delete_cohort tool call."""
    cohort_id = arguments.get("cohort_id")
    if not cohort_id:
        return [TextContent(type="text", text=format_error("Cohort ID is required"))]
    
    # TODO: Integrate with actual state management
    return [TextContent(
        type="text",
        text=f"**Note:** State management for TrialSim is not yet fully implemented.\n\n"
             f"Cohort '{cohort_id}' would be deleted here."
    )]


async def handle_workspace_summary(arguments: dict) -> list[TextContent]:
    """Handle workspace_summary tool call."""
    # TODO: Integrate with actual state management
    summary = {
        "subject_count": 0,
        "visit_count": 0,
        "ae_count": 0,
        "exposure_count": 0,
    }
    return [TextContent(type="text", text=format_workspace_summary(summary))]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
