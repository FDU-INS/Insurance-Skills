---
name: life-insurance-contract-cancel
description: 既存の生命保険契約を解約する。解約前に代替プランの提案も行う。
---

# life_insurance_contract_cancel

生命保険の既存契約を解約するスキル。

## 概要
有効な生命保険契約を解約処理する。このスキルは **必ず2ターンに分けて** 実行すること。

## ⚠️ 必須: 2段階処理フロー

### ステップ1（解約申し出を受けたとき） — 必ずここで応答を止める
1. `life_insurance_recommendation` スキルを使って代替プランを取得し、顧客に提示する
2. 「解約をそのまま進めますか？それとも見直しプランをご検討されますか？」と確認を求める
3. **ここで応答を完了し、顧客の返答を待つ。`cancel_contract.py` は絶対に実行しない。**

### ステップ2（顧客が「解約する」と明示的に返答したとき）
1. `scripts/cancel_contract.py` を実行して解約処理を行う
2. **`load_skill("activity-log-writer")` を実行してスキルを読み込んだうえで**、`scripts/write_activity.py` を呼び出して活動記録を残す
   - スクリプト名は必ず `write_activity.py`。`log_activity.py` は存在しない

> **重要**: ステップ1とステップ2を同一ターンで実行してはならない。代替案を提示した同じメッセージの中で解約スクリプトを呼び出すことは禁止。

## 入力パラメータ
- `customer_id` (str): 顧客ID
- `contract_id` (str): 解約対象の契約ID（例: CT008）
- `reason` (str): 解約理由（例: 保険料負担、補償見直し、その他）

## 出力
- `status`: `success` / `error`
- `message`: 処理結果メッセージ
- `contract_id`: 契約ID
- `product_name`: 解約した商品名
- `cancel_date`: 解約日

## 使用スクリプト
- `scripts/cancel_contract.py`

## 関連スキル
- `life_insurance_recommendation`: 解約前に代替プランを提示すること
- `activity_log_writer`: 解約完了後にアクティビティを記録

## ⚠️ contract_id の取り扱い（重要）
- `contract_id` は **「CT」＋数字** の形式（例: CT008, CT012）
- `product_id` は **「P」＋数字** の形式（例: P007, P008）— これは商品マスタのIDであり、**contract_id とは別物**
- スクリプトに渡す `contract_id` には必ず引き継ぎコンテキストの `contract_id`（CT形式）を使うこと
- `product_id` や `product_name` を `contract_id` として渡してはならない
- 例: `{"customer_id": "C016", "contract_id": "CT008", "reason": "解約希望"}` ← 正しい
- 例: `{"customer_id": "C016", "contract_id": "P007", ...}` ← **誤り（product_id を渡している）**

## 注意事項
- 解約はエージェントが単独で判断せず、必ず顧客の意思確認を行うこと
- 解約前に「補償の見直しで保険料を下げる方法がある」旨を案内する（解約防止）
- 解約後の返戻金は概算を案内（詳細は書面確認を促す）
- 自動車保険との同時解約の場合は無保険リスクを説明すること
