# HealthSim Documentation

Central hub for HealthSim technical documentation. Start here to understand the architecture, find guides, or explore specific topics.

---

## Quick Navigation

| I want to... | Go to |
|--------------|-------|
| **Get started quickly** | [hello-healthsim/](../hello-healthsim/README.md) |
| **Understand the architecture** | [Architecture Guide](#architecture) |
| **Learn how products relate** | [Integration Guide](integration-guide.md) |
| **Understand the database** | [Data Architecture](data-architecture.md) |
| **Create new skills** | [Skills Documentation](#skills-development) |
| **Work with MCP servers** | [MCP Documentation](#mcp-servers) |
| **Contribute to HealthSim** | [Contributing Guide](contributing.md) |

---

## Architecture

Core documents describing how HealthSim is designed and built.

| Document | Description |
|----------|-------------|
| [HEALTHSIM-ARCHITECTURE-GUIDE.md](HEALTHSIM-ARCHITECTURE-GUIDE.md) | **Start here** - Complete architecture overview including products, data flow, skills patterns, and extension points |
| [data-architecture.md](data-architecture.md) | Database schema, state management patterns, and data flow |
| [integration-guide.md](integration-guide.md) | Cross-product integration patterns and entity relationships |
| [healthsim-duckdb-schema.md](healthsim-duckdb-schema.md) | DuckDB table definitions and schema reference |

### Visual Architecture (HTML)

| Document | Description |
|----------|-------------|
| [healthsim-duckdb-architecture.html](healthsim-duckdb-architecture.html) | Interactive diagram of DuckDB unified architecture |

---

## Development

Guides for developing and extending HealthSim.

| Document | Description |
|----------|-------------|
| [HEALTHSIM-DEVELOPMENT-PROCESS.md](HEALTHSIM-DEVELOPMENT-PROCESS.md) | Development workflow, session management, super-prompts |
| [contributing.md](contributing.md) | How to contribute - code style, PR process, testing |
| [testing-patterns.md](testing-patterns.md) | Testing strategies and patterns for HealthSim |

---

## Skills Development

Everything about creating and maintaining HealthSim skills.

| Document | Description |
|----------|-------------|
| [skills-template.md](skills-template.md) | Template for creating new skill files |
| [skills/format-specification-v2.md](skills/format-specification-v2.md) | Current skill file format specification |
| [skills/creating-skills.md](skills/creating-skills.md) | Guide to creating effective skills |
| [skills/migration-guide.md](skills/migration-guide.md) | Migrating skills between format versions |

---

## MCP Servers

Model Context Protocol server documentation.

| Document | Description |
|----------|-------------|
| [mcp/configuration.md](mcp/configuration.md) | MCP server configuration for Claude Desktop/Code |
| [mcp/development-guide.md](mcp/development-guide.md) | Building MCP servers for HealthSim |
| [mcp/integration-guide.md](mcp/integration-guide.md) | Integrating MCP tools with skills |
| [mcp/duckdb-connection-architecture.md](mcp/duckdb-connection-architecture.md) | DuckDB connection patterns for MCP |

---

## Extensions

Guides for extending HealthSim capabilities.

| Document | Description |
|----------|-------------|
| [extensions/philosophy.md](extensions/philosophy.md) | Extension design philosophy |
| [extensions/skills.md](extensions/skills.md) | Adding new domain skills |
| [extensions/mcp-tools.md](extensions/mcp-tools.md) | Adding new MCP tools |
| [extensions/slash-commands.md](extensions/slash-commands.md) | Creating slash commands |
| [extensions/quick-reference.md](extensions/quick-reference.md) | Quick reference for extension patterns |

---

## Active Initiatives

Current development work in progress.

| Initiative | Location | Status |
|------------|----------|--------|
| NetworkSim v2 | [initiatives/networksim-v2/](initiatives/networksim-v2/) | Active |

---

## Archive

Historical documentation preserved for reference. These documents are no longer current but may provide useful context.

**[docs/archive/](archive/)** contains:

| Category | Description |
|----------|-------------|
| [archive/initiatives/](archive/initiatives/) | Completed initiative plans and session logs |
| [archive/planning/](archive/planning/) | Historical planning documents |
| [archive/migration/](archive/migration/) | Past migration guides |
| [archive/audits/](archive/audits/) | Completed audit reports |
| [archive/obsolete/](archive/obsolete/) | Superseded documentation |

---

## Documentation by Product

Each product has its own documentation in the `skills/` directory:

| Product | README | Skill Reference |
|---------|--------|-----------------|
| **PatientSim** | [skills/patientsim/README.md](../skills/patientsim/README.md) | [SKILL.md](../skills/patientsim/SKILL.md) |
| **MemberSim** | [skills/membersim/README.md](../skills/membersim/README.md) | [SKILL.md](../skills/membersim/SKILL.md) |
| **RxMemberSim** | [skills/rxmembersim/README.md](../skills/rxmembersim/README.md) | [SKILL.md](../skills/rxmembersim/SKILL.md) |
| **TrialSim** | [skills/trialsim/README.md](../skills/trialsim/README.md) | [SKILL.md](../skills/trialsim/SKILL.md) |
| **PopulationSim** | [skills/populationsim/README.md](../skills/populationsim/README.md) | [SKILL.md](../skills/populationsim/SKILL.md) |
| **NetworkSim** | [skills/networksim/README.md](../skills/networksim/README.md) | [SKILL.md](../skills/networksim/SKILL.md) |

---

## Output Formats

Format specifications in the `formats/` directory:

| Category | Formats |
|----------|---------|
| **Clinical** | [FHIR R4](../formats/fhir-r4.md), [HL7v2](../formats/hl7v2-adt.md), [C-CDA](../formats/ccda-format.md) |
| **Claims** | [X12 837](../formats/x12-837.md), [X12 835](../formats/x12-835.md), [X12 834](../formats/x12-834.md) |
| **Pharmacy** | [NCPDP D.0](../formats/ncpdp-d0.md) |
| **Clinical Trials** | [CDISC SDTM](../formats/cdisc-sdtm.md), [CDISC ADaM](../formats/cdisc-adam.md) |
| **Analytics** | [Dimensional/Star Schema](../formats/dimensional-analytics.md), [CSV](../formats/csv.md) |

---

*HealthSim generates synthetic test data only. Never use for actual patient care or real PHI.*
