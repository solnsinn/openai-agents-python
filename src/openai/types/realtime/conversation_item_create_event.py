"""Shim for ConversationItemCreateEvent used in tests."""
from __future__ import annotations

from typing import Any, Optional

try:
    from pydantic import BaseModel

    class ConversationItemCreateEvent(BaseModel):
        type: Optional[str] = None
        item: Optional[Any] = None

except Exception:
    class ConversationItemCreateEvent:
        def __init__(self, type: Any = None, item: Any = None):
            self.type = type
            self.item = item


__all__ = ["ConversationItemCreateEvent"]
