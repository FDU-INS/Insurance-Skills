# Phase 0 — Managed Agent Validation Spike

## Context

We are migrating HealthSim from a local Claude Code workspace to Anthropic's Managed Agents platform. Phase 0 validates three critical assumptions before we invest further:

1. A FastMCP server can run on Railway with HTTP transport and be reachable by a Managed Agent
2. MotherDuck can serve as the analytical data layer (replacing local DuckDB files)
3. Skills can be uploaded via the Anthropic Skills API and loaded by a Managed Agent

The prompts in this directory are designed to be executed sequentially in Claude Code.
Run `/clear` between prompts. Run `/compact` mid-prompt only if context exceeds 50%.

## Prompts

| # | File | Title | Effort |
|---|------|-------|--------|
| p0-01 | p0-01-scaffold.md | Directory scaffold + env setup | 15 min |
| p0-02 | p0-02-mcp-http.md | MCP server HTTP transport + auth | 30 min |
| p0-03 | p0-03-motherduck.md | MotherDuck migration script (small slice) | 30 min |
| p0-04 | p0-04-deploy-railway.md | Deploy MCP server to Railway | 30 min |
| p0-05 | p0-05-test-skill.md | Upload test skill to Skills API | 20 min |
| p0-06 | p0-06-managed-agent.md | Create Managed Agent + test session | 30 min |

## Prerequisites

- Railway account created and `railway` CLI installed (`brew install railway`)
- MotherDuck account created and token available
- Anthropic API key with Managed Agents beta access
- All tokens/keys stored in a `.env` file at project root (gitignored)

## Gate Check

Phase 0 passes when a Managed Agent session (via Console UI or start-session.py) can:
- Call the Railway-hosted MCP server
- The MCP server can query MotherDuck
- The agent loads the uploaded skill correctly

If any of these fail, debug here. Do not proceed to Phase 1.
