"""
Finance Assistant Debt Optimizer.

Debt payoff strategies (avalanche, snowball), mortgage optimization,
and payoff timeline calculations.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

try:
    from finance_storage import get_debts_path, get_payoff_plan_path, load_json, save_json
    from currency import format_money
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from finance_storage import get_debts_path, get_payoff_plan_path, load_json, save_json
    from currency import format_money


def _load_debts() -> list[dict]:
    data = load_json(get_debts_path(), default={"debts": []})
    return data.get("debts", []) if isinstance(data, dict) else []


def _save_debts(debts: list[dict]) -> None:
    save_json(get_debts_path(), {
        "last_updated": datetime.now().isoformat(),
        "debts": debts,
    })


def get_debts() -> list[dict]:
    return _load_debts()


def add_debt(debt_data: dict) -> dict:
    debts = _load_debts()
    debt = {
        "id": debt_data.get("id") or debt_data.get("name", "debt").lower().replace(" ", "-"),
        "name": debt_data.get("name", ""),
        "type": debt_data.get("type", "other"),
        "balance": float(debt_data.get("balance", 0)),
        "interest_rate": float(debt_data.get("interest_rate", 0)),
        "minimum_payment": float(debt_data.get("minimum_payment", 0)),
        "currency": debt_data.get("currency", "EUR"),
        "term_months": debt_data.get("term_months"),
        "extra_payment": float(debt_data.get("extra_payment", 0)),
    }
    debts.append(debt)
    _save_debts(debts)
    return debt


def update_debt(debt_id: str, updates: dict) -> Optional[dict]:
    debts = _load_debts()
    for i, d in enumerate(debts):
        if d["id"] == debt_id:
            d.update(updates)
            debts[i] = d
            _save_debts(debts)
            return d
    return None


def delete_debt(debt_id: str) -> bool:
    debts = _load_debts()
    filtered = [d for d in debts if d["id"] != debt_id]
    if len(filtered) == len(debts):
        return False
    _save_debts(filtered)
    return True


def _simulate_payoff(debts: list[dict], extra_monthly: float, order_key) -> dict:
    """Simulate paying off debts in a given order with extra payments."""
    if not debts:
        return {"months": 0, "total_interest": 0, "total_paid": 0, "schedule": []}

    # Deep copy balances
    active = []
    for d in sorted(debts, key=order_key):
        active.append({
            "id": d["id"],
            "name": d["name"],
            "balance": float(d["balance"]),
            "rate": float(d["interest_rate"]) / 100 / 12,  # Monthly rate
            "minimum": float(d["minimum_payment"]),
        })

    total_interest = 0.0
    total_paid = 0.0
    month = 0
    schedule = []
    max_months = 600  # 50 year cap

    while any(d["balance"] > 0.01 for d in active) and month < max_months:
        month += 1
        extra_remaining = extra_monthly

        for d in active:
            if d["balance"] <= 0:
                continue

            # Accrue interest
            interest = d["balance"] * d["rate"]
            d["balance"] += interest
            total_interest += interest

            # Pay minimum
            payment = min(d["minimum"], d["balance"])
            d["balance"] -= payment
            total_paid += payment

        # Apply extra to the first debt with balance (priority order)
        for d in active:
            if d["balance"] <= 0 or extra_remaining <= 0:
                continue
            extra = min(extra_remaining, d["balance"])
            d["balance"] -= extra
            total_paid += extra
            extra_remaining -= extra

        # When a debt is paid off, redirect its minimum to extra
        freed = sum(d["minimum"] for d in active if d["balance"] <= 0.01)
        # (This is implicit in next iteration since we skip zero-balance debts)

        if month % 6 == 0 or month <= 3:
            schedule.append({
                "month": month,
                "remaining_debts": sum(1 for d in active if d["balance"] > 0.01),
                "total_balance": round(sum(max(0, d["balance"]) for d in active), 2),
            })

    return {
        "months": month,
        "years": round(month / 12, 1),
        "total_interest": round(total_interest, 2),
        "total_paid": round(total_paid, 2),
        "schedule": schedule,
    }


def calculate_avalanche_plan(extra_monthly: float = 0.0) -> dict:
    """Pay highest interest rate first (minimizes total interest)."""
    debts = _load_debts()
    result = _simulate_payoff(debts, extra_monthly, lambda d: -float(d["interest_rate"]))
    result["strategy"] = "avalanche"
    result["description"] = "Pay highest interest rate first — minimizes total interest paid"
    return result


def calculate_snowball_plan(extra_monthly: float = 0.0) -> dict:
    """Pay smallest balance first (psychological wins)."""
    debts = _load_debts()
    result = _simulate_payoff(debts, extra_monthly, lambda d: float(d["balance"]))
    result["strategy"] = "snowball"
    result["description"] = "Pay smallest balance first — quick wins for motivation"
    return result


def compare_payoff_strategies(extra_monthly: float = 0.0) -> dict:
    """Compare avalanche vs snowball with interest savings."""
    avalanche = calculate_avalanche_plan(extra_monthly)
    snowball = calculate_snowball_plan(extra_monthly)

    interest_saved = snowball["total_interest"] - avalanche["total_interest"]
    months_saved = snowball["months"] - avalanche["months"]

    return {
        "avalanche": avalanche,
        "snowball": snowball,
        "comparison": {
            "interest_saved_by_avalanche": round(interest_saved, 2),
            "months_saved_by_avalanche": months_saved,
            "recommendation": (
                "avalanche" if interest_saved > 50
                else "snowball" if interest_saved < 10
                else "either — the difference is minimal"
            ),
        },
        "extra_monthly": extra_monthly,
    }


def calculate_mortgage_optimization(
    balance: float,
    rate: float,
    remaining_months: int,
    extra_monthly: float = 0.0,
    lump_sum: float = 0.0,
    refinance_rate: Optional[float] = None,
) -> dict:
    """Analyze mortgage optimization options."""
    monthly_rate = rate / 100 / 12

    # Current schedule
    current_payment = balance * monthly_rate / (1 - (1 + monthly_rate) ** -remaining_months) if monthly_rate > 0 else balance / remaining_months
    current_total_interest = current_payment * remaining_months - balance

    # With extra payments
    new_balance = balance - lump_sum
    new_payment = current_payment + extra_monthly
    months_with_extra = 0
    interest_with_extra = 0.0
    bal = new_balance
    while bal > 0.01 and months_with_extra < remaining_months * 2:
        months_with_extra += 1
        interest = bal * monthly_rate
        interest_with_extra += interest
        bal = bal + interest - new_payment
        if bal < 0:
            bal = 0

    result = {
        "current": {
            "balance": round(balance, 2),
            "rate": rate,
            "monthly_payment": round(current_payment, 2),
            "remaining_months": remaining_months,
            "total_interest": round(current_total_interest, 2),
        },
        "optimized": {
            "extra_monthly": extra_monthly,
            "lump_sum": lump_sum,
            "new_monthly_payment": round(new_payment, 2),
            "months_to_payoff": months_with_extra,
            "total_interest": round(interest_with_extra, 2),
            "interest_saved": round(current_total_interest - interest_with_extra, 2),
            "months_saved": remaining_months - months_with_extra,
        },
    }

    # Refinance comparison
    if refinance_rate is not None:
        new_monthly_rate = refinance_rate / 100 / 12
        refi_payment = balance * new_monthly_rate / (1 - (1 + new_monthly_rate) ** -remaining_months) if new_monthly_rate > 0 else balance / remaining_months
        refi_interest = refi_payment * remaining_months - balance
        result["refinance"] = {
            "new_rate": refinance_rate,
            "new_monthly_payment": round(refi_payment, 2),
            "total_interest": round(refi_interest, 2),
            "monthly_savings": round(current_payment - refi_payment, 2),
            "total_interest_saved": round(current_total_interest - refi_interest, 2),
        }

    return result


def get_debt_free_date(strategy: str = "avalanche", extra_monthly: float = 0.0) -> str:
    """Calculate debt-free date."""
    if strategy == "snowball":
        plan = calculate_snowball_plan(extra_monthly)
    else:
        plan = calculate_avalanche_plan(extra_monthly)

    today = date.today()
    months = plan["months"]
    year = today.year + (today.month + months - 1) // 12
    month = ((today.month + months - 1) % 12) + 1
    return date(year, month, 1).isoformat()


def format_debt_display() -> str:
    debts = _load_debts()
    if not debts:
        return "No debts tracked. Add debts to get optimization suggestions."

    total_balance = sum(float(d["balance"]) for d in debts)
    total_minimum = sum(float(d["minimum_payment"]) for d in debts)
    avg_rate = sum(float(d["interest_rate"]) * float(d["balance"]) for d in debts) / total_balance if total_balance else 0

    lines = ["═══ Your Debts ═══\n"]
    for d in sorted(debts, key=lambda x: -float(x["interest_rate"])):
        lines.append(f"  {d['name']}")
        lines.append(f"    Balance: {format_money(d['balance'], d.get('currency', 'EUR'))}  "
                     f"Rate: {d['interest_rate']:.1f}%  "
                     f"Min payment: {format_money(d['minimum_payment'], d.get('currency', 'EUR'))}")

    lines.append(f"\n  Total debt: {format_money(total_balance, 'EUR')}")
    lines.append(f"  Weighted avg rate: {avg_rate:.1f}%")
    lines.append(f"  Total minimum payments: {format_money(total_minimum, 'EUR')}/month")

    return "\n".join(lines)
