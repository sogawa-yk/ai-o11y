"""Ch14: OTel SDK + Traceloop (OpenLLMetry) initialization."""
from __future__ import annotations

import logging
import os
from typing import Tuple

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


def _endpoint() -> str:
    return os.environ.get(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://otel-gateway-opentelemetry-collector.observability:4317",
    )


def init_otel(service_name: str) -> Tuple[trace.Tracer, metrics.Meter]:
    """OTel SDKをまず初期化（TracerProvider/MeterProvider/LoggerProvider）。"""
    resource = Resource.create(
        {"service.name": service_name, "service.namespace": "aio11y-book"}
    )

    tp = TracerProvider(resource=resource)
    tp.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=_endpoint(), insecure=True))
    )
    trace.set_tracer_provider(tp)

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=_endpoint(), insecure=True),
        export_interval_millis=10_000,
    )
    mp = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(mp)

    lp = LoggerProvider(resource=resource)
    lp.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(endpoint=_endpoint(), insecure=True))
    )
    set_logger_provider(lp)
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=lp)
    logging.getLogger().addHandler(handler)

    return trace.get_tracer(service_name), metrics.get_meter(service_name)


def init_traceloop(service_name: str) -> None:
    """OTel SDK初期化後にOpenLLMetryを重ねる。

    Traceloop.init() は既存のTracerProviderを検出して共存する設計。
    既存TracerProviderがあればそれを使うため、第13章の構成にinstrumentationだけが
    追加される形になる。
    """
    try:
        from traceloop.sdk import Traceloop

        # Traceloopはデフォルトで Traceloop Cloud に送ろうとするため、
        # api_endpoint を Collector のOTLP/HTTP エンドポイントに明示する。
        # これによりOpenLLMetryのinstrumentationも既存のCollector経路に合流する。
        api_endpoint = os.environ.get(
            "TRACELOOP_BASE_URL",
            "http://otel-gateway-opentelemetry-collector.observability:4318",
        )
        Traceloop.init(
            app_name=service_name,
            api_endpoint=api_endpoint,
            disable_batch=False,
        )
    except Exception as exc:  # noqa: BLE001
        logging.getLogger(__name__).error("Traceloop.init failed: %s", exc)
