#!/usr/bin/env python3
"""
UK Life Insurance Needs Calculator

This script calculates life insurance coverage requirements using multiple UK-specific
methodologies tailored to FCA Consumer Duty requirements. Calculates:
- Human Life Value (HLV) - Present value of future earnings
- Needs-Based Analysis - Income replacement, debts, education, funeral costs
- Income Multiplier Method - Simple earnings multiple
- Mortgage Protection - Specific mortgage coverage requirements
- Family Income Benefit - Regular income vs lump sum analysis

CRITICAL: This calculator implements exact UK life insurance needs analysis.
DO NOT perform these calculations manually - use this validated script.

Why this matters for UK protection advice:
- Consumer Duty requires good outcomes - adequate coverage is essential
- Underinsurance leaves families financially vulnerable
- Overinsurance wastes client money and fails fair value test
- FCA expects evidence-based protection recommendations
- Professional indemnity requires documented needs analysis

Usage:
    python life_insurance_needs.py \\
        --annual-income 50000 \\
        --age 35 \\
        --retirement-age 67 \\
        --mortgage-balance 250000 \\
        --other-debts 15000 \\
        --dependents 2 \\
        --years-income-replacement 20 \\
        --education-cost-per-child 50000 \\
        --existing-life-cover 100000 \\
        --output protection_needs.json

Regulatory Context:
- FCA Consumer Duty: Ensure adequate coverage at fair value
- COBS Rules: Suitability and affordability assessment required
- Vulnerable customers: Consider capacity for loss and understanding

Author: Financial Services Skill System
Version: 1.0.0
Last Updated: 2024-25 Tax Year
"""

import argparse
import json
import sys
from typing import Dict, Any, List
from datetime import datetime


class UKLifeInsuranceCalculator:
    """
    Calculate UK life insurance needs using multiple methodologies.

    Methods:
    1. Human Life Value (HLV) - Actuarial approach
    2. Needs-Based Analysis - Detailed family needs
    3. Income Multiplier - Rule of thumb (10-15x income)
    4. Mortgage Protection - Outstanding mortgage debt
    5. Family Income Benefit analysis - Regular income vs lump sum
    """

    def __init__(self):
        """Initialize calculator with UK-specific defaults."""
        # UK tax-free lump sum death benefit (pension schemes)
        self.pension_lump_sum_death_benefit_typical = 4  # Multiple of salary

        # Average UK costs
        self.funeral_costs_uk_average = 4500
        self.university_cost_estimate = 60000  # Total 3-year degree

        # Income replacement typical percentage
        self.income_replacement_percentage = 0.70  # 70% of gross income

    def calculate_life_insurance_needs(
        self,
        annual_income: float,
        age: int,
        retirement_age: int = 67,
        mortgage_balance: float = 0,
        other_debts: float = 0,
        number_of_dependents: int = 0,
        years_income_replacement: int = 0,
        education_cost_per_child: float = 0,
        funeral_costs: float = 0,
        existing_life_cover: float = 0,
        existing_savings: float = 0,
        pension_scheme_death_benefit: float = 0,
        discount_rate: float = 0.03,
        inflation_rate: float = 0.02,
        spouse_income: float = 0,
        state_benefits_annual: float = 0,
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive life insurance needs.

        Args:
            annual_income: Gross annual income
            age: Current age
            retirement_age: Expected retirement age (default 67 - UK State Pension age)
            mortgage_balance: Outstanding mortgage balance
            other_debts: Other debts (loans, credit cards, etc.)
            number_of_dependents: Number of financial dependents
            years_income_replacement: Years to provide income (0 = until retirement)
            education_cost_per_child: Education costs per child (university, etc.)
            funeral_costs: Estimated funeral costs (0 = use UK average)
            existing_life_cover: Existing life insurance coverage
            existing_savings: Family savings/emergency fund
            pension_scheme_death_benefit: Death in service benefit from pension
            discount_rate: Discount rate for present value (real return assumption)
            inflation_rate: Expected inflation rate
            spouse_income: Surviving spouse's annual income
            state_benefits_annual: Expected state benefits (Bereavement Support Payment, etc.)

        Returns:
            Comprehensive life insurance needs analysis
        """
        # Validate inputs
        self._validate_inputs(annual_income, age, retirement_age)

        # Set defaults
        if funeral_costs == 0:
            funeral_costs = self.funeral_costs_uk_average

        if years_income_replacement == 0:
            years_income_replacement = max(1, retirement_age - age)

        # Calculate real discount rate (adjusted for inflation)
        real_discount_rate = ((1 + discount_rate) / (1 + inflation_rate)) - 1

        # Method 1: Human Life Value
        hlv_analysis = self._calculate_human_life_value(
            annual_income,
            years_income_replacement,
            real_discount_rate,
            self.income_replacement_percentage
        )

        # Method 2: Needs-Based Analysis
        needs_based = self._calculate_needs_based(
            annual_income,
            years_income_replacement,
            mortgage_balance,
            other_debts,
            number_of_dependents,
            education_cost_per_child,
            funeral_costs,
            self.income_replacement_percentage,
            real_discount_rate
        )

        # Method 3: Income Multiplier
        income_multiplier = self._calculate_income_multiplier(
            annual_income,
            age,
            number_of_dependents
        )

        # Method 4: Mortgage Protection
        mortgage_protection = self._calculate_mortgage_protection(
            mortgage_balance,
            other_debts
        )

        # Method 5: Family Income Benefit Analysis
        fib_analysis = self._calculate_family_income_benefit(
            annual_income,
            years_income_replacement,
            real_discount_rate,
            spouse_income,
            state_benefits_annual
        )

        # Net needs (after existing coverage)
        net_needs = self._calculate_net_needs(
            needs_based["total_needs"],
            existing_life_cover,
            existing_savings,
            pension_scheme_death_benefit
        )

        # Cross-verify all methods
        verification = self._verify_calculations(
            hlv_analysis["human_life_value"],
            needs_based["total_needs"],
            income_multiplier["recommended_coverage"],
            mortgage_protection["total_debt_coverage"]
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            needs_based["total_needs"],
            net_needs,
            verification,
            mortgage_balance,
            number_of_dependents,
            years_income_replacement,
            fib_analysis
        )

        # Compile result
        result = {
            "calculation_timestamp": datetime.now().isoformat(),
            "regulatory_context": "FCA Consumer Duty - Adequate coverage at fair value",

            "client_profile": {
                "annual_income": annual_income,
                "age": age,
                "retirement_age": retirement_age,
                "years_to_retirement": retirement_age - age,
                "mortgage_balance": mortgage_balance,
                "other_debts": other_debts,
                "number_of_dependents": number_of_dependents,
                "spouse_income": spouse_income,
            },

            "calculation_methods": {
                "human_life_value": hlv_analysis,
                "needs_based_analysis": needs_based,
                "income_multiplier": income_multiplier,
                "mortgage_protection": mortgage_protection,
                "family_income_benefit": fib_analysis,
            },

            "existing_coverage": {
                "life_insurance": existing_life_cover,
                "savings_emergency_fund": existing_savings,
                "pension_death_benefit": pension_scheme_death_benefit,
                "total_existing_resources": existing_life_cover + existing_savings + pension_scheme_death_benefit,
            },

            "net_needs_analysis": net_needs,

            "recommended_coverage": {
                "primary_recommendation": needs_based["total_needs"],
                "net_coverage_required": net_needs["net_life_insurance_required"],
                "recommended_structure": recommendations["recommended_structure"],
                "priority_order": recommendations["priority_order"],
            },

            "verification": verification,
            "recommendations": recommendations,

            "assumptions": {
                "discount_rate_nominal": discount_rate,
                "inflation_rate": inflation_rate,
                "real_discount_rate": real_discount_rate,
                "income_replacement_percentage": self.income_replacement_percentage,
                "funeral_costs": funeral_costs,
            }
        }

        return result

    def _validate_inputs(self, income: float, age: int, retirement_age: int):
        """Validate input parameters."""
        if income < 0:
            raise ValueError("Annual income cannot be negative")

        if age < 18 or age > 100:
            raise ValueError("Age must be between 18 and 100")

        if retirement_age <= age:
            raise ValueError("Retirement age must be greater than current age")

        if retirement_age > 100:
            raise ValueError("Retirement age must be 100 or less")

    def _calculate_human_life_value(
        self,
        annual_income: float,
        years: int,
        discount_rate: float,
        replacement_percentage: float
    ) -> Dict[str, Any]:
        """Calculate Human Life Value using present value of future earnings."""
        income_to_replace = annual_income * replacement_percentage

        if abs(discount_rate) < 0.0001:
            # If discount rate near zero, simple multiplication
            present_value = income_to_replace * years
        else:
            # Present value of annuity formula: PV = PMT × [(1-(1+r)^-n)/r]
            pv_factor = (1 - (1 + discount_rate) ** -years) / discount_rate
            present_value = income_to_replace * pv_factor

        return {
            "human_life_value": present_value,
            "annual_income_to_replace": income_to_replace,
            "years_of_income": years,
            "discount_rate": discount_rate,
            "method": "Present value of future earnings at {}% replacement".format(int(replacement_percentage * 100)),
            "explanation": f"Present value of {years} years of income (£{income_to_replace:,.0f}/year) discounted at {discount_rate*100:.1f}%"
        }

    def _calculate_needs_based(
        self,
        annual_income: float,
        years: int,
        mortgage: float,
        other_debts: float,
        dependents: int,
        education_per_child: float,
        funeral: float,
        replacement_pct: float,
        discount_rate: float
    ) -> Dict[str, Any]:
        """Calculate needs-based coverage (UK DIME-F method: Debt, Income, Mortgage, Education, Funeral)."""

        # Income replacement need (present value)
        income_to_replace = annual_income * replacement_pct
        if abs(discount_rate) < 0.0001:
            income_replacement_pv = income_to_replace * years
        else:
            pv_factor = (1 - (1 + discount_rate) ** -years) / discount_rate
            income_replacement_pv = income_to_replace * pv_factor

        # Debt coverage
        total_debts = mortgage + other_debts

        # Education costs
        total_education = dependents * education_per_child

        # Emergency fund (3-6 months expenses, using 6 months)
        emergency_fund = (annual_income * replacement_pct * 0.5)

        # Total needs
        total_needs = (
            income_replacement_pv +
            total_debts +
            total_education +
            funeral +
            emergency_fund
        )

        return {
            "total_needs": total_needs,
            "breakdown": {
                "income_replacement": income_replacement_pv,
                "mortgage_debt": mortgage,
                "other_debts": other_debts,
                "total_debt": total_debts,
                "education_costs": total_education,
                "funeral_costs": funeral,
                "emergency_fund": emergency_fund,
            },
            "method": "Needs-Based Analysis (UK DIME-F)",
            "explanation": f"Total family needs: income replacement (£{income_replacement_pv:,.0f}), debts (£{total_debts:,.0f}), education (£{total_education:,.0f}), funeral (£{funeral:,.0f}), emergency fund (£{emergency_fund:,.0f})"
        }

    def _calculate_income_multiplier(
        self,
        annual_income: float,
        age: int,
        dependents: int
    ) -> Dict[str, Any]:
        """Calculate coverage using income multiplier rule of thumb."""
        # Multiplier varies by age and dependents
        if age < 30:
            base_multiplier = 15
        elif age < 40:
            base_multiplier = 12
        elif age < 50:
            base_multiplier = 10
        elif age < 60:
            base_multiplier = 8
        else:
            base_multiplier = 5

        # Adjust for dependents
        if dependents > 2:
            multiplier = base_multiplier + 2
        elif dependents > 0:
            multiplier = base_multiplier + 1
        else:
            multiplier = max(5, base_multiplier - 2)

        coverage = annual_income * multiplier

        return {
            "recommended_coverage": coverage,
            "multiplier_used": multiplier,
            "annual_income": annual_income,
            "method": "Income Multiplier (Rule of Thumb)",
            "explanation": f"{multiplier}x annual income based on age {age} and {dependents} dependents"
        }

    def _calculate_mortgage_protection(
        self,
        mortgage_balance: float,
        other_debts: float
    ) -> Dict[str, Any]:
        """Calculate mortgage and debt protection needs."""
        total_debt = mortgage_balance + other_debts

        return {
            "total_debt_coverage": total_debt,
            "mortgage_balance": mortgage_balance,
            "other_debts": other_debts,
            "method": "Mortgage & Debt Protection",
            "explanation": f"Total debt coverage: £{total_debt:,.0f} (mortgage: £{mortgage_balance:,.0f}, other debts: £{other_debts:,.0f})",
            "note": "Consider decreasing term assurance aligned with mortgage term for cost efficiency"
        }

    def _calculate_family_income_benefit(
        self,
        annual_income: float,
        years: int,
        discount_rate: float,
        spouse_income: float,
        state_benefits: float
    ) -> Dict[str, Any]:
        """Calculate Family Income Benefit (regular income) vs lump sum comparison."""
        # Income needed
        gross_income_needed = annual_income * self.income_replacement_percentage

        # Subtract spouse income and state benefits
        net_income_needed = max(0, gross_income_needed - spouse_income - state_benefits)

        # Lump sum equivalent (present value)
        if abs(discount_rate) < 0.0001:
            lump_sum_equivalent = net_income_needed * years
        else:
            pv_factor = (1 - (1 + discount_rate) ** -years) / discount_rate
            lump_sum_equivalent = net_income_needed * pv_factor

        # Annual FIB payment
        annual_fib_payment = net_income_needed

        return {
            "annual_income_needed": net_income_needed,
            "lump_sum_equivalent": lump_sum_equivalent,
            "family_income_benefit_annual": annual_fib_payment,
            "payment_years": years,
            "spouse_income": spouse_income,
            "state_benefits": state_benefits,
            "gross_income_needed": gross_income_needed,
            "method": "Family Income Benefit Analysis",
            "explanation": f"Annual FIB payment of £{annual_fib_payment:,.0f} for {years} years, or lump sum of £{lump_sum_equivalent:,.0f}",
            "recommendation": "FIB typically 30-50% cheaper than level term for income replacement needs"
        }

    def _calculate_net_needs(
        self,
        total_needs: float,
        existing_life_cover: float,
        existing_savings: float,
        pension_death_benefit: float
    ) -> Dict[str, Any]:
        """Calculate net life insurance required after existing resources."""
        total_existing = existing_life_cover + existing_savings + pension_death_benefit
        net_required = max(0, total_needs - total_existing)

        coverage_gap_percentage = (net_required / total_needs * 100) if total_needs > 0 else 0

        return {
            "total_needs": total_needs,
            "total_existing_resources": total_existing,
            "existing_life_insurance": existing_life_cover,
            "existing_savings": existing_savings,
            "pension_death_benefit": pension_death_benefit,
            "net_life_insurance_required": net_required,
            "coverage_gap_percentage": coverage_gap_percentage,
            "adequately_covered": net_required == 0,
            "explanation": f"Total needs £{total_needs:,.0f} - existing resources £{total_existing:,.0f} = additional coverage required £{net_required:,.0f}"
        }

    def _verify_calculations(
        self,
        hlv: float,
        needs_based: float,
        income_mult: float,
        mortgage: float
    ) -> Dict[str, Any]:
        """Verify calculations by comparing methods."""
        all_values = [hlv, needs_based, income_mult]
        average = sum(all_values) / len(all_values)

        min_val = min(all_values)
        max_val = max(all_values)
        spread = max_val - min_val
        spread_percentage = (spread / average * 100) if average > 0 else 0

        # Reasonable agreement if within 50% spread
        reasonable_agreement = spread_percentage < 50

        return {
            "human_life_value": hlv,
            "needs_based": needs_based,
            "income_multiplier": income_mult,
            "mortgage_protection": mortgage,
            "average_of_methods": average,
            "minimum": min_val,
            "maximum": max_val,
            "spread": spread,
            "spread_percentage": spread_percentage,
            "reasonable_agreement": reasonable_agreement,
            "explanation": f"Methods range from £{min_val:,.0f} to £{max_val:,.0f} (spread: {spread_percentage:.0f}%). {'Reasonable agreement' if reasonable_agreement else 'Wide variation - review assumptions'}"
        }

    def _generate_recommendations(
        self,
        total_needs: float,
        net_needs: Dict,
        verification: Dict,
        mortgage: float,
        dependents: int,
        years: int,
        fib: Dict
    ) -> Dict[str, Any]:
        """Generate protection recommendations."""
        recommendations = []

        # Coverage structure
        if mortgage > 100000 and years > 10:
            structure = "Combination: Decreasing Term (mortgage) + Level Term (family protection)"
            recommendations.append(f"Consider decreasing term assurance for £{mortgage:,.0f} mortgage, reducing cost significantly")
        else:
            structure = "Level Term Assurance"

        # Family Income Benefit
        if dependents > 0 and years > 10:
            recommendations.append(f"Family Income Benefit of £{fib['annual_income_needed']:,.0f}/year could be 30-50% cheaper than lump sum cover")

        # Priority order
        priority_order = []
        if mortgage > 0:
            priority_order.append(f"1. Mortgage protection: £{mortgage:,.0f} (decreasing term)")
        if dependents > 0:
            priority_order.append(f"2. Income replacement: £{fib['lump_sum_equivalent']:,.0f} (level term or FIB)")
        priority_order.append("3. Emergency fund and final expenses coverage")
        if dependents > 0:
            priority_order.append("4. Education costs (if budget allows)")

        # Adequacy check
        if net_needs["net_life_insurance_required"] == 0:
            recommendations.append("✅ Existing coverage appears adequate based on current needs")
        elif net_needs["coverage_gap_percentage"] > 50:
            recommendations.append(f"⚠️ Significant protection gap: {net_needs['coverage_gap_percentage']:.0f}% of needs uncovered (£{net_needs['net_life_insurance_required']:,.0f})")
        else:
            recommendations.append(f"ℹ️ Moderate protection gap: £{net_needs['net_life_insurance_required']:,.0f} additional coverage recommended")

        # Affordability
        recommendations.append("📊 Obtain quotes for recommended coverage and ensure affordable within client budget")
        recommendations.append("🔄 Review protection needs annually and at major life events")

        return {
            "recommended_structure": structure,
            "priority_order": priority_order,
            "key_recommendations": recommendations,
            "consumer_duty_note": "Ensure coverage provides good outcomes and fair value. Avoid over-insurance."
        }


def main():
    """Command-line interface for UK Life Insurance Needs Calculator."""
    parser = argparse.ArgumentParser(
        description="Calculate UK Life Insurance Needs using multiple methodologies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic calculation
  python life_insurance_needs.py --annual-income 50000 --age 35 --retirement-age 67 \\
      --mortgage-balance 250000 --dependents 2

  # Comprehensive analysis
  python life_insurance_needs.py --annual-income 75000 --age 40 --retirement-age 67 \\
      --mortgage-balance 300000 --other-debts 20000 --dependents 2 \\
      --years-income-replacement 20 --education-cost-per-child 60000 \\
      --existing-life-cover 100000 --existing-savings 30000 \\
      --pension-scheme-death-benefit 150000 --spouse-income 40000

Output: JSON file with comprehensive life insurance needs analysis
        """
    )

    parser.add_argument("--annual-income", type=float, required=True, help="Gross annual income")
    parser.add_argument("--age", type=int, required=True, help="Current age")
    parser.add_argument("--retirement-age", type=int, default=67, help="Expected retirement age (default: 67)")
    parser.add_argument("--mortgage-balance", type=float, default=0, help="Outstanding mortgage balance")
    parser.add_argument("--other-debts", type=float, default=0, help="Other debts (loans, credit cards)")
    parser.add_argument("--dependents", type=int, default=0, help="Number of financial dependents")
    parser.add_argument("--years-income-replacement", type=int, default=0, help="Years to provide income (0=until retirement)")
    parser.add_argument("--education-cost-per-child", type=float, default=60000, help="Education costs per child")
    parser.add_argument("--funeral-costs", type=float, default=0, help="Funeral costs (0=use UK average £4,500)")
    parser.add_argument("--existing-life-cover", type=float, default=0, help="Existing life insurance coverage")
    parser.add_argument("--existing-savings", type=float, default=0, help="Family savings/emergency fund")
    parser.add_argument("--pension-scheme-death-benefit", type=float, default=0, help="Death in service benefit")
    parser.add_argument("--discount-rate", type=float, default=0.03, help="Discount rate (default: 3%%)")
    parser.add_argument("--inflation-rate", type=float, default=0.02, help="Inflation rate (default: 2%%)")
    parser.add_argument("--spouse-income", type=float, default=0, help="Surviving spouse's income")
    parser.add_argument("--state-benefits", type=float, default=0, help="Expected annual state benefits")
    parser.add_argument("--output", default="life_insurance_needs.json", help="Output JSON file")

    args = parser.parse_args()

    calculator = UKLifeInsuranceCalculator()

    try:
        result = calculator.calculate_life_insurance_needs(
            annual_income=args.annual_income,
            age=args.age,
            retirement_age=args.retirement_age,
            mortgage_balance=args.mortgage_balance,
            other_debts=args.other_debts,
            number_of_dependents=args.dependents,
            years_income_replacement=args.years_income_replacement,
            education_cost_per_child=args.education_cost_per_child,
            funeral_costs=args.funeral_costs,
            existing_life_cover=args.existing_life_cover,
            existing_savings=args.existing_savings,
            pension_scheme_death_benefit=args.pension_scheme_death_benefit,
            discount_rate=args.discount_rate,
            inflation_rate=args.inflation_rate,
            spouse_income=args.spouse_income,
            state_benefits_annual=args.state_benefits,
        )

        # Write to file
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)

        # Print summary
        print(f"\n{'='*80}")
        print(f"UK LIFE INSURANCE NEEDS ANALYSIS")
        print(f"{'='*80}\n")

        print(f"Client: Age {args.age}, Income £{args.annual_income:,.0f}, {args.dependents} dependents\n")

        methods = result['calculation_methods']
        print("CALCULATION METHODS:")
        print(f"  Human Life Value:      £{methods['human_life_value']['human_life_value']:,.0f}")
        print(f"  Needs-Based Analysis:  £{methods['needs_based_analysis']['total_needs']:,.0f}")
        print(f"  Income Multiplier:     £{methods['income_multiplier']['recommended_coverage']:,.0f}")
        print(f"  Mortgage Protection:   £{methods['mortgage_protection']['total_debt_coverage']:,.0f}\n")

        rec = result['recommended_coverage']
        print(f"RECOMMENDED COVERAGE:   £{rec['primary_recommendation']:,.0f}")
        print(f"Less existing coverage: £{result['existing_coverage']['total_existing_resources']:,.0f}")
        print(f"NET COVERAGE REQUIRED:  £{rec['net_coverage_required']:,.0f}\n")

        print(f"Structure: {rec['recommended_structure']}\n")

        print("RECOMMENDATIONS:")
        for r in result['recommendations']['key_recommendations']:
            print(f"  {r}")

        print(f"\n{'='*80}")
        print(f"Full analysis written to: {args.output}")
        print(f"{'='*80}\n")

        sys.exit(0)

    except ValueError as e:
        print(f"\n❌ ERROR: {str(e)}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
