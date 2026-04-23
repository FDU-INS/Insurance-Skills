# Phase 3 — Agent Assembly & Validation

## Context

Phase 2 uploaded all 9 skills to the Skills API. Phase 3 wires everything together: converts the CLAUDE.md to a Managed Agent system prompt, builds the remaining deploy scripts, creates the full agent definition, and validates end-to-end.

At the end of Phase 3, HealthSim runs as a fully functional Managed Agent.

Run `/clear` between prompts. Run `/compact` mid-prompt only if context exceeds 50%.

## Prompts

| # | File | Title | Effort |
|---|------|-------|--------|
| p3-01 | p3-01-system-prompt.md | Convert CLAUDE.md to Managed Agent system prompt | 30 min |
| p3-02 | p3-02-deploy-scripts.md | Build push-agent.py and push-environment.py | 30 min |
| p3-03 | p3-03-deploy-agent.md | Deploy the full agent and start session | 20 min |
| p3-04 | p3-04-validate.md | Run full validation checklist | 30 min |
| p3-05 | p3-05-update-session-cli.md | Update start-session.py for production agent | 20 min |

## Prerequisites

- Phase 2 complete — all skills uploaded, skill-ids.json populated
- Railway MCP server running with MotherDuck backend
