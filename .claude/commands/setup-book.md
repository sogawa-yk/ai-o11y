---
description: "初回セットアップ: 永続ドキュメントをideas/book-concept.mdを元に作成する"
---

# 初回書籍セットアップ

このコマンドは、書籍プロジェクトの永続ドキュメントを対話的に作成します。

**引数（任意）:** `--pages [ページ数]` で書籍全体の想定ページ数を指定できます。

## 実行方法

```bash
claude
> /setup-book
> /setup-book --pages 200
```

## 実行前の確認

`docs/ideas/` ディレクトリ内のファイルを確認します。

```
# 確認
ls docs/ideas/

# ファイルが存在する場合
✅ docs/ideas/book-concept.md が見つかりました
   この内容を元に書籍企画書を作成します

# ファイルが存在しない場合
⚠️  docs/ideas/ にファイルがありません
   対話形式で書籍企画書を作成します
```

## 手順

### ステップ0: インプットの読み込み

1. `docs/ideas/` 内のマークダウンファイルを全て読む
2. 内容を理解し、書籍企画書作成の参考にする

### ステップ1: 分量（ページ数）の解決

書籍の分量を以下の優先順位で確定する。**企画書作成前に必ず分量を確定させること。**

**優先順位1: アイデアファイルの記述（最優先）**

ステップ0で読み込んだ `docs/ideas/` 内のファイルに、分量に関する記述があるか確認する。以下のような表現を含む場合、その値を採用する:
- 直接的な表現: 「200ページ」「200p」「全200頁」
- 文字数での指定: 「10万字程度」→ ページ数に換算
- 章数×ページ数: 「全8章、各章20ページ」→ 合計160ページ
- 間接的な表現: 「薄い本で50ページくらい」「同人誌サイズ」等

**優先順位2: `--pages` パラメータ**

アイデアファイルに分量の記述がなく、コマンド実行時に `--pages N` が指定されている場合、その値を採用する。

**優先順位3: ユーザーへの確認（フォールバック）**

アイデアファイルにもパラメータにも分量の指定がない場合、**必ずユーザーに確認する**:

```
「書籍の想定ページ数が指定されていません。
おおよその想定ページ数を教えてください（例: 200）。
ページ数以外の表現（例: 10万字、全8章×各20ページ）でも構いません。」
```

**ユーザーから回答を得るまで次のステップに進まないこと。**

### ステップ2: 書籍企画書の作成

1. **book-planningスキル**をロード
2. `docs/ideas/book-concept.md`の内容と、**ステップ1で確定した分量**を元に`docs/book-plan.md`を作成
3. コンセプトドキュメントを具体化：
   - 対象読者の詳細化
   - 到達目標の明確化
   - 全体構成とページ配分（**確定した分量に基づく**）
   - 執筆方針
   - スコープ外の明示
4. ユーザーに確認を求め、**承認されるまで待機**

**以降のステップはbook-plan.mdの内容を元にするため、自動的に作成する**

### ステップ3: 書籍構成・依存関係の作成

1. `docs/book-plan.md`を読む
2. 章間の依存関係（前提知識の関係）を整理
3. `docs/book-architecture.md`を作成

### ステップ4: 執筆ガイドラインの作成

1. **writing-guidelinesスキル**をロード
2. 既存のドキュメントを読む
3. `docs/writing-guidelines.md`を作成

### ステップ5: 用語集の作成

1. **glossary-creationスキル**をロード
2. book-concept.mdとbook-plan.mdから用語を抽出
3. `docs/glossary.md`を作成

### ステップ6: リポジトリ構造定義書の作成

1. 既存のドキュメントを読む
2. `docs/repository-structure.md`を作成

### ステップ7: サンプルコード仕様の作成（該当する場合）

`docs/book-plan.md` にサンプルコード（アプリケーション、Kubernetesマニフェスト、Terraformファイル等）の記述がある場合のみ実行する。記述がない場合はスキップ。

1. `docs/ideas/book-concept.md` からサンプルコードの構想を抽出する
2. `docs/sample-code-spec/ideas/app-concept.md` に書き出す
3. `app-concept.md` を参照しながら、以下の永続ドキュメントを生成する:
   - `docs/sample-code-spec/product-requirements.md` — 全体仕様、章ごとの機能一覧
   - `docs/sample-code-spec/functional-design.md` — 機能設計
   - `docs/sample-code-spec/architecture.md` — アーキテクチャ設計
   - `docs/sample-code-spec/development-guidelines.md` — 開発ルール
4. 各ドキュメントは1ファイルずつ作成し、ユーザーの承認を得てから次に進む

### ステップ8: 各章の仕様書を作成

1. **chapter-spec-writingスキル**をロード
2. `docs/book-plan.md`の全体構成に基づき、全章の仕様書を作成
3. 各仕様書を`docs/chapter-specs/chNN-spec.md`に保存
4. 仕様書には以下を含める：
   - 章の目的
   - 前提知識（依存する章）
   - 節の構成
   - 図表リスト
   - 章末の理解度チェック問題の方針
   - 前の章からの接続方法
   - 次の章への接続方法
   - 目標ページ数
   - **サンプルコード要件**（該当する場合）: この章で実装・掲載するサンプルコードの機能と種別（app、k8s、terraform、dockerfile等）、原稿のどの節で使用するか

### ステップ9: 図表一覧の作成

1. 全章の仕様書から図表情報を集約
2. `docs/figure-list.md`を作成

## 完了条件

- 全ての永続ドキュメントが作成されていること

完了時のメッセージ:
```
「初回セットアップが完了しました!

作成したドキュメント:
✅ docs/book-plan.md
✅ docs/book-architecture.md
✅ docs/writing-guidelines.md
✅ docs/glossary.md
✅ docs/repository-structure.md
✅ docs/chapter-specs/ch01-spec.md 〜 chNN-spec.md
✅ docs/figure-list.md
✅ docs/sample-code-spec/ （サンプルコードがある場合）

これで執筆を開始する準備が整いました。

今後の使い方:
- 章の執筆: /write-chapter [章番号]
  例: /write-chapter 1

- 章の執筆（検証環境指定）: /write-chapter [章番号] --env [環境名]
  例: /write-chapter 1 --env local

- 全章一括執筆: /write-all
  例: /write-all --env staging

- 章のレビュー: /review-chapter [章番号]
  例: /review-chapter 4

- ドキュメントの編集: 普通に会話で依頼してください
  例: 「用語集に新しい用語の定義を追加して」
」
```
