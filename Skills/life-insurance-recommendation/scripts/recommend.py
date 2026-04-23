"""
recommend.py — 顧客の属性をもとに生命保険プランを提案する
Usage: python recommend.py --customer_id C016 [--marital_status 未婚]
       python recommend.py --age 31 --annual_income 5500000 [--marital_status 未婚]
"""
import argparse
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "demo_app" / "data"


def _load_customer(customer_id: str) -> dict:
    with open(BASE / "customers.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["customer_id"] == customer_id:
                return r
    return {}


def recommend(age: int, annual_income: int, marital_status: str = "未婚", customer_id: str = "") -> dict:
    with open(BASE / "products.csv", encoding="utf-8") as f:
        products = [r for r in csv.DictReader(f) if r["product_category"] == "生命保険"]

    existing = []
    if customer_id:
        with open(BASE / "contracts.csv", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["customer_id"] == customer_id and r["contract_status"] == "有効":
                    existing.append(r["product_id"])

    eligible = [
        p for p in products
        if int(p["target_age_min"]) <= age <= int(p["target_age_max"])
    ]

    def score(p: dict) -> int:
        s = 0
        pid = p["product_id"]
        if age >= 60 and pid == "P010":
            s += 10
        if marital_status == "既婚" and pid == "P007":
            s += 9
        if annual_income >= 10_000_000 and pid == "P006":
            s += 8
        if age >= 40 and pid == "P009":
            s += 7
        if pid == "P008":
            s += 5
        if pid in existing:
            s -= 20  # 重複
        return s

    ranked = sorted(eligible, key=score, reverse=True)[:3]

    return {
        "recommendations": [
            {
                "product_id": p["product_id"],
                "product_name": p["product_name"],
                "monthly_premium": p["monthly_premium"],
                "coverage_amount": p["coverage_amount"],
                "description": p["description"],
                "features": p["features"],
                "already_contracted": p["product_id"] in existing,
            }
            for p in ranked
        ],
        "existing_life_contracts": existing,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", default="")
    parser.add_argument("--age", type=int, default=None)
    parser.add_argument("--annual_income", type=int, default=None)
    parser.add_argument("--marital_status", default="未婚")
    args = parser.parse_args()

    age_val = args.age
    income_val = args.annual_income
    marital_val = args.marital_status

    if args.customer_id and (age_val is None or income_val is None):
        cust = _load_customer(args.customer_id)
        if not cust:
            print(json.dumps({"error": f"顧客 {args.customer_id} が見つかりません"}, ensure_ascii=False))
            raise SystemExit(1)
        if age_val is None:
            age_val = int(cust.get("age", 0))
        if income_val is None:
            income_val = int(cust.get("annual_income", 0))

    if age_val is None or income_val is None:
        parser.error("--customer_id または (--age と --annual_income) が必要です")

    print(json.dumps(recommend(age_val, income_val, marital_val, args.customer_id), ensure_ascii=False, indent=2))
