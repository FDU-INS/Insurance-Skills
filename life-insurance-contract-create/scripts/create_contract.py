"""
create_contract.py — 生命保険の新規契約を contracts.csv に追加する
Usage: python create_contract.py --customer_id C016 --product_id P007 --beneficiary_name 又吉花子 --beneficiary_relation 配偶者
"""
import argparse
import csv
import json
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "demo_app" / "data"
CONTRACTS_FILE = BASE / "contracts.csv"
PRODUCTS_FILE = BASE / "products.csv"


def create_contract(customer_id: str, product_id: str, beneficiary_name: str, beneficiary_relation: str) -> dict:
    # 商品存在確認
    product = None
    with open(PRODUCTS_FILE, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["product_id"] == product_id:
                product = r
                break

    if not product:
        return {"status": "error", "message": f"商品 {product_id} が見つかりません"}

    if product["product_category"] != "生命保険":
        return {"status": "error", "message": f"商品 {product_id} は生命保険ではありません"}

    # 受取人情報チェック
    if not beneficiary_name.strip():
        return {"status": "error", "message": "受取人氏名は必須です"}
    if not beneficiary_relation.strip():
        return {"status": "error", "message": "受取人続柄は必須です"}

    # 重複契約チェック
    contracts = []
    with open(CONTRACTS_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        contracts = list(reader)

    for c in contracts:
        if c["customer_id"] == customer_id and c["product_id"] == product_id and c["contract_status"] == "有効":
            return {"status": "error", "message": f"顧客 {customer_id} はすでに {product_id} の有効な契約を保有しています"}

    # 新規契約ID生成
    existing_ids = [int(c["contract_id"][2:]) for c in contracts if c["contract_id"].startswith("CT")]
    new_num = max(existing_ids, default=0) + 1
    contract_id = f"CT{new_num:03d}"

    today = date.today().isoformat()
    new_row = {
        "contract_id": contract_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "contract_status": "有効",
        "start_date": today,
        "end_date": "",
        "monthly_premium": product["monthly_premium"],
        "coverage_amount": product["coverage_amount"],
        "beneficiary_name": beneficiary_name,
        "beneficiary_relation": beneficiary_relation,
    }

    # CSV 追記
    # 既存ファイルの fieldnames に beneficiary 列がなければ追加
    all_fields = list(fieldnames) if fieldnames else list(new_row.keys())
    for col in ("beneficiary_name", "beneficiary_relation"):
        if col not in all_fields:
            all_fields.append(col)

    contracts.append(new_row)
    with open(CONTRACTS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_fields, extrasaction="ignore")
        writer.writeheader()
        for row in contracts:
            writer.writerow(row)

    return {
        "status": "success",
        "message": f"生命保険契約 {contract_id} を新規登録しました",
        "contract_id": contract_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "product_name": product["product_name"],
        "monthly_premium": int(product["monthly_premium"]),
        "start_date": today,
        "beneficiary_name": beneficiary_name,
        "beneficiary_relation": beneficiary_relation,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", required=True)
    parser.add_argument("--product_id", required=True)
    parser.add_argument("--beneficiary_name", required=True)
    parser.add_argument("--beneficiary_relation", required=True)
    args = parser.parse_args()
    print(json.dumps(create_contract(args.customer_id, args.product_id, args.beneficiary_name, args.beneficiary_relation), ensure_ascii=False, indent=2))
