#!/usr/bin/env python3
"""
Life Insurance Needs Calculator - US Edition

Calculates life insurance coverage needs using multiple methods:
1. Human Life Value (HLV) method
2. Needs-Based method (DIME: Debt, Income, Mortgage, Education)
3. Income Multiplier method

Produces comprehensive analysis with self-verification.

Usage:
    python life_insurance_needs.py \\
        --annual-income 100000 \\
        --age 35 \\
        --years-to-retirement 30 \\
        --mortgage-balance 300000 \\
        --other-debt 25000 \\
        --education-expenses 200000 \\
        --final-expenses 15000 \\
        --existing-coverage 200000 \\
        --liquid-assets 50000 \\
        --output life_insurance_analysis.json

Author: Financial Services Skills Project
Version: 1.0.0
Last Updated: 2025-01-18
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, Any


class LifeInsuranceCalculator:
    """Calculate life insurance needs using multiple methodologies."""

    def __init__(self, current_year: int = 2025):
        """Initialize calculator with current year."""
        self.current_year = current_year

        # Default assumptions (can be overridden)
        self.default_discount_rate = 0.04  # 4% discount rate for PV calculations
        self.default_inflation_rate = 0.025  # 2.5% inflation
        self.default_income_replacement_years = 15  # Years to replace income
        self.default_income_replacement_percentage = 0.70  # 70% replacement

    def _validate_inputs(
        self,
        annual_income: float,
        age: int,
        years_to_retirement: int,
        mortgage_balance: float,
        other_debt: float,
        education_expenses: float,
        final_expenses: float,
        existing_coverage: float,
        liquid_assets: float,
        spouse_income: float,
        income_replacement_years: int,
        income_replacement_percentage: float,
        discount_rate: float,
        inflation_rate: float
    ) -> None:
        """Validate all inputs and raise ValueError if invalid."""

        if annual_income < 0:
            raise ValueError("Annual income cannot be negative")

        if age < 18 or age > 100:
            raise ValueError("Age must be between 18 and 100")

        if years_to_retirement < 0 or years_to_retirement > 50:
            raise ValueError("Years to retirement must be between 0 and 50")

        if age + years_to_retirement > 100:
            raise ValueError("Retirement age (current age + years) cannot exceed 100")

        if mortgage_balance < 0:
            raise ValueError("Mortgage balance cannot be negative")

        if other_debt < 0:
            raise ValueError("Other debt cannot be negative")

        if education_expenses < 0:
            raise ValueError("Education expenses cannot be negative")

        if final_expenses < 0:
            raise ValueError("Final expenses cannot be negative")

        if existing_coverage < 0:
            raise ValueError("Existing coverage cannot be negative")

        if liquid_assets < 0:
            raise ValueError("Liquid assets cannot be negative")

        if spouse_income < 0:
            raise ValueError("Spouse income cannot be negative")

        if income_replacement_years < 1 or income_replacement_years > 40:
            raise ValueError("Income replacement years must be between 1 and 40")

        if income_replacement_percentage <= 0 or income_replacement_percentage > 1.0:
            raise ValueError("Income replacement percentage must be between 0 and 1.0")

        if discount_rate < 0 or discount_rate > 0.20:
            raise ValueError("Discount rate must be between 0 and 0.20 (20%)")

        if inflation_rate < 0 or inflation_rate > 0.15:
            raise ValueError("Inflation rate must be between 0 and 0.15 (15%)")

    def _calculate_human_life_value(
        self,
        annual_income: float,
        years_to_retirement: int,
        discount_rate: float,
        income_replacement_percentage: float
    ) -> float:
        """
        Calculate Human Life Value (present value of future earnings).

        HLV = PV of future income stream discounted to present
        """

        # Income to replace (typically 70% - some expenses go away at death)
        income_to_replace = annual_income * income_replacement_percentage

        # Calculate present value of income stream
        if abs(discount_rate) < 0.0001:
            # Edge case: zero discount rate (simple multiplication)
            return income_to_replace * years_to_retirement

        # Standard PV of annuity formula
        pv_factor = (1 - (1 + discount_rate) ** -years_to_retirement) / discount_rate
        hlv = income_to_replace * pv_factor

        return hlv

    def _calculate_needs_based(
        self,
        annual_income: float,
        income_replacement_years: int,
        income_replacement_percentage: float,
        mortgage_balance: float,
        other_debt: float,
        education_expenses: float,
        final_expenses: float,
        spouse_income: float,
        inflation_rate: float
    ) -> Dict[str, float]:
        """
        Calculate needs-based insurance (DIME method + income replacement).

        Components:
        D - Debt (mortgage, other debts)
        I - Income replacement
        M - Mortgage (included in Debt)
        E - Education expenses

        Plus: Final expenses, emergency fund
        Minus: Spouse income contribution, existing assets
        """

        # 1. Debt payoff
        total_debt = mortgage_balance + other_debt

        # 2. Income replacement
        # Annual income needed
        income_needed = annual_income * income_replacement_percentage

        # Adjust for spouse income (if spouse works, need less insurance)
        income_gap = max(0, income_needed - spouse_income)

        # Total income replacement needed (simple multiplication, not discounted)
        # Using nominal dollars (includes inflation implicitly)
        income_replacement_need = income_gap * income_replacement_years

        # 3. Education expenses (assume future, so adjust for inflation)
        # Simple approach: current estimate of total education costs
        education_need = education_expenses

        # 4. Final expenses
        final_expense_need = final_expenses

        # 5. Emergency fund (6 months expenses)
        emergency_fund = (annual_income * 0.5) / 2  # 6 months of 50% of income

        # Total needs
        total_needs = (
            total_debt +
            income_replacement_need +
            education_need +
            final_expense_need +
            emergency_fund
        )

        return {
            "debt_payoff": total_debt,
            "mortgage_balance": mortgage_balance,
            "other_debt": other_debt,
            "income_replacement": income_replacement_need,
            "income_gap_annual": income_gap,
            "education_expenses": education_need,
            "final_expenses": final_expense_need,
            "emergency_fund": emergency_fund,
            "total_needs": total_needs
        }

    def _calculate_income_multiplier(
        self,
        annual_income: float,
        multiplier: float = 10.0
    ) -> float:
        """
        Calculate insurance need using simple income multiplier rule of thumb.

        Common multipliers: 7-10x annual income
        """
        return annual_income * multiplier

    def _calculate_net_need(
        self,
        total_needs: float,
        existing_coverage: float,
        liquid_assets: float
    ) -> Dict[str, float]:
        """
        Calculate net insurance need after existing coverage and assets.
        """

        # Assets that can be used
        available_assets = liquid_assets

        # Net need
        net_need = total_needs - existing_coverage - available_assets

        # Ensure not negative
        net_need = max(0, net_need)

        return {
            "gross_need": total_needs,
            "existing_coverage": existing_coverage,
            "liquid_assets": available_assets,
            "net_need": net_need,
            "coverage_gap": max(0, total_needs - existing_coverage),
            "total_available": existing_coverage + available_assets
        }

    def _verify_calculation(
        self,
        needs_based_total: float,
        hlv: float,
        income_multiplier: float
    ) -> Dict[str, Any]:
        """
        Verify calculations using multiple methods comparison.

        All three methods should be within reasonable range of each other.
        """

        # Calculate average and spread
        values = [needs_based_total, hlv, income_multiplier]
        average = sum(values) / len(values)
        min_value = min(values)
        max_value = max(values)

        # Check if spread is reasonable (within 50% of average)
        spread_percentage = (max_value - min_value) / average if average > 0 else 0

        # Verification passes if spread is less than 50%
        # (methods can differ, but shouldn't be wildly different)
        verification_passed = spread_percentage < 0.50

        return {
            "verification_passed": verification_passed,
            "needs_based_total": needs_based_total,
            "human_life_value": hlv,
            "income_multiplier": income_multiplier,
            "average_need": average,
            "min_need": min_value,
            "max_need": max_value,
            "spread_percentage": spread_percentage,
            "explanation": (
                "All three methods agree within reasonable range"
                if verification_passed
                else "Methods show significant divergence - review inputs and assumptions"
            )
        }

    def _generate_warnings(
        self,
        net_need: float,
        annual_income: float,
        age: int,
        existing_coverage: float
    ) -> list:
        """Generate warnings based on analysis results."""

        warnings = []

        # High coverage need (>15x income)
        if net_need > annual_income * 15:
            warnings.append(
                f"Very high coverage need (${net_need:,.0f}, {net_need/annual_income:.1f}x income). "
                "Consider term life insurance for affordability."
            )

        # Significant coverage gap
        coverage_ratio = existing_coverage / net_need if net_need > 0 else 1.0
        if coverage_ratio < 0.5 and net_need > 100000:
            warnings.append(
                f"Large coverage gap: existing ${existing_coverage:,.0f} vs need ${net_need:,.0f}. "
                f"You are {(1-coverage_ratio)*100:.0f}% underinsured."
            )

        # Age considerations
        if age > 55 and net_need > annual_income * 5:
            warnings.append(
                "Over age 55 with significant insurance need. "
                "Life insurance becomes more expensive - consider alternatives like annuities."
            )

        if age < 35 and existing_coverage < annual_income * 5:
            warnings.append(
                "Young with low coverage. "
                "Now is best time to buy term insurance (rates lowest, guaranteed insurability)."
            )

        # No coverage warning
        if existing_coverage == 0 and annual_income > 0:
            warnings.append(
                "No existing life insurance coverage. "
                "Strongly recommend obtaining coverage to protect dependents."
            )

        return warnings

    def calculate_life_insurance_needs(
        self,
        annual_income: float,
        age: int,
        years_to_retirement: int = None,
        mortgage_balance: float = 0,
        other_debt: float = 0,
        education_expenses: float = 0,
        final_expenses: float = 15000,
        existing_coverage: float = 0,
        liquid_assets: float = 0,
        spouse_income: float = 0,
        income_replacement_years: int = None,
        income_replacement_percentage: float = None,
        discount_rate: float = None,
        inflation_rate: float = None,
        income_multiplier: float = 10.0
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive life insurance needs analysis.

        Returns dict with all calculations, verification, and warnings.
        """

        # Set defaults
        if years_to_retirement is None:
            years_to_retirement = max(1, 65 - age)

        if income_replacement_years is None:
            income_replacement_years = self.default_income_replacement_years

        if income_replacement_percentage is None:
            income_replacement_percentage = self.default_income_replacement_percentage

        if discount_rate is None:
            discount_rate = self.default_discount_rate

        if inflation_rate is None:
            inflation_rate = self.default_inflation_rate

        # Validate inputs
        self._validate_inputs(
            annual_income, age, years_to_retirement,
            mortgage_balance, other_debt, education_expenses, final_expenses,
            existing_coverage, liquid_assets, spouse_income,
            income_replacement_years, income_replacement_percentage,
            discount_rate, inflation_rate
        )

        # Calculate using three methods

        # 1. Human Life Value
        hlv = self._calculate_human_life_value(
            annual_income, years_to_retirement, discount_rate, income_replacement_percentage
        )

        # 2. Needs-Based (DIME)
        needs_based = self._calculate_needs_based(
            annual_income, income_replacement_years, income_replacement_percentage,
            mortgage_balance, other_debt, education_expenses, final_expenses,
            spouse_income, inflation_rate
        )

        # 3. Income Multiplier
        income_mult = self._calculate_income_multiplier(annual_income, income_multiplier)

        # Calculate net need (using needs-based as primary method)
        net_need_analysis = self._calculate_net_need(
            needs_based["total_needs"],
            existing_coverage,
            liquid_assets
        )

        # Verify calculations
        verification = self._verify_calculation(
            needs_based["total_needs"],
            hlv,
            income_mult
        )

        # Generate warnings
        warnings = self._generate_warnings(
            net_need_analysis["net_need"],
            annual_income,
            age,
            existing_coverage
        )

        # Compile results
        result = {
            "calculation_date": datetime.now().isoformat(),
            "inputs": {
                "annual_income": float(annual_income),
                "age": age,
                "years_to_retirement": years_to_retirement,
                "retirement_age": age + years_to_retirement,
                "mortgage_balance": float(mortgage_balance),
                "other_debt": float(other_debt),
                "education_expenses": float(education_expenses),
                "final_expenses": float(final_expenses),
                "existing_coverage": float(existing_coverage),
                "liquid_assets": float(liquid_assets),
                "spouse_income": float(spouse_income),
                "income_replacement_years": income_replacement_years,
                "income_replacement_percentage": income_replacement_percentage,
                "discount_rate": discount_rate,
                "inflation_rate": inflation_rate,
                "income_multiplier": income_multiplier
            },
            "method_1_human_life_value": {
                "description": "Present value of future earnings discounted to today",
                "calculated_need": round(hlv, 2),
                "formula": "PV = Income × Replacement% × [(1-(1+r)^-n)/r]",
                "assumptions": f"{discount_rate*100:.1f}% discount rate, {income_replacement_percentage*100:.0f}% replacement"
            },
            "method_2_needs_based": {
                "description": "DIME method: Debt + Income + Mortgage + Education + Emergency",
                "components": {
                    k: round(v, 2) for k, v in needs_based.items()
                },
                "calculated_need": round(needs_based["total_needs"], 2)
            },
            "method_3_income_multiplier": {
                "description": f"Rule of thumb: {income_multiplier}x annual income",
                "calculated_need": round(income_mult, 2),
                "note": "Simple approach, does not account for specific circumstances"
            },
            "recommended_coverage": {
                "primary_method": "needs_based",
                "gross_need": round(needs_based["total_needs"], 2),
                "existing_coverage": round(existing_coverage, 2),
                "liquid_assets": round(liquid_assets, 2),
                "net_additional_need": round(net_need_analysis["net_need"], 2),
                "coverage_gap": round(net_need_analysis["coverage_gap"], 2)
            },
            "verification": verification,
            "warnings": warnings,
            "recommendations": self._generate_recommendations(
                net_need_analysis["net_need"],
                annual_income,
                age
            )
        }

        return result

    def _generate_recommendations(
        self,
        net_need: float,
        annual_income: float,
        age: int
    ) -> list:
        """Generate actionable recommendations."""

        recommendations = []

        if net_need > 0:
            # Recommend term life for most cases
            if age < 60:
                term_length = min(30, max(10, 65 - age))
                recommendations.append(
                    f"Consider {term_length}-year term life insurance for ${net_need:,.0f}. "
                    "Most affordable option for temporary needs."
                )

            # Permanent life if older or estate planning
            if age >= 55 or net_need < annual_income * 3:
                recommendations.append(
                    "Consider permanent life insurance (whole life or universal life) "
                    "if need is permanent or for estate planning purposes."
                )

            # Layering strategy
            if net_need > annual_income * 10:
                recommendations.append(
                    "Consider 'laddering' term policies: e.g., $500k for 30 years + "
                    "$500k for 20 years + $500k for 10 years. Reduces cost as needs decrease."
                )
        else:
            recommendations.append(
                "Current coverage appears adequate based on needs analysis. "
                "Review annually as circumstances change."
            )

        # Always recommend review triggers
        recommendations.append(
            "Review life insurance needs when: marriage/divorce, birth/adoption, "
            "home purchase, career change, or every 3-5 years minimum."
        )

        return recommendations


def main():
    """Command-line interface for life insurance calculator."""

    parser = argparse.ArgumentParser(
        description="Calculate life insurance needs using multiple methods"
    )

    # Required inputs
    parser.add_argument("--annual-income", type=float, required=True,
                       help="Annual gross income")
    parser.add_argument("--age", type=int, required=True,
                       help="Current age")

    # Optional inputs
    parser.add_argument("--years-to-retirement", type=int,
                       help="Years until retirement (default: 65 - age)")
    parser.add_argument("--mortgage-balance", type=float, default=0,
                       help="Outstanding mortgage balance")
    parser.add_argument("--other-debt", type=float, default=0,
                       help="Other debts (car loans, credit cards, etc.)")
    parser.add_argument("--education-expenses", type=float, default=0,
                       help="Estimated total education costs for children")
    parser.add_argument("--final-expenses", type=float, default=15000,
                       help="Final expenses (funeral, burial, etc.)")
    parser.add_argument("--existing-coverage", type=float, default=0,
                       help="Existing life insurance coverage")
    parser.add_argument("--liquid-assets", type=float, default=0,
                       help="Liquid assets (savings, investments)")
    parser.add_argument("--spouse-income", type=float, default=0,
                       help="Spouse's annual income")
    parser.add_argument("--income-replacement-years", type=int,
                       help="Years to replace income (default: 15)")
    parser.add_argument("--income-replacement-percentage", type=float,
                       help="Percentage of income to replace (default: 0.70)")
    parser.add_argument("--discount-rate", type=float,
                       help="Discount rate for HLV calculation (default: 0.04)")
    parser.add_argument("--inflation-rate", type=float,
                       help="Expected inflation rate (default: 0.025)")
    parser.add_argument("--income-multiplier", type=float, default=10.0,
                       help="Income multiplier for rule of thumb (default: 10.0)")

    # Output
    parser.add_argument("--output", type=str, default="life_insurance_analysis.json",
                       help="Output JSON file path")

    args = parser.parse_args()

    # Create calculator
    calc = LifeInsuranceCalculator()

    try:
        # Calculate
        result = calc.calculate_life_insurance_needs(
            annual_income=args.annual_income,
            age=args.age,
            years_to_retirement=args.years_to_retirement,
            mortgage_balance=args.mortgage_balance,
            other_debt=args.other_debt,
            education_expenses=args.education_expenses,
            final_expenses=args.final_expenses,
            existing_coverage=args.existing_coverage,
            liquid_assets=args.liquid_assets,
            spouse_income=args.spouse_income,
            income_replacement_years=args.income_replacement_years,
            income_replacement_percentage=args.income_replacement_percentage,
            discount_rate=args.discount_rate,
            inflation_rate=args.inflation_rate,
            income_multiplier=args.income_multiplier
        )

        # Write output
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"Life insurance needs analysis complete. Results written to {args.output}")
        print(f"\nSummary:")
        print(f"  Needs-Based Method: ${result['method_2_needs_based']['calculated_need']:,.0f}")
        print(f"  Human Life Value: ${result['method_1_human_life_value']['calculated_need']:,.0f}")
        print(f"  Income Multiplier: ${result['method_3_income_multiplier']['calculated_need']:,.0f}")
        print(f"\nRecommended Additional Coverage: ${result['recommended_coverage']['net_additional_need']:,.0f}")
        print(f"Verification: {'✓ PASSED' if result['verification']['verification_passed'] else '✗ FAILED'}")

        if result['warnings']:
            print(f"\n⚠ Warnings: {len(result['warnings'])}")
            for warning in result['warnings']:
                print(f"  - {warning}")

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
