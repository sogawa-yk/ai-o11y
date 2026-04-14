"""Stub tools for ch15 (same as ch13 but without random errors for stable E2E demo)."""
from __future__ import annotations

import random
import time

from opentelemetry import trace

tracer = trace.get_tracer("travel-helper-ch15.tools")


def weather_tool(city: str, days: int) -> str:
    with tracer.start_as_current_span("tool.weather") as span:
        span.set_attribute("tool.name", "weather")
        span.set_attribute("tool.city", city)
        span.set_attribute("tool.days", days)
        time.sleep(random.uniform(0.1, 0.2))
        return f"{city}は晴れ予報"


def places_tool(city: str, keyword: str) -> list[str]:
    with tracer.start_as_current_span("tool.places") as span:
        span.set_attribute("tool.name", "places")
        span.set_attribute("tool.city", city)
        span.set_attribute("tool.keyword", keyword)
        time.sleep(random.uniform(0.1, 0.2))
        return [f"{city}{keyword}スポット{i}" for i in range(1, 4)]
