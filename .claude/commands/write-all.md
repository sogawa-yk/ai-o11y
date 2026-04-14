---
description: 全章を一括で執筆・レビュー・修正・コミットする
---

# 全章一括執筆 (中断再開対応)

**重要:** このワークフローは、`docs/book-plan.md`に定義された全章を自動で執筆・レビュー・修正・コミットします。レートリミット等で中断されても、再実行時に続きから再開します。

**引数:** なし (例: `/write-all`)

**オプション引数:** `--env [環境名]` で検証環境を指定 (例: `/write-all --env local`)

---

## ステップ1: 進捗ファイルの確認と初期化

1. `.steering/book-progress.json` の存在を確認する。

2. **ファイルが存在する場合（再開モード）**:
   - ファイルを読み込み、各章の進捗状態を把握する。
   - ユーザーに現在の進捗を報告する:
     ```
     「進捗ファイルを検出しました。中断された地点から再開します。
     完了済み: 第1章〜第3章
     中断地点: 第4章（レビュー修正中）
     未着手: 第5章〜第N章」
     ```
   - 中断された章から再開する。中断時のステップも記録されているため、そのステップから再開する。

3. **ファイルが存在しない場合（新規開始）**:
   - `docs/book-plan.md` を読み、書籍の総章数を確認する。
   - 以下の形式で `.steering/book-progress.json` を作成する（章数は `book-plan.md` に基づく）:

   ```json
   {
     "started_at": "YYYY-MM-DDTHH:MM:SS",
     "total_chapters": N,
     "chapters": {
       "01": { "status": "pending", "step": null, "completed_at": null },
       "02": { "status": "pending", "step": null, "completed_at": null },
       ...
       "NN": { "status": "pending", "step": null, "completed_at": null }
     }
   }
   ```

4. **サンプルコードの検証環境を確認する**:
   - `docs/sample-code-spec/` が存在するか確認する
   - 存在する場合、`--env` 引数が指定されているか確認する
   - 指定されていない場合、**ユーザーに確認する**:
     ```
     「サンプルコード（アプリケーション、マニフェスト、IaCファイル等）を含む書籍です。
     検証環境を指定してください（例: local, staging）。
     静的検証のみで進める場合は「なし」と入力してください。」
     ```
   - ユーザーから回答を得るまで次に進まないこと。

5. 第1章（または再開対象の章）からステップ2へ進む。

## ステップ2: 章ループ（全章完了まで繰り返す）

**以下を第1章〜最終章で繰り返す。各章で4つのサブステップ（執筆→レビュー→修正→コミット）を実行する。**

---

### サブステップA: 執筆

1. 進捗ファイルを更新する:
   ```json
   { "status": "writing", "step": "writing" }
   ```

2. `/write-chapter [章番号] --env [環境名]` と同等の処理を実行する:
   - ステップ1〜9（準備、プロジェクト理解、前後の章確認、計画、**サンプルコード構築・検証**、執筆ループ、品質チェック、修正反映、振り返り）を全て実行する。
   - 検証環境はステップ1で確認した `--env` 引数を引き継ぐ（ステップ5で再確認しない）。
   - **ただし**、`/write-chapter`内のサブエージェントによる品質チェック（ステップ7-8）はここでは**スキップ**する。次のサブステップBで実施する。

3. 執筆が完了したら進捗ファイルを更新する:
   ```json
   { "status": "writing_done", "step": "writing_done" }
   ```

---

### サブステップB: レビュー

1. 進捗ファイルを更新する:
   ```json
   { "status": "reviewing", "step": "reviewing" }
   ```

2. `/review-chapter [章番号]` と同等の処理を実行する:
   - chapter-reviewerサブエージェントを起動
   - 7つの観点（仕様整合性、用語統一、文体表記、章間整合性、技術正確性、図表品質、理解度チェック）でレビュー

3. **技術検証エージェントを起動する**:
   - `Task`ツールを使用し、`tech-verifier`サブエージェントを起動する。
   - `subagent_type`: "tech-verifier"
   - `description`: "Technical accuracy verification with web search"
   - `prompt`:
     ```
     あなたは技術検証エージェントです。以下の原稿に含まれる技術的な記述の正確性を、ウェブ検索を使って検証してください。

     対象原稿: manuscript/ch[章番号]/ch[章番号].md

     検証手順:
     1. 原稿を読み、技術的な主張・記述を抽出する（API仕様、サービス名、パラメータ、プロトコルの仕様、パターンの定義、バージョン情報等）
     2. 抽出した各主張について、web_searchツールで公式ドキュメントや信頼できるソースを検索する
     3. 原稿の記述とソースを照合し、不一致や古い情報を特定する

     特に以下を重点的に検証すること:
     - 書籍で扱う主要サービス/プロダクトの仕様（docs/book-plan.mdの技術スタックに基づく）
     - 関連サービス・ツールの仕様
     - 書籍で扱うプロトコル・標準の仕様と現在のステータス
     - 書籍で扱うフレームワーク・ライブラリの最新情報
     - 書籍で扱うIaCツール・プロバイダーの仕様（該当する場合）

     出力形式:
     検証した主張ごとに以下の形式で報告すること:

     ### [検証項目]
     - **原稿の記述**: [原稿に書かれている内容]
     - **検索結果**: [web_searchで確認した内容とソースURL]
     - **判定**: 正確 / 要修正 / 要確認（ソースが見つからない場合）
     - **修正案**（要修正の場合）: [正しい記述]
     ```
   - このサブエージェントには `web_search` ツールの使用を許可する。

4. **情報ソース検証エージェントを起動する**:
   - `Task`ツールを使用し、`citation-verifier`サブエージェントを起動する。
   - `subagent_type`: "citation-verifier"
   - 「一般的には〜」等の主張に情報ソースが付いているかを確認し、付いている場合はweb_searchでソースの内容を検証する。
   - 詳細なプロンプトは `/review-chapter` のステップ4を参照。

5. **理解度チェック問題フォーマット検証エージェントを起動する**:
   - `Task`ツールを使用し、`quiz-format-checker`サブエージェントを起動する。
   - `subagent_type`: "quiz-format-checker"
   - 章末の理解度チェック問題が共通フォーマットに準拠しているかを検証する。
   - 詳細なプロンプトは `/review-chapter` のステップ5を参照。

6. **Mermaid構文検証エージェントを起動する**:
   - `Task`ツールを使用し、`mermaid-syntax-checker`サブエージェントを起動する。
   - `subagent_type`: "mermaid-syntax-checker"
   - `description`: "Mermaid syntax and style validation"
   - 原稿内のMermaidブロックの構文エラーと配色ルール準拠を検証する。
   - 詳細なプロンプトは `/review-chapter` のステップ6を参照。

7. 全エージェント（chapter-reviewer, tech-verifier, citation-verifier, quiz-format-checker, mermaid-syntax-checker）の結果を統合し、`docs/feedbacks/ch[章番号]-review.md` に保存する。
   - ファイルは以下の構造とする:
     ```markdown
     # 第[章番号]章 レビュー結果

     ## 構成・文体レビュー
     [chapter-reviewerの結果]

     ## 技術検証レビュー
     [tech-verifierの結果]

     ## 情報ソース検証
     [citation-verifierの結果]

     ## 理解度チェック問題フォーマット検証
     [quiz-format-checkerの結果]

     ## Mermaid構文検証
     [mermaid-syntax-checkerの結果]
     ```

8. 進捗ファイルを更新する:
   ```json
   { "status": "reviewed", "step": "reviewed" }
   ```

---

### サブステップC: レビュー修正

1. 進捗ファイルを更新する:
   ```json
   { "status": "fixing", "step": "fixing" }
   ```

2. `docs/feedbacks/ch[章番号]-review.md` のレビュー結果を読み込む。

3. 指摘事項がある場合:
   - 指摘事項を修正タスクに分解する。
   - 原稿（`manuscript/ch[章番号]/ch[章番号].md`）を直接修正する。
   - 用語や図表の問題があれば `docs/glossary.md` や `docs/figure-list.md` も修正する。
   - 修正内容をフィードバックファイルの末尾に追記する:
     ```markdown
     ---
     ## 対応結果
     - **対応日**: [日付]
     - **修正内容**: [修正の要約]
     ```

4. 指摘事項がない場合: そのまま次へ。

5. 進捗ファイルを更新する:
   ```json
   { "status": "fixed", "step": "fixed" }
   ```

---

### サブステップD: コミット＆プッシュ

1. 進捗ファイルを更新する:
   ```json
   { "status": "committing", "step": "committing" }
   ```

2. 以下のgitコマンドを実行する:
   ```bash
   git add manuscript/ch[章番号]/ docs/ .steering/
   git commit -m "第[章番号]章 執筆完了"
   git push origin main
   ```

3. pushが失敗した場合（認証エラー、ネットワークエラー等）:
   - commitは維持する（ローカルには残る）。
   - エラーをログに記録し、次の章に進む。
   - 進捗ファイルには `"push_failed": true` を追記する。

4. 進捗ファイルを更新する:
   ```json
   { "status": "done", "step": "done", "completed_at": "2026-03-05T12:34:56" }
   ```

5. **次の章へ**: 章番号をインクリメントし、サブステップAに戻る。

---

## ステップ3: 全章完了

全章が `"status": "done"` になったら:

1. 最終的な進捗を報告する:
   ```
   「全N章の執筆・レビュー・修正・コミットが完了しました。

   各章の完了時刻:
   第1章: YYYY-MM-DDTHH:MM:SS
   第2章: YYYY-MM-DDTHH:MM:SS
   ...
   第N章: YYYY-MM-DDTHH:MM:SS

   push失敗の章: [あれば列挙]
   ```

2. push失敗の章がある場合、手動でのpushを促す:
   ```
   「以下の章はpushに失敗しています。手動で `git push origin main` を実行してください。」
   ```

---

## 中断時の再開ロジック

レートリミットやセッション切断で中断された場合、`/write-all` を再実行すると:

1. `.steering/book-progress.json` を読み込む。
2. 各章のstatusを確認する:

   | status | 再開時の動作 |
   |--------|-------------|
   | `pending` | サブステップAから開始 |
   | `writing` | サブステップAを最初からやり直す（冪等性のため） |
   | `writing_done` | サブステップBから開始 |
   | `reviewing` | サブステップBを最初からやり直す |
   | `reviewed` | サブステップCから開始 |
   | `fixing` | サブステップCを最初からやり直す |
   | `fixed` | サブステップDから開始 |
   | `committing` | サブステップDを最初からやり直す |
   | `done` | スキップ（次の章へ） |

3. 最初の `"done"` でない章を見つけ、対応するサブステップから再開する。

---

## 例外処理ルール

### レートリミットエラー
- 処理中にレートリミットに達した場合、現在の章のステップまでの進捗は保存済み。
- 再実行で続きから再開される。

### git操作の失敗
- commit失敗: リトライ1回。それでも失敗なら進捗を `"commit_failed": true` にして次の章へ。
- push失敗: 進捗を `"push_failed": true` にして次の章へ。commitはローカルに残る。

### 執筆・レビューの失敗
- 原則としてリトライせず、エラー内容を進捗ファイルに記録して次の章に進む。
- 進捗を `"status": "error", "error": "[エラー内容]"` にする。
- 全章完了後にエラーの章を報告する。

---

## 完了条件

このワークフローは、以下の条件を満たした時点で完了となる:
- 全章の `status` が `done` または `error` になっている。
- 完了レポートがユーザーに表示されている。
- `error` の章がある場合、その一覧がユーザーに報告されている。
