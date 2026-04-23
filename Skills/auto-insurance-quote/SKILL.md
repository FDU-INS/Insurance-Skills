---
name: auto-insurance-quote
description: 車種・年齢に応じた保険料を算出し、自動車保険の正式見積もりを作成する。
---

# auto_insurance_quote

自動車保険の正式見積書を作成するスキル。

## 概要
顧客の車種情報、年齢、希望プランを受け取り、月額保険料・補償内容・特約オプションを含む詳細見積書を生成する。

## 入力パラメータ
- `customer_id` (str): 顧客ID（例: C016）
- `product_id` (str): 対象商品ID（例: P002）
- `vehicle_type` (str): 車種区分（例: 普通車、軽自動車、SUV）
- `vehicle_age` (int): 車齢（年）。**「新車」「新車・購入予定」「0年」はすべて整数 `0` として渡すこと**（文字列「新車」は不可）

## 出力
- `quote_id`: 見積番号（一時ID）
- `product_name`: 商品名
- `monthly_premium`: 月額保険料（円）
- `annual_premium`: 年額保険料（円）
- `coverage_details`: 補償詳細リスト
- `valid_until`: 見積有効期限（発行日 +30日）
- `notes`: 注意事項

## 使用スクリプト
- `scripts/quote.py`

## 関連スキル
- `auto_insurance_recommendation`: 商品選定時に先行して実行
- `auto_insurance_contract_create`: 見積承認後に契約作成

## 注意事項
- 見積はあくまで概算。正式契約時に審査が入ることを顧客に伝える。
- 車齢 10年超の場合は割増係数を適用。
