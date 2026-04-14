# リポジトリ構造 (Repository Structure)

本書プロジェクトのディレクトリ構成と、各ディレクトリ・ファイルの役割を定義する。

## トップレベル構成

```
ai-o11y/
├── CLAUDE.md                    # プロジェクトメモリ（Claude Code向け）
├── Makefile                     # ビルド・検証・クリーンアップのエントリポイント
├── README.md                    # プロジェクト概要と利用手順
├── cleanup.sh                   # 全サンプルリソースの一括削除スクリプト
├── .steering/                   # 作業単位の仕様ドキュメント（/write-chapter等で生成）
├── .claude/                     # Claude Codeのエージェント・スキル定義
├── docs/                        # 永続ドキュメント（本書全体の設計）
├── manuscript/                  # 書籍本文（章ごとに分割）
├── sample-app/                  # サンプルコード（章ごとの状態を保存）
├── manifests/                   # Kubernetesマニフェスト（章横断）
└── collector-config/            # OTel Collector設定の章ごとのバリエーション
```

## `docs/` ― 永続ドキュメント

書籍全体の「何を書くか」「どう書くか」を定義する。

```
docs/
├── ideas/                       # 下書き・構想メモ
│   └── idea.md                  # 書籍コンセプトの原案
├── feedbacks/                   # レビューフィードバック
│   └── YYYY-MM-DD-chNN-*.md
├── book-plan.md                 # 書籍企画書
├── book-architecture.md         # 章間依存関係図
├── writing-guidelines.md        # 執筆ガイドライン
├── glossary.md                  # 用語集
├── figure-list.md               # 図表一覧（全章横断）
├── repository-structure.md      # 本ファイル
├── chapter-specs/               # 各章の仕様書
│   ├── ch01-spec.md
│   ├── ch02-spec.md
│   └── ...
└── sample-code-spec/            # サンプルコード仕様
    ├── ideas/
    │   └── app-concept.md       # サンプルアプリ構想
    ├── product-requirements.md  # 全体仕様
    ├── functional-design.md     # 機能設計
    ├── architecture.md          # アーキテクチャ設計
    └── development-guidelines.md # 開発ルール
```

## `manuscript/` ― 書籍本文

章ごとに分割して管理する。図表ソース（Mermaid）は章内のサブディレクトリに配置する。

```
manuscript/
├── ch01/
│   ├── ch01.md                  # 第1章本文
│   └── figures/                 # Mermaidソースファイル等
│       ├── fig1-1-3layer.mmd
│       └── ...
├── ch02/
│   └── ...
├── ...
├── ch17/
└── appendix/
    ├── appendixA.md             # 付録A クエリ言語チートシート
    ├── appendixB.md             # 付録B OTel Python SDK APIリファレンス
    └── appendixC.md             # 付録C 用語集（glossary.mdからの抜粋）
```

## `sample-app/` ― サンプルコード

同一のサンプルエージェントアプリを章ごとに発展させていく構成を取る。各章の最終状態を `chNN/` に保存し、読者はどの章からでも追試可能とする。

```
sample-app/
├── README.md                    # サンプルアプリ全体の説明・起動方法
├── common/                      # 章をまたいで共通の雛形
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── ch04/                        # 第4章: 最小Spanを送る状態
│   ├── agent.py
│   ├── k8s/
│   │   ├── namespace.yaml       # aio11y-book namespace
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── Makefile                 # make deploy / make verify / make clean
├── ch05/                        # 第5章: Metric/Log追加
├── ch13/                        # 第13章: 手動計装の完全版
├── ch14/                        # 第14章: OpenLLMetry追加
├── ch15/                        # 第15章: カスタムCollector設定
├── ch11/                        # 第11章: Langfuse SDK統合（評価付き）
└── ch17/                        # 第17章: 新メトリクス追加版（最終形）
```

### サンプルアプリの段階的発展

各章のディレクトリは独立して動作する（前章への依存なし）。ただし、コードの発展経路としては `ch04 → ch05 → ch13 → ch14 → ch15 → ch11 → ch17` の順に積み増していく。読者が一部の章のみを読んでも追試できることを優先する。

## `manifests/` ― 章横断のKubernetesマニフェスト

複数章で共有するマニフェスト（namespace、ServiceAccount、RBAC、ConfigMap等）を置く。章固有のマニフェストは `sample-app/chNN/k8s/` に置く。

```
manifests/
├── namespace.yaml               # aio11y-book namespace定義
├── rbac.yaml                    # サンプルアプリ用のServiceAccount/Role
└── kustomization.yaml           # 全章共通のベース
```

## `collector-config/` ― OTel Collector設定

第6章・第15章で扱うCollectorの設定を、章ごとのバリエーションとして保存する。既存の共有Collectorを直接変更せず、サイドカー or 新規Collectorを `aio11y-book` namespaceに立てる構成を基本とする。

```
collector-config/
├── README.md                    # 各設定の差分と使い分け
├── ch06-baseline/               # 第6章: 典型的な構成
│   └── config.yaml
├── ch15-add-langfuse/           # 第15章: Langfuse Exporter追加版
│   └── config.yaml
└── deploy/
    ├── collector-deployment.yaml  # aio11y-book用のCollector Pod定義
    └── Makefile
```

## `.steering/` ― 作業単位のドキュメント

執筆作業ごとに生成されるディレクトリ。`/write-chapter` 等のスラッシュコマンドが自動管理する。

```
.steering/
├── 20260415-ch01-writing/
│   ├── requirements.md          # 今回書く節・含めるトピック
│   ├── design.md                # 執筆アプローチ
│   └── tasklist.md              # タスクと進捗
└── 20260420-sample-code-agent/  # サンプルコード開発作業
```

## `Makefile` ― エントリポイント

リポジトリルートのMakefileで、章横断の操作を一元化する。

```makefile
# 書籍全体
.PHONY: setup clean

# 初期セットアップ（namespace作成、共通RBAC適用）
setup:
	kubectl apply -f manifests/namespace.yaml
	kubectl apply -f manifests/rbac.yaml

# 全サンプルリソースの削除
clean:
	./cleanup.sh

# 章単位のビルド・デプロイ・検証・クリーン
.PHONY: build-chNN deploy-chNN verify-chNN clean-chNN
# 各章のMakefileに委譲
```

各章の `sample-app/chNN/Makefile` には以下の標準ターゲットを設ける:

- `make build`: コンテナイメージのビルド（必要な場合）
- `make deploy`: マニフェスト適用
- `make verify`: 動作確認（Tempo/Prometheus/Loki/Langfuseでデータが見えるか）
- `make clean`: その章のリソース削除

ルートからは `make deploy-ch04` のように章番号を指定して委譲する形にする。

## `cleanup.sh` ― 一括クリーンアップ

本書で作成した全リソースを削除するスクリプト。読者が試し終わった後、環境を元の状態に戻せることを保証する。

```bash
#!/usr/bin/env bash
# 本書で作成した全リソースを削除する
# 対象: aio11y-book namespace内の全リソース、共有Collectorへの変更のロールバック
set -euo pipefail

NS=aio11y-book

# aio11y-book namespace を削除すれば、配下のリソースは全て消える
kubectl delete namespace "$NS" --ignore-not-found

# 共有Collectorに本書用設定を追加していた場合、ConfigMapだけは元に戻す手順を記載
# （本書では共有Collectorを直接変更しない方針のため、通常は不要）

echo "Cleanup completed."
```

## 命名規則のまとめ

| 対象 | 命名規則 | 例 |
|------|---------|-----|
| 章ディレクトリ | `chNN`（2桁ゼロ埋め） | `ch04` |
| 章本文ファイル | `chNN.md` | `ch04.md` |
| Mermaid図ソース | `figN-M-shortname.mmd` | `fig4-1-span-tree.mmd` |
| ステアリングディレクトリ | `YYYYMMDD-chNN-purpose` | `20260415-ch04-writing` |
| サンプルアプリnamespace | `aio11y-book`（全章共通） | `aio11y-book` |
| サンプルアプリDeployment | `ch<NN>-agent` | `ch04-agent` |
| Kubernetes Label | `book.aio11y/chapter=NN` | `book.aio11y/chapter=04` |

全リソースに `book.aio11y/owned-by=book` ラベルを付与し、ラベルセレクタでの一括削除も可能とする。

## 読者向けの利用フロー

読者は次の流れで本書のサンプルを追試する:

1. リポジトリをクローン
2. `make setup` で `aio11y-book` namespace作成
3. 各章で `cd sample-app/chNN && make deploy` を実行
4. Grafana／Langfuseで観測データを確認
5. 終了時に `make clean`（全削除）または `make clean-chNN`（章単位削除）を実行
