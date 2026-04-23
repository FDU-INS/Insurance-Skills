#!/usr/bin/env python3
"""
Israeli Bituach Leumi (National Insurance) Benefit Calculator

Standalone utility for estimating Bituach Leumi benefit amounts
including old age pension, unemployment, maternity, and child allowance.

Usage:
    python calculate_benefits.py pension --age 67 --status single
    python calculate_benefits.py unemployment --salary 15000 --age 35 --months 14
    python calculate_benefits.py maternity --salary 20000 --months-employed 12
    python calculate_benefits.py child-allowance --children 3
"""

import argparse
import sys


def calculate_pension(age: int, status: str, years_contributed: int = 30,
                      defer_years: int = 0) -> None:
    """Estimate old age pension (kiztavat zikna)."""
    # 2025 approximate base amounts
    base_single = 1810  # NIS/month
    base_couple = 2730  # NIS/month

    # Check eligibility age
    eligibility_age_men = 67
    eligibility_age_women = 65  # rising to 65 by 2027

    print("=== Old Age Pension (Kiztavat Zikna) Estimate ===\n")

    if age < eligibility_age_women:
        print(f"Age {age}: Not yet eligible for old age pension.")
        print(f"  Men eligible at: {eligibility_age_men}")
        print(f"  Women eligible at: {eligibility_age_women} (2025)")
        return

    base = base_couple if status == "couple" else base_single

    # Seniority supplement: +2% per year of contributions beyond 10 years
    seniority_years = max(0, years_contributed - 10)
    seniority_bonus = min(seniority_years * 0.02, 0.50)  # capped at 50%

    # Deferral bonus: +5% per year deferred after eligibility age
    deferral_bonus = min(defer_years * 0.05, 0.25)  # capped at 25%

    total_bonus = seniority_bonus + deferral_bonus
    estimated_monthly = base * (1 + total_bonus)

    print(f"Status: {status.title()}")
    print(f"Age: {age}")
    print(f"Years contributed: {years_contributed}")
    print(f"Deferral years: {defer_years}")
    print()
    print(f"Base amount: {base:,.0f} NIS/month")
    print(f"Seniority bonus: +{seniority_bonus:.0%} ({seniority_years} years beyond 10)")
    print(f"Deferral bonus: +{deferral_bonus:.0%} ({defer_years} years)")
    print(f"Estimated monthly pension: {estimated_monthly:,.0f} NIS/month")
    print(f"Estimated annual pension: {estimated_monthly * 12:,.0f} NIS/year")
    print()
    print("NOTE: This is an estimate. Actual amounts depend on contribution")
    print("history and current rates. Verify at btl.gov.il or call *6050.")


def calculate_unemployment(salary: float, age: int, months_employed: int,
                           has_dependents: bool = False) -> None:
    """Estimate unemployment benefits (dmei avtala)."""
    print("=== Unemployment Benefits (Dmei Avtala) Estimate ===\n")

    # Check basic eligibility
    if months_employed < 12:
        print(f"Months employed: {months_employed}")
        print("NOT ELIGIBLE: Minimum 12 months of employment in last 18 months required.")
        return

    # Duration based on age and dependents
    if age < 25:
        duration_days = 50
    elif age < 28:
        duration_days = 50 if not has_dependents else 67
    elif age < 35:
        duration_days = 67 if not has_dependents else 100
    elif age < 45:
        duration_days = 100 if not has_dependents else 138
    else:
        duration_days = 138 if not has_dependents else 175

    # Benefit calculation (simplified)
    # First 125 days: Higher percentage, remaining: lower
    daily_wage = salary / 25  # Approximate working days per month
    max_daily = 520  # Approximate maximum daily benefit (2025)

    # First period (~60% of duration): ~80% of daily wage
    # Remaining: ~50% of daily wage
    first_period_days = min(125, duration_days)
    second_period_days = max(0, duration_days - 125)

    first_rate = min(daily_wage * 0.80, max_daily)
    second_rate = min(daily_wage * 0.50, max_daily)

    total_first = first_period_days * first_rate
    total_second = second_period_days * second_rate
    total_benefit = total_first + total_second

    waiting_days = 5

    print(f"Monthly salary: {salary:,.0f} NIS")
    print(f"Age: {age}")
    print(f"Has dependents: {'Yes' if has_dependents else 'No'}")
    print(f"Months employed: {months_employed}")
    print()
    print(f"Waiting period: {waiting_days} days")
    print(f"Benefit duration: {duration_days} days")
    print(f"First period ({first_period_days} days): ~{first_rate:,.0f} NIS/day")
    if second_period_days > 0:
        print(f"Second period ({second_period_days} days): ~{second_rate:,.0f} NIS/day")
    print()
    print(f"Estimated total benefit: {total_benefit:,.0f} NIS")
    print(f"Estimated monthly equivalent: {total_benefit / (duration_days / 25):,.0f} NIS/month")
    print()
    print("NOTE: Actual amounts depend on precise salary history and current")
    print("Bituach Leumi rates. Benefits subject to income tax.")


def calculate_maternity(salary: float, months_employed: int) -> None:
    """Estimate maternity benefits (dmei leida)."""
    print("=== Maternity Benefits (Dmei Leida) Estimate ===\n")

    # Eligibility
    if months_employed < 6:
        print(f"Months employed: {months_employed}")
        print("NOT ELIGIBLE: Minimum 6 months of employment required.")
        return

    # Duration
    if months_employed >= 10:
        weeks = 15
    else:
        weeks = 8

    # Benefit = full salary up to maximum insurable income
    max_daily = 1550  # Approximate maximum daily benefit (2025)
    daily_salary = salary / 30

    daily_benefit = min(daily_salary, max_daily)
    total_days = weeks * 7
    total_benefit = daily_benefit * total_days

    print(f"Monthly salary: {salary:,.0f} NIS")
    print(f"Months employed: {months_employed}")
    print()
    print(f"Leave duration: {weeks} weeks ({total_days} days)")
    print(f"Daily benefit: {daily_benefit:,.0f} NIS/day")
    print(f"Total estimated benefit: {total_benefit:,.0f} NIS")
    print()
    print("Partner leave: Minimum 1 week, option to split remaining weeks.")
    print()
    print("NOTE: Actual benefit based on average of last 3 months salary.")


def calculate_child_allowance(num_children: int) -> None:
    """Estimate child allowance (kiztavat yeladim)."""
    print("=== Child Allowance (Kiztavat Yeladim) Estimate ===\n")

    # 2025 approximate amounts (simplified - actual varies by birth year)
    per_child_base = 170  # NIS/month approximate

    total_monthly = num_children * per_child_base
    total_annual = total_monthly * 12

    print(f"Number of children: {num_children}")
    print(f"Per child (approx): {per_child_base:,.0f} NIS/month")
    print(f"Total monthly: {total_monthly:,.0f} NIS/month")
    print(f"Total annual: {total_annual:,.0f} NIS/year")
    print()
    print("NOTE: Actual amounts vary by child's birth date. Children born")
    print("after June 2003 receive a uniform amount. Verify current rates at btl.gov.il.")


def main():
    parser = argparse.ArgumentParser(
        description="Israeli Bituach Leumi Benefit Calculator"
    )
    subparsers = parser.add_subparsers(dest="command", help="Benefit type")

    # Pension
    pension_parser = subparsers.add_parser("pension", help="Old age pension estimate")
    pension_parser.add_argument("--age", type=int, required=True, help="Current age")
    pension_parser.add_argument("--status", choices=["single", "couple"],
                                default="single", help="Marital status")
    pension_parser.add_argument("--years", type=int, default=30,
                                help="Years of NI contributions")
    pension_parser.add_argument("--defer", type=int, default=0,
                                help="Years of deferred claiming")

    # Unemployment
    unemp_parser = subparsers.add_parser("unemployment", help="Unemployment estimate")
    unemp_parser.add_argument("--salary", type=float, required=True,
                              help="Last monthly salary (NIS)")
    unemp_parser.add_argument("--age", type=int, required=True, help="Current age")
    unemp_parser.add_argument("--months", type=int, required=True,
                              help="Months employed in last 18 months")
    unemp_parser.add_argument("--dependents", action="store_true",
                              help="Has dependents")

    # Maternity
    mat_parser = subparsers.add_parser("maternity", help="Maternity benefit estimate")
    mat_parser.add_argument("--salary", type=float, required=True,
                            help="Monthly salary (NIS)")
    mat_parser.add_argument("--months-employed", type=int, required=True,
                            help="Months employed before due date")

    # Child allowance
    child_parser = subparsers.add_parser("child-allowance", help="Child allowance estimate")
    child_parser.add_argument("--children", type=int, required=True,
                              help="Number of children under 18")

    args = parser.parse_args()

    if args.command == "pension":
        calculate_pension(args.age, args.status, args.years, args.defer)
    elif args.command == "unemployment":
        calculate_unemployment(args.salary, args.age, args.months, args.dependents)
    elif args.command == "maternity":
        calculate_maternity(args.salary, args.months_employed)
    elif args.command == "child-allowance":
        calculate_child_allowance(args.children)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
