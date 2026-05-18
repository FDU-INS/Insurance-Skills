# p0-04: Deploy MCP Server to Railway

## What to build

Containerize the HealthSim MCP server and deploy it to Railway. For Phase 0, the server will still connect to the LOCAL DuckDB file bundled in the container (not MotherDuck yet — that switch happens in Phase 1). The goal is to prove Railway deployment and HTTP reachability.

## Context

The MCP server now supports HTTP transport (from p0-02). We need to deploy it somewhere reachable by Anthropic's Managed Agents infrastructure. Railway provides Docker-native deployment with persistent volumes.

For the Phase 0 spike, we'll deploy a minimal version: the MCP server + its dependencies + a copy of the DuckDB file. This validates the deployment pipeline. In Phase 1, we'll switch the server to connect to MotherDuck instead.

## Tasks

1. **Create a `Dockerfile`** at the project root:
   - Base image: `python:3.11-slim`
   - Copy the necessary packages: `packages/mcp-server/`, `packages/core/src/healthsim/` (the server imports from healthsim modules)
   - Copy the DuckDB file: `healthsim_current.duckdb`
   - Install dependencies: `fastmcp`, `duckdb`, `pydantic`, plus any other imports the server needs
   - Set environment variables: `MCP_TRANSPORT=http`, `MCP_PORT=8001`
   - Expose port 8001
   - CMD to run the server

   **Important**: Read the MCP server's imports first to understand what modules it needs. Run:
   ```bash
   grep -r "^import\|^from" packages/mcp-server/healthsim_mcp.py
   ```
   Then trace those imports to figure out the minimum set of files to copy.

   Also read `packages/mcp-server/pyproject.toml` for declared dependencies.

2. **Create a `.dockerignore`** to exclude `.venv`, `.git`, `__pycache__`, `.pytest_cache`, etc.

3. **Test the Docker build locally**:
   ```bash
   docker build -t healthsim-mcp .
   docker run -p 8001:8001 -e HEALTHSIM_MCP_TOKEN=test-token healthsim-mcp
   ```
   
   In another terminal:
   ```bash
   curl http://localhost:8001/  # verify server responds
   ```

4. **Deploy to Railway**:
   ```bash
   railway login
   railway init  # or link to existing project
   railway up
   ```

   Set environment variables in Railway dashboard or CLI:
   - `HEALTHSIM_MCP_TOKEN` — generate a random token (e.g., `openssl rand -hex 32`)
   - `MCP_TRANSPORT=http`
   - `MCP_PORT=8001`

5. **Verify the Railway deployment**:
   ```bash
   # Get the Railway URL (something like https://healthsim-mcp-production-xxxx.up.railway.app)
   curl https://<your-railway-url>/
   ```

6. **Record the Railway URL** — you'll need it in p0-06 when creating the Managed Agent. Write it to `deploy/railway-url.txt` (gitignored).

7. **Git commit**: "feat: add Dockerfile and Railway deployment for MCP server"

## Deliverables

- `Dockerfile` at project root
- `.dockerignore`
- MCP server deployed and responding on Railway
- Railway URL recorded
- Committed

## Notes

- The Railway deployment will include a copy of the DuckDB file. This is temporary — in Phase 1, the server will connect to MotherDuck instead, and the DuckDB file won't be needed in the container.
- The DuckDB file is ~500MB+ (NPPES data). If this is too large for Railway's free tier, create a stripped-down version with only a sample of the data for Phase 0. The full migration happens in Phase 1.
- Add `deploy/railway-url.txt` to `.gitignore`.
