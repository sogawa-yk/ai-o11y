"""LLM client wrapper with OCI GenAI / mock modes."""
from __future__ import annotations

import logging
import os
from typing import List

log = logging.getLogger(__name__)


def _mode() -> str:
    return os.environ.get("LLM_MODE", "mock")


class LLMClient:
    def __init__(self) -> None:
        self.mode = _mode()
        self.model = os.environ.get("OCI_GENAI_MODEL", "xai.grok-3")
        self.client = None  # oci初期化失敗時の安全側デフォルト
        if self.mode == "oci":
            try:
                from openai import OpenAI  # noqa: F401

                self.client = OpenAI(
                    base_url=os.environ["OCI_GENAI_ENDPOINT"],
                    api_key=os.environ["OCI_GENAI_API_KEY"],
                )
            except Exception as exc:  # noqa: BLE001
                log.error("OCI GenAI client init failed: %s. Falling back to mock.", exc)
                self.mode = "mock"

    def chat(self, messages: List[dict]) -> str:
        if self.mode == "oci":
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return resp.choices[0].message.content or ""
        # mock
        last = messages[-1]["content"] if messages else ""
        return f"[mock応答] 入力長={len(last)}文字"
