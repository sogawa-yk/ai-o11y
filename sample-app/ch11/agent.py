"""travel-helper ch11: OTel + Langfuse SDK for LLM quality observation.

本章のサンプルは ch05 をベースに Langfuse SDK を追加する。
Langfuse credentials (LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY / LANGFUSE_HOST)
は Langfuse Web UI でプロジェクトを作成して取得する。
"""
from __future__ import annotations

import logging
import os
import random
import time
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from langfuse_setup import init_langfuse
from otel_setup import init_otel

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("travel-helper-ch11")

tracer, _meter = init_otel(os.environ.get("OTEL_SERVICE_NAME", "travel-helper-ch11"))
langfuse = init_langfuse()

app = FastAPI()


class PlanRequest(BaseModel):
    city: str = Field(..., min_length=1)
    days: int = Field(..., ge=1, le=14)
    keywords: List[str] = Field(default_factory=list)


class PlanResponse(BaseModel):
    itinerary: str
    trace_id: str


def simple_llm_judge(itinerary: str, req: PlanRequest) -> float:
    """最小限のLLM-as-judge疑似実装。

    本番ではLLMを呼んで採点する。ここでは長さとキーワード包含率で簡易採点する。
    """
    score = min(len(itinerary) / 80.0, 1.0) * 0.5
    if req.keywords:
        hit = sum(1 for kw in req.keywords if kw in itinerary) / len(req.keywords)
        score += hit * 0.5
    return round(score, 2)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest) -> PlanResponse:
    start = time.perf_counter()
    with tracer.start_as_current_span("handle_plan") as root:
        root.set_attribute("user.city", req.city)
        root.set_attribute("user.days", req.days)
        trace_id_hex = format(root.get_span_context().trace_id, "032x")

        with tracer.start_as_current_span("stage.plan"):
            items = [f"{kw}関連スポット" for kw in req.keywords] or ["市内中心部"]

        with tracer.start_as_current_span("stage.gather"):
            time.sleep(random.uniform(0.05, 0.15))
            forecast = f"{req.city}は晴れ"

        itinerary = f"{req.city} {req.days}日間: {forecast} / " + " / ".join(items)

    elapsed_ms = (time.perf_counter() - start) * 1000
    score = simple_llm_judge(itinerary, req)

    # Langfuse側のトレース記録（OTel trace_idをmetadataに含める）
    if langfuse is not None:
        lf_trace = langfuse.trace(
            name="travel-helper.plan",
            user_id=req.city,
            metadata={
                "otel_trace_id": trace_id_hex,
                "keywords_count": len(req.keywords),
            },
            input={"city": req.city, "days": req.days, "keywords": req.keywords},
            output={"itinerary": itinerary},
        )
        lf_trace.span(
            name="stage.plan",
            input={"keywords": req.keywords},
            output={"items_count": len(items)},
        )
        lf_trace.span(
            name="stage.gather",
            input={"city": req.city, "days": req.days},
            output={"forecast": forecast},
        )
        lf_trace.score(name="judge.quality", value=score, comment="simple rule-based judge")

    log.info("plan done trace_id=%s score=%.2f elapsed_ms=%.1f", trace_id_hex, score, elapsed_ms)
    return PlanResponse(itinerary=itinerary, trace_id=trace_id_hex)
