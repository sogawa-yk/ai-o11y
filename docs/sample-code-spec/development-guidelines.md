# サンプルアプリ開発ガイドライン (Development Guidelines)

`travel-helper` の実装・検証・更新時のルールを定義する。執筆時に `sample-code-verification` スキルが参照する基準となる。

## 開発原則

### 最小主義
- 各章のサンプルコードは、その章のテーマを実証するのに必要な最小限に絞る
- 「いつか使うかもしれない」機能は入れない
- 章をまたいで共通化したくなったら、その時点で `sample-app/common/` に抽出する

### 実機検証の絶対性
- 原稿に掲載する全てのコード・マニフェスト・Collector設定は、本プロジェクトがアクセス可能なKubernetesクラスタ（`context-c7lwigzhjea`）で実際に動作させる
- 動作確認なしでコード例を原稿に載せない
- 疑似コードを示す場合は冒頭に `# 疑似コード（動作検証対象外）` と明記

### 独立性
- 各章の `sample-app/chNN/` は単独で動作可能とする
- 前章への依存（コード・リソース・状態）は持たない
- 読者が任意の章から試せる

## Python関連

### バージョン
- Python 3.11以上
- 実機検証環境のPythonバージョンは `sample-app/common/.python-version` に記録

### 依存管理
- `requirements.txt` でバージョン固定
- 各章で `requirements.txt` をコピーして章固有の依存を追記（重複を許容する）
- 本書全体で固定するキーライブラリのバージョン目安:

| ライブラリ | バージョン目安 | 備考 |
|----------|--------------|------|
| `opentelemetry-api` | 1.x系最新 | Traces／Metrics／Logs API |
| `opentelemetry-sdk` | 上に合わせる | |
| `opentelemetry-exporter-otlp` | 同上 | gRPC版 |
| `opentelemetry-instrumentation-logging` | 対応最新 | ログへのtrace_id付与 |
| `opentelemetry-instrumentation-fastapi` | 対応最新 | FastAPI自動計装（ch05から使用） |
| `traceloop-sdk` | 最新 | OpenLLMetry |
| `langfuse` | 3.x系 | Python SDK |
| `openai` | 1.x系 | OCI GenAI互換クライアント |
| `fastapi` | 0.11x系 | Webフレームワーク |
| `uvicorn` | 最新 | ASGIサーバ |
| `pydantic` | 2.x系 | 入出力スキーマ |

確定版は実機検証の際に `pip freeze` から抽出して章ごとに固定する。

### コーディング規約
- フォーマッタ: `ruff format`
- リンタ: `ruff check`
- 型チェック: `mypy --strict`（ベストエフォート、実行時エラーとはしない）
- 命名規則: PEP8
- docstringは短く（1行で十分）。詳細は書籍本文に書く

### 構造化
- FastAPIアプリはモジュール化せず、単一ファイル `agent.py` に収める（章のコード量を抑えるため）
- LLM／ツール／設定は別ファイル（`llm.py` `tools.py` `config.py`）
- OTel初期化は `otel_setup.py` に隔離

## OTel計装のルール

### Span命名
- ドットで階層を表現する（`stage.plan`、`tool.weather`）
- 変数を含めない（`tool.weather_kyoto` はNG、`tool.weather` に `tool.city=kyoto` Attributeを付ける）

### Attribute命名
- スネークケース＋ドット階層（`user.city`、`stage.investigation_items_count`）
- LLM関連は GenAI Semantic Conventions に準拠（`gen_ai.request.model` 等）
- カスタム属性の名前空間プレフィックスは `travel_helper.`

### エラー処理
- Span内で例外発生時は必ず以下を行う:
  1. `span.record_exception(exc)`
  2. `span.set_status(Status(StatusCode.ERROR, str(exc)))`
  3. 必要に応じてre-raise（呼び出し元のSpanにも伝播させたい場合）
- `ToolError` は記録するがユーザー応答は200 OKで返す（ツールエラーはリクエスト失敗にしない設計）

### OpenLLMetry（ch14以降）
- `Traceloop.init(app_name=..., disable_batch=False)` で初期化
- プロンプト／レスポンスのキャプチャは環境変数 `TRACELOOP_TRACE_CONTENT=true` で有効化
- デフォルトではキャプチャ無効（プライバシー考慮）。本書検証時は有効にしてTempoで内容が見えることを確認

## Kubernetesマニフェストのルール

### 共通
- 全マニフェストに以下のラベルを付与:
  ```yaml
  labels:
    app.kubernetes.io/name: travel-helper
    app.kubernetes.io/part-of: aio11y-book
    book.aio11y/owned-by: book
    book.aio11y/chapter: "NN"
  ```
- namespace指定は必ず `aio11y-book`
- `kustomize` は使わず素のYAMLで配布（読者の学習コスト低減）
- apiVersionは固定の安定版を使用

### リソース命名
- Deployment: `chNN-agent`（例: `ch04-agent`）
- Service: `travel-helper-chNN`
- ConfigMap: `travel-helper-chNN-config`
- Secret: `travel-helper-chNN-secret`

### Secret
- 実値は `.gitignore` 対象
- テンプレート `secret.example.yaml` は平文で配布（ダミー値）
- 読者は以下のコマンドで実Secret作成:
  ```bash
  cp secret.example.yaml secret.yaml
  # secret.yaml を編集
  kubectl apply -f secret.yaml
  ```

## Makefileのルール

### 章Makefileの標準ターゲット
各章 `sample-app/chNN/Makefile` に以下を必ず用意する:

```makefile
CHAPTER := NN
NS := aio11y-book
LABEL := book.aio11y/chapter=$(CHAPTER)

.PHONY: build deploy verify clean

build:
	docker build -t travel-helper:ch$(CHAPTER) .

deploy:
	kubectl apply -f k8s/ -n $(NS)
	kubectl rollout status deployment/ch$(CHAPTER)-agent -n $(NS) --timeout=120s

verify:
	./scripts/verify.sh

clean:
	kubectl delete -l $(LABEL) -n $(NS) deployment,service,configmap,secret --ignore-not-found
```

### ルートMakefile
```makefile
.PHONY: setup clean clean-ch%
setup:
	kubectl apply -f manifests/namespace.yaml
	kubectl apply -f manifests/rbac.yaml

clean:
	./cleanup.sh

clean-ch%:
	$(MAKE) -C sample-app/ch$* clean
```

## 検証（verify）スクリプト

各章に `scripts/verify.sh` を置き、以下を検証する:
1. Podが Running 状態である
2. `/plan` にリクエストを投げて200 OKが返る
3. レスポンスに `trace_id` が含まれる
4. （該当章では）Tempo／Prometheus／Loki／Langfuse でデータが観測可能である

`verify.sh` の終了コード0で成功、それ以外で失敗とする。

## 検証環境と検証手順

### 接続情報
- kubectl context: `context-c7lwigzhjea`
- 稼働確認済みの共有スタック:
  - `observability/otel-gateway-opentelemetry-collector`
  - `observability/prometheus-*`
  - `observability/tempo-0`
  - `observability/loki-0`
  - `observability/prometheus-grafana-*`
  - `langfuse/langfuse-web`

### 検証の流れ
1. `make setup` で namespace・RBAC を適用
2. `cd sample-app/chNN && make build` でイメージビルド
3. `make deploy` でマニフェスト適用
4. `make verify` で動作確認
5. Grafana／Langfuseでデータ目視確認
6. 問題なければその章の `sample-app/chNN/` をコミット
7. 検証完了後 `make clean-chNN` で掃除

## 変更追従のルール

### SDKバージョンアップ時
- `requirements.txt` を更新したら全章で `make verify` を再実行
- 破壊的変更があれば該当章のコードを修正し、本文も更新

### Kubernetesバージョン依存
- apiVersionは検証環境で動くものを使用
- 検証環境のKubernetesバージョンは `docs/sample-code-spec/architecture.md` に追記する（検証時に確認）

## ドキュメント連携

- サンプルコードの重要な決定事項（例: 「OCI GenAIのモデルXを使う」「OpenLLMetryバージョンYで固定」）は本文ではなく本ガイドラインに記録する
- 本文は「本ガイドラインで定めた構成に従う」と参照する
- 本ガイドラインと本文の記述が矛盾した場合、本ガイドラインを優先して本文を修正する

## 禁止事項

- `latest` タグの使用
- `default` namespaceへのデプロイ
- 既存の `observability` `langfuse` namespaceのリソースの直接編集
- 認証情報のリポジトリへのコミット
- 読者が追試できない環境固有のハードコード（具体的なpodIPやOCIDの直書き等）
- 動作未検証のコード例を原稿に載せること
