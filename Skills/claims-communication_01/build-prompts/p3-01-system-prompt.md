# p3-01: Convert CLAUDE.md to Managed Agent System Prompt

## What to build

Create a Managed Agent system prompt derived from the existing `.claude/CLAUDE.md`. The system prompt needs to work in a cloud container context (MotherDuck, HTTP MCP tools) rather than a local Claude Code context (local files, stdio MCP).

## Context

The current CLAUDE.md contains instructions specific to the local Claude Code environment: local file paths, DuckDB file locations, stdio MCP server references, Claude Code-specific commands. The Managed Agent system prompt needs to convey the same domain knowledge and behavioral instructions but reference the cloud infrastructure instead.

## Tasks

1. **Read the current CLAUDE.md**:
   ```bash
   cat .claude/CLAUDE.md
   ```

2. **Create `deploy/system-prompt.md`** — the Managed Agent system prompt. Adapt from CLAUDE.md with these changes:

   a. **Remove Claude Code-specific references**: local file paths, `/init` commands, `.venv` references, git workflow instructions
   
   b. **Update data access instructions**: Replace "query the local DuckDB" with "use the healthsim MCP tools to query reference data and manage cohorts"
   
   c. **Update MCP tool references**: The tools are the same, but they're accessed via HTTP now. The agent doesn't need to know this — just reference tools by name as before
   
   d. **Keep all domain knowledge**: Healthcare domain expertise, generation patterns, data quality rules, PHI safety rules, format specifications — all of this transfers directly
   
   e. **Keep the personality and behavioral instructions**: How to interact with users, how to present results, safety guardrails
   
   f. **Add Managed Agent context**: Note that the agent runs in a cloud container with Python, pandas, and DuckDB available for computation. Outputs can be files (CSV, JSON) or structured artifact descriptors for the visualization layer.

3. **Keep the system prompt under 8,000 tokens** if possible. Managed Agents have built-in compaction, but a shorter system prompt means more room for conversation context. If the current CLAUDE.md is very long, prioritize: domain knowledge > behavioral instructions > formatting preferences.

4. **Review the result**: Read through the system prompt and verify it makes sense for a cloud-hosted agent that a user interacts with via chat (not a developer working in a terminal).

5. **Git commit**: "feat: create Managed Agent system prompt from CLAUDE.md"

## Deliverables

- `deploy/system-prompt.md` — production system prompt
- Adapted for cloud context (MotherDuck, HTTP MCP)
- Domain knowledge preserved
- Committed

## Important

- The original `.claude/CLAUDE.md` stays unchanged — it's still used for local development
- The system prompt is a separate file that `push-agent.py` reads when creating the agent definition
- Update `agent-config.yaml` to reference this new file: `system_prompt_source: ./deploy/system-prompt.md`
