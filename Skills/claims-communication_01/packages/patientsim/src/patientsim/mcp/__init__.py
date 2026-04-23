"""Model Context Protocol (MCP) integration for Claude.

This module provides MCP servers that expose PatientSim capabilities
for use with Claude Code and other MCP clients.
"""

from patientsim.mcp.generation_server import app as generation_server
from patientsim.mcp.session import PatientSession, PatientSessionManager, SessionManager
from patientsim.mcp.state_server import app as state_server

__all__ = [
    "generation_server",
    "state_server",
    "PatientSessionManager",
    "SessionManager",  # Backwards-compatible alias
    "PatientSession",
]
