FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    "mcp>=1.0.0" \
    "duckdb>=0.9.0,<1.5.2" \
    "pydantic>=2.0.0" \
    "pydantic-settings>=2.0.0" \
    "uvicorn>=0.30.0" \
    "starlette>=0.40.0" \
    "anyio>=3.5.0"

# Copy healthsim core library
COPY packages/core/src/healthsim/ /app/healthsim/

# Replace __init__.py with minimal version for MCP server
# The full __init__.py eagerly imports all submodules (generation, skills,
# benefits, dimensional) which pull in heavy deps not needed by the server.
# The MCP server only needs healthsim.db and healthsim.state.
RUN echo '__version__ = "1.0.0"' > /app/healthsim/__init__.py

# Copy MCP server
COPY packages/mcp-server/healthsim_mcp.py /app/

# Set Python path so healthsim imports resolve
ENV PYTHONPATH=/app

# MCP server configuration — connects to MotherDuck (no local DB needed)
# MOTHERDUCK_TOKEN and HEALTHSIM_MCP_TOKEN are set via Railway env vars
ENV MCP_TRANSPORT=http
# Railway sets PORT automatically; MCP_PORT falls back to 8000 if unset
# HEALTHSIM_DB_PATH must be set at runtime: md:healthsim_ref?motherduck_token=<token>

CMD ["python", "healthsim_mcp.py"]
