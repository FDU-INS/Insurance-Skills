---
name: ttl-daily-marketing-review-agent
description: Perform a daily review of Texas Total Loss marketing activity, competitor updates, and performance to suggest next actions.
trigger: >
  Use this skill once per day (or on demand) to summarize what happened,
  what worked, and what to do next for Texas Total Loss marketing.
---

# Goal
Create a concise daily intelligence report summarizing activity, performance, and recommending next actions.

# Instructions
1. **Gather context**
   - Read recent `docs/marketing-insights.md`, `docs/competitor-trends.md`, and campaign files.
2. **Review performance data**
   - Look in `data/analytics/` and summarize high-level metrics.
3. **Synthesize a Daily Summary**
   - What changed, what performed best, issues/anomalies.
4. **Recommend next actions**
   - Propose 3–5 actions, clearly ranked by impact/effort.
   - **Apply Decision Tier Framework (from `context.md`)**:
     - **Auto-Determine**: If a choice has high confidence/precedent, state the decision made.
     - **Propose Narrowed List**: If multiple viable paths exist, present a "Top 3" list with trade-offs.
   - For each action, note:
     - Which skill(s) should handle it.
     - Whether it needs human review or can be mostly automated.
5. **Write back to workspace**
   - Update `docs/marketing-insights.md` and `.antigravity/brain/plan.md`.
6. **Output a concise report**.
