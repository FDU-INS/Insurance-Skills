# p0-02: MCP Server HTTP Transport + Bearer Token Auth

## What to build

Modify `packages/mcp-server/healthsim_mcp.py` to support both stdio (for local Claude Code development) and HTTP (for Railway deployment) transports. Add bearer token authentication for the HTTP transport.

## Context

The current MCP server uses FastMCP and runs with `mcp.run(transport="stdio")`. For Managed Agents, the server needs to be reachable via HTTPS URL. FastMCP supports both transports — we need to make it switchable via environment variable.

Read `packages/mcp-server/healthsim_mcp.py` first to understand the current structure.

## Tasks

1. **Add transport switching** at the bottom of `healthsim_mcp.py`:
   ```python
   import os

   transport = os.environ.get("MCP_TRANSPORT", "stdio")

   if transport == "http":
       port = int(os.environ.get("MCP_PORT", "8001"))
       mcp.run(transport="http", host="0.0.0.0", port=port)
   else:
       mcp.run(transport="stdio")
   ```

   Replace the existing `mcp.run()` call with this block.

2. **Add bearer token authentication middleware** for HTTP transport. Before the transport switching block, add authentication that checks for a bearer token on incoming requests when running in HTTP mode. The token is read from the `HEALTHSIM_MCP_TOKEN` environment variable. If the token env var is not set, skip auth (for local development). If it IS set, reject requests without a matching `Authorization: Bearer <token>` header.

   Note: Check FastMCP's documentation for the correct way to add authentication middleware. FastMCP may have built-in auth support — use it if available rather than writing custom middleware.

3. **Test locally in HTTP mode**:
   ```bash
   export MCP_TRANSPORT=http
   export MCP_PORT=8001
   # Don't set HEALTHSIM_MCP_TOKEN for now (skip auth in local test)
   .venv/bin/python packages/mcp-server/healthsim_mcp.py
   ```

   In another terminal, verify the server responds:
   ```bash
   # Check if the server is running and listing tools
   curl http://localhost:8001/
   ```

   Note: The exact health check endpoint depends on FastMCP's HTTP implementation. Explore what endpoints are available.

4. **Test that stdio still works** — kill the HTTP server, unset MCP_TRANSPORT, and verify that Claude Code can still use the MCP server in its normal stdio mode. This is critical — we must not break the local development workflow.

5. **Git commit**: "feat: add HTTP transport and bearer auth to MCP server"

## Deliverables

- Modified `healthsim_mcp.py` with dual transport support
- Bearer token auth for HTTP mode
- Verified: HTTP mode works locally
- Verified: stdio mode still works for Claude Code
- Committed

## Important

- Do NOT change the MCP server's tool definitions or business logic
- Do NOT change the DuckDB connection — that happens in p0-03
- The server should work identically in both modes — same tools, same behavior, different transport
