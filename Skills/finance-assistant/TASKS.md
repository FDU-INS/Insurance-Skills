# Scheduled Tasks

These tasks are designed to run automatically via Cowork's task scheduler.
Each calls a function in `scripts/cowork_tasks.py` and returns a formatted
string that Claude presents to the user.

---

## Daily Brief (recommended: every morning)

**Function:** `scripts/cowork_tasks.py` → `daily_brief()`

Surfaces budget warnings, upcoming bills, and critical insights every morning
so you start each day knowing exactly what needs attention.

**What it checks:**
- Active budget alerts (overspend, pacing warnings)
- Recurring payments due in the next 7 days
- Savings goals with approaching deadlines
- Tax deadlines within 45 days
- FIRE progress (once per month)
- Critical actionable insights from the insight engine

**Recommended schedule:** Daily, 07:00–09:00 local time on working days.

---

## Weekly Summary (recommended: every Monday)

**Function:** `scripts/cowork_tasks.py` → `weekly_summary()`

A short Monday-morning review of how the month is tracking and what is coming up.

**What it covers:**
- Budget pace: how much of the month is spent vs how much budget is used
- Categories currently over budget
- Top 3 cross-domain financial insights
- All bills due in the next 7 days with amounts

**Recommended schedule:** Every Monday, 08:00 local time.

---

## Monthly Snapshot (recommended: last day of month)

**Function:** `scripts/cowork_tasks.py` → `monthly_snapshot()`

Month-end snapshot that locks in your net worth and portfolio values, then
generates the full HTML and Markdown finance reports for the month.

**What it does:**
1. Takes a net worth snapshot (`net_worth_engine.take_snapshot()`)
2. Takes a portfolio snapshot (`investment_tracker.take_portfolio_snapshot()`)
3. Generates the HTML and Markdown monthly report (`generate_report.generate_monthly_report()`)
4. Returns a summary with the saved file paths

Reports are saved to `.finance/reports/YYYY-MM.md` and `.finance/reports/YYYY-MM.html`.

**Recommended schedule:** Last day of each month, 23:00 local time.

---

## Setup in Cowork

1. Open Cowork and navigate to **Scheduled Tasks**.
2. Add a new task for each function above.
3. Set the trigger to the finance-assistant skill.
4. Enter the function call as the task body, e.g.:

   ```
   Run scripts/cowork_tasks.py → daily_brief()
   ```

5. Set the cron schedule and save.

Each task runs in an isolated context and never crashes Cowork even if a data
source is missing — errors are caught and reported as part of the output string.
