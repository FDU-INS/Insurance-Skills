import argparse
import sys
import json

def calculate_initial_csm(pv_premiums, pv_claims, pv_expenses, risk_adjustment):
    """
    Calculates the Initial Contractual Service Margin (CSM) under IFRS 17 (GMM/BBA).
    pv_premiums: Present value of expected future premiums (cash INFLOW)
    pv_claims: Present value of expected future claims (cash OUTFLOW)
    pv_expenses: Present value of expected future expenses (cash OUTFLOW)
    risk_adjustment: Risk Adjustment for Non-Financial Risk
    """
    
    # Fulfillment Cash Flows (FCF) = PV(Outflows) - PV(Inflows) + Risk Adjustment
    # Under IFRS 17, Inflows are negative, Outflows are positive
    pv_outflows = pv_claims + pv_expenses
    pv_inflows = -pv_premiums # Inflows reduce the liability
    
    fcf = pv_outflows + pv_inflows + risk_adjustment
    
    # If FCF < 0 (Profitable), set CSM to offset it (so Initial LRC is 0)
    # If FCF > 0 (Onerous/Loss-Making), CSM is 0 and loss is recognized immediately
    csm = max(0, -fcf)
    loss_component = max(0, fcf)
    
    initial_lrc = fcf + csm
    
    return {
        "pv_inflows": pv_inflows,
        "pv_outflows": pv_outflows,
        "risk_adjustment": risk_adjustment,
        "fcf": fcf,
        "csm": csm,
        "loss_component": loss_component,
        "initial_lrc": initial_lrc
    }

def main():
    parser = argparse.ArgumentParser(description="IFRS 17 Initial CSM Calculator (GMM)")
    parser.add_argument("--pv-premiums", type=float, required=True, help="Present Value of Expected Premiums")
    parser.add_argument("--pv-claims", type=float, required=True, help="Present Value of Expected Claims")
    parser.add_argument("--pv-expenses", type=float, required=True, help="Present Value of Expected Expenses")
    parser.add_argument("--risk-adj", type=float, required=True, help="Risk Adjustment for Non-Financial Risk")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    
    args = parser.parse_args()
    
    result = calculate_initial_csm(
        args.pv_premiums,
        args.pv_claims,
        args.pv_expenses,
        args.risk_adj
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=== IFRS 17 Initial Measurement (GMM) ===")
        print(f"PV of Inflows (Premiums):    {result['pv_inflows']:,.2f}")
        print(f"PV of Outflows (Claims/Exp): {result['pv_outflows']:,.2f}")
        print(f"Risk Adjustment (RA):        {result['risk_adjustment']:,.2f}")
        print("-" * 40)
        print(f"Fulfillment Cash Flows(FCF): {result['fcf']:,.2f}")
        print("-" * 40)
        
        if result['csm'] > 0:
            print(f"Contract is Profitable. Initial CSM: {result['csm']:,.2f}")
        else:
            print(f"Contract is Onerous. Loss Component: {result['loss_component']:,.2f}")
            
        print(f"Initial LRC:                 {result['initial_lrc']:,.2f}")

if __name__ == "__main__":
    main()
