# Adding MCP Tools

Guide to creating new MCP tools that give Claude new capabilities.

## When to Add an MCP Tool

Add an MCP tool when **Claude needs to DO something** that requires code execution.

### Good Reasons to Add MCP Tool

**Performing calculations**
```
User: "Calculate SOFA score for this ICU patient"
→ Need calculate_sofa_score() tool
```

**Data transformations**
```
User: "Compare these two patients and show me the differences"
→ Need compare_patients() tool
```

**Complex operations**
```
User: "Generate a cohort with specific distribution criteria"
→ Need generate_cohort() tool with advanced parameters
```

**Stateful operations**
```
User: "Modify patient MRN-12345 to add diabetic retinopathy"
→ Need modify_patient() tool that updates session state
```

### Bad Reasons to Add MCP Tool

**Claude just needs knowledge**
```
User: "Generate a septic patient"
→ Don't need tool, just add sepsis skill with clinical knowledge
```

**Simple parameter passing**
```
User: "Generate patient aged 65-70"
→ Don't need tool, existing generate_patient() handles this
```

**Just formatting responses**
```
User: "Show me this patient's medications in a table"
→ Don't need tool, Claude can format responses
```

## MCP Tool Anatomy

### Basic Structure

```python
from mcp.server import Server
from mcp.types import TextContent

server = Server("your-server-name")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="your_tool_name",
            description="What this tool does (Claude sees this)",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "What this parameter means"
                    }
                },
                "required": ["param1"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "your_tool_name":
        result = your_implementation(arguments)

        # Return conversational response
        return [TextContent(
            type="text",
            text=format_conversational_response(result)
        )]
```

### Tool Description Guidelines

The `description` field is what Claude uses to decide when to call your tool.

**Good descriptions:**
```python
Tool(
    name="calculate_sofa_score",
    description="Calculate Sequential Organ Failure Assessment (SOFA) score for ICU patients based on lab values and vital signs. Use when asked to calculate organ dysfunction severity."
)
```

**Bad descriptions:**
```python
Tool(
    name="calculate_sofa_score",
    description="Calculates SOFA"  # Too vague
)
```

## Tool Response Design (CRITICAL)

**The most common mistake when adding MCP tools is returning data dumps instead of conversational responses.**

### The Problem with Data Dumps

**Bad Response (Data Dump):**
```python
return [TextContent(
    type="text",
    text=json.dumps({
        "patients": [
            {"mrn": "MRN-123", "age": 65, "conditions": [...]},
            {"mrn": "MRN-456", "age": 72, "conditions": [...]}
        ],
        "stats": {
            "total": 2,
            "avg_age": 68.5
        }
    })
)]
```

**Why this is bad:**
- Claude sees raw JSON and has to parse it
- User sees ugly JSON if Claude passes it through
- Loses conversational flow
- Doesn't highlight key insights

### Conversational Response Design

**Good Response (Conversational):**
```python
def format_comparison_response(patient1: Patient, patient2: Patient, diffs: dict) -> str:
    """Format comparison as conversational summary."""

    response = f"**Comparing Patients: {patient1.mrn} vs {patient2.mrn}**\n\n"

    # Lead with key insights
    if len(diffs) == 0:
        response += "These patients are clinically identical.\n"
    else:
        response += f"Found {len(diffs)} key differences:\n\n"

    # Summarize important differences
    if "age_difference" in diffs:
        response += f"- **Age:** {patient1.age} vs {patient2.age} ({diffs['age_difference']} year difference)\n"

    if "medication_differences" in diffs:
        p1_only = diffs["medication_differences"]["patient1_only"]
        p2_only = diffs["medication_differences"]["patient2_only"]

        if p1_only:
            response += f"\n**Medications only in {patient1.mrn}:**\n"
            for med in p1_only:
                response += f"  - {med}\n"

        if p2_only:
            response += f"\n**Medications only in {patient2.mrn}:**\n"
            for med in p2_only:
                response += f"  - {med}\n"

    # Add clinical interpretation
    response += "\n**Clinical Notes:**\n"
    if diffs.get("severity_difference"):
        response += f"- Patient {diffs['more_severe_patient']} has more severe disease burden\n"

    # Suggest next actions
    response += "\n**Suggested Actions:**\n"
    response += "- Review medication regimens for standardization opportunities\n"
    response += "- Consider clinical trial eligibility differences\n"

    return response
```

### Response Design Principles

**1. Lead with the answer, not the data**

Bad:
```
Patient data: {...}
Comparison results: {...}
```

Good:
```
These two diabetic patients differ primarily in disease control.
Patient MRN-123 has well-controlled diabetes (HbA1c 6.8%) while
Patient MRN-456 shows poor control (HbA1c 9.2%)...
```

**2. Summarize, don't dump**

Bad:
```json
{"labs": [{"name": "glucose", "value": 145}, {"name": "hba1c", "value": 8.2}, ...]}
```

Good:
```
Lab results show moderate glycemic control:
- Fasting glucose: 145 mg/dL (elevated)
- HbA1c: 8.2% (above target of <7%)
- Lipid panel: Within normal limits
```

**3. Use formatting for readability**

```python
# Use markdown formatting
response = "**Section Title**\n\n"
response += "- Bullet point 1\n"
response += "- Bullet point 2\n\n"
response += "**Another Section**\n"
```

**4. Include counts and statistics when relevant**

```python
response = f"Generated {len(patients)} patients:\n"
response += f"- Average age: {avg_age:.1f} years\n"
response += f"- {female_count} female ({female_pct:.0f}%), {male_count} male ({male_pct:.0f}%)\n"
```

**5. Provide clinical context**

```python
if hba1c > 9.0:
    response += "\n⚠️  HbA1c >9% indicates poor glycemic control. Consider treatment intensification.\n"
```

**6. Suggest next actions**

```python
response += "\n**Next Steps:**\n"
response += "- Export to FHIR for EHR integration\n"
response += "- Run validation checks\n"
response += "- Generate additional patients if needed\n"
```

## Adding a Tool: Step by Step

### Step 1: Identify the Server

HealthSim products typically have three MCP servers:

- **generation_server.py** - Patient/entity generation and modification
- **export_server.py** - Format export and transformation
- **validation_server.py** - Quality and compliance checks

Choose the server that matches your tool's purpose.

### Step 2: Define Tool Schema

Add to the server's `list_tools()` function:

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...

        Tool(
            name="your_new_tool",
            description="Clear description of what this tool does and when Claude should use it",
            inputSchema={
                "type": "object",
                "properties": {
                    "required_param": {
                        "type": "string",
                        "description": "What this parameter means"
                    },
                    "optional_param": {
                        "type": "integer",
                        "description": "Optional parameter",
                        "default": 10
                    }
                },
                "required": ["required_param"]
            }
        )
    ]
```

### Step 3: Implement Tool Handler

Add to the server's `call_tool()` function:

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # ... existing tool handlers ...

    if name == "your_new_tool":
        # Extract parameters
        required_param = arguments["required_param"]
        optional_param = arguments.get("optional_param", 10)

        # Perform the operation
        result = perform_your_operation(required_param, optional_param)

        # Format conversational response
        response = format_conversational_response(result)

        # Return to Claude
        return [TextContent(
            type="text",
            text=response
        )]
```

### Step 4: Add Implementation Logic

Create helper functions for your tool's logic:

```python
def perform_your_operation(param1: str, param2: int) -> dict:
    """Implement the tool's core logic.

    Returns:
        Dictionary with results suitable for formatting
    """
    # Your implementation here
    return {
        "summary": "...",
        "details": [...],
        "insights": [...]
    }

def format_conversational_response(result: dict) -> str:
    """Format result as conversational response.

    Returns:
        Markdown-formatted string for Claude
    """
    response = "**Summary**\n\n"
    response += result["summary"] + "\n\n"

    if result["details"]:
        response += "**Details:**\n"
        for detail in result["details"]:
            response += f"- {detail}\n"

    return response
```

### Step 5: Update Server State (if needed)

If your tool modifies session state:

```python
# At top of server file
session_state = {
    "patients": {},
    "cohorts": {}
}

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "modify_patient":
        mrn = arguments["mrn"]
        modifications = arguments["modifications"]

        # Get patient from session
        patient = session_state["patients"].get(mrn)
        if not patient:
            return [TextContent(
                type="text",
                text=f"❌ Patient {mrn} not found in session. Generate patient first."
            )]

        # Apply modifications
        for field, value in modifications.items():
            setattr(patient, field, value)

        # Update session
        session_state["patients"][mrn] = patient

        return [TextContent(
            type="text",
            text=f"✓ Updated patient {mrn}: {', '.join(modifications.keys())}"
        )]
```

### Step 6: Test the Tool

```python
# Add to tests/mcp/test_your_server.py

import pytest
from your_product.mcp.your_server import call_tool

@pytest.mark.asyncio
async def test_your_new_tool():
    """Test your new tool with typical inputs."""
    result = await call_tool("your_new_tool", {
        "required_param": "test_value",
        "optional_param": 5
    })

    assert len(result) == 1
    assert "expected content" in result[0].text
```

## Quick Add Prompt Template

Use this prompt to quickly add a new MCP tool:

```
Add MCP tool to HealthSim product:

**Tool Purpose:** [What Claude should be able to do]

**Example Conversation:**
User: "[example user request]"
Claude: "[calls your tool]"
Claude: "[conversational response]"

**Tool Details:**
- Name: [tool_name]
- Server: [generation/export/validation]_server.py
- Parameters:
  - [param1]: [type] - [description]
  - [param2]: [type] - [description] (optional)

**Response Format:**
[Describe how response should be formatted conversationally]

**Implementation Notes:**
[Any specific logic or considerations]
```

## Tool Categories and Patterns

| Category | Examples | Key Considerations |
|----------|----------|-------------------|
| **Generation** | generate_patient, generate_cohort, modify_patient | Session state management, reproducibility (seeds) |
| **Analysis** | calculate_score, compare_patients, analyze_cohort | Clear clinical interpretation, show reasoning |
| **Export** | export_fhir, export_hl7v2, export_mimic | Format validation, file handling, batch operations |
| **Validation** | validate_patient, validate_cohort, check_coherence | Severity levels (error/warning), actionable feedback |
| **Transformation** | anonymize_patient, adjust_demographics, apply_guidelines | State consistency, reversibility considerations |

## Checklist

When adding a new MCP tool, complete this checklist:

### Design Phase
- [ ] Identified clear conversation goal (what users should be able to say)
- [ ] Confirmed MCP tool is appropriate (not just a skill or parameter)
- [ ] Designed conversational response format (not data dump)
- [ ] Identified which server to add tool to

### Implementation Phase
- [ ] Added tool to `list_tools()` with clear description
- [ ] Implemented tool handler in `call_tool()`
- [ ] Created helper functions for core logic
- [ ] Implemented conversational response formatter
- [ ] Added session state management (if needed)
- [ ] Handled error cases with helpful messages

### Response Quality Phase
- [ ] Response leads with answer, not data
- [ ] Response uses markdown formatting
- [ ] Response includes summary and details
- [ ] Response provides clinical context/interpretation
- [ ] Response suggests next actions
- [ ] Response tested with example data

### Testing Phase
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Manual testing with Claude completed
- [ ] Error handling tested
- [ ] Edge cases covered

### Documentation Phase
- [ ] Tool documented in relevant guide
- [ ] Example conversation added to examples/
- [ ] Tool parameters documented
- [ ] Response format documented

### Validation Phase
- [ ] Code formatted (black)
- [ ] Linting passed (ruff)
- [ ] Type checking passed (mypy)
- [ ] All tests passing
- [ ] Reviewed conversational response quality

---

**Remember:** The goal isn't just to add a tool—it's to enable new conversations. If you can't articulate what users should be able to say after adding your tool, reconsider whether it's needed.

## See Also

- [Extension Philosophy](philosophy.md) - Conversation-first approach
- [Skills Guide](skills.md) - When tools aren't needed
- [Slash Commands](slash-commands.md) - Adding shortcuts
- [Quick Reference](quick-reference.md) - Fast lookup
