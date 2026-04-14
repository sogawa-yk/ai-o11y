# 第15章 OTel Collectorの設定 ― 仕様書

## 章の概要

**章の目的**: Collectorの設定ファイルを読めるようになり、Exporter追加等の変更を自分で行えるようになる。本書用Collectorを `aio11y-book` namespaceにデプロイして実体験する。

**目標ページ数**: 12p

**所属する部**: 第IV部 実践 ― 収集と可視化

## 前提知識

- 第6章（Collector概念）、第13章（アプリ側の実装）

## 節の構成

### 15.1 設定ファイルの全体構造（再訪）

**概要**: receivers／processors／exporters／service の4セクションを、実際のYAMLを開いて解説する。

**図表**:
- リスト15.1: `collector-config/ch15-add-langfuse/config.yaml` の全体

**キーポイント**:
- コンポーネントの名前指定とインスタンス化
- `service.pipelines` でのつなぎ合わせ

### 15.2 よく使うReceiver・Processor・Exporter

**概要**: 本書で必要となる主要コンポーネントの設定パターンを一覧で示す。

**図表**:
- 表15.1: 主要コンポーネントの設定パターン一覧

**キーポイント**:
- Receiver: otlp (gRPC/HTTP)
- Processor: batch、memory_limiter、attributes
- Exporter: otlp（Gateway転送）、otlphttp（Langfuse等）、prometheusremotewrite、loki

### 15.3 本書用Collectorのデプロイ

**概要**: `aio11y-book` namespaceに本書用Collectorをデプロイし、サンプルアプリの送信先を切り替える。

**図表**:
- 図15.1: 本書用Collectorをデプロイした構成（travel-helper-ch15 → ch15-collector.aio11y-book → Gateway / Langfuse）
- リスト15.2: `collector-config/deploy/collector-deployment.yaml`

**キーポイント**:
- 共有Collectorは変更しない方針
- 本書用Collectorは `aio11y-book` 内でのみ動作
- ConfigMapで設定管理

### 15.4 実践: Langfuse Exporterの追加

**概要**: Langfuse向けOTLPエクスポートを `traces` パイプラインに追加する手順を示す。

**図表**:
- 図15.2: 追加前後のパイプライン変化
- リスト15.3: `ch15-add-langfuse/config.yaml` の差分（diff表示）

**キーポイント**:
- 既存パイプラインを壊さない追加方法
- Langfuse OTLPエンドポイント指定
- 認証情報（Basic Auth）をSecret経由で注入

### 15.5 変更の反映と動作確認

**概要**: Collector再起動・動作確認の手順を示す。

**図表**:
- 図15.3: 変更反映フロー（ConfigMap更新 → Rollout restart → 疎通確認）

**キーポイント**:
- `kubectl rollout restart` で安全に反映
- サンプルアプリのログとCollectorメトリクスで疎通確認
- Langfuse WebでOTLP経由のトレース到着確認
- `make clean-ch15` の掃除手順

## 図表リスト

| 図表番号 | タイトル | 種類 | 所属する節 |
|---------|---------|------|----------|
| リスト15.1 | ch15 config.yaml全体 | YAML | 15.1 |
| 表15.1 | 主要コンポーネント | 表 | 15.2 |
| 図15.1 | 本書用Collector構成 | 構造図 | 15.3 |
| リスト15.2 | Deploymentマニフェスト | YAML | 15.3 |
| 図15.2 | パイプライン変化 | フロー図 | 15.4 |
| リスト15.3 | 設定追加diff | YAML | 15.4 |
| 図15.3 | 変更反映フロー | フロー図 | 15.5 |

## コード例

| リスト | 内容 | 言語 | 所属する節 |
|-------|------|------|----------|
| リスト15.1 | `collector-config/ch15-add-langfuse/config.yaml` | YAML | 15.1 |
| リスト15.2 | Collector Deployment | YAML | 15.3 |
| リスト15.3 | Langfuse Exporter追加差分 | YAML（diff） | 15.4 |

## サンプルコード要件

- **種別**: Collector設定＋k8s
- **場所**: `collector-config/ch15-add-langfuse/`、`collector-config/deploy/`、`sample-app/ch15/`
- **機能**:
  - `aio11y-book` namespaceに本書用Collectorをデプロイ
  - サンプルアプリ（ch14同等）の送信先を本書用Collectorに変更
  - 本書用Collectorから既存Gateway＋LangfuseへExport
- **verify**: Tempo・Langfuse Webで両方にトレース到着

## 章末の理解度チェック問題

### 問題の方針
- 問題数: 4問
- 種類: 概念の確認1問、判断問題1問、設計問題2問

### 問題案
1. Collector設定の4セクションを挙げ、それぞれの役割を述べよ。（概念の確認）
2. 既存の共有Collectorを直接変更せず、本書用Collectorを別途立てた理由は何か。（判断問題）
3. 特定のAttributeをログから削除したい場合、どのProcessorをどう設定するか。（設計問題）
4. LangfuseへのOTLP送信に認証が必要な場合、SecretをCollectorにどう注入するか。（設計問題）

## 章間の接続

### 前の章からの接続
- **前章の最後**: アプリ側計装完成
- **この章の導入**: 「Collectorに手を入れる。本書用を立ててExporterを追加」
- **接続のキーフレーズ**: 「Collectorに手を入れる」

### 次の章への接続
- **この章の結び**: データは揃った。次は活用側、Grafanaでの可視化を扱う
- **次章への橋渡し**: 「Grafanaで何ができるか」
- **接続のキーフレーズ**: 「データを活かす」
