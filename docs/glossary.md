# 用語集 (Glossary)

**更新日**: 2026-04-14

## 凡例

- **表記**: 本書での統一表記
- **英語**: 英語表記（初出時に併記）
- **定義**: 本書における定義
- **初出**: 最初に登場する章

---

## Observability全般

### Observability（オブザーバビリティ）
**定義**: システム内部で何が起きているかを、外部から観測可能なデータ（ログ・メトリクス・トレース等）を通じて推測・診断できる性質。本書ではAIエージェントの「判断」も観測対象に含める。
**初出**: 第1章

### 3シグナル（Three Signals）
**定義**: OpenTelemetryが扱うデータ種別。Traces、Metrics、Logsの総称。
**初出**: 第5章

### 計装（Instrumentation）
**定義**: アプリケーションコードから観測データ（Span、Metric、Log）を生成するための仕組み・コード。本書では手動計装と自動計装の2種を区別する。
**初出**: 第2章

### 手動計装（Manual Instrumentation）
**定義**: 開発者がコードに明示的にSpan生成やMetric記録のロジックを書き込む計装方式。
**初出**: 第7章

### 自動計装（Auto Instrumentation）
**定義**: ライブラリのメソッドにモンキーパッチを当て、呼び出しを自動的にSpan等に変換する計装方式。
**初出**: 第7章

### Context Propagation（コンテキスト伝播）
**定義**: Trace IDやSpan IDをプロセス境界・サービス境界を越えて伝える仕組み。本書ではW3C Trace Context形式を基本とする。
**初出**: 第4章

### サンプリング（Sampling）
**定義**: 全てのトレースではなく一部のみを記録するための選別処理。
**初出**: 第6章

## OpenTelemetry関連

### OpenTelemetry（OTel）
**定義**: ベンダーニュートラルな観測データ（Traces、Metrics、Logs）の生成・収集・エクスポートの標準仕様およびSDK群を提供するCNCFプロジェクト。2019年にOpenTracingとOpenCensusが統合して誕生。
**初出**: 第1章

### OTLP（OpenTelemetry Protocol）
**定義**: OpenTelemetryが定義するデータ転送プロトコル。gRPCとHTTPの2方式がある。
**初出**: 第4章

### OpenTracing
**定義**: 分散トレーシングの計装APIを標準化したCNCFプロジェクト（2016年〜）。2019年にOpenCensusと統合されOpenTelemetryとなった。
**初出**: 第3章

### OpenCensus
**定義**: Google主導で開発された観測データの計装ライブラリ。2019年にOpenTracingと統合されOpenTelemetryとなった。
**初出**: 第3章

### Trace（トレース）
**定義**: 1つのリクエスト処理の全体像を表す、Spanの集合。同一のTrace IDを共有する。
**初出**: 第4章

### Span（スパン）
**定義**: ある処理区間を表す単位。開始時刻・終了時刻・名前・Attribute・親子関係を持つ。
**初出**: 第4章

### Attribute（属性）
**定義**: SpanやMetricに付与するキー・バリュー形式のメタデータ。
**初出**: 第4章

### SpanContext
**定義**: Trace IDとSpan IDのペア。「今どのTraceのどのSpanにいるか」を表す識別子。
**初出**: 第4章

### Event（イベント）
**定義**: Span内の特定の瞬間を記録する仕組み。OTel GenAI Semantic Conventionsではプロンプト／レスポンス記録に用いられる。
**初出**: 第4章

### Metric（メトリクス）
**定義**: 時系列の集計データ。Counter、Histogram、Gaugeの型がある。
**初出**: 第5章

### Counter（カウンタ）
**定義**: 累積値を記録するMetric型。リクエスト数・エラー数等に使う。
**初出**: 第5章

### Histogram（ヒストグラム）
**定義**: 値の分布を記録するMetric型。レイテンシ・レスポンスサイズ等に使う。
**初出**: 第5章

### Gauge（ゲージ）
**定義**: 現在値を記録するMetric型。キュー長・接続数等に使う。
**初出**: 第5章

### Log（ログ）
**定義**: イベント単位のテキストデータ。OTelではSpanContextと紐付けられる。
**初出**: 第5章

### TracerProvider
**定義**: Tracerのファクトリ。OTel SDKの初期化時に構成される。
**初出**: 第13章

### MeterProvider
**定義**: Meterのファクトリ。Metricの初期化時に構成される。
**初出**: 第13章

### GenAI Semantic Conventions
**定義**: OTelプロジェクトのGenAI SIGが策定する、LLM計装向けの標準Attribute命名・構造。`gen_ai.request.model` 等のキーを定義する。執筆時点でexperimental。
**初出**: 第8章

### W3C Trace Context
**定義**: HTTP通信上でTrace ID・Span IDを伝播するためのW3C標準仕様。`traceparent` `tracestate` ヘッダを定義する。
**初出**: 第4章

## OTel Collector関連

### OTel Collector
**定義**: 観測データを受信・加工・転送するベンダーニュートラルな中継点。ReceiversーProcessorsーExportersの3段パイプラインで構成される。
**初出**: 第2章

### Receiver（レシーバ）
**定義**: Collectorのデータ受信コンポーネント。OTLP、Prometheus等の形式をサポートする。
**初出**: 第6章

### Processor（プロセッサ）
**定義**: Collectorの中間処理コンポーネント。バッチ化、Attribute操作、サンプリング等を行う。
**初出**: 第6章

### Exporter（エクスポータ）
**定義**: Collectorのデータ送信コンポーネント。Tempo、Prometheus、Loki、Langfuse等の送信先に対応する。
**初出**: 第6章

### Pipeline（パイプライン）
**定義**: Receiver→Processor→Exporterの処理経路。traces／metrics／logsで独立に構成する。
**初出**: 第6章

## LLM Observability関連

### AIエージェント（AI Agent）
**定義**: LLMを中核に、ツール選択・ルーティング等の「判断」を行いながらタスクを遂行するソフトウェア。本書では複数エージェントの協調動作も扱う。
**初出**: 第1章

### LLM Observability
**定義**: LLM呼び出しの入出力・判断品質・コストを観測・評価する実践領域。OTel中心のシステム観測と区別する。
**初出**: 第1章

### OpenLLMetry
**定義**: Traceloop社が開発する、LLM SDK呼び出しを自動的にOTel Spanに変換するOSSライブラリ群。40以上のSDKをサポート。
**初出**: 第2章

### Traceloop
**定義**: OpenLLMetryを開発・メンテナンスする企業。計装コードのOTel本体への寄贈を進めている。
**初出**: 第8章

### Langfuse
**定義**: LLMアプリケーションのトレーシング、評価（Evaluation）、プロンプト管理を提供するLLM Observability特化プラットフォーム。
**初出**: 第2章

### Evaluation（評価）
**定義**: LLMの出力品質にスコアを付ける仕組み。人手レビューとLLM-as-judgeの両方式がある。
**初出**: 第11章

### LLM-as-judge
**定義**: 別のLLMに出力品質を評価させる自動評価手法。
**初出**: 第11章

### プロンプト管理（Prompt Management）
**定義**: プロンプトのバージョン管理と、バージョン間の出力品質比較を行う仕組み。Langfuseの主要機能。
**初出**: 第11章

### trace_id紐付け
**定義**: OTelのTrace IDをLangfuseのトレースにメタデータとして渡し、システム観測とLLM品質観測を横断デバッグ可能にする手法。
**初出**: 第12章

## LLMプラットフォーム関連

### OCI Generative AI Service
**定義**: Oracle Cloud Infrastructureが提供する生成AIサービス。OpenAI SDK互換のエンドポイントを提供する。
**初出**: 第1章

### Responses API
**定義**: OCI GenAIが提供する、内部でツール呼び出しやオーケストレーションを行うAPI。OpenAI SDK互換のインターフェースを持つ。
**初出**: 第10章

### Chat Completions API
**定義**: OpenAI互換のチャット補完API。単発のプロンプトに対する応答を返す基本的なインターフェース。
**初出**: 第10章

### OpenAI SDK
**定義**: OpenAIが提供するクライアントSDK。base_urlを変更することでOpenAI互換の他バックエンドにも接続可能。
**初出**: 第10章

## データストア・可視化関連

### Prometheus（プロメテウス）
**定義**: メトリクス時系列データベース。本書ではメトリクスの保存先として扱い、内部構造は扱わない。
**初出**: 第2章

### Tempo（テンポ）
**定義**: Grafana Labs開発のトレースストア。本書ではトレースの保存先として扱う。
**初出**: 第2章

### Loki（ロキ）
**定義**: Grafana Labs開発のログストア。本書ではログの保存先として扱う。
**初出**: 第2章

### Grafana（グラファナ）
**定義**: 複数データソース（Prometheus／Tempo／Loki等）に対する可視化・ダッシュボードUIを提供するOSS。
**初出**: 第2章

### データソース（Data Source）
**定義**: Grafanaが参照するバックエンド。Grafanaはクエリを投げて結果を表示するのみで、データ自体は保持しない。
**初出**: 第16章

### PromQL
**定義**: Prometheusのクエリ言語。メトリクスの集計・レート計算等を記述する。
**初出**: 第16章

### TraceQL
**定義**: Tempoのクエリ言語。Span属性・時間・サービス名等によるトレース検索を記述する。
**初出**: 第16章

### LogQL
**定義**: Lokiのクエリ言語。ラベルとパターンによるログ検索・集計を記述する。
**初出**: 第16章

### ダッシュボード（Dashboard）
**定義**: Grafanaのパネル集合。複数のクエリ結果をまとめて表示する単位。
**初出**: 第16章

### パネル（Panel）
**定義**: Grafanaダッシュボード上の1つの可視化単位。単一クエリの結果を折れ線・棒・ゲージ等で表示する。
**初出**: 第16章

## 実行基盤関連

### Kubernetes
**定義**: コンテナオーケストレーションプラットフォーム。本書ではサンプルアプリの実行基盤として前提とする。
**初出**: 第2章

### OKE（Oracle Kubernetes Engine）
**定義**: Oracle Cloud InfrastructureのマネージドKubernetesサービス。
**初出**: 第2章

### Namespace（名前空間）
**定義**: Kubernetesのリソース分離単位。本書のサンプルは全て `aio11y-book` namespace に配置する。
**初出**: 第13章

### DaemonSet
**定義**: Kubernetesで全ノードに1つずつPodを配置するワークロード。本書ではOTel Logs Collectorがこの形式で動作する。
**初出**: 第6章

## 一般技術用語

### gRPC
**定義**: HTTP/2ベースのRPCフレームワーク。OTLPのデフォルト転送プロトコル。
**初出**: 第6章

### OTLP/gRPC
**定義**: OTLPのgRPC実装。デフォルトポートは4317。
**初出**: 第6章

### OTLP/HTTP
**定義**: OTLPのHTTP実装。デフォルトポートは4318。
**初出**: 第6章

### モンキーパッチ（Monkey Patching）
**定義**: 実行時にライブラリのメソッドを差し替える技法。自動計装の基本メカニズム。
**初出**: 第7章

### デコレータ（Decorator）
**定義**: Python関数にメタ情報や前後処理を付与する構文。OpenLLMetryでは `@workflow` `@task` `@agent` として提供される。
**初出**: 第9章

### 分散トレーシング（Distributed Tracing）
**定義**: 複数サービスをまたぐリクエスト処理を1つのTraceとして追跡する手法。
**初出**: 第1章

### SDK（Software Development Kit）
**定義**: 特定のプラットフォーム・APIを利用するための開発ツール群。
**初出**: 第4章

### CNCF（Cloud Native Computing Foundation）
**定義**: クラウドネイティブ技術の標準化・普及を推進する非営利団体。OTelやKubernetesをホストする。
**初出**: 第3章

---

## 索引（五十音順）

### あ行
- [AIエージェント](#aiエージェントai-agent)
- [Attribute（属性）](#attribute属性)
- [Event（イベント）](#eventイベント)
- [Exporter（エクスポータ）](#exporterエクスポータ)
- [OCI Generative AI Service](#oci-generative-ai-service)
- [OKE](#okeoracle-kubernetes-engine)
- [OpenAI SDK](#openai-sdk)
- [OpenCensus](#opencensus)
- [OpenLLMetry](#openllmetry)
- [OpenTelemetry](#opentelemetryotel)
- [OpenTracing](#opentracing)
- [OTLP](#otlpopentelemetry-protocol)
- [OTel Collector](#otel-collector)
- [Observability](#observabilityオブザーバビリティ)

### か行
- [Gauge（ゲージ）](#gaugeゲージ)
- [Chat Completions API](#chat-completions-api)
- [計装](#計装instrumentation)
- [Context Propagation](#context-propagationコンテキスト伝播)
- [Counter（カウンタ）](#counterカウンタ)
- [gRPC](#grpc)
- [GenAI Semantic Conventions](#genai-semantic-conventions)
- [Grafana](#grafanaグラファナ)
- [CNCF](#cnccloud-native-computing-foundation)

### さ行
- [3シグナル](#3シグナルthree-signals)
- [サンプリング](#サンプリングsampling)
- [自動計装](#自動計装auto-instrumentation)
- [手動計装](#手動計装manual-instrumentation)
- [Span](#spanスパン)
- [SpanContext](#spancontext)
- [SDK](#sdksoftware-development-kit)

### た行
- [DaemonSet](#daemonset)
- [ダッシュボード](#ダッシュボードdashboard)
- [データソース](#データソースdata-source)
- [デコレータ](#デコレータdecorator)
- [Tempo](#tempoテンポ)
- [TracerProvider](#tracerprovider)
- [Trace](#traceトレース)
- [trace_id紐付け](#trace_id紐付け)
- [TraceQL](#traceql)

### な行
- [Namespace](#namespace名前空間)

### は行
- [パイプライン](#pipelineパイプライン)
- [パネル](#パネルpanel)
- [Histogram](#histogramヒストグラム)
- [評価](#evaluation評価)
- [プロンプト管理](#プロンプト管理prompt-management)
- [分散トレーシング](#分散トレーシングdistributed-tracing)
- [Prometheus](#prometheusプロメテウス)
- [PromQL](#promql)
- [Processor](#processorプロセッサ)

### ま行
- [MeterProvider](#meterprovider)
- [Metric](#metricメトリクス)
- [モンキーパッチ](#モンキーパッチmonkey-patching)

### や行

### ら行
- [Langfuse](#langfuse)
- [LLM Observability](#llm-observability)
- [LLM-as-judge](#llm-as-judge)
- [Receiver](#receiverレシーバ)
- [Responses API](#responses-api)
- [LogQL](#logql)
- [Log](#logログ)
- [Loki](#lokiロキ)

### わ行
- [W3C Trace Context](#w3c-trace-context)

### A-Z
- Attribute / Chat Completions API / Context Propagation / Counter / CNCF / DaemonSet / Event / Evaluation / Exporter / Gauge / GenAI Semantic Conventions / Grafana / gRPC / Histogram / Kubernetes / Langfuse / LLM-as-judge / LLM Observability / Log / Loki / LogQL / MeterProvider / Metric / Namespace / Observability / OCI GenAI Service / OKE / OpenAI SDK / OpenCensus / OpenLLMetry / OpenTelemetry / OpenTracing / OTel Collector / OTLP / Pipeline / Prometheus / PromQL / Processor / Receiver / Responses API / SDK / Span / SpanContext / Tempo / Trace / TracerProvider / TraceQL / Traceloop / W3C Trace Context
