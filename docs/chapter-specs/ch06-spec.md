# 第6章 OTel Collector ― データの中継と変換 ― 仕様書

## 章の概要

**章の目的**: OTel Collectorの役割とパイプライン構造を理解し、設定ファイルを読めるようになる。次章以降でExporter追加等の変更ができる土台を作る。

**目標ページ数**: 14p

**所属する部**: 第II部 OTelの概念と仕組み

## 前提知識

- 第5章（3シグナル）
- YAMLの基本読み書き

## 節の構成

### 6.1 Collectorの役割

**概要**: アプリとバックエンドの間にCollectorを挟む意義を、第3章の「計装とバックエンドの分離」の延長で再確認する。

**図表**:
- 図6.1: Collectorを挟む構成と挟まない構成の比較

**キーポイント**:
- バッチ化・サンプリング・Attribute変換等をアプリから剥がせる
- バックエンド変更時の影響範囲が限定される

### 6.2 パイプラインの3段構成

**概要**: Receivers／Processors／Exportersの役割を順に説明する。

**図表**:
- 図6.2: 3段パイプラインの詳細（各段の入出力）

**キーポイント**:
- Receivers: データの受け口（OTLP gRPC/HTTPが基本）
- Processors: バッチ化、Attribute操作、サンプリング、memory_limiter等
- Exporters: 保存先への送信（Tempo/Prometheus/Loki/Langfuse等）

### 6.3 3シグナルそれぞれの独立パイプライン

**概要**: traces／metrics／logsが独立したパイプラインとして動作することを示し、設定ファイルの `service.pipelines` 節の構造を解説する。

**図表**:
- 図6.3: 3つのパイプラインの並列動作（同じReceiver／Processorを共有できるが、Exporterは通常異なる）

**キーポイント**:
- 同じReceiverを3パイプラインで共有することが多い
- Exporterはシグナル種別に応じて切り替わる

### 6.4 設定ファイルの読み方

**概要**: 実際の設定ファイル例を読み解く。receivers/processors/exporters/service の4セクション構成を理解する。

**図表**:
- リスト6.1: 典型的なCollector設定（`collector-config/ch06-baseline/config.yaml`）
- 表6.1: 主要な標準コンポーネント一覧（よく使うReceiver・Processor・Exporter）

**キーポイント**:
- 4セクションの役割
- コンポーネントは名前（`otlp`）とインスタンス（`otlp/customer1`）の区別
- `service.pipelines` で「どのreceiver→processor→exporterを組み合わせるか」を宣言

### 6.5 既存の共有Collectorを読む

**概要**: プロジェクト既存の `otel-gateway-opentelemetry-collector`（observability namespace）の設定を読み、どこから入ってどこに出ているかを図と共に確認する。

**図表**:
- 図6.4: 既存Collectorのパイプライン図（OTLP→batch→tempo/prometheusremotewrite/loki）

**キーポイント**:
- 既存Collectorは本書では変更しない（共有資産のため）
- 第15章で本書用Collectorを新規デプロイする

### 6.6 Exporter追加の考え方（概念のみ、実装は第15章）

**概要**: Langfuse等の新しいExporterを追加する一般的な流れを概念レベルで示す。実際の設定追加は第15章で行う。

**図表**:
- 図6.5: Exporter追加時のパイプライン変化イメージ

**キーポイント**:
- 既存Pipelineを壊さない追加方法
- 設定反映方法（Collector再起動／reload signal）

## 図表リスト

| 図表番号 | タイトル | 種類 | 所属する節 |
|---------|---------|------|----------|
| 図6.1 | Collectorあり／なしの比較 | 構造図 | 6.1 |
| 図6.2 | 3段パイプラインの詳細 | フロー図 | 6.2 |
| 図6.3 | 3パイプラインの並列動作 | フロー図 | 6.3 |
| リスト6.1 | 典型的なCollector設定 | YAML | 6.4 |
| 表6.1 | 主要コンポーネント一覧 | 表 | 6.4 |
| 図6.4 | 既存Collectorのパイプライン | フロー図 | 6.5 |
| 図6.5 | Exporter追加イメージ | フロー図 | 6.6 |

## コード例

| リスト | 内容 | 言語 | 所属する節 |
|-------|------|------|----------|
| リスト6.1 | ベースラインCollector設定（`collector-config/ch06-baseline/config.yaml`） | YAML | 6.4 |

## サンプルコード要件

- **種別**: Collector設定（デプロイは第15章で行うため、本章では設定ファイル配置のみ）
- **場所**: `collector-config/ch06-baseline/config.yaml`
- **機能**: Receiver（OTLP）→ Processor（batch、memory_limiter）→ Exporter（otlp/tempo、prometheusremotewrite、loki）の典型的な構成を記述
- **verify**: `otelcol --config` で構文チェック（syntaxチェックのみ、本章ではK8sデプロイは行わない）

## 章末の理解度チェック問題

### 問題の方針
- 問題数: 4問
- 種類: 概念の確認2問、判断問題1問、設計問題1問

### 問題案
1. Receivers／Processors／Exportersのそれぞれの役割を1文で述べよ。（概念の確認）
2. Collectorを挟まずアプリから直接バックエンドに送る場合の欠点を2つ挙げよ。（概念の確認）
3. アプリからのログ送信を増やしたがLokiのストレージが逼迫した。Collector側でどう対応するか、複数案から選べ。（判断問題）
4. Langfuseへもデータ送信を追加したい。設定ファイルのどこを編集するか、pipelineとexporterの追加内容を疑似YAMLで示せ。（設計問題）

## 章間の接続

### 前の章からの接続
- **前章の最後**: 3シグナルを生成できるようになった
- **この章の導入**: 「生成したデータをどう中継するか。Collectorの中身を見る」
- **接続のキーフレーズ**: 「データはどう中継されるか」

### 次の章への接続
- **この章の結び**: Collectorの役割を押さえたので、次はアプリ側の計装方式（自動と手動）の選択を扱う
- **次章への橋渡し**: 「自動計装と手動計装の使い分け」
- **接続のキーフレーズ**: 「何を自動に任せ、何を手動で書くか」
