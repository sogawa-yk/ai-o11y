---
name: sample-code-verification
description: サンプルコード（アプリケーション、Kubernetesマニフェスト、Terraform、Dockerfile等）の構築・検証・クリーンアップに使用。/write-chapterのステップ5から呼び出される。スペック駆動開発（計画→実装ループ→検証→クリーンアップ）で自律的に実行する。
---

# サンプルコード検証スキル

サンプルコードをスペック駆動開発で構築・検証する。原稿に掲載するコード例は（疑似コードを除き）全てこのスキルを通じて動作検証済みであること。

## サンプルコードの種別

書籍で扱うサンプルコードは以下の種別に分類される。種別は`docs/book-plan.md`の技術環境セクションや`docs/sample-code-spec/`の構成から判定する。

| 種別 | 対象ファイル例 | 静的検証 | デプロイ検証 |
|---|---|---|---|
| `app` | アプリケーションコード | ユニットテスト、lint | デプロイ + E2Eテスト |
| `k8s` | Kubernetesマニフェスト | `kubectl dry-run --validate` | 実クラスタへの `kubectl apply` |
| `terraform` | Terraformファイル | `terraform validate` / `terraform plan` | `terraform apply` |
| `dockerfile` | Dockerfile, Compose | `docker build` / `docker compose config` | コンテナ起動テスト |

1つの章が複数の種別を含む場合がある（例: アプリケーション + Kubernetes マニフェスト + Dockerfile）。その場合は全ての種別について検証を実施する。

## 前提条件

1. `docs/sample-code-spec/` にサンプルコードの永続ドキュメントが存在すること（`/setup-book` で生成済み）
2. `docs/chapter-specs/chNN-spec.md` にサンプルコード要件セクションがあること

## 構成パターン

`docs/book-plan.md` の「サンプルコード構成」に以下のいずれかが記載されている:

### 章独立型

各章で独立したサンプルコードを使用する。

```
sample-code/chNN/    # 章ごとに独立したサンプルコード
```

- 各章のサンプルコードは相互に依存しない
- 検証・クリーンアップが章単位で完結する

### 累積型

1つのサンプルコードを章ごとに段階的に拡張する。

```
sample-code/          # 単一のサンプルコード
├── src/              # ソースコード（最新状態）
├── k8s/              # Kubernetesマニフェスト
├── terraform/        # Terraformファイル
├── tests/            # テストコード
└── ...
```

- Gitブランチで各章時点のスナップショットを管理: `sample-code/ch01`, `sample-code/ch02`, ...
- 章の執筆時は前章のブランチをベースに差分を適用する
- 各ブランチは「その章まで読み進めた読者が持つべきコード」の完全な状態を保持する

## スペック駆動開発による機能実装

サンプルコードの機能実装は、Galleyプロジェクトの `/add-feature` パターンを踏襲し、以下の手順で自律的に実行する。

### Phase 1: 計画

1. `docs/sample-code-spec/` の永続ドキュメントを読み、今回実装する機能の全体像を把握する
2. `docs/chapter-specs/chNN-spec.md` のサンプルコード要件セクションから、この章で必要な機能を特定する
3. ステアリングディレクトリ `.steering/[YYYYMMDD]-sample-code-[機能名]/` を作成する
4. `Skill('steering')` を**計画モード**で実行し、以下を生成する:

   **requirements.md** には以下を含める:
   - 概要: この機能で実現すること（1-2行）
   - 背景: この機能が読者に何を理解させるか
   - サンプルコードの種別: この章で扱う種別（app、k8s、terraform、dockerfile等）
   - 実装機能: 機能一覧（各機能と章のコード例との対応を明記）
   - 累積型の場合の差分: 前章からの追加・変更点
   - 使用技術: 言語、フレームワーク、ライブラリ、IaCツール
   - 受け入れ基準: チェックボックス形式の検証項目
   - スコープ外: この機能では扱わない項目
   - 参考資料: 章仕様書、`docs/sample-code-spec/` へのリンク

   **design.md** には以下を含める:
   - アーキテクチャ概要: ディレクトリ構成、コンポーネント図
   - 累積型の場合: 前章からの変更箇所のハイライト
   - データフロー: 主要ユースケースの処理フロー
   - テスト戦略: 種別ごとの検証方法（静的検証 + デプロイ検証）
   - 実装ステップ: 順序付きの実装手順
   - 原稿との対応: どの実装がどの節のコード例として掲載されるか

   **tasklist.md** には以下を含める:
   ```markdown
   # Phase 1: 実装
   - [ ] [機能1の実装]
   - [ ] [機能2の実装]

   # Phase 2: テスト
   - [ ] ユニットテスト作成・実行
   - [ ] E2Eテスト作成・実行

   # Phase 3: 静的検証
   - [ ] [種別に応じた静的検証]（例: kubectl dry-run、terraform validate等）

   # Phase 4: デプロイ・検証
   - [ ] 検証環境へデプロイ
   - [ ] sample-code-verifier による検証
   - [ ] スクリーンショット取得

   # Phase 5: スナップショット（累積型のみ）
   - [ ] ブランチ sample-code/chNN の作成

   # Phase 6: クリーンアップ
   - [ ] 検証環境のリソース削除

   ## 振り返り（完了後に記入）
   ```

### Phase 2: 実装ループ

1. `Skill('steering')` を**実装モード**で使用する
2. 既存のコードベースでパターン分析を行う（累積型の場合、前章のコードを参照）
3. tasklist.md の全タスクが `[x]` になるまで自律的に実装を継続する
4. タスクが大きすぎる場合はサブタスクに分割する
5. テストの作成・実行も tasklist.md に従って行う

### Phase 3: 静的検証

種別に応じた静的検証を実施する:

| 種別 | 静的検証コマンド |
|---|---|
| `app` | ユニットテスト、lint |
| `k8s` | `kubectl dry-run --validate -f [マニフェスト]` |
| `terraform` | `terraform init && terraform validate && terraform plan` |
| `dockerfile` | `docker build --no-cache -t test .` / `docker compose config` |

静的検証で問題が見つかった場合はコードを修正してから次のPhaseに進む。

### Phase 4: デプロイ・検証

1. 検証環境情報を確認する（`--env` 引数またはCLAUDE.mdの「検証環境」セクション）
2. **検証環境が指定されている場合**:
   - 種別に応じたデプロイを実行する:
     - `app`: アプリケーションをデプロイ
     - `k8s`: `kubectl apply -f [マニフェスト]`
     - `terraform`: `terraform apply`
     - `dockerfile`: `docker compose up -d` またはコンテナ起動
   - `sample-code-verifier` サブエージェントを起動して検証する:
     - `Task`ツール使用、`subagent_type`: "sample-code-verifier"
   - 検証に失敗した場合はコードを修正して再デプロイ（最大3回リトライ）
3. **検証環境が指定されていない場合**:
   - Phase 3の静的検証のみ実行する

### Phase 5: 結果の反映

1. 検証に成功した場合:
   - 動作確認済みのコードを原稿に含める準備をする
   - スクリーンショットがあれば `manuscript/chNN/figures/` に配置する
2. 累積型の場合:
   - 検証済みコードをブランチ `sample-code/chNN` として保存する

### Phase 6: クリーンアップ・振り返り

1. 検証環境のリソースを削除する（種別に応じて）:
   - `app`: アプリケーションの停止・削除
   - `k8s`: `kubectl delete -f [マニフェスト]`
   - `terraform`: `terraform destroy`
   - `dockerfile`: `docker compose down` / コンテナ停止・削除
2. `Skill('steering')` を**振り返りモード**で実行する

## コード例と動作検証の原則

**原稿に掲載するコード例は、概念的な説明（疑似コード）を除き、全て動作検証済みであること。**

- サンプルコードの一部として実行可能なコードは、必ずこのスキルを通じて検証する
- 検証環境が未設定の場合は静的検証（構文チェック、ベストプラクティス確認）で代替する
- 疑似コードには明示的に「疑似コード」であることをコードブロック内のコメントで示す

## 出力

- 検証の結果レポート（成功/失敗、種別ごとの検証結果、スクリーンショットのパス等）
- 累積型の場合: 作成されたブランチ名
- ステアリングファイル（`.steering/YYYYMMDD-sample-code-[機能名]/`）
