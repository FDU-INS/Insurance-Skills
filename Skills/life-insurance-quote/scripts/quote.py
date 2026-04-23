"""
quote.py — 生命保険の見積書を生成する
Usage: python quote.py --customer_id C002 --product_id P007 [--gender 女性] [--health_status 良好]
"""
import argparse
import csv
import json
import uuid
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "demo_app" / "data"


def generate_quote(customer_id: str, product_id: str, gender: str = "男性", health_status: str = "良好") -> dict:
    product = None
    with open(BASE / "products.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["product_id"] == product_id:
                product = r
                break

    if not product:
        return {"error": f"商品 {product_id} が見つかりません"}

    if product["product_category"] != "生命保険":
        return {"error": f"商品 {product_id} は生命保険ではありません"}

    base_premium = int(product["monthly_premium"])
    surcharge = 1.0
    notes = []

    if gender == "女性" and product_id in ("P006", "P008"):
        surcharge -= 0.05
        notes.append("女性割引 -5%")
    if health_status == "注意":
        surcharge += 0.10
        notes.append("健康状態「注意」のため10%割増（審査が必要）")
    elif health_status == "要観察":
        surcharge += 0.25
        notes.append("健康状態「要観察」のため25%割増（審査が必要）")

    monthly = round(base_premium * surcharge)
    annual = monthly * 12

    return {
        "quote_id": f"QL-{str(uuid.uuid4())[:8].upper()}",
        "customer_id": customer_id,
        "product_id": product_id,
        "product_name": product["product_name"],
        "gender": gender,
        "health_status": health_status,
        "base_monthly_premium": base_premium,
        "monthly_premium": monthly,
        "annual_premium": annual,
        "coverage_amount": product["coverage_amount"],
        "description": product["description"],
        "features": product["features"],
        "valid_until": (date.today() + timedelta(days=30)).isoformat(),
        "notes": notes if notes else ["標準レートが適用されています"],
        "disclosure_notice": "ご契約には健康状態の告知義務があります。告知義務違反があった場合、ご契約が解除されることがあります。",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", required=True)
    parser.add_argument("--product_id", required=True)
    parser.add_argument("--gender", default="男性")
    parser.add_argument("--health_status", default="良好")
    args = parser.parse_args()
    print(json.dumps(generate_quote(args.customer_id, args.product_id, args.gender, args.health_status), ensure_ascii=False, indent=2))
