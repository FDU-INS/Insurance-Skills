# Adding Slash Commands

Guide to creating slash commands that provide shortcuts for common actions.

## When to Add a Slash Command

Add a slash command when **users frequently perform the same action** and would benefit from a shortcut.

### Good Reasons to Add Slash Command

**Frequent repetitive actions**
```
Users often say: "Generate 10 diabetic patients with HbA1c >9%"
→ Add /generate command: /generate diabetes --count 10 --hba1c >9
```

**Multi-step workflows**
```
Users often: Generate patients → Validate → Export to FHIR
→ Add /workflow command: /workflow test-cohort --format fhir
```

**Common parameter combinations**
```
Users often say: "Generate cardiac patients for cath lab testing"
→ Add /cath-lab command that sets up standard cardiac test patients
```

**Quick access to help or info**
```
Users ask: "What cohorts are available?"
→ Add /cohorts command to list available cohorts
```

### Bad Reasons to Add Slash Command

**One-time or rare actions**
```
User says once: "Generate patient named John with MRN-12345"
→ Don't add /custom-patient command, too specific
```

**Actions that need explanation**
```
User asks: "How do I generate sepsis patients?"
→ Don't add command, user needs conversation and guidance
```

**Complex, context-dependent requests**
```
User says: "Generate patients similar to the last cohort but with variations"
→ Don't add command, needs conversational refinement
```

## Slash Command Anatomy

Slash commands in Claude Code map to expanded prompts or tool sequences.

### Basic Structure

```markdown
# /command-name

**Description:** Brief description of what this command does

**Usage:** /command-name [arguments]

**Arguments:**
- `arg1` - Description of first argument (required)
- `arg2` - Description of second argument (optional)

**Expansion:**
[The prompt that Claude receives when this command is invoked]

**Example:**
/command-name value1 value2
```

### Example: /generate Command

```markdown
# /generate

**Description:** Quickly generate patients by cohort type

**Usage:** /generate <cohort> [--count N] [--severity level]

**Arguments:**
- `cohort` - Cohort type (diabetes, cardiac, sepsis, joint-replacement)
- `--count N` - Number of patients to generate (default: 1)
- `--severity level` - Severity level (mild, moderate, severe)

**Expansion:**
Generate {count} {cohort} patients with {severity} severity.
For each patient provide:
- Full demographics (name, MRN, age, gender)
- Complete condition list with ICD-10 codes
- Medications with doses and frequencies
- Recent labs with values and dates
- Brief clinical summary

After generation, ask if I want to:
1. Validate the patients
2. Export to a specific format
3. Make modifications
4. Generate additional patients

**Example:**
/generate diabetes --count 5 --severity moderate

Expands to:
"Generate 5 diabetes patients with moderate severity. For each patient provide..."
```

## Quick Add Prompt

Use this prompt to add a slash command:

```
Add slash command to HealthSim:

**Command:** /[command-name]

**Purpose:** [What users accomplish with this shortcut]

**Common Use Case:**
Users frequently: "[what users currently say/do]"

**Shortcut:**
Instead, they'll use: /[command-name] [args]

**Expansion:**
When user types /[command-name] [args], Claude receives:
"[expanded prompt with arguments filled in]"

**Arguments:**
- [arg1]: [type] - [description] (required/optional)
- [arg2]: [type] - [description] (required/optional)

**Example Usage:**
/[command-name] [example args]

**File:** .claude/commands/[command-name].md

**Follow existing command structure** in .claude/commands/
```

### Example Prompt: Adding /validate Command

```
Add slash command to HealthSim:

**Command:** /validate

**Purpose:** Quick validation of recently generated patients

**Common Use Case:**
Users frequently: "Can you validate those patients?" or "Run validation checks"

**Shortcut:**
Instead, they'll use: /validate [mrn] or /validate --all

**Expansion:**
When user types /validate [mrn], Claude receives:
"Run clinical validation checks on patient [mrn]. Report any errors, warnings, or issues found. Provide actionable feedback on how to fix issues."

When user types /validate --all, Claude receives:
"Run clinical validation checks on all patients in the current session. Provide summary of:
- Total patients checked
- Patients with errors
- Patients with warnings
- Patients that passed all checks
For any issues found, provide actionable feedback."

**Arguments:**
- `mrn`: string - Specific patient MRN to validate (optional)
- `--all`: flag - Validate all patients in session (optional)

**Example Usage:**
/validate MRN-12345
/validate --all

**File:** .claude/commands/validate.md
```

## Implementation Steps

### Step 1: Create Command File

Create `.claude/commands/[command-name].md`:

```markdown
# /[command-name]

Brief description of what this command does.

## Usage

/[command-name] <required-arg> [optional-arg]

## Arguments

- `required-arg` - Description (required)
- `optional-arg` - Description (optional, default: value)

## Behavior

When this command is invoked, [describe what happens].

## Examples

### Example 1: Basic usage
```
/[command-name] value1
```

Output: [describe expected output]

### Example 2: With options
```
/[command-name] value1 --option value2
```

Output: [describe expected output]

## Related Commands

- /related-command - Description
```

### Step 2: Register Command

Commands in `.claude/commands/` are automatically discovered by Claude Code.

No additional registration needed.

### Step 3: Test Command

In Claude Desktop or Claude Code:

```
1. Type: /[command-name] [test-args]
2. Verify Claude receives expanded prompt
3. Verify Claude performs expected actions
4. Refine prompt if needed
```

### Step 4: Document Command

Add to `.claude/commands/README.md`:

```markdown
## /[command-name]

Brief description

**Usage:** `/[command-name] <args>`

**Example:** `/[command-name] example-value`

See [command-name.md](command-name.md) for details.
```

## Common Patterns

### Pattern 1: Quick Generation

```markdown
# /quick

**Description:** Generate single patient with minimal details

**Usage:** /quick <cohort>

**Expansion:**
Generate a single {cohort} patient. Provide name, MRN, age, gender, primary conditions, and key medications. Keep response brief.

**Example:**
/quick diabetes
```

### Pattern 2: Workflow Shortcuts

```markdown
# /test-cohort

**Description:** Generate, validate, and export test cohort

**Usage:** /test-cohort <cohort> <format>

**Expansion:**
1. Generate 10 {cohort} patients with varying severity
2. Run validation checks on all patients
3. If validation passes, export to {format}
4. Report summary of cohort characteristics

**Example:**
/test-cohort sepsis fhir
```

### Pattern 3: Information Retrieval

```markdown
# /cohorts

**Description:** List available cohort skills

**Usage:** /cohorts [category]

**Expansion:**
List all available cohorts in the {category} category (or all categories if not specified). For each cohort, provide:
- Cohort name
- Brief description
- Example usage
- Key parameters users can control

**Example:**
/cohorts
/cohorts cardiac
```

### Pattern 4: Session Management

```markdown
# /cohort

**Description:** Manage patient cohorts in session

**Usage:** /cohort <action> [name]

**Actions:**
- list - List all cohorts
- show [name] - Show cohort details
- name [name] - Name the current cohort

**Expansion:**
{action} patient cohort {name}.

For "list": Show all named cohorts in current session
For "show": Display all patients in cohort {name}
For "name": Assign name {name} to most recently generated patients

**Example:**
/cohort list
/cohort show test-group-1
/cohort name cardiac-cath-patients
```

## Advanced: Parameterized Commands

Commands can parse complex arguments:

```markdown
# /batch

**Description:** Batch generation with distributions

**Usage:** /batch <cohort> --total N [--distribution key:value]

**Arguments:**
- `cohort` - Cohort type
- `--total N` - Total patients to generate
- `--distribution key:value` - Distribution percentages

**Expansion:**
Generate {total} {cohort} patients with the following distribution:
{parse distribution arguments}

For example, if arguments are:
--total 100 --distribution male:60 female:40 --distribution mild:50 moderate:30 severe:20

Generate:
- 100 total patients
- 60 male, 40 female
- 50 mild severity, 30 moderate severity, 20 severe severity

**Example:**
/batch diabetes --total 50 --distribution male:45 female:55 --distribution controlled:30 uncontrolled:70
```

## Testing Checklist

When adding a slash command:

### Functionality Testing
- [ ] Command file created in `.claude/commands/`
- [ ] Command shows in /help or command list
- [ ] Command expands to correct prompt
- [ ] Arguments parsed correctly
- [ ] Required arguments enforced
- [ ] Optional arguments have sensible defaults
- [ ] Error messages helpful for invalid usage

### Usability Testing
- [ ] Command name is intuitive
- [ ] Arguments are clear and memorable
- [ ] Usage examples cover common cases
- [ ] Help text is concise and useful
- [ ] Command saves time vs typing full request

### Integration Testing
- [ ] Command works with existing features
- [ ] Command output works with subsequent commands
- [ ] Command respects session state
- [ ] Command documented in README

## Checklist

When adding a new slash command, complete this checklist:

### Design Phase
- [ ] Identified frequent, repetitive action
- [ ] Confirmed command is useful shortcut (not one-off)
- [ ] Designed clear command syntax
- [ ] Planned argument structure
- [ ] Wrote example usage

### Implementation Phase
- [ ] Created `.claude/commands/[command-name].md`
- [ ] Wrote clear description
- [ ] Documented usage and arguments
- [ ] Defined prompt expansion
- [ ] Included 2-3 examples
- [ ] Listed related commands

### Documentation Phase
- [ ] Added to `.claude/commands/README.md`
- [ ] Usage examples clear
- [ ] Arguments documented
- [ ] Related commands cross-referenced

### Testing Phase
- [ ] Command appears in Claude
- [ ] Expansion works correctly
- [ ] Arguments parse as expected
- [ ] Examples all work
- [ ] Error cases handled gracefully

### User Experience Phase
- [ ] Command name intuitive
- [ ] Saves time vs full request
- [ ] Help text sufficient
- [ ] Examples representative

---

**Remember:** Slash commands are shortcuts for conversations users already have. If users don't frequently say something similar to what your command does, it's probably not needed. Focus on high-frequency actions that benefit from shortcuts.

## Example Commands

### /generate Command

```markdown
# /generate

Generate patients by cohort type with options for count and severity.

## Usage

/generate <cohort> [--count N] [--severity level]

## Arguments

- `cohort` - Cohort type (diabetes, cardiac, sepsis, joint-replacement)
- `--count N` - Number of patients (default: 1)
- `--severity level` - Severity (mild, moderate, severe)

## Examples

### Generate single diabetic patient
```
/generate diabetes
```

### Generate multiple cardiac patients
```
/generate cardiac --count 10
```

### Generate severe sepsis patients
```
/generate sepsis --count 5 --severity severe
```

## Related Commands

- /validate - Validate generated patients
- /export - Export patients to format
```

### /export Command

```markdown
# /export

Export patients to healthcare data formats.

## Usage

/export <format> [mrn] [--validate]

## Arguments

- `format` - Export format (fhir, hl7v2, mimic)
- `mrn` - Specific patient MRN (optional, default: all)
- `--validate` - Validate before export (optional)

## Examples

### Export all patients to FHIR
```
/export fhir
```

### Export specific patient to HL7v2
```
/export hl7v2 MRN-12345
```

### Export with validation
```
/export fhir --validate
```

## Related Commands

- /generate - Generate patients
- /validate - Validate patients
```

## See Also

- [Extension Philosophy](philosophy.md) - Overall extension philosophy
- [MCP Tools](mcp-tools.md) - When commands need new capabilities
- [Skills](skills.md) - When commands need new knowledge
- [Quick Reference](quick-reference.md) - Fast lookup
