import argparse
import sys
import json
import math

def calculate_life_valuation(issue_age, interest_rate, term, mortality_type, mortality_rate):
    """
    Calculates Actuarial Present Value (APV) for:
    - n-Year Term Life Insurance ($A^1_{x:n}$)
    - Whole Life Insurance ($A_x$)
    - n-Year Endowment Insurance ($A_{x:n}$)
    - Whole Life Annuity Due ($\ddot{a}_x$)
    
    Assuming benefits are paid at the end of the year of death.
    """
    
    # Simple Constant Force of Mortality approximation
    # qx = 1 - exp(-mu)
    qx = mortality_rate
    px = 1.0 - qx
    v = 1.0 / (1.0 + interest_rate)
    
    max_age = 120
    remaining_years = min(term if term > 0 else max_age - issue_age, max_age - issue_age)

    term_apv = 0.0
    whole_life_apv = 0.0
    annuity_due_apv = 0.0
    survival_prob = 1.0
    
    # Calculate for n years
    for t in range(remaining_years):
        # Probability of surviving exactly t years and dying in year t+1
        # t|qx = tpx * q_{x+t}
        t_px_qx = survival_prob * qx
        
        # Present value of 1 unit paid at the end of year t+1
        discount = v ** (t + 1)
        
        # Term Life Insurance
        term_apv += t_px_qx * discount
        
        # Annuity Due (paid at start of year, so no discount for year 0)
        annuity_due_apv += survival_prob * (v ** t)
        
        # Update survival probability for next year
        survival_prob *= px
        
    # Endowment Insurance (Term + Pure Endowment)
    # Pure Endowment: survives exactly n years, receives 1
    pure_endowment = survival_prob * (v ** remaining_years)
    endowment_apv = term_apv + pure_endowment
    
    # Whole Life Insurance (Calculated to max age 120)
    survival_prob_wl = 1.0
    for t in range(max_age - issue_age):
        t_px_qx = survival_prob_wl * qx
        discount = v ** (t + 1)
        whole_life_apv += t_px_qx * discount
        survival_prob_wl *= px

    # Annual Level Premium for Whole Life = A_x / a_ddot_x
    # Annual Level Premium for n-Year Endowment = A_x:n / a_ddot_x:n
    
    return {
        "issue_age": issue_age,
        "interest_rate": interest_rate,
        "mortality_type": mortality_type,
        "mortality_rate": mortality_rate,
        "term": remaining_years,
        "term_life_apv": term_apv,
        "whole_life_apv": whole_life_apv,
        "endowment_apv": endowment_apv,
        "annuity_due_apv": annuity_due_apv,
        "pure_endowment": pure_endowment
    }

def main():
    parser = argparse.ArgumentParser(description="Actuarial Present Value Calculator")
    parser.add_argument("--age", type=int, required=True, help="Issue Age (e.g., 35)")
    parser.add_argument("--interest", type=float, required=True, help="Annual Interest Rate (e.g., 0.05 for 5%)")
    parser.add_argument("--term", type=int, default=0, help="Term of policy in years (0 for Whole Life)")
    parser.add_argument("--mortality", type=float, default=0.01, help="Constant Mortality Rate (qx)")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    
    args = parser.parse_args()
    
    if args.age < 0 or args.age >= 120:
        print(json.dumps({"error": "Issue age must be between 0 and 119."}))
        sys.exit(1)
        
    result = calculate_life_valuation(
        args.age,
        args.interest,
        args.term,
        "Constant Force",
        args.mortality
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=== Life Valuation: Actuarial Present Value ===")
        print(f"Issue Age (x):             {result['issue_age']}")
        print(f"Term (n):                  {result['term']} years")
        print(f"Interest Rate (i):         {result['interest_rate']*100:.2f}%")
        print(f"Mortality Rate (qx):       {result['mortality_rate']*100:.2f}% (Constant)")
        print("-" * 47)
        print(f"n-Year Term Life A_1_x:n:  {result['term_life_apv']:.4f}")
        print(f"n-Year Pure Endowment:     {result['pure_endowment']:.4f}")
        print(f"n-Year Endowment A_x:n:    {result['endowment_apv']:.4f}")
        print(f"Whole Life A_x:            {result['whole_life_apv']:.4f}")
        print(f"Annuity Due a_ddot_x:      {result['annuity_due_apv']:.4f}")

if __name__ == "__main__":
    main()
