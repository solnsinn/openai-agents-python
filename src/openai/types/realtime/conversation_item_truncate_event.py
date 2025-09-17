"""Shim for ConversationItemTruncateEvent used in tests."""
from __future__ import annotations

from typing import Optional, Any

try:
    from pydantic import BaseModel

    class ConversationItemTruncateEvent(BaseModel):
        type: Optional[str] = None
        item_id: Optional[str] = None
        content_index: Optional[int] = None
        audio_end_ms: Optional[int] = None

except Exception:
    class ConversationItemTruncateEvent:
        def __init__(self, type: Any = None, item_id: Any = None, content_index: Any = None, audio_end_ms: Any = None):
            self.type = type
            self.item_id = item_id
            self.content_index = content_index
            self.audio_end_ms = audio_end_ms


__all__ = ["ConversationItemTruncateEvent"]
