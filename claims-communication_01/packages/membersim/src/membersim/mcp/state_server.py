"""MCP Server for MemberSim state management capabilities.

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

from membersim.mcp.session import MemberSessionManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("membersim.mcp.state")

# Initialize MCP server
app = Server("membersim-state")

# Session manager - this would be shared with generation server in practice
# For standalone operation, we create our own instance
session_manager = MemberSessionManager()


def format_cohort_saved(cohort: Any) -> str:
    """Format cohort save confirmation."""
    lines = [
        f'**Saved: "{cohort.metadata.name}"**',
        "",
        "**Cohort Summary:**",
        f"- Cohort ID: `{cohort.metadata.workspace_id}`",
        f"- Members: {cohort.get_entity_count('members')}",
        f"- Total entities: {cohort.get_entity_count()}",
    ]

    if cohort.metadata.description:
        lines.append(f"- Description: {cohort.metadata.description}")

    if cohort.metadata.tags:
        lines.append(f"- Tags: {', '.join(cohort.metadata.tags)}")

    # Provenance breakdown
    prov = cohort.provenance_summary
    if prov.by_source_type:
        lines.append("")
        lines.append("**Provenance:**")
        if prov.by_source_type.get("generated", 0) > 0:
            lines.append(f"- Generated: {prov.by_source_type['generated']} entities")
        if prov.by_source_type.get("loaded", 0) > 0:
            lines.append(f"- Loaded: {prov.by_source_type['loaded']} entities")
        if prov.by_source_type.get("derived", 0) > 0:
            lines.append(f"- Derived: {prov.by_source_type['derived']} entities")

    if prov.skills_used:
        lines.append(f"- Skills used: {', '.join(prov.skills_used)}")

    lines.append("")
    lines.append(f'You can load this anytime with: `load "{cohort.metadata.name}"`')

    return "\n".join(lines)


def format_cohort_loaded(cohort: Any, summary: dict) -> str:
    """Format cohort load confirmation."""
    lines = [
        f'**Loaded: "{cohort.metadata.name}"**',
        "",
        f"- Members loaded: {summary['members_loaded']}",
        f"- Total entities: {summary['total_entities']}",
    ]

    if summary.get("members_skipped", 0) > 0:
        lines.append(f"- Members skipped (conflicts): {summary['members_skipped']}")

    if summary.get("conflicts"):
        lines.append("")
        lines.append("**Conflicts:**")
        for conflict in summary["conflicts"]:
            lines.append(f"- Member {conflict['member_id']}: {conflict['resolution']}")

    lines.append("")
    lines.append("Ready to continue! What would you like to work on?")

    return "\n".join(lines)


def format_cohort_list(cohorts: list[dict]) -> str:
    """Format list of saved cohorts."""
    if not cohorts:
        return (
            "No saved cohorts found.\n\n"
            "Create some members and use `save_cohort` to save your work."
        )

    lines = ["**Your Saved Cohorts:**", ""]

    for s in cohorts:
        name = s["name"]
        created = s["created_at"][:10]  # Just the date
        member_count = s["member_count"]
        tags = ", ".join(s.get("tags", [])) if s.get("tags") else ""

        line = f"- **{name}** ({created}) - {member_count} members"
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
    return f"**Deleted:** \"{info['name']}\"\n- {info['member_count']} members removed"


def format_error(message: str) -> str:
    """Format error message."""
    return f"**Error:** {message}"


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available state management tools."""
    return [
        Tool(
            name="save_cohort",
            description=(
                "Save the current workspace as a named cohort. "
                "Captures all members and claims with provenance tracking."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the cohort (e.g., 'hedis-testing', 'claims-demo')",
                        "minLength": 1,
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of what this cohort contains",
                    },
                    "tags": {
                        "type": "array",
                        "description": "Optional tags for organization (e.g., ['testing', 'hedis'])",
                        "items": {"type": "string"},
                    },
                    "member_ids": {
                        "type": "array",
                        "description": "Specific member IDs to save (default: all members)",
                        "items": {"type": "string"},
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="load_cohort",
            description=(
                "Load a saved cohort into the workspace. "
                "Can replace or merge with existing members."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "string",
                        "description": "UUID of cohort to load (if known)",
                    },
                    "name": {
                        "type": "string",
                        "description": "Name to search for (fuzzy match)",
                    },
                    "mode": {
                        "type": "string",
                        "description": "Load mode: 'replace' clears workspace first, 'merge' adds to existing",
                        "enum": ["replace", "merge"],
                        "default": "replace",
                    },
                    "member_ids": {
                        "type": "array",
                        "description": "Specific member IDs to load (default: all members)",
                        "items": {"type": "string"},
                    },
                },
            },
        ),
        Tool(
            name="list_saved_cohorts",
            description="List saved cohorts with optional filtering by name, description, or tags.",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Search string for name or description",
                    },
                    "tags": {
                        "type": "array",
                        "description": "Filter by tags (cohorts must have ALL specified tags)",
                        "items": {"type": "string"},
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum cohorts to return",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100,
                    },
                },
            },
        ),
        Tool(
            name="delete_cohort",
            description="Delete a saved cohort. This action cannot be undone.",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {
                        "type": "string",
                        "description": "UUID of cohort to delete",
                    },
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be true to confirm deletion",
                    },
                },
                "required": ["cohort_id", "confirm"],
            },
        ),
        Tool(
            name="workspace_summary",
            description=(
                "Get a summary of the current workspace state including "
                "member count and provenance breakdown."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for state management."""

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
    name = arguments.get("name")
    if not name:
        return [TextContent(type="text", text=format_error("Cohort name is required"))]

    # Check if workspace has content
    if session_manager.count() == 0:
        return [
            TextContent(
                type="text",
                text=format_error(
                    "Nothing to save. Create some members first with `create_member`."
                ),
            )
        ]

    description = arguments.get("description")
    tags = arguments.get("tags", [])
    member_ids = arguments.get("member_ids")

    try:
        cohort = session_manager.save_cohort(
            name=name,
            description=description,
            tags=tags,
            member_ids=member_ids,
        )
        return [TextContent(type="text", text=format_cohort_saved(cohort))]

    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Failed to save cohort: {e}"))]


async def handle_load_cohort(arguments: dict) -> list[TextContent]:
    """Handle load_cohort tool call."""
    cohort_id = arguments.get("cohort_id")
    name = arguments.get("name")
    mode = arguments.get("mode", "replace")
    member_ids = arguments.get("member_ids")

    if not cohort_id and not name:
        # List recent cohorts to help user choose
        cohorts = session_manager.list_cohorts(limit=5)
        if cohorts:
            lines = [
                "Please specify a cohort to load. Recent cohorts:",
                "",
            ]
            for s in cohorts:
                lines.append(f"- **{s['name']}** ({s['created_at'][:10]})")
            lines.append("")
            lines.append("Use `load_cohort` with `name` or `cohort_id`.")
            return [TextContent(type="text", text="\n".join(lines))]
        else:
            return [
                TextContent(
                    type="text",
                    text="No cohorts found. Save your work first with `save_cohort`.",
                )
            ]

    try:
        # Warn if replacing non-empty workspace
        current_count = session_manager.count()

        cohort, summary = session_manager.load_cohort(
            cohort_id=cohort_id,
            name=name,
            mode=mode,
            member_ids=member_ids,
        )

        result = format_cohort_loaded(cohort, summary)

        if mode == "replace" and current_count > 0:
            result = f"_Replaced {current_count} existing members._\n\n" + result

        return [TextContent(type="text", text=result)]

    except FileNotFoundError:
        return [
            TextContent(
                type="text",
                text=format_error(f"Cohort not found: {cohort_id or name}"),
            )
        ]
    except ValueError as e:
        return [TextContent(type="text", text=format_error(str(e)))]
    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Failed to load cohort: {e}"))]


async def handle_list_cohorts(arguments: dict) -> list[TextContent]:
    """Handle list_saved_cohorts tool call."""
    search = arguments.get("search")
    tags = arguments.get("tags")
    limit = arguments.get("limit", 20)

    cohorts = session_manager.list_cohorts(
        search=search,
        tags=tags,
        limit=limit,
    )

    return [TextContent(type="text", text=format_cohort_list(cohorts))]


async def handle_delete_cohort(arguments: dict) -> list[TextContent]:
    """Handle delete_cohort tool call."""
    cohort_id = arguments.get("cohort_id")
    confirm = arguments.get("confirm", False)

    if not cohort_id:
        return [
            TextContent(
                type="text",
                text=format_error("cohort_id is required"),
            )
        ]

    if not confirm:
        return [
            TextContent(
                type="text",
                text="Deletion requires confirmation. Set `confirm: true` to proceed.",
            )
        ]

    info = session_manager.delete_cohort(cohort_id)

    if info:
        return [TextContent(type="text", text=format_cohort_deleted(info))]
    else:
        return [
            TextContent(
                type="text",
                text=format_error(f"Cohort not found: {cohort_id}"),
            )
        ]


async def handle_workspace_summary(_arguments: dict) -> list[TextContent]:
    """Handle workspace_summary tool call."""
    summary = session_manager.get_workspace_summary()

    if summary["member_count"] == 0:
        return [
            TextContent(
                type="text",
                text=(
                    "**Workspace is empty.**\n\n"
                    "Create members with `create_member` or load a cohort with `load_cohort`."
                ),
            )
        ]

    lines = [
        "**Current Workspace:**",
        "",
        f"- Members: {summary['member_count']}",
    ]

    if summary["claims_count"] > 0:
        lines.append(f"- Claims: {summary['claims_count']}")
    if summary["authorization_count"] > 0:
        lines.append(f"- Authorizations: {summary['authorization_count']}")
    if summary["care_gap_count"] > 0:
        lines.append(f"- Care Gaps: {summary['care_gap_count']}")

    # Provenance breakdown
    prov = summary.get("provenance_summary", {})
    if prov:
        lines.append("")
        lines.append("**Provenance:**")
        if prov.get("generated", 0) > 0:
            lines.append(f"- Generated: {prov['generated']} members")
        if prov.get("loaded", 0) > 0:
            lines.append(f"- Loaded: {prov['loaded']} members")
        if prov.get("derived", 0) > 0:
            lines.append(f"- Derived: {prov['derived']} members")

    return [TextContent(type="text", text="\n".join(lines))]


def get_session_manager() -> MemberSessionManager:
    """Get the session manager instance for external use."""
    return session_manager


def set_session_manager(manager: MemberSessionManager) -> None:
    """Set the session manager instance for shared use with other servers."""
    global session_manager
    session_manager = manager


async def main():
    """Run the state management MCP server."""
    logger.info("Starting MemberSim State Management MCP Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
