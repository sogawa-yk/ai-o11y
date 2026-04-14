# 付録B OTel Python SDK APIリファレンス ― 仕様書

## 章の概要

**章の目的**: 本書で扱ったOTel Python SDKの主要APIを早見表にまとめる。初期化テンプレートと関数シグネチャを集約する。

**目標ページ数**: 6p

**所属する部**: 付録

## 前提知識

- 第13章（Python OTel SDK手動計装）

## 節の構成

### B.1 初期化テンプレート

**概要**: TracerProvider／MeterProvider／LoggerProviderの初期化をコピペで使える形で提示する。

**図表**:
- リストB.1: 最小初期化テンプレート（OTLPエンドポイント1本に3シグナル送信）

### B.2 Tracer API早見表

**概要**: Span生成・Attribute付与・Status・Exception・Event記録のAPI一覧。

**図表**:
- 表B.1: Tracer関連API早見表

### B.3 Meter API早見表

**概要**: Counter／Histogram／Gaugeの作成と記録のAPI一覧。

**図表**:
- 表B.2: Meter関連API早見表

### B.4 Logging統合の早見

**概要**: LoggingInstrumentorの初期化オプションとSpanContext紐付けの使い方。

**図表**:
- リストB.2: logging統合の初期化

### B.5 OpenLLMetry初期化の早見

**概要**: Traceloop.init()の主要オプションを1枚にまとめる。

**図表**:
- 表B.3: Traceloop.init()オプション一覧
- リストB.3: 本書で使う構成のTraceloop初期化

## 図表リスト

| 図表番号 | タイトル | 種類 | 所属する節 |
|---------|---------|------|----------|
| リストB.1 | 最小初期化テンプレート | Python | B.1 |
| 表B.1 | Tracer API早見表 | 表 | B.2 |
| 表B.2 | Meter API早見表 | 表 | B.3 |
| リストB.2 | logging統合初期化 | Python | B.4 |
| 表B.3 | Traceloop.init()オプション | 表 | B.5 |
| リストB.3 | Traceloop初期化例 | Python | B.5 |

## コード例

| リスト | 内容 | 言語 | 所属する節 |
|-------|------|------|----------|
| リストB.1 | 最小初期化（本書の `otel_setup.py` を簡略化） | Python | B.1 |
| リストB.2 | logging統合初期化 | Python | B.4 |
| リストB.3 | Traceloop初期化 | Python | B.5 |

## サンプルコード要件

掲載コードは本書の `sample-app/` で動作検証済みのものを使用する。

## 章末の理解度チェック問題

付録のため問題は設けない。

## 章間の接続

### 前の章からの接続
- **前章の最後**: 付録A（クエリ言語チートシート）
- **この章の導入**: 「OTel Python SDKの主要APIを1箇所に集約する」

### 次の章への接続
- **この章の結び**: 付録C（用語集の抜粋）に進む
- **接続のキーフレーズ**: 「用語の確認に戻れる」
