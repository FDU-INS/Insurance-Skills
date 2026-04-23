# Extending HealthSim

**Complete guide to adding new capabilities to HealthSim products using the conversation-first philosophy.**

---

## Quick Start

**Every extension starts with one question:**

> **"What new conversation does this enable?"**

Before writing any code, design the conversation you want users to have.

---

## Choose Your Extension Type

### [MCP Tools](mcp-tools.md) - Add New Actions

**Use when:** Claude needs to DO something requiring code execution

**Examples:**
- Calculate clinical scores (SOFA, HEART, CHADS2)
- Compare multiple patients
- Transform or analyze data
- Perform complex operations

**Quick Add:**
```
User: "Compare these two patients"
→ Need MCP tool to perform comparison
```

[Full MCP Tools Guide](mcp-tools.md)

---

### [Skills](skills.md) - Add New Knowledge

**Use when:** Claude needs to KNOW about a clinical domain or cohort

**Examples:**
- New clinical specialties (nephrology, neurology)
- New cohorts (sepsis, stroke, pregnancy)
- Clinical guidelines and protocols
- Healthcare format knowledge

**Quick Add:**
```
User: "Generate a stroke patient eligible for tPA"
→ Need skill teaching stroke management
```

[Full Skills Guide](skills.md)

---

### [Slash Commands](slash-commands.md) - Add Shortcuts

**Use when:** Users frequently perform the same action

**Examples:**
- `/generate diabetes --count 10 --hba1c >9`
- `/export fhir --validate`
- `/workflow test-cohort`

**Quick Add:**
```
Users often say: "Generate 10 diabetic patients with HbA1c >9%"
→ Add /generate command for quick access
```

[Full Slash Commands Guide](slash-commands.md)

---

### Export Formats - Add New Standards

**Use when:** Users need data in a new healthcare standard or format

**Examples:**
- CDA (Clinical Document Architecture)
- X12 (Healthcare claims)
- OMOP CDM (Research databases)
- EHR-specific formats

**Quick Add:**
```
User: "Export to CDA format"
→ Need transformer, validator, MCP tool, skill
```

---

### Core Models - Add New Data Types

**Use when:** Users need to work with new patient data that doesn't exist

**Examples:**
- Allergies
- Immunizations
- Family history
- Social determinants of health

**Quick Add:**
```
User: "Generate patient with allergy information"
→ Need Allergy model, generation, exports
```

---

## Quick Reference

**[Extension Quick Reference](quick-reference.md)** - Single-page lookup for all extension types

### Decision Tree

```
What capability do you want to add?
│
├─ Claude needs to DO something → MCP Tool
├─ Claude needs to KNOW something → Skill
├─ Shortcut for common action → Slash Command
├─ New output format → Export Format
└─ New patient data type → Core Model
```

### Quick Prompts

| Extension | Quick Prompt Template |
|-----------|----------------------|
| **MCP Tool** | "Add [tool] to enable: '[user request]'. Response: [conversational format]" |
| **Skill** | "Create [domain] skill for: '[user request]'. Include: knowledge, guidelines, examples" |
| **Slash Command** | "Add /[cmd] that expands to: '[prompt]'. Args: [list]" |
| **Export Format** | "Add [FORMAT] export for: 'Export to [FORMAT]'. Include: transformer, validator, tool, skill" |
| **Core Model** | "Add [Model] for: '[user request]'. Include: model, generation, exports, validation" |

---

## Extension Philosophy

### Conversation-First Development

HealthSim is a **conversational system first**. Every extension should enhance what users can say and do through natural language.

**Don't think:** "I'll add a Python function to generate X"

**Do think:** "What should users be able to say to generate X?"

### Design Questions

Before building any extension, ask:

1. **What new conversations does this enable?**
   - What can users say after this extension?
   - Show me an example dialogue

2. **Does it enhance the conversational experience?**
   - Makes requests clearer?
   - Provides better responses?
   - Enables new use cases?

3. **Is the conversational interface natural?**
   - Would a clinician say this?
   - Is it intuitive?
   - Does it match domain language?

### Response Quality

All MCP tools must return **conversational responses**, not data dumps:

**Bad (Data Dump):**
```json
{"patients": [...], "stats": {...}}
```

**Good (Conversational):**
```
**Comparison Results**

Found 3 key differences between these patients:
- Age: 64 vs 68 (4 year difference)
- HbA1c: 7.2% vs 9.1% (significant control difference)
- Medications: Patient 2 is on insulin while Patient 1 uses oral agents

**Clinical Implications:**
The control difference suggests different disease progression...

**Next Steps:**
- Review medication regimens
- Consider treatment adjustments
```

---

## Extension Workflow

### 1. Design the Conversation

**Before writing code**, design the complete user experience:

```markdown
User: "Generate a stroke patient eligible for tPA"

Claude: "I'll generate an acute ischemic stroke patient meeting tPA eligibility:

**Generated Patient: Linda Martinez, 67F, MRN-847293**

**Presentation:**
- Symptom onset: 2 hours ago
- Arrival: Within 4.5h window ✓
- NIH Stroke Scale: 12 (moderate severity)

**tPA Eligibility:**
✓ Within treatment window
✓ No hemorrhage on CT
✓ No contraindications
✓ BP controlled

**Decision: tPA ELIGIBLE**"
```

### 2. Identify What Claude Needs

**Knowledge (Skill):**
- Stroke types and presentations
- NIH Stroke Scale scoring
- tPA eligibility criteria
- Timing windows and contraindications

**Actions (MCP Tool):**
- Calculate stroke severity scores?
- Check eligibility criteria?
- Generate time-based cohorts?

### 3. Implement Backend Support

Write the Python code to support the conversation:

```python
# src/product/core/stroke.py

def calculate_nihss_score(symptoms: dict) -> int:
    """Calculate NIH Stroke Scale score."""
    # Implementation

def check_tpa_eligibility(patient: Patient, onset: datetime) -> dict:
    """Check tPA eligibility criteria."""
    # Implementation
```

### 4. Update Configuration

**Skills:** Add domain knowledge
**MCP Tools:** Register new tools
**Project Instructions:** Update if needed

### 5. Write Example Conversation

Show the extension in action with a complete conversation example.

### 6. Test with Claude

Actually test the conversation works as designed!

---

## Extension Impact Matrix

Understanding what changes when you add each extension type:

| Extension Type | Claude Learns | MCP Changes | Config Changes | Docs Needed |
|----------------|---------------|-------------|----------------|-------------|
| **MCP Tool** | How to use it | New function | Register tool | Tool reference, example |
| **Skill** | Domain knowledge | None | Add to Project | Skill markdown, usage |
| **Cohort** | Pattern to apply | Uses existing | Skill file | Conversation example |
| **Slash Command** | Command mapping | None | Command def | User guide section |
| **Export Format** | Format details | Export function | Format list | Format reference |
| **Core Model** | Data structure | Response format | None | Model docs, API ref |
| **Validation Rule** | Quality criteria | Validation tool | None | Rule explanation |

---

## Best Practices

### 1. Start with Conversation

Write the example conversation BEFORE implementing code.

### 2. Prefer Skills Over Code

If Claude just needs knowledge, add a skill instead of an MCP tool.

### 3. Test with Claude

After implementing, actually test the conversation works as designed.

### 4. Document Conversationally

Write docs in terms of conversations, not just code.

### 5. Follow Existing Patterns

Look at existing implementations in:
- `src/*/mcp/` for MCP tool patterns
- `skills/` for skill examples
- Product documentation for detailed guides

---

## Extension Checklist

When adding any extension:

- [ ] Designed conversation first
- [ ] Identified extension type correctly
- [ ] Implemented conversational responses (not data dumps)
- [ ] Updated relevant configuration
- [ ] Wrote tests (≥90% coverage)
- [ ] Created example conversation
- [ ] Documented in relevant guide
- [ ] Tested with Claude
- [ ] Code formatted and linted
- [ ] All tests passing

---

## Ready to Extend?

1. **Choose your extension type** from the list above
2. **Read the detailed guide** for that type
3. **Use the quick prompt template** to plan your extension
4. **Follow the conversation-first workflow**
5. **Test with Claude to verify it works**

**Remember:** Every extension should answer the question:

> **"What new conversations does this enable for users?"**

If you can't articulate the conversation, the extension isn't ready yet.

---

## See Also

- **[MCP Tools Guide](mcp-tools.md)** - Adding actions
- **[Skills Guide](skills.md)** - Adding knowledge
- **[Slash Commands Guide](slash-commands.md)** - Adding shortcuts
- **[Quick Reference](quick-reference.md)** - Fast lookup
- **[Architecture](../HEALTHSIM-ARCHITECTURE-GUIDE.md)** - System design
- **[Contributing](../contributing.md)** - Development standards

---

**Questions?** Check the detailed extension guides or ask in GitHub Discussions!
