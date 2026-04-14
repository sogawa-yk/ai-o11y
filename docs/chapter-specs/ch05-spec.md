# 第5章 3つのシグナル ― Traces、Metrics、Logs ― 仕様書

## 章の概要

**章の目的**: OTelが扱う3つのデータ種別の用途と保存先を整理し、読者がどのシグナルを何に使うべきかを判断できるようになる。サンプルアプリで3シグナルすべてを流す状態を作る。

**目標ページ数**: 14p

**所属する部**: 第II部 OTelの概念と仕組み

## 前提知識

- 第4章（Spanの生成・Attribute・Context）

## 節の構成

### 5.1 Tracesの深掘り

**概要**: 第4章で扱ったTracesの使いどころを、個別リクエストの深掘りという観点で再確認する。

**図表**:
- 図5.1: Tracesの典型的な活用シナリオ（1リクエストのSpanウォーターフォール表示）

**キーポイント**:
- 用途: 個別リクエストの詳細追跡
- 保存先: Tempo
- エージェント開発で最頻用のシグナル

### 5.2 Metrics ― 集計データ

**概要**: Counter／Histogram／Gaugeの3型を導入し、それぞれの記録パターンと用途を示す。

**図表**:
- 表5.1: Metric3型の比較（累積・分布・現在値、典型的用途）
- 図5.2: Counter／Histogramのデータ構造の違い

**キーポイント**:
- Counter: 単調増加（リクエスト数等）
- Histogram: 値の分布（レイテンシ、トークン数）
- Gauge: 現在値（キュー長）
- 保存先はPrometheus

### 5.3 Logs ― イベント単位のデータ

**概要**: OTel Logsの特徴として、SpanContextとの自動紐付けに焦点を当てる。

**図表**:
- 図5.3: ログがSpanContextと紐付く仕組み（trace_id / span_idがログに自動付与される流れ）

**キーポイント**:
- 従来のログ基盤との違いはSpanContext紐付け
- Python標準loggingにOTel Logs Instrumentationを適用すると自動化できる
- 保存先はLoki

### 5.4 3シグナルの使い分け

**概要**: Metricsで異常検知→Tracesで個別リクエスト特定→Logsで詳細確認、という典型的なフローを提示する。

**図表**:
- 図5.4: 3シグナルの協調フロー（時系列の異常→該当TraceID→該当ログ）

**キーポイント**:
- 3シグナルは独立に存在するがtrace_idで連結できる
- エージェント開発での標準ワークフロー

### 5.5 ハンズオン ― 3シグナルを流す

**概要**: `sample-app/ch05/` でMetricsとLogsを追加し、3シグナルすべてをOTel Collectorへ送ってGrafanaで確認する。

**図表**:
- 図5.5: ハンズオン構成（Counter/Histogram/Log追加）
- リスト5.1: `sample-app/ch05/otel_setup.py` の初期化抜粋
- リスト5.2: `sample-app/ch05/agent.py` のMetric記録抜粋

**キーポイント**:
- PrometheusでCounter／Histogramが見える
- LokiでSpanContext付きログが見える
- 末尾に `make clean-ch05` の掃除手順

## 図表リスト

| 図表番号 | タイトル | 種類 | 所属する節 |
|---------|---------|------|----------|
| 図5.1 | Tracesの活用シナリオ | フロー図 | 5.1 |
| 表5.1 | Metric3型の比較 | 比較表 | 5.2 |
| 図5.2 | Counter／Histogramのデータ構造 | 構造図 | 5.2 |
| 図5.3 | ログとSpanContextの紐付け | フロー図 | 5.3 |
| 図5.4 | 3シグナルの協調フロー | フロー図 | 5.4 |
| 図5.5 | ハンズオン構成 | 構造図 | 5.5 |
| リスト5.1 | 3シグナル用OTel初期化 | Python | 5.5 |
| リスト5.2 | Metric記録コード | Python | 5.5 |

## コード例

| リスト | 内容 | 言語 | 所属する節 |
|-------|------|------|----------|
| リスト5.1 | TracerProvider／MeterProvider／LoggerProvider初期化 | Python | 5.5 |
| リスト5.2 | Metric（Counter/Histogram）記録 | Python | 5.5 |

## サンプルコード要件

- **種別**: app（Python）＋k8s
- **場所**: `sample-app/ch05/`
- **機能**:
  - ch04に加え `gather_stage`（簡易版：weather_toolのみ呼ぶ）を追加
  - Counter `travel_helper.requests`、Histogram `travel_helper.request.duration` を記録
  - Python標準loggingをOTel Logs Instrumentationで自動ログ送信
- **verify**: Tempo／Prometheus／Lokiそれぞれでデータが確認できる

## 章末の理解度チェック問題

### 問題の方針
- 問題数: 4問
- 種類: 概念の確認2問、判断問題1問、設計問題1問

### 問題案
1. Traces、Metrics、Logsの3シグナルそれぞれの用途を1文で説明せよ。（概念の確認）
2. OTel Logsが従来のログ基盤と異なる点を述べよ。（概念の確認）
3. 「ある時間帯のリクエストが平均より遅い」という傾向を発見した。次にどのシグナルを見るべきか、理由と共に答えよ。（判断問題）
4. LLM呼び出しのトークン使用量を可視化するため、MetricsとTracesのどちらでどう記録するかを設計せよ。（設計問題）

## 章間の接続

### 前の章からの接続
- **前章の最後**: Traceを作れるようになった
- **この章の導入**: 「同じOTelの枠組みでMetricsとLogsも扱える。3シグナルの全体像を押さえる」
- **接続のキーフレーズ**: 「3シグナルへ広げる」

### 次の章への接続
- **この章の結び**: 3シグナルを生成できるようになった。次はデータの中継点であるCollectorの内部を理解する
- **次章への橋渡し**: 「Collectorのパイプラインを読み解く」
- **接続のキーフレーズ**: 「データはどう中継されるか」
