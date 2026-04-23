---
name: ttl-marketing-report-agent
description: Generate comprehensive marketing reports, calculating ROI, CPA, and other key financial and performance metrics for Texas Total Loss.
trigger: >
  Use this when asked for marketing reports, ROI analysis, cost per lead summaries,
  or financial performance of specific campaigns or the site as a whole.
---

# Goal
Provide accurate, data-driven financial and performance reports to guide marketing investment decisions.

# Instructions
1. **Gather Data**
   - Aggregate cost data from `docs/campaigns/` (look for `spend` or `budget` fields).
   - Aggregate conversion/lead data from `docs/marketing-insights.md` or `data/analytics/`.
   - If available, pull revenue/case-value data from Supabase or manual logs.
2. **Calculate Key Metrics**
   - **CPA (Cost Per Acquisition)**: Total Spend / Number of Leads.
   - **ROI (Return on Investment)**: (Total Revenue - Total Spend) / Total Spend.
   - **Conversion Rate**: Total Leads / Total Traffic.
3. **Analyze Trends**
   - Compare performance across different cities (Dallas vs. Houston vs. San Antonio).
   - Identify high-performing vs. low-performing channels (Organic, Paid, Email).
4. **Generate Report**
   - Create a dated report in `docs/reports/marketing-roi-<date>.md`.
   - Use tables and concise summaries for easy reading.
5. **Suggest Allocations**
   - Based on ROI, suggest where to increase or decrease marketing spend for the next period.

# Constraints
- Clearly label "estimates" vs. "verified data".
- Do not invent data; if a metric is missing, report it as "N/A" and suggest how to start tracking it.
