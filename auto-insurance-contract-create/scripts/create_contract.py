"""
create_contract.py — 自動車保険の新規契約を contracts.csv に登録する
Usage: python create_contract.py --customer_id C016 --product_id P002 --start_date 2026-04-01 --insured_name 又吉佑樹 --payment_method 口座振替
"""
import argparse
import csv
import json
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[4] / "demo_app" / "data"
CONTRACTS_FILE = BASE / "contracts.csv"


def next_contract_id() -> str:
    with open(CONTRACTS_FILE, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return "CT001"
    max_num = max(int(r["contract_id"][2:]) for r in rows if r["contract_id"].startswith("CT"))
    return f"CT{max_num + 1:03d}"


def create_contract(
    customer_id: str,
    product_id: str,
    start_date: str,
    insured_name: str,
    payment_method: str = "口座振替",
) -> dict:
    with open(BASE / "products.csv", encoding="utf-8") as f:
        products = {r["product_id"]: r for r in csv.DictReader(f)}

    product = products.get(product_id)
    if not product:
        return {"error": f"商品ID '{product_id}' は存在しません。"}

    new_id = next_contract_id()
    row = {
        "contract_id": new_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "contract_date": date.today().isoformat(),
        "start_date": start_date,
        "end_date": "",
        "contract_status": "有効",
        "monthly_premium": product["monthly_premium"],
        "coverage_amount": product["coverage_amount"],
        "payment_method": payment_method,
        "insured_name": insured_name,
        "beneficiary_name": "",
        "beneficiary_relation": "",
        "next_review_date": "",
        "notes": f"新規契約 ({product['product_name']})",
    }

    with open(CONTRACTS_FILE, encoding="utf-8") as f:
        fieldnames = csv.DictReader(f).fieldnames

    with open(CONTRACTS_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)

    return {
        "success": True,
        "contract_id": new_id,
        "product_name": product["product_name"],
        "monthly_premium": product["monthly_premium"],
        "start_date": start_date,
        "message": f"契約 {new_id} ({product['product_name']}) を登録しました。月額保険料: {product['monthly_premium']}円",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", required=True)
    parser.add_argument("--product_id", required=True)
    parser.add_argument("--start_date", default=date.today().isoformat())
    parser.add_argument("--insured_name", default="")
    parser.add_argument("--payment_method", default="口座振替")
    args = parser.parse_args()
    print(json.dumps(create_contract(args.customer_id, args.product_id, args.start_date, args.insured_name, args.payment_method), ensure_ascii=False, indent=2))
