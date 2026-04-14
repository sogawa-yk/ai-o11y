# 第6章 レビュー結果

## 構成・文体（4.5/5）
- 軽微な指摘のみ。仕様遵守。

## 技術検証（10/14 正確）
- 要修正: `reload` シグナル記述（標準提供されず誤解の恐れ）
- 要確認: lokiexporterのdeprecated（補足推奨）、batch/extensions（任意）

## 情報ソース
- [^1] URLを contrib receivers ディレクトリに差し替え
- [^2] URLを contrib processors ディレクトリに差し替え
- [^4] 削除（reload文削除と連動）

## サンプルコード（条件付き合格）
- config.yamlの `debug` exporter削除（リスト6.1と一致させる）

## 理解度・Mermaid
- 修正不要

---

## 対応結果
- 対応日: 2026-04-14
- 修正:
  1. config.yamlから `debug` exporter削除
  2. 6.6節「`reload` シグナルで再読込に対応するバージョンもある」を削除し「Pod再起動による反映」に簡素化
  3. [^4]削除、参考文献から該当行削除
  4. [^1] を contrib/receiver ディレクトリへ
  5. [^2] を contrib/processor ディレクトリへ
  6. 表6.1 loki行に「（近年は `otlphttp` + Loki OTLPエンドポイント利用も一般的）」追記
