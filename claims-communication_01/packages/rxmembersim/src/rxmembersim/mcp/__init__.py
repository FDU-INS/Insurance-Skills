"""MCP server for RxMemberSim."""

from .session import RxMemberSession, RxMemberSessionManager, session_manager

# server and state_server require mcp package - import conditionally
try:
    from .server import server
    from .state_server import app as state_server
except ImportError:
    server = None  # type: ignore[assignment]
    state_server = None  # type: ignore[assignment]

__all__ = [
    "server",
    "RxMemberSession",
    "RxMemberSessionManager",
    "session_manager",
    "state_server",
]
