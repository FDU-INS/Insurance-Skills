import argparse
import sys
import json
import csv
from math import isclose

def calculate_chain_ladder(triangle_data):
    """
    triangle_data: list of lists (rows: origin year, cols: development periods)
    """
    n = len(triangle_data)
    
    # Calculate age-to-age (link) ratios
    link_ratios = []
    for j in range(n - 1):
        sum_prev = 0
        sum_curr = 0
        for i in range(n - 1 - j):
            if triangle_data[i][j] is not None and triangle_data[i][j+1] is not None:
                sum_prev += triangle_data[i][j]
                sum_curr += triangle_data[i][j+1]
        
        if sum_prev > 0:
            ratio = sum_curr / sum_prev
            link_ratios.append(ratio)
        else:
            link_ratios.append(1.0) # Fallback if no data

    # Project ultimate claims
    ultimates = []
    ibnr = []
    
    for i in range(n):
        # Find the latest available data point for origin year i
        latest_val = None
        latest_idx = -1
        for j in range(n):
            if j < len(triangle_data[i]) and triangle_data[i][j] is not None:
                latest_val = triangle_data[i][j]
                latest_idx = j
                
        if latest_val is None:
            ultimates.append(0)
            ibnr.append(0)
            continue
            
        # Project forward using cumulative link ratios
        projected = latest_val
        for j in range(latest_idx, n - 1):
            if j < len(link_ratios):
                projected *= link_ratios[j]
                
        ultimates.append(projected)
        ibnr.append(projected - latest_val)

    return {
        "link_ratios": link_ratios,
        "ultimates": ultimates,
        "ibnr": ibnr,
        "total_ibnr": sum(ibnr)
    }

def main():
    parser = argparse.ArgumentParser(description="Actuarial Chain Ladder Method Calculator")
    parser.add_argument("--json-data", type=str, help="JSON string representing the runoff triangle (list of lists)")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    
    args = parser.parse_args()
    
    if args.json_data:
        try:
            triangle = json.loads(args.json_data)
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON format for --json-data"}))
            sys.exit(1)
    else:
        # Default sample data if not provided (Origin Years 1-4, Dev Years 1-4)
        triangle = [
            [100, 150, 175, 180],
            [110, 168, 192, None],
            [115, 176, None, None],
            [122, None, None, None]
        ]
        
    result = calculate_chain_ladder(triangle)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=== Chain Ladder Reserving Output ===")
        print(f"Link Ratios (Age-to-Age): {[round(r, 4) for r in result['link_ratios']]}")
        print("-------------------------------------")
        print(f"{'Origin':<10} | {'Ultimate':<15} | {'IBNR':<15}")
        print("-" * 45)
        for i in range(len(result['ultimates'])):
            print(f"Year {i+1:<5} | {result['ultimates'][i]:<15.2f} | {result['ibnr'][i]:<15.2f}")
        print("-" * 45)
        print(f"TOTAL IBNR RESERVE: {result['total_ibnr']:.2f}")

if __name__ == "__main__":
    main()
