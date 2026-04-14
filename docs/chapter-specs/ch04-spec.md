# 第4章 OTelの概念モデル ― 仕様書

## 章の概要

**章の目的**: OTelのデータモデル（Attribute、Span、Trace、SpanContext、Context Propagation、Event）を読者が自分の言葉で説明できるようにする。最小のハンズオンを通じて、Spanを作ってTempoに届ける動作を実機で確認する。

**目標ページ数**: 18p

**所属する部**: 第II部 OTelの概念と仕組み

## 前提知識

- 第2章（3層モデル）、第3章（OTelの設計思想）
- Python基礎（クラス・with構文）

## 節の構成

### 4.1 Attribute ― 最小単位のメタデータ

**概要**: key-valueペアとしてのAttributeを導入。他の全ての概念がAttributeを含むことを示す。

**図表**:
- 図4.1: Attributeの構造（キー・バリュー・型）

**キーポイント**:
- Attributeは構造を持たないメタデータ
- 命名規則（ドット階層）と型（string／int／bool／array）を押さえる

### 4.2 Span ― 処理区間の単位

**概要**: 開始時刻と終了時刻を持つ「処理区間」としてのSpanを説明する。名前・Attribute・ネストを持てる点を示す。

**図表**:
- 図4.2: Spanの構造図（開始終了時刻、名前、Attribute、親子関係）

**キーポイント**:
- `with tracer.start_as_current_span("name")` で作る
- Spanは親子関係を持ち、ネストしたwithで自動的に親子が設定される

### 4.3 Trace ― Spanの集合

**概要**: 同じTrace IDを共有するSpanの集合がTraceであることを示し、Traceオブジェクトを明示的に作らない点を強調する。

**図表**:
- 図4.3: Trace＝複数Spanの木構造（Root Spanから子Spanへ広がる木）

**キーポイント**:
- Trace IDはRoot Span生成時に自動割り当て
- 「Traceクラス」は存在しない（Span IDの集合として現れる）

### 4.4 SpanContext ― 現在位置の表現

**概要**: Trace IDとSpan IDのペアとしてのSpanContextを導入し、「現在どのSpanの中にいるか」がwithのネストで自動伝播する仕組みを示す。

**図表**:
- 図4.4: SpanContextの伝播（withネスト時の親子関係の自動設定）

**キーポイント**:
- SpanContextはコンテキストマネージャ（`contextvars`）で管理される
- 非同期処理では明示的なContext渡しが必要になる場合がある

### 4.5 Context Propagation ― プロセス境界を越える伝播

**概要**: HTTPヘッダーを介してSpanContextを別プロセスに引き継ぐ仕組みを、W3C Trace Context形式で概念的に示す。

**図表**:
- 図4.5: `traceparent` ヘッダーを介したサービス間伝播

**キーポイント**:
- W3C Trace Context（`traceparent` `tracestate`）が標準
- 本書のサンプルは単一Pod内で完結するが、概念として理解しておく

### 4.6 Event ― Span内の瞬間

**概要**: Span内の特定時点を記録する仕組みとしてEventを導入。GenAI Semantic Conventionsでは、プロンプト／レスポンス記録にEventを用いる動きがある点に触れる（experimentalとして深入りしない）。

**図表**:
- 図4.6: Span上のタイムライン上に配置されるEvent

**キーポイント**:
- Eventは「ログ」のSpan内版と考えられる
- 現状experimentalなため、本書では概念レベルに留める

### 4.7 ハンズオン ― 最小Spanを送る

**概要**: サンプルアプリ `sample-app/ch04/` をデプロイし、Spanを1つ生成してTempoで確認する。

**図表**:
- 図4.7: この章で動かす構成（`travel-helper-ch04` Pod → OTel Gateway Collector → Tempo → Grafana）
- リスト4.1: `sample-app/ch04/agent.py` のSpan生成部分抜粋
- リスト4.2: `sample-app/ch04/k8s/deployment.yaml` の該当部分

**キーポイント**:
- Tempoで `service.name=travel-helper-ch04` を検索してTraceを表示
- Spanの親子関係・Attributeが表示されることを確認
- 末尾で `make clean-ch04` による掃除手順を示す

## 図表リスト

| 図表番号 | タイトル | 種類 | 所属する節 |
|---------|---------|------|----------|
| 図4.1 | Attributeの構造 | 構造図 | 4.1 |
| 図4.2 | Spanの構造 | 構造図 | 4.2 |
| 図4.3 | Trace＝Spanの木 | 木構造図 | 4.3 |
| 図4.4 | SpanContextの伝播 | フロー図 | 4.4 |
| 図4.5 | Context Propagation（HTTP） | フロー図 | 4.5 |
| 図4.6 | Event on Span timeline | タイムライン図 | 4.6 |
| 図4.7 | ハンズオンの構成 | 構造図（Mermaid） | 4.7 |
| リスト4.1 | 最小Span生成コード | Pythonコード | 4.7 |
| リスト4.2 | Deploymentマニフェスト抜粋 | YAML | 4.7 |

## コード例

| リスト | 内容 | 言語 | 所属する節 |
|-------|------|------|----------|
| リスト4.1 | 最小Span生成（`sample-app/ch04/agent.py`） | Python | 4.7 |
| リスト4.2 | Deployment抜粋（`sample-app/ch04/k8s/deployment.yaml`） | YAML | 4.7 |

## サンプルコード要件

- **種別**: app（Python）＋k8s
- **場所**: `sample-app/ch04/`
- **機能**:
  - FastAPI `POST /plan` が `plan_stage` のみ実行して結果を返す
  - `plan_stage` を単一Spanとして記録し、`user.city` `user.days` `user.keywords_count` をAttributeとして付与
  - OTel TracerProviderの最小初期化
  - OTLP/gRPCで `otel-gateway-opentelemetry-collector.observability:4317` に送信
- **マニフェスト**: namespace.yaml（既にcommon）・deployment.yaml・service.yaml・configmap.yaml・secret.example.yaml
- **Makefile**: `build`・`deploy`・`verify`・`clean`
- **verify**: Pod Running、`/plan` 200 OK、Tempoで `service.name=travel-helper-ch04` のTraceが検索可能

## 章末の理解度チェック問題

### 問題の方針
- 問題数: 4問
- 種類: 概念の確認3問、設計問題1問

### 問題案
1. Trace・Span・Attribute・SpanContextの関係を図もしくは文で説明せよ。（概念の確認）
2. `with tracer.start_as_current_span()` をネストしたとき、内側Spanの親はどう決まるかを述べよ。（概念の確認）
3. Context Propagationがないとサービスを跨いだ分散トレーシングで何が起きるかを説明せよ。（概念の確認）
4. 2つのステージ（planとsynthesize）を持つ関数に対して、Spanをどう配置するかを設計せよ（何をRoot Spanにするか、stageごとにSpanを分けるか、Attributeに何を入れるか）。（設計問題）

## 章間の接続

### 前の章からの接続
- **前章の最後**: OTelの設計思想を示し、概念モデルは第II部で扱うと予告
- **この章の導入**: 「ここから第II部。OTelが扱う最小の概念から始める」
- **接続のキーフレーズ**: 「データモデルから理解する」

### 次の章への接続
- **この章の結び**: Traceを作れるようになったので、次はMetricsとLogsも同じ枠組みで扱えることを予告
- **次章への橋渡し**: 「3つのシグナルの違いと使い分けを理解する」
- **接続のキーフレーズ**: 「3シグナルへ広げる」
