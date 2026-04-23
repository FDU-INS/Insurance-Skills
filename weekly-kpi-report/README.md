# Weekly KPI Report Generator (McKinsey Style)

> Generate executive-ready board presentations from weekly insurance data using McKinsey consulting design principles.

**Version:** v1.3.0 | **Last Updated:** 2025-12-08

## Quick Start

Upload weekly auto insurance cost data (Excel/CSV) and request a board presentation:

```
我上传了第45周的车险数据,帮我生成董事会汇报PPT
```

The skill automatically:

1. ✅ Validates data quality and required fields
2. 📊 Calculates 16+ board-level KPIs across 4 categories
3. 📈 Generates McKinsey-style PPT with conclusion-first slides
4. 💡 Provides actionable recommendations based on thresholds

## Key Features

### McKinsey Consulting Style

- **Conclusion-first titles** - Every slide answers "So what?"
- **Minimalist design** - Generous white space, clean layout
- **Professional visualization** - Data-driven insights, not decoration
- **Client-specific colors** - Extracted from corporate reports (#a02724 deep red)

### Intelligent Analysis

- **16+ KPIs** across business scale, profitability, structure, and risk
- **Auto-generated insights** - Identifies top highlights and risks
- **Actionable recommendations** - Based on configurable thresholds
- **Week-over-week comparison** - Optional trend analysis

### Flexible Configuration

Customize without code changes via `config.json`:

- Alert thresholds (combined ratio, claims frequency, etc.)
- Display parameters (top N business types, organizations)
- PPT styling (colors, fonts, sizes)
- Business rules (NEV definition, high-risk segments)

## File Structure

```
weekly-kpi-report/
├── SKILL.md                          # Skill definition and core workflow
├── README.md                         # This file - overview and quick reference
├── examples.md                       # Comprehensive usage examples
├── config.json                       # Business rules & alert thresholds
├── assets/                           # Templates & design configurations
│   ├── mckinsey_board_template.pptx  # McKinsey-style PPT template
│   ├── mckinsey_config.json          # McKinsey design specification
│   └── theme_config.json             # Color and layout themes
├── references/                       # Extended documentation
│   ├── mckinsey-style-guide.md       # Complete McKinsey design principles
│   └── config-guide.md               # Configuration customization guide
├── scripts/                          # Processing automation
│   ├── data_validator.py             # Data quality and field validation
│   ├── kpi_calculator.py             # KPI computation engine (16+ metrics)
│   ├── board_ppt_generator.py        # PPT slide generation
│   └── optional_modules/
│       └── week_comparator.py        # Week-over-week comparison analysis
└── kpis_week_*.json                  # Generated KPI data (intermediate files)
```

## Usage Methods

### Method 1: Natural Language (Recommended)

**Basic usage:**

```
我上传了第45周的车险数据,帮我生成董事会汇报PPT
```

**With WoW comparison:**

```
我上传了第45周和第44周的数据,生成带环比分析的董事会PPT
```

Claude automatically:

1. Identifies file and week number
2. Calculates all KPIs using configured thresholds
3. Generates professional PPT using McKinsey template
4. Optional: If two weeks provided, generates comparison slide
5. Returns download link

### Method 2: Manual Execution (Advanced)

```bash
# Step 1: Calculate KPIs
python scripts/kpi_calculator.py <excel_file_path> <week_number>

# Step 2 (Optional): Calculate WoW changes
python scripts/optional_modules/week_comparator.py \
  kpis_week_45.json kpis_week_44.json

# Step 3: Generate PPT
python scripts/board_ppt_generator.py \
  kpis_week_45.json 45 [week_comparison_45_vs_44.json]
```

### Method 3: Custom Configuration

Edit `config.json` to adjust:

```json
{
  "预警阈值": {
    "综合成本率_上限": 100, // Change to 100%
    "出险频度_上限": 30 // Change to 30%
  }
}
```

Changes take effect immediately on next run.

## Generated PPT Structure

**7 Slides:**

1. **Cover** - Title, date range, presenter
2. **Executive Summary** - Core metrics with top 3 highlights/risks
3. **Premium Analysis** - Revenue trends, business mix, YoY comparison
4. **Profitability Analysis** - Combined ratio breakdown, cost rate by segment
5. **NEV Business Focus** - Penetration, loss ratio comparison vs. traditional
6. **Risk Management** - Claims frequency heatmap, high-risk segments
7. **Action Items** - Auto-generated recommendations

**Slide Title Examples:**

- ✅ "Profitability remains healthy with 83.9% combined ratio below industry benchmark"
- ✅ "NEV profitability is concerning: 108.5% loss ratio, 41.4pp higher than traditional vehicles"
- ✅ "Business scale expanded 5.9%, but cost control needs attention"

## Design Standards

**McKinsey Three Pillars:**

1. **Conclusion-first** - Every title answers "So what?"
2. **Minimalist** - Large white space, clean single red accent line
3. **Left-aligned** - Professional business structure

**Color Scheme:**

- Primary: Deep Red (#a02724) - core messages
- Alert: Bright Red (#c00000) - warnings
- Text: Black (#000000) - titles
- Background: White (#FFFFFF) - clean

## Auto-Generated Action Item Examples

- ⚠️ Combined ratio at 102.3%, recommend tightening high-cost business underwriting
- 🔋 NEV loss ratio 8.2pp higher than traditional vehicles, recommend optimizing pricing model
- 🚨 Average claims frequency 28.5% is high, recommend strengthening risk screening

## Documentation

| File                                                                     | Purpose                                                          |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| [SKILL.md](SKILL.md)                                                     | Complete workflow, activation triggers, and step-by-step process |
| [examples.md](examples.md)                                               | 6+ comprehensive usage examples with inputs/outputs              |
| [references/mckinsey-style-guide.md](references/mckinsey-style-guide.md) | Full McKinsey design principles and visual standards             |
| [references/config-guide.md](references/config-guide.md)                 | Business rule configuration and threshold customization          |

## Technical Requirements

**Dependencies:**

```bash
pip install pandas openpyxl python-pptx numpy matplotlib seaborn --break-system-packages
```

**Data Requirements:**

- File format: `.xlsx`
- Required fields: Premium, loss ratio, expense ratio, variable cost rate, claims frequency
- File naming: `车险保单变动成本清单__第XX周_.xlsx`

## Prompt Optimization

**❌ Not Recommended:**

- "分析这个文件" (too vague)
- "做个 PPT" (lacks context)

**✅ Recommended:**

- "我上传了第45周的车险数据,生成董事会汇报PPT"
- "帮我制作本周车险业务的高管汇报演示文稿"
- "基于这份周报数据创建董事会级别的分析PPT"

## Troubleshooting

- **File path error** → Check if file is uploaded
- **Week number wrong** → Manually specify: "这是第45周的数据"
- **Missing fields** → Check Excel column names match standard format
- **Invalid JSON config** → Use online JSON validator

## Version History

- **v1.3.0** (2025-12-08):
  - ✨ Renamed skill to `weekly-kpi-report` following naming best practices
  - ✨ Created comprehensive `examples.md` with 6+ detailed scenarios
  - ✨ Optimized SKILL.md frontmatter with better activation triggers
  - ✨ Improved README structure for better discoverability
  - 📝 Full compliance with official Claude Code skill guidelines

- **v1.2.0_McKinsey** (2025-12-08):
  - ✨ McKinsey consulting style template
  - ✨ Client-specific color scheme (#a02724 deep red)
  - ✨ Conclusion-first slide titles
  - ✨ Reorganized folder structure (assets/, references/)

- **v1.1.0** (2025-12-08):
  - ✨ Configurable alert thresholds via config.json
  - ✨ Week-over-week comparison module
  - 🐛 Fixed field reference errors

- **v1.0.0** (2025-12-08): Initial release

## Use Cases

**Recommended for:**

- ✅ Board presentations
- ✅ Executive decision meetings
- ✅ Investor roadshows
- ✅ Strategic planning presentations
- ✅ External client proposals

## License

See LICENSE.txt for complete terms.

---

**Data Source:** Hua'an Insurance Sichuan Branch weekly auto insurance reports
**Design Style:** McKinsey & Company Consulting Style
