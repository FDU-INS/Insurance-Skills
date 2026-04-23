"""
Finance Assistant Recurring Transactions Engine.

Manages recurring income/expenses (rent, salary, subscriptions) and
auto-generates transactions when they're due.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta
from typing import Optional

try:
    from finance_storage import ensure_subdir, load_json, save_json
    from transaction_logger import add_transaction
    from currency import format_money
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import ensure_subdir, load_json, save_json
    from transaction_logger import add_transaction
    from currency import format_money


FREQUENCIES = {
    "daily": 1,
    "weekly": 7,
    "biweekly": 14,
    "monthly": 30,       # Approximate; actual logic uses calendar months
    "quarterly": 91,
    "semi_annual": 182,
    "annual": 365,
}


def _recurrings_path():
    return ensure_subdir("recurring") / "recurring.json"


def _load_recurrings() -> list[dict]:
    data = load_json(_recurrings_path(), default={"items": []})
    return data.get("items", []) if isinstance(data, dict) else []


def _save_recurrings(items: list[dict]) -> None:
    save_json(_recurrings_path(), {
        "last_updated": datetime.now().isoformat(),
        "items": items,
    })


# ── Public API ───────────────────────────────────────────────────────────────

def add_recurring(
    name: str,
    amount: float,
    category: str,
    frequency: str = "monthly",
    account_id: str = "default",
    currency: str = "EUR",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    day_of_month: Optional[int] = None,
    **kwargs,
) -> dict:
    """Add a recurring transaction rule."""
    items = _load_recurrings()
    item = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "amount": round(amount, 2),
        "category": category,
        "type": "income" if amount > 0 else "expense",
        "frequency": frequency,
        "account_id": account_id,
        "currency": currency,
        "start_date": start_date or date.today().isoformat(),
        "end_date": end_date,
        "day_of_month": day_of_month or date.today().day,
        "last_generated": None,
        "status": "active",
        "tags": kwargs.get("tags", []),
        "tax_relevant": kwargs.get("tax_relevant", False),
    }
    items.append(item)
    _save_recurrings(items)
    return item


def get_recurrings() -> list[dict]:
    return _load_recurrings()


def update_recurring(recurring_id: str, updates: dict) -> Optional[dict]:
    items = _load_recurrings()
    for i, item in enumerate(items):
        if item["id"] == recurring_id:
            item.update(updates)
            items[i] = item
            _save_recurrings(items)
            return item
    return None


def delete_recurring(recurring_id: str) -> bool:
    items = _load_recurrings()
    filtered = [i for i in items if i["id"] != recurring_id]
    if len(filtered) == len(items):
        return False
    _save_recurrings(filtered)
    return True


def pause_recurring(recurring_id: str) -> Optional[dict]:
    return update_recurring(recurring_id, {"status": "paused"})


def resume_recurring(recurring_id: str) -> Optional[dict]:
    return update_recurring(recurring_id, {"status": "active"})


def generate_due_transactions(as_of: Optional[str] = None) -> dict:
    """
    Check all active recurrings and generate transactions for any that are due.
    Returns a summary of what was generated.
    """
    today = date.fromisoformat(as_of) if as_of else date.today()
    items = _load_recurrings()
    generated = []
    skipped = []

    for item in items:
        if item.get("status") != "active":
            continue

        # Check end date
        end = item.get("end_date")
        if end and date.fromisoformat(end) < today:
            continue

        start = date.fromisoformat(item["start_date"])
        if start > today:
            continue

        # Determine due dates since last generation
        last_gen = date.fromisoformat(item["last_generated"]) if item.get("last_generated") else start - timedelta(days=1)
        due_dates = _calculate_due_dates(item, last_gen, today)

        for due_date in due_dates:
            txn = add_transaction(
                date=due_date.isoformat(),
                type=item["type"],
                amount=item["amount"],
                category=item["category"],
                description=f"[recurring] {item['name']}",
                account_id=item["account_id"],
                currency=item["currency"],
                is_recurring=True,
                tags=item.get("tags", []),
                tax_relevant=item.get("tax_relevant", False),
            )
            generated.append({
                "recurring_id": item["id"],
                "name": item["name"],
                "date": due_date.isoformat(),
                "amount": item["amount"],
            })

        if due_dates:
            item["last_generated"] = max(due_dates).isoformat()
        else:
            skipped.append(item["id"])

    _save_recurrings(items)

    return {
        "as_of": today.isoformat(),
        "generated_count": len(generated),
        "generated": generated,
        "skipped_count": len(skipped),
    }


def _calculate_due_dates(item: dict, after: date, up_to: date) -> list[date]:
    """Calculate all due dates for a recurring item between after and up_to."""
    freq = item["frequency"]
    day_of_month = item.get("day_of_month", 1)
    start = date.fromisoformat(item["start_date"])
    dates = []

    if freq == "monthly":
        # Jump directly to the first month on or after `after` to avoid looping from epoch
        from math import ceil
        months_elapsed = (after.year - start.year) * 12 + (after.month - start.month)
        months_elapsed = max(0, months_elapsed)
        year_offset, month_offset = divmod(start.month - 1 + months_elapsed, 12)
        current = start.replace(year=start.year + year_offset, month=month_offset + 1, day=1)
        while current <= up_to:
            try:
                d = current.replace(day=min(day_of_month, 28))
            except ValueError:
                d = current.replace(day=28)
            if d > after and d <= up_to:
                dates.append(d)
            # Next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1, day=1)
            else:
                current = current.replace(month=current.month + 1, day=1)

    elif freq == "quarterly":
        # Jump to a quarter on or after `after`
        from math import ceil
        quarters_elapsed = ceil(((after.year - start.year) * 12 + (after.month - start.month)) / 3)
        quarters_elapsed = max(0, quarters_elapsed)
        month_offset = start.month - 1 + quarters_elapsed * 3
        year_offset, month_rem = divmod(month_offset, 12)
        current = start.replace(year=start.year + year_offset, month=month_rem + 1, day=1)
        while current <= up_to:
            try:
                d = current.replace(day=min(day_of_month, 28))
            except ValueError:
                d = current.replace(day=28)
            if d > after and d <= up_to:
                dates.append(d)
            month = current.month + 3
            year = current.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1
            current = date(year, month, 1)

    elif freq == "annual":
        current = start
        while current <= up_to:
            if current > after and current <= up_to:
                dates.append(current)
            current = current.replace(year=current.year + 1)

    elif freq in FREQUENCIES:
        interval = FREQUENCIES[freq]
        from math import ceil
        if start < after:
            intervals_to_skip = ceil((after - start).days / interval)
            current = start + timedelta(days=intervals_to_skip * interval)
        else:
            current = start
        while current <= up_to:
            if current > after:
                dates.append(current)
            current += timedelta(days=interval)

    return dates


def get_upcoming(days: int = 30) -> list[dict]:
    """Preview upcoming recurring transactions in the next N days."""
    today = date.today()
    future = today + timedelta(days=days)
    items = _load_recurrings()
    upcoming = []

    for item in items:
        if item.get("status") != "active":
            continue
        last_gen = date.fromisoformat(item["last_generated"]) if item.get("last_generated") else today - timedelta(days=1)
        dues = _calculate_due_dates(item, last_gen, future)
        for d in dues:
            upcoming.append({
                "name": item["name"],
                "amount": item["amount"],
                "category": item["category"],
                "due_date": d.isoformat(),
                "recurring_id": item["id"],
            })

    return sorted(upcoming, key=lambda x: x["due_date"])


def format_recurrings_display() -> str:
    items = _load_recurrings()
    if not items:
        return "No recurring transactions set up."

    lines = ["═══ Recurring Transactions ═══\n"]
    total_monthly_income = 0.0
    total_monthly_expense = 0.0

    for item in sorted(items, key=lambda x: x.get("amount", 0)):
        status = item.get("status", "active")
        freq = item.get("frequency", "monthly")
        amt = float(item["amount"])
        cur = item.get("currency", "EUR")
        sign = "+" if amt >= 0 else ""

        # Estimate monthly equivalent
        monthly_equiv = _monthly_equivalent(amt, freq)
        if amt >= 0:
            total_monthly_income += monthly_equiv
        else:
            total_monthly_expense += abs(monthly_equiv)

        lines.append(f"  {item['name']} [{status}]")
        lines.append(f"    {sign}{format_money(amt, cur)} / {freq}  "
                     f"(~{format_money(monthly_equiv, cur)}/mo)")

    lines.append(f"\n  Monthly recurring income:  +{format_money(total_monthly_income, 'EUR')}")
    lines.append(f"  Monthly recurring expense: -{format_money(total_monthly_expense, 'EUR')}")
    lines.append(f"  Net recurring:             {format_money(total_monthly_income - total_monthly_expense, 'EUR')}")

    return "\n".join(lines)


def _monthly_equivalent(amount: float, frequency: str) -> float:
    multipliers = {
        "daily": 30, "weekly": 4.33, "biweekly": 2.17,
        "monthly": 1, "quarterly": 1/3, "semi_annual": 1/6, "annual": 1/12,
    }
    return round(amount * multipliers.get(frequency, 1), 2)
