# Phase 1 — Data Migration & MCP Server

## Context

Phase 0 validated that MotherDuck, Railway, and the Skills API all work. Phase 1 migrates the full reference dataset to MotherDuck, switches the MCP server to connect to MotherDuck instead of a local DuckDB file, and deploys the production version to Railway.

Run `/clear` between prompts. Run `/compact` mid-prompt only if context exceeds 50%.

## Prompts

| # | File | Title | Effort |
|---|------|-------|--------|
| p1-01 | p1-01-full-migration.md | Full MotherDuck data migration | 45 min |
| p1-02 | p1-02-connection-manager.md | Adapt connection manager for MotherDuck | 30 min |
| p1-03 | p1-03-mcp-motherduck.md | Switch MCP server to MotherDuck | 30 min |
| p1-04 | p1-04-deploy-production.md | Deploy production MCP server to Railway | 30 min |
| p1-05 | p1-05-verify-local.md | Verify local CLI still works | 15 min |

## Prerequisites

- Phase 0 complete and all gate checks passing
- MotherDuck account with sample data from Phase 0
