"""MCP server for MemberSim."""

from membersim.mcp.server import MemberSimMCPHandler, default_handler
from membersim.mcp.session import MemberSession, MemberSessionManager, session_manager

# state_server requires mcp package - import conditionally
try:
    from membersim.mcp.state_server import app as state_server
except ImportError:
    state_server = None  # type: ignore[assignment]

__all__ = [
    "MemberSimMCPHandler",
    "default_handler",
    "MemberSession",
    "MemberSessionManager",
    "session_manager",
    "state_server",
]
