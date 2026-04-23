"""MCP Server for TrialSim generation capabilities.

This module implements a Model Context Protocol (MCP) server that exposes
clinical trial subject generation tools for use with Claude Code and other MCP clients.

Tools:
- generate_subject: Generate a single trial subject
- generate_subject_cohort: Generate multiple subjects
- generate_visit_schedule: Create visit schedule for a subject
- generate_adverse_events: Generate adverse events for a subject
- generate_exposures: Generate drug exposure records
- list_skills: List available generation skills
- get_skill_details: Get details about a specific skill
"""

import logging
from datetime import date
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from trialsim.core import (
    AdverseEventGenerator,
    ExposureGenerator,
    TrialSubjectGenerator,
    VisitGenerator,
)
from trialsim.mcp.formatters import (
    format_adverse_events,
    format_cohort_summary,
    format_error,
    format_exposures,
    format_skill_details,
    format_skill_list,
    format_subject_summary,
    format_success,
    format_visit_schedule,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trialsim.mcp")

# Initialize MCP server
app = Server("trialsim-generation")

# Available skills/templates
TRIAL_SKILLS = [
    {
        "name": "phase3_oncology",
        "description": "Phase 3 oncology trial with tumor assessments and safety monitoring",
        "parameters": {
            "treatment_cycles": {"description": "Number of treatment cycles", "default": 6},
            "cycle_length_days": {"description": "Days per cycle", "default": 21},
        },
    },
    {
        "name": "phase2_diabetes",
        "description": "Phase 2 diabetes trial with HbA1c monitoring",
        "parameters": {
            "duration_weeks": {"description": "Study duration in weeks", "default": 24},
        },
    },
    {
        "name": "phase1_healthy",
        "description": "Phase 1 healthy volunteer PK study",
        "parameters": {
            "pk_sampling_hours": {"description": "PK sampling timepoints", "default": [0, 1, 2, 4, 8, 12, 24]},
        },
    },
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="generate_subject",
            description="Generate a single trial subject with demographics and enrollment status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol_id": {
                        "type": "string",
                        "description": "Protocol identifier (e.g., 'ABC-123')",
                    },
                    "site_id": {
                        "type": "string",
                        "description": "Site identifier",
                    },
                    "skill": {
                        "type": "string",
                        "description": "Optional skill to use for generation",
                    },
                    "age_range": {
                        "type": "array",
                        "description": "Age range as [min, max]",
                        "items": {"type": "integer"},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                    },
                },
                "required": ["protocol_id"],
            },
        ),
        Tool(
            name="generate_subject_cohort",
            description="Generate multiple trial subjects for a protocol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "count": {
                        "type": "integer",
                        "description": "Number of subjects to generate",
                        "minimum": 1,
                        "maximum": 500,
                    },
                    "protocol_id": {
                        "type": "string",
                        "description": "Protocol identifier",
                    },
                    "sites": {
                        "type": "array",
                        "description": "List of site IDs to distribute subjects across",
                        "items": {"type": "string"},
                    },
                    "skill": {
                        "type": "string",
                        "description": "Optional skill to use",
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                    },
                },
                "required": ["count", "protocol_id"],
            },
        ),
        Tool(
            name="generate_visit_schedule",
            description="Generate a visit schedule for a subject.",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject_id": {
                        "type": "string",
                        "description": "Subject identifier",
                    },
                    "protocol_id": {
                        "type": "string",
                        "description": "Protocol identifier",
                    },
                    "duration_weeks": {
                        "type": "integer",
                        "description": "Study duration in weeks",
                        "minimum": 1,
                        "maximum": 156,
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Study start date (YYYY-MM-DD)",
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                    },
                },
                "required": ["subject_id", "protocol_id", "duration_weeks"],
            },
        ),
        Tool(
            name="generate_adverse_events",
            description="Generate adverse events for a subject.",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject_id": {
                        "type": "string",
                        "description": "Subject identifier",
                    },
                    "protocol_id": {
                        "type": "string",
                        "description": "Protocol identifier",
                    },
                    "visit_count": {
                        "type": "integer",
                        "description": "Number of visits to generate AEs for",
                        "minimum": 1,
                    },
                    "ae_probability": {
                        "type": "number",
                        "description": "Probability of AE per visit (0-1)",
                        "minimum": 0,
                        "maximum": 1,
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                    },
                },
                "required": ["subject_id", "protocol_id"],
            },
        ),
        Tool(
            name="generate_exposures",
            description="Generate drug exposure records for a subject.",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject_id": {
                        "type": "string",
                        "description": "Subject identifier",
                    },
                    "protocol_id": {
                        "type": "string",
                        "description": "Protocol identifier",
                    },
                    "drug_name": {
                        "type": "string",
                        "description": "Name of study drug",
                    },
                    "dose": {
                        "type": "number",
                        "description": "Drug dose",
                    },
                    "duration_weeks": {
                        "type": "integer",
                        "description": "Treatment duration in weeks",
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                    },
                },
                "required": ["subject_id", "protocol_id", "drug_name", "dose", "duration_weeks"],
            },
        ),
        Tool(
            name="list_skills",
            description="List available TrialSim generation skills.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_skill_details",
            description="Get detailed information about a specific skill.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "Name of the skill",
                    },
                },
                "required": ["skill_name"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "generate_subject":
            return await handle_generate_subject(arguments)
        elif name == "generate_subject_cohort":
            return await handle_generate_cohort(arguments)
        elif name == "generate_visit_schedule":
            return await handle_generate_visits(arguments)
        elif name == "generate_adverse_events":
            return await handle_generate_aes(arguments)
        elif name == "generate_exposures":
            return await handle_generate_exposures(arguments)
        elif name == "list_skills":
            return await handle_list_skills(arguments)
        elif name == "get_skill_details":
            return await handle_get_skill_details(arguments)
        else:
            return [TextContent(type="text", text=format_error(f"Unknown tool: {name}"))]
    except Exception as e:
        logger.exception(f"Error in tool {name}")
        return [TextContent(type="text", text=format_error(str(e)))]


async def handle_generate_subject(arguments: dict) -> list[TextContent]:
    """Handle generate_subject tool call."""
    protocol_id = arguments["protocol_id"]
    site_id = arguments.get("site_id")
    seed = arguments.get("seed")
    age_range = arguments.get("age_range")
    
    generator = TrialSubjectGenerator(seed=seed)
    
    kwargs = {"protocol_id": protocol_id}
    if site_id:
        kwargs["site_id"] = site_id
    if age_range:
        kwargs["age_range"] = tuple(age_range)
    
    subject = generator.generate(**kwargs)
    
    return [TextContent(type="text", text=format_subject_summary(subject))]


async def handle_generate_cohort(arguments: dict) -> list[TextContent]:
    """Handle generate_subject_cohort tool call."""
    count = arguments["count"]
    protocol_id = arguments["protocol_id"]
    sites = arguments.get("sites")
    seed = arguments.get("seed")
    skill = arguments.get("skill")
    
    generator = TrialSubjectGenerator(seed=seed)
    
    subjects = generator.generate_many(
        count=count,
        protocol_id=protocol_id,
        sites=sites,
    )
    
    return [TextContent(type="text", text=format_cohort_summary(subjects, skill))]


async def handle_generate_visits(arguments: dict) -> list[TextContent]:
    """Handle generate_visit_schedule tool call."""
    from trialsim.core.models import Subject, SubjectStatus
    
    subject_id = arguments["subject_id"]
    protocol_id = arguments["protocol_id"]
    duration_weeks = arguments["duration_weeks"]
    start_date_str = arguments.get("start_date")
    seed = arguments.get("seed")
    
    # Create a minimal subject for visit generation
    subject = Subject(
        subject_id=subject_id,
        protocol_id=protocol_id,
        site_id="SITE-001",
        age=50,
        sex="M",
        status=SubjectStatus.ENROLLED,
    )
    
    start_date = None
    if start_date_str:
        start_date = date.fromisoformat(start_date_str)
    
    generator = VisitGenerator(seed=seed)
    visits = generator.generate_schedule(
        subject=subject,
        duration_weeks=duration_weeks,
        start_date=start_date,
    )
    
    return [TextContent(type="text", text=format_visit_schedule(visits))]


async def handle_generate_aes(arguments: dict) -> list[TextContent]:
    """Handle generate_adverse_events tool call."""
    from trialsim.core.models import Subject, SubjectStatus
    
    subject_id = arguments["subject_id"]
    protocol_id = arguments["protocol_id"]
    visit_count = arguments.get("visit_count", 10)
    ae_probability = arguments.get("ae_probability", 0.3)
    seed = arguments.get("seed")
    
    # Create a minimal subject
    subject = Subject(
        subject_id=subject_id,
        protocol_id=protocol_id,
        site_id="SITE-001",
        age=50,
        sex="M",
        status=SubjectStatus.ON_TREATMENT,
    )
    
    generator = AdverseEventGenerator(seed=seed)
    adverse_events = generator.generate_for_subject(
        subject=subject,
        visit_count=visit_count,
        ae_probability=ae_probability,
    )
    
    return [TextContent(type="text", text=format_adverse_events(adverse_events))]


async def handle_generate_exposures(arguments: dict) -> list[TextContent]:
    """Handle generate_exposures tool call."""
    from trialsim.core.models import Subject, SubjectStatus
    
    subject_id = arguments["subject_id"]
    protocol_id = arguments["protocol_id"]
    drug_name = arguments["drug_name"]
    dose = arguments["dose"]
    duration_weeks = arguments["duration_weeks"]
    seed = arguments.get("seed")
    
    # Create a minimal subject
    subject = Subject(
        subject_id=subject_id,
        protocol_id=protocol_id,
        site_id="SITE-001",
        age=50,
        sex="M",
        status=SubjectStatus.ON_TREATMENT,
    )
    
    generator = ExposureGenerator(seed=seed)
    exposures = generator.generate_for_subject(
        subject=subject,
        drug_name=drug_name,
        dose=dose,
        duration_weeks=duration_weeks,
    )
    
    return [TextContent(type="text", text=format_exposures(exposures))]


async def handle_list_skills(_arguments: dict) -> list[TextContent]:
    """Handle list_skills tool call."""
    return [TextContent(type="text", text=format_skill_list(TRIAL_SKILLS))]


async def handle_get_skill_details(arguments: dict) -> list[TextContent]:
    """Handle get_skill_details tool call."""
    skill_name = arguments["skill_name"]
    
    for skill in TRIAL_SKILLS:
        if skill["name"] == skill_name:
            return [TextContent(type="text", text=format_skill_details(skill))]
    
    return [TextContent(type="text", text=format_error(f"Skill not found: {skill_name}"))]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
