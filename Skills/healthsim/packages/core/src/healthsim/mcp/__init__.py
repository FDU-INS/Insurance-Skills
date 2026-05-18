"""MCP servers for HealthSim core.

This package provides Model Context Protocol (MCP) servers for
profile and journey management.

Tools provided:
- Profile: build, save, load, list, templates, execute
- Journey: build, save, load, list, templates, execute
"""

from healthsim.mcp.profile_server import app, main

__all__ = ["app", "main"]
