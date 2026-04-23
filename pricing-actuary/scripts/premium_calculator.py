import argparse
import sys
import json

def calculate_premiums(frequency, severity, admin_expense_fixed, expense_ratio, profit_margin_ratio):
    """Calculates pure premium and gross premium based on risk and loadings."""
    
    # Pure Risk Premium
    pure_premium = frequency * severity
    
    # Gross Premium = (Pure Premium + Fixed Admin) / (1 - Expense Ratio - Profit Margin Ratio)
    # Ensure denominator > 0
    denominator = 1.0 - expense_ratio - profit_margin_ratio
    
    if denominator <= 0:
        print(json.dumps({"error": "Expense ratio + Profit Margin ratio must be less than 1.0"}))
        sys.exit(1)
        
    gross_premium = (pure_premium + admin_expense_fixed) / denominator
    
    return {
        "pure_premium": pure_premium,
        "expense_loading": (gross_premium * expense_ratio) + admin_expense_fixed,
        "profit_loading": gross_premium * profit_margin_ratio,
        "gross_premium": gross_premium
    }

def main():
    parser = argparse.ArgumentParser(description="Actuarial Premium Calculator")
    parser.add_argument("--frequency", type=float, required=True, help="Expected claims frequency (e.g., 0.05 for 5%)")
    parser.add_argument("--severity", type=float, required=True, help="Average cost per claim (e.g., 10000)")
    parser.add_argument("--fixed-expense", type=float, default=0.0, help="Fixed administrative expense per policy")
    parser.add_argument("--variable-expense", type=float, default=0.15, help="Variable expense ratio as % of gross premium (e.g., 0.15 for 15%)")
    parser.add_argument("--profit-margin", type=float, default=0.05, help="Profit margin as % of gross premium (e.g., 0.05 for 5%)")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    
    args = parser.parse_args()
    
    result = calculate_premiums(
        args.frequency,
        args.severity,
        args.fixed_expense,
        args.variable_expense,
        args.profit_margin
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=== Pricing Summary ===")
        print(f"Frequency:         {args.frequency}")
        print(f"Severity:          {args.severity}")
        print(f"Pure Premium:      {result['pure_premium']:.2f}")
        print("-----------------------")
        print(f"Expense Loading:   {result['expense_loading']:.2f}")
        print(f"Profit Loading:    {result['profit_loading']:.2f}")
        print("-----------------------")
        print(f"Gross Premium:     {result['gross_premium']:.2f}")

if __name__ == "__main__":
    main()
