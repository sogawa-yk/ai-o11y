"""travel-helper ch17: complete manual instrumentation (Span / Metric / Log / Exception)."""
from __future__ import annotations

import logging
import os
import time
from typing import List

from fastapi import FastAPI
from opentelemetry import trace
from pydantic import BaseModel, Field

from otel_setup import init_otel
from tools import ToolError, places_tool, restaurant_tool, weather_tool

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("travel-helper-ch17")

tracer, meter = init_otel(os.environ.get("OTEL_SERVICE_NAME", "travel-helper-ch17"))

# Metric一覧（development-guidelines準拠）
requests_counter = meter.create_counter(
    "travel_helper.requests",
    description="Total /plan requests",
)
errors_counter = meter.create_counter(
    "travel_helper.errors",
    description="Requests that raised an exception",
)
duration_hist = meter.create_histogram(
    "travel_helper.request.duration",
    unit="ms",
    description="End-to-end /plan request duration",
)
tool_errors_counter = meter.create_counter(
    "travel_helper.tool.errors",
    description="Tool-level errors (kept recorded, not user-failing)",
)
# ch17で追加: LLMトークン消費のHistogram（direction=input/output のラベル付き）
llm_tokens_hist = meter.create_histogram(
    "travel_helper.llm.tokens",
    unit="tokens",
    description="LLM token usage per call (direction=input/output)",
)

app = FastAPI()


class PlanRequest(BaseModel):
    city: str = Field(..., min_length=1)
    days: int = Field(..., ge=1, le=14)
    keywords: List[str] = Field(default_factory=list)


class PlanResponse(BaseModel):
    itinerary: str
    trace_id: str


def _record_llm_tokens(input_tokens: int, output_tokens: int, model: str) -> None:
    """ch17で追加: LLM呼び出しのトークン消費をHistogramに記録。"""
    llm_tokens_hist.record(input_tokens, {"direction": "input", "model": model})
    llm_tokens_hist.record(output_tokens, {"direction": "output", "model": model})


def _plan_stage(req: PlanRequest) -> List[str]:
    with tracer.start_as_current_span("stage.plan") as span:
        span.set_attribute("travel_helper.stage", "plan")
        items = [f"{kw}関連スポット" for kw in req.keywords] or ["市内中心部の主要観光"]
        span.set_attribute("travel_helper.investigation_items_count", len(items))
        # ch17で追加: LLM呼び出しの代わりにトークン数を擬似算出して記録
        prompt_chars = sum(len(kw) for kw in req.keywords) + 20
        response_chars = len(items) * 20
        _record_llm_tokens(prompt_chars // 3, response_chars // 3, "mock-model")
        log.info("plan_stage decided items=%d", len(items))
        return items


def _gather_stage(req: PlanRequest, items: List[str]) -> dict:
    with tracer.start_as_current_span("stage.gather") as span:
        span.set_attribute("travel_helper.stage", "gather")
        forecast = None
        places: List[str] = []
        restaurants: List[str] = []

        try:
            forecast = weather_tool(req.city, req.days)
        except ToolError as exc:
            tool_errors_counter.add(1, {"tool": "weather"})
            log.warning("weather_tool failed: %s", exc)

        for kw in req.keywords[:2]:
            try:
                places.extend(places_tool(req.city, kw))
            except ToolError as exc:
                tool_errors_counter.add(1, {"tool": "places"})
                log.warning("places_tool failed: %s", exc)

        try:
            restaurants = restaurant_tool(req.city)
        except ToolError as exc:
            tool_errors_counter.add(1, {"tool": "restaurant"})
            log.warning("restaurant_tool failed: %s", exc)

        span.set_attribute("travel_helper.gather.forecast_ok", forecast is not None)
        span.set_attribute("travel_helper.gather.places_count", len(places))
        span.set_attribute("travel_helper.gather.restaurants_count", len(restaurants))
        return {"forecast": forecast, "places": places, "restaurants": restaurants}


def _synthesize_stage(req: PlanRequest, items: List[str], gathered: dict) -> str:
    with tracer.start_as_current_span("stage.synthesize") as span:
        span.set_attribute("travel_helper.stage", "synthesize")
        pieces = [f"{req.city} {req.days}日間プラン"]
        if gathered["forecast"]:
            pieces.append(gathered["forecast"])
        pieces.extend(items[:3])
        pieces.extend(gathered["places"][:3])
        pieces.extend(gathered["restaurants"][:3])
        text = " / ".join(pieces)
        span.set_attribute("travel_helper.itinerary.chars", len(text))
        return text


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest) -> PlanResponse:
    start = time.perf_counter()
    with tracer.start_as_current_span("handle_plan_request") as root:
        root.set_attribute("user.city", req.city)
        root.set_attribute("user.days", req.days)
        root.set_attribute("user.keywords_count", len(req.keywords))
        trace_id_hex = format(root.get_span_context().trace_id, "032x")
        try:
            items = _plan_stage(req)
            gathered = _gather_stage(req, items)
            itinerary = _synthesize_stage(req, items, gathered)
        except Exception as exc:
            root.record_exception(exc)
            root.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
            errors_counter.add(1, {"endpoint": "/plan"})
            raise

    elapsed_ms = (time.perf_counter() - start) * 1000
    requests_counter.add(1, {"endpoint": "/plan"})
    duration_hist.record(elapsed_ms, {"endpoint": "/plan"})
    log.info(
        "request done trace_id=%s elapsed_ms=%.1f itinerary_chars=%d",
        trace_id_hex,
        elapsed_ms,
        len(itinerary),
    )
    return PlanResponse(itinerary=itinerary, trace_id=trace_id_hex)
