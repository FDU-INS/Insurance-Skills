---
name: life-insurance-quote
description: 性別・健康状態に応じた保険料を算出し、生命保険の正式見積もりを作成する。
---

# life_insurance_quote

生命保険の正式見積書を作成するスキル。

## 概要
顧客の年齢・性別・健康状態・希望商品をもとに生命保険の月額保険料・補償内容・特約を含む詳細見積書を生成する。

## 入力パラメータ
- `customer_id` (str): 顧客ID
- `product_id` (str): 対象商品ID（例: P006〜P010）
- `gender` (str): 性別（男性 / 女性）
- `health_status` (str): 健康状態（良好 / 注意 / 要観察）

## 出力
- `quote_id`: 見積番号
- `product_name`: 商品名
- `monthly_premium`: 月額保険料（円）
- `annual_premium`: 年額保険料（円）
- `coverage_details`: 補償詳細
- `valid_until`: 見積有効期限
- `notes`: 注意事項

## 使用スクリプト
- `scripts/quote.py`

## 関連スキル
- `life_insurance_recommendation`: 商品選定時に先行して実行
- `life_insurance_contract_create`: 見積承認後に契約作成

## 注意事項
- 人によって健康状態の割増が発生することがある。
- 保険料告知義務について必ず案内すること。
