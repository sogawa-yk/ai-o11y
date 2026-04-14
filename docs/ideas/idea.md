# AIエージェント開発のためのObservability実践ガイド

## 本書の概要

### 対象読者

- Kubernetes実務経験あり（OKE等でのデプロイ・運用経験）
- Pythonでのアプリケーション開発が可能
- LLMアプリケーション開発の実務経験あり（OCI Generative AI Service等）
- OpenTelemetry（OTel）は名前と概要を知っている程度。体系的な理解はない
- Prometheus, Loki, Tempo, Grafana, Langfuse, OTel Collectorはクラスタにデプロイ済みだが、各ツールの具体的な利用方法やアーキテクチャの深い理解はない

### 本書のゴール

AIエージェントシステムの開発品質を上げるためのObservability環境を理解し、自律的に活用・拡張できるようになること。具体的には以下の状態を目指す。

- Observabilityに関わるツール群の関係性と役割分担を「知識地図」として描ける
- OTelの概念モデルを理解し、エージェントアプリケーションに対して何を計装すべきか判断できる
- 手動計装のコードを書ける、自動計装の仕組みと限界を理解している
- 収集したデータをGrafana・Langfuseで活用するために、何ができるかを把握し、具体的な作業をコーディングエージェントに指示できる
- 新しいメトリクスやトレースの追加が必要になったとき、アプリ側の計装追加からダッシュボードへの反映まで、一連のフローを自力で回せる

### 前提環境

- Kubernetesクラスタ上に以下がデプロイ済み
  - OpenTelemetry Collector
  - Prometheus（メトリクスストア）
  - Loki（ログストア）
  - Tempo（トレースストア）
  - Grafana（可視化）
  - Langfuse（LLM Observability）
- LLMバックエンドはOCI Generative AI Service（Responses API対応、OpenAI SDK互換）
- エージェント実装言語はPython
- セットアップ手順は本書のスコープ外（環境は既にある前提）

### 想定分量

200〜300ページ

### 表現方針

- 図はMermaid記法で記述する
- コード例は実際に動くシンプルなものを使う。本題（Observabilityの理解）からズレる複雑なセットアップは避ける
- 各概念は「なぜそうなっているか」の背景から説明する。浮いた知識にならないよう、知識地図の中での位置づけを常に示す
- QL系（PromQL, TraceQL, LogQL）は文法詳細に深入りしない。「何ができるか」「コーディングエージェントにどう指示すればいいか」を重視する
- バックエンド（Prometheus, Loki, Tempo）の内部構造やチューニングには深入りしない。「データストア」としての役割を理解する程度

---

## 第1部: 全体像と知識地図

### 第1章: なぜAIエージェントにObservabilityが必要なのか

#### この章のゴール

Observabilityの必要性を「従来のシステムとの違い」から理解し、本書で学ぶ内容の全体像を掴む。

#### 内容

- 従来のマイクロサービスのObservability
  - 決定論的な処理フロー: リクエストが来て、処理して、レスポンスを返す
  - 「何が起きたか」はログ・メトリクス・トレースで概ね追跡可能
  - 障害の原因は「どこで何が壊れたか」のレベルで特定できる

- AIエージェントの根本的な違い
  - 非決定論的な処理: 同じ入力でもLLMの出力が変わる
  - 「判断」がシステムの中核にある: どのツールを使うか、どのエージェントにルーティングするか、LLMが決めている
  - 「何が起きたか」だけでなく「なぜそう判断したか」まで追わないと品質改善ができない
  - エージェント間の協調動作: 複数のエージェントが連鎖的に動くため、1つのリクエストの全体像を把握するのが難しい

- AIエージェントのObservabilityで追うべき2つの関心事
  - 関心事A: システムとして何が起きたか（トレーシング）
    - リクエストがどのAgentを通って、どのくらい時間がかかって、どこでエラーが出たか
    - 従来の分散トレーシングの延長
  - 関心事B: LLMの出力品質はどうだったか（評価）
    - プロンプトに対してLLMがどう返したか
    - その判断は適切だったか
    - トークンコストはいくらか
    - 従来のObservabilityにはなかった関心事

- 改善ループの具体的な流れ（本書を通じて理解するもの）
  - 「リクエスト全体が遅い」→ Grafana + Tempoでトレースを確認 → ボトルネック特定
  - 「LLMが変な判断をした」→ Langfuseでプロンプトとレスポンスを精査 → プロンプト修正
  - 「修正後、全体的に品質上がった？」→ Langfuseでスコア推移確認 + Grafanaでレイテンシ・エラー率変化確認

### 第2章: ツール群の知識地図

#### この章のゴール

本書で扱うツール群の全体像を知識地図として描く。各ツールが「どの層の問題を解決するか」を明確にし、以降の章で個別のツールに入ったときに「今、地図のどこの話をしているか」を常に把握できる状態にする。

#### 内容

- 3層モデルで整理する
  - 計装層（Instrumentation）: アプリケーション内部でデータを生成する
    - OTel SDK（手動計装）: 自分でSpanやMetricを定義して記録する
    - OpenLLMetry（自動計装）: LLM SDK呼び出しを自動でOTelのSpanに変換する
    - Langfuse SDK: LLMの入出力を記録し、評価・スコアリングに使う
  - 収集・転送層（Collection）: 生成されたデータを受け取り、適切な保存先に流す
    - OTel Collector: Receivers → Processors → Exportersの3段パイプライン
  - 保存・可視化層（Storage & Visualization）: データを保存し、人間が見て判断できるようにする
    - Prometheus: メトリクスストア
    - Tempo: トレースストア
    - Loki: ログストア
    - Grafana: 3つのストアを横断的に見るUI
    - Langfuse: LLM特化の可視化・評価UI

- データフロー全体図（Mermaid図で表現）
  - エージェントアプリ → (OTel SDK / OpenLLMetry) → OTel Collector → Tempo / Prometheus / Loki → Grafana
  - エージェントアプリ → (Langfuse SDK or OTLP) → Langfuse

- 各ツールの役割を一言で
  - OTel: 計装の標準仕様とSDK。「何をどう記録するか」のフレームワーク
  - OTel Collector: データの中継・変換。アプリとバックエンドを疎結合にする
  - OpenLLMetry: OTelのLLM向け拡張。LLM呼び出しの自動計装
  - Prometheus / Loki / Tempo: データストア。それぞれメトリクス、ログ、トレースを保存する。内部の詳細は本書のスコープ外
  - Grafana: 可視化UI。3つのデータストアに対してクエリを投げて結果を表示する
  - Langfuse: LLM Observabilityの専用プラットフォーム。トレーシング、評価、プロンプト管理

- 「どっちを見ればいい？」の判断基準
  - 「システムが正常に動いているか」→ Grafana（Prometheus + Tempo + Loki）
  - 「LLMが賢く動いているか」→ Langfuse

### 第3章: OTelはなぜ生まれたか ― 標準化の背景

#### この章のゴール

OTelが「なぜ標準になったか」を理解する。単なるツールの紹介ではなく、どういう課題を解決するために生まれたかを知ることで、設計判断の根拠を持てるようにする。

#### 内容

- ベンダーロックイン問題
  - 分散トレーシングの初期: 各ベンダー（Datadog, New Relic, Jaeger, Zipkin等）が独自のSDKとフォーマットを持っていた
  - アプリケーションの計装コードがベンダーに依存 → バックエンドを変えるたびに計装の書き直し
  - 「計装」と「バックエンド」を分離したい、という動機

- OpenTracing と OpenCensus
  - OpenTracing: CNCFプロジェクト。計装APIの標準化を目指した（トレース特化）
  - OpenCensus: Google主導。トレースとメトリクスの両方をカバー
  - 2つの標準が並立する状態に → エコシステムの分断

- OpenTelemetryの誕生
  - 2019年、OpenTracingとOpenCensusが統合してOTelに
  - CNCFのIncubatingプロジェクト → Graduatedへ
  - 目標: 計装の標準を1つにする。Traces, Metrics, Logsの3シグナルすべてをカバー
  - ベンダーニュートラル: 計装はOTelで統一し、バックエンドは自由に選べる

- なぜこの背景が重要か
  - OTel Collectorを間に挟む設計の理由: バックエンドの差し替えがアプリに影響しない
  - OpenLLMetryがOTelの上に構築されている理由: LLM向けの計装も標準に乗せることで、バックエンドを選ばない
  - OpenLLMetryのOTel本体への合流の動き: LLM計装の標準化が進行中

---

## 第2部: OTelの概念と仕組み

### 第4章: OTelの概念モデル

#### この章のゴール

OTelのデータモデル（Trace, Span, Attribute, SpanContext, Event）を理解する。それぞれが何であり、どう関係するかを、コード例を通じて体感する。

#### 内容

- Attribute
  - OTelの最小単位。key-valueペア
  - 例: `model_name: "gpt-4"`, `token_count: 150`, `agent.name: "ri-agent"`
  - それ自体は構造を持たない、ただのメタデータ
  - コード例: Attributeの定義と付与

- Span
  - 「ある処理の区間」。開始時刻と終了時刻を持つ
  - 名前を持つ（`decide_routing`, `llm_call`等）
  - Attributeを複数つけられる
  - Pythonでは `with tracer.start_as_current_span("name")` で作る
  - コード例: Spanの作成、Attributeの付与、ネストしたSpanの親子関係

- Trace
  - Spanの集合。1つのリクエストの全体像
  - 重要: Traceというオブジェクトを明示的に作ることはない
  - 同じTrace IDを共有するSpanの集まりが結果としてTraceになる
  - Root Spanを作った時点でTrace IDが自動生成される

- SpanContext
  - Trace IDとSpan IDのペア
  - 「今どのTraceのどのSpanの中にいるか」を表す
  - `with` をネストすると、内側のSpanは外側のSpanContextを親として参照
  - コード例: ネストしたSpanでSpanContextがどう伝播するかを確認

- Context Propagation
  - SpanContextをプロセス境界を越えて伝える仕組み
  - W3C Trace Context形式: HTTPヘッダーにTrace IDとSpan IDを埋め込む
  - これがないと、サービス間のトレースがバラバラになる
  - 概念レベルで理解すれば十分（エージェント間通信への適用は後日）
  - コード例: HTTPヘッダーへのTrace Context注入の仕組み（概念的に示す）

- Event
  - Span内の特定の瞬間を記録する仕組み
  - OTelのGenAI Semantic Conventionsでは、プロンプトやレスポンスの内容をEventとして記録する方向で仕様策定中
  - Span Attributeにプロンプト全文を入れるか、Eventとして記録するかの違い
  - 現状experimentalなので深入りはしない。「こういう概念がある」レベルで認識しておく

- ハンズオン: 最小限のコードでSpanを作り、OTel Collectorに送り、Tempoで表示されることを確認
  - 手動でSpanを作成
  - ネストしたSpanで親子関係を確認
  - Attributeをつけて、Tempoの検索で引っかかることを確認

### 第5章: 3つのシグナル ― Traces, Metrics, Logs

#### この章のゴール

OTelが扱う3つのデータ種別を理解し、それぞれの用途と保存先を把握する。

#### 内容

- Traces（前章の深掘り）
  - 「1つのリクエストの処理の流れ」を追う
  - 用途: 個別のリクエストを深掘りするとき
  - 保存先: Tempo
  - エージェント開発では最も頻繁に使うシグナル

- Metrics
  - 集計データ。「過去5分間のリクエスト数」「平均レイテンシ」「エラー率」
  - 型: Counter（累積値）, Histogram（分布）, Gauge（現在値）
  - 用途: システム全体の傾向を見るとき
  - 保存先: Prometheus
  - コード例: CounterとHistogramの作成・記録

- Logs
  - イベント単位のテキストデータ
  - OTelでの特徴: SpanContextを紐付けられる → 「このログはどのTraceのどのSpanで出たか」を辿れる
  - 用途: 詳細なデバッグ情報、構造化されていないイベント
  - 保存先: Loki

- 3つのシグナルの関係と使い分け
  - Metricsで異常を検知 → Tracesで該当リクエストを特定 → Logsで詳細を確認、という流れ
  - エージェント開発では: Metricsで全体傾向 → Tracesで個別リクエストの判断フローを追う → Langfuseでプロンプト品質を深掘り

- ハンズオン: 3つのシグナルをすべてOTel Collectorに送り、それぞれGrafanaで確認
  - Metric（Counter）を送ってPrometheusで確認
  - Logを送ってLokiで確認
  - 前章のTraceと合わせて、3シグナルが全部流れる状態を作る

### 第6章: OTel Collector ― データの中継と変換

#### この章のゴール

Collectorの設定ファイルを読めるようになり、基本的な変更（Exporterの追加等）ができるようになる。

#### 内容

- Collectorの役割
  - アプリとバックエンドの間に入る中継点
  - なぜ直接バックエンドに送らないのか: バックエンドの差し替え、バッチ処理、サンプリング等をアプリから切り離す
  - 第3章の「なぜ標準化が必要だったか」との接続

- パイプラインの3段構成
  - Receivers: データの受け口。OTLP（gRPC/HTTP）が基本
  - Processors: 中間処理。バッチ化、属性の追加・削除、サンプリング
  - Exporters: データの送り先。Tempo, Prometheus, Loki等

- パイプラインの種類
  - traces用パイプライン: Receiver → Processor → Exporter (Tempo)
  - metrics用パイプライン: Receiver → Processor → Exporter (Prometheus)
  - logs用パイプライン: Receiver → Processor → Exporter (Loki)
  - 独立して動く

- 設定ファイルの読み方
  - YAML形式
  - receivers, processors, exporters, service.pipelines のセクション構成
  - 一般的な構成例をベースに各セクションを解説

- 実践: Exporterの追加
  - 既存の設定に新しいExporterを追加する手順
  - 例: Langfuse向けOTLPエクスポートを追加する場合の設定変更
  - 設定変更後の反映方法（Collector再起動/リロード）

### 第7章: 自動計装と手動計装

#### この章のゴール

2つの計装方式の仕組みと使い分けを理解する。「何を自動に任せ、何を手動で書くか」の判断基準を持つ。

#### 内容

- 自動計装の仕組み
  - モンキーパッチ: ライブラリの内部メソッドにフックを挿入
  - 例: `requests.get()` を呼ぶだけでHTTPリクエストのSpanが出る
  - メリット: コード変更なし。1行の初期化で有効になる
  - 限界: ライブラリが対応していなければ動かない。「何を記録するか」の細かい制御ができない

- 手動計装の仕組み
  - `with tracer.start_as_current_span()` で自分でSpanを定義
  - Attributeで任意のメタデータを付与
  - メリット: 完全な制御。ビジネスロジック固有の「判断ポイント」を記録できる
  - コスト: コードに計装ロジックを埋め込む必要がある

- エージェント開発での使い分け
  - 自動計装で捕捉できるもの: LLM API呼び出し（OpenLLMetry経由）、HTTP通信
  - 手動計装が必要なもの: エージェントの判断ポイント（なぜそのツールを選んだか）、A2A通信のContext伝播、ビジネスロジック固有のメトリクス
  - 実際のエージェントでは両方を組み合わせる

- コード例: 両方を組み合わせたエージェントの計装
  - 自動計装（OpenLLMetry init）+ 手動計装（判断ロジックのSpan）が共存するコード
  - 生成されるトレースの構造を図示

### 第8章: GenAI Semantic Conventions ― LLM計装の標準化

#### この章のゴール

OTelプロジェクト内で進行中のGenAI向け標準化の動きを理解し、今後の技術選定に活かせる背景知識を得る。

#### 内容

- なぜGenAI向けの標準が必要なのか
  - LLM呼び出しは従来のHTTPリクエストとは質的に異なる情報を持つ（プロンプト、レスポンス、トークン使用量、モデルパラメータ等）
  - 各ツール（OpenLLMetry, Langfuse, LangSmith等）が独自のAttribute名・フォーマットを使っていた
  - 相互運用性の問題: ツールを切り替えるとデータの互換性がない

- OTel GenAI Semantic Conventions の概要
  - OTelプロジェクト内のGenAI SIG（Special Interest Group）が策定
  - 標準Attribute名: `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.response.model` 等
  - 3つのシグナルへの対応: Traces（Span属性）, Metrics（トークン使用量等の集計）, Events（プロンプト/レスポンスの記録）
  - 現状はexperimentalだが、主要ベンダーが準拠を進めている

- OpenLLMetryとOTel本体の合流
  - TraceloopがOpenLLMetryの計装コードをOTelプロジェクトに寄贈する動き
  - OTel Python Contribリポジトリ内でのOpenAI向け計装ライブラリの開発
  - 将来的には: OpenLLMetryの個別パッケージ → OTel公式パッケージとして提供

- 実務への影響
  - 今OpenLLMetryを使っている場合、将来的にOTel本体の計装に移行しやすい
  - Attribute名がSemantic Conventionsに準拠していれば、バックエンドの入れ替えが容易
  - 「枯れた標準」ではないため、破壊的変更の可能性はある → experimentalステータスの意味を理解しておく

---

## 第3部: AIエージェント固有のObservability

### 第9章: OpenLLMetry ― LLM呼び出しの自動計装

#### この章のゴール

OpenLLMetryの仕組み、セットアップ方法、出力されるデータ、そして限界を理解する。

#### 内容

- OpenLLMetryとは何か
  - Traceloop社が開発するOSS。LLM SDKの呼び出しを自動的にOTelのSpanに変換する
  - OTelの自動計装と同じ仕組み（モンキーパッチ）をLLM SDK向けにやるもの
  - 40以上の計装パッケージ: OpenAI, Anthropic, Cohere, LangChain, LlamaIndex等

- セットアップと基本的な使い方
  - `Traceloop.init()` 1行で自動計装が有効になる
  - 対応SDKを普通に呼ぶだけで、裏側でSpanが生成される
  - コード例: 最小限のセットアップと動作確認

- 自動で記録されるデータ
  - Span名: `openai.chat` 等
  - Attributes: モデル名、トークン数（input/output）、temperature等のパラメータ
  - プロンプトとレスポンスの内容（環境変数 `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=True` で有効化）
  - 注意: プロンプト/レスポンスの記録はデフォルトOFF（セキュリティ/プライバシー考慮）

- OpenLLMetryの限界
  - 対応SDKにしか効かない: OCI GenAI固有のSDK（`oci.generative_ai_inference`）には非対応の可能性
  - 「判断の理由」は記録できない: LLM呼び出し自体は捕捉するが、なぜその呼び出しをしたかの文脈は手動計装が必要
  - フレームワーク依存: SDKのバージョンアップで計装が壊れる可能性がある

- デコレータによるワークフロー定義
  - `@workflow`, `@task`, `@agent` デコレータでSpanの階層を宣言的に定義できる
  - 手動の `with` 句との使い分け

### 第10章: OCI GenAI + OpenAI SDK環境での検証ポイント

#### この章のゴール

OCI Generative AI ServiceをOpenAI SDK経由で利用する環境で、OpenLLMetryがどこまで機能するかを検証する。実践的な判断ポイントを押さえる。

#### 内容

- OCI GenAI ServiceのOpenAI SDK互換性
  - Responses APIがOpenAI SDK互換のインターフェースを提供
  - `oci-openai` パッケージ、またはOCI GenAI API Key + OpenAI SDKのbase_url変更で利用可能
  - Chat Completions APIとResponses APIの2つのインターフェースがある

- 検証すべきポイント
  - OpenAI SDK + Chat Completions API経由 → OpenLLMetryの自動計装が効くか
    - OpenAI SDKのメソッドにパッチが当たるので、バックエンドがOCIでも動くはず
    - トークン使用量やモデル名が正しく記録されるかの確認
  - Responses API固有の機能（オーケストレーション、ツール呼び出し、メモリ等）→ OpenLLMetryが追跡できるか
    - Responses APIは内部で複数のLLM呼び出しやツール実行を行う
    - OpenLLMetryがこの内部フローを個別のSpanとして捕捉できるかは不明
    - 対応していない場合、Responses APIの内部は1つのブラックボックスSpanになり、手動計装で補う必要がある

- 検証の手順
  - Step 1: OpenAI SDK + Chat Completions API + OpenLLMetryで基本動作を確認
  - Step 2: Responses APIで同様に試し、出力されるSpanの構造を確認
  - Step 3: 不足があれば手動計装のポイントを特定

- 判断基準
  - 自動計装で十分な情報が取れるなら、それに乗る（メンテナンスコストが低い）
  - 不足があれば手動計装で補完する。ただし将来的にOpenLLMetryやOTel本体がResponses APIに対応する可能性もあるため、手動計装部分は差し替え可能な設計にしておく

### 第11章: Langfuseの機能と使い方

#### この章のゴール

Langfuseの3つの機能（トレーシング、評価、プロンプト管理）を理解し、基本的な使い方を身につける。

#### 内容

- Langfuseの位置づけ
  - 「LLMの判断品質を顕微鏡で見る」ツール
  - OTel+Grafanaが「システム全体の地図」なら、LangfuseはLLMの出力品質に特化した分析ツール

- 機能1: トレーシング
  - LLM呼び出しの入出力を記録・閲覧
  - プロンプトとレスポンスを並べて見る
  - トークンコストの集計
  - OTelのトレースビューアではこの操作が面倒なところを、専用UIで効率化
  - コード例: Langfuse SDKでのトレース記録

- 機能2: 評価（Evaluation）
  - トレースに対してスコアをつける
  - 人手レビュー: 「この回答は適切だった」を手動で記録
  - 自動評価: 別のLLMに判定させる（LLM-as-judge）
  - スコアの推移を時系列で追跡
  - これが「改善ループ」の核。OTel側にはない機能

- 機能3: プロンプト管理
  - プロンプトのバージョン管理
  - v1とv2でどちらが良い結果を出すかをトレースデータと紐付けて比較
  - プロンプトの変更がシステム全体の品質にどう影響したかを定量的に評価

- コード例: Langfuse SDKの基本操作
  - トレースの作成
  - Spanの追加（Generation, Span等）
  - スコアの付与
  - プロンプトのバージョン管理

### 第12章: OTelとLangfuseの役割分担とデータ送信経路

#### この章のゴール

OTelとLangfuseの使い分けを明確にし、Langfuseへのデータ送信経路（OTLP vs SDK）の選択基準を理解する。

#### 内容

- 役割分担の整理
  - OTel + Grafana: 「システムとして何が起きたか」を見る
    - リクエストのレイテンシ、エラー率、スループット
    - トレース全体の構造（どのAgentを通ったか）
    - インフラのリソース使用状況
  - Langfuse: 「LLMが賢く動いているか」を見る
    - プロンプトとレスポンスの内容
    - 出力品質のスコアリング
    - トークンコストの管理
    - プロンプトのバージョン比較

- trace_idによる紐付け
  - OTelのtrace_idをLangfuseのトレースにメタデータとして渡す
  - 「Grafanaでボトルネックを見つける → 同じtrace_idでLangfuseを開いてLLMの判断品質を精査」という横断的なデバッグフロー

- Langfuseへのデータ送信経路の選択

  - 経路A: OTLP経由（OTel Collector → Langfuse）
    - LangfuseがOTLPエンドポイントを提供している
    - OpenLLMetryで計装 → OTel Collector → Langfuseの流れ
    - メリット: 計装コードがOTelに統一される。Collectorで一元管理できる
    - デメリット: Langfuse固有の機能（評価、プロンプト管理）はOTLP経由では使えない

  - 経路B: Langfuse SDK直接
    - アプリケーションからLangfuse SDKで直接データを送る
    - メリット: Langfuseの全機能（評価、スコアリング、プロンプト管理）が使える
    - デメリット: 計装コードにLangfuse依存が入る

  - 経路C: 併用（推奨）
    - OTel（OpenLLMetry + 手動計装）でシステムトレーシングを行い、Collector経由でTempo等に送る
    - Langfuse SDKでLLMの品質評価に必要なデータを送る
    - trace_idで両者を紐付ける
    - 各ツールの強みを活かす実践的な構成

  - 判断基準のまとめ
    - 評価・スコアリング機能が必要 → Langfuse SDK必須
    - プロンプト管理が必要 → Langfuse SDK必須
    - システムトレーシングの一貫性を重視 → OTel経由
    - 現実的には併用が最も効果的

---

## 第4部: 実践 ― 収集と可視化

### 第13章: Python OTel SDKでの手動計装

#### この章のゴール

実際にPythonコードで手動計装を書けるようになる。SDKの初期化からSpan/Metric/Logの記録、Collectorへの送信までの一連のフローを身につける。

#### 内容

- SDK初期化の基本パターン
  - TracerProviderの設定
  - MeterProviderの設定
  - OTLPエクスポータの設定（CollectorへのgRPC接続）
  - コード例: 最小限の初期化コード

- Spanの作成と操作
  - `tracer.start_as_current_span()` の使い方
  - Attributeの付与: `span.set_attribute()`
  - ステータスの設定: 成功/エラーの記録
  - 例外の記録: `span.record_exception()`
  - コード例: エラーハンドリングを含むSpan作成

- Metricの記録
  - Counter: `meter.create_counter()` → `counter.add()`
  - Histogram: `meter.create_histogram()` → `histogram.record()`
  - コード例: リクエスト数とレイテンシの記録

- エージェントの計装パターン
  - 自動計装（OpenLLMetry）と手動計装を組み合わせた典型的なパターン
  - LLM呼び出しは自動、判断ロジックは手動、という組み合わせ
  - 生成されるトレースの構造を図示
  - コード例: エージェントのハンドラ関数に計装を追加

### 第14章: OpenLLMetryのセットアップと検証

#### この章のゴール

OpenLLMetryを実際にセットアップし、OCI GenAI環境で動作検証を行う。

#### 内容

- セットアップ手順
  - パッケージのインストール
  - `Traceloop.init()` の設定オプション
  - Collectorへの接続設定（環境変数）
  - プロンプト/レスポンスのキャプチャ設定

- OCI GenAI環境での動作検証
  - OpenAI SDK + base_url変更でOCI GenAIに接続
  - Chat Completions APIでの自動計装動作確認
  - Responses APIでの動作確認と出力されるSpanの構造確認
  - 不足がある場合の手動計装での補完方法

- Tempoでのトレース確認
  - Grafana上でTempoデータソースからトレースを検索
  - 自動計装で生成されたSpanの内容確認
  - Attributeの中身（モデル名、トークン数等）の確認

### 第15章: OTel Collectorの設定

#### この章のゴール

Collectorの設定ファイルを読めるようになり、Exporterの追加程度の変更ができるようになる。

#### 内容

- 設定ファイルの全体構造
  - 一般的な構成例のYAMLを読み解く
  - receivers, processors, exporters, service.pipelines の各セクション

- よく使うReceiver
  - otlp: gRPC/HTTP でOTelデータを受け取る（最も基本的）

- よく使うProcessor
  - batch: バッチ処理（送信効率の向上）
  - attributes: Attributeの追加・変更・削除
  - memory_limiter: メモリ使用量の制限

- よく使うExporter
  - otlphttp (Tempo向け): トレースの送信
  - prometheusremotewrite (Prometheus向け): メトリクスの送信
  - loki (Loki向け): ログの送信

- 実践: 設定変更の手順
  - 新しいExporterを追加する例
  - pipelineに組み込む
  - 変更の反映方法

### 第16章: Grafanaでのデータ活用

#### この章のゴール

Grafanaで何ができるかを把握し、ダッシュボードの作成やトレース検索をコーディングエージェントに指示できるようになる。

#### 内容

- データソースの概念
  - Grafanaはデータを自分で持たない。バックエンドに対してクエリを投げて結果を表示する
  - Prometheus, Tempo, Loki がそれぞれデータソースとして接続される

- Prometheusデータソースで何ができるか（メトリクス）
  - 時系列データの可視化: 折れ線グラフ、棒グラフ、ゲージ
  - 集計: 一定期間のレート、平均、パーセンタイル
  - クエリ言語: PromQL
  - 指示の出し方の例: 「過去1時間のリクエスト数を1分単位で折れ線グラフにして」「エラー率が5%を超えたらアラート出して」

- Tempoデータソースで何ができるか（トレース）
  - トレースの検索: サービス名、Span名、Attribute値で絞り込み
  - トレースの詳細表示: Spanのウォーターフォール表示、各Spanの所要時間とAttribute
  - クエリ言語: TraceQL
  - 指示の出し方の例: 「ri-agentのSpanでレイテンシが3秒以上のトレースを検索して」「特定のtrace_idのトレースを表示して」

- Lokiデータソースで何ができるか（ログ）
  - ログの検索: ラベルとテキストパターンで絞り込み
  - 時系列集計: ログの発生頻度のグラフ化
  - クエリ言語: LogQL
  - 指示の出し方の例: 「過去30分のエラーログを表示して」「特定のtrace_idに紐づくログを検索して」

- ダッシュボードの基本
  - パネル: 1つのクエリ結果を1つの可視化として表示する単位
  - ダッシュボード: パネルの集合
  - テンプレート変数: ドロップダウンで動的にフィルタリング
  - 作成の流れ: ダッシュボード作成 → パネル追加 → データソース選択 → クエリ記述 → 可視化タイプ選択

- ベースラインダッシュボードの例
  - エージェントシステム向けに最低限あるとよいパネル構成
  - リクエスト数の推移（Prometheus）
  - レイテンシの分布（Prometheus）
  - エラー率（Prometheus）
  - 最新のトレース一覧（Tempo）

### 第17章: End-to-Endフロー ― メトリクス追加からダッシュボード表示まで

#### この章のゴール

「新しいメトリクスが欲しい」となったときに、アプリ側の計装からダッシュボードへの反映まで、一連のフローを自力で回せるようになる。

#### 内容

- 追加の流れ（全体像）
  1. アプリケーションコードでMeter APIを使って新しいメトリクスを定義・記録
  2. OTel Collectorが既存のmetricsパイプラインで受信（通常、設定変更不要）
  3. Prometheusに保存される
  4. GrafanaでPromQLクエリを書いてパネルに表示

- 実践: トークン使用量のメトリクスを追加する例
  - Step 1: Pythonコードでhistogramを作成し、LLM呼び出しごとにトークン数を記録
  - Step 2: Collectorの設定を確認（通常は既存パイプラインで受信できる）
  - Step 3: GrafanaでPromQLクエリを作成し、パネルに表示
  - Step 4: ダッシュボードに追加

- トレースの追加も同様
  - 新しいカスタムSpanをコードに追加 → Tempoに自動保存 → GrafanaのTraceQL検索で確認
  - Collector側の設定変更は通常不要

- 拡張パターンの理解
  - 計装の追加はアプリ側の作業
  - Collectorは基本的に変更不要（新しいバックエンドを追加しない限り）
  - Grafanaはクエリとパネルの追加

---

## 付録

### 付録A: クエリ言語チートシート

- PromQL, TraceQL, LogQLの基本パターンを一覧で
- 「こういうことを調べたいとき、どう書くか」の逆引きリファレンス
- コーディングエージェントへの指示テンプレート

### 付録B: OTel Python SDK APIリファレンス

- よく使うAPI（TracerProvider, Tracer, Span, Meter, Counter, Histogram）の使い方早見表
- 初期化コードのテンプレート

### 付録C: 用語集

- 本書で使用する用語の定義一覧
