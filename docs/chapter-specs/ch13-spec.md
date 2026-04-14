# 第13章 Python OTel SDKでの手動計装 ― 仕様書

## 章の概要

**章の目的**: Python OTel SDKで手動計装を書けるようになる。SDK初期化からSpan／Metric／Logの記録、Collectorへの送信までの一連の実装を身につける。

**目標ページ数**: 16p

**所属する部**: 第IV部 実践 ― 収集と可視化

## 前提知識

- 第4章（OTel概念）、第5章（3シグナル）、第7章（手動計装）
- Python実務経験

## 節の構成

### 13.1 SDK初期化の基本パターン

**概要**: TracerProvider／MeterProvider／LoggerProviderの初期化とOTLPエクスポータ設定を扱う。

**図表**:
- 図13.1: SDK初期化後のコンポーネント関係図
- リスト13.1: `sample-app/ch13/otel_setup.py` 初期化コード

**キーポイント**:
- Resource（`service.name`等）の設定
- BatchSpanProcessor／PeriodicExportingMetricReaderの役割
- OTLP/gRPCエンドポイント指定

### 13.2 Spanの作成と操作

**概要**: `start_as_current_span`、Attribute付与、Status設定、例外記録のパターンを示す。

**図表**:
- リスト13.2: `sample-app/ch13/agent.py` のSpan操作抜粋
- 図13.2: Span生成・Attribute・Status・Exception記録のフロー

**キーポイント**:
- `span.set_attribute()`、`span.set_status(Status(...))`、`span.record_exception()`
- エラー時の定型処理

### 13.3 Metricの記録

**概要**: Counter／Histogramの作成と記録を扱う。

**図表**:
- リスト13.3: Counter／Histogram記録
- 表13.1: メトリクス設計（本書サンプルで使う全Metricの一覧）

**キーポイント**:
- `meter.create_counter()` → `counter.add(value, attributes)`
- `meter.create_histogram()` → `histogram.record(value, attributes)`
- 共通Attributeの付与

### 13.4 Logの記録

**概要**: Python標準loggingとOTel Logs Instrumentationの組み合わせを示す。

**図表**:
- リスト13.4: loggingセットアップとSpanContext付きログ出力
- 図13.3: ログの流れ（logging→Handler→OTel→Loki）

**キーポイント**:
- `LoggingInstrumentor().instrument(set_logging_format=True)` で自動紐付け
- 構造化ログとの組み合わせ

### 13.5 エージェントの計装パターン

**概要**: `travel-helper` のplan／gather／synthesize 3stageを手動計装する完全版を提示する。

**図表**:
- 図13.4: 完全版Span木（handle_plan_request→3 stages→tool呼び出し）
- リスト13.5: handle_plan_request関数の完全コード

**キーポイント**:
- Span名・Attribute名の命名規則（`travel_helper.*`、`gen_ai.*`、`tool.*`）
- エラーハンドリングの統一パターン

### 13.6 ハンズオン ― 完全版をデプロイ

**概要**: `sample-app/ch13/` をデプロイし、Tempo/Prometheus/Lokiそれぞれでデータを確認する。

**図表**:
- 図13.5: 確認画面のイメージ（Tempoウォーターフォール、Prometheusグラフ、Lokiログ）

**キーポイント**:
- Tempoで階層Span確認
- Prometheusで新規Metric確認
- Lokiでtrace_id付きログ確認
- `make clean-ch13` の掃除手順

## 図表リスト

| 図表番号 | タイトル | 種類 | 所属する節 |
|---------|---------|------|----------|
| 図13.1 | SDK初期化後のコンポーネント関係 | 構造図 | 13.1 |
| リスト13.1 | otel_setup.py初期化 | Python | 13.1 |
| 図13.2 | Span操作フロー | フロー図 | 13.2 |
| リスト13.2 | Span操作抜粋 | Python | 13.2 |
| リスト13.3 | Metric記録 | Python | 13.3 |
| 表13.1 | 本書のMetric一覧 | 表 | 13.3 |
| リスト13.4 | loggingセットアップ | Python | 13.4 |
| 図13.3 | ログの流れ | フロー図 | 13.4 |
| 図13.4 | 完全版Span木 | 木構造図 | 13.5 |
| リスト13.5 | handle_plan_request完全版 | Python | 13.5 |
| 図13.5 | 確認画面イメージ | 画面図 | 13.6 |

## コード例

| リスト | 内容 | 言語 | 所属する節 |
|-------|------|------|----------|
| リスト13.1 | `sample-app/ch13/otel_setup.py` 初期化 | Python | 13.1 |
| リスト13.2 | `sample-app/ch13/agent.py` Span操作 | Python | 13.2 |
| リスト13.3 | `sample-app/ch13/agent.py` Metric | Python | 13.3 |
| リスト13.4 | `sample-app/ch13/agent.py` Log | Python | 13.4 |
| リスト13.5 | `sample-app/ch13/agent.py` ハンドラ完全版 | Python | 13.5 |

## サンプルコード要件

- **種別**: app（Python）＋k8s
- **場所**: `sample-app/ch13/`
- **機能**: `functional-design.md` の「最終形（ch13以降）」を完全実装。全stage・全Attribute・全Metric・全Log記録
- **verify**: Tempo／Prometheus／Lokiですべて観測確認

## 章末の理解度チェック問題

### 問題の方針
- 問題数: 4問
- 種類: 概念の確認1問、判断問題1問、設計問題2問

### 問題案
1. TracerProviderにResourceを設定する目的は何か。（概念の確認）
2. 例外発生時にSpanに対して行うべき定型処理を述べよ。（判断問題）
3. 新しい関数を計装するとき、どのような観点でSpan名を決めるか。（設計問題）
4. レイテンシを分布で記録したい。Counter／Histogramのどちらを使うか、理由とともにコード断片を示せ。（設計問題）

## 章間の接続

### 前の章からの接続
- **前章の最後**: OTel／Langfuse併用の設計判断
- **この章の導入**: 「第IV部に入る。まず手動計装の実装を完全に固める」
- **接続のキーフレーズ**: 「実装へ」

### 次の章への接続
- **この章の結び**: 手動計装が揃ったので、LLM呼び出し部分を自動計装（OpenLLMetry）で強化する
- **次章への橋渡し**: 「OpenLLMetryのセットアップと検証」
- **接続のキーフレーズ**: 「自動計装を加える」
