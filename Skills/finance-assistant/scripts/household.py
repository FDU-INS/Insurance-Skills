"""
Finance Assistant Shared Household Budget.

Manages shared household expenses, per-member balances, and settle-up calculations.
Storage: .finance/household/household.json and .finance/household/shared_expenses.json
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime
from typing import Optional

try:
    from finance_storage import ensure_subdir, load_json, save_json
    from currency import format_money
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir, load_json, save_json
    from currency import format_money


# ── Storage paths ─────────────────────────────────────────────────────────────

def _household_dir():
    return ensure_subdir("household")


def _household_config_path():
    return _household_dir() / "household.json"


def _shared_expenses_path():
    return _household_dir() / "shared_expenses.json"


# ── Internal helpers ──────────────────────────────────────────────────────────

def _load_household() -> dict:
    return load_json(_household_config_path(), default={})


def _load_expenses() -> list[dict]:
    data = load_json(_shared_expenses_path(), default={"expenses": []})
    return data.get("expenses", []) if isinstance(data, dict) else []


def _save_expenses(expenses: list[dict]) -> None:
    save_json(_shared_expenses_path(), {
        "last_updated": datetime.now().isoformat(),
        "expenses": expenses,
    })


# ── Public API ────────────────────────────────────────────────────────────────

def create_household(name: str, member_ids: list[str]) -> dict:
    """
    Create a shared household with named members.
    Saves to .finance/household/household.json.

    Args:
        name:        Household name (e.g., "Flat 3B").
        member_ids:  List of member identifiers (names or IDs).

    Returns:
        The household config dict.
    """
    if not member_ids:
        raise ValueError("A household must have at least one member.")

    household = {
        "name": name,
        "members": member_ids,
        "created_at": datetime.now().isoformat(),
        "currency": "EUR",
    }
    save_json(_household_config_path(), household)
    return household


def get_household() -> dict:
    """Load current household config. Returns {} if none exists."""
    return _load_household()


def log_shared_expense(
    amount: float,
    category: str,
    paid_by: str,
    split: Optional[dict] = None,
    description: str = "",
) -> dict:
    """
    Log a shared expense.

    Args:
        amount:      Total amount of the expense (positive float).
        category:    Expense category.
        paid_by:     Member ID who paid.
        split:       {member_id: fraction} dict. Fractions must sum to 1.0.
                     Defaults to equal split among all household members.
        description: Optional description.

    Returns:
        The expense record plus each member's running balance.
    """
    household = _load_household()
    members = household.get("members", [])
    currency = household.get("currency", "EUR")

    if not members and split is None:
        raise ValueError("No household defined. Create one first with create_household().")

    # Default: equal split
    if split is None:
        if not members:
            raise ValueError("Cannot auto-split: no household members defined.")
        fraction = round(1.0 / len(members), 8)
        split = {m: fraction for m in members}

    # Normalize fractions to ensure they sum to 1
    total_fraction = sum(split.values())
    if abs(total_fraction - 1.0) > 0.01:
        split = {k: v / total_fraction for k, v in split.items()}

    expense_id = str(uuid.uuid4())[:8]
    expense = {
        "id": expense_id,
        "date": datetime.now().date().isoformat(),
        "amount": round(float(amount), 2),
        "category": category,
        "paid_by": paid_by,
        "split": {k: round(v, 6) for k, v in split.items()},
        "description": description,
        "currency": currency,
        "created_at": datetime.now().isoformat(),
    }

    expenses = _load_expenses()
    expenses.append(expense)
    _save_expenses(expenses)

    # Calculate running balances for return value
    balances = _calculate_balances(expenses)

    return {
        "expense": expense,
        "member_balances": balances,
    }


def _calculate_balances(expenses: list[dict]) -> dict[str, float]:
    """
    Calculate net balance per member across all shared expenses.
    Positive = owed money (others owe this member).
    Negative = owes money (this member owes others).
    """
    balances: dict[str, float] = {}

    for expense in expenses:
        amount = float(expense.get("amount", 0))
        paid_by = expense.get("paid_by", "")
        split = expense.get("split", {})

        # Payer gets credit for the full amount
        balances[paid_by] = balances.get(paid_by, 0.0) + amount

        # Each member (including payer) owes their share
        for member, fraction in split.items():
            share = round(amount * fraction, 2)
            balances[member] = balances.get(member, 0.0) - share

    return {k: round(v, 2) for k, v in balances.items()}


def get_shared_balance() -> dict:
    """
    Calculate who owes what.

    Returns:
        {
            "balances": {member_id: net_amount},  # positive = owed money, negative = owes
            "settle_up": [{"from": id, "to": id, "amount": float}]
        }
    """
    expenses = _load_expenses()
    balances = _calculate_balances(expenses)

    # Compute minimal settle-up transactions
    settle_up = _compute_settle_up(balances)

    return {
        "balances": balances,
        "settle_up": settle_up,
    }


def _compute_settle_up(balances: dict[str, float]) -> list[dict]:
    """
    Compute the minimal set of transfers to settle all balances.
    Uses a greedy algorithm: largest debtor pays largest creditor.
    """
    # Separate creditors (positive) and debtors (negative)
    creditors = sorted(
        [(m, v) for m, v in balances.items() if v > 0.005],
        key=lambda x: -x[1]
    )
    debtors = sorted(
        [(m, -v) for m, v in balances.items() if v < -0.005],
        key=lambda x: -x[1]
    )

    creditors = list(creditors)
    debtors = list(debtors)
    transfers = []

    while creditors and debtors:
        creditor, credit = creditors.pop(0)
        debtor, debt = debtors.pop(0)

        paid = round(min(credit, debt), 2)
        if paid > 0.01:
            transfers.append({
                "from": debtor,
                "to": creditor,
                "amount": paid,
            })

        remaining_credit = round(credit - paid, 2)
        remaining_debt = round(debt - paid, 2)

        if remaining_credit > 0.005:
            creditors.insert(0, (creditor, remaining_credit))
        if remaining_debt > 0.005:
            debtors.insert(0, (debtor, remaining_debt))

    return transfers


def get_shared_budget_status(budget_month: Optional[str] = None) -> dict:
    """
    Shared budget: total shared spend vs shared budget limits for the month.
    Returns category breakdown with each member's contribution.

    Args:
        budget_month: "YYYY-MM" string. Defaults to current month.

    Returns:
        {
            "month": str,
            "total_spend": float,
            "by_category": {category: {"total": float, "by_member": {member: float}}},
            "member_totals": {member: float},
        }
    """
    if budget_month is None:
        budget_month = datetime.now().strftime("%Y-%m")

    expenses = _load_expenses()
    month_expenses = [
        e for e in expenses
        if e.get("date", "").startswith(budget_month)
    ]

    by_category: dict[str, dict] = {}
    member_totals: dict[str, float] = {}
    total_spend = 0.0

    for expense in month_expenses:
        cat = expense.get("category", "other")
        amount = float(expense.get("amount", 0))
        split = expense.get("split", {})
        total_spend += amount

        if cat not in by_category:
            by_category[cat] = {"total": 0.0, "by_member": {}}
        by_category[cat]["total"] = round(by_category[cat]["total"] + amount, 2)

        for member, fraction in split.items():
            member_share = round(amount * fraction, 2)
            by_category[cat]["by_member"][member] = round(
                by_category[cat]["by_member"].get(member, 0.0) + member_share, 2
            )
            member_totals[member] = round(
                member_totals.get(member, 0.0) + member_share, 2
            )

    return {
        "month": budget_month,
        "total_spend": round(total_spend, 2),
        "expense_count": len(month_expenses),
        "by_category": by_category,
        "member_totals": member_totals,
    }


def format_household_summary() -> str:
    """
    Plain-text summary: shared spend, who owes what, settle-up instructions.
    """
    household = _load_household()
    if not household:
        return "No household set up. Use create_household() to get started."

    balance_data = get_shared_balance()
    budget_data = get_shared_budget_status()
    currency = household.get("currency", "EUR")

    cur_sym = "€" if currency == "EUR" else ("£" if currency == "GBP" else currency + " ")
    lines = [
        f"═══ Household: {household.get('name', 'Shared')} ═══",
        f"Members: {', '.join(household.get('members', []))}",
        "",
        f"This month ({budget_data['month']})",
        f"  Total shared spend: {cur_sym}{budget_data['total_spend']:,.2f}",
        f"  Transactions: {budget_data['expense_count']}",
        "",
    ]

    # Category breakdown
    if budget_data["by_category"]:
        lines.append("Spend by category:")
        for cat, data in sorted(budget_data["by_category"].items()):
            lines.append(f"  {cat}: {cur_sym}{data['total']:,.2f}")
        lines.append("")

    # Member balances
    lines.append("Current balances (+ = owed money, - = owes money):")
    balances = balance_data.get("balances", {})
    for member, bal in sorted(balances.items()):
        sign = "+" if bal >= 0 else ""
        lines.append(f"  {member}: {sign}{cur_sym}{bal:,.2f}")
    lines.append("")

    # Settle-up
    settle = balance_data.get("settle_up", [])
    if settle:
        lines.append("Settle up:")
        for transfer in settle:
            lines.append(
                f"  {transfer['from']} → {transfer['to']}: {cur_sym}{transfer['amount']:,.2f}"
            )
    else:
        lines.append("All balances are settled.")

    return "\n".join(lines)
