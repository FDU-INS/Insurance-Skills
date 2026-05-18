# p2-02: Adapt populationsim Skill (Hardest First)

## What to build

Adapt the populationsim skill for the Skills API. This is the most complex adaptation because it has embedded CSV data files that need to be replaced with MCP tool references.

## Context

The populationsim skill directory contains large embedded CSV files (CDC PLACES, SVI, FIPS crosswalks) that the agent currently reads directly from the filesystem. In the Managed Agent environment, the agent won't have these files — the data lives in MotherDuck, accessible via the `healthsim_query_reference` MCP tool.

## Tasks

1. **Read the current skill structure**:
   ```bash
   find skills/populationsim/ -type f | head -30
   cat skills/populationsim/SKILL.md
   ```

2. **Identify all embedded data references** in the SKILL.md and supporting files. Look for:
   - File paths referencing CSV files
   - Instructions to "read from" or "load" local files
   - Inline data tables
   - Any `skills/populationsim/data/` references

3. **Replace each embedded data reference** with an MCP tool instruction. The pattern:

   **Before** (references local file):
   ```
   Load county-level health data from skills/populationsim/data/county/cdc_places.csv
   ```

   **After** (references MCP tool):
   ```
   Query county-level health data using the healthsim_query_reference tool:
   Tool: healthsim_query_reference
   Query: SELECT * FROM reference.cdc_places WHERE state = '{state}' AND county = '{county}'
   ```

4. **Add an Output Formats section** at the end of the SKILL.md:
   ```markdown
   ## Output Formats

   When generating population data, emit structured output as JSON artifact descriptors
   that the visualization layer can render:

   ### Population Summary
   {
     "artifact_type": "population_config",
     "data": {
       "total_members": 500,
       "geography": "San Diego County, CA",
       "demographics": {...},
       "health_indicators": {...}
     }
   }
   ```

5. **Test the adapted skill locally** — open Claude Code and ask it to generate a population using the adapted skill. Verify the skill works correctly with MCP tool references instead of file references.

6. **Do NOT delete the data files** — they're gitignored anyway and may still be useful for local reference. The skill just doesn't reference them anymore.

7. **Git commit**: "refactor: adapt populationsim skill for Skills API — MCP tool references"

## Deliverables

- Adapted `skills/populationsim/SKILL.md` and supporting files
- All embedded data references replaced with MCP tool calls
- Output format section added
- Tested locally in Claude Code
- Committed
