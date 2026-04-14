# 第16章 レビュー結果

## 構成・文体（4.5/5）
- 低: リスト16.4の抜粋である旨を補足
- 低: gen_ai.*記述に第13章参照の1行補強

## 技術検証（8/10 正確）
- 要修正: Q4 TraceQL `| by(trace:duration) | limit 20` は意図通り動作しない → `| limit(20)` + UI側ソート
- 要修正: Q3 GenAI metric の Prometheus変換は `_seconds_bucket`（OTel GenAI規約のunit=秒）

## 情報ソース・理解度・Mermaid
- 修正不要

---

## 対応結果
- 対応日: 2026-04-14
- 修正:
  1. Q4 TraceQL解答例を `| limit(20)` に修正、ソートは「Grafana UI のTracesテーブル列ヘッダ」で行う旨を補足
  2. Q3 `gen_ai_client_operation_duration_bucket` → `gen_ai_client_operation_duration_seconds_bucket`
  3. リスト16.4直後に「残り2パネルは `sample-app/ch16/dashboards/baseline.json` 参照」の補足
