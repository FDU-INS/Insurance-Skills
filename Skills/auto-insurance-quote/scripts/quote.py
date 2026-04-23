"""
quote.py — 自動車保険の見積書を生成する
Usage: python quote.py --customer_id C016 --product_id P002 --vehicle_type 普通車 --vehicle_age 0
"""
import argparse
import csv
import json
import uuid
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "demo_app" / "data"


def generate_quote(customer_id: str, product_id: str, vehicle_type: str, vehicle_age: int) -> dict:
    # 商品マスタ
    product = None
    with open(BASE / "products.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["product_id"] == product_id:
                product = r
                break

    if not product:
        return {"error": f"商品 {product_id} が見つかりません"}

    if product["product_category"] != "自動車保険":
        return {"error": f"商品 {product_id} は自動車保険ではありません"}

    base_premium = int(product["monthly_premium"])

    # 割増・割引
    surcharge = 1.0
    notes = []
    if vehicle_age >= 10:
        surcharge += 0.15
        notes.append("車齢10年超のため15%割増")
    if vehicle_type == "軽自動車":
        surcharge -= 0.10
        notes.append("軽自動車割引 -10%")
    if vehicle_type == "SUV":
        surcharge += 0.05
        notes.append("SUV区分のため5%割増")

    monthly = round(base_premium * surcharge)
    annual = monthly * 12

    quote_id = f"QT-{str(uuid.uuid4())[:8].upper()}"
    valid_until = (date.today() + timedelta(days=30)).isoformat()

    return {
        "quote_id": quote_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "product_name": product["product_name"],
        "vehicle_type": vehicle_type,
        "vehicle_age": vehicle_age,
        "base_monthly_premium": base_premium,
        "monthly_premium": monthly,
        "annual_premium": annual,
        "coverage_amount": product["coverage_amount"],
        "description": product["description"],
        "features": product["features"],
        "valid_until": valid_until,
        "notes": notes if notes else ["標準レートが適用されています"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", required=True)
    parser.add_argument("--product_id", required=True)
    parser.add_argument("--vehicle_type", default="普通車")
    parser.add_argument("--vehicle_age", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(generate_quote(args.customer_id, args.product_id, args.vehicle_type, args.vehicle_age), ensure_ascii=False, indent=2))
