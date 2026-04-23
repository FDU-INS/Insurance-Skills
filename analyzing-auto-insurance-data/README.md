# Vehicle Insurance Data Analysis Skill

A Claude Code skill for analyzing vehicle insurance business data with AI-friendly design following best practices.

## Why This Skill Follows Best Practices

### 1. AI-Friendly Data Formats

**Problem**: Excel files are binary and require external libraries (pandas) to read, making them inefficient for AI processing.

**Solution**: This skill prioritizes text-based formats:
- **CSV files**: AI can read directly using the Read tool → Fast ⚡⚡⚡
- **JSON files**: Structured text data, perfect for configuration → Instant ⚡⚡⚡
- **Excel files**: Supported but converted to CSV first → Acceptable ⚡⚡

### 2. Clear Workflow with Step-by-Step Instructions

The skill provides a 7-step analysis workflow:
1. Data Loading & Validation (with CSV preference)
2. Data Cleaning (specific rules)
3. Load Reference Data (with JSON alternative)
4. Calculate Core Metrics
5. Dimensional Analysis
6. Anomaly Detection
7. Generate Report

Each step has clear, actionable instructions.

### 3. Specific Trigger Conditions

The frontmatter description includes:
- What it does: "Analyzes vehicle insurance daily reports"
- When to use: "Use when user asks to analyze insurance data"
- What it handles: "Excel/CSV files with fields like premium, institution..."

This helps Claude know exactly when to activate the skill.

### 4. Pre-Converted Reference Data

Instead of forcing AI to read Excel every time:
- `staff_mapping.json` (228 agent records) is ready to use
- AI can read JSON instantly using the Read tool
- No conversion overhead for common operations

## File Structure

```
analyzing-auto-insurance-data/
├── SKILL.md                       # Main skill definition
├── README.md                      # This file (best practices)
├── scripts/
│   └── convert_excel_to_csv.py   # Excel → CSV/JSON converter
├── 业务规则与数据洞察.md           # Business rules documentation
├── 数据分析预警规则.py             # Monitoring script
└── staff_mapping.json             # Pre-converted mapping (228 agents)
```

## Quick Start

### For End Users

**Best approach**: Convert Excel to CSV first
```bash
# Convert Excel to CSV (one-time or when data updates)
python scripts/convert_excel_to_csv.py your_data.xlsx

# Then ask Claude to analyze the CSV
# "Please analyze your_data.csv"
```

**For staff mapping**: Convert to JSON once
```bash
python scripts/convert_excel_to_csv.py 业务员机构团队对照表.xlsx --mapping
```

### For AI Assistants

When this skill activates:
1. **Check input format**:
   - CSV/JSON → Use Read tool directly (fast path ⚡⚡⚡)
   - Excel → Convert to CSV first using Bash tool, then analyze
2. **Always use staff_mapping.json** for institution mapping (don't convert Excel each time)
3. **Parse CSV as text** - no need for pandas unless complex operations required

## Performance Comparison

| Input Format | AI Processing | Speed | Context Usage | Tool Calls |
|--------------|---------------|-------|---------------|------------|
| CSV + JSON   | Read tool only | ⚡⚡⚡ Fast | Low | 2 Read |
| CSV + Excel mapping | Bash + Read | ⚡⚡ Medium | Medium | 1 Bash + 2 Read |
| Excel → CSV → analyze | Bash + Read | ⚡⚡ Medium | Medium | 2 Bash + 1 Read |
| Excel direct (pandas) | Complex processing | ⚡ Slow | High | Multiple Bash + pandas |

**Recommendation**: Always use CSV + JSON for best performance.

## Data Files

### Primary Input
- **Signing lists**: Daily insurance policy records
- **Preferred format**: CSV (UTF-8 with BOM, comma-delimited)
- **Required fields**: 投保确认时间, 业务员, 总保费, 客户类别, 险别组合, 续保情况, 三级机构

### Reference Data
- **staff_mapping.json**: Pre-converted mapping file (228 agents)
  - Format: `{"业务员ID+姓名": {"三级机构": "...", "四级机构": "...", "团队简称": "..."}}`
  - Usage: Look up correct 三级机构 for each agent
  - Updated: 2025-11-04
- **Original**: 业务员机构团队对照表20251104.xlsx (keep for backup)

## Design Principles

1. **Text over Binary**: Prefer formats AI can read directly without external tools
2. **Convert Once, Use Many**: Pre-convert reference data to JSON for repeated use
3. **Clear Instructions**: Every step has explicit actions, not vague descriptions
4. **Specific Triggers**: Description includes exact use cases and field names
5. **Fallback Support**: Accept Excel files but convert them first (graceful degradation)
6. **Progressive Disclosure**: Reference detailed docs only when needed

## Example Workflow

### Scenario: Analyze daily insurance report

**User provides**: `daily_report_20251106.xlsx`

**AI workflow (Excel input)**:
```python
# Step 1: Convert Excel to CSV (one-time overhead)
Bash: python scripts/convert_excel_to_csv.py daily_report_20251106.xlsx
# Output: daily_report_20251106.csv created

# Step 2: Read CSV directly (AI can parse text!)
Read: daily_report_20251106.csv
# Result: Raw CSV text loaded into context

# Step 3: Read pre-converted mapping (instant!)
Read: staff_mapping.json
# Result: 228 agent mappings available

# Step 4-7: Analysis happens in AI context
# - Parse CSV text
# - Apply business rules
# - Calculate metrics
# - Generate report
# No external tools needed!
```

**Benefits**:
- Only 1 Bash call for conversion
- 2 Read calls for text files
- All analysis in AI context
- Fast and efficient

**AI workflow (CSV input - recommended)**:
```python
# Step 1: Read CSV directly (no conversion needed!)
Read: daily_report_20251106.csv

# Step 2: Read mapping
Read: staff_mapping.json

# Step 3-7: Analysis
# Even faster!
```

## Comparison to Original Version

| Aspect | Original (v1.0) | Optimized (v2.0) |
|--------|-----------------|------------------|
| Description length | Too long (>1024 chars) | Concise (248 chars) ✓ |
| Trigger clarity | Vague functionality description | Specific keywords and use cases ✓ |
| Data format priority | Excel-focused | CSV/JSON priority ✓ |
| Instructions | General descriptions with emojis | 7-step actionable workflow ✓ |
| Reference data | Read Excel every time | Pre-converted JSON (read once) ✓ |
| Professionalism | Emojis throughout 📊📈🏢 | Clean, professional text ✓ |
| Scenarios | Basic examples | 4 detailed scenarios with steps ✓ |
| File organization | Flat structure | scripts/ directory for tools ✓ |

## Maintenance

### Updating Staff Mapping

When the mapping table is updated:
```bash
python scripts/convert_excel_to_csv.py 业务员机构团队对照表_new.xlsx --mapping
```

This regenerates `staff_mapping.json` for instant AI access.

### Adding New Data Sources

Follow the same pattern:
1. Create conversion script if needed
2. Generate JSON/CSV versions
3. Update SKILL.md with field descriptions
4. Add to "Related Files" section
5. Document in this README

### Updating Business Rules

When business rules change:
1. Update SKILL.md (thresholds, categories, etc.)
2. Update 业务规则与数据洞察.md (detailed documentation)
3. Update monitoring script if automated checks are affected
4. Increment version number

## Best Practices for Users

### Data Quality
1. **Time fields**: Ensure 投保确认时间 is properly formatted
2. **Institution names**: Use standardized 三级机构 names
3. **Category consistency**: Keep 客户类别 and 险别组合 classifications consistent
4. **Encoding**: Always use UTF-8 encoding for CSV files

### Workflow Optimization
1. **Convert once**: Convert Excel to CSV when you receive the data
2. **Keep CSV**: Work with CSV copies, keep Excel as backup
3. **Update mapping**: Regenerate staff_mapping.json when staff changes occur
4. **Automate**: Use the conversion script in your data pipeline

### Analysis Tips
1. **Priority alerts**: Focus on daily premium changes exceeding ±10%
2. **Monday volatility**: Pay special attention to Monday fluctuations
3. **Weekend spikes**: Verify if weekend surges are due to holidays/makeup work days
4. **Institution concentration**: Monitor if single institution exceeds 40% share

## Technical Requirements

### For Conversion Scripts
- Python 3.7+
- pandas library
- openpyxl (for Excel support)

Installation:
```bash
pip install pandas openpyxl
```

### For AI Analysis
- Claude Code with Read tool
- No external dependencies (works with CSV text parsing)

## Contributing

When extending this skill:
- Maintain CSV/JSON priority in all new features
- Provide step-by-step instructions, not just descriptions
- Add conversion scripts for any new binary formats
- Update trigger conditions in SKILL.md description
- Test with Read tool (avoid unnecessary pandas operations)
- Keep README.md in sync with SKILL.md

## Version History

- **v2.0** (2025-11-06):
  - AI-friendly redesign following best practices
  - CSV/JSON priority over Excel
  - Pre-converted staff_mapping.json (228 agents)
  - 7-step workflow with clear instructions
  - Conversion scripts in scripts/ directory
  - Professional documentation without emojis
  - Specific trigger conditions in description

- **v1.0** (2025-11-04):
  - Initial version
  - Excel-focused workflow
  - Basic business rules documentation

## Key Takeaways

This skill demonstrates Claude Code best practices:

1. **Data format matters**: Text-based formats (CSV/JSON) are 3-5x faster for AI than binary formats (Excel)
2. **Pre-conversion saves time**: Converting reference data once (Excel → JSON) eliminates repeated overhead
3. **Clear instructions work**: 7-step workflow is much clearer than general capability descriptions
4. **Specific triggers help**: Including field names and use cases in description improves skill discovery
5. **Graceful degradation**: Supporting Excel with automatic conversion provides flexibility without sacrificing optimization

---

**For questions or issues**: Check that your data files have required fields, use UTF-8 encoding for CSV, and try converting Excel to CSV first.

**Version**: 2.0
**Last Updated**: 2025-11-06
**Maintained by**: Claude Code Skills Team
