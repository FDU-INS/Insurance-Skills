---
name: life-insurance-recommendation
description: 顧客のライフステージ・年収・既存契約に基づき、最適な生命保険プランを提案する。
---

# Skill: life_insurance_recommendation

## 目的
顧客のライフステージ・家族構成・年収・既契約をもとに最適な生命保険プランを提案する。

## エージェントが使う判断ルール
- `scripts/recommend.py` を呼び出し候補プランを取得する
- RECOMMENDATION_RULES.md のライフステージ基準に従ってプランを絞り込む
- 既契約の保障とのギャップを分析して「足りている保障」「不足している保障」を明示する
- 最大3プランを月額保険料・保障内容・推奨理由とともに提示する
- 複数プランを提示する場合は必ず以下のテーブル形式で出力する:

| プラン | 月額保険料 | 保障内容 | 推奨理由 |
|---|---|---|---|
| {商品名} | {金額}円 | {保障の概要} | {推奨理由} |

## 業務上の暗黙知
- 解約を申し出た場合はまず「保障見直し」の可能性を探る
- 家族が増えた、住宅購入した等のライフイベントは提案の好機
- 医療保険は「先進医療特約」の重要性を必ず説明する

## 使用するスクリプト
- `scripts/recommend.py` — 条件に合うプラン一覧の取得
  - `customer_id` があれば `--customer_id C016` のみで呼べる（age/annual_income は自動取得）
  - 例: `{"customer_id": "C016"}`

## 使用するデータ
- `demo_app/data/products.csv`
- `demo_app/data/contracts.csv`
- `references/RECOMMENDATION_RULES.md`
