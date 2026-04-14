# 付録C 用語集

本付録は `docs/glossary.md` から主要用語を抽出して本文と同じ紙面に収録したものである。本文読解中に用語の定義を確認したいときに参照する。各表の「初出」列は本書内で用語が最初に登場する章を示す。

## C.1 Observability全般

*表C.1: Observability全般の用語*

| 用語（日本語） | 英語表記 | 定義 | 初出 |
|--------------|----------|------|------|
| Observability | Observability | システム内部で何が起きているかを、外部から観測可能なデータ（ログ・メトリクス・トレース等）を通じて推測・診断できる性質。本書ではAIエージェントの「判断」も観測対象に含める。 | 第1章 |
| 3シグナル | Three Signals | OpenTelemetryが扱うデータ種別。Traces、Metrics、Logsの総称。 | 第5章 |
| 計装 | Instrumentation | アプリケーションコードから観測データ（Span、Metric、Log）を生成するための仕組み・コード。手動計装と自動計装の2種を区別する。 | 第2章 |
| 手動計装 | Manual Instrumentation | 開発者がコードに明示的にSpan生成やMetric記録のロジックを書き込む計装方式。 | 第7章 |
| 自動計装 | Auto Instrumentation | ライブラリのメソッドにモンキーパッチを当て、呼び出しを自動的にSpan等に変換する計装方式。 | 第7章 |
| Context Propagation | Context Propagation | Trace IDやSpan IDをプロセス境界・サービス境界を越えて伝える仕組み。本書ではW3C Trace Context形式を基本とする。 | 第4章 |
| サンプリング | Sampling | 全てのトレースではなく一部のみを記録するための選別処理。 | 第6章 |
| 分散トレーシング | Distributed Tracing | 複数サービスをまたぐリクエスト処理を1つのTraceとして追跡する手法。 | 第1章 |

## C.2 OpenTelemetry関連

*表C.2: OpenTelemetry関連の用語*

| 用語 | 英語表記 | 定義 | 初出 |
|------|----------|------|------|
| OpenTelemetry（OTel） | OpenTelemetry | ベンダーニュートラルな観測データ（Traces、Metrics、Logs）の生成・収集・エクスポートの標準仕様およびSDK群を提供するCNCFプロジェクト。2019年にOpenTracingとOpenCensusが統合して誕生。 | 第1章 |
| OTLP | OpenTelemetry Protocol | OpenTelemetryが定義するデータ転送プロトコル。gRPCとHTTPの2方式がある（デフォルトポート 4317／4318）。 | 第4章 |
| OpenTracing | OpenTracing | 分散トレーシングの計装APIを標準化したCNCFプロジェクト（2016年〜）。2019年にOpenCensusと統合されOpenTelemetryとなった。 | 第3章 |
| OpenCensus | OpenCensus | Google主導で開発された観測データの計装ライブラリ。2019年にOpenTracingと統合されOpenTelemetryとなった。 | 第3章 |
| Trace | Trace | 1つのリクエスト処理の全体像を表す、Spanの集合。同一のTrace IDを共有する。 | 第4章 |
| Span | Span | ある処理区間を表す単位。開始時刻・終了時刻・名前・Attribute・親子関係を持つ。 | 第4章 |
| Attribute | Attribute | SpanやMetricに付与するキー・バリュー形式のメタデータ。 | 第4章 |
| SpanContext | SpanContext | Trace IDとSpan IDのペア。「今どのTraceのどのSpanにいるか」を表す識別子。 | 第4章 |
| Event | Event | Span内の特定の瞬間を記録する仕組み。 | 第4章 |
| Metric | Metric | 時系列の集計データ。Counter、Histogram、Gaugeの型がある。 | 第5章 |
| Counter | Counter | 累積値を記録するMetric型。リクエスト数・エラー数等に使う。 | 第5章 |
| Histogram | Histogram | 値の分布を記録するMetric型。レイテンシ・レスポンスサイズ等に使う。 | 第5章 |
| Gauge | Gauge | 現在値を記録するMetric型。キュー長・接続数等に使う。 | 第5章 |
| Log | Log | イベント単位のテキストデータ。OTelではSpanContextと紐付けられる。 | 第5章 |
| TracerProvider | TracerProvider | Tracerのファクトリ。OTel SDKの初期化時に構成される。 | 第13章 |
| MeterProvider | MeterProvider | Meterのファクトリ。Metricの初期化時に構成される。 | 第13章 |
| GenAI Semantic Conventions | GenAI Semantic Conventions | OTelプロジェクトのGen AI SIGが策定する、LLM計装向けの標準Attribute命名・構造。`gen_ai.request.model` 等のキーを定義する。執筆時点でexperimental／development。 | 第8章 |
| W3C Trace Context | W3C Trace Context | HTTP通信上でTrace ID・Span IDを伝播するためのW3C標準仕様。`traceparent` `tracestate` ヘッダを定義する。 | 第4章 |
| OTel Collector | OTel Collector | 観測データを受信・加工・転送するベンダーニュートラルな中継点。ReceiversーProcessorsーExportersの3段パイプラインで構成される。 | 第2章 |
| Receiver | Receiver | Collectorのデータ受信コンポーネント。OTLP、Prometheus等の形式をサポートする。 | 第6章 |
| Processor | Processor | Collectorの中間処理コンポーネント。バッチ化、Attribute操作、サンプリング等を行う。 | 第6章 |
| Exporter | Exporter | Collectorのデータ送信コンポーネント。Tempo、Prometheus、Loki、Langfuse等の送信先に対応する。 | 第6章 |
| Pipeline | Pipeline | Receiver→Processor→Exporterの処理経路。traces／metrics／logsで独立に構成する。 | 第6章 |

## C.3 LLM Observability関連

*表C.3: LLM Observability関連の用語*

| 用語 | 英語表記 | 定義 | 初出 |
|------|----------|------|------|
| AIエージェント | AI Agent | LLMを中核に、ツール選択・ルーティング等の「判断」を行いながらタスクを遂行するソフトウェア。本書では複数エージェントの協調動作も扱う。 | 第1章 |
| LLM Observability | LLM Observability | LLM呼び出しの入出力・判断品質・コストを観測・評価する実践領域。OTel中心のシステム観測と区別する。 | 第1章 |
| OpenLLMetry | OpenLLMetry | Traceloop社が開発する、LLM SDK呼び出しを自動的にOTel Spanに変換するOSSライブラリ群。多数のSDKをサポート。 | 第2章 |
| Traceloop | Traceloop | OpenLLMetryを開発・メンテナンスする企業。計装コードのOTel本体への寄贈を進めている。 | 第8章 |
| Langfuse | Langfuse | LLMアプリケーションのトレーシング、評価（Evaluation）、プロンプト管理を提供するLLM Observability特化プラットフォーム。 | 第2章 |
| Evaluation | Evaluation | LLMの出力品質にスコアを付ける仕組み。人手レビューとLLM-as-judgeの両方式がある。 | 第11章 |
| LLM-as-judge | LLM-as-judge | 別のLLMに出力品質を評価させる自動評価手法。 | 第11章 |
| プロンプト管理 | Prompt Management | プロンプトのバージョン管理と、バージョン間の出力品質比較を行う仕組み。Langfuseの主要機能。 | 第11章 |
| trace_id紐付け | trace_id linking | OTelのTrace IDをLangfuseのトレースにメタデータとして渡し、システム観測とLLM品質観測を横断デバッグ可能にする手法。 | 第12章 |

## C.4 ツール・プラットフォーム関連

*表C.4: ツール・プラットフォーム関連の用語*

| 用語 | 英語表記 | 定義 | 初出 |
|------|----------|------|------|
| OCI Generative AI Service | OCI GenAI Service | Oracle Cloud Infrastructureが提供する生成AIサービス。OpenAI SDK互換のエンドポイントを提供する。 | 第1章 |
| Chat Completions API | Chat Completions API | OpenAI互換のチャット補完API。単発のプロンプトに対する応答を返す基本的なインターフェース。 | 第10章 |
| Responses API | Responses API | OCI GenAIが提供する、内部でツール呼び出しやオーケストレーションを行うAPI。OpenAI SDK互換のインターフェースを持つ。 | 第10章 |
| OpenAI SDK | OpenAI SDK | OpenAIが提供するクライアントSDK。base_urlを変更することでOpenAI互換の他バックエンドにも接続可能。 | 第10章 |
| Prometheus | Prometheus | メトリクス時系列データベース。本書ではメトリクスの保存先として扱う。 | 第2章 |
| Tempo | Tempo | Grafana Labs開発のトレースストア。本書ではトレースの保存先として扱う。 | 第2章 |
| Loki | Loki | Grafana Labs開発のログストア。本書ではログの保存先として扱う。 | 第2章 |
| Grafana | Grafana | 複数データソース（Prometheus／Tempo／Loki等）に対する可視化・ダッシュボードUIを提供するOSS。 | 第2章 |
| データソース | Data Source | Grafanaが参照するバックエンド。Grafanaはクエリを投げて結果を表示するのみで、データ自体は保持しない。 | 第16章 |
| PromQL | PromQL | Prometheusのクエリ言語。メトリクスの集計・レート計算等を記述する。 | 第16章 |
| TraceQL | TraceQL | Tempoのクエリ言語。Span属性・時間・サービス名等によるトレース検索を記述する。 | 第16章 |
| LogQL | LogQL | Lokiのクエリ言語。ラベルとパターンによるログ検索・集計を記述する。 | 第16章 |
| ダッシュボード | Dashboard | Grafanaのパネル集合。複数のクエリ結果をまとめて表示する単位。 | 第16章 |
| パネル | Panel | Grafanaダッシュボード上の1つの可視化単位。単一クエリの結果を折れ線・棒・ゲージ等で表示する。 | 第16章 |
| Kubernetes | Kubernetes | コンテナオーケストレーションプラットフォーム。本書ではサンプルアプリの実行基盤として前提とする。 | 第2章 |
| OKE | Oracle Kubernetes Engine | Oracle Cloud InfrastructureのマネージドKubernetesサービス。 | 第2章 |
| Namespace | Namespace | Kubernetesのリソース分離単位。本書のサンプルは全て `aio11y-book` namespace に配置する。 | 第13章 |
| DaemonSet | DaemonSet | Kubernetesで全ノードに1つずつPodを配置するワークロード。本書ではOTel Logs Collectorがこの形式で動作する。 | 第6章 |
| gRPC | gRPC | HTTP/2ベースのRPCフレームワーク。OTLPのデフォルト転送プロトコル。 | 第6章 |
| モンキーパッチ | Monkey Patching | 実行時にライブラリのメソッドを差し替える技法。自動計装の基本メカニズム。 | 第7章 |
| CNCF | Cloud Native Computing Foundation | クラウドネイティブ技術の標準化・普及を推進する非営利団体。OTelやKubernetesをホストする。 | 第3章 |

---

完全な用語集は `docs/glossary.md` を参照してほしい。本書で使う全ての専門用語と、日英対応・表記統一基準が網羅されている。

本書はここで終わる。ここまで読み進めてくれた読者に感謝を申し上げる。第1章で示した2つの関心事と、改善ループを回す道具立ては手元に揃った。あとは自分のエージェントと、自分の環境で、ループを1回ずつ回していくだけである。
