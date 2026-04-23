"""
recommend.py — 顧客の年齢・年収をもとに自動車保険プランを提案する
Usage: python recommend.py --age 31 --annual_income 5500000 [--customer_id C016]
"""
import argparse
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "demo_app" / "data"


def recommend(age: int, annual_income: int, customer_id: str = "") -> dict:
    with open(BASE / "products.csv", encoding="utf-8") as f:
        products = [r for r in csv.DictReader(f) if r["product_category"] == "自動車保険"]

    # 既契約チェック
    existing = []
    if customer_id:
        with open(BASE / "contracts.csv", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["customer_id"] == customer_id and r["contract_status"] == "有効":
                    existing.append(r["product_id"])

    eligible = [
        p for p in products
        if int(p["target_age_min"]) <= age <= int(p["target_age_max"])
        and p["product_id"] not in existing
    ]

    # 優先順位付け
    def score(p: dict) -> int:
        s = 0
        pid = p["product_id"]
        premium = int(p["monthly_premium"])
        if age <= 25 and pid == "P004":
            s += 10
        if age >= 60 and pid == "P005":
            s += 10
        if annual_income >= 10_000_000 and pid == "P003":
            s += 8
        if annual_income >= 5_000_000 and pid in ("P002", "P003"):
            s += 5
        if annual_income < 4_000_000 and pid == "P001":
            s += 5
        return s

    ranked = sorted(eligible, key=score, reverse=True)[:3]

    return {
        "recommendations": [
            {
                "product_id": p["product_id"],
                "product_name": p["product_name"],
                "monthly_premium": p["monthly_premium"],
                "description": p["description"],
                "features": p["features"],
            }
            for p in ranked
        ],
        "existing_auto_contracts": existing,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--age", type=int, required=True)
    parser.add_argument("--annual_income", type=int, required=True)
    parser.add_argument("--customer_id", default="")
    args = parser.parse_args()
    print(json.dumps(recommend(args.age, args.annual_income, args.customer_id), ensure_ascii=False, indent=2))
