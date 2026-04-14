"""Langfuse SDK initialization for ch11.

Credentials（LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY / LANGFUSE_HOST）が
未設定の場合は None を返し、ランタイム側で記録をスキップする。
"""
from __future__ import annotations

import logging
import os
from typing import Optional

log = logging.getLogger(__name__)


def init_langfuse() -> Optional[object]:
    host = os.environ.get("LANGFUSE_HOST")
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    if not (host and public_key and secret_key):
        log.warning("Langfuse credentials not set; skipping Langfuse recording")
        return None
    try:
        # Langfuse SDK v2 系の API。v3 系では trace/span を OTel 準拠にする別APIになる
        from langfuse import Langfuse

        return Langfuse(public_key=public_key, secret_key=secret_key, host=host)
    except ImportError as exc:
        log.error("langfuse package not installed: %s", exc)
        return None
    except Exception as exc:  # noqa: BLE001
        log.error("Failed to init Langfuse: %s", exc)
        return None
