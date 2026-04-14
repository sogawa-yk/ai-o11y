# サンプルアプリ全体仕様 (Product Requirements)

## 目的

本書で使うサンプルエージェント `travel-helper` の全体仕様を定義する。章をまたいで発展させる際の、機能範囲と非機能要件を確定させる。

## スコープ

### 含む
- ユーザー入力を受け取り、LLM判断で複数ツールを呼び、旅行行程を返すHTTP APIサーバ
- OCI Generative AI Service（OpenAI SDK互換）呼び出し
- スタブツール3種（weather／places／restaurant）
- Kubernetes（`aio11y-book` namespace）でのデプロイ
- OTel SDK／OpenLLMetry／Langfuse SDK を段階的に追加する計装

### 含まない
- 永続化ストレージ（DB、Redis等）
- 認証・認可
- 複数レプリカでの水平スケール
- UI（クライアントはcurlやPython scriptで十分）
- 本番運用向けのセキュリティ対策

## 機能要件

### FR-1: エージェントAPIエンドポイント

- `POST /plan` エンドポイントを持つ
- リクエストボディ: `{ "city": string, "days": integer, "keywords": [string] }`
- レスポンスボディ: `{ "itinerary": string, "trace_id": string }`
- 異常系: 400（バリデーションエラー）、500（LLM／ツールエラー）
- ヘルスチェック: `GET /healthz` → 200 OK

### FR-2: 3段階のエージェント処理

1. **plan_stage**: 入力キーワードから調査項目を決定（LLM呼び出し1回）
2. **gather_stage**: 必要なツールを順次呼ぶ（weather→places×N→restaurant）
3. **synthesize_stage**: 収集情報から行程文を生成（LLM呼び出し1回）

各stageは計装の単位となる（Span化する）。

### FR-3: LLMバックエンド切り替え

- 環境変数 `LLM_MODE=oci`（デフォルト）または `LLM_MODE=mock`
- `oci` の場合: OpenAI SDKの `base_url` をOCI GenAIに向けて呼び出す
- `mock` の場合: 固定の疑似レスポンスを返す（読者がキー無しで動作確認できる）

### FR-4: スタブツール

- `weather_tool(city, days)`: 固定パターン＋100〜200msの遅延
- `places_tool(city, keyword)`: 架空スポット3件＋150〜300msの遅延
- `restaurant_tool(city)`: 架空レストラン3件＋100〜200msの遅延
- 5%の確率で `ToolError` を投げる（Observability観測対象として意図的に挿入）

### FR-5: 章ごとの発展

`sample-app/chNN/` ディレクトリに章ごとの最終状態を配置。各章は独立して動作し、前章への依存は持たない。章間の差分は `docs/sample-code-spec/development-guidelines.md` に記録する。

## 非機能要件

### NFR-1: 動作検証可能性
- 本プロジェクトがアクセス可能なKubernetesクラスタ（OTel Collector／Prometheus／Loki／Tempo／Grafana／Langfuseデプロイ済み）で実機動作確認を行う
- 各章のMakefileに `make verify` を用意し、デプロイ後にTempo／Prometheus／Loki／Langfuseで観測データが確認できることをチェックする

### NFR-2: 追試容易性
- 読者は `git clone → make setup → cd sample-app/chNN → make deploy` の4ステップで動作確認可能
- 外部APIキーなしで動作するMockモードを提供

### NFR-3: 共有環境への非破壊性
- 全リソースは `aio11y-book` namespaceに閉じ込める
- 既存の `observability` `langfuse` namespaceには変更を加えない
- ラベル `book.aio11y/owned-by=book` を全リソースに付与

### NFR-4: クリーンアップ
- 章単位: 各章Makefileの `make clean` で当該章のリソースのみ削除
- 全削除: リポジトリルートの `make clean` で `aio11y-book` namespace全削除（namespace削除1回で完結）
- 実行時間: 全削除は60秒以内に完了することを目安とする

### NFR-5: 再現性
- コンテナイメージは固定タグで参照する（`latest` は使わない）
- Pythonの依存は `requirements.txt` でバージョン固定
- OTel／OpenLLMetry／Langfuse SDKのバージョンは `development-guidelines.md` に記録

### NFR-6: 計装のオーバーヘッド
- 計装追加前後でレスポンスタイムが2倍以上にならないこと（実用性確認の目安）

## 章ごとの機能マトリクス

| 章 | エージェント機能 | 計装 | 観測先 |
|----|----------------|------|-------|
| ch04 | plan_stageのみ | 手動Span（1個） | Tempo |
| ch05 | plan+gather（簡易） | Span／Metric／Log | Tempo／Prometheus／Loki |
| ch13 | 全stage | 全stage手動計装＋Attribute／Event／Status／Exception | Tempo／Prometheus／Loki |
| ch14 | 全stage | ch13 + OpenLLMetry自動計装 | Tempo（LLM呼び出しSpan詳細化） |
| ch15 | 全stage（ch14同等） | ch14 + カスタムCollector経由 | Tempo／Prometheus／Loki／Langfuse |
| ch11 | 全stage（ch14同等） | ch14 + Langfuse SDK評価記録 | Langfuse |
| ch17 | 全stage + トークンMetric追加 | ch15 + トークン使用量Histogram | Grafanaダッシュボード追加 |

## 環境変数仕様

全章共通で以下を認識する:

| 変数名 | デフォルト | 説明 |
|--------|-----------|------|
| `LLM_MODE` | `oci` | `oci` または `mock` |
| `OCI_GENAI_ENDPOINT` | なし | OCI GenAIのエンドポイントURL |
| `OCI_GENAI_API_KEY` | なし | APIキー |
| `OCI_GENAI_MODEL` | `xai.grok-3` | 使用モデル名 |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://otel-gateway-opentelemetry-collector.observability:4317` | OTLPエンドポイント |
| `OTEL_SERVICE_NAME` | `travel-helper-chNN` | サービス名（章ごとに異なる） |
| `LANGFUSE_HOST` | `http://langfuse-web.langfuse:3000` | Langfuseエンドポイント |
| `LANGFUSE_PUBLIC_KEY` | なし | Langfuse Public Key |
| `LANGFUSE_SECRET_KEY` | なし | Langfuse Secret Key |
| `LOG_LEVEL` | `INFO` | ログレベル |

機密情報（APIキー類）はKubernetes Secretとして管理し、Deploymentの `envFrom` で読み込む。Secretマニフェストは `sample-app/chNN/k8s/secret.example.yaml` として配置し、読者は実値を埋めた `secret.yaml` を作成する形とする。`.gitignore` で実値Secretはコミット対象外とする。

## 成功基準

- 全章のサンプルが `make deploy && make verify` で動作すること
- 読者が `make clean` 1コマンドで環境を元に戻せること
- 各章のREADMEに「この章で何が観測できるか」「どこをGrafana／Langfuseで確認するか」が明記されること
