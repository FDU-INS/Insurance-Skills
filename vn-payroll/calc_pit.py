import argparse
import locale

locale.setlocale(locale.LC_ALL, '')

# Vietnam Tax Configuration (2025 Assumptions)
SELF_DEDUCTION = 11_000_000
DEPENDENT_DEDUCTION = 4_400_000
INSURANCE_CAP_SALARY = 46_800_000  # 20x Base Salary (approx)
# Rates
BHXH_RATE = 0.08
BHYT_RATE = 0.015
BHTN_RATE = 0.01

def calculate_pit(taxable_income):
    if taxable_income <= 0: return 0
    
    # Progressive Tax Brackets (Million VND)
    brackets = [
        (80_000_000, 0.35, 9_850_000),
        (52_000_000, 0.30, 5_850_000),
        (32_000_000, 0.25, 3_250_000),
        (18_000_000, 0.20, 1_650_000),
        (10_000_000, 0.15, 750_000),
        (5_000_000,  0.10, 250_000),
        (0,          0.05, 0)
    ]
    
    for limit, rate, subtraction in brackets:
        if taxable_income > limit:
            return (taxable_income * rate) - subtraction
    return 0

def main():
    parser = argparse.ArgumentParser(description="Vietnam PIT Calculator")
    parser.add_argument("--gross", type=float, required=True, help="Gross monthly income")
    parser.add_argument("--dependents", type=int, default=0, help="Number of dependents")
    parser.add_argument("--region", type=int, default=1, help="Region ID")
    
    args = parser.parse_args()
    
    # Insurance Calculation
    insurance_base = min(args.gross, INSURANCE_CAP_SALARY)
    social_ins = insurance_base * BHXH_RATE
    health_ins = insurance_base * BHYT_RATE
    unemp_ins = insurance_base * BHTN_RATE
    total_insurance = social_ins + health_ins + unemp_ins
    
    # Taxable Income Calculation
    income_before_tax = args.gross - total_insurance
    total_deductions = SELF_DEDUCTION + (args.dependents * DEPENDENT_DEDUCTION)
    taxable_income = max(0, income_before_tax - total_deductions)
    
    # Tax Calculation
    pit = calculate_pit(taxable_income)
    
    # Net
    net_income = args.gross - total_insurance - pit
    
    # Formatted Output
    print(f"{'--- VIETNAM PAYROLL BREAKDOWN ---':<35}")
    print(f"{'GROSS INCOME':<20}: {args.gross:,.0f} VND")
    print(f"{'Dependents':<20}: {args.dependents}")
    print("-" * 35)
    print(f"{'Social Ins (8%)':<20}: -{social_ins:,.0f}")
    print(f"{'Health Ins (1.5%)':<20}: -{health_ins:,.0f}")
    print(f"{'Unemp Ins (1%)':<20}: -{unemp_ins:,.0f}")
    print("-" * 35)
    print(f"{'Taxable Income':<20}: {taxable_income:,.0f}")
    print(f"{'PIT':<20}: -{pit:,.0f}")
    print("=" * 35)
    print(f"{'NET INCOME':<20}: {net_income:,.0f} VND")
    print("=" * 35)

if __name__ == "__main__":
    main()