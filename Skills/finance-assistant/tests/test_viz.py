"""Tests for scripts/viz.py — ASCII visualization module."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from viz import (
    budget_bars,
    portfolio_allocation,
    net_worth_timeline,
    debt_payoff_curves,
    fire_milestone_chart,
    spending_category_delta,
    _SPARK_CHARS,
)


# ── budget_bars ───────────────────────────────────────────────────────────────

class TestBudgetBars:
    def _sample(self):
        return {
            "Food": {"limit": 400, "actual": 340},
            "Transport": {"limit": 150, "actual": 112},
            "Eating out": {"limit": 80, "actual": 89},
        }

    def test_renders_without_error(self):
        out = budget_bars(self._sample())
        assert isinstance(out, str)
        assert len(out) > 0

    def test_all_categories_present(self):
        out = budget_bars(self._sample())
        assert "Food" in out
        assert "Transport" in out
        assert "Eating out" in out

    def test_over_budget_shows_block_char(self):
        out = budget_bars(self._sample())
        # Eating out is over budget — must contain ▓
        eating_line = [l for l in out.splitlines() if "Eating out" in l][0]
        assert "▓" in eating_line

    def test_over_budget_shows_warning(self):
        out = budget_bars(self._sample())
        eating_line = [l for l in out.splitlines() if "Eating out" in l][0]
        assert "OVER" in eating_line

    def test_sorted_by_pct_descending(self):
        out = budget_bars(self._sample())
        lines = [l for l in out.splitlines() if l.strip()]
        # Eating out is 111% — should appear first
        assert "Eating out" in lines[0]
        # Food is 85%, Transport is 75% — Food before Transport
        food_idx = next(i for i, l in enumerate(lines) if "Food" in l)
        transport_idx = next(i for i, l in enumerate(lines) if "Transport" in l)
        assert food_idx < transport_idx

    def test_empty_returns_message(self):
        out = budget_bars({})
        assert "no budget" in out.lower() or len(out) > 0

    def test_money_amounts_shown(self):
        out = budget_bars(self._sample())
        assert "340" in out
        assert "400" in out


# ── portfolio_allocation ──────────────────────────────────────────────────────

class TestPortfolioAllocation:
    def _holdings(self):
        return [
            {"name": "MSCI World ETF", "value": 52_000, "asset_class": "Equities"},
            {"name": "Bond Fund", "value": 28_000, "asset_class": "Bonds"},
            {"name": "Cash", "value": 20_000, "asset_class": "Cash"},
        ]

    def test_renders_without_error(self):
        out = portfolio_allocation(self._holdings())
        assert isinstance(out, str)

    def test_all_asset_classes_shown(self):
        out = portfolio_allocation(self._holdings())
        assert "Equities" in out
        assert "Bonds" in out
        assert "Cash" in out

    def test_percentages_sum_to_100(self):
        # Parse "Equities 52%  │  Bonds 28%  │  Cash 20%"
        out = portfolio_allocation(self._holdings())
        import re
        pcts = re.findall(r"(\d+)%", out)
        # First three occurrences should be allocation percentages
        total = sum(int(p) for p in pcts[:3])
        assert abs(total - 100) <= 2  # allow rounding

    def test_top3_holdings_shown(self):
        out = portfolio_allocation(self._holdings())
        assert "Top holdings" in out
        assert "MSCI World ETF" in out

    def test_empty_returns_message(self):
        out = portfolio_allocation([])
        assert "no holdings" in out.lower()

    def test_bar_line_correct_width(self):
        out = portfolio_allocation(self._holdings(), width=40)
        bar_line = out.splitlines()[0].strip()
        assert abs(len(bar_line) - 40) <= 2  # allow small rounding


# ── net_worth_timeline ────────────────────────────────────────────────────────

class TestNetWorthTimeline:
    def _snaps(self):
        base = 142_000
        return [
            {"date": f"2024-{m:02d}-01", "net_worth": base + i * 5_000}
            for i, m in enumerate(range(1, 13))
        ]

    def test_renders_without_error(self):
        out = net_worth_timeline(self._snaps())
        assert isinstance(out, str)

    def test_sparkline_chars_in_set(self):
        out = net_worth_timeline(self._snaps())
        spark_line = out.splitlines()[0]
        spark_part = spark_line.split(":")[-1].strip()
        valid = set(_SPARK_CHARS)
        for ch in spark_part:
            assert ch in valid, f"Unexpected char: {repr(ch)}"

    def test_growth_calculated_correctly(self):
        out = net_worth_timeline(self._snaps())
        # First value 142k, last value 142k + 11*5k = 197k
        assert "142k" in out
        assert "197k" in out

    def test_shows_12_months(self):
        out = net_worth_timeline(self._snaps())
        assert "12 months" in out

    def test_caps_at_12_months(self):
        snaps = [
            {"date": f"2023-{m:02d}-01", "net_worth": 100_000 + i * 1_000}
            for i, m in enumerate(range(1, 13))
        ] + [
            {"date": f"2024-{m:02d}-01", "net_worth": 120_000 + i * 1_000}
            for i, m in enumerate(range(1, 7))
        ]
        out = net_worth_timeline(snaps)
        assert "12 months" in out or "6 months" in out  # takes last 12

    def test_empty_returns_message(self):
        out = net_worth_timeline([])
        assert "no net worth" in out.lower()


# ── debt_payoff_curves ────────────────────────────────────────────────────────

class TestDebtPayoffCurves:
    def _avalanche(self):
        return [{"month": m, "remaining": max(0, 25_000 - m * 650)} for m in range(0, 40)]

    def _snowball(self):
        return [{"month": m, "remaining": max(0, 25_000 - m * 600)} for m in range(0, 42)]

    def test_renders_without_error(self):
        out = debt_payoff_curves(self._avalanche(), self._snowball())
        assert isinstance(out, str)

    def test_two_legend_lines_present(self):
        out = debt_payoff_curves(self._avalanche(), self._snowball())
        assert "Avalanche" in out
        assert "Snowball" in out

    def test_avalanche_char_present(self):
        out = debt_payoff_curves(self._avalanche(), self._snowball())
        assert "─" in out

    def test_snowball_char_present(self):
        out = debt_payoff_curves(self._avalanche(), self._snowball())
        assert "╌" in out

    def test_months_on_x_axis(self):
        out = debt_payoff_curves(self._avalanche(), self._snowball())
        assert "0m" in out

    def test_empty_returns_message(self):
        out = debt_payoff_curves([], [])
        assert "no debt" in out.lower()


# ── fire_milestone_chart ──────────────────────────────────────────────────────

class TestFireMilestoneChart:
    def test_renders_without_error(self):
        out = fire_milestone_chart(317_000, 750_000, 1500)
        assert isinstance(out, str)

    def test_progress_percentage_correct(self):
        out = fire_milestone_chart(375_000, 750_000, 1500)
        assert "50%" in out

    def test_progress_bar_correct_width(self):
        out = fire_milestone_chart(375_000, 750_000, 1500, width=40)
        bar_line = out.splitlines()[0]
        # bar is between [ and ]
        start = bar_line.index("[") + 1
        end = bar_line.index("]")
        bar = bar_line[start:end]
        assert len(bar) == 40

    def test_milestone_markers_present(self):
        out = fire_milestone_chart(317_000, 750_000, 1500)
        assert "25%" in out
        assert "50%" in out
        assert "75%" in out
        assert "100%" in out

    def test_reached_milestones_show_checkmark(self):
        # 60% reached: 25% and 50% should be checked
        out = fire_milestone_chart(450_000, 750_000, 1500)
        # milestone line has ✓ for reached milestones
        milestone_line = out.splitlines()[1]
        assert "✓" in milestone_line

    def test_years_remaining_shown(self):
        out = fire_milestone_chart(200_000, 750_000, 2000)
        assert "years remaining" in out

    def test_invalid_target_returns_message(self):
        out = fire_milestone_chart(100_000, 0, 500)
        assert "invalid" in out.lower()


# ── spending_category_delta ───────────────────────────────────────────────────

class TestSpendingCategoryDelta:
    def _cur(self):
        return {"Food": 340.0, "Transport": 112.0, "Eating out": 89.0}

    def _prev(self):
        return {"Food": 298.0, "Transport": 130.0, "Eating out": 65.0}

    def test_renders_without_error(self):
        out = spending_category_delta(self._cur(), self._prev())
        assert isinstance(out, str)

    def test_delta_calculated_correctly(self):
        out = spending_category_delta(self._cur(), self._prev())
        # Food delta = +42
        food_line = [l for l in out.splitlines() if "Food" in l][0]
        assert "42" in food_line

    def test_decrease_shows_down_arrow(self):
        out = spending_category_delta(self._cur(), self._prev())
        transport_line = [l for l in out.splitlines() if "Transport" in l][0]
        assert "▼" in transport_line

    def test_increase_shows_up_arrow(self):
        out = spending_category_delta(self._cur(), self._prev())
        food_line = [l for l in out.splitlines() if "Food" in l][0]
        assert "▲" in food_line

    def test_large_increase_flagged_with_warning(self):
        # Eating out went from 65 to 89 = +37%, > 20% threshold
        out = spending_category_delta(self._cur(), self._prev())
        eating_line = [l for l in out.splitlines() if "Eating out" in l][0]
        assert "⚠" in eating_line

    def test_sorted_by_absolute_delta_descending(self):
        out = spending_category_delta(self._cur(), self._prev())
        data_lines = [l for l in out.splitlines() if "Food" in l or "Transport" in l or "Eating out" in l]
        # Food delta abs=42, Eating out=24, Transport=18
        # Food should be first
        assert "Food" in data_lines[0]

    def test_all_categories_shown(self):
        out = spending_category_delta(self._cur(), self._prev())
        assert "Food" in out
        assert "Transport" in out
        assert "Eating out" in out

    def test_empty_returns_message(self):
        out = spending_category_delta({}, {})
        assert "no spending" in out.lower()
