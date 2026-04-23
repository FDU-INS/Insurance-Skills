---
name: auto-insurance-contract-cancel
description: 既存の自動車保険契約を解約し、contracts.csv を更新する。
---

# Skill: auto_insurance_contract_cancel

## 目的
顧客の自動車保険契約を解約（契約ステータスを「解約」に更新）する。

## エージェントが使う判断ルール
- 解約前に必ず解約理由をヒアリングする（引越し・売却・乗り換えなど）
- 解約理由によっては「見直し」や「更新」を代替案として提示する
- 解約確認は2回行う（お客様に口頭で最終確認）
- 解約後は **`load_skill("activity-log-writer")` を実行してスキルを読み込んだうえで** `scripts/write_activity.py` を呼び出し、解約内容と理由を活動履歴に記録する
  - `load_skill` を呼ばずに直接 `write_activity.py` を実行することは禁止

## 業務上の暗黙知
- 「車を売却した」→ 解約手続きを進める
- 「保険料が高い」→ エコノミープランへの変更を提案する
- 「他社に乗り換え」→ 乗り換え理由を確認し、必要なら価格競争力のあるプランを提示

## 使用するスクリプト
- `scripts/cancel_contract.py` — 契約ステータスの更新

## 使用するデータ
- `demo_app/data/contracts.csv`
