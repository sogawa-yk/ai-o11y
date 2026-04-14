# 付録B OTel Python SDK APIリファレンス

本付録では、本書で扱ったOpenTelemetry（以下OTel）Python SDKの主要APIを早見表として集約する。初期化テンプレートと関数シグネチャ、本書サンプルで使う典型パターンを1箇所に集めた。実務中に開いて参照する用途を想定している。

## B.1 初期化テンプレート

OTLPエンドポイント1本で3シグナル（Traces／Metrics／Logs）をまとめて送る最小構成をリストB.1に示す。本書の `sample-app/ch13/otel_setup.py` を簡略化したものに相当する。

**リストB.1: 最小初期化テンプレート（`sample-app/ch13/otel_setup.py` 相当）**

```python
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import logging

def init_otel(service_name: str, endpoint: str):
    resource = Resource.create({"service.name": service_name})

    tp = TracerProvider(resource=resource)
    tp.add_span_processor(BatchSpanProcessor(
        OTLPSpanExporter(endpoint=endpoint, insecure=True)))
    trace.set_tracer_provider(tp)

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=endpoint, insecure=True),
        export_interval_millis=10_000)
    mp = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(mp)

    lp = LoggerProvider(resource=resource)
    lp.add_log_record_processor(BatchLogRecordProcessor(
        OTLPLogExporter(endpoint=endpoint, insecure=True)))
    set_logger_provider(lp)
    logging.getLogger().addHandler(
        LoggingHandler(level=logging.NOTSET, logger_provider=lp))

    return trace.get_tracer(service_name), metrics.get_meter(service_name)
```

注意: Logs SDKのインポートパスは `opentelemetry.sdk._logs`（アンダースコア付き）である。APIとSDKでStableステータスは異なるため、手元のパッケージバージョンで確認する。

## B.2 Tracer API早見表

*表B.1: Tracer関連APIの主要メソッド*

| メソッド／属性 | 用途 | 使用例 |
|-------------|------|--------|
| `trace.get_tracer(name)` | Tracer取得 | `tracer = trace.get_tracer("app")` |
| `tracer.start_as_current_span(name)` | Span生成＋現在のSpanとして登録 | `with tracer.start_as_current_span("stage.plan") as span: ...` |
| `tracer.start_span(name, context=...)` | Span生成のみ（現在に設定しない） | 非同期タスクで親を明示する場合 |
| `span.set_attribute(key, value)` | 単一Attribute追加 | `span.set_attribute("user.city", "kyoto")` |
| `span.set_attributes(dict)` | 複数Attribute一括 | `span.set_attributes({"user.city":"kyoto", "user.days":2})` |
| `span.add_event(name, attributes={})` | Eventの追加 | `span.add_event("cache.miss", {"key":"foo"})` |
| `span.set_status(Status(StatusCode.ERROR, msg))` | ステータス設定 | エラー時に必須 |
| `span.record_exception(exc)` | 例外をSpanに記録 | `except` ブロックで呼ぶ |
| `span.get_span_context().trace_id` | Trace ID（int 128bit） | `format(id, "032x")` でhex化 |
| `span.get_span_context().span_id` | Span ID（int 64bit） | `format(id, "016x")` でhex化 |

例外処理の定型パターン:

```python
with tracer.start_as_current_span("op") as span:
    try:
        do_work()
    except Exception as exc:
        span.record_exception(exc)
        span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
        raise
```

## B.3 Meter API早見表

*表B.2: Meter関連APIの主要メソッド*

| メソッド | 用途 | 使用例 |
|---------|------|--------|
| `metrics.get_meter(name)` | Meter取得 | `meter = metrics.get_meter("app")` |
| `meter.create_counter(name, unit="", description="")` | Counter作成 | `c = meter.create_counter("app.requests")` |
| `counter.add(value, attributes={})` | Counterに加算 | `c.add(1, {"endpoint":"/plan"})` |
| `meter.create_histogram(name, unit="", description="")` | Histogram作成 | `h = meter.create_histogram("app.duration", unit="ms")` |
| `histogram.record(value, attributes={})` | Histogramに記録 | `h.record(120.5, {"endpoint":"/plan"})` |
| `meter.create_up_down_counter(name, unit="", description="")` | UpDownCounter作成 | インフライトリクエスト数等 |
| `meter.create_observable_gauge(name, callbacks, ...)` | Gauge（非同期） | コールバックで瞬間値を返す |

Prometheus変換後の命名:
- Counter `app.requests` → `app_requests_total`
- Histogram `app.duration` (unit=ms) → `app_duration_milliseconds_bucket` / `_sum` / `_count`
- UpDownCounter `app.inflight` → `app_inflight`
- ドット→アンダースコア、`-` → `_` への正規化が入る

## B.4 Logging統合の早見

Python標準 `logging` にOTel Logsを重ねる最小パターンをリストB.2に示す。

**リストB.2: logging統合の初期化**

```python
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
import logging

lp = LoggerProvider(resource=resource)
lp.add_log_record_processor(BatchLogRecordProcessor(
    OTLPLogExporter(endpoint=endpoint, insecure=True)))
set_logger_provider(lp)

# 標準logging に OTel Handler を追加
handler = LoggingHandler(level=logging.NOTSET, logger_provider=lp)
logging.getLogger().addHandler(handler)

# アプリ側は通常の logging 呼び出し
log = logging.getLogger("my-app")
log.info("request done items=%d", items_count)  # OTLP Logsとして自動送信
```

ポイント:
- `LoggingHandler` は現在のSpanContextから `trace_id`／`span_id` を自動付与する
- アプリコードは `log.info(...)` などを普通に呼ぶだけで良い
- Lokiで `{service_name="..."} | json` で `trace_id` を取り出し、Tempoと横断デバッグが可能

## B.5 OpenLLMetry初期化の早見

Traceloop SDK（OpenLLMetry）は既存のOTel TracerProviderを再利用する形で上に乗せる。代表的なオプションを表B.3に示す。

*表B.3: `Traceloop.init()` の主要オプション*

| パラメータ／環境変数 | 役割 | 典型値 |
|-------------------|------|--------|
| `app_name` | 表示／Resource属性用のアプリ名 | `"travel-helper"` |
| `api_endpoint` | 送信先OTLPエンドポイント。未指定でTraceloop Cloud宛になるため必須級 | `"http://otel-collector:4318"` |
| `disable_batch` | バッチ処理の無効化 | `False`（本番）／ `True`（開発／即時可視化） |
| `instruments` | 有効にするinstrumentationを限定 | 省略時は利用可能な全instrumentationをロード |
| `exporter` | 独自Exporterを使う | 通常は未指定 |
| 環境変数 `TRACELOOP_TRACE_CONTENT` | プロンプト／レスポンス本文のキャプチャ | デフォルト `true`。本番では `false` 検討 |
| 環境変数 `TRACELOOP_BASE_URL` | `api_endpoint` の代替（環境変数経由） | `"http://otel-collector:4318"` |

**リストB.3: 本書で使う構成のTraceloop初期化**

```python
from traceloop.sdk import Traceloop
import os

# 前提: OTel SDK（TracerProvider/MeterProvider/LoggerProvider）は既に初期化済み
Traceloop.init(
    app_name=os.environ.get("OTEL_SERVICE_NAME", "travel-helper"),
    api_endpoint=os.environ.get(
        "TRACELOOP_BASE_URL",
        "http://otel-gateway-opentelemetry-collector.observability:4318"),
    disable_batch=False,
)
```

順序は「OTel SDK初期化を先、`Traceloop.init()` を後」とする。Traceloopはグローバル `TracerProvider` を検出して再利用する設計のため、この順序を守れば手動計装と自動計装が同じTraceContextを共有する。

---

次の付録Cでは、本書で使う用語の定義を本文と同じ紙面に収録する。
