#!/usr/bin/env python3
"""
Israeli Vehicle Test Reminder

Calculates when the next annual vehicle test (טסט) is due based on
registration date and vehicle age.

Usage:
    python test-reminder.py --reg-date 2023-06-15
    python test-reminder.py --reg-date 2023-06-15 --is-rental
    python test-reminder.py --help
"""

import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys

PRIVATE_EXEMPT_YEARS = 3
RENTAL_EXEMPT_YEARS = 2


def calculate_next_test(reg_date_str: str, is_rental: bool = False) -> dict:
    """Calculate the next vehicle test date."""
    try:
        reg_date = datetime.strptime(reg_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{reg_date_str}'. Use YYYY-MM-DD.")
        sys.exit(1)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    vehicle_age_years = relativedelta(today, reg_date).years

    exempt_years = RENTAL_EXEMPT_YEARS if is_rental else PRIVATE_EXEMPT_YEARS

    if vehicle_age_years < exempt_years:
        first_test = reg_date + relativedelta(years=exempt_years)
        days_until = (first_test - today).days
        return {
            "reg_date": reg_date.strftime("%Y-%m-%d"),
            "vehicle_age_years": vehicle_age_years,
            "exempt": True,
            "exempt_until": first_test.strftime("%Y-%m-%d"),
            "days_until_first_test": max(days_until, 0),
            "next_test_date": first_test.strftime("%Y-%m-%d"),
            "is_over_15": False,
        }

    # Find the next test date (annual from exemption end)
    first_test = reg_date + relativedelta(years=exempt_years)
    next_test = first_test
    while next_test < today:
        next_test += relativedelta(years=1)

    days_until = (next_test - today).days
    is_over_15 = vehicle_age_years >= 15

    return {
        "reg_date": reg_date.strftime("%Y-%m-%d"),
        "vehicle_age_years": vehicle_age_years,
        "exempt": False,
        "next_test_date": next_test.strftime("%Y-%m-%d"),
        "days_until_test": max(days_until, 0),
        "is_over_15": is_over_15,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Calculate next Israeli vehicle test date"
    )
    parser.add_argument(
        "--reg-date",
        required=True,
        help="Vehicle first registration date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--is-rental",
        action="store_true",
        help="Vehicle is rental/leased (2-year exemption instead of 3)",
    )

    args = parser.parse_args()
    result = calculate_next_test(args.reg_date, args.is_rental)

    vehicle_type = "Rental/Leased" if args.is_rental else "Private"
    exempt_years = RENTAL_EXEMPT_YEARS if args.is_rental else PRIVATE_EXEMPT_YEARS

    print(f"\n{'='*50}")
    print(f"  Vehicle Test Reminder")
    print(f"{'='*50}")
    print(f"  Registration date: {result['reg_date']}")
    print(f"  Vehicle type:      {vehicle_type}")
    print(f"  Vehicle age:       {result['vehicle_age_years']} years")
    print(f"  Exempt period:     {exempt_years} years")

    if result["exempt"]:
        print(f"  Status:            EXEMPT (new vehicle)")
        print(f"  First test due:    {result['next_test_date']}")
        print(f"  Days until:        {result['days_until_first_test']} days")
    else:
        print(f"  Next test due:     {result['next_test_date']}")
        print(f"  Days until:        {result['days_until_test']} days")
        if result["is_over_15"]:
            print(f"  WARNING:           Vehicle is 15+ years old")
            print(f"                     Brake check at licensed garage required BEFORE test")

    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
