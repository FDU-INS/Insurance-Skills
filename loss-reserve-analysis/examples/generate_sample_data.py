"""Generate a synthetic raw loss transaction dataset for testing the Loss Reserve Analysis skill.

Produces ~500 claims across 5 accident years (2019-2023), each with multiple
evaluation snapshots at 12/31 of each year. The result is a ~2000-row CSV
that mirrors what an actuary would receive from a claims system before
aggregating into a development triangle.

Usage:
    python examples/generate_sample_data.py
    python examples/generate_sample_data.py --seed 42 --output examples/sample_loss_transactions.csv
"""

import argparse
import datetime
from pathlib import Path

import numpy as np
import pandas as pd


def generate_claims(seed=42):
    rng = np.random.default_rng(seed)

    accident_years = [2019, 2020, 2021, 2022, 2023]
    # Slightly increasing claim counts to reflect portfolio growth
    lambdas = {2019: 90, 2020: 85, 2021: 95, 2022: 105, 2023: 110}

    # Development emergence pattern: cumulative % paid by dev month
    # 12mo, 24mo, 36mo, 48mo, 60mo
    emergence = {12: 0.52, 24: 0.77, 36: 0.91, 48: 0.97, 60: 1.00}

    final_eval_date = datetime.date(2023, 12, 31)
    rows = []
    claim_counter = 0

    for ay in accident_years:
        n_claims = rng.poisson(lambdas[ay])
        ay_start = datetime.date(ay, 1, 1)
        ay_end = datetime.date(ay, 12, 31)
        days_in_year = (ay_end - ay_start).days

        for _ in range(n_claims):
            claim_counter += 1
            claim_id = f"CLM-{claim_counter:05d}"

            # Random accident date within the year
            accident_date = ay_start + datetime.timedelta(days=int(rng.integers(0, days_in_year)))

            # Reporting lag: 0-90 days, skewed toward shorter lags
            report_lag = min(int(rng.exponential(scale=15)), 90)
            report_date = accident_date + datetime.timedelta(days=report_lag)

            # Ultimate loss from lognormal — calibrated so paid aggregation
            # roughly matches sample_triangle.csv (e.g., 2019 ultimate ~3070)
            # mean = exp(3.21 + 0.32) ≈ 34, × ~90 claims ≈ 3,060
            log_mean = 3.21
            log_sigma = 0.8
            ultimate = round(rng.lognormal(log_mean, log_sigma), 2)

            # Determine closure: assign a random development month at which claim closes
            # Earlier closure for smaller claims
            if ultimate < 15:
                close_dev = rng.choice([12, 24, 36], p=[0.6, 0.3, 0.1])
            elif ultimate < 65:
                close_dev = rng.choice([12, 24, 36, 48], p=[0.3, 0.35, 0.25, 0.1])
            else:
                close_dev = rng.choice([24, 36, 48, 60], p=[0.2, 0.3, 0.3, 0.2])

            # Generate evaluation rows at 12/31 of each year
            first_eval_year = report_date.year
            for eval_year in range(first_eval_year, 2024):
                eval_date = datetime.date(eval_year, 12, 31)
                if eval_date > final_eval_date:
                    break

                # Development age in months (approximate)
                dev_months = (eval_date.year - ay) * 12

                if dev_months <= 0:
                    dev_months = 12  # at least 12 months if evaluated in accident year

                # Find the emergence bracket
                sorted_devs = sorted(emergence.keys())
                cum_pct = 0.0
                for d in sorted_devs:
                    if dev_months <= d:
                        cum_pct = emergence[d]
                        break
                else:
                    cum_pct = 1.0

                # Add per-claim noise to emergence (+/- 10%)
                noise = rng.normal(1.0, 0.05)
                cum_pct_noisy = min(max(cum_pct * noise, 0.05), 1.0)

                is_closed = dev_months >= close_dev

                if is_closed:
                    paid = round(ultimate, 2)
                    case_reserve = 0.0
                else:
                    paid = round(ultimate * cum_pct_noisy, 2)
                    # Case reserve: estimate of remaining, with some noise
                    remaining_estimate = ultimate - paid
                    reserve_noise = rng.normal(1.0, 0.15)
                    case_reserve = round(max(remaining_estimate * reserve_noise, 0.0), 2)

                incurred = round(paid + case_reserve, 2)

                rows.append({
                    "claim_id": claim_id,
                    "accident_date": accident_date.isoformat(),
                    "report_date": report_date.isoformat(),
                    "evaluation_date": eval_date.isoformat(),
                    "paid_loss": paid,
                    "case_reserve": case_reserve,
                    "incurred_loss": incurred,
                })

    df = pd.DataFrame(rows)
    return df


def generate_premium():
    """Generate earned premium by accident year.

    Deterministic (not random) — premium is a known exposure measure.
    Calibrated so loss ratios are ~60-73% against sample_triangle.csv ultimates.
    ~4% annual growth mirrors the portfolio growth in claim counts.
    """
    return pd.DataFrame({
        "Accident Year": [2019, 2020, 2021, 2022, 2023],
        "Earned Premium": [4200, 4350, 4550, 4800, 5050],
    })


def print_summary(df, premium_df=None):
    print(f"Total rows: {len(df)}")
    print(f"Unique claims: {df['claim_id'].nunique()}")
    print()

    df_copy = df.copy()
    df_copy["accident_year"] = pd.to_datetime(df_copy["accident_date"]).dt.year
    df_copy["eval_year"] = pd.to_datetime(df_copy["evaluation_date"]).dt.year
    df_copy["dev_period"] = df_copy["eval_year"] - df_copy["accident_year"] + 1

    # Show aggregated paid triangle for verification
    paid_tri = df_copy.groupby(["accident_year", "dev_period"])["paid_loss"].sum().unstack()
    paid_tri = paid_tri.round(0).astype("Int64")
    print("Aggregated paid triangle (for verification):")
    print(paid_tri.to_string())
    print()

    # Show aggregated incurred triangle for verification
    triangle = df_copy.groupby(["accident_year", "dev_period"])["incurred_loss"].sum().unstack()
    triangle = triangle.round(0).astype("Int64")
    print("Aggregated incurred triangle (for verification):")
    print(triangle.to_string())
    print()

    if premium_df is not None:
        print("Earned premium:")
        print(premium_df.to_string(index=False))
        print()


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic loss transaction data")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output CSV path (default: sample_loss_transactions.csv in same directory)")
    parser.add_argument("--premium-output", type=str, default=None,
                        help="Premium CSV path (default: sample_premium.csv in same directory)")
    args = parser.parse_args()

    df = generate_claims(seed=args.seed)
    premium_df = generate_premium()

    examples_dir = Path(__file__).parent

    output_path = args.output if args.output else examples_dir / "sample_loss_transactions.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {output_path}")

    premium_path = args.premium_output if args.premium_output else examples_dir / "sample_premium.csv"
    premium_df.to_csv(premium_path, index=False)
    print(f"Generated {premium_path}")

    print()
    print_summary(df, premium_df)


if __name__ == "__main__":
    main()
