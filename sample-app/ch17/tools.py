"""Stub tool implementations for travel-helper ch17."""
from __future__ import annotations

import random
import time

from opentelemetry import trace

tracer = trace.get_tracer("travel-helper-ch17.tools")


class ToolError(RuntimeError):
    """ツール内部で発生した回復不能なエラー。"""


def _maybe_raise(tool_name: str) -> None:
    # 5%確率で意図的なエラー（Observability観測対象として）
    if random.random() < 0.05:
        raise ToolError(f"{tool_name}: stub error for observation")


def weather_tool(city: str, days: int) -> str:
    with tracer.start_as_current_span("tool.weather") as span:
        span.set_attribute("tool.name", "weather")
        span.set_attribute("tool.city", city)
        span.set_attribute("tool.days", days)
        try:
            time.sleep(random.uniform(0.1, 0.2))
            _maybe_raise("weather")
            return f"{city}は晴れ予報"
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
            raise


def places_tool(city: str, keyword: str) -> list[str]:
    with tracer.start_as_current_span("tool.places") as span:
        span.set_attribute("tool.name", "places")
        span.set_attribute("tool.city", city)
        span.set_attribute("tool.keyword", keyword)
        try:
            time.sleep(random.uniform(0.15, 0.3))
            _maybe_raise("places")
            return [f"{city}{keyword}スポット{i}" for i in range(1, 4)]
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
            raise


def restaurant_tool(city: str) -> list[str]:
    with tracer.start_as_current_span("tool.restaurant") as span:
        span.set_attribute("tool.name", "restaurant")
        span.set_attribute("tool.city", city)
        try:
            time.sleep(random.uniform(0.1, 0.2))
            _maybe_raise("restaurant")
            return [f"{city}レストラン{i}" for i in range(1, 4)]
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
            raise
