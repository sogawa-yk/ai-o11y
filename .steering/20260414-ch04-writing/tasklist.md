# 第4章 タスクリスト
- [x] サンプルコード構築・検証 (sample-app/ch04, k8s deploy, Tempo verified)
- [ ] 章導入
- [ ] 4.1 Attribute（図4.1）
- [ ] 4.2 Span（図4.2）
- [ ] 4.3 Trace（図4.3）
- [ ] 4.4 SpanContext（図4.4）
- [ ] 4.5 Context Propagation（図4.5）
- [ ] 4.6 Event（図4.6）
- [ ] 4.7 ハンズオン（図4.7、リスト4.1、4.2）
- [ ] まとめ・理解度チェック4問・参考文献・次章接続
- [ ] セルフレビュー

## 振り返り
- 完了日: 2026-04-14
- 申し送り（第5章以降）:
  - サンプルコードはConfigMap+pip-at-startup方式が有効。Dockerレジストリ不要で読者再現性も高い。第5章以降も踏襲する。
  - OTLP/SDK等の略語は本文初出時に必ず日本語（英語）展開する
  - 脚注URLは公式ドキュメントトップではなく具体ページに必ず合わせる
  - 第5章では3シグナル初出として「3シグナル（Three Signals）」併記、Metric/Counter/Histogram/Gauge/Logの初出展開を意識
  - クリーンアップを章ごとに必ず実行（共有環境への配慮）
