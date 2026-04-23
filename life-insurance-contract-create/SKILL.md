---
name: life-insurance-contract-create
description: 受取人情報を含む新規の生命保険契約を contracts.csv に登録する。
---

# life_insurance_contract_create

生命保険の新規契約を締結するスキル。

## 概要
顧客の本人確認完了後、生命保険商品の契約を contracts.csv に新規登録する。受取人情報の取得が必要。

## 入力パラメータ
- `customer_id` (str): 顧客ID（例: C002）
- `product_id` (str): 商品ID（生命保険は P006〜P010）
- `beneficiary_name` (str): 受取人氏名
- `beneficiary_relation` (str): 受取人続柄（例: 配偶者、子、親、その他）

## 出力
- `contract_id`: 新規発行された契約ID
- `customer_id`: 顧客ID
- `product_id`: 商品ID
- `product_name`: 商品名
- `monthly_premium`: 月額保険料
- `start_date`: 契約開始日（当日）
- `beneficiary_name`: 受取人氏名
- `beneficiary_relation`: 受取人続柄
- `status`: `success` / `error`
- `message`: 処理結果メッセージ

## 使用スクリプト
- `scripts/create_contract.py`

## 関連スキル
- `identity_verification`: 事前の本人確認が必須
- `life_insurance_quote`: 契約前に見積書を提示すること
- `activity_log_writer`: 契約完了後にアクティビティを記録

## 注意事項
- 同一顧客が同一商品に有効な契約を持つ場合はエラーを返す
- 受取人情報（`beneficiary_name`, `beneficiary_relation`）は必須
- 健康告知義務について事前に説明を要する
