---
name: insurance-underwriting-claims
description: ウェアラブルやドライブレコーダーのデータから個人のリスクを瞬時に算定し、保険料の決定と支払いを自動化するスキル。
version: 2.0.0
author: SBI Orchestrator
---
# insurance-underwriting-claims (InsurTech Core)

## 1. Overview
保険ビジネスを「事後処理型」から「データ駆動型」へと変革するスキルです。
IoTデータを用いた動的なリスク評価（アンダーライティング）と、スマートコントラクトによる即時支払い（保険金請求）を実現します。

## 2. Capabilities & Routing
| Intent | Agent | Strategy |
| :--- | :--- | :--- |
| 保険金支払い自動判定 | **Claim Settlement Bot** | 事故データや公的証明書と照合し、人手を介さずに支払いを承認。 |
| ダイナミック・アンダーライティング | **Underwriting Engine** | リアルタイムのリスクデータに基づき、個別に最適化された保険料を算出。 |

## 3. Workflow
1. **Monitor**: `Underwriting Engine` がテレマティクスデータを監視し、安全運転なら保険料を割引。
2. **Detect**: 事故や災害の発生を検知。
3.  **Verify**: `Claim Settlement Bot` が、提出された証拠（写真、GPS）の真正性を検証。
4.  **Pay**: 条件を満たせば、銀行API経由で即時送金。

## 4. Operational Principles
*   **Fairness**: AIの判定ロジックに差別的なバイアスが含まれないよう監視する。
*   **Transparency**: 査定結果の理由（なぜ支払われないのか）を明確に説明する。
