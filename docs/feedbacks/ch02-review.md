# 第2章 レビュー結果

## 構成・文体レビュー（chapter-reviewer）
総合 4.5/5。仕様整合・図表・章間接続は良好。
- 中: 「計装（Instrumentation）」の本文初出時に日本語（英語）併記がない（図中のみ）
- 低: 2.6節「関心事A／B」の既出明示はあるが補強可

## 技術検証レビュー（tech-verifier）
重要指摘:
- **要修正**: 「Langfuse SDKはOTLP経路ではない」という断定は不正確。Langfuse Python SDK v3（2025年5月）以降はOTelベースで、Langfuseの`/api/public/otel`にOTLP/HTTPで送信する。表2.1の「Langfuse独自API」記載と本文断定を見直す。
- **要確認**: 「40を超えるLLM SDKやベクトル検索ライブラリ」の数値根拠。Traceloop公式ページに具体的な数値の裏付けが弱い。「多数の」へ緩和、または出典を具体的integrationページに差し替え推奨。
- 正確: OTel Collectorパイプライン構造、3シグナル独立、Grafanaの非保存性、Tempo/Loki/Prometheusの位置付け。

## 情報ソース検証（citation-verifier）
- 2.3節Collectorパイプライン記述に脚注なし → `[^4]` でCollector公式アーキテクチャURLを参照すべき（参考文献には既掲載）
- [^1]と「40を超える」の整合改善
- [^2]とLangfuse断定の整合改善（上記と同じ問題）

## 理解度チェック問題フォーマット検証（quiz-format-checker）
- 第1章ベースラインに完全準拠。修正不要。

## Mermaid構文検証（mermaid-syntax-checker）
- 構文エラー0件、配色ルール準拠。修正不要。

---

## 対応結果
- **対応日**: 2026-04-14
- **修正内容**:
  1. 2.1節初出箇所で「計装（Instrumentation）」の併記を追加
  2. 2.2節の「OpenLLMetry」の記述から「40を超える」を「多数の」に緩和し、脚注URLを具体的なintegrations introductionページに差し替え
  3. 2.2節・2.4節のLangfuse SDK記述を「現行のSDK（v3以降）はOTel上に構築されOTLP/HTTPでLangfuseに直接送信する」と事実に整合する形に修正。表2.1の送信先欄も更新
  4. 2.3節Collectorパイプライン記述に脚注[^4]を追加
  5. Q2の解説をLangfuse SDK送信経路の事実に合わせて更新
