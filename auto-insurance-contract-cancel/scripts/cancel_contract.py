"""
cancel_contract.py — 契約を解約ステータスに更新する（自動車・生命保険共用）
Usage: python cancel_contract.py --customer_id C016 --contract_id CT009 --cancel_reason 讲型売却
"""
import argparse
import csv
import json
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).resolve().parents[4] / "demo_app" / "data" / "contracts.csv"


def cancel_contract(contract_id: str, cancel_reason: str) -> dict:
    rows = []
    target = None
    with open(DATA_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["contract_id"] == contract_id:
                if row["contract_status"] != "有効":
                    return {"error": f"契約 {contract_id} は既に解約済みまたは無効です。"}
                row["contract_status"] = "解約"
                row["end_date"] = date.today().isoformat()
                row["notes"] = f"{row['notes']} | 解約日: {date.today().isoformat()} 理由: {cancel_reason}"
                target = row
            rows.append(row)

    if not target:
        return {"error": f"契約ID '{contract_id}' が見つかりません。"}

    with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return {
        "success": True,
        "contract_id": contract_id,
        "cancel_date": date.today().isoformat(),
        "message": f"契約 {contract_id} を解約しました。解約理由: {cancel_reason}",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_id", default="")
    parser.add_argument("--contract_id", required=True)
    parser.add_argument("--cancel_reason", default="顧客申出")
    args = parser.parse_args()
    print(json.dumps(cancel_contract(args.contract_id, args.cancel_reason), ensure_ascii=False, indent=2))
