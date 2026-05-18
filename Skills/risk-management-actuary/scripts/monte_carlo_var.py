import argparse
import sys
import json
import math
import random

def calculate_monte_carlo_var(initial_value, drift, volatility, time_horizon, simulations, confidence_level):
    """
    Simulates portfolio paths using Geometric Brownian Motion (GBM).
    Returns the Empirical VaR and Conditional Tail Expectation (CTE / Expected Shortfall).
    All parameters are annualized.
    """
    # Simulate final portfolio values
    final_values = []
    
    # Pre-calculate constants for GBM: S_t = S_0 * exp((mu - sigma^2 / 2)*t + sigma * W_t)
    drift_term = (drift - 0.5 * volatility**2) * time_horizon
    vol_term = volatility * math.sqrt(time_horizon)
    
    for _ in range(simulations):
        # Generate random standard normal variable (Box-Muller transform)
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2.0 * math.log(max(1e-10, u1))) * math.cos(2.0 * math.pi * u2)
        
        # Calculate path ending value
        path_value = initial_value * math.exp(drift_term + vol_term * z)
        final_values.append(path_value)
        
    # Calculate losses (Initial - Final)
    # Positive loss means the portfolio dropped in value
    losses = [initial_value - v for v in final_values]
    
    # Sort losses to find percentiles
    losses.sort()
    
    # VaR Index calculation (e.g., 99% VaR means the 99th percentile of losses)
    var_index = int(confidence_level * simulations) - 1
    # Handle index out of bounds
    var_index = max(0, min(var_index, simulations - 1))
    
    var = losses[var_index]
    
    # CTE / Expected Shortfall (Average of losses greater than VaR)
    tail_losses = losses[var_index:]
    if len(tail_losses) > 0:
        cte = sum(tail_losses) / len(tail_losses)
    else:
        cte = var
        
    # Return worst case (max loss) and best case (min loss)
    worst_case = losses[-1]
    best_case = losses[0]

    return {
        "initial_value": initial_value,
        "simulations": simulations,
        "confidence_level": confidence_level,
        "var": var,
        "cte": cte,
        "worst_case_loss": worst_case,
        "best_case_loss": best_case
    }

def main():
    parser = argparse.ArgumentParser(description="Monte Carlo VaR & CTE Calculator (GBM)")
    parser.add_argument("--initial-value", type=float, required=True, help="Initial portfolio value")
    parser.add_argument("--drift", type=float, required=True, help="Annual expected return (e.g., 0.05 for 5%)")
    parser.add_argument("--volatility", type=float, required=True, help="Annual volatility (e.g., 0.15 for 15%)")
    parser.add_argument("--horizon", type=float, default=1.0, help="Time horizon in years (default: 1.0)")
    parser.add_argument("--simulations", type=int, default=10000, help="Number of Monte Carlo paths (default: 10000)")
    parser.add_argument("--confidence", type=float, default=0.99, help="Confidence level for VaR (e.g., 0.99 for 99%)")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    
    args = parser.parse_args()
    
    if args.confidence <= 0 or args.confidence >= 1:
        print(json.dumps({"error": "Confidence level must be between 0 and 1 exclusive."}))
        sys.exit(1)
        
    result = calculate_monte_carlo_var(
        args.initial_value,
        args.drift,
        args.volatility,
        args.horizon,
        args.simulations,
        args.confidence
    )
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=== Risk Management: Monte Carlo Analysis ===")
        print(f"Initial Value:           {result['initial_value']:,.2f}")
        print(f"Drift/Volatility:        {args.drift*100:.1f}% / {args.volatility*100:.1f}%")
        print(f"Horizon/Simulations:     {args.horizon} yrs / {result['simulations']:,}")
        print(f"Confidence Level:        {result['confidence_level']*100:.1f}%")
        print("-" * 45)
        print(f"Value at Risk (VaR):     {result['var']:,.2f}")
        print(f"Conditional Tail (CTE):  {result['cte']:,.2f}")
        print("-" * 45)
        print(f"Worst Case Loss (Max):   {result['worst_case_loss']:,.2f}")
        print(f"Best Case Loss (Min):    {result['best_case_loss']:,.2f}")

if __name__ == "__main__":
    main()
