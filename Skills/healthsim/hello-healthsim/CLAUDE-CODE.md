# Claude Code Configuration

Configure Claude Code CLI to use HealthSim for synthetic healthcare data generation.

## Prerequisites

- Claude Code installed
- Anthropic API key
- HealthSim repository cloned locally

## Installation

### Step 1: Install Claude Code

**Via npm:**
```bash
npm install -g @anthropic-ai/claude-code
```

**Via Homebrew (macOS):**
```bash
brew install claude-code
```

**Verify installation:**
```bash
claude --version
```

### Step 2: Set Up API Key

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Or add to your shell profile (~/.zshrc, ~/.bashrc)
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Clone HealthSim

```bash
git clone https://github.com/mark64oswald/healthsim-common.git
cd healthsim-common
```

---

## Configuration Methods

### Method 1: Run from HealthSim Directory (Simplest)

Claude Code automatically has access to files in your current directory.

```bash
# Navigate to HealthSim
cd /path/to/healthsim-common

# Start Claude Code
claude

# Claude can now read all skill files directly
```

### Method 2: MCP Server Configuration (Recommended)

Configure HealthSim as an MCP server for access from any directory.

#### Create/Edit Claude Code Settings

**Location:**
- macOS/Linux: `~/.claude/settings.json`
- Windows: `%USERPROFILE%\.claude\settings.json`

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

**Replace the path** with your actual HealthSim location.

#### Project-Level Configuration

For project-specific settings, create `.claude/settings.json` in any project:

```bash
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
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
EOF
```

### Method 3: Using Custom Instructions

Create a `.claude/instructions.md` file in your project:

```markdown
# Project Instructions

This project uses HealthSim for synthetic healthcare data generation.

When generating healthcare data:
1. Read SKILL.md from the healthsim-common directory for guidance
2. Follow the data models in references/data-models.md
3. Use appropriate code systems from references/code-systems.md
4. Apply clinical rules from references/clinical-rules.md

Available products:
- PatientSim: Clinical/EMR data (patients, encounters, labs)
- MemberSim: Claims/payer data (professional, facility claims)
- RxMemberSim: Pharmacy/PBM data (prescriptions, DUR alerts)
```

---

## Quick Start

### Interactive Mode

```bash
cd healthsim-common
claude
```

Then in the Claude Code session:

```
Generate a 65-year-old diabetic patient with recent labs
```

### Single Command Mode

```bash
# Generate and output to stdout
claude -p "Generate a patient with hypertension as JSON"

# Generate and save to file
claude -p "Generate a FHIR Patient resource" > patient.json
```

### With Print Mode (Non-Interactive)

```bash
# Quick generation without entering interactive mode
claude --print "Generate a pharmacy claim for metformin"
```

---

## Automation Examples

### Generate Test Data File

```bash
#!/bin/bash
# generate-test-patients.sh

cd /path/to/healthsim-common

claude --print "Generate 5 patients with various chronic conditions as a JSON array" \
  > test-patients.json
```

### Integration with Scripts

```bash
#!/bin/bash
# generate-claims-batch.sh

SCENARIOS=("office visit" "emergency room" "inpatient admission")

for scenario in "${SCENARIOS[@]}"; do
  echo "Generating: $scenario"
  claude --print "Generate a professional claim for $scenario" \
    > "claim-${scenario// /-}.json"
done
```

### CI/CD Integration

```yaml
# .github/workflows/generate-test-data.yml
name: Generate Test Data

on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Clone HealthSim
        run: git clone https://github.com/mark64oswald/healthsim-common.git

      - name: Generate Test Data
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cd healthsim-common
          claude --print "Generate 10 diverse patients with chronic conditions" \
            > ../test-data/patients.json
          claude --print "Generate 10 professional claims" \
            > ../test-data/claims.json

      - name: Upload Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: test-data
          path: test-data/
```

---

## Slash Commands

Create custom slash commands for common HealthSim operations.

### Setup Slash Commands

Create `.claude/commands/` directory:

```bash
mkdir -p .claude/commands
```

### Example: Patient Generator

```bash
# .claude/commands/patient.md
cat > .claude/commands/patient.md << 'EOF'
Generate a patient based on the provided description.

Read the SKILL.md file and relevant scenario from skills/patientsim/
to generate appropriate clinical data including:
- Demographics
- Diagnoses (ICD-10)
- Medications (with RxNorm codes)
- Recent lab results (with LOINC codes)

Patient request: $ARGUMENTS
EOF
```

**Usage:**
```
/patient 72-year-old male with COPD and heart failure
```

### Example: Claim Generator

```bash
# .claude/commands/claim.md
cat > .claude/commands/claim.md << 'EOF'
Generate a healthcare claim based on the provided description.

Read skills/membersim/SKILL.md to generate appropriate claim data.
Include:
- Claim header with proper codes
- Service lines with CPT/HCPCS
- Adjudication with realistic amounts

Claim request: $ARGUMENTS
EOF
```

**Usage:**
```
/claim denied MRI claim requiring prior authorization
```

### Example: FHIR Export

```bash
# .claude/commands/fhir.md
cat > .claude/commands/fhir.md << 'EOF'
Generate FHIR R4 resources based on the provided description.

Read formats/fhir-r4.md for transformation rules.
Output as a valid FHIR Bundle.

Request: $ARGUMENTS
EOF
```

**Usage:**
```
/fhir Bundle with Patient, Condition, and MedicationRequest for a diabetic
```

---

## Verification

### Test Basic Generation

```bash
cd healthsim-common
claude --print "Generate a patient with Type 2 diabetes"
```

**Expected:** JSON with patient, E11.x diagnoses, metformin medication.

### Test File Access

```bash
claude --print "Read SKILL.md and list the available products"
```

**Expected:** Summary of PatientSim, MemberSim, RxMemberSim.

### Test Format Output

```bash
claude --print "Generate a FHIR R4 Patient resource for a 45-year-old male"
```

**Expected:** Valid FHIR Patient resource with demographics.

---

## Troubleshooting

### "API key not found"

```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# Set it if missing
export ANTHROPIC_API_KEY="your-key"
```

### "Cannot read skill files"

1. Verify you're in the healthsim-common directory
2. Check MCP server configuration path
3. Ensure files exist: `ls SKILL.md`

### "MCP server not connecting"

```bash
# Test MCP server manually
npx -y @modelcontextprotocol/server-filesystem /path/to/healthsim-common

# Check for Node.js
node --version  # Should be 18+
```

### "Rate limiting errors"

- Reduce request frequency
- Use `--print` mode for single outputs
- Consider batching requests

### "Incomplete or malformed output"

- Be more specific in your requests
- Add "as valid JSON" to requests
- Try: "Generate a complete, valid..."

---

## Performance Tips

1. **Use `--print` for automation** - Avoids interactive overhead

2. **Be specific** - More detail = better output
   ```bash
   # Good
   claude --print "Generate a 65-year-old male diabetic with A1C 8.5, on metformin and glipizide"

   # Less good
   claude --print "Generate a patient"
   ```

3. **Request format upfront** - Faster than converting after
   ```bash
   claude --print "Generate as FHIR R4 Bundle: patient with heart failure"
   ```

4. **Cache common outputs** - Save and reuse test data

5. **Use local models** - If available, for faster iteration during development

---

## Next Steps

- Explore [examples/](examples/) for detailed use cases
- Create custom [slash commands](#slash-commands) for your workflow
- Learn to [extend HealthSim](EXTENDING.md) with new scenarios
- Integrate with your [CI/CD pipeline](#cicd-integration)

---

*Questions? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open a GitHub issue.*
