from __future__ import annotations

from typing import TypedDict


class ResponseReasoningTextDoneEvent(TypedDict, total=False):
    item_id: str
    output_index: int
    summary_index: int


__all__ = ["ResponseReasoningTextDoneEvent"]
