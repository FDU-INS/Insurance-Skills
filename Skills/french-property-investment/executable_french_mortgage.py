#!/usr/bin/env python3
"""
French Property Investment Analyzer

Analyzes French rental property investments with comprehensive financial modeling
including cash flow projections, ROI calculations, and break-even analysis.
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class PropertyInvestmentInput:
    property_price: float
    down_payment: float
    interest_rate: float
    loan_term_years: int
    monthly_rent: float
    holding_period_years: int
    property_tax_annual: float = 0.0
    hoa_monthly: float = 0.0
    maintenance_percent: float = 1.0
    management_fee_percent: float = 0.0
    vacancy_rate: float = 0.0
    rent_increase_annual: float = 0.0


@dataclass
class MortgageDetails:
    monthly_payment: float
    total_interest: float
    total_payments: float


@dataclass
class YearlyExpenses:
    mortgage: float
    property_tax: float
    hoa: float
    maintenance: float
    management: float
    insurance: float
    total: float


@dataclass
class YearlyProjection:
    year: int
    rental_income: float
    expenses: YearlyExpenses
    net_cash_flow: float
    cumulative_cash_flow: float
    principal_paydown: float
    total_equity: float
    remaining_balance: float


@dataclass
class InvestmentSummary:
    initial_investment: float
    loan_amount: float
    total_rental_income: float
    total_expenses: float
    total_cash_flow: float
    total_principal_paydown: float
    final_equity: float
    net_profit: float
    roi: float
    avg_cash_on_cash_return: float
    break_even_year: Optional[int]


@dataclass
class PropertyInvestmentResult:
    input: PropertyInvestmentInput
    mortgage: MortgageDetails
    yearly_projections: List[YearlyProjection]
    summary: InvestmentSummary


class FrenchPropertyInvestmentCalculator:
    """Calculator for French property investment analysis."""

    def analyze(self, input_data: PropertyInvestmentInput) -> PropertyInvestmentResult:
        """Analyze a property investment scenario."""
        self._validate_input(input_data)

        loan_amount = input_data.property_price - input_data.down_payment

        monthly_rate = input_data.interest_rate / 100.0 / 12.0
        num_payments = input_data.loan_term_years * 12

        monthly_mortgage_payment = self._calculate_monthly_payment(
            loan_amount, monthly_rate, num_payments
        )

        monthly_life_insurance = (loan_amount * 0.004) / 12.0
        total_monthly_mortgage = monthly_mortgage_payment + monthly_life_insurance

        total_mortgage_payments = total_monthly_mortgage * num_payments
        total_interest = total_mortgage_payments - loan_amount

        mortgage_details = MortgageDetails(
            monthly_payment=total_monthly_mortgage,
            total_interest=total_interest,
            total_payments=total_mortgage_payments
        )

        arrangement_fee = loan_amount * 0.01
        registration_fee = loan_amount * 0.015
        survey_fee = 750.0
        initial_investment = input_data.down_payment + arrangement_fee + registration_fee + survey_fee

        yearly_projections = []
        cumulative_cash_flow = -initial_investment
        remaining_balance = loan_amount
        break_even_year = None

        for year in range(1, input_data.holding_period_years + 1):
            rent_multiplier = (1 + input_data.rent_increase_annual / 100.0) ** (year - 1)
            base_monthly_rent = input_data.monthly_rent * rent_multiplier
            effective_monthly_rent = base_monthly_rent * (1 - input_data.vacancy_rate / 100.0)
            annual_rental_income = effective_monthly_rent * 12

            annual_mortgage = total_monthly_mortgage * 12
            annual_property_tax = input_data.property_tax_annual
            annual_hoa = input_data.hoa_monthly * 12
            annual_maintenance = input_data.property_price * (input_data.maintenance_percent / 100.0)
            annual_management = base_monthly_rent * 12 * (input_data.management_fee_percent / 100.0)
            annual_insurance = loan_amount * 0.004

            total_expenses = (annual_mortgage + annual_property_tax + annual_hoa +
                            annual_maintenance + annual_management)

            principal_paydown = self._calculate_yearly_principal_paydown(
                remaining_balance,
                monthly_rate,
                total_monthly_mortgage,
                year,
                input_data.loan_term_years
            )

            remaining_balance -= principal_paydown

            net_cash_flow = annual_rental_income - total_expenses
            cumulative_cash_flow += net_cash_flow

            if break_even_year is None and cumulative_cash_flow >= 0:
                break_even_year = year

            total_equity = input_data.down_payment + (loan_amount - remaining_balance)

            yearly_projections.append(YearlyProjection(
                year=year,
                rental_income=annual_rental_income,
                expenses=YearlyExpenses(
                    mortgage=annual_mortgage,
                    property_tax=annual_property_tax,
                    hoa=annual_hoa,
                    maintenance=annual_maintenance,
                    management=annual_management,
                    insurance=annual_insurance,
                    total=total_expenses
                ),
                net_cash_flow=net_cash_flow,
                cumulative_cash_flow=cumulative_cash_flow,
                principal_paydown=principal_paydown,
                total_equity=total_equity,
                remaining_balance=remaining_balance
            ))

        total_rental_income = sum(p.rental_income for p in yearly_projections)
        total_expenses_sum = sum(p.expenses.total for p in yearly_projections)
        total_cash_flow = total_rental_income - total_expenses_sum
        total_principal_paydown = loan_amount - remaining_balance
        final_equity = input_data.down_payment + total_principal_paydown
        net_profit = total_cash_flow + final_equity - initial_investment
        roi = (net_profit / initial_investment) * 100.0
        avg_cash_on_cash_return = (total_cash_flow / input_data.holding_period_years / initial_investment) * 100.0

        summary = InvestmentSummary(
            initial_investment=initial_investment,
            loan_amount=loan_amount,
            total_rental_income=total_rental_income,
            total_expenses=total_expenses_sum,
            total_cash_flow=total_cash_flow,
            total_principal_paydown=total_principal_paydown,
            final_equity=final_equity,
            net_profit=net_profit,
            roi=roi,
            avg_cash_on_cash_return=avg_cash_on_cash_return,
            break_even_year=break_even_year
        )

        return PropertyInvestmentResult(
            input=input_data,
            mortgage=mortgage_details,
            yearly_projections=yearly_projections,
            summary=summary
        )

    def _calculate_monthly_payment(self, principal: float, monthly_rate: float, num_payments: int) -> float:
        """Calculate monthly mortgage payment using amortization formula."""
        if monthly_rate == 0.0:
            return principal / num_payments

        rate_times_one_plus_rate_pow_n = monthly_rate * ((1 + monthly_rate) ** num_payments)
        one_plus_rate_pow_n_minus_one = ((1 + monthly_rate) ** num_payments) - 1

        return principal * rate_times_one_plus_rate_pow_n / one_plus_rate_pow_n_minus_one

    def _calculate_yearly_principal_paydown(
        self,
        starting_balance: float,
        monthly_rate: float,
        monthly_payment: float,
        current_year: int,
        loan_term_years: int
    ) -> float:
        """Calculate principal paid down in a given year."""
        if current_year > loan_term_years:
            return 0.0

        balance = starting_balance
        yearly_principal = 0.0

        for month in range(1, 13):
            if balance <= 0:
                break

            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            yearly_principal += principal_payment
            balance -= principal_payment

        return yearly_principal

    def _validate_input(self, input_data: PropertyInvestmentInput) -> None:
        """Validate input parameters."""
        if input_data.property_price <= 0:
            raise ValueError("Property price must be positive")
        if input_data.down_payment < 0:
            raise ValueError("Down payment cannot be negative")
        if input_data.down_payment >= input_data.property_price:
            raise ValueError("Down payment must be less than property price")
        if input_data.interest_rate <= 0:
            raise ValueError("Interest rate must be positive")
        if input_data.loan_term_years <= 0:
            raise ValueError("Loan term must be positive")
        if input_data.monthly_rent < 0:
            raise ValueError("Monthly rent cannot be negative")
        if input_data.holding_period_years <= 0:
            raise ValueError("Holding period must be positive")
        if input_data.property_tax_annual < 0:
            raise ValueError("Property tax cannot be negative")
        if input_data.hoa_monthly < 0:
            raise ValueError("HOA fees cannot be negative")
        if input_data.maintenance_percent < 0:
            raise ValueError("Maintenance percentage cannot be negative")
        if input_data.management_fee_percent < 0:
            raise ValueError("Management fee percentage cannot be negative")
        if not 0 <= input_data.vacancy_rate <= 100:
            raise ValueError("Vacancy rate must be between 0 and 100")
        if input_data.rent_increase_annual <= -100:
            raise ValueError("Rent increase must be greater than -100%")


def format_table(result: PropertyInvestmentResult) -> str:
    """Format result as a human-readable table."""
    lines = []
    lines.append("\n" + "=" * 80)
    lines.append("FRENCH PROPERTY INVESTMENT ANALYSIS")
    lines.append("=" * 80)

    lines.append("\nINVESTMENT OVERVIEW")
    lines.append("-" * 80)
    lines.append(f"Property Price:        €{result.input.property_price:,.2f}")
    lines.append(f"Down Payment:          €{result.input.down_payment:,.2f}")
    lines.append(f"Loan Amount:           €{result.summary.loan_amount:,.2f}")
    lines.append(f"Initial Investment:    €{result.summary.initial_investment:,.2f}")
    lines.append(f"Interest Rate:         {result.input.interest_rate:.2f}%")
    lines.append(f"Loan Term:             {result.input.loan_term_years} years")
    lines.append(f"Holding Period:        {result.input.holding_period_years} years")

    lines.append("\nMORTGAGE DETAILS")
    lines.append("-" * 80)
    lines.append(f"Monthly Payment:       €{result.mortgage.monthly_payment:,.2f}")
    lines.append(f"Total Interest:        €{result.mortgage.total_interest:,.2f}")
    lines.append(f"Total Payments:        €{result.mortgage.total_payments:,.2f}")

    lines.append("\nRENTAL PARAMETERS")
    lines.append("-" * 80)
    lines.append(f"Monthly Rent:          €{result.input.monthly_rent:,.2f}")
    lines.append(f"Vacancy Rate:          {result.input.vacancy_rate:.2f}%")
    lines.append(f"Rent Increase:         {result.input.rent_increase_annual:.2f}% annually")
    lines.append(f"Management Fee:        {result.input.management_fee_percent:.2f}%")

    lines.append("\nYEARLY PROJECTIONS")
    lines.append("-" * 80)
    lines.append(f"{'Year':<6} {'Rent':<12} {'Expenses':<12} {'Net Cash':<12} {'Cumulative':<14} {'Equity':<12}")
    lines.append("-" * 80)

    for projection in result.yearly_projections:
        lines.append(
            f"{projection.year:<6} "
            f"€{projection.rental_income:<11,.2f} "
            f"€{projection.expenses.total:<11,.2f} "
            f"€{projection.net_cash_flow:<11,.2f} "
            f"€{projection.cumulative_cash_flow:<13,.2f} "
            f"€{projection.total_equity:<11,.2f}"
        )

    lines.append("\nSUMMARY")
    lines.append("-" * 80)
    lines.append(f"Total Rental Income:   €{result.summary.total_rental_income:,.2f}")
    lines.append(f"Total Expenses:        €{result.summary.total_expenses:,.2f}")
    lines.append(f"Total Cash Flow:       €{result.summary.total_cash_flow:,.2f}")
    lines.append(f"Principal Paid:        €{result.summary.total_principal_paydown:,.2f}")
    lines.append(f"Final Equity:          €{result.summary.final_equity:,.2f}")
    lines.append(f"Net Profit:            €{result.summary.net_profit:,.2f}")
    lines.append(f"ROI:                   {result.summary.roi:.2f}%")
    lines.append(f"Avg Cash-on-Cash:      {result.summary.avg_cash_on_cash_return:.2f}%")

    if result.summary.break_even_year:
        lines.append(f"Break-even Year:       {result.summary.break_even_year}")
    else:
        lines.append(f"Break-even Year:       Not reached in {result.input.holding_period_years} years")

    lines.append("=" * 80 + "\n")

    return "\n".join(lines)


def dataclass_to_dict(obj):
    """Convert dataclass to dictionary recursively."""
    if hasattr(obj, '__dataclass_fields__'):
        return {k: dataclass_to_dict(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    return obj


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze French rental property investments"
    )

    parser.add_argument('--property-price', '-p', type=float,
                       help='Property purchase price in EUR')
    parser.add_argument('--down-payment', '-d', type=float,
                       help='Down payment in EUR')
    parser.add_argument('--interest-rate', '-i', type=float,
                       help='Annual interest rate (%%)')
    parser.add_argument('--loan-term', '-l', type=int,
                       help='Loan term in years')
    parser.add_argument('--monthly-rent', '-r', type=float,
                       help='Monthly rental income in EUR')
    parser.add_argument('--holding-period', type=int,
                       help='Investment holding period in years')

    parser.add_argument('--property-tax-annual', type=float, default=0.0,
                       help='Annual property tax (EUR, default: 0)')
    parser.add_argument('--hoa-monthly', type=float, default=0.0,
                       help='Monthly HOA fees (EUR, default: 0)')
    parser.add_argument('--maintenance-percent', type=float, default=1.0,
                       help='Annual maintenance as %% of property value (default: 1.0)')
    parser.add_argument('--management-fee-percent', type=float, default=0.0,
                       help='Property management fee as %% of rent (default: 0)')
    parser.add_argument('--vacancy-rate', type=float, default=0.0,
                       help='Expected vacancy rate %% (default: 0)')
    parser.add_argument('--rent-increase-annual', type=float, default=0.0,
                       help='Annual rent increase %% (default: 0)')

    parser.add_argument('--json-input', action='store_true',
                       help='Read JSON input from stdin')
    parser.add_argument('--format', '-f', choices=['json', 'table'], default='json',
                       help='Output format (default: json)')

    args = parser.parse_args()

    try:
        if args.json_input:
            input_json = sys.stdin.read()
            input_dict = json.loads(input_json)
            input_data = PropertyInvestmentInput(
                property_price=input_dict['propertyPrice'],
                down_payment=input_dict['downPayment'],
                interest_rate=input_dict['interestRate'],
                loan_term_years=input_dict['loanTermYears'],
                monthly_rent=input_dict['monthlyRent'],
                holding_period_years=input_dict['holdingPeriodYears'],
                property_tax_annual=input_dict.get('propertyTaxAnnual', 0.0),
                hoa_monthly=input_dict.get('hoaMonthly', 0.0),
                maintenance_percent=input_dict.get('maintenancePercent', 1.0),
                management_fee_percent=input_dict.get('managementFeePercent', 0.0),
                vacancy_rate=input_dict.get('vacancyRate', 0.0),
                rent_increase_annual=input_dict.get('rentIncreaseAnnual', 0.0)
            )
        else:
            required = [
                args.property_price, args.down_payment, args.interest_rate,
                args.loan_term, args.monthly_rent, args.holding_period
            ]
            if None in required:
                parser.error("All required arguments must be provided when not using --json-input")

            input_data = PropertyInvestmentInput(
                property_price=args.property_price,
                down_payment=args.down_payment,
                interest_rate=args.interest_rate,
                loan_term_years=args.loan_term,
                monthly_rent=args.monthly_rent,
                holding_period_years=args.holding_period,
                property_tax_annual=args.property_tax_annual,
                hoa_monthly=args.hoa_monthly,
                maintenance_percent=args.maintenance_percent,
                management_fee_percent=args.management_fee_percent,
                vacancy_rate=args.vacancy_rate,
                rent_increase_annual=args.rent_increase_annual
            )

        calculator = FrenchPropertyInvestmentCalculator()
        result = calculator.analyze(input_data)

        if args.format == 'json':
            result_dict = dataclass_to_dict(result)
            print(json.dumps(result_dict, indent=2))
        else:
            print(format_table(result))

    except (ValueError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
