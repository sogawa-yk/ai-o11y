"""travel-helper ch05: 3-signal demo (plan + simple gather)."""
from __future__ import annotations

import logging
import os
import random
import time
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from otel_setup import init_otel

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("travel-helper-ch05")

tracer, meter = init_otel(
    service_name=os.environ.get("OTEL_SERVICE_NAME", "travel-helper-ch05")
)

requests_counter = meter.create_counter(
    "travel_helper.requests",
    description="Total number of /plan requests",
)
duration_hist = meter.create_histogram(
    "travel_helper.request.duration",
    unit="ms",
    description="End-to-end /plan request duration",
)

app = FastAPI()


class PlanRequest(BaseModel):
    city: str = Field(..., min_length=1)
    days: int = Field(..., ge=1, le=14)
    keywords: List[str] = Field(default_factory=list)


class PlanResponse(BaseModel):
    itinerary: str
    trace_id: str


def weather_tool(city: str, days: int) -> str:
    with tracer.start_as_current_span("tool.weather") as span:
        span.set_attribute("tool.city", city)
        span.set_attribute("tool.days", days)
        time.sleep(random.uniform(0.1, 0.2))
        return f"{city}は晴れ予報"


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest) -> PlanResponse:
    start = time.perf_counter()
    with tracer.start_as_current_span("handle_plan") as root:
        root.set_attribute("user.city", req.city)
        root.set_attribute("user.days", req.days)
        root.set_attribute("user.keywords_count", len(req.keywords))
        ctx = root.get_span_context()
        trace_id_hex = format(ctx.trace_id, "032x")

        with tracer.start_as_current_span("stage.plan") as span:
            items = [f"{kw}関連スポット" for kw in req.keywords] or ["市内中心部"]
            span.set_attribute("travel_helper.investigation_items_count", len(items))
            log.info("plan_stage decided items=%d", len(items))

        with tracer.start_as_current_span("stage.gather") as span:
            forecast = weather_tool(req.city, req.days)
            span.set_attribute("travel_helper.forecast_chars", len(forecast))
            log.info("gather_stage done forecast=%s", forecast)

        itinerary = f"{req.city} {req.days}日間: {forecast} / " + " / ".join(items)
    elapsed_ms = (time.perf_counter() - start) * 1000
    requests_counter.add(1, {"endpoint": "/plan"})
    duration_hist.record(elapsed_ms, {"endpoint": "/plan"})
    log.info("request done trace_id=%s elapsed_ms=%.1f", trace_id_hex, elapsed_ms)
    return PlanResponse(itinerary=itinerary, trace_id=trace_id_hex)
