#!/usr/bin/env python3
"""
US Retirement Needs Calculator

Calculates required retirement savings using replacement ratio method.
Includes Social Security integration, IRMAA analysis, and RMD calculations.

DO NOT RELY ON LLM FOR THESE CALCULATIONS - USE THIS SCRIPT.

Usage:
    python retirement_needs.py --current-income 150000 --age 45 --retirement-age 67

Author: Financial Services Skills
License: MIT
"""

import argparse
import json
import math
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


class RetirementCalculator:
    """Calculate retirement savings needs with verification."""

    def __init__(self, current_year=2025):
        """Initialize with current year for limit lookups."""
        self.current_year = current_year

        # 2025 IRS Limits (UPDATE ANNUALLY)
        self.limits = {
            "social_security_max_benefit_fra": 4018 * 12,  # $48,216/year at FRA
            "social_security_max_benefit_70": 5108 * 12,   # $61,296/year at age 70
            "social_security_wage_base": 176100,
            "rmd_age_73": 73,  # For those turning 72 after Dec 31, 2022
            "rmd_age_75": 75,  # Effective Jan 1, 2033
        }

        # 2025 IRMAA Thresholds (single filers)
        # Format: (max_magi, monthly_surcharge)
        self.irmaa_thresholds_single = [
            (106000, 0),
            (133000, 74),
            (167000, 184),
            (200000, 295),
            (500000, 405),
            (float('inf'), 443)
        ]

        # 2025 Tax Brackets (single filers)
        self.tax_brackets_single = [
            (11925, 0.10),
            (48475, 0.12),
            (103350, 0.22),
            (197300, 0.24),
            (250525, 0.32),
            (626350, 0.35),
            (float('inf'), 0.37)
        ]

    def calculate_retirement_needs(
        self,
        current_income,
        current_age,
        retirement_age,
        retirement_duration=30,
        replacement_ratio=0.80,
        inflation_rate=0.025,
        nominal_return=0.06,
        social_security_estimate=None,
        filing_status="single"
    ):
        """
        Calculate comprehensive retirement needs.

        Args:
            current_income: Current annual gross income
            current_age: Current age
            retirement_age: Planned retirement age
            retirement_duration: Expected years in retirement (default 30)
            replacement_ratio: Percentage of income to replace (default 0.80)
            inflation_rate: Expected annual inflation (default 0.025)
            nominal_return: Expected nominal investment return (default 0.06)
            social_security_estimate: Estimated annual SS benefit (if None, will estimate)
            filing_status: 'single' or 'married' (affects tax/IRMAA calculations)

        Returns:
            dict: Comprehensive retirement analysis with verification
        """

        # Input validation
        self._validate_inputs(
            current_income, current_age, retirement_age,
            retirement_duration, replacement_ratio, inflation_rate, nominal_return
        )

        years_to_retirement = retirement_age - current_age

        # Calculate future income need (inflation-adjusted)
        future_income_need = self._calculate_future_income_need(
            current_income, replacement_ratio, years_to_retirement, inflation_rate
        )

        # Estimate Social Security if not provided
        if social_security_estimate is None:
            social_security_estimate = self._estimate_social_security(
                current_income, retirement_age
            )

        # Calculate after-tax Social Security benefit
        after_tax_ss = self._calculate_after_tax_ss(
            social_security_estimate, future_income_need, filing_status
        )

        # Calculate portfolio income need (after SS)
        portfolio_income_needed = future_income_need - after_tax_ss

        # Calculate real return (nominal - inflation)
        real_return = ((1 + nominal_return) / (1 + inflation_rate)) - 1

        # Calculate required portfolio value at retirement
        required_portfolio = self._calculate_required_portfolio(
            portfolio_income_needed, real_return, retirement_duration
        )

        # Calculate annual savings required
        annual_savings = self._calculate_annual_savings(
            required_portfolio, nominal_return, years_to_retirement
        )

        # Calculate RMD age and first RMD
        rmd_age = self._calculate_rmd_age(current_age)
        first_rmd = self._calculate_first_rmd(required_portfolio, rmd_age)

        # Check for IRMAA impact
        irmaa_analysis = self._check_irmaa_impact(
            portfolio_income_needed + social_security_estimate,
            filing_status
        )

        # Self-verification
        verification = self._verify_calculation(
            portfolio_income_needed, required_portfolio, real_return, retirement_duration
        )

        # Build comprehensive result
        result = {
            "calculation_date": datetime.now().isoformat(),
            "inputs": {
                "current_income": float(current_income),
                "current_age": current_age,
                "retirement_age": retirement_age,
                "years_to_retirement": years_to_retirement,
                "retirement_duration": retirement_duration,
                "replacement_ratio": replacement_ratio,
                "inflation_rate": inflation_rate,
                "nominal_return": nominal_return,
                "filing_status": filing_status
            },
            "calculated_values": {
                "future_income_need_gross": round(future_income_need, 2),
                "social_security_estimate": round(social_security_estimate, 2),
                "social_security_after_tax": round(after_tax_ss, 2),
                "portfolio_income_needed": round(portfolio_income_needed, 2),
                "real_return": round(real_return, 6),
                "required_portfolio_value": round(required_portfolio, 2),
                "annual_savings_required": round(annual_savings, 2),
                "monthly_savings_required": round(annual_savings / 12, 2),
                "rmd_age": rmd_age,
                "first_rmd_amount": round(first_rmd, 2)
            },
            "irmaa_analysis": irmaa_analysis,
            "verification": verification,
            "warnings": self._generate_warnings(
                current_age, retirement_age, annual_savings, current_income
            )
        }

        return result

    def _validate_inputs(
        self, current_income, current_age, retirement_age,
        retirement_duration, replacement_ratio, inflation_rate, nominal_return
    ):
        """Validate all inputs and raise ValueError if invalid."""

        if current_income <= 0:
            raise ValueError("Current income must be positive")

        if current_age < 18 or current_age > 100:
            raise ValueError("Current age must be between 18 and 100")

        if retirement_age <= current_age:
            raise ValueError("Retirement age must be greater than current age")

        if retirement_age > 100:
            raise ValueError("Retirement age must be 100 or less")

        if retirement_duration <= 0 or retirement_duration > 50:
            raise ValueError("Retirement duration must be between 1 and 50 years")

        if replacement_ratio <= 0 or replacement_ratio > 2.0:
            raise ValueError("Replacement ratio must be between 0 and 2.0")

        if inflation_rate < 0 or inflation_rate > 0.15:
            raise ValueError("Inflation rate must be between 0% and 15%")

        if nominal_return < 0 or nominal_return > 0.20:
            raise ValueError("Nominal return must be between 0% and 20%")

        if nominal_return <= inflation_rate:
            raise ValueError(
                "Nominal return must be greater than inflation rate. "
                f"Got nominal={nominal_return:.2%}, inflation={inflation_rate:.2%}"
            )

    def _calculate_future_income_need(
        self, current_income, replacement_ratio, years_to_retirement, inflation_rate
    ):
        """Calculate future income need adjusted for inflation."""
        return current_income * replacement_ratio * ((1 + inflation_rate) ** years_to_retirement)

    def _estimate_social_security(self, current_income, retirement_age):
        """
        Estimate Social Security benefit.

        Simple estimation: Use proportion of max benefit based on income.
        Real calculation requires full earnings history and PIA formula.
        """

        # Cap earnings at wage base
        earnings_for_ss = min(current_income, self.limits["social_security_wage_base"])

        # Rough estimate: proportion of max benefit
        proportion = earnings_for_ss / self.limits["social_security_wage_base"]

        if retirement_age >= 70:
            base_benefit = self.limits["social_security_max_benefit_70"] * proportion
        else:
            # FRA is 67 for those born 1960 or later
            # Simplified: use FRA benefit with adjustment for early/late claiming
            base_benefit = self.limits["social_security_max_benefit_fra"] * proportion

            # Adjust for early/late claiming (simplified)
            if retirement_age < 67:
                # Reduce by ~5-7% per year before FRA
                reduction = (67 - retirement_age) * 0.06
                base_benefit *= (1 - reduction)
            elif retirement_age > 67:
                # Increase by 8% per year after FRA up to age 70
                increase = min(retirement_age - 67, 3) * 0.08
                base_benefit *= (1 + increase)

        return base_benefit

    def _calculate_after_tax_ss(self, social_security_benefit, total_income, filing_status):
        """
        Calculate after-tax Social Security benefit.

        Up to 85% of SS is taxable depending on total income.
        """

        # Simplified: assume 85% taxable at higher income levels
        # Real calculation uses provisional income and two-tier thresholds

        if total_income > 100000:  # Simplified threshold
            taxable_portion = 0.85
        elif total_income > 50000:
            taxable_portion = 0.50
        else:
            taxable_portion = 0.00

        taxable_ss = social_security_benefit * taxable_portion

        # Estimate tax on Social Security (simplified - use 22% bracket)
        estimated_tax = taxable_ss * 0.22

        return social_security_benefit - estimated_tax

    def _calculate_required_portfolio(self, annual_income_needed, real_return, duration):
        """
        Calculate required portfolio value using annuity formula.

        Formula: PV = PMT * [(1 - (1 + r)^-n) / r]
        Where: PV = present value, PMT = annual payment, r = real return, n = duration
        """

        if abs(real_return) < 0.0001:
            # Edge case: zero real return
            return annual_income_needed * duration

        # Standard annuity present value calculation
        pv_factor = (1 - (1 + real_return) ** -duration) / real_return
        required_portfolio = annual_income_needed * pv_factor

        return required_portfolio

    def _calculate_annual_savings(self, future_value, nominal_return, years):
        """
        Calculate annual savings required to reach future value.

        Formula: PMT = FV * [r / ((1 + r)^n - 1)]
        Where: PMT = payment, FV = future value, r = return, n = years
        """

        if abs(nominal_return) < 0.0001:
            # Edge case: zero return
            return future_value / years

        # Future value of annuity formula (solve for PMT)
        fv_factor = nominal_return / (((1 + nominal_return) ** years) - 1)
        annual_savings = future_value * fv_factor

        return annual_savings

    def _calculate_rmd_age(self, current_age):
        """Determine RMD age based on SECURE 2.0 rules."""

        # Born 1951-1959: RMD age 73 (turned 72 after Dec 31, 2022)
        # Born 1960+: RMD age 75 (starting Jan 1, 2033)

        birth_year = self.current_year - current_age

        if birth_year >= 1960:
            return 75
        else:
            return 73

    def _calculate_first_rmd(self, portfolio_value, rmd_age):
        """
        Calculate first required minimum distribution.

        Uses IRS Uniform Lifetime Table.
        Simplified - uses distribution period of 27.4 for age 73.
        """

        # IRS Uniform Lifetime Table (simplified)
        distribution_periods = {
            73: 27.4,
            74: 26.5,
            75: 25.5,
            76: 24.6,
            77: 23.7,
            78: 22.9,
            79: 22.0,
            80: 21.2
        }

        distribution_period = distribution_periods.get(rmd_age, 27.4)

        return portfolio_value / distribution_period

    def _check_irmaa_impact(self, magi, filing_status):
        """Check if income triggers Medicare IRMAA surcharges."""

        thresholds = self.irmaa_thresholds_single if filing_status == "single" else [
            (212000, 0),
            (266000, 74),
            (334000, 184),
            (400000, 295),
            (750000, 405),
            (float('inf'), 443)
        ]

        current_surcharge = 0
        for threshold, surcharge in thresholds:
            if magi <= threshold:
                current_surcharge = surcharge
                break

        annual_irmaa_cost = current_surcharge * 12

        # Find next threshold
        next_threshold = None
        next_surcharge = None
        for threshold, surcharge in thresholds:
            if threshold > magi:
                next_threshold = threshold
                next_surcharge = surcharge
                break

        return {
            "magi": round(magi, 2),
            "current_irmaa_surcharge_monthly": current_surcharge,
            "current_irmaa_surcharge_annual": annual_irmaa_cost,
            "next_threshold": next_threshold,
            "next_threshold_surcharge_increase": next_surcharge - current_surcharge if next_surcharge else 0,
            "warning": f"MAGI of ${magi:,.0f} triggers ${current_surcharge}/month IRMAA surcharge" if current_surcharge > 0 else None
        }

    def _verify_calculation(self, income_needed, portfolio_value, real_return, duration):
        """
        Verify calculation using alternative method.

        Generate income from portfolio and compare to needed income.
        """

        if abs(real_return) < 0.0001:
            generated_income = portfolio_value / duration
        else:
            # Annuity payment formula
            generated_income = portfolio_value * real_return / (1 - (1 + real_return) ** -duration)

        difference = abs(generated_income - income_needed)
        tolerance = income_needed * 0.01  # 1% tolerance

        verification_passed = difference < tolerance

        return {
            "income_needed": round(income_needed, 2),
            "income_generated_by_portfolio": round(generated_income, 2),
            "difference": round(difference, 2),
            "difference_percentage": round((difference / income_needed) * 100, 4),
            "tolerance_percentage": 1.0,
            "verification_passed": verification_passed,
            "verification_method": "Annuity payment formula (alternative calculation)"
        }

    def _generate_warnings(self, current_age, retirement_age, annual_savings, current_income):
        """Generate warnings about the retirement plan."""

        warnings = []

        years_to_retirement = retirement_age - current_age

        if years_to_retirement < 10:
            warnings.append(
                f"Short time horizon: Only {years_to_retirement} years to retirement. "
                "Limited time to recover from market downturns."
            )

        savings_rate = annual_savings / current_income
        if savings_rate > 0.30:
            warnings.append(
                f"High savings rate required: {savings_rate:.1%} of gross income. "
                "This may be difficult to sustain. Consider working longer or reducing income needs."
            )

        if savings_rate > 0.50:
            warnings.append(
                "CRITICAL: Savings rate exceeds 50% of gross income. "
                "This is likely not achievable. Recommend adjusting plan parameters."
            )

        if retirement_age < 62:
            warnings.append(
                f"Early retirement age: {retirement_age}. Social Security not available until age 62, "
                "and early claiming reduces benefits. Portfolio must cover full income until SS starts."
            )

        return warnings


def main():
    """Command-line interface for retirement calculator."""

    parser = argparse.ArgumentParser(
        description="Calculate retirement savings needs with Social Security and IRMAA analysis"
    )

    # Required arguments
    parser.add_argument(
        "--current-income",
        type=float,
        required=True,
        help="Current annual gross income"
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="Current age"
    )
    parser.add_argument(
        "--retirement-age",
        type=int,
        required=True,
        help="Planned retirement age"
    )

    # Optional arguments
    parser.add_argument(
        "--replacement-ratio",
        type=float,
        default=0.80,
        help="Percentage of income to replace in retirement (default: 0.80)"
    )
    parser.add_argument(
        "--retirement-duration",
        type=int,
        default=30,
        help="Expected years in retirement (default: 30)"
    )
    parser.add_argument(
        "--inflation",
        type=float,
        default=0.025,
        help="Expected annual inflation rate (default: 0.025)"
    )
    parser.add_argument(
        "--return",
        type=float,
        default=0.06,
        dest="nominal_return",
        help="Expected nominal investment return (default: 0.06)"
    )
    parser.add_argument(
        "--social-security",
        type=float,
        default=None,
        help="Estimated annual Social Security benefit (default: auto-calculate)"
    )
    parser.add_argument(
        "--filing-status",
        choices=["single", "married"],
        default="single",
        help="Tax filing status (default: single)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="retirement_analysis.json",
        help="Output file path (default: retirement_analysis.json)"
    )

    args = parser.parse_args()

    try:
        calculator = RetirementCalculator()

        result = calculator.calculate_retirement_needs(
            current_income=args.current_income,
            current_age=args.age,
            retirement_age=args.retirement_age,
            retirement_duration=args.retirement_duration,
            replacement_ratio=args.replacement_ratio,
            inflation_rate=args.inflation,
            nominal_return=args.nominal_return,
            social_security_estimate=args.social_security,
            filing_status=args.filing_status
        )

        # Save to file
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)

        # Print summary
        print("=" * 70)
        print("RETIREMENT NEEDS ANALYSIS")
        print("=" * 70)
        print(f"Current age: {result['inputs']['current_age']}")
        print(f"Retirement age: {result['inputs']['retirement_age']}")
        print(f"Years to retirement: {result['inputs']['years_to_retirement']}")
        print(f"Current income: ${result['inputs']['current_income']:,.0f}")
        print()
        print("REQUIRED SAVINGS:")
        print(f"Future income need: ${result['calculated_values']['future_income_need_gross']:,.0f}/year")
        print(f"Social Security (est): ${result['calculated_values']['social_security_estimate']:,.0f}/year")
        print(f"Portfolio income need: ${result['calculated_values']['portfolio_income_needed']:,.0f}/year")
        print()
        print(f"Required portfolio: ${result['calculated_values']['required_portfolio_value']:,.0f}")
        print(f"Annual savings: ${result['calculated_values']['annual_savings_required']:,.0f}")
        print(f"Monthly savings: ${result['calculated_values']['monthly_savings_required']:,.0f}")
        print()
        print("RMD INFORMATION:")
        print(f"RMD starts at age: {result['calculated_values']['rmd_age']}")
        print(f"First RMD amount: ${result['calculated_values']['first_rmd_amount']:,.0f}")
        print()
        print("IRMAA ANALYSIS:")
        irmaa = result['irmaa_analysis']
        print(f"Estimated retirement MAGI: ${irmaa['magi']:,.0f}")
        print(f"IRMAA surcharge: ${irmaa['current_irmaa_surcharge_monthly']}/month (${irmaa['current_irmaa_surcharge_annual']:,.0f}/year)")
        if irmaa['warning']:
            print(f"WARNING: {irmaa['warning']}")
        print()
        print("VERIFICATION:")
        verification = result['verification']
        print(f"Calculation verified: {'✓ PASSED' if verification['verification_passed'] else '✗ FAILED'}")
        print(f"Difference: ${verification['difference']:,.2f} ({verification['difference_percentage']:.4f}%)")
        print()

        if result['warnings']:
            print("WARNINGS:")
            for warning in result['warnings']:
                print(f"⚠ {warning}")
            print()

        print(f"Full results saved to: {args.output}")
        print("=" * 70)

    except ValueError as e:
        print(f"ERROR: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
