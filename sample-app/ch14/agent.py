"""travel-helper ch14: manual + automatic (OpenLLMetry) instrumentation."""
from __future__ import annotations

import logging
import os
import time
from typing import List

from fastapi import FastAPI
from opentelemetry import trace
from pydantic import BaseModel, Field

from llm import LLMClient
from otel_setup import init_otel, init_traceloop
from tools import places_tool, weather_tool

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("travel-helper-ch14")

# 初期化順: まずOTel SDK、次にTraceloop（既存TracerProviderを再利用）
tracer, meter = init_otel(os.environ.get("OTEL_SERVICE_NAME", "travel-helper-ch14"))
init_traceloop(os.environ.get("OTEL_SERVICE_NAME", "travel-helper-ch14"))

llm = LLMClient()

requests_counter = meter.create_counter(
    "travel_helper.requests", description="Total /plan requests"
)
duration_hist = meter.create_histogram(
    "travel_helper.request.duration", unit="ms", description="End-to-end /plan request duration"
)

app = FastAPI()


class PlanRequest(BaseModel):
    city: str = Field(..., min_length=1)
    days: int = Field(..., ge=1, le=14)
    keywords: List[str] = Field(default_factory=list)


class PlanResponse(BaseModel):
    itinerary: str
    trace_id: str


@app.get("/healthz")
def healthz():
    return {"status": "ok", "llm_mode": llm.mode}


@app.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest) -> PlanResponse:
    start = time.perf_counter()
    with tracer.start_as_current_span("handle_plan_request") as root:
        root.set_attribute("user.city", req.city)
        root.set_attribute("user.days", req.days)
        trace_id_hex = format(root.get_span_context().trace_id, "032x")

        # stage.plan: LLMで調査項目を決める（OpenLLMetryがopenai呼び出しを自動Span化）
        with tracer.start_as_current_span("stage.plan") as span:
            prompt = (
                f"{req.city}の{req.days}日間プラン用にキーワード{req.keywords}を踏まえた"
                "調査項目を3つ挙げて。"
            )
            try:
                plan_text = llm.chat([{"role": "user", "content": prompt}])
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
                raise
            span.set_attribute("travel_helper.plan.prompt_chars", len(prompt))
            span.set_attribute("travel_helper.plan.response_chars", len(plan_text))

        # stage.gather: ツール呼び出し
        with tracer.start_as_current_span("stage.gather") as span:
            forecast = weather_tool(req.city, req.days)
            places: List[str] = []
            for kw in req.keywords[:2]:
                places.extend(places_tool(req.city, kw))
            span.set_attribute("travel_helper.gather.places_count", len(places))

        # stage.synthesize: LLMで最終応答生成（2回目のLLM呼び出しも自動Span化）
        with tracer.start_as_current_span("stage.synthesize") as span:
            synth_prompt = (
                f"{req.city} {req.days}日間のプランを{plan_text}と{forecast}"
                f"と{places}をもとに1段落で作成して。"
            )
            try:
                itinerary = llm.chat([{"role": "user", "content": synth_prompt}])
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
                raise
            span.set_attribute("travel_helper.itinerary.chars", len(itinerary))

    elapsed_ms = (time.perf_counter() - start) * 1000
    requests_counter.add(1, {"endpoint": "/plan"})
    duration_hist.record(elapsed_ms, {"endpoint": "/plan"})
    log.info("request done trace_id=%s elapsed_ms=%.1f", trace_id_hex, elapsed_ms)
    return PlanResponse(itinerary=itinerary, trace_id=trace_id_hex)
