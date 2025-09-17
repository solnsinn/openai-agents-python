from __future__ import annotations

from typing import TypedDict, Any


class ResponseAudioDeltaEvent(TypedDict, total=False):
    type: str
    audio: Any
    item_id: str
    content_index: int


__all__ = ["ResponseAudioDeltaEvent"]
