# p2-04: Adapt Remaining Skills (networksim, common, generation, formats)

## What to build

Adapt the remaining four skills: networksim, common, generation framework, and the bundled format specs.

## Tasks

1. **networksim** — Provider network skill. References NPPES data that now lives in MotherDuck. Replace any local file references with `healthsim_search_providers` and `healthsim_query_reference` MCP tool calls. Add output format section with `provider_network_result` artifact type.

2. **common** — Cross-cutting instructions for DuckDB access patterns, identity correlation, state management. Update DuckDB references to mention MotherDuck as the cloud backend. The identity correlation and state management content stays the same — these are conceptual instructions, not data references. Add output format section noting the common artifact types used across all skills.

3. **generation** — The generative framework skill (profiles, journeys, distributions). This teaches the agent HOW to use the generation MCP tools. Review for any local file path references but this should mostly be conceptual. Add output format section with `generation_progress` and `generation_complete` artifact types.

4. **formats** — The 15 format specification files in `formats/`. Bundle these into a single skill for upload. Create a new `skills/formats/SKILL.md` that:
   - Has a brief introduction ("HealthSim supports these output formats...")
   - References each format spec
   - The supporting .md files from `formats/` become the bundled content

   ```bash
   # Create the skill wrapper
   mkdir -p skills/formats
   # The SKILL.md should reference the format specs
   ```

5. **Test common and generation locally** — these are foundational skills. Verify Claude Code still works correctly with the adapted versions.

6. **Git commit**: "refactor: adapt networksim, common, generation, formats skills for Skills API"

## Deliverables

- All four skills adapted
- `skills/formats/SKILL.md` created as a bundle wrapper
- Tested locally
- Committed
