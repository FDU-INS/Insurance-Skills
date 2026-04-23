Insurance Weekly Report Generator v2.1.1
=========================================

Quick Start
-----------
1. Upload this skill to Claude
2. Upload your insurance data file (Excel/CSV/JSON/DuckDB)
   ✨ 新增：支持原始明细数据，自动聚合！
3. Say: "Generate weekly report for week 49"

File Structure
--------------
- SKILL.md                 Core skill documentation
- scripts/                 Executable scripts
  ├─ generate_report.py    Main generator script (v2.1增强版)
  └─ data_transformer.py   Data transformation module (NEW!)
- references/              Configuration files (user editable)
  ├─ thresholds.json       Threshold configuration
  ├─ plans.json            Premium plan data (user provided)
  └─ field_mappings.json   Field mapping rules (NEW!)

Supported Data Formats
----------------------
✅ Excel (.xlsx, .xls) - 汇总数据或明细数据
✅ CSV (.csv) - 汇总数据或明细数据
✅ JSON (.json) - 汇总数据或明细数据
✅ DuckDB (.db, .duckdb) - 汇总数据或明细数据

✨ 新功能：自动数据格式识别
- 保单明细数据（英文字段）→ 自动聚合 → 生成报告
- 汇总数据（中文字段）→ 直接使用 → 生成报告
- 无需手动预处理！

KPI Calculation
---------------
All KPI formulas are aligned with kpi-calculator skill:
- Matured Loss Ratio
- Expense Ratio
- Variable Cost Ratio
- Maturity Rate (NEW in v2.1.1)
- Matured Margin Contribution Rate (NEW in v2.1.1)
- Matured Claim Frequency (NEW in v2.1.1)
- Average Premium per Policy (NEW in v2.1.1)
- Average Expense per Policy (NEW in v2.1.1)
- Matured Margin Contribution Amount (NEW in v2.1.1)

No need to run kpi-calculator separately!

Configuration
-------------
Before first use, please edit references/plans.json to add your premium plan data.
If this file is missing, premium progress analysis pages will be skipped.

Thresholds in references/thresholds.json can be adjusted based on business needs.

Output Report Structure
-----------------------
- Cover page
- 1. Business Overview (2 pages)
- 2. Premium Progress Analysis (2 pages)
- 3. Cost Analysis (2 pages)
- 4. Loss Exposure Analysis (4 pages)
- 5. Expense Analysis (2 pages)

Total: 12-13 pages in McKinsey style PPT

Support
-------
For detailed documentation, see SKILL.md
