"""
cancel_contract.py — 生命保険の契約を解約し contracts.csv を更新する
Usage: python cancel_contract.py --customer_id C002 --contract_id CT008 [--reason 保険料見直し]
"""
import argparse
import csv
import json
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "demo_app" / "data"
CONTRACTS_FILE = BASE / "contracts.csv"
PRODUCTS_FILE = BASE / "products.csv"


def cancel_contract(customer_id: str, contract_id: str, reason: str = "顧客申出") -> dict:
    contracts = []
    with open(CONTRACTS_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        contracts = list(reader)

    target = None
    for c in contracts:
        if c["contract_id"] == contract_id:
            target = c
            break

    if target is None:
        return {"status": "error", "message": f"契約 {contract_id} が見つかりません"}

    if target["customer_id"] != customer_id:
        # Return valid life insurance contract IDs for this customer so the LLM can retry
        valid_ids = [
            c["contract_id"] for c in contracts
            if c["customer_id"] == customer_id and c["contract_status"] == "有効"
        ]
        return {
            "status": "error",
            "message": f"契約 {contract_id} は顧客 {customer_id} に属していません。"
                       f"有効な契約ID: {valid_ids if valid_ids else '（なし）'}。"
                       "正しい contract_id で再実行してください。",
        }

    if target["contract_status"] != "有効":
        return {"status": "error", "message": f"契約 {contract_id} はすでに解約済みまたは無効です"}

    # 商品カテゴリ確認
    product_name = target["product_id"]
    with open(PRODUCTS_FILE, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["product_id"] == target["product_id"]:
                if r["product_category"] != "生命保険":
                    return {"status": "error", "message": "指定された契約は生命保険ではありません"}
                product_name = r["product_name"]
                break

    today = date.today().isoformat()
    target["contract_status"] = "解約"
    target["end_date"] = today

    with open(CONTRACTS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in contracts:
            writer.writerow(row)

    return {
        "status": "success",
        "message": f"生命保険契約 {contract_id} を解約しました",
        "contract_id": contract_id,
        "customer_id": customer_id,
        "product_name": product_name,
        "cancel_date": today,
        "reason": reason,
        "coverage_review_suggestion": "補償内容を見直すことで保険料を抑えつつ必要な保障を維持できる場合があります。ご希望の場合は代替プランをご案内します。",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", required=True)
    parser.add_argument("--contract_id", required=True)
    parser.add_argument("--reason", default="顧客申出")
    args = parser.parse_args()
    print(json.dumps(cancel_contract(args.customer_id, args.contract_id, args.reason), ensure_ascii=False, indent=2))
