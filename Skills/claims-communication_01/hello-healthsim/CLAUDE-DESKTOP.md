# Claude Desktop Configuration

Configure Claude Desktop to use HealthSim for synthetic healthcare data generation.

## Prerequisites

- Claude Desktop installed ([Download](https://claude.ai/download))
- Claude Pro or Team subscription (recommended for extended usage)
- HealthSim repository cloned locally

## Configuration Options

There are two ways to use HealthSim with Claude Desktop:

### Option A: Using Projects (Recommended)

Claude Desktop's Projects feature allows you to attach files that Claude can reference during conversations.

#### Step 1: Create a New Project

1. Open Claude Desktop
2. Click **"Projects"** in the left sidebar
3. Click **"+ New Project"**
4. Name it "HealthSim" or similar

#### Step 2: Add HealthSim Files

1. In your new project, click **"Add content"**
2. Select **"Add files"**
3. Navigate to your cloned `healthsim-common` folder
4. Add these key files:
   - `SKILL.md` (required - master skill file)
   - `references/data-models.md` (recommended)
   - `references/code-systems.md` (recommended)

**Tip:** Start with just `SKILL.md`. Claude will instruct you to add scenario files as needed.

#### Step 3: Set Project Instructions

In the project settings, add these instructions:

```
You have access to HealthSim, a synthetic healthcare data generation framework.
When generating healthcare data, refer to SKILL.md for guidance on available
scenarios and output formats. Follow the data models and code systems provided.
```

#### Step 4: Start Generating

Open a new chat in your HealthSim project and try:

```
Generate a 58-year-old female with poorly controlled Type 2 diabetes
```

### Option B: Using MCP Server (Advanced)

For more integrated experience, you can configure HealthSim as an MCP (Model Context Protocol) server.

#### Step 1: Locate Claude Desktop Config

Find your Claude Desktop configuration file:

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### Step 2: Add MCP Server Configuration

Edit the config file to add a filesystem MCP server pointing to HealthSim:

```json
{
  "mcpServers": {
    "healthsim": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/your/healthsim-common"
      ]
    }
  }
}
```

**Replace `/path/to/your/healthsim-common`** with the actual path where you cloned the repository.

**macOS Example:**
```json
{
  "mcpServers": {
    "healthsim": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/projects/healthsim-common"
      ]
    }
  }
}
```

**Windows Example:**
```json
{
  "mcpServers": {
    "healthsim": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\yourname\\projects\\healthsim-common"
      ]
    }
  }
}
```

#### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop for changes to take effect.

#### Step 4: Verify MCP Connection

In a new chat, you should see a tools icon indicating MCP servers are connected. Ask Claude:

```
Can you see the HealthSim skill files?
```

Claude should be able to read files from the healthsim-common directory.

---

## Verification

Test your setup with these prompts:

### Basic Test
```
Generate a patient with hypertension
```

**Expected:** JSON with patient demographics, I10 diagnosis, and antihypertensive medication.

### Scenario Test
```
Generate an inpatient claim for heart failure with DRG
```

**Expected:** 837I-style claim with DRG 291 or 292, revenue codes, and adjudication.

### Format Test
```
Generate a patient as FHIR R4 Bundle
```

**Expected:** FHIR Bundle resource with Patient, Condition, and MedicationStatement resources.

---

## Troubleshooting

### "I don't see the HealthSim files"

**Projects Method:**
- Verify files are added to your project
- Check that SKILL.md is included
- Try removing and re-adding the files

**MCP Method:**
- Verify the path in your config is correct
- Check that the path exists and is readable
- Restart Claude Desktop after config changes
- Look for error messages in Claude Desktop's developer console

### "The generated data doesn't match the schema"

- Add `references/data-models.md` to your project
- Explicitly request: "Generate according to the data model schema"

### "Claude doesn't know about specific scenarios"

Add the relevant scenario file:
- Diabetes issues → Add `skills/patientsim/diabetes-management.md`
- Claims issues → Add `skills/membersim/professional-claims.md`
- Pharmacy issues → Add `skills/rxmembersim/retail-pharmacy.md`

### "MCP server not connecting"

1. Ensure Node.js is installed: `node --version`
2. Check the config file is valid JSON (use a JSON validator)
3. Verify the path uses forward slashes or escaped backslashes
4. Try running the MCP server manually to check for errors:
   ```bash
   npx -y @modelcontextprotocol/server-filesystem /path/to/healthsim-common
   ```

---

## Tips for Best Results

1. **Be Specific** - "65-year-old diabetic with A1C of 9.2" beats "sick patient"

2. **Request Formats Early** - "Generate as FHIR..." rather than converting after

3. **Use Trigger Phrases** - Each scenario has trigger phrases that activate it:
   - "DUR alert" → Drug utilization review scenario
   - "prior auth" → Prior authorization workflow
   - "HEDIS" → Value-based care measures

4. **Combine Products** - Request cross-domain data:
   ```
   Generate a diabetic patient with their professional claim and pharmacy claims
   ```

5. **Iterate** - Start simple, then add complexity:
   ```
   Generate a patient with heart failure
   → Now add their recent hospitalization
   → Now add the facility claim for that admission
   ```

---

## Next Steps

- Try the [examples](examples/) for detailed walkthroughs
- Read [SKILL.md](../SKILL.md) for complete capabilities
- Learn to [extend HealthSim](EXTENDING.md) with custom scenarios

---

*Having issues? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open a GitHub issue.*
