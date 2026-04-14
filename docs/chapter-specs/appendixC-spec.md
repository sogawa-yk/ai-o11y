# 付録C 用語集 ― 仕様書

## 章の概要

**章の目的**: `docs/glossary.md` の主要用語を本書の紙面に収録し、読者が本文読解中に即座に参照できるようにする。

**目標ページ数**: 4p

**所属する部**: 付録

## 前提知識

- なし（本書の全章で参照される）

## 節の構成

### C.1 Observability全般

**概要**: Observability／3シグナル／計装／Context Propagation／サンプリング等の基礎用語の定義。

**図表**:
- 表C.1: Observability全般用語

### C.2 OpenTelemetry関連

**概要**: OTel／OTLP／Trace／Span／Attribute／SpanContext／Event／Metric／GenAI Semantic Conventions等の定義。

**図表**:
- 表C.2: OpenTelemetry関連用語

### C.3 LLM Observability関連

**概要**: AIエージェント／OpenLLMetry／Langfuse／Evaluation／LLM-as-judge／trace_id紐付け等の定義。

**図表**:
- 表C.3: LLM Observability関連用語

### C.4 ツール・プラットフォーム関連

**概要**: OCI GenAI／OpenAI SDK／Prometheus／Loki／Tempo／Grafana／Langfuse／Kubernetes等の定義。

**図表**:
- 表C.4: ツール・プラットフォーム関連用語

## 図表リスト

| 図表番号 | タイトル | 種類 | 所属する節 |
|---------|---------|------|----------|
| 表C.1 | Observability全般用語 | 表 | C.1 |
| 表C.2 | OpenTelemetry関連用語 | 表 | C.2 |
| 表C.3 | LLM Observability関連用語 | 表 | C.3 |
| 表C.4 | ツール・プラットフォーム関連用語 | 表 | C.4 |

## コード例

コード例はない。

## サンプルコード要件

付録Cはサンプルコードを含まない。内容は `docs/glossary.md` からの抜粋で、定義・初出章・英語表記を併記する。

## 章末の理解度チェック問題

付録のため問題は設けない。

## 章間の接続

### 前の章からの接続
- **前章の最後**: 付録B（OTel Python SDK APIリファレンス）
- **この章の導入**: 「本書で使う用語の定義を本文と同じ紙面に収める」

### 次の章への接続
- **この章の結び**: 本書の最終頁。あとがき／参考文献総覧（書籍化時に追加）につなぐ
- **接続のキーフレーズ**: なし（最終章）
