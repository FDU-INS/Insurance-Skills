# Extension Quick Reference

Single-page reference for extending HealthSim products.

## Decision Tree

```
What capability do you want to add?
│
├─ Claude needs to DO something new → MCP Tool (mcp-tools.md)
│  Examples: Calculate score, compare patients, transform data
│
├─ Claude needs to KNOW something new → Skill (skills.md)
│  Examples: Clinical domain, cohort pattern, format details
│
├─ Shortcut for common action → Slash Command (slash-commands.md)
│  Examples: Quick generation, batch export, workflow automation
│
├─ New output format → Export Format
│  Examples: CDA, X12, OMOP, EHR-specific formats
│
└─ New patient data type → Core Model
   Examples: Allergy, Immunization, Family History, Social Determinants
```

## Universal Rule

> **Every extension starts with: "What conversation does this enable?"**

Design the conversation first, then implement the code to support it.

## Quick Prompt Templates

| Extension | Start With |
|-----------|------------|
| **MCP Tool** | "Add [tool_name] to src/*/mcp/[server].py enabling: '[what users will say]'. The tool should [action]. Response format: conversational summary with [key elements]." |
| **Skill** | "Create [domain/cohort] skill at skills/[type]/[name].md for: '[what users will say]'. Include: domain knowledge, generation guidelines, examples." |
| **Slash Command** | "Add /[cmd] to .claude/commands/[cmd].md that expands: '[full prompt expansion]'. Arguments: [list]. Example: /[cmd] [example]." |
| **Export Format** | "Add [FORMAT] export to src/*/formats/[format]/ enabling: 'Export to [FORMAT]'. Include: transformer, validator, MCP tool, skill, tests." |
| **Core Model** | "Add [Model] to src/*/core/models.py for: '[what users will say]'. Include: model definition, generation, skills update, exports, validation." |

## File Locations

| What | Where |
|------|-------|
| **MCP Servers** | `src/*/mcp/*.py` |
| **Skills** | `skills/[category]/*.md` |
| **Slash Commands** | `.claude/commands/*.md` |
| **Export Formats** | `src/*/formats/[format]/` |
| **Core Models** | `src/*/core/models.py` |
| **Generators** | `src/*/core/generator.py` |
| **Validation** | `src/*/validation/` |
| **Tests** | `tests/` (mirror src structure) |
| **Examples** | `examples/conversations/` |
| **User Docs** | `docs/user-guide/` |
| **Developer Docs** | `docs/developer-guide/` |

## Extension Type Cheat Sheet

### MCP Tools

**When:** Claude needs to perform action requiring code execution

**Quick Check:**
- Does it calculate something? → Tool
- Does it transform data? → Tool
- Does it require state? → Tool
- Is it just knowledge? → Not a tool

**Files to create/modify:**
- `src/*/mcp/[server].py` - Add tool definition and handler
- `tests/mcp/test_[server].py` - Add tests
- `.claude/project-instructions.md` - Document tool (optional)

**Response format:** Conversational summary (NOT data dump)

**See:** [mcp-tools.md](mcp-tools.md)

### Skills

**When:** Claude needs clinical/domain knowledge

**Quick Check:**
- Does it teach Claude something? → Skill
- Is it clinical guidelines? → Skill
- Is it generation pattern? → Skill
- Does it need code execution? → Not a skill

**Files to create/modify:**
- `skills/[category]/[name].md` - Create skill file
- Add to Claude Project knowledge

**Structure:** For Claude → When to Use → Domain Knowledge → Generation Guidelines → Examples

**See:** [skills.md](skills.md)

### Slash Commands

**When:** Users frequently perform same action

**Quick Check:**
- Is it repetitive? → Command
- Is it multi-step? → Command
- Is it rare? → Not a command
- Does it need explanation? → Not a command

**Files to create/modify:**
- `.claude/commands/[cmd].md` - Create command file
- `.claude/commands/README.md` - Document command

**Format:** Command maps to expanded prompt

**See:** [slash-commands.md](slash-commands.md)

### Export Formats

**When:** Users need data in healthcare standard

**Quick Check:**
- Is it industry standard? → Format
- Is it for EHR integration? → Format
- Is it one-off custom? → Not a format
- Is it just field selection? → Not a format

**Files to create/modify:**
- `src/*/formats/[format]/transformer.py` - Transformation logic
- `src/*/formats/[format]/validator.py` - Validation logic
- `src/*/mcp/export_server.py` - Add MCP tool
- `skills/formats/[format]-format.md` - Create skill
- `tests/formats/test_[format].py` - Add tests
- `examples/exports/[format]/` - Add examples

### Core Models

**When:** Users need new type of patient data

**Quick Check:**
- Is it reusable data type? → Model
- Does it have structure? → Model
- Is it temporary calculated value? → Not a model
- Is it simple annotation? → Not a model

**Files to create/modify:**
- `src/*/core/models.py` - Add model class
- `src/*/core/generator.py` - Add generation
- `skills/healthcare/clinical-domain.md` - Update skill
- `src/*/mcp/generation_server.py` - Update responses
- `src/*/formats/*/` - Update all exports
- `src/*/validation/clinical.py` - Add validation
- `tests/core/test_[model].py` - Add tests

## Copy-Paste Prompts

### Add MCP Tool (Basic)

```
Add MCP tool to HealthSim:

**Purpose:** [What users will say]

**Example:**
User: "[request]"
Claude: [calls tool, shows conversational response]

**Tool Details:**
- Name: [tool_name]
- Server: [generation/export/validation]_server.py
- Parameters:
  - [param]: [type] - [description]

**Response:** [Conversational format description]
```

### Add Skill (Basic)

```
Create [domain/cohort] skill:

**Purpose:** Enable "[what users will say]"

**Knowledge:**
- [Key concept 1]
- [Key concept 2]
- [Key concept 3]

**File:** skills/[category]/[name].md

**Structure:** Follow skills/SKILL_TEMPLATE_V2.md
```

### Add Slash Command (Basic)

```
Add slash command:

**Command:** /[name]

**Purpose:** [What it shortcuts]

**Usage:** /[name] [args]

**Expansion:** "[full prompt]"

**File:** .claude/commands/[name].md
```

### Add Export Format (Basic)

```
Add [FORMAT] export:

**Purpose:** Enable "Export to [FORMAT]"

**Use case:** [Primary use case]

**Components:**
- Transformer: src/*/formats/[format]/transformer.py
- Validator: src/*/formats/[format]/validator.py
- MCP tool: export_[format] in export_server.py
- Skill: skills/formats/[format]-format.md
- Tests: tests/formats/test_[format].py
```

### Add Core Model (Basic)

```
Add [Model] to core:

**Purpose:** Enable "[what users will say]"

**Fields:**
- [field1]: [type] - [description]
- [field2]: [type] - [description]

**Components:**
- Model: src/*/core/models.py
- Generation: src/*/core/generator.py
- Skills: Update clinical-domain.md
- Exports: Update FHIR, HL7v2, MIMIC
- Validation: src/*/validation/clinical.py
- Tests: tests/core/test_[model].py
```

## Testing Checklist

For any extension:

- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Manual test with Claude successful
- [ ] Example conversation works
- [ ] Coverage ≥90%
- [ ] Error cases handled
- [ ] Edge cases covered

## Documentation Checklist

For any extension:

- [ ] Code documented (docstrings)
- [ ] User guide updated (if user-facing)
- [ ] Developer guide updated (if API change)
- [ ] Example added to examples/
- [ ] README updated (if major feature)
- [ ] CHANGELOG updated

## Quality Checklist

For any extension:

- [ ] Code formatted (black)
- [ ] Linting passed (ruff)
- [ ] Type checking passed (mypy)
- [ ] All tests passing
- [ ] No security vulnerabilities
- [ ] Performance acceptable

## Common Patterns

### Pattern: Conversational Response

**Bad (Data Dump):**
```python
return json.dumps({"result": data})
```

**Good (Conversational):**
```python
response = f"**Summary**\n\n"
response += f"Found {len(results)} items:\n"
for item in results[:3]:
    response += f"- {item.name}: {item.description}\n"
response += f"\n**Next Steps:**\n- [Action 1]\n- [Action 2]\n"
return response
```

### Pattern: Parameter Validation

```python
if not required_param:
    return error_response("❌ Missing required parameter: [param]")

if param not in valid_values:
    return error_response(f"❌ Invalid [param]: {param}. Must be one of: {valid_values}")
```

### Pattern: Session State Access

```python
# Get from session
item = session_state["items"].get(item_id)
if not item:
    return error_response(f"❌ Item {item_id} not found. Generate first.")

# Modify session
session_state["items"][item_id] = modified_item
```

### Pattern: Seed-Based Generation

```python
# Always use self._random for reproducibility
value = self._random.choice(options)
number = self._random.randint(min_val, max_val)
float_val = self._random.uniform(min_val, max_val)
```

## Workflow Summary

1. **Design conversation** - What will users say?
2. **Identify extension type** - Tool/Skill/Command/Format/Model?
3. **Use prompt template** - Copy-paste quick start
4. **Implement code** - Follow existing patterns
5. **Write tests** - ≥90% coverage
6. **Document** - Docs and examples
7. **Test with Claude** - Verify conversation works
8. **Submit** - Create PR with checklist

## Getting Help

**Before asking:**
- Check existing implementations in respective directories
- Review relevant guide (mcp-tools.md, skills.md, etc.)
- Try the conversation-first approach

**Where to ask:**
- GitHub Discussions for questions
- GitHub Issues for bugs
- Code review on PRs

## See Full Guides

- **[Extension Philosophy](philosophy.md)** - Conversation-first approach
- **[MCP Tools](mcp-tools.md)** - Adding actions
- **[Skills](skills.md)** - Adding knowledge
- **[Slash Commands](slash-commands.md)** - Adding shortcuts

---

**Remember:** Every extension enables a new conversation. If you can't articulate what users will say, refine your design before coding.
