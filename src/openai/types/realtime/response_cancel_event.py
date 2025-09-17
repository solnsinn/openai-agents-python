from __future__ import annotations

from typing import TypedDict, Any


class ResponseCancelEvent(TypedDict, total=False):
    type: str
    id: str
    reason: Any


__all__ = ["ResponseCancelEvent"]
