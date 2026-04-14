# 書籍企画書 (Book Plan)

## 書籍概要

### タイトル
**AIエージェント開発のためのObservability実践ガイド** ― OpenTelemetry・Grafana・Langfuseで築く「判断」の可視化基盤

### 形態
- 判型: B5
- 想定ページ数: 約240ページ（200〜300ページの範囲）
- 配布形態: 技術書典想定（商業出版対応可）

### コンセプト
- **知識地図で理解する**: 個別ツールの羅列ではなく、計装層・収集層・保存可視化層の3層モデルで全体像を描き、読者が常に「今どこの話か」を把握できる構成とする
- **「何が起きたか」と「なぜそう判断したか」の両立**: 従来のシステムObservabilityに加え、LLMの判断品質を追跡する視点（Langfuse）をOTelと併用する実践的アプローチを提示する
- **エージェントに指示できる運用者を育てる**: クエリ言語（PromQL/TraceQL/LogQL）の文法詳細ではなく「何ができるか」「コーディングエージェントにどう依頼するか」に重点を置く

### ビジョン
AIエージェントシステムを開発・運用するエンジニアが、Observabilityツール群を「なんとなく動いているブラックボックス」から「自律的に活用・拡張できる道具」へと変えるための1冊。本書を読み終えた読者は、OpenTelemetryの概念モデルを自分の言葉で語れ、OCI Generative AI Serviceを使ったPythonエージェントに適切な計装を施し、Grafana・Langfuseで品質改善ループを回せるようになる。個別ツールのマニュアルではなく、ツール間の関係性と役割分担を「地図」として提示することで、新しいツールや要件が出てきても自力で位置付けができる汎用的な理解を提供する。

## 対象読者

### プライマリーペルソナ
- AIエージェント／LLMアプリケーションの開発・運用を担うエンジニア
- Kubernetes（OKE等）の実務経験があり、Pythonでのアプリケーション開発が可能
- OCI Generative AI Service等を用いたLLMアプリ開発経験を持つ
- OpenTelemetryは名前と概要を知る程度で、体系的な理解はない
- Prometheus・Loki・Tempo・Grafana・Langfuse・OTel Collectorはクラスタにデプロイ済みだが、各ツールの具体的な利用方法やアーキテクチャの深い理解はない
- 課題: 「計装したログやメトリクスをどう活用すれば品質改善につながるのか」「自分で新しい観測項目を追加する方法がわからない」

### 前提知識
読者が本書を読む前に理解していることを前提とする:
- Kubernetesの基本操作（Pod、Service、Deployment、マニフェスト適用）
- Pythonでの開発経験（パッケージ管理、非同期処理の基本）
- LLM API（OpenAI SDK互換含む）を呼ぶコードを書いた経験
- HTTP／gRPCの基本、分散システムの基本概念

### 前提としない知識
本書で説明する:
- OpenTelemetryのデータモデル（Trace、Span、Attribute、Context Propagation、GenAI Semantic Conventions）
- 自動計装と手動計装の仕組みと使い分け
- OTel Collectorのパイプライン（Receivers／Processors／Exporters）
- Grafana・Langfuseで何ができるか、どう使い分けるか
- OpenLLMetryの仕組み・限界・OCI GenAI環境での検証ポイント

## 到達目標

読了後、読者が以下をできるようになること:

1. Observabilityツール群の関係性と役割分担を3層モデルの「知識地図」として描ける
2. OpenTelemetryの概念モデル（Trace／Span／Context／3シグナル）を理解し、エージェントアプリケーションに対して何を計装すべきか判断できる
3. Python OTel SDKで手動計装のコードを書け、OpenLLMetryによる自動計装の仕組みと限界を理解している
4. GrafanaとLangfuseの機能を把握し、ダッシュボード作成や評価のフローをコーディングエージェントに的確に指示できる
5. 新しいメトリクスやトレースの追加が必要になった際、アプリ側の計装追加からOTel Collector・Grafanaへの反映までを自力で一通り回せる

## 全体構成

### 部構成

| 部 | タイトル | 概要 | ページ（目安） |
|----|---------|------|--------------|
| 第I部 | 全体像と知識地図 | Observabilityが必要な理由、ツール群の3層モデル、OTel標準化の背景 | 32 |
| 第II部 | OTelの概念と仕組み | Trace／Span／3シグナル／Collector／自動・手動計装／GenAI Semantic Conventions | 68 |
| 第III部 | AIエージェント固有のObservability | OpenLLMetry、OCI GenAI+OpenAI SDK環境の検証、Langfuse、OTelとの併用戦略 | 54 |
| 第IV部 | 実践 ― 収集と可視化 | Python SDKでの手動計装、OpenLLMetry実践、Collector設定、Grafana活用、E2Eフロー | 70 |
| 付録 | クエリ言語チートシート／SDK APIリファレンス／用語集 | 逆引きリファレンスと早見表 | 16 |

### 章構成

| 章 | タイトル | ページ（目安） | 性質 |
|----|---------|--------------|------|
| 第1章 | なぜAIエージェントにObservabilityが必要なのか | 10 | 動機・概念 |
| 第2章 | ツール群の知識地図 | 12 | 全体像 |
| 第3章 | OTelはなぜ生まれたか ― 標準化の背景 | 10 | 背景・歴史 |
| 第4章 | OTelの概念モデル | 18 | 概念＋ハンズオン |
| 第5章 | 3つのシグナル ― Traces、Metrics、Logs | 14 | 概念＋ハンズオン |
| 第6章 | OTel Collector ― データの中継と変換 | 14 | 概念＋設定 |
| 第7章 | 自動計装と手動計装 | 12 | 概念＋比較 |
| 第8章 | GenAI Semantic Conventions ― LLM計装の標準化 | 10 | 背景・仕様 |
| 第9章 | OpenLLMetry ― LLM呼び出しの自動計装 | 14 | ツール解説＋実装 |
| 第10章 | OCI GenAI + OpenAI SDK環境での検証ポイント | 12 | 検証・実践判断 |
| 第11章 | Langfuseの機能と使い方 | 14 | ツール解説＋実装 |
| 第12章 | OTelとLangfuseの役割分担とデータ送信経路 | 14 | 設計判断 |
| 第13章 | Python OTel SDKでの手動計装 | 16 | 実装ハンズオン |
| 第14章 | OpenLLMetryのセットアップと検証 | 12 | 実装ハンズオン |
| 第15章 | OTel Collectorの設定 | 12 | 設定ハンズオン |
| 第16章 | Grafanaでのデータ活用 | 16 | 活用・指示出し |
| 第17章 | End-to-Endフロー ― メトリクス追加からダッシュボード表示まで | 14 | 統合ハンズオン |
| 付録A | クエリ言語チートシート | 6 | リファレンス |
| 付録B | OTel Python SDK APIリファレンス | 6 | リファレンス |
| 付録C | 用語集 | 4 | リファレンス |

合計: 約240ページ

## 技術環境

- **主要な技術スタック**:
  - 計装: OpenTelemetry Python SDK、OpenLLMetry（Traceloop SDK）、Langfuse SDK
  - 収集: OpenTelemetry Collector
  - 保存: Prometheus（メトリクス）、Loki（ログ）、Tempo（トレース）
  - 可視化・評価: Grafana、Langfuse
  - LLMバックエンド: OCI Generative AI Service（OpenAI SDK互換、Chat Completions／Responses API）
  - 実行基盤: Kubernetes（OKE想定、セットアップはスコープ外だが**既存クラスタ上の稼働済みスタックに対して全サンプルを実機検証する**）
- **コード例の言語**: Python（3.11以上を想定）
- **サンプル実行環境の前提**: 読者はOTel Collector・Prometheus・Loki・Tempo・Grafana・Langfuseがデプロイ済みのKubernetesクラスタを持つ。本書のサンプルは共有スタックを汚染しないよう、本書専用namespace（例: `aio11y-book`）に全リソースを閉じ込める
- **クリーンアップ機構**: リポジトリルートに一括掃除スクリプト（`make clean` もしくは `cleanup.sh`）と章単位の掃除ターゲット（`make clean-chNN`）を用意する。付録で手順を明記する

## 執筆方針

- **知識地図との接続を常に示す**: 個別のツール・概念を説明する際、3層モデルの「どこの話か」を毎章の冒頭または図で明示し、浮いた知識にならないようにする
- **「なぜそうなっているか」から入る**: 各概念は背景・動機から説明する。OTelの標準化、Collectorの分離、Langfuse併用の必要性など、設計判断の根拠を読者が自分で語れるレベルで記述する
- **図はMermaid記法**: 各節に最低1つの図表を配置する。Mermaid記法を優先し、表現できない場合のみテキスト図を用いる
- **コード例は最小限かつ実機で動作検証済み**: 概念理解に必要な最小限のコードに絞る。原稿に掲載する全てのコード・マニフェスト・Collector設定は、本プロジェクトがアクセス可能なKubernetesクラスタ（OTel Collector・Prometheus・Loki・Tempo・Grafana・Langfuseデプロイ済み）で実際に実行して動作確認したものに限定する（疑似コードにはその旨を明示）
- **掃除しやすさを設計原則に含める**: 全サンプルは専用namespaceに閉じ込め、一括削除スクリプト（`make clean`）と章単位の掃除ターゲット（`make clean-chNN`）を提供する。読者が「試してみて、後で綺麗に戻せる」状態を保証する
- **クエリ言語は深入りしない**: PromQL／TraceQL／LogQLは「何ができるか」「コーディングエージェントへの指示例」を重視し、文法の網羅は付録のチートシートに集約する
- **バックエンドの内部には立ち入らない**: Prometheus／Loki／Tempoは「データストア」として扱い、内部構造やチューニングは扱わない

## スコープ外

明示的にスコープ外とする項目:
- Kubernetesクラスタや各種ツール（Prometheus／Loki／Tempo／Grafana／Langfuse／OTel Collector）のデプロイ・セットアップ手順
- Prometheus／Loki／Tempoの内部アーキテクチャ、ストレージチューニング、スケーリング
- PromQL／TraceQL／LogQLの網羅的な文法解説
- OpenAI SDK・OCI GenAI Service以外のLLMプロバイダ（Anthropic、Cohere等）固有の計装詳細
- LangChain／LlamaIndex等のフレームワーク固有の自動計装の詳細網羅
- 本番運用のSRE観点（SLO設計、アラートポリシー、インシデント対応プロセス）

## 成功指標

- 読者が本書を読んだ後、自分のエージェントアプリに手動計装を追加し、Tempo／Prometheus／Loki／Langfuseでデータを確認できる
- 読者が「トークン使用量を可視化したい」等の要件に対し、アプリ計装→Collector→Grafanaダッシュボードまでの一連のフローを自力で組み立てられる
- 読者がOTelとLangfuseの役割分担を自分の言葉で説明でき、trace_idでの横断デバッグフローを実践できる
