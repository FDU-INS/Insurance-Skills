# p1-04: Deploy Production MCP Server to Railway

## What to build

Update the Railway deployment to connect to MotherDuck instead of bundling a local DuckDB file. This is the production deployment — smaller container, cloud data, ready for the Managed Agent.

## Context

The Phase 0 deployment bundled the DuckDB file inside the Docker container. Now that the MCP server connects to MotherDuck, we can remove the DuckDB file from the container entirely. This makes the container much smaller and the deployment faster.

## Tasks

1. **Update the Dockerfile**:
   - Remove the `COPY healthsim_current.duckdb` line
   - Remove any `HEALTHSIM_DB_PATH` env var
   - Add `MOTHERDUCK_TOKEN` as a required env var (set via Railway dashboard, not in the Dockerfile)
   - Keep everything else the same

2. **Rebuild and test locally**:
   ```bash
   docker build -t healthsim-mcp .
   docker run -p 8001:8001 \
     -e HEALTHSIM_MCP_TOKEN=test-token \
     -e MOTHERDUCK_TOKEN=<your-token> \
     -e MCP_TRANSPORT=http \
     healthsim-mcp
   ```
   
   Run `scripts/test_mcp_motherduck.py` against the containerized server to verify.

3. **Deploy to Railway**:
   ```bash
   railway up
   ```
   
   Set/update environment variables in Railway:
   - `MOTHERDUCK_TOKEN` — your MotherDuck token
   - `HEALTHSIM_MCP_TOKEN` — same bearer token as Phase 0
   - `MCP_TRANSPORT=http`
   - `MCP_PORT=8001`

4. **Verify Railway deployment**:
   - Check the Railway logs for startup success
   - Run `scripts/test_mcp_motherduck.py` pointed at the Railway URL instead of localhost
   - Verify provider search returns full NPPES data (not just the 1,000-row sample)

5. **Update `deploy/railway-url.txt`** if the URL changed.

6. **Git commit**: "feat: production Railway deployment with MotherDuck backend"

## Deliverables

- Updated Dockerfile (no bundled DuckDB)
- Railway deployment updated and verified
- All tools working against MotherDuck via Railway
- Committed
