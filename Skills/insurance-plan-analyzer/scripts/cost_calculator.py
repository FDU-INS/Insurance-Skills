#!/usr/bin/env python3
"""
Insurance Cost Calculator
Supports: Annual costs, tax savings, ICHRA analysis, subsidy eligibility
"""

class InsuranceCostCalculator:
    """Calculate insurance costs with various scenarios"""

    # Constants
    ACA_AFFORDABILITY_PERCENTAGE = 0.0912  # 9.12% for 2025
    DEFAULT_TAX_RATE = 0.30  # 30% combined federal + state + FICA

    def __init__(self, monthly_premium, household_income,
                 employer_contribution_percent=0, tax_rate=None):
        """
        Initialize calculator

        Args:
            monthly_premium: Total monthly insurance premium
            household_income: Annual household income
            employer_contribution_percent: Employer contribution as decimal (0.10 = 10%)
            tax_rate: Combined tax rate (default 30%)
        """
        self.monthly_premium = monthly_premium
        self.household_income = household_income
        self.employer_contribution_percent = employer_contribution_percent
        self.tax_rate = tax_rate or self.DEFAULT_TAX_RATE

    def calculate_annual_cost(self):
        """Calculate total annual cost"""
        return self.monthly_premium * 12

    def calculate_employer_contribution(self):
        """Calculate monthly employer contribution"""
        return self.monthly_premium * self.employer_contribution_percent

    def calculate_employee_cost(self):
        """Calculate monthly employee cost"""
        return self.monthly_premium - self.calculate_employer_contribution()

    def calculate_tax_savings(self, is_pretax=True):
        """Calculate tax savings if paid pre-tax through payroll"""
        if not is_pretax:
            return 0
        employee_cost = self.calculate_employee_cost()
        return employee_cost * self.tax_rate

    def calculate_net_cost_to_employee(self, is_pretax=True):
        """Calculate employee's net cost after tax savings"""
        employee_cost = self.calculate_employee_cost()
        tax_savings = self.calculate_tax_savings(is_pretax)
        return employee_cost - tax_savings

    def is_affordable_under_aca(self):
        """
        Determine if coverage is affordable under ACA rules

        Returns:
            Tuple: (is_affordable: bool, threshold: float, employee_cost: float)
        """
        monthly_threshold = (self.household_income * self.ACA_AFFORDABILITY_PERCENTAGE) / 12
        employee_monthly_cost = self.calculate_employee_cost()
        is_affordable = employee_monthly_cost <= monthly_threshold

        return is_affordable, monthly_threshold, employee_monthly_cost

    def estimate_subsidy_eligibility(self, employer_sponsors_h1b=False):
        """
        Estimate if H-1B employee qualifies for marketplace subsidies

        Args:
            employer_sponsors_h1b: Does employer sponsor the H-1B visa?

        Returns:
            Dict with eligibility details
        """
        is_affordable, threshold, employee_cost = self.is_affordable_under_aca()

        result = {
            "employer_sponsors_h1b": employer_sponsors_h1b,
            "is_affordable": is_affordable,
            "monthly_threshold": threshold,
            "employee_monthly_cost": employee_cost,
            "qualifies_for_subsidy": False,
            "reason": ""
        }

        if not employer_sponsors_h1b:
            result["reason"] = "Employer does not sponsor H-1B visa"
        elif is_affordable:
            result["reason"] = "Employer coverage is affordable"
        else:
            result["qualifies_for_subsidy"] = True
            result["reason"] = "Employer coverage is unaffordable and sponsors H-1B"

        return result

    def compare_with_alternative(self, alternative_premium, alternative_subsidy=0):
        """
        Compare this plan with an alternative (e.g., individual marketplace)

        Args:
            alternative_premium: Monthly premium of alternative plan
            alternative_subsidy: Monthly subsidy amount (if any)

        Returns:
            Dict with comparison details
        """
        current_annual = self.calculate_annual_cost()
        alternative_annual = (alternative_premium - alternative_subsidy) * 12

        savings = current_annual - alternative_annual

        return {
            "current_plan_annual": current_annual,
            "alternative_plan_annual": alternative_annual,
            "annual_savings": savings,
            "monthly_savings": savings / 12,
            "alternative_is_cheaper": savings > 0
        }

    def generate_summary(self):
        """Generate summary of all calculations"""
        is_affordable, threshold, employee_cost = self.is_affordable_under_aca()

        return {
            "monthly_premium": self.monthly_premium,
            "annual_premium": self.calculate_annual_cost(),
            "employer_monthly": self.calculate_employer_contribution(),
            "employer_annual": self.calculate_employer_contribution() * 12,
            "employee_monthly": employee_cost,
            "employee_annual": employee_cost * 12,
            "tax_savings_monthly": self.calculate_tax_savings(True),
            "tax_savings_annual": self.calculate_tax_savings(True) * 12,
            "net_cost_employee_monthly": self.calculate_net_cost_to_employee(True),
            "net_cost_employee_annual": self.calculate_net_cost_to_employee(True) * 12,
            "aca_affordable": is_affordable,
            "aca_threshold_monthly": threshold,
            "aca_threshold_annual": threshold * 12
        }


def format_currency(amount):
    """Format number as currency"""
    return f"${amount:,.2f}"


def print_comparison_report(plan_name, calculator, is_pretax=True):
    """Print formatted comparison report"""
    summary = calculator.generate_summary()

    print(f"\n{'='*60}")
    print(f"  {plan_name}")
    print(f"{'='*60}")
    print(f"Monthly Premium:           {format_currency(summary['monthly_premium'])}")
    print(f"Annual Premium:            {format_currency(summary['annual_premium'])}")
    print(f"\nEmployer Contribution:")
    print(f"  Monthly:                 {format_currency(summary['employer_monthly'])}")
    print(f"  Annual:                  {format_currency(summary['employer_annual'])}")
    print(f"\nEmployee Cost:")
    print(f"  Monthly (before tax):    {format_currency(summary['employee_monthly'])}")
    print(f"  Annual (before tax):     {format_currency(summary['employee_annual'])}")

    if is_pretax:
        print(f"\nTax Savings (pre-tax payroll):")
        print(f"  Monthly:                 {format_currency(summary['tax_savings_monthly'])}")
        print(f"  Annual:                  {format_currency(summary['tax_savings_annual'])}")
        print(f"\nEmployee Net Cost (after tax):")
        print(f"  Monthly:                 {format_currency(summary['net_cost_employee_monthly'])}")
        print(f"  Annual:                  {format_currency(summary['net_cost_employee_annual'])}")

    print(f"\nACA Affordability Check:")
    print(f"  Threshold:               {format_currency(summary['aca_threshold_monthly'])}/month")
    print(f"  Employee Cost:           {format_currency(summary['employee_monthly'])}/month")
    print(f"  Status:                  {'AFFORDABLE ✓' if summary['aca_affordable'] else 'UNAFFORDABLE ✗'}")


# Example usage
if __name__ == "__main__":
    print("Insurance Cost Calculator - Example Usage\n")

    # Example 1: Small Group Insurance
    print("\n" + "="*60)
    print("EXAMPLE 1: Small Group Insurance")
    print("="*60)

    small_group = InsuranceCostCalculator(
        monthly_premium=2053.33,
        household_income=132000,
        employer_contribution_percent=0.10
    )

    print_comparison_report("Small Group: AmeriHealth Silver EPO", small_group)

    # Check subsidy eligibility
    subsidy_check = small_group.estimate_subsidy_eligibility(employer_sponsors_h1b=True)
    print(f"\nH-1B Subsidy Eligibility:")
    print(f"  Qualifies: {'YES ✓' if subsidy_check['qualifies_for_subsidy'] else 'NO ✗'}")
    print(f"  Reason: {subsidy_check['reason']}")

    # Example 2: Individual Marketplace (no subsidy)
    print("\n\n" + "="*60)
    print("EXAMPLE 2: Individual Marketplace (No Subsidy)")
    print("="*60)

    individual_no_subsidy = InsuranceCostCalculator(
        monthly_premium=1585.92,
        household_income=132000,
        employer_contribution_percent=0.10  # Optional ICHRA
    )

    print_comparison_report("Individual: AmeriHealth Silver EPO (no subsidy)",
                          individual_no_subsidy, is_pretax=False)

    # Example 3: Individual Marketplace (with subsidy)
    print("\n\n" + "="*60)
    print("EXAMPLE 3: Individual Marketplace (With Subsidy)")
    print("="*60)

    individual_with_subsidy = InsuranceCostCalculator(
        monthly_premium=1585.92 - 866,  # After subsidy
        household_income=132000,
        employer_contribution_percent=0
    )

    print_comparison_report("Individual: AmeriHealth Silver EPO (with subsidy)",
                          individual_with_subsidy, is_pretax=False)

    # Comparison
    print("\n\n" + "="*60)
    print("COST COMPARISON")
    print("="*60)

    comparison = small_group.compare_with_alternative(
        alternative_premium=1585.92,
        alternative_subsidy=0
    )

    print(f"\nSmall Group vs Individual (no subsidy):")
    print(f"  Small Group Annual:      {format_currency(comparison['current_plan_annual'])}")
    print(f"  Individual Annual:       {format_currency(comparison['alternative_plan_annual'])}")
    print(f"  Annual Savings:          {format_currency(comparison['annual_savings'])}")
    print(f"  Monthly Savings:         {format_currency(comparison['monthly_savings'])}")

    comparison_subsidy = small_group.compare_with_alternative(
        alternative_premium=1585.92,
        alternative_subsidy=866
    )

    print(f"\nSmall Group vs Individual (with subsidy):")
    print(f"  Small Group Annual:      {format_currency(comparison_subsidy['current_plan_annual'])}")
    print(f"  Individual Annual:       {format_currency(comparison_subsidy['alternative_plan_annual'])}")
    print(f"  Annual Savings:          {format_currency(comparison_subsidy['annual_savings'])}")
    print(f"  Monthly Savings:         {format_currency(comparison_subsidy['monthly_savings'])}")
