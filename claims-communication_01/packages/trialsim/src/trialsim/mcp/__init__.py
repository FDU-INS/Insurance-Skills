"""MCP server components for TrialSim.

This package provides Model Context Protocol (MCP) servers for
clinical trial subject generation and state management.

Servers:
- generation_server: Subject and trial data generation tools
- state_server: Cohort save/load and workspace management
"""

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

__all__ = [
    "format_adverse_events",
    "format_cohort_summary",
    "format_error",
    "format_exposures",
    "format_skill_details",
    "format_skill_list",
    "format_subject_summary",
    "format_success",
    "format_visit_schedule",
]
