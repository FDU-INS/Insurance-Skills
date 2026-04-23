"""MCP Server for profile and journey management.

This module implements a Model Context Protocol (MCP) server that exposes
tools for building, saving, loading, and executing profile and journey
specifications.

Profile Management Tools:
- build_profile: Create a profile specification from parameters
- save_profile: Save a profile to persistent storage
- load_profile: Load a profile by name or ID
- list_profiles: List available profiles
- list_profile_templates: List built-in profile templates
- get_profile_template: Get details of a specific profile template
- execute_profile: Execute a profile to generate entities

Journey Management Tools:
- build_journey: Create a journey specification from parameters
- save_journey: Save a journey to persistent storage
- load_journey: Load a journey by name or ID
- list_journeys: List available journeys
- list_journey_templates: List built-in journey templates
- get_journey_template: Get details of a specific journey template
- execute_journey: Execute a journey for an entity/cohort
"""

import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from healthsim.generation.profile_schema import (
    PROFILE_TEMPLATES,
    ProfileSpecification,
)
from healthsim.generation.profile_executor import (
    ProfileExecutor,
    ExecutionResult,
)
from healthsim.generation.journey_engine import (
    JOURNEY_TEMPLATES,
    JourneySpecification,
    JourneyEngine,
    EventDefinition,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("healthsim.mcp.profile")

# Initialize MCP server
app = Server("healthsim-profiles")

# Default storage path for saved profiles and journeys
PROFILES_DIR = Path.home() / ".healthsim" / "profiles"
JOURNEYS_DIR = Path.home() / ".healthsim" / "journeys"


def ensure_storage_dirs():
    """Ensure storage directories exist."""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    JOURNEYS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Profile Formatters
# =============================================================================

def format_profile_summary(profile: ProfileSpecification) -> str:
    """Format a profile specification for display."""
    lines = [
        f"**Profile: {profile.name}**",
        f"- ID: `{profile.id}`",
        f"- Version: {profile.version}",
    ]
    
    if profile.description:
        lines.append(f"- Description: {profile.description}")
    
    lines.append("")
    lines.append("**Generation:**")
    lines.append(f"- Count: {profile.generation.count}")
    lines.append(f"- Products: {', '.join(profile.generation.products)}")
    if profile.generation.seed:
        lines.append(f"- Seed: {profile.generation.seed}")
    
    if profile.demographics:
        lines.append("")
        lines.append("**Demographics:**")
        if profile.demographics.age:
            age = profile.demographics.age
            if age.type.value == "normal" and age.mean:
                lines.append(f"- Age: Normal(μ={age.mean}, σ={age.std_dev or 10})")
            elif age.type.value == "age_bands" and age.bands:
                lines.append(f"- Age bands: {', '.join(age.bands.keys())}")
        if profile.demographics.gender:
            lines.append(f"- Gender distribution defined")
    
    if profile.clinical:
        lines.append("")
        lines.append("**Clinical:**")
        if profile.clinical.primary_condition:
            cond = profile.clinical.primary_condition
            lines.append(f"- Primary: {cond.code} ({cond.description or 'N/A'})")
        if profile.clinical.comorbidities:
            lines.append(f"- Comorbidities: {len(profile.clinical.comorbidities)}")
    
    if profile.coverage:
        lines.append("")
        lines.append("**Coverage:**")
        if profile.coverage.type:
            lines.append(f"- Type: {profile.coverage.type}")
    
    return "\n".join(lines)


def format_profile_list(profiles: list[dict]) -> str:
    """Format list of profiles for display."""
    if not profiles:
        return "No saved profiles found.\n\nUse `build_profile` to create one."
    
    lines = ["**Saved Profiles:**", ""]
    
    for p in profiles:
        line = f"- **{p['name']}** (`{p['id']}`)"
        if p.get("description"):
            line += f"\n  _{p['description']}_"
        lines.append(line)
    
    return "\n".join(lines)


def format_template_list(templates: dict, entity_type: str) -> str:
    """Format list of templates for display."""
    lines = [f"**Built-in {entity_type.title()} Templates:**", ""]
    
    for name, spec in templates.items():
        desc = spec.get("description", spec.get("name", name))
        lines.append(f"- **{name}**: {desc}")
    
    lines.append("")
    lines.append(f"Use `get_{entity_type.lower()}_template` to see details.")
    
    return "\n".join(lines)


def format_execution_result(result: ExecutionResult) -> str:
    """Format execution result for display."""
    lines = [
        f"**Execution Complete**",
        "",
        f"- Entities generated: {result.count}",
        f"- Seed used: {result.seed}",
        f"- Duration: {result.duration_seconds:.2f}s",
    ]
    
    if result.validation:
        lines.append("")
        lines.append("**Validation:**")
        status = "Passed" if result.validation.passed else "Failed"
        lines.append(f"- Status: {status}")
        if result.validation.warnings:
            lines.append(f"- Warnings: {len(result.validation.warnings)}")
        if result.validation.errors:
            lines.append(f"- Errors: {len(result.validation.errors)}")
    
    return "\n".join(lines)


# =============================================================================
# Journey Formatters
# =============================================================================

def format_journey_summary(journey: dict) -> str:
    """Format a journey specification for display."""
    lines = [
        f"**Journey: {journey.get('name', journey.get('journey_id', 'Unnamed'))}**",
        f"- ID: `{journey.get('journey_id', journey.get('id', 'N/A'))}`",
    ]
    
    if journey.get("version"):
        lines.append(f"- Version: {journey['version']}")
    
    if journey.get("description"):
        lines.append(f"- Description: {journey['description']}")
    
    lines.append("")
    
    # Duration
    if journey.get("duration_days"):
        lines.append(f"**Duration:** {journey['duration_days']} days")
    elif journey.get("duration"):
        dur = journey["duration"]
        lines.append(f"**Duration:** {dur.get('min_days', '?')}-{dur.get('max_days', '?')} days")
    
    # Products
    products = journey.get("products", ["patientsim"])
    lines.append(f"**Products:** {', '.join(products)}")
    
    # Events
    events = journey.get("events", [])
    if events:
        lines.append("")
        lines.append(f"**Events ({len(events)}):**")
        for evt in events[:8]:
            evt_name = evt.get("name", evt.get("event_type", "Event"))
            evt_type = evt.get("event_type", "")
            if evt_type and evt_type != evt_name:
                lines.append(f"- {evt_name} ({evt_type})")
            else:
                lines.append(f"- {evt_name}")
        if len(events) > 8:
            lines.append(f"- ... and {len(events) - 8} more")
    
    # Parameters
    params = journey.get("parameters", {})
    if params:
        lines.append("")
        lines.append(f"**Parameters:** {len(params)} defined")
    
    return "\n".join(lines)


def format_journey_list(journeys: list[dict]) -> str:
    """Format list of journeys for display."""
    if not journeys:
        return "No saved journeys found.\n\nUse `build_journey` to create one."
    
    lines = ["**Saved Journeys:**", ""]
    
    for j in journeys:
        name = j.get('name', j.get('journey_id', 'Unnamed'))
        jid = j.get('journey_id', j.get('id', 'N/A'))
        line = f"- **{name}** (`{jid}`)"
        
        event_count = len(j.get('events', []))
        duration = j.get('duration_days', '')
        
        details = []
        if event_count:
            details.append(f"{event_count} events")
        if duration:
            details.append(f"{duration} days")
        
        if details:
            line += f" - {', '.join(details)}"
        
        if j.get("description"):
            line += f"\n  _{j['description']}_"
        lines.append(line)
    
    return "\n".join(lines)


# =============================================================================
# Common Formatters
# =============================================================================

def format_error(message: str) -> str:
    """Format error message."""
    return f"**Error:** {message}"


def format_success(message: str) -> str:
    """Format success message."""
    return f"✓ {message}"


# =============================================================================
# Tool Definitions
# =============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available profile/journey management tools."""
    return [
        # Profile Tools
        Tool(
            name="build_profile",
            description=(
                "Build a profile specification from parameters. "
                "Creates a ProfileSpecification that can be saved or executed."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Profile name"},
                    "id": {"type": "string", "description": "Unique identifier"},
                    "description": {"type": "string", "description": "Description"},
                    "count": {"type": "integer", "description": "Generation count", "default": 100},
                    "products": {"type": "array", "items": {"type": "string"}, "description": "Target products"},
                    "seed": {"type": "integer", "description": "Random seed"},
                    "age_mean": {"type": "number", "description": "Mean age"},
                    "age_std": {"type": "number", "description": "Age std dev"},
                    "age_min": {"type": "number", "description": "Min age"},
                    "age_max": {"type": "number", "description": "Max age"},
                    "gender_weights": {"type": "object", "description": "Gender weights {'M': 0.5, 'F': 0.5}"},
                    "primary_condition_code": {"type": "string", "description": "ICD-10 code"},
                    "primary_condition_name": {"type": "string", "description": "Condition name"},
                    "coverage_type": {"type": "string", "description": "Coverage type"},
                    "from_template": {"type": "string", "description": "Base template name"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="save_profile",
            description="Save a profile specification to persistent storage.",
            inputSchema={
                "type": "object",
                "properties": {
                    "profile_json": {"type": "string", "description": "Profile JSON"},
                    "overwrite": {"type": "boolean", "description": "Overwrite if exists", "default": False},
                },
                "required": ["profile_json"],
            },
        ),
        Tool(
            name="load_profile",
            description="Load a profile by name, ID, or template name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Profile name or ID"},
                    "template": {"type": "string", "description": "Template name"},
                },
            },
        ),
        Tool(
            name="list_profiles",
            description="List available saved profiles.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_profile_templates",
            description="List built-in profile templates.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_profile_template",
            description="Get details of a specific profile template.",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_name": {"type": "string", "description": "Template name"},
                },
                "required": ["template_name"],
            },
        ),
        Tool(
            name="execute_profile",
            description="Execute a profile to generate entities.",
            inputSchema={
                "type": "object",
                "properties": {
                    "profile_json": {"type": "string", "description": "Profile JSON"},
                    "profile_name": {"type": "string", "description": "Saved profile name"},
                    "template": {"type": "string", "description": "Template name"},
                    "count_override": {"type": "integer", "description": "Override count"},
                    "seed_override": {"type": "integer", "description": "Override seed"},
                },
            },
        ),
        # Journey Tools
        Tool(
            name="build_journey",
            description=(
                "Build a journey specification from parameters. "
                "Creates a JourneySpecification that can be saved or executed."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Journey name"},
                    "id": {"type": "string", "description": "Unique identifier"},
                    "description": {"type": "string", "description": "Description"},
                    "duration_days": {"type": "integer", "description": "Journey duration in days"},
                    "products": {"type": "array", "items": {"type": "string"}, "description": "Target products"},
                    "events": {"type": "array", "description": "List of event definitions"},
                    "from_template": {"type": "string", "description": "Base template name"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="save_journey",
            description="Save a journey specification to persistent storage.",
            inputSchema={
                "type": "object",
                "properties": {
                    "journey_json": {"type": "string", "description": "Journey JSON"},
                    "overwrite": {"type": "boolean", "description": "Overwrite if exists", "default": False},
                },
                "required": ["journey_json"],
            },
        ),
        Tool(
            name="load_journey",
            description="Load a journey by name, ID, or template name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Journey name or ID"},
                    "template": {"type": "string", "description": "Template name"},
                },
            },
        ),
        Tool(
            name="list_journeys",
            description="List available saved journeys.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_journey_templates",
            description="List built-in journey templates.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_journey_template",
            description="Get details of a specific journey template.",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_name": {"type": "string", "description": "Template name"},
                },
                "required": ["template_name"],
            },
        ),
        Tool(
            name="execute_journey",
            description="Execute a journey to generate a timeline of events.",
            inputSchema={
                "type": "object",
                "properties": {
                    "journey_json": {"type": "string", "description": "Journey JSON"},
                    "journey_name": {"type": "string", "description": "Saved journey name"},
                    "template": {"type": "string", "description": "Template name"},
                    "entity_id": {"type": "string", "description": "Entity ID to execute journey for"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "seed": {"type": "integer", "description": "Random seed for reproducibility"},
                },
            },
        ),
    ]


# =============================================================================
# Tool Router
# =============================================================================

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        # Profile tools
        if name == "build_profile":
            return await handle_build_profile(arguments)
        elif name == "save_profile":
            return await handle_save_profile(arguments)
        elif name == "load_profile":
            return await handle_load_profile(arguments)
        elif name == "list_profiles":
            return await handle_list_profiles(arguments)
        elif name == "list_profile_templates":
            return await handle_list_profile_templates(arguments)
        elif name == "get_profile_template":
            return await handle_get_profile_template(arguments)
        elif name == "execute_profile":
            return await handle_execute_profile(arguments)
        # Journey tools
        elif name == "build_journey":
            return await handle_build_journey(arguments)
        elif name == "save_journey":
            return await handle_save_journey(arguments)
        elif name == "load_journey":
            return await handle_load_journey(arguments)
        elif name == "list_journeys":
            return await handle_list_journeys(arguments)
        elif name == "list_journey_templates":
            return await handle_list_journey_templates(arguments)
        elif name == "get_journey_template":
            return await handle_get_journey_template(arguments)
        elif name == "execute_journey":
            return await handle_execute_journey(arguments)
        else:
            return [TextContent(type="text", text=format_error(f"Unknown tool: {name}"))]
    except Exception as e:
        logger.exception(f"Error in tool {name}")
        return [TextContent(type="text", text=format_error(str(e)))]


# =============================================================================
# Profile Handlers
# =============================================================================

async def handle_build_profile(arguments: dict) -> list[TextContent]:
    """Handle build_profile tool call."""
    name = arguments["name"]
    
    # Start from template if specified
    if arguments.get("from_template"):
        template_name = arguments["from_template"]
        if template_name in PROFILE_TEMPLATES:
            base_spec = PROFILE_TEMPLATES[template_name].copy()
        else:
            return [TextContent(type="text", text=format_error(f"Template not found: {template_name}"))]
    else:
        base_spec = {}
    
    profile_id = arguments.get("id") or name.lower().replace(" ", "-")
    
    # Build demographics
    demographics = base_spec.get("demographics", {}).copy() if base_spec.get("demographics") else {}
    if arguments.get("age_mean"):
        demographics["age"] = {
            "type": "normal",
            "mean": arguments["age_mean"],
            "std_dev": arguments.get("age_std", 10),
            "min": arguments.get("age_min"),
            "max": arguments.get("age_max"),
        }
    if arguments.get("gender_weights"):
        demographics["gender"] = {"type": "categorical", "weights": arguments["gender_weights"]}
    
    # Build clinical
    clinical = base_spec.get("clinical", {}).copy() if base_spec.get("clinical") else {}
    if arguments.get("primary_condition_code"):
        clinical["primary_condition"] = {
            "code": arguments["primary_condition_code"],
            "description": arguments.get("primary_condition_name"),
            "prevalence": 1.0,
        }
    
    # Build coverage
    coverage = base_spec.get("coverage", {}).copy() if base_spec.get("coverage") else {}
    if arguments.get("coverage_type"):
        coverage["type"] = arguments["coverage_type"]
    
    # Build generation
    generation = {
        "count": arguments.get("count", 100),
        "products": arguments.get("products", ["patientsim"]),
    }
    if arguments.get("seed"):
        generation["seed"] = arguments["seed"]
    
    spec = {
        "id": profile_id,
        "name": name,
        "description": arguments.get("description"),
        "version": "1.0",
        "generation": generation,
    }
    if demographics:
        spec["demographics"] = demographics
    if clinical:
        spec["clinical"] = clinical
    if coverage:
        spec["coverage"] = coverage
    
    try:
        profile = ProfileSpecification.model_validate(spec)
    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Invalid profile: {e}"))]
    
    result = format_profile_summary(profile)
    result += "\n\n**JSON:**\n```json\n" + profile.to_json() + "\n```"
    result += "\n\nUse `save_profile` to save or `execute_profile` to generate."
    
    return [TextContent(type="text", text=result)]


async def handle_save_profile(arguments: dict) -> list[TextContent]:
    """Handle save_profile tool call."""
    ensure_storage_dirs()
    
    profile_json = arguments["profile_json"]
    overwrite = arguments.get("overwrite", False)
    
    try:
        profile = ProfileSpecification.from_json(profile_json)
    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Invalid JSON: {e}"))]
    
    filepath = PROFILES_DIR / f"{profile.id}.json"
    
    if filepath.exists() and not overwrite:
        return [TextContent(
            type="text",
            text=format_error(f"Profile exists: {profile.id}. Use overwrite=true.")
        )]
    
    filepath.write_text(profile.to_json())
    
    return [TextContent(type="text", text=format_success(f"Saved: {profile.name} ({filepath})"))]


async def handle_load_profile(arguments: dict) -> list[TextContent]:
    """Handle load_profile tool call."""
    name = arguments.get("name")
    template = arguments.get("template")
    
    if not name and not template:
        return [TextContent(type="text", text=format_error("Either name or template required"))]
    
    if template:
        if template in PROFILE_TEMPLATES:
            profile = ProfileSpecification.model_validate(PROFILE_TEMPLATES[template])
            result = format_profile_summary(profile)
            result += "\n\n**JSON:**\n```json\n" + profile.to_json() + "\n```"
            return [TextContent(type="text", text=result)]
        else:
            return [TextContent(type="text", text=format_error(f"Template not found: {template}"))]
    
    ensure_storage_dirs()
    filepath = PROFILES_DIR / f"{name}.json"
    if not filepath.exists():
        for f in PROFILES_DIR.glob("*.json"):
            try:
                content = json.loads(f.read_text())
                if content.get("name") == name or content.get("id") == name:
                    filepath = f
                    break
            except:
                continue
    
    if not filepath.exists():
        return [TextContent(type="text", text=format_error(f"Profile not found: {name}"))]
    
    profile = ProfileSpecification.from_json(filepath.read_text())
    result = format_profile_summary(profile)
    result += "\n\n**JSON:**\n```json\n" + profile.to_json() + "\n```"
    
    return [TextContent(type="text", text=result)]


async def handle_list_profiles(arguments: dict) -> list[TextContent]:
    """Handle list_profiles tool call."""
    ensure_storage_dirs()
    
    profiles = []
    for f in sorted(PROFILES_DIR.glob("*.json")):
        try:
            content = json.loads(f.read_text())
            profiles.append({
                "id": content.get("id"),
                "name": content.get("name"),
                "description": content.get("description"),
            })
        except:
            continue
    
    return [TextContent(type="text", text=format_profile_list(profiles))]


async def handle_list_profile_templates(arguments: dict) -> list[TextContent]:
    """Handle list_profile_templates tool call."""
    return [TextContent(type="text", text=format_template_list(PROFILE_TEMPLATES, "Profile"))]


async def handle_get_profile_template(arguments: dict) -> list[TextContent]:
    """Handle get_profile_template tool call."""
    template_name = arguments["template_name"]
    
    if template_name not in PROFILE_TEMPLATES:
        available = ", ".join(PROFILE_TEMPLATES.keys())
        return [TextContent(
            type="text",
            text=format_error(f"Template not found: {template_name}. Available: {available}")
        )]
    
    template = PROFILE_TEMPLATES[template_name]
    
    try:
        profile = ProfileSpecification.model_validate(template)
        result = format_profile_summary(profile)
        result += "\n\n**JSON:**\n```json\n" + profile.to_json() + "\n```"
    except Exception:
        # Template may not be a full ProfileSpecification
        result = f"**Profile Template: {template_name}**\n\n"
        result += "```json\n" + json.dumps(template, indent=2, default=str) + "\n```"
    
    return [TextContent(type="text", text=result)]


async def handle_execute_profile(arguments: dict) -> list[TextContent]:
    """Handle execute_profile tool call."""
    profile_json = arguments.get("profile_json")
    profile_name = arguments.get("profile_name")
    template = arguments.get("template")
    count_override = arguments.get("count_override")
    seed_override = arguments.get("seed_override")
    
    if profile_json:
        try:
            profile = ProfileSpecification.from_json(profile_json)
        except Exception as e:
            return [TextContent(type="text", text=format_error(f"Invalid JSON: {e}"))]
    elif template:
        if template in PROFILE_TEMPLATES:
            profile = ProfileSpecification.model_validate(PROFILE_TEMPLATES[template])
        else:
            return [TextContent(type="text", text=format_error(f"Template not found: {template}"))]
    elif profile_name:
        ensure_storage_dirs()
        filepath = PROFILES_DIR / f"{profile_name}.json"
        if not filepath.exists():
            return [TextContent(type="text", text=format_error(f"Profile not found: {profile_name}"))]
        profile = ProfileSpecification.from_json(filepath.read_text())
    else:
        return [TextContent(type="text", text=format_error("Provide profile_json, profile_name, or template"))]
    
    if count_override:
        profile.generation.count = count_override
    if seed_override:
        profile.generation.seed = seed_override
    
    executor = ProfileExecutor()
    result = executor.execute(profile)
    
    return [TextContent(type="text", text=format_execution_result(result))]


# =============================================================================
# Journey Handlers
# =============================================================================

async def handle_build_journey(arguments: dict) -> list[TextContent]:
    """Handle build_journey tool call."""
    name = arguments["name"]
    
    # Start from template if specified
    if arguments.get("from_template"):
        template_name = arguments["from_template"]
        if template_name in JOURNEY_TEMPLATES:
            base_spec = JOURNEY_TEMPLATES[template_name].copy()
        else:
            return [TextContent(type="text", text=format_error(f"Template not found: {template_name}"))]
    else:
        base_spec = {}
    
    journey_id = arguments.get("id") or name.lower().replace(" ", "-")
    
    # Build journey spec
    spec = {
        "journey_id": journey_id,
        "name": name,
        "description": arguments.get("description", base_spec.get("description", "")),
        "version": "1.0",
        "products": arguments.get("products", base_spec.get("products", ["patientsim"])),
        "duration_days": arguments.get("duration_days", base_spec.get("duration_days")),
        "events": arguments.get("events", base_spec.get("events", [])),
        "parameters": base_spec.get("parameters", {}),
    }
    
    result = format_journey_summary(spec)
    result += "\n\n**JSON:**\n```json\n" + json.dumps(spec, indent=2, default=str) + "\n```"
    result += "\n\nUse `save_journey` to save or `execute_journey` to run."
    
    return [TextContent(type="text", text=result)]


async def handle_save_journey(arguments: dict) -> list[TextContent]:
    """Handle save_journey tool call."""
    ensure_storage_dirs()
    
    journey_json = arguments["journey_json"]
    overwrite = arguments.get("overwrite", False)
    
    try:
        journey = json.loads(journey_json)
    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Invalid JSON: {e}"))]
    
    journey_id = journey.get("journey_id", journey.get("id"))
    if not journey_id:
        return [TextContent(type="text", text=format_error("Journey must have journey_id or id field"))]
    
    filepath = JOURNEYS_DIR / f"{journey_id}.json"
    
    if filepath.exists() and not overwrite:
        return [TextContent(
            type="text",
            text=format_error(f"Journey exists: {journey_id}. Use overwrite=true.")
        )]
    
    filepath.write_text(json.dumps(journey, indent=2, default=str))
    
    journey_name = journey.get("name", journey_id)
    return [TextContent(type="text", text=format_success(f"Saved: {journey_name} ({filepath})"))]


async def handle_load_journey(arguments: dict) -> list[TextContent]:
    """Handle load_journey tool call."""
    name = arguments.get("name")
    template = arguments.get("template")
    
    if not name and not template:
        return [TextContent(type="text", text=format_error("Either name or template required"))]
    
    if template:
        if template in JOURNEY_TEMPLATES:
            journey = JOURNEY_TEMPLATES[template]
            result = format_journey_summary(journey)
            result += "\n\n**JSON:**\n```json\n" + json.dumps(journey, indent=2, default=str) + "\n```"
            return [TextContent(type="text", text=result)]
        else:
            return [TextContent(type="text", text=format_error(f"Template not found: {template}"))]
    
    ensure_storage_dirs()
    filepath = JOURNEYS_DIR / f"{name}.json"
    if not filepath.exists():
        for f in JOURNEYS_DIR.glob("*.json"):
            try:
                content = json.loads(f.read_text())
                if content.get("name") == name or content.get("journey_id") == name:
                    filepath = f
                    break
            except:
                continue
    
    if not filepath.exists():
        return [TextContent(type="text", text=format_error(f"Journey not found: {name}"))]
    
    journey = json.loads(filepath.read_text())
    result = format_journey_summary(journey)
    result += "\n\n**JSON:**\n```json\n" + json.dumps(journey, indent=2, default=str) + "\n```"
    
    return [TextContent(type="text", text=result)]


async def handle_list_journeys(arguments: dict) -> list[TextContent]:
    """Handle list_journeys tool call."""
    ensure_storage_dirs()
    
    journeys = []
    for f in sorted(JOURNEYS_DIR.glob("*.json")):
        try:
            content = json.loads(f.read_text())
            journeys.append(content)
        except:
            continue
    
    return [TextContent(type="text", text=format_journey_list(journeys))]


async def handle_list_journey_templates(arguments: dict) -> list[TextContent]:
    """Handle list_journey_templates tool call."""
    lines = ["**Built-in Journey Templates:**", ""]
    
    for name, spec in JOURNEY_TEMPLATES.items():
        desc = spec.get("description", spec.get("name", name))
        duration = spec.get("duration_days") or spec.get("duration", {}).get("max_days", "?")
        events = len(spec.get("events", []))
        lines.append(f"- **{name}**: {desc} ({events} events, ~{duration} days)")
    
    lines.append("")
    lines.append("Use `get_journey_template` to see details.")
    
    return [TextContent(type="text", text="\n".join(lines))]


async def handle_get_journey_template(arguments: dict) -> list[TextContent]:
    """Handle get_journey_template tool call."""
    template_name = arguments["template_name"]
    
    if template_name not in JOURNEY_TEMPLATES:
        available = ", ".join(JOURNEY_TEMPLATES.keys())
        return [TextContent(
            type="text",
            text=format_error(f"Template not found: {template_name}. Available: {available}")
        )]
    
    template = JOURNEY_TEMPLATES[template_name]
    
    result = format_journey_summary(template)
    result += "\n\n**JSON:**\n```json\n" + json.dumps(template, indent=2, default=str) + "\n```"
    
    return [TextContent(type="text", text=result)]


async def handle_execute_journey(arguments: dict) -> list[TextContent]:
    """Handle execute_journey tool call."""
    journey_json = arguments.get("journey_json")
    journey_name = arguments.get("journey_name")
    template = arguments.get("template")
    entity_id = arguments.get("entity_id", f"entity-{uuid4().hex[:8]}")
    start_date_str = arguments.get("start_date")
    seed = arguments.get("seed")
    
    # Determine start date
    if start_date_str:
        try:
            start_date = date.fromisoformat(start_date_str)
        except ValueError:
            return [TextContent(type="text", text=format_error(f"Invalid date format: {start_date_str}. Use YYYY-MM-DD."))]
    else:
        start_date = date.today()
    
    # Load journey spec
    if journey_json:
        try:
            journey_spec = json.loads(journey_json)
        except Exception as e:
            return [TextContent(type="text", text=format_error(f"Invalid JSON: {e}"))]
    elif template:
        if template in JOURNEY_TEMPLATES:
            journey_spec = JOURNEY_TEMPLATES[template]
        else:
            return [TextContent(type="text", text=format_error(f"Template not found: {template}"))]
    elif journey_name:
        ensure_storage_dirs()
        filepath = JOURNEYS_DIR / f"{journey_name}.json"
        if not filepath.exists():
            # Try to find by name
            for f in JOURNEYS_DIR.glob("*.json"):
                try:
                    content = json.loads(f.read_text())
                    if content.get("name") == journey_name or content.get("journey_id") == journey_name:
                        filepath = f
                        break
                except:
                    continue
        if not filepath.exists():
            return [TextContent(type="text", text=format_error(f"Journey not found: {journey_name}"))]
        journey_spec = json.loads(filepath.read_text())
    else:
        return [TextContent(type="text", text=format_error("Provide journey_json, journey_name, or template"))]
    
    # Execute journey using JourneyEngine
    try:
        engine = JourneyEngine(seed=seed)
        timeline = engine.create_timeline(
            entity_id=entity_id,
            entity_type="patient",
            journey_spec=journey_spec,
            start_date=start_date,
        )
        
        # Format results
        lines = [
            "**Journey Execution Complete**",
            "",
            f"- Entity ID: `{entity_id}`",
            f"- Journey: {journey_spec.get('name', journey_spec.get('journey_id', 'Unknown'))}",
            f"- Start date: {start_date}",
            f"- Events scheduled: {len(timeline.events)}",
        ]
        
        if seed:
            lines.append(f"- Seed: {seed}")
        
        if timeline.events:
            lines.append("")
            lines.append("**Timeline Preview (first 10 events):**")
            for evt in timeline.events[:10]:
                lines.append(f"- {evt.scheduled_date}: {evt.event_name} ({evt.event_type})")
            if len(timeline.events) > 10:
                lines.append(f"- ... and {len(timeline.events) - 10} more events")
        
        return [TextContent(type="text", text="\n".join(lines))]
    except Exception as e:
        logger.exception("Error executing journey")
        return [TextContent(type="text", text=format_error(f"Execution failed: {e}"))]


# =============================================================================
# Main Entry Point
# =============================================================================

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
