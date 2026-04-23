# Insurance Plan Analyzer - Claude Skill

A comprehensive Claude skill for analyzing and comparing health insurance options, with specialized support for small business decisions, H-1B visa considerations, and ICHRA analysis.

## 📋 Overview

This skill automates the complex process of comparing health insurance plans by:
- Extracting data from multiple quote sources
- Calculating total costs with various scenarios
- Analyzing tax benefits and subsidies
- Generating formatted comparison reports
- Providing clear recommendations

## 🎯 Use Cases

### Perfect For:
- Small business owners choosing employee health insurance
- HR managers comparing group insurance quotes
- Companies considering individual marketplace + ICHRA vs traditional group plans
- H-1B visa holders analyzing subsidy eligibility
- Anyone needing to compare multiple insurance options systematically

### Your Actual Use Case:
This skill was created based on your recent work comparing insurance options for Rajesh. It would have automated:
1. ✅ Extracting quotes from Chuck, Jolly, and Adriana's emails
2. ✅ Calculating cost comparisons (individual vs group)
3. ✅ Analyzing H-1B subsidy eligibility
4. ✅ Generating the comprehensive comparison report
5. ✅ Formatting everything for Notepad++

**Time Savings:** What took hours manually would take minutes with this skill.

## 📦 Contents

```
insurance-plan-analyzer-skill/
├── SKILL.md                          # Main skill definition (REQUIRED)
├── README.md                         # This file
├── templates/
│   └── comparison_report_template.txt  # Standard report format
└── scripts/
    └── cost_calculator.py            # Python cost calculation helper
```

## 🚀 Installation Methods

### Method 1: Claude.ai Web/Desktop App (Easiest)

**Requirements:** Pro, Max, Team, or Enterprise plan

1. **Enable Skills Feature:**
   - Go to Settings → Capabilities
   - Enable "Code execution and file creation"
   - Toggle on "Skills"

2. **Package the Skill:**
   ```bash
   cd /home/user01/claude-test/html
   zip -r insurance-plan-analyzer-skill.zip insurance-plan-analyzer-skill/
   ```

3. **Upload:**
   - Settings → Capabilities → Skills section
   - Click "Upload custom skill"
   - Select `insurance-plan-analyzer-skill.zip`

4. **Verify:**
   - Skill should appear in your Skills list
   - Description should read: "Analyzes and compares health insurance plans..."

### Method 2: Claude Code CLI

**Requirements:** Claude Code installed

1. **Copy to Skills Directory:**
   ```bash
   # For project-specific skill
   cp -r /home/user01/claude-test/html/insurance-plan-analyzer-skill \
         /home/user01/claude-test/.claude/skills/

   # For personal skill (available in all projects)
   mkdir -p ~/.claude/skills
   cp -r /home/user01/claude-test/html/insurance-plan-analyzer-skill \
         ~/.claude/skills/
   ```

2. **Verify:**
   ```bash
   # Skills are auto-discovered when you use Claude Code
   # Just start using it!
   ```

### Method 3: API Implementation

**Requirements:** Anthropic API access

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Read the skill file
with open("insurance-plan-analyzer-skill/SKILL.md", "r") as f:
    skill_content = f.read()

# Create a custom skill (simplified approach)
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25"],
    system=skill_content,  # Include skill as system prompt
    messages=[{
        "role": "user",
        "content": "Compare these insurance quotes: [your data]"
    }]
)
```

## 💡 Usage Examples

### Example 1: Basic Comparison
```
You: "I have 3 insurance quotes from different agents.
      Chuck quoted $2,053/month for AmeriHealth Silver EPO.
      Jolly quoted $1,586/month for the same plan on marketplace.
      Which is better?"

Claude: [Activates insurance-plan-analyzer skill]
        [Compares costs, calculates savings, generates report]

        Result: Individual marketplace saves $5,604/year
```

### Example 2: H-1B Subsidy Analysis
```
You: "My H-1B employee makes $132k. Can he get subsidies if
      group insurance would cost him $1,848/month?"

Claude: [Activates skill, applies 9.12% affordability rule]

        Result: YES - Coverage is unaffordable ($1,848 > $1,003 threshold)
                Since you sponsor his H-1B, he qualifies for subsidies
```

### Example 3: Full Analysis
```
You: "Analyze insurance options for Rajesh (H-1B, $132k income,
      family of 4). I have quotes from 3 agents in these emails."
      [Attach email files]

Claude: [Activates skill]
        [Extracts all quote data]
        [Calculates costs for all options]
        [Analyzes subsidy eligibility]
        [Generates comprehensive report]

        Result: 15-page formatted comparison report with clear recommendation
```

## 🔧 Testing the Calculator

Run the Python cost calculator to verify calculations:

```bash
cd /home/user01/claude-test/html/insurance-plan-analyzer-skill/scripts
python3 cost_calculator.py
```

**Expected Output:**
```
============================================================
EXAMPLE 1: Small Group Insurance
============================================================
Monthly Premium:           $2,053.33
Annual Premium:            $24,639.96
...
ACA Affordability Check:
  Status:                  UNAFFORDABLE ✗

H-1B Subsidy Eligibility:
  Qualifies: YES ✓
...
```

## 📊 Key Features

### 1. Automatic Data Extraction
- Reads quotes from emails, PDFs, or text
- Recognizes major carriers (Horizon, UHC, AmeriHealth, etc.)
- Extracts: premiums, deductibles, copays, coinsurance

### 2. Comprehensive Cost Analysis
- Annual cost projections
- Tax savings calculations (pre-tax vs after-tax)
- ICHRA reimbursement scenarios
- Subsidy eligibility (ACA affordability rule)

### 3. H-1B Specialized Analysis
- **9.12% Affordability Rule:** Determines if employer coverage is "unaffordable"
- **Subsidy Eligibility:** Checks if H-1B holder qualifies for marketplace subsidies
- **Visa Documentation:** Considers what's needed for visa purposes

### 4. ICHRA Analysis
- Calculates tax-free reimbursement scenarios
- Compares ICHRA + individual vs traditional group
- Shows savings for both employer and employee

### 5. Formatted Reports
- Fixed-width text formatting for Notepad++
- Aligned tables and columns
- Visual indicators (✓/✗/⭐)
- Ready to share with stakeholders

## 🎓 How It Works (Technical)

### Progressive Disclosure System

Claude reads a short description from the YAML frontmatter:
```yaml
description: Analyzes and compares health insurance plans (individual vs
             group), calculates costs, verifies networks, and generates
             formatted comparison reports for decision-making
```

**Token Efficient:**
- Skill metadata: ~50 tokens
- Full skill content: Only loaded when needed
- Your conversation: No unnecessary token usage

### Automatic Activation

Claude automatically loads this skill when you:
- Mention "insurance comparison" or "health insurance quotes"
- Ask about "individual vs group insurance"
- Discuss "H-1B subsidies" or "ICHRA"
- Request cost analysis or formatted reports

**You don't need to manually invoke it** - Claude decides based on context.

## 📈 Real-World Impact

### Your Recent Work (Before This Skill):
- ⏱️ Time spent: ~4-5 hours
- 📧 Emails reviewed: 10+
- 🔢 Manual calculations: 30+
- 📄 Reports created: 2 comprehensive documents

### With This Skill (Future):
- ⏱️ Time spent: ~15-30 minutes
- 📧 Just forward emails to Claude
- 🔢 Automatic calculations
- 📄 Instant formatted reports

**ROI: Save 3-4 hours per insurance comparison analysis**

## 🔐 Security & Privacy

### Sandboxed Execution
- All calculations run in isolated environment
- No external API calls for sensitive data
- Scripts execute locally

### Data Privacy
- Employee data stays in your Claude conversation
- No data sent to third parties
- You control when/how skill is used

### Best Practices
- Don't include SSNs or sensitive IDs in quotes
- Verify agent contacts before sharing reports
- Use skill for analysis only, not enrollment

## 🚦 Key Takeaways Achievement

### ✅ Availability: Pro, Max, Team, Enterprise
**Status:** Skill created and ready for these plan levels

### ✅ Purpose: Standardize and automate repetitive tasks
**Achieved:**
- Standardizes insurance comparison process
- Automates quote extraction and cost calculation
- Saves 3-4 hours per analysis

### ✅ Portability: Build once, use everywhere
**Achieved:**
- Same skill file works in: Claude.ai, Claude Code, API
- Templates reusable across all platforms
- Scripts executable anywhere Python runs

### ✅ Automatic: Claude decides when to use
**Achieved:**
- No manual invocation needed
- Activates on keywords: insurance, quotes, comparison, H-1B, ICHRA
- Progressive disclosure: Only loads when relevant

### ✅ Composable: Multiple skills work together
**Achieved:**
- Can combine with Excel skill for spreadsheet generation
- Works with PDF skill to extract quote data
- Integrates with web search for carrier research

### ✅ Secure: Sandboxed with safety controls
**Achieved:**
- Python scripts run in isolated environment
- No external API calls
- User controls all data

## 🎯 Next Steps

### Immediate Actions:
1. **Test the calculator script:**
   ```bash
   python3 scripts/cost_calculator.py
   ```

2. **Package the skill:**
   ```bash
   cd /home/user01/claude-test/html
   zip -r insurance-plan-analyzer-skill.zip insurance-plan-analyzer-skill/
   ```

3. **Upload to Claude.ai** (if you have Pro/Max/Team/Enterprise)

### Future Enhancements:
- [ ] Add support for more states (currently NJ-focused)
- [ ] Include HSA/FSA analysis
- [ ] Add dental and vision insurance comparison
- [ ] Create Excel output option (combine with xlsx skill)
- [ ] Add timeline/deadline tracking
- [ ] Include benefits communication templates

## 📞 Support

### Questions?
- Check the SKILL.md file for detailed instructions
- Review the examples in this README
- Run cost_calculator.py to understand calculations

### Customization:
Want to modify for your specific needs?
1. Edit SKILL.md to add/remove features
2. Update templates for your preferred format
3. Modify cost_calculator.py for different calculations
4. Re-package and upload

## 📝 Version History

- **v1.0.0** (October 2025)
  - Initial release
  - H-1B subsidy analysis
  - ICHRA support
  - NJ small group rules
  - Formatted text report generation

## 📄 License

Created for Paragroup LLC.
Free to use and modify for your organization's needs.

---

**Created:** October 17, 2025
**Author:** Paragroup LLC
**Purpose:** Automate health insurance comparison and analysis

---

## 🎉 Success Story

This skill was created based on actual work performed for Rajesh's insurance analysis. It encodes all the knowledge, calculations, and decision frameworks used in that analysis, making it instantly reusable for:

- Future employee insurance decisions
- Annual renewal comparisons
- New hire benefits setup
- Policy change evaluations

**Bottom Line:** Turn hours of manual work into minutes of automated analysis.
