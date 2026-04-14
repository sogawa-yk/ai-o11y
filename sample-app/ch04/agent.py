"""travel-helper ch04: minimal Span emitter (plan_stage only)."""
from __future__ import annotations

import logging
import os
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from otel_setup import init_tracer

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("travel-helper-ch04")

tracer = init_tracer(service_name=os.environ.get("OTEL_SERVICE_NAME", "travel-helper-ch04"))

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
    return {"status": "ok"}


@app.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest) -> PlanResponse:
    with tracer.start_as_current_span("stage.plan") as span:
        span.set_attribute("user.city", req.city)
        span.set_attribute("user.days", req.days)
        span.set_attribute("user.keywords_count", len(req.keywords))
        ctx = span.get_span_context()
        trace_id_hex = format(ctx.trace_id, "032x")
        items = [f"{kw}関連スポット" for kw in req.keywords] or ["市内中心部の主要観光"]
        itinerary = (
            f"{req.city} {req.days}日間プラン: " + " / ".join(items)
        )
        span.set_attribute("travel_helper.investigation_items_count", len(items))
        log.info("plan_stage done trace_id=%s items=%d", trace_id_hex, len(items))
        return PlanResponse(itinerary=itinerary, trace_id=trace_id_hex)
